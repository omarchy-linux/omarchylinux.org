---
title: "Roll back a bad Omarchy update with snapper and Limine"
description: "How to roll back a bad Omarchy update using Btrfs snapshots, snapper and the Limine boot menu, plus what a snapshot restore does not cover."
answer: "Reboot, pick the dated snapshot from Limine's Snapshots submenu, then run `sudo omarchy-snapshot restore` and reboot again. Omarchy takes a numbered snapper snapshot of the root subvolume before every update and keeps five. A rollback restores root only. Your /home, your ~/.config and the EFI partition are untouched, so config format changes still need sorting out by hand."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [snapper, btrfs, limine, rollback, snapshots, update]
sources:
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/8047"
    title: "Issue #8047: btrfs-overlayfs is enabled by default, which makes snapshot rollback impossible: limine-snapper-sync refuses to start inside every snapshot boot"
    kind: issue
    author: "Cloud-Ops-Dev"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/10421"
    title: "Issue #10421: omarchy-snapshot: a failed sudo is reported as \"No Snapper configs found\", and the suggested fix overwrites a working /etc/snapper/configs/root"
    kind: issue
    author: "ericziko"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/11100"
    title: "Issue #11100: omarchy-snapshot: handle non-subvolume /.snapshots with clear diagnostic and recovery instructions"
    kind: issue
    author: "patsonatorEFPL"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/9097"
    title: "Issue #9097: omarchy-snapshot create fails with - IO Error (subvolume is not a btrfs subvolume)"
    kind: issue
    author: "rofoto"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/9619"
    title: "Issue #9619: snapper.sh overwrites /etc/conf.d/snapper, silently de-registering user configs (home) so omarchy-snapshot stops covering /home"
    kind: issue
    author: "CaptainVirgil"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/6456"
    title: "Issue #6456: omarchy update fails at snapshot step when a swapfile is active on the btrfs root subvolume"
    kind: issue
    author: "markbus-ai"
    date: "2026-07-31"
  - url: "https://github.com/omacom/omarchy/issues/6629"
    title: "Issue #6629: [Bug]: limine-snapper-sync inactive due to missing inotify-tools dependency & missing Snapper root configuration"
    kind: issue
    author: "mikemayuare"
    date: "2026-08-08"
  - url: "https://github.com/omacom/omarchy/issues/5916"
    title: "Issue #5916: Configs broken after reverting to pre-update Snapshot"
    kind: issue
    author: "Varantha"
    date: "2026-05-20"
  - url: "https://github.com/omacom/omarchy/issues/5361"
    title: "Issue #5361: /home being restored while using omarchy-snapshot restore"
    kind: issue
    author: "varungarg6756"
    date: "2026-04-19"
credits:
  - name: "Cloud-Ops-Dev"
    url: "https://github.com/Cloud-Ops-Dev"
    for: "Traced the btrfs-overlayfs conflict that can stop limine-snapper-restore inside a snapshot boot"
  - name: "ericziko"
    url: "https://github.com/ericziko"
    for: "Showed that a failed sudo is misreported as a missing snapper config"
faq:
  - q: "Does rolling back also restore my home directory?"
    a: "Not on the standard Omarchy layout, where /home is its own Btrfs subvolume (@home) and sits outside the root snapshot. Issue #5361 reports a restore on 3.5.1 that did bring /home back, and nobody in the thread explained why. A /home that sits inside the root subvolume would behave that way, so check with findmnt -no SOURCE /home if you are unsure."
  - q: "How many snapshots does Omarchy keep?"
    a: "Five. The shipped snapper template sets NUMBER_LIMIT and NUMBER_LIMIT_IMPORTANT to 5 with timeline snapshots off, and the Limine drop-in allows six entries so a freshly created snapshot is not rejected before cleanup runs."
  - q: "Can I roll back if I use GRUB or systemd-boot?"
    a: "No. The manual is explicit that snapshot booting is a Limine feature, and Limine has been the default since Omarchy 2.0. On GRUB or systemd-boot the snapshots may still exist but nothing puts them in your boot menu."
  - q: "Why is there no snapshot from before my last update?"
    a: "The update continues without one if snapper fails, printing a warning rather than stopping. Common causes are an active swapfile on the root subvolume, a /.snapshots path that is a plain directory, or snapper having no root config at all, which issue #6629 reports on a fresh install."
related: [3-to-4-quattro, before-you-update-checklist, what-migrations-do]
draft: false
---

Checked against Omarchy 4.0.4 (2026-09-15) and the v4.0.4 source tree.

