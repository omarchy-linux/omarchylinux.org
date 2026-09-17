---
title: "Apple Silicon Macs and Asahi on Omarchy"
description: "Omarchy has no official Apple Silicon build. What actually works on M-series Macs under Asahi, which quirk scripts misfire on aarch64, and the fixes people have verified."
answer: "Omarchy does not officially support M-series Macs. There is no aarch64 ISO, and the manual points you at Asahi Alarm plus a community fork. On those forks the desktop runs, but brightness, lid handling, touchpad toggle, HDMI output and post-resume audio all have open bugs, and one Intel-Mac Wi-Fi quirk misfires on Apple Silicon and kills Wi-Fi entirely."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "apple-silicon-asahi"
issueCount: 40
tags: [apple-silicon, asahi, aarch64, macbook, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7439"
    title: "Issue #7439: No Wi-Fi on Apple Silicon Macs: the Broadcom quirk's chip-ID gate includes BCM4378/BCM4387"
    kind: issue
    author: "thejamescollins"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/8125"
    title: "Issue #8125: Brightness slider/keys silently no-op on Apple Silicon: wrong backlight device picked"
    kind: issue
    author: "CuraMagis"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7872"
    title: "Issue #7872: [Quattro/Apple Silicon] Audio tuning command misreports active Asahi J316 DSP as unsupported"
    kind: issue
    author: "SurreptitiousFabric"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8376"
    title: "Issue #8376: omarchy-hw-touchpad misses Apple Touch (MTP) trackpads, so omarchy-toggle-touchpad silently does nothing"
    kind: issue
    author: "GonzFC"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8418"
    title: "Issue #8418: Asahi MacBooks: lid handling can never fire"
    kind: issue
    author: "GonzFC"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8645"
    title: "Issue #8645: Install menu offers x86_64-only packages on aarch64"
    kind: issue
    author: "alexandru-savinov"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/8946"
    title: "Issue #8946: Quattro/Apple Silicon: lock-screen DPMS blank causes repeating HDMI hotplug flap"
    kind: issue
    author: "gmahfood"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/10477"
    title: "Issue #10477: omarchy-hw-laptop: DMI chassis fallback never matches"
    kind: issue
    author: "flip-in"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10857"
    title: "Issue #10857: Wi-Fi resume fix excludes BCM4388 (14e4:4434), but it wedges on real lid-close suspend too"
    kind: issue
    author: "doomnote"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10858"
    title: "Issue #10858: Apple Silicon: speakersafetyd's post-resume PCM reinit wedges/crashes wireplumber"
    kind: issue
    author: "doomnote"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11591"
    title: "Issue #11591: aarch64: menu offers impossible installs (Spotify, Dropbox) and the floating terminal reports Done! on failure"
    kind: issue
    author: "Fromzy1"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/11914"
    title: "Issue #11914: Apple Silicon M1 Pro: built-in HDMI link teardown hangs Hyprland even at 1080p/60"
    kind: issue
    author: "lo-nau"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
credits:
  - name: "thejamescollins"
    url: "https://github.com/thejamescollins"
    for: "Found that the Intel-Mac Broadcom quirk matches Apple Silicon chip IDs"
  - name: "bodhiblues"
    url: "https://github.com/bodhiblues"
    for: "Verified the Wi-Fi recovery steps on an M1 Pro and flagged that existing installs do not self-heal"
  - name: "CuraMagis"
    url: "https://github.com/CuraMagis"
    for: "Traced the dead brightness slider to the wrong backlight device and published a working override"
  - name: "GonzFC"
    url: "https://github.com/GonzFC"
    for: "Reported the Apple MTP trackpad and Asahi lid-switch detection failures"
  - name: "flip-in"
    url: "https://github.com/flip-in"
    for: "Proposed the logind LidClosed fallback and found the third blocker in omarchy-hw-laptop"
  - name: "doomnote"
    url: "https://github.com/doomnote"
    for: "Reproduced the BCM4388 resume wedge and the post-resume audio teardown"
faq:
  - q: "Can I install Omarchy on an M1 or M2 Mac?"
    a: "Not with the official installer. There is no aarch64 ISO. People run Omarchy on top of Asahi Alarm using community forks, and the manual links a user-driven guide for that."
  - q: "Does Omarchy's Mac hardware setup help on Apple Silicon?"
    a: "Barely. Three of the four scripts in install/hardware/apple gate on Intel Mac DMI names or the T2 PCI ID. The fourth matches Apple Silicon Wi-Fi chips and breaks Wi-Fi, which is issue #7439."
  - q: "Why does my brightness slider do nothing?"
    a: "omarchy-hw-display does not know about apple-panel-bl, so it picks the DSI node, which accepts writes and changes nothing. Point OMARCHY_BACKLIGHT_PATH at the real device."
  - q: "Is external HDMI usable?"
    a: "Not reliably on the built-in HDMI port. Issues #11914 and #8946 both trace to the apple-dcp kernel driver, and there is no fix at the Omarchy layer."
related: [t2-mac, apple-silicon-macs, wifi, audio, multi-monitor]
draft: false
---

## Status on 4.0.4

Omarchy does not ship an Apple Silicon build. There is no aarch64 ISO, and the installer is x86_64 only. The [Mac support chapter](https://omarchy.org/manual/mac-support/) covers Intel Macs and says plainly that installing on an M-series Mac is not directly supported. The [Omarchy on... chapter](https://omarchy.org/manual/omarchy-on/) points at Asahi Alarm, which is Arch for M1 and M2 Macs built on Asahi Linux, and links a user-driven guide for layering Omarchy on top.

So everything on this page describes Omarchy running on an Asahi or Arch Linux ARM base, usually through a community fork. The reporters below name theirs: `omarchy-mac`, `omarchy-mac.N` builds, and `omarchy-mx-mac`. None of that is an official channel, and none of it gets release testing.

What does work once you are there: the Hyprland session and the Quickshell bar come up, the GPU has a Vulkan driver, Wi-Fi associates, and Asahi's own audio DSP loads and produces sound. What does not work is a long list, and most of it is Omarchy code assuming x86 Linux conventions rather than anything Asahi got wrong.

Forty issues in the tracker match Apple Silicon and Asahi terms. Many of those are Intel Mac reports that share vocabulary, so treat the count as a search result, not a defect list. For Intel Macs with the T2 chip, see [/hardware/t2-mac/](/hardware/t2-mac/) instead.

## What Omarchy does automatically

Almost nothing, and one thing it should not.

`install/hardware/vulkan.sh` maps a PCI display controller whose vendor string contains "Apple" to `vulkan-asahi`. That package is also in `install/omarchy-other.packages`, and the 3.x to 4.x upgrade path adds it (`bin/omarchy-upgrade-to-quattro`, plus migration `1784401744.sh`). This is the one piece of Apple Silicon support in the released tree, and it works.

The four scripts in `install/hardware/apple/` are Intel-Mac code:

- `fix-t2.sh` gates on PCI IDs `106b:1801` and `106b:1802`, the T2 bridge. No M-series Mac has one, so it never runs.
- `fix-spi-keyboard.sh` and `fix-suspend-nvme.sh` gate on DMI `product_name` matching `MacBookPro13,x`, `MacBookPro14,x` and friends. Asahi machines report a device-tree compatible like `apple,j314s`, not those names, so neither runs.
- `fix-brcmfmac-supplicant.sh` is the problem. It matches `sys_vendor` starting with "Apple" plus Broadcom IDs including `14e4:4425` and `14e4:4433`, which are BCM4378 and BCM4387, the Wi-Fi chips in Apple Silicon Macs. It then writes `feature_disable=0x82000` into `/etc/modprobe.d/brcmfmac.conf`, which is correct for Intel Macs and wrong here.

The `omarchy-brightness-display-apple` and `omarchy-hyprland-monitor-focused-apple` commands sound relevant but are not. They drive external Apple Studio Display and Pro Display XDR panels over HID, on any machine.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#7439](https://github.com/omacom/omarchy/issues/7439) Broadcom quirk disables the firmware supplicant on M-series Wi-Fi | Any M1/M2 with BCM4378 or BCM4387 | Open. An `x86_64` gate exists on main but is in no released tag through 4.0.4 | not yet |
| [#8125](https://github.com/omacom/omarchy/issues/8125) brightness slider and keys no-op | M1 MacBook Pro 13" (`apple,j293`), likely all | Open. `omarchy-hw-display` still has no `apple-panel-bl` entry in 4.0.4 | not yet |
| [#7872](https://github.com/omacom/omarchy/issues/7872) audio tuning reports "nothing ships for this laptop" while the Asahi DSP is active | MacBook Pro 16" M1 Max (`apple,j316c`) | Open, cosmetic but misleading | not yet |
| [#10858](https://github.com/omacom/omarchy/issues/10858) audio dies after VT switch or resume | MacBook Pro M1 Pro (J314) | Open. Root cause traced to PipeWire module teardown, not Omarchy | not yet |
| [#10857](https://github.com/omacom/omarchy/issues/10857) Wi-Fi wedges after lid-close suspend | MacBook Pro 16" 2023, M2 Pro (`Mac14,10`), BCM4388 | Open. The chip gate in the forks' resume fix omits `14e4:4434` | not yet |
| [#8418](https://github.com/omacom/omarchy/issues/8418) lid close does nothing | Asahi MacBooks, confirmed on MacBookPro18,3 | Open. Lid state is read from `/proc/acpi`, which Asahi does not have | not yet |
| [#10477](https://github.com/omacom/omarchy/issues/10477) `omarchy-hw-laptop` DMI fallback never matches | Any machine without an ACPI lid button | Closed as not planned. The bug is still in 4.0.4 | no |
| [#8376](https://github.com/omacom/omarchy/issues/8376) touchpad toggle silently does nothing | MacBook Air M2 2022 (M1 Air unaffected) | Open. Hyprland names the device `apple-mtp-multi-touch` | not yet |
| [#8946](https://github.com/omacom/omarchy/issues/8946) external HDMI flaps "No Signal" every ~16s while locked | M-series with built-in HDMI | Open. Reporter traced it to `apple-dcp` upstream | no Omarchy fix |
| [#11914](https://github.com/omacom/omarchy/issues/11914) built-in HDMI link teardown hangs Hyprland | MacBook Pro 16" M1 Pro 2021 | Open. `flip_done timed out` from `apple-drm` | no Omarchy fix |
| [#8645](https://github.com/omacom/omarchy/issues/8645) and [#11591](https://github.com/omacom/omarchy/issues/11591) install menu offers x86-only packages | All aarch64 | Open. Nothing in the menu checks architecture | not yet |

Two patterns run through that list. The first is hardcoded x86 Linux assumptions: `/proc/acpi` for the lid, device names containing "touchpad", backlight device names from Intel and AMD laptops. The second is real Asahi driver limits, mainly `apple-dcp` display output, which Omarchy cannot fix from userspace.

## Fixes that work

Work in this order.

**Wi-Fi dead after install.** Delete the file the quirk wrote and reload the driver:

```sh
sudo rm /etc/modprobe.d/brcmfmac.conf
sudo modprobe -r brcmfmac_wcc brcmfmac && sudo modprobe brcmfmac
```

bodhiblues verified this on an M1 Pro with BCM4387 and `linux-asahi 7.1.6`. Note that an updated install does not clean the file up on its own, so if you installed between mid and late August 2026 you have to remove it by hand.

**Brightness does nothing.** Check which device is real:

```sh
brightnessctl -l
brightnessctl -d apple-panel-bl set 10%
```

If `apple-panel-bl` visibly dims the screen while the numeric DSI node does not, point Omarchy at it. `omarchy-hw-display` honours `OMARCHY_BACKLIGHT_PATH`, so CuraMagis made a directory containing only a symlink to `apple-panel-bl` and exported that path via `hl.env(...)` in `~/.config/hypr/hyprland.lua`.

**Wi-Fi does not come back after suspend.** If your chip is BCM4388 (`14e4:4434`), the fork's resume fix skips you. doomnote enabled the same `omarchy-wifi-resume-fix.service` unit by hand and logged a clean wedge-and-recover cycle: the service reloaded `brcmfmac` after 12 seconds and NetworkManager reconnected 8 seconds later. That unit is not in the upstream 4.0.4 tree, only in the Mac forks.

**Lid close does nothing while docked.** flip-in's fix has three parts: read the lid from logind instead of ACPI, with `busctl get-property org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager LidClosed`; drop the `2>/dev/null` from the `$(< file)` substitution in `omarchy-hw-laptop` so the DMI fallback actually matches; and re-register the binds against the switch Hyprland reports, which is `Apple SMC power/lid events`. With all three, a lid close while docked disabled the internal panel and held it.

**Audio stuck muted after a VT switch.** Restart WirePlumber with `systemctl --user restart wireplumber`. There is no configuration fix, because the defect is reentrant module destruction inside PipeWire's filter-chain teardown.

**External HDMI.** No workaround found. Disabling the lock screen's blank timer did not stop the flap, and forcing 1080p60 did not stop the hang. Use an external display only if you can tolerate that, or stay on the internal panel.

**Install menu entries that fail.** On aarch64, entries like Spotify and Dropbox cannot succeed, and the floating terminal prints a green "Done!" regardless of exit status. Check availability first with `pacman -Si <pkg>`. birkskyum reported on 2026-09-06 that the edge aarch64 package database at `pkgs.omarchy.org` served 115 packages while stable and rc still returned 404, so some Omarchy-packaged apps do exist for ARM.

## Report it

Run `omarchy debug --no-sudo --print` and paste the output. That command exists in 4.0.4. Several reports on this page say it was missing, because those machines were on 4.0.1rc1 or an older fork build. If yours does not have it, say so and include the manual equivalents.

Always include, because none of it is guessable from a normal Omarchy bundle:

- `uname -m` and the kernel string, for example `7.1.13-1-1-ARCH`.
- The device-tree compatible: `cat /proc/device-tree/compatible`, which gives you `apple,j314s` or `apple,t6001`.
- Which fork and channel you run, and the exact `omarchy version` output such as `4.0.3.r6962.ga67d7f7-1`.
- For audio, the `asahi-audio`, `speakersafetyd`, PipeWire and WirePlumber versions.
- For Wi-Fi, `lspci -nn | grep -i network` so the chip ID is in the report.

File against `omacom/omarchy` only when the defect is in Omarchy's own scripts, which is true for the backlight, lid, touchpad and menu bugs. Display and audio-stack failures usually belong upstream with Asahi or PipeWire, and saying so in the report saves everyone a round trip.

## Related

- [/hardware/t2-mac/](/hardware/t2-mac/) for Intel Macs with the T2 chip, which Omarchy does support
- [/hardware/apple-silicon-macs/](/hardware/apple-silicon-macs/) for the model page
- [/hardware/wifi/](/hardware/wifi/) and [/hardware/audio/](/hardware/audio/)
- [/hardware/multi-monitor/](/hardware/multi-monitor/) and [/hardware/suspend-sleep/](/hardware/suspend-sleep/)
- [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/)
- [/hardware/submit/](/hardware/submit/) to add your machine
