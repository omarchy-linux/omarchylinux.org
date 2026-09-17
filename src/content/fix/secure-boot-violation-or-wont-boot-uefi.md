---
title: "Secure Boot Violation, or the Omarchy USB will not boot"
description: "Secure Boot Violation and UEFI boot failures on Omarchy: turn Secure Boot off, pick the UEFI USB entry, fix Ventoy, and re-sign Limine after an update."
answer: "Turn Secure Boot off in firmware before you boot the Omarchy USB. The installer refuses to run with it enabled, and on some machines the live ISO also panics. In the boot menu pick the entry labelled UEFI, not the plain legacy one. If Secure Boot Violation appears after an update on an install where you enrolled your own keys, disable Secure Boot to get back in, then re-sign the Limine binary with sbctl."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: install
errorStrings:
  - "Secure Boot Violation"
  - "Not booted with EFI or running in a container"
  - "Omarchy install requires: Secure Boot disabled"
  - "PANIC: efi: LoadImage failure (0x800000000000000f)"
  - "/arch/boot/x86_64/vmlinuz-linux not found"
tags: [secure-boot, uefi, install, iso, limine, sbctl]
sources:
  - url: "https://github.com/omacom/omarchy/issues/5387"
    title: "Issue #5387: Installer fails with \"Not booted with EFI\" despite UEFI setup"
    kind: issue
    author: "Satbir6"
    date: "2026-04-22"
  - url: "https://github.com/omacom/omarchy/issues/5385"
    title: "Issue #5385: Installer incorrectly detects non-UEFI boot when using Ventoy (UEFI confirmed)"
    kind: issue
    author: "Satbir6"
    date: "2026-04-21"
  - url: "https://github.com/omacom/omarchy/issues/1814"
    title: "Issue #1814: Problem with installation Omarchy 3.0 ISO using Ventoy as boot media"
    kind: issue
    author: "Rakura-cloud"
    date: "2025-09-19"
  - url: "https://github.com/omacom/omarchy/issues/2100"
    title: "Issue #2100: ISO not loading through USB stick"
    kind: issue
    author: "ashd90"
    date: "2025-09-30"
  - url: "https://github.com/omacom/omarchy/issues/2164"
    title: "Issue #2164: ISO: Incorrect path in grub configuration"
    kind: issue
    author: "LazyStability"
    date: "2025-10-02"
  - url: "https://github.com/omacom/omarchy/issues/10945"
    title: "Issue #10945: Limine-only update leaves limine_x64.efi unsigned, causes Secure Boot Violation lockout"
    kind: issue
    author: "LoboHacks"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/12045"
    title: "Issue #12045: Secure Boot UKI chainload panics on MSI firmware (LoadImage failure); ENABLE_UKI=no workaround"
    kind: issue
    author: "fenfenau"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/10647"
    title: "Issue #10647: LiveUSB Claims Secure Boot Enabled But It Isn't"
    kind: issue
    author: "moore-bryan"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/10734"
    title: "Issue #10734: ISO does not boot on fast USB drives with SSD controllers"
    kind: issue
    author: "jacobjennings"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/discussions/2296"
    title: "Discussion #2296: Omarchy Dual-Boot Secure Boot Setup (Custom Keys Guide)"
    kind: discussion
    author: "borgox"
    date: "2025-10-07"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.0.2"
    title: "Release v3.0.2: Fix hanging issue for normal boot when using Ventoy"
    kind: release
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.1.0"
    title: "Release v3.1.0: Add guard against installing on systems with secure boot enabled"
    kind: release
    date: "2025-10-19"
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
credits:
  - name: "Satbir6"
    url: "https://github.com/Satbir6"
    for: "Worked out that the EFI error came from picking the legacy USB entry, not from a Ventoy detection bug"
  - name: "dsimonow"
    url: "https://github.com/dsimonow"
    for: "Found that Ventoy's grub2 mode boots the Omarchy ISO when normal mode hangs"
  - name: "LazyStability"
    url: "https://github.com/LazyStability"
    for: "Traced the Ventoy boot failure to wrong kernel paths in the ISO's loopback.cfg"
  - name: "LoboHacks"
    url: "https://github.com/LoboHacks"
    for: "Diagnosed the unsigned limine_x64.efi lockout down to the pacman hook ordering and a case-sensitive glob"
  - name: "fenfenau"
    url: "https://github.com/fenfenau"
    for: "Found the ENABLE_UKI=no workaround for LoadImage panics on MSI firmware"
  - name: "killeik"
    url: "https://github.com/killeik"
    for: "Added the Secure Boot guard to the installer in v3.1.0"
