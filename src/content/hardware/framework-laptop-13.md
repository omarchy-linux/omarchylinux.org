---
title: "Framework Laptop 13 on Omarchy"
description: "Framework Laptop 13 running Omarchy 4.0.4: what works, the AMD mic fix Omarchy ships, the suspend and USB-C dock bugs, and which generation to buy."
answer: "Silver. The Framework Laptop 13 is one of the most common Omarchy machines and installs cleanly on every generation. Wi-Fi, Bluetooth, display, battery and the Goodix fingerprint reader all work. The real quirks are around sleep: fingerprint unlock can die after a suspend, and external displays behind a Thunderbolt dock can stay dark after a long clamshell sleep. Prefer AMD 7040 or AI 300 over 11th gen Intel."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Framework"
model: "Framework Laptop 13"
dmi: ["Laptop 13 (AMD Ryzen AI 300 Series)", "Laptop 13 (AMD Ryzen 7040Series)", "Laptop 13 Pro (Intel Core Ultra Series 3)"]
cpu: "Intel 11th to 13th gen, Intel Core Ultra Series 1 and 3 (Panther Lake), AMD Ryzen 7040, AMD Ryzen AI 300"
gpu: "Intel Iris Xe / Arc iGPU, AMD Radeon 760M / 780M / 890M"
year: "2021 to 2026"
rating: silver
subsystems:
  wifi: works
  bluetooth: works
  audio: works
  webcam: unknown
  fingerprint: partial
  gpu: works
  suspend: partial
  hibernate: partial
  touchpad: unknown
  display: partial
  battery: works
  keyboard: partial
quirkScripts:
  - name: "fix-f13-amd-audio-input.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/framework/fix-f13-amd-audio-input.sh"
    note: "Selects the HiFi (Mic1, Mic2, Speaker) PipeWire card profile on AMD Family 17h/19h audio so the internal mics are exposed. Runs on every install."
