---
title: "Typing Chinese on Omarchy 4 with fcitx5"
description: "Omarchy 4 already runs fcitx5 as a service. Add fcitx5-chinese-addons or Rime, pick a toggle key that is not Shift or Ctrl+Space, and verify it works."
answer: "Omarchy 4 already runs fcitx5 as a systemd user service for compose sequences, so you only need to add an engine. Run omarchy pkg add fcitx5-chinese-addons fcitx5-configtool, restart with omarchy restart xcompose, then add Pinyin in fcitx5-configtool. Do not rely on Shift as the toggle on 4.0.x, the default kb_options breaks it, and Ctrl+Space collides with the tmux prefix."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [chinese, fcitx5, input-method, rime, cjk, keyboard]
sources:
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy Manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://omarchy.org/manual/shell-plugins/"
    title: "Omarchy Manual: Shell Plugins"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/11456"
    title: "Issue #11456: Feature request: out-of-the-box Chinese input support, is it on the roadmap?"
    kind: issue
    author: "jamesMuWB"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/7440"
    title: "Issue #7440: shift:both_capslock_cancel (default kb_options) breaks fcitx5 Shift toggle for Chinese/English input"
    kind: issue
    author: "a-lang"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/7346"
    title: "Issue #7346: [Bug] Modifier key (Shift) release events dropped with fcitx5-rime, Shift cannot switch Chinese/English"
    kind: issue
    author: "jfdnet"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/4842"
    title: "Issue #4842: Ctrl+Space tmux prefix conflicts with fcitx5 input method toggle (introduced in v3.4.0)"
    kind: issue
    author: "hoornet"
    date: "2026-03-01"
  - url: "https://github.com/omacom/omarchy/issues/11303"
    title: "Issue #11303: [Bug] Fcitx5 candidate popup is invisible in Hyprland true fullscreen (SUPER+F)"
    kind: issue
    author: "CoderLambert"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7559"
    title: "Issue #7559: [Bug] Fcitx5/Mozc candidate window is misplaced in native Wayland Chromium and Electron apps"
    kind: issue
    author: "simosako"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/11682"
    title: "Issue #11682: omarchy-menu search field ignores IME composition (Korean/CJK via Fcitx5)"
    kind: issue
    author: "TAE58"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/9552"
    title: "Issue #9552: Default fcitx5 service breaks Hyprland multi-layout keyboard switching"
    kind: issue
    author: "je2020je"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/7461"
    title: "Issue #7461: omarchy-fcitx5.service restart-loops forever when a user autostart .desktop launches fcitx5 under a different filename"
    kind: issue
    author: "jkubo"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/pull/9695"
    title: "PR #9695: Add a Setup > Region toggle with Chinese language and input method"
    kind: pr
    author: "ZacharyZhang-NY"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy-pkgs/pull/265"
    title: "PR #265: Add rime-ice-installer, the Rime Ice Chinese input method setup TUI"
    kind: pr
    author: "ZacharyZhang-NY"
    date: "2026-09-01"
  - url: "https://github.com/ryuhzk/omarchy-ime"
    title: "ryuhzk/omarchy-ime: Omarchy bar plugin that owns Fcitx5 and Rime"
    kind: other
    author: "ryuhzk"
  - url: "https://github.com/gmaxxxie/omarchy-fcitx5-theme"
    title: "gmaxxxie/omarchy-fcitx5-theme: fcitx5 candidate box follows the Omarchy theme"
    kind: other
    author: "gmaxxxie"
credits:
  - name: "a-lang"
    url: "https://github.com/a-lang"
    for: "Traced the dead Shift toggle to the shift:both_capslock_cancel XKB mapping and published the kb_options workaround"
  - name: "jfdnet"
    url: "https://github.com/jfdnet"
    for: "Showed with fcitx5 key traces that Hyprland 0.56.2 drops Shift release events for Rime users"
  - name: "hoornet"
    url: "https://github.com/hoornet"
    for: "Documented the Ctrl+Space collision between the tmux prefix and the fcitx5 trigger key"
  - name: "CoderLambert"
    url: "https://github.com/CoderLambert"
    for: "Isolated the invisible candidate popup to Hyprland internal fullscreen state 2"
  - name: "simosako"
    url: "https://github.com/simosako"
    for: "Traced the misplaced candidate window in Chromium to the GNOME text-scaling-factor and found the --force-device-scale-factor=1 workaround"
  - name: "kazedayo"
    url: "https://github.com/kazedayo"
    for: "Tested the Restart=on-failure drop-in that stops the omarchy-fcitx5.service restart loop"
