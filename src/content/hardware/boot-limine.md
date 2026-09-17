---
title: "Boot, Limine and LUKS on Omarchy 4.x"
description: "How the Limine bootloader, the UKI, LUKS unlock and snapshot booting work on Omarchy 4.0.4, what breaks on real machines, and the order to fix it in."
answer: "Omarchy boots Limine, which chainloads a unified kernel image named omarchy_<kernel>.efi and unlocks LUKS from the initramfs. Most failures are config layering, not hardware: a stale value in /etc/default/limine overrides everything else. Check `sudo limine-entry-tool --get-cmdline default` for root=, fix the file, run `sudo limine-mkinitcpio`, and boot an older entry or a snapshot meanwhile."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "boot-limine"
issueCount: 692
tags: [limine, boot, luks, uki, snapper, secure-boot]
sources:
  - url: "https://github.com/omacom/omarchy/issues/12143"
    title: "Issue #12143: Fresh Quattro install: Limine UKI chainload panics with efi: LoadImage failure (EFI_INVALID_PARAMETER) on older UEFI"
    kind: issue
    author: "keylimesoda"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12145"
    title: "Issue #12145: Direct boot keeps booting the old linux UKI after the linux-omarchy migration"
    kind: issue
    author: "ctarx"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11878"
    title: "Issue #11878: Stale/orphaned PARTUUID in /etc/default/limine silently overrides /etc/kernel/cmdline, breaking LUKS auto-unlock after update"
    kind: issue
    author: "pastorinj-pixel"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9826"
    title: "Issue #9826: limine-mkinitcpio-install calls limine-entry-tool --get-cmdline with wrong argument count, silently dropping root= from UKI cmdline"
    kind: issue
    author: "ThomsV897"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/10945"
    title: "Issue #10945: Limine-only update leaves limine_x64.efi unsigned, causes Secure Boot Violation lockout"
    kind: issue
    author: "LoboHacks"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/11526"
    title: "Issue #11526: Non-AVX2 CPUs can be left unbootable while updating to the fixed limine tooling"
    kind: issue
    author: "nischaljs"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/8047"
    title: "Issue #8047: btrfs-overlayfs is enabled by default, which makes snapshot rollback impossible"
    kind: issue
    author: "Cloud-Ops-Dev"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/6629"
    title: "Issue #6629: limine-snapper-sync inactive due to missing inotify-tools dependency and missing Snapper root configuration"
    kind: issue
    author: "mikemayuare"
    date: "2026-08-08"
  - url: "https://github.com/omacom/omarchy/issues/7989"
    title: "Issue #7989: omarchy-upgrade-to-quattro leaves archinstall's /EFI/Linux/arch-linux.efi Limine entry in place, so the default boot entry panics"
    kind: issue
    author: "michaelsahlmann"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/7867"
    title: "Issue #7867: Dual-boot install creates a redundant ESP instead of reusing the existing Windows one, and omarchy-refresh-limine permanently drops the Windows entry on every run"
    kind: issue
    author: "ThePeteJames"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7906"
    title: "Issue #7906: limine-scan (documented dual-boot step) generates a Windows entry that panics at boot"
    kind: issue
    author: "alkevintan"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11997"
    title: "Issue #11997: Installer's ENABLE_LIMINE_FALLBACK=no hides Omarchy from the Mac boot picker, leaving it unbootable after an NVRAM reset"
    kind: issue
    author: "makoni"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11101"
    title: "Issue #11101: limine-install fails on software RAID / Intel RST ESP: 'Failed to parse disk and partition from source /dev/mdXpY'"
    kind: issue
    author: "patsonatorEFPL"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/8814"
    title: "Issue #8814: Installer omits direct Omarchy UKI UEFI entry; first boot halts in Limine on dual-NVMe/dual-ESP system"
    kind: issue
    author: "majesticio"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/11442"
    title: "Issue #11442: Limine autoboot is cancelled by mouse movement"
    kind: issue
    author: "rva79"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/12096"
    title: "Issue #12096: hibernation remove leaves resume kernel parameters in the UKI (Limine drop-in not removed)"
    kind: issue
    author: "maandrij"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/4152"
    title: "Issue #4152: Limine bootloader entry doesn't get created on nvidia"
    kind: issue
    author: "28allday"
    date: "2026-01-08"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy manual: Dual Boot Install"
    kind: manual
