---
title: "omarchy update fails or hangs part way through"
description: "Read the omarchy update log, find the stage that died, rerun safely, replay a failed migration, and decide when to roll back on Omarchy 4.0.x."
answer: "Open /tmp/omarchy-update.log and find the last green stage heading, then run omarchy-update-analyze-logs before you reboot. Rerunning omarchy update is safe: the pacman transaction is idempotent and finished migrations are skipped by their per-user markers. Every silent hang we could trace was a custom or plugin hook, since omarchy-hook runs every hook under bash."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 386
errorStrings:
  - "Something went wrong during the update!"
  - "Please review the output above carefully, correct the error, and retry the update."
  - "An Omarchy update is already running."
  - "You need at least 10 GiB free to safely update Omarchy."
  - "Error: Initramfs generation may have failed. Review logs before restart."
  - "error: failed to commit transaction (conflicting files)"
  - "error: unresolvable package conflicts detected"
tags: [update, pacman, migrations, logs, rollback]
sources:
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual chapter 30, Updates"
    kind: manual
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/8492"
    title: "Issue #8492: omarchy-hook runs every hook via bash, ignoring the shebang, silently hangs on non-bash hooks that collide with a real binary name"
    kind: issue
    author: "hbabb"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9294"
    title: "Issue #9294: omarchy-hook runs hooks with bash, ignoring shebang and executable bit, non-bash hook silently hung omarchy-update"
    kind: issue
    author: "lvkz-okcapsule"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9845"
    title: "Issue #9845: omarchy-hook always runs .d hook scripts with bash, breaking non-bash hooks despite correct shebang + exec bit"
    kind: issue
    author: "DookyShooz"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8832"
    title: "Issue #8832: Migration 1787515927 failed"
    kind: issue
    author: "neheb"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/8835"
    title: "PR #8835: Fix migration 1787515927 failing on Bash 5.3"
    kind: pr
    author: "ryanrhughes"
    date: "2026-08-28"
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
  - url: "https://github.com/omacom/omarchy/issues/12044"
    title: "Issue #12044: Migration failed due to missing nvidia modules on linux-omarchy"
    kind: issue
    author: "xiyeming"
    date: "2026-09-16"
credits:
  - name: "hbabb"
    url: "https://github.com/hbabb"
    for: "Traced a silent update hang to a Python plugin hook being parsed by bash"
  - name: "lvkz-okcapsule"
    url: "https://github.com/lvkz-okcapsule"
    for: "Posted the process tree that identifies a hung post-update hook"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Diagnosed the unowned kernel modules tree that wedges pacman"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Fixed the Bash 5.3 migration failure carried in 4.0.2"
faq:
  - q: "Is it safe to rerun omarchy update after it failed?"
    a: "Yes, in almost every case. The pacman transaction either committed or did not, and migrations are tracked per user by marker files in ~/.local/state/omarchy/migrations/, so the ones that already succeeded are skipped."
  - q: "Where is the update log?"
    a: "/tmp/omarchy-update.log. omarchy update re-executes itself under script(1) so the whole session is captured, including pacman and yay output. It is in /tmp, so a reboot erases it."
  - q: "Can I just run pacman -Syu instead?"
    a: "No. Omarchy 4 installs an ALPM pre-transaction guard that aborts a direct system upgrade, because you would skip the snapshot, the migrations and the post-update hooks."
related: [migration-failed-mid-update, errors-occurred-no-packages-were-upgraded, creating-a-snapshot-failed-snapper]
draft: false
---

An Omarchy update that stops part way is almost always recoverable. The update is a
pipeline of small scripts, and the transcript tells you which one died. Start there
before you reboot or roll back.

## The fix

1. Read the transcript. `omarchy update` re-executes itself under `script(1)`, so the
   whole session lands in `/tmp/omarchy-update.log`. Open it with `less -R
   /tmp/omarchy-update.log` and jump to the end. Each stage prints a green heading
   (`Update system packages`, `Update Arch signing keys`, `Running migration (...)`),
   so the last heading is the stage that failed. The log lives in `/tmp`, so copy it
   somewhere before you reboot.

