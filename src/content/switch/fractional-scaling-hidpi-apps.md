---
title: "Fractional scaling and HiDPI apps on Omarchy"
description: "How to set fractional scaling on Omarchy 4.x in monitors.lua, why Electron, Chromium and XWayland apps look blurry or oversized, and what to do about each."
answer: "Omarchy ships GDK_SCALE=2 and monitor scale \"auto\". On a 4K 27-inch or 32-inch panel, open Setup > Monitors and set omarchy_monitor_scale to 1.6; on 1080p or 1440p set both it and omarchy_gdk_scale to 1. Wayland apps follow immediately. Electron, Chromium and XWayland apps need per-app flags and a restart."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [scaling, hidpi, monitors, hyprland, electron, xwayland]
sources:
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy Manual: Monitors"
    kind: manual
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
  - url: "https://github.com/omacom/omarchy/issues/7505"
    title: "Issue #7505: omarchy hyprland monitor scaling replaces scale = \"auto\" with one global value, binding every monitor to the last-adjusted scale"
    kind: issue
    author: "ocewers"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/10555"
    title: "Issue #10555: Monitor scaling changes leave GDK_SCALE stale in the app-launch environment"
    kind: issue
    author: "Geokec"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/7021"
    title: "Issue #7021: GDK_SCALE=2 + force_zero_scaling overflows XWayland/Java windows on auto-scaled 1080p"
    kind: issue
    author: "v-t-r-gg"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/11175"
    title: "Issue #11175: Spotify is oversized on mixed-DPI setups: ship spotify-flags.conf with --ozone-platform=wayland"
    kind: issue
    author: "jamers99"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/8574"
    title: "Issue #8574: `omarchy display text size` breaks 1Password's fixed-size dialogs (root cause of #2016)"
    kind: issue
    author: "SilentKernel"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/6911"
    title: "Issue #6911: Quattro upgrade replaces customized monitors.conf with default monitors.lua (auto layout, GDK_SCALE=2) without porting or warning"
    kind: issue
    author: "daventhedude"
    date: "2026-08-15"
credits:
  - name: "kurtome"
    url: "https://github.com/kurtome"
    for: "Found that --force-device-scale-factor=1 makes the 1Password unlock popup usable at fractional scale"
  - name: "d-geula"
    url: "https://github.com/d-geula"
    for: "Isolated the Electron repaint corruption at scale 1.6 to Chromium's WaylandFractionalScaleV1"
  - name: "Geokec"
    url: "https://github.com/Geokec"
    for: "Showed that the systemd user environment keeps a stale GDK_SCALE after a scale change"
  - name: "jamers99"
    url: "https://github.com/jamers99"
    for: "Traced Spotify's mixed-DPI sizing to it still running on XWayland"
faq:
  - q: "What scale should I use on a 27-inch 4K monitor?"
    a: "1.6 is the value the Omarchy manual recommends for 27-inch and 32-inch 4K panels. Keep omarchy_gdk_scale at 2, because GTK only honours whole numbers and 2 is the nearest integer."
  - q: "Why is everything huge after installing Omarchy on a 1080p laptop?"
    a: "Omarchy assumes a retina-class 2x display and ships GDK_SCALE=2. On a 1080p or 1440p panel, set both omarchy_gdk_scale and omarchy_monitor_scale to 1 in ~/.config/hypr/monitors.lua, then restart the oversized apps."
  - q: "Can I give two monitors different scales?"
    a: "Yes, with explicit hl.monitor lines per output. Do not use the Super + / shortcut to do it: issue #7505 reports that the scaling command rewrites the single shared omarchy_monitor_scale value, so the last monitor you adjusted binds all of them."
  - q: "Does fractional scaling make text blurry on Omarchy?"
    a: "Native Wayland apps render sharp at fractional scale. XWayland apps stay sharp too, because Omarchy sets xwayland force_zero_scaling and they draw 1:1 on physical pixels, but they are sized by the integer GDK_SCALE rather than the monitor scale, so they come out too big or too small. Softness only appears in apps you launch with --force-device-scale-factor=1, which render at 1x and get upscaled."
