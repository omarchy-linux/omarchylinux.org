---
title: "Framework Desktop (Strix Halo) on Omarchy"
description: "Framework Desktop with Ryzen AI Max 385/395 on Omarchy 4.0.4: the amdgpu hard-lock issues, the DPMS reset on dual monitors, 6K DSC limits, and what to check before you buy."
answer: "Buy it with your eyes open. The Framework Desktop runs Omarchy 4.0.4 with no model-specific setup, and Omarchy ships no quirk script for it. The recurring problems are all amdgpu on Strix Halo: hard locks under Chromium, a hard reset when the screen blanks on dual external monitors, and DisplayPort DSC limits. On one display it is fine. On two or three, expect work."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Framework"
model: "Framework Desktop"
dmi: ["Desktop (AMD Ryzen AI Max 300 Series)"]
year: "2025"
cpu: "AMD Ryzen AI Max 385 / 395 / 395+ (Strix Halo)"
gpu: "AMD Radeon 8050S / 8060S integrated (amdgpu, PCI 1002:1586, DCN 3.5.1)"
rating: bronze
subsystems:
  wifi: works
  bluetooth: unknown
  audio: unknown
  webcam: n/a
  fingerprint: n/a
  gpu: partial
  suspend: unknown
  hibernate: unknown
  touchpad: n/a
  display: partial
  battery: n/a
  keyboard: n/a
