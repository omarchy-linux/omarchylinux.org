---
title: "Lenovo IdeaPad on Omarchy"
description: "Lenovo IdeaPad on Omarchy 4.0.4: modern Intel and AMD models install and run, MX150 models still abort the installer, and Omarchy ships no IdeaPad enablement."
answer: "Bronze. Recent Intel and AMD IdeaPads (2021 and newer) install and run, and the bugs their owners file are generic Omarchy bugs rather than dead hardware. Two classes fail hard: NVIDIA MX150 models still abort the installer in 4.0.4, and pre-2016 AMD models can lose the console entirely. Omarchy ships zero IdeaPad specific enablement."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
kind: model
vendor: "Lenovo"
model: "Lenovo IdeaPad (1, 3, 5, Pro, Gaming, and older Z series)"
dmi: ["82KU", "82VY", "82LM", "81FE", "80EC"]
year: "2014 to 2026"
cpu: "Intel Core i3 to i7 (Kaby Lake to Alder Lake), AMD Ryzen 5 and 7 (Lucienne, Cezanne, Renoir), AMD FX on the oldest models"
gpu: "Intel UHD, AMD Radeon integrated, optional NVIDIA MX150, GTX 1650 or RTX 3050"
rating: bronze
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: partial
  gpu: partial
  suspend: unknown
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: unknown
quirkScripts:
  - name: "bin/omarchy-hw-match"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    note: "The DMI matcher every model quirk uses. It greps product_name and product_family. No caller in the v4.0.4 tree passes an IdeaPad pattern."
  - name: "install/hardware/nvidia.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    note: "Installs nvidia-open-dkms on Turing and newer, nvidia-580xx-dkms on Maxwell, Pascal and Volta. The 580xx branch is what breaks MX150 installs."
  - name: "bin/omarchy-hw-nvidia-without-gsp"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-nvidia-without-gsp"
    note: "Classifies a GPU as pre-Turing by PCI device ID between 0x1340 and 0x1e00. The MX150 (GP108) lands here."
  - name: "install/hardware/fix-synaptic-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-synaptic-touchpad.sh"
    note: "Once aborted installs at modprobe psmouse. Made non-fatal in 4.0.1 by PR #7236. It never applied InterTouch to an installed machine."
  - name: "install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    note: "The only Lenovo directory script in the tree. It matches the DMI string \"Yoga Pro 7 14IAH10\" and never fires on an IdeaPad."
