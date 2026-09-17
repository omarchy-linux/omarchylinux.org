---
title: "Lenovo ThinkPad X220, X230, T420 and T430 on Omarchy Linux"
description: "Classic ThinkPads on Omarchy 4.0.4: the X220 is the project's own potato demo, but scaling, VA-API, dictation and dual-battery reporting all need hand work."
answer: "Rate the classic ThinkPad class bronze. Omarchy boots and runs well on an X220 or X230, and omarchy.org uses a 2 GB 2011 X220 as its old-hardware showcase. Expect real hand work: set scaling to 1 on a 1366x768 panel, install libva-intel-driver yourself, skip dictation on pre-AVX2 chips, and watch for an unresolved Mesa rendering regression on old Intel graphics."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [lenovo, thinkpad, x220, old-hardware, intel-gpu, potato]
kind: model
vendor: "Lenovo"
model: "ThinkPad X220, X230, T420, T430 and other classics"
dmi: []
cpu: "Intel Core 2nd gen (Sandy Bridge) and 3rd gen (Ivy Bridge); Haswell on the T440 series"
gpu: "Intel HD Graphics 3000 and 4000, integrated"
year: "2011-2014"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: unknown
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: partial
  keyboard: unknown
quirkScripts:
  - name: "intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Installs and enables thermald on any Intel laptop with a battery and CPU model 42 or higher. The comment names Sandy Bridge as the floor, so an X220 or T420 qualifies."
  - name: "intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Picks the VA-API driver by lspci name. HD 4000 matches \"hd graphics\" and gets intel-media-driver, which only supports Broadwell and newer. The HD 3000 lspci name matches neither branch, so nothing is installed. Both need libva-intel-driver. See issue #7866."
  - name: "vulkan.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/vulkan.sh"
    note: "Installs vulkan-intel whenever lspci reports an Intel display device, with no generation check. That gives you nothing usable before Haswell, and a crashing device on Haswell."
  - name: "fix-synaptic-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-synaptic-touchpad.sh"
    note: "Enables Synaptics InterTouch on psmouse when the running kernel can resolve the module. Not ThinkPad specific, and it only takes effect when run on the booted machine."
issueCount: 9
sources:
  - url: "https://omarchy.org/potato/"
    title: "Omarchy on Old Hardware (the potato page)"
    kind: docs
    author: "omacom"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/5979"
    title: "Issue #5979: rendering glitch after update from 3.8.0 to 3.8.2"
    kind: issue
    author: "SantosVilanculos"
    date: "2026-05-26"
  - url: "https://github.com/omacom/omarchy/issues/7301"
    title: "Issue #7301: DE scaling defaullts to 2 & screensaver overrides scaling settiing"
    kind: issue
    author: "mikl0s"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7866"
    title: "Issue #7866: video-acceleration.sh installs wrong VA-API driver for Intel HD 4000 (Ivy Bridge)"
    kind: issue
    author: "BlueBirdBack"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/4062"
    title: "Issue #4062: Lenovo x230: Ghostty unable to acquire a OpenGL"
    kind: issue
    author: "gustavdias"
    date: "2026-01-02"
  - url: "https://github.com/omacom/omarchy/issues/4554"
    title: "Issue #4554: Upgrade issues on older CPU"
    kind: issue
    author: "richard-sistern"
    date: "2026-02-08"
  - url: "https://github.com/omacom/omarchy/issues/8197"
    title: "Issue #8197: omarchy voxtype install has no source-build fallback for pre-AVX2 CPUs"
    kind: issue
    author: "rowan5now"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/11370"
    title: "Issue #11370: Voxtype install enables Vulkan on Haswell (hasvk) GPUs, causing an endless SIGABRT crash loop"
    kind: issue
    author: "llyorshch"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/8303"
    title: "Issue #8303: Power panel only reads the first battery on dual-battery hardware (ignores real combined charge, no per-battery breakdown)"
    kind: issue
    author: "jadonfloyd"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7916"
    title: "Issue #7916: Power panel reports dead BAT0 (0% / 0W / Holding) on dual-battery ThinkPads"
    kind: issue
    author: "hilather"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8523"
    title: "Issue #8523: omarchy-brightness-display: Brightness trapped at 0% on displays with low max_brightness (acpi_video0)"
    kind: issue
    author: "gorem"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro) release notes"
    kind: release
    author: "omacom"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.4.0"
    title: "Release v3.4.0 release notes"
    kind: release
    author: "omacom"
    date: "2026-02-26"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
    author: "omacom"
    date: "2026-09-16"
  - url: "https://omarchypulse.com/articles/omarchy-on-a-potato"
    title: "Omarchy on a potato: X220 numbers, and how low you can go"
    kind: blog
    date: "2026-08-23"
