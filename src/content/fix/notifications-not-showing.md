---
title: "Notifications not showing"
description: "No notification toasts on Omarchy 4? Check do-not-disturb, find out which daemon owns org.freedesktop.Notifications, and test with notify-send."
answer: "Check do-not-disturb first: run omarchy-shell notifications dndState, and press Super + Ctrl + comma to turn it off. If it is already off, another daemon such as xfce4-notifyd or dunst has claimed org.freedesktop.Notifications; kill it and mask its D-Bus activation file. If nothing owns the name, the Quickshell shell is down, so run omarchy restart shell."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 231
errorStrings:
  - "--exec takes the command as separate words, not one quoted string."
  - "Usage: omarchy-notification-send"
tags: [notifications, quickshell, do-not-disturb, shell, quattro]
sources:
  - url: "https://github.com/omacom/omarchy/issues/9149"
    title: "Issue #9149: Notifications are not showing up properly"
    kind: issue
    author: "Danannme"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10023"
    title: "Issue #10023: Cloning a service plugin silently breaks its bar indicator"
    kind: issue
    author: "simonlomax"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/8638"
    title: "Issue #8638: 4.0.1 breaks the invitation hooks 4.0.0 installed in user config"
    kind: issue
    author: "tecnarchico"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9394"
    title: "Issue #9394: v4.0.2 package missing hover-revealed notification close button"
    kind: issue
    author: "johnpippett"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9671"
    title: "Issue #9671: Shell restores unbounded backlog of stale never-expiring critical popups after power loss"
    kind: issue
    author: "calumol"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/pull/7926"
    title: "PR #7926: Run notification click actions as safe argv"
    kind: pr
    author: "ryanrhughes"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/9361"
    title: "Issue #9361: Critical notifications have no visible close button and never auto-expire"
    kind: issue
    author: "mrocha-montes"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/10145"
    title: "Issue #10145: Identical notifications are no longer grouped since the Quickshell notification daemon replaced mako"
    kind: issue
    author: "rdjperron"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/7834"
    title: "Issue #7834: Notification replacement hints honoured by mako are ignored by the 4.0 shell"
    kind: issue
    author: "lucletoffe"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7195"
    title: "Issue #7195: Notification toasts render on every connected monitor"
    kind: issue
    author: "EduardsSk"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7183"
    title: "Issue #7183: omarchy-font-set notifications never fire because -g consumes the message as a glyph"
    kind: issue
    author: "WhiskeyTuesday"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/10133"
    title: "Issue #10133: omarchy font set prints omarchy-notification-send usage error when the font name contains a space"
    kind: issue
    author: "TheRealGhost007"
    date: "2026-09-04"
  - url: "https://omarchy.org/manual/toggles-idle-screensaver/"
    title: "Omarchy manual: Toggles, Idle & the Screensaver"
    kind: manual
    date: "2026-09-16"
  - url: "https://omarchy.org/manual/notices/"
    title: "Omarchy manual: Notices"
    kind: manual
    date: "2026-09-16"
credits:
  - name: "Rockeyxx"
    url: "https://github.com/Rockeyxx"
    for: "Traced silent, unstyled notifications to xfce4-notifyd hijacking the org.freedesktop.Notifications bus name, and published the D-Bus masking workaround"
  - name: "simonlomax"
    url: "https://github.com/simonlomax"
    for: "Showed that a cloned notifications plugin leaves the do-not-disturb indicator dead, so the desktop looks broken rather than silenced"
  - name: "tecnarchico"
    url: "https://github.com/tecnarchico"
    for: "Found that 4.0.1 tightened omarchy-notification-send --exec and broke the hooks 4.0.0 had already written into user config"
