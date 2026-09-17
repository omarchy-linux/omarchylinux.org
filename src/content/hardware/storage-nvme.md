---
title: "Storage, NVMe and filesystems on Omarchy"
description: "What works and what breaks for NVMe, SSD, btrfs, LUKS and the EFI partition on Omarchy 4.x, with real issue numbers, the Apple NVMe quirk script, and fixes."
answer: "NVMe and SATA storage on ordinary PC hardware works out of the box on Omarchy 4.x. The installer builds LUKS plus btrfs with snapper snapshots, and zram swap. The real breakage is in the EFI partition and the installer, not the drive: dirty or automounted ESPs, dual-disk dual-boot installs, and old Apple AHCI controllers. TRIM is not enabled by default."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "storage-nvme"
issueCount: 111
tags: [storage, nvme, btrfs, luks, esp, trim]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11979"
    title: "Issue #11979: 2013 MacBook Pro A1502: Apple AHCI SSD not detected, then pacstrap I/O error; cannot set libata.force=noncq"
    kind: issue
    author: "adriannoes"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12060"
    title: "Issue #12060: Kernel migration rejects valid FAT32 ESP discovered as systemd autofs"
    kind: issue
    author: "holystix04"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11821"
    title: "Issue #11821: Nothing in the update path measures ESP free space, including the post-transaction hook that writes the UKI"
    kind: issue
    author: "TechLuddite"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11368"
    title: "Issue #11368: BUG: Omarchy v4.0.2 does not detect eMMC as an installation drive"
    kind: issue
    author: "matcarfer"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11101"
    title: "Issue #11101: limine-install fails on software RAID / Intel RST ESP: 'Failed to parse disk and partition from source /dev/mdXpY'"
    kind: issue
    author: "patsonatorEFPL"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10826"
    title: "Issue #10826: NVMe suspend fix targets the dGPU on MacBooks with discrete graphics"
    kind: issue
    author: "passerini"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/8725"
    title: "Issue #8725: Error mounting an external hard drive"
    kind: issue
    author: "alwindoss"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7263"
    title: "Issue #7263: Dual-boot install fails when the free space is on a different disk than Windows itself"
    kind: issue
    author: "igor-gorohovsky"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/2229"
    title: "Issue #2229: Enable SSD TRIM"
    kind: issue
    author: "zsolt-donca"
    date: "2025-10-05"
  - url: "https://github.com/omacom/omarchy/pull/4840"
    title: "PR #4840: Enable SSD TRIM on LUKS-encrypted drives (closed unmerged)"
    kind: pr
    author: "n8himmel"
    date: "2026-03-01"
  - url: "https://github.com/omacom/omarchy/issues/2747"
    title: "Issue #2747: Unable to install Omarchy on a 4TiB ssd"
    kind: issue
    author: "boognevatz"
    date: "2025-10-22"
  - url: "https://github.com/omacom/omarchy/issues/4284"
    title: "Issue #4284: systemd-stub prints 'Failed to read *.cred, Volume corrupt' on boot (Limine + UKI)"
    kind: issue
    author: "FruitPnchSamuraiG"
    date: "2026-01-16"
  - url: "https://github.com/omacom/omarchy/issues/4192"
    title: "Issue #4192: Kernel 6.18.1-arch1-2 update breaks boot - missing vfat module prevents /boot mount"
    kind: issue
    author: "KhlifiIsmail"
    date: "2026-01-09"
  - url: "https://github.com/omacom/omarchy/issues/3850"
    title: "Issue #3850: Snapshots using up all disk space"
    kind: issue
    author: "gregg-cbs"
    date: "2025-12-11"
  - url: "https://github.com/omacom/omarchy/pull/5448"
    title: "PR #5448: Add dosfstools for /boot recovery (merged)"
    kind: pr
    author: "niraletter"
    date: "2026-04-29"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-suspend-nvme.sh"
    title: "install/hardware/apple/fix-suspend-nvme.sh in v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/snapper/root"
    title: "default/snapper/root in v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-update-requires-free-space"
    title: "bin/omarchy-update-requires-free-space in v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy Manual: System snapshots"
    kind: manual
