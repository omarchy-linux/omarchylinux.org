---
title: "Lenovo Legion gaming laptops on Omarchy"
description: "Lenovo Legion 5, 7 and Pro on Omarchy 4.0.4: bronze. The generic NVIDIA path installs cleanly, but suspend, brightness and video decode keep failing."
answer: "Bronze. A Legion installs and runs, but it is a hybrid NVIDIA laptop with no Legion specific enablement in Omarchy 4.0.4. Expect to fight suspend: owners report no sleep on lid close on a 2020 unit and hard freezes after resume on both an RTX 4060 and an RTX 5080 machine. Brightness keys are dead on one 2026 model, and one Legion Pro 7 has silent internal speakers."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: partial
kind: model
vendor: "Lenovo"
model: "Legion 5, Legion 7, Legion Pro (and Y7000P)"
dmi: ["82JW", "82WQ", "83DG", "Legion 5 15ACH6", "Legion 5 15ARH05H", "Legion 5 15IAX10", "Legion 5 15IAX11", "Legion 7 16IRX9", "Legion Pro 7 16IRX8H", "Legion Y7000P IRX9"]
year: "2020 to 2026"
cpu: "AMD Ryzen 7 4800H and 5800H, Intel Core i7/i9 HX, Intel Core Ultra 7/9 HX (Arrow Lake)"
gpu: "Hybrid: AMD or Intel iGPU driving the internal panel plus NVIDIA GTX 1660 Ti to RTX 5080 Max-Q"
rating: bronze
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: unknown
quirkScripts:
  - name: "install/hardware/nvidia.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/nvidia.sh"
    note: "The only driver work a Legion gets. Installs nvidia-open-dkms on Turing and newer, nvidia-580xx-dkms below that, writes nvidia_drm modeset=1 and adds the NVIDIA modules to mkinitcpio."
  - name: "bin/omarchy-hw-nvidia-gsp"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-nvidia-gsp"
    note: "Picks the open driver when the PCI device id is 0x1e00 or higher. GTX 16 series and every RTX Legion clear that line; a GTX 10 series Y530 does not."
  - name: "default/hypr/nvidia.lua"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/hypr/nvidia.lua"
    note: "Sets NVD_BACKEND, LIBVA_DRIVER_NAME=nvidia and __GLX_VENDOR_LIBRARY_NAME=nvidia whenever the NVIDIA GPU has GSP firmware, without asking which GPU renders. This is the cause of the hybrid video corruption below."
  - name: "bin/omarchy-toggle-hybrid-gpu"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-toggle-hybrid-gpu"
    note: "Installs supergfxctl on demand and flips between Hybrid and Integrated. Its own summary names an Asus G14, but nothing in the script checks the vendor. No Legion report confirms it either way."
  - name: "bin/omarchy-hw-display"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-display"
    note: "Picks the backlight device from a fixed preference list: gmux, amdgpu_bl*, intel_backlight, acpi_video*. The nvidia_0 node that nvidia_wmi_ec_backlight registers on newer Legions is not in that list."
  - name: "bin/omarchy-hw-match"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-match"
    note: "The DMI matcher used by every model quirk. It checks product_name and product_family. No caller in the v4.0.4 tree passes a Legion pattern; the only Lenovo string any caller matches is Yoga Pro 7 14IAH10."
  - name: "install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/lenovo/fix-yoga-pro7-bass-speakers.sh"
    note: "The only Lenovo file in install/hardware on v4.0.4, and it matches the Yoga Pro 7 14IAH10, not any Legion."
