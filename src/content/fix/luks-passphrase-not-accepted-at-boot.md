---
title: "LUKS passphrase not accepted at boot"
description: "The Omarchy disk unlock prompt rejects the right LUKS passphrase. Type it as US QWERTY to get in, then put XKBLAYOUT in vconsole.conf and rebuild the UKI."
answer: "Almost always the boot prompt is on a different keyboard layout than the one your passphrase was enrolled under. Type the passphrase as if the keyboard were US QWERTY. Once you are in, make sure /etc/vconsole.conf has an XKBLAYOUT line, not just KEYMAP, then run sudo limine-mkinitcpio to rebuild the boot image. Omarchy 3.8.3 and later bundle vconsole.conf into the initramfs for Latin layouts."
appliesTo:
  from: "3.x"
status: workaround
fixedIn: "3.8.3"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: boot
issueCount: 151
errorStrings:
  - "No key available with this passphrase."
tags: [luks, boot, keyboard-layout, plymouth, initramfs, encryption]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6072"
    title: "Issue #6072: Plymouth LUKS unlock prompt uses QWERTY despite French keymap present in UKI"
    kind: issue
    author: "lionel-arnaud"
    date: "2026-06-11"
  - url: "https://github.com/omacom/omarchy/issues/6151"
    title: "Issue #6151: Non-US keyboard layout not applied at LUKS decrypt prompt after 3.8.x update"
    kind: issue
    author: "Codinger-404"
    date: "2026-06-29"
  - url: "https://github.com/omacom/omarchy/issues/6165"
    title: "Issue #6165: LUKS password prompt fails on boot after Plymouth update"
    kind: issue
    author: "Jick1164"
    date: "2026-07-04"
  - url: "https://github.com/omacom/omarchy/issues/6229"
    title: "Issue #6229: vconsole.conf bundled into initramfs locks out LUKS users with non-Latin keyboard layouts (Hebrew/Greek/Cyrillic)"
    kind: issue
    author: "elpddev"
    date: "2026-07-16"
  - url: "https://github.com/omacom/omarchy/issues/8196"
    title: "Issue #8196: Full-disk install: password set under a non-US keyboard layout can be untypeable at the LUKS boot prompt"
    kind: issue
    author: "notwitcheer"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7049"
    title: "Issue #7049: Fresh Quattro install ignores installer keyboard layout choice, vconsole.conf gets only KEYMAP"
    kind: issue
    author: "Asknorway"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/6878"
    title: "Issue #6878: Quattro upgrade drops non-US keyboard layout when vconsole.conf only has KEYMAP"
    kind: issue
    author: "cempack"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/9828"
    title: "Issue #9828: Snapper rollbacks silently un-apply Omarchy migrations (surfaced as: LUKS prompt still QWERTY)"
    kind: issue
    author: "v-h-z"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/10453"
    title: "Issue #10453: Early thunderbolt module removes firmware-provided dock USB before the LUKS prompt"
    kind: issue
    author: "davidisgeek"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10335"
    title: "Issue #10335: Cannot login with Bluetooth keyboard"
    kind: issue
    author: "folken718"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/6876"
    title: "Issue #6876: omarchy_hooks.conf replaces HOOKS instead of extending it, leaving LVM-on-LUKS roots unbootable"
    kind: issue
    author: "alancaldas84"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.3"
    title: "Release v3.8.3"
    kind: release
    date: "2026-07-13"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 Quattro"
    kind: release
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
credits:
  - name: "Zeus-Deus"
    url: "https://github.com/Zeus-Deus"
    for: "Fixed the wrong layout at the LUKS prompt by bundling /etc/vconsole.conf into the initramfs, shipped in 3.8.3"
  - name: "elpddev"
    url: "https://github.com/elpddev"
    for: "Showed that bundling a non-Latin layout locks those users out instead, and diffed the pre and post update boot images to prove it"
  - name: "Codinger-404"
    url: "https://github.com/Codinger-404"
    for: "Posted the vconsole.keymap kernel cmdline workaround via /etc/limine-entry-tool.d"
  - name: "KrissLodBrok"
    url: "https://github.com/KrissLodBrok"
    for: "Confirmed that typing the passphrase in US QWERTY positions unlocks the disk when the prompt has fallen back"
