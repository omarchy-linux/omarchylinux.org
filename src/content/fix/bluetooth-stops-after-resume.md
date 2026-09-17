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
  - url: "https://github.com/omacom/omarchy/issues/10142"
    title: "Issue #10142: Bluetooth panel: unbounded StartDiscovery retry wedges the controller and kills LE background scanning"
    kind: issue
    author: "bukson"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/pull/10176"
    title: "PR #10176: Bound the Bluetooth panel's discovery retry"
    kind: pr
    author: "omarchybot"
    date: "2026-09-04"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "JareckiB12"
    url: "https://github.com/JareckiB12"
    for: "Instrumented the resume and caught the last Powered write going to false while BlueZ was still powering the controller up"
  - name: "spaceXrace"
    url: "https://github.com/spaceXrace"
    for: "First showed the Turned Off latch is reached from resume, not just from a boot race"
  - name: "zelti"
    url: "https://github.com/zelti"
    for: "Reproduced the latch on a controller the kernel resets in place, proving it does not need a USB re-enumeration"
  - name: "mhbnielsen"
    url: "https://github.com/mhbnielsen"
    for: "Confirmed a bluetooth.service restart clears the stuck discovery flag with no re-pairing"
  - name: "iuliansafta"
    url: "https://github.com/iuliansafta"
    for: "Traced the stuck Discovering flag to BlueZ 5.87 and explained why only an adapter power cycle resets it"
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
    a: "No. Check whether the adapter is stuck in discovery. Leaving the Bluetooth panel open holds an LE scan that blocks bonded LE devices from connecting, the panel can fail to stop that scan when it closes, and another program such as a browser passkey prompt can leave one behind too."
related: [suspend-wont-resume-s2idle, quickshell-crashes-or-bar-missing, wifi-drops-after-kernel-update-iwlwifi, battery-drains-fast]
draft: false
---

Bluetooth going quiet after a suspend is one problem name covering at least three different faults on Omarchy 4. Work through them in order. The first one is by far the most common, and it does not involve the radio at all.

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

