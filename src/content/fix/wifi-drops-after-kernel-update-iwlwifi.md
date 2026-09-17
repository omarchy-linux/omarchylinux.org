---
title: "Wi-Fi gone or dropping after a kernel update (iwlwifi, mt7921, brcmfmac)"
description: "Wi-Fi disappears or drops after an Omarchy kernel update: boot the previous Limine kernel entry, install matching headers, rebuild DKMS modules, fix firmware."
answer: "Boot the previous kernel entry in the Limine menu to get a network back. Then check whether the driver is out of tree: install the headers for every installed kernel and run sudo dkms autoinstall. If dmesg shows firmware load errors instead, update linux-firmware and the vendor split package such as linux-firmware-intel. Reboot and verify with nmcli device status."
appliesTo:
  from: "3.x"
status: workaround
category: network
issueCount: 202
errorStrings:
  - "iwlwifi 0000:00:14.3: Direct firmware load for iwlwifi-bz-b0-wh-b0-c101.ucode failed with error -2"
  - "iwlwifi 0000:00:14.3: no suitable firmware found!"
  - "iwlwifi 0000:00:14.3: Failed to run INIT ucode: -110"
  - "probe with driver iwlwifi failed with error -110"
  - "modprobe: FATAL: Module wl not found in directory /lib/modules/7.2.2-arch1-1"
  - "==> ERROR: Missing 7.2.3-arch1-3 kernel headers for module broadcom-wl/6.30.223.271."
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [wifi, kernel, dkms, firmware, limine, network]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10975"
    title: "Issue #10975: 4.0.3 upgrade replaces broadcom-wl with DKMS without installing kernel headers, breaking Wi-Fi after reboot"
    kind: issue
    author: "cdevroe"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/9386"
    title: "Issue #9386: Kernel 7.2 update leaves BCM4360 Macs offline: wl module missing and DKMS fails to build"
    kind: issue
    author: "robertogogoni"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/6551"
    title: "Issue #6551: Wifi (Intel BE213 on Dell XPS 13) doesn't work out of the box - linux-firmware on install media too old"
    kind: issue
    author: "anthonylinks"
    date: "2026-08-05"
  - url: "https://github.com/omacom/omarchy/issues/1829"
    title: "Issue #1829: Wifi - Mediatek 7921 / Asus Vivobook S14 (possibly others)"
    kind: issue
    author: "jkc-2"
    date: "2025-09-20"
  - url: "https://github.com/omacom/omarchy/issues/8461"
    title: "Issue #8461: System hangs on second suspend when iwlwifi firmware fails to reinitialize after wake"
    kind: issue
    author: "hojner"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7311"
    title: "Issue #7311: Quattro iwd to NetworkManager migration: wpa_supplicant roam-thrashes onto AP 6 GHz radio it can't hold (MT7922/mt7921e)"
    kind: issue
    author: "Chosen9115"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/8996"
    title: "Issue #8996: Quattro upgrade silently drops all saved Wi-Fi networks in the iwd to NetworkManager switch"
    kind: issue
    author: "orospakr"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/discussions/3053"
    title: "Discussion #3053: iwd doesn't connect to my wifi [RESOLVED]"
    kind: discussion
    author: "RainWasHe"
    date: "2025-11-01"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4: Install our bespoke kernel and set linux-omarchy as the default boot option"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3: Switch Broadcom Wi-Fi to the DKMS driver after Arch dropped the prebuilt module"
    kind: release
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/networking/"
    title: "Omarchy manual: Networking"
    kind: manual
credits:
  - name: "cdevroe"
    url: "https://github.com/cdevroe"
    for: "Traced the 4.0.3 Broadcom DKMS swap to missing kernel headers"
  - name: "bbarthel"
    url: "https://github.com/bbarthel"
    for: "Showed the DKMS hook error scrolling past under the updater's --noconfirm"
  - name: "Ladeby"
    url: "https://github.com/Ladeby"
    for: "Pointed out that headers must be derived from installed kernels and that skipped DKMS builds need a retry"
  - name: "frankjmattia"
    url: "https://github.com/frankjmattia"
    for: "Documented the broadcom-wl to broadcom-wl-dkms bridge on a 7.2 kernel"
  - name: "jkc-2"
    url: "https://github.com/jkc-2"
    for: "Reported the MediaTek MT7921 loss on an Asus Vivobook and the downgrade that recovered it"
  - name: "kromsam"
    url: "https://github.com/kromsam"
    for: "Linked the MT7921 breakage to an upstream linux-firmware bug and narrowed the downgrade to linux-firmware-mediatek alone"
