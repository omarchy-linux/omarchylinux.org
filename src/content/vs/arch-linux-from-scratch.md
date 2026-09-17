---
title: "Omarchy vs building Arch + Hyprland yourself"
description: "What Omarchy 4.0.4 adds on top of a hand-built Arch and Hyprland desktop, what control you give up, and which of the two you should actually install."
answer: "Omarchy is a pre-decided Arch and Hyprland desktop: an ISO that sets up LUKS, Btrfs, Limine and Snapper, 147 base packages, a Quickshell shell, its own linux-omarchy kernel since 4.0.4, 444 omarchy CLI commands, versioned migrations and 34 hardware quirk scripts. You give up package freshness on the stable mirror, direct pacman upgrades and per-choice control. Build Arch yourself if those matter more than the setup time."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
other: "Arch Linux"
otherVersion: "rolling, checked 2026-09-16"
tags: [comparison, arch, hyprland, packaging, channels]
sources:
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-cli/"
    title: "Omarchy manual: Omarchy CLI"
    kind: manual
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0: The Quattro Release"
    kind: release
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9064"
    title: "Issue #9064: stable-mirror.omarchy.org Arch repo databases stale (~5 days behind)"
    kind: issue
    author: "a-lang"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10732"
    title: "Issue #10732: Stable mirror frozen since Aug 25 keeps default Chromium on 151 while 152.0.7977.82 fixes an in-the-wild exploit (CVE-2026-85046)"
    kind: issue
    author: "JohnAtl"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations (surfaced as: LUKS prompt still QWERTY after e891e5c)"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/discussions/8347"
    title: "Discussion #8347: How can I update Omarchy without updating optional AUR applications"
    kind: discussion
    author: "ammarove"
    date: "2026-08-26"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: other
    author: "dhh"
faq:
  - q: "Is Omarchy still Arch underneath?"
    a: "Yes. It is Arch with pacman, the Arch repos and the AUR, installed from its own ISO. The difference is that Omarchy ships its own mirrors, its own package repository for the Omarchy components, and a defined update path on top."
  - q: "Can I run pacman -Syu on Omarchy like on Arch?"
    a: "Not by default. A pacman hook calls omarchy-update-pacman-guard, which aborts a direct sync-and-upgrade and points you at omarchy update. The message tells you to rerun with sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu if you really mean it."
  - q: "Will I learn less about Linux by starting with Omarchy?"
    a: "You skip the partitioning, bootloader and Hyprland assembly work, which is where a lot of the learning happens. You still meet pacman, systemd, Btrfs and Hyprland config the first time something breaks, because Omarchy does not hide any of them."
  - q: "How current are packages on Omarchy compared to plain Arch?"
    a: "On the stable channel they lag deliberately. Checked on 2026-09-16, stable-mirror.omarchy.org had last synced on 2026-09-07, about nine days behind the Arch geo mirror. The edge channel mirror was under an hour behind."
related: [cachyos, omakub, forks-and-ports]
draft: false
---

If you can already partition a disk, set up LUKS on Btrfs, install a bootloader and write a Hyprland config, you can build everything Omarchy gives you. The question is not capability, it is whether you want to own the decisions. Omarchy is a fixed set of answers, shipped as an ISO and kept in sync by a package repository and a migration runner. Plain Arch is no answers and no maintenance contract.

This page compares Omarchy 4.0.4, released 2026-09-15, against a hand-built Arch plus Hyprland desktop. Where 3.x behaved differently, it says so.

## What Omarchy actually adds

These are things you would otherwise build or maintain yourself. All of them are in the repo at tag v4.0.4.

**An installer that makes the storage decisions.** The ISO does a full-disk or free-space install, and full-disk encryption with LUKS is the default rather than an option you remember to pick. You can drop encryption by pressing `Ctrl + C` at the disk formatting confirmation, and you can defer the whole personal setup to first boot so someone else becomes the owner. See the manual's [Getting Started](https://omarchy.org/manual/getting-started/) chapter.

