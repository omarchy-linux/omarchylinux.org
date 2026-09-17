---
title: "Omarchy shell plugin fails to load or the bar disappears"
description: "A third-party or cloned Omarchy shell plugin will not load, or installing one leaves no bar at all. How to find the failing plugin, validate it, and remove it."
answer: "Open a terminal with SUPER + RETURN, run omarchy plugin list to see what is installed, then omarchy plugin disable <id> or omarchy plugin remove <id> and omarchy restart shell. If the bar is gone entirely, run omarchy bar reset first. Check the real error with journalctl -t omarchy-shell -b, and validate your own plugin with omarchy plugin validate <folder>."
appliesTo:
  from: "4.0.0"
status: workaround
category: shell
issueCount: 160
errorStrings:
  - "WARN scene: @shell.qml[256:-1]: ReferenceError: errorString is not defined"
  - "Required property barConfig was not initialized"
  - "Required property barWidgetRegistry was not initialized"
  - "panel plugin <id> failed to load:"
  - "Plugin widget <id> failed:"
  - "Unable to assign [undefined] to QObject*"
  - "plugin id 'x' uses the reserved omarchy.* namespace"
  - "kind 'bar' requires an 'entryPoints.bar' to load"
  - "symlinks are not allowed inside a plugin folder"
  - "plugin 'x' is not known; run: omarchy-shell shell rescanPlugins"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [plugin, quickshell, shell, bar, manifest, sandbox]
sources:
  - url: "https://omarchy.org/manual/shell-plugins/"
    title: "Omarchy manual: Shell Plugins"
    kind: manual
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3: restrict plugin access to authentication services"
    kind: release
    author: "ryanrhughes"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Release v4.0.1: guard plugin-add against git transport-helper URLs, fix Clone Plugin"
    kind: release
    author: "dhh"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7253"
    title: "Issue #7253: Cloned or third-party bar plugin fails to load, leaving no bar and no error"
    kind: issue
    author: "koenhendriks"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/6915"
    title: "Issue #6915: Shell: third-party bar plugins never load, required properties are set after construction"
    kind: issue
    author: "andrepadez"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/9116"
    title: "Issue #9116: Failed bar option leaves no bar at all, pluginBarLoader error handler throws ReferenceError before the fallback runs"
    kind: issue
    author: "hshshshs12"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10745"
    title: "Issue #10745: Custom bar/panel plugins fail silently, ReferenceError in Loader error handler swallows the diagnostic"
    kind: issue
    author: "ltehacker"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10556"
    title: "Issue #10556: Custom bar plugin fails to load, cloning the built-in bar breaks the shell"
    kind: issue
    author: "toppzi"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/10863"
    title: "Issue #10863: Regression 4.0.2 to 4.0.3, publicPluginManifest() strips __sourceDir"
    kind: issue
    author: "redglover"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10908"
    title: "Issue #10908: Third-party menu clones get null appLibrary in 4.0.3, Apps submenu empty"
    kind: issue
    author: "crueber"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10929"
    title: "Issue #10929: 4.0.3 bar-widget sandbox drops the bar drag API from PluginBarApi"
    kind: issue
    author: "aksasahara"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10888"
    title: "Issue #10888: 4.0.3 bar-widget sandbox leaves no way for a plugin to enumerate plugins"
    kind: issue
    author: "PapaHawk14"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10937"
    title: "Issue #10937: 4.0.3 bar-widget sandbox scopes _moduleWidgets to the caller"
    kind: issue
    author: "PeterHennesey"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10814"
    title: "Issue #10814: Cloning a service and bar-widget plugin silently breaks its widget"
    kind: issue
    author: "nanfxqs"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/9772"
    title: "Issue #9772: Plugin hot reload never clears the QML component cache"
    kind: issue
    author: "johnstoj"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/9304"
    title: "Issue #9304: omarchy plugin add --enable, one-shot enablePlugin IPC times out and the plugin lands disabled"
    kind: issue
    author: "nocstah"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/11062"
    title: "Issue #11062: plugin enable and bar put report success without placing a widget"
    kind: issue
    author: "kevinbsr"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10706"
    title: "Issue #10706: Editing any plugins file while locked aborts the shell"
    kind: issue
    author: "johnldean"
    date: "2026-09-07"
credits:
  - name: "koenhendriks"
    url: "https://github.com/koenhendriks"
    for: "Traced the missing bar to required properties in Bar.qml plus the swallowed Loader error, and confirmed the recovery path"
  - name: "hshshshs12"
    url: "https://github.com/hshshshs12"
    for: "Identified the ReferenceError in the bar Loader error handler that blocks the default-bar fallback"
  - name: "redglover"
    url: "https://github.com/redglover"
    for: "Found that 4.0.3 strips __sourceDir, so plugins can no longer locate their own bundled scripts"
  - name: "crueber"
    url: "https://github.com/crueber"
    for: "Isolated the null appLibrary on third-party menu plugins with a minimal repro"
  - name: "johnstoj"
    url: "https://github.com/johnstoj"
    for: "Showed that plugin hot reload never clears the QML component cache"
