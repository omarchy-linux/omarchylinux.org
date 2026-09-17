---
title: "Lenovo Yoga on Omarchy Linux"
description: "Lenovo Yoga support on Omarchy 4.0.4: the Yoga Pro 7 14IAH10 gets a bass speaker quirk, but touchpad, USB-C display and older-BIOS boot problems are open."
answer: "Rate the modern Intel Yoga silver. Wi-Fi, Intel graphics and the display work, and the Yoga Pro 7 14IAH10 is the only Yoga with a dedicated Omarchy quirk (an ALC287 bass speaker pin). Expect one or two quirks: the I2C Precision Touchpad can fail to bind at cold boot, and USB-C DisplayPort can wedge. Older Yogas (730, C940, 11e) are bronze at best and may not boot without BIOS changes."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [lenovo, yoga, laptop, convertible, intel, touchpad]
kind: model
vendor: "Lenovo"
model: "Lenovo Yoga"
dmi: ["Yoga Pro 7 14IAH10", "Yoga Slim 7 ProX 14IAH7", "Yoga 7 2-in-1 14ILL10", "Yoga Pro 9 16IMH9", "Yoga 14s ITL 2021", "YOGA 730-15IKB", "Yoga C940", "83KF", "82TK", "83JQ", "82G2"]
cpu: "Intel Core, Kaby Lake through Arrow Lake and Lunar Lake in the reported machines"
gpu: "Intel integrated (UHD, Iris Xe, Arc); RTX 3050/4060 Mobile on Pro X and Pro 9"
year: "2017-2026"
rating: silver
subsystems:
  wifi: works
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: partial
  gpu: works
  suspend: partial
  hibernate: unknown
  touchpad: partial
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "fix-yoga-pro7-bass-speakers.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    note: "Matches DMI \"Yoga Pro 7 14IAH10\" and writes an snd-sof-intel-hda-generic hda_model pin quirk so both AMP speakers get bass."
issueCount: 25
sources:
  - url: "https://github.com/omacom/omarchy/issues/6110"
    title: "Issue #6110: No audio on Intel Arrow Lake - sof-firmware not installed, DSP fails to boot (Dummy Output)"
    kind: issue
    author: "hyprcat"
    date: "2026-06-19"
  - url: "https://github.com/omacom/omarchy/issues/9658"
    title: "Issue #9658: Trackpad (MSFT0001 I2C Precision Touchpad) fails to bind at boot due to i2c_designware controller timeout"
    kind: issue
    author: "vashizm0r"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10492"
    title: "Issue #10492: USB-C DP alt mode dead after LTTPR link-training failures (no HPD, zero events) until EC power drain - Yoga 14s ITL 2021"
    kind: issue
    author: "dunova"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10459"
    title: "Issue #10459: Session lock silently lost on output re-add: desktop exposed without authentication (and quickshell SIGABRT on the same path)"
    kind: issue
    author: "nikitaprokopov"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/9450"
    title: "Issue #9450: Omarchy install ends with cryptic VFS: Cannot open root device \"\" or unknown-block(0,0) or grub_memalign:552:out of memory"
    kind: issue
    author: "jsuchal"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/5903"
    title: "Issue #5903: Toggling laptop screen back on moves touchscreen to external monitor"
    kind: issue
    author: "MrKrar"
    date: "2026-05-19"
  - url: "https://github.com/omacom/omarchy/issues/5980"
    title: "Issue #5980: Panic: High memory allocator: Out of memory on Update to 3.8.0"
    kind: issue
    author: "yellowbluebus"
    date: "2026-05-26"
  - url: "https://github.com/omacom/omarchy/issues/2693"
    title: "Issue #2693: Black Screen | Unresponsive system | First Boot"
    kind: issue
    author: "Dan-Kingsley"
    date: "2025-10-22"
  - url: "https://github.com/omacom/omarchy/issues/3616"
    title: "Issue #3616: Intermittent fan failure on Lenovo Yoga Slim 7 ProX (ACPI H_EC errors)"
    kind: issue
    author: "domozurek"
    date: "2025-11-25"
  - url: "https://github.com/omacom/omarchy/issues/1336"
    title: "Issue #1336: Wifi - Powered Off After Suspend (FIXED)"
    kind: issue
    author: "Prajwal-Prathiksh"
    date: "2025-08-30"
  - url: "https://github.com/omacom/omarchy/issues/4576"
    title: "Issue #4576: USB keyboard eject on lock screen bugs laptop keyboard"
    kind: issue
    author: "thebrahman"
    date: "2026-02-11"
  - url: "https://github.com/omacom/omarchy/issues/12143"
    title: "Issue #12143: Fresh Quattro install: Limine UKI chainload panics with efi: LoadImage failure (EFI_INVALID_PARAMETER) on older UEFI"
    kind: issue
    author: "keylimesoda"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11841"
    title: "Issue #11841: Fingerprint setup gives no diagnosis when libfprint has no driver for the detected reader"
    kind: issue
    author: "busbyjon"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/7803"
    title: "Issue #7803: `pending-charge` treated as a charge-limit hold without checking the level: a failed battery reports \"Holding at 75-80%\" at 0%"
    kind: issue
    author: "xeeg"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    title: "install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.0"
    title: "Release v3.8.0 release notes"
    kind: release
    author: "omacom"
    date: "2026-05-09"
