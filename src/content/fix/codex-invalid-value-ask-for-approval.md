---
title: "error: invalid value 'untrusted' for '--ask-for-approval'"
description: "Codex limits stay empty in the Omarchy agents panel because the collector passes an --ask-for-approval value Codex CLI removed. Fixed in 4.0.2."
answer: "Update to Omarchy 4.0.2 or newer with `omarchy update`, then run `omarchy agent usage-update --force codex`. The agents panel collector in 4.0.0 and 4.0.1 launched Codex with `-a untrusted`, which Codex CLI 0.149 and later reject, so the panel showed `Codex limits unavailable` and the word `initialize`. Your normal Codex sessions were never affected."
appliesTo:
  from: "4.0.0"
  to: "4.0.1"
status: fixed
fixedIn: "4.0.2"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: agents
issueCount: 19
errorStrings:
  - "error: invalid value 'untrusted' for '--ask-for-approval <APPROVAL_POLICY>'"
  - "[possible values: on-request, never]"
  - "Codex limits unavailable"
  - "initialize"
tags: [codex, agents, quickshell, cli, quattro]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7648"
    title: "Issue #7648: Codex 0.149 breaks Agents panel limit display"
    kind: issue
    author: "orienw"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/pull/7649"
    title: "PR #7649: Fix Codex usage collection on 0.149"
    kind: pr
    author: "orienw"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/8460"
    title: "Issue #8460: Agents widget: Codex collector hardcodes stale --ask-for-approval value, breaks limits fetch"
    kind: issue
    author: "robertxxiv"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/8398"
    title: "Issue #8398: Omarchy 4.0.1-1 still ships incompatible Codex approval policy"
    kind: issue
    author: "naolselemon"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/9283"
    title: "Issue #9283: omarchy-agent-usage-codex: hardcoded --ask-for-approval value 'untrusted' rejected by current codex-cli"
    kind: issue
    author: "sal-he"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/10727"
    title: "Issue #10727: omarchy-agent-usage-codex passes a removed --ask-for-approval value, so Codex limits never load"
    kind: issue
    author: "CougarM"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Omarchy v4.0.2 release notes"
    kind: release
    author: "omacom"
    date: "2026-08-31"
  - url: "https://omarchy.org/manual/ai/"
    title: "Omarchy manual: AI"
    kind: manual
    author: "omacom"
    date: "2026-09-16"
credits:
  - name: "orienw"
    url: "https://github.com/orienw"
    for: "Reported the regression and shipped the one-line collector fix in PR #7649"
  - name: "rubenmeza"
    url: "https://github.com/rubenmeza"
    for: "Showed the fix merged about three hours after the v4.0.1 tag was cut"
  - name: "mPanasiewicz"
    url: "https://github.com/mPanasiewicz"
    for: "Posted the verified sed workaround for people stuck on 4.0.1"
  - name: "Faxulous"
    url: "https://github.com/Faxulous"
    for: "Measured that the approval policy is never consulted on the limits probe"
faq:
  - q: "Is my Codex CLI broken?"
    a: "No. Only the Omarchy agents panel probe fails. Plain `codex` passes no approval flag at all, and the `cy` alias and `omarchy agent` launch Codex with `--approve-for-me`, which current Codex CLI still accepts."
  - q: "Should I downgrade Codex CLI to make the panel work?"
    a: "No. Update Omarchy to 4.0.2 or newer instead. Downgrading to a Codex build that still accepts `untrusted` fixes the symptom but leaves you on an old CLI."
  - q: "Why does the panel say `initialize` instead of a real error?"
    a: "The collector sends the Codex error output to /dev/null and reports the name of the pending RPC call as help text. That is still true in 4.0.4, so any future handshake failure will look the same."
related: [claude-code-or-agent-cli-not-found, mise-command-not-found-or-shims, quickshell-crashes-or-bar-missing, plugin-fails-to-load]
draft: false
---

The agents panel in the top bar shows your Codex tokens by day and by model, but the plan and the rate limit meters never appear. Instead you get `Codex limits unavailable` and a red box containing the single word `initialize`. Run the probe by hand and you see the real error:

```
$ codex -s read-only -a untrusted app-server
error: invalid value 'untrusted' for '--ask-for-approval <APPROVAL_POLICY>'
  [possible values: on-request, never]
```

This is an Omarchy bug, not a Codex login problem. It was fixed in v4.0.2.

## The fix

**On 4.0.2, 4.0.3 or 4.0.4: update and refresh.**

1. Check what you are on:
   ```bash
   omarchy version
   ```
2. If it reports 4.0.0 or 4.0.1, update:
   ```bash
   omarchy update
   ```
3. Regenerate the usage records so you do not wait for the next 15 minute refresh:
   ```bash
   omarchy agent usage-update --force codex
   ```
4. Open the agents panel again. The plan and the limit windows should be there.

**If you cannot update right now**, patch the collector in place. This is the workaround mPanasiewicz verified on issue #8398:

```bash
sudo sed -i 's/"-a", "untrusted"/"-a", "on-request"/' /usr/bin/omarchy-agent-usage-codex
omarchy agent usage-update --force codex
```