Omarchy snapshots the root Btrfs subvolume with snapper before every update, and `limine-snapper-sync` publishes those snapshots as entries in the Limine boot menu. That is your rollback. It covers the system, not your files.

## The fix

1. Reboot. If the machine goes straight to the LUKS passphrase prompt, you have direct boot enabled, so interrupt the firmware and pick Limine from your BIOS boot menu first.
2. In Limine, open the Snapshots submenu and pick the entry from before the update. Each entry carries a date, and the Omarchy version recorded at snapshot time shows in the bottom left corner. That version string is the snapshot description, because `omarchy-snapshot` labels each snapshot with the output of `omarchy-version`.
3. Boot it and log in. The manual describes a notification that offers to restore for you. Do not wait for it on 4.x: Omarchy 4 ships an autostart override that hides `limine-snapper-notify`, and a migration disables any copy an upgraded machine already had.
4. Run the restore from a terminal:

```bash
sudo omarchy-snapshot restore
```

That is a thin wrapper. Under the hood it runs `sudo limine-snapper-restore`, which is deliberately hidden from the app launcher.

5. Reboot into the restored system.

If you only want a snapshot before doing something risky, that is the same tool:

```bash
omarchy snapshot create
```

## Verify it worked

After the reboot, confirm you are on real Btrfs and not still inside a snapshot boot, and confirm the version:

```bash
findmnt -no FSTYPE,SOURCE /
omarchy-version
sudo snapper -c root list
```

`findmnt` should report `btrfs`, and the source should not contain a `/snapshot` path component. `omarchy-version` reads the installed `omarchy` package version from pacman, so on a restored root it should report the older release you rolled back to. `snapper -c root list` shows the snapshots that survived, with the version string in the description column.

## Why it happens

The pieces are ordinary Arch parts wired together by Omarchy.

`omarchy-update` calls `omarchy-snapshot create` as one of its first steps, before any package is touched, and right after the package cache prune. The comment in the script explains the ordering: the cache lives on the subvolume about to be snapshotted, so pruning afterwards would free nothing until the snapshot ages out.

`omarchy-snapshot create` lists every registered snapper config and, for each one, runs `snapper -c <config> create -c number -d <version>` followed by `snapper -c <config> cleanup number`. A missing snapper is the one silent skip: the script exits 127 and the update ignores that specific code. Any other failure prints a warning and the update continues anyway, so an update never blocks on a failed snapshot.

Retention comes from the template at `default/snapper/root`, installed to `/etc/snapper/configs/root`. It sets `NUMBER_CLEANUP="yes"`, `NUMBER_MIN_AGE="0"`, `NUMBER_LIMIT="5"`, `NUMBER_LIMIT_IMPORTANT="5"` and `TIMELINE_CREATE="no"`. So you get the last five update snapshots and no hourly ones. The install step also writes `/etc/conf.d/snapper` with `SNAPPER_CONFIGS="root"`, disables `snapper-timeline.timer`, and enables `snapper-cleanup.timer` and `limine-snapper-sync.service`.

The boot entries come from the Limine drop-in at `/etc/limine-entry-tool.d/omarchy-defaults.conf`, which sets `MAX_SNAPSHOT_ENTRIES=6` and puts `Snapshots` last in the boot order. Six, not five, because `limine-snapper-sync` can see a newly created sixth snapshot before cleanup brings the count back down.

One 4.x change worth knowing: a migration shipped in 4.0.0 deletes leftover timeline snapshots from earlier defaults. Older installs ran hourly timeline snapshots, later configs stopped creating them but never removed the old ones, and number cleanup skips anything marked `Cleanup=timeline`, so they accumulated. The migration only runs when your config still has `TIMELINE_CREATE="no"`, and it deletes in batches of twenty so a DBus timeout does not take the whole migration run down.

## What a rollback does not give you back

- **Your home directory.** On the standard Omarchy layout, `/home` is a separate Btrfs subvolume (`@home`, alongside `@` and `@log`), so it is not part of the root snapshot. Good for reverting a broken update, useless for recovering deleted files. Issue #5361 reports the opposite experience on 3.5.1: a restore brought back `~/.config` and screenshots from the home directory, and nobody explained it in the thread. A `/home` that lives inside the root subvolume instead of `@home` would behave that way, so check `findmnt -no SOURCE /home` before you count on the separation.
- **`~/.config`.** This is the sharp edge. Roll back to a release whose libraries or apps wrote configs in an older format, and you keep the new config files. Issue #5916 is a clean example: a user rolled back from 3.8.0, the release that moved the Hyprland configs from `.conf` to `.lua`, and was left with Lua configs the older version could not use. Running `omarchy reinstall configs` did not help either, because it pulled the 3.8.0 configs straight back.
- **`/boot`.** That is the EFI system partition, a separate FAT filesystem outside Btrfs entirely. Kernels and the unified kernel image there are not snapshot content.
- **Nested subvolumes.** Btrfs snapshots do not recurse into nested subvolumes, so anything you or the installer split out is outside the picture.

