---
title: "What Omarchy encrypts and firewalls by default"
description: "Omarchy ships LUKS full-disk encryption and ufw set to deny incoming, with port 53317 open for LocalSend and ufw-docker rules. What that covers and misses."
answer: "Omarchy installs LUKS full-disk encryption by default, and configures ufw to deny all incoming traffic and allow all outgoing. Only port 53317 (TCP and UDP) is open, for LocalSend, plus two Docker DNS rules and the ufw-docker block in after.rules. SSH is off until you enable it. Outbound traffic, the EFI partition, and anything after unlock are not covered."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: info
reported: "Documented posture, Omarchy manual security chapter; the LocalSend rule scope raised in issue #11560 on 2026-09-12"
projectResponse: "The manual states that full-disk encryption is mandatory and that all incoming traffic is blocked by default except port 53317 for LocalSend, with Docker locked down via ufw-docker."
tags: [luks, ufw, firewall, encryption, docker, defaults]
sources:
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy manual: Security"
    kind: manual
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy manual: Dual Boot Install"
    kind: manual
  - url: "https://omarchy.org/manual/unattended-installs/"
    title: "Omarchy manual: Unattended Installs"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/11560"
    title: "Issue #11560: Default ufw rule for LocalSend (port 53317) allows inbound from Anywhere, including IPv6"
    kind: issue
    author: "CRTFD-DVLPR"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11757"
    title: "Issue #11757: Docker DNS defaults hardcode 172.17.0.1, colliding with routers on that subnet"
    kind: issue
    author: "OtherStep"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/8248"
    title: "Issue #8248: OpenSSH daemon bound to all interfaces"
    kind: issue
    author: "helioryn"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/6229"
    title: "Issue #6229: vconsole.conf bundled into initramfs locks out LUKS users with non-Latin keyboard layouts (Hebrew/Greek/Cyrillic)"
    kind: issue
    author: "elpddev"
    date: "2026-07-16"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Omarchy v4.0.2 release notes"
    kind: release
    date: "2026-08-31"
  - url: "https://github.com/chaifeng/ufw-docker"
    title: "ufw-docker: solve the problem that Docker bypasses UFW rules"
    kind: docs
credits:
  - name: "CRTFD-DVLPR"
    url: "https://github.com/CRTFD-DVLPR"
    for: "Pointed out that the LocalSend rule is unscoped and therefore reachable over globally routable IPv6"
  - name: "elpddev"
    url: "https://github.com/elpddev"
    for: "Traced the non-Latin keymap LUKS lockout to the initramfs vconsole bundling"
faq:
  - q: "Is full-disk encryption really mandatory on Omarchy?"
    a: "The manual's security chapter calls it mandatory, but the getting-started chapter documents an opt-out: press Ctrl+C at the disk formatting confirmation to install without encryption. Treat it as on by default and easy to skip, not impossible to skip."
  - q: "Do I need to open ports for LocalSend myself?"
    a: "No. The installer already opens 53317 on TCP and UDP. If you do not use LocalSend, you can delete those two rules."
  - q: "Does the firewall stop a Docker container from being reachable?"
    a: "Yes, because Omarchy runs ufw-docker install, which adds a DOCKER-USER filter block to /etc/ufw/after.rules. Without it, a published container port bypasses ufw entirely."
  - q: "Is SSH open on a fresh install?"
    a: "No. sshd is not enabled by install/config/enable-services.sh and port 22 is closed. Setup > Security > SSHD runs omarchy-setup-security-sshd, which adds a rate-limited ufw rule for 22/tcp."
related: [is-omarchy-safe, docker-group-root-escalation, unattended-install-plaintext-passphrase]
draft: false
---

Omarchy's out-of-the-box security posture is two decisions: the disk is encrypted with LUKS, and the network is closed except for one file-sharing port. Beyond those two, the base install leans on Arch defaults plus a handful of targeted hardening changes listed in the release notes. This page states exactly what those two decisions cover on 4.0.4, checked against the installer scripts in the source tree, and where the gaps are.

