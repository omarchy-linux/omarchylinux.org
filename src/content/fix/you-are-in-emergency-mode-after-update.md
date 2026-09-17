---
title: "You are in emergency mode after an Omarchy update"
description: "Omarchy drops to emergency mode after an update. Boot a Limine snapshot, then repair the kernel cmdline, the LUKS selector, or the failed fstab mount."
answer: "Reboot and pick a dated snapshot entry in the Limine menu instead of the normal one. That almost always boots. Then remount root read-write, check systemctl --failed and journalctl -xb, and rebuild the boot image with limine-mkinitcpio. The usual causes are a UKI built without root=, a LUKS unlock parameter the initramfs does not understand, or a mkinitcpio run that failed during the update."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: boot
issueCount: 11
errorStrings:
  - "You are in emergency mode"
  - "You are now being dropped into an emergency shell."
  - "ERROR: Failed to mount '/dev/mapper/root' on real root"
  - "mount: /new_root: wrong fs type, bad option, bad superblock"
tags: [boot, emergency-mode, limine, luks, btrfs, mkinitcpio]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6894"
    title: "Issue #6894: System does not boot after upgrade to quattro"
    kind: issue
    author: "arrowcircle"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/pull/6951"
    title: "PR #6951: Pin root= before the packages that can drop it"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7222"
    title: "Issue #7222: Quattro upgrade writes rd.luks.name while mkinitcpio uses encrypt hook, breaking encrypted root boot"
    kind: issue
    author: "gcarre"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/4192"
    title: "Issue #4192: Kernel 6.18.1-arch1-2 update breaks boot - missing vfat module prevents /boot mount"
    kind: issue
    author: "KhlifiIsmail"
    date: "2026-01-09"
  - url: "https://github.com/omacom/omarchy/issues/4781"
    title: "Issue #4781: Omarchy 3.4.0 breaks boot with LUKS encryption - emergency mode with locked root"
    kind: issue
    author: "folone"
    date: "2026-02-27"
  - url: "https://github.com/omacom/omarchy/issues/5026"
    title: "Issue #5026: Boot failure: depmod runs before DKMS, leaving modules.dep stale for mkinitcpio"
    kind: issue
    author: "amlucas0xff"
    date: "2026-03-15"
  - url: "https://github.com/omacom/omarchy/issues/4605"
    title: "Issue #4605: UKI Build Regression: Illegal Instruction (Exit Status 32) on x86-64-v2 Hardware"
    kind: issue
    author: "acraig78"
    date: "2026-02-14"
  - url: "https://github.com/omacom/omarchy/issues/8637"
    title: "Issue #8637: Hyprland reload-pause guard silently fails to prevent mid-update Lua reload"
    kind: issue
    author: "tecnarchico"
    date: "2026-08-27"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
    author: "omarchy"
    date: "2026-09-16"
credits:
  - name: "fowlie"
    url: "https://github.com/fowlie"
    for: "Found the truncated cmdline line in /boot/limine.conf and the snapshot-boot repair path"
  - name: "gcarre"
    url: "https://github.com/gcarre"
    for: "Traced the rd.luks.name against encrypt hook mismatch on encrypted roots"
  - name: "rubas"
    url: "https://github.com/rubas"
    for: "Reported that adding btrfs and dm_crypt to MODULES fixed the rebuild"
  - name: "amlucas0xff"
    url: "https://github.com/amlucas0xff"
    for: "Documented the depmod before DKMS hook ordering race"
faq:
  - q: "Is my data gone?"
    a: "No. Every case in the tracked issues was a boot image or kernel command line problem, not filesystem damage. Your Btrfs subvolumes are intact, which is why mounting them by hand from the emergency shell works."
  - q: "Does restoring a snapshot roll back my home directory?"
    a: "No. The Omarchy manual states a restore replaces the root filesystem only and leaves /home alone. Your ~/.config is also kept as-is, so config written by the newer version stays behind."
  - q: "Should I just reinstall?"
    a: "Not yet. A snapshot boot plus one limine-mkinitcpio run has fixed this for most reporters. Reinstalling is only worth it if the ESP itself was emptied."
related: [kernel-panic-after-update-limine, migration-failed-mid-update, omarchy-update-fails-or-hangs, luks-passphrase-not-accepted-at-boot, creating-a-snapshot-failed-snapper]
draft: false
---

Two different screens get called "emergency mode" and they need different repairs, so read the text before you touch anything.

If you see `ERROR: Failed to mount ... on real root` followed by a line about being dropped into an emergency shell, and the prompt is `[rootfs ~]#`, you never left the initramfs. The kernel command line or the LUKS unlock failed.

If you see a message about being in emergency mode with a normal login prompt, systemd booted fine and a mount in `/etc/fstab` failed. That is usually `/boot`.

A third thing also uses the word: Hyprland 0.56 shows an emergency binds banner when your Lua config fails to load, reported in issue #8637. That is a desktop banner, not a boot failure, and your machine is running fine.

## The fix

1. Power cycle the machine and stop at the Limine menu. If you turned on direct boot, pick Limine from your firmware boot menu first.
2. Choose a dated snapshot entry from before the update instead of the normal Omarchy entry. Omarchy takes a snapshot on every update, and snapshot entries point at a complete kernel and boot image, so they usually boot when the main entry does not. In issue #6894, @fowlie recovered this way after an upgrade was interrupted mid transaction.
3. The snapshot boots read-only. Make it writable:

```
sudo mount -o remount,rw /
```

4. Find out what actually broke:

```
systemctl --failed
sudo journalctl -xb -p err
sudo cat /proc/cmdline
```

