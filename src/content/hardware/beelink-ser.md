---
title: "Beelink SER8, SER9 and other Beelink mini PCs on Omarchy"
description: "Beelink SER8, SER9, EQR and GTR mini PCs on Omarchy 4.0.4: suspend broken by Beelink firmware, AX200 Wi-Fi that needs a power drain, and what actually works."
answer: "Buy it. A Beelink SER runs Omarchy well as an always-on desk machine, and Omarchy ships no Beelink-specific setup because none is needed. Two things are not fixed: suspend is broken by Beelink firmware on the HX 370 and Strix Halo units, and idle screen blanking can wedge or loop the display on AMD integrated graphics. Plan to leave it running."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Beelink"
model: "Beelink SER / EQ / GTR mini PCs"
dmi: ["AZW", "SER8", "SER", "GTR Pro"]
year: "2023-2026"
cpu: "AMD Ryzen 7 8745HS / 8845HS (Hawk Point), Ryzen AI 9 HX 370 (Strix Point), Ryzen AI Max+ 395 (Strix Halo), Ryzen 5 5500U / 7535U on older SER5 and EQR units"
gpu: "AMD Radeon 780M / 760M / 660M / 8060S integrated (amdgpu)"
rating: silver
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: unknown
  webcam: n/a
  fingerprint: n/a
  gpu: partial
  suspend: broken
  hibernate: unknown
  touchpad: n/a
  display: partial
  battery: n/a
  keyboard: n/a
quirkScripts: []
issueCount: 27
tags: [beelink, ser8, ser9, mini-pc, amd, amdgpu, suspend]
sources:
  - url: "https://github.com/omacom/omarchy/issues/394"
    title: "Issue #394: suspend on BeeLink SER9 (and new Framework 13 AMD Ryzen AI 9 HX 370)"
    kind: issue
    author: "marcinczenko"
    date: "2025-07-29"
  - url: "https://github.com/omacom/omarchy/issues/2202"
    title: "Issue #2202: Wifi does not work on Beelink SER9 PRO"
    kind: issue
    author: "ocewers"
    date: "2025-10-04"
  - url: "https://github.com/omacom/omarchy/issues/374"
    title: "Issue #374: Problems with Display Port over USB4 (BeeLink SER9)"
    kind: issue
    author: "marcinczenko"
    date: "2025-07-27"
  - url: "https://github.com/omacom/omarchy/issues/1893"
    title: "Issue #1893: Plymouth Login screen not showing on external monitor connected via Thunderbolt dock"
    kind: issue
    author: "sgruendel"
    date: "2025-09-23"
  - url: "https://github.com/omacom/omarchy/pull/1894"
    title: "PR #1894: Add thunderbolt module in omarchy hook"
    kind: pr
    author: "sgruendel"
    date: "2025-09-23"
  - url: "https://github.com/omacom/omarchy/issues/5910"
    title: "Issue #5910: Default hypridle.conf wedges display on AMD Phoenix/HawkPoint iGPUs"
    kind: issue
    author: "ordanalabs"
    date: "2026-05-19"
  - url: "https://github.com/omacom/omarchy/issues/8689"
    title: "Issue #8689: Lock screen alternates black <-> lock UI every ~13.5s on AMD iGPU over HDMI"
    kind: issue
    author: "williavs"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/10852"
    title: "Issue #10852: AMD display freeze retains valid mode and active CRTC, bypassing monitor recovery; DPMS restores session"
    kind: issue
    author: "theinventor"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11376"
    title: "Issue #11376: SDDM's Hyprland compositor repeatedly crashes with SIGSEGV as the login greeter exits after successful authentication"
    kind: issue
    author: "rclinux"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/6380"
    title: "Issue #6380: Suspend does not work anymore in 3.8.4 (worked in 3.8.2)"
    kind: issue
    author: "hirschnase"
    date: "2026-07-26"
  - url: "https://github.com/omacom/omarchy/issues/1485"
    title: "Issue #1485: The system doesn't boot after install"
    kind: issue
    author: "wavic"
    date: "2025-09-06"
  - url: "https://github.com/omacom/omarchy/discussions/136"
    title: "Discussion #136: CalDigit TS4 + Beelink SER8 + Arch Linux + Apple Studio Display 5K Setup"
    kind: discussion
    author: "melonamin"
    date: "2025-07-12"
