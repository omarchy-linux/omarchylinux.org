---
title: "Intel Macs with the Apple T2 chip on Omarchy"
description: "What works and what breaks on T2 Macs running Omarchy 4.x: the linux-t2 kernel, the quirk scripts the installer applies, open issues, and the fix order."
answer: "Omarchy detects the T2 by PCI ID 106b:1801 or 106b:1802 and installs the linux-t2 kernel, apple-t2-audio-config, apple-bcm-firmware and t2fanrd automatically. Keyboard, trackpad, Wi-Fi, audio, fans and the Touch Bar usually work. Suspend, hybrid graphics on the 16-inch, USB hot-plug and the AMD-only 2020 iMac are the weak spots. Start by confirming you booted linux-t2."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "t2-mac"
issueCount: 64
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [t2-mac, macbook, apple, linux-t2, suspend]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6559"
    title: "Issue #6559: [quattro only] Update fix-t2.sh to enhance T2 macs compatibility"
    kind: issue
    author: "twilightresonance86"
    date: "2026-08-05"
  - url: "https://github.com/omacom/omarchy/issues/6558"
    title: "Issue #6558: [quattro only] omarchy-hw-display on T2 Mac returns the touchbar display instead of internal display"
    kind: issue
    author: "twilightresonance86"
    date: "2026-08-05"
  - url: "https://github.com/omacom/omarchy/pull/6562"
    title: "PR #6562: Fix T2 Mac suspend and fan defaults"
    kind: pr
    author: "dhh"
    date: "2026-08-07"
  - url: "https://github.com/omacom/omarchy/pull/6597"
    title: "PR #6597: Use the gmux backlight instead of the Touch Bar on T2 Macs"
    kind: pr
    author: "dhh"
    date: "2026-08-07"
  - url: "https://github.com/omacom/omarchy/issues/6862"
    title: "Issue #6862: MacBookPro15,1 (T2): deep never resumes; s2idle hangs on second suspend after Thunderbolt/xHCI die"
    kind: issue
    author: "adityathakker"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/9609"
    title: "Issue #9609: MacBookPro16,1 (T2, hybrid graphics): gmux leaves the internal panel on the AMD dGPU, hard-hanging the machine at session start"
    kind: issue
    author: "yezooz"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/12197"
    title: "Issue #12197: T2 iMac20,1 (2020 5K, Radeon Pro 5300): amdgpu SMU init fails; Plymouth/KMS black screen before LUKS"
    kind: issue
    author: "McoreD"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11926"
    title: "Issue #11926: USB hot-plug doesn't work in Intel-based MacBook Pro (16-inch, 2019) with T2 chip"
    kind: issue
    author: "VasylBaran"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/10825"
    title: "Issue #10825: Touch Bar dead on T1 Macs: macbook12-spi-driver DKMS never builds"
    kind: issue
    author: "passerini"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/3883"
    title: "Issue #3883: In Macbook pro with T2 chip keyboard, wake-from-suspend, and webcam not working"
    kind: issue
    author: "berkecyln"
    date: "2025-12-15"
  - url: "https://github.com/omacom/omarchy/issues/4402"
    title: "Issue #4402: Mac T2 Bluetooth menu doesn't open"
    kind: issue
    author: "Jan747"
    date: "2026-01-31"
  - url: "https://github.com/omacom/omarchy/issues/1840"
    title: "Issue #1840: Omarchy lid/sleep/suspend issue on MacBook (bug + solution to be tested)"
    kind: issue
    author: "nunix"
    date: "2025-09-20"
  - url: "https://github.com/omacom/omarchy/issues/7347"
    title: "Issue #7347: T2 + t2archinstall overlay: Limine writes branding-only to the ESP, linux-t2 never becomes an entry, PipeWire has no ALSA SPA"
    kind: issue
    author: "twfyke"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/10815"
    title: "Issue #10815: T2 Macbook Pro Trackpad disable_while_typing setting not working"
    kind: issue
    author: "djfergus"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/6608"
    title: "Issue #6608: Follow up to #6559 - update fix-t2.sh and migrations/1785944594.sh to not use grep -q"
    kind: issue
    author: "twilightresonance86"
    date: "2026-08-07"
  - url: "https://github.com/omacom/omarchy/issues/6833"
    title: "Issue #6833: Keyboard layout bar widget can switch the wrong device on T2 Macs (Apple Headset phantom keyboard not excluded)"
    kind: issue
    author: "brwaters"
    date: "2026-08-13"
  - url: "https://github.com/omacom/omarchy/issues/10121"
    title: "Issue #10121: T2 Macs: battery charge limiting is unreachable, applesmc binds no device and the t2bce stack has no SMC transport"
    kind: issue
    author: "ratandeepbansal"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/2291"
    title: "Issue #2291: Keyboard backlight support for T2 macbooks"
    kind: issue
    author: "satyapraneet63"
    date: "2025-10-07"
  - url: "https://github.com/omacom/omarchy/pull/5145"
    title: "PR #5145: Fix Bluetooth on T2 Macs by loading hci_bcm4377 module"
    kind: pr
    author: "fedesapuppo"
    date: "2026-04-01"
  - url: "https://github.com/omacom/omarchy/pull/5135"
    title: "PR #5135: Use percentage-based step for keyboard backlight brightness"
    kind: pr
    author: "fedesapuppo"
    date: "2026-04-01"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-t2.sh"
    title: "install/hardware/apple/fix-t2.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "twilightresonance86"
    url: "https://github.com/twilightresonance86"
    for: "Found the pipefail false negative in the T2 hardware check and the Touch Bar backlight picking bug, and tested both fixes"
  - name: "fedesapuppo"
    url: "https://github.com/fedesapuppo"
    for: "T2 Bluetooth and keyboard backlight fixes that shipped in 3.5.0"
  - name: "passerini"
    url: "https://github.com/passerini"
    for: "Traced the dead Touch Bar on T1 Macs to a DKMS build that never runs and a mkinitcpio drop-in that resets MODULES"
  - name: "niconistal"
    url: "https://github.com/niconistal"
    for: "Built a recovery tool for T1 Macs whose Apple ESP the installer erased"
