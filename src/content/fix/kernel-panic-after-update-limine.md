---
title: "Kernel panic after an Omarchy update (Limine boot menu)"
description: "Kernel panic or a dead boot after an Omarchy update: pick another kernel in the Limine menu, undo the 4.0.4 linux-omarchy default, or roll back a snapshot."
answer: "Boot a different kernel. Omarchy 4.0.4 installs linux-omarchy and makes it the first Limine entry, but it leaves your previous kernel installed. At the Limine menu pick the entry named linux, or boot a pre-update snapshot. To make that stick, edit BOOT_ORDER in /etc/default/limine and run sudo limine-mkinitcpio. On 3.x the cause was a stale limine.conf, fixed in 3.1.6."
appliesTo:
  from: "3.x"
status: workaround
category: boot
issueCount: 19
errorStrings:
  - "Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)"
  - "PANIC: efi: LoadImage failure (0x8000000000000002)"
  - "ERROR: Failed to mount '/dev/mapper/omarchy_root' on real root"
  - "You are now being dropped into an emergency shell."
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [boot, limine, kernel, linux-omarchy, update, rollback]
sources:
  - url: "https://github.com/omacom/omarchy/pull/11845"
    title: "PR #11845: Migrate to linux-omarchy except on T2 Macs"
    kind: pr
    author: "ryanrhughes"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/12087"
    title: "Issue #12087: Omarchy Linux kernel breaks boot"
    kind: issue
    author: "vcelletti"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12097"
    title: "Issue #12097: linux-omarchy 7.2.5-3 boots to emergency shell on MacBookAir6,1"
    kind: issue
    author: "nordbergmikael"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12119"
    title: "Issue #12119: linux-omarchy 7.2.5-3 fails on 2016 MacBook Pro (MacBookPro13,3) unless intel_iommu=off"
    kind: issue
    author: "dzanaga"
    date: "2026-09-16"
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
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/3231"
    title: "Issue #3231: Kernel panic after update"
    kind: issue
    author: "RodriMora"
    date: "2025-11-07"
  - url: "https://github.com/omacom/omarchy/discussions/3236"
    title: "Discussion #3236: Kernel Panic After Update Fix Guide"
    kind: discussion
    author: "ryanrhughes"
    date: "2025-11-07"
  - url: "https://github.com/omacom/omarchy/issues/3335"
    title: "Issue #3335: Kernel panic after update: /boot/EFI/Limine/limine.conf not synced with /boot/limine.conf"
    kind: issue
    author: "tsurelad"
    date: "2025-11-11"
  - url: "https://github.com/omacom/omarchy/discussions/6094"
    title: "Discussion #6094: Kernel panic (ReBAR and Above 4G Decoding on Z790 with 128 GB)"
    kind: discussion
    author: "dollebrekel"
    date: "2026-06-14"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Wrote the Limine recovery guide for the 3.x panic and authored the linux-omarchy migration"
  - name: "whargrove"
    url: "https://github.com/whargrove"
    for: "Found that booting the Omarchy EFI entry directly skips a broken Limine config"
  - name: "tsurelad"
    url: "https://github.com/tsurelad"
    for: "Traced the 3.x panic to a stale limine.conf next to the EFI binary"
  - name: "dzanaga"
    url: "https://github.com/dzanaga"
    for: "Isolated intel_iommu=off as the workaround on MacBookPro13,3"
  - name: "ctarx"
    url: "https://github.com/ctarx"
    for: "Showed that direct boot keeps launching the old UKI after the kernel migration"
  - name: "Nord-Nogare"
    url: "https://github.com/Nord-Nogare"
    for: "Linked the post-4.0.4 NVIDIA freeze to missing prebuilt modules for the new kernel"
faq:
  - q: "Does Omarchy 4.0.4 remove my old kernel?"
    a: "No. The migration installs linux-omarchy and linux-omarchy-headers and leaves the previous kernel installed on purpose, so you still have a working entry in the Limine menu if the new one will not boot."
  - q: "Can I just uninstall the Omarchy kernel?"
    a: "Yes. The migration writes a machine-wide marker at /var/lib/omarchy/migrations/1789325478 and exits early when it exists, so removing linux-omarchy will not be undone by the next update."
  - q: "I never see the Limine menu, it goes straight to the disk password."
    a: "You have direct boot enabled. Open your firmware boot menu and choose the Limine entry instead of the Omarchy entry to get the kernel and snapshot list back."