issueCount: 80
tags: [framework, framework-13, amd, intel, laptop, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/11412"
    title: "Issue #11412: Fingerprint unlock fails after every suspend (fprintd device stuck busy) and the shell retries every 250ms until unlock"
    kind: issue
    author: "callumau"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/11411"
    title: "Issue #11411: Lock screen blanks ~5 seconds after resume: suspend-gap guard re-arms the blank timer instead of holding the display"
    kind: issue
    author: "callumau"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/9513"
    title: "Issue #9513: USB-C hub/dock monitors dead on Framework 13 (Tiger Lake) after linux 7.1.9, ucsi_acpi never binds USBC000, /sys/class/typec empty"
    kind: issue
    author: "edlandm"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/7328"
    title: "Issue #7328: External display stays dark after a long suspend in clamshell: nothing re-probes the connector when the dock never re-asserts HPD"
    kind: issue
    author: "paracycle"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/6637"
    title: "Issue #6637: System freezes after upgrade to Framework 13 Pro Screen"
    kind: issue
    author: "jstreic"
    date: "2026-08-08"
  - url: "https://github.com/omacom/omarchy/issues/7730"
    title: "Issue #7730: omarchy-hibernation-available returns success when the kernel has hibernation disabled, making the Hibernate menu entry a silent no-op"
    kind: issue
    author: "mnemonicspace"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/7650"
    title: "Issue #7650: Keyboard backlight stays off after unlock: brightness-keyboard off saves 0 over the good value"
    kind: issue
    author: "mnemonicspace"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/issues/4047"
    title: "Issue #4047: Cannot boot with AMD eGPU attached, system hangs before Plymouth (Framework 13 + RX 9070 XT)"
    kind: issue
    author: "hngrdev"
    date: "2026-01-01"
  - url: "https://github.com/omacom/omarchy/issues/8629"
    title: "Issue #8629: GRUB out of memory early boot failure on AMD Zen 5 (Ryzen AI 9 HX 370 / Strix Point) Platforms"
    kind: issue
    author: "gmcquillan"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/3585"
    title: "Issue #3585: omarchy-install-steam auto-selects nvidia-utils on my Framework 13 Ai 370 HX"
    kind: issue
    author: "mechanicsunlocked"
    date: "2025-11-24"
  - url: "https://github.com/omacom/omarchy/issues/908"
    title: "Issue #908: Framework 13 Fingerprint Sensor"
    kind: issue
    author: "Rnedlose"
    date: "2025-08-18"
  - url: "https://github.com/omacom/omarchy/releases/tag/v2.1.0"
    title: "Omarchy v2.1.0 release notes (Framework Laptop 13 audio input fix)"
    kind: release
    author: "omacom"
    date: "2025-08-31"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.6.0"
    title: "Omarchy v3.6.0 release notes (2 W idle cited on the Framework 13 Pro IPS panel)"
    kind: release
    author: "omacom"
    date: "2026-04-23"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/framework/fix-f13-amd-audio-input.sh"
    title: "install/user/hardware/framework/fix-f13-amd-audio-input.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "callumau"
    url: "https://github.com/callumau"
    for: "Traced the post-suspend fingerprint failure to a stuck fprintd verify and an uncapped 250ms retry loop"
  - name: "paracycle"
    url: "https://github.com/paracycle"
    for: "Measured sleep length against dock HPD arrival to explain why long clamshell sleeps kill the external display"
  - name: "edlandm"
    url: "https://github.com/edlandm"
    for: "Diagnosed the Tiger Lake ucsi_acpi bind failure that killed USB-C dock video"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "The Framework 13 AMD audio input fix that still ships in tree"
faq:
  - q: "Is the Framework Laptop 13 a good Omarchy machine?"
    a: "Yes. It is one of the most frequently reported machines in the Omarchy tracker, it installs without hardware workarounds, and Omarchy carries an in-tree fix for its AMD microphone routing. Expect friction around suspend and Thunderbolt docks rather than around basic install."
  - q: "Does the Framework 13 fingerprint reader work on Omarchy?"
    a: "Enrollment and unlock work. The Goodix reader is recognised by Omarchy's fingerprint detection and users have reported it working since 2025. On Omarchy 4.0.3, if the machine suspends while a verify is in flight, the reader stays dead after resume until you unlock with the password, per issue #11412."
  - q: "Which Framework 13 generation should I buy for Omarchy?"
    a: "AMD Ryzen 7040 or Ryzen AI 300, or the Intel Core Ultra Series 3 Pro board. The 11th gen Tiger Lake boards hit a kernel regression in 7.1.9 that killed USB-C dock video, which is the one generation-specific breakage on record."
related: [framework-laptop-16, framework-desktop, suspend-sleep, thunderbolt-dock, fingerprint]
draft: false
---

## Verdict

Silver. The Framework Laptop 13 is a safe Omarchy machine, and it is clearly a popular one: 80 issues in the Omarchy tracker come from Framework 13 owners, the highest count of any single model in the dataset, just ahead of the MacBook Pro. Most of those reports are not about the laptop. They are quickshell, clipboard, reminder and update bugs that happen to be filed from a Framework 13.

It is not gold because of sleep. Three separate open issues describe things that do not come back correctly after resume: the fingerprint reader, the lock screen itself, and external displays behind a Thunderbolt dock. None of them stop you using the machine, and none of them are Framework faults, but you will meet at least one of them in normal laptop use.

Checked against v4.0.4 (2026-09-15) and the 4.0.x issue history. Where a report predates Quattro it is called out below.

## What works

Wi-Fi, Bluetooth, the internal panel, the battery gauge and the Goodix fingerprint reader all come up with no manual setup. Journals attached to issue [#6637](https://github.com/omacom/omarchy/issues/6637) show a Framework 13 AMD 7040 associating on wlan0, loading Intel Bluetooth firmware and enumerating the Goodix MOC reader on a single boot, all without extra packages.

Audio works, including the internal microphones, because Omarchy ships a fix for them. See the next section.

Graphics are uneventful. AMD 760M, 780M and 890M run on amdgpu, and the Intel boards run on i915 or Xe. Omarchy installs `vulkan-radeon` or `vulkan-intel` through its generic GPU scripts and nothing Framework-specific is needed. Power is genuinely good: the v3.6.0 release notes cite 2 W idle on the Framework 13 Pro with the IPS panel.

Fingerprint enrollment has worked since at least August 2025. Issue [#908](https://github.com/omacom/omarchy/issues/908) opens with a user saying the reader works well after setting it up from the Omarchy menu, and complains only that cancelling out of the prompt was unreliable.

## What breaks

**Fingerprint unlock after suspend (4.0.3, open).** Issue [#11412](https://github.com/omacom/omarchy/issues/11412), on a Ryzen 5 7640U board, shows fprintd left with a busy device when the machine suspends mid-verify. After resume every retry fails instantly and the shell re-tries four times a second until you type your password. Workaround: type the password. A ThinkPad owner in the same thread saw the stuck fprintd survive three suspend cycles and only recover once it idled out after a password unlock, so expect it again after the next suspend that lands mid-verify.

**Lock screen blanks 5 seconds after waking (4.0.3, open).** Issue [#11411](https://github.com/omacom/omarchy/issues/11411), same reporter, same laptop. A timer frozen across suspend fires on resume and turns the displays off under you. A keypress normally brings them back, but the reporter measured a 10 second window on a Thunderbolt dock where keystrokes went nowhere until the DisplayPort link retrained.

**External display dark after a long clamshell sleep (4.0.0, open).** Issue [#7328](https://github.com/omacom/omarchy/issues/7328) is the best-measured Framework 13 bug in the tracker. On a Ryzen AI 9 HX 370 behind a CalDigit TS3 Plus, sleeps under about 12 minutes always came back; a 40 minute sleep with the lid still closed never did. The cause is that amdgpu drops hotplug interrupts raised inside the resume window, so nothing re-probes the connector when the dock fails to re-assert HPD. Opening the lid forces the rescan. The reporter's fix, PR #7329, was still open at 4.0.4.

**USB-C dock video on 11th gen Intel (open).** Issue [#9513](https://github.com/omacom/omarchy/issues/9513) reports that on a Tiger Lake Framework 13, kernel 7.1.9 stopped binding `ucsi_acpi` to the `USBC000` device, leaving `/sys/class/typec` empty and DisplayPort Alt Mode dead while USB and Ethernet on the same hub kept working. The reporter's escape hatch was `linux-lts`. A commenter later argued the timeout variant of this bug is fixed in kernel 7.2.4 but that the never-binds variant is separate and has no known upstream fix. Omarchy's stable channel now carries `linux-omarchy` 7.2.5, so this is worth re-testing before you downgrade anything.

**Pro screen module plus AMD 7040 lockups (3.8.4, open).** Issue [#6637](https://github.com/omacom/omarchy/issues/6637) describes hard freezes with kernel page faults and soft lockups when using the volume or brightness function keys, starting after a display module upgrade. Later in the thread the reporter says disabling hibernation kept the machine stable for four days.

**Hibernate menu entry can be a silent no-op.** Issue [#7730](https://github.com/omacom/omarchy/issues/7730), filed on a Framework 13 Pro Intel, shows the Hibernate menu entry appearing and doing nothing when the kernel has hibernation disabled, because `omarchy-hibernation-available` never asks the kernel. The reporter later traced the disabled state on that machine to Bitwarden Desktop holding `memfd_secret` memory, not to the laptop. The check fix, PR #7779, was still open at 4.0.4.

**eGPU attached at boot hangs the machine.** Issue [#4047](https://github.com/omacom/omarchy/issues/4047), Framework 13 plus RX 9070 XT over Thunderbolt: boot hangs before Plymouth. Hot-plugging the enclosure after login works fine. Closed with no Omarchy-side fix, since it fails before userspace exists.

**Keyboard backlight off after unlock.** Issue [#7650](https://github.com/omacom/omarchy/issues/7650), Framework 13 Pro Intel X7: the brightness helper saves 0 over the good value when the screen blanks twice, so the backlight never comes back. Four PRs proposing fixes were still open at 4.0.4.

## What Omarchy does for this model

Less than you might expect, and that is a good sign.

There is exactly one Framework 13 quirk script in the tree at v4.0.4: [`install/user/hardware/framework/fix-f13-amd-audio-input.sh`](https://github.com/omacom/omarchy/blob/v4.0.4/install/user/hardware/framework/fix-f13-amd-audio-input.sh). It looks for an AMD Family 17h/19h audio card in `pactl list cards` and sets its profile to `HiFi (Mic1, Mic2, Speaker)`, which is what exposes the internal microphones. It runs unconditionally on every install, so it is harmless on non-Framework machines. This landed as "Fix Framework Laptop 13 audio input was misconfigured" in [v2.1.0](https://github.com/omacom/omarchy/releases/tag/v2.1.0) and has survived every release since.

There is no DMI matcher for the Framework 13. `omarchy-hw-framework16` checks `sys_vendor` equals `Framework` and then matches "Laptop 16" against `product_name` or `product_family` via `omarchy-hw-match`, and the `qmk-hid` udev rule for RGB keyboards is gated behind it. Nothing in the tree keys on a Framework 13 product string. Owners report DMI product names of the form `Laptop 13 (AMD Ryzen AI 300 Series)`, `Laptop 13 (AMD Ryzen 7040Series)` and `Laptop 13 Pro (Intel Core Ultra Series 3)`, but those come from issue reports, not from a matcher you can read in the repo.

Intel Framework 13s pick up Omarchy's generic Intel enablement instead: `sof-firmware` for the audio DSP, `thermald`, `intel-lpmd` on Alder Lake and newer hybrid CPUs, `intel-media-driver` for video acceleration, and on Panther Lake boards a `fred=on` kernel command line and the IPU7 camera driver when the ACPI camera `OVTI08F4` is present. All of those match on CPU or PCI IDs, not on the Framework name.

## Variants

**AMD Ryzen 7040 and Ryzen AI 300.** The best-represented boards in the tracker and the ones the audio fix targets. Nothing generation-specific is broken on them.

**Intel Core Ultra Series 3, the "13 Pro" board.** DHH said in issue #6637 that he runs a 13 Pro on Quattro himself, and it is the machine the v3.6.0 notes cite for 2 W idle. Two of the issues cited on this page come from Pro Intel owners, both small: the hibernation availability check and the keyboard backlight.

**Intel 11th generation, Tiger Lake.** The one variant with a real generation-specific problem, issue #9513. Buy it used and cheap if you want, but test your dock before you commit.

**Ryzen AI 9 HX 370 with 64 GB: the installer may not boot.** Issue [#8629](https://github.com/omacom/omarchy/issues/8629) reports the Omarchy 4.0.1 installer ISO dying with a GRUB out-of-memory error before or at its boot menu on an HX 370 Framework with 64 GB, with Secure Boot, UMA size and TPM settings all ruled out. The reporter did not say whether the chassis was a 13 or a 16, and the issue had no replies at 4.0.4. The installed system boots with Limine, so this is an ISO-only problem.

## Before you install

- Update the Framework BIOS from Windows or the EFI updater first. Reports in the tracker name BIOS 3.05, 3.20 and 4.02, and firmware is the one layer Omarchy cannot patch for you.
- On 11th gen Intel, plug in your USB-C dock and confirm DisplayPort Alt Mode works before wiping anything.
- If you rely on hibernation, test it early. The one AMD report of lockups after hibernation resume is still open, and the Hibernate menu entry can silently do nothing if something on the system has hibernation disabled in the kernel.
- Do not attach an eGPU before first boot.
- After install, check your microphone in a call. If it is missing, the AMD profile fix did not take and you can run it by hand.
- If you game, watch the driver prompt. Issue [#3585](https://github.com/omacom/omarchy/issues/3585) reported the Steam installer auto-selecting `nvidia-utils` on an all-AMD Framework 13; that was fixed on dev the same day, but it is worth a glance.

## Related

- [Suspend and sleep on Omarchy](/hardware/suspend-sleep/) for the resume failures above
- [Thunderbolt docks](/hardware/thunderbolt-dock/) for the clamshell display problem
- [Fingerprint readers](/hardware/fingerprint/) for enrollment and PAM behaviour
- [Framework Laptop 16](/hardware/framework-laptop-16/) and the [Framework Desktop](/hardware/framework-desktop/)
- [Still broken in the latest release](/releases/still-broken/)
- Manual chapters: [System sleep](https://omarchy.org/manual/system-sleep/), [Monitors](https://omarchy.org/manual/monitors/), [Hardware authentication](https://omarchy.org/manual/hardware-authentication/)
- Own one? [Submit a hardware report](/hardware/submit/)
