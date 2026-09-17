---
title: "ASUS ROG Zephyrus and Strix on Omarchy"
description: "ASUS ROG Zephyrus G14, G16 and Strix on Omarchy 4.0.4: bronze. asusctl and the hybrid GPU toggle ship, but hibernate, boot and audio still bite."
answer: "Bronze. ASUS ROG is one of the few families Omarchy names by hand: asusctl installs automatically, brightness and volume keys work, and the hybrid GPU toggle is built in. But 13 of 17 Zephyrus issues are still open on 4.0.4. The 2024 Strix Point G14 can black screen at boot, hibernate hangs hard on G14s, and the ROG audio fix caps volume at 80 percent."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: partial
kind: model
vendor: "ASUS"
model: "ROG Zephyrus G14, G15, G16, M16 and ROG Strix G16, G18"
dmi: ["GA401QC", "GA401QE", "GA402XV", "GA403UI", "GA403UM", "GA403UV", "GA605KM", "GA605WI", "GU603ZEB", "GU605CR", "G614FM", "G614FR", "G733ZW"]
year: "2021 to 2026"
cpu: "AMD Ryzen 5000H to Ryzen AI 9 HX 370, Intel Core Ultra 9 HX on some G16 and Strix models"
gpu: "Hybrid: AMD Radeon or Intel Arc iGPU on the panel plus NVIDIA RTX 3050 to RTX 5070 Ti Laptop"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: broken
  touchpad: unknown
  display: partial
  battery: partial
  keyboard: partial
quirkScripts:
  - name: "bin/omarchy-hw-asus-rog"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-asus-rog"
    note: "The gate every ROG fix hangs off. True when DMI sys_vendor is exactly ASUSTeK COMPUTER INC. and product_family contains ROG. It reads the family, never the product name, so a G14 and a G733 Strix get identical treatment."
  - name: "install/hardware/asus-rog.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus-rog.sh"
    note: "Two lines. If omarchy-hw-asus-rog passes, install asusctl. That is the entire root level ROG enablement. Omarchy ships asusctl 6.4.0-1 in its own stable channel repo."
  - name: "install/user/hardware/asus/fix-audio-mixer.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/asus/fix-audio-mixer.sh"
    note: "Copies alsa-soft-mixer.conf into WirePlumber, clears saved routes, then sets the ALC285 hardware Master to 80 percent and unmutes it. The 80 percent is the cause of issue #11046."
  - name: "install/user/hardware/asus/fix-mic.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/asus/fix-mic.sh"
    note: "Zeroes Internal Mic Boost on the ALC285 card, sets Capture to 70 percent, then runs alsactl store so the values survive reboot."
  - name: "bin/omarchy-theme-set-keyboard-asus-rog"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-theme-set-keyboard-asus-rog"
    note: "Reads the current theme keyboard.rgb and runs asusctl aura effect static with that color, so the keyboard follows your theme. Called from omarchy-theme-set."
  - name: "bin/omarchy-toggle-hybrid-gpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-toggle-hybrid-gpu"
    note: "Installs supergfxctl on first use, writes /etc/supergfxd.conf, and flips between Hybrid and Integrated with a reboot. Switching to Integrated is also what installs the force-igpu sleep hook."
  - name: "default/systemd/system-sleep/force-igpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/systemd/system-sleep/force-igpu"
    note: "Detaches the NVIDIA dGPU to Vfio before hibernate and restores Integrated after resume. Its own comments name the Asus G14. It is only installed if you have chosen Integrated mode."
  - name: "default/systemd/system-sleep/keyboard-backlight"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/systemd/system-sleep/keyboard-backlight"
    note: "Turns the keyboard LEDs off before hibernate because, in its own words, the ASUS keyboard controller can block S4 shutdown if LEDs are active."
  - name: "install/hardware/asus/fix-z13-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus/fix-z13-touchpad.sh"
    note: "The only ASUS quirk in the tree gated on a DMI product string: omarchy-hw-asus-rog plus omarchy-hw-match GZ302. That is the ROG Flow Z13, not a Zephyrus."
  - name: "install/hardware/nvidia.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    note: "The generic NVIDIA path your dGPU gets: nvidia-open-dkms on Turing and newer, early KMS, nvidia_drm modeset=1. It never enables nvidia-powerd, which is issue #9678."
