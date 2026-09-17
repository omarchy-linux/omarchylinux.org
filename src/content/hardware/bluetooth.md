---
title: "Bluetooth on Omarchy"
description: "What works and what breaks in Bluetooth on Omarchy 4.0.4: the rfkill power model, Quickshell panel bugs, BLE mouse reconnects, and the fix order."
answer: "Bluetooth itself works: BlueZ, the pairing agent, and A2DP audio are all set up for you. The breakage is in the 4.x panel. Turning Bluetooth off hides the widget, the panel can latch a stale off state, and its scan blocks BLE mice from reconnecting. Recover with omarchy bluetooth power on and omarchy restart shell."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "bluetooth"
issueCount: 148
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [bluetooth, bluez, quickshell, ble, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-bluetooth-power"
    title: "bin/omarchy-bluetooth-power at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-bluetooth-device"
    title: "bin/omarchy-bluetooth-device at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/bluetooth.sh"
    title: "install/hardware/bluetooth.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/systemd/user/bt-agent.service"
    title: "default/systemd/user/bt-agent.service at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/config/wireplumber/wireplumber.conf.d/bluetooth-a2dp-autoconnect.conf"
    title: "config/wireplumber/wireplumber.conf.d/bluetooth-a2dp-autoconnect.conf at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1786380259.sh"
    title: "migrations/1786380259.sh at v4.0.4"
    kind: commit
  - url: "https://github.com/omacom/omarchy/issues/6956"
    title: "Issue #6956: Bluetooth widget disappears from shell when turned off"
    kind: issue
    author: "elytraVIII"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7936"
    title: "Issue #7936: omarchy-bluetooth-power off: type-wide rfkill block trips platform switches and removes the radio from the USB bus (ThinkPad/Dell)"
    kind: issue
    author: "DrakeMorrison"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7573"
    title: "Issue #7573: Bluetooth panel latches \"Turned Off\" when the adapter powers up after quickshell, disabling GUI pairing and the toggle"
    kind: issue
    author: "martin-irwin"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/11739"
    title: "Issue #11739: omarchy.bluetooth panel cannot turn Bluetooth back on: rfkill removes the adapter, which hides the icon and the switch"
    kind: issue
    author: "m3ssage"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/10818"
    title: "Issue #10818: Bluetooth panel LE scan blocks reconnect of dual-channel BLE mice"
    kind: issue
    author: "stevepresley"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/11380"
    title: "Issue #11380: Bluetooth bar panel leaks discovery session, breaking LE device auto-reconnect"
    kind: issue
    author: "jturan"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/8962"
    title: "Issue #8962: bt-agent.service ExecCondition races bluetooth.service from the user manager, skipping the pairing agent for the whole boot"
    kind: issue
    author: "luizbafilho"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/11936"
    title: "Issue #11936: Bluetooth agent stays stale after bluetoothd restarts"
    kind: issue
    author: "n0mahd"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12095"
    title: "Issue #12095: omarchy-usb-autosuspend.conf is a no-op; Intel Bluetooth controllers still autosuspend (BLE HID reconnect timeouts)"
    kind: issue
    author: "jordanglean"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11683"
    title: "Issue #11683: Bluetooth headset volume partly disconnected from audio panel"
    kind: issue
    author: "wolf0403"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/12113"
    title: "Issue #12113: Bluetooth HFP microphone captures complete silence on OnePlus Bullets Wireless Z2 and JBL Tune 770NC"
    kind: issue
    author: "arsinghin"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12120"
    title: "Issue #12120: Internal Broadcom Bluetooth controller fails HCI reset after linux-omarchy 7.2.5-3 update (MacBookPro11,4)"
    kind: issue
    author: "akopitsa"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1744"
    title: "Issue #1744: Enable Bluetooth keyboard and mice at login screen"
    kind: issue
    author: "socket72"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/issues/1818"
    title: "Issue #1818: Bluetooth Audio Devices Doesn't Work"
    kind: issue
    author: "matheorism"
    date: "2025-09-19"
  - url: "https://github.com/omacom/omarchy/pull/5336"
    title: "PR #5336: Enable Bluetooth A2DP auto-connect in WirePlumber"
    kind: pr
    author: "dandresrp"
    date: "2026-05-07"
  - url: "https://github.com/omacom/omarchy/pull/7048"
    title: "PR #7048: Fix unreachable Bluetooth toggle when radio is off"
    kind: pr
    author: "tedwardd"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/pull/7065"
    title: "PR #7065: fix: ensure bluetooth panel stays visible when adapter is soft-blocked"
    kind: pr
    author: "elytraVIII"
    date: "2026-08-16"
  - url: "https://omarchy.org/manual/networking/"
    title: "Omarchy manual: Networking"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 Quattro"
    kind: release
    date: "2026-08-14"
credits:
  - name: "elytraVIII"
    url: "https://github.com/elytraVIII"
    for: "Tracing the vanishing Bluetooth widget to the adapter-null visibility check and opening a fix"
  - name: "oren"
    url: "https://github.com/oren"
    for: "Showing that a platform rfkill switch removes the radio from the USB bus entirely on a Dell Latitude 7440"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Identifying the type-wide rfkill block as the root cause and filing it separately"
  - name: "martin-irwin"
    url: "https://github.com/martin-irwin"
    for: "Pinning the latched Turned Off panel to a firmware-load race at shell startup"
  - name: "stevepresley"
    url: "https://github.com/stevepresley"
    for: "Documenting that an open panel scan blocks BLE mice from reconnecting"
  - name: "erikvanzijst"
    url: "https://github.com/erikvanzijst"
    for: "Showing that Chrome FIDO discovery can hold the same stuck scan the panel gets blamed for"
  - name: "jturan"
    url: "https://github.com/jturan"
    for: "Retracting a panel report after finding a third-party AirPods daemon owned the leaked scan"
  - name: "igouss"
    url: "https://github.com/igouss"
    for: "Finding the missing volumeStep on BlueZ routes behind the dead output slider"
  - name: "jordanglean"
    url: "https://github.com/jordanglean"
    for: "Proving the shipped usbcore autosuspend drop-in cannot apply to a builtin module"
  - name: "techfg"
    url: "https://github.com/techfg"
    for: "Getting a Bluetooth keyboard to unlock LUKS with mkinitcpio-bluetooth"
faq:
  - q: "I turned Bluetooth off and the icon disappeared. How do I turn it back on?"
    a: "Run omarchy bluetooth power on in a terminal, or rfkill unblock bluetooth. The off path soft-blocks the radio, BlueZ then deletes the adapter object, and the widget hides itself because it is gated on that adapter existing. This is issue #6956, still open on 4.0.4."
  - q: "Why does my Logitech MX mouse stop reconnecting?"
    a: "An active LE scan blocks the connect. Close the Bluetooth panel, then check busctl --system get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Discovering. If it is still true, some other client owns the scan, and omarchy bluetooth power off followed by on clears it."
  - q: "Can I type my LUKS passphrase on a Bluetooth keyboard?"
    a: "Not with the stock setup. The radio is not up in the initramfs. Use a 2.4 GHz receiver, or add the AUR package mkinitcpio-bluetooth to your hooks as described in issue #1744. Omarchy does not ship or support that path."
related: [audio, suspend-sleep, wifi]
draft: false
---

Bluetooth in Omarchy 4.x is stock BlueZ with a Quickshell panel in front of it. The BlueZ half is quiet. The panel half accounts for most of the open complaints, and several of them end with a working radio that the user interface insists is off.

This page was checked against v4.0.4, released 2026-09-15, using the v4.0.4 source tree. The counter in the sidebar covers every Bluetooth-matching issue and discussion in the tracker, open and closed, so read it as traffic rather than as current breakage.

## Status on 4.0.4

Pairing, A2DP audio, BLE mice and keyboards, and Xbox controllers all work on ordinary hardware. What is unreliable is the control surface:

- Turning Bluetooth **off** from the bar removes the only control that can turn it back on (issue #6956, open).
- The panel can show **Turned Off** while the adapter is powered and connected, and its switch then does nothing (issue #7573, open).
- An **open panel scans continuously**, and that scan blocks bonded BLE mice from reconnecting (issue #10818, open).
- The pairing agent can be **skipped for a whole boot** on a race, with no sign of it in the interface (issue #8962, open).

None of these has shipped a fix. The 4.0.1 through 4.0.4 release notes carry no Bluetooth entries at all, and both candidate panel fixes are still open pull requests.

## What Omarchy does automatically

**Installs and enables the stack.** `bluez`, `bluez-tools` and `bluez-utils` are in the base package list, and `install/hardware/bluetooth.sh` enables `bluetooth.service`.

**Holds the power state in rfkill.** Since 4.0.0, on and off go through `omarchy-bluetooth-power`, which blocks or unblocks the radio rather than touching BlueZ `Powered`. The reasoning is in the script: BlueZ never persists `Powered`, while systemd-rfkill saves every switch under `/var/lib/systemd/rfkill` and restores it at the next boot. A migration in 4.0.0 carries old installs across and reverts the `AutoEnable=false` line Omarchy used to write, which had only ever meant Bluetooth came up off on every boot.

**Runs an auto-accept pairing agent.** `bt-agent.service` is a user unit, enabled at first run, that registers `bt-agent -c NoInputNoOutput`. Pair requests are auto-accepted, which is safe only because the adapter is pairable while you have the panel open and scanning.

**Auto-connects A2DP.** A WirePlumber drop-in sets `bluez5.auto-connect` to `a2dp_sink` and `a2dp_source` for every `bluez_card`. That landed in v3.8.0 from PR #5336 by dandresrp and closed the long-running "Bluetooth audio does not work" report, issue #1818.

**Gives you a CLI.** `omarchy bluetooth power on|off|toggle|is-on` and `omarchy bluetooth device pair|connect|disconnect|forget <address>`. The device helper powers the radio up first, trusts the device, and caps each `bluetoothctl` call at 20 seconds.

There is no hardware quirk script for Bluetooth beyond `install/hardware/bluetooth.sh`. T2 Macs get their Broadcom firmware and the `hci_bcm4377` module from `install/hardware/apple/fix-t2.sh`, and Xbox controllers get `xpadneo-dkms` from the menu installer.

**Where 3.x differed.** Up to v3.8.4 the interface was the bluetui terminal app launched from Waybar, `main.conf` carried `AutoEnable=false`, and there was no per-device panel. Everything described here as a panel bug is new in 4.0.0.

## Known problems

| Issue | Models seen | Status | Fixed in |
| --- | --- | --- | --- |
| [#6956](https://github.com/omacom/omarchy/issues/6956) widget vanishes when Bluetooth is turned off | any adapter | open, PRs #7048 and #7065 unmerged | not yet |
| [#7936](https://github.com/omacom/omarchy/issues/7936) type-wide rfkill block trips platform switches | Dell Latitude 7440, ThinkPad E16 Gen 1 | open | not yet |
| [#7573](https://github.com/omacom/omarchy/issues/7573) panel latched at "Turned Off" | Intel 8087:0a2b, ThinkPad E16 Gen 2 (RTL8852BU) | open, upstream Quickshell cache | not yet |
| [#11739](https://github.com/omacom/omarchy/issues/11739) panel cannot turn Bluetooth back on | Intel Haswell desktop, 4.0.3 | open | not yet |
| [#10818](https://github.com/omacom/omarchy/issues/10818) LE scan blocks BLE mouse reconnect | MX Master 3S, MX Anywhere 3S, EM01 NL | open | not yet |
| [#8962](https://github.com/omacom/omarchy/issues/8962) pairing agent skipped on boot race | Intel i7-8700K, AX211 laptops | open | not yet |
| [#11936](https://github.com/omacom/omarchy/issues/11936) agent stale after bluetoothd restart | MacBook Air M1 | open | not yet |
| [#12095](https://github.com/omacom/omarchy/issues/12095) usbcore autosuspend drop-in is a no-op | Intel AX201 and similar | open | not yet |
| [#11683](https://github.com/omacom/omarchy/issues/11683) output slider does not move a BlueZ sink | Shokz OpenRun Pro, Kanto YU4 | open, upstream quickshell#807 | not yet |
| [#12113](https://github.com/omacom/omarchy/issues/12113) HFP microphone records silence | OnePlus Bullets Z2, JBL Tune 770NC and 780NC | open, not Omarchy specific | not yet |
| [#12120](https://github.com/omacom/omarchy/issues/12120) Broadcom HCI reset fails on linux-omarchy 7.2.5-3 | MacBookPro11,4 | open, one report | not yet |
| [#1818](https://github.com/omacom/omarchy/issues/1818) Bluetooth audio devices do not work | various | closed | v3.8.0 |
| [#1744](https://github.com/omacom/omarchy/issues/1744) no Bluetooth keyboard at the LUKS prompt | any | closed, by design | not a bug |

Two cautions on the LE reconnect cluster. First, a stuck scan is often not the panel's: jturan filed #11380 against it, then closed it after finding a third-party AirPods daemon held an unbounded discovery session, and erikvanzijst traced the same signature to Chrome starting a FIDO discovery and never stopping it. Second, `StopDiscovery` answering "No discovery started" while `Discovering` stays true looks identical in all three cases.

## Fixes that work

Go in this order.

1. **Bring the radio back.** `omarchy bluetooth power on`, or `rfkill unblock bluetooth`. This is the answer to the vanished widget. On a Dell or ThinkPad with a platform rfkill switch it may not be enough, because the block removed the radio from the USB bus, and only suspend and resume or a reboot re-enumerates it.
2. **Restart the shell.** `omarchy restart shell` is the only cure for a panel latched at "Turned Off". A fresh process re-reads the adapter state.
3. **Close the panel before expecting a BLE device to reconnect.** Then check `busctl --system get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Discovering`. If it is still true with the panel closed, something else owns the scan. Look at Chromium and at any third-party Bluetooth plugin or daemon.
4. **Power cycle the adapter.** `omarchy bluetooth power off` then `on` clears a stuck scan that `StopDiscovery` refuses to clear.
5. **Check the pairing agent before blaming the device.** `systemctl --user status bt-agent.service`. "Skipped due to exec-condition" means no agent registered for this boot, and `bluetoothd` will log `No agent available for request type 2` on every confirmation. Fix it with `systemctl --user restart bt-agent.service`, and do the same after any `bluetooth.service` restart.
6. **Use the CLI when the panel will not cooperate.** `omarchy bluetooth device pair <address>` does the pair, trust and connect sequence that the panel does. Plain `bluetoothctl` works too.
7. **Restart the subsystem from the menu.** _Update > Hardware > Bluetooth_ runs `omarchy-restart-bluetooth`. Note what it actually does despite its name: it unblocks rfkill and prints `rfkill list bluetooth`. It does not restart `bluetooth.service`, so run `sudo systemctl restart bluetooth` yourself if that is what you want.
8. **Suspect the kernel last.** `journalctl -b | grep -i hci0`. A controller that never initialises, such as `BCM: Reset failed (-110)`, is a firmware or kernel problem, not a panel one. 4.0.4 makes `linux-omarchy` the default, so booting the stock Arch kernel entry in Limine is a clean way to test that.

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, `dmesg`, the current boot's warnings and errors from the journal, and the full package list. Add `--no-sudo` to skip `dmesg`, or `--print` to read it in the terminal.

For a Bluetooth report, add the four things triage always asks for and the log does not make obvious:

- `bluetoothctl show` and `rfkill list bluetooth`, together, so power state and block state can be compared.
- `busctl --system get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Powered` and the same for `Discovering`. This is what separates a genuinely off adapter from a panel showing the wrong thing.
- The controller's USB ID from `lsusb` and the firmware lines from `journalctl -b | grep -i hci0`.
- `systemctl --user status bt-agent.service` if pairing is what failed.

If the panel disagrees with `busctl`, say so explicitly and say whether `omarchy restart shell` fixed it. That distinction is what turned issue #7573 from a vague report into a located upstream bug.

## Related

- [Audio](/hardware/audio/) for the PipeWire and WirePlumber side of headsets.
- [Suspend and sleep](/hardware/suspend-sleep/) when the adapter comes back wrong after a resume.
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/) for that specific failure.
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/) when the whole bar is gone, not just the Bluetooth icon.
- [Omarchy commands](/reference/commands/) for the full `omarchy bluetooth` group.
- The official manual covers the panel in [networking](https://omarchy.org/manual/networking/) and [the top bar](https://omarchy.org/manual/the-top-bar/).
