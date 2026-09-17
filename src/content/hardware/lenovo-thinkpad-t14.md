---
title: "Lenovo ThinkPad T14 and T14s (Gen 1 to Gen 6) on Omarchy"
description: "ThinkPad T14 and T14s on Omarchy 4.0.4: a silver buy with known AMD s2idle, lid-wake, Wi-Fi firmware and fwupd quirks to check first."
answer: "Silver. The T14 and T14s are among the safest laptops to put Omarchy on: no model-specific driver is missing, and the open reports are sleep and boot quirks rather than dead hardware. Expect to check three things: AMD s2idle on the T14s Gen 2, lid wake on the Gen 5, and an fwupd ESP workaround before firmware updates."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
kind: model
vendor: "Lenovo"
model: "ThinkPad T14 and T14s"
dmi: ["ThinkPad T14", "20UD003LUS", "20S1S64W1A", "21HES5TB2C", "21MDX000R2", "20XG", "20XF"]
year: "2020 to 2026"
cpu: "Intel Core i5/i7 (Gen 1 to Gen 4), Intel Core Ultra (Gen 5 to Gen 6), AMD Ryzen PRO 4000 to 8000 series"
gpu: "Integrated only: Intel UHD, Iris Xe, Arc (i915 or xe) or AMD Radeon (amdgpu, Renoir onward)"
rating: silver
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: works
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "bin/omarchy-hw-match"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    note: "The DMI matcher every model quirk uses. It greps /sys/class/dmi/id/product_name and product_family. No caller in the v4.0.4 tree passes a T14 or ThinkPad pattern."
  - name: "install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    note: "The only Lenovo file in install/hardware on v4.0.4. It matches \"Yoga Pro 7 14IAH10\" and never fires on a T14."
  - name: "install/hardware/intel/sof-firmware.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/sof-firmware.sh"
    note: "Installs sof-firmware whenever an Intel audio controller is present. Covers every Intel T14."
  - name: "install/hardware/intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Installs intel-media-driver, libvpl and vpl-gpu-rt for UHD, Iris and Xe graphics."
  - name: "install/hardware/intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Enables thermald on an Intel CPU of model 42 (Sandy Bridge) or newer when a battery is present."
  - name: "install/hardware/intel/lpmd.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/lpmd.sh"
    note: "Enables intel-lpmd on hybrid Intel CPU models 151, 154, 170, 172, 183, 186, 189, 191 and 204: Alder Lake, Raptor Lake, Meteor Lake, Lunar Lake and Panther Lake. Other CPU models are skipped."
  - name: "install/hardware/fix-synaptic-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-synaptic-touchpad.sh"
    note: "Loads psmouse with synaptics_intertouch=1 when a Synaptics device is listed. Made non-fatal after it broke Quattro installs in #6985."
  - name: "bin/omarchy-brightness-keyboard-mute"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-brightness-keyboard-mute"
    note: "Drives the platform::micmute LED that ThinkPads expose, so the mic-mute key lights correctly."
  - name: "bin/omarchy-update-firmware"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-update-firmware"
    note: "Installs fwupdx64.efi into /boot/EFI/arch, which is the directory whose absence broke firmware updates in #5939."
