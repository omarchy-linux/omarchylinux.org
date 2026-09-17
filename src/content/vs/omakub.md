---
title: "Omarchy vs Omakub: the retired Ubuntu predecessor"
description: "Omakub was DHH's Ubuntu and GNOME setup script, now retired and archived. What it was, why Omarchy replaced it, and the two migration paths."
answer: "Omakub was DHH's one command setup for fresh Ubuntu 24.04 with GNOME. It is retired and its GitHub repos are archived. Omarchy is the successor and a full Arch distro, so moving means a clean ISO install, not an upgrade. If you want to stay on Ubuntu, the community fork Omabuntu continues the Omakub line and ships a migration script."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
other: "Omakub"
otherVersion: "1.5.0"
tags: [omakub, omabuntu, ubuntu, migration, history]
sources:
  - url: "https://omarchy.org/omakub"
    title: "Omakub, the retirement page on omarchy.org"
    kind: docs
    author: "dhh"
  - url: "https://github.com/omacom/omakub"
    title: "omacom/omakub, archived repository"
    kind: other
  - url: "https://github.com/omacom/omakub/discussions/594"
    title: "Discussion #594: Omabuntu, an Omakub continuation inspired by Omarchy"
    kind: discussion
    author: "Kasui92"
    date: "2026-01-26"
  - url: "https://github.com/omacom/omakub/discussions/620"
    title: "Discussion #620: Updated Omakub (Quattro style) for Ubuntu 26.04"
    kind: discussion
    author: "Mikcode"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/discussions/207"
    title: "Discussion #207: No omarchy app like there is an omakub app?"
    kind: discussion
    author: "jomz"
    date: "2025-07-17"
  - url: "https://github.com/omacom/omarchy/discussions/5042"
    title: "Discussion #5042: Support debian as alternative distro base"
    kind: discussion
    author: "alfonsocv12"
    date: "2026-03-17"
  - url: "https://github.com/omakasui/omabuntu"
    title: "omakasui/omabuntu, a fork of Omakub"
    kind: other
    author: "Kasui92"
  - url: "https://omabuntu.omakasui.org/manual/setup/migration/"
    title: "Omabuntu manual: migration from Omakub"
    kind: docs
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-cli/"
    title: "Omarchy manual: Omarchy CLI"
    kind: manual
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
    date: "2026-09-08"
credits:
  - name: "Kasui92 (Luca Pattocchio)"
    url: "https://github.com/Kasui92"
    for: "Maintaining Omabuntu, the Omakub continuation, and writing the Omakub to Omabuntu migration script"
faq:
  - q: "Can I upgrade an Omakub machine to Omarchy in place?"
    a: "No. Omakub was a script layered on Ubuntu, and Omarchy is a full Arch based distribution installed from an ISO. You back up your data and do a clean install. There is no import tool, and the Omarchy 4.0.4 source tree contains no references to Omakub at all."
  - q: "Does the old Omakub install command still work?"
    a: "No. omakub.org now returns a 301 redirect to omarchy.org/omakub, so the old one liner fetches an HTML page instead of a shell script. Piping that into bash installs nothing."
  - q: "What happens to my Omakub machine if I do nothing?"
    a: "It keeps working. Ubuntu still ships its own security updates through apt. Only the Omakub layer itself, meaning its theme files, its app install scripts and its own menu, is frozen. Its last release was v1.5.0 and the last push to its stable branch was in April 2026."
  - q: "Is there an Omarchy style Quickshell desktop for Ubuntu?"
    a: "Not an official one. In discussion #620 in August 2026 someone asked for a Quattro style Omakub on Ubuntu 26.04, and the Omabuntu maintainer replied that it is unlikely because Hyprland and Quickshell are different from GNOME."
related: [debian-ubuntu-mint, forks-and-ports]
draft: false
---

