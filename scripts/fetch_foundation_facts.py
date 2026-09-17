#!/usr/bin/env python3
"""Collect the headline Omarchy / Omacom Foundation figures -> data/facts.json.

Sources:
  * official momentum figures  -> raw.githubusercontent.com/omacom/omarchy-site (momentum.json)
  * Discord community size     -> discord.com invite API (with_counts)
  * Wikipedia interest         -> Wikimedia pageviews REST API (last 60 days)
  * OMARCHY trademark record   -> static, transcribed from USPTO TSDR (see checkedAt)

Every source is optional: a failure writes nulls and an entry in `errors`, never a crash.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "facts.json")

UA = "omarchylinux.org-live-data/1.0 (+https://omarchylinux.org; unofficial reference site)"
TIMEOUT = 25

MOMENTUM_URL = "https://raw.githubusercontent.com/omacom/omarchy-site/master/src/data/momentum.json"
DISCORD_URL = "https://discord.com/api/v10/invites/tXFUdasqhY?with_counts=true"
WIKI_URL = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
            "en.wikipedia/all-access/user/Omarchy/daily/{start}/{end}")
WIKI_DAYS = 60

TRADEMARK = {
    "mark": "OMARCHY",
    "serial": "99322411",
    "registration": "8250209",
    "registered": "2026-05-12",
    "register": "Principal",
    "class": "009",
    "basis": "1(a) use",
    "firstUse": "2024-07-04",
    "owner": "37signals LLC, 137 N Oak Park Ave Suite 208, Oak Park, Illinois",
    "madridIR": "1879867",
    "tsdrUrl": "https://tsdr.uspto.gov/statusview/sn99322411",
    "assignmentToFoundationOnFile": False,
    "checkedAt": "2026-09-11",
}

ERRORS: list[str] = []


def log(msg: str) -> None:
    print(f"[facts] {msg}", file=sys.stderr, flush=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def get_json(url: str, label: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:  # noqa: BLE001 - any failure degrades to null
        msg = f"{label}: {type(exc).__name__}: {exc}"
        log(f"FAILED {msg}")
        ERRORS.append(msg)
        return None


def build_momentum() -> dict:
    raw = get_json(MOMENTUM_URL, "momentum.json")
    result = {
        "source": MOMENTUM_URL,
        "checked": None,
        "github": {"stars": None, "pullRequests": None, "contributors": None, "commitsYear": None},
        "isoDownloads": {
            "total": None, "countries": None, "yesterday": None, "lastWeek": None,
            "lastMonth": None, "yearOne": None, "periods": [], "countingSince": None,
            "countingThrough": None,
        },
        "funding": {"totalMillionsUsd": None, "steps": []},
    }
    if not isinstance(raw, dict):
        return result

    result["checked"] = raw.get("checked")

    gh = raw.get("github") or {}
    result["github"] = {
        "stars": gh.get("stars"),
        "pullRequests": gh.get("pullRequests"),
        "contributors": gh.get("contributors"),
        "commitsYear": gh.get("commitsYear"),
    }

    dl = raw.get("downloads") or {}
    periods = dl.get("periods") or []
    by_label = {str(p.get("label", "")).strip().lower(): p.get("count") for p in periods}
    counting = dl.get("counting") or {}
    result["isoDownloads"] = {
        "total": dl.get("total"),
        "countries": dl.get("countries"),
        "yesterday": by_label.get("yesterday"),
        "lastWeek": by_label.get("last week"),
        "lastMonth": by_label.get("last month"),
        # "year one" only appears in some revisions of momentum.json; fall back to the
        # cumulative total, which is the project's since-launch (first-year) figure.
        "yearOne": next((v for k, v in by_label.items() if "year" in k), None) or dl.get("total"),
        "periods": periods,
        "countingSince": counting.get("since"),
        "countingThrough": counting.get("through"),
        "post": dl.get("post"),
    }

    fnd = raw.get("foundation") or {}
    result["funding"] = {
        "totalMillionsUsd": fnd.get("total"),
        "steps": fnd.get("steps") or [],
    }
    return result


def build_discord() -> dict:
    raw = get_json(DISCORD_URL, "discord invite")
    result = {
        "inviteUrl": "https://discord.gg/tXFUdasqhY",
        "guildId": None, "guildName": None, "description": None,
        "approximateMemberCount": None, "approximatePresenceCount": None,
    }
    if not isinstance(raw, dict):
        return result
    guild = raw.get("guild") or {}
    result.update({
        "guildId": guild.get("id"),
        "guildName": guild.get("name"),
        "description": guild.get("description"),
        "approximateMemberCount": raw.get("approximate_member_count"),
        "approximatePresenceCount": raw.get("approximate_presence_count"),
    })
    return result


def build_wikipedia() -> dict:
    today = dt.date.today()
    start = today - dt.timedelta(days=WIKI_DAYS)
    url = WIKI_URL.format(start=start.strftime("%Y%m%d"), end=today.strftime("%Y%m%d"))
    raw = get_json(url, "wikipedia pageviews")
    result = {
        "article": "Omarchy",
        "project": "en.wikipedia",
        "source": url,
        "from": start.isoformat(),
        "to": today.isoformat(),
        "days": [], "totalViews": None, "dailyAverage": None, "peak": None,
    }
    if not isinstance(raw, dict):
        return result
    days = []
    for item in raw.get("items") or []:
        stamp = str(item.get("timestamp", ""))
        if len(stamp) >= 8:
            date = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
        else:
            date = None
        days.append({"date": date, "views": item.get("views")})
    result["days"] = days
    views = [d["views"] for d in days if isinstance(d["views"], int)]
    if views:
        result["totalViews"] = sum(views)
        result["dailyAverage"] = round(sum(views) / len(views), 1)
        peak = max(days, key=lambda d: d["views"] if isinstance(d["views"], int) else -1)
        result["peak"] = peak
    return result


def main() -> int:
    os.makedirs(DATA, exist_ok=True)
    payload = {
        "fetchedAt": now_iso(),
        "momentum": build_momentum(),
        "discord": build_discord(),
        "wikipedia": build_wikipedia(),
        "trademark": TRADEMARK,
        "errors": ERRORS,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    log(f"wrote {OUT} ({len(ERRORS)} source failures)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        log(f"FATAL: {exc}")
        # still try to leave a valid file behind
        sys.exit(0)