credits:
  - name: "marko-builds"
    url: "https://github.com/marko-builds"
    for: "Traced the external NTFS mount error to the ntfs3 dirty flag and wrote the ntfsfix and udisksctl recovery steps"
  - name: "Damian626"
    url: "https://github.com/Damian626"
    for: "Found the missing -t vfat on the ESP mount that breaks dual-boot installs, and the live workaround"
  - name: "passerini"
    url: "https://github.com/passerini"
    for: "Showed the Apple NVMe suspend quirk pins the discrete GPU out of D3cold instead of the NVMe"
  - name: "TechLuddite"
    url: "https://github.com/TechLuddite"
    for: "Traced the update path end to end and showed the ESP is never measured for free space"
  - name: "n8himmel"
    url: "https://github.com/n8himmel"
    for: "Measured stale blocks on a LUKS install and wrote the TRIM enablement PR"
faq:
  - q: "Is TRIM enabled on Omarchy?"
    a: "Not by default. A stock LUKS install does not pass allow-discards through dm-crypt and does not enable fstrim.timer. There is no fstrim reference in the v4.0.4 tree outside the factory reset script. PR #4840 proposed both and was closed unmerged."
  - q: "What filesystem does the Omarchy installer use?"
    a: "btrfs on top of LUKS, with snapper snapshots of the root subvolume only. The mkinitcpio hook line in v4.0.4 is base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs."
  - q: "Why did my disk fill up with snapshots?"
    a: "That was issue #3850 on 3.x, when Omarchy also snapshotted /home. Release 3.6.0 dropped /home snapshots and btrfs quotas and kept the last 5 root snapshots. Old installs can still carry an @home/.snapshots subvolume."
  - q: "Does the installer see eMMC and RAID?"
    a: "Not reliably. eMMC can be missing from the live environment until the mmc modules are loaded by hand (#11368), and limine-install has no parser for /dev/mdXpY on software or Intel RST RAID (#11101)."
related: [boot-limine, suspend-sleep, t2-mac, vm]
draft: false
---

On a normal PC with an NVMe or SATA SSD, storage is the part of Omarchy you never think about. The drive is detected, the installer builds LUKS plus btrfs, snapshots happen before every update, and swap lives in compressed RAM. Almost everything filed under this component is really about something next to the drive: the EFI system partition, the installer's disk detection, or snapshot space.

## Status on 4.0.4

Checked against Omarchy 4.0.4 (2026-09-15) and the v4.0.4 source tree.

Our issue data tracks 111 issues touching storage, 60 of them open. Treat that number loosely: the match pattern catches any report from a machine that mentions an NVMe or an SSD. The genuinely storage specific failures fall into five groups.

1. The ESP. A dirty or automounted FAT32 `/boot` breaks updates and boots more often than the drive itself does.
2. Installer disk detection on unusual controllers: old Apple AHCI, eMMC, software RAID.
3. Dual-boot and multi-disk layouts.
4. Space accounting: snapshots on `/`, and nothing at all on the ESP.
5. TRIM, which is not configured.

There is no `omarchy-hw-storage` script. Storage has exactly one quirk script in the whole tree, and it is for Intel MacBooks.

## What Omarchy does automatically

From the v4.0.4 tree:

