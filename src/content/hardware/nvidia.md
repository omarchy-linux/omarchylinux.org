---
title: "NVIDIA on Omarchy"
description: "NVIDIA GPUs on Omarchy 4.0.4: driver selection by GPU generation, hybrid laptop video decode corruption, kernel module failures, and the fix order."
answer: "Omarchy installs NVIDIA drivers automatically: nvidia-open-dkms on Turing and newer, nvidia-580xx-dkms on Maxwell through Volta, plus early KMS via modprobe and mkinitcpio. Desktop reports are mostly update and packaging failures. Hybrid Intel or AMD laptops are the weak spot: forced NVDEC decode corrupts browser video, and a kernel whose NVIDIA modules did not build freezes or loops the login."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "nvidia"
issueCount: 807
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [nvidia, gpu, drivers, hybrid-graphics, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    title: "install/hardware/nvidia.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-nvidia-gsp"
    title: "bin/omarchy-hw-nvidia-gsp at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-toggle-hybrid-gpu"
    title: "bin/omarchy-toggle-hybrid-gpu at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12129"
    title: "Issue #12129: Black screen / Failure to wake from sleep on NVIDIA hardware"
    kind: issue
    author: "rafi-the-dev"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/8215"
    title: "Issue #8215: 4.0.1: shell_succeeds fix enables NVDEC VAAPI routing on hybrid laptops with Intel-driven displays, corrupting browser video"
    kind: issue
    author: "SisyphusOfCorinth"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/pull/7851"
    title: "PR #7851: Don't force the NVIDIA VA-API driver on hybrid-GPU systems"
    kind: pr
    author: "Suzu1Dev"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6790"
    title: "Issue #6790: NVIDIA installs: kms hook bundles ~100 MB of unused nouveau GSP firmware into every initramfs/UKI"
    kind: issue
    author: "matjam"
    date: "2026-08-13"
  - url: "https://github.com/omacom/omarchy/issues/5706"
    title: "Issue #5706: Login loop after update if nvidia DKMS fails to build for the new kernel"
    kind: issue
    author: "sanity"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/4901"
    title: "Issue #4901: Hybrid Intel+NVIDIA: Chromium hardware acceleration requires manual workarounds"
    kind: issue
    author: "josefdc"
    date: "2026-03-04"
  - url: "https://github.com/omacom/omarchy/issues/12054"
    title: "Issue #12054: omarchy/sunshine 2026.516 package: NVENC broken on Turing, falls back to software x264"
    kind: issue
    author: "trinknx"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1776"
    title: "Issue #1776: Laptop / Hybrid GPU Power Management Issue (NVIDIA, iGPU + dGPU)"
    kind: issue
    author: "itsmedardan"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/issues/2635"
    title: "Issue #2635: Omarchy 3.1 No Signal to Monitors When Waking from Sleep"
    kind: issue
    author: "ochowie"
    date: "2025-10-20"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 Quattro"
    kind: release
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
credits:
  - name: "matjam"
    url: "https://github.com/matjam"
    for: "Finding and fixing the 100 MB of nouveau GSP firmware baked into every NVIDIA initramfs"
  - name: "Suzu1Dev"
    url: "https://github.com/Suzu1Dev"
    for: "Diagnosing the forced NVIDIA VA-API driver on hybrid laptops and proposing the detector fix"
  - name: "SisyphusOfCorinth"
    url: "https://github.com/SisyphusOfCorinth"
    for: "Tracing the 4.0.1 NVDEC video corruption back to the shell_succeeds helper change"
  - name: "sanity"
    url: "https://github.com/sanity"
    for: "Documenting the DKMS build failure that turns into a silent SDDM login loop"
  - name: "stephentaylor-com"
    url: "https://github.com/stephentaylor-com"
    for: "Forcing software cursors on nouveau so the pointer stays visible"
faq:
  - q: "Does Omarchy install NVIDIA drivers for me?"
    a: "Yes. install/hardware/nvidia.sh detects the card from sysfs and installs nvidia-open-dkms on Turing and newer, or nvidia-580xx-dkms on Maxwell, Pascal and Volta. It also writes the modprobe and mkinitcpio drop-ins for early KMS. Pre-Maxwell cards get no driver and stay on nouveau."
  - q: "Why is video corrupted or stuttering in Chromium on my NVIDIA laptop?"
    a: "On hybrid laptops Omarchy sets LIBVA_DRIVER_NAME=nvidia, which sends decode to NVDEC while the Intel or AMD iGPU composites. Set it to iHD or radeonsi in ~/.config/hypr/hyprland.lua, run systemctl --user set-environment with the same value, and restart the browser. Tracked in issue #8215 and PR #7851."
  - q: "My machine freezes after updating to 4.0.4. Is that NVIDIA?"
    a: "It can be. 4.0.4 makes linux-omarchy the default boot kernel. If your NVIDIA modules were built only for the stock Arch kernel, the new default entry boots without them. Pick the stock linux entry in Limine, then make sure you are on nvidia-open-dkms rather than a prebuilt module package."
related: [hybrid-gpu, suspend-sleep, multi-monitor]
draft: false
---

Omarchy has real NVIDIA support, not an afterthought. The installer detects your card, picks a driver branch by GPU generation, and configures early kernel mode setting. On a desktop with a single NVIDIA card, the open reports are about what happens at update time and in packaging, not about the driver setup itself. On a hybrid laptop, where an Intel or AMD iGPU drives the panel and the NVIDIA chip sits behind it, most of the open complaints live.

This page was checked against v4.0.4, released 2026-09-15, using the v4.0.4 source tree. The issue counter in the sidebar covers every NVIDIA-matching issue and discussion in the tracker, open and closed, so treat it as a measure of traffic rather than of current breakage.

## Status on 4.0.4

Which driver you get depends on the PCI device ID of your card.

- **Turing or newer**, meaning device ID `0x1e00` and above, roughly GTX 16 series and RTX 20 series onward. You get `nvidia-open-dkms`, `nvidia-utils`, `lib32-nvidia-utils` and `libva-nvidia-driver`. This is the supported path.
- **Maxwell, Pascal and Volta**, device IDs `0x1340` through `0x1dff`, roughly GTX 700 later parts through GTX 10 series and Titan V. You get the legacy `nvidia-580xx-dkms` branch. Omarchy's own repos carry 580.178.04 on the stable, rc and edge channels.
- **Kepler and older.** The installer prints that there is no compatible driver and points at the Arch wiki. You stay on nouveau, and the software cursor fix below is the only NVIDIA-specific thing Omarchy does for you.

Vulkan comes from `nvidia-utils` on NVIDIA. The separate `vulkan.sh` installer only handles Intel, AMD and Apple.

## What Omarchy does automatically

**Detects from sysfs, not lspci.** `omarchy-hw-nvidia`, `omarchy-hw-nvidia-gsp` and `omarchy-hw-nvidia-without-gsp` read cached IDs under `/sys/bus/pci/devices`. The 4.0.0 notes explain why: an `lspci` call touches PCI config space, which pulls a runtime-suspended dGPU out of D3cold, and on a hybrid laptop that wake by itself blows through the 1.5 seconds Hyprland allows for loading its config.

**Configures early KMS.** It writes `options nvidia_drm modeset=1` to `/etc/modprobe.d/nvidia.conf` and `MODULES+=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)` to `/etc/mkinitcpio.conf.d/nvidia.conf`.

**Drops the kms hook where it is dead weight.** Since 4.0.0, `omarchy_hooks.conf` removes `kms` from `HOOKS` when `nvidia_drm` is early-loaded and NVIDIA owns every display controller. That cuts nouveau and about 100 MB of its GSP firmware out of the initramfs, the problem matjam measured in issue #6790 on a 256 MB unified kernel image. Hybrid machines keep `kms`, because the iGPU still needs it for the LUKS prompt. A migration rebuilds existing images once.

**Sets session environment in Lua.** `default/hypr/nvidia.lua` sets `NVD_BACKEND=direct`, `LIBVA_DRIVER_NAME=nvidia` and `__GLX_VENDOR_LIBRARY_NAME=nvidia` on GSP cards, and `NVD_BACKEND=egl` plus the GLX variable on older ones. In 3.x these were `.conf` env lines; in 4.x they are Lua, which matters if you are copying an old guide. See [the conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

**Offers a hybrid GPU toggle.** If `omarchy-hw-hybrid-gpu` reports hybrid, the Omarchy menu shows Hardware, Hybrid GPU, which runs `omarchy-toggle-hybrid-gpu`. That installs `supergfxctl`, writes `/etc/supergfxd.conf`, enables the daemon, and reboots. Switching to Integrated also installs a `supergfxd` startup delay, because starting it in Integrated mode races the display manager and can freeze the boot, and a `force-igpu` sleep hook that flips the card through Vfio back to Integrated after resume, and to Vfio before hibernate so the driver is never asked to freeze a powered-off dGPU.

**Fixes the nouveau cursor.** If you end up on nouveau, an installer appends `no_hardware_cursors = true` to your `looknfeel.lua`, because on many older cards nouveau never shows the hardware cursor plane, so under Hyprland you get no visible pointer at all.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#12187](https://github.com/omacom/omarchy/issues/12187) hard freeze about 5 seconds after login on the new default kernel | Lenovo hybrid, Intel iGPU plus RTX 4070 Max-Q, on prebuilt `nvidia-open` rather than DKMS | Open | not fixed |
| [#5706](https://github.com/omacom/omarchy/issues/5706) DKMS fails to build for a new kernel, SDDM login loop with no visible error | RTX 3090 Ti, 3060 Ti, 4060 Ti | Open, assigned, [PR #6840](https://github.com/omacom/omarchy/pull/6840) proposed | not fixed |
| [#8215](https://github.com/omacom/omarchy/issues/8215) NVDEC VA-API routing corrupts or kills browser video | Hybrid Intel plus RTX 3050, Meteor Lake plus RTX 4050, AMD Cezanne plus RTX 3050 Ti | Open, [PR #7851](https://github.com/omacom/omarchy/pull/7851) proposed | not fixed |
| [#4901](https://github.com/omacom/omarchy/issues/4901) cross-GPU DMA-BUF import fails, `eglCreateImage failed with 0x00003009` | Hybrid Intel plus RTX 3050, AMD plus NVIDIA confirmations | Open, [PR #5312](https://github.com/omacom/omarchy/pull/5312) proposed | not fixed |
| [#12129](https://github.com/omacom/omarchy/issues/12129) black screen on resume from suspend | ASUS TUF F17 FX707VI, RTX 4070 Mobile, kernel 7.2.5-3-omarchy | Open, no comments yet | not fixed |
| [#12054](https://github.com/omacom/omarchy/issues/12054) Sunshine NVENC probe fails, falls back to software x264 | RTX 2080 Ti, single report | Open, no comments yet | not fixed |
| [#6790](https://github.com/omacom/omarchy/issues/6790) about 100 MB of unused nouveau GSP firmware in every initramfs | All NVIDIA-only installs | Closed | 4.0.0 |
| [#1776](https://github.com/omacom/omarchy/issues/1776) dGPU never reaches D3cold, battery drains | Hybrid Intel plus NVIDIA laptops | Closed 2026-02-01 as completed, thread is a manual setup guide | no linked fix |

Two of these deserve detail.

**The kernel module gap.** 4.0.4 ships the bespoke `linux-omarchy` kernel to everyone and makes it the default boot entry. In issue #12187 the reporter was on the prebuilt `nvidia-open` package rather than the `nvidia-open-dkms` that Omarchy installs, so modules existed only under the stock kernel's tree. Every boot on `7.2.5-3-omarchy` froze about five seconds after login, with `systemd-modules-load` failing to find `nvidia_uvm` and `supergfxd` reporting `nvidia_drm` missing. The stock `linux` entry worked with identical userspace. Issue #5706 is the same shape from a different angle: DKMS failed to build, mkinitcpio printed `module not found: 'nvidia'`, and the result was a login loop that gives the user no error at all.

**The hybrid video decode regression.** Omarchy 4.0.0 had a broken `o.shell_succeeds` helper, so the NVIDIA branch of `nvidia.lua` never ran. 4.0.1 fixed the helper, which switched `LIBVA_DRIVER_NAME=nvidia` on for the first time. On hybrid machines the iGPU composites while decode is forced to NVDEC, and the cross-GPU buffer import goes wrong. Reporters in issue #8215 describe stale frames rotating on a three frame cycle, wallpaper punch-through, and on one machine `vaEndPicture failed, VA error: internal decoding error` on every decoder instance. It reproduces with AMD iGPUs as well as Intel, so it is not Mesa iris specific.

Issue #2635, monitors showing no signal after wake, is often filed as an NVIDIA bug and the original report is a 3070. Read the thread before assuming: several confirmations are AMD Beelink mini PCs. Treat it as a display wake problem, not an NVIDIA one.

## Fixes that work

Work in this order.

1. **Confirm your driver branch.** Run `omarchy-hw-nvidia-gsp; echo $?`. Zero means you should be on `nvidia-open-dkms`. Then check what is actually installed with `pacman -Qs nvidia`.
2. **Make sure the package is the DKMS one.** A prebuilt `nvidia-open` only has modules for the kernel it was built against. That is the trap in issue #12187.
3. **Check modules exist for the kernel you boot.** `uname -r`, then `dkms status`, then `ls /usr/lib/modules/$(uname -r)/`. If NVIDIA modules are missing there, do not reboot yet.
4. **If you are already frozen or looping,** pick the stock `linux` entry in Limine instead of the `linux-omarchy` one, or roll back with [Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/). Fix DKMS from a working session. See [login loop or password not accepted](/fix/login-loop-or-password-not-accepted-sddm/) and [black screen after login](/fix/black-screen-after-login/).
5. **For hybrid video corruption,** add `hl.env("LIBVA_DRIVER_NAME", "iHD")` to `~/.config/hypr/hyprland.lua`, using `radeonsi` instead on an AMD iGPU. Also run `systemctl --user set-environment LIBVA_DRIVER_NAME=iHD` so you do not have to log out, then restart the browser. Reporters note this variable affects video decode only, not Vulkan, OpenGL, NVENC or `prime-run`. One reporter in issue #4901 found that on a machine where Chromium renders through NVIDIA EGL, changing only the VA-API driver killed hardware decode entirely; the EGL vendor override in that thread has to go with it. More in [Chromium flicker and hardware acceleration](/fix/chromium-flicker-hardware-acceleration/).
6. **For battery drain on a hybrid laptop,** try the Hybrid GPU toggle in the Omarchy menu and switch to Integrated. Details on [the hybrid GPU page](/hardware/hybrid-gpu/).
7. **For resume failures,** start with [suspend will not resume](/fix/suspend-wont-resume-s2idle/) and [the suspend and sleep page](/hardware/suspend-sleep/), and say in your report whether the stock kernel behaves differently.

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` containing `inxi -Farz`, `dmesg`, this boot's warnings and errors from the journal, and your full package list. Use `--no-sudo` to skip `dmesg` and `--print` to print instead of saving. See [the command reference](/reference/commands/omarchy-debug/).

For an NVIDIA report, add four things the log does not make obvious: the output of `lspci -k | grep -A3 -i vga`, `dkms status`, the exact Limine entry you booted, and whether the problem also happens on the stock `linux` entry. That last one separates a kernel module gap from a driver bug and is the single most useful line you can include.

If your machine works, or works with one tweak, [submit it](/hardware/submit/) so the model pages get more accurate.

## Related

- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Hybrid GPU laptop black screen and AQ_DRM_DEVICES](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [Kernel panic after update with Limine](/fix/kernel-panic-after-update-limine/)
- [Steam or Proton game crashes](/fix/steam-or-proton-game-crashes/)
- [Cursor invisible or wrong size](/fix/cursor-invisible-or-wrong-size/)
- [Release channels](/releases/channels/) and [v4.0.4](/releases/v4.0.4/)
- Omarchy manual: [Troubleshooting](https://omarchy.org/manual/troubleshooting/) and [Gaming](https://omarchy.org/manual/gaming/)
