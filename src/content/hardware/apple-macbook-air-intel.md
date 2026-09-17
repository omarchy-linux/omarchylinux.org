---
title: "Apple MacBook Air (Intel, T2) on Omarchy"
description: "MacBook Air 2018 to 2020 with the Apple T2 chip on Omarchy 4.0.4: the linux-t2 kernel it gets, the suspend and Bluetooth bugs, what to check first."
answer: "Bronze. Omarchy installs the linux-t2 kernel automatically on the T2 MacBook Air, and the screen, keyboard, trackpad, audio and Wi-Fi all come up. Sleep is the problem. On the 2020 Air suspend aborts every time on a brcmfmac timeout, hibernate hangs the machine, and Bluetooth often never powers on at boot. Use it plugged in or shut it down."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Apple"
model: "MacBook Air (Intel, T2)"
dmi: ["MacBookAir8,1", "MacBookAir9,1"]
cpu: "Intel Core i5 Amber Lake Y (2018 and 2019), Intel Core i3/i5/i7 Ice Lake (2020)"
gpu: "Intel UHD Graphics 617 (2018 and 2019), Intel Ice Lake integrated graphics (2020)"
year: "2018 to 2020"
rating: bronze
subsystems:
  wifi: partial
  bluetooth: partial
  audio: works
  webcam: partial
  fingerprint: unknown
  gpu: works
  suspend: broken
  hibernate: broken
  touchpad: works
  display: works
  battery: unknown
  keyboard: works
quirkScripts:
  - name: "fix-t2.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-t2.sh"
    note: "Matches the T2 bridge by PCI ID 106b:1801 or 106b:1802, not by DMI. Installs linux-t2, linux-t2-headers, apple-t2-audio-config, apple-bcm-firmware and t2fanrd, loads t2bce_vhci and hci_bcm4377, adds intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep to the Limine kernel command line, and writes a two-fan t2fand.conf."
  - name: "fix-brcmfmac-supplicant.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-brcmfmac-supplicant.sh"
    note: "Writes options brcmfmac feature_disable=0x82000 so wpa_supplicant runs the WPA handshake in software instead of the Broadcom firmware. Triggered by the T2 PCI ID on this machine."
  - name: "fix-fkeys.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-fkeys.sh"
    note: "Sets options hid_apple fnmode=2 so the top row acts as F-keys by default."
  - name: "omarchy-hw-display"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-display"
    note: "Picks the backlight device the brightness keys drive. Reworked in 4.0.0 and 4.0.2 for Apple panels."
issueCount: 3
tags: [macbook-air, apple, t2-mac, linux-t2, suspend, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11264"
    title: "Issue #11264: MacBook Air 2020 (MacBookAir9,1, T2): Bluetooth never powers on at boot, and suspend always fails on brcmfmac D3 timeout"
    kind: issue
    author: "austinsomer"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/9237"
    title: "Issue #9237: Hibernation hangs and kills the keyboard on Apple T2 Macs"
    kind: issue
    author: "spuder"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/5155"
    title: "Issue #5155: T2 Mac: fan control broken after system update (applesmc kernel bug)"
    kind: issue
    author: "fedesapuppo"
    date: "2026-03-30"
  - url: "https://github.com/omacom/omarchy/issues/3883"
    title: "Issue #3883: In Macbook pro with T2 chip keyboard, wake-from-suspend, and webcam not working"
    kind: issue
    author: "berkecyln"
    date: "2025-12-15"
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/6862"
    title: "Issue #6862: MacBookPro15,1 (T2): deep never resumes; s2idle hangs on second suspend after Thunderbolt/xHCI die"
    kind: issue
    author: "adityathakker"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/12097"
    title: "Issue #12097: linux-omarchy 7.2.5-3 boots to emergency shell on MacBookAir6,1"
    kind: issue
    author: "nordbergmikael"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/pull/6562"
    title: "PR #6562: Fix T2 Mac suspend and fan defaults"
    kind: pr
    author: "dhh"
    date: "2026-08-07"
  - url: "https://github.com/omacom/omarchy/pull/5145"
    title: "PR #5145: Fix Bluetooth on T2 Macs by loading hci_bcm4377 module"
    kind: pr
    author: "fedesapuppo"
    date: "2026-04-01"
  - url: "https://github.com/omacom/omarchy/pull/5998"
    title: "PR #5998: Add suspend/resume recovery for T2 Macs (using legacy apple_bce)"
    kind: pr
    author: "jjohnson"
    date: "2026-05-29"
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro): Fix suspend and fan defaults on T2 Macs"
    kind: release
    author: "omacom"
    date: "2026-08-14"