credits:
  - name: "rva79"
    url: "https://github.com/rva79"
    for: "Found that Limine's mouse support cancels the autoboot countdown, and the mouse: no workaround"
  - name: "pastorinj-pixel"
    url: "https://github.com/pastorinj-pixel"
    for: "Traced a dead LUKS prompt to a stale PARTUUID in /etc/default/limine overriding /etc/kernel/cmdline"
  - name: "ctarx"
    url: "https://github.com/ctarx"
    for: "Showed that direct boot keeps booting the old kernel's UKI after the 4.0.4 linux-omarchy migration"
  - name: "keylimesoda"
    url: "https://github.com/keylimesoda"
    for: "Isolated the UKI chainload panic on older Lenovo UEFI and the ENABLE_UKI=no workaround"
  - name: "Cloud-Ops-Dev"
    url: "https://github.com/Cloud-Ops-Dev"
    for: "Documented the btrfs-overlayfs and limine-snapper-sync conflict that blocks snapshot restore"
faq:
  - q: "Can I go back to GRUB or systemd-boot?"
    a: "You can, but you lose snapshot booting. The manual states plainly that the snapshot feature only exists on Limine installs, which has been the default since Omarchy 2.0. Nothing in Omarchy 4.x offers a supported migration off Limine."
  - q: "My machine boots straight to the LUKS prompt and never shows the menu. Is Limine gone?"
    a: "No. That is direct boot, an EFI entry pointing at the UKI that skips Limine. To reach snapshots again, pick Limine from the firmware boot menu, or run Setup > Direct Boot a second time to remove the entry."
  - q: "Which kernel entry should I pick after updating to 4.0.4?"
    a: "The migration puts linux-omarchy first and deliberately leaves the stock linux kernel installed. If the new kernel misbehaves, select the older linux entry in Limine and report the difference."
related: [kernel-panic-after-update-limine, you-are-in-emergency-mode-after-update, secure-boot-violation-or-wont-boot-uefi, luks-passphrase-not-accepted-at-boot, rollback-with-snapper-and-limine, 3-to-4-quattro]
draft: false
---

Omarchy has used Limine as its bootloader since 2.0. On 4.x the chain is: firmware, Limine menu, a unified kernel image (UKI) on the EFI system partition, an initramfs that unlocks LUKS, then Btrfs root. Everything on this page was checked against the v4.0.4 source tree and against issues filed between August and September 2026.

## Status on 4.0.4

For a plain single-disk install from the ISO, this subsystem is boring in the good way: you get a themed menu, a snapshot submenu, a Plymouth splash, and a LUKS prompt. The failures cluster in five places, and almost none of them are hardware faults:

- **Config layering.** `/etc/default/limine` has the highest priority of every config layer. One stale value there overrides `/etc/kernel/cmdline` and every drop-in, silently.
- **Unusual firmware.** Old UEFI implementations, Apple firmware, and American Megatrends boards each break a different assumption.
- **Unusual storage.** Software RAID, Intel RST, dual NVMe with two ESPs.
- **Dual boot.** The documented `limine-scan` step and the second-ESP layout both have open bugs.
- **The 4.0.4 kernel switch.** Making `linux-omarchy` the default boot entry moved the UKI filename, which surprised anything pinned to the old path.

The component tracker counts 692 issues matching boot, Limine, LUKS, UEFI and kernel-panic terms, 387 of them still open, so treat the table below as the sharp edges rather than an exhaustive list.

## What Omarchy does automatically

Omarchy installs `limine-mkinitcpio-hook` and drives everything through `limine-entry-tool` drop-ins rather than hand-editing boot entries.

The packaged drop-in `/etc/limine-entry-tool.d/omarchy-defaults.conf` sets the UKI name to `omarchy`, turns on `ENABLE_LIMINE_FALLBACK` and `FIND_BOOTLOADERS`, keeps at most six snapshot entries, and appends a quiet kernel command line: `quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0`. It also appends `initramfs_async=0`, with a comment explaining why: kernel 7.1 unpacks the initramfs asynchronously, `plymouthd` then fails to read `/proc/cmdline`, and encrypted boots fall back to an unthemed text LUKS prompt.

