---
title: "Errors occurred, no packages were upgraded."
description: "Why pacman aborts an Omarchy update with \"failed to commit transaction\" and no packages were upgraded, and the order to try mirror, keyring and file-conflict fixes."
answer: "Nothing was installed, so your system is intact. Read the real pacman error above the summary line in /tmp/omarchy-update.log. Mirror or 404 errors: run omarchy-refresh-pacman, then omarchy update. Signature or corrupted-package errors: clear /var/cache/pacman/pkg and refresh the keyrings. Conflicting files: find the unowned path with pacman -Qo and move it aside."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 22
errorStrings:
  - "Errors occurred, no packages were upgraded."
  - "error: failed to commit transaction (failed to retrieve some files)"
  - "error: failed to commit transaction (invalid or corrupted package (PGP signature))"
  - "error: failed to commit transaction (conflicting files)"
  - "error: unresolvable package conflicts detected"
  - "Please review the output above carefully, correct the error, and retry the update."
tags: [update, pacman, mirrors, keyring, transaction]
sources:
  - url: "https://github.com/omacom/omarchy/issues/4197"
    title: "Issue #4197: Unable to update Omarchy (invalid or corrupted package (PGP signature))"
    kind: issue
    author: "apurbapokharel"
    date: "2026-01-09"
  - url: "https://github.com/omacom/omarchy/issues/2916"
    title: "Issue #2916: key \"F0134EE680CAC571\" could not be looked up remotely"
    kind: issue
    author: "yapus"
    date: "2025-10-28"
  - url: "https://github.com/omacom/omarchy/issues/4594"
    title: "Issue #4594: libvpl corrupted error while upgrading Omarchy"
    kind: issue
    author: "ajoabraham"
    date: "2026-02-13"
  - url: "https://github.com/omacom/omarchy/issues/3650"
    title: "Issue #3650: stable package mirror returns 404 when installing howdy"
    kind: issue
    author: "wim07101993"
    date: "2025-11-27"
  - url: "https://github.com/omacom/omarchy/issues/3357"
    title: "Issue #3357: Unable to update fresh Omarchy 3.1.7 installation"
    kind: issue
    author: "inad9300"
    date: "2025-11-12"
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
  - url: "https://github.com/omacom/omarchy/issues/7059"
    title: "Issue #7059: Bitwarden menu installation fails after installing Zed"
    kind: issue
    author: "kvechkanov"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/3877"
    title: "Issue #3877: omarchy failed everything when yay not working after a failed update, dead lock"
    kind: issue
    author: "aohan237"
    date: "2025-12-15"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
credits:
  - name: "apurbapokharel"
    url: "https://github.com/apurbapokharel"
    for: "Posted the pacman-key reinit sequence that cleared a stuck PGP signature error"
  - name: "yapus"
    url: "https://github.com/yapus"
    for: "Found the manual key import workaround when the keyserver refused the Omarchy key"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Traced the unowned kernel module tree that wedges the file-conflict retry"
faq:
  - q: "Did the failed update break my system?"
    a: "No. Pacman aborts the whole transaction before installing anything, which is exactly what that message means. Your packages are still at the versions they were at before you started."
  - q: "Can I just run sudo pacman -Syu instead?"
    a: "Omarchy 4 blocks a direct system upgrade with a guard so you do not skip the snapshot and migrations. If you really need one transaction outside the update, the guard prints the bypass: sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu."
  - q: "Where is the update log?"
    a: "omarchy update records the whole run to /tmp/omarchy-update.log. It is cleared on reboot, so read it before you restart."
related: [failed-to-retrieve-some-files-pacman, signature-is-unknown-trust-keyring, omarchy-update-fails-or-hangs, migration-failed-mid-update]
draft: false
---

This is pacman's summary line, not the error. It means the transaction was rolled back before anything was written, so your system is in the same state it was in before you ran the update. The cause is on the lines above it.

## The fix

1. Find the real error. On Omarchy 4 the whole update run is recorded, so open the log rather than scrolling the terminal:

   ```bash
   grep -nE "^error:|exists in filesystem|is corrupted|404|signature" /tmp/omarchy-update.log | tail -40
   ```

   The log lives at `/tmp/omarchy-update.log` and is wiped on reboot. Read it first.

2. Run the update once more. Several of the reported failures are transient: a mirror that was mid-sync, a download that stalled, a Wi-Fi drop during the transfer. In issue #3357 the reporter got through after repeated attempts with no other change.

   ```bash
   omarchy update
   ```

   On 3.x the command is `omarchy-update`, and `omarchy update` also works from 3.7 on.

3. If the error mentions `failed to retrieve some files`, a 404, or a TLS failure, your pacman config or database has drifted from the mirrors Omarchy uses. Reset both:

   ```bash
   omarchy-refresh-pacman
   ```

   That backs up `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist` to `.bak`, rewrites them from the channel defaults, and runs a full `pacman -Syyuu`. Pass `rc` or `edge` as an argument only if you are deliberately on that channel. This is what DHH recommended first in issue #4197.