credits:
  - name: "austinsomer"
    url: "https://github.com/austinsomer"
    for: "Traced the 2020 Air's failed suspends to the BCM4377 D3 timeout and the Bluetooth controller's failed first probe"
  - name: "spuder"
    url: "https://github.com/spuder"
    for: "Reported the hibernate hang on a MacBookAir9,1 and proposed a T2 guard for hibernation setup"
  - name: "fedesapuppo"
    url: "https://github.com/fedesapuppo"
    for: "Found the applesmc MMIO bug behind dead fan control on a MacBookAir8,1, and wrote the T2 Bluetooth module fix"
  - name: "jjohnson"
    url: "https://github.com/jjohnson"
    for: "Built and tested the T2 suspend and resume recovery service on the legacy apple_bce stack"
  - name: "framp"
    url: "https://github.com/framp"
    for: "Reported that a T2 Mac's Touch Bar, Esc key and webcam still work under Omarchy"
faq:
  - q: "Does the Intel MacBook Air work with Omarchy?"
    a: "It installs and runs. Omarchy detects the T2 chip by PCI ID and installs the linux-t2 kernel, Apple's Broadcom firmware, the T2 audio config and fan control without you doing anything. Display, keyboard, trackpad, audio and Wi-Fi work. Sleep does not, so treat it as a desk machine."
  - q: "Will installing Omarchy brick my MacBook Air's webcam or Touch ID like the Touch Bar Macs?"
    a: "No. The firmware that the installer wipes with the partition table belongs to the T1 chip in 2016 and 2017 Touch Bar MacBook Pros. Issue #8271 concluded the T2 is unaffected, and a T2 MacBook Pro owner in that thread reported Touch Bar, Esc and webcam still working on Omarchy."
  - q: "Does the new Omarchy kernel in 4.0.4 replace linux-t2 on my Air?"
    a: "No. Migration 1789325478 exits early when linux-t2 is installed or the running kernel name contains -t2, so T2 Macs keep their kernel and never get linux-omarchy as the default boot entry."
  - q: "Can I make suspend work on a 2020 MacBook Air?"
    a: "Not with what Omarchy ships. Issue #11264 gets deep sleep working by unloading brcmfmac and hci_bcm4377 before sleep and reloading them about 15 seconds after wake, but that is one person's out-of-tree service tested on one machine."
related: [t2-mac, apple-macbook-pro-intel, apple-silicon-macs, suspend-sleep, wifi, bluetooth]
draft: false
---

## Verdict

Bronze. The Intel MacBook Air with a T2 chip, meaning the 2018, 2019 and 2020 models, is the least complicated T2 laptop to run. The manual covers Intel Macs, and the installer does the T2 setup for you. The Air has one integrated GPU and no Touch Bar, so the Touch Bar and dual-GPU trouble that fills the T2 MacBook Pro reports does not apply to it.

What keeps it out of silver is sleep. On a MacBookAir9,1 (2020), suspend has never once succeeded for the one owner who filed a full diagnosis, and hibernate hangs the machine hard. That is a laptop you shut down rather than close. If you want a laptop that sleeps in a bag, buy something else. If you want to bring a shelved Air back to life as a desk or couch machine, it is a good fit.

Checked against Omarchy 4.0.4 (2026-09-15) with the source at tag v4.0.4. The three T2 Air issues in the tracker are all open.

## What works

The T2 bridge brings up the internal keyboard, the trackpad and audio, and they all survive a resume once the Wi-Fi chip is out of the way. The 2020 Air report in issue #11264 shows it directly: take the Broadcom chip out of the picture and a deep sleep cycle completes, after which "the `t2bce` bridge, keyboard, trackpad and audio all come back", in the reporter's words.