related: [fractional-scaling-blurry-or-huge-apps, monitors-conf-replaced-by-monitors-lua, what-replaces-what, day-one-checklist]
draft: false
---

Omarchy's defaults are tuned for a retina-class 2x display. The shipped `~/.config/hypr/monitors.lua` sets `GDK_SCALE` to 2 and leaves the Hyprland monitor scale on `"auto"`. On a 2x panel that is right. On a 4K 27-inch monitor, a 1080p laptop, or an ultrawide, it is not, and the first thing you notice after switching from macOS or Windows is that some windows are the wrong size while others are fine.

This page was checked against Omarchy 4.0.4. The official reference is the [Monitors chapter of the manual](https://omarchy.org/manual/monitors/).

## Set the monitor scale

1. Open the config from the Omarchy menu, under *Setup > Monitors*. That opens `~/.config/hypr/monitors.lua` in your editor.
2. Edit the two variables at the top. For a 27-inch or 32-inch 4K panel:

```lua
local omarchy_gdk_scale = 2
local omarchy_monitor_scale = 1.6
```

For 1080p, 1440p, or an ultrawide like 3440x1440:

```lua
local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1
```

3. Save. Hyprland picks the monitor scale up on reload. `GDK_SCALE` only reaches apps started afterwards, so quit anything that still looks oversized, or close everything with `Ctrl + Alt + Del`.

To try values before committing, step through the presets with `Super + /` to go up and `Super + Alt + /` to go down. Those run `omarchy hyprland monitor scaling`, which walks 1, 1.25, 1.6, 2, 3 and 4, applies the value to the focused output, and writes it back to `monitors.lua` so it survives a reboot.

Two things about that command are worth knowing. It rounds your requested scale up to the nearest value where the panel's mode divides into whole logical pixels, in steps of 1/120, so 1.5 on some panels lands somewhere else. And it persists `GDK_SCALE` as the nearest integer of the monitor scale, because GTK ignores fractional values there.

## Verify it worked

```bash
hyprctl monitors all | grep -E 'Monitor|scale'
systemctl --user show-environment | grep GDK_SCALE
```

The first command shows the scale Hyprland actually applied per output, which is what `"auto"` resolved to if you left it alone. The second shows what new apps will inherit. If those two disagree with `monitors.lua`, see the last section.

## Which apps still look wrong

Native Wayland GTK and Qt apps handle fractional scale well. The problems cluster in three places.

**XWayland apps.** Omarchy sets `xwayland { force_zero_scaling = true }` in `default/hypr/envs.lua`, which it also did in 3.x. X11 clients therefore see the full physical resolution and draw 1:1 on real pixels. That keeps them sharp, but it means they are not sized by the monitor scale at all. They size themselves from `GDK_SCALE`, which is a whole number and the same for every output, so at 1.6 they come out 25 percent too big, at 1.25 too small, and on mixed-DPI setups there is no value that suits both screens. Of the apps Omarchy installs for you, Spotify is the one still on XWayland: issue #11175 describes it sized for the 1.6 laptop panel and oversized on 1x externals, and proposes shipping a `spotify-flags.conf` with `--ozone-platform=wayland`. As of 4.0.4 no such file ships, and `omarchy-launch-spotify` runs `/usr/bin/spotify` with no flags. Chromium is fine here because Omarchy does ship `~/.config/chromium-flags.conf` with `--ozone-platform=wayland`.

**Java and X11-only toolkits.** Issue #7021 describes the combination that bites: `GDK_SCALE=2` plus zero XWayland scaling means a Swing or AWT window asks for twice its 1x minimum size against a full-resolution X screen, and on a 1080p panel the window hangs off the edge. Override the variable for that one process rather than globally. The reporter's line also covers the Java-side scale hint:

```bash
GDK_SCALE=1 GDK_DPI_SCALE=1 JAVA_TOOL_OPTIONS=-Dsun.java2d.uiScale=1 your-java-app
```

**Electron and Chromium at fractional scale.** Two separate reports. Issue #9904 found that the 1Password browser-unlock popup maps at a size that does not match its own layout at scale 1.6, clipping the password field, and that launching with `--force-device-scale-factor=1` makes it usable. Omarchy 4.0.3 added the same flag to `bin/omarchy-launch-1password`, which now runs `1password --force-device-scale-factor=1`; the comment in that script cites oversized 1Password windows on scaled monitors as the reason. The trade is softness, because the app renders at 1x and gets upscaled. Issue #9907 is a different defect, stale and duplicated regions in Electron secondary windows at scale 1.6, and the reporter's workaround is to disable one Chromium feature:

```bash
/opt/1Password/1password --disable-features=WaylandFractionalScaleV1
```

Both issues were open on 2026-09-16. Add flags like these to an app's own `*-flags.conf` in `~/.config/`, or to a copy of its `.desktop` file in `~/.local/share/applications/`, rather than globally.

## Per-monitor and mixed-DPI setups

The shipped catch-all line applies one scale to every output:

```lua
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
```

For a laptop plus an external of different DPI, write explicit lines instead:

```lua
hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 1.6 })
hl.monitor({ output = "DP-1", mode = "3440x1440@60", position = "auto", scale = 1 })
```

Get the output names and supported modes from `hyprctl monitors all`. Then stop using `Super + /`: issue #7505 reports that the first manual adjustment overwrites `omarchy_monitor_scale`, replacing `"auto"` with one number that then binds every output, with no way back to `"auto"` short of editing the file.

`GDK_SCALE` is still a single session-wide value, so on a mixed-DPI pair there is no correct setting for the XWayland apps that read it. Pick the integer that suits the monitor you work on most.

## Text without changing the scale

If everything is the right size and only the text is too small, do not touch the scale. Omarchy 4.x added one knob:

```bash
omarchy display text size 14
```

It accepts a pixel size from 9 to 20 and changes three things in lockstep: the Omarchy shell font, GTK's `text-scaling-factor`, and the point size in your terminal config. `omarchy display text size reset` returns to the 12px default. Foot has no reload signal, so an already-open Foot window stays at the old size; new windows pick the change up.

One caveat: issue #8574 reports that Chromium and Electron multiply GTK's text-scaling factor into their device scale factor, so fixed-size dialogs such as the 1Password SSH authorization prompt lose content off the edge at larger text sizes. If a dialog is clipped, try the default text size before blaming the monitor scale.

## If that did not work

If `monitors.lua` says one thing and apps behave as though the old scale is still set, check the launch environment. Issue #10555 reports `systemctl --user show-environment` still holding `GDK_SCALE=2` after the scale was lowered to 1, because the environment import runs at session start only. The reporter's confirmed workaround:

```bash
dbus-update-activation-environment --systemd GDK_SCALE=1
```

Then relaunch the affected app. Logging out and back in has the same effect. A fix that runs that sync after every scale change was proposed in [PR #10570](https://github.com/omacom/omarchy/pull/10570), still open on 2026-09-16.

If you upgraded from 3.x and your display layout came back wrong, that is expected rather than mysterious. Issue #6911 reports that the Quattro upgrade writes the stock `monitors.lua` and stops loading your customised `monitors.conf`, without backing it up or mentioning it. The old file is still on disk at `~/.config/hypr/monitors.conf`. Read your old `monitor=` and `env = GDK_SCALE,` lines out of it and port them into `hl.monitor` and `hl.env` calls by hand. See [monitors.conf replaced by monitors.lua](/fix/monitors-conf-replaced-by-monitors-lua/) for a worked example and [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) for the general mapping.

## What to watch for on newer versions

The 1Password window rule still tags every 1Password window as floating in 4.0.4, which issue #9904 argues applies a size rule to a popup that cannot be resized. The development branch for the announced "Quattro RS 4.5" release fixes only the class-matching regex in that line, not the sizing. That branch also rewrites the comments in the stock `monitors.lua` but leaves both default values, the XWayland zero-scaling setting, and `omarchy-hyprland-monitor-scaling` unchanged, so expect the workarounds above to stay relevant.
