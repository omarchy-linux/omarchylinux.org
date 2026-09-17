---
title: "cidata drives store the LUKS passphrase in plaintext"
description: "Omarchy's unattended install reads a cidata drive whose config carries the LUKS passphrase in plaintext. The risk, and the defer-provisioning path."
answer: "Omarchy's unattended installer reads a drive labeled cidata. If that config enables encryption, the passphrase sits in plaintext inside user_configuration.json under disk_config.disk_encryption.encryption_password, so the drive image is as sensitive as the disk it unlocks. For imaging rigs, ship an empty defer-provisioning marker instead of credentials: the installer then generates a throwaway passphrase and the first owner re-keys it."
appliesTo:
  from: "4.0.0"
status: by-design
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: medium
reported: "Documented by the project itself in manual chapter 51, Unattended Installs, shipped with v4.0.0 on 2026-08-14"
projectResponse: "The manual states the caveat directly, telling you to \"treat a cidata drive built from an encrypted install as the secret it is\", and offers a defer-provisioning marker so imaging rigs ship no credentials at all."
tags: [unattended-install, cidata, luks, imaging, provisioning]
sources:
  - url: "https://omarchy.org/manual/unattended-installs/"
    title: "Omarchy Manual: Unattended Installs"
    kind: manual
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/airootfs/usr/local/bin/omarchy-cidata-load"
    title: "omarchy-cidata-load: the ISO script that mounts and copies a cidata drive"
    kind: other
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/airootfs/usr/share/omarchy-iso/orchestrator/context.py"
    title: "orchestrator/context.py: generates a throwaway LUKS passphrase for deferred-provisioning installs"
    kind: other
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 release notes: deferred first-boot provisioning"
    kind: release
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/10378"
    title: "Issue #10378: Factory reset retains the previous owner's password hash"
    kind: issue
    author: "AksharP5"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/pull/10379"
    title: "PR #10379: Erase old password hashes during factory reset"
    kind: pr
    author: "AksharP5"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/9384"
    title: "Issue #9384: omarchy-drive-password: \"No encrypted drives available\" due to unprivileged blkid call"
    kind: issue
    author: "LoupiBe"
    date: "2026-08-31"
credits:
  - name: "AksharP5"
    url: "https://github.com/AksharP5"
    for: "Found that a factory reset left the previous owner's password hash in the retained baseline snapshot"
  - name: "LoupiBe"
    url: "https://github.com/LoupiBe"
    for: "Traced the drive encryption password tool failing for unprivileged users to an unprivileged blkid call"
faq:
  - q: "Does the plaintext passphrase end up on the installed disk?"
    a: "The cidata files are copied into /root on the live ISO, which is RAM, not the target disk. The exposure this page covers is the drive image itself and wherever you stored it, such as a Proxmox ISO datastore, a Packer build directory, or a git repository."
  - q: "Can I use unattended install with encryption and no passphrase on the drive?"
    a: "Yes, if you let the installer partition the disk and you use the defer-provisioning marker. The installer then generates its own throwaway passphrase. A rig that pre-encrypts the target itself must still hand the passphrase over in user_credentials.json."
  - q: "Is the disk encrypted during the provisioning window?"
    a: "The volume is a real LUKS2 container, but a deferred-provisioning install embeds the throwaway keyfile in the initramfs so the machine boots unattended. Until the first owner finishes setup, anyone who can boot the machine is inside it."
  - q: "Is the account password on the drive plaintext too?"
    a: "No. user_credentials.json carries a hash you generate with openssl passwd -6. That is still worth protecting, because a hash on a drive image invites offline cracking, but it is not the password itself."
related: [is-omarchy-safe, luks-and-ufw-defaults]
draft: false
---

Omarchy's unattended install works by label. When the ISO boots and finds a second drive labeled `cidata`, the live system mounts it read only, copies the configuration files off it into `/root`, skips the setup wizard, and installs. `cidata` is the cloud-init NoCloud label, which is why Proxmox, libvirt and Packer already know how to attach one.

The security cost is in one file. `user_configuration.json` is an archinstall configuration, and when it turns on full disk encryption it carries the passphrase as a plain string at `disk_config.disk_encryption.encryption_password`. Nothing is hashed, wrapped or sealed. A `cidata.iso` built from an encrypted install unlocks the machine it installed.

The project documents this. Chapter 51 of the manual ends by telling you to "treat a cidata drive built from an encrypted install as the secret it is". That text shipped with v4.0.0 on 2026-08-14 and is byte for byte identical in v4.0.4 and on the current development branch, so nothing has changed about it through the 4.0.x point releases. There is no 3.x equivalent, because unattended installs did not exist before Quattro.

Rated medium here, not high, because it is documented, it requires that you already hold the drive image, and the cidata copy itself lands in the live ISO's RAM rather than on the target disk. It is still the kind of file that quietly ends up in a shared ISO datastore or a build repository.

## The fix

For any rig that images more than one machine, do not put credentials on the drive at all.

1. Copy the configuration file into a build directory and strip the `encryption_password` key out of its `disk_encryption` block. Keep the rest of the block, so the installer still knows to encrypt.

2. Add an empty marker file named `defer-provisioning` in place of `user_credentials.json`, then build the image from the configuration file and the marker only.

