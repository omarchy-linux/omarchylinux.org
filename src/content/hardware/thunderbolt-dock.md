---
title: "Thunderbolt and USB-C docks on Omarchy 4"
description: "What works and what breaks with Thunderbolt and USB-C docks on Omarchy 4.0.4: the early thunderbolt module, bolt authorization, DP alt mode wedges and fixes."
answer: "Booting docked is the case that works in the reports; the trouble starts on undock, suspend or a monitor power cycle. Omarchy early-loads the thunderbolt module so dock displays live at the LUKS prompt, ships bolt for authorization, and re-syncs clamshell state on hotplug. The common failure is a DisplayPort alt mode path that stays dead. Suspend and resume or a VT switch clears many of these; the aquamarine 0.15.0 regression is fixed upstream in 0.15.1."
appliesTo:
  from: "4.0.0"
kind: component
componentKey: "thunderbolt-dock"
status: partial
issueCount: 163
lastVerified: 2026-09-17
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
    title: "Issue #11249: aquamarine 0.15.0: external monitor never recovers after being turned off (NVIDIA repro), please hold or patch aquamarine"
    kind: issue
    author: "Tigres2526"
    date: "2026-09-10"
  - url: "https://github.com/hyprwm/aquamarine/releases/tag/v0.15.1"
    title: "aquamarine v0.15.1 release notes (includes PR #410, release output on disconnect manually)"
    kind: release
    author: "hyprwm"
    date: "2026-09-17"
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
    title: "Issue #9513: USB-C hub/dock monitors dead on Framework 13 (Tiger Lake) after linux 7.1.9, ucsi_acpi never binds USBC000"
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
    for: "Found that the missing thunderbolt initramfs module blanked dock displays at the Plymouth prompt, and shipped the fix"
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
    for: "Found that a T1 MacBook still carried pcie_ports=compat, blocking dock PCIe tunneling"
faq:
  - q: "My dock's monitors are dead after unplugging and replugging. What do I do?"
    a: "Suspend and resume the machine first, then try a VT switch (Ctrl+Alt+F2, then back). Suspend cleared the wedged Type-C state for two reporters on #11864 and one on #9513; the VT switch released the orphaned CRTC on #11019 and #11249. If the failure started with aquamarine 0.15.0, install aquamarine 0.15.1, which carries the upstream fix and needs no Hyprland rebuild."
  - q: "Why does my dock keyboard not work at the LUKS passphrase prompt?"
    a: "Omarchy early-loads the thunderbolt module so dock displays come up in Plymouth, but the dock cannot be authorized until boltd starts from the encrypted root. On docks whose USB ports sit behind a Thunderbolt PCIe xHCI controller, that removes the firmware-provided USB, as reported in #10453. Type the passphrase on a directly attached keyboard."
  - q: "Do I need to run boltctl to authorize a new dock?"
    a: "Possibly. Omarchy installs bolt in the base package set and nothing in the tree configures it, so you get upstream defaults. On #10453 the reporter ran boltctl enroll once, which restored the dock's USB immediately, and boltd re-authorized the stored dock automatically on every later boot. Run boltctl list to confirm a dock is authorized before blaming the display path."
related: [multi-monitor, suspend-sleep, t2-mac, boot-limine, multi-monitor-layout-not-saved]
draft: false
---

Thunderbolt and USB-C docks are one of the busiest problem areas in the Omarchy tracker. The search this page draws on returns 163 issues matching dock and Thunderbolt terms, but that pattern also catches Docker reports, so the real Thunderbolt volume is smaller. This page covers what was checked against the 4.0.4 source tree and the issues open on 2026-09-17.

## Status on 4.0.4

Booting with the dock attached is the case that works in the reports here. On #11019 a docked boot and a hotplug from a clean boot both worked, on #10453 the dock monitors were up from firmware through to the desktop, and on #11908 the dock display worked until the first suspend. The failures cluster in one place: the DisplayPort alt mode path through a USB-C or Thunderbolt port, which can wedge after an undock, a monitor power cycle, or a suspend, and then refuse to come back until you reboot. The USB side of the same dock usually keeps working while video is dead, which is why these reports read like GPU bugs and are not.

