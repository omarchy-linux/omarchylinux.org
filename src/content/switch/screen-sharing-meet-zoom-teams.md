---
title: "Screen sharing in Google Meet, Zoom and Teams on Omarchy"
description: "How screen sharing works on Omarchy 4.x: the Hyprland portal picker, the stuck sharing bar, missing monitors in the Outputs tab, and Meet glitches."
answer: "Screen sharing works on Omarchy 4.0.4. Chromium, Chrome, Brave and Firefox hand the request to xdg-desktop-portal-hyprland, which opens hyprland-preview-share-picker with Outputs, Windows and Region tabs. Choose the source there, not in the browser. If a monitor is missing from Outputs, shift your layout so one display sits at 0,0. The stuck sharing bar is already hidden by a shipped window rule."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [screen-sharing, wayland, portal, google-meet, zoom, hyprland]
sources:
  - url: "https://github.com/omacom/omarchy/issues/1862"
    title: "Issue #1862: Unable to dismiss \"sharing your screen message , in google meet\"."
    kind: issue
    author: "Manujdixit"
    date: "2025-09-22"
  - url: "https://github.com/omacom/omarchy/issues/5373"
    title: "Issue #5373: Screen sharing notification bar: Hide button not responding"
    kind: issue
    author: "leolucena22"
    date: "2026-04-21"
  - url: "https://github.com/omacom/omarchy/commit/35650a633d7930c2821a49e957e1172c9c7aab4f"
    title: "Commit 35650a6: Fix broken hide button on screensharing overlay"
    kind: commit
    author: "dhh"
    date: "2026-04-22"
  - url: "https://github.com/omacom/omarchy/issues/11221"
    title: "Issue #11221: hyprland-preview-share-picker-git package is pinned to a Dec 2025 build, missing the upstream origin-offset fix (merged Aug 2026)"
    kind: issue
    author: "jpaferreira-git"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10057"
    title: "Issue #10057: hyprland preview share picker not working properly"
    kind: issue
    author: "rudy-pro"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/10496"
    title: "Issue #10496: Screen glitches in Google Meet"
    kind: issue
    author: "Abi-de-jo"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/9890"
    title: "Issue #9890: hypr/nvidia.lua: LIBVA_DRIVER_NAME=nvidia corrupts hardware video decode on hybrid laptops where the compositor renders on the iGPU"
    kind: issue
    author: "andrea-bavetta"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/10348"
    title: "Issue #10348: Quattro (4.0.2): GPU-accelerated app windows (Electron/CEF, GTK4) never get a compositor surface on hybrid Intel+NVIDIA"
    kind: issue
    author: "sammyyakk"
    date: "2026-09-05"
  - url: "https://github.com/WhySoBad/hyprland-preview-share-picker/issues/15"
    title: "Upstream issue #15: Outputs tab empty when single monitor has non-zero position offset"
    kind: issue
  - url: "https://github.com/WhySoBad/hyprland-preview-share-picker/issues/24"
    title: "Upstream issue #24: Draw the outputs page from the origin of the monitor layout"
    kind: issue
  - url: "https://omarchy.org/manual/web-apps/"
    title: "Omarchy Manual: Web Apps"
    kind: manual
credits:
  - name: "sspaeti"
    url: "https://github.com/sspaeti"
    for: "Traced the repeated Meet share prompt to the portal restore token"
  - name: "Mhdfirmus"
    url: "https://github.com/Mhdfirmus"
    for: "Pinned Meet and browser video glitching to LIBVA_DRIVER_NAME and published the one line override"
  - name: "jpaferreira-git"
    url: "https://github.com/jpaferreira-git"
    for: "Matched the missing monitors in the Outputs tab to a stale share picker package build"
