---
title: "Slimbook and TUXEDO on Omarchy Linux"
description: "Slimbook and TUXEDO laptop support on Omarchy 4.0.4: the vendor-wide backlight and ethernet quirk scripts, the 3.8.4 suspend regression, and what to check before you buy."
answer: "Rate Slimbook and TUXEDO silver. Omarchy matches these machines on DMI sys_vendor alone, installs tuxedo-drivers for the keyboard backlight, and installs a Motorcomm YT6801 ethernet driver for the Slimbook Executive. Slimbook sells machines with Omarchy preinstalled. Evidence in the tracker is thin: three issues total, including a 3.8.4 suspend regression on an InfinityBook Pro 15 that the reporter says Omarchy 4 fixed."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [slimbook, tuxedo, clevo, laptop, backlight, dkms]
kind: model
vendor: "Slimbook and TUXEDO"
model: "Slimbook and TUXEDO Linux laptops (Clevo chassis)"
dmi: ["TUXEDO", "Slimbook", "SLIMBOOK Executive-14-UC2", "TUXEDO InfinityBook Pro 15 - Gen10 - AMD"]
cpu: "Intel Core Ultra (Arrow Lake-H) and AMD Ryzen AI 9 HX 370 in the reported machines"
gpu: "Intel Arc 130T/140T integrated on the Executive-14-UC2; AMD Radeon 890M on the Ryzen AI machines"
year: "2025-2026"
rating: silver
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: unknown
  display: unknown
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "fix-tuxedo-backlight.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-tuxedo-backlight.sh"
    note: "Matches /sys/class/dmi/id/sys_vendor against TUXEDO or Slimbook, installs tuxedo-drivers-nocompatcheck-dkms, blacklists clevo_xsm_wmi and deletes orphaned clevo-xsm-wmi.ko files."
  - name: "fix-yt6801-ethernet-adapter.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-yt6801-ethernet-adapter.sh"
    note: "Matches a Motorcomm YT6801 NIC in lspci and installs yt6801-dkms. Written for the Slimbook Executive."
issueCount: 3
sources:
  - url: "https://github.com/omacom/omarchy/issues/6380"
    title: "Issue #6380: Suspend does not work anymore in 3.8.4 (worked in 3.8.2)"
    kind: issue
    author: "hirschnase"
    date: "2026-07-26"
  - url: "https://github.com/omacom/omarchy/issues/4278"
    title: "Issue #4278: Hyprland crashes & Screen doesn't load after reboot"
    kind: issue
    author: "nursahketene"
    date: "2026-01-15"
  - url: "https://github.com/omacom/omarchy/issues/11376"
    title: "Issue #11376: SDDM's Hyprland compositor repeatedly crashes with SIGSEGV as the login greeter exits after successful authentication"
    kind: issue
    author: "rclinux"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-tuxedo-backlight.sh"
    title: "install/hardware/fix-tuxedo-backlight.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/fix-yt6801-ethernet-adapter.sh"
    title: "install/hardware/fix-yt6801-ethernet-adapter.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.5.0"
    title: "Omarchy v3.5.0 release notes: Fix keyboard backlighting for Tuxedo/Slimbook laptops"
    kind: release
    author: "dhh"
    date: "2026-04-03"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.4.0"
    title: "Omarchy v3.4.0 release notes: Add compatible ethernet driver (Motorcomm YT6801) for Slimbook + Tuxedo laptops"
    kind: release
    author: "dhh"
    date: "2026-02-26"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 Quattro release notes: Stop the Tuxedo/Slimbook backlight fix from aborting hardware setup"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://learn.omacom.io/3/omacom/74/good-linux-hardware"
    title: "Good Linux Hardware (DHH's hardware list, includes the Tuxedo InfiniteBook Pro 14)"
    kind: blog
    author: "dhh"
    date: "2026-09-16"
  - url: "https://x.com/dhh/status/2097994217897283624"
    title: "DHH: You can order Omarchy preinstalled on @slimbook machines"
    kind: other
    author: "dhh"
    date: "2026-09-09"
credits:
  - name: "hirschnase"
    url: "https://github.com/hirschnase"
    for: "Reported the 3.8.4 suspend regression on a TUXEDO InfinityBook Pro 15 Gen10 AMD and confirmed Omarchy 4 fixed it"
  - name: "jaredpohl"
    url: "https://github.com/jaredpohl"
    for: "Posted the only detailed Slimbook Executive-14-UC2 report, with full Aquamarine teardown backtraces on 4.0.3"
  - name: "nursahketene"
    url: "https://github.com/nursahketene"
    for: "Reported the black screen after login on a Tuxedo 14 inch Ryzen AI 9 HX 370"
