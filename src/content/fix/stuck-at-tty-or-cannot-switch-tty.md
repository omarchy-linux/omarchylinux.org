---
title: "Stuck at a TTY, or cannot switch to a TTY on Omarchy"
description: "Stuck at a text console on Omarchy 4, or Ctrl+Alt+F keys do nothing: which VT to use, how to read the uwsm session log, and how to start Hyprland by hand."
answer: "Press Ctrl+Alt+F2 through F6, log in with your user password, and read journalctl --user -b -u wayland-wm-env@hyprland.desktop.service. A shell error in ~/.profile or ~/.config/uwsm/env.d aborts the session silently. Start it by hand with uwsm start -g -1 -e -D Hyprland hyprland.desktop. If no F-key reaches a TTY, the compositor is wedged and only a reboot or SSH gets you back."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: boot
issueCount: 165
errorStrings:
  - "failed to get hyprland version string (bad json)"
  - "Greeter stopped. SDDM::Auth::HELPER_TTY_ERROR"
  - "wayland-wm-env@hyprland.desktop.service: Failed with result 'exit-code'."
  - "Unknown Omarchy command: omarchy debug"
tags: [tty, boot, uwsm, sddm, hyprland, recovery]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8669"
    title: "Issue #8669: Rust install leaves unguarded ~/.profile cargo source that can login-loop UWSM"
    kind: issue
    author: "pkayokay"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/10700"
    title: "Issue #10700: Silent lock-screen login loop when ~/.config/uwsm/env.d has a shell error (UWSM preloader fails with no UI)"
    kind: issue
    author: "austrasien"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/11700"
    title: "Issue #11700: SwitchToGreeter freezes the session: greeter relaunch targets the occupied VT (HELPER_TTY_ERROR)"
    kind: issue
    author: "MAXIDEA"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/8319"
    title: "Issue #8319: After omarchy update + reboot: 'failed to get hyprland version string (bad json)', NVIDIA initramfs migration may break boot"
    kind: issue
    author: "mayounderrated"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/11208"
    title: "Issue #11208: Lock screen freezes / keyboard input unresponsive after suspend-resume until DRM/VT switch"
    kind: issue
    author: "OP017"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10258"
    title: "Issue #10258: omarchy debug command is unreachable via the CLI router despite being advertised in --help"
    kind: issue
    author: "ajgorrell"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/discussions/7758"
    title: "Discussion #7758: Omarchy on VirtualBox"
    kind: discussion
    author: "nightdevil00"
    date: "2026-08-22"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "pkayokay"
    url: "https://github.com/pkayokay"
    for: "Traced a bounced login to an unguarded cargo line in ~/.profile that kills the uwsm env preloader"
  - name: "austrasien"
    url: "https://github.com/austrasien"
    for: "Showed that a bad file in ~/.config/uwsm/env.d fails the session silently, and that renaming it in place does not disable it"
  - name: "MAXIDEA"
    url: "https://github.com/MAXIDEA"
    for: "Found that SwitchToGreeter relaunches the greeter onto the occupied VT and freezes the display"
  - name: "mayounderrated"
    url: "https://github.com/mayounderrated"
    for: "Spotted a stale /usr/local/bin/start-hyprland shadowing the packaged one in PATH"
  - name: "OP017"
    url: "https://github.com/OP017"
    for: "Documented a VT switch restoring keyboard input to a frozen lock screen after resume"
  - name: "rodolfoghi"
    url: "https://github.com/rodolfoghi"
    for: "Diagnosed a VM black screen from a TTY by running Hyprland by hand and checking the runtime dirs"