issueCount: 22
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [lenovo, legion, nvidia, hybrid-gpu, gaming-laptop, suspend]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7988"
    title: "Issue #7988: Omarchy Quattro fails to boot/install on Lenovo Legion 5"
    kind: issue
    author: "damain"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/2501"
    title: "Issue #2501: Laptop does not suspend when the lid is closed"
    kind: issue
    author: "xElkomy"
    date: "2025-10-17"
  - url: "https://github.com/omacom/omarchy/issues/9765"
    title: "Issue #9765: Legion Pro 7 with RTX 5080 hard-freezes after resume from deep suspend"
    kind: issue
    author: "1977-eu"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/10626"
    title: "Issue #10626: Desktop becomes unresponsive after S3 resume: NVIDIA 610.57.04 modeset lock blocks Hyprland"
    kind: issue
    author: "chivopic"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/11665"
    title: "Issue #11665: Display brightness keys/OSD have no effect on Lenovo Legion 5 15IAX11 (nvidia_wmi_ec_backlight EC bug, upstream kernel #221430)"
    kind: issue
    author: "selenophilezh"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/12086"
    title: "Issue #12086: Internal speakers silent on Legion Pro 7 16IRX8H; TAS2781 binding changes with codec SSID override"
    kind: issue
    author: "slavkof"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9890"
    title: "Issue #9890: hypr/nvidia.lua: LIBVA_DRIVER_NAME=nvidia corrupts hardware video decode on hybrid laptops where the compositor renders on the iGPU"
    kind: issue
    author: "andrea-bavetta"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/8989"
    title: "Issue #8989: Hybrid iGPU-primary laptops: nvidia.lua forces NVIDIA env session-wide, video corruption (root cause of #4901) and blocked dGPU runtime suspend"
    kind: issue
    author: "karluiz"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/11943"
    title: "Issue #11943: Hardware cursor intermittently stops rendering on hybrid Intel/NVIDIA multi-monitor laptop (recurs despite no_hardware_cursors=true)"
    kind: issue
    author: "Cousint98"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/1286"
    title: "Issue #1286: AFter install of omarchy iso on Lenovo Legion"
    kind: issue
    author: "ramlev"
    date: "2025-08-29"
  - url: "https://github.com/omacom/omarchy/issues/10621"
    title: "Issue #10621: omarchy toggle bar on/off arguments are inverted (filed from a Legion Y530-15ICH with a GTX 1060 on the 580xx driver)"
    kind: issue
    author: "macbe"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/all.sh"
    title: "install/hardware/all.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-display"
    title: "bin/omarchy-hw-display at v4.0.4"
    kind: commit
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy Manual: System sleep"
    kind: manual
credits:
  - name: "selenophilezh"
    url: "https://github.com/selenophilezh"
    for: "Traced dead brightness keys on the Legion 5 15IAX11 through evdev, Hyprland and brightnessctl to an EC firmware bug, and showed omarchy-hw-display has no nvidia_wmi_ec case"
  - name: "karluiz"
    url: "https://github.com/karluiz"
    for: "Showed on a Legion 7i Pro that nvidia.lua exports NVIDIA VA-API and GLX variables session wide even when the iGPU drives the panel"
  - name: "andrea-bavetta"
    url: "https://github.com/andrea-bavetta"
    for: "Reproduced the same LIBVA_DRIVER_NAME problem on a Legion 5 15IAX10 and tied it to Chromium video corruption"
  - name: "perogycook"
    url: "https://github.com/perogycook"
    for: "Found that mem_sleep_default=deep restored lid suspend on their machine in the long running Legion lid thread"
  - name: "damain"
    url: "https://github.com/damain"
    for: "Narrowed a stuck Quattro installer on a Legion 5 15ACH6 to the USB stick disappearing mid boot rather than a bad image"
  - name: "slavkof"
    url: "https://github.com/slavkof"
    for: "Documented the silent TAS2781 speaker amp on the Legion Pro 7 16IRX8H, including the codec SSID override that makes it bind"
