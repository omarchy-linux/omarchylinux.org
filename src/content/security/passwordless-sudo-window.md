---
title: "Omarchy's passwordless sudo window: risk and how to shorten it"
description: "What Omarchy's temporary passwordless sudo window does, the NOPASSWD sudoers file it writes, the real risk, and how to end it early or shorten it."
answer: "Omarchy's Passwordless Sudo toggle writes a blanket NOPASSWD rule for your user and arms a systemd timer to delete it, 15 minutes by default. End it early by running omarchy-sudo-passwordless again with no argument. Shorten the default by passing minutes, for example omarchy-sudo-passwordless 5. Since 4.0.3 a boot rule also clears any grant left behind by a reboot."
appliesTo:
  from: "3.x"
status: by-design
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: medium
reported: "Issue #8218, 2026-08-25, by lbonvarl"
projectResponse: "Omarchy shipped the fail-closed expiry and boot-time cleanup in v4.0.3, listed in the release notes as \"Require expiry setup for temporary passwordless sudo\"."
tags: [sudo, sudoers, privilege-escalation, agents, hardening]
sources:
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/8218"
    title: "Issue #8218: Passwordless sudo expiry is lost on reboot, leaving NOPASSWD active"
    kind: issue
    author: "lbonvarl"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/pull/9387"
    title: "PR #9387: Fail closed when passwordless sudo expiry cannot arm"
    kind: pr
    author: "ErikMelton"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/7990"
    title: "PR #7990: Clear passwordless sudo grants at boot"
    kind: pr
    author: "Adolanium"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/9066"
    title: "Issue #9066: `omarchy update` hangs on a sudo password prompt even after `omarchy sudo passwordless`"
    kind: issue
    author: "duffmahn"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10352"
    title: "Issue #10352: omarchy update prompts for password even when the user has a NOPASSWD sudoers drop-in (sudo -v gate)"
    kind: issue
    author: "christianjgilman"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/5708"
    title: "Issue #5708: First-run sudoers allows unrestricted systemctl"
    kind: issue
    author: "afurm"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Omarchy v4.0.3 release notes"
    kind: release
    date: "2026-09-08"
credits:
  - name: "lbonvarl"
    url: "https://github.com/lbonvarl"
    for: "Reported that the expiry timer did not survive a reboot"
  - name: "Adolanium"
    url: "https://github.com/Adolanium"
    for: "Proposed clearing leftover grants at boot"
  - name: "ErikMelton"
    url: "https://github.com/ErikMelton"
    for: "Shipped the fail-closed expiry and boot cleanup merged for 4.0.3"
  - name: "duffmahn"
    url: "https://github.com/duffmahn"
    for: "Traced the sudo -v prompt to sudo's verifypw default"
faq:
  - q: "How long does Omarchy's passwordless sudo last?"
    a: "Fifteen minutes by default. Pass a number of minutes to change it, for example omarchy-sudo-passwordless 5. A reboot also ends it on 4.0.3 and later."
  - q: "How do I turn passwordless sudo off right now?"
    a: "Run omarchy-sudo-passwordless with no argument. It sees the existing grant, deletes the sudoers file, and stops the expiry timer."
  - q: "Why does omarchy update still ask for my password while passwordless sudo is on?"
    a: "The updater calls sudo -v, and sudo's verifypw default of all makes that prompt whenever any matching rule needs a password. Omarchy's own %wheel rule is one. This is open as issue #9066."
  - q: "Is passwordless sudo on by default in Omarchy?"
    a: "No. Nothing enables it for you. You have to run the menu item or the command and confirm the warning prompt."
related: [is-omarchy-safe, docker-group-root-escalation, plugins-run-unsandboxed]
draft: false
---

Omarchy ships a deliberate, temporary way to make `sudo` stop asking for a password. It exists mostly for AI coding agents doing a long stretch of system work, where a password prompt in the middle stalls everything. The manual is blunt about the tradeoff, and so is the command itself. This page explains exactly what it writes to disk, what changed in 4.0.3, and how to end or shorten the window.