faq:
  - q: "Which function key gets me a TTY on Omarchy?"
    a: "Ctrl+Alt+F2 through Ctrl+Alt+F6. VT1 is taken by the SDDM greeter and by your Hyprland session, so F1 takes you back to the desktop rather than to a console."
  - q: "Do I type my LUKS passphrase at the TTY login prompt?"
    a: "No. The console login wants your Linux username and its password. The LUKS passphrase is only asked for once, by the bootloader, before the kernel starts."
  - q: "How do I start the desktop from a TTY?"
    a: "Run uwsm start -g -1 -e -D Hyprland hyprland.desktop, which is exactly what Omarchy's session entry runs. Run plain Hyprland instead if you want the crash output on screen."
  - q: "Why does Ctrl+Alt+F2 do nothing when the screen is frozen?"
    a: "Hyprland owns the keyboard on that VT and performs the switch itself. A compositor stuck in a GPU or output operation never processes the key combination, so nothing happens and only a reboot or an SSH session gets you back."
related: [black-screen-after-login, login-loop-or-password-not-accepted-sddm, quickshell-crashes-or-bar-missing, lock-screen-wont-unlock]
draft: false
---

A TTY is the plain text console behind the desktop. On Omarchy it is both a symptom (you booted and landed there instead of on the desktop) and the main repair tool (the desktop is broken and you need a shell). This page covers both, on 4.0.0 through 4.0.4, with the 3.x differences noted.

## The fix

**1. Get to a console.** Press `Ctrl+Alt+F2`. If that bounces you straight back, try `F3`, `F4`, `F5` and `F6`. VT1 is not free: SDDM's greeter and your Hyprland session both sit there. You can see it in SDDM's own log, which prints `Jumping to VT 1` when it restarts a greeter, and in `omarchy-debug` output, which reports `vt 1` for the desktop. Omarchy ships no logind override for the auto-spawned consoles, so Arch's default login prompts on VT2 through VT6 are what you get. `Ctrl+Alt+F1` returns you to the session.

At the `login:` prompt use your Linux username and its password. Not the LUKS passphrase, which is only used once by the bootloader.

**2. Find out what is missing.** From the console:

```bash
systemctl status sddm
journalctl -b -u sddm
journalctl --user -b -u wayland-wm-env@hyprland.desktop.service
journalctl --user -b -u wayland-wm@hyprland.desktop.service
journalctl -b -t omarchy-shell
```

Omarchy starts Hyprland through uwsm on both 3.x and 4.x. The session entry is identical in v3.8.4 and v4.0.4: `Exec=uwsm start -g -1 -e -D Hyprland hyprland.desktop`. That produces two user units, the environment preloader and the compositor itself, and that first unit is where most silent failures live.

**3. Check the uwsm environment first.** If the greeter takes your password, flashes, and returns to the greeter while the TTY works fine, this is almost always it. uwsm sources `~/.profile` and everything in `~/.config/uwsm/env.d/` before starting Hyprland, and any shell error aborts the session with nothing on screen.

Two confirmed shapes. In issue #8669 a Mac user on 4.0.1 had rustup's unguarded `. "$HOME/.cargo/env"` as line 1 of `~/.profile` with the file gone, and the journal showed `wayland-wm-env@hyprland.desktop.service: Failed with result 'exit-code'`. In issue #10700 on 4.0.2 a typo in an `env.d` fragment produced `Env output mark ... not found in shell output` and an endless return to the lock screen. Guard the profile line or delete it:

```bash
sed -i 's|^\. "\$HOME/.cargo/env"|[[ -r "$HOME/.cargo/env" ]] \&\& . "$HOME/.cargo/env"|' ~/.profile
```

For `env.d`, move the file out of the directory. Renaming it to `.bak` or `.broken` does not help, because uwsm loads every entry it finds there:

```bash
mkdir -p ~/broken-env && mv ~/.config/uwsm/env.d/99-bad ~/broken-env/
```

Note that a Snapper rollback will not fix either one. Both files live under `/home`, which snapshots of the root subvolume do not carry.

**4. Start the session by hand.** Still on the TTY:

```bash
uwsm start -g -1 -e -D Hyprland hyprland.desktop
```

If that fails or exits instantly, run the compositor bare so the crash lands on your screen instead of in a log:

```bash
Hyprland
```

That is how the VirtualBox diagnosis in discussion #7758 was done: `Hyprland` aborted with signal 6 right after `Creating the AsyncResourceGatherer!`, which put the fault at GPU and EGL init rather than anywhere in Omarchy.

