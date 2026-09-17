---
title: "GTK4 and libadwaita apps ignore the Omarchy theme"
description: "Nautilus and other GTK4/libadwaita apps stay Adwaita gray on Omarchy 4. Omarchy only sets light/dark, so generate a gtk.css palette with a theme template and hook."
answer: "Omarchy does not theme GTK4 apps. omarchy-theme-set-gnome only sets color-scheme, gtk-theme and icon-theme, so Nautilus follows light or dark and nothing else. Fix it yourself: add a gtk.css.tpl template in ~/.config/omarchy/themed/ that maps colors.toml onto libadwaita @define-color names, then a theme-set hook that copies the result to ~/.config/gtk-4.0/gtk.css and restarts the app. Chromium is themed separately and does work."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 20
errorStrings:
  - "@define-color background     #;"
  - "Theme is set by your Organization"
tags: [theme, gtk4, libadwaita, nautilus, chromium, quattro]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7557"
    title: "Issue #7557: GTK4/libadwaita apps don't follow the Omarchy theme"
    kind: issue
    author: "akitaonrails"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/9751"
    title: "Issue #9751: Nautilus doesn't follow the theme palette"
    kind: issue
    author: "suleman-dawood"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8380"
    title: "Issue #8380: Nautilus background transparent with Solitude theme (empty GTK color values)"
    kind: issue
    author: "Rowdydangerous"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7203"
    title: "Issue #7203: Vantablack/White themes: 'Yaru-gray' icon theme unresolvable in 4.0.0"
    kind: issue
    author: "pcrisho"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/1888"
    title: "Issue #1888: Chromium theming issue / Persistent accent color after theme change"
    kind: issue
    author: "erik-brueggemann"
    date: "2025-09-22"
  - url: "https://github.com/omacom/omarchy/pull/8408"
    title: "PR #8408: Theme GTK4 apps with Omarchy colors"
    kind: pr
    author: "nimixh"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/pull/8584"
    title: "PR #8584: Theme Files and GTK apps from colors.toml"
    kind: pr
    author: "robertkokenyesi"
    date: "2026-08-27"
  - url: "https://omarchy.org/manual/making-your-own-theme/"
    title: "Omarchy manual: Making your own theme"
    kind: manual
credits:
  - name: "akitaonrails"
    url: "https://github.com/akitaonrails"
    for: "Traced the cause to the missing ~/.config/gtk-4.0/gtk.css and measured which parts of the pipeline can and cannot be recolored"
  - name: "suleman-dawood"
    url: "https://github.com/suleman-dawood"
    for: "Pinned the gap to omarchy-theme-set-gnome setting only gtk-theme, color-scheme and icon-theme"
  - name: "Rowdydangerous"
    url: "https://github.com/Rowdydangerous"
    for: "Reported transparent Nautilus windows caused by a gtk.css full of empty color values"
  - name: "pcrisho"
    url: "https://github.com/pcrisho"
    for: "Workaround for the unresolvable Yaru-gray icon theme on Vantablack and White"
  - name: "hjanuschka"
    url: "https://github.com/hjanuschka"
    for: "Diagnosed and fixed the Chromium policy-theme bug that froze browser accent colors"
faq:
  - q: "Does Omarchy theme Nautilus at all?"
    a: "Only light or dark, plus an icon theme. On 4.0.4 omarchy-theme-set-gnome sets org.gnome.desktop.interface color-scheme, gtk-theme and icon-theme. It never writes a GTK stylesheet, so the palette from colors.toml never reaches the app."
  - q: "Will an official fix land?"
    a: "Two pull requests, #8408 and #8584, propose it with different pipelines. Both were still open and unmerged as of v4.0.4 on 2026-09-15, so nothing has shipped."
  - q: "Why does Chromium say the theme is set by my organization?"
    a: "That is expected. Omarchy writes BrowserThemeColor into an enterprise policy file at /etc/chromium/policies/managed/color.json, and Chromium labels any policy-driven theme that way."
  - q: "Can I recolor GTK3 apps the same way?"
    a: "Not reliably. The reporter of #7557 measured that @define-color in the user stylesheet is provider scoped and does not reach Adwaita's own rules, so GTK3 apps still need a real binary theme."
