---
title: "NVIDIA drivers on Omarchy 4"
description: "How Omarchy 4 detects your NVIDIA GPU, which driver package it installs, the env vars it sets, and the fix order when the NVIDIA driver breaks."
answer: "Omarchy 4 picks the driver by PCI device ID: Turing and newer get nvidia-open-dkms, Maxwell through Volta get nvidia-580xx-dkms, older cards get nothing. Most breakage is DKMS having no module built for the kernel you actually booted. Install the matching dkms package plus headers for every installed kernel, rebuild the initramfs, and reboot. On hybrid laptops also override LIBVA_DRIVER_NAME."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 850
errorStrings:
  - "No compatible driver for your NVIDIA GPU."
  - "error: target not found: nvidia-580xx-dkms"
  - "==> ERROR: module not found: 'nvidia'"
  - "Failed to find module 'nvidia_uvm'"
  - "The module nvidia_drm is missing"
  - "ERROR! Allocate Root client failed 0x59"
  - "eglCreateImage failed with 0x00003009"
tags: [nvidia, display, dkms, hybrid-gpu, kernel, quattro]
sources:
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel (prebuilt nvidia-open has no modules for it)"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/5706"
    title: "Issue #5706: Login loop after update if nvidia DKMS fails to build for the new kernel"
    kind: issue
    author: "sanity"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/7755"
    title: "Issue #7755: NVIDIA env vars (NVD_BACKEND, LIBVA_DRIVER_NAME, __GLX_VENDOR_LIBRARY_NAME) never set: os.execute() broken inside Hyprland Lua config"
    kind: issue
    author: "seanymc85"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/pull/6939"
    title: "PR #6939: Fix o.shell_succeeds() always returning false inside Hyprland"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
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
  - url: "https://github.com/omacom/omarchy/issues/7947"
    title: "Issue #7947: nvidia.sh fails on Pascal GPUs (MX150): nvidia-580xx-dkms and lib32-nvidia-580xx-utils not found"
    kind: issue
    author: "gtech-pedrol"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6216"
    title: "Issue #6216: omarchy-hw-nvidia-without-gsp misclassifies Turing-based MX cards (e.g. MX550) as no-GSP, causing driver conflict with Steam install"
    kind: issue
    author: "AndresSM415"
    date: "2026-07-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro) notes"
    kind: release
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4 notes"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.3.0"
    title: "Release v3.3.0 notes"
    kind: release
    date: "2026-01-07"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    title: "Source: install/hardware/nvidia.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-nvidia-gsp"
    title: "Source: bin/omarchy-hw-nvidia-gsp at v4.0.4"
    kind: commit
credits:
  - name: "dhh"
    url: "https://github.com/dhh"
    for: "Fixed o.shell_succeeds() inside Hyprland so the NVIDIA env vars fire at all"
  - name: "sanity"
    url: "https://github.com/sanity"
    for: "Traced the login loop to a DKMS build failure leaving a stale kernel image"
  - name: "SisyphusOfCorinth"
    url: "https://github.com/SisyphusOfCorinth"
    for: "Isolated the 4.0.1 VA-API routing regression on hybrid laptops"
  - name: "Nord-Nogare"
    url: "https://github.com/Nord-Nogare"
    for: "Reported the 4.0.4 freeze when NVIDIA modules exist only for the old kernel"
faq:
  - q: "Does Omarchy install nvidia-open or the proprietary driver?"
    a: "Omarchy installs nvidia-open-dkms on Turing and newer. On Maxwell, Pascal and Volta it installs the proprietary legacy branch, nvidia-580xx-dkms. There is no menu option to switch between them."
  - q: "Why does my old card get no driver at all?"
    a: "The detector only claims PCI device IDs from 0x1340 up. Kepler and older fall below that line, so the installer prints a message and skips the driver. Those cards fall back to nouveau."
  - q: "Do I need to set NVD_BACKEND or __GLX_VENDOR_LIBRARY_NAME myself?"
    a: "No. default/hypr/nvidia.lua sets them per session from 4.0.1 onward. On 4.0.0 they were silently never set, which PR 6939 fixed."
