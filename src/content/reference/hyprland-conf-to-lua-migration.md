---
title: "Hyprland .conf to Omarchy 4 Lua migration"
description: "Port a customized Omarchy 3.x ~/.config/hypr/*.conf setup to Omarchy 4 Lua: the o.bind and hl.* API, worked examples, and why bindings.conf stopped loading."
answer: "Omarchy 4 loads ~/.config/hypr/hyprland.lua, which never sources your old .conf files. The upgrade leaves them on disk, unloaded and unbacked up, with no error. Port each one by hand: bind lines become o.bind, env lines become hl.env, sections become hl.config tables, monitor lines become hl.monitor, and windowrule lines become o.window."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-17
omarchyVersionTested: "4.0.4"
tags: [hyprland, lua, migration, quattro, keybindings, config]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6933"
    title: "Issue #6933: Quattro update preserves bindings.conf but silently stops loading custom keybindings"
    kind: issue
    author: "evo-social-world"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/6911"
    title: "Issue #6911: Quattro upgrade replaces customized monitors.conf with default monitors.lua (auto layout, GDK_SCALE=2) without porting or warning"
    kind: issue
    author: "daventhedude"
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
  - url: "https://omarchy.org/manual/dotfiles/"
    title: "Omarchy Manual: Dotfiles"
    kind: manual
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy Manual: Monitors"
    kind: manual
credits:
  - name: "evo-social-world"
    url: "https://github.com/evo-social-world"
    for: "First report that bindings.conf survives the upgrade but stops being loaded"
  - name: "alinuxfan"
    url: "https://github.com/alinuxfan"
    for: "Showed the same orphaning hits envs.conf and input.conf, not just bindings"
  - name: "daventhedude"
    url: "https://github.com/daventhedude"
    for: "Documented the monitors.conf case and the hl.monitor replacement"
  - name: "temper303"
    url: "https://github.com/temper303"
    for: "Spotted that the keybindings printer uses a different key-string dialect than hl.unbind"
  - name: "ryanmoreau-ctrl"
    url: "https://github.com/ryanmoreau-ctrl"
    for: "Reported and traced the code:N bind-string parse problem on 4.0.4"
  - name: "BSTail"
    url: "https://github.com/BSTail"
    for: "Reproduced the code:N report on other hardware and found that the broken binds must be unbound first"
faq:
  - q: "Does the upgrade delete my old .conf files?"
    a: "No. On 4.0.0 through 4.0.4 the old Hyprland .conf files (bindings, monitors, input, envs, looknfeel, autostart, hyprland.conf) are left exactly where they were. They are not renamed, not backed up with a .bak suffix, and not loaded. That is why the breakage is silent. Only hyprsunset.conf and xdph.conf are on the upgrade script's refresh list."
  - q: "Can I just source the old .conf from the new Lua config?"
    a: "There is no supported way to do it. hyprland.lua is the entry point and it only loads Lua, through dofile() and require(). Port the settings instead."
  - q: "Is there an o.rebind helper?"
    a: "Not in any 4.0.x release. On 4.0.4 you call hl.unbind() and then o.bind(). o.rebind exists only in the upstream development branch, so treat it as not yet available."
  - q: "How do I start over if I break the Lua config?"
    a: "Run omarchy-refresh-hyprland. It replaces the seven Omarchy-owned files in ~/.config/hypr with the shipped defaults and saves each changed file next to it as .bak.<timestamp>. Copy anything you want to keep first anyway; the backups are easy to lose track of."
related: [still-true-guides-and-videos]
draft: false
---

Omarchy 4.0.0 "Quattro" (2026-08-14) moved Hyprland configuration from hyprlang `.conf` files to Lua. The entry point is now `~/.config/hypr/hyprland.lua`. Everything checked here is against v4.0.4 (2026-09-15).

The important part is what the upgrade does not do. It writes the new Lua templates and leaves your old `.conf` files sitting in `~/.config/hypr/` untouched. Nothing sources them. Nothing renames them. `hyprctl configerrors` stays clean, because from Hyprland's point of view the files do not exist. Your customizations simply stop applying.