The kernel-side failures below are not Omarchy-specific; reporters on #11864 and #10492 reproduced them on stock Arch kernels. What 4.x changed is the compositor side: Hyprland 0.56 with the aquamarine backend, and the aquamarine 0.14.0 to 0.15.0 package update that reached the stable channel around 2026-09-09 (#11019) is behind two of the worst current dock bugs.

## What Omarchy does automatically

Four things, all confirmed in the 4.0.4 tree:

- **Early Thunderbolt in the initramfs.** `/etc/mkinitcpio.conf.d/thunderbolt_module.conf` contains a single line, `MODULES+=(thunderbolt)`. It was added by PR #1894 for issue #1893, where a BeeLink SER8 on a Dell WD22TB4 showed a black screen at the Plymouth login, and shipped in v3.2.3 on 2025-12-15. Without it, a display behind a dock is dark at the Plymouth and LUKS prompt.
- **`bolt` in the base package set.** `install/omarchy-base.packages` lists `bolt`, so `boltd` and `boltctl` are present for Thunderbolt device authorization. No Omarchy script configures it further, so enrollment and security level follow upstream bolt defaults.
- **Monitor hotplug recovery.** `omarchy-hyprland-monitor-watch` listens on the Hyprland socket for `monitoradded` and `monitorremoved`, re-syncs clamshell state three more times at one, three and seven seconds after each change, and runs a backoff loop that reloads Hyprland while any enabled output reports a 0x0 mode. `omarchy-hw-external-monitors` reads `/sys/class/drm` directly and ignores eDP, LVDS and DSI, so an external panel on a dock counts. `omarchy-hw-recover-internal-monitor` clears a stale internal-display-disable toggle when no external display is connected.
- **DDC/CI brightness.** `ddcutil` is in the base list and 4.0.0 wired the brightness keys to the focused external display, so a dock-attached monitor that speaks DDC responds to the same keys as the laptop panel.

There is no dock-specific script in `install/hardware/` and no `omarchy-hw-thunderbolt`. The `omarchy-hw-*` scripts that matter here are the clamshell and external-monitor helpers listed above.

## Known problems

