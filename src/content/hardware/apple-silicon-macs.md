---
title: "Apple Silicon Macs (M1 to M4) on Omarchy"
description: "What actually runs on an M1 to M4 Mac in September 2026: the Try Omarchy app, the omarchy-mac Asahi install, the Omarchy M plan, and the open bugs."
answer: "Experimental. The 4.0.4 ISO is x86_64 and will not boot an M-series Mac. Three other paths exist: the Try Omarchy app, which runs the desktop as a hardware-accelerated macOS app, the omarchy-mac script, which installs Omarchy 4 on Asahi Alarm beside macOS on M1 and M2, and a signed macOS installer app that does the same from a GUI. Brightness, lid, built-in HDMI and post-resume Wi-Fi and audio all have open bugs."
appliesTo:
  from: "4.0.0"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Apple"
model: "Apple Silicon Macs (M1 to M4)"
dmi: []
cpu: "Apple M1, M1 Pro/Max/Ultra, M2, M2 Pro/Max/Ultra, M3, M4"
gpu: "Apple integrated GPU, driven by Asahi (mesa asahi, vulkan-asahi)"
year: "2020 to 2026"
rating: experimental
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: partial
  display: partial
  battery: unknown
  keyboard: works
quirkScripts:
  - name: "vulkan.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/vulkan.sh"
    note: "Upstream. Installs vulkan-asahi when lspci reports an Apple VGA or Display device. Migration 1784401744.sh backfills the same package on installs that predate it."
  - name: "fix-brcmfmac-supplicant.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/apple/fix-brcmfmac-supplicant.sh"
    note: "Upstream. Intended for Intel Macs, but its chip-ID list still includes BCM4378 and BCM4387 in v4.0.4, which is issue #7439. The omarchy-mac fork carries the x86_64 gate."
  - name: "fix-wifi-resume.sh"
    url: "https://github.com/omacom/omarchy-mac/blob/quattro/install/hardware/apple/fix-wifi-resume.sh"
    note: "Fork only. Installs omarchy-wifi-resume-fix, which reloads brcmfmac when the firmware wedges after s2idle. Gated to aarch64 and to BCM4378/BCM4387."
  - name: "fix-asahi-hid-race.sh"
    url: "https://github.com/omacom/omarchy-mac/blob/quattro/install/hardware/apple/fix-asahi-hid-race.sh"
    note: "Fork only. Early-loads hid_apple and hid_magicmouse from the initramfs so the internal trackpad does not lose its device node on unlucky boots."
  - name: "audio.sh"
    url: "https://github.com/omacom/omarchy-mac/blob/quattro/install/hardware/apple/audio.sh"
    note: "Fork only. Adds pipewire-pulse, rtkit, asahi-audio and speakersafetyd, which is what makes a speaker sink exist at all."
  - name: "enable-notch.sh"
    url: "https://github.com/omacom/omarchy-mac/blob/quattro/install/hardware/apple/enable-notch.sh"
    note: "Fork only. Sets appledrm show_notch=1 so the bar can use the strip beside the notch instead of the panel being cropped."
  - name: "video-decode.sh"
    url: "https://github.com/omacom/omarchy-mac/blob/quattro/install/hardware/apple/video-decode.sh"
    note: "Fork only. Adds avd-fw and libva-v4l2_request-avd so the Apple Video Decoder probes and VA-API can use it."
