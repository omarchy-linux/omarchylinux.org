---
title: 'signature from "..." is unknown trust'
description: "Pacman aborts an Omarchy update with a signature is unknown trust error. Refresh archlinux-keyring, trust the Omarchy signing key, then retry the update."
answer: "Your local pacman keyring is stale. Run omarchy update first, since it reinstalls archlinux-keyring and locally signs the Omarchy key. If it still fails, run sudo pacman -Sy archlinux-keyring and retry. If the failing line names Omarchy pkgs@omarchy.org, receive and lsign key 40DFB630FF42BCFFB047046CF0134EE680CAC571, then reinstall omarchy-keyring. Never set SigLevel to Never."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 56
errorStrings:
  - 'signature from "Andreas Radke <andyrtr@archlinux.org>" is unknown trust'
  - 'error: libseccomp: signature from "Levente Polyak (anthraxx) <levente0@leventepolyak.net>" is unknown trust'
  - "invalid or corrupted package (PGP signature)"
  - 'error: wayfreeze: signature from "Omarchy <pkgs@omarchy.org>" is invalid'
  - 'key "F0134EE680CAC571" could not be looked up remotely'
tags: [pacman, keyring, update, signatures, security]
sources:
  - url: "https://github.com/omacom/omarchy/issues/2916"
    title: 'Issue #2916: key "F0134EE680CAC571" could not be looked up remotely'
    kind: issue
    author: "yapus"
    date: "2025-10-28"
  - url: "https://github.com/omacom/omarchy/issues/4197"
    title: "Issue #4197: Unable to update Omarchy (invalid or corrupted package (PGP signature))"
    kind: issue
    author: "apurbapokharel"
    date: "2026-01-09"
  - url: "https://github.com/omacom/omarchy/issues/4268"
    title: "Issue #4268: Updating broke system configuration"
    kind: issue
    author: "Michallote"
    date: "2026-01-15"
  - url: "https://github.com/omacom/omarchy/issues/4594"
    title: "Issue #4594: libvpl corrupted error while upgrading Omarchy"
    kind: issue
    author: "ajoabraham"
    date: "2026-02-13"
  - url: "https://github.com/omacom/omarchy/issues/4608"
    title: "Issue #4608: Invalid or corrupted packages when updating"
    kind: issue
    author: "gpakosz"
    date: "2026-02-15"
  - url: "https://github.com/omacom/omarchy/issues/3466"
    title: "Issue #3466: Fail to update: wayfreeze signature is invalid"
    kind: issue
    author: "EmrysMyrddin"
    date: "2025-11-19"
  - url: "https://github.com/omacom/omarchy/issues/2712"
    title: "Issue #2712: Enhance [omarchy] Repo Security: Switch SigLevel to Required DatabaseOptional and Update Security Docs"
    kind: issue
    author: "MrJack91"
    date: "2025-10-22"
  - url: "https://github.com/omacom/omarchy/issues/9199"
    title: "Issue #9199: omarchy repo signing key exists in keyring but SigLevel still Optional TrustAll (follow-up to #2712)"
    kind: issue
    author: "drneb99"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/6576"
    title: "Issue #6576: upgrade-to-quattro: install_keyrings uses pacman -Sy, so a rebuilt package loops forever on corrupted (checksum)"
    kind: issue
    author: "jfbourdeau"
    date: "2026-08-06"
  - url: "https://github.com/omacom/omarchy/issues/5083"
    title: "Issue #5083: stable-mirror.omarchy.org signature file retrieval fails (max file size exceeded)"
    kind: issue
    author: "osharko"
    date: "2026-03-20"
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy manual: Security (Signing Keys)"
    kind: manual
credits:
  - name: "dhh"
    url: "https://github.com/dhh"
    for: "Posted the full receive, lsign and omarchy-keyring sequence in issue #2916 that became omarchy-update-keyring"
  - name: "yapus"
    url: "https://github.com/yapus"
    for: "Found the manual key import path when keys.openpgp.org refuses the receive"
  - name: "apurbapokharel"
    url: "https://github.com/apurbapokharel"
    for: "Documented the pacman-key init and populate recovery"
  - name: "Gundrak"
    url: "https://github.com/Gundrak"
    for: "Confirmed a plain archlinux-keyring refresh clears the corrupted package error"
  - name: "hbouttev"
    url: "https://github.com/hbouttev"
    for: "Separated the Arch keyring failure from the unrelated Hyprland config errors in the same thread"
  - name: "jfbourdeau"
    url: "https://github.com/jfbourdeau"
    for: "Traced the endless checksum loop to a stale package database rather than a bad download"
  - name: "drneb99"
    url: "https://github.com/drneb99"
    for: "Reported that older installs kept SigLevel = Optional TrustAll for the omarchy repo"
