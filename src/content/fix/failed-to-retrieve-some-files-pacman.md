---
title: "error: failed to commit transaction (failed to retrieve some files)"
description: "Pacman 404s from stable-mirror.omarchy.org usually mean stale package databases, not a broken mirror. Refresh with pacman -Syy, then run omarchy update."
answer: "Your package databases are newer than the mirror you are pointed at, so pacman asks for files that are not there yet. Run `sudo pacman -Syy` to re-download the databases, then `omarchy update`. If the mirror and the Omarchy repo disagree about which channel you are on, run `omarchy channel set stable` to reset both and upgrade."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 19
errorStrings:
  - "warning: failed to retrieve some files"
  - "error: failed to commit transaction (failed to retrieve some files)"
  - "error: failed to synchronize all databases (failed to retrieve some files)"
  - "The requested URL returned error: 404"
tags: [pacman, mirror, update, channels, 404]
sources:
  - url: "https://github.com/omacom/omarchy/issues/3650"
    title: "Issue #3650: stable package mirror returns 404 when installing howdy"
    kind: issue
    author: "wim07101993"
    date: "2025-11-27"
  - url: "https://github.com/omacom/omarchy/issues/3559"
    title: "Issue #3559: lib32-llvm-libs stable-mirror.omarchy.org 404"
    kind: issue
    author: "NathanaelRea"
    date: "2025-11-22"
  - url: "https://github.com/omacom/omarchy/issues/3716"
    title: "Issue #3716: stable package mirror returns 404 when installing pandoc"
    kind: issue
    author: "adecora"
    date: "2025-12-01"
  - url: "https://github.com/omacom/omarchy/issues/5085"
    title: "Issue #5085: Install script fails due to package mirror 404 error and lacks dependency error handling"
    kind: issue
    author: "death366"
    date: "2026-03-20"
  - url: "https://github.com/omacom/omarchy/issues/4258"
    title: "Issue #4258: Installing Dropbox raises 404"
    kind: issue
    author: "ayadcodes"
    date: "2026-01-14"
  - url: "https://github.com/omacom/omarchy/issues/3357"
    title: "Issue #3357: Unable to update fresh Omarchy 3.1.7 installation"
    kind: issue
    author: "inad9300"
    date: "2025-11-12"
  - url: "https://github.com/omacom/omarchy/issues/1645"
    title: "Issue #1645: error: failed retrieving file, Exceeded the maximum allowed file size (16384) with 16384 bytes"
    kind: issue
    author: "abuturabofficial"
    date: "2025-09-13"
  - url: "https://github.com/omacom/omarchy/issues/6985"
    title: "Issue #6985: Quattro (4.0) install fails: fix-synaptic-touchpad.sh psmouse module mismatch + vulkan.sh offline mirror missing files"
    kind: issue
    author: "ahmedsrea"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.2.0"
    title: "Release v3.2.0: new stable Arch mirror and stable package repository"
    kind: release
    author: "dhh"
    date: "2025-11-21"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.2.2"
    title: "Release v3.2.2: fix repository DBs being out of sync with the current channel"
    kind: release
    author: "dhh"
    date: "2025-11-29"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
    author: "dhh"
    date: "2026-09-15"
credits:
  - name: "dhh"
    url: "https://github.com/dhh"
    for: "Pointing at `sudo pacman -Syy` and `omarchy-channel-set stable` as the cure for 404s on the stable mirror"
  - name: "alebahn"
    url: "https://github.com/alebahn"
    for: "Explaining that a cached database from a wider mirror set is what makes pacman ask for files stable does not have"
  - name: "Flashengo"
    url: "https://github.com/Flashengo"
    for: "Showing that switching to the edge mirror unblocks a package stable has not picked up yet"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Noting the error text is misleading and that the databases, not the files, are usually out of sync"
  - name: "Laiter"
    url: "https://github.com/Laiter"
    for: "The IPv6 workaround for downloads that stall with Operation too slow"
  - name: "idrissmortadi"
    url: "https://github.com/idrissmortadi"
    for: "Suggesting ParallelDownloads = 1 for flaky downloads"
