---
title: "Omarchy forks and ports: which ones are still alive"
description: "A health check on every Omarchy fork and port, from omarchy-mac and Nixarchy to omadora, okimarchy and the CachyOS scripts: who rebased onto Quattro 4.x."
answer: "Most Omarchy forks stopped at 3.x. As of 4.0.4, only three community trees track Quattro: omarchy-mac (now in the omacom org), Nixarchy for NixOS, and malik-na's Omadora for Fedora Asahi. omarchy-nix, okimarchy, armarchy, deckarchy, omarchy-titus and both CachyOS projects were last touched before Quattro shipped. Check the last commit date before you install any of them."
other: "Forks and ports"
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [forks, ports, community, quattro, cachyos, nixos]
sources:
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/omarchy/discussions/9176"
    title: "Discussion #9176: Nixarchy -- Omarchy for NixOS users"
    kind: discussion
    author: "olafkfreund"
    date: "2026-08-30"
  - url: "https://github.com/mroboff/omarchy-on-cachyos/issues/74"
    title: "Issue #74: omarchy-settings can leave a CachyOS machine unbootable (likely root cause of #54), and the installer cannot drive Omarchy v4.x"
    kind: issue
    author: "isaac30503"
    date: "2026-08-16"
  - url: "https://github.com/mroboff/omarchy-on-cachyos/pull/77"
    title: "PR #77: feat: add v3/v4 support, boot guards, and filtered version picker"
    kind: pr
    author: "marlo4220mc"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy-mac"
    title: "omacom/omarchy-mac: Opinionated Arch/Hyprland Setup for Apple Silicon Macs M1/M2"
    kind: other
  - url: "https://github.com/olafkfreund/nixarchy"
    title: "olafkfreund/nixarchy: Omarchy 4.x vendored for NixOS"
    kind: other
  - url: "https://github.com/henrysipp/omarchy-nix"
    title: "henrysipp/omarchy-nix: An opinionated NixOS config based on DHH's Omarchy"
    kind: other
  - url: "https://github.com/CyphrRiot/ArchRiot"
    title: "CyphrRiot/ArchRiot: A curated Arch Linux Experience like no other"
    kind: other
  - url: "https://github.com/aorumbayev/awesome-omarchy"
    title: "aorumbayev/awesome-omarchy: a curated list of awesome omarchy resources"
    kind: other
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "isaac30503"
    url: "https://github.com/isaac30503"
    for: "Documented that the CachyOS installer cannot drive Omarchy 4.x, plus two delayed boot failures from omarchy-settings"
  - name: "olafkfreund"
    url: "https://github.com/olafkfreund"
    for: "Nixarchy, a NixOS package that vendors the Omarchy 4.x tree instead of reimplementing it"
  - name: "malik-na"
    url: "https://github.com/malik-na"
    for: "The Apple Silicon work behind omarchy-mac and the Fedora Asahi Omadora build"
faq:
  - q: "Which Omarchy fork should I use if I want Quattro?"
    a: "On Apple Silicon, omarchy-mac. On NixOS, Nixarchy. On Fedora Asahi Remix, malik-na's Omadora. Every other Omarchy derived tree listed here either has no commits since before Omarchy 4.0.0 shipped on 2026-08-14 or, in the case of elpritchos's Omadora, still builds on the Waybar generation."
  - q: "Why did so many forks stop at 3.x?"
    a: "Omarchy 3.x could be installed by curling boot.sh with an OMARCHY_REPO override, so a fork was a patched clone. In 4.0.4 there is no boot.sh or install.sh in the repo root, the system installs from an ISO, and the desktop ships as two pacman packages. That removes the hook forks were built on."
  - q: "Is omarchy-nix still maintained?"
    a: "No. The README says the author moved to regular Arch Omarchy full time and is not actively working on the repo, and the last commit on main is from 2025-11-13. The official manual still links it."
  - q: "Can I still install Omarchy on CachyOS?"
    a: "Not with the published mroboff script on 4.x. Issue #74 reports the installer cannot drive v4, and PR #77, which adds a v4 branch and boot guards, was still open on 2026-09-16."
related: [cachyos, omakub]
draft: false
---

Omarchy is MIT licensed, so forks are legal and plentiful. The useful question is not which forks exist but which ones survived Quattro. Omarchy 4.0.0 landed on 2026-08-14 and changed the two things every fork depended on: how the system installs, and where the desktop config lives. Most community trees have not made that jump.

