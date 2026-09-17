---
title: "Lenovo ThinkPad X1 Carbon on Omarchy"
description: "Omarchy on the ThinkPad X1 Carbon Gen 8 to Gen 14: what works, the Gen 13 speaker and Gen 14 camera breakage, and the hardware scripts that fire."
answer: "Gen 8 through Gen 12 mostly show up in generic Omarchy bugs, with one open Gen 11 random-reboot thread. Gen 13 and Gen 14 carry the hardware bugs: the Gen 14 webcam only works with an out-of-tree IMX471 driver, its microphone needed a Lenovo BIOS update, and one Gen 13 lost its speakers to a SoundWire clash. No ThinkPad quirk script ships in 4.0.4."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Lenovo"
model: "ThinkPad X1 Carbon"
dmi: ["20U9CTO1WW", "20XWCTO1WW", "21HMCTO1WW", "21HNS65E00", "21NS0012US", "21V7CTO1WW"]
cpu: "Intel Core, Comet Lake through Panther Lake"
gpu: "Intel integrated (i915 or xe)"
year: "2020 to 2026"
rating: silver
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: partial
  fingerprint: partial
  gpu: partial
  suspend: partial
  hibernate: partial
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: unknown
quirkScripts:
  - name: "intel/sof-firmware.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/sof-firmware.sh"
    note: "Installs sof-firmware when omarchy-hw-intel-sof finds an Intel audio device in lspci output."
  - name: "intel/thermald.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/thermald.sh"
    note: "Installs and enables thermald on Intel laptops from Sandy Bridge up."
  - name: "intel/lpmd.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/lpmd.sh"
    note: "Installs intel-lpmd for listed hybrid CPU model IDs. No Arrow Lake ID is in the list."
  - name: "intel/video-acceleration.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/video-acceleration.sh"
    note: "Installs intel-media-driver, libvpl and vpl-gpu-rt for HD, UHD, Iris, Xe, Arc and Panther Lake graphics."
  - name: "intel/ipu7-camera.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    note: "Installs intel-ipu7-camera only when ACPI device OVTI08F4 exists. Fires on Gen 14, but that package cannot drive the IMX471 sensor the Gen 14 actually has."
  - name: "intel/fred.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/fred.sh"
    note: "Adds fred=on to the Limine kernel cmdline on Panther Lake. Gen 14 only."
  - name: "omarchy-brightness-keyboard-mute"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-brightness-keyboard-mute"
    note: "Writes the platform::micmute LED node through brightnessctl on any laptop that exposes one."
