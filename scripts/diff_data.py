#!/usr/bin/env python3
"""Diff the extracted data between snapshots.

Writes data/diffs/<from>-to-<to>.json for every consecutive pair plus the
long-range v3.8.4 -> v4.0.4 comparison, and data/diffs/index.json.

Run after the extract_* scripts.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import DATA_DIR, available_tags, write_json  # noqa: E402

OUT_DIR = DATA_DIR / "diffs"

COMMAND_FIELDS = ("aliases", "args", "cli", "examples", "group", "hidden",
                  "requiresSudo", "summary")

MOD_ORDER = ["SUPER", "CTRL", "CONTROL", "ALT", "SHIFT", "MOD", "WIN", "LOGO",
             "CAPS", "MOD1", "MOD2", "MOD3", "MOD4", "MOD5"]


def load(kind: str, tag: str) -> dict:
    path = DATA_DIR / kind / f"{tag}.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_chord(chord: str) -> str:
    """Order-insensitive, case-insensitive chord key for cross-version matching."""
    parts = [p.strip() for p in chord.split("+") if p.strip()]
    mods = [p.upper() for p in parts if p.upper() in MOD_ORDER]
    keys = [p for p in parts if p.upper() not in MOD_ORDER]
    mods.sort(key=MOD_ORDER.index)
    return " + ".join(mods + [k.upper() for k in keys])


def binding_key(record: dict) -> str:
    return canonical_chord(record["chord"]) + "\u0000" + (record.get("label") or "")


def diff_commands(old: dict, new: dict) -> dict:
    old_map = {c["name"]: c for c in old.get("commands", [])}
    new_map = {c["name"]: c for c in new.get("commands", [])}

    changed = []
    for name in sorted(set(old_map) & set(new_map)):
        fields = {}
        for field in COMMAND_FIELDS:
            before, after = old_map[name].get(field), new_map[name].get(field)
            if before != after:
                fields[field] = [before, after]
        if fields:
            changed.append({"fields": fields, "name": name})

    return {
        "added": sorted(set(new_map) - set(old_map)),
        "changed": changed,
        "counts": {
            "added": len(set(new_map) - set(old_map)),
            "changed": len(changed),
            "from": len(old_map),
            "removed": len(set(old_map) - set(new_map)),
            "to": len(new_map),
        },
        "removed": sorted(set(old_map) - set(new_map)),
    }


def diff_bindings(old: dict, new: dict) -> dict:
    # 3.x ships the same chord in both tiling.conf and the deprecated
    # tiling-v2.conf; records are sorted by file, and "tiling-v2.conf" sorts
    # before "tiling.conf", so the active definition wins the key.
    old_map, new_map = {}, {}
    for record in old.get("bindings", []):
        old_map.setdefault(binding_key(record), record)
    for record in new.get("bindings", []):
        new_map.setdefault(binding_key(record), record)

    def brief(record):
        return {"chord": record["chord"], "label": record.get("label")}

    added = [brief(new_map[k]) for k in sorted(set(new_map) - set(old_map))]
    removed = [brief(old_map[k]) for k in sorted(set(old_map) - set(new_map))]

    changed_action = []
    for key in sorted(set(old_map) & set(new_map)):
        before, after = old_map[key].get("action"), new_map[key].get("action")
        if before != after:
            changed_action.append({
                "action": [before, after],
                "chord": new_map[key]["chord"],
                "label": new_map[key].get("label"),
            })

    note = None
    old_format, new_format = old.get("format"), new.get("format")
    if old_format and new_format and old_format != new_format:
        note = (
            f"binding definitions moved from {old_format} to {new_format}; the "
            "`action` string is written differently in each, so changedAction "
            "reflects that rewrite rather than a behaviour change"
        )

    return {
        "added": added,
        "changedAction": changed_action,
        "counts": {
            "added": len(added),
            "changedAction": len(changed_action),
            "from": len(old_map),
            "fromRecords": len(old.get("bindings", [])),
            "removed": len(removed),
            "to": len(new_map),
            "toRecords": len(new.get("bindings", [])),
        },
        "note": note,
        "removed": removed,
    }


def diff_menu(old: dict, new: dict) -> dict:
    old_ids = {n["id"] for n in old.get("flat", [])}
    new_ids = {n["id"] for n in new.get("flat", [])}
    new_map = {n["id"]: n for n in new.get("flat", [])}
    old_map = {n["id"]: n for n in old.get("flat", [])}

    changed = []
    for node_id in sorted(old_ids & new_ids):
        fields = {}
        for field in ("action", "label", "provider", "when", "checked"):
            before, after = old_map[node_id].get(field), new_map[node_id].get(field)
            if before != after:
                fields[field] = [before, after]
        if fields:
            changed.append({"fields": fields, "id": node_id})

    return {
        "added": sorted(new_ids - old_ids),
        "changed": changed,
        "counts": {
            "added": len(new_ids - old_ids),
            "changed": len(changed),
            "from": len(old_ids),
            "removed": len(old_ids - new_ids),
            "to": len(new_ids),
        },
        "removed": sorted(old_ids - new_ids),
    }


def diff_migrations(old: dict, new: dict) -> dict:
    old_files = {m["file"] for m in old.get("migrations", [])}
    new_records = {m["file"]: m for m in new.get("migrations", [])}
    new_files = sorted(set(new_records) - old_files)
    return {
        "counts": {
            "from": len(old_files),
            "new": len(new_files),
            "removed": len(old_files - set(new_records)),
            "to": len(new_records),
        },
        "new": [
            {
                "date": new_records[f]["date"],
                "description": new_records[f]["description"],
                "file": f,
            }
            for f in new_files
        ],
        "removed": sorted(old_files - set(new_records)),
    }


def build_diff(from_tag: str, to_tag: str) -> dict:
    return {
        "bindings": diff_bindings(load("bindings", from_tag), load("bindings", to_tag)),
        "commands": diff_commands(load("commands", from_tag), load("commands", to_tag)),
        "from": from_tag,
        "menu": diff_menu(load("menu", from_tag), load("menu", to_tag)),
        "migrations": diff_migrations(load("migrations", from_tag), load("migrations", to_tag)),
        "to": to_tag,
    }


def main() -> int:
    tags = available_tags()
    if len(tags) < 2:
        print("need at least two snapshots to diff", file=sys.stderr)
        return 1

    pairs = list(zip(tags, tags[1:]))
    long_range = (tags[0], "v4.0.4")
    if long_range[1] in tags and long_range not in pairs:
        pairs.append(long_range)

    index = []
    for from_tag, to_tag in pairs:
        diff = build_diff(from_tag, to_tag)
        name = f"{from_tag}-to-{to_tag}"
        write_json(OUT_DIR / f"{name}.json", diff)
        index.append({
            "file": f"{name}.json",
            "from": from_tag,
            "name": name,
            "summary": {
                "bindings": diff["bindings"]["counts"],
                "commands": diff["commands"]["counts"],
                "menu": diff["menu"]["counts"],
                "migrations": diff["migrations"]["counts"],
            },
            "to": to_tag,
        })
        c = diff["commands"]["counts"]
        b = diff["bindings"]["counts"]
        print(
            f"  diff     {name:<26} cmds +{c['added']}/-{c['removed']}/~{c['changed']}  "
            f"binds +{b['added']}/-{b['removed']}/~{b['changedAction']}  "
            f"migrations +{diff['migrations']['counts']['new']}"
        )

    write_json(OUT_DIR / "index.json", {"diffs": index, "tags": tags})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
