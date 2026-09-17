---
title: "Omarchy development practices and AI-written code"
description: "The claim that Omarchy's AI-written bash and fast release cadence cause security bugs, with the checkable evidence on both sides, as of v4.0.4."
answer: "The critique is real and partly checkable. Omarchy ships AI agent instructions in its own repo, and dozens of merged pull requests carry Claude Code or Codex authorship trailers, including security fixes. Against that, a five person security team now reviews fixes, the repo has 299 test files, and v4.0.1 through v4.0.3 shipped 28 listed security changes. There is no CI workflow in the public repo."
appliesTo:
  from: "3.x"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: info
reported: "blog.happyfellow.dev, 2026-08-25, then Hacker News 2026-08-26"
projectResponse: "Omarchy formed a five person security team, published a disclosure policy at omarchy.org/security, and listed 28 security changes across v4.0.1, v4.0.2 and v4.0.3."
tags: [security, development, ai, code-review, process, releases]
sources:
  - url: "https://blog.happyfellow.dev/merchants-of-insecurity/"
    title: "Merchants of Insecurity"
    kind: blog
    author: "One Happy Fellow"
    date: "2026-08-25"
  - url: "https://news.ycombinator.com/item?id=49447682"
    title: "Omarchy development practices lead to predictable security issues (Hacker News)"
    kind: other
    author: "arn3n"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/pull/7884"
    title: "PR #7884: Stop an installed theme from running code"
    kind: pr
    author: "omarchybot"
    date: "2026-08-23"
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
  - url: "https://github.com/omacom/omarchy/pull/7001"
    title: "PR #7001: Launch claude and codex agents with auto-review instead of full bypass"
    kind: pr
    author: "dhh"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/9458"
    title: "PR #9458: [codex] OM-SEC-02: Keep Windows VM passwords out of process argv"
    kind: pr
    author: "AFOliveira"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/7902"
    title: "PR #7902: [Security] Keep the Windows VM password out of the RDP client's argument list"
    kind: pr
    author: "dicemans"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/pull/9463"
    title: "PR #9463: [codex] OM-SEC-08: Publish SSH only after proving key-only access"
    kind: pr
    author: "AFOliveira"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/9469"
    title: "PR #9469: [codex] OM-SEC-14: Run update hooks without reusable sudo authority"
    kind: pr
    author: "AFOliveira"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/pull/10217"
    title: "PR #10217: OM-SEC-22: Isolate OCaml cleanup authorization"
    kind: pr
    author: "ErikMelton"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Release v4.0.1: Fast-Follow Fixes"
    kind: release
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Release v4.0.2"
    kind: release
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.3"
    title: "Release v4.0.3"
    kind: release
    date: "2026-09-08"
  - url: "https://omarchy.org/security/"
    title: "Omarchy: Report a vulnerability"
    kind: docs
  - url: "https://omarchy.org/security/credits/"
    title: "Omarchy security credits"
    kind: docs
  - url: "https://omarchy.org/teams/"
    title: "Omarchy Teams"
    kind: docs
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: Next version of Omarchy is going to be Quattro RS 4.5"
    kind: other
    author: "dhh"
credits:
  - name: "One Happy Fellow"
    url: "https://blog.happyfellow.dev/merchants-of-insecurity/"
    for: "The argument that AI-written bash handling untrusted input produces repeatable injection bugs"
  - name: "AFOliveira"
    url: "https://github.com/AFOliveira"
    for: "The coordinated 21 finding OM-SEC disclosure sent to the Omarchy security team"
  - name: "ErikMelton"
    url: "https://github.com/ErikMelton"
    for: "Public review of the OM-SEC branches, including a P1 migration-ordering defect"
