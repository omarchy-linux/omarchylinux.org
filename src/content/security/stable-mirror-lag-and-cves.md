---
title: "Stable mirror lag vs Arch upstream, and what it costs you"
description: "How far behind Arch the Omarchy stable mirror really runs, measured 2026-09-17, what it cost during the Chromium exploit, and how to switch channels."
answer: "Omarchy's stable channel pulls Arch core, extra and multilib from stable-mirror.omarchy.org, which is deliberately frozen between resyncs. On 2026-09-17 it was 9 days behind Arch, with 2,658 extra packages and 52 core packages at older versions than edge. Check yours with the mirror's lastupdate endpoint. Switch with omarchy-channel-set edge if you need a fix now."
appliesTo:
  from: "3.x"
status: by-design
lastVerified: 2026-09-17
omarchyVersionTested: "4.0.4"
severity: medium
reported: "Issue #9064 (2026-08-30) and issue #10732 (2026-09-07)"
projectResponse: "No maintainer has replied on either issue as of 2026-09-17, but the stable mirror resynced on 2026-09-08 and now carries the fixed Chromium 152.0.7977.82-1 that #10732 asked for."
tags: [security, mirror, updates, channels, pacman, cve]
sources:
  - url: "https://github.com/omacom-io/omarchy-mirror"
    title: "omacom-io/omarchy-mirror README"
    kind: docs
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy Manual: Updates"
    kind: manual
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/10732"
    title: "Issue #10732: Stable mirror frozen since Aug 25 keeps default Chromium on 151 while 152.0.7977.82 fixes an in-the-wild exploit (CVE-2026-85046)"
    kind: issue
    author: "JohnAtl"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/9064"
    title: "Issue #9064: stable-mirror.omarchy.org Arch repo databases stale (~5 days behind)"
    kind: issue
    author: "a-lang"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10833"
    title: "Issue #10833: Public kernel LPE targeting Omarchy (vxlan FDB flush UAF)"
    kind: issue
    author: "alvarofraguas"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/6189"
    title: "Issue #6189: RC pacman mirror is stale since May 23"
    kind: issue
    author: "pvellacott"
    date: "2026-07-08"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
credits:
  - name: "a-lang"
    url: "https://github.com/a-lang"
    for: "Documented that a stale mirror makes pacman report the databases up to date instead of failing"
  - name: "JohnAtl"
    url: "https://github.com/JohnAtl"
    for: "Measured the frozen stable mirror against an actively exploited Chromium fix"
  - name: "alvarofraguas"
    url: "https://github.com/alvarofraguas"
    for: "Tracked which kernel release closes the vxlan LPE used against Omarchy"
faq:
  - q: "Is the stable mirror really a month behind?"
    a: "The omarchy-mirror README says it typically runs one month behind and may be updated sooner for security or release reasons. Measured on 2026-09-17 it was 9 days behind Arch, because the lag you feel is the time since the last resync, not a fixed rolling window."
  - q: "Does the lag also delay Omarchy's own releases and its kernel?"
    a: "No. Omarchy's own packages come from pkgs.omarchy.org, which is separate from the Arch mirror. On 2026-09-17, two days after the 4.0.4 release, the stable Omarchy repo already carried omarchy 4.0.4-1 and linux-omarchy 7.2.5-3."
  - q: "Can I pull just one package from the edge mirror?"
    a: "Do not. Mixing one newer package into a frozen package set is a partial upgrade, which Arch does not support and which can break glibc-linked software. Switch the whole channel or wait for the resync."
  - q: "Is the RC channel a middle ground between stable and edge?"
    a: "No. On issue #6189 DHH said the RC mirror is only kept current when a release is pending. On 2026-09-17 the RC mirror databases were a day older than stable's."
related: [is-omarchy-safe, development-practices-and-ai-written-code]
draft: false
---

Omarchy's stable channel does not track Arch. It tracks a snapshot of Arch that gets refreshed when the Omarchy team decides to refresh it. That is intentional, and it is the main reason stable installs rarely break. It is also the reason a patched browser or kernel can sit in Arch for a week while your machine keeps running the vulnerable build.

This page was checked against Omarchy 4.0.4 on 2026-09-17.

## Two servers, only one of them lags

Omarchy pulls packages from two different places, and people confuse them constantly.