`BOOT_ORDER` in that file reads `linux-t2, linux-omarchy, linux-omarchy-*, *, *fallback, Snapshots`. T2 Macs stay on their own kernel on purpose; everything else prefers the Omarchy kernel.

Hardware quirks write their own drop-ins during install. `install/hardware/apple/fix-t2.sh` adds `intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep` for T2 Macs along with the `linux-t2` kernel; `install/hardware/intel/fred.sh` adds `fred=on` on Panther Lake; `install/hardware/asus/fix-asus-ptl-b9406-display.sh` adds `xe.enable_panel_replay=0` on the ExpertBook B9406. Those are the only shipped scripts that touch the kernel command line.

Updates carry migrations that rebuild the boot image when they must. Migration `1786482992` compares the running `/proc/cmdline` against the defaults drop-in and runs `limine-mkinitcpio` if parameters are missing. Migration `1789325478`, the one that landed in 4.0.4, installs `linux-omarchy`, rewrites `BOOT_ORDER`, rebuilds that kernel's entry, then verifies with `limine-entry-tool --tree` and refuses to mark itself complete if the entry is absent. It leaves the old kernel installed on purpose so you have something to fall back to.

Snapshots come from `install/config/snapper.sh`, which writes a root config limited to five snapshots with the timeline disabled, then enables `snapper-cleanup.timer` and `limine-snapper-sync.service`. `omarchy-snapshot create` runs before updates and labels each snapshot with the Omarchy version.

Two commands are worth knowing. `omarchy-refresh-limine` moves `/boot/limine.conf` to `.bak`, copies the packaged default over it, then runs `limine-update` and `limine-snapper-sync`. `omarchy-setup-direct-boot` adds or removes an `efibootmgr` entry pointing straight at the UKI, and refuses to run on American Megatrends and Apple firmware.

## Known problems

