---
title: "HP EliteBook, Spectre, Envy and Omen on Omarchy Linux"
description: "HP EliteBook, Spectre x360, Envy and Omen support on Omarchy 4.x: no HP-specific enablement, broken webcams on Meteor Lake, flaky s2idle resume."
answer: "Bronze. HP laptops install and run, but Omarchy ships zero HP-specific enablement, so you get the generic kernel path. Confirmed open problems on 4.0.4: intermittent s2idle resume failure on the EliteBook 845 G10, a black webcam on Meteor Lake Spectre x360 caused by Omarchy's own IPU7 script, a dark panel after lid-open, and Validity fingerprint readers libfprint cannot drive."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [hp, elitebook, spectre, envy, omen, laptop]
kind: model
vendor: "HP"
model: "HP EliteBook / Spectre / Envy / Omen"
dmi:
  - "HP EliteBook 845 14 inch G10 Notebook PC"
  - "HP EliteBook 835 G8"
  - "HP EliteBook 8470w"
  - "HP Spectre x360 2-in-1 Laptop 14-ef1xxx"
  - "HP Spectre x360 Convertible 13-aw0xxx"
  - "HP ENVY x360 m 15m-bq121dx"
  - "Victus by HP Gaming Laptop 15-fa2xxx"
cpu: "AMD Ryzen 5/7 PRO 7000 series on recent EliteBooks; Intel Core Ultra (Meteor Lake), 12th/13th Gen and older on Spectre, Envy and Omen"
gpu: "AMD Radeon 740M / Vega integrated, Intel Iris Xe and UHD, NVIDIA RTX on Omen and Victus"
year: "2012 to 2026 in the reports collected"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: partial
  fingerprint: partial
  gpu: works
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "install/hardware/intel/ipu7-camera.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    note: "Installs intel-ipu7-camera on any machine exposing ACPI HID OVTI08F4. Fires on Meteor Lake Spectre x360 and breaks the webcam there."
  - name: "install/hardware/intel/sof-firmware.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/sof-firmware.sh"
    note: "Generic Intel path. Installs sof-firmware when an Intel audio DSP is present, which covers Intel Spectre and Envy models."
  - name: "bin/omarchy-hw-fingerprint"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-fingerprint"
    note: "Vendor-ID heuristic that returns true for Validity readers (138a) whether or not libfprint has a driver for them."
issueCount: 11
sources:
  - url: "https://github.com/omacom/omarchy/issues/11332"
    title: "Issue #11332: Intermittent s2idle resume failure on HP EliteBook 845 G10, more frequent with Linux 7.2.3"
    kind: issue
    author: "mrelph"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/10892"
    title: "Issue #10892: `omarchy setup security fingerprint` fails at enroll on readers libfprint can't drive (Validity VFS491, 138a:003d)"
    kind: issue
    author: "NianticBooks"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/7697"
    title: "Issue #7697: ipu7-camera.sh misdetects Meteor Lake (IPU6) hardware as IPU7, breaking the webcam"
    kind: issue
    author: "mhbnielsen"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/pull/7773"
    title: "PR #7773: Gate the IPU7 camera stack on the controller, not the sensor"
    kind: pr
    author: "omarchybot"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/10170"
    title: "Issue #10170: Laptop with no external monitor has no path from lid-open to dpms enable: panel stays dark after resume"
    kind: issue
    author: "EitanSchuler"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/11611"
    title: "Issue #11611: Top-bar audio widget shows permanently 'muted' with no way to unmute when the sink is unresponsive"
    kind: issue
    author: "Hubert342"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/8747"
    title: "Issue #8747: Lock screen fingerprint auth hangs ~25-30s if fprintd restarts while locked"
    kind: issue
    author: "9500"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/4529"
    title: "Issue #4529: Built-in webcam not detected on Arch / Omarchy (/dev/video* missing)"
    kind: issue
    author: "yassinekrika"
    date: "2026-02-06"
  - url: "https://github.com/omacom/omarchy/issues/5127"
    title: "Issue #5127: XF86 mic audio mute is not working"
    kind: issue
    author: "novalkun"
    date: "2026-03-27"
  - url: "https://github.com/omacom/omarchy/issues/4570"
    title: "Issue #4570: Mute button doesn't work after update"
    kind: issue
    author: "strudelPi"
    date: "2026-02-10"
  - url: "https://github.com/omacom/omarchy/issues/3829"
    title: "Issue #3829: ACPI and AMD fTPM memory sections overlap on HP ENVY x360 m (Model 15m-bq121dx), causing hang at boot"
    kind: issue
    author: "sonicbhoc"
    date: "2025-12-09"
  - url: "https://github.com/omacom/omarchy/issues/4987"
    title: "Issue #4987: Add built-in RGB keyboard color control for HP Victus / Omen (stock hp-wmi)"
    kind: issue
    author: "hassandevelops"
    date: "2026-03-12"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy Manual: System sleep"
    kind: manual
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy Manual: Hardware authentication"
    kind: manual