issueCount: 40
tags: [apple-silicon, asahi, macbook, aarch64, omarchy-m, hardware]
sources:
  - url: "https://omarchy.org/news/2026/09/introducing-omarchy-m/"
    title: "Introducing Omarchy M"
    kind: blog
    author: "dhh"
    date: "2026-09-11"
  - url: "https://omarchy.org/manual/mac-support/"
    title: "Omarchy manual: Mac support"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/try-omarchy"
    title: "omacom/try-omarchy: run Omarchy on macOS without any setup"
    kind: docs
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy-mac"
    title: "omacom/omarchy-mac: Omarchy 4 on Apple Silicon via Asahi Alarm"
    kind: docs
    date: "2026-09-16"
  - url: "https://github.com/maralcbr/omarchy-mx-mac"
    title: "maralcbr/omarchy-mx-mac: native macOS installer for Omarchy on Apple Silicon"
    kind: docs
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/7439"
    title: "Issue #7439: No Wi-Fi on Apple Silicon Macs: the Broadcom quirk's chip-ID gate includes BCM4378/BCM4387"
    kind: issue
    author: "thejamescollins"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/7872"
    title: "Issue #7872: Quattro/Apple Silicon: audio tuning command misreports the active Asahi J316 DSP as unsupported"
    kind: issue
    author: "SurreptitiousFabric"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8125"
    title: "Issue #8125: Brightness slider/keys silently no-op on Apple Silicon: wrong backlight device picked"
    kind: issue
    author: "CuraMagis"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8418"
    title: "Issue #8418: Asahi MacBooks: lid handling can never fire"
    kind: issue
    author: "GonzFC"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8376"
    title: "Issue #8376: omarchy-hw-touchpad misses Apple Touch (MTP) trackpads"
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
  - url: "https://github.com/omacom/omarchy/issues/10857"
    title: "Issue #10857: Wi-Fi resume fix excludes BCM4388 (14e4:4434), but it wedges on real lid-close suspend too"
    kind: issue
    author: "doomnote"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10858"
    title: "Issue #10858: Apple Silicon: speakersafetyd's post-resume PCM reinit wedges wireplumber"
    kind: issue
    author: "doomnote"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11591"
    title: "Issue #11591: aarch64: menu offers impossible installs and the floating terminal reports Done! on failure"
    kind: issue
    author: "Fromzy1"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/11914"
    title: "Issue #11914: Apple Silicon M1 Pro: built-in HDMI link teardown hangs Hyprland even at 1080p/60"
    kind: issue
    author: "lo-nau"
    date: "2026-09-15"
credits:
  - name: "thejamescollins"
    url: "https://github.com/thejamescollins"
    for: "Traced the dead Wi-Fi on M1 Pro and M1 Max to the Broadcom chip-ID list"
  - name: "bodhiblues"
    url: "https://github.com/bodhiblues"
    for: "Verified the Wi-Fi workaround on a BCM4387 M1 Pro and pointed out that updating does not remove the stale file"
  - name: "GonzFC"
    url: "https://github.com/GonzFC"
    for: "Found the lid switch name and the Apple MTP trackpad naming on M1 and M2 Airs"
  - name: "CuraMagis"
    url: "https://github.com/CuraMagis"
    for: "Identified apple-panel-bl as the real backlight device"
  - name: "SurreptitiousFabric"
    url: "https://github.com/SurreptitiousFabric"
    for: "Showed the Asahi J316 speaker DSP loaded and active while Omarchy reported no supported tuning"
  - name: "doomnote"
    url: "https://github.com/doomnote"
    for: "Documented the post-resume Wi-Fi and audio wedges on M2 Pro"
faq:
  - q: "Can I install the Omarchy 4.0.4 ISO on an M1 or M2 Mac?"
    a: "No. The ISO is x86_64 and the manual says M-series Macs are not directly supported. Use the Try Omarchy app, or the macOS installer app, or install Asahi Alarm first and run the omarchy-mac script."
  - q: "Is the Omarchy team working on Apple Silicon?"
    a: "Yes. Omarchy M was announced on 11 September 2026. The first release targets M1 and M2, including Pro and Max, with GPU, USB-C monitors, Touch ID, MLX and disk encryption. M3 and newer are being worked on in parallel."
  - q: "Does Omarchy M wipe macOS?"
    a: "The stated goal is an installer that carves out partitions and boots Omarchy alongside macOS. That is the opposite of the Intel Mac path in the manual, which wipes the drive."
  - q: "Why is my Wi-Fi dead right after installing?"
    a: "An Intel Mac quirk wrote /etc/modprobe.d/brcmfmac.conf on your machine. Delete it, reload brcmfmac, and reboot. See issue #7439."
related: [apple-silicon-asahi, t2-mac, apple-macbook-pro-intel, utm-apple-silicon]
draft: false
---

## Verdict

Experimental, and that word is doing real work here. Omarchy's own installer is x86_64. Through v4.0.4 there is no aarch64 ISO, and the [Mac support chapter](https://omarchy.org/manual/mac-support/) states that installing on an M-series Mac is not directly supported. Nothing about downloading the current release applies to an M1, M2, M3 or M4.

What changed recently is the effort around that gap. Omarchy M was announced on 11 September 2026 as the team for Apple Silicon, with "perfect compatibility with M1 and M2" as the first release target, including GPU, external monitors over USB-C, Touch ID, MLX and disk encryption, plus a macOS installer that puts Omarchy next to macOS rather than over it. M3 and newer are described as being worked on in parallel.

