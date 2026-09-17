---
title: "Wi-Fi on Omarchy"
description: "Wi-Fi on Omarchy 4.x runs on NetworkManager. What works out of the box, the quirk scripts Omarchy ships, the Broadcom and enterprise bugs, and the fix order."
answer: "Wi-Fi on Omarchy 4.x is NetworkManager plus the Quickshell network panel on Super + Ctrl + W. Intel, MediaTek and Qualcomm cards generally work on a fresh install. Broadcom Wi-Fi in Intel Macs and enterprise 802.1X networks are the two weak spots. First move for a dead link is omarchy restart-wifi, then check your regulatory domain with iw reg get."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "wifi"
issueCount: 235
tags: [wifi, networkmanager, broadcom, iwlwifi, 802.1x, hardware]
sources:
  - url: "https://github.com/omacom/omarchy/issues/1414"
    title: "Issue #1414: Use NetworkManager instead of systemd-networkd"
    kind: issue
    author: "kromsam"
    date: "2025-09-02"
  - url: "https://github.com/omacom/omarchy/issues/11745"
    title: "Issue #11745: BCM43602 on 2015-2017 Intel Macs associates but has no connectivity until iw reg set <country>"
    kind: issue
    author: "Clowdyffs"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/9019"
    title: "Issue #9019: BCM43602 (pre-T2 2017 MacBook Pro): feature_disable=0x82000 is not enough, regulatory domain is also required"
    kind: issue
    author: "benjarlett"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/11859"
    title: "Issue #11859: BCM4360: Wi-Fi goes dark, toggle won't recover it"
    kind: issue
    author: "in0vik"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11613"
    title: "Issue #11613: BCM43602 WiFi signal extremely weak (-90 dBm) on MacBook Pro 2015-2017"
    kind: issue
    author: "andyholst"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/11791"
    title: "Issue #11791: Network panel's enterprise WiFi reconnect flow overwrites a working profile and misreports failures as wrong password"
    kind: issue
    author: "pixelsandpointers"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11985"
    title: "Issue #11985: Network Panel shows NOT CONNECTED for active 802.1x Enterprise (eduroam) networks"
    kind: issue
    author: "Pabl0125"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/12028"
    title: "Issue #12028: Bar network icon shows disconnected while Wi-Fi is actually connected."
    kind: issue
    author: "fils"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11961"
    title: "Issue #11961: Captive portal sign-in button uses a hardcoded URL most portals won't recognize"
    kind: issue
    author: "daffelito"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11812"
    title: "Issue #11812: WiFi auto-connects to 2.4GHz instead of preferring 5GHz on fresh install"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11813"
    title: "Issue #11813: WiFi does not reconnect automatically after it disconnects"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/pull/6652"
    title: "PR #6652: Apply the Broadcom Wi-Fi quirk to Macs without a T2"
    kind: pr
    author: "cupatea"
    date: "2026-08-10"
  - url: "https://github.com/omacom/omarchy/pull/6334"
    title: "PR #6334: Connect to enterprise (802.1X) Wi-Fi networks from the network panel"
    kind: pr
    author: "KazeTachinuu"
    date: "2026-07-24"
  - url: "https://github.com/omacom/omarchy/pull/7238"
    title: "PR #7238: Fix passwordless OWE Wi-Fi handling"
    kind: pr
    author: "dhh"
    date: "2026-08-17"
  - url: "https://omarchy.org/manual/networking/"
    title: "Omarchy manual: Networking"
    kind: manual
credits:
  - name: "cupatea"
    url: "https://github.com/cupatea"
    for: "Extending the brcmfmac firmware-supplicant quirk to every Mac whose Wi-Fi brcmfmac drives, not just T2 models"
  - name: "benjarlett"
    url: "https://github.com/benjarlett"
    for: "Tracing pre-T2 MacBook association failures to an unset cfg80211 regulatory domain"
  - name: "KazeTachinuu"
    url: "https://github.com/KazeTachinuu"
    for: "Adding 802.1X enterprise connect support to the network panel"
  - name: "pixelsandpointers"
    url: "https://github.com/pixelsandpointers"
    for: "Finding that the panel's enterprise reconnect rebuilds the profile and mislabels timeouts as a wrong password"
