---
title: "Printers and printing on Omarchy"
description: "CUPS ships enabled on Omarchy 4.0.4, but automatic printer discovery was removed in 4.0.2 and no HP or scanner drivers ship. What works and what to install."
answer: "CUPS and Avahi are installed and enabled on Omarchy 4.0.4, so printing works once you add the queue yourself in Print Settings. Automatic network discovery was removed in 4.0.2 with cups-browsed. No hplip, gutenprint or SANE packages ship, so HP inkjets and all scanners need manual package installs. Driverless IPP Everywhere queues work best on modern printers."
appliesTo:
  from: "4.0.0"
kind: component
componentKey: "printer"
status: partial
issueCount: 46
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [printer, cups, printing, hplip, avahi, scanner]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/omarchy-base.packages"
    title: "install/omarchy-base.packages at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/config/enable-services.sh"
    title: "install/config/enable-services.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1788009111.sh"
    title: "migrations/1788009111.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1787815267.sh"
    title: "migrations/1787815267.sh at v4.0.4"
    kind: commit
    date: "2026-09-15"
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
  - url: "https://github.com/omacom/omarchy/pull/9406"
    title: "PR #9406: Let cups-browsed removal proceed when CUPS isn't running"
    kind: pr
    author: "Chessing234"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/9650"
    title: "PR #9650: Force English lpstat messages in cups-browsed migration"
    kind: pr
    author: "Chessing234"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/12101"
    title: "PR #12101: Cups-browsed migration: locale-safe empty queue and CUPS-down"
    kind: pr
    author: "Chessing234"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11186"
    title: "Issue #11186: Printing from Firefox to a local USB HP printer produces PJL garbage + blank pages"
    kind: issue
    author: "docPoacher"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11814"
    title: "Issue #11814: HP Smart Tank 520/540 USB printer not plug-and-play (universal filter failed)"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
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
  - url: "https://github.com/omacom/omarchy/discussions/250"
    title: "Discussion #250: Guide - Install HP Printer"
    kind: discussion
    author: "curtisspendlove"
    date: "2025-07-20"
  - url: "https://github.com/omacom/omarchy/discussions/10417"
    title: "Discussion #10417: Add a default picture-printing dialog and right-click Print action"
    kind: discussion
    author: "jonnyace"
    date: "2026-09-06"
  - url: "https://omarchy.org/manual/faq/"
    title: "Omarchy Manual: FAQ, How do I add a printer?"
    kind: manual
    date: "2026-09-16"
credits:
  - name: "joselberg"
    url: "https://github.com/joselberg"
    for: "Traced the failed 1788009111 migration to lpstat reporting a stopped scheduler"
  - name: "rafaelclima"
    url: "https://github.com/rafaelclima"
    for: "Showed that LC_ALL=C does not force English for lpstat, breaking the migration on non-English locales"
  - name: "docPoacher"
    url: "https://github.com/docPoacher"
    for: "Isolated the blank-page regression to libcupsfilters 2.2.x by single-variable downgrade"
  - name: "HIMANSHU11827"
    url: "https://github.com/HIMANSHU11827"
    for: "Documented the working hplip PPD setup for HP Smart Tank USB printers"
  - name: "EERomeo"
    url: "https://github.com/EERomeo"
    for: "Found the cups reinstall that unfreezes GUI print dialogs"
faq:
  - q: "Why does my network printer no longer appear by itself?"
    a: "Omarchy 4.0.2 removed cups-browsed and its automatic discovery. Add the printer once in Print Settings, by IPP address if it is not found by the Add wizard. The manual FAQ says discovery is off while it is reworked."
  - q: "Does Omarchy ship scanner support?"
    a: "No. There is no sane, simple-scan or xsane package in install/omarchy-base.packages at v4.0.4. Scanning needs packages you install yourself, and multifunction HP devices need hplip too."
  - q: "My update stops at \"Temporarily remove automatic printer discovery\". What now?"
    a: "That is migration 1788009111. Start CUPS, rerun the update, then stop CUPS again. See issues #9377 and #9640 for the two causes."
related: [printer-not-found, migration-failed-mid-update, omarchy-update-fails-or-hangs]
draft: false
---

Printing on Omarchy is close to plain Arch with CUPS. The daemon is installed and enabled for you, and the GUI is the standard `system-config-printer`, which shows up as **Print Settings** in the launcher. What changed in the 4.x line is discovery: Omarchy 4.0.2 pulled `cups-browsed` out of the default set, so printers no longer appear on their own.

