---
title: "\"Something went wrong during the update!\" on a migration"
description: "An Omarchy migration failed and aborted the update. How to find the failing migration id, re-run omarchy-migrate safely, and skip one when it will never pass."
answer: "Usually nothing is broken. Re-run the migration step on its own with omarchy-migrate. Markers are only written after a migration exits zero, so finished ones are skipped and the failed one retries from the start. Read /usr/share/omarchy/migrations/<id>.sh to see what it wanted, fix that, then run omarchy update again to finish the steps the abort skipped."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 296
errorStrings:
  - "Something went wrong during the update!"
  - "Please review the output above carefully, correct the error, and retry the update."
  - "Running migration (1787515927)"
  - "Pending Omarchy Migrations"
  - "Waiting for pacman transaction to finish before running Omarchy migrations..."
tags: [update, migration, omarchy-migrate, quattro, recovery]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8832"
    title: "Issue #8832: Migration 1787515927 failed"
    kind: issue
    author: "neheb"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/8833"
    title: "Issue #8833: omarchy-theme-set-browser-policy exits 1 on success under Bash 5.3, breaking omarchy update at migration 1787515927"
    kind: issue
    author: "miltonio94"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/8835"
    title: "PR #8835: Fix migration 1787515927 failing on Bash 5.3"
    kind: pr
    author: "ryanrhughes"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/7026"
    title: "PR #7026: Prevent migration (1786643346) from hanging on stale browser lock files"
    kind: pr
    author: "joshuafouch"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/7130"
    title: "PR #7130: Skip the sleep lock repair when the unit is not installed"
    kind: pr
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7108"
    title: "Issue #7108: Migration 1781587663 aborts the whole migration queue when omarchy-nvim is not installed"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7078"
    title: "Issue #7078: omarchy-migrate mishandles legacy (git-checkout) installs: wrong OMARCHY_PATH default hides pending migrations, and migration 1785608166 aborts the whole queue"
    kind: issue
    author: "DiegoMirner"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/6866"
    title: "Issue #6866: Migration 1786643346 loops after reboot on stale Chromium SingletonLock"
    kind: issue
    author: "rfmyrick"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/7019"
    title: "Issue #7019: Cannot run Migration (1786643346) because an \"browser window is open\" according to the migration."
    kind: issue
    author: "joshuafouch"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/11257"
    title: "Issue #11257: omarchy update aborts on the final migration (1788619462, \"Hand Hermes Desktop the Omarchy theme as a skin\")"
    kind: issue
    author: "SavagePossum"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Omarchy v4.0.2 release notes"
    kind: release
    date: "2026-08-31"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
credits:
  - name: "miltonio94"
    url: "https://github.com/miltonio94"
    for: "Traced the Bash 5.3 EXIT trap change that made a successful migration report failure"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Fixed the Bash 5.3 migration abort and documented that markers are written only after success"
  - name: "rfmyrick"
    url: "https://github.com/rfmyrick"
    for: "Identified the stale Chromium SingletonLock symlinks that trap the browser migration in a loop"
  - name: "DiegoMirner"
    url: "https://github.com/DiegoMirner"
    for: "Showed that one failing migration strands every migration queued behind it"
faq:
  - q: "Is it safe to run omarchy-migrate again?"
    a: "Yes. Every migration has a marker file under ~/.local/state/omarchy/migrations/, and the runner writes that marker only after the script exits zero. Re-running skips everything already applied and retries only what is still pending."
  - q: "Where do I see which migrations are still pending?"
    a: "Run omarchy-migrate --pending. It prints one filename per pending migration and exits 0. When nothing is pending it prints nothing and exits 1, which is the clean state."
  - q: "Can I skip a migration that will never pass?"
    a: "On Omarchy 4 there is no skip flag. Create the marker by hand with touch ~/.local/state/omarchy/migrations/<id>.sh. Read the script first, because you are promising Omarchy that its change is already in place. On 3.x the runner asked you instead."
  - q: "Should I run the update with sudo?"
    a: "No. Run omarchy update as your normal user and let it ask for sudo where it needs it. Migrations read per-user state under your home, and in issue #11257 a sudo run put HOME at /root so the theme migration could not find the user's state and aborted."
