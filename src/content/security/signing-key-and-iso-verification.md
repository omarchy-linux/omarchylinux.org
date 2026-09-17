---
title: "Verify an Omarchy ISO: signing key, .sha256 and .sig files"
description: "How to verify an Omarchy ISO: the pkgs@omarchy.org signing key fingerprint, the .sha256 and .sig sidecar files, and commands for Linux, macOS and Windows."
answer: "Download the .sha256 and .sig files that sit next to the ISO on iso.omarchy.org, run sha256sum -c, then gpg --verify against key 40DFB630FF42BCFFB047046CF0134EE680CAC571. Only 4.0.1 and newer ship a .sha256 file. Most 3.x ISOs and every 4.0.x ISO have a .sig, but a few, including 3.8.0, 3.8.2 and 3.8.4, have neither, so for those compare against the SHA256 line in the GitHub release notes."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: info
reported: "Requested in discussion #1501 (2025-09-08) and discussion #4545 (2026-02-08)"
projectResponse: "The manual publishes one signing key fingerprint for ISOs and repo packages, and every release that ships an ISO has carried a SHA256 line in its GitHub release notes since v3.0.2."
tags: [security, iso, verification, gpg, checksum, signing-key]
sources:
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://keys.openpgp.org/search?q=pkgs%40omarchy.org"
    title: "keys.openpgp.org: Omarchy <pkgs@omarchy.org>"
    kind: docs
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    author: "ryanrhughes"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/discussions/1501"
    title: "Discussion #1501: Omarchy ISO Checksum"
    kind: discussion
    author: "ebcagadas"
    date: "2025-09-08"
  - url: "https://github.com/omacom/omarchy/discussions/4545"
    title: "Discussion #4545: Add checksum and signature info for ISO downloads"
    kind: discussion
    author: "j13k"
    date: "2026-02-08"
  - url: "https://github.com/omacom/omarchy/issues/5231"
    title: "Issue #5231: SHA256 checksum mismatch for omarchy-3.5.0.iso"
    kind: issue
    author: "rjltrevisan"
    date: "2026-04-05"
  - url: "https://github.com/omacom/omarchy/issues/9199"
    title: "Issue #9199: omarchy repo signing key exists in keyring but SigLevel still Optional TrustAll (follow-up to #2712)"
    kind: issue
    author: "drneb99"
    date: "2026-08-30"
credits:
  - name: "EFrMG"
    url: "https://github.com/EFrMG"
    for: "Pointed to the manual's signing key section when the ISO verification question came up"
  - name: "ayuxsec"
    url: "https://github.com/ayuxsec"
    for: "Reported that the .sig URL for 3.8.2 returns page not found"
  - name: "rjltrevisan"
    url: "https://github.com/rjltrevisan"
    for: "Reported that the served 3.5.0 ISO had stopped matching the SHA256 in its release notes, which surfaced the respin"
faq:
  - q: "What is the Omarchy signing key fingerprint?"
    a: "40DFB630FF42BCFFB047046CF0134EE680CAC571, an ed25519 key with the user ID Omarchy <pkgs@omarchy.org> created on 2025-08-28. The same key signs ISO releases and Omarchy repo packages."
  - q: "Why does https://iso.omarchy.org/omarchy-3.8.4.iso.sha256 return 404?"
    a: "Checksum files only exist for 4.0.1 and newer, and 3.8.4 has no .sig either. For 3.8.4 and older, take the SHA256 from that version's GitHub release notes and compare it yourself, and verify the .sig when one exists."
  - q: "Is a SHA256 check enough on its own?"
    a: "It proves the file is intact, not that it came from the project. The checksum file sits on the same server as the ISO. The signature is the part an attacker cannot fake without the private key, so verify the signature too when a .sig exists."
  - q: "Does gpg saying the key is not certified mean verification failed?"
    a: "No. That warning just means you have not personally signed the key in your own keyring. What matters is the Good signature line and the primary key fingerprint matching the one the manual publishes."
related: [is-omarchy-safe, stable-mirror-lag-and-cves]
draft: false
---

The Omarchy ISO is about 6 GB, it is served from a CDN, and it installs an operating system on your machine. Verifying it takes two minutes. This page covers what is actually published, checked against v4.0.4 on 2026-09-16.

Two separate checks are available:

