---
title: "Japanese input on Omarchy 4 with fcitx5-mozc"
description: "Set up Japanese typing on Omarchy 4.0.x: install fcitx5-mozc, register it with the running fcitx5, pick a toggle key, and fix the Chromium and fullscreen gaps."
answer: "fcitx5 is already running in every Omarchy 4 session, so you only add the engine. Run `omarchy pkg add fcitx5-mozc fcitx5-configtool`, restart the service with `omarchy restart xcompose`, then run `fcitx5-configtool` from a terminal and add Mozc to your input method group. Toggle with Ctrl+Space. If Chromium ignores the IME, add `--enable-wayland-ime` to its flags file."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [keyboard, japanese, mozc, fcitx5, input-method, cjk]
sources:
  - url: "https://github.com/omacom/omarchy/pull/9634"
    title: "PR #9634: Add one-step Japanese input setup"
    kind: pr
    author: "komagata"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/12139"
    title: "PR #12139: Enable Wayland input methods in Chromium-based browsers"
    kind: pr
    author: "akitaonrails"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/7559"
    title: "Issue #7559: [Bug] Fcitx5/Mozc candidate window is misplaced in native Wayland Chromium and Electron apps"
    kind: issue
    author: "simosako"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/11303"
    title: "Issue #11303: [Bug] Fcitx5 candidate popup is invisible in Hyprland true fullscreen (SUPER+F)"
    kind: issue
    author: "CoderLambert"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7440"
    title: "Issue #7440: shift:both_capslock_cancel (default kb_options) breaks fcitx5 Shift toggle for Chinese/English input"
    kind: issue
    author: "a-lang"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/9552"
    title: "Issue #9552: Default fcitx5 service breaks Hyprland multi-layout keyboard switching (bar label switches, typing doesn't)"
    kind: issue
    author: "je2020je"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/11682"
    title: "Issue #11682: omarchy-menu search field ignores IME composition (Korean/CJK via Fcitx5), Keys.onPressed path bypasses Qt input method"
    kind: issue
    author: "TAE58"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/10050"
    title: "Issue #10050: Default Voxtype type mode can corrupt longer Japanese/CJK dictation through wtype"
    kind: issue
    author: "komagata"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/10452"
    title: "Issue #10452: [JIS keyboard] Window resize shortcuts are misleading because they use US physical key labels"
    kind: issue
    author: "simosako"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/pull/12142"
    title: "PR #12142: Follow the Omarchy theme in the fcitx5 candidate window"
    kind: pr
    author: "akitaonrails"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/7461"
    title: "Issue #7461: omarchy-fcitx5.service restart-loops forever when a user autostart .desktop launches fcitx5 under a different filename"
    kind: issue
    author: "jkubo"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/pull/11719"
    title: "PR #11719: Add one-step Korean input setup"
    kind: pr
    author: "MoerAI"
    date: "2026-09-13"
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy Manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://github.com/komagata/omarchy-input-method"
    title: "komagata/omarchy-input-method: Omarchy bar widget for Fcitx 5 input methods"
    kind: other
    author: "komagata"
  - url: "https://github.com/Praveensenpai/omarchy-japanese-ime"
    title: "Praveensenpai/omarchy-japanese-ime: Japanese (Mozc) and English input method toggle widget"
    kind: other
    author: "Praveensenpai"
  - url: "https://github.com/fcitx/fcitx5/blob/master/src/lib/fcitx/globalconfig.cpp"
    title: "fcitx5 globalconfig.cpp: default trigger and group-enumerate keys"
    kind: other
  - url: "https://docs.komagata.org/6462"
    title: "Omarchyの日本語対応を手伝いたい人のためのまとめ"
    kind: blog
    author: "komagata"
    date: "2026-09-08"
