---
title: "mise: command not found, or a mise wrapper that hangs or prints noise"
description: "Omarchy 4 runs Claude, Codex and gh through mise stubs in ~/.local/bin. Fix a missing mise command, a looping wrapper, and mise Python breaking AUR."
answer: "Regenerate the stubs with omarchy-refresh-applications, then open a new shell. If a wrapped command hangs and repeats a \"tools:\" line, run any mise command first so mise puts its install dir ahead of ~/.local/bin, or replace the stub with a direct exec of the path mise which prints. If AUR builds fail, run mise unuse python."
appliesTo:
  from: "3.x"
status: workaround
category: apps
issueCount: 105
errorStrings:
  - "mise: command not found"
  - "bash: claude: command not found"
  - "mise ~/.config/mise/config.toml tools: gh@2.100.0"
  - "warning: invalid credential line: mise ~/.config/mise/config.toml tools: gh@2.100.0"
  - "No module named build"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [mise, shims, path, agents, wrappers]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6349"
    title: "Issue #6349: omarchy-mise-install wrappers infinite-loop when mise's PATH hook isn't active (related #3685)"
    kind: issue
    author: "husamemadH"
    date: "2026-07-23"
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
  - url: "https://github.com/omacom/omarchy/issues/6908"
    title: "Issue #6908: mise wrappers pollute stdout and break protocol-based tools"
    kind: issue
    author: "luisrudge"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/pull/6940"
    title: "PR #6940: Keep mise wrappers from writing to stdout"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/11971"
    title: "Issue #11971: mise wrappers made before --quiet pollute stdout, and the regeneration migration can no longer parse them"
    kind: issue
    author: "jayrascodes"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11886"
    title: "Issue #11886: mise wrappers perform global install/config writes on every command invocation"
    kind: issue
    author: "LoonanChauvette"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/6618"
    title: "Issue #6618: omarchy-mise-install overwrites symlink targets (breaks existing Grok installs)"
    kind: issue
    author: "JustMrMendez"
    date: "2026-08-07"
  - url: "https://github.com/omacom/omarchy/pull/7994"
    title: "PR #7994: Quote mise-install arguments and refuse unusable command names"
    kind: pr
    author: "Adolanium"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/3685"
    title: "Issue #3685: mise activate hook overwritten by starship/zoxide - PATH not updated automatically"
    kind: issue
    author: "plgonzalezrx8"
    date: "2025-11-29"
  - url: "https://github.com/omacom/omarchy/issues/2831"
    title: "Issue #2831: mise python installation breaks AUR packages installations"
    kind: issue
    author: "Michallote"
    date: "2025-10-25"
  - url: "https://github.com/omacom/omarchy/issues/2728"
    title: "Issue #2728: Mise Python conflicting with system python"
    kind: issue
    author: "MichaelM3"
    date: "2025-10-22"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3: fix mise upgrades removing tool versions still in use, harden mise command-wrapper input handling"
    kind: release
    author: "dhh"
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/development-tools/"
    title: "Omarchy Manual: Development Tools"
    kind: manual
    author: "dhh"
    date: "2026-09-15"
credits:
  - name: "husamemadH"
    url: "https://github.com/husamemadH"
    for: "Traced the wrapper loop to exec by bare name through PATH"
  - name: "jayrascodes"
    url: "https://github.com/jayrascodes"
    for: "Showed that stale wrappers break git push through the gh credential helper"
  - name: "naxels"
    url: "https://github.com/naxels"
    for: "Documented mise unuse python as the AUR workaround"
  - name: "Adolanium"
    url: "https://github.com/Adolanium"
    for: "Hardened omarchy-mise-install argument handling in 4.0.3"
faq:
  - q: "Where do the claude, codex and gh commands actually live?"
    a: "They are small shell stubs in ~/.local/bin written by omarchy-mise-install. Each one asks mise to install the tool on first run, then executes it. The real binary sits under ~/.local/share/mise/installs/."
  - q: "How do I regenerate every Omarchy mise stub at once?"
    a: "Run omarchy-refresh-applications. It reruns install/user/mise.sh, which calls omarchy-mise-install for every shipped tool and overwrites the stubs in ~/.local/bin."
  - q: "Does omarchy update keep mise tools current?"
    a: "Yes. omarchy-update-mise runs MISE_MINIMUM_RELEASE_AGE=0 mise up during an update, which skips mise's release cooldown. The mup alias does the same thing on demand."
related: [claude-code-or-agent-cli-not-found, omarchy-update-fails-or-hangs, command-not-found-xdg-terminal-exec]
draft: false
---

