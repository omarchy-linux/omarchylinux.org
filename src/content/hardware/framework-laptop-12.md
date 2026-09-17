---
title: "Framework Laptop 12 on Omarchy"
description: "Framework Laptop 12 on Omarchy 4.0.4: Intel Raptor Lake runs out of the box, but tablet mode is half done. Rotation, on-screen keyboard, touch gaps."
answer: "Buy it as a laptop, not as a tablet. The Framework Laptop 12 runs Omarchy 4.0.4 on the generic Intel path with no model specific setup, and owners including DHH use one. Touch input works, but Omarchy has no auto rotation and no on-screen keyboard, and the screensaver still will not dismiss on touch. Prefer the 13th Gen Intel board over the new Wildcat Lake one for now."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Framework"
model: "Framework Laptop 12"
dmi:
  - "Laptop 12 (13th Gen Intel Core)"
  - "Laptop 12 (Intel Core Series 3)"
year: "2025-2026"
cpu: "Intel Core i3-1315U or i5-1334U (Raptor Lake U); Core 3 304, Core 5 320 or Core 7 350 (Wildcat Lake) on the 2026 board"
gpu: "Intel integrated (Iris Xe on the 13th Gen board)"
rating: silver
subsystems:
  wifi: works
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: works
  suspend: unknown
  hibernate: unknown
  touchpad: works
  display: works
  battery: unknown
  keyboard: works
quirkScripts:
  - name: "intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Installs intel-media-driver, libvpl and vpl-gpu-rt when lspci shows an Iris or Xe part. Matches the 13th Gen board, misses Wildcat Lake."
  - name: "intel/lpmd.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/lpmd.sh"
    note: "Installs and enables intel-lpmd when the CPU model number is in the Alder Lake through Panther Lake list, which includes Raptor Lake 183, 186 and 191."
  - name: "intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Installs and enables thermald on any Intel laptop with a battery."
  - name: "intel/sof-firmware.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/sof-firmware.sh"
    note: "Installs sof-firmware when an Intel audio controller is present, which is what keeps PipeWire from showing only a Dummy Output."
  - name: "framework16.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/framework16.sh"
    note: "The only Framework specific script in the tree. It gates on omarchy-hw-framework16, so it never runs on a Laptop 12."
issueCount: 7
tags: [framework, framework-laptop-12, intel, touchscreen, tablet, convertible]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7762"
    title: "Issue #7762: [Quattro] Screensaver only exits on a keypress inside its own terminal"
    kind: issue
    author: "Atarit0"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/2361"
    title: "Issue #2361: Better framework laptop 12 support?"
    kind: issue
    author: "ColtonIdle"
    date: "2025-10-10"
  - url: "https://github.com/omacom/omarchy/discussions/4431"
    title: "Discussion #4431: Better framework laptop 12 support?"
    kind: discussion
    author: "ColtonIdle"
    date: "2025-10-10"
  - url: "https://github.com/omacom/omarchy/discussions/834"
    title: "Discussion #834: Arch + Omarchy in Touchscreen laptops"
    kind: discussion
    author: "SatoriSec"
    date: "2025-08-15"
  - url: "https://github.com/omacom/omarchy/discussions/848"
    title: "Discussion #848: Omarchy + Rotation on Framework 12"
    kind: discussion
    author: "2disbetter"
    date: "2025-08-16"
  - url: "https://github.com/omacom/omarchy/issues/2215"
    title: "Issue #2215: Removing USB installer when prompted results in error on framework 12"
    kind: issue
    author: "ColtonIdle"
    date: "2025-10-04"
  - url: "https://github.com/omacom/omarchy/issues/1422"
    title: "Issue #1422: Wifi sometimes stops working and requires rfkill or restarting iwd to work"
    kind: issue
    author: "ColtonIdle"
    date: "2025-09-03"
  - url: "https://github.com/omacom/omarchy/issues/296"
    title: "Issue #296: intel-media-driver required for screen recording to work on intel integrated graphics"
    kind: issue
    author: "aifrim"
    date: "2025-07-23"
  - url: "https://github.com/omacom/omarchy/issues/11958"
    title: "Issue #11958: intel/video-acceleration.sh doesn't match Intel Wildcat Lake GPU, skips installing intel-media-driver"
    kind: issue
    author: "theswampdawg"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/3069"
    title: "Issue #3069: Exit screen saver on touch screen or power button."
    kind: issue
    author: "WangElectronics"
    date: "2025-11-02"
  - url: "https://github.com/omacom/omarchy/issues/2308"
    title: "Issue #2308: Chromium asks for keyring password on every startup"
    kind: issue
    author: "mmsbrggr"
    date: "2025-10-08"
  - url: "https://github.com/FrameworkComputer/framework-system/blob/main/framework_lib/src/smbios.rs"
    title: "framework-system: SMBIOS product name to platform table"
    kind: docs
    author: "FrameworkComputer"
  - url: "https://www.phoronix.com/news/Framework-Laptop-12-WCL"
    title: "Framework Laptop 12 Updated For Intel Wildcat Lake, Shipping Starts In October"
    kind: blog
    author: "Michael Larabel"
    date: "2026-08-18"
  - url: "https://frame.work/blog/framework-laptop-12-now-with-core-series-3"
    title: "Framework Laptop 12, now with Core Series 3"
    kind: blog
    author: "Framework"
    date: "2026-08-18"
  - url: "https://omarchy.org/manual/toggles-idle-screensaver/"
    title: "Omarchy manual: Toggles, idle and screensaver"
    kind: manual