faq:
  - q: "Is it safe to add SigLevel = Never to get the update through?"
    a: "No. That turns off signature checking for every package from that repo, permanently, and nothing later turns it back on. Refreshing the keyring takes about the same amount of time and keeps the check."
  - q: "Why is the Omarchy key not in archlinux-keyring?"
    a: "It is a separate key for a separate repository. archlinux-keyring only carries Arch developer and trusted user keys. The Omarchy packaging key ships in the omarchy-keyring package and has fingerprint 40DFB630FF42BCFFB047046CF0134EE680CAC571."
  - q: "Does running pacman -Sy archlinux-keyring on its own break anything?"
    a: "It leaves your package database newer than your installed packages, which is a partial upgrade state. That is acceptable as a one step bridge if you immediately run a full omarchy update afterwards, which is exactly what omarchy-update-keyring does."
related: [errors-occurred-no-packages-were-upgraded, failed-to-retrieve-some-files-pacman, omarchy-update-fails-or-hangs]
draft: false
---

Pacman stops partway through an update and prints a line like `error: tzdata: signature from "Andreas Radke <andyrtr@archlinux.org>" is unknown trust`, the exact line apurbapokharel hit in issue #4197, usually followed by a prompt asking whether to delete the cached file and then `error: failed to commit transaction`. Nothing is broken on your machine. Your local pacman keyring does not yet trust the key that signed the new package.

Checked against v4.0.4, v4.0.3 and v4.0.2 source, and against the last 3.x release, v3.8.4.

## The fix

Work down this list and stop as soon as an update completes.

1. Run the normal update first, from the Omarchy menu or the terminal:

   ```bash
   omarchy update
   ```

   In both 3.x and 4.x this calls `omarchy-update-keyring` before the package transaction. That script reinstalls `archlinux-keyring` every run, on purpose, because the keyring contents can change without the package version changing. For many people this alone is the whole fix.

2. If the update still stops, refresh the Arch keyring on its own and retry:

   ```bash
   sudo pacman -Sy archlinux-keyring
   omarchy update
   ```

   This is what cleared it for Gundrak and ajoabraham in issue #4594. In issue #4268 hbouttev likewise told kqualters-elastic to update `archlinux-keyring` on its own before retrying, and to run `sudo pacman-key --refresh-keys` if that was not enough.

3. If the failing line names `Omarchy <pkgs@omarchy.org>` rather than an Arch developer, or pacman asks `Import PGP key F0134EE680CAC571, "Unknown Packager"?` and then reports `key "F0134EE680CAC571" could not be looked up remotely`, the missing key is the Omarchy packaging key. That second form is what yapus saw in issue #2916. Trust the key directly, using the sequence dhh posted in that thread:

   ```bash
   sudo pacman-key --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571 --keyserver keys.openpgp.org
   sudo pacman-key --lsign-key 40DFB630FF42BCFFB047046CF0134EE680CAC571
   sudo pacman -Sy
   omarchy-pkg-add omarchy-keyring
   ```

   If the first command fails with `Remote key not fetched correctly from keyserver`, yapus worked around it by downloading the key from the keys.openpgp.org search page and importing the file:

   ```bash
   sudo pacman-key -a ~/Downloads/40DFB630FF42BCFFB047046CF0134EE680CAC571.asc
   ```

4. If the error now says `corrupted (invalid or corrupted package (checksum))` and repeats forever no matter how often the file is downloaded, your local copy of the package database still holds the old checksum for a package the server has rebuilt, so deleting the cached file changes nothing. Force the databases to download again:

   ```bash
   sudo pacman -Syy
   omarchy update
   ```

   The double `y` is the part that matters. A plain `-Sy` keeps a database it believes is current. jfbourdeau traced exactly this loop in issue #6576 while re-running the 3.x to 4.x upgrade, where `omarchy-keyring` itself was the package that kept failing, and `pacman -Syy` was the workaround. If you would rather reset the mirrors and repo config at the same time, `sudo omarchy-refresh-pacman` rewrites `/etc/pacman.conf` and the mirrorlist from the Omarchy defaults for your channel and then runs `pacman -Syyuu`. It overwrites local edits to `/etc/pacman.conf`, though it does back the old file up to `/etc/pacman.conf.bak` first.

5. Only if all of the above fail, clear the cache and rebuild the keyring from scratch. dhh suggested the cache clear in issue #4197, and apurbapokharel plus moritzuehling landed on the rebuild:

   ```bash
   sudo rm -rf /var/cache/pacman/pkg/*
   sudo pacman-key --init
   sudo pacman-key --populate archlinux
   sudo pacman -Sy archlinux-keyring
   omarchy update
   ```

