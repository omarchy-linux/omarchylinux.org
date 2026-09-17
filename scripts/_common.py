"""Shared helpers for the omarchylinux.org data pipeline.

Python 3.12, stdlib only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

REPO = "omacom/omarchy"

# Processing order: released tags oldest -> newest, then the unreleased head.
TAGS = [
    "v3.8.4",
    "v4.0.0",
    "v4.0.1",
    "v4.0.2",
    "v4.0.3",
    "v4.0.4",
    "quattro-dev",
]

# Snapshots that are not a published release.
PRERELEASE_REFS = {"quattro-dev"}

# git ref used to build blob URLs for each snapshot directory name.
REF_FOR_TAG = {"quattro-dev": "quattro"}  # the repo default branch

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "data" / "source"
DATA_DIR = ROOT / "data"


def git_ref(tag: str) -> str:
    return REF_FOR_TAG.get(tag, tag)


def source_url(tag: str, relpath: str) -> str:
    return f"https://github.com/{REPO}/blob/{git_ref(tag)}/{relpath}"


def tag_dir(tag: str) -> Path:
    return SOURCE_DIR / tag


def available_tags() -> list[str]:
    """Tags that have a non-empty checkout under data/source/."""
    out = []
    for tag in TAGS:
        d = tag_dir(tag)
        if d.is_dir() and any(d.iterdir()):
            out.append(tag)
    return out


def is_prerelease(tag: str) -> bool:
    return tag in PRERELEASE_REFS


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json(path: Path, payload) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    path.write_text(text + "\n", encoding="utf-8")
    return path


def rel_to_tag(tag: str, path: Path) -> str:
    return os.path.relpath(path, tag_dir(tag)).replace(os.sep, "/")
