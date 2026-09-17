---
title: "MSI laptops on Omarchy"
description: "MSI Titan, Stealth, Raider, Katana, Bravo and GL series on Omarchy 4.0.4: bronze. No MSI enablement ships, so fans, EC and hybrid GPU are all manual."
answer: "Bronze. MSI laptops install and run, but Omarchy 4.0.4 ships zero MSI-specific enablement: no DMI detector, no install script, no EC or fan driver. You get the generic NVIDIA and hybrid GPU path and nothing else, so fan and embedded controller control is manual and hybrid GPU crashes on external monitors are still open. A community PR adding MSI support is open, not merged."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: partial
kind: model
vendor: "MSI"
model: "MSI gaming and creator laptops (Titan, Stealth, Raider, Vector, Katana, Bravo, Prestige, GL series)"
dmi: ["Micro-Star International Co., Ltd.", "Titan GT77HX 13VI", "GT77HX", "GL63"]
year: "2016 to 2026"
cpu: "Intel Core i7-6700HQ through Core i9-13980HX, plus AMD Ryzen on the Bravo line"
gpu: "Hybrid Optimus in almost every case: Intel HD/UHD iGPU driving the panel plus NVIDIA GTX 1060 Mobile to RTX 4090 Laptop"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: partial
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "install/hardware/all.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh"
    note: "The full hardware enablement list on v4.0.4. It names Asus, Framework, Dell XPS, Surface, Apple, Lenovo and Tuxedo. There is no MSI line."
  - name: "install/hardware/nvidia.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    note: "The main thing an MSI laptop actually gets. Installs nvidia-open-dkms on Turing and newer, nvidia-580xx-dkms on older Pascal and Maxwell, sets nvidia_drm modeset=1 and adds the NVIDIA modules to mkinitcpio."
  - name: "bin/omarchy-hw-nvidia-gsp"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-nvidia-gsp"
    note: "Decides open driver versus the 580xx branch. The GTX 1060 Mobile in an older MSI falls on the legacy side."
  - name: "bin/omarchy-hw-hybrid-gpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-hybrid-gpu"
    note: "Counts VGA/3D/Display PCI entries or asks supergfxctl. Returns true on essentially every MSI gaming laptop, which is what exposes the toggle below."
  - name: "bin/omarchy-toggle-hybrid-gpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-toggle-hybrid-gpu"
    note: "Flips Integrated and Hybrid through supergfxctl. It has no Vfio case, which is how MSI owners get stranded (issue #11808)."
  - name: "default/systemd/system-sleep/force-igpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/systemd/system-sleep/force-igpu"
    note: "Uses Vfio as a transient to detach nvidia across sleep. If its confirm poll times out, supergfxd persists Vfio and the restore never runs."
  - name: "bin/omarchy-hw-match"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    note: "The DMI product_name and product_family matcher every model quirk uses. No caller in the v4.0.4 tree passes an MSI or Micro-Star pattern."
