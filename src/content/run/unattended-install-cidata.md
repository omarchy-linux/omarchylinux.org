---
title: "Unattended Omarchy installs with a cloud-init cidata drive"
description: "Build a NoCloud cidata drive so the Omarchy 4 ISO installs itself: the exact file set, genisoimage and Proxmox commands, SSH keys, and the passphrase risk."
answer: "Attach a second drive labeled cidata next to the Omarchy 4 ISO. Put user_configuration.json and user_credentials.json on it, plus optional authorized_keys, tailscale_authkey and defer-provisioning. The installer copies them into /root, skips the wizard and reboots into the finished system. Build the drive with genisoimage -volid cidata. Encrypted installs still need someone to type the LUKS passphrase at first boot."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Unattended (cidata)"
hostVersion: "Any host that can attach a second drive"
tags: [cidata, unattended, cloud-init, proxmox, iso, provisioning]
sources:
  - url: "https://omarchy.org/manual/unattended-installs/"
    title: "Omarchy manual, chapter 51: Unattended Installs"
    kind: manual
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/airootfs/usr/local/bin/omarchy-cidata-load"
    title: "omarchy-cidata-load: the live ISO script that finds and loads the cidata drive"
    kind: other
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/airootfs/usr/share/omarchy-iso/orchestrator/phases_impl.py"
    title: "orchestrator/phases_impl.py: the SSH, Tailscale and factory-snapshot phases of the installer"
    kind: other
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/README.md"
    title: "omarchy-iso README: Autoinstall section"
    kind: docs
  - url: "https://github.com/omacom/omarchy-iso/pull/155"
    title: "PR #155: Generate cidata configs with omarchy-iso-configurator"
    kind: pr
    author: "gosuwachu"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy-iso/pull/154"
    title: "PR #154: Support unattended installs in omarchy-iso-boot"
    kind: pr
    author: "gosuwachu"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy-iso/pull/153"
    title: "PR #153: Fix omarchy-vm boot helper path"
    kind: pr
    author: "gosuwachu"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy-iso/pull/180"
    title: "PR #180: cidata: keep probing for the drive for a bounded time"
    kind: pr
    author: "tbvl"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy-iso/pull/181"
    title: "PR #181: Skip the offline-mirror prefetch on an autoinstall"
    kind: pr
    author: "tbvl"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/pull/11530"
    title: "PR #11530: Explain how to do an unattended install from one USB stick"
    kind: pr
    author: "tbvl"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy-iso/pull/129"
    title: "PR #129: Boot and install Omarchy on Snapdragon X ARM64 systems"
    kind: pr
    author: "birkskyum"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
credits:
  - name: "gosuwachu"
    url: "https://github.com/gosuwachu"
    for: "Proposed generating cidata files from the configurator and booting them from the VM helper"
  - name: "tbvl"
    url: "https://github.com/tbvl"
    for: "Reported that a second USB stick can enumerate too late for the cidata probe on real hardware, and proposed the boot-stick partition layout"
faq:
  - q: "Do I need a special ISO build for an unattended install?"
    a: "No. The shipped Omarchy ISO looks for a drive labeled cidata on every boot. With no such drive attached, the normal wizard runs and nothing changes."
  - q: "Can I do an unattended encrypted install?"
    a: "Partly. The install itself runs unattended, but the LUKS passphrase prompt at the first boot still needs a person. The passphrase also sits in plain text on the cidata drive, so treat that drive as a secret."
  - q: "How do I build a drive that carries no credentials at all?"
    a: "Put an empty file named defer-provisioning on the drive instead of user_credentials.json. The install then creates no account; the first person to boot the machine chooses a keyboard layout and becomes the owner."
  - q: "Does the cidata drive have to be an ISO image?"
    a: "No. Any filesystem the live environment can mount works, as long as the volume label is cidata or CIDATA. A small FAT image made with mkfs.vfat -n CIDATA is equally fine."
related: [proxmox-qemu-kvm, what-breaks-in-a-vm]
draft: false
---

Every boot of the Omarchy ISO starts with a look for a second drive labeled `cidata`. When one is there and carries the right files, the installer copies them into `/root`, skips the setup wizard, installs, and reboots into the finished system. There is no separate ISO build for this, no extra boot menu entry and no kernel parameter to pass. Without such a drive, the same ISO runs the normal wizard.

The label is the one cloud-init uses for its `NoCloud` data source, so the tooling people already use for cloud-init seeds (Proxmox, libvirt, Packer) attaches it without any special handling.

Checked against Omarchy v4.0.4 and the `omarchy-iso` repository as of 2026-09-16. This is a 4.x feature. The first autoinstall commit landed in `omarchy-iso` on 2026-07-28; the standalone loader, `authorized_keys`, `tailscale_authkey` and `defer-provisioning` followed between 4 and 9 August, all before Omarchy 4.0.0 shipped on 2026-08-14. There is nothing equivalent to set up on 3.8.4 or earlier. The manual chapter is identical in 4.0.0 through 4.0.4 and the current development branch, and the loader script has not changed since 2026-08-09.

## The file set

