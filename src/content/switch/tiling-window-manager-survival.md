---
title: "Surviving a tiling window manager in Omarchy"
description: "How Omarchy 4's tiling window manager actually works, the twelve Hyprland keybindings that matter, and how to make it feel like macOS or Windows."
answer: "Learn twelve keys and stop fighting the layout. Super + Space launches, Super + K lists every binding, Super + W closes, Super + Arrow moves focus, Super + Shift + Arrow swaps windows, Super + 1 to 0 switches workspaces, Super + J flips a split, Super + T floats a window, Super + F fullscreens. Everything else is optional. Use workspaces the way you used to use overlapping windows."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [tiling, hyprland, keybindings, workspaces, floating, switching]
sources:
  - url: "https://omarchy.org/manual/navigation/"
    title: "Omarchy Manual: Navigation"
    kind: manual
  - url: "https://omarchy.org/manual/hotkeys/"
    title: "Omarchy Manual: Hotkeys"
    kind: manual
  - url: "https://omarchy.org/manual/coming-from-mac-or-windows/"
    title: "Omarchy Manual: Coming From Mac or Windows"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/9726"
    title: "Issue #9726: SUPER + J (togglesplit) raises \"no such layoutmsg for scrolling\" on scrolling-layout workspaces"
    kind: issue
    author: "johnwu"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8220"
    title: "Issue #8220: Super+J (togglesplit) errors on scrolling layout: 'no such layoutmsg for scrolling'"
    kind: issue
    author: "khru"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/12117"
    title: "Issue #12117: Alt+Tab does not follow adjacent windows in scrolling layout"
    kind: issue
    author: "DaDecky"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/10342"
    title: "Issue #10342: Hyprland 0.56.2 SIGSEGV on Super+T: grouped window keeps a dead workspace CSpace, toggleTargetFloating dereferences expired m_parent"
    kind: issue
    author: "Dayruke"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/11995"
    title: "Issue #11995: Inkscape's file dialogs tile instead of floating: it draws its own GTK chooser, not the portal's"
    kind: issue
    author: "omeganter"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/5101"
    title: "Issue #5101: Cant Increase Width on Last window when on Scrolling workspace Layout (Not dwindle)"
    kind: issue
    author: "rasyidrafi"
    date: "2026-03-23"
  - url: "https://github.com/omacom/omarchy/issues/9271"
    title: "Issue #9271: [hyprland] Steam main window defaults to small floating 1100x700 instead of tiled/maximizable"
    kind: issue
    author: "MAXI8594"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/discussions/4039"
    title: "Discussion #4039: windows navigation for floating to tiling mode (SUPER + ARROW)"
    kind: discussion
    author: "Muhammad-Jafar"
    date: "2025-12-31"
  - url: "https://github.com/omacom/omarchy/discussions/6624"
    title: "Discussion #6624: Feature Request: Workspace Overview (similar to GNOME Activities / macOS Mission Control)"
    kind: discussion
    author: "flaxrora"
    date: "2026-08-06"
  - url: "https://github.com/omacom/omarchy/discussions/7849"
    title: "Discussion #7849: macOS-style Super+Tab app switcher (external plugin)"
    kind: discussion
    author: "920four4"
    date: "2026-08-23"
  - url: "https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/"
    title: "Hyprland Wiki: Dwindle Layout"
    kind: docs
credits:
  - name: "johnwu"
    url: "https://github.com/johnwu"
    for: "Traced the Super + J error on scrolling workspaces to the unconditional togglesplit binding"
  - name: "omeganter"
    url: "https://github.com/omeganter"
    for: "Worked out why Inkscape's own GTK file chooser escapes Omarchy's floating dialog rules"
faq:
  - q: "Can I just drag windows around like I always did?"
    a: "Partly. Hold Super and drag with the left mouse button to move a window, or hold Super and drag with the right button to resize it. In the dwindle layout a dragged window swaps into the tile you drop it on rather than floating free, so it is repositioning, not free placement."
  - q: "How do I make one app always float?"
    a: "Add a window rule at the bottom of ~/.config/hypr/hyprland.lua, for example o.window(\"^(org\\\\.gnome\\\\.Calculator)$\", { float = true }). Find the class with hyprctl clients. Omarchy already floats portal dialogs, 1Password, Bitwarden, mpv, imv and its own TUI windows."
  - q: "Is there a Mission Control or Task View equivalent?"
    a: "Not in 4.0.4. There is no workspace overview screen, and it has been requested in discussion #6624. The nearest thing is Super + K for the full binding list and the workspace numbers on the top bar."
  - q: "Did the keybindings change in Omarchy 4?"
    a: "The tiling keys themselves are essentially the same as the tiling-v2 set in 3.8.4. What changed is where they live: Hyprland config moved from ~/.config/hypr/*.conf to Lua files, so you now write o.bind(...) instead of bindd = lines."