faq:
  - q: "Does the snapshot menu help if the passphrase is rejected?"
    a: "Sometimes. Older Limine snapshot entries carry their own older boot image, so an entry from before the change that broke your prompt may still unlock. That is how the reporter of issue #6229 got back in. It does not help on a fresh install that never booted correctly."
  - q: "Why does my layout work in the desktop but not at the unlock prompt?"
    a: "They read different files. The desktop layout comes from Hyprland, and since 4.0.0 the packaged input.lua reads XKBLAYOUT from /etc/vconsole.conf. The unlock prompt runs inside the initramfs and only sees what mkinitcpio put there."
  - q: "Can I change the passphrase to something that types the same on every layout?"
    a: "Yes, from a working session. Run Update then Password then Drive Encryption in the Omarchy menu, which calls omarchy-drive-password and runs cryptsetup luksChangeKey on the encrypted drive it finds."
related: [you-are-in-emergency-mode-after-update, kernel-panic-after-update-limine, login-loop-or-password-not-accepted-sddm, lock-screen-wont-unlock, stuck-at-tty-or-cannot-switch-tty]
draft: false
---

The passphrase is almost never wrong. The keyboard is. The Omarchy unlock prompt runs inside the initramfs, long before Hyprland loads your layout, and for most of 3.x it typed US QWERTY no matter what you picked in the installer. If your passphrase contains a character that moves between layouts, the prompt rejects it and tells you nothing useful. Everything below was checked against the 3.8.4 and 4.0.4 source trees.

## The fix

### 1. Get in by typing the passphrase in US QWERTY

Before changing anything, retype the passphrase as if the keycaps were a US keyboard. On AZERTY that means `a` and `q` swap, `z` and `w` swap, `m` moves to the right of `l`, and the digits on the top row are unshifted. On QWERTZ, `y` and `z` swap.

In issue #6072, KrissLodBrok reported that typing the passphrase this way unlocked the disk on a French machine whose prompt had reverted to QWERTY. Do this first, because every real repair below needs a booted system.

If you use a Hebrew, Greek, Cyrillic or Arabic layout and the prompt broke after an update, the failure is the mirror image: the prompt started typing your layout, and your passphrase is Latin. Same answer, type it as US QWERTY.

### 2. Check what the system actually recorded

Once you are in, look at the file the boot image reads:

```bash
cat /etc/vconsole.conf
```

A healthy file has both keys:

```
KEYMAP=fr
XKBLAYOUT=fr
```

Issues #7049 and #6878 both report installs where only `KEYMAP` is present. That is legal, `vconsole.conf` only guarantees the console keymap, but Omarchy's Quattro defaults key off `XKBLAYOUT`, so a missing line silently means `us`.

### 3. Set XKBLAYOUT if it is missing

```bash
sudo localectl set-x11-keymap fr
cat /etc/vconsole.conf
```

Substitute your own code (`de`, `no`, `it`, `be`, `se`). Confirm the file now carries `XKBLAYOUT`. If `localectl` writes it somewhere else on your machine, append the line by hand instead.

### 4. Rebuild the boot image

On 4.0.x and on 3.8.3 or later:

```bash
sudo limine-mkinitcpio
```

That is the whole fix on a current system. Omarchy ships `/etc/mkinitcpio.conf.d/omarchy_hooks.conf`, and on 4.0.x that file decides at rebuild time whether to add `/etc/vconsole.conf` to `FILES`. It adds it for Latin layouts and skips it for the non-Latin list (`ara`, `bg`, `gr`, `il`, `ru`, `ua` and others), so a Latin passphrase stays typeable.

On 3.8.2 and earlier there is no such logic at all. Either update, or append the line yourself and rebuild:

```bash
echo 'FILES+=(/etc/vconsole.conf)' | sudo tee -a /etc/mkinitcpio.conf.d/omarchy_hooks.conf
sudo limine-mkinitcpio
```