issueCount: 30
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [msi, titan-gt77hx, nvidia, hybrid-gpu, gaming-laptop, thermals]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11583"
    title: "Issue #11583: MSI Titan GT77HX: driver packaging and Cooler Boost at 85C"
    kind: issue
    author: "andyholst"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/pull/12003"
    title: "PR #12003: Add MSI Titan GT77HX driver wiring and Cooler Boost after 30s sustained 85C"
    kind: pr
    author: "andyholst"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11532"
    title: "Issue #11532: MSI Titan GT77HX: Missing laptop-specific driver optimizations (RGB removed)"
    kind: issue
    author: "andyholst"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11573"
    title: "Issue #11573: MSI Titan GT77HX: RGB keyboard control not supported by msi-perkeyrgb"
    kind: issue
    author: "andyholst"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11808"
    title: "Issue #11808: omarchy-toggle-hybrid-gpu has no Vfio case: a failed force-igpu restore strands the machine in Vfio with no supported way back"
    kind: issue
    author: "dreamsgarage"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/10350"
    title: "Issue #10350: Hybrid Pascal (nvidia-580xx) + Intel iGPU: Hyprland crashes when dGPU-driven external monitors are actively used"
    kind: issue
    author: "christianjgilman"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/3487"
    title: "Issue #3487: Advisory: install to NVMe *with* SSD causes issues on older MSI laptop"
    kind: issue
    author: "houstonhaynes"
    date: "2025-11-21"
  - url: "https://github.com/omacom/omarchy/issues/2787"
    title: "Issue #2787: hyprland doesn't detect all display modes of builtin monitor"
    kind: issue
    author: "rmusaev99"
    date: "2025-10-24"
  - url: "https://github.com/omacom/omarchy/issues/12045"
    title: "Issue #12045: Secure Boot UKI chainload panics on MSI firmware (LoadImage failure 0x800000000000000f); ENABLE_UKI=no workaround"
    kind: issue
    author: "fenfenau"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh"
    title: "install/hardware/all.sh on v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
credits:
  - name: "andyholst"
    url: "https://github.com/andyholst"
    for: "Mapped the whole MSI gap on a Titan GT77HX 13VI and wrote the open enablement PR"
  - name: "christianjgilman"
    url: "https://github.com/christianjgilman"
    for: "Traced the i915 rcs0 hang on a hybrid MSI Optimus laptop to render device ordering"
  - name: "dreamsgarage"
    url: "https://github.com/dreamsgarage"
    for: "Found the Vfio dead end in omarchy-toggle-hybrid-gpu on an MSI RTX 2070 laptop"
  - name: "houstonhaynes"
    url: "https://github.com/houstonhaynes"
    for: "Advisory on installing to NVMe with a second SSD present on a GL63"
faq:
  - q: "Does Omarchy have an MSI hardware profile?"
    a: "No. On 4.0.4 there is no omarchy-hw-msi detector and no install/hardware/msi.sh. PR #12003 adds both but is still open as of 2026-09-16."
  - q: "Will Cooler Boost work out of the box?"
    a: "No. The EC sysfs interface needs msi-ec-dkms-git, which Omarchy does not install. Without it the silent and auto fan curves leave the machine throttling past 85C."
  - q: "Is per-key RGB supported?"
    a: "Not on the Titan GT77HX. msi-perkeyrgb does not cover it, and RGB was dropped from the enablement PR (issues #11572 and #11573)."
  - q: "Should I buy an MSI laptop for Omarchy?"
    a: "Only if you are comfortable doing your own driver work. A Framework 16, an Asus ROG or a Dell XPS gets real enablement code in the v4.0.4 tree. MSI gets none."
related: [hybrid-gpu, nvidia, intel-gpu, suspend-sleep, lenovo-legion, asus-rog-zephyrus]
draft: false
---

## Verdict

Bronze. MSI laptops boot and run Omarchy, but you are on your own for everything that makes an MSI an MSI.

Omarchy 4.0.4 ships hardware enablement for Asus, Framework, Dell XPS, Microsoft Surface, Apple, Lenovo and Tuxedo. Read [install/hardware/all.sh](https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh) on the v4.0.4 tag and you will not find a single MSI line. There is no `omarchy-hw-msi` detector, no `install/hardware/msi.sh`, and no caller anywhere in `bin/` that passes an MSI or Micro-Star pattern to `omarchy-hw-match`. We grepped the v4.0.4 tree for `msi-ec`, `r8125`, `coolercontrol` and `nct6687` and got nothing.

That means the embedded controller, the fan curves, the Killer Ethernet chip and the per-key keyboard backlight are all unmanaged. What you get is the generic NVIDIA and hybrid GPU path, which is the same path every other NVIDIA laptop gets, with the same problems.

