---
title: "command not found: xdg-terminal-exec"
description: "Super+Return does nothing and menu entries fail with command not found: xdg-terminal-exec. Reinstall the package, then finish the interrupted Omarchy update."
answer: "Your update stopped before it installed the xdg-terminal-exec package, but the new config already calls it. Get a shell (launch a terminal from the Omarchy menu, or press Ctrl+Alt+F2 for a text console), run sudo pacman -S --needed xdg-terminal-exec, then run omarchy-update again so the migrations finish. On 3.x also confirm the terminal lines in bindings.conf."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: apps
issueCount: 49
errorStrings:
  - "command not found: xdg-terminal-exec"
  - "Error command not found xdg-terminal-exec"
  - "App failure - Error: Command not found \"xdg-terminal-exec\""
  - "error: unexpected argument '-e' found"
tags: [terminal, xdg-terminal-exec, update, keybindings, foot]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/3112"
    title: "Discussion #3112: \"Error command not found xdg-terminal-exec\" After updating omarchy to v3.1.5 when opening any TUI"
    kind: discussion
    author: "ammarove"
    date: "2025-11-03"
  - url: "https://github.com/omacom/omarchy/discussions/3112#discussioncomment-14862643"
    title: "Accepted answer on discussion #3112"
    kind: discussion
    author: "ryanrhughes"
    date: "2025-11-03"
  - url: "https://github.com/omacom/omarchy/discussions/3120"
    title: "Discussion #3120: SUPER + RETURN not working due to misconfiguration"
    kind: discussion
    author: "zdehasek"
    date: "2025-11-03"
  - url: "https://github.com/omacom/omarchy/discussions/3380"
    title: "Discussion #3380: Not able to open few options after the update"
    kind: discussion
    author: "MananDesai54"
    date: "2025-11-12"
  - url: "https://github.com/omacom/omarchy/issues/3200"
    title: "Issue #3200: Terminal Doesn't Launch(via Super+Enter) After Upgrading to Omarchy 3.1.5"
    kind: issue
    author: "jandrusk"
    date: "2025-11-06"
  - url: "https://github.com/omacom/omarchy/issues/3250"
    title: "Issue #3250: xdg-terminal-exec ( comment not found )"
    kind: issue
    author: "mir4zul"
    date: "2025-11-08"
  - url: "https://github.com/omacom/omarchy/issues/11632"
    title: "Issue #11632: Quattro upgrade silently reverts default terminal and browser"
    kind: issue
    author: "JoshJAL"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/9356"
    title: "Issue #9356: omarchy install terminal <pkg> reports failure but still mutates xdg-terminals.list"
    kind: issue
    author: "ozz1ee-dev"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/7105"
    title: "Issue #7105: A theme with no colors.toml applies silently and leaves foot, the default terminal, unable to start"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.1.5"
    title: "Omarchy v3.1.5 release notes"
    kind: release
    author: "omacom"
    date: "2025-11-03"
  - url: "https://omarchy.org/manual/terminal/"
    title: "Omarchy manual: Terminal"
    kind: manual
    author: "omacom"
    date: "2026-09-16"
credits:
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "The accepted answer that traced the missing binary to a half-finished omarchy-update"
  - name: "lypanov"
    url: "https://github.com/lypanov"
    for: "Pointing out that omarchy-migrate alone can restore the missing command"
  - name: "jelenv"
    url: "https://github.com/jelenv"
    for: "Posting the two bindings.conf lines on issue #3200 and noting why the quotes matter"
  - name: "dexterhere04"
    url: "https://github.com/dexterhere04"
    for: "The bindings.conf fix on issue #3200 that dhh confirmed as correct"
  - name: "JoshJAL"
    url: "https://github.com/JoshJAL"
    for: "Tracing the Quattro default-terminal revert to hash matching in the retire list"
