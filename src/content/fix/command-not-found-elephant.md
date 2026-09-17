---
title: "command not found: elephant"
description: "Omarchy 4 removed Walker and its elephant backend, so \"command not found: elephant\" means a stale script or a half-finished Quattro upgrade."
answer: "On Omarchy 4.x, elephant is gone on purpose: Quattro replaced Walker and its elephant providers with the Quickshell menu on Super + Space. Delete or repoint whatever still calls elephant, and rerun omarchy-upgrade-to-quattro if the upgrade stopped midway. On 3.x the command is missing because the packages were dropped, so reinstall the omarchy-walker meta package and restart the services."
appliesTo:
  from: "3.x"
status: by-design
category: apps
issueCount: 68
errorStrings:
  - "command not found: elephant"
  - "bash: elephant: command not found"
  - "zsh: command not found: elephant"
  - "Command not found: \"elephant\""
  - "error: target not found: elephant-bluetooth"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [elephant, walker, launcher, quattro, upgrade]
sources:
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro): Walker is gone, Super + Space opens the Omarchy menu"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.1.5"
    title: "Release v3.1.5: fix possibility for walker/elephant to brick on upgrading by introducing omarchy-walker meta package"
    kind: release
    author: "dhh"
    date: "2025-11-03"
  - url: "https://github.com/omacom/omarchy/issues/2546"
    title: "Issue #2546: Walker and Elephant missing after system upgrade"
    kind: issue
    author: "defaultdino"
    date: "2025-10-19"
  - url: "https://github.com/omacom/omarchy/issues/2548"
    title: "Issue #2548: Walker and Elephant missing after upgrade. Not open and show error. press win+space or win+alt+space"
    kind: issue
    author: "mir4zul"
    date: "2025-10-19"
  - url: "https://github.com/omacom/omarchy/issues/1738"
    title: "Issue #1738: After upgrading to the latest version, walker and elephant are gone"
    kind: issue
    author: "halilozercan"
    date: "2025-09-17"
  - url: "https://github.com/omacom/omarchy/issues/2638"
    title: "Issue #2638: Problem with Walker and Elephant after update"
    kind: issue
    author: "nmonev"
    date: "2025-10-20"
  - url: "https://github.com/omacom/omarchy/issues/7012"
    title: "Issue #7012: Menu launcher lost Walker's web-search fallback for no-match queries"
    kind: issue
    author: "Balmisjutas"
    date: "2026-08-15"
  - url: "https://omarchy.org/manual/navigation/"
    title: "Omarchy manual: Navigation"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Introduced the omarchy-walker meta package in v3.1.5 so walker and the elephant providers stop disappearing one by one, and pointed people at omarchy-restart-walker for the intermittent 3.x failure while its cause was traced"
  - name: "Balmisjutas"
    url: "https://github.com/Balmisjutas"
    for: "Documented which elephant provider behaviour did not survive the move to the native Quattro menu"
faq:
  - q: "Is elephant coming back in Omarchy 4?"
    a: "No. Quattro replaced Walker and every elephant provider with plugins inside the Quickshell process. Nothing in the 4.0.4 tree calls elephant, and the packages are on the retired list that the Quattro upgrade uninstalls."
  - q: "I am still on 3.x. Should I install elephant by hand?"
    a: "No. Install the omarchy-walker meta package instead. Individual elephant-* names fail with \"target not found\" once the repo stops shipping them separately."
  - q: "What replaced the elephant websearch provider?"
    a: "Nothing, as of 4.0.4. Issue #7012 tracks the missing web-search fallback for queries that match no app or command, and it is still open."
related: [walker-launcher-missing-after-update, where-did-waybar-go, migration-failed-mid-update, omarchy-update-fails-or-hangs]
draft: false
---

Elephant was the data backend behind Walker, the launcher Omarchy used from v1.6.0 through the 3.x series. Walker drew the window, elephant supplied the results: desktop applications, the calculator, clipboard history, emoji and symbols, files, bluetooth devices, web search, and the theme, background and unlock pickers inside the Omarchy menu. If a shell, a keybinding, or a script tries to run `elephant` and the binary is not installed, you get `command not found: elephant`.

What you do about it depends entirely on which major version you are on. Run `omarchy-version` first.

## The fix

### On Omarchy 4.x (4.0.0 through 4.0.4)

Elephant is supposed to be missing. Quattro removed it deliberately, so the goal is to stop whatever is still calling it.

1. Find the caller. Search your own config and dotfiles, since nothing shipped in 4.0.4 references the command:

   ```bash
   grep -rn "elephant" ~/.config ~/.local/bin ~/.bashrc ~/.zshrc 2>/dev/null
   ```

2. If the hits are in your own scripts, aliases, or Hyprland Lua bindings, repoint them at the Quattro equivalents:

   ```bash
   omarchy-menu toggle        # Super + Space, replaces omarchy-launch-walker
   omarchy-menu toggle apps   # Super + Alt + Space, the app list on its own
   omarchy-menu-clipboard     # replaces omarchy-launch-walker -m clipboard
   omarchy-menu-emoji         # replaces omarchy-launch-walker -m symbols
   omarchy-menu-file          # file picker
   ```

