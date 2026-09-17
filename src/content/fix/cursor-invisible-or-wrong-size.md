---
title: "Cursor invisible, wrong size, or a black box on Omarchy"
description: "Mouse pointer missing, tiny, huge, or drawn as a black square on Omarchy 4. Force software cursors in looknfeel.lua and set the cursor size where Hyprland actually reads it."
answer: "If the pointer is invisible, glitchy, or a black box, force software cursors: add an hl.config block with cursor.no_hardware_cursors = true to ~/.config/hypr/looknfeel.lua, then run hyprctl reload. If the size is wrong, do not use ~/.config/hypr/envs.lua, which Omarchy 4 never loads. Put hl.env(\"XCURSOR_SIZE\", \"32\") at the bottom of ~/.config/hypr/hyprland.lua and log out."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 177
errorStrings:
  - "legacy drm: drmCloseBufferHandle in cursor failed"
  - "drm: Cannot commit when a page-flip is awaiting"
  - "keyword can't work with non-legacy parsers. Use eval."
tags: [cursor, hyprland, display, nvidia, scaling, quattro]
sources:
  - url: "https://github.com/omacom/omarchy/issues/4847"
    title: "Issue #4847: Cursor on second monitor is displayed as a black box"
    kind: issue
    author: "theswampdawg"
    date: "2026-03-01"
  - url: "https://github.com/omacom/omarchy/issues/4934"
    title: "Issue #4934: Cursor renders as a large black square on secondary monitor"
    kind: issue
    author: "joao1barbosa"
    date: "2026-03-08"
  - url: "https://github.com/omacom/omarchy/issues/7918"
    title: "Issue #7918: Invisible mouse cursor in VMware guest: vmwgfx hardware cursor plane fails to commit (needs no_hardware_cursors)"
    kind: issue
    author: "BigNatoDemon"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11943"
    title: "Issue #11943: Hardware cursor intermittently stops rendering on hybrid Intel/NVIDIA multi-monitor laptop (recurs despite no_hardware_cursors=true)"
    kind: issue
    author: "Cousint98"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9902"
    title: "Issue #9902: 4.0.x: user ~/.config/hypr/envs.lua is never loaded"
    kind: issue
    author: "Makedayz"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8240"
    title: "Issue #8240: Screenshot picker runs with hardware cursors forced on, hiding the pointer on nouveau/vmwgfx while you select"
    kind: issue
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8797"
    title: "Issue #8797: omarchy-capture-screenshot kills the compositor: hyprctl eval of cursor:no_hardware_cursors faults in hl.config() (SIGABRT)"
    kind: issue
    author: "jeffsidekick"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/2132"
    title: "Issue #2132: Cursor lag on dual monitor setup with NVIDIA (RTX 4090) - Solution included"
    kind: issue
    author: "al3rez"
    date: "2025-10-01"
  - url: "https://github.com/omacom/omarchy/issues/4973"
    title: "Issue #4973: Night light does not apply to cursor"
    kind: issue
    author: "thomasboom"
    date: "2026-03-10"
  - url: "https://github.com/omacom/omarchy/discussions/8428"
    title: "Discussion #8428: How can I change the default mouse cursor to Bibata Modern Classic?"
    kind: discussion
    author: "sunbyte"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/discussions/10947"
    title: "Discussion #10947: Consider Oxygen White as the default cursor"
    kind: discussion
    author: "zain1806481"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/discussions/5833"
    title: "Discussion #5833: shake to find cursor"
    kind: discussion
    author: "ramzlab000"
    date: "2026-05-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 release notes (Force software cursors on nouveau)"
    kind: release
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, mouse and trackpad"
    kind: manual
credits:
  - name: "theswampdawg"
    url: "https://github.com/theswampdawg"
    for: "Pinned the black-box pointer on a second monitor to the hardware cursor plane"
  - name: "BigNatoDemon"
    url: "https://github.com/BigNatoDemon"
    for: "Traced the invisible pointer under VMware to failing vmwgfx cursor commits and confirmed the Lua fix"
  - name: "Makedayz"
    url: "https://github.com/Makedayz"
    for: "Showed that ~/.config/hypr/envs.lua is never loaded in 4.0.x"
  - name: "stephentaylor-com"
    url: "https://github.com/stephentaylor-com"
    for: "Contributed the nouveau software-cursor fix shipped in 4.0.0"
