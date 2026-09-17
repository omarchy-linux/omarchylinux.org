---
title: "Fonts wrong or missing after an Omarchy update"
description: "Wrong monospace font, tofu boxes, or broken emoji after an Omarchy 4 update. Reset fontconfig with omarchy font set, rebuild the font cache, fix leftovers."
answer: "Run `omarchy font set \"JetBrainsMono Nerd Font\"`. That rewrites ~/.config/fontconfig/fonts.conf from scratch, updates every terminal config, and restarts the shell, which clears a stale Omarchy 3 fontconfig file left behind by the Quattro upgrade. Then run `fc-cache -f` and restart Ghostty, Foot, and your browser by hand, because none of them reload fonts in place."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 127
errorStrings:
  - "Font '<name>' not found."
  - "Usage: omarchy-font-set <font-name>"
  - "Packaged Omarchy icon font is missing; keeping the legacy font."
tags: [fonts, fontconfig, quattro, emoji, glyphs, update]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11002"
    title: "Issue #11002: Last-resort fontconfig rule only covers Arabic, so other non-Latin scripts render as tofu boxes in Chromium/Electron"
    kind: issue
    author: "ganjeez"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/8928"
    title: "Issue #8928: Last-resort Noto Naskh Arabic rule renders Latin digits in GTK apps as serif"
    kind: issue
    author: "anakinrpi"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/8404"
    title: "Issue #8404: omarchy font set redirects every family whose name contains mono, not just generic monospace"
    kind: issue
    author: "DanielSRojo"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/10117"
    title: "Issue #10117: omarchy-upgrade-to-quattro: retired user configs are backed up but never removed; the abort is reported as success"
    kind: issue
    author: "Sean-Mulcahy"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/7698"
    title: "Issue #7698: Font picker excludes FC_DUAL monospace fonts (spacing=90)"
    kind: issue
    author: "silouanwright"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/8608"
    title: "Issue #8608: Bar icons render at ~half size with Iosevka Nerd Font Mono"
    kind: issue
    author: "Sojournn"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9167"
    title: "Issue #9167: omarchy font set leaves bold_font/italic_font stale in kitty.conf"
    kind: issue
    author: "ekollof"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/7183"
    title: "Issue #7183: omarchy-font-set: terminal restart notifications never fire"
    kind: issue
    author: "WhiskeyTuesday"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/pull/7370"
    title: "PR #7370: Fire the restart-terminal toast after a font change"
    kind: pr
    author: "686f6c61"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/discussions/4818"
    title: "Discussion #4818: ghostty falls back to default font after upgrade to 3.4.0"
    kind: discussion
    author: "hrzlgnm"
    date: "2026-02-28"
  - url: "https://github.com/omacom/omarchy/discussions/3555"
    title: "Discussion #3555: ghostty font size change not taking effect"
    kind: discussion
    author: "sepulworld"
    date: "2025-11-22"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.3/migrations/1788848726.sh"
    title: "Migration 1788848726: Retire the stock user icon font missed by the Quattro upgrade"
    kind: commit
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/fonts/"
    title: "Omarchy manual: Fonts"
    kind: manual
credits:
  - name: "ganjeez"
    url: "https://github.com/ganjeez"
    for: "Traced Chromium tofu boxes to 50-omarchy.conf truncating the Noto alias chain, and published a working /etc/fonts/conf.d workaround"
  - name: "DanielSRojo"
    url: "https://github.com/DanielSRojo"
    for: "Showed with fc-conflist why a named font can resolve to the font set by omarchy font set"
  - name: "anakinrpi"
    url: "https://github.com/anakinrpi"
    for: "Found that the last-resort Arabic rule captures Latin digits in GTK apps"
  - name: "Sean-Mulcahy"
    url: "https://github.com/Sean-Mulcahy"
    for: "Documented that a Quattro upgrade can leave the old ~/.config/fontconfig/fonts.conf active while still reporting success"
  - name: "Sojournn"
    url: "https://github.com/Sojournn"
    for: "Measured Nerd Font glyph boxes to explain why bar icons shrink with some fonts"
