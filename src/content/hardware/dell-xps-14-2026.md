---
title: "Dell XPS 14 and XPS 16 (2026, Panther Lake) on Omarchy"
description: "Dell XPS 14 DA14260 and XPS 16 DA16260 on Omarchy 4.0.4: the enablement Omarchy ships, plus the open backlight, camera and Wi-Fi quirks."
answer: "Silver. The 2026 XPS 14 (DA14260) and XPS 16 (DA16260) are the Panther Lake machines Omarchy enables first: haptic trackpad package, IPU7 camera stack, a shipped speaker tuning and a Wi-Fi workaround all match on them. Expect real open bugs anyway: OLED backlight needs xe.enable_dpcd_backlight=1, Panel Replay causes desktop lag, and Wi-Fi 7 is disabled on purpose."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: partial
kind: model
vendor: "Dell"
model: "XPS 14 / XPS 16 (2026, Panther Lake)"
dmi: ["DA14260", "DA16260", "XPS 14", "XPS 16"]
year: "2026"
cpu: "Intel Core Ultra X7 358H (Panther Lake)"
gpu: "Intel Arc B390 (xe, 8086:b080)"
rating: silver
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: partial
  webcam: partial
  fingerprint: unknown
  gpu: works
  suspend: partial
  hibernate: unknown
  touchpad: works
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "install/hardware/dell-xps-touchpad-haptics.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/dell-xps-touchpad-haptics.sh"
    note: "Installs dell-xps-touchpad-haptics when omarchy-hw-dell-xps-haptic-touchpad matches."
  - name: "bin/omarchy-hw-dell-xps-haptic-touchpad"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-haptic-touchpad"
    note: "Matches DMI XPS plus the i2c-VEN_06CB:00 Synaptics haptic device."
  - name: "bin/omarchy-hw-dell-xps-oled"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-oled"
    note: "Matches XPS with the LG OLED eDP panel (EDID bytes 30e4) on Panther Lake. Nothing in the v4.0.4 install tree calls it yet."
  - name: "install/hardware/intel/fix-wifi7-eht.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fix-wifi7-eht.sh"
    note: "Writes options iwlwifi disable_11be=Y for BE200/BE211 (8086:e440, 8086:272b)."
  - name: "install/hardware/intel/ipu7-camera.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    note: "Installs intel-ipu7-camera when an OVTI08F4 ACPI device is present."
  - name: "install/hardware/intel/fred.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fred.sh"
    note: "Adds fred=on to the Limine cmdline on any Panther Lake GPU."
  - name: "default/audio/tunings/dell-xps-2026/tuning.conf"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/audio/tunings/dell-xps-2026/tuning.conf"
    note: "PipeWire filter chain for the internal speakers, matched on SKU 0DB9 (XPS 14) and 0DBA (XPS 16)."
