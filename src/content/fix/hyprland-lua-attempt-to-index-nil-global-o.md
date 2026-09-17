---
title: "attempt to index a nil value (global 'o')"
description: "Hyprland starts with no bindings, no monitors and a config-error banner after Quattro. Your hyprland.lua never loads Omarchy's helpers, so the global o is nil."
answer: "Your ~/.config/hypr/hyprland.lua is an old copy that never loads Omarchy's helpers, so the global o is nil and every default module fails. Switch to a TTY with Ctrl+Alt+F2 and run omarchy refresh hyprland, which backs up your file and restores the stock entrypoint. Then re-add your personal lines to hypr/bindings.lua and hypr/monitors.lua instead."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 6
errorStrings:
  - "attempt to index a nil value (global 'o')"
  - "require(\"default.hypr.autostart\"): attempt to index a nil value (global 'o')"
  - "Runtime error in lua:"
tags: [hyprland, lua, quattro, config, migration]
sources:
  - url: "https://github.com/omacom/omarchy/issues/5879"
    title: "Issue #5879: Existing ~/.config/hypr/hyprland.lua not migrated to load default.hypr.helpers after 4.0 update"
    kind: issue
    author: "Cyrus-n8n"
    date: "2026-05-16"
  - url: "https://github.com/omacom/omarchy/issues/5822"
    title: "Issue #5822: dev commit e916491c9f1805be292ed274e59d99921c71398b breaks all hyprland lua files"
    kind: issue
    author: "danieldonaldson"
    date: "2026-05-14"
  - url: "https://github.com/omacom/omarchy/issues/5814"
    title: "Issue #5814: hyprland user config broken"
    kind: issue
    author: "felixzsh"
    date: "2026-05-14"
  - url: "https://github.com/omacom/omarchy/issues/5824"
    title: "Issue #5824: New update breaks hyperland"
    kind: issue
    author: "AdrianMora8"
    date: "2026-05-15"
  - url: "https://github.com/omacom/omarchy/issues/5911"
    title: "Issue #5911: Missing migration: helpers.lua not loaded in existing hyprland.lua after update"
    kind: issue
    author: "luizo"
    date: "2026-05-19"
  - url: "https://github.com/omacom/omarchy/issues/7103"
    title: "Issue #7103: Migration 1781063758 can truncate a customized hyprland.lua to two lines"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/pull/11222"
    title: "PR #11222: Stop the bootstrap migration truncating a customized hyprland.lua"
    kind: pr
    author: "vovarbv"
    date: "2026-09-10"
  - url: "https://omarchy.org/manual/dotfiles/"
    title: "Omarchy Manual: Dotfiles"
    kind: manual
credits:
  - name: "Cyrus-n8n"
    url: "https://github.com/Cyrus-n8n"
    for: "Traced the error to helpers.lua never being required from the user entrypoint"
  - name: "alipadron"
    url: "https://github.com/alipadron"
    for: "Posted the one-line require fix with the surrounding config context"
  - name: "felixzsh"
    url: "https://github.com/felixzsh"
    for: "Pointed people at omarchy refresh hyprland as the recovery command"
  - name: "vovarbv"
    url: "https://github.com/vovarbv"
    for: "Showed the bootstrap migration can truncate a hand-edited hyprland.lua"
faq:
  - q: "Will omarchy refresh hyprland delete my customizations?"
    a: "It overwrites the seven shipped files in ~/.config/hypr with the Omarchy defaults, but omarchy-refresh-config copies each one to <file>.bak.<timestamp> first. Your old content is still on disk, so you can copy your bindings back out of the backup."
  - q: "Can I just downgrade Hyprland instead?"
    a: "No. On 4.x the Lua config is the only config. The channel switch that dhh recommended in May 2026 applied to Omarchy 3.8 running against Hyprland 0.55, before Quattro shipped. Going back to stable on 4.0.4 does not give you a .conf setup."
  - q: "Why does the error name autostart.lua when I never edited it?"
    a: "Every Omarchy default module calls o.something on its first lines. The module that fails first is just the first one your entrypoint requires. The broken file is your hyprland.lua, not the module named in the error."
