---
title: "Fingerprint enrollment fails: Enrollment failed. Please try again."
description: "Fingerprint enrollment failing on Omarchy 4 with NoSuchDevice or a generic retry message. How to tell a bad scan from a reader libfprint cannot drive."
answer: "Run `fprintd-list \"$USER\"` first. If it lists a device, the reader is drivable: run `sudo systemctl stop fprintd` to drop a stale claim, then re-run `omarchy setup security fingerprint` with a slow flat press. If it prints No devices available on 4.0.3 or later, libfprint has no driver for your reader and retrying can never work. On 4.0.0 to 4.0.2, update first: setup swaps in a newer libfprint-git."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: input
issueCount: 103
errorStrings:
  - "Enrollment failed. Please try again."
  - "Impossible to enroll: GDBus.Error:net.reactivated.Fprint.Error.NoSuchDevice: No devices available"
  - "No devices available"
  - "Verification failed. You may want to try enrolling again."
  - "net.reactivated.Fprint.Error.AlreadyInUse"
  - "Device disabled to prevent overheating"
tags: [fingerprint, fprintd, libfprint, pam, enrollment]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11841"
    title: "Issue #11841: Fingerprint setup gives no diagnosis when libfprint has no driver for the detected reader"
    kind: issue
    author: "busbyjon"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/10892"
    title: "Issue #10892: omarchy setup security fingerprint fails at enroll on readers libfprint can't drive (Validity VFS491, 138a:003d)"
    kind: issue
    author: "NianticBooks"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11721"
    title: "Issue #11721: Stock fingerprint setup fails with NoSuchDevice on Validity 06cb:009a (libfprint lists it as unsupported)"
    kind: issue
    author: "BeameX"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/7991"
    title: "Issue #7991: omarchy setup security fingerprint fails instantly on Goodix 27c6:530c/533c/538c readers, no open libfprint driver exists"
    kind: issue
    author: "anupanup2001"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/7006"
    title: "Issue #7006: setup security fingerprint fails on sensors requiring open-fprintd (ThinkPad 06cb:009a)"
    kind: issue
    author: "ItsNotPaths"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7483"
    title: "Issue #7483: ELAN 04f3:0c4b fingerprint reader never matches under stock libfprint (ThinkPad E14/E15 Gen 3/4)"
    kind: issue
    author: "jcperdomoybarra"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/7229"
    title: "Issue #7229: Fingerprint reader fails after suspend: fprintd reports \"Cannot run while suspended\""
    kind: issue
    author: "hojner"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/2046"
    title: "Issue #2046: Cannot Enroll Fingerprint, NoSuchDevice Error"
    kind: issue
    author: "landsman"
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/pull/10442"
    title: "PR #10442: Install libfprint-git for every fingerprint reader"
    kind: pr
    author: "powderluv"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/pull/8757"
    title: "PR #8757: Support fprintd-compatible backends other than libfprint in fingerprint setup"
    kind: pr
    author: "alhasapi"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/11842"
    title: "PR #11842: Give a clear diagnosis when libfprint has no driver for the detected fingerprint reader"
    kind: pr
    author: "busbyjon"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/pull/11047"
    title: "PR #11047: Name the cause when libfprint cannot drive the fingerprint reader"
    kind: pr
    author: "codeclawd"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/pull/7993"
    title: "PR #7993: Route Goodix 53xc fingerprint readers to Dell's proprietary TOD driver"
    kind: pr
    author: "anupanup2001"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/discussions/3980"
    title: "Discussion #3980: Fingerprint Support"
    kind: discussion
    author: "syntaxboybe"
    date: "2025-12-24"
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy manual: Hardware authentication"
    kind: manual
credits:
  - name: "powderluv"
    url: "https://github.com/powderluv"
    for: "Restored libfprint-git for every reader in 4.0.3, so a new sensor only needs a package pin bump"
  - name: "anupanup2001"
    url: "https://github.com/anupanup2001"
    for: "Showed the Goodix 53xc ids are absent from libfprint's driver table and mapped the Dell TOD route"
  - name: "BeameX"
    url: "https://github.com/BeameX"
    for: "Traced 06cb:009a to libfprint's known-unsupported hwdb list and documented the working replacement stack"
  - name: "NianticBooks"
    url: "https://github.com/NianticBooks"
    for: "Demonstrated that the hardware gate passes while fprintd enumerates zero devices"
  - name: "jcperdomoybarra"
    url: "https://github.com/jcperdomoybarra"
    for: "Found that ELAN 04f3:0c4b enrolls but scores zero on every verify under the generic driver"
  - name: "busbyjon"
    url: "https://github.com/busbyjon"
    for: "Proposed the fprintd-list gate so an undrivable reader is named instead of being sent to retry"