| Issue | Models affected | Status | Fixed in |
| --- | --- | --- | --- |
| [#11878](https://github.com/omacom/omarchy/issues/11878) stale PARTUUID in `/etc/default/limine` kills the LUKS prompt | any LUKS plus Btrfs install | open | not yet |
| [#9826](https://github.com/omacom/omarchy/issues/9826) `root=` silently dropped from the UKI command line | any | open | not yet |
| [#8047](https://github.com/omacom/omarchy/issues/8047) btrfs-overlayfs blocks `limine-snapper-restore` | any Btrfs install | open | not yet |
| [#6629](https://github.com/omacom/omarchy/issues/6629) `limine-snapper-sync` inactive, no snapshot entries | any | open | not yet |
| [#12145](https://github.com/omacom/omarchy/issues/12145) direct boot keeps booting the old kernel after 4.0.4 | any with direct boot enabled | open | not yet |
| [#12143](https://github.com/omacom/omarchy/issues/12143) UKI chainload panic, `EFI_INVALID_PARAMETER` | ThinkPad Yoga 11e, older UEFI | open | not yet |
| [#10945](https://github.com/omacom/omarchy/issues/10945) Secure Boot Violation after a Limine-only update | sbctl custom-key setups | open | not yet |
| [#11526](https://github.com/omacom/omarchy/issues/11526) non-AVX2 CPU left unbootable mid-update | Celeron N4000 and similar | open | tooling fixed, path to it is not |
| [#7989](https://github.com/omacom/omarchy/issues/7989) leftover archinstall entry panics as the default | 3.x installs upgraded to Quattro | open | not yet |
| [#7867](https://github.com/omacom/omarchy/issues/7867) second ESP created, Windows entry dropped on refresh | dual-boot with Windows | open | not yet |
| [#7906](https://github.com/omacom/omarchy/issues/7906) `limine-scan` writes an uppercase Windows path that panics | dual-boot with Windows | open | not yet |
| [#11997](https://github.com/omacom/omarchy/issues/11997) no `BOOTX64.EFI`, invisible in the Mac boot picker | Intel Macs | open | not yet |
| [#11101](https://github.com/omacom/omarchy/issues/11101) `limine-install` fails on RAID or Intel RST ESP | software RAID, Intel RST | open | not yet |
| [#8814](https://github.com/omacom/omarchy/issues/8814) first boot halts in Limine, no direct UKI entry | dual-NVMe, dual-ESP | open | not yet |
| [#11442](https://github.com/omacom/omarchy/issues/11442) mouse movement cancels the autoboot countdown | desktops with a USB mouse | open | not yet |
| [#12096](https://github.com/omacom/omarchy/issues/12096) removing hibernation leaves `resume=` in the UKI | hibernation users | open | not yet |

Three of these are worth a sentence more. In #11878 the reporter's boot dropped to an emergency shell with no passphrase prompt at all, because a PARTUUID in `/etc/default/limine` matched no partition on the disk and outranked the correct one in `/etc/kernel/cmdline`. Nothing validates that value before baking it into an entry. In #11442 the reporter points out that `omarchy debug` is useless for this class of bug, since the hang happens in Limine before the kernel starts. In #12143 the reporter got a native-Linux entry generated with `ENABLE_UKI=no`, but says openly that a full boot was not confirmed, so treat that one as a lead rather than a fix.

The 4.0.4 kernel switch has its own tail. #12187 reports a hybrid NVIDIA laptop freezing seconds after login on `linux-omarchy` while the stock kernel is fine, on a machine carrying prebuilt `nvidia-open` rather than the DKMS package Omarchy installs.

Where 3.x differed: the boot failures were mostly install-time. In #4152, January 2026, NVIDIA machines finished a 3.3.x install with only an EFI fallback entry in Limine, and @ryanrhughes closed it against the v3.3.2 release. The 4.x failures are config-layer and upgrade-path failures instead.

## Fixes that work

Work in this order.

1. **Do not reinstall.** Limine keeps older entries. Arrow to the previous kernel or a snapshot and boot that first, then fix from a working desktop. With direct boot enabled you must pick Limine from the firmware boot menu to see the snapshot submenu at all.
2. **If you land in an emergency shell or get no LUKS prompt**, check the effective command line with `sudo limine-entry-tool --get-cmdline default` and look for `root=`. Compare any UUID or PARTUUID in `/etc/default/limine` against `blkid`. Fix the file, then `sudo limine-mkinitcpio`.
3. **If the menu itself is wrong**, run `omarchy-refresh-limine`. It backs up your current `/boot/limine.conf` to `.bak` first. Be aware it replaces the file wholesale, so a hand-added Windows entry does not survive.
4. **If snapshots are missing from the menu**, check `systemctl status limine-snapper-sync.service` and confirm a root config exists with `sudo snapper --csvout list-configs`. If there is none, rerun the packaged `install/config/snapper.sh`.
5. **If the countdown never expires**, add `mouse: no` to the global section of `/boot/limine.conf`, above the first entry.
6. **If Secure Boot refuses Limine after an update**, re-sign and verify with `sbctl` before rebooting again.
7. **If nothing boots**, use the ISO as a rescue system, `arch-chroot` into the install, repair the config, and run `limine-mkinitcpio` there.

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, `dmesg`, the current boot's warnings and errors from `journalctl`, and the full package list, then offers to upload it with a 24 hour expiry. Use `omarchy debug --print --no-sudo` if you would rather read it first.

For a boot bug that log is often empty of the useful part, because the failure happened before the kernel. Add, by hand: a phone photo of the panic text, `efibootmgr -v`, `sudo limine-entry-tool --tree`, `ls /boot/EFI/Linux/`, and the contents of `/etc/default/limine` and `/etc/limine-entry-tool.d/`. Say which kernel entry you picked and whether the other one boots. That last detail is what made #12187 and #12145 readable.

## Related

- [Kernel panic after update](/fix/kernel-panic-after-update-limine/)
- [You are in emergency mode after update](/fix/you-are-in-emergency-mode-after-update/)
- [Secure Boot violation or will not boot UEFI](/fix/secure-boot-violation-or-wont-boot-uefi/)
- [LUKS passphrase not accepted at boot](/fix/luks-passphrase-not-accepted-at-boot/)
- [Creating a snapshot failed](/fix/creating-a-snapshot-failed-snapper/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Should you dual boot](/switch/should-you-dual-boot/)
- [T2 Macs](/hardware/t2-mac/)
- [Storage and NVMe](/hardware/storage-nvme/)
