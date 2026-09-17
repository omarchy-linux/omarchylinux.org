---
title: "Omarchy vs CachyOS: which one, and can you run both?"
description: "Omarchy 4.0.4 and CachyOS compared on install, kernel, desktop, gaming, updates and support, plus why the Omarchy on CachyOS scripts are stuck on 3.x."
answer: "Pick Omarchy if you want one finished Hyprland desktop and are happy to accept its opinions. Pick CachyOS if you want a performance-tuned Arch base and your own choice of desktop from 17 or more. Since 4.0.4 Omarchy ships its own tuned kernel, so the kernel gap is much smaller than it was. Do not try to install Omarchy 4.x on top of CachyOS today, the community scripts only drive 3.x."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
other: "CachyOS"
otherVersion: "August 2026 ISO"
tags: [cachyos, comparison, kernel, gaming, arch, install]
sources:
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
  - url: "https://omarchy.org/manual/gaming/"
    title: "Omarchy manual: Gaming"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Omarchy v4.0.4 release notes"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/discussions/650"
    title: "Discussion #650: Guide: Install Omarchy using CachyOS base install"
    kind: discussion
    author: "inffy"
    date: "2025-08-11"
  - url: "https://github.com/omacom/omarchy/discussions/1247"
    title: "Discussion #1247: Thoughts After a Line-By-Line Install of Omarchy (on CachyOS)"
    kind: discussion
    author: "mroboff"
    date: "2025-08-28"
  - url: "https://github.com/omacom/omarchy/discussions/3515"
    title: "Discussion #3515: Change base kernel to CachyOS kernel"
    kind: discussion
    author: "ethanannane"
    date: "2025-11-22"
  - url: "https://github.com/omacom/omarchy/issues/6876"
    title: "Issue #6876: omarchy_hooks.conf replaces HOOKS instead of extending it, dropping lvm2/resume and leaving LVM-on-LUKS roots unbootable"
    kind: issue
    author: "alancaldas84"
    date: "2026-08-14"
  - url: "https://github.com/mroboff/omarchy-on-cachyos"
    title: "mroboff/omarchy-on-cachyos: Installation script for DHH's Omarchy on top of CachyOS"
    kind: other
    author: "mroboff"
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
  - url: "https://cachyos.org/"
    title: "CachyOS: Performance-First Linux, Built on Arch"
    kind: docs
  - url: "https://cachyos.org/blog/2608-august-release/"
    title: "CachyOS August 2026 Release"
    kind: blog
    date: "2026-08-09"
  - url: "https://wiki.cachyos.org/features/kernel/"
    title: "CachyOS Wiki: CachyOS Kernel"
    kind: docs
  - url: "https://wiki.cachyos.org/features/kernel_manager/"
    title: "CachyOS Wiki: Kernel Manager"
    kind: docs
  - url: "https://wiki.cachyos.org/features/optimized_repos/"
    title: "CachyOS Wiki: Optimized Repositories"
    kind: docs
  - url: "https://wiki.cachyos.org/configuration/gaming/"
    title: "CachyOS Wiki: Gaming"
    kind: docs
  - url: "https://packages.cachyos.org/package/cachyos/x86_64/linux-cachyos"
    title: "CachyOS package: linux-cachyos"
    kind: docs
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "inffy"
    url: "https://github.com/inffy"
    for: "Wrote the original CachyOS base install guide and found the tealdeer versus tldr conflict"
  - name: "mroboff"
    url: "https://github.com/mroboff"
    for: "Published the line-by-line writeup and the omarchy-on-cachyos installer"
  - name: "isaac30503"
    url: "https://github.com/isaac30503"
    for: "Traced the mkinitcpio HOOKS takeover that breaks LUKS unlock on CachyOS, and audited which installer paths no longer exist in 4.x"
  - name: "marlo4220mc"
    url: "https://github.com/marlo4220mc"
    for: "Opened the pull request adding 4.x support and boot guards to omarchy-on-cachyos"
faq:
  - q: "Is CachyOS faster than Omarchy?"
    a: "On package builds, probably a little. CachyOS recompiles Arch packages for x86-64-v3, x86-64-v4 and znver4 with LTO, which Omarchy does not do. On the kernel the gap has closed, since Omarchy 4.0.4 ships linux-omarchy and both projects were on upstream 7.2.5 in mid September 2026."
  - q: "Can I just install the CachyOS kernel on Omarchy?"
    a: "Nobody upstream supports it, and adding the CachyOS repositories puts a second package source ahead of Omarchy's pinned mirror, which is a partial upgrade risk. Omarchy already offers linux-omarchy-bore if you want a BORE scheduler build. A request to adopt the CachyOS kernel is open as discussion #3515 with no maintainer commitment."
  - q: "Does the omarchy-on-cachyos script work with Omarchy 4?"
    a: "Not as of 2026-09-16. Its last commit is from 2026-06-01 and issue #74 documents that Omarchy 4 removed the root install.sh the script calls. Pull request #77 adds 4.x support but is still open."
  - q: "Which one is better for gaming?"
    a: "CachyOS, if gaming is the reason you are choosing. It ships proton-cachyos, cachyos-gaming-meta, gamescope-session-cachyos and a deckify kernel for handhelds. Omarchy ships Steam, Lutris, Heroic, Battle.net under GE-Proton and Moonlight, which covers most people but is not tuned for handhelds."
