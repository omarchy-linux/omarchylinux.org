---
title: "Microsoft Surface on Omarchy Linux"
description: "Microsoft Surface Laptop and Surface Pro on Omarchy 4.0.4: the keyboard works after boot but often dies at the LUKS prompt, and touch needs linux-surface."
answer: "Rate the Surface family bronze. Omarchy does detect Surface hardware and installs Marvell firmware plus an initramfs keyboard module list, but that list is only written when a pinctrl module is found, so AMD Surfaces get nothing and the built-in keyboard is dead at the LUKS prompt. Touch and stylus on IPTS models still need the third-party linux-surface kernel. Prefer an Intel Surface Laptop 3 or 4."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [microsoft, surface, laptop, luks, touchscreen, linux-surface]
kind: model
vendor: "Microsoft"
model: "Microsoft Surface (Laptop, Pro, Book, Go, Laptop Studio)"
dmi: ["Surface Laptop 3", "Surface_Laptop_3_1873", "Surface Laptop 4", "Surface Pro 8", "Surface Pro 10", "Surface Laptop Studio 2", "Surface Book 2", "Surface Go 2"]
cpu: "Intel Core (Ice Lake, Tiger Lake, Meteor Lake) and AMD Ryzen Microsoft Surface Edition (Picasso/Raven2)"
gpu: "Intel integrated or AMD Vega integrated; discrete NVIDIA on Surface Book 2 and Laptop Studio"
year: "2017-2026"
rating: bronze
subsystems:
  wifi: works
  bluetooth: unknown
  audio: unknown
  webcam: partial
  fingerprint: unknown
  gpu: partial
  suspend: unknown
  hibernate: unknown
  touchpad: partial
  display: works
  battery: partial
  keyboard: partial
quirkScripts:
  - name: "omarchy-hw-surface"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-surface"
    note: "Returns true when DMI sys_vendor is \"Microsoft Corporation\" and omarchy-hw-match finds \"Surface\" in product_name or product_family."
  - name: "install/hardware/surface.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/surface.sh"
    note: "Installs linux-firmware-marvell on any detected Surface. That is the whole script."
  - name: "install/hardware/fix-surface-keyboard.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-surface-keyboard.sh"
    note: "Writes /etc/mkinitcpio.conf.d/surface_device_modules.conf with the surface_aggregator and surface_hid module chain, but only when lsmod shows a pinctrl_ module."
issueCount: 26
sources:
  - url: "https://github.com/omacom/omarchy/issues/11128"
    title: "Issue #11128: Keyboard/touchpad dead at LUKS prompt on AMD Surface devices (fix-surface-keyboard.sh only handles pinctrl/Intel)"
    kind: issue
    author: "gs86baker"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/7111"
    title: "Issue #7111: fix-surface-keyboard.sh resets MODULES instead of appending, stripping NVIDIA early KMS on Surface devices"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/729"
    title: "Issue #729: Surface Laptop Studio keyboard not working during Plymouth boot screen"
    kind: issue
    author: "JonathanRiche"
    date: "2025-08-12"
  - url: "https://github.com/omacom/omarchy/issues/2092"
    title: "Issue #2092: [Microsoft Surface Laptop 4] - Can't type/login"
    kind: issue
    author: "Jasonghtmr"
    date: "2025-09-30"
  - url: "https://github.com/omacom/omarchy/issues/9484"
    title: "Issue #9484: Surface Book 2 touchscreen dead on stock kernel (needs linux-surface/IPTS)"
    kind: issue
    author: "GimpyHand"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/12136"
    title: "Issue #12136: Surface Laptop Studio 2: offer an opt-in linux-surface touchpad profile"
    kind: issue
    author: "Andre1Becker"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/pull/7857"
    title: "PR #7857: feat(surface-touch): add touchscreen support for Surface devices via linux-surface kernel as boot option"
    kind: pr
    author: "div5yesh"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8504"
    title: "Issue #8504: Battery percentage shows 0% on multi-battery systems (e.g. Surface Book)"
    kind: issue
    author: "jfluet"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11990"
    title: "Issue #11990: omarchy-battery-status reports only the first battery on multi-battery machines"
    kind: issue
    author: "xbones84"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9537"
    title: "Issue #9537: Surface internal display defaults to 60 Hz when 120 Hz is available"
    kind: issue
    author: "Rohansguliani"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/8843"
    title: "Issue #8843: Browser cannot access built-in camera even when libcamera, pipewire-libcamera, and qcam all work"
    kind: issue
    author: "loganwoolf"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/6079"
    title: "Issue #6079: System still running after shutdown"
    kind: issue
    author: "80think"
    date: "2026-06-12"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-surface-keyboard.sh"
    title: "install/hardware/fix-surface-keyboard.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4 release notes"
    kind: release
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "gs86baker"
    url: "https://github.com/gs86baker"
    for: "Traced the dead LUKS keyboard on AMD Surface models to the pinctrl-only branch in fix-surface-keyboard.sh, with a confirmed module list"
  - name: "chrisrharris"
    url: "https://github.com/chrisrharris"
    for: "Published the working initramfs module order for the Surface Pro 8 Signature keyboard"
  - name: "gugahoi"
    url: "https://github.com/gugahoi"
    for: "Published the Surface Laptop 3 module list and the reminder to rebuild the initramfs afterwards"
  - name: "GimpyHand"
    url: "https://github.com/GimpyHand"
    for: "Verified the linux-surface plus iptsd path for the Surface Book 2 touchscreen"
  - name: "div5yesh"
    url: "https://github.com/div5yesh"
    for: "Wrote the open PR that would add an opt-in linux-surface kernel for Surface touch"
