---
title: "Omarchy shell plugins run unsandboxed inside omarchy-shell"
description: "Omarchy 4 shell plugins are QML loaded into the long-lived omarchy-shell process with your full user rights. What 4.0.3 scoped, and how to vet a plugin."
answer: "Treat an Omarchy plugin like any program you run as your user, because that is what it is. Plugin QML loads into the long-lived omarchy-shell process and can do anything your account can. 4.0.3 narrowed the shell object third-party plugins receive, but it is not a sandbox. Read the repo, pin it to a commit, and enable only after review."
appliesTo:
  from: "4.0.0"
status: by-design
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: high
reported: "Documented by Omarchy itself in shell/README.md and the Shell Plugins manual chapter since 4.0.0 (2026-08-14)"
projectResponse: "Omarchy warns before cloning unless you pass --yes, installs plugins disabled by default, never runs plugin install hooks, and in 4.0.3 replaced the trusted shell object with a capability-scoped facade for third-party plugins."
tags: [security, plugins, quickshell, marketplace, supply-chain]
sources:
  - url: "https://omarchy.org/manual/shell-plugins/"
    title: "Omarchy Manual: Shell Plugins"
    kind: manual
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/shell/README.md"
    title: "omarchy v4.0.4: shell/README.md"
    kind: docs
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3"
    kind: release
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11638"
    title: "Issue #11638: Plugin sandboxing (4.0.3): no opt-in for embedding-style plugins to read other plugins' manifests"
    kind: issue
    author: "dbgoodm"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy-plugin-marketplace/blob/main/SECURITY.md"
    title: "omarchy-plugin-marketplace: Security Policy and Automated Security Baseline"
    kind: docs
  - url: "https://github.com/omacom/omarchy-plugin-marketplace/blob/main/VERIFICATION.md"
    title: "omarchy-plugin-marketplace: Plugin Verification"
    kind: docs
  - url: "https://plugins.omarchy.org/publish.html"
    title: "Publish a Plugin | Omarchy Plugins"
    kind: docs
  - url: "https://github.com/omacom/omarchy/issues/11375"
    title: "Issue #11375: plugins.omarchy.org shows broken 'omarchy bar plugin add' command for first-party plugins"
    kind: issue
    author: "a3qz"
    date: "2026-09-11"
credits:
  - name: "dbgoodm"
    url: "https://github.com/dbgoodm"
    for: "Documented exactly which shell object third-party plugins receive after 4.0.3"
  - name: "a3qz"
    url: "https://github.com/a3qz"
    for: "Found that marketplace pages print an install command that does not exist"
faq:
  - q: "Is there any sandbox at all around an Omarchy plugin?"
    a: "No process or filesystem sandbox. Since 4.0.3 a third-party plugin gets a narrowed QML facade instead of the full shell object, which limits what host services it can look up, but the QML engine, the process, and your user account are shared."
  - q: "Does the installer run code from the plugin repository?"
    a: "No. omarchy-plugin-add clones the repo, validates manifest.json, and flips an enabled bit over IPC. It never runs an install hook and never asks for sudo. The code runs only once the plugin is enabled and the shell loads it."
  - q: "What does a Verified badge on plugins.omarchy.org mean?"
    a: "It means an automated static check passed on one exact commit, or a maintainer accepted the reported capabilities on that commit. The marketplace states plainly that it validates listings, not plugin security, and that it is not an audit."
  - q: "Can I pin a plugin to a reviewed commit?"
    a: "Not through the omarchy commands. An installed plugin is an ordinary git checkout in ~/.config/omarchy/plugins/, so you can git checkout a specific SHA yourself, but omarchy plugin update will still offer to fast-forward you from that SHA to upstream HEAD, and does so if you confirm."
related: [is-omarchy-safe, install-commands-clone-mutable-head, development-practices-and-ai-written-code]
draft: false
---

Omarchy 4 runs the whole desktop as one long-lived Quickshell process called `omarchy-shell`. The bar, the panels, the menu, the emoji picker, the lock screen, the polkit agent and the battery watcher are all plugins inside that one process. A third-party plugin you install from GitHub is loaded the same way, into the same process.