credits:
  - name: "aikazu"
    url: "https://github.com/aikazu"
    for: "Contributed the Yoga Pro 7 14IAH10 bass speaker fix shipped in v3.8.0"
  - name: "vashizm0r"
    url: "https://github.com/vashizm0r"
    for: "Traced the cold-boot touchpad failure to an i2c_designware controller timeout and published a PCI rescan workaround"
  - name: "dunova"
    url: "https://github.com/dunova"
    for: "Documented the USB-C DisplayPort wedge and the EC power drain recovery on a Yoga 14s ITL"
  - name: "jsuchal"
    url: "https://github.com/jsuchal"
    for: "Found that Intel PTT has to be disabled to install on a Yoga 7 ProX"
faq:
  - q: "Does Omarchy have hardware support for the Lenovo Yoga?"
    a: "One script only. install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh matches the DMI string \"Yoga Pro 7 14IAH10\" and installs an ALC287 pin quirk. Every other Yoga rides the generic Intel path."
  - q: "My Yoga trackpad is dead after a cold boot. Is it broken?"
    a: "Probably not. Issue #9658 shows the Intel LPSS I2C controller timing out before the Precision Touchpad answers, so no input device is created. Removing and rescanning the PCI I2C controllers brings it back."
  - q: "Which Yoga should I avoid?"
    a: "Pre-2020 units. The YOGA 730-15IKB, C940 and ThinkPad Yoga 11e all have open or worked-around boot failures. Buy a 2023 or newer Intel Yoga Pro or Slim instead."
related: [touchpad-input, multi-monitor, audio, boot-limine, lenovo-thinkpad-t14]
draft: false
---

## Verdict

Silver, and only if you buy a recent one. A 2023-or-newer Intel Yoga Pro or Yoga Slim installs and runs Omarchy on the generic Intel path: Wi-Fi, Intel graphics, the internal display and the keyboard all come up without intervention. The quirks are real but narrow, and each has a known workaround.

The Yoga family is broad, so the rating is not uniform. Omarchy ships exactly one Yoga-specific fix, for the Yoga Pro 7 14IAH10. Everything else is generic enablement. Older Yogas (the 730-15IKB, the C940, the ThinkPad Yoga 11e) have open boot failures and drop to bronze.

Evidence base: 25 issues in the tracker touch a Yoga, 15 of them still open. That is enough to describe failures, not enough to certify successes. Anywhere below where a subsystem is marked unknown, it means nobody filed a bug, not that it was tested.

## What works

