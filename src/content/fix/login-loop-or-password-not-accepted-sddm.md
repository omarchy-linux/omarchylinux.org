---
title: "SDDM login loop or password not accepted on Omarchy"
description: "SDDM login loop on Omarchy: the greeter always types US, so non-US passwords fail. Fix the greeter keymap, faillock, the autologin user, and a dying session."
answer: "Most Omarchy SDDM login loops are not a wrong password. The greeter runs its own Hyprland from /usr/share/sddm/hyprland.lua, which sets no kb_layout, so it always types US. Add an input block with your layout, or type the password in US positions. If the greeter accepts the password and bounces back, the session is dying instead: get a TTY and read the journal."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: boot
issueCount: 125
errorStrings:
  - 'Authentication error: SDDM::Auth::ERROR_AUTHENTICATION "Authentication failure"'
  - "[PAM] authenticate: Authentication failure"
  - "pam_unix(sddm:auth): authentication failure"
  - 'Authentication error: SDDM::Auth::ERROR_AUTHENTICATION "User not known to the underlying authentication module"'
  - "gkr-pam: couldn't unlock the login keyring."
  - "drm: Found no gpus to use, cannot continue"
tags: [sddm, login-loop, keyboard-layout, faillock, boot]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6880"
    title: "Issue #6880: SDDM greeter always uses US keyboard layout, ignoring the system layout"
    kind: issue
    author: "g-desoutter"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/10269"
    title: "Issue #10269: SDDM greeter ignores system keyboard layout, causing silent password-mismatch after autologin is used up"
    kind: issue
    author: "AltairSD"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/5986"
    title: "Issue #5986: SDDM greeter defaults to us keymap instead of the one selected on install"
    kind: issue
    author: "hugochinchilla"
    date: "2026-05-27"
  - url: "https://github.com/omacom/omarchy/pull/11293"
    title: "PR #11293: Resolve the SDDM greeter's keyboard layout from vconsole.conf"
    kind: pr
    author: "Schleuse"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/pull/9177"
    title: "PR #9177: Apply the configured keyboard layout on the SDDM greeter"
    kind: pr
    author: "florentdestremau"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/5044"
    title: "Issue #5044: Cannot log in to Omarchy Session (possible SDDM startup issue)"
    kind: issue
    author: "benjamalegni"
    date: "2026-03-17"
  - url: "https://github.com/omacom/omarchy/issues/7949"
    title: "Issue #7949: SDDM authenticates empty username after interrupted/resumed install"
    kind: issue
    author: "gtech-pedrol"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/5706"
    title: "Issue #5706: Login loop after update if nvidia DKMS fails to build for the new kernel"
    kind: issue
    author: "sanity"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/8776"
    title: "Issue #8776: Dual-GPU AMD: PCI by-path in AQ_DRM_DEVICES silently login-loops SDDM autologin"
    kind: issue
    author: "mowgli42"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/10700"
    title: "Issue #10700: Silent lock-screen login loop when ~/.config/uwsm/env.d has a shell error"
    kind: issue
    author: "austrasien"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/6439"
    title: "Issue #6439: Password screen loop after update to 3.8.4"
    kind: issue
    author: "v-h-z"
    date: "2026-07-30"
  - url: "https://github.com/omacom/omarchy/issues/9147"
    title: "Issue #9147: Changing password via Super Menu updater breaks SDDM login due to gkr-pam keyring mismatch"
    kind: issue
    author: "BSBrouwers"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/8190"
    title: "Issue #8190: ThinkPad T470 boot loop when TPM is visible but unresponsive"
    kind: issue
    author: "KalenJosifovski"
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "g-desoutter"
    url: "https://github.com/g-desoutter"
    for: "Proved the greeter runs its own Hyprland with no input block, so it always falls back to US"
  - name: "hugochinchilla"
    url: "https://github.com/hugochinchilla"
    for: "Showed PAM is being fed the wrong characters rather than refusing a locked account"
  - name: "AltairSD"
    url: "https://github.com/AltairSD"
    for: "Explained why permanent autologin hides the greeter keymap bug until the first real logout"
  - name: "kukat"
    url: "https://github.com/kukat"
    for: "Found the autologin drop-in pointing at root instead of the real user"
  - name: "sanity"
    url: "https://github.com/sanity"
    for: "Traced an update-triggered SDDM loop to a stale UKI carrying the old NVIDIA module"
  - name: "austrasien"
    url: "https://github.com/austrasien"
    for: "Showed one bad file in ~/.config/uwsm/env.d loops the login screen with no visible error"
