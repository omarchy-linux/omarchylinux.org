---
title: "Battery and power management on Omarchy"
description: "How battery reporting, power profiles and the low-battery warning behave on Omarchy 4.0.4, which laptops break, and the fix order that actually works."
answer: "Battery and power management mostly works on Omarchy 4.0.4. Power profiles switch automatically between AC and battery and are remembered per source. The known gaps are all in reporting: dual-battery laptops show only one pack (#11990), the 10% low-battery warning is suppressed while docked (#10939), and charge limits are misreported (#10344). Real drain problems are almost always an idle NVIDIA dGPU."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "battery-power"
issueCount: 362
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [battery, power, power-profiles, laptop, upower, thermald]
sources:
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/11990"
    title: "Issue #11990: omarchy-battery-status reports only the first battery on multi-battery machines"
    kind: issue
    author: "xbones84"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/10939"
    title: "Issue #10939: Low-battery warning never fires while docked"
    kind: issue
    author: "zorzysty"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/9670"
    title: "Issue #9670: Low-battery warning storm when AC online status flaps"
    kind: issue
    author: "calumol"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/12005"
    title: "Issue #12005: Power widget shows Charging while battery is discharging"
    kind: issue
    author: "DerAlbertCom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/10344"
    title: "Issue #10344: Battery panel ignores charge_control_end_threshold and misreports the charge limit"
    kind: issue
    author: "brightwalker25"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/7374"
    title: "Issue #7374: Power panel shows UPower hwdb charge limit instead of the real asusctl-set limit"
    kind: issue
    author: "chickymonkeys"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/6895"
    title: "Issue #6895: Power panel shows 0W discharging when power_now read returns ENODEV"
    kind: issue
    author: "ujo4eva"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/8536"
    title: "Issue #8536: Power panel never opens on battery-less desktops"
    kind: issue
    author: "sgersz"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/8648"
    title: "Issue #8648: Consumiing insane amount of battery"
    kind: issue
    author: "notTanveer"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/12095"
    title: "Issue #12095: omarchy-usb-autosuspend.conf is a no-op"
    kind: issue
    author: "jordanglean"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12096"
    title: "Issue #12096: hibernation remove leaves resume kernel parameters in the UKI"
    kind: issue
    author: "maandrij"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12190"
    title: "Issue #12190: linux-omarchy 7.2.5-3 hangs during suspend entry on Wildcat Lake"
    kind: issue
    author: "t27duck"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1776"
    title: "Issue #1776: Laptop / Hybrid GPU Power Management Issue (NVIDIA, iGPU + dGPU)"
    kind: issue
    author: "itsmedardan"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/pull/12177"
    title: "PR #12177: Add 80% battery charge cap toggle"
    kind: pr
    author: "Per0-1"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/pull/11750"
    title: "PR #11750: Support multi-battery laptops via UPower DisplayDevice in omarchy-battery-status"
    kind: pr
    author: "chartzngrafs"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/discussions/3907"
    title: "Discussion #3907: Guide: Replacing Power Profiles with TLP to improve battery life"
    kind: discussion
    author: "pomartel"
    date: "2025-12-16"
credits:
  - name: "zorzysty"
    url: "https://github.com/zorzysty"
    for: "Traced the suppressed low-battery warning to the onBattery guard in BatteryModel.js"
  - name: "calumol"
    url: "https://github.com/calumol"
    for: "Traced the repeating low-battery warning to the latch resetting on every onBattery change"
  - name: "xbones84"
    url: "https://github.com/xbones84"
    for: "Showed that the power panel text and its progress bar read two different data sources"
  - name: "brightwalker25"
    url: "https://github.com/brightwalker25"
    for: "Showed that the sysfs charge-threshold fallback is unreachable"
  - name: "ujo4eva"
    url: "https://github.com/ujo4eva"
    for: "Found the readable-but-unreadable power_now attribute that zeroes the power draw"
faq:
  - q: "Does Omarchy switch power profiles automatically when I unplug?"
    a: "Yes. Since 4.0.0 the shell reacts to the UPower on-battery change and runs omarchy-powerprofiles-set, which remembers your last explicit choice separately for AC and for battery. Out of the box that is performance on AC and balanced on battery."
  - q: "Why does my laptop show the wrong battery percentage?"
    a: "If it has two packs, omarchy-battery-status only reads the first one. That is issue #11990 and several duplicates, still open on 4.0.4. The bar icon uses the UPower aggregate device, so the icon and the panel text can disagree."
  - q: "Can I set an 80 percent charge limit from Omarchy?"
    a: "Not on 4.0.4. There is no built-in toggle. PR #12177 proposes one but is unmerged. Set charge_control_end_threshold yourself, or use your vendor tool such as asusctl."
  - q: "Should I install TLP?"
    a: "Only if power-profiles-daemon is not enough. Omarchy installs and enables power-profiles-daemon, and the two conflict. Discussion #3907 documents the swap."