faq:
  - q: "Does retrying enrollment ever help?"
    a: "Only when fprintd already lists a device. If `fprintd-list` says No devices available, libfprint has no driver for your chip and every retry fails the same way in under a second."
  - q: "Did my fingerprint setup break when I upgraded to Omarchy 4?"
    a: "Possibly, but no cited report blames the package swap itself. 4.0.0 moved machines from libfprint-git to stock libfprint 1.94.100; 4.0.3 went back to a newer libfprint-git pin that adds readers the release lacks, such as Synaptics 06cb:010b. Re-run the setup to get it."
  - q: "Is it safe to leave a failed run half-configured?"
    a: "On 4.x yes. The setup writes the PAM stacks only after enroll and verify both pass, so a failed enrollment touches nothing in /etc/pam.d. On 3.8.4 the PAM edits came before enrollment, so check those files."
  - q: "My print enrolls but sudo still asks for a password. Broken?"
    a: "Check the lid. Omarchy inserts a clamshell gate before pam_fprintd, so with the lid shut it skips the reader and goes straight to the password prompt."
related: [lock-screen-wont-unlock, suspend-wont-resume-s2idle, login-loop-or-password-not-accepted-sddm]
draft: false
---

`Enrollment failed. Please try again.` is what `omarchy-setup-security-fingerprint` prints whenever `fprintd-enroll` exits non-zero. On Omarchy 4 that one message covers two completely different situations: a reader libfprint can drive that you scanned badly, and a reader libfprint has no driver for at all, where no amount of retrying can work. Find out which one you have before you touch anything else.

## The fix

Checked on 4.0.4. Notes for 3.x are called out where they differ.

**1. Ask fprintd, not the setup wizard, whether you have a usable reader.**

```bash
lsusb | grep -iE 'fingerprint|goodix|synaptic|validity|elan'
sudo systemctl start fprintd
fprintd-list "$USER"
```

If `fprintd-list` prints a device path, the hardware is drivable and your failure is fixable. Carry on with steps 2 to 4. If it prints `No devices available`, that is the same enumeration gap behind `Impossible to enroll: GDBus.Error:net.reactivated.Fprint.Error.NoSuchDevice: No devices available`. On 4.0.0 to 4.0.2 do step 2 first, because the newer libfprint-git that 4.0.3 setup installs carries readers stock libfprint lacks. If the list is still empty on 4.0.3 or later, skip to step 5.

**2. Get to 4.0.3 or later, then run setup again.**

```bash
omarchy version
omarchy update
omarchy setup security fingerprint
```

