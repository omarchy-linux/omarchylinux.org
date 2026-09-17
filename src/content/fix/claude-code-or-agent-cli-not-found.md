---
title: "Claude Code or agent CLI not found on Omarchy"
description: "Why claude, codex, gh and other mise-backed agent CLIs go missing, hang forever, or print junk on Omarchy 4, and how to rebuild the stubs and fix PATH."
answer: "On Omarchy 4 the agent CLIs are not packages. They are tiny mise stubs in ~/.local/bin written by omarchy-mise-install. If claude or codex is not found, run omarchy refresh applications to rewrite every stub, then open a new shell. If the command is found but hangs forever, your PATH puts ~/.local/bin ahead of the mise shims, which makes the stub exec itself."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: agents
issueCount: 239
errorStrings:
  - "claude: command not found"
  - "claude is not installed. Choose an installed agent with: omarchy default agent <name>"
  - "Choose default agent with: omarchy default agent <name>"
  - "Could not install Claude Code with mise"
  - "mise ~/.config/mise/config.toml tools: claude@2.1.217"
  - "warning: invalid credential line: mise ~/.config/mise/config.toml tools: gh@2.100.0"
  - "exec: node: not found"
tags: [agents, claude-code, codex, mise, path]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6349"
    title: "Issue #6349: omarchy-mise-install wrappers infinite-loop when mise's PATH hook isn't active (related #3685)"
    kind: issue
    author: "husamemadH"
    date: "2026-07-23"
  - url: "https://github.com/omacom/omarchy/pull/6350"
    title: "PR #6350: Fix infinite loop in omarchy-mise-install wrappers"
    kind: pr
    author: "husamemadH"
    date: "2026-07-24"
  - url: "https://github.com/omacom/omarchy/issues/7360"
    title: "Issue #7360: mise tool wrappers can exec themselves forever: `mise x <pkg> -- <bin>` resolves <bin> back to the wrapper"
    kind: issue
    author: "guruthechosen"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/7234"
    title: "Issue #7234: mise wrappers still exec-loop when mise x falls back to a PATH lookup (residual case of #6349)"
    kind: issue
    author: "pedrosekine"
    date: "2026-08-17"
  - url: "https://github.com/omacom/omarchy/issues/8990"
    title: "Issue #8990: omarchy-mise-install generates wrappers that recurse through PATH and hang"
    kind: issue
    author: "LukeSkypewalker"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/pull/9175"
    title: "PR #9175: Stop mise wrappers from re-executing themselves (breaks Claude Code detection in T3 Code)"
    kind: pr
    author: "lllangWV"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/11971"
    title: "Issue #11971: mise wrappers made before --quiet pollute stdout, and the regeneration migration can no longer parse them"
    kind: issue
    author: "jayrascodes"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/pull/6940"
    title: "PR #6940: Keep mise wrappers from writing to stdout"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/8253"
    title: "Issue #8253: Selecting the default agent installs an older version than the one already installed"
    kind: issue
    author: "yashksaini-coder"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/7101"
    title: "Issue #7101: omarchy update destroys user binaries in ~/.local/bin at 13 fixed names, including gh and claude"
    kind: issue
    author: "omarchybot"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/6886"
    title: "Issue #6886: Agent setup for OpenCode fails on Quattro: mise resolves to deprecated aqua:sst/opencode"
    kind: issue
    author: "alvarosaavedra"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/issues/6887"
    title: "Issue #6887: Any mise-wrapped tool hits broken aqua attestations: gh wrapper fails on Quattro (affects omarchy-mise-install defaults)"
    kind: issue
    author: "alvarosaavedra"
    date: "2026-08-14"
  - url: "https://omarchy.org/manual/ai/"
    title: "Omarchy manual: AI"
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Omarchy v4.0.0 release notes"
    kind: release
    date: "2026-08-14"
credits:
  - name: "husamemadH"
    url: "https://github.com/husamemadH"
    for: "First diagnosis of the wrapper exec loop and the merged fix in PR #6350"
  - name: "smartpbx"
    url: "https://github.com/smartpbx"
    for: "The PATH rule that decides whether the loop fires, worked out on issue #7360"
  - name: "guruthechosen"
    url: "https://github.com/guruthechosen"
    for: "Filing issue #7360 with the depth-counted proof of the loop, and showing that npm-backed agents still need the mise x environment for node"
  - name: "LukeSkypewalker"
    url: "https://github.com/LukeSkypewalker"
    for: "Reproducing the hang with a throwaway wrapper name"
  - name: "jayrascodes"
    url: "https://github.com/jayrascodes"
    for: "Finding that pre-4.0.1 stubs still pollute stdout and break git credential helpers"
  - name: "yashksaini-coder"
    url: "https://github.com/yashksaini-coder"
    for: "Tracing the default-agent picker installing an older build than the one you have"
