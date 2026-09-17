---
title: "Walker launcher missing after update"
description: "Omarchy 4 removed the Walker launcher. Super + Space now opens the Omarchy menu and Super + Alt + Space opens the apps-only launcher."
answer: "Walker was removed on purpose in Omarchy 4.0.0. Super + Space now opens the Omarchy menu, which searches apps and commands in one box, and Super + Alt + Space opens an apps-only launcher. Your old ~/.config/walker was renamed to a .bak folder by the Quattro upgrade. Rebind Super + Space to omarchy-menu toggle apps if you want the old feel."
appliesTo:
  from: "4.0.0"
status: by-design
category: shell
issueCount: 210
errorStrings:
  - "Nothing here yet"
  - "Command not found: \"elephant\""
  - "error: target not found: elephant-bluetooth"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [walker, launcher, quattro, menu, keybindings, shell]
sources:
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro): the launcher and the menu, together"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/11107"
    title: "Issue #11107: Apps menu (Super+Space > Apps) always shows \"Nothing here yet\", regression in 4.0.3-1"
    kind: issue
    author: "derekios88"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11028"
    title: "Issue #11028: Cloned menu plugins get null shell.appLibrary, Apps submenu is empty"
    kind: issue
    author: "KalEl117"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/7012"
    title: "Issue #7012: Menu launcher lost Walker's web-search fallback for no-match queries"
    kind: issue
    author: "Balmisjutas"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/6443"
    title: "Issue #6443: Walker autostart service bypasses the GSK_RENDERER=cairo workaround, hard-freezing the desktop on amdgpu"
    kind: issue
    author: "MaciekTW"
    date: "2026-07-30"
  - url: "https://github.com/omacom/omarchy/issues/2546"
    title: "Issue #2546: Walker and Elephant missing after system upgrade"
    kind: issue
    author: "defaultdino"
    date: "2025-10-19"
  - url: "https://github.com/omacom/omarchy/issues/8650"
    title: "Issue #8650: Flatpak apps don't appear in the launcher: session XDG_DATA_DIRS misses Flatpak export dirs"
    kind: issue
    author: "lde-alen"
    date: "2026-08-27"
  - url: "https://omarchy.org/manual/navigation/"
    title: "Omarchy manual: Navigation"
    kind: manual
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/shell-plugins/"
    title: "Omarchy manual: Shell Plugins"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "derekios88"
    url: "https://github.com/derekios88"
    for: "Traced the empty Apps submenu on 4.0.3 down to AppLibrary caching an empty row set"
  - name: "KalEl117"
    url: "https://github.com/KalEl117"
    for: "Showed that a cloned omarchy.menu plugin receives a null appLibrary, which empties the Apps list"
  - name: "Balmisjutas"
    url: "https://github.com/Balmisjutas"
    for: "Documented the web-search fallback that did not survive the move off Walker"
faq:
  - q: "Can I reinstall Walker on Omarchy 4?"
    a: "The Quattro upgrade uninstalls omarchy-walker, walker-bin and every elephant provider, and nothing in the 4.0.4 tree drives them any more. You would be running an unthemed launcher with no Omarchy integration, so it is not worth it."
  - q: "Which key opens the app launcher now?"
    a: "Super + Alt + Space opens the apps-only menu. Super + Space opens the full Omarchy menu, which also matches installed apps as you type."
  - q: "Where did my Walker config go?"
    a: "The upgrade renamed ~/.config/walker to ~/.config/walker.omarchy-upgrade-to-quattro.<timestamp>.bak. It deleted ~/.config/elephant outright without a backup."
related: [command-not-found-elephant, where-did-waybar-go, custom-keybindings-lost-after-quattro, quickshell-crashes-or-bar-missing]
draft: false
---

Walker was the app launcher Omarchy shipped through the 3.x series. In Omarchy 4 it is gone. The v4.0.0 release notes are blunt about it: Walker is gone, and `SUPER + SPACE` now opens the Omarchy menu itself. Nothing is broken on your machine. The keys just moved.

The part that trips people up is that the two shortcuts swapped meanings:

| Key | Omarchy 3.x | Omarchy 4.x |
| --- | --- | --- |
| `Super + Space` | Walker app launcher | Omarchy menu (apps and commands) |
| `Super + Alt + Space` | Omarchy menu | Apps-only menu |

So if you press `Super + Space` expecting a plain list of applications and get a command palette with Apps, Learn, Style, Setup and System in it, you are looking at the new default, not a fault. Checked against the shipped bindings in 4.0.4 (`default/hypr/bindings/utilities.lua`) and against 3.8.4 (`default/hypr/bindings/utilities.conf`).

## The fix

### If you just want your apps back (4.0.0 through 4.0.4)

1. Press `Super + Alt + Space`. That is the dedicated apps-only launcher now. The v4.0.0 notes describe it as having fuzzy and acronym matching with live app icon indexing.
2. Or press `Super + Space` and start typing an app name. The unified menu matches installed apps as well as Omarchy commands, so you usually do not need the second shortcut at all.
3. From a terminal or a script, the same two surfaces are:

   ```bash
   omarchy-menu toggle        # the full menu
   omarchy-menu toggle apps   # the apps-only launcher
   ```

### If you want `Super + Space` to open apps directly

Omarchy 4 moved Hyprland config from `.conf` to Lua, so this goes in `~/.config/hypr/bindings.lua`, not in any `.conf` file.

1. Open the file:

   ```bash
   $EDITOR ~/.config/hypr/bindings.lua
   ```