faq:
  - q: "Is a Lenovo Legion a good machine for Omarchy?"
    a: "It is workable, not carefree. Nothing in Omarchy 4.0.4 targets a Legion, so you get the generic NVIDIA path and nothing else. The recurring complaints are suspend and resume, brightness control on at least one 2026 model, and hybrid graphics environment variables that hurt video playback."
  - q: "My Legion does not suspend when I close the lid. What do I try?"
    a: "Two things owners reported helping in issue #2501: switch the power profile away from performance, and add mem_sleep_default=deep to the kernel cmdline. Neither worked for everybody, and the original reporter was still stuck after trying the logind.conf settings."
  - q: "Which Legion generation is safest?"
    a: "The tracker does not name one. Lid close suspend fails on a 2020 Ryzen unit with a GTX 1660 Ti, and resume from deep sleep freezes on both an RTX 4060 Y7000P and an RTX 5080 Legion Pro 7. The 2026 Arrow Lake machines simply have the most open reports. Very old Pascal Legions such as the Y530 fall back to the nvidia-580xx legacy driver."
  - q: "Does the Legion Go count as a Legion here?"
    a: "No. The handheld is a different platform with an AMD APU and no NVIDIA GPU, and none of the issues on this page apply to it."
related: [nvidia, hybrid-gpu, suspend-sleep, audio, multi-monitor, asus-rog-zephyrus]
draft: false
---

## Verdict

Bronze. A Legion installs and runs Omarchy, and the GPU side is no worse than any other NVIDIA Optimus laptop. The tracker is still unflattering: 22 issues mention a Legion and 18 of them are open. About half are generic Omarchy bugs that happen to have been filed from a Legion, but the ones that are really about the hardware cluster on suspend, display and hybrid graphics. Omarchy 4.0.4 ships no Legion specific enablement at all. There is no Legion entry in `install/hardware`, and no caller of `bin/omarchy-hw-match` passes a Legion pattern. The only Lenovo model any caller matches is the Yoga Pro 7 14IAH10. What you get is the generic NVIDIA install script plus whatever your iGPU vendor gets.

An earlier hand written prototype of this site rated the Legion silver on the strength of one working dual monitor setup. The issue tracker since Quattro does not support that. Checked against v4.0.4, with v3.8.4 as the last 3.x reference.

## What works

The install path itself is normal. `install/hardware/nvidia.sh` sees the NVIDIA GPU, installs `nvidia-open-dkms` and `nvidia-utils` on Turing and newer, writes `options nvidia_drm modeset=1` and adds the four NVIDIA modules to the initramfs. Every RTX Legion and the GTX 16 series units take that path, because `omarchy-hw-nvidia-gsp` keys on a PCI device id of 0x1e00 or higher.

The hybrid GPU toggle is at least offered to you. `omarchy-toggle-hybrid-gpu` installs `supergfxctl` on first use, writes `/etc/supergfxd.conf` and flips between Hybrid and Integrated with a reboot. It is usually described as an Asus feature, and the script's own summary names an Asus G14, but nothing in it checks the vendor and `omarchy-hw-hybrid-gpu` falls back to counting display class PCI devices when supergfxd cannot answer. Whether supergfxd actually drives a Legion is not something any report in the tracker settles. See [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) for what that costs you.

Multiple monitor setups are in use. The reporter in issue #11943 runs a Legion 7 16IRX9 with the internal panel plus three external displays, and the complaint is a cursor rendering glitch, not a failure to light the outputs.

Nobody has filed a Legion specific Wi-Fi, Bluetooth, webcam, fingerprint or touchpad failure that we could find in this data set. That is weak evidence of health rather than proof, which is why those rows are marked unknown above.

## What breaks

