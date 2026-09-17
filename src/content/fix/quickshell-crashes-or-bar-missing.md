---
title: "Quickshell crashes or the Omarchy bar is missing"
description: "The Omarchy 4 Quickshell bar vanished or omarchy-shell keeps crashing. Restart the shell, read its journal, reset a broken bar, fix a Qt ABI mismatch."
answer: "Run `omarchy restart shell` from a terminal. If it reports the shell is not running, check `journalctl -t omarchy-shell -b | tail -50`. A blank bar after cloning or setting a custom bar is fixed with `omarchy bar reset`. A shell that will not start at all after an update on the edge or rc channel is usually a quickshell and Qt version mismatch."
appliesTo:
  from: "4.0.0"
status: workaround
category: shell
issueCount: 547
errorStrings:
  - "Omarchy shell exited with status 255; relaunching."
  - "Giving up on the Omarchy shell after 6 relaunches in under a minute."
  - "omarchy-shell is not running"
  - "omarchy-shell is not responding"
  - "The Wayland connection experienced a fatal error: Invalid argument"
  - "Got removal for monitor \"FALLBACK\" which was not previously tracked."
  - "WARN scene: @shell.qml[256:-1]: ReferenceError: errorString is not defined"
  - "FATAL: Tried to show lockscreen surfaces without active lock"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [quickshell, bar, shell, quattro, crash, plugins]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7596"
    title: "Issue #7596: Quickshell unable to restart after latest update on Edge branch"
    kind: issue
    author: "agworkgit"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/8438"
    title: "Issue #8438: Omarchy 4.0.1 migration installs a Qt 6.11.2-built quickshell that cannot start on the Qt 6.11.1 pin"
    kind: issue
    author: "greencubator1"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/6952"
    title: "Issue #6952: Quickshell SIGSEGV in QQuickRepeater when PipeWire removes USB audio nodes"
    kind: issue
    author: "sanjyay"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/7783"
    title: "PR #7783: Keep PwNode objects out of the audio panel's Repeater models"
    kind: pr
    author: "omarchybot"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/7380"
    title: "Issue #7380: omarchy-shell crashes and relaunches on every wake from idle lock (FALLBACK monitor removal, fatal Wayland error)"
    kind: issue
    author: "mcjansen"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/10930"
    title: "Issue #10930: omarchy-launch-shell exits silently when compositor_alive() false-negatives during output reconfiguration, leaving no bar"
    kind: issue
    author: "matti-lamppu"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/7418"
    title: "Issue #7418: Cloning the bar plugin blanks the bar (broken Loader.Error fallback in shell.qml)"
    kind: issue
    author: "kesavsabari"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/10792"
    title: "Issue #10792: Cloning the built-in bar leaves no bar: Loader.Error handler throws ReferenceError, skipping the default-bar fallback"
    kind: issue
    author: "james-engelbrecht"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/7106"
    title: "Issue #7106: Saving a file under ~/.config/omarchy/plugins/ while locked strands the session, and omarchy-restart-shell refuses to help"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://omarchy.org/manual/the-top-bar/"
    title: "Omarchy manual: The Top Bar"
    kind: manual
    date: "2026-08-14"
credits:
  - name: "robouk"
    url: "https://github.com/robouk"
    for: "Traced the dead shell on the edge channel to a quickshell build against a newer Qt than the one installed"
  - name: "mouadse"
    url: "https://github.com/mouadse"
    for: "Confirmed the downgrade to the cached quickshell package restores the shell on rc"
  - name: "aml360"
    url: "https://github.com/aml360"
    for: "Found that the audio panel crash is far more frequent on Bluetooth AAC profiles than on SBC"
  - name: "matti-lamppu"
    url: "https://github.com/matti-lamppu"
    for: "Showed that the shell supervisor can give up silently during a dock hotplug, leaving no bar and no journal line"
