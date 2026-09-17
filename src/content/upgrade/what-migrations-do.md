---
title: "What Omarchy migrations do and how to read them"
description: "Omarchy migrations are one-time repair scripts in migrations/*.sh. How omarchy-migrate runs them, how to preview them, and what to do when one aborts an update."
answer: "Migrations are one-time repair scripts at /usr/share/omarchy/migrations/<timestamp>.sh that fix state pacman cannot own. omarchy update runs them after the package transaction through omarchy-migrate. Completion is tracked per user in ~/.local/state/omarchy/migrations/. Run omarchy-migrate --pending to list what is queued, and read each file's first echo line to see what it does. If one fails, the queue stops and you resume with omarchy-migrate."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [migrations, omarchy-migrate, updates, quattro, troubleshooting]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/docs/migrations.md"
    title: "docs/migrations.md at v4.0.4"
    kind: docs
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/docs/update-process.md"
    title: "docs/update-process.md at v4.0.4"
    kind: docs
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/11257"
    title: "Issue #11257: omarchy update` aborts on the final migration (1788619462, \"Hand Hermes Desktop the Omarchy theme as a skin\""
    kind: issue
    author: "SavagePossum"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7078"
    title: "Issue #7078: omarchy-migrate mishandles legacy (git-checkout) installs: wrong OMARCHY_PATH default hides pending migrations, and migration 1785608166 aborts the whole queue"
    kind: issue
    author: "DiegoMirner"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/9640"
    title: "Issue #9640: 1788009111.sh fails on pt_BR (and other non-English locales): LC_ALL=C não força inglês para lpstat"
    kind: issue
    author: "rafaelclima"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations (surfaced as: LUKS prompt still QWERTY after e891e5c)"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/12173"
    title: "Issue #12173: Migration 1789095456.sh collides with the deleted PTL-kernel migration of the same name"
    kind: issue
    author: "ekollof"
    date: "2026-09-16"
credits:
  - name: "rafaelclima"
    url: "https://github.com/rafaelclima"
    for: "Traced a failing migration to gettext ignoring LC_ALL, which is why one locale can stop the whole queue"
  - name: "v-h-z"
    url: "https://github.com/v-h-z"
    for: "Showed that Snapper rollbacks rewind the root subvolume but not the per-user migration markers on @home"
faq:
  - q: "How do I see what an Omarchy migration will do before I run it?"
    a: "Run omarchy-migrate --pending to get the filenames, then read each file under /usr/share/omarchy/migrations/. Every migration shipped in v4.0.4 opens with an echo line that states its purpose in one sentence."
  - q: "Is it safe to run omarchy-migrate by hand?"
    a: "Yes. Migrations that already have a marker under ~/.local/state/omarchy/migrations/ are skipped, and the runner waits for any active pacman transaction first. It is the same command omarchy update calls."
  - q: "Why does omarchy-migrate --pending exit non-zero when everything is fine?"
    a: "The exit code is inverted on purpose so the login notifier can use it as a test. Exit 0 means at least one migration is pending, and a non-zero exit means none are."
  - q: "Do migrations handle the upgrade from Omarchy 3 to 4?"
    a: "No. The 3 to 4 crossing is done by bin/omarchy-upgrade-to-quattro, which runs the normal migration queue at the end of its work. Upstream asks contributors not to write compatibility migrations for pre-4 installer layouts."
related: [3-to-4-quattro, before-you-update-checklist, rollback-with-snapper-and-limine]
draft: false
---

An Omarchy migration is a one-time repair script. It exists because some things an update needs to change are not owned by a package: files in your home directory, user systemd units, a session setting, sometimes a stale file a retired installer left behind. Pacman cannot safely rewrite those, so Omarchy ships a small script that does, runs it once per user, and remembers that it ran.

This page describes the model as of v4.0.4, released 2026-09-15. The runner changed shape in 4.0.0 and the commands below are 4.x commands.

## Where migrations live and what they look like

In the source repository they sit in `migrations/`. On a package-backed 4.x install they land at `/usr/share/omarchy/migrations/`. Each file is named after a unix timestamp, for example `1789325478.sh`, which is what gives the queue a strict order.

