---
title: "Omarchy on Apple Silicon: UTM, Try Omarchy, omarchy-mac"
description: "There is no official Apple Silicon build of Omarchy 4. The three working routes in 2026: Try Omarchy, omarchy-mac on Asahi, and a native aarch64 UTM VM."
answer: "Omarchy ships no aarch64 ISO. On any Apple Silicon Mac, the easiest route is the Try Omarchy app, which runs an ARM64 Omarchy Quattro guest under Hypervisor.framework. On an M1 or M2 you can instead install on bare metal with omarchy-mac on top of Asahi Alarm. On M3 or M4, build a native aarch64 UTM VM. All three are community work."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Apple Silicon (UTM, try-omarchy, omarchy-mac)"
hostVersion: "macOS 15 or newer"
tags: [apple-silicon, aarch64, utm, asahi, vm, macos]
sources:
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/omarchy/discussions/7960"
    title: "Discussion #7960: FR: Support aarch64"
    kind: discussion
    author: "stephenmw"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/discussions/7956"
    title: "Discussion #7956: Omarchy 4 (quattro) on Apple Silicon: a one-script build for a native aarch64 UTM VM"
    kind: discussion
    author: "ggalancs"
    date: "2026-08-23"
  - url: "https://github.com/omacom/try-omarchy"
    title: "omacom/try-omarchy: Run Omarchy on MacOS without any setup"
    kind: docs
  - url: "https://github.com/omacom/omarchy-mac"
    title: "omacom/omarchy-mac: Opinionated Arch/Hyprland Setup for Apple Silicon Macs M1/M2"
    kind: docs
  - url: "https://github.com/ggalancs/omarchy-arm-utm"
    title: "ggalancs/omarchy-arm-utm: Omarchy 4 (quattro) on Arch Linux ARM, a native aarch64 UTM VM"
    kind: docs
    author: "ggalancs"
  - url: "https://github.com/omacom/omarchy-pkgs/commit/4ed5f14629"
    title: "omarchy-pkgs commit 4ed5f14: Build the omarchy package pair for aarch64"
    kind: commit
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8645"
    title: "Issue #8645: Install menu offers x86_64-only packages on aarch64: every entry fails with `target not found` in a floating terminal that closes"
    kind: issue
    author: "alexandru-savinov"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11591"
    title: "Issue #11591: aarch64: menu offers impossible installs (Spotify, Dropbox) and the floating terminal reports \"Done!\" on failure"
    kind: issue
    author: "Fromzy1"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/10048"
    title: "Issue #10048: \"Kernel has been updated. Reboot?\" on every update on Arch ARM (linux-aarch64)"
    kind: issue
    author: "ericmoret"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/8125"
    title: "Issue #8125: Brightness slider/keys silently no-op on Apple Silicon: wrong backlight device picked (228600000.dsi.0 instead of apple-panel-bl)"
    kind: issue
    author: "CuraMagis"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/plans/aarch64-support.md"
    title: "omacom/omarchy-iso: plans/aarch64-support.md (generic UEFI ARM64 build plan)"
    kind: docs
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
    date: "2026-09-08"
credits:
  - name: "ggalancs"
    url: "https://github.com/ggalancs"
    for: "Establishing that Quattro has no architecture guard and that the blocker is the missing aarch64 package repository, plus the one-script UTM build"
  - name: "ericmoret"
    url: "https://github.com/ericmoret"
    for: "Tracing the repeated reboot prompt to the vmlinuz lookup in omarchy-update-restart"
faq:
  - q: "Is there an official Omarchy ISO for Apple Silicon?"
    a: "No. As of v4.0.4 the only ISO Omarchy publishes is x86_64. The aarch64 feature request, discussion #7960, is still open with no maintainer answer, and the plan document in the ISO repository targets generic UEFI ARM64 servers and laptops while putting Apple Silicon and Asahi out of scope."
  - q: "Can I just run the normal Omarchy installer in UTM on an M-series Mac?"
    a: "Not as-is. Omarchy 4 has no uname check that blocks you, but the installer repoints pacman at Omarchy's own mirrors, and those serve core/os/x86_64 only. The first sync fails because there is nothing to install from."
  - q: "Which option gives real GPU acceleration?"
    a: "omarchy-mac on bare metal gives you the actual Apple GPU through Asahi, but it only covers M1 and M2. Try Omarchy renders through VirGL and ANGLE onto Metal, so the guest gets real GPU acceleration, although its README says video decoding is still CPU-only. The ggalancs UTM image ships with software rendering forced on because GPU clients never paint under UTM 4.7; its README says that bug is gone under UTM 5.0.x, where `omarchy-arm-gpu --on` switches the GPU on."
  - q: "Will my x86-only apps work?"
    a: "No. On aarch64 the Omarchy install menu still offers packages that only exist for x86_64, so entries like Spotify or Dropbox fail. Issues #8645 and #11591 track this."
