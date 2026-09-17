---
title: "Upgrading Omarchy 3.x to 4 (Quattro)"
description: "What the Omarchy 3.x to 4 Quattro upgrade changes, what omarchy-upgrade-to-quattro actually does, and which of your configs silently stop loading."
answer: "Run Update > Omarchy first, then Update > Omarchy to Quattro (or omarchy upgrade to quattro). It is one way, so take a snapshot. The upgrade swaps Omarchy from a git checkout to pacman packages and from Hyprland .conf files to Lua. Your old bindings.conf, monitors.conf and input.conf stay on disk but stop being loaded, so port them into the .lua files by hand after the reboot."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [upgrade, quattro, hyprland, lua, migration, config]
sources:
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0: The Quattro Release"
    kind: release
    date: "2026-08-14"
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
  - url: "https://github.com/omacom/omarchy/issues/6878"
    title: "Issue #6878: Quattro upgrade drops non-US keyboard layout when vconsole.conf only has KEYMAP"
    kind: issue
    author: "cempack"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/8357"
    title: "Issue #8357: omarchy-upgrade-to-quattro force-overwrites shell.json instead of migrating it, silently dropping bar/plugin config"
    kind: issue
    author: "Orneyfish"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8996"
    title: "Issue #8996: Quattro upgrade silently drops all saved Wi-Fi networks in the iwd to NetworkManager switch"
    kind: issue
    author: "orospakr"
    date: "2026-08-29"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
credits:
  - name: "evo-social-world"
    url: "https://github.com/evo-social-world"
    for: "Traced custom bindings.conf entries being kept on disk but never loaded after the Quattro upgrade"
  - name: "daventhedude"
    url: "https://github.com/daventhedude"
    for: "Found that a customized monitors.conf is left unreferenced while a stock monitors.lua takes over"
  - name: "cempack"
    url: "https://github.com/cempack"
    for: "Identified the vconsole.conf KEYMAP vs XKBLAYOUT fallback that drops non-US keyboard layouts"
  - name: "Orneyfish"
    url: "https://github.com/Orneyfish"
    for: "Pinpointed shell.json being force-copied from the stock default instead of merged"
  - name: "orospakr"
    url: "https://github.com/orospakr"
    for: "Documented saved Wi-Fi profiles being stranded in /var/lib/iwd during the NetworkManager switch"
faq:
  - q: "Can I roll back from Quattro to Omarchy 3?"
    a: "Not with a command. The upgrade script itself warns that upgrading to Quattro is one way and that you cannot downgrade. Your only realistic route back is the Snapper or Limine snapshot taken before the upgrade, so confirm that snapshot exists first."
  - q: "Do I have to reinstall to get Omarchy 4?"
    a: "No. A 3.8.x machine upgrades in place. Run Update > Omarchy to get current on 3.x, then Update > Omarchy to Quattro. A fresh install is only needed if you want a clean slate."
  - q: "Why did my keybindings stop working after the upgrade?"
    a: "Omarchy 4 loads ~/.config/hypr/bindings.lua and never sources the old bindings.conf. Your old file is still there, which makes the setup look intact. Re-add each custom binding as an o.bind(...) call in bindings.lua."
  - q: "Where did ~/.config/omarchy/current go?"
    a: "Theme state moved to ~/.local/state/omarchy/current. The upgrade rewrites references in alacritty, foot, ghostty, kitty and the Hyprland config, but anything you wrote yourself that points at the old path needs updating by hand."
related: [before-you-update-checklist, rollback-with-snapper-and-limine, what-migrations-do]
draft: false
---

Omarchy 4.0.0 "Quattro" shipped on 2026-08-14 and is the largest change the project has made. Two things move at once. Omarchy itself stops being a git checkout in `~/.local/share/omarchy` and becomes a set of pacman packages under `/usr/share/omarchy`. And the whole desktop shell, previously eight separate programs, becomes one long-running Quickshell process. As a side effect, the Hyprland configuration you edit moves from `.conf` files to Lua.

This page is checked against v4.0.4 (2026-09-15), reading the upgrade script shipped in the v4.0.0 and v4.0.4 trees.

## Before you start