related: [you-are-in-emergency-mode-after-update, black-screen-after-login, nvidia-drivers-omarchy-4, secure-boot-violation-or-wont-boot-uefi]
draft: false
---

Checked against Omarchy v4.0.4 (2026-09-15) and the v3.8.4 and v4.0.x source trees.

A panic right after an update is almost never a broken disk. It is a boot entry pointing at something the machine cannot run. Omarchy keeps the previous kernel installed for exactly this reason, so the first move is to boot the other entry, not to reinstall.

## The fix

**1. Get back to the Limine menu.** Power cycle the machine. If Limine's countdown is running, press a key to stop it. If the machine goes straight to the disk password prompt, you have direct boot enabled, so open your firmware boot menu (usually F12, F10 or Esc) and pick the Limine entry rather than the Omarchy one.

**2. On 4.0.x, pick a different kernel.** Since 4.0.4 the default entry is `linux-omarchy`. Migration `1789325478.sh` installs it, sets `BOOT_ORDER="linux-omarchy, linux-omarchy-*, *, *fallback, Snapshots"` in `/etc/default/limine`, and deliberately leaves your old kernel installed. Its own comment says the old kernel stays "so it remains available if the new one cannot boot". Arrow down to the entry named `linux` (or `linux-lts`, or `linux-ptl` on a Panther Lake machine) and press Enter. T2 Macs are skipped by the migration and keep `linux-t2` first. Several people on 4.0.4 report exactly this: the new entry fails, the stock entry boots the same install untouched.

**3. Make it stick.** Once you are logged in, edit the boot order so the next reboot does not drop you back into the panic:

```bash
sudo nano /etc/default/limine
```

Change the `BOOT_ORDER` line the migration appended to put your working kernel first, for example:

```
BOOT_ORDER="linux, linux-omarchy, linux-omarchy-*, *, *fallback, Snapshots"
```

Then rebuild the entries:

```bash
sudo limine-mkinitcpio
```

`/etc/default/limine` takes priority over the packaged drop-in at `/etc/limine-entry-tool.d/omarchy-defaults.conf`, so this wins.

**4. Or remove the new kernel outright.** If you do not want it at all:

```bash
sudo pacman -Rns linux-omarchy linux-omarchy-headers
sudo limine-mkinitcpio
```

The migration records completion at `/var/lib/omarchy/migrations/1789325478` and exits early when that file exists, so an update will not silently reinstall it.

