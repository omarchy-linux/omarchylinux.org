---
title: "Dell Latitude on Omarchy Linux"
description: "Dell Latitude hardware support on Omarchy 4.x: Intel graphics and Wi-Fi work, ControlVault fingerprint readers are undetected, and Bluetooth off can drop the radio."
answer: "Most Latitudes run Omarchy fine on the generic Intel path. Rate it silver. Wi-Fi (iwlwifi), Intel graphics and the display work; the fingerprint reader does not if your Latitude has a Broadcom ControlVault 3, because Omarchy never looks for vendor 0a5c. Turning Bluetooth off can remove the radio from the bus. Omarchy ships no Latitude-specific enablement at all."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [dell, latitude, laptop, fingerprint, intel, bluetooth]
kind: model
vendor: "Dell"
model: "Dell Latitude"
dmi: ["Latitude 3380", "Latitude 5320", "Latitude 5420", "Latitude 5430", "Latitude 5431", "Latitude 5490", "Latitude 5521", "Latitude 7420", "Latitude 7430", "Latitude 7440", "Latitude 7450", "Latitude E5470", "Latitude E7490"]
cpu: "Intel Core, Skylake through Raptor Lake in the reported machines"
gpu: "Intel integrated (HD 530, Iris Xe, UHD)"
rating: silver
subsystems:
  wifi: partial
  bluetooth: partial
  audio: unknown
  webcam: unknown
  fingerprint: partial
  gpu: works
  suspend: unknown
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: unknown
quirkScripts: []
issueCount: 22
sources:
  - url: "https://github.com/omacom/omarchy/issues/9507"
    title: "Issue #9507: omarchy-hw-fingerprint doesn't detect Dell ControlVault 3 (Broadcom BCM58200, vendor 0a5c)"
    kind: issue
    author: "JeronimoColon"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/7662"
    title: "Issue #7662: Fingerprint setup misses Broadcom BCM58200 ControlVault 3 (vendor 0a5c not in detection list)"
    kind: issue
    author: "bartcho"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/pull/9524"
    title: "PR #9524: Detect Broadcom ControlVault 3 fingerprint readers"
    kind: pr
    author: "qybaihe"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/8486"
    title: "PR #8486: Detect Broadcom fingerprint readers by vendor ID"
    kind: pr
    author: "gbillium143"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/7323"
    title: "Issue #7323: Quattro upgrade removes iwd but leaves wifi.backend=iwd in NetworkManager conf.d"
    kind: issue
    author: "skoom21"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7326"
    title: "Issue #7326: Internal monitor position cannot be made to stick"
    kind: issue
    author: "skoom21"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7936"
    title: "Issue #7936: omarchy-bluetooth-power off: type-wide rfkill block trips platform switches and removes the radio from the USB bus (ThinkPad/Dell)"
    kind: issue
    author: "DrakeMorrison"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6956"
    title: "Issue #6956: Bluetooth widget disappears from shell when turned off"
    kind: issue
    author: "elytraVIII"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/2947"
    title: "Issue #2947: Live ISO freezes on systems with Intel i915 GPU"
    kind: issue
    author: "h4r0n1"
    date: "2025-10-28"
  - url: "https://github.com/omacom/omarchy/issues/3644"
    title: "Issue #3644: Omarchy can't connect to different wifi networks"
    kind: issue
    author: "Amit4218"
    date: "2025-11-27"
  - url: "https://github.com/omacom/omarchy/issues/2619"
    title: "Issue #2619: Omarchy takes long time during boot except hammering keyboard randomly"
    kind: issue
    author: "xianlin"
    date: "2025-10-20"
  - url: "https://github.com/omacom/omarchy/issues/1610"
    title: "Issue #1610: Intel Iris Xe on Arch feels laggy"
    kind: issue
    author: "atiqullahsadeqi"
    date: "2025-09-11"
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy Manual: Hardware authentication"
    kind: manual
credits:
  - name: "JeronimoColon"
    url: "https://github.com/JeronimoColon"
    for: "Traced ControlVault 3 detection on a Latitude 5420 and found the libfprint-tod conflict in the 4.0.3 setup script"
  - name: "bartcho"
    url: "https://github.com/bartcho"
    for: "First report that vendor 0a5c is missing from the fingerprint allowlist"
  - name: "skoom21"
    url: "https://github.com/skoom21"
    for: "Wi-Fi backend and monitor position reports from a Latitude E5470 on 4.0.0"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Root-caused the Bluetooth rfkill behaviour on Dell and ThinkPad platform switches"