faq:
  - q: "How do I get the bar back right now?"
    a: "Open a terminal with SUPER + RETURN, run omarchy bar reset to switch back to omarchy.bar, then omarchy restart shell. If a widget rather than the bar is the problem, omarchy plugin disable <id> is enough."
  - q: "Where does the real error message go?"
    a: "The shell is launched through systemd-cat with the tag omarchy-shell, so journalctl -t omarchy-shell -b shows the QML warnings. Bar widget and service load failures print there. Panel load failures do not, because of an open bug in the error handler."
  - q: "Does omarchy plugin validate catch everything?"
    a: "No. It checks the manifest, entry points, reserved ids and symlinks, the same checks the registry runs. It does not run your QML, so a syntax error or a missing import still only shows up at load time."
  - q: "Did 4.0.3 break my working plugin?"
    a: "It can have. 4.0.3 put third-party plugins behind a scoped API. Plugins that reached into the shell's internals for the plugin registry, the bar drag surface or their own source directory lost that access, usually with no visible error."
related: [quickshell-crashes-or-bar-missing, where-did-waybar-go, walker-launcher-missing-after-update, theme-not-applied-to-gtk4-apps]
draft: false
---

Since Omarchy 4.0.0 the whole desktop is one Quickshell process, and nearly every visible piece of it is a plugin. That is why a single bad plugin can take the bar, a panel or an overlay with it. The failure is usually silent: no dialog, no notification, just a missing piece of the desktop.

Checked on 4.0.4 against the source snapshots for 4.0.0 through 4.0.4. None of this applies to 3.x, which had no shell plugin system at all.

## The fix

If the bar itself is gone you have no launcher. Press `SUPER + RETURN` for a terminal.

1. See what is installed and what claims to be enabled.

   ```bash
   omarchy plugin list
   ```

   The columns are id, state, first-party or third-party, kinds, and name. Add `--json` for the raw record.

2. Read the shell log. The shell writes to the journal under its own tag, so this survives a restart.

   ```bash
   journalctl -t omarchy-shell -b --no-pager | tail -n 80
   ```

   Look for `Plugin widget <id> failed:`, `service plugin load failed for <id>`, `Required property ... was not initialized`, or `Unable to assign [undefined] to QObject*`.

3. Turn the suspect off and restart the shell.

   ```bash
   omarchy plugin disable acme.weather
   omarchy restart shell
   ```

4. If the bar is missing entirely, the bar plugin is the suspect. Put the stock bar back.

   ```bash
   omarchy bar reset
   omarchy restart shell
   ```

   `omarchy bar reset` is the same as `omarchy bar use omarchy.bar`.

5. If disabling is not enough, remove it. Removal disables first, then deletes a git checkout or unlinks a symlink. A hand-made folder with no git repo is moved to a timestamped backup inside the plugins directory rather than deleted.

   ```bash
   omarchy plugin remove acme.weather
   ```

6. If it is a plugin you are writing, run the validator against the folder before blaming the shell.

   ```bash
   omarchy plugin validate ~/.config/omarchy/plugins/acme.weather
   ```

   It exits 0 when the manifest is acceptable, and otherwise prints one line naming the problem.

## Verify it worked

Run `omarchy plugin list` again and confirm the plugin reads `disabled`, or is gone. Then check the bar is back with `hyprctl layers | grep omarchy-bar`, which should print a layer on each monitor.

Re-read the log for the current boot with `journalctl -t omarchy-shell -b` and confirm no new `failed to load` or `Required property` lines appear after the restart.

## Why it happens

Four different things produce the same symptom.