## Verify it worked

Check that the rebuilt image carries the file. A commenter on issue #6151 inspected the unified kernel image directly:

```bash
sudo lsinitcpio /boot/EFI/Linux/omarchy_linux.efi | grep vconsole
```

Then reboot and type the passphrase on your own layout. If it unlocks on the first try, you are done. If you want a second check without rebooting, `localectl status` should report the same VC keymap and X11 layout.

## Why it happens

Omarchy boots a unified kernel image through Limine, with Plymouth drawing the unlock prompt. The layout that prompt uses comes from the initramfs, not from your session.

Two separate things broke here. The first was Plymouth. Issues #6072, #6151 and #6165 all land in late June and early July 2026, all on Plymouth 26.134.222, and all describe the same regression: the console keymap was present in the boot image, but the graphical prompt ignored it and fell back to QWERTY. Release v3.8.3 on 2026-07-13 fixed it by bundling `/etc/vconsole.conf` into the initramfs, credited to Zeus-Deus, and v4.0.0 carried the same change forward.

That fix then created its own lockout. elpddev filed issue #6229 four days later: with a Hebrew layout bundled, the prompt mapped letter keys to Hebrew, and a Latin passphrase could no longer be typed at all. Omarchy 4.0.x answers this with the layout filter in `omarchy_hooks.conf` plus migration `1784476564.sh`, which strips the bundling on non-Latin machines and rebuilds the image.

The second problem is the missing `XKBLAYOUT`, and it is still open. Issue #7049 shows a fresh Quattro install writing only `KEYMAP=no-latin1`, and #6878 shows a Quattro upgrade in the same state with `KEYMAP=fr`. Issue #8196, filed 2026-08-25 and open at the time of writing, is the worst version: a passphrase set under AZERTY during a full-disk install that could not be typed at the boot prompt afterwards, with the reporter saying QWERTY translation did not help either. That one has no confirmed explanation yet, and the reporter reinstalled with a layout-stable passphrase.

## If that did not work

**You restored a snapshot.** Issue #9828 reports that restoring a Snapper snapshot rewinds the root subvolume but not `/home`, where the migration markers live, so a migration that already fixed your boot image gets undone while still counting as applied. `omarchy-migrate` will not rerun it. Redo steps 3 and 4 by hand.

**The keyboard itself is not alive yet.** If you type through a Thunderbolt dock, issue #10453 reports the early `thunderbolt` module removing the dock's USB controller before the prompt appears. Bluetooth keyboards are not connected at that point either, per issue #10335. Plug a wired keyboard straight into the machine.

**The prompt never appears, or the boot dies right after unlocking.** That is a different failure. Issue #6876 reports that `omarchy_hooks.conf` replaces the whole `HOOKS` array rather than extending it, so an LVM-on-LUKS root loses the `lvm2` hook and never comes up. See [kernel panic after update](/fix/kernel-panic-after-update-limine/) and [emergency mode after update](/fix/you-are-in-emergency-mode-after-update/).

**You cannot get in anywhere.** Boot an older entry from the Limine menu, described in the [manual chapter on system snapshots](https://omarchy.org/manual/system-snapshots/). Those entries carry their own older boot image, which is how the reporter of #6229 recovered. Failing that, boot an Arch live USB, unlock with `cryptsetup open`, mount the `@` subvolume, `arch-chroot`, and repeat steps 3 and 4. Be honest with yourself about the last resort: if the passphrase is rejected from a live USB too, it was never enrolled as the characters you think it was, and a reinstall is the only path left.

## Related

- [Non-US keyboard layout at LUKS and SDDM](/switch/non-us-keyboard-layout-luks-sddm/)
- [Layouts and locale](/keyboard/layouts-and-locale/)
- [Login loop or password not accepted at SDDM](/fix/login-loop-or-password-not-accepted-sddm/)
- [Lock screen will not unlock](/fix/lock-screen-wont-unlock/)
- [LUKS and UFW defaults](/security/luks-and-ufw-defaults/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
