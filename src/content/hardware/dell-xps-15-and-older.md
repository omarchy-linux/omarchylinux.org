---
title: "Dell XPS 15, XPS 17 and pre-2026 XPS on Omarchy"
description: "Field notes on running Omarchy 4.x on the Dell XPS 15, XPS 17 and older XPS laptops: what is known, the Goodix fingerprint dead end, MIPI webcams and NVIDIA."
answer: "Older XPS laptops install and run Omarchy 4.x, but they get almost none of the Dell-specific enablement, which targets the 2026 Panther Lake XPS. Known problems: Goodix 27c6:5395 fingerprint readers cannot enroll, MIPI webcams on the XPS 13 9315 and 9350 get no working camera stack, and a hybrid NVIDIA XPS is the reference report for the lock screen dying on resume. Nobody has confirmed the rest either way."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-17
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Dell"
model: "XPS 15 / XPS 17 / pre-2026 XPS"
dmi: ["XPS 15 7590", "XPS 15 9500", "XPS 15 9520", "XPS 15 9530", "XPS 15 9560", "XPS 15 9570", "XPS 9700", "XPS 9320", "XPS 13 9315", "XPS 13 9350", "XPS 13 9360"]
cpu: "Intel Core, Kaby Lake through Lunar Lake"
gpu: "Intel iGPU, often with an NVIDIA GTX/RTX dGPU"
year: "2017-2024"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: partial
  fingerprint: broken
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: unknown
  battery: unknown
  keyboard: unknown
quirkScripts:
  - name: "omarchy-hw-dell-xps-haptic-touchpad"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-haptic-touchpad"
    note: "Matches DMI 'XPS' plus an i2c Synaptics device. Older XPS units without that device do not match."
  - name: "install/hardware/dell-xps-touchpad-haptics.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/dell-xps-touchpad-haptics.sh"
    note: "Installs the dell-xps-touchpad-haptics package only when the predicate above is true."
  - name: "omarchy-hw-dell-xps-oled"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-oled"
    note: "Requires Intel Panther Lake, so no pre-2026 XPS can match it."
  - name: "install/hardware/intel/fix-wifi7-eht.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fix-wifi7-eht.sh"
    note: "Gated on Intel BE200/BE211 PCI IDs, which older XPS laptops do not ship."
  - name: "install/hardware/fix-synaptic-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-synaptic-touchpad.sh"
    note: "Generic: enables Synaptics InterTouch on psmouse when a Synaptics input device is present."