That is the security model in one sentence. A plugin is not an app in a box. It is QML that the shell evaluates, running with every right your user account has. Omarchy says so itself, in `shell/README.md` and in the [Shell Plugins manual chapter](https://omarchy.org/manual/shell-plugins/), and `omarchy plugin add` prints a warning before it clones anything unless you pass `--yes`.

Checked against 4.0.4. The plugin system does not exist on 3.x at all, so nothing here applies to v3.8.4 or earlier.

## What the process boundary actually is

There is none worth relying on. Plugin QML shares the QML engine, the scene graph and the process memory of `omarchy-shell`. There is no seccomp filter, no bubblewrap, no separate user, no filesystem namespace. A plugin can read your SSH keys, start a process, open a socket, and keep doing it for as long as your graphical session lasts, because the shell is the session.

The manual is direct about the residual risk after the 4.0.3 hardening. In its words: "Visual plugins still share the shell's QML scene and can walk ordinary parent objects, while all plugin code runs with everything your user account can reach."

## What 4.0.3 changed, and what it did not

Up to and including 4.0.2, `shell/shell.qml` handed every plugin the same trusted root object. In 4.0.3 that changed. Third-party manifests now receive a capability-scoped facade instead, and the release notes for [v4.0.3](https://github.com/omacom/omarchy/releases/tag/v4.0.3) list "Restrict plugin access to authentication services" under Security, credited to acrogenesis, barmstrong and ryanrhughes.

Concretely, after 4.0.3 a third-party plugin gets a small object with its own plugin id, summon and hide calls, its own settings, and a service lookup scoped to itself. It does not get the plugin registry. Authentication services such as the lock screen are held outside the host's public service map and outside the reachable QML object tree, so a plugin cannot walk to them.

That is a real reduction in blast radius and it is worth being on 4.0.3 or later for. It is still not a sandbox. It narrows what the host hands you, not what the process can do.

The change was tight enough to break legitimate plugins. In [issue #11638](https://github.com/omacom/omarchy/issues/11638), dbgoodm reports that a panel plugin whose whole purpose is hosting other plugins' widgets can no longer read their manifests, and asks for a declared, auditable permission field in `manifest.json` in the spirit of browser extension permissions. That issue was still open on 2026-09-16. There is no permission declaration in the manifest schema today.

## The install path clones mutable upstream HEAD

`omarchy plugin add <git-url>` refuses a URL that names a git option or transport helper, warns you unless you passed `--yes`, clones into a staging directory, runs `omarchy-plugin-validate`, refuses a duplicate id, and moves the result into `~/.config/omarchy/plugins/<id>/`. It never executes anything from the repo, never runs an install hook and never asks for sudo.

What it does not do is pin. The clone takes whatever the default branch points at right now. `omarchy plugin update` runs `git fetch origin HEAD` and fast-forwards, showing you the diff first unless you passed `--yes`.

The marketplace maintainers say this in their own `SECURITY.md`: "The current Omarchy install and update commands obtain mutable upstream HEAD and do not accept an exact marketplace SHA." Because of that, plugin detail pages label the install command as current upstream rather than verification bound, and code you install may differ from the commit that was checked.

That matters more than it sounds. A plugin that was clean when it was listed can be force pushed, have its default branch moved, or be transferred to a new owner, and the next person to run `omarchy plugin add` gets the new code with no second look. Same pattern as [install commands that clone mutable HEAD](/security/install-commands-clone-mutable-head/) elsewhere in Omarchy.

## What the marketplace checks

[plugins.omarchy.org](https://plugins.omarchy.org) is the community registry. Its publishing guide states that the marketplace validates listings, not plugin security, and that plugins run unsandboxed with the author responsible for the code.

Behind the badge there is more machinery than that sentence suggests. An Automated Security Baseline does a static, commit-bound scan without executing plugin code. It produces one of three outcomes: `passed`, `review-required` when it sees capabilities such as an installer, a package manager, `sudo` or `pkexec` use, a bundled executable binary or sudoers changes, and `needs-fixes` when it matches a documented finding such as `curl-pipe-shell` or `cargo-git-unpinned`.

Verification statuses on the site are snapshot statuses, not statements about the plugin:

- **Snapshot verified**: the listed commit has eligible evidence and no newer upstream commit was seen.
- **Update unverified**: upstream has moved past the verified commit, so the code you would install is not covered.
- **Unverified**: no current record for the listed snapshot. The marketplace is explicit that this does not mean the plugin is malicious.

The published registry on 2026-09-16 held 3363 plugin sources. Of the 3317 carrying a baseline result, 1891 passed, 1402 were review-required, and 24 landed on `needs-fixes`. All 24 of those are still listed, because the baseline runs in `selective` enforcement mode where remote-execution findings add a review label rather than blocking publication. In the live catalog of 3401 entries, 2355 showed as effectively verified and 1010 as unverified, of which 793 were verified snapshots that upstream has since moved past.

So the badge is a real, deterministic, exact-commit check. It is also, in the project's own words, not an audit, a certification, an endorsement, or a guarantee, and it does not cover the code `omarchy plugin add` will actually fetch.

## How to evaluate a plugin before you install it

1. Read the repo on GitHub first. Look at the QML entry points named in `manifest.json`, plus anything named install, setup or uninstall.
2. Check the author and the commit history. A one-commit repo from an account created last week is a different proposition to a plugin with months of history.
3. Search for the shape of the problems the baseline looks for: a `curl ... | sh`, an unpinned `cargo install --git`, a `NOPASSWD` sudoers drop-in, anything reading a PID from `/tmp` and passing it to a privilege wrapper.
4. Add it without enabling it. Leave off `--enable`, answer no at the prompt, then read the code that landed in `~/.config/omarchy/plugins/<id>/`.
5. Pin it yourself if you care. It is a plain git checkout, so `git -C ~/.config/omarchy/plugins/<id> checkout <sha>` works. Be aware that this is not a lock: `omarchy plugin update` runs `git merge --ff-only`, which fast-forwards cleanly from an older commit, so the next update will show you the diff from your pinned SHA and move you to upstream HEAD if you say yes. The pin only holds as long as you keep saying no.
6. Enable it only after that, with `omarchy plugin enable <id>`.
7. On update, read the diff `omarchy plugin update` shows you. Do not pass `--yes` to a plugin update you have not read.

Removal is `omarchy plugin remove <id>`, which disables first and then deletes the checkout.

## What to watch for on newer versions

The scoped facade arrived in 4.0.3 and is unchanged in 4.0.4. The open request in issue #11638 is for a declared capability field in `manifest.json`, which would be the first thing resembling a permission model. If that lands in a future release, expect the trade to be more capability for more visible, auditable declarations, not a real sandbox.

Watch also for exact-SHA support in `omarchy plugin add`. The marketplace has said commit-bound installation cannot be guaranteed without it. Until it exists, the badge and the code you install are two different things.

One smaller thing to know: issue #11375 reports that plugin pages on the marketplace print `omarchy bar plugin add <id>` for first-party plugins, which is not a real command. The correct one is `omarchy plugin enable <id>`. It was still open on 2026-09-16.

## Related

- [Is Omarchy safe to use](/security/is-omarchy-safe/)
- [Install commands clone mutable HEAD](/security/install-commands-clone-mutable-head/)
- [Development practices and AI written code](/security/development-practices-and-ai-written-code/)