The internal panel works. Both Air reporters run the Omarchy desktop on it, one of them as far as the lock screen after a resume. Brightness goes through `omarchy-hw-display`, which Omarchy 4.0.0 taught to skip the Touch Bar backlight and prefer gmux, with Apple brightness detection improved again in 4.0.2. An Air has neither a Touch Bar nor a gmux, so the picker falls through to the panel's own `intel_backlight`.

Wi-Fi associates and stays up in normal use. The BCM4377 needs Omarchy's `brcmfmac` quirk to complete a WPA handshake against a mixed WPA2/WPA3 access point, and the installer writes it for you.

Graphics are plain Intel, and the desktop runs on them in both Air reports. There is no second GPU here, so none of the gmux and dual-GPU backlight handling that `omarchy-hw-display` carries for the bigger MacBook Pros comes into play.

The webcam routes through the T2 bridge rather than a separate PCIe camera. A MacBook Air 2018 owner corrected an earlier guess on issue #3883 to say the T2 webcam is handled by the bridge driver plus `uvcvideo`, both already in `linux-t2`, and that the `facetimehd` packages only do anything on pre-T2 Macs with the older Broadcom camera. Treat it as working once the bridge is up, and as a casualty whenever the bridge is not.

## What breaks

**Suspend on the 2020 Air.** Issue #11264 (open, MacBookAir9,1 on 4.0.3) reports that every suspend aborts with `brcmf_pcie_pm_enter_D3: Timeout on response for entering D3 substate` followed by `PM: failed to suspend: error -5`. The s2idle retry that systemd falls back to dies on the same timeout. Closing the lid turns that into a loop: logind reattempts the suspend about twice a minute, and the laptop sits there running instead of sleeping. The reporter counted 371 failed attempts in one three-hour stretch with the lid down.

**Bluetooth at boot.** On the same machine the driver loads and the `hci0` device appears, yet the controller stays dead: `command 0x0c56 tx timeout`, and `bluetoothctl power on` returns an error. Unbinding and rebinding the driver after boot brings it up, usually on the second try. Omarchy already loads the module, from PR #5145 (merged 2026-04-01, shipped in 3.5.0), so this is a firmware-init flake rather than a missing driver.

**Hibernate.** Issue #9237 (open) is a MacBookAir9,1 on 4.0.1: `omarchy hibernation setup` configures hibernation happily, and triggering it hard-freezes the machine partway through, with an unresponsive keyboard and no resume. The journal stops after the filesystem sync and the next boot is a cold one. The reporter points at the T2 embedded controller not surviving S4 and proposed an `omarchy-hw-t2` guard that refuses hibernation setup on T2 hardware. No such helper exists in v4.0.4, so nothing stands between you and a hung machine. Do not set it up.

**Fan control on the 2018 Air.** Issue #5155 (open) is a MacBookAir8,1 where `t2fanrd` stopped controlling the fan after a kernel update. The cause was traced to the `linux-t2` patch set, where an unaligned `iowrite32` on byte-sized SMC registers made the T2 reject every fan write. The machine does not cook, because the T2 does its own basic thermal management, but the fan sits near minimum and the laptop stays warmer than it needs to be.

**Touch ID.** Nothing in Omarchy enables it and nothing in the tracker reports it working. Omarchy's fingerprint setup targets ordinary fprintd readers. Assume it does nothing on this machine.

## What Omarchy does for this model

Detection is by PCI ID, not by DMI. `install/hardware/apple/fix-t2.sh` greps `lspci` for `106b:1801` or `106b:1802` and, when it matches, installs `linux-t2`, `linux-t2-headers`, `apple-t2-audio-config`, `apple-bcm-firmware` and `t2fanrd`, enables `t2fanrd.service`, loads `t2bce_vhci` and `hci_bcm4377`, adds `t2bce_vhci usbhid hid_apple hid_generic xhci_pci xhci_hcd` to the initramfs, appends `intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep` to the Limine kernel command line, and writes a `t2fand.conf` with two fan sections. The ISO's own configurator makes the same PCI check to pick `linux-t2` at install time.

`install/hardware/apple/fix-brcmfmac-supplicant.sh` writes `options brcmfmac feature_disable=0x82000`, which turns off the firmware supplicant and authenticator so `wpa_supplicant` runs the handshake. In 4.x this quirk also covers Macs without a T2.