faq:
  - q: "Does Omarchy still use iwd and impala?"
    a: "No. Omarchy 4.0.0 switched Wi-Fi to NetworkManager and replaced impala with the Quickshell network panel. The hardware setup script actively disables iwd and systemd-networkd on every run, so a machine upgraded from 3.x ends up on NetworkManager too."
  - q: "Why does my Wi-Fi say connected but nothing loads?"
    a: "On Broadcom Macs this is usually the regulatory domain. Run iw reg get. If it prints country 00, set your country in /etc/conf.d/wireless-regdom, or for brcmfmac hardware set options cfg80211 ieee80211_regdom=XX in /etc/modprobe.d and rebuild the boot image."
  - q: "How do I force 5GHz?"
    a: "Run omarchy network band 5. It pins the band on the NetworkManager profile rather than a BSSID, so roaming between access points still works. omarchy network band auto undoes it."
  - q: "Is eduroam supported?"
    a: "It connects, but the 4.0.x panel has open bugs around it. Build the profile with nmcli once, then bring it up with nmcli connection up rather than re-entering credentials in the panel."
related: [wifi-drops-after-kernel-update-iwlwifi, bluetooth, t2-mac, apple-macbook-pro-intel, tailscale-not-connecting]
draft: false
---

Wi-Fi is one of the subsystems Quattro rewrote from the ground up. Everything below was checked against the v4.0.4 source tree and against issues filed in September 2026.

## Status on 4.0.4

For mainstream laptop radios, Wi-Fi is boring in the good way. Intel AX and BE cards, MediaTek MT7921 and MT7925, and Qualcomm parts associate during the ISO install and keep working. The component carries 235 tracked issues, 117 of them still open, and the open ones cluster hard in two places: Broadcom Wi-Fi in Intel Macs, and WPA2-Enterprise or 802.1X networks.

