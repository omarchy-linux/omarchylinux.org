#!/usr/bin/env bash
# Deploy dist/ to Cloudflare Pages. Creates the project on first run.
#
# Needs CLOUDFLARE_API_TOKEN in the environment. CLOUDFLARE_ACCOUNT_ID is
# looked up automatically when the token can read more than one account.
#
#   export CLOUDFLARE_API_TOKEN=...
#   bash scripts/deploy-cloudflare.sh
set -euo pipefail

PROJECT="${CF_PAGES_PROJECT:-omarchylinux-org}"
BRANCH="${CF_PAGES_BRANCH:-main}"
cd "$(dirname "$0")/.."

if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "CLOUDFLARE_API_TOKEN is not set." >&2
  echo "Create one at https://dash.cloudflare.com/profile/api-tokens with:" >&2
  echo "  Account > Cloudflare Pages > Edit      (create the project and deploy)" >&2
  echo "  Zone    > DNS > Edit  on omarchylinux.org   (attach the custom domain)" >&2
  exit 1
fi

api() { curl -sS -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" "$@"; }

if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  echo "Looking up account id..."
  CLOUDFLARE_ACCOUNT_ID=$(api https://api.cloudflare.com/client/v4/accounts \
    | python3 -c 'import sys,json; r=json.load(sys.stdin); assert r.get("success"), r; a=r["result"]; print(a[0]["id"]) if a else sys.exit("no accounts visible to this token")')
  export CLOUDFLARE_ACCOUNT_ID
fi
echo "Account: $CLOUDFLARE_ACCOUNT_ID"

echo "Building..."
npm run build

exists=$(api "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/$PROJECT" \
  | python3 -c 'import sys,json; print("yes" if json.load(sys.stdin).get("success") else "no")')

if [ "$exists" = "no" ]; then
  echo "Creating Pages project '$PROJECT'..."
  api -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects" \
    --data "{\"name\":\"$PROJECT\",\"production_branch\":\"$BRANCH\"}" \
    | python3 -c 'import sys,json; r=json.load(sys.stdin); print("  created" if r.get("success") else "  "+json.dumps(r.get("errors")))'
fi

echo "Deploying..."
npx wrangler pages deploy dist --project-name="$PROJECT" --branch="$BRANCH" --commit-dirty=true

echo
echo "Deployed. Attach the custom domain once:"
echo "  npx wrangler pages domain add omarchylinux.org --project-name=$PROJECT"
echo "  npx wrangler pages domain add www.omarchylinux.org --project-name=$PROJECT"
