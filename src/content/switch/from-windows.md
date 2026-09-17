---
title: "Switching from Windows 11 to Omarchy Linux"
description: "What actually changes moving from Windows 11 to Omarchy 4.0.4: trying it in a window first, dual boot traps, Secure Boot, the Super key, and gaming."
answer: "Try Omarchy in a window on Windows first with Try Omarchy for Windows, which needs no partitioning. If you commit, turn off BitLocker and Secure Boot before installing, and shrink the Windows partition from Disk Management, never from the installer's cfdisk. Then relearn one key: Super replaces the Windows key and drives everything."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [windows, dual-boot, migration, secure-boot, gaming]
sources:
  - url: "https://omarchy.org/manual/getting-started/"
    title: "Omarchy manual: Getting Started"
    kind: manual
  - url: "https://omarchy.org/manual/dual-boot-install/"
    title: "Omarchy manual: Dual Boot Install"
    kind: manual
  - url: "https://omarchy.org/manual/coming-from-mac-or-windows/"
    title: "Omarchy manual: Coming From Mac or Windows"
    kind: manual
  - url: "https://omarchy.org/manual/gaming/"
    title: "Omarchy manual: Gaming"
    kind: manual
  - url: "https://omarchy.org/manual/windows-vm/"
    title: "Omarchy manual: Windows VM"
    kind: manual
  - url: "https://github.com/omacom/try-omarchy-windows"
    title: "omacom/try-omarchy-windows: Use Omarchy Linux on Windows without any hassle"
    kind: docs
  - url: "https://github.com/omacom/omarchy/issues/7903"
    title: "Issue #7903: Installer partitioning step lets users resize a live Windows NTFS partition with cfdisk, resulting in unbootable Windows"
    kind: issue
    author: "alkevintan"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7906"
    title: "Issue #7906: limine-scan (documented dual-boot step) generates a Windows entry that panics at boot"
    kind: issue
    author: "alkevintan"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7867"
    title: "Issue #7867: Dual-boot install creates a redundant ESP instead of reusing the existing Windows one, and omarchy-refresh-limine permanently drops the Windows entry on every run"
    kind: issue
    author: "ThePeteJames"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/10598"
    title: "Issue #10598: 4.0.2 free-space install registers no UEFI boot entry, boots straight to Windows"
    kind: issue
    author: "exergonic"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/10945"
    title: "Issue #10945: Limine-only update leaves limine_x64.efi unsigned, causing Secure Boot Violation lockout"
    kind: issue
    author: "LoboHacks"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/9630"
    title: "Issue #9630: omarchy windows vm launch fails, numeric chmod 0700 cannot clear the setgid bit on ~/Windows"
    kind: issue
    author: "zakkoo"
    date: "2026-09-01"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "alkevintan"
    url: "https://github.com/alkevintan"
    for: "Traced the cfdisk NTFS resize data loss and the case-sensitive limine-scan path bug"
  - name: "ThePeteJames"
    url: "https://github.com/ThePeteJames"
    for: "Documented the duplicate ESP and the Windows entry being dropped by omarchy-refresh-limine"
  - name: "zakkoo"
    url: "https://github.com/zakkoo"
    for: "Root-caused the Windows VM setgid launch failure to numeric chmod on a directory"
faq:
  - q: "Can I keep Windows and install Omarchy next to it?"
    a: "Yes. The installer has a free-space option that puts Omarchy in unallocated space and still encrypts it with LUKS. Shrink the Windows partition from Windows Disk Management first, and turn BitLocker off, because the dual-boot path is not compatible with full-drive BitLocker encryption."
  - q: "Do I have to disable Secure Boot?"
    a: "Yes. The Omarchy manual states plainly that Secure Boot and/or TPM must be off in the BIOS to install. That is the supported path as of 4.0.4, and Secure Boot related boot failures are still open issues."
  - q: "Where did my Windows key go?"
    a: "It is Super, and it is now the anchor for almost every shortcut. Super + Space opens the Omarchy menu, Super + K lists every binding, Super + Ctrl + V is the clipboard history that used to be Win + V."
  - q: "Can I still run Microsoft Office?"
    a: "LibreOffice ships with Omarchy and opens Office files. If you need the real thing, Install > Windows sets up a Windows 11 Pro VM in Docker that shares a clipboard and the ~/Windows folder, but it has no GPU passthrough and arrives unactivated."
related: [day-one-checklist, what-replaces-what, should-you-dual-boot, screen-sharing-meet-zoom-teams]
draft: false
---

