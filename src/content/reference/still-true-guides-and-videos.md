---
title: "Is that Omarchy guide still true on 4.x?"
description: "A dated verdict on the most-watched Omarchy videos and cheat sheets, which ones still work on Omarchy 4.0.4, which describe a desktop that is gone."
answer: "Check the publish date against 2026-08-14, the day Omarchy 4.0 Quattro shipped. Anything older describes Waybar, Walker, Mako and hyprland.conf, none of which 4.x ships or loads, and it has Super + Space backwards. Post-4.0 material from NetworkChuck, Chris Titus, pacyfist and the acrogenesis cheat sheet still matches 4.0.4."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [guides, videos, cheat-sheets, quattro, keybindings, documentation]
sources:
  - url: "https://omarchy.org/manual/hotkeys/"
    title: "Hotkeys, the Omarchy Manual"
    kind: manual
  - url: "https://learn.omacom.io/2/the-omarchy-manual/53/hotkeys"
    title: "Hotkeys, The Omarchy 3 Manual"
    kind: docs
    author: "dhh"
  - url: "https://github.com/omacom/omarchy/issues/6933"
    title: "Issue #6933: Quattro update preserves bindings.conf but silently stops loading custom keybindings"
    kind: issue
    author: "evo-social-world"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0"
    kind: release
    date: "2026-08-14"
  - url: "https://www.youtube.com/watch?v=Urq__zOwQqg"
    title: "The Linux Experience - Omarchy"
    kind: video
    author: "Bog"
    date: "2025-09-24"
  - url: "https://www.youtube.com/watch?v=6YJImMYKefk"
    title: "You NEED to try this Linux Setup! (Omarchy for Newbs)"
    kind: video
    author: "typecraft"
    date: "2025-07-30"
  - url: "https://www.youtube.com/watch?v=d23jFJmcaMI"
    title: "You installed Omarchy, Now What?"
    kind: video
    author: "typecraft"
    date: "2025-11-07"
  - url: "https://www.youtube.com/watch?v=9SDkU5VDQEQ"
    title: "You need to switch to Linux RIGHT NOW!!"
    kind: video
    author: "NetworkChuck"
    date: "2026-08-21"
  - url: "https://www.youtube.com/watch?v=2IDjteRQgMQ"
    title: "Omarchy Can Do WHAT?! 50 Features You're Missing"
    kind: video
    author: "NetworkChuck"
    date: "2026-09-05"
  - url: "https://www.youtube.com/watch?v=5cQsIOjW0NY"
    title: "Omarchy - The Best Tiling Window Setup Ever?"
    kind: video
    author: "Chris Titus Tech"
    date: "2025-08-09"
  - url: "https://www.youtube.com/watch?v=9d9PQ1hrhBk"
    title: "Omarchy: Arch Savior or Overhyped Reskin?"
    kind: video
    author: "Chris Titus Tech"
    date: "2026-09-10"
  - url: "https://www.youtube.com/watch?v=lPEHoc3fDlM"
    title: "Omarchy Is Beautiful, Modern and Opinionated"
    kind: video
    author: "DistroTube"
    date: "2025-10-12"
  - url: "https://cheatography.com/dimitrios/cheat-sheets/omarchy-v3-2-2-hotkeys/"
    title: "Omarchy v3.2.2 Hotkeys Keyboard Shortcuts"
    kind: docs
    author: "dimitrios"
    date: "2025-12-03"
  - url: "https://github.com/acrogenesis/omarchy-cheat-sheet"
    title: "acrogenesis/omarchy-cheat-sheet"
    kind: other
    author: "acrogenesis"
    date: "2026-08-17"
  - url: "https://www.pacyfist.dev/posts/omarchy-has-227-shortcuts-heres-how-i-remember-them/"
    title: "Omarchy Has 227 Shortcuts: Here's How I Remember Them"
    kind: blog
    date: "2026-08-15"
  - url: "https://deepwiki.com/basecamp/omarchy"
    title: "DeepWiki: basecamp/omarchy"
    kind: docs
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "Next version of Omarchy is going to be Quattro RS 4.5"
    kind: other
    author: "dhh"
    date: "2026-09-08"
credits:
  - name: "acrogenesis"
    url: "https://github.com/acrogenesis"
    for: "Re-synced the printable hotkey cheat sheet to the Omarchy 4.0 bindings three days after Quattro shipped"
  - name: "evo-social-world"
    url: "https://github.com/evo-social-world"
    for: "Documented that pre-4.0 hypr .conf files stay on disk but stop being loaded"
