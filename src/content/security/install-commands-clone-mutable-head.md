---
title: "omarchy plugin add clones upstream HEAD with no pin"
description: "omarchy plugin add and omarchy theme install do a bare git clone of a repo's current HEAD. No commit pin, no signature. What that means and how to pin yourself."
answer: "Both commands are a plain git clone of whatever the repository's default branch points at right now. There is no commit argument, no tag, and no signature check. Clone the repo yourself, read it, check out a specific commit, then move it into ~/.config/omarchy/plugins/ and enable it. A signed registry at plugins.omarchy.org is designed but its Omarchy-side client is not built yet."
appliesTo:
  from: "3.x"
status: open
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: medium
reported: "Stated by Omarchy's own plugin marketplace in its README security notice and SECURITY.md"
projectResponse: "The marketplace README says the current install and update commands clone mutable upstream HEAD and are not verification-bound, and the omacom/omarchy-plugin-registry design replaces them with signed, checksummed tarballs while demoting git URLs to an --unsafe flag."
tags: [plugins, themes, supply-chain, registry, quickshell, security]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-plugin-add"
    title: "omarchy-plugin-add at tag v4.0.4"
    kind: other
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-theme-install"
    title: "omarchy-theme-install at tag v4.0.4"
    kind: other
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-plugin-validate"
    title: "omarchy-plugin-validate at tag v4.0.4"
    kind: other
  - url: "https://github.com/omacom/omarchy-plugin-marketplace"
    title: "omacom/omarchy-plugin-marketplace: Community-curated marketplace for Omarchy plugins"
    kind: docs
  - url: "https://github.com/omacom/omarchy-plugin-marketplace/blob/main/SECURITY.md"
    title: "Marketplace SECURITY.md: Automated Security Baseline"
    kind: docs
  - url: "https://github.com/omacom/omarchy-plugin-registry"
    title: "omacom/omarchy-plugin-registry: the hosted plugin registry for Omarchy Quattro"
    kind: docs
  - url: "https://github.com/omacom/omarchy-plugin-registry/blob/main/docs/client-spec.md"
    title: "Registry docs: client contract for omarchy plugin and plugins.omarchy.org"
    kind: docs
  - url: "https://github.com/omacom/omarchy-plugin-registry/blob/main/docs/design.md"
    title: "Registry docs: design, section 11 Rollout"
    kind: docs
  - url: "https://github.com/omacom/omarchy/issues/11375"
    title: "Issue #11375: plugins.omarchy.org shows broken 'omarchy bar plugin add' command for first-party plugins"
    kind: issue
    author: "a3qz"
    date: "2026-09-11"
  - url: "https://plugins.omarchy.org/catalog.json"
    title: "Omarchy plugin marketplace catalog JSON"
    kind: other
    date: "2026-09-16"
  - url: "https://omarchy.org/manual/shell-plugins/"
    title: "Omarchy manual: Shell Plugins"
    kind: manual
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "a3qz"
    url: "https://github.com/a3qz"
    for: "Documented that omarchy-plugin-add only ever accepts a git URL and has no path for a plugin id"
faq:
  - q: "Does omarchy plugin add run code from the repo during install?"
    a: "No. It clones, validates the manifest, checks for an id collision, and asks before enabling. It runs no install hook and never asks for sudo. The exposure starts when you enable the plugin, and it reopens on every update."
  - q: "Can I tell the CLI to install a specific commit or tag?"
    a: "Not at 4.0.4. The command takes a URL, --enable and --yes, and nothing else. Pinning means doing the clone and the checkout yourself."
  - q: "Is omarchy theme install any safer?"
    a: "The clone is the same, but a theme is mostly data and omarchy-theme-set stages only the files an extra theme is allowed to contribute. The weaker part is omarchy theme update, which runs git pull on every user theme with no diff and no prompt."
  - q: "Will the signed registry at plugins.omarchy.org fix this?"
    a: "That is its purpose. Its README lists the registry side as built and the Omarchy-side client, including signature and freshness verification, as not yet done and required before launch."