faq:
  - q: "Why did Wi-Fi work before the reboot and not after?"
    a: "The update installed the new kernel but you kept running the old one. Modules and firmware are only chosen at boot, so a module that failed to build or a firmware blob the new driver rejects only bites on the next boot."
  - q: "Can I just reinstall linux-firmware?"
    a: "Only if the log shows a firmware load error. Arch splits linux-firmware into per-vendor packages, and issue #6551 reports a normal upgrade leaving linux-firmware-intel behind while every other split package moved forward."
  - q: "Is the Omarchy kernel the cause?"
    a: "Not usually, but 4.0.4 makes linux-omarchy the default boot entry, so an update that changes nothing else still changes the kernel you boot. The previous kernel stays installed, so you can pick it in the Limine menu."
  - q: "Where did my saved networks go after upgrading from 3.x?"
    a: "Quattro moved from iwd to NetworkManager and nothing converts the old profiles. Issue #8996 reports them still sitting in /var/lib/iwd as root, with the passphrase in each .psk file."
related: [kernel-panic-after-update-limine, suspend-wont-resume-s2idle, bluetooth-stops-after-resume, omarchy-update-fails-or-hangs]
draft: false
---

Your machine updated, rebooted, and now there is no Wi-Fi at all, or it connects and falls over every few minutes. This page covers the case where a kernel or firmware change is the trigger. It was checked against 4.0.4 (2026-09-15), with notes where 3.x behaves differently.

## The fix

**1. Find out what broke.** Run these before changing anything:

```bash
uname -r
nmcli device status
rfkill list wifi
lspci -nnk | grep -A3 -i 'network\|wireless'
journalctl -k -b | grep -iE 'iwlwifi|mt7921|brcmfmac|rtw89|firmware'
```

Three outcomes matter. No `wifi` row in `nmcli device status` and no `Kernel driver in use` line from `lspci` means the driver never loaded. A driver line plus `failed with error -2` in the log means the firmware blob is missing. A device that appears and then drops means the driver loaded but cannot hold the link.

**2. Get a network back first.** Everything below needs packages. At the Limine menu, stop the countdown and arrow down to your previous kernel entry, usually `linux`. Since 4.0.4, migration `1789325478.sh` installs `linux-omarchy` and puts it first in `BOOT_ORDER`, but it does not remove the kernel you were running, so that entry is still in the menu. If no entry boots with Wi-Fi, use a pre-update snapshot entry, plug in Ethernet, or tether a phone over USB.

**3. If the driver is out of tree, fix the headers and rebuild.** This is the common one on Broadcom Macs and on any machine that carried `broadcom-wl`, `rtl8821ce`, `nvidia` or similar. List what is installed, then install headers to match:

```bash
dkms status
pacman -Qoq /usr/lib/modules/*/vmlinuz
sudo pacman -S --needed dkms linux-headers linux-omarchy-headers
sudo dkms autoinstall
```

Trim that `pacman -S` line to the `-headers` packages matching kernels the previous command actually printed. The `dkms autoinstall` at the end is not optional: the DKMS pacman hook only fires while a package is being installed or upgraded, and a build it skipped for lack of headers is never picked up again. Installing the headers afterwards, on its own, leaves the module missing.

On 4.0.2 and earlier, `install/hardware/fix-bcm43xx.sh` asked for `broadcom-wl`, which Arch stopped building for Linux 7.2. Release 4.0.3 switched that to `broadcom-wl-dkms`. If you are still holding the old package:

```bash
sudo pacman -R broadcom-wl
sudo pacman -S broadcom-wl-dkms
sudo dkms autoinstall
```

**4. If the log shows a firmware load error, update firmware, not the driver.** An `error -2` is a missing file:

```bash
sudo pacman -S --needed linux-firmware linux-firmware-intel
```

Substitute your vendor's split package, for example `linux-firmware-mediatek` or `linux-firmware-marvell`. Reboot and read the log again. If the machine has no network at all, copy the package files over on a USB stick from another machine and install them offline with `sudo pacman -U ./<file>.pkg.tar.zst`, which is what issue #6551 did on a Dell XPS 13 with an Intel BE213.

