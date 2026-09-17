---
title: "How to spot a fake Omarchy site or download"
description: "Check the domain, the download, and the signature. The omarchy.net clone, the real download source, the signing key, and the red flags that give a fake away."
answer: "Only omarchy.org and its subdomains, plus github.com/omacom, are the project's own. Omarchy ships as an ISO from iso.omarchy.org with a .sha256 and a .sig next to it, signed by key 40DFB630FF42BCFFB047046CF0134EE680CAC571. A ZIP, an installer EXE, or a paste-this-script line on any other domain is a fake."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [security, phishing, downloads, domains, verification]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/6160"
    title: "Discussion #6160: Likely impersonation at omarchy[.]net"
    kind: discussion
    author: "Arusekk"
    date: "2026-07-02"
  - url: "https://github.com/omacom/omarchy/discussions/8054"
    title: "Discussion #8054: omarchy.net"
    kind: discussion
    author: "treeshateorcs"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/discussions/8211"
    title: "Discussion #8211: Spam site - https://omarchy.net -"
    kind: discussion
    author: "zekola"
    date: "2026-08-25"
  - url: "https://x.com/dhh/status/2092142632449212581"
    title: "DHH: warning that omarchy.net is not legitimate"
    kind: other
    author: "dhh"
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy Manual: Getting Started"
    kind: manual
  - url: "https://omarchy.org/"
    title: "omarchy.org, the official site and download page"
    kind: docs
  - url: "https://keys.openpgp.org/search?q=pkgs%40omarchy.org"
    title: "keys.openpgp.org: Omarchy <pkgs@omarchy.org>"
    kind: docs
  - url: "https://github.com/omacom/omarchy"
    title: "omacom/omarchy, the official repository"
    kind: docs
  - url: "https://omarchy.io/"
    title: "omarchy.io, a tribute page offering the domain for sale"
    kind: other
credits:
  - name: "Arusekk"
    url: "https://github.com/Arusekk"
    for: "Filed the impersonation report with whois data and side by side screenshots"
  - name: "dakotahp"
    url: "https://github.com/dakotahp"
    for: "Spotted that the clone served a random ZIP instead of linking the real project"
  - name: "farangkao"
    url: "https://github.com/farangkao"
    for: "Pointed out the generated images that gave the clone away"
faq:
  - q: "Is omarchy.net dangerous right now?"
    a: "It does not resolve. The domain sits on registrar clientHold as of 16 September 2026, so DNS returns nothing. Treat any future revival of it as hostile, and do not run anything you downloaded from it earlier."
  - q: "Is a site official just because it uses the Omarchy logo and colors?"
    a: "No. The clone copied the official layout closely enough that people could not tell from the screenshot alone. Design proves nothing. The domain and the signature on the download are what prove something."
  - q: "Is every unofficial Omarchy site a scam?"
    a: "No. Plenty of community sites, mirrors, and fan redirects exist and are harmless. The line is whether the site hosts its own installer and whether it claims to be the project. A site that links to omarchy.org for downloads is not impersonating anyone."
  - q: "Does Omarchy have a curl install command?"
    a: "Not since 4.0.0. Older 3.x releases had a boot.sh you could pipe from omarchy.org/install onto an existing Arch system. That file is gone from the repository, so the only supported install is booting the ISO."
related: [trademark, naming-your-omarchy-project]
draft: false
---

Three checks settle whether an Omarchy site or download is real. Check the domain, check where the download actually comes from, and check the signature. Design, logos, screenshots, and search ranking prove nothing. A clone of the official site was ranking second on Bing when it was reported in July 2026.

## Check 1: the domain

The project owns exactly one web domain and its subdomains.

| What | Where | Notes |
|---|---|---|
| The site, manual, news, themes, plugins | `omarchy.org` and subdomains | Includes `iso.omarchy.org` and `plugins.omarchy.org` |
| The source code | `github.com/omacom` | The old `basecamp/omarchy` address and repositories under the earlier `omacom-io` organisation redirect here |
| The manual mirror | `learn.omacom.io` | Named as a mirror in the repository README |

Anything else is not the project, whatever it looks like. Some of the rest is harmless. `omarchylinux.com` redirects to `omarchy.org` and hosts nothing of its own. `omarchyplugins.com`, which the 4.0.0 release notes linked as the plugin ecosystem, now redirects to `plugins.omarchy.org`, and the marketplace repository lives under `github.com/omacom`. `omarchy.com` is a parked domain. `omarchy.io` is a one page tribute that offers the domain free to the maintainers and for ten thousand dollars to anyone else. None of those ask you to download anything, which is the point.

## Check 2: where the download comes from

Omarchy ships as one thing: an ISO you write to a USB stick and boot. As of 4.0.4 the download on the front page is `iso.omarchy.org/omarchy-4.0.4.iso`, with two sidecar files next to it at the same path, a `.sha256` and a `.sig`. The manual's [Getting Started](https://omarchy.org/manual/getting-started/) chapter describes no other install route.

There is no ZIP. There is no installer executable. There is no torrent, no Google Drive link, no Mega link, and no "download manager". If a site offers any of those, you are not on the project's site.