quirkScripts: []
issueCount: 16
tags: [framework, framework-desktop, strix-halo, amd, amdgpu, desktop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6223"
    title: "Issue #6223: Crash and restart after omarchy-system-lock"
    kind: issue
    author: "filip-spaldon"
    date: "2026-07-14"
  - url: "https://github.com/omacom/omarchy/issues/5478"
    title: "Issue #5478: Hard Crash with AMD GPU on 3.6 since upgrade. Triggered by Chromium use"
    kind: issue
    author: "censey"
    date: "2026-04-28"
  - url: "https://github.com/omacom/omarchy/issues/5984"
    title: "Issue #5984: linux-firmware-amdgpu 20260519 (DMUB 0x09004700) black-screens Strix Halo + 5K DSC display"
    kind: issue
    author: "melonamin"
    date: "2026-05-27"
  - url: "https://github.com/omacom/omarchy/issues/3815"
    title: "Issue #3815: Framework Desktop + LG 6K: DSC inactive, stuck at 6K@30 (no 6K@60)"
    kind: issue
    author: "kvz"
    date: "2025-12-08"
  - url: "https://github.com/omacom/omarchy/issues/3816"
    title: "Issue #3816: linux-git (6.18.0-1-git) crashes on Framework Desktop (Strix Halo) before GUI"
    kind: issue
    author: "kvz"
    date: "2025-12-08"
  - url: "https://github.com/omacom/omarchy/issues/3918"
    title: "Issue #3918: Shutdown not working w/ thunderbolt monitor (system restarts)"
    kind: issue
    author: "raphaelstary"
    date: "2025-12-17"
  - url: "https://github.com/omacom/omarchy/issues/8114"
    title: "Issue #8114: [Quattro] omarchy-launch-screensaver creates focus-check race condition on 3+ monitor setups causing immediate self-termination"
    kind: issue
    author: "grhoades"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/5647"
    title: "Issue #5647: No internet access, but WiFi connects"
    kind: issue
    author: "pmpinto"
    date: "2026-05-07"
  - url: "https://github.com/omacom/omarchy/issues/3372"
    title: "Issue #3372: Framework desktop doesn't have it's gpu noticed"
    kind: issue
    author: "ColtonIdle"
    date: "2025-11-12"
  - url: "https://github.com/omacom/omarchy/issues/2278"
    title: "Issue #2278: Studio Display brightness not working / asdcontrol not present on a fresh install"
    kind: issue
    author: "miharekar"
    date: "2025-10-07"
  - url: "https://github.com/omacom/omarchy/issues/10852"
    title: "Issue #10852: AMD display freeze retains valid mode and active CRTC, bypassing monitor recovery; DPMS restores session"
    kind: issue
    author: "theinventor"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/discussions/3846"
    title: "Discussion #3846: Framework Desktop + LG 6K: DSC inactive, stuck at 6K@30 (no 6K@60)"
    kind: discussion
    author: "kvz"
    date: "2025-12-08"
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
credits:
  - name: "filip-spaldon"
    url: "https://github.com/filip-spaldon"
    for: "Bisected the DPMS hard reset to the kernel and found that amdgpu.dcdebugmask=0x800 prevents it"
  - name: "harkgill-amd"
    url: "https://github.com/harkgill-amd"
    for: "Worked the IPS entry path from the AMD side and supplied the ISM flush patch that stopped the reset"
  - name: "censey"
    url: "https://github.com/censey"
    for: "Found that raising the BIOS VRAM allocation stops the Chromium-triggered GPU lockups"
  - name: "andyjeffries"
    url: "https://github.com/andyjeffries"
    for: "Isolated the Chromium video decode flags that kept a 0.5 GB VRAM machine stable"
  - name: "melonamin"
    url: "https://github.com/melonamin"
    for: "Bisected the DMUB firmware regression that black-screened Strix Halo with a 5K DSC display"
  - name: "kvz"
    url: "https://github.com/kvz"
    for: "Documented the 6K DSC limit over DisplayPort and that Thunderbolt 4 works instead"
faq:
  - q: "Which Framework Desktop CPU should I pick for Omarchy?"
    a: "Both the Ryzen AI Max 385 and the 395/395+ are reported working. The open DPMS hard reset in issue #6223 was first reported on a 385 and later confirmed on 395 boxes too, so the chip choice does not avoid it. Pick on RAM and budget instead."
  - q: "Does Omarchy install anything special for the Framework Desktop?"
    a: "No. In the v4.0.4 tree the only Framework-specific script is omarchy-hw-framework16, which matches the DMI string Laptop 16. Nothing matches the Desktop, so it gets the generic AMD path: the amdgpu kernel driver plus vulkan-radeon from install/hardware/vulkan.sh."
  - q: "My machine hard resets when the screen blanks. What do I do now?"
    a: "Add amdgpu.dcdebugmask=0x800 to the kernel command line. filip-spaldon ran a clean A/B in issue #6223 and that bit, DC_DISABLE_IPS, was the only one that survived. The proper fix is an AMD ISM flush patch that had not reached a shipping kernel as of 2026-09-16."
related: [amd-gpu, multi-monitor, thunderbolt-dock, framework-laptop-13]
draft: false
---

The Framework Desktop is a 4.5 litre box built around AMD Strix Halo: a Ryzen AI Max 385, 395 or 395+ with Radeon 8050S or 8060S graphics and up to 128 GB of soldered unified memory. It is one of the machines the Omarchy community talks about most, and DHH runs one. It is also the machine that generates the most repeated amdgpu bug reports in the tracker.

## Verdict

Bronze. The machine installs and runs Omarchy with zero model-specific setup, and everything outside graphics is quiet. But the GPU is the whole computer here, and Strix Halo has produced three separate hard-lock classes on Omarchy in under a year, one of which is still open on 4.x.

The honest split is by display count. On a single monitor, owners report long uptimes and the rating would be silver. On two or three monitors, which is the obvious use for a box with this much RAM, you are likely to meet issue #6223 and will need a kernel parameter to get through a normal lock cycle. That is a real problem on a default workflow, so bronze is the fair call.

## What works

Installation is unremarkable. There is no dGPU to fight, no hybrid switching, no Secure Boot dance beyond the usual.

Wi-Fi associates and routes normally. The one Framework Desktop network report we could find, issue #5647, turned out to be a Mullvad service re-enabling itself on boot and was closed by the reporter as their own configuration.

Brightness control on an Apple Studio Display works now. Issue #2278 in October 2025 was a missing `asdcontrol` binary on fresh installs. In the v4.0.4 tree `asdcontrol` is listed in `install/omarchy-base.packages`, so it is present from the start.

We have no first-party evidence about the headphone jack, HDMI or DisplayPort audio, or Bluetooth on this model, so those stay marked unknown rather than assumed good. The same goes for suspend and hibernate. No desktop has a webcam, fingerprint reader, battery, touchpad or internal keyboard, so those are not applicable.

## What breaks

**Hard reset when the display blanks, dual external monitors, still open.** Issue #6223, opened 2026-07-14 by filip-spaldon on a 385, reproduces every time `dpms off` fires, whether from `omarchy-system-lock`, an idle timeout, or `hyprctl` directly. The journal just stops. It was bisected to the `linux` 7.1.x series and confirmed by grhoades and nickkaltner on 395 machines. The trigger condition matters: it only fires when both monitors were connected at boot. filip-spaldon then ran a clean A/B and found `amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is the only debug bit that survives; `0x10` and `0x2000` do not help. An AMD engineer, harkgill-amd, picked the thread up and produced an ISM flush patch on 2026-09-03 that stopped the reset across six runs. That patch was still heading for amd-staging-drm-next as of 2026-09-16, so treat it as unfixed on any shipping kernel.

**Hard freeze under Chromium, closed but not really solved.** Issue #5478 on Omarchy 3.6 collected 57 comments from Framework Desktop owners seeing `amdgpu: ring gfx_0.0.0 timeout` followed by a failed GPU reset. Multiple people found that raising the BIOS VRAM allocation from the 0.5 GB default to 16 GB or more stopped it. Others, including andyjeffries, stayed stable at 0.5 GB by disabling Chromium video decode acceleration instead. DHH's own read in the thread was that this is an AMD and kernel bug rather than something Omarchy can fix.

**DMUB firmware regressions arriving through `omarchy update`.** Issue #5984 black-screened a Strix Halo machine with a 5K DSC display after `linux-firmware-amdgpu` moved to 20260519. The reporter's note is worth keeping: downgrading the package is not enough, because early KMS bundles the firmware into the UKI, so you must run `sudo limine-mkinitcpio` afterward. Booting the previous Limine snapshot is the faster recovery. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

**6K over DisplayPort tops out at 30 Hz.** Issue #3815 and discussion #3846: an LG UltraFine 6K on a direct DisplayPort cable never activates DSC, leaving 6K at 30 Hz or 4K at 60 Hz. The same monitor and cable worked at 6K60 on a Beelink SER9. kvz later reported that a Thunderbolt 4 cable to the same monitor just worked, and DHH said his 6K Apple XDR runs fine over a DisplayPort to USB-C adapter. Do not try to escape this with a git kernel: issue #3816 is that experiment ending in a kernel BUG in `lib/string_helpers.c` before the GUI comes up.

**Shutdown restarts the machine with a Thunderbolt monitor.** Issue #3918 has been open since 2025-12-17. The reporter's workaround is to turn the monitor off, or unplug it, before shutting down.

**Screensaver dies instantly on three or more monitors.** Issue #8114, open, filed on 4.0.0 from a Framework Desktop with three displays. The screensaver self-terminates, the shell reads that as a dismissal, and the idle sequence never reaches the lock.

## What Omarchy does for this model

Nothing specific, and that is the important fact. Grep the v4.0.4 tree: `bin/omarchy-hw-match` matches on DMI `product_name` or `product_family`, and the only Framework caller is `bin/omarchy-hw-framework16`, which checks for `sys_vendor` Framework plus the string `Laptop 16` and installs `qmk-hid`. Nothing in `install/hardware/` matches the Desktop.

So the Framework Desktop gets the generic AMD path: the in-kernel `amdgpu` driver, plus `vulkan-radeon` added by `install/hardware/vulkan.sh` when `lspci` sees an AMD display device. No kernel parameters, no firmware pins, no VRAM tuning. Every mitigation on this page is something you apply yourself.

The Omarchy DMI strings to match against, taken from `fastfetch` output in the issue reports, are `sys_vendor` Framework and `product_name` `Desktop (AMD Ryzen AI Max 300 Series)`. Note that the product name does not contain the word Framework, which is why a naive `omarchy-hw-match Framework` would miss it.

Issue #3372 is worth knowing about for a different reason: a new owner found LM Studio reporting no GPU. Omarchy installs Mesa and Vulkan only, not ROCm, so compute stacks that expect ROCm need manual work.

## Variants

All Framework Desktop SKUs are Strix Halo, so they share the same amdgpu exposure. Reports in the tracker cover the Ryzen AI Max 385 with Radeon 8050S and the 395 and 395+ with Radeon 8060S, and both sides show the DPMS reset. Memory is soldered, so choose capacity at purchase.

The one variant choice that has mattered in practice is BIOS VRAM allocation, which is a setting rather than a SKU. 3.x reporters running the 0.5 GB default hit the Chromium lockups; several stopped after moving it to 16 GB or 32 GB. On a 64 or 128 GB machine that is cheap insurance.

Machines with the same silicon behave the same way. The Beelink GTR9 Pro and the Corsair AI Workstation 300 appear in these threads with matching symptoms, and issue #10852 on a Beelink GTR Pro with the same `1002:1586` GPU was resolved by an Aquamarine 0.15.0 update rather than anything vendor specific.

## Before you install

- Update the BIOS first. Reporters were on 03.02 through 03.05 during the 3.x crash wave.
- Raise the VRAM allocation in BIOS before your first boot if you drive more than one high-resolution display.
- Plan your monitor cabling. If you own a 5K or 6K panel, prefer Thunderbolt or USB-C over a direct DisplayPort run.
- Accept snapshots during install. Both the firmware regression and the kernel regression on this machine were recovered fastest by booting the previous Limine snapshot.
- If you run two or more monitors, add `amdgpu.dcdebugmask=0x800` before you trust the lock screen.
- Keep a second machine or an SSH route in for the first week. Several of these failures take the display down while the kernel is still alive.

Versions checked: the v4.0.4 source tree, release notes for 3.x through 4.0.4, and the issues linked above. The 3.x and 4.x difference here is smaller than usual. The Quattro shell rewrite changed the lock and idle path, but the failures on this box are below Hyprland, in amdgpu, and they carried across the 3.x to 4.x line unchanged.

## Related

- [AMD GPUs on Omarchy](/hardware/amd-gpu/)
- [Multi-monitor](/hardware/multi-monitor/)
- [Thunderbolt docks](/hardware/thunderbolt-dock/)
- [Chromium flicker and hardware acceleration](/fix/chromium-flicker-hardware-acceleration/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
