---
title: "Switching from macOS to Omarchy: the honest day-one guide"
description: "What actually changes when you move from macOS to Omarchy 4.0.4: which Macs can run it, how Cmd becomes Super, and what the official manual leaves out."
answer: "Intel Macs run Omarchy natively and the installer applies Broadcom Wi-Fi, SPI keyboard and T2 fixes automatically. A full-disk install wipes Apple's EFI partition, which on 2016 and 2017 Touch Bar MacBook Pros with the T1 chip takes the Touch Bar, camera and Touch ID with it; the free-space install leaves it alone. Apple Silicon is not directly supported and needs Asahi. The main habit change is Cmd becoming Super, plus tiling instead of dragging windows."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [macos, switching, apple, keyboard, tiling]
sources:
  - url: "https://omarchy.org/manual/coming-from-mac-or-windows/"
    title: "Omarchy Manual, chapter 03: Coming From Mac or Windows"
    kind: manual
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy Manual, chapter 44: Mac support"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy Manual, chapter 49: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy Manual, chapter 50: Dual Boot Install"
    kind: manual
  - url: "https://github.com/omacom/omarchy-mac"
    title: "omacom/omarchy-mac: Opinionated Arch/Hyprland Setup for Apple Silicon Macs M1/M2"
    kind: docs
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8323"
    title: "Issue #8323: Installer erases EFI/APPLE payload required by T1 MacBook hardware"
    kind: issue
    author: "sebastiang"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy-iso/pull/174"
    title: "omarchy-iso PR #174: Preserve Apple EFI firmware folder across the install"
    kind: pr
    author: "niconistal"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7666"
    title: "Issue #7666: Can Omarchy be installed as a dual-boot setup alongside macOS 10.15 without formatting the entire disk?"
    kind: issue
    author: "foobra"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/11997"
    title: "Issue #11997: Installer's ENABLE_LIMINE_FALLBACK=no hides Omarchy from the Mac boot picker, leaving it unbootable after an NVRAM reset"
    kind: issue
    author: "makoni"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/10593"
    title: "Issue #10593: Suspend/resume support for vintage MacBook Pro 13\" 2017 (MacBookPro14,1): default `deep` sleep breaks Thunderbolt on resume"
    kind: issue
    author: "orospakr"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7838"
    title: "Issue #7838: Proposal: macOS-friendly Tab keybindings (SUPER+TAB for windows, not workspaces)"
    kind: issue
    author: "nestor-bolivar"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11369"
    title: "Issue #11369: numlock_by_default silently breaks letter keys on old Apple Bluetooth keyboards (hid-apple numpad emulation)"
    kind: issue
    author: "roju"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7439"
    title: "Issue #7439: No Wi-Fi on Apple Silicon Macs: the Broadcom quirk's chip-ID gate includes BCM4378/BCM4387"
    kind: issue
    author: "thejamescollins"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/8645"
    title: "Issue #8645: Install menu offers x86_64-only packages on aarch64: every entry fails with `target not found` in a floating terminal that closes"
    kind: issue
    author: "alexandru-savinov"
    date: "2026-08-27"
credits:
  - name: "PaulShadwell"
    url: "https://github.com/PaulShadwell"
    for: "Documented that a full-disk install destroys T1 coprocessor firmware stored on the Apple ESP"
  - name: "niconistal"
    url: "https://github.com/niconistal"
    for: "Published t1-revive, a Linux-side T1 firmware regeneration tool, and the omarchy-iso patch to preserve EFI/APPLE"
  - name: "makoni"
    url: "https://github.com/makoni"
    for: "Traced why Omarchy does not appear in the Mac boot picker and tested the fallback loader fix"
  - name: "orospakr"
    url: "https://github.com/orospakr"
    for: "Root-caused deep-sleep Thunderbolt breakage on MacBookPro14,1"
  - name: "roju"
    url: "https://github.com/roju"
    for: "Identified numlock numpad emulation on old Apple Bluetooth keyboards"