The recurring pattern is a Type-C port whose PD or alt mode state gets stuck. On the Dell XPS 16 DA16260 (Panther Lake, `xe`) and the XPS 15 9530 (`i915`) the kernel logs `ucsi_acpi ... Firmware bug: duplicate partner altmode SVID 0xff01` and a VDO mismatch, the adapter enumerates as a USB billboard device, and the port stays at USB2 with no DRM connector (#11864). All three reporters there saw the same first VDO value, and one saw a byte-identical pair with two different monitors on all three ports, which points at the laptop's firmware table rather than the monitor. On Meteor Lake the symptom after s2idle is `ucsi_acpi ... GET_CABLE_PROPERTY failed (-5)` with both partner alt modes inactive, and there a reboot was the only recovery (#11908). On two Tiger Lake machines `/sys/class/typec` is empty because `ucsi_acpi` never binds the `USBC000` device at all (#9513, #10492).

A second pattern is compositor side. aquamarine 0.15.0 rejects a commit to an output the kernel already reports disconnected, but Hyprland only sends its disable commit after the disconnect, so the disable is dropped and the kernel CRTC stays active. On Intel that stale pipe pins the Type-C port and every modeset afterwards fails with EINVAL (#11019); on NVIDIA the failure is silent and the monitor just shows no signal (#11249). Reports cover i915, xe, amdgpu and nvidia-drm, and the trigger can be an undock, a monitor power button, or the lock screen's blank. Upstream fixed it in hyprwm/aquamarine#410, merged 2026-09-15 and released as aquamarine 0.15.1 on 2026-09-17; Arch extra had 0.15.1-1 the same morning. The Omarchy issues are still open, and whether the stable mirror has synced it is something to check with `pacman -Si aquamarine`.

### Known issues

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#1893](https://github.com/omacom/omarchy/issues/1893) dock display black at LUKS/Plymouth | BeeLink SER8 + Dell WD22TB4, Framework Desktop | fixed | v3.2.3 |
| [#10453](https://github.com/omacom/omarchy/issues/10453) early thunderbolt module drops dock USB before LUKS | GMKtec NucBox K8 Plus + Dell WD19TB | open | not yet |
| [#11019](https://github.com/omacom/omarchy/issues/11019) dock monitors never return after undock | Dell XPS 9320, ThinkPad X1 Carbon Gen 11, MST docks on i915 | open | aquamarine 0.15.1 upstream, 2026-09-17 |
| [#11249](https://github.com/omacom/omarchy/issues/11249) external monitor dead after power cycle | ASUS Ryzen 9 8945HS + RTX 4060, desktop RTX 4080/4090 | open | aquamarine 0.15.1 upstream, 2026-09-17 |
| [#11908](https://github.com/omacom/omarchy/issues/11908) monitor gone after suspend, reboot only | Meteor Lake laptop (model not given), Genesys Logic USB-C dock | open | not yet |
| [#11864](https://github.com/omacom/omarchy/issues/11864) DP alt mode wedged until reboot or suspend | Dell XPS 16 DA16260, XPS 15 9530 | open | not yet |
| [#9513](https://github.com/omacom/omarchy/issues/9513) ucsi_acpi never binds, no typec ports | Framework Laptop 13 11th gen | open | not yet |
| [#12207](https://github.com/omacom/omarchy/issues/12207) USB4 monitor stuck at 640x480, corrupt EDID | Dell XPS 16 + CalDigit TS5 or direct | open | not yet |
| [#7328](https://github.com/omacom/omarchy/issues/7328) display dark after long clamshell suspend | Framework 13 AMD + CalDigit TS3 Plus | open | not yet |
| [#8758](https://github.com/omacom/omarchy/issues/8758) lid-closed boot on dock strands NetworkManager | ThinkPad P16v Gen 3, Dell laptop + WD22TB4 | open | not yet |
| [#10690](https://github.com/omacom/omarchy/issues/10690) USB-C power blip fakes a lid close | Dell XPS 14 DA14260 | open | not yet |
| [#7388](https://github.com/omacom/omarchy/issues/7388) Studio Display over USB4 flashes | HP ZBook X G1i, Arrow Lake | open | not yet |
| [#10638](https://github.com/omacom/omarchy/issues/10638) pcie_ports=compat blocks dock PCIe tunneling | MacBookPro13,2 (T1), reported on 4.0.0.alpha | open | not yet |
| [#11926](https://github.com/omacom/omarchy/issues/11926) no USB hotplug at all | MacBook Pro 16-inch 2019, T2 | open | not yet |
| [#8097](https://github.com/omacom/omarchy/issues/8097) USB autosuspend drop-in has no effect | all installs with the stock drop-in | open | not yet |
| [#10492](https://github.com/omacom/omarchy/issues/10492) DP alt mode dead until EC power drain | Lenovo Yoga 14s ITL 2021 | open | not yet |
| [#3918](https://github.com/omacom/omarchy/issues/3918) shutdown restarts instead | Framework Desktop (3.2.3 and 3.3.3 reports, none on 4.x) | open | not yet |

## Fixes that work

Try these in order. Stop when the picture comes back.

1. **Suspend and resume.** This is the highest-yield step and the least obvious. On #11864 one reporter confirmed a roughly twelve-second suspend restored the display with the cable untouched and no firmware-bug message on the resume path; a second reporter on an XPS 15 9530 found suspend and logging out both worked while `hyprctl reload` did not. A HUAWEI MateBook X Pro reporter on #9513 got the same result and scripted it as `sudo rtcwake -m mem -s 5`. It does not help on #11908, where suspend is what breaks the port.
2. **Switch to a TTY and back.** `Ctrl+Alt+F2`, then `Ctrl+Alt+F1`. Hyprland drops and reacquires DRM master, which releases a CRTC that aquamarine 0.15.0 left orphaned. Confirmed on #11019 and #11249, and on #7328 for monitors powered off overnight while the host stayed awake. It sometimes needs a second round, and one reporter had Chrome crash on the switch.
3. **Re-probe the connector.** As root, `echo off > /sys/class/drm/card0-DP-1/status`, then `echo on >` and `echo detect >` into the same file, substituting your connector. On #12207 this recovered the full EDID on eight of eight failed hotplugs, and it is the basis of that reporter's udev workaround for USB4 monitors that come up at 640x480. On #7328 `detect` on its own was a no-op after a long suspend; the `off`, `on`, `detect` sequence brought the monitor back within a second.
4. **Check whether video or the whole dock is gone.** Run `boltctl list` and `ls /sys/class/typec`. If `/sys/class/typec` is empty, the Type-C stack never came up at all, which is #9513 and a kernel problem, not a display one. If boltctl shows the dock authorized but no DRM connector appears, you are in the alt mode wedge.
5. **If the failure started after the aquamarine 0.15.0 update, install 0.15.1.** It reached Arch extra on 2026-09-17, keeps the 0.15.0 soname, so Hyprland and hyprtoolkit stay as they are, and one reporter on #11019 confirmed it on Meteor Lake over USB-C. Restart the session afterwards. If the stable mirror has not synced it yet, the alternative is downgrading to aquamarine 0.14.0, which means holding aquamarine, Hyprland and hyprtoolkit together because 0.15.0 bumped the library soname; #11249 has the exact package set.
6. **Pin a mode instead of using `preferred`, and expect only partial relief.** The stock `~/.config/hypr/monitors.lua` uses `mode = "preferred"`, which on an Apple Studio Display picks 5120x2880@120 as the first EDID mode (#7388). Pinning `5120x2880@60` or `3840x2160@60` stopped that choice, but the reporter's USB4 tunnel still dropped after about twenty seconds with `failed to reach state TB_PORT_UP` in the log, so this is not a complete fix on Arrow Lake. See the [Monitors chapter](https://omarchy.org/manual/monitors/) and [/hardware/multi-monitor/](/hardware/multi-monitor/).
7. **Last resort for a truly dead port: full power drain.** On #10492 the port stayed dead across reboots and shutdowns, and only came back after removing all cables and holding the power button for thirty to forty seconds.

Two Omarchy-side notes. If your dock keyboard is dead at the LUKS prompt, that is #10453 and there is no fix yet; use a directly attached keyboard. If you are on a T1 Touch Bar MacBook and the dock's ethernet never appears, check `/etc/limine-entry-tool.d/` for a file carrying `pcie_ports=compat`. The reporter on #10638 was on 4.0.0.alpha with a `macbook-t1.conf`; the 4.0.4 tree only writes `t2-mac.conf`, and neither the installer nor migration `1785944594` touches a T1 file. The reporter's one-line `sed` replacing `pcie_ports=compat` with `pm_async=off mem_sleep_default=deep`, followed by `limine-mkinitcpio` and a reboot, made the dock's ethernet enumerate.

## Report it

Run `omarchy debug`, which in the 4.0.4 tree dispatches to `omarchy-debug`. Add `--print` to see the output without uploading, and `--no-sudo` to skip `dmesg`. Two reporters on 4.0.x builds (#7388, #12207) found the command missing; if that is you, collect the items below by hand.

A dock report is only useful with the parts the maintainers cannot guess. Include the dock model and the exact cable, `boltctl list`, `ls /sys/class/typec` and the contents of any `portN-partner` directory, the `status` of every `/sys/class/drm/card*-*`, and `hyprctl monitors all -j`. Capture `journalctl -k -b` filtered for `ucsi`, `typec`, `thunderbolt` and `drm`. Say explicitly whether the USB side of the dock still works while video is gone, and whether suspend and resume or a VT switch recovers it. That one sentence separates the alt mode wedge from the aquamarine regression faster than anything else.

## Related

- [/hardware/multi-monitor/](/hardware/multi-monitor/) for layout, scaling and clamshell behaviour
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) for resume failures that are not dock-specific
- [/hardware/t2-mac/](/hardware/t2-mac/) for Intel Macs with T1 and T2 chips
- [/hardware/boot-limine/](/hardware/boot-limine/) for kernel command line edits
- [/fix/multi-monitor-layout-not-saved/](/fix/multi-monitor-layout-not-saved/) when the arrangement resets on every dock
