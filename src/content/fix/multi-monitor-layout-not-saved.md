---
title: "Multi-monitor layout not saved: scale and position reset on Omarchy 4"
description: "Your external monitor layout, scale and position do not survive a reload on Omarchy 4. Write explicit hl.monitor rules in monitors.lua, then reload."
answer: "Omarchy 4's Display panel and Super + / only persist scale into the catch-all rule in ~/.config/hypr/monitors.lua, and on a docked laptop a watcher re-applies that file every two seconds with position \"auto\". Write one literal hl.monitor line per output, keyed by connector name, with the scale and position you want, then run hyprctl reload and stop using the scale buttons."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 60
errorStrings:
  - "keyword can't work with non-legacy parsers. Use eval."
tags: [monitors, multi-monitor, scaling, hyprland, lua, clamshell]
sources:
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
  - url: "https://github.com/omacom/omarchy/issues/7625"
    title: "Issue #7625: omarchy-hyprland-monitor-scaling: scale reverts instantly, monitors get rearranged, and sed -i destroys a symlinked monitors.lua"
    kind: issue
    author: "FCygan"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/7242"
    title: "Issue #7242: omarchy hyprland monitor scaling reverts instantly when monitors.lua has per-monitor rules"
    kind: issue
    author: "Douda"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/6909"
    title: "Issue #6909: [Quattro] eDP-1 monitor scaling forces 2x reset on mixed-monitor array with Quickshell navbar"
    kind: issue
    author: "PedroMiguelInacio"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/7066"
    title: "Issue #7066: Omarchy Quatro: Not Honoring Transform in Monitor Config"
    kind: issue
    author: "YuseiRun"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/4785"
    title: "Issue #4785: Omarchy 3.4.0: Monitor scale cycling breaks layout"
    kind: issue
    author: "reppiz"
    date: "2026-02-27"
  - url: "https://github.com/omacom/omarchy/discussions/8213"
    title: "Discussion #8213: Update monitor configuration defaults and docs to use relative positioning (auto) to prevent cursor trapping"
    kind: discussion
    author: "syskey8"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/pull/7581"
    title: "PR #7581: Leave an auto-scaled internal panel alone in clamshell recovery"
    kind: pr
    author: "fuchsblau"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/pull/7437"
    title: "PR #7437: Persist monitor scaling to explicit per-monitor entries"
    kind: pr
    author: "ckopsa"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/pull/8145"
    title: "PR #8145: Persist monitor scaling onto named per-output rules"
    kind: pr
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
credits:
  - name: "RonRayReed"
    url: "https://github.com/RonRayReed"
    for: "Traced the two-second clamshell poll re-applying the stale scale from monitors.lua"
  - name: "mkelk"
    url: "https://github.com/mkelk"
    for: "Showed that the watcher cannot read a desc: rule and asserts a guessed scale instead"
  - name: "skoom21"
    url: "https://github.com/skoom21"
    for: "Found the two code paths that hardcode position = auto for the internal panel"
  - name: "nico-kovacs"
    url: "https://github.com/nico-kovacs"
    for: "Showed that a per-monitor scale change persists globally and rescales the other screens"
  - name: "syskey8"
    url: "https://github.com/syskey8"
    for: "Explained the cursor dead zone caused by absolute positions under fractional scaling"
faq:
  - q: "Why does my scale snap back about a second after I set it?"
    a: "On a laptop with an external monitor active, omarchy-hyprland-monitor-watch runs omarchy-hyprland-monitor-clamshell every two seconds. That script reads monitors.lua and re-applies the internal panel to the scale it finds there. If the Display panel did not write your new value into the file, the poll undoes it."
  - q: "Can I use nwg-displays or Hyprmon to arrange screens?"
    a: "You can use them to work out coordinates, and the manual links Hyprmon. But anything that only sets the live Hyprland state loses to the same watcher and to the next reload. Copy the numbers into monitors.lua as hl.monitor rules to make them stick."
  - q: "Does any 4.0.x release fix this?"
    a: "Only partly. 4.0.1 shipped PR #7581, which stops the clamshell recovery fighting a panel whose scale is left at auto. The persistence bugs in omarchy-hyprland-monitor-scaling were still open on 2026-09-16, with PRs #7437 and #8145 unmerged."
