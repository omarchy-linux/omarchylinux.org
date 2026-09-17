---
title: "Dell XPS 13 (2026, Wildcat Lake) on Omarchy"
description: "Dell XPS 13 DX13260 on Omarchy 4.0.4: speakers are the big open problem, plus a Panel Replay judder and a suspend hang on the new kernel."
answer: "Buy it only if you can live with the audio bugs. On the 2026 XPS 13 (DX13260) the Cirrus CS35L56 speaker amps still fail to load firmware on both known SKUs, so internal speakers are silent or bass-less. The touchpad, panel and text scaling are handled by Omarchy. Panel Replay judder and a linux-omarchy suspend hang are open too."
appliesTo:
  from: "4.0.0"
kind: model
vendor: "Dell"
model: "Dell XPS 13"
dmi: ["XPS 13 DX13260", "XPS 9315"]
year: "2026"
cpu: "Intel Core Ultra (Wildcat Lake); Panther Lake on some SKUs"
gpu: "Intel Xe3 integrated"
rating: bronze
status: partial
issueCount: 18
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: broken
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: works
  display: partial
  battery: unknown
  keyboard: unknown
quirkScripts:
  - name: "omarchy-hw-dell-xps-haptic-touchpad"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-haptic-touchpad"
    note: "Matches XPS in DMI plus the Synaptics i2c-VEN_06CB:00 device, then installs dell-xps-touchpad-haptics."
  - name: "install/hardware/dell-xps-touchpad-haptics.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/dell-xps-touchpad-haptics.sh"
    note: "Adds the haptics package during install."
  - name: "install/user/hardware/dell/xps13-text-scaling.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/dell/xps13-text-scaling.sh"
    note: "Matches DMI DX13260 and sets the unified display text size to 11."
  - name: "omarchy-hw-dell-xps-oled"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-oled"
    note: "Panther Lake plus LG OLED EDID only, so it does not match the IPS DX13260."
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [dell, xps-13, dx13260, wildcat-lake, audio, cs35l56]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7427"
    title: "Issue #7427: Dell XPS 13 (0E53) has no bass: CS35L56 woofer amps never load firmware without the sof_sdw sidecar quirk"
    kind: issue
    author: "jonnyace"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/9687"
    title: "Issue #9687: dell-xps13-sidecar-amps reports success but speakers stay silent on spkid0 units (XPS 13 DX13260)"
    kind: issue
    author: "wizaj"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10543"
    title: "Issue #10543: Dell XPS 13 DX13260 (1028:0e53): no sound at all after dell-xps13-sidecar-amps workaround"
    kind: issue
    author: "fvargasventura"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10987"
    title: "Issue #10987: Dell XPS 13 DX13260 (1028:0e53): intermittent sof_sdw card-instantiation failure (-16 EBUSY)"
    kind: issue
    author: "aarondouglasrich"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/11320"
    title: "Issue #11320: No speaker audio on Dell XPS 13 DX13260 (2026): CS35L56 amp firmware never loads"
    kind: issue
    author: "beurle"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11356"
    title: "Issue #11356: Dell XPS 13 DX13260 (0E54): silent speakers due to missing Cirrus firmware links"
    kind: issue
    author: "zspetersen"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11374"
    title: "Issue #11374: No sound from internal speakers on Dell XPS 13 DX13260, speaker-ID/tuning read failure"
    kind: issue
    author: "Nitad"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/6853"
    title: "Issue #6853: Jittery scrolling on Dell XPS 13 (Wildcat Lake): Panel Replay stalls frame delivery"
    kind: issue
    author: "zoan37"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/pull/6849"
    title: "PR #6849: Fix jittery scrolling on Dell XPS 13 Wildcat Lake by disabling PSR and Panel Replay"
    kind: pr
    author: "zoan37"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/6551"
    title: "Issue #6551: Wifi (Intel BE213 on Dell XPS 13) doesn't work out of the box, linux-firmware on install media too old"
    kind: issue
    author: "anthonylinks"
    date: "2026-08-05"
  - url: "https://github.com/omacom/omarchy/issues/12190"
    title: "Issue #12190: linux-omarchy 7.2.5-3 hangs during suspend entry on Wildcat Lake (XPS 13 DX13260)"
    kind: issue
    author: "t27duck"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12178"
    title: "Issue #12178: Lunar Lake: intel-ipu7-camera is installed by detection but built for Panther Lake only"
    kind: issue
    author: "pkolbas"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9879"
    title: "Issue #9879: IPU6 MIPI cameras (ov01a10 / OVTI01A0) get no setup, hardware detection only covers IPU7"
    kind: issue
    author: "extragloves"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/7991"
    title: "Issue #7991: omarchy setup security fingerprint fails instantly on Goodix 27c6:530c/533c/538c readers"
    kind: issue
    author: "anupanup2001"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/dell/xps13-text-scaling.sh"
    title: "install/user/hardware/dell/xps13-text-scaling.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/audio/tunings/dell-xps-2026/tuning.conf"
    title: "default/audio/tunings/dell-xps-2026/tuning.conf at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fix-wifi7-eht.sh"
    title: "install/hardware/intel/fix-wifi7-eht.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