Two other Apple scripts do not apply here. `fix-spi-keyboard.sh` and `fix-suspend-nvme.sh` match DMI names like `MacBook8,1`, `MacBookPro13,x` and `MacBookPro14,x`. `MacBookAir8,1` and `MacBookAir9,1` do not match either pattern, which is correct, since the T2 Air's keyboard hangs off the bridge rather than a bare SPI controller.

4.0.4 makes `linux-omarchy` the default boot entry for most machines. Migration `1789325478` exits immediately when `linux-t2` is present or the running kernel name contains `-t2`, so your Air keeps `linux-t2`. This is worth knowing in both directions: a pre-T2 Air does get the new kernel, and issue #12097 is a MacBookAir6,1 (2013) dropping into an emergency shell on `linux-omarchy` 7.2.5-3 while the stock `linux` entry boots fine.

## Where 3.x differs

Omarchy 3.x used the older `apple-bce` driver, installed `tiny-dfr` for the Touch Bar, passed `pcie_ports=compat` instead of `pm_async=off mem_sleep_default=deep`, and wrote a single-fan `t2fand.conf`. Quattro switched to the `t2bce` stack, dropped `tiny-dfr` in favour of the kernel's built-in Boot Camp-style Touch Bar, and pinned deep sleep. The migration that performs that change is `1785944594`, from PR #6562, and it also removes `tiny-dfr` from machines that had it.

Pinning `deep` is a mixed result across T2 models. Issue #6862, a MacBookPro15,1, argues it pins the worse of two bad options on that machine. No Air report contradicts the default, since on the 2020 Air both modes fail for the same Wi-Fi reason.

## Variants

Three machines carry the T2 in this family: the 2018 Air (`MacBookAir8,1`, A1932), the 2019 Air (`MacBookAir8,2`, A1932) and the 2020 Air (`MacBookAir9,1`, A2179). Only 8,1 and 9,1 appear in the tracker data. The manual's list of T2 models names only the 2018 Retina Air, but detection never reads those names, so all three get the same treatment.

The 2020 model is the better machine on paper, with an Ice Lake i3, i5 or i7 in place of the dual-core Amber Lake Y parts in 2018 and 2019, but it is also the one with the documented suspend and Bluetooth failures. The 2018 Air is the one with the documented fan control bug. Neither has an unambiguously better record.

Do not confuse the 2020 Intel Air with the M1 Air released the same year. The M1 machine is A2337, has no T2, and is not covered here. See [Apple Silicon Macs](/hardware/apple-silicon-macs/).

## Before you install

- Back up anything on the machine. Omarchy's standard path wipes the disk and macOS stops being bootable. You can restore it later through Internet Recovery.
- Disable Secure Boot and allow external boot from macOS Recovery first, following the manual's [Mac support](https://omarchy.org/manual/mac-support/) chapter. Without it the USB will not boot.
- Do not worry about the T1 firmware story on this machine. Issue #8271 concerns 2016 and 2017 Touch Bar MacBook Pros, whose coprocessor loads firmware from the macOS EFI partition. The thread's own analysis puts the scope at `MacBookPro13,2`, `13,3`, `14,2` and `14,3`, and a T2 owner there reported Touch Bar, Esc and webcam still working.
- After the first boot, check you are on the right kernel: `uname -r` should contain `-t2`. If it does not, the T2 detection did not run and nothing else will behave.
- Skip `omarchy hibernation setup` entirely.
- Plan for a machine you shut down rather than suspend, at least until a Wi-Fi sleep hook ships. PR #5998, the closest thing to one, was closed without merging and targeted the older `apple-bce` stack.

Evidence here is thin in one direction and solid in the other. Three open issues name a T2 MacBook Air specifically, so almost everything above that says "this breaks" is well sourced and almost everything that says "this works" rests on the same small number of reports. Battery life on Omarchy is unmeasured on this model. If you run one, [send a report](/hardware/submit/).

## Related

- [Intel Macs with the Apple T2 chip](/hardware/t2-mac/) for the full T2 picture across models
- [Intel MacBook Pro](/hardware/apple-macbook-pro-intel/) for the Touch Bar and dGPU machines
- [Suspend and sleep](/hardware/suspend-sleep/) and [hibernate fails or hangs](/fix/hibernate-fails-or-hangs/)
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/)
