---
title: "Printers and scanners on Omarchy"
description: "How printing works on Omarchy 4.0.4: CUPS and avahi ship enabled, you add each printer by hand in Print Settings, and scanning needs SANE installed."
answer: "Printing is installed and running on every Omarchy 4.x machine, but since 4.0.2 nothing is discovered automatically. Open Print Settings from Super + Space, choose Add, and pick your printer. Modern printers work on the driverless IPP Everywhere profile. Scanning ships nothing at all, so install sane, sane-airscan and a scan app yourself."
appliesTo:
  from: "4.0.2"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [printing, scanning, cups, avahi, sane, hardware]
sources:
  - url: "https://omarchy.org/manual/faq/"
    title: "Omarchy Manual: FAQ, How do I add a printer?"
    kind: manual
  - url: "https://github.com/omacom/omarchy/pull/8951"
    title: "PR #8951: Temporarily remove automatic printer discovery"
    kind: pr
    author: "omarchybot"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Omarchy v4.0.2 release notes"
    kind: release
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/11186"
    title: "Issue #11186: Printing from Firefox to a local USB HP printer produces PJL garbage + blank pages after cups-browsed is removed in 4.0.3"
    kind: issue
    author: "docPoacher"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11814"
    title: "Issue #11814: HP Smart Tank 520/540 USB printer not plug-and-play: driverless queue always fails (universal filter failed), hplip not shipped"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/9377"
    title: "Issue #9377: Migration 1788009111 fails when CUPS scheduler is not running"
    kind: issue
    author: "joselberg"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9640"
    title: "Issue #9640: 1788009111.sh fails on pt_BR (and other non-English locales)"
    kind: issue
    author: "rafaelclima"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/9406"
    title: "PR #9406: Let cups-browsed removal proceed when CUPS isn't running (closed unmerged)"
    kind: pr
    author: "Chessing234"
    date: "2026-09-16"
credits:
  - name: "docPoacher"
    url: "https://github.com/docPoacher"
    for: "Isolated the dropped-page regression to a libcupsfilters version bump rather than the discovery removal"
  - name: "HIMANSHU11827"
    url: "https://github.com/HIMANSHU11827"
    for: "Documented an hplip PPD workaround for an HP Smart Tank inkjet that fails on the driverless queue"
  - name: "joselberg"
    url: "https://github.com/joselberg"
    for: "Traced a failed update to the printer migration running with the CUPS scheduler stopped"
  - name: "rafaelclima"
    url: "https://github.com/rafaelclima"
    for: "Found that the printer migration parses an English-only lpstat string"
  - name: "arkmpm"
    url: "https://github.com/arkmpm"
    for: "Confirmed the stopped-scheduler failure blocks the rest of the update and verified the start-CUPS-then-retry workaround"
faq:
  - q: "Why does my printer no longer appear by itself after updating to 4.0.2 or later?"
    a: "Automatic discovery was removed on purpose in 4.0.2. Fresh installs no longer get the cups-browsed daemon, and updated machines lose it through a migration. Add the printer once in Print Settings and it stays."
  - q: "Does Omarchy ship a Print to PDF printer?"
    a: "Not since 4.0.2. The cups-pdf package was dropped for security reasons: CUPS ran its backend as root, and a print job could steer what that backend executed afterwards. Use the application's own Print to File option in the print dialog instead."
  - q: "Can I scan out of the box?"
    a: "No. Nothing scanner related is in the base package set on 4.0.4. Install sane, sane-airscan and a front end such as simple-scan yourself."
  - q: "Do I need sudo to add a printer?"
    a: "In Print Settings, no. It asks through polkit using cups-pk-helper. From the terminal, yes: the desktop user is not a CUPS administrator any more, so lpadmin and lpinfo need sudo."
related: [day-one-checklist, what-replaces-what]
draft: false
---

Printing on Omarchy is ordinary Arch printing with one large change made in 4.0.2. The stack is installed and running for you. The discovery daemon that used to make network printers appear on their own is gone. So the practical answer is: everything works, but you add each printer once, by hand.

Checked against v4.0.4, released 2026-09-15.

## What ships and what does not

The base package set on 4.0.4 contains `cups`, `cups-filters`, `cups-pk-helper`, `system-config-printer` (the app the launcher calls Print Settings), plus `avahi` and `nss-mdns`. The installer enables `cups.service` and `avahi-daemon.service` in `install/config/enable-services.sh`, and the shipped `/etc/nsswitch.conf` puts `mdns_minimal` ahead of DNS on the hosts line, so a printer advertising itself as `something.local` resolves.

Nothing for scanning ships. There is no `sane`, no `sane-airscan`, no `simple-scan`, no `ipp-usb` and no `hplip` in the base package list. Scanning is a manual install, covered further down.

## Add a printer

1. Press `Super + Space` and launch Print Settings.
2. Choose _Add_ and give it several seconds. A USB printer that is plugged in and powered on, and most network printers, are found during that probe.
3. If yours is not listed, pick _Network Printer > Internet Printing Protocol (ipp)_ and type the address. Get it from the printer's front panel or its web interface. It is usually a plain IP with a queue path of `ipp/print`.
4. _Forward_ offers a driver. The manual's advice is to leave a modern printer on the driverless _IPP Everywhere_ profile and to give an older one its model driver.
5. Right-click the finished printer and choose _Set as Default_. Paper size, duplex and print quality are under _Properties_.