faq:
  - q: "Does the Omarchy 4.0.4 kernel replace linux-t2?"
    a: "No. The migration that installs linux-omarchy exits early when linux-t2 is present or when the running kernel name contains -t2, so T2 Macs keep their patched kernel. A separate migration adds linux-t2-headers if they are missing."
  - q: "Do I need tiny-dfr for the Touch Bar?"
    a: "Not on 4.x. Omarchy deliberately does not install it, and its own test asserts that. The Touch Bar runs on the kernel's in-tree hid_appletb_kbd path."
  - q: "Can I dual boot macOS?"
    a: "The manual says Omarchy supports being the only OS, and the full-disk install wipes the partition table. On T1 Macs that also destroys firmware stored on the Apple ESP, per issue 8271. Reporters on that thread who kept macOS used the installer's free-space option, which creates a second ESP and leaves Apple's alone."
related: [suspend-sleep, hybrid-gpu, wifi, audio, apple-macbook-pro-intel, apple-silicon-asahi]
draft: false
---

Intel Macs with the Apple T2 Security Chip get more installer attention than any other Apple hardware on Omarchy. The T2 sits between the CPU and the keyboard, trackpad, audio, webcam, storage and Wi-Fi, so a stock Arch kernel sees almost nothing. Omarchy handles this by swapping in the community `linux-t2` kernel and a small pile of quirks.

## Status on 4.0.4

Verified against the v4.0.4 source tree and against issues filed on 4.0.2, 4.0.3 and 4.0.4.

Working for most reporters: internal keyboard and trackpad, Wi-Fi and Bluetooth, speakers, fan control, the webcam, and the Touch Bar. On issue 8271 a reporter running a 2019 T2 MacBook Pro confirmed the Touch Bar, the Escape key and the webcam all still work after an ordinary install.

Unreliable: suspend and resume, hybrid graphics on the 16-inch models, USB hot-plug, and the 2020 27-inch iMac, whose only display adapter is AMD. Battery charge limiting is not reachable at all on T2, because the machine has no SMC transport the kernel can use (issue 10121).

One 4.0.4 detail matters here. The release shipped the bespoke `linux-omarchy` kernel to everyone else, but the migration that installs it exits immediately if `linux-t2` is installed or the running kernel name contains `-t2`. T2 Macs stay on `linux-t2`. A later migration installs `linux-t2-headers` if the installer skipped them.

