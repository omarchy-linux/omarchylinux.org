---
title: "Monitor layout lost after Quattro: monitors.conf replaced by monitors.lua"
description: "After the Omarchy 4 Quattro upgrade your monitors.conf is ignored and monitors.lua holds stock defaults. Port each monitor line to hl.monitor by hand."
answer: "Your old ~/.config/hypr/monitors.conf is still on disk but Omarchy 4 never reads it. Open ~/.config/hypr/monitors.lua (Setup > Monitors in the menu) and rewrite each old monitor= line as an hl.monitor table, and each env = GDK_SCALE line as hl.env. Save, then run hyprctl reload. Nothing ports it for you, on any 4.0.x release."
appliesTo:
  from: "4.0.0"
status: open
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 60
errorStrings:
  - "keyword can't work with non-legacy parsers"
tags: [monitors, quattro, hyprland, lua, scaling, upgrade]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6911"
    title: "Issue #6911: Quattro upgrade replaces customized monitors.conf with default monitors.lua (auto layout, GDK_SCALE=2) without porting or warning"
    kind: issue
    author: "daventhedude"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7242"
    title: "Issue #7242: omarchy hyprland monitor scaling reverts instantly when monitors.lua has per-monitor rules"
    kind: issue
    author: "Douda"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/8103"
    title: "Issue #8103: omarchy-hyprland-monitor-scaling doesn't persist scale on outputs with explicit per-monitor rules in monitors.lua"
    kind: issue
    author: "RonRayReed"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/7066"
    title: "Issue #7066: Omarchy Quatro: Not Honoring Transform in Monitor Config"
    kind: issue
    author: "YuseiRun"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/9721"
    title: "Issue #9721: hyprland.lua: Sub-module require errors abort script evaluation before hypr.bindings, locking user out of keybindings"
    kind: issue
    author: "codyoss"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/discussions/8213"
    title: "Discussion #8213: Update monitor configuration defaults and docs to use relative positioning (auto) to prevent cursor trapping"
    kind: discussion
    author: "syskey8"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/pull/8362"
    title: "PR #8362: Fix: Use relative positioning (auto-right) in multi-monitor defaults to prevent scaling cursor traps"
    kind: pr
    author: "syskey8"
    date: "2026-08-26"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
credits:
  - name: "daventhedude"
    url: "https://github.com/daventhedude"
    for: "Traced the upgrade path and published a working three-monitor monitors.lua"
  - name: "Douda"
    url: "https://github.com/Douda"
    for: "Isolated why a scale change reverts when an explicit per-output rule exists"
  - name: "RonRayReed"
    url: "https://github.com/RonRayReed"
    for: "Traced the clamshell watcher re-applying the stale scale from monitors.lua"
  - name: "syskey8"
    url: "https://github.com/syskey8"
    for: "Explained the cursor dead zone from absolute positions under fractional scaling"
faq:
  - q: "Does the Quattro upgrade delete my monitors.conf?"
    a: "No. It leaves the file in ~/.config/hypr/ untouched and simply stops reading it. It gets no .bak rename and no mention in the upgrade output, which is why the loss is silent. The reporter of #6911 noted that other configs on their 4.0.0 upgrade did get parked as .bak files, which is what made the omission stand out."
  - q: "Can I just symlink monitors.conf back in?"
    a: "No. Omarchy 4 starts Hyprland from hyprland.lua, which requires hypr.monitors as a Lua module. The old keyword parser is not loaded, so a .conf file has nothing to parse it."
  - q: "Is there a tool that converts the file for me?"
    a: "Not in Omarchy as of 4.0.4. No migration shipped through 4.0.4 touches monitors.conf, and the filename does not appear anywhere in the 4.0.4 source tree. Porting the lines by hand is the only path."
related: [custom-keybindings-lost-after-quattro, multi-monitor-layout-not-saved, fractional-scaling-blurry-or-huge-apps, hyprland-lua-attempt-to-index-nil-global-o]
draft: false
---

You upgraded to Omarchy 4 and your screens came back in the wrong order, the wrong rotation, or at the wrong scale. Your old `~/.config/hypr/monitors.conf` is still sitting there. Omarchy 4 never reads it.

## The fix

Checked on 4.0.4. The same steps apply to every 4.0.x release, because nothing in 4.0.1 through 4.0.4 changed this.

1. Look at what you had. `cat ~/.config/hypr/monitors.conf`. The file survives the upgrade unchanged, so your old layout is still readable. The upgrade makes no backup of it, so if it is gone, something other than Omarchy removed it.

2. Open the new file. Use *Setup > Monitors* in the Omarchy menu, or run `omarchy launch config-editor ~/.config/hypr/monitors.lua`.

3. Translate each line. The Lua form takes one table per output:

   ```lua
   -- monitor=,preferred,auto,auto
   hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })

   -- monitor = DP-2, 2560x1440@165, 1920x0, 1
   hl.monitor({ output = "DP-2", mode = "2560x1440@165", position = "1920x0", scale = 1 })

   -- monitor = DP-2, preferred, auto, 1, transform, 1
   hl.monitor({ output = "DP-2", mode = "preferred", position = "auto", scale = 1, transform = 1 })

   -- monitor=DP-2,disable
   hl.monitor({ output = "DP-2", disabled = true })
   ```

   Positional arguments become named keys. Extra 3.x flags that used to trail the line, such as `transform` and `vrr`, become keys in the same table. Numbers stay unquoted, strings get quotes, and `scale = "auto"` is a quoted string because it is not a number. `mirror = "eDP-1"` is the mirroring key, which is what `omarchy-hyprland-monitor-internal-mirror` writes.

4. Match monitors by description if you have identical panels. `output = "desc:Hewlett Packard HP Z27i CNK4040DPF"` works the same as it did in 3.x. Get the strings from `hyprctl monitors all`.