issueCount: 23
tags: [dell, xps, hybrid-gpu, fingerprint, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11899"
    title: "Issue #11899: `omarchy setup security fingerprint` silently evicts a working libfprint fork, then \"succeeds\" against the stale daemon"
    kind: issue
    author: "StuartRP"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9156"
    title: "Issue #9156: Shell lock client dies on resume from suspend, showing Hyprland 'screensaver died' failsafe"
    kind: issue
    author: "MartinNielsen"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/11019"
    title: "Issue #11019: External monitors on a USB-C dock never return after undocking (aquamarine 0.15.0 regression)"
    kind: issue
    author: "jacobrosenthal"
    date: "2026-09-09"
  - url: "https://github.com/hyprwm/aquamarine/releases/tag/v0.15.1"
    title: "aquamarine v0.15.1 release notes (carries PR #410, which closes upstream issue #386)"
    kind: release
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/9879"
    title: "Issue #9879: IPU6 MIPI cameras (ov01a10 / OVTI01A0) get no setup; hardware detection only covers IPU7"
    kind: issue
    author: "extragloves"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/12178"
    title: "Issue #12178: Lunar Lake: intel-ipu7-camera is installed by detection but built for Panther Lake only"
    kind: issue
    author: "pkolbas"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1868"
    title: "Issue #1868: Omarchy audio broken on dell xps 13"
    kind: issue
    author: "tjcwilk"
    date: "2025-09-22"
  - url: "https://github.com/omacom/omarchy/issues/7195"
    title: "Issue #7195: Notification toasts render on every connected monitor; the notifications plugin has no focused-monitor gate"
    kind: issue
    author: "EduardsSk"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7054"
    title: "Issue #7054: Media bar widget marquee freezes mid-scroll, showing only a few leading characters"
    kind: issue
    author: "schotime"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7019"
    title: "Issue #7019: Cannot run Migration (1786643346) because an \"browser window is open\" according to the migration."
    kind: issue
    author: "joshuafouch"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/4326"
    title: "Issue #4326: omarchy-3.3.2.iso is not bootable (Omarchy logo is frozen)"
    kind: issue
    author: "macmillen"
    date: "2026-01-20"
  - url: "https://github.com/omacom/omarchy/issues/2307"
    title: "Issue #2307: Complete System Brick after Omarchy Update"
    kind: issue
    author: "mmsbrggr"
    date: "2025-10-08"
  - url: "https://github.com/omacom/omarchy/issues/903"
    title: "Issue #903: System Freezes After Waking from Sleep Mode with Previous Session Prompt on Omarchy"
    kind: issue
    author: "OerdBej"
    date: "2025-08-18"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-haptic-touchpad"
    title: "omarchy-hw-dell-xps-haptic-touchpad at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/audio/tunings/dell-xps-2026/tuning.conf"
    title: "Speaker tuning for Dell XPS 14/16 (2026) at v4.0.4"
    kind: commit
    date: "2026-09-15"
credits:
  - name: "StuartRP"
    url: "https://github.com/StuartRP"
    for: "Traced why the fingerprint setup command destroys a working Goodix 27c6:5395 driver on the XPS 15 7590"
  - name: "jacobrosenthal"
    url: "https://github.com/jacobrosenthal"
    for: "Isolated the undock regression to aquamarine 0.15.0 rather than the kernel"
  - name: "MartinNielsen"
    url: "https://github.com/MartinNielsen"
    for: "Journal evidence for the lock client dying on resume on a hybrid NVIDIA XPS"
faq:
  - q: "Does Omarchy have hardware support for the XPS 15 or XPS 17?"
    a: "Not specifically. The Dell enablement in the repo targets the 2026 Panther Lake XPS 13/14/16. The only Dell-specific predicate that can match an older XPS is the haptic touchpad check, and it also requires a Synaptics i2c device most older XPS units do not have."
  - q: "Will the fingerprint reader work on an XPS 15 7590?"
    a: "No, not with the packages Omarchy installs. The Goodix 27c6:5395 reader has no driver in the pinned libfprint, and running the Omarchy fingerprint setup will remove a community fork if you installed one. See issue #11899."
  - q: "Should I buy an old XPS 15 to run Omarchy?"
    a: "Only if the price is right. It will run, but you get no model-specific tuning, and a hybrid NVIDIA model adds suspend and lock-screen risk. A used ThinkPad or a 2026 XPS is a calmer choice."
related: [dell-xps-14-2026, dell-xps-13-2026, hybrid-gpu, fingerprint, suspend-sleep, webcam]
draft: false
---

## Verdict

Bronze. An XPS 15, XPS 17 or older XPS 13 installs Omarchy 4.x and runs it as a normal Intel Arch laptop. What it does not get is any of the Dell work Omarchy has done over the past year, which is aimed squarely at the 2026 Panther Lake XPS line. Bronze rather than silver because not one subsystem on these machines has a report confirming it works; the table below is a mix of "broken" and "nobody has said".

Three things are concretely broken rather than merely unsupported. Goodix `27c6:5395` fingerprint readers cannot enroll, and the Omarchy fingerprint setup actively removes the community driver that does work. The MIPI webcams in the XPS 13 9315 (IPU6) and XPS 13 9350 (Lunar Lake IPU7) get no usable camera stack from hardware detection. And the reference report for the shell's lock client dying on resume from suspend comes from a hybrid Intel plus NVIDIA XPS 9570, although the same bug has since been reproduced on AMD and ASUS machines, so it is not an XPS quirk. Most of what else sits in the issue tracker for these machines is generic Omarchy software, not XPS hardware.

Evidence here is thinner than for the current XPS models. The tracker holds about two dozen issues that name an XPS 15, XPS 17 or a pre-2026 XPS product code, and only a handful of those are hardware. Treat the "unknown" entries in the subsystem table as genuinely unknown, not as quiet approval.

## What works

Reports come in from XPS 15 7590, 9500, 9520, 9530, 9560 and 9570, from an XPS 9700, an XPS 9320 and the XPS 13 9315, 9350 and 9360, all of them running Omarchy and mostly filing bugs about the desktop rather than about the machine. Issue [#7195](https://github.com/omacom/omarchy/issues/7195) is filed from an XPS 15 9520 driving four outputs, one internal plus three DisplayPort, which is a reasonable signal that display output and docking basically function.

Installation has two closed reports and no open ones. [#4326](https://github.com/omacom/omarchy/issues/4326) is an XPS 9520 where the 3.3.2 ISO froze at the splash screen while 3.2.3 booted; it was closed in the July 2026 issue sweep without a stated root cause. A Ventoy boot problem on an XPS 13 9360 was resolved in v3.0.2. Nothing has been filed against the 4.x ISO from any of these machines.

Wi-Fi, Bluetooth, the keyboard, battery and the touchpad produce no XPS-specific bug reports across 3.x or 4.x. That is weak positive evidence. It means nobody has complained, not that anyone verified it. An earlier hand-written prototype of this site claimed Wi-Fi, audio, webcam, GPU and suspend all worked on a 7590 and that only fingerprint failed. That claim is unverified, so it is not reflected in the subsystem table above.

## What breaks

**Fingerprint, on Goodix `27c6:5395`.** Issue [#11899](https://github.com/omacom/omarchy/issues/11899) is an XPS 15 7590 report and it is the sharpest finding on this page. The reader has no driver in the `libfprint-git` snapshot Omarchy pins. A community AUR fork adds one and works. Running `omarchy setup security fingerprint` checks for the literal package name `libfprint-git` via `omarchy-pkg-missing`, decides it is missing, and replaces the fork in one unattended pacman transaction. Because `fprintd` is still running with the fork's library mapped in memory, enrollment then succeeds and the script prints a success message. The next time `fprintd` restarts, `fprintd-list` reports no devices, permanently and silently. Open as of 4.0.4. Do not run the fingerprint setup on one of these machines if you have a working fork installed.

**Webcam, on the MIPI-camera XPS 13 models.** Two open issues cover the pre-2026 XPS 13. [#9879](https://github.com/omacom/omarchy/issues/9879) points out that `install/hardware/intel/ipu7-camera.sh` only acts on IPU7 hardware, so IPU6 laptops, the XPS 13 Plus 9315 named among them, get raw Bayer `/dev/video*` nodes and no userspace to use them. [#12178](https://github.com/omacom/omarchy/issues/12178) is filed from a Dell Pro 14 Premium, not an XPS, but by its own analysis it applies to every Lunar Lake IPU7 laptop including the XPS 13 9350: `intel-ipu7-camera` is installed by detection but built for Panther Lake only, so the `ipu7x` HAL plugin a Lunar Lake IPU asks for does not exist. XPS 15 and 17 units use ordinary USB webcams and have no reports either way.

**Speakers, one unresolved report.** [#1868](https://github.com/omacom/omarchy/issues/1868) is an XPS 13 9315 (Alder Lake, SOF audio) from September 2025 where the speakers showed "no route selected" while AirPlay output worked. It was closed a month later with only generic PipeWire debugging advice and no confirmed fix. That is the only audio report from any pre-2026 XPS; the XPS 15 and 17 have none.

**Suspend and the lock screen on hybrid NVIDIA models.** Issue [#9156](https://github.com/omacom/omarchy/issues/9156) was filed from a "Dell XPS 9570 class" Optimus laptop with an HD 630 and a GTX 1050 Mobile: the shell's session-lock client hits a fatal Wayland error while Hyprland is still rebuilding outputs after resume, and you land on Hyprland's crashed-screensaver failsafe. The shell relaunches and re-locks, so you re-authenticate rather than lose the session. Intermittent, open as of 4.0.4, and later comments reproduce it on an AMD desktop and an ASUS Zephyrus, so treat it as a shell bug the XPS happens to hit. The older [#903](https://github.com/omacom/omarchy/issues/903) from an XPS 15 9570 in 2025 looked like a freeze on wake but turned out to be GNOME installed alongside Omarchy fighting over the session; it says nothing about the hardware.

**Undocking, on Raptor Lake i915 units.** Issue [#11019](https://github.com/omacom/omarchy/issues/11019) is verified on an XPS 9320 on Omarchy 4.0.3. Unplugging a USB-C dock kills the external displays until reboot. The reporter traced it to aquamarine 0.15.0, not the kernel. Starting up with the dock already attached works, and so does plugging in after a clean boot; only the unplug path is broken. Upstream closed the aquamarine bug on 2026-09-15 with a different patch than the one the reporter tested, and it ships in [aquamarine 0.15.1](https://github.com/hyprwm/aquamarine/releases/tag/v0.15.1), released 2026-09-17. The Omarchy issue is still open; check `pacman -Q aquamarine` to see whether your install has picked up 0.15.1 yet.

**Black screen after the 3.1 update.** [#2307](https://github.com/omacom/omarchy/issues/2307) is a 2025 report from an XPS 15 9500 where an update left the screen flickering between black and grey after the LUKS prompt. The reporter got back in through a Limine snapshot and guessed at the kernel; the thread's actual fix was stale Hyprland plugins, cleared with `hyprpm purge-cache` and `hyprpm update`. Closed, and not XPS-specific, but it is a good reason to keep the snapshot rollback path in mind on these machines.

Two open bugs get reported from XPS 15 hardware but are not hardware bugs: [#7195](https://github.com/omacom/omarchy/issues/7195) duplicates every notification toast onto every monitor, and [#7054](https://github.com/omacom/omarchy/issues/7054) freezes the media widget's scrolling label. [#7019](https://github.com/omacom/omarchy/issues/7019) is a stuck migration reported from a 9530. All three affect every machine equally.

## What Omarchy does for this model

Very little, and it is worth knowing exactly how little before you expect otherwise.

Omarchy matches hardware through `bin/omarchy-hw-match`, which greps `/sys/class/dmi/id/product_name` and `product_family` case-insensitively. Three XPS-related predicates exist at v4.0.4:

- `omarchy-hw-dell-xps-haptic-touchpad` requires DMI `XPS` **and** `/sys/bus/i2c/devices/i2c-VEN_06CB:00`. On a match, `install/hardware/dell-xps-touchpad-haptics.sh` installs the `dell-xps-touchpad-haptics` package. Older XPS laptops without that i2c Synaptics haptic device get nothing.
- `omarchy-hw-dell-xps-oled` requires DMI `XPS`, an Intel Panther Lake GPU, and a specific LG panel EDID. No pre-2026 XPS can satisfy the Panther Lake half.
- The 2026 speaker tuning in `default/audio/tunings/dell-xps-2026/` is matched on the exact DMI SKUs `0DB9` and `0DBA`, the XPS 14 and XPS 16. The tuning file states outright that whole-value matching is used so it "cannot widen to the rest of the XPS line".

The Intel Wi-Fi 7 workaround in `install/hardware/intel/fix-wifi7-eht.sh` is gated on BE200/BE211 PCI IDs and does not apply. `install/hardware/fix-synaptic-touchpad.sh` is generic and may enable Synaptics InterTouch if your touchpad shows up as Synaptics. NVIDIA handling is generic too: `install/hardware/nvidia.sh` splits by GPU generation, so Pascal parts such as the GTX 1050 Mobile in a 9560 get the legacy `nvidia-580xx-dkms` branch, while Turing and newer parts such as the GTX 1650 Mobile in a 7590 get `nvidia-open-dkms`.

Release notes back this up. From v3.5.0 through v4.0.4, the XPS line items are about Panther Lake and the 2026 machines: Wi-Fi 7, the haptic trackpad, the OLED panel, the XPS 13 DX13260 text scaling, the XPS 14/16 speaker tuning, and v4.0.4's webcam fix, which addresses the IPU7 camera on Panther Lake XPS units after the 7.2 kernel regression in [#10948](https://github.com/omacom/omarchy/issues/10948). The items that are not model-locked are small: v3.5.1 broadened haptic touchpad detection to any Synaptics product "for broader Dell XPS compatibility", and the v3.5.1 XPS mic-mute key support was folded into the generic `omarchy-audio-input-mute` in v3.7.0. Neither changes anything on a machine without the haptic touchpad or the mic-mute LED.

## Variants

Prefer the Intel-graphics-only configurations. The XPS 15 and 17 with a discrete GTX or RTX chip put you on the hybrid GPU path, which is where the resume and lock-screen reports come from. If you have the dGPU, read [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) and [/hardware/nvidia/](/hardware/nvidia/) before installing.

Avoid buying one specifically for the fingerprint reader. The 7590 generation ships Goodix parts that the pinned libfprint cannot drive.

Pre-2026 XPS 13 units belong on this page, and they carry the webcam caveat above: the 9315 is IPU6 and the 9350 is Lunar Lake IPU7, and neither gets a working camera stack from Omarchy's hardware detection as of 4.0.4. The 2026 Wildcat Lake XPS 13 is a different machine and has its own page at [/hardware/dell-xps-13-2026/](/hardware/dell-xps-13-2026/).

## Before you install

- Update the BIOS from Windows or a Dell boot stick first. It is general good practice, and the v3.6.0 release notes are a reminder of why: an XPS resume workaround was removed because the real fix turned out to be a BIOS update, on the 2026 model in that case.
- Decide about the dGPU before you start, not after. Check `lspci | grep -i nvidia`.
- Keep the snapshot rollback path in your head. See [/upgrade/rollback-with-snapper-and-limine/](/upgrade/rollback-with-snapper-and-limine/).
- If you already run a libfprint fork for a Goodix reader, do not run _Setup > Security > Fingerprint_. Read [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/) first.
- On an XPS 13 9315 or 9350, expect the webcam to need manual work. See [/fix/webcam-not-detected/](/fix/webcam-not-detected/) and [/hardware/webcam/](/hardware/webcam/).
- Test undock behaviour before you rely on a dock. See [/hardware/thunderbolt-dock/](/hardware/thunderbolt-dock/).
- The manual chapter on fingerprint and other hardware auth is at [omarchy.org/manual/hardware-authentication/](https://omarchy.org/manual/hardware-authentication/).

If you run one of these machines, the tracker would benefit from a plain confirmation that Wi-Fi, audio and the webcam do work, because right now nobody has written that down. You can add a report through [/hardware/submit/](/hardware/submit/).

## Related

- [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) and [/hardware/nvidia/](/hardware/nvidia/)
- [/hardware/fingerprint/](/hardware/fingerprint/) and [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/)
- [/hardware/webcam/](/hardware/webcam/) and [/fix/webcam-not-detected/](/fix/webcam-not-detected/)
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/dell-xps-14-2026/](/hardware/dell-xps-14-2026/) and [/hardware/dell-xps-13-2026/](/hardware/dell-xps-13-2026/)
- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/)