`pkgs.omarchy.org/<channel>/` holds Omarchy's own packages: `omarchy`, `omarchy-settings`, `omarchy-keyring`, and the `linux-omarchy` kernel that 4.0.4 installs and makes the default boot entry. It is configured in `/etc/pacman.conf` as the `[omarchy]` repo. It moves with the release cadence and it is not the slow part.

`stable-mirror.omarchy.org` (or `rc-mirror` or `mirror`, depending on your channel) holds Arch's `core`, `extra` and `multilib`. It is configured in `/etc/pacman.d/mirrorlist`. This is the one that lags, and it is where Chromium, Firefox, OpenSSL, ffmpeg and every other Arch package comes from.

So a stable machine can be fully current on Omarchy itself while being a week or two behind on the actual attack surface.

## What the lag measured on 2026-09-17

All timestamps below were collected at about 15:00 UTC on 2026-09-17 from the mirrors' own `Last-Modified` headers on `extra.db`, compared against Arch's `geo.mirror.pkgbuild.com`.

| Mirror | `extra.db` last modified | Behind Arch |
| --- | --- | --- |
| stable-mirror.omarchy.org | 2026-09-08 18:23 UTC | about 9 days |
| rc-mirror.omarchy.org | 2026-09-07 17:54 UTC | about 10 days |
| mirror.omarchy.org (edge) | 2026-09-17 13:23 UTC | current |
| geo.mirror.pkgbuild.com | 2026-09-17 14:16 UTC | reference |

Concrete version gaps between stable and edge on the same day:

- `chromium` 152.0.7977.82-1 on stable, 153.0.8010.36-1 on edge
- `linux` 7.2.3.arch1-3 on stable, 7.2.6.arch2-1 on edge
- `linux-firmware` 20260810-2 on stable, 20260910-2 on edge
- `openssl` 3.6.4-1 on both, so not everything drifts

Across the whole repo, 2,658 of the 14,948 `extra` packages present on both mirrors were at an older version on stable, plus 52 of 297 in `core`. About 1,150 of the `extra` gaps are pkgrel-only rebuilds rather than new upstream versions, so the raw count overstates what you would notice, but it does not overstate the browser and kernel gaps above.

Note the shape of this. The `omarchy-mirror` README says the stable mirror "typically runs one month behind the very latest" and may be updated sooner for security or general releases. The numbers do not look like a rolling one month offset. They look like the mirror taking a near current snapshot of Arch and then freezing until someone resyncs it, so your real exposure equals the time since the last resync. That is an inference from the dated syncs in #6189, #9064 and #10732 plus this measurement, not stated policy. It was 14 days between the 2026-08-25 and 2026-09-08 syncs, and 9 days at the time of this measurement.

## The Chromium case