The installer's own wizard writes exactly these files, so the quickest way to a working set is one interactive install in a VM followed by copying whatever it left behind in `/root`.

| File | Required | What it carries |
|------|----------|-----------------|
| `user_configuration.json` | Yes | The archinstall config: disk, hostname, timezone, keyboard, and the `disk_encryption` block when encryption is on |
| `user_credentials.json` | Yes, or `defer-provisioning` | Username and password hash |
| `defer-provisioning` | Stands in for the credentials file | Empty marker. Installs with no user, first boot creates the owner |
| `user_full_name.txt` | No | Git full name |
| `user_email_address.txt` | No | Git email |
| `user_encrypt_installation.txt` | No | `true` when the configuration carries a `disk_encryption` block |
| `authorized_keys` | No | SSH public keys in sshd's own format, one per line |
| `tailscale_authkey` | No | A single Tailscale auth key |

The loader treats `user_configuration.json` plus one of `user_credentials.json` or `defer-provisioning` as the mandatory pair. Anything less and it decides this is not an autoinstall drive at all, and the wizard runs as usual. That failure is silent by design, which is worth remembering when a machine you expected to install itself is sitting at the keyboard prompt.

Generate the password hash with:

```bash
openssl passwd -6 "yourpassword"
```

Put the result in the `enc_password` field for the user, and in `root_enc_password`, inside `user_credentials.json`.

## Build the drive

Any filesystem works as long as the label is right. The loader looks for both `cidata` and `CIDATA` under `/dev/disk/by-label`, so either spelling is fine. The manual's recipe is a small ISO:

```bash
mkdir cidata
cp user_configuration.json user_credentials.json authorized_keys cidata/
genisoimage -output cidata.iso -volid cidata -joliet -rock cidata/
```

A FAT image works just as well if your tooling prefers one. PR #154 packages the files that way, and the single-stick layout described further down was verified on hardware with a FAT32 partition. Create the image, then copy the same files into it with `mcopy` from mtools:

```bash
truncate -s 8M cidata.img
mkfs.vfat -n CIDATA cidata.img
mcopy -i cidata.img user_configuration.json user_credentials.json authorized_keys ::
```

## Attach it in Proxmox

This is the manual's own example, reproduced because the flags matter:

```bash
qm create 101 --name my-omarchy \
  --bios ovmf --machine q35 --cpu host --cores 4 --memory 8192 \
  --ostype l26 --scsihw virtio-scsi-single \
  --efidisk0 local-lvm:0,efitype=4m,pre-enrolled-keys=0 \
  --scsi0 local-lvm:40,discard=on,iothread=1 \
  --net0 virtio,bridge=vmbr0 --vga virtio --serial0 socket \
  --ide2 local:iso/omarchy.iso,media=cdrom \
  --ide3 local:iso/cidata.iso,media=cdrom \
  --boot order='scsi0;ide2'

qm start 101
```

Putting `scsi0` ahead of the ISO in the boot order is deliberate. A blank disk cannot boot, so the first start lands on the ISO; once the install has written the disk, every later start boots from it, and you never have to detach the ISO by hand.

