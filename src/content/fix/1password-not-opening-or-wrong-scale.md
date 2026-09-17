---
title: "1Password not opening or scaled wrong on Omarchy"
description: "1Password oversized, its unlock or SSH approval dialog clipped, or the window nowhere to be seen on Omarchy 4. Launch it via Omarchy, reset text size."
answer: "Launch 1Password with Super + Shift + / or omarchy launch 1password. Since 4.0.3 that launcher adds --force-device-scale-factor=1, which fixes oversized windows and clipped dialogs. If a dialog is still cut off, run omarchy display text size reset, then fully quit 1Password and start it again. A window that never appears is usually the single running instance stranded off-screen."
appliesTo:
  from: "4.0.0"
status: workaround
fixedIn: "4.0.3"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: apps
issueCount: 68
errorStrings:
  - "1Password is already running, closing."
  - "traps: 1password[8088] trap invalid opcode"
  - "Rejecting MCP connection: Linux peer effective GID check failed"
tags: [1password, scaling, electron, apps, quattro, polkit]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8574"
    title: "Issue #8574: omarchy display text size breaks 1Password's fixed-size dialogs (root cause of #2016)"
    kind: issue
    author: "SilentKernel"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9904"
    title: "Issue #9904: 1Password: unlock popup unusable on fractional scaling, and its window rule targets a non-resizable window"
    kind: issue
    author: "kurtome"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/2016"
    title: "Issue #2016: 1Password authorization window cut off"
    kind: issue
    author: "helioascorreia"
    date: "2025-09-27"
  - url: "https://github.com/omacom/omarchy/issues/8010"
    title: "Issue #8010: 1Password floating window is left off-screen after a monitor is disabled; relaunch focuses the invisible window"
    kind: issue
    author: "dougvk"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/7870"
    title: "Issue #7870: omarchy-install-service-1password launches 1Password without setsid, so it dies on SIGHUP when the installer terminal closes"
    kind: issue
    author: "osamahbeig"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8470"
    title: "Issue #8470: 1password crashes with SIGILL (ILL_ILLOPN) on first launch after fresh install"
    kind: issue
    author: "pgremo"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/10158"
    title: "Issue #10158: 1password 8.12.34-34 crashes with SIGILL on CPUs without AVX-512"
    kind: issue
    author: "inumineq"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/11830"
    title: "Issue #11830: 1password 8.12.36-2 omits MCP group/setgid setup, causing peer authentication rejection"
    kind: issue
    author: "larok00"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/12030"
    title: "Issue #12030: 1password 8.12.36-2: polkit policy bakes in build host's user; vendor after-install.sh never run"
    kind: issue
    author: "edgardoalz"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9576"
    title: "Issue #9576: omarchy-install-1password pins 8.12.0 with an existence-only guard, so Apple Silicon never gets 1Password updates"
    kind: issue
    author: "bierlingm"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/8998"
    title: "Issue #8998: 1Password window is not visible when accessing desktop over sunshine/moonlight"
    kind: issue
    author: "spuder"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3: Fix oversized 1Password windows on scaled displays"
    kind: release
    author: "dhh"
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/commercial-apps-services/"
    title: "Omarchy Manual: Commercial apps/services"
    kind: manual
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy Manual: Troubleshooting"
    kind: manual
credits:
  - name: "SilentKernel"
    url: "https://github.com/SilentKernel"
    for: "Measured that Chromium multiplies the GNOME text scaling factor into its device scale, which clips 1Password's fixed-size dialogs"
  - name: "kurtome"
    url: "https://github.com/kurtome"
    for: "Showed the browser unlock popup is size pinned, so no Hyprland size rule can rescue it"
  - name: "dougvk"
    url: "https://github.com/dougvk"
    for: "Traced the invisible 1Password window to a float stranded outside the remaining monitor"
  - name: "osamahbeig"
    url: "https://github.com/osamahbeig"
    for: "Found that the installer launches 1Password without setsid, so it dies when the installer terminal closes"