related: [chromium-flicker-hardware-acceleration, fonts-wrong-or-missing-after-update, fractional-scaling-blurry-or-huge-apps, cursor-invisible-or-wrong-size]
draft: false
---

Omarchy themes your terminal, Neovim, btop, Chromium and the whole Quickshell desktop. GTK4 and libadwaita apps are the hole in that list. Open Nautilus on Tokyo Night or Osaka Jade and you get stock Adwaita gray. This is true on every 4.0.x release including 4.0.4, and it was true on 3.x too.

## The fix

There is no setting to flip. You have to generate the stylesheet yourself using two extension points Omarchy already supports: theme templates and the `theme-set` hook.

1. Create a template so every theme switch produces a palette file:

```bash
mkdir -p ~/.config/omarchy/themed
cat > ~/.config/omarchy/themed/gtk.css.tpl <<'EOF'
@define-color window_bg_color {{ background }};
@define-color window_fg_color {{ foreground }};
@define-color view_bg_color {{ background }};
@define-color view_fg_color {{ foreground }};
@define-color headerbar_bg_color {{ lighter_background }};
@define-color headerbar_fg_color {{ foreground }};
@define-color sidebar_bg_color {{ dark_background }};
@define-color sidebar_fg_color {{ foreground }};
@define-color card_bg_color {{ lighter_background }};
@define-color card_fg_color {{ foreground }};
@define-color popover_bg_color {{ lighter_background }};
@define-color popover_fg_color {{ foreground }};
@define-color dialog_bg_color {{ lighter_background }};
@define-color dialog_fg_color {{ foreground }};
@define-color accent_bg_color {{ accent }};
@define-color accent_fg_color {{ background }};
@define-color accent_color {{ accent }};
@define-color destructive_bg_color {{ red }};
@define-color error_bg_color {{ red }};
@define-color success_bg_color {{ green }};
@define-color warning_bg_color {{ yellow }};
EOF
```

`omarchy-theme-set-templates` expands every `.tpl` in that directory against the incoming theme's `colors.toml`, and user templates take priority over Omarchy's own. The result lands at `~/.local/state/omarchy/current/theme/gtk.css`.

2. Create a hook that installs the generated file where GTK4 actually reads it:

```bash
mkdir -p ~/.config/omarchy/hooks/theme-set.d
cat > ~/.config/omarchy/hooks/theme-set.d/50-gtk4-palette <<'EOF'
#!/bin/bash
src="$HOME/.local/state/omarchy/current/theme/gtk.css"
[[ -f $src ]] || exit 0
mkdir -p "$HOME/.config/gtk-4.0"
cp "$src" "$HOME/.config/gtk-4.0/gtk.css"
pkill -x nautilus 2>/dev/null
EOF
```

`omarchy-hook` runs every file in `theme-set.d` with bash after a theme change, so the hook does not need an execute bit. It skips anything ending in `.sample`.

3. Apply it:

```bash
omarchy theme refresh
```

That re-runs the whole theme pipeline against the current theme without cycling your background.

Add more app names to the `pkill` line only if you use them, for example `gnome-calendar` or `gnome-text-editor`. Those daemons survive their last window, so closing the window is not enough. Killing one discards anything unsaved in it.

## Verify it worked

```bash
cat ~/.config/gtk-4.0/gtk.css
grep -c '{{' ~/.config/gtk-4.0/gtk.css
```

Every line should carry a real hex value. A count above zero means a palette key in your template does not exist for that theme and the literal placeholder was left in place. Empty or missing values are what produced transparent Nautilus windows in #8380, where the reporter saw lines reading `@define-color background     #;`.

