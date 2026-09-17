---
title: "No sound from laptop speakers on Omarchy"
description: "Silent built-in speakers on Omarchy 4: restart PipeWire, install sof-firmware, drop the ASUS soft-mixer config, and read the CS35L56 amp firmware log."
answer: "Run omarchy restart audio first, then check wpctl status. If you only see Dummy Output, install sof-firmware and reboot. If sinks exist but have no ports since the September update, downgrade wireplumber to 0.5.15. On ASUS ROG laptops delete ~/.config/wireplumber/wireplumber.conf.d/alsa-soft-mixer.conf and restart WirePlumber. On Dell XPS machines with CS35L56 amps, grep the kernel log for FIRMWARE_MISSING, an open upstream bug, not an Omarchy setting."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: audio
issueCount: 244
errorStrings:
  - "Dummy Output"
  - "cs35l56 spi-cs35l56-left: FIRMWARE_MISSING"
  - "Calibration disabled due to missing firmware controls"
  - "Can't read tuning IDs"
  - "sof_sdw sof_sdw: ASoC: failed to instantiate card -16"
  - "SOF firmware and/or topology file not found."
  - "Check if you have 'sof-firmware' package installed."
tags: [audio, speakers, pipewire, wireplumber, cs35l56, sof-firmware, asus-rog]
sources:
  - url: "https://github.com/omacom/omarchy/issues/4821"
    title: "Issue #4821: No Sound Fix: ASUS ROG Strix G16 (2025) on Omarchy 3.4.1"
    kind: issue
    author: "beyondeye"
    date: "2026-02-28"
  - url: "https://github.com/omacom/omarchy/issues/11046"
    title: "Issue #11046: ASUS ROG: soft-mixer caps hardware Master at 80% so bar 100% is not full volume"
    kind: issue
    author: "rdoupe"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/6110"
    title: "Issue #6110: No audio on Intel Arrow Lake: sof-firmware not installed, DSP fails to boot (Dummy Output)"
    kind: issue
    author: "hyprcat"
    date: "2026-06-19"
  - url: "https://github.com/omacom/omarchy/issues/11320"
    title: "Issue #11320: No speaker audio on Dell XPS 13 DX13260 (2026): CS35L56 amp firmware never loads"
    kind: issue
    author: "Gundrak"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/9687"
    title: "Issue #9687: dell-xps13-sidecar-amps: reports success but speakers stay silent on spkid0 units (XPS 13 DX13260)"
    kind: issue
    author: "wizaj"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10543"
    title: "Issue #10543: Dell XPS 13 DX13260 (1028:0e53): no sound at all after dell-xps13-sidecar-amps workaround"
    kind: issue
    author: "MBvisti"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/7427"
    title: "Issue #7427: Dell XPS 13 (0E53) has no bass: CS35L56 woofer amps never load firmware without the sof_sdw sidecar quirk"
    kind: issue
    author: "jonnyace"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/pull/7032"
    title: "PR #7032: Enable Dell XPS 13 sidecar speaker amplifiers"
    kind: pr
    author: "spencerbull"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy-pkgs/pull/150"
    title: "omarchy-pkgs PR #150: Add Dell XPS 13 sidecar amplifier workaround"
    kind: pr
    author: "spencerbull"
    date: "2026-08-25"
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
  - url: "https://github.com/omacom/omarchy/issues/11350"
    title: "Issue #11350: Kernel Regression Omarch audio works on 7.1.9 but breaks after the 7.2.3 kernel update"
    kind: issue
    author: "jBNeo"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.3"
    title: "Omarchy v3.8.3 release notes"
    kind: release
    date: "2026-07-13"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 Quattro release notes"
    kind: release
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "beyondeye"
    url: "https://github.com/beyondeye"
    for: "Traced silent ASUS ROG output to the soft-mixer config blocking PipeWire from unmuting hardware switches"
  - name: "hyprcat"
    url: "https://github.com/hyprcat"
    for: "Showed that the Intel SOF firmware hook only matched Panther Lake, leaving Arrow Lake with a Dummy Output"
  - name: "wizaj"
    url: "https://github.com/wizaj"
    for: "Isolated the CS35L56 spkid0 firmware gap on the XPS 13 and took it upstream to Cirrus"
  - name: "rdoupe"
    url: "https://github.com/rdoupe"
    for: "Measured the 80 percent hardware Master ceiling left behind by the ASUS mixer fix"
  - name: "zygote55"
    url: "https://github.com/zygote55"
    for: "Traced the September zero-port sinks to a WirePlumber 0.5.17 v4l2 hook stall rather than the kernel"