faq:
  - q: "Did Omarchy 4 change the default font?"
    a: "The family is the same, JetBrainsMono Nerd Font, but the package is not. Omarchy 3.8.4 installed ttf-jetbrains-mono-nerd; 4.0.0 switched to the lighter ttf-jetbrains-mono-nerd-basic to save about 200MB, and the Quattro upgrader removes the old package. If you were using a variant family that only the full package shipped, it is gone after the upgrade."
  - q: "Where does Omarchy set the system font now?"
    a: "In two places. The package-owned default lives at /usr/share/fontconfig/conf.avail/50-omarchy.conf and is loaded from /etc/fonts/conf.d. Your own choice lives in ~/.config/fontconfig/fonts.conf, which omarchy font set rewrites in full every time you run it. On 3.x there was no package-owned file; ~/.config/fontconfig/fonts.conf was the only one."
  - q: "Why did my terminal font change but nothing else, or the other way round?"
    a: "omarchy font set writes fontconfig and each terminal config separately. Fontconfig covers the Omarchy shell, Qt and anything asking for monospace. Alacritty, Kitty, Ghostty and Foot each get their own line edited. If one of those files was customized in a way the edit does not match, that terminal keeps the old font while everything else moves."
  - q: "Do I need to reboot after changing fonts?"
    a: "No. Restart the shell with omarchy restart shell, restart Ghostty and Foot by hand, and restart your browser. Chromium and Electron read the fontconfig chain at process start, so an open window keeps the old fallback until you close every process."
related: [where-did-waybar-go, theme-not-applied-to-gtk4-apps, fractional-scaling-blurry-or-huge-apps, quickshell-crashes-or-bar-missing, pacnew-and-pacsave-files-after-update]
draft: false
---

Fonts break after an Omarchy update in three distinct ways, and they have different causes. Either the monospace font is not the one you picked, or some characters render as empty boxes, or the icon glyphs in the bar and the terminal prompt look wrong. All of this was checked against the v4.0.0 through v4.0.4 trees, with v3.8.4 as the 3.x reference.

Start with `omarchy-version`. Everything below is for 4.0.0 and later. If you are still on 3.8.4 or earlier, see the note at the end.

## The fix

1. Ask what fontconfig actually resolved, not what your terminal shows: `omarchy font current`. It runs `fc-match monospace` and prints the first family. On a healthy 4.x install with no override that is `JetBrainsMono Nerd Font`.

2. Re-apply your font. `omarchy font list` shows what is installed, then `omarchy font set "JetBrainsMono Nerd Font"` (or your own choice, in quotes). This is the step that fixes most post-update font trouble, because `omarchy-font-set` does not patch your fontconfig file, it overwrites `~/.config/fontconfig/fonts.conf` in full. Any leftover from Omarchy 3 is gone afterwards. It also rewrites the Alacritty, Kitty, Ghostty and Foot configs and restarts the Omarchy shell.

3. If you get `Font '<name>' not found.`, the family really is not installed. Check with `fc-list | grep -i <name>`. The Quattro upgrader removes `ttf-jetbrains-mono` and `ttf-jetbrains-mono-nerd` before the main package transaction and installs `ttf-jetbrains-mono-nerd-basic` instead, so a variant family that came from the full Nerd Font package will not resolve any more. Pick a family that `omarchy font list` shows, or install a fresh one from _Install > Style > Font_ in the Omarchy menu (`Super + Space`), which installs the package and switches to it in one go.

4. Rebuild the font cache and restart the clients: `fc-cache -f`, then `omarchy restart shell`. Add `-r` (`fc-cache -f -r`) if you want the old cache files discarded rather than updated.

5. Close and reopen Ghostty, Foot and your browser. Kitty and Alacritty pick up the change live; Ghostty and Foot do not. Omarchy is supposed to warn you about this with a toast, but the notification call in `omarchy-font-set` is malformed and the message is never delivered. That was reported in issue #7183 and PR #7370 is still open as of 4.0.4, so treat the manual restart as required.

