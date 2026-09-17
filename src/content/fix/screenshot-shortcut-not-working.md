---
title: "Screenshot shortcut not working"
description: "Print Screen does nothing, the picker never appears, or screen recording fails silently on Omarchy 4.x. How to find which part of the capture chain broke."
answer: "Run the command by hand first: omarchy capture screenshot. If that works, your keybinding is the problem. If it prints jq errors, use omarchy capture screenshot region as a workaround. If the screen looks frozen and clicks are dead, switch to a TTY and run pkill -x hyprpicker slurp. No Print Screen key? Super + Ctrl + C opens the same capture menu."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 211
errorStrings:
  - "jq: error (at <stdin>:107): string (\"null\") cannot be parsed as a number"
  - "Screen recording directory does not exist"
  - "gsr error: display \"HDMI-A-1\" not found"
tags: [screenshot, screen-recording, keybindings, slurp, quickshell]
sources:
  - url: "https://omarchy.org/manual/screenshots-recording/"
    title: "Omarchy Manual: Screenshots & Recording"
    kind: manual
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11903"
    title: "Issue #11903: [4.0.2-2 ARM/M2 + Hyprland 0.56.0] omarchy capture screenshot fails: jq string (\"null\") cannot be parsed as a number"
    kind: issue
    author: "avillagran"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/8797"
    title: "Issue #8797: omarchy-capture-screenshot kills the compositor: hyprctl eval of cursor:no_hardware_cursors faults in hl.config() (SIGABRT)"
    kind: issue
    author: "jeffsidekick"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/5468"
    title: "Issue #5468: omarchy-cmd-screenshot: hitting Print Screen occasionally locks input"
    kind: issue
    author: "joshualambert"
    date: "2026-04-27"
  - url: "https://github.com/omacom/omarchy/issues/5506"
    title: "Issue #5506: omarchy-capture-screenshot toggle leaves stale hyprpicker overlay after crash"
    kind: issue
    author: "dphov"
    date: "2026-04-30"
  - url: "https://github.com/omacom/omarchy/issues/8240"
    title: "Issue #8240: Screenshot picker runs with hardware cursors forced on, hiding the pointer on nouveau/vmwgfx while you select"
    kind: issue
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8237"
    title: "Issue #8237: A bare click in the capture picker snaps to the whole monitor instead of the highlighted window"
    kind: issue
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7845"
    title: "Issue #7845: Screenshot editor doesn't close on Enter (tensaku-edit missing --early-exit)"
    kind: issue
    author: "mtaplits"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7184"
    title: "Issue #7184: Screen recording fails silently on the external monitor of a hybrid-GPU laptop, and --fullscreen ignores OMARCHY_SCREENRECORD_USE_PORTAL"
    kind: issue
    author: "Literato2"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/10311"
    title: "Issue #10311: ScreenRecording bar indicator stuck 'active' after boot despite no gpu-screen-recorder process running"
    kind: issue
    author: "AmanKRoy"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/discussions/611"
    title: "Discussion #611: Guide: Adapting Omarchy's Screenshot & Media Keys for MacBooks (or Keyboards without a Print Screen key)"
    kind: discussion
    author: "sailoz"
    date: "2025-08-10"
credits:
  - name: "avillagran"
    url: "https://github.com/avillagran"
    for: "Traced the jq tonumber failure to Hyprland dropping .activeWorkspace.id, and found the region and fullscreen workarounds"
  - name: "jeffsidekick"
    url: "https://github.com/jeffsidekick"
    for: "Symbolized the compositor crash that Print Screen can trigger through hyprctl eval"
  - name: "joshualambert"
    url: "https://github.com/joshualambert"
    for: "Identified the hyprpicker freeze layer stealing keyboard focus from slurp"
  - name: "dphov"
    url: "https://github.com/dphov"
    for: "Showed that a stale hyprpicker overlay survives the toggle and looks like a frozen desktop"
  - name: "Chessing234"
    url: "https://github.com/Chessing234"
    for: "Reported the invisible pointer during selection and the bare-click snapping to the wrong rectangle"
  - name: "zailtz"
    url: "https://github.com/zailtz"
    for: "Found that keysym names like bracketleft work where LBRACKET does not"