faq:
  - q: "Is the Omarchy mirror down when I get a 404?"
    a: "Usually not. A 404 means the exact filename pacman asked for is not on that mirror. That is most often a stale local database asking for a version the stable mirror has not synced yet, not an outage. Occasionally a package really is missing, as with lib32-llvm-libs in issue #3559, which dhh added to the stable repo by hand."
  - q: "Can I just add an Arch mirror to /etc/pacman.d/mirrorlist?"
    a: "It works, and `omarchy update` itself leaves the file alone. But `omarchy refresh pacman` and `omarchy channel set` both overwrite it from the Omarchy defaults, so the edit is gone the next time either of those runs."
  - q: "Why does sudo pacman -Syu print Woah partner on Omarchy 4?"
    a: "4.0 added an ALPM guard that blocks direct system upgrades so you do not skip the snapshot and migrations. Use `omarchy update`, or `sudo env OMARCHY_ALLOW_DIRECT_PACMAN=1 pacman -Syu` for one transaction."
related: [errors-occurred-no-packages-were-upgraded, omarchy-update-fails-or-hangs, signature-is-unknown-trust-keyring, migration-failed-mid-update]
draft: false
---

Pacman prints this when it knows the filename of a package but the server it asks does not have that file. On Omarchy the server is almost always one of the Omarchy mirrors, and the cause is almost always your local package databases being ahead of the mirror you are pointed at.

## The fix

These steps were checked against v4.0.4. On v3.8.4 the same commands exist except `omarchy channel current`, `omarchy channel set` also resets the git branch there, and there is no update guard (step 4).

1. See which channel you are actually on:

   ```bash
   omarchy version channel
   omarchy channel current
   ```

   `omarchy version channel` reads `/etc/pacman.d/mirrorlist` and `/etc/pacman.conf` separately and prints one word if they agree. If it prints something like `edge / stable`, your Arch mirror and your Omarchy package repo are on different channels, which is the classic 404 setup. Skip to step 3.