credits:
  - name: "komagata"
    url: "https://github.com/komagata"
    for: "Wrote the one-step Mozc setup PR and the D-Bus group registration it uses"
  - name: "akitaonrails"
    url: "https://github.com/akitaonrails"
    for: "Pointed out that fcitx5-configtool is hidden from the launcher and reported Chromium dropping the IME until --enable-wayland-ime was set"
  - name: "a-lang"
    url: "https://github.com/a-lang"
    for: "Traced the broken Shift toggle to Omarchy's default shift:both_capslock_cancel"
  - name: "je2020je"
    url: "https://github.com/je2020je"
    for: "Showed that fcitx5 overrides Hyprland xkb layout switching once it is running"
faq:
  - q: "Do I need to install fcitx5 first?"
    a: "No. Omarchy ships fcitx5, fcitx5-gtk and fcitx5-qt in the base package list and runs fcitx5 as a supervised user service, because the CapsLock compose sequences depend on it. You only add the Japanese engine."
  - q: "Why does Japanese input work everywhere except my browser?"
    a: "Possibly because it needs --enable-wayland-ime, which Omarchy 4.0.4 does not put in config/chromium-flags.conf. PR #12139 proposes shipping it; PR #11719 argues current Chromium no longer needs it. If your browser drops the IME, add the flag to ~/.config/chromium-flags.conf and restart it."
  - q: "Can I just edit ~/.config/fcitx5/profile by hand?"
    a: "It usually does not stick. fcitx5 rewrites that file from its live state when it exits, so an edit made while fcitx5 is running gets overwritten. Use fcitx5-configtool, or stop fcitx5 before editing."
  - q: "Is there a one-click setup in the Omarchy menu?"
    a: "Not in 4.0.4. PR #9634 adds Setup > Input Method > Mozc (Japanese) to the menu, but it was still open on 2026-09-16."
related: [layouts-and-locale, chinese-input-fcitx5, korean-input-hangul]
draft: false
---

Omarchy does most of the work for you already, and that is the part people miss. fcitx5 is not an optional extra. It has been in the base package list since the 3.x releases, and since 4.0.0 it runs as a supervised systemd user service, because the whole CapsLock compose system depends on it. The fonts are there too: `noto-fonts-cjk` is in the base package list, so Japanese renders before you type any of it.

