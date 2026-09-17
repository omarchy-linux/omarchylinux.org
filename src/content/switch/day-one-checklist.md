---
title: "Omarchy 4 day-one checklist: your first 48 hours"
description: "A first 48 hours checklist for Omarchy 4.0.4: what to set up first, and the open issues that block keyboard layout, screen sharing, scaling and printing."
answer: "Do three things in the first hour: use only lowercase ASCII letters in your disk passphrase, confirm your login password types on a US QWERTY greeter, and test that snapshot rollback actually works before you trust it. Then expect real friction on screen sharing, fractional scaling, printers, and Wi-Fi or Bluetooth after suspend."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [checklist, onboarding, switching, quattro, first-run]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8196"
    title: "Issue #8196: Full-disk install: password set under a non-US keyboard layout can be untypeable at the LUKS boot prompt"
    kind: issue
    author: "notwitcheer"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/6880"
    title: "Issue #6880: SDDM greeter always uses US keyboard layout, ignoring the system layout"
    kind: issue
    author: "g-desoutter"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/10842"
    title: "Issue #10842: SDDM boot greeter clips on mixed displays and ignores Colemak/Russian layouts"
    kind: issue
    author: "backmeupplz"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/8047"
    title: "Issue #8047: btrfs-overlayfs is enabled by default, which makes snapshot rollback impossible: limine-snapper-sync refuses to start inside every snapshot boot"
    kind: issue
    author: "Cloud-Ops-Dev"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations (surfaced as: LUKS prompt still QWERTY after e891e5c)"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/11221"
    title: "Issue #11221: hyprland-preview-share-picker-git package is pinned to a Dec 2025 build, missing the upstream origin-offset fix (merged Aug 2026)"
    kind: issue
    author: "jpaferreira-git"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10496"
    title: "Issue #10496: Screen glitches in Google Meet"
    kind: issue
    author: "Abi-de-jo"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/9904"
    title: "Issue #9904: 1Password: unlock popup unusable on fractional scaling, and its window rule targets a non-resizable window"
    kind: issue
    author: "kurtome"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/9907"
    title: "Issue #9907: Electron/Chromium secondary windows leave stale/duplicated regions at scale 1.6"
    kind: issue
    author: "d-geula"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/11814"
    title: "Issue #11814: HP Smart Tank 520/540 USB printer not plug-and-play: driverless queue always fails (universal filter failed), hplip not shipped"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11186"
    title: "Issue #11186: Printing from Firefox to a local USB HP printer produces PJL garbage + blank pages after cups-browsed is removed in 4.0.3"
    kind: issue
    author: "docPoacher"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11377"
    title: "Issue #11377: brcmfmac wedges NetworkManager+wpa_supplicant into unkillable D-state, aborting suspend"
    kind: issue
    author: "rand0mdud3"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11264"
    title: "Issue #11264: MacBook Air 2020 (MacBookAir9,1, T2): Bluetooth never powers on at boot, and suspend always fails on brcmfmac D3 timeout"
    kind: issue
    author: "austinsomer"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11630"
    title: "Issue #11630: omarchy update exits silently with no output (script -qefc re-exec appears to no-op)"
    kind: issue
    author: "kostadinoff"
    date: "2026-09-13"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
credits:
  - name: "notwitcheer"
    url: "https://github.com/notwitcheer"
    for: "Traced the AZERTY LUKS lockout to the installer layout not reaching the initramfs"
  - name: "Cloud-Ops-Dev"
    url: "https://github.com/Cloud-Ops-Dev"
    for: "Found that btrfs-overlayfs blocks limine-snapper-sync inside every snapshot boot"
  - name: "docPoacher"
    url: "https://github.com/docPoacher"
    for: "Isolated the dropped-page printing bug to a libcupsfilters version mismatch"
