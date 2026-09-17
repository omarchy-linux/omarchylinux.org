#!/usr/bin/env python3
"""
Fetch every issue and discussion from github.com/omacom/omarchy via the
authenticated `gh` CLI (GraphQL API) into data/issues/raw.json and
data/issues/raw_discussions.json.

Pages are cached incrementally to data/issues/raw_cache_*.jsonl so a rerun with
--resume picks up where an interrupted run stopped.

Usage:
    python3 scripts/fetch_issues.py [--resume] [--issues-only] [--discussions-only]

Requires: Python 3.12 stdlib + `gh` (authenticated).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_OWNER = "omacom"
REPO_NAME = "omarchy"

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "issues"
# Cache files live beside the outputs and match the gitignored "raw*.json*" pattern.
CACHE_DIR = OUT_DIR

BODY_LIMIT = 4000
COMMENT_LIMIT = 300
COMMENT_SEARCH_LIMIT = 800    # per comment, for the searchable thread blob
THREAD_TEXT_LIMIT = 8000      # per issue, for the searchable thread blob
DISCUSSION_BODY_LIMIT = 1500
ANSWER_LIMIT = 500

PAGE_SIZE = 100
MAX_RETRIES = 6
RATE_FLOOR = 200  # sleep when fewer graphql points than this remain

ISSUES_QUERY = """
query($owner: String!, $name: String!, $cursor: String, $pageSize: Int!) {
  rateLimit { cost remaining resetAt nodeCount }
  repository(owner: $owner, name: $name) {
    issues(first: $pageSize, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      totalCount
      nodes {
        number
        title
        url
        state
        stateReason
        createdAt
        closedAt
        updatedAt
        author { login }
        labels(first: 20) { nodes { name } }
        comments { totalCount }
        reactions { totalCount }
        body
        recentComments: comments(last: 5) {
          nodes { author { login } createdAt url body }
        }
        allComments: comments(first: 50) {
          nodes { body }
        }
        timelineItems(itemTypes: [CLOSED_EVENT, CROSS_REFERENCED_EVENT, CONNECTED_EVENT], first: 20) {
          nodes {
            __typename
            ... on ClosedEvent {
              createdAt
              closer {
                __typename
                ... on PullRequest { number title url merged mergedAt }
                ... on Commit { oid url }
              }
            }
            ... on CrossReferencedEvent {
              createdAt
              source {
                __typename
                ... on PullRequest { number title url merged mergedAt }
                ... on Issue { number title url }
              }
            }
            ... on ConnectedEvent {
              createdAt
              subject {
                __typename
                ... on PullRequest { number title url merged mergedAt }
                ... on Issue { number title url }
              }
            }
          }
        }
      }
    }
  }
}
"""

DISCUSSIONS_QUERY = """
query($owner: String!, $name: String!, $cursor: String, $pageSize: Int!) {
  rateLimit { cost remaining resetAt nodeCount }
  repository(owner: $owner, name: $name) {
    discussions(first: $pageSize, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      totalCount
      nodes {
        number
        title
        url
        createdAt
        updatedAt
        upvoteCount
        isAnswered
        category { name }
        author { login }
        comments { totalCount }
        answer { body url createdAt author { login } }
        topComments: comments(first: 3) {
          nodes { author { login } url createdAt upvoteCount body }
        }
        body
      }
    }
  }
}
"""


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}", flush=True)


def truncate(text: str | None, limit: int) -> tuple[str, bool]:
    if not text:
        return "", False
    text = text.replace("\r\n", "\n")
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def run_graphql(query: str, variables: dict) -> dict:
    """Run a GraphQL query through `gh api graphql`, retrying on transient errors."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            cmd += ["-F", f"{key}=null"]
        elif isinstance(value, bool):
            cmd += ["-F", f"{key}={'true' if value else 'false'}"]
        elif isinstance(value, int):
            cmd += ["-F", f"{key}={value}"]
        else:
            cmd += ["-f", f"{key}={value}"]

    last_err = ""
    for attempt in range(1, MAX_RETRIES + 1):
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            try:
                payload = json.loads(proc.stdout)
            except json.JSONDecodeError as exc:
                last_err = f"bad json: {exc}"
            else:
                if "errors" in payload and payload.get("data") is None:
                    last_err = json.dumps(payload["errors"])[:500]
                else:
                    if "errors" in payload:
                        log(f"  partial errors: {json.dumps(payload['errors'])[:300]}")
                    return payload
        else:
            last_err = (proc.stderr or proc.stdout)[:500]

        wait = min(60, 2 ** attempt)
        log(f"  retry {attempt}/{MAX_RETRIES} after error: {last_err[:200]} (sleep {wait}s)")
        time.sleep(wait)

    raise RuntimeError(f"GraphQL failed after {MAX_RETRIES} attempts: {last_err}")