faq:
  - q: "Can I run Omarchy on my M1 or M2 MacBook?"
    a: "Not with the normal Omarchy installer. The official manual says M-series Macs are not directly supported, and the route people actually use is Asahi Alarm plus a community setup script. Expect open bugs in that path, including Wi-Fi and package availability problems tracked in issues #7439 and #8645."
  - q: "Does Omarchy remap the Command key?"
    a: "No. Linux already reports a Mac keyboard's Command key as Super, so Omarchy's Super bindings land under the same thumb position you used for Cmd. Chapter 03 of the manual states this directly."
  - q: "Will installing Omarchy keep macOS on the same Mac?"
    a: "The Mac chapter of the manual says Omarchy only supports being the only OS on a Mac and that the drive is wiped. The manual's dual-boot chapter documents a free-space install, and Mac owners in issues #7666 and #8271 report it leaving macOS and Apple's EFI partition intact. Nobody upstream has reconciled the two chapters yet."
  - q: "Where is Cmd + Tab?"
    a: "Alt + Tab cycles windows, and Super + Tab moves to the next workspace. That mapping surprises macOS switchers often enough that issue #7838 proposes changing it, but it is unchanged in 4.0.4."
related: [what-replaces-what, day-one-checklist, tiling-window-manager-survival, should-you-dual-boot]
draft: false
---

Most of what makes the macOS to Omarchy move hard is not Linux. It is three specific things: whether your Mac can run it at all, where your Cmd reflexes go, and the fact that you stop placing windows. This page checks against Omarchy 4.0.4, released 2026-09-15.

## Which Macs can actually run it