related: [battery-drains-fast, suspend-sleep, hybrid-gpu, nvidia]
draft: false
---

Battery handling on Omarchy 4.x is split between three things: `power-profiles-daemon`, which Omarchy installs and enables; a small set of shell scripts under `omarchy-battery-*` and `omarchy-powerprofiles-*`; and the Quickshell power panel on `Super + Ctrl + P`. Version 4.0.0 replaced the old Waybar battery module and the udev-driven profile switching with that shell, and most of the open complaints on 4.0.4 are about what the new panel reports rather than about power management itself.

## Status on 4.0.4

Power management itself is not what people report. Profiles switch on plug and unplug as the manual describes, the 10 percent warning fires on a plain battery discharge, and thermal daemons are installed for you on Intel laptops.

Reporting is where it breaks. Checked against the v4.0.4 source tree, three of the most reported problems are visible directly in the shipped code, and all three are open: only the first battery pack is read, the low-battery warning depends on a daemon-wide flag rather than on the battery's own state, and the charge limit shown in the panel is not the limit the firmware is enforcing.

Sleep and resume are a separate subsystem with their own failure modes. See [suspend, sleep and resume](/hardware/suspend-sleep/).

## What Omarchy does automatically

On any install:

- Installs `power-profiles-daemon` from the base package list and enables it at install time.
- Runs `omarchy-powerprofiles-init` from the Hyprland autostart, which sets the profile matching your current power source on every login.
- Remembers explicit profile choices separately for AC and battery under `~/.local/state/omarchy/powerprofiles/`. With no saved choice you get `performance` on AC and `balanced` on battery.
- Re-applies the profile whenever UPower reports a power source change, which is what replaced the 3.x udev rules.
- Ignores the physical power key at the logind level, so a stray press does not shut you down.
- Holds a 15 second inhibitor before sleep so the session can lock first.
- Keeps Wi-Fi power save off on purpose. The shipped NetworkManager drop-in notes that it trades latency spikes for a fraction of a watt, and that some Intel BE200 and BE211 firmware drops the link when the radio naps.
- Disables zswap in favour of swap on zram, and skips the `plocate` index update while on battery.

On Intel laptops with a battery present, the install also adds `thermald` for Sandy Bridge and newer, and `intel-lpmd` for the hybrid cores in Alder Lake through Panther Lake. Both are gated on `omarchy-battery-present`, so desktops do not get them.

Hibernation is opt-in. `omarchy hibernation setup` creates a `/swap` btrfs subvolume with a RAM-sized swapfile, adds the `resume` mkinitcpio hook and the matching Limine kernel parameters, and installs a sleep hook that turns the keyboard backlight off before S4 because some ASUS keyboard controllers block the power-off with the LEDs lit.

## Known problems

The big one is drain, not reporting. When a laptop that used to get hours suddenly gets minutes, the usual cause is a discrete NVIDIA GPU that never enters a low power state. Issue #1776 is the long-running version of this and drew 29 reactions before it was closed with a pointer to the hybrid GPU toggle. Issue #8648, a GTX 1650 HP Pavilion that went from full to empty in ten minutes after the 4.0.0 update, is less clear-cut: the reporter later noted the pack has dead cells, and a second reporter with an HP Victus saw 20 percent gone in the same ten minutes. Omarchy 4.x ships `omarchy toggle hybrid gpu`, which drives `supergfxd` to park the dGPU in integrated mode, plus a sleep hook that re-parks it after a wake.

