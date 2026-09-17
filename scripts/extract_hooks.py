#!/usr/bin/env python3
"""Extract the user hook system from every source snapshot.

Collects config/omarchy/hooks/<event>.d directories (with their .sample
contents), where each event is fired from, and the hook sections of the
manual's dotfiles page.

Writes data/hooks/<tag>.json and data/hooks/index.json.
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

OUT_DIR = DATA_DIR / "hooks"
HOOKS_REL = "config/omarchy/hooks"

FIRE_RE = re.compile(r"\bomarchy-hook\s+([A-Za-z0-9_-]+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def sample_description(text: str) -> str:
    """First comment paragraph of a .sample file, as one line."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#!"):
            continue
        if not stripped:
            if lines:
                break
            continue
        if not stripped.startswith("#"):
            break
        lines.append(stripped.lstrip("#").strip())
    return " ".join(x for x in lines if x)


def find_fired_by(tag: str) -> dict[str, list[dict]]:
    """Map hook event -> the files that invoke `omarchy-hook <event>`."""
    root = tag_dir(tag)
    fired: dict[str, list[dict]] = {}
    for sub in ("bin", "default", "shell", "config", "install"):
        base = root / sub
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.name == "omarchy-hook":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if line.lstrip().startswith("#"):
                    continue
                for m in FIRE_RE.finditer(line):
                    event = m.group(1)
                    relpath = str(path.relative_to(root)).replace(os.sep, "/")
                    entry = {
                        "file": relpath,
                        "line": lineno,
                        "snippet": line.strip(),
                        "sourceUrl": f"{source_url(tag, relpath)}#L{lineno}",
                    }
                    fired.setdefault(event, []).append(entry)
    return fired


def manual_hook_docs(tag: str) -> list[dict]:
    """Sections of manual/*dotfiles*.md that talk about hooks."""
    manual = tag_dir(tag) / "manual"
    docs = []
    if not manual.is_dir():
        return docs

    for path in sorted(manual.glob("*.md")):
        if "dotfile" not in path.name.lower():
            continue
        text = read_text(path)
        relpath = f"manual/{path.name}"

        sections = []
        current = None
        for lineno, line in enumerate(text.splitlines(), start=1):
            m = HEADING_RE.match(line)
            if m:
                if current:
                    sections.append(current)
                current = {"heading": m.group(2).strip(), "level": len(m.group(1)),
                           "line": lineno, "lines": []}
                continue
            if current:
                current["lines"].append(line)
        if current:
            sections.append(current)

        for section in sections:
            body = "\n".join(section["lines"]).strip()
            if "hook" not in (section["heading"] + " " + body).lower():
                continue
            docs.append({
                "body": body,
                "file": relpath,
                "heading": section["heading"],
                "level": section["level"],
                "line": section["line"],
                "sourceUrl": f"{source_url(tag, relpath)}#L{section['line']}",
            })
    return docs


def process_tag(tag: str) -> dict:
    root = tag_dir(tag)
    hooks_dir = root / HOOKS_REL
    fired = find_fired_by(tag)

    events = []
    if hooks_dir.is_dir():
        for directory in sorted(hooks_dir.iterdir()):
            if not directory.is_dir() or not directory.name.endswith(".d"):
                continue
            event = directory.name[:-2]
            samples = []
            for sample in sorted(directory.iterdir()):
                if not sample.is_file():
                    continue
                relpath = f"{HOOKS_REL}/{directory.name}/{sample.name}"
                text = read_text(sample)
                samples.append({
                    "content": text,
                    "description": sample_description(text),
                    "isSample": sample.name.endswith(".sample"),
                    "lineCount": len(text.splitlines()),
                    "name": sample.name,
                    "path": relpath,
                    "sourceUrl": source_url(tag, relpath),
                })
            events.append({
                "directory": f"{HOOKS_REL}/{directory.name}",
                "event": event,
                "firedBy": fired.get(event, []),
                "samples": samples,
                "sourceUrl": source_url(tag, f"{HOOKS_REL}/{directory.name}"),
                "userPath": f"~/.config/omarchy/hooks/{directory.name}",
            })

    runner_rel = "bin/omarchy-hook"
    runner = root / runner_rel
    payload = {
        "count": len(events),
        "docs": manual_hook_docs(tag),
        "events": events,
        "generatedFrom": f"data/source/{tag}/{HOOKS_REL}",
        "prerelease": is_prerelease(tag),
        "runner": {
            "content": read_text(runner),
            "path": runner_rel,
            "sourceUrl": source_url(tag, runner_rel),
        } if runner.is_file() else None,
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
    for tag in tags:
        payload = process_tag(tag)
        counts[tag] = {
            "docSections": len(payload["docs"]),
            "events": len(payload["events"]),
            "samples": sum(len(e["samples"]) for e in payload["events"]),
        }
        print(
            f"  hooks    {tag:<12} {counts[tag]['events']:>4} events, "
            f"{counts[tag]['samples']:>3} samples, "
            f"{counts[tag]['docSections']:>2} doc sections"
        )

    write_json(OUT_DIR / "index.json", {"counts": counts, "tags": tags})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