faq:
  - q: "What cursor size does Omarchy use by default?"
    a: "24. default/hypr/envs.lua sets both XCURSOR_SIZE and HYPRCURSOR_SIZE to 24, and Omarchy never sets a GNOME cursor-size or cursor-theme key, so GTK apps fall back to their own defaults."
  - q: "Does WLR_NO_HARDWARE_CURSORS=1 still work?"
    a: "No. That environment variable is ignored by the Hyprland builds Omarchy 4 ships. Use cursor.no_hardware_cursors in looknfeel.lua instead."
  - q: "Why did my cursor fix disappear after upgrading to Omarchy 4?"
    a: "The Quattro upgrade always writes a fresh hypr/looknfeel.lua. Your old looknfeel.conf is left on disk for reference but Hyprland never reads it, so any cursor block in it stops applying."
related: [hybrid-gpu-laptop-black-screen-aq-drm-devices, nvidia-drivers-omarchy-4, fractional-scaling-blurry-or-huge-apps, multi-monitor-layout-not-saved, screenshot-shortcut-not-working]
draft: false
---

Three different problems share the same symptom bucket here: the pointer is gone, the pointer is drawn as a black square or a smear, or the pointer is the wrong size. The first two are the same bug with different hardware. The third is a config plumbing problem specific to Omarchy 4.

## The fix

### Pointer invisible, a black box, or glitchy (Omarchy 4.0.x)

1. Open `~/.config/hypr/looknfeel.lua` and append:

```lua
-- The GPU's hardware cursor plane does not display the pointer here.
hl.config({
  cursor = {
    no_hardware_cursors = true,
  },
})
```

2. Run `hyprctl reload`.

That is the exact block Omarchy itself appends on nouveau machines in `install/user/hardware/fix-nouveau-cursor.sh`, shipped since 4.0.0. It is also the block BigNatoDemon verified on a VMware guest in issue #7918.

Do not put a `cursor { ... }` section in `hyprland.conf` on 4.x. A legacy `.conf` block is ignored once a `hyprland.lua` config exists.

