---
title: "Should you dual boot Omarchy with Windows or macOS?"
description: "Dual booting Omarchy with Windows works but the free-space installer has real traps. macOS dual boot is unsupported. When to use a VM instead."
answer: "Dual boot Omarchy with Windows only if you actually need to reboot into Windows for games or GPU work, and only after shrinking the Windows partition from inside Windows Disk Management. Never resize NTFS or Btrfs with the installer's cfdisk step. Do not dual boot with macOS, it is unsupported and the installer wipes the drive. For Office or Teams, use the Windows VM instead."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [dual-boot, windows, macos, limine, secure-boot, installer]
sources:
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy manual: Dual Boot Install"
    kind: manual
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
  - url: "https://omarchy.org/manual/windows-vm/"
    title: "Omarchy manual: Windows VM"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/7903"
    title: "Issue #7903: Installer partitioning step lets users resize a live Windows NTFS partition with cfdisk, resulting in unbootable Windows"
    kind: issue
    author: "alkevintan"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8954"
    title: "Issue #8954: Installer partition resize corrupts BTRFS filesystem, breaks existing OS boot"
    kind: issue
    author: "sylvainobegi"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/7867"
    title: "Issue #7867: Dual-boot install creates a redundant ESP instead of reusing the existing Windows one, and `omarchy-refresh-limine` permanently drops the Windows entry on every run"
    kind: issue
    author: "ThePeteJames"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7906"
    title: "Issue #7906: limine-scan (documented dual-boot step) generates a Windows entry that panics at boot"
    kind: issue
    author: "alkevintan"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7270"
    title: "Issue #7270: Bootloader install doesn't probe for other OSes"
    kind: issue
    author: "bjornharrtell"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/10598"
    title: "Issue #10598: 4.0.2 free-space install registers no UEFI boot entry, boots straight to Windows"
    kind: issue
    author: "exergonic"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7263"
    title: "Issue #7263: Dual-boot install fails when the free space is on a different disk than Windows itself"
    kind: issue
    author: "igor-gorohovsky"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7846"
    title: "Issue #7846: Omarchy Installation Causes GRUB to Stop Detecting Existing Ubuntu and Windows Installations"
    kind: issue
    author: "cn0xroot"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7666"
    title: "Issue #7666: Can Omarchy be installed as a dual-boot setup alongside macOS 10.15 without formatting the entire disk?"
    kind: issue
    author: "foobra"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/12045"
    title: "Issue #12045: Secure Boot UKI chainload panics on MSI firmware (LoadImage failure 0x800000000000000f); ENABLE_UKI=no workaround"
    kind: issue
    author: "fenfenau"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/10945"
    title: "Issue #10945: Limine-only update leaves limine_x64.efi unsigned, zz-sbctl.hook glob never matches BOOTX64.EFI (case-sensitive), causes Secure Boot Violation lockout"
    kind: issue
    author: "LoboHacks"
    date: "2026-09-09"
credits:
  - name: "alkevintan"
    url: "https://github.com/alkevintan"
    for: "Traced the cfdisk NTFS resize data loss and the case-sensitive Windows path in limine-scan entries"
  - name: "ThePeteJames"
    url: "https://github.com/ThePeteJames"
    for: "Documented the duplicate ESP and the Windows entry being wiped by omarchy-refresh-limine"
  - name: "exergonic"
    url: "https://github.com/exergonic"
    for: "Showed that a free-space install can finish with no UEFI boot entry registered at all"
faq:
  - q: "Can I dual boot Omarchy and macOS on a Mac?"
    a: "No. The official Mac support chapter says Omarchy only supports being the only OS installed, and the install wipes the drive so macOS is no longer bootable. You can restore macOS later through Internet Recovery."
  - q: "Do I need to turn off BitLocker before installing Omarchy alongside Windows?"
    a: "Yes. The manual says the free-space install is not compatible with BitLocker because BitLocker encrypts the whole drive rather than a partition. Decrypt from Settings, Privacy and Security, Device encryption before you start."
  - q: "Can I keep Secure Boot enabled for Windows?"
    a: "It is not the default and it is not smooth. Omarchy installs with Secure Boot off. Users who enroll custom keys with sbctl have reported both a boot panic chainloading the UKI on some firmware and a signing hook gap that can lock you out entirely."
  - q: "Is running Omarchy in a VM a real substitute?"
    a: "For evaluating it, yes. For daily use, no. A VM costs you GPU acceleration and some of the Hyprland animation smoothness. Use it to decide, then install on metal if you commit."
