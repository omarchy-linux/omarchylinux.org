---
title: "Docker to Podman on Omarchy: what shipped and what has not"
description: "Omarchy 4.0.1 made the docker group opt-in. Podman is still an unmerged branch. What is shipped, what is pending, and how to prepare now."
answer: "Nothing about Podman has shipped. Omarchy 4.0.4 still installs Docker, and the only container change that landed is from 4.0.1: your user is no longer added to the docker group, so plain docker needs sudo unless you opt in under Setup > Security > Sudoless Docker. Podman lives in open pull request 11032 on the feature/podman branch, unmerged."
appliesTo:
  from: "4.0.1"
status: info
fixedIn: "4.0.1"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [docker, podman, containers, security, migration]
sources:
  - url: "https://github.com/omacom/omarchy/pull/8056"
    title: "Pull #8056: Don't put the user in the docker group; make it opt-in"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/pull/8080"
    title: "Pull #8080: Flag a reboot when the docker group changes"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/pull/8098"
    title: "Pull #8098: Offer to reboot when toggling sudoless Docker; show only the relevant menu entry"
    kind: pr
    author: "omarchybot"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.1"
    title: "Omarchy v4.0.1 release notes: Fast-Follow Fixes"
    kind: release
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/9101"
    title: "Issue #9101: Docker migration removes socket access without an apparent sudoless-Docker setup prompt"
    kind: issue
    author: "mattrayner"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/pull/11032"
    title: "Pull #11032: Make Podman native with optional Docker compatibility"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/blob/feature/podman/docs/podman-migration.md"
    title: "docs/podman-migration.md on the feature/podman branch"
    kind: docs
    author: "acrogenesis"
  - url: "https://github.com/omacom/omarchy/pull/11386"
    title: "Pull #11386: Run development containers with rootless Docker"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy-pkgs/pull/369"
    title: "Pull #369: Package Podman defaults and rootless ONCE"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy-iso/pull/171"
    title: "Pull #171: Build ISOs with Podman and test legacy migrations"
    kind: pr
    author: "acrogenesis"
    date: "2026-09-09"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
    date: "2026-09-08"
  - url: "https://omarchy.org/manual/development-tools/"
    title: "Omarchy Manual: Development Tools"
    kind: manual
  - url: "https://omarchy.org/manual/security/"
    title: "Omarchy Manual: Security"
    kind: manual
credits:
  - name: "mattrayner"
    url: "https://github.com/mattrayner"
    for: "Reported that the docker group migration removes socket access with no obvious next step"
  - name: "acrogenesis"
    url: "https://github.com/acrogenesis"
    for: "Wrote both the Podman and rootless Docker proposals and the migration boundary docs"
  - name: "ErikMelton"
    url: "https://github.com/ErikMelton"
    for: "Found that the draft migration let host proxy variables leak into migrated containers"
faq:
  - q: "Is Omarchy switching to Podman?"
    a: "Not yet, and it is not decided. As of v4.0.4 the switch exists only as open pull request 11032, and a competing proposal, pull request 11386, keeps Docker but runs it rootless. Neither has been merged."
  - q: "Why does docker ps say permission denied after updating?"
    a: "Because 4.0.1 stopped putting your user in the docker group. Run commands with sudo, or opt back in under Setup > Security > Sudoless Docker and reboot."
  - q: "Should I install Podman myself right now?"
    a: "You can, since Podman is a normal Arch package, but Omarchy will not manage it, theme it, or migrate your containers. Nothing in 4.0.4 knows about Podman."
  - q: "Will my containers survive a future Podman migration?"
    a: "The proposed migration only moves unprivileged containers on the default bridge with localhost ports and private named volumes. Privileged containers, device and GPU access, host path mounts, custom networks and shared volumes are all left on Docker."
related: [3-to-4-quattro, what-migrations-do, before-you-update-checklist]
draft: false
---

Two different things get mixed up whenever Omarchy and Podman come up in the same sentence. One has shipped and is on your machine right now. The other is an open pull request that nobody has merged. Keeping them apart saves a lot of confusion.

## What is shipped

Omarchy v4.0.4, checked on 2026-09-16, still installs Docker. The base package list names `docker`, `docker-buildx`, `docker-compose`, `lazydocker` and `ufw-docker`, and `install/config/enable-services.sh` still enables `docker.socket`. There is no mention of Podman anywhere in the v3.8.4, v4.0.0, v4.0.1, v4.0.2, v4.0.3 or v4.0.4 source trees.

What did change is who can talk to the daemon. Through v4.0.0, `install/config/docker.sh` added the installing user to the docker group with `usermod -aG docker`, and v4.0.0 also recorded the group for first boot provisioning. The docker group is root equivalent, because anything in it can bind mount the whole filesystem into a container and write to it as root. Pull request 8056, merged on 2026-08-24 and listed under Security in the v4.0.1 release notes, removed that grant, and in v4.0.1 the file is a comment explaining the decision and nothing else. Two follow ups landed the same day: pull request 8080 flags a reboot when the group changes, and pull request 8098 offers the reboot from the toggle and hides the menu entry that does not apply to you.

So since v4.0.1, on a fresh install and after the migration on an existing one, your user is not in the docker group.

## What changed for you on the command line

The daemon still runs. Only your direct, unprompted access to its socket is gone.