credits:
  - name: "ColtonIdle"
    url: "https://github.com/ColtonIdle"
    for: "Filed the tablet mode request and the Framework 12 install and Wi-Fi reports"
  - name: "2disbetter"
    url: "https://github.com/2disbetter"
    for: "First working screen rotation recipe for the Framework 12 under Hyprland, then FW12Rotate"
  - name: "mechanicsunlocked"
    url: "https://github.com/mechanicsunlocked"
    for: "Gimbal, a tablet mode package for the Framework 12 on Omarchy 4"
  - name: "devteapot"
    url: "https://github.com/devteapot"
    for: "Confirmed on real Framework 12 hardware that touch does not dismiss the screensaver"
  - name: "eclecticc"
    url: "https://github.com/eclecticc"
    for: "Flagged the missing intel-media-driver on Intel Framework laptops and fixed Intel video acceleration"
faq:
  - q: "Does the Framework Laptop 12 touchscreen work in Omarchy?"
    a: "Yes as a pointer. Hyprland sees the touch device, taps and scrolling work, and Omarchy can even disable it from Trigger > Hardware. What is missing is everything above that layer: no auto rotation, no on-screen keyboard, and no touch dismissal of the screensaver."
  - q: "Does Omarchy auto rotate the screen when I fold the Framework 12 into tablet mode?"
    a: "No. There is nothing in the v4.0.4 tree that reads the accelerometer. monitors.lua only takes a static transform value. Community projects FW12Rotate and Gimbal fill the gap, and neither is part of Omarchy."
  - q: "Which Framework Laptop 12 board should I buy for Omarchy?"
    a: "The 13th Gen Intel Core board, if you want the quiet option today. The Core Series 3 Wildcat Lake board is only scheduled to start shipping in October 2026 and already has one known Omarchy gap: issue #11958 shows video-acceleration.sh does not recognize its GPU string."
  - q: "Is there a Framework specific install script for the Laptop 12?"
    a: "No. The only Framework script in the tree, framework16.sh, gates on omarchy-hw-framework16 and only fires on a Laptop 16. The Laptop 12 is handled entirely by the generic Intel scripts."
related: [intel-gpu, touchpad-input, wifi, framework-laptop-13, suspend-sleep]
draft: false
---

## Verdict