### Known issues

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#11990](https://github.com/omacom/omarchy/issues/11990) only the first battery pack is read | dual-battery ThinkPads, Surface Book 2 | open | not yet |
| [#10939](https://github.com/omacom/omarchy/issues/10939) low-battery warning suppressed while docked | any laptop drawing more than its dock supplies | open | not yet |
| [#9670](https://github.com/omacom/omarchy/issues/9670) low-battery warning repeats every few seconds | laptops whose USB-C PD line flaps at low charge | open | not yet |
| [#12005](https://github.com/omacom/omarchy/issues/12005) widget says Charging while discharging | MacBook Air M2 on Asahi | open | not yet |
| [#10344](https://github.com/omacom/omarchy/issues/10344), [#7374](https://github.com/omacom/omarchy/issues/7374) charge limit misreported | ASUS Zenbook, ThinkPads | open | not yet |
| [#6895](https://github.com/omacom/omarchy/issues/6895) power draw shows 0W | HP Pavilion Gaming 15-dk0xxx | open | not yet |
| [#8536](https://github.com/omacom/omarchy/issues/8536) power panel never opens without a battery | desktops and mini PCs with no battery | open, and the acceptance suite asserts the panel is hidden without battery hardware | not yet |
| [#8648](https://github.com/omacom/omarchy/issues/8648) very fast drain after updating to 4.0.0 | HP Pavilion and Victus gaming laptops, GTX 1650 | open | not yet |
| [#12095](https://github.com/omacom/omarchy/issues/12095) USB autosuspend drop-in is a no-op | Intel Bluetooth controllers | open | not yet |
| [#12096](https://github.com/omacom/omarchy/issues/12096) hibernation removal leaves resume parameters | Limine plus btrfs installs | open | not yet |
| [#12190](https://github.com/omacom/omarchy/issues/12190) `linux-omarchy` hangs entering suspend | Dell XPS 13 DX13260, Wildcat Lake | open | not yet |

A few of these are worth spelling out. The dual-battery bug is a single `head -n 1` in `omarchy-battery-status`; the bar icon uses UPower's aggregate device while the panel text uses the script, so the percentage above the progress bar and the bar itself can show different numbers at once. At least four unmerged pull requests propose the same fix, including PR #11750.

The warning bugs share one root. The low-battery check requires UPower's daemon-wide on-battery flag, not the battery device's own state, so a dock that supplies less power than the machine draws hides the warning entirely, and a flapping power line resets the already-warned latch on every event. One reporter logged roughly 260 critical popups over fourteen minutes before the machine died.

## Fixes that work

Work down this list.

1. Confirm what your hardware actually reports before blaming Omarchy. `upower -i $(upower -e | grep BAT | head -1)` and `cat /sys/class/power_supply/BAT*/power_now`. If UPower has the right number and the panel does not, it is a reporting bug, not a power bug.
2. For fast drain on a hybrid laptop, park the discrete GPU with `omarchy toggle hybrid gpu`. It installs `supergfxctl` if needed, switches the mode to Integrated and reboots. After the reboot, check with `cat /sys/bus/pci/devices/*/power/runtime_status` that the dGPU reads `suspended`.
3. Set the profile you want per power source explicitly: `omarchy powerprofiles set battery power-saver`. It sticks for that source across reboots.
4. For a laptop that only drains hard while asleep, the problem is suspend, not the battery. Read [suspend, sleep and resume](/hardware/suspend-sleep/) and [suspend will not resume](/fix/suspend-wont-resume-s2idle/).
5. For a charge limit, write `charge_control_end_threshold` yourself or use your vendor tool. There is no Omarchy toggle on 4.0.4; PR #12177 proposes one and is unmerged.
6. If you want deeper tuning than three profiles offer, community discussion #3907 documents replacing `power-profiles-daemon` with TLP. Remove or mask the daemon first, because the two fight over the same knobs and Omarchy's own profile commands stop working once it is gone.
7. If suspend started hanging on 4.0.4 specifically, boot the stock `linux` or `linux-lts` kernel from the Limine menu. The bespoke `linux-omarchy` kernel became the default boot entry in 4.0.4, and #12190 is a detailed open report of it hanging on suspend entry where stock `linux` 7.2.3 does not.

On 3.x the profile switching came from udev rules under `/etc/udev/rules.d/`. A 4.x migration removes the vulnerable versions of those rules, so do not expect to find them any more.

## Report it

Run `omarchy debug`, which collects `inxi -Farz`, `dmesg`, this boot's journal warnings and errors, and your package list, and offers to upload it. Add the output of `upower -d`, `powerprofilesctl`, `omarchy-battery-status --shell`, and `ls /sys/class/power_supply/`. For drain reports, add the runtime status of your GPU, or `powertop` output if you install it; Omarchy does not ship it. For anything involving a dock or charger, include the online state of every `Mains` and `USB` supply, because most of the warning bugs turn on exactly that.

Check the open issues first. Battery reporting has heavy duplication: the single dual-battery bug alone has more than ten separate reports.

## Related

- [Suspend, sleep and resume](/hardware/suspend-sleep/)
- [Battery drains fast](/fix/battery-drains-fast/)
- [Hybrid GPU laptops](/hardware/hybrid-gpu/)
- [Hibernate fails or hangs](/fix/hibernate-fails-or-hangs/)
- [`omarchy-battery-status`](/reference/commands/omarchy-battery-status/) and [`omarchy-powerprofiles-set`](/reference/commands/omarchy-powerprofiles-set/)
- [Omarchy manual: System sleep](https://omarchy.org/manual/system-sleep/)