**Limine plus Snapper wired together.** Limine has been the default bootloader since Omarchy 2.0. `install/config/snapper.sh` writes a Snapper root config from the shipped template, disables the timeline timer and enables `snapper-cleanup.timer` and `limine-snapper-sync.service`, so snapshots appear as boot entries. `omarchy update` takes a snapshot before touching packages. On plain Arch this is several hours of reading and a fragile hook you own forever.

**A curated package base.** `install/omarchy-base.packages` lists 147 packages that the ISO pacstraps, and the ISO builder reads the same file to build its offline mirror. A second list of 57 covers optional and build-time packages.

**One shell instead of eight components.** Omarchy 4.0.0 "Quattro", released 2026-08-14, replaced Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle, swaybg and polkit-gnome with a single Quickshell process that owns the bar, launcher, menus, notifications, on-screen displays, control panels, lock screen and polkit agent. On plain Arch you assemble those yourself and you own the themes for each one.

**Themes as a system.** v4.0.4 ships 22 themes under `themes/`, up from 19 in v3.8.4, and `omarchy-theme-set` retints the terminal, the shell, the browser and the background together.

**Its own kernel.** Since 4.0.4, released 2026-09-15, Omarchy installs `linux-omarchy` from its own package repository and migration `1789325478` puts it first in Limine's `BOOT_ORDER`, keeping the Arch kernel installed as a fallback. T2 Macs keep `linux-t2`. On plain Arch you run `linux`, `linux-lts` or `linux-zen` from the Arch repos, and patching your own kernel is on you.

