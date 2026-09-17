---
title: "Thunderbolt and USB-C docks on Omarchy 4"
description: "What works and what breaks with Thunderbolt and USB-C docks on Omarchy 4.0.4: the early thunderbolt module, boltd authorization, DP alt mode wedges and the fixes."
answer: "Docks mostly work on 4.0.4. Omarchy early-loads the thunderbolt module so dock displays live at the LUKS prompt, ships bolt for device authorization, and recovers clamshell state on hotplug. The common failure is a DisplayPort alt mode path that dies after undock or suspend and needs a reboot. Suspend and resume clears many of these; the aquamarine 0.15.0 regression needs a downgrade."
appliesTo:
  from: "4.0.0"
kind: component
componentKey: "thunderbolt-dock"
status: partial
issueCount: 163
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [thunderbolt, dock, usb-c, displayport-alt-mode, ucsi]
sources:
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/1893"
    title: "Issue #1893: Plymouth Login screen not showing on external monitor connected via Thunderbolt dock"
    kind: issue
    author: "sgruendel"
    date: "2025-09-23"
  - url: "https://github.com/omacom/omarchy/pull/1894"
    title: "PR #1894: Add thunderbolt module in omarchy hook."
    kind: pr
    author: "sgruendel"
    date: "2025-12-14"
  - url: "https://github.com/omacom/omarchy/issues/10453"
    title: "Issue #10453: Early thunderbolt module removes firmware-provided dock USB before the LUKS prompt"
    kind: issue
    author: "davidisgeek"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/11019"
    title: "Issue #11019: External monitors on a USB-C dock never return after undocking (aquamarine 0.15.0 regression)"
    kind: issue
    author: "jacobrosenthal"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/11249"
    title: "Issue #11249: aquamarine 0.15.0: external monitor never recovers after being turned off (NVIDIA repro)"
    kind: issue
    author: "Tigres2526"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11908"
    title: "Issue #11908: External monitor over USB-C dock never returns after suspend (ucsi_acpi GET_CABLE_PROPERTY failed, Meteor Lake)"
    kind: issue
    author: "NikPiermafrost"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11864"
    title: "Issue #11864: USB-C to HDMI DisplayPort Alt Mode negotiation fails and stays wedged until reboot (Panther Lake xe/ucsi_acpi)"
    kind: issue
    author: "artjsalina5"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/9513"
    title: "Issue #9513: USB-C hub/dock monitors dead on Framework 13 (Tiger Lake) after linux 7.1.9"
    kind: issue
    author: "edlandm"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/7328"
    title: "Issue #7328: External display stays dark after a long suspend in clamshell"
    kind: issue
    author: "paracycle"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/8758"
    title: "Issue #8758: Boot with the lid closed on a dock: logind suspends before the dock is detected"
    kind: issue
    author: "xtr3m3b00t3r"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/10690"
    title: "Issue #10690: USB-C / Thunderbolt power blip reports lid-close while lid is open and instantly suspends"
    kind: issue
    author: "bjcatar"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7388"
    title: "Issue #7388: Apple Studio Display over USB4 flashes: stock preferred is 5K@120, then DP tunnel drops"
    kind: issue
    author: "saariuslystoned"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/10638"
    title: "Issue #10638: T1 MacBook (macbook-t1.conf) still ships pcie_ports=compat, breaking Thunderbolt dock PCIe tunneling"
    kind: issue
    author: "jeyrb"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/12207"
    title: "Issue #12207: linux-omarchy 7.2.5 (xe, Panther Lake): USB4 monitor's EDID read fails on about half of hotplugs"
    kind: issue
    author: "diazkev314"
    date: "2026-09-17"
  - url: "https://github.com/omacom/omarchy/issues/8097"
    title: "Issue #8097: omarchy-usb-autosuspend.conf never applies: usbcore is built into the kernel"
    kind: issue
    author: "paracycle"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/10492"
    title: "Issue #10492: USB-C DP alt mode dead after LTTPR link-training failures until EC power drain"
    kind: issue
    author: "dunova"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/11926"
    title: "Issue #11926: USB hot-plug doesn't work in Intel-based MacBook Pro (16-inch, 2019) with T2 chip"
    kind: issue
    author: "VasylBaran"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/3918"
    title: "Issue #3918: Shutdown not working w/ thunderbolt monitor (system restarts)"
    kind: issue
    author: "raphaelstary"
    date: "2025-12-17"