3. If the hits are only in leftover `~/.config/hypr/*.conf` files, ignore them. Quattro moved Hyprland config to Lua and leaves the old `.conf` files on disk, but it no longer loads them. See [the conf to Lua migration notes](/reference/hyprland-conf-to-lua-migration/).

4. If nothing in your config matches and the menu itself is broken, your upgrade probably stopped partway: the retired packages came off but the new shell never landed. Rerun the upgrade, which is written to be rerun:

   ```bash
   omarchy upgrade to quattro
   ```

5. Then restart the shell:

   ```bash
   omarchy-restart-shell
   ```

### On Omarchy 3.x (3.1.5 and later)

Reinstall the meta package, not the individual providers:

```bash
omarchy-pkg-add omarchy-walker
omarchy-restart-walker
```

`omarchy-walker` pulls in `walker` plus every `elephant-*` provider as one unit. Installing the pieces by hand is what produces `error: target not found: elephant-bluetooth` and the 404s for individual `elephant-*` package files.

### On Omarchy 3.x before 3.1.5

Update first. The meta package arrived in v3.1.5 on 2025-11-03 precisely because partial removals were bricking the launcher. Open a terminal with `Super + Return`, run `omarchy-update`, and if that finishes cleanly the migration installs `omarchy-walker` for you.

## Verify it worked

On 4.x:

```bash
omarchy-version                  # expect 4.0.4 or later
command -v elephant              # expect no output, that is correct
omarchy-shell shell ping         # the shell answers if it is running
```

There is no `omarchy-shell.service` to check on 4.x. The upgrade script lists that unit among the ones it retires, and Hyprland starts the shell itself through `omarchy-launch-shell` at login. Then press `Super + Space`. You should get the native Omarchy menu, and typing should filter apps and commands in the same box.

On 3.x:

```bash
pacman -Q omarchy-walker walker
systemctl --user status elephant.service app-walker@autostart.service
```

Both units should be active. `Super + Space` should open Walker without a "waiting for elephant" placeholder.

## Why it happens

Two different causes share one error string.

The 3.x cause was packaging. Walker and elephant were split across more than a dozen separate packages, and an interrupted or partially applied update could leave some installed and some gone. Several people hit this within hours of each other on 2025-10-19, including [#2546](https://github.com/omacom/omarchy/issues/2546) and [#2548](https://github.com/omacom/omarchy/issues/2548), and [#1738](https://github.com/omacom/omarchy/issues/1738) reported the same shape a month earlier on 3.0.1. In 3.x, `omarchy-launch-walker` starts `elephant` directly before launching Walker, so a missing binary surfaces the error the moment you press `Super + Space`. There was also an intermittent variant where both packages were present but Walker sat on its "Waiting for elephant..." placeholder. On [#2638](https://github.com/omacom/omarchy/issues/2638), collaborator ryanrhughes said that case was solved by `omarchy-restart-walker` while the root cause was still being traced with Walker's author. v3.1.5 addressed the packaging half by adding the `omarchy-walker` meta package.

The 4.x cause is by design. The v4.0.0 release notes state that Walker is gone and `Super + Space` now opens the Omarchy menu itself, with a native launcher merged into that menu inside the shell process. `omarchy-upgrade-to-quattro` lists `elephant` and thirteen `elephant-*` packages among the retired packages it uninstalls, removes `elephant.service` and `app-walker@autostart.service`, deletes `~/.config/elephant`, and drops the pacman hook that used to restart Walker. So on a 4.x box, anything calling `elephant` is either your own leftover customisation or an upgrade that did not finish.

## If that did not work

- The menu opens but a feature you used is missing. Not everything survived the rewrite. The elephant websearch fallback, where an unmatched query became a browser search, is gone and tracked in [#7012](https://github.com/omacom/omarchy/issues/7012), still open as of 4.0.4. Check [what replaces what](/switch/what-replaces-what/) before assuming your install is broken.
- The upgrade rerun fails. `omarchy-upgrade-to-quattro` stops with a message telling you to fix the error and rerun before rebooting. Work that error first, then see [migration failed mid-update](/fix/migration-failed-mid-update/).
- `Super + Space` does nothing at all on 4.x. That is a shell problem rather than an elephant problem. See [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/).
- You are looking for the old launcher generally rather than this one error. See [Walker launcher missing after update](/fix/walker-launcher-missing-after-update/).

## Related

- [Walker launcher missing after update](/fix/walker-launcher-missing-after-update/)
- [Where did Waybar go](/fix/where-did-waybar-go/)
- [Upgrading 3 to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Omarchy command reference](/reference/commands/)
- [Omarchy manual: Navigation](https://omarchy.org/manual/navigation/)