issueCount: 29
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [lenovo, thinkpad, t14, t14s, laptop, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10754"
    title: "Issue #10754: ThinkPad T14s Gen 2 AMD (20XG): sleep/wake failures improve with temporary PMC workaround; resolution unconfirmed"
    kind: issue
    author: "Theotius"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/5939"
    title: "Issue #5939: ThinkPad T14 Gen 5 firmware update fails when ESP lacks EFI/arch directory"
    kind: issue
    author: "sgirard"
    date: "2026-05-22"
  - url: "https://github.com/omacom/omarchy/issues/3511"
    title: "Issue #3511: bug: Screen does not wake up after some interval of either lid closed and reopened or leave to sit for a while"
    kind: issue
    author: "aashish-thapa"
    date: "2025-11-22"
  - url: "https://github.com/omacom/omarchy/issues/8580"
    title: "Issue #8580: Lock: monitor that drops HPD after DPMS-off comes back lit and never re-blanks (blank timer is one-shot)"
    kind: issue
    author: "bmcswee"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/8618"
    title: "Issue #8618: LUKS password rejected multiple times on boot (ThinkPad T14s Gen 1), works after several attempts"
    kind: issue
    author: "AllergicCypress"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/2286"
    title: "Issue #2286: Wifi adapter not detecting"
    kind: issue
    author: "Sabadon"
    date: "2025-10-07"
  - url: "https://github.com/omacom/omarchy/issues/1132"
    title: "Issue #1132: Omarchy 2.0 linux-firmware missing critical firmware, breaks iwd and more"
    kind: issue
    author: "zaneschepke"
    date: "2025-08-26"
  - url: "https://github.com/omacom/omarchy/issues/9392"
    title: "Issue #9392: CapsLock broken"
    kind: issue
    author: "zaneschepke"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/6883"
    title: "Issue #6883: Quattro upgrade leaves broken app-menu icons and a ghost Alacritty launcher"
    kind: issue
    author: "cempack"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/5527"
    title: "Issue #5527: It seems gpu is being forcelly throttled causing the UI to be slow like as if I am using over a VNC"
    kind: issue
    author: "phoscoder"
    date: "2026-05-01"
  - url: "https://github.com/omacom/omarchy/issues/3443"
    title: "Issue #3443: Omarchy not shutting down properly"
    kind: issue
    author: "matyssxdxd"
    date: "2025-11-17"
  - url: "https://github.com/omacom/omarchy/issues/8099"
    title: "Issue #8099: Keyboard backlight stays off after unlock (idle-blank restore doesn't fire reliably)"
    kind: issue
    author: "Alkiviadroot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh"
    title: "install/hardware/all.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/hypr/input.lua"
    title: "default/hypr/input.lua at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-update-firmware"
    title: "bin/omarchy-update-firmware at v4.0.4"
    kind: commit
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
credits:
  - name: "Theotius"
    url: "https://github.com/Theotius"
    for: "Traced T14s Gen 2 AMD sleep failures to a missing 20XG entry in the kernel AMD PMC quirk table and reported the result honestly as unconfirmed"
  - name: "sgirard"
    url: "https://github.com/sgirard"
    for: "Found that creating an empty /boot/EFI/arch lets fwupd flash Lenovo system firmware on a UKI install, and linked a possible upstream fwupd fix"
  - name: "Sabadon"
    url: "https://github.com/Sabadon"
    for: "Pinned a dead MT7922 adapter on a T14s Gen 3 to one bad linux-firmware-mediatek build and confirmed the later package fixed it"
  - name: "aashish-thapa"
    url: "https://github.com/aashish-thapa"
    for: "Reported the T14 Gen 5 lid-wake failure with the full /proc/acpi/wakeup state"
faq:
  - q: "Which T14 generation is the safest buy for Omarchy?"
    a: "Any of Gen 1 through Gen 4, Intel or AMD. They use ordinary Intel or AMD integrated graphics and Intel, Qualcomm or MediaTek Wi-Fi, and the reports against them are Omarchy behaviour bugs or packaging slips rather than missing drivers. Gen 5 and Gen 6 are newer silicon with fewer confirmed reports either way."
  - q: "Does Omarchy ship anything specific to the ThinkPad T14?"
    a: "No. On v4.0.4 the only Lenovo file in install/hardware matches a Yoga Pro 7, and no script passes a ThinkPad pattern to omarchy-hw-match. The T14 gets generic Intel or AMD enablement plus the platform::micmute LED support that ThinkPads expose."
  - q: "Why did Caps Lock stop working after I updated to Quattro?"
    a: "It moved. Omarchy 4.0.0 set kb_options to compose:caps,shift:both_capslock_cancel, so Caps Lock is the compose key and Caps Lock itself is toggled by pressing both Shift keys. That is by design. Override kb_options in ~/.config/hypr/input.lua if you want the old behaviour."
  - q: "Is suspend reliable on the AMD models?"
    a: "Not on every one. The T14s Gen 2 AMD (machine type 20XG) is missing from the kernel AMD PMC quirk table that already covers its 20XF sibling, and one owner saw repeated s2idle wake failures until they added it locally. Test suspend before you trust the machine with unsaved work."
related: [lenovo-thinkpad-x1-carbon, suspend-sleep, wifi, boot-limine, battery-power, multi-monitor]
draft: false
---

## Verdict

Silver. The ThinkPad T14 and T14s are close to the default recommendation for Omarchy: everything on board is mainstream silicon with in-tree drivers, and across the 29 issues and 4 discussions that name a T14 or T14s in the Omarchy tracker there is not one report of a subsystem with no driver at all. That is the difference between this machine and a brand new Panther Lake laptop.

It is not gold, for three reasons. Suspend is unresolved on at least one AMD variant. The Gen 5 lid-wake report from 2025 is still open. And Omarchy ships zero T14-specific enablement, so anything Lenovo does oddly is between you and the kernel.

Checked on 4.0.4 (2026-09-15) with the v4.0.4 source tree. Most of the evidence below predates Quattro and was filed against 3.x, which matters: the 4.0.0 rewrite replaced the whole shell and moved Hyprland config to Lua, so pre-Quattro reports about the bar, the lock screen or keybindings no longer describe what you will see.

## What works

Graphics are the best-evidenced subsystem. AMD Renoir and newer run on amdgpu, Intel from Comet Lake to Arc run on i915 or xe, and none of the T14 issues that mention graphics is about a black screen; they are about session behaviour. Issue [#8580](https://github.com/omacom/omarchy/issues/8580) shows a T14 Gen 1 (20UD003LUS, Ryzen 5 PRO 4650U) driving its internal panel plus two external 1440p monitors on a dock, which is a decent proof of the amdgpu path.

No T14 report describes a dead keyboard or TrackPoint. The one ThinkPad-flavoured touch Omarchy has is `omarchy-brightness-keyboard-mute`, which drives the `platform::micmute` LED node ThinkPads expose so the mic-mute indicator can track the mute state.

Wi-Fi has no hardware gap on record. The two Wi-Fi failures were both firmware packaging regressions, and the reporters confirmed the later packages worked, although one commenter on a fresh install still had no adapter and never followed up. See below.

Everything else is marked unknown in the table above on purpose. Nobody has filed a T14 audio, webcam, fingerprint, hibernate or touchpad failure against Omarchy, which is weak positive evidence at best. An issue tracker only proves what breaks.

## What breaks

**AMD s2idle on the T14s Gen 2.** Issue [#10754](https://github.com/omacom/omarchy/issues/10754) (open, filed 2026-09-08 against 4.0.2) reports repeated sleep and wake attempts leaving the session unusable, with file operations failing until reboot. The reporter found that the kernel's AMD PMC quirk table carries a firmware sleep workaround for machine type 20XF but not for the sibling 20XG, rebuilt the module with a 20XG entry, and saw three clean suspend cycles afterwards. They were careful to call it promising rather than fixed, and so should you. This is a kernel and firmware interaction, not an Omarchy defect.

**Lid wake on the Gen 5.** Issue [#3511](https://github.com/omacom/omarchy/issues/3511) is still open from 2025-11-22: the display does not come back after the lid is closed and reopened, and setting `HandleLidSwitch=ignore` in logind did not help. A later commenter described the same symptom in clamshell mode on a dock. No fix is recorded. See [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/).

**Firmware updates fail on a UKI install.** On a T14 Gen 5 (21MDX000R2) with Limine and a UKI at `/boot/EFI/Linux/`, fwupd refused a Lenovo system firmware update with `cannot find either EFI/systemd or EFI/arch in ESP`. Creating an empty `/boot/EFI/arch` was enough to let it flash ([#5939](https://github.com/omacom/omarchy/issues/5939), open, confirmed by one other owner). Omarchy's own `omarchy-update-firmware` installs `fwupdx64.efi` into `/boot/EFI/arch`, which creates the directory as a side effect, so running firmware updates through the Omarchy command rather than bare `fwupdmgr` avoids this. The reporter also linked a possible upstream fwupd fix.

**Wi-Fi, twice, both packaging.** On a T14s Gen 3 with a MediaTek MT7922, the adapter vanished entirely and Impala reported no adapter found ([#2286](https://github.com/omacom/omarchy/issues/2286), closed). The reporter isolated it to `linux-firmware-mediatek` 20250917-1 and confirmed 20251011-1 works; a later commenter on a fresh install with the same package still saw no adapter and did not reply to follow-up. Separately, the Omarchy 2.0 update left a T14 Gen 5 AMD with missing amdgpu, ath11k and Bluetooth firmware ([#1132](https://github.com/omacom/omarchy/issues/1132), closed), which dhh attributed to a general kernel 6.16 era firmware problem fixed by reinstalling `linux-firmware`. Neither is current. See [/hardware/wifi/](/hardware/wifi/) and [/fix/wifi-drops-after-kernel-update-iwlwifi/](/fix/wifi-drops-after-kernel-update-iwlwifi/).

**Caps Lock is not broken, it moved.** Issue [#9392](https://github.com/omacom/omarchy/issues/9392) from a T14 Gen 5 AMD owner on 4.0.2 was closed within five minutes. Quattro sets `kb_options = "compose:caps,shift:both_capslock_cancel"` in `default/hypr/input.lua`, making Caps Lock the compose key, with Caps Lock itself toggled by both Shift keys. See [/fix/custom-keybindings-lost-after-quattro/](/fix/custom-keybindings-lost-after-quattro/).

**Two open annoyances that look like shell bugs.** On a T14 Gen 1 (20S1S64W1A, i5-10310U) the keyboard backlight stayed at zero after unlock even though the shell had reported the session unlocked; the reporter polled `tpacpi::kbd_backlight` to prove it and blames the lock plugin's wake path ([#8099](https://github.com/omacom/omarchy/issues/8099), open). And on the three-monitor Gen 1 above, a cheap external panel that drops hotplug-detect after being blanked gets re-added powered on, and the lock screen's single blank timer never runs again ([#8580](https://github.com/omacom/omarchy/issues/8580), open, reproduced by another user on a desktop amdgpu box).

**Thin or stale reports.** A T14s Gen 1 owner had LUKS passphrases rejected several times per boot after a Quickshell crash ([#8618](https://github.com/omacom/omarchy/issues/8618), open); the thread's later comments point at failing RAM and unclean shutdowns on entirely different machines, so treat it as unexplained rather than as a T14 defect. See [/fix/luks-passphrase-not-accepted-at-boot/](/fix/luks-passphrase-not-accepted-at-boot/). A T14 Gen 4 (21HES5TB2C, i7-1365U) reported bursty UI lag on 3.6.0 ([#5527](https://github.com/omacom/omarchy/issues/5527)) and it was closed the next day with no comments and no recorded cause. A T14s Gen 4 AMD shutdown hang ([#3443](https://github.com/omacom/omarchy/issues/3443)) was closed in February 2026 when dhh said a fix had shipped in 3.4; the reporter had already stopped seeing it.

## What Omarchy does for this model

Nothing by name. `bin/omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `product_family`, and no caller in the v4.0.4 tree passes a ThinkPad or T14 pattern. The only file under `install/hardware/lenovo/` is a Yoga Pro 7 14IAH10 speaker pin quirk that will never match your machine.

What you actually get is the generic path in `install/hardware/all.sh`. On an Intel T14 that is `sof-firmware` for the audio DSP, `intel-media-driver` plus `libvpl` and `vpl-gpu-rt` for video acceleration, `thermald` on anything newer than Sandy Bridge with a battery, and `intel-lpmd` on Alder Lake and later CPU models. On both Intel and AMD you also get the Synaptics InterTouch attempt, Bluetooth service enablement, and a wireless regulatory domain derived from your timezone. The Panther Lake specific scripts (`fred.sh`, the WiFi 7 EHT disable, the IPU7 camera package) key off a Panther Lake GPU in `lspci`, a BE200 or BE211 Wi-Fi card, or an `OVTI08F4` ACPI device, none of which appears in any Omarchy T14 report.

## Variants

Gen 1 through Gen 4, Intel or AMD, are the safest buy. That is where the Omarchy reports are ordinary and where the hardware has had years of kernel attention.

If you get to choose the Wi-Fi card, know that the MediaTek MT7922 in some AMD T14s configurations is the part behind the only "no adapter at all" report on this model. That specific firmware build is fixed, but it is the card with the least margin.

The T14s Gen 2 AMD (machine type 20XG) is the one variant to approach with the sleep test in hand.

Gen 5 and Gen 6 are thinner evidence rather than bad evidence. Only two Gen 6 reports exist. One is the T14s Gen 6 (Core Ultra 5 228V, Arc 140V) upgrade cosmetic bug in [#6883](https://github.com/omacom/omarchy/issues/6883), which says the machine runs Quattro and nothing about its hardware. The other, [#5989](https://github.com/omacom/omarchy/issues/5989), is a T14 Gen 6 with a Core Ultra 7 255H running Ubuntu rather than Omarchy, so it says nothing useful here.

The P14s and T14p are close relatives and are not covered here.

## Before you install

- Check `cat /sys/class/dmi/id/product_name` and note the machine type, for example 20XG or 21MD. That string, not the marketing name, is what kernel quirk tables match on.
- Update the BIOS from Windows or a Lenovo USB stick before you wipe the drive. It is the least painful time to do it.
- After install, run firmware updates through `omarchy update firmware`, not bare `fwupdmgr`, so `/boot/EFI/arch` exists.
- Test suspend and lid close twice, before you trust the machine, and check [/hardware/suspend-sleep/](/hardware/suspend-sleep/) if it misbehaves. The [System sleep chapter](https://omarchy.org/manual/system-sleep/) covers turning suspend and hibernate off if your machine cannot do them.
- If you are coming from Omarchy 3, read [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/) first. A T14s Gen 6 owner lost custom app-menu icons to the Quattro upgrade ([#6883](https://github.com/omacom/omarchy/issues/6883), open) because the migration moves the legacy icon directory out from under surviving desktop entries.
- Expect Caps Lock to be the compose key, and both Shifts to toggle Caps Lock, before you file a bug about it.

## Related

[/hardware/lenovo-thinkpad-x1-carbon/](/hardware/lenovo-thinkpad-x1-carbon/), [/hardware/suspend-sleep/](/hardware/suspend-sleep/), [/hardware/wifi/](/hardware/wifi/), [/hardware/boot-limine/](/hardware/boot-limine/), [/hardware/battery-power/](/hardware/battery-power/), [/hardware/multi-monitor/](/hardware/multi-monitor/), [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/), [/fix/luks-passphrase-not-accepted-at-boot/](/fix/luks-passphrase-not-accepted-at-boot/), [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/), [/releases/v4.0.4/](/releases/v4.0.4/), [/hardware/submit/](/hardware/submit/). Manual chapter: [System sleep](https://omarchy.org/manual/system-sleep/).
