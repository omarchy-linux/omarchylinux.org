---
title: "Intel GPUs on Omarchy"
description: "Intel GPU support in Omarchy 4.x: what the installer sets up, the hybrid LIBVA_DRIVER_NAME bug, Panther Lake panel quirks, and the fix order that works."
answer: "Intel graphics on an Intel-only machine is the best supported setup in Omarchy 4.x. The installer adds intel-media-driver, libvpl and vulkan-intel for you. Almost all real breakage is hybrid Intel plus NVIDIA, where nvidia.lua forces LIBVA_DRIVER_NAME=nvidia and corrupts browser video. Override it to iHD after the Omarchy require in hyprland.lua. Panther Lake panels need their kernel flags checked."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "intel-gpu"
issueCount: 293
tags: [intel, gpu, vaapi, vulkan, panther-lake, hybrid-gpu]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8215"
    title: "Issue #8215: 4.0.1: shell_succeeds fix enables NVDEC VAAPI routing on hybrid laptops with Intel-driven displays, corrupting browser video"
    kind: issue
    author: "SisyphusOfCorinth"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8328"
    title: "Issue #8328: nvidia.lua forces LIBVA_DRIVER_NAME=nvidia on hybrid laptops where the dGPU drives no displays"
    kind: issue
    author: "emshiarla"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8989"
    title: "Issue #8989: Hybrid iGPU-primary laptops: nvidia.lua forces NVIDIA env session-wide"
    kind: issue
    author: "karluiz"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/4901"
    title: "Issue #4901: Hybrid Intel+NVIDIA: Chromium hardware acceleration requires manual workarounds"
    kind: issue
    author: "josefdc"
    date: "2026-03-04"
  - url: "https://github.com/omacom/omarchy/pull/7851"
    title: "PR #7851: Don't force the NVIDIA VA-API driver on hybrid-GPU systems"
    kind: pr
    author: "Suzu1Dev"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11958"
    title: "Issue #11958: intel/video-acceleration.sh doesn't match Intel Wildcat Lake GPU, skips installing intel-media-driver"
    kind: issue
    author: "theswampdawg"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/1441"
    title: "Issue #1441: Zed fails to load on Intel GPU"
    kind: issue
    author: "ElBrodino"
    date: "2025-09-04"
  - url: "https://github.com/omacom/omarchy/issues/5695"
    title: "Issue #5695: Black image on resume from suspend (sometimes ~60s freeze) after 3.7 kernel bump to 7.0"
    kind: issue
    author: "b-Tomas"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/5573"
    title: "Issue #5573: XPS 14 internal panel frozen after 3.7.0 upgrade"
    kind: issue
    author: "rblalock"
    date: "2026-05-04"
  - url: "https://github.com/omacom/omarchy/issues/12188"
    title: "Issue #12188: linux-omarchy kernel breaks screen backlight and USB audio volume on Dell XPS 14 (Panther Lake)"
    kind: issue
    author: "cthybert"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12147"
    title: "Issue #12147: LG display stays off after wake: dpmsStatus desyncs true while panel has no signal"
    kind: issue
    author: "SykesTheLord"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12152"
    title: "Issue #12152: External-only HDMI display becomes unusable after idle lock/DPMS wake with eDP-1 disabled"
    kind: issue
    author: "dudis"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11943"
    title: "Issue #11943: Hardware cursor intermittently stops rendering on hybrid Intel/NVIDIA multi-monitor laptop"
    kind: issue
    author: "Cousint98"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/6985"
    title: "Issue #6985: Quattro (4.0) install fails: fix-synaptic-touchpad.sh psmouse module mismatch + vulkan.sh offline mirror missing files"
    kind: issue
    author: "ahmedsrea"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    title: "install/hardware/intel/video-acceleration.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
    author: "dhh"
    date: "2026-09-15"