related: [hybrid-gpu-laptop-black-screen-aq-drm-devices, black-screen-after-login, chromium-flicker-hardware-acceleration, suspend-wont-resume-s2idle, login-loop-or-password-not-accepted-sddm]
draft: false
---

Omarchy 4 has no NVIDIA chapter in the manual and no driver picker in the menu. The whole policy lives in two short files: `install/hardware/nvidia.sh` chooses the packages, and `default/hypr/nvidia.lua` sets the session environment. Almost every NVIDIA report on 4.x is one of three things: the wrong branch got picked, DKMS has no module for the kernel you booted, or the VA-API default is wrong for a hybrid laptop. Work through them in that order.

## The fix

### 1. Find out which branch your card is on

```bash
lspci -nn | grep -Ei 'vga|3d|display'
omarchy-hw-nvidia; echo "nvidia=$?"
omarchy-hw-nvidia-gsp; echo "gsp=$?"
omarchy-hw-nvidia-without-gsp; echo "legacy=$?"
```

Exit code 0 means yes. Since 4.0.0 these read PCI IDs from `/sys/bus/pci/devices` instead of shelling out to `lspci`. A device ID of `0x1e00` or higher is Turing or newer and takes the GSP branch. `0x1340` up to `0x1e00` is Maxwell, Pascal or Volta and takes the legacy branch. Below `0x1340` nothing matches and the installer prints `No compatible driver for your NVIDIA GPU.`

### 2. Install the matching packages

Turing and newer:

```bash
sudo pacman -S --needed nvidia-open-dkms nvidia-utils lib32-nvidia-utils libva-nvidia-driver
```

Maxwell, Pascal, Volta:

```bash
sudo pacman -S --needed nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils
```

The 580xx packages come from the Omarchy repository, not from Arch. They are present in the stable, rc and edge channels at 580.178.04 as of 2026-09-17. If pacman says `error: target not found: nvidia-580xx-dkms`, your mirror list is missing the Omarchy repo or the mirror is unreachable. See [/releases/channels/](/releases/channels/).

Use the DKMS package, not a prebuilt `nvidia-open`. A prebuilt package carries modules for one specific Arch kernel and nothing is prebuilt for `linux-omarchy`, which is exactly the gap #12187 fell into.

### 3. Give DKMS headers for every installed kernel

On x86_64 machines that are not T2 Macs, 4.0.4 installs the bespoke `linux-omarchy` kernel and makes it the first Limine boot entry. DKMS needs headers for it or no NVIDIA module gets built for the entry you now boot by default.

```bash
pacman -Qq | grep -E '^linux(-omarchy|-lts|-zen|-t2)?$'
sudo pacman -S --needed linux-omarchy-headers
dkms status
```

`dkms status` should list your nvidia module as `installed` against every kernel version you can boot. 4.0.4 also ships a migration that installs `linux-omarchy-headers` where a fresh ISO install left them out; `omarchy-migrate` applies it if it has not run yet.

### 4. Check the boot pieces

```bash
cat /etc/modprobe.d/nvidia.conf
cat /etc/mkinitcpio.conf.d/nvidia.conf
```

The first should hold `options nvidia_drm modeset=1`. The second should add `nvidia nvidia_modeset nvidia_uvm nvidia_drm` to `MODULES`. If either is missing, recreate it and rebuild.

### 5. Rebuild and reboot

```bash
sudo limine-mkinitcpio
sudo limine-entry-tool --tree
reboot
```

Read the rebuild output rather than trusting the exit code. `mkinitcpio` can print a successful image line and then `ERROR: mkinitcpio failed for kernel X, skipping` right after it, which is how #5706 turned a DKMS failure into a silent login loop.

### 6. Hybrid laptops: undo the VA-API default

Only if an iGPU drives your displays. Add to `~/.config/hypr/hyprland.lua`, which loads after the defaults:

```lua
hl.env("LIBVA_DRIVER_NAME", "iHD")      -- radeonsi on an AMD iGPU
```

Then either relogin or, for the current session, `systemctl --user set-environment LIBVA_DRIVER_NAME=iHD` and restart the browser.

