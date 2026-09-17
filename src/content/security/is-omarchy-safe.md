---
title: "Is Omarchy safe to use? The defaults, the criticisms, the fixes"
description: "A sourced look at Omarchy security: mandatory LUKS, ufw default deny, the docker group root escalation, and the hardening that shipped in 4.0.1 through 4.0.3."
answer: "Omarchy 4.0.4 is reasonable for a personal developer machine if you keep it updated. Full disk encryption is mandatory, ufw denies all incoming traffic except LocalSend, and ssh is off until you enable it. It also had a real root escalation through the docker group, fixed in 4.0.1, plus twenty-eight more hardening changes across 4.0.1, 4.0.2 and 4.0.3. Update first, then judge."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: info
reported: "Public criticism peaked 2026-08-26 and 2026-08-30 on Hacker News"
projectResponse: "Omarchy lists a five person security team, publishes a disclosure process and credits page, and shipped security fixes in 4.0.1, 4.0.2 and 4.0.3."
tags: [security, hardening, firewall, luks, docker, disclosure]
sources:
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Release v4.0.1: Fast-Follow Fixes"
    kind: release
    author: "dhh"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Release v4.0.2"
    kind: release
    author: "ryanrhughes"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3"
    kind: release
    author: "ryanrhughes"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/pull/8056"
    title: "PR #8056: Don't put the user in the docker group; make it opt-in"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://0xcc.io/posts/omarchy-root-creds/"
    title: "Omarchy: Any User Process Can Escalate to Root"
    kind: blog
    date: "2026-08-28"
  - url: "https://news.ycombinator.com/item?id=49499854"
    title: "Omarchy: Any User Process Can Escalate to Root (Hacker News)"
    kind: other
    date: "2026-08-30"
  - url: "https://blog.happyfellow.dev/merchants-of-insecurity/"
    title: "Merchants of Insecurity"
    kind: blog
    date: "2026-08-25"
  - url: "https://news.ycombinator.com/item?id=49447682"
    title: "Omarchy development practices lead to predictable security issues (Hacker News)"
    kind: other
    date: "2026-08-26"
  - url: "https://community.frame.work/t/omarchy-is-not-a-secure-distribution-and-should-be-taken-off-the-linux-installation-options/77363"
    title: "Omarchy is not a secure distribution and should be taken off the Linux installation options"
    kind: other
    author: "MayOrMayNotBeACat"
    date: "2025-11-03"
  - url: "https://omarchy.org/security/"
    title: "Omarchy: Report a vulnerability"
    kind: docs
  - url: "https://omarchy.org/security/credits/"
    title: "Omarchy security credits"
    kind: docs
  - url: "https://omarchy.org/teams/"
    title: "Omarchy Teams"
    kind: docs
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "0xcc.io"
    url: "https://0xcc.io/posts/omarchy-root-creds/"
    for: "Documenting the docker group root escalation and its disclosure timeline"
  - name: "One Happy Fellow"
    url: "https://blog.happyfellow.dev/merchants-of-insecurity/"
    for: "The critique of Omarchy's handling of untrusted input in shell scripts"
faq:
  - q: "Is Omarchy safe for a work laptop?"
    a: "For a personal developer machine on 4.0.4, the defaults are sensible. For a managed fleet, Omarchy does not ship an LSM policy, a hardened kernel, or centrally managed configuration, so it is a poor fit unless your organisation adds those itself."
  - q: "Was the root escalation ever exploited in the wild?"
    a: "No public evidence says so. The 0xcc.io writeup describes a private report followed by a fix, and the Omarchy security credits page thanks researchers who disclosed privately."
  - q: "Do I need to do anything if I installed before 4.0.1?"
    a: "Run Update > Omarchy. A migration removes your account from the docker group, and the change takes effect after a reboot. Check with id -nG afterwards."
  - q: "Does Omarchy have a CVE history?"
    a: "The project does not publish CVE identifiers for its own fixes. It lists them in release notes and thanks reporters on omarchy.org/security/credits/, which makes tracking harder than for a distro with a security advisory feed."
