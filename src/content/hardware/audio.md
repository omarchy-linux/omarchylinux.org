---
title: "Audio on Omarchy Linux"
description: "How audio works on Omarchy 4.x: PipeWire defaults, the SOF firmware and speaker tuning install hooks, the bugs that still bite, and the fix order."
answer: "Audio on Omarchy 4.x is plain PipeWire, WirePlumber and pipewire-pulse, with nothing Omarchy-specific in the path for ordinary hardware. Omarchy adds three things: sof-firmware on Intel DSP laptops, a soft-mixer rule on ASUS ROG, and a measured speaker tuning on the 2026 XPS 14/16. When sound dies, run omarchy-restart-audio first, then check the ALSA hardware mixer with amixer, then test the stock Arch kernel."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "audio"
issueCount: 267
tags: [audio, pipewire, wireplumber, speakers, microphone, sof]
sources:
  - url: "https://github.com/omacom/omarchy/issues/4821"
    title: "Issue #4821: No Sound Fix, ASUS ROG Strix G16 (2025) on Omarchy 3.4.1"
    kind: issue
    author: "beyondeye"
    date: "2026-02-28"
  - url: "https://github.com/omacom/omarchy/issues/4801"
    title: "Issue #4801: Speaker output not working in Asus Zephyrus G14 after 3.4 update"
    kind: issue
    author: "abhiram-ar"
    date: "2026-02-28"
  - url: "https://github.com/omacom/omarchy/issues/5557"
    title: "Issue #5557: No sound on ASUS Zenbook S14 UX5406AA (Panther Lake)"
    kind: issue
    author: "Pegorim"
    date: "2026-05-03"
  - url: "https://github.com/omacom/omarchy/issues/6952"
    title: "Issue #6952: Quickshell SIGSEGV in QQuickRepeater when PipeWire removes USB audio nodes"
    kind: issue
    author: "sanjyay"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/12086"
    title: "Issue #12086: Internal speakers silent on Legion Pro 7 16IRX8H; TAS2781 binding changes with codec SSID override"
    kind: issue
    author: "slavkof"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12008"
    title: "Issue #12008: MacBook9,1 / 10,1 internal speakers silent after install"
    kind: issue
    author: "karlentwistle"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12131"
    title: "Issue #12131: linux-omarchy 7.2.5 kernel causes constant HDMI audio underruns on Haswell Mac"
    kind: issue
    author: "rissanssi"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12188"
    title: "Issue #12188: linux-omarchy kernel breaks screen backlight and USB audio volume on Dell XPS 14 (Panther Lake)"
    kind: issue
    author: "cthybert"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12204"
    title: "Issue #12204: omarchy-audio-output-sink fails to resolve physical sink for EasyEffects"
    kind: issue
    author: "layolayo"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12191"
    title: "Issue #12191: omarchy-audio-tuning fronted-sink ignores community omarchy_speaker_tuning sinks"
    kind: issue
    author: "roehrbacher"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12113"
    title: "Issue #12113: Bluetooth HFP microphone captures complete silence on OnePlus Bullets Wireless Z2 and JBL Tune 770NC"
    kind: issue
    author: "arsinghin"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12047"
    title: "Issue #12047: Blue Yeti microphone detected but produces no capture after reboot"
    kind: issue
    author: "daveplatt71"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1818"
    title: "Issue #1818: Bluetooth Audio Devices Doesn't Work"
    kind: issue
    author: "matheorism"
    date: "2025-09-19"
  - url: "https://github.com/omacom/omarchy/pull/5336"
    title: "PR #5336: Enable Bluetooth A2DP auto-connect in WirePlumber"
    kind: pr
    author: "dandresrp"
    date: "2026-05-07"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/docs/AUDIO-TUNING.md"
    title: "Omarchy docs: Speaker tunings"
    kind: docs
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "Nobody1902"
    url: "https://github.com/Nobody1902"
    for: "Traced silent ASUS ROG speakers to the shipped alsa-soft-mixer.conf"
  - name: "beyondeye"
    url: "https://github.com/beyondeye"
    for: "Documented the ALC285 hardware mixer and soft-mixer interaction in detail"
  - name: "Pegorim"
    url: "https://github.com/Pegorim"
    for: "Built a kernel with the two upstream SOF patches that bring up Zenbook S14 audio"
  - name: "karlentwistle"
    url: "https://github.com/karlentwistle"
    for: "Found that MacBook9,1 speakers also need the EFI chime un-muted"
