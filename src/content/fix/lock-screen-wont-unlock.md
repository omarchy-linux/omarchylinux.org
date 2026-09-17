---
title: "Omarchy lock screen will not unlock"
description: "Omarchy lock screen rejects the right password or never shows a prompt. Reset the faillock counter, restart the shell from a TTY, and repair the lock PAM file."
answer: "Two different faults look the same. If the box rejects a correct password, pam_faillock has locked the account: wait 120 seconds, or switch to a TTY with Ctrl+Alt+F2 and run faillock --user $USER --reset. If there is no password box at all, the lock client died and the compositor is holding the session. On 4.x run omarchy-restart-shell from that TTY instead of rebooting."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 210
errorStrings:
  - "Authentication failed (1)"
  - "Consecutive login failures for user <you> account temporarily locked"
  - "FATAL: Tried to show lockscreen surfaces without active lock"
  - "Authentication service cannot retrieve authentication info"
  - "Refusing to restart Omarchy shell while the session is locked."
  - "missing-pam"
  - "su: Authentication failure"
tags: [lock-screen, quickshell, hyprlock, pam, faillock, suspend]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6628"
    title: "Issue #6628: Lock shell dies during normal idle->lock; session permanently locked, reboot required"
    kind: issue
    author: "akashgagda"
    date: "2026-08-08"
  - url: "https://github.com/omacom/omarchy/pull/6630"
    title: "PR #6630: Make a dead lock client diagnosable and recoverable"
    kind: pr
    author: "dhh"
    date: "2026-08-09"
  - url: "https://github.com/omacom/omarchy/issues/1571"
    title: "Issue #1571: Can't become sudo sometimes, password not accepted"
    kind: issue
    author: "naxels"
    date: "2025-09-10"
  - url: "https://github.com/omacom/omarchy/issues/2094"
    title: "Issue #2094: Authentication failure via lock screen after some X amount of time"
    kind: issue
    author: "maxdmayhew"
    date: "2025-09-30"
  - url: "https://github.com/omacom/omarchy/discussions/1469"
    title: "Discussion #1469: Password auth failing randomly on Lock Screen"
    kind: discussion
    author: "sepulworld"
    date: "2025-09-05"
  - url: "https://github.com/omacom/omarchy/issues/3185"
    title: "Issue #3185: When every i wake my laptop from sleep, I always have to enter password two times even if it is correct"
    kind: issue
    author: "shubham-mamodiya-dev"
    date: "2025-11-05"
  - url: "https://github.com/omacom/omarchy/issues/9441"
    title: "Issue #9441: Plugin hot-reload while locked destroys the lock client; Quickshell then SIGABRTs"
    kind: issue
    author: "oliverlukschander"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/9485"
    title: "PR #9485: Honor keepLoaded for services during plugin hot-reload"
    kind: pr
    author: "barmstrong"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/10459"
    title: "Issue #10459: Session lock silently lost on output re-add: desktop exposed without authentication"
    kind: issue
    author: "nikitaprokopov"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/pull/10225"
    title: "PR #10225: Harden lock authentication command lookup"
    kind: pr
    author: "mdisec"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/pull/9618"
    title: "PR #9618: Restrict third-party plugin access to authentication services"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/11412"
    title: "Issue #11412: Fingerprint unlock fails after every suspend (fprintd device stuck busy) and the shell retries every 250ms until unlock"
    kind: issue
    author: "callumau"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/7176"
    title: "Issue #7176: Lock screen retries fingerprint auth every 250ms with no backoff, keeping throttled readers permanently disabled"
    kind: issue
    author: "AdamWorley"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/6223"
    title: "Issue #6223: Crash and restart after omarchy-system-lock"
    kind: issue
    author: "filip-spaldon"
    date: "2026-07-14"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "apfernandes"
    url: "https://github.com/apfernandes"
    for: "Reproduced the lockout from blind Enter presses on the lock screen and showed that a failed sudo shares the counter"
  - name: "akashgagda"
    url: "https://github.com/akashgagda"
    for: "Traced the dead lock client to the lock's own DPMS blank dropping the output, with before and after logs"
  - name: "nikitaprokopov"
    url: "https://github.com/nikitaprokopov"
    for: "Found that a lock lost on output re-add is treated as a successful unlock"
  - name: "callumau"
    url: "https://github.com/callumau"
    for: "Pinned the post-resume fingerprint failure to a busy fprintd device and a 250ms retry with no backoff"
  - name: "ItsMick"
    url: "https://github.com/ItsMick"
    for: "Posted the missing /etc/pam.d/hyprlock workaround for 3.x"
