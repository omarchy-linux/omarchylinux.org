---
title: "Keyboard layouts and locale on Omarchy 4"
description: "Where Omarchy 4 reads your keyboard layout, how to add and switch layouts in input.lua, the LUKS non-Latin trap, and why the clock stays English."
answer: "On Omarchy 4 the layout comes from /etc/vconsole.conf, which the packaged default/hypr/input.lua reads at every Hyprland start. Change it machine-wide with localectl, or override it per user with kb_layout in ~/.config/hypr/input.lua. Repeat compose:caps,shift:both_capslock_cancel in kb_options or you lose the compose key. The shell clock stays English on purpose."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [keyboard, layouts, locale, fcitx5, luks, hyprland]
sources:
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://omarchy.org/manual/faq/"
    title: "Omarchy manual: FAQ"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/6934"
    title: "Issue #6934: Bar clock always shows weekday/month names in English, ignoring system locale (LANG)"
    kind: issue
    author: "isaac30503"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/6988"
    title: "PR #6988: Keep the calendar's day names in English"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7211"
    title: "Issue #7211: Calendar weekday labels hardcoded to English instead of using system locale"
    kind: issue
    author: "markbus-ai"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7760"
    title: "Issue #7760: Bar clock/calendar ignores system locale - always renders English day/month names"
    kind: issue
    author: "Hehed04"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/8600"
    title: "Issue #8600: Clock widget ignores system locale, always shows English day/month/AM-PM"
    kind: issue
    author: "JDavidCarreno"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/6229"
    title: "Issue #6229: vconsole.conf bundled into initramfs locks out LUKS users with non-Latin keyboard layouts (Hebrew/Greek/Cyrillic)"
    kind: issue
    author: "elpddev"
    date: "2026-07-16"
  - url: "https://github.com/omacom/omarchy/pull/9299"
    title: "PR #9299: Offer Korean as an install-time keyboard choice"
    kind: pr
    author: "ronaldlangeveld"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/9634"
    title: "PR #9634: Add one-step Japanese input setup"
    kind: pr
    author: "komagata"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/9695"
    title: "PR #9695: Add a Setup > Region toggle with Chinese language and input method"
    kind: pr
    author: "ZacharyZhang-NY"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/10949"
    title: "PR #10949: Ask for a language at setup, and offer one in the menu"
    kind: pr
    author: "sbelcl"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/pull/10955"
    title: "PR #10955: Read day and month names from the system locale"
    kind: pr
    author: "sbelcl"
    date: "2026-09-09"
credits:
  - name: "elpddev"
    url: "https://github.com/elpddev"
    for: "Traced the LUKS lockout to vconsole.conf being bundled into the initramfs on a non-Latin layout"
  - name: "JDavidCarreno"
    url: "https://github.com/JDavidCarreno"
    for: "Pinned the English clock on Qt.formatDateTime rendering format specifiers through the C locale"
faq:
  - q: "Why is my clock in English when the rest of my system is not?"
    a: "It is deliberate. DHH closed issue #6934 as not planned, because the whole Omarchy shell is English and localizing only the clock would have made it the odd surface out. PR #6988 went the other way and made the calendar English too."
  - q: "Does changing the keyboard layout in input.lua also change the LUKS unlock prompt?"
    a: "No. The unlock prompt follows /etc/vconsole.conf, and only after the initramfs is rebuilt. Change the layout with localectl, then run sudo limine-mkinitcpio."
  - q: "Can I install Omarchy with a Russian or Hebrew layout and still use the keybindings?"
    a: "Yes. The packaged default/hypr/input.lua prepends us in front of any non-Latin layout and adds grp:alts_toggle, because Hyprland resolves keybindings against the first layout in the list."
  - q: "Is fcitx5 already running on a stock Omarchy 4 install?"
    a: "Yes. fcitx5, fcitx5-gtk and fcitx5-qt are in install/omarchy-base.packages and fcitx5 runs as omarchy-fcitx5.service, because it powers the CapsLock compose sequences. You still add an engine and fcitx5-configtool yourself."
related: [chinese-input-fcitx5, japanese-input-mozc, korean-input-hangul]
draft: false
---

Checked against Omarchy v4.0.4 (2026-09-15).

Omarchy 4 has one source of truth for your keyboard layout, and it is not a file in your home directory. It is `/etc/vconsole.conf`. Everything else reads from there, or deliberately ignores it. Once you know that, the rest of this page is detail.

