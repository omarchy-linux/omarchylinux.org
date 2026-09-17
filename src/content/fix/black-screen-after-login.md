---
title: "Black screen after login on Omarchy"
description: "Black screen after login on Omarchy 4: tell a dead Hyprland apart from a dead Quickshell, get a TTY, and fix the GPU, uwsm env, and VM causes."
answer: "Get a TTY with Ctrl+Alt+F2 and check whether Hyprland is running. If it is, the Quickshell bar died: run omarchy-restart-shell and read journalctl -b -t omarchy-shell. If it is not, Hyprland aborted at GPU init. The usual causes on 4.x are an NVIDIA kernel and userspace mismatch after an update, a colon in AQ_DRM_DEVICES, or a broken file in ~/.config/uwsm/env.d."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 121
errorStrings:
  - "Omarchy shell exited with status 255; relaunching."
  - "Giving up on the Omarchy shell after 6 relaunches in under a minute."
  - "drm: Found no gpus to use, cannot continue"
  - "[AQ] atomic drm request: failed to commit: Cannot allocate memory"
  - 'Env output mark "<hex>" not found in shell output'
  - "quickshell: symbol lookup error: quickshell: undefined symbol"
  - "WARN: The Wayland connection experienced a fatal error: Invalid argument"
tags: [black-screen, hyprland, quickshell, nvidia, sddm, display]
sources:
  - url: "https://github.com/omacom/omarchy/issues/5706"
    title: "Issue #5706: Login loop after update if nvidia DKMS fails to build for the new kernel"
    kind: issue
    author: "sanity"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/8776"
    title: "Issue #8776: Dual-GPU AMD: PCI by-path in AQ_DRM_DEVICES silently login-loops SDDM autologin"
    kind: issue
    author: "mowgli42"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/10700"
    title: "Issue #10700: Silent lock-screen login loop when ~/.config/uwsm/env.d has a shell error (UWSM preloader fails with no UI)"
    kind: issue
    author: "austrasien"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/9720"
    title: "Issue #9720: Black screen on boot on AMD Strix Point / Radeon 890M laptops (ASUS ROG Zephyrus G14) due to Aquamarine atomic DRM commit failure"
    kind: issue
    author: "codyoss"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8113"
    title: "Issue #8113: Omarchy unusable under VMware Workstation with 3D acceleration enabled"
    kind: issue
    author: "cavanaug"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/8438"
    title: "Issue #8438: Omarchy 4.0.1 migration 1787399318 installs a Qt 6.11.2-built quickshell that cannot start on the Qt 6.11.1 pin from #7750"
    kind: issue
    author: "greencubator1"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7750"
    title: "Issue #7750: Qt 6.11.2 SIGSEGV in QUntypedPropertyBinding on Omarchy shell startup (Variants / Repeater)"
    kind: issue
    author: "rliessum"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/10930"
    title: "Issue #10930: omarchy-launch-shell exits silently when compositor_alive() false-negatives during output reconfiguration, leaving no bar"
    kind: issue
    author: "matti-lamppu"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/11213"
    title: "Issue #11213: omarchy-shell crashes (exit 255) on resume when FALLBACK monitor is removed, briefly showing Hyprland's lock-crashed screen"
    kind: issue
    author: "coloradobum"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/discussions/7758"
    title: "Discussion #7758: Omarchy on VirtualBox"
    kind: discussion
    author: "nightdevil00"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/pull/8786"
    title: "PR #8786: Fix AQ_DRM_DEVICES by-path login loop"
    kind: pr
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
credits:
  - name: "sanity"
    url: "https://github.com/sanity"
    for: "Traced the SDDM loop to a stale UKI carrying an old NVIDIA module, and posted the modprobe recovery"
  - name: "mowgli42"
    url: "https://github.com/mowgli42"
    for: "Found that Aquamarine splits AQ_DRM_DEVICES on every colon, so by-path GPU pins kill Hyprland"
  - name: "Elshayib"
    url: "https://github.com/Elshayib"
    for: "Wrote PR #8786, the proposed by-path sanitizer for AQ_DRM_DEVICES"
  - name: "greencubator1"
    url: "https://github.com/greencubator1"
    for: "Separated the exit 127 symbol lookup failure from the Qt 6.11.2 SIGSEGV and posted the keep-the-pin workaround"
  - name: "austrasien"
    url: "https://github.com/austrasien"
    for: "Showed that one bad line in ~/.config/uwsm/env.d loops the login screen with no visible error"
  - name: "rodolfoghi"
    url: "https://github.com/rodolfoghi"
    for: "Diagnosed the VirtualBox black screen down to the vmwgfx channel error and a software GL workaround"
  - name: "codyoss"
    url: "https://github.com/codyoss"
    for: "Documented the AQ_NO_ATOMIC workaround for AMD Strix Point laptops"