Print Settings asks for your password through polkit when it needs administrator rights. That is `cups-pk-helper` doing its job.

From a terminal, the same thing needs `sudo`, because the desktop user's `wheel` group is no longer a CUPS `SystemGroup`:

```bash
sudo lpinfo -v
sudo lpadmin -p Office -E -v ipp://192.168.1.50/ipp/print -m everywhere
sudo lpadmin -d Office
```

## Verify it worked

```bash
systemctl is-active cups
lpstat -r
lpstat -v
echo "Omarchy test page" | lp -d Office
lpstat -W completed -o
```

`lpstat -r` should answer that the scheduler is running, and `lpstat -v` should list your queue with its device URI. To see what your network is actually advertising, use avahi directly:

```bash
avahi-browse -rt _ipp._tcp
```

One result that looks like a failure is not one. Running `lpinfo -v` without `sudo` returns `Forbidden`. That is the intended 4.0.2 hardening, and the project's own acceptance test asserts it.

## Why discovery is off

Omarchy 4.0.2, released 2026-08-31, lists "Temporarily remove automatic printer discovery" under Deprecations. PR #8951 took `cups-browsed` out of the default package set and added migration `1788009111`, which stops and removes the daemon on machines that already had it, clears idle discovery queues, and leaves manually added IPP and USB printers in place. The same release dropped `cups-pdf`, because CUPS launched its backend as root and a print job could influence the command that backend ran afterwards, and added `cups-pk-helper` so printer administration goes through polkit instead of a privileged group.

That is a real behaviour change between point releases. On 3.8.4 and on 4.0.0 and 4.0.1, `cups-browsed` was installed and enabled, so network printers tended to show up unprompted. From 4.0.2 onward they do not. The hardened discovery configuration still sits in the repository, unused, which is a fair signal that the project intends to bring discovery back rather than drop it for good.

If `omarchy update` itself failed at this migration rather than after it, there are two known causes: it exits nonzero when the CUPS scheduler is not running (#9377), and it fails on non-English locales because it matches an English `lpstat` string while `LANGUAGE` overrides `LC_ALL` (#9640). Both were still open when this page was checked, the 4.0.4 migration script still only recognises the English `No destinations added.` message, and the pull request that addressed the stopped-scheduler case (#9406) was closed without being merged on 2026-09-16. Because the migration runner stops at the first failure, a machine hitting either bug also skips every later update step until the migration passes. For the stopped-scheduler case a second reporter on #9377 confirmed a workaround: start `cups.socket` and `cups.service`, rerun `omarchy update`, then stop them again if you do not want CUPS running.

## If that did not work

**Jobs print one good page then garbage or blanks, on a USB HP printer.** Issue #11186 reports exactly this after updating to 4.0.3, printing from Firefox to an HP LaserJet over the `hp` backend. The reporter first suspected the discovery removal, then isolated it with a single-variable test to a `libcupsfilters` upgrade from 2.1.1-4 to 2.2.1-2 while `cups-filters` stayed at 2.0.1-2. Downgrading the library and restarting CUPS fixed it for them. The issue is open and this is a reporter's finding, not a confirmed upstream diagnosis, so treat it as a lead rather than a rule. If it matches your symptoms, check your versions first with `pacman -Q cups-filters libcupsfilters`.

**Every job fails with `universal filter failed` or `pdftopdf stopped with status 1`.** That is the driverless profile failing on a printer that is not really an IPP Everywhere device. Issue #11814 covers an HP Smart Tank inkjet where the only offered option was the broken driverless queue. The reporter's fix was to install `hplip` and the Gutenprint PPD database, then recreate the queue against an `hpcups` PPD. `hplip` is not shipped by default, so this is the general shape of the answer for older or oddball printers: install the vendor driver package, then re-add the printer and pick the model's own driver at step 4 instead of IPP Everywhere.

**No Print to PDF printer.** There is not one any more. Use the print dialog's own Print to File, which every GTK and browser print dialog offers.

## Scanning

Nothing scanner related is installed, so start from scratch:

```bash
sudo pacman -S sane sane-airscan simple-scan
scanimage -L
```

`sane-airscan` is the piece that matters for anything modern. It speaks eSCL and WSD over the network, which is the scanning equivalent of driverless printing, and it means most recent all-in-one devices work without a vendor driver. `avahi-daemon` is already running, which is what airscan uses to find them. If `scanimage -L` lists your device, `simple-scan` will too.

USB-only scanners are less predictable. Device permissions come from the udev rules the `sane` package installs, and an HP all-in-one generally wants `hplip` as well. We have not tested a USB scanner on 4.0.4 hardware, and there are no open Omarchy issues about scanning at all, so that part is standard Arch behaviour rather than anything Omarchy specific.

## What to watch for on newer versions

The next release is announced as Quattro RS 4.5. Automatic discovery was removed as a temporary measure, and the 4.0.4 tree still carries `etc/cups/cups-browsed.conf`, a sysusers file for a dedicated `cups-browsed` account and a locked-down service drop-in, none of which anything installs. That is the strongest hint about what comes next: discovery coming back in a hardened form. If it does, network printers may start appearing on their own again and any queue you added by hand will simply sit alongside them.