5. Port your GTK scale. The old `env = GDK_SCALE,1` becomes `hl.env("GDK_SCALE", "1")`. The shipped template sets this through two variables at the top of the file, and ships them at the 2x retina defaults:

   ```lua
   local omarchy_gdk_scale = 2
   local omarchy_monitor_scale = "auto"

   hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))
   hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
   ```

   If you run one scale for everything, keep that shape and just change the two numbers, for example `1` and `1` for a 1080p or 1440p desk. The `Super + /` scaling hotkeys write back into those two variables, so editing them is the supported path.

6. Reload. Save the file and Hyprland picks it up on its own config reload. If you want to force it, run `hyprctl reload`.

7. Delete or rename `monitors.conf` once the new file works, so you do not edit the dead one by mistake six months from now.

## Verify it worked

Run `hyprctl monitors all` and read back `scale`, `transform`, `at` and `description` for each output. They should match what you wrote.

Then log out and back in. This catches the case where a value applies live but not at startup, which is the shape of issue [#7066](https://github.com/omacom/omarchy/issues/7066), where a `transform` value survives in the file but the rotation is not applied after a restart until the value is changed and changed back.

Also press `Super + Return`. If no keybinding responds, your Lua did not parse. See below.

## Why it happens

Omarchy 4 moved the whole Hyprland configuration from `.conf` to Lua. `~/.config/hypr/hyprland.lua` is the entry point and it pulls in your overrides with `require("hypr.monitors")`, which resolves to `monitors.lua`. There is no keyword parser left to read a `.conf` file.

The upgrade script `omarchy-upgrade-to-quattro` keeps a list it calls `always_copy_config_files`, and `hypr/monitors.lua` is on it. Those files are treated as new Quattro entry points that no older install could have, so the stock template is copied in unconditionally. The stock template is a single catch-all rule with `position = "auto"`, `scale = "auto"`, and `omarchy_gdk_scale = 2`.

`monitors.conf` is not on the retire list, so it is neither backed up nor removed. That is the whole bug. daventhedude documented this in [issue #6911](https://github.com/omacom/omarchy/issues/6911): the old file stays on disk, nothing renames it, and the upgrade summary never mentions it, so you get no hint that your display settings stopped applying. Their three-monitor setup came up with a portrait panel in landscape, wrong positions, and GTK apps at 2x on 1440p.

That issue was still open on 2026-09-16. The filename `monitors.conf` does not appear anywhere in the 4.0.4 tree, not in the upgrade script and not in any migration. The only attention the old `~/.config/hypr/*.conf` files get is a temporary shim the upgrade script builds so the still-running 3.x session does not break on reload mid-upgrade. Nothing reads them afterwards.

## If that did not work

**Nothing responds to the keyboard after you edit the file.** A syntax error or runtime error in `monitors.lua` aborts the Lua thread before `require("hypr.bindings")` runs, so the desktop starts with a wallpaper and a bar but no shortcuts at all. codyoss filed this as [#9721](https://github.com/omacom/omarchy/issues/9721), still open. Get a TTY with `Ctrl + Alt + F2`, fix the file, or restore the shipped default with `omarchy-refresh-config hypr/monitors.lua`, which backs your version up first.

**A scale change snaps back within a second or two.** This is the known interaction between explicit per-output rules and the scaling tool. `omarchy-hyprland-monitor-scaling` applies the new scale live with `hyprctl eval`, then persists it by rewriting only the `omarchy_monitor_scale` variable or the wildcard `output = ""` rule. With explicit `hl.monitor({ output = "eDP-1", ... })` rules in the file, that goes wrong in one of two ways. If you kept the stock catch-all above your rules, the variable does get rewritten, but the file write triggers a config reload and your explicit rule overrides the catch-all again, which is what Douda traced in [#7242](https://github.com/omacom/omarchy/issues/7242). If you removed the catch-all, the sed finds nothing to rewrite and silently no-ops, and on a laptop with an external screen the clamshell poller re-applies the file value every couple of seconds, which RonRayReed traced in [#8103](https://github.com/omacom/omarchy/issues/8103) using `~/.local/state/omarchy/monitor-scaling.log`. Either way the fix is the one RonRayReed gives: edit the scale in the explicit rule and reload, rather than using the Display panel or the hotkey. Both issues were still open on 2026-09-16.

**Your cursor gets stuck between two screens.** If you ported absolute positions like `1920x0` and then changed a scale, the logical size of that output shrank and left a dead zone. syskey8 wrote this up in [discussion #8213](https://github.com/omacom/omarchy/discussions/8213) and proposed relative positions such as `position = "auto-right"` in [PR #8362](https://github.com/omacom/omarchy/pull/8362). That PR was still open and unmerged on 2026-09-16, and the 4.0.4 template still ships `position = "auto"`, so you have to make this change yourself.

**You are copying a 3.x guide that says `hyprctl keyword monitor ...`.** That call is rejected under the Lua parser with `keyword can't work with non-legacy parsers`. Use `hyprctl eval` with an `hl.monitor({ ... })` call instead, which is what the Omarchy monitor scripts do.

## Related

The manual chapter on [monitors](https://omarchy.org/manual/monitors/) covers scaling values and the clamshell behaviour on 4.x. For the same silent replacement applied to your shortcuts, see [custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/). For layouts that refuse to stick across reboots or docking, see [multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/) and [multi-monitor](/hardware/multi-monitor/). For apps that came back huge or blurry after the GDK_SCALE default changed, see [fractional scaling blurry or huge apps](/fix/fractional-scaling-blurry-or-huge-apps/). The broader port is covered in [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) and [3 to 4 Quattro](/upgrade/3-to-4-quattro/).