faq:
  - q: "Does Omarchy come with Chinese input already installed?"
    a: "No. Omarchy 4.0.4 installs fcitx5, fcitx5-gtk and fcitx5-qt as base packages, but only for CapsLock compose sequences. There is no Pinyin engine until you add fcitx5-chinese-addons or fcitx5-rime yourself. Making it work out of the box is an open feature request, issue #11456."
  - q: "Which toggle key should I use on Omarchy 4?"
    a: "Something that is neither Shift nor Ctrl+Space. Shift as a modifier-only trigger is broken on 4.0.x by the default kb_options and by a Hyprland regression. Ctrl+Space is the tmux prefix Omarchy ships. Super+Space is taken by the Omarchy menu. Ctrl+Shift+Space is the replacement a commenter in issue #4842 tested."
  - q: "Do I need to install a Chinese font?"
    a: "No. noto-fonts-cjk is already in omarchy-base.packages on both 3.8.4 and 4.0.4, so Han glyphs resolve through fontconfig fallback. If your terminal shows boxes, the app is pinning a font family rather than asking fontconfig for a fallback."
  - q: "Can I use Rime instead of the built-in Pinyin?"
    a: "Yes. Install fcitx5-rime, then add a schema. Rime Ice is the one both PR #9695's installer and the omarchy-ime plugin use. Be aware that issue #7346 reports Shift release events being dropped for Rime users on Hyprland 0.56.2, which breaks Rime's usual ascii_composer Shift toggle."
related: [layouts-and-locale, japanese-input-mozc, korean-input-hangul]
draft: false
---

Omarchy already runs the input method framework you need. What it does not ship is a Chinese engine. This page covers Omarchy 4.0.4, and calls out where 3.x and 4.0.x differ.

## The fix

1. Install the engine and the configuration tool. `noto-fonts-cjk` is already a base package, so you do not need to add it.

```bash
omarchy pkg add fcitx5-chinese-addons fcitx5-configtool
```

`fcitx5-chinese-addons` is the package the manual names. Upstream describes it as the Pinyin and table-based input methods for fcitx5. If you want Rime instead, use `fcitx5-rime` here and add a schema afterwards.

2. Restart fcitx5 so it picks up the new addon. Do not run `fcitx5 -d` by hand. On 4.x fcitx5 is a supervised systemd user service, and a second instance makes the unit restart loop.

```bash
omarchy restart xcompose
```

That wrapper stops `omarchy-fcitx5.service`, kills any stray `fcitx5`, then starts the unit again.

3. Open the configuration tool. Omarchy hides `fcitx5-configtool` from the launcher on purpose, so run it from a terminal.

```bash
fcitx5-configtool
```

4. In the Input Method tab, add **Pinyin** (or **Rime**) next to the existing `Keyboard - English (US)` entry. Keep the keyboard layout entry first in the list, so a fresh window starts in Latin mode.

5. In the Global Options tab, set the trigger key. Clear the default and bind something that Omarchy is not already using. `Ctrl+Shift+Space` is the one a commenter in issue #4842 tested on 4.0.2 and confirmed hands `Ctrl+Space` back to tmux. Avoid these three:

- `Ctrl+Space` is fcitx5's own default and it is also the tmux prefix Omarchy ships in `config/tmux/tmux.conf`. Issue #4842 covers the collision. If you keep it, tmux still answers on its second prefix, `Ctrl+B`.
- A bare `Shift` tap does not work on 4.0.x. See the known bugs below.
- `Super+Space` opens the Omarchy menu.

6. Log out and back in if you changed anything under `environment.d`. The variables are read by the systemd user manager at session start, not per process.

## Verify it worked

Check the service is up and has not been restarting:

```bash
systemctl --user status omarchy-fcitx5.service
systemctl --user show omarchy-fcitx5.service -p NRestarts
```