faq:
  - q: "Can I just set my terminal back to alacritty instead?"
    a: "No. On both 3.x and 4.x, TERMINAL is meant to stay xdg-terminal-exec. It is a resolver, not a terminal. Choose the actual terminal from the Omarchy menu instead: Install > Terminal on 3.x, Setup > Defaults > Terminal on 4.x. Both write ~/.config/xdg-terminals.list."
  - q: "Is xdg-terminal-exec supposed to be installed by default?"
    a: "Yes. The v3.1.5 migration installs it, and it is listed in install/omarchy-base.packages in the v3.8.4 and v4.0.x snapshots, so a missing binary means a package step did not run, not that you opted out."
  - q: "Did a release fix this?"
    a: "No release carries a fix, because the error is a symptom of an interrupted update rather than a bug in one version. v3.1.5 introduced the xdg-terminal-exec launcher, and the reports start the same day."
related: [omarchy-update-fails-or-hangs, migration-failed-mid-update, stuck-at-tty-or-cannot-switch-tty, custom-keybindings-lost-after-quattro]
draft: false
---

You pressed `Super + Return` and nothing happened. Or a menu entry flashed an error naming `xdg-terminal-exec`. Either way, your config is calling a program that is not on disk. This is almost always an `omarchy-update` run that stopped partway.

Checked against the source snapshots for v3.8.4, v4.0.0 and v4.0.4, plus the issue and discussion threads listed below.

## The fix

