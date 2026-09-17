---
title: "Typing Korean on Omarchy 4 with fcitx5-hangul"
description: "Omarchy 4 ships fcitx5 but no Korean engine and no Korean keyboard choice at install. Add fcitx5-hangul, register it, and type Hangul."
answer: "fcitx5 is already running in every Omarchy session, so all that is missing is the engine. Run `omarchy pkg add fcitx5-hangul fcitx5-configtool`, restart the unit with `systemctl --user restart omarchy-fcitx5.service`, then open fcitx5-configtool and add Hangul to your input method group below Keyboard - English (US). Toggle with the 한/영 key or Ctrl+Space. Korean fonts are already installed."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [korean, hangul, fcitx5, input-method, keyboard, cjk]
sources:
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy Manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://github.com/omacom/omarchy/pull/11719"
    title: "PR #11719: Add one-step Korean input setup"
    kind: pr
    author: "MoerAI"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/pull/9299"
    title: "PR #9299: Offer Korean as an install-time keyboard choice"
    kind: pr
    author: "ronaldlangeveld"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/11682"
    title: "Issue #11682: omarchy-menu search field ignores IME composition (Korean/CJK via Fcitx5)"
    kind: issue
    author: "TAE58"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/4842"
    title: "Issue #4842: Ctrl+Space tmux prefix conflicts with fcitx5 input method toggle (introduced in v3.4.0)"
    kind: issue
    author: "hoornet"
    date: "2026-03-01"
  - url: "https://github.com/omacom/omarchy/issues/7559"
    title: "Issue #7559: [Bug] Fcitx5/Mozc candidate window is misplaced in native Wayland Chromium and Electron apps"
    kind: issue
    author: "simosako"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/9580"
    title: "Issue #9580: CJK font fallback always selects Korean variant regardless of locale"
    kind: issue
    author: "usutani"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/discussions/10052"
    title: "Discussion #10052: Omarchy internationalization: current status and directions"
    kind: discussion
    author: "komagata"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/pull/11341"
    title: "PR #11341: Show Fcitx5 input method in the keyboard layout widget"
    kind: pr
    author: "Kaorw"
    date: "2026-09-11"
  - url: "https://github.com/yelixir-dev/omarchy-starter"
    title: "yelixir-dev/omarchy-starter: simple guide for omarchy linux starter in korea"
    kind: docs
    author: "yelixir-dev"
credits:
  - name: "MoerAI"
    url: "https://github.com/MoerAI"
    for: "Wrote the one-step D-Bus group rewrite and documented the xkb options for keyboards with no 한/영 key"
  - name: "ronaldlangeveld"
    url: "https://github.com/ronaldlangeveld"
    for: "Traced why Korean is missing from the installer's keyboard picker"
  - name: "TAE58"
    url: "https://github.com/TAE58"
    for: "Found that the Omarchy menu search field drops IME composition"
  - name: "hoornet"
    url: "https://github.com/hoornet"
    for: "Documented the Ctrl+Space clash between fcitx5 and the tmux prefix"
  - name: "yelixir-dev"
    url: "https://github.com/yelixir-dev"
    for: "Published a Korean-language Omarchy setup guide with a scripted fcitx5-hangul installer"
faq:
  - q: "Does Omarchy install a Korean input method by default?"
    a: "No. Through v4.0.4 the base package list installs fcitx5, fcitx5-gtk and fcitx5-qt for the CapsLock compose sequences, but no engine. You add fcitx5-hangul yourself."
  - q: "Why is Korean missing from the installer's keyboard list?"
    a: "Every entry in the picker resolves to a console keymap, and there is no Korean one in kbd. That is not much of a loss, because a Korean keyboard types Latin letters on the US map and Hangul is produced by the input method rather than the keymap. PR #9299 proposes adding Korean as a special case."
  - q: "Do I need extra fonts for Korean?"
    a: "No. noto-fonts-cjk is in Omarchy's base package list, so Hangul and Hanja render out of the box. You may want a Korean UI font for looks, but nothing is missing."
  - q: "Why does Ctrl+Space not reach tmux any more?"
    a: "fcitx5 grabs Ctrl+Space as its input method trigger before tmux sees it. Either use the 한/영 key to toggle Korean and drop Control+space from the fcitx5 trigger keys, or move your tmux prefix. See issue #4842."
related: [chinese-input-fcitx5, japanese-input-mozc, layouts-and-locale]
draft: false
---