def check_rate_limit(rate: dict | None) -> None:
    """Sleep until reset when the GraphQL budget is nearly exhausted."""
    if not rate:
        return
    remaining = rate.get("remaining")
    if remaining is None or remaining > RATE_FLOOR:
        return
    reset_at = rate.get("resetAt")
    try:
        reset = datetime.fromisoformat(reset_at.replace("Z", "+00:00"))
        wait = (reset - datetime.now(timezone.utc)).total_seconds() + 5
    except Exception:
        wait = 60.0
    wait = max(5.0, min(wait, 3700.0))
    log(f"  rate limit low ({remaining} left) - sleeping {int(wait)}s until reset")
    time.sleep(wait)


def rate_limit_snapshot() -> dict:
    proc = subprocess.run(["gh", "api", "rate_limit"], capture_output=True, text=True)
    if proc.returncode != 0:
        return {}
    try:
        return json.loads(proc.stdout).get("resources", {}).get("graphql", {})
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------- normalizers

def norm_pr_ref(node: dict | None) -> dict | None:
    """Normalize a PullRequest / Issue / Commit reference node."""
    if not node:
        return None
    kind = node.get("__typename")
    if kind == "PullRequest":
        return {
            "type": "pull_request",
            "number": node.get("number"),
            "title": node.get("title"),
            "url": node.get("url"),
            "merged": node.get("merged"),
            "mergedAt": node.get("mergedAt"),
        }
    if kind == "Issue":
        return {
            "type": "issue",
            "number": node.get("number"),
            "title": node.get("title"),
            "url": node.get("url"),
        }
    if kind == "Commit":
        return {"type": "commit", "oid": node.get("oid"), "url": node.get("url")}
    return {"type": kind}