faq:
  - q: "Does Omarchy support Secure Boot at all?"
    a: "Not out of the box. The manual tells you to turn Secure Boot off before installing, and the installer refuses to proceed while it is on. You can enrol your own keys with sbctl afterwards, which people do to keep a Windows dual boot happy, but nothing in Omarchy signs or verifies for you and issue #10945 shows an ordinary update can leave the bootloader unsigned."
  - q: "Is Ventoy safe to use for the Omarchy ISO?"
    a: "It works now, and a maintainer said in issue #2164 that they use Ventoy to test. Normal mode hung on 3.0 and 3.0.1 and was fixed in v3.0.2. If it still hangs for you, pick grub2 mode in the Ventoy menu, which is what worked for the people in issues #1814 and #2100."
  - q: "Do I need to turn TPM off too?"
    a: "The manual's getting started chapter says to turn off Secure Boot and TPM in the BIOS. Only Secure Boot is actually checked by the installer, but disabling both removes a class of firmware problems that have shown up repeatedly in boot reports."
related: [install-fails-or-stalls, kernel-panic-after-update-limine, you-are-in-emergency-mode-after-update, luks-passphrase-not-accepted-at-boot, stuck-at-tty-or-cannot-switch-tty]
draft: false
---

Three different problems share this page, because they look alike from the outside. Your firmware prints **Secure Boot Violation** and stops. Or the USB stick never reaches the installer. Or the installer starts and then refuses with `Not booted with EFI or running in a container`. Checked against v4.0.4, with the 3.x history noted where it matters.

## The fix

1. **Turn Secure Boot off in firmware first.** Reboot into your firmware setup (usually F2, F10, Del or Esc at power on), find Security or Boot, set Secure Boot to Disabled, and save. On many Lenovo and MSI boards you must also switch OS Type to "Other OS" rather than "Windows UEFI mode". The Omarchy manual's [getting started chapter](https://omarchy.org/manual/getting-started/) tells you to disable Secure Boot and TPM before you install.

