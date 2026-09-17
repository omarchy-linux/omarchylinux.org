---
title: "Secure Boot Violation, or the Omarchy USB will not boot"
description: "Secure Boot Violation and UEFI boot failures on Omarchy: turn Secure Boot off, pick the UEFI USB entry, fix Ventoy, and re-sign Limine after an update."
answer: "Turn Secure Boot off in firmware before you boot the Omarchy USB. The manual requires it and the installer refuses to run with it enabled. In the boot menu pick the entry labelled UEFI, not the plain legacy one. If Secure Boot Violation appears after an update on an install where you enrolled your own keys, disable Secure Boot to get back in, then re-sign the Limine binary with sbctl and re-enrol its config."
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
  - name: "dot3x3q"
    url: "https://github.com/dot3x3q"
    for: "Reproduced the lockout on a 4.0.2 to 4.0.3 update and worked out that limine-enroll-config is the complete repair"
  - name: "killeik"
    url: "https://github.com/killeik"
    for: "Added the Secure Boot guard to the installer in v3.1.0"
faq:
  - q: "Does Omarchy support Secure Boot at all?"
    a: "Not out of the box. The manual tells you to turn Secure Boot off before installing, and the installer refuses to proceed while it is on. You can enrol your own keys with sbctl afterwards, which people do to keep a Windows dual boot happy, but Omarchy does not set Secure Boot up for you, and issue #10945 shows an ordinary update can leave the bootloader unsigned."
  - q: "Is Ventoy safe to use for the Omarchy ISO?"
    a: "A maintainer said in issue #2164 that they use Ventoy to test and had no trouble with 3.0.2. Normal mode hung on 3.0.1 and was fixed in v3.0.2. If it still hangs for you, pick grub2 mode in the Ventoy menu, which is what worked for the people in issue #1814. It did not help the reporter in #2100, who later said the issue was resolved without saying how."
  - q: "Do I need to turn TPM off too?"
    a: "The manual's getting started chapter says to turn off Secure Boot and TPM in the BIOS. The 3.x installer guard only checked Secure Boot, and nothing on this page needs TPM off, but the manual's instruction is the supported route so follow it."
related: [install-fails-or-stalls, kernel-panic-after-update-limine, you-are-in-emergency-mode-after-update, luks-passphrase-not-accepted-at-boot, stuck-at-tty-or-cannot-switch-tty]
draft: false
---

Three different problems share this page, because they look alike from the outside. Your firmware prints **Secure Boot Violation** and stops. Or the USB stick never reaches the installer. Or the installer starts and then refuses with `Not booted with EFI or running in a container`. Checked against v4.0.4, with the 3.x history noted where it matters.

## The fix

1. **Turn Secure Boot off in firmware first.** Reboot into your firmware setup (usually F2, F12 or Delete at power on), find Security or Boot, set Secure Boot to Disabled, and save. On ASUS boards there is a separate OS Type setting; the second reporter in issue #10945 had to set it to "Other OS" before the machine would boot again. The Omarchy manual's [getting started chapter](https://omarchy.org/manual/getting-started/) tells you to disable Secure Boot and TPM before you install.

