---
title: "Where did Waybar go after the Omarchy 4 update?"
description: "Omarchy 4 replaced Waybar with the Quickshell bar, so waybar, its config, and omarchy-refresh-waybar are all gone. Here is where each piece moved to."
answer: "Waybar is gone on purpose. Omarchy 4.0.0 (Quattro) replaced it with the bar inside the single Quickshell process, so the package is uninstalled and ~/.config/waybar is moved aside to a timestamped .bak. Bar config now lives in ~/.config/omarchy/shell.json under the bar key, and omarchy-refresh-waybar is replaced by omarchy refresh shell."
appliesTo:
  from: "4.0.0"
status: by-design
category: shell
issueCount: 224
errorStrings:
  - "omarchy-refresh-waybar: command not found"
  - "omarchy-restart-waybar: command not found"
  - "omarchy-toggle-waybar: command not found"
  - "bash: waybar: command not found"
  - "Unknown Omarchy command: omarchy refresh waybar"
  - "error: package 'waybar' was not found"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [waybar, quickshell, bar, quattro, shell-json, upgrade]
sources:
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro): the entire desktop shell reimagined in Quickshell"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Release v4.0.2: prevent the desktop bar visibility toggle from becoming unresponsive"
    kind: release
    author: "ryanrhughes"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/discussions/7544"
    title: "Discussion #7544: Waybar/Menubar config"
    kind: discussion
    author: "mightbeloren"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/discussions/6577"
    title: "Discussion #6577: Notes from a 3.8.4 to Quattro upgrade: Wi-Fi credentials, user state in ~/.config/waybar, and symlinks in plugin folders"
    kind: discussion
    author: "jfbourdeau"
    date: "2026-08-06"
  - url: "https://github.com/omacom/omarchy/discussions/6332"
    title: "Discussion #6332: Where is the Waybar source/config? I'd like to contribute a UI improvement?"
    kind: discussion
    author: "Aashutosh31"
    date: "2026-07-21"
  - url: "https://github.com/omacom/omarchy/issues/8357"
    title: "Issue #8357: omarchy-upgrade-to-quattro force-overwrites shell.json instead of migrating it, silently dropping bar/plugin config"
    kind: issue
    author: "Orneyfish"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7022"
    title: "Issue #7022: omarchy toggle bar on/off has inverted semantics (hides bar on 'on', shows it on 'off')"
    kind: issue
    author: "Amvurguezo"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/10319"
    title: "Issue #10319: Bar: custom command module with empty \"text\" renders the raw JSON"
    kind: issue
    author: "raetsch-hue"
    date: "2026-09-05"
  - url: "https://omarchy.org/manual/the-top-bar/"
    title: "Omarchy manual: The Top Bar"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "CtByte"
    url: "https://github.com/CtByte"
    for: "Gave the short answer in discussion #7544 that there is no Waybar on Quattro, only the new Quickshell bar"
  - name: "jfbourdeau"
    url: "https://github.com/jfbourdeau"
    for: "Documented that the upgrade moves the whole ~/.config/waybar directory aside, including unrelated user state kept in it"
  - name: "Orneyfish"
    url: "https://github.com/Orneyfish"
    for: "Traced the Quattro upgrade overwriting a customized shell.json and located the timestamped backup it leaves behind"
  - name: "Amvurguezo"
    url: "https://github.com/Amvurguezo"
    for: "Found that omarchy toggle bar on hides the bar because the on/off argument is passed straight to the bar-off flag"
faq:
  - q: "Can I install Waybar again on Omarchy 4?"
    a: "You can install the package from the Arch repos and run it yourself, but nothing in Omarchy will configure or theme it. The 4.0.4 tree ships no waybar config and no themes/*/waybar.css, so styling, theme switching, and the update indicator all stay with the Quickshell bar."
  - q: "Where is my old Waybar config?"
    a: "The upgrade renames the directory to ~/.config/waybar.omarchy-upgrade-to-quattro.<timestamp>.bak rather than deleting it. Check there for style.css, config.jsonc, and any scripts or data files you kept in that folder."
  - q: "What replaced omarchy-refresh-waybar?"
    a: "omarchy refresh shell, which resets ~/.config/omarchy/shell.json to the Omarchy default, restores the default bar layout, and restarts the shell. It is a reset, not a reload, so back up your shell.json first."