issueCount: 17
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [asus, rog, zephyrus, strix, nvidia, hybrid-gpu]
sources:
  - url: "https://github.com/omacom/omarchy/issues/9720"
    title: "Issue #9720: [Hardware]: Black screen on boot on AMD Strix Point / Radeon 890M laptops (ASUS ROG Zephyrus G14) due to Aquamarine atomic DRM commit failure"
    kind: issue
    author: "codyoss"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/9696"
    title: "Issue #9696: Hibernate hangs (forced power-off required) on hybrid-GPU ASUS ROG G14, force-igpu/supergfxctl never installed"
    kind: issue
    author: "rdelpiano"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/8589"
    title: "Issue #8589: Hibernation aborts during image creation on ASUS ROG Zephyrus G14 (GA403UV); HibernateMode=shutdown fixes it"
    kind: issue
    author: "wjax"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11046"
    title: "Issue #11046: ASUS ROG: soft-mixer caps hardware Master at 80% so bar \"100%\" is not full volume"
    kind: issue
    author: "rdoupe"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/8359"
    title: "Issue #8359: ASUS ROG blanket software-mixer fix degrades audio quality on smart-amp laptops (e.g. G733ZW)"
    kind: issue
    author: "Orneyfish"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/4821"
    title: "Issue #4821: # No Sound Fix: ASUS ROG Strix G16 (2025) on Omarchy 3.4.1"
    kind: issue
    author: "beyondeye"
    date: "2026-02-28"
  - url: "https://github.com/omacom/omarchy/issues/8491"
    title: "Issue #8491: Omarchy shell stays alive but stops rendering after resume-time EGL_BAD_CONTEXT"
    kind: issue
    author: "Marlos001"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/7811"
    title: "Issue #7811: Lock screen visible but keyboard input dead after lid-open resume (reproduces on Quattro, follow-up to #2991)"
    kind: issue
    author: "awt"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/11460"
    title: "Issue #11460: LIBVA_DRIVER_NAME=nvidia forced on hybrid laptops where the panel is driven by the iGPU"
    kind: issue
    author: "elliott-ringasund"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/9678"
    title: "Issue #9678: Laptop NVIDIA GPUs stuck at default TGP, nvidia-powerd is never enabled"
    kind: issue
    author: "onelegdave"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/7374"
    title: "Issue #7374: Power panel shows UPower's hwdb charge limit (75-80%) instead of the real asusctl-set limit, and a bogus 0 cycle count"
    kind: issue
    author: "chickymonkeys"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/6949"
    title: "Issue #6949: Fn + F3 keyboard backlight shortcut not working on ASUS ROG Zephyrus G14"
    kind: issue
    author: "CosmicKittu"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7607"
    title: "Issue #7607: Display panel can't persistently turn off internal display, Omarchy watcher reverts it"
    kind: issue
    author: "EZHatETHZ"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/7303"
    title: "Issue #7303: Quattro: Suspend hard-freezes (s2idle) on ASUS ROG Strix G16 G614FR"
    kind: issue
    author: "PraiseTheDuck"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/5428"
    title: "Issue #5428: Hybrid GPU menu entry disappears after switching to Integrated mode"
    kind: issue
    author: "mechanicsunlocked"
    date: "2026-04-24"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.4.0"
    title: "Omarchy v3.4.0 release notes: Full Asus Zephyrous G14/16 compatibility"
    kind: release
    date: "2026-02-26"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-asus-rog"
    title: "bin/omarchy-hw-asus-rog at v4.0.4"
    kind: commit
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy Manual: System sleep"
    kind: manual
