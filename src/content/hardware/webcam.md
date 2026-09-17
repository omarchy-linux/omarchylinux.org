---
title: "Webcams on Omarchy"
description: "USB webcams work on Omarchy 4.0.4. Built-in MIPI cameras behind Intel IPU6 or IPU7 are the hard part: what Omarchy installs, what breaks, and the fix order."
answer: "USB and UVC webcams work out of the box on Omarchy 4.0.4. Built-in MIPI cameras are where it goes wrong. Omarchy installs intel-ipu7-camera only when the ACPI id OVTI08F4 is present, so IPU6 laptops get nothing at all. Check the HAL plugin with ldd first, then the sensor's ACPI status, then the kernel bind lines in dmesg."
appliesTo:
  from: "4.0.0"
kind: component
componentKey: "webcam"
status: info
issueCount: 36
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [webcam, camera, intel-ipu7, libcamera, v4l2]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/intel/ipu7-camera.sh"
    title: "install/hardware/intel/ipu7-camera.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-capture-webcam-list"
    title: "bin/omarchy-capture-webcam-list at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/10837"
    title: "Issue #10837: RC jsoncpp 1.9.8 soname bump breaks intel-ipu7-camera 1.0.5"
    kind: issue
    author: "klaudworks"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10948"
    title: "Issue #10948: [Regression] linux-ptl 7.2.3: IPU7 / OV08X40 sensor missing from media graph on Dell XPS 14 DA14260"
    kind: issue
    author: "milep"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/12178"
    title: "Issue #12178: Lunar Lake: intel-ipu7-camera is installed by detection but built for Panther Lake only"
    kind: issue
    author: "pkolbas"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9879"
    title: "Issue #9879: IPU6 MIPI cameras (ov01a10 / OVTI01A0) get no setup"
    kind: issue
    author: "extragloves"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/7697"
    title: "Issue #7697: ipu7-camera.sh misdetects Meteor Lake (IPU6) hardware as IPU7, breaking the webcam"
    kind: issue
    author: "mhbnielsen"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/6000"
    title: "Issue #6000: Camera (IPU7-PTL / OV08X40) on ThinkPad X1 Carbon Gen 14: ACPI status=0, sensor invisible to Linux"
    kind: issue
    author: "ocewers"
    date: "2026-05-30"
  - url: "https://github.com/omacom/omarchy/issues/8641"
    title: "Issue #8641: XPS 14 (Panther Lake): Windows Hello IR camera (Himax HM1092) has no Linux driver"
    kind: issue
    author: "jorgemanrubia"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/10624"
    title: "Issue #10624: IPU7 camera: ov08x40 sensor bind is lost on suspend/resume and camera-init can't restore it"
    kind: issue
    author: "suhaskashyaps"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/8843"
    title: "Issue #8843: Browser cannot access built-in camera even when libcamera, pipewire-libcamera, and qcam all work"
    kind: issue
    author: "loganwoolf"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/11850"
    title: "Issue #11850: screenrecording --with-webcam: overlay mpv is orphaned when the camera never delivers a frame"
    kind: issue
    author: "jasrys"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11373"
    title: "Issue #11373: No driver path for the pre-T2 FaceTime HD camera (Broadcom 1570)"
    kind: issue
    author: "rand0mdud3"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy-pkgs/pull/418"
    title: "omarchy-pkgs #418: Fix Intel IPU7 camera on Linux 7.2 by adopting the CVS V4L2 bridge"
    kind: pr
    author: "spencerbull"
    date: "2026-09-13"
  - url: "https://omarchy.org/manual/screenshots-recording/"
    title: "Omarchy manual: Screenshots & Recording"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "disy-mk"
    url: "https://github.com/disy-mk"
    for: "The one-line ldd check that identifies the jsoncpp soname break without camera hardware"
  - name: "labjt"
    url: "https://github.com/labjt"
    for: "Binary diff of ipu-bridge.ko showing the CVS ACPI ids added in kernel 7.2"
  - name: "nathankramm"
    url: "https://github.com/nathankramm"
    for: "Tracing the broken camera to the package rebuild rather than the kernel upgrade"
  - name: "spencerbull"
    url: "https://github.com/spencerbull"
    for: "The CVS V4L2 bridge fix that shipped in 4.0.4"