## Where the layout comes from on Omarchy 4

Setup asks you one keyboard question. The list of choices lives in `install/provisioning/setup-form.sh` as label and console keymap pairs, around fifty entries, defaulting to "English (US)". Your answer goes through `systemd-firstboot --keymap=`, falling back to `localectl set-keymap`, so it lands as both the console `KEYMAP` and the XKB layout in `/etc/vconsole.conf`.

Then Omarchy's packaged `/usr/share/omarchy/default/hypr/input.lua` opens that file at every Hyprland start and reads `XKBLAYOUT` and `XKBVARIANT` out of it, falling back to `us`. No per-user rewrite happens.

This is new in 4.0.0. On 3.x, `install/config/detect-keyboard-layout.sh` ran once at install time and used `sed` to splice a `kb_layout` line into your `~/.config/hypr/input.conf`. After that the two files could drift apart forever. If you upgraded from 3.x, migration `1781485962.sh` replaced your `input.lua` with the packaged one when it was still stock or still matched `vconsole.conf`, so the live read took over. If you had customized it, your file was left alone and your old hardcoded layout still wins.

The packaged defaults you inherit are `repeat_rate = 40`, `repeat_delay = 250`, `numlock_by_default = true`, and `kb_options = "compose:caps,shift:both_capslock_cancel"`. Caps Lock is the compose key, and both Shift keys together give you Caps Lock back, self-cancelling on the next lone Shift.

## Change the layout for the whole machine

This is the right route if you want the TTY, the LUKS prompt and Hyprland to agree.

```bash
sudo localectl set-keymap de
sudo localectl set-x11-keymap de pc105 nodeadkeys
cat /etc/vconsole.conf
hyprctl reload
```

If your disk is encrypted, the unlock prompt only picks this up after the initramfs is rebuilt:

```bash
sudo limine-mkinitcpio
```

Check it landed with `hyprctl devices`, which lists every keyboard on the seat with its active keymap.

## Override it per user in input.lua

`~/.config/hypr/input.lua` is loaded after Omarchy's defaults, and anything you uncomment there replaces them. You can also reach it from _Setup > Input_ in the Omarchy menu (`Super + Space`). Hyprland auto-reloads on save.

```lua
hl.config({
  input = {
    kb_layout = "us,de",
    kb_variant = ",nodeadkeys",
    kb_options = "compose:caps,shift:both_capslock_cancel,grp:alts_toggle",
  },
})
```

One trap worth spelling out. `kb_options` is a replacement, not an addition. If you set it to just `grp:alts_toggle` you silently lose the compose key and the Shift handling, and your CapsLock emoji and completion sequences stop working. Carry `compose:caps,shift:both_capslock_cancel` forward every time. The manual's own examples do this, which is why they all look repetitive.

`kb_variant` is positional against `kb_layout`. Two layouts need two comma-separated variant slots, even when the first one is empty.

## Switching between layouts

With two or more layouts configured, `grp:alts_toggle` cycles them on Left Alt plus Right Alt. That is the option the manual and the FAQ both use.

The bar also carries a keyboard layout widget, `omarchy.keyboard-layout`, added to the default layout by migration `1786279107.sh` and placed just right of the clock. It hides itself when the active keyboard has only one layout, so a single-layout machine never sees it. Clicking it runs `hyprctl switchxkblayout <keyboard> next` on the keyboard the widget is describing. If yours is missing:

```bash
omarchy bar put omarchy.keyboard-layout --after omarchy.clock
```

## The LUKS trap on non-Latin layouts

Bundling `/etc/vconsole.conf` into the initramfs is what makes Plymouth apply your layout at the LUKS prompt. For a Hebrew, Greek, Cyrillic, Arabic or similar layout that backfires badly: the passphrase is Latin, the prompt is not, and you cannot type it. elpddev reported exactly that lockout in issue #6229, with only older snapshot boot entries still unlocking.

Omarchy 4 handles this in two places. `etc/mkinitcpio.conf.d/omarchy_hooks.conf` only adds `FILES+=(/etc/vconsole.conf)` when the first layout is not in the non-Latin list, and migration `1784476564.sh` strips the line and rebuilds the UKI on machines that already had it. The list covers `af am ara bd bg by et ge gr il in iq ir kg kh kz la lk mk mm mn mv np rs ru sy th tj ua`.