faq:
  - q: "Why does the volume slider show 100 percent while nothing plays?"
    a: "Because that slider is the software mixer. With api.alsa.soft-mixer enabled, PipeWire never reads or writes the ALSA hardware controls, so a muted hardware switch is invisible to it. Check amixer -c <card> contents to see the real state."
  - q: "Where did wiremix go in Omarchy 4?"
    a: "Quattro dropped it. The upgrade script removes wiremix and ~/.config/wiremix, and the shell audio panel on SUPER + CTRL + A replaced it. Install pavucontrol or wiremix yourself if you want a separate mixer."
  - q: "Is omarchy audio tuning the reason my speakers are silent?"
    a: "Rarely. A tuning only ships for the 2026 Dell XPS 14 and 16 today. If the graph fails to build, for example when lsp-plugins-lv2 is missing, the tuning sink never appears and playback stays on the raw speaker sink. Run omarchy audio tuning status to see."
  - q: "My speakers worked before I updated. What changed?"
    a: "Check pacman -Qi wireplumber first. Issue #11350 opened as a 7.1.9 to 7.2.3 kernel regression and was corrected in the thread: WirePlumber 0.5.17 leaves every ALSA sink with zero ports on machines where a rule disables a V4L2 device, which the intel-ipu7-camera package does on Intel laptops. Downgrading to 0.5.15 restored audio for the reporters. 4.0.4 also moved everyone to the linux-omarchy kernel and left the old one installed, so the stock linux entry in Limine tests the kernel theory in one reboot."
related: [bluetooth-stops-after-resume, dictation-voxtype-not-working, quickshell-crashes-or-bar-missing]
draft: false
---

Silent built-in speakers on Omarchy are usually one of five unrelated faults: the stream is going somewhere else, the audio DSP never loaded firmware, the session manager built sinks with no ports, a hardware mixer control is muted where PipeWire cannot see it, or a smart amplifier refused to load its tuning blob. The steps below split them apart. Everything here was checked against the v4.0.4 source tree, with notes where 3.x differs.

## The fix

**1. Confirm where the sound is actually going.** Open the audio panel with `SUPER + CTRL + A`, or from a terminal:

```bash
wpctl status
pactl list sinks | grep -E "Name:|Active Port:|Mute:|Volume:"
```

If the default sink is an HDMI monitor or a USB dock, pick the speakers in the panel. `SHIFT + XF86AudioMute` cycles outputs. If the only sink listed is `Dummy Output`, skip to step 3.

**2. Restart the audio stack.** On 4.x:

```bash
omarchy restart audio
```

The same thing lives in the Omarchy menu under Update > Hardware > Audio. `omarchy-restart-audio` restarts pipewire, pipewire-pulse and wireplumber, and if `wpctl` still does not answer it looks for a USB audio device stuck in `SETUP` state and resets it. On 3.x the command was `omarchy-restart-pipewire`, which only restarts the services.

**3. No soundcard at all, or only Dummy Output, on an Intel laptop.** Check the kernel log:

```bash
sudo dmesg | grep -i sof
```

Lines like `SOF firmware and/or topology file not found` and `Check if you have 'sof-firmware' package installed` mean the DSP never booted. Install the firmware and reload the driver, or reboot:

```bash
sudo pacman -S sof-firmware
```