`NRestarts=0` is what you want. A number climbing every two seconds means the unit is losing to another fcitx5 that already owns the bus name, or cannot exec the binary at all. Issue #7461 collects three ways that happens, and the start rate limiter never trips because one cycle is just over two seconds.

Check the environment your apps actually see:

```bash
printenv | grep -E 'INPUT_METHOD|QT_IM_MODULE|XMODIFIERS|SDL_IM_MODULE'
```

On 4.0.4 those come from `/usr/lib/environment.d/10-omarchy-fcitx.conf` and should read `fcitx`, `fcitx`, `@im=fcitx` and `fcitx`. There is no `GTK_IM_MODULE`, and that is not a mistake. The 4.x file never had it, and an earlier migration (`1752292967.sh`, the UWSM switch) stripped it from the old user file for Wayland. Do not treat its absence as the bug.

Then run the framework's own health check:

```bash
fcitx5-diagnose | less
```

Look for your engine under the loaded addons and for a frontend line naming `wayland_v2`. Finally, open a terminal, press your toggle key, type `nihao`, and confirm a candidate bar appears.

## Why it happens

Omarchy installs `fcitx5`, `fcitx5-gtk` and `fcitx5-qt` in `install/omarchy-base.packages` on both 3.8.4 and 4.0.4, but it installs them for the CapsLock compose sequences, not for CJK. The unit description in `default/systemd/user/omarchy-fcitx5.service` says as much: it exists to turn `~/.XCompose` sequences into text for Wayland clients. No engine is included, so the framework is present and idle until you add one.

The plumbing moved in 4.0.0. On 3.8.4, fcitx5 was launched fire and forget from `~/.config/hypr/autostart.conf` with `exec-once = uwsm-app -- fcitx5 --disable notificationitem`, and the environment lived in `~/.config/environment.d/fcitx.conf`. Quattro replaced that with a supervised user unit (`Restart=always`, `RestartSec=2`, gated on `WAYLAND_DISPLAY`) and moved the environment file to a package-owned path. The Quattro upgrade retires your old `~/.config/environment.d/fcitx.conf` if it still matches a shipped hash. If you customised that file, your copy is kept and keeps winning, because `~/.config/environment.d` outranks `/usr/lib/environment.d` for a file of the same name.

## Known bugs on 4.0.x

These are all open against 4.0.x as of 2026-09-16.

**The Shift toggle does not work.** Two separate causes land on the same symptom. Issue #7440 shows that Omarchy's default `kb_options = "compose:caps,shift:both_capslock_cancel"` gives the Shift keys a two-level XKB mapping, so the release event arrives with a `Caps_Lock` keysym and fcitx5's modifier-only trigger never matches. The reporter's verified workaround is to drop the option in `~/.config/hypr/input.lua`:

```lua
hl.config({
  input = {
    kb_options = "compose:caps",
  },
})
```

Issue #7346 is the second cause, and it survives that change. On Hyprland 0.56.2, which 4.0.x ships, fcitx5-rime sees Shift presses but never the releases, so Rime's `ascii_composer` toggle never fires and the modifier is left stuck on. The reporter blamed the Hyprland keybinds refactor and posted a Rime Lua processor that toggles `ascii_mode` on press instead. A later commenter disputes the regression story: the same code is in 0.56.1, and they trace it to Hyprland merging key state across every keyboard device, so one stale key on a second HID interface eats releases. Their workaround is to disable the offending device with `hl.device({ name = "...", enabled = false })` in `~/.config/hypr/input.lua`. The upstream report was auto-closed, so nothing is queued to fix it. Bind a chord rather than a bare modifier.

**The candidate window misbehaves in some windows.** Issue #11303 reports the popup going invisible when a native Wayland terminal enters Hyprland true fullscreen with `Super+F`, while composing and committing keep working. Omarchy's `Super+Ctrl+F` tiled fullscreen avoids the bad state. Issue #7559 reports the candidate window failing to follow the caret in native Wayland Chromium and Electron apps, with XWayland unaffected. The thread traced that one to Omarchy's text size setting: anything other than 12 px writes a non-1 GNOME `text-scaling-factor`, Chromium folds it into its device scale, and the IME caret rectangle ends up in the wrong coordinate space. Both reproduce on stock Omarchy 4.0.x.