faq:
  - q: "Why is my 1Password window huge or its unlock box cut off?"
    a: "Chromium multiplies the GNOME text scaling factor into its own device scale, so 1Password lays out bigger than the window it was given. Omarchy 4.0.3 works around this by launching with --force-device-scale-factor=1. Resetting the text size removes the trigger."
  - q: "Does fingerprint unlock work with 1Password on Omarchy?"
    a: "Set the reader up with Setup > Security > Fingerprint first. Issue #12030 notes that the 1Password unlock polkit action carries no owner annotation, so it is not affected by the packaging bug that breaks the CLI and SSH agent prompts. We have no confirmed report of fingerprint unlock failing on 4.x."
  - q: "Why does 1Password show up black in a screen share or Moonlight stream?"
    a: "Omarchy tags the window no_screen_share on purpose, so it is blanked in captures. Issue #8998 reports the same blanking over Sunshine and Moonlight, which is the rule working as designed rather than a bug."
related: [fractional-scaling-blurry-or-huge-apps, multi-monitor-layout-not-saved, quickshell-crashes-or-bar-missing, theme-not-applied-to-gtk4-apps]
draft: false
---

Checked on 4.0.4 (2026-09-15), with the 4.0.0 through 4.0.3 sources and the last 3.x release, v3.8.4, for comparison.

## The fix

1. Update first. The scaling workaround shipped in 4.0.3, and the 4.0.3 release notes list it as a fix for oversized 1Password windows on scaled displays. Run `omarchy update`, then `omarchy version` to confirm you are on 4.0.3 or newer.

2. Start 1Password the Omarchy way. Press `Super + Shift + /`, pick it from the Omarchy menu, or run `omarchy launch 1password`. In 4.0.3 and 4.0.4 that launcher runs `setsid uwsm-app -- 1password --force-device-scale-factor=1`. Running plain `1password` from a shell skips the flag. On 4.0.0 through 4.0.2 the same launcher had no flag at all.

3. Quit the old instance before you judge the result. 1Password is single instance, and autostart already has one running. A second launch just focuses the existing window, flag or not. Close it from the tray, or run `pkill -x 1password`, then press `Super + Shift + /` again.

4. If a dialog is still clipped, remove the trigger. Run `omarchy display text size` to see the current GTK factor. Anything above 1.0 shrinks the usable area of 1Password's fixed-size dialogs. Run `omarchy display text size reset` to return to 12px and factor 1.0, then restart 1Password.

5. If you want the larger text and a working dialog, pin the environment for the autostart copy too. 1Password rewrites `~/.config/autostart/1password.desktop` on every start, so the setting cannot live there. Omarchy runs autostart entries as systemd user units, so create `/etc/systemd/user/app-1password@autostart.service.d/text-scaling.conf` with `[Service]` and `Environment=GSETTINGS_BACKEND=memory`, then log out and back in. SilentKernel documented this drop-in in issue #8574.

6. If the window never appears at all, it is probably off-screen. After you disable a monitor, the floating 1Password window keeps its old global coordinates and lands outside the remaining display, as dougvk measured in issue #8010. `pkill -x 1password` and relaunch puts it back in the centre.

7. If it died right after installation, just launch it again. The installer opens the app without detaching it, so it takes a SIGHUP when the installer terminal closes, which osamahbeig traced in issue #7870. Nothing is broken; the next launch from the hotkey survives.

## Verify it worked

Check the flag actually reached the process:

```bash
pgrep -af 'force-device-scale-factor'
```

Check where the window ended up and how big it is:

```bash
hyprctl clients -j | jq '.[] | select(.class|test("1[pP]assword")) | {at, size, title}'
```

The `at` coordinates should fall inside one of your enabled monitors. Check the text scaling factor:

```bash
omarchy display text size
```

