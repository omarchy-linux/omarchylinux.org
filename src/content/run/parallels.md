---
title: "Run Omarchy 4 in Parallels Desktop on Intel and Apple Silicon"
description: "Omarchy 4 in Parallels Desktop: the Intel Mac route that works, the repeat_delay double-character fix, and why Apple Silicon has no supported path."
answer: "On an Intel Mac running Parallels Desktop 26 or earlier, the normal x86_64 Omarchy ISO installs like any other VM. Give it EFI boot, 4 cores, 8 GB RAM and 64 GB of disk. Then raise repeat_delay in ~/.config/hypr/input.lua, because the default of 250 produces duplicated characters in Parallels guests. On Apple Silicon there is no supported path: the ISO and the package repository are x86_64 only."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Parallels Desktop"
hostVersion: "26 and 27"
tags: [parallels, macos, vm, aarch64, keyboard, hyprland]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8760"
    title: "Issue #8760: Default repeat_delay = 250 causes duplicated characters during normal typing (Parallels VM guest)"
    kind: issue
    author: "Crankygeek01-dev"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/5293"
    title: "PR #5293: Update default repeat_delay to improve holding delete and vim motions"
    kind: pr
    author: "jondkinney"
    date: "2026-04-13"
  - url: "https://github.com/omacom/omarchy/discussions/452"
    title: "Discussion #452: Installing Omarchy in a VM on an M* Mac"
    kind: discussion
    author: "swombat"
    date: "2025-08-02"
  - url: "https://github.com/omacom/omarchy/discussions/1407"
    title: "Discussion #1407: Fix images rendering as entirely black in Parallels Desktop on M-Series Macs ARM64 aarch64"
    kind: discussion
    author: "jondkinney"
    date: "2025-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8645"
    title: "Issue #8645: Install menu offers x86_64-only packages on aarch64: every entry fails with `target not found` in a floating terminal that closes"
    kind: issue
    author: "alexandru-savinov"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/discussions/7956"
    title: "Discussion #7956: Omarchy 4 (quattro) on Apple Silicon: a one-script build for a native aarch64 UTM VM"
    kind: discussion
    author: "ggalancs"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/2251"
    title: "Issue #2251: Add VM Guides"
    kind: issue
    author: "ryanrhughes"
    date: "2025-10-06"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
  - url: "https://kb.parallels.com/en/131175"
    title: "Parallels KB 131175: Parallels Desktop compatibility with Intel-based Mac computers"
    kind: docs
  - url: "https://kb.parallels.com/en/130217"
    title: "Parallels KB 130217: Run Intel-based virtual machines on Apple silicon Macs using Parallels Desktop x86 emulator"
    kind: docs
  - url: "https://github.com/vivek-dg/omarchy-m1"
    title: "vivek-dg/omarchy-m1: Omarchy Setup for Apple Silicon M1 Mac on Parallels"
    kind: other
    author: "vivek-dg"
    date: "2025-11-12"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH on X: Next version of Omarchy is going to be Quattro RS 4.5"
    kind: other
    author: "dhh"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
credits:
  - name: "Crankygeek01-dev"
    url: "https://github.com/Crankygeek01-dev"
    for: "Isolating the duplicated-character problem in a Parallels guest to repeat_delay and measuring which values fix it"
  - name: "jondkinney"
    url: "https://github.com/jondkinney"
    for: "The software-rendering workaround for black image windows in Parallels on M-series Macs"
  - name: "swombat"
    url: "https://github.com/swombat"
    for: "The original end-to-end Parallels on Apple Silicon write-up that the official manual links to"
  - name: "ggalancs"
    url: "https://github.com/ggalancs"
    for: "Documenting why the Omarchy 4 package cannot be installed on aarch64 and what an ARM build has to reproduce by hand"
faq:
  - q: "Can I run Omarchy on a Mac with Apple Silicon using Parallels?"
    a: "Not with the official ISO. Omarchy ships an x86_64 image and its package repository has no stable aarch64 tree, so a native ARM guest has to be assembled by hand. Parallels' x86 emulation preview is far too slow and too limited to carry a desktop."
  - q: "Why do I get doubled letters like helllo when typing in a Parallels VM?"
    a: "Omarchy ships repeat_delay = 250, and one Parallels user found that inside the VM a normal keypress is often held long enough to trigger key repeat at that setting. Raise it to 500 or 600 in ~/.config/hypr/input.lua. This is issue #8760 and it is still open on 4.0.4."
  - q: "Does the old Parallels guide in the manual still apply to Omarchy 4?"
    a: "Only in outline. Discussion #452 was written in August 2025 and edits GRUB, hyprland.conf and uses a bare install mode. Omarchy 4 boots with Limine, configures Hyprland in Lua, and has no bare mode, so those specific commands no longer match."
  - q: "Do I need Parallels Tools?"
    a: "Not to get a working desktop. Clipboard and display resize are the things you lose without it, and Parallels Tools is a kernel module you install from Parallels' own ISO, not a package in the Arch repositories."