faq:
  - q: "Where does the claude command actually live on Omarchy 4?"
    a: "At ~/.local/bin/claude, as a four-line bash stub. It runs mise use -g --quiet claude, then execs the real binary through mise x. Nothing is downloaded until the first run."
  - q: "Is Claude Code still a pacman package like it was on Omarchy 3?"
    a: "No. Omarchy 3.8.4 listed claude-code in install/omarchy-base.packages. Omarchy 4.0.0 moved Claude Code and the GitHub CLI from packages and npm to mise stubs."
  - q: "Why does claude --version sit there at 40 percent CPU and never return?"
    a: "The stub found itself on PATH instead of the real binary and exec'd itself. It stays one PID, so it looks wedged rather than looping. See issues #7360 and #8990."
related: [mise-command-not-found-or-shims, codex-invalid-value-ask-for-approval, omarchy-update-fails-or-hangs, command-not-found-xdg-terminal-exec]
draft: false
---

On Omarchy 4 the coding agents are not packages. `claude`, `codex`, `opencode`, `gemini`, `copilot`, `crush`, `grok`, `pi`, `omp`, `gh` and the rest are small bash stubs in `~/.local/bin`, each written by `omarchy-mise-install` and each backed by [mise](https://mise.jdx.dev/). That is why "not found" and "found but broken" have completely different causes here. Checked against v4.0.0 through v4.0.4.

## The fix

Work through these in order. Everything below is for Omarchy 4.x; 3.x is at the end.

1. Find out what the shell actually resolves.

   ```bash
   type -a claude
   ls -l ~/.local/bin/claude
   ```

   A stub is a regular file starting with `#!/bin/bash` and containing `mise use -g --quiet`.

2. If the stub is missing, rewrite every stub at once:

   ```bash
   omarchy refresh applications
   ```

   That runs `install/user/mise.sh`, which calls `omarchy-mise-install` for each shipped tool. For a single tool: `omarchy-mise-install claude`. For a tool with a non-default backend, pass the package first, for example `omarchy-mise-install npm:@xai-official/grok grok`.

3. Open a new shell, or reload PATH in the current one:

   ```bash
   exec bash -l
   ```

   `~/.local/bin` and `~/.local/share/mise/shims` are appended to PATH by `default/bash/env-bootstrap`, which the login profile, `/etc/skel/.bashrc` and the uwsm session all source. If you never get a login shell, that bootstrap never runs.

4. If the command is found but hangs forever, check PATH order. This is the exec loop. The 4.0.4 stub template still has it, and the fix in PR #9175 is open and unmerged:

   ```bash
   printf '%s\n' "$PATH" | tr : '\n' | grep -n 'local/bin\|mise/shims'
   ```

   If the `.local/bin` line number is lower than the `mise/shims` line, the stub shadows the real binary and execs itself. Fix the thing that prepends `~/.local/bin`. The common offender is the `uv` installer's env snippet in `~/.bashrc`, which prepends `$HOME/.local/share/../bin`. That path resolves to `~/.local/bin`, but because the string differs, the snippet's own "already on PATH" check does not catch it. Remove that line, or move it above Omarchy's own bootstrap so the shims stay in front.

   To get work done right now without touching your rc files, bypass the stub:

   ```bash
   mise x claude -- "$(mise which claude)"
   ```

5. If the stub runs but its output is corrupted, it predates the `--quiet` flag that landed in 4.0.1. Symptoms are a `mise ~/.config/mise/config.toml tools: gh@...` banner on stdout, and for `gh` a git push that dies with `warning: invalid credential line`. Regenerate it:

   ```bash
   omarchy-mise-install gh
   omarchy-mise-install claude
   ```

   Nothing regenerates these automatically. The bulk regeneration migration parses an older wrapper format and silently skips every current stub.

6. If the launcher says `claude is not installed. Choose an installed agent with: omarchy default agent <name>`, you have no default agent recorded, or the recorded one has no command. Set it:

   ```bash
   omarchy default agent claude
   ```

   This writes `~/.config/omarchy/defaults/agent` and installs the tool through mise if it is not there. `omarchy agent` then launches it; `Super + Shift + Ctrl + A` and the `a` alias both go through the same path.

7. If picking the default agent installs an older build than the one you already had, defeat mise's release cooldown by hand:

   ```bash
   MISE_MINIMUM_RELEASE_AGE=0 mise use -g claude
   ```

   `omarchy-default-agent` is the one place that does not set that variable. The stubs, `omarchy-update-mise` and the `mup` alias all do.

On 3.x this page mostly does not apply. Omarchy 3.8.4 shipped `claude-code` as a pacman package in `install/omarchy-base.packages`, there was no `omarchy-agent`, no default-agent picker and no `~/.local/bin` stub. If `claude` is missing on 3.x, reinstall the package. The switch to mise stubs happened in 4.0.0.

## Verify it worked

```bash
type -a claude          # ~/.local/bin/claude first, then the mise shim
timeout 60 claude --version
mise which claude       # absolute path inside ~/.local/share/mise/installs
claude --version 2>/dev/null | head -1   # no mise banner on stdout
omarchy default agent   # prints the recorded default, empty if none
```

`claude --version` should return in seconds. If it is still running after a minute, you are in the exec loop, not a slow download.

## Why it happens

`omarchy-mise-install` writes a stub of this shape:

```bash
#!/bin/bash
export MISE_MINIMUM_RELEASE_AGE=0
mise use -g --quiet "claude" || exit 1
exec mise x "claude" -- "claude" "$@"
```

The last line hands `mise x` a bare command name. `mise x` resolves that name through PATH, and how it builds that PATH is the whole story. smartpbx worked out the rule on issue #7360 and guruthechosen confirmed it. With no shims directory on PATH, mise puts the tool's install directory at the very front, and the stub can never win. With the shims directory present, mise slots the install directory in just ahead of it and does not touch anything earlier. So if `~/.local/bin` sits ahead of the shims, the stub finds itself, execs itself, and never returns. `exec` keeps it in one PID, so `ps` shows a single command burning a core rather than an obvious fork bomb.

A stock install does not trip this: `env-bootstrap` appends the shims directory first and `~/.local/bin` after it, so the order mise needs is already there. Something else has to push `~/.local/bin` to the front, which is why the loop shows up for some people and not others on identical releases.

Two other paths lead to the same symptom. `omarchy-mise-install` runs `rm -f` on the target before writing, so a hand-written wrapper you put at one of those names is deleted without a prompt when the stubs are refreshed. And a stale mise registry can make the install itself fail, which leaves you with a stub and no binary behind it; that is what the OpenCode and `gh` reports on 4.0.0 turned out to be, cleared by updating mise rather than by any Omarchy change.

## If that did not work

- npm-backed agents need the mise environment, not just the path. Running `"$(mise which grok)"` directly can fail with `exec: node: not found`, because the npm shim's fallback is a bare `exec node`. Always keep `mise x` in the chain.
- If `omarchy default agent` prints `Could not install Claude Code with mise`, run `mise use -g claude` by hand and read the full error. A stale registry or a failed attestation shows up there and nowhere else.
- Update mise itself before blaming Omarchy: `sudo pacman -Syu mise-bin`. Omarchy 4.0.1 swapped Arch's `mise` for the `mise-bin` package from its own repo (migration 1786952219).
- If you removed the preinstalls, `~/.local/state/omarchy/preinstalls-removed` exists and several migrations deliberately skip writing stubs for you. Install what you want by hand with `omarchy-mise-install`.
- A wrapper of your own that was overwritten is probably gone for good. Omarchy configures snapper for the root subvolume only, so pre-update snapshots do not cover `/home`.

Evidence on the exec loop is strong and current: three separate open reports filed on 4.0.0 and 4.0.1, a confirmation on 4.0.3, matching reproductions in each, and an unmerged PR (#9175) that changes the stub template. Evidence on how often the stub simply goes missing is thinner, and mostly reaches the tracker as a side effect of the other bugs.

## Related

- [mise command not found or shims](/fix/mise-command-not-found-or-shims/)
- [Codex invalid value for --ask-for-approval](/fix/codex-invalid-value-ask-for-approval/)
- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Upgrading 3 to 4](/upgrade/3-to-4-quattro/)
- The official manual chapter: [omarchy.org/manual/ai/](https://omarchy.org/manual/ai/)
