#!/usr/bin/env python3
"""Extract the Omarchy CLI surface from bin/ for every source snapshot.

Mirrors the metadata scanner and group/route derivation in bin/omarchy
(register_command / GROUP_DESCRIPTIONS), so the output matches what
`omarchy commands --json` would report for that snapshot.

Writes data/commands/<tag>.json and data/commands/index.json.
"""

from __future__ import annotations

import os
import re
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

OUT_DIR = DATA_DIR / "commands"

# bin/omarchy: METADATA_SCAN_LIMIT=80
SCAN_LIMIT = 80

# ^[[:space:]]*#[[:space:]]*omarchy:([[:alnum:]_-]+)=(.*)$
META_RE = re.compile(r"^[ \t]*#[ \t]*omarchy:([A-Za-z0-9_-]+)=(.*)$")
# ^[[:space:]]*#[[:space:]]*(.+)$
COMMENT_RE = re.compile(r"^[ \t]*#[ \t]*(.+)$")
BLANK_RE = re.compile(r"^[ \t]*$")
IS_COMMENT_RE = re.compile(r"^[ \t]*#")

GROUP_DESC_RE = re.compile(r'^GROUP_DESCRIPTIONS\[([^\]]+)\]="(.*)"[ \t]*$', re.M)

ROUTER_SUMMARY = "Omarchy command center"


def group_descriptions(tag: str) -> dict[str, str]:
    """GROUP_DESCRIPTIONS[...] table as declared in that snapshot's bin/omarchy."""
    router = tag_dir(tag) / "bin" / "omarchy"
    if not router.is_file():
        return {}
    return {m.group(1): m.group(2) for m in GROUP_DESC_RE.finditer(read_text(router))}


def split_pipe(value: str) -> list[str]:
    """Split on '|' and trim, dropping empties - same as the router's jq filter."""
    return [part.strip() for part in value.split("|") if part.strip()]


def scan_metadata(text: str) -> tuple[dict[str, str], bool, str]:
    """Replicate bin/omarchy's register_command header scan.

    Returns (metadata, name_seen, fallback_summary).
    """
    meta: dict[str, str] = {}
    name_seen = False
    fallback_summary = ""

    for line_count, line in enumerate(text.splitlines()[:SCAN_LIMIT], start=1):
        line = line.rstrip("\r")
        if line_count == 1 and line.startswith("#!"):
            continue
        if BLANK_RE.match(line):
            continue
        if not IS_COMMENT_RE.match(line):
            break

        m = META_RE.match(line)
        if m:
            key, value = m.group(1), m.group(2)
            value = value.rstrip("\r").replace("\t", " ")
            if key == "name":
                name_seen = True
            if key in {
                "group",
                "name",
                "summary",
                "args",
                "examples",
                "alias",
                "aliases",
                "requires-sudo",
                "hidden",
            }:
                if key == "alias":
                    key = "aliases"
                meta[key] = value
            continue

        if not fallback_summary:
            c = COMMENT_RE.match(line)
            if c:
                candidate = c.group(1).rstrip("\r").replace("\t", " ")
                if candidate and not candidate.startswith("omarchy:"):
                    fallback_summary = candidate

    return meta, name_seen, fallback_summary


def build_command(tag: str, path, descriptions: dict[str, str]) -> dict:
    binary = path.name
    text = read_text(path)
    meta, name_seen, fallback_summary = scan_metadata(text)

    is_router = binary == "omarchy"
    stem = binary[len("omarchy-"):] if binary.startswith("omarchy-") else binary

    if "-" in stem:
        fallback_group = stem.split("-", 1)[0]
        fallback_name = stem.split("-", 1)[1].replace("-", " ")
    else:
        fallback_group = stem
        fallback_name = ""

    group = meta.get("group") or fallback_group
    name = meta.get("name", "") if name_seen else fallback_name

    summary = meta.get("summary", "")
    if not summary and fallback_summary:
        summary = fallback_summary
    if not summary:
        summary = f"Run the {stem.replace('-', ' ')} command"

    route = "omarchy " + group
    if name:
        route += " " + name

    if is_router:
        # The router is not registered as a command by load_commands(); it is the
        # entry point. Use its own help banner verbatim when present.
        route = "omarchy"
        group = "omarchy"
        if ROUTER_SUMMARY in text:
            summary = ROUTER_SUMMARY

    aliases = [a for a in split_pipe(meta.get("aliases", "")) if a != route]
    relpath = f"bin/{binary}"

    group_desc = descriptions.get(group, "")
    if is_router and not group_desc:
        group_desc = ROUTER_SUMMARY

    return {
        "aliases": aliases,
        "args": meta.get("args", ""),
        "cli": route,
        "examples": split_pipe(meta.get("examples", "")),
        "executable": os.access(path, os.X_OK),
        "group": group,
        "groupDescription": group_desc,
        "hasMetadata": bool(meta),
        "hidden": meta.get("hidden", "") == "true",
        "lineCount": len(text.splitlines()),
        "name": binary,
        "path": relpath,
        "requiresSudo": meta.get("requires-sudo", "") == "true",
        "sourceUrl": source_url(tag, relpath),
        "summary": summary,
    }


def process_tag(tag: str) -> dict:
    bindir = tag_dir(tag) / "bin"
    descriptions = group_descriptions(tag)

    files = []
    if bindir.is_dir():
        for p in sorted(bindir.iterdir()):
            if not p.is_file():
                continue
            if p.name == "omarchy" or p.name.startswith("omarchy-"):
                files.append(p)

    commands = [build_command(tag, p, descriptions) for p in files]
    commands.sort(key=lambda c: c["name"])

    payload = {
        "commands": commands,
        "count": len(commands),
        "generatedFrom": f"data/source/{tag}/bin",
        "groups": dict(sorted(descriptions.items())),
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

    counts = {}
    groups: dict[str, str] = {}

    for tag in tags:
        payload = process_tag(tag)
        cmds = payload["commands"]
        groups.update(payload["groups"])
        counts[tag] = {
            "commands": len(cmds),
            "groups": len({c["group"] for c in cmds}),
            "hidden": sum(1 for c in cmds if c["hidden"]),
            "nonExecutable": sum(1 for c in cmds if not c["executable"]),
            "requiresSudo": sum(1 for c in cmds if c["requiresSudo"]),
            "withMetadata": sum(1 for c in cmds if c["hasMetadata"]),
        }
        print(
            f"  commands {tag:<12} {counts[tag]['commands']:>4} files, "
            f"{counts[tag]['withMetadata']:>4} with metadata, "
            f"{counts[tag]['hidden']:>3} hidden"
        )

    write_json(
        OUT_DIR / "index.json",
        {
            "counts": counts,
            "groups": dict(sorted(groups.items())),
            "prerelease": sorted(t for t in tags if is_prerelease(t)),
            "tags": tags,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
