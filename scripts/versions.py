#!/usr/bin/env python3
"""Build data/versions.json from the omacom/omarchy GitHub releases.

Uses the authenticated `gh` CLI. Each release keeps its full markdown body; the
ISO download URL and SHA256 checksum are pulled out of it when present.

If `gh` is unavailable and data/versions.json already exists, the existing file
is kept so the pipeline stays idempotent offline.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import (  # noqa: E402
    DATA_DIR,
    REPO,
    available_tags,
    write_json,
)

OUT_PATH = DATA_DIR / "versions.json"

SHA256_RE = re.compile(r"SHA-?256\s*[:=]\s*\**\s*`?([0-9a-fA-F]{64})`?")
ISO_URL_RE = re.compile(r"https://iso\.omarchy\.org/[^\s)\]\"'>]+")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+.*$", re.M)
SUMMARY_LEN = 300


def fetch_releases() -> list[dict]:
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases", "--paginate"],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    if isinstance(payload, dict):
        payload = [payload]
    return payload


def summarise(body: str) -> str:
    text = HEADING_RE.sub("", body or "")
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= SUMMARY_LEN:
        return text
    return text[:SUMMARY_LEN].rstrip()


def build_release(raw: dict) -> dict:
    body = raw.get("body") or ""
    sha = SHA256_RE.search(body)
    iso = ISO_URL_RE.search(body)
    return {
        "body": body,
        "date": raw.get("published_at") or raw.get("created_at"),
        "isoUrl": iso.group(0).rstrip(".,;:") if iso else None,
        "name": raw.get("name") or raw.get("tag_name"),
        "prerelease": bool(raw.get("prerelease")),
        "sha256": sha.group(1).lower() if sha else None,
        "summary": summarise(body),
        "tag": raw.get("tag_name"),
        "url": raw.get("html_url"),
    }


def main() -> int:
    try:
        raw_releases = fetch_releases()
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        if OUT_PATH.is_file():
            print(f"  versions  gh unavailable ({exc}); keeping existing "
                  f"{OUT_PATH.relative_to(DATA_DIR.parent)}", file=sys.stderr)
            return 0
        print(f"  versions  gh failed and no cached file: {exc}", file=sys.stderr)
        return 1

    releases = [build_release(r) for r in raw_releases]
    releases.sort(key=lambda r: (r["date"] or "", r["tag"] or ""), reverse=True)

    stable = [r for r in releases if not r["prerelease"]]
    tags_in_data = available_tags()

    write_json(
        OUT_PATH,
        {
            "count": len(releases),
            "latest": stable[0]["tag"] if stable else None,
            "releases": releases,
            "repo": REPO,
            "tagsInData": tags_in_data,
        },
    )

    missing = [t for t in tags_in_data if t not in {r["tag"] for r in releases}]
    print(
        f"  versions  {len(releases):>4} releases, latest="
        f"{stable[0]['tag'] if stable else 'n/a'}, "
        f"{sum(1 for r in releases if r['sha256'])} with sha256, "
        f"{sum(1 for r in releases if r['isoUrl'])} with iso url"
    )
    if missing:
        print(f"            snapshots without a matching release: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
