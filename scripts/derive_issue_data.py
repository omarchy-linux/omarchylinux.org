#!/usr/bin/env python3
"""
Derive the issue-backed data files for omarchylinux.org from the raw GitHub
dumps produced by scripts/fetch_issues.py.

Inputs
    data/issues/raw.json              (gitignored)
    data/issues/raw_discussions.json  (gitignored)
    data/source/v4.0.4/               (upstream tree, for quirk-script links)
    legacy-site/js/hardware.js        (hand-written prototype ratings)

Outputs
    data/issues/components.json
    data/issues/models.json
    data/issues/clusters.json
    data/issues/still-broken.json
    data/issues/stats.json

Every derived record traces back to a fetched issue/discussion number; nothing
is invented.

Usage: python3 scripts/derive_issue_data.py [--verbose]
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISSUE_DIR = ROOT / "data" / "issues"
SOURCE_REF = "v4.0.4"
SOURCE_TREE = ROOT / "data" / "source" / SOURCE_REF
BLOB_BASE = f"https://github.com/omacom/omarchy/blob/{SOURCE_REF}/"
LEGACY_HW = ROOT / "legacy-site" / "js" / "hardware.js"

TOP_ISSUES_PER_COMPONENT = 25
RECENT_ISSUES_PER_COMPONENT = 15
TOP_ISSUES_PER_CLUSTER = 15
MAX_AUTO_CLUSTERS = 150
MAX_ISSUES_PER_MODEL = 150
MIN_AUTO_CLUSTER_ISSUES = 3


def log(msg: str) -> None:
    print(msg, flush=True)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def load_json(path: Path):
    if not path.exists():
        sys.exit(f"missing input {path} - run scripts/fetch_issues.py first")
    with path.open() as fh:
        return json.load(fh)


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def write_json(path: Path, payload) -> None:
    with path.open("w") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    log(f"  wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1024:.0f} KB)")


# ===========================================================================
# Component definitions
# ===========================================================================
# "pattern"       classifies issues/discussions (matched against title + body)
# "scriptPattern" matches upstream quirk-script filenames/contents
COMPONENT_DEFS = [
    {
        "key": "nvidia",
        "title": "NVIDIA GPUs",
        "pattern": r"nvidia|geforce|\brtx\s?\d{3,4}\b|\bgtx\s?\d{3,4}\b|nouveau|\bcuda\b|nvidia-open|nvidia-dkms|\bnvk\b",
        "scriptPattern": r"nvidia|nouveau|gsp",
    },
    {
        "key": "amd-gpu",
        "title": "AMD GPUs",
        "pattern": r"\bamdgpu\b|\bradeon\b|\brx\s?[5-9]\d{3}\b|\bvega\b|\brdna\s?\d?\b|amd\s+(gpu|graphics|igpu|apu)|strix\s+halo|\b(680m|780m|880m|890m)\b",
        "scriptPattern": r"amdgpu|radeon|\bamd\b",
    },
    {
        "key": "intel-gpu",
        "title": "Intel GPUs",
        "pattern": r"intel\s+(gpu|graphics|arc|igpu)|\bi915\b|intel\s+arc|iris\s+xe|\bxe\s+driver\b|xe\s+kernel|intel_gpu",
        "scriptPattern": r"\bintel\b|i915|\bxe\b|vulkan",
    },
    {
        "key": "hybrid-gpu",
        "title": "Hybrid / dual GPU",
        "pattern": r"hybrid\s+(gpu|graphics)|\boptimus\b|prime-?run|\bdgpu\b|\bigpu\b|muxless|\bmux\b|aq_drm_devices|dual\s+gpu|discrete\s+gpu",
        "scriptPattern": r"hybrid|dgpu|igpu|\bmux\b|optimus|aq_drm_devices",
    },
    {
        "key": "suspend-sleep",
        "title": "Suspend, sleep and resume",
        "pattern": r"\bsuspend\w*|\bsleep\b|s2idle|\bhibernat\w*|\bresume\b|\blid\b",
        "scriptPattern": r"suspend|sleep|s2idle|hibernate|resume|\blid\b|clamshell",
    },
    {
        "key": "multi-monitor",
        "title": "Displays and multi-monitor",
        "pattern": r"\bmonitor\w*|\bdisplay\w*|hidpi|scaling|fractional|external\s+display|\bdock\w*|thunderbolt",
        "scriptPattern": r"monitor|display|hidpi|scaling|fractional|backlight|oled",
    },
    {
        "key": "audio",
        "title": "Audio",
        "pattern": r"\baudio\b|\bsound\b|speaker\w*|microphone|pipewire|wireplumber|headphone\w*",
        "scriptPattern": r"audio|sound|speaker|\bmic\b|pipewire|wireplumber|\bsof\b|mixer",
    },
    {
        "key": "wifi",
        "title": "Wi-Fi",
        "pattern": r"\bwifi\b|wi-fi|\bwlan\b|iwlwifi|brcmfmac|mt7921|network\s+manager",
        "scriptPattern": r"wifi|wlan|iwlwifi|brcm|mt7921|wireless|regdom|network",
    },
    {
        "key": "bluetooth",
        "title": "Bluetooth",
        "pattern": r"bluetooth|\bbluez\b",
        "scriptPattern": r"bluetooth|bluez",
    },
    {
        "key": "boot-limine",
        "title": "Boot, Limine and LUKS",
        "pattern": r"limine|\bboot\b|\bgrub\b|\buefi\b|secure\s+boot|\bluks\b|emergency\s+mode|kernel\s+panic",
        "scriptPattern": r"limine|\bboot\b|grub|uefi|luks|plymouth|mkinitcpio",
    },
    {
        "key": "fingerprint",
        "title": "Fingerprint readers",
        "pattern": r"fingerprint|\bfprintd?\b|libfprint",
        "scriptPattern": r"fingerprint|fprint",
    },
    {
        "key": "touchpad-input",
        "title": "Touchpad, keyboard and input",
        "pattern": r"touchpad|trackpad|keyboard|libinput|gesture\w*",
        "scriptPattern": r"touchpad|trackpad|keyboard|libinput|synaptic|fkeys|qmk|touchscreen",
    },
    {
        "key": "webcam",
        "title": "Webcams",
        "pattern": r"webcam|\bipu[67]\b|\bv4l2\b|\buvcvideo\b",
        "scriptPattern": r"webcam|camera|ipu6|ipu7",
    },
    {
        "key": "battery-power",
        "title": "Battery and power management",
        "pattern": r"battery|\bpower\b|\btlp\b|charging",
        "scriptPattern": r"battery|power|\btlp\b|charg|lpmd|thermald|powerprofiles",
    },
    {
        "key": "t2-mac",
        "title": "Intel T2 Macs",
        "pattern": r"linux-t2|\bt2\s+(mac\w*|chip|security)|(macbook|imac|mac\s?mini|mac\s?pro)[^\n]{0,80}\bt2\b|\bt2\b[^\n]{0,80}(macbook|mac\b)",
        "scriptPattern": r"\bt2\b|apple|macbook|brcmfmac|spi-keyboard",
    },
    {
        "key": "apple-silicon-asahi",
        "title": "Apple Silicon and Asahi",
        "pattern": r"\basahi\b|apple\s+silicon|\bm[1-4]\s*(pro|max|ultra)?\s*(mac\w*|chip)|(macbook|mac\s?mini|imac)[^\n]{0,40}\bm[1-4]\b|aarch64\s+mac",
        "scriptPattern": r"asahi|apple silicon|aarch64",
    },
    {
        "key": "vm",
        "title": "Virtual machines",
        "pattern": r"vmware|virtualbox|\bqemu\b|\bkvm\b|proxmox|parallels|\butm\b|hyper-?v\b|virtual\s+machine",
        "scriptPattern": r"vmware|virtualbox|qemu|\bkvm\b|\bvirt\b|hypervisor",
    },
    {
        "key": "windows-vm",
        "title": "Omarchy Windows VM",
        "pattern": r"windows[\s-]vm|omarchy-windows-vm",
        "scriptPattern": r"windows-vm|windows vm",
    },
    {
        "key": "printer",
        "title": "Printers and scanning",
        "pattern": r"\bprinter\w*|\bprinting\b|\bcups\b|\bsane\b\s+scanner|\bscanner\b",
        "scriptPattern": r"printer|\bcups\b|print",
    },
    {
        "key": "thunderbolt-dock",
        "title": "Thunderbolt and docks",
        "pattern": r"thunderbolt|\bdock\w*|docking\s+station|usb-?c\s+hub|displaylink",
        "scriptPattern": r"thunderbolt|dock|displaylink|external-monitors",
    },
    {
        "key": "storage-nvme",
        "title": "Storage, NVMe and filesystems",
        "pattern": r"\bnvme\b|\bssd\b|\bsata\b|\bhdd\b|hard\s+drive|\bmdadm\b|\braid\b|\blvm\b|\bfstab\b",
        "scriptPattern": r"nvme|\bssd\b|disk|btrfs|storage",
    },
]

WINDOWS_VM_TITLE_RE = re.compile(r"windows[\s-]vm", re.I)

for _c in COMPONENT_DEFS:
    _c["re"] = re.compile(_c["pattern"], re.I)
    _c["script_re"] = re.compile(_c["scriptPattern"], re.I)


# ===========================================================================
# Error-line extraction / normalization
# ===========================================================================
FENCE_RE = re.compile(r"```[\w+.-]*\n(.*?)(?:```|\Z)", re.S)
BACKTICK_RE = re.compile(r"`([^`\n]{8,160})`")
DQUOTE_RE = re.compile(r"\"([^\"\n]{10,160})\"")
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
KERNEL_TS_RE = re.compile(r"^\[\s*\d+\.\d+\]\s*")
SYSTEMD_TS_RE = re.compile(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+")
ISO_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\S*\s*")
PATH_RE = re.compile(r"(?:/[\w.+@~%-]+){2,}/?")
HEX_RE = re.compile(r"0x[0-9a-fA-F]+")
HASH_RE = re.compile(r"\b[0-9a-f]{7,}\b")
NUM_RE = re.compile(r"\d+")

ERRORISH_RE = re.compile(
    r"error|\bfail|cannot|can't|couldn'?t|not found|no such|unable|missing|invalid|"
    r"denied|refused|timed?\s?out|panic|segfault|traceback|fatal|aborted|"
    r"unknown trust|conflicting files|command not found|exit code|exited with|"
    r"warning:|\bbroken\b|not supported|does not exist",
    re.I,
)

NOISE_SIG_RE = re.compile(
    r"^(<path>|<n>|error|error:|warning|warning:|failed|<hex>|none|n/?a)[\s:]*$", re.I
)

# Source-code lines quoted inside issue bodies are not error messages.
CODE_LINE_RE = re.compile(
    r"===|&&|\|\||=>|\);|[{}]|^\s*(var|const|let|function|import|export|return|if|for|while)\s|"
    r"console\.(log|warn|error)|^\s*[.#@]|^\s*<[a-z/]",
    re.I,
)


def looks_errorish(line: str) -> bool:
    return bool(ERRORISH_RE.search(line))


def clean_line(line: str) -> str:
    s = ANSI_RE.sub("", line).strip()
    s = s.lstrip("> ").strip()
    s = KERNEL_TS_RE.sub("", s)
    s = SYSTEMD_TS_RE.sub("", s)
    s = ISO_TS_RE.sub("", s)
    return s.strip().strip("`").strip()


def normalize_signature(line: str) -> str:
    s = clean_line(line).lower()
    s = HEX_RE.sub("<hex>", s)
    s = PATH_RE.sub("<path>", s)
    s = HASH_RE.sub("<hash>", s)
    s = NUM_RE.sub("<n>", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_error_lines(body: str) -> list[str]:
    """Lines inside ``` fences that look like errors, plus any line with 'error'."""
    out: list[str] = []
    if not body:
        return out
    for block in FENCE_RE.findall(body):
        for raw in block.split("\n"):
            line = clean_line(raw)
            if 10 <= len(line) <= 300 and looks_errorish(line):
                out.append(line)
    for raw in body.split("\n"):
        if "error" not in raw.lower():
            continue
        line = clean_line(raw)
        if 10 <= len(line) <= 300:
            out.append(line)
    # de-duplicate while preserving order
    seen = set()
    uniq = []
    for line in out:
        if line not in seen:
            seen.add(line)
            uniq.append(line)
    return uniq[:60]


def extract_quoted_errors(body: str) -> list[str]:
    """Backticked / double-quoted spans that read like error strings."""
    out = []
    if not body:
        return out
    for pattern in (BACKTICK_RE, DQUOTE_RE):
        for span in pattern.findall(body):
            line = clean_line(span)
            if 10 <= len(line) <= 200 and looks_errorish(line):
                out.append(line)
    return out[:30]


def usable_signature(sig: str) -> bool:
    if len(sig) < 14 or len(sig) > 180:
        return False
    if NOISE_SIG_RE.match(sig):
        return False
    if CODE_LINE_RE.search(sig):
        return False
    words = [w for w in re.findall(r"[a-z]{2,}", sig)]
    return len(words) >= 3


# ===========================================================================
# Hardware-model extraction
# ===========================================================================
def _mk(vendor, model, variant=None):
    return (vendor, model, variant)


MODEL_RULES: list[tuple[re.Pattern, callable]] = [
    # --- Framework
    (re.compile(r"\bframework\s*(?:laptop\s*)?(1[236])\b", re.I),
     lambda m: _mk("Framework", f"Framework Laptop {m.group(1)}")),
    (re.compile(r"\bframework\s*desktop\b", re.I),
     lambda m: _mk("Framework", "Framework Desktop")),
    # --- Dell
    (re.compile(r"\b(?:dell\s+)?xps\s*(13|14|15|16|17)\b(?:[^\n]{0,14}?\b(DX\d{5,6}|9\d{3})\b)?", re.I),
     lambda m: _mk("Dell", f"Dell XPS {m.group(1)}", m.group(2))),
    (re.compile(r"\bdell\s+(latitude|inspiron|precision|vostro|alienware|g15|g16)\s*([\w-]{0,8})?", re.I),
     lambda m: _mk("Dell", f"Dell {m.group(1).title()}", (m.group(2) or "").strip() or None)),
    (re.compile(r"\balienware\s+([\w-]{0,10})", re.I),
     lambda m: _mk("Dell", "Alienware", (m.group(1) or "").strip() or None)),
    # --- Lenovo
    (re.compile(r"\bthinkpad\s+([TXPLE]\d{1,3}[a-z]{0,3})\b(?!\s*(?:carbon|yoga|extreme|nano|tablet))"
                r"(?:\s*gen\s*(\d+))?", re.I),
     lambda m: _mk("Lenovo", f"ThinkPad {m.group(1).upper()}",
                   f"Gen {m.group(2)}" if m.group(2) else None)),
    (re.compile(r"\b(?:thinkpad\s+)?x1\s*carbon\b(?:\s*gen\s*(\d+))?", re.I),
     lambda m: _mk("Lenovo", "ThinkPad X1 Carbon",
                   f"Gen {m.group(1)}" if m.group(1) else None)),
    (re.compile(r"\bthinkpad\s+(x1\s+(?:yoga|extreme|nano|tablet))\b", re.I),
     lambda m: _mk("Lenovo", f"ThinkPad {m.group(1).title()}")),
    (re.compile(r"\blegion\s+go\b", re.I),
     lambda m: _mk("Lenovo", "Lenovo Legion Go")),
    (re.compile(r"\b(?:lenovo\s+)?legion\s*([\w-]{0,8})?", re.I),
     lambda m: _mk("Lenovo", "Lenovo Legion", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:lenovo\s+)?yoga\s*(slim\s*\d+x?|pro\s*\d+|book\s*\d*|\d{3}[a-z]?)?", re.I),
     lambda m: _mk("Lenovo", "Lenovo Yoga", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:lenovo\s+)?ideapad\s*([\w-]{0,12})?", re.I),
     lambda m: _mk("Lenovo", "Lenovo IdeaPad", (m.group(1) or "").strip() or None)),
    # --- Apple
    (re.compile(r"\bmacbook\s?(pro|air)?\s?(\d+,\d+)\b", re.I),
     lambda m: _mk("Apple", f"MacBook{(m.group(1) or '').title()}{m.group(2)}")),
    (re.compile(r"\bmacbook\s+(pro|air)\b(?:[^\n]{0,20}?\b((?:19|20)\d{2})\b)?", re.I),
     lambda m: _mk("Apple", f"MacBook {m.group(1).title()}", m.group(2))),
    (re.compile(r"\bmacbook\b(?!\s*(pro|air|\d))", re.I),
     lambda m: _mk("Apple", "MacBook")),
    (re.compile(r"\bimac\b(?:[^\n]{0,20}?\b((?:19|20)\d{2})\b)?", re.I),
     lambda m: _mk("Apple", "iMac", m.group(1))),
    (re.compile(r"\bmac\s?mini\b(?:[^\n]{0,20}?\b((?:19|20)\d{2})\b)?", re.I),
     lambda m: _mk("Apple", "Mac mini", m.group(1))),
    (re.compile(r"\bmac\s?pro\b", re.I),
     lambda m: _mk("Apple", "Mac Pro")),
    (re.compile(r"\bmac\s?studio\b", re.I),
     lambda m: _mk("Apple", "Mac Studio")),
    # --- ASUS
    (re.compile(r"\b(?:asus\s+)?rog\s+(zephyrus|strix|flow|ally)\s*([a-z]?\d{2,3}[\w-]{0,6})?", re.I),
     lambda m: _mk("ASUS", f"ASUS ROG {m.group(1).title()}", (m.group(2) or "").strip() or None)),
    (re.compile(r"\b(?:asus\s+)?zen\s?book\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("ASUS", "ASUS Zenbook", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:asus\s+)?vivo\s?book\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("ASUS", "ASUS Vivobook", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:asus\s+)?expert\s?book\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("ASUS", "ASUS ExpertBook", (m.group(1) or "").strip() or None)),
    (re.compile(r"\basus\s+tuf\s*([\w-]{0,8})?|\btuf\s+(gaming|[af]\d{2})\b", re.I),
     lambda m: _mk("ASUS", "ASUS TUF", ((m.group(1) or m.group(2) or "").strip() or None))),
    # --- Microsoft Surface
    (re.compile(r"\bsurface\s+(laptop|pro|book|go|studio)\s*(\d+)?", re.I),
     lambda m: _mk("Microsoft", f"Surface {m.group(1).title()}", m.group(2))),
    # --- HP
    (re.compile(r"\b(?:hp\s+)?(elitebook|spectre|envy|omen|pavilion|probook|victus|zbook)\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("HP", f"HP {m.group(1).title()}", (m.group(2) or "").strip() or None)),
    # --- Acer
    (re.compile(r"\bacer\s+(swift|aspire|nitro|predator|chromebook)\s*([\w-]{0,8})?", re.I),
     lambda m: _mk("Acer", f"Acer {m.group(1).title()}", (m.group(2) or "").strip() or None)),
    (re.compile(r"\b(aspire|nitro\s*\d|predator)\s*([\w-]{0,8})?", re.I),
     lambda m: _mk("Acer", f"Acer {m.group(1).split()[0].title()}", (m.group(2) or "").strip() or None)),
    # --- Others
    # "MSI" is also kernel-speak for Message Signaled Interrupts - exclude those.
    (re.compile(r"\bmsi\s+(?!detect|embedd|interrupt|vector|capab|remap|domain|messag|mask|"
                r"enabl|disabl|alloc|entr|support|mode|irq|pci|x\b)([\w-]{2,14})", re.I),
     lambda m: _mk("MSI", "MSI", m.group(1))),
    (re.compile(r"\bbeelink\s*(ser\s?\d+\w*|eq\s?\d+\w*|gtr\s?\d+\w*|me\s?mini)?", re.I),
     lambda m: _mk("Beelink", "Beelink", (m.group(1) or "").strip() or None)),
    (re.compile(r"\bminis\s?forum\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("Minisforum", "Minisforum", (m.group(1) or "").strip() or None)),
    (re.compile(r"\bgpd\s+(win|pocket|micro|duo)\s*([\w-]{0,6})?", re.I),
     lambda m: _mk("GPD", f"GPD {m.group(1).title()}", (m.group(2) or "").strip() or None)),
    (re.compile(r"\bsteam\s?deck\b", re.I),
     lambda m: _mk("Valve", "Steam Deck")),
    (re.compile(r"\braspberry\s?pi\s*(\d)?", re.I),
     lambda m: _mk("Raspberry Pi", "Raspberry Pi", m.group(1))),
    (re.compile(r"\bslimbook\b\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("Slimbook", "Slimbook", (m.group(1) or "").strip() or None)),
    (re.compile(r"\btuxedo\b\s*([\w-]{0,12})?", re.I),
     lambda m: _mk("Tuxedo", "Tuxedo", (m.group(1) or "").strip() or None)),
    (re.compile(r"\bsystem\s?76\b\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("System76", "System76", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:star\s*labs?|starlabs|starbook)\b\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("Star Labs", "Star Labs", (m.group(1) or "").strip() or None)),
    (re.compile(r"\brazer\s+blade\s*(\d+)?", re.I),
     lambda m: _mk("Razer", "Razer Blade", m.group(1))),
    (re.compile(r"\b(?:samsung\s+)?galaxy\s?book\s*(\d+\w*)?", re.I),
     lambda m: _mk("Samsung", "Samsung Galaxy Book", m.group(1))),
    (re.compile(r"\blg\s?gram\b\s*([\w-]{0,8})?", re.I),
     lambda m: _mk("LG", "LG Gram", (m.group(1) or "").strip() or None)),
    (re.compile(r"\b(?:huawei\s+)?matebook\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("Huawei", "Huawei MateBook", (m.group(1) or "").strip() or None)),
    (re.compile(r"\bchromebook\b\s*([\w-]{0,10})?", re.I),
     lambda m: _mk("Chromebook", "Chromebook", (m.group(1) or "").strip() or None)),
]

# inxi / fastfetch style DMI block: "System: Dell product: XPS 13 9310 v: N/A"
INXI_RE = re.compile(
    r"System:\s*([A-Za-z0-9_.&-]+(?:\s+[A-Za-z0-9_.&-]+)?)\s+product:\s*(.+?)\s+v:\s*(\S+)",
    re.I,
)

_VARIANT_JUNK = re.compile(
    r"^(?:the|and|for|with|is|on|in|to|a|an|of|or|my|this|that|it|but|not|has|was|"
    r"laptop|gen|pro|max|ultra|from|when|after|de|se|https?)$",
    re.I,
)


def clean_variant(variant: str | None) -> str | None:
    if not variant:
        return None
    v = variant.strip(" -_:,.;()[]")
    if not v or len(v) > 16:
        return None
    if _VARIANT_JUNK.match(v):
        return None
    if not re.search(r"[0-9]", v) and len(v) < 3:
        return None
    return v


def extract_models(text: str) -> dict[str, dict]:
    """Return {model_key: {vendor, model, variants:set, matches:set}} for a text blob."""
    found: dict[str, dict] = {}
    for rx, builder in MODEL_RULES:
        for m in rx.finditer(text):
            try:
                vendor, model, variant = builder(m)
            except Exception:
                continue
            if not model:
                continue
            key = slugify(model if model.lower().startswith(vendor.lower()) else f"{vendor} {model}")
            entry = found.setdefault(key, {
                "vendor": vendor, "model": model, "variants": set(), "matches": set()
            })
            variant = clean_variant(variant)
            if variant:
                entry["variants"].add(variant)
            snippet = m.group(0).strip()
            if snippet:
                entry["matches"].add(re.sub(r"\s+", " ", snippet)[:60])
    return found


def extract_dmi_hints(text: str) -> list[str]:
    hints = []
    for m in INXI_RE.finditer(text):
        vendor, product, ver = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if len(product) > 60:
            continue
        hint = f"{vendor} / product: {product}"
        if ver and ver.lower() not in ("n/a", "none", "not"):
            hint += f" / v: {ver}"
        hints.append(hint[:120])
    return hints[:5]


# ===========================================================================
# Upstream quirk scripts
# ===========================================================================
def load_quirk_scripts() -> list[dict]:
    scripts: list[dict] = []
    if not SOURCE_TREE.exists():
        log(f"WARNING: {SOURCE_TREE} not found - relatedQuirkScripts will be empty")
        return scripts

    candidates: list[Path] = []
    bin_dir = SOURCE_TREE / "bin"
    if bin_dir.is_dir():
        candidates += sorted(p for p in bin_dir.glob("omarchy-hw-*") if p.is_file())
    for sub in ("install/hardware", "install/user/hardware"):
        d = SOURCE_TREE / sub
        if d.is_dir():
            candidates += sorted(p for p in d.rglob("*.sh") if p.is_file())

    for path in candidates:
        if path.name == "all.sh":
            continue  # dispatcher that sources every other script; not a quirk itself
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        rel = path.relative_to(SOURCE_TREE).as_posix()
        summary = ""
        m = re.search(r"#\s*omarchy:summary=(.+)", text)
        if m:
            summary = m.group(1).strip()
        else:
            for line in text.split("\n")[1:8]:
                line = line.strip()
                if line.startswith("#") and len(line) > 4 and "!/" not in line:
                    summary = line.lstrip("# ").strip()
                    break
        scripts.append({
            "name": path.name,
            "path": rel,
            "sourceUrl": BLOB_BASE + rel,
            "summary": summary[:220],
            "_haystack": f"{rel}\n{text}".lower(),
        })
    return scripts


# ===========================================================================
# Legacy prototype (legacy-site/js/hardware.js)
# ===========================================================================
LEGACY_CALL_RE = re.compile(r"m\(\{(.*?)\}\);", re.S)
LEGACY_PAIR_RE = re.compile(r"(\w+)\s*:\s*\"((?:[^\"\\]|\\.)*)\"")
LEGACY_DEFAULTS = {
    "wifi": "works", "audio": "works", "webcam": "works", "fingerprint": "unknown",
    "gpu": "works", "suspend": "works", "type": "laptop", "tags": "",
}


def parse_legacy_prototype() -> list[dict]:
    if not LEGACY_HW.exists():
        log(f"WARNING: {LEGACY_HW} not found - no legacy prototype entries")
        return []
    text = LEGACY_HW.read_text()
    rows = []
    for body in LEGACY_CALL_RE.findall(text):
        row = dict(LEGACY_DEFAULTS)
        for key, value in LEGACY_PAIR_RE.findall(body):
            row[key] = value.replace('\\"', '"').replace("\\\\", "\\")
        if row.get("id"):
            rows.append(row)
    return rows


# ===========================================================================
# Cluster seeds
# ===========================================================================
SEED_CLUSTERS: list[tuple[str, str, list[str]]] = [
    ("xdg-terminal-exec", "xdg-terminal-exec", ["xdg-terminal-exec"]),
    ("elephant-not-found", "command not found: elephant",
     ["command not found: elephant", "elephant: command not found", "elephant"]),
    ("ask-for-approval", "ask-for-approval", ["ask-for-approval"]),
    ("snapshot-failed", "Creating a snapshot failed / snapper",
     ["Creating a snapshot failed", "snapper"]),
    ("no-packages-upgraded", "no packages were upgraded", ["no packages were upgraded"]),
    ("failed-retrieve-files", "failed to retrieve some files", ["failed to retrieve some files"]),
    ("failed-commit-transaction", "failed to commit transaction", ["failed to commit transaction"]),
    ("emergency-mode", "emergency mode", ["emergency mode"]),
    ("black-screen", "black screen", ["black screen"]),
    ("kernel-panic", "kernel panic", ["kernel panic"]),
    ("polkit", "polkit", ["polkit"]),
    ("keyring", "keyring", ["keyring"]),
    ("signature-unknown-trust", "signature is unknown trust",
     ["signature is unknown trust", "unknown trust", "signature from"]),
    ("conflicting-files", "conflicting files", ["conflicting files"]),
    ("waybar", "waybar", ["waybar"]),
    ("walker", "walker", ["walker"]),
    ("nil-value-global-o", "attempt to index a nil value (global 'o')",
     ["attempt to index a nil value (global 'o')", "attempt to index a nil value"]),
    ("bindings-conf", "bindings.conf", ["bindings.conf"]),
    ("monitors-lua", "monitors.lua", ["monitors.lua"]),
    ("screen-share", "screen share / screen sharing", ["screen share", "screen sharing", "screensharing"]),
    ("fingerprint", "fingerprint", ["fingerprint"]),
    ("bluetooth", "bluetooth", ["bluetooth"]),
    ("no-sound", "no sound", ["no sound"]),
    ("suspend", "suspend", ["suspend"]),
    ("hibernate", "hibernate", ["hibernate"]),
    ("fractional", "fractional", ["fractional"]),
    ("scaling", "scaling", ["scaling"]),
    ("1password", "1password", ["1password"]),
    ("chromium", "chromium", ["chromium"]),
    ("docker", "docker", ["docker"]),
    ("podman", "podman", ["podman"]),
    ("steam", "steam", ["steam"]),
    ("gamescope", "gamescope", ["gamescope"]),
    ("luks", "luks", ["luks"]),
    ("keyboard-layout", "keyboard layout", ["keyboard layout"]),
    ("azerty", "azerty", ["azerty"]),
    ("sddm", "sddm", ["sddm"]),
    ("login-loop", "login loop", ["login loop"]),
    ("lock-screen", "lock screen", ["lock screen"]),
    ("hyprlock", "hyprlock", ["hyprlock"]),
    ("battery", "battery", ["battery"]),
    ("tlp", "tlp", ["tlp"]),
    ("nvidia", "nvidia", ["nvidia"]),
    ("aq-drm-devices", "AQ_DRM_DEVICES", ["AQ_DRM_DEVICES"]),
    ("tty", "tty", ["tty"]),
    ("omarchy-update", "omarchy-update / omarchy update", ["omarchy-update", "omarchy update"]),
    ("migration", "migration", ["migration"]),
    ("pacnew", "pacnew", ["pacnew"]),
    ("mise", "mise", ["mise"]),
    ("codex", "codex", ["codex"]),
    ("claude", "claude", ["claude"]),
    ("tailscale", "tailscale", ["tailscale"]),
    ("wifi", "wifi", ["wifi"]),
    ("iwlwifi", "iwlwifi", ["iwlwifi"]),
    ("webcam", "webcam", ["webcam"]),
    ("ipu6", "ipu6", ["ipu6"]),
    ("ipu7", "ipu7", ["ipu7"]),
    ("audio", "audio", ["audio"]),
    ("cs35l56", "cs35l56", ["cs35l56"]),
    ("speaker", "speaker", ["speaker"]),
    ("cursor", "cursor", ["cursor"]),
    ("font", "font", ["font"]),
    ("printer", "printer", ["printer"]),
    ("cups", "cups", ["cups"]),
    ("clipboard", "clipboard", ["clipboard"]),
    ("notification", "notification", ["notification"]),
    ("screenshot", "screenshot", ["screenshot"]),
    ("voxtype", "voxtype", ["voxtype"]),
    ("dictation", "dictation", ["dictation"]),
    ("theme", "theme", ["theme"]),
    ("gtk4", "gtk4", ["gtk4"]),
    ("libadwaita", "libadwaita", ["libadwaita"]),
    ("plugin", "plugin", ["plugin"]),
    ("quickshell", "quickshell", ["quickshell"]),
]


def build_query_regex(queries: list[str]) -> re.Pattern:
    parts = []
    for q in queries:
        if re.fullmatch(r"[A-Za-z0-9]+", q):
            parts.append(r"\b" + re.escape(q) + r"\b")
        else:
            parts.append(re.escape(q))
    return re.compile("|".join(parts), re.I)


VERSION_RE = re.compile(r"\b([34])\.(\d{1,2})\.(\d{1,2})\b")


def version_counts(texts) -> dict[str, int]:
    counts: Counter = Counter()
    for text in texts:
        seen = set()
        for m in VERSION_RE.finditer(text):
            major, minor, patch = m.group(1), int(m.group(2)), int(m.group(3))
            if major == "3":
                token = "3.x"
            elif minor == 0 and patch <= 4:
                token = f"4.0.{patch}"
            else:
                token = f"4.{minor}.x"
            seen.add(token)
        counts.update(seen)
    return dict(counts.most_common())


# ===========================================================================
# Shared issue helpers
# ===========================================================================
def fixed_by_prs(issue: dict) -> list[int]:
    numbers: list[int] = []
    closer = issue.get("closedBy") or {}
    if closer.get("type") == "pull_request" and closer.get("number"):
        numbers.append(closer["number"])
    for ref in issue.get("referencedPRs") or []:
        if ref.get("merged") and ref.get("number") and ref["number"] not in numbers:
            numbers.append(ref["number"])
    return numbers[:5]


def issue_weight(issue: dict) -> int:
    return (issue.get("reactions") or 0) + (issue.get("comments") or 0)


def slim_issue(issue: dict, with_components: bool = False) -> dict:
    out = {
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["url"],
        "state": issue["state"],
        "comments": issue.get("comments", 0),
        "reactions": issue.get("reactions", 0),
        "createdAt": issue.get("createdAt"),
        "closedAt": issue.get("closedAt"),
    }
    prs = fixed_by_prs(issue)
    if prs:
        out["fixedBy"] = prs
    if with_components:
        out["components"] = issue.get("_components", [])
    return out


# ===========================================================================
# Main
# ===========================================================================
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    raw = load_json(ISSUE_DIR / "raw.json")
    raw_disc = load_json(ISSUE_DIR / "raw_discussions.json")
    issues: list[dict] = raw["issues"]
    discussions: list[dict] = raw_disc["discussions"]
    fetched_at = raw.get("fetchedAt")
    log(f"loaded {len(issues)} issues, {len(discussions)} discussions (fetchedAt={fetched_at})")

    quirk_scripts = load_quirk_scripts()
    log(f"loaded {len(quirk_scripts)} upstream quirk scripts from {SOURCE_REF}")

    # ---------------------------------------------------------------- index
    sig_to_issues: dict[str, set[int]] = defaultdict(set)
    sig_to_discussions: dict[str, set[int]] = defaultdict(set)
    sig_example: dict[str, str] = {}
    issue_by_number: dict[int, dict] = {}

    for issue in issues:
        issue_by_number[issue["number"]] = issue
        title = issue.get("title") or ""
        body = issue.get("body") or ""
        blob = f"{title}\n{body}"
        issue["_text"] = blob
        # Clusters search the whole thread (opening post + fetched comment text);
        # components classify on the opening post only.
        issue["_search"] = blob + "\n" + (issue.get("commentsText") or "")

        # components
        comps = []
        is_windows_vm = bool(WINDOWS_VM_TITLE_RE.search(title))
        for cdef in COMPONENT_DEFS:
            if cdef["key"] == "vm" and is_windows_vm:
                continue
            if cdef["key"] == "windows-vm":
                if is_windows_vm or cdef["re"].search(blob):
                    comps.append(cdef["key"])
                continue
            if cdef["re"].search(blob):
                comps.append(cdef["key"])
        issue["_components"] = comps

        # error lines + signatures
        err_lines = extract_error_lines(body)
        issue["_errorLines"] = err_lines
        issue["_errorLinesAll"] = err_lines + [
            l for l in extract_error_lines(issue.get("commentsText") or "")
            if l not in err_lines
        ]
        sigs = set()
        for line in err_lines + extract_quoted_errors(body):
            sig = normalize_signature(line)
            if usable_signature(sig):
                sigs.add(sig)
                sig_example.setdefault(sig, line)
        issue["_sigs"] = sigs
        for sig in sigs:
            sig_to_issues[sig].add(issue["number"])

    for disc in discussions:
        blob = f"{disc.get('title') or ''}\n{disc.get('body') or ''}"
        disc["_text"] = blob
        disc["_search"] = blob + "\n" + "\n".join(
            [(disc.get("answer") or {}).get("body") or ""]
            + [(c.get("body") or "") for c in (disc.get("topComments") or [])]
        )
        comps = []
        is_windows_vm = bool(WINDOWS_VM_TITLE_RE.search(disc.get("title") or ""))
        for cdef in COMPONENT_DEFS:
            if cdef["key"] == "vm" and is_windows_vm:
                continue
            if cdef["key"] == "windows-vm":
                if is_windows_vm or cdef["re"].search(blob):
                    comps.append(cdef["key"])
                continue
            if cdef["re"].search(blob):
                comps.append(cdef["key"])
        disc["_components"] = comps
        for line in extract_error_lines(disc.get("body") or ""):
            sig = normalize_signature(line)
            if usable_signature(sig):
                sig_to_discussions[sig].add(disc["number"])
                sig_example.setdefault(sig, line)

    # ============================================================ components
    log("deriving components.json ...")
    components_out = []
    for cdef in COMPONENT_DEFS:
        key = cdef["key"]
        matched = [i for i in issues if key in i["_components"]]
        matched_disc = [d for d in discussions if key in d["_components"]]
        open_n = sum(1 for i in matched if i["state"] == "OPEN")

        top = sorted(matched, key=lambda i: (-issue_weight(i), i["number"]))[:TOP_ISSUES_PER_COMPONENT]
        recent = sorted(matched, key=lambda i: (i.get("createdAt") or "", i["number"]), reverse=True)[
            :RECENT_ISSUES_PER_COMPONENT]

        # common error strings within this component
        sig_counter: Counter = Counter()
        for issue in matched:
            for sig in issue["_sigs"]:
                sig_counter[sig] += 1
        common_errors = [
            {"signature": sig, "issues": n, "example": sig_example.get(sig, "")}
            for sig, n in sig_counter.most_common(15) if n >= 2
        ]

        related = []
        for script in quirk_scripts:
            if cdef["script_re"].search(script["_haystack"]):
                related.append({
                    "name": script["name"],
                    "path": script["path"],
                    "sourceUrl": script["sourceUrl"],
                    "summary": script["summary"],
                })
        related = related[:40]

        components_out.append({
            "key": key,
            "title": cdef["title"],
            "matchPattern": cdef["pattern"],
            "counts": {
                "issues": len(matched),
                "open": open_n,
                "closed": len(matched) - open_n,
                "discussions": len(matched_disc),
            },
            "topIssues": [slim_issue(i) for i in top],
            "recentIssues": [slim_issue(i) for i in recent],
            "commonErrorStrings": common_errors,
            "relatedQuirkScripts": related,
        })

    components_out.sort(key=lambda c: -c["counts"]["issues"])
    write_json(ISSUE_DIR / "components.json", {
        "source": f"github.com/{raw.get('repo', 'omacom/omarchy')}",
        "fetchedAt": fetched_at,
        "derivedAt": datetime.now(timezone.utc).isoformat(),
        "quirkScriptRef": SOURCE_REF,
        "matchScope": "issue/discussion title + body (opening post only)",
        "components": components_out,
    })

    # ================================================================ models
    log("deriving models.json ...")
    models: dict[str, dict] = {}

    def ensure_model(key, vendor, model):
        return models.setdefault(key, {
            "key": key,
            "vendor": vendor,
            "model": model,
            "aliases": set(),
            "variants": set(),
            "issues": [],
            "componentCounts": Counter(),
            "dmiHints": Counter(),
        })

    for issue in issues:
        found = extract_models(issue["_text"])
        if not found:
            continue
        hints = extract_dmi_hints(issue["_text"])
        for key, info in found.items():
            entry = ensure_model(key, info["vendor"], info["model"])
            entry["aliases"].update(info["matches"])
            entry["variants"].update(info["variants"])
            entry["issues"].append(issue)
            for comp in issue["_components"]:
                entry["componentCounts"][comp] += 1
            for hint in hints:
                entry["dmiHints"][hint] += 1

    disc_model_counts: Counter = Counter()
    for disc in discussions:
        for key in extract_models(disc["_text"]):
            disc_model_counts[key] += 1

    # quirk scripts per model
    def scripts_for_model(entry) -> list[dict]:
        model_words = re.findall(r"[a-z0-9]+", entry["model"].lower())
        vendor_token = entry["vendor"].lower().split()[0]
        stop = {"laptop", "book", "the", "pro", "air", "mini", "gen"}
        distinctive = {
            w for w in model_words
            if w != vendor_token and w not in stop and (len(w) >= 3 or w.isdigit())
        }
        # digits must not be part of a longer number (USB ids, versions, ...)
        matchers = [
            re.compile(rf"(?<!\d){re.escape(t)}(?!\d)") if t.isdigit() else re.compile(re.escape(t))
            for t in sorted(distinctive)
        ]
        joined = " ".join(model_words)
        out = []
        for script in quirk_scripts:
            hay = script["_haystack"]
            hit = joined in hay
            if not hit and matchers and vendor_token in hay:
                hit = any(rx.search(hay) for rx in matchers)
            if hit:
                out.append({
                    "name": script["name"],
                    "path": script["path"],
                    "sourceUrl": script["sourceUrl"],
                    "summary": script["summary"],
                })
        return out[:20]

    legacy_rows = parse_legacy_prototype()
    log(f"parsed {len(legacy_rows)} legacy prototype entries")
    legacy_by_key: dict[str, list[dict]] = defaultdict(list)
    legacy_unmatched: list[dict] = []
    for row in legacy_rows:
        haystack = " ".join([
            row.get("name", ""), row.get("tags", ""), row.get("brand", ""),
            (row.get("id", "") or "").replace("-", " "),
        ])
        keys = list(extract_models(haystack).keys())
        placed = False
        for key in keys:
            if key in models:
                legacy_by_key[key].append(row)
                placed = True
        if not placed:
            row["_fallbackKey"] = keys[0] if keys else slugify(
                f"{row.get('brand', '')} {row.get('name', '')}")
            row["_fallbackVendor"] = row.get("brand") or "Unknown"
            legacy_unmatched.append(row)

    def legacy_payload(row: dict) -> dict:
        payload = {
            "id": row.get("id"),
            "name": row.get("name"),
            "brand": row.get("brand"),
            "rating": row.get("rating"),
            "summary": row.get("summary"),
            "type": row.get("type"),
            "tags": row.get("tags"),
            "wifi": row.get("wifi"),
            "audio": row.get("audio"),
            "webcam": row.get("webcam"),
            "fingerprint": row.get("fingerprint"),
            "gpu": row.get("gpu"),
            "suspend": row.get("suspend"),
            "href": row.get("href"),
        }
        return {k: v for k, v in payload.items() if v not in (None, "")}

    models_out = []
    for key, entry in models.items():
        issue_list = sorted(entry["issues"], key=lambda i: (i.get("createdAt") or ""), reverse=True)
        open_n = sum(1 for i in issue_list if i["state"] == "OPEN")
        record = {
            "key": key,
            "vendor": entry["vendor"],
            "model": entry["model"],
            "aliases": sorted(entry["aliases"])[:15],
            "variants": sorted(entry["variants"])[:20],
            "counts": {
                "issues": len(issue_list),
                "open": open_n,
                "closed": len(issue_list) - open_n,
                "discussions": disc_model_counts.get(key, 0),
            },
            "components": [
                {"key": c, "issues": n}
                for c, n in entry["componentCounts"].most_common()
            ],
            "issues": [
                {
                    "number": i["number"],
                    "title": i["title"],
                    "url": i["url"],
                    "state": i["state"],
                    "components": i["_components"],
                    "createdAt": i.get("createdAt"),
                }
                for i in issue_list[:MAX_ISSUES_PER_MODEL]
            ],
            "issuesTruncated": len(issue_list) > MAX_ISSUES_PER_MODEL,
            "quirkScripts": scripts_for_model(entry),
            "dmiHints": [h for h, _ in entry["dmiHints"].most_common(10)],
        }
        rows = legacy_by_key.get(key)
        if rows:
            record["legacyPrototype"] = legacy_payload(rows[0])
            if len(rows) > 1:
                record["legacyPrototypeAlso"] = [legacy_payload(r) for r in rows[1:]]
            record["legacyPrototypeSource"] = "legacy-prototype-unverified"
        models_out.append(record)

    models_out.sort(key=lambda m: (-m["counts"]["issues"], m["key"]))

    legacy_only_out = []
    for row in legacy_unmatched:
        legacy_only_out.append({
            "key": row["_fallbackKey"],
            "vendor": row["_fallbackVendor"],
            "model": row.get("name"),
            "source": "legacy-prototype-unverified",
            "counts": {"issues": 0, "open": 0, "closed": 0, "discussions": 0},
            "issues": [],
            "legacyPrototype": legacy_payload(row),
        })

    write_json(ISSUE_DIR / "models.json", {
        "source": f"github.com/{raw.get('repo', 'omacom/omarchy')}",
        "fetchedAt": fetched_at,
        "derivedAt": datetime.now(timezone.utc).isoformat(),
        "quirkScriptRef": SOURCE_REF,
        "counts": {
            "models": len(models_out),
            "legacyOnly": len(legacy_only_out),
        },
        "models": models_out,
        "legacyOnlyModels": legacy_only_out,
    })

    # ============================================================== clusters
    log("deriving clusters.json ...")

    def build_cluster(key, label, queries, issue_numbers=None, disc_numbers=None,
                      auto=False, signature=None):
        if issue_numbers is None:
            rx = build_query_regex(queries)
            matched = [i for i in issues if rx.search(i["_search"])]
            matched_disc = [d for d in discussions if rx.search(d["_search"])]
        else:
            rx = None
            matched = [issue_by_number[n] for n in sorted(issue_numbers) if n in issue_by_number]
            disc_set = disc_numbers or set()
            matched_disc = [d for d in discussions if d["number"] in disc_set]

        open_n = sum(1 for i in matched if i["state"] == "OPEN")
        top = sorted(matched, key=lambda i: (-issue_weight(i), i["number"]))[:TOP_ISSUES_PER_CLUSTER]

        best_answers = []
        for d in sorted(matched_disc, key=lambda d: (-(d.get("upvoteCount") or 0),
                                                     -(d.get("comments") or 0)))[:6]:
            ans = d.get("answer")
            if ans and ans.get("body"):
                best_answers.append({
                    "discussion": d["number"], "title": d["title"], "url": d["url"],
                    "category": d.get("category"), "upvoteCount": d.get("upvoteCount", 0),
                    "kind": "accepted-answer", "author": ans.get("author"),
                    "answerUrl": ans.get("url"), "snippet": ans.get("body", "")[:500],
                })
                continue
            tops = sorted(d.get("topComments") or [],
                          key=lambda c: -(c.get("upvoteCount") or 0))
            if tops:
                c = tops[0]
                best_answers.append({
                    "discussion": d["number"], "title": d["title"], "url": d["url"],
                    "category": d.get("category"), "upvoteCount": d.get("upvoteCount", 0),
                    "kind": "top-comment", "author": c.get("author"),
                    "answerUrl": c.get("url"), "snippet": (c.get("body") or "")[:500],
                })
            if len(best_answers) >= 5:
                break
        best_answers = best_answers[:5]

        examples: list[str] = []
        seen_examples = set()
        for issue in top + matched[:200]:
            for line in issue.get("_errorLinesAll", []):
                if rx is not None and not rx.search(line):
                    continue
                if signature is not None and normalize_signature(line) != signature:
                    continue
                if line not in seen_examples:
                    seen_examples.add(line)
                    examples.append(line)
                if len(examples) >= 5:
                    break
            if len(examples) >= 5:
                break
        if not examples and signature:
            ex = sig_example.get(signature)
            if ex:
                examples.append(ex)

        return {
            "key": key,
            "label": label,
            "query": queries,
            "discovered": "auto" if auto else "seed",
            "searchScope": "title+body+error-signature" if auto else "title+body+comments",
            "counts": {
                "issues": len(matched),
                "open": open_n,
                "closed": len(matched) - open_n,
                "discussions": len(matched_disc),
            },
            "versionsMentioned": version_counts(
                [i["_search"] for i in matched] + [d["_search"] for d in matched_disc]),
            "topIssues": [slim_issue(i) for i in top],
            "bestAnswers": best_answers,
            "exampleErrorLines": examples,
        }

    clusters = [build_cluster(k, label, queries) for k, label, queries in SEED_CLUSTERS]
    seed_keys = {c["key"] for c in clusters}
    seed_queries_lower = {q.lower() for _, _, qs in SEED_CLUSTERS for q in qs}

    auto_candidates = [
        (sig, nums) for sig, nums in sig_to_issues.items()
        if len(nums) >= MIN_AUTO_CLUSTER_ISSUES
    ]
    auto_candidates.sort(key=lambda kv: (-len(kv[1]), kv[0]))
    auto_added = 0
    for sig, nums in auto_candidates:
        if auto_added >= MAX_AUTO_CLUSTERS:
            break
        if any(q in sig for q in seed_queries_lower):
            continue
        key = "err-" + slugify(sig)[:60]
        if not key or key in seed_keys:
            continue
        seed_keys.add(key)
        label = sig_example.get(sig, sig)[:160]
        clusters.append(build_cluster(
            key, label, [sig], issue_numbers=nums,
            disc_numbers=sig_to_discussions.get(sig, set()), auto=True, signature=sig))
        auto_added += 1

    clusters.sort(key=lambda c: (-c["counts"]["issues"], c["key"]))
    write_json(ISSUE_DIR / "clusters.json", {
        "source": f"github.com/{raw.get('repo', 'omacom/omarchy')}",
        "fetchedAt": fetched_at,
        "derivedAt": datetime.now(timezone.utc).isoformat(),
        "counts": {"clusters": len(clusters), "seed": len(SEED_CLUSTERS), "auto": auto_added},
        "clusters": clusters,
    })

    # =========================================================== still-broken
    log("deriving still-broken.json ...")
    STILL_RE = re.compile(
        r"still|same issue|reproduc|not fixed|reopen|happening again|4\.0\.4|4\.0\.3", re.I)
    still_broken = []
    funnel = Counter()
    for issue in issues:
        if issue.get("stateReason") != "COMPLETED":
            continue
        funnel["completed"] += 1
        closed_at = parse_dt(issue.get("closedAt"))
        if not closed_at:
            continue
        if issue.get("recentComments"):
            funnel["withFetchedComments"] += 1
        hits = []
        for c in issue.get("recentComments") or []:
            cdt = parse_dt(c.get("createdAt"))
            if not cdt or cdt <= closed_at:
                continue
            if STILL_RE.search(c.get("body") or ""):
                hits.append(c)
        if hits:
            funnel["withAtLeastOnePostCloseMarker"] += 1
        if len(hits) < 2:
            continue
        funnel["withAtLeastTwoPostCloseMarkers"] += 1
        closer = issue.get("closedBy")
        closer_out = None
        if closer:
            if closer.get("type") == "pull_request":
                closer_out = {"type": "pull_request", "number": closer.get("number"),
                              "url": closer.get("url"), "merged": closer.get("merged"),
                              "mergedAt": closer.get("mergedAt")}
            elif closer.get("type") == "commit":
                closer_out = {"type": "commit", "sha": closer.get("oid"), "url": closer.get("url")}
            else:
                closer_out = {"type": closer.get("type")}
        still_broken.append({
            "number": issue["number"],
            "title": issue["title"],
            "url": issue["url"],
            "state": issue["state"],
            "stateReason": issue.get("stateReason"),
            "closedAt": issue.get("closedAt"),
            "closer": closer_out,
            "fixedBy": fixed_by_prs(issue),
            "components": issue["_components"],
            "comments": issue.get("comments", 0),
            "postCloseComments": len(hits),
            "sampleSnippets": [
                {"author": c.get("author"), "createdAt": c.get("createdAt"),
                 "url": c.get("url"), "snippet": (c.get("body") or "")[:300]}
                for c in hits[:3]
            ],
            "lastActivity": issue.get("updatedAt"),
        })
    still_broken.sort(key=lambda r: (-r["postCloseComments"], r.get("lastActivity") or ""),
                      reverse=False)
    still_broken.sort(key=lambda r: (r.get("lastActivity") or ""), reverse=True)
    write_json(ISSUE_DIR / "still-broken.json", {
        "source": f"github.com/{raw.get('repo', 'omacom/omarchy')}",
        "fetchedAt": fetched_at,
        "derivedAt": datetime.now(timezone.utc).isoformat(),
        "criteria": {
            "stateReason": "COMPLETED",
            "minPostCloseComments": 2,
            "commentMarkers": ["still", "same issue", "reproduc", "not fixed", "reopen",
                               "happening again", "4.0.4", "4.0.3"],
            "commentWindow": "last 5 comments fetched per closed issue",
        },
        "count": len(still_broken),
        "funnel": {
            "completedIssues": funnel["completed"],
            "withFetchedComments": funnel["withFetchedComments"],
            "withAtLeastOnePostCloseMarker": funnel["withAtLeastOnePostCloseMarker"],
            "withAtLeastTwoPostCloseMarkers": funnel["withAtLeastTwoPostCloseMarkers"],
        },
        "issues": still_broken,
    })

    # ================================================================= stats
    log("deriving stats.json ...")
    now = parse_dt(fetched_at) or datetime.now(timezone.utc)
    open_issues = [i for i in issues if i["state"] == "OPEN"]
    closed_issues = [i for i in issues if i["state"] == "CLOSED"]

    def opened_within(days: int) -> int:
        cutoff = now - timedelta(days=days)
        return sum(1 for i in issues if (parse_dt(i.get("createdAt")) or now) >= cutoff)

    closed_sorted = sorted(
        (i for i in closed_issues if i.get("closedAt")),
        key=lambda i: i["closedAt"], reverse=True)[:300]
    ttc_hours = []
    for i in closed_sorted:
        created, closed = parse_dt(i.get("createdAt")), parse_dt(i.get("closedAt"))
        if created and closed:
            ttc_hours.append((closed - created).total_seconds() / 3600.0)
    median_ttc = round(statistics.median(ttc_hours), 2) if ttc_hours else None

    closed_by_merged_pr = 0
    closed_by_commit = 0
    closed_with_merged_pr_ref = 0
    for i in closed_issues:
        closer = i.get("closedBy") or {}
        if closer.get("type") == "pull_request" and closer.get("merged"):
            closed_by_merged_pr += 1
        elif closer.get("type") == "commit":
            closed_by_commit += 1
        if any(r.get("merged") for r in i.get("referencedPRs") or []):
            closed_with_merged_pr_ref += 1

    label_counts: Counter = Counter()
    for i in issues:
        label_counts.update(i.get("labels") or [])

    disc_by_cat: Counter = Counter()
    disc_answered_by_cat: Counter = Counter()
    for d in discussions:
        cat = d.get("category") or "Uncategorized"
        disc_by_cat[cat] += 1
        if d.get("isAnswered"):
            disc_answered_by_cat[cat] += 1
    answered_total = sum(disc_answered_by_cat.values())

    stats = {
        "source": f"github.com/{raw.get('repo', 'omacom/omarchy')}",
        "fetchedAt": fetched_at,
        "derivedAt": datetime.now(timezone.utc).isoformat(),
        "issues": {
            "total": len(issues),
            "open": len(open_issues),
            "closed": len(closed_issues),
            "openedLast30Days": opened_within(30),
            "openedLast7Days": opened_within(7),
            "zeroCommentOpen": sum(1 for i in open_issues if (i.get("comments") or 0) == 0),
            "medianTimeToCloseHoursLast300": median_ttc,
            "medianTimeToCloseDaysLast300": round(median_ttc / 24, 2) if median_ttc else None,
            "closedByMergedPR": closed_by_merged_pr,
            "closedByCommit": closed_by_commit,
            "pctClosedByMergedPR": round(100.0 * closed_by_merged_pr / len(closed_issues), 2)
            if closed_issues else 0.0,
            "closedWithMergedPRReferenced": closed_with_merged_pr_ref,
            "pctClosedWithMergedPRReferenced": round(
                100.0 * closed_with_merged_pr_ref / len(closed_issues), 2) if closed_issues else 0.0,
            "stateReasons": dict(Counter(i.get("stateReason") or "NONE" for i in issues).most_common()),
        },
        "discussions": {
            "total": len(discussions),
            "answered": answered_total,
            "answeredRate": round(100.0 * answered_total / len(discussions), 2) if discussions else 0.0,
            "byCategory": [
                {
                    "category": cat,
                    "count": n,
                    "answered": disc_answered_by_cat.get(cat, 0),
                    "answeredRate": round(100.0 * disc_answered_by_cat.get(cat, 0) / n, 2),
                }
                for cat, n in disc_by_cat.most_common()
            ],
        },
        "topLabels": [{"label": l, "count": n} for l, n in label_counts.most_common(10)],
        "derived": {
            "components": len(components_out),
            "models": len(models_out),
            "legacyOnlyModels": len(legacy_only_out),
            "clusters": len(clusters),
            "stillBroken": len(still_broken),
        },
    }
    write_json(ISSUE_DIR / "stats.json", stats)

    if args.verbose:
        log("\ncomponent counts:")
        for c in components_out:
            log(f"  {c['key']:<22} {c['counts']['issues']:>5} issues "
                f"({c['counts']['open']} open) {c['counts']['discussions']:>4} discussions")
        log("\ntop 15 models:")
        for m in models_out[:15]:
            log(f"  {m['key']:<32} {m['counts']['issues']:>4} issues")
        log("\ntop 20 clusters:")
        for c in clusters[:20]:
            log(f"  {c['key']:<34} {c['counts']['issues']:>5} issues "
                f"{c['counts']['discussions']:>4} discussions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