related: [quickshell-crashes-or-bar-missing, walker-launcher-missing-after-update, custom-keybindings-lost-after-quattro, monitors-conf-replaced-by-monitors-lua, plugin-fails-to-load]
draft: false
---

Waybar drew the top bar on every Omarchy release up to and including v3.8.4. On v4.0.0 "Quattro" (2026-08-14) it was removed. The strip along the top of your screen is still there, but it is now part of the Omarchy shell, one long running Quickshell process that also draws the menu, the notifications, the OSD popups, the control panels, and the lock screen. So the bar is not missing. Waybar is, and the config, the CSS, and the `omarchy-*-waybar` commands went with it.

Run `omarchy-version` first. Everything below applies to 4.0.0 through 4.0.4. On 3.8.4 and earlier, Waybar is still the bar and none of this applies.

## The fix

1. If you see no bar at all, it may just be hidden. Press `Super + Shift + Space`, which is bound to "Toggle top bar" in the shipped Hyprland bindings. The same thing lives in the menu under Trigger, Toggle, Menu Bar.

2. If you script that toggle, know that `omarchy toggle bar on` currently hides the bar and `omarchy toggle bar off` shows it. The wrapper is a one liner that hands whatever you typed to the `bar-off` state flag, so `on` turns the off flag on. Amvurguezo filed this as issue #7022; it is still open, and the 4.0.4 copy of `omarchy-toggle-bar` still has no inversion. Plain `omarchy toggle bar` with no argument flips the state correctly.

3. Find your old config. The upgrade does not delete it, it renames it:

   ```bash
   ls -d ~/.config/waybar.omarchy-upgrade-to-quattro.*.bak
   ```

   The timestamp is the moment you ran the upgrade. `config.jsonc`, `style.css`, and anything else you kept in that folder are inside.

4. Edit the bar through its new config file, `~/.config/omarchy/shell.json`, under the `bar` key. Every widget is one entry in `bar.layout.left`, `bar.layout.center`, or `bar.layout.right`, and its settings sit inline on that entry. There is no separate style sheet:

   ```bash
   jq .bar ~/.config/omarchy/shell.json
   ```

5. Prefer the commands to hand editing, because they keep the file valid and reload the shell for you:

   ```bash
   omarchy bar position bottom
   omarchy bar transparent toggle
   omarchy bar move omarchy.clock --section center --index 0
   omarchy bar set omarchy.clock format "HH:mm"
   omarchy bar defaults
   ```

   You can also just drag. Grabbing an empty patch of bar and pulling it to a screen edge moves it, and dragging a widget reorders it.

6. Add or remove whole widgets with the plugin commands. `omarchy plugin list` prints every widget the shell knows about with its id:

   ```bash
   omarchy plugin enable omarchy.media --section center
   omarchy plugin disable omarchy.weather
   ```

7. Port custom modules. A Waybar `custom/*` module becomes an inline entry with `type` set to `command`:

   ```json
   { "id": "vpn", "type": "command", "exec": "~/.config/omarchy/bar/scripts/vpn-status",
     "interval": 5, "tooltip": "VPN", "onClick": "nm-connection-editor" }
   ```

   Your script can keep printing the Waybar style JSON it printed before, `{"text": ..., "tooltip": ..., "class": ...}`, or plain text. For something Waybar could not do, use `"type": "qml"` and drop a QML `Item` at `~/.config/omarchy/bar/modules/<id>.qml`.

8. Replace the old commands. These are the ones that disappeared:

   | Omarchy 3.x | Omarchy 4.x |
   | --- | --- |
   | `omarchy-refresh-waybar` | `omarchy refresh shell` |
   | `omarchy-restart-waybar` | `omarchy restart shell` |
   | `omarchy-toggle-waybar` | `omarchy toggle bar` |
   | edit `~/.config/waybar/config.jsonc` | `omarchy bar ...` or `~/.config/omarchy/shell.json` |
   | edit `~/.config/waybar/style.css` | theme plus `~/.config/omarchy/shell.toml` |

   Note that `omarchy refresh shell` is a reset, not a reload. It puts `shell.json` back to the Omarchy default and restores the default bar, exactly as `omarchy-refresh-waybar` reset the Waybar config. Copy your `shell.json` somewhere first.