Download the ISO from [omarchy.org](https://omarchy.org) and check it against the published `.sha256` and `.sig` files first. See [verifying a download](/verify/).

## SSH and Tailscale

Out of the box, Omarchy installs openssh but leaves the service disabled, and ufw rejects incoming connections by default. An unattended machine built that way has no way in. When `authorized_keys` is present, the install fixes all three parts: it writes the keys to the user's `~/.ssh/authorized_keys` with mode 600 inside a 700 directory, chowns them to the user, enables `sshd.service`, and runs `ufw allow ssh` in the chroot. ufw cannot talk to netfilter from inside a chroot, so the installer checks that the port 22 rule was recorded in the target's `/etc/ufw/user.rules`, which is what `ufw.service` loads on first boot. Nothing else about sshd's authentication settings is changed. A keys file with no usable key stops the install rather than producing an unreachable machine.

On a deferred-provisioning install there is no user yet, so the keys are staged under `/var/lib/omarchy/provisioning/` and `omarchy-provision-owner` installs them once first boot creates the owner.

When `tailscale_authkey` is present, the `tailscale` package is added from the ISO's bundled mirror, the key is written to `/etc/tailscale/authkey` (root only), `tailscaled` is enabled, ufw gets an allow rule for `tailscale0`, and an `omarchy-tailscale-join.service` unit retries `tailscale up` every 15 seconds after boot until the join succeeds, then deletes the key and disables itself. A reusable, pre-authorized key lets one drive image cover a whole batch of machines; an ephemeral key suits throwaway VMs.

The installer also takes a read-only factory snapshot at the end of every install, and it strips the staged provisioning keys, the Tailscale auth key and the join unit out of that snapshot before sealing it. A later factory reset additionally deletes every regular user account and home directory, so a reset years later neither hands the next owner your SSH keys nor rejoins your tailnet.

## Verify it worked

On the console, a successful load prints a line saying autoinstall configuration was found on the cidata drive and the configurator is being skipped. The install dashboard then comes up with no questions.

After the reboot, check that the pieces you asked for actually landed:

```bash
systemctl is-enabled sshd.service
sudo ufw status | grep 22
hostnamectl hostname
tailscale status
```

If you only wanted to test the drive itself, boot the ISO in a throwaway VM and look at `/var/log/omarchy-install.log`.

## The plaintext passphrase problem

This is the one thing to get right before you put a cidata drive anywhere shared. When you build the files from an encrypted install, the LUKS passphrase is written in clear text in two places: the `encryption_password` field inside the `disk_encryption` block of `user_configuration.json`, and an `encryption_password` field in `user_credentials.json`. Neither is hashed. The user password is hashed, the disk passphrase is not, because the installer has to hand the real string to cryptsetup.

So a cidata ISO built from an encrypted install is the disk passphrase. Do not commit it, do not park it in a Proxmox ISO store that your whole team browses, and do not bake it into a Packer artifact you push to a registry. Build it, use it, delete it, and re-key the volume if it ever leaves your hands.

An encrypted unattended install is also only unattended up to the first reboot. Nothing unlocks the root volume before the system comes up, so a person has to type the passphrase once. For a genuinely hands-off fleet, install unencrypted or use deferred provisioning. More on the trade-off in [unattended install plaintext passphrase](/security/unattended-install-plaintext-passphrase/).

## If the installer showed the wizard anyway

Work through these in order.

1. Check the label, not the filename. `genisoimage -volid cidata` sets it. `lsblk -o NAME,LABEL` inside the live environment tells you what the kernel actually saw.
2. Check the mandatory pair. `user_configuration.json` on its own is not enough, and a typo in the filename `user_credentials.json` means the loader falls straight through.
3. Check the JSON parses. The loader copies the files blind; the orchestrator parses them and stops on a parse error.
4. On physical hardware booting from two USB sticks, suspect enumeration timing. The loader waits for the udev queue to drain and then checks for the label a single time, and a stick the kernel has not discovered yet is not in that queue. One tester hit exactly this on an Intel MacBook Pro 16,2 with the 4.0.3 ISO: the wizard appeared, yet running `omarchy-cidata-load` from a second console a moment later found the drive, and rerunning the install script completed the unattended install. The tester opened a draft pull request adding a bounded wait (PR #180) and closed it the same day in favour of a layout that has nothing to wait for: put the cidata filesystem on the boot stick itself, as a partition after the ISO image, because a stick that just booted is by definition already enumerated. That advice is proposed as a manual addition in [omacom/omarchy PR #11530](https://github.com/omacom/omarchy/pull/11530), still an open draft as of 2026-09-16, where the author reports a successful unattended install from a single stick carrying the 4.0.3 image plus a FAT32 `CIDATA` partition. Neither change is in 4.0.4, so on bare metal the boot-stick-partition layout is the more reliable arrangement today, and it is one tester's report rather than a documented path.

A separate theory, that the ISO's offline mirror prefetch slows autoinstalls down by racing the installer on the same stick, was proposed in PR #181 and withdrawn the next day when an ISO built from the branch showed the same long stay on the splash screen. Treat slow autoinstall boots on USB as unexplained for now.

## What to watch for on newer versions

Two pieces of tooling are in flight in `omacom/omarchy-iso` and neither has merged as of 2026-09-16. Note that both live in the ISO repository, not in `omacom/omarchy` itself.

[PR #155](https://github.com/omacom/omarchy-iso/pull/155) adds an `--output-dir` flag to `omarchy-iso-configurator`, so you can generate a reusable cidata file set from the existing interactive configurator instead of installing once and copying `/root` by hand. It targets the standard 40 GiB virtual disk rather than asking you to pick a host disk, stages files before publishing them, and uses private permissions. It is open and has one approving review.

[PR #154](https://github.com/omacom/omarchy-iso/pull/154) is the matching half: a `--cidata-dir` flag for `omarchy-iso-boot` that packages the configurator's files into a FAT image, attaches it to QEMU, creates or reuses a dedicated VM SSH identity, injects its public key, and prints ready-to-use SSH and SCP commands. Together they turn the manual recipe on this page into two flags. Both are from the same author; #154 depends on a small path fix in [PR #153](https://github.com/omacom/omarchy-iso/pull/153), which is also still open.

On ARM, [PR #129](https://github.com/omacom/omarchy-iso/pull/129) merged on 2026-09-13 and adds Snapdragon X and generic AArch64 ISO builds. It is ISO build and hardware work, not cidata work, and the autoinstall path is architecture independent, so a cidata drive should behave the same there. The PR's reported testing covered live boots and installs on physical Snapdragon laptops, not unattended installs, and as of 2026-09-16 omarchy.org still offers a single ISO download with no ARM variant. Treat unattended ARM installs as untested.

## Related

- [Omarchy manual, chapter 51: Unattended Installs](https://omarchy.org/manual/unattended-installs/)
- [Proxmox, QEMU and KVM](/run/proxmox-qemu-kvm/)
- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [LUKS and ufw defaults](/security/luks-and-ufw-defaults/)
- [Verifying your download](/verify/)