faq:
  - q: "What is the single fastest way to tell if an Omarchy guide is out of date?"
    a: "Look at what it says Super + Space does. On 3.x it opened the Walker app launcher. On 4.x it opens the Omarchy menu, and the app launcher moved to Super + Alt + Space. A guide that gets that backwards was written before 2026-08-14."
  - q: "Do the 3.x videos still work if I install an older Omarchy?"
    a: "The v3.8.4 ISO is still served from iso.omarchy.org, and a 3.x machine only moves to 4 when you run Update > Omarchy to Quattro, which is one way. So 3.x guides are still accurate on a 3.x install. But the last 3.x release was v3.8.4 on 2026-07-21 and nothing new ships there, so treat that material as history rather than as the path forward."
  - q: "Is the Omarchy 3 Manual on learn.omacom.io still the official manual?"
    a: "No. On 4.x the manual lives in the omacom/omarchy repository under manual/ and is published at omarchy.org/manual/. The learn.omacom.io copy is still titled The Omarchy 3 Manual and still shows the 3.x hotkey table."
  - q: "Are keybindings stable across the 4.0.x point releases?"
    a: "Yes. The default binding file default/hypr/bindings/utilities.lua is byte-identical between v4.0.0 and v4.0.4, so a cheat sheet built against 4.0.0 is still correct on 4.0.4."
related: [hyprland-conf-to-lua-migration]
draft: false
---

Omarchy 4.0 "Quattro" shipped on 2026-08-14. It dropped Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle, swaybg and polkit-gnome from the base package list, added Quickshell as the shell, and moved the Hyprland config from `~/.config/hypr/*.conf` to Lua. That means most of the popular Omarchy tutorial material was recorded against a desktop that no longer exists.

The date is the whole test. Published before 2026-08-14, assume it is wrong about the shell, the config files and the two most-used keys. Published after, assume it is right unless it says otherwise.

## The 30 second date test

Checked against v4.0.4. Read the guide and look for any one of these:

| If the guide says | It was written for |
| --- | --- |
| `Super + Space` opens the app launcher | 3.x |
| `Super + Space` opens the Omarchy menu | 4.x |
| Edit `~/.config/hypr/bindings.conf` or `monitors.conf` | 3.x |
| Edit `~/.config/hypr/bindings.lua` or `monitors.lua` | 4.x |
| Waybar, Walker, Mako, SwayOSD, hyprlock, hypridle | 3.x |
| `omarchy-launch-walker`, `omarchy-restart-waybar`, `omarchy-restart-mako` | 3.x |
| `Super + Ctrl + K` for Herdr keybindings | 4.x |

The swap is real and it is confirmed in the shipped defaults. In v3.8.4, `default/hypr/bindings/utilities.conf` binds `SUPER, SPACE` to `omarchy-launch-walker` and `SUPER ALT, SPACE` to `omarchy-menu`. In v4.0.4, `default/hypr/bindings/utilities.lua` binds `SUPER + SPACE` to the Omarchy menu and `SUPER + ALT + SPACE` to the apps menu. Those are the first two keys any beginner learns, and every 3.x guide teaches them the wrong way round.

The commands are gone too, not renamed. `omarchy-launch-walker`, `omarchy-launch-wifi`, `omarchy-launch-audio`, `omarchy-launch-bluetooth`, `omarchy-refresh-waybar`, `omarchy-restart-waybar`, `omarchy-restart-mako`, `omarchy-restart-swayosd` and `omarchy-refresh-hyprlock` are all present in v3.8.4's `bin/` and absent from v4.0.4's.

## The dated table

View counts read on 2026-09-16 and will drift.

