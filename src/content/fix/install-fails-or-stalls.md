---
title: "Omarchy installer fails or stalls partway through"
description: "Read /var/log/omarchy-install.log on the live ISO and find the first error. Offline mirror, ESP mount and psmouse failures each have a different fix."
answer: "Find the first error, not the last. On the live ISO the installer logs to /var/log/omarchy-install.log. A missing package from /var/cache/omarchy/mirror/offline means reboot the stick and retry. \"mounting the ESP failed (exit 32)\" on a free-space install means pre-create a FAT32 EFI partition on the target disk. A psmouse modprobe failure was fixed in 4.0.1, so use a newer ISO."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: install
errorStrings:
  - "ERROR: Failed to install packages to new root"
  - "error: failed retrieving file ... from disk : Could not open file /var/cache/omarchy/mirror/offline/"
  - "mounting the ESP failed (exit 32)"
  - "Can't find a SQUASHFS superblock on nvme0n1p3."
  - "modprobe: FATAL: Module psmouse not found in directory"
  - "Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)"
  - "grub_memalign:552:out of memory"
tags: [install, iso, offline-mirror, esp, dual-boot, pacstrap]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6985"
    title: "Issue #6985: Quattro (4.0) install fails: fix-synaptic-touchpad.sh psmouse module mismatch + vulkan.sh offline mirror missing files"
    kind: issue
    author: "ahmedsrea"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/7236"
    title: "PR #7236: Stop a psmouse quirk from failing every install"
    kind: pr
    author: "omarchybot"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Release v4.0.1"
    kind: release
    author: "dhh"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7704"
    title: "Issue #7704: Omarchy 4.0.0 install fails because gst-plugin-gtk is missing from offline mirror"
    kind: issue
    author: "jack-builds"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/7263"
    title: "Issue #7263: Dual-boot install fails when the free space is on a different disk than Windows itself"
    kind: issue
    author: "igor-gorohovsky"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7515"
    title: "Issue #7515: Free space install (alongside exsisting data) Doesn't work alongside non-OS partitions"
    kind: issue
    author: "Matredit"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/7867"
    title: "Issue #7867: Dual-boot install creates a redundant ESP instead of reusing the existing Windows one, and omarchy-refresh-limine permanently drops the Windows entry on every run"
    kind: issue
    author: "ThePeteJames"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/9450"
    title: "Issue #9450: Omarchy install ends with cryptic VFS: Cannot open root device or unknown-block(0,0) or grub_memalign:552:out of memory"
    kind: issue
    author: "jsuchal"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/8196"
    title: "Issue #8196: Full-disk install: password set under a non-US keyboard layout can be untypeable at the LUKS boot prompt"
    kind: issue
    author: "notwitcheer"
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
    author: "dhh"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy manual: Dual Boot Install"
    kind: manual
    author: "dhh"
    date: "2026-09-15"
credits:
  - name: "ahmedsrea"
    url: "https://github.com/ahmedsrea"
    for: "Traced the psmouse modprobe failure to the chroot kernel mismatch"
  - name: "Damian626"
    url: "https://github.com/Damian626"
    for: "Found the vfat mount workaround for the ESP failure"
  - name: "Matredit"
    url: "https://github.com/Matredit"
    for: "Found that a dummy FAT32 EFI partition on the target disk gets free-space installs through"
  - name: "HalbonLabs"
    url: "https://github.com/HalbonLabs"
    for: "Confirmed the pre-created ESP workaround on 4.0.3 and gave the diskpart steps"
  - name: "jsuchal"
    url: "https://github.com/jsuchal"
    for: "Identified Intel PTT as the hidden TPM setting behind boot panics"
  - name: "jack-builds"
    url: "https://github.com/jack-builds"
    for: "Reported the offline mirror package that goes missing mid-install"
faq:
  - q: "Where is the installer log?"
    a: "On the live ISO it is /var/log/omarchy-install.log. After a finished install the same path on the installed system holds the run from omarchy-apply-system."
  - q: "Should I re-download the ISO when a package fails?"
    a: "Only if the same package fails again after a full reboot of the USB stick. A different package each time points at flaky reads, not a bad download."
  - q: "Can I install an older ISO and upgrade instead?"
    a: "Yes. One reporter on issue #6985 installed 3.6 and ran the Quattro upgrade afterwards, and a maintainer comment there confirmed that route avoids the ISO-side psmouse bug."
related: [secure-boot-violation-or-wont-boot-uefi, failed-to-retrieve-some-files-pacman, luks-passphrase-not-accepted-at-boot, kernel-panic-after-update-limine]
draft: false
---

The Omarchy installer is a chain of shell scripts, and a failure anywhere in the chain stops the whole run. The screen you are looking at almost never names the real cause. Find the first error in the log, then match it below.

## The fix

1. Get a shell on the live ISO. Press `Ctrl + C` at the failure screen, or pick the drop to shell option from the failure menu. The target stays mounted at `/mnt`.

2. Read the log from the top. The installer writes to `/var/log/omarchy-install.log` on the live session, and `run_logged` in `install/helpers/logging.sh` stamps every script it starts and every one that fails.

   ```
   grep -n "Failed:" /var/log/omarchy-install.log | head
   less /var/log/omarchy-install.log
   ```

   The first failure names the cause. Everything after it is wreckage.