Wi-Fi is the one subsystem with a clean history. The only Yoga Wi-Fi bug of substance, [#1336](https://github.com/omacom/omarchy/issues/1336), was radio staying powered off after suspend, closed on 2025-09-01 when DHH added an rfkill trigger under Update > Hardware > Wifi.

Intel graphics work. The reported Yogas span Kaby Lake, Tiger Lake, Alder Lake, Arrow Lake and Lunar Lake, all on i915 or xe, and none of the open issues are about the internal panel failing to light up on a current kernel.

Speakers work once firmware is present, and on v4.0.4 it is. `install/hardware/intel/sof-firmware.sh` installs `sof-firmware` whenever `omarchy-hw-intel-sof` sees an Intel audio controller, which every Yoga in the tracker has. That enablement landed in v3.8.3 (2026-07-13).

Convertible hinge hardware (touchscreen, pen) is reported working in passing, but there is no automatic screen rotation or tablet UI. Tablet mode is your own Hyprland configuration, not something Omarchy provides.

## What breaks

**Touchpad missing at cold boot.** [#9658](https://github.com/omacom/omarchy/issues/9658) (open, filed 2026-09-01 by vashizm0r on a Lenovo 21DM convertible) shows `i2c_hid_acpi i2c-MSFT0001:01: probe with driver i2c_hid_acpi failed with error -110` and an `i2c_designware ... controller timed out` behind it. The Precision Touchpad never binds, so `hyprctl devices` lists no mice at all. The reporter's fix is to remove each PCI I2C controller and rescan the bus; rebinding only the HID driver is not enough. The controller addresses are machine-specific, so read yours from `lspci` first. Omarchy ships no generic version of this.

**USB-C DisplayPort goes permanently dead.** [#10492](https://github.com/omacom/omarchy/issues/10492) (open, Yoga 14s ITL 2021) is the sharpest report on the page. After repeated i915 LTTPR link-training failures, both Type-C ports stop reporting display connectivity: every DRM connector reads `disconnected`, `udevadm monitor` records zero events, and `/sys/class/typec/` is empty. Power delivery over the same cable keeps working. The state survives reboot and full shutdown on two kernels. The only recovery dunova found was a full EC drain: shut down, unplug everything, hold the power button for 30 to 40 seconds.

**Audio silent on Arrow Lake.** [#6110](https://github.com/omacom/omarchy/issues/6110) was filed on a LENOVO Yoga Pro 7 14IAH10 (`83KF`) running Omarchy 3.8.2, with PipeWire showing only a Dummy Output. The v3.8.3 `sof-firmware` change addresses the cause, but the issue is still open with later reports on other machines, so check `cat /proc/asound/cards` before assuming your hardware is broken.

**Boot failures on older units.** [#9450](https://github.com/omacom/omarchy/issues/9450) on a Yoga 7 ProX ends in `VFS: Cannot open root device`; jsuchal's own answer is that the firmware calls Secure Boot support Intel Platform Trust Technology (Intel PTT), and disabling it made the install work. [#5980](https://github.com/omacom/omarchy/issues/5980) is a Limine out-of-memory panic on a YOGA 730-15IKB. [#2693](https://github.com/omacom/omarchy/issues/2693) is a first-boot black screen on a Yoga C940 that the reporter solved by switching to the LTS kernel. [#12143](https://github.com/omacom/omarchy/issues/12143) is a Quattro UKI chainload panic on a Bay Trail ThinkPad Yoga 11e.

**Convertible-specific display handling.** [#5903](https://github.com/omacom/omarchy/issues/5903) (open, Yoga 7 2-in-1 14ILL10) reports that toggling the laptop panel back on reassigns the touchscreen to the external monitor.

**Lock screen on hybrid Yogas.** [#10459](https://github.com/omacom/omarchy/issues/10459), filed on a Yoga Pro 9 16IMH9 with an Arc iGPU plus RTX 4060 Mobile, describes the session lock being lost when an output is re-added, leaving the desktop visible. A related stranded-lock bug, [#6684](https://github.com/omacom/omarchy/issues/6684), was fixed by PR #6692 and shipped before 4.0.0.

**Fingerprint.** On a ThinkPad L13 Yoga Gen 3, [#11841](https://github.com/omacom/omarchy/issues/11841) shows `omarchy-hw-fingerprint` correctly detecting a Goodix `27c6:55b4` reader, then enrollment failing because libfprint has no driver for it. Detection is not support.

**Fan control, historical.** [#3616](https://github.com/omacom/omarchy/issues/3616) on a Yoga Slim 7 ProX 14IAH7 (`82TK`) reported fans stopping while the CPU passed 90 C, with `ACPI BIOS Error ... \_SB.PC00.LPCB.HEC.CFSP, AE_NOT_FOUND` in the log. A suspend and resume restarted them. Closed as completed on 2025-11-25 with no comments, so treat the resolution as unexplained rather than fixed.

## What Omarchy does for this model

One script, added in v3.8.0 (2026-05-09) by @aikazu and still present at v4.0.4:

`install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh` runs `omarchy-hw-match "Yoga Pro 7 14IAH10"` and, on a match, writes `/etc/modprobe.d/lenovo-yoga-pro7-bass.conf` with `options snd-sof-intel-hda-generic hda_model=alc287-yoga9-bass-spk-pin`. Without it the ALC287 codec drives only one speaker and the bass AMP stays silent.

`omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `/sys/class/dmi/id/product_family`, case-insensitively. Lenovo puts the numeric code (`83KF`) in `product_name` and the marketing name in the family or version field, so run `cat /sys/class/dmi/id/product_family` yourself to confirm the match before blaming the script.

Beyond that, a Yoga gets only the generic passes in `install/hardware/all.sh`: Intel video acceleration, `lpmd`, `thermald`, the IPU7 camera driver when an `OVTI08F4` sensor is present, `sof-firmware`, the Wi-Fi 7 EHT fix, and the wireless regdom. There is no Yoga speaker tuning in `default/audio/tunings/` (only the Dell XPS 2026 has one), no Yoga touchpad fix, and nothing Lenovo-specific for suspend.

## Variants

Prefer a 2023 or newer Intel Yoga Pro or Yoga Slim. The Yoga Pro 7 14IAH10 is the best-understood model here because it is the only one with dedicated code.

Be careful with the Yoga Pro 9 16IMH9 and Slim 7 ProX: both pair an Intel iGPU with an NVIDIA mobile GPU, which puts you on the hybrid GPU path with its own failure modes.

Avoid pre-2020 Yogas for a first install. The 730-15IKB, C940 and ThinkPad Yoga 11e all appear in the tracker with boot problems.

Snapdragon Yogas (Yoga Slim 7x and similar) are not covered here. An earlier prototype of this site rated the Slim 7x experimental on the strength of a live session in an ARM enablement PR. That is not the public ISO and this page does not carry the claim forward.

## Before you install

- In the BIOS, look for Intel Platform Trust Technology, not a menu item called Secure Boot. Disable it if the installer stalls at boot.
- Update the Lenovo UEFI first. The oldest machines in this tracker are also the ones that fail to chainload.
- Boot the live ISO and check `hyprctl devices` for a touchpad before you commit the disk. If it is missing, you have #9658.
- Plug in and unplug your USB-C monitor while you still have a fallback. #10492 is not recoverable by software.
- Run `cat /sys/class/dmi/id/product_family` and note the string. It decides whether the bass fix applies.
- After first boot, check `cat /proc/asound/cards` for a real device rather than Dummy Output.

## Related

- [/hardware/touchpad-input/](/hardware/touchpad-input/) for the I2C HID binding failure in general
- [/hardware/multi-monitor/](/hardware/multi-monitor/) and [/hardware/thunderbolt-dock/](/hardware/thunderbolt-dock/) for USB-C display problems
- [/hardware/audio/](/hardware/audio/) and [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/)
- [/hardware/boot-limine/](/hardware/boot-limine/) and [/fix/kernel-panic-after-update-limine/](/fix/kernel-panic-after-update-limine/)
- [/hardware/fingerprint/](/hardware/fingerprint/) and [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/)
- Omarchy manual: [hardware authentication](https://omarchy.org/manual/hardware-authentication/), [monitors](https://omarchy.org/manual/monitors/), [keyboard, mouse and trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/)