**Suspend, repeatedly.** This is the headline problem. Issue #2501, open since October 2025, is a Legion 5 15ARH05H that never suspends on lid close even after uncommenting the `HandleLidSwitch` settings in `logind.conf`. Other owners piled on, including a second Legion 5 owner who said no Linux distribution would suspend on that machine. One commenter got their own machine working by adding `mem_sleep_default=deep`; another traced their case to the performance power profile. Neither is confirmed on the original reporter's hardware. On newer hardware it fails in the other direction: issue #9765 is a Legion Pro 7 with a Core Ultra 9 275HX and an RTX 5080 Max-Q that resumes from ACPI S3 into a frozen session, with `spd5118_resume` returning an error and the shell reporting no outputs. Issue #10626 is a Legion Y7000P IRX9 with an RTX 4060 whose journal has Hyprland stuck in an NVIDIA modeset lock for four minutes past the point where the kernel had already finished its resume. Both run driver 610.57.04. Start at [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/) and the [System sleep](https://omarchy.org/manual/system-sleep/) manual chapter.

**Brightness keys on a 2026 model.** Issue #11665 traces dead brightness keys on a Legion 5 15IAX11 all the way down. The key emits the right event, Hyprland dispatches it, `brightnessctl` writes and reads back both `intel_backlight` and `nvidia_0`, and the panel ignores all of it. The cause is an EC firmware bug behind `nvidia_wmi_ec_backlight`, reported upstream as kernel bugzilla 221430. No compositor level fix exists. The reporter also notes that `nvidia_0` is absent from `omarchy-hw-display`'s preference list, which the v4.0.4 script confirms, so the picker lands on `intel_backlight` on this machine.

**Hybrid video decode.** `default/hypr/nvidia.lua` exports `LIBVA_DRIVER_NAME=nvidia` and `__GLX_VENDOR_LIBRARY_NAME=nvidia` on any machine whose NVIDIA GPU has GSP firmware, which is every Legion from the GTX 16 series up, and `autostart.lua` pushes that environment into the whole session. On a Legion where the Intel or AMD iGPU drives the panel, every VA-API client then decodes on the wrong device. Two Legion owners filed it: issue #8989 from a Legion 7i Pro and issue #9890 from a Legion 5 15IAX10, which reports corrupted video on live streams and one Chromium GPU process abort. The validated workaround is the one in #8989: set `LIBVA_DRIVER_NAME` back to `iHD`, or `radeonsi` on an AMD iGPU, and `__GLX_VENDOR_LIBRARY_NAME` to `mesa` in `~/.config/hypr/hyprland.lua`, below the `require("default.hypr.omarchy")` line. Put them above that line and Omarchy silently wins. See [/hardware/nvidia/](/hardware/nvidia/).

**Audio on at least one model.** Issue #12086, filed on 4.0.4 with the bundled `linux-omarchy` kernel, has silent internal speakers on a Legion Pro 7 16IRX8H. The TAS2781 amplifier loads and binds its I2C device, but the ALC287 codec does not bind the amplifier component on a normal boot. Reloading `snd_hda_intel` with a codec SSID override makes it bind. The reporter is explicit that this is a diagnostic override, not a confirmed fix, and that it is unproven whether the defect is Omarchy's or upstream's. One machine, and the report landed on the day this page was checked. More at [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/).

**Installer media on some units.** Issue #7988 is a Legion 5 15ACH6 that hangs on the Omarchy logo with the Quattro installer. Two ISO downloads, Secure Boot off, and a BIOS switch to discrete graphics all failed. Removing the quiet boot options dropped the reporter to a root shell where the USB stick was simply gone from `lsblk` until it was replugged, which points at USB enumeration rather than the image. Older but worth knowing: issue #1286 from 2025 is a Legion that would not reach the boot menu after an Omarchy 2.0 install, and other Lenovo owners in that thread had to unplug the NVMe drive or reset the BIOS to recover. See [/fix/install-fails-or-stalls/](/fix/install-fails-or-stalls/).

**Cursor glitches on multi head hybrid setups.** Issue #11943, Legion 7 16IRX9 with four outputs, has the cursor going invisible or trailing even with `no_hardware_cursors = true` set in `looknfeel.lua`. Setting the cursor again with `hyprctl setcursor` fixes it until it recurs. See [/fix/cursor-invisible-or-wrong-size/](/fix/cursor-invisible-or-wrong-size/).