Checked against Omarchy 4.0.4, released 2026-09-15. Everything below assumes the 4.x Quickshell based desktop. On 3.x the keys are mostly the same but the config files are `~/.config/hypr/*.conf` instead of Lua.

## Try it without touching your disk

The lowest risk move is not an install at all. [Try Omarchy for Windows](https://github.com/omacom/try-omarchy-windows) runs the full desktop in a window on Windows 10 or 11. It is a single `TryOmarchy.exe` that switches on the Windows Hypervisor Platform, downloads a prebuilt Arch image with Omarchy in it, and boots. No partitions, no bootloader changes, everything in one folder.

Know what you are getting. The current release is `v0.0.19-preview`, published 2026-09-16, and it carries Omarchy 4.0.3 rather than 4.0.4. The project describes itself as working toward v1, with physical acceptance testing centred on one AMD Windows 11 laptop. It is x86_64 only, so ARM64 Windows machines with Snapdragon chips are not supported. Networking is QEMU NAT, and host webcam capture did not work in the recorded acceptance run.

What it is good for is exactly the question you have: does the tiling model click for me, do my web apps work, does the keyboard layout feel right. Two evenings in that window will tell you more than any review.

## Dual boot or wipe

Omarchy installs either full disk or into free space. The free-space option is the dual boot path, and it still applies LUKS encryption to its own partition.

Before you boot the ISO, do three things in Windows.

1. Turn BitLocker off. The dual-boot install is not compatible with it, because BitLocker encrypts the whole drive rather than a partition. Settings, then Privacy and Security, then Device encryption. Decryption takes a while.
2. Shrink the Windows volume from Disk Management, not from the installer. Type `disk management` in the Start menu, right click the partition, choose Shrink Volume.
3. Turn off Secure Boot in the BIOS, and TPM as well if the installer still complains. The manual's wording is that Secure Boot and/or TPM must be off to install.

Step 2 is the one that eats people. Issue [#7903](https://github.com/omacom/omarchy/issues/7903), filed against 4.0.0 and still open as of 2026-09-16, describes the installer's guided partitioning dropping the user into `cfdisk`, whose Resize only rewrites the GPT entry. It does not shrink the NTFS filesystem inside. Windows then refused to boot with `UNMOUNTABLE_BOOT_VOLUME`, and data beyond the new boundary was already gone. Shrink from Windows, leave the free space unallocated, and let the installer use it.

After the install, expect boot menu work. Three separate open issues describe the same family of problems:

- [#7867](https://github.com/omacom/omarchy/issues/7867): the free-space install can create a second ESP instead of reusing the existing Windows one, and `omarchy-refresh-limine` copies in a template with no OS entries, so a Windows entry you added by hand disappears on the next refresh.
- [#7906](https://github.com/omacom/omarchy/issues/7906): `limine-scan`, the step the manual tells you to run to add Windows to the menu, writes the uppercase path reported by `efibootmgr`. Limine's FAT lookup is case sensitive, so the entry panics with "image not found". Correcting the casing in `/boot/limine.conf` to the real on-disk `EFI/Microsoft/Boot/bootmgfw.efi` fixes it.
- [#10598](https://github.com/omacom/omarchy/issues/10598): on 4.0.2 a free-space install completed with all files in place but registered no UEFI boot entry at all, so the machine went straight back to Windows.

None of these are fatal, and all of them are recoverable from a live USB. But if you are not comfortable with `efibootmgr` and editing `limine.conf`, a separate drive for Omarchy is the calmer choice. See [should you dual boot](/switch/should-you-dual-boot/) and [Limine boot](/hardware/boot-limine/).

One more physical detail: full disk encryption means typing a passphrase before the OS exists, and Bluetooth keyboards do not work at that prompt. Have a wired or 2.4GHz keyboard for first boot. If you use a non-US layout, read [non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/) before you install, not after.

## The Win key becomes Super

On Linux the Windows key is Super, and in Omarchy it is the anchor for nearly everything. The hotkeys that carry over most directly:

| Windows habit | Omarchy |
| --- | --- |
| Start menu, PowerToys Run | `Super + Space` |
| Win + V clipboard history | `Super + Ctrl + V` |
| Win + Shift + S | `Print Screen` |
| Alt + Tab | `Alt + Tab` still cycles windows |
| Explorer | `Super + Shift + F` opens Files |
| Ctrl + C in the terminal | `Super + C` and `Super + V` work everywhere |
| Win + arrow snapping | nothing, windows tile themselves |
| PowerToys Text Extractor | `Super + Ctrl + Print` |
| PowerToys Color Picker | `Super + Print` |
| PowerToys Awake | `Super + Ctrl + I` |

The one binding worth memorising is `Super + K`, which lists every binding with its description. The [official switching chapter](https://omarchy.org/manual/coming-from-mac-or-windows/) is the short version of this table.

FancyZones has no equivalent because it has no job. Windows do not overlap and you do not drag them. The default layout is dwindle, which shrinks everything to fit; `Super + L` turns the current workspace into a scrolling layout instead, and the choice sticks per workspace. Give it a fortnight before you decide, and read [tiling window manager survival](/switch/tiling-window-manager-survival/) if the first day feels hostile.

## What replaces what

- **Explorer:** Nautilus, branded Files, on `Super + Shift + F`. USB sticks automount. Disks handles formatting and SMART.
- **PowerToys:** split across the bindings above plus `~/.config/hypr/input.lua` for keyboard remapping. There is no single settings panel.
- **Office:** LibreOffice is preinstalled and reads Office formats. Microsoft 365 in the browser is the other route, and Install > Web App will pin it as a frameless app. For the genuine desktop suite, Install > Windows builds a Windows 11 Pro VM in Docker with shared clipboard, sound and a `~/Windows` shared folder. It arrives unactivated, needs KVM enabled in the BIOS, and has no GPU passthrough.
- **OneDrive:** nothing ships for it. Omarchy's base install deliberately stays off the AUR, and there is no OneDrive installer in the menu. Your realistic options are the web client as a web app, or Dropbox, which does have an Install > Service entry.
- **Settings app:** plain text files, opened through the Setup section of the Omarchy menu.
- **Windows Update:** one command, Update > Omarchy, which snapshots the system first.

A fuller table lives at [what replaces what](/switch/what-replaces-what/).

## Gaming expectations

Omarchy covers the whole spread: Steam, Lutris, Heroic, Battle.net, RetroArch, Minecraft, Xbox Cloud Gaming and GeForce NOW all install from Install > Gaming, and Moonlight comes preinstalled for streaming from a Windows PC running Sunshine.

The honest limit is anti-cheat, not performance. The [gaming chapter](https://omarchy.org/manual/gaming/) says outright that Fortnite and Rocket League do not run natively, and points at Xbox Cloud Gaming or Moonlight streaming from a Windows PC as the way to play Fortnite. Check your specific library on ProtonDB before you commit, because that single answer decides the migration for a lot of people. The Windows VM is not a workaround here: no GPU passthrough means it is for Office, not for games.

If you have an NVIDIA card, sort the driver out first. See [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/).

## Day one blockers to plan for

- Screen sharing in Meet, Zoom and Teams behaves differently under Wayland. See [screen sharing](/switch/screen-sharing-meet-zoom-teams/).
- Omarchy assumes a 2x display. On a 1080p or 1440p monitor set `omarchy_gdk_scale` and `omarchy_monitor_scale` to 1 in `~/.config/hypr/monitors.lua`, or step through scales with `Super + /`. See [fractional scaling and HiDPI apps](/switch/fractional-scaling-hidpi-apps/).
- Caps Lock is the compose key by default, which surprises everyone once.
- Printers are not auto-discovered right now. You add each one from Print Settings. See [printers and scanners](/switch/printers-and-scanners/).
- If you use the Windows VM, `omarchy windows vm launch` can start failing after the first session with "Failed to start Windows VM!". Issue [#9630](https://github.com/omacom/omarchy/issues/9630) traces it to the container leaving a setgid bit on `~/Windows` that a numeric `chmod 0700` cannot clear. The workaround is `chmod g-s ~/Windows` before relaunching. The numeric chmod is still in `bin/omarchy-windows-vm` in 4.0.4, and a search of the tracker on 2026-09-16 found more than thirty open issues describing the same failure, so expect to hit it.

Work through [the day one checklist](/switch/day-one-checklist/) on your first evening.

## What to watch for on newer versions

DHH has announced the next release as "Quattro RS 4.5". The dual-boot bugs above are all open against 4.0.x, so check the issue numbers before assuming they still apply.

Secure Boot remains the weakest area. The manual says to disable it, and the people who try to re-enable it with their own keys run into trouble. Issue [#10945](https://github.com/omacom/omarchy/issues/10945), open, reports that a Limine-only package update overwrites the signed `limine_x64.efi` with the unsigned stock binary, which locks the machine out with a Secure Boot Violation on the next boot. Do not turn Secure Boot back on after installing and assume it will keep working across updates.
