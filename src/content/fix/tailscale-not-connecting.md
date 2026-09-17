---
title: "Tailscale not connecting or DNS broken on Omarchy"
description: "Tailscale says Connected while every DNS lookup fails, or the bar panel says Disconnected on a healthy tailnet. The accept-routes fix, the panel bugs, and ufw."
answer: "Run `tailscale status --json | jq -r '.Health[]?'` first, because the Omarchy bar panel never reads Health. If it reports unreachable DNS servers plus advertised routes, run `sudo tailscale set --accept-routes` to accept them, or `sudo tailscale set --accept-dns=false` to keep your local resolvers. If the tailnet is fine and only the panel says Disconnected, run `omarchy restart shell`."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: network
issueCount: 42
errorStrings:
  - "Tailscale can't reach the configured DNS servers. Internet connectivity may be affected."
  - "Some peers are advertising routes but --accept-routes is false"
  - "Tailscale CLI is not installed or not on PATH."
  - "getting WaitingFiles: Access denied: file access denied"
  - "DNS_PROBE_FINISHED_NXDOMAIN"
tags: [tailscale, dns, vpn, networking, ufw, quickshell]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6962"
    title: "Issue #6962: Tailscale widget reports Connected while tailnet DNS is unreachable"
    kind: issue
    author: "z23"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7774"
    title: "Issue #7774: tailscale: pollWatchdog kills healthy in-flight status polls, panel shows TAILSCALE IS DISCONNECTED"
    kind: issue
    author: "iskakaushik"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/7354"
    title: "Issue #7354: Tailscale panel reports \"CLI is not installed or not on PATH\" when the which package is absent"
    kind: issue
    author: "anupanup2001"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/8484"
    title: "Issue #8484: Taildrop migration enables receiver without Tailscale operator permission on existing installs"
    kind: issue
    author: "cking-bot"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9526"
    title: "Issue #9526: Remove Tailscale reports success after cancelling sudo, and still tears down plugin/webapp"
    kind: issue
    author: "AtypicalMike"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/10107"
    title: "Issue #10107: Network panel shows fake \"Ethernet\" instead of Wi-Fi when a VPN/tunnel owns the default route"
    kind: issue
    author: "sal-he"
    date: "2026-09-04"
  - url: "https://github.com/omacom/omarchy/issues/5400"
    title: "Issue #5400: Tailscale not automatically connecting after fresh install of Omarchy 3.6.0"
    kind: issue
    author: "eddownes"
    date: "2026-04-23"
  - url: "https://github.com/omacom/omarchy/issues/3664"
    title: "Issue #3664: DNS sometimes disappears"
    kind: issue
    author: "Jamesking56"
    date: "2025-11-27"
  - url: "https://github.com/omacom/omarchy/issues/2925"
    title: "Issue #2925: Wifi (DNS?) doesn't work after suspending for a while"
    kind: issue
    author: "luposlip"
    date: "2025-10-28"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.1.0"
    title: "Release v3.1.0: Fix Tailscale split DNS compatibility by removing [!UNAVAIL=return]"
    kind: release
    author: "jardahrazdera"
    date: "2025-10-19"
  - url: "https://omarchy.org/manual/networking/"
    title: "Omarchy Manual: Networking"
    kind: manual
credits:
  - name: "z23"
    url: "https://github.com/z23"
    for: "Traced the silent DNS break to the widget's flagless tailscale up and the Linux accept-dns / accept-routes default"
  - name: "thomas-trijindev"
    url: "https://github.com/thomas-trijindev"
    for: "Showed with tailscaled journal output that a bare tailscale up resets prefs set earlier with tailscale set"
  - name: "iskakaushik"
    url: "https://github.com/iskakaushik"
    for: "Found the poll watchdog that kills healthy status polls and paints the panel Disconnected"
  - name: "anupanup2001"
    url: "https://github.com/anupanup2001"
    for: "Identified the missing which package behind the CLI not on PATH message"
  - name: "cking-bot"
    url: "https://github.com/cking-bot"
    for: "Reported the Taildrop receiver enabled without operator permission by migration 1785101000"