Three routes already exist, and none of them is the ISO. [Try Omarchy](https://github.com/omacom/try-omarchy) runs the real desktop as a hardware-accelerated macOS app and is linked from omarchy.org as "Try on Mac". [omarchy-mac](https://github.com/omacom/omarchy-mac) installs Omarchy 4 on top of Asahi Alarm on the metal, on M1 and M2 family machines. The announcement also links Marcelo Alcantara's [macOS installer app](https://github.com/maralcbr/omarchy-mx-mac), signed and notarized, which fetches a signed release, carves out the partitions and does the same job without the terminal. Buy or keep a Mac for macOS first, then treat Omarchy on it as a project rather than a daily driver you can rely on next week.

## What works

In Try Omarchy (v0.4.1, released 15 September 2026): the Quattro desktop with VirGL acceleration, Mac audio in and out, the FaceTime camera exposed as a 720p webcam, two-way clipboard, one shared folder, and loopback port forwarding. It needs macOS 15 or newer and about 8 GB free to start. On M3 and newer with macOS 26 or newer it also exposes EL2, so the guest gets /dev/kvm for nested VMs. The README's own caveat is that video decoding is CPU-only, so playback is slow at high resolutions.

On the metal with omarchy-mac on an M1 or M2: the Asahi GPU driver and vulkan-asahi are in place, the internal keyboard binds (the fork's `fix-asahi-hid-race.sh` documents the internal keyboard and trackpad coming up through `dockchannel-hid`, with only the trackpad at risk of losing its node), the Asahi audio DSP loads with the model-specific profile ([#7872](https://github.com/omacom/omarchy/issues/7872) shows `audio_effect.j316-convolver` as the live default sink on a MacBook Pro 16-inch M1 Max), full-disk encryption is offered during setup, and `omarchy snapshot restore` works and offers the pre-Omarchy system as a restore point. The install is one command after Asahi Alarm, with roughly fifteen minutes and three reboots.

Upstream itself contributes one thing: `install/hardware/vulkan.sh` maps an Apple display device to `vulkan-asahi`, and migration `1784401744.sh` backfills it on existing installs.

## What breaks

Everything below is open as of 2026-09-16, and none of it was fixed by a 4.0.x release.

- Wi-Fi never associates after install, [#7439](https://github.com/omacom/omarchy/issues/7439). The Intel Mac Broadcom quirk still lists BCM4378 and BCM4387 in v4.0.4 and writes `feature_disable=0x82000`. The x86_64 gate exists as a commit but is not in the `quattro` branch or in any released tag. The omarchy-mac fork does carry the gate, so a fresh fork install is clean. Anything installed from upstream since the quirk widened to all Macs on 2026-08-10 keeps the bad file, because the gate only stops the file being written and no update removes one already on disk.
- Wi-Fi wedges after lid-close suspend on BCM4388, [#10857](https://github.com/omacom/omarchy/issues/10857), reported on a MacBook Pro 16-inch M2 Pro. The fork's resume fix deliberately skips that chip ID.
- Audio is stuck muted after resume, [#10858](https://github.com/omacom/omarchy/issues/10858). speakersafetyd reinitialises the PCM at resume and wireplumber either wedges or crashes.
- Brightness does nothing, [#8125](https://github.com/omacom/omarchy/issues/8125). `omarchy-hw-display` picks the DSI node instead of `apple-panel-bl`.
- Closing the lid does nothing, [#8418](https://github.com/omacom/omarchy/issues/8418). The bind targets "Lid Switch" while Apple hardware reports "Apple SMC power/lid events", and the lid state is read from `/proc/acpi`, which Asahi does not have. The reporter measured 6.61 W with the lid closed and lit against 1.66 W with the panel off.
- Touchpad toggle silently fails on a MacBook Air M2, [#8376](https://github.com/omacom/omarchy/issues/8376), because Hyprland names it `apple-mtp-multi-touch`. The M1 Air is unaffected.
- The built-in HDMI port on 14-inch and 16-inch MacBook Pros is the worst area. [#11914](https://github.com/omacom/omarchy/issues/11914) hangs Hyprland with `flip_done timed out`, and [#8946](https://github.com/omacom/omarchy/issues/8946) flaps the monitor every 16 to 17 seconds once the desktop goes idle, during the screensaver as well as after the lock. Both trace to the `apple-dcp` kernel driver, not to Omarchy, and the reporter ruled out every lever Omarchy has.
- The Install menu offers packages that cannot exist on aarch64, [#8645](https://github.com/omacom/omarchy/issues/8645) and [#11591](https://github.com/omacom/omarchy/issues/11591), and the floating terminal can report success anyway.

For the per-bug detail and the current workarounds, see [/hardware/apple-silicon-asahi/](/hardware/apple-silicon-asahi/).

## What Omarchy does for this model

Less than you would expect, and not for the reason people assume. DMI is populated on these machines: the upstream commit that tried to narrow the Wi-Fi quirk says an Asahi MacBook "reports Apple Inc. through DMI like any other Mac", and the confirming comment on [#8418](https://github.com/omacom/omarchy/issues/8418) reads `chassis_type` as 9 on an Asahi MacBookPro18,3. What is missing is a rule that matches an M-series machine on purpose. `omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `product_family`, and no script in the released tree pairs that with an Apple Silicon model. The fork gates on `uname -m` and on `/proc/device-tree/compatible`, which reports strings like `apple,j314s`, `apple,j316c`, `apple,j416s` and `apple,t6020`.

In the released v4.0.4 tree, `install/hardware/apple/` holds four scripts and three of them are Intel-only by construction: `fix-t2.sh` matches the T2 bridge PCI IDs, and `fix-spi-keyboard.sh` and `fix-suspend-nvme.sh` match DMI names such as `MacBookPro14,3`. The fourth is the Wi-Fi quirk described above. One piece of good news: the 4.0.4 kernel migration that installs `linux-omarchy` exits immediately unless `uname -m` is x86_64, so the bespoke kernel never touches an Asahi install.

The Apple Silicon enablement lives in the fork instead. Its `install/hardware/apple/` adds `audio.sh`, `fix-wifi-resume.sh`, `fix-asahi-hid-race.sh`, `enable-notch.sh`, `electron-gl.sh` and `video-decode.sh`, listed with their jobs in the frontmatter above. If a page or a video tells you Omarchy handles Apple Silicon audio or the notch out of the box, it means the fork.

## Variants

- M1 and M2, including Pro, Max and Ultra: the supported set. Asahi covers all M1 and M2 MacBook, Mac mini, Mac Studio, Mac Pro and iMac models, and omarchy-mac asks for an M1 or M2 family machine with at least 50 GB free, 100 GB recommended.
- M3 and M4: outside what the bare-metal paths ask for. omarchy-mac wants an M1 or M2 family machine, Omarchy M says newer chips are parallel work, and the announcement credits recent progress getting the M3 Air's internal display onto Apple's display controller. Asahi's own device support list is the place to check a specific model, and it did not cover M4 when this page was checked. Try Omarchy runs on M3 and M4 and is the sensible choice there for now.
- MacBook Pro 14-inch and 16-inch: expect trouble on the built-in HDMI port. Prefer USB-C or DisplayPort output, which is what the Omarchy M first release targets.
- Almost every bug report on file is a laptop. The tracker has no Mac mini or Mac Studio reports under Omarchy, so treat desktops as untested rather than working.

## Before you install

1. Back up macOS with Time Machine or equivalent first.
2. Run Try Omarchy for a day before touching partitions. It is a normal macOS app and changes nothing on disk beyond its own VM.
3. Check your machine on Asahi's device support list before planning a bare-metal install.
4. Keep macOS installed. Unlike the Intel Mac path, this is a side-by-side layout, and the Asahi partitioning cheatsheet is what you need to undo it.
5. Leave 50 to 100 GB free and plan for about fifteen minutes plus three reboots.
6. After install, check `/etc/modprobe.d/brcmfmac.conf`. If it exists on an M-series machine, delete it and reload `brcmfmac`.
7. Expect the fork to lag upstream. Its newest tagged release is still on the 4.0.3 line while [/releases/v4.0.4/](/releases/v4.0.4/) has already shipped.

## Related

- [/hardware/apple-silicon-asahi/](/hardware/apple-silicon-asahi/) for the full bug list and workarounds
- [/hardware/t2-mac/](/hardware/t2-mac/) and [/hardware/apple-macbook-pro-intel/](/hardware/apple-macbook-pro-intel/) for Intel Macs, which Omarchy does support
- [/run/utm-apple-silicon/](/run/utm-apple-silicon/) for running Omarchy in a VM on a Mac
- [/hardware/multi-monitor/](/hardware/multi-monitor/) and [/hardware/audio/](/hardware/audio/) for the general versions of the display and sound problems