So on a non-Latin layout the unlock prompt stays US QWERTY by design. Type the passphrase as if you were on a US keyboard. The guard is not in v3.8.4, which still bundles unconditionally via migration `1783355853.sh`.

The same list appears a second time in `default/hypr/input.lua`, for a different reason. Hyprland resolves keybindings against the first entry in `kb_layout`, not the active one, so a non-Latin layout in front would break `SUPER + W` and everything like it. Omarchy prepends `us,` and appends `grp:alts_toggle` so your real layout is one Alt-Alt away.

## Why the clock and calendar are English

This is settled, not broken. `Qt.formatDateTime` and `Qt.formatDate` render `dddd`, `MMMM` and `AP` through the C locale whatever `Qt.locale()` resolves to, so the Quickshell bar clock comes out English even with `LANG=sv_SE.UTF-8`.

isaac30503 reported it as issue #6934 and diagnosed it correctly. DHH closed it as not planned on the same day, with the reasoning that the entire shell is English already, so localizing the clock alone would make it the one localized surface on an English desktop. The calendar popup was treated as the accident, and PR #6988 by DHH, merged 2026-08-15, made the calendar's day names English too by pinning `labelLocale` to `Qt.locale("en_US")` in `shell/plugins/panels/clock/Panel.qml`. Where the week starts still follows your locale, since that is a regional convention rather than a translation, and it is overridable with `weekStartDay`.

Issues #7211, #7760 and #8600 all report the same surface from different angles and are all still open on 4.0.4. Treat English dates as current behaviour, not as a bug waiting on you.

There is also no language question at setup. Nothing in the omarchy repository writes `/etc/locale.gen` or `/etc/locale.conf`. Setup asks for keyboard layout, hostname and timezone only.

## Input methods: what is already installed

`install/omarchy-base.packages` on 4.0.4 ships `fcitx5`, `fcitx5-gtk`, `fcitx5-qt`, plus `noto-fonts`, `noto-fonts-cjk` and `noto-fonts-emoji`. fcitx5 runs as `omarchy-fcitx5.service` under systemd, supervised since migration `1785167800.sh`, because it is what powers the CapsLock compose sequences.

So the framework and the CJK fonts are already there on a stock install. What is not there is an engine, and `fcitx5-configtool` is not in the base package list either. It appears in the retired-package list inside `omarchy-upgrade-to-quattro`, so a 3.x machine that had it loses it on the upgrade. Install what you need:

```bash
omarchy pkg add fcitx5-configtool fcitx5-mozc
omarchy restart xcompose
```

Then use `fcitx5-configtool` to add the engine to your input method group and set the switch key. Per-language walkthroughs live at [Chinese input with fcitx5](/keyboard/chinese-input-fcitx5/), [Japanese input with Mozc](/keyboard/japanese-input-mozc/) and [Korean Hangul input](/keyboard/korean-input-hangul/).

## What to watch for on newer versions

Five relevant pull requests were open against `omacom/omarchy` on 2026-09-16. None of them is merged, so nothing here describes current behaviour.

| PR | Author | What it proposes |
| --- | --- | --- |
| #9695 | ZacharyZhang-NY | A _Setup > Region_ toggle between World and China that switches the system language to zh_CN, installs a Rime input method and swaps the menu to Chinese labels |
| #9634 | komagata | A _Setup > Input Method > Mozc (Japanese)_ menu entry that installs `fcitx5-mozc` and appends Mozc to the current input method group |
| #9299 | ronaldlangeveld | Korean as an install-time keyboard choice, wired through fcitx5 rather than a console keymap, since kbd ships none for Korean |
| #10949 | sbelcl | A language question at setup plus an `omarchy-menu-language` entry, so `LANG` is not left at the default |
| #10955 | sbelcl | Replacing `Qt.formatDateTime` with `toLocaleString(Qt.locale(), ...)` so day and month names follow the system locale |

The last one is worth watching closely, because it points the opposite way from the decision in #6934. If it merges, English dates stop being the answer. Until then they are.

"Quattro RS 4.5" is the announced next release. Nothing published about it commits to any of these, so do not plan around them.

## Related

- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
- [Non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/)
- [Upgrading 3 to 4](/upgrade/3-to-4-quattro/)