faq:
  - q: "How do I get a terminal when the screen is black?"
    a: "Press Ctrl+Alt+F2, and try F3 through F6 if F2 does nothing. You get a text login. If no console key works, reboot and pick an older snapshot from the Limine menu, which boots the same way but with an older system state."
  - q: "Is a black screen with a visible mouse cursor the same problem as a black screen with nothing at all?"
    a: "Usually not. A cursor most often means Hyprland is running and the Quickshell shell died, so there is no bar, no wallpaper and no lock screen. No cursor usually means Hyprland never started, which is almost always a GPU or session environment problem. The cursor is not proof, though: the VirtualBox report in discussion #7758 had a cursor with Hyprland dead, so check with pgrep rather than trusting the pointer."
  - q: "Will rolling back a snapshot fix it?"
    a: "Only if the cause is in the system tree. Issue #10700 and a comment in issue #8776 both note that the offending file lives under /home, which snapshots of the root subvolume do not revert, so every snapshot in the Limine menu inherits the same broken value."
related: [quickshell-crashes-or-bar-missing, hybrid-gpu-laptop-black-screen-aq-drm-devices, nvidia-drivers-omarchy-4, login-loop-or-password-not-accepted-sddm, stuck-at-tty-or-cannot-switch-tty]
draft: false
---

A black screen after login is two different failures wearing the same face. Either Hyprland never started, or Hyprland started and the Quickshell shell that draws everything died. Telling them apart takes one command and decides everything else you do. Every script name and journal message below was checked against the 4.0.4 source tree.

## The fix

Every step here runs from a text console. Nothing can be done from the black screen itself.