faq:
  - q: "Does the Surface keyboard work in Omarchy?"
    a: "In the desktop session, yes. At the LUKS passphrase prompt it depends on whether /etc/mkinitcpio.conf.d/surface_device_modules.conf exists. On AMD Surface models Omarchy 4.0.x does not write it, so you need an external USB keyboard until you create it yourself."
  - q: "Does the Surface touchscreen and pen work?"
    a: "Not on the stock kernel for IPTS-era models such as the Surface Pro 4 and newer, Surface Book 2 and the Laptop Studio. Those need the third-party linux-surface kernel plus iptsd. Omarchy does not install it as of 4.0.4."
  - q: "Should I buy a Surface to run Omarchy?"
    a: "Not if you have a choice. A Framework or ThinkPad will cost you far fewer evenings. If you already own a Surface Laptop 3 or 4 on Intel, it is workable."
related: [touchpad-input, boot-limine, webcam, battery-power, nvidia]
draft: false
---

## Verdict

Bronze. A Microsoft Surface will run Omarchy, and the desktop session is mostly ordinary once you are logged in, but you should expect to do real work before and after the install. Omarchy has exactly three lines of Surface-specific code, all of them about the keyboard and Wi-Fi firmware, and none of them about touch, pen or the multi-battery machines.

The two problems that define this family are pre-boot input and touch. The built-in keyboard often does not exist yet at the LUKS passphrase prompt, because the Surface Aggregator modules are not in the initramfs. And the touchscreen and stylus on every IPTS-era Surface need a kernel Omarchy does not ship.

Checked against Omarchy 4.0.4 source, with the v3.8.4 tree compared for what changed. The single best case in the tracker is an Intel Surface Laptop 3, which is the only model the Omarchy script claims to have been tested on.

## What works