The panel picks up the live BlueZ state again, the toggle works, and paired devices show up. This is the fix for the panel reading `Turned Off` while everything underneath is fine, reported in [#7573](https://github.com/omacom/omarchy/issues/7573) and [#9561](https://github.com/omacom/omarchy/issues/9561). You lose nothing but the shell process. Expect to repeat it after future resumes; no fix had shipped in Omarchy or Quickshell as of 4.0.4. One reporter on #9561 resyncs the panel without a shell restart by cycling rfkill, `rfkill block bluetooth && sleep 0.5 && rfkill unblock bluetooth`, but on ThinkPads and some Dells a type-wide block can drop the radio off the USB bus (see below), so prefer the shell restart there.

**3. If the adapter is gone, unblock then restart bluez.**

```bash
omarchy restart bluetooth
sudo systemctl restart bluetooth.service
```

Note what the first command actually does in 4.0.4: it runs `rfkill unblock bluetooth` and prints the rfkill table. Despite the name and the menu entry under _Update > Hardware > Bluetooth_, it does not restart the service. That is why the second line is there. If the controller still does not appear, the hardware-specific recoveries are in the last section. Reloading `btusb` is not one of them: on the threads where people tried it, the controller came back in the same broken state.

**4. If paired mice or keyboards will not reconnect, check for a stuck scan.**

```bash
busctl --system get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Discovering
```

If that says `true` with the Bluetooth panel closed, the adapter is pinned in discovery and bonded LE devices cannot get back in. Power cycle the adapter:

```bash
bluetoothctl power off && sleep 1 && bluetoothctl power on
```

That is what most reporters on [#10818](https://github.com/omacom/omarchy/issues/10818) used, and the mouse or keyboard reconnected afterwards with no re-pairing. One reporter used `sudo systemctl restart bluetooth.service` instead with the same result. `bluetoothctl scan off` and `omarchy restart shell` do not clear it. Keep the panel closed while switching a multi-host mouse or keyboard back to this machine.

**5. If pairing fails after bluetooth.service restarted.**

```bash
systemctl --user restart bt-agent.service
```

[#11936](https://github.com/omacom/omarchy/issues/11936) shows why: the pairing agent registers with one `bluetoothd` process, and when that process is replaced, including by the restart in steps 3 and 4, the new daemon has no agent while systemd still reports `bt-agent.service` as healthy. The reporter's fix relaunches the agent whenever the `org.bluez` owner changes; restarting the unit by hand does the same once.

## Verify it worked

```bash
bluetoothctl show | grep -E 'Powered|Discovering'
bluetoothctl devices Connected
```

You want `Powered: yes`, `Discovering: no` with the panel closed, and your device listed as connected. Then open the panel with `Super + Ctrl + B` and confirm it agrees with those numbers. Suspend and resume once more and check again, because the panel fault only reappears on a resume.

## Why it happens

Three separate mechanisms produce the same complaint.

**The panel holds a stale power state.** On many controllers a resume tears the adapter down and brings it back, reloading firmware as it goes. BlueZ reports the adapter as not powered during that window, then powers it up. In Quickshell 0.3.1 the Bluetooth adapter object takes a one-time property snapshot and subscribes to later changes, and the completion event can land in the gap between those two moments. Nothing re-reads the value afterwards. JareckiB12 instrumented a resume on [#7573](https://github.com/omacom/omarchy/issues/7573) and found the final recorded write set the powered flag to false while BlueZ itself reported the controller as on four minutes later. The panel then renders `Turned Off`, its device list stays empty, and its switch sends the on command forever.

**The adapter is stuck in discovery.** While the panel is open it re-asserts discovery every second. On close it tries to stop it, but gives up after three attempts, and an active scan aborts the LE connects that bonded mice and keyboards need to come back. Reporters on [#10818](https://github.com/omacom/omarchy/issues/10818) found the same stuck `Discovering: true` on Intel 8265, AX200, AX210, a PCIe Intel controller and a MediaTek MT7922, so it is not chipset specific, but the panel is not always the owner. One reporter traced the leaked session to a Chrome passkey prompt, and another showed that in BlueZ 5.87 a failed `StopDiscovery` leaves the flag set with no client owning it, so every later stop is refused with `No discovery started` and only powering the adapter down resets it. A related storm, [#10142](https://github.com/omacom/omarchy/issues/10142), has the panel's one-second start retry wedging a Realtek RTL8761BU until the kernel resets it; the patch bounding that retry, [#10176](https://github.com/omacom/omarchy/pull/10176), was still open as of 4.0.4.

**The controller is genuinely suspended or wedged.** Omarchy ships `/etc/modprobe.d/omarchy-usb-autosuspend.conf` containing `options usbcore autosuspend=-1`, and [#12095](https://github.com/omacom/omarchy/issues/12095) shows it cannot take effect, because `usbcore` is built into the kernel. The per-device setting comes from a udev rule instead, so Intel controllers keep runtime suspending and BLE reconnects time out.

Worth knowing about the on and off path: 4.0.0 moved the remembered Bluetooth power state into the rfkill soft block, since BlueZ never persisted it. The 4.0.0 migration also reverts the old `AutoEnable=false` line in `/etc/bluetooth/main.conf`. On 3.x you got bluetui and a Waybar module instead of a Quickshell panel, so the stale panel fault does not exist there, though the wedged controller cases do.

## If that did not work

Pin the Intel controller on with a udev rule, using your own vendor and product IDs from `lsusb`:

```
ACTION=="add|bind|change", SUBSYSTEM=="usb", ATTR{idVendor}=="8087", ATTR{idProduct}=="0026", ATTR{power/control}="on"
```

Save that as `/etc/udev/rules.d/61-bluetooth-no-autosuspend.rules`. This is the rule jordanglean verified on [#12095](https://github.com/omacom/omarchy/issues/12095).

On ThinkPads and some Dells, turning Bluetooth off through the panel can cut USB power to the module rather than just soft blocking it, so the adapter vanishes from the bus entirely. [#7936](https://github.com/omacom/omarchy/issues/7936) documents the mechanism. On some models `rfkill unblock bluetooth` re-enumerates the module; on two X1 Carbons it did not, and what brought the radio back was rebinding the xHCI controller that owns the port: `echo -n 0000:00:14.0 > /sys/bus/pci/drivers/xhci_hcd/unbind`, wait a few seconds, then the same into `bind`, with your own PCI address from `lspci`. Expect the webcam and fingerprint reader on that controller to drop for a moment. Elsewhere only a suspend and resume, or a reboot, brings it back.

On T2 MacBooks with the BCM4377 combo chip, Bluetooth and suspend fail together, and the reporter on [#11264](https://github.com/omacom/omarchy/issues/11264) needed the Wi-Fi and Bluetooth modules unloaded before sleep and Wi-Fi reloaded about 15 seconds after wake, since reloading it immediately crashed the machine. See [/hardware/t2-mac/](/hardware/t2-mac/). A separate report, [#12120](https://github.com/omacom/omarchy/issues/12120), has a Broadcom controller failing its HCI reset after the 4.0.4 `linux-omarchy` kernel, with `Bluetooth: hci0: command 0x0c03 tx timeout` in the journal. There, reloading `btusb` reproduced the failure and only a full USB re-enumeration of the port, writing 0 then 1 to that device's `authorized` file under `/sys/bus/usb/devices/`, cleared it for the boot. Both were open and unfixed at the time of writing.

If Bluetooth audio specifically dies on resume, [#11280](https://github.com/omacom/omarchy/issues/11280) traces a WirePlumber crash in the PipeWire bluez plugin right after S3 resume. Systemd restarted the service on its own within a second, and the headset still failed to connect, so restarting WirePlumber by hand is unlikely to help. The fault is upstream in PipeWire and the thread records no workaround.

## Related

- [/hardware/bluetooth/](/hardware/bluetooth/) for controller by controller status
- [/hardware/suspend-sleep/](/hardware/suspend-sleep/) if the machine itself struggles to sleep or wake
- [/fix/quickshell-crashes-or-bar-missing/](/fix/quickshell-crashes-or-bar-missing/) if the whole bar is wrong, not just the Bluetooth part
- [/reference/commands/omarchy-bluetooth-power/](/reference/commands/omarchy-bluetooth-power/) for what the toggle actually runs
- The Omarchy manual's [Troubleshooting](https://omarchy.org/manual/troubleshooting/) chapter points at _Update > Hardware > Bluetooth_ as the first thing to try, which is the rfkill unblock in step 3