2. Run the built-in check: `omarchy-update-analyze-logs`. On 4.0.4 it scans that same
   log for one high-value condition, a failed initramfs rebuild, and prints
   `Error: Initramfs generation may have failed. Review logs before restart.` If you
   see that, do not reboot yet. Fix the initramfs first, or roll back.

3. If it hung instead of failing, find the child process before you kill anything:

   ```bash
   pstree -aps $(pgrep -f 'omarchy-update' | head -1)
   ```

   A hang under `omarchy-hook post-update` or under a migration calling
   `omarchy-theme-set` points at a custom or plugin-installed hook. Move
   `~/.config/omarchy/hooks/` aside and retry.

4. Rerun the update. `omarchy update` is safe to repeat: pacman either committed the
   transaction or did not, and `omarchy-migrate` records each finished migration as a
   marker file under `~/.local/state/omarchy/migrations/`, so completed migrations are
   skipped.

5. If you get `An Omarchy update is already running.`, a real process still holds a
   flock on `$XDG_RUNTIME_DIR/omarchy-update.lock`. Find it with `pgrep -af
   omarchy-update` and end it. The lock is held on an open file descriptor, so it
   releases the moment the process is gone. The file itself stays on disk and is
   harmless; deleting it does not unblock anything.

6. If the log ends in `You need at least 10 GiB free to safely update Omarchy.`, free
   space on `/` and retry. `sudo paccache -rk1` and pruning Snapper snapshots are the
   usual wins. The update's own cache prune (`paccache -rk2`) runs after this check,
   so it cannot rescue you here. `OMARCHY_UPDATE_FORCE=1 omarchy update` bypasses the check, which is a
   bad idea mid-kernel-upgrade.

7. If the log ends in `error: unresolvable package conflicts detected`, run the update
   interactively, without `-y`. Omarchy reruns pacman without `--noconfirm` in that case
   so you can answer the replace question yourself, and it refuses to do so under `-y`
   or without a terminal.

8. If a single migration failed, fix the cause and run `omarchy-migrate` on its own.
   A migration only gets its marker after it succeeds, so the failed one is still
   pending and runs again; the ones that finished are skipped.
   `omarchy-migrate --pending` lists what is still outstanding. To force a migration
   that already completed to run again, remove its marker first:

   ```bash
   rm ~/.local/state/omarchy/migrations/<migration>.sh
   omarchy-migrate
   ```

9. If the machine will not boot, or the failure hit the kernel or bootloader, pick the
   pre-update snapshot in the Limine menu instead. See
   [/upgrade/rollback-with-snapper-and-limine/](/upgrade/rollback-with-snapper-and-limine/).

## Verify it worked

Run `omarchy update` once more. A clean run ends with the restart prompt and no red
trap message. Then confirm nothing is left pending:

```bash
omarchy-migrate --pending   # prints nothing and exits non-zero when clean
pacman -Qu                  # no pending upgrades
omarchy-version
```

If `omarchy-update-analyze-logs` is quiet after a fresh run, either the initramfs
rebuilt or no kernel package was touched. The check only fires when the log contains
an `Updating linux initcpios` line without a matching success line.

## Why it happens

On 4.x the update is package-backed. `omarchy-update` takes a lock, checks for 10 GiB
free, prunes the package cache, takes a Snapper snapshot, updates the keyrings, runs
`pacman -Syu`, then runs migrations, post-update hooks, AUR and mise updates, and the
log analyzer. Any step that exits non-zero trips a shell trap that prints
`Something went wrong during the update!` followed by
`Please review the output above carefully, correct the error, and retry the update.`
That message is generic on purpose. The real cause is in the lines above it.

Four causes account for most reports we could verify:

- **A hook that is not a bash script.** `omarchy-hook` runs every file in a hook
  directory with `bash`, ignoring the shebang and the executable bit. A Python hook gets
  half-interpreted, and a line starting with `import` runs ImageMagick's `import`, which
  waits forever for a click. Reported independently in
  [#8492](https://github.com/omacom/omarchy/issues/8492),
  [#9294](https://github.com/omacom/omarchy/issues/9294) and
  [#9845](https://github.com/omacom/omarchy/issues/9845), all still open as of 4.0.4.
  A plugin can install such a hook without you knowing.

- **A migration that hits an environment it did not expect.** Migration `1787515927`
  failed for users on Bash 5.3 ([#8832](https://github.com/omacom/omarchy/issues/8832));
  ryanrhughes fixed it in [PR #8835](https://github.com/omacom/omarchy/pull/8835), and
  the 4.0.2 release notes list a fix for migration failures on Bash 5.3.

- **Unowned files pacman refuses to overwrite.** Omarchy clears leftovers it recognises
  as its own, but files outside that set stop the transaction. In
  [#9142](https://github.com/omacom/omarchy/issues/9142) a kernel downgrade plus
  kernel-modules-hook left the running kernel's module tree owned by nobody, and every
  later update failed with 6,454 `exists in filesystem` lines.
  [PR #9285](https://github.com/omacom/omarchy/pull/9285) proposes handling it and is
  still open. Rebooting into the installed kernel first, then updating, clears it.

- **A DKMS module that fails to build.** In
  [#12044](https://github.com/omacom/omarchy/issues/12044) the 4.0.4 kernel migration
  reported `module not found: 'nvidia'`, but a commenter showed the real failure was the
  NVIDIA DKMS build being killed by the OOM killer during a parallel compile. The
  initramfs error is downstream of that.

**3.x differs.** On 3.8.4 and earlier the update was a git pull into `~/.local/share/omarchy`
plus `omarchy-update-perform`. There was no update lock, no free-space check and no
package cache prune, and a failed snapshot aborted the update instead of warning and
carrying on. `/tmp/omarchy-update.log` and `omarchy-update-analyze-logs` already
existed, so step 1 and step 2 work on 3.x too.

## If that did not work

Collect the evidence rather than guessing. `omarchy-debug` writes a diagnostic dump to
`/tmp/omarchy-debug.log` (`--print` sends it to the terminal instead), and
`omarchy-upload-log this-boot` pushes the current boot journal to logs.omarchy.org with a
24 hour expiry so you can paste one URL into an issue or the Discord. Include the last
green stage heading from `/tmp/omarchy-update.log`.

If the update keeps failing at the same package transaction, check whether your real
problem is a mirror or signature issue rather than the updater. See
[/fix/failed-to-retrieve-some-files-pacman/](/fix/failed-to-retrieve-some-files-pacman/)
and [/fix/signature-is-unknown-trust-keyring/](/fix/signature-is-unknown-trust-keyring/).

As a last resort the manual points at `omarchy reinstall`, which reinstalls the default
packages, puts you back on stable and resets the Omarchy config files. It overwrites your
customisations of those defaults, so back up `~/.config/hypr/` and `~/.config/omarchy/`
first.

## Related

- [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/)
- [/fix/creating-a-snapshot-failed-snapper/](/fix/creating-a-snapshot-failed-snapper/)
- [/fix/errors-occurred-no-packages-were-upgraded/](/fix/errors-occurred-no-packages-were-upgraded/)
- [/fix/plugin-fails-to-load/](/fix/plugin-fails-to-load/)
- [/upgrade/before-you-update-checklist/](/upgrade/before-you-update-checklist/)
- [/upgrade/what-migrations-do/](/upgrade/what-migrations-do/)
- [/reference/commands/omarchy-update/](/reference/commands/omarchy-update/)
- [/releases/still-broken/](/releases/still-broken/)