related: [docker-group-root-escalation, luks-and-ufw-defaults, signing-key-and-iso-verification]
draft: false
---

Omarchy is a personal desktop distribution built on Arch. Judged as that, and kept updated, it is reasonable to use. Judged as a hardened platform for a managed fleet, it is not, and it does not claim to be. The interesting part is what sits in between, because in August 2026 Omarchy shipped a real local root escalation and then shipped a lot of fixes for it and its neighbours.

This page checked against v4.0.4, released 2026-09-15, using the source tree for every tag from v3.8.4 forward.

## What the defaults actually do

Four things matter, and all four are verifiable on your own machine.

**Full disk encryption is mandatory.** The installer uses standard LUKS. There is no unencrypted path through the graphical installer. That protects a lost or stolen laptop, which is the threat most desktop users actually face.

**The firewall denies everything inbound except one port.** In v4.0.4, `install/config/firewall.sh` sets `ufw default deny incoming`, `ufw default allow outgoing`, and opens 53317 on TCP and UDP for LocalSend. It also allows DNS from Docker bridge ranges to the host, installs the `ufw-docker` rules so containers do not publish themselves past ufw, and enables the ufw service for the installed system.

**ssh is off by default.** You turn it on through Setup > Security > SSHD, which opens port 22 with rate limiting. Since 4.0.2, that flow also disables password authentication and hardens existing ssh installs.

**Packages and ISOs are signed.** The public key for ISO signatures and Omarchy repository packages is `40DFB630FF42BCFFB047046CF0134EE680CAC571`. Every ISO has a signature at the same URL with `.sig` appended. See [signing key and ISO verification](/security/signing-key-and-iso-verification/) and the [verify page](/verify/).