Silver. The Framework Laptop 12 is a plain Intel laptop as far as Omarchy is concerned, and plain Intel laptops are the easiest hardware this distro runs on. Nothing in the v4.0.4 tree is written for this machine, and nothing needs to be. The half that is not solved is the half you bought it for if you bought it as a convertible: touch works as a pointer, but Omarchy has no screen rotation, no on-screen keyboard, and an open bug where touching the screen will not wake it.

Owners are real and vocal. DHH posted about his own Framework 12 in issue #1422 in October 2025, and ColtonIdle, who filed most of the Framework 12 reports in the tracker, called it a delight to use Omarchy with in issue #2361. In discussion #834, inffy noted that people have made Omarchy work nicely on this machine. That is the accurate summary: it works, with a tablet shaped hole.

We checked this against the v4.0.4 source tree and against the issue tracker on 2026-09-16. Three issues name the Framework 12 in their own body, and four more carry Framework 12 owner reports inside someone else's thread.

## What works

The silicon is unremarkable, which is the point. The 13th Gen board is Raptor Lake U with Intel integrated graphics, and Omarchy's generic Intel path covers all of it.

Wi-Fi works. The 13th Gen board ships an Intel AX211, driven by iwlwifi with firmware from linux-firmware. It is not in the BE200 and BE211 list that Omarchy's Wi-Fi 7 workaround targets, so that script leaves it alone.

Graphics work. The iGPU reports as an Iris Xe part, which matches the detector in `intel/video-acceleration.sh`, so a fresh install gets `intel-media-driver`, `libvpl` and `vpl-gpu-rt` without you asking. That was not always true. Issue #296 is the history: Framework's own eclecticc pointed out in August 2025 that Intel Framework laptops, the Laptop 12 included, needed `intel-media-driver` installed by hand before screen recording worked. The v2.1.1 release notes carry the fix, credited to him.

Touch, keyboard and touchpad work as input devices. The reporter in issue #2361 describes scrolling working, the machine running fast, and the physical keyboard going quiet when folded into tablet mode. No touchpad or keyboard bug has ever been filed against this model.

## What breaks

The screensaver does not dismiss on touch. This is the live one. Issue #7762 is open against Quattro, and devteapot reproduced it on Framework Laptop 12 hardware specifically: touching the screen does nothing, moving the mouse does nothing, clicking does nothing, only a keypress works. The analysis in that thread pins it on `bin/omarchy-screensaver`, which waits for a byte on its terminal's stdin, and touch never becomes one. Worse, the lock timer is never cancelled, so the session can lock while you are actively tapping. Three pull requests are open against it and the maintainer has not picked one. On a convertible this is the difference between a tablet and a brick, so flip the keyboard back or raise the screensaver timeout under _Trigger > Toggle_ until it lands. The same request was filed for this machine much earlier as issue #3069 and closed without a shipped fix.