5. If `/proc/cmdline` has no `root=`, or `/boot/limine.conf` has a `cmdline:` line with nothing but boot cosmetics on it, pin the parameters yourself. Add a line to `/etc/default/limine`:

```
KERNEL_CMDLINE[default]+=" root=UUID=<your-root-uuid> rw rootflags=subvol=@"
```

Use `findmnt -no UUID /` to get the UUID. On an encrypted root add the unlock parameter too, then rebuild:

```
sudo limine-mkinitcpio
```

6. On an encrypted root, check which unlock parameter you have. Omarchy 4 ships `HOOKS=(... block encrypt filesystems fsck btrfs-overlayfs)` in `/etc/mkinitcpio.conf.d/omarchy_hooks.conf`. That classic `encrypt` hook only reads `cryptdevice=`. If the Quattro upgrade carried a `rd.luks.name=` parameter over from an older systemd based setup, the initramfs ignores it and `/dev/mapper` stays empty. Replace it with the equivalent form and rebuild:

```
cryptdevice=UUID=<luks-uuid>:root root=/dev/mapper/root rw
```

This is issue #7222, still open as of 4.0.4.

7. If the failure is a failed `boot.mount` rather than root, your kernel modules or boot image are incomplete. Reinstall the kernel and rebuild everything:

```
sudo pacman -S linux
sudo mkinitcpio -P
sudo limine-update
```

8. Reboot into the normal entry. If you ran `limine-update` while running from a snapshot, the new entry may be rooted on the snapshot. Restore the snapshot you were running from with `omarchy-snapshot restore` before you trust it, or check `mount | grep " / "` shows `subvol=/@`.

On 3.x the same steps apply, except the Quattro cmdline problem in step 5 and 6 does not exist. The 3.x reports are about a failed `mkinitcpio` run leaving stale modules, so start at step 7.

## Verify it worked

Boot the normal Omarchy entry with no menu tricks. Then run:

```
mount | grep " / "
systemctl --failed
sudo cat /proc/cmdline
```

You want `subvol=/@` on root, an empty failed list, and a command line that names your root filesystem. Confirm the UKI carries it too:

```
sudo objcopy -O binary --only-section=.cmdline \
  /boot/EFI/Linux/omarchy_linux.efi /dev/stdout | tr -d '\0'
```

That is the same check `omarchy-upgrade-to-quattro` runs on itself in 4.0.4.

## Why it happens

Omarchy boots a unified kernel image through Limine, so the command line that matters is baked into the UKI on the EFI partition, not read at boot time.

For the Quattro upgrade, dhh reproduced the failure in PR #6951 and measured it. The `omarchy-defaults.conf` drop-in appends to `KERNEL_CMDLINE[default]`, which makes `limine-entry-tool` stop falling back to `/proc/cmdline`. On installs that predate the ISO pinning `root=`, a kernel bump in the same transaction can bake a UKI with no `root=` at all. His instrumented run measured roughly ten seconds where that state existed before the upgrade repaired it. Ten seconds is short, but anything that interrupts the upgrade there leaves the machine stranded. That PR is still open.

The other family is a boot image that was never rebuilt. In issue #5026, @amlucas0xff traced pacman hook ordering: `depmod` runs before DKMS builds its modules, so `mkinitcpio` cannot find them, fails, and skips the UKI rebuild. The old image stays on the ESP pointing at a kernel version whose modules directory no longer exists. Issue #4605 is the same shape from a different angle, with the UKI build crashing on an x86-64-v2 only CPU. Issue #4192 is the same again, with `vfat` missing so `/boot` could not mount.

Collaborator @ryanrhughes said in issue #4781 that the update does check whether `mkinitcpio` succeeded, and that the fix for essentially everyone has been to trigger a rebuild. That matches what the reports show.

## If that did not work

If no snapshot entry boots, or the Limine menu is gone entirely, use the Omarchy ISO as a live USB and chroot in. The one trap people hit is Btrfs. Mounting the top level gives you a directory of subvolumes and `arch-chroot` fails on it, as @wico-merkel described in issue #4192. Mount the root subvolume explicitly:

```
cryptsetup luksOpen /dev/nvmeXn1pY root      # encrypted roots only
mount -o subvol=@ /dev/mapper/root /mnt
mount /dev/nvmeXn1pZ /mnt/boot
arch-chroot /mnt
```

Then run steps 5 through 7 inside the chroot.

If `/etc/kernel/cmdline` and the Limine files are missing altogether, one reporter on issue #4781 had to reinstall `limine`, rebuild DKMS modules, recreate the command line file, and then rebuild the boot image, in that order. DKMS has to build before `mkinitcpio` runs or the rebuild fails again.

If you are on NVIDIA and the rebuild reports missing `nvidia` modules, install the matching DKMS package before rebuilding. Note that modules belong in a drop-in under `/etc/mkinitcpio.conf.d/`, not in `/etc/mkinitcpio.conf` itself, per @ryanrhughes in issue #4781.

Evidence for the 4.x cmdline cases is thin in one respect: both #7222 and #6951 are open, no 4.0.x release notes list a fix for them, and the cluster holds only eleven issues with most of them from 3.x. Treat the 4.x guidance as a repair, not a permanent fix.

## Related

- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Kernel panic after update](/fix/kernel-panic-after-update-limine/)
- [Migration failed mid update](/fix/migration-failed-mid-update/)
- [Upgrading 3 to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Limine boot](/hardware/boot-limine/)
- Omarchy manual: [System snapshots](https://omarchy.org/manual/system-snapshots/)