3. **Missing package from the offline mirror.** If the first error looks like `error: failed retrieving file '<package>' from disk : Could not open file /var/cache/omarchy/mirror/offline/<package>`, or the run ends with `ERROR: Failed to install packages to new root`, reboot the USB stick and try again before anything else. During install the offline mirror is both pacman's repository and its cache, so a package that fails its checksum is deleted out of the mirror under `--noconfirm`. The stick itself is untouched, because the live system writes to a RAM overlay, so a reboot brings the file back. Without rebooting you can copy the file back from the read only image, which is the fix a maintainer comment gives on issue #7704:

   ```
   sudo cp /run/archiso/airootfs/var/cache/omarchy/mirror/offline/<package>*.pkg.tar.zst \
           /var/cache/omarchy/mirror/offline/
   ```

   If the same package fails again after a clean reboot, your copy of the ISO or the write to the stick is bad. Check the download against the SHA256 published in the release notes (for 4.0.4 that is `ddeded2758c48318d201dfdac905ecb28f570441883f0c052ea3cd5d05acf92d`) and check the medium itself before installing:

   ```
   cd /run/archiso/bootmnt/arch/x86_64 && sha512sum -c airootfs.sha512
   ```

4. **Free space install dies at the EFI partition.** The signature is `mounting the ESP failed (exit 32)` preceded by `Can't find a SQUASHFS superblock on <partition>`, where the partition is the one the installer just created. Every report on issue #7515 is a target disk with data partitions and no EFI partition. The workaround that got Matredit and two other commenters through is to give the target disk an EFI partition before you start. From Windows, `diskpart` on that disk, then `create partition efi size=1024` and `format quick fs=fat32` (HalbonLabs did this on 4.0.3); from Linux, a 256 MB EFI System partition in `cfdisk` formatted with `mkfs.fat -F32` did the same job. Re-run the installer and pick the free space as before. Damian626's alternative on issue #7263 patches the installer's configurator script in the live session, adding `udevadm settle` and `sleep 2` after the ESP is created and forcing `mount -t vfat` on both the new ESP mount and the `detect_windows_esp()` probe, then `umount -R /mnt 2>/dev/null` and `./.automated_script.sh` to start over. Three other commenters confirmed it worked for them.

5. **Install halts in "Configuring system" with a psmouse error.** `modprobe: FATAL: Module psmouse not found in directory` followed by `[Failed]: /usr/share/omarchy/install/hardware/fix-synaptic-touchpad.sh (exit code: 1)` was a 4.0.0 ISO bug. PR #7236 fixed it and shipped in v4.0.1 on 2026-08-25, so install from a 4.0.1 or newer ISO. On stuck 4.0.0 media, append `|| true` to the `modprobe` line in `/usr/share/omarchy/install/hardware/fix-synaptic-touchpad.sh` and restart the installer.

6. **The ISO never gets as far as the installer.** `Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)` or `grub_memalign:552:out of memory` before the installer appears usually mean a firmware setting. The manual's [Getting Started](https://omarchy.org/manual/getting-started/) page says to turn off Secure Boot and/or TPM. On a Lenovo Yoga 7 ProX the setting was named `Intel Platform Trust Technology (Intel PTT)`, not TPM, which is why issue #9450 was filed. An HP EliteBook 1040 G8 in the same thread showed both messages with Secure Boot already off; a later comment suggested dropping the firmware's Video Memory Size to its minimum, which nobody had confirmed when this page was checked. See [secure boot violation or will not boot UEFI](/fix/secure-boot-violation-or-wont-boot-uefi/).

## Verify it worked

After the installer reports success and the machine reboots into Omarchy:

```
grep -c "Failed:" /var/log/omarchy-install.log
omarchy version
findmnt /
```

The grep should print `0`. `omarchy version` should print the version of the ISO you installed from. If you dual boot, reboot once more and confirm both entries appear in Limine before you trust the machine.

## Why it happens

Three separate designs combine badly.

The ISO installs from a mirror baked into the image at `/var/cache/omarchy/mirror/offline/`, bind mounted into the target. The target's `pacman.conf` during install lists that directory as its only repository, so there is nothing to fall back to when a file is unreadable. The online repositories are restored later by `install/post-install/pacman.sh`, which never runs if the install stopped earlier.

Every install script runs through `run_logged` under `bash -eE`, and `bin/omarchy-apply-hardware` runs under `set -euo pipefail`. An optional hardware tweak that fails takes the entire install down with it. That is exactly what the psmouse quirk did.

The free space path creates its own new ESP rather than reusing an existing one, which issue #7867 documents with a full partition table. Every failing report on issue #7515 is a target disk with no ESP at all, and adding an empty one is enough to get through, so the installer appears to depend on one being present even though it does not use it.

Evidence on the ESP failures is good but the root cause is not settled. Issues #7263, #7515 and #7867 were all still open when this page was checked against 4.0.4.

## If that did not work

If you patched scripts and resumed by hand, the offline mirror bind mount is gone and every later package will fail. Re-mount it before you chroot:

```
mount --bind /var/cache/omarchy/mirror/offline /mnt/var/cache/omarchy/mirror/offline
```

If the install completes but pacman 404s afterwards, that is a different problem: see [failed to retrieve some files](/fix/failed-to-retrieve-some-files-pacman/). If the machine installs but the LUKS prompt rejects your password, and you chose a non-US keyboard layout, see [LUKS passphrase not accepted at boot](/fix/luks-passphrase-not-accepted-at-boot/); issue #8196 describes digits enrolled under AZERTY becoming untypeable at the prompt. If Windows vanishes from the boot menu, [run `limine-scan`](https://omarchy.org/manual/dual-boot-install/) as the manual describes.

A blunt option one reporter on issue #6985 took: install 3.6, then run the [3 to 4 Quattro upgrade](/upgrade/3-to-4-quattro/). A maintainer comment there confirmed that route avoids the psmouse failure, since the ISO is where that script runs.

## Related

- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Should you dual boot](/switch/should-you-dual-boot/)
- [Unattended install with cidata](/run/unattended-install-cidata/)
- [Verify the ISO signature](/verify/)
- [Limine and boot hardware notes](/hardware/boot-limine/)