faq:
  - q: "Do USB webcams work on Omarchy?"
    a: "Yes. They bind to uvcvideo like on any Arch system and show up as a real /dev/video node. Nothing in Omarchy touches them."
  - q: "Why does my laptop camera show a black picture instead of nothing at all?"
    a: "Because the Intel relay stack created a v4l2loopback node (usually /dev/video50) that no sensor is feeding. The node exists, so apps list a camera, but every frame is black."
  - q: "Does Omarchy install libcamera for me?"
    a: "No. As of 4.0.4 the only automatic camera work is installing intel-ipu7-camera when the ACPI id OVTI08F4 is present. There is no libcamera or IPU6 install path."
related: [webcam-not-detected, suspend-wont-resume-s2idle, t2-mac, dell-xps-14-2026, lenovo-thinkpad-x1-carbon]
draft: false
---

## Status on 4.0.4

Split webcams into two groups and the picture gets clear fast.

USB and UVC cameras are fine. They bind to `uvcvideo`, they get a real `/dev/video` node, and Chromium, OBS and the screen recorder all find them. Omarchy does nothing special for them and nothing special is needed.

Built-in MIPI cameras on recent Intel laptops are the problem. These sit behind an Intel Image Processing Unit (IPU6 or IPU7) and need a kernel bridge, a sensor driver, a proprietary camera HAL, and a relay daemon that fakes a normal `/dev/video` node so browsers can read it. Any one of those four can be missing or mismatched, and on Omarchy several of them regularly are. The component tracker counts 36 issues here, 25 of them still open, and the bulk are Intel MIPI cameras.