faq:
  - q: "Does the fingerprint reader work on a Dell Latitude?"
    a: "Only if it is not a Broadcom ControlVault. Omarchy's reader detection allowlist has no entry for Broadcom vendor 0a5c as of 4.0.4, so Setup > Security > Fingerprint exits with \"No fingerprint sensor detected\" on Latitudes that carry a ControlVault 3 (USB 0a5c:5843)."
  - q: "Is a used Latitude a reasonable machine to buy for Omarchy?"
    a: "Yes, if you pick an Intel Wi-Fi model and do not need the fingerprint reader. Reports cover machines from the 2016 E5470 through the 7450, and the Intel graphics and iwlwifi path is the one Omarchy exercises most."
  - q: "Why did Wi-Fi stop after I upgraded my Latitude to Quattro?"
    a: "The upgrade removes iwd but can leave /etc/NetworkManager/conf.d/wifi_backend.conf pointing at it, so every Wi-Fi device sits at unavailable. Delete or correct that file and restart NetworkManager."
related: [fingerprint-enrollment-fails, bluetooth-stops-after-resume, multi-monitor-layout-not-saved, wifi-drops-after-kernel-update-iwlwifi]
draft: false
---

## Verdict

Silver. A Dell Latitude installs and runs Omarchy on the generic Intel laptop path, and the tracker shows machines from a 2016 E5470 up to a 7450 doing exactly that. Nothing in the Omarchy tree is written for this line, so what you get is whatever the kernel and the generic Intel enablement give you. That is usually enough.

Two things pull it off gold. Fingerprint readers on ControlVault models are not detected at all, and turning Bluetooth off through the shell can take the radio off the bus entirely. Both are open on 4.0.4.

Evidence here is broader than it is deep. Twenty-two issues touch a Latitude across 3.x and 4.x, but most are generic Omarchy bugs that happened to be filed from one. The Latitude-specific findings below are the ones where the reporter's hardware is actually the cause.

## What works