Omarchy 4 gets you most of the way to Korean without telling you. The framework is already running. What is missing is one package and one registration step.

This page was checked against the v4.0.4 source tree (released 2026-09-15) and the open upstream threads listed below, not on a live Korean install.

## The fix

1. Install the Hangul engine and the fcitx5 configuration tool. Neither is in the base package list.

```bash
omarchy pkg add fcitx5-hangul fcitx5-configtool
```

2. Restart fcitx5 so it picks up the newly installed engine. On 4.0.x it runs as a user unit, so this is a systemd command, not a `pkill`.

```bash
systemctl --user restart omarchy-fcitx5.service
```

Omarchy also ships a wrapper that stops the unit, kills any stray process, and starts it again. Either works.

```bash
omarchy-restart-xcompose
```

3. Open the configuration tool. Omarchy hides `fcitx5-configtool` from the application launcher (it is listed in `default/omarchy/launcher.hides`), so start it from a terminal.

```bash
fcitx5-configtool &
```

4. In the left-hand list of the current input method group, keep **Keyboard - English (US)** first and add **Hangul** below it. Order matters: the first entry is what a new window starts in, and you want to land in English. Apply and close.

5. Toggle between English and Hangul with the **한/영** key on a Korean keyboard, or with **Ctrl+Space** on a keyboard that has no dedicated key. Both are fcitx5 defaults, so you do not need to configure a hotkey. Hanja conversion is on the **한자** key or **F9** by default, per PR #11719.

If you would rather not touch a GUI, you can register the engine over fcitx5's D-Bus interface instead. This rewrites the group named `Default` to hold the US keyboard plus Hangul, then saves it.

```bash
busctl --user call org.fcitx.Fcitx5 /controller \
  org.fcitx.Fcitx.Controller1 SetInputMethodGroupInfo 'ssa(ss)' \
  Default us 2 keyboard-us '' hangul ''
busctl --user call org.fcitx.Fcitx5 /controller \
  org.fcitx.Fcitx.Controller1 Save
```

