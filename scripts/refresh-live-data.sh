#!/usr/bin/env bash
# Refresh every live-data file under data/ for omarchylinux.org.
#
#   scripts/fetch_channels.py          -> data/channels.json, data/channels-history.jsonl
#   scripts/fetch_iso_index.py         -> data/isos.json
#   scripts/check_domains.py           -> data/domains.json
#   scripts/fetch_foundation_facts.py  -> data/facts.json
#
# A source being down must never break a site build, so this script always exits 0 and
# reports per-step status in its summary instead.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
DATA="$ROOT/data"
PYTHON="${PYTHON:-python3}"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$DATA"

STEP_NAMES=()
STEP_STATUS=()
STEP_SECONDS=()

run_step() {
  local label="$1"; shift
  local start end rc
  echo ""
  echo "=== $label ==="
  start=$(date +%s)
  "$@"
  rc=$?
  end=$(date +%s)
  STEP_NAMES+=("$label")
  STEP_SECONDS+=("$((end - start))")
  if [ "$rc" -eq 0 ]; then
    STEP_STATUS+=("ok")
  else
    STEP_STATUS+=("FAILED(rc=$rc)")
    echo "!! $label failed with exit code $rc -- continuing" >&2
  fi
  return 0
}

echo "omarchylinux.org live-data refresh, started $STARTED_AT"
echo "root: $ROOT"

run_step "channels (pkgs.omarchy.org + mirrors)" "$PYTHON" "$SCRIPT_DIR/fetch_channels.py"
run_step "isos (iso.omarchy.org + GitHub tags)"  "$PYTHON" "$SCRIPT_DIR/fetch_iso_index.py"
run_step "domains (dig + curl + whois)"          "$PYTHON" "$SCRIPT_DIR/check_domains.py"
run_step "facts (momentum + discord + wikipedia)" "$PYTHON" "$SCRIPT_DIR/fetch_foundation_facts.py"

echo ""
echo "=== summary ==="
printf '%-45s %-14s %s\n' "STEP" "STATUS" "SECONDS"
for i in "${!STEP_NAMES[@]}"; do
  printf '%-45s %-14s %s\n' "${STEP_NAMES[$i]}" "${STEP_STATUS[$i]}" "${STEP_SECONDS[$i]}"
done

echo ""
echo "=== outputs ==="
for f in channels.json isos.json domains.json facts.json channels-history.jsonl; do
  path="$DATA/$f"
  if [ -f "$path" ]; then
    size=$(wc -c < "$path" | tr -d ' ')
    mtime=$(date -u -r "$path" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "?")
    printf '  %-26s %10s bytes  %s\n' "$f" "$size" "$mtime"
  else
    printf '  %-26s %s\n' "$f" "MISSING"
  fi
done

# Headline numbers, best-effort: a malformed or missing file must not fail the run.
"$PYTHON" - "$DATA" <<'PY' || true
import json, os, sys
data = sys.argv[1]

def load(name):
    try:
        with open(os.path.join(data, name), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

print("")
print("=== headlines ===")

ch = load("channels.json")
if ch:
    for m in ch.get("mirrors", []):
        print(f"  mirror {m['name']:<15} lastupdate={m['lastupdate'].get('iso')} "
              f"lag={m.get('lagHoursVsUpstream')}h")
    print(f"  omarchy package: {ch.get('omarchyPackage')}")
    print("  packages: " + ", ".join(
        f"{k}={v.get('packageCount')}" for k, v in (ch.get("channels") or {}).items()))
    print("  diffs: " + ", ".join(f"{k}={len(v)}" for k, v in (ch.get("diffs") or {}).items()))

iso = load("isos.json")
if iso:
    print(f"  isos: {iso.get('availableIsoCount')} of {len(iso.get('isos', []))} tags "
          f"currently downloadable")

dom = load("domains.json")
if dom:
    s = dom.get("summary", {})
    print(f"  domains: {s.get('total')} entries, {s.get('resolving')} resolving, "
          f"{s.get('discrepancies')} discrepancies vs seed")
    for e in dom.get("domains", []):
        if e.get("discrepancy"):
            print(f"    ! {e['host']}: {e['discrepancy']}")

facts = load("facts.json")
if facts:
    gh = (facts.get("momentum") or {}).get("github", {})
    dc = facts.get("discord") or {}
    print(f"  github stars={gh.get('stars')} contributors={gh.get('contributors')}; "
          f"discord members={dc.get('approximateMemberCount')}")
    errs = facts.get("errors") or []
    if errs:
        print(f"  facts source failures: {errs}")
PY

echo ""
echo "refresh finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit 0