related: [from-macos, day-one-checklist, what-replaces-what]
draft: false
---

If you have spent twenty years dragging windows by their title bars, the first hour in Omarchy feels like the mouse broke. It did not. The model is just different, and it is small enough to learn in an afternoon. This page is checked against Omarchy 4.0.4 on Hyprland 0.56.2.

## The mechanism: windows do not have positions

In macOS and Windows a window has coordinates. You put it somewhere, it stays there, and it overlaps whatever was underneath.

In Omarchy a window has a slot in a tree. Open one app and it fills the screen. Open a second and the screen splits. Open a third and one of those halves splits again. You never choose a position, you choose a neighbour. Nothing overlaps, so nothing ever gets lost behind anything else.

Four concepts carry the whole system.

**Workspaces.** Ten of them, numbered 1 to 10, each with its own set of tiles. These do the job your overlapping windows used to do. Instead of stacking a browser on top of an editor, you put the browser on workspace 2 and jump between them instantly. The manual's [Navigation chapter](https://omarchy.org/manual/navigation/) makes the same point, and it is the single habit that makes tiling click.

**The tiling layout.** The default is dwindle: every new window splits the focused one, and every window on the workspace stays visible even as they shrink. Omarchy configures dwindle with `preserve_split = true` and `force_split = 2` in `/usr/share/omarchy/default/hypr/looknfeel.lua`. Per the [Hyprland wiki](https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/), `force_split = 2` means a new window always lands to the right of or below the focused one, so placement is predictable rather than cursor-dependent. `preserve_split` means a split keeps its orientation, which is also what makes `Super + J` work at all.

The alternative is the scrolling layout, a side-scrolling tape of columns that runs past the edge of the screen. `Super + L` toggles it, the choice is per workspace, and it persists across restarts.

**Floating.** The escape hatch. A floating window sits on top of the tiles with a free position and size, exactly like the desktop you came from. Omarchy already floats the things that should float: portal file dialogs, 1Password, Bitwarden, mpv, imv, and its own terminal utility windows, per `default/hypr/apps/system.lua`. Everything else tiles unless you say otherwise.

**Groups.** Several windows sharing one tile with a tab bar across the top, which is the closest thing to browser tabs for arbitrary apps.

## The twelve keybindings that matter

Verified against `default/hypr/bindings/tiling.lua`, `applications.lua` and `utilities.lua` in the 4.0.4 source.

| Keys | What it does |
| --- | --- |
| `Super + K` | Show every binding, searchable. The only one you must memorise. |
| `Super + Space` | The Omarchy menu. Your Spotlight, Raycast or Start menu. |
| `Super + Return` | Terminal. `Super + Shift + Return` for the browser. |
| `Super + W` | Close the focused window. The app really quits. |
| `Super + Arrow` | Move focus left, right, up or down. |
| `Super + Shift + Arrow` | Swap the focused window with its neighbour. |
| `Super + 1` to `Super + 0` | Jump to workspace 1 through 10. |
| `Super + Shift + 1` to `0` | Send the focused window to that workspace. |
| `Super + J` | Flip the current split between side by side and stacked. |
| `Super + T` | Toggle the focused window between tiled and floating. |
| `Super + F` | Fullscreen. `Super + Alt + F` for full width, keeping the bar. |
| `Super + -` and `Super + =` | Resize the focused window. Add Alt for smaller steps, Ctrl for bigger. |

That is enough to run the machine. Six more are worth learning in week two: `Super + O` pops a window out as floating and pinned so it follows you between workspaces, `Super + S` toggles the scratchpad overlay and `Super + Alt + S` sends a window there, `Super + G` groups windows into tabs, `Super + Tab` walks to the next workspace, `Alt + Tab` cycles windows on the current workspace, and `Super + L` switches the workspace between dwindle and scrolling. The full list is in the manual's [Hotkeys chapter](https://omarchy.org/manual/hotkeys/) and on [our keybindings reference](/reference/keybindings/).

The mouse is not dead either. Hold `Super` and drag with the left button to move a window, hold `Super` and drag with the right button to resize it.

## Five things that confuse everyone

**"My new window went somewhere odd."** It split whatever was focused, and because of `force_split = 2` it went right or below. If you wanted it elsewhere, focus the window you want it next to first, then launch. `Super + Shift + Arrow` fixes it after the fact.