related: [arch-linux-from-scratch, forks-and-ports]
draft: false
---

## The short decision

Checked against Omarchy 4.0.4 (released 2026-09-15) and the CachyOS August 2026 ISO.

- **Choose Omarchy** if you want a finished Hyprland desktop that someone else already decided for you, with themes, keybindings, a menu and an update path that ships as one unit. You accept the opinions in exchange for not configuring anything.
- **Choose CachyOS** if you want a fast Arch base and you want to pick your own desktop. It offers 17 or more desktops and window managers, a graphical Calamares installer and a CLI installer, and recompiled packages for your CPU.
- **Choose CachyOS** if gaming is the main reason you are switching, especially on a handheld.
- **Do not try to put Omarchy 4.x on top of CachyOS right now.** The community tooling for that only understands Omarchy 3.x, and the failure mode is an unbootable machine, not an error message. Details below.

## Philosophy

CachyOS calls itself "Performance-First Linux, Built on Arch". Its product is the base: kernel patches, repositories rebuilt with x86-64-v3, x86-64-v4 and znver4 instruction sets plus LTO, and a mirror and installer around that. The desktop is your choice, and the list is long.

Omarchy's product is the desktop. There is exactly one: Hyprland, with a Quickshell based shell that since 4.0.0 replaced Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle, swaybg and polkit-gnome. Configuration moved from `~/.config/hypr/*.conf` to Lua files with a small binding DSL, so a keybinding now looks like `o.bind("SUPER + RETURN", "Terminal", { omarchy = "terminal" })`. If you want KDE, you are in the wrong distro. See [the hyprland.conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) for what that change costs you.

Both are Arch underneath. Neither is a fork.

## Install

CachyOS gives you choices at install time: bootloader, filesystem, encryption, desktop, extra package groups. That flexibility is why it works as a base for other setups.

Omarchy's ISO makes those choices for you: Btrfs with Snapper snapshots, LUKS encryption unless you opt out, Limine, SDDM. It is fewer screens and fewer ways to get it wrong. The only real choice is full disk, which wipes the drive, or a free-space install into unallocated space, which is how Quattro added dual boot. If you need to keep another operating system, read [should you dual boot](/switch/should-you-dual-boot/) first.

## Kernel

This is the comparison that changed most recently, so old articles get it wrong.

Through 4.0.3, a normal Omarchy install booted Arch's own `linux` package, with `linux-ptl` and `linux-t2` only for Panther Lake and T2 Mac hardware, and CachyOS's tuned kernel was a real reason to prefer CachyOS. Release 4.0.4 on 2026-09-15 shipped `linux-omarchy` to everyone and made it the first Limine boot entry. The release notes describe it as tuned to keep the desktop responsive under load, with gaming compatibility fixes and AMD HDMI improvements.

As of 2026-09-16 the stable Omarchy channel carried `linux-omarchy` 7.2.5-3, plus `linux-omarchy-bore` and `linux-omarchy-muqss` variants, and `linux-ptl` for Panther Lake hardware. CachyOS's `linux-cachyos` was 7.2.5-1, built the same day. Same upstream kernel, different patch sets.

CachyOS still has more variants, including `linux-cachyos-lts`, `linux-cachyos-hardened`, `linux-cachyos-rt-bore` and `linux-cachyos-deckify` for handhelds, and its kernel manager for switching between them and loading sched-ext schedulers. But the headline claim that Omarchy runs a plain kernel while CachyOS runs a tuned one is no longer true.

Wanting the CachyOS kernel on Omarchy is a request upstream has had since discussion #3515 in November 2025. It is open with no maintainer commitment.

## Gaming

Omarchy's gaming story is a menu of installers under _Install > Gaming_: Steam, RetroArch preconfigured with CRT Royale, Battle.net under GE-Proton, Lutris, Heroic, Moonlight, Xbox Cloud Gaming, GeForce NOW and Minecraft. The Battle.net launcher has a `--with-mangohud` flag for an FPS overlay. That covers a normal desktop gamer.

CachyOS goes deeper on the plumbing: `proton-cachyos` with Wine staging patches and FSR, `cachyos-gaming-meta` and `cachyos-gaming-applications`, `gamescope-session-cachyos`, and a `game-performance` wrapper that switches the power profile to performance for the duration of a game.

If you are choosing a distro because of games, CachyOS is the better fit. If you want a good desktop that also plays games, Omarchy is fine.