One person has done real work here. Andy Holst filed [issue #11583](https://github.com/omacom/omarchy/issues/11583) against a Titan GT77HX 13VI and opened [PR #12003](https://github.com/omacom/omarchy/pull/12003) with a detector, an install script and a Cooler Boost watcher. As of 2026-09-16 that PR is open and unmerged. Nothing in it is in a release yet.

## What works

Be honest about the evidence here: the Omarchy tracker only proves what breaks. Almost no one files an issue to say their webcam is fine.

What we can point at:

- Installation. The GL63 owner in [issue #3487](https://github.com/omacom/omarchy/issues/3487) says the distro is a keeper once the drive layout is sorted, and multiple MSI owners are clearly running it day to day.
- NVIDIA driver selection. `install/hardware/nvidia.sh` picks `nvidia-open-dkms` on Turing and newer and `nvidia-580xx-dkms` on Pascal and Maxwell, so a GTX 1060 Mobile and an RTX 4090 Laptop both land on a branch that installs.
- On one machine, a Titan GT77HX 13VI, Andy Holst's post-reboot driver table in [issue #11532](https://github.com/omacom/omarchy/issues/11532) shows `iwlwifi` and `nvidia-open-dkms` both loaded. Read it carefully before you lean on it: that machine is running PR #12003's patch, not stock 4.0.4, and the table covers driver load state, not whether audio, the webcam or the touchpad actually work. One report, one model, one patched tree. That is why the subsystem table above says unknown rather than works.

## What breaks

**Thermal throttling under sustained load.** This is the best documented MSI problem, though the evidence is a single Titan GT77HX. Cooler Boost is an all-or-nothing embedded controller switch for maximum fan duty, and neither the silent nor the auto firmware curve ever throws it, even past 85C. CoolerControl is no help either: it can read these fans but not drive them, because they take RPM targets and not PWM. Issue #11583 reports the machine throttling during rendering, gaming and compiles. There is no fix in 4.0.4.

**Hybrid GPU crashes on external monitors.** [Issue #10350](https://github.com/omacom/omarchy/issues/10350) is an MSI Optimus laptop, i7-6700HQ with a GTX 1060 Mobile, on 4.0.2. On the internal panel alone it ran for hours without a crash. Move a window onto a dGPU-driven external and Hyprland aborts with an `i915 rcs0` GPU hang and an identical error code every time. The reporter's fix was to put the NVIDIA node first in `AQ_DRM_DEVICES`. Open on 4.0.4. See [the hybrid GPU black screen fix](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/).

**Getting stranded in Vfio mode.** [Issue #11808](https://github.com/omacom/omarchy/issues/11808) is an MSI laptop with UHD 630 plus an RTX 2070 Mobile on 4.0.3. The `force-igpu` sleep hook uses Vfio as a transient, `supergfxd` persists it, and the script runs under `set -e`, so a timed-out mode switch leaves the saved mode at Vfio. `omarchy-toggle-hybrid-gpu` only has cases for Integrated and Hybrid, so there is no supported way back. Open.

**Per-key RGB.** `msi-perkeyrgb` does not support the Titan GT77HX. Issues [#11572](https://github.com/omacom/omarchy/issues/11572) and [#11573](https://github.com/omacom/omarchy/issues/11573) were closed to consolidate the work, and RGB was explicitly dropped from PR #12003's scope. Do not expect it.

**Panel refresh rates.** [Issue #2787](https://github.com/omacom/omarchy/issues/2787) reports a 1440p 240 Hz MSI panel showing only a 60 Hz mode under Hyprland. A collaborator closed it as an upstream Hyprland bug rather than an Omarchy one. That was 3.x era, and we have no 4.x retest. Check your panel before you commit.

**Install with two drives.** On a GL63 with both an SSD and an NVMe, the first boot timed out into the emergency prompt. The reporter traced it to a `cryptdevice=PARTUUID=` in the cmdline that did not match the drive he had installed to. He pulled the SSD, reinstalled to the NVMe alone, then reattached the SSD. That was 3.x, in November 2025, and it was closed the same day it was filed. Nothing in the tree obviously changed, so treat it as unretested rather than fixed. See [install fails or stalls](/fix/install-fails-or-stalls/) and [storage and NVMe](/hardware/storage-nvme/).

**Secure Boot on MSI firmware.** [Issue #12045](https://github.com/omacom/omarchy/issues/12045) is an MSI desktop board, not a laptop, but the mechanism is firmware-level and worth knowing: Limine's UKI chainload hits `EFI_ACCESS_DENIED` from `LoadImage()` with Secure Boot on, and switching to Limine's native `protocol: linux` clears it. If your MSI laptop shares that AMI firmware behaviour, this is the shape of the failure. See [Secure Boot violation or won't boot UEFI](/fix/secure-boot-violation-or-wont-boot-uefi/).

## What Omarchy does for this model

Nothing model-specific. That is the whole answer.

An MSI laptop hits the generic paths during install: `nvidia.sh` for the driver, `vulkan.sh`, the Intel scripts for video acceleration, `lpmd`, `thermald` and SOF firmware if the CPU is Intel, `network.sh`, `bluetooth.sh` and `speaker-tuning.sh`. `omarchy-hw-hybrid-gpu` will return true, so the hybrid GPU toggle appears in the menu with the Vfio bug above.

If PR #12003 lands, MSI owners would get `bin/omarchy-hw-msi` matching the Micro-Star vendor string plus fourteen laptop family names, and an `install/hardware/msi.sh` that installs `msi-ec-dkms-git`, `r8125-dkms` and CoolerControl and sets battery thresholds at 60 and 80 percent. The `omarchy-msi-cooler-boost-watch` systemd unit, which flips Cooler Boost after 30 seconds sustained at or above 85C and drops it again at 70C, is gated on the Titan GT77HX alone. Every other MSI family in that PR gets driver packaging only. None of it is shipping today. Watch the PR rather than the release notes.

## Variants

Prefer: anything Turing or newer, so you land on `nvidia-open-dkms` instead of the 580xx legacy branch. The Titan GT77HX is the single best-documented MSI on this tracker, purely because one owner did the work.

Be careful with: older Optimus units on Pascal and Maxwell. The GTX 1060 Mobile in #10350 sits on the legacy 580xx branch, which is where the external-monitor hang lives.

Out of scope here: MSI desktop boards. The MSI bucket in our issue data holds 30 issues, and a good share of them are MAG, MPG, X370 and X570 motherboards, not laptops. If you are chasing an ALC892 headphone jack or a Nuvoton NCT6687 fan sensor, that is a desktop problem with a different shape.

## Before you install

- Plan on doing the EC and fan work yourself. Read PR #12003's description as a recipe even if it never merges.
- If you have both an SSD and an NVMe, install with only the target drive attached, then add the second one back.
- Note your panel's native refresh rate now, so you know whether Hyprland is short-changing you later. The [monitors chapter](https://omarchy.org/manual/monitors/) covers `monitors.lua`.
- If you use external monitors on the dGPU, expect to set `AQ_DRM_DEVICES` with the NVIDIA node first. List both cards, not just the NVIDIA one, or the other GPU's outputs go dark.
- Leave Secure Boot off unless you have a reason. Omarchy's own docs recommend that anyway.
- Do not rely on the hybrid GPU toggle before a hibernate. Read the [system sleep chapter](https://omarchy.org/manual/system-sleep/) and check `supergfxctl -g` afterwards.
- Own an MSI that works better or worse than this? [Send us the details](/hardware/submit/).

## Related

- [Hybrid GPU laptops](/hardware/hybrid-gpu/) and [NVIDIA on Omarchy](/hardware/nvidia/)
- [Suspend and sleep](/hardware/suspend-sleep/)
- [Lenovo Legion](/hardware/lenovo-legion/) and [Asus ROG Zephyrus](/hardware/asus-rog-zephyrus/), the two closest comparison points
- [Still broken on the latest release](/releases/still-broken/)
