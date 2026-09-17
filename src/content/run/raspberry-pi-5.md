---
title: "Omarchy on Raspberry Pi 5 and ARM boards"
description: "Omarchy has no official aarch64 build. What the edge channel actually publishes for ARM, what breaks on a Raspberry Pi 5, and the path that works."
answer: "There is no official Omarchy build for the Raspberry Pi 5. The ISO is x86_64 only and the stable and RC package channels have no aarch64 tree. Only the edge channel serves aarch64, and it lagged at Omarchy 4.0.2 with 115 packages when checked. The working path is Arch Linux ARM plus a community port, accepting that menus, the kernel check and several apps are broken."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Raspberry Pi 5 and ARM boards"
hostVersion: "Raspberry Pi 5 (BCM2712) on Arch Linux ARM aarch64"
tags: [raspberry-pi, aarch64, arm, edge-channel, unsupported]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/642"
    title: "Discussion #642: To be revised [The Guide to Installing Omarchy (Hyprland) on a Raspberry Pi 5]"
    kind: discussion
    author: "sailoz"
    date: "2025-08-11"
  - url: "https://github.com/omacom/omarchy/discussions/7960"
    title: "Discussion #7960: FR: Support aarch64"
    kind: discussion
    author: "stephenmw"
    date: "2026-08-23"
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
  - url: "https://github.com/omacom/omarchy/issues/9356"
    title: "Issue #9356: omarchy install terminal <pkg> reports failure but still mutates xdg-terminals.list and copies config when package is missing on aarch64"
    kind: issue
    author: "ozz1ee-dev"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9576"
    title: "Issue #9576: omarchy-install-1password pins 8.12.0 with an existence-only guard, so Apple Silicon never gets 1Password updates (current: 8.12.34)"
    kind: issue
    author: "bierlingm"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/876"
    title: "PR #876: Add aarch64 support (closed unmerged)"
    kind: pr
    author: "nilszeilon"
    date: "2025-08-17"
  - url: "https://github.com/omacom/omarchy/issues/803"
    title: "Issue #803: om-arm-archy ? (closed)"
    kind: issue
    author: "iandol"
    date: "2025-08-15"
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/plans/aarch64-support.md"
    title: "omarchy-iso: Plan: aarch64 (Generic UEFI ARM64) build for omarchy-iso"
    kind: docs
  - url: "https://github.com/omacom/omarchy-pkgs"
    title: "omacom/omarchy-pkgs: Omarchy Package Repository build system"
    kind: docs
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "The Omarchy Manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/hyprwm/Hyprland/discussions/11253"
    title: "Hyprland Discussion #11253: Fractional scaling on 4K monitor exceeds GL_MAX_TEXTURE_SIZE on Raspberry Pi 5"
    kind: discussion
    author: "sailoz"
    date: "2025-07-28"
  - url: "https://github.com/vincenth19/omarchy-pi"
    title: "vincenth19/omarchy-pi: Omarchy on Raspberry Pi 5, port, patches, and flashable images"
    kind: other
  - url: "https://github.com/alexisraitano-myffu/omarchy-arm"
    title: "alexisraitano-myffu/omarchy-arm: Unofficial aarch64 port of Omarchy"
    kind: other
  - url: "https://github.com/omacom/omarchy-mac"
    title: "omacom/omarchy-mac: Opinionated Arch/Hyprland Setup for Apple Silicon Macs M1/M2"
    kind: other
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "sailoz"
    url: "https://github.com/sailoz"
    for: "The original Pi 5 install walkthrough and the Hyprland V3D scaling bug report"
  - name: "nilszeilon"
    url: "https://github.com/nilszeilon"
    for: "The aarch64 preflight work in PR #876"
  - name: "alexandru-savinov"
    url: "https://github.com/alexandru-savinov"
    for: "Tracing the missing architecture gate through omarchy-pkg-add and the floating terminal"
  - name: "vincenth19"
    url: "https://github.com/vincenth19"
    for: "Rebuilding the Omarchy package set for aarch64 and documenting the porting patches"
faq:
  - q: "Is there an official Omarchy image for the Raspberry Pi 5?"
    a: "No. The Omarchy ISO is x86_64 only, and the ISO repository states the ISO is the only supported way to install Omarchy. Nothing on omarchy.org publishes an ARM image."
  - q: "Does the edge channel mean aarch64 is supported now?"
    a: "Not yet. The edge package tree does serve aarch64, but the scheduled build pipeline in omarchy-pkgs still publishes x86_64 only by default, so the ARM tree is off the scheduled pipeline and falls behind. Stable and RC have no aarch64 tree at all."
  - q: "Will a Raspberry Pi 5 run the Quickshell desktop from Omarchy 4?"
    a: "It can. Quickshell and Hyprland both build for aarch64 and community ports boot the Quattro shell. Expect modest performance and avoid fractional scaling, which exceeds the V3D GPU texture limit."
  - q: "What about Apple Silicon or an ARM VM instead?"
    a: "Apple Silicon is much better served. Asahi Alarm plus omarchy-mac is a one-command install and gets far more attention than any single board computer."