**The `omarchy` CLI.** v4.0.4 carries 444 commands in `bin/`, grouped into namespaces such as `audio`, `channel`, `hw`, `snapshot` and `theme`. 74 are hidden internals. v3.8.4 had 283. Run `omarchy` with no arguments for the index, documented in the [Omarchy CLI](https://omarchy.org/manual/omarchy-cli/) chapter. Our [command reference](/reference/commands/) tracks the list per release.

**Migrations.** The 4.x series has shipped 106 migration scripts so far. `omarchy update` runs pending ones after the package transaction, so config format changes land without you reading a changelog. Arch gives you the Arch news page and a manual intervention section instead.

**Hardware quirk scripts.** `install/hardware/all.sh` runs 34 scripts: NVIDIA driver selection that picks between `nvidia-open-dkms` and the 580xx branch, Intel video acceleration, thermald, lpmd and an IPU7 camera fix, ASUS ROG and Z13 touchpad fixes, Framework 16 and QMK HID, Apple T2, SPI keyboard and suspend NVMe fixes, Lenovo Yoga speaker tuning, Broadcom and Surface keyboard workarounds. Each one is a thread you would otherwise find yourself.

**Channels and mirrors.** Omarchy runs its own Arch mirrors and its own package repository. `omarchy-channel-set` switches between stable, rc, edge and dev, rewriting `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist` from the shipped defaults. Since 4.0.0 Omarchy itself installs as pacman packages under `/usr/share/omarchy`, where 3.x kept a git checkout in `~/.local/share/omarchy`.

**Firewall and sane defaults.** `install/config/firewall.sh` sets ufw to deny incoming and allow outgoing, opens 53317 for LocalSend and installs the ufw-docker rules.

## What you give up

**Package freshness on stable.** The [Updates](https://omarchy.org/manual/updates/) chapter says the stable mirror deliberately runs behind so incompatibilities get caught before they reach users. That lag is real and it is not always the documented amount. Checked on 2026-09-16 (00:49 UTC on the 17th), `stable-mirror.omarchy.org` had last synced on 2026-09-07, roughly nine days behind `geo.mirror.pkgbuild.com`, while `mirror.omarchy.org`, which the edge mirrorlist points at, was under an hour behind. Open issue [#9064](https://github.com/omacom/omarchy/issues/9064) reports the stable databases sitting five days stale and pacman silently accepting them. Open issue [#10732](https://github.com/omacom/omarchy/issues/10732) makes the sharper point: with the mirror still frozen at its 2026-08-25 sync when the issue was filed, stable installs stayed on Chromium 151 after Arch published 152, which carried a fix for a vulnerability Google said was being exploited in the wild. On plain Arch you would have had it the day it landed. More on this in [stable mirror lag and CVEs](/security/stable-mirror-lag-and-cves/).

**Arch news timing.** Arch expects you to read the news before upgrading and to perform manual interventions yourself. Omarchy's model is that migrations and the mirror delay handle this for you. That is genuinely less work, and it also means you are not the first to know when upstream changes something.

**Direct pacman upgrades.** A pacman hook calls `omarchy-update-pacman-guard`, which aborts a direct `-Syu` and tells you to use `omarchy update`. The bypass is `sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu`, and using it skips the snapshot, the migrations and the post-update hooks. Partial upgrade freedom is also coarse: discussion [#8347](https://github.com/omacom/omarchy/discussions/8347) asks for a way to update the system without pulling in every optional AUR app. There is no built-in switch; the answer offered in the thread is pacman's own `IgnorePkg`.

**Configuration you did not choose.** `omarchy-refresh-pacman` copies over `/etc/pacman.conf` and the mirrorlist, keeping `.bak` copies. The `omarchy refresh` family does the same for other shipped configs, and `omarchy-refresh-config` backs up your copy before overwriting it. On a hand-built Arch, nothing rewrites your config unless you tell it to.

**Layered state you have to understand anyway.** Rollback is not a clean undo. Snapshots restore the root filesystem but not `/home`, so your `~/.config` stays on the newer format. Open issue [#9828](https://github.com/omacom/omarchy/issues/9828) documents the other half: migration markers live under `$HOME/.local/state/omarchy/migrations/`, so a Snapper rollback reverts the system while the markers claim the migrations already ran. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

**Config format churn.** 4.0.0 moved Hyprland config from `~/.config/hypr/*.conf` to Lua files with an `o.bind("SUPER + K", "Label", action)` DSL. If you already had a tuned Hyprland config, that was a rewrite. See [hyprland.conf to Lua](/reference/hyprland-conf-to-lua-migration/) and [upgrading 3 to 4](/upgrade/3-to-4-quattro/).

## Who should pick which

Pick **Omarchy** if you want a working Hyprland desktop this afternoon, if encrypted disks with bootable snapshots matter more to you than choosing the bootloader, if your hardware is on the quirk-script list, or if you are happy to be a week or two behind Arch in exchange for a tested upgrade path. It also suits a second machine where you do not want to maintain a second set of dotfiles.

Pick **plain Arch plus Hyprland** if you need packages the day they ship, if you run security-sensitive work where browser fixes cannot wait on a mirror sync, if you already have dotfiles you like, if you want a different bootloader, filesystem or shell, or if the point of the exercise is learning how the parts fit. Also pick it if you dislike software that guards your package manager.

A middle path exists: install Omarchy and run `omarchy-channel-set edge`, which puts you on the fast mirror and the development packages. The manual is blunt that this is for people who can recover a broken system.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5 rather than 4.1, with DHH citing the bespoke optimized kernel build as part of the reason. That kernel already reached existing installs in 4.0.4, so the kernel is now an Omarchy package rather than an Arch one. How quickly kernel fixes flow through that channel is a different question from the mirror lag above, and this page has not measured it.

Watch the mirror behaviour too. Both mirror issues cited here were open as of 2026-09-16, and the gap between the manual's description of stable and what the mirror actually does is the single most load-bearing difference in this comparison.

## Related

- [Omarchy vs CachyOS](/vs/cachyos/)
- [Omarchy vs Omakub](/vs/omakub/)
- [Forks and ports](/vs/forks-and-ports/)
- [Is Omarchy safe](/security/is-omarchy-safe/)
