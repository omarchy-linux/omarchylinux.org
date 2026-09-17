#!/usr/bin/env python3
"""Build an index of every published Omarchy ISO -> data/isos.json.

For each tag on github.com/omacom/omarchy we HEAD-probe the ISO, its .sha256 sidecar and
its .sig on https://iso.omarchy.org, fetch the sidecar checksum when present, and pull the
SHA256 / download URL out of the matching GitHub release body.

Requests are sequential with a 0.3s pause and a 20s timeout -- iso.omarchy.org is a
volunteer-funded mirror, so we stay polite.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "isos.json")

UA = "omarchylinux.org-live-data/1.0 (+https://omarchylinux.org; unofficial reference site)"
TIMEOUT = 20
SLEEP = 0.3
BASE = "https://iso.omarchy.org"
REPO = "omacom/omarchy"
SIGNING_KEY_FINGERPRINT = "40DFB630FF42BCFFB047046CF0134EE680CAC571"

SHA_RE = re.compile(r"SHA256:\s*([0-9a-fA-F]{64})")
ISO_URL_RE = re.compile(r"https?://\S+?\.iso\b")


def log(msg: str) -> None:
    print(f"[isos] {msg}", file=sys.stderr, flush=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def gh_json(path: str, paginate: bool = True) -> list | dict | None:
    cmd = ["gh", "api", path]
    if paginate:
        cmd.append("--paginate")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        log(f"gh api {path} failed: {exc}")
        return None
    if proc.returncode != 0:
        log(f"gh api {path} exited {proc.returncode}: {proc.stderr.strip()[:200]}")
        return None
    out = proc.stdout.strip()
    if not out:
        return None
    # `gh --paginate` concatenates one JSON array per page; stitch them together.
    decoder = json.JSONDecoder()
    items: list = []
    idx = 0
    last: dict | list | None = None
    while idx < len(out):
        try:
            obj, end = decoder.raw_decode(out, idx)
        except json.JSONDecodeError as exc:
            log(f"gh api {path}: JSON decode error at {idx}: {exc}")
            break
        last = obj
        if isinstance(obj, list):
            items.extend(obj)
        idx = end
        while idx < len(out) and out[idx] in " \t\r\n":
            idx += 1
    return items if items else last


def probe(url: str, method: str = "HEAD") -> dict:
    """Return {status, sizeBytes, lastModified, body?} for one request."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    result: dict = {"status": None, "sizeBytes": None, "lastModified": None, "body": None}
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result["status"] = resp.status
            length = resp.headers.get("Content-Length")
            result["sizeBytes"] = int(length) if length and length.isdigit() else None
            result["lastModified"] = resp.headers.get("Last-Modified")
            if method == "GET":
                result["body"] = resp.read(8192).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        result["status"] = exc.code
        length = exc.headers.get("Content-Length") if exc.headers else None
        result["sizeBytes"] = int(length) if length and length.isdigit() else None
        result["lastModified"] = exc.headers.get("Last-Modified") if exc.headers else None
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        result["status"] = None
        result["error"] = str(exc)
    finally:
        time.sleep(SLEEP)
    return result


def version_key(version: str) -> tuple:
    """Sort key for a release version: 4.0.0 ranks above 4.0.0-beta3."""
    core, _, pre = version.partition("-")

    def num_parts(text: str) -> tuple:
        parts = []
        for chunk in re.split(r"[.+_]", text):
            if chunk.isdigit():
                parts.append((0, int(chunk), ""))
            else:
                m = re.match(r"^(\d+)(.*)$", chunk)
                parts.append((0, int(m.group(1)), m.group(2)) if m else (1, 0, chunk))
        return tuple(parts)

    # a missing pre-release suffix outranks any pre-release ("1" > "0")
    return (num_parts(core), 1 if not pre else 0, num_parts(pre) if pre else ())


def main() -> int:
    os.makedirs(DATA, exist_ok=True)

    tags_raw = gh_json(f"repos/{REPO}/tags") or []
    tags = [t["name"] for t in tags_raw if isinstance(t, dict) and t.get("name")]
    log(f"{len(tags)} tags from {REPO}")

    releases_raw = gh_json(f"repos/{REPO}/releases") or []
    releases = {
        r["tag_name"]: r
        for r in releases_raw
        if isinstance(r, dict) and r.get("tag_name")
    }
    log(f"{len(releases)} releases from {REPO}")

    isos = []
    for tag in sorted(tags, key=lambda t: version_key(t.lstrip("v")), reverse=True):
        version = tag.lstrip("v")
        iso_url = f"{BASE}/omarchy-{version}.iso"
        rel = releases.get(tag) or {}
        body = rel.get("body") or ""

        head = probe(iso_url, "HEAD")
        sha_sidecar = probe(iso_url + ".sha256", "HEAD")
        sha_value = None
        if sha_sidecar.get("status") == 200:
            got = probe(iso_url + ".sha256", "GET")
            text = (got.get("body") or "").strip()
            m = re.search(r"\b([0-9a-fA-F]{64})\b", text)
            sha_value = m.group(1).lower() if m else (text or None)
        sig = probe(iso_url + ".sig", "HEAD")

        m = SHA_RE.search(body)
        sha_from_release = m.group(1).lower() if m else None
        m = ISO_URL_RE.search(body)
        iso_url_from_release = m.group(0) if m else None

        entry = {
            "version": version,
            "tag": tag,
            "releaseDate": rel.get("published_at"),
            "isoUrl": iso_url,
            "isoUrlFromRelease": iso_url_from_release,
            "isoStatus": head.get("status"),
            "sizeBytes": head.get("sizeBytes"),
            "lastModified": head.get("lastModified"),
            "sha256FromSidecar": sha_value,
            "sha256FromRelease": sha_from_release,
            "sha256Match": (
                None if not (sha_value and sha_from_release)
                else sha_value.lower() == sha_from_release.lower()
            ),
            "sigStatus": sig.get("status"),
            "sha256SidecarStatus": sha_sidecar.get("status"),
            "releaseUrl": rel.get("html_url"),
        }
        isos.append(entry)
        log(f"{tag:<14} iso={entry['isoStatus']} sha={entry['sha256SidecarStatus']} "
            f"sig={entry['sigStatus']} size={entry['sizeBytes']}")

    payload = {
        "fetchedAt": now_iso(),
        "signingKeyFingerprint": SIGNING_KEY_FINGERPRINT,
        "tagCount": len(tags),
        "availableIsoCount": sum(1 for i in isos if i["isoStatus"] == 200),
        "isos": isos,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    log(f"wrote {OUT}: {payload['availableIsoCount']}/{len(isos)} ISOs currently downloadable")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        log(f"FATAL: {exc}")
        sys.exit(1)
