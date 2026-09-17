---
title: "Multi-monitor on Omarchy 4"
description: "What works and what breaks with multi-monitor setups on Omarchy 4.0.4: clamshell handling, per-monitor scaling, wake failures and the fixes that hold."
answer: "Multiple displays work out of the box on 4.0.4. Hyprland auto-arranges them and Omarchy handles lid close, mirroring and DDC brightness. The sore spots are per-monitor scaling and position, which the clamshell watcher re-applies every two seconds, and displays that stay dark after idle wake. Edit ~/.config/hypr/monitors.lua with connector-name rules rather than the Display panel."
appliesTo:
  from: "4.0.0"
kind: component
componentKey: "multi-monitor"
status: info
issueCount: 1132
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [multi-monitor, displays, scaling, clamshell, hyprland]
sources:
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/pull/7581"
    title: "PR #7581: Leave an auto-scaled internal panel alone in clamshell recovery"
    kind: pr
    author: "fuchsblau"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/6909"
    title: "Issue #6909: [Quattro] eDP-1 monitor scaling forces 2x reset on mixed-monitor array with Quickshell navbar"
    kind: issue
    author: "PedroMiguelInacio"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/6673"
    title: "Issue #6673: [Quattro] Display panel scale is per-monitor at runtime but persists globally, rescaling other monitors on reload"
    kind: issue
    author: "nico-kovacs"
    date: "2026-08-10"
  - url: "https://github.com/omacom/omarchy/issues/7084"
    title: "Issue #7084: Clamshell watcher ignores desc: rules for the internal panel and overwrites its scale every 2s"
    kind: issue
    author: "mkelk"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7326"
    title: "Issue #7326: Internal monitor position cannot be made to stick: clamshell watcher and Display panel scaling both re-apply position = \"auto\""
    kind: issue
    author: "skoom21"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/8103"
    title: "Issue #8103: omarchy-hyprland-monitor-scaling doesn't persist scale on outputs with explicit per-monitor rules in monitors.lua"
    kind: issue
    author: "RonRayReed"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/12147"
    title: "Issue #12147: LG display stays off after wake: dpmsStatus desyncs true while panel has no signal"
    kind: issue
    author: "SykesTheLord"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12152"
    title: "Issue #12152: External-only HDMI display becomes unusable after idle lock/DPMS wake with eDP-1 disabled"
    kind: issue
    author: "dudis"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12207"
    title: "Issue #12207: linux-omarchy 7.2.5 (xe, Panther Lake): USB4 monitor's EDID read fails on about half of hotplugs"
    kind: issue
    author: "diazkev314"
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/12180"
    title: "Issue #12180: Black screen / full hang on unlock after idle screensaver: lock surface fails to attach"
    kind: issue
    author: "socalest1977"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12208"
    title: "Issue #12208: Lock screen dies during HDMI/display thrash, Hyprland lockscreen failsafe loop"
    kind: issue
    author: "qaz027"
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/12188"
    title: "Issue #12188: linux-omarchy kernel breaks screen backlight and USB audio volume on Dell XPS 14 (Panther Lake)"
    kind: issue
    author: "cthybert"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12083"
    title: "Issue #12083: 4K@120 HDMI screen blanks for seconds on every new frame after linux-omarchy 7.2.5-3 (AMD Navi 33)"
    kind: issue
    author: "berkesadam74"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12192"
    title: "Issue #12192: System-update icon only appears on one monitor (checkupdates race)"
    kind: issue
    author: "loraque-git"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12198"
    title: "Issue #12198: Update icon appears on only one monitor: concurrent omarchy-update-available runs race inside checkupdates"
    kind: issue
    author: "kevinbsr"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9804"
    title: "Issue #9804: Quickshell crashes with SIGSEGV in QSGRenderThread when Hyprland monitor is set to 10-bit"
    kind: issue
    author: "ozdil"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/2858"
    title: "Issue #2858: Add a better display configuration tool"
    kind: issue
    author: "revan1611"
    date: "2025-10-26"
  - url: "https://github.com/omacom/omarchy/issues/427"
    title: "Issue #427: Disable Internal (Laptop) Display on Lid Close"
    kind: issue
    author: "curtisspendlove"
    date: "2025-07-31"
  - url: "https://github.com/omacom/omarchy/pull/2394"
    title: "PR #2394: fix: prevent Chromium crash when moving windows between monitors"
    kind: pr
    author: "d-cas"
    date: "2025-10-14"