faq:
  - q: "Does Omarchy have hardware support for Slimbook and TUXEDO?"
    a: "Yes, two scripts. install/hardware/fix-tuxedo-backlight.sh installs tuxedo-drivers-nocompatcheck-dkms for the keyboard backlight, and install/hardware/fix-yt6801-ethernet-adapter.sh installs yt6801-dkms for the Motorcomm NIC in the Slimbook Executive. Neither one checks the model, only the vendor or the PCI ID."
  - q: "Can I buy a laptop with Omarchy already installed?"
    a: "Slimbook sells machines with Omarchy preinstalled, announced by DHH in September 2026. Confirm the exact SKU and the image version with the vendor. This page is not a store and cannot verify any specific order."
  - q: "Is TUXEDO OS the same thing as Omarchy?"
    a: "No. TUXEDO OS is the vendor's own Ubuntu-based distribution. Omarchy is Arch plus Hyprland. Only the tuxedo-drivers kernel package is shared, and Omarchy pulls it from the AUR as a DKMS module."
related: [suspend-sleep, intel-gpu, battery-power, dell-xps-14-2026, framework-laptop-13]
draft: false
---

## Verdict

Silver. Omarchy has shipped vendor-specific enablement for Slimbook and TUXEDO since 3.4.0, Slimbook now sells machines with Omarchy preinstalled, and the issue tracker is almost empty for both brands. But "almost empty" cuts both ways. Three issues across two vendors is not enough to call any subsystem confirmed working, so most of the subsystem table on this page says unknown on purpose.

Treat these as Clevo chassis with a Linux-first vendor in front of them. That buys you two things Omarchy uses: a working keyboard backlight driver and a Motorcomm ethernet driver. It does not buy you a tested fingerprint reader or a tested webcam.

If you want the shortest path, buy a Slimbook SKU that the vendor ships with Omarchy on the disk. You get the factory provisioning flow described below instead of an install.

## What works

The keyboard backlight works once `tuxedo-drivers-nocompatcheck-dkms` is installed, which Omarchy does for you. DHH added this in v3.5.0 under the line "Fix keyboard backlighting for Tuxedo/Slimbook laptops".

Wired ethernet on the Slimbook Executive works. The machine uses a Motorcomm YT6801 NIC that the mainline kernel does not drive, so v3.4.0 added `yt6801-dkms` behind an `lspci` check.