Since 4.0.0 there is also no curl install command. In 3.x, `omarchy.org/install` returned a one liner that piped `boot.sh` from the repository onto an existing Arch system. That URL still returns the same one liner today, but the file it points at is gone: the repository has no `master` branch any more, the default branch is `quattro`, and `boot.sh` exists at the `v3.8.4` tag but at no 4.x tag, so the inner fetch 404s and the command does nothing. Checked 16 September 2026 against 4.0.4. Treat any page that gives you a fresh looking `curl ... | bash` line for Omarchy as a fake, because the project does not have a working one.

## Check 3: the signature

The signature is the only check that a copied design cannot fake. The manual publishes one fingerprint for both ISO signatures and Omarchy repository packages:

```
40DFB630FF42BCFFB047046CF0134EE680CAC571
```

Verify it yourself rather than trusting a fingerprint printed on a web page:

```bash
gpg --keyserver keys.openpgp.org --recv-keys 40DFB630FF42BCFFB047046CF0134EE680CAC571
gpg --verify omarchy-4.0.4.iso.sig omarchy-4.0.4.iso
```

Pull the key from the keyserver, not from the site that is offering you the download. A fake page can print any fingerprint it likes.

On 16 September 2026 the published signature for 4.0.4 carries that exact issuer fingerprint and a creation date of 15 September 2026, matching the release. Full commands for Linux, macOS and Windows, plus which older releases are missing a `.sha256` or a `.sig`, are on [signing key and ISO verification](/security/signing-key-and-iso-verification/) and [verify](/verify/).

## The omarchy.net case

This is the one confirmed impersonation, and it is worth knowing in detail because the next one will look the same.

`omarchy.net` was registered on 24 April 2026 through Spaceship. On 2 July 2026, a community member filed [discussion #6160](https://github.com/omacom/omarchy/discussions/6160) with whois output and side by side screenshots of the real and the fake front pages. The report noted the clone ranked second on Bing and therefore on DuckDuckGo, which is how ordinary users would have reached it.

The site looked like an AI generated copy of the official design. One commenter pointed at a generated Neovim screenshot served from a WordPress uploads path as the giveaway. At first it pointed downloads at the real GitHub project, which is what makes this pattern hard to judge early. By 21 August another commenter reported that it had stopped doing that and was serving a ZIP file instead.

Two more reports arrived in August, [#8054](https://github.com/omacom/omarchy/discussions/8054) and [#8211](https://github.com/omacom/omarchy/discussions/8211), both pointed back to #6160 as duplicates. On 25 August, DHH posted a public warning that the domain was not legitimate and looked like a scam, malware or phishing operation, and said Spaceship, the company the domain is registered through, had acknowledged his report but refused to act.

The registrar record changed later that same day. As of today the domain carries `clientHold`, `clientTransferProhibited` and `clientUpdateProhibited`, and it no longer resolves. `clientHold` is the status a registrar sets to pull a domain out of DNS, so the site is dark. The whois record does not say why, and the registration itself does not expire until April 2027.

## Red flags, in order of usefulness

1. **Any download that is not the ISO from `iso.omarchy.org`.** A ZIP, an EXE, an AppImage, a "setup" binary. This is what turned omarchy.net from suspicious into dangerous.
2. **A domain that is not `omarchy.org`.** Especially `.net`, `.com`, `.app`, `.download`, and hyphenated variants.
3. **A `curl | bash` line.** The project has no working one on 4.x.
4. **No signature or checksum anywhere on the page.** The real download page links both next to the ISO.
5. **Generated or subtly wrong screenshots.** Odd fonts in terminal shots, garbled text in menus, stock photos of laptops.
6. **A WordPress footprint**, such as `/wp-content/` paths. The official site is not WordPress.
7. **Urgency or account prompts.** Omarchy asks you to create no account and pay nothing.
8. **A copyright line, team page, or "sponsors" list you cannot corroborate** against `omarchy.org` or the GitHub organisation.

Search ranking is not on that list on purpose. The clone sat second on Bing when it was reported.

## Mirrors and community sites are a separate thing

A third party mirror is not an impersonation. SourceForge, for example, carries a mirror of the repository's source tarballs and says plainly on the page that it is a mirror and that SourceForge is not affiliated with Omarchy. That is honest, and it is also not where you should get an ISO, because the tarball is source code and carries no ISO signature.

The same goes for community documentation, theme galleries, and forks. The test is simple: does the site host its own installer, and does it claim to be the project? A site that answers no to both is a community site, even if it uses the word Omarchy in its domain. See [trademark](/official/trademark/) and [naming your Omarchy project](/official/naming-your-omarchy-project/) for where the name itself sits.

## What to watch for on newer versions

The next release is announced as "Quattro RS 4.5". Two things to re-check when it lands.

The ISO filename and its sidecars follow the version, so the paths change with every release, and older releases are inconsistent about which sidecars exist. Check what the front page of `omarchy.org` actually links rather than typing a URL from memory.

The stale `omarchy.org/install` endpoint is the more interesting one. It still returns a command pointing at a branch and a file that no longer exist. If a future release either restores a real install script there or removes the endpoint, the advice in Check 2 changes, so confirm against the release notes before you run anything that claims to be an Omarchy install command.