If you use the `start-hyprland` wrapper, call it by absolute path as `/usr/bin/start-hyprland`. Issue #8319 found a stale `hyprpm`-built copy at `/usr/local/bin/start-hyprland` shadowing the packaged one in PATH; the SDDM session entry is unaffected because it uses the absolute path, but your typed command is not.

**5. Check the config, then the shell.** `hyprctl configerrors` reports a bad config. On 4.x that config is `~/.config/hypr/hyprland.lua` and edits to a leftover `hyprland.conf` are ignored; on 3.x it is the `.conf` file. If Hyprland is up but there is no bar, `omarchy-restart-shell` works from a TTY, because it derives the Hyprland instance signature from the runtime directory and respawns the shell through the compositor.

**6. Collect a log.** Run `omarchy-debug --no-sudo`, which writes `/tmp/omarchy-debug.log`. Call the script directly. As of 4.0.2, `omarchy debug` through the CLI router answers `Unknown Omarchy command: omarchy debug` (issue #10258, open at the time of writing).

## Verify it worked

```bash
systemctl --user status wayland-wm@hyprland.desktop.service
hyprctl monitors
hyprctl layers | grep omarchy-bar
```

The unit should be active, `hyprctl monitors` should list a real output rather than error out, and the `omarchy-bar` layer should be present. Then press `Ctrl+Alt+F2` and `Ctrl+Alt+F1` once each: a session that survives a round trip through a console is a session whose compositor is answering.

## Why it happens

The greeter and the session share VT1, and everything else is queued behind that. When SDDM is asked to put a second greeter on the same VT, its helper cannot take the tty and the display dies with `Greeter stopped. SDDM::Auth::HELPER_TTY_ERROR`, which is what issue #11700 reports from a `SwitchToGreeter` D-Bus call on 4.0.3. Do not call it; start a second session from a spare TTY instead.

Landing on a console instead of the desktop means something in the chain exited: SDDM, the uwsm preloader, or Hyprland. The preloader case is silent by design, which is why it accounts for so many "wrong password" reports that turn out to be nothing of the sort. The Hyprland case is usually GPU init, and it looks the same whether the cause is a VM without working 3D or an initramfs that came back without the NVIDIA modules.

The reverse problem, no console at all, has a different root. Under Wayland the compositor owns the keyboard on its VT and carries out the switch itself, so `Ctrl+Alt+F<n>` is a request to Hyprland rather than to the kernel console. A compositor that is wedged in a GPU or output operation never processes it. This also explains why a VT switch is such a reliable unsticker when the compositor is alive but confused: issue #11208 on 4.0.3 describes a lock screen that ignores the keyboard after resume until `Ctrl+Alt+F3` and back forces a DRM and VT transition, after which typing works again.

## If that did not work

If no function key reaches a console, you have three options left. SSH in from another machine, if you turned sshd on beforehand. Power cycle and pick an older snapshot in the Limine menu, covered in [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/). Or boot the install media and chroot in.

If the console works but the desktop still will not start, the fault is downstream of this page. Go to [black screen after login](/fix/black-screen-after-login/) when Hyprland starts and nothing draws, [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/) when Hyprland is running without a bar, and [login loop or password not accepted](/fix/login-loop-or-password-not-accepted-sddm/) when the greeter keeps coming back. NVIDIA machines that stopped booting after an update belong on [the NVIDIA hardware page](/hardware/nvidia/), and virtual machines on [what breaks in a VM](/run/what-breaks-in-a-vm/).

One honest gap: the issue tracker has plenty of reports of the console being used as a rescue shell, and several of sessions frozen hard enough that nothing responds, but very few that isolate why a specific machine refuses the VT switch. If yours does, the journal from the next boot is the only evidence worth filing.

## Related

- [Black screen after login](/fix/black-screen-after-login/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Login loop or password not accepted](/fix/login-loop-or-password-not-accepted-sddm/)
- [Lock screen will not unlock](/fix/lock-screen-wont-unlock/)
- [Rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
- Omarchy manual: [Troubleshooting](https://omarchy.org/manual/troubleshooting/)