credits:
  - name: "codyoss"
    url: "https://github.com/codyoss"
    for: "Traced the Strix Point G14 boot black screen to an Aquamarine atomic DRM commit failure and showed AQ_NO_ATOMIC has to be set in the session environment, not in hyprland.lua"
  - name: "rdelpiano"
    url: "https://github.com/rdelpiano"
    for: "Showed that asus-rog.sh installs only asusctl, so a fresh G14 has hibernation enabled with none of the dGPU sleep handling Omarchy's own force-igpu hook says it needs"
  - name: "wjax"
    url: "https://github.com/wjax"
    for: "Isolated a silent swsusp_save abort on the GA403UV and confirmed HibernateMode=shutdown fixes it, while flagging the result as a single machine finding"
  - name: "rdoupe"
    url: "https://github.com/rdoupe"
    for: "Measured the ROG audio ceiling on a G16 GA605KM: soft-mixer plus a hardware Master at step 70 of 87 means the bar's 100 percent is 12.75 dB down"
  - name: "beyondeye"
    url: "https://github.com/beyondeye"
    for: "Worked out why the headphone jack stays silent on a Strix G16 and that removing the soft-mixer config lets PipeWire unmute the hardware switches on every boot"
  - name: "onelegdave"
    url: "https://github.com/onelegdave"
    for: "Proved by masking nvidia-powerd on a working install that the missing service is what pins ROG laptop GPUs at default TGP"
  - name: "Orneyfish"
    url: "https://github.com/Orneyfish"
    for: "Reported that the blanket ROG soft-mixer hurts smart-amp models such as the Strix G733ZW"
faq:
  - q: "Should I buy a ROG Zephyrus to run Omarchy?"
    a: "Only if you want the machine anyway. ROG gets real attention in Omarchy, including asusctl, a keyboard backlight that follows your theme and a built in hybrid GPU toggle, but the tracker still has an open boot black screen on the 2024 Strix Point G14 and two open hibernate hangs. A Framework or ThinkPad is a quieter life."
  - q: "Why is my volume at 100 percent still quiet?"
    a: "Omarchy's ROG audio script enables a software mixer and leaves the ALC285 hardware Master at 80 percent, which on one measured G16 is 12.75 dB below full scale. Raise it with amixer on the ALC285 card and store it. See issue #11046."
  - q: "Does hibernate work on a G14?"
    a: "Not reliably on 4.0.4. Two open reports end in a hard power off. On a hybrid unit the force-igpu sleep hook is not installed unless you have switched to Integrated mode, and on an iGPU only GA403UV the ACPI platform path aborts and HibernateMode=shutdown is what fixed it."
  - q: "Do I need asusctl or supergfxctl by hand?"
    a: "asusctl is installed for you on any ROG machine. supergfxctl is not: it arrives the first time you run the hybrid GPU toggle from Trigger then Hardware, or Super plus Ctrl plus H."
related: [nvidia, hybrid-gpu, suspend-sleep, asus-zenbook-vivobook, hibernate-fails-or-hangs]
draft: false
---

## Verdict

