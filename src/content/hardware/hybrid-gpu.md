---
title: "Hybrid and dual GPU laptops on Omarchy"
description: "What works and what breaks on Intel or AMD iGPU plus NVIDIA dGPU laptops running Omarchy 4.x, with the real issue numbers, the quirk scripts, and the fix order."
answer: "Hybrid laptops boot and run on Omarchy 4.x. Hyprland composites on the iGPU and the dGPU sits idle until you use prime-run. Three things break often: nvidia.lua forces LIBVA_DRIVER_NAME=nvidia and corrupts browser video, suspend and resume can freeze the compositor, and the dGPU rarely reaches D3cold. Fix video first with LIBVA_DRIVER_NAME=iHD."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "hybrid-gpu"
issueCount: 204
tags: [hybrid-gpu, optimus, nvidia, prime-run, supergfxctl, vaapi]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8215"
    title: "Issue #8215: 4.0.1: shell_succeeds fix enables NVDEC VAAPI routing on hybrid laptops with Intel-driven displays, corrupting browser video"
    kind: issue
    author: "SisyphusOfCorinth"
    date: "2026-08-25"
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
  - url: "https://github.com/omacom/omarchy/issues/3242"
    title: "Issue #3242: System Freezes on Hybrid Graphics Laptops (NVIDIA Optimus)"
    kind: issue
    author: "commandlinetips"
    date: "2025-11-08"
  - url: "https://github.com/omacom/omarchy/issues/5274"
    title: "Issue #5274: NVIDIA hybrid GPU: kernel crashes on lid close with s2idle default sleep"
    kind: issue
    author: "Arzamendiaariel"
    date: "2026-04-10"
  - url: "https://github.com/omacom/omarchy/issues/4891"
    title: "Issue #4891: Suspend/resume causes compositor freeze on NVIDIA hybrid GPU laptops"
    kind: issue
    author: "KrisKind75"
    date: "2026-03-03"
  - url: "https://github.com/omacom/omarchy/issues/10433"
    title: "Issue #10433: install/hardware/nvidia.sh never enables nvidia-suspend/resume/hibernate services"
    kind: issue
    author: "mudiam"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10350"
    title: "Issue #10350: Hybrid Pascal (nvidia-580xx) + Intel iGPU: Hyprland crashes when dGPU-driven external monitors are actively used"
    kind: issue
    author: "christianjgilman"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/8776"
    title: "Issue #8776: Dual-GPU AMD: PCI by-path in AQ_DRM_DEVICES silently login-loops SDDM autologin"
    kind: issue
    author: "mowgli42"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11868"
    title: "Issue #11868: force-igpu resume hook strands system in Vfio mode on Integrated->Vfio transition failure"
    kind: issue
    author: "ujo4eva"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/pull/8546"
    title: "PR #8546: Enable NVIDIA S0ix power management on s2idle systems"
    kind: pr
    author: "nhodges"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11988"
    title: "Issue #11988: contributing guide: 'omarchy debug' command does not exist (4.0.3-1)"
    kind: issue
    author: "jte369"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/hypr/nvidia.lua"
    title: "default/hypr/nvidia.lua at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-toggle-hybrid-gpu"
    title: "bin/omarchy-toggle-hybrid-gpu at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/toggles-idle-screensaver/"
    title: "Omarchy manual: Toggles, Idle and the Screensaver"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "josefdc"
    url: "https://github.com/josefdc"
    for: "Traced the Chromium cross-GPU DMA-BUF failure to GLVND EGL vendor priority and published the per-app Mesa EGL fix"
  - name: "SisyphusOfCorinth"
    url: "https://github.com/SisyphusOfCorinth"
    for: "Attributed the 4.0.1 NVDEC video regression to the shell_succeeds helper change in nvidia.lua"
  - name: "karluiz"
    url: "https://github.com/karluiz"
    for: "Showed that clearing the session-wide NVIDIA env restores full Chromium acceleration and lets the dGPU reach D3cold"
  - name: "mowgli42"
    url: "https://github.com/mowgli42"
    for: "Traced the silent SDDM login loop to Aquamarine splitting a by-path AQ_DRM_DEVICES value on every colon"
  - name: "Elshayib"
    url: "https://github.com/Elshayib"
    for: "Wrote the session-env sanitizer for by-path AQ_DRM_DEVICES values and the omarchy debug warning, PRs 8786 and 9063"
  - name: "christianjgilman"
    url: "https://github.com/christianjgilman"
    for: "Documented the i915 GPU hang on Pascal hybrids and the NVIDIA-first device order that avoids it"
