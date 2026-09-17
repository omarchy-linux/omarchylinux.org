---
title: "permission denied while trying to connect to the docker API"
description: "Omarchy 4.0.1 stopped putting your user in the docker group, so plain docker commands now need sudo. How to opt back in, and what the Podman proposal changes."
answer: "Omarchy 4.0.1 deliberately removed you from the docker group, because that group is passwordless root. Run Docker with sudo (`sudo docker ps`, `sudo docker compose up`). If you want the old behaviour back, run `omarchy setup security sudoless docker` (Setup > Security > Sudoless Docker), accept the warning, and reboot. A logout is not enough."
appliesTo:
  from: "4.0.1"
status: by-design
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: apps
issueCount: 86
errorStrings:
  - "permission denied while trying to connect to the docker API at unix:///var/run/docker.sock"
  - "dial unix /var/run/docker.sock: connect: permission denied"
tags: [docker, permissions, security, sudo, containers, podman]
sources:
  - url: "https://github.com/omacom/omarchy/pull/8056"
    title: "PR #8056: Don't put the user in the docker group; make it opt-in"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/pull/8098"
    title: "PR #8098: Offer to reboot when toggling sudoless Docker; show only the relevant menu entry"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/9101"
    title: "Issue #9101: Docker migration removes socket access without an apparent sudoless-Docker setup prompt"
    kind: issue
    author: "mattrayner"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/discussions/8293"
    title: "Discussion #8293: install docker as rootless docker to avoid root elevation"
    kind: discussion
    author: "perfecto25"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/discussions/3839"
    title: "Discussion #3839: feature request: option to select podman installation instead of docker"
    kind: discussion
    author: "elephantatech"
    date: "2025-12-10"
  - url: "https://github.com/omacom/omarchy/pull/11032"
    title: "PR #11032: Make Podman native with optional Docker compatibility"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Omarchy v4.0.1 release notes"
    kind: release
    author: "omacom"
    date: "2026-08-25"
  - url: "https://omarchy.org/manual/development-tools/"
    title: "Omarchy manual: Development Tools"
    kind: manual
    author: "omacom"
    date: "2026-09-16"
  - url: "https://0xcc.io/posts/omarchy-root-creds/"
    title: "Omarchy: Any User Process Can Escalate to Root"
    kind: blog
    author: "0xcc.io"
    date: "2026-08-28"
credits:
  - name: "mattrayner"
    url: "https://github.com/mattrayner"
    for: "Filed the clearest report of the post-migration state, with the socket permissions and group list side by side"
  - name: "perfecto25"
    url: "https://github.com/perfecto25"
    for: "Argued for a rootless Docker setup rather than group membership"
  - name: "paulgmiller"
    url: "https://github.com/paulgmiller"
    for: "Pointed out that the first docker run on a new machine now fails"
  - name: "acrogenesis"
    url: "https://github.com/acrogenesis"
    for: "Authored the open Podman migration proposal"
  - name: "elephantatech"
    url: "https://github.com/elephantatech"
    for: "Opened the original request for a Podman option"
faq:
  - q: "Is this a bug I should report?"
    a: "No. It is a deliberate security change shipped in 4.0.1 and documented in the Omarchy manual. Issue #9101 asked the same question and was closed the same morning."
  - q: "Can I just run newgrp docker instead of rebooting?"
    a: "Omarchy's own toggle scripts say a logout or newgrp is not reliably enough and only a reboot applies the change. The scripts set a reboot-required flag and offer to reboot for you."
  - q: "Does Omarchy ship Podman yet?"
    a: "No. There is no podman anywhere in the 4.0.4 source tree. PR #11032 proposes making Podman native, but it is still open and unmerged as of 2026-09-16."
  - q: "Did my containers get deleted?"
    a: "No. Only your group membership changed. The daemon, images, volumes and containers are untouched, and sudo docker ps shows them all."
related: [migration-failed-mid-update, omarchy-update-fails-or-hangs]
draft: false
---

Docker still works. You just lost the shortcut that let you talk to it without a password. Omarchy 4.0.1 stopped putting your user in the `docker` group, and the update migration took existing users out of it. The daemon is running, the socket is there, and your containers are intact. Your user account simply cannot write to `/var/run/docker.sock` any more.

Everything below was checked against the v4.0.0 through v4.0.4 source trees and the v3.8.4 tree.

## The fix

First confirm this is the group change and not a dead daemon.

1. Check the socket unit:

   ```bash
   systemctl is-active docker.socket
   ```

   It should say `active`. Omarchy still enables `docker.socket` at install time in every 4.x release.

2. Check the socket ownership and your groups:

   ```bash
   stat -c '%U %G %a %n' /var/run/docker.sock
   id -nG
   ```

   You will see `root docker 660 /var/run/docker.sock` and a group list with no `docker` in it. That combination is the whole problem.

3. Pick one of the two supported paths.

**Path A, the default. Use sudo.**

