---
title: "Bluetooth stops working after suspend on Omarchy"
description: "Bluetooth dead, stuck on Turned Off, or paired mice not reconnecting after resume on Omarchy 4. The shell restart, the bluez restart, and the firmware cases."
answer: "Most of the time the radio is fine and only the bar panel is wrong. Run `bluetoothctl show`; if it reports Powered yes while the panel says Turned Off, run `omarchy restart shell` and the panel resyncs. If the adapter is genuinely gone, run `omarchy restart bluetooth` then `sudo systemctl restart bluetooth.service`."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: network
issueCount: 181
errorStrings:
  - "Turned Off"
  - "No default controller available"
  - "org.bluez.Error.Failed le-connection-abort-by-local"
  - "Failed to stop discovery on adapter"
  - "Bluetooth: hci0: command 0x0c03 tx timeout"
tags: [bluetooth, suspend, resume, quickshell, bluez]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7573"
    title: "Issue #7573: Bluetooth panel latches \"Turned Off\" when the adapter powers up after quickshell, disabling GUI pairing and the toggle"
    kind: issue
    author: "martin-irwin"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/9561"
    title: "Issue #9561: Bluetooth bar toggle can remain visually off after resume while adapter is powered"
    kind: issue
    author: "Matt1656"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10818"
    title: "Issue #10818: Bluetooth panel LE scan blocks reconnect of dual-channel BLE mice"
    kind: issue
    author: "stevepresley"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/12095"
    title: "Issue #12095: omarchy-usb-autosuspend.conf is a no-op; Intel Bluetooth controllers still autosuspend (BLE HID reconnect timeouts)"
    kind: issue
    author: "jordanglean"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11936"
    title: "Issue #11936: Bluetooth agent stays stale after bluetoothd restarts"
    kind: issue
    author: "n0mahd"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/7936"
    title: "Issue #7936: omarchy-bluetooth-power off: type-wide rfkill block trips platform switches and removes the radio from the USB bus (ThinkPad/Dell)"
    kind: issue
    author: "DrakeMorrison"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11280"
    title: "Issue #11280: WirePlumber SIGSEGV in PipeWire Bluetooth plugin immediately after S3 resume"
    kind: issue
    author: "AnoopLamba"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11264"
    title: "Issue #11264: MacBook Air 2020 (MacBookAir9,1, T2): Bluetooth never powers on at boot, and suspend always fails on brcmfmac D3 timeout"
    kind: issue
    author: "austinsomer"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/12120"
    title: "Issue #12120: Internal Broadcom Bluetooth controller fails HCI reset after linux-omarchy 7.2.5-3 update (MacBookPro11,4)"
    kind: issue
    author: "akopitsa"
    date: "2026-09-16"
  - url: "https://omarchy.org/manual/networking/"
    title: "Omarchy manual: Networking"
    kind: manual
credits:
  - name: "JareckiB12"
    url: "https://github.com/JareckiB12"
    for: "Instrumented the resume and caught the last Powered write going to false while BlueZ was still powering the controller up"
  - name: "zelti"
    url: "https://github.com/zelti"
    for: "Showed the Turned Off latch is reached from resume, not just from a boot race"
  - name: "hermes-os"
    url: "https://github.com/hermes-os"
    for: "Confirmed the shell restart clears it on Broadcom btusb hardware"
  - name: "DrakeMorrison"
    url: "https://github.com/DrakeMorrison"
    for: "Traced the type-wide rfkill block cutting USB power to the module on ThinkPads"
  - name: "jordanglean"
    url: "https://github.com/jordanglean"
    for: "Showed the shipped usbcore autosuspend file cannot apply and wrote the udev rule that does"