**5. If new firmware broke a card that used to work, downgrade only that package.** In issue #1829 an Asus Vivobook with an MT7921 lost Wi-Fi after an update. The reporter recovered by downgrading both the kernel and `linux-firmware-mediatek`; a later comment traced it to an upstream firmware bug and narrowed the downgrade to `linux-firmware-mediatek` alone, and the `20251011-1` build was reported working. Add the pinned package to `IgnorePkg` in `/etc/pacman.conf` while you wait, then remove the pin.

**6. If the new kernel itself is the regression, stay on the old one.** Edit `/etc/default/limine`, put your working kernel first in `BOOT_ORDER`, and run `sudo limine-mkinitcpio`. The steps and the exact syntax are in [kernel panic after update](/fix/kernel-panic-after-update-limine/). This is the shape of discussion #3053 on 3.x, where iwlwifi stopped working on 6.17.2 and later and the reporter went back to 6.17.1.

**7. If the radio is simply blocked,** run _Update > Hardware > Wi-Fi_ from the Omarchy menu. That is `omarchy-restart-wifi`, which does `rfkill unblock wifi`, turns NetworkManager's radio back on, and rescans.

## Verify it worked

```bash
uname -r
dkms status
nmcli device status
journalctl -k -b | grep -i 'loaded firmware version'
```

`dkms status` should list your module as `installed` against the running kernel, not only an older one. `nmcli device status` should show a `wifi` device in state `connected`. For an out-of-tree Broadcom module, `modinfo wl | grep filename` should point into `/lib/modules/$(uname -r)/updates/dkms/`. Then reboot once more and check again, because the first boot after a rebuild is the one that proves the module survives.

## Why it happens

Kernel modules live under `/usr/lib/modules/<version>`, so every kernel update needs its own copy of anything out of tree. DKMS rebuilds those during the package transaction, and only if headers for that exact kernel are present. `omarchy-update` calls `pacman -Syu --noconfirm`, and the DKMS hook's `Missing kernel headers for module` line is not fatal to the transaction, so the update finishes green with a module that was never built. You find out at the next boot when there is no Wi-Fi. That is the sequence in issue #10975 on 4.0.3 and, with a kernel-specific `broadcom-wl` instead of a skipped DKMS build, in issue #9386 on a BCM4360 MacBook Air.

Firmware is separate again. It ships in `linux-firmware` and its per-vendor split packages, versioned on their own schedule. A newer driver can ask for a ucode revision your firmware package does not carry yet, which is the `no suitable firmware found!` case, and newer firmware can break a driver that was fine, which is the MediaTek case.

Two things changed in 4.x. Quattro replaced iwd with NetworkManager and wpa_supplicant, so a post-upgrade outage may be lost profiles rather than a dead radio. And 4.0.4 installs `linux-omarchy` and makes it the first boot entry on every x86_64 machine that is not a T2 Mac, so an update can hand you a different kernel even when the stock `linux` package did not move.

## If that did not work

If Wi-Fi only dies after sleep, this is not your page. Issue #8461 describes iwlwifi failing to reinitialize after wake with repeated `-110` timeouts; see [suspend will not resume](/fix/suspend-wont-resume-s2idle/) and [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/).

If the link is up but unusable, with high jitter rather than low throughput, check roaming. Issue #7311 traced constant reassociation on an MT7922 to wpa_supplicant electing a 6 GHz radio it could not hold, fixed by pinning the band. Omarchy has a command for that, documented in the manual's [Networking](https://omarchy.org/manual/networking/) chapter:

```bash
omarchy network band
omarchy network band 5
```

Intel BE200 and BE211 cards get an EHT workaround from Omarchy at install time, written to `/etc/modprobe.d/iwlwifi-disable-eht.conf`. If you have one of those cards and the file is missing, rerunning hardware detection with `sudo omarchy-apply-hardware --install-user $USER` reapplies the quirks.

If the machine upgraded from 3.x and every saved network vanished, the profiles are still in `/var/lib/iwd` as root, one file per SSID.

Evidence on the Omarchy kernel specifically is still thin. It reached everyone on 2026-09-15, one day before this page was checked, so treat reports about it as early.

## Related

- [Kernel panic after an update](/fix/kernel-panic-after-update-limine/)
- [Suspend will not resume](/fix/suspend-wont-resume-s2idle/)
- [Wi-Fi hardware notes](/hardware/wifi/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Releases and channels](/releases/channels/)
