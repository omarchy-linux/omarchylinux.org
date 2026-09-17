---
title: "Webcam not detected on Omarchy"
description: "Why the built-in webcam is missing on Omarchy 4, split by platform: Intel IPU7 on Panther Lake, Lunar Lake, IPU6 laptops, ThinkPad IMX471, and Macs."
answer: "Find out which camera you have first. On a Panther Lake Dell XPS, update to 4.0.4 and reboot: it ships the rebuilt intel-ipu7-camera with the in-tree CVS bridge driver. On Lunar Lake, IPU6, ThinkPad X1 Carbon Gen 14 and pre-T2 Macs, Omarchy ships no working path yet, and the fix is a community DKMS stack or removing the package that serves black frames."
appliesTo:
  from: "3.x"
status: workaround
fixedIn: "4.0.4"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: input
issueCount: 26
errorStrings:
  - "CamHAL[ERR] HalAdaptor: load_camera_hal_library, failed to open library"
  - "libjsoncpp.so.26: cannot open shared object file: No such file or directory"
  - "CameraParserInvoker: parseSensors: No sensors available"
  - "gst_element_set_state: assertion 'GST_IS_ELEMENT (element)' failed"
  - "zsh: no matches found: /dev/video*"
  - "Camera might be blocked."
tags: [webcam, camera, ipu7, ipu6, intel, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10948"
    title: "Issue #10948: [Regression] linux-ptl 7.2.3: IPU7 / OV08X40 sensor missing from media graph on Dell XPS 14 DA14260"
    kind: issue
    author: "milep"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy-pkgs/pull/418"
    title: "PR #418: Fix Intel IPU7 camera on Linux 7.2 by adopting the CVS V4L2 bridge"
    kind: pr
    author: "spencerbull"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/10837"
    title: "Issue #10837: RC jsoncpp 1.9.8 soname bump breaks intel-ipu7-camera 1.0.5"
    kind: issue
    author: "iuliansafta"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11358"
    title: "Issue #11358: IPU7 camera HAL requires missing libjsoncpp.so.26 on current Arch"
    kind: issue
    author: "jamielmccormick"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/12178"
    title: "Issue #12178: Lunar Lake: intel-ipu7-camera is installed by detection but built for Panther Lake only"
    kind: issue
    author: "pkolbas"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/9879"
    title: "Issue #9879: IPU6 MIPI cameras (ov01a10 / OVTI01A0) get no setup, hardware detection only covers IPU7"
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
  - url: "https://github.com/omacom/omarchy/issues/7776"
    title: "Issue #7776: Built-in camera does not work on a fresh Omarchy install."
    kind: issue
    author: "skovuri41"
    date: "2026-08-22"
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
  - url: "https://github.com/omacom/omarchy/issues/7277"
    title: "Issue #7277: webcam picker: Device Caps filter still passes IPU7 raw Bayer node"
    kind: issue
    author: "danteRub"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/5676"
    title: "Issue #5676: Intel IPU6 MIPI camera Raptor Lake not working"
    kind: issue
    author: "vitorpacheco"
    date: "2026-05-08"
  - url: "https://github.com/omacom/omarchy/issues/8271"
    title: "Issue #8271: Installer erases T1/T2 firmware on Apple hardware, permanently disabling Touch Bar / camera / Touch ID"
    kind: issue
    author: "PaulShadwell"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/11373"
    title: "Issue #11373: No driver path for the pre-T2 FaceTime HD camera (Broadcom 1570)"
    kind: issue
    author: "rand0mdud3"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/4529"
    title: "Issue #4529: Built-in webcam not detected on Arch / Omarchy (/dev/video* missing)"
    kind: issue
    author: "yassinekrika"
    date: "2026-02-06"
  - url: "https://github.com/omacom/omarchy/issues/6233"
    title: "Issue #6233: Built-in webcam not working on Acer Nitro laptop, also broken on Ubuntu"
    kind: issue
    author: "abduvaliy-hbai"
    date: "2026-07-18"
credits:
  - name: "spencerbull"
    url: "https://github.com/spencerbull"
    for: "The CVS bridge rework of intel-ipu7-camera that shipped in 4.0.4"
  - name: "labjt"
    url: "https://github.com/labjt"
    for: "Showing that the package's own DKMS intel_cvs shadows the in-tree module"
  - name: "nathankramm"
    url: "https://github.com/nathankramm"
    for: "Pinning the jsoncpp soname break to the HAL plugin with one ldd check"
  - name: "ocewers"
    url: "https://github.com/ocewers"
    for: "Working out the IMX471 path on the ThinkPad X1 Carbon Gen 14"
  - name: "pkolbas"
    url: "https://github.com/pkolbas"
    for: "Documenting that the package is built for Panther Lake only"
  - name: "yashranaway"
    url: "https://github.com/yashranaway"
    for: "The 4.0.0 change that stops the picker offering raw sensor nodes"
faq:
  - q: "Does Omarchy install anything for my webcam automatically?"
    a: "One thing only. install/hardware/intel/ipu7-camera.sh installs intel-ipu7-camera if the ACPI HID OVTI08F4 appears anywhere in /sys/bus/acpi/devices. There is no IPU6 leaf and no check on which IPU controller you actually have."
  - q: "Why does my camera show up in every app but send black frames?"
    a: "That is /dev/video50, the v4l2loopback node intel-ipu7-camera publishes. The node exists whether or not the HAL behind it found a sensor, so apps see a camera that never delivers a picture."
  - q: "Will a newer kernel fix it?"
    a: "Sometimes. The IMX471 driver and its TBE20A0 binding landed after 7.2 was tagged, so Arch gets them at 7.3. Panther Lake needed a package change instead, not a kernel one."
related: [suspend-wont-resume-s2idle, screenshot-shortcut-not-working, fingerprint-enrollment-fails, install-fails-or-stalls]
draft: false
---

Most "no webcam" reports on Omarchy are not one bug. They are five or six different machines whose only shared symptom is an empty camera list. Work out which one you have before you change anything.

## The fix

**1. Identify what you actually have.** Run these on 3.x and 4.x alike:

```bash
omarchy-capture-webcam-list
lsusb | grep -i cam
lspci -nn | grep -iE 'imaging|image signal|camera'
for d in /sys/bus/acpi/devices/*/; do
  printf '%s %s\n' "$(cat "$d/hid" 2>/dev/null)" "$(cat "$d/status" 2>/dev/null)"
done | grep -iE 'OVTI|TBE|SONY|INT3472|INTC10'
```

If `lsusb` names your camera, it is an ordinary UVC device and none of the Intel sections below apply. If `lspci` shows an imaging unit, the PCI ID decides the rest: `8086:b05d` is Panther Lake IPU7.5, `8086:645d` is Lunar Lake, `8086:7d19` is Meteor Lake IPU6.

**2. Panther Lake (`8086:b05d`, sensor `OVTI08F4` with status 15).** This is the Dell XPS 14 and XPS 16 case, and it is the one Omarchy fixed. Update and reboot:

```bash
omarchy update   # or Update > Omarchy in the menu, then reboot
```

4.0.4 carries `intel-ipu7-camera` 1.0.6, which adds a DKMS build of the in-tree `Intel CVS` bridge driver for 7.2 kernels, patches the HAL to route the sensor link through that entity, and gates the old `vision-drivers` module to pre-7.2 kernels. A reboot is required, not just a service restart. The release notes list it as a webcam fix for XPS systems on 7.2.x.

**3. Still on 4.0.3, camera died after a normal update.** Check the HAL plugin:

```bash
ldd /usr/lib/libcamhal/plugins/ipu75xa.so | grep -i json
```

`libjsoncpp.so.26 => not found` means you hit the jsoncpp 1.9.8 soname bump. Updating to 4.0.4 resolves it. The journal only shows GLib assertions from `v4l2-relayd`, which never mention jsoncpp, so this is worth checking before you blame the kernel.

**4. Lunar Lake (`8086:645d`, Core Ultra 200V).** The package is installed by detection but built with `IPU_VERSIONS="ipu75xa"` only, so the plugin your IPU asks for, `ipu7x.so`, is not on disk. There is no packaged fix as of 4.0.4. If you want the fake camera out of the way:

```bash
omarchy-pkg-drop intel-ipu7-camera
```

**5. IPU6 laptops (Meteor Lake and older, sensors `OVTI01A0`, `OVTI02C1`, `OVTI2740`).** Omarchy ships no IPU6 leaf at all. Worse, if your firmware also exposes an `OVTI08F4` node, the IPU7 package installs and hides the raw nodes behind a black `/dev/video50`. Drop it first, then try the libcamera route:

```bash
omarchy-pkg-drop intel-ipu7-camera
sudo pacman -S libcamera libcamera-ipa pipewire-libcamera
cam -l
```

That gets PipeWire-native apps working. Browsers want a real `/dev/video` node, which needs a `libcamerasrc` to `v4l2sink` bridge on a v4l2loopback device.

**6. ThinkPad X1 Carbon Gen 14 and X9 15p.** If `OVTI08F4` reports status 0 and `TBE20A0` reports 15, your sensor is a Sony IMX471 and the OV08X40 stack can never drive it. The driver and its ACPI binding both landed upstream after 7.2 was tagged, so Arch gets them at 7.3. Until then people are running `imx471-dkms-git` plus the libcamera plumbing in `ocewers/x1c14-camera-imx471`. Do not uninstall `intel-ipu7-camera` if you follow that route: those overlays retarget it rather than replace it.

**7. Macs.** On T2 machines the camera comes from `linux-t2` and `uvcvideo`. On pre-T2 models the FaceTime HD 1570 has no in-tree driver and Omarchy ships nothing for it. See [/hardware/t2-mac/](/hardware/t2-mac/).

## Verify it worked

```bash
omarchy-capture-webcam-list
media-ctl -p -d /dev/media0 | grep -i ov08x40     # Intel IPU only
gst-launch-1.0 icamerasrc num-buffers=5 ! fakesink
```

On a working Intel IPU machine the media graph shows the sensor entity, and on 7.2 it links through an `Intel CVS` entity rather than straight to CSI2. Then open a camera in a browser. The first two or three frames are black while the HAL starts the sensor, so give it a second before you call it dead.

## Why it happens

Omarchy's entire built-in camera setup is four lines in `install/hardware/intel/ipu7-camera.sh`. It greps `/sys/bus/acpi/devices/*/hid` for `OVTI08F4` and installs `intel-ipu7-camera` if it finds it. It does not check whether the node is enabled, which IPU controller is present, or which sensor is live. That single gate produces most of the cases above: it fires on ThinkPads whose `OVTI08F4` is a disabled table slot, on Meteor Lake machines the package cannot serve, and on Lunar Lake machines whose HAL plugin was never built.

The package then does real work on the system. It blacklists `ov08x40` behind `intel_cvs`, hides the raw V4L2 nodes with a udev rule, turns off WirePlumber's libcamera monitor, and publishes `/dev/video50` from `icamerasrc`. So when it lands on hardware it cannot drive, you get a camera that appears everywhere and delivers nothing, which is worse than having no node at all.

The Panther Lake break on kernel 7.2 was separate and specific. Linux 7.2's `ipu-bridge` started placing the Intel CVS controller between the sensor and the CSI2 receiver, and added a matching in-tree V4L2 bridge driver. The package's own out-of-tree `intel_cvs` has the same module name, installs into `updates/`, and depmod searches that first, so it displaced the in-tree driver. It registers no subdev, the IPU waited forever for one, and the sensor never joined the media graph. Two reporters found the same mechanism independently before the fix landed.

## If that did not work

**No `/dev/video*` at all and `lsusb` shows nothing.** Check the BIOS for a camera or I/O port access toggle, and any physical shutter. Some laptops simply have no Linux driver. On a report about an Acer Nitro whose camera also failed on Ubuntu, DHH answered that it has to be fixed upstream or by the vendor.

**Camera works in `qcam` but never in the browser.** That is a portal problem, not a driver one. The GTK portal rejects Hyprland's toplevel handle and the camera request fails quietly. Watch `journalctl --user -f -u xdg-desktop-portal-gtk` while you trigger it.

**Camera works at boot and dies after the first suspend.** On Panther Lake the `ov08x40` bind is dropped on resume and `camera-init` cannot restore it, so only a reboot brings it back. The 7.2 stack in 4.0.4 has proper PM ops and may change this, but it had not been confirmed when the PR merged.

**Screen recording shows a black webcam overlay.** The picker only filters on Device Caps, and IPU7 raw Bayer nodes advertise Video Capture while offering no format mpv can read. Pick the `/dev/video50` entry by hand instead of letting auto-detect take the first one.

## Related

- [/hardware/webcam/](/hardware/webcam/) for the per machine status table
- [/hardware/dell-xps-14-2026/](/hardware/dell-xps-14-2026/) and [/hardware/lenovo-thinkpad-x1-carbon/](/hardware/lenovo-thinkpad-x1-carbon/)
- [/hardware/t2-mac/](/hardware/t2-mac/) for Apple hardware, including what a full disk install costs you
- [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/) if the camera is one of several things lost on resume
- [/switch/screen-sharing-meet-zoom-teams/](/switch/screen-sharing-meet-zoom-teams/) for the portal side of calls
- [/reference/commands/omarchy-hw-webcam/](/reference/commands/omarchy-hw-webcam/) for what the detection check actually runs
- The Omarchy manual covers the overlay in [Screenshots and Recording](https://omarchy.org/manual/screenshots-recording/)