credits:
  - name: "mrelph"
    url: "https://github.com/mrelph"
    for: "Counted suspend entries against suspend exits across two kernels to show the EliteBook 845 G10 resume failure got worse on Linux 7.2.3"
  - name: "mhbnielsen"
    url: "https://github.com/mhbnielsen"
    for: "Found that Omarchy's IPU7 camera script installs the wrong HAL on Meteor Lake Spectre x360 and produces a black frame"
  - name: "EitanSchuler"
    url: "https://github.com/EitanSchuler"
    for: "Traced the dark-panel-after-lid-open path through the shell's lock service on a Spectre x360 14-ef1xxx"
  - name: "NianticBooks"
    url: "https://github.com/NianticBooks"
    for: "Showed the fingerprint setup passes its hardware gate on a Validity VFS491 that libfprint cannot drive"
  - name: "sonicbhoc"
    url: "https://github.com/sonicbhoc"
    for: "Identified the ACPI and fTPM overlap that adds 90 seconds to boot on an Envy x360 15m-bq121dx"
faq:
  - q: "Does the webcam work on an HP Spectre x360?"
    a: "Not on the Meteor Lake models, as of 4.0.4. Omarchy's install/hardware/intel/ipu7-camera.sh keys off the ov08x40 sensor's ACPI HID alone, so it installs the IPU7 camera stack on an IPU6 machine. The camera then appears in every app as a black frame. Remove the package with omarchy-pkg-drop intel-ipu7-camera."
  - q: "Is the fingerprint reader usable on an HP EliteBook?"
    a: "It depends on the sensor. Omarchy detects Validity readers by vendor ID 138a, but libfprint has no driver for the VFS491 found on an 8470w, so enroll fails with NoSuchDevice after the packages are already installed. Check your sensor's USB ID against libfprint's supported list before you rely on it."
  - q: "Why does my HP laptop sometimes not wake from sleep?"
    a: "On the AMD EliteBook 845 G10 this is an open s2idle problem, tracked in issue #11332. The reporter measured about 6 percent of suspends failing on Linux 7.1.9 and about 31 percent on 7.2.3. The machine offers only s2idle, so there is no S3 to fall back to."
related: [suspend-wont-resume-s2idle, webcam-not-detected, fingerprint-enrollment-fails, black-screen-after-login]
draft: false
---

## Verdict

Bronze. These machines install and run, but nothing in Omarchy is written for them, and several of the problems people hit are real and still open on 4.0.4.

There is no HP entry anywhere in the hardware enablement tree. Grepping `install/hardware/`, `bin/` and `migrations/` in the v4.0.4 snapshot for EliteBook, Spectre, Envy, Omen, Victus or `hp_wmi` returns nothing. Compare that with ASUS, Framework, Dell XPS, Surface, Apple and Lenovo Yoga, which all have named scripts. On an HP you get the generic path: the Intel or AMD kernel drivers, `network.sh`, `fix-fkeys.sh`, `bluetooth.sh`, `nvidia.sh` on the Omen and Victus, and whatever the Intel subdirectory decides applies.