faq:
  - q: "Is Mako still the notification daemon on Omarchy 4?"
    a: "No. Omarchy 4.0.0 replaced Mako with a notifications plugin inside the single Quickshell shell process. makoctl is gone, and the Quattro upgrade removes the mako package, disables mako.service, and backs up ~/.config/mako."
  - q: "How do I see notifications I missed?"
    a: "Press Super + Shift + Alt + comma, or run omarchy-shell notifications showHistory. The shell keeps the last ten, including the ones do-not-disturb silenced."
  - q: "Why did notify-send show nothing while a critical notify-send worked?"
    a: "That is do-not-disturb. The 4.x daemon lets a notify-send message through DND only when its urgency is critical, and it does not even record a silenced plain notify-send in history."
related: [quickshell-crashes-or-bar-missing, where-did-waybar-go, plugin-fails-to-load, clipboard-history-not-working]
draft: false
---

Omarchy 4 has no Mako. Since 4.0.0 "Quattro" the notification daemon is a plugin called `omarchy.notifications` living inside the one long-running Quickshell process that also draws the bar, the menu, the OSDs and the lock screen. So when no toast appears, the cause is usually one of four things: do-not-disturb is on, a foreign daemon grabbed the D-Bus name, the shell is not running, or the plugin is off. Work them in that order.

Checked on v4.0.4 source, with v4.0.0 through v4.0.3 and v3.8.4 compared.

## The fix

### 1. Check do-not-disturb

```bash
omarchy-shell notifications dndState
```

`on` means every popup is being suppressed. Turn it off with `Super + Ctrl + comma`, from the _Trigger > Toggle_ menu (`Super + Ctrl + O`), or:

```bash
omarchy toggle notification silencing
```