related: [virtualbox, utm-apple-silicon, vmware-workstation-fusion, what-breaks-in-a-vm]
draft: false
---

Parallels Desktop is two different products depending on your Mac, and Omarchy behaves very differently on each. Decide which one you have before you download anything.

On an **Intel Mac**, Parallels runs x86_64 guests natively. The stock Omarchy ISO installs the same way it would in any other desktop hypervisor. This is the route that works. Parallels Desktop 26 is the last version that runs on Intel Macs at all, and Parallels' own compatibility note says version 27 requires Apple Silicon, so this route ends with Parallels 26.

On an **Apple Silicon Mac**, Parallels runs ARM guests. Omarchy publishes an x86_64 ISO only, and its package repository has no stable aarch64 tree, so there is no supported install. Everything in that direction is a hand-built ARM system with Omarchy's files copied onto it. The official manual links a user guide for it and describes the process as cumbersome, which is fair.

Checked against Omarchy 4.0.4, released 2026-09-15.

## Intel Macs: the settings that work

1. Create a new VM in Parallels from the Omarchy ISO. Download it from [omarchy.org](https://omarchy.org) and check it against the [verification page](/verify/).
2. In the VM's hardware settings, use EFI boot, and leave Secure Boot and the virtual TPM off. The manual's [Getting Started](https://omarchy.org/manual/getting-started/) page says Secure Boot and TPM have to be turned off to install Omarchy at all.
3. Give it at least 4 CPUs, 8 GB of RAM and 64 GB of disk. For comparison, the one documented Parallels build in discussion #452 used 4 CPUs, 16 GB and 64 GB and reported that as comfortable.
4. Boot the ISO and answer the installer's questions normally. Full disk encryption inside a VM is fine, though you will type the passphrase at every boot.
5. After the first login, fix key repeat before you do anything else. See the next section.

If you are building a throwaway VM you will rebuild often, the [unattended install path](https://omarchy.org/manual/unattended-installs/) is worth the setup. Attach a second small drive labelled `cidata` with the installer's configuration files on it and the wizard is skipped entirely.

## Fix the duplicated characters

This is the one Parallels-specific bug with a filed report. The symptom is stray doubled letters turning up every few sentences while you type at a normal pace, not while holding a key down.

1. Open `~/.config/hypr/input.lua`, or reach it through _Setup > Input_ in the Omarchy menu (`Super + Space`).
2. Add this block:

```lua
hl.config({
  input = {
    repeat_delay = 600,
    repeat_rate = 30,
  },
})
```

3. Save. If the new delay does not take effect on its own, run `hyprctl reload`. No logout is needed.

### Verify it worked

Type a long paragraph of prose in a terminal or an editor and watch for doubled letters. The reporter on issue #8760 found 500 improved things noticeably and 600 removed the duplication completely, so if 600 feels sluggish when you hold backspace, try 500 and retest.

You can also confirm the value landed:

```bash
hyprctl getoption input:repeat_delay
```

### Why it happens

Omarchy's default is `repeat_delay = 250` in `default/hypr/input.lua`. That value came from PR #5293 in April 2026, which lowered it from 600 so that holding backspace or holding `j` in Vim responds quickly, with the author noting it was the lowest value that did not cause double presses in their testing.

The PR says nothing about VMs, and the #8760 reporter could not test the same config on bare metal, so the link to Parallels is the reporter's theory rather than a measured cause: a hypervisor adds latency and jitter to key events, which makes it easier for a key held for a perfectly normal length of time to trip a 250 ms threshold. The high `repeat_rate` of 40 then turns each trip into several extra characters rather than one.

Issue #8760 is open, and `repeat_delay = 250` is still the shipped default in 4.0.4 and on the development branch as of 2026-09-16. The same PR put the value into late 3.x as well (3.8.4 ships it in `~/.config/hypr/input.conf` rather than the Lua file), so the report is not specific to 4.x.

## Resolution and scaling

Omarchy assumes a HiDPI display and ships `GDK_SCALE` at 2. In a Parallels window that usually means everything is enormous.

Open `~/.config/hypr/monitors.lua` via _Setup > Monitors_ and set both knobs to 1:

```lua
local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1
```

To pin a resolution rather than take whatever Parallels offers, list what the guest can see first:

```bash
hyprctl monitors all
```

Then add an entry using the output name that command prints:

```lua
hl.monitor({ output = "Virtual-1", mode = "2560x1440@60", position = "0x0", scale = 1 })
```

You can also step through scaling ratios live with `Super + /` and `Super + Alt + /`, which is the quickest way to find a setting that suits the window size you actually use.

## Black image windows

If opening an image gives you a solid black window, the app is failing at hardware GL init inside the guest. jondkinney documented the fix for Parallels on M-series Macs in discussion #1407: force software rendering for the image viewer.

```bash
cp /usr/share/applications/imv.desktop ~/.local/share/applications/
sed -i 's/Exec=imv/Exec=env LIBGL_ALWAYS_SOFTWARE=1 imv/' ~/.local/share/applications/imv.desktop
update-desktop-database ~/.local/share/applications/
```

`imv` is still the image viewer in 4.0.4, so the recipe still applies. If more than one app is affected rather than just images, set the variable for the whole session instead by adding `hl.env("LIBGL_ALWAYS_SOFTWARE", "1")` to `~/.config/hypr/hyprland.lua` after the `require("default.hypr.omarchy")` line, and accept that you lose blur and shadows.

## Parallels Tools

You do not need Parallels Tools for a working desktop. You need it for shared clipboard, drag and drop, and dynamic resolution.

Be aware of what you are signing up for. Parallels Tools is not in the Arch repositories or the AUR. It ships as an installer on an ISO that Parallels mounts into the guest, and it builds a kernel module. Omarchy 4.0.4 installs its own `linux-omarchy` kernel and makes it the first Limine boot entry, so any module has to build against that kernel rather than stock `linux`. The matching headers are installed alongside it, so the build has something to compile against, but Parallels has no reason to test against this kernel and the build can break on any kernel bump. Evidence here is thin: I have no confirmed report of Parallels Tools working on Omarchy 4.0.4. The one community write-up that covers it, [vivek-dg/omarchy-m1](https://github.com/vivek-dg/omarchy-m1) for an ARM guest in late 2025, found the tools' kernel support stopped at 6.13 and expected most features not to work even after installing them.

## Apple Silicon: what is actually possible

Three separate things block the official path:

- The ISO is x86_64. There is no ARM image.
- The Omarchy package repository has no stable aarch64 tree. Issue #8645 shows `https://pkgs.omarchy.org/stable/aarch64/omarchy.db` returning 404 while x86_64 returns 200. A later comment on that issue reports that as of 2026-09-06 the `edge` channel serves an aarch64 database with 115 packages, while stable and RC still return 404.
- Because of that, Install menu entries fail on ARM with `target not found` in a floating terminal that closes before you can read it. That is the substance of issue #8645, which is open.

The `linux-omarchy` kernel is x86_64 only, and its install migration exits immediately on any other architecture, so an ARM guest keeps the Arch Linux ARM kernel.

The manual's linked Parallels guide, discussion #452 by swombat, still describes the general shape: bootstrap Arch Linux ARM from a live Ubuntu ARM session, then layer Omarchy on top. But it was written in August 2025 for 1.x. It edits GRUB, edits `hyprland.conf`, and uses a bare install mode. Omarchy 4 boots with Limine, configures Hyprland in Lua, and has no bare mode, so treat that guide as a map, not a script. Issue #2251, raised by ryanrhughes and closed in July 2026, made exactly that point from the project's side: the VM guides had "deviated from our prescribed install of Limine".

The most current ARM work for Omarchy 4 is discussion #7956, which targets UTM rather than Parallels. It is worth reading anyway, because its findings are about the ARM side and not the hypervisor: the Omarchy package is `arch=('any')` and only the repository is x86-bound, 121 of the 148 base packages already exist in Arch Linux ARM by name (123 with two substitutions), and leaving `mako` installed on a 4.x system is harmful because Quickshell is now the notification daemon and mako grabs the D-Bus notification name first, so toasts come out unstyled.

Parallels' x86 emulation, introduced as an early preview in Desktop 20.2, is not a way around any of this. Parallels' own KB puts Windows boot times at 2 to 7 minutes with low responsiveness, limits the guest to one vCPU and 8 GB of RAM, rules out USB devices and sound, and cannot use the Parallels hypervisor. A Wayland desktop is not going to be usable under it.

## What to watch for on newer versions

DHH has said on X that the next release will be Quattro RS 4.5 rather than a 4.1. Two things to recheck then:

- Whether `repeat_delay` is still 250. It has not moved through any 4.0.x point release, and issue #8760 is still open.
- Whether `pkgs.omarchy.org` publishes an aarch64 tree on the stable channel. That single change would turn the Apple Silicon story from "assemble it yourself" into something much closer to a normal install.

## Related

- [Run Omarchy in VirtualBox](/run/virtualbox/)
- [Run Omarchy in UTM on Apple Silicon](/run/utm-apple-silicon/)
- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Unattended installs with cidata](/run/unattended-install-cidata/)