related: [parallels, virtualbox, what-breaks-in-a-vm]
draft: false
---

Omarchy 4.0.4 has no Apple Silicon build. The manual is direct about it: the [Mac support chapter](https://omarchy.org/manual/mac-support/) covers Intel Macs and says installing on an M-series Mac is not directly supported, and the [Omarchy on... chapter](https://omarchy.org/manual/omarchy-on/) points M1 and M2 owners at Asahi Alarm plus a user-driven guide. The feature request for official aarch64 support, [discussion #7960](https://github.com/omacom/omarchy/discussions/7960), was opened on 2026-08-23 and still has no maintainer answer.

So everything below is community work. Pick the route that matches your chip and how much you want to risk.

## Pick your route

**Any Apple Silicon Mac, least effort: Try Omarchy.** [omacom/try-omarchy](https://github.com/omacom/try-omarchy) is a signed and notarized macOS app. Inside it are three things: a prebuilt ARM64 Arch Linux ARM disk image with Omarchy Quattro already set up, a QEMU build that runs on Apple's Hypervisor.framework, and a small native launcher. Download the DMG from its releases page, drag it to Applications, launch it. The README asks for macOS 15 or newer, an APFS volume, roughly 7 GB free to create the VM and up to 30 GB as it fills. Latest release at the time of writing is v0.4.1, published 2026-09-15.

**M1 or M2, and you want the metal: omarchy-mac.** [omacom/omarchy-mac](https://github.com/omacom/omarchy-mac) installs Omarchy 4 alongside macOS on top of [Asahi Alarm](https://asahi-alarm.org/), with full-disk encryption, in roughly one command. This is the only route that gives you the real Apple GPU. Asahi's installer covers M1 and M2 only, so M3 and M4 owners cannot use it.

**M3, M4, or you want a plain UTM VM: build a native aarch64 guest.** [ggalancs/omarchy-arm-utm](https://github.com/ggalancs/omarchy-arm-utm), announced in [discussion #7956](https://github.com/omacom/omarchy/discussions/7956), is a single script that builds Arch Linux ARM plus the Omarchy 4 tree into a UTM bundle without you touching UTM's own interface. The author reports one full timed run of about 57 minutes on an M3 Max, and publishes a prebuilt image on the Internet Archive for people who do not want to build. Note that the image ships with software rendering forced on (`LIBGL_ALWAYS_SOFTWARE=1`), so blur and shadows are off; the README says the underlying bug is gone under UTM 5.0.x and `omarchy-arm-gpu --on` turns the GPU on there.

You can also emulate the normal x86_64 ISO in UTM, since QEMU can do that on ARM hosts, but you lose hardware acceleration entirely. Nobody in the threads above recommends it and we have not benchmarked it, so treat it as a last resort.

## Why the normal installer does not work

This part is worth understanding, because the common explanation is wrong.

Omarchy 4 does not refuse to run on ARM. The `uname -m` guard people quote lives in `install/preflight/guard.sh` on the 3.x line. In the v4.0.4 tree that directory is gone, and the only `uname -m` left is a single migration, `migrations/1789325478.sh`, that exits early on anything but x86_64. Nothing else in the repository is compiled for one CPU: it is shell scripts, Lua for Hyprland, QML for the shell, and config.

What is missing is the repository. Omarchy's installer (`install/post-install/pacman.sh`) copies `default/pacman/mirrorlist-stable` over `/etc/pacman.d/mirrorlist`, which points every Arch repo at `stable-mirror.omarchy.org/$repo/os/$arch`, and those mirrors are x86_64 only. Checked on 2026-09-16:

- `https://stable-mirror.omarchy.org/core/os/x86_64/core.db` returns 200, `core/os/aarch64/core.db` returns 404
- `https://mirror.omarchy.org/core/os/x86_64/core.db` returns 200, the aarch64 path returns 404

The shipped `default/pacman/pacman-stable.conf` (and its rc and edge siblings) also enables `[multilib]`, which has no Arch Linux ARM counterpart.

There is real movement on the add-on repo, though. Commit [4ed5f14](https://github.com/omacom/omarchy-pkgs/commit/4ed5f14629), "Build the omarchy package pair for aarch64", landed on 2026-09-02, and the `omarchy` PKGBUILD now declares `arch=('x86_64' 'aarch64')`. The `[omarchy]` repo that ships alongside the Arch mirrors does now have an aarch64 tree, but only on the edge channel. Checked on 2026-09-16:

| Channel | aarch64 `omarchy.db` | x86_64 `omarchy.db` |
| --- | --- | --- |
| edge | 200, 115 packages, `omarchy` 4.0.2-1 | 200, 243 packages, `omarchy` 4.0.4-1 |
| rc | 404 | 200 |
| stable | 404 | 200 |

So the aarch64 side of the add-on repo exists, is roughly half the size of the x86_64 side, and is two point releases behind. The base Arch packages still have to come from Arch Linux ARM. That is exactly the gap every project on this page works around by hand.

The ISO repository has a plan document, `plans/aarch64-support.md` in [omacom/omarchy-iso](https://github.com/omacom/omarchy-iso), that targets a generic UEFI ARM64 ISO for Ampere servers, Graviton VMs and Snapdragon X laptops. It lists a real `pkgs.omarchy.org/{stable,edge}/aarch64/` as a hard prerequisite, and it puts Apple Silicon and Asahi explicitly out of scope. Read that as: even when an official ARM ISO ships, it is not aimed at your Mac.

## What still breaks once you are running

These are upstream bugs in Omarchy itself, not in the projects above, and all were open on 2026-09-16.

- The Install menu offers packages that only exist for x86_64. Every one fails with `target not found` in a floating terminal that closes before you can read it ([#8645](https://github.com/omacom/omarchy/issues/8645)), and the wrapper prints `Done!` anyway, so the failure is invisible ([#11591](https://github.com/omacom/omarchy/issues/11591)).
- Every `omarchy update` ends with "Linux kernel has been updated. Reboot?" even when nothing changed. `bin/omarchy-update-restart` looks for a package-owned `/usr/lib/modules/*/vmlinuz`, and Arch Linux ARM's `linux-aarch64` puts the image in `/boot` instead, so the check can never pass ([#10048](https://github.com/omacom/omarchy/issues/10048)). The code is still there unchanged in v4.0.4.
- On bare metal Asahi, brightness controls report success and do nothing, because the wrong backlight device gets picked ([#8125](https://github.com/omacom/omarchy/issues/8125)).

A few more, verified as open in the same tracker: 1Password is pinned to an old version on Apple Silicon (#9576), and an Omarchy user systemd unit is never installed into `/usr/lib/systemd/user/`, which leaves the other Omarchy user units disabled too (#10484). That last one is not ARM-specific, but it hits the ARM builds in a different way: the `omarchy-settings` package that ships those unit files exists for aarch64 only on the edge channel, so the ggalancs UTM build reproduces the package by hand, and he reports in discussion #7956 that his first image missed those unit files entirely, which made the first-run enable step fail on every login until the v2 image.

If you came from Omarchy 3, note that the config layout changed completely in 4.0.0. See [the Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) and [upgrading 3 to 4](/upgrade/3-to-4-quattro/) before you copy old dotfiles into an ARM guest.

## A word on the prebuilt images

The UTM route publishes a ready-made bundle on the Internet Archive with a default user and password, which the author tells you to change with `passwd`. That is a third-party disk image you cannot audit quickly. If you use it, treat it as untrusted: change the password immediately, do not put credentials or SSH keys on it, and check the published SHA-256 before importing. Building from the script yourself is slower and gives you something you watched get made.

The same caution applies less strongly to Try Omarchy, whose DMG is signed and notarized, and to omarchy-mac, which you run as a script you can read first.

## What to watch for on newer versions

DHH said on X on 2026-09-08 that the next release will be called Quattro RS 4.5. The thing to check when it lands is whether `pkgs.omarchy.org/stable/aarch64/` starts returning 200, and whether the aarch64 edge tree catches up to the x86_64 package count. That single change would turn most of the work in these projects into a normal install. Watch the ISO plan too, but remember it names Apple Silicon as out of scope, so an official ARM ISO is not the same as official Mac support.

Both `try-omarchy` and `omarchy-mac` now sit in the `omacom` GitHub organisation, the same one that hosts Omarchy itself, and `omarchy-mac` is a fork of `omacom/omarchy`. That is where the code lives, not a statement of support. The manual still describes the M-series path as user-driven, and neither project is listed as a supported install route.

## Related

- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Running Omarchy in Parallels](/run/parallels/)
- [Apple Silicon hardware notes](/hardware/apple-silicon-asahi/)