Apple hardware is a third case. T2 Macs get their camera through `linux-t2` and `uvcvideo`, pre-T2 Macs with the Broadcom 1570 FaceTime HD part get nothing at all (#11373). See [T2 Macs](/hardware/t2-mac/) and [Apple Silicon](/hardware/apple-silicon-asahi/).

Checked against the v4.0.4 source tree. On 3.x the same `ipu7-camera.sh` detection existed, so the shape of the problem has not changed across Quattro.

## What Omarchy does automatically

Less than you would guess. The entire automatic camera setup in v4.0.4 is `install/hardware/intel/ipu7-camera.sh`, run from `install/hardware/all.sh`:

```sh
if grep -q "OVTI08F4" /sys/bus/acpi/devices/*/hid 2>/dev/null; then
  omarchy-pkg-add intel-ipu7-camera
fi
```

That is it. One ACPI id, one package. `intel-ipu7-camera` also sits in `install/omarchy-other.packages` so the ISO carries it. The package itself brings the DKMS modules (`ipu7-drivers`, `vision-drivers`), the CamHAL plugin `/usr/lib/libcamhal/plugins/ipu75xa.so`, `camera-init.service`, `v4l2-relayd@ipu7.service`, a v4l2loopback node that usually lands at `/dev/video50`, and a `systemd` system-sleep hook that restarts the camera on resume.

There is no libcamera install path, no `pipewire-libcamera`, and no IPU6 leaf.

The rest of the webcam surface is capture tooling, not enablement:

- `omarchy-hw-webcam` returns true when `omarchy-capture-webcam-list` prints anything. The menu entry for recording with a webcam is gated on it, so if you have no camera the option simply does not appear.
- `omarchy-capture-webcam-list` runs `v4l2-ctl --list-devices` and keeps only nodes whose Device Caps advertise Video Capture. This is what stops IPU laptops offering their raw Bayer `/dev/video0` as a camera (#5722, shipped in 4.0.0).
- `omarchy-capture-screenrecording-with-webcam` picks the device, then hands off to the recorder.
- The overlay is an `mpv` window titled `WebcamOverlay`, positioned by rules in `default/hypr/apps/webcam-overlay.lua` and resized with `Super + Alt + [` and `]`. The manual covers it in [Screenshots & Recording](https://omarchy.org/manual/screenshots-recording/).

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#10948](https://github.com/omacom/omarchy/issues/10948) kernel 7.2.3 routes the sensor through a CVS node with no in-tree driver, so `ov08x40` never reaches the media graph | Dell XPS 14 DA14260, XPS 16 DA16260 | closed | 4.0.4 |
| [#10837](https://github.com/omacom/omarchy/issues/10837) jsoncpp 1.9.8 soname bump leaves `ipu75xa.so` unable to load | any IPU7 laptop | open, package rebuilt | `intel-ipu7-camera` 1.0.5-2 and later |
| [#12178](https://github.com/omacom/omarchy/issues/12178) package is installed by detection but built for Panther Lake only, so the `ipu7x` plugin Lunar Lake needs does not exist | Dell Pro 13/14 Premium, XPS 13 9350, other Core Ultra 200V | open | not yet |
| [#9879](https://github.com/omacom/omarchy/issues/9879) IPU6 machines get no camera setup at all | Dell XPS 13 Plus 9315, Alder/Raptor/Meteor Lake laptops | open | not yet |
| [#7697](https://github.com/omacom/omarchy/issues/7697) the OVTI08F4 test also matches Meteor Lake IPU6 boards, installing the wrong HAL | HP Spectre x360 14 (Core Ultra 7 155H) | open | not yet |
| [#5676](https://github.com/omacom/omarchy/issues/5676) IPU6 needs AUR packages and a forced libcamera pipeline | Tiger Lake, Alder Lake, Raptor Lake | open | not yet |
| [#6000](https://github.com/omacom/omarchy/issues/6000) sensor ACPI `_STA` reads 0, so it never binds | Lenovo ThinkPad X1 Carbon Gen 14 | open | not yet |
| [#7776](https://github.com/omacom/omarchy/issues/7776) same `_STA` 0 signature plus "IPU7 in secure mode" | Lenovo X1 Aura 14 / X1 Carbon Gen 14 | open | not yet |
| [#8641](https://github.com/omacom/omarchy/issues/8641) Windows Hello IR sensor (Himax HM1092) has no Linux driver anywhere | Dell XPS 14 DA14260 | open | not yet |
| [#10624](https://github.com/omacom/omarchy/issues/10624) sensor bind is lost on resume and `camera-init` cannot restore it | Dell XPS 16 DA16260 | open | not yet |
| [#6222](https://github.com/omacom/omarchy/issues/6222) sleep hook uses a fixed transient unit name, so suspend-then-hibernate skips the resume restart | IPU7 laptops | open | not yet |
| [#8843](https://github.com/omacom/omarchy/issues/8843) libcamera and `qcam` see the camera, Chromium never does | Microsoft Surface Pro | open | not yet |
| [#11850](https://github.com/omacom/omarchy/issues/11850) recording overlay is orphaned when the camera opens but sends no frames, and holds the device open | any machine whose camera opens without streaming | open | not yet |
| [#11373](https://github.com/omacom/omarchy/issues/11373) no driver path for the pre-T2 Broadcom 1570 FaceTime HD camera | MacBook Pro 2013 to 2015 | open | not yet |
| [#3883](https://github.com/omacom/omarchy/issues/3883) built-in webcam not detected alongside keyboard and resume problems | MacBook Pro 13-inch 2020 (T2) | open | not yet |

Two closures worth knowing about. #5722, the raw Bayer node in the picker, was fixed in 4.0.0. #6233, a dead camera on an Acer Nitro, was closed by DHH as out of Omarchy's reach because the same camera failed on Ubuntu too. That is the general rule: if it does not work on any distro, it is a kernel or vendor gap and Omarchy cannot patch around it.

## Fixes that work

Work through this in order. Most people stop at step three.

1. Confirm what you actually have. `omarchy-capture-webcam-list` prints only real capture devices. If it lists nothing, the camera never reached userspace. If it lists a node and the picture is still black, the node is a relay with nothing feeding it.
2. Identify the IPU generation, not the sensor. `lspci | grep -i multimedia` and `lsmod | grep intel_ipu`. If `intel_ipu6` is bound but `intel-ipu7-camera` is installed, you are in #7697 and the installed HAL is for the wrong chip.
3. Check the HAL plugin for a missing library. `ldd /usr/lib/libcamhal/plugins/ipu75xa.so | grep -i json`. If it says `libjsoncpp.so.26 => not found` you have #10837, and the fix is `intel-ipu7-camera` 1.0.5-2 or newer. disy-mk pointed out this reproduces with no camera hardware at all, and nathankramm's faster version is `gst-inspect-1.0 icamerasrc 2>&1 | grep 'CamHAL\[ERR\]'`, which names the missing library in about a second. Do this before blaming a kernel upgrade, because on those XPS machines the kernel took the blame for three days.
4. If you are on kernel 7.2.x with a Panther Lake XPS, update to 4.0.4. The CVS bridge fix landed via omarchy-pkgs #418 and [4.0.4](/releases/v4.0.4/) lists it as "Fix webcam issues on XPS systems in the 7.2.x kernel".
5. Check whether firmware ever enabled the sensor: `cat /sys/bus/acpi/devices/OVTI08F4:00/status`. A `0` means the device is disabled at ACPI level, and no userspace change will help. That is the ThinkPad X1 Carbon Gen 14 wall in #6000 and #7776. Try a BIOS update, then wait.
6. Look for the bind in the kernel log: `journalctl -k -b | grep -i 'bind ov08x40'`. Seeing `All sensor registration completed` means the kernel half is healthy and the problem is in the HAL or the relay. Not seeing it after a resume is #10624, and today a reboot is the only reliable recovery.
7. Browser sees nothing while `qcam` works. Browsers read `/dev/video` nodes, so a working libcamera and PipeWire path is not enough on its own. That is #8843, still open.
8. A frozen black overlay left after a recording is #11850. `pkill -9 mpv` removes it and releases the device.

If your camera is IPU6, there is currently no supported path in Omarchy. Both #9879 and #5676 contain working community recipes, but they are AUR packages and user units you install yourself.

## Report it

Camera reports need more than the usual dump, because the failure can sit in any of four layers. Run `omarchy debug --no-sudo --print` for the system section, then add:

- The IPU PCI id from `lspci -nn | grep -i multimedia` and which of `intel_ipu6` or `intel_ipu7` is bound.
- Sensor ACPI id and status, for example `cat /sys/bus/acpi/devices/OVTI08F4:00/status`.
- `journalctl -k -b | grep -iE 'ov08x40|ipu|cvs'`, including whether the bind line appears.
- `media-ctl -p /dev/media0` showing whether a sensor entity exists.
- `ldd` output for the HAL plugin, plus the exact versions of `intel-ipu7-camera`, `jsoncpp` and your kernel.

Search the tracker for your sensor id before filing, since most of these threads already have your machine in them. Then add your model to [hardware submissions](/hardware/submit/). Details on `omarchy debug` are in [the command reference](/reference/commands/omarchy-debug/).

## Related

- [Webcam not detected](/fix/webcam-not-detected/)
- [Suspend will not resume](/fix/suspend-wont-resume-s2idle/) and [suspend and sleep](/hardware/suspend-sleep/)
- [Dell XPS 14 (2026)](/hardware/dell-xps-14-2026/), [ThinkPad X1 Carbon](/hardware/lenovo-thinkpad-x1-carbon/), [Microsoft Surface](/hardware/microsoft-surface/)
- [T2 Macs](/hardware/t2-mac/) and [Intel MacBook Pro](/hardware/apple-macbook-pro-intel/)
- [Release 4.0.4](/releases/v4.0.4/) and [what is still broken](/releases/still-broken/)