credits:
  - name: "mfornasa"
    url: "https://github.com/mfornasa"
    for: "Traced the SER9 suspend failure to Beelink firmware with help from AMD, and filed it upstream"
  - name: "sudhir-b"
    url: "https://github.com/sudhir-b"
    for: "Found that a full power drain brings the dead Wi-Fi card back"
  - name: "sgruendel"
    url: "https://github.com/sgruendel"
    for: "Diagnosed the missing thunderbolt module and wrote the PR that fixed it"
  - name: "ordanalabs"
    url: "https://github.com/ordanalabs"
    for: "Pinned the display wedge on Hawk Point boxes to the DPMS-off path in the idle config"
  - name: "Abdullah-00"
    url: "https://github.com/Abdullah-00"
    for: "Identified the atlantic 10GbE driver as the suspend blocker on the SER10 Max"
faq:
  - q: "Can I make suspend work on a Beelink SER9?"
    a: "Probably not. mfornasa tested with an AMD engineer and reported that the BIOS does not configure the devices correctly, and that suspend will not work until Beelink ships new firmware. Check your BIOS version first, then plan around it: power off, or leave the machine on and let the screen turn off."
  - q: "My Beelink lost its Wi-Fi card and iwctl shows no devices. What now?"
    a: "Shut down, unplug the power brick, hold the power button for 30 to 90 seconds, wait, then plug in and boot. That restored the Intel AX200 for several people in issue #2202. If it comes back repeatedly, Beelink support advised a CMOS clear with the pinhole reset."
  - q: "Does Omarchy install anything specific for Beelink hardware?"
    a: "No. Nothing in the v4.0.4 tree matches a Beelink DMI string. You get the generic AMD path: the amdgpu kernel driver, vulkan-radeon from install/hardware/vulkan.sh, and the thunderbolt module in the initramfs."
  - q: "SER8 or SER9 for Omarchy?"
    a: "The SER8 with the Radeon 780M is the better documented machine and the one most Omarchy users run. The SER9 with the HX 370 is faster and has the firmware suspend bug on record. Neither choice avoids the amdgpu blanking problems."
related: [amd-gpu, suspend-sleep, thunderbolt-dock, minisforum, framework-desktop]
draft: false
---

## Verdict

Silver. A Beelink SER is a good, cheap Omarchy desk machine, and it needs nothing special from you at install time. Omarchy 4.0.4 contains no Beelink-specific code at all, which is the compliment it sounds like: the AMD integrated graphics take the generic amdgpu path and just work.

It is not gold for two reasons. Suspend is broken at the firmware level on the Ryzen AI HX 370 and Strix Halo units, and Beelink has not fixed it. And the AMD integrated GPUs in these boxes have a long history of wedging or flapping when Omarchy turns the display off for idle or lock. If you want a machine you close the lid on, this is not it. If you want a box that stays on a desk and stays awake, it is one of the better value choices in the Omarchy community.

Across the tracker, 27 issues mention Beelink hardware, 24 of them closed. The reporting is real and sustained, not a handful of one-off posts.

## What works