def normalize_issue(node: dict) -> dict:
    body, body_trunc = truncate(node.get("body"), BODY_LIMIT)
    state = node.get("state")
    comment_count = (node.get("comments") or {}).get("totalCount", 0)

    closed_by = None
    references: list[dict] = []
    seen_refs: set = set()
    for item in ((node.get("timelineItems") or {}).get("nodes") or []):
        if not item:
            continue
        kind = item.get("__typename")
        if kind == "ClosedEvent":
            ref = norm_pr_ref(item.get("closer"))
            if ref:
                ref = dict(ref)
                ref["at"] = item.get("createdAt")
                closed_by = ref
        else:
            src = item.get("source") if kind == "CrossReferencedEvent" else item.get("subject")
            ref = norm_pr_ref(src)
            if not ref or ref.get("type") != "pull_request":
                continue
            key = ("pr", ref.get("number"))
            if key in seen_refs:
                continue
            seen_refs.add(key)
            ref = dict(ref)
            ref["via"] = "cross_referenced" if kind == "CrossReferencedEvent" else "connected"
            ref["at"] = item.get("createdAt")
            references.append(ref)

    out = {
        "number": node.get("number"),
        "title": node.get("title") or "",
        "url": node.get("url"),
        "state": state,
        "stateReason": node.get("stateReason"),
        "createdAt": node.get("createdAt"),
        "closedAt": node.get("closedAt"),
        "updatedAt": node.get("updatedAt"),
        "author": ((node.get("author") or {}) or {}).get("login"),
        "labels": [l.get("name") for l in ((node.get("labels") or {}).get("nodes") or []) if l],
        "comments": comment_count,
        "reactions": (node.get("reactions") or {}).get("totalCount", 0),
        "body": body,
        "bodyTruncated": body_trunc,
        "closedBy": closed_by,
        "referencedPRs": references,
    }

    # Concatenated comment text (no metadata) so cluster/error-string searches can
    # see the whole thread, not just the opening post.
    chunks: list[str] = []
    total = 0
    for c in ((node.get("allComments") or {}).get("nodes") or []):
        if not c or not c.get("body"):
            continue
        chunk = c["body"].replace("\r\n", "\n")[:COMMENT_SEARCH_LIMIT]
        chunks.append(chunk)
        total += len(chunk)
        if total >= THREAD_TEXT_LIMIT:
            break
    out["commentsFetched"] = len(chunks)
    out["commentsText"] = "\n---\n".join(chunks)[:THREAD_TEXT_LIMIT]

    # Last 5 comments are retained for closed issues with >= 2 comments
    # (used for still-broken detection).
    if state == "CLOSED" and comment_count >= 2:
        recent = []
        for c in ((node.get("recentComments") or {}).get("nodes") or []):
            if not c:
                continue
            ctext, ctrunc = truncate(c.get("body"), COMMENT_LIMIT)
            recent.append({
                "author": ((c.get("author") or {}) or {}).get("login"),
                "createdAt": c.get("createdAt"),
                "url": c.get("url"),
                "body": ctext,
                "bodyTruncated": ctrunc,
            })
        out["recentComments"] = recent
    return out


def normalize_discussion(node: dict) -> dict:
    body, body_trunc = truncate(node.get("body"), DISCUSSION_BODY_LIMIT)
    answer = node.get("answer")
    answer_out = None
    if answer:
        atext, atrunc = truncate(answer.get("body"), ANSWER_LIMIT)
        answer_out = {
            "author": ((answer.get("author") or {}) or {}).get("login"),
            "createdAt": answer.get("createdAt"),
            "url": answer.get("url"),
            "body": atext,
            "bodyTruncated": atrunc,
        }
    top_comments = []
    for c in ((node.get("topComments") or {}).get("nodes") or []):
        if not c:
            continue
        ctext, ctrunc = truncate(c.get("body"), ANSWER_LIMIT)
        top_comments.append({
            "author": ((c.get("author") or {}) or {}).get("login"),
            "createdAt": c.get("createdAt"),
            "url": c.get("url"),
            "upvoteCount": c.get("upvoteCount", 0),
            "body": ctext,
            "bodyTruncated": ctrunc,
        })
    return {
        "number": node.get("number"),
        "title": node.get("title") or "",
        "url": node.get("url"),
        "category": ((node.get("category") or {}) or {}).get("name"),
        "createdAt": node.get("createdAt"),
        "updatedAt": node.get("updatedAt"),
        "author": ((node.get("author") or {}) or {}).get("login"),
        "upvoteCount": node.get("upvoteCount", 0),
        "comments": (node.get("comments") or {}).get("totalCount", 0),
        "isAnswered": bool(node.get("isAnswered")),
        "answer": answer_out,
        "topComments": top_comments,
        "body": body,
        "bodyTruncated": body_trunc,
    }


# ------------------------------------------------------------------ fetch loop

