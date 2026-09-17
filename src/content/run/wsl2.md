---
title: "Omarchy on WSL2: Hyprland will not run, and what to do instead"
description: "Omarchy on WSL2: Hyprland cannot start because WSL2 exposes no DRM node. What community .wsl images actually give you, and how to get the real desktop."
answer: "You cannot run the Omarchy desktop on WSL2. Hyprland needs a DRM node for its GBM allocator and WSL2 exposes only /dev/dxg, so the compositor refuses to start, nested or headless. Community .wsl images give you Omarchy's CLI, themes and tooling only. For the real desktop on Windows, use Try Omarchy for Windows or a Hyper-V VM."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "WSL2"
hostVersion: "Windows 10 and 11, WSL 2.x"
tags: [wsl2, windows, hyprland, wayland, vm]
sources:
  - url: "https://github.com/hyprwm/Hyprland/issues/3479"
    title: "Hyprland issue #3479: May I ask if there is a way to run Hyprland in wsl"
    kind: issue
    author: "w934423231"
    date: "2023-10-03"
  - url: "https://github.com/omacom/omarchy/discussions/473"
    title: "Discussion #473: wsl?"
    kind: discussion
    author: "WillEhrendreich"
    date: "2025-08-03"
  - url: "https://github.com/omacom/omarchy/discussions/10748"
    title: "Discussion #10748: push a wsl image.?"
    kind: discussion
    author: "kilasuit"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy-iso/issues/150"
    title: "omarchy-iso issue #150: Build and publish omarchy's .wsl artifact"
    kind: issue
    author: "linghengqian"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/discussions/445"
    title: "Discussion #445: Guide - Omarchy on Hyper-V"
    kind: discussion
    author: "max-pv"
    date: "2025-08-01"
  - url: "https://github.com/omacom/try-omarchy-windows"
    title: "omacom/try-omarchy-windows: Use Omarchy Linux on Windows without any hassle"
    kind: other
  - url: "https://github.com/craigloewen-msft/Omarchy-wsl"
    title: "craigloewen-msft/Omarchy-wsl: build a .wsl package for the CLI flavour of Omarchy"
    kind: other
    author: "craigloewen-msft"
  - url: "https://github.com/clarenceb/omarchy-wsl2"
    title: "clarenceb/omarchy-wsl2: Omarchy tooling as a WSL2 distro, with sway instead of Hyprland"
    kind: other
    author: "clarenceb"
  - url: "https://github.com/taufderl/omarchy-wsl"
    title: "taufderl/omarchy-wsl: Run Omarchy on Windows"
    kind: other
    author: "taufderl"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
credits:
  - name: "clarenceb"
    url: "https://github.com/clarenceb"
    for: "The writeup tracing Hyprland's WSL2 failure to Aquamarine's GBM allocator, and shipping sway with Omarchy keybindings as the substitute"
  - name: "nunix"
    url: "https://github.com/nunix"
    for: "The first step by step walkthrough of installing Omarchy inside an Arch WSL2 distro, and the list of installer steps to skip"
  - name: "craigloewen-msft"
    url: "https://github.com/craigloewen-msft"
    for: "A .wsl builder for the CLI half of Omarchy, on both x86_64 and ARM64"
  - name: "linghengqian"
    url: "https://github.com/linghengqian"
    for: "Filing the request for an official .wsl artifact alongside the ISO"
faq:
  - q: "Can I run Hyprland inside WSL2 if I use WSLg?"
    a: "No. WSLg gives you per application windows, not a compositor Hyprland can nest inside, and the one published trace of its protocol list shows no dmabuf support. Hyprland's backend also needs a DRM file descriptor to build its allocator, and WSL2 has no DRM device at all, so it exits before it draws anything."
  - q: "Is there an official Omarchy .wsl image?"
    a: "Not as of 4.0.4. A request is open as omarchy-iso issue #150 and a suggestion sits unanswered as discussion #10748. Nothing is published at iso.omarchy.org next to the ISO."
  - q: "What is the closest thing to real Omarchy on Windows?"
    a: "Try Omarchy for Windows, which runs a prebuilt Omarchy image under QEMU on the Windows Hypervisor Platform. It is still preview software. A Hyper-V or VMware VM installed from the normal Omarchy ISO is the other route."
  - q: "Do the community .wsl builds track Omarchy 4?"
    a: "Partly. Omarchy-wsl pins its Omarchy checkout to v4.0.0 by default. taufderl/omarchy-wsl pins the omarchy pacman package to 4.0.1-1 in a single file you bump by hand. clarenceb/omarchy-wsl2 builds from whatever Omarchy master is at build time. None of them updates itself when a point release ships, so expect to rebuild."