Intel graphics. Latitudes running 4.0.0 with an internal panel plus an external HDMI display show up in bug reports doing ordinary Hyprland work, including the E5470 with HD 530 in [#7326](https://github.com/omacom/omarchy/issues/7326). An older performance complaint about Iris Xe on a 7420 ([#1610](https://github.com/omacom/omarchy/issues/1610)) was closed the same day and never established a defect.

Intel Wi-Fi. The kernel side is clean. The E5470 report in [#7323](https://github.com/omacom/omarchy/issues/7323) includes a full `iwlwifi` log for a Dual Band Wireless-AC 8260: firmware loaded, MAC detected, no rfkill block, zero driver errors. When Wi-Fi breaks on a Latitude it has so far been NetworkManager configuration, not the radio.

Installation. The reports come from installed, updated systems, which is itself evidence that the installer handles these machines.

Everything else on the checklist is unknown rather than confirmed. No one has filed a Latitude audio, webcam, battery, hibernate or keyboard bug, and an empty tracker is not a test result. Treat audio and webcam as untested here, not as working.

## What breaks

**Fingerprint on ControlVault models.** This is the clearest Latitude problem. `omarchy-hw-fingerprint` matches a USB product string or a vendor allowlist. In 4.0.4 that list is `27c6 138a 06cb 08ff 1c7a 147e`. A Dell ControlVault 3 is Broadcom `0a5c:5843` and reports its product string as just `58200`, so it matches neither test and `Setup > Security > Fingerprint` bails out before it installs anything. Reported independently by bartcho in [#7662](https://github.com/omacom/omarchy/issues/7662) and by JeronimoColon on a Latitude 5420 in [#9507](https://github.com/omacom/omarchy/issues/9507). Two competing pull requests are open and unmerged, [#9524](https://github.com/omacom/omarchy/pull/9524) (match the exact USB ID) and [#8486](https://github.com/omacom/omarchy/pull/8486) (allowlist the vendor).

There is a second trap behind it. Since 4.0.3 the setup script installs `libfprint-git`, which conflicts with `libfprint`, and it passes `--ask 4` so pacman accepts the conflict without prompting. ControlVault readers need `libfprint-tod` plus Dell's `libfprint-2-tod1-broadcom` driver, which also provides `libfprint`. JeronimoColon's follow-up notes that fixing detection alone would let the wizard swap the working TOD stack for an upstream build with no driver for the reader. Do not run the fingerprint wizard on a ControlVault machine even after detection is fixed, unless you have checked what it will do to your packages.

**Bluetooth off removes the radio.** `omarchy-bluetooth-power off` issues a type-wide `rfkill block bluetooth`. On Dells the `dell-laptop` platform switch is blocked along with the adapter, and the embedded controller answers by cutting USB power to the module, so `hci0` disappears instead of going unpowered. DrakeMorrison traced this in [#7936](https://github.com/omacom/omarchy/issues/7936) and notes that a Latitude 7440 report on [#6956](https://github.com/omacom/omarchy/issues/6956) describes hardware where even `rfkill unblock bluetooth` does not bring the radio back, and only a suspend and resume cycle or a reboot does. The bar widget vanishes with the adapter, so there is no UI route back. Open on 4.0.4.

**Wi-Fi dead after upgrading to Quattro.** On skoom21's E5470, the 4.0.0 upgrade removed the `iwd` package but left `/etc/NetworkManager/conf.d/wifi_backend.conf` still selecting `wifi.backend=iwd`. NetworkManager then points at a daemon that no longer exists and every Wi-Fi device sits at `unavailable` forever, with nothing in the UI explaining why. The one migration that touches iwd-era breakage, `migrations/1786567036.sh`, exits immediately unless `wpa_supplicant.service` is masked, which it was not here. Check that file before you blame the card.

**Monitor layout does not stick.** Also from the E5470: an explicit position for the internal panel is re-applied as `position = "auto"` within about a second, by the clamshell watcher and by the Display panel's scaling path ([#7326](https://github.com/omacom/omarchy/issues/7326)). This is not Latitude-specific, it affects any laptop with an external monitor, but it is what a docked Latitude owner hits first.

**Live ISO freeze on i915.** One report, [#2947](https://github.com/omacom/omarchy/issues/2947), from a Latitude E7490 with an i7-8650U: the live ISO freezes in early boot, which the reporter attributes to i915 power saving. It is open, has no comments, and no one has reproduced it. Thin evidence, but worth knowing if your install stalls at the same point.

## What Omarchy does for this model

Nothing specific. As of 4.0.4 no shipped script calls `omarchy-hw-match` with a Latitude or a Dell-family pattern. The only Dell matches in the tree are `XPS` (OLED handling and haptic touchpad) and the `DX13260` SKU used by the 2026 XPS 13 text-scaling and audio paths. There is no `install/hardware/dell/` directory beyond the XPS touchpad script, and no Latitude speaker tuning.

What a Latitude actually gets is the generic run in `install/hardware/all.sh`: Intel video acceleration, `lpmd`, `thermald`, SOF firmware, the wireless regdom, the F-key fix, the Synaptics touchpad fix and the Bluetooth setup. `omarchy-hw-laptop` picks the machine up from its ACPI lid switch, and `omarchy-hw-intel` from the CPU vendor string. That is the whole of it.

## Variants

Prefer a 5000 or 7000 series unit from 2020 onward with an Intel AX-series card. Those are the configurations the reports come from, and they sit on the best-exercised driver path in Omarchy.

Check the fingerprint reader before you count on it. Run `lsusb` on the machine and look for `0a5c`. If it is a Broadcom ControlVault, the Omarchy wizard will not see it on 4.0.4. Latitudes with a Goodix (`27c6`) or Validity/Synaptics (`138a`, `06cb`) reader are inside the allowlist, though no Latitude report confirms enrollment on one.

Older E-series units (E5470, E7490) are usable but carry the two oldest open problems on this page, the ISO freeze and the low-resolution multi-monitor grief. A 1366x768 panel also fights Omarchy's default assumption of a 2x display, covered in the [Monitors chapter](https://omarchy.org/manual/monitors/).

No AMD Latitude report exists in the data. If you have one, that configuration is untested here.

## Before you install

- Run `lsusb | grep -i 0a5c` from the live ISO. A hit means the fingerprint reader will not be detected.
- Check `/etc/NetworkManager/conf.d/` after any 3.x to 4.x upgrade and remove a `wifi_backend.conf` that still names iwd.
- Leave Bluetooth on rather than toggling it off from the bar, until [#7936](https://github.com/omacom/omarchy/issues/7936) lands.
- Have a wired connection or a phone tether available for the first boot after upgrading.
- If the live ISO freezes early, that is [#2947](https://github.com/omacom/omarchy/issues/2947) and not your disk.

## Related

- [Fingerprint enrollment fails](/fix/fingerprint-enrollment-fails/)
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [Fingerprint readers](/hardware/fingerprint/) and [Bluetooth](/hardware/bluetooth/)
- [Upgrading 3 to 4 (Quattro)](/upgrade/3-to-4-quattro/)
- [Submit your hardware report](/hardware/submit/)
