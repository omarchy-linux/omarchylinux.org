---
title: "Fingerprint readers on Omarchy"
description: "Fingerprint readers on Omarchy 4.0.4: what enrolls out of the box, the omarchy-hw-fingerprint detection gaps, fprintd wedging after suspend, and the fix order."
answer: "Fingerprint auth is opt in. Run Setup > Security > Fingerprint, or omarchy setup security fingerprint, and Omarchy installs libfprint-git and fprintd, enrolls a finger, and wires sudo, polkit and the lock screen. Goodix MOC and FocalTech readers that libfprint has a driver for enroll and verify. The common failures are detection false negatives, readers with no libfprint driver, and fprintd wedging after suspend."
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
    for: "Proposing a lid-state PAM gate in 2025, the same shape Omarchy shipped in 4.x"
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

- Enrollment and verification on Goodix MOC readers the pinned libfprint knows (`27c6:609c`, `27c6:634c`, `27c6:6594`) and on FocalTech `2808` readers once detection is bypassed. Every reporter on the suspend issues below had a working reader before the first suspend.
- The PAM wiring itself. Several people who had to install a different driver stack by hand reported that Omarchy's `sudo`, polkit and lock-screen PAM files worked unchanged once a working backend was in place (issues [#7006](https://github.com/omacom/omarchy/issues/7006) and [#11721](https://github.com/omacom/omarchy/issues/11721)).
- The closed-lid fallback for `sudo` and polkit. With the lid shut, those two stacks skip the reader and go straight to the password. The lock screen has no such gate.

What does not:

- Detection. Two vendor families are missed entirely, so the setup command refuses to run.
- Readers libfprint cannot drive: Validity `06cb:009a` and `138a:0097`, Goodix IDs outside the pinned snapshot such as `27c6:5395` and `27c6:55b4`, and ELAN `04f3:0c4b`, which the stock driver claims but mishandles. Setup asks for your finger anyway, then fails with a generic message.
- Suspend and resume. This is the largest cluster of open reports on 4.x.

The component has 97 issues on record, 66 of them still open.

## What Omarchy does automatically

Nothing is installed until you ask. The pieces that ship by default are detection and the invitation.

`omarchy-hw-fingerprint` reads `/sys/bus/usb/devices` directly, so it works before `fprintd` or `usbutils` exist. It says yes when a device's product string contains `fingerprint`, `biometric`, `elan:arm-m4`, or starts with `fpc `, or when the USB vendor is one of `27c6 138a 06cb 08ff 1c7a 147e` and no kernel driver is bound to any interface. That driver check is deliberate: libfprint drives readers from userspace over libusb, so a real reader binds nothing, while the same vendors' touchpads and webcam bridges bind `usbhid` or `uvcvideo`.

That one script gates three things: the first-run notification in `install/user/first-run/setup-fingerprint.hook`, the visibility of the `Setup > Security > Fingerprint` menu row, and the setup command's own entry check.

`omarchy-setup-security-fingerprint` then does, in order: bail if no reader is detected, install `libfprint-git`, `fprintd` and `usbutils` in one `pacman --ask 4` transaction, run `fprintd-enroll`, run `fprintd-verify`, and only then write PAM. The ordering is intentional. The script's own comment notes that detection proves a reader is present, not that libfprint can drive it, so it refuses to edit the PAM stacks for a sensor it could not enroll against.

The PAM it writes is three files. `/etc/pam.d/sudo` and `/etc/pam.d/polkit-1` each get `auth sufficient pam_fprintd.so`, preceded by a `pam_exec` gate calling `/usr/bin/omarchy-hw-laptop-closed`. `/etc/pam.d/omarchy-lock-fingerprint` is a separate stack the lock screen opens on its own. Existing 3.x setups got the lid gate retrofitted by migration `1784818437.sh`.

