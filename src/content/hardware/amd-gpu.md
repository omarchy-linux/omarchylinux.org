---
title: "AMD GPUs on Omarchy"
description: "What works and what breaks on AMD Radeon graphics under Omarchy 4.x: kernel and firmware regressions, DPMS lock flaps, hybrid GPU env vars, fixes."
answer: "AMD graphics work out of the box on Omarchy 4.x. The kernel ships amdgpu, and Omarchy only adds vulkan-radeon. Most real breakage is a kernel or firmware regression, not a config problem. If your display blanks or freezes after an update, boot the previous kernel from Limine first, then check linux-firmware-amdgpu and Mesa versions before changing anything else."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "amd-gpu"
issueCount: 418
tags: [amd, amdgpu, radeon, graphics, mesa, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/9720"
    title: "Issue #9720: Black screen on boot on AMD Strix Point / Radeon 890M laptops (ASUS ROG Zephyrus G14) due to Aquamarine atomic DRM commit failure"
    kind: issue
    author: "codyoss"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/12083"
    title: "Issue #12083: 4K@120 HDMI screen blanks for seconds on every new frame after linux-omarchy 7.2.5-3 (AMD Navi 33)"
    kind: issue
    author: "berkesadam74"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11499"
    title: "Issue #11499: ddcutil 3.0.0 hangs the amdgpu SMU at every login via the shell's brightness probe (RX 7600), session hard-freezes"
    kind: issue
    author: "hegjon"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/8863"
    title: "Issue #8863: Display flickers off/on repeatedly after idle lock on AMD APU + HDMI/DP (DPMS flap loop)"
    kind: issue
    author: "pablo-io"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/7514"
    title: "Issue #7514: Stable mirror contains broken linux-firmware-amdgpu 20260810-1"
    kind: issue
    author: "mwheelersmith"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/5984"
    title: "Issue #5984: linux-firmware-amdgpu 20260519 (DMUB 0x09004700) black-screens Strix Halo + 5K DSC display"
    kind: issue
    author: "melonamin"
    date: "2026-05-27"
  - url: "https://github.com/omacom/omarchy/issues/11687"
    title: "Issue #11687: nvidia.lua forces LIBVA_DRIVER_NAME=nvidia on hybrid AMD+NVIDIA laptops, breaking Chromium/Brave video"
    kind: issue
    author: "Yarlord"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/10410"
    title: "Issue #10410: LIBVA_DRIVER_NAME=nvidia is set even when the NVIDIA GPU drives no output, stalling video playback on hybrid laptops"
    kind: issue
    author: "sl4ppy"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/12041"
    title: "Issue #12041: Whole-screen rainbow/color corruption after lid resume on hybrid AMD+NVIDIA laptop"
    kind: issue
    author: "BigRed4547"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/6089"
    title: "Issue #6089: Vulkan driver not backfilled: pre-vulkan.sh installs left without Mesa Vulkan ICD"
    kind: issue
    author: "ki11e6"
    date: "2026-06-14"
  - url: "https://github.com/omacom/omarchy/issues/8856"
    title: "Issue #8856: omarchy-install-gaming-steam pulls nvidia-utils onto non-NVIDIA systems"
    kind: issue
    author: "microfire21-og"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/10380"
    title: "Issue #10380: Ollama install menu picks CUDA/CPU on AMD systems"
    kind: issue
    author: "bel-maty"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/4496"
    title: "Issue #4496: xdg-desktop-portal-hyprland crashes (SIGSEGV) when starting screen recording on AMD RDNA4 (RX 9070)"
    kind: issue
    author: "datalektiker"
    date: "2026-02-04"
  - url: "https://github.com/omacom/omarchy/issues/10852"
    title: "Issue #10852: AMD display freeze retains valid mode and active CRTC, bypassing monitor recovery"
    kind: issue
    author: "theinventor"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/vulkan.sh"
    title: "install/hardware/vulkan.sh in v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-install-gaming-gpu-lib32"
    title: "bin/omarchy-install-gaming-gpu-lib32 in v4.0.4"
    kind: commit
    date: "2026-09-15"
credits:
  - name: "hegjon"
    url: "https://github.com/hegjon"
    for: "Traced the ddcutil 3.0.0 login freeze to the shell brightness probe and the amdgpu SMU hang"
  - name: "pablo-io"
    url: "https://github.com/pablo-io"
    for: "Identified HDMI audio jack events as the wake source in the lock screen DPMS flap loop"
  - name: "melonamin"
    url: "https://github.com/melonamin"
    for: "Bisected the DMUB firmware regression that black-screened Strix Halo with a 5K DSC display"
  - name: "codyoss"
    url: "https://github.com/codyoss"
    for: "Documented the AQ_NO_ATOMIC session environment fix for Strix Point black screens"
faq:
  - q: "Do I need to install an AMD driver on Omarchy?"
    a: "No. The amdgpu kernel driver and Mesa are already there. Omarchy only adds vulkan-radeon at install time, plus lib32-vulkan-radeon if you install Steam."
  - q: "My AMD display started blanking after updating to 4.0.4. What changed?"
    a: "4.0.4 installs the bespoke linux-omarchy kernel and makes it the default boot entry. Three reporters on Navi 33, Radeon 780M and Radeon 680M describe display blanking on 7.2.5-3, and two confirm it stops when they boot the stock Arch kernel from Limine. See issue #12083."
  - q: "Is ROCm installed for AMD compute?"
    a: "No. A stock install gets Mesa and vulkan-radeon only. That is one reason the Ollama menu entry misdetects AMD machines in issue #10380: its `rocminfo` check never fires, and a stray `nvidia-smi` from nvidia-utils wins instead."
related: [nvidia, hybrid-gpu, multi-monitor, suspend-sleep]
draft: false
---

AMD is the easiest graphics vendor to run on Omarchy, because there is almost nothing to install. The tradeoff is that when something does break, it is usually a kernel, firmware or Mesa regression arriving through `omarchy update`, and the fix is a package version rather than a config change.

## Status on 4.0.4

Checked against Omarchy 4.0.4 (2026-09-15) and the v4.0.4 source tree. Integrated Radeon graphics (Rembrandt 680M, Phoenix 780M, Hawk Point, Strix Halo) and discrete Radeon cards (Navi 31, 32, 33, 48) all reach a working Hyprland desktop without manual driver work; every report below was filed from a running session on one of them. Strix Point 890M laptops are the exception, where #9720 documents a black screen at login until an Aquamarine variable is set.

Our issue data tracks 418 issues touching this component, 269 of them open, but that count is misleading. The match pattern catches any report from a machine that happens to have a Radeon in it. The genuinely AMD specific failures cluster in four places: kernel and firmware regressions, display link flaps around lock and DPMS, hybrid AMD plus NVIDIA environment variables, and the external monitor brightness probe.

## What Omarchy does automatically

There is no `amd.sh` in `install/hardware/`. `all.sh` runs an NVIDIA script and an Intel directory, but AMD gets exactly one step:

- `install/hardware/vulkan.sh` greps `lspci` for `(VGA|Display).*AMD` and installs `vulkan-radeon`. That is the whole AMD driver story at install time.
- `migrations/1784401744.sh` backfills `vulkan-radeon` on machines that were installed before `vulkan.sh` existed. It shipped with 4.0.0 and closed issue #6089, where a pre-existing install had no Mesa Vulkan ICD at all.
- `bin/omarchy-install-gaming-gpu-lib32` adds `lib32-vulkan-radeon` when you install Steam or other 32 bit games.
- `bin/omarchy-hw-display` prefers an `amdgpu_bl*` backlight device over `intel_backlight` and `acpi_video*` when picking the panel to dim.
- `bin/omarchy-hw-hybrid-gpu` detects an iGPU plus dGPU pair, and `bin/omarchy-toggle-hybrid-gpu` drives `supergfxctl` on those laptops, installing the daemon and writing `/etc/supergfxd.conf` on first use.
- `bin/omarchy-brightness-display-ddc` handles external monitor brightness with `ddcutil`, which matters below.

Notably, Omarchy does not list `amdgpu` in `MODULES` in `mkinitcpio.conf`. Only the NVIDIA, Surface and Apple scripts touch `MODULES`. AMD still gets early KMS, because `etc/mkinitcpio.conf.d/omarchy_hooks.conf` keeps the `kms` hook, which lets autodetect pull `amdgpu` and its firmware into the UKI. That is why a firmware downgrade in #5984 only took effect after `limine-mkinitcpio` rebuilt the boot image.

4.0.4 also installs the bespoke `linux-omarchy` kernel on every machine and makes it the default boot entry. The release notes credit it with smoother gaming on supported AMD HDMI displays. On some RDNA2 and RDNA3 setups the same kernel is currently the problem.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#12083](https://github.com/omacom/omarchy/issues/12083) display blanks for seconds at 4K@120 over HDMI on linux-omarchy 7.2.5-3 | Navi 33, Radeon 780M, Radeon 680M | open | not yet |
| [#11499](https://github.com/omacom/omarchy/issues/11499) ddcutil 3.0.0 hangs the amdgpu SMU at every login, whole session freezes | RX 7600 on Omarchy, with upstream ddcutil reports on RX 7900 XT/XTX and RX 9070 XT | open | not yet |
| [#8863](https://github.com/omacom/omarchy/issues/8863) display flickers off and on for the whole lock, thousands of DPMS transitions | Hawk Point, Cezanne, Renoir, RX 7700 XT | open | not yet |
| [#9720](https://github.com/omacom/omarchy/issues/9720) black screen after login, Aquamarine atomic DRM commit fails | Radeon 890M Strix Point laptops | open | not yet |
| [#11687](https://github.com/omacom/omarchy/issues/11687), [#10410](https://github.com/omacom/omarchy/issues/10410) black video in Chromium and Brave because LIBVA_DRIVER_NAME is forced to nvidia | Phoenix and other AMD iGPUs paired with an NVIDIA dGPU | open | not yet |
| [#12041](https://github.com/omacom/omarchy/issues/12041) rainbow color corruption after lid resume, survives shell restart | Rembrandt APU plus RTX 3050 | open | not yet |
| [#4496](https://github.com/omacom/omarchy/issues/4496) portal SIGSEGV when starting a screen recording | RX 9070 XT, RDNA4 gfx1201 | open | not yet |
| [#7514](https://github.com/omacom/omarchy/issues/7514) color corruption in AV1 video from broken linux-firmware-amdgpu 20260810-1 | RX 9070 XT and other gfx12 | fixed | firmware 20260810-2 on the stable mirror |
| [#5984](https://github.com/omacom/omarchy/issues/5984) black screen from a DMUB firmware regression | Strix Halo with a 5K DSC display | closed, no fix named | reporter downgraded to 20260410-1 and rebuilt the UKI |
| [#10852](https://github.com/omacom/omarchy/issues/10852) sole display freezes with a valid mode and active CRTC, so monitor recovery never fires, a DPMS cycle restores the session | Strix Halo with a 5120x1440@144 DSC display | closed | aquamarine 0.15.0-2, on six days of follow-up rather than a bisect |
| [#6089](https://github.com/omacom/omarchy/issues/6089) no Mesa Vulkan ICD on installs predating vulkan.sh | any AMD or Intel install from before 2026-02-20 | fixed | 4.0.0 |
| [#8856](https://github.com/omacom/omarchy/issues/8856) Steam install pulls nvidia-utils onto AMD only machines | Radeon 780M and other AMD only systems | open | not yet |
| [#10380](https://github.com/omacom/omarchy/issues/10380) Ollama menu installs ollama-cuda on AMD | RX 7900 XT and similar | open | not yet |

Two patterns are worth calling out. First, the 4.0.4 kernel. In #12083 a Gigabyte M28U at 3840x2160@120 blanks for several seconds on every static to active transition after `linux-omarchy 7.2.5-3` lands, and drops to a stable picture at 60 Hz. Two other reporters on the same thread, on a Radeon 780M and a Radeon 680M, say booting the still installed stock `linux 7.2.3.arch1-3` stops it completely. The 780M reporter's journal shows `DC: failed to blank crtc!` and `REG_WAIT timeout` lines on the omarchy kernel only.

Second, the lock screen flap. The lock plugin blanks the display five seconds after locking with a live DPMS off. On AMD parts with an HDMI or DP audio codec, the link drop generates jack switch events that count as activity, which wakes the lock and re-arms the blank. One reporter in #8863 logged over four thousand display sleep transitions in a single overnight lock. PRs #8896 and #10343 propose debounces but neither is merged as of 4.0.4.

## Fixes that work

Work in this order.

1. If it started after an update, boot the previous kernel from the Limine menu before changing anything. On 4.0.4 that means picking the `Omarchy/linux` entry instead of the `linux-omarchy` one. This is the single highest yield step for AMD display faults right now.
2. Check `linux-firmware-amdgpu` and Mesa versions. Both #7514 and #5984 were firmware regressions delivered by a normal update, and #7514 also had a Mesa side fix. `pacman -Qi linux-firmware-amdgpu mesa vulkan-radeon` tells you where you are. The stable mirror can lag Arch by days, so a fixed package may exist upstream before it reaches you.
3. If the session hard freezes seconds after login on a desktop with a discrete Radeon and no laptop panel, downgrade `ddcutil` to 2.2.7-1 and add it to `IgnorePkg`. That is the confirmed workaround in #11499.
4. If the lock screen flickers, `omarchy toggle idle stay-awake` stops the blank from arming, which is the workaround used in #8863.
5. On Strix Point laptops that black screen at login, export `AQ_NO_ATOMIC=1` in the session environment, not in `hyprland.lua`. Aquamarine reads it before Lua config runs, so `~/.config/uwsm/env-hyprland` is the right place. See #9720.
6. On hybrid AMD plus NVIDIA laptops where the panel hangs off the AMD iGPU, unset the forced NVIDIA variables for the affected app. Reporters in #11687 confirm `env -u LIBVA_DRIVER_NAME -u __GLX_VENDOR_LIBRARY_NAME` restores video.
7. For a high refresh HDMI panel that blanks, pin a lower mode in `~/.config/hypr/monitors.lua`. Dropping to 60 Hz is the documented workaround in #12083.

See [the Omarchy manual's monitors chapter](https://omarchy.org/manual/monitors/) for `monitors.lua` scaling examples, and the Hyprland monitor docs it links for mode syntax.

## Report it

Collect diagnostics with `omarchy-debug --no-sudo --print`, which writes `/tmp/omarchy-debug.log` and includes `inxi -Farz`, the current boot's journal warnings and your package list. Run it without `--no-sudo` to add `dmesg`, and without `--print` to get the upload option. Issue #11988 reports that the `omarchy debug` subcommand is not registered on 4.0.3, so call the script directly if the subcommand fails.

For a display fault, add `hyprctl monitors all`, the exact `linux`, `linux-omarchy`, `mesa`, `vulkan-radeon`, `libdrm` and `linux-firmware-amdgpu` versions, and whether the problem survives booting the other installed kernel. Reports that name a working kernel and a broken one get triaged fastest, as the #12083 thread shows.

## Related

- [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) for AMD iGPU plus NVIDIA dGPU laptops
- [/hardware/nvidia/](/hardware/nvidia/) for the NVIDIA side of those machines
- [/fix/black-screen-after-login/](/fix/black-screen-after-login/)
- [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/)
- [/fix/steam-or-proton-game-crashes/](/fix/steam-or-proton-game-crashes/)
- [/hardware/multi-monitor/](/hardware/multi-monitor/)
- [/releases/still-broken/](/releases/still-broken/)
- [/hardware/submit/](/hardware/submit/) to add your machine