Evidence here is uneven. Twenty-six issues match HP EliteBook, Spectre, Envy or Omen by text, but many are false matches: the word "Spectre" mostly appears in kernel `Spectre V2` mitigation log lines, and "Envy" usually means the `envycontrol` tool rather than an Envy laptop. Eleven issues are from a confirmed HP machine. The EliteBook and Spectre x360 lines have the most, the Omen and Victus have almost none, so treat the Omen as unrated in practice.

## What works

The GPU is the quiet part. On the AMD EliteBook 845 G10 the journal in issue #11332 shows amdgpu resuming normally across most suspend cycles, including the SMU. On the Intel Spectre x360 14-ef1xxx in issue #10170 the i915 backlight resume returns 0 and the machine is fully responsive after wake. Neither reporter has a graphics complaint.

Installation itself is not a topic. No HP reporter has filed a failed install, and the Envy boot hang in issue #3829 is firmware behaviour rather than an installer problem.

Everything else on this list is unknown rather than proven good. The tracker only tells you what broke. Wi-Fi, Bluetooth, touchpad, battery life and hibernation have no HP-specific reports either way, which is mildly encouraging and not evidence.

## What breaks

**Suspend on the AMD EliteBook 845 G10.** Issue #11332, open, filed on 4.0.3 with Linux 7.2.3 and BIOS V82. Closing the lid intermittently leaves the machine unable to resume; the lid, the power button and everything else are dead until you hold power down. The reporter counted his own journals: about 6 percent of suspends left no matching `PM: suspend exit` on Linux 7.1.9, and about 31 percent on 7.2.3. Since 4.0.4 ships the bespoke `linux-omarchy` kernel to every machine, and the stable channel is on 7.2.5 as of this check, this is a risk worth knowing about before you update. The machine exposes only `[s2idle]` in `/sys/power/mem_sleep`, so there is no S3 to fall back on. See [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/).

**A dark panel after lid-open on a laptop with no external monitor.** Issue #10170, open, from a Spectre x360 14-ef1xxx on 4.0.2. The lock screen blanks the panel five seconds after locking, and the only two code paths that re-enable DPMS are a keypress on the lock screen password field and the clamshell reconciler, which does nothing when no external monitor was ever attached. Press any key and the screen comes back. The power button will not do it, because logind swallows it.

**The webcam on Meteor Lake Spectre x360.** Issue #7697, open. Omarchy's `ipu7-camera.sh` installs `intel-ipu7-camera` whenever ACPI HID `OVTI08F4` is present, but that sensor is paired with IPU6 on Meteor Lake. The IPU7 package ships only the `ipu75xa` HAL, so `icamerasrc` finds no plugin and the v4l2loopback device serves a black frame. PR #7773 narrows the gate to the Panther Lake controller `8086:b05d`; it was still open when checked. It does not remove the package from machines that already have it, so you clear it yourself with `omarchy-pkg-drop intel-ipu7-camera`. Older AMD EliteBooks have their own webcam report, issue #4529 on an 835 G8, closed with no confirmed fix after a contributor said his own camera was fine.

**Fingerprint readers.** Omarchy's detector keys on USB vendor IDs, and Validity's `138a` is on the list, so an EliteBook 8470w with a VFS491 passes the gate, installs packages, then fails to enroll with `NoSuchDevice` because libfprint carries no driver for that sensor. That is issue #10892, open. A separate EliteBook report, issue #8747, found the lock screen hanging 25 to 30 seconds after resume when the fprintd daemon restarts under it; the reporter closed it himself after fixing it at the driver level by enabling `open-fprintd-suspend` and `open-fprintd-resume`. See [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/) and the manual chapter on [hardware authentication](https://omarchy.org/manual/hardware-authentication/).