related: [monitors-conf-replaced-by-monitors-lua, fractional-scaling-blurry-or-huge-apps, cursor-invisible-or-wrong-size, suspend-wont-resume-s2idle]
draft: false
---

You arrange your screens, set a scale, and it looks right. Then you reload, dock, undock, or reboot, and the layout is back where it started. On Omarchy 4 this is usually not Hyprland losing your config. It is Omarchy writing over it.

## The fix

Checked on 4.0.4. The same steps apply to 4.0.0 through 4.0.3. On 3.x the file is `monitors.conf` and only step 5 applies, see [the Quattro config page](/fix/monitors-conf-replaced-by-monitors-lua/).

1. Get your real output names. Run `hyprctl monitors all`. Note the connector name (`eDP-1`, `DP-2`, `HDMI-A-1`), the mode you want, and the description string if you have two identical panels.

2. Open the file. Use *Setup > Monitors* in the Omarchy menu, which runs `omarchy-launch-config-editor "$HOME/.config/hypr/monitors.lua"`.

3. Write one explicit rule per output, each on a single literal line, above the shipped catch-all. Keep the catch-all last so any screen you did not name still comes up:

   ```lua
   local omarchy_gdk_scale = 1
   local omarchy_monitor_scale = "auto"

   hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))

   hl.monitor({ output = "DP-2", mode = "2560x1440@165", position = "0x0", scale = 1 })
   hl.monitor({ output = "HDMI-A-1", mode = "1920x1080@60", position = "auto-right", scale = 1 })
   hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto-down", scale = 1.6 })

   hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
   ```