related: [omarchy-update-fails-or-hangs, errors-occurred-no-packages-were-upgraded, pacnew-and-pacsave-files-after-update, you-are-in-emergency-mode-after-update]
draft: false
---

Your update stopped part way and printed a red block ending in "Please review the output above carefully, correct the error, and retry the update." A few lines above it there is a green `Running migration (<number>)` line. That number is the migration that failed. The failing script may have got part way through its own work, but the runner stops there and leaves every later migration untouched.

This page covers Omarchy 4.0.0 through 4.0.4, and notes where 3.x behaved differently.

## The fix

1. Find the failing migration id. The whole update run is recorded, so read the log rather than scrolling the terminal.

   ```bash
   grep -n "Running migration" /tmp/omarchy-update.log | tail -5
   ```

   The last id printed is the one that stopped. `/tmp/omarchy-update.log` is overwritten by the next run and wiped on reboot, so read it before either.

2. See what is still queued behind it.

   ```bash
   omarchy-migrate --pending
   ```

   It prints one filename per pending migration. When nothing is pending it prints nothing and exits 1, so `omarchy-migrate --pending; echo $?` returning `1` means you are caught up. The one exception is a pre-Quattro git checkout, where it exits 1 because it cannot find the migrations directory at all (see below).

3. Re-run the migration step on its own. This is safe, and it is the normal recovery.

   ```bash
   omarchy-migrate
   ```

   Do not use `sudo`. The runner keeps its markers in `~/.local/state/omarchy/migrations/` and writes each one only after that migration exits zero, so a re-run skips everything already applied and retries the failed one from the start.

4. If it fails again, read the migration. They are short shell scripts, and the file name is the only documentation you need to find it.

   ```bash
   less /usr/share/omarchy/migrations/<id>.sh
   ```

   Most failures are a precondition the script assumed. Close the browser it asks you to close, install the package it expects, or make the file it edits writable, then run `omarchy-migrate` again.

5. Finish the update. The migration step sits in the middle of `omarchy update`, so the abort also skipped the AUR packages, the mise update, the orphan prune and the log check.

   ```bash
   omarchy update
   ```

6. Last resort, mark one migration done without running it.

   ```bash
   touch ~/.local/state/omarchy/migrations/<id>.sh
   ```

   Only do this after reading the script and either applying its change by hand or confirming it does not apply to your machine. Omarchy 4 has no skip flag. On 3.x the runner asked `Migration <id> failed. Skip and continue?` and recorded your answer under `~/.local/state/omarchy/migrations/skipped/`; that prompt was removed in 4.0.

## Verify it worked

```bash
omarchy-migrate --pending; echo "exit=$?"
```

`exit=1` with no output above it is the finished state. If you want a second check, the marker count should match the shipped migration count:

```bash
ls /usr/share/omarchy/migrations/*.sh | wc -l
ls ~/.local/state/omarchy/migrations/*.sh | wc -l
```

Then run `omarchy update` once more and let it reach the restart prompt. If you were getting a "Pending Omarchy Migrations" notification at login, it should not come back on the next login. That toast comes from `omarchy-migrate-notify.service`, which runs once per login and offers to open `omarchy-migrate` in a floating terminal.

## Why it happens

Migrations are small shell scripts shipped inside the `omarchy` package at `/usr/share/omarchy/migrations/`. Each is named for a Unix timestamp, and they run in that order. Their job is to bring an existing machine in line with what a new release assumes: rewrite a config file, drop a retired package, move state to a new path. A fresh install marks them all done at provisioning time, so only upgrades run them.

The state is per user. Markers live in your home, which is why a second account on the same machine sees the whole list as pending and gets the login notification the first time it signs in.

`omarchy update` runs them in a fixed order: prune the package cache, take a Snapper snapshot, update the keyring, update system packages, then `omarchy-migrate`, then the post-update hook, AUR packages, mise, and orphan removal. Migrations run after the packages because they are written against the versions that were just installed. The cost of that placement is the one people hit: a migration failure aborts the whole update and everything after it never runs.