related: [plugins-run-unsandboxed, docker-group-root-escalation, is-omarchy-safe]
draft: false
---

## What the two commands actually do

Checked against the v4.0.4 source tree, `omarchy plugin add` and `omarchy theme install` both end in a plain `git clone` of whatever the repository's default branch points at at that moment.

`bin/omarchy-plugin-add` does this, in order:

1. Runs `omarchy-git-url-check` on the URL. That helper refuses a `helper::address` form and any `scheme://` that git does not connect itself, so a URL cannot name `ext::` and run a shell command at clone time. It landed in 4.0.1. It is a check on the URL, not on the code.
2. Prints a warning that plugins run as arbitrary, unsandboxed code inside your long-lived shell process, shows the URL, and asks you to confirm.
3. Runs `git clone -- "$url" "$stage"` into a staging directory under `~/.config/omarchy/plugins/`.
4. Runs `omarchy-plugin-validate` on the staged folder.
5. Refuses if another plugin already claims that id, moves the folder to `~/.config/omarchy/plugins/<id>/`, and asks whether to enable it.

There is no `--rev`, no branch or tag argument, no checksum, and no signature anywhere in that path. The command accepts a URL, `--enable` and `--yes`. Issue #11375 makes the same point from the other direction while reporting a website bug: `omarchy-plugin-add` always requires a git URL and has no code path for a bare plugin id.

`bin/omarchy-theme-install` has the same shape. It runs the same URL check, derives a theme name from the repository path and holds it to a safe character set, deletes any existing directory of that name, then `git clone -- "$REPO_URL" "$THEME_PATH"`.

Updates differ between the two:

- `omarchy plugin update` fetches `origin HEAD`, shows you the full diff before applying it, asks you to confirm, fast-forwards, revalidates, and resets back with `git reset --hard ORIG_HEAD` if the new revision fails validation. That review step is the strongest control in the whole flow, and it disappears if you pass `--yes`.
- `omarchy theme update` runs `git -C "$theme" pull` for every user-installed theme. No diff, no prompt.

It matters what `omarchy-plugin-validate` is and is not. It checks `schemaVersion`, required manifest fields, an id outside the reserved `omarchy.` namespace, entry points that are safe relative paths and exist, an entry point for every declared kind, and no symlinks inside the folder. It is a manifest check. It reads none of the QML that will run inside your shell.

## Omarchy's own marketplace says the same thing

The community marketplace at plugins.omarchy.org, repo `omacom/omarchy-plugin-marketplace`, publishes a security notice in its README. It says upstream code may change after review unless the installed version is pinned to the reviewed commit, and then states plainly that the current install and update commands "clone mutable upstream HEAD and are not verification-bound".

The gap is measurable. The marketplace catalog records both `listingValidatedCommit`, the commit its baseline scan actually read, and `upstreamObservedCommit`, what the default branch points at now. In the catalog generated on 2026-09-16 there were 2,921 listings with a working install command, and 771 of them, about one in four, had moved past the commit that was reviewed. The catalog marks every one of those 771 as unverified. Copy the install line from one of their listing pages and you get the current HEAD, not the commit the scan read.

There is a second irony worth knowing. The marketplace's own Automated Security Baseline flags `remote-git-execution-unpinned` inside a submitted plugin: code pulled from an external git repository and run without being bound to a full commit. Omarchy's install command is that pattern, applied to the plugin itself.

## Pin it yourself

Nothing here needs new tooling. Use the clone as a staging area and do the review before the code ever runs.

1. Clone somewhere harmless and read it. Plugins are QML plus a manifest, so this is usually a short read.

```bash
git clone https://github.com/acme/omarchy-weather.git /tmp/omarchy-weather
cd /tmp/omarchy-weather
git log --oneline -10
```