The manual chapter is [Mac support](https://omarchy.org/manual/mac-support/). Its T2 model list does not include the 2020 27-inch iMac, which is one reason issue 12197 exists.

## What Omarchy does automatically

Everything below runs from `install/hardware/apple/` during install, and the matching migrations repair older machines.

`fix-t2.sh` matches `lspci` output against PCI IDs `106b:1801` and `106b:1802`. When it hits, it installs `linux-t2`, `linux-t2-headers`, `apple-t2-audio-config`, `apple-bcm-firmware` and `t2fanrd`, enables `t2fanrd.service`, and writes four files:

- `/etc/modules-load.d/t2.conf` loading `t2bce_vhci` and `hci_bcm4377`
- `/etc/mkinitcpio.conf.d/apple-t2.conf` adding `t2bce_vhci usbhid hid_apple hid_generic xhci_pci xhci_hcd` to the initramfs
- `/etc/limine-entry-tool.d/t2-mac.conf` appending `intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep` to the kernel command line
- `/etc/t2fand.conf` with a linear curve from 55C to 75C for two fans

`fix-brcmfmac-supplicant.sh` writes `options brcmfmac feature_disable=0x82000` to `/etc/modprobe.d/brcmfmac.conf`. Broadcom's firmware runs the WPA handshake itself and fails against access points in WPA2 and WPA3 transition mode, which users read as a rejected password. The flag hands the handshake back to `wpa_supplicant`. Since 4.0.0 this covers Macs without a T2 as well, gated on the Broadcom PCI IDs rather than the T2 bridge.

`omarchy-hw-display` skips `appletb_backlight` and prefers `gmux_backlight`, so brightness keys drive the panel instead of the Touch Bar.

Note what is not installed: `tiny-dfr`. Omarchy's own test suite asserts that `fix-t2.sh` leaves it out and that the ISO no longer caches it. The Touch Bar uses the kernel's in-tree driver.

Two more Apple scripts run but target pre-T2 and T1 machines, not yours: `fix-spi-keyboard.sh` (MacBook8,1 through MacBookPro14,3) and `fix-suspend-nvme.sh`, which disables `d3cold` on the NVMe at PCI address `0000:01:00.0`.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#12197](https://github.com/omacom/omarchy/issues/12197) amdgpu SMU init fails, black screen before the LUKS prompt | iMac20,1 | open | |
| [#11926](https://github.com/omacom/omarchy/issues/11926) USB hot-plug dead unless the device was plugged in at boot | MacBookPro16,1 | open | |
| [#6862](https://github.com/omacom/omarchy/issues/6862) `deep` never resumes, `s2idle` hangs on the second suspend | MacBookPro15,1, MacBookPro16,1 | open | |
| [#9609](https://github.com/omacom/omarchy/issues/9609) gmux leaves the panel on the AMD dGPU and hangs at session start | MacBookPro16,1 | open | |
| [#3883](https://github.com/omacom/omarchy/issues/3883) keyboard dead during setup, no wake from suspend, webcam not detected | 2018 to 2020 T2 laptops | open | |
| [#10815](https://github.com/omacom/omarchy/issues/10815) trackpad `disable_while_typing` ignored, trackpad classified external | MacBookPro15,2, MacBookAir9,1, MacBookPro16,1 | open | |
| [#6833](https://github.com/omacom/omarchy/issues/6833) keyboard layout widget switches the phantom "Apple Headset" device | all T2 | open | |
| [#7347](https://github.com/omacom/omarchy/issues/7347) overlay installs get a branding-only Limine config and no `linux-t2` entry | MacBookPro16,3 via t2archinstall | open | |
| [#8271](https://github.com/omacom/omarchy/issues/8271) full-disk install erases the Apple ESP holding T1 firmware | T1 only: 13,2 13,3 14,2 14,3 | open | |
| [#10825](https://github.com/omacom/omarchy/issues/10825) Touch Bar dead, `macbook12-spi-driver` DKMS never builds | T1 MacBookPro13,3, MacBookPro14,3 | open | |
| [#6559](https://github.com/omacom/omarchy/issues/6559) stale suspend and fan defaults, and the `pipefail` false negative in the T2 check filed as [#6608](https://github.com/omacom/omarchy/issues/6608) | all T2 | fixed | 4.0.0 |
| [#6558](https://github.com/omacom/omarchy/issues/6558) brightness stuck at 100 percent, backlight resolved to the Touch Bar | Touch Bar T2 laptops | fixed | 4.0.0 |
| [#4402](https://github.com/omacom/omarchy/issues/4402) Bluetooth menu opens and closes instantly | all T2 | fixed | 3.5.0 |
| [#2291](https://github.com/omacom/omarchy/issues/2291) keyboard backlight keys step 1 of 512 levels, so nothing visibly changes | all T2 | fixed | 3.5.0 |

The T1 rows are here because owners of 2016 and 2017 Touch Bar Macs routinely read themselves into the T2 section of the manual. Check `lspci -nn | grep 106b:180`. No output means no T2.

## Fixes that work

Work down this list in order.

1. Confirm the kernel. `uname -r` should contain `-t2`. If it does not, the T2 detection never fired and nothing else here applies.
2. Confirm the command line actually took. Run `cat /proc/cmdline` and look for `mem_sleep_default=deep`. On issue 1840 a commenter pointed out that if `/etc/default/limine` uses `KERNEL_CMDLINE[default]=` rather than `+=`, it overwrites every drop-in including `t2-mac.conf`. Change it to `+=` and run `sudo limine-update`.
3. If suspend dies immediately rather than failing to resume, try `mem_sleep_default=s2idle` instead. The reporter on issue 6862 says `deep` never resumes on the 15,1, and one commenter adds that it kills the 16,1 outright. On the 15,1, `s2idle` survived exactly one cycle before Thunderbolt failed to resume. Neither mode is reliable on the 15,1 and 16,1 yet, and there is no upstream fix.
4. If brightness is pinned at 100 percent, run `omarchy-hw-display`. It should print `gmux_backlight` or `intel_backlight`, never `appletb_backlight`. If it prints the Touch Bar, your install predates 4.0.0 and needs `omarchy update`.
5. If Wi-Fi reports a wrong password on a WPA2 or WPA3 network, check `/etc/modprobe.d/brcmfmac.conf` for `feature_disable=0x82000`, then reboot.
6. If the Bluetooth menu closes instantly, check that `/etc/modules-load.d/t2.conf` lists `hci_bcm4377`.
7. For hybrid graphics hangs at session start on the 16-inch, the reporter on issue 9609 boots with `apple_gmux.force_igd=1` and persists it as `options apple-gmux force_igd=y` in `/etc/modprobe.d/apple-gmux.conf`. A commenter on issue 6559 hit the same black screen on the Quattro edge ISO and used the same flag. It hands the panel to the integrated GPU, the reporter had not tested external displays with it, and it is a workaround, not a fix.

Do not install the `facetimehd` driver on a T2 machine. A contributor corrected their own earlier advice on issue 3883: the T2 webcam comes through the bridge driver and `uvcvideo`, both already in `linux-t2`, and `facetimehd` is for pre-T2 Broadcom cameras.

## Report it

Run `omarchy debug` and pick the upload option. It writes `/tmp/omarchy-debug.log`, uploads it to `logs.omarchy.org` with a 24 hour expiry, and prints a URL to paste into the issue. Use `omarchy debug --print --no-sudo` first if you want to read it before sharing.

Add four things the T2 reports that get fixed all include: the exact model from `cat /sys/class/dmi/id/product_name`, the output of `lspci -nn | grep 106b:180`, `uname -r`, and whether you installed from the Omarchy ISO or overlaid Omarchy onto an existing Arch install. That last one matters more than it sounds, because the overlay path is the whole subject of issue 7347.

## Related

- [Suspend and sleep](/hardware/suspend-sleep/) and [suspend will not resume](/fix/suspend-wont-resume-s2idle/)
- [Hybrid GPU laptops](/hardware/hybrid-gpu/) and [hybrid GPU black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [Wi-Fi](/hardware/wifi/), [Bluetooth](/hardware/bluetooth/), [audio](/hardware/audio/), [webcam](/hardware/webcam/)
- [Intel MacBook Pro](/hardware/apple-macbook-pro-intel/) and [Intel MacBook Air](/hardware/apple-macbook-air-intel/)
- [Apple Silicon and Asahi](/hardware/apple-silicon-asahi/) for M-series machines, which Omarchy does not support
- [Report your machine](/hardware/submit/)
