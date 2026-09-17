#!/usr/bin/env python3
"""Verify the Omarchy domain landscape -> data/domains.json.

The seed list below is hand-researched (classification + note). Every domain and subdomain
is then RE-VERIFIED live with:
  * dig NS            -> nameservers, delegation
  * dig A/AAAA/CNAME  -> does it resolve at all
  * curl -sI -L       -> final URL, HTTP status, redirect chain
  * whois             -> creation date and EPP status, where the TLD exposes them

Social/org handles are recorded as seed data only (verification = "seed-only").

The hand classification always wins: when the live check contradicts the seed we keep the
seed's classification and attach a "discrepancy" string describing what we actually saw.
"""

from __future__ import annotations

import concurrent.futures as futures
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
OUT = os.path.join(DATA, "domains.json")

UA = "Mozilla/5.0 (compatible; omarchylinux.org-live-data/1.0; +https://omarchylinux.org)"
HTTP_TIMEOUT = 20
DIG_TIMEOUT = 12
WHOIS_TIMEOUT = 25
WHOIS_SLEEP = 0.4
RDAP_SLEEP = 2.5  # rdap.org rate-limits hard; stay well under it
RDAP_TIMEOUT = 20
HTTP_WORKERS = 8

FOUNDATION = "Omacom Foundation / 37signals"
CLOUDFLARE_OFFICIAL_NS = {"eva.ns.cloudflare.com", "mario.ns.cloudflare.com"}