Then open Nautilus. The window, sidebar and header bar should carry your theme's background, and selected rows should carry the accent. Switch to another theme with `Super + Ctrl + Shift + Space` and confirm it follows.

## Why it happens

`omarchy-theme-set` runs a list of per-app setters after it swaps the theme in. The GNOME one, `omarchy-theme-set-gnome`, does exactly three things: it sets `color-scheme` to `prefer-light` or `prefer-dark`, sets `gtk-theme` to `Adwaita` or `Adwaita-dark`, and sets `icon-theme` from the theme's `icons.theme` file. That is the whole of it in v4.0.4. There is no `gtk.css.tpl` in `default/themed/`, and no stock theme ships a `gtk.css`.

libadwaita is the reason a binary theme name is not enough. It deliberately ignores `gtk-theme` and honors only `@define-color` overrides in the user stylesheet at `~/.config/gtk-4.0/gtk.css`, which Omarchy never writes. That is the root cause given in #7557, and #9751 reaches the same conclusion from the Nautilus side on 4.0.2.

Two competing pull requests would close the gap. #8408 generates the palette through a `default/themed/gtk.css.tpl` and adds a Nautilus extension that reloads it over D-Bus. #8584 writes both GTK3 and GTK4 stylesheets and reloads Files only when a window is mapped. Neither had been merged when 4.0.4 shipped on 2026-09-15.

Two limits are worth knowing before you invest in this. The author of #7557 reports that GTK3 cannot be recolored the same way, because `@define-color` in the user stylesheet is provider scoped and never reaches Adwaita's rules. They also note that libadwaita reads the user stylesheet once, at process start, which is why the hook restarts the app. Both are their measurements, not ours.

## If that did not work

**Nautilus is transparent instead of themed.** You probably have a stale or broken `~/.config/gtk-3.0/gtk.css` or `~/.config/gtk-4.0/gtk.css` with empty color values, the symptom in #8380. Delete both, then re-run `omarchy theme refresh`. Note that the reporter there blames a `10-gtk.sh` hook that stock Omarchy does not ship, so check `~/.config/omarchy/hooks/theme-set.d/` for something you or a plugin installed.

**Icons are broken squares rather than wrong colors.** On Vantablack and White the theme asks for a `Yaru-gray` icon theme that does not exist on disk, and `omarchy-theme-set-gnome` only falls back when the `icons.theme` file is missing, not when the name is unresolvable. Check with `gsettings get org.gnome.desktop.interface icon-theme`. The workaround in #7203 is to copy the theme into `~/.config/omarchy/themes/`, write a real icon theme name such as `Yaru-dark` into its `icons.theme`, and refresh.

**Chromium is not following the theme.** Chromium is themed, through a different path. `omarchy-theme-set-browser` writes `{"BrowserThemeColor": "#rrggbb", "BrowserColorScheme": "device"}` into `/etc/chromium/policies/managed/color.json` and the equivalent directories for Chrome, Edge and Brave, then asks a running browser to reload its policy. Check that the file exists and carries your theme's background color. The message "Theme is set by your Organization" in browser settings is expected with this design.

**Chromium or Brave is stuck on an old accent.** This was a Chromium bug in how policy-based themes update, reported in #1888 and confirmed by hjanuschka, who landed a fix upstream in November 2025. Omarchy's Chromium build carried it first and Brave picked it up later. On 4.0.x you should not see it. If you do, restart the browser fully.

**Qt apps.** Nothing in the theme pipeline targets Qt toolkit apps either. The Omarchy shell is Quickshell, which is themed directly, but a third-party Qt application is on its own.

## Related

- [Chromium flicker and hardware acceleration](/fix/chromium-flicker-hardware-acceleration/)
- [Fonts wrong or missing after an update](/fix/fonts-wrong-or-missing-after-update/)
- [Fractional scaling makes apps blurry or huge](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Making your own theme](https://omarchy.org/manual/making-your-own-theme/) and [Themes](https://omarchy.org/manual/themes/) in the official manual