faq:
  - q: "How long does the Omarchy lockout last?"
    a: "The shipped PAM stack uses deny=10 and unlock_time=120, so after ten failures the account refuses the correct password for two minutes and then accepts it again. A successful authentication clears the counter."
  - q: "Can I recover a dead lock screen without rebooting?"
    a: "On 4.x yes. Switch to a TTY with Ctrl+Alt+F2 or SSH in, then run omarchy-restart-shell. It relaunches the shell, re-takes the session lock, and lets you authenticate normally. On 3.x there is no supported relock path, so a reboot is the practical route."
  - q: "Why does my first keypress on the lock screen get eaten?"
    a: "Several 3.x reports describe the first key or click after wake being swallowed while the lock surface is still coming up. Tap a key, wait a second, then type the password."
related: [black-screen-after-login, login-loop-or-password-not-accepted-sddm, suspend-wont-resume-s2idle, quickshell-crashes-or-bar-missing, fingerprint-enrollment-fails]
draft: false
---

Two very different faults produce the same complaint. Either the lock screen shows a password box and rejects a password you know is right, or there is no box at all and the desktop stays behind a blank or grey screen. Fix them differently.

## The fix

Start by working out which one you have. If you can see the Omarchy password field and it answers with `Authentication failed (1)`, go to step 1. If there is no field, no cursor, and nothing reacts, go to step 3.

**1. Wait out the lockout, or reset it.** Omarchy configures PAM with `deny=10 unlock_time=120`. After ten failures the correct password is refused for two minutes. Stop typing, wait, then try once more.

**2. Clear the counter from a TTY.** If waiting does not help, press `Ctrl + Alt + F2`, log in, and run:

```bash
faillock --user $USER          # shows the recorded failures
sudo faillock --user $USER --reset
```

Then `Ctrl + Alt + F1` back to the session and unlock. On 3.x and 4.0.0 the same thing is wrapped as `omarchy-sudo-reset`, which runs `su -c "faillock --reset --user $USER"` and needs the root password. That wrapper was removed in 4.0.1, so from there on use `faillock` directly. This is also what the manual's troubleshooting chapter recommends.

**3. Restart the shell instead of rebooting (4.x only).** When the Quickshell process that holds the lock dies, Hyprland keeps the session locked with no client left to type into. Get a TTY with `Ctrl + Alt + F2`, or SSH in from another machine, then:

```bash
omarchy-restart-shell
```

It kills the old instance, relaunches the shell through Hyprland, asks for the session lock again, and keeps checking `lock status` until it reports secure. Go back to the session and authenticate normally. This path landed in PR #6630 and shipped in 4.0.0. Older builds of `omarchy-restart-shell` bailed out whenever the session was locked, so a dead lock client meant a reboot.

**4. Repair the lock PAM file.** If the lock never appears at all, and `omarchy-shell lock lock` answers `missing-pam`, the file `/etc/pam.d/omarchy-lock-password` is missing. Recreate it:

```bash
sudo omarchy-apply-lock
```

The same command rewrites `/etc/pam.d/omarchy-lock-fingerprint` when you have prints enrolled, and removes it when you do not.