Note the driver choice. Since [PR #10442](https://github.com/omacom/omarchy/pull/10442), merged 6 September 2026 and shipped in v4.0.3, setup installs `libfprint-git` rather than stock `libfprint`. It is a pinned upstream snapshot, so new readers are enabled by bumping the pin. Before 4.0.3 setup installed stock `libfprint`, and an earlier form of migration `1785090473.sh` had already swapped `libfprint-git` out for stock once, so the direction has flipped twice. That migration now only repairs machines its two-step form left with `fprintd` and no library at all.

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
| [#7229](https://github.com/omacom/omarchy/issues/7229) `Cannot run while suspended` after resume | Goodix MOC `27c6:634c`, `27c6:609c`, `27c6:6594`, `27c6:6890`, Synaptics `06cb:00fc`; Framework 13 and 16, ThinkPad X1 Carbon Gen 11 and X13 Gen 2a, Dell Precision 5690, Intel Core Ultra laptops | open | PRs #7158, #9868, #9919 open |
| [#11412](https://github.com/omacom/omarchy/issues/11412) unlock dead after every suspend, 4 Hz retry loop | Goodix MOC, Framework Laptop 13 AMD, ThinkPad T14 Gen 7 AMD | open | not yet |
| [#11889](https://github.com/omacom/omarchy/issues/11889) enrolled print erased across suspend | Goodix MOC `27c6:6594` | open | not yet |
| [#12202](https://github.com/omacom/omarchy/issues/12202) only one PAM session per lock, reader dead after one miss | Broadcom ControlVault 3 `0a5c:5843`, TOD drivers | open | not yet |
| [#7645](https://github.com/omacom/omarchy/issues/7645) lock screen segfaults in `PamSubprocess` | any reader when the shell dies mid-conversation | open | upstream quickshell fix landed after 0.3.1; not in the 0.3.1 Omarchy ships |

The suspend cluster is worth understanding because it explains the most common complaint, which is fingerprint working for `sudo` but never for the lock screen. Two reporters on [#7229](https://github.com/omacom/omarchy/issues/7229) traced it the same way. Omarchy's sleep monitor takes a logind delay inhibitor of its own so that the screen locks before the machine goes down. Locking starts fingerprint auth at once, and on a machine where `fprintd` is not already resident that D-Bus-activates the daemon while logind is mid-transition, so logind turns down the daemon's request for its own inhibitor. Without one, `fprintd` never hears `PrepareForSleep(false)`, its suspended flag stays set, and that same process carries on refusing requests after resume. One reporter measured a poisoned instance lasting just over ten hours and 56 failed unlock attempts. `sudo` tends to reach a freshly started daemon with no sleep in progress, which is why it keeps working. Two later reports complicate the picture: on a ThinkPad X13 using `deep` suspend the daemon wedged with its inhibitor installed, and on an X1 Carbon Gen 11 a resume-time USB disconnect left `fprintd` holding a dead first device that `pam_fprintd` kept picking over the live second one. In both the common factor is a verify left open across the transition.

The retry behaviour on top is contested and probably reader-dependent. Several reports ([#7176](https://github.com/omacom/omarchy/issues/7176), [#11412](https://github.com/omacom/omarchy/issues/11412)) describe `fingerprintRetryTimer` in `shell/plugins/lock/Service.qml` rearming on every error at a flat 250 ms, never slowing down and never giving up, so a reader that fails instantly gets a fresh PAM subprocess roughly four times a second until someone types the password. [#12202](https://github.com/omacom/omarchy/issues/12202) describes the opposite on a Broadcom TOD reader, where the single `PamContext` never goes inactive so no retry ever starts. The timer interval is in fact 250 ms in the v4.0.4 source. Both shapes are open.

## Fixes that work

Work down this list. Stop when the reader responds.

1. **Check detection first.** Run `omarchy-hw-fingerprint; echo $?`. Zero means detected. If it returns 1 but `lsusb` shows a reader, you have the false negative in #11384 or #11426. The script honours `OMARCHY_USB_DEVICES_PATH`, so you can point it at a fake sysfs tree containing a file named `product` with the word `fingerprint` in it to get past the gate, as the #11384 reporter did. The rest of setup then ran normally on that FocalTech machine; the #11426 reporter installed the packages and wrote the PAM files by hand instead.
2. **Check that libfprint can actually open it.** Install `fprintd` and run `fprintd-list "$USER"`. If that prints `No devices available` even though `lsusb` shows the reader, the problem is a missing driver, not your finger. Look up your USB ID in `/usr/lib/udev/hwdb.d/60-autosuspend-libfprint-2.hwdb`, which lists known unsupported devices explicitly.
3. **If a driver exists, just run setup.** `omarchy setup security fingerprint`, or the menu row. Keep moving the finger around during enrollment.
4. **If you already installed a working alternative stack, do not re-run setup.** This is the trap in #7006 and #11899. Setup checks for the literal package name `libfprint-git`, which no fork can provide, so it removes your working driver without a prompt. Apply the three PAM edits by hand instead, copying the pattern from the setup script.
5. **After every suspend, restart the daemon.** The workaround from #7229 is an executable hook in `/usr/lib/systemd/system-sleep/` that runs `systemctl stop fprintd.service` on both `pre` and `post`. `/etc/systemd/system-sleep/` is not scanned, and a file without the executable bit is ignored silently. One reporter warns that a wedged daemon ignores `SIGTERM`, so a plain stop can hold up resume for the ten second kill timeout; `systemctl kill -s KILL` avoids that, and enrollments live on disk so nothing is lost. A second reporter prefers keeping the daemon resident with `/usr/lib/fprintd --no-timeout` started with the session, so its inhibitor is installed at a quiet moment. Three PRs cover this ([#7158](https://github.com/omacom/omarchy/pull/7158), [#9868](https://github.com/omacom/omarchy/pull/9868), [#9919](https://github.com/omacom/omarchy/pull/9919)); all were still open on 17 September.
6. **If enrollment vanished rather than failed,** re-enroll and watch for #11889. A USB rebind that does not bring the print back points at genuine on-chip erasure.
7. **If a sensor stops responding entirely,** check `journalctl -u fprintd` for `Device disabled to prevent overheating`. ELAN, Broadcom, Upek and TOD-driven Goodix units all report it after enough rapid failures, and the retry loop above keeps them there. On the ELAN unit in #7483 it survived a daemon restart and a package reinstall, and only a USB device reset cleared it; on the Upek reader in #7176 restarting `fprintd` was enough.

Escaping a fingerprint prompt at a terminal is `Ctrl + C`, which drops you to the password. It did not always land cleanly: issue [#856](https://github.com/omacom/omarchy/issues/856) reports the keystroke ending up as the first character of the password, and its reporter proposed a lid-state PAM gate a year before Omarchy shipped one.

## Report it

Fingerprint reports are only useful with the USB ID in them. Include, at minimum:

- `lsusb` output for the reader, with vendor and product ID.
- `omarchy-hw-fingerprint; echo $?`.
- `fprintd-list "$USER"` and `pacman -Q fprintd libfprint libfprint-git`.
- `journalctl -u fprintd -b` and `journalctl --user -t omarchy-shell -b` around the failure.
- `omarchy debug --no-sudo --print`, or drop `--print` and pick `Upload log` to send it to `logs.omarchy.org` and paste the link.

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