Omarchy 3.8.3 fixed the install hook that caused this. Before it, the hook only matched Panther Lake, so Arrow Lake, Meteor Lake and similar machines shipped without `sof-firmware`, as hyprcat documented in issue #6110. Since 3.8.3 the gate is `omarchy-hw-intel-sof`, which matches any Intel audio controller, and the same release shipped a migration that adds the package on existing installs. If `pacman -Q sof-firmware` still comes back empty on an updated machine, install it by hand as above.

**4. ASUS ROG laptops: remove the soft-mixer config.** Omarchy installs `~/.config/wireplumber/wireplumber.conf.d/alsa-soft-mixer.conf` on ROG hardware. It sets `api.alsa.soft-mixer = true`, which tells PipeWire to do volume in software and never touch the ALSA controls. beyondeye's issue #4821 traced the consequence on an ALC285 Strix G16: the hardware `Master` switch started out muted at zero, the kernel's jack detection switched `Headphone` off on every boot, and with the soft mixer in place PipeWire never ran the mixer paths that would unmute `Master`, `Headphone` and `Speaker`. That report was about the headphone jack, but owners of the Zephyrus G14, G16, M16 and Flow X13 confirmed the same fix in the thread. The fix that report gives:

```bash
rm ~/.config/wireplumber/wireplumber.conf.d/alsa-soft-mixer.conf
systemctl --user restart wireplumber pipewire pipewire-pulse
```

If you would rather keep the soft mixer, unmute and raise the hardware control by hand instead:

```bash
card=$(aplay -l | grep -i ALC285 | head -1 | sed 's/card \([0-9]*\).*/\1/')
amixer -c "$card" set Master 100% unmute
sudo alsactl store
```

Omarchy's own script sets that control to 80 percent, which rdoupe measured as a 12.75 dB ceiling under the soft mixer in issue #11046.

**5. Framework Laptop 13 AMD: reset the card profile.** Omarchy's install script for this machine puts the card on `HiFi (Mic1, Mic2, Speaker)`, the profile that carries both microphones and the speakers. If `pactl list cards` shows a different active profile, put it back:

```bash
pactl list cards short
pactl set-card-profile <card-name> "HiFi (Mic1, Mic2, Speaker)"
```

**6. Dell XPS with CS35L56 amps: read the amp log before changing anything.**

```bash
journalctl -k -b | grep -i cs35l56
```

`FIRMWARE_MISSING`, `Calibration disabled due to missing firmware controls` and `Can't read tuning IDs` mean the amplifiers bound but never downloaded their tuning. On the XPS 13 DX13260 with SKU 0E53 this is an upstream kernel bug: the amps misread their speaker ID as 0, and `linux-firmware` only carries spkid1, spkid2 and spkid3 for that subsystem. Gundrak confirmed the root cause in issue #11320 and closed it as a duplicate of wizaj's #9687, which is tracked at kernel.org. Cirrus supplied a driver patch for `spi-cs42l43` that three owners on #9687 built as an out-of-tree module and confirmed, with the caveat that every kernel update reverts it until the module is rebuilt. Two things to know before you copy a recipe from those threads:

- wizaj retracted the symlink workaround that aliased spkid0 to spkid1. It made sound, but it applies protection parameters that were never validated for those drivers. Do not use it.
- The `dell-xps13-sidecar-amps` package, merged as omarchy-pkgs PR #150 alongside PR #7032, writes `options snd_soc_sof_sdw quirk=65536`. The same quirk value restored bass for jonnyace in #7427, but MBvisti's #10543 shows the package producing complete silence on another 0E53 unit. PR #7032 landed on the quattro branch on 2026-08-25, yet the hook is absent from the v4.0.0 through v4.0.4 release tags, so nothing installs the package for you.

The only reversible thing to try is routing playback back through the codec instead of the sidecar amps, which a1local reported as audible on #9687:

```bash
echo 'options snd_soc_sof_sdw quirk=0' | sudo tee /etc/modprobe.d/sof-sdw-quirk.conf
sudo limine-mkinitcpio && reboot
```

Use `sudo mkinitcpio -P` instead if `limine-mkinitcpio` is not present. That route gives you the tweeters only, with no bass and no amp firmware. Delete the file to undo it.