**5. If nothing boots, roll back.** Every Omarchy update takes a Snapper snapshot first. From the Limine menu choose a snapshot dated before the update, boot it, then click the notification or run `omarchy-snapshot restore`. That restores the root filesystem, not `/home`. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/) and the [system snapshots manual chapter](https://omarchy.org/manual/system-snapshots/).

**On 3.x the fix is different.** In November 2025 Limine v10.3.0 changed its config search order to prefer a `limine.conf` sitting next to the EFI binary. A stale `/boot/EFI/limine/limine.conf` left over from an older install then won over Omarchy's `/boot/limine.conf` and pointed at kernel files that no longer existed. The recovery, from ryanrhughes' guide, is to highlight the entry, press `e`, remove the two lines the guide marks, set `protocol: efi_chainload`, add `image_path: boot():/EFI/Linux/omarchy_linux.efi` (on a T2 Mac, `omarchy_linux-t2.efi`) and press F10. Then run Update > Omarchy so the hotfix migration deletes the stray config. Omarchy 3.1.6 shipped that hotfix, but people on 3.1.7 in issue #3335 still found `/boot/EFI/Limine/limine.conf` in place afterwards and had to `sudo rm` it themselves, so check.

## Verify it worked

Check which kernel actually booted:

```bash
uname -r
```

An Omarchy kernel reports something like `7.2.5-3-omarchy`; the stock Arch kernel reports `7.2.3-arch1-3`. Then confirm the menu matches what you intended:

```bash
sudo limine-entry-tool --tree
```

On 3.x, or after any Limine confusion, confirm there is exactly one config:

```bash
lt --level 3 /boot
```

Only `/boot/limine.conf` should exist (`lt` is Omarchy's `eza --tree` alias; plain `find /boot -name limine.conf` works too). If a second one has reappeared under `/boot/EFI/limine/`, delete it. `omarchy-refresh-limine` only resets `/boot/limine.conf` itself and rebuilds the entries; it does not touch the copy next to the EFI binary.

## Why it happens

Three separate causes wear the same face.

The 4.0.4 kernel swap is the current one. Omarchy 4.0.4 shipped the bespoke `linux-omarchy` kernel to everyone and made it the first boot entry. The stable channel carries 7.2.5-3. It is a different config from Arch's 7.2.3, and the differences bite on older or unusual hardware: a MacBookPro13,3 needs `intel_iommu=off` before NVMe, the Apple SPI keyboard and amdgpu come up at all, a MacBookAir6,1 drops both the normal and fallback entries into the emergency shell, and a Lenovo P1 Gen5 reboots partway through. The MacBook case has a named cause: dzanaga diffed the two kernel configs and the Omarchy kernel sets `CONFIG_INTEL_IOMMU_DEFAULT_ON=y` where Arch leaves it unset. A Surface Pro 4 owner in the same thread lost the touchscreen to DMAR faults for the same reason, and both fixed it with a drop-in in `/etc/limine-entry-tool.d/` containing `KERNEL_CMDLINE[default]+=" intel_iommu=off"` followed by `sudo limine-update`. Out-of-tree modules are a second trap. On a hybrid NVIDIA laptop running the prebuilt `nvidia-open` package rather than the DKMS one Omarchy installs, the modules exist only under the stock kernel's module directory, so the new default boots with no NVIDIA driver and freezes seconds after login.

Boot plumbing is the second cause. Omarchy boots a unified kernel image chainloaded by Limine, and some firmware refuses it. On a ThinkPad Yoga 11e with a fresh 4.0.4 install, the chainload panics with `PANIC: efi: LoadImage failure (0x8000000000000002)`, which is `EFI_INVALID_PARAMETER`, before Linux starts at all. The reporter set `ENABLE_UKI=no` in `/etc/default/limine`, reran `limine-mkinitcpio` from the ISO's chroot, and got a plain `protocol: linux` entry instead of the UKI one. He had not yet confirmed that entry boots all the way, so treat it as a lead rather than a fix.

Direct boot is the third. With direct boot on, the firmware launches a UKI by filename and never consults Limine's boot order. The kernel migration only edits `BOOT_ORDER`, so the firmware entry keeps launching `omarchy_linux.efi` and you stay on the old kernel with no warning. That is benign, but it means changing `BOOT_ORDER` does nothing until you turn direct boot off.

## If that did not work

If you cannot reach Limine at all, boot the Omarchy ISO, press Ctrl+C and exit out to a shell, then mount your EFI partition and inspect it. Deleting a stale `/mnt/boot/EFI/limine/limine.conf` is the 3.x repair.

If the panic survives every kernel entry and every snapshot, it is probably not the kernel. Check firmware settings first: on a Z790 board with an RTX 5090 and 128 GB of RAM, Resizable BAR plus Above 4G Decoding fragmented the memory map badly enough that even the live ISO could not boot, and turning both off fixed it.

If the Omarchy kernel is the only one that fails and you want it fixed rather than skipped, boot the stock kernel and capture the failed boot with `journalctl -b -1 -k`, then open an issue with that log, `uname -a` and `cat /proc/cmdline`. Two of the open reports already have a cause (the IOMMU default and the missing NVIDIA modules). The P1 Gen5 and MacBookAir6,1 reports do not, because neither has produced a kernel log from the failed boot yet.

## Related

- [You are in emergency mode after update](/fix/you-are-in-emergency-mode-after-update/)
- [Black screen after login](/fix/black-screen-after-login/)
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Secure Boot violation or will not boot (UEFI)](/fix/secure-boot-violation-or-wont-boot-uefi/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Boot and Limine hardware notes](/hardware/boot-limine/)
- [Omarchy 4.0.4 release notes](/releases/v4.0.4/)