Day to day, the basics are boring in the good way. Ethernet, the AMD integrated GPU, NVMe storage, and multi-monitor output over HDMI and DisplayPort all come up on a plain install. DHH has said he runs a SER9 with the HX 370 and that Wi-Fi is fine on it ([#2202](https://github.com/omacom/omarchy/issues/2202)).

Thunderbolt and USB4 docks work, including the awkward cases. A SER8 owner documented a full CalDigit TS4 setup driving an Apple Studio Display 5K over a single cable in [discussion #136](https://github.com/omacom/omarchy/discussions/136). Docked boot used to leave the LUKS prompt on a black screen because the `thunderbolt` module was missing from the initramfs; sgruendel reported that as [#1893](https://github.com/omacom/omarchy/issues/1893) and fixed it in [PR #1894](https://github.com/omacom/omarchy/pull/1894). Omarchy 4.0.4 ships `etc/mkinitcpio.conf.d/thunderbolt_module.conf` with `MODULES+=(thunderbolt)`, so new installs get it automatically.

Installs are fast. That is a function of the NVMe drive more than the CPU, and these boxes ship decent ones.

## What breaks

**Suspend, on HX 370 and Strix Halo.** This is the big one. Issue [#394](https://github.com/omacom/omarchy/issues/394) has run since July 2025. The machine tries to suspend, the fans spin up, it wakes within seconds, and the network interfaces do not come back. mfornasa took it to an AMD engineer and reported the likely cause as the BIOS failing to configure devices properly, tracked upstream at `gitlab.freedesktop.org/drm/amd/-/issues/4519`. His conclusion was blunt: without new Beelink firmware, suspend is not going to work. The same behaviour is reported on the GTR9 Pro with the Ryzen AI Max+ 395. DHH commented on the thread that he stopped bothering with suspend and pointed out that idle draw is about 8 watts anyway. See [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/) and the manual chapter on [system sleep](https://omarchy.org/manual/system-sleep/).

**Wi-Fi that disappears entirely.** In [#2202](https://github.com/omacom/omarchy/issues/2202) the Intel AX200 in a SER9 Pro stopped probing, with `iwlwifi 0000:c3:00.0: probe with driver iwlwifi failed with error -110` and no device listed at all. Kernel and firmware updates did not help. What did: a full power drain. Shut down, unplug, hold the power button 30 to 90 seconds, reconnect, boot. jondkinney reported that Beelink support recommended a CMOS clear through the pinhole for the same symptom. A botched suspend can put the card into this state, which ties the two problems together. More at [/fix/wifi-drops-after-kernel-update-iwlwifi/](/fix/wifi-drops-after-kernel-update-iwlwifi/).

**Screen blanking wedges the display.** In [#5910](https://github.com/omacom/omarchy/issues/5910), ordanalabs showed that the DPMS-off path in Omarchy 3.x hung the display controller on Phoenix and Hawk Point integrated GPUs, confirmed on a SER8, with `REG_WAIT timeout` from `optc314_disable_crtc` in the kernel log and no recovery short of the power button. DHH closed it because Quattro replaced the old hyprlock and hypridle stack. The symptom did not disappear with it. [#8689](https://github.com/omacom/omarchy/issues/8689) is open on Omarchy 4.0.1, on a Beelink EQR7 with a Radeon 660M over HDMI: the new lock plugin blanks the display five seconds after lock, amdgpu emits a spurious disconnect, Hyprland drops and re-adds the output, and the lock screen cycles black roughly every 13.5 seconds. See [/hardware/amd-gpu/](/hardware/amd-gpu/).

**Display freezes with the session still alive.** [#10852](https://github.com/omacom/omarchy/issues/10852) on a Beelink GTR Pro with Strix Halo describes scanout stopping while SSH and Hyprland IPC kept working, with a DPMS off and on cycle restoring the session. The reporter closed it on 2026-09-14 after six days without a recurrence on Aquamarine 0.15.0, which was a package upgrade rather than a verified fix.

**Login greeter crash on amdgpu.** In a comment on [#11376](https://github.com/omacom/omarchy/issues/11376), sparkrussell reported an AZW SER box with a Ryzen 5 5500U on Omarchy 4.0.3 where the SDDM greeter's Hyprland segfaults in libaquamarine on every boot, and once took the kernel down with it in an amdgpu hard lockup. Mostly harmless, occasionally not. See [/fix/login-loop-or-password-not-accepted-sddm/](/fix/login-loop-or-password-not-accepted-sddm/).

**DisplayPort over USB4.** [#374](https://github.com/omacom/omarchy/issues/374) on a SER9: a 5K display works over the USB4 port until you reboot, after which the monitor reports no signal. DHH's advice on the thread was that DisplayPort over USB-C is generally poor on Linux and to use the native DisplayPort output. That still holds. See [/hardware/multi-monitor/](/hardware/multi-monitor/).

## What Omarchy does for this model

Nothing model-specific. There is no Beelink DMI match anywhere in the v4.0.4 tree. `omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `product_family`, and every caller of it targets Asus, Dell, Framework, Lenovo, Surface or Apple hardware. `install/hardware/all.sh` never branches for Beelink.

What you actually get is the generic path:

- `install/hardware/vulkan.sh` sees an AMD display controller in `lspci` and installs `vulkan-radeon`.
- `install/hardware/bluetooth.sh` enables `bluetooth.service`.
- `install/hardware/network.sh` retires stale systemd-networkd state and leaves NetworkManager in charge. Quattro moved Wi-Fi management from iwd to NetworkManager, so 3.x advice about `iwd.conf` no longer applies.
- `install/hardware/set-wireless-regdom.sh` writes the regulatory domain from your timezone.
- `etc/mkinitcpio.conf.d/thunderbolt_module.conf` puts `thunderbolt` in the initramfs.

No firmware blobs, no speaker tuning, no DMI quirk. The DMI strings owners have posted are the vendor `AZW` and product names like `SER8` and `SER`. Nothing in Omarchy reads them.

## Variants

**SER8 (Ryzen 7 8745HS or 8845HS, Radeon 780M).** The most reported unit and the safest buy. Its weakness is the Hawk Point display wedge in [#5910](https://github.com/omacom/omarchy/issues/5910).

**SER9 and SER9 Pro (Ryzen AI 9 HX 370).** Faster, and the machine with the documented firmware suspend bug. Also the machine in the AX200 Wi-Fi thread.

**SER10 Max.** In [#6380](https://github.com/omacom/omarchy/issues/6380) an owner traced a hard suspend hang to the Aquantia AQC113 10GbE controller on the `atlantic` driver, which logged `atlantic: Boot code hanged` after resume. Unloading `atlantic` before sleep and reloading it after fixed suspend and hibernate for them. If you want 10GbE on a Beelink, budget for that workaround.

**GTR9 Pro and GTR Pro (Ryzen AI Max+ 395, Strix Halo).** Same suspend failure as the SER9, plus the Strix Halo display freeze in [#10852](https://github.com/omacom/omarchy/issues/10852).

**Older SER5, EQR5 and EQR7 (Ryzen 5 5500U, 7535U).** Cheap and fine for light use, but they are where the amdgpu lock screen loop and the greeter segfault show up.

## Before you install

- Update the BIOS from Beelink before you install anything. The suspend bug is firmware, and firmware is the only place it can be fixed.
- Install over Ethernet. If Wi-Fi is missing at first boot, do a full power drain before you start debugging drivers.
- Connect your main monitor to the native HDMI or DisplayPort output, not the USB4 port, at least for the install and the first boot.
- If you use a Thunderbolt dock, run the install on a directly attached display, then move to the dock afterwards.
- Expect to disable or lengthen idle screen blanking. That single setting is behind most of the AMD display complaints on these boxes.
- If a black screen at the LUKS prompt stops you cold, `nomodeset` on the kernel command line got several AMD Beelink owners to a working install in [#1485](https://github.com/omacom/omarchy/issues/1485). Treat it as a temporary crutch, not a setting to keep.

## Related

- [/hardware/amd-gpu/](/hardware/amd-gpu/) for the amdgpu problems that dominate this page
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/thunderbolt-dock/](/hardware/thunderbolt-dock/) for dock and USB4 display behaviour
- [/hardware/minisforum/](/hardware/minisforum/) for the other common AMD mini PC
- [/hardware/submit/](/hardware/submit/) if you own one of these and can confirm or correct anything here