The stack itself changed in 4.0.0. Omarchy 3.x used iwd with the impala TUI. Issue [#1414](https://github.com/omacom/omarchy/issues/1414), filed by kromsam in September 2025 and one of the most upvoted requests in the tracker, argued that iwd could not carry desktop reality: VPN clients, eduroam, Enhanced Open. Quattro switched to NetworkManager and replaced impala, bluetui and wiremix with Quickshell panels. The network panel is `Super + Ctrl + W`. See the manual chapter on [networking](https://omarchy.org/manual/networking/).

## What Omarchy does automatically

Several things run at install time and again whenever hardware setup is re-run.

`install/hardware/network.sh` disables `iwd.service`, disables every `systemd-networkd` unit, and masks `systemd-networkd-wait-online.service`. It also hunts down the stock DHCP files archinstall used to drop (`20-ethernet.network`, `20-wlan.network`, `20-wwan.network`), checks that they are unmodified, and moves them into a timestamped backup directory under `/etc/systemd/network/`. That is why a 3.x machine that upgrades still lands on NetworkManager. `install/config/enable-services.sh` enables `NetworkManager.service` and masks `NetworkManager-wait-online.service` so nothing in the session blocks on DHCP.

`install/hardware/set-wireless-regdom.sh` derives a two-letter country from your timezone (falling back to `zone.tab`) and writes `WIRELESS_REGDOM` into `/etc/conf.d/wireless-regdom`. It deliberately does not run `iw reg set` live, because install is followed by a reboot. `wireless-regdb` is in the base package list, which is what makes 6GHz legal on cards that support it.

Three quirk scripts target specific radios:

- `install/hardware/fix-bcm43xx.sh` looks for PCI IDs `14e4:43a0` and `14e4:4331` (BCM4360 in 2013 to 2015 Macs, BCM4331 in 2012 era Macs) and installs `broadcom-wl-dkms`. 4.0.3 switched this to the DKMS package after Arch dropped the prebuilt module.
- `install/hardware/apple/fix-brcmfmac-supplicant.sh` writes `options brcmfmac feature_disable=0x82000`, which turns off Broadcom's firmware supplicant and authenticator so `wpa_supplicant` runs the four-way handshake in software. Without it, a Mac against a WPA2/WPA3 transition-mode access point associates, never finishes the handshake, and NetworkManager reports a wrong password. cupatea's [PR #6652](https://github.com/omacom/omarchy/pull/6652) widened the trigger from the T2 bridge ID to the brcmfmac PCI IDs, so BCM43602, BCM4350, BCM4355, BCM4364, BCM4377, BCM4378 and BCM4387 all get it. BCM4360 is intentionally excluded because it runs the out-of-tree `wl` driver.
- `install/hardware/intel/fix-wifi7-eht.sh` writes `options iwlwifi disable_11be=Y` for Intel BE200 and BE211 (`8086:e440`, `8086:272b`), because the EHT receive path drops those links to a crawl. The comment in the script says to remove it once Intel fixes the driver.

On the command side you get `omarchy restart-wifi` (rfkill unblock, radio on, rescan), `omarchy network status`, `omarchy network band`, `omarchy network qr`, `omarchy network password`, `omarchy network speedtest`, and `omarchy dns`. First login runs `nm-online` before deciding you have no Wi-Fi, so an Ethernet machine no longer gets a spurious setup prompt.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#11745](https://github.com/omacom/omarchy/issues/11745) Associates but no traffic until `iw reg set` | BCM43602 Intel Macs 2015-2017 | Open | not fixed |
| [#9019](https://github.com/omacom/omarchy/issues/9019) Association fails, regdom never set | MacBookPro14,3 and similar | Open, workaround verified | not fixed |
| [#11859](https://github.com/omacom/omarchy/issues/11859) Wi-Fi dies after long uptime, toggle will not recover | BCM4360 MacBook Air 2017 | Open | not fixed |
| [#11613](https://github.com/omacom/omarchy/issues/11613) Signal pinned near -90 dBm | MacBookPro13,3 and 2015-2017 siblings | Open | not fixed |
| [#11791](https://github.com/omacom/omarchy/issues/11791) Enterprise reconnect rebuilds profile, reports wrong password | any 802.1X, eduroam | Open | not fixed |
| [#11985](https://github.com/omacom/omarchy/issues/11985) Panel header says NOT CONNECTED while connected | any 802.1X, eduroam | Open | not fixed |
| [#12028](https://github.com/omacom/omarchy/issues/12028) Bar icon shows disconnected while connected | eduroam, many BSSIDs | Open | not fixed |
| [#11961](https://github.com/omacom/omarchy/issues/11961) Captive portal button opens a URL portals ignore | any | Open | not fixed |
| [#11812](https://github.com/omacom/omarchy/issues/11812) Joins 2.4GHz when 5GHz shares the SSID | ASUS Vivobook, MT7902 | Open, workaround | not fixed |
| [#11813](https://github.com/omacom/omarchy/issues/11813) No automatic reconnect after a drop | ASUS Vivobook, MT7902 | Open | not fixed |
| [#1806](https://github.com/omacom/omarchy/issues/1806) Cannot connect at all, brcmfmac | MacBook Pro 2020 | Open since the 3.x iwd era | not fixed |

The Broadcom Mac cluster is the one to take seriously. Clowdyffs on a MacBookPro14,1 found in [#11745](https://github.com/omacom/omarchy/issues/11745) that Wi-Fi showed connected with 100 percent packet loss until `sudo iw reg set US`. benjarlett went further in [#9019](https://github.com/omacom/omarchy/issues/9019): on a MacBookPro14,3 the firmware-supplicant quirk alone was not enough, because `cfg80211` had no regulatory hint source at all and sat in the world domain until beacon hints accumulated, which took roughly 47 minutes. andyholst's [#11613](https://github.com/omacom/omarchy/issues/11613) is separate again, a signal-strength problem he attributes to generic NVRAM data rather than the antenna tuning those machines need. Be careful reading that issue: the pull request it links is a Cirrus Logic audio patch and was closed without merging, so nothing has shipped for it.

The enterprise cluster is newer and is all panel logic, not driver logic. [#11791](https://github.com/omacom/omarchy/issues/11791) reports that the panel's enterprise connect path always adds a fresh profile hardcoded to PEAP with MSCHAPv2, no CA certificate and an eight second auth timeout, then maps that timeout to "Wrong password" and reprompts. If your institution's CAT installer already created a working profile, the panel can bury it.

## Fixes that work

Work down this list. Stop when you are online.

1. `omarchy restart-wifi`, or _Update > Hardware > Wi-Fi_ in the menu. It unblocks rfkill, turns the radio back on and rescans. This clears most "it worked ten minutes ago" cases.
2. Check the regulatory domain: `iw reg get`. A `country 00` line means you are in the world domain, which on Broadcom hardware often means association or traffic failure. Put your country in `/etc/conf.d/wireless-regdom` and reboot.
3. On a Mac with brcmfmac, if step 2 alone does not hold, add `options cfg80211 ieee80211_regdom=XX` in `/etc/modprobe.d/cfg80211.conf`, rebuild the Limine boot image with `sudo limine-mkinitcpio`, and reboot. This is the workaround benjarlett verified across a cold reboot.
4. Confirm the Mac quirk is present: `cat /etc/modprobe.d/brcmfmac.conf` should show `feature_disable=0x82000`. Machines installed before 4.0.0 may not have it.
5. Slow or flaky on a dual-band SSID: `omarchy network band 5`. It refuses bands the access point is not answering on, and reverts if the radio cannot come back up.
6. Enterprise networks: build the profile once with `nmcli`, matching your institution's documented EAP method, then bring it up with `nmcli connection up <name>`. Avoid re-entering credentials in the panel until [#11791](https://github.com/omacom/omarchy/issues/11791) is resolved.
7. Captive portals: if the sign-in button does nothing, open `http://captive.apple.com` or `http://connectivitycheck.gstatic.com/generate_204` in your browser to force the redirect.
8. If a kernel or firmware update broke a previously working card, that is its own path. See [wifi drops after a kernel update](/fix/wifi-drops-after-kernel-update-iwlwifi/) and the [release channels](/releases/channels/) page. 4.0.4 makes the bespoke `linux-omarchy` kernel the default boot entry on every machine, so a regression that appeared on 2026-09-15 is worth testing against the stock kernel.

## Report it

Run `omarchy debug`. It writes `/tmp/omarchy-debug.log` with `inxi -Farz`, full `dmesg`, and the current boot's warnings and errors from the journal. That log carries your PCI IDs, driver, firmware version and kernel, which is what triage needs first.

Add three things by hand, because they are what every Wi-Fi thread ends up asking for: `lspci -nn | grep -i net` for the exact PCI ID, `iw reg get` for the regulatory domain, and `iw dev <iface> link` for signal and negotiated rate. `omarchy network status --verbose` prints interface, address, gateway, SSID, signal in dBm, bitrate and ping in one go. If the failure is intermittent, say how long the machine had been up, as in0vik did in [#11859](https://github.com/omacom/omarchy/issues/11859). File at [github.com/omacom/omarchy/issues](https://github.com/omacom/omarchy/issues) and say whether Ethernet works, since that separates a radio problem from a DNS or firewall problem.

## Related

- [Bluetooth](/hardware/bluetooth/), which shares a chip with Wi-Fi on most combo cards
- [T2 Macs](/hardware/t2-mac/) and [Intel MacBook Pro](/hardware/apple-macbook-pro-intel/) for the Broadcom story in full
- [Wi-Fi drops after a kernel update](/fix/wifi-drops-after-kernel-update-iwlwifi/)
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/)
- [Tailscale not connecting](/fix/tailscale-not-connecting/)
- [What replaces what in Quattro](/reference/changes/)