Two warnings about that edit. First, `/usr/share/omarchy/bin/omarchy-agent-usage-codex` is a symlink to the file in `/usr/bin`, and both belong to the `omarchy` package, so the next package upgrade overwrites your change. That is fine, because the next upgrade is also what fixes it properly. Second, keep `-s read-only` in place. Only the `-a` value needs to change.

**On 3.x there is nothing to do.** The agents panel and the `omarchy-agent-usage-codex` collector arrived with Quattro. No such file exists in v3.8.4, so 3.x systems cannot hit this.

## Verify it worked

Check that the shipped collector no longer carries the retired value:

```bash
grep -n 'app-server' /usr/bin/omarchy-agent-usage-codex
```

On 4.0.2 and later that line reads `[codex, "-s", "read-only", "-a", "on-request", "app-server"]`. The same line is present in the v4.0.2, v4.0.3 and v4.0.4 source.

Then look at the record the panel actually reads:

```bash
jq '{tierLabel, usageStatusText, limits}' ~/.local/state/omarchy/agents/usage/codex.json
```

A healthy record has your plan in `tierLabel`, an empty `usageStatusText`, and one or two entries in `limits` for the 5 hour and weekly windows. A broken one has `limits: []` and `authHelpText: "initialize"`.

You can also drive the probe by hand. `codex -s read-only -a on-request app-server` should start and sit waiting for JSON-RPC input, which you can leave with Ctrl+C. With `untrusted` it exits immediately with exit status 2.

## Why it happens

Codex CLI retired `untrusted` as an approval policy. On issue #9283 the maintainer bot posted the accepted values read back from four builds: 0.100.0 and 0.130.0 took `untrusted`, `on-failure`, `on-request` and `never`; 0.146.1 had dropped `on-failure`; and 0.149.0 accepts only `on-request` and `never`.

Quattro's agents panel, new in 4.0.0, asks Codex for your plan and limits by spawning the Codex app server and sending three calls: `initialize`, `account/read` and `account/rateLimits/read`. Line 531 of `bin/omarchy-agent-usage-codex` hardcoded `-a untrusted`. Once you had a Codex CLI at 0.149 or newer, the process died on argument parsing before the handshake started.

Omarchy does not pin the Codex CLI, so the two move independently. When the first reports came in, the packaged `openai-codex-bin` was still on 0.148.0, the last build that accepted `untrusted`, so the early reporters were people who had installed Codex another way, mostly through mise. That is why this looked patchy at first.

The opaque `initialize` text is a second, separate defect. The collector sends the subprocess stderr to `subprocess.DEVNULL`, and its RPC helper raises `TimeoutError(method)` when the pipe closes, so the exception message is the RPC method name. The handler assigns that string to `authHelpText`, which is exactly what the panel renders. That code is unchanged in 4.0.4, so the real Codex error is still hidden if the handshake fails for some other reason.

The timing explains why so many people filed this after it was fixed. orienw's PR #7649 merged as commit `4cd8a08` at 14:07 UTC on 2026-08-25. As rubenmeza documented on issue #8460, the v4.0.1 tag had been published at 11:24 UTC the same day, about three hours earlier. So the fix missed 4.0.1 by hours, and 4.0.1 stayed the newest package for six days until v4.0.2 shipped on 2026-08-31. The v4.0.2 release notes list it as "Fix Codex usage collection on version 0.149 by @orienw".

One detail worth knowing: the approval policy is never actually used on this path. Faxulous probed `-a never`, `-a on-request`, `-s read-only` alone and no flags at all against the same account on issue #8460 and got identical rate limit results, because the collector never starts a model turn. Both surviving values are equally safe here.

## If that did not work

- **Confirm the panel is looking at the right failure.** If `authHelpText` says `codex not found in PATH`, the collector could not find the `codex` binary at all. That is a mise shim or PATH problem, not this bug.
- **Check you are signed in.** Run `codex login status`. An unauthenticated CLI cannot return a plan or limits no matter which approval policy is passed.
- **Run the probe by hand.** Because stderr is discarded, the panel will keep saying `initialize` for any handshake failure. `codex -s read-only -a on-request app-server` prints the real error.
- **Check you actually updated.** Several reports filed in September, including #10727 on 2026-09-07 and #11254 on 2026-09-11, are from machines still running 4.0.0-1 or 4.0.1-1. No report of this exact error has come from anyone on 4.0.2 or later.
- **Expect the tab to vanish, not just break, on a fresh machine.** The panel admits a provider only when it has local usage, limits or a balance, so a new install with no Codex session history and a failing limits probe shows no Codex chip at all.

Evidence note: the mechanism and steps above come from the Omarchy issue tracker and from `bin/omarchy-agent-usage-codex` in the v4.0.0 through v4.0.4 source. The claim that `on-request` is accepted by every Codex build from 0.100 forward rests on the maintainer bot's posted output on issue #9283.

## Related

- [Claude Code or agent CLI not found](/fix/claude-code-or-agent-cli-not-found/)
- [mise command not found or shims](/fix/mise-command-not-found-or-shims/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [omarchy-agent-usage-codex command reference](/reference/commands/omarchy-agent-usage-codex/)
- [Omarchy releases](/releases/)
- [Omarchy manual: AI](https://omarchy.org/manual/ai/)
