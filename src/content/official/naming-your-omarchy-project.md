---
title: Naming your Omarchy plugin, theme, or site safely
description: The de facto rules for using the Omarchy name in a plugin, theme, fork, meetup, or community site, drawn from what the project has written and what has actually been enforced.
answer: Use "omarchy-<name>" for plugins and themes like the other 3,000 do, put "unofficial" and a one-line disclaimer where people will see it, never use the official logo files, never host or mirror the installer, never imply official status, and never sell merchandise under the name. Nothing else has ever drawn a complaint.
appliesTo: { from: '3.x' }
status: info
lastVerified: 2026-09-16
tags: [trademark, community, plugins, themes]
sources:
  - url: "https://omarchy.org/meetups/"
    title: "Omarchy meetups page"
    kind: docs
  - url: "https://omarchy.org/brand/"
    title: "omarchy.org brand page"
    kind: docs
  - url: "https://github.com/omacom/omarchy/discussions/6160"
    title: "Discussion #6160: Likely impersonation at omarchy.net"
    kind: discussion
  - url: "https://github.com/omacom/omarchy-theme-registry"
    title: "Official theme registry naming convention (omarchy-<name>-theme)"
    kind: docs
  - url: "https://rubyonrails.org/trademarks"
    title: "Ruby on Rails trademark guidelines"
    kind: docs
faq:
  - q: "What disclaimer text should I use?"
    a: "Something like: \"Omarchy is a registered trademark of 37signals LLC. This project is an independent community effort and is not affiliated with or endorsed by 37signals or the Omacom Foundation.\" Put it in the README and, for a website, in the footer of every page."
  - q: "Can I register a domain with omarchy in it?"
    a: "People have, and disclaimed community domains have not been challenged. The domain that was suspended imitated the official design and offered a download. If your site is clearly unofficial and links downloads upstream, you are in the same position as a dozen existing community sites."
---

## Naming patterns that are already normal

- **Plugins and themes:** `omarchy-<name>` and `omarchy-<name>-theme` are the conventions the official registries expect. Thousands of repositories use them.
- **Forks and ports:** armarchy, deckarchy, omarchy-nix, omadora. Portmanteaus and "omarchy-on-<platform>" names are common and unchallenged.
- **Meetups:** "Omarchy <City>" is explicitly fine per the official meetups page.
- **Community sites:** several domains contain the word. The ones that have lasted all carry a disclaimer and link downloads to omarchy.org.

## The lines

1. **Do not imply official status.** No "official", no "the Omarchy site", no claim to speak for the project. The meetups page says this directly.
2. **Do not use the logo or wordmark files.** They are offered on the brand page for partnership use; nothing grants community use.
3. **Do not host installers, ISOs, or mirrors.** The one suspended domain did exactly this. Link to iso.omarchy.org and github.com/omacom.
4. **Do not copy the official design.** The suspended clone used the same look. Make yours obviously different.
5. **Do not sell merchandise under the name.** Official merch exists; the Rails precedent reserves it.
6. **Disclose sponsorships** if you take any money, and do not turn the name into a sales pitch.

## If the Foundation asks

Expect adoption before enforcement: good community projects have been moved into the official organization with their maintainers. If you are asked to rename or hand over a domain, the sensible answer is yes. Building your project as a public repository with a CNAME makes that a ten-minute job.
