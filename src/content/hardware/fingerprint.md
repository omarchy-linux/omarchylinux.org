---
title: "Fingerprint readers on Omarchy"
description: "Fingerprint readers on Omarchy 4.0.4: what enrolls out of the box, the omarchy-hw-fingerprint detection gaps, fprintd wedging after suspend, and the fix order."
answer: "Fingerprint auth is opt in. Run Setup > Security > Fingerprint, or omarchy setup security fingerprint, and Omarchy installs libfprint-git and fprintd, enrolls a finger, and wires sudo, polkit and the lock screen. Goodix and FocalTech match-on-chip readers generally work. The common failures are detection false negatives, readers libfprint has no driver for, and fprintd wedging after suspend."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "fingerprint"
issueCount: 97
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [fingerprint, fprintd, libfprint, pam, lock-screen, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-fingerprint"
    title: "bin/omarchy-hw-fingerprint at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-setup-security-fingerprint"
    title: "bin/omarchy-setup-security-fingerprint at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-remove-security-fingerprint"
    title: "bin/omarchy-remove-security-fingerprint at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/first-run/setup-fingerprint.hook"
    title: "install/user/first-run/setup-fingerprint.hook at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1784818437.sh"
    title: "migrations/1784818437.sh at v4.0.4 (lid gate for sudo and polkit)"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1785090473.sh"
    title: "migrations/1785090473.sh at v4.0.4 (repair fingerprint left without a libfprint)"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/shell/plugins/lock/Service.qml"
    title: "shell/plugins/lock/Service.qml at v4.0.4"
    kind: commit
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
  - url: "https://github.com/omacom/omarchy/issues/11384"
    title: "Issue #11384: omarchy-hw-fingerprint false negative: FocalTech readers (2808:*) report as no sensor"
    kind: issue
    author: "alanwcurry-dev"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11426"
    title: "Issue #11426: omarchy-hw-fingerprint misses Microarray MAFP readers (3274:8012), fingerprint setup refuses to run"
    kind: issue
    author: "Rafale83"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11721"
    title: "Issue #11721: Stock fingerprint setup fails with NoSuchDevice on Validity 06cb:009a (libfprint lists it as unsupported)"
    kind: issue
    author: "BeameX"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/7006"
    title: "Issue #7006: setup security fingerprint fails on sensors requiring open-fprintd (ThinkPad 06cb:009a)"
    kind: issue
    author: "ItsNotPaths"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7483"
    title: "Issue #7483: ELAN 04f3:0c4b fingerprint reader never matches under stock libfprint (ThinkPad E14/E15 Gen 3/4), works with libfprint-tod instead"
    kind: issue
    author: "jcperdomoybarra"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/11899"
    title: "Issue #11899: omarchy setup security fingerprint silently evicts a working libfprint fork, then succeeds against the stale daemon"
    kind: issue
    author: "StuartRP"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11841"
    title: "Issue #11841: Fingerprint setup gives no diagnosis when libfprint has no driver for the detected reader"
    kind: issue
    author: "busbyjon"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/7229"
    title: "Issue #7229: Fingerprint reader fails after suspend: fprintd reports Cannot run while suspended"
    kind: issue
    author: "hojner"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/11412"
    title: "Issue #11412: Fingerprint unlock fails after every suspend (fprintd device stuck busy) and the shell retries every 250ms until unlock"
    kind: issue
    author: "callumau"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11889"
    title: "Issue #11889: Enrolled fingerprint permanently erased after suspend/resume (Goodix MOC 27c6:6594)"
    kind: issue
    author: "Frenagon"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12202"
    title: "Issue #12202: Lock screen fingerprint sensor only ever runs ONE pam session per lock"
    kind: issue
    author: "slr01"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/7645"
    title: "Issue #7645: Quickshell lock crashes in PamSubprocess during overlapping fingerprint retries"
    kind: issue
    author: "prestoncabe"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/7176"
    title: "Issue #7176: Lock screen retries fingerprint auth every 250ms with no backoff, keeping throttled readers permanently disabled"
    kind: issue
    author: "AdamWorley"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/856"
    title: "Issue #856: Fingerprint fallback to password auth failing"
    kind: issue
    author: "shawnyeager"
    date: "2025-08-16"
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy manual: Hardware authentication"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3"
    kind: release
    date: "2026-09-08"
credits:
  - name: "mnemonicspace"
    url: "https://github.com/mnemonicspace"
    for: "Tracing the post-suspend fprintd wedge to a sleep-delay inhibitor logind refuses when fprintd is activated inside the sleep window"
  - name: "martlets"
    url: "https://github.com/martlets"
    for: "Measuring the retry storm at 94 PAM sessions in 27 seconds and publishing a system-sleep hook workaround"
  - name: "alanwcurry-dev"
    url: "https://github.com/alanwcurry-dev"
    for: "Showing that FocalTech vendor 2808 readers fail the Omarchy detector while libfprint drives them fine"
  - name: "Rafale83"
    url: "https://github.com/Rafale83"
    for: "Reproducing the detector gap for Microarray MAFP 3274:8012 with a fake sysfs tree and a patch"
  - name: "BeameX"
    url: "https://github.com/BeameX"
    for: "Documenting that libfprint's own hwdb lists Validity 06cb:009a as unsupported"
  - name: "jcperdomoybarra"
    url: "https://github.com/jcperdomoybarra"
    for: "Writing up the ELAN 04f3:0c4b libfprint-tod stack that makes those readers work"
  - name: "StuartRP"
    url: "https://github.com/StuartRP"
    for: "Showing that setup can evict a working libfprint fork and still report success against the stale daemon"
  - name: "shawnyeager"
    url: "https://github.com/shawnyeager"
    for: "Proposing the lid-state PAM gate that Omarchy now ships"
faq:
  - q: "Does Omarchy set up my fingerprint reader automatically?"
    a: "No. It only detects one and offers to set it up. On first run you get a notification, and the menu row Setup > Security > Fingerprint appears when omarchy-hw-fingerprint returns true. Nothing is installed until you accept."
  - q: "Why does my fingerprint work for sudo but not to unlock the screen?"
    a: "Because sudo usually activates fprintd at a quiet moment, while the lock screen activates it inside logind's sleep-delay window. fprintd is then refused its own sleep inhibitor, never learns that the machine resumed, and refuses every lock-screen request. See issue #7229."
  - q: "Can I use my fingerprint instead of the LUKS passphrase at boot?"
    a: "No. Omarchy wires pam_fprintd into sudo, polkit and the lock screen only. Disk unlock at boot still needs the passphrase."
  - q: "How do I remove fingerprint auth?"
    a: "Remove > Security > Fingerprint in the menu, or omarchy-remove-security-fingerprint. It strips pam_fprintd and the lid gate from /etc/pam.d/sudo and /etc/pam.d/polkit-1, deletes /etc/pam.d/omarchy-lock-fingerprint, and drops fprintd and libfprint."
related: [fingerprint-enrollment-fails, lock-screen-wont-unlock, suspend-wont-resume-s2idle]
draft: false
---

Omarchy 4.x will use a fingerprint reader for `sudo`, for polkit prompts, and for the Quickshell lock screen. It will not use one for LUKS at boot. Everything below was checked against the v4.0.4 source tree and against issues filed between August 2025 and 16 September 2026.

## Status on 4.0.4

Fingerprint support is opt in and reasonably solid once it is running. The weak points are at the two ends: deciding whether your reader exists, and surviving suspend.

What holds up well:

- Enrollment and verification on Goodix and FocalTech match-on-chip readers, which cover most 2023 and newer laptops.
- The PAM wiring itself. Several people who had to install a different driver stack by hand reported that Omarchy's `sudo`, polkit and lock-screen PAM files worked unchanged once a working backend was in place (issues [#7006](https://github.com/omacom/omarchy/issues/7006) and [#11721](https://github.com/omacom/omarchy/issues/11721)).
- The closed-lid fallback. With the lid shut, PAM skips the reader and goes straight to the password.

What does not:

- Detection. Two vendor families are missed entirely, so the setup command refuses to run.
- Older Validity and ELAN readers that libfprint has no driver for. Setup asks for your finger anyway, then fails with a generic message.
- Suspend and resume. This is the single largest cluster of open reports on 4.x.

The component has 97 issues on record, 66 of them still open.

## What Omarchy does automatically

Nothing is installed until you ask. The pieces that ship by default are detection and the invitation.

`omarchy-hw-fingerprint` reads `/sys/bus/usb/devices` directly, so it works before `fprintd` or `usbutils` exist. It says yes when a device's product string contains `fingerprint`, `biometric`, `elan:arm-m4`, or starts with `fpc `, or when the USB vendor is one of `27c6 138a 06cb 08ff 1c7a 147e` and no kernel driver is bound to any interface. That driver check is deliberate: libfprint drives readers from userspace over libusb, so a real reader binds nothing, while the same vendors' touchpads and webcam bridges bind `usbhid` or `uvcvideo`.

That one script gates three things: the first-run notification in `install/user/first-run/setup-fingerprint.hook`, the visibility of the `Setup > Security > Fingerprint` menu row, and the setup command's own entry check.

`omarchy-setup-security-fingerprint` then does, in order: bail if no reader is detected, install `libfprint-git`, `fprintd` and `usbutils` in one `pacman --ask 4` transaction, run `fprintd-enroll`, run `fprintd-verify`, and only then write PAM. The ordering is intentional. The script's own comment notes that detection proves a reader is present, not that libfprint can drive it, so it refuses to edit the PAM stacks for a sensor it could not enroll against.

The PAM it writes is three files. `/etc/pam.d/sudo` and `/etc/pam.d/polkit-1` each get `auth sufficient pam_fprintd.so`, preceded by a `pam_exec` gate calling `/usr/bin/omarchy-hw-laptop-closed`. `/etc/pam.d/omarchy-lock-fingerprint` is a separate stack the lock screen opens on its own. Existing 3.x setups got the lid gate retrofitted by migration `1784818437.sh`.

Note the driver choice. Since [PR #10442](https://github.com/omacom/omarchy/pull/10442), merged 6 September 2026 and shipped in v4.0.3, setup installs `libfprint-git` rather than stock `libfprint`. It is a pinned upstream snapshot, so new readers are enabled by bumping the pin. In 3.x and early 4.0.x the flow was stock `libfprint`, and the direction has flipped twice, which is why migration `1785090473.sh` exists to repair machines left with `fprintd` and no library at all.

## Known problems

| Issue | Readers and models | Status | Fixed in |
| --- | --- | --- | --- |
| [#11384](https://github.com/omacom/omarchy/issues/11384) detector returns no sensor | FocalTech `2808:*`, ASUS ExpertBook and Vivobook, Samsung Galaxy Book | open | not yet |
| [#11426](https://github.com/omacom/omarchy/issues/11426) detector misses Microarray MAFP | `3274:8012`, ASUS ProArt P16 | open | not yet |
| [#11721](https://github.com/omacom/omarchy/issues/11721) `NoSuchDevice` on enroll | Validity `06cb:009a`, ThinkPad T480, T480s, T490, X1 Carbon 6th | open | not yet |
| [#7006](https://github.com/omacom/omarchy/issues/7006) setup clobbers a working open-fprintd stack | Validity `06cb:009a` and `138a:0097`, ThinkPad T480s, T570 | open | PR #8757 proposed |
| [#7483](https://github.com/omacom/omarchy/issues/7483) reader enrolls but never matches, or errors mid-enroll | ELAN `04f3:0c4b` and `04f3:0c58`, ThinkPad E14 and E15 Gen 3 and 4, IdeaPad 3 14ALC6, IdeaPad 5 15ITL05, ThinkBook 14 G8 | open | not yet |
| [#11899](https://github.com/omacom/omarchy/issues/11899) setup evicts a working libfprint fork, then reports success | Goodix `27c6:5395`, Dell XPS 15 7590 | open | not yet |
| [#11841](https://github.com/omacom/omarchy/issues/11841) no diagnosis when no driver exists | any unsupported reader | open | not yet |
| [#7229](https://github.com/omacom/omarchy/issues/7229) `Cannot run while suspended` after resume | Goodix MOC `27c6:634c`, `27c6:609c`, Intel Core Ultra laptops | open | not yet |
| [#11412](https://github.com/omacom/omarchy/issues/11412) unlock dead after every suspend, 4 Hz retry loop | Goodix MOC, Framework Laptop 13 AMD | open | not yet |
| [#11889](https://github.com/omacom/omarchy/issues/11889) enrolled print erased across suspend | Goodix MOC `27c6:6594` | open | not yet |
| [#12202](https://github.com/omacom/omarchy/issues/12202) only one PAM session per lock, reader dead after one miss | Broadcom ControlVault 3 `0a5c:5843`, TOD drivers | open | not yet |
| [#7645](https://github.com/omacom/omarchy/issues/7645) lock screen segfaults in `PamSubprocess` | any reader under overlapping retries | open | not yet |

The suspend cluster is worth understanding because it explains the most common complaint, which is fingerprint working for `sudo` but never for the lock screen. Two reporters on [#7229](https://github.com/omacom/omarchy/issues/7229) traced it the same way. The sleep monitor holds a logind delay inhibitor so it can lock before suspend. The lock screen appears inside that window and immediately starts fingerprint auth, which activates `fprintd` mid-transition. logind then refuses `fprintd` its own sleep-delay inhibitor, so it never receives `PrepareForSleep(false)` and its internal suspended flag is never cleared. The same process survives resume and denies everything after that. One reporter measured a poisoned instance lasting just over ten hours and 56 failed unlock attempts. `sudo` escapes this because it activates a fresh daemon outside any sleep transition.

The retry behaviour on top is contested and probably reader-dependent. Several reports ([#7176](https://github.com/omacom/omarchy/issues/7176), [#11412](https://github.com/omacom/omarchy/issues/11412)) describe `fingerprintRetryTimer` in `shell/plugins/lock/Service.qml` firing every 250 ms with no backoff and no cap, spawning PAM subprocesses four times a second for the whole lock. [#12202](https://github.com/omacom/omarchy/issues/12202) describes the opposite on a Broadcom TOD reader, where the single `PamContext` never goes inactive so no retry ever starts. The timer interval is in fact 250 ms in the v4.0.4 source. Both shapes are open.

## Fixes that work

Work down this list. Stop when the reader responds.

1. **Check detection first.** Run `omarchy-hw-fingerprint; echo $?`. Zero means detected. If it returns 1 but `lsusb` shows a reader, you have the false negative in #11384 or #11426. The script honours `OMARCHY_USB_DEVICES_PATH`, so you can point it at a fake sysfs tree containing a file named `product` with the word `fingerprint` in it to get past the gate, as both reporters did. The rest of setup then runs normally.
2. **Check that libfprint can actually open it.** Install `fprintd` and run `fprintd-list "$USER"`. `No devices available` while the kernel enumerates the device means no driver, not a bad finger. Look up your USB ID in `/usr/lib/udev/hwdb.d/60-autosuspend-libfprint-2.hwdb`, which lists known unsupported devices explicitly.
3. **If a driver exists, just run setup.** `omarchy setup security fingerprint`, or the menu row. Keep moving the finger around during enrollment.
4. **If you already installed a working alternative stack, do not re-run setup.** This is the trap in #7006 and #11899. Setup checks for the literal package name `libfprint-git`, which no fork can provide, so it removes your working driver without a prompt. Apply the three PAM edits by hand instead, copying the pattern from the setup script.
5. **After every suspend, restart the daemon.** The workaround from #7229 is a `system-sleep` hook that runs `systemctl stop fprintd.service` on both `pre` and `post`. A second reporter prefers keeping the daemon resident with `/usr/lib/fprintd --no-timeout` started with the session, so its inhibitor is installed at a quiet moment.
6. **If enrollment vanished rather than failed,** re-enroll and watch for #11889. A USB rebind that does not bring the print back points at genuine on-chip erasure.
7. **If a sensor stops responding entirely,** some ELAN and Broadcom units latch a firmware overheat state after repeated failures. It survives a daemon restart and a package reinstall. A USB device reset clears it.

Escaping a fingerprint prompt at a terminal is `Ctrl + C`, which drops you to the password. That was awkward enough to become issue [#856](https://github.com/omacom/omarchy/issues/856), and the lid gate that now ships came out of it.

## Report it

Fingerprint reports are only useful with the USB ID in them. Include, at minimum:

- `lsusb` output for the reader, with vendor and product ID.
- `omarchy-hw-fingerprint; echo $?`.
- `fprintd-list "$USER"` and `pacman -Q fprintd libfprint libfprint-git`.
- `journalctl -u fprintd -b` and `journalctl --user -t omarchy-shell -b` around the failure.
- `omarchy debug --no-sudo --print`, or drop `--print` to upload the log to `logs.omarchy.org` and paste the link.

File at [github.com/omacom/omarchy/issues](https://github.com/omacom/omarchy/issues). If your reader works and is not listed above, say so on [/hardware/submit/](/hardware/submit/) so the model pages can record it.

## Related

- [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/)
- [/fix/lock-screen-wont-unlock/](/fix/lock-screen-wont-unlock/)
- [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/)
- [/hardware/lenovo-thinkpad-t480/](/hardware/lenovo-thinkpad-t480/)
- [/hardware/framework-laptop-13/](/hardware/framework-laptop-13/)
- [/hardware/dell-xps-15-and-older/](/hardware/dell-xps-15-and-older/)
- [/reference/commands/omarchy-setup-security-fingerprint/](/reference/commands/omarchy-setup-security-fingerprint/)
- [Omarchy manual: Hardware authentication](https://omarchy.org/manual/hardware-authentication/)
