---
title: "Framework Desktop (Strix Halo) on Omarchy"
description: "Framework Desktop (Ryzen AI Max 385/395) on Omarchy 4.0.4: the Strix Halo amdgpu lockups, the dual-monitor DPMS reset, 6K DSC limits, and what to check first."
answer: "Buy it with your eyes open. The Framework Desktop runs Omarchy 4.0.4 with no model-specific setup, and Omarchy ships no quirk script for it. The recurring problems are all amdgpu on Strix Halo: hard freezes under Chromium video, a hard reset when the screen blanks with two monitors connected at boot, and DisplayPort DSC limits. With one display the tracker is quiet. With two or three, expect work."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-17
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
  suspend: partial
  hibernate: unknown
  touchpad: n/a
  display: partial
  battery: n/a
  keyboard: n/a
quirkScripts: []
issueCount: 30
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
  - url: "https://github.com/omacom/omarchy/commit/ad2ae30f1ee8b75a4c794f278693a08d5eff929d"
    title: "Commit ad2ae30f: Remove VAAPI GL video feature flags from Chromium-based browser configs to prevent crashing on some machines"
    kind: commit
    author: "dhh"
    date: "2026-05-08"
  - url: "https://github.com/omacom/omarchy/pull/5664"
    title: "PR #5664: Warn on low amdgpu vram assignment to workaround hard freezes (closed, not merged)"
    kind: pr
    author: "dhh"
    date: "2026-05-08"
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
  - url: "https://github.com/omacom/omarchy/pull/8142"
    title: "PR #8142: Keep the screensaver up while launch hops between monitors (open)"
    kind: pr
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/5277"
    title: "Issue #5277: System hard-freeze on suspend with hyprlock active, no resume, requires hard reboot"
    kind: issue
    author: "heathdog"
    date: "2026-04-11"
  - url: "https://github.com/omacom/omarchy/issues/7280"
    title: "Issue #7280: omarchy-sleep-lock.service fails on resume: Restart=always re-runs systemd-inhibit while logind's sleep operation is still in flight"
    kind: issue
    author: "ki11e6"
    date: "2026-08-17"
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
    for: "Bisected the DPMS hard reset to the kernel, found the dual-monitor-at-boot trigger, and showed that amdgpu.dcdebugmask=0x800 prevents it"
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
    for: "Documented the 6K DSC limit over DisplayPort and that a Thunderbolt 4 cable works instead"
faq:
  - q: "Which Framework Desktop CPU should I pick for Omarchy?"
    a: "Both the Ryzen AI Max 385 and the 395/395+ are reported running Omarchy. The open DPMS hard reset in issue #6223 was reported on a 385 and reproduced on a 395+ with three displays, but another 395 owner, an AMD engineer on a Corsair box with the same chip, and DHH on his own 385 could not reproduce it, and the reporter's best guess is that the monitor mix matters more than the chip. Pick on RAM and budget."
  - q: "Does Omarchy install anything special for the Framework Desktop?"
    a: "No. In the v4.0.4 tree the only Framework-specific script is omarchy-hw-framework16, which matches the DMI string Laptop 16. Nothing matches the Desktop, so it gets the generic AMD path: the amdgpu kernel driver plus vulkan-radeon from install/hardware/vulkan.sh."
  - q: "My machine hard resets when the screen blanks. What do I do now?"
    a: "Add amdgpu.dcdebugmask=0x800 to the kernel command line. filip-spaldon ran a clean A/B in issue #6223 and that bit, DC_DISABLE_IPS, was the only one that survived. The proper fix is an AMD ISM flush patch that had not reached stock Arch 7.2.3 as of the last thread update on 2026-09-09."
related: [amd-gpu, multi-monitor, thunderbolt-dock, framework-laptop-13]
draft: false
---

The Framework Desktop is a 4.5 litre box built around AMD Strix Halo: a Ryzen AI Max 385, 395 or 395+ with Radeon 8050S or 8060S graphics and up to 128 GB of soldered unified memory. It is one of the machines the Omarchy community talks about most, and DHH runs one; he has posted from both a 385 and a 395 in the tracker. It also generates a steady stream of amdgpu bug reports.

## Verdict

Bronze. The machine installs and runs Omarchy with zero model-specific setup, and everything outside graphics is quiet. But the GPU is the whole computer here, and Strix Halo has produced three separate ways to lose the display on Omarchy in under a year: a Chromium-triggered GPU ring timeout, a firmware regression that black-screens 5K DSC panels, and a hard reset on DPMS off that is still open on 4.x.

The honest split is by display count. With one monitor connected at boot, the DPMS reset does not fire in filip-spaldon's A/B testing, and the Chromium lockups have workarounds, so a single-display box would rate silver. With two or three monitors, which is the obvious use for a box with this much RAM, you may meet issue #6223 and need a kernel parameter to get through a normal lock cycle. Not every dual-monitor owner hits it, but the ones who do hit it on every lock. That is a real problem on a default workflow, so bronze is the fair call.

## What works

Installation is unremarkable. There is no dGPU to fight, no hybrid switching, no Secure Boot dance beyond the usual.

