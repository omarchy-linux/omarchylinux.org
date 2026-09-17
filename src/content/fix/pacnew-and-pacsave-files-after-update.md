---
title: "pacnew and pacsave files after an Omarchy update"
description: "What .pacnew and .pacsave files mean after an Omarchy update, which ones actually matter on Omarchy 4, and how to merge them without breaking pacman or your initramfs."
answer: "They are pacman's backup files, not errors. A .pacnew means a package shipped a new config but you had edited the old one, so your version was kept. Omarchy does not warn about them yet. List them with pacdiff, then merge by hand. On Omarchy only a few matter: pacman.conf, omarchy_hooks.conf, and the limine drop-ins."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: update
issueCount: 7
errorStrings:
  - "installed as /etc/pacman.conf.pacnew"
  - "warning: /etc/mkinitcpio.conf.d/omarchy_hooks.conf installed as /etc/mkinitcpio.conf.d/omarchy_hooks.conf.pacnew"
  - "saved as /etc/cups/cups-browsed.conf.pacsave"
tags: [update, pacman, pacnew, pacsave, mkinitcpio, config]
sources:
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/docs/update-process.md"
    title: "docs/update-process.md at v4.0.4 (Remaining concerns: pacnew/pacsave handling is still missing)"
    kind: docs
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/docs/file-layout.md"
    title: "docs/file-layout.md at v4.0.4 (Why etc-overrides/ exists)"
    kind: docs
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/migrations/1786605598.sh"
    title: "Migration 1786605598: rebuild the initramfs, skipping a user-edited omarchy_hooks.conf"
    kind: commit
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/6876"
    title: "Issue #6876: omarchy_hooks.conf replaces HOOKS instead of extending it, dropping lvm2/resume and leaving LVM-on-LUKS roots unbootable"
    kind: issue
    author: "alancaldas84"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/619"
    title: "Issue #619: Add way to lock a config so Omarchy won't ever auto-update it"
    kind: issue
    author: "dhh"
    date: "2025-08-10"
  - url: "https://github.com/omacom/omarchy/pull/887"
    title: "PR #887: Improve config updates with baseline tracking and safe diffs"
    kind: pr
    author: "mfontcada"
    date: "2025-08-18"
  - url: "https://github.com/omacom/omarchy/issues/6234"
    title: "Issue #6234: Default hypridle.conf: screensaver killed ~2s after launch, and update overwrites user-modified hypridle.conf"
    kind: issue
    author: "dlsvob"
    date: "2026-07-18"
  - url: "https://omarchy.org/manual/updates/"
    title: "Omarchy manual: Updates"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "alancaldas84"
    url: "https://github.com/alancaldas84"
    for: "Showing that omarchy_hooks.conf replaces HOOKS wholesale, which is why editing it is common and why its .pacnew matters"
  - name: "mfontcada"
    url: "https://github.com/mfontcada"
    for: "Proposing pacnew-style handling for Omarchy's own config updates in PR #887"
faq:
  - q: "Is a .pacnew file an error?"
    a: "No. It means pacman kept your edited config and parked the package's new version next to it. Nothing is broken, but you are now running an old config that the package no longer expects."
  - q: "Can I just delete every .pacnew file?"
    a: "You can, and nothing breaks immediately. You lose whatever the package changed, which on Omarchy can mean a new mkinitcpio hook or a new pacman repo line that a later update assumes is present."
  - q: "Does omarchy update tell me about them?"
    a: "Not in 4.0.4. docs/update-process.md lists pacnew and pacsave handling under Remaining concerns. The only log check omarchy-update-analyze-logs performs is for failed initramfs generation."
  - q: "Why did my config get overwritten with no .pacnew at all?"
    a: "A handful of files ship through /usr/share/omarchy/etc-overrides/ and are copied into place by a package scriptlet rather than by pacman. Those get clobbered on every omarchy-settings upgrade."
related: [errors-occurred-no-packages-were-upgraded, omarchy-update-fails-or-hangs, migration-failed-mid-update]
draft: false
---

Checked on 4.0.4 (2026-09-15), with the 3.x behaviour taken from the v3.8.4 tree.