1. **Get a TTY.** Press Ctrl+Alt+F2 and log in as your normal user. If nothing happens, try F3 through F6. Some people get no console at all, as in issue [#5706](https://github.com/omacom/omarchy/issues/5706); in that case reboot and pick an older snapshot from the Limine menu, then read the rest of this page from there.

2. **Find out which half is broken.**

   ```bash
   pgrep -a Hyprland
   ls "$XDG_RUNTIME_DIR"/hypr 2>/dev/null
   ```

   A running Hyprland with an instance directory means the compositor is fine and the shell is gone. Go to step 3. Nothing listed means Hyprland aborted. Go to step 4.

3. **Hyprland is alive, the shell is not.** This is usually the cursor-on-black case. Restart the shell:

   ```bash
   omarchy-restart-shell
   journalctl -b -t omarchy-shell
   ```

   The `omarchy-shell` journal tag is where Quickshell's output goes, because `omarchy-launch-shell` pipes it through `systemd-cat`. Three signatures matter.

   `exited with status 127` plus `symbol lookup error`, with nothing in `coredumpctl list`, means the quickshell binary and the installed Qt do not match. In issue [#8438](https://github.com/omacom/omarchy/issues/8438) that happened because the reporter had pinned `qt6-*` at 6.11.1 in `/etc/pacman.conf` to dodge issue [#7750](https://github.com/omacom/omarchy/issues/7750), and the 4.0.1 migration then installed a quickshell built against 6.11.2. The reporter's workaround is to keep the pin and reinstall the matching `quickshell-git` package from the pacman cache with `sudo pacman -U`, then `omarchy restart shell`, all from the TTY because the polkit agent lives inside the dead shell. Dropping the pin instead brings back the #7750 crash, which was closed as an upstream Qt bug rather than fixed. If you never pinned anything and still see exit 127, the triage in the same thread points at mirror skew, and a full `sudo pacman -Syu` once your mirror has caught up is the answer.

   A run of SIGSEGVs with coredumps, ending in `Giving up on the Omarchy shell after 6 relaunches`, is #7750 itself: Qt 6.11.2 crashes the shell on first graph load.

   `WARN: The Wayland connection experienced a fatal error` as the last `omarchy-shell` line is the supervisor problem in issues [#10930](https://github.com/omacom/omarchy/issues/10930) and [#11213](https://github.com/omacom/omarchy/issues/11213), usually after a dock hotplug or a resume. Sometimes it is followed by `exited with status 255; relaunching` and the shell comes back on its own; in #10930 the supervisor gave up silently because Hyprland was busy reconfiguring outputs and missed the liveness check. The restart above is the recovery. The 4.0.4 `omarchy-launch-shell` still has that silent exit path, so there is no fix in 4.0.4.

4. **Hyprland never started.** Read the journal before changing anything:

   ```bash
   journalctl -b -p 4..1 | tail -60
   journalctl -b | grep -Ei 'hyprland|aquamarine|uwsm_env-preloader'
   ```

   Then match what you see:

   **`drm: Found no gpus to use, cannot continue`.** Something set `AQ_DRM_DEVICES` to a value Aquamarine cannot parse. It splits the variable on every colon, so any `/dev/dri/by-path/pci-0000:13:00.0-card` string becomes three nonexistent paths and the compositor dies with no message on screen. Find it and remove it:

   ```bash
   grep -rn AQ_DRM_DEVICES ~/.config/uwsm/ ~/.config/hypr/ /etc/environment 2>/dev/null
   ```

   Delete the line. If you genuinely need to pin a GPU, do not swap in `/dev/dri/cardN` either: the reporter of issue [#8776](https://github.com/omacom/omarchy/issues/8776) found those numbers rotate between boots on their hardware, and used a udev rule that gives each card a colon-free name like `/dev/dri/igpu` instead. The same failure was reported in that thread on a dual-AMD desktop and again on an MSI hybrid laptop running 4.0.3. PR [#8786](https://github.com/omacom/omarchy/pull/8786) proposes a sanitizer but was still open when this page was written, and there is no `AQ_` handling anywhere in the 4.0.4 tree.

   **`uwsm_env-preloader` errors, or `Env output mark ... not found in shell output`.** A shell syntax error in any file under `~/.config/uwsm/env.d/` aborts the session environment preloader, and you bounce straight back to the lock or login screen with no error. Move the file out of the directory, not just rename it, because uwsm sources every entry it finds:

   ```bash
   mkdir -p ~/uwsm-broken && mv ~/.config/uwsm/env.d/99-bad ~/uwsm-broken/
   ```

   That is issue [#10700](https://github.com/omacom/omarchy/issues/10700), on a Framework 13 running 4.0.2.

   **NVIDIA, and the black screen started right after an update.** If DKMS failed to build for a new kernel, your boot image can still carry the old NVIDIA module while userspace is already upgraded, and Hyprland aborts during EGL init. From the console:

   ```bash
   sudo systemctl stop sddm
   sudo modprobe -r nvidia_drm nvidia_uvm nvidia_modeset nvidia
   sudo modprobe nvidia
   sudo systemctl start sddm
   ```

   That recovery is from the reporter of issue [#5706](https://github.com/omacom/omarchy/issues/5706). It gets you logged in now, but the boot image is still stale, so rebuild it before you reboot. Another user in the same thread reported that `sudo pacman -Syyu nvidia` from a TTY was what fixed it for them.

   **`[AQ] atomic drm request: failed to commit` on an AMD Strix Point laptop.** The reporter of issue [#9720](https://github.com/omacom/omarchy/issues/9720), on a ROG Zephyrus G14 with a Radeon 890M, got past this with `AQ_NO_ATOMIC=1` in the session environment, not in `hyprland.lua`. Their finding is that Aquamarine reads it before Hyprland parses Lua, so `hl.env()` is too late. Put `export AQ_NO_ATOMIC=1` in `~/.config/uwsm/env-hyprland` and reboot. They also set `WLR_NO_HARDWARE_CURSORS=1` alongside it.

   **You are in a VM.** In VirtualBox, a commenter on discussion [#7758](https://github.com/omacom/omarchy/discussions/7758) traced a cursor-on-black to Hyprland aborting at GPU init with `vmwgfx` channel errors, on 4.0.2. Their fix is all three of: the VMSVGA controller with 128 MB of video memory and 3D acceleration on, `virtualbox-guest-utils` installed with `vboxservice` enabled, and software GL forced by adding `hl.env("LIBGL_ALWAYS_SOFTWARE", "1")` to `~/.config/hypr/hyprland.lua` right after the bootstrap line. Editing `hyprland.conf` does nothing on 4.x. VMware Workstation with 3D acceleration is a different shape: Hyprland runs but the shell dies on a Wayland protocol error, tracked as an open bug in issue [#8113](https://github.com/omacom/omarchy/issues/8113), where a commenter reports `hl.env("QT_QUICK_BACKEND", "software")` keeps the shell up without pushing the compositor onto llvmpipe. See [running Omarchy in VirtualBox](/run/virtualbox/) and [VMware](/run/vmware-workstation-fusion/).

## Verify it worked

Log in again. You should get the wallpaper and the bar within a second or two. If you fixed a shell problem, `journalctl -b -t omarchy-shell` should be quiet after the restart, with no `relaunching` and no `Giving up on the Omarchy shell` lines. If you fixed a compositor problem, `pgrep -a Hyprland` should return a process and `hyprctl monitors` should list your displays. Run `omarchy-debug --print --no-sudo | head -40` to confirm the version you are actually on.

## Why it happens

Omarchy 4 splits the desktop into two processes that can fail independently. Hyprland is the compositor. Everything you can see, the bar, wallpaper, notifications, menus, on-screen displays and the lock screen, is one Quickshell process started by `omarchy-launch-shell` from `default/hypr/autostart.lua`. Before 4.0.0 those jobs were spread across Waybar, Walker, Mako, SwayOSD, hyprlock and swaybg, so a single crash took out one piece. Now it takes out all of them at once, and the result is a usable but completely blank desktop.

The compositor side fails earlier and harder. Once `AQ_DRM_DEVICES` is set, Aquamarine takes the explicit-device branch with no fallback to automatic GPU selection, which is why a malformed value is fatal rather than merely degraded. The uwsm session environment has the same shape of problem: the preloader either produces a full environment or aborts, and the session manager treats the abort as a failed login. In both cases SDDM just shows the greeter again, or on autologin installs simply loops, and nothing is printed where a user would see it.

## If that did not work

Collect the evidence before asking anywhere. `omarchy-debug` writes `/tmp/omarchy-debug.log` with `inxi -Farz`, dmesg, the current-boot journal at warning level and up, and the package list. Add `coredumpctl list Hyprland` and `journalctl -b -1 -t omarchy-shell` for the boot that failed.

If the black screen only appears when an external display or a dock is attached, it is more likely a monitor layout problem than a GPU one; see [multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/) and the manual chapter on [monitors](https://omarchy.org/manual/monitors/). If the screen goes black on resume rather than at login, that is [suspend](/fix/suspend-wont-resume-s2idle/), not this. If the bar comes back but keeps dying, read [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/).

Rolling back is a reasonable move when an update caused this, but be careful about what a rollback actually restores. Issue #10700 and a comment in issue #8776 both point out that the file at fault sits under `/home`, so every snapshot in the Limine menu inherits it. In the NVIDIA thread, one user reported an older snapshot booted fine while another said none of theirs did. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

Evidence for 3.x is thinner and mostly historical. The black-screen reports on GitHub mention 3.x more often than any single 4.x release, but the most-discussed ones are install and first-boot failures on older ISOs, and the shell-side causes above cannot apply because Quickshell did not exist before 4.0.0. The NVIDIA recovery above comes from a 3.x-era report, issue #5706, and the mechanism it describes, a UKI that was not rebuilt after a failed DKMS build, is the same Limine and mkinitcpio setup 4.0.4 installs.

## Related

- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/) and [NVIDIA hardware notes](/hardware/nvidia/)
- [Hybrid GPU laptop black screen and AQ_DRM_DEVICES](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/) and [hybrid GPU](/hardware/hybrid-gpu/)
- [Login loop or password not accepted in SDDM](/fix/login-loop-or-password-not-accepted-sddm/)
- [Stuck at TTY or cannot switch TTY](/fix/stuck-at-tty-or-cannot-switch-tty/)
- [What changed in Quattro](/upgrade/3-to-4-quattro/)
