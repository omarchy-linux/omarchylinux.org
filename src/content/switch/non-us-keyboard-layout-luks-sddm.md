---
title: "Non-US keyboard layouts: LUKS, SDDM and Hyprland"
description: "On Omarchy 4.0.x your keyboard layout has to be set in three separate places. Fix the LUKS prompt, the Hyprland session and the SDDM greeter."
answer: "Omarchy applies your layout in three places and only one of them is automatic. The LUKS prompt uses KEYMAP in /etc/vconsole.conf, the Hyprland session uses XKBLAYOUT from the same file, and the SDDM greeter uses neither, so it is always US. Set both variables, rebuild the UKI, and add an input block for the greeter under /etc."
appliesTo:
  from: "4.0.0"
status: open
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [keyboard, luks, sddm, hyprland, install]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8196"
    title: "Issue #8196: Full-disk install: password set under a non-US keyboard layout can be untypeable at the LUKS boot prompt"
    kind: issue
    author: "notwitcheer"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/6880"
    title: "Issue #6880: SDDM greeter always uses US keyboard layout, ignoring the system layout"
    kind: issue
    author: "g-desoutter"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/9421"
    title: "Issue #9421: SDDM greeter's Hyprland config ignores system keyboard layout, causing password mismatches for non-US layouts"
    kind: issue
    author: "winless-code"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/10269"
    title: "Issue #10269: SDDM greeter ignores system keyboard layout, causing silent password-mismatch after autologin is used up"
    kind: issue
    author: "AltairSD"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/10454"
    title: "Issue #10454: SDDM greeter ignores system keyboard layout (always US, breaks AZERTY at login/lock screen)"
    kind: issue
    author: "tecknozic"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/7049"
    title: "Issue #7049: Fresh Quattro install ignores installer keyboard layout choice, vconsole.conf gets only KEYMAP, Hyprland falls back to us"
    kind: issue
    author: "Asknorway"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/6878"
    title: "Issue #6878: Quattro upgrade drops non-US keyboard layout when vconsole.conf only has KEYMAP"
    kind: issue
    author: "cempack"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/6229"
    title: "Issue #6229: vconsole.conf bundled into initramfs locks out LUKS users with non-Latin keyboard layouts (Hebrew/Greek/Cyrillic)"
    kind: issue
    author: "elpddev"
    date: "2026-07-16"
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy Manual: Keyboard, Mouse, Trackpad"
    kind: manual
credits:
  - name: "g-desoutter"
    url: "https://github.com/g-desoutter"
    for: "Traced the US greeter to the SDDM compositor config having no input block"
  - name: "tecknozic"
    url: "https://github.com/tecknozic"
    for: "Documented the standalone greeter-hyprland.lua plus 20- drop-in form of the greeter fix"
  - name: "Asknorway"
    url: "https://github.com/Asknorway"
    for: "Showed that a fresh install writes KEYMAP but no XKBLAYOUT"
  - name: "notwitcheer"
    url: "https://github.com/notwitcheer"
    for: "Reported the AZERTY LUKS lockout on a fresh 4.x install"
faq:
  - q: "Why does my password work in the terminal but not on the login screen?"
    a: "The SDDM greeter runs its own small Hyprland instance whose config ships with no input block, so it falls back to US. Your session and your TTY read the system layout, the greeter does not. Any password character that moves between layouts is typed wrong there."
  - q: "Why did nobody notice the greeter bug sooner?"
    a: "Encrypted installs turn on autologin, and the autologin PAM stack does not actually check the password. The greeter only appears after you log out, which is when authentication starts failing for real."
  - q: "I use Hebrew, Greek, Cyrillic or Arabic. Why is the LUKS prompt still US?"
    a: "That is deliberate. Omarchy keeps non-Latin layouts out of the initramfs so a Latin passphrase stays typeable, after issue #6229 locked a Hebrew user out. Your session also gets us prepended to kb_layout, and Left Alt plus Right Alt switches."
  - q: "Will omarchy update undo my fix?"
    a: "Only if you edited a packaged file. Anything under /usr/share is owned by a package and gets replaced. Changes in /etc/vconsole.conf, /etc/sddm.conf.d and ~/.config/hypr/input.lua survive updates."
related: [day-one-checklist, what-replaces-what]
draft: false
---

If you type on AZERTY, QWERTZ, a Nordic layout or anything else that is not US QWERTY, Omarchy 4.0.x will surprise you at least once. Checked against v4.0.4.

## Where the layout actually comes from

There are three separate places, and only one of them is set for you reliably.

