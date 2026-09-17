---
title: "Apps blurry or huge with fractional scaling on Omarchy"
description: "Fractional scaling on Omarchy 4 leaves GTK, Electron and XWayland apps oversized or soft. Fix the monitor scale, GDK_SCALE, text scaling and per-app flags."
answer: "Set the monitor scale in ~/.config/hypr/monitors.lua (omarchy_monitor_scale) and set omarchy_gdk_scale to the nearest whole number, then restart the oversized apps. If apps launched from the menu keep the old size, run dbus-update-activation-environment --systemd GDK_SCALE=N. For Electron dialogs that clip, run omarchy display text size reset or add --force-device-scale-factor=1."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 101
errorStrings:
  - "Size must be an integer between 9 and 20 (px)."
  - "gtk text-scaling-factor:"
tags: [scaling, display, hyprland, electron, gtk, xwayland]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7021"
    title: "Issue #7021: GDK_SCALE=2 + force_zero_scaling overflows XWayland/Java windows on auto-scaled 1080p"
    kind: issue
    author: "v-t-r-gg"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/10555"
    title: "Issue #10555: Monitor scaling changes leave GDK_SCALE stale in the app-launch environment"
    kind: issue
    author: "Geokec"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/pull/10570"
    title: "PR #10570: Sync GDK_SCALE into the activation environment on scale change"
    kind: pr
    author: "fresh3nough"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/8574"
    title: "Issue #8574: omarchy display text size breaks 1Password's fixed-size dialogs (root cause of #2016)"
    kind: issue
    author: "SilentKernel"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/pull/8575"
    title: "PR #8575: Keep GNOME text scaling from clipping 1Password's fixed-size dialogs"
    kind: pr
    author: "SilentKernel"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/pull/8825"
    title: "PR #8825: Add --no-gtk option to display text size command"
    kind: pr
    author: "pazthor"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/8716"
    title: "Issue #8716: Text size below default shrinks Electron surfaces inside Hyprland windows"
    kind: issue
    author: "jonnyace"
    date: "2026-08-28"
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
  - url: "https://github.com/omacom/omarchy/issues/11175"
    title: "Issue #11175: Spotify is oversized on mixed-DPI setups: ship spotify-flags.conf with --ozone-platform=wayland"
    kind: issue
    author: "jamers99"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/9950"
    title: "Issue #9950: Display panel's scale presets silently no-op when monitors.lua has explicit per-output hl.monitor lines"
    kind: issue
    author: "isaac30503"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/2058"
    title: "Issue #2058: Steam window too small on a 4k monitor with fractional scalling"
    kind: issue
    author: "colutti"
    date: "2025-09-29"
  - url: "https://github.com/omacom/omarchy/issues/3309"
    title: "Issue #3309: Spotify does not scale right"
    kind: issue
    author: "nightdevil00"
    date: "2025-11-10"
  - url: "https://github.com/omacom/omarchy/issues/1847"
    title: "Issue #1847: (Qt) apps blurry after re-opening laptop lid"
    kind: issue
    author: "michaelshmitty"
    date: "2025-09-21"
  - url: "https://github.com/omacom/omarchy/issues/7676"
    title: "Issue #7676: Chromium profile menu renders as a clipped sliver when the window is wide (external 4K display)"
    kind: issue
    author: "ktaraszk"
    date: "2026-08-21"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
credits:
  - name: "SilentKernel"
    url: "https://github.com/SilentKernel"
    for: "Measured how GNOME text scaling multiplies into Chromium's device pixel ratio and clips fixed-size dialogs"
  - name: "v-t-r-gg"
    url: "https://github.com/v-t-r-gg"
    for: "Traced the three-way disagreement between Hyprland scale, force_zero_scaling and GDK_SCALE on XWayland"
  - name: "Geokec"
    url: "https://github.com/Geokec"
    for: "Found the stale GDK_SCALE in the systemd user activation environment and a working refresh command"
  - name: "kurtome"
    url: "https://github.com/kurtome"
    for: "Documented the 1Password popup at scale 1.6 and the force-device-scale-factor workaround"
  - name: "jamers99"
    url: "https://github.com/jamers99"
    for: "Showed that Spotify is still on XWayland and cannot follow per-output scale"