```bash
mkdir cidata
cp user_configuration.json cidata/
touch cidata/defer-provisioning
genisoimage -output cidata.iso -volid cidata -joliet -rock cidata/
```

3. Let the installer partition the disk itself. Do not pre-encrypt the target on the rig. A pre-encrypted target is the one case where the installer still demands a passphrase in `user_credentials.json`, which puts the plaintext straight back on the drive.

4. Build the image somewhere that is not persisted. A tmpfs directory works, and so does deleting the image after you attach it.

```bash
mkdir -p /dev/shm/cidata-build
```

5. Attach the image, install, then remove the image from your ISO storage rather than leaving it next to `omarchy.iso`.

With the marker in place the installer creates no user. When the machine first boots, the owner picks a keyboard layout, creates their account and sets their own password. On an encrypted disk, that first boot also re-keys LUKS from the installer's throwaway passphrase to the owner's password.

## Verify it worked

On the rig, before you ship the image, check that no passphrase is in the file.

```bash
grep -o 'encryption_password' cidata/user_configuration.json
ls cidata/
```

The first command should print nothing. The listing should show `user_configuration.json` and `defer-provisioning`, and no `user_credentials.json`.

On an installed machine, after the first owner has finished setup, confirm the throwaway key is gone.

```bash
sudo ls /etc/omarchy/provisioning.key /var/lib/omarchy/provisioning/luks-key
sudo cryptsetup luksDump /dev/nvme0n1p2 | grep -c 'luks2'
grep -o 'cryptkey=[^ ]*' /proc/cmdline
```

The first command should report both paths missing. The slot count should be 1. The last command should print nothing. If `cryptkey=rootfs:/etc/omarchy/provisioning.key` is still on the kernel command line, the machine is still auto-unlocking and provisioning has not completed.

## Why it happens

Unattended install was built to reuse the wizard's own output. The files on a cidata drive are exactly what an interactive install writes into `/root`, which is why the manual tells you to run one interactive install and copy the results. That design keeps one code path instead of two, but it also means the format is archinstall's format, and archinstall's configuration schema stores the encryption password as a string.

The deferred path exists precisely because of this. Passing an empty `defer-provisioning` marker tells the orchestrator to discard account material and, on an encrypted target with no passphrase supplied, to generate a random throwaway passphrase on the installing machine. That passphrase is written to `/var/lib/omarchy/provisioning/luks-key` and `/etc/omarchy/provisioning.key`, both root only, and added to the initramfs with a `cryptkey=rootfs:` kernel parameter so the machine can reboot unattended.

That is the trade-off you are accepting. Between the install finishing and the owner completing first boot, the disk unlocks itself. The volume is encrypted at rest against someone who pulls the drive, but not against someone who powers the machine on. Keep that window short and keep the machines physically controlled until they are handed over.

First boot closes it. The provisioning step adds the owner's password as a new LUKS slot, rebuilds the boot image without the embedded keyfile, kills every other slot including the throwaway one, and then shreds the staged key. The v4.0.0 release notes describe this as all or nothing, and the code matches: if the boot image rebuild fails, auto-unlock is restored so the attempt can be retried rather than leaving a disk nobody can open.

## If that did not work

If you must ship a passphrase on the drive, because the rig pre-encrypts the target or because you are producing a single machine rather than a fleet, treat it as a per-machine throwaway and rotate it after the machine is in the owner's hands.

```bash
sudo /usr/share/omarchy/bin/omarchy-drive-password
```

Run it with `sudo`. As of v4.0.4, `omarchy drive password` and the Drive Encryption menu entry report "No encrypted drives available" for an unprivileged user, because the tool probes with `blkid`, which needs root to read raw device headers. That is issue #9384, reported by LoupiBe on 2026-08-31 and still open. If you would rather not depend on the wrapper, `sudo cryptsetup luksChangeKey` on the LUKS partition does the same job.

One more thing to sweep if you image machines. Every install from the Quattro ISO keeps a `@factory` baseline snapshot for later resets. The installer scrubs provisioning credentials out of that baseline, including the staged LUKS key, the keyfile, the boot drop-ins, any `authorized_keys` and any Tailscale auth key. Account password hashes were another matter: the reset's own cleanup locked root with `passwd --lock`, which prefixes the hash with `!` rather than erasing it, and left the `shadow-` backup file behind. Akshar Patel reported that in issue #10378 on 2026-09-05, the omarchybot collaborator account confirmed it by mounting a real baseline, and the fix in PR #10379 was merged on 2026-09-16. That is after v4.0.4 shipped on 2026-09-15, so on v4.0.4 a machine you factory reset still carries the previous owner's hashes in the retained snapshot.

## What to watch for on newer versions

Two things to recheck when the next release lands. First, whether chapter 51 still describes the same file set, since the caveat text has not moved since 4.0.0 and any change to it signals a change in behaviour. Second, whether the factory reset hash scrub from PR #10379 has shipped, which would let you drop the extra sweep above. Check [the release notes](/releases/) before you rebuild a golden image.

## Related

- [Is Omarchy safe to run?](/security/is-omarchy-safe/)
- [LUKS and ufw defaults](/security/luks-and-ufw-defaults/)
- [Omarchy in Proxmox, QEMU and KVM](/run/proxmox-qemu-kvm/)
- [Unattended install with a cidata drive](/run/unattended-install-cidata/)