1. Get current on 3.x first. The release notes tell you to run `Update > Omarchy`, then `Update > Omarchy to Quattro`. The CLI form is `omarchy upgrade to quattro`.
2. Copy your customized files somewhere outside `~/.config`. At minimum: `hypr/bindings.conf`, `hypr/monitors.conf`, `hypr/input.conf`, `hypr/envs.conf`, `hypr/looknfeel.conf`, `hypr/autostart.conf`, and any window rules you added to `hypr/hyprland.conf`.
3. Write down your saved Wi-Fi passwords, or export them. See the Wi-Fi note below.
4. Confirm you have a working snapshot. The script calls `omarchy-snapshot create` before it touches anything, but it only warns if that fails, it does not stop.
5. Have a wired connection or a phone hotspot available.

The script prints its own warning before you confirm: upgrading to Quattro is one way, and you cannot downgrade from it. Treat the snapshot as your only rollback.

## What replaces what

Eight components were retired in favour of the single `omarchy-shell` process:

| Omarchy 3.x | Omarchy 4 |
| --- | --- |
| Waybar | Quickshell bar plugin, draggable to any screen edge |
| Walker | the Omarchy menu itself on `SUPER + SPACE`, plus a native emoji picker |
| Mako | the shell's own notification daemon, with do-not-disturb and replayable history |
| SwayOSD | native volume, brightness and media OSDs |
| hyprlock | shell lock screen with password and fingerprint PAM flows |
| hypridle | idle handling inside the shell, configured in `~/.config/omarchy/shell.json` |
| swaybg | background drawn by the shell |
| polkit-gnome | polkit agent as a shell plugin |

The same upgrade retires a long list of other defaults, including `iwd`, `impala`, `bluetui`, `wiremix`, `pavucontrol`, `playerctl`, `satty`, `walker-bin` and the `elephant-*` providers. Network management switches to NetworkManager.

Configuration moves in parallel:

| Omarchy 3.x path | Omarchy 4 path |
| --- | --- |
| `~/.config/hypr/hyprland.conf` | `~/.config/hypr/hyprland.lua` |
| `~/.config/hypr/bindings.conf` | `~/.config/hypr/bindings.lua` |
| `~/.config/hypr/monitors.conf` | `~/.config/hypr/monitors.lua` |
| `~/.config/hypr/input.conf` | `~/.config/hypr/input.lua` |
| `~/.config/hypr/looknfeel.conf` | `~/.config/hypr/looknfeel.lua` |
| `~/.config/hypr/autostart.conf` | `~/.config/hypr/autostart.lua` |
| `~/.config/hypr/hyprlock.conf`, `hypridle.conf` | gone, shell settings instead |
| `~/.config/omarchy/current/` | `~/.local/state/omarchy/current/` |

`hyprsunset.conf` and `xdph.conf` are still plain `.conf` files in 4.0.4.

The Lua files use a small DSL on top of Hyprland: `o.bind("SUPER + K", "Label", "command")` to add a binding, `hl.unbind("SUPER + SPACE")` to drop a default, `hl.monitor({ output = "DP-2", mode = "2560x1440@144", position = "0x0", scale = 1 })` for displays, and `hl.env("GDK_SCALE", "1")` for environment variables. Full detail is in [the .conf to Lua migration reference](/reference/hyprland-conf-to-lua-migration/).

## What the upgrade actually runs

`omarchy-upgrade-to-quattro` is a single self-contained script, around 2,400 lines. In the 4.0.4 copy the top-level sequence is:

- suppress live Hyprland config reloads so the running session does not throw errors mid-swap
- take a Snapper snapshot
- rewrite `/etc/pacman.d/mirrorlist` to the Omarchy mirror for your channel, keeping a timestamped `.bak`
- refresh the Arch and Omarchy keyrings, remove the legacy installer package, stray Limine configs and known-conflicting packages
- run `pacman -Syu` with `omarchy-keyring`, `omarchy-settings`, `omarchy-nvim` and `omarchy` as the core set
- normalize the Limine config and verify the kernel `root=` parameters are preserved
- apply the system transition: SDDM, NetworkManager, DNS, firewall defaults
- apply the user transition: move `~/.local/share/omarchy` aside as a `.bak`, symlink it to `/usr/share/omarchy`, copy the new Lua config entry points into `~/.config/hypr` (backing up anything already there), rewrite theme paths
- disable retired user services, then remove the retired packages (57 in the list) in one pacman transaction, with dependency-aware fallbacks
- run a final full package upgrade, then pending migrations, then refresh the active theme
- prompt for a reboot, which is the real cutover

The v4.0.0 copy runs a few of the late steps in a slightly different order; the page describes 4.0.4.

