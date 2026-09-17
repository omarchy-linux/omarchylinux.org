---
title: "Lenovo ThinkPad X1 Carbon on Omarchy"
description: "Omarchy on the ThinkPad X1 Carbon Gen 8 to Gen 14: what works, the Gen 13 speaker and Gen 14 camera breakage, and the hardware scripts that fire."
answer: "Buy Gen 8 through Gen 12 and you get a solid Omarchy laptop. Gen 13 and Gen 14 are the risky ones: the Gen 14 webcam is still dead in tracked reports, its microphone needed a Lenovo BIOS update, and a Gen 13 owner lost internal speakers to a SoundWire clash. No ThinkPad quirk script ships in 4.0.4, so enablement is generic Intel."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Lenovo"
model: "ThinkPad X1 Carbon"
dmi: ["20U9CTO1WW", "20XWCTO1WW", "21HMCTO1WW", "21HNS65E00", "21NS0012US", "21V7CTO1WW"]
cpu: "Intel Core, Comet Lake through Panther Lake"
gpu: "Intel integrated (i915 or xe)"
year: "2020 to 2026"
rating: silver
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: partial
  fingerprint: partial
  gpu: works
  suspend: partial
  hibernate: partial
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: works
quirkScripts:
  - name: "intel/sof-firmware.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/sof-firmware.sh"
    note: "Installs sof-firmware whenever an Intel audio DSP is present. Every X1 Carbon in range matches."
  - name: "intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Installs and enables thermald on Intel laptops from Sandy Bridge up."
  - name: "intel/lpmd.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/lpmd.sh"
    note: "Installs intel-lpmd for listed hybrid CPU model IDs. No Arrow Lake ID is in the list."
  - name: "intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Installs intel-media-driver, libvpl and vpl-gpu-rt for Iris and Xe graphics."
  - name: "intel/ipu7-camera.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    note: "Installs intel-ipu7-camera only when ACPI device OVTI08F4 exists. Gen 14 only."
  - name: "intel/fred.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fred.sh"
    note: "Adds fred=on to the Limine kernel cmdline on Panther Lake. Gen 14 only."
  - name: "omarchy-brightness-keyboard-mute"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-brightness-keyboard-mute"
    note: "Drives the ThinkPad platform::micmute LED through brightnessctl."