Issue [#10732](https://github.com/omacom/omarchy/issues/10732), opened 2026-09-07 by JohnAtl, is the clearest example. The stable mirror was still serving the 2026-08-25 snapshot. Arch had published `chromium 152.0.7977.82-1` on 2026-09-03, a release Google described as fixing a V8 type confusion for which an exploit existed in the wild, tracked as CVE-2026-85046. Chromium is listed in `install/omarchy-base.packages`, so this was the default browser on every stable install.

The issue points out that the manual's Security chapter says Arch security fixes are quickly available through the update flow, while the Updates chapter says the stable mirror runs a month behind, and that both cannot be true for a browser zero day.

The mirror resynced on 2026-09-08, and as of 2026-09-17 stable does carry 152.0.7977.82-1. The immediate gap closed. The issue is still open, because the request was for a stated policy on fast tracking security updates, not just one resync.

Issue [#9064](https://github.com/omacom/omarchy/issues/9064), opened 2026-08-30 by a-lang, adds the detail that makes this hard to notice. pacman compares the mirror's database timestamp with its local copy and skips the fetch when nothing is newer, so a frozen mirror produces a clean, successful, reassuring "up to date" during `omarchy update`. Nothing warns you.

## The kernel case, and why 4.0.4 changes it

Issue [#10833](https://github.com/omacom/omarchy/issues/10833) tracks a public local privilege escalation exploit aimed at Omarchy that races a vxlan FDB flush use after free in the Linux kernel. The reporter is clear that it is an upstream kernel bug, not an Omarchy bug, and says the backported fix lands in kernel 7.2.5 and 7.1.12.

On 2026-09-17 the stable Arch mirror still had `core/linux` at 7.2.3.arch1-3, short of that. But 4.0.4, released 2026-09-15, makes `linux-omarchy` the default boot kernel, and `linux-omarchy` ships from `pkgs.omarchy.org`, where the stable channel was at 7.2.5-3. So a 4.0.4 machine on the default kernel is on a 7.2.5 base while the Arch mirror's `linux` is not. Version numbers are what was verified here, not patch contents.

The general lesson is worth keeping: on 4.0.4 the packages that matter most are split across two feeds with different freshness, so check both.

## How to check what your channel is missing

Find your channel and mirror:

```bash
omarchy-channel-current
omarchy-version-channel
```

`omarchy-version-channel` prints the Arch mirror and the Omarchy repo separately, and shows them as `mirror / pkgs` when they disagree, which is exactly the state you want to catch.

Check how stale your mirror is:

```bash
curl -s https://stable-mirror.omarchy.org/lastupdate | xargs -I{} date -d @{}
curl -s https://geo.mirror.pkgbuild.com/lastupdate | xargs -I{} date -d @{}
```

On the stable mirror `/lastupdate` can sit about a day behind the databases themselves (it read 2026-09-07 16:43 UTC while `extra.db` was stamped 2026-09-08 18:23 UTC), so the `Last-Modified` header in the next command is the figure to trust.

Check a specific package against Arch:

```bash
pacman -Si chromium | grep '^Version'
curl -sI https://stable-mirror.omarchy.org/extra/os/x86_64/extra.db | grep -i last-modified
```

Then compare with the package page on archlinux.org.

For a CVE view of what is actually installed, `arch-audit` is in `extra` on all three mirrors. It checks your installed versions against the Arch Security Tracker:

```bash
sudo pacman -S arch-audit
arch-audit -u
```

Treat its output as a starting point. It reports advisories Arch has recorded, so a fix that has not been assigned a CVE, like the vxlan issue in #10833, will not show up.

## How to switch channels

Switching is a supported operation, not a hack:

```bash
omarchy-channel-set edge     # latest Arch, hourly sync, and Omarchy dev packages
omarchy-channel-set stable   # back to the frozen snapshot
```

The same thing lives under Update, Channel in the Omarchy menu. Under the hood `omarchy-refresh-pacman` replaces `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist` with the channel defaults, backs up the originals as `.bak`, and runs `pacman -Syyuu`.

Three things to know before you do it.

Do not cherry pick. Pointing at the edge mirror and installing one package is a partial upgrade. Arch does not support it, and it is a good way to break everything linked against a newer glibc. Switch the channel or wait.

Going back downgrades. The `-uu` in that pacman call means returning to stable will downgrade packages that are newer than the snapshot. That usually works, and occasionally a downgraded package leaves behind config or database state it cannot read. Take a snapshot first, see [before you update](/upgrade/before-you-update-checklist/) and [rollback with snapper and limine](/upgrade/rollback-with-snapper-and-limine/).

Edge is a real commitment. The manual says edge is for people experienced enough to recover a broken system, and `omarchy-channel-set edge` also moves you to the `omarchy-dev` packages, not just newer Arch. It is not a security channel, it is a testing channel that happens to be fresher.

RC is not the middle ground people assume. On issue [#6189](https://github.com/omacom/omarchy/issues/6189), DHH replied that the RC mirror is only kept up to date when a release is pending and that users should normally be on stable. That matched the measurement above, where RC was slightly older than stable.

## What to watch for on newer versions

Two things could change this page in the next release.

The split between `pkgs.omarchy.org` and the Arch mirror is new enough that more packages may migrate into the Omarchy repo, the way the kernel did in 4.0.4. Every package that moves gets faster updates and leaves the mirror lag behind.

And the ask in #10732 was for a stated security resync policy. If one appears in the [Updates](https://omarchy.org/manual/updates/) or [Security](https://omarchy.org/manual/security/) manual chapters, the numbers here stop being the best available answer. Until then, measure your own mirror rather than trusting the one month figure.

## Related

- [Is Omarchy safe to use?](/security/is-omarchy-safe/)
- [Development practices and AI written code](/security/development-practices-and-ai-written-code/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