Everything below was checked against the v4.0.4 source tree and against open issues as of 2026-09-16.

## Status on 4.0.4

Verdict: partial. The print stack is present and works, but three things are on you.

- CUPS itself works. `cups`, `cups-filters` and `cups-pk-helper` are in `install/omarchy-base.packages`, and `install/config/enable-services.sh` runs `systemctl enable cups.service`.
- `avahi` and `nss-mdns` are installed and `avahi-daemon.service` is enabled, so mDNS name resolution for network printers is available.
- Automatic discovery is gone. There is no `cups-browsed` on a 4.0.2 or later machine, and no queues appear by themselves.
- No vendor drivers ship. `hplip`, `gutenprint` and the `foomatic` PPD databases are not in the base package list. Neither is any scanning software: there is no `sane`, `simple-scan` or `xsane` anywhere in the install tree.

If your printer speaks IPP Everywhere or AirPrint, which covers most machines sold in the last decade, you add it once and you are done. If it is an older PCL or PostScript model, or an HP inkjet, you are installing packages by hand.

## What Omarchy does automatically

Unlike GPUs or fingerprint readers, printing has no `omarchy-hw-*` detection script and no `install/hardware/` quirk file. Nothing probes your printer at install time. What Omarchy does is limited and worth knowing precisely.

- **Installs and enables the stack.** CUPS, cups-filters, the Polkit helper, Avahi and nss-mdns, plus `system-config-printer` as the GUI.
- **Uses cups-pk-helper instead of group membership.** Migration `1787815267` adds `cups-pk-helper` because CUPS on Omarchy no longer treats the `wheel` group as `@SYSTEM`. You administer printers through Polkit, not by being in `lp` or `sys`.
- **Dropped cups-pdf.** The same migration removes `cups-pdf`, on the reasoning that its backend runs a job-controlled post-processing command as root and that applications have their own print-to-file. Use your app's own Print to File or Save as PDF instead of a `PDF` queue.
- **Removed cups-browsed.** Migration `1788009111`, shipped by PR #8951 in v4.0.2, disables the service, deletes idle `implicitclass://` queues that discovery created, leaves queues that still have jobs, and drops the package. PR #8951 says manually added IPP and USB printers are left untouched.
- **Protects one config file.** `install/post-install/pacman.sh` reinstalls Omarchy's `cups-files.conf` override and deletes the `.pacnew` that pacman would otherwise leave. See [/fix/pacnew-and-pacsave-files-after-update/](/fix/pacnew-and-pacsave-files-after-update/) for the general pattern.
- **Hides two launcher entries.** `default/omarchy/launcher.hides` hides `cups` and `avahi-discover` so only Print Settings shows up.

## Known problems

The two migrations above are the source of most 4.x printing reports, and the rest are upstream Arch package problems that land on you through `omarchy update`.