## What Omarchy does for this model

Nothing by name. To be concrete about what runs on your Legion during install: `install/hardware/all.sh` calls the Asus, Framework 16, Dell XPS touchpad, Surface, Apple and Yoga Pro 7 scripts, none of which match a Legion, plus the generic network, wireless regdom, f-key, touchpad, Bluetooth, NVIDIA and Vulkan scripts, plus the Intel set if you have an Intel CPU. The speaker tuning framework in `omarchy-audio-tuning` only ships one profile, `dell-xps-2026`, and it matches on the Dell DMI SKU. No Legion tuning exists.

DMI values people reported in these issues are the Lenovo type codes `82JW` (Legion 5 15ACH6), `82WQ` (Legion Pro 7 16IRX8H) and `83DG` (Legion Y7000P IRX9). Reporters give the type code and the marketing name together, but no full DMI dump from a Legion appears in these threads, so which field carries which string is not settled here. `omarchy-hw-match` reads only `product_name` and `product_family`, so a future Legion quirk has to match whichever of those two holds the model string on your unit.

## Variants

No generation comes out of this tracker clean, so choose on which failure you can live with rather than on a safe year.

The Arrow Lake HX machines carry the newest reports: the hybrid decode problem on a Legion 5 15IAX10 with an RTX 5070 Max-Q and on a Legion 7i Pro with an RTX 5080, and one frozen resume on a Legion Pro 7 with an RTX 5080. The Legion 5 15IAX11 sits in the same recent wave, and it is the one where brightness control is dead, though its report names neither the CPU nor the dGPU.

The 13th and 14th generation HX units with RTX 40 graphics are not a safe harbour either. The other frozen resume is a Y7000P IRX9 with an RTX 4060, the silent speakers are a Legion Pro 7 16IRX8H with an RTX 4080, and the cursor glitch is a Legion 7 16IRX9, also on an RTX 4060.

The 2020 and 2021 AMD units are quieter about graphics and louder about basics: the lid suspend thread starts on a Ryzen 4800H Legion 5 15ARH05H with a GTX 1660 Ti, and the installer hang is a Ryzen 5800H 15ACH6 with an RTX 3050 Ti.

Very old Legions such as the Y530 with Pascal graphics drop below the GSP cutoff and get `nvidia-580xx-dkms` instead of the open driver. Issue #10621, filed about an unrelated bar toggle bug, shows exactly that machine: a Y530-15ICH with a GTX 1060 running driver 580.178.04. That works but is a legacy branch.

The Legion Go handheld is not covered here. It is an AMD APU device with no discrete NVIDIA GPU; see [/hardware/steam-deck-and-handhelds/](/hardware/steam-deck-and-handhelds/).

## Before you install

- Do not assume your generation is exempt. The two frozen resume reports are an RTX 5080 and an RTX 4060, and the oldest suspend thread is a GTX 1660 Ti.
- In BIOS, decide on hybrid versus discrete before installing, and leave Secure Boot off.
- Write the ISO to a USB port you trust, and if the installer hangs on the logo, drop the quiet boot options first and check whether the stick is still enumerated.
- Test suspend on day one from the Omarchy menu and from a lid close, separately. They fail independently on this family.
- If video looks corrupted in Chromium or Electron apps, override `LIBVA_DRIVER_NAME` in `~/.config/hypr/hyprland.lua`, below the Omarchy require, before assuming your GPU is broken.
- If brightness keys do nothing, check `ls /sys/class/backlight` for an `nvidia_0` entry. If it is there and writes do nothing, that is the EC bug and you are waiting on the kernel.

## Related

- [/hardware/nvidia/](/hardware/nvidia/)
- [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/)
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/)
- [/fix/nvidia-drivers-omarchy-4/](/fix/nvidia-drivers-omarchy-4/)
- [/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [/hardware/asus-rog-zephyrus/](/hardware/asus-rog-zephyrus/)
