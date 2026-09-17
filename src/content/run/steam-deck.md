---
title: "Omarchy on the Steam Deck: deckarchy, gaming mode, SteamOS"
description: "What it takes to run Omarchy 4 on a Steam Deck, why the deckarchy Neptune kernel script predates Quattro, and where the gaming mode plugins fit."
answer: "Keep SteamOS on the Deck unless you want a handheld Linux laptop. Omarchy 4 only installs from its ISO, so the deckarchy Neptune kernel script, which is meant to run on a vanilla Arch install before Omarchy, no longer fits the 4.x flow and has not been touched since August 2025. If you want Deck style gaming on an Omarchy desktop instead, use a gaming mode plugin."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Steam Deck"
hostVersion: "LCD (Jupiter) and OLED (Galileo)"
tags: [steam-deck, gaming, gamescope, deckarchy, handheld]
sources:
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/gaming/"
    title: "Omarchy manual: Gaming"
    kind: manual
  - url: "https://github.com/aorumbayev/deckarchy"
    title: "deckarchy: Fix Steam Deck OLED hardware issues after installing Omarchy on a vanilla Arch Linux installation"
    kind: docs
    author: "aorumbayev"
    date: "2025-08-19"
  - url: "https://github.com/cephalization/omarchy-steam-gaming-mode"
    title: "omarchy-steam-gaming-mode: Setup a steam-deck-like gaming experience on your Omarchy install"
    kind: docs
    author: "cephalization"
    date: "2026-07-05"
  - url: "https://github.com/cephalization/omarchy-steam-gaming-mode/pull/4"
    title: "PR #4: fix: support Lua-based Hyprland configs (Omarchy >=0.9)"
    kind: pr
    author: "johtok"
    date: "2026-05-13"
  - url: "https://github.com/cephalization/omarchy-steam-gaming-mode/issues/3"
    title: "Issue #3: Steam Big Picture starts ok but with bad /sluggish performance. Games run fine"
    kind: issue
    author: "ypsilonkah"
    date: "2026-02-05"
  - url: "https://github.com/cephalization/omarchy-steam-gaming-mode/issues/5"
    title: "Issue #5: fix: stop mangoapp before gamescope when leaving with Super+W"
    kind: issue
    author: "Ruegen"
    date: "2026-09-08"
  - url: "https://github.com/28allday/deckshift"
    title: "DeckShift: Steam Deck-style Gaming Mode for Linux + Hyprland (Omarchy)"
    kind: docs
    author: "28allday"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/discussions/840"
    title: "Discussion #840: Running on steam deck (alternate options)"
    kind: discussion
    author: "JaydenIvanovic"
    date: "2025-08-16"
  - url: "https://github.com/omacom/omarchy/discussions/3421"
    title: "Discussion #3421: Support overlaying Omarchy on SteamOS"
    kind: discussion
    author: "nnutter"
    date: "2025-11-15"
  - url: "https://github.com/omacom/omarchy/discussions/4534"
    title: "Discussion #4534: Omarchy STEAM DECK MODE"
    kind: discussion
    author: "28allday"
    date: "2026-02-07"
  - url: "https://github.com/omacom/omarchy/discussions/5143"
    title: "Discussion #5143: Omarchy Steam Deck Mode"
    kind: discussion
    author: "28allday"
    date: "2026-03-28"
  - url: "https://github.com/omacom/omarchy/issues/6947"
    title: "Issue #6947: Steam idle-inhibit rule matches the client but not steam_app games"
    kind: issue
    author: "nicoladen05"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
    date: "2026-09-08"
credits:
  - name: "aorumbayev"
    url: "https://github.com/aorumbayev"
    for: "deckarchy, the Neptune kernel and Deck audio firmware script the Omarchy manual links to"
  - name: "cephalization"
    url: "https://github.com/cephalization"
    for: "The gamescope gaming mode toggle for Omarchy"
  - name: "johtok"
    url: "https://github.com/johtok"
    for: "Teaching the gaming mode script to write Lua keybindings instead of .conf syntax"
  - name: "28allday"
    url: "https://github.com/28allday"
    for: "DeckShift, the gamescope session installer that targets Omarchy 4 directly"
  - name: "phren0logy"
    url: "https://github.com/phren0logy"
    for: "The first report of an unmodified Omarchy install to a Deck microSD card, and the volume up plus power boot menu trick"