6. If bold or italic text in Kitty still uses the old font, open `~/.config/kitty/kitty.conf` and look for `bold_font` and `italic_font` lines. `omarchy font set` only rewrites `font_family`, so an explicit `bold_font` from an earlier choice survives (issue #9167). Set them to `auto` or to your new family.

7. If the Omarchy icon glyphs in the bar look wrong or duplicated, check for a leftover user copy of the icon font: `ls -l ~/.local/share/fonts/omarchy.ttf`. Migration 1788848726, which shipped in v4.0.3, removes that file, but only when its checksum matches the stock one, and it refuses to touch symlinks or a font you replaced yourself. If the file is still there and you did not put it there, move it aside and run `fc-cache -f`.

## Verify it worked

```
omarchy font current
fc-match monospace
fc-match sans-serif
fc-match serif
```

On a stock 4.0.x install those return your chosen monospace family, `Liberation Sans` and `Liberation Serif`. The two Liberation answers come from the package-owned `50-omarchy.conf`, not from anything in your home directory, so seeing them is a good sign that the package default is in charge again.

Then look at the desktop. The bar icons should be crisp and evenly sized, emoji should be in colour in a fresh terminal, and any CJK or other non-Latin text you use should render as glyphs rather than boxes.

## Why it happens

Quattro moved the font defaults out of your home directory. On 3.8.4 the whole configuration was one user file, `~/.config/fontconfig/fonts.conf`, and `omarchy-font-set` edited the monospace entry inside it with `xmlstarlet`. On 4.x the defaults are package-owned, shipped as `50-omarchy.conf` and loaded from `/etc/fonts/conf.d`, and the user file only carries your override.

The upgrade handles that move by hash. It backs up each retired config file, then compares the backup against a list of checksums for every default Omarchy has ever shipped. A file that matches is deleted so the packaged one takes over. A file that does not match is copied back, on the assumption that you customized it deliberately. Five stock hashes for `fontconfig/fonts.conf` are on that list. If you ever changed your font on 3.x, your copy matches none of them, so it is restored and stays active alongside the new packaged file. Issue #10117 documents an upgrade where the removal pass never ran at all, leaving `fontconfig/fonts.conf` and an orphaned `omarchy.ttf` behind while the upgrade still showed its completion screen.

The other half is the new fallback rules. `50-omarchy.conf` pins the three generic families with a strong `assign`, which cuts the alias chains that `noto-fonts` appends later in the load order. It then adds an unconditional last-resort family to catch Chromium and Electron, which resolve missing glyphs one character at a time. Both choices have visible side effects that are open as of 4.0.4.

## If that did not work

- **Empty boxes for Tamil, Devanagari, Thai and other non-Latin scripts in Chromium, Chrome, Brave or Electron apps.** The last-resort fallback only names an Arabic face, so every other script has nothing to fall back to. Issue #11002 has the analysis and a verified workaround: a file in `/etc/fonts/conf.d/` with a number above 50 that appends the Noto family for your script, then `fc-cache -f` and a full browser restart.
- **Digits rendering in a serif or calligraphic face in GTK4 apps such as Files.** Same last-resort rule, opposite failure. Issue #8928 has a user-level override that drops the Arabic face when it is the effective fallback.
- **An app asks for a specific font and gets the one you set globally.** Any family whose name contains "mono" is affected, because fontconfig's own `48-guessfamily.conf` widens such patterns before the Omarchy rule sees them. Issue #8404 has the full load order and the evidence.
- **Your font is installed but missing from _Style > Font_.** `omarchy-font-list` filters on `fc-list :spacing=100`, so dual-width fonts are excluded from the picker even though `omarchy font set` will accept them by name. Issue #7698.
- **Bar icons much smaller than before.** Some Nerd Fonts draw icon glyphs at about half the em box. The bar renders them at a fixed pixel size, so the painted icon shrinks. Issue #8608 has measurements per codepoint. Switching back to JetBrainsMono Nerd Font is the only fix today.
- **Ghostty ignores a font size you set by hand.** Ghostty honours whichever config file loads last. In discussion #3555 the reporter kept the Omarchy-managed line in place and added a `config-file` include as the final line, with personal font settings in the included file.
- **You are still on 3.x.** Discussion #4818 describes the 3.4.0 version of this problem, where an update reset Ghostty to the default font. The workaround was the same in spirit: pick your font again in _Style > Font_. None of the fontconfig detail above applies, since 3.x has no packaged `50-omarchy.conf`.

If the update that broke your fonts also broke other things, the aborted-upgrade case in issue #10117 is worth ruling out before you spend time on fontconfig.

## Related

- The manual chapter is [Fonts](https://omarchy.org/manual/fonts/), and text size across the whole desktop is one knob, `omarchy display text size`.
- [Where did Waybar go](/fix/where-did-waybar-go/) covers the rest of the bar changes in Quattro.
- [Theme not applied to GTK4 apps](/fix/theme-not-applied-to-gtk4-apps/) for GTK styling that survived the update but looks wrong.
- [Fractional scaling blurry or huge apps](/fix/fractional-scaling-blurry-or-huge-apps/) if the problem is size rather than shape.
- [Upgrading 3 to 4](/upgrade/3-to-4-quattro/) for what the Quattro upgrader does to the rest of your config.
