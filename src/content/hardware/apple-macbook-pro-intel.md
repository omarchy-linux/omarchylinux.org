---
title: "Intel MacBook Pro (2016-2020) on Omarchy"
description: "Intel MacBook Pro 2016-2020 on Omarchy 4.0.4: T2 models are supported and mostly work, 2016-2017 T1 models lose the Touch Bar and audio."
answer: "Bronze, and it depends hard on the year. 2018-2020 T2 MacBook Pros are officially supported: Omarchy installs linux-t2, Apple Wi-Fi/Bluetooth firmware and fan control automatically, and most things work. 2016-2017 T1 models are worse: the installer wipes the Apple EFI payload the Touch Bar and camera need, speaker audio is broken, and the 15-inch fails to boot the 4.0.4 kernel without intel_iommu=off."
appliesTo:
  from: "3.0.0"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Apple"
model: "MacBook Pro (Intel)"
dmi: ["MacBookPro13,1", "MacBookPro13,2", "MacBookPro13,3", "MacBookPro14,1", "MacBookPro14,2", "MacBookPro14,3", "MacBookPro15,1", "MacBookPro15,2", "MacBookPro15,4", "MacBookPro16,1", "MacBookPro16,3"]
cpu: "Intel Core i5/i7/i9, Skylake through Ice Lake and Coffee Lake Refresh"
gpu: "Intel HD/Iris/Iris Plus, plus AMD Radeon Pro on the 15-inch and 16-inch"
year: "2016 to 2020"
rating: bronze
subsystems:
  wifi: partial
  bluetooth: partial
  audio: partial
  webcam: partial
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: partial
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "fix-t2.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-t2.sh"
    note: "Fires when lspci finds the T2 chip (106b:1801 or 106b:1802). Installs linux-t2, linux-t2-headers, apple-t2-audio-config, apple-bcm-firmware and t2fanrd, loads t2bce_vhci and hci_bcm4377, adds t2bce_vhci and the HID/xHCI modules to the initramfs, writes a two-fan t2fand.conf, and appends intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep to the Limine kernel command line."
  - name: "fix-spi-keyboard.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-spi-keyboard.sh"
    note: "Matches DMI product_name against MacBook8,1 / MacBook10,1 / MacBook12,1 / MacBookPro13,1-3 / MacBookPro14,1-3. Installs macbook12-spi-driver-dkms and puts applespi, intel_lpss_pci and spi_pxa2xx_platform in the initramfs so the built-in keyboard works at the LUKS prompt."
  - name: "fix-suspend-nvme.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-suspend-nvme.sh"
    note: "Same DMI match. Installs a systemd unit that clears d3cold_allowed on the NVMe device at 0000:01:00.0 so the SSD survives resume."
  - name: "fix-brcmfmac-supplicant.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-brcmfmac-supplicant.sh"
    note: "Writes options brcmfmac feature_disable=0x82000 on any Apple machine with a brcmfmac chip ID in its list, or with the T2 PCI ID. Moves the WPA four-way handshake back into wpa_supplicant."