faq:
  - q: "Does Omarchy set up Optimus offloading for me?"
    a: "Partly. It installs the matching NVIDIA and Mesa driver packages, Vulkan drivers and Intel VA-API packages, and it sets NVIDIA session variables in default/hypr/nvidia.lua. It does not configure per-application offload beyond what prime-run from nvidia-utils already gives you, and it does not set AQ_DRM_DEVICES."
  - q: "Why is my browser video corrupt or black after updating to 4.0.1 or later?"
    a: "On a Turing or newer NVIDIA card, nvidia.lua exports LIBVA_DRIVER_NAME=nvidia for the whole session even when the iGPU drives every display. Decode lands on the wrong card. Set LIBVA_DRIVER_NAME to iHD on Intel or radeonsi on AMD and restart the browser. Tracked in issue 8215."
  - q: "Can I just turn the discrete GPU off?"
    a: "Yes, if supergfxctl supports your laptop. Run omarchy toggle hybrid gpu, or use Super plus Ctrl plus H and pick Hybrid GPU. It installs supergfxctl, switches the mode and reboots. Battery life improves, but issue 11868 shows the resume hook can strand the machine in Vfio mode."
  - q: "Should I set AQ_DRM_DEVICES?"
    a: "Only as a last resort. Never use a /dev/dri/by-path name: Aquamarine splits the value on every colon, so a PCI path becomes garbage and the session login-loops with no error. If you set it at all, use colon-free udev symlink names rather than /dev/dri/cardN, which can change number between boots, and list both cards."
related: [nvidia, intel-gpu, amd-gpu, suspend-sleep, battery-power]
draft: false
---

Omarchy treats a hybrid laptop as an NVIDIA machine plus an integrated GPU. It installs drivers for both cards, Hyprland composites on whichever card owns your panel, and the discrete card idles until something asks for it. The friction is in the details: which card decodes video, which card the browser renders on, and whether the discrete card ever powers down. For single-vendor pages see [NVIDIA](/hardware/nvidia/), [Intel GPU](/hardware/intel-gpu/) and [AMD GPU](/hardware/amd-gpu/).

## Status on 4.0.4

Verified against the v4.0.4 source tree on 2026-09-16. The tracker holds 204 issues matching hybrid or dual GPU terms, 156 of them open.

What works on a stock install: both drivers get installed, the session starts on the integrated card, external monitors wired to either card light up, Vulkan drivers for both vendors are installed, and `prime-run` from nvidia-utils still offloads a single application to the discrete card.

