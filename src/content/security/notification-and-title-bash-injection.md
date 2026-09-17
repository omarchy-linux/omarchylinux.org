---
title: "Notification and video title bash injection in Omarchy 4.0.0"
description: "In Omarchy 4.0.0 a web page's video title could reach the command run when you clicked the Download complete toast. Fixed in 4.0.1 by PR 7847 and PR 7926."
answer: "Update to 4.0.1 or later. Run omarchy update, or use Update > Omarchy in the menu. Only 4.0.0 is affected. A malicious page could hide a forged record in a video title, and clicking the Download complete notification handed it to the play command through bash. PR 7847 hardened the yt-dlp path, and PR 7926 stopped a shell from parsing any notification click command."
appliesTo:
  from: "4.0.0"
  to: "4.0.0"
status: fixed
fixedIn: "4.0.1"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: high
reported: "Public proof of concept at mehmetince.net/omarchy, cited by PR #7847 on 2026-08-23"
projectResponse: "Omarchy merged both fixes on 2026-08-23 and shipped them in v4.0.1 on 2026-08-25, listed under the Security heading of the release notes."
tags: [security, notifications, yt-dlp, rce, quickshell, 4-0-1]
sources:
  - url: "https://github.com/omacom/omarchy/pull/7847"
    title: "PR #7847: [Security] Stop a video title from becoming the Download Video play command"
    kind: pr
    author: "acrogenesis"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/pull/7926"
    title: "PR #7926: Run notification click actions as safe argv"
    kind: pr
    author: "ryanrhughes"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Release v4.0.1: Fast-Follow Fixes"
    kind: release
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/browsers/"
    title: "Omarchy Manual: Browsers"
    kind: manual
  - url: "https://omarchy.org/security/"
    title: "Omarchy security disclosure process"
    kind: docs
  - url: "https://mehmetince.net/omarchy/"
    title: "Omarchy Hoodie Drop (public proof of concept page)"
    kind: blog
    author: "Mehmet Ince"
credits:
  - name: "Mehmet Ince"
    url: "https://mehmetince.net/omarchy/"
    for: "Published the proof of concept that showed a video title reaching the notification click command"
  - name: "acrogenesis"
    url: "https://github.com/acrogenesis"
    for: "Hardened the yt-dlp record parsing so a title cannot forge a file path"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Rewrote notification click actions as an argv vector so no shell parses them"
faq:
  - q: "Is Omarchy 3.x affected?"
    a: "No. The Download Video shortcut and the clickable notification exec hint are both 4.x features. The v3.8.4 tree has no chromium yt-dlp host and no exec hint in omarchy-notification-send."
  - q: "Did I have to click anything for this to run?"
    a: "Yes. The download itself was not the dangerous part. The forged command only ran when you clicked the Download complete toast, which is why the public demo asked you to press Alt + Shift + D and then click."
  - q: "Was a CVE assigned?"
    a: "Nothing in the pull requests, the v4.0.1 release notes, or the Omarchy security pages names a CVE for either issue. Treat the PR numbers as the identifiers."
  - q: "Do I need to do anything besides updating?"
    a: "No. Both fixes are code changes in shipped files. There is no setting to flip and no config to edit. If you are on 4.0.1 or later you already have them."
related: [is-omarchy-safe, plugins-run-unsandboxed]
draft: false
---

Omarchy 4.0.0 shipped a Download Video shortcut, `Alt + Shift + D`, that hands the current browser tab to `yt-dlp` and pops a "Download complete" toast you can click to play the file. In 4.0.0 that click path went through a shell. A web page controls its own video title, and the title reached that shell. Two pull requests closed it, and both shipped in v4.0.1 on 2026-08-25.

This page is about 4.0.0 only. If you installed from the 4.0.1 ISO or a later one, or you have run an update since 25 August 2026, you are not running the affected code.

## The fix

1. Update Omarchy. Use _Update > Omarchy_ from the Omarchy menu (`Super + Space`), or run it from a terminal.

```bash
omarchy update
```

2. Let the update finish and run its migrations. It installs the latest release from the Omarchy package repository, which is v4.0.4 at the time of writing (released 2026-09-15).

3. Let the update restart the shell. The notification click handler lives in the Quickshell process, so it keeps the old code until that process restarts, which is why `omarchy-update-restart` finishes every update by running `omarchy-restart-shell`. If that step was skipped, for example because the session was locked or you updated over ssh, do it yourself or just reboot.

```bash
omarchy-restart-shell
```

That is the whole fix. There is no configuration change, no flag to set, and nothing to remove from your dotfiles.

## Verify it worked

Check the installed version first.

```bash
omarchy-version
```

Anything at 4.0.1 or higher carries both fixes. Then confirm the two code changes are present on disk.

```bash
grep -c omarchy-exec-argv /usr/share/omarchy/bin/omarchy-notification-send
grep -n 'OMARCHY_TITLE' /usr/share/omarchy/bin/omarchy-chromium-ytdlp-host
```