faq:
  - q: "Why does Omarchy default to GDK_SCALE=2?"
    a: "Omarchy targets retina-class panels. The shipped ~/.config/hypr/monitors.lua sets omarchy_gdk_scale = 2 and omarchy_monitor_scale = \"auto\". On a 1080p or 1440p screen both should be 1."
  - q: "Can GDK_SCALE be fractional?"
    a: "No. GTK only honours whole numbers, which is why the monitor scale can be 1.6 while GDK_SCALE has to be 1 or 2. Omarchy's scaling command persists int(scale + 0.5)."
  - q: "Does changing the scale need a reboot?"
    a: "No, but apps already running keep their old scale. Quit and relaunch anything that looks wrong, or close everything with Ctrl + Alt + Del."
related: [monitors-conf-replaced-by-monitors-lua, multi-monitor-layout-not-saved, 1password-not-opening-or-wrong-scale, where-did-waybar-go]
draft: false
---

Omarchy ships assuming a 2x retina panel. On anything else you end up picking a fractional monitor scale, and then some apps look right, some look enormous, and some look soft. Checked on 4.0.4, with the 4.0.0 to 4.0.3 behaviour noted where it differs.

## The fix

**1. Set the monitor scale.** Print the focused monitor's scale with `omarchy hyprland monitor scaling`, or see every output with `hyprctl monitors -j | jq '.[] | {name, width, height, scale}'`. Step through the presets with `Super + /` (up) and `Super + Alt + /` (down), or set one directly:

```bash
omarchy hyprland monitor scaling 1.6
```

The presets in 4.0.x are 1, 1.25, 1.6, 2, 3 and 4. Hyprland only accepts scales that divide the mode into whole logical pixels in 1/120 steps, so the command rounds your request up to the nearest clean value. That is why asking for 1.5 on some panels lands you somewhere else.

**2. Match GDK_SCALE to it.** Open `~/.config/hypr/monitors.lua` (Setup > Monitors in the Omarchy menu). The stock file has two variables:

```lua
local omarchy_gdk_scale = 2
local omarchy_monitor_scale = "auto"
```

GTK only honours whole numbers, so set `omarchy_gdk_scale` to the nearest integer of your monitor scale: 1 for 1 and 1.25, 2 for 1.6 and 2. Save, then quit and relaunch every oversized window. GDK_SCALE is read at launch, not live. On 3.x the same two knobs live in `~/.config/hypr/monitors.conf` as `env = GDK_SCALE,2` and a `monitor=,preferred,auto,auto` line.

**3. Refresh the launch environment.** If apps started from the menu or a keybinding still come up at the old size after a scale change, the systemd user manager is still exporting the old value. Check and fix it:

```bash
systemctl --user show-environment | grep GDK_SCALE
dbus-update-activation-environment --systemd GDK_SCALE=1
```

