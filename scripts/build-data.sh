#!/usr/bin/env bash
# Build every data/ artefact for omarchylinux.org from the snapshots in
# data/source/. Idempotent: re-running overwrites the generated JSON in place.
#
# Usage:
#   scripts/build-data.sh            # build from the snapshots already present
#   scripts/build-data.sh --fetch    # download any missing snapshot first
#   scripts/build-data.sh --no-versions   # skip the GitHub releases fetch

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
SOURCE_DIR="$ROOT/data/source"
PYTHON=${PYTHON:-python3}

REFS=(v3.8.4 v4.0.0 v4.0.1 v4.0.2 v4.0.3 v4.0.4)
DEV_REF=quattro-dev
DEV_BRANCH=quattro   # omacom/omarchy default branch

FETCH=false
RUN_VERSIONS=true

for arg in "$@"; do
  case "$arg" in
  --fetch) FETCH=true ;;
  --no-versions) RUN_VERSIONS=false ;;
  -h | --help)
    sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  *)
    echo "Unknown option: $arg" >&2
    exit 2
    ;;
  esac
done

have_snapshot() {
  local dir="$1"
  [[ -d $dir ]] && [[ -n $(ls -A "$dir" 2>/dev/null) ]]
}

fetch_ref() {
  local ref="$1" url="$2" dir="$SOURCE_DIR/$ref"
  echo "  fetching $ref"
  mkdir -p "$dir"
  curl -sLf "$url" | tar -xz --strip-components=1 -C "$dir"
}

echo "==> snapshots"
missing=()
for ref in "${REFS[@]}" "$DEV_REF"; do
  if have_snapshot "$SOURCE_DIR/$ref"; then
    printf '  %-14s present\n' "$ref"
  else
    printf '  %-14s MISSING\n' "$ref"
    missing+=("$ref")
  fi
done

if ((${#missing[@]} > 0)); then
  if [[ $FETCH == true ]]; then
    for ref in "${missing[@]}"; do
      if [[ $ref == "$DEV_REF" ]]; then
        fetch_ref "$ref" "https://github.com/omacom/omarchy/archive/refs/heads/$DEV_BRANCH.tar.gz"
      else
        fetch_ref "$ref" "https://github.com/omacom/omarchy/archive/refs/tags/$ref.tar.gz"
      fi
    done
  else
    echo "  (re-run with --fetch to download the missing snapshots)"
  fi
fi

if ! have_snapshot "$SOURCE_DIR"; then
  echo "data/source is empty; nothing to build" >&2
  exit 1
fi

echo
echo "==> extracting"
"$PYTHON" "$SCRIPT_DIR/extract_commands.py"
"$PYTHON" "$SCRIPT_DIR/extract_bindings.py"
"$PYTHON" "$SCRIPT_DIR/extract_menu.py"
"$PYTHON" "$SCRIPT_DIR/extract_migrations.py"
"$PYTHON" "$SCRIPT_DIR/extract_hooks.py"

echo
echo "==> diffs"
"$PYTHON" "$SCRIPT_DIR/diff_data.py"

echo
echo "==> releases"
if [[ $RUN_VERSIONS == true ]]; then
  "$PYTHON" "$SCRIPT_DIR/versions.py"
else
  echo "  skipped (--no-versions)"
fi

echo
"$PYTHON" - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
data = root / "data"

tags = json.loads((data / "commands" / "index.json").read_text())["tags"]

def load(kind, tag):
    path = data / kind / f"{tag}.json"
    return json.loads(path.read_text()) if path.is_file() else {}

rows = []
for tag in tags:
    commands = load("commands", tag)
    bindings = load("bindings", tag)
    menu = load("menu", tag)
    migrations = load("migrations", tag)
    hooks = load("hooks", tag)
    rows.append((
        tag,
        commands.get("count", 0),
        sum(1 for c in commands.get("commands", []) if c["hasMetadata"]),
        bindings.get("count", 0),
        bindings.get("format") or "-",
        menu.get("count", 0),
        migrations.get("count", 0),
        len(hooks.get("events", [])),
        "yes" if commands.get("prerelease") else "no",
    ))

headers = ("tag", "commands", "w/meta", "bindings", "fmt", "menu", "migrations",
           "hooks", "prerelease")
widths = [max(len(str(r[i])) for r in [headers, *rows]) for i in range(len(headers))]

def render(row):
    return "  " + "  ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)).rstrip()

print("==> summary")
print(render(headers))
print("  " + "  ".join("-" * w for w in widths))
for row in rows:
    print(render(row))

diffs = json.loads((data / "diffs" / "index.json").read_text())["diffs"]
print()
dheaders = ("diff", "cmd +", "cmd -", "cmd ~", "bind +", "bind -", "bind ~",
            "menu +", "menu -", "migr +")
drows = []
for d in diffs:
    c, b, m, g = (d["summary"][k] for k in ("commands", "bindings", "menu", "migrations"))
    drows.append((d["name"], c["added"], c["removed"], c["changed"],
                  b["added"], b["removed"], b["changedAction"],
                  m["added"], m["removed"], g["new"]))
dwidths = [max(len(str(r[i])) for r in [dheaders, *drows]) for i in range(len(dheaders))]

def drender(row):
    return "  " + "  ".join(str(v).ljust(dwidths[i]) for i, v in enumerate(row)).rstrip()

print(drender(dheaders))
print("  " + "  ".join("-" * w for w in dwidths))
for row in drows:
    print(drender(row))

versions = data / "versions.json"
if versions.is_file():
    v = json.loads(versions.read_text())
    print()
    print(f"  releases: {v['count']}   latest: {v['latest']}")

owned = ["commands", "bindings", "menu", "migrations", "hooks", "diffs"]
files = sorted(p for d in owned for p in (data / d).glob("*.json"))
files.append(data / "versions.json")
files = [p for p in files if p.is_file()]
total = sum(p.stat().st_size for p in files)
print()
print(f"  {len(files)} JSON files written, {total / 1024 / 1024:.1f} MB total")
PY