faq:
  - q: "Does Omarchy officially support the Steam Deck?"
    a: "No. The manual's Omarchy on... chapter points at one user's script, deckarchy, and says nothing about support or testing. No Valve partnership has been announced, and a request to support overlaying Omarchy on SteamOS is an open suggestion in discussion #3421 with no reply from the project."
  - q: "Will installing Omarchy wipe SteamOS?"
    a: "The Omarchy ISO does a full disk install or a free space install. A full disk install on the Deck's internal drive takes SteamOS with it. The lower risk route is a microSD card, which three people in discussion #840 report working."
  - q: "Can I just get Deck style gaming mode on my normal Omarchy machine?"
    a: "Yes, and that is what most people actually want. Two community projects wrap Steam Big Picture in gamescope and bind it to a hotkey. Neither is part of Omarchy, and neither is reviewed by the project."
  - q: "Does the Neptune kernel script work on Omarchy 4?"
    a: "Not as written. It only knows how to update GRUB or systemd-boot, and Omarchy has shipped Limine as its default bootloader since 2.0. It also assumes you are layering Omarchy onto an existing Arch install, which 4.x no longer supports."
related: [what-breaks-in-a-vm, raspberry-pi-5]
draft: false
---

## Decide what you actually want first

Two very different things get called "Omarchy on the Steam Deck", and only one of them is a good idea for most people.

The first is replacing SteamOS on the handheld itself. That is real, people have done it, and the Omarchy manual's [Omarchy on...](https://omarchy.org/manual/omarchy-on/) chapter links to a community script for it. It is also a downgrade for gaming. You give up SteamOS gaming mode, the suspend and resume that Valve tuned for the hardware, the TDP and fan controls, and the A/B system updates, in exchange for a tiling desktop on a 7 inch screen with no keyboard.

The second is getting a Deck style gaming mode on an ordinary Omarchy machine, so a hotkey drops you into Steam Big Picture running under gamescope. That is what the two plugins below do, and it works on normal hardware today.

Version facts here were checked against the Omarchy 4.0.4 source tree, released 2026-09-15. Nothing on this page was run on Deck hardware.

## Why deckarchy no longer slots into the install