faq:
  - q: "Does screen sharing work in Google Meet on Omarchy 4?"
    a: "Yes. On a single monitor with no NVIDIA GPU in the mix, sharing a screen, a window or a region in Meet or the bundled Zoom web app works on 4.0.4 with no configuration. Teams on the web takes the same portal path, but nobody has filed a Teams report either way. The bugs that remain are multi monitor and hybrid GPU bugs."
  - q: "Why can I not dismiss the bar that says a site is sharing your screen?"
    a: "The Hide button on that Chromium bar does nothing under Wayland. Omarchy works around it with a window rule that moves any window whose title contains \"is sharing\" to a silent special workspace. If your browser is not in English the title will not match and the bar stays visible."
  - q: "Why is one of my monitors missing from the picker?"
    a: "The Outputs tab draws monitor cards from coordinate 0,0. If your Hyprland layout has no output at x=0 or y=0, cards land off screen. Omarchy still ships a share picker build from December 2025 that predates the upstream fix, per issue #11221."
  - q: "Will my password manager appear when I share my whole screen?"
    a: "1Password and Bitwarden windows carry a no_screen_share rule in Omarchy's Hyprland defaults, so they are excluded from capture. Nothing else is, so a second browser window or a terminal with secrets in it will be visible."
related: [day-one-checklist, what-replaces-what]
draft: false
---

Video calls are the first thing most people test after switching, and on Omarchy they mostly just work. This page is checked against 4.0.4 (2026-09-15). Where behaviour differs from 3.x, it says so.

## How sharing actually works here