Omakub is the project Omarchy grew out of. It is now retired, its GitHub repositories are archived, and omakub.org redirects to a farewell page at [omarchy.org/omakub](https://omarchy.org/omakub). If you are running Omakub today you have two honest choices: move to Omarchy, which means a clean install of an Arch based distro, or stay on Ubuntu and follow the community fork Omabuntu. There is no upgrade path between the two, because they are not the same kind of thing.

Checked against Omarchy v4.0.4, released 2026-09-15, and Omakub v1.5.0, the last tagged Omakub release, published 2025-11-09.

## What Omakub actually was

Omakub was a shell script, not a distribution. You installed Ubuntu yourself, then ran one command, and it turned a fresh machine into a configured development system. The bootstrap script in the repo is blunt about its requirements. It prints that Omakub is for fresh Ubuntu 24.04 or newer installations only, then clones itself into `~/.local/share/omakub` and runs the installer.

The installer checked the desktop environment before doing anything visual. If `XDG_CURRENT_DESKTOP` did not contain GNOME, it installed the terminal tools and stopped there. That check is the whole story of Omakub in one line. The desktop half was a set of GNOME settings, GNOME extensions, dock and app grid tweaks and a GTK theme. It could only bend GNOME, never replace it.

What it installed is familiar to anyone who has used Omarchy: Alacritty as the terminal, Zellij, Neovim, Docker, mise, lazygit, lazydocker, btop, fastfetch, the GitHub CLI, plus desktop apps like Chrome, VS Code, Obsidian, LibreOffice, Signal, VLC and LocalSend. It shipped ten themes, including catppuccin, everforest, gruvbox, kanagawa, matte-black, nord, osaka-jade, ristretto, rose-pine and tokyo-night. All ten names still exist in Omarchy 4.0.4, which ships twenty two.

It also had a menu. The `omakub` binary opened a text interface for installing apps, switching themes and running updates. People missed it when they moved. In [discussion #207](https://github.com/omacom/omarchy/discussions/207) from July 2025, a new Omarchy user asked whether there was an Omarchy app like the Omakub app. There is. On 4.x it is the Omarchy menu on `Super + Space` and the `omarchy` command in a terminal, both documented in the [Omarchy CLI chapter](https://omarchy.org/manual/omarchy-cli/).

## Why Omarchy replaced it

The retirement page gives the reasoning in DHH's own words, and it is short. Omakub showed there was demand: tens of thousands of developers installed it. It also showed the limit of the approach. Ubuntu and GNOME each have their own design goals, and a script sitting on top of them could only push so far. The things DHH wanted most, a tiling desktop, keyboard control of everything and a terminal at the centre, needed a base that was built for them rather than one that tolerated them. Hence Arch instead of Ubuntu and Hyprland instead of GNOME, and hence a full distribution instead of a script. The page closes with the line that Omakub walked so Omarchy could run.

That is the practical difference too. Omarchy ships an ISO. You install it as your operating system, with full disk encryption by default, as described in the manual chapter on [getting started](https://omarchy.org/manual/getting-started/). It owns the compositor, the shell, the lock screen and the system update path. Omakub owned none of those.

## Path one: move to Omarchy

There is no migration tool. A grep of the Omarchy v4.0.4 source tree finds no mention of Omakub anywhere. Plan a clean install:

1. Back up your home directory, your SSH keys, your GPG keys and any Docker volumes you care about. The `~/.local/share/omakub` directory is only a clone of the installer repository, so nothing of yours lives there.
2. Note your app list. Most Omakub apps exist in Omarchy, but the package names and install method differ, because you are moving from apt and snap to pacman, the AUR and Flatpak.
3. Install Omarchy from the ISO at [omarchy.org](https://omarchy.org) and verify the download first. See [/verify/](/verify/).
4. Expect the desktop to be unfamiliar. Tiling is the default, and the GNOME muscle memory does not carry over. Start with [/switch/tiling-window-manager-survival/](/switch/tiling-window-manager-survival/) and [/switch/day-one-checklist/](/switch/day-one-checklist/).

One thing to know before you read old tutorials. Omarchy 4.0.0 "Quattro", released 2026-08-14, replaced Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle, swaybg and polkit-gnome with a single Quickshell based shell, and moved Hyprland configuration from `~/.config/hypr/*.conf` to Lua files. Anything written for Omarchy 3.x, which ended at v3.8.4, describes a different config layout. See [/reference/hyprland-conf-to-lua-migration/](/reference/hyprland-conf-to-lua-migration/).

## Path two: stay on Ubuntu with Omabuntu

If Arch is a step too far, the retirement page points at Omabuntu, a community fork that continues the Ubuntu line. It is maintained by Luca Pattocchio, who posts as Kasui92, and who also wrote the last functional change merged into Omakub itself, a Spotify GPG key fix authored in February 2026 and merged that March.

Omabuntu is not an Omarchy port. It is still Ubuntu and GNOME, taking selected ideas from Omarchy where they fit. The project announced itself in [discussion #594](https://github.com/omacom/omakub/discussions/594) on the Omakub repo in January 2026, and it publishes a migration route for existing Omakub machines:

```bash
wget -qO- https://omabuntu.omakasui.org/migrate | bash
```

The migration script requires an existing `~/.local/share/omakub` directory, runs an apt update and upgrade, then backs your current setup up to a timestamped `~/.local/share/omakub-backup-<date>` directory and repoints the install at the Omabuntu repository. The Omabuntu manual says the process is not designed to be reversible and asks for roughly 5 GB of free space for the backup, so take your own backup first. A reboot is required afterwards.

If you would rather start clean on Ubuntu 24.04, the fresh install command is `wget -qO- https://omabuntu.omakasui.org/install | bash`. As with any pipe to bash, read the script before you run it.

## Things people get wrong

The old install command is dead. `https://omakub.org/install` now follows a 301 redirect to the Omarchy retirement page and returns HTML, not a script. Piping it into bash does nothing useful.

Nothing suggests Omarchy will gain an Ubuntu or Debian base. The request comes up, for example in [discussion #5042](https://github.com/omacom/omarchy/discussions/5042) from March 2026 asking for Debian as an alternative base. As of 2026-09-16 that discussion has no accepted answer, and nothing in the 4.0.4 tree supports a non Arch base.

Omakub is not unsafe to keep running. Ubuntu still patches Ubuntu. What is frozen is the Omakub layer, at v1.5.0, with the last merge into its default branch on 2026-03-07 and a final push to its stable branch on 2026-04-03. The archived repository still had 8,094 stars and 800 forks when checked on 2026-09-16.

## What to watch for on newer versions

DHH said on X on 2026-09-08 that the next Omarchy release will be called "Quattro RS 4.5" rather than 4.1. Nothing announced for it changes the Omakub story, since the two projects no longer share code, but it is likely to move more configuration around, so prefer current pages over old blog posts and videos.

On the Ubuntu side, watch which Ubuntu release Omabuntu targets. Its documentation currently names Ubuntu 24.04. In [discussion #620](https://github.com/omacom/omakub/discussions/620) from August 2026, someone asked whether Omakub would be updated with the Quattro look and made compatible with Ubuntu 26.04. The Omabuntu maintainer replied that a Quickshell style desktop on GNOME is unlikely, and pointed at Omabuntu for the closest thing available.

## Related

- [What replaces what when you switch](/switch/what-replaces-what/)
- [Omarchy vs Debian, Ubuntu and Mint](/vs/debian-ubuntu-mint/)
- [Forks and ports of Omarchy](/vs/forks-and-ports/)
- [Upgrading 3.x to 4.x Quattro](/upgrade/3-to-4-quattro/)