A `.pacnew` file is pacman telling you that a package shipped a new version of a
config file you had edited, so it kept yours and saved the new one alongside. A
`.pacsave` is the mirror case: a package was removed and pacman preserved the
config you had. Neither is an error. Both are silent on Omarchy, because as of
4.0.4 nothing in the update pipeline looks for them.

## The fix

1. List what you have. `pacman-contrib` is in `install/omarchy-base.packages`, so
   `pacdiff` is already installed:

   ```bash
   sudo find /etc /boot /usr/share -name '*.pacnew' -o -name '*.pacsave' 2>/dev/null
   ```

   For an interactive pass, use `pacdiff`, which walks each pair and lets you
   view, merge, skip, or remove:

   ```bash
   sudo DIFFPROG='nvim -d' pacdiff
   ```

2. Handle `/etc/pacman.conf.pacnew` first, and do not blindly copy it over.
   Omarchy replaces this file with its own, which carries the `[omarchy]` repo
   pointing at `https://pkgs.omarchy.org/<channel>/$arch` plus the Omarchy
   mirrorlist. The `.pacnew` comes from upstream Arch and has none of that.
   Merge only the new `[options]` lines you want, or reset the whole file to
   Omarchy's version for your channel:

   ```bash
   omarchy-refresh-pacman stable   # or rc, or edge
   ```

   That backs up your current file to `/etc/pacman.conf.bak` before copying, then
   runs a full `pacman -Syyuu`.