faq:
  - q: "Do I have to reboot to get Bluetooth back after suspend?"
    a: "Almost never. On Omarchy 4 the usual cause is the bar panel holding a stale power state, and `omarchy restart shell` fixes that without touching the radio. If the adapter itself is wedged, restarting bluetooth.service is the next step and a reboot is the last one."
  - q: "Why does clicking the Bluetooth toggle do nothing after I wake the laptop?"
    a: "Because the panel thinks Bluetooth is off, so every click sends the on command instead of the off command. That command runs `rfkill unblock bluetooth` on an already unblocked radio, which changes nothing. The journal fills with repeated unblock lines."
  - q: "My mouse stays paired but will not reconnect after idle or resume. Is the bond broken?"
    a: "No. Check whether the adapter is stuck in discovery. Leaving the Bluetooth panel open holds an LE scan that blocks bonded LE devices from connecting, and the panel can fail to stop that scan when it closes."
related: [suspend-wont-resume-s2idle, quickshell-crashes-or-bar-missing, wifi-drops-after-kernel-update-iwlwifi, battery-drains-fast]
draft: false
---

Bluetooth going quiet after a suspend is one problem name covering at least four different faults on Omarchy 4. Work through them in order. The first one is by far the most common, and it does not involve the radio at all.

## The fix

Checked on 4.0.4. Steps 1 and 2 apply to 4.0.0 and later only, since the Quickshell Bluetooth panel arrived in 4.0.0 (Quattro).

**1. Find out whether the radio is actually down.**

```bash
bluetoothctl show | grep -E 'Powered|PowerState'
rfkill list bluetooth
omarchy bluetooth power is-on; echo "exit $?"
```

If you get `Powered: yes`, `PowerState: on`, no soft or hard block, and exit 0, the radio is alive and the bar is lying to you. Go to step 2. If `bluetoothctl show` prints `No default controller available`, skip to step 3.

**2. Restart the Omarchy shell.**

```bash
omarchy restart shell
```