There is no Google Meet client, no Zoom client and no Teams client on Omarchy. All three run in a browser, and the Zoom entry you get out of the box is a Chromium web app wrapper: `Zoom.desktop` runs `omarchy-webapp-handler-zoom`, which turns a `zoommtg://` or `zoomus://` link into a `https://app.zoom.us/wc/join/...` URL and opens it frameless. The [Web Apps manual chapter](https://omarchy.org/manual/web-apps/) covers that side.

Because everything runs under Wayland, the browser does not draw its own source list. It calls `xdg-desktop-portal-hyprland`, which Omarchy installs as a base package, and the portal opens a picker window. So when Meet says to choose what to share, the window that appears is not part of Chromium. It is `hyprland-preview-share-picker`, wired up in `~/.config/hypr/xdph.conf`:

```
screencopy {
    allow_token_by_default = true
    custom_picker_binary = hyprland-preview-share-picker
}
```

The picker has three tabs. Outputs is the default page and covers whole monitors. Windows lists live previews of every open window, one click to pick. Region runs `slurp` so you can drag a rectangle. Its settings live in `~/.config/hyprland-preview-share-picker/config.yaml` if you want bigger previews or a different default tab.

One thing that trips up people following old guides: because `allow_token_by_default` is on and the picker sets `hide_token_restore: true`, the restore token is already granted for you. Advice from 2025 about ticking a box to allow a restore token so Meet stops asking on every share, which is how a contributor on #1862 solved it on 3.0.x, no longer applies: the box is hidden and the token is granted. `xdph.conf` is identical in 3.8.4 and in 4.0.4.

`xdph.conf` is read by the portal, not by Hyprland, so `hyprctl reload` does nothing to it. Changes land when the portal restarts, which normally means your next login.

## Verify it worked

```bash
echo "$XDG_CURRENT_DESKTOP"                      # must print Hyprland
pacman -Qs hyprland-preview-share-picker
systemctl --user status xdg-desktop-portal-hyprland --no-pager
```

`XDG_CURRENT_DESKTOP` is set to `Hyprland` in Omarchy's `envs.lua` specifically so the portal picks the right backend. If it prints something else, a custom session or a launcher is overriding it, and the portal may not select the Hyprland backend at all.

## The sharing bar you cannot dismiss

Chromium shows a floating bar reading something like "meet.google.com is sharing your screen". Its Hide button does nothing under Wayland, so the bar parks itself in the middle of your screen. That is issue #1862, still open, and issue #5373, closed.

Omarchy has shipped a fix since commit `35650a6` on 2026-04-22, which landed in v3.6.0. On 4.x it lives in the Lua config as a window rule that throws that window onto a silent special workspace. If the bar is still in your face:

1. Check that the rule is loading.

```bash
hyprctl clients | grep -i -A2 "is sharing"
```

2. If the window exists on a normal workspace, its title probably did not match. The shipped rule matches the English string, so a browser running in another language slips through. Add your own rule with the wording your browser uses to `~/.config/hypr/hyprland.lua`:

```lua
o.window({ title = ".*compartiendo.*" }, { workspace = "special silent" })
```

3. Reload and retest.

```bash
hyprctl reload && hyprctl configerrors
```

On 3.x the same rule was a `windowrule = workspace special silent, match:title .*is sharing.*` line in `~/.local/share/omarchy/default/hypr/apps/browser.conf`, sourced from the defaults rather than from your own config. On 4.x it only loads if your `~/.config/hypr/hyprland.lua` still carries the `require("default.hypr.omarchy")` line. If a hand edited config lost it, `omarchy refresh hyprland` restores the defaults.

## A monitor is missing from the picker

The Outputs tab lays monitor cards out starting at coordinate 0,0. If your Hyprland monitor layout has every output at a positive offset, which is easy to end up with after dragging displays around, the cards are drawn outside the visible window and the picker looks like it has fewer monitors than you do. Issue #11221 documents this in detail and ties it to an upstream bug that was fixed on 2026-08-24, upstream issues 15 and 24, both now closed. The `hyprland-preview-share-picker` package Omarchy installs is 0.2.1-1, built in December 2025, and the `-git` variant is pinned to a commit from the same month, so the fix has not reached you on 4.0.4. Issue #10057 looks like the same symptom.

Two workarounds:

1. Move your layout in `~/.config/hypr/monitors.lua` so one output has position 0x0, and shift the others by the same amount so nothing overlaps.
2. Or skip the Outputs tab. The Windows tab and the Region tab do not use that layout maths, so they still list everything.

## Glitching and artifacts once you start sharing

Issue #10496 reports the browser filling with rendering artifacts in Meet when you start sharing while someone else is already sharing, on a hybrid Intel plus NVIDIA laptop. The likely root cause is issue #9890: `default/hypr/nvidia.lua` exports `LIBVA_DRIVER_NAME=nvidia` whenever an NVIDIA GPU with GSP firmware is detected, without checking whether that GPU is the one driving your displays. On a laptop where the iGPU renders the session, every VA-API client is pointed at the wrong driver.

The override, reported working by a commenter on #10496 with an AMD iGPU, goes in `~/.config/hypr/hyprland.lua`:

```lua
hl.env("LIBVA_DRIVER_NAME", "radeonsi")  -- use "iHD" on Intel iGPUs
```

Log out and back in, because environment changes only reach apps launched afterwards. If you want to confirm the diagnosis before editing anything, launch the browser once with the variable set and a throwaway profile.

## If that did not work

- The picker never appears at all. Issue #10348 reports that on a fresh 4.0.2 install with Intel plus NVIDIA, the picker process starts and logs correctly but its window never reaches the compositor, and other Electron and GTK4 apps fail the same way. It is open with no fix as of 4.0.4. Check with `hyprctl clients | grep -i picker` while the prompt should be up.
- Sharing works but video decode is broken generally. That is the same `LIBVA_DRIVER_NAME` story, see [NVIDIA on Omarchy](/hardware/nvidia/).
- Nothing at all happens when the site asks. Restart the portal with `systemctl --user restart xdg-desktop-portal-hyprland xdg-desktop-portal` and try again before you dig further.

Evidence for Microsoft Teams specifically is thin. A search of the issue tracker on 2026-09-16 turned up no Teams screen sharing reports at all, so the honest answer is that Teams on the web goes through exactly the same portal path as Meet and nobody has filed anything against it.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5. The share picker package pin from #11221 is the one to check first after any update: if the `hyprland-preview-share-picker` package moves past the upstream origin offset fix, the missing monitor workaround stops being necessary. The `LIBVA_DRIVER_NAME` detection in `nvidia.lua` is the other one. If it learns to ask which GPU drives the displays, remove your override rather than leaving a stale one behind.

## Related

- [NVIDIA on Omarchy](/hardware/nvidia/)
- [Multi monitor setup](/hardware/multi-monitor/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
