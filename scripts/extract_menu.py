#!/usr/bin/env python3
"""Extract the Omarchy menu tree from default/omarchy/omarchy-menu.jsonc.

The file is JSON with `//` comments and trailing commas; IDs are dotted keys
that imply the hierarchy (trigger.share.file sits under trigger.share).

Writes data/menu/<tag>.json.
"""

from __future__ import annotations

import json
import os
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

OUT_DIR = DATA_DIR / "menu"
MENU_REL = "default/omarchy/omarchy-menu.jsonc"

# Keys copied straight through from the source object.
PASSTHROUGH = ("action", "checked", "command", "icon", "iconFont", "label",
               "provider", "target", "title", "when")


def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments and trailing commas, respecting strings."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]

        if ch == '"':
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    j += 1
                    break
                j += 1
            out.append(text[i:j])
            i = j
            continue

        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j == -1 else j
            continue

        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue

        out.append(ch)
        i += 1

    stripped = "".join(out)

    # Drop trailing commas that precede a closing brace/bracket, again keeping
    # strings intact.
    result = []
    i = 0
    n = len(stripped)
    while i < n:
        ch = stripped[i]
        if ch == '"':
            j = i + 1
            while j < n:
                if stripped[j] == "\\":
                    j += 2
                    continue
                if stripped[j] == '"':
                    j += 1
                    break
                j += 1
            result.append(stripped[i:j])
            i = j
            continue
        if ch == ",":
            j = i + 1
            while j < n and stripped[j] in " \t\r\n":
                j += 1
            if j < n and stripped[j] in "}]":
                i += 1
                continue
        result.append(ch)
        i += 1

    return "".join(result)


def make_node(node_id: str, raw: dict | None) -> dict:
    raw = raw or {}
    aliases = raw.get("aliases") or []
    if isinstance(aliases, str):
        aliases = [aliases]

    node = {
        "aliases": list(aliases),
        "children": [],
        "depth": node_id.count("."),
        "declared": raw is not None and bool(raw),
        "id": node_id,
        "parent": node_id.rsplit(".", 1)[0] if "." in node_id else None,
    }
    for key in PASSTHROUGH:
        node[key] = raw.get(key)

    if node["action"]:
        node["kind"] = "action"
    elif node["target"]:
        node["kind"] = "link"
    else:
        node["kind"] = "submenu"
    return node


def build(entries: dict) -> tuple[list[dict], list[dict]]:
    nodes: dict[str, dict] = {}
    order: list[str] = []

    for node_id, raw in entries.items():
        nodes[node_id] = make_node(node_id, raw if isinstance(raw, dict) else {})
        order.append(node_id)

    # Create any implied parent that the file does not declare.
    for node_id in list(nodes):
        parts = node_id.split(".")
        for depth in range(1, len(parts)):
            ancestor = ".".join(parts[:depth])
            if ancestor not in nodes:
                nodes[ancestor] = make_node(ancestor, {})
                nodes[ancestor]["declared"] = False
                order.insert(0, ancestor)

    roots = []
    for node_id in order:
        node = nodes[node_id]
        parent = node["parent"]
        if parent and parent in nodes:
            nodes[parent]["children"].append(node)
        else:
            roots.append(node)

    flat = [
        {k: v for k, v in nodes[node_id].items() if k != "children"}
        for node_id in sorted(nodes)
    ]
    return roots, flat


def process_tag(tag: str) -> dict:
    path = tag_dir(tag) / MENU_REL
    tree: list[dict] = []
    flat: list[dict] = []
    note = None

    if path.is_file():
        entries = json.loads(strip_jsonc(read_text(path)))
        tree, flat = build(entries)
    else:
        note = (
            f"{MENU_REL} is not present in {tag}; the menu is defined inside "
            "bin/omarchy-menu instead"
        )

    payload = {
        "count": len(flat),
        "flat": flat,
        "generatedFrom": f"data/source/{tag}/{MENU_REL}",
        "note": note,
        "prerelease": is_prerelease(tag),
        "sourceUrl": source_url(tag, MENU_REL) if path.is_file() else None,
        "tag": tag,
        "tree": tree,
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
        flat = payload["flat"]
        counts[tag] = {
            "actions": sum(1 for n in flat if n["kind"] == "action"),
            "maxDepth": max((n["depth"] for n in flat), default=0),
            "nodes": len(flat),
            "roots": len(payload["tree"]),
            "submenus": sum(1 for n in flat if n["kind"] == "submenu"),
        }
        print(
            f"  menu     {tag:<12} {counts[tag]['nodes']:>4} nodes, "
            f"{counts[tag]['roots']:>2} roots, "
            f"{counts[tag]['actions']:>3} actions"
        )

    write_json(OUT_DIR / "index.json", {"counts": counts, "tags": tags})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