- **btrfs plus LUKS root.** `etc/mkinitcpio.conf.d/omarchy_hooks.conf` sets the hook line `base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs`. The `encrypt` hook is what decrypts at the Plymouth passphrase prompt.
- **Snapshots before updates.** `install/config/snapper.sh` installs `default/snapper/root`, which sets `NUMBER_LIMIT="5"` and `TIMELINE_CREATE="no"`, then disables `snapper-timeline.timer` and enables `snapper-cleanup.timer` and `limine-snapper-sync.service`. `etc/limine-entry-tool.d/omarchy-defaults.conf` pins `MAX_SNAPSHOT_ENTRIES=6`, one above the retention limit to cover the creation window. See the manual chapter on [system snapshots](https://omarchy.org/manual/system-snapshots/).
- **Swap in RAM.** `default/systemd/zram-generator.conf.d/90-omarchy.conf` gives zram a size equal to RAM with zstd compression and `swap-priority = 100`, above the `pri=0` disk swapfile that `omarchy-hibernation-setup` creates.
- **A free space guard on `/`.** `bin/omarchy-update-requires-free-space` refuses to update when the root filesystem has less than 10 GiB available. It measures `/` and nothing else.
- **Removable drive automount.** `default/hypr/autostart.lua` launches `udiskie --automount --no-notify --no-tray`, added in 4.0.0.
- **FAT repair tools.** `dosfstools` is a default package since 3.7.0, so `fsck.fat` exists before you need it. PR #5448 added it after the dirty ESP reports in #4192 and #4284.
- **Disk tooling.** `dua-cli` for usage, `omarchy-drive-info` and `omarchy-drive-select` for picking a device, `omarchy-drive-password` for the LUKS passphrase, and `omarchy-disk-speedtest` under Trigger then Speed Test, which uses O_DIRECT against NOCOW scratch files and reads throughput from the kernel block counters.
- **One quirk script.** `install/hardware/apple/fix-suspend-nvme.sh` matches MacBook8,1, 9,1 and 10,1 and MacBookPro13,1 through 14,3 by DMI product name, then installs `omarchy-nvme-suspend-fix.service` to write `0` into `d3cold_allowed` for the PCI device at `0000:01:00.0`, so the NVMe is not powered off across suspend.

What Omarchy does not do: enable `fstrim.timer`, or pass `allow-discards` to dm-crypt.

## Known problems

| Issue | Models affected | Status | Fixed in |
| --- | --- | --- | --- |
| [#11979](https://github.com/omacom/omarchy/issues/11979) Apple AHCI SSD never completes IDENTIFY, installer shows no disk, then pacstrap I/O errors | 2013 to 2015 MacBook Pro (A1502, MacBookPro11,1) | open | not fixed |
| [#11368](https://github.com/omacom/omarchy/issues/11368) eMMC missing from the installer's drive list | Cherry Trail mini PCs and tablets | open | not fixed |
| [#7263](https://github.com/omacom/omarchy/issues/7263) ESP mount fails with a SQUASHFS superblock error during dual-boot install | multi-disk PCs, Windows on a second NVMe | open, workaround | not fixed |
| [#12060](https://github.com/omacom/omarchy/issues/12060) kernel migration says `/boot` is not FAT32 when it is a systemd automount | any install whose ESP is not in fstab | open | not fixed |
| [#11101](https://github.com/omacom/omarchy/issues/11101) `limine-install` cannot parse `/dev/mdXpY` | software RAID and Intel RST FakeRAID | open, unconfirmed | not fixed |
| [#11821](https://github.com/omacom/omarchy/issues/11821) nothing checks ESP free space before the UKI is written | small ESPs | open | not fixed |
| [#10826](https://github.com/omacom/omarchy/issues/10826) NVMe suspend quirk pins the dGPU instead of the NVMe | MacBookPro13,3 and 14,3 | open | not fixed |
| [#8271](https://github.com/omacom/omarchy/issues/8271) full disk install wipes T1/T2 firmware along with the ESP | Touch Bar Intel MacBooks | open | not fixed |
| [#8725](https://github.com/omacom/omarchy/issues/8725) external NTFS drive refuses to mount | any USB drive last used on Windows | workaround | not fixed |
| [#2229](https://github.com/omacom/omarchy/issues/2229) TRIM blocked by dm-crypt, no periodic trim | every LUKS install | open, PR #4840 closed unmerged | not fixed |
| [#2747](https://github.com/omacom/omarchy/issues/2747) 4 TiB drive hits the msdos partition table sector limit | ThinkPad T560 with a 4 TB SATA SSD, 3.x installer | open | not fixed |
| [#4284](https://github.com/omacom/omarchy/issues/4284) systemd-stub reports a corrupt `.cred` from a dirty ESP | Limine plus UKI on 3.3.x | closed | 3.7.0, recovery tools only |
| [#3850](https://github.com/omacom/omarchy/issues/3850) snapshots consume the whole disk | btrfs installs on 3.x | closed | 3.6.0 |

Two notes on that table. #11101 was filed by an AI agent and has no maintainer reply or second reporter, so treat the diagnosis as a lead rather than a confirmed bug. #2747 is from the 3.1.1 archinstall era and has no 4.x confirmation, so it may not reproduce on the current ISO.

Where 3.x differs from 4.x: the dirty ESP class of failure (#4192, #4284) was largely a 3.x story, and the snapshot bloat in #3850 was addressed in 3.6.0 by dropping `/home` snapshots and btrfs quotas. An install that started on 3.x can still carry an `@home/.snapshots` subvolume that the new policy never cleans.

## Fixes that work

Work in this order.

1. **Measure both filesystems.** `df -h /` and `df -h /boot`. The update guard only looks at `/`, so a full ESP fails late, after the pacman transaction has committed.
2. **Clear old snapshots** if `/` is tight. `sudo snapper -c root list`, then `sudo snapper -c root delete <number>`. Rollback is covered in [rollback with snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).
3. **Repair a dirty ESP.** `sudo umount /boot`, `sudo fsck.fat -a /dev/nvme0n1p1` for your ESP device, then mount it again. This is the fix reporters confirmed on #4284, and `fsck.fat` is already installed.
4. **Give the ESP an explicit fstab entry** if `findmnt /boot` reports `autofs`. A plain `vfat` line makes systemd generate a normal `boot.mount`, and the Limine check then sees `vfat` instead of the automount layer (#12060).
5. **For the dual-boot ESP failure**, the community workaround on #7263 is to force the filesystem type on the two mount calls in the ISO configurator, adding `-t vfat`, then rerun the automated script. The upstream change is open as omarchy-iso#111 and is not in any release.
6. **External NTFS drives.** Install `ntfsprogs`, run `sudo ntfsfix --clear-dirty /dev/sdX1`, then mount from Files rather than with sudo, so udisks mounts it under your own user. Turning off Windows Fast Startup prevents it recurring.
7. **TRIM, if you want it.** Check with `lsblk --discard`: a `DISC-GRAN` of `0B` on the crypt device means discards are blocked. `sudo cryptsetup --allow-discards --persistent refresh root` opens the path and `sudo systemctl enable --now fstrim.timer` runs it weekly. This is your own change, not an Omarchy default, and it does leak which blocks are in use to anyone with physical access to the drive.
8. **Apple NVMe suspend.** Run `systemctl cat omarchy-nvme-suspend-fix.service` and compare its PCI address with `lspci`. If `01:00.0` is a GPU on your machine, the service is on the wrong device.

If the installer cannot see your drive at all, see [install fails or stalls](/fix/install-fails-or-stalls/). If you are already in emergency mode, see [you are in emergency mode after update](/fix/you-are-in-emergency-mode-after-update/).

## Report it

Run `omarchy debug`, which writes `/tmp/omarchy-debug.log` with `inxi -Farz`, `dmesg`, the current boot's warnings and errors from journalctl, and the package list. Use `omarchy debug --print --no-sudo` if you would rather not include dmesg.

Storage reports need four more things that `omarchy debug` does not single out, so paste them too:

- `lsblk -f` and `findmnt -no SOURCE,TARGET,FSTYPE,OPTIONS /boot /`
- `df -h / /boot`
- `lsblk --discard` if the question is TRIM
- the `ata`, `nvme`, `mmc` or `ntfs3` lines from `sudo dmesg`

Say which release you installed from and which one you are on now, because installer bugs and update bugs live in different repositories. Then file at [github.com/omacom/omarchy/issues](https://github.com/omacom/omarchy/issues), or send us a report through [hardware submit](/hardware/submit/).

## Related

- [Boot and Limine](/hardware/boot-limine/)
- [Suspend and sleep](/hardware/suspend-sleep/)
- [T2 Macs](/hardware/t2-mac/)
- [Creating a snapshot failed](/fix/creating-a-snapshot-failed-snapper/)
- [LUKS passphrase not accepted at boot](/fix/luks-passphrase-not-accepted-at-boot/)
- [Rollback with snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