Releases 4.0.0, 4.0.1 and 4.0.2 install stock `libfprint` and remove `libfprint-git` if it is present. 4.0.3 reversed that through [PR #10442](https://github.com/omacom/omarchy/pull/10442) by powderluv: setup now installs `libfprint-git` for every reader in a single `--ask 4` pacman transaction. That package is pinned to an upstream commit newer than the Arch release, which is how it picks up readers such as the Synaptics `06cb:010b` that stock 1.94.100 lacks. Updating alone does not move you, because the repair migration only installs `libfprint-git` on a machine left with no libfprint at all. Re-running the setup is what swaps the package.

**3. Clear a stale device claim before you retry.**

An interrupted enroll or verify can leave fprintd holding the device, and later attempts fail with `AlreadyInUse`. `fprintd.service` is D-Bus activated, so stopping it is enough: the next attempt starts a clean daemon, and enrolled prints survive.

```bash
sudo systemctl stop fprintd
sudo fprintd-enroll "$USER"
```

Watch it in a second terminal with `journalctl -fu fprintd` while you scan.

**4. Match your technique to the sensor and slow down.**

The wizard tells you to keep moving your finger, which is advice for swipe sensors. The Goodix 53xc family and the ELAN `04f3:0c4b` are press sensors: put the finger down flat and hold it for about a second per stage. Goodix 53xc firmware also disables itself after repeated touches, logging `Device disabled to prevent overheating`, and fast retry loops extend the lockout. Let it cool down or reboot rather than hammering it. On the ELAN `04f3:0c4b` one reporter found the same lockout survived an fprintd restart and a package reinstall and only cleared after a USB device reset.

**5. If fprintd sees no device, the stock stack is the wrong stack.**

These are the readers with confirmed reports. All of them pass Omarchy's hardware check and then fail at enroll.

| Reader | Reported on | State under stock Omarchy 4 | Route that worked |
| --- | --- | --- | --- |
| Goodix `27c6:530c` / `533c` / `538c` | Dell Inspiron 5585, XPS 13 9310 | ids absent from the open driver table | `libfprint-tod` plus Dell's closed goodix-tod plugin |
| Synaptics/Validity `06cb:009a`, `138a:0097` | ThinkPad T480, T480s, T570 (reporters say T490 and X1 Carbon 6th share the chip) | listed under known unsupported devices in libfprint's hwdb | `open-fprintd` plus `python-validity` plus `fprintd-clients-git` |
| ELAN `04f3:0c4b` | ThinkPad E15 Gen 3, IdeaPad 3 14ALC6, ThinkBook 14 G8 | enrolls then never verifies, or dies at enroll with a protocol error | `libfprint-tod` plus Lenovo's ELAN plugin plus `openssl-1.1` |
| Validity VFS491 `138a:003d` | HP EliteBook 8470w | no driver in libfprint | none reported |
| Goodix `27c6:55b4` | ThinkPad L13 Yoga (20R5000SUK) | no driver in libfprint | none reported |

Every one of those routes is unofficial, pulls AUR packages, and in two cases a vendor binary. Treat them as your own maintenance burden. Once you are on a replacement stack, do not re-run the stock setup. On the python-validity stack it tries to install `fprintd`, which conflicts with `fprintd-clients-git`, and the whole command aborts. On a TOD stack the 4.0.3 and later `--ask 4` install accepts the conflict and swaps `libfprint-tod` out for `libfprint-git`. [PR #8757](https://github.com/omacom/omarchy/pull/8757) would make setup detect an existing fprintd-compatible backend and leave it alone, but it was still open at 4.0.4.

## Verify it worked

```bash
fprintd-list "$USER"
fprintd-verify
ls -l /etc/pam.d/omarchy-lock-fingerprint
grep -n 'pam_fprintd\|omarchy-hw-laptop-closed' /etc/pam.d/sudo /etc/pam.d/polkit-1
```

You want a listed finger, a `verify-match` result, the lock PAM file present, and both a `pam_fprintd.so` line and a `pam_exec.so` clamshell gate line above it in `sudo` and `polkit-1`. Then open a fresh terminal, run any `sudo` command with the lid open, and lock with `Super + Ctrl + L` to confirm the reader is offered on the lock screen.

## Why it happens

Detection and drivability are two different questions, and 4.x only asks the first one up front. `omarchy-hw-fingerprint` reads sysfs directly so it can run before fprintd is installed. It matches a product string containing fingerprint, biometric, an Elan match-on-chip name or an FPC prefix, or a USB vendor from a short list with no kernel driver bound to any interface. That establishes a reader is physically there. It says nothing about whether libfprint has code for the chip.

v3.8.4 asked the second question instead: its `check_fingerprint_hardware` ran `fprintd-list` and bailed out with `No fingerprint sensor detected.` when the list was empty. 4.0.0 replaced that with the sysfs probe, which is what lets the menu hide the entry on machines with no reader, but it also means the enroll step is now the first moment anything consults fprintd. So an unsupported reader gets all the way to `fprintd-enroll` and comes back with retry advice that cannot work. The setup script's own comments acknowledge this class of failure for Elan sensors outside the driver table. [PR #11842](https://github.com/omacom/omarchy/pull/11842) proposes an `fprintd-list` check between package install and enrollment, and [PR #11047](https://github.com/omacom/omarchy/pull/11047) names the three Validity ids on the failure path instead of saying try again; neither had merged as of 4.0.4.

The libfprint package choice has also moved twice. 3.8.4 installed `libfprint-git`. A migration shipped with 4.0.0 swapped everyone back to stock `libfprint`, on the grounds that release 1.94.100 had absorbed the FocalTech driver the snapshot was carrying. 4.0.3 went back to `libfprint-git`, now pinned past 1.94.100, and rewrote that migration to only repair machines the two-step swap had left with fprintd and no library. None of the cited reports trace a failure to the 4.0.0 swap itself; what the newer pin buys you is readers the release lacks.

One thing 4.x does better: PAM configuration comes last, only after enroll and verify both succeed. On 3.8.4 the PAM edits ran before enrollment, after an `fprintd-list` check, so a failed enrollment on a drivable reader could leave `pam_fprintd.so` in your sudo and polkit stacks with no print behind it.

## If that did not work

If enrollment completes and verification fails every single time with no partial match, you are probably on the ELAN case rather than a scanning problem. Check `journalctl -u fprintd` for the driver name it loaded.

If the fingerprint works for `sudo` but never on the lock screen, that is not an enrollment problem at all. fprintd gets activated inside logind's sleep delay window, misses its own sleep inhibitor, and comes back from resume refusing everything, while the lock screen retries it roughly four times a second. See [suspend and resume](/fix/suspend-wont-resume-s2idle/) and [the lock screen page](/fix/lock-screen-wont-unlock/).

If _Setup > Security > Fingerprint_ is missing from the menu entirely, the detector did not match your reader, so nothing downstream ever runs. Run `omarchy-hw-fingerprint; echo $?` and compare your device against `lsusb`.

To get back to a clean state, use _Remove > Security > Fingerprint_, which strips the PAM lines, the clamshell gates and the lock PAM file, then drops the packages.

If your reader is not in the table above, open an issue with the exact `lsusb` id, the `fprintd-list` output and your `omarchy version`, or send it to [hardware submissions](/hardware/submit/) so the model pages can carry it.

## Related

- [Fingerprint reader hardware notes](/hardware/fingerprint/)
- [ThinkPad T480 and classics](/hardware/lenovo-thinkpad-t480/)
- [Lock screen will not unlock](/fix/lock-screen-wont-unlock/)
- [Omarchy manual: hardware authentication](https://omarchy.org/manual/hardware-authentication/)