Checked against v4.0.4. The behaviour described here is the same in the v4.0.3 and v4.0.4 source trees, and the same again in the development branch for the next release.

## What the toggle actually does

Two entry points, one script:

- Omarchy menu: _Setup > Security > Passwordless Sudo_
- Terminal: `omarchy-sudo-passwordless [MINUTES]`, also routed as `omarchy sudo passwordless`

When you confirm the warning, the script writes a sudoers drop-in for your user and sets it to mode 0440. The file is `/etc/sudoers.d/99-omarchy-nopasswd-$USER`, and its one line is:

```bash
$USER ALL=(ALL) NOPASSWD: ALL
```

Then it arms a transient systemd timer whose only job is to delete that file again:

```bash
sudo systemd-run --on-active=15m --timer-property=AccuracySec=1s \
  --unit="omarchy-nopasswd-expire-$USER" rm -f -- /etc/sudoers.d/99-omarchy-nopasswd-$USER
```

Fifteen minutes is the default. `omarchy-sudo-passwordless 30` gives you thirty. The rule is not scoped to a command, a package manager, or the Omarchy tooling. It is `NOPASSWD: ALL`, so while it is live, anything already running as your user, a shell plugin, a browser extension host, a compromised npm postinstall, an agent that took a bad instruction, can run any command as root without a prompt and without leaving a password trail.

That is the whole risk, and it is by design. There is no narrower mode.

## The fix: end it early or shorten the window

1. End the window right now. Run the same command with no argument:

   ```bash
   omarchy-sudo-passwordless
   ```

   With the grant in place and no minutes argument, the script deletes the sudoers file and stops the expiry timer. It prints that passwordless sudo has been disabled.

2. Prefer a shorter default. Pass the minutes you actually need rather than accepting fifteen:

   ```bash
   omarchy-sudo-passwordless 5
   ```

   Running it again with a number while a grant is already live stops the old timer and arms a new one, so you can shrink a running window instead of waiting it out.

3. Remove a grant by hand if the script is not available:

   ```bash
   sudo rm -f "/etc/sudoers.d/99-omarchy-nopasswd-$USER"
   sudo systemctl stop "omarchy-nopasswd-expire-$USER.timer"
   ```

4. Avoid the window entirely for scripted work. Put `source omarchy-sudo-keepalive` at the top of your script, which is how Omarchy's own package installers use it. It prompts once with `sudo -v` and refreshes the sudo timestamp in the background until the script exits. That keeps a normal, per-user sudo credential instead of a blanket NOPASSWD rule.

## Verify it worked

Check the file and the timer, then ask sudo itself:

```bash
ls -l /etc/sudoers.d/ | grep 99-omarchy-nopasswd
systemctl list-timers --all | grep omarchy-nopasswd-expire
sudo -l | grep NOPASSWD
```

No `99-omarchy-nopasswd-<you>` file means no window. If the file is gone but a timer is still listed, stop the timer as shown above. `sudo -l` prints the rules that apply to you, so a lingering `(ALL) NOPASSWD: ALL` line there is the grant still being live.

You can also confirm the boot cleanup rule is installed on 4.0.3 or later:

```bash
systemd-tmpfiles --cat-config | grep omarchy-nopasswd
```

You should see a boot-only rule matching `/etc/sudoers.d/99-omarchy-nopasswd-*`.

## Why it happens, and what 4.0.3 changed

The expiry timer has been there since 3.x. The problem was what happened when the timer was not there.