What is unreliable: video decode routing in browsers, suspend and resume, and discrete GPU runtime power management. Two reporters in [#8989](https://github.com/omacom/omarchy/issues/8989) measured zero milliseconds of runtime suspension across a whole session.

The policy is older than Quattro: 3.x wrote the same NVIDIA variables into each user's config at install time, ungated, and #4901 is the March report of the result. 4.0.0 moved them into `nvidia.lua` behind a detector call that never returned true, because `os.execute` inside the Hyprland Lua config could not read an exit status, so 4.0.0 was the one release where hybrid machines were accidentally correct. The 4.0.1 fix to that helper switched the variables back on, which is why users date their video problems to 4.0.1.

## What Omarchy does automatically

`install/hardware/nvidia.sh` splits on GSP firmware. Turing and newer, meaning PCI device IDs at or above `0x1e00`, get `nvidia-open-dkms`, `nvidia-utils`, `lib32-nvidia-utils` and `libva-nvidia-driver`. Maxwell, Pascal and Volta, IDs from `0x1340` up to `0x1e00`, get the `nvidia-580xx` legacy branch. Anything older is refused with a pointer to the Arch wiki. It writes `options nvidia_drm modeset=1` to `/etc/modprobe.d/nvidia.conf` and adds the four NVIDIA modules to `/etc/mkinitcpio.conf.d/nvidia.conf` for early KMS.

`install/hardware/vulkan.sh` adds `vulkan-intel`, `vulkan-radeon` or `vulkan-asahi` for whichever integrated card `lspci` reports, so a hybrid machine gets both vendors' Vulkan drivers. `install/hardware/intel/video-acceleration.sh` adds `intel-media-driver`, `libvpl` and `vpl-gpu-rt` for HD, UHD, Xe, Iris, Arc and Panther Lake parts, and `libva-intel-driver` for GMA.

`default/hypr/nvidia.lua` sets the per-session environment. The GSP branch exports `NVD_BACKEND=direct`, `LIBVA_DRIVER_NAME=nvidia` and `__GLX_VENDOR_LIBRARY_NAME=nvidia`; the legacy branch exports `NVD_BACKEND=egl` and `__GLX_VENDOR_LIBRARY_NAME=nvidia` only. The detectors `omarchy-hw-nvidia`, `omarchy-hw-nvidia-gsp` and `omarchy-hw-nvidia-without-gsp` read cached IDs under `/sys/bus/pci/devices` instead of running `lspci`, because reading PCI config space wakes a runtime-suspended card out of D3cold, and that wake by itself takes longer than the 1.5 seconds Hyprland allows for a config reload. That landed in 4.0.0.

`omarchy-hw-hybrid-gpu` decides whether you have a hybrid setup. It asks `supergfxctl -s` with a one second timeout and looks for Hybrid in the reply; if supergfxctl is missing or wedged, it falls back to counting VGA, 3D and Display entries in `lspci`. A wedged `supergfxd` used to hang the menu, which 4.0.0 fixed.

`omarchy-toggle-hybrid-gpu` sits behind `omarchy toggle hybrid gpu` and the Hardware trigger menu (`Super + Ctrl + H`), documented in the manual chapter on [toggles and idle](https://omarchy.org/manual/toggles-idle-screensaver/). On first run it installs `supergfxctl`, writes `/etc/supergfxd.conf` with mode Hybrid and `vfio_enable`, and enables the daemon. Switching to Integrated adds a `supergfxd` drop-in that sleeps five seconds before start, because otherwise the daemon races the display manager and the machine freezes at boot. It also installs the `force-igpu` sleep hook, which bounces the card Vfio then Integrated after every resume so it powers off again, and switches to Vfio before hibernate so the driver detaches from a card it cannot freeze.

Omarchy never sets `AQ_DRM_DEVICES`. There is no reference to it in `bin/`, `default/` or `config/` at v4.0.4, and `omarchy-debug` does not collect it either.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#8215](https://github.com/omacom/omarchy/issues/8215) forced `LIBVA_DRIVER_NAME=nvidia` kills or corrupts browser video | Any iGPU plus Turing or newer NVIDIA. Confirmed on ASUS Vivobook 16, Dell Meteor Lake, HP Arrow Lake, AMD Cezanne plus RTX 3050 Ti | open | not fixed, PR #7851 open |
| [#8989](https://github.com/omacom/omarchy/issues/8989) session-wide NVIDIA env also blocks dGPU runtime suspend | iGPU-primary hybrids, both driver branches | open | not fixed |
| [#4901](https://github.com/omacom/omarchy/issues/4901) Chromium picks NVIDIA EGL, cross-GPU DMA-BUF failures | Intel plus NVIDIA, also AMD plus NVIDIA | workaround | not fixed |
| [#3242](https://github.com/omacom/omarchy/issues/3242) random full freeze from RTD3 PCI reallocation loop | Pascal Optimus laptops, Intel HD 530/630 plus GTX 1060 Mobile | workaround | not fixed |
| [#5274](https://github.com/omacom/omarchy/issues/5274) NVRM assertion storm and crash on lid close under s2idle | Hybrids in supergfxctl Hybrid mode, also dGPU-only laptops | open | not fixed, PR #8546 under test |
| [#4891](https://github.com/omacom/omarchy/issues/4891) compositor freeze on resume, stale frame, dead input | Intel or AMD plus NVIDIA, also dual-NVIDIA desktops | open | not fixed |
| [#10433](https://github.com/omacom/omarchy/issues/10433) nvidia-suspend, resume and hibernate units never enabled | all NVIDIA installs, worst on laptops | open | not fixed |
| [#10350](https://github.com/omacom/omarchy/issues/10350) i915 GPU hang and Hyprland abort when dGPU-driven externals are used | Pascal on the 580xx branch | workaround | not fixed |
| [#8776](https://github.com/omacom/omarchy/issues/8776) by-path `AQ_DRM_DEVICES` login-loops SDDM with no error | any dual-GPU machine with the variable set | open | not fixed, PRs #8786 and #9063 open |
| [#11868](https://github.com/omacom/omarchy/issues/11868) `force-igpu` strands the machine in Vfio, toggle cannot recover | Integrated mode, supergfxctl laptops | open | not fixed |
| [#12187](https://github.com/omacom/omarchy/issues/12187) hard freeze about five seconds after login on 4.0.4 | one Lenovo RTX 4070 laptop on prebuilt `nvidia-open`, not DKMS | open | not fixed |
| [#12041](https://github.com/omacom/omarchy/issues/12041) whole-screen rainbow corruption after lid resume | AMD Rembrandt iGPU plus RTX 3050 | open | not fixed |

The first three rows are one bug seen from three angles. Where the integrated card drives every display, `nvidia.lua` still exports `LIBVA_DRIVER_NAME=nvidia`, so libva loads the NVDEC driver on a card that is not compositing. Reporters measured corrupted frames, wallpaper punch-through, or `vaEndPicture failed, VA error: internal decoding error` in a loop that never completes a frame. Pointing that one variable at the integrated card's driver, `iHD` or `radeonsi`, fixed it for every reporter in the thread who tried it. The NVDEC backend also advertises zero encode entrypoints, so hardware encode is silently lost at the same time.

A related trap from #8989: `--disable-features=VaapiVideoDecoder` does not fix it. One reporter verified the flag was active in the running process, saw no change, and lost a day to network and compositor theories before finding the environment variable. Disabling the browser's decoder feature does nothing about the driver name that is still exported session-wide.

## Fixes that work

Work in this order.

**1. Find out which card owns your panel.** Check which `cardN` has the connected output under `/sys/class/drm/`. If the NVIDIA card logs `Cannot find any crtc or sizes`, it has no outputs wired and your machine is muxless. That is the common case, and it is what makes the default VA-API choice wrong here.

**2. Fix video decode routing.** Add `hl.env("LIBVA_DRIVER_NAME", "iHD")` to `~/.config/hypr/hyprland.lua`, or `radeonsi` on an AMD integrated card. To skip a relogin also run `systemctl --user set-environment LIBVA_DRIVER_NAME=iHD`, then restart the browser, since a running process keeps its old environment. This affects encode and decode only, not Vulkan, OpenGL, NVENC or `prime-run`.

**3. If Chromium still ghosts or blacks out,** force it onto Mesa EGL per application. A wrapper or desktop file setting `__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/50_mesa.json` puts Chromium on the same card as the compositor. Set that variable globally and Hyprland's own EGL init breaks, dropping you to a TTY, so keep it scoped to the browser. See [Chromium flicker and hardware acceleration](/fix/chromium-flicker-hardware-acceleration/).

**4. For suspend problems,** start with `nvidia-suspend.service`, `nvidia-resume.service` and `nvidia-hibernate.service`. Omarchy installs the driver but leaves those units disabled, and enabling them together with `NVreg_PreserveVideoMemoryAllocations=1` fixed a slow resume in #10433. The evidence is mixed further along: one #5274 reporter crashed with the units already enabled, one #4891 reporter found the sleep script exits immediately on the 610 driver branch, and another #5274 reporter froze on `deep` sleep, so `mem_sleep_default=deep` is not a guaranteed fix either. If your machine sleeps with s2idle, the option under test in PR #8546, `options nvidia NVreg_EnableS0ixPowerManagement=1` followed by `limine-mkinitcpio`, has three clean reports in that thread. See [suspend will not resume](/fix/suspend-wont-resume-s2idle/).

**5. For random full freezes on older Optimus hardware,** pin runtime power management off with `options nvidia NVreg_DynamicPowerManagement=0x00` plus a udev rule setting `power/control` to `on` for vendor `0x10de`, then rebuild the initramfs. Costs battery, stops the PCI reallocation loop.

**6. If you never use the discrete card,** turn it off. `omarchy toggle hybrid gpu` switches to Integrated and reboots. Caveat from #11868: if a resume transition fails you can land in Vfio mode, where the toggle prints `Hybrid GPU not found or in unknown mode.` and exits. The reporter recovered with `supergfxctl -m Hybrid`, removing `/usr/lib/systemd/system-sleep/force-igpu` and `/etc/systemd/system/supergfxd.service.d/delay-start.conf`, then a reboot.

**7. Leave `AQ_DRM_DEVICES` alone unless nothing else works.** Never use a `/dev/dri/by-path/pci-...` name. Aquamarine splits the value on every colon, so the PCI address falls apart, no GPU is found, and the session loops at login with nothing useful logged. Do not pin a bare `/dev/dri/cardN` either: #8776 saw the numbers rotate between reboots. Use colon-free udev symlink names and list both cards. On btrfs installs the variable lives in `~/.config/uwsm/env-hyprland` on the home subvolume, so every snapshot inherits a bad value and rolling back does not help.

**8. On 4.0.4,** if the machine freezes shortly after login, check which NVIDIA package you have. The release changed the default boot entry to `linux-omarchy`, and the #12187 reporter traced their freeze to prebuilt `nvidia-open`, which only ships modules for the stock Arch kernel. That is one report with no follow-up yet. Boot the stock kernel entry from Limine, then switch to `nvidia-open-dkms`, which is what the installer selects. See [kernel panic after update](/fix/kernel-panic-after-update-limine/) and [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

## Report it

Run `omarchy debug`. It gathers `inxi -Farz`, `dmesg`, this boot's journal warnings and errors, and the package list, then offers to upload to `logs.omarchy.org` with a 24 hour expiry or save locally. Use `omarchy debug --print --no-sudo` to read it first. If the subcommand is not registered on your install, reported on 4.0.2 and 4.0.3-1 in [#11988](https://github.com/omacom/omarchy/issues/11988), call `omarchy-debug` directly.

Add what it does not capture: which `cardN` and `renderDN` map to which PCI address, which card holds the connected outputs, `systemctl --user show-environment | grep -E 'LIBVA|GLX|NVD_BACKEND'`, whether `AQ_DRM_DEVICES` is set, and `/sys/bus/pci/devices/<dGPU>/power/runtime_status`. Copy the A/B tables in [#8215](https://github.com/omacom/omarchy/issues/8215) and [#8989](https://github.com/omacom/omarchy/issues/8989): same clip, same profile, one variable changed. If your laptop is not listed yet, send it to [hardware submissions](/hardware/submit/).

## Related

- [NVIDIA on Omarchy 4](/fix/nvidia-drivers-omarchy-4/), [hybrid GPU black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [Suspend and sleep](/hardware/suspend-sleep/), [battery and power](/hardware/battery-power/), [multi-monitor](/hardware/multi-monitor/)
- [Battery drains fast](/fix/battery-drains-fast/), [still broken on the current release](/releases/still-broken/), [v4.0.4 notes](/releases/v4.0.4/)
