---
title: "Creating a snapshot failed."
description: "Creating a snapshot failed during omarchy update. Fix the snapper error: an active swapfile on root, /.snapshots not a subvolume, or a missing snapper config."
answer: "Read the real snapper error first, then fix the cause. The usual one is an active swapfile on the root subvolume: run swapon --show and sudo swapoff /swapfile, then retry. Other causes are /.snapshots existing as a plain directory, no snapper config at all, or a non-Btrfs root. On 4.x the update continues without a snapshot; on 3.x it aborted."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 68
errorStrings:
  - "Creating a snapshot failed."
  - "Creating snapshot failed."
  - "IO Error (.snapshots is not a btrfs subvolume)."
  - "IO Error (query default id failed, subvolume is not a btrfs subvolume)."
  - "No Snapper configs found, so no snapshot was created."
  - "Continuing the update without a snapshot."
tags: [snapper, btrfs, update, snapshots, limine, swapfile]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/3168"
    title: "Discussion #3168: Creating snapshot failed"
    kind: discussion
    author: "abbaty48"
    date: "2025-11-04"
  - url: "https://github.com/omacom/omarchy/issues/11100"
    title: "Issue #11100: omarchy-snapshot: handle non-subvolume /.snapshots with clear diagnostic and recovery instructions"
    kind: issue
    author: "patsonatorEFPL"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10421"
    title: "Issue #10421: omarchy-snapshot: a failed sudo is reported as \"No Snapper configs found\", and the suggested fix overwrites a working /etc/snapper/configs/root"
    kind: issue
    author: "ericziko"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/6683"
    title: "Issue #6683: snapper.sh installs a btrfs snapper config on non-btrfs roots, so snapper-cleanup fails daily"
    kind: issue
    author: "tpatzelt"
    date: "2026-08-10"
  - url: "https://github.com/omacom/omarchy/issues/6629"
    title: "Issue #6629: limine-snapper-sync inactive due to missing inotify-tools dependency & missing Snapper root configuration"
    kind: issue
    author: "mikemayuare"
    date: "2026-08-08"
  - url: "https://github.com/omacom/omarchy/issues/9619"
    title: "Issue #9619: snapper.sh overwrites /etc/conf.d/snapper, silently de-registering user configs (home)"
    kind: issue
    author: "CaptainVirgil"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/3055"
    title: "Issue #3055: /.snapshots takes up all my space"
    kind: issue
    author: "derluke"
    date: "2025-11-01"
  - url: "https://github.com/omacom/omarchy/pull/6354"
    title: "PR #6354: Fix locate index on Btrfs: skip snapshots, index /home, drain leaked timeline snapshots"
    kind: pr
    author: "yuters"
    date: "2026-07-23"
  - url: "https://github.com/omacom/omarchy/issues/3543"
    title: "Issue #3543: install fails on omarchy 3.2 with limine-snapper script expecting /boot/limine/limine.conf"
    kind: issue
    author: "ZarK"
    date: "2025-11-22"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 release notes"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
credits:
  - name: "davemaier"
    url: "https://github.com/davemaier"
    for: "found the active swapfile in the snapper logs and confirmed swapoff fixes it"
  - name: "jacksenechal"
    url: "https://github.com/jacksenechal"
    for: "wrote the steps to move the swapfile onto its own Btrfs subvolume"
  - name: "takiido"
    url: "https://github.com/takiido"
    for: "pointed out that .snapshots must be a real subvolume, not a plain directory"
  - name: "tpatzelt"
    url: "https://github.com/tpatzelt"
    for: "traced the phantom root config that breaks snapshots on non-Btrfs roots"
  - name: "ericziko"
    url: "https://github.com/ericziko"
    for: "showed that a failed sudo is misreported as a missing snapper config"
  - name: "fresh3nough"
    url: "https://github.com/fresh3nough"
    for: "opened PR #10428, still unmerged, to tell a failed sudo apart from a missing config"