Loic Bonvarlet reported in [issue #8218](https://github.com/omacom/omarchy/issues/8218) that the timer is transient, so systemd discards it at shutdown, while the sudoers file is an ordinary file on disk that survives. Reboot inside the fifteen minutes and you came back up with an unrestricted `NOPASSWD: ALL` rule and nothing left scheduled to remove it. The script only cleaned that up if you happened to run it again. The issue is closed.

Two changes landed in v4.0.3, both in [PR #9387](https://github.com/omacom/omarchy/pull/9387) by ErikMelton, which kept the boot cleanup first proposed by Adolanium in [PR #7990](https://github.com/omacom/omarchy/pull/7990):

- A boot-only `systemd-tmpfiles` rule removes any leftover `99-omarchy-nopasswd-*` drop-in during early boot. The `r!` form matters here: it fires only on the boot pass, so a `systemd-tmpfiles --remove` run later in the session leaves a live grant alone.
- The script now fails closed. If `systemd-run` cannot arm the timer, the script deletes the grant it just wrote and exits non-zero instead of leaving an unexpiring NOPASSWD rule behind. Before 4.0.3 the grant was published first and the timer armed afterwards, so a failed `systemd-run` left the window open forever.

The v4.0.3 release notes list this as "Require expiry setup for temporary passwordless sudo". The manual line about a restart removing the rule was added in the same release, so a 4.0.0 through 4.0.2 machine still has the reboot gap. If you are on 4.0.2 or older, update before you use this feature.

A caveat the project states plainly: removing the rule does not revoke anything already running. A root process that started during the window keeps its privileges after the grant is gone.

## If that did not work

**`sudo` still prompts even though the grant is live.** This is a known open bug, not a broken install. `omarchy update` calls `sudo -v`, and sudo's `verifypw` option defaults to `all`, which makes validation prompt if any rule matching you requires a password. On a 4.x install, `omarchy-provision-owner` writes `%wheel ALL=(ALL:ALL) ALL` to `/etc/sudoers.d/00-omarchy-wheel`, and older installs carry an equivalent password-required rule under another name (the reporter of #10352 found it as `04_<user>`). That rule alone is enough to trigger the prompt while actual `sudo <command>` runs stay passwordless. Duffmahn traced this in [issue #9066](https://github.com/omacom/omarchy/issues/9066) and christianjgilman filed the same root cause from a hand-rolled drop-in in [issue #10352](https://github.com/omacom/omarchy/issues/10352). Both are open as of 2026-09-16. Both reporters say a `verifypw` override in a sudoers drop-in gets past it (`Defaults:<user> verifypw=any` in #9066, `Defaults verifypw=never` in #10352), but that changes how sudo validates credentials, so treat it as a workaround rather than a setting to leave in place.

**A grant you did not create.** Two retired Omarchy install scripts left root-owned sudoers files behind: `/etc/sudoers.d/first-run`, which granted unrestricted `systemctl` as reported in [issue #5708](https://github.com/omacom/omarchy/issues/5708), and `/etc/sudoers.d/tsui` from the dropped Tailscale helper. A migration that shipped in 4.0.2 inspects both and removes them if they match what the installer wrote. It runs as part of `omarchy update`, but it needs an account that can use sudo and fails loudly otherwise, so if your updates run from an unprivileged account, run `omarchy-migrate` once from one that can. The first-run grant was written by installs between August 2025 and late May 2026. Check anyway with `sudo ls -l /etc/sudoers.d/`.

**Nothing to do with Omarchy's toggle.** If `sudo -l` shows a NOPASSWD rule in a file that is not `99-omarchy-nopasswd-<you>`, something else wrote it. Read the file before deleting it.

## What to watch for on newer versions

The passwordless sudo script, the tmpfiles rule and the security manual chapter are byte for byte identical between v4.0.4 and the quattro-dev branch for the next release, so nothing here is queued to change. The `sudo -v` bug is the thing to re-check after the next release. Issue #9066 proposes either dropping the updater's `sudo -v` pre-flight or having `omarchy-sudo-passwordless` set `verifypw` itself, and #10352 asks for documentation or a non-interactive updater, so a fix could land in either place.

## Related

- [Is Omarchy safe?](/security/is-omarchy-safe/)
- [The docker group is passwordless root](/security/docker-group-root-escalation/)
- [Plugins run unsandboxed](/security/plugins-run-unsandboxed/)
- Official manual: [Security](https://omarchy.org/manual/security/)