faq:
  - q: "Why does the Tailscale panel say Connected while nothing resolves?"
    a: "The panel reads BackendState from `tailscale status --json` and ignores the Health array, so it cannot see the daemon reporting that it cannot reach the DNS servers the tailnet pushed. Check Health yourself."
  - q: "Should I just turn on --accept-routes everywhere?"
    a: "No. Accepting routes installs every prefix a subnet router advertises into your routing table, which can overlap your own LAN. Use `--accept-dns=false` instead if you only want your local resolvers back."
  - q: "Can I reach SSH or a dev server on my laptop over the tailnet?"
    a: "Not until you open it. Omarchy's ufw default is deny incoming, and the only port it opens to the outside is LocalSend's 53317, so add a rule such as `sudo ufw allow in on tailscale0 to any port 22 proto tcp`."
related: [wifi-drops-after-kernel-update-iwlwifi, quickshell-crashes-or-bar-missing, plugin-fails-to-load]
draft: false
---

Omarchy installs Tailscale from _Install > Service > Tailscale_, which runs `omarchy-install-service-tailscale`. That script adds the package, enables `tailscaled.service`, runs `sudo tailscale up --accept-routes`, sets you as the local operator, enables the Taildrop receiver, and turns on the `omarchy.tailscale` bar plugin. Most "Tailscale is broken" reports on Omarchy 4 come from one of those steps not finishing, or from the bar panel telling you something the daemon never said.

## The fix

Work through these in order. All of this is checked against 4.0.4.

1. Ask the daemon, not the bar.

   ```bash
   tailscale status
   tailscale status --json | jq -r '.Health[]?'
   ```

   The panel never reads `Health`, so this is the only place the real complaint shows up.

2. If `Health` contains `Tailscale can't reach the configured DNS servers. Internet connectivity may be affected.` together with `Some peers are advertising routes but --accept-routes is false`, pick one of these two. They are different choices, not alternatives to try in sequence:

   ```bash
   # Accept the subnet routes, so the pushed nameservers become reachable
   sudo tailscale set --accept-routes

   # Or keep your own resolvers and stop using tailnet DNS
   sudo tailscale set --accept-dns=false
   ```

   Accepting routes puts every advertised prefix in your routing table, including ranges that may collide with your home LAN. If you do not know what the subnet router advertises, take the second option.

3. If you never finished the login. The installer's `sudo tailscale up --accept-routes` is also the authentication gate. Close that terminal before you follow the link and the node never joins, and the routes preference is never written. One 3.6.0 report ([issue #5400](https://github.com/omacom/omarchy/issues/5400)) saw the terminal end at Done! without ever showing a link. Run it again by hand, follow the link, then claim operator rights so the panel and Taildrop work without sudo:

   ```bash
   sudo tailscale up --accept-routes
   sudo tailscale set --operator="$USER"
   ```

4. If `tailscale status` says `Running` but the bar panel says Disconnected, restart the shell:

   ```bash
   omarchy restart shell
   ```

   It will come back. This is a panel bug, not a network one, and it returns on large tailnets.

5. If the panel says `Tailscale CLI is not installed or not on PATH.` while the CLI plainly works, install `which`:

   ```bash
   omarchy pkg add which
   omarchy restart shell
   ```

6. If you can reach peers but cannot reach a service hosted on this machine, open the port on the tunnel interface. Omarchy's firewall denies incoming traffic by default. The only inbound holes it ships are LocalSend's 53317 and a Docker DNS rule scoped to the bridge address:

   ```bash
   sudo ufw allow in on tailscale0 to any port 22 proto tcp
   sudo ufw reload
   ```

   That is the same shape Omarchy's own Sunshine installer uses for its ports.

7. If an exit node is selected and unreachable, clear it:

   ```bash
   tailscale exit-node list
   tailscale set --exit-node=
   ```

## Verify it worked

```bash
tailscale status --json | jq -r '.Health[]?'        # should print nothing
tailscale ping <machine>                            # end to end path
resolvectl query <machine>.<tailnet>.ts.net         # MagicDNS name resolves
resolvectl status tailscale0                        # per-link DNS and routing domains
```

An empty `Health` array with a resolving MagicDNS name is the real all clear. The bar panel agreeing is not evidence of anything by itself.

## Why it happens