| Resource | Published | Verdict | What broke, and what to use instead |
| --- | --- | --- | --- |
| Bog, "The Linux Experience - Omarchy" (~1.35M views) | 2025-09-24 | Describes a desktop that no longer exists | Published eleven months before Quattro, so the desktop it shows is the Waybar and Walker one. Still fine as a reason to try Omarchy, useless as instructions. No Omarchy follow-up in the channel feed as of 2026-09-16. |
| typecraft, "You NEED to try this Linux Setup! (Omarchy for Newbs)" (~257k) | 2025-07-30 | Describes a desktop that no longer exists | Pre-dates even Omarchy 2. Install flow and hotkeys both moved. Start at [omarchy.org/manual/hotkeys/](https://omarchy.org/manual/hotkeys/). |
| typecraft, "You installed Omarchy, Now What?" (~194k) | 2025-11-07 | Partly | Published nine months before Quattro. Keeping your own dotfiles and overriding the defaults instead of editing them is still the right idea. The paths are not. Anything it has you put in `~/.config/hypr/*.conf` is dead weight on 4.x; the same overrides belong in `bindings.lua` and its siblings now. |
| NetworkChuck, "You need to switch to Linux RIGHT NOW!!" (~1.9M) | 2026-08-21 | Still works | Published a week after Quattro shipped, so the desktop it shows is the 4.0.x one, and the shipped bindings have not changed since. |
| NetworkChuck, "Omarchy Can Do WHAT?! 50 Features You're Missing" (~479k) | 2026-09-05 | Still works | Published between the 4.0.2 and 4.0.3 releases. The shipped bindings are identical from 4.0.0 through 4.0.4. |
| Chris Titus Tech, "Omarchy - The Best Tiling Window Setup Ever?" (~146k) | 2025-08-09 | Describes a desktop that no longer exists | 3.x era walkthrough. Superseded by the same channel's 2026 video below. |
| Chris Titus Tech, "Omarchy: Arch Savior or Overhyped Reskin?" (~210k) | 2026-09-10 | Still works | Published two days after 4.0.3. The title frames it as a verdict rather than a walkthrough, so take the opinion and get the how-to from the manual. |
| DistroTube, "Omarchy Is Beautiful, Modern and Opinionated" (~108k) | 2025-10-12 | Describes a desktop that no longer exists | No Omarchy follow-up in the channel feed as of 2026-09-16. |
| learn.omacom.io, "The Omarchy 3 Manual" | 3.x era | Describes a desktop that no longer exists | Its hotkeys chapter still lists `Super + Space` as "Application launcher". The v4.0.4 README points at this mirror, but the mirror is still titled and written for 3. Use [omarchy.org/manual/](https://omarchy.org/manual/). |
| Cheatography, "Omarchy v3.2.2 Hotkeys" by dimitrios | 2025-12-03, updated 2025-12-05 | Describes a desktop that no longer exists | Version-stamped 3.2.2 and it means it. Points you at `~/.config/hypr/bindings.conf` for edits. |
| acrogenesis/omarchy-cheat-sheet | Re-synced 2026-08-17 | Still works | The maintainer resynced it to the 4.0 hotkeys three days after Quattro. It has the `Super + Space` order right, names Herdr, lists the `Super + Ctrl + Q` calculator, and tells you to edit `~/.config/hypr/bindings.lua`. It does not print a version number anywhere, so the commit history is the only date stamp. |
| pacyfist.dev, "Omarchy Has 227 Shortcuts: Here's How I Remember Them" | 2026-08-15 | Still works | Written the day after Quattro. Teaches the modifier pattern rather than the list, which is why it ages well. |
| DeepWiki, basecamp/omarchy | Last indexed 2026-09-05 | Partly | The overview calls Quickshell the desktop architecture and the Waybar page itself now admits the bar is Quickshell-based, but the navigation still carries "Waybar Status Bar" and "Walker Application Launcher" sections and the theme architecture page still says themes hold config for Waybar and Walker. Treat it as a mixed 3.x and 4.x document. Note it is also still filed under the old `basecamp/omarchy` path, which now redirects to `omacom/omarchy`. |

## Why following an old guide fails quietly

The worst case is not an error message. It is silence. Quattro leaves your old `~/.config/hypr/*.conf` files on disk but stops loading them, so a custom binding copied out of a 3.x tutorial sits in `bindings.conf` doing nothing, with no `hyprctl configerrors` output to explain it. That is [issue #6933](https://github.com/omacom/omarchy/issues/6933), filed on 2026-08-15 and still open on 2026-09-16, with reporters confirming the same orphaning for `envs.conf` and `looknfeel.conf`.

So when a guide says "add this line to bindings.conf", the line will appear to be accepted and will never fire. See [custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/) and [monitors.conf replaced by monitors.lua](/fix/monitors-conf-replaced-by-monitors-lua/).

## Salvaging a 3.x guide

Most 3.x material is still useful if you translate rather than copy.

1. Read the intent, not the command. "Restart the bar" is still a real thing to want, `omarchy-restart-waybar` is not the way to do it.
2. Convert bindings by hand. A 3.x line like `bindd = SUPER, G, Launch app, exec, some-app` becomes `o.bind("SUPER + G", "Launch app", "some-app")` in `~/.config/hypr/bindings.lua`.
3. Check the key against the shipped list. Press `Super + K` for the main bindings, `Super + Alt + K` for tmux, `Super + Ctrl + K` for Herdr. The live list always beats a cheat sheet.
4. Look the topic up in the current manual at [omarchy.org/manual/](https://omarchy.org/manual/) before trusting any third party page.

Related: [upgrading 3 to 4](/upgrade/3-to-4-quattro/), [where did Waybar go](/fix/where-did-waybar-go/), [Walker launcher missing after update](/fix/walker-launcher-missing-after-update/).

## What to watch for on newer versions

Within 4.0.x, guides age well. `default/hypr/bindings/utilities.lua` is byte-identical between v4.0.0 and v4.0.4, so a 4.0.0 cheat sheet is still correct on 4.0.4. The manual moved a little: nine of its 52 chapters changed between 4.0.0 and 4.0.4, including the AI, networking, security and FAQ chapters, so prefer the live manual over a screenshot of it.

DHH has said on X that the next version will be "Quattro RS 4.5" rather than a 4.1. Nothing about its keybindings has been published. When it lands, re-run the date test on this page too: if this page still says the newest release is 4.0.4, it is the thing that is stale.

One thing this page cannot verify: whether any given creator has quietly re-recorded or annotated an old video. Channel feeds were checked on 2026-09-16 and no Omarchy 4 replacement was found for the Bog, typecraft or DistroTube entries, but a pinned comment or a description edit would not show up in that check.