**Audio and the mute keys.** On a Meteor Lake Spectre x360 with dual CS35L41 amplifiers, issue #11611 describes the ALSA sink stuck in SUSPENDED and the top bar showing a permanent muted glyph with no way back. The reporter is clear that the root cause is a driver bug going upstream, not Omarchy. Separately, the microphone mute key on a Spectre x360 13-aw0xxx emits an ACPI event rather than a keycode, issue #5127, still open; the reporter works around it with an acpid handler calling `wpctl`. The EliteBook 845 G10 mic-mute report, issue #4570, turned out to be a SwayOSD 0.3.0 regression and is not relevant on 4.x, since Quattro removed SwayOSD entirely.

**Envy x360 boot delay.** Issue #3829, from a 15m-bq121dx on 3.2.2: the ACPI NVS and AMD fTPM regions overlap, systemd waits out the TPM, and boot takes 90 extra seconds. The fix is `memmap=` kernel parameters carving out the TPM CRBs, and those addresses are machine-specific.

## What Omarchy does for this model

Nothing by name. There is no `omarchy-hw-hp-*` script, no HP branch in `install/hardware/all.sh`, and no DMI match string for an HP product anywhere in v4.0.4. `omarchy-hw-match` exists and is used for Framework 16, Dell XPS OLED and haptics, Surface and two ASUS models. HP is not among its callers.

What does touch these machines is generic: `install/hardware/intel/ipu7-camera.sh` (the webcam problem above), `install/hardware/intel/sof-firmware.sh`, `install/hardware/intel/lpmd.sh` and `thermald.sh` on Intel models, `install/hardware/nvidia.sh` on Omen and Victus, and `install/hardware/speaker-tuning.sh`, which only installs the LV2 plugins when `omarchy-audio-tuning match` finds a tuning. No shipped tuning matches an HP, so the CS35L41 amplifiers in the Spectre x360 get no speaker profile.

The RGB keyboard on Victus and Omen has no control. Issue #4987 offered a `kbdcolor` helper driving `/sys/class/leds/hp::kbd_backlight/multi_intensity` and was closed without landing. `omarchy-brightness-keyboard` only handles brightness, not colour.

## Variants

Prefer the Intel Spectre x360 generations before Meteor Lake if the webcam matters, or accept removing the IPU7 package. A 14-ef1xxx on Alder Lake has a working camera path and a shell bug instead.

The AMD EliteBook 800 series is the best-documented HP here, but the 845 G10 carries the open s2idle resume problem. If you buy one, budget time on sleep testing before you trust it to a lid close.

Avoid assuming the fingerprint reader works. Check the USB ID first. Validity VFS491 and the `138a:00ab` sensor both needed work; neither is driven by stock libfprint out of the box.

The Omen and Victus are the gap. There is essentially no hardware evidence for them beyond a declined RGB feature request, and the NVIDIA side of those machines is a bigger factor than the HP side. Read [/hardware/nvidia/](/hardware/nvidia/) and [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) before you buy one.

## Before you install

Check `cat /sys/power/mem_sleep`. If it prints only `[s2idle]`, read [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and plan for the possibility that lid-close sleep is unreliable.

Run `lsusb | grep -iE '138a|27c6|06cb'` in a live session and look your reader up in libfprint's supported list before you count on fingerprint unlock.

On a Meteor Lake Spectre, check `lsmod | grep intel_ipu` after install. If `intel_ipu6` is loaded and `intel-ipu7-camera` is installed, drop the package.

Update your BIOS from the vendor first. The EliteBook report was on a current BIOS and still failed, but firmware is the cheapest variable to eliminate.

Read [/upgrade/before-you-update-checklist/](/upgrade/before-you-update-checklist/) before taking 4.0.4, since it is the release that puts the `linux-omarchy` kernel on every machine, and the one open HP suspend report blames a kernel bump.

## Related

[/hardware/suspend-sleep/](/hardware/suspend-sleep/), [/hardware/webcam/](/hardware/webcam/), [/hardware/fingerprint/](/hardware/fingerprint/), [/hardware/audio/](/hardware/audio/), [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/), [/fix/webcam-not-detected/](/fix/webcam-not-detected/), [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/), [/hardware/submit/](/hardware/submit/).