# --------------------------------------------------------------------------- seed data
# (host, kind, classification, owner, note)
SEED: list[tuple[str, str, str, str, str]] = [
    # ---------------- official domains -------------------------------------------------
    ("omarchy.org", "domain", "official", FOUNDATION, "Primary official site"),
    ("omarchy.us", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.de", "domain", "official", FOUNDATION, "Country domain; bunny.net nameservers rather than Cloudflare"),
    ("omarchy.fr", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.jp", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.in", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.kr", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.mx", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.se", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.tr", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.is", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.dk", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.fi", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.gr", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.hu", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.ae", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.pt", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.no", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.nz", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.sg", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.ph", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.eu", "domain", "official", FOUNDATION, "Regional domain"),
    ("omarchy.it", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.co.uk", "domain", "official", FOUNDATION, "Country domain"),
    ("omarchy.cn", "domain", "official", FOUNDATION, "Redirects (301) to zh.omarchy.org, the Chinese-language site"),
    ("omarchy.com.au", "domain", "official", FOUNDATION, "Redirects (302) to omarchy.org"),
    ("omakub.org", "domain", "official", FOUNDATION, "Omarchy's Ubuntu-based predecessor; redirects to omarchy.org/omakub"),
    ("omacom.io", "domain", "official", FOUNDATION, "Foundation domain; redirects to omarchy.org/foundation"),
    ("omachee.org", "domain", "official", FOUNDATION, "Common-misspelling joke page run by the project"),
    ("wecanfixeverything.com", "domain", "official", FOUNDATION, "Project slogan page"),
    ("omarchs.fyi", "domain", "official", FOUNDATION, "Official side domain"),
    ("oligarchy.fyi", "domain", "official", FOUNDATION, "Official joke/side domain"),
    ("omarchy.news", "domain", "official", FOUNDATION, "Redirects to omarchy.org/news"),
    ("omacon.org", "domain", "official", FOUNDATION, "Omarchy conference"),
    ("omerchy.org", "domain", "official", FOUNDATION, "Official merch store"),
    ("herdr.dev", "domain", "official", FOUNDATION, "Official project domain"),
    ("tryomarchy.com", "domain", "official", "community-registered, serves official try-omarchy",
     "Registered by a community member but serves the official try-omarchy experience"),
    ("omarchyplugins.com", "domain", "official", "community-registered, redirects to official plugins site",
     "Community-registered 2026-07-28; now 301 to plugins.omarchy.org"),

    # ---------------- official subdomains ----------------------------------------------
    ("plugins.omarchy.org", "subdomain", "official", FOUNDATION, "Official plugin directory"),
    ("themes.omarchy.org", "subdomain", "official", FOUNDATION, "Official theme directory; may not resolve yet"),
    ("iso.omarchy.org", "subdomain", "official", FOUNDATION, "ISO download host"),
    ("pkgs.omarchy.org", "subdomain", "official", FOUNDATION, "Pacman repository (stable/rc/edge)"),
    ("mirror.omarchy.org", "subdomain", "official", FOUNDATION, "Arch package mirror (edge)"),
    ("stable-mirror.omarchy.org", "subdomain", "official", FOUNDATION, "Pinned Arch mirror for the stable channel"),
    ("rc-mirror.omarchy.org", "subdomain", "official", FOUNDATION, "Pinned Arch mirror for the rc channel"),
    ("donate.omarchy.org", "subdomain", "official", FOUNDATION, "Foundation donations"),
    ("radio.omarchy.org", "subdomain", "official", FOUNDATION, "Omarchy radio"),
    ("crt.omarchy.org", "subdomain", "official", FOUNDATION, "Certificate/transparency host"),
    ("logs.omarchy.org", "subdomain", "official", FOUNDATION, "Public logs"),
    ("zh.omarchy.org", "subdomain", "official", FOUNDATION, "Chinese-language site"),

    # ---------------- community (unofficial, disclaimed) --------------------------------
    ("omarchylinux.org", "domain", "community", "this site", "This site; unofficial reference. Registered 2026-09-11"),
    ("omarchylinux.com", "domain", "community", "unknown (likely a fan)",
     "Registered 2025-09-09, Cloudflare maisie/ruben nameservers, 301 to omarchy.org"),
    ("omarchyarchive.com", "domain", "community", "community", "Community archive"),
    ("omarchy.deepakness.com", "subdomain", "community", "Deepak Ness", "Personal-site subdomain with Omarchy content"),
    ("omarchytheme.com", "domain", "community", "community", "Community theme site"),
    ("omarchythemes.com", "domain", "community", "community", "Community theme site"),
    ("omarchy.gallery", "domain", "community", "community", "Community screenshot gallery"),
    ("omarchypulse.com", "domain", "community", "community", "Community news/stats site"),
    ("omarchy-weekly.com", "domain", "community", "community", "Community newsletter"),
    ("sudomarchy.com", "domain", "community", "community", "Community site"),
    ("omarchycompare.com", "domain", "community", "community", "Community comparison site"),
    ("omarchyguild.com", "domain", "community", "community", "Community guild site"),
    ("omarchy-official.org", "domain", "community", "community",
     "Fan-made guide site with a confusingly official-sounding name; registered 2026-09-01. NOT official"),
    ("omarchyhardware.com", "domain", "community", "community", "Community hardware compatibility site"),
    ("omarchycentral.com", "domain", "community", "community", "Community portal"),
    ("omarchyapps.com", "domain", "community", "community", "Community app directory"),
    ("omarchystories.org", "domain", "community", "community", "Community stories site"),
    ("omarchynews.com", "domain", "community", "community", "Community news site"),
    ("omafied.com", "domain", "community", "community", "Community site"),
    ("omahub.dev", "domain", "community", "community", "Community hub"),
    ("awesome-omarchy.com", "domain", "community", "community", "Community awesome-list site"),
    ("omarchy.pro", "domain", "community", "community", "Chinese-language community forum; Cloudflare-gated"),
    ("omarchy.iamcheyan.com", "subdomain", "community", "iamcheyan", "Personal-site subdomain with Omarchy content"),
    ("0marchy.org", "domain", "community", "community", "Satire site (zero instead of the letter O)"),

    # ---------------- for sale / parked ---------------------------------------------------
    ("omarchy.io", "domain", "for-sale", "private owner",
     "Registered 2026-08-24; owner offers it free to the maintainers, otherwise $10,000"),
    ("omarchy.com", "domain", "for-sale", "unrelated third party",
     "Registered 2016, unrelated to the distro; parked lander"),
    ("omarchyos.com", "domain", "for-sale", "private owner", "Listed for sale"),
    ("getomarchy.com", "domain", "for-sale", "private owner", "Listed for sale via Dynadot"),
    ("omarchy.club", "domain", "for-sale", "private owner", "Listed for sale"),

    # ---------------- suspended / hostile -------------------------------------------------
    ("omarchy.net", "domain", "suspended", "unknown",
     "AI-generated lookalike site serving a random ZIP download; flagged in "
     "github.com/omacom/omarchy/discussions/6160. whois status clientHold since 2026-08-25"),

    # ---------------- unregistered at last check ------------------------------------------
    ("omarchylinux.net", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchylinux.io", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchylinux.dev", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchy-linux.com", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchy.dev", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchy.app", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchy.sh", "domain", "unregistered", "", "Unregistered at last check"),
    ("omarchy.ai", "domain", "unregistered", "", "Unregistered at last check"),

    # ---------------- social / orgs (recorded only, no network check) -----------------------
    ("github.com/omacom", "social", "official", FOUNDATION,
     "Official GitHub org, 54 repos. github.com/omacom-io does not exist; basecamp/omarchy redirects here"),
    ("x.com/dhh", "social", "official", "David Heinemeier Hansson", "Project creator; release announcements"),
    ("x.com/OmarchyLinux", "social", "community", "community",
     "Self-described unofficial handle, roughly 19k followers"),
    ("discord.gg/tXFUdasqhY", "social", "official", FOUNDATION, 'Official "Omacom" Discord server'),
    ("youtube.com/@omarchy", "social", "unknown", "unknown", "Not official; squatter/parody account"),
    ("mastodon.social/@omarchy", "social", "unknown", "unknown", "Not official; squatter/parody account"),
    ("reddit.com/r/omarchy", "social", "community", "community", "Community subreddit, not affiliated with the project"),
]

OFFICIAL_HOSTS = {h for h, kind, cls, _o, _n in SEED if cls == "official" and kind != "social"}

MULTI_LABEL_TLDS = {"co.uk", "com.au", "org.uk", "com.br", "co.jp", "co.nz", "com.mx"}

CREATED_PATTERNS = [
    r"^\s*(?:Creation Date|Created On|Created Date|Created|Registered on|Registered|"
    r"Registration Time|Domain Registration Date|Domain Record Activated|created|"
    r"Record created on|Registration Date|\[Created on\]|Creation date)\s*[:.]?\s*(.+)$",
]
STATUS_PATTERNS = [
    r"^\s*(?:Domain Status|Status|status|EPP Status|state)\s*[:.]?\s*(.+)$",
]


def log(msg: str) -> None:
    print(f"[domains] {msg}", file=sys.stderr, flush=True)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def run(cmd: list[str], timeout: int) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, ""
    except OSError as exc:
        return 127, str(exc)


def run_split(cmd: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        return 127, "", str(exc)


def registrable(host: str) -> str:
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    if ".".join(parts[-2:]) in MULTI_LABEL_TLDS:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


# --------------------------------------------------------------------------- DNS

def _ns_records(name: str) -> list[str]:
    """Real NS records only -- `dig +short NS` on a CNAME'd name returns the CNAME target."""
    _code, out = run(["dig", "+noall", "+answer", "+time=5", "+tries=2", "NS", name], DIG_TIMEOUT)
    found = set()
    for line in out.splitlines():
        fields = line.split()
        if len(fields) >= 5 and fields[3].upper() == "NS":
            found.add(fields[4].rstrip(".").lower())
    return sorted(found)


def dig_ns(host: str) -> tuple[list[str], str | None]:
    """Nameservers for `host`; falls back to the registrable parent zone."""
    ns = _ns_records(host)
    if ns:
        return ns, "self"
    parent = registrable(host)
    if parent != host:
        ns = _ns_records(parent)
        if ns:
            return ns, f"parent:{parent}"
    return [], None


def dig_cname(host: str) -> str | None:
    _code, out = run(["dig", "+short", "+time=5", "+tries=2", "CNAME", host], DIG_TIMEOUT)
    for line in out.splitlines():
        line = line.strip()
        if line and not line.startswith(";"):
            return line.rstrip(".")
    return None


def dig_resolves(host: str) -> tuple[bool, list[str]]:
    addrs: list[str] = []
    for rtype in ("A", "AAAA", "CNAME"):
        _code, out = run(["dig", "+short", "+time=5", "+tries=2", rtype, host], DIG_TIMEOUT)
        for line in out.splitlines():
            line = line.strip()
            if line and not line.startswith(";"):
                addrs.append(line.rstrip("."))
        if addrs:
            break
    return bool(addrs), addrs[:6]


# --------------------------------------------------------------------------- HTTP

HTTP_LINE = re.compile(r"^HTTP/[\d.]+\s+(\d{3})", re.I)
LOCATION_LINE = re.compile(r"^location:\s*(.+)$", re.I)
MARKER = "__FINAL__"


def curl_probe(url: str, method_head: bool = True) -> dict:
    cmd = ["curl", "-s", "-L", "--max-time", str(HTTP_TIMEOUT), "--connect-timeout", "10",
           "-A", UA, "-o", "/dev/null", "-D", "-",
           "-w", f"\\n{MARKER}%{{http_code}}\\t%{{url_effective}}\\t%{{num_redirects}}\\n"]
    if method_head:
        cmd.append("-I")
    cmd.append(url)
    code, out = run(cmd, HTTP_TIMEOUT + 15)

    statuses: list[int] = []
    chain: list[dict] = []
    current = url
    for line in out.splitlines():
        m = HTTP_LINE.match(line.strip())
        if m:
            statuses.append(int(m.group(1)))
            continue
        m = LOCATION_LINE.match(line.strip())
        if m:
            target = m.group(1).strip()
            chain.append({"from": current, "status": statuses[-1] if statuses else None, "to": target})
            current = target

    final_status = None
    final_url = None
    redirects = None
    for line in out.splitlines():
        if line.startswith(MARKER):
            parts = line[len(MARKER):].split("\t")
            if parts and parts[0].isdigit():
                final_status = int(parts[0])
            if len(parts) > 1 and parts[1]:
                final_url = parts[1]
            if len(parts) > 2 and parts[2].strip().isdigit():
                redirects = int(parts[2].strip())
            break

    return {
        "exitCode": code,
        "httpStatus": final_status if final_status else None,
        "finalUrl": final_url or None,
        "redirectChain": chain,
        "numRedirects": redirects,
        "statuses": statuses,
    }


def http_check(host: str) -> dict:
    url = f"https://{host}" if "://" not in host else host
    res = curl_probe(url, method_head=True)
    # Some hosts reject HEAD outright -- retry once with GET.
    if res["httpStatus"] in (None, 0, 403, 405, 501):
        res_get = curl_probe(url, method_head=False)
        if res_get["httpStatus"] not in (None, 0):
            res = res_get
    if res["httpStatus"] in (None, 0):
        res_http = curl_probe(f"http://{host}", method_head=False)
        if res_http["httpStatus"] not in (None, 0):
            res_http["note"] = "https failed, answered over http"
            res = res_http
    return res


# --------------------------------------------------------------------------- whois

def normalize_date(raw: str) -> str | None:
    raw = raw.strip().strip("[]").strip()
    raw = re.sub(r"\s*\(.*\)$", "", raw)
    candidates = [
        ("%Y-%m-%dT%H:%M:%S%z", None), ("%Y-%m-%dT%H:%M:%SZ", None),
        ("%Y-%m-%dT%H:%M:%S.%f%z", None), ("%Y-%m-%dT%H:%M:%S", None),
        ("%Y-%m-%d %H:%M:%S", None), ("%Y-%m-%d", None), ("%Y/%m/%d", None),
        ("%d-%b-%Y", None), ("%d.%m.%Y", None), ("%d/%m/%Y", None),
        ("%Y.%m.%d", None), ("%b %d %Y", None), ("%d %B %Y", None),
    ]
    cleaned = raw.replace("Z", "+0000") if raw.endswith("Z") else raw
    cleaned = re.sub(r"([+-]\d{2}):(\d{2})$", r"\1\2", cleaned)
    for fmt, _ in candidates:
        try:
            parsed = dt.datetime.strptime(cleaned, fmt)
            return parsed.date().isoformat()
        except ValueError:
            continue
    m = re.search(r"(\d{4})[-/.](\d{2})[-/.](\d{2})", raw)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return raw[:64] or None


def whois_lookup(host: str) -> dict:
    """Look up `host` in whois.

    The whois client chases the registrar referral, and that second hop often fails
    (unreachable registrar whois server) *after* the registry has already returned a
    complete record on stdout. So: always parse stdout first, and only report a
    transport problem when nothing usable came back.
    """
    code, out, err = run_split(["whois", host], WHOIS_TIMEOUT)
    time.sleep(WHOIS_SLEEP)

    combined = (out + "\n" + err).lower()
    transport_error = any(s in combined for s in (
        "getaddrinfo(", "connection refused", "network is unreachable",
        "no route to host", "temporary failure in name resolution",
        "no address associated with hostname",
    ))
    tld_unsupported = any(s in combined for s in (
        "no whois server", "not have a whois server", "no whois data",
        "this tld has no whois", "tld is not supported",
    ))
    rate_limited = any(s in combined for s in (
        "rate limit", "query rate", "exceeded the maximum", "too many requests",
        "quota exceeded", "try again later", "please try again",
    ))

    if code == 124:
        return {"whoisCreated": None, "whoisStatus": None, "whoisNote": "timeout"}

    low = out.lower()
    not_found = any(s in low for s in (
        "no match for", "not found", "no entries found", "no data found",
        "status: free", "status: available", "domain not found", "no object found",
        "nothing found", "is available for registration",
    ))

    created = None
    for line in out.splitlines():
        for pat in CREATED_PATTERNS:
            m = re.match(pat, line, re.I)
            if m and m.group(1).strip():
                value = m.group(1).strip()
                if value.lower() in ("", "n/a", "not available"):
                    continue
                created = normalize_date(value)
                break
        if created:
            break

    statuses: list[str] = []
    for line in out.splitlines():
        for pat in STATUS_PATTERNS:
            m = re.match(pat, line, re.I)
            if m:
                value = m.group(1).strip()
                value = re.sub(r"\s*https?://\S+$", "", value)
                if not value:
                    continue
                if value not in statuses:
                    statuses.append(value)

    registrar = None
    m = re.search(r"^\s*Registrar:\s*(.+)$", out, re.M | re.I)
    if m:
        registrar = m.group(1).strip()

    have_data = bool(created or statuses or not_found)

    if have_data:
        note = None
        if transport_error:
            note = "registry record read; registrar whois referral unreachable"
        elif not_found:
            note = "no matching record"
        return {
            "whoisCreated": created,
            "whoisStatus": statuses[:8] or None,
            "whoisRegistrar": registrar,
            "whoisRegistered": not not_found,
            "whoisNote": note,
        }

    # nothing parseable -- say why, so downstream never reads silence as "unregistered"
    if rate_limited:
        note = "whois rate-limited, no data this run"
    elif tld_unsupported:
        note = "whois unavailable for this TLD"
    elif transport_error:
        note = "whois server unreachable from this host"
    elif not out.strip():
        note = "empty response"
    else:
        note = "no creation date or status published by this registry"
    return {"whoisCreated": None, "whoisStatus": None, "whoisRegistrar": registrar,
            "whoisRegistered": None, "whoisNote": note}


def rdap_lookup(host: str) -> dict:
    """RDAP fallback for domains whois could not answer for.

    Used only to establish registration POSITIVELY: a 200 proves the domain exists and
    carries its registration date. A 404 is recorded as "not found" but never treated as
    proof the domain is free -- plenty of ccTLDs simply have no RDAP service.
    """
    url = f"https://rdap.org/domain/{host}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/rdap+json, application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=RDAP_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        time.sleep(RDAP_SLEEP)
        return {"rdapNote": f"rdap: HTTP {exc.code} (not proof of availability)"}
    except Exception as exc:  # noqa: BLE001
        time.sleep(RDAP_SLEEP)
        return {"rdapNote": f"rdap: {type(exc).__name__}"}
    time.sleep(RDAP_SLEEP)

    if not isinstance(body, dict) or body.get("errorCode"):
        return {"rdapNote": f"rdap: error {body.get('errorCode') if isinstance(body, dict) else '?'}"}

    events = {e.get("eventAction"): e.get("eventDate")
              for e in body.get("events") or [] if isinstance(e, dict)}
    created = events.get("registration")
    if created:
        created = normalize_date(str(created).replace("Z", "+0000"))
    statuses = [str(x) for x in (body.get("status") or [])]
    return {
        "rdapCreated": created,
        "rdapStatus": statuses or None,
        "rdapRegistered": True,
        "rdapNote": None,
    }


# --------------------------------------------------------------------------- verification

def final_host(final_url: str | None) -> str | None:
    if not final_url:
        return None
    m = re.match(r"^[a-z]+://([^/:]+)", final_url, re.I)
    return m.group(1).lower() if m else None


def lands_on_official(final_url: str | None) -> bool:
    host = final_host(final_url)
    if not host:
        return False
    if host.endswith(".omarchy.org") or host == "omarchy.org":
        return True
    return host in OFFICIAL_HOSTS or registrable(host) in OFFICIAL_HOSTS


def find_discrepancy(entry: dict) -> str | None:
    cls = entry["classification"]
    ns = set(entry.get("nameservers") or [])
    status = entry.get("httpStatus")
    resolves = entry.get("dnsResolves")
    notes: list[str] = []

    if cls == "unregistered":
        if (resolves or entry.get("whoisCreated")
                or entry.get("whoisRegistered") is True):
            notes.append(
                f"seed says unregistered but it now resolves={resolves}, "
                f"whoisCreated={entry.get('whoisCreated')}, httpStatus={status}"
            )
    elif cls == "official":
        official_ns = bool(ns & CLOUDFLARE_OFFICIAL_NS)
        bunny = any(n.endswith("bunny.net") for n in ns)
        if not official_ns and not bunny and not lands_on_official(entry.get("finalUrl")):
            notes.append(
                f"official per seed but nameservers={sorted(ns) or 'none'} and "
                f"finalUrl={entry.get('finalUrl')} does not land on an official host"
            )
        if not resolves:
            notes.append("does not resolve")
    elif cls == "suspended":
        if status and 200 <= status < 400:
            notes.append(f"seed says suspended but HTTP {status} at {entry.get('finalUrl')}")
        wstatus = " ".join(entry.get("whoisStatus") or [])
        if entry.get("whoisStatus") and "clienthold" not in wstatus.lower():
            notes.append(f"expected clientHold in whois status, saw {entry.get('whoisStatus')}")
    elif cls in ("community", "for-sale"):
        if resolves is False:
            notes.append("no longer resolves")
        if entry.get("whoisRegistered") is False and entry.get("whoisCreated") is None:
            notes.append("whois reports no record (possibly expired)")

    return "; ".join(notes) or None


def check_network(item: tuple[str, str, str, str, str]) -> dict:
    host, kind, cls, owner, note = item
    ns, ns_from = dig_ns(host)
    resolves, addrs = dig_resolves(host)
    cname = dig_cname(host)
    http = http_check(host) if resolves else {
        "httpStatus": None, "finalUrl": None, "redirectChain": [], "numRedirects": None,
    }
    entry = {
        "host": host,
        "kind": kind,
        "classification": cls,
        "owner": owner,
        "note": note,
        "nameservers": ns,
        "nameserversFrom": ns_from,
        "dnsResolves": resolves,
        "addresses": addrs,
        "cname": cname,
        "httpStatus": http.get("httpStatus"),
        "finalUrl": http.get("finalUrl"),
        "redirectChain": http.get("redirectChain") or [],
        "whoisCreated": None,
        "whoisStatus": None,
        "lastChecked": now_iso(),
        "verification": "checked",
    }
    if http.get("note"):
        entry["httpNote"] = http["note"]
    return entry


def main() -> int:
    os.makedirs(DATA, exist_ok=True)
    checked_at = now_iso()

    network_items = [s for s in SEED if s[1] != "social"]
    social_items = [s for s in SEED if s[1] == "social"]

    log(f"checking {len(network_items)} hosts (dns + http, {HTTP_WORKERS} workers)")
    entries: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=HTTP_WORKERS) as pool:
        for entry in pool.map(check_network, network_items):
            entries.append(entry)
            log(f"  {entry['host']:<30} dns={entry['dnsResolves']} "
                f"http={entry['httpStatus']} -> {entry['finalUrl']}")

    by_host = {e["host"]: e for e in entries}

    # whois sequentially -- registries rate-limit parallel queries.
    whois_targets = [e for e in entries if e["kind"] == "domain"]
    log(f"whois for {len(whois_targets)} registrable domains (sequential)")
    for entry in whois_targets:
        info = whois_lookup(entry["host"])
        entry.update({k: v for k, v in info.items() if v is not None or k in
                      ("whoisCreated", "whoisStatus")})
        log(f"  {entry['host']:<30} created={entry.get('whoisCreated')} "
            f"status={entry.get('whoisStatus')}")
    rdap_targets = [e for e in whois_targets
                    if e.get("whoisCreated") is None and e.get("whoisRegistered") is None]
    log(f"rdap fallback for {len(rdap_targets)} domains whois could not answer for")
    for entry in rdap_targets:
        info = rdap_lookup(entry["host"])
        entry.update(info)
        if info.get("rdapCreated") and not entry.get("whoisCreated"):
            entry["whoisCreated"] = info["rdapCreated"]
            entry["creationSource"] = "rdap"
        if info.get("rdapRegistered"):
            entry["whoisRegistered"] = True
        log(f"  {entry['host']:<30} rdapCreated={info.get('rdapCreated')} "
            f"note={info.get('rdapNote')}")

    for entry in entries:
        if entry["kind"] == "subdomain":
            entry["whoisNote"] = f"see parent domain {registrable(entry['host'])}"

    for entry in entries:
        disc = find_discrepancy(entry)
        if disc:
            entry["discrepancy"] = disc
            log(f"  DISCREPANCY {entry['host']}: {disc}")

    for host, kind, cls, owner, note in social_items:
        entries.append({
            "host": host, "kind": kind, "classification": cls, "owner": owner, "note": note,
            "nameservers": [], "dnsResolves": None, "httpStatus": None, "finalUrl": None,
            "redirectChain": [], "whoisCreated": None, "whoisStatus": None,
            "lastChecked": checked_at, "verification": "seed-only",
        })

    order = {"official": 0, "community": 1, "for-sale": 2, "suspended": 3,
             "unregistered": 4, "unknown": 5}
    kind_order = {"domain": 0, "subdomain": 1, "social": 2}
    entries.sort(key=lambda e: (order.get(e["classification"], 9),
                                kind_order.get(e["kind"], 9), e["host"]))

    summary = {
        "total": len(entries),
        "byClassification": {},
        "byKind": {},
        "resolving": sum(1 for e in entries if e.get("dnsResolves")),
        "notResolving": sum(1 for e in entries if e.get("dnsResolves") is False),
        "checked": sum(1 for e in entries if e["verification"] == "checked"),
        "seedOnly": sum(1 for e in entries if e["verification"] == "seed-only"),
        "discrepancies": sum(1 for e in entries if e.get("discrepancy")),
    }
    for e in entries:
        summary["byClassification"][e["classification"]] = \
            summary["byClassification"].get(e["classification"], 0) + 1
        summary["byKind"][e["kind"]] = summary["byKind"].get(e["kind"], 0) + 1

    payload = {
        "checkedAt": checked_at,
        "summary": summary,
        "methodology": (
            "Classification is hand-researched and authoritative; every domain and subdomain is "
            "re-verified live with dig NS, dig A/AAAA/CNAME, curl -sI -L and whois. Where the live "
            "check contradicts the seed the seed classification is kept and a 'discrepancy' field "
            "records what was observed. Nothing is marked official unless its nameservers are "
            "eva/mario.ns.cloudflare.com, it redirects to an official host, or the seed says so."
        ),
        "domains": entries,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    log(f"wrote {OUT}: {summary['total']} entries, {summary['discrepancies']} discrepancies")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        log(f"FATAL: {exc}")
        sys.exit(1)