The file format is deliberately plain. There is no shebang line, and the files ship mode `0644`. The runner executes them with `bash -euo pipefail` rather than relying on an executable bit. Each one is expected to be idempotent, so that running it a second time, or running it as a second user on the same machine, does nothing harmful.

The useful convention for you as a reader: a migration starts with an `echo` that describes what it does. That is a documented authoring rule, and it holds in practice. All 106 migration files shipped in v4.0.4 begin with an `echo` line. So the first line of any migration file is a one-sentence summary written by the person who wrote the change.

```bash
head -n 1 /usr/share/omarchy/migrations/1789325478.sh
```

## How completion is tracked

Completion state is per user:

```text
~/.local/state/omarchy/migrations/<migration filename>
```

The marker is an empty file. If it exists, that migration is considered done for that user and will never run again for them. If you have two accounts on one machine, each account gets its own chance to run every migration, which is why migrations that repair machine-wide state have to detect that the repair already happened and quietly do nothing.

Some migrations do that detection with machine-wide state of their own. In v4.0.4, 10 of the 106 migrations use `/var/lib/omarchy/migrations/`, most of them for a `<timestamp>` marker written once the privileged part of the work is done so the next user to hit the same migration can skip the sudo prompt, and a couple for reload-needed flags or a quarantine directory. The runner itself knows nothing about those files. It only ever checks the per-user directory.

## When migrations run

There are three triggers.

During `omarchy update`, the package transaction goes first and migrations follow it. The order inside `omarchy-update` on 4.0.4 is `omarchy-update-system-pkgs`, then `omarchy-migrate`, then `omarchy-hook post-update`. Migrations are written against the packages that were just installed, so if the package step fails the whole update stops there and no migration runs against the old files.

At login, `omarchy-migrate-notify.service` starts after `graphical-session.target`, checks for pending migrations, and shows a notification if there are any. Clicking it opens a terminal running `omarchy-migrate`; nothing runs behind your back. It stays quiet while `omarchy update` holds its lock at `$XDG_RUNTIME_DIR/omarchy-update.lock`, because that update is about to apply the same migrations in a terminal you can see. This login path is what covers a second user on the machine, and anyone who bypassed the pacman guard with `sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu`.

Manually, at any time:

```bash
omarchy-migrate
```

Before it runs anything it waits on `/var/lib/pacman/db.lck`, polling once a second for up to 900 seconds. If a pacman transaction is still going after that, it tells you so and leaves the migrations for next login.

The 3 to 4 upgrade is not a migration. That work belongs to `bin/omarchy-upgrade-to-quattro`, which calls `omarchy-migrate` near the end of its work and refuses to finish if anything is still pending. See [the 3 to 4 upgrade page](/upgrade/3-to-4-quattro/).

## Reading pending migrations before you update

```bash
omarchy-migrate --pending
```

It prints one filename per line. Watch the exit code, because it is inverted: `0` means one or more migrations are pending, non-zero means none are. That is so the login notifier can use the command directly as a test.

To turn that list into readable descriptions, use the first line of each file:

```bash
for m in $(omarchy-migrate --pending); do
  printf '%-12s %s\n' "${m%.sh}" \
    "$(head -n 1 "/usr/share/omarchy/migrations/$m" | cut -d' ' -f2- | tr -d '"')"
done
```

Then read any file that sounds like it touches something you care about. Most are short. In v4.0.4, 85 of the 106 are 40 lines or fewer.

```bash
cat /usr/share/omarchy/migrations/1788619462.sh
```

One limit worth knowing. The pending list only contains migrations from the Omarchy package version you already have installed. New migrations arrive with the new package, so `--pending` before an update cannot show you what the next release will run. For that, use the decoded per-release list on [the releases page](/releases/), or read `migrations/` in the repository at the tag you are about to move to.

## When an update aborts partway through a migration

On 4.x the queue is strict. `omarchy-migrate` runs with `set -euo pipefail`, and it only writes the marker after the migration exits zero. A migration that fails therefore stops the queue, stays pending, and leaves everything after it pending too. `omarchy-update` has an error trap, so what you see is a red "Something went wrong during the update!" message.

The important thing to understand is what state you are in. The pacman transaction already finished. Your packages are updated. What is incomplete is the repair work, and the queue picks up where it stopped.

