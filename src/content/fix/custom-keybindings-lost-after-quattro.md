---
title: "Custom keybindings stopped working after upgrading to Omarchy 4"
description: "Omarchy 4 Quattro stopped loading ~/.config/hypr/bindings.conf. Port your custom keybindings to bindings.lua with o.bind and hl.unbind, then reload Hyprland."
answer: "Omarchy 4 moved the Hyprland config to Lua. Your old ~/.config/hypr/bindings.conf is still on disk but nothing loads it, and there is no error. Copy each custom binding into ~/.config/hypr/bindings.lua using o.bind(\"SUPER + SHIFT + R\", \"SSH\", \"command\") and hl.unbind(\"SUPER + SPACE\"), then run hyprctl reload. Check the other orphaned .conf files too."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 59
errorStrings: []
tags: [keybindings, quattro, hyprland, lua, migration, bindings-lua]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6933"
    title: "Issue #6933: Quattro update preserves bindings.conf but silently stops loading custom keybindings"
    kind: issue
    author: "evo-social-world"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7627"
    title: "Issue #7627: keybindings --print uses a different format than hl.unbind / o.bind"
    kind: issue
    author: "temper303"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/12050"
    title: "Issue #12050: [hyprland] Lua binds written as \"MODS + code:N\" don't parse"
    kind: issue
    author: "ryanmoreau-ctrl"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 release notes: convert the Hyprland configuration to Lua"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/dotfiles/"
    title: "Omarchy manual: Dotfiles"
    kind: manual
  - url: "https://omarchy.org/manual/hotkeys/"
    title: "Omarchy manual: Hotkeys"
    kind: manual
credits:
  - name: "evo-social-world"
    url: "https://github.com/evo-social-world"
    for: "Reported the silent orphaning of bindings.conf on two machines and published the working o.bind translation"
  - name: "temper303"
    url: "https://github.com/temper303"
    for: "Found that the printed keybinding format does not match the syntax hl.unbind and o.bind expect"
  - name: "ryanmoreau-ctrl"
    url: "https://github.com/ryanmoreau-ctrl"
    for: "Showed that MODS + code:N bind specs are not parsed by the Lua bind API"
faq:
  - q: "Did the update delete my old keybindings?"
    a: "No. ~/.config/hypr/bindings.conf is still there with every line intact. Omarchy 4 simply never reads it, because the Hyprland entry point is now ~/.config/hypr/hyprland.lua and it only requires the .lua override files. That is why the shortcuts fail with no error and no missing file."
  - q: "Will a future update port the file for me?"
    a: "Nothing has shipped for it. Issue #6933 was opened on 2026-08-15 and was still open on 2026-09-16, through 4.0.1, 4.0.2, 4.0.3 and 4.0.4. Treat the manual port as the fix for now."
  - q: "Can I just keep my 3.x defaults instead of Omarchy's?"
    a: "Yes. Put omarchy_default_bindings = false in ~/.config/hypr/hyprland.lua above require(\"default.hypr.omarchy\") and define everything yourself in bindings.lua. Setting omarchy_preinstalled_bindings = false instead keeps the window-manager bindings and drops only the preinstalled app and web app shortcuts."
  - q: "Is it safe to edit bindings.lua, or will an update overwrite it?"
    a: "It is safe. The Omarchy migration that refreshes bindings.lua compares the file against known stock checksums first and only replaces it when it is still untouched. An edited file is left alone."
related: [monitors-conf-replaced-by-monitors-lua, hyprland-lua-attempt-to-index-nil-global-o, where-did-waybar-go, walker-launcher-missing-after-update, omarchy-update-fails-or-hangs]
draft: false
---

Omarchy 4.0.0 "Quattro" moved the Hyprland configuration from `.conf` files to Lua. The release notes describe it as converting bindings, monitors and toggles to "expressive Lua". Your old `~/.config/hypr/bindings.conf` survives the upgrade untouched, but nothing loads it any more, so every custom shortcut in it stops working. There is no error banner and `hyprctl configerrors` stays clean, which is what makes this hard to spot.