**A failed bar used to take the whole bar with it.** In 4.0.0 through 4.0.2 the built-in `Bar.qml` declared `omarchyPath`, `barWidgetRegistry` and `barConfig` as QML `required` properties, but the plugin path injected them after construction, so no third-party or cloned bar could ever instantiate. The fallback that should have loaded the stock bar then hit a second bug: the `Loader.Error` handler read a non-existent `errorString`, which throws a `ReferenceError` before `shell.failedBarId` is set. Both the warning and the fallback were skipped, so the result was no bar at all. Reported in [#7253](https://github.com/omacom/omarchy/issues/7253), [#6915](https://github.com/omacom/omarchy/issues/6915), [#9116](https://github.com/omacom/omarchy/issues/9116) and [#10556](https://github.com/omacom/omarchy/issues/10556). From 4.0.3 the bar path is repaired: the three properties have defaults, and the bar error handler no longer touches `errorString`. No release note mentions it and the pull requests for it are still open, but the 4.0.3 and 4.0.4 source both carry the change, so on 4.0.3 or later this particular chain is closed and a failed bar option falls back to the stock bar.

**Panel plugins still fail silently.** The same `errorString` expression is still in the panel loader in 4.0.4. When a panel plugin fails to load, the handler throws before it can print the reason and before it calls `shell.hide()`, so the bar widget, `omarchy-shell shell summon <id>` and the plugin's desktop entry all do nothing and say nothing. This is [#10745](https://github.com/omacom/omarchy/issues/10745). Widget and service loads use a different, correct path, which is why those do log.

**4.0.3 narrowed what a plugin can see.** The 4.0.3 release notes list "Restrict plugin access to authentication services". In practice it did more than that: third-party plugins now receive scoped `PluginBarApi`, `PluginShellApi` and `PluginRegistryApi` objects instead of the shell internals. Plugins that relied on the old access broke across the upgrade with nothing logged. Confirmed cases: the plugin's own install path is stripped from its manifest, so bundled scripts get a broken path ([#10863](https://github.com/omacom/omarchy/issues/10863)); third-party and cloned menu plugins get a null app library and an empty Apps submenu ([#10908](https://github.com/omacom/omarchy/issues/10908)); the bar drag surface is not forwarded ([#10929](https://github.com/omacom/omarchy/issues/10929)); a plugin can no longer enumerate its peers, which breaks plugin managers ([#10888](https://github.com/omacom/omarchy/issues/10888)); and widget enumeration is scoped to the caller ([#10937](https://github.com/omacom/omarchy/issues/10937)). All of those were open when this page was checked. If a plugin worked on 4.0.2 and stopped on 4.0.3, this is the likely cause, and only the plugin author can fix it.

**Hot reload does not always take.** Saving a file under `~/.config/omarchy/plugins/` is supposed to reload the plugin. The reload path tries to clear the QML component cache first, but the call it uses is not a QML API, so it never runs ([#9772](https://github.com/omacom/omarchy/issues/9772)). A plugin that gains a new script or QML file while the shell is running can end up half-loaded until you restart the shell. When in doubt, use `omarchy restart shell` rather than trusting the file watcher.

## If that did not work

Force a rescan before restarting, in case the shell simply never noticed the change: `omarchy-shell shell rescanPlugins`. If `omarchy plugin disable <id>` answers with `plugin 'x' is not known`, that is the same hint.

If `omarchy plugin add ... --enable` reported that the shell is not responding, the plugin is probably installed but disabled: the enable call can time out while the shell is still rebuilding its plugin set ([#9304](https://github.com/omacom/omarchy/issues/9304)). Run `omarchy plugin enable <id>` again. If enable reports success but the widget still does not appear on the bar, its id is probably sitting in `plugins[]` in `~/.config/omarchy/shell.json` without a `bar.layout` entry. `omarchy plugin enable` and `omarchy bar put` both treat that as already configured and change nothing ([#11062](https://github.com/omacom/omarchy/issues/11062), reproduced on 4.0.4). Add `{ "id": "<id>" }` to a `bar.layout` section by hand, keep the `plugins[]` entry if it holds the widget's settings, and restart the shell.

Cloning a plugin that is both a service and a bar widget can break the widget, because the clone's widget does not get routed to the original service ([#10814](https://github.com/omacom/omarchy/issues/10814)). Removing the clone restores the built-in.

Do not edit files under `~/.config/omarchy/plugins/` while the session is locked. The file watcher reloads plugins under the lock and can abort the shell, stranding the session ([#10706](https://github.com/omacom/omarchy/issues/10706)). Unlock first.

As a last resort, edit `~/.config/omarchy/shell.json` by hand. A third-party plugin is enabled exactly when its id appears in that file, as a bar layout entry, in `plugins[]`, or as `bar.id`. Remove the id, save, and restart the shell. First-party non-bar plugins are the reverse: they are on unless listed in `disabledPlugins[]`.

Everything under `~/.config/omarchy/plugins/` is arbitrary unsandboxed code running inside your long-lived shell process with everything your user account can reach. `omarchy plugin add` says so before it clones, and it means it. Read a plugin before you enable it.

The upstream reference is the manual chapter on [shell plugins](https://omarchy.org/manual/shell-plugins/), plus `shell/README.md` and `shell/plugins/README.md` in the repo.

## Related

- [/fix/quickshell-crashes-or-bar-missing/](/fix/quickshell-crashes-or-bar-missing/)
- [/fix/where-did-waybar-go/](/fix/where-did-waybar-go/)
- [/fix/walker-launcher-missing-after-update/](/fix/walker-launcher-missing-after-update/)
- [/reference/commands/](/reference/commands/)
- [/security/plugins-run-unsandboxed/](/security/plugins-run-unsandboxed/)
- [/releases/still-broken/](/releases/still-broken/)