Avoid `hyprctl eval 'hl.config({ cursor = { no_hardware_cursors = true } })'` as a quick test. On at least one AMD build that same eval faults inside Hyprland and takes the whole session down with SIGABRT (issue #8797). Edit the file and reload instead.

### Pointer invisible, a black box, or glitchy (3.8.4 and earlier)

Append to `~/.config/hypr/looknfeel.conf`:

```
cursor {
  no_hardware_cursors = true
}
```

Then `hyprctl reload`. This is the pre-Quattro form of the same setting, and it is what fixed #4847 on an AMD RX 6700 XT dual-monitor setup on 3.4.1.

### Pointer is the wrong size (Omarchy 4.0.x)

The default is 24. Do not create `~/.config/hypr/envs.lua`: nothing requires that module, so anything you set there is silently dropped. Issue #9902 documents this, and the maintainer triage on that issue reproduced it by proving an `XCURSOR_SIZE` override in a personal `envs.lua` never reached spawned clients.

1. Open `~/.config/hypr/hyprland.lua` and add this at the very bottom, under the "Add any other personal Hyprland configuration below" comment:

```lua
hl.env("XCURSOR_SIZE", "32")
hl.env("HYPRCURSOR_SIZE", "32")
```

2. Set the GTK side too, because Omarchy never touches it:

```bash
gsettings set org.gnome.desktop.interface cursor-size 32
```

3. Log out and back in. Environment variables reach applications when they launch, so `hyprctl reload` is not enough.

The tail of `hyprland.lua` is evaluated after `require("default.hypr.omarchy")`, so your value wins over the 24 in `default/hypr/envs.lua`. That ordering is the part the triage on #9902 confirmed on a clean 4.0 worker.

### Pointer is the wrong size (3.8.4 and earlier)

`~/.config/hypr/envs.conf` is not sourced by the shipped `hyprland.conf` on 3.8.4 either. Put `env = XCURSOR_SIZE,32` at the bottom of `~/.config/hypr/hyprland.conf` and log out.

### Wrong cursor theme

Omarchy ships no cursor theme and never sets `org.gnome.desktop.interface cursor-theme`, which is why discussion #8428 got no official answer. Install a theme, then apply it in both places:

```bash
gsettings set org.gnome.desktop.interface cursor-theme "Bibata-Modern-Classic"
hyprctl setcursor Bibata-Modern-Classic 24
```

To make the Hyprland half survive a relogin, add `hl.env("XCURSOR_THEME", "Bibata-Modern-Classic")` alongside the size lines at the bottom of `hyprland.lua`. Check your theme actually provides a cursor named `default`: on discussion #10947 a reporter saw imv 5.0.1 crash with a theme that does not.

## Verify it worked

```bash
hyprctl getoption cursor:no_hardware_cursors
hyprctl configerrors
```

The first should report the value you set, the second should be empty. For the size, read the environment of a freshly launched application rather than trusting the config:

```bash
tr '\0' '\n' < /proc/$(pgrep -n ghostty)/environ | grep -i cursor
```

If the hardware cursor plane was the problem, the error spam stops. Check the session log at `/run/user/$UID/hypr/$HYPRLAND_INSTANCE_SIGNATURE/hyprland.log` for `drmCloseBufferHandle in cursor failed`, which BigNatoDemon counted over 1700 times in a few hours before applying the fix.

## Why it happens

Hyprland normally hands the pointer to a dedicated DRM cursor plane on the GPU. Several drivers accept the buffer and then fail the commit, so the plane shows nothing, a stale black buffer, or a partial smear. Confirmed on nouveau (Omarchy automates the fix there), on VMware's vmwgfx, and on AMD and NVIDIA multi-output setups in #4847 and #4934. Software cursors cost almost nothing on a desktop and simply sidestep the plane.

The size problem is unrelated. Omarchy 4 moved Hyprland config to Lua, and the personal override files that `hyprland.lua` requires are `monitors`, `input`, `bindings`, `looknfeel` and `autostart`. There is no `envs` in that list and Omarchy has never shipped a `config/hypr/envs.lua`, so a file you create there is dead code. The session environment channel the manual points at, `~/.config/uwsm/env.d/*`, is exported before Hyprland starts, so it cannot override anything Omarchy sets with `hl.env` afterwards.

If your pointer fix vanished during the 3 to 4 upgrade, that is expected: `hypr/looknfeel.lua` is on the upgrade's always-copy list, and your old `looknfeel.conf` is deliberately left on disk unread so you can port it by hand.

## If that did not work

- The pointer comes back and then breaks again in the same session. That is #11943, still open on 4.0.3 with `no_hardware_cursors` already set, on a hybrid Intel plus NVIDIA laptop driving four outputs. `hyprctl setcursor Adwaita 24` re-renders it each time, but only until the next recurrence.
- The pointer is visible but laggy across monitors rather than missing. Give each output an explicit rule instead of a generic one, as al3rez did in #2132. Ignore the `WLR_NO_HARDWARE_CURSORS` line in that issue: that variable is ignored by current Hyprland, and the rest of that config is 3.x `.conf` syntax you would have to port.
- The pointer disappears only while you are dragging a screenshot selection. That is #8240, open: `omarchy-capture-screenshot` forces hardware cursors back on before opening the picker so the software pointer is not baked into the capture, which hides it on exactly the hardware that needs software cursors.
- Night light does not tint the pointer. Cosmetic and open as #4973.
- If you lose the pointer on a big screen rather than seeing it broken, discussion #5833 is where people compare the `hypr-dynamic-cursors` plugin. Third party plugins are not covered by Omarchy support.

Checked against the shipped source for v4.0.4 and v3.8.4.

## Related

- [Hybrid GPU laptop black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Fractional scaling looks blurry or huge](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Screenshot shortcut not working](/fix/screenshot-shortcut-not-working/)
- [Hardware notes: hybrid GPU](/hardware/hybrid-gpu/) and [multi-monitor](/hardware/multi-monitor/)
- Omarchy manual: [Keyboard, mouse and trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/)