issueCount: 46
tags: [thinkpad, x1-carbon, lenovo, intel, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10916"
    title: "Issue #10916: ThinkPad X1 Carbon Gen 13: RT1318 speakers permanently silent after SoundWire CTRL_CLASH (empty Cadence PING)"
    kind: issue
    author: "aramsdale"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10250"
    title: "Issue #10250: ThinkPad X1 Carbon Gen 14: lid s2idle never wakes; hibernate reboots; lid-open leaves panel dark"
    kind: issue
    author: "heredia21"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/10252"
    title: "Issue #10252: Lock-on-suspend runs after PrepareForSleep(true), so pam_fprintd can never install fprintd's sleep delay inhibitor"
    kind: issue
    author: "wbnns"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/11005"
    title: "Issue #11005: SOF ThinkPad: no headphone autoswitch, stale HDMI default, MPRIS pause on jack, mute LED dark"
    kind: issue
    author: "JeffFlag"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/7909"
    title: "Issue #7909: Random hard reboots on ThinkPad X1 Carbon Gen 11 - Omarchy only, Ubuntu stable"
    kind: issue
    author: "SuleymanSuleymanzade"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6001"
    title: "Issue #6001: Microphone on ThinkPad X1 Carbon Gen 14 (Panther Lake + CS42L45) silent"
    kind: issue
    author: "ocewers"
    date: "2026-05-30"
  - url: "https://github.com/omacom/omarchy/issues/6000"
    title: "Issue #6000: Camera (IPU7-PTL / OV08X40) on ThinkPad X1 Carbon Gen 14: ACPI status=0, sensor invisible to Linux"
    kind: issue
    author: "ocewers"
    date: "2026-05-30"
  - url: "https://github.com/omacom/omarchy/issues/3619"
    title: "Issue #3619: X1 Carbon Gen 13 LUKS Prompt Black Screen"
    kind: issue
    author: "cutzenfriend"
    date: "2025-11-25"
  - url: "https://github.com/omacom/omarchy/issues/2776"
    title: "Issue #2776: Omarchy not starting and ending in a black screen after first installation"
    kind: issue
    author: "TayoJuang"
    date: "2025-10-23"
  - url: "https://github.com/omacom/omarchy/issues/7776"
    title: "Issue #7776: Built-in camera does not work on a fresh Omarchy install"
    kind: issue
    author: "skovuri41"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/3229"
    title: "Issue #3229: Fingerprint fails, showing fingerprint auth deactivated on hyprlock lockscreen"
    kind: issue
    author: "hojner"
    date: "2025-11-07"
  - url: "https://github.com/omacom/omarchy/issues/731"
    title: "Issue #731: Plymouth not working on ThinkPad X1 Carbon Gen 8 w/ systemd-boot"
    kind: issue
    author: "shawnyeager"
    date: "2025-08-12"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.3"
    title: "Omarchy v3.8.3 release notes"
    kind: release
    date: "2026-07-13"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
credits:
  - name: "ocewers"
    url: "https://github.com/ocewers"
    for: "Traced the Gen 14 microphone and camera failures, found the BIOS update that fixed the mic, and got the IMX471 camera running with an out-of-tree driver and libcamera"
  - name: "heredia21"
    url: "https://github.com/heredia21"
    for: "Mapped Gen 14 lid sleep, hibernate and dark-panel behaviour and corrected the first report"
  - name: "aramsdale"
    url: "https://github.com/aramsdale"
    for: "Documented the Gen 13 SoundWire clash that left the RT1318 speaker amp unattached"
  - name: "AlwxSin"
    url: "https://github.com/AlwxSin"
    for: "Found that removing the kms hook fixes the Gen 13 black LUKS prompt"
  - name: "felipecpaiva"
    url: "https://github.com/felipecpaiva"
    for: "Spotted that thermald was dying at every boot on a Gen 10"
  - name: "wbnns"
    url: "https://github.com/wbnns"
    for: "Measured the fingerprint sleep-inhibitor race on a Gen 8 and retracted the workaround"
  - name: "jriff"
    url: "https://github.com/jriff"
    for: "Confirmed the Gen 14 camera recipe on a second 21V7CTO1WW using the imx471-dkms-git AUR package"
faq:
  - q: "Is the ThinkPad X1 Carbon a good Omarchy laptop?"
    a: "Gen 8 to Gen 12 mostly appear in generic Omarchy bugs, though Gen 11 has an open random-reboot thread worth reading. Gen 13 and Gen 14 carry open hardware bugs, so buy those only if you are willing to debug audio and camera."
  - q: "Does the webcam work on the X1 Carbon Gen 14?"
    a: "Not out of the box. Issue #6000 is still open: the stock intel-ipu7-camera chain delivers black frames. Two owners got 720p30 working with the out-of-tree IMX471 driver plus libcamera. The driver landed in mainline after 7.2, so Arch should carry it at 7.3."
  - q: "Why is my X1 Carbon LUKS prompt a black screen?"
    a: "Reported on Gen 13 in issue #3619. Removing the kms hook from /etc/mkinitcpio.conf and rerunning mkinitcpio -P restored the prompt for two owners."
related: [suspend-sleep, webcam, audio, fingerprint, intel-gpu, lenovo-thinkpad-t14]
draft: false
---

## Verdict

Silver, and the rating hides a split. The older half of this family is one of the calmest things you can run Omarchy on. The newest half is not.

Across 46 tracked issues that mention an X1 Carbon, the failures that trace to the machine itself rather than to Omarchy policy land on Gen 13 and Gen 14. Gen 8 through Gen 12 show up mostly in generic Omarchy bugs that have nothing to do with the chassis, plus one open Gen 11 reboot thread. If you rated Gen 14 on its own it would be bronze today.

Everything below was checked against Omarchy 4.0.4 source and against issue reports filed from August 2025 through Omarchy 4.0.3.

## What works

Graphics are quiet once you are past first boot. On Gen 13 the reporter of the black LUKS prompt said the i915 driver works perfectly once the system is up, and later booted the same machine with xe loaded. The caveat is issue #2776, where a Gen 13 showed nothing but a black screen after a fresh ISO install on 3.1.1, and the #3619 reporter said in that same thread that installing `linux-firmware-intel` is what finally brought his identical machine up. That is why `gpu` is marked partial here and not works. After first boot no Gen 8 to Gen 14 report in the set blames the Intel stack for a compositor that will not start: the one login loop, issue #6439 on a Gen 12, was traced by its own reporter to a hand-written `monitors.conf`.

The ThinkPad mic-mute lamp works. Omarchy writes the `platform::micmute` LED node through `omarchy-brightness-keyboard-mute`, which is wired into `omarchy-audio-input-mute`. That path started as a ThinkPad contribution in 3.6.0 and was folded into the unified command in 3.7.0. The Gen 9 owner in issue #11005 confirms it, and confirms the F1 mute key itself mutes PipeWire; only the speaker-mute lamp stays dark.

Enrollment and verification do work on the Gen 8 Synaptics `06cb:00bd` reader, and between incidents it unlocks the lock screen normally. The subsystem is only partial because the enrollment does not stay put, which is the Gen 8 entry below. The other X1 Carbon fingerprint thread in the set is issue #3229, a Gen 12 whose reader stopped answering hyprlock after more than a couple of minutes idle; it closed unfixed on 2026-07-18 when Quattro replaced hyprlock, with a request to refile if it recurs. See the manual chapter on [hardware authentication](https://omarchy.org/manual/hardware-authentication/) for the setup path.

The Gen 13 camera works. The Gen 14 reporter in issue #6000 says the Gen 13, on Lunar Lake with IPU7-LNL, ran correctly on the same Omarchy install.

Wi-Fi, Bluetooth, touchpad, keyboard and battery life are marked unknown on purpose. No Gen 8 to Gen 14 report in the set describes any of them as broken hardware, and the one Bluetooth report in the whole set, issue #5807, is a Gen 7 on a dev branch. Absence of complaints is not a test result. If you have run one of these machines for a while, [submit what you found](/hardware/submit/).

## What breaks

**Gen 14 camera, open but solvable.** Issue #6000 started as a dead sensor: the media graph had no sensor entity and `/dev/video50` emitted black NV12 frames on Omarchy 3.8.2. The reporter's first two diagnoses turned out wrong, and on 2026-07-20 the same reporter corrected the record. The sensor is a Sony IMX471 at ACPI node `TBE20A0`, not the OV08X40 that `intel-ipu7-camera` targets, so Omarchy's stock icamerasrc chain cannot drive it. With the out-of-tree IMX471 kernel series and libcamera's software ISP, the camera runs at 720p30 in browsers and Teams. A second 21V7CTO1WW owner reproduced it on the stock `linux` kernel via the `imx471-dkms-git` AUR package plus `libcamera`, `pipewire-libcamera` and a `libcamerasrc` relayd config. The IMX471 driver and its `TBE20A0` binding have since landed in mainline, tagged after 7.2, so stock Arch should carry them at 7.3. Nothing in 4.0.4 ships them. A separate report, issue #7776, filed as an X1 Aura 14 but identifying itself as a Gen 14 by PCI subsystem ID, shows the same dead sensor on a fresh install; its reporter later dumped ACPI and found `TBE20A0` enabled at 15 with `OVTI08F4` at 0, the same signature as #6000. The `IPU7 in secure mode` line quoted in that report is a red herring, and a maintainer showed why: it is a routine `dev_info` that prints on working machines too.

**Gen 14 microphone, fixed by firmware, not by Omarchy.** Issue #6001 tracked a silent CS42L45 microphone with no matching SOF topology. It closed on 2026-06-08 when the reporter updated the Lenovo BIOS from N4OET47W (1.10) to N4OET49W (1.12) through Omarchy's firmware updater. The reporter's own note: the lid had to be open for the update to apply.

**Gen 14 lid and hibernate.** Issue #10250 is open. Lid-open does not light the internal panel when there is no external display, because the stock binding for `switch:off:Lid Switch` is `omarchy-hyprland-monitor-clamshell`, which only re-enables DPMS on the internal panel when it had been put into clamshell mode by an external display. Hibernate does not come back as a resume on that machine while zram sits at priority 100 above the resume swapfile, so `systemctl hibernate` returns a cold SDDM login. The reporter later corrected himself: stock lid-close sleep does wake on that hardware, and the never-wakes reports came from his own lid-ignore experiments.

**Gen 13 internal speakers.** Issue #10916 is the ugliest report in the set. After four or five days of normal use on a new Gen 13, the RT1318 amp on SoundWire link 1 went `UNATTACHED` after a `DATA_CLASH` and `CTRL_CLASH`, and never came back, on Linux or on Windows. Nobody has shown Omarchy caused it, and the reporter does not claim that either. Treat it as one unexplained incident, not a pattern.

**Gen 13 black LUKS prompt.** Issue #3619, closed. The prompt is invisible at the Plymouth stage while the password still types through blind. Removing the `kms` hook from `/etc/mkinitcpio.conf` and running `sudo mkinitcpio -P` fixed it for two owners.

**Gen 11 random hard reboots.** Issue #7909 is open and unresolved. Spontaneous resets with no panic, no MCE, no thermal event, on both `linux` and `linux-lts`, with Ubuntu stable on the same machine. A second Gen 11 owner sees the same reset signature on Fedora 44 with niri, which argues against an Omarchy-specific cause. A third owner reported hard hangs on CachyOS and Manjaro, then traced his own hangs to Netbird running in kernel mode, so that data point no longer counts. An IdeaPad owner in the same thread said a full Omarchy update made his resets stop, then hit the same crash again four days later on 4.0.3, so read that as a pause rather than a fix. Buyers of used Gen 11 units should know this thread exists.

**Gen 9 audio policy.** Issue #11005 collects four SOF gaps on a Gen 9: plugging headphones does not switch output because Speaker and Headphones are separate UCM card profiles, the ALSA HDMI jack stays on long after the monitor is unplugged so a speakerless display keeps winning the default sink, switching profiles pauses MPRIS players, and the `platform::mute` speaker lamp stays dark because it follows ALSA Master rather than PipeWire mute.

**Gen 8 fingerprint during suspend.** Issue #10252, closed. `omarchy-system-sleep-monitor` locks after logind emits `PrepareForSleep(true)`, so `fprintd` can no longer take a sleep inhibitor. The measured gap was 283 ms with the reader open, 8 inhibitor failures across 10 suspends over 14 days. The expensive part is what happened to the enrollment: the on-chip template store on that reader read back as empty three times over the life of the report, on the first incident and again on 2026-09-13 and 2026-09-16, and match-on-chip templates cannot be rebuilt from the 118-byte host receipts, so every finger has to be enrolled again. The reporter is careful that the link between the race and the wipe is inference, not proof. He also retracted his workaround twice and asks people to remove it: stopping `fprintd` does not release the reader, and the hook cuts it mid-identify instead. The only other Gen 8 report, issue #731 about Plymouth not appearing with systemd-boot, closed as a config mistake: Plymouth needs its cmdline options when used with a unified kernel image.

## What Omarchy does for this model

Nothing by name. Grep `bin/`, `install/hardware/` and `default/` in the v4.0.4 tree and there is no ThinkPad match anywhere. The only script under `install/hardware/lenovo/` is `fix-yoga-pro7-bass-speakers.sh`, which matches the DMI string `Yoga Pro 7 14IAH10` and skips every X1 Carbon.

What you actually get is the generic Intel path from `install/hardware/all.sh`:

- `intel/sof-firmware.sh` installs `sof-firmware` when an Intel audio DSP is present. Without it PipeWire only shows a Dummy Output. v3.8.3 widened this across Arrow Lake, Meteor Lake, Wildcat Lake and Panther Lake and made it ask for a reboot.
- `intel/video-acceleration.sh` pulls `intel-media-driver`, `libvpl` and `vpl-gpu-rt` for Iris and Xe graphics.
- `intel/thermald.sh` and `intel/lpmd.sh` add thermal and low-power management. Worth checking after install: a Gen 10 owner in issue #7909 found `thermald` had been dying at every boot for weeks with `Unsupported cpu model or platform`, and fixed it with a drop-in adding `--ignore-cpuid-check`. Note that `lpmd.sh` gates on a fixed list of CPU model IDs covering Alder, Raptor, Meteor, Lunar and Panther Lake. There is no Arrow Lake ID in that list, and nothing older than Alder Lake, so Gen 8 and Gen 9 skip it too.
- `intel/ipu7-camera.sh` installs `intel-ipu7-camera` only if an ACPI device with HID `OVTI08F4` exists. The Gen 14 exposes that node, so the package installs, but the real sensor is the IMX471 at `TBE20A0` and the package does nothing for it.
- `intel/fred.sh` writes a Limine drop-in adding `fred=on` on Panther Lake, so Gen 14 only.
- `intel/fix-wifi7-eht.sh` disables 802.11be, but only for PCI IDs `8086:e440` and `8086:272b`. An AX211 card does not match.

`bin/omarchy-hw-match` is the tool these scripts use, and it greps `/sys/class/dmi/id/product_name` or `product_family` case-insensitively. Reporters in these threads name their machines by the Lenovo machine type, so read both of those nodes on your own unit before you write an override that matches a string like `21V7CTO1WW`.

## Variants

Machine types seen in the reports: `20U9CTO1WW` (Gen 8), `20XWCTO1WW` (Gen 9), `21HMCTO1WW` and `21HNS65E00` (Gen 11), `21NS0012US` (Gen 13), `21V7CTO1WW` (Gen 14).

- **Gen 8 to Gen 10.** The safe used buy. Comet Lake through Alder Lake, Intel Wi-Fi, Synaptics reader, well-trodden i915.
- **Gen 11.** Raptor Lake-P with Iris Xe. Good hardware, but read issue #7909 before you commit.
- **Gen 12.** Meteor Lake. Mostly generic Omarchy bugs in the set. The one hardware-flavoured report, fingerprint auth going dead after idle on the old hyprlock stack, closed without a fix when Quattro arrived.
- **Gen 13.** Two different silicon configurations appear in the reports, one described as Arrow Lake-U and one as Lunar Lake. Camera works, speakers have one bad incident, the LUKS prompt needed the kms hook removed on one Arrow Lake-U unit, and one owner needed `linux-firmware-intel` before a fresh install would draw anything at all.
- **Gen 14.** Panther Lake. Avoid unless you want to do enablement work. Camera needs an out-of-tree driver, microphone needs current firmware, hibernate is not usable as shipped.

## Before you install

1. Update the Lenovo BIOS from Windows or through the Omarchy firmware updater first. On Gen 14 that is what fixed the microphone. Keep the lid open while it applies.
2. Snapshot before every update. Two reporters in this set diagnosed problems by booting a prior Snapper snapshot.
3. On Gen 13, if the LUKS prompt is a black screen, do not reach for `nomodeset`. Remove the `kms` hook and rerun `mkinitcpio -P`.
4. After the first boot, run `journalctl -u thermald` and confirm it is running rather than dying on a cpuid check.
5. On Gen 14, do not rely on hibernate. Check `swapon --show` and see whether zram outranks your swapfile.
6. If you use fingerprint unlock on a Gen 8, expect the reader to re-enumerate on every resume. See [Omarchy's system sleep chapter](https://omarchy.org/manual/system-sleep/) for the suspend toggle and hibernation setup.

## Related

- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/)
- [/hardware/webcam/](/hardware/webcam/) and [/fix/webcam-not-detected/](/fix/webcam-not-detected/)
- [/hardware/audio/](/hardware/audio/) and [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/)
- [/hardware/fingerprint/](/hardware/fingerprint/) and [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/)
- [/hardware/intel-gpu/](/hardware/intel-gpu/), [/hardware/lenovo-thinkpad-t14/](/hardware/lenovo-thinkpad-t14/), [/hardware/lenovo-thinkpad-t480/](/hardware/lenovo-thinkpad-t480/)
- [/fix/hibernate-fails-or-hangs/](/fix/hibernate-fails-or-hangs/) and [/releases/still-broken/](/releases/still-broken/)