What is missing is the engine and one line in a config file. The official manual covers this in one paragraph of the [Keyboard, Mouse, Trackpad chapter](https://omarchy.org/manual/keyboard-mouse-trackpad/), which tells you to install `fcitx5-mozc` and `fcitx5-configtool` and stops there. This page fills in the rest.

Checked against v4.0.4 (2026-09-15).

## The fix

1. Install the engine and the config tool.

```bash
omarchy pkg add fcitx5-mozc fcitx5-configtool
```

2. Restart the fcitx5 service so it discovers the new engine. Omarchy 4 supervises fcitx5 with a systemd user unit, so do not just `pkill` it.

```bash
omarchy restart xcompose
```

That wrapper stops `omarchy-fcitx5.service`, kills any stray `fcitx5` process, and starts the unit again. The stray-kill matters: a second fcitx5 that finds the D-Bus name already taken exits cleanly, so if a copy started outside the unit is still alive, systemd will report a successful restart while the old process keeps serving.

3. Add Mozc to your input method group.

```bash
fcitx5-configtool
```

In the left pane, add **Mozc** to the current group. Keep a keyboard layout entry (`Keyboard - English (US)`, or `Keyboard - Japanese` on a JIS board) as the first entry, so plain Latin typing stays the default and Mozc is what you switch into.

4. Apply, close, and log out and back in if any already-running app ignores the new engine. Toggle with `Ctrl + Space`, which is fcitx5's stock trigger key. On a JIS board, `Zenkaku_Hankaku` is in the same default trigger list.

## Verify it worked

```bash
systemctl --user is-active omarchy-fcitx5.service
fcitx5-remote -n
```

The first should print `active`. The second prints the current input method name; press `Ctrl + Space` and run it again, and it should flip between your keyboard layout and `mozc`.

Then open a terminal and type `nihongo`. You should get a hiragana preedit and a candidate list, and space should convert it to 日本語.

If you want to check the group programmatically, ask fcitx5 over D-Bus:

```bash
busctl --user --json=short call org.fcitx.Fcitx5 /controller \
  org.fcitx.Fcitx.Controller1 InputMethodGroupInfo s "$(fcitx5-remote -q)"
```

`mozc` should appear in the returned list.

## Why it happens

Omarchy sets `INPUT_METHOD`, `QT_IM_MODULE`, `XMODIFIERS` and `SDL_IM_MODULE` to `fcitx` in `/usr/lib/environment.d/10-omarchy-fcitx.conf`. It does not set `GTK_IM_MODULE`. On Wayland, GTK uses the `text-input` protocol instead of an im-module, and an older migration (the one that moved logins to UWSM, still shipped in 3.8.4) strips `GTK_IM_MODULE=fcitx` out of `~/.config/environment.d/fcitx.conf`. If you find a guide or a plugin README telling you to add it back, skip that line. It is a leftover from X11 setups, and Omarchy's own migration removes it.

This is also why nothing about the framework needs installing. The only thing `omarchy pkg add fcitx5-mozc` changes is which engines fcitx5 can offer.

## Known pitfalls on 4.0.x

**`fcitx5-configtool` will not appear in the launcher.** Omarchy hides it on purpose: `fcitx5-configtool`, `org.fcitx.Fcitx5` and the other fcitx desktop entries are all listed in `default/omarchy/launcher.hides`. Run it from a terminal. akitaonrails flagged exactly this on PR #9634 as a few confused minutes of hunting.

**Chromium may ignore the IME.** Whether Chromium-based browsers need `--enable-wayland-ime` to take the Wayland text-input path is contested. akitaonrails reported on PR #9634 that on 4.0.4 every terminal and GTK and Qt app accepted Japanese after setup while the browser did not until the flag was set, and opened [PR #12139](https://github.com/omacom/omarchy/pull/12139) to ship it. [PR #11719](https://github.com/omacom/omarchy/pull/11719) argues that current Chromium enables text-input-v3 by default and the flag is redundant, and [issue #7559](https://github.com/omacom/omarchy/issues/7559) lists only the stock ozone flags for Chromium and reports conversion working. Omarchy 4.0.4 does not ship the flag. If your browser drops the IME, add it yourself:

```bash
echo '--enable-wayland-ime' >> ~/.config/chromium-flags.conf
```

Restart the browser afterwards. PR #12139 also carries a migration for existing installs, because `omarchy-install-browser` copies the flags file once, at install time. It was open on 2026-09-16.

**The candidate window is misplaced in native Wayland Chromium and Electron apps.** [Issue #7559](https://github.com/omacom/omarchy/issues/7559) reports the popup not following the caret in Chromium and Obsidian, while the same apps behave under XWayland. Input and conversion still work. Open as of this writing.

**The candidate popup is invisible in true fullscreen.** [Issue #11303](https://github.com/omacom/omarchy/issues/11303) covers a native Wayland terminal put into Hyprland's internal fullscreen with `SUPER + F`. Composition and commit still work, but you cannot see the candidate list. The issue points at Omarchy's `SUPER + CTRL + F` tiled fullscreen binding, which avoids the failing internal fullscreen state, as the workaround.

**Do not expect a Shift-key toggle.** Omarchy's default `kb_options` is `compose:caps,shift:both_capslock_cancel`. [Issue #7440](https://github.com/omacom/omarchy/issues/7440) traced why fcitx5's modifier-only Shift trigger never fires under it: the Shift release arrives with a `Caps_Lock` keysym, so fcitx5's release matching fails. Stick with `Ctrl + Space` or, on a JIS board, the `Zenkaku_Hankaku` key.

**`Super + Space` is not available as a switch key.** Hyprland grabs it for the Omarchy menu, and `Super + Shift + Space` toggles the top bar. Those are fcitx5's usual group-enumerate defaults, so they never reach fcitx5.

**Do not switch layouts through Hyprland once fcitx5 is running.** [Issue #9552](https://github.com/omacom/omarchy/issues/9552) describes the trap: a `grp:` xkb toggle or the bar widget changes the label and `hyprctl devices` agrees, but typed characters stay in the old layout in most apps. The issue's own workaround is disabling `omarchy-fcitx5.service`, which also takes Mozc and the compose sequences with it. For a Japanese setup, keep the layouts you need as keyboard entries in the fcitx5 group next to Mozc and switch there.

**The Omarchy menu search field does not accept composed text.** [Issue #11682](https://github.com/omacom/omarchy/issues/11682) reports the Quickshell menu collecting raw key events instead of going through Qt's input method, so CJK preedit never reaches it. Filed against Hangul, and the same code path applies to Mozc.

**Dictation is a separate problem.** [Issue #10050](https://github.com/omacom/omarchy/issues/10050) reports Voxtype's default type mode corrupting longer Japanese text through `wtype`.

**JIS keyboards and the resize bindings.** [Issue #10452](https://github.com/omacom/omarchy/issues/10452) points out that the window resize shortcuts are bound to physical keycodes (`code:20`, `code:21`) but labelled `MINUS` and `EQUAL`, which do not line up on a JIS board.

## If that did not work

If `fcitx5-remote -n` returns nothing or errors, fcitx5 is not running for your session. Check `systemctl --user status omarchy-fcitx5.service`. The unit has `ConditionEnvironment=WAYLAND_DISPLAY`, so it deliberately does not start over SSH.

If the journal shows the service restarting over and over, you probably have a leftover autostart entry launching fcitx5 under its own name. [Issue #7461](https://github.com/omacom/omarchy/issues/7461) documents a machine that reached over 11,000 restarts this way. Remove the stray `.desktop` file from `~/.config/autostart/` and restart the unit.

If Mozc shows up in the config tool but disappears after a reboot, you probably edited `~/.config/fcitx5/profile` by hand while fcitx5 was running. fcitx5 rewrites that file from its live state on exit, which is why PR #9634 registers the engine over D-Bus rather than by editing the file.

## What is coming

[PR #9634](https://github.com/omacom/omarchy/pull/9634) by komagata adds *Setup > Input Method > Mozc (Japanese)* to the Omarchy menu, backed by a small `omarchy-setup-input-mozc` script that installs the package, restarts fcitx5, waits for it to answer, and appends `mozc` to the current group over D-Bus. It also rewrites the manual paragraph to point at the menu. It was open on 2026-09-16. A Korean sibling, [PR #11719](https://github.com/omacom/omarchy/pull/11719), takes the same shape, and [PR #12142](https://github.com/omacom/omarchy/pull/12142) would make the candidate window follow your Omarchy theme. None of these are merged, so treat the manual steps above as the current path.

For a bar indicator, two third-party Quickshell plugins exist. [komagata/omarchy-input-method](https://github.com/komagata/omarchy-input-method) builds its list from the active fcitx5 group, so it covers Mozc, Rime and Hangul alike. [Praveensenpai/omarchy-japanese-ime](https://github.com/Praveensenpai/omarchy-japanese-ime) is Japanese-specific and shows あ or a keyboard glyph. Both are MIT licensed; komagata's was last pushed on 2026-09-06 and Praveensenpai's on 2026-08-29. Note that the Praveensenpai README recommends setting `GTK_IM_MODULE=fcitx` and hand-editing the fcitx5 profile, and neither is right on Omarchy 4. Third-party plugins run as unsandboxed code inside your long-lived shell process, so read them before you enable them. See [plugins run unsandboxed](/security/plugins-run-unsandboxed/).

## Related

- [Keyboard layouts and locale](/keyboard/layouts-and-locale/)
- [Non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/)
- [Chinese input with fcitx5](/keyboard/chinese-input-fcitx5/)