related: [hyper-v, virtualbox, what-breaks-in-a-vm]
draft: false
---

Short version: WSL2 can run Omarchy's command line, and it cannot run Omarchy's desktop. That split is not a packaging problem someone will fix next month. It comes from what WSL2 exposes to Linux. It was already the answer when the first WSL thread appeared in August 2025, back on Omarchy 1.x, and it is still the answer on 4.0.4.

## What runs and what does not

| Piece | On WSL2 |
|---|---|
| Omarchy CLI, `omarchy-*` scripts, themes, Neovim, lazygit, btop, starship | Works |
| Individual GUI apps as normal Windows windows, through WSLg | Works |
| Hyprland, the Quickshell bar, lock screen, screensavers, the whole Omarchy 4 desktop | Does not start |
| Limine, snapper rollback, LUKS, Plymouth, hardware drivers | Not applicable, no boot sequence and no block device |

Omarchy's own manual has an "[Omarchy on...](https://omarchy.org/manual/omarchy-on/)" chapter listing Asahi, Parallels, VirtualBox, VMware Workstation, the Steam Deck and a NixOS port. WSL is not on it, and the string "wsl" does not appear anywhere in the v4.0.4 tree.

## Why Hyprland cannot start on WSL2

Linux inside WSL2 never sees a DRM device. What it sees instead is `/dev/dxg`, a paravirtualised Direct3D 12 device that Mesa's d3d12 driver talks to through dxcore. There is no `/dev/dri/card0` and no render node. You can confirm that from inside any WSL2 distro:

```bash
ls -l /dev/dri /dev/dxg
```

Since v0.42.0 in August 2024, Hyprland's backends live in a separate library, Aquamarine, and Aquamarine only knows how to build a GBM buffer allocator, which needs a DRM file descriptor. When none of its backends can hand one over, `src/backend/Backend.cpp` logs `Cannot open backend: no allocator available` and gives up. That code is still in hyprwm/aquamarine as of this page's verification date. The headless backend is no escape hatch: its `drmFD()` returns `-1`, so it hits the same wall.