2. **On an Intel Mac, disable Apple's Secure Boot instead.** Hold Command-R at power on, then Utilities > Startup Security Utility, choose "No Security", and allow booting from external media. Those exact steps are in the manual's [Mac support chapter](https://omarchy.org/manual/mac-support/).

3. **Pick the UEFI boot entry, not the legacy one.** Many firmware boot menus list the same stick twice, as `USB Name` and `UEFI: USB Name`. Select the `UEFI:` entry. Picking the wrong one is exactly what produced the EFI error in issue #5387, where the reporter first blamed the installer, then confirmed that `/sys/firmware/efi` was missing in the failing case, meaning the machine really had booted in legacy or CSM mode. Turn CSM off in firmware so the legacy entry disappears entirely.

4. **Check it from the live environment before starting the install.** Open a terminal on the ISO and run:

   ```bash
   ls /sys/firmware/efi
   ```

   A populated directory means you are in UEFI mode. `No such file or directory` means you booted legacy and the installer is right to stop.

5. **If the stick was written with Rufus, rewrite it.** Rufus writes ISOs this large to NTFS and boots them through its UEFI:NTFS shim, and the reporter in issue #5387 lists that as a likely contributor. Use balenaEtcher on Mac or Windows, or caligula on Linux, both of which the manual recommends, and let them write the image unmodified.

6. **If you use Ventoy and it hangs on the Omarchy logo, choose grub2 mode.** When Ventoy asks how to boot the ISO, pick grub2 mode instead of normal mode. Two people confirmed that in issue #1814. It did not work for the reporter in #2100, who eventually got the ISO booting some other way and did not say how. Normal mode was fixed in [v3.0.2](https://github.com/omacom/omarchy/releases/tag/v3.0.2), which lists "Fix hanging issue for normal boot when using Ventoy".

7. **If Secure Boot Violation appears after an update on a machine where you enrolled your own keys**, disable Secure Boot in firmware to get back in, then boot Omarchy and repair the signature:

   ```bash
   sudo sbctl verify
   sudo sbctl sign -s /boot/EFI/limine/limine_x64.efi
   sudo limine-enroll-config
   ```

   The `sbctl sign` line is the reporter's own workaround in issue #10945. The `limine-enroll-config` line comes from the second reporter there, who found that on a 4.0.2 to 4.0.3 update the hook also wiped the enrolled config checksum, so a bare re-sign left Limine panicking on a config hash mismatch. Re-enable Secure Boot afterwards.

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

In 3.x that abort still offered to proceed anyway. The 4.x ISO still refuses with Secure Boot on, but the preflight code is not in the omarchy repo's 4.x source, so you cannot read it from a source tag. One person reports a false positive from it in issue #10647, where the live USB claimed Secure Boot was on when it was not. That issue is open, has no comments and no logs, so treat it as unconfirmed.

The EFI error is almost never a detection bug. Both #5385 and #5387 came from the same reporter on the same Lenovo machine, and the second one shows the machine was genuinely booting legacy. Neither issue got a maintainer reply, and both were closed the same day.

The Ventoy hang was real and separate. On the 3.0.1 ISO, Ventoy's normal mode sat on the Omarchy logo forever, and grub2 mode got past it. A different bug surfaced on the 3.0.2 ISO: its `/boot/grub/loopback.cfg` pointed at `/arch/boot/x86_64/vmlinuz-linux` while the ISO actually shipped `vmlinuz-linux-t2`, which is what LazyStability found in issue #2164 using Multios-USB. Tools that boot through loopback.cfg fail with `vmlinuz-linux not found` and drop back to a grub menu. The maintainer said he would copy the fix over; no release note names it, so if you see that error, write the ISO to a plain stick instead.

The post-install violation is a signing gap. Omarchy's installer drops a pacman hook at `/etc/pacman.d/hooks/99-omarchy-limine.hook` that copies the stock `BOOTX64.EFI` over the just-signed `limine_x64.efi`, and sbctl's safety-net hook does not catch it because its target globs are lowercase while the shipped file is uppercase. That is LoboHacks's analysis in #10945. The second reporter there saw the sbctl hook fire and still sign nothing, because the file had been signed without `-s` and was not in sbctl's database. The issue is open, so expect it to bite again.

## If that did not work

- **Limine panics with `PANIC: efi: LoadImage failure` once Secure Boot is back on.** Omarchy forces unified kernel images through `/etc/limine-entry-tool.d/omarchy-uki.conf`, which contains only `ENABLE_UKI=yes` in v4.0.4. The reporter in issue #12045, on an MSI X870E board, found the firmware refused to `LoadImage()` the signed UKI and ties that to the firmware family sbctl tracks as FQ0001, which covers MSI 600-series boards and newer. Setting the value to `no` and rerunning `echo linux | sudo /usr/share/libalpm/scripts/limine-mkinitcpio-install` switched the entry to Limine's native `linux` protocol and it booted. Snapshots taken before the change still point at the old UKI.
- **The stick boots on other machines but not this one.** One reporter in issue #10734 says fast USB drives with SSD controllers present as non-removable and will not boot the ISO over UEFI. Nobody has confirmed it. Try a plain flash drive before anything else.
- **You want Secure Boot for a Windows dual boot.** Discussion #2296 is the community custom-keys guide people follow. It does not cover the UKI panic above, so read #12045 alongside it.

## Related

Boot problems that follow an update rather than an install belong on [kernel panic after update](/fix/kernel-panic-after-update-limine/) and [emergency mode after update](/fix/you-are-in-emergency-mode-after-update/). If the installer starts and then dies for another reason, see [install fails or stalls](/fix/install-fails-or-stalls/). For general Limine and firmware notes, see [boot and Limine](/hardware/boot-limine/), and for the dual boot decision itself, [should you dual boot](/switch/should-you-dual-boot/).