credits:
  - name: "SisyphusOfCorinth"
    url: "https://github.com/SisyphusOfCorinth"
    for: "Pinned the hybrid VA-API regression to the 4.0.1 shell_succeeds fix"
  - name: "emshiarla"
    url: "https://github.com/emshiarla"
    for: "Showed nvidia.lua fires even when the dGPU has no display connectors"
  - name: "jtmorris"
    url: "https://github.com/jtmorris"
    for: "Measured the battery cost of the forced NVIDIA session variables"
  - name: "theswampdawg"
    url: "https://github.com/theswampdawg"
    for: "Found the Wildcat Lake gap in the video acceleration detector"
  - name: "spencerbull"
    url: "https://github.com/spencerbull"
    for: "Traced Panther Lake panel freezes to a stale panel replay boot flag"
  - name: "SykesTheLord"
    url: "https://github.com/SykesTheLord"
    for: "Traced the stuck-display-after-wake path in omarchy-brightness-display"
faq:
  - q: "Do I need to install anything for Intel graphics on a fresh Omarchy 4 install?"
    a: "No. The installer runs intel/video-acceleration.sh and vulkan.sh, which add intel-media-driver, libvpl, vpl-gpu-rt and vulkan-intel when it sees an Intel display device. The known gap is Wildcat Lake, which the detector regex misses (issue #11958)."
  - q: "Why is video corrupted in Chromium on my Intel plus NVIDIA laptop?"
    a: "Omarchy sets LIBVA_DRIVER_NAME=nvidia session-wide when it sees a GSP-era NVIDIA GPU, so decode runs on the dGPU while the Intel iGPU composites. Set it back to iHD in hyprland.lua. Tracked in issues #8215, #8328 and #8989."
  - q: "Is the xe driver or i915 used on my machine?"
    a: "It depends on generation and kernel. Reports on Meteor Lake in 2026 still show i915 messages, while Panther Lake machines report xe. Run journalctl -k and grep for both names rather than guessing."
related: [nvidia, hybrid-gpu, multi-monitor, suspend-sleep]
draft: false
---

Intel graphics is the quietest GPU class on Omarchy. On a machine where an Intel iGPU is the only GPU and drives the panel, 4.0.4 generally installs, boots and plays video with nothing added by hand. Almost every noisy Intel report in the tracker is really one of two other things: a hybrid Intel plus NVIDIA laptop where session variables point at the wrong GPU, or a Panther Lake panel fighting its kernel flags.

This page was checked against the v4.0.4 source tree and against issues open on 2026-09-16.

## Status on 4.0.4

Intel-only desktops and laptops: works. Mesa handles rendering, `intel-media-driver` handles VA-API decode and encode, and `vulkan-intel` handles Vulkan. The 293 issues that mention Intel graphics are dominated by hybrid machines, not by Intel-only ones.

Hybrid Intel plus NVIDIA: partial, and worse on 4.0.1 and later than it was on 4.0.0. See the hybrid section below and [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/).

Panther Lake (Core Ultra X series, Arc B-series iGPU): mostly works, with active regressions. This is the newest silicon Omarchy ships for, and the kernel it ships changed twice in a month. 4.0.3 moved the Panther Lake kernel to 7.2.3, and 4.0.4 made the bespoke `linux-omarchy` kernel the default boot entry for everyone.

Old Intel (GMA era, pre-2014): still handled, but with the legacy `libva-intel-driver` rather than the modern stack.

## What Omarchy does automatically

The installer runs these on every machine, and `omarchy-update` reruns the hardware phase:

- `install/hardware/intel/video-acceleration.sh` looks at the `lspci` display line and installs `intel-media-driver`, `libvpl` and `vpl-gpu-rt` when the name matches HD Graphics, UHD Graphics, Xe, Iris, Arc or Panther Lake. GMA-era parts get `libva-intel-driver` instead.
- `install/hardware/vulkan.sh` installs `vulkan-intel` when a display-class Intel device is present. This is what made Zed start on Intel machines after issue #1441.
- `install/hardware/intel/fred.sh` writes `/etc/limine-entry-tool.d/intel-panther-lake-fred.conf` with `fred=on` when `omarchy-hw-intel-ptl` matches. Added in 3.7.0.
- `install/hardware/intel/thermald.sh` and `intel/lpmd.sh` install and enable thermald and intel-lpmd on Intel laptops, which shapes how hard the iGPU is allowed to run.
- `install/hardware/asus/fix-asus-ptl-display-backlight.sh` adds `xe.enable_dpcd_backlight=1`, and `asus/fix-asus-ptl-b9406-display.sh` adds `xe.enable_panel_replay=0`. Both are gated to the ASUS ExpertBook B9406 and Zenbook UX5406AA, and the scripts say other models still need confirmation.
- `install/hardware/intel/ipu7-camera.sh` installs `intel-ipu7-camera` for MIPI webcams. That stack has its own problems, covered at [/hardware/webcam/](/hardware/webcam/).