credits:
  - name: "SantosVilanculos"
    url: "https://github.com/SantosVilanculos"
    for: "Reported the garbled rendering that hit old Intel graphics after 3.8.2"
  - name: "7oo1er"
    url: "https://github.com/7oo1er"
    for: "Narrowed the X220 rendering glitch to a Mesa upgrade and documented the downgrade and IgnorePkg workaround"
  - name: "braintornapart"
    url: "https://github.com/braintornapart"
    for: "Confirmed the same glitch on a second X220 with an i5-2540M"
  - name: "BlueBirdBack"
    url: "https://github.com/BlueBirdBack"
    for: "Showed that the Intel video acceleration script routes HD 4000 to the wrong VA-API driver"
  - name: "mikl0s"
    url: "https://github.com/mikl0s"
    for: "Reported the 1366x768 scaling reset after the screensaver on an X250 running Quattro"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Rebuilt limine-mkinitcpio-hook with compatibility flags so pre-AVX2 CPUs could finish an update"
  - name: "hllstr"
    url: "https://github.com/hllstr"
    for: "Wrote the x86-64-v2 rescue guide other owners used while that build was broken"
faq:
  - q: "Will Omarchy run on a ThinkPad X220 with 2 GB of RAM?"
    a: "Yes, and that exact machine is the demo on the project's potato page. A third-party writeup measured about 890 MB at idle on an i5-2520M X220 running Quattro. Browser and Electron work is where 2 GB runs out, so buy the 8 GB stick before you buy anything else."
  - q: "Why is everything huge after I install on a 1366x768 ThinkPad?"
    a: "Omarchy ships omarchy_gdk_scale = 2 in ~/.config/hypr/monitors.lua because it assumes a high resolution display. Set it to 1 and set a numeric monitor scale. On issue #7301 the screensaver wake path put the scale back to 2 until the file was touched again."
  - q: "Is hardware video decode working on HD 3000 and HD 4000?"
    a: "Not out of the box on 4.0.4. The install script installs intel-media-driver, which starts at Broadwell. Install libva-intel-driver and check vainfo. Issue #7866 is open and PR #8514 is the fix still in review."
related: [intel-gpu, battery-power, lenovo-thinkpad-t480, boot-limine, touchpad-input]
draft: false
---

## Verdict

Bronze. A classic ThinkPad runs Omarchy, and the project leans on that fact: the project's own [old hardware page](https://omarchy.org/potato/) is a 2011 ThinkPad X220 with 2 GB of RAM. The desktop itself is not the problem. Everything around the desktop is.

On Omarchy 4.0.4 this class of machine hits a default display scale meant for a 4K panel, an Intel video acceleration script that installs a driver its GPU generation cannot use, a dictation installer that hands pre-AVX2 CPUs a binary they cannot execute, and an unresolved rendering regression on old Intel graphics. None of that is fatal. All of it is manual. If you want a used ThinkPad that mostly just works, buy a [T480](/hardware/lenovo-thinkpad-t480/) instead and keep the X220 as the cheap second machine it is good at being.

