#!/usr/bin/env python3
"""Fetch Omarchy package-channel state (stable / rc / edge) -> data/channels.json.

Reads the pacman databases published at https://pkgs.omarchy.org/<channel>/<arch>/omarchy.db
plus the mirror /lastupdate and /lastsync stamps, diffs the channels against each other and
appends one compact line per run to data/channels-history.jsonl.

Python 3.12 stdlib only (plus `tar`/`zstd` from the system for zstd-compressed databases).
"""

from __future__ import annotations

import datetime as dt
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "channels.json")
HISTORY = os.path.join(DATA, "channels-history.jsonl")

UA = "omarchylinux.org-live-data/1.0 (+https://omarchylinux.org; unofficial reference site)"
TIMEOUT = 30

# channel key -> (url path channel, arch)
CHANNELS = {
    "stable": ("stable", "x86_64"),
    "rc": ("rc", "x86_64"),
    "edge": ("edge", "x86_64"),
    "edge-aarch64": ("edge", "aarch64"),
}

MIRRORS = [
    ("stable-mirror", "https://stable-mirror.omarchy.org"),
    ("rc-mirror", "https://rc-mirror.omarchy.org"),
    ("mirror", "https://mirror.omarchy.org"),
]
UPSTREAM = ("arch-geo-mirror", "https://geo.mirror.pkgbuild.com")

KERNEL_RE = re.compile(r"^linux")


def log(msg: str) -> None:
    print(f"[channels] {msg}", file=sys.stderr, flush=True)


def iso(ts) -> str | None:
    if ts is None:
        return None
    return dt.datetime.fromtimestamp(int(ts), dt.timezone.utc).isoformat().replace("+00:00", "Z")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def http_get(url: str, timeout: int = TIMEOUT) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as exc:
        log(f"GET {url} failed: {exc}")
        return None


# --------------------------------------------------------------------------- db parsing

def decompress_members(blob: bytes) -> dict[str, bytes]:
    """Return {member_path: content} for every regular file in the (compressed) tar `blob`."""
    magic = blob[:6]
    members: dict[str, bytes] = {}

    if magic[:4] == b"\x28\xb5\x2f\xfd":  # zstd -- not supported by tarfile on 3.12
        raw = _zstd_to_tar(blob)
        if raw is None:
            return _zstd_via_tar_extract(blob)
        fobj: io.BytesIO | None = io.BytesIO(raw)
        mode = "r:"
    else:
        fobj = io.BytesIO(blob)
        mode = "r:*"  # tarfile sniffs gzip / xz / bzip2 itself

    with tarfile.open(fileobj=fobj, mode=mode) as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue
            fh = tf.extractfile(member)
            if fh is not None:
                members[member.name] = fh.read()
    return members