Wi-Fi associates and routes normally. The one Framework Desktop network report we could find, issue #5647 on 3.7.0, showed the interface up with an address and the LAN reachable; the missing internet turned out to be a Mullvad service re-enabling itself on boot, and the reporter closed it as their own configuration.

A monitor on the USB-C ports shows the login screen. raphaelstary notes in issue #3918 that before 3.2.3 the Plymouth unlock prompt was invisible over a Thunderbolt monitor and had to be typed blind; the 3.2.3 release added the `thunderbolt` module to the initramfs and fixed that.

Brightness control on an Apple Studio Display works. Issue #2278 in October 2025 was not a missing binary: `asdcontrol` itself ran fine, but the sudoless helper looked for it at `/usr/local/bin/asdcontrol`, which does not exist on a fresh install. DHH had already corrected the path on dev in commit 3cb52c0b two days earlier, and 3.8.0 later added XDR support. In the v4.0.4 tree `asdcontrol` is in `install/omarchy-base.packages` and `bin/omarchy-brightness-display-apple` calls it through `sudo` directly.

We have no first-party evidence about the headphone jack, HDMI or DisplayPort audio, or Bluetooth on this model, so those stay marked unknown rather than assumed good. The same goes for hibernate. No desktop has a webcam, fingerprint reader, battery, touchpad or internal keyboard, so those are not applicable.

Suspend is marked partial rather than unknown because the only two reports are negative. In issue #5277, censey says a Framework Desktop hard-freezes on suspend with hyprlock active "on a regular basis" since the 3.6 upgrade, with no follow-up. In issue #7280, a Framework Desktop owner on 4.0.0 reproduced the `omarchy-sleep-lock.service` restart loop on resume, which is a service bug rather than a hardware one. Neither is confirmed by a second Framework Desktop, so treat it as a caution, not a verdict.

## What breaks

**Hard reset when the display blanks, two monitors at boot, still open.** Issue #6223, opened 2026-07-14 by filip-spaldon on a 385 running 3.8.3, reproduces every time `dpms off` fires, whether from `omarchy-system-lock`, an idle timeout, or `hyprctl` directly. The journal ends with no error at all. It was bisected to `linux` 7.1.3 (7.0.10 is fine) and persists on 7.1.8 under Quattro 4.0.0, on 7.1.9, and on stock 7.2.3. The trigger condition matters: it only fires when both monitors were connected at boot, and hotplugging the second one after login takes a different path that does not crash. grhoades reproduced it on a 395+ with three displays and nickkaltner on another 8050S box with two. DHH could not reproduce it on his own 385, SmartALB could not on a 395 with two monitors, and harkgill-amd could not on a Corsair AI Workstation 300 with the same silicon, so the display mix seems to matter; filip-spaldon's guess is his 170 Hz panel next to a 60 Hz one. He then ran a clean A/B and found `amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is the only debug bit that survives; `0x10` and `0x2000` do not help. His other workaround is to disable one output before blanking. harkgill-amd, an AMD engineer, picked the thread up and produced an ISM flush patch on 2026-09-03 that stopped the reset across six runs, and said it would go to amd-staging-drm-next and then upstream with no timeline. On 2026-09-09 filip-spaldon confirmed stock Arch 7.2.3 still lacks it. Treat it as unfixed on any shipping kernel; we did not check whether the `linux-omarchy` kernel in 4.0.4 carries it. The same thread also collected a delayed variant on a Strix Point Beelink SER and a DPMS-off crash on an Intel Latitude, which may or may not be the same bug.

**Hard freeze under Chromium, closed with a partial fix.** Issue #5478 on Omarchy 3.6 collected 57 comments, mostly from Framework Desktop owners, showing `amdgpu: ring gfx_0.0.0 timeout` followed by a failed GPU reset, usually while a video was playing or paused. DHH closed it on 2026-05-08 with commit ad2ae30f, which removed the VAAPI GL video flags from the default Chromium config and shipped as a migration the day before 3.8.0. That helped some owners immediately and not others. censey, jwilliams55 and DHH himself stopped crashing after raising the BIOS VRAM allocation from the 0.5 GB default to 16 GB. DannyManzietti had crashed with 32 GB set, and once with 64 GB, then settled with the flags removed plus 32 GB. andyjeffries stayed stable at 0.5 GB for 15 days by also disabling accelerated video decode in his browser flags. `amdgpu.gfxoff=0`, `amdgpu.ppfeaturemask`, and a BIOS update from 03.03 to 03.05 did not help. DHH's read in the thread was that this is an AMD and kernel bug rather than something Omarchy can fix, and his PR #5664 to warn on a low VRAM setting was closed without merging.

**DMUB firmware regressions arriving through `omarchy update`.** Issue #5984 black-screened a Strix Halo machine with a 5K DSC Apple Studio Display after `linux-firmware-amdgpu` moved to 20260519. The reporter's note is worth keeping: downgrading the package is not enough, because early KMS bundles the firmware into the UKI, so you must run `sudo limine-mkinitcpio` afterward. Booting the previous Limine snapshot is the faster recovery. The issue was closed in August with no fix recorded. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