Bronze. ASUS ROG is one of the very few laptop families Omarchy names by hand. Release [v3.4.0](https://github.com/omacom/omarchy/releases/tag/v3.4.0) in February 2026 shipped what its notes call full Zephyrus G14 and G16 compatibility: screen and keyboard brightness, volume keys, a hybrid GPU switch under _Trigger > Hardware_, and keyboard backlighting that follows your theme. That work is all still in the 4.0.4 tree.

The problem is everything around it. Of the 17 Zephyrus issues in the tracker, 13 are open, and they are not cosmetic. The 2024 and 2025 Strix Point G14 can black screen before you ever see a desktop. Hibernate ends in a forced power off on two separate G14 reports. The audio script that makes ROG speakers work also caps them below what the hardware can do.

Everything below was checked against the v4.0.4 source tree on 2026-09-16. Where a fix landed in 3.x it is noted; nothing here is a 4.x regression from 3.8.4 unless it says so.

## What works

The ROG specific enablement is genuine. `install/hardware/asus-rog.sh` installs `asusctl` on any machine where `omarchy-hw-asus-rog` passes, and Omarchy carries `asusctl 6.4.0-1` in its own stable channel repo rather than leaving you to the AUR. `omarchy-theme-set-keyboard-asus-rog` pushes your theme color to the keyboard through `asusctl aura effect static`.

Hybrid graphics have a first class path. `omarchy-toggle-hybrid-gpu` installs `supergfxctl` on demand, writes `/etc/supergfxd.conf`, and flips between Hybrid and Integrated. Integrated mode is what buys you battery life on these machines. A closed bug, [#5428](https://github.com/omacom/omarchy/issues/5428) on a G16 GU605CR, had the menu entry vanish after switching to Integrated because detection counted PCI display devices; DHH replied in the thread that GPU detection was rewritten for 3.6.1, and v4.0.0 added a timeout so a wedged `supergfxd` cannot hang the menu.

Suspend on the Strix side improved. [#7303](https://github.com/omacom/omarchy/issues/7303), a hard s2idle freeze on a Strix G16 G614FR, was closed by its own reporter with a note that it was resolved in 4.0.1 on stable.

Community reports in the earlier prototype of this site rated a 2023 G14 and a Strix G18 as ordinary installs. Those are single owner reports, not something we reproduced, so treat them as encouragement rather than evidence.

## What breaks

**Boot black screen on Strix Point G14.** [#9720](https://github.com/omacom/omarchy/issues/9720) is open. On a GA403 with a Ryzen AI 9 HX 370 and Radeon 890M, Hyprland stalls at `[AQ] atomic drm request: failed to commit: Cannot allocate memory`. The workaround is `AQ_NO_ATOMIC=1` plus `WLR_NO_HARDWARE_CURSORS=1`, and the important detail from codyoss is that Aquamarine reads the environment before it reads your Lua config, so setting it with `hl.env()` is too late. Put it in `~/.config/uwsm/env-hyprland`.

**Hibernate.** Two open issues, two different mechanisms, same ending. [#9696](https://github.com/omacom/omarchy/issues/9696) on a hybrid GA403UM: `asus-rog.sh` installs only `asusctl`, so `supergfxctl` and the `force-igpu` sleep hook are absent on a fresh install even though that hook's own comments describe this exact failure on a G14. The machine writes the image, fails to power off, and deadlocks `amdgpu` reset against the LUKS worker. [#8589](https://github.com/omacom/omarchy/issues/8589) on an iGPU only GA403UV: `swsusp_save()` aborts silently under the default `HibernateMode=platform`, and `HibernateMode=shutdown` in `/etc/systemd/sleep.conf.d/` fixes it. Its author is explicit that this is one machine and one BIOS.

**Audio is capped and, on some models, wrong.** `fix-audio-mixer.sh` enables WirePlumber's soft mixer and then sets the ALC285 hardware Master to 80 percent. With the soft mixer on, PipeWire never touches that control again. [#11046](https://github.com/omacom/omarchy/issues/11046) measured this on a G16 GA605KM: step 70 of 87, which is 12.75 dB below full scale, so the bar showing 100 percent is a lie. [#8359](https://github.com/omacom/omarchy/issues/8359) argues the blanket soft mixer actively hurts smart amp ROG models like the Strix G733ZW. [#4821](https://github.com/omacom/omarchy/issues/4821) is the one to read if your headphone jack is silent: the kernel's ALC285 jack handler keeps resetting the Headphone switch to off, and the soft mixer stops PipeWire from undoing that. Deleting `~/.config/wireplumber/wireplumber.conf.d/alsa-soft-mixer.conf` fixed it for the reporter and for commenters on a G16 GA605WI, an M16 GU603ZEB and a G14.

**Resume.** [#8491](https://github.com/omacom/omarchy/issues/8491) on a GA402XV in MUX dGPU mode: the shell survives resume but loses its EGL context and stops rendering, logging thousands of failed frames until `omarchy restart shell`. Two of four recorded events recovered on their own. [#7811](https://github.com/omacom/omarchy/issues/7811) on a GA403UM: after a lid open resume the lock screen draws but never receives keyboard input, so you cannot type your password.

**Power and battery.** [#9678](https://github.com/omacom/omarchy/issues/9678) on a Strix G16 G614FM shows the dGPU pinned at its 50 W default TGP because `nvidia-powerd` is never enabled. We confirmed no `nvidia-powerd` reference anywhere in `install/hardware/nvidia.sh` at v4.0.4. [#7374](https://github.com/omacom/omarchy/issues/7374) has the power panel reporting a 75 to 80 percent charge limit that came from a UPower hwdb default rather than from `asusctl`.

**Video decode.** [#11460](https://github.com/omacom/omarchy/issues/11460) on a GA401QC: `default/hypr/nvidia.lua` sets `LIBVA_DRIVER_NAME=nvidia` whenever any NVIDIA GPU exists, without asking which GPU drives the panel. On these muxless units the panel hangs off the AMD iGPU, so video plays audio over a black frame. Override with `hl.env("LIBVA_DRIVER_NAME", "radeonsi")`.

**Smaller things.** [#6949](https://github.com/omacom/omarchy/issues/6949) reports Fn plus F3 keyboard backlight dead on a GA401QE after an update, with no comments and no triage, so the evidence there is thin. [#7607](https://github.com/omacom/omarchy/issues/7607) on a GA403UI has the Display panel's internal monitor toggle reverted within seconds by the clamshell watcher.

## What Omarchy does for this model

Every ROG fix hangs off one predicate. `bin/omarchy-hw-asus-rog` is true when DMI `sys_vendor` is exactly `ASUSTeK COMPUTER INC.` and `product_family` contains `ROG`. It reads the family, never the product name, so a Zephyrus G14 and a Strix G733 get byte identical treatment. There is no DMI narrowing for any Zephyrus or Strix product name in the v4.0.4 tree.

That gate drives `asus-rog.sh` (asusctl), `fix-audio-mixer.sh`, `fix-mic.sh` and the keyboard theme sync. The only ASUS quirk that matches a product string is `install/hardware/asus/fix-z13-touchpad.sh`, gated on `omarchy-hw-asus-rog && omarchy-hw-match "GZ302"`, and GZ302 is the ROG Flow Z13, not a Zephyrus. The Panther Lake ASUS fixes in `install/hardware/asus/` target the ExpertBook B9406 and Zenbook UX5406AA and will not fire on your machine.

## Variants

GA401 units from 2021 are the calmest on paper, with only the Fn plus F3 report and the VA-API one against them, both with workarounds. GA402 from 2023 adds the resume rendering stall in MUX dGPU mode. GA403, the 2024 and 2025 Strix Point and Hawk Point G14, carries the boot black screen and both hibernate reports, so budget an evening for it. On the G16 side, GU605 with Intel Core Ultra plus an RTX 50 had the hybrid menu bug that is already fixed, and GA605 is where the audio ceiling was measured. Strix G614 and G733 share the TGP cap and the smart amp audio complaint.

Prefer a unit whose panel you are happy to run at the default scale, since the OLED G14 needs a scale set by hand in `monitors.lua`. Avoid buying a brand new chassis generation in the first months if a black screen at first boot would ruin your week.

## Before you install

- Read [/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/) before the first boot on a GA403. Know the `AQ_NO_ATOMIC` trick in advance.
- Decide about hibernate. Check [/fix/hibernate-fails-or-hangs/](/fix/hibernate-fails-or-hangs/) and the manual's [System sleep](https://omarchy.org/manual/system-sleep/) chapter, and be ready to run `omarchy hibernation remove` rather than discover the hang the hard way.
- Run the hybrid GPU toggle once, early. It is what installs `supergfxctl` and the `force-igpu` sleep hook, and it is also your battery life.
- Check the real speaker volume with `amixer` on the ALC285 card after install. See [/hardware/audio/](/hardware/audio/).
- If you game, enable `nvidia-powerd` yourself or accept base TGP. Background on the driver path is at [/hardware/nvidia/](/hardware/nvidia/).
- Keep an external keyboard nearby for the lock screen input bug, and know that `omarchy restart shell` fixes a bar that stopped drawing.

## Related

- [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) and [/hardware/nvidia/](/hardware/nvidia/) for the driver and mux story
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/hardware/battery-power/](/hardware/battery-power/)
- [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/asus-zenbook-vivobook/](/hardware/asus-zenbook-vivobook/) for the non ROG ASUS machines
- [/releases/still-broken/](/releases/still-broken/) for what is open right now, and [/hardware/submit/](/hardware/submit/) if your Zephyrus behaves differently