The official manual chapter is at [omarchy.org/manual/security/](https://omarchy.org/manual/security/).

## What went wrong

**The docker group.** Until 4.0.1, the installer ran `sudo usermod -aG docker ${USER}`. You can see the line in the v3.8.4 tree at `install/config/docker.sh`. Being in the docker group is root in all but name: any process running as you can ask the root owned daemon to mount `/` into a container and rewrite the host from inside it. That means a compromised browser extension, editor plugin, npm postinstall script or coding agent reached root with no prompt.

The 0xcc.io writeup published 2026-08-28 dates the group membership to June 2025 and the removal to 2026-08-24. It was posted to Hacker News on 2026-08-30, where it gathered 536 points. The fix is PR #8056, "Don't put the user in the docker group; make it opt-in", merged 2026-08-24 and shipped in v4.0.1. Full detail on [the docker group root escalation](/security/docker-group-root-escalation/).

**Shell scripts handling untrusted input.** Four days earlier, on 2026-08-26, a post titled "Merchants of Insecurity" hit Hacker News with 297 points. Its argument is about process rather than one bug: that Omarchy's habit of gluing the desktop together with shell scripts, some of them AI written, keeps producing injection bugs that the industry solved decades ago. It cites the video title that became part of a download command (PR #7847) and notification click actions that ran as a shell string (PR #7926). Both are in the v4.0.1 security list. See [notification and title bash injection](/security/notification-and-title-bash-injection/) and [development practices and AI written code](/security/development-practices-and-ai-written-code/).

**The older complaints.** A Framework community thread opened 2025-11-03 by MayOrMayNotBeACat argued Omarchy should be dropped from Framework's Linux install options. Its claims were that the firewall was configured but not actually enabled up to 3.1.0, that ssh was allowed through by default, that there is no LSM policy or hardened kernel, and that some install steps pipe curl into a shell. Two of those have moved. The 3.x tree carries a migration dated 2025-09-03 that enables and starts the ufw service on machines where rules were configured but the service was not enabled at boot, which is consistent with the firewall report, and by v3.8.4 first run calls `ufw --force enable` directly. That same v3.8.4 script opens only 53317, not 22, and in 4.x ssh stays off until you enable it. The kernel hardening and packaging complaints still stand: Omarchy ships its own `linux-omarchy` kernel as of 4.0.4, tuned for desktop responsiveness rather than hardening, and much of the system is bash rather than packaged units.

## How the project responded

Omarchy now lists a security team of five people on [omarchy.org/teams](https://omarchy.org/teams/), publishes a disclosure process at [omarchy.org/security](https://omarchy.org/security/), and keeps a [credits page](https://omarchy.org/security/credits/) thanking researchers who report privately. The site does not date when any of that appeared.

The releases show the shape of it:

- **v4.0.1** (2026-08-25) lists eleven security fixes, including the docker group change, safe argv for notification actions, blocking themes from running code at install, and pinning PATH in a privileged DNS helper.
- **v4.0.2** (2026-08-31) lists ten more, including requiring signed packages from the Omarchy repository, hardening CUPS, closing unprivileged input and ssh escalation paths, and disabling ssh password authentication. It also ships a migration that deletes root owned files left behind by three retired installers, including a first run sudoers grant and a Tailscale helper grant.
- **v4.0.3** (2026-09-08) lists seven, including requiring an expiry timer for temporary passwordless sudo, restricting plugin access to authentication services, and restricting Kitty remote control to local sockets.
- **v4.0.4** (2026-09-15) has no security section. It is the bespoke kernel release.

That is a fast response by most distro standards. It is also a lot of ground to have covered in three weeks, which is the honest read on both sides of the argument.

## What you can verify yourself

Check whether your account is in the root-equivalent docker group:

```bash
id -nG | tr ' ' '\n' | grep -x docker
```

Check the firewall state and every open port:

```bash
sudo ufw status verbose
```

Look for passwordless sudo grants left on the machine, and for an open passwordless sudo window:

```bash
sudo ls -la /etc/sudoers.d/
systemctl list-timers 'omarchy-nopasswd-*'
```

Confirm the signing key your system trusts:

```bash
gpg --fingerprint 40DFB630FF42BCFFB047046CF0134EE680CAC571
```

If `id -nG` still shows `docker` after updating to 4.0.1 or later, reboot. The migration removes the membership, but your session keeps its groups until you log out. If you deliberately opted back in with Setup > Security > Sudoless Docker, you have passwordless root again by choice.

The passwordless sudo toggle deserves the same clear eye the manual gives it. Setup > Security > Passwordless Sudo opens a 15 minute window during which anything running as you can become root without a prompt. More at [the passwordless sudo window](/security/passwordless-sudo-window/).

## What to watch for on newer versions

DHH has announced the next release as Quattro RS 4.5. Three things are worth rechecking when it lands.

First, whether the opt-in docker group stays opt-in. Convenience pressure runs the other way.

Second, plugins. Shell plugins and themes run unsandboxed in your session, and the 4.0.1 and 4.0.3 notes show the project tightening what they can touch rather than sandboxing them. See [plugins run unsandboxed](/security/plugins-run-unsandboxed/) and [install commands clone a mutable HEAD](/security/install-commands-clone-mutable-head/).

Third, patch lag. Arch itself is fast, but Omarchy pins a stable mirror snapshot, so a patched Arch package is not automatically a patched Omarchy package on the same day. See [stable mirror lag and CVEs](/security/stable-mirror-lag-and-cves/).

One thing this page cannot tell you: there is no CVE feed or security advisory stream for Omarchy's own fixes, so tracking what changed means reading release notes. Run `omarchy-update` regularly and read [before you update](/upgrade/before-you-update-checklist/) first.

## Related

- [The docker group root escalation](/security/docker-group-root-escalation/)
- [LUKS and ufw defaults](/security/luks-and-ufw-defaults/)
- [Unattended install passphrase handling](/security/unattended-install-plaintext-passphrase/)
- [Release history](/releases/)