def _zstd_to_tar(blob: bytes) -> bytes | None:
    """Decompress a zstd stream to a raw tar using the `zstd` CLI."""
    if shutil.which("zstd") is None:
        return None
    try:
        proc = subprocess.run(["zstd", "-dc"], input=blob, capture_output=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        log(f"zstd -dc failed: {exc}")
        return None
    if proc.returncode != 0:
        log(f"zstd -dc exited {proc.returncode}: {proc.stderr[:200]!r}")
        return None
    return proc.stdout


def _zstd_via_tar_extract(blob: bytes) -> dict[str, bytes]:
    """Last resort: `tar --zstd` into a temp dir and read the files back."""
    members: dict[str, bytes] = {}
    with tempfile.TemporaryDirectory() as tmp:
        archive = os.path.join(tmp, "db.tar.zst")
        dest = os.path.join(tmp, "x")
        os.makedirs(dest, exist_ok=True)
        with open(archive, "wb") as fh:
            fh.write(blob)
        try:
            subprocess.run(
                ["tar", "--zstd", "-xf", archive, "-C", dest],
                check=True, capture_output=True, timeout=180,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            log(f"tar --zstd extract failed: {exc}")
            return members
        for dirpath, _dirs, files in os.walk(dest):
            for name in files:
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, dest)
                try:
                    with open(full, "rb") as fh:
                        members[rel] = fh.read()
                except OSError:
                    pass
    return members


def parse_desc(text: str) -> dict[str, list[str]]:
    """Parse a pacman `desc` file into {SECTION: [values]}."""
    fields: dict[str, list[str]] = {}
    key: str | None = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            key = None
            continue
        if line.startswith("%") and line.endswith("%") and len(line) > 2:
            key = line[1:-1]
            fields[key] = []
            continue
        if key is not None:
            fields[key].append(line)
    return fields


def parse_db(blob: bytes) -> dict[str, dict]:
    packages: dict[str, dict] = {}
    for path, content in decompress_members(blob).items():
        if os.path.basename(path) != "desc":
            continue
        fields = parse_desc(content.decode("utf-8", "replace"))
        name = (fields.get("NAME") or [None])[0]
        if not name:
            # fall back to the "<pkg>-<ver>-<rel>/desc" directory name
            name = os.path.dirname(path).rsplit("-", 2)[0] or None
        if not name:
            continue
        builddate = (fields.get("BUILDDATE") or [None])[0]
        try:
            builddate = int(builddate) if builddate is not None else None
        except ValueError:
            builddate = None
        packages[name] = {
            "version": (fields.get("VERSION") or [None])[0],
            "desc": (fields.get("DESC") or [None])[0],
            "builddate": builddate,
        }
    return dict(sorted(packages.items()))


def fetch_channel(channel: str, arch: str) -> dict:
    url = f"https://pkgs.omarchy.org/{channel}/{arch}/omarchy.db"
    blob = http_get(url)
    if blob is None:
        return {"arch": arch, "url": url, "ok": False, "error": "fetch failed",
                "packageCount": 0, "packages": {}}
    try:
        packages = parse_db(blob)
    except Exception as exc:  # noqa: BLE001 - never let one channel kill the run
        log(f"parse {url} failed: {exc}")
        return {"arch": arch, "url": url, "ok": False, "error": f"parse failed: {exc}",
                "packageCount": 0, "packages": {}}
    log(f"{channel}/{arch}: {len(packages)} packages")
    return {"arch": arch, "url": url, "ok": True, "packageCount": len(packages), "packages": packages}


# --------------------------------------------------------------------------- mirrors

def fetch_stamp(base: str, name: str) -> int | None:
    body = http_get(f"{base}/{name}", timeout=20)
    if body is None:
        return None
    text = body.decode("utf-8", "replace").strip()
    try:
        return int(float(text.split()[0]))
    except (ValueError, IndexError):
        log(f"{base}/{name}: unparseable body {text[:60]!r}")
        return None


def mirror_entry(name: str, base: str, upstream_lastupdate: int | None) -> dict:
    lastupdate = fetch_stamp(base, "lastupdate")
    lastsync = fetch_stamp(base, "lastsync")
    lag = None
    if upstream_lastupdate is not None and lastupdate is not None:
        lag = round((upstream_lastupdate - lastupdate) / 3600.0, 2)
    return {
        "name": name,
        "url": base,
        "lastupdate": {"unix": lastupdate, "iso": iso(lastupdate)},
        "lastsync": {"unix": lastsync, "iso": iso(lastsync)},
        "lagHoursVsUpstream": lag,
    }


# --------------------------------------------------------------------------- diffs

def diff_channels(left_name: str, left: dict, right_name: str, right: dict) -> list[dict]:
    lp, rp = left.get("packages", {}), right.get("packages", {})
    rows = []
    for name in sorted(set(lp) | set(rp)):
        lv = (lp.get(name) or {}).get("version")
        rv = (rp.get(name) or {}).get("version")
        if lv != rv:
            rows.append({"name": name, left_name: lv, right_name: rv})
    return rows


def main() -> int:
    os.makedirs(DATA, exist_ok=True)

    upstream_lastupdate = fetch_stamp(UPSTREAM[1], "lastupdate")
    upstream_lastsync = fetch_stamp(UPSTREAM[1], "lastsync")
    upstream = {
        "name": UPSTREAM[0],
        "url": UPSTREAM[1],
        "lastupdate": {"unix": upstream_lastupdate, "iso": iso(upstream_lastupdate)},
        "lastsync": {"unix": upstream_lastsync, "iso": iso(upstream_lastsync)},
    }

    mirrors = [mirror_entry(n, u, upstream_lastupdate) for n, u in MIRRORS]

    channels = {key: fetch_channel(ch, arch) for key, (ch, arch) in CHANNELS.items()}

    diffs = {
        "stable-vs-edge": diff_channels("stable", channels["stable"], "edge", channels["edge"]),
        "rc-vs-edge": diff_channels("rc", channels["rc"], "edge", channels["edge"]),
        "stable-vs-rc": diff_channels("stable", channels["stable"], "rc", channels["rc"]),
    }

    kernels = {}
    omarchy_package = {}
    for key, chan in channels.items():
        pkgs = chan.get("packages", {})
        kernels[key] = {n: p["version"] for n, p in pkgs.items() if KERNEL_RE.match(n)}
        omarchy_package[key] = (pkgs.get("omarchy") or {}).get("version")

    payload = {
        "fetchedAt": now_iso(),
        "mirrors": mirrors,
        "upstream": upstream,
        "channels": channels,
        "diffs": diffs,
        "kernels": kernels,
        "omarchyPackage": omarchy_package,
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    log(f"wrote {OUT}")

    by_name = {m["name"]: m["lastupdate"]["unix"] for m in mirrors}
    history_line = {
        "ts": payload["fetchedAt"],
        "stable_lastupdate": by_name.get("stable-mirror"),
        "rc_lastupdate": by_name.get("rc-mirror"),
        "edge_lastupdate": by_name.get("mirror"),
        "upstream_lastupdate": upstream_lastupdate,
        "omarchy_versions": omarchy_package,
    }
    with open(HISTORY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(history_line, separators=(",", ":"), ensure_ascii=False) + "\n")
    log(f"appended to {HISTORY}")

    ok = sum(1 for c in channels.values() if c.get("ok"))
    log(f"done: {ok}/{len(channels)} channels parsed, "
        f"{len(diffs['stable-vs-edge'])} stable-vs-edge package diffs")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        log(f"FATAL: {exc}")
        sys.exit(1)