2. If the plugin is listed on the marketplace, get the commit its scan actually read.

```bash
curl -s https://plugins.omarchy.org/catalog.json |
  jq -r '.plugins[]
         | select(.repo == "https://github.com/acme/omarchy-weather")
         | [.verificationStatus, .listingValidatedCommit, .upstreamObservedCommit]
         | @tsv'
```

3. Check out the commit you reviewed, or the one the scan reviewed, as a full 40 character SHA.

```bash
git -C /tmp/omarchy-weather checkout <full-sha>
```

4. Validate it and move it into place under its own manifest id, then enable it as a separate step.

```bash
id=$(jq -r .id /tmp/omarchy-weather/manifest.json)
omarchy plugin validate /tmp/omarchy-weather
mv /tmp/omarchy-weather ~/.config/omarchy/plugins/"$id"
omarchy-shell shell rescanPlugins
omarchy plugin enable "$id"
```

The directory name has to match the manifest id, because `omarchy plugin update` and `omarchy plugin remove` address plugins by id.

If you would rather stay on the supported path, run `omarchy plugin add <url>` without `--enable`, answer no when it offers to turn the plugin on, read the checkout in `~/.config/omarchy/plugins/<id>/`, then `git checkout` the commit you want and enable it. You still clone HEAD, but nothing has run yet.

For themes, clone and check out the same way into `~/.config/omarchy/themes/<name>/`, then run `omarchy theme set <name>`. Remember that `omarchy theme update` will pull every user theme forward without asking, so skip it if you are pinning.

## Verify the pin held

```bash
git -C ~/.config/omarchy/plugins/<id> rev-parse HEAD
git -C ~/.config/omarchy/plugins/<id> status --short --branch
omarchy plugin list
```

The first command should print the SHA you chose. The second should report a detached HEAD, which is what a pin looks like. `omarchy plugin list` should show the plugin with its id and enabled state.

## Why it works this way

Git URLs are the whole distribution mechanism today. The manual says as much: publish a public repo and anyone can run `omarchy plugin add` against your URL. Nothing else existed when the Quattro shell shipped in 4.0.0 on 2026-08-14, and theme installs worked the same way on 3.x, back when `omarchy-theme-install` did not even check the URL first.

Omarchy is honest about the consequence rather than hiding it. The install prompt tells you plugins run as arbitrary unsandboxed code, the manual repeats it, and the manual tells you to read the code before you enable anything. What is missing is not the warning. It is any way to record which code you read.

## The registry that is coming

`omacom/omarchy-plugin-registry` is a Rails control plane serving an append-only JSON index and immutable, checksummed tarballs at plugins.omarchy.org. Its client contract specifies a pinned Ed25519 public key, detached signatures on every index file, SHA-256 verification of each tarball, a signed revocation list that fails closed when stale, an install receipt written next to the manifest, and plugins that land disabled so enabling stays a separate consent step. The rollout plan puts git URL installs behind an `--unsafe` flag.

None of that is shipped. The registry README lists the Omarchy-side client, signature and freshness verification, receipts, the kill-bit check and deployment as not yet done and required before launch. There is no plugin registry code in the 4.0.4 `bin/` tree. Treat the registry as a design you can read, not a protection you have.

## What to watch for on newer versions

The next announced release is Quattro RS 4.5. If a registry client lands, the signal is a `bin/` script that talks to plugins.omarchy.org and an `omarchy plugin add publisher/name` form that takes no URL. Until then, check `omarchy plugin add --help` after any update: while it still prints `[git-url]`, nothing has changed. Behaviour has been identical across 4.0.1, 4.0.2, 4.0.3 and 4.0.4.

## Related

- [Plugins run unsandboxed](/security/plugins-run-unsandboxed/)
- [Is Omarchy safe](/security/is-omarchy-safe/)
- [Omarchy manual: Shell Plugins](https://omarchy.org/manual/shell-plugins/)