4. Prefer relative positions. Use `auto-right`, `auto-left`, `auto-up` or `auto-down` rather than pixel coordinates unless every screen is at scale 1. Absolute coordinates are computed against logical pixels, so a 1080p screen at scale 1.25 is only 864 logical pixels tall and a neighbour pinned at `0x1080` leaves a gap your cursor cannot cross. syskey8 worked the arithmetic out in [discussion #8213](https://github.com/omacom/omarchy/discussions/8213).

5. Set `GDK_SCALE` to the nearest whole number of your largest monitor scale. GTK only honours integers, and apps already running keep the old value until you restart them.

6. Reload with `hyprctl reload`. Do not use `hyprctl keyword monitor ...` from a 3.x guide. Omarchy 4 loads Hyprland through Lua, and that call fails with `keyword can't work with non-legacy parsers. Use eval.`

7. From now on, change scale by editing the rule, not with the Display panel buttons or `Super + /`. Those call `omarchy-hyprland-monitor-scaling`, which is the source of most of the resets described below.

## Verify it worked

Read the live state back and compare it to what you wrote:

```bash
hyprctl monitors all -j | jq -r '.[] | "\(.name) \(.width)x\(.height) scale=\(.scale) at \(.x)x\(.y) transform=\(.transform)"'
```

Then wait ten seconds and run it again. A docked laptop is re-checked every two seconds, so a layout that is going to be overwritten will change within that window. Check `hyprctl configerrors` for a silent parse failure, unplug and replug the external screen, and reboot once. If a scale keeps moving on its own, `~/.local/state/omarchy/monitor-scaling.log` records every change the scaling tool made, including which process asked for it.

## Why it happens

Three separate mechanisms in 4.0.x can write over your layout.

**The scale tool persists to the wrong place.** `bin/omarchy-hyprland-monitor-scaling` applies the new scale live with `hyprctl eval`, then tries to save it by rewriting either `local omarchy_monitor_scale` or the wildcard `output = ""` rule. Both are global. nico-kovacs showed in [#6673](https://github.com/omacom/omarchy/issues/6673) that setting a scale on one screen therefore changes the others within a second or two, because the file write itself triggers a config reload. If your file has explicit per-output rules instead, RonRayReed found in [#8103](https://github.com/omacom/omarchy/issues/8103) that the save silently does nothing, and Douda reported the same revert in [#7242](https://github.com/omacom/omarchy/issues/7242).

**The clamshell watcher re-asserts the internal panel.** `omarchy-hyprland-monitor-watch` runs `omarchy-hyprland-monitor-clamshell` on every monitor event, and every two seconds for as long as a laptop has an active external monitor. That script parses `monitors.lua` with `sed`. It matches only a rule written literally as `output = "eDP-1"`. mkelk showed in [#7084](https://github.com/omacom/omarchy/issues/7084) that a `desc:` rule is invisible to it, so it falls back to the catch-all or to a hardcoded `2` and forces that value back. This is why an unmatched panel snaps back about a second after every change.

**Position is never read from the catch-all.** skoom21 documented in [#7326](https://github.com/omacom/omarchy/issues/7326) that the clamshell script's `read_monitor_position` returns `auto` whenever it cannot find a connector-name rule for the internal panel, and that the live `hyprctl eval` inside the scale tool hardcodes `position = "auto"` as well. So on a stock `monitors.lua`, which contains no per-output rule at all, a deliberate offset is discarded on the next monitor event or scale press. reppiz saw the same rearrangement on 3.4.0 in [#4785](https://github.com/omacom/omarchy/issues/4785), so the position half predates Quattro.

One piece did get fixed. [PR #7581](https://github.com/omacom/omarchy/pull/7581) by fuchsblau merged on 2026-08-22 and shipped in [4.0.1](/releases/v4.0.1/) as "Leave an auto-scaled internal panel alone in clamshell recovery". It makes the recovery step return early when the configured scale is not a number, which is the default `"auto"`, and it closed PedroMiguelInacio's [#6909](https://github.com/omacom/omarchy/issues/6909). The persistence PRs [#7437](https://github.com/omacom/omarchy/pull/7437) and [#8145](https://github.com/omacom/omarchy/pull/8145) were still open on 2026-09-16.

## If that did not work

**You keyed a monitor by description.** `desc:` is valid Hyprland syntax and Hyprland honours it, but the clamshell script does not. Key the internal panel by connector name. Connector numbering is stable for `eDP`, `LVDS` and `DSI`; only DP connectors renumber across hotplug, so use `desc:` for external screens if you need it and keep the internal panel literal.

**You generated the rules with a Lua loop.** In a comment on [#8103](https://github.com/omacom/omarchy/issues/8103), gfk reported that this makes things worse, because the shell parser finds no literal line and falls back to the catch-all every two seconds. Keep at least the internal panel's rule as one plain line.

**Your `monitors.lua` is a symlink into a dotfiles repo.** FCygan reported in [#7625](https://github.com/omacom/omarchy/issues/7625) that `sed -i` without `--follow-symlinks` replaces the symlink with a regular file the first time a scale button is pressed, so the repo quietly stops driving the config. Check with `ls -l ~/.config/hypr/monitors.lua` after any scale change.

**Rotation comes back wrong after a reboot.** YuseiRun reported in [#7066](https://github.com/omacom/omarchy/issues/7066) that a `transform` value in the config is present but not applied until you change it and change it back. That report is one machine with no follow-up, so treat it as thin evidence rather than a confirmed pattern.

**Nothing responds to the keyboard after your edit.** A Lua error in `monitors.lua` aborts evaluation before the bindings load. See [the nil global o page](/fix/hyprland-lua-attempt-to-index-nil-global-o/), and recover the shipped file with `omarchy-refresh-config hypr/monitors.lua`, which backs your version up first.

**The screen comes back blank rather than misplaced.** That is a different failure. Try [suspend and resume](/fix/suspend-wont-resume-s2idle/) or [the dock notes](/hardware/thunderbolt-dock/).

## Related

- [Monitor layout lost after Quattro](/fix/monitors-conf-replaced-by-monitors-lua/)
- [Fractional scaling looks blurry or huge](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Multi-monitor hardware notes](/hardware/multi-monitor/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
- [Omarchy manual: Monitors](https://omarchy.org/manual/monitors/)