faq:
  - q: "Does Omarchy use PulseAudio or PipeWire?"
    a: "PipeWire, with WirePlumber as session manager and pipewire-pulse for PulseAudio clients. That is why pactl and wpctl both work."
  - q: "How do I restart audio without rebooting?"
    a: "Run omarchy-restart-audio, or pick Update then Hardware then Audio in the Omarchy menu. It restarts the three user services and can reset a stuck USB audio device."
  - q: "What is the speaker tuning and can I turn it off?"
    a: "A PipeWire filter chain placed in front of the internal speaker sink on laptops Omarchy ships a measured profile for. Run omarchy audio tuning status to see it, and omarchy audio tuning off to remove it."
  - q: "My sound broke right after the 4.0.4 update. What changed?"
    a: "4.0.4 made the bespoke linux-omarchy kernel the default boot entry. Two reports filed the next day, HDMI underruns on a 2013 MacBook Pro and lost USB speaker volume on an XPS 14, both vanish when the reporter picks the stock Arch linux kernel in the Limine menu. Test that before anything else."
related: [no-sound-from-laptop-speakers, bluetooth-stops-after-resume, quickshell-crashes-or-bar-missing]
draft: false
---

Audio on Omarchy is stock Arch audio. PipeWire, WirePlumber and pipewire-pulse do the work, and Omarchy adds a thin layer of hardware hooks and CLI helpers on top. For ordinary hardware there is nothing Omarchy-specific in the path. The failures cluster in a few predictable places, and the list below comes from the 267 audio-tagged issues in the tracker plus the v4.0.4 source tree.

## Status on 4.0.4

Omarchy ships no audio configuration of its own for ordinary HDA codecs, USB DACs and headsets, HDMI and DisplayPort output, or Bluetooth A2DP. On that hardware you get stock Arch PipeWire behaviour plus the WirePlumber A2DP auto-connect rule that arrived in 3.8.0.

Reliably rough: Intel SoundWire laptops whose machine driver the kernel does not yet match, laptops whose smart amplifier is driven by a separate chip such as TAS2781 or CS35L56, Bluetooth HFP microphones, and Apple hardware older than the T2 era.

New on 4.0.4 and worth knowing: the release made the bespoke `linux-omarchy` kernel the default boot entry for everyone. Two audio regressions filed the day after it shipped both disappear when the reporter boots the stock Arch `linux` kernel from the Limine menu instead. If your sound changed on 15 or 16 September 2026, that is the first thing to test.

## What Omarchy does automatically

The root-side hooks live in `install/hardware/` and run through `omarchy-apply-hardware` when the ISO is finalized; the per-user ones live in `install/user/hardware/` and run from `omarchy-finalize-user`. A regular `omarchy-update` does not rerun them. A fix that lands after your install reaches you only when it also ships as a migration, which is how the wider `sof-firmware` check got to existing machines in 3.8.3.

- **Intel SOF firmware.** `install/hardware/intel/sof-firmware.sh` calls `omarchy-hw-intel-sof`, which just looks for an Intel audio controller in `lspci`. If one is there, `sof-firmware` is installed. The script's own comment is blunt about why: without that firmware the `sof-audio-pci-intel-*` drivers give you a Dummy Output and nothing else. This hook arrived in 3.8.0 for Panther Lake and was widened in 3.8.3 to Arrow Lake, Meteor Lake and Wildcat Lake.
- **ASUS ROG soft mixer.** `install/user/hardware/asus/fix-audio-mixer.sh` copies `alsa-soft-mixer.conf` into your WirePlumber config, wipes the saved default routes, and sets `Master` to 80 percent unmuted on an ALC285 card. A companion script drops `Internal Mic Boost` to zero and sets capture to 70 percent, because the default boost clips.
- **Lenovo Yoga Pro 7 bass.** `install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh` matches the DMI string `Yoga Pro 7 14IAH10` and writes a modprobe option pinning the ALC287 to the `alc287-yoga9-bass-spk-pin` model, so both amplifier speakers get signal.
- **Framework 13 AMD input.** `fix-f13-amd-audio-input.sh` sets the AMD card profile to the HiFi variant that exposes both microphones plus the speaker.
- **Speaker tunings.** On a match, `install/hardware/speaker-tuning.sh` pulls in `lsp-plugins-lv2`, and at first login `omarchy audio tuning on` installs a PipeWire filter chain in front of the internal speaker sink. Only the 2026 Dell XPS 14 and XPS 16 ship one today, matched on DMI product SKU `0DB9` and `0DBA`. The XPS 14 profile was measured, the XPS 16 is covered on report only, and the config file says so.