1. The console and the LUKS unlock prompt read `KEYMAP` in `/etc/vconsole.conf`. These are console keymap names such as `fr`, `be-latin1` or `no-latin1`. Omarchy's `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` keeps the `keymap` and `consolefont` hooks and adds `FILES+=(/etc/vconsole.conf)` so Plymouth applies the layout at the prompt, unless your layout is non-Latin.
2. The Hyprland session reads `XKBLAYOUT` and `XKBVARIANT` from the same file. The packaged `/usr/share/omarchy/default/hypr/input.lua` does `local kb_layout = vconsole.XKBLAYOUT or "us"`. No `XKBLAYOUT` means US, no matter what `KEYMAP` says.
3. The SDDM greeter reads neither. Its compositor config, `/usr/share/sddm/hyprland.lua`, sets only `misc` and `animations`. With no `input` block, Hyprland uses its own default, which is US. Four separate reports say the same thing: [#6880](https://github.com/omacom/omarchy/issues/6880), [#9421](https://github.com/omacom/omarchy/issues/9421), [#10269](https://github.com/omacom/omarchy/issues/10269) and [#10454](https://github.com/omacom/omarchy/issues/10454), all still open as of 2026-09-16.

## Before you install, pick a safe passphrase

The dangerous moment is full-disk encryption on a fresh install. In [#8196](https://github.com/omacom/omarchy/issues/8196) an AZERTY user picked French in the installer, used digits in the password, and found the LUKS prompt rejecting it on every boot. On AZERTY the digits are the shifted top row, so a passphrase enrolled with the layout applied is untypeable when the prompt falls back to US. Reinstalling was the only way out.

Until that is fixed, pick a disk passphrase from keys that sit in the same place on your layout and on US. In practice that means lowercase letters only. Leave out `a`, `q`, `z`, `w` and `m` on AZERTY, `y` and `z` on QWERTZ, and skip digits and punctuation entirely. Change it to something stronger after first boot, once you have confirmed the prompt uses your layout.

## The fix

Run these after your first boot. Replace `fr` with your layout and `pc105` with your model.

1. See what you have now.

```bash
cat /etc/vconsole.conf
localectl status
hyprctl getoption input:kb_layout
```

2. Set both the console keymap and the XKB layout.

```bash
sudo localectl set-keymap fr
sudo localectl set-x11-keymap fr pc105
grep -E 'KEYMAP|XKB' /etc/vconsole.conf
```

If that `grep` shows no `XKBLAYOUT`, add it yourself. This is the missing piece on the fresh 4.0.0 install in [#7049](https://github.com/omacom/omarchy/issues/7049), and on machines upgraded from 3.x, reported in [#6878](https://github.com/omacom/omarchy/issues/6878).

```bash
printf 'XKBLAYOUT=fr\n' | sudo tee -a /etc/vconsole.conf
```

3. Rebuild the initramfs and the UKI so the LUKS prompt picks up the keymap.

```bash
sudo limine-mkinitcpio
```

4. Fix the session if it is still US after a logout. Open `~/.config/hypr/input.lua`, or reach it from the Omarchy menu with `Super + Space` under Setup then Input, and add:

```lua
hl.config({
  input = {
    kb_layout = "fr",
    kb_variant = "",
  },
})
```

5. Fix the SDDM greeter. Do not edit `/usr/share/sddm/hyprland.lua`, because it belongs to the `omarchy-settings` package and the next `omarchy update` that ships that package will put the stock file back. Put your own copy under `/etc` and point SDDM at it.

```bash
sudo mkdir -p /etc/sddm
sudo tee /etc/sddm/greeter-hyprland.lua >/dev/null <<'EOF'
hl.config({
  input = {
    kb_layout = "fr",
    kb_variant = "",
    kb_model = "pc105",
  },
  misc = {
    disable_hyprland_logo = true,
    disable_splash_rendering = true,
    force_default_wallpaper = 0,
  },
  animations = { enabled = false },
})
EOF
sudo tee /etc/sddm.conf.d/20-keyboard.conf >/dev/null <<'EOF'
[Wayland]
CompositorCommand=start-hyprland -- --config /etc/sddm/greeter-hyprland.lua
EOF
```

SDDM merges everything in `sddm.conf.d` in filename order, so `20-keyboard.conf` wins over the shipped `10-wayland.conf`. Neither new file is owned by a package, so a package update has no reason to touch them.

## Verify it worked

```bash
grep -E 'KEYMAP|XKB' /etc/vconsole.conf
hyprctl getoption input:kb_layout
hyprctl devices | grep -i 'active keymap'
```

`hyprctl getoption` should report your layout, not `us`. For the greeter, log out rather than reboot: with encryption enabled, autologin skips the greeter at boot, so a reboot proves nothing. Type a layout-sensitive character in the password field and check it appears correctly. For the LUKS prompt, reboot and type one character of your passphrase that moves between layouts before you finish entering it.

The top bar carries a keyboard layout widget, but it stays hidden while only one layout is configured, so do not treat its absence as a failure.

## Why it happens

On the fresh 4.0.0 install in [#7049](https://github.com/omacom/omarchy/issues/7049), the installer recorded the choice as a console keymap only: `vconsole.conf` had `KEYMAP=no-latin1` and nothing else, so the packaged `input.lua` fell through to its `"us"` default even though the console was correct. A later report in the same thread, on 4.0.2, did get `XKBLAYOUT=ch` written, and the 4.0.4 first boot provisioner's own comments say `systemd-firstboot --keymap` is expected to set both values. So whether you are missing `XKBLAYOUT` depends on which release installed your machine, which is why step 2 has you check rather than assume.

Upgrades from 3.x fail differently. On 3.8.4 the layout lived in `~/.config/hypr/input.conf` as `kb_layout = fr`. Quattro moved Hyprland config to Lua, installs a stock `input.lua`, and does not copy the old value across. If `vconsole.conf` has only `KEYMAP`, the session silently becomes US. That is [#6878](https://github.com/omacom/omarchy/issues/6878).

The greeter is a third code path. It runs its own Hyprland instance through `CompositorCommand` in `/etc/sddm.conf.d/10-wayland.conf`, and the config that instance loads never reads `/etc/vconsole.conf`.

## If the LUKS prompt already rejects your passphrase

You are not necessarily locked out. The enrolled bytes are whatever the installer produced with your layout applied, so a live environment with the same layout loaded can usually still open the volume.

1. Boot the Omarchy ISO from [omarchy.org](https://omarchy.org) and check it against the [verification steps](/verify/).
2. In the live shell, load your layout and try the volume. Use `lsblk` to find the partition.

```bash
loadkeys fr
sudo cryptsetup open /dev/nvme0n1p2 test
```

3. If it opens, the passphrase is fine and only the boot prompt's keymap was wrong. Mount your root subvolume, `arch-chroot` in, make sure `/etc/vconsole.conf` has the right `KEYMAP`, and run `limine-mkinitcpio` before rebooting.
4. If it does not open, try again with `loadkeys us`, then with the characters you believe you typed rather than the ones you intended. Once it opens, change the passphrase with `cryptsetup luksChangeKey` to something layout-stable.

Rolling back to an earlier boot entry is another route if a rebuild broke a prompt that used to work. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).

## If that did not work

Check whether your layout is non-Latin. Omarchy treats `af am ara bd bg by et ge gr il in iq ir kg kh kz la lk mk mm mn mv np rs ru sy th tj ua` as a special case: `vconsole.conf` is deliberately kept out of the initramfs so a Latin passphrase stays typeable, after [#6229](https://github.com/omacom/omarchy/issues/6229) locked a Hebrew user out of their own machine. The session also gets `us` prepended to `kb_layout`, with `grp:alts_toggle` so Left Alt plus Right Alt switches. A US LUKS prompt on those layouts is intended behaviour, not a bug to fix.

If the session ignores `input.lua`, check that you are editing `~/.config/hypr/input.lua` and not the old `input.conf`, which Quattro no longer reads. See the [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) for what moved where.

If Hyprland reports the right layout but the on-screen keyboard or fcitx5 still types US, look at `~/.config/fcitx5/profile`. Both reports in [#7049](https://github.com/omacom/omarchy/issues/7049) found it pinned to `keyboard-us` regardless of the installer choice. Stop fcitx5 before editing it, because it rewrites the file on exit.

If the greeter is still US, confirm the drop-in is being read, and check that nothing else in `/etc/sddm.conf.d` sets `CompositorCommand` later in sort order. SDDM does not filter that directory by extension, so an old file you renamed to `.bak` or `.disabled` is still loaded.

## What to watch for on newer versions

The seven open issues behind this page were all still open on 2026-09-16, and neither the 4.0.3 nor the 4.0.4 release notes mention keyboard layout. The packaged `default/sddm/hyprland.lua` in the 4.0.4 snapshot still has no `input` block, and the quattro-dev development branch did not have one either at the time of checking. When a fix does land, the shipped greeter config will start reading `/etc/vconsole.conf`, at which point your `/etc/sddm.conf.d/20-keyboard.conf` drop-in becomes redundant but harmless. Remove it then so you are not pinning an old copy of the greeter config.

## Related

- [Day one checklist](/switch/day-one-checklist/)
- [Keyboard layouts and locale](/keyboard/layouts-and-locale/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- Official manual: [Keyboard, Mouse, Trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/)
