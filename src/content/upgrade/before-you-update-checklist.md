---
title: "Before you run omarchy update: a pre-flight checklist"
description: "A pre-flight checklist for omarchy update on Omarchy 4.0.4: check your channel, free space, snapshots and pending migrations, then handle pacnew files yourself."
answer: "Before running omarchy update, check your channel with omarchy-channel-current, confirm at least 10 GiB free on /, make sure Snapper is actually configured so the automatic snapshot really happens, and list pending work with omarchy-migrate --pending. After the update, hunt for .pacnew files yourself, because Omarchy still does not do it for you in 4.0.4."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [update, migrations, snapper, channels, pacnew, rollback]
sources:
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy Manual: System snapshots"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/6456"
    title: "Issue #6456: omarchy update fails at snapshot step when a swapfile is active on the btrfs root subvolume"
    kind: issue
    author: "markbus-ai"
    date: "2026-07-31"
  - url: "https://github.com/omacom/omarchy/issues/9142"
    title: "Issue #9142: omarchy update wedged by unowned kernel-modules-hook leftovers after release-migration kernel downgrade"
    kind: issue
    author: "DrakeMorrison"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/pull/9285"
    title: "PR #9285: Clear unowned running-kernel modules leftovers during update"
    kind: pr
    author: "fresh3nough"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations (surfaced as: LUKS prompt still QWERTY after e891e5c)"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/12060"
    title: "Issue #12060: Kernel migration rejects valid FAT32 ESP discovered as systemd autofs"
    kind: issue
    author: "holystix04"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9640"
    title: "Issue #9640: 1788009111.sh fails on pt_BR (and other non-English locales): LC_ALL=C não força inglês para lpstat"
    kind: issue
    author: "rafaelclima"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/8833"
    title: "Issue #8833: omarchy-theme-set-browser-policy exits 1 on success under Bash 5.3, breaking omarchy update at migration 1787515927"
    kind: issue
    author: "miltonio94"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/8835"
    title: "PR #8835: Fix migration 1787515927 failing on Bash 5.3"
    kind: pr
    author: "ryanrhughes"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/8282"
    title: "Issue #8282: Update Omarchy to 4.0.1 updates to release candidate and moves users to edge channel forcefully"
    kind: issue
    author: "Michallote"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7634"
    title: "Issue #7634: Omarchy update installs incompatible quickshell"
    kind: issue
    author: "mattrayner"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/6169"
    title: "Issue #6169: Kernel/limine update leaves boot broken until manual limine-mkinitcpio rerun"
    kind: issue
    author: "el7oussine3yyache"
    date: "2026-07-05"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
    date: "2026-09-08"
credits:
  - name: "miltonio94"
    url: "https://github.com/miltonio94"
    for: "Traced a whole-update failure to a Bash 5.3 EXIT trap changing a helper's exit status"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Explained why a kernel downgrade plus kernel-modules-hook wedges omarchy update"
  - name: "markbus-ai"
    url: "https://github.com/markbus-ai"
    for: "Found that an active swapfile on the btrfs root blocks the pre-update snapshot"
faq:
  - q: "Do I need to make a snapshot manually before updating?"
    a: "Not if Snapper is configured, because omarchy update creates one for you. Run omarchy-snapshot create once by hand first, though, to prove it works. If Snapper is installed but has no configs, the snapshot step prints a warning and the update continues without one."
  - q: "Does Omarchy warn me about .pacnew files?"
    a: "No. As of 4.0.4 the project's own update-process document still lists pacnew and pacsave handling as missing, and no shipped update command looks for them. You have to search /etc yourself after an update."
  - q: "Can I just run sudo pacman -Syu instead?"
    a: "An ALPM pre-transaction guard aborts direct pacman system upgrades and points you back to omarchy update. You can bypass it with sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu, but you then skip the snapshot, the migrations and the post-update hooks."
  - q: "How much free disk space does an update need?"
    a: "At least 10 GiB on /. omarchy-update-requires-free-space checks before the confirmation prompt and stops the update below that. Set OMARCHY_UPDATE_FORCE=1 to skip the check."