**5. On 3.x, check the hyprlock PAM file.** Omarchy 3.x locks with hyprlock, which needs `/etc/pam.d/hyprlock`. Users in issue #2094 reported unlock failing outright when it was absent, and restored it by writing a stack that includes `system-local-login`. On 4.x this file is irrelevant, since the Quickshell lock uses its own two stacks.

## Verify it worked

Ask the lock service directly rather than guessing:

```bash
omarchy-shell lock status     # JSON with locked, secure, requested, lastEvent
omarchy debug idle            # idle, screensaver and lock diagnostics in one dump
faillock --user $USER         # should print no failure records
journalctl -t omarchy-shell -n 100
```

The shell log lines look like `omarchy lock <timestamp> secure=true`. A healthy cycle logs `lock-requested`, then `secure=true`, then `unlocked`. Lines such as `lock-denied: missing-pam` or `lock-stranded: recovering` point straight at steps 4 and 3. Then test deliberately: run `omarchy system lock` from a terminal and unlock it once while you are sitting there.

## Why it happens

The rejected password is almost always `pam_faillock`, not a wrong password. The counter is shared: a mistyped `sudo` password in a terminal, or a script with a broken sudoers rule, counts toward the same lockout the lock screen enforces. In issue #1571 one reporter traced a constant lockout to a Waybar script calling `sudo wg show`. A common accidental trigger is waking the machine by mashing Enter, which submits empty passwords. That is the repro apfernandes posted on the same issue.

The missing password box is a different failure. Wayland's `ext-session-lock` deliberately keeps the session locked if the lock client dies, so the compositor shows its failsafe and nothing accepts input. In 4.x that client is the single Quickshell process. Reported ways to kill it: the lock's own DPMS blank causing a monitor to drop its DRM connector, which akashgagda demonstrated with an A/B test in issue #6628, and writing to any file under `~/.config/omarchy/plugins/` while locked, which used to tear down and recreate the lock service (issue #9441). PR #9485 made `keepLoaded` services survive a plugin hot reload and shipped in 4.0.3, so keep plugins out of the picture on 4.0.0 through 4.0.2.

4.0.3 also carried two changes to lock authentication. PR #10225 pinned the privileged lock helper's PATH and calls `/usr/bin/fprintd-list` by absolute path, and PR #9618 restricted third-party plugins from reaching the shell's authentication services, with the lock plugin now declaring an `authentication` capability in its manifest. If a custom plugin of yours reached into the lock or polkit services, it stopped working at 4.0.3 by design.

## If that did not work

Check the keyboard first. Locking runs `hyprctl switchxkblayout all 0`, which forces the first configured layout, so a second layout or a remapped Caps Lock can silently change what you type. See [layouts and locale](/keyboard/layouts-and-locale/).

Fingerprint unlock has its own open bug. If the machine suspends while a verify is in flight, fprintd comes back busy, PAM answers `Authentication service cannot retrieve authentication info`, and the shell retries every 250ms for the rest of the lock (issues #7176 and #11412, still open on 4.0.4). Type the password instead, or run `omarchy-remove-security-fingerprint` if you want the retry loop gone.

Two more open items worth knowing. Issue #10459 reports the opposite risk: a lock lost on output re-add is treated as a successful unlock and the desktop is exposed without a password. Issue #6223 covers machines that hard reset at DPMS off after lock, which is a kernel and GPU problem rather than a lock problem. Both were open when this page was checked against 4.0.4.

If you cannot reach a TTY at all, see [stuck at TTY or cannot switch TTY](/fix/stuck-at-tty-or-cannot-switch-tty/).

## Related

- [Black screen after login](/fix/black-screen-after-login/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Login loop or password not accepted in SDDM](/fix/login-loop-or-password-not-accepted-sddm/)
- [Suspend will not resume](/fix/suspend-wont-resume-s2idle/)
- [Fingerprint enrollment fails](/fix/fingerprint-enrollment-fails/)
- [Hardware notes on suspend and sleep](/hardware/suspend-sleep/)