- **SHA256** tells you the file downloaded intact and matches the bytes the project published.
- **OpenPGP signature** tells you the file was signed by the Omarchy key, which is the check an attacker who controls the download server cannot fake.

Do both when both are available. See [how to verify a download](/verify/) for the short version.

## The fix

### 1. Know the key

The manual's [Security chapter](https://omarchy.org/manual/security/) publishes one fingerprint for both ISO signatures and Omarchy repo packages:

```
40DFB630FF42BCFFB047046CF0134EE680CAC571
```

Fetched from keys.openpgp.org on 2026-09-16, that key is an ed25519 key created 2025-08-28 with the user ID `Omarchy <pkgs@omarchy.org>`. You can look it up yourself at [keys.openpgp.org](https://keys.openpgp.org/search?q=pkgs%40omarchy.org).

### 2. Get the sidecar files

Both live next to the ISO, same filename plus a suffix:

```bash
curl -fLO https://iso.omarchy.org/omarchy-4.0.4.iso.sha256
curl -fLO https://iso.omarchy.org/omarchy-4.0.4.iso.sig
```

The `.sha256` file is one plain `sha256sum` line. For 4.0.4 it reads:

```
ddeded2758c48318d201dfdac905ecb28f570441883f0c052ea3cd5d05acf92d  omarchy-4.0.4.iso
```

The `.sig` file is a binary detached OpenPGP signature, roughly 120 bytes. There is no ASCII armored `.asc` variant, and there is no combined `SHA256SUMS` file. Both return 404.

### 3. Verify on Linux

Run this in the directory holding the ISO and both sidecars:

```bash
sha256sum -c omarchy-4.0.4.iso.sha256
gpg --keyserver keys.openpgp.org --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
gpg --verify omarchy-4.0.4.iso.sig omarchy-4.0.4.iso
```

If you are already on Omarchy 4.x, the same key should be in the pacman keyring rather than your personal one. The `omarchy-keyring` package carries it, and `omarchy-update-keyring` in the 4.0.4 tree fetches and locally signs this exact fingerprint before installing that package if either is missing. You can confirm it there as well:

```bash
sudo pacman-key --list-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
```

### 4. Verify on macOS

macOS has `shasum` built in. Install GnuPG for the signature part with `brew install gnupg`.

```bash
shasum -a 256 -c omarchy-4.0.4.iso.sha256
gpg --keyserver keys.openpgp.org --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
gpg --verify omarchy-4.0.4.iso.sig omarchy-4.0.4.iso
```

### 5. Verify on Windows

PowerShell can do the checksum with no extra software:

```powershell
(Get-FileHash .\omarchy-4.0.4.iso -Algorithm SHA256).Hash.ToLower() -eq (Get-Content .\omarchy-4.0.4.iso.sha256).Split()[0]
```

That prints `True` on a match. If you prefer to eyeball it, `certutil -hashfile omarchy-4.0.4.iso SHA256` works in cmd.exe. `Get-FileHash` returns uppercase hex and the published checksum is lowercase, so compare case insensitively.

For the signature, install [Gpg4win](https://gpg4win.org/), then in a terminal:

```powershell
gpg --keyserver keys.openpgp.org --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
gpg --verify omarchy-4.0.4.iso.sig omarchy-4.0.4.iso
```

## Verify it worked

The checksum check prints the filename followed by `OK`. Anything else, including `FAILED`, means stop and re-download.

The signature check prints a `Good signature from "Omarchy <pkgs@omarchy.org>"` line. On a key you have not locally signed, gpg also prints the primary key fingerprint as part of the trust warning below it. Confirm it matches character for character:

```
Primary key fingerprint: 40DF B630 FF42 BCFF B047  046C F013 4EE6 80CA C571
```

gpg will also warn that the key is not certified with a trusted signature. That is normal and expected. It means you have not built a trust path to the key in your own keyring, not that the signature is bad. If you want the warning gone, run `gpg --lsign-key 40DFB630FF42BCFFB047046CF0134EE680CAC571` after you have checked the fingerprint against the manual.

As a third data point, every release that ships an ISO has put the ISO's SHA256 directly in its GitHub release notes since v3.0.2, on a different host from the download. Only v3.0.0 lacks one. Hotfix releases such as 3.7.1 and 3.8.1 have no ISO and no hash. For 4.0.4 the release notes hash matches the `.sha256` sidecar exactly. Cross-checking those two is cheap and worth doing.

## Why it happens

Sidecar coverage is uneven, and this trips people up. Checked by HEAD request on 2026-09-16:

| Release | `.sig` | `.sha256` |
| --- | --- | --- |
| 3.0.0 through 3.5.0, except 3.1.6 | yes | no |
| 3.5.0-2 respin, 3.5.1, 3.6.0 | no | no |
| 3.7.0 | yes | no |
| 3.8.0, 3.8.2, 3.8.4 | no | no |
| 3.8.3, 4.0.0 | yes | no |
| 4.0.1 through 4.0.4 | yes | yes |

Releases 3.3.3, 3.7.1 and 3.8.1 were hotfixes with no ISO, so their URLs return 404 across the board.

So checksum files are a 4.0.1 and later feature, and signature coverage across 3.x has holes. Someone hit exactly this in [discussion #1501](https://github.com/omacom/omarchy/discussions/1501) when the `.sig` for 3.8.2 returned page not found. That discussion, opened in September 2025, and [discussion #4545](https://github.com/omacom/omarchy/discussions/4545) from February 2026 are both requests for published checksums and signatures. A reply in #4545 quoted the manual's signing key section, which is where the fingerprint is published.

The other thing worth knowing is that an ISO can be respun under the same version number. In [issue #5231](https://github.com/omacom/omarchy/issues/5231), the file served for 3.5.0 stopped matching the SHA256 in the release notes. DHH replied in the thread that a re-release had changed the hash and pointed users at a `-2` suffixed filename. That respun file is still served today. The lesson is that a mismatch is not automatically an attack, but it is always a reason to stop, check the release notes and the [release history](/releases/), and not write the image to a stick.

One more note on the same key. The manual says the `omarchy/omarchy-keyring` package carries it for package signing too. The `pacman-stable.conf` shipped with 4.0.0 and 4.0.1 set `SigLevel = Optional TrustAll` on the `[omarchy]` repo, so pacman never demanded a signature from it. 4.0.2 dropped that line, so fresh 4.0.2 and newer installs inherit `SigLevel = Required DatabaseOptional` from the global options, and it added a migration that deletes the override from an existing `/etc/pacman.conf` once the key is in the pacman keyring. The Quattro upgrade script in the 4.0.4 tree still writes the override when it rewrites the repo section, but the same script runs the migrations before it finishes, which removes it again. [Issue #9199](https://github.com/omacom/omarchy/issues/9199), filed from a 4.0.1 machine on 2026-08-30, reports the override still in place and is open as of 2026-09-16. Checked against the 4.0.0 through 4.0.4 source trees. That affects packages, not the ISO, but it is the same key.

## If that did not work

**The checksum does not match.** Most of the time this is a truncated or resumed download rather than tampering. The 4.0.4 ISO is 6185304064 bytes. Check the size first, then re-download with a client that handles resume properly. One user in issue #5231 posted a wget log with a TLS read error and retries partway through a multi gigabyte pull. If the size is right and the hash is still wrong, compare against the release notes hash before concluding anything.

**gpg says "Can't check signature: No public key".** The `--recv-keys` step did not land. Retry it, or fetch the key over HTTPS instead:

```bash
curl -fsSL "https://keys.openpgp.org/vks/v1/by-fingerprint/40DFB630FF42BCFFB047046CF0134EE680CAC571" | gpg --import
```

**gpg says "no valid OpenPGP data found".** You probably saved an HTML error page instead of the signature. Check the file size. A real `.sig` is small and binary. Re-download with `curl -f` so a 404 fails loudly instead of writing the error body to disk.

**There is no .sig or .sha256 for your version.** A missing `.sha256` is expected below 4.0.1. A missing `.sig` happens on a handful of 3.x releases, listed in the table above. Either way, use the SHA256 line from that version's GitHub release notes, and prefer downloading a 4.0.x release instead if you have the choice.

**You want to verify before you download 6 GB.** You cannot. Both checks need the whole file. What you can do is confirm the sidecar and the release notes agree before you start, which takes seconds.

## Related

- [Is Omarchy safe to use?](/security/is-omarchy-safe/)
- [Stable mirror lag and CVEs](/security/stable-mirror-lag-and-cves/)
- [Day one checklist](/switch/day-one-checklist/)
- [How to spot a fake Omarchy site](/official/how-to-spot-a-fake-omarchy-site/)