On a fixed system the first command prints a non zero count, and the second shows a separate `OMARCHY_TITLE` print line using `%(title)j`, the JSON encoded title. On 4.0.0 the first prints `0`, and the yt-dlp host instead has a single `after_move:OMARCHY_FILE` line carrying `%(title)s` and `%(filepath)s` together.

You can also read the notification helper's own usage line. On 4.0.1 and later it documents `--exec <program> [args...]` at the end. On 4.0.0 it documented `--exec <command>` at the front.

```bash
grep -m1 'Usage:' /usr/share/omarchy/bin/omarchy-notification-send
```

## Why it happens

Two separate weaknesses lined up.

The first was in the yt-dlp host. Omarchy 4.0.0 asked yt-dlp to print one tab separated record after a successful download, carrying both the video title and the saved file path on the same line. Omarchy then split that line and built a click command with `printf 'mpv %q'` on the path half. The catch is that a title is page metadata, and nothing cleaned it. `--restrict-filenames` only governs the filename yt-dlp writes to disk; the title went to `--print` raw, so a title with a newline and a tab inside it came out as a second `OMARCHY_FILE` record. The host took whichever record it read last, and the forged one carried an `mpv` option where the path belonged. That is the forgery.

The second was the notification click path itself. In 4.0.0, `omarchy-notification-send --exec` took one whole command as a single string, put it in a D-Bus hint called `omarchy-exec`, and the Quickshell notification service ran it with `Quickshell.execDetached(["bash", "-lc", command])`. Everything downstream of that hint was a shell string, which meant every caller had to quote its command correctly, every time, or the same class of bug came back.

PR #7847 by acrogenesis, "[Security] Stop a video title from becoming the Download Video play command", fixed the first. In the shipped form it prints the path and the title as two separate records, JSON encodes the title with `%(title)j` so a newline becomes an escape sequence rather than a record boundary, throws away any printed path unless it resolves to a regular file under the download directory, and passes `--no-exec` and a `--` terminator to yt-dlp. The title is now toast text only. It never becomes part of a command.

PR #7926 by ryanrhughes, "Run notification click actions as safe argv", fixed the second and is the more durable of the two. The hint is now called `omarchy-exec-argv` and holds a JSON array, one element per argument. Quickshell hands that array to `bash -lc 'exec "$@"'` as positional parameters, and bash expands `"$@"` without re-tokenising it, so a filename or title that lands in there stays one inert argument no matter what characters it contains. The helper's `--exec` flag changed to match: it takes the command as separate words at the end of the line, refuses a single quoted string that contains whitespace rather than splitting it itself, and is only looked for once the headline and description have been consumed, so a headline that happens to be the text `--exec` is treated as text. On the Quickshell side, a persisted hint is parsed fail closed: it must be a JSON array of strings, non empty, and the first element must not start with a dash. Every caller was migrated, including the screenshot and screen recording tools, Taildrop receive, the crash watcher, and the first run hooks.

The practical difference is that #7847 closed one forgery, while #7926 took shell parsing out of the click path altogether, so the next caller that forgets to quote something does not reopen the hole.

It was never a silent drive by. The download had to happen, and you had to click the toast. The public proof of concept dressed itself up as an Omarchy merchandise page and asked visitors to press `Alt + Shift + D`, which is what made it convincing rather than what made it powerful. The page is still up and is referenced directly from PR #7847. Do not go poking at it on an unpatched machine.

## If that did not work

- If `omarchy-version` still reports 4.0.0 after an update, check which channel you are on with `omarchy-version-channel` and see the manual's [updates chapter](https://omarchy.org/manual/updates/).
- If you are on the dev channel, your Omarchy comes from a git checkout in `~/omarchy` rather than from packages. Pull that checkout before assuming you have the fix.
- If you copied `omarchy-notification-send` calls into your own scripts or a shell plugin, those still use the old `--exec "some string"` form. On 4.0.1 and later that form no longer works. A quoted string at the end fails with an error that spells out the unquoted version; `--exec` at the front, where 4.0.0 accepted it, is no longer recognised as an option at all and the call fails with `Unknown option`. Rewrite them as `--exec program arg arg` at the very end of the command.
- If your own tooling relies on the `omarchy-exec` hint name, it is gone. The hint is `omarchy-exec-argv` now and it holds a JSON array.

## Related

- [Is Omarchy safe to use?](/security/is-omarchy-safe/) for the wider picture of what 4.0.1 through 4.0.3 hardened.
- [Plugins run unsandboxed](/security/plugins-run-unsandboxed/) for the other place where third party content reaches your shell.
- [Before you update checklist](/upgrade/before-you-update-checklist/) if you are jumping several point releases at once.
- The official [Browsers chapter](https://omarchy.org/manual/browsers/) documents the Download Video shortcut itself, and [omarchy.org/security](https://omarchy.org/security/) has the disclosure process.