2. Unbind the default first, then bind your own. Order matters:

   ```lua
   hl.unbind("SUPER + SPACE")
   o.bind("SUPER + SPACE", "Apps", "omarchy-menu toggle apps")
   ```

3. Optionally put the full menu somewhere else:

   ```lua
   hl.unbind("SUPER + ALT + SPACE")
   o.bind("SUPER + ALT + SPACE", "Omarchy menu", "omarchy-menu toggle")
   ```

4. Reload. Hyprland re-reads its config on save, but forcing it and checking for Lua mistakes is cheap. The shell itself does not need restarting for a binding change:

   ```bash
   hyprctl reload
   hyprctl configerrors
   ```

The `hl.unbind` then `o.bind` pattern is the one the stock `~/.config/hypr/bindings.lua` documents in its own comments, and the one the Dotfiles chapter of the manual uses. See [the conf to Lua migration notes](/reference/hyprland-conf-to-lua-migration/) if your bindings did not survive the upgrade at all.

### Where your old config went

The Quattro upgrade script does not delete your Walker settings, but it does move them out of the way:

- `~/.config/walker` is renamed to `~/.config/walker.omarchy-upgrade-to-quattro.<timestamp>.bak`, where the timestamp is the moment you ran the upgrade.
- `~/.config/elephant` is removed outright. There is no backup of it. Same for `~/.config/autostart/walker.desktop`.
- The user units `app-walker@autostart.service` and `elephant.service` are deleted, along with `/etc/pacman.d/hooks/walker-restart.hook`.

Nothing reads the `.bak` folder. It is there so you can copy custom entries across by hand. The new equivalents are `~/.config/omarchy/extensions/omarchy-menu.jsonc` for your own menu entries and `~/.config/omarchy/shell.json` for plugin state.

## Verify it worked

```bash
omarchy-menu toggle apps            # apps launcher should appear
pacman -Qq | grep -E '^(walker|walker-bin|omarchy-walker|elephant)' ; echo "exit $?"
ls -d ~/.config/walker* 2>/dev/null
```

The `pacman -Qq` grep should print nothing and report `exit 1`. If it prints package names, your Quattro upgrade did not finish removing the retired set. The `ls` should show only a `.bak` directory, or nothing at all on a fresh 4.x install.

## Why it happens

Omarchy 4.0.0 rewrote the whole desktop shell as one Quickshell process. The bar, notifications, OSDs, lock screen, polkit agent and the menu are now plugins inside `omarchy-shell`. Once the menu could search its own nested entries, keeping a second palette with a second shortcut stopped making sense, so the launcher was merged into the menu.

Walker also carried real costs. It ran as a resident `walker --gapplication-service` process started from an XDG autostart entry, and on at least one amdgpu machine that process hard-froze the desktop because the autostart entry carried no renderer override, reported in issue #6443 and closed by dhh the day before the 4.0.0 release with the note that Walker is gone on Quattro. The 3.x series also had a long tail of walker and elephant packages disappearing or mismatching on upgrade, which is what issue #2546 and its siblings were about.

The upgrade path is explicit. `omarchy-upgrade-to-quattro` lists `omarchy-walker`, `walker-bin`, `elephant` and thirteen `elephant-*` packages in its retired set and removes them in one pacman transaction, with a dependency-aware fallback group so they come off together rather than failing one at a time.

## If that did not work

**The Apps menu is empty or says "Nothing here yet".** This is a real bug, not the redesign. Issue #11107 reports it as a regression in 4.0.3-1, still open as of 2026-09-16, with the Apps submenu caching an empty row set that never recovers in that session. The one cause pinned down so far is a cloned or third-party menu plugin: a clone of `omarchy.menu` gets a scoped shell API whose `appLibrary` is null, so its Apps list stays empty (issue #11028, also #10946 and #11307). Check what you have loaded and drop the clone:

```bash
omarchy plugin list
omarchy plugin remove <your-clone-id>
omarchy restart shell
```

One reporter on #11107 confirmed the stock launcher worked again once they deleted their own launcher plugin.

**Typing a query that matches nothing does nothing.** Walker had an elephant `websearch` provider that fell back to a browser search. The native menu has no such fallback. Issue #7012 tracks it and is still open. Two pull requests add a fallback to the menu (#7075 and #8012), and neither is merged as of 2026-09-16, so for now you need your own binding or menu entry.

**Flatpak apps do not show up.** Tracked separately in issue #8650, where the session `XDG_DATA_DIRS` misses the Flatpak export directories. Not a Walker issue.

**You are still on 3.x.** Different problem entirely. On 3.1.5 and later, install the meta package rather than the individual providers, then restart the services: `omarchy-pkg-add omarchy-walker` followed by `omarchy-restart-walker`. Full detail is on [command not found: elephant](/fix/command-not-found-elephant/).

**The shell itself is not running.** If neither shortcut does anything and the bar is missing too, the problem is upstream of the menu. See [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/).

## Related

- [Omarchy manual: Navigation](https://omarchy.org/manual/navigation/) and [Shell Plugins](https://omarchy.org/manual/shell-plugins/)
- [Upgrading 3 to 4 (Quattro)](/upgrade/3-to-4-quattro/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [Where did Waybar go](/fix/where-did-waybar-go/)
- [command not found: elephant](/fix/command-not-found-elephant/)
- [Keybindings reference](/reference/keybindings/)
- [Release v4.0.0](/releases/v4.0.0/)
