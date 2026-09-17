---
title: "Printer not found on Omarchy"
description: "Your printer no longer appears by itself on Omarchy 4.0.2 and later. Add it by hand in Print Settings, or with lpadmin, and pick the right CUPS driver."
answer: "Omarchy 4.0.2 removed cups-browsed, so nothing is discovered automatically any more. Open Print Settings from the app launcher, choose Add, and wait for the scan. If the printer is still missing, add it manually as Network Printer, Internet Printing Protocol (ipp), using its IP and the queue ipp/print. Make sure cups.service is running first."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: apps
issueCount: 6
errorStrings:
  - "lpstat: No destinations added."
  - "lpstat: Scheduler is not running."
  - 'printer-state-message="universal filter failed."'
  - "Temporary failure in name resolution"
tags: [printer, cups, avahi, ipp, printing]
sources:
  - url: "https://omarchy.org/manual/faq/"
    title: "Omarchy manual, FAQ: How do I add a printer?"
    kind: manual
  - url: "https://github.com/omacom/omarchy/pull/8951"
    title: "PR #8951: Temporarily remove automatic printer discovery"
    kind: pr
    author: "omarchybot"
    date: "2026-08-29"
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
  - url: "https://github.com/omacom/omarchy/issues/11814"
    title: "Issue #11814: HP Smart Tank 520/540 USB printer not plug-and-play: driverless queue always fails (universal filter failed), hplip not shipped"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11186"
    title: "Issue #11186: Printing from Firefox to a local USB HP printer produces PJL garbage + blank pages after cups-browsed is removed in 4.0.3"
    kind: issue
    author: "docPoacher"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/3790"
    title: "Issue #3790: GUI applications freeze when attempting to print (CUPS works via command line)"
    kind: issue
    author: "clwalker85"
    date: "2025-12-06"
  - url: "https://github.com/omacom/omarchy/issues/9311"
    title: "Issue #9311: The update breaks the edits in /etc/nsswitch.conf"
    kind: issue
    author: "ramzlab000"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/256"
    title: "Issue #256: Add Avahi for mDNS network discovery as core package"
    kind: issue
    author: "danfascia"
    date: "2025-07-20"
  - url: "https://github.com/omacom/omarchy/discussions/250"
    title: "Discussion #250: Guide - Install HP Printer"
    kind: discussion
    author: "curtisspendlove"
    date: "2025-07-20"
  - url: "https://github.com/omacom/omarchy/discussions/4667"
    title: "Discussion #4667: Printer Setup"
    kind: discussion
    author: "SeanGSR"
    date: "2026-02-20"
  - url: "https://github.com/omacom/omarchy/pull/9406"
    title: "PR #9406: Let cups-browsed removal proceed when CUPS isn't running"
    kind: pr
    author: "Chessing234"
    date: "2026-08-31"
credits:
  - name: "joselberg"
    url: "https://github.com/joselberg"
    for: "Pinned the migration failure to lpstat reporting a stopped scheduler"
  - name: "rafaelclima"
    url: "https://github.com/rafaelclima"
    for: "Showed LC_ALL=C does not force English for lpstat, which breaks the same migration on non-English locales"
  - name: "HIMANSHU11827"
    url: "https://github.com/HIMANSHU11827"
    for: "Worked out the hplip PPD and device URI that makes an HP Smart Tank print after the driverless queue fails"
  - name: "docPoacher"
    url: "https://github.com/docPoacher"
    for: "Isolated the libcupsfilters 2.2 page-drop with a single-package downgrade test"
  - name: "EERomeo"
    url: "https://github.com/EERomeo"
    for: "Found that reinstalling cups, cups-filters and libcups together unfreezes GUI print dialogs"
faq:
  - q: "Why did my printer disappear after updating to 4.0.2?"
    a: "The update removes cups-browsed, which was the service that created queues for discovered printers by itself. Queues it had generated are deleted by migration 1788009111 unless they have pending jobs. Printers you added by hand are left alone. Add the missing one again from Print Settings and it will stay."
  - q: "Do I still need avahi?"
    a: "Yes, if you want to reach a printer by its .local name or let the Add dialog find it over mDNS. avahi-daemon.service is enabled at install time, and the shipped /etc/nsswitch.conf keeps mdns_minimal in the hosts line."
  - q: "Can I print to a PDF without a printer?"
    a: "Yes. The manual FAQ says printing to a PDF file works with no printer configured, through the print dialog's own file output. Note that 4.0.2 also dropped the cups-pdf package, so there is no longer a PDF queue listed alongside real printers."
related: [migration-failed-mid-update, omarchy-update-fails-or-hangs, pacnew-and-pacsave-files-after-update, tailscale-not-connecting]
draft: false
---

Since Omarchy 4.0.2 your printer does not show up on its own. That is deliberate, not a bug. Automatic discovery was pulled out and the manual now tells you to add each printer yourself. Everything below was checked against the 4.0.2, 4.0.3 and 4.0.4 source trees and the 3.8.4 tree for comparison.

## The fix

1. Confirm the print scheduler is up. A fresh install enables it, but some machines end up with it inactive, which is what issue #9377 reports.

   ```bash
   systemctl status cups.service
   sudo systemctl enable --now cups.service
   ```

2. For a USB printer, check that the kernel sees it at all before blaming CUPS.

   ```bash
   lsusb
   lpinfo -v
   ```

   `lpinfo -v` lists every backend and device CUPS can reach. A USB printer shows as a `usb://` or `hp:/usb/` line.

3. Open _Print Settings_ from the app launcher with `Super + Space`. Choose _Add_ and give the scan a few seconds. USB printers and most network printers turn up here.