related: [utm-apple-silicon, what-breaks-in-a-vm, proxmox-qemu-kvm]
draft: false
---

## The decision first

If you want a supported Omarchy, buy or borrow an x86_64 machine. As of Omarchy 4.0.4, checked on 2026-09-16, there is no official Raspberry Pi 5 image, no aarch64 ISO, and no aarch64 tree on the stable or release candidate package channels. Everything that runs Omarchy on a Pi today is a community port that patches upstream.

If you want to do it anyway, the working shape is: install Arch Linux ARM on the Pi first, then lay a community aarch64 port of Omarchy on top of it. Do not try to run the official installer or `omarchy-channel-set` on an ARM board. Both assume x86_64 mirrors.

## What is actually published for ARM

Omarchy ships in three separate layers, and they have different architecture support.

| Layer | What it is | aarch64 today |
| --- | --- | --- |
| The ISO | archiso image with the Omarchy Configurator | No. `configs/profiledef.sh` sets `arch="x86_64"` and `bin/omarchy-iso-make` has no arch flag |
| Arch mirror | `mirror.omarchy.org`, `stable-mirror.omarchy.org` for core, extra, multilib | No. `core/os/aarch64/core.db` returns 404 on both |
| `[omarchy]` repo | `pkgs.omarchy.org/<channel>/$arch`, the Omarchy packages themselves | Edge only |

I fetched all of these on 2026-09-16. `pkgs.omarchy.org/edge/aarch64/omarchy.db` returns 200 and contains 115 packages, last modified 2026-09-05, with `omarchy` at 4.0.2-1. The x86_64 edge tree at the same moment carried 243 packages with `omarchy` at 4.0.4-1, and stable x86_64 carried 235. Both `stable/aarch64` and `rc/aarch64` return 404.

That gap is not an accident. The build system in `omacom/omarchy-pkgs` documents multi-architecture support and builds foreign architectures under QEMU emulation, but its checked-in list of published architectures is `PUBLISHED_ARCHES="${OMARCHY_ARCHES:-x86_64}"`. The scheduled pipeline therefore queues x86_64 only. The README documents a one-off `OMARCHY_ARCHES=aarch64` override, and an aarch64 tree that sits eleven days and two point releases behind x86_64 looks like the product of such runs rather than the pipeline, though nothing public says who runs them. Contributors have been landing aarch64 recipes into that repo through September 2026, including Ghostty, OBS Studio and Pinta builds merged on 2026-09-15, but those had not reached the published aarch64 database yet when I checked.

The ISO repository carries an unimplemented design document, `plans/aarch64-support.md`, for a generic UEFI ARM64 ISO. Read its scope line before you get excited: it targets Ampere servers, Graviton VMs and Snapdragon X laptops, and explicitly puts Apple Silicon and single board computers with U-Boot or rpi-firmware out of scope. A Raspberry Pi 5 is in that excluded group.

## What breaks on a Pi 5, specifically

These are open issues filed from aarch64 machines. I checked each one against the 4.0.4 tree, and one of them turns out to be a port's bug rather than upstream's.

- The Install menu offers packages that cannot exist on ARM. Issue #8645 showed that nothing in the install path or the `omarchy-hw-*` predicates checks the architecture, so entries fail with `target not found` inside a floating terminal that vanishes before you can read it. Issue #11591 found the same thing still true in September, with Spotify and Dropbox as examples. It also found that the presentation wrapper prints `Done!` for any exit status except Ctrl-C, and because the entry is only hidden once the package is present, it is offered again every time.
- `omarchy install terminal <pkg>` can leave you with no terminal, but only on a port. Issue #9356 reports that on aarch64 the Ghostty install is skipped while `~/.config/xdg-terminals.list` is rewritten anyway, so keybindings point at a binary that is not installed. The `omarchy-pkg-add` it quotes, which skips unavailable packages and exits 0, is omarchy-mac's. Upstream's 4.0.4 `omarchy-pkg-add` exits 1 when a package did not install, so `omarchy-install-terminal` takes its failure branch and leaves the file alone. PR #9365, which makes the terminal script check the result itself, is still open.
- Every update asks you to reboot. Issue #10048 explains why: `omarchy-update-restart` looks for `/usr/lib/modules/*/vmlinuz`, but `linux-aarch64` puts its kernel image at `/boot/Image` and leaves only modules under `/usr/lib/modules`, so the check finds nothing and treats that as a kernel replacement.
- The Omarchy kernel is x86_64 only. `linux-omarchy` does not exist in the aarch64 tree, and migration `1789325478.sh` exits early unless `uname -m` is `x86_64`. On a Pi you stay on `linux-rpi` or `linux-aarch64`.
- Several apps are simply x86_64 binaries. Spotify, Dropbox and LM Studio are `arch=('x86_64')` in the AUR and absent from the aarch64 edge tree. 1Password is the odd one out: the AUR package is x86_64 only, but the aarch64 edge tree carries its own `1password` build, and issue #9576 is about omarchy-mac's tarball install script pinning 8.12.0 on Apple Silicon rather than an upstream script.
- Fractional scaling on a 4K display fails on the Pi GPU. Hyprland discussion #11253 traced it to `GL_MAX_TEXTURE_SIZE` on the V3D driver. Use an integer scale.