credits:
  - name: "sgruendel"
    url: "https://github.com/sgruendel"
    for: "Found that the missing thunderbolt initramfs module blanked dock displays at the LUKS prompt, and shipped the fix"
  - name: "davidisgeek"
    url: "https://github.com/davidisgeek"
    for: "Traced dock keyboards dying at the LUKS prompt to the early thunderbolt module unbinding firmware-provided USB"
  - name: "jacobrosenthal"
    url: "https://github.com/jacobrosenthal"
    for: "Identified the aquamarine 0.15.0 commit that leaves an orphaned CRTC after undocking"
  - name: "NikPiermafrost"
    url: "https://github.com/NikPiermafrost"
    for: "Documented the ucsi_acpi partner PD state loss that kills DP alt mode across suspend"
  - name: "diazkev314"
    url: "https://github.com/diazkev314"
    for: "Captured the failing USB4 EDID read with drm.debug and built a re-probe workaround"
  - name: "jeyrb"
    url: "https://github.com/jeyrb"
    for: "Found that T1 Macs still carry pcie_ports=compat, blocking dock PCIe tunneling"
faq:
  - q: "My dock's monitors are dead after unplugging and replugging. What do I do?"
    a: "Suspend and resume the machine first. That clears the wedged Type-C state in several reports, including #11908 and #11864. If it does not, and you are on aquamarine 0.15.0, you are probably hitting #11019 and need to downgrade aquamarine, Hyprland and hyprtoolkit together, since 0.15.0 bumped the soname."
  - q: "Why does my dock keyboard not work at the LUKS passphrase prompt?"
    a: "Omarchy early-loads the thunderbolt module so dock displays come up in Plymouth, but the dock cannot be authorized until boltd starts from the encrypted root. On docks whose USB ports sit behind a Thunderbolt PCIe xHCI controller, that removes the firmware-provided USB, as reported in #10453. Type the passphrase on a directly attached keyboard."
  - q: "Do I need to run boltctl to authorize a new dock?"
    a: "Usually not. Omarchy installs bolt in the base package set and leaves its defaults alone, so an attached dock is enrolled on first connection and re-authorized automatically after that. Run boltctl list when you want to confirm a dock is authorized before blaming the display path."
related: [multi-monitor, suspend-sleep, t2-mac, boot-limine, multi-monitor-layout-not-saved]
draft: false
---

Thunderbolt and USB-C docks are one of the busiest problem areas in the Omarchy tracker. The component bucket holds 163 issues, though the match pattern also sweeps in unrelated Docker reports, so the real Thunderbolt volume is smaller. This page covers what was checked against the v4.0.4 source tree and issues open on 2026-09-16.

## Status on 4.0.4

Docking works for most people. Boot with the dock attached and displays, ethernet, audio and USB come up. The failures cluster in one place: the DisplayPort alt mode path through a USB-C or Thunderbolt port, which can wedge after an undock, a monitor power cycle, or a suspend, and then refuse to come back until you reboot. The USB side of the same dock usually keeps working while video is dead, which is why these reports read like GPU bugs and are not.

Nothing here is specific to 4.x versus 3.x on the kernel side. What changed in 4.0.0 is the compositor stack: Quickshell, Hyprland 0.56 and aquamarine, and two of the worst current dock bugs live in aquamarine 0.15.0.

## What Omarchy does automatically

Four things, all confirmed in `data/source/v4.0.4`:

- **Early Thunderbolt in the initramfs.** `/etc/mkinitcpio.conf.d/thunderbolt_module.conf` contains a single line, `MODULES+=(thunderbolt)`. It was added by PR #1894 for issue #1893, where a BeeLink SER8 on a Dell WD22TB4 showed a black screen at login, and shipped in v3.2.3 on 2025-12-15. Without it, a display behind a dock is dark at the Plymouth and LUKS prompt.
- **`bolt` in the base package set.** `install/omarchy-base.packages` lists `bolt`, so `boltd` and `boltctl` are present for Thunderbolt device authorization. No Omarchy script configures it further, so enrollment and security level follow upstream bolt defaults.
- **Monitor hotplug recovery.** `omarchy-hyprland-monitor-watch` listens on the Hyprland socket for `monitoradded` and `monitorremoved`, re-syncs clamshell state three more times at one, three and seven seconds after each change, and runs a backoff loop that reloads Hyprland while any enabled output reports a 0x0 mode. `omarchy-hw-external-monitors` reads `/sys/class/drm` directly and ignores eDP, LVDS and DSI, so an external panel on a dock counts. `omarchy-hw-recover-internal-monitor` clears a stale internal-display-disable toggle when you undock.
- **DDC/CI brightness.** `ddcutil` is in the base list and 4.0.0 wired the brightness keys to the focused external display, so a dock-attached monitor that speaks DDC responds to the same keys as the laptop panel.

There is no dock-specific script in `install/hardware/` and no `omarchy-hw-thunderbolt`. The `omarchy-hw-*` scripts that matter here are the clamshell and external-monitor helpers listed above.

## Known problems

The recurring pattern is a Type-C port whose PD or alt mode state gets stuck. On Panther Lake and Meteor Lake Dell XPS machines the kernel logs `ucsi_acpi ... Firmware bug: duplicate partner altmode SVID 0xff01` and a VDO mismatch, the adapter falls back to a USB billboard device, and the port stays in USB2 mode until reboot. Reporters on #11864 confirmed the same VDO pair on an XPS 16 and an XPS 15 9530, with different monitors, so the bad table is laptop firmware rather than anything negotiated from the sink.

A second pattern is compositor side. aquamarine 0.15.0 added a guard that rejects a commit to an already-disconnected output, which leaves the kernel CRTC active after an undock. The orphaned pipe holds the Type-C link reference and every later modeset fails. That is #11019 on Intel and #11249 on NVIDIA, and it is a regression against aquamarine 0.14.0.