faq:
  - q: "Is Omarchy actually written by AI?"
    a: "Partly. The repo ships AGENTS.md and CLAUDE.md instruction files, and a GitHub search on 2026-09-16 found 77 merged pull requests whose body contains the Claude Code generation trailer. Most of the 1,243 merged pull requests carry no such trailer, so this is a meaningful minority, not the whole codebase."
  - q: "Does anyone review the AI-written code?"
    a: "Some of it is reviewed by another model. PR #7884, a security fix, is signed as generated by Opus 5 in Claude Code and reviewed by Codex. Human review also happens through the five person security team, but the public repo has no GitHub Actions workflow, so nothing is gated automatically."
  - q: "Were the bugs the blog post cited already fixed?"
    a: "Yes. PR #7847 and PR #7926 were both merged on 2026-08-23, two days before the post published, and shipped in v4.0.1 on 2026-08-25. The post's argument is about the process that produced them rather than about unpatched bugs."
  - q: "What happened to the OM-SEC pull requests?"
    a: "As of 2026-09-16, none of the 21 OM-SEC branches have been merged. Fourteen are open, the rest were closed, at least one by its own author as a duplicate. Some findings were fixed by separate pull requests instead. OM-SEC-02 was a duplicate of PR #7902, which merged into the quattro branch on 2026-09-15 and is not in a tagged release yet."
related: [is-omarchy-safe, notification-and-title-bash-injection, plugins-run-unsandboxed]
draft: false
---

On 2026-08-25 a post titled "Merchants of Insecurity" argued that Omarchy's security bugs are not accidents but the predictable output of how the project is built. It reached Hacker News the next day under the title "Omarchy development practices lead to predictable security issues" and collected 297 points and 445 comments. This page separates the claims from the evidence, checked against v4.0.4 and the source tree for every tag from v3.8.4 forward.

## What the critique claims

The post makes three linked claims. First, that Omarchy uses AI-generated bash scripts to process untrusted input. Its exact phrasing adds "particularly with seemingly no review". Second, that the resulting bugs are of a kind the industry already knows how to prevent, in its words "We know how to deal with untrusted inputs", and it cites two pull requests as examples: PR #7847, where a video title reached the download command, and PR #7926, where notification click actions ran as a shell string. Third, that the project's public messaging about security does not match its posture.

The Hacker News thread is worth reading with that in mind. Most of the highly voted comments are about Omarchy's funding and about the project founder's politics rather than about the code.

## What is verifiable about AI-written code

Omarchy does not hide this. The repository has shipped an `AGENTS.md` since at least v3.8.4, and a `CLAUDE.md` since v4.0.0 that contains nothing but `@AGENTS.md`. Since 4.0.0 there is also an `agents/skills/` directory with six task guides covering install scripts, command metadata, the Quickshell desktop, the icon font, acceptance tests, and visual verification. These are instructions written for coding agents.

Merged pull requests carry authorship trailers. A GitHub search on 2026-09-16 across the repository's 1,243 merged pull requests found:

- 77 whose body contains "Generated with Claude Code"
- 24 whose body contains "Generated by Opus"
- 41 whose body contains "Reviewed by Codex"

Those sets overlap, and the search only sees pull request bodies, so treat them as a floor rather than a census. There is also a `omarchybot` account, created 2026-08-15, with 30 merged pull requests.

The important part for a security page is that this reaches security fixes. PR #7884, "Stop an installed theme from running code", is one of the eleven security items in v4.0.1. Its description ends by crediting Opus 5 in Claude Code for writing it and Codex for reviewing it. So the claim that Omarchy uses AI to write code that handles untrusted input is accurate, including for the fixes.

One thing often conflated with this: PR #7001, "Launch claude and codex agents with auto-review instead of full bypass", is about the coding agents Omarchy launches for *you* from its menu, not about how Omarchy itself is written. It changed `bin/omarchy-agent` to stop passing `--dangerously-bypass-approvals-and-sandbox` to codex. That is a user-facing hardening change, not a development process change.

## What is verifiable about review

The "seemingly no review" half of the claim is the weaker half, and it has weakened further since the post published.

