---
title: "Minisforum mini PCs on Omarchy"
description: "Minisforum UM790, UM870, EliteMini and AI X1 Pro on Omarchy 4.0.4: what the tracker actually proves, the amdgpu dcn31 panics, the fingerprint gate, and DMI quirks."
answer: "Minisforum AMD mini PCs are a reasonable Omarchy box, but the evidence is thin. Omarchy ships no quirk script and no DMI match for Minisforum, so you get the generic AMD path. Three confirmed reports: amdgpu dcn31 panics on 4.0.0 that a clean Quattro reinstall cleared, hibernate that needs the Limine bootloader, and a fingerprint reader Omarchy still refuses to detect in 4.0.4."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Minisforum"
model: "Minisforum mini PCs (UM780, UM790, UM870, EliteMini, AI X1 Pro)"
dmi: ["Venus series", "F7BSC", "Micro Computer (HK) Tech Limited"]
year: "2023-2026"
cpu: "AMD Ryzen 9 7940HS, Ryzen 7 8745H, Ryzen AI 9 HX 470 in the reported machines"
gpu: "AMD Radeon 780M integrated (amdgpu, Phoenix1, gfx1103, PCI 1002:15bf)"
rating: silver
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: unknown
  webcam: "n/a"
  fingerprint: broken
  gpu: partial
  suspend: unknown
  hibernate: works
  touchpad: "n/a"
  display: partial
  battery: "n/a"
  keyboard: "n/a"
quirkScripts: []
issueCount: 3
tags: [minisforum, mini-pc, amd, amdgpu, radeon-780m, fingerprint]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7549"
    title: "Issue #7549: Frequent kernel panics after upgrade to Quattro."
    kind: issue
    author: "kowalcj0"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/7535"
    title: "Issue #7535: Fingerprint reader not detected: Minisforum AI X1 Pro (Realtek 2541:fa03)"
    kind: issue
    author: "Zyliax"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/4212"
    title: "Issue #4212: Enable hibernate throws limine-mkinitcpio not found"
    kind: issue
    author: "sedubois"
    date: "2026-01-10"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Omarchy v4.0.4 release notes"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Omarchy v4.0.3 release notes"
    kind: release
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy manual: Hardware authentication"
    kind: manual
credits:
  - name: "kowalcj0"
    url: "https://github.com/kowalcj0"
    for: "Full debug dump and amdgpu dcn31 backtrace from a Venus series UM790-class box"
  - name: "Zyliax"
    url: "https://github.com/Zyliax"
    for: "Traced the fingerprint failure to two specific lines in omarchy-hw-fingerprint"
  - name: "perminder-klair"
    url: "https://github.com/perminder-klair"
    for: "Second machine confirming the same Realtek 2541:fa03 detection gate"
  - name: "RokRage"
    url: "https://github.com/RokRage"
    for: "Confirmed the same gate blocks vendor 3274 on Omarchy 4.0.3"
  - name: "sedubois"
    url: "https://github.com/sedubois"
    for: "Reported and later confirmed hibernate on a UM870 Slim"
faq:
  - q: "Does Omarchy have a Minisforum hardware profile?"
    a: "No. There is no Minisforum entry in install/hardware/ and nothing calls omarchy-hw-match with a Minisforum string in v4.0.4. You get the generic AMD path."
  - q: "Why does omarchy-hw-match Minisforum return nothing?"
    a: "Minisforum boxes do not put the brand in DMI. The UM790-class machine in issue #7549 reports vendor Micro Computer (HK) Tech Limited, product name Venus series, board F7BSC."
  - q: "Can I use the fingerprint reader on a Minisforum AI X1 Pro?"
    a: "Not through the Omarchy menu on 4.0.4. The reader works with stock fprintd and libfprint, but Omarchy's detection script exits before setup starts. Issue #7535 is still open."
related: [amd-gpu, fingerprint, suspend-sleep, boot-limine, beelink-ser]
draft: false
---

