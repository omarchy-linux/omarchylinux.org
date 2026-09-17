---
title: "Lenovo ThinkPad T480 and T480s on Omarchy"
description: "ThinkPad T480 and T480s on Omarchy 4.0.4: Intel UHD 620 works, the dual-battery readout is wrong, and the Validity fingerprint reader never enrolls."
answer: "Silver. A T480 or T480s runs Omarchy 4.0.4 well: i915 graphics, Intel 8265 Wi-Fi and HDA audio come up with no extra work, and TPM must be off in the BIOS. Two things bite. The bar and power panel report only BAT0, so the second pack is invisible, and the Synaptics Validity 06cb:009a fingerprint reader has no libfprint driver, so Setup > Security > Fingerprint always fails."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
kind: model
vendor: "Lenovo"
model: "ThinkPad T480 / T480s"
dmi: ["20L6S77E00", "20L8S27E04", "20L7S2QV00", "20MF000DUS", "ThinkPad T480s"]
year: "2018"
cpu: "Intel Core i5-8250U / i5-8350U / i7-8550U / i7-8650U (Kaby Lake-R)"
gpu: "Intel UHD Graphics 620 (8086:5917, i915); optional NVIDIA MX150 on the T480"
rating: silver
subsystems:
  wifi: works
  bluetooth: works
  audio: works
  webcam: unknown
  fingerprint: broken
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: partial
  keyboard: unknown
quirkScripts:
  - name: "bin/omarchy-hw-match"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    note: "The DMI matcher every model quirk uses. It greps product_name and product_family. No caller in the v4.0.4 tree passes a ThinkPad or T480 pattern, so no T480-specific quirk exists."
  - name: "install/hardware/intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Installs and enables thermald on any Intel laptop CPU with model number 42 or higher. Kaby Lake-R qualifies, so this fires on every T480."
  - name: "install/hardware/intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Matches the UHD Graphics string and installs intel-media-driver, libvpl and vpl-gpu-rt."
  - name: "install/hardware/intel/lpmd.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/lpmd.sh"
    note: "Skipped here. It only runs on CPU models 151, 154, 170, 172, 183, 186, 189, 191 and 204, which is Alder Lake and newer."
  - name: "install/hardware/fix-synaptic-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-synaptic-touchpad.sh"
    note: "Loads psmouse with synaptics_intertouch=1 when the input device list names Synaptics. Generic, not T480-specific, and a no-op during an arch-chroot install."
  - name: "migrations/1789325478.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1789325478.sh"
    note: "The 4.0.4 migration that installs linux-omarchy and puts it first in the Limine boot order. It leaves the old kernel installed on purpose."