credits:
  - name: "wizaj"
    url: "https://github.com/wizaj"
    for: "Found the spkid0 firmware gap and published the symlink workaround, then filed it upstream with Cirrus"
  - name: "Nitad"
    url: "https://github.com/Nitad"
    for: "Traced the 0E54 failure to unread ACPI sidecar calibration properties and missing 0e54 firmware names"
  - name: "zoan37"
    url: "https://github.com/zoan37"
    for: "Isolated the Panel Replay judder on the 120 Hz panel and proposed the kernel command line fix"
  - name: "anthonylinks"
    url: "https://github.com/anthonylinks"
    for: "Documented the Intel BE213 firmware gap on install media and the sideload recovery path"
  - name: "t27duck"
    url: "https://github.com/t27duck"
    for: "Measured suspend success per kernel and pinned the hang to linux-omarchy 7.2.5-3"
faq:
  - q: "Do the speakers work on the 2026 XPS 13?"
    a: "Not reliably. Both known SKUs have open reports where the CS35L56 amps never load firmware, so you get silence or tweeters only. Headphones, USB and Bluetooth audio are unaffected."
  - q: "Is the dell-xps13-sidecar-amps package still needed?"
    a: "Not on kernel 7.2 or newer. Issue #10987 shows the kernel already sets the sidecar quirk natively, so the package logs an override that changes nothing."
  - q: "Which XPS 13 is the safest used buy?"
    a: "Older Intel XPS 13 models avoid the Cirrus amp problem, but the 9315 has an IPU6 camera that Omarchy does not set up at all, per issue #9879."
related: [dell-xps-14-2026, audio, no-sound-from-laptop-speakers, suspend-wont-resume-s2idle, wifi]
draft: false
---

## Verdict

Bronze on Omarchy 4.0.4. The 2026 XPS 13, DMI product name `XPS 13 DX13260`, is a good machine with one bad subsystem and two open annoyances. Internal speakers are the bad subsystem. Across seven issues filed between August and September 2026, the Cirrus CS35L56 amplifiers on this chassis either never load their firmware or the sound card fails to come up at all. Nothing in Omarchy fixes it today, and the two remaining paths are a kernel patch and a firmware alias, both upstream.

Everything else is livable. The haptic touchpad has a real Omarchy package, the 2560x1600 panel gets a text size tuned for it, and the machine installs and runs. If you want a laptop where audio is handled, the XPS 14 and 16 are the models Omarchy actually ships speaker tunings for.

## What works