On Omarchy 4 that last one lives in Lua, not the old `monitors.conf`. Edit `~/.config/hypr/monitors.lua` and set an integer scale:

```lua
local omarchy_gdk_scale = 2
local omarchy_monitor_scale = 2

hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
```

If you are following a Pi guide written for Omarchy 3.x, it will tell you to edit `monitors.conf` and `bindings.conf`. Those files no longer drive anything in 4.x. See [the Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

## The path that works

1. Flash Arch Linux ARM for the Pi 5 and get it booting, updated and online first. Nothing about Omarchy helps with the Pi boot chain, firmware or the V3D driver.
2. Do not run `omarchy-channel-set edge`. It calls `omarchy-refresh-pacman`, which overwrites `/etc/pacman.conf` with `default/pacman/pacman-edge.conf` and `/etc/pacman.d/mirrorlist` with `default/pacman/mirrorlist-edge`. That leaves you with core, extra and multilib pointed at `mirror.omarchy.org`, no `alarm` repo, and a `pacman -Syyuu` straight after. The mirror has no aarch64 tree, so you would lose your base repositories. If you want Omarchy packages, add the `[omarchy]` edge section by hand and leave your Arch Linux ARM mirrorlist alone:

Append this to `/etc/pacman.conf`, keeping your existing core, extra and alarm entries:

```ini
[omarchy]
Server = https://pkgs.omarchy.org/edge/$arch
```

The packages are signed, so pacman will refuse them until the Omarchy key is trusted. `bin/omarchy-update-keyring` shows the upstream bootstrap: `pacman-key --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571 --keyserver keys.openpgp.org`, `pacman-key --lsign-key` on the same fingerprint, then `pacman -S omarchy-keyring`. The keyring package is in the aarch64 edge tree.

3. Install from a community port rather than upstream's installer. Two worth looking at, both unofficial and both explicit about it: `vincenth19/omarchy-pi`, which rebuilds the Omarchy package set for aarch64 and is aiming at a flashable Pi 5 image, and `alexisraitano-myffu/omarchy-arm`, which installs onto a machine already running Arch Linux ARM. Read the diff before you run either. Ports are covered on [forks and ports](/vs/forks-and-ports/).
4. Expect to skip the Install menu and use `pacman` and `yay` directly, because of issues #8645 and #11591.

The honest caveat on the Pi specifically: `omarchy-pi` describes itself as alpha and says it has been verified in an aarch64 VM and under QEMU, but not yet on real Pi 5 hardware with the V3D GPU and BCM2712 firmware. Earlier reports in discussion #642 from people on real hardware recommend 1080p over 4K and Brave over Chromium.

## Verify what you have

```bash
uname -m                     # aarch64 on a Pi 5
pacman -Q omarchy 2>/dev/null || echo "Omarchy not installed as a package"
curl -o /dev/null -w '%{http_code}\n' https://pkgs.omarchy.org/edge/$(uname -m)/omarchy.db
curl -o /dev/null -w '%{http_code}\n' https://pkgs.omarchy.org/stable/$(uname -m)/omarchy.db
```

On aarch64 today the first curl prints 200 and the second prints 404. If the second one ever prints 200, stable has gained an ARM tree and this page is out of date.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5. Three specific things would change the answer here, and each is checkable in a minute:

- `PUBLISHED_ARCHES` in `helpers/paths.sh` in `omacom/omarchy-pkgs` gaining `aarch64`. That is the switch that puts ARM on the scheduled build pipeline, and the README says adding an architecture there is the enablement step.
- A 200 from `pkgs.omarchy.org/stable/aarch64/omarchy.db`, which would mean ARM packages reached the stable channel.
- An `--arch` flag on `bin/omarchy-iso-make`, or `arch="aarch64"` appearing in the ISO profile. Even then, the plan document excludes Raspberry Pi class boards, so an ARM ISO would not automatically mean a Pi image.

The upstream history is worth knowing so you do not misread a stale thread. Issue #803 asked for ARM support in 2025 and was closed by DHH pointing at PR #876, which added aarch64 and Asahi preflight scripts. That PR was closed unmerged on 2025-10-27 after 59 commits. Discussion #7960, opened 2026-08-23, is the live feature request and is still open with no maintainer commitment.

If your goal is just Omarchy on ARM rather than Omarchy on a Pi, Apple Silicon is a far better bet. `omacom/omarchy-mac` installs Omarchy 4 alongside macOS on Asahi Alarm in one command, and the manual's [Omarchy on...](https://omarchy.org/manual/omarchy-on/) chapter points there too. See [Apple Silicon hardware notes](/hardware/apple-silicon-asahi/) and [UTM on Apple Silicon](/run/utm-apple-silicon/).

## Related

- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Verifying an Omarchy download](/verify/)