Geokec reported this on 4.0.2 with Spotify (issue #10555). The environment import runs on Hyprland start only, so a mid-session scale change never reaches it. PR #10570 adds the sync to the scaling command; it was still open when 4.0.4 shipped, so keep the command handy.

**4. Leave the text-size knob alone while you debug.** `omarchy display text size <9-20>` moves the shell font, the GTK `text-scaling-factor` and your terminal point size together. Chromium and Electron multiply that GTK factor into their own device pixel ratio, so anything other than the default 12 changes how Electron apps lay out. Reset it with:

```bash
omarchy display text size reset
```

Above 12 the factor clips fixed-size Electron dialogs, measured by SilentKernel at a device pixel ratio of 2.72 on a 2x monitor at text size 16 (issue #8574). Below 12 the whole Electron surface undershoots the Hyprland window and leaves wallpaper showing, reported by jonnyace at text size 10 (issue #8716). PR #8825 proposes a `--no-gtk` flag so the bar slider stops touching GTK; both it and PR #8575 were still open at 4.0.4.

**5. Per-app flags for the stragglers.** 1Password was fixed in 4.0.3: `omarchy-launch-1password` now runs `1password --force-device-scale-factor=1`, listed in the release notes as "Fix oversized 1Password windows on scaled displays". For other Electron apps with clipped or oversized windows, the same flag goes in `~/.config/<app>-flags.conf`, one flag per line. Spotify still runs on XWayland, which is why it ignores per-output scale on mixed-DPI setups (issue #11175). Create `~/.config/spotify-flags.conf`:

```
--ozone-platform=wayland
```

That is the same fix nightdevil00 posted for 3.x in issue #3309. Omarchy does not ship this file on 4.0.4; it ships `chromium-flags.conf` only, which its browser installer copies for each Chromium-based browser.

**6. Repaint corruption at 1.6.** If Electron secondary windows leave stale or duplicated regions at a fractional scale, d-geula found that disabling one Chromium feature clears it (issue #9907):

```
--disable-features=WaylandFractionalScaleV1
```

## Verify it worked

Run these after relaunching the affected app.

```bash
omarchy hyprland monitor scaling            # focused monitor scale
omarchy display text size                   # px, gtk text-scaling-factor, terminal pt
systemctl --user show-environment | grep GDK_SCALE
hyprctl clients -j | jq '.[] | {class, xwayland}'
```

The text-size command should report `12`, `1.0` and `9 pt` on a stock system. Anything listed with `"xwayland": true` will not follow per-output scale, so judge it separately. In a Chromium window, the devtools console reporting `window.devicePixelRatio` should equal your monitor scale, not the scale times the text factor.

## Why it happens

Three scaling layers stack, and they do not agree.

Hyprland gives native Wayland clients a fractional output scale, and they re-render for it. GTK's `GDK_SCALE` is an integer multiplier applied at app launch. GNOME's `text-scaling-factor`, which the Omarchy text-size knob drives, is a third multiplier that Chromium and Electron fold into their device pixel ratio.

On top of that, `default/hypr/envs.lua` sets `xwayland.force_zero_scaling = true`. XWayland clients therefore get 1:1 physical pixels and have to enlarge themselves through toolkit settings. That keeps them sharp instead of compositor-upscaled, but it means an X11 or Java app sees a 1920 wide screen and a `GDK_SCALE` of 2 at the same time, and asks for windows twice as wide as it needs. v-t-r-gg measured a client advertising a 1530px minimum width where 765 was correct (issue #7021). Going the other way, forcing `--force-device-scale-factor=1` on a scaled monitor makes the app render at 1x and the compositor upscale it, so text goes softer. kurtome flagged that trade-off in issue #9904.

## If that did not work

The scale presets silently do nothing if you have written explicit per-output `hl.monitor` lines in `monitors.lua`. The scaling command persists a single global variable, so the file reload undoes its own live change (issue #9950). Per-monitor scaling and the bar's Display panel are effectively mutually exclusive on 4.0.x.

Two failures look like scaling but are not. A Chromium profile bubble that opens as a thin clipped sliver is triggered by the window's logical width, not the scale, and reproduces at integer scale 1 as well (issue #7676). Qt apps that go blurry only after closing and reopening the laptop lid look like an output hotplug bug rather than a configuration problem, and that report has been open since 3.x with no fix (issue #1847).

Evidence is thin for mixed-DPI multi-monitor setups generally. Several reports overlap, none has a merged fix as of 4.0.4, and the honest answer today is to pick one scale that is least wrong for the monitor you use most.

## Related

- [Monitor layout lost after Quattro](/fix/monitors-conf-replaced-by-monitors-lua/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [1Password not opening or wrong scale](/fix/1password-not-opening-or-wrong-scale/)
- [Multi-monitor hardware notes](/hardware/multi-monitor/)
- [Fractional scaling and HiDPI apps when switching](/switch/fractional-scaling-hidpi-apps/)
- [omarchy-display-text-size](/reference/commands/omarchy-display-text-size/)
- Official manual chapter: [Monitors](https://omarchy.org/manual/monitors/)