2. Force a full database re-download, then update:

   ```bash
   sudo pacman -Syy
   omarchy update
   ```

   The double `y` discards the cached databases instead of skipping ones that look current. This is the step dhh pointed people at in [issue #3650](https://github.com/omacom/omarchy/issues/3650), and `sudo pacman -Syyu` is what resolved [issue #4258](https://github.com/omacom/omarchy/issues/4258) for the reporter.

3. If the channels disagreed in step 1, reset both sides at once:

   ```bash
   omarchy channel set stable
   ```

   That runs `omarchy refresh pacman`, which copies `pacman-stable.conf` and `mirrorlist-stable` into place, runs `pacman -Syyuu`, makes sure the `omarchy` and `omarchy-settings` packages are installed, and finishes with a full update. dhh suggested exactly this in [issue #3716](https://github.com/omacom/omarchy/issues/3716). Use `rc` or `edge` in place of `stable` if that is the channel you meant to be on.

4. On 4.x, do not reach for `sudo pacman -Syu` yourself. 4.0 added an ALPM pre-transaction hook, `omarchy-update-pacman-guard`, that aborts direct system upgrades with a message starting "Woah partner..." and tells you to run `omarchy update` instead. Plain `pacman -Syy` and single-package installs are not blocked. On 3.8.4 there is no guard, which is why older comments tell people to run `sudo pacman -Syu` directly.

5. If the package you want simply has not reached stable yet, you have two honest choices: wait for the next mirror sync, or move to the edge channel with `omarchy channel set edge`. Edge moves your whole system to current Arch, not just the one package, and on 4.x it also swaps you onto the `omarchy-dev` packages, so treat it as a commitment rather than a workaround.

## Verify it worked

Re-run whatever failed. Beyond that:

- `omarchy version channel` should print a single word, not a pair separated by a slash.
- `omarchy version pkgs` prints when your packages were last upgraded.
- Compare the mirror stamp to upstream:

  ```bash
  date -d @$(curl -s https://stable-mirror.omarchy.org/lastupdate)
  date -d @$(curl -s https://geo.mirror.pkgbuild.com/lastupdate)
  ```

  Arch mirrors serve `/lastupdate` and `/lastsync` as a unix timestamp, and the Omarchy hosts do too. If the mirror stamp is older than the package version pacman is asking for, waiting is the fix.

## Why it happens

Omarchy moved off public Arch mirrors during 3.x; by v3.8.4 each default mirrorlist carries a single Omarchy host and nothing else. The stable channel points at `stable-mirror.omarchy.org`, which is deliberately behind upstream Arch so package breakage gets caught before it reaches everyone. The [v3.2.0 release notes](https://github.com/omacom/omarchy/releases/tag/v3.2.0) describe that lag as about a month. Measured on 2026-09-17 (UTC), `stable-mirror.omarchy.org` reported a `lastupdate` of 2026-09-07, roughly nine days behind the Arch geo mirror, while `mirror.omarchy.org` (edge) was within an hour of it.

That lag is fine until your local databases come from somewhere else. Pacman resolves a package to an exact filename from the database, then fetches that filename. If the database came from edge and the files come from stable, the name it wants does not exist and you get a 404 rather than a useful message. dhh said as much in [issue #3559](https://github.com/omacom/omarchy/issues/3559): databases from edge reference packages that do not exist on stable. alebahn described this well in [issue #5085](https://github.com/omacom/omarchy/issues/5085): the available version was cached from when a wider mirror set was configured, and `pacman -Syy` cleared it. ryanrhughes made the same point on [issue #1645](https://github.com/omacom/omarchy/issues/1645), adding that the error text is not a reliable guide to the real problem.

The Omarchy package repo lags in the same way. Measured on the same day, the stable repo carried 235 packages and edge carried 243; 39 packages differed in version between the two, 10 existed only on edge, and 2 only on stable. A database from one and files from the other will 404.

v3.2.2 shipped a fix for the worst version of this, where switching from edge to stable left the old databases in place. That helps when you switch channels through the supported command. It does not help if you edited `/etc/pacman.conf` or the mirrorlist by hand, and it does not remove the lag itself.

## If that did not work

- **Downloads stall or time out rather than 404.** [Issue #3357](https://github.com/omacom/omarchy/issues/3357) collects a few things people tried: temporarily disabling IPv6 with `sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1` (two people said it worked), simply retrying until the transfer completes (the reporter), and setting `ParallelDownloads = 1` in `/etc/pacman.conf` (suggested, with no one confirming it). dhh called it a network issue. None of these is a confirmed root cause.
- **Signature or keyring errors mixed in with the 404s.** Those are a different problem, see [signature is unknown trust](/fix/signature-is-unknown-trust-keyring/).
- **You are failing during a fresh install from the ISO, with `from disk : Could not open file` instead of a 404.** The installer uses an offline mirror bind mounted into the target, and a run that stopped partway leaves an empty directory behind, so every later package fails to retrieve. That is [issue #6985](https://github.com/omacom/omarchy/issues/6985), not mirror lag. See [install fails or stalls](/fix/install-fails-or-stalls/).
- **You added an upstream Arch mirror by hand.** Two people in [issue #5085](https://github.com/omacom/omarchy/issues/5085) got unblocked that way, and it does work. It is not durable, and the install script in that thread kept forcing the mirrorlist back: `omarchy refresh pacman` and `omarchy channel set` both overwrite `/etc/pacman.d/mirrorlist`. They do back up the previous file to `mirrorlist.bak` and `pacman.conf.bak` first.
- **The error mentions a maximum allowed file size instead of a 404.** Same family of causes. In [issue #1645](https://github.com/omacom/omarchy/issues/1645) the reporter cleared it by re-running with `-Sy`, ryanrhughes suggested `sudo pacman -Syu` or waiting for the mirror to settle, and cicku pointed at the Cloudflare setup in front of the mirror. Refreshing the databases is still the first thing to try.

## Related

- The manual chapter on [updates and channels](https://omarchy.org/manual/updates/)
- [Errors occurred, no packages were upgraded](/fix/errors-occurred-no-packages-were-upgraded/)
- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Release channels](/releases/channels/) and [stable mirror lag and CVEs](/security/stable-mirror-lag-and-cves/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