**1. Get a shell.** On 4.x, `Super + Space` opens the Omarchy menu and `Super + Alt + Space` opens the Apps menu; try launching Foot, Ghostty, Alacritty or Kitty from there. On 3.x, use Walker. If no launcher responds, switch to a text console with `Ctrl + Alt + F2` and log in there. Dropping to a TTY is what ryanrhughes recommended in the accepted answer on [discussion #3112](https://github.com/omacom/omarchy/discussions/3112#discussioncomment-14862643), written there as `ctrl + alt + 2`.

**2. Install the missing package.**

```bash
sudo pacman -S --needed xdg-terminal-exec
```

The discussion answer suggests `pacman -Sy xdg-terminal-exec`. Prefer the form above. A bare `-Sy` refreshes the database without upgrading and can leave you in a partial-upgrade state on Arch. If you have a working shell with the Omarchy tools on PATH, `omarchy pkg add xdg-terminal-exec` does the same thing (it wraps `pacman -S --noconfirm --needed`).

**3. Finish the update that failed.** Installing the package alone is not enough, because the migrations that rewrite your config did not run either.

```bash
omarchy-update
```

If the update itself is what is broken, run the migrations on their own first. lypanov reported in [discussion #3380](https://github.com/omacom/omarchy/discussions/3380) that `omarchy-migrate` restored the missing command, after which the update completed. See [omarchy-update fails or hangs](/fix/omarchy-update-fails-or-hangs/) and [migration failed mid-update](/fix/migration-failed-mid-update/).

**4. On 3.x only, check your Hyprland bindings.** Open `~/.config/hypr/bindings.conf` and confirm these two lines exist:

```
$terminal = uwsm-app -- xdg-terminal-exec
bindd = SUPER, RETURN, Terminal, exec, $terminal --dir="$(omarchy-cmd-terminal-cwd)"
```

jelenv posted these two lines on [issue #3200](https://github.com/omacom/omarchy/issues/3200), dexterhere04 restated them the next day, and dhh confirmed that as the correct fix. Two details matter: the flag is `--dir`, not `--working-directory` (the v3.1.5 migration renamed it), and, as jelenv pointed out, the quotes around the command substitution are required for paths with spaces.

**5. On 4.x, do not edit a bindings.conf.** Quattro moved Hyprland config to Lua. The binding lives in `default/hypr/bindings/applications.lua` as `o.bind("SUPER + RETURN", "Terminal", { omarchy = "terminal" })`, which runs `omarchy-launch-terminal`. That script is a one-liner that execs `setsid uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`. Run `omarchy-launch-terminal` by hand to see the real error. See the [conf to Lua migration reference](/reference/hyprland-conf-to-lua-migration/).

## Verify it worked

```bash
command -v xdg-terminal-exec        # should print a path
pacman -Q xdg-terminal-exec         # should print a version
omarchy-default-terminal            # should print foot, ghostty, alacritty or kitty
omarchy-migrate --pending           # should list nothing
```

Then press `Super + Return`. If `omarchy-default-terminal` prints a raw `.desktop` id or nothing, your `~/.config/xdg-terminals.list` points at a terminal that is not installed. Fix it with `omarchy default terminal foot`, since Foot ships in the base package list on 4.0.4 and is always present.

## Why it happens

Omarchy v3.1.5 (2025-11-03) switched terminal launching to `xdg-terminal-exec`. The release notes describe it as making sure you cannot end up without a working terminal. `TERMINAL` became `xdg-terminal-exec`, the Hyprland binding stopped calling `$TERMINAL` directly, and migration 1762121828 installed the package and then rewrote `bindings.conf`, `uwsm/default` and the Waybar config.

`omarchy-update` pulls the new checkout before it runs migrations, and that checkout's scripts and defaults already call `xdg-terminal-exec`. The package itself only arrives when the migration runs. If the update stops before that, for example on a dependency conflict, you are left with new files referencing a binary you do not have. ryanrhughes described this in the accepted answer on discussion #3112, and lypanov saw exactly that state in discussion #3380: repo up to date, no migrations run, no packages updated. The reports cluster on the v3.1.5 release day and the week after it: issues [#3200](https://github.com/omacom/omarchy/issues/3200), [#3250](https://github.com/omacom/omarchy/issues/3250) and discussions #3112, #3120 and #3380 are all the same failure.

The design has not changed in 4.x. `xdg-terminal-exec` is still in `install/omarchy-base.packages` and `TERMINAL=xdg-terminal-exec` is still exported by the session defaults in v4.0.4. So the same interrupted update produces the same missing binary. What changed is the recovery: there is no `bindings.conf` to patch, and the terminal preference file moved from `~/.config/xdg-terminals.list` to `/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list` for the stock case.

## If that did not work

If the binary is present but no terminal opens, you have a different problem with the same symptom. Three are open against 4.x as of 2026-09-16.

**Your default terminal silently reverted after the Quattro upgrade.** JoshJAL showed in [issue #11632](https://github.com/omacom/omarchy/issues/11632) that `omarchy-upgrade-to-quattro` deletes `~/.config/xdg-terminals.list` when its sha256 matches a known stock default. Because `omarchy-default-terminal` writes a fixed template, a deliberately chosen Ghostty produces a byte-identical file and gets retired, so the system default (Foot) wins. The two hashes on the retire list are the Ghostty and Alacritty templates, so a chosen Alacritty is lost the same way. Re-run `omarchy default terminal ghostty` after upgrading. More context at [3 to 4 Quattro](/upgrade/3-to-4-quattro/).

**Your terminals list points at something you never installed.** In [issue #9356](https://github.com/omacom/omarchy/issues/9356), ozz1ee-dev reported that `omarchy install terminal ghostty` on Omarchy 4.0.1 for aarch64 rewrites `~/.config/xdg-terminals.list` even though the package is not available and never gets installed. The `omarchy-pkg-add` in the v4.0.4 snapshot exits non-zero when a package did not install, which should stop `omarchy-install-terminal` from touching the list, but the issue is still open. Check with `pacman -Q ghostty` before trusting the list.

**Your theme broke Foot.** [Issue #7105](https://github.com/omacom/omarchy/issues/7105) documents a theme with no `colors.toml` producing no `foot.ini`, which Foot treats as a fatal config error. Alacritty and Kitty have the same unguarded include; Ghostty does not. Recover from a TTY with `omarchy theme set tokyo-night`.

**You see `error: unexpected argument '-e' found`.** In discussion #3380, MananDesai54 hit this after installing the package by hand. The usage text under the error is Warp's, so `xdg-terminal-exec` was resolving to a terminal that does not accept `-e`. Reset to a supported terminal with `omarchy default terminal foot` and re-run the update.

## Related

- [omarchy-update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Migration failed mid-update](/fix/migration-failed-mid-update/)
- [Stuck at TTY or cannot switch TTY](/fix/stuck-at-tty-or-cannot-switch-tty/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [omarchy-default-terminal](/reference/commands/omarchy-default-terminal/)
- Omarchy manual: [Terminal](https://omarchy.org/manual/terminal/)