## The two defaults, precisely

**Disk.** The installer encrypts the root partition with LUKS by default. That applies to the full-disk install and to the free-space install used for dual boot, which the manual says is "effectively no different than full drive". The encryption covers the whole Btrfs root, so `/home`, your Snapper snapshots, and logs are all inside it, and so is the hibernation swapfile at `/swap/swapfile` if you have run `omarchy hibernation setup` (it is not created by default). The zram swap device lives in RAM and never touches the disk at all.

**Network.** One file does the firewall work, `/usr/share/omarchy/install/config/firewall.sh`, and it is short enough to read in full. It sets `ufw default deny incoming` and `ufw default allow outgoing`, opens 53317 on both UDP and TCP for LocalSend, adds two rules letting Docker containers reach DNS on the host at 172.17.0.1, runs `ufw-docker install`, then sets `ENABLED=yes` in `/etc/ufw/ufw.conf` and enables the ufw unit. It deliberately does not activate ufw during the install itself, because the install runs in a chroot that shares the live ISO's kernel firewall. The firewall comes up on the first boot of the installed system.

That is the whole default rule set. There is no other port.

## Check what your machine actually has

```bash
sudo ufw status verbose
systemctl is-enabled ufw
lsblk -o NAME,TYPE,FSTYPE,MOUNTPOINTS
```

A stock 4.0.x install should show `Default: deny (incoming), allow (outgoing), disabled (routed)` and four LocalSend lines (IPv4 and IPv6, TCP and UDP) plus the two `allow-docker-dns` rules. Your root device should appear under a `crypt` type in `lsblk`, sitting on a `crypto_LUKS` partition.

Confirm the Docker protections landed, which is the part most likely to be missing on a machine upgraded from 3.x:

```bash
grep -c ufw-docker /etc/ufw/after.rules
sudo iptables -S DOCKER-USER
```

If `after.rules` has no `ufw-docker` block, re-run the packaged script:

```bash
sudo bash /usr/share/omarchy/install/config/firewall.sh
sudo ufw reload
```

The Quattro upgrade tool, `omarchy-upgrade-to-quattro`, calls that same packaged script rather than carrying its own copy. The comment above its `apply_firewall_defaults` function says why: the copy it replaced had drifted and never installed the ufw-docker rules, so upgraded machines came up without the Docker protections a fresh install gets. That function is present in every 4.0.x release in the source tree, so the gap belongs to earlier upgrade-tool builds, not to the shipped installer.

## What the encryption does not cover

The EFI system partition is not encrypted. It holds the unified kernel image and the Limine configuration, so anyone with physical access can modify what your machine boots. Omarchy's own getting-started chapter tells you to turn Secure Boot and/or TPM off in the BIOS before installing, so there is no measured boot and no signed boot chain to detect that tampering. LUKS protects a powered-off machine against data extraction, not against an evil-maid boot-image swap.

Encryption also stops mattering the moment the machine is unlocked. Once you have typed the passphrase and booted, the root filesystem is plaintext to anything running as your user, including agents, shell plugins, and anything in a Docker container you run as root.

Two operational notes. First, the passphrase is typed at the Plymouth prompt with a Latin keymap. Issue #6229, reported by elpddev on 2026-07-16 and since closed, showed that bundling a non-Latin layout such as Hebrew, Greek, Cyrillic, or Arabic into the initramfs made the correct passphrase untypeable and locked users out. The packaged `omarchy_hooks.conf` now skips bundling `vconsole.conf` for those layouts. See [non-US keyboard layouts at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/). Second, encryption is opt-out, not compulsory: pressing Ctrl+C at the disk formatting confirmation switches to an unencrypted install, and the dual-boot chapter says the free-space install offers the same unencrypted option, marked not recommended. The security chapter's word "mandatory" describes the intent, not the installer.

If you are imaging machines, note that the `disk_encryption` block in a cidata `user_configuration.json` carries the passphrase in plaintext. See [unattended install plaintext passphrase](/security/unattended-install-plaintext-passphrase/).