There is no screen rotation. Omarchy reads no accelerometer anywhere in v4.0.4. `~/.config/hypr/monitors.lua` takes a static `transform` value and stops there, which the [monitors chapter](https://omarchy.org/manual/monitors/) documents. 2disbetter wrote the first working workaround in discussion #848, a shell loop around `monitor-sensor` that calls `hyprctl keyword monitor` on each orientation change, and later packaged it as FW12Rotate. In August 2026, mechanicsunlocked posted Gimbal in discussion #4431, which adds auto rotation, an on-screen keyboard laid out like the machine's own, and edge swipes for Omarchy 4. Neither is shipped or reviewed by Omarchy. Treat both as third party code you are choosing to run.

There is no on-screen keyboard. Nothing in the tree provides one. That was request item one in issue #2361, which was closed in February 2026 with no feature.

Two older reports have aged out but are worth knowing if you find an old thread. Issue #1422 is the Wi-Fi that comes up connected but routes nothing until `sudo rfkill unblock all`; both ColtonIdle and DHH hit it on new Framework 12 units on 3.0.2. DHH closed it in July 2026 on the grounds that Quattro replaced the iwd, Impala and systemd-networkd stack with NetworkManager, and asked for a fresh issue if it reproduces. Issue #2215 is an install failure on this machine caused by pulling the USB stick out at the reboot prompt instead of after the reboot. Both are 3.x era. If you hit either on 4.0.4, file it.

## What Omarchy does for this model

Nothing by name. `bin/omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `product_family`, and the only Framework caller is `omarchy-hw-framework16`, which checks that `sys_vendor` is Framework and then matches the literal string `Laptop 16`. A Laptop 12 fails that test, so `framework16.sh` and the `qmk-hid` udev rule never run on it. You lose nothing: both exist for the Laptop 16 input module.

For reference when you want to write your own match, Framework's own `framework-system` tool maps two DMI product names for this machine: `Laptop 12 (13th Gen Intel Core)` and `Laptop 12 (Intel Core Series 3)`. Check yours with `cat /sys/class/dmi/id/product_name`.

What actually runs on a Laptop 12 install is the Intel set: `video-acceleration.sh` for VA-API, `sof-firmware.sh` for the audio DSP, `thermald.sh` on any Intel laptop with a battery, and `lpmd.sh`, which installs and enables `intel-lpmd` when `/proc/cpuinfo` reports a CPU model in its list. Raptor Lake's 183, 186 and 191 are in that list, so the 13th Gen board gets it. `fred.sh` and `fix-wifi7-eht.sh` are gated to Panther Lake and to BE200 and BE211 cards, so neither fires here.

## Variants

Two boards now share the chassis, and they are not equally proven.

The 13th Gen Intel Core board, with the i3-1315U or the i5-1334U, is the one every report on this page was written on. Prefer it if you want the boring outcome.

The Core Series 3 board, announced by Framework on 2026-08-18, is Intel Wildcat Lake with Core 3 304, Core 5 320 and Core 7 350 options, Thunderbolt 4, and an Intel BE213 Wi-Fi 7 module. Phoronix reported the first batch shipping in October 2026. It already has one confirmed Omarchy gap that is not model specific but will bite it: issue #11958, filed on 2026-09-15 against 4.0.3 and still open, shows that the Wildcat Lake GPU reports as `Wildcat Lake [Intel Graphics]`, which matches none of the patterns in `video-acceleration.sh`, so no VA-API driver is installed at all. Installing `intel-media-driver libvpl vpl-gpu-rt libva-utils` by hand fixes it. We have no Omarchy report on the BE213 Wi-Fi module or on suspend behaviour on that board at all. If you buy it, expect to be the first.

The fingerprint reader and the backlit input cover are separate parts on the newer configuration rather than standard. We have no Framework 12 fingerprint report either way, so see [fingerprint readers](/hardware/fingerprint/) for the general picture rather than assuming.

## Before you install

Pick the 13th Gen board unless you want to test Wildcat Lake yourself.

Leave the USB stick in until the machine has actually rebooted and shown the vendor logo. That is what issue #2215 is about.

Expect to run without rotation on day one. Decide in advance whether you want to run FW12Rotate or Gimbal, both third party, or live with a static landscape screen.

Raise the screensaver timeout, or plan to keep a keyboard reachable, until issue #7762 closes. The [toggles and screensaver chapter](https://omarchy.org/manual/toggles-idle-screensaver/) covers where those settings live.

If video decode looks wrong after install on any board, check `vainfo` before changing anything else.

We have no verified data on suspend, hibernate, battery life, audio, bluetooth or the webcam on this model under 4.0.4. An earlier hand written prototype of this site claimed all of those worked, and we could not source any of it, so those rows read unknown here. If you run one, [send us your results](/hardware/submit/).

## Related

[Intel graphics](/hardware/intel-gpu/) covers the VA-API detector and the Wildcat Lake gap in full. [Framework Laptop 13](/hardware/framework-laptop-13/) is the better documented sibling. [Touchpad and input](/hardware/touchpad-input/), [Wi-Fi](/hardware/wifi/) and [suspend and sleep](/hardware/suspend-sleep/) cover the subsystems we could not verify here. If you are moving a 3.x install forward, read [3 to 4 Quattro](/upgrade/3-to-4-quattro/) first.