| Issue | Models affected | Status | Fixed in |
| --- | --- | --- | --- |
| [#9377](https://github.com/omacom/omarchy/issues/9377) Migration 1788009111 aborts the whole update when cups.service is stopped | Any machine with CUPS disabled | open | not yet |
| [#9640](https://github.com/omacom/omarchy/issues/9640) Same migration aborts on non-English locales because `LC_ALL=C` does not translate `lpstat` | Any non-English system, reported on pt_BR | open | not yet |
| [#11186](https://github.com/omacom/omarchy/issues/11186) Browser print gives one page then PJL garbage and blank sheets | HP LaserJet P2055dn over USB, hplip backend | open | not yet |
| [#11814](https://github.com/omacom/omarchy/issues/11814) Driverless queue fails every job with `universal filter failed` | HP Smart Tank 520/540 series over USB | open | not yet |
| [#3790](https://github.com/omacom/omarchy/issues/3790) GUI print dialogs hang forever while `lp` works | Canon MF210 on 3.2.2, reported by several users | workaround | closed by package reinstall, no release fix |
| [#9311](https://github.com/omacom/omarchy/issues/9311) Updates rewrite `/etc/nsswitch.conf` and put `mdns_minimal` before `files` | Anyone using `.local` hostnames | open | not yet |

Two of these deserve detail.

**The migration failures (#9377, #9640).** `omarchy-update` runs under `set -e` and migrations run early, so the abort skips the AUR update, mise update and orphan cleanup that come after. joselberg's report and the code both show the script only accepts `lpstat: No destinations added.` as an empty queue list. A stopped scheduler says `Scheduler is not running.` instead, and a Portuguese system says it in Portuguese. rafaelclima traced that to gettext's `LANGUAGE` overriding `LC_ALL`, and confirmed `LC_MESSAGES=C` does force English. PR #9406 proposed the one-line fix for the stopped-scheduler half and PR #9650 the locale half. Both were closed unmerged on 2026-09-16 and folded into PR #12101, which covers both cases and is still open. Neither half is fixed in 4.0.4.

**The blank-page regression (#11186).** This one looks like the cups-browsed removal and is not. docPoacher first blamed the migration, then disproved it with a single-variable test: downgrading `libcupsfilters` from 2.2.1-2 back to 2.1.1-4 restored correct two-page output while cups-browsed stayed installed. The report is that `pacman -Syu` pulled libcupsfilters across a major version while `cups-filters` stayed at 2.0.1-2. Command line `lp` jobs printed fine in the broken state, which is why it reads as a browser bug.

## Fixes that work

Work in this order.

1. **Check the daemon.** `systemctl status cups.service`. If it is disabled, enable it before you touch anything else, and before you run `omarchy update`.
2. **Add the queue by hand.** Open Print Settings from the launcher and choose Add. The [manual FAQ](https://omarchy.org/manual/faq/) walks through it: USB and most network printers are found by the wizard, and if yours is not, pick Network Printer then Internet Printing Protocol and enter the address, typically the printer's IP with a queue of `ipp/print`. Modern printers want the driverless IPP Everywhere profile.
3. **If the update stops on the printer migration**, give it a running scheduler, following joselberg's and arkmpm's workaround: `sudo systemctl start cups.socket cups.service`, rerun `omarchy update`, then stop the units again if you want them off. See [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/).
4. **If GUI dialogs hang but `lp` prints**, reinstall the CUPS libraries so their versions match. EERomeo's fix in #3790 was `sudo pacman -S cups cups-filters libcups --overwrite='*'` followed by `sudo systemctl restart cups`. daviewales noted this downgraded two packages on their machine, which is the tell that the freeze is a version mismatch.
5. **If pages come out blank or full of PJL text**, check whether `libcupsfilters` is 2.2.x while `cups-filters` is still 2.0.x. docPoacher's workaround is a downgrade from the pacman cache plus an `IgnorePkg` pin.
6. **For HP hardware**, install the vendor stack. HIMANSHU11827's verified recipe on a Smart Tank 529 installs `hplip`, `gutenprint`, `foomatic-db-gutenprint-ppds` and friends, disables `ipp-usb` so it stops fighting the kernel `usblp` driver, then creates the queue with `lpadmin` against the model's hpcups PPD. curtisspendlove's older guide in discussion #250 covers the `hp-setup -i` route.
7. **If `.local` names stop resolving after an update**, that is #9311, not your printer. Reorder `files` ahead of `mdns_minimal` in the `hosts:` line of `/etc/nsswitch.conf`.

Two gaps to set expectations. There is no built-in print dialog for images: jonnyace opened discussion #10417 and PR #10418 asking for one, and the PR is still open. And scanning is entirely unaddressed by the distribution.

## Report it

Printing reports are worth filing because nothing in the hardware scripts covers printers, so issues are the only place the problems get recorded.

Run `omarchy debug` to collect `inxi`, `dmesg`, the boot journal and your full package list into `/tmp/omarchy-debug.log`. Add `--no-sudo` to skip `dmesg` if you would rather not share it. See [/reference/commands/omarchy-debug/](/reference/commands/omarchy-debug/).

For a printing report specifically, attach these on top of the debug log, because the good reports above all had them:

- `pacman -Q cups cups-filters libcupsfilters libcups hplip` so the version-mismatch class is visible immediately.
- The device URI from `lpstat -v`, and the job failure line from `/var/log/cups/error_log`.
- Your printer's IEEE-1284 string and USB vendor:product id.
- Whether `lp -d <queue> <file>` behaves differently from printing in an app. That single comparison is what separated #11186 from a browser bug.

File at [github.com/omacom/omarchy/issues](https://github.com/omacom/omarchy/issues), and if your machine's printer situation is worth recording here, use [/hardware/submit/](/hardware/submit/).

## Related

- [/fix/printer-not-found/](/fix/printer-not-found/)
- [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/)
- [/fix/omarchy-update-fails-or-hangs/](/fix/omarchy-update-fails-or-hangs/)
- [/switch/printers-and-scanners/](/switch/printers-and-scanners/)
- [/releases/v4.0.2/](/releases/v4.0.2/)
- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/)