This was verified on 4.0.4 (2026-09-15) and reported against 4.0.0-1 in issue [#6933](https://github.com/omacom/omarchy/issues/6933). On 3.x, `~/.config/hypr/hyprland.conf` carried a `source = ~/.config/hypr/bindings.conf` line. On 4.x, `~/.config/hypr/hyprland.lua` calls `require("hypr.bindings")`, which loads `~/.config/hypr/bindings.lua` and nothing else.

## The fix

1. List the files that went inert:

   ```bash
   ls ~/.config/hypr/*.conf
   ```

   Anything printed here is dead weight on 4.x. `bindings.conf` is the one people notice, but `input.conf`, `envs.conf`, `looknfeel.conf` and window rules left in `hyprland.conf` are equally ignored.

2. Print only the lines you actually wrote:

   ```bash
   grep -vE '^\s*(#|$)' ~/.config/hypr/bindings.conf
   ```

3. Open the new override file. Either press `Super + Space` and pick Setup > Keybindings, which opens `~/.config/hypr/bindings.lua` in your editor, or edit it directly:

   ```bash
   $EDITOR ~/.config/hypr/bindings.lua
   ```

4. Translate each line. The dispatcher goes in as a plain string for a shell command, and the description that `bindd` used to carry becomes the second argument:

   | 3.x `bindings.conf` | 4.x `bindings.lua` |
   | --- | --- |
   | `bind = SUPER SHIFT, R, exec, my-script` | `o.bind("SUPER + SHIFT + R", nil, "my-script")` |
   | `bindd = SUPER SHIFT, R, SSH, exec, my-script` | `o.bind("SUPER + SHIFT + R", "SSH", "my-script")` |
   | `unbind = SUPER, SPACE` | `hl.unbind("SUPER + SPACE")` |
   | `bind = SUPER, S, togglesplit` | `o.bind("SUPER + S", "Split", hl.dsp.layout("togglesplit"))` |
   | `bind = SUPER, H, movefocus, l` | `o.bind("SUPER + H", "Focus left", hl.dsp.focus({ direction = "l" }))` |
   | `bind = SUPER SHIFT, H, swapwindow, l` | `o.bind("SUPER + SHIFT + H", "Swap left", hl.dsp.window.swap({ direction = "l" }))` |
   | `bindr = ...` | fourth argument `{ release = true }` |
   | `bindl = ...` | fourth argument `{ locked = true }` |
   | `bindm = ...` | fourth argument `{ mouse = true }` |

   For graphical apps, prefer the table forms Omarchy's own defaults use, because they wrap the command in `uwsm-app` for you: `{ launch = "obsidian", focus = "^obsidian$" }`, `{ webapp = "https://example.com" }`, `{ tui = "cliamp", focus = true }`.

5. To change a default, unbind it first, then bind your own. Binding on top of an existing combination does not replace it:

   ```lua
   hl.unbind("SUPER + SPACE")
   o.bind("SUPER + SPACE", "Omarchy menu", "omarchy-menu toggle root")
   ```

6. Reload:

   ```bash
   hyprctl reload
   ```

   That is exactly what `omarchy-restart-hyprctl` runs.

7. Once the new bindings work, move the old files out of the way so you do not read them again by mistake:

   ```bash
   mkdir -p ~/omarchy-3x-conf-backup
   mv ~/.config/hypr/*.conf ~/omarchy-3x-conf-backup/
   ```

## Verify it worked

Press the shortcut. If it does nothing, check the live bind table:

```bash
hyprctl binds | grep -B2 -A4 'your description'
```

A bind registered from Lua shows up with the dispatcher `__lua`, which is normal on 4.x. What matters is that the entry exists and that `key` holds the key you expect.

`omarchy-menu-keybindings --print` lists everything with descriptions, which is the quickest way to see whether your entry landed. Do not copy its output back into Lua verbatim. The printed combo joins the modifiers with spaces and puts a single `+` before the key (`SUPER SHIFT + S`), but the Lua helpers want a `+` after every token (`SUPER + SHIFT + S`). temper303 reported in [#7627](https://github.com/omacom/omarchy/issues/7627) that an `hl.unbind` written in the printed form does nothing and the default stays bound, with no error to tell you why. That issue is still open on 4.0.4.

Finally, run `hyprctl configerrors`. A syntax error anywhere in `bindings.lua` stops the whole file from compiling, so one typo can take out every binding in it, not just the broken line.

## Why it happens

Quattro replaced the whole Hyprland config layer. The upgrade path installs fresh stock copies of `hypr/hyprland.lua`, `hypr/bindings.lua`, `hypr/input.lua`, `hypr/looknfeel.lua`, `hypr/monitors.lua` and `hypr/autostart.lua`, backing up any file already at those paths with a `.omarchy-upgrade-to-quattro.<timestamp>.bak` suffix. The old `.conf` files are not in that list, so they are neither converted nor removed. They just stop being sourced.

The upgrade script does detect a live legacy config: it builds a temporary `.conf` shim so the running 3.x session survives the package swap until you reboot. What it does not do is tell you that your own `.conf` customizations will be inert on the other side. In #6933, the reporter found a working `binddr` dictation binding still sitting in `bindings.conf` while `hyprctl binds -j` showed no matching entry at all. Commenters on the same thread reported the same pattern for `envs.conf` NVIDIA variables, `input.conf` keyboard options and `looknfeel.conf` settings, so treat this as a whole-directory problem rather than a bindings problem.

## If that did not work

**The binding is registered but fires the wrong thing, or a plain `SUPER` chord walks you through workspaces.** Avoid `code:N` in your own bindings. Issue [#12050](https://github.com/omacom/omarchy/issues/12050), opened 2026-09-16 against a stock 4.0.4 config, reports that the Lua bind API does not resolve a spec like `"SUPER + code:10"`. Hyprland keeps the literal text as the key name with a zero keycode, and the result is that all binds on that modifier set fire together. Use key names such as `"SUPER + 1"` while that is open.

**A punctuation key does nothing.** Use the xkbcommon keysym name in lower case. Omarchy's own defaults bind `"SUPER + comma"` with a source comment noting that the upper-case `COMMA` does not match.

**Your bindings load but everything Omarchy ships is gone.** Check whether `omarchy_default_bindings = false` or `omarchy_preinstalled_bindings = false` is set in `~/.config/hypr/hyprland.lua`. The second is also implied by a `~/.local/state/omarchy/preinstalls-removed` marker file.

**`hyprctl configerrors` reports `attempt to index a nil value (global 'o')`.** That is a different problem: your `hyprland.lua` is not loading Omarchy's helper module. See [/fix/hyprland-lua-attempt-to-index-nil-global-o/](/fix/hyprland-lua-attempt-to-index-nil-global-o/).

**Your monitor layout also reverted.** Same cause, different file. See [/fix/monitors-conf-replaced-by-monitors-lua/](/fix/monitors-conf-replaced-by-monitors-lua/).

## Related

- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/) for what else the Quattro upgrade changes under your home directory
- [/reference/hyprland-conf-to-lua-migration/](/reference/hyprland-conf-to-lua-migration/) for the full `.conf` to Lua mapping
- [/reference/keybindings/](/reference/keybindings/) for the 4.0.4 default shortcut list
- [/reference/commands/omarchy-menu-keybindings/](/reference/commands/omarchy-menu-keybindings/)
- The official manual chapters [Dotfiles](https://omarchy.org/manual/dotfiles/) and [Hotkeys](https://omarchy.org/manual/hotkeys/)