faq:
  - q: "Does a failed snapshot stop the update?"
    a: "On Omarchy 4.0.0 and later, no. The updater prints \"Continuing the update without a snapshot.\" and carries on. On 3.x a non-127 failure tripped the error trap and aborted the run."
  - q: "Can I update without any snapshot at all?"
    a: "Yes. If snapper is not installed, omarchy-snapshot exits 127 and the updater stays quiet. You simply lose the Limine rollback entry for that update, so take your own backup first."
  - q: "Why does snapper refuse when a swapfile is active?"
    a: "Btrfs will not snapshot a subvolume that holds an active swapfile. Omarchy's own omarchy-hibernation-setup puts its swapfile on a separate /swap subvolume, which keeps it out of the root snapshot. Hand made swapfiles at /swapfile sit on root and block it."
related: [omarchy-update-fails-or-hangs, migration-failed-mid-update, kernel-panic-after-update-limine]
draft: false
---

Omarchy takes a Btrfs snapshot before every update so you can roll back from the Limine boot menu. When that step fails you see a snapper error, and on older releases the whole update stopped there. This page covers Omarchy 3.x through 4.0.4.

## The fix

**1. Get the real error.** The line you saw is snapper's generic failure message (its source string is "Creating snapshot failed."), and the specific cause is printed next to it. Run the snapshot by hand:

```bash
omarchy-snapshot create
```

If the update itself failed, the full session is logged at `/tmp/omarchy-update.log`. Background failures show up in `journalctl -u snapper-cleanup.service -u limine-snapper-sync.service -b`.

**2. If a swapfile sits on the root subvolume.** This is the most common cause. Btrfs refuses to snapshot a subvolume that holds an active swapfile. Check:

```bash
swapon --show
```

If you see a file such as `/swapfile` (as opposed to `/dev/zram0` or `/swap/swapfile`), turn it off and retry:

```bash
sudo swapoff /swapfile
omarchy-snapshot create
```

That is the quick unblock. To keep swap and keep snapshots, move the swapfile onto its own top level subvolume. Omarchy's own `omarchy-hibernation-setup` (present in 3.8.4 and 4.x) creates a `/swap` subvolume, marks it NOCOW, and puts a RAM sized swapfile there, but it also adds the resume hook and kernel parameters for hibernation. If you want swap without hibernation, jacksenechal posted the manual version in discussion #3168: `swapoff`, delete `/swapfile`, drop its `/etc/fstab` line, mount `subvolid=5`, `btrfs subvolume create @swap`, mount it at `/swap`, then `sudo btrfs filesystem mkswapfile --size 16g /swap/swapfile` and add the new fstab entry.

**3. If the error says `.snapshots is not a btrfs subvolume`.** This happens after restoring a system from rsync, tar, or a clone, where `/.snapshots` comes back as a plain directory. Reported as issue #11100 on 4.0.3, still open. Confirm first:

```bash
sudo btrfs subvolume show /.snapshots
```

If that fails and the directory is empty, replace it:

```bash
sudo rmdir /.snapshots
sudo btrfs subvolume create /.snapshots
sudo chmod 750 /.snapshots
omarchy-snapshot create
```

Do not `rm -rf` a `/.snapshots` that still holds real snapshots. Check `sudo snapper -c root list` first.

**4. If you get `No Snapper configs found, so no snapshot was created.`** This message is 4.x only. Before you act on it, check that sudo actually worked. Issue #10421 showed that a `sudo` failure inside the config lookup produces the same message, and the suggested repair then overwrites a config that was fine. Run `sudo -v` first, then:

```bash
sudo snapper list-configs
```

If that really is empty, create the config:

```bash
sudo snapper -c root create-config /
sudo bash -euo pipefail /usr/share/omarchy/install/config/snapper.sh
```

The second command installs Omarchy's retention template (five snapshots, no timeline), enables `snapper-cleanup.timer` and `limine-snapper-sync.service`. Caution from issue #9619: it rewrites `/etc/conf.d/snapper` to `SNAPPER_CONFIGS="root"`, which de-registers any extra config you added, such as `home`. Copy that file aside first and put your config names back afterwards.

**5. If your root is not Btrfs.** Issue #6683 covers this. `install/config/snapper.sh` writes a config with `FSTYPE="btrfs"` regardless of the real filesystem, so on ext4 you get a phantom `root` config, a daily failing `snapper-cleanup.service`, and a failing pre-update snapshot. Check with `findmnt / -o TARGET,SOURCE,FSTYPE`. If it is not btrfs, remove the config and stop the timers:

```bash
sudo snapper -c root delete-config 2>/dev/null || sudo rm -f /etc/snapper/configs/root
sudo systemctl disable --now snapper-cleanup.timer limine-snapper-sync.service
```

Snapshots are not available on a non-Btrfs root. Updates still work, and 4.x will say it continued without one.

## Verify it worked

```bash
sudo snapper -c root create -c number -d "verify"
sudo snapper -c root list | tail -5
systemctl status snapper-cleanup.timer limine-snapper-sync.service
```

You should see your new snapshot numbered at the bottom of the list, both units healthy, and then `omarchy-snapshot create` finishing with "Snapshots can be selected during boot." (4.x wording; 3.x prints nothing after the green header). Reboot once and confirm the dated entries appear under Snapshots in the Limine menu. Delete the test snapshot with `sudo snapper -c root delete <number>`.

## Why it happens

`omarchy-snapshot create` asks snapper for its list of configs, then loops over them running `snapper -c <config> create -c number` followed by `cleanup number`. Anything that makes one of those calls fail takes the whole step down. That includes an active swapfile pinning the root subvolume, a `/.snapshots` path that is not a subvolume, a config that names a filesystem the machine does not have, and a sudo prompt that cannot be answered.

The version difference matters. On 3.x the updater ran `omarchy-snapshot create || (($? == 127))` under `set -e`, so any failure other than "snapper is not installed" tripped the error trap and you got "Something went wrong during the update!" with nothing updated. Omarchy 4.0.0 changed this with PR #6580 by nille, merged 2026-08-07: a failed snapshot now prints "Continuing the update without a snapshot." and the update proceeds, and a snapper with no configs fails loudly instead of printing a green header over nothing. That is friendlier but easy to miss in the scroll, so an install can keep updating with no working rollback.

Disk pressure is the other family of reports. Machines set up before the snapper config was normalized in June 2026 took hourly timeline snapshots. Later configs stopped creating new ones but never removed the old ones, and snapper's number cleanup ignores anything tagged `Cleanup=timeline`, so the pile only grew. PR #6354 measured one machine at 592 leaked snapshots pinning 219 GB. Omarchy 4.x ships a migration that drains snapshots marked `Cleanup=timeline` in batches of 20, but only when your config has `TIMELINE_CREATE="no"`. If the disk is full, snapper fails too. Note that 4.x refuses to start an update with less than 10 GiB free on `/`.

## If that did not work

Check `sudo btrfs filesystem du -s --human-readable /.snapshots` for what the snapshots actually cost, and `sudo snapper list -a` for stragglers. Old `@home/.snapshots/<n>/snapshot` subvolumes can survive a snapper delete and need `sudo btrfs subvolume delete` by hand.

If `limine-snapper-sync.service` goes inactive right after boot, issue #6629, filed on 3.8.4, reports the watcher needs `inotify-tools`, which that release did not install. The 4.x base package list includes it, so this should only bite older installs: `sudo pacman -S inotify-tools` then restart the unit.

If this started at install time rather than at update time, you are probably looking at issue #3543 instead: on a hand built Arch install, the Omarchy limine-snapper install step bails with "Error: Limine config not found", leaving snapper unconfigured. The original report had `limine.conf` in a path the script did not check; later commenters hit it because `/boot` was mounted with `fmask=0077`, so the config on the ESP was unreadable as a normal user. They worked around it by setting `fmask=0022,dmask=0022` on the `/boot` line in `/etc/fstab` and remounting, or by adding sudo to the checks, then re-running `install/login/limine-snapper.sh`.

Evidence for the rest is thin. Several of these reports are still open against 4.0.x with no merged fix, so treat the steps above as workarounds rather than a repaired upstream. If the snapshot step keeps failing, you can still update: take your own backup, run the update, and read [what migrations do](/upgrade/what-migrations-do/) so you know what changed.

## Related

- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Rollback with snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Hibernate fails or hangs](/fix/hibernate-fails-or-hangs/)
- [Kernel panic after update](/fix/kernel-panic-after-update-limine/)
- Omarchy manual: [System snapshots](https://omarchy.org/manual/system-snapshots/)