faq:
  - q: "What is the single most common day-one mistake?"
    a: "Setting a disk passphrase with characters that move between keyboard layouts. Issue #8196 reports a fresh AZERTY install where the digits in the passphrase were untypeable at the boot prompt, with no recovery short of reinstalling. Use lowercase ASCII letters only for the passphrase."
  - q: "Do I need to update immediately after installing?"
    a: "Yes, run omarchy update once before you customise anything. The ISO can be several point releases behind, and the update runs pending migrations that fix earlier bugs. Check that it printed output, because issue #11630 reports it exiting silently on 4.0.3."
  - q: "Is my old ~/.config/hypr/hyprland.conf still used on Omarchy 4?"
    a: "No. Omarchy 4.0.0 moved Hyprland configuration to Lua. The files are now hyprland.lua, input.lua, monitors.lua, bindings.lua and looknfeel.lua in ~/.config/hypr/. Leftover .conf files are ignored."
  - q: "Should I trust snapshot rollback as my safety net?"
    a: "Not without testing it. Issue #8047 reports that btrfs-overlayfs is on by default and prevents the restore path from running at all. Keep a real backup of your home directory as well."
related: [non-us-keyboard-layout-luks-sddm, screen-sharing-meet-zoom-teams, fractional-scaling-hidpi-apps, printers-and-scanners]
draft: false
---

Checked against Omarchy 4.0.4, released 15 September 2026. Everything below was verified against the 4.0.4 source tree and against open issues on the tracker.

## Hour one: three things that can lock you out

These are the items where a wrong choice costs you a reinstall. Do them before you customise anything.