The panel picks up the live BlueZ state again, the toggle works, and paired devices show up. This is the fix for the panel reading `Turned Off` while everything underneath is fine, reported in [#7573](https://github.com/omacom/omarchy/issues/7573) and [#9561](https://github.com/omacom/omarchy/issues/9561). You lose nothing but the shell process. Expect to repeat it after future resumes until the upstream fix lands.

**3. If the adapter is gone, unblock then restart bluez.**

```bash
omarchy restart bluetooth
sudo systemctl restart bluetooth.service
```

Note what the first command actually does in 4.0.4: it runs `rfkill unblock bluetooth` and prints the rfkill table. Despite the name and the menu entry under _Update > Hardware > Bluetooth_, it does not restart the service. That is why the second line is there. If the controller still does not appear, reload the USB driver:

```bash
sudo modprobe -r btusb && sudo modprobe btusb
```

**4. If paired mice or keyboards will not reconnect, check for a stuck scan.**

```bash
busctl --system get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Discovering
```

If that says `true` with the Bluetooth panel closed, the adapter is pinned in discovery and bonded LE devices cannot get back in. `sudo systemctl restart bluetooth.service` clears it immediately, and several reporters on [#10818](https://github.com/omacom/omarchy/issues/10818) confirmed the device reconnects afterwards with no re-pairing. Keep the panel closed while switching a multi-host mouse or keyboard back to this machine.

**5. If pairing fails after bluez restarted on its own.**

```bash
systemctl --user restart bt-agent.service
```

**6. If a Bluetooth headset or speaker is connected but silent.**

```bash
systemctl --user restart wireplumber
```

## Verify it worked

```bash
bluetoothctl show | grep -E 'Powered|Discovering'
bluetoothctl devices Connected
```

You want `Powered: yes`, `Discovering: no` with the panel closed, and your device listed as connected. Then open the panel with `Super + Ctrl + B` and confirm it agrees with those numbers. Suspend and resume once more and check again, because the panel fault only reappears on a resume.

## Why it happens

Three separate mechanisms produce the same complaint.

**The panel holds a stale power state.** On many controllers a resume tears the adapter down and brings it back, reloading firmware as it goes. BlueZ reports the adapter as not powered during that window, then powers it up. In Quickshell 0.3.1 the Bluetooth adapter object takes a one-time property snapshot and subscribes to later changes, and the completion event can land in the gap between those two moments. Nothing re-reads the value afterwards. JareckiB12 instrumented a resume on [#7573](https://github.com/omacom/omarchy/issues/7573) and found the final recorded write set the powered flag to false while BlueZ itself reported the controller as on four minutes later. The panel then renders `Turned Off`, its device list stays empty, and its switch sends the on command forever.

**The panel leaks its discovery session.** While the panel is open it re-asserts discovery every second. On close it tries to stop it, but gives up after three attempts. When those attempts are swallowed, the adapter stays in active inquiry, which starves the passive background scan that bonded LE mice and keyboards rely on to get reconnected. Reporters on [#10818](https://github.com/omacom/omarchy/issues/10818) hit this on Intel 8265, AX200, AX210, a PCIe Intel controller and a MediaTek MT7922, so it is not chipset specific. A bounding patch is proposed but had not shipped as of 4.0.4.

**The controller is genuinely suspended or wedged.** Omarchy ships `/etc/modprobe.d/omarchy-usb-autosuspend.conf` containing `options usbcore autosuspend=-1`, and [#12095](https://github.com/omacom/omarchy/issues/12095) shows it cannot take effect, because `usbcore` is built into the kernel. The per-device setting comes from a udev rule instead, so Intel controllers keep runtime suspending and BLE reconnects time out.

Worth knowing about the on and off path: 4.0.0 moved the remembered Bluetooth power state into the rfkill soft block, since BlueZ never persisted it. The 4.0.0 migration also reverts the old `AutoEnable=false` line in `/etc/bluetooth/main.conf`. On 3.x you got bluetui and a Waybar module instead of a Quickshell panel, so the stale panel fault does not exist there, though the wedged controller cases do.

## If that did not work

Pin the Intel controller on with a udev rule, using your own vendor and product IDs from `lsusb`:

```
ACTION=="add|bind|change", SUBSYSTEM=="usb", ATTR{idVendor}=="8087", ATTR{idProduct}=="0026", ATTR{power/control}="on"
```

Save that as `/etc/udev/rules.d/61-bluetooth-no-autosuspend.rules`. This is the rule jordanglean verified on [#12095](https://github.com/omacom/omarchy/issues/12095).

On ThinkPads and some Dells, turning Bluetooth off through the panel can cut USB power to the module rather than just soft blocking it, so the adapter vanishes from the bus entirely. [#7936](https://github.com/omacom/omarchy/issues/7936) documents the mechanism and notes hardware where only a suspend and resume, or a reboot, brings it back.

On T2 MacBooks with the BCM4377 combo chip, Bluetooth and suspend fail together, and the reporter on [#11264](https://github.com/omacom/omarchy/issues/11264) needed the Wi-Fi and Bluetooth modules unloaded before sleep and reloaded a few seconds after wake. See [/hardware/t2-mac/](/hardware/t2-mac/). A separate report, [#12120](https://github.com/omacom/omarchy/issues/12120), has a Broadcom controller failing its HCI reset after the 4.0.4 `linux-omarchy` kernel, with `Bluetooth: hci0: command 0x0c03 tx timeout` in the journal. Both were open and unfixed at the time of writing.

If Bluetooth audio specifically dies on resume, [#11280](https://github.com/omacom/omarchy/issues/11280) traces a WirePlumber crash in the PipeWire bluez plugin right after S3 resume. Systemd restarts the service, but the device can be left disconnected.

## Related

- [/hardware/bluetooth/](/hardware/bluetooth/) for controller by controller status
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) if the machine itself struggles to sleep or wake
- [/fix/quickshell-crashes-or-bar-missing/](/fix/quickshell-crashes-or-bar-missing/) if the whole bar is wrong, not just the Bluetooth part
- [/reference/commands/omarchy-bluetooth-power/](/reference/commands/omarchy-bluetooth-power/) for what the toggle actually runs
- The Omarchy manual covers the panel in [Networking](https://omarchy.org/manual/networking/) and [Troubleshooting](https://omarchy.org/manual/troubleshooting/)