credits:
  - name: "fuchsblau"
    url: "https://github.com/fuchsblau"
    for: "Traced and fixed the internal panel scale flapping to 2x on every idle wake"
  - name: "mkelk"
    url: "https://github.com/mkelk"
    for: "Found that the clamshell watcher cannot read desc: keyed monitor rules"
  - name: "nico-kovacs"
    url: "https://github.com/nico-kovacs"
    for: "Showed that the Display panel scale persists globally and rescales other monitors"
  - name: "dudis"
    url: "https://github.com/dudis"
    for: "Traced dead external-only output after wake to an Aquamarine 0.15.0 CRTC regression"
  - name: "diazkev314"
    url: "https://github.com/diazkev314"
    for: "Captured the failing USB4 EDID read with drm.debug and a working re-probe workaround"
  - name: "SykesTheLord"
    url: "https://github.com/SykesTheLord"
    for: "Identified the dpmsStatus desync that makes a wake skip a dark monitor"
faq:
  - q: "Why does my monitor scale snap back a second after I change it?"
    a: "The clamshell watcher re-applies the internal panel every two seconds while an external monitor is active, and the scaling command only writes back to monitors.lua when the file still has Omarchy's generic catch-all. Issues #8103 and #7084 cover this. Edit the rule in monitors.lua directly instead."
  - q: "Does Omarchy ship a GUI for arranging monitors?"
    a: "Not for arrangement. The Display panel on Super + Ctrl + D does brightness, text size, scale and enable or disable only. Issue #2858 was closed as completed without an arrangement tool, so positions still go in ~/.config/hypr/monitors.lua."
  - q: "My laptop screen stays on when I close the lid. What changed?"
    a: "Nothing on 4.x should need the manual bindl lines from issue #427. Omarchy disables the internal panel itself when the lid shuts and an external output is active. If it does not, check that an external monitor is really enabled in hyprctl monitors, since the internal panel is never disabled as the only display."
related: [multi-monitor-layout-not-saved, fractional-scaling-blurry-or-huge-apps, monitors-conf-replaced-by-monitors-lua, hybrid-gpu, suspend-sleep]
draft: false
---

## Status on 4.0.4

Two or more displays work on Omarchy 4.0.4 without any configuration. Hyprland detects each output, brings it up at its preferred mode and places it automatically, and the Quickshell bar appears on every monitor. This page was checked against the v4.0.4 source tree, the 4.0.0 through 4.0.4 release notes and open issues as of 2026-09-16.

The problems are not with getting a picture. They are with making a layout stay put, and with monitors that go dark after an idle cycle and never come back. The displays and multi-monitor component carries 1132 issues in the tracking data, and the 4.x ones cluster tightly on those two themes.

On 3.x you edited `~/.config/hypr/monitors.conf` with `monitor=` lines. Since 4.0.0 that file is `monitors.lua` and the rules are `hl.monitor({ ... })` calls. Old guides that tell you to paste `monitor=eDP-1, preferred, auto, 2` do not apply. See [monitors.conf replaced by monitors.lua](/fix/monitors-conf-replaced-by-monitors-lua/).

## What Omarchy does automatically

The shipped `~/.config/hypr/monitors.lua` contains one catch-all rule, `hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })`, with `omarchy_monitor_scale` set to `"auto"` and `GDK_SCALE` set to 2. Everything else is machinery around it:

- **Clamshell.** `switch:off:Lid Switch` runs `omarchy-hyprland-monitor-clamshell`, which disables the internal panel when the lid shuts and an external output is active, and re-enables it at the remembered scale when you open it. This replaced the hand-written `bindl` lid switches people were copying from issue #427 for a year.
- **A monitor watcher.** `omarchy-hyprland-monitor-watch` subscribes to Hyprland's event socket, reconciles clamshell state on `monitoradded` and `monitorremoved`, and polls every two seconds while a laptop is docked as a backstop for drift across suspend.
- **Modeless recovery.** A display that was powered off at boot answers with a partial EDID and comes up at 0x0. Powering it on fires no DRM hotplug, so 4.0.0 added `omarchy-hyprland-monitor-modeless` plus a backing-off reload loop that recovers it without a reboot.
- **Toggle recovery.** A systemd user service runs `omarchy-hw-recover-internal-monitor` before the graphical session and clears a stale internal-disable toggle if no external display is connected, so you cannot boot undocked into a disabled laptop screen.
- **Mirroring and toggles.** `Super + Ctrl + Delete` toggles the laptop display, `Super + Ctrl + Alt + Delete` mirrors it to the first external output. Both refuse unsafe connector names and refuse to disable your only display.
- **Scaling.** `Super + /` and `Super + Alt + /` step through 1, 1.25, 1.6, 2, 3 and 4, rounded up to a scale Hyprland accepts in 1/120 steps. `omarchy display text size` moves shell, GTK and terminal text together without touching monitor scale.
- **External brightness.** Brightness keys drive the focused display. External monitors that speak DDC/CI are adjusted through `ddcutil`, Apple Studio and XDR displays through `asdcontrol`, and laptop panels through the kernel backlight picked by `omarchy-hw-display`.
- **Panel quirks.** `fix-asus-ptl-b9406-display.sh` adds `xe.enable_panel_replay=0` on the ASUS ExpertBook B9406, where Panel Replay latches the last frame and the screen only updates on a full modeset. `fix-nouveau-cursor.sh` forces software cursors on nouveau, where the hardware cursor plane is invisible. `xps13-text-scaling.sh` drops text size to 11 on the 2026 XPS 13.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#6909](https://github.com/omacom/omarchy/issues/6909) internal panel scale snaps to 2x on every idle wake | Laptops on stock `scale = "auto"` with an external monitor | Fixed by [#7581](https://github.com/omacom/omarchy/pull/7581) | 4.0.1 |
| [#7084](https://github.com/omacom/omarchy/issues/7084) clamshell watcher ignores `desc:` keyed rules and overwrites the scale every 2s | Any docked laptop using description-keyed rules | Open | |
| [#8103](https://github.com/omacom/omarchy/issues/8103) scale changes not persisted when `monitors.lua` has explicit per-output rules | Dell Latitude 7420 and any laptop plus external | Open | |
| [#6673](https://github.com/omacom/omarchy/issues/6673) Display panel scale is per-monitor live but persists globally, rescaling the others | Three-display AMD Ryzen AI 9 setup, any mixed-DPI array | Open | |
| [#7326](https://github.com/omacom/omarchy/issues/7326) internal monitor position forced back to `auto` | Dell Latitude E5470, any laptop plus external | Open | |
| [#12147](https://github.com/omacom/omarchy/issues/12147) monitor stays dark after wake because `dpmsStatus` desyncs to true | Hybrid Intel plus NVIDIA, LG HDR 4K on DP | Open | |
| [#12152](https://github.com/omacom/omarchy/issues/12152) external-only output unusable after idle wake, atomic commits fail with EINVAL | Dell Vostro 5470, i915 plus nouveau | Open, Aquamarine fix upstream | |
| [#12180](https://github.com/omacom/omarchy/issues/12180) lock surface not backed by a valid wayland output, black screen then hard freeze | Intel UHD 630 | Open | |
| [#12208](https://github.com/omacom/omarchy/issues/12208) lockscreen failsafe loop during HDMI thrash | AMD Phoenix1 with Dell U2719DX on HDMI | Open | |
| [#12207](https://github.com/omacom/omarchy/issues/12207) USB4 monitor EDID read fails on about half of hotplugs, stuck at 640x480 | Dell XPS 16 DA16260, Panther Lake with `xe` | Open | |
| [#12083](https://github.com/omacom/omarchy/issues/12083) 4K at 120 Hz blanks for seconds on every frame after a pause | AMD Navi 33 on HDMI 2.1 | Open | |
| [#9804](https://github.com/omacom/omarchy/issues/9804) Quickshell SIGSEGV when a monitor is set to `bitdepth = 10` | NVIDIA RTX 4060 laptop with OLED external | Open | |
| [#12192](https://github.com/omacom/omarchy/issues/12192) and [#12198](https://github.com/omacom/omarchy/issues/12198) update icon appears on one bar only | Any multi-monitor machine | Open | |
| [#2184](https://github.com/omacom/omarchy/issues/2184) Chromium crashes when moved between monitors | All, 3.x era | Fixed by [#2394](https://github.com/omacom/omarchy/pull/2394) | 3.x |

## Fixes that work

Work down this list in order.

1. **Put your layout in `monitors.lua`, keyed by connector name.** Open it with _Setup > Monitors_ in the Omarchy menu. Use `hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 2 })` and a matching line per output. Connector names come from `hyprctl monitors`. Do not use `desc:` for the internal panel on a laptop: the clamshell watcher cannot read those rules and will fight you every two seconds (#7084).
2. **If a scale will not stick, stop using the panel and the hotkeys.** Edit the value in `monitors.lua` and reload. Both #8103 and #6673 come from the same gap: the live change and the file disagree, and the docked poller re-asserts the file. Editing the file removes the mismatch.
3. **A display that is dark after wake usually needs a real state transition.** Run `hyprctl dispatch 'hl.dsp.dpms({ action = "disable" })'` then the same with `"enable"`. The wake path skips the enable when every monitor already claims to be on, which is exactly the stuck state (#12147).
4. **If that does nothing, switch VT and back.** `Ctrl + Alt + F2` then `Ctrl + Alt + F1` forces a full modeset and recovered the output for the reporters of both #12152 and #12208. Treat it as a workaround, not a fix.
5. **A monitor stuck at 640x480 has a bad EDID read.** Check `cat /sys/class/drm/card*-DP-1/edid | wc -c`. If it is empty, re-probe with `echo off | sudo tee /sys/class/drm/card0-DP-1/status` then `echo detect`, wait a few seconds, and the full EDID comes back (#12207).
6. **If display trouble started with 4.0.4, suspect the kernel.** 4.0.4 shipped `linux-omarchy` to everyone. Boot the stock `linux` entry once from the Limine menu and compare. That is how #12083 and #12188 were isolated.
7. **Chromium crashing on a monitor move is already handled.** `--disable-features=WaylandWpColorManagerV1` ships in the default flag files. If you replaced them, put it back.

## Report it

Collect a bundle with `omarchy-debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, dmesg, this boot's warnings and errors, and the package list. Use `omarchy-debug --no-sudo` to skip dmesg, and `--print` to print instead of upload. Two reporters on 4.0.4, in #12147 and #12207, found that `omarchy debug` through the CLI wrapper was not available on their install, so run the hyphenated command directly.

For a display bug, add these by hand, since the debug log does not carry them:

- `hyprctl monitors all -j`, which shows disabled outputs, mirrors, scale and `dpmsStatus`.
- The connector state: `cat /sys/class/drm/card*-*/status` and the size of the matching `edid` file.
- Your `~/.config/hypr/monitors.lua`.
- The Hyprland log lines around the failure. `atomic drm request: failed to commit: Invalid argument` is the signature of the Aquamarine and kernel modeset failures behind several of the open wake bugs.
- Whether the same thing happens on the stock `linux` kernel.

Say which connector, which monitor make and model, and whether the machine was docked. Half the open reports above were diagnosable only because the reporter said that much. If you have a machine that works well, add it at [hardware submit](/hardware/submit/).

## Related

- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [monitors.conf replaced by monitors.lua](/fix/monitors-conf-replaced-by-monitors-lua/)
- [Fractional scaling blurry or huge apps](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Hybrid GPU laptops](/hardware/hybrid-gpu/) and [suspend and sleep](/hardware/suspend-sleep/)
- [Thunderbolt docks](/hardware/thunderbolt-dock/)
- [Lock screen will not unlock](/fix/lock-screen-wont-unlock/) and [black screen after login](/fix/black-screen-after-login/)
- Official manual chapter on [monitors](https://omarchy.org/manual/monitors/)