The Synaptics haptic touchpad is enabled by Omarchy itself, and click strength is adjustable from the menu under Trigger, Hardware, Touchpad Haptics. See the [keyboard, mouse and trackpad chapter](https://omarchy.org/manual/keyboard-mouse-trackpad/) of the manual.

Display text size is pre-adjusted. `install/user/hardware/dell/xps13-text-scaling.sh` matches DMI `DX13260` and calls `omarchy-display-text-size 11`, because the panel renders the default a touch large.

Suspend works on the stock Arch kernel. In issue [#12190](https://github.com/omacom/omarchy/issues/12190), thirteen of thirteen suspends completed on `7.2.3-arch1-3` on this exact model.

Headphones, the internal microphones and the jack behaved normally in every audio report, including [#7427](https://github.com/omacom/omarchy/issues/7427). The speaker bug is confined to the two woofer amplifiers and, on some units, to card creation.

## What breaks

**Speakers.** There are two SKUs and both are broken in different ways. On SKU `0E53` (audio subsystem `1028:0e53`) the amps read their hardware speaker ID as `0`, then request `10280e53-spkid0` firmware that upstream never published, since only spkid1 to spkid3 exist. That is issue [#9687](https://github.com/omacom/omarchy/issues/9687), confirmed by three more reporters in [#10543](https://github.com/omacom/omarchy/issues/10543) and closed-as-duplicate [#11320](https://github.com/omacom/omarchy/issues/11320). On SKU `0E54` there are no `10280e54` firmware links at all, per [#11356](https://github.com/omacom/omarchy/issues/11356). Symptoms in the kernel log are `FIRMWARE_MISSING`, `Calibration disabled due to missing firmware controls` and `Can't read tuning IDs`.

The tracked upstream bug is kernel.org bugzilla 221956, where Cirrus has a patch for the speaker ID read. Until it lands, the community workarounds are symlinking the spkid0 or 0e54 filenames onto the existing spkid1 set. Both authors call them temporary, and wizaj notes Cirrus considers the tuning speaker-specific, so keep the volume moderate.

**Sound card fails to appear on some boots.** Issue [#10987](https://github.com/omacom/omarchy/issues/10987) reports roughly half of boots ending in `sof_sdw: ASoC: failed to instantiate card -16`, a probe race between the two SPI amps, leaving PipeWire with Dummy Output only. Unbinding and rebinding `sof_sdw` recovers it for that boot.

**Panel Replay judder.** The 120 Hz panel negotiates Panel Replay Selective Update, and its wake path drops frames in multiples of the refresh period. Scrolling and the mouse cursor stutter. Issue [#6853](https://github.com/omacom/omarchy/issues/6853) has the diagnosis and the one line fix, `xe.enable_psr=0 xe.enable_panel_replay=0`. The pull request that would ship it, [#6849](https://github.com/omacom/omarchy/pull/6849), was still open when this page was checked, so 4.0.4 does not apply it for you.

**Suspend on the 4.0.4 kernel.** Version 4.0.4 makes `linux-omarchy` the default boot entry for everyone. Issue [#12190](https://github.com/omacom/omarchy/issues/12190) reports `linux-omarchy 7.2.5-3` wedging on lid close on this model, backlight on and input dead, four forced power cycles in a day, while the stock kernel on the same command line suspends fine. It is one reporter so far, filed the day this page was written.

**Wi-Fi on the Intel BE213 card.** Issue [#6551](https://github.com/omacom/omarchy/issues/6551) shows `iwlwifi` finding no acceptable `bz-b0-wh-b0` ucode because the install media carries `linux-firmware 20260410-1`. With no wired port, that is a fresh install with zero network. The reporter fixed it by sideloading `linux-firmware-intel` and a newer kernel with `pacman -U`. Note that a normal update left `linux-firmware-intel` behind on the old version.

## What Omarchy does for this model

Match strings come from `omarchy-hw-match`, which greps `/sys/class/dmi/id/product_name` and `product_family` case-insensitively.

- `omarchy-hw-dell-xps-haptic-touchpad` matches `XPS` plus the presence of `/sys/bus/i2c/devices/i2c-VEN_06CB:00`, and `install/hardware/dell-xps-touchpad-haptics.sh` then installs `dell-xps-touchpad-haptics`, version 1.0.0-3 in the stable channel.
- `install/user/hardware/dell/xps13-text-scaling.sh` matches `DX13260` and sets the text size.
- `omarchy-hw-dell-xps-oled` requires Panther Lake graphics and an LG OLED EDID, so it does not fire on the IPS DX13260.
- `install/hardware/intel/fix-wifi7-eht.sh` disables Wi-Fi 7 only for PCI ids `8086:e440` and `8086:272b`, the BE200 and BE211 in the XPS 14 and 16. The BE213 in the XPS 13 is `8086:4d40` and is not covered.
- The shipped speaker tuning `dell-xps-2026` matches DMI SKUs `0DB9` and `0DBA`, which are the XPS 14 and XPS 16. There is no tuning for the XPS 13. Check yours with `omarchy audio tuning status`.
- `dell-xps13-sidecar-amps` exists in the Omarchy repo at 1.0.0-2, but no install script adds it. On kernel 7.2 and newer it is a no-op, because upstream commit `efd80de2de9d` already sets the sidecar quirk for `1028:0e53`.

## Variants

The 2026 DX13260 comes in at least two speaker SKUs, `0E53` and `0E54`. Neither is currently safe for speaker audio. Read your own with `cat /sys/class/dmi/id/product_sku`.

Older XPS 13 models avoid the Cirrus problem but bring their own. The XPS 13 Plus 9315 is Alder Lake with an IPU6 camera, and Omarchy's camera detection only covers IPU7, so nothing is installed and the webcam stays dark, per [#9879](https://github.com/omacom/omarchy/issues/9879). The Lunar Lake XPS 13 9350 gets `intel-ipu7-camera` by detection, but that package is built for Panther Lake only, so the HAL plugin its IPU needs does not exist, per [#12178](https://github.com/omacom/omarchy/issues/12178). Fingerprint readers on Dell laptops are often Goodix parts with no open libfprint driver, described in [#7991](https://github.com/omacom/omarchy/issues/7991). We have no confirmed fingerprint report for the DX13260 either way.

If you are buying new for Omarchy, the XPS 14 and 16 have the speaker tuning, the Wi-Fi 7 workaround and the camera enablement that the 13 does not.

## Before you install

- Have a USB Ethernet adapter or phone tethering ready in case Wi-Fi does not come up.
- Record your SKU and audio subsystem id before you change anything: `cat /sys/class/dmi/id/product_sku` and `lspci -nn | grep -i audio`.
- After the first boot, run `journalctl -b -k | grep cs35l56` and look for `FIRMWARE_MISSING` and the `system name:` line, which tells you which spkid your unit asks for.
- Expect to keep the stock `linux` entry available in the boot menu while [#12190](https://github.com/omacom/omarchy/issues/12190) is open. See [system sleep](https://omarchy.org/manual/system-sleep/) in the manual.
- If scrolling judders, try the Panel Replay kernel parameters from [#6853](https://github.com/omacom/omarchy/issues/6853) yourself, since Omarchy does not apply them.
- All of the above was checked against 4.0.4 on the 4.x line. None of these issues predate Quattro in any report we found, and the 3.x reports on this model, such as [#1868](https://github.com/omacom/omarchy/issues/1868), are older XPS 13 units with unrelated audio routing problems.

## Related

Component pages: [audio](/hardware/audio/), [wifi](/hardware/wifi/), [suspend and sleep](/hardware/suspend-sleep/), [webcam](/hardware/webcam/), [touchpad and input](/hardware/touchpad-input/), [intel gpu](/hardware/intel-gpu/). Fix pages: [no sound from laptop speakers](/fix/no-sound-from-laptop-speakers/), [suspend will not resume](/fix/suspend-wont-resume-s2idle/), [webcam not detected](/fix/webcam-not-detected/). Sibling model: [Dell XPS 14](/hardware/dell-xps-14-2026/). Report your own unit at [hardware submit](/hardware/submit/).
