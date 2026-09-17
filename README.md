# omarchylinux.org

Unofficial, version-stamped field manual for [Omarchy Linux](https://omarchy.org): hardware compatibility reports, one page per error with the fix first, a generated command and keybinding reference, and what changed between releases.

**Not affiliated** with 37signals or the Omacom Foundation. Omarchy is a registered trademark of 37signals LLC. This site never hosts installers; downloads link only to omarchy.org.

## Stack

- [Astro](https://astro.build) static site, no client framework. Search is [Pagefind](https://pagefind.app), built after `astro build`.
- Content lives in `src/content/<section>/*.md` with a strict frontmatter schema (`src/content.config.ts`). Every page carries `appliesTo`, `status`, `lastVerified`, `sources`, and `credits`.
- Reference data is generated from the MIT-licensed `omacom/omarchy` source per release tag by `scripts/build-data.sh` into `data/`.
- Issue-derived data (component hubs, model mentions, error clusters, still-broken list) comes from `scripts/build-issue-data.sh` (needs an authenticated `gh`).
- Live data (channels, mirrors, ISO checksums, domain registry, facts) comes from `scripts/refresh-live-data.sh`.

## Develop

```bash
npm install
bash scripts/build-data.sh --fetch      # once; downloads source snapshots into data/source/ (gitignored)
bash scripts/build-issue-data.sh        # optional, ~10 min, needs gh auth
bash scripts/refresh-live-data.sh       # optional, ~2 min
npm run dev                             # http://localhost:4321
npm run build                           # dist/ + Pagefind index
node scripts/linkcheck.mjs              # internal links
node scripts/validate-content.mjs       # frontmatter rules
node scripts/og.mjs                     # regenerate Open Graph images
```

## Before you go live

Five things need your input. Everything else is done.

1. **Create the GitHub repository** and push. The site links to it for "Improve this page" and the hardware-report form, so until it exists those two links 404. If you use a different name or account, change `repo` and `editBase` in `src/lib/site.ts`.
2. **Set the contact address.** `src/lib/site.ts` has `contact: 'hello@omarchylinux.org'`. Point it somewhere you read, or change it to a GitHub discussions link.
3. **Point DNS at the host.** The domain is already on Cloudflare nameservers. Create the Pages project (below), then add the custom domain `omarchylinux.org` in the Pages dashboard, which writes the DNS record for you.
4. **Email the Omacom Foundation before launch.** Draft is in the research brief: tell them what the site is, that you will never host installers or use their logo, and that the domain is theirs on request. Keep the reply.
5. **Verify the trademark facts are still current** on `/official/trademark/` (USPTO records change) and re-run `bash scripts/refresh-live-data.sh`.

## Deploy

The domain is on Cloudflare. Create a Cloudflare Pages project named `omarchylinux-org`, connect this repository (build command `npm run build`, output `dist`), or set the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets and let `.github/workflows/deploy.yml` deploy on push to `main`. `public/_headers` and `public/_redirects` are picked up by Pages automatically. Any static host works; `dist/` is plain files.

`.github/workflows/nightly-data.yml` refreshes `data/` every night and commits, which triggers a rebuild.

## Writing a page

Copy the frontmatter from an existing page in the same section. Rules that the validator enforces: block-style YAML, a 120-160 character description, a 40-80 word answer, headings from `##`, no em dashes, absolute internal links, no direct `.iso` links. Paraphrase sources and credit people; GitHub comments are not licensed for republication.

## Layout

```
src/content/   fix, hardware, switch, keyboard, vs, run, upgrade, security, reference, official, pages
src/pages/     routes; every content page also has a .md twin and every section has an index
src/layouts/   Base (head, JSON-LD, header, footer) and Article (answer box, badges, sources, FAQ)
src/lib/       site constants, SEO helpers, data loaders
data/          generated JSON (committed) and source snapshots (gitignored)
scripts/       extraction and refresh scripts, OG image generator, validators
legacy-site/   the September 2026 hand-written prototype, kept for reference; redirected via public/_redirects
```

## Licenses

Site text CC BY 4.0. Data exports CC0. Upstream source excerpts MIT (omacom/omarchy). Fonts: Barlow Condensed, Source Sans 3, IBM Plex Mono (OFL).