related: [rollback-with-snapper-and-limine, what-migrations-do, 3-to-4-quattro]
draft: false
---

Most Omarchy updates are uneventful. The ones that are not tend to fail in the same few places: the snapshot that never happened, a migration that aborts the run, a kernel bump that does not produce a bootable entry. This checklist takes about two minutes and is written against 4.0.4.

## The checklist

1. Know which channel you are on.

```bash
omarchy-channel-current
```

That prints `stable`, `rc`, `edge`, `dev`, or `unknown`. Stable tracks tagged releases and an Arch mirror that deliberately runs about a month behind. Edge tracks development builds and current Arch. Dev points `OMARCHY_PATH` at a git checkout in `~/omarchy` instead of the packaged `/usr/share/omarchy`, plus the edge packages. Switch with `omarchy-channel-set stable` or the Omarchy menu under Update, Channel. Channel changes are worth verifying rather than assuming: in [issue #8282](https://github.com/omacom/omarchy/issues/8282) a user on stable reported that updating to 4.0.1 appeared to put them on a release candidate, and re-selecting stable ran a second round of downloads. That issue is closed.

2. Read the release notes for whatever is about to land. The releases page is [github.com/omacom/omarchy/releases](https://github.com/omacom/omarchy/releases). Compare it with your installed version from `omarchy-version`.

3. Check free space.

```bash
df -h /
```

`omarchy-update-requires-free-space` stops the update before the confirmation prompt if `/` has less than 10 GiB available. `OMARCHY_UPDATE_FORCE=1` bypasses it, which is a bad idea when a kernel and an initramfs rebuild are in the transaction.

4. Prove that snapshots actually work.

```bash
sudo snapper list-configs
omarchy-snapshot create
```

`omarchy update` calls `omarchy-snapshot create` for you, but the failure modes are quiet. If Snapper is not installed the command exits 127 and the update continues on purpose. If Snapper is installed with no configs, it warns that nothing was captured and tells you to run the Snapper installer script, and the update still proceeds. A hand-run snapshot now tells you which of those you are in. One concrete case: an active swapfile on the btrfs root subvolume makes the kernel refuse the snapshot, reported in [issue #6456](https://github.com/omacom/omarchy/issues/6456) against a pre-release 4.0 build and still open. Back then it aborted the update. Since 4.0.0 the update prints the warning and carries on without a snapshot, which is the quieter failure and the reason to run the snapshot by hand first.

5. Back up `/home` separately. Snapshot restore rewinds the root subvolume only. Your `/home` and your `~/.config` are left exactly as they are, which the manual states plainly in the [system snapshots chapter](https://omarchy.org/manual/system-snapshots/).

6. List pending work.

```bash
omarchy-migrate --pending
```

It prints pending migration names and exits 0 when there are any. Silence and a non-zero exit means nothing is pending.

7. Run the update from a real terminal on mains power, not over SSH and not on a laptop at 3 percent. The run ends with `omarchy-update-restart`, which offers a reboot when the kernel or Hyprland changed and then tries to restart the Quickshell shell every time, printing a reason if that fails.

## Verify it worked

```bash
omarchy-version
omarchy-channel-current
omarchy-migrate --pending
grep -i -E "error|failed" /tmp/omarchy-update.log | head
```

`/tmp/omarchy-update.log` holds the full transcript, captured through `script(1)`. `omarchy-update-analyze-logs` already scans it for one known pattern, a failed initramfs generation, and prints a red warning if the "Updating linux initcpios" line appears without a matching success line. Read that warning before rebooting, not after.

## Handle pacnew files yourself

This is the gap people trip over. Omarchy's own `docs/update-process.md` lists pacnew and pacsave handling under "Remaining concerns" as still missing, and that text is unchanged in the 4.0.4 tree and in the in-progress development tree for the next release. No shipped command mentions `.pacnew`. So do it by hand after every update:

```bash
sudo find /etc -name '*.pacnew' -o -name '*.pacsave'
```

This matters more than it sounds, because migrations read your live config. Migration `1786605598`, the one that rebuilds the initramfs so NVIDIA-only machines stop bundling unused nouveau firmware, explicitly skips systems where the user edited `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` and pacman therefore parked the packaged update in a `.pacnew`. The migration treats that skip as correct, since an edited file is your choice, but it means an unmerged `.pacnew` can silently opt you out of a change Omarchy meant to make.

## Known breakage patterns

Kernel and bootloader work is where updates hurt. [Issue #6169](https://github.com/omacom/omarchy/issues/6169) reports a system dropping to an emergency shell after kernel and Limine updates until `limine-mkinitcpio` is rerun by hand; that one was filed from a 3.8.2 install updating with plain `pacman -Syu`, but the boot pieces are the same. [Issue #12060](https://github.com/omacom/omarchy/issues/12060), filed against 4.0.4, has the kernel migration's Limine hook rejecting a perfectly valid FAT32 ESP because systemd auto-mounts `/boot` and the filesystem type reads as `autofs`. Both are open.

A second pattern is a single migration taking the whole run down. In [issue #8833](https://github.com/omacom/omarchy/issues/8833) a helper returned exit status 1 on success under Bash 5.3, so the browser-policy migration failed, its marker was never written, and every retry failed the same way. That one was fixed by [PR #8835](https://github.com/omacom/omarchy/pull/8835), merged on 2026-08-29. The broken form only ever reached edge builds: the migration is absent from the 4.0.0 and 4.0.1 trees, and 4.0.2, the first tagged release to carry it, already has the fix. The same shape is still live in [issue #9640](https://github.com/omacom/omarchy/issues/9640): a printer migration compares an English `lpstat` string, `LC_ALL=C` does not override `LANGUAGE` for gettext, and the update dies on non-English locales. The `LC_ALL=C` call is still there in the 4.0.4 migration, so treat this as open.

Third, package conflicts. [Issue #9142](https://github.com/omacom/omarchy/issues/9142) describes thousands of "exists in filesystem" errors under `/usr/lib/modules` after a kernel downgrade left unowned module files behind. Omarchy's conflict handler only clears leftovers that pacman blames on the omarchy packages themselves, so conflicts reported against `linux` stay put, and the proposed widening in [PR #9285](https://github.com/omacom/omarchy/pull/9285) is still open. Finally, mirror skew: [issue #7634](https://github.com/omacom/omarchy/issues/7634) had an edge update installing a Quickshell build needing a newer Qt than the mirror served, and the thread shows the same skew hitting RC and stable in the opposite direction. It closed once the mirrors caught up the next day, but the package repository and the Arch mirrors sync independently, so it can recur on any channel.

## If the update breaks your system

Reboot, choose Limine, pick the snapshot dated before the update, and confirm the restore from inside it, or run `omarchy-snapshot restore`. Note the trap in [issue #9828](https://github.com/omacom/omarchy/issues/9828): migration markers live in `~/.local/state/omarchy/migrations/` on the home subvolume, which a rollback does not rewind, so migrations that were undone will not run again on their own. After any rollback, list that directory and delete the marker for anything you want re-applied, then run `omarchy-migrate`. Be selective: the maintainer follow-up in that thread notes some migrations run real pacman transactions, so a blanket replay is not free.

As a last resort `omarchy reinstall` puts you back on stable defaults and overwrites your config customizations.

## Differences from 3.x

On v3.8.4 the update was much thinner: a confirmation, a snapshot, a git pull, and a single perform step. There was no free-space check, no update lock, no pacman guard and no per-user migration notifier, and sleep prevention was a `hyprctl` noidle tag rather than a proper inhibitor. If a guide you are following predates 4.0.0, assume its update advice is stale.

## What to watch for on newer versions

DHH said on X on 2026-09-08 that the next release will be Quattro RS 4.5. Two things are worth rechecking on it: whether pacnew handling has finally moved out of the "remaining concerns" list, and whether the Limine hook's boot path check has been taught about systemd automounts.