This page covers the X220 and X230, the T420 and T430, and by extension the Haswell T440 series. Two of the cited reports come from the Broadwell X250 and T450, which ride the same generic Intel path. Everything was checked against the v4.0.4 source tree and the issue tracker on 2026-09-16.

## What works

The shell runs. A third-party measurement of an X220 with an i5-2520M and 2 GB of RAM under Quattro reported roughly 890 MB used at idle with Hyprland, the Quickshell bar and a Foot terminal, and about 1.3 GB with browser tabs, video and a recorder going. Treat those as one person's numbers, not a guarantee.

Two defaults help this hardware specifically. Since v4.0.0 the default terminal is Foot, which the manual describes as compatible with even old computers, and the v3.4.0 notes say the default was moved off Ghostty precisely so old systems without compatible GPUs could run Omarchy out of the box. Thermal management is also handled: `install/hardware/intel/thermald.sh` installs and enables thermald on any Intel laptop with a battery and a CPU model of 42 or higher, and its own comment names Sandy Bridge as that floor.

The pre-AVX2 update failure from early 2026 is fixed. Issue #4554 had owners of i5-3210M and similar chips stuck when the Limine unified kernel image build refused to run, reporting a missing list of CPU features including AVX2 and BMI2. ryanrhughes closed it on 2026-02-22 after tracing it to the `limine-mkinitcpio-hook` build and rebuilding it with compatibility flags in the Omarchy package repository. A fresh 4.0.4 install pulls that rebuilt package, so the failure should not recur.

Wi-Fi, Bluetooth, audio, webcam, fingerprint, suspend, hibernate, touchpad and keyboard are marked unknown. Nobody has filed a 4.x report for these machines on any of them, in either direction, and the tracker only proves what breaks.

## What breaks

**Rendering glitches after a Mesa update.** Issue #5979 is open. Owners of an X220 with an i5-2540M and an i5-2520M saw garbled text and corrupted cursors after moving to 3.8.2. Hyprland's maintainer noted in the thread that everyone reporting it was on old Intel, and one owner fixed it by downgrading Mesa from cache and pinning it with `IgnorePkg`. No fix has landed in Omarchy, and the thread has been quiet since 2026-05-30. This is the single reason to keep snapshots on this hardware.

**Display scale defaults to 2.** `config/hypr/monitors.lua` in v4.0.4 still ships `local omarchy_gdk_scale = 2`, and the manual confirms Omarchy assumes a 2x display. On a 1366x768 panel that is close to unusable. Issue #7301, filed on an X250 running Quattro, adds a second problem: after the screensaver ran, the scale went back to 2 until the file was saved again. It is still open. See the [monitors chapter](https://omarchy.org/manual/monitors/) for the values to set.

**VA-API gets the wrong driver.** Issue #7866 is open. `install/hardware/intel/video-acceleration.sh` picks the driver by lspci name. An HD 4000 reports as "Ivy Bridge mobile GT2 [HD Graphics 4000]", matches the "hd graphics" branch and gets `intel-media-driver`, which only covers Broadwell and newer. An HD 3000 reports as "2nd Generation Core Processor Family Integrated Graphics Controller", matches neither branch, and gets nothing. Either way there is no working VA-API driver. A second reporter on an Ivy Bridge machine found `vaInitialize` failing outright rather than merely dropping frames. Of the two fixes, #8490 was closed in favour of #8514, which selects the package by PCI device ID and is still open.

**Dictation on pre-AVX2 chips.** Issue #8197 reports the prebuilt voxtype binary dying with SIGILL on an Ivy Bridge i5-3210M, with no warning from the installer. The upstream maintainer said in the thread that pre-AVX2 binaries would ship from voxtype 1.0.1. That did not happen: 1.0.1 shipped on 2026-08-31 with AVX2 and AVX-512 builds only, and the x86-64-v2 "baseline" variant exists so far only in the 1.1.0 release candidates, with the AUR packages due to pick it up at the 1.1.0 stable release. On Haswell it is worse: issue #11370 describes `omarchy-hw-vulkan` seeing any Vulkan ICD as good enough, enabling GPU offload on a Mesa hasvk device that cannot support it, and leaving a systemd restart loop that produced roughly 127,000 core dumps. See [dictation not working](/fix/dictation-voxtype-not-working/).

