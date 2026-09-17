---
title: "Docker group root escalation fixed in Omarchy 4.0.1"
description: "The docker group on Omarchy was root-equivalent and granted by default. What the August 2026 root escalation was, and how to check your machine."
answer: "Omarchy put your user in the docker group by default, and that group is passwordless root: anything running as you could run docker with the host filesystem mounted and take over the machine. Version 4.0.1, released 2026-08-25, stopped granting the group and added a migration that removes it. Run omarchy-version, update if you are below 4.0.1, then check id -nG for docker and reboot."
appliesTo:
  from: "3.x"
status: fixed
fixedIn: "4.0.1"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
severity: critical
reported: "Privately through the Omarchy responsible-disclosure process; write-up published 2026-08-28 at 0xcc.io"
projectResponse: "Omarchy stopped granting the docker group in v4.0.1 and listed the change under Security in the release notes, crediting review by the new Omarchy security team."
tags: [docker, privilege-escalation, security, 4-0-1, sudo]
sources:
  - url: "https://0xcc.io/posts/omarchy-root-creds/"
    title: "Omarchy: Any User Process Can Escalate to Root"
    kind: blog
    date: "2026-08-28"
  - url: "https://news.ycombinator.com/item?id=49499854"
    title: "Omarchy: Any User Process Can Escalate to Root | Hacker News"
    kind: other
    author: "trap0xcc"
  - url: "https://github.com/omacom/omarchy/pull/8056"
    title: "PR #8056: Don't put the user in the docker group; make it opt-in"
    kind: pr
    author: "omarchybot"
  - url: "https://github.com/omacom/omarchy/pull/8080"
    title: "PR #8080: Flag a reboot when the docker group changes"
    kind: pr
    author: "omarchybot"
  - url: "https://github.com/omacom/omarchy/pull/8098"
    title: "PR #8098: Offer to reboot when toggling sudoless Docker; show only the relevant menu entry"
    kind: pr
    author: "omarchybot"
  - url: "https://github.com/omacom/omarchy/issues/9101"
    title: "Issue #9101: Docker migration removes socket access without an apparent sudoless-Docker setup prompt"
    kind: issue
    author: "mattrayner"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Omarchy v4.0.1 release notes: Fast-Follow Fixes"
    kind: release
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/development-tools/"
    title: "Omarchy manual: Development Tools"
    kind: manual
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy manual: Security"
    kind: manual
credits:
  - name: "trap0xcc"
    url: "https://news.ycombinator.com/user?id=trap0xcc"
    for: "Submitted the 0xcc.io write-up to Hacker News. The post itself does not name its author"
  - name: "mattrayner"
    url: "https://github.com/mattrayner"
    for: "Reported that the migration silently took away Docker socket access mid-update"
faq:
  - q: "Am I still affected if I never updated past 3.8.4?"
    a: "Yes. Every release before 4.0.1 added the install user to the docker group, including the last 3.x release v3.8.4 and Quattro 4.0.0. There is no backport, so the fix is to update."
  - q: "Does updating to 4.0.1 or later break my Docker workflow?"
    a: "Plain docker commands stop working without sudo, because the group is what gave you socket access. Use sudo docker, or opt back in with omarchy-setup-security-sudoless-docker if you accept the tradeoff."
  - q: "Is logging out enough to apply the group change?"
    a: "No. Omarchy's own scripts say only a reboot reliably applies it, and they flag reboot-required after changing the group. Until you reboot, the running session still has whatever access it started with."
  - q: "Was a CVE assigned?"
    a: "No CVE is named in the 0xcc.io write-up or in the v4.0.1 release notes. Track it by the release and by pull request #8056 instead."
related: [is-omarchy-safe, passwordless-sudo-window, plugins-run-unsandboxed]
draft: false
---

Omarchy's installer used to add your user to the `docker` group. That group is not a convenience feature, it is a root grant. The Docker daemon runs as root and owns its socket, so anything that can talk to that socket can ask root to start a container with the host filesystem mounted inside it. This was fixed in v4.0.1, released 2026-08-25. Everything below was checked against v4.0.4.

## Check your machine

1. Check what you are running.

```bash
omarchy-version
```

2. If it is below 4.0.1, update now. Use _Update > Omarchy_ in the Omarchy menu, or run the update from a terminal.

```bash
omarchy-update
```

3. Check whether your account is still in the group. This is the real test, because updating does not retroactively change a session that already started.

```bash
id -nG | tr ' ' '\n' | grep -x docker
```

If that prints `docker`, your user is still in the group. On 4.0.1 and later you can ask Omarchy the same question:

```bash
omarchy-sudo-docker --configured
```

That command exits 0 when sudo will be needed after your next login, meaning you are not in the group. It exits 1 when you are.

4. If you are still in the group and did not choose that deliberately, take yourself out and reboot.

```bash
omarchy-remove-security-sudoless-docker
```

It offers to reboot for you. Group membership is fixed when a session is created, so the change is not live until the machine comes back up.

## Verify it worked

After the reboot, `id -nG` should no longer list `docker`, and a plain Docker command should be refused:

```bash
docker ps
```

You should get a permission denied error against `unix:///var/run/docker.sock`. That is the expected state on a patched machine. The socket itself stays `root:docker 660`, and the daemon keeps running, so `systemctl is-active docker.socket` still reports `active`. Use `sudo docker ps` from now on.