faq:
  - q: "My laptop has no Print Screen key. How do I take a screenshot?"
    a: "Press Super + Ctrl + C. That opens the capture menu with Screenshot, Screenrecord, Text, QR Code and Color in it. You can also add your own binding in ~/.config/hypr/bindings.lua on 4.x."
  - q: "Where do screenshots go?"
    a: "A PNG in ~/Pictures named screenshot-YYYY-MM-DD_HH-MM-SS.png, plus the clipboard. Set OMARCHY_SCREENSHOT_DIR to change the folder. Omarchy creates that folder for you if it does not exist."
  - q: "Why does the annotation editor stay open when I press Enter?"
    a: "Tensaku saves and copies on Enter but does not exit, because Omarchy's wrapper does not pass --early-exit. Press Escape to close it. The file was already written before the editor opened, so nothing is lost. Tracked in issue #7845."
  - q: "Does pressing Print Screen again cancel the picker?"
    a: "Yes. The script starts with pkill slurp and exits, so a second press dismisses an open selection. It does not kill a stale hyprpicker overlay, which is why a crashed run can leave the screen looking frozen."
related: [quickshell-crashes-or-bar-missing, notifications-not-showing, custom-keybindings-lost-after-quattro, clipboard-history-not-working, hybrid-gpu-laptop-black-screen-aq-drm-devices]
draft: false
---

"Nothing happens when I press Print Screen" covers at least six different faults on Omarchy. The capture chain has a lot of moving parts: a Hyprland keybinding, a freeze layer, a region picker, `grim`, the clipboard, and a notification from the Quickshell bar. Work through it from the outside in.

Checked on 4.0.4 with the shipped scripts from the v4.0.4 tree, and against v3.8.4 for the 3.x differences.

## The fix

### 1. Run the command by hand

Open a terminal and run the command the key is bound to:

```bash
omarchy capture screenshot
```

This is the single most useful step. If the picker comes up here, your keybinding is broken and the capture stack is fine. If it fails here too, the binding is irrelevant.

### 2. Confirm the key is actually bound

On 4.x, press `Super + K` for the keybindings overlay, or print them:

```bash
omarchy menu keybindings --print
```

The defaults ship in `default/hypr/bindings/utilities.lua` as `o.bind("PRINT", "Screenshot", "omarchy-capture-screenshot")`. Your own overrides belong in `~/.config/hypr/bindings.lua`.

On 3.x the same binding lived in `~/.config/hypr/bindings.conf` as `bindd = , PRINT, Screenshot, exec, omarchy-capture-screenshot`. If you copied a binding from an older guide that calls `omarchy-cmd-screenshot`, that name is gone. The script has been `omarchy-capture-screenshot` since well before 3.8.4, so an old binding silently runs a command that does not exist. See [custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/).

### 3. If you get jq errors and no picker

```
jq: error (at <stdin>:107): string ("null") cannot be parsed as a number
```