That call is lifted from the scripted installer in the community repo [yelixir-dev/omarchy-starter](https://github.com/yelixir-dev/omarchy-starter), a Korean-language first-day guide for Omarchy. The proposed upstream command in PR #11719 uses the same D-Bus method but reads the current group first and appends `hangul` to whatever is already there. The two-line version above does not: it replaces the group wholesale, so if you already run another engine, add it back in the same call or use the GUI.

## Verify it worked

Check that fcitx5 is up and answering:

```bash
systemctl --user status omarchy-fcitx5.service
fcitx5-remote --check
```

Then open a terminal, press 한/영 or Ctrl+Space, and type `gks` on a Dubeolsik layout. You should see `한`. If you get the literal letters `gks`, the engine is registered but not active, or the window is not talking to fcitx5.

For a fuller report, run:

```bash
fcitx5-diagnose | head -60
```

The environment variables should already be correct. Omarchy ships `INPUT_METHOD`, `QT_IM_MODULE`, `XMODIFIERS` and `SDL_IM_MODULE` in `/usr/share/omarchy/default/environment.d/10-omarchy-fcitx.conf`, so there is nothing to add to your shell profile.

## Why it happens

Omarchy runs fcitx5 for a reason that has nothing to do with Korean. It is what turns the CapsLock compose sequences in `~/.XCompose` into text for Wayland clients. So `fcitx5`, `fcitx5-gtk` and `fcitx5-qt` are in the base package list, and since 4.0.0 a user unit called `omarchy-fcitx5.service` supervises the process. On 3.x the same binary was launched fire-and-forget from Hyprland's autostart, which is why older guides tell you to `pkill fcitx5 && fcitx5 -d`.

What Omarchy does not ship is any language engine. The official manual chapter [Keyboard, Mouse, Trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/) has a short section on non-Latin input that names `fcitx5-mozc` for Japanese and `fcitx5-chinese-addons` for Chinese. As of v4.0.4 it does not mention Korean or `fcitx5-hangul` at all. That is the whole reason this page exists.

The installer is a separate gap. The keyboard picker in `install/provisioning/setup-form.sh` offers 48 layouts, including Japanese as `jp106`, but there is no Korean entry. PR #9299 by ronaldlangeveld explains why. Each entry resolves to a console keymap and kbd does not ship a Korean one, and in any case a keymap is the wrong tool: a Korean keyboard produces Latin letters on the US map and it is the input method that turns them into Hangul. That PR proposes writing `KEYMAP=us` with `XKBLAYOUT=kr` and seeding a Hangul profile on first run. It was opened on 2026-08-31 and is still open.

Fonts are fine. `noto-fonts-cjk` is in the base package list, so Hangul and Hanja render without any extra install. Ironically, issue #9580 reports that Omarchy's sans-serif fallback chain reaches for the Korean variant of Noto Sans CJK for all CJK text regardless of locale, which is a problem for Japanese and Chinese users and a quiet convenience for Korean ones.

## If that did not work

**Hangul does not compose in the Omarchy menu.** This is a known bug, not your setup. Issue #11682 reports that the menu's search field is a plain QML `Item` collecting characters in `Keys.onPressed` rather than a real text input, so it never participates in Qt's input method protocol and preedit is dropped. Korean works in every other window on the same machine. The issue was filed on 2026-09-13 and is open. There is no workaround short of patching the menu plugin.

**Ctrl+Space stopped reaching tmux.** fcitx5 grabs it as a trigger key. Issue #4842 covers this. If you have a 한/영 key, remove `Control+space` from the trigger keys in `~/.config/fcitx5/config` and restart the unit. Otherwise move your tmux prefix.

**The candidate window floats in the wrong place in Chromium or Electron apps.** Issue #7559 reports the candidate popup not following the caret in native Wayland Chromium and Obsidian, while the same apps behave under XWayland. It was filed against Japanese input with Mozc. Nobody has reported it for Hangul yet. The report is about where the fcitx5 candidate popup lands in those apps, not about anything Mozc does, so Hanja candidate lists may well behave the same way. Still open.

Note a live disagreement here. PR #9299 adds `--enable-wayland-ime` to `config/chromium-flags.conf`, arguing Chromium ignores the compositor's text-input protocol without it. PR #11719 argues the opposite, that Chromium's text-input-v3 support is now enabled by default and the flag is obsolete. Omarchy's shipped `chromium-flags.conf` in v4.0.4 carries neither the flag nor a reason. If Hangul does not reach Chromium at all, adding the flag costs nothing and is worth trying.

**The top bar shows nothing when you switch to Hangul.** It will not. The bar's keyboard layout widget only knows about Hyprland's XKB layout, and switching an fcitx5 engine leaves that untouched. With a single `us` layout the widget stays hidden entirely, because `KeyboardLayout.qml` only shows it when more than one layout is configured. PR #11341 proposed showing `EN` or `KO` in that widget, but it is closed and unmerged. Do not count on a tray icon either: the shipped unit starts fcitx5 with `--disable notificationitem`, the addon that would register one. Run `fcitx5-remote` in a terminal to read the state (PR #11719 notes it reports `2` when an engine is active), or just type and see what comes out.

**You use Dvorak or Colemak.** According to the manual text drafted in PR #11719, Hangul input assumes a QWERTY physical mapping. Add a QWERTY entry to your fcitx5 group and switch to it before typing Korean.

**No 한/영 key and Ctrl+Space is taken.** xkb has options for this. PR #11719 points at `korean:ralt_hangul` and `korean:rctrl_hanja`, which turn Right Alt and Right Ctrl into the Hangul and Hanja keys. Add them to `kb_options` in `~/.config/hypr/input.lua`, keeping the shipped `compose:caps,shift:both_capslock_cancel` in the list so CapsLock compose keeps working. Not tested on this page.

## What to watch for on newer versions

Two open pull requests would change this page. PR #11719 by MoerAI adds an `omarchy setup input hangul` command and a Setup > Input Method menu entry that installs `fcitx5-hangul` and registers it for you in one step, plus a Typing in Korean section for the manual. PR #9299 adds Korean to the installer's keyboard picker. Neither had merged as of 2026-09-16, and neither is in v4.0.4.

Both sit under a broader effort. Discussion #10052, opened by komagata on 2026-09-03, surveys Omarchy internationalization across UI translation, documentation, input methods, fonts and locale, and states plainly that fcitx5 is installed but language engines are not configured, with no approach adopted yet. That is the thread to follow. If the next release, announced as Quattro RS 4.5, ships a one-step Korean setup, the steps above become unnecessary and the manual should finally name Korean.

## Related

- [Chinese input with fcitx5](/keyboard/chinese-input-fcitx5/)
- [Japanese input with Mozc](/keyboard/japanese-input-mozc/)
- [Keyboard layouts and locale](/keyboard/layouts-and-locale/)
- [Non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/)