## Verify it worked

```bash
nvidia-smi
cat /sys/module/nvidia_drm/parameters/modeset
systemctl --user show-environment | grep -E 'NVD_BACKEND|LIBVA_DRIVER_NAME|__GLX'
```

`modeset` should read `Y`. On a GSP card the environment should show `NVD_BACKEND=direct`, `LIBVA_DRIVER_NAME=nvidia` and `__GLX_VENDOR_LIBRARY_NAME=nvidia`. On a Maxwell to Volta card you should see `NVD_BACKEND=egl` and `__GLX_VENDOR_LIBRARY_NAME=nvidia`, with `LIBVA_DRIVER_NAME` correctly absent. If you set the override in step 6, your value wins.

`vainfo --display drm --device /dev/dri/renderD128` tells you which VA-API driver actually loaded.

## Why it happens

NVIDIA kernel modules and userspace libraries must match exactly. Anything that lets them drift, a DKMS build that fails, headers that were never installed, a new default kernel with no module built for it, produces the same class of failure: Hyprland aborts at EGL init, SDDM bounces you back, or the session freezes seconds after login. That is the mechanism behind #5706, filed in May 2026 before Quattro, and #12187 on 4.0.4, where the NVIDIA modules existed only under the stock kernel's directory while `linux-omarchy` had become the default entry.

The branch split exists because NVIDIA dropped Maxwell, Pascal and Volta in its 590 drivers. Omarchy added the legacy 580xx path in v3.3.0 to keep those cards working. In 3.x the split was decided by matching card names out of `lspci`, which misread Turing-era MX parts as legacy and caused pacman conflicts, as reported in #6216. v4.0.0 replaced that with the device ID test, which also stopped the detector from waking a runtime-suspended dGPU on every config reload.

The environment variables are newer trouble. In 4.0.0 they were never set at all: the helper behind them used `os.execute`, and Hyprland reaps child processes itself before Lua can collect an exit status, so every branch took the false path (#7755). PR #6939 rewrote the helper and v4.0.1 shipped it. That fix then turned on `LIBVA_DRIVER_NAME=nvidia` for the first time on hybrid laptops where the iGPU owns the displays, so browsers started decoding on the dGPU and importing frames across PCIe into an iGPU GL context. Reporters on #8215 and #8328 measured corrupted frames, dead decode, higher dGPU power draw and juddery scrolling. `nvidia.lua` is byte-identical from v4.0.0 through v4.0.4 and unchanged on the `quattro` branch as of 2026-09-17. Two PRs that gate the variables on whether NVIDIA drives a display, #7851 and #9483, are still open, and a third, #11431, was closed without merging. Until one lands, the user override is the only remedy.

## If that did not work

- Session dies before you see a desktop: go to [/fix/black-screen-after-login/](/fix/black-screen-after-login/).
- Black screen only on a hybrid laptop: [/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/).
- Machine will not boot the new entry at all: [/fix/kernel-panic-after-update-limine/](/fix/kernel-panic-after-update-limine/). A stock `linux` entry in the Limine menu is the escape hatch while you rebuild.
- Browser flicker that survives the `LIBVA_DRIVER_NAME` override: the EGL vendor, not VA-API, is the remaining half. One reporter on #8215 measured EGL import errors dropping to zero only after also pointing `__EGL_VENDOR_LIBRARY_FILENAMES` at the Mesa ICD for that one browser. See [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/).
- Pre-Maxwell card: Omarchy packages no driver for it and the installer says so. You are on nouveau, and Omarchy forces software cursors there.

Evidence for 4.0.4 specifically is still thin. #12187 was filed on 2026-09-16 with one reaction and no comments, so treat the kernel and module mismatch as a single well-documented report rather than a settled pattern.

## Related

- [/hardware/nvidia/](/hardware/nvidia/) and [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/)
- [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/fix/steam-or-proton-game-crashes/](/fix/steam-or-proton-game-crashes/)
- [/reference/commands/omarchy-hw-nvidia/](/reference/commands/omarchy-hw-nvidia/)
- [/upgrade/before-you-update-checklist/](/upgrade/before-you-update-checklist/)