Omarchy now lists a five person Security team on [omarchy.org/teams](https://omarchy.org/teams/): Adrian Rangel, Mehmet İnce, Erik Melton, Sayem Chowdhury and Sebastian Stange. Three of them, as acrogenesis, mdisec and ErikMelton, appear as authors in the v4.0.1, v4.0.2 and v4.0.3 security lists. A disclosure policy sits at [omarchy.org/security](https://omarchy.org/security/), and a [credits page](https://omarchy.org/security/credits/) thanks eleven reporters, one of them a team. The credits page lists names only, with no vulnerability descriptions, dates, or identifiers. The [manual's security chapter](https://omarchy.org/manual/security/) covers passwords, passwordless sudo and signing keys, and says nothing about how the code itself is reviewed.

There is a real test suite. The v4.0.4 tree has 299 files under `test/`, with `./test/all` running the CLI and shell suites and a separate graphical acceptance suite that runs in a disposable VM. Some of those tests encode style and safety rules directly, such as `test/shell.d/bin-style-test.sh`, which fails the shell suite if anything in `bin/` calls `notify-send` instead of the notification helper.

What is missing is automation. Across v3.8.4, v4.0.0, v4.0.2, v4.0.4 and the quattro-dev branch, the `.github` directory contains only issue templates, plus a `SECURITY.md` that is new on quattro-dev. There is no GitHub Actions workflow in the public repository, so no test suite and no linter runs automatically on a pull request. The tree carries six `# shellcheck disable=` directives, which means shellcheck gets run somewhere, but nothing in the repo enforces it against 444 commands in `bin/` and 76 install scripts.

## What the OM-SEC disclosure shows

The most concrete evidence on both sides is a coordinated disclosure filed on 2026-08-31. Twenty pull requests appeared that day from AFOliveira, each titled `[codex] OM-SEC-NN`, several of them describing themselves as one finding in a coordinated 21 finding disclosure sent to the Omarchy security team. A twenty-first, PR #10217, arrived from ErikMelton on 2026-09-04 and supersedes one of the original twenty, PR #9476.

As of 2026-09-16, none of the 21 have been merged. Fourteen are open and the rest are closed. PR #9458 was closed by its own author as a duplicate of PR #7902, which fixes the same Windows VM password exposure and was merged into the quattro branch on 2026-09-15, about ten hours after the v4.0.4 tag was cut. That fix is not in v4.0.4 or any other tagged release yet.

The open ones are not ignored. On PR #9463, Erik Melton posted a P1 finding on 2026-09-09 describing a migration ordering defect where a per-user marker lets an older migration undo a newer one. On PR #9469, Sayem Chowdhury asked an account named robosayem to audit the branch, which came back with a full audit and no blocking findings, and Erik Melton approved on 2026-09-10 after asking for a hook documentation fix. Both branches also carry GitHub Copilot review comments. That is a security team reviewing AI-assisted security patches, sometimes with AI assistance, in public.

## Release cadence

Quattro shipped on 2026-08-14. Four point releases followed inside 32 days: v4.0.1 on 2026-08-25, v4.0.2 on 2026-08-31, v4.0.3 on 2026-09-08 and v4.0.4 on 2026-09-15. The security sections list eleven fixes, ten fixes, seven fixes and none in that order, so 28 listed security changes in the 25 days between Quattro and v4.0.3.

Read that either way. It is a fast response to disclosure, and it is also 28 security defects in a release that had just shipped. The 3.x cadence was slower, with roughly two months between v3.8.2 on 2026-05-24 and v3.8.4 on 2026-07-21.

## What to watch for on newer versions

Quattro RS 4.5 is the next announced release. Three things are worth rechecking when it lands.

Whether the OM-SEC backlog cleared. Fourteen open branches from a coordinated disclosure is the single clearest measurable on this page.

Whether CI arrives. A workflow that runs `./test/all` and shellcheck on every pull request would answer the review question more convincingly than any statement. The `SECURITY.md` that appeared on quattro-dev suggests process work is happening.

Whether the project publishes advisories. There is still no CVE feed or advisory stream for Omarchy's own fixes, so tracking what changed means reading release notes.

## Related

- [Is Omarchy safe to use?](/security/is-omarchy-safe/)
- [Notification and title bash injection](/security/notification-and-title-bash-injection/)
- [Plugins run unsandboxed](/security/plugins-run-unsandboxed/)
- [Release history](/releases/)