## What the firewall does not cover

**Outgoing traffic is unrestricted.** `default allow outgoing` means any process running as you can reach any host on any port. Nothing in the base install inspects, logs, or limits that.

**The LocalSend rule is not scoped to your LAN.** `ufw allow 53317/tcp` applies to IPv4 and IPv6 from anywhere. Issue #11560, opened by CRTFD-DVLPR on 2026-09-12 against 4.0.3 and still open, points out that many home and mobile networks hand out globally routable IPv6 addresses with no NAT in front, so a LocalSend receiver meant for the local Wi-Fi can be reachable from the internet. If you do not use LocalSend, close it:

```bash
sudo ufw delete allow 53317/tcp
sudo ufw delete allow 53317/udp
sudo ufw reload
```

If you do use it, the issue's suggested shape is to re-add it scoped to private ranges. That is a user change, not upstream behaviour, so test it before relying on it.

**The Docker DNS rules hardcode 172.17.0.1.** That is the classic Docker bridge gateway and also a plausible real router address. Issue #11757, opened by OtherStep on 2026-09-14 and still open, reports the host's own resolved stub listener capturing queries meant for a router on that address. The rules themselves are narrow, allowing only UDP port 53 from 172.16.0.0/12 and 192.168.0.0/16 to that one address, but the collision is real if your LAN uses that subnet.

**Published container ports still need a deliberate rule.** `ufw-docker install` appends a block to `/etc/ufw/after.rules` that filters the `DOCKER-USER` chain, which Docker consults for forwarded traffic. The effect is that `docker run -p 8080:80` is no longer silently exposed. To expose one on purpose, use `ufw route allow` or the `ufw-docker allow` helper against the container's own port, not the host-mapped port.

**Nothing sandboxes applications.** There is no AppArmor, SELinux, firejail, or bubblewrap configuration anywhere in the Omarchy tree, and no fail2ban. SSH brute-force protection is the `ufw limit 22/tcp` rule that `omarchy-setup-security-sshd` adds, nothing more.

**Locally listening services are still listening.** `enable-services.sh` enables cups and avahi-daemon. The firewall keeps them off the network, but they are running, and any change to the default-deny policy exposes them.

## SSH, the one port you are likely to open

`omarchy-setup-security-sshd`, reached via Setup > Security > SSHD, installs openssh, enables sshd, adds `ufw limit 22/tcp`, authorizes a key you paste or pull from GitHub, and then writes `/etc/ssh/sshd_config.d/10-omarchy-hardening.conf` turning password and keyboard-interactive authentication off. It validates with `sshd -t` and `sshd -T` before keeping that file, and refuses to disable passwords if no key is authorized. That hardening shipped in v4.0.2 on 2026-08-31, listed in the release notes under Security. On 4.0.0 and 4.0.1 the same command left password authentication on.

Once enabled, sshd binds all interfaces. Issue #8248, opened by helioryn on 2026-08-25 and still open, argues that a roaming laptop should bind loopback or a management interface instead. Until that changes, scope it yourself with a `ufw allow from` rule or keep SSH on a Tailscale interface only.

## What to watch for on newer versions

The firewall script is byte-identical across v4.0.0 through v4.0.4 and in the quattro-dev branch, so nothing has moved yet. The next release is announced as Quattro RS 4.5. Two open issues touch this file directly, #11560 on the LocalSend scope and #11757 on the Docker DNS address, so re-read `/usr/share/omarchy/install/config/firewall.sh` after upgrading and compare `sudo ufw status verbose` against it. On 3.x the same rules lived in `install/first-run/firewall.sh` and were applied with `ufw --force enable` on first run, so the rule set itself has not changed since 3.x; what changed in 4.x is when it is applied and, on upgraded machines, whether the ufw-docker block was ever written.

## Related

- [Is Omarchy safe?](/security/is-omarchy-safe/)
- [Docker group root escalation](/security/docker-group-root-escalation/)
- [Omarchy manual: Security](https://omarchy.org/manual/security/)