Nothing was lost. Replay the last ten with `Super + Shift + Alt + comma`, which is `omarchy-shell notifications showHistory`. If the history is full of what you were waiting for, DND was the whole story. See the manual chapter on [toggles, idle and the screensaver](https://omarchy.org/manual/toggles-idle-screensaver/).

On 3.x this switch was Mako's: `makoctl mode -t do-not-disturb`. Neither `makoctl` nor that mode exists on 4.x.

### 2. Send one message DND cannot swallow

```bash
notify-send -u critical "critical test"
notify-send "plain test"
```

The 4.x daemon lets a `notify-send` message past DND only when its urgency is critical. If the critical one appears and the plain one does not, you are still in DND no matter what step 1 printed. If neither appears, carry on.

### 3. Find out who owns the notification bus name

```bash
busctl --user call org.freedesktop.Notifications /org/freedesktop/Notifications \
  org.freedesktop.Notifications GetServerInformation
```

That returns the server name, vendor and version of whatever currently answers. If it errors, nothing is listening. If it names something that is not the Omarchy shell, a stray daemon took the name:

```bash
pgrep -a 'dunst|mako|swaync|xfce4-notifyd'
```

On issue #9149 the reporter had dead notification keybindings and unstyled popups. Rockeyxx traced the same symptoms to `xfce4-notifyd` auto-activating on D-Bus and hijacking `org.freedesktop.Notifications`. Kill the process, then shadow its activation file so it cannot come back:

```bash
mkdir -p ~/.local/share/dbus-1/services
ln -sf /dev/null ~/.local/share/dbus-1/services/org.xfce.xfce4-notifyd.Notifications.service
```

The same shadowing works for any other daemon: find its `.service` file under `/usr/share/dbus-1/services/` and symlink a file of that exact name to `/dev/null` in your user directory. Then restart the shell. The Quattro upgrade already uninstalls the `mako` package, retires `mako.service` and moves `~/.config/mako` aside, so a surviving Mako only happens if you reinstalled it yourself.

### 4. Restart the shell

If the Quickshell process died you lose the bar, the menu and notifications together.

```bash
omarchy restart shell
```

### 5. Confirm the plugin is enabled

```bash
omarchy plugin list | grep notifications
```

`omarchy.notifications` is first party and on by default. It only turns off by being listed in `disabledPlugins[]` in `~/.config/omarchy/shell.json`. Delete it from that array and restart the shell.

## Verify it worked

Wait for the server to claim the bus, then send one of each kind:

```bash
omarchy-notification-wait 10 && echo "server up"
notify-send "hello" "body text"
omarchy notification send "Hello" "From omarchy" -u normal
```

A low-urgency toast lasts 5 seconds, a normal one 8, and a critical one does not auto-expire at all. Dismiss the newest with `Super + comma`, clear them all with `Super + Shift + comma`, and open history with `Super + Shift + Alt + comma`. The date and battery notices on `Super + Ctrl + Alt + T` and `Super + Ctrl + Alt + B` are a quick second check, since both are sent with `omarchy-notification-send` and go through the same daemon. The weather hotkey on `W` is not a notification, it toggles the weather bar widget, so it proves nothing here. All three are documented in the [notices chapter](https://omarchy.org/manual/notices/).

## Why it happens

The DND preference is persistent user state, stored as a `dnd` key in `~/.local/state/omarchy/notifications.json` and read back at shell startup, so it survives reboots and updates. That is how one accidental keypress leaves a desktop quiet for days.

Two categories still get through DND by design. Omarchy's own confirmation toasts, which use the app name `omarchy-action`, and command-line alerts sent with urgency critical and the default `notify-send` app name. Chat apps that mark everything critical do not qualify, because they set their own app name.

There is a trap in testing here. The daemon treats `notify-send` and `omarchy-action` as ephemeral senders, so a plain `notify-send` that DND silences is not even written to history. "I tested with notify-send, nothing appeared, and history was empty" is exactly what DND looks like, not a second bug.

The visual cue for DND is a crossed-out bell indicator in the bar. If you have run `omarchy plugin clone omarchy.notifications`, that indicator stops working. simonlomax documented the cause on issue #10023: the bar indicator asks `firstPartyServiceFor()` for `omarchy.notifications`, and that function reads the service table by the built-in id without first resolving it to the enabled clone, so it gets null. IPC calls do go through the resolver, which is why the hotkey and the menu entry still toggle DND while the bar shows nothing and clicking where the bell should be does nothing. Still open as of 4.0.4; the proposed fix, PR #10429, is not merged.

## If that did not work

Your own scripts stopped notifying after 4.0.1. PR #7926 tightened `omarchy-notification-send` so `--exec` takes the command as separate words. The old quoted single-string form now prints `--exec takes the command as separate words, not one quoted string.` and exits. tecnarchico reported on issue #8638 that this broke the first-run hooks 4.0.0 had itself written into `~/.config/omarchy/hooks/post-update.d/`. Rewrite any `--exec "prog arg"` as `--exec prog arg`.

The other way to get the `Usage: omarchy-notification-send` line instead of a toast is to feed the headline to a flag that takes a value. `-g` wants a glyph, so `omarchy-notification-send -g "Restart the terminal"` swallows the message as the glyph and has no headline left. Omarchy's own `omarchy font set` still makes exactly that call in 4.0.4, which is why issues #7183 and #10133 report the usage text, or no toast at all, after a font change. Give every value-taking flag its value and pass the headline as its own argument.

Toasts that show but seem to vanish are a different set of open bugs: identical notifications are no longer grouped (issue #10145), and senders that update a toast in place stack a new one per update instead (issue #7834). Popups also render on every connected monitor at once rather than the focused one (issue #7195).

Stuck toasts are the inverse problem and are also open. Critical notifications never auto-expire (`durationFor` returns 0 for them, tracked on issue #9361), and the hover-revealed close button that landed on the development branch is still absent from the packaged tree in v4.0.4, so right-click or `Super + comma` is the only way to clear one. calumol showed on issue #9671 that a hard power-off can leave the shell rehydrating hundreds of stale critical toasts on the next boot, plus zero-byte state files under `~/.local/state/omarchy/notifications/` that come back as blank popups. Deleting those files by hand is the only cleanup today.

If none of this applies, gather `omarchy-shell notifications dndState`, the `GetServerInformation` output and your Omarchy version before filing, because those three lines separate all four causes above.

## Related

- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Where did Waybar go](/fix/where-did-waybar-go/)
- [Plugin fails to load](/fix/plugin-fails-to-load/)
- [Upgrading 3 to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Omarchy commands reference](/reference/commands/)
- [Keybindings reference](/reference/keybindings/)