```bash
sudo docker ps
sudo docker compose up -d
```

This is what the manual tells you to do, and it needs no configuration. The `d` alias that Omarchy ships in `~/.local/share/omarchy/default/bash/aliases` is a plain alias for `docker`, so `d ps` fails the same way. Type `sudo docker` or write your own `sd` alias.

**Path B, opt back in, knowingly.**

```bash
omarchy setup security sudoless docker
```

Or use the menu: `Super + Space`, then Setup > Security > Sudoless Docker. The script prints a warning explaining that the group is equivalent to passwordless root, asks you to confirm, runs `sudo usermod -aG docker "$USER"`, records a reboot-required flag, and offers to reboot right away. Say yes. The change does not take effect until you do.

To go the other way later, the menu entry moves to Remove > Security > Sudoless Docker, or run `omarchy remove security sudoless docker`. Only one of the two entries is ever shown, which is what PR #8098 added.

**On 3.x there is nothing to do.** Omarchy 3.8.4 and earlier ran `sudo usermod -aG docker ${USER}` during install, and so did 4.0.0. If you are still on 3.x, plain `docker` works and this page does not apply to you until you upgrade.

## Verify it worked

If you chose sudo, `sudo docker ps` returning a table is the whole test.

If you opted into sudoless Docker and rebooted:

```bash
id -nG | tr ' ' '\n' | grep -x docker
docker ps
omarchy-sudo-docker; echo $?
```

`omarchy-sudo-docker` is Omarchy's own answer to "does Docker need sudo right now". It exits `0` when sudo is still needed and `1` when the socket is directly writable, so `1` is what you want. Add `--configured` and it answers for the account rather than this session, which is how it reports the window between enabling the group and the reboot that applies it.

The Docker TUI on `Super + Shift + D` is the other check. By default it opens behind a polkit prompt, via `pkexec lazydocker`. Once sudoless Docker is on and you have rebooted, it opens with no prompt at all.

## Why it happens

Membership in the `docker` group is not a convenience, it is root. The daemon runs as root and owns the socket, so anyone who can reach the socket can run `docker run -v /:/host` and rewrite the host filesystem as root, with no password. On a machine where you are already a sudo user, that is not new power, but it is a silent, headless path to root that no longer has a password prompt in front of it. A poisoned dependency or a plugin running as you gets the same access you do.

PR #8056 changed the default in v4.0.1 on 2026-08-25, listed in the release notes under Security. The install no longer grants the group, first-boot provisioning refuses to replay it even if an older snapshot recorded it, and the Quattro upgrade path no longer adds it. Migration `1787580187.sh` removes existing users from the group during `omarchy update` and refreshes the Docker launcher entry. A public write-up of the old default appeared on 0xcc.io on 2026-08-28, three days after the fix shipped.

The confusing part is the timing. The migration takes the group away immediately, but group membership is only read when a session is created, so the running session keeps working and the failure appears after the next reboot. That is exactly what mattrayner described in issue #9101, which he closed himself within twenty minutes once the rationale was clear.

Omarchy's own manual chapter on [development tools](https://omarchy.org/manual/development-tools/) documents the new default, including the `sudo docker ps` examples.

## If that did not work

**Still denied after enabling sudoless Docker.** You did not reboot. The toggle scripts are explicit that a logout or `newgrp` is not reliably enough on Omarchy, which is why they set a reboot-required flag and prompt. Reboot and try again.

**Registry logins stopped working.** `docker login` writes credentials to `$HOME/.docker/config.json`. Under `sudo docker` you are reading root's config instead, so you will be asked to log in again. Run `sudo docker login` once, or opt into the group.

**Scripts and CI helpers that call bare `docker`.** Anything that shells out to `docker` without sudo now fails, including some project task runners and agent tooling. Either edit the caller or opt in.

**The Docker TUI prompt fails.** That is a polkit problem, not a group problem. The same prompt is used by several Omarchy actions.

**You want rootless containers instead.** Omarchy does not ship them. Rootless Docker was requested in discussion #8293, and a Podman option was requested back in discussion #3839, which now has fifteen upvotes. PR #11032 by acrogenesis, opened 2026-09-09, proposes making Podman native with optional Docker compatibility, Quadlet user services for the development databases, and a container transfer path. It has community approvals but is open and unmerged as of 2026-09-16, and there is no `podman` anywhere in the v4.0.4 source tree. Treat it as a proposal, not a plan you can wait for.

## Related

- [Migration failed mid update](/fix/migration-failed-mid-update/)
- [omarchy update fails or hangs](/fix/omarchy-update-fails-or-hangs/)
- [The docker group root escalation](/security/docker-group-root-escalation/)
- [What migrations do](/upgrade/what-migrations-do/)
- [omarchy-setup-security-sudoless-docker](/reference/commands/omarchy-setup-security-sudoless-docker/)
- [Omarchy 4.0.1 release notes](/releases/v4.0.1/)