Useful flags: `--yes` to skip the confirmation, `--reboot` to reboot automatically, `--channel stable|rc|edge`, and `--user USER`. If the script exits partway it prints "Upgrade incomplete - do NOT reboot" and tells you re-running is safe.

## What silently breaks

These are the failures that produce no error at all, only wrong behaviour after the reboot. All five issues were still open on 2026-09-16, after 4.0.4 shipped.

**Custom keybindings stop firing.** `hyprland.lua` requires `hypr.bindings`, which is the new `bindings.lua`. Nothing sources the old `bindings.conf`, and the old file is left in place, so the config looks intact. `hyprctl configerrors` is clean because there is no error, the file is simply not read ([#6933](https://github.com/omacom/omarchy/issues/6933)). Check with `hyprctl binds -j` and port each binding to an `o.bind(...)` call. Follow-up reports on the same thread show the same thing happening to `envs.conf` (NVIDIA video-decode variables), `looknfeel.conf` (`vrr`, `allow_tearing`, animations) and window rules left in `hyprland.conf`, so treat every `.conf` you edited as dead.

**Multi-monitor layouts reset.** The upgrade always installs the stock `monitors.lua`, which is a single auto-placed, preferred-mode monitor with `GDK_SCALE=2`. A customized `monitors.conf` is not ported, not backed up, and not mentioned in the output ([#6911](https://github.com/omacom/omarchy/issues/6911)). Rotated monitors, custom positions and GTK scaling all come back wrong.

**Non-US keyboard layouts fall back to `us`.** The packaged `default/hypr/input.lua` reads `XKBLAYOUT` from `/etc/vconsole.conf`. Installs that only have `KEYMAP=fr` and a `kb_layout = fr` in the old `input.conf` end up on QWERTY ([#6878](https://github.com/omacom/omarchy/issues/6878)).

**Bar and plugin config resets on a re-run.** `omarchy/shell.json` is in the always-copy list, so an existing customized file is replaced by the stock default. It is backed up first, as `shell.json.omarchy-upgrade-to-quattro.<timestamp>.bak`, but nothing tells you ([#8357](https://github.com/omacom/omarchy/issues/8357)). A stock 3.8.x install has no `shell.json` (the bar lived in `waybar/config.jsonc`), so a first upgrade from 3.x loses nothing here. The reproduction on that thread shows it bites machines that were already on a Quattro RC or edge build, and anyone who re-runs the script after a partial failure: the same always-copy list carries `monitors.lua`, `bindings.lua` and `input.lua`, so a re-run resets those too, and the script ends by running `omarchy bar defaults` regardless.

**Saved Wi-Fi networks disappear.** The iwd to NetworkManager switch does not convert saved profiles. `nmcli connection show` comes back empty after the reboot. The credentials still exist in `/var/lib/iwd/`, which is root-only, but `iwd` and `impala` have been removed by then ([#8996](https://github.com/omacom/omarchy/issues/8996)).

## After the reboot

```bash
hyprctl binds -j | head            # are your custom bindings live?
hyprctl monitors all               # correct modes, positions, transforms?
hyprctl getoption input:kb_layout  # right layout?
nmcli connection show              # saved Wi-Fi still there?
omarchy-migrate                    # any migrations still pending?
ls ~/.config/hypr/*.conf           # leftover 3.x files you still need to port
find ~/.config -name '*.omarchy-upgrade-to-quattro.*.bak'
```

Anything in that last listing is a file the upgrade replaced. Diff each one against its new counterpart before deleting it.

## If something went wrong

Reboot and pick the pre-upgrade snapshot from the Limine boot menu. That is the documented rollback path, and after Quattro it is the only one, since there is no downgrade command. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

## What to watch for on newer versions

None of the five issues above were listed as fixed in the 4.0.1, 4.0.2, 4.0.3 or 4.0.4 release notes, all of which were dominated by security fixes, agent integrations and the new `linux-omarchy` kernel. Assume you still have to port `bindings.conf`, `monitors.conf` and `input.conf` by hand, and re-check the five issues above before any later upgrade.

One naming caution: the "Notices" chapter in the official manual is about the date, weather and battery hotkey popups, not about the notification daemon that replaced Mako. They are different things in the same shell.

## Related

- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Hyprland .conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
- [What migrations do](/upgrade/what-migrations-do/)
- [Official manual: Updates](https://omarchy.org/manual/updates/)