faq:
  - q: "Is it safe to kill quickshell while the screen is locked?"
    a: "No. Killing the shell while the lock is held strands the session behind Hyprland's failsafe screen, which has no password box. omarchy-restart-shell refuses on purpose when the lock reports itself secure, and recovers the session only when the locker is already dead."
  - q: "Does restarting the shell lose anything?"
    a: "Open panels and on-screen notification popups are redrawn, and clipboard history and reminders live outside the process, so they survive. A restart does not touch your windows: Hyprland keeps running the whole time."
  - q: "Where are the crash logs?"
    a: "Quickshell writes crash reports under ~/.cache/quickshell/crashes/, and Omarchy pipes the shell's own output into the journal under the omarchy-shell tag, so journalctl -t omarchy-shell survives a reboot."
related: [where-did-waybar-go, plugin-fails-to-load, walker-launcher-missing-after-update, lock-screen-wont-unlock, notifications-not-showing]
draft: false
---

On Omarchy 4 the bar, the menu, notifications, OSD popups, the lock screen and the polkit agent are all plugins inside one Quickshell process called `omarchy-shell`. When that process dies you lose all of them at once, which is why a missing bar and a dead `SUPER + SPACE` menu are the same bug. This page was checked against the shipped source of 4.0.0 through 4.0.4. On 3.x the bar was Waybar in its own process, so none of this applies there. See [where did Waybar go](/fix/where-did-waybar-go/).

## The fix

Work through these in order. You need a terminal: `SUPER + RETURN` still works while the shell is down, because Hyprland is a separate process.

1. **Rule out the hide toggle.** `SUPER + SHIFT + SPACE` hides the bar without killing the shell. If the menu and notifications still work, you probably hid it. Press it again, or delete the flag file directly:

   ```bash
   rm -f ~/.local/state/omarchy/toggles/bar-off
   omarchy restart shell
   ```

2. **Restart the shell.**

   ```bash
   omarchy restart shell
   ```

   Same thing from the menu under _Update > Process > Shell_. The script kills every running instance, respawns it through Hyprland so it inherits the session environment, and waits for it to answer. It refuses while the session is genuinely locked and secure. If the lock client died and you are stuck on Hyprland's failsafe screen, run it from a TTY (`CTRL + ALT + F2`) and it will restart the shell and re-secure the lock so you can type your password again.

3. **Read the log before guessing.** Omarchy pipes the shell into the journal:

   ```bash
   journalctl -t omarchy-shell -b --no-pager | tail -50
   ls -t ~/.cache/quickshell/crashes/ | head
   ```

   Lines like `Omarchy shell exited with status 255; relaunching.` mean it crashed and came back. `Giving up on the Omarchy shell after 6 relaunches in under a minute.` means the supervisor stopped trying.