## Updates and channels

Omarchy updates as one unit through _Update > Omarchy_. It takes a snapshot, installs the release, runs pending migrations and updates packages. Direct `pacman -Syu` is blocked by a guard that points you back to `omarchy update`, because a bare pacman upgrade skips the snapshot and the migrations.

There are four channels: stable, RC, edge and dev. Stable pins `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist` to Omarchy's own Arch mirror, which the manual describes as running about one month behind upstream so incompatibilities get caught first. That deliberate lag has a security cost worth understanding before you pick Omarchy, see [stable mirror lag and CVEs](/security/stable-mirror-lag-and-cves/).

CachyOS is a normal rolling Arch system with its own repositories layered ahead of Arch's. You update with pacman or its own tools, and nothing stops you.

Those two update models are the deep reason the hybrid is awkward. Omarchy wants to own your mirrorlist. CachyOS needs its own.

## Support

Omarchy has an active Discord and a very busy GitHub tracker, and the project ships fast, which means fixes arrive quickly and so do regressions. CachyOS has a forum, a wiki that is genuinely good, and a slower cadence of ISO snapshots, the August 2026 ISO being its fifth of the year.

Neither supports the other. The official Omarchy manual chapter [Omarchy on...](https://omarchy.org/manual/omarchy-on/) lists Asahi, Parallels, VirtualBox, VMware, Steam Deck and NixOS. CachyOS is not on that list.

## Omarchy on CachyOS

Two community efforts exist, and both are behind.

**Discussion #650** by inffy, from August 2025, walks through a CachyOS base install with no desktop, unticking the CachyOS shell configuration box to avoid a `tealdeer` versus `tldr` conflict, then running the Omarchy installer. It has 18 upvotes and 11 comments. It ends with `wget -qO- https://omarchy.org/install | bash`. On 2026-09-16 that URL still returns a one line script that evaluates `boot.sh` from the repository's master branch, and that file returns 404. It is also absent from the 4.0.4 source tree, though it is present in 3.8.4. So the last step of the guide no longer does anything.

**mroboff/omarchy-on-cachyos** is the maintained script, 657 stars, MIT licensed. Its README says it supports Omarchy 3.0 and later. Its last commit is from 2026-06-01, which is before Omarchy 4.0.0 shipped on 2026-08-14. There are 22 open issues and 10 open pull requests.

Issue #74, filed by isaac30503 in August 2026 and still open, is the one to read before you try anything. Two findings:

1. Installing `omarchy-settings` writes `/etc/mkinitcpio.conf.d/omarchy_hooks.conf`, which reassigns the whole `HOOKS` array rather than extending it. On CachyOS that swaps the systemd based `sd-encrypt` hook for the legacy `encrypt` hook and drops `sd-btrfs-overlayfs`. The machine keeps booting until the next initramfs rebuild, which could be a kernel update days later, and then cannot unlock an encrypted root. The reporter says it cost them an install. This is not CachyOS specific: upstream issue #6876 documents the same reassignment dropping `lvm2` and `resume` on a plain Omarchy machine with LVM on LUKS.
2. Omarchy 4 removed the root `install.sh` the script calls, and moved several hardware scripts. The reporter's path audit found 9 of 9 expected paths present in 3.8.4 and 4 of 9 in 4.0.0. Because the script does not use `set -e`, it still prints a success summary.

Pull request #77 by marlo4220mc, opened 2026-09-06, adds 4.x support, boot guards and a version picker that filters pre-release tags. It was still open on 2026-09-16.

There is one more structural problem. Omarchy's `install/post-install/pacman.sh` copies its own `pacman.conf` and mirrorlist over whatever is there. Omarchy's stable `pacman.conf` defines only core, extra, multilib and the omarchy repository, so on CachyOS the overwrite removes the CachyOS repository sections entirely and points core, extra and multilib at Omarchy's lagging mirror. Every package that came from a CachyOS repository is then stranded, which is a partial upgrade hazard.

If you want both, the honest options today are: run CachyOS and copy the Omarchy themes and Hyprland ideas you like by hand, or run Omarchy and use `linux-omarchy-bore` rather than chasing the CachyOS kernel.

## What to watch for on newer versions

- The next release is announced as Quattro RS 4.5. If the kernel work in 4.0.4 continues, the performance argument for CachyOS narrows further.
- Watch pull request #77 on omarchy-on-cachyos. If it merges and gets real testing, "Omarchy on CachyOS" becomes viable again for 4.x.
- Watch upstream issue #6876. A fix that makes `omarchy_hooks.conf` extend rather than replace `HOOKS` would remove the single most dangerous part of the hybrid setup, on CachyOS and on LVM machines alike.
- Anything written before 2026-08-14 describes Omarchy 3.x, with Waybar, Walker and `hyprland.conf`. Treat comparison articles from that era as history. See [still true guides and videos](/reference/still-true-guides-and-videos/).