**6K over DisplayPort tops out at 30 Hz.** Issue #3815 and discussion #3846: an LG UltraFine 6K on a direct DisplayPort cable never activates DSC, leaving 6K at 30 Hz or 4K at 60 Hz. The same monitor and cable worked at 6K60 on a Beelink SER9. whargrove got 6K60 over USB4, kvz later reported that a Thunderbolt 4 cable to the same monitor just worked, and DHH said his 6K Apple XDR runs fine over a DisplayPort plus USB-A to USB-C cable. Do not try to escape this with a git kernel: issue #3816 is that experiment ending in a kernel BUG in `lib/string_helpers.c` before the GUI comes up.

**Shutdown restarts the machine with a Thunderbolt monitor.** Issue #3918 has been open since 2025-12-17. The reporter's workaround is to turn the monitor off, or unplug it, before shutting down.

**Screensaver dies instantly on three or more monitors.** Issue #8114, open, filed on 4.0.0 from a Framework Desktop with three displays. The screensaver self-terminates, the shell reads that as a dismissal, and the idle sequence never reaches the lock. PR #8142 addresses the focus check and was still open, unmerged, on 2026-09-17.

## What Omarchy does for this model

Nothing specific, and that is the important fact. Grep the v4.0.4 tree: `bin/omarchy-hw-match` matches on DMI `product_name` or `product_family`, and the only Framework caller is `bin/omarchy-hw-framework16`, which checks for `sys_vendor` Framework plus the string `Laptop 16` and installs `qmk-hid`. Nothing in `install/hardware/` matches the Desktop.

So the Framework Desktop gets the generic AMD path: the in-kernel `amdgpu` driver, plus `vulkan-radeon` added by `install/hardware/vulkan.sh` when `lspci` sees an AMD display device. No kernel parameters, no firmware pins, no VRAM tuning. Every mitigation on this page is something you apply yourself.

The DMI strings to match against come from the kernel's `Hardware name:` line in the issue #5478 oops: `sys_vendor` Framework, `product_name` `Desktop (AMD Ryzen AI Max 300 Series)`, board `FRANMFCP04` (filip-spaldon's is `FRANMFCP02`). Note that the product name does not contain the word Framework, which is why a naive `omarchy-hw-match Framework` would miss it.

Issue #3372 is worth knowing about for a different reason: a new owner found LM Studio reporting no GPU. It was closed with no fix recorded. Omarchy installs Mesa and Vulkan only; nothing in the v4.0.4 `install/` tree pulls in ROCm, so compute stacks that expect ROCm need manual work.

## Variants

All Framework Desktop SKUs are Strix Halo, so they share the same amdgpu exposure. Reports in the tracker cover the Ryzen AI Max 385 with Radeon 8050S and the 395 and 395+ with Radeon 8060S. Both sides show the Chromium lockups, and the DPMS reset has been reproduced on both a 385 and a 395+. Memory is soldered, so choose capacity at purchase.

The one variant choice that has mattered in practice is BIOS VRAM allocation, which is a setting rather than a SKU. 3.x reporters running the 0.5 GB default hit the Chromium lockups, and most stopped after moving it to 16 GB or 32 GB. One reporter still crashed at 32 GB and once at 64 GB, so it is a strong mitigation rather than a guarantee. On a 64 or 128 GB machine it costs you little, unless you want that memory for local LLMs.

Machines with the same silicon are not automatically the same experience. harkgill-amd's Corsair AI Workstation 300, same Radeon 8060S, could not reproduce the DPMS reset. Issue #10852, on a Beelink GTR Pro with the same `1002:1586` GPU, was a different display freeze that stopped recurring after Aquamarine 0.15.0; the reporter closed it after six clean days and said it was not a bisect.

## Before you install

- Update the BIOS. Reporters were on 03.02 through 03.06, and going from 03.03 to 03.05 did not stop the Chromium crash for one of them, so do it for the usual reasons and not as a fix.
- Raise the VRAM allocation in BIOS before your first boot if you drive more than one high-resolution display.
- Plan your monitor cabling. If you own a 5K or 6K panel, prefer Thunderbolt or USB-C over a direct DisplayPort run.
- Accept snapshots during install. Both the firmware regression and the kernel regression on this machine were recovered fastest by booting the previous Limine snapshot.
- If you run two or more monitors, add `amdgpu.dcdebugmask=0x800` before you trust the lock screen, or disable one output before you blank.
- Keep a second machine or an SSH route in for the first week. Several of these failures take the display down while the kernel is still alive.

Versions checked: the v4.0.4 source tree, release notes for 3.x through 4.0.4, and the issues linked above. The 3.x and 4.x difference here is smaller than usual. The Quattro shell rewrite changed the lock and idle path, but the failures on this box are below Hyprland, in amdgpu, and they carried across the 3.x to 4.x line unchanged.

## Related

- [AMD GPUs on Omarchy](/hardware/amd-gpu/)
- [Multi-monitor](/hardware/multi-monitor/)
- [Thunderbolt docks](/hardware/thunderbolt-dock/)
- [Chromium flicker and hardware acceleration](/fix/chromium-flicker-hardware-acceleration/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