3. Handle `/etc/mkinitcpio.conf.d/omarchy_hooks.conf.pacnew` next. This is the
   one that can cost you a boot. The file is owned by `omarchy-settings` and it
   reassigns `HOOKS` wholesale rather than extending it, which is why people on
   LVM, mdraid, hibernation, or a systemd initramfs chain end up editing it
   (issue #6876). Merge the new hook list by hand, keep the hooks your root
   layout needs, then rebuild and inspect before rebooting:

   ```bash
   sudo limine-mkinitcpio
   objcopy -O binary --only-section=.initrd \
     /boot/EFI/Linux/omarchy_linux.efi /tmp/uki-initrd.img
   lsinitcpio -l /tmp/uki-initrd.img | grep '^hooks/'
   ```

   Omarchy enables unified kernel images by default through
   `/etc/limine-entry-tool.d/omarchy-uki.conf`, so the initramfs lives inside the
   `.efi` file rather than as a standalone image. That extraction is the method
   the reporter of #6876 used to prove the `lvm2` hook had vanished.

4. Handle `/etc/limine-entry-tool.d/omarchy-defaults.conf.pacnew`. Leaving this
   one is fine. Migration `1789325478` in 4.0.4 writes `BOOT_ORDER` into
   `/etc/default/limine`, which has priority over every drop-in, and Omarchy's
   own test asserts that the `.pacnew` is left untouched for the administrator to
   merge. Merge any non-`BOOT_ORDER` settings you care about, or delete it.

5. Handle the rest. For anything else, diff it, take what you want, and remove
   the leftover:

   ```bash
   sudo rm /etc/some/file.pacnew
   ```

6. Delete `.pacsave` files once you have read them. They belong to packages that
   are gone. Omarchy removes `cups-browsed`, for example, and its acceptance test
   asserts that neither `/etc/cups/cups-browsed.conf.pacsave` nor the matching
   `.pacnew` is left behind.

## Verify it worked

- The `find` command above returns nothing.
- `pacman -Sl omarchy | head -n 1` prints a package, which proves you did not
  lose the `[omarchy]` repo while merging `pacman.conf`.
- If you touched anything under `/etc/mkinitcpio.conf.d/`, the `lsinitcpio`
  output lists every hook your root needs, especially `encrypt` or `sd-encrypt`,
  and `lvm2`, `mdadm_udev`, or `resume` if you use them. An empty or short list
  is the signature of issue #6876.
- Reboot once after merging any boot path file, before you forget you changed it.

## Why it happens

Pacman only writes a `.pacnew` when three things are true: the file is listed as
a backup file by its package, the package shipped a new version, and your copy
differs from the one the package previously installed. Unmodified files are
simply replaced and you never see a `.pacnew`.

What changed in Omarchy 4 is who owns the files. In 3.x Omarchy was a git
checkout under your home directory, so Omarchy's own defaults were never pacman
managed and could never produce a `.pacnew`. Only plain Arch packages did. There
is no mention of `pacnew` anywhere in the v3.8.4 tree. Quattro made Omarchy
package backed: `omarchy` and `omarchy-settings` now install real files into
`/etc`, so your edits to them can now collide with a package upgrade the way any
other Arch config does.

Omarchy has not caught up with that yet. `docs/update-process.md` closes with a
section called Remaining concerns, and the second entry says pacnew and pacsave
handling is still missing, noting that package backed Omarchy should warn about
or help process these files. `omarchy-update-analyze-logs`, the only step that
reads the update transcript, currently checks for one thing: failed initramfs
generation.

There is a second, quieter category worth knowing about. `docs/file-layout.md`
explains that a few files owned by upstream Arch packages, including
`/etc/nsswitch.conf`, `/etc/security/faillock.conf`, `/etc/cups/cups-browsed.conf`,
`/etc/plymouth/plymouthd.conf`, `/etc/os-release`, and `/etc/skel/.bashrc`, ship
at `/usr/share/omarchy/etc-overrides/` and are copied into place by the
`omarchy-settings` scriptlet. The doc states the tradeoff plainly: user edits to
those files get clobbered on every `omarchy-settings` upgrade. No `.pacnew` is
written, because pacman is not the one doing the copying.

A `.pacnew` also has a knock on effect on migrations. Migration `1786605598`
rebuilds the initramfs to drop unused nouveau firmware, and its comment notes
that a user edited `omarchy_hooks.conf`, whose update landed in a `.pacnew`,
keeps the old hook list and correctly skips the rebuild. Merging your `.pacnew`
files is therefore also how you stop silently opting out of repairs.

Asking for better handling is not new. Issue #619, opened by dhh, proposed
locking configs so Omarchy would not auto update them, and was closed as not
planned in November 2025. PR #887 by mfontcada proposed a pacnew style baseline
with safe diffs for Omarchy's own configs, and was closed without merging.

## If that did not work

- The machine will not boot after you merged a hooks file. Pick the pre update
  snapshot in the Limine menu and start over. See
  [/upgrade/rollback-with-snapper-and-limine/](/upgrade/rollback-with-snapper-and-limine/)
  and [/fix/you-are-in-emergency-mode-after-update/](/fix/you-are-in-emergency-mode-after-update/).
- The same `.pacnew` returns after every update. That is the expected outcome of
  editing a package owned file. Where the directory supports it, move your change
  into a separate drop in that sorts after Omarchy's, rather than editing
  Omarchy's file. This works for `mkinitcpio.conf.d`, `sysctl.d`, and systemd
  drop in directories, since the last assignment wins.
- You cannot remember what you changed. Compare the installed file against the
  package's copy with `pacman -Qkk <package>`, or extract the original from
  `/var/cache/pacman/pkg/`.
- You want a warning next time. `omarchy update` runs `omarchy-hook post-update`
  after migrations, so a script at
  `~/.config/omarchy/hooks/post-update.d/pacnew-check` that runs the `find`
  command above will print leftovers at the end of every update. Install it with
  `omarchy hook install post-update <file>`.
- The update itself failed rather than leaving a `.pacnew`. That is a different
  problem. See
  [/fix/errors-occurred-no-packages-were-upgraded/](/fix/errors-occurred-no-packages-were-upgraded/).

## Related

- [/upgrade/what-migrations-do/](/upgrade/what-migrations-do/)
- [/upgrade/before-you-update-checklist/](/upgrade/before-you-update-checklist/)
- [/upgrade/3-to-4-quattro/](/upgrade/3-to-4-quattro/)
- [/fix/migration-failed-mid-update/](/fix/migration-failed-mid-update/)
- [/fix/kernel-panic-after-update-limine/](/fix/kernel-panic-after-update-limine/)
- [/reference/commands/omarchy-refresh-pacman/](/reference/commands/omarchy-refresh-pacman/)
- Official manual chapter: [Updates](https://omarchy.org/manual/updates/)