def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def fetch_paginated(kind: str, query: str, normalizer, resume: bool) -> list[dict]:
    """Fetch every page of a connection, caching each page to disk as JSONL."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = CACHE_DIR / f"raw_cache_{kind}.jsonl"
    state_path = CACHE_DIR / f"raw_cache_{kind}.state.json"

    state = load_state(state_path) if resume else {}
    cursor = state.get("cursor")
    records: dict[int, dict] = {}

    if resume and jsonl_path.exists():
        with jsonl_path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("number") is not None:
                    records[rec["number"]] = rec
        log(f"{kind}: resuming with {len(records)} cached records, cursor={str(cursor)[:16]}...")
    else:
        if jsonl_path.exists():
            jsonl_path.unlink()
        cursor = None

    page = state.get("pages", 0)
    total_count = state.get("totalCount")
    out_fh = jsonl_path.open("a")
    try:
        while True:
            payload = run_graphql(query, {
                "owner": REPO_OWNER,
                "name": REPO_NAME,
                "cursor": cursor,
                "pageSize": PAGE_SIZE,
            })
            data = payload.get("data") or {}
            rate = data.get("rateLimit")
            conn = ((data.get("repository") or {}) or {}).get(
                "issues" if kind == "issues" else "discussions"
            )
            if conn is None:
                raise RuntimeError(f"no {kind} connection in response: {json.dumps(payload)[:400]}")

            total_count = conn.get("totalCount", total_count)
            nodes = conn.get("nodes") or []
            for node in nodes:
                if not node:
                    continue
                rec = normalizer(node)
                if rec.get("number") is None:
                    continue
                records[rec["number"]] = rec
                out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out_fh.flush()
            os.fsync(out_fh.fileno())

            page += 1
            info = conn.get("pageInfo") or {}
            cursor = info.get("endCursor")
            state_path.write_text(json.dumps({
                "cursor": cursor,
                "pages": page,
                "records": len(records),
                "totalCount": total_count,
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            }))
            log(f"{kind}: page {page} (+{len(nodes)}) -> {len(records)}/{total_count} "
                f"[graphql remaining {(rate or {}).get('remaining')}]")

            check_rate_limit(rate)
            if not info.get("hasNextPage"):
                break
    finally:
        out_fh.close()

    result = [records[n] for n in sorted(records)]
    if total_count and abs(len(result) - total_count) > max(5, total_count * 0.02):
        log(f"WARNING {kind}: fetched {len(result)} but API reports totalCount={total_count}")
    return result


def write_json(path: Path, payload) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    tmp.replace(path)
    log(f"wrote {path} ({path.stat().st_size / 1_048_576:.1f} MB)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch omacom/omarchy issues + discussions")
    ap.add_argument("--resume", action="store_true", help="resume from the on-disk page cache")
    ap.add_argument("--issues-only", action="store_true")
    ap.add_argument("--discussions-only", action="store_true")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    snap = rate_limit_snapshot()
    log(f"graphql budget: {snap.get('remaining')}/{snap.get('limit')}")

    fetched_at = datetime.now(timezone.utc).isoformat()

    if not args.discussions_only:
        issues = fetch_paginated("issues", ISSUES_QUERY, normalize_issue, args.resume)
        open_n = sum(1 for i in issues if i["state"] == "OPEN")
        write_json(OUT_DIR / "raw.json", {
            "repo": f"{REPO_OWNER}/{REPO_NAME}",
            "fetchedAt": fetched_at,
            "count": len(issues),
            "open": open_n,
            "closed": len(issues) - open_n,
            "issues": issues,
        })
        log(f"issues: {len(issues)} total ({open_n} open / {len(issues) - open_n} closed)")

    if not args.issues_only:
        discussions = fetch_paginated(
            "discussions", DISCUSSIONS_QUERY, normalize_discussion, args.resume
        )
        write_json(OUT_DIR / "raw_discussions.json", {
            "repo": f"{REPO_OWNER}/{REPO_NAME}",
            "fetchedAt": fetched_at,
            "count": len(discussions),
            "discussions": discussions,
        })
        log(f"discussions: {len(discussions)} total")

    return 0


if __name__ == "__main__":
    sys.exit(main())