## Verify it worked

Waybar really is uninstalled, not broken:

```bash
pacman -Qi waybar          # error: package 'waybar' was not found
pgrep -af quickshell       # the running omarchy shell
omarchy shell shell ping   # IPC round trip to that process
hyprctl layers | grep omarchy-bar
```

If `hyprctl layers` shows `omarchy-bar` at a negative `y` value, the bar exists and is parked off screen, which means the hide toggle is on rather than the shell being dead.

## Why it happens

The v4.0.0 release notes describe the whole shell being rewritten in Quickshell, with the bar, launcher, menus, notifications, OSDs, panels, lock screen and polkit agent living as plugins in one process. Waybar is on the retired package list in `bin/omarchy-upgrade-to-quattro`, which tries to remove every retired package in one pacman transaction and falls back to dependency groups, `waybar playerctl` being one of them, so a dependency between the two does not block the removal. The same script moves `~/.config/waybar`, `~/.config/swayosd`, `~/.config/mako` and `~/.config/walker` to timestamped `.bak` directories, and clears the old `~/.local/state/omarchy/toggles/waybar-off` flag. Theming moved too: v3.8.4 shipped `themes/*/waybar.css` and `default/themed/waybar.css.tpl`, and v4.0.4 ships neither.

Two upgrade side effects are worth knowing about. jfbourdeau pointed out in discussion #6577 that the whole `~/.config/waybar` directory is moved aside, so any data file you happened to keep in there, such as a watchlist read by a custom module, goes with it and the module silently falls back to defaults. And Orneyfish showed in issue #8357 that the upgrade overwrites `~/.config/omarchy/shell.json` with the stock Quattro default instead of merging it, so a bar you had customized before the upgrade reverts. That issue is still open, and the previous file is at `~/.config/omarchy/shell.json.omarchy-upgrade-to-quattro.<timestamp>.bak`.

## If that did not work

- The bar is gone but the shell is alive, and toggling does nothing. v4.0.2 shipped a fix for the bar visibility toggle becoming unresponsive, so make sure you are past that release before debugging further.
- Nothing at all is drawn, no menu, no notifications. That is the shell failing rather than the bar, so start at [quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/).
- Your custom command module prints the raw JSON line instead of hiding. raetsch-hue traced this in issue #10319: an explicitly empty `"text"` falls through to the raw output. Until it is fixed, print nothing at all when the widget should be invisible.
- Widgets you added to `shell.json` before an update do not pick up new defaults. Once you have your own `shell.json` it is canonical, with no deep merge, so future default widgets will not appear on your bar. `omarchy bar defaults` gives you a clean slate.
- You genuinely want Waybar back. Install it yourself and launch it yourself, but treat it as unsupported: no Omarchy theme will style it, and the update indicator, the panels, and the `Super + Ctrl` panel hotkeys all stay with the Quickshell bar.

Evidence for the "where did it go" question is thin in the issue tracker on purpose, because this is intended behaviour rather than a bug. The clearest confirmation is discussion #7544, where CtByte answered a user hunting for the missing `~/.config/waybar/style.css` by saying Quattro has no Waybar any more, only the new Quickshell bar. farangkao had made the same point a month earlier in discussion #6332.

## Related

- [The Top Bar](https://omarchy.org/manual/the-top-bar/) in the official manual is the reference for widgets, panels and `shell.json`.
- [Upgrading 3 to 4](/upgrade/3-to-4-quattro/) for the rest of what the Quattro upgrade moves.
- [Walker launcher missing after update](/fix/walker-launcher-missing-after-update/) is the same story for the launcher.
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/) and [monitors.conf replaced by monitors.lua](/fix/monitors-conf-replaced-by-monitors-lua/) cover the other configs that moved.