1. Find the last migration the terminal announced. It prints `Running migration (<timestamp>)` in green before each one. The full transcript is at `/tmp/omarchy-update.log`.
2. Read that file, starting with its `echo` line.
3. Reproduce the failure on its own so you can see the real error:

```bash
bash -euo pipefail /usr/share/omarchy/migrations/<timestamp>.sh
```

4. Fix whatever precondition it tripped over, then resume the queue:

```bash
omarchy-migrate
```

5. If it is a known upstream bug and the migration genuinely does not apply to your machine, you can mark it complete by hand so the queue moves on. This is a deliberate choice to skip that repair forever, so do it only when you have read the file:

```bash
touch ~/.local/state/omarchy/migrations/<timestamp>.sh
omarchy-migrate
```

The reverse also works. To make a migration run again, delete its marker and run the migrator.

Note the behaviour change from 3.x. The 3.8.4 runner prompted "Migration ... failed. Skip and continue?" and tracked skipped migrations in a separate `skipped/` directory. The 4.x runner has no prompt and no skip directory. You get the stop, and the decision is yours to make by hand.

### Verify you are caught up

```bash
omarchy-migrate --pending || echo "nothing pending"
```

Do not compare directory sizes instead. Markers from migrations that upstream has since pruned stay in `~/.local/state/omarchy/migrations/`, and an install that crossed from 3.x carries markers for all 330 of the 3.8.4 migrations plus the old `skipped/` directory, so the state directory is normally larger than the shipped set. `--pending` is the only check that asks the right question.

## Failures people have actually hit

These are open reports at the time of writing, and they are good illustrations of how the model can bite.

Running the update through `sudo` breaks the per-user assumption. In [issue #11257](https://github.com/omacom/omarchy/issues/11257), a user on 4.0.3 ran `sudo omarchy update -y` and the Hermes theme migration failed because `$HOME` was `/root`, where no Omarchy theme state exists. Run `omarchy update` as your normal user. It asks for sudo where it needs it.

A non-English locale stopped the queue. [Issue #9640](https://github.com/omacom/omarchy/issues/9640) reports a printer migration on 4.0.2 failing under `pt_BR.UTF-8`, because the script compared `lpstat` output against a hardcoded English string and `LC_ALL=C` alone does not force English out of gettext. Everything after that migration stayed pending.

Legacy git-checkout installs see a false all-clear. [Issue #7078](https://github.com/omacom/omarchy/issues/7078) points out that `omarchy-migrate` defaults `OMARCHY_PATH` to `/usr/share/omarchy`. On an old self-updating checkout that directory does not exist, so `--pending` finds nothing and reports that you are up to date when dozens of migrations have never run.

Snapshot rollbacks desynchronise state. [Issue #9828](https://github.com/omacom/omarchy/issues/9828) explains that markers live on `@home` while most migrations change `/` on `@`. Restoring a Snapper snapshot rewinds the changes and keeps the markers, so those migrations never run again. If you roll back, consider deleting the markers for migrations you know ran after the snapshot. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

Filename reuse can skip a migration entirely. [Issue #12173](https://github.com/omacom/omarchy/issues/12173) reports that on the development branch after 4.0.4, `1789095456.sh` was deleted and later re-added with unrelated content, so anyone who completed the original version already carries that marker and silently skips the new one. The file is not in the v4.0.4 package; it would arrive with the next release unless it is renamed first.

## What to watch for on newer versions

The migration model has been stable across 4.0.0 through 4.0.4. The only change to `omarchy-migrate` in that span moved the migration list onto a separate file descriptor, and the script is byte-identical between the v4.0.4 tag and the current development snapshot, so the commands here should survive the next release.

Two things are worth rechecking after any upgrade. First, whether the runner still tracks completion only per user. Issue #9828 asks upstream to move markers for system-scoped migrations to `/var/lib/omarchy/migrations/`, where individual migrations already keep their machine-wide markers, and issue #12173 already speaks of a machine marker as part of completion. Second, whether a second user on the machine still gets the login prompt, since that path depends on `omarchy-migrate-notify.service` being enabled for that account.

## Related

- [Before you update checklist](/upgrade/before-you-update-checklist/)
- [Upgrading 3 to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Release notes with decoded migration lists](/releases/)
- Official manual: [Updates](https://omarchy.org/manual/updates/)