The Linux defaults are accept DNS on, accept routes off. That combination is fine until your tailnet points DNS at nameservers that only exist behind an advertised subnet route. Tailscale then rewrites your resolvers to addresses you have no route to, and every lookup fails, not just tailnet names. z23 documented this in [issue #6962](https://github.com/omacom/omarchy/issues/6962) on a ThinkPad X1 Carbon running 4.0.0, and confirmed `tailscale set --accept-routes` restored DNS.

Omarchy makes it easy to land in that state. Nothing in 4.0.4 passes `--accept-routes` except the installer script. The bar panel's own connect action runs a flagless `tailscale up` (`loginPlan` in `shell/plugins/panels/tailscale/Model.js`), which applies stock Linux defaults on a node that never got the installer's flag. thomas-trijindev added journal evidence on the same issue that a bare `up` also rewrites the full preference set, so a later toggle can undo an `--accept-routes` you set yourself.

The false Disconnected is separate. `Service.qml` arms a 15 second `pollWatchdog` when a poll starts but never stops it when the poll finishes, so it kills whatever is in flight when it fires. When a status poll needs several seconds to return, as it does on big tailnets, the watchdog reaps that healthy poll, the non zero exit path runs, and the panel resets to Disconnected. iskakaushik reproduced this against a slow status stub in [issue #7774](https://github.com/omacom/omarchy/issues/7774). The watchdog in 4.0.4 still has no `stop()` in any of the process exit handlers.

The CLI detection bug is simpler. The plugin shells out to `which tailscale`, and `which` is a standalone Arch package that Omarchy does not install.

## If that did not work

- **Taildrop receives nothing and the journal repeats `getting WaitingFiles: Access denied: file access denied`.** Migration `1785101000.sh` enabled `omarchy-tailscale-receive.service` on existing installs without setting an operator, reported in [issue #8484](https://github.com/omacom/omarchy/issues/8484). Run `sudo tailscale set --operator="$USER"`, or `systemctl --user disable --now omarchy-tailscale-receive.service` if you do not want it.
- **The network panel shows a fake Ethernet connection.** `omarchy-network-status` picks the device that owns the default route and treats anything without a `wireless` sysfs entry as wired, so a tunnel becomes Ethernet. Cosmetic, tracked in [issue #10107](https://github.com/omacom/omarchy/issues/10107), and the fix is still an open pull request.
- **You removed Tailscale and it half went.** Cancelling the sudo prompt in _Remove > Service > Tailscale_ still prints success while leaving the package and `tailscaled` in place, per [issue #9526](https://github.com/omacom/omarchy/issues/9526). Finish it with `sudo systemctl disable --now tailscaled.service` and `omarchy pkg drop tailscale`.
- **You edited `/etc/nsswitch.conf` or restored a pacnew over it.** Omarchy ships a `hosts:` line without `[!UNAVAIL=return]` after `resolve`, a change made in v3.1.0 specifically for Tailscale split DNS and still present in 4.0.4. Restoring stock Arch ordering can break tailnet name resolution again. See [pacnew and pacsave files after an update](/fix/pacnew-and-pacsave-files-after-update/).
- **Check the system DNS override.** `omarchy dns` prints the current provider. Picking Cloudflare, Google, or Custom writes `/etc/NetworkManager/conf.d/20-omarchy-dns.conf`, pins DNS on every NetworkManager connection, and rewrites `/etc/systemd/resolved.conf`. `omarchy dns DHCP` deletes the drop-in, clears the per connection servers, and resets `resolved.conf` to a stub, which hands DNS back to your network.

On 3.x this looked different, because the stack was iwd and systemd-networkd rather than NetworkManager. Reports there mixed Tailscale with plain post suspend DNS loss ([issue #2925](https://github.com/omacom/omarchy/issues/2925), [issue #3664](https://github.com/omacom/omarchy/issues/3664)), and users worked around it by toggling the DNS provider or restarting `tailscaled`. DHH closed both in July 2026 as superseded by Quattro's NetworkManager stack, and asked on #3664 for a new issue if it reproduces there. Neither has been reopened. The evidence for a genuine 4.x suspend and Tailscale interaction is thin, so if you hit one, file it.

## Related

- [Wi-Fi drops after a kernel update](/fix/wifi-drops-after-kernel-update-iwlwifi/)
- [Quickshell crashes or the bar is missing](/fix/quickshell-crashes-or-bar-missing/)
- [A plugin fails to load](/fix/plugin-fails-to-load/)
- [LUKS and ufw defaults](/security/luks-and-ufw-defaults/)
- [Still broken in the current release](/releases/still-broken/)