2. **On an Intel Mac, disable Apple's Secure Boot instead.** Hold Command-R at power on, then Utilities > Startup Security Utility, choose "No Security", and allow booting from external media. Those exact steps are in the manual's [Mac support chapter](https://omarchy.org/manual/mac-support/).

3. **Pick the UEFI boot entry, not the legacy one.** Most firmware boot menus list the same stick twice, as `USB Name` and `UEFI: USB Name`. Select the `UEFI:` entry. This is the single most common cause of the EFI error. In issue #5387 the reporter first blamed the installer, then confirmed that `/sys/firmware/efi` was missing in the failing case, meaning the machine really had booted in legacy or CSM mode. Turn CSM off in firmware so the legacy entry disappears entirely.

4. **Check it from the live environment before starting the install.** Open a terminal on the ISO and run:

   ```bash
   ls /sys/firmware/efi
   ```

   A populated directory means you are in UEFI mode. `No such file or directory` means you booted legacy and the installer is right to stop.

5. **If the stick was written with Rufus, rewrite it.** Rufus defaults to an NTFS target that uses its UEFI:NTFS shim. Issue #5387 lists this as a cause of the failure. Use balenaEtcher on Mac or Windows, or caligula on Linux, both of which the manual recommends, and let them write the image unmodified.

6. **If you use Ventoy and it hangs on the Omarchy logo, choose grub2 mode.** In the Ventoy boot menu press the key for boot mode and pick grub2. This was the confirmed workaround in issues #1814 and #2100. Normal mode was fixed in [v3.0.2](https://github.com/omacom/omarchy/releases/tag/v3.0.2), which lists "Fix hanging issue for normal boot when using Ventoy".

7. **If Secure Boot Violation appears after an update on a machine where you enrolled your own keys**, disable Secure Boot in firmware to get back in, then boot Omarchy and repair the signature:

   ```bash
   sudo sbctl verify
   sudo sbctl sign -s /boot/EFI/limine/limine_x64.efi
   sudo limine-enroll-config
   ```

   Re-enable Secure Boot afterwards. Issue #10945 documents this on 4.0.x, and a second reporter there hit it on a 4.0.2 to 4.0.3 update.

## Verify it worked

Boot the stick and confirm the installer gets past its checks. On an installed system, check both halves:

```bash
bootctl status | grep -i "secure boot"
sudo sbctl verify
```

`Secure Boot: disabled` is the supported state. If you run with it enabled and your own keys, every file listed by `sbctl verify` must be signed, including `limine_x64.efi`.

## Why it happens

Omarchy refuses to install while Secure Boot is on. That guard was added in [v3.1.0](https://github.com/omacom/omarchy/releases/tag/v3.1.0) by killeik. In the 3.x source the check is a plain grep in `install/preflight/guard.sh`:

```bash
if bootctl status 2>/dev/null | grep -q 'Secure Boot: enabled'; then
  abort "Secure Boot disabled"
fi
```

In 3.x that abort still offered to proceed anyway. The 4.x ISO installer keeps the same check but the preflight script no longer lives in the omarchy repo, so you cannot read it from a source tag. One person reports a false positive from it in issue #10647, where the live USB claimed Secure Boot was on when it was not. That issue is open, has no comments and no logs, so treat it as unconfirmed.

The EFI error is almost never a detection bug. Both #5385 and #5387 came from the same reporter on the same Lenovo machine, and the second one shows the machine was genuinely booting legacy. Neither issue got a maintainer reply, and both were closed the same day.

The Ventoy hang was real and separate. Ventoy loop-mounts the ISO and reads `/boot/grub/loopback.cfg`, and in the 3.0.2 era that file pointed at `/arch/boot/x86_64/vmlinuz-linux` while the ISO actually shipped `vmlinuz-linux-t2`, which is what LazyStability found in issue #2164. Grub2 mode sidesteps the broken file.

The post-install violation is a signing gap. Omarchy's installer drops a pacman hook at `/etc/pacman.d/hooks/99-omarchy-limine.hook` that copies the stock `BOOTX64.EFI` over the just-signed `limine_x64.efi`, and sbctl's safety-net hook does not catch it because its target globs are lowercase while the shipped file is uppercase. That is LoboHacks's analysis in #10945. It is open, so expect it to bite again.

## If that did not work

- **Limine panics with `PANIC: efi: LoadImage failure` once Secure Boot is back on.** Omarchy forces unified kernel images through `/etc/limine-entry-tool.d/omarchy-uki.conf`, which contains only `ENABLE_UKI=yes` in v4.0.4. Some firmware, notably MSI 600-series and newer, cannot `LoadImage()` a non-factory-signed binary. Issue #12045 reports setting that value to `no` and rerunning `limine-mkinitcpio-install` fixes it. Snapshots taken before the change still point at the old UKI.
- **The stick boots on other machines but not this one.** Fast USB drives with SSD controllers report as non-removable, and issue #10734 says those do not boot the ISO over UEFI. Try a plain USB 2.0 or 3.0 flash drive.
- **Firmware refuses to add a boot entry.** If the installer fails around `efibootmgr` with "No space left on device", your NVRAM variable store is full. Clear stale entries in firmware setup first.
- **You want Secure Boot for a Windows dual boot.** Discussion #2296 is the community custom-keys guide people follow. It does not cover the UKI panic above, so read #12045 alongside it.

## Related

Boot problems that follow an update rather than an install belong on [kernel panic after update](/fix/kernel-panic-after-update-limine/) and [emergency mode after update](/fix/you-are-in-emergency-mode-after-update/). If the installer starts and then dies for another reason, see [install fails or stalls](/fix/install-fails-or-stalls/). For general Limine and firmware notes, see [boot and Limine](/hardware/boot-limine/), and for the dual boot decision itself, [should you dual boot](/switch/should-you-dual-boot/).