Suspend works on 4.x on the one TUXEDO that reported a problem. In [issue #6380](https://github.com/omacom/omarchy/issues/6380) hirschnase reported that suspend broke going from 3.8.2 to 3.8.4 on an InfinityBook Pro 15 Gen10 AMD, and later commented that after updating to Quattro the problem was gone and sleep worked again on that machine.

The TUXEDO InfiniteBook Pro 14 sits on [DHH's hardware list](https://learn.omacom.io/3/omacom/74/good-linux-hardware), described there as a matte 3K screen, an 80 Wh battery, dual NVMe, built-in ethernet and HDMI, five USB ports, at 1.45 kg. That is a recommendation, not a test report, and it is not an endorsement by Omarchy of every TUXEDO SKU.

## What breaks

Suspend on 3.8.4. Issue #6380 is the clearest data point on this page. The screen went black, the power LED changed colour, and the machine needed a hard reset. It is closed and the reporter says 4.x fixed it, so if you are still on 3.8.4 the fix is to update rather than to chase power profile rules.

Graphics teardown crashes on 4.0.3. In [issue #11376](https://github.com/omacom/omarchy/issues/11376) jaredpohl posted the only detailed Slimbook report on the tracker: a SLIMBOOK Executive-14-UC2 with an Intel Core Ultra 7 255H and Arc 130T/140T graphics, hitting a SIGSEGV inside `Aquamarine::CDRMBackend::flushAsyncCommitEvents()` when both the SDDM greeter compositor and the user session exit. The desktop still starts, so this is noise in `coredumpctl` rather than a broken machine, and it is not Slimbook-specific: the same issue collects NVIDIA and AMD reports. That report also notes a Slimbook vendor repository was enabled alongside Omarchy's mirror, which is not a clean-install reproduction.

Black screen after login on 3.x. [Issue #4278](https://github.com/omacom/omarchy/issues/4278) came from a Tuxedo 14 inch with a Ryzen AI 9 HX 370 in January 2026. The reporter recovered by switching to a TTY, removing the Hyprland config, rebooting into the default config and running `omarchy-reinstall`. That predates Quattro and the Lua config format, so the recovery steps no longer apply verbatim.

Nothing else is reported. There is no Slimbook or TUXEDO Wi-Fi issue, no audio issue, no fingerprint issue in the data. That is an absence of evidence, not a clean bill of health.

## What Omarchy does for this model

Two scripts run from `install/hardware/all.sh` on every install and every `omarchy-update`.

`install/hardware/fix-tuxedo-backlight.sh` reads `/sys/class/dmi/id/sys_vendor` and matches `TUXEDO` or `Slimbook`, case-insensitively. When it matches it installs `tuxedo-drivers-nocompatcheck-dkms`, writes `blacklist clevo_xsm_wmi` to `/etc/modprobe.d/blacklist-clevo-xsm-wmi.conf`, and deletes any leftover `clevo-xsm-wmi.ko` in `/lib/modules/*/extra/`. The comment in the file explains why: if `clevo_xsm_wmi` loads first it grabs the Clevo WMI GUIDs and `tuxedo-drivers` cannot bring up the backlight.

`install/hardware/fix-yt6801-ethernet-adapter.sh` greps `lspci` for `YT6801` or a Motorcomm ethernet controller and installs `yt6801-dkms`.

Note what these do not do. Neither script calls `omarchy-hw-match`, which is the helper other vendors use to match on `product_name` or `product_family`. The match here is vendor-wide, so every Slimbook and every TUXEDO gets the same treatment regardless of model. There is also no speaker tuning: `default/audio/tunings/` in v4.0.4 contains only `dell-xps-2026`.

Version differences matter here. On 3.5.0 through 3.8.4 the backlight script ended with `[ -f "$f" ] && sudo rm "$f"` inside a loop, which returns non-zero when the glob matches nothing and could take the rest of hardware setup down with it. v4.0.0 rewrote that as a plain `if` block, listed in the Quattro notes as "Stop the Tuxedo/Slimbook backlight fix from aborting hardware setup". In 4.0.4 both scripts also stopped asking for `linux-headers` by name, because Omarchy now ships `linux-omarchy` with `linux-omarchy-headers`, and 4.0.4 carries a migration that installs the matching headers package on machines that were missing it. If your DKMS modules are the reason you care about this page, 4.0.4 is the release you want.

## Variants

Prefer a Slimbook SKU sold with Omarchy preinstalled if you do not want to flash a USB stick at all. Confirm the model and the shipped Omarchy version with Slimbook directly before ordering.

The Slimbook Executive is the best-covered model in Omarchy's own code, since both quirk scripts name it. The Executive-14-UC2 with Intel Arrow Lake-H graphics is the one machine with a public 4.0.3 report.

The TUXEDO InfinityBook Pro line is the best-covered on the issue tracker, such as it is: a Gen10 AMD 15 inch and a 14 inch Ryzen AI 9 HX 370. The InfiniteBook Pro 14 is the one DHH lists, with a small right Shift key on the US ANSI layout as the noted annoyance.

Older Clevo rebadges from either vendor are unrated. The `clevo_xsm_wmi` blacklist exists precisely because those machines may have an out-of-tree module installed from elsewhere.

TUXEDO OS is not Omarchy. Buying TUXEDO hardware does not mean the vendor supports Omarchy on it.

## Before you install

- Run `cat /sys/class/dmi/id/sys_vendor` from the live ISO. If it does not contain TUXEDO or Slimbook, neither quirk script will fire and your backlight is on its own.
- Run `lspci | grep -i ethernet` and look for Motorcomm or YT6801. That tells you whether you depend on `yt6801-dkms`, and therefore on working kernel headers.
- Install 4.0.4 or later, or update to it first. Older releases carried the backlight script bug and asked for the wrong headers package.
- Test suspend from the System menu before you rely on the machine. Do it on battery and on AC, since the power profile switches between them.
- If you bought the machine preinstalled, run `omarchy version` and `omarchy update` on day one. A factory image can be months behind the current release.
- If you are reselling or handing the machine on, `Setup > Reset Computer` returns a Quattro-installed machine to its first-boot state. It only works on machines installed from the Quattro ISO, not on ones upgraded from 3.x.

## Related

- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/) for the failure in #6380
- [/hardware/intel-gpu/](/hardware/intel-gpu/) for Arrow Lake-H graphics on the Executive-14-UC2
- [/fix/quickshell-crashes-or-bar-missing/](/fix/quickshell-crashes-or-bar-missing/) and [/fix/black-screen-after-login/](/fix/black-screen-after-login/)
- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/) if you are still on 3.8.4 with broken suspend
- [/hardware/submit/](/hardware/submit/) if you own one of these and can fill in the unknowns
- Omarchy manual: [system sleep](https://omarchy.org/manual/system-sleep/), [updates](https://omarchy.org/manual/updates/), [troubleshooting](https://omarchy.org/manual/troubleshooting/)