4. If it is still not listed, add it by address. In the _Add_ dialog pick _Network Printer_, then _Internet Printing Protocol (ipp)_, and enter the printer's IP with a queue of `ipp/print`. The printer's own panel or its web page tells you the address. The manual FAQ walks through the same path.

   The command line equivalent, if you prefer it:

   ```bash
   sudo lpadmin -p Office -E -v ipp://192.168.1.50/ipp/print -m everywhere
   sudo lpadmin -d Office
   ```

   `-m everywhere` is the driverless IPP Everywhere profile. `lpadmin -d` sets the default queue that apps reach for first.

5. If you want to reach the printer by name instead of by IP, check that mDNS works.

   ```bash
   systemctl status avahi-daemon.service
   getent hosts myprinter.local
   avahi-browse -rt _ipp._tcp
   ```

   `avahi-browse` is in the `avahi` package, which Omarchy ships. If `getent` fails while `avahi-browse` finds the printer, the problem is the `hosts:` line in `/etc/nsswitch.conf`, not the printer.

6. Pick the driver last. A modern printer works best on driverless IPP Everywhere. An older one wants the model's own driver, which usually means an extra package. For HP hardware that is `hplip`, which Omarchy does not ship.

## Verify it worked

```bash
lpstat -t
lp -d Office /usr/share/cups/data/testprint
lpstat -o
```

`lpstat -t` should say the scheduler is running and show your queue as idle and accepting requests. `lpstat -o` should empty out as the job finishes. If the queue prints from `lp` but not from apps, skip to the GUI freeze note below, because that is a different fault.

## Why it happens

Omarchy 4.0.1 and everything before it shipped `cups-browsed`, which watched the network and created queues for printers it found. The 4.0.2 release listed "Temporarily remove automatic printer discovery" under Deprecations, from PR #8951. Comparing the package lists in the source tree, `cups-browsed` and `cups-pdf` are present through v4.0.1 and gone from v4.0.2 onward, replaced by `cups-pk-helper`. The manual FAQ changed with it: 4.0.1 said a network printer is usually already discovered, and 4.0.2 onward says you add each printer yourself.

Migration `1788009111` does the removal on existing machines. It disables `cups-browsed.service`, deletes the queues that service generated, which are the ones with an `implicitclass://` device URI, and then drops the package. Queues with jobs waiting are left for you. Queues you added yourself are not touched.

`cups`, `cups-filters`, `cups-pk-helper`, `avahi`, `nss-mdns` and `system-config-printer` are all still in the base package list on 4.0.4, and the installer enables both `cups.service` and `avahi-daemon.service`. So the plumbing is there. Only the discovery layer is missing.

On 3.x, and on 4.0.0 and 4.0.1, a printer that vanished was usually an mDNS problem instead. Issue #256 asked for avahi as a core package, and a commenter there described `.local` names failing to resolve while CUPS hung trying to use them. That was addressed by PR #1021, merged well before 4.x.

## If that did not work

**The update itself fails on this migration.** If `omarchy update` stops with `lpstat: Scheduler is not running.`, that is issue #9377. The migration only expects a running scheduler or the exact English string `lpstat: No destinations added.`, so a stopped CUPS aborts it, and because the marker is written on the last line the failure repeats on every retry. A commenter's workaround is to start `cups.socket` and `cups.service`, run the update again so the migration completes and writes its marker, then stop CUPS again. PR #9406 proposed handling the stopped scheduler, but it was closed without being merged, and the check is still unhandled in the 4.0.4 tree.

**The same migration fails on a non-English system.** Issue #9640 shows the string check failing under `pt_BR.UTF-8` because `LC_ALL=C` does not override `LANGUAGE` for gettext, so `lpstat` still answers in Portuguese. The reporter notes `LC_MESSAGES=C` does force English. Same workaround applies: complete the removal by hand, then let the migration marker be written.

**Print dialogs freeze while `lp` works.** Issue #3790, closed in January 2026, is a mixed set of CUPS libraries rather than a missing printer. Two people confirmed that reinstalling the three packages together and restarting the scheduler fixes it:

```bash
sudo pacman -S cups cups-filters libcups --overwrite='*'
sudo systemctl restart cups
```

**An HP inkjet fails every job with `universal filter failed.`** Issue #11814 covers an HP Smart Tank on a driverless queue. The reporter's verified fix installs `hplip` plus `gutenprint`, disables `ipp-usb` because it fights the kernel `usblp` driver, and rebuilds the queue against the hplip PPD and an `hp:/usb/...` device URI. Discussion #250 is a longer community guide for HP hardware along the same lines. This is still open, so treat it as a workaround.

**Pages come out blank or full of PJL text.** Issue #11186 traced that to `libcupsfilters` moving to 2.2.x while `cups-filters` stayed at 2.0.1, and the reporter fixed it by downgrading `libcupsfilters` alone and restarting CUPS. Open, and worth checking before you rebuild a queue that was working yesterday.

**`.local` names break after an update.** Issue #9311 and its comments describe `nss-mdns` ordering in `/etc/nsswitch.conf` being reset by updates, with mDNS answering before `/etc/hosts` is consulted. This is still open. If you keep local hostnames in `/etc/hosts`, expect to reapply your ordering after updates that touch the avahi package set.

Evidence on printers is thinner than on most Omarchy topics. The printer cluster holds six issues and seven discussions, and none of the printing issues open today has a merged fix.

## Related

- Manual chapter: [FAQ, How do I add a printer?](https://omarchy.org/manual/faq/)
- [/hardware/printer/](/hardware/printer/) for the component overview
- [/switch/printers-and-scanners/](/switch/printers-and-scanners/) if you are coming from macOS or Windows
- [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/) if migration 1788009111 blocked your update
- [/reference/changes/](/reference/changes/) for what else 4.x removed