[deckarchy](https://github.com/aorumbayev/deckarchy) by Altynbek Orumbayev is the script the manual links to. Read its README before you trust the manual's framing: it is a Neptune kernel installer, not an Omarchy installer, and it says it is experimental and only tested on the Steam Deck OLED.

Its documented order is vanilla Arch first, then the Neptune script, then Omarchy. That order made sense in the 3.x era, when you could layer Omarchy onto an existing Arch system with a shell script. Omarchy 4 dropped that. The 4.0.4 tree has no `boot.sh` and no top level `install.sh` at all, and the manual now opens with a flat statement that Omarchy is installed using an ISO. So there is no "proceed with Omarchy installation" step left to run after the kernel script.

Three more things to know before you run it:

- Its last commit is from 2025-08-19, roughly a year before Omarchy 4.0.0 shipped. No report of anyone running it against Quattro was found.
- Its bootloader logic only handles GRUB and systemd-boot. If it finds neither, it prints an error and tells you to configure the bootloader yourself. Omarchy installs Limine by default and has since 2.0, so that is the branch you land on.
- The README's one line install, piping `linux-neptune.sh` from raw.githubusercontent.com straight into a shell, cannot work on its own. The first line of that script sources `./common-script.sh`, a separate file in the repo that the pipe never fetches. Clone the repo and run it from inside the checkout instead.

## What the script changes, so you can judge it

Worth knowing before you hand it sudo. On a machine whose DMI product name is `Jupiter` or `Galileo`, it:

- appends the `jupiter-staging` and `holo-staging` SteamOS repos to `/etc/pacman.conf` with `SigLevel = Never`, which turns off signature checking for those repos
- force removes `linux-firmware` and its split packages with `pacman -Rdd`, which skips dependency checks
- installs `linux-neptune-611`, its headers, `steamdeck-dsp`, `alsa-ucm-conf` from jupiter-staging, and `linux-firmware-neptune`
- copies the Cirrus `cs35l41` speaker calibration and protection firmware into `/usr/lib/firmware/cirrus`, the step its own warning text ties to OLED speaker audio

The unsigned repos are the piece to think hardest about. See [is Omarchy safe](/security/is-omarchy-safe/) for how the project handles package trust normally.

## If you install on a Deck anyway

Use a microSD card, not the internal drive, at least the first time. In [discussion #840](https://github.com/omacom/omarchy/discussions/840), phren0logy reported installing Omarchy 2.0 to a Deck microSD card with no modifications, and noted you reach the boot menu by holding volume up while clicking power, then releasing volume up. JaydenIvanovic and sulphur later reported the same route working. That leaves SteamOS untouched on the eMMC or SSD.

Expect the internal speakers to stay silent. sulphur's report in that thread says the microSD install was otherwise smooth, but speaker audio did not work and installing `linux-firmware-neptune` from the AUR did not fix it; what did was the Bazzite kernel, `linux-bazzite-bin` from the AUR. That is the same problem deckarchy exists to solve, by a different kernel. Bluetooth audio worked without any of it.

Then plan around three things the installer assumes and the Deck does not have.

1. A keyboard. The ISO wizard needs one, and Omarchy encrypts the disk by default. The LUKS passphrase prompt will not take a Bluetooth keyboard, so the manual's advice applies: a wired or 2.4 GHz dongle keyboard, which on a Deck means a USB-C hub or adapter, at install and at every boot. The manual documents pressing `Ctrl + C` at the disk formatting confirmation to install without encryption, which is the honest trade if this is a throwaway handheld install.
2. Secure Boot. The manual requires it off before the ISO will install.
3. Screen rotation. The Deck's internal panel is mounted portrait. Check what Hyprland reports, then set the transform in `~/.config/hypr/monitors.lua`. That file ships with the syntax in a comment; adapted for the Deck's panel it looks like this:

```lua
-- transform: 1 = 90 degrees, 3 = 270 degrees
hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 1, transform = 3 })
```

Run `hyprctl monitors all` first to get the real connector name and to see which transform lands the right way up.

A gentler option exists if you only want to try Omarchy: JaydenIvanovic's original write up in the same discussion runs it in a GNOME Boxes VM on top of SteamOS, leaving the Deck vanilla. He later moved to the microSD route himself. Performance is what you would expect from a VM on a handheld APU. See [what breaks in a VM](/run/what-breaks-in-a-vm/) for the general caveats.

## The gaming mode plugins

These target any Omarchy machine, not Deck hardware.

### omarchy-steam-gaming-mode

[cephalization/omarchy-steam-gaming-mode](https://github.com/cephalization/omarchy-steam-gaming-mode) is the small one. It installs gamescope, writes `/usr/local/bin/switch-to-gaming` and `/usr/local/bin/return-to-desktop`, adds a `Super + F12` keybind and a Gaming Mode launcher entry, then runs Steam Big Picture inside a nested gamescope at your current resolution and refresh rate.

It should apply cleanly on 4.0.x, because [PR #4](https://github.com/cephalization/omarchy-steam-gaming-mode/pull/4) by johtok taught it to detect a Lua config and append a Lua binding rather than `.conf` syntax. It writes to `~/.config/hypr/bindings.lua`, which 4.0.4 ships, and the line it writes uses `hl.bind` with `hl.dsp.exec_cmd`, the same underlying call Omarchy 4's own `o.bind` helper ends in. Nobody has posted a run on a 4.0.x install, though, so treat that as reading the code, not a test. Install it from a clone:

```bash
git clone https://github.com/cephalization/omarchy-steam-gaming-mode.git
cd omarchy-steam-gaming-mode
chmod +x setup-gaming-mode.sh
./setup-gaming-mode.sh
```

Then fix two things the script gets wrong on 4.0.x.

Install mangohud yourself. In the current script the mangohud block sits after a `return 0` in the same function, so it never runs when Steam is already installed. The gamescope command it writes passes `--mangoapp`, which needs that package:

```bash
omarchy pkg add mangohud
```

Ignore its idle handling. The script kills `hypridle` and tries to restart it on exit. Omarchy 4 removed hypridle along with the rest of the pre Quattro stack, so both calls are no ops. The screensaver flag it touches, `~/.local/state/omarchy/toggles/screensaver-off`, is still the right file on 4.0.4, so that half still works.

One more README drift: it tells you to install Steam from the menu with `Super + Alt + Space`. On 4.0.x that opens the Apps menu. The Omarchy menu is `Super + Space`.

Open problems worth knowing: [issue #3](https://github.com/cephalization/omarchy-steam-gaming-mode/issues/3) reports Big Picture navigation being sluggish while games themselves run fine, with the maintainer saying he has seen the same on another distro, and [issue #5](https://github.com/cephalization/omarchy-steam-gaming-mode/issues/5) reports that leaving gaming mode with the documented `Super + W` crashes because mangoapp is still attached. `Super + W` is not something the script adds, it is Omarchy's stock close window binding, so what it actually does is close the nested gamescope window.

### DeckShift

[28allday/deckshift](https://github.com/28allday/deckshift) is the heavier project, grown out of the scripts shown off in discussions [#4534](https://github.com/omacom/omarchy/discussions/4534) and [#5143](https://github.com/omacom/omarchy/discussions/5143). It builds a ChimeraOS style gamescope session, binds `Super + Shift + S` to enter and `Super + Shift + R` to leave, and its README names Omarchy 4 as the primary target, including a native omarchy-shell panel that only installs on 4.x. It is the more current of the two. It is also much larger, it restarts SDDM to switch sessions, and it is a small community project with no review from the Omarchy project. It ships an `uninstall.sh` with a `--dry-run` mode; read what that removes before you commit.

## Verify it worked

Confirm the hardware is what the Deck scripts expect:

```bash
cat /sys/class/dmi/id/product_name
```

`Jupiter` is the LCD Deck, `Galileo` is the OLED. Anything else means the Deck specific firmware steps will be skipped.

After a gaming mode install, check the pieces rather than trusting the summary text:

```bash
grep switch-to-gaming ~/.config/hypr/bindings.lua
command -v gamescope mangoapp
```

All three should print something. If `mangoapp` is missing, gaming mode will fail at launch.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5, per DHH on 2026-09-08. Both plugins write to paths that 4.0 already moved once, so re check `~/.config/hypr/bindings.lua` after any major upgrade and after running the Quattro migration. See [3 to 4 Quattro](/upgrade/3-to-4-quattro/) and the [hyprland.conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

Also watch [issue #6947](https://github.com/omacom/omarchy/issues/6947), filed the day after 4.0.0 shipped and still open. Omarchy's default Steam window rule inhibits idle for the Steam client class only, and games launched through Steam normally get an XWayland class of `steam_app_<appid>`, so the screensaver can appear over a fullscreen game. That bites hardest with a controller, because gamepad input does not reset the idle timer, which is exactly the handheld and gaming mode case. One commenter confirmed on 4.0.0-1 that this rule at the bottom of `~/.config/hypr/hyprland.lua` fixes the plain Steam case:

```lua
o.window("steam_app_.*", { idle_inhibit = "fullscreen" })
```

It is not the whole fix, and the thread says why. Games running under gamescope, which is what both plugins above do, show up to Hyprland as class `gamescope`, not `steam_app_*`, so a second commenter needed `o.window("gamescope", { idle_inhibit = "fullscreen" })` as well. A third found a Proton title that reports class `steam`, matching neither. Run `hyprctl clients -j` while the game is up and write the rule against what it actually prints. None of this was verified here on Deck hardware.

Evidence on actual Deck installs is thin. The first hand reports found are the three microSD installs in discussion #840, all from 2025 and none against 4.0.x. Treat this page as a map of the terrain, not a tested recipe.

## Related

- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Is Omarchy safe](/security/is-omarchy-safe/)
- [3 to 4 Quattro upgrade](/upgrade/3-to-4-quattro/)