related: [where-did-waybar-go, custom-keybindings-lost-after-quattro, monitors-conf-replaced-by-monitors-lua, migration-failed-mid-update, quickshell-crashes-or-bar-missing]
draft: false
---

Hyprland comes up with the red config-error banner, no keybindings, no monitor layout and no autostarted apps. `hyprctl configerrors` lists the same message once per Omarchy module:

```
require("default.hypr.autostart"): .../default/hypr/autostart.lua:1: attempt to index a nil value (global 'o')
require("default.hypr.bindings.media"): .../media.lua:2: attempt to index a nil value (global 'o')
```

The file at fault is always `~/.config/hypr/hyprland.lua`, not the module the error names.

## The fix

You probably cannot open the Omarchy menu or a terminal, because the bindings that launch them never loaded. Get a text console first.

1. Press `Ctrl + Alt + F2` and log in at the TTY prompt.
2. Look at the top of your entrypoint:

   ```bash
   head -6 ~/.config/hypr/hyprland.lua
   ```

   A healthy 4.x file starts with a `dofile(...)` line ending in `/default/hypr/bootstrap.lua` and, a few lines down, `require("default.hypr.omarchy")`. If either is missing, that is your bug.
3. Restore the shipped entrypoint:

   ```bash
   omarchy refresh hyprland
   ```

   This runs `omarchy-refresh-hyprland`, which copies each of `hyprland.lua`, `bindings.lua`, `monitors.lua`, `input.lua`, `looknfeel.lua`, `autostart.lua` and `.luarc.json` from `/usr/share/omarchy/config/hypr` into `~/.config/hypr`. Every file it replaces is saved first as `<file>.bak.<unix-timestamp>` in the same directory, and the command prints a diff of what changed.
4. Log out and back in, or reboot.
5. Copy your personal lines out of the `.bak.` files into `~/.config/hypr/bindings.lua` and `~/.config/hypr/monitors.lua`. Do not put them back into `hyprland.lua`. The stock entrypoint loads those override files after the defaults for exactly this reason.

### If you want to keep your hyprland.lua as it is

Two lines are enough. Edit `~/.config/hypr/hyprland.lua` from the TTY and make sure the top of the file reads:

```lua
dofile((os.getenv("OMARCHY_PATH") or "/usr/share/omarchy") .. "/default/hypr/bootstrap.lua")

require("default.hypr.omarchy")
```

Everything that uses `o` must come after those, including your own `require("hypr.bindings")` and any `o.window(...)` you added at the bottom. Then log out and back in.

If your file still carries the older 4.0 alpha preamble (a hand-built `package.path = ...` block and `require("default.hypr.paths")`), the minimal repair people used in May 2026 was to add `require("default.hypr.helpers")` before the first `require("default.hypr.*")` line. That works, but on 4.0.4 you are better off moving to the bootstrap `dofile`, because the bootstrap also adds `~/.local/state/?.lua` to the search path, and the current theme and toggle modules live there.

## Verify it worked

From a graphical session:

```bash
hyprctl reload
hyprctl configerrors
```

Omarchy's own agent notes use that pair as the validation step after any Lua config change. A clean result prints no errors. Then check that the things that were missing are back: `Super + K` opens the keybindings list, `Super + Space` opens the menu, and your wallpaper and bar are up.

## Why it happens

In Quattro the global `o` is not a Hyprland builtin. It is created by `/usr/share/omarchy/default/hypr/helpers.lua`, which starts with `o = o or {}` and then hangs `o.bind`, `o.window`, `o.launch_on_start` and the rest off that table. Nothing else defines it. `helpers.lua` is loaded on the first line of `default/hypr/omarchy.lua`, which is the single entry point the shipped `hyprland.lua` requires.

So `o` is nil whenever your entrypoint reaches a default module without going through `default.hypr.omarchy` first. Three real ways that happens:

- **You carried an old `hyprland.lua` forward.** A file written during the 4.0 alpha requires `default.hypr.autostart` and friends directly, with no helpers line. This is what issue #5879 documents, and what issues #5814, #5822 and #5824 were all hitting in May 2026 on the dev and edge channels.
- **Your `package.path` still points at the 3.x location.** Before 4.0, `OMARCHY_PATH` was `$HOME/.local/share/omarchy`. On 4.x it is `/usr/share/omarchy`, because Omarchy is a pacman package now. A restored dotfiles copy of the old preamble searches a directory that no longer holds the defaults, so every `require("default.hypr.*")` fails and `o` never gets defined.
- **You reordered the requires.** Putting `require("hypr.bindings")` above `require("default.hypr.omarchy")` runs your `o.bind` calls before `o` exists.

Omarchy ships migration `1781063758.sh` ("Update Hyprland Lua entrypoint to load Omarchy bootstrap", dated 2026-06-10) to rewrite the old preamble into the bootstrap `dofile` automatically. It is present in every 4.0.x tag from 4.0.0 through 4.0.4. It skips any file that already contains `/default/hypr/bootstrap.lua`, which is why fresh 4.0 installs are never affected.

The migration is also why this page says workaround rather than fixed. Issue #7103, filed by an automated QA pass in August 2026 and still open, shows the migration's awk swallowing every line after the trigger until it finds a standalone `.. package.path` line. If you had rewrapped that assignment or appended your own path entry, there is no such line, so it reads to end of file and writes back a two-line config with no backup. PR #11222 rewrites it to consume the assignment by its continuation lines and to save a copy as `hyprland.lua.omarchy-bootstrap.bak` first. That PR was still open on 2026-09-16.

## What changed between 3.x and 4.x

On 3.8.4, the last 3.x release, `~/.config/hypr` held `hyprland.conf`, `bindings.conf`, `monitors.conf` and the rest. There was no Lua and no `o`. The May 2026 reports in this cluster came from people on the dev and edge channels running a pre-release Lua config against Hyprland 0.55, and dhh's answer at the time was to go back to the stable channel via *Update > Channel > Stable*. That advice is dead on 4.x. Quattro moved the whole config to Lua, and there is no `.conf` path to fall back to.

## If that did not work

- **`omarchy refresh hyprland` ran but nothing changed.** Check that the command actually wrote: if `~/.config/hypr/hyprland.lua` is a symlink into a dotfiles repo managed by stow or chezmoi, the refresh updates the target and your repo copy wins on the next sync. Fix the file in the repo instead.
- **Still broken after the refresh.** Two people in issue #5879 reported that only removing the whole directory worked. Move it aside rather than deleting it: `mv ~/.config/hypr ~/hypr.broken && omarchy refresh hyprland`, then reboot and pull your edits back from `~/hypr.broken`.
- **Your `hyprland.lua` is now two lines long.** That is issue #7103. Look for a Snapper snapshot, but note that Omarchy snapshots the root subvolume only, so `/home` is not in it. In practice `omarchy refresh hyprland` plus rewriting your bindings is the recovery.
- **A different Lua error, such as `Runtime error in lua:` or a `bad_any_cast` crash.** Those are separate faults in Hyprland 0.56 rather than a missing `o`. See [/releases/still-broken/](/releases/still-broken/).
- **The error appeared during an update rather than after one.** See [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/).

The manual chapter that covers these files is [Dotfiles](https://omarchy.org/manual/dotfiles/). It lists what each `~/.config/hypr/*.lua` file is for and shows the `hl.unbind` plus `o.bind` pattern for replacing a default binding.

## Related

- [/fix/custom-keybindings-lost-after-quattro/](/fix/custom-keybindings-lost-after-quattro/)
- [/fix/monitors-conf-replaced-by-monitors-lua/](/fix/monitors-conf-replaced-by-monitors-lua/)
- [/reference/hyprland-conf-to-lua-migration/](/reference/hyprland-conf-to-lua-migration/)
- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/)
- [/upgrade/what-migrations-do/](/upgrade/what-migrations-do/)
- [/reference/commands/omarchy-refresh-hyprland/](/reference/commands/omarchy-refresh-hyprland/)