Intel Macs are the supported case. The official [Mac support chapter](https://omarchy.org/manual/mac-support/) says Omarchy has built-in support for Intel Macs, and the installer does real work for you: it detects Apple hardware and installs Broadcom Wi-Fi drivers and firmware, the SPI keyboard driver on the MacBook models that need it, and an NVMe suspend fix. On T2 machines it also pulls the patched `linux-t2` kernel, `apple-t2-audio-config`, Apple's Broadcom firmware, and `t2fanrd` for fan control.

Two limits matter before you commit.

First, the disk. The Mac chapter states Omarchy only supports being the only OS on a Mac at the moment, and that macOS will no longer be bootable afterwards; you can restore it later through Internet Recovery. But the manual's own [dual-boot chapter](https://omarchy.org/manual/dual-boot-install/) documents a "Free space install" option in the same installer, and Mac owners have used it. A reply in [issue #7666](https://github.com/omacom/omarchy/issues/7666) describes shrinking APFS from macOS, leaving the space unallocated, picking the free-space install on a 2020 T2 MacBook Pro, and keeping macOS bootable. The issue is still open with no maintainer reply, and the Mac chapter has not been updated to match. See [should you dual-boot](/switch/should-you-dual-boot/) before deciding.

Second, and this is the one that catches people: the 2016 and 2017 Touch Bar MacBook Pros with the T1 chip (MacBookPro13,2, 13,3, 14,2 and 14,3) keep the T1's firmware in an `EFI/APPLE` folder on the EFI System Partition that macOS maintains. [Issue #8271](https://github.com/omacom/omarchy/issues/8271) reports that a full-disk install replaces that partition, after which the T1 comes up in recovery mode on every boot and the Touch Bar, FaceTime camera, Touch ID and ambient light sensor stop working. On these models that also means no physical Esc and no function row. [Issue #8323](https://github.com/omacom/omarchy/issues/8323) is an independent report on a MacBookPro13,3, and two more owners confirmed the same in the thread. The installer has no T1 detection and prints no warning; a collaborator diagnosis in the thread confirms the wipe is unconditional on the full-disk path. The same diagnosis, and a T2 owner in the thread, say T2 Macs are not affected, so the issue's own "T1/T2" title overstates it. The manual's own T1 section already lists the Touch Bar and sound as non-functional, but it only names 2016 models, so a 2017 owner reading it would file themselves under T2.

What to do about it: the free-space install creates its own ESP and leaves Apple's alone, which is what an owner of a MacBookPro14,2 reports after checking the partition hash before and after. Copy `EFI/APPLE` off the machine from macOS first regardless; the folder contains per-machine data, so another Mac's copy is no use. If you have already wiped one, the reporter's original finding stands that Apple's Configurator revive does not cover T1. Since 2026-09-15 a third-party tool, `t1-revive`, claims to regenerate the firmware from Linux by talking to Apple's signing server, with one confirmation on a MacBookPro14,2 in the thread. It is days old and lightly tested. Upstream, [omarchy-iso PR #174](https://github.com/omacom/omarchy-iso/pull/174) would preserve `EFI/APPLE` across the full-disk install; it is open and unmerged as of 2026-09-16. Read our [T2 Mac page](/hardware/t2-mac/) before you start.

Apple Silicon is a different project. Chapter 49 of the manual, [Omarchy on...](https://omarchy.org/manual/omarchy-on/), points M1 and M2 owners at [Asahi Alarm](https://asahi-alarm.org/) and a user-driven guide rather than the normal installer. There is also [omacom/omarchy-mac](https://github.com/omacom/omarchy-mac), which layers Omarchy 4 on top of an Asahi Alarm Minimal install alongside macOS. That path works for people, but it is not the same tested surface. [Issue #7439](https://github.com/omacom/omarchy/issues/7439) describes Wi-Fi scanning but never associating on an M1 Max because the Intel-Mac Broadcom handshake workaround lists BCM4378 and BCM4387 too; a follow-up comment reports the quirk since gated to Intel Macs and gives the cleanup for a `/etc/modprobe.d/brcmfmac.conf` already on disk, though the 4.0.4 script we checked still lists both chip IDs. [Issue #8645](https://github.com/omacom/omarchy/issues/8645), filed from an aarch64 VM, shows the Install menu offering packages that only exist for x86_64; a comment notes an aarch64 edge package tree appeared on 2026-09-06, but stable still lacks one. Both issues are open. See [Apple Silicon](/hardware/apple-silicon-asahi/) for detail, or [Omarchy in UTM](/run/utm-apple-silicon/) if you would rather run Omarchy in a VM.

## Cmd becomes Super, and nothing is remapped

The single most useful thing in [chapter 03](https://omarchy.org/manual/coming-from-mac-or-windows/) is the reassurance that Omarchy does not remap anything. Linux treats a Mac keyboard's Command key as Super, so the key stays exactly where your thumb expects.

The bindings that carry over directly, confirmed in Omarchy 4.0.4's `default/hypr/bindings/`:

- `Super + Space` opens the Omarchy menu. This is where your Spotlight or Raycast habit goes. `Super + Alt + Space` is apps only.
- `Super + C`, `Super + X` and `Super + V` are copy, cut and paste, and they work in the terminal too. `Super + Ctrl + V` is clipboard history.
- `Super + K` lists every binding. If you memorise one thing, memorise this.
- `Super + W` closes the window, and the app really quits. There is no windowless limbo.
- `Super + 1` through `Super + 4` jump to workspaces, which are Spaces without the animation.

The one that will bite you: `Alt + Tab` cycles windows, while `Super + Tab` moves to the next workspace. Your Cmd + Tab reflex lands on the wrong thing. [Issue #7838](https://github.com/omacom/omarchy/issues/7838) argues for flipping this, pointing out that GNOME on Fedora and Ubuntu binds Super + Tab to window switching. It is open with no maintainer response as of 2026-09-16, so plan on retraining or rebinding it yourself in Lua; the issue includes a working `bindings.lua` snippet.

On Mac hardware, two more keyboard details. The installer writes `options hid_apple fnmode=2` on every install, so on any keyboard the `hid_apple` driver handles the top row acts as F keys and you hold Fn for brightness and volume, the opposite of the macOS default. And there is no Print Screen key on a MacBook, which is what screenshots are bound to, so you will want to rebind that or use the capture menu on `Super + Ctrl + C`. If you pair an old Apple Bluetooth keyboard without a numpad, [issue #11369](https://github.com/omacom/omarchy/issues/11369) reports that U, I, O, P, J, K, L and M type digits instead of letters, because Omarchy enables numlock by default and the `hid-apple` driver has numpad emulation for those keyboards.

## What the official chapter does not cover

Chapter 03 is a good map and a short one. It is a translation table, not a troubleshooting guide, and it stays silent on the three things most likely to cost you an afternoon:

- **Screen sharing.** Nothing in chapter 03 mentions that Wayland screen capture goes through a portal, so Meet, Zoom and Teams behave differently than they did on macOS. See [screen sharing](/switch/screen-sharing-meet-zoom-teams/).
- **Non-US keyboard layouts.** If you used a German, French or Nordic layout on macOS, the layout you pick in the desktop is not the one LUKS and the login screen use. See [non-US layouts](/switch/non-us-keyboard-layout-luks-sddm/).
- **Scaling.** Retina panels want fractional scaling, and Electron and Chromium apps still have open rendering bugs at non-integer scales. See [fractional scaling](/switch/fractional-scaling-hidpi-apps/).

Chapter 03 also says nothing about Mac firmware behaviour after install. [Issue #11997](https://github.com/omacom/omarchy/issues/11997) reports that Omarchy does not appear in the Option-key boot picker: on an installed 4.0.3 system `/etc/default/limine` carried `ENABLE_LIMINE_FALLBACK=no`, so nothing lands at the `EFI/BOOT/BOOTX64.EFI` path Apple's firmware looks for. The reporter had not traced which part of the installer writes that line, and the Omarchy tree's own Limine drop-in sets it to `yes`, so it comes from the ISO installer rather than anything you can read in the omarchy repository. Day to day it boots fine from its NVRAM entry, but Mac NVRAM gets cleared by PRAM resets, macOS updates and drained batteries, and then you need a live USB or macOS to get back in. The reporter's fix was to set the variable to `yes` and run `limine-install`; the reply in issue #7666 reaches the same place by copying `limine_x64.efi` to `EFI/BOOT/BOOTX64.EFI` from macOS.

## The tiling shock

You do not drag windows any more. The first window you open gets the whole screen, the second shares it, and nothing overlaps, so nothing gets lost behind anything.

The reflex that fights this hardest is not window dragging, it is window hoarding. On macOS you keep twenty windows open and dig. In a tiler that is misery, because every window you open shrinks the ones you care about. The fix is workspaces. Put one task per workspace, jump with `Super + 1` through `Super + 4`, and close what you are done with. `Super + T` floats the current window when you genuinely need it, and `Super + F` goes full screen.

Give it the two weeks the manual asks for. See [tiling survival](/switch/tiling-window-manager-survival/) for the longer version.

## First-week habits that actually help

1. Hit `Super + K` every time you blank on a key. It is faster than searching.
2. Learn `Super + Space` before anything else. Installing software, changing settings and capturing the screen all live there.
3. Put your Cmd + Tab reflex on `Alt + Tab` deliberately for a few days.
4. On a MacBook, test lid-close suspend early. [Issue #10593](https://github.com/omacom/omarchy/issues/10593) documents a 2017 13-inch MacBook Pro where the default deep sleep takes 75 to 107 seconds to resume and can kill Thunderbolt until a cold boot. Draft patches exist (PR #10758) but nothing has merged as of 2026-09-16. See [suspend and sleep](/hardware/suspend-sleep/).
5. Update with the menu, not per-app updaters. Omarchy snapshots before it updates.

## What to watch for on newer versions

Everything above is checked against 4.0.4. If you are reading older Mac walkthroughs or videos from the 3.x era, the config paths in them are wrong: Omarchy 4.0.0 "Quattro" moved Hyprland configuration from `~/.config/hypr/*.conf` to Lua files using an `o.bind("SUPER + K", "Label", action)` DSL, so any guide that tells you to edit `bindings.conf` predates 4.0. See [the conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

None of the Mac issues above are marked fixed in 4.0.1 through 4.0.4, so assume they still apply until a release note says otherwise, and check [releases](/releases/).

One honest caveat: the T1 firmware loss is now several independent reports plus a collaborator diagnosis against the installer source, and the recovery tool that appeared this week has one confirmation. What is still missing is any maintainer decision on whether the installer should warn, refuse or preserve the folder. Treat it as a reason to take the free-space path and back up `EFI/APPLE` before wiping a Touch Bar Mac, not as something the next release is guaranteed to fix.