Wi-Fi is fine on the reported machines. Omarchy installs `linux-firmware-marvell` on any detected Surface, and the debug dump in [issue #11128](https://github.com/omacom/omarchy/issues/11128) shows a Qualcomm Atheros QCA6174 bound to `ath10k_pci` on a Surface Laptop 3 running 4.0.3.

The internal display works, including high-resolution panels. A Surface Pro 10 reported a 2880x1920 panel driving correctly in [issue #9537](https://github.com/omacom/omarchy/issues/9537). The only complaint there was refresh rate, covered below.

The built-in keyboard and touchpad work normally inside the Hyprland session on Surface Laptop and Surface Pro models. Every keyboard report in the tracker is about the pre-boot stage, not the desktop.

There is no Surface-specific audio, Bluetooth or suspend issue in the data set. That is weak evidence, not good evidence. It means nobody filed one, not that somebody verified it. Those subsystems are marked unknown here on purpose.

## What breaks

**Keyboard and touchpad dead at the LUKS prompt.** This is the headline bug. On AMD Surface models, `install/hardware/fix-surface-keyboard.sh` never writes its module drop-in, so the initramfs has no `surface_aggregator` chain and you must plug in a USB keyboard to unlock the disk. Greg Baker filed [issue #11128](https://github.com/omacom/omarchy/issues/11128) on 2026-09-10 with the full chain and a confirmed workaround. The script looks for a `pinctrl_` module in `lsmod`, which exists on Intel Surfaces and not on AMD ones, and on failure it simply does nothing.

This is a regression between 3.x and 4.x. In v3.8.4 the `MODULES=(...)` line sat outside the pinctrl branch and was written either way, with an empty first entry. In v4.0.0 through v4.0.4 the write moved inside the `else`, so a failed pinctrl autodetect now means no drop-in at all.

The Intel side of the same problem is older. [Issue #729](https://github.com/omacom/omarchy/issues/729) covers a Surface Laptop Studio with no keyboard at the Plymouth screen, and [issue #2092](https://github.com/omacom/omarchy/issues/2092) is a Surface Laptop 4 owner who could not type a password at all and closed it after switching keyboards. See [/fix/luks-passphrase-not-accepted-at-boot/](/fix/luks-passphrase-not-accepted-at-boot/) for the general shape of that failure.

**Touchscreen and pen do not work on the stock kernel.** Surfaces from the Pro 4 era onwards use Intel Precise Touch and Stylus, and mainline has no IPTS driver. Alex Jessup confirmed this on a Surface Book 2 in [issue #9484](https://github.com/omacom/omarchy/issues/9484) and got touch working by installing the third-party `linux-surface` kernel, `iptsd` and `surface-ipts-firmware`. [PR #7857](https://github.com/omacom/omarchy/pull/7857) would add that as an opt-in install step, keeping the stock kernel as the default boot entry and skipping when Secure Boot is on. It is still open as of 2026-09-16.

**Surface Laptop Studio 2 touchpad is worse than that.** In [issue #12136](https://github.com/omacom/omarchy/issues/12136), the haptic touchpad produces no pointer events at all on 4.0.4 with `linux-omarchy`, and the fix was the same linux-surface kernel plus the ITHC DKMS driver.

**NVIDIA early KMS gets stripped.** On a Surface Book 2 or Laptop Studio, the Surface drop-in sorts after `nvidia.conf` and resets `MODULES` instead of appending, so the NVIDIA modules are dropped from the initramfs. That is [issue #7111](https://github.com/omacom/omarchy/issues/7111), filed by an automated QA pass and confirmed in source. The Omarchy tree already documents the hazard in its own `mkinitcpio.conf.d/omarchy_hooks.conf`. See [/hardware/nvidia/](/hardware/nvidia/).

**Battery percentage is wrong on Surface Book.** `omarchy-battery-status` picks the first `BAT*` device, which on a Surface Book is the small tablet pack, so the panel can read 0% while the bar icon reads the truth. Filed twice, in [issue #8504](https://github.com/omacom/omarchy/issues/8504) and [issue #11990](https://github.com/omacom/omarchy/issues/11990). More at [/hardware/battery-power/](/hardware/battery-power/).

**The webcam may work everywhere except your browser.** On a Surface Pro running 4.0.1, `qcam` and WirePlumber saw the camera but Chromium-based browsers never did, with the GTK portal logging an unhandled parent window type. That is [issue #8843](https://github.com/omacom/omarchy/issues/8843). See [/hardware/webcam/](/hardware/webcam/).

**Internal panel defaults to 60 Hz.** On a Surface Pro 10 with a 120 Hz panel, the default wildcard rule picks the preferred mode, which is 60 Hz. [Issue #9537](https://github.com/omacom/omarchy/issues/9537) was closed by the reporter as acceptable behavior. An explicit `eDP-1` rule using Hyprland's `highrr` mode in `~/.config/hypr/monitors.lua` fixes it. The official [monitors chapter](https://omarchy.org/manual/monitors/) covers the file.

## What Omarchy does for this model

Detection is `bin/omarchy-hw-surface`: DMI `sys_vendor` must be exactly `Microsoft Corporation`, and `omarchy-hw-match "Surface"` must find the substring in `product_name` or `product_family`, case-insensitively. That catches every Surface line, including ones nobody has tested.

Two install-time leaves then run, both from `install/hardware/all.sh`:

- `surface.sh` installs `linux-firmware-marvell`. That is its entire body. The package is also listed in `install/omarchy-other.packages` under a "Surface laptop support packages" comment.
- `fix-surface-keyboard.sh` writes `/etc/mkinitcpio.conf.d/surface_device_modules.conf` containing the detected pinctrl module plus `surface_aggregator`, `surface_aggregator_registry`, `surface_aggregator_hub`, `surface_hid_core`, `surface_hid`, `surface_kbd`, `intel_lpss_pci` and `8250_dw`. The module list comes from Chris McLeod's Surface Laptop Studio install write-up, credited in the file. If `product_name` is not literally `Surface Laptop 3` the script prints "Untested Surface Device" and carries on anyway.

Both are install-time scripts. `omarchy-update` does not re-run them, so a machine that came up from 3.x through [the Quattro upgrade](/upgrade/3-to-4-quattro/) keeps whatever drop-in it already had. Check the file yourself rather than assuming.

There is no Surface entry in the Omarchy speaker tuning set, no Surface touch package, and no Surface power profile.

## Variants

Prefer the **Intel Surface Laptop 3 and 4**. The Laptop 3 is the only product name the keyboard script treats as tested, and the Intel pinctrl path is the one that actually fires.

Avoid or treat as a project: **AMD Surface Laptop 3 and 4**, where the keyboard drop-in is never written; **Surface Book 2 and Laptop Studio**, which add the NVIDIA initramfs bug on top of dead touch; **Surface Laptop Studio 2**, where the touchpad itself needs an out-of-tree driver; and **Surface Go 2**, whose only tracker report is a machine that does not finish shutting down and drains its battery overnight ([issue #6079](https://github.com/omacom/omarchy/issues/6079)).

Do not buy an **ARM Surface** for this. Omarchy ships x86_64 only.

Machines with two batteries, meaning the Surface Book family, will show wrong numbers in the power panel until one of the open battery PRs lands.

## Before you install

- Have a USB keyboard on hand. You may need it to type the LUKS passphrase on first boot, and you will need it if you land in a text console. See [/fix/stuck-at-tty-or-cannot-switch-tty/](/fix/stuck-at-tty-or-cannot-switch-tty/).
- Decide about disk encryption up front. Skipping LUKS sidesteps the whole pre-boot keyboard problem, at the obvious cost.
- After install, check that `/etc/mkinitcpio.conf.d/surface_device_modules.conf` exists. If it does not, and you are on an AMD Surface, write the module list from issue #11128 and rebuild the initramfs. Reporters used both `mkinitcpio -P` and `limine-mkinitcpio` depending on their boot setup; see [/hardware/boot-limine/](/hardware/boot-limine/).
- If you have a discrete NVIDIA GPU, check that the drop-in did not wipe your NVIDIA modules, per issue #7111.
- Treat touch and pen as not working until you decide whether to run the third-party linux-surface kernel. That kernel is unsigned for Microsoft Secure Boot keys, so plan for firmware changes.
- Turn off Secure Boot if you intend to use linux-surface at all.
- Report what you find at [/hardware/submit/](/hardware/submit/). This family has thin, mostly negative evidence, and the tracker only ever proves what is broken.

## Related

- [/hardware/touchpad-input/](/hardware/touchpad-input/)
- [/hardware/boot-limine/](/hardware/boot-limine/)
- [/hardware/webcam/](/hardware/webcam/)
- [/hardware/battery-power/](/hardware/battery-power/)
- [/hardware/nvidia/](/hardware/nvidia/)
- [/fix/luks-passphrase-not-accepted-at-boot/](/fix/luks-passphrase-not-accepted-at-boot/)
- [/releases/v4.0.4/](/releases/v4.0.4/)