- Plain `docker` needs `sudo`. So does the `d` alias, which is still defined as `docker` in `default/bash/aliases`.
- The Docker TUI on `Super + Shift + D` goes through `omarchy-launch-docker-tui`, which runs lazydocker under `pkexec` when the socket is not writable. You get a polkit prompt instead of an error.
- The Windows VM helper asks for authorization the same way.
- `omarchy-install-docker-dbs`, the Install > Development > Docker DB menu entry, already calls `sudo docker run` for every database it sets up.

If you want the old behaviour back, run `omarchy-setup-security-sudoless-docker`, or pick Setup > Security > Sudoless Docker in the Omarchy menu. It prints a warning, adds you to the group after you confirm, and asks to reboot. Group membership is fixed when your session is created, so the reboot is not optional theatre. Setup > Security > Sudoless Docker only appears when you are out of the group, and Remove > Security > Sudoless Docker only appears when you are in it.

To check where you stand:

```bash
id -nG | grep -w docker && echo "in the group" || echo "not in the group"
```

The upgrade itself was not loud about this. In issue 9101, closed as completed on 2026-08-30, Matt Rayner reported working Docker commands starting to fail with a socket permission error after an update, with no obvious prompt explaining the change. If that happened to you, the group removal is the reason.

## The Podman work, which has not shipped

There is a real branch. `feature/podman` exists on the upstream repository, and its head commit at the time of writing is from 2026-09-14. It is open as pull request 11032, "Make Podman native with optional Docker compatibility", by acrogenesis, opened 2026-09-09 against the `quattro` branch. It carries 51 commits ahead of `quattro`, touches 101 files, and adds roughly 4,500 lines. It sits 22 commits behind and currently reports merge conflicts. It has two approving reviews from a bot reviewer and no maintainer merge.

There is a companion design document at `docs/podman-migration.md` on that branch, plus companion pull requests in the packages repository (369) and the ISO repository (171). All three are open.

There is also a rival. Pull request 11386, by the same author, opened 2026-09-11 from `feature/rootless-docker`, keeps Docker and its CLI and API but moves development workloads into a per user rootless daemon. Its own description calls it a direct Docker alternative to 11032 for side by side review. When two competing proposals from the same author are both open, the design is not settled.

If 11032 were merged as written, this is roughly what would change:

- Podman, Podman TUI and Podman Desktop replace Docker Engine, Buildx, lazydocker and ufw-docker. `Super + Shift + D` would open Podman TUI.
- Development databases become rootless Quadlet user services with named volumes, managed by systemd, instead of `sudo docker run` containers.
- Docker Compose stays as the compose frontend, used through `podman compose`.
- The `podman-docker` CLI shim becomes optional on fresh installs, offered as Install > Development > Docker Compatibility, and retained automatically for machines migrating off Docker.
- The Windows VM stays rootful, behind an authenticated launcher.

## How to prepare

You do not need to do anything today. If you want to be ready either way, these steps are useful now and cost nothing.

1. Decide your sudo posture deliberately. Either accept `sudo docker` as normal, or opt into the group knowing it is passwordless root. Do not drift between the two.
2. Look at your containers through the lens of what an automatic migration could carry. The boundary document is explicit: automatic transfer covers unprivileged containers on the default bridge, with localhost published ports, private named volumes, and ordinary CPU, memory, PID and shared memory limits.
3. Expect to move these by hand, whatever ships: privileged containers, added capabilities, device and GPU or CDI access, host directory and host socket mounts, custom networks, shared volumes, custom domain names, Docker in Docker, persistent BuildKit, and anything binding a low host port. Cached images and unattached volumes are also outside the automatic path.
4. Name your volumes. Anonymous volumes are the ones most likely to be left behind.
5. Stop hardcoding `/var/run/docker.sock` as a bind mount in your own compose files. Both proposals hit the same wall during testing, where an application mounted the rootful socket path and failed under a rootless engine. Rootless is the direction of travel in both designs.
6. Take a snapshot before any large update. See [rollback with Snapper and Limine](/upgrade/rollback-with-snapper-and-limine/).
7. Do not run either feature branch on a machine you care about. They are proposals under review, with conflicts against the default branch.

## What to watch for on newer versions

DHH said on X on 2026-09-08 that the next release will be called Quattro RS 4.5. If a container engine change lands, it will be in release notes under its own heading, and a migration script will appear under `migrations/`. Until then, treat any guide that tells you Omarchy ships Podman as wrong.

Two smaller things to watch. First, pull request 11032 changes the `d` alias from `docker` to `podman` and rewrites the Docker DB installer, so check both after any update that mentions containers. Second, if a migration does arrive, it is designed to leave Docker installed and the migration pending whenever it finds a workload it cannot reproduce, so a partially migrated machine is an expected state rather than a failure.

## Related

- [The docker group root escalation](/security/docker-group-root-escalation/)
- [Permission denied while trying to connect to the docker API](/fix/docker-permission-denied-after-group-change/)
- [Upgrading 3.x to 4.0 Quattro](/upgrade/3-to-4-quattro/)
- [What Omarchy migrations do](/upgrade/what-migrations-do/)
- Official manual: [Development Tools](https://omarchy.org/manual/development-tools/) and [Security](https://omarchy.org/manual/security/)