The tuning runs as its own PipeWire client under `omarchy-speaker-tuning.service` rather than inside the daemon, so switching it does not drop every PulseAudio client. If the tuning sink fails to appear, or links to the wrong sink, the script removes itself and leaves your audio untouched.

You also get the Quickshell audio panel on `SUPER + CTRL + A`, volume keys routed through `omarchy-audio-output-volume`, output rotation on `SHIFT + XF86AudioMute`, and `omarchy-restart-audio` wired into the menu at Update, Hardware, Audio.

## Known problems

### Known issues

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#6952](https://github.com/omacom/omarchy/issues/6952) shell segfaults when PipeWire nodes vanish | Any, triggered by USB DACs, AirPods on AAC, WirePlumber restarts | open | not yet |
| [#4821](https://github.com/omacom/omarchy/issues/4821), [#4801](https://github.com/omacom/omarchy/issues/4801) soft mixer leaves ALC285 hardware controls muted | ASUS ROG Strix and Zephyrus G14, G16, G17, Flow | open, workaround known | not yet |
| [#5557](https://github.com/omacom/omarchy/issues/5557) `sof_sdw` fails to instantiate the card | ASUS Zenbook S14 UX5406AA | open, needs upstream kernel patches | not yet |
| [#12086](https://github.com/omacom/omarchy/issues/12086) TAS2781 amplifier does not bind to the HDA codec at boot | Lenovo Legion Pro 7 16IRX8H | open | not yet |
| [#12008](https://github.com/omacom/omarchy/issues/12008) CS4208 speakers silent, needs driver plus EFI chime un-mute | MacBook9,1 and 10,1 | open | not yet |
| [#12131](https://github.com/omacom/omarchy/issues/12131) constant HDMI audio underruns on the Omarchy kernel | MacBookPro11,2 Haswell | open | not yet |
| [#12188](https://github.com/omacom/omarchy/issues/12188) USB speaker loses volume headroom on the Omarchy kernel | Dell XPS 14 DA14260 | open | not yet |
| [#12204](https://github.com/omacom/omarchy/issues/12204) volume keys act on `easyeffects_sink`, not the speakers | Any machine running EasyEffects | open | not yet |
| [#12191](https://github.com/omacom/omarchy/issues/12191) `fronted-sink` ignores community tuning sinks | Desktops using a third-party calibrator plugin | open | not yet |
| [#12113](https://github.com/omacom/omarchy/issues/12113) Bluetooth HFP microphone records silence | OnePlus Bullets Wireless Z2, JBL Tune 770NC | open | not yet |
| [#12047](https://github.com/omacom/omarchy/issues/12047) USB microphone detected but capture clock stays at zero | Blue Yeti 046d:0ab7 | open, workaround known | not yet |
| [#1818](https://github.com/omacom/omarchy/issues/1818) Bluetooth headsets connect but never appear as sinks | Sony XM5, AirPods Pro 2 and others | closed May 2026 | 3.8.0 |

Two patterns dominate. The first is the ASUS ROG one. Omarchy's own soft-mixer rule stops PipeWire from touching ALSA hardware controls, and on the ALC285 the kernel's jack detection keeps resetting `Headphone Playback Switch` to off. Nothing then unmutes it. The rule exists to avoid other Realtek volume quirks, so it helps some machines and silences others.

The second is the smart amplifier problem. CS35L56 on SoundWire and TAS2781 over I2C both need the right machine description, firmware and topology before the speakers make any noise at all. On the Zenbook S14 the log shows `sof_sdw sof_sdw: ASoC: failed to instantiate card -22` and `aplay -l` reports no soundcards. Pegorim built a kernel with two upstream SOF patches and got speakers, jack, microphone and HDMI all working, which pins the cause outside Omarchy.

The Bluetooth sink problem in #1818 closed when [#5336](https://github.com/omacom/omarchy/pull/5336) added a WirePlumber rule that auto-connects the A2DP sink and source profiles. It merged on 7 May 2026 and shipped two days later in 3.8.0, which is why it is the only row above with a version.

The Quickshell crash in #6952 is not a sound failure but it looks like one, because the bar disappears when a USB DAC or a Bluetooth headset re-registers. Several reporters traced it to the audio panel holding live PipeWire node objects that go null underneath it.

## Fixes that work

Try these in order. Stop when sound comes back.

1. `omarchy-restart-audio`. It restarts WirePlumber, PipeWire and pipewire-pulse, and if `wpctl` is still unresponsive it looks for a USB audio device stuck in SETUP state and resets it with `usbreset`. This clears most "it worked an hour ago" cases.
2. Check the real hardware mixer, not the PipeWire one. `amixer -c <n> contents`; alsa-utils is in the base package set. PipeWire can report 30 percent volume and no mute while `Master Playback Switch` is off underneath.
3. On an ASUS ROG laptop, remove the soft-mixer file: `rm ~/.config/wireplumber/wireplumber.conf.d/alsa-soft-mixer.conf` and restart audio. Reporters on the Strix G16, Zephyrus G14, G16, M16 and Flow X13 confirmed it in #4821, and the Strix G17 reporter in #4801 got the same result by moving the whole WirePlumber config aside.
4. If you only have a Dummy Output, check `journalctl -b -k | grep -iE 'sof|snd'`. A missing `sof-firmware` package is a one-line fix. A `failed to instantiate card -22` is not, and means waiting on a kernel.
5. Since 4.0.4, boot the stock Arch `linux` kernel once from the Limine menu and test again. Distortion, underruns and lost volume headroom on the `linux-omarchy` build have all been reported this way.
6. If a speaker tuning is active and the sound is wrong rather than absent, `omarchy audio tuning status` shows what matched and `omarchy audio tuning off` reverts you to raw speakers.
7. For a virtual sink, remember that `omarchy-audio-output-sink` resolves through it. With EasyEffects that resolution currently fails, so set the hardware sink volume directly with `pactl set-sink-volume`.

On 3.x the picture differs in two places: the bar was Waybar and there was no audio panel, since `SUPER + CTRL + A` arrived with 4.0.0, and speaker tunings did not exist before 4.0.0. The SOF firmware hook and the ASUS mixer scripts both predate 4.0 and behave the same.

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, `dmesg`, the current boot's warnings and errors from the journal, and your full package list. Attach that.

Add the audio specifics the debug log does not spell out: `wpctl status`, `pactl list sinks`, `aplay -l`, `cat /proc/asound/cards`, and `journalctl -b -k | grep -iE 'sof|snd_hda|cs35l|tas27'`. Name the codec and its subsystem ID, because fixes are keyed on the PCI SSID. Say which kernel you booted, `linux-omarchy` or stock Arch `linux`, and whether the other one behaves differently. That A/B result is the most useful single line in an audio report right now.

## Related

- [No sound from laptop speakers](/fix/no-sound-from-laptop-speakers/)
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Bluetooth](/hardware/bluetooth/)
- [T2 Macs](/hardware/t2-mac/)
- [ASUS ROG Zephyrus](/hardware/asus-rog-zephyrus/)
- [Dell XPS 14 (2026)](/hardware/dell-xps-14-2026/)
- [Lenovo Legion](/hardware/lenovo-legion/)
- [omarchy-restart-audio](/reference/commands/omarchy-restart-audio/)
- [omarchy-audio-tuning](/reference/commands/omarchy-audio-tuning/)
- [Omarchy 4.0.4](/releases/v4.0.4/)
- [Submit your hardware report](/hardware/submit/)