The detectors behind this are `omarchy-hw-intel` (CPU vendor), `omarchy-hw-intel-ptl` (a Panther Lake display device), `omarchy-hw-vulkan` and `omarchy-hw-hybrid-gpu`. There is also `omarchy-hw-dell-xps-oled`, which matches an LG OLED panel on a Panther Lake XPS, but nothing in the 4.0.4 tree calls it.

One thing Omarchy does that hurts Intel: `default/hypr/nvidia.lua` sets `LIBVA_DRIVER_NAME=nvidia`, `NVD_BACKEND=direct` and `__GLX_VENDOR_LIBRARY_NAME=nvidia` whenever a GSP-era NVIDIA GPU is present, and `autostart.lua` exports that into the systemd user environment for every app.

## Known problems

The hybrid VA-API regression is the big one. On 4.0.0 the `o.shell_succeeds` helper always returned false inside Hyprland, so `nvidia.lua` was dead code and hybrid machines were accidentally correct. 4.0.1 fixed the helper, the variables took effect, and browser video broke. SisyphusOfCorinth pinned that in issue #8215; reporters there confirm it on Raptor Lake, Meteor Lake and AMD iGPU pairings. emshiarla's issue #8328 shows the detector only asks whether an NVIDIA chip exists, not whether it drives a display, and jtmorris measured roughly six extra watts in a browser because the dGPU never runtime-suspends. Issue #8989 adds that a user override placed before the Omarchy require is silently overwritten. PR #7851 proposes gating the variable on a sysfs hybrid check; it is still open.

Panther Lake panels are the second cluster. Issue #5573 was a 3.x case where a stale `xe.enable_panel_replay=0` line survived in `/etc/default/limine` and froze the XPS 14 internal panel after 3.7.0; spencerbull reproduced it and a hotfix went out as v3.7.1. Issue #12188 is the current one: after 4.0.4 makes `linux-omarchy` 7.2.5 the default, brightness keys on a Dell XPS 14 write successfully to `intel_backlight` but the panel does not change, and booting the stock `linux` 7.2.3 entry restores it. That symptom matches what the ASUS backlight script describes, so `xe.enable_dpcd_backlight=1` is worth testing there, but nobody has confirmed it on an XPS.

Displays that stay dark after idle are the third. Issue #12147 traces it into `omarchy-brightness-display`: the script skips the DPMS enable when Hyprland already reports every monitor lit, and a failed atomic commit can leave that flag stuck true while the panel has no signal. Issue #12152 is the external-only variant on Haswell i915, recovered with a VT switch.

Older i915 resume failures are still open in issue #5695, with PHY and transcoder timeouts on Meteor Lake after the 7.0 kernel bump.

