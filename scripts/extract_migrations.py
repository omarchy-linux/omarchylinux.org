#!/usr/bin/env python3
"""Extract the migrations/ timeline from every source snapshot.

Each migrations/<unixtimestamp>.sh is summarised: its announcement echo, the
first ~40 lines of body, the config paths it touches, and the packages it adds
or drops (via omarchy-pkg-* helpers or pacman/yay directly).

Writes data/migrations/<tag>.json and data/migrations/index.json.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import (  # noqa: E402
    DATA_DIR,
    available_tags,
    is_prerelease,
    read_text,
    source_url,
    tag_dir,
    write_json,
)

OUT_DIR = DATA_DIR / "migrations"
BODY_LINES = 40

ECHO_RE = re.compile(r"""\becho\s+(?:-[A-Za-z]+\s+)*(["'])(.*?)\1""")

# Most migrations are named <unixtimestamp>.sh; a few 3.x ones add a slug.
MIGRATION_NAME_RE = re.compile(r"^(\d+)(?:_.*)?\.sh$")

PATH_RES = [
    re.compile(r"(?:~|\$HOME|\$\{HOME\})/[A-Za-z0-9._/@+-]+"),
    re.compile(r"/(?:etc|usr|var|boot|opt|srv)/[A-Za-z0-9._/@+-]+"),
]

SEGMENT_RE = re.compile(r"&&|\|\||[;|]")
LEADING_WORDS = {"sudo", "if", "then", "elif", "else", "do", "done", "!", "while",
                 "until", "command", "env", "exec", "time", "nohup"}

PKG_ADD_HELPERS = {"omarchy-pkg-add", "omarchy-pkg-aur-add", "omarchy-pkg-install"}
PKG_DROP_HELPERS = {"omarchy-pkg-drop", "omarchy-pkg-remove"}
PACMAN_LIKE = {"pacman", "yay", "paru"}


def strip_comment(line: str) -> str:
    """Drop a shell comment, ignoring '#' inside quotes."""
    out = []
    quote = None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out)


def code_lines(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        stripped = strip_comment(line).strip()
        if stripped:
            out.append(stripped)
    return out


def clean_path(value: str) -> str:
    value = value.rstrip(".,;:)\"'")
    value = re.sub(r"^\$\{HOME\}|^\$HOME", "~", value)
    return value


def find_touches(lines: list[str]) -> list[str]:
    found = set()
    for line in lines:
        for rx in PATH_RES:
            for m in rx.finditer(line):
                path = clean_path(m.group(0))
                if len(path) > 2:
                    found.add(path)
    return sorted(found)


def is_package_token(token: str) -> bool:
    if not token or token.startswith("-"):
        return False
    if "$" in token or "`" in token or "*" in token:
        return False
    if token.isdigit():
        return False
    if any(c in token for c in "/<>=\"'(){}[]"):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", token))


def split_commands(line: str) -> list[list[str]]:
    commands = []
    for segment in SEGMENT_RE.split(line):
        segment = segment.strip()
        if not segment:
            continue
        try:
            tokens = shlex.split(segment, comments=False)
        except ValueError:
            tokens = segment.split()
        # Drop leading noise words and `VAR=value` command prefixes.
        while tokens and (tokens[0] in LEADING_WORDS
                          or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0])):
            tokens = tokens[1:]
        if tokens:
            commands.append(tokens)
    return commands