faq:
  - q: "Why does my password work for sudo but not at the login screen?"
    a: "Because sudo reads the key you pressed through your session layout, and the SDDM greeter reads it through its own Hyprland instance, which has no layout configured and defaults to US. Any character that moves between layouts, such as the at sign, slash, colon or underscore, reaches PAM as a different character."
  - q: "Does faillock --reset fix this?"
    a: "Only if you are actually locked out. Issue #5986 checked the journal and found no pam_faillock lines at all, just plain pam_unix authentication failures, which means the wrong password arrived rather than a locked account. Check faillock --user first before assuming."
  - q: "Will a Snapper rollback get me back in?"
    a: "It depends where the broken thing lives. Snapshot restore covers the root filesystem, not /home, so a bad ~/.config/uwsm/env.d file or a bad monitors.lua survives every snapshot in the Limine menu."
  - q: "Is the greeter keymap fixed in 4.0.4?"
    a: "No. Two pull requests, #9177 and #11293, proposed resolving the greeter layout from /etc/vconsole.conf, and neither was merged. The shipped default/sddm/hyprland.lua in the 4.0.4 tree still sets only misc and animations."
related: [black-screen-after-login, lock-screen-wont-unlock, luks-passphrase-not-accepted-at-boot, stuck-at-tty-or-cannot-switch-tty, nvidia-drivers-omarchy-4]
draft: false
---

There are two very different failures behind "Omarchy will not let me log in", and they need opposite fixes. Either the greeter rejects your password, or the greeter accepts it and the session dies a second later and drops you back. Everything below was checked against the 4.0.4 source tree, with 3.x differences called out.

## The fix

1. **Decide which failure you have.** Get a text console with Ctrl+Alt+F2, log in, then run:

   ```bash
   journalctl -u sddm -b | tail -40
   ```

   Lines like `pam_unix(sddm:auth): authentication failure` or `[PAM] authenticate: Authentication failure` mean the password was rejected. Go to step 2. A clean `Session started true` followed by the greeter returning a second later means authentication succeeded and the session crashed. Skip to step 6.