All figures below come from the GitHub API on 2026-09-16, with dates in UTC. Stars and last-commit dates move, so treat this as a snapshot, not a verdict.

## The health table

| Project | Base | What it changes | Stars | Last commit | On Quattro 4.x? |
| --- | --- | --- | --- | --- | --- |
| [omarchy-mac](https://github.com/omacom/omarchy-mac) | Asahi Alarm (Arch on Apple Silicon) | aarch64 packages, one-command installer alongside macOS, notch aware bar | 1770 | 2026-09-16 | Yes. Default branch `quattro`, releases up to v4.0.2-2 |
| [nixarchy](https://github.com/olafkfreund/nixarchy) | NixOS | Vendors the upstream 4.x tree as a derivation, Arch bits swapped for Nix | 62 | 2026-09-17 | Yes, built against 4.x from the start |
| [omadora](https://github.com/malik-na/omadora) (malik-na) | Fedora Asahi Remix 44, M1/M2 | Quattro desktop on Fedora Asahi, extension of omarchy-mac | 46 | 2026-09-04 | Yes. Default branch `quattro` |
| [omadora](https://github.com/elpritchos/omadora) (elpritchos) | Fedora 44 | Minimal Hyprland install using Omarchy's patterns, Fedora repos plus one COPR for Hyprland, mise and starship | 124 | 2026-08-17 | No. Config still ships waybar and wofi |
| [omarchy-nix](https://github.com/henrysipp/omarchy-nix) | NixOS | Reimplementation as a flake plus home-manager modules | 800 | 2025-11-13 | No. Author states he is not actively working on it |
| [omarchy-on-cachyos](https://github.com/mroboff/omarchy-on-cachyos) | CachyOS | Patches the Omarchy installer to run on CachyOS, keeps fish and tealdeer | 657 | 2026-06-01 | No. See issue #74 and open PR #77 |
| [omarchy-cachyos](https://github.com/lentra0/omarchy-cachyos) | CachyOS | Opinionated rework: zsh, Brave, 8 workspaces, waybar overhaul, Apple tweaks removed | 131 | 2025-10-17 | No |
| [okimarchy](https://github.com/cristian-fleischer/okimarchy) | Arch | Adds niri beside Hyprland with runtime switching and themed niri configs | 125 | 2025-11-13 | No. Only tag is v3.1.7-1 |
| [armarchy](https://github.com/nilszeilon/armarchy) | Arch on ARM, Asahi | Restores ARM and Asahi install paths on the 3.x tree | 51 | 2025-09-17 | No |
| [deckarchy](https://github.com/aorumbayev/deckarchy) | Arch on Steam Deck | Neptune kernel, audio DSP and firmware, run before Omarchy | 48 | 2025-08-19 | No. Written for a vanilla Arch install that Omarchy is layered on afterwards |
| [omarchy-titus](https://github.com/ChrisTitusTech/omarchy-titus) | Omarchy | Personal `~/.config/hypr` overlay: eight `.conf` files plus a link script | 60 | 2025-08-29 | No |
| [Fedpunk](https://github.com/hinriksnaer/fedpunk) | Fedora | YAML module engine, desktop shipped separately as hyprpunk | 11 | 2026-03-19 | No. README no longer mentions Omarchy |
| [ArchRiot](https://github.com/CyphrRiot/ArchRiot) | Arch | Independent themed Arch desktop, own versioning | 155 | 2026-06-15 | No. README declares end of active development |
| [ohmydebn](https://github.com/dougburks/ohmydebn) | Debian, Ubuntu, Mint, Kali | Cinnamon desktop with Omarchy inspired themes, not Hyprland | 140 | 2026-09-14 | n/a, different desktop |
| [omacosy](https://github.com/paulsp94/omacosy) | macOS 26 | Omarchy style tiling, bar and themes for macOS, Swift binaries | 647 | 2026-09-15 | n/a, different OS |

## Why so many stalled before Quattro

In 3.x, forking was cheap. The repo root carried `boot.sh`, and that script read an `OMARCHY_REPO` environment variable that defaulted to the upstream repo. You could install any fork with one curl line pointed at your own clone, which is exactly how okimarchy told people to install. lentra0's CachyOS fork skipped even that step and had you clone the tree and run `install.sh` directly. Patching `install/` scripts on top of a clone was the whole porting technique.

Check the v4.0.4 tree and both entry points are gone. There is no `boot.sh` and no `install.sh` in the repo root. The manual's getting started chapter now says Omarchy is installed using an ISO, and the repo's own `docs/file-layout.md` says two Arch packages are built from the tree, `omarchy` for the runtime and Quickshell desktop, and `omarchy-settings` for everything that has to exist before the user account and bootloader are created.

On top of that, Quattro replaced Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle, swaybg and polkit-gnome with a single Quickshell process, and moved Hyprland config from `~/.config/hypr/*.conf` to Lua files using the `o.bind("SUPER + K", "Label", action)` DSL. A fork whose value was a reworked Waybar layout or a patched `hyprland.conf` has nothing left to patch. See [the Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) for what that means in practice.

The CachyOS case is documented. Issue #74 on mroboff/omarchy-on-cachyos, opened by isaac30503 on 2026-08-16, reports two things. First, the installer does not work against v4 because five of the nine paths it patches, including the root `install.sh`, no longer exist. Second, installing `omarchy-settings` on CachyOS sets up boot failures that only appear at the next initramfs rebuild: the shipped mkinitcpio drop-in overwrites the whole `HOOKS` array, swapping CachyOS's `sd-encrypt` for `encrypt`, and the limine-entry-tool drop-ins take over boot entry generation. That issue was still open on 2026-09-16. PR #77 by marlo4220mc, opened 2026-09-06, adds a v4 branch and boot guards, and was also still open. If you run CachyOS, read [Omarchy vs CachyOS](/vs/cachyos/) before you try either.

## The three that made the jump

**omarchy-mac** is the healthiest of the lot and no longer really a community fork. The repository now lives in the `omacom` organisation, the same org as Omarchy itself, as a fork of `omacom/omarchy` with `quattro` as its default branch. It cuts its own releases against upstream tags, v4.0.2-2 on 2026-09-07 at the time of writing, and ships `docs/upgrade-to-quattro.md` for existing 3.x installs. The manual still describes it as a user-driven guide, so do not read the org move as a support promise. Details on the hardware side are in [Apple Silicon](/hardware/apple-silicon-asahi/).

**Nixarchy** by olafkfreund was announced in [discussion #9176](https://github.com/omacom/omarchy/discussions/9176) on 2026-08-30. It vendors the Omarchy 4.x tree and swaps Arch specific pieces for Nix equivalents, rather than reimplementing the desktop in Nix. That design is why it keeps up: a new upstream release means bumping the vendored source, not redoing the port. It is young, 62 stars and a repository created on 2026-08-25, so expect rough edges.

**Omadora** by malik-na targets Fedora Asahi Remix 44 on M1 and M2 Macs, with `quattro` as its default branch and a `QUATTRO-CHANGES.md` describing the Quickshell and Lua move. It is the Fedora sibling of omarchy-mac rather than an independent project.

## Read this before installing any of them

1. Check the last commit on the default branch, not the star count. Several of the best known projects here have hundreds of stars and no commits since 2025.
2. Check whether the project installs Omarchy or replaces it. omarchy-on-cachyos and deckarchy are helper scripts around an upstream install. okimarchy, armarchy and lentra0's fork are full clones that only receive upstream fixes if their maintainer merges them, and none has since 2025.
3. Watch for freshly pushed clones of popular scripts. There are low star copies of omarchy-on-cachyos on GitHub, including one that describes itself as an independent continuation and one whose entire commit history is README edits pointing at a zip download. Compare the commit history against the original before running anything. [How to spot a fake Omarchy site](/official/how-to-spot-a-fake-omarchy-site/) covers the same pattern for websites.
4. The official manual's [Omarchy on...](https://omarchy.org/manual/omarchy-on/) chapter still links deckarchy and omarchy-nix. Those links are real, but as of 4.0.4 neither project has been updated for Quattro, so treat them as historical.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5. Nothing published so far suggests the install mechanism reverts, so the practical filter stays the same: a port either tracks the upstream tree and rebuilds the two packages, like omarchy-mac and Nixarchy do, or it drifts. If you are moving an existing install rather than picking a port, start at [upgrading 3.x to Quattro](/upgrade/3-to-4-quattro/).

Evidence for the dormant projects is thin by nature. Most have no issue explaining the stall, no archive flag and no note in the README. Absence of commits is the only signal, which is why every row above carries a date.

## Related

- [Omarchy vs CachyOS](/vs/cachyos/)
- [Omarchy vs Omakub](/vs/omakub/)
- [Running Omarchy on a Steam Deck](/run/steam-deck/)
- [Naming your own Omarchy project](/official/naming-your-omarchy-project/)