Omarchy 4 does not install Claude Code, Codex, GitHub CLI and the rest as packages. It writes tiny stubs into `~/.local/bin` that install the tool through [mise](https://mise.jdx.dev/) on first run. That design is described in the manual chapters on [AI](https://omarchy.org/manual/ai/) and [development tools](https://omarchy.org/manual/development-tools/). Most mise complaints on Omarchy are really complaints about those stubs.

Checked against v4.0.4 source, with v3.8.4 for comparison.

## The fix

Pick the symptom you actually have.

**1. `mise: command not found`.** mise is a base package. Confirm it is installed and reinstall if not.

```bash
command -v mise || sudo pacman -S --needed mise-bin
```

Omarchy 4.0.1 added a migration that swaps Arch's `mise` for `mise-bin` from the Omarchy repo in a single pacman transaction. The swap happens in one go because `omarchy-zsh` and `omarchy-fish` depend on `mise`, so removing it first would break them. The command above installs `mise-bin` if no `mise` is on your `PATH`.

**2. A wrapped command is missing (`bash: claude: command not found`).** Regenerate every shipped stub, then open a new shell.

```bash
omarchy-refresh-applications
exec bash
```

That command reruns `install/user/mise.sh`, which calls `omarchy-mise-install` for `codex`, `claude`, `crush`, `gemini`, `gh`, `copilot`, `opencode`, `playwright`, `pi`, `omp`, `grok`, `cursor-agent`, `ghui`, `hunk` and `muse` (`cursor-agent` and `muse` only when nothing by that name is already installed).

If nothing comes back, check whether you opted out:

```bash
ls ~/.local/state/omarchy/preinstalls-removed
```

If that file exists, `omarchy-remove-preinstalls` deleted the stubs on purpose and the migrations that add new agents skip you. `omarchy-refresh-applications` ignores the marker and writes the stubs anyway. Run `omarchy-install-preinstalls` instead if you want the marker cleared and the rest of the preinstalls back as well.

**3. The command hangs and repeats a `tools:` line forever.** Run any mise command first so mise prepends its install directory, then try again:

```bash
mise ls
claude --version
```

If it still spins, bypass the stub permanently for that tool:

```bash
mise use -g gh
printf '#!/bin/bash\nexec "%s" "$@"\n' "$(mise which gh)" > ~/.local/bin/gh
chmod +x ~/.local/bin/gh
```

A later migration can rewrite that file with a fresh stub, so keep your replacement somewhere you can copy it back from.

**4. Output is prefixed with `mise ~/.config/mise/config.toml tools: gh@...`.** That line is stdout, not stderr, so it corrupts pipes. It breaks `git push` when `gh` is your credential helper. Regenerate the stubs as in step 2, then confirm the stub carries `--quiet`.

**5. AUR builds or system apps fail with `No module named build`, or a GTK app cannot find its Python bindings.** Stop mise from owning the global `python`:

```bash
mise unuse python
```

Answer no when asked to delete the installed version. Or prefix a single command instead: `PATH=/usr/bin:$PATH yay -S <package>`.

## Verify it worked

```bash
command -v claude          # expect /home/you/.local/bin/claude
head -4 ~/.local/bin/gh    # expect "mise use -g --quiet" and "exec mise x"
gh auth status 2>/dev/null | head -1   # expect no "tools:" banner
timeout 15 gh --version    # expect a version, not a timeout
which python               # expect /usr/bin/python if you ran mise unuse
```

## Why it happens

In 3.x these commands were npx wrappers written by `omarchy-npx-install`, which resolved a package through `npx` against mise's Node. Quattro replaced that with `omarchy-mise-install`, and the v4.0.0 notes describe the switch of lazy-loaded tools from npm to mise. The generated stub is three lines: export `MISE_MINIMUM_RELEASE_AGE=0`, run `mise use -g --quiet <package>`, then `exec mise x <package> -- <bin> "$@"`.

The loop comes from that last line. `mise x` resolves the final `<bin>` by name through `PATH`, and `~/.local/bin` holds the stub itself. If mise has not put its install directory ahead of `~/.local/bin`, the stub execs itself. Since each hop is an `exec`, one PID spins at full CPU instead of a growing tree of processes, so a process list looks almost normal. Issue #6349 found the original form of the loop, when the stub ran `exec` on the bare bin name, and the reporter notes that `~/.local/bin` sitting before mise's install dir is enough to trigger it. Issue #3685 explains why that happens on a stock install: `default/bash/init` runs `mise activate bash` first, then starship and zoxide, and the mise hook gets dropped from `PROMPT_COMMAND`. Routing the final exec through `mise x` fixed only that ordering case. Issues #7234, #7360 and #8990 show the current template still loops whenever `mise x` falls back to a plain PATH lookup, for example after an interrupted first install left an empty version directory, or when a GUI app spawns the stub. All three were still open when this page was checked against 4.0.4.

The stdout banner is separate. `mise use -g` prints the tool it resolved, and it prints that line to stdout rather than stderr. PR #6940 added `--quiet` and shipped in 4.0.1, but nothing regenerates stubs written earlier. Issue #11971 shows the bulk regeneration migration still matching the wrapper format from before the July 2026 loop fix (a bare `exec` of the bin), so it skips every current stub without saying so.

The 4.0.3 hardening is PR #7994. It quotes the package and bin names with `printf %q` before they are written into the stub, and refuses command names containing a slash, a leading dot, a leading dash or control characters. Before that, a package name containing `$(...)` became live shell in the stub, and a name like `../../evil` wrote and deleted files outside `~/.local/bin`. Nothing Omarchy ships passed such names, so this matters only if you call `omarchy-mise-install` yourself. 4.0.3 also set `upgrade.auto_prune false`, so `mise up` stops deleting a version a running process is still executing from.

The Python conflict is older and is not a bug in the stubs. `omarchy-install-dev-env python` runs `mise use --global python@latest`, which puts mise's Python ahead of `/usr/bin/python`. Arch's PEP 517 build helpers are registered against the system interpreter, so `makepkg` builds fail. Issues #2831 and #2728 have been open since October 2025.

## If that did not work

Put mise's shims directory at the front of `PATH` in your own shell config. Issue #3685 reports that this covers non-interactive contexts a `PROMPT_COMMAND` hook never reached.

If a stub replaced a binary you installed yourself, that is issue #6618: `omarchy-mise-install` used to write through an existing symlink. The current script unlinks first, but a clobbered target is not restored for you. Reinstall that tool from its own installer.

If a tool is slow rather than broken, issue #11886 is the likely cause. Every invocation still writes global mise config before running the tool, and a killed invocation can leave mise processes holding locks. It was open against 4.0.3 with no fix in 4.0.4.

## Related

- [Claude Code or another agent CLI is not found](/fix/claude-code-or-agent-cli-not-found/)
- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Omarchy command reference](/reference/commands/)
