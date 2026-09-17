#!/usr/bin/env bash
# Rebuild the issue-derived data for omarchylinux.org.
#
#   1. fetch  github.com/omacom/omarchy issues + discussions -> data/issues/raw*.json
#      (resumes from the on-disk page cache, so an interrupted run is cheap to retry)
#   2. derive components / models / clusters / still-broken / stats
#
# Usage:
#   scripts/build-issue-data.sh              # resume fetch, then derive
#   scripts/build-issue-data.sh --fresh      # ignore the cache and refetch everything
#   scripts/build-issue-data.sh --derive-only
#
# Requires: python3 (3.12+, stdlib only) and an authenticated `gh` CLI.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FETCH_ARGS=(--resume)
RUN_FETCH=1

for arg in "$@"; do
  case "$arg" in
    --fresh) FETCH_ARGS=() ;;
    --derive-only) RUN_FETCH=0 ;;
    -h | --help)
      sed -n '2,14p' "${BASH_SOURCE[0]}"
      exit 0
      ;;
    *)
      echo "unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

command -v python3 >/dev/null || {
  echo "python3 is required" >&2
  exit 1
}
command -v gh >/dev/null || {
  echo "the gh CLI is required (https://cli.github.com)" >&2
  exit 1
}

if [[ $RUN_FETCH -eq 1 ]]; then
  gh auth status >/dev/null 2>&1 || {
    echo "gh is not authenticated - run: gh auth login" >&2
    exit 1
  }
  echo "==> fetching issues and discussions"
  python3 scripts/fetch_issues.py "${FETCH_ARGS[@]}"
fi

echo "==> deriving issue data"
python3 scripts/derive_issue_data.py --verbose

echo "==> done"
ls -la data/issues/components.json data/issues/models.json data/issues/clusters.json \
  data/issues/still-broken.json data/issues/stats.json