Minisforum builds small AMD desktops: the UM780 and UM790 on Ryzen 7040-series, the UM870 on Ryzen 8000-series, the older EliteMini line, and newer Ryzen AI boxes. They sit in the same category as a Beelink SER, which is the mini PC shape the Omarchy community talks about most. This page covers what the tracker actually proves about them on Omarchy 3.x and 4.x, checked against the v4.0.4 source tree.

## Verdict

Silver, with the caveat that the evidence base is small. My dataset attaches six issues to Minisforum, but only three of them are on Minisforum hardware. The other three were matched on passing mentions in comments and are on unrelated machines, so I am not counting them.

The three real reports show a box that works once it is installed, with AMD integrated graphics doing the usual AMD integrated graphics things. There is no Minisforum-specific enablement in Omarchy at all. No script under `install/hardware/`, no DMI match, no audio tuning. That is normal for a mini PC and it is not a bad sign: a Ryzen APU with a Realtek 2.5GbE NIC and an Intel Wi-Fi card is about as mainline as x86 gets.

The reason it is not gold is that nobody has published a clean, multi-subsystem confirmation on a current release, and one of the three reports is an open bug that is still open in 4.0.4.

## What works

From the full `omarchy-debug` dump in issue [#7549](https://github.com/omacom/omarchy/issues/7549), a UM790-class machine on Omarchy 4.0.0 brings up:

- `amdgpu` on Phoenix1 (`gfx1103`, PCI `1002:15bf`), with RADV Vulkan 1.4 and Mesa OpenGL 4.6 both live.
- Two DisplayPort outputs driving a 4K panel and a Dell U4025QW at the same time.
- Realtek RTL8125 2.5GbE on `r8169`, link up at 1000 Mbps.
- Intel AX210 on `iwlwifi` and its Bluetooth radio on `btusb`, both present and bound.
- Kingston NVMe, Btrfs on LUKS, zram swap, and hibernation registered by the kernel.

Hibernate is separately confirmed. sedubois opened issue [#4212](https://github.com/omacom/omarchy/issues/4212) on a UM870 Slim and later reported hibernate working end to end on Omarchy 3.4.0: pick hibernate, wait for the front LED, unplug, plug back in, power on, and the running applications come back.

I have marked Wi-Fi, Bluetooth, audio and suspend as unknown rather than working. The radios are present and bound in that dump, but the reporter was on Ethernet with Wi-Fi down and Bluetooth soft blocked, so nobody has said out loud that they carry traffic on a Minisforum. Treat those as very likely fine rather than proven.

## What breaks

**amdgpu display-engine faults on Quattro.** kowalcj0 reported frequent kernel panics after upgrading a Venus series box to 4.0.0. Nothing landed in `dmesg` or `journalctl` at the moment of the crash, but the previous boot's log carried a `REG_WAIT timeout` and a warning at `dcn31_program_compbuf_size`, with the backtrace running through `dcn20_optimize_bandwidth`, `dc_commit_streams`, `amdgpu_dm_atomic_commit_tail` and `drm_framebuffer_remove`. That is the DCN 3.1 display engine on a dual-DisplayPort desk, not the 3D engine. The reporter closed his own issue on 2026-09-01 after reinstalling Quattro from scratch: he said everything worked afterwards, with no GPU or kernel crashes. So this reads as an upgrade-state problem rather than a hardware defect, but a 4.0.0 in-place upgrade was enough to produce it.

**The fingerprint reader is gated off.** Issue [#7535](https://github.com/omacom/omarchy/issues/7535) covers a Minisforum AI X1 Pro with a Realtek `2541:fa03` reader. `omarchy setup security fingerprint` aborts with "No fingerprint sensor detected." Zyliax traced it to two lines in `bin/omarchy-hw-fingerprint`: vendor `2541` is not in `fingerprint_vendors`, and the reader's product string is "Finger Print" as two words, which the `*fingerprint*` glob does not catch. perminder-klair confirmed the same reader on a second machine and noted that stock `fprintd` and `libfprint 1.94.100` drive it fine once the PAM files are written by hand. RokRage hit the same gate on Omarchy 4.0.3 with a different reader, vendor `3274`.

I checked this against the shipped source. `bin/omarchy-hw-fingerprint` is byte-identical in v4.0.2, v4.0.3 and v4.0.4, and `fingerprint_vendors` still reads `27c6 138a 06cb 08ff 1c7a 147e`. The v4.0.3 notes list "Improve fingerprint-reader support during setup", but whatever that changed, it was not this file. The issue is open and unfixed on 4.0.4.

**Hibernate needs Limine.** Issue #4212 was a machine installed before Omarchy moved to Limine, so `omarchy hibernation setup` called `limine-mkinitcpio` and got "command not found". DHH confirmed that hibernation auto-configuration requires Limine. In v4.0.4 the script checks first and prints "Skipping hibernation setup (requires Limine bootloader)" instead of failing, and that guard is already present in v3.8.4. If you installed from a recent ISO you are on Limine and this does not apply.

## What Omarchy does for this model

Nothing model-specific. Grepping the v4.0.4 tree for `minisforum`, `UM790`, `UM870`, `UM780` and `EliteMini` returns no hits, and `install/hardware/all.sh` has no Minisforum entry. The scripts it does run on your box are the generic ones: `network.sh`, `set-wireless-regdom.sh`, `bluetooth.sh`, `vulkan.sh`, `speaker-tuning.sh` and `pacman.sh`.

The DMI detail is worth knowing. `omarchy-hw-match` greps `/sys/class/dmi/id/product_name` and `product_family`, and Minisforum does not put its own name there. The UM790-class machine in #7549 reports system vendor "Micro Computer (HK) Tech Limited", product name "Venus series", board "F7BSC" from Shenzhen Meigao Equipment, on AMI UEFI 1.09. If you write your own hook or a bug report, match on `Venus series` or the board string, not on `Minisforum`.

## Variants

The reported machines are all AMD APUs on the Radeon 780M, spread across three generations: Ryzen 9 7940HS on the UM790 class, Ryzen 7 8745H on the UM870 Slim, and Ryzen AI 9 HX 470 on the AI X1 Pro. From an Omarchy point of view they are the same box with different clock speeds, because the display and graphics stack is the same `amdgpu` DCN 3.1 path in all three.

Prefer a plain AMD APU model. Minisforum also sells boxes with discrete NVIDIA graphics and Intel variants; neither appears in any Minisforum report I found, so you would be the first, and the NVIDIA path on Omarchy is a different set of problems. See [/hardware/nvidia/](/hardware/nvidia/) before you commit to one.

The AI X1 Pro is the only variant with a known open bug, and it is the fingerprint gate, not the machine.

## Before you install

- Update firmware from the vendor before installing. The machine in #7549 was still on a BIOS dated 2023-11-20.
- Install fresh from a current ISO rather than carrying an old install forward. Both the panic report and the hibernate report were on machines that had been upgraded in place, and the panic went away on a clean 4.0.0 install.
- Keep Limine. Hibernate is wired to it, per the [system sleep chapter](https://omarchy.org/manual/system-sleep/).
- If you run two or three DisplayPort monitors, read [/hardware/amd-gpu/](/hardware/amd-gpu/) and [/hardware/multi-monitor/](/hardware/multi-monitor/) first. The one panic on record was on a dual-DisplayPort desk.
- If your unit has a fingerprint reader, assume it will not be detected until #7535 lands. See [/hardware/fingerprint/](/hardware/fingerprint/) and the [hardware authentication chapter](https://omarchy.org/manual/hardware-authentication/).
- v4.0.4 makes `linux-omarchy` the default boot option for everyone. If a display fault appears right after that update, the previous kernel entry in Limine is the first thing to try. See [/releases/v4.0.4/](/releases/v4.0.4/).

## Related

- [/hardware/amd-gpu/](/hardware/amd-gpu/) for the `amdgpu` failure patterns behind #7549.
- [/hardware/fingerprint/](/hardware/fingerprint/) for the detection gate that blocks #7535.
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) and [/fix/hibernate-fails-or-hangs/](/fix/hibernate-fails-or-hangs/) for the Limine dependency.
- [/hardware/multi-monitor/](/hardware/multi-monitor/) if you drive more than one external panel.
- [/hardware/submit/](/hardware/submit/) if you own one of these. This page needs more than three reports.