### Known issues

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#1893](https://github.com/omacom/omarchy/issues/1893) dock display black at LUKS/Plymouth | BeeLink SER8 + Dell WD22TB4 | fixed | v3.2.3 |
| [#10453](https://github.com/omacom/omarchy/issues/10453) early thunderbolt module drops dock USB before LUKS | GMKtec NucBox K8 Plus + Dell WD19TB | open | not yet |
| [#11019](https://github.com/omacom/omarchy/issues/11019) dock monitors never return after undock | Dell XPS 13 9320, Intel i915 MST docks | open | not yet |
| [#11249](https://github.com/omacom/omarchy/issues/11249) external monitor dead after power cycle | ASUS Ryzen 9 8945HS + RTX 4060 | open | not yet |
| [#11908](https://github.com/omacom/omarchy/issues/11908) monitor gone after suspend, reboot only | Meteor Lake laptops on USB-C docks | open | not yet |
| [#11864](https://github.com/omacom/omarchy/issues/11864) DP alt mode wedged until reboot | Dell XPS 16 DA16260, XPS 15 9530 | open | not yet |
| [#9513](https://github.com/omacom/omarchy/issues/9513) ucsi_acpi never binds, no typec ports | Framework Laptop 13 11th gen | open | not yet |
| [#12207](https://github.com/omacom/omarchy/issues/12207) USB4 monitor stuck at 640x480, corrupt EDID | Dell XPS 16 + CalDigit TS5 | open | not yet |
| [#7328](https://github.com/omacom/omarchy/issues/7328) display dark after long clamshell suspend | Framework 13 AMD + CalDigit TS3 Plus | open | not yet |
| [#8758](https://github.com/omacom/omarchy/issues/8758) lid-closed boot on dock strands NetworkManager | ThinkPad P16v Gen 3 | open | not yet |
| [#10690](https://github.com/omacom/omarchy/issues/10690) USB-C power blip fakes a lid close | Dell XPS 14 DA14260 | open | not yet |
| [#7388](https://github.com/omacom/omarchy/issues/7388) Studio Display over USB4 flashes | HP ZBook X G1i, Arrow Lake | open | not yet |
| [#10638](https://github.com/omacom/omarchy/issues/10638) pcie_ports=compat blocks dock PCIe tunneling | T1 Touch Bar MacBooks | open | not yet |
| [#11926](https://github.com/omacom/omarchy/issues/11926) no USB hotplug at all | MacBook Pro 16-inch 2019, T2 | open | not yet |
| [#8097](https://github.com/omacom/omarchy/issues/8097) USB autosuspend drop-in has no effect | all | open | not yet |
| [#10492](https://github.com/omacom/omarchy/issues/10492) DP alt mode dead until EC power drain | Lenovo Yoga 14s ITL 2021 | open | not yet |
| [#3918](https://github.com/omacom/omarchy/issues/3918) shutdown restarts instead | Framework Desktop | open | not yet |

## Fixes that work

Try these in order. Stop when the picture comes back.

1. **Suspend and resume.** This is the highest-yield step and the least obvious. On #11864 a reporter confirmed a twelve-second suspend restored the display with the cable untouched, and no firmware-bug message was logged on the resume path. Logging out also worked for them. `hyprctl reload` did not.
2. **Re-probe the connector.** As root, `echo off > /sys/class/drm/card0-DP-1/status` then `echo detect >` the same file, substituting your connector. On #12207 this recovered the full EDID on eight of eight failed hotplugs, and it is the basis of that reporter's udev workaround for USB4 monitors that come up at 640x480.
3. **Check whether video or the whole dock is gone.** Run `boltctl list` and `ls /sys/class/typec`. If `/sys/class/typec` is empty, the Type-C stack never came up at all, which is #9513 and a kernel problem, not a display one. If boltctl shows the dock authorized but no DRM connector appears, you are in the alt mode wedge.
4. **Pin a mode instead of using `preferred`.** The stock `~/.config/hypr/monitors.lua` uses `mode = "preferred"`, which on an Apple Studio Display picks 5120x2880@120 and then drops the tunnel, per #7388. Write an explicit mode for the dock monitor. See the [Monitors chapter](https://omarchy.org/manual/monitors/) and [/hardware/multi-monitor/](/hardware/multi-monitor/).
5. **If the failure started after the 2026-09-09 update, suspect aquamarine.** Downgrading means holding aquamarine, Hyprland and hyprtoolkit together, because 0.15.0 bumped the library soname. That is a real risk on a rolling system, so read #11019 and #11249 before doing it.
6. **Last resort for a truly dead port: full power drain.** On #10492 the port stayed dead across reboots and shutdowns, and only came back after removing all cables and holding the power button for roughly half a minute.

Two Omarchy-side notes. If your dock keyboard is dead at the LUKS prompt, that is #10453 and there is no fix yet; use a directly attached keyboard. If you are on a T1 Touch Bar MacBook and the dock's ethernet never appears, #10638 has a one-line `sed` on `/etc/limine-entry-tool.d/macbook-t1.conf` that the reporter confirmed, followed by `limine-mkinitcpio` and a reboot. Neither change has landed upstream as of 4.0.4.

## Report it

Run `omarchy debug`, which exists in 4.0.4 and wraps `omarchy-debug`. Add `--print` to see the output without uploading, and `--no-sudo` to skip `dmesg`.

A dock report is only useful with the parts the maintainers cannot guess. Include the dock model and the exact cable, `boltctl list`, `ls /sys/class/typec` and the contents of any `portN-partner` directory, the `status` of every `/sys/class/drm/card*-*`, and `hyprctl monitors all -j`. Capture `journalctl -k -b` filtered for `ucsi`, `typec`, `thunderbolt` and `drm`. Say explicitly whether the USB side of the dock still works while video is gone, and whether suspend and resume recovers it. That one sentence separates the alt mode wedge from the aquamarine regression faster than anything else.

## Related

- [/hardware/multi-monitor/](/hardware/multi-monitor/) for layout, scaling and clamshell behaviour
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) for resume failures that are not dock-specific
- [/hardware/t2-mac/](/hardware/t2-mac/) for Intel Macs with T1 and T2 chips
- [/hardware/boot-limine/](/hardware/boot-limine/) for kernel command line edits
- [/fix/multi-monitor-layout-not-saved/](/fix/multi-monitor-layout-not-saved/) when the arrangement resets on every dock