issueCount: 78
tags: [apple, macbook-pro, t2-mac, intel, laptop, hardware]
sources:
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12119"
    title: "Issue #12119: linux-omarchy 7.2.5-3 fails on 2016 MacBook Pro (MacBookPro13,3) unless intel_iommu=off"
    kind: issue
    author: "dzanaga"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/8323"
    title: "Issue #8323: Installer erases EFI/APPLE payload required by T1 MacBook hardware"
    kind: issue
    author: "sebastiang"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/11619"
    title: "Issue #11619: MacBook Pro 2015-2017 audio broken, needs the snd_hda_macbookpro driver"
    kind: issue
    author: "andyholst"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/9019"
    title: "Issue #9019: BCM43602 pre-T2 2017 MacBook Pro, feature_disable=0x82000 is not enough and a regulatory domain is also required"
    kind: issue
    author: "benjarlett"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/11745"
    title: "Issue #11745: BCM43602 on 2015-2017 Intel Macs associates but has no connectivity until iw reg set"
    kind: issue
    author: "Clowdyffs"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/9802"
    title: "Issue #9802: MacBookPro16,1 Broadcom quirk disables WPA3-SAE"
    kind: issue
    author: "kazeshini178"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/9609"
    title: "Issue #9609: MacBookPro16,1 (T2, hybrid graphics), gmux leaves the internal panel on the AMD dGPU, hard-hanging the machine at session start"
    kind: issue
    author: "yezooz"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10119"
    title: "Issue #10119: Bluetooth audio dropouts on T2 MacBook Pro 16-inch 2019, hci_uart_bcm binds instead of hci_bcm4377"
    kind: issue
    author: "ratandeepbansal"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/11926"
    title: "Issue #11926: USB hot-plug doesn't work in Intel-based MacBook Pro (16-inch, 2019) with T2 chip"
    kind: issue
    author: "VasylBaran"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/10593"
    title: "Issue #10593: Suspend/resume support for MacBookPro14,1, default deep sleep breaks Thunderbolt on resume"
    kind: issue
    author: "orospakr"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/10815"
    title: "Issue #10815: T2 MacBook Pro trackpad disable_while_typing setting not working"
    kind: issue
    author: "djfergus"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10618"
    title: "Issue #10618: omarchy-hw-external-monitors false positive from the Touch Bar DRM device causes lid-close lock to silently fail on T2 Macs"
    kind: issue
    author: "kutassy"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/3883"
    title: "Issue #3883: In Macbook pro with T2 chip keyboard, wake-from-suspend, and webcam not working"
    kind: issue
    author: "berkecyln"
    date: "2025-12-15"
  - url: "https://github.com/omacom/omarchy/issues/6559"
    title: "Issue #6559: [quattro only] Update fix-t2.sh to enhance T2 macs compatibility"
    kind: issue
    author: "twilightresonance86"
    date: "2026-08-05"
  - url: "https://github.com/omacom/omarchy/issues/1666"
    title: "Issue #1666: Built-in MacBook Pro 2016 (13,1) keyboard not working at LUKS password prompt"
    kind: issue
    author: "reza866"
    date: "2025-09-14"
credits:
  - name: "PaulShadwell"
    url: "https://github.com/PaulShadwell"
    for: "Traced the T1 EFI/APPLE wipe through the installer source and narrowed the scope to T1 models"
  - name: "dzanaga"
    url: "https://github.com/dzanaga"
    for: "Isolated the 4.0.4 linux-omarchy boot failure on MacBookPro13,3 to the IOMMU default"
  - name: "benjarlett"
    url: "https://github.com/benjarlett"
    for: "Found that BCM43602 Macs also need an explicit regulatory domain, not just the Broadcom quirk"
  - name: "orospakr"
    url: "https://github.com/orospakr"
    for: "Root-caused the MacBookPro14,1 Thunderbolt resume failure and published an s2idle enablement"
  - name: "twilightresonance86"
    url: "https://github.com/twilightresonance86"
    for: "Rewrote fix-t2.sh for the t2bce kernel transition, fixing suspend and the fan daemon crash"
faq:
  - q: "Is the Touch Bar usable on Omarchy?"
    a: "On 2018-2020 T2 models yes, through the kernel's built-in Boot Camp style support. Omarchy 4.0.0 stopped shipping tiny-dfr and its migration removes it. On 2016-2017 T1 models the Touch Bar is documented as non-functional, and a full-disk install makes that permanent."
  - q: "Does Touch ID work?"
    a: "There is no evidence it does. Nothing in the Omarchy tree enrolls the T2 fingerprint sensor, and no issue reports it working. Treat Touch ID as unavailable."
  - q: "Can I dual-boot macOS?"
    a: "The manual says Omarchy only supports being the only OS installed, and that the drive is wiped. On T1 models that wipe is what destroys the Touch Bar and camera, so if you care about those, do not do a full-disk install."
  - q: "Which kernel do I end up on?"
    a: "T2 models get linux-t2 from fix-t2.sh. Everything else, including 2016-2017 T1 models, gets the bespoke linux-omarchy kernel that 4.0.4 shipped to everyone."
related: [t2-mac, apple-macbook-air-intel, apple-silicon-macs, suspend-sleep, wifi]
draft: false
---

## Verdict

Bronze overall, and the year matters more than anything else.

A 2018 to 2020 MacBook Pro with a T2 chip is the machine Omarchy actually supports. The installer detects the T2 by PCI ID, swaps in the patched `linux-t2` kernel, installs Apple's Broadcom firmware and the `t2fanrd` fan daemon, and sets a kernel command line tuned for suspend. Most people get a working desktop on the first boot. Call it silver on its own.