**"Super + Arrow does nothing on this window."** Directional focus is built for tiles. Moving focus between a floating window and the tiled ones is not smooth, and it is an open request in [discussion #4039](https://github.com/omacom/omarchy/discussions/4039). Use `Alt + Tab` to reach a floating window, or `Super + T` to tile it.

**"Alt + Tab is not an app switcher."** It cycles windows on the current workspace only, not applications across the system. There is no macOS-style command-tab switcher in 4.0.4; someone proposed one as an external plugin in [discussion #7849](https://github.com/omacom/omarchy/discussions/7849). There is also no workspace overview screen, requested in [discussion #6624](https://github.com/omacom/omarchy/discussions/6624). Workspace numbers plus `Super + 1` to `0` is the intended replacement, and it is faster once it is muscle memory.

**"Super + J threw a red error."** You are on a scrolling workspace. `Super + J` sends `togglesplit`, which only exists in dwindle, so Hyprland raises "no such layoutmsg for scrolling". This is open and reported several times over, including [#8220](https://github.com/omacom/omarchy/issues/8220) and [#9726](https://github.com/omacom/omarchy/issues/9726). Press `Super + L` to go back to dwindle, or just do not use `Super + J` there. Scrolling has a couple of other rough edges: `Alt + Tab` follows internal order rather than the visible left-to-right order ([#12117](https://github.com/omacom/omarchy/issues/12117)), and widening the last column is reported broken in [#5101](https://github.com/omacom/omarchy/issues/5101).

**"This app opened tiny, or in the wrong mode."** Some apps guess wrong. Inkscape's file dialogs tile and become unusable because Inkscape draws its own GTK chooser instead of calling the portal ([#11995](https://github.com/omacom/omarchy/issues/11995)), and Steam's main window opens small and floating ([#9271](https://github.com/omacom/omarchy/issues/9271)). Both are window-rule problems, not tiling problems. Find the class with `hyprctl clients`, then add a rule at the bottom of `~/.config/hypr/hyprland.lua`:

```lua
o.window("^(com\\.example\\.App)$", { float = true })
```

## Making it feel like your old desktop

You can soften the edges without giving up tiling. Every file below is yours; Omarchy's defaults load first and your overrides win.

Natural scrolling and three-finger workspace swipes, in `~/.config/hypr/input.lua`:

```lua
hl.config({
  input = {
    touchpad = {
      natural_scroll = true,
    },
  },
})

hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
```

Rounded corners and no gaps, in `~/.config/hypr/looknfeel.lua`:

```lua
hl.config({
  decoration = { rounding = 8 },
  general = { gaps_in = 0, gaps_out = 0 },
})
```

Rebinding, in `~/.config/hypr/bindings.lua`. Unbind first, then bind:

```lua
hl.unbind("SUPER + W")
o.bind("SUPER + Q", "Close window", hl.dsp.window.close())
```

Two more that help ultrawide and large-display users: `Super + Shift + Backspace` toggles gaps and borders off, and `Super + Ctrl + Backspace` constrains a lone window to a square aspect ratio instead of stretching it across the whole panel. Omarchy 4 also added `Super + Alt + Home` to remember a window width and `Super + Home` to restore it, which is the closest thing to a saved layout.

If you are still reaching for a dock, do not add one. Give it the two weeks the manual asks for, then decide.

## What to watch for on newer versions

The tiling keys have been stable across 3.8.4 and the whole 4.0.x line, so muscle memory carries forward. What changed in 4.0.0 is the config format: Hyprland moved from `~/.config/hypr/*.conf` to Lua, and `bindd =` lines became `o.bind("SUPER + K", "Label", action)`. Old blog posts and videos showing `.conf` snippets still describe the right keys but the wrong syntax. See [the conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) and [upgrading 3 to 4](/upgrade/3-to-4-quattro/).

Two live bugs are worth knowing before you lean on a feature. `Super + T` on a grouped window can segfault Hyprland 0.56.2 ([#10342](https://github.com/omacom/omarchy/issues/10342)), so ungroup before floating. And the scrolling layout is clearly less finished than dwindle; if you are new, stay on dwindle until the reports above close.

The next release is announced as Quattro RS 4.5. After any major upgrade, press `Super + K` before assuming a binding survived, and re-read your own `~/.config/hypr/bindings.lua` for overrides that now collide with a new default.

## Related

- [Coming from macOS](/switch/from-macos/)
- [Day one checklist](/switch/day-one-checklist/)
- [Keybindings reference](/reference/keybindings/)