def find_packages(lines: list[str]) -> tuple[list[str], list[str]]:
    added: list[str] = []
    removed: list[str] = []

    for line in lines:
        for tokens in split_commands(line):
            binary = os.path.basename(tokens[0])
            args = tokens[1:]

            if binary in PKG_ADD_HELPERS:
                added += [t for t in args if is_package_token(t)]
                continue
            if binary in PKG_DROP_HELPERS:
                removed += [t for t in args if is_package_token(t)]
                continue
            if binary not in PACMAN_LIKE:
                continue

            flags = [t for t in args if t.startswith("-")]
            operation = ""
            for flag in flags:
                if flag.startswith("--"):
                    continue
                operation = flag[1:2].upper()
                break
            if operation not in {"S", "R"}:
                continue

            # `--ask 4` style values are consumed with their flag.
            names = []
            skip_next = False
            for token in args:
                if skip_next:
                    skip_next = False
                    continue
                if token in {"--ask", "--assume-installed", "--overwrite"}:
                    skip_next = True
                    continue
                if is_package_token(token):
                    names.append(token)

            if operation == "S":
                added += names
            else:
                removed += names

    def dedupe(values):
        seen = {}
        for value in values:
            seen[value] = None
        return sorted(seen)

    return dedupe(added), dedupe(removed)


def build_migration(tag: str, path) -> dict:
    text = read_text(path)
    lines = text.splitlines()
    code = code_lines(text)
    timestamp = int(MIGRATION_NAME_RE.match(path.name).group(1))
    relpath = f"migrations/{path.name}"

    description = ""
    for line in code[:12]:
        m = ECHO_RE.search(line)
        if m and m.group(2).strip():
            description = m.group(2).strip()
            break

    added, removed = find_packages(code)

    return {
        "body": "\n".join(lines[:BODY_LINES]),
        "bodyTruncated": len(lines) > BODY_LINES,
        "date": dt.datetime.fromtimestamp(timestamp, dt.UTC).isoformat().replace("+00:00", "Z"),
        "description": description,
        "file": path.name,
        "lineCount": len(lines),
        "packagesAdded": added,
        "packagesRemoved": removed,
        "path": relpath,
        "sourceUrl": source_url(tag, relpath),
        "timestamp": timestamp,
        "touches": find_touches(code),
    }


def process_tag(tag: str) -> dict:
    migrations_dir = tag_dir(tag) / "migrations"
    records = []
    if migrations_dir.is_dir():
        for path in sorted(migrations_dir.glob("*.sh")):
            if not MIGRATION_NAME_RE.match(path.name):
                print(f"    skipping unrecognised migration name: {tag}/{path.name}",
                      file=sys.stderr)
                continue
            records.append(build_migration(tag, path))
    records.sort(key=lambda r: (r["timestamp"], r["file"]))

    payload = {
        "count": len(records),
        "generatedFrom": f"data/source/{tag}/migrations",
        "migrations": records,
        "prerelease": is_prerelease(tag),
        "tag": tag,
    }
    write_json(OUT_DIR / f"{tag}.json", payload)
    return payload


def main() -> int:
    tags = available_tags()
    if not tags:
        print("no snapshots under data/source/", file=sys.stderr)
        return 1

    per_tag = {}
    for tag in tags:
        payload = process_tag(tag)
        per_tag[tag] = payload["migrations"]

    counts = {}
    index_tags = {}
    previous = None
    for tag in tags:
        records = per_tag[tag]
        names = {r["file"] for r in records}
        prior = {r["file"] for r in per_tag[previous]} if previous else set()
        new = sorted(names - prior) if previous else sorted(names)
        dropped = sorted(prior - names) if previous else []

        counts[tag] = {
            "migrations": len(records),
            "new": len(new),
            "packagesAdded": len({p for r in records for p in r["packagesAdded"]}),
            "packagesRemoved": len({p for r in records for p in r["packagesRemoved"]}),
            "removed": len(dropped),
        }
        index_tags[tag] = {
            "count": len(records),
            "new": new,
            "previousTag": previous,
            "removed": dropped,
        }
        print(
            f"  migrate  {tag:<12} {len(records):>4} migrations, "
            f"{len(new):>3} new vs {previous or '(baseline)'}"
        )
        previous = tag

    write_json(
        OUT_DIR / "index.json",
        {"counts": counts, "tags": tags, "byTag": index_tags},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