4. **If the shell will not start at all, check the package.** On the edge and rc channels in August 2026, a `quickshell-git` build compiled against Qt 6.11.2 was installed next to Qt 6.11.1, and the shell died instantly with a symbol lookup error. Quickshell links Qt's private ABI, so it has to be rebuilt for every Qt release. Check it by hand:

   ```bash
   quickshell --version
   ```

   If that prints `symbol lookup error`, reinstall from the repo or roll back to the cached package, as confirmed in [#7596](https://github.com/omacom/omarchy/issues/7596):

   ```bash
   sudo pacman -U /var/cache/pacman/pkg/quickshell-git-*-1-x86_64.pkg.tar.zst
   omarchy restart shell
   ```

   Moving back to the stable channel also cleared it for several people. Stable was never affected. See [releases and channels](/releases/channels/).

5. **If you cloned or replaced the bar, reset it.**

   ```bash
   omarchy bar reset      # back to the built-in omarchy.bar
   omarchy plugin list    # see which plugins are enabled
   ```

   On 4.0.0 through 4.0.2, `omarchy plugin clone omarchy.bar` produced a bar that never rendered, and the fallback to the built-in bar was itself broken, so you got nothing at all. Both halves changed in 4.0.3: the built-in bar's injected properties are no longer `required`, and the loader's error handler no longer references an undefined `errorString`. If you are still on 4.0.2 or earlier, update first.

6. **If a third-party plugin is the suspect**, disable it and restart:

   ```bash
   omarchy plugin disable <plugin.id>
   omarchy restart shell
   ```

7. **Last resort: reset the shell config.**

   ```bash
   omarchy refresh shell
   ```

   That restores `~/.config/omarchy/shell.json` to the shipped defaults, keeps a timestamped `.bak` copy of yours, resets the bar layout and restarts the shell.

## Verify it worked

```bash
omarchy-shell shell ping
hyprctl layers -j | jq '[.[].levels[][].namespace]'
hyprctl monitors -j | jq '.[].reserved'
journalctl -t omarchy-shell -b --no-pager | tail -20
```

`ping` should answer, the layer list should contain `omarchy-bar`, and each monitor should reserve space for the bar rather than reporting zeros on every edge. The last command should show no new relaunch lines after your fix.

## Why it happens

Quickshell is one long-lived QML process. `omarchy-launch-shell` supervises it, because Qt can leave through `_exit()` on a fatal Wayland error without raising a signal, so there is no core dump and nothing to relaunch it otherwise. The supervisor allows five relaunches in sixty seconds before giving up.

The crashes reported most often on 4.0.x fall into a few families:

- **Audio graph churn.** The audio panel's refresh timer hands a Repeater rows that still hold PipeWire node objects, and Qt segfaults when one of those objects has already been destroyed. Unplugging USB audio, a Bluetooth reconnect, `omarchy-restart-audio` and plain suspend all reach it ([#6952](https://github.com/omacom/omarchy/issues/6952)). A maintainer reproduced it ten times out of ten in a VM and confirmed the Qt 6.11.2 point release does not fix it. The proposed fix, [PR #7783](https://github.com/omacom/omarchy/pull/7783), was still open when this page was checked.
- **Output changes.** On wake from an idle lock, or during a dock or HDMI reconfiguration, Hyprland reports the removal of a monitor the shell never tracked, the Wayland connection fails, and the shell exits with status 255 and relaunches ([#7380](https://github.com/omacom/omarchy/issues/7380)). Users have reported this on NVIDIA, on Intel-only laptops, and on displays that drop their connector in standby.
- **The supervisor giving up quietly.** If the compositor is too busy to answer `hyprctl` during a display bring-up, the liveness check false-negatives and the supervisor exits without logging anything, leaving a running session with no bar and no explanation ([#10930](https://github.com/omacom/omarchy/issues/10930)).
- **Plugin reloads during a lock.** Editing or syncing a file under `~/.config/omarchy/plugins/` while the session is locked can abort the shell with a fatal lock-surface error, sometimes long after the edit ([#7106](https://github.com/omacom/omarchy/issues/7106)).
- **Bar plugin load failures**, covered in step 5 above.

## If that did not work

Avoid the audio panel crash while it is unfixed: close the panel before you unplug a USB interface, switch a Bluetooth profile or restart audio, because the refresh path returns immediately when the panel is closed. One reporter in [#6952](https://github.com/omacom/omarchy/issues/6952) also found that keeping Bluetooth headphones on an SBC profile rather than AAC made the crash stop.

If the shell crashes in a loop from boot, roll back to the snapshot before your last update and try again on a later release. See [rollback with snapper and Limine](/upgrade/rollback-with-snapper-and-limine/) and [before you update](/upgrade/before-you-update-checklist/).

Collect `omarchy-debug` output and the journal excerpt before filing anything. Many of the open reports above are already detailed; adding your hardware, channel, `quickshell --version` and the exact log lines to the matching issue is more useful than a new one.

## Related

- [Where did Waybar go](/fix/where-did-waybar-go/)
- [Plugin fails to load](/fix/plugin-fails-to-load/)
- [Walker launcher missing after the update](/fix/walker-launcher-missing-after-update/)
- [Lock screen will not unlock](/fix/lock-screen-wont-unlock/)
- [Notifications not showing](/fix/notifications-not-showing/)
- [Omarchy manual: The Top Bar](https://omarchy.org/manual/the-top-bar/) and [Shell Plugins](https://omarchy.org/manual/shell-plugins/)