issueCount: 22
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [lenovo, ideapad, nvidia, laptop, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7947"
    title: "Issue #7947: nvidia.sh fails on Pascal GPUs (MX150): nvidia-580xx-dkms and lib32-nvidia-580xx-utils not found"
    kind: issue
    author: "gtech-pedrol"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8544"
    title: "Issue #8544: Installation fails on Lenovo Ideapad Z50-70 with black screen during boot"
    kind: issue
    author: "pigreco"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/7996"
    title: "Issue #7996: Installer hangs/fails on missing offline packages, local keyring sync, and synaptic touchpad script"
    kind: issue
    author: "kridaydave"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/pull/7236"
    title: "PR #7236: Stop a psmouse quirk from failing every install"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/8152"
    title: "Issue #8152: Hyprland not allowing login"
    kind: issue
    author: "kridaydave"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/9151"
    title: "Issue #9151: Screen tearing(or scroll going down and up) on both browsers(chromium and brave) after update"
    kind: issue
    author: "Linar46"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/2064"
    title: "Issue #2064: Omarchy do not recognize my fringerprint reader"
    kind: issue
    author: "oliverperboni"
    date: "2025-09-29"
  - url: "https://github.com/omacom/omarchy/issues/3458"
    title: "Issue #3458: Wi-fi applet is frozen"
    kind: issue
    author: "Randomovski"
    date: "2025-11-19"
  - url: "https://github.com/omacom/omarchy/issues/7257"
    title: "Issue #7257: Quickshell network panel shows WPA2-Enterprise connection as disconnected"
    kind: issue
    author: "emredurak01"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/7391"
    title: "Issue #7391: Chromium browser PiP video always falls outside viewport, does not respect video aspect ratio"
    kind: issue
    author: "freezzby"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/7276"
    title: "Issue #7276: Bar shows a checkered overlay after an interrupted bar-move gesture, omarchy-bar-move-ghost layer stays stuck open"
    kind: issue
    author: "edvaldo4d5"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/11664"
    title: "Issue #11664: Third-party service plugins report enabled: false despite being correctly configured and actually running"
    kind: issue
    author: "kibendar"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/5405"
    title: "Issue #5405: Lenovo notebooks trigger lid open event immediately after closing the lid"
    kind: issue
    author: "pkwagner"
    date: "2026-04-23"
  - url: "https://github.com/omacom/omarchy/pull/8672"
    title: "PR #8672: Add generic Snapdragon X support on aarch64"
    kind: pr
    author: "birkskyum"
    date: "2026-09-13"
credits:
  - name: "heliohsilva"
    url: "https://github.com/heliohsilva"
    for: "Diagnosed the Z50-75 black screen as a video output problem by asking the reporter to plug in an external monitor, which made the installer visible"
  - name: "gtech-pedrol"
    url: "https://github.com/gtech-pedrol"
    for: "Isolated the MX150 installer abort to the 580xx branch of nvidia.sh and published the exit 0 workaround"
  - name: "spencerflagg"
    url: "https://github.com/spencerflagg"
    for: "Narrowed the Chromium 152 scroll and tearing bug to the ANGLE Vulkan backend and found that --use-angle=egl fixes it without disabling hardware acceleration"
  - name: "suraj-9849"
    url: "https://github.com/suraj-9849"
    for: "Pointed out that Tab and Shift+Tab move focus in the Wi-Fi TUI, which unblocked the frozen applet report"
  - name: "pkwagner"
    url: "https://github.com/pkwagner"
    for: "Retracted the IdeaPad Pro 5 lid switch report after tracing the phantom lid open events to a keyd virtual keyboard on his own machine"
faq:
  - q: "Will Omarchy install on an IdeaPad with an NVIDIA MX150?"
    a: "Not without a workaround as of 4.0.4. nvidia.sh classifies the MX150 as pre-Turing and tries to install nvidia-580xx-dkms, which fails with target not found and aborts the install. Issue #7947 is still open. The reported workaround is to add exit 0 to the top of install/hardware/nvidia.sh and resume."
  - q: "Does Omarchy have any IdeaPad specific hardware fixes?"
    a: "No. Grepping the v4.0.4 tree for IdeaPad returns nothing. The only Lenovo directory script targets the DMI string Yoga Pro 7 14IAH10. Everything else an IdeaPad gets is generic: Intel or AMD graphics, thermald, lpmd, SOF firmware, NVIDIA."
  - q: "Can I run Omarchy on a Snapdragon X IdeaPad?"
    a: "Not from the public ISO, which is x86_64 only. PR #8672 added generic Snapdragon X support on aarch64 and merged on 13 September 2026, but no Qualcomm or Snapdragon code appears anywhere in the v4.0.4 tree and the 4.0.4 release notes do not mention it. Treat ARM IdeaPads as experimental, not as a machine you install on this week."
related: [lenovo-legion, lenovo-yoga, nvidia, hybrid-gpu, fingerprint]
draft: false
---

The IdeaPad is Lenovo's consumer line, which means it is not one machine. Twenty-two issues in the Omarchy tracker name an IdeaPad, spread across a 2015 AMD FX laptop, several Alder Lake and Ryzen thin-and-lights, and gaming models with discrete NVIDIA. Everything below was checked against the v4.0.4 source tree and against issues open on 16 September 2026.

## Verdict

Bronze. Not because IdeaPads are bad Linux machines, but because the line is wide and Omarchy does nothing for it.

The positive evidence is indirect but real. Owners of an IdeaPad 1 15IAU7, an IdeaPad 3 15ALC6, an IdeaPad 5 14ALC05 and an IdeaPad 5 with a Ryzen 5600H are all filing bug reports from a running Omarchy desktop. Those reports are about the Quickshell bar, plugin status, Chromium picture-in-picture and browser scrolling, not about dead Wi-Fi or a silent speaker. A machine that can file a bug about the top bar is a machine that booted.

The negative evidence is specific. One variant class cannot complete the installer at all, and Omarchy ships no IdeaPad enablement of any kind, so anything the machine needs beyond stock Arch is on you.

## What works

Modern Intel and AMD IdeaPads reach a usable desktop. The reporters above run Hyprland 0.56.2 on Omarchy 4.0.0 through 4.0.3, on both i915 Alder Lake graphics and AMD Radeon integrated graphics, on Btrfs over LUKS.

Wi-Fi hardware works on the models reported. The two Wi-Fi issues in this bucket are interface problems, not radio problems. In [#3458](https://github.com/omacom/omarchy/issues/3458) an IdeaPad Gaming 3 owner thought the Wi-Fi applet was frozen; suraj-9849 pointed out that Tab moves focus in the Impala TUI, and DHH confirmed the discoverability gap. That was 3.x. In [#7257](https://github.com/omacom/omarchy/issues/7257) an IdeaPad 5 on 4.0.0 connects to a WPA2-Enterprise network, but the Quickshell network panel shows it as disconnected. Both are software.

The fingerprint reader is at least detected. `omarchy-hw-fingerprint` lists Goodix vendor ID `27c6` among the vendors it treats as fingerprint hardware, so setup offers enrollment on IdeaPads that carry one.

## What breaks

**NVIDIA MX150 aborts the installer.** In [#7947](https://github.com/omacom/omarchy/issues/7947), still open, an IdeaPad 330-15IKB (machine type 81FE, i7-8550U, MX150) fails during the hardware phase. `omarchy-hw-nvidia-without-gsp` classifies the GP108 as pre-Turing, so `nvidia.sh` asks for `nvidia-580xx-dkms` and `lib32-nvidia-580xx-utils`, pacman answers `target not found`, and the whole install stops. The reporter saw it on 4.0 and on 3.8.x, and the same code is still in the v4.0.4 tree. His workaround was to add `exit 0` at the top of `/mnt/usr/share/omarchy/install/hardware/nvidia.sh` and resume with `omarchy-apply-system`. See [/fix/nvidia-drivers-omarchy-4/](/fix/nvidia-drivers-omarchy-4/).

**Pre-2016 AMD models can lose the console.** [#8544](https://github.com/omacom/omarchy/issues/8544) is an IdeaPad Z50-75 (machine type 80EC, AMD FX-7500 with Radeon R7) where the ISO boots, prints `No irq handler` lines, then goes black. heliohsilva asked the reporter to attach an external monitor; the installer had been running the whole time, and the reporter could finally read it on the external screen. The internal panel output is the casualty, and the same firmware is why F2 does not reach the BIOS on that machine. Related: [/fix/black-screen-after-login/](/fix/black-screen-after-login/).

**Hybrid NVIDIA models get the hybrid tax.** [#9151](https://github.com/omacom/omarchy/issues/9151), open, is an IdeaPad 5 with a Ryzen 5600H and an RTX 3050 where Chromium and Brave scroll up and down forever after an update. The reporter fixed it by disabling hardware acceleration. spencerflagg reproduced it on a different hybrid laptop, traced it to the Chromium 152 ANGLE Vulkan backend, and recommends `--use-angle=egl` instead, which keeps GPU compositing. See [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/) and [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/).

**Fingerprint enrollment can fail even when the reader is present.** In [#2064](https://github.com/omacom/omarchy/issues/2064), on 3.0.1, `lsusb` shows a Goodix `27c6:55b4`, but enrollment ends with `Impossible to enroll: GDBus.Error:net.reactivated.Fprint.Error.NoSuchDevice: No devices available`. Omarchy detecting a reader and libfprint supporting that exact chip are two different things. 4.0.3 lists a fingerprint reader improvement during setup by powderluv, but nothing in the tree confirms 55b4 specifically. See [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/) and [/hardware/fingerprint/](/hardware/fingerprint/).

**Installer bugs, mostly historical.** [#7996](https://github.com/omacom/omarchy/issues/7996) from an IdeaPad 3 collected several 4.0.0 installer failures, including `fix-synaptic-touchpad.sh` hanging at `modprobe psmouse`. [PR #7236](https://github.com/omacom/omarchy/pull/7236) made that script non-fatal and shipped in 4.0.1; the reporter confirmed the fix. The same owner's follow-up [#8152](https://github.com/omacom/omarchy/issues/8152) is a login loop, but it came from driving `omarchy-apply-system` by hand rather than using the installer, so do not read it as an IdeaPad fault. See [/fix/install-fails-or-stalls/](/fix/install-fails-or-stalls/) and [/fix/login-loop-or-password-not-accepted-sddm/](/fix/login-loop-or-password-not-accepted-sddm/).

One report you can ignore: [#5405](https://github.com/omacom/omarchy/issues/5405) looked like Lenovo laptops firing a phantom lid-open event, but pkwagner retracted it himself within the hour. The cause was his own keyd virtual keyboard, not the hardware.

## What Omarchy does for this model

Nothing specific. Grepping the v4.0.4 source tree for `IdeaPad` returns no matches in `bin/`, `install/hardware/`, `default/` or `migrations/`. The single script under `install/hardware/lenovo/` matches the DMI string `Yoga Pro 7 14IAH10` and will never fire on an IdeaPad. The speaker tuning framework in `default/audio/tunings/` currently ships one tuning, and it is for the Dell XPS.

What an IdeaPad does get is the generic pass in `install/hardware/all.sh`: Intel video acceleration, `thermald`, `lpmd`, SOF firmware and the IPU7 camera script on Intel models, `nvidia.sh` and `vulkan.sh` where a GPU matches, Bluetooth, the wireless regulatory domain, and the F-key and Synaptics scripts.

If you want to check what DMI strings your machine exposes, run `cat /sys/class/dmi/id/product_name /sys/class/dmi/id/product_family`. Lenovo puts a four character machine type in `product_name`: reporters here show `82KU`, `82VY`, `82LM`, `81FE` and `80EC`. `omarchy-hw-match` greps both fields, which is why a quirk aimed at IdeaPads would have to key on `product_family`.

## Variants

Prefer a 2021 or newer Intel or AMD IdeaPad with integrated graphics only. Every IdeaPad in the tracker that is running a working desktop is in that group.

Be careful with anything carrying an NVIDIA MX150 or another Maxwell, Pascal or Volta part. That is the one variant with a confirmed, currently unfixed installer abort.

Treat IdeaPad Gaming and IdeaPad 5 models with a GTX 1650 or RTX 3050 as hybrid laptops first and IdeaPads second. Read [/hardware/nvidia/](/hardware/nvidia/) before you buy.

Avoid pre-2016 AMD models such as the Z50-70 and Z50-75 unless you enjoy the work. They can install, but only after you solve a display problem that also blocks your own BIOS.

Snapdragon X IdeaPads are not covered by the public x86_64 ISO. Generic Snapdragon X support merged in [PR #8672](https://github.com/omacom/omarchy/pull/8672) on 13 September 2026, two days before 4.0.4, but none of it reached the shipped 4.0.4 tree. That is experimental, not a buying recommendation.

## Before you install

- Identify your GPU first. `lspci | grep -i nvidia`. If it returns an MX150 or similar, expect the installer to stop, and plan for the `exit 0` workaround.
- If the installer goes black on an older model, plug in an external monitor before you conclude it hung.
- Update the BIOS from Windows while you still can. The worst report here is on a machine whose firmware could not be reached at all, from a cold boot or from Windows advanced startup, which also blocked the update.
- Install from the current ISO, not a 4.0.0 one. Several installer bugs in this bucket were fixed in 4.0.1. See [/releases/v4.0.4/](/releases/v4.0.4/).
- Use the installer. Do not hand-run `omarchy-apply-system` unless you are recovering, which is how the login loop above happened.
- Test fingerprint, sleep and the webcam during your return window. Those subsystems are marked unknown on this page because nobody has reported them either way.

## Related

- [/hardware/lenovo-legion/](/hardware/lenovo-legion/) and [/hardware/lenovo-yoga/](/hardware/lenovo-yoga/) for the rest of the Lenovo consumer range
- [/hardware/nvidia/](/hardware/nvidia/) and [/fix/nvidia-drivers-omarchy-4/](/fix/nvidia-drivers-omarchy-4/)
- [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) and [/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [/hardware/amd-gpu/](/hardware/amd-gpu/) and [/hardware/intel-gpu/](/hardware/intel-gpu/)
- [/hardware/wifi/](/hardware/wifi/) and the manual chapter on [networking](https://omarchy.org/manual/networking/)
- [/hardware/submit/](/hardware/submit/) if you own an IdeaPad and can confirm or correct anything above