### What not to do

Do not add `SigLevel = Never` or `SigLevel = Optional TrustAll` to `/etc/pacman.conf` to push the transaction through. It disables the check for good and nothing puts it back. Do not delete `/etc/pacman.d/gnupg` as a first move, since `pacman-key --init` recreates it anyway and a half deleted keyring is harder to reason about. Do not run a bare `sudo pacman -Syu` to work around it either. Omarchy 4.x installs `omarchy-update-pacman-guard`, which blocks direct system upgrades and tells you to use `omarchy update` instead.

## Verify it worked

Check that the Omarchy key is present and locally signed:

```bash
sudo pacman-key --list-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
pacman -Q archlinux-keyring omarchy-keyring
```

On 4.0.2 and later, the `[omarchy]` block in `/etc/pacman.conf` should have no `SigLevel` line of its own, so it inherits the global `SigLevel = Required DatabaseOptional`:

```bash
grep -A2 '^\[omarchy\]' /etc/pacman.conf
```

Then run `omarchy update` once more and let it finish through migrations without an error.

## Why it happens

Two separate keyrings are in play.

Arch packages from core, extra and multilib are signed by Arch developers and trusted users. Their keys live in the `archlinux-keyring` package. Those keys rotate, expire and get added as people join and leave. If your machine has been off for a while, or an install media snapshot is old, a package can arrive signed by a key your local keyring has never seen. Pacman reports that as unknown trust rather than as a bad signature, because it can read the signature fine and just has no reason to believe the signer.

Omarchy packages from the `[omarchy]` repo are signed by a different key, `Omarchy <pkgs@omarchy.org>`, fingerprint `40DFB630FF42BCFFB047046CF0134EE680CAC571`. That key is not in `archlinux-keyring`, a point phush0 made in issue #2916. It ships in the `omarchy-keyring` package, and the manual lists the same fingerprint under [Signing Keys](https://omarchy.org/manual/security/).

This is why `omarchy-update-keyring` exists, and it works the same way in v3.8.4 and v4.0.4. It checks whether `omarchy-keyring` is missing or the fingerprint is absent from `pacman-key --list-keys`, receives and locally signs the key if so, and then reinstalls `archlinux-keyring` on every single run.

### What changed in 4.0.2

Until then the `[omarchy]` repo carried `SigLevel = Optional TrustAll` in the shipped `pacman.conf`, which you can see in the v3.8.4, v4.0.0 and v4.0.1 source. Signatures were effectively not enforced for that repo. Issue #2712, filed by MrJack91 and argued out at length by alerque and ryanrhughes, pushed for real enforcement. ryanrhughes announced there on 2025-10-26 that every package going into the repo would be signed from then on, and posted the same receive and lsign pair two days before dhh repeated it in issue #2916. v4.0.2 shipped enforcement as "Require signed packages from the Omarchy repository", and a migration removes the override from existing installs, after first making sure the key is trusted so it cannot lock you out of the transaction that would repair it. drneb99 filed issue #9199 the day before, showing a 4.0.1 machine that still had the old line.

The practical effect is that a machine upgraded past 4.0.2 with a keyring that never picked up the Omarchy key will now stop instead of silently accepting the package. That is the intended behaviour, and the fix is step 3 above.

## If that did not work

Read the error line carefully, because `is invalid` is not the same as `is unknown trust`. Invalid means the signature does not match the file, which is usually a repository or mirror problem rather than yours. In issue #3466 a run of packages including wayfreeze failed that way and dhh fixed it server side within a day. If you see invalid, wait an hour and retry before touching your keyring.

If the failure is on retrieving the `.sig` file rather than verifying it, that is a mirror issue too. osharko reported in issue #5083 that `stable-mirror.omarchy.org` rejected signature downloads over a size cap, which shows up as a retrieval failure, not a trust failure. See [failed to retrieve some files](/fix/failed-to-retrieve-some-files-pacman/).

A badly wrong system clock will also make signature checks fail, since GPG compares timestamps. Check `timedatectl` before anything more invasive. That is general Arch behaviour rather than something reported against Omarchy, so treat it as a cheap thing to rule out.

The issue count above is for keyring problems as a whole. Only a minority of those threads are signature trust failures, and no single one is the canonical report, which is why the steps are assembled from several.

## Related

- [Errors occurred, no packages were upgraded](/fix/errors-occurred-no-packages-were-upgraded/)
- [failed to retrieve some files](/fix/failed-to-retrieve-some-files-pacman/)
- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Signing key and ISO verification](/security/signing-key-and-iso-verification/)
- [Release channels](/releases/channels/)
- [omarchy-refresh-pacman](/reference/commands/omarchy-refresh-pacman/)