**7. Sinks exist, nothing links to them, and it started with a September update.** Issue #11350 opened as a kernel regression between 7.1.9 and 7.2.3 and was corrected in its own thread: with WirePlumber 0.5.17 every ALSA sink is created with zero ports, `wpctl get-volume @DEFAULT_AUDIO_SINK@` answers `'-1' is not a valid ID`, and raw ALSA playback with `speaker-test -D hw:1,2` still works. zygote55 traced it to the v4l2 `create-device` script stalling the event dispatcher whenever a rule disables a camera device, which the `intel-ipu7-camera` package Omarchy installs on Intel laptops does. The fix is merged upstream but Arch still ships 0.5.17-1. Two reporters restored audio by downgrading `wireplumber` and `libwireplumber` to 0.5.15-1 from the pacman cache or the Arch Linux Archive:

```bash
pacman -Qi wireplumber | grep Version
sudo pacman -U /var/cache/pacman/pkg/{wireplumber,libwireplumber}-0.5.15-1-x86_64.pkg.tar.zst
```

Add `IgnorePkg = wireplumber libwireplumber` to `/etc/pacman.conf` until a fixed release lands, then remove it. zygote55's comment on #11350 also has a one-line override of the script under `~/.local/share/wireplumber/scripts/` if you would rather not downgrade.

## Verify it worked

```bash
speaker-test -c 2 -t wav -l 1
wpctl status | head -30
journalctl -k -b | grep -ciE 'firmware_missing|sof_probe_work failed'
```

You want an audible left and right test tone, a real sink name in `wpctl status` rather than `Dummy Output`, and a zero from the last command. If a speaker tuning applies to your machine, `omarchy audio tuning status` should print an active host service and a present tuning sink.

## Why it happens

Three designs meet here. PipeWire and WirePlumber own routing. ALSA still owns the hardware mixer underneath, and Omarchy's soft-mixer config deliberately hides that layer from PipeWire, which is why a muted hardware switch looks like a working desktop. Modern laptop speakers then add a third layer: Cirrus, TI and similar smart amplifiers that refuse to make sound until they load a tuning blob keyed to the machine's subsystem ID. When the vendor never shipped the blob variant your unit asks for, no userspace setting can help.

On top of that, Quattro moved the audio UI. v4.0.0 replaced wiremix with the shell's own audio panel and added output switching that preserves playback. v4.0.0 also introduced per-laptop speaker tunings, which are PipeWire filter chains in front of the speaker sink, currently shipping only for the 2026 XPS 14 and XPS 16.

## If that did not work

Collect a report with `omarchy-debug` and search the tracker before filing. Cases with no clean fix yet:

- Lenovo Legion Pro 7 16IRX8H, where the TAS2781 amplifier binding changes with a codec SSID override, in issue #12086.
- MacBook9,1 and 10,1, where karlentwistle found in #12008 that the out-of-tree Cirrus driver is not enough on its own and the NVRAM startup chime has to be unmuted before firmware powers the speaker amp.
- The `linux-omarchy` kernel, which 4.0.4 installs on every x86 machine while leaving the previous kernel in place. No audio report has pinned a fault on it yet, and the one that tried, #11350, turned out to be WirePlumber. Booting the stock `linux` entry from the Limine menu rules it in or out in one reboot.

The Lenovo Yoga Pro 7 14IAH10 bass pin quirk already ships in `install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh`, so that model needs nothing from you.

## Related

- [/hardware/audio/](/hardware/audio/) for the wider audio picture
- [/hardware/dell-xps-13-2026/](/hardware/dell-xps-13-2026/) and [/hardware/asus-rog-zephyrus/](/hardware/asus-rog-zephyrus/)
- [/fix/bluetooth-stops-after-resume/](/fix/bluetooth-stops-after-resume/) if only your headset is silent
- [/releases/v4.0.4/](/releases/v4.0.4/) for what the kernel change in 4.0.4 covers
- Omarchy manual: [Troubleshooting](https://omarchy.org/manual/troubleshooting/)