issueCount: 23
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [dell, xps, panther-lake, intel, laptop, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/audio/tunings/dell-xps-2026/tuning.conf"
    title: "default/audio/tunings/dell-xps-2026/tuning.conf at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fix-wifi7-eht.sh"
    title: "install/hardware/intel/fix-wifi7-eht.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    title: "install/hardware/intel/ipu7-camera.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-dell-xps-oled"
    title: "bin/omarchy-hw-dell-xps-oled at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1789325478.sh"
    title: "migrations/1789325478.sh at v4.0.4 (install linux-omarchy and reorder Limine)"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.3/install/hardware/intel/ptl-kernel.sh"
    title: "install/hardware/intel/ptl-kernel.sh at v4.0.3 (linux-ptl for XPS Panther Lake)"
    kind: commit
  - url: "https://github.com/omacom/omarchy/issues/6676"
    title: "Issue #6676: Brightness control does nothing on Dell XPS 14 OLED (Panther Lake, xe)"
    kind: issue
    author: "nille"
    date: "2026-08-10"
  - url: "https://github.com/omacom/omarchy/issues/11646"
    title: "Issue #11646: Display backlight non-functional on Dell XPS Panther Lake, needs xe.enable_dpcd_backlight=1"
    kind: issue
    author: "RodriMora"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/12188"
    title: "Issue #12188: linux-omarchy kernel breaks screen backlight and USB audio volume on Dell XPS 14"
    kind: issue
    author: "cthybert"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11016"
    title: "Issue #11016: Panel Replay desktop lag on Dell XPS 14 after 4.0.3 update"
    kind: issue
    author: "rbulcher"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10948"
    title: "Issue #10948: linux-ptl 7.2.3 IPU7 / OV08X40 sensor missing from media graph on XPS 14 DA14260"
    kind: issue
    author: "milep"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10837"
    title: "Issue #10837: RC jsoncpp 1.9.8 soname bump breaks intel-ipu7-camera 1.0.5"
    kind: issue
    author: "iuliansafta"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/8641"
    title: "Issue #8641: XPS 14 Windows Hello IR camera (Himax HM1092) has no Linux driver"
    kind: issue
    author: "jorgemanrubia"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/10010"
    title: "Issue #10010: SoundWire bus clash/parity errors cause speaker dropout on Dell XPS 14 2026"
    kind: issue
    author: "vitillo"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/9922"
    title: "Issue #9922: Dell XPS 14 DA14260 closing lid causes severe Wi-Fi TX stall while docked"
    kind: issue
    author: "esemczak"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/10690"
    title: "Issue #10690: USB-C / Thunderbolt power blip reports lid-close while lid is open and instantly suspends"
    kind: issue
    author: "bjcatar"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7109"
    title: "Issue #7109: Wi-Fi 7 is disabled on every Core Ultra Series 3 laptop and every BE200 card"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/5827"
    title: "Issue #5827: linux-ptl iwlwifi skbuff runaway OOM under wlan0 TX load on Dell XPS Panther Lake"
    kind: issue
    author: "berenddeboer"
    date: "2026-05-15"
  - url: "https://github.com/omacom/omarchy/issues/5953"
    title: "Issue #5953: Dell XPS 14 DA14260 periodic hard reset after unplugging"
    kind: issue
    author: "rblalock"
    date: "2026-05-23"
  - url: "https://github.com/omacom/omarchy/issues/6114"
    title: "Issue #6114: XPS 16 DA16260 capacitive function row emits no key events"
    kind: issue
    author: "kaptivkapital"
    date: "2026-06-19"
  - url: "https://github.com/omacom/omarchy/issues/7206"
    title: "Issue #7206: No sound after reboot with headphones plugged in (Dell XPS 16 / cs42l45)"
    kind: issue
    author: "kafatekactual"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/11176"
    title: "Issue #11176: XPS 16 DA16260 internal panel stays black with xe PSR timeouts"
    kind: issue
    author: "klaudworks"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/12207"
    title: "Issue #12207: USB4 monitor EDID read fails on about half of hotplugs, display stuck at 640x480"
    kind: issue
    author: "diazkev314"
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/10154"
    title: "Issue #10154: ptl-kernel.sh never removes the stock kernel"
    kind: issue
    author: "Faxulous"
    date: "2026-09-04"
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, mouse and trackpad"
    kind: manual
credits:
  - name: "nille"
    url: "https://github.com/nille"
    for: "Read the DPCD registers under both backlight modes and showed that only xe.enable_dpcd_backlight=1 makes the OLED panel act on brightness writes"
  - name: "RodriMora"
    url: "https://github.com/RodriMora"
    for: "Showed the backlight failure is a per-boot race by tracking max_brightness across boots"
  - name: "rbulcher"
    url: "https://github.com/rbulcher"
    for: "Bisected the post-4.0.3 desktop lag to Panel Replay by booting old and new kernels on the same userspace"
  - name: "jorgemanrubia"
    url: "https://github.com/jorgemanrubia"
    for: "Traced the dead Windows Hello IR camera to a missing HM1092 driver and attempted one"
  - name: "esemczak"
    url: "https://github.com/esemczak"
    for: "Isolated the docked Wi-Fi stall to physical lid state rather than suspend"
faq:
  - q: "Is the 2026 XPS 14 a good laptop to buy for Omarchy?"
    a: "It is one of the best supported Panther Lake machines because Omarchy ships model specific enablement for it, but it is not trouble free on 4.0.4. Prefer the 1920x1200 IPS panel if you want brightness control to work without a kernel flag."
  - q: "Do I still need the linux-ptl kernel?"
    a: "No. 4.0.3 and earlier installed linux-ptl on XPS Panther Lake machines. 4.0.4 installs linux-omarchy for everyone and makes it the first Limine entry, leaving the old kernel installed so you can still select it at boot."
  - q: "Why is my Wi-Fi 7 card only giving me Wi-Fi 6 speeds?"
    a: "Omarchy writes /etc/modprobe.d/iwlwifi-disable-eht.conf on any machine with an Intel BE200 or BE211 card because the iwlwifi EHT receive path drops rates. Delete that file and reboot to test EHT yourself."
  - q: "Does the fingerprint reader work?"
    a: "No report in the tracker confirms enrollment on the 2026 XPS 14 or 16 either way, so this page leaves it unknown. Run Setup then Security then Fingerprint and report back."
related: [dell-xps-13-2026, intel-gpu, webcam, wifi, multi-monitor]
draft: false
---

The Dell XPS 14 (DA14260) and XPS 16 (DA16260) from 2026 are the Panther Lake laptops Omarchy targets by name. Both carry the Core Ultra X7 358H, an Intel Arc B390 iGPU on the `xe` driver, an Intel BE211 Wi-Fi card, a Synaptics haptic trackpad, four Cirrus `cs35l56` speaker amps and an IPU7 camera with an OV08X40 sensor. Everything below was checked against the v4.0.4 source tree and against issues open on 16 September 2026.

## Verdict

Silver. Not gold, and the gap is mostly the display.

Omarchy carries more code for this machine than for almost any other laptop: a haptic trackpad package, an IPU7 camera package, a measured speaker tuning, a Wi-Fi workaround and, until 4.0.3, a dedicated kernel. All of that works. What keeps it off gold is a set of open display and camera bugs that a buyer will meet in the first week. Brightness control is dead on some boots and permanently dead on the OLED panel unless you add a kernel flag yourself (issues [#6676](https://github.com/omacom/omarchy/issues/6676) and [#11646](https://github.com/omacom/omarchy/issues/11646)). Panel Replay makes the desktop feel sluggish on kernels from 7.2.3 onward ([#11016](https://github.com/omacom/omarchy/issues/11016)). The camera stack has broken twice in a month. Wi-Fi 7 is switched off on purpose.

If you want the smoothest version of this laptop today, buy the IPS panel, not the OLED.

## What works

The trackpad, including haptic click strength, which Omarchy exposes under Trigger then Hardware then Touchpad Haptics ([manual](https://omarchy.org/manual/keyboard-mouse-trackpad/)). The iGPU, with the `xe` driver and hardware video acceleration installed by the Intel path. Internal speakers, with a shipped filter chain that the project measured on an XPS 14 and validated on 24 July 2026. Wi-Fi associates and runs, at Wi-Fi 6 rates. The RGB webcam works once `intel-ipu7-camera` is installed and the relay is running, which the installer does automatically when it sees the `OVTI08F4` ACPI device.

Suspend works in the ordinary case: reports on this machine are about spurious suspends and docked behaviour, not about failing to resume.

## What breaks

**Backlight on the OLED panel.** On the 2880x1800 LG OLED unit, `brightnessctl` and the sysfs value both change and the panel does not. nille read the DPCD registers under both modes and found the panel only acts on brightness under `xe.enable_dpcd_backlight=1`; the kernel's own suggestion of `=3` is wrong twice, since the driver here is `xe` and not `i915` and that value forces an interface the panel ignores ([#6676](https://github.com/omacom/omarchy/issues/6676)). RodriMora later showed the same failure is nondeterministic on other units: broken boots expose `max_brightness=192000`, healthy ones `512` ([#11646](https://github.com/omacom/omarchy/issues/11646)). Omarchy already ships this exact fix for two ASUS Panther Lake models, and ships an `omarchy-hw-dell-xps-oled` predicate that detects the affected panel by EDID, but nothing in the v4.0.4 install tree calls that predicate yet.

**The 4.0.4 kernel switch.** 4.0.3 and earlier installed `linux-ptl` on XPS Panther Lake machines and pinned it first in Limine. 4.0.4 installs `linux-omarchy` for everyone and rewrites `BOOT_ORDER`, explicitly overriding the old Dell drop-in. One report against 7.2.5-3 says brightness keys and USB audio volume both regress against stock `linux` 7.2.3 and recover when the older entry is picked from the Limine menu ([#12188](https://github.com/omacom/omarchy/issues/12188)). This is one report, filed the day after release, so treat it as a lead rather than a rule.

**Panel Replay lag.** rbulcher compared kernels on identical userspace and found 7.1.8 smooth and 7.2.3 sluggish, with the lag switching off and on live as Panel Replay is disabled and re-enabled. Booting with `xe.enable_panel_replay=0` restored smooth motion ([#11016](https://github.com/omacom/omarchy/issues/11016)).

**Camera fragility.** The IPU7 path broke twice in September: a `jsoncpp` soname bump left the Intel HAL plugin linked against a library that no longer exists ([#10837](https://github.com/omacom/omarchy/issues/10837), still open, though stable now carries `intel-ipu7-camera` 1.0.6), and the 7.2.3 kernel moved the CVS bridge in tree so the sensor vanished from the media graph ([#10948](https://github.com/omacom/omarchy/issues/10948), closed 13 September). The 4.0.4 notes credit a webcam fix on XPS systems for the 7.2.x kernel. The Windows Hello IR camera is a separate matter: the Himax HM1092 has no Linux driver anywhere, so IR face unlock does not exist on this machine ([#8641](https://github.com/omacom/omarchy/issues/8641)).

**Wi-Fi.** `fix-wifi7-eht.sh` disables 802.11be on any BE200 or BE211 card, which is every Panther Lake laptop rather than just the XPS this was written for ([#7109](https://github.com/omacom/omarchy/issues/7109)). Two harder Wi-Fi reports exist and are unresolved: a TX stall whenever the lid is physically closed while docked ([#9922](https://github.com/omacom/omarchy/issues/9922)) and an `iwlwifi` memory storm under sustained upload on the older `linux-ptl` builds ([#5827](https://github.com/omacom/omarchy/issues/5827)).

**Suspend and power.** A USB-C power blip can report a lid close while the lid is open, suspending the session instantly ([#10690](https://github.com/omacom/omarchy/issues/10690)). One owner sees roughly weekly hard resets after unplugging, with a Dell power-button blink code ([#5953](https://github.com/omacom/omarchy/issues/5953)); that one has no second report and may be a firmware fault on a single unit.

**Audio edge cases.** Intermittent one-sided speaker dropout on the XPS 14 traced to SoundWire bus clash and parity errors on one of the two links, and was sent upstream to the SOF project ([#10010](https://github.com/omacom/omarchy/issues/10010)).

## What Omarchy does for this model

At install time, on a machine matching DMI `XPS` and a Panther Lake GPU:

- `dell-xps-touchpad-haptics` is installed when the Synaptics haptic device at `i2c-VEN_06CB:00` is present.
- `intel-ipu7-camera` is installed when an `OVTI08F4` ACPI device is present.
- `fred=on` is added to the Limine cmdline for every Panther Lake GPU.
- `/etc/modprobe.d/iwlwifi-disable-eht.conf` is written for BE200 and BE211 cards.
- The speaker tuning is enabled when the DMI SKU is `0DB9` (XPS 14) or `0DBA` (XPS 16), pulling in `lsp-plugins-lv2` for its limiter.

The tuning is matched on SKU rather than a marketing name, so it cannot widen to the rest of the XPS line. Its own notes say the XPS 16 profile is included on report rather than measurement.

## Variants

Prefer the 1920x1200 IPS panel. The 2880x1800 OLED is the one with the backlight problem, and you can identify it by EDID bytes reading `30e4`. The XPS 16 shares the enablement but adds its own open bugs: the capacitive function row emits no key events at all, since the HID device exposes only pointer usages ([#6114](https://github.com/omacom/omarchy/issues/6114)), the internal panel can go black with `xe` PSR timeouts ([#11176](https://github.com/omacom/omarchy/issues/11176)), a USB4 monitor's EDID read fails on about half of hotplugs ([#12207](https://github.com/omacom/omarchy/issues/12207)), and rebooting with headphones already plugged in leaves everything silent until you cycle the jack ([#7206](https://github.com/omacom/omarchy/issues/7206)). The 2026 XPS 13 (DX13260) is a different machine with a different and worse audio story; see [the XPS 13 page](/hardware/dell-xps-13-2026/).

## Before you install

- Update the Dell BIOS first. Reports on these machines span 1.2.1 to 1.10.1, and several owners updated during triage.
- Decide your panel. If you bought the OLED, expect to add `xe.enable_dpcd_backlight=1` through a Limine drop-in yourself.
- Know your kernel. After 4.0.4 you boot `linux-omarchy`; the previous kernel stays installed, so the Limine menu is your first test when something regresses. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).
- If the desktop feels sluggish at 120 Hz, try `xe.enable_panel_replay=0` before blaming Hyprland.
- If Wi-Fi tops out around Wi-Fi 6 rates, that is deliberate. The file to remove is named in the Wi-Fi section above.
- Fingerprint, Bluetooth, hibernate and battery life on these units are unverified here. Nothing in the tracker proves them working, and the tracker only proves what is broken.

## Related

[Intel graphics](/hardware/intel-gpu/), [webcams](/hardware/webcam/), [Wi-Fi](/hardware/wifi/), [multi-monitor](/hardware/multi-monitor/), [suspend and sleep](/hardware/suspend-sleep/), [no sound from laptop speakers](/fix/no-sound-from-laptop-speakers/), [fractional scaling](/fix/fractional-scaling-blurry-or-huge-apps/), [submit your hardware report](/hardware/submit/).