issueCount: 46
tags: [thinkpad, x1-carbon, lenovo, intel, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10916"
    title: "Issue #10916: ThinkPad X1 Carbon Gen 13: RT1318 speakers permanently silent after SoundWire CTRL_CLASH (empty Cadence PING)"
    kind: issue
    author: "aramsdale"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10250"
    title: "Issue #10250: ThinkPad X1 Carbon Gen 14: lid s2idle never wakes; hibernate reboots; lid-open leaves panel dark"
    kind: issue
    author: "heredia21"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/10252"
    title: "Issue #10252: Lock-on-suspend runs after PrepareForSleep(true), so pam_fprintd can never install fprintd's sleep delay inhibitor"
    kind: issue
    author: "wbnns"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/11005"
    title: "Issue #11005: SOF ThinkPad: no headphone autoswitch, stale HDMI default, MPRIS pause on jack, mute LED dark"
    kind: issue
    author: "JeffFlag"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/7909"
    title: "Issue #7909: Random hard reboots on ThinkPad X1 Carbon Gen 11 - Omarchy only, Ubuntu stable"
    kind: issue
    author: "SuleymanSuleymanzade"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6001"
    title: "Issue #6001: Microphone on ThinkPad X1 Carbon Gen 14 (Panther Lake + CS42L45) silent"
    kind: issue
    author: "ocewers"
    date: "2026-05-30"
  - url: "https://github.com/omacom/omarchy/issues/6000"
    title: "Issue #6000: Camera (IPU7-PTL / OV08X40) on ThinkPad X1 Carbon Gen 14: ACPI status=0, sensor invisible to Linux"
    kind: issue
    author: "ocewers"
    date: "2026-05-30"
  - url: "https://github.com/omacom/omarchy/issues/3619"
    title: "Issue #3619: X1 Carbon Gen 13 LUKS Prompt Black Screen"
    kind: issue
    author: "cutzenfriend"
    date: "2025-11-25"
  - url: "https://github.com/omacom/omarchy/issues/731"
    title: "Issue #731: Plymouth not working on ThinkPad X1 Carbon Gen 8 w/ systemd-boot"
    kind: issue
    author: "shawnyeager"
    date: "2025-08-12"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.3"
    title: "Omarchy v3.8.3 release notes"
    kind: release
    date: "2026-07-13"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
credits:
  - name: "ocewers"
    url: "https://github.com/ocewers"
    for: "Traced the Gen 14 microphone and camera failures to Panther Lake codec and IPU7 gaps, and found the BIOS update that fixed the mic"
  - name: "heredia21"
    url: "https://github.com/heredia21"
    for: "Mapped Gen 14 lid sleep, hibernate and dark-panel behaviour and corrected the first report"
  - name: "aramsdale"
    url: "https://github.com/aramsdale"
    for: "Documented the Gen 13 SoundWire clash that left the RT1318 speaker amp unattached"
  - name: "AlwxSin"
    url: "https://github.com/AlwxSin"
    for: "Found that removing the kms hook fixes the Gen 13 black LUKS prompt"
  - name: "felipecpaiva"
    url: "https://github.com/felipecpaiva"
    for: "Spotted that thermald was dying at every boot on a Gen 10"
  - name: "wbnns"
    url: "https://github.com/wbnns"
    for: "Measured the fingerprint sleep-inhibitor race on a Gen 8 and retracted his own workaround"
faq:
  - q: "Is the ThinkPad X1 Carbon a good Omarchy laptop?"
    a: "Gen 8 to Gen 12 are among the safest machines you can pick. Gen 13 and Gen 14 carry open hardware bugs, so buy those only if you are willing to debug audio and camera."
  - q: "Does the webcam work on the X1 Carbon Gen 14?"
    a: "Not in the tracked reports. Issue #6000 is still open: the OV08X40 sensor reports ACPI status 0, never binds, and /dev/video50 delivers black frames."
  - q: "Why is my X1 Carbon LUKS prompt a black screen?"
    a: "Reported on Gen 13 in issue #3619. Removing the kms hook from /etc/mkinitcpio.conf and rerunning mkinitcpio -P restored the prompt for two owners."
related: [suspend-sleep, webcam, audio, fingerprint, intel-gpu, lenovo-thinkpad-t14]
draft: false
---

## Verdict

Silver, and the rating hides a split. The older half of this family is one of the calmest things you can run Omarchy on. The newest half is not.

Across 46 tracked issues that mention an X1 Carbon, almost every hardware failure with a clear root cause lands on Gen 13 or Gen 14. Gen 8 through Gen 12 show up mostly in generic Omarchy bugs that have nothing to do with the chassis. If you rated Gen 14 on its own it would be bronze today.

Everything below was checked against Omarchy 4.0.4 source and against issue reports filed on 3.2.0 through 4.0.3.

## What works

Graphics are the strong point. On Gen 13 the reporter of the black LUKS prompt said the i915 driver works perfectly once the system is up, and the same machine ran fine under the xe driver too. No X1 Carbon issue in the set reports a broken desktop, a compositor that will not start, or missing acceleration.

The ThinkPad mic-mute lamp works. Omarchy writes the `platform::micmute` LED node through `omarchy-brightness-keyboard-mute`, which is wired into `omarchy-audio-input-mute`. That path started as a ThinkPad contribution in 3.6.0 and was folded into the unified command in 3.7.0.

Fingerprint enrollment works on the Synaptics readers these machines ship. The Gen 8 report in issue #10252 is about a suspend race, not about enrollment: the reader enrolls, verifies, and unlocks the lock screen. See the manual chapter on [hardware authentication](https://omarchy.org/manual/hardware-authentication/) for the setup path.

Wi-Fi, Bluetooth, touchpad and battery life are marked unknown on purpose. No X1 Carbon report in the set claims any of them is broken, but absence of complaints is not a test result. If you have run one of these machines for a while, [submit what you found](/hardware/submit/).

## What breaks

**Gen 14 camera, still open.** Issue #6000 reports the OV08X40 sensor behind IPU7-PTL is invisible to Linux. ACPI `_STA` returns 0 for the sensor, nothing binds to the i2c driver, the media graph has no sensor entity, and `/dev/video50` emits black NV12 frames. The reporter says the Gen 13 on the same Omarchy install works, which points at Lenovo Panther Lake specifically rather than IPU7 in general. Tested on Omarchy 3.8.2 and unchanged in later reports.

**Gen 14 microphone, fixed by firmware, not by Omarchy.** Issue #6001 tracked a silent CS42L45 microphone with no matching SOF topology. It closed on 2026-06-08 when the reporter updated the Lenovo BIOS from N4OET47W (1.10) to N4OET49W (1.12) through Omarchy's firmware updater. His own note: the lid had to be open for the update to apply.

**Gen 14 lid and hibernate.** Issue #10250 is open. Lid-open does not light the internal panel when there is no external display, because the stock binding for `switch:off:Lid Switch` is `omarchy-hyprland-monitor-clamshell`, which never re-enables DPMS on eDP-1. Hibernate is not a resume on that machine while zram sits at priority 100 above the resume swapfile. The reporter later corrected himself: stock lid-close sleep does wake on that hardware, and the never-wakes reports came from his own lid-ignore experiments.

**Gen 13 internal speakers.** Issue #10916 is the ugliest report in the set. After four or five days of normal use on a new Gen 13, the RT1318 amp on SoundWire link 1 went `UNATTACHED` after a `DATA_CLASH` and `CTRL_CLASH`, and never came back, on Linux or on Windows. Nobody has shown Omarchy caused it, and the reporter does not claim that either. Treat it as one unexplained incident, not a pattern.

**Gen 13 black LUKS prompt.** Issue #3619, closed. The prompt is invisible at the Plymouth stage while the password still types through blind. Removing the `kms` hook from `/etc/mkinitcpio.conf` and running `sudo mkinitcpio -P` fixed it for two owners.

**Gen 11 random hard reboots.** Issue #7909 is open and unresolved. Spontaneous resets with no panic, no MCE, no thermal event, on both `linux` and `linux-lts`, with Ubuntu stable on the same machine. Another owner reproduced hard hangs on the same chassis under CachyOS and Manjaro, which argues the cause sits in the Arch kernel, firmware and Mesa stack rather than in Omarchy. One reporter later said a full Omarchy update made it stop for him. Buyers of used Gen 11 units should know this thread exists.

**Gen 9 and older audio policy.** Issue #11005 collects four SOF gaps on a Gen 9: plugging headphones does not switch output because Speaker and Headphones are separate UCM card profiles, HDMI jack detect does not clear after unplug, and the `platform::mute` speaker lamp stays dark because it follows ALSA Master rather than PipeWire mute.

**Gen 8 fingerprint during suspend.** Issue #10252, closed. `omarchy-system-sleep-monitor` locks after logind emits `PrepareForSleep(true)`, so `fprintd` can no longer take a sleep inhibitor. The measured gap was 283 ms with the reader open, 8 inhibitor failures across 10 suspends over 14 days. The reporter also retracted his own workaround twice and asks people to remove it: stopping `fprintd` does not release the reader.

## What Omarchy does for this model

Nothing by name. Grep `bin/`, `install/hardware/` and `default/` in the v4.0.4 tree and there is no ThinkPad match anywhere. The only script under `install/hardware/lenovo/` is `fix-yoga-pro7-bass-speakers.sh`, which matches the DMI string `Yoga Pro 7 14IAH10` and skips every X1 Carbon.

What you actually get is the generic Intel path from `install/hardware/all.sh`:

- `intel/sof-firmware.sh` installs `sof-firmware` when an Intel audio DSP is present. Without it PipeWire only shows a Dummy Output. v3.8.3 widened this across Arrow Lake, Meteor Lake, Wildcat Lake and Panther Lake and made it ask for a reboot.
- `intel/video-acceleration.sh` pulls `intel-media-driver`, `libvpl` and `vpl-gpu-rt` for Iris and Xe graphics.
- `intel/thermald.sh` and `intel/lpmd.sh` add thermal and low-power management. Worth checking after install: a Gen 10 owner in issue #7909 found `thermald` had been dying at every boot for weeks with `Unsupported cpu model or platform`, and fixed it with a drop-in adding `--ignore-cpuid-check`. Note that `lpmd.sh` gates on a fixed list of CPU model IDs covering Alder, Raptor, Meteor, Lunar and Panther Lake. There is no Arrow Lake ID in that list.
- `intel/ipu7-camera.sh` installs `intel-ipu7-camera` only if an ACPI device with HID `OVTI08F4` exists, which is the Gen 14 sensor.
- `intel/fred.sh` writes a Limine drop-in adding `fred=on` on Panther Lake, so Gen 14 only.
- `intel/fix-wifi7-eht.sh` disables 802.11be, but only for PCI IDs `8086:e440` and `8086:272b`. An AX211 card does not match.

`bin/omarchy-hw-match` is the tool these scripts use, and it greps `/sys/class/dmi/id/product_name` or `product_family` case-insensitively. On a ThinkPad `product_name` is the machine type, so your own overrides should match strings like `21V7CTO1WW`.

## Variants

Machine types seen in the reports: `20U9CTO1WW` (Gen 8), `20XWCTO1WW` (Gen 9), `21HMCTO1WW` and `21HNS65E00` (Gen 11), `21NS0012US` (Gen 13), `21V7CTO1WW` (Gen 14).

- **Gen 8 to Gen 10.** The safe used buy. Comet Lake through Alder Lake, Intel Wi-Fi, Synaptics reader, well-trodden i915.
- **Gen 11.** Raptor Lake-P with Iris Xe. Good hardware, but read issue #7909 before you commit.
- **Gen 12.** Meteor Lake. Only generic Omarchy bugs in the set, no chassis-specific breakage found.
- **Gen 13.** Two different silicon configurations appear in the reports, one described as Arrow Lake-U and one as Lunar Lake. Camera works, speakers have one bad incident, boot-time display needs the kms hook removed.
- **Gen 14.** Panther Lake. Avoid unless you want to do enablement work. Camera is dead, microphone needs current firmware, hibernate is not usable as shipped.

## Before you install

1. Update the Lenovo BIOS from Windows or through the Omarchy firmware updater first. On Gen 14 that is what fixed the microphone. Keep the lid open while it applies.
2. Snapshot before every update. Two reporters in this set diagnosed problems by booting a prior Snapper snapshot.
3. On Gen 13, if the LUKS prompt is a black screen, do not reach for `nomodeset`. Remove the `kms` hook and rerun `mkinitcpio -P`.
4. After the first boot, run `journalctl -u thermald` and confirm it is running rather than dying on a cpuid check.
5. On Gen 14, do not rely on hibernate. Check `swapon --show` and see whether zram outranks your swapfile.
6. If you use fingerprint unlock, expect the reader to re-enumerate on every resume. See [Omarchy's system sleep chapter](https://omarchy.org/manual/system-sleep/) for the toggles.

## Related

- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/webcam/](/hardware/webcam/) and [/fix/webcam-not-detected/](/fix/webcam-not-detected/)
- [/hardware/audio/](/hardware/audio/) and [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/)
- [/hardware/fingerprint/](/hardware/fingerprint/) and [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/)
- [/hardware/intel-gpu/](/hardware/intel-gpu/), [/hardware/lenovo-thinkpad-t14/](/hardware/lenovo-thinkpad-t14/), [/hardware/lenovo-thinkpad-t480/](/hardware/lenovo-thinkpad-t480/)
- [/fix/hibernate-fails-or-hangs/](/fix/hibernate-fails-or-hangs/) and [/releases/still-broken/](/releases/still-broken/)