Running Hyprland nested inside WSLg fails for a different reason. In the protocol trace clarenceb captured for [clarenceb/omarchy-wsl2](https://github.com/clarenceb/omarchy-wsl2), WSLg's Weston fork offered `wl_shm` but not `zwp_linux_dmabuf_v1`, and Aquamarine's Wayland backend treats dmabuf as required. That trace came from one ARM64 machine, so re-run it on your own build before assuming it still holds. Upstream has not been coy about any of this. When someone asked in October 2023 whether Hyprland could run in WSL, in [Hyprland issue #3479](https://github.com/hyprwm/Hyprland/issues/3479), the maintainer closed it the same day with a one word answer: "no". The crash log in that report is from the older wlroots backend, but the missing DRM fd is the same complaint. The issue has stayed closed.

wlroots compositors such as sway do start under WSL2, because wlroots will settle for plain shared memory buffers and a CPU renderer when there is no DRM node to build GBM on. That gets you a tiling desktop, but it is a different compositor with its own config, not Omarchy.

## If you want the real Omarchy desktop on Windows

Use a virtual machine, not WSL2.

1. **Try Omarchy for Windows.** [omacom/try-omarchy-windows](https://github.com/omacom/try-omarchy-windows) runs a prebuilt Omarchy image under QEMU on the Windows Hypervisor Platform, the same hypervisor layer WSL2 depends on, so the Hyper-V role is not required and Windows Home works. The current release is v0.0.19-preview, published 2026-09-16, carrying Omarchy 4.0.3. It lives in the same GitHub organisation as Omarchy itself, but it is preview software with an open v1 checklist, so treat it as a trial rather than a daily driver.
2. **Hyper-V.** Available on Windows Pro, Education and Enterprise. There is a community guide at [discussion #445](https://github.com/omacom/omarchy/discussions/445), but read it with the date in mind: it was written in August 2025 against a plain Arch ISO with GRUB, and Omarchy now ships its own installer ISO with Limine. See [Omarchy on Hyper-V](/run/hyper-v/) for the current steps.
3. **VirtualBox or VMware.** Both are covered in the manual and on this site at [VirtualBox](/run/virtualbox/) and [VMware](/run/vmware-workstation-fusion/). Expect the usual VM compromises, listed at [what breaks in a VM](/run/what-breaks-in-a-vm/).

Download the ISO from [omarchy.org](https://omarchy.org) and check it against the [verification steps](/verify/) before you boot it.

## If you only want the Omarchy CLI on WSL2

Three community builders exist. All of them produce a `.wsl` file you install with `wsl --install --from-file`. None of them gives you Hyprland, and all of them are young, so read the repo before you trust it.

- [craigloewen-msft/Omarchy-wsl](https://github.com/craigloewen-msft/Omarchy-wsl) builds a CLI and TUI image with `wslc`, on x86_64 and ARM64. It pins the Omarchy checkout to v4.0.0 by default and says so. Its README calls it a community project.
- [taufderl/omarchy-wsl](https://github.com/taufderl/omarchy-wsl) installs the actual `omarchy` pacman package with pacstrap, so the full dependency graph comes along, then lets Omarchy's own scripts under `/usr/share/omarchy/install/` do the setup, then documents every piece that does not apply under WSL2. Its stated status is that it runs without a Hyprland desktop session.
- [clarenceb/omarchy-wsl2](https://github.com/clarenceb/omarchy-wsl2) ships Omarchy's tooling plus a sway session configured with Omarchy keybindings, gaps and themes, rendered on the CPU with pixman. No animations, no blur, no rounded corners, no Xwayland, one output.

If you would rather do it by hand, the walkthrough by nunix in [discussion #473](https://github.com/omacom/omarchy/discussions/473) is the original recipe: install the `archlinux` WSL distro, create a user, add them to sudoers, set `[user] default` in `/etc/wsl.conf`, then run Omarchy's installer with the network, power, login, nvidia, firewall, bluetooth and asdcontrol steps commented out. That was written in August 2025 against Omarchy 1.x, when the installer was a single `install.sh` sourcing scripts under `config/`, `development/` and `desktop/`. The 4.0.4 tree has `install/config/`, `install/hardware/`, `install/login/`, `install/post-install/` and `install/user/` instead, and there is no `power.sh` or `asdcontrol.sh` any more, so the exact file list no longer matches. Use it as a map, not a script.

## Is an official image coming

There is no published `.wsl` artifact. The URL pattern proposed in the request, next to the ISO on iso.omarchy.org, returns 404 for both 4.0.2 and 4.0.4 as of 2026-09-16.

Two threads are open. [omarchy-iso issue #150](https://github.com/omacom/omarchy-iso/issues/150), filed 2026-09-03 by linghengqian, asks the project to build and publish a `.wsl` artifact the way Ubuntu does alongside its ISOs. [Discussion #10748](https://github.com/omacom/omarchy/discussions/10748), opened 2026-09-08, asks the same thing in one line and has no replies. Neither has a maintainer answer. Nothing in the 4.0.4 tree suggests WSL support is being built.

Be clear about what an official image would and would not change. It would make the CLI install one command. It would not make Hyprland start, because that limitation is in WSL2's device model, not in Omarchy's packaging.

## What to watch for on newer versions

The thing that would actually change this answer is Microsoft exposing a DRM render node inside WSL2, WSLg starting to advertise dmabuf, or Aquamarine gaining a non GBM allocator path. Watch the hyprwm/aquamarine and microsoft/wslg repos rather than the Omarchy tracker; [Hyprland issue #3479](https://github.com/hyprwm/Hyprland/issues/3479) has been closed since 2023 and will not be where news lands.

On the Omarchy side, the 3.x to 4.x move matters for any WSL guide you find. Config now lives in Lua files with an `o.bind("SUPER + K", "Label", action)` DSL instead of `~/.config/hypr/*.conf`, and the bar, menus, notifications and lock screen run inside one long running Quickshell process. Any WSL walkthrough written before 2026-08-14 predates that. See [the 3 to 4 upgrade](/upgrade/3-to-4-quattro/) and the [hyprland.conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) for what changed.

Evidence for the CLI builders is thin. Two of the three repos had zero or one star and no pushes since late August 2026 when this page was checked. Nobody has published a long running report of Omarchy under WSL2 on a daily workload, so treat these as experiments.