## What the flaw was

On every Omarchy release before 4.0.1, `install/config/docker.sh` ran `usermod -aG docker` for the install user. In 3.x that was a literal `sudo usermod -aG docker ${USER}` line. In 4.0.0 the same grant moved into the provisioning system, which recorded `docker` in the provisioning groups list so that first-boot user creation and factory reset would reapply it.

The consequence is the classic docker group problem. Any process running as you, with no password prompt and no polkit dialog, could do this:

```bash
docker run --rm -v /:/hostroot alpine cat /hostroot/etc/shadow
```

The 0xcc.io write-up uses that exact shape as its demonstration. Mount the host root into a container, act on it as root, and you own the machine. No sudo password is ever typed.

The point people miss is that the owner of a single-user laptop already has sudo, so this is not an escalation for a human sitting at the keyboard. It matters because of everything else running under your user: browsers, editors, npm postinstall scripts, shell plugins, AI coding agents. Any one of them, compromised or simply malicious, could reach root without a prompt, with nothing for you to see or approve, which is exactly the situation the sudo password exists to prevent. Omarchy's own pull request frames it the same way, with a rogue plugin and a poisoned dependency as the examples.

## Who found it and what happened

The write-up, titled "Omarchy: Any User Process Can Escalate to Root", was published at 0xcc.io on 2026-08-28, after the fix landed in code on 2026-08-24. Its author is not named on the page. The post says the issue was reported privately through the project's responsible-disclosure process, and it credits the speed of the response as a healthy sign.

It was submitted to Hacker News by `trap0xcc` in late August 2026 and reached the front page. As of 2026-09-16 that thread has over 500 points and more than 500 comments. The discussion is worth reading but is mostly about desktop Linux sandboxing in general, not about Omarchy specifics, and there is no maintainer reply in the visible thread.

The post states that every release before 4.0.1 was affected, including the last 3.x release. That matches the local source: v3.8.4 and v4.0.0 both grant the group, v4.0.1 does not.

## What 4.0.1 actually changed

The fix is pull request #8056, "Don't put the user in the docker group; make it opt-in", listed under Security in the v4.0.1 release notes.

- The install no longer grants the group. `install/config/docker.sh` is now only a comment explaining the decision. Provisioning never records `docker`, and it filters a stale `docker` line out of an older factory snapshot.
- Migration `1787580187.sh` runs on existing installs. If you are in the group, it calls `omarchy-remove-security-sudoless-docker` for you, with `OMARCHY_DEFER_REBOOT=1` so it does not cut the update short.
- The Docker TUI on `Super + Shift + D` now goes through `omarchy-launch-docker-tui`, which uses `pkexec` when the socket is not reachable. The desktop entry was repointed at that wrapper.
- The Windows VM was reworked to keep working without the group. Its compose file moved from `~/.config/windows/docker-compose.yml` to the root-owned `/var/lib/omarchy/windows/docker-compose.yml`, so that a process running as you cannot edit the file and then trigger a root-level bring-up of it. The guest password now lives in a private `0600` credentials file instead of a world-readable compose.
- Follow-ups #8080 and #8098 flagged `reboot-required` on any group change and made _Setup > Security > Sudoless Docker_ show only the relevant entry, Setup when it is off and Remove when it is on.

Note that the `d` alias is still just `docker`, so it fails the same way a bare `docker` does. Reach for `sudo docker`.

## If you want sudoless Docker back

This is supported, as a deliberate choice. Use _Setup > Security > Sudoless Docker_ in the Omarchy menu, or run it directly:

```bash
omarchy-setup-security-sudoless-docker
```

It prints a warning, asks you to confirm with gum, adds you to the group, and offers a reboot. Understand what you are agreeing to: you are restoring the exact condition described above. The manual chapter on [development tools](https://omarchy.org/manual/development-tools/) documents both sides of the toggle.

## If Docker broke after the update

This is the common complaint, and it is expected behaviour rather than a bug. Issue #9101 reported that after updating, `docker ps` failed with a socket permission error and the user could not tell whether an opt-in step had been missed. The reporter closed it himself a quarter of an hour later, with no maintainer comment on the thread. The answer, from the code rather than from the issue, is that the migration deliberately removed you from the group, and your choices are `sudo docker` or the explicit opt-in above. The socket permission error itself has its own page, [permission denied while trying to connect to the docker API](/fix/docker-permission-denied-after-group-change/).

If Docker still fails after you reboot and you are not trying to run it sudoless, check that the daemon socket is up with `systemctl is-active docker.socket` before assuming the group is the problem.

## What to watch for on newer versions

The opt-in default is unchanged through v4.0.4 and is still present in the Quattro development snapshot, so expect it to survive into the next release. If you keep a factory snapshot or an unattended install profile made before 4.0.1, check it: the provisioning filter exists precisely because older snapshots can carry a `docker` line. Re-verify with `id -nG` after any factory reset.

## Related

- [Is Omarchy safe?](/security/is-omarchy-safe/)
- [The passwordless sudo window](/security/passwordless-sudo-window/)
- [Plugins run unsandboxed](/security/plugins-run-unsandboxed/)
- [Docker permission denied after the group change](/fix/docker-permission-denied-after-group-change/)
- [Omarchy manual: Security](https://omarchy.org/manual/security/)