**Two batteries, one reading.** If you run a slice or Ultrabay battery, the power panel lies. `omarchy-battery-status` in v4.0.4 still picks a single device with `upower -e | grep BAT | head -n 1`. Issues #8303 and #7916 are both open and both from ThinkPad owners, including a case where a dead BAT0 made the panel report 0% while the live pack was nearly full. Two pull requests, #8864 for the aggregate reading and #8904 for a per-battery breakdown, were still open on 2026-09-16.

**Brightness can trap at zero.** Issue #8523 is open: on panels using `acpi_video0` with a `max_brightness` of 15, stepping down to 0% leaves the backlight stuck, because a 1% step rounds back to raw zero. A commenter reproduced it on 4.0.2 with Ivy Bridge HD 4000. Do not hold the brightness-down key.

**Terminal choice, on 3.x.** Issue #4062 is closed: an X230 with HD 4000 could not get an OpenGL context for Ghostty in January 2026, and the answer was to use Alacritty. On 4.x the default is Foot, so you only meet this by choosing Ghostty or Kitty yourself.

## What Omarchy does for this model

Nothing model specific. There is no ThinkPad DMI match anywhere in v4.0.4. `bin/omarchy-hw-match` greps only `/sys/class/dmi/id/product_name` and `product_family`, and the only Lenovo script in `install/hardware/lenovo/` targets the Yoga Pro 7 14IAH10. Classic ThinkPads are carried entirely by the generic Intel path, so check what your machine actually reports before assuming a future quirk would match it:

```
cat /sys/class/dmi/id/product_name /sys/class/dmi/id/product_family /sys/class/dmi/id/product_version
```

Of the generic scripts, thermald helps, the video acceleration script hurts, and `vulkan.sh` installs `vulkan-intel` on any Intel display device with no generation check. `omarchy-hw-intel-sof` matches any Intel audio device by name, so these machines also pull `sof-firmware` they will never load. That one is harmless.

## Variants

Prefer an X230 or T430 over an X220 or T420 if the price is close, mostly for the newer chipset and USB 3. Prefer any of them with 8 GB or more and an SSD. The potato writeup makes the same point bluntly: a cheap SATA or mSATA SSD does more for responsiveness than any software tweak.

Avoid buying a 2 GB machine for browser work. Avoid counting on the dictation and AI features that the rest of Omarchy assumes, because that is where pre-AVX2 CPUs fall over. If you specifically want a Haswell T440 or a Broadwell T450, know that the voxtype Vulkan crash loop in #11370 is a Haswell report, and that the T450 dual-battery report in #8303 is the same battery bug described above.

## Before you install

- Put in an SSD and at least 8 GB of RAM first.
- Take a snapshot habit seriously from day one, then read [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/). Mesa is the package most likely to ruin your week here.
- Right after first boot, open `~/.config/hypr/monitors.lua`, set `omarchy_gdk_scale` to 1, and set an explicit numeric monitor scale. Details in [fractional scaling](/fix/fractional-scaling-blurry-or-huge-apps/).
- Keep Foot as your terminal.
- If you want hardware video decode, install `libva-intel-driver` and verify with `vainfo` before you believe it.
- Skip dictation until the voxtype 1.1.0 baseline build reaches the package Omarchy installs.
- If you run a slice or Ultrabay battery, read the percentage from `upower -e` rather than the panel.

## Related

- [Intel graphics on Omarchy](/hardware/intel-gpu/)
- [Battery and power](/hardware/battery-power/)
- [ThinkPad T480](/hardware/lenovo-thinkpad-t480/)
- [Still broken in the current release](/releases/still-broken/)
- [Before you update checklist](/upgrade/before-you-update-checklist/)