**The Omarchy menu itself cannot take IME input.** Issue #11682 shows the menu's search field collecting raw key events instead of using a Qt text input, so preedit never reaches it. Chinese, Japanese and Korean all hit this. Search the menu in Latin.

**Multi layout switching stops working.** Issue #9552 reports that with the fcitx5 service running, the bar's layout widget and `hyprctl switchxkblayout` change the label but not what you type, because fcitx5 commits through its own virtual keyboard pinned to `us`. The reporter's verified workaround is `systemctl --user disable --now omarchy-fcitx5.service`, which gets xkb switching back and loses the CapsLock compose sequences, and on this page loses your Chinese engine too. The issue's own analysis says the default fcitx5 profile only holds `keyboard-us` and nothing follows the compositor's layout list, which points at adding the second layout as a fcitx5 keyboard entry instead. Nobody in the thread has confirmed that route.

## If that did not work

- If the candidate box lands in the wrong place in Chromium or an Electron app, check `gsettings get org.gnome.desktop.interface text-scaling-factor`. If it is not `1.0`, either set the Omarchy text size back to 12 px or launch the app with `--force-device-scale-factor=1` (via `~/.config/chromium-flags.conf` for Chromium). Two commenters in issue #7559 tested `--enable-wayland-ime` for this and it changed nothing.
- If candidates render as empty boxes, the app is pinning a font family with no Han coverage. Omarchy's fontconfig maps `monospace` to JetBrainsMono Nerd Font, which has no CJK, and relies on fallback to `noto-fonts-cjk`. Name a CJK face explicitly in that app.
- If the service restart loops with `Unable to request dbus name` in the journal, look for a hand made `~/.config/autostart/*.desktop` that starts fcitx5. XDG autostart deduplication is by filename, so an entry under any name other than `org.fcitx.Fcitx5.desktop` escapes the `Hidden=true` mask Omarchy ships in `config/autostart/`. Remove it and restart the unit. If there is no such file, the second copy was D-Bus activated by the fcitx5 package's own service file; a commenter in issue #7461 tested a drop-in at `~/.config/systemd/user/omarchy-fcitx5.service.d/restart.conf` containing `[Service]` and `Restart=on-failure`, so the losing instance stops after one cycle.
- If the loop shows `status=203/EXEC` instead, `/usr/bin/fcitx5` is missing. The unit is enabled regardless of whether the package is present. `omarchy pkg add fcitx5` stops it.
- If nothing reaches the IME at all after an upgrade, confirm the unit is enabled: `systemctl --user is-enabled omarchy-fcitx5.service`.

## What is coming

PR #9695 by ZacharyZhang-NY, open since 2026-09-01, adds a **Setup > Region** toggle that flips between World and China. The China setting switches the system language to `zh_CN`, installs and runs a Rime Ice installer, makes Rime the active input method with Ctrl+Space as the toggle, and swaps the menu to Chinese labels. Its companion, omarchy-pkgs PR #265, packages that installer. Both were still open and unmerged when this page was checked, and the only review comment so far warns that Rime and fcitx5 grab Ctrl+~, a key VS Code uses; the author said they would look at it. Treat it as a proposal, not a shipped feature.

Two community projects exist in the meantime, both third party and unaffiliated with Omarchy. `ryuhzk/omarchy-ime` is a bar plugin that installs fcitx5 and Rime, generates their configuration, and puts a live input state indicator on the bar. `gmaxxxie/omarchy-fcitx5-theme` is a service plugin that repaints the fcitx5 candidate box whenever you run `omarchy theme set`. Read both repos before installing. The manual's Shell Plugins chapter is blunt that a plugin is code that runs for as long as your session does, with everything your user account can reach.

## Related

- Official manual: [Keyboard, Mouse, Trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/)
- Official manual: [Shell Plugins](https://omarchy.org/manual/shell-plugins/)
- [Keyboard layouts and locale](/keyboard/layouts-and-locale/)
- [Japanese input with Mozc](/keyboard/japanese-input-mozc/)
- [Korean input with Hangul](/keyboard/korean-input-hangul/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