related: [day-one-checklist, what-replaces-what, from-windows]
draft: false
---

Short version. Dual booting Omarchy with Windows works and is documented upstream, but the free-space install path has a cluster of open bugs that can leave you with no boot menu, no Windows entry, or a corrupted neighbouring filesystem. Dual booting with macOS is not supported at all. Checked against v4.0.4.

## The decision

| Your situation | What to do |
| --- | --- |
| Windows lives on a separate physical drive and your firmware lets you pick the boot drive | Dual boot. This is the lowest risk layout. |
| Windows and Omarchy share one drive | Dual boot is possible, but shrink Windows from inside Windows first and read the traps below. |
| You need Windows only for Office, Teams, or one business app | Skip dual boot. Use the Windows VM that Omarchy ships. |
| You need Windows for anti-cheat games or CUDA work | Dual boot, and expect Secure Boot friction. |
| You want to keep macOS on an Apple machine | Do not. It is unsupported and the installer wipes the drive. |
| You are still deciding whether you like Omarchy | Do not touch your disk yet. Run it in a VM first. |

## What a dual-boot install actually does

The installer offers a **Free space install** option after you pick a disk. Instead of wiping the drive it uses unallocated space, and it still applies LUKS encryption to the Omarchy partition by default. Limine becomes the bootloader. Other operating systems do not appear in the Limine menu automatically, so the manual tells you to run `limine-scan` afterwards and add them by hand.

Two things follow from that design. Your Omarchy partition is encrypted but your Windows partition is not, so LUKS protects only half the machine. And the boot menu is a file that Omarchy manages, which is where most of the pain comes from.

## The traps, in the order they bite

**Do not resize a partition with the installer's `cfdisk` step.** This is the most expensive mistake on the list. `cfdisk` rewrites the partition table only, it does not touch the filesystem inside. Shrinking a live NTFS volume this way left Windows with `UNMOUNTABLE_BOOT_VOLUME` in [issue #7903](https://github.com/omacom/omarchy/issues/7903), with data beyond the new boundary already gone. The same shape of failure hit a Btrfs CachyOS install in [issue #8954](https://github.com/omacom/omarchy/issues/8954). Shrink from Windows Disk Management, or from the other distro's own tools, before you boot the Omarchy ISO. Both issues were open on 2026-09-16.

**Turn BitLocker off first.** The manual is explicit that this install method is not compatible with BitLocker, because BitLocker encrypts the whole drive rather than a partition. Decrypt under Settings, Privacy and Security, Device encryption. It can take hours, so start it the day before.