4. If the error mentions a signature, marginal or unknown trust, or `invalid or corrupted package`, clear the cached download and rebuild the keyrings:

   ```bash
   sudo rm -rf /var/cache/pacman/pkg/*
   sudo pacman-key --init
   sudo pacman-key --populate archlinux
   sudo pacman -Sy archlinux-keyring
   omarchy update
   ```

   That sequence is what finally cleared issue #4197 for the reporter. If the missing key is the Omarchy one, import it by hand:

   ```bash
   sudo pacman-key --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571 --keyserver keys.openpgp.org
   sudo pacman-key --lsign-key 40DFB630FF42BCFFB047046CF0134EE680CAC571
   ```

   Since 3.1.4 `omarchy-update-keyring` runs those two commands for you when the key is absent, so needing them by hand usually means the keyserver fetch failed.

5. If the error is `conflicting files` with lines like `pkg: /some/path exists in filesystem`, check who owns each path before touching it:

   ```bash
   pacman -Qo /some/path
   ```

   If pacman reports no owner, move it aside and retry. Keep a copy somewhere outside the directory it came from, because some directories are scanned wholesale.

   ```bash
   sudo mkdir -p /var/lib/omarchy/replaced/some
   sudo mv -T /some/path /var/lib/omarchy/replaced/some/path
   omarchy update
   ```

6. If the error is `unresolvable package conflicts detected` or `failed to prepare transaction (conflicting dependencies)`, pacman needed a yes or no answer and answered it with No. Run `omarchy update` from a real terminal without `-y`. On 4.x the update reruns the upgrade interactively so you can answer the replacement prompt yourself.

## Verify it worked

The update ends without the red "Something went wrong during the update!" banner. After it finishes:

```bash
pacman -Qu
omarchy-version
```

`pacman -Qu` should print nothing, and `omarchy-version` should show the release you expected. If you moved files aside in step 5, check whether `/var/lib/omarchy/replaced` now holds anything you still need before deleting it.

## Why it happens

Pacman is all or nothing. It resolves the transaction, downloads every package, verifies every signature, and checks every file it is about to write. Any failure in that sequence aborts the whole thing and prints `Errors occurred, no packages were upgraded.` So the summary is always the same regardless of cause, and there are four common causes.

Mirror and network problems. Omarchy serves packages from its own mirrors, and the stable channel runs about a month behind Arch, so a package that exists upstream can be missing from the Omarchy mirror. Issue #3650 is a plain 404 from the stable mirror. Issue #3357 is the other shape: repeated download stalls during the update, where commenters got further by setting `ParallelDownloads = 1` in `/etc/pacman.conf`, and one reporter got through by temporarily disabling IPv6.

Signature and keyring drift. `SigLevel = Required DatabaseOptional` is the shipped default, and 4.0.2 tightened this further by requiring signed packages from the Omarchy repository. A stale `archlinux-keyring`, a cached package that was truncated mid-download, or a maintainer key you have never trusted all produce a corruption or trust error. Issue #4594 is a clean example, where a marginal-trust signature on `libvpl` ended the transaction.

File conflicts. Pacman refuses to write over a file no package owns. Omarchy 4 handles the common case itself: `omarchy-update-system-pkgs` runs `pacman -Syu --noconfirm --overwrite '/usr/share/omarchy/*'`, captures stderr, and on failure hands off to a retry helper that moves unowned files reported against the `omarchy` and `omarchy-settings` packages into `/var/lib/omarchy/replaced` and tries again, putting anything the upgrade did not take back afterwards. That helper only acts when every reported conflict belongs to those packages, which is why issue #9142 stays wedged: thousands of unowned files under `/usr/lib/modules/` left behind by `kernel-modules-hook` are outside its remit. That issue is still open, with a proposed fix in PR #9285.

Package conflicts. Two packages that cannot coexist need a human decision. Issue #7059 is the textbook case: `bitwarden-cli` wants `nodejs-lts-jod` while an earlier Zed install pulled in `nodejs`, and `--noconfirm` answers the replacement prompt with No.

3.x behaved differently here. `omarchy-update-system-pkgs` on v3.8.4 is two lines, a plain `pacman -Syyu --noconfirm`, with no conflict handler and no retry. On 3.x every one of these failures lands in your lap.

## If that did not work

Check whether the failure is actually in a later stage. `omarchy update` runs the keyring step, then system packages, then migrations, then AUR packages. A failure after the pacman stage is a different problem: issue #3877 is the well-known one, where `yay` stopped loading after a `libalpm` soname bump and several people fixed it by rebuilding `yay` from the AUR.

If the update is failing at migrations rather than at pacman, see [migration failed mid-update](/fix/migration-failed-mid-update/). If it hangs rather than errors, see [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/).

When you are out of ideas, roll back. Omarchy takes a Snapper snapshot before each update, so you can return to the pre-update state with [rollback with snapper and limine](/upgrade/rollback-with-snapper-and-limine/), then try again once the mirror has caught up.

## Related

- [failed to retrieve some files](/fix/failed-to-retrieve-some-files-pacman/)
- [signature is unknown trust](/fix/signature-is-unknown-trust-keyring/)
- [pacnew and pacsave files after update](/fix/pacnew-and-pacsave-files-after-update/)
- [before you update checklist](/upgrade/before-you-update-checklist/)
- [release channels](/releases/channels/)
- [Omarchy Manual: Updates](https://omarchy.org/manual/updates/)