A 2016 or 2017 MacBook Pro with a Touch Bar is a different machine. Those carry the T1 chip, not the T2, and Omarchy has no detection for it at install time. The manual is blunt about the result: on T1 models the Touch Bar is non-functional and sound is not functioning. Worse, a full-disk install destroys Apple boot data those machines need. That corner of the lineup is closer to broken than bronze.

Checked against v4.0.4 (2026-09-15) and the v4.0.4 source tree. T2 support first landed in v3.0.0.

## What works

On T2 models (`MacBookPro15,x` and `MacBookPro16,x`), the internal keyboard and trackpad come up through the `t2bce_vhci` virtual USB bridge, speaker audio works via `apple-t2-audio-config`, the Touch Bar runs on the kernel's in-tree Boot Camp style driver, and fan control works through `t2fanrd`. Wi-Fi and Bluetooth use Apple's Broadcom firmware from `apple-bcm-firmware`. Keyboard backlight control was fixed in v3.5.0.

Across the whole Intel range, the internal display works, the Intel iGPU works, and the SPI keyboard on 2016-2017 models reaches the LUKS prompt once `fix-spi-keyboard.sh` has run. The manual reports a 36% performance gain over macOS on a 2019 MacBook Pro, which matches the general reason people do this.

## What breaks

The T1 firmware wipe is the serious one. Issue [#8323](https://github.com/omacom/omarchy/issues/8323) and the source audit in [#8271](https://github.com/omacom/omarchy/issues/8271) show that the full-disk installer recreates the EFI system partition and nothing anywhere reads, copies or preserves an existing `EFI/APPLE` directory. On a T1 Mac that payload is what initializes the iBridge, so after the install the T1 shows up as `05ac:1281` in recovery mode instead of `05ac:8600`, and the Touch Bar, camera and ambient light sensor stay dead. The audit's own correction is worth repeating: T2 machines are not affected, because their Touch Bar is a plain USB HID device. Scope is `MacBookPro13,2`, `13,3`, `14,2` and `14,3`.

Kernel regression on the 15-inch T1. Issue [#12119](https://github.com/omacom/omarchy/issues/12119) reports that `linux-omarchy` 7.2.5-3, which 4.0.4 pushed to everyone, hangs during `amdgpu` init on a `MacBookPro13,3` and then cannot find the NVMe root. The stock Arch kernel boots fine on the same box. Adding `intel_iommu=off` fixes NVMe, the Apple SPI keyboard and AMD graphics in one go. A second reporter hit the same `CONFIG_INTEL_IOMMU_DEFAULT_ON` default on unrelated hardware. Still open.

Audio on 2016-2017. The Cirrus Logic CS8409 codec in those models is not configured correctly by the in-tree driver, so speakers stay silent and headphone switching is broken. Issue [#11619](https://github.com/omacom/omarchy/issues/11619) proposes the out-of-tree `snd_hda_macbookpro` driver, but the attached PR was closed without merging. Nothing ships for this.

Wi-Fi needs a regulatory domain, not just the Broadcom quirk. On BCM43602 machines the shipped `feature_disable=0x82000` option is not enough. In [#9019](https://github.com/omacom/omarchy/issues/9019) a `MacBookPro14,3` failed to associate for roughly 47 minutes until enough beacon hints accumulated, and setting `options cfg80211 ieee80211_regdom=GB` fixed it from cold boot. Issue [#11745](https://github.com/omacom/omarchy/issues/11745) is the same thing on a `MacBookPro14,1`, where Wi-Fi looked connected but dropped every packet until `iw reg set`. In the other direction, [#9802](https://github.com/omacom/omarchy/issues/9802) shows the same quirk disabling SAE on a `MacBookPro16,1`, so WPA3-only networks fail with `ssid-not-found`.

T2 odds and ends, all open: Bluetooth audio drops out on the 16-inch 2019 because `hci_uart_bcm` wins the bind race against `hci_bcm4377` ([#10119](https://github.com/omacom/omarchy/issues/10119)); USB hot-plug does nothing on the same model unless the device was present at boot ([#11926](https://github.com/omacom/omarchy/issues/11926)); the trackpad is classified as external by udev so disable-while-typing never activates ([#10815](https://github.com/omacom/omarchy/issues/10815)); and the `MacBookPro16,1` gmux can leave the internal panel on the AMD dGPU and hang the machine at session start ([#9609](https://github.com/omacom/omarchy/issues/9609)).

Suspend is model-specific. On `MacBookPro14,1` the default `deep` sleep leaves the Thunderbolt controller dead and resume takes 75 to 107 seconds; if anything is plugged into a Thunderbolt port at lid close, only a cold boot brings the port back ([#10593](https://github.com/omacom/omarchy/issues/10593)). Wake-from-suspend problems on T2 models are still reported in [#3883](https://github.com/omacom/omarchy/issues/3883), which is open from 2025.

## What Omarchy does for this model

Four scripts in `install/hardware/apple/` run at install time, plus a migration.

`fix-t2.sh` gates on `lspci` finding `106b:1801` or `106b:1802`. It installs `linux-t2`, `apple-t2-audio-config`, `apple-bcm-firmware` and `t2fanrd`, force-loads `t2bce_vhci` and `hci_bcm4377`, adds the T2 bridge and HID modules to the initramfs, and appends `intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep` to the Limine command line.

`fix-spi-keyboard.sh` and `fix-suspend-nvme.sh` both match DMI `product_name` against `MacBookPro13,[123]` and `MacBookPro14,[123]` plus the 12-inch MacBooks. The first installs `macbook12-spi-driver-dkms` and puts `applespi` in the initramfs; the second clears `d3cold_allowed` on the NVMe device so it wakes.

`fix-brcmfmac-supplicant.sh` writes the `feature_disable=0x82000` module option. Since v4.0.0 it applies to non-T2 Macs too, gated on the chip IDs `brcmfmac` actually binds rather than on the T2 bridge.

Migration `1785944594.sh` rewrote the T2 suspend defaults for the `t2bce` kernel, added the missing `[Fan2]` section that was crashing `t2fanrd` on dual-fan models, and removes `tiny-dfr` if present. That came from [#6559](https://github.com/omacom/omarchy/issues/6559) and shipped in 4.0.0.

## Variants

Prefer the 13-inch T2 models (`MacBookPro15,2`, `15,4`, `16,2`, `16,3`). Intel graphics only, so no gmux or dGPU problems, and they get the full T2 stack.

Be careful with the 15-inch and 16-inch T2 models. They work, but the AMD discrete GPU adds the gmux hang and dual-GPU power problems on top.

Avoid the 2016-2017 Touch Bar models unless you accept losing the Touch Bar, camera and speakers. The 2016 15-inch (`MacBookPro13,3`) currently also needs a manual `intel_iommu=off` to boot 4.0.4.

The 2012-2015 models are a separate story: they use the BCM4360 or BCM4331 with the out-of-tree `wl` driver, handled by `fix-bcm43xx.sh`, and none of the T1 or T2 machinery applies.

## Before you install

- Back up the whole disk, not just files. On a T1 Mac the Apple `EFI/APPLE` payload is not recoverable from a file backup.
- Disable Secure Boot and allow external boot from macOS Recovery, per the [Mac support chapter](https://omarchy.org/manual/mac-support/).
- Know your model identifier before you commit. `MacBookPro13,x` and `14,x` are T1, `15,x` and `16,x` are T2.
- Have a USB keyboard ready. The internal keyboard has repeatedly failed at the LUKS prompt on 2016-2017 machines ([#1666](https://github.com/omacom/omarchy/issues/1666)).
- Plan to set a regulatory domain by hand if Wi-Fi associates but passes no traffic.
- On a 15-inch 2016, be ready to edit the Limine entry and add `intel_iommu=off` at first boot.

## Related

- [/hardware/t2-mac/](/hardware/t2-mac/) for the T2 stack itself
- [/hardware/apple-macbook-air-intel/](/hardware/apple-macbook-air-intel/) for the Air, which shares the T2 path
- [/hardware/apple-silicon-macs/](/hardware/apple-silicon-macs/) for M-series machines
- [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/) and [/hardware/suspend-sleep/](/hardware/suspend-sleep/)
- [/fix/bluetooth-stops-after-resume/](/fix/bluetooth-stops-after-resume/)
- [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/)
- [/fix/kernel-panic-after-update-limine/](/fix/kernel-panic-after-update-limine/)
- [/switch/should-you-dual-boot/](/switch/should-you-dual-boot/)