On Omarchy 4 the runner executes each migration under `bash -euo pipefail` and is itself under `set -euo pipefail`, so a single non-zero exit ends the loop. Issue #7078 is the clearest account of the blast radius: one migration that could not run left 28 more queued behind it, and the update ended with the same generic red block. Issue #7108 describes the same shape for a migration that installs a file from the `omarchy-nvim` package on a machine where that package was removed.

The individual causes reported against 4.0.x are varied rather than systemic:

- A shell change, not an Omarchy bug. Migration `1787515927` failed on every Bash 5.3 machine that reached it, even with nothing to harden, because an `EXIT` trap ended on a false test and Bash 5.3 adopts the trap's status as the script's exit status, where 5.2 did not. Reported in #8832, diagnosed in #8833, fixed by PR #8835 and shipped in [v4.0.2](/releases/v4.0.2/).
- Stale state that looks live. Migration `1786643346` decides a browser is open purely from `SingletonLock` and `SingletonSocket` under the profile directory. A Chromium-family browser that crashed or lost power leaves those behind, and because they sit under `~/.config` rather than `/tmp`, rebooting does not remove them. The migration then loops forever asking you to close a browser that is not running (#6866, #7019). The stuck profile can belong to a browser you rarely open: one report had the lock in a Brave profile last used two days earlier while Chromium was the browser being closed and reopened. Moving the stale `Singleton*` links out of the profile, with every Chromium-family browser genuinely closed, let the migration complete immediately. The fix in PR #7026 is still unmerged as of 4.0.4.
- Running the update through `sudo`. In #11257 the theme handover migration looked for per-user theme state under `$HOME`, which `sudo` had set to `/root`, and aborted. That issue is still open and the migration is unchanged in the 4.0.4 tree.
- A pre-Quattro git checkout. `omarchy-migrate` defaults `OMARCHY_PATH` to `/usr/share/omarchy`, which does not exist on a legacy self-updating checkout, so `--pending` reports nothing while dozens are actually outstanding (#7078). See [3 to 4 Quattro](/upgrade/3-to-4-quattro/).

## If that did not work

If the run stops at "Waiting for pacman transaction to finish before running Omarchy migrations...", another pacman process holds `/var/lib/pacman/db.lck`. The runner waits up to 15 minutes, then tells you migrations will retry at next login and exits cleanly. Let the other transaction finish rather than deleting the lock.

If you restored a Snapper snapshot at any point, treat your migration state as suspect. Markers live on the home subvolume and the changes migrations make live on the root subvolume, so a rollback rewinds the work and keeps the markers. Issue #9828 walks through one case where a boot-config migration was silently undone and never re-ran. There is no automatic detection for this; if you know which migration was reverted, delete its marker and run `omarchy-migrate`. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

If the failing step was not a migration at all, the red block is the same for every part of the update. Check whether the line above it came from pacman instead: see [errors occurred, no packages were upgraded](/fix/errors-occurred-no-packages-were-upgraded/) and [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/).

If a config file you edited is now shadowed by a `.pacnew`, the migration may have succeeded while the live file stayed stale. That is covered in [pacnew and pacsave files after update](/fix/pacnew-and-pacsave-files-after-update/).

These are one-off script bugs rather than a fault in the runner, but only the Bash 5.3 one has shipped a fix. The stale-lock fix (PR #7026) and the sleep-lock no-op for legacy installs (PR #7130) were both still open pull requests when 4.0.4 shipped, so for those the workarounds above are what you have.

## Related

- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Errors occurred, no packages were upgraded](/fix/errors-occurred-no-packages-were-upgraded/)
- [pacnew and pacsave files after update](/fix/pacnew-and-pacsave-files-after-update/)
- [What migrations do](/upgrade/what-migrations-do/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [omarchy-migrate command reference](/reference/commands/omarchy-migrate/)
- [Omarchy Manual: Updates](https://omarchy.org/manual/updates/)