**Expect the boot entry to be wrong.** Three separate open reports describe the same family of failure. In [#7270](https://github.com/omacom/omarchy/issues/7270) the bootloader install does no OS probing at all. In [#7867](https://github.com/omacom/omarchy/issues/7867) the installer created a second EFI system partition instead of reusing the Windows one, so the firmware never surfaced Omarchy in its top level boot list. In [#10598](https://github.com/omacom/omarchy/issues/10598) on 4.0.2 the EFI partition was fully populated but no NVRAM entry was registered, and the machine booted straight to Windows.

**`limine-scan` can produce an entry that panics.** The documented step reads EFI paths from `efibootmgr`, which reports Windows in uppercase. Limine's FAT driver does case-sensitive lookups, so the entry can fail with an image not found panic. That is [issue #7906](https://github.com/omacom/omarchy/issues/7906), open, with the reporter noting that fixing the casing in `/boot/limine.conf` made Windows boot.

**`omarchy-refresh-limine` erases your Windows entry.** This is confirmed in the v4.0.4 source, not just in a report. The script moves `/boot/limine.conf` to `limine.conf.bak` and copies in the packaged default, and that default contains only theme and timeout settings with no OS entries at all. Anything you added by hand is gone. The backup is your recovery path. Keep your own copy of the working `limine.conf` somewhere outside `/boot`.

**Free space on a different disk to Windows is fragile.** [Issue #7263](https://github.com/omacom/omarchy/issues/7263) reports the install dying while mounting the ESP in a two-NVMe layout. If you have two drives, the safest arrangement is one operating system per drive and switching between them from the firmware boot menu, not from Limine.

**Other Linux installs are not handled either.** [Issue #7846](https://github.com/omacom/omarchy/issues/7846) describes an existing Ubuntu GRUB setup losing sight of Windows and Ubuntu after an Omarchy install, with Ubuntu's `update-grub` not detecting Omarchy either.

## macOS: the answer is no

The Mac support chapter states plainly that Omarchy only supports being the only OS installed, and that the drive is wiped during installation so macOS will no longer be bootable. You can restore macOS afterwards through Internet Recovery. That is the official position as of v4.0.4.

[Issue #7666](https://github.com/omacom/omarchy/issues/7666) asks exactly this question and is open. One commenter reports succeeding on a 2020 T2 MacBook Pro with macOS still bootable, and a later commenter in the same thread reports being dropped into an emergency shell after following similar steps. Treat that as one person's result on specific hardware, not as a supported path. On Apple Silicon, dual booting is not on the table at all.

## Secure Boot

Omarchy installs with Secure Boot off, and the documentation tells you to disable it. That matters for dual booters, because some Windows anti-cheat systems require Secure Boot to stay on.

There is no official custom key enrollment flow. People who do it with `sbctl` have hit real problems. [Issue #12045](https://github.com/omacom/omarchy/issues/12045), filed 2026-09-16 against 4.0.3, reports the default UKI boot entry panicking with a `LoadImage` failure on MSI AMI firmware even after correctly signing everything, with switching the entry to Limine's native `protocol: linux` as the workaround. [Issue #10945](https://github.com/omacom/omarchy/issues/10945) is worse: a Limine-only package update can leave `limine_x64.efi` unsigned, producing a Secure Boot Violation lockout on the next boot. Both were open on 2026-09-16.

If you need Secure Boot on for Windows, the honest recommendation today is to put Omarchy on a separate drive and switch drives in firmware, or to keep Windows on the machine it already owns.

## The VM alternative

Two directions, and they solve different problems.

**Windows inside Omarchy.** Omarchy ships a Windows 11 Pro VM through Docker, installed from the menu under Install, Windows. It gives you sound, microphone, a shared clipboard, display scaling, and a `~/Windows` shared folder. There is no GPU passthrough, so it is fine for Office and useless for gaming or video editing. If Office is your only reason to keep Windows, this removes the reason to dual boot at all. See the [Windows VM chapter](https://omarchy.org/manual/windows-vm/).

**Omarchy inside Windows or macOS.** If you are still evaluating, run it as a guest first. See [what breaks in a VM](/run/what-breaks-in-a-vm/), plus the per-host pages for [VirtualBox](/run/virtualbox/), [VMware](/run/vmware-workstation-fusion/), [Hyper-V](/run/hyper-v/), [WSL2](/run/wsl2/) and [UTM on Apple Silicon](/run/utm-apple-silicon/).

## If you dual boot anyway

1. Back up. Not a snapshot, a real backup on another device.
2. Decrypt BitLocker and let it finish.
3. Shrink the Windows volume from Windows Disk Management, then reboot into Windows once to confirm it still works.
4. Boot the Omarchy ISO and choose **Free space install**. Do not resize anything from `cfdisk`.
5. After first boot, run `limine-scan` and add Windows. If the entry panics, check the path casing in `/boot/limine.conf` against the real files on the EFI partition.
6. Copy the working `/boot/limine.conf` somewhere in your home directory. You will need it after any `omarchy-refresh-limine` run.
7. Learn how to reach the firmware boot menu on your machine before you need it.

## What to watch for on newer versions

Every issue cited here was open on 2026-09-16 against 4.0.x, and the dual-boot manual chapter is byte for byte identical across v4.0.0 through v4.0.4, so nothing in the documented procedure changed across the point releases. The next release is announced as Quattro RS 4.5. Re-check the ESP reuse behaviour, whether the bootloader install gains OS probing, and whether `omarchy-refresh-limine` learns to preserve non-Omarchy entries before you trust an upgrade on a dual-boot machine. Read the [before you update checklist](/upgrade/before-you-update-checklist/) first, and know how to [roll back with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

## Related

- [Day one checklist](/switch/day-one-checklist/)
- [What replaces what](/switch/what-replaces-what/)
- [Coming from Windows](/switch/from-windows/)
- [Limine and boot](/hardware/boot-limine/)