For the SSH agent prompt specifically, sign something without touching the network, the way issue #8574 reproduces it, and confirm the checkbox and the buttons are both on screen:

```bash
ssh-add -L > /tmp/k.pub
SSH_AUTH_SOCK=~/.1password/agent.sock ssh-keygen -Y sign -f /tmp/k.pub -U -n test /etc/hostname
```

## Why it happens

1Password is an Electron app, and Chromium on Wayland computes its device scale as the monitor scale multiplied by GNOME's `text-scaling-factor`. Omarchy's `omarchy display text size` sets exactly that key, so raising your text size inflates 1Password's internal scale while the window frame stays the size it asked for. Dialogs whose minimum size equals their maximum size, such as the SSH and CLI approval prompt, then lay out into fewer effective pixels than they were designed for, and the bottom of the dialog is pushed out of the frame. SilentKernel measured a device pixel ratio of 2.71875 on a scale 2 monitor at text size 16, and identified this as the root cause of the older issue #2016, which had been closed and blamed on a 1Password regression.

The same arithmetic runs at fractional monitor scales. On a display at scale 1.6, kurtome found the browser unlock popup mapping at 402 by 371 logical pixels while its interface expected roughly 643 by 594, with the password field clipped. That popup is size pinned by the app, so no Hyprland rule can fix it. Omarchy's `default/hypr/apps/1password.lua` tags every 1Password window `floating-window`, which pulls in a 875 by 600 size from `system.lua`; the main window takes it, the popup silently refuses.

Omarchy's answer in 4.0.3 was the launcher flag rather than a window rule. The comment in `omarchy-launch-1password` says 1Password reads the display scale itself and comes up oversized next to everything else, and that the flag covers the hotkey path, which runs the binary directly.

## If that did not work

The 1Password CLI approval prompt or the SSH agent authorization not appearing at all is a different problem. The manual's troubleshooting chapter says the rich prompt needs Settings > Advanced > Use Hardware Acceleration turned on, and a reboot afterwards, and that the prompt never appears if you have not opened 1Password since booting. On top of that, the `[omarchy]` package build has two open packaging bugs: edgardoalz found in issue #12030 that the polkit policy ships with the build host's account name in the owner annotation, and larok00 found in issue #11830 that the MCP group and setgid setup from the vendor's own install script is never applied. Both affect `op` and the SSH agent. Per #12030 the plain unlock action has no owner annotation, so desktop and fingerprint unlock are not in scope of that bug.

If 1Password crashes instantly with SIGILL, read issues #8470 and #10158 together before acting. inumineq attributes it to AVX-512 instructions in the binary, but a later comment on #8470 reports the identical fault at the same offset on an Ice Lake CPU that does have AVX-512, and another commenter argues the install-time case is really the SIGHUP shutdown from #7870. Both are open and neither has a confirmed fix, so try a clean launch from the hotkey before you go hunting for a rebuild.

On Apple Silicon, bierlingm reported in issue #9576 that the aarch64 installer pins version 8.12.0 behind an existence-only guard, so the app never updates there. And if 1Password is simply black in a meeting or a Moonlight session, that is the deliberate `no_screen_share` tag, reported as issue #8998.

Two 3.x differences worth knowing if you are following an older guide. Up to v3.8.4 the window rules lived in `default/hypr/apps/1password.conf` as `windowrule` lines, which is what the "invalid field noscreenshare" config errors in old threads refer to; in 4.x they are Lua. And 3.x shipped a migration that added `gnome-keyring` because 1Password could not save 2FA setup without it. On 4.0.4 `gnome-keyring` is in the base package list, so that particular fix is already in place.

## Related

- [Fractional scaling, blurry or huge apps](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [Theme not applied to GTK4 apps](/fix/theme-not-applied-to-gtk4-apps/)
- [Multi-monitor hardware notes](/hardware/multi-monitor/)
- [Fingerprint reader](/hardware/fingerprint/)
- [Commands reference](/reference/commands/)