### Known issues

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#8215](https://github.com/omacom/omarchy/issues/8215) NVDEC routed to the dGPU, corrupt browser video | Hybrid Intel or AMD iGPU plus NVIDIA | Open, workaround known | Not yet, PR #7851 open |
| [#8328](https://github.com/omacom/omarchy/issues/8328) NVIDIA env forced when the dGPU drives no display | Dell XPS 14 9440, Raptor Lake laptops | Open | Not yet |
| [#8989](https://github.com/omacom/omarchy/issues/8989) User override defeated, dGPU cannot suspend | Lenovo Legion 7i Pro, Arrow Lake | Open | Not yet |
| [#4901](https://github.com/omacom/omarchy/issues/4901) Chromium acceleration needs manual flags | Iris Xe plus RTX 3050 | Open | Not yet |
| [#11958](https://github.com/omacom/omarchy/issues/11958) Wildcat Lake skipped by the detector regex | Wildcat Lake iGPU | Open | Not yet |
| [#12188](https://github.com/omacom/omarchy/issues/12188) Backlight dead on linux-omarchy 7.2.5 | Dell XPS 14 DA14260, Arc B390 | Open | Not yet |
| [#12147](https://github.com/omacom/omarchy/issues/12147) Monitor stays off after idle wake | Multi-monitor, external LG 4K | Open | Not yet |
| [#12152](https://github.com/omacom/omarchy/issues/12152) External-only HDMI unusable after wake | Haswell i915 laptops | Open | Not yet |
| [#11943](https://github.com/omacom/omarchy/issues/11943) Hardware cursor stops rendering | Hybrid Intel plus NVIDIA, 4 monitors | Open | Not yet |
| [#5695](https://github.com/omacom/omarchy/issues/5695) Black image and long freeze on resume | ThinkPad P1 Gen 7, Meteor Lake | Open | Not yet |
| [#5573](https://github.com/omacom/omarchy/issues/5573) Internal panel frozen after upgrade | Dell XPS 14, Panther Lake | Fixed | 3.7.1 |
| [#1441](https://github.com/omacom/omarchy/issues/1441) Zed fails to start, no Vulkan driver | Any Intel iGPU | Fixed | Installer vulkan.sh, backfilled in 3.8.3 |
| [#6985](https://github.com/omacom/omarchy/issues/6985) Install stops at vulkan.sh on the 4.0 ISO | Intel ThinkPads, free-space install | Fixed | 4.0.1 ISO, PR #7236 |

## Fixes that work

Work in this order.

1. Find out what you actually have. Run `lspci -k | grep -A3 -E 'VGA|3D|Display'` and `journalctl -k | grep -E 'i915|xe '`. Then run `vainfo` and `systemctl --user show-environment | grep -E 'LIBVA|GLX|NVD'`.
2. If `LIBVA_DRIVER_NAME` is `nvidia` and your panel hangs off the Intel iGPU, that is your bug. In `~/.config/hypr/hyprland.lua`, after `require("default.hypr.omarchy")`, add `hl.env("LIBVA_DRIVER_NAME", "iHD")` and `hl.env("__GLX_VENDOR_LIBRARY_NAME", "mesa")`. It must come after the require, or it is overwritten. To avoid a relogin, also run `systemctl --user set-environment LIBVA_DRIVER_NAME=iHD` and restart the browser. Reporters in issue #8215 confirmed this on several chassis.
3. If `vainfo` finds no driver at all, install the packages by hand: `sudo pacman -S intel-media-driver libvpl vpl-gpu-rt libva-utils`. On Wildcat Lake this is expected until issue #11958 lands.
4. If a Vulkan app refuses to start, check `pacman -Q vulkan-intel`. Installing it is the whole fix.
5. On Panther Lake with a panel problem, read `/etc/default/limine` and `/etc/limine-entry-tool.d/`. Remove any `xe.enable_psr=0` or `xe.enable_panel_replay=0` line left over from 3.5 or 3.6, run `sudo limine-update`, and reboot.
6. If the trouble started with 4.0.4, boot the older `linux` entry once from the Limine menu. The 4.0.4 migration keeps the previous kernel installed for exactly this. If the problem disappears, say so in a `linux-omarchy` issue.
7. If a display stays dark after idle, force a real transition: `hyprctl dispatch 'hl.dsp.dpms({ action = "disable" })'` then the same with `enable`.
8. For Chromium specifically, see [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/).

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, dmesg, the current boot journal at warning level and up, and your package list. Use `omarchy debug --print` to read it first, and `--no-sudo` if you would rather leave dmesg out.

Attach that, plus the exact output of `lspci -k` for the display device, `vainfo`, `systemctl --user show-environment`, `uname -r`, and which Limine entry you booted. For hybrid machines, say which connector your panel is on and whether the dGPU exposes any DRM connectors at all, because that is the distinction the current detector misses. Hardware reports for this site go to [/hardware/submit/](/hardware/submit/).

## Related

[/hardware/hybrid-gpu/](/hardware/hybrid-gpu/), [/hardware/nvidia/](/hardware/nvidia/), [/hardware/multi-monitor/](/hardware/multi-monitor/), [/hardware/suspend-sleep/](/hardware/suspend-sleep/), [/hardware/dell-xps-14-2026/](/hardware/dell-xps-14-2026/), [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/), [/fix/cursor-invisible-or-wrong-size/](/fix/cursor-invisible-or-wrong-size/), [/releases/v4.0.4/](/releases/v4.0.4/), [/reference/commands/omarchy-debug/](/reference/commands/omarchy-debug/). Manual chapter: [Monitors](https://omarchy.org/manual/monitors/).