issueCount: 29
lastVerified: 2026-09-17
omarchyVersionTested: "4.0.4"
tags: [lenovo, thinkpad, t480, t480s, intel, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11721"
    title: "Issue #11721: Stock fingerprint setup fails with NoSuchDevice on Validity 06cb:009a (libfprint lists it as unsupported)"
    kind: issue
    author: "BeameX"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/7006"
    title: "Issue #7006: setup security fingerprint fails on sensors requiring open-fprintd (ThinkPad 06cb:009a)"
    kind: issue
    author: "ItsNotPaths"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/2046"
    title: "Issue #2046: Cannot Enroll Fingerprint - NoSuchDevice Error"
    kind: issue
    author: "landsman"
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/issues/6885"
    title: "Issue #6885: Battery percent in the top bar shows only BAT0"
    kind: issue
    author: "vcelletti"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/7214"
    title: "Issue #7214: omarchy-battery-status reads only the first battery on dual-battery laptops"
    kind: issue
    author: "syntaxboybe"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/10244"
    title: "Issue #10244: omarchy-battery-status reports wrong percentage on dual-battery laptops (reads only BAT0)"
    kind: issue
    author: "nick-terrant"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/12238"
    title: "Issue #12238: i915 CPU pipe A FIFO underrun (KBL 0x5917) since linux-omarchy 7.2.5-3"
    kind: issue
    author: "pony-montana"
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/8447"
    title: "Issue #8447: ThinkPad T480s: stale/frozen lock screen for ~30 s after S3 resume"
    kind: issue
    author: "hugo88"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/10266"
    title: "Issue #10266: External monitor reconnect can ignore configured mode in clamshell dock setup"
    kind: issue
    author: "mkeiji"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/4296"
    title: "Issue #4296: TPM boot failure on fresh installation (omarchy 3.3.2 iso)"
    kind: issue
    author: "felixzsh"
    date: "2026-01-17"
  - url: "https://github.com/omacom/omarchy/issues/5330"
    title: "Issue #5330: Machine unbootable. No Limine config. No kernel entry. Nothing"
    kind: issue
    author: "endafk"
    date: "2026-04-16"
  - url: "https://github.com/omacom/omarchy/issues/4208"
    title: "Issue #4208: Boot fails on first boot with Libreboot/Coreboot (no EFI payload)"
    kind: issue
    author: "Somnius"
    date: "2026-01-10"
  - url: "https://github.com/omacom/omarchy/issues/4120"
    title: "Issue #4120: Thinkpad stalling after entering Omarchy credentials and rebooting"
    kind: issue
    author: "kaledin"
    date: "2026-01-07"
  - url: "https://github.com/omacom/omarchy/issues/5780"
    title: "Issue #5780: Desktop notification showing incorrect battery percentage on dual battery systems"
    kind: issue
    author: "Michael-Steshenko"
    date: "2026-05-12"
  - url: "https://github.com/omacom/omarchy/pull/10384"
    title: "PR #10384: Read battery aggregate from UPower DisplayDevice"
    kind: pr
    author: "fresh3nough"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-battery-status"
    title: "bin/omarchy-battery-status at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh"
    title: "install/hardware/all.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    title: "bin/omarchy-hw-match at v4.0.4"
    kind: commit
credits:
  - name: "BeameX"
    url: "https://github.com/BeameX"
    for: "Showed that libfprint's own hwdb lists 06cb:009a under known unsupported devices, so the stock wizard can never enroll it"
  - name: "ItsNotPaths"
    url: "https://github.com/ItsNotPaths"
    for: "Traced the package conflict that makes the fingerprint wizard abort on a working open-fprintd stack"
  - name: "syntaxboybe"
    url: "https://github.com/syntaxboybe"
    for: "Reported the single-battery assumption in omarchy-battery-status"
  - name: "vcelletti"
    url: "https://github.com/vcelletti"
    for: "Reported that the bar icon and the power panel disagree about the battery on a T480"
  - name: "pony-montana"
    url: "https://github.com/pony-montana"
    for: "First report of i915 FIFO underruns on Kaby Lake-R after the 4.0.4 kernel switch"
faq:
  - q: "Does the fingerprint reader work on a T480?"
    a: "Not with stock Omarchy. Most T480 and T480s units ship the Synaptics Validity 06cb:009a reader, which libfprint lists as unsupported, so Setup > Security > Fingerprint ends in NoSuchDevice. The community python-validity and open-fprintd stack works but conflicts with the packages Omarchy installs."
  - q: "Why does my battery percentage jump around?"
    a: "The top bar icon reads UPower's combined device while the power panel runs omarchy-battery-status, which still picks the first BAT device. On a T480 with the rear hot-swap pack those two numbers disagree. Fixes are open in PR #10384 and PR #8864, neither merged as of 4.0.4."
  - q: "Should I buy a T480 to run Omarchy?"
    a: "Yes, if you want cheap and predictable. Buy the version without the MX150, put 16 GB or more in it, and plan on no fingerprint login. Prefer the T480 over the T480s if you want the second hot-swap battery, and accept that Omarchy will only show one of the packs."
related: [fingerprint, battery-power, intel-gpu, suspend-sleep, thunderbolt-dock]
draft: false
---

## Verdict

Silver. The 2018 ThinkPad T480 and T480s are Kaby Lake-R machines with Intel UHD 620 graphics, an Intel 8265 Wi-Fi card and HDA audio. Every one of those has been in the kernel for years, and nothing in the Omarchy issue tracker suggests they stop working under 4.x. This is the cheap used laptop that mostly behaves.

Two problems are real and neither is fixed in v4.0.4. Omarchy reads only one battery, which matters because the T480's selling point is two of them. And the fingerprint reader in most units cannot be driven by stock libfprint at all, so the setup wizard fails every time. A third, newer one is worth watching: the bespoke kernel that shipped to everyone in v4.0.4 has a first report of display flicker on this exact GPU.

Everything below was checked against the v4.0.4 source tree and against issues filed on 4.0.x. Where a report is from the 3.x era it says so.

## What works

The clearest evidence is a full `omarchy debug` dump from a T480s (machine type 20L8S27E04, i5-8350U, 8 GB) running 4.0.3 posted in [issue #11721](https://github.com/omacom/omarchy/issues/11721). In it:

- Graphics come up on `i915` with the UHD 620 at PCI ID `8086:5917`, driving the internal 1920x1080 eDP panel under Hyprland 0.56.2.
- Wi-Fi is the Intel 8265/8275 on `iwlwifi`, interface up. Wired is the Intel I219-LM on `e1000e`.
- Bluetooth is the Intel `btusb` adapter, `hci0` up at Bluetooth 4.2.
- Audio is Sunrise Point-LP HD Audio on `snd_hda_intel`, with PipeWire, pipewire-pulse and WirePlumber all active. The T480 predates the SOF-based codecs that cause so much trouble on newer ThinkPads, so `install/hardware/intel/sof-firmware.sh` is not what makes sound work here.
- Both cameras, the regular Chicony one and the IR camera on IR-equipped units, bind to `uvcvideo`. That is a driver binding, not a capture test, so the camera row above stays at unknown.
- Suspend states `freeze,mem,disk` are available and the machine reports `deep` as the configured suspend mode, so the T480 still has real S3 rather than s2idle only.

That is one machine, so treat the Bluetooth and audio lines as "came up on a live system" rather than as a broad guarantee. There are no open T480 issues against any of them.

## What breaks

**The second battery is invisible.** A T480 has an internal BAT0 and a hot-swappable rear BAT1. `omarchy-battery-status` in v4.0.4 still starts with `upower -e | grep BAT | head -n 1`, so the power panel describes BAT0 only, while the bar icon uses UPower's aggregate DisplayDevice. The two disagree, sometimes wildly: in [#6885](https://github.com/omacom/omarchy/issues/6885) the panel showed 94 percent while the icon showed 24 percent on the same machine at the same moment. [#7214](https://github.com/omacom/omarchy/issues/7214) and [#10244](https://github.com/omacom/omarchy/issues/10244) are the same bug reported again, and a commenter on #7214 adds that the power draw reads 0 W while the laptop is actually discharging, because a T480 runs down the rear pack before it touches the internal one, and the script only reads the internal one. [PR #10384](https://github.com/omacom/omarchy/pull/10384) and PR #8864 both propose reading DisplayDevice and summing wattage across packs. Both were still open when this page was written. [#5780](https://github.com/omacom/omarchy/issues/5780) reported the same mismatch against the Waybar notification in May and was closed when Quattro replaced Waybar, not fixed, so the script carried the assumption into the new shell. Detail: [/fix/battery-drains-fast/](/fix/battery-drains-fast/) and [/hardware/battery-power/](/hardware/battery-power/).

**The fingerprint reader does not enroll.** The T480, T480s, T490 and X1 Carbon 6th generation commonly carry the Synaptics Metallica reader `06cb:009a`. Omarchy's `omarchy-hw-fingerprint` sees the USB device and the wizard proceeds, installs `libfprint-git` and `fprintd`, then dies with `Impossible to enroll: GDBus.Error:net.reactivated.Fprint.Error.NoSuchDevice: No devices available`. In [#11721](https://github.com/omacom/omarchy/issues/11721) BeameX points out that libfprint's own hwdb file lists `usb:v06CBp009A*` under known unsupported devices, so this is a missing driver, not a flaky sensor. [#7006](https://github.com/omacom/omarchy/issues/7006) covers the other half: if you already run the AUR `python-validity` plus `open-fprintd` plus `fprintd-clients-git` stack, rerunning the wizard hits an unresolvable package conflict and can leave you with the reader gone. The same complaint goes back to 3.x in [#2046](https://github.com/omacom/omarchy/issues/2046), closed in favor of #2064 with the note that the missing driver is a limitation beyond Omarchy's scope. v4.0.3 shipped an "improve fingerprint-reader support during setup" change, and #11721 was filed against 4.0.3 anyway, so first-run enrollment is still broken. See [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/) and [/hardware/fingerprint/](/hardware/fingerprint/).

**Display flicker on the 4.0.4 kernel.** [#12238](https://github.com/omacom/omarchy/issues/12238) reports random flicker with repeated `i915 [drm] *ERROR* CPU pipe A FIFO underrun` on a T480 after `linux-omarchy 7.2.5-3` replaced stock Arch `linux 7.2.3`. The reporter suspects i915 power features on Kaby Lake and has not bisected it. One report, filed the day this page was checked, so treat it as a lead, not a verdict. The migration keeps your previous kernel installed, so Limine can still boot it.

**Resume is not instant.** On a T480s, [#8447](https://github.com/omacom/omarchy/issues/8447) describes a lock screen that stays frozen for roughly 30 seconds after S3 resume. Authentication actually succeeds immediately; only the picture is stale. The reporter ruled out lock-screen plugins and `hyprmoncfgd`, and found no i915 errors. Open.

**Docked monitor modes.** [#10266](https://github.com/omacom/omarchy/issues/10266) is a T480 in clamshell mode on a dock: a monitor with an explicit `mode` line in `monitors.lua` comes back at 1920x1080 instead of 2560x1440 after a dock reconnect. `hyprctl reload` restores it. See [/fix/multi-monitor-layout-not-saved/](/fix/multi-monitor-layout-not-saved/).

**TPM left on.** Two 3.x-era T480 reports are the same failure: a hang after the LUKS prompt followed by a reboot in [#4296](https://github.com/omacom/omarchy/issues/4296), and a two-minute stall at the login screen after the 3.3.0 update in [#4120](https://github.com/omacom/omarchy/issues/4120). The logs show systemd's TPM2 and PCR services timing out on the T480's TPM, a systemd 259 bug. The fix in both threads was turning TPM off in the BIOS, which the Getting Started chapter of the manual still requires. One T480 in #4120 was stuck in a TPM "MFG mode" it could not disable, and booted only after masking `systemd-tpm2-setup`, `systemd-pcrphase` and the other pcr services on the kernel command line. A separate 3.5 offline ISO bug, an archinstall Limine crash that left a T480 unbootable in [#5330](https://github.com/omacom/omarchy/issues/5330), was fixed in ISO 3.5.1-2.

## What Omarchy does for this model

Nothing by name. `bin/omarchy-hw-match` is the DMI matcher, and it greps `/sys/class/dmi/id/product_name` and `product_family`. No caller in the v4.0.4 tree passes a ThinkPad or T480 pattern, and `install/hardware/lenovo/` contains exactly one script, for Yoga Pro 7 bass speakers. Your T480 gets only the generic Intel path from `install/hardware/all.sh`: `thermald` enabled (Kaby Lake-R clears the Sandy Bridge or newer test), `intel-media-driver` plus `libvpl` and `vpl-gpu-rt` for video acceleration, and the generic Synaptics InterTouch touchpad nudge. `intel-lpmd` is skipped, since that script only matches Alder Lake and newer CPU model numbers.

On DMI, ThinkPads put the machine type in `product_name` and the friendly name in `product_version` and `product_family`. Machine types seen in the cited issues are `20L6S77E00` for a T480 and `20L8S27E04`, `20L7S2QV00` and `20MF000DUS` for the T480s; the T480s family string reads `ThinkPad T480s`. If you write your own quirk, match on the family, not the machine type, because every configuration has a different type code.

## Variants

Prefer the plain T480 if you want the second battery and user-replaceable RAM in both slots. Prefer the T480s if you want a lighter machine and can live with one pack, which incidentally sidesteps the battery reporting bug entirely.

Avoid the MX150 discrete graphics option on the T480 unless you specifically need it. There is no T480 NVIDIA report in the data behind this page, so the hybrid path here is unverified, and hybrid graphics is the single largest source of laptop breakage elsewhere in the tracker. See [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) before you buy one.

Libreboot or Coreboot units without an EFI payload install but never boot: [#4208](https://github.com/omacom/omarchy/issues/4208) is a T480 in exactly that state, the installer finished and the first reboot failed because it assumes UEFI. The response was that nobody on the team runs that setup and a patch would be welcome.

## Before you install

- Check the fingerprint reader with `lsusb | grep -iE '06cb|138a|04f3'` first. If it says `06cb:009a`, plan on password login.
- Put in 16 GB. The 8 GB unit in the #11721 dump sat at 3 GB used with a fairly idle desktop.
- Confirm UEFI, not Libreboot or a BIOS-only Coreboot payload.
- Turn off Secure Boot and TPM in the BIOS before the first boot. The manual requires it, and #4296 and #4120 are what a T480 does with TPM left on.
- Leave the old kernel entry in Limine alone after updating to 4.0.4, in case of #12238.
- Expect the power panel number to be wrong if you have two packs, and check with `upower -i /org/freedesktop/UPower/devices/DisplayDevice` when it matters.
- Read the sleep and fingerprint chapters of the official manual: [system sleep](https://omarchy.org/manual/system-sleep/) and [hardware authentication](https://omarchy.org/manual/hardware-authentication/).

## Related

[/hardware/fingerprint/](/hardware/fingerprint/) · [/hardware/battery-power/](/hardware/battery-power/) · [/hardware/intel-gpu/](/hardware/intel-gpu/) · [/hardware/suspend-sleep/](/hardware/suspend-sleep/) · [/hardware/thunderbolt-dock/](/hardware/thunderbolt-dock/) · [/hardware/lenovo-thinkpad-x1-carbon/](/hardware/lenovo-thinkpad-x1-carbon/) · [/reference/commands/omarchy-battery-status/](/reference/commands/omarchy-battery-status/) · [/releases/v4.0.4/](/releases/v4.0.4/) · [/hardware/submit/](/hardware/submit/)