2. **Check whether you are simply locked out.** Omarchy raises the failure limit to ten attempts in `/etc/security/faillock.conf` and writes `unlock_time=120` into `/etc/pam.d/system-auth`, so a lockout normally clears itself after two minutes.

   ```bash
   faillock --user "$USER"
   sudo faillock --reset --user "$USER"
   ```

   The manual covers this under [Troubleshooting](https://omarchy.org/manual/troubleshooting/). If the output was empty, you were never locked out, and the password really is arriving wrong.

3. **Fix the greeter keyboard layout.** This is the single most common cause on any non-US layout. Check what the system thinks your layout is:

   ```bash
   localectl status
   grep -E 'KEYMAP|XKBLAYOUT|XKBVARIANT' /etc/vconsole.conf
   ```

   On 4.x, edit `/usr/share/sddm/hyprland.lua` and add an `input` table to the existing call:

   ```lua
   hl.config({
     input = {
       kb_layout = "fr",
       kb_variant = "",
     },

     misc = {
       disable_hyprland_logo = true,
       disable_splash_rendering = true,
       force_default_wallpaper = 0,
     },

     animations = {
       enabled = false,
     },
   })
   ```

   On 3.x the file is `/usr/share/sddm/hyprland.conf` and the syntax is the old block form:

   ```conf
   input {
     kb_layout = fr
   }
   ```

   On 4.x the `.lua` file belongs to the `omarchy-settings` package, so a package upgrade can overwrite it. Re-apply the edit after updates until this lands upstream. On 3.x, issue [#6880](https://github.com/omacom/omarchy/issues/6880) found `hyprland.conf` was not owned by any package, and its reporter kept the edit in a separate file under `/etc/sddm/` pointed at by a `CompositorCommand` drop-in instead.

4. **If you cannot edit anything yet, type the password in US positions.** The greeter is a plain US QWERTY keyboard no matter what the label on the key says. Several reporters got in this way and fixed the config afterwards.

5. **Check that SDDM knows who you are.** Two files matter:

   ```bash
   cat /etc/sddm.conf.d/autologin.conf
   cat /var/lib/sddm/state.conf
   ```

   `User=` must be your account. In issue [#5044](https://github.com/omacom/omarchy/issues/5044) it had been written as `root`, which loops forever. In issue [#7949](https://github.com/omacom/omarchy/issues/7949), after an interrupted install resumed through `arch-chroot`, SDDM authenticated an empty username and logged `User not known to the underlying authentication module`; writing a correct `[Autologin]` block was the workaround there.

6. **If the password is accepted and the session dies,** the compositor is failing, not PAM. Read `journalctl -b | grep -Ei 'hyprland|aquamarine|uwsm_env-preloader'` and check `~/.cache/hyprland/` for a crash report. Three causes have clear reports: an NVIDIA kernel and userspace mismatch after an update, a colon-bearing `AQ_DRM_DEVICES` value, and a shell error in `~/.config/uwsm/env.d/`. Those are covered on [/fix/black-screen-after-login/](/fix/black-screen-after-login/).

## Verify it worked

Log out from the Omarchy menu rather than rebooting, so you meet the real greeter instead of autologin. Type one layout-sensitive character into the username field first, such as the at sign or the underscore, and confirm it appears correctly. Then log in normally. Afterwards, `journalctl -u sddm -b | grep -c 'Authentication failure'` should return zero for that boot.

## Why it happens

SDDM starts a Wayland greeter by launching its own Hyprland instance. Omarchy's `/etc/sddm.conf.d/10-wayland.conf` sets `CompositorCommand=start-hyprland -- --config /usr/share/sddm/hyprland.lua`, and that config is deliberately minimal: in the 4.0.4 tree it declares only `misc` and `animations`. Hyprland has no reason to look at `/etc/vconsole.conf` or `/etc/X11/xorg.conf.d/00-keyboard.conf`, so `kb_layout` stays at its built-in default of `us`.

The session is fine, which is what makes this so confusing. Since 4.0.0 the shipped `default/hypr/input.lua` reads `/etc/vconsole.conf` at runtime and derives `kb_layout`, `kb_variant` and `kb_options` from it. The greeter never got the same treatment. Two pull requests offered to share that logic, [#9177](https://github.com/omacom/omarchy/pull/9177) and [#11293](https://github.com/omacom/omarchy/pull/11293), and neither was merged.

Autologin hides the bug. On an encrypted install the LUKS passphrase already gates access, so `omarchy-provision-owner` keeps the autologin drop-in permanently, and the `sddm-autologin` PAM service never checks a password at all. The first time you actually see the greeter is after a logout or a compositor crash, long after install, with nothing pointing at the layout. AltairSD described exactly that sequence in issue [#10269](https://github.com/omacom/omarchy/issues/10269).

One more trap worth knowing: SDDM does not filter `/etc/sddm.conf.d` by file extension, so a renamed `autologin.disabled` is still read. Move the file out of the directory instead.

## If that did not work

- **The loop started right after an update.** A failed DKMS build can leave a stale UKI whose embedded NVIDIA module no longer matches userspace, and Hyprland then aborts at EGL init. Issue [#5706](https://github.com/omacom/omarchy/issues/5706) walks through it. See [/fix/nvidia-drivers-omarchy-4/](/fix/nvidia-drivers-omarchy-4/).
- **You edited your monitor config recently.** In issue [#6439](https://github.com/omacom/omarchy/issues/6439) a fixed resolution and refresh rate made Hyprland fail silently; switching that entry to `preferred` restored login. See [/fix/monitors-conf-replaced-by-monitors-lua/](/fix/monitors-conf-replaced-by-monitors-lua/).
- **You changed your password from the Omarchy menu.** Issue [#9147](https://github.com/omacom/omarchy/issues/9147) reports `gkr-pam: couldn't unlock the login keyring.` and a reset progress bar on the next cold boot, because the keyring was not re-encrypted with the new password. That one is open and unfixed.
- **The machine reboots instead of looping.** On a ThinkPad T470 in issue [#8190](https://github.com/omacom/omarchy/issues/8190), a TPM that answered but timed out failed the PCR barrier unit and forced a reboot right after the password. Disabling the Security Chip in firmware was the workaround.
- **No console key works.** One commenter in #5706 could not reach any TTY from the loop. Reboot, pick an older entry in the Limine menu, and work from there. See [/fix/stuck-at-tty-or-cannot-switch-tty/](/fix/stuck-at-tty-or-cannot-switch-tty/) and [/upgrade/rollback-with-snapper-and-limine/](/upgrade/rollback-with-snapper-and-limine/).

Evidence for the keymap cause is strong and reproduced across `fr`, `be`, `de`, `es`, `gb`, Colemak and Russian layouts. Evidence for the keyring and TPM cases is a single report each, so treat those as leads rather than known answers.

## Related

- [/fix/black-screen-after-login/](/fix/black-screen-after-login/)
- [/fix/lock-screen-wont-unlock/](/fix/lock-screen-wont-unlock/)
- [/fix/luks-passphrase-not-accepted-at-boot/](/fix/luks-passphrase-not-accepted-at-boot/)
- [/switch/non-us-keyboard-layout-luks-sddm/](/switch/non-us-keyboard-layout-luks-sddm/)
- [/keyboard/layouts-and-locale/](/keyboard/layouts-and-locale/)