## If that did not work

**Restore fails with "You are not in Btrfs".** Issue #8047 reports that `btrfs-overlayfs`, which Omarchy has in its mkinitcpio `HOOKS` line since 4.0.0 and still has on the development branch, mounts an overlay over `/` in every read only snapshot boot, and that `limine-snapper-sync` then refuses to run because `/` is no longer Btrfs. The report is detailed and unanswered by maintainers, so treat it as reported rather than confirmed, and check on your own machine from inside a snapshot boot:

```bash
findmnt -no FSTYPE /
sudo btrfs property get / ro
```

If the first prints `overlay`, the restore path will not run there. The reporter's workaround, which they say they verified end to end and which nobody else has confirmed, is a drop-in that filters the hook out. It has to sort after `omarchy_hooks.conf`, because that file assigns `HOOKS` outright rather than extending it, hence the `zz-` prefix. Create `/etc/mkinitcpio.conf.d/zz-no-btrfs-overlayfs.conf`:

```bash
_hooks=()
for _h in "${HOOKS[@]}"; do
  [[ $_h == "btrfs-overlayfs" ]] || _hooks+=("$_h")
done
HOOKS=("${_hooks[@]}")
unset _hooks _h
```

Then rebuild with `sudo limine-mkinitcpio`, not `mkinitcpio -P`, and take a fresh snapshot. Existing boot entries stay pinned to the initramfs that was current when they were taken, so an old entry keeps loading the overlay and looks like the fix failed. Dropping the hook also gives up the writable snapshot boot it provides, and you are editing a boot-critical file, so have a live USB within reach.

**"No Snapper configs found, so no snapshot was created."** Issue #10421 points out that a failed `sudo`, for example with no controlling terminal or a mistyped password, produces the same empty output as having no configs, so the script blames the wrong thing. Check first with `sudo snapper list-configs`. If a config exists, do not run the suggested `install/config/snapper.sh`, because it overwrites `/etc/snapper/configs/root` with the template.

**"IO Error (.snapshots is not a btrfs subvolume)".** Snapper needs `/.snapshots` to be a subvolume, and a snapshot of `@` carries it only as a plain directory, which is why Omarchy's own factory reset script repairs it afterwards. Issue #11100 ties the error to machines restored from an rsync, tar or clone backup, which flattens `/.snapshots` the same way. Issue #9097 hit the similar `subvolume is not a btrfs subvolume` on a fresh 4.0.1 install and only cleared it by reinstalling from USB. Verify with `sudo btrfs subvolume show /.snapshots` before doing anything destructive.

**The snapshot step fails during an update.** If you run a swapfile on the root subvolume, the kernel refuses to snapshot it. Issue #6456 reports this from a pre-4.0.0 development build, where the update still aborted at that step; on 4.0.x it continues without the snapshot. The workaround is `swapoff` before the update and `swapon` after.

**No snapshots appear in Limine at all.** Check the two services that feed it, then refresh the boot config:

```bash
systemctl status limine-snapper-sync.service snapper-cleanup.timer
sudo limine-snapper-sync
```

Issue #6629 reports `limine-snapper-sync` sitting inactive because of a missing dependency and a missing snapper root config. If your `/home` is a separate subvolume and you expected it covered, note issue #9619: the Omarchy install step rewrites `SNAPPER_CONFIGS` to `root` alone, which de-registers a `home` config you added yourself.

**Everything is still broken after a rollback.** `omarchy reinstall` resets Omarchy's default packages and configuration files, puts you back on the stable channel and downgrades packages that are too new. It also overwrites your changes to the Omarchy defaults, so keep it as the last step.

## Related

- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Upgrading 3.x to 4.0 Quattro](/upgrade/3-to-4-quattro/)
- [What migrations do](/upgrade/what-migrations-do/)
- Official manual: [System snapshots](https://omarchy.org/manual/system-snapshots/) and [Updates](https://omarchy.org/manual/updates/)