That is confirmed upstream for bindings ([#6933](https://github.com/omacom/omarchy/issues/6933), open), for monitors ([#6911](https://github.com/omacom/omarchy/issues/6911), open), and in a comment on #6933 for `envs.conf` and `input.conf` as well. Reading the v4.0.4 upgrade script backs this up: `hypr/bindings.lua`, `hypr/monitors.lua`, `hypr/input.lua`, `hypr/looknfeel.lua`, `hypr/autostart.lua`, `hypr/hyprland.lua` and `hypr/.luarc.json` are on an always-copy list, while the only `hypr/*.conf` entries in the whole file table are `hyprsunset.conf` and `xdph.conf` on the hash-matched refresh list. `bindings.conf`, `monitors.conf`, `input.conf`, `envs.conf`, `looknfeel.conf`, `autostart.conf` and `hyprland.conf` appear nowhere, so nothing renames or backs them up.

So the migration is manual. Here is how to do it exactly.

## Load order and the bootstrap preamble

The shipped `~/.config/hypr/hyprland.lua` starts like this:

```lua
dofile((os.getenv("OMARCHY_PATH") or "/usr/share/omarchy") .. "/default/hypr/bootstrap.lua")

require("default.hypr.omarchy")

require("hypr.monitors")
require("hypr.input")
require("hypr.bindings")
require("hypr.looknfeel")
require("hypr.autostart")

require("default.hypr.toggles")
```

`bootstrap.lua` clears cached modules so a reload re-reads your files, then puts three roots on `package.path`, in this order: `~/.local/state/`, `~/.config/`, and `$OMARCHY_PATH` (`/usr/share/omarchy`). That is why `require("hypr.bindings")` finds `~/.config/hypr/bindings.lua`, and why the current theme's override module `omarchy.current.theme.hyprland` resolves to `~/.local/state/omarchy/current/theme/hyprland.lua`.

Defaults load first, your files load second, so your files win. You can add your own modules: drop `~/.config/hypr/envs.lua` on disk and add `require("hypr.envs")` after the other requires.

If your `hyprland.lua` predates the `dofile(...)` line or lacks `~/.local/state/?.lua` on `package.path`, two shipped migrations patch it in place. If you hand-edited that preamble away, put it back.

## The two globals

`hl` is Hyprland's own Lua config API. `o` is Omarchy's helper table, defined in `/usr/share/omarchy/default/hypr/helpers.lua`. Read that file; it is short and it is the real documentation. The `.luarc.json` that ships in `~/.config/hypr/` declares both globals for lua-language-server, so a Lua LSP will not flag them.

## Bindings

Old 3.x forms, taken from the 3.8.4 defaults (`tiling-v2.conf`, `media.conf`, and the shipped `~/.config/hypr/bindings.conf`):

```ini
bindd = SUPER, W, Close window, killactive,
bindd = SUPER SHIFT, RETURN, Browser, exec, omarchy-launch-browser
bindeld = ,XF86AudioMute, Mute, exec, omarchy-swayosd-client --output-volume mute-toggle
bindeld = ,XF86MonBrightnessUp, Brightness up, exec, omarchy-brightness-display +5%
bindmd = SUPER, mouse:272, Move window, movewindow
unbind = SUPER, SPACE
```

What 4.0.4 ships for the same keys (the mute line dropped its repeat flag and the command behind it changed, so these are the current defaults rather than mechanical translations):

```lua
o.bind("SUPER + W", "Close window", hl.dsp.window.close())
o.bind("SUPER + SHIFT + RETURN", "Browser", { omarchy = "browser" })
o.bind("XF86AudioMute", "Mute", "omarchy-audio-output-volume mute-toggle", { locked = true })
o.bind("XF86MonBrightnessUp", "Brightness up", "omarchy-brightness-display +5%", { locked = true, repeating = true })
o.bind("SUPER + mouse:272", "Move window", hl.dsp.window.drag(), { mouse = true })
hl.unbind("SUPER + SPACE")
```

The rules:

- Every modifier and the key are joined with ` + `. `SUPER SHIFT, S` becomes `"SUPER + SHIFT + S"`.
- The suffix letters become options: `l` is `{ locked = true }`, `e` is `{ repeating = true }`, `m` is `{ mouse = true }`, `r` is `{ release = true }`, and `d` just means the description field is present. They combine, so `bindeld` is `{ locked = true, repeating = true }` plus a description.
- A plain string third argument is treated as a shell command and wrapped in `hl.dsp.exec_cmd` for you.
- Non-exec dispatchers become `hl.dsp.*` calls: `killactive` is `hl.dsp.window.close()`, `movefocus, l` is `hl.dsp.focus({ direction = "l" })`, `workspace, 3` is `hl.dsp.focus({ workspace = "3" })`, `movetoworkspace, 3` is `hl.dsp.window.move({ workspace = "3" })`, `togglefloating` is `hl.dsp.window.float({ action = "toggle" })`, `fullscreen, 0` is `hl.dsp.window.fullscreen({ mode = "fullscreen" })`.
- The description is now the second argument, and `nil` is allowed if you do not want the binding listed.

Table dispatchers are an Omarchy shortcut: `{ launch = "obsidian" }` prefixes `uwsm-app --`, `{ webapp = "https://..." }` calls the web app launcher, `{ tui = "cliamp", focus = true }` launches or focuses a TUI, and `{ omarchy = "browser" }` runs `omarchy-launch-browser`.

**To change a default you must unbind it first.** On 4.0.4 there is no combined helper, so write two lines:

```lua
hl.unbind("SUPER + SHIFT + F")
o.bind("SUPER + SHIFT + F", "File manager", { launch = "thunar" })
```

To start from nothing, set `omarchy_default_bindings = false` in `hyprland.lua` before `require("default.hypr.omarchy")`. To keep the window-manager bindings but drop the preinstalled app and web app ones, set `omarchy_preinstalled_bindings = false` instead.

## Environment variables

`env = LIBVA_DRIVER_NAME,nvidia` becomes `hl.env("LIBVA_DRIVER_NAME", "nvidia")`. No `envs.lua` ships, so put these at the bottom of `hyprland.lua`, in `monitors.lua` (the template already sets `GDK_SCALE` that way), or in your own required module. This is the case that bites hardest, because a dead `LIBVA_DRIVER_NAME` looks like a video decode regression, not a config problem.

## Monitors

```ini
env = GDK_SCALE,1
monitor = DP-2, 2560x1440@165, 0x0, 1, transform, 1
monitor = DP-3, disable
```

becomes

```lua
hl.env("GDK_SCALE", "1")
hl.monitor({ output = "DP-2", mode = "2560x1440@165", position = "0x0", scale = 1, transform = 1 })
hl.monitor({ output = "DP-3", disabled = true })
```

Trailing `key, value` pairs become named keys: `transform`, `vrr`, `mirror`, `disabled`. The catch-all `monitor=,preferred,auto,auto` is `hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })`. Note that the stock template sets `GDK_SCALE` to 2, which is wrong for a 1440p or 1080p panel at scale 1, so check that line first. Workspace pinning uses `hl.workspace_rule({ workspace = "3", layout = "scrolling" })`.

## Input, looknfeel, and other sections

Any hyprlang section becomes a nested table passed to `hl.config`. Sub-sections nest, and a `col.active_border` style key becomes a `col = { ... }` table:

```lua
hl.config({
  input = {
    kb_layout = "us,dk",
    kb_options = "compose:caps,grp:alts_toggle",
    repeat_rate = 40,
    touchpad = { natural_scroll = true, scroll_factor = 0.4 },
  },
  general = { gaps_in = 0, gaps_out = 0, border_size = 0 },
  decoration = { rounding = 8 },
})
```

Beziers and animations are separate calls rather than entries in an `animations` block: `hl.curve("easeOutQuint", { type = "bezier", points = { { 0.23, 1 }, { 0.32, 1 } } })` and `hl.animation({ leaf = "windows", enabled = true, speed = 3.79, bezier = "easeOutQuint" })`. Gradients are tables: `{ colors = { "rgba(33ccffee)", "rgba(00ff99ee)" }, angle = 45 }`. Gestures use `hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })`, and a single device is configured with `hl.device({ name = "...", enabled = false })`.

## Window rules

`windowrule = opacity 0.97 0.9, match:tag default-opacity` becomes `o.window({ tag = "default-opacity" }, { opacity = "0.985 0.96" })`. The helper takes a match first and rules second. A bare string match is shorthand for a class match:

```lua
o.window("qemu", { workspace = "5" })
o.window({ title = "(Picture.?in.?[Pp]icture)", class = "^firefox$" }, { float = true, pin = true, size = { 600, 338 } })
```

Layer rules use `hl.layer_rule({ match = { namespace = "..." }, no_anim = true })`. Hyprland's window rule syntax changes often between compositor releases, so check the [Hyprland wiki](https://wiki.hypr.land/Configuring/Basics/Window-Rules/) rather than copying old rules verbatim.

## Autostart

`exec-once = uwsm-app -- my-service` becomes `o.launch_on_start("my-service")`, which adds the `uwsm-app --` wrapper itself. For something that should not go through uwsm, use `o.exec_on_start("my-command")`.

## Verify it worked

```bash
hyprctl reload
hyprctl configerrors
hyprctl binds | grep -A3 "SUPER"
omarchy menu keybindings --print
hyprctl getoption input:kb_options
hyprctl monitors all
```

A Lua syntax error shows up in `hyprctl configerrors`, but a setting you forgot to port does not. Check the values, not just the absence of errors. When you are done, move the old files aside so nobody trusts them later:

```bash
mkdir -p ~/hypr-conf-archive
mv ~/.config/hypr/*.conf ~/hypr-conf-archive/
cp ~/hypr-conf-archive/hyprsunset.conf ~/hypr-conf-archive/xdph.conf ~/.config/hypr/
```

Keep `hyprsunset.conf` and `xdph.conf` in place. Those two are still `.conf` on 4.0.4, read by separate processes, and `hyprctl` neither applies nor validates them.

## Gotchas that cost people time

The keybindings printer and the Lua API disagree on key-string format. `omarchy menu keybindings --print` shows `SUPER SHIFT + S`, but `hl.unbind` needs `"SUPER + SHIFT + S"`. Paste the printed form into `hl.unbind` and nothing is removed; the default keeps working and no error is raised. That is [#7627](https://github.com/omacom/omarchy/issues/7627), still open.

There is an open report, [#12050](https://github.com/omacom/omarchy/issues/12050) filed on 2026-09-16 against 4.0.4, that `"MODS + code:N"` bind strings do not resolve their keycode in the Lua bind parser, so every bind sharing a modifier set fires together and a stock `SUPER + RETURN` walks through all ten workspace binds. A second user reproduced it on different hardware on 2026-09-17. There is no maintainer response yet, so treat it as a lead rather than a fact. If you see several bindings fire at once, check `hyprctl binds` for `key:` entries that still contain `code:` with `keycode: 0`. The reproducer's workaround was to `hl.unbind` each affected `code:` spec and rebind it with a plain key name. Rebinding without the unbind stacked the new bind next to the broken one.

Config-flag toggles moved too. Omarchy 3.x sourced `~/.local/state/omarchy/toggles/hypr/*.conf`; 4.x loads every `.lua` file in that directory instead.

## What to watch for on newer versions

The six user templates in `~/.config/hypr/` are byte-identical across v4.0.0 through v4.0.4, so nothing about this migration changed inside the 4.0 series. `o.shell_succeeds` and `o.notify` in the defaults did change, but neither affects a user config.

The upstream development branch adds `o.rebind(keys, description, dispatcher, options)`, which is just `hl.unbind` followed by `o.bind`, and the shipped `bindings.lua` comments are rewritten around it. It is not in any 4.0.x release. Write the two-line form today and it will keep working either way.

If you want to start clean, `omarchy-refresh-hyprland` replaces the seven Omarchy-owned files in `~/.config/hypr` with the shipped defaults, saving a `.bak.<timestamp>` copy of each one that differed.

## Related

- Official manual: [Dotfiles](https://omarchy.org/manual/dotfiles/) and [Monitors](https://omarchy.org/manual/monitors/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- [What Omarchy migrations do](/upgrade/what-migrations-do/)
- [Keybindings reference](/reference/keybindings/)