**1. Keep your disk passphrase to lowercase ASCII letters.** Issue [#8196](https://github.com/omacom/omarchy/issues/8196) is an open report from a full-disk install on a French AZERTY laptop. The installer honoured the chosen layout while the passphrase was typed, but the early-boot LUKS prompt read US QWERTY. Digits on AZERTY sit on the shifted top row, so a passphrase with digits became untypeable, and the reporter found no recovery except reinstalling. QWERTZ and other remapped layouts are exposed the same way.

On 4.x the packaged `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` does bundle `/etc/vconsole.conf` into the initramfs so Plymouth applies your layout, but only when that layout types Latin letters. Cyrillic, Greek, Hebrew, Arabic, Thai and similar layouts are deliberately excluded, because bundling them would make a Latin passphrase untypeable. If you use one of those, the LUKS prompt is US QWERTY on purpose.

**2. Check that your login password types on a US QWERTY greeter.** This is a separate prompt with a separate bug. Issue [#6880](https://github.com/omacom/omarchy/issues/6880), open since 4.0.0, reports that the SDDM greeter always uses US QWERTY regardless of the system layout, because the greeter runs its own Hyprland instance whose config declares no input block. Issue [#10842](https://github.com/omacom/omarchy/issues/10842) confirms the same on 4.0.2 with Colemak and Russian, and adds that there is no layout indicator and no switcher on the greeter. Both are still open on 4.0.4.

Full detail on both prompts: [non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/) and [layouts and locale](/keyboard/layouts-and-locale/).

**3. Test snapshot rollback before you rely on it.** The manual tells you snapshots are created on every update and restored from the Limine boot menu. Issue [#8047](https://github.com/omacom/omarchy/issues/8047) reports that this does not work on a stock install: `btrfs-overlayfs` is enabled by default, every Snapper snapshot is read-only, so every snapshot boot gets an overlay mounted over `/`, and `limine-snapper-sync` refuses to start because `/` is then no longer a btrfs object. The restore chain dies before it begins. Issue [#9828](https://github.com/omacom/omarchy/issues/9828) adds a second trap: a restore rewinds the root subvolume but not `@home`, and migration markers live in `~/.local/state/omarchy/migrations/`, so migrations are undone while their markers survive and never run again.

Keep an ordinary backup of your home directory. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

## Day one: the setup pass

Run the update first. The ISO is usually a few point releases behind, and the update applies pending migrations that fix earlier bugs.

```bash
omarchy update
```

It requires sudo, creates a snapshot first, and logs to `/tmp/omarchy-update.log`. Confirm it actually printed something: issue [#11630](https://github.com/omacom/omarchy/issues/11630) reports `omarchy update` exiting silently with status 0 on 4.0.3, doing nothing and writing no log. There is an unattended form, `omarchy update -y`. See [before you update checklist](/upgrade/before-you-update-checklist/) and [what migrations do](/upgrade/what-migrations-do/).

Then learn where configuration lives. Omarchy 4.0.0 replaced the old `~/.config/hypr/*.conf` files with Lua. On 4.0.4 the files are `hyprland.lua`, `input.lua`, `monitors.lua`, `bindings.lua` and `looknfeel.lua`. Guides written for 3.x that tell you to edit `hyprland.conf` no longer apply. See [hyprland.conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

Set your session keyboard layout in `~/.config/hypr/input.lua`:

```lua
hl.config({
  input = {
    kb_layout = "us,dk",
    kb_options = "compose:caps,grp:alts_toggle",
  },
})
```

Set displays in `~/.config/hypr/monitors.lua`. The shipped default is one catch-all rule with automatic scale:

```lua
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })
```

List what you actually have with `hyprctl monitors all` before pinning anything. See [multi-monitor](/hardware/multi-monitor/).

## The first 48 hours: what will actually block you

**Screen sharing.** Two open issues. [#11221](https://github.com/omacom/omarchy/issues/11221) reports that the Outputs tab of the share picker renders monitor cards off-screen whenever no output is anchored at x=0 or y=0, so monitors silently vanish from the picker. The reporter traced it to Omarchy shipping `hyprland-preview-share-picker-git` built from a December 2025 commit, before the upstream fix merged in August 2026. Omarchy points at that picker through `custom_picker_binary` in `~/.config/hypr/xdph.conf`. [#10496](https://github.com/omacom/omarchy/issues/10496) reports heavy rendering corruption in Google Meet when you start sharing while another participant is already sharing. Details and workarounds: [screen sharing in Meet, Zoom and Teams](/switch/screen-sharing-meet-zoom-teams/).

**Fractional scaling.** Electron and Chromium apps are the weak point. [#9904](https://github.com/omacom/omarchy/issues/9904) reports the 1Password browser-unlock popup mapping at 402x371 logical pixels while its layout expects roughly 1.6 times that, clipping the password field at scale 1.6. [#9907](https://github.com/omacom/omarchy/issues/9907) reports Electron and Chromium secondary windows leaving stale or duplicated regions at the same scale, and notes it is not specific to 1Password. Both are open. See [fractional scaling and HiDPI apps](/switch/fractional-scaling-hidpi-apps/).

**Printers.** Do not assume plug and play. [#11814](https://github.com/omacom/omarchy/issues/11814) reports an HP Smart Tank 529 over USB where the only option offered is a driverless queue that fails every job with `universal filter failed`, because `hplip` is not shipped on the image. [#11186](https://github.com/omacom/omarchy/issues/11186) reports dropped and blank pages after updating to 4.0.3, traced by the reporter to `libcupsfilters` jumping to 2.2.1-2 while `cups-filters` stayed at 2.0.1-2. See [printers and scanners](/switch/printers-and-scanners/).

**Wi-Fi and Bluetooth around suspend.** [#11377](https://github.com/omacom/omarchy/issues/11377) reports a Broadcom `brcmfmac` adapter wedging NetworkManager and wpa_supplicant into unkillable D-state, which aborts suspend and leaves the machine awake with dead Wi-Fi. [#11264](https://github.com/omacom/omarchy/issues/11264) reports a T2 MacBook Air where Bluetooth never powers on at boot and every suspend fails on a D3 timeout. Both are open. Two commands are worth knowing before you need them:

```bash
omarchy restart wifi
omarchy restart bluetooth
```

Both unblock the radio with `rfkill` and restart the service. See [suspend and sleep](/hardware/suspend-sleep/), [Wi-Fi](/hardware/wifi/) and [Bluetooth](/hardware/bluetooth/).

## What to watch for on newer versions

All fourteen issues cited here were open on 2026-09-16 against 4.0.4. None carries a `fixedIn` release yet, so check each thread before assuming a point release cleared it. The next announced release is Quattro RS 4.5, which has not shipped, and nothing here has been confirmed against it.

If you are coming from 3.x rather than a fresh install, the config format change is the bigger shock than any single bug. Start with [what replaces what](/switch/what-replaces-what/) and [tiling window manager survival](/switch/tiling-window-manager-survival/).

Official references: the [system snapshots chapter](https://omarchy.org/manual/system-snapshots/), the [keyboard, mouse and trackpad chapter](https://omarchy.org/manual/keyboard-mouse-trackpad/), and the [updates chapter](https://omarchy.org/manual/updates/).