`omarchy-capture-region` reads `.activeWorkspace.id` out of `hyprctl monitors -j`. On Hyprland builds where that field is gone, the id comes back as `null` and `tonumber` fails, so no rectangles are collected and the picker never opens. avillagran hit this on an aarch64 M2 machine running a non-release Hyprland 0.56.0 build ([#11903](https://github.com/omacom/omarchy/issues/11903), closed as not planned). The two modes that skip the workspace filter still work:

```bash
omarchy capture screenshot region       # freeform selection
omarchy capture screenshot fullscreen save
```

### 4. If the screen looks frozen and clicks do nothing

Switch to a TTY with `Ctrl + Alt + F2`, then:

```bash
pkill -x slurp
pkill -x hyprpicker
```

Go back with `Ctrl + Alt + F1`. Two separate reports produce this: the hyprpicker freeze layer grabbing keyboard focus so `slurp` never sees Escape ([#5468](https://github.com/omacom/omarchy/issues/5468)), and a stale hyprpicker overlay left behind after a killed run ([#5506](https://github.com/omacom/omarchy/issues/5506)). Pressing Print Screen again only runs `pkill slurp`, so it cannot clear the overlay.

### 5. If you have no Print Screen key

Press `Super + Ctrl + C`. That opens the capture menu, which has Screenshot, Screenrecord, Text, QR Code and Color in it, and it needs no Print key at all.

To add your own binding on 4.x, edit `~/.config/hypr/bindings.lua`:

```lua
o.bind("SUPER + ALT + GRAVE", "Screenshot", "omarchy-capture-screenshot")
```

MacBook users in [discussion #611](https://github.com/omacom/omarchy/discussions/611) found that friendly names like `LBRACKET` do not resolve. zailtz reported that the X keysym name works instead, for example `bracketleft`. `GRAVE` worked for several people where the bracket keys did not.

### 6. If a screenshot is taken but you never see it

The PNG is written to `~/Pictures` and copied to the clipboard before the notification is sent, and the notification call ends in `|| true` so a dead notification daemon cannot fail the capture. Check the folder first:

```bash
ls -t ~/Pictures | head
```

If the file is there but no toast appeared, the bar is your problem, not capture. See [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/) and [notifications not showing](/fix/notifications-not-showing/).

### 7. If screen recording specifically does nothing

`Alt + Print Screen` runs `omarchy-capture-screenrecording`. Unlike the screenshot directory, the recording directory is not created for you:

```
Screen recording directory does not exist: /path
```

Then turn on logging and read the recorder's own stderr:

```bash
OMARCHY_SCREENRECORD_DEBUG=true omarchy capture screenrecording --fullscreen
cat /tmp/omarchy-screenrecord.log
```

On a hybrid-GPU laptop whose external monitor hangs off the discrete GPU, `gpu-screen-recorder` enumerates only one DRM card and never sees that connector, so it dies instantly with `gsr error: display "HDMI-A-1" not found` while the script still exits 0 ([#7184](https://github.com/omacom/omarchy/issues/7184)). The portal backend is GPU agnostic:

```bash
OMARCHY_SCREENRECORD_USE_PORTAL=true omarchy capture screenrecording
```

Note that per the same report, the `--fullscreen` branch is evaluated before the portal branch and ignores that variable, so use the picker rather than `--fullscreen` when you enable it.

## Verify it worked

```bash
omarchy capture screenshot fullscreen save
```

That skips the picker entirely and prints the path it wrote. If you get a path and the file exists, `grim` and your output directory are fine and the fault is in the picker layer. Then try `omarchy capture screenshot` and confirm the screen freezes, a selection box follows the pointer, and `Return` captures the highlighted window.

Check the pieces are installed if anything is missing:

```bash
pacman -Q grim slurp hyprpicker wl-clipboard tensaku gpu-screen-recorder
```

## Why it happens

The Print Screen key does not take a screenshot by itself. It runs a shell script that does six things in order: kill any running `slurp` and exit (so a second press cancels), force `cursor:no_hardware_cursors` off, start `hyprpicker -r -z` as a screen freeze, run `slurp` fed the monitor and window rectangles from `hyprctl`, capture with `grim -g`, then copy with `wl-copy` and send a notification with a thumbnail and an edit action.

Every one of those steps has produced a bug report:

- The `hyprctl` JSON parsing breaks when Hyprland changes shape ([#11903](https://github.com/omacom/omarchy/issues/11903)).
- The `hyprctl eval` that sets cursor mode has taken the whole compositor down with SIGABRT on Hyprland 0.56.2. jeffsidekick symbolized the core and traced the fault to an expired keybind handle upstream, not to the cursor call itself ([#8797](https://github.com/omacom/omarchy/issues/8797)).
- Forcing hardware cursors on makes the pointer vanish during selection on nouveau and vmwgfx, exactly the hardware where Omarchy's own installer turns software cursors on ([#8240](https://github.com/omacom/omarchy/issues/8240)).
- The freeze layer can swallow the input that would dismiss the picker ([#5468](https://github.com/omacom/omarchy/issues/5468)).
- A bare click snaps to the first containing rectangle, and monitors are listed before windows, so clicking a window gives you the whole monitor ([#8237](https://github.com/omacom/omarchy/issues/8237)).

So "the shortcut is broken" almost never means the key is unbound. Splitting the manual command from the binding tells you which half to chase in one step.

## If that did not work

- **The editor opens and will not close.** Press Escape. Tensaku saves and copies on Enter but stays open because the wrapper omits `--early-exit` ([#7845](https://github.com/omacom/omarchy/issues/7845)). On 3.x the editor was Satty, which did close on Enter. Set `OMARCHY_SCREENSHOT_EDITOR` to something else if you prefer.
- **The stop-recording indicator is stuck on.** The bar can show the recording state at boot with no recorder running ([#10311](https://github.com/omacom/omarchy/issues/10311)), and stopping twice can post two toasts with a broken thumbnail ([#11508](https://github.com/omacom/omarchy/issues/11508)). Confirm with `pgrep -af gpu-screen-recorder` before believing the indicator.
- **The notification icon is a block of purple and black squares.** Cosmetic. The script sends no app icon ([#11506](https://github.com/omacom/omarchy/issues/11506)).
- **You want the file somewhere else.** `OMARCHY_SCREENSHOT_DIR` and `OMARCHY_SCREENRECORD_DIR` both work, and `omarchy capture screenshot smart copy` puts the shot on the clipboard only.

One caveat on the evidence: several of these are single-reporter issues that are still open, and none of 4.0.1 through 4.0.4 carries a release note fixing any of them. Where a report is one machine's story, this page says so rather than presenting it as the cause.

## Related

- [Omarchy manual: Screenshots & Recording](https://omarchy.org/manual/screenshots-recording/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Notifications not showing](/fix/notifications-not-showing/)
- [Clipboard history not working](/fix/clipboard-history-not-working/)
- [Screen sharing in Meet, Zoom and Teams](/switch/screen-sharing-meet-zoom-teams/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
