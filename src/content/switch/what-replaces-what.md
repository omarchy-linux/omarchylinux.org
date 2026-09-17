---
title: "What replaces what: macOS and Windows apps in Omarchy"
description: "Which Omarchy app replaces Alfred, Rectangle, Time Machine, Explorer, Office and the rest. A replacement matrix for switchers, checked against 4.0.4."
answer: "Most habits map to something Omarchy already ships. Spotlight and the Start menu become Super + Space. Window snapping disappears because Hyprland tiles for you. Finder and Explorer become Nautilus on Super + Shift + F. AirDrop becomes LocalSend on Super + Ctrl + S. Time Machine is the weakest match, because snapshots restore the system root and never your home directory."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [switching, macos, windows, apps, defaults]
sources:
  - url: "https://omarchy.org/manual/coming-from-mac-or-windows/"
    title: "Omarchy manual: Coming From Mac or Windows"
    kind: manual
  - url: "https://omarchy.org/manual/guis/"
    title: "Omarchy manual: GUIs"
    kind: manual
  - url: "https://omarchy.org/manual/web-apps/"
    title: "Omarchy manual: Web Apps"
    kind: manual
  - url: "https://omarchy.org/manual/commercial-apps-services/"
    title: "Omarchy manual: Commercial apps/services"
    kind: manual
  - url: "https://omarchy.org/manual/system-snapshots/"
    title: "Omarchy manual: System snapshots"
    kind: manual
  - url: "https://omarchy.org/manual/unified-clipboard-history/"
    title: "Omarchy manual: Unified Clipboard & History"
    kind: manual
  - url: "https://omarchy.org/manual/screenshots-recording/"
    title: "Omarchy manual: Screenshots & Recording"
    kind: manual
  - url: "https://omarchy.org/manual/windows-vm/"
    title: "Omarchy manual: Windows VM"
    kind: manual
  - url: "https://omarchy.org/manual/hardware-authentication/"
    title: "Omarchy manual: Hardware authentication"
    kind: manual
  - url: "https://omarchy.org/manual/filling-out-pdfs/"
    title: "Omarchy manual: Filling out PDFs"
    kind: manual
  - url: "https://omarchy.org/manual/tuis/"
    title: "Omarchy manual: TUIs"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/8340"
    title: "Issue #8340: omarchy share clipboard sends an empty file when the clipboard holds an image (e.g. a screenshot)"
    kind: issue
    author: "dima-engineer"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7482"
    title: "Issue #7482: default/hypr/apps/localsend.lua rule doesn't match in Hyprland 0.56, LocalSend opens tiled and clicks break"
    kind: issue
    author: "fieldnote-ops"
    date: "2026-08-19"
  - url: "https://github.com/omacom/omarchy/issues/8817"
    title: "Issue #8817: Hyprland window rule for LocalSend does not match (class is 'org.localsend.localsend_app')"
    kind: issue
    author: "richerve"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/11560"
    title: "Issue #11560: Default ufw rule for LocalSend (port 53317) allows inbound from Anywhere, including IPv6"
    kind: issue
    author: "CRTFD-DVLPR"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/9235"
    title: "Issue #9235: default-keyring.sh writes an unparseable stub keyring, wiping Chrome/Docker secrets on every login"
    kind: issue
    author: "gurupak"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/9393"
    title: "Issue #9393: [hyprland/libreoffice] LibreOffice file picker dialog opens fullscreen and slides under top bar"
    kind: issue
    author: "on370"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9904"
    title: "Issue #9904: 1Password: unlock popup unusable on fractional scaling, and its window rule targets a non-resizable window"
    kind: issue
    author: "kurtome"
    date: "2026-09-02"
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
credits:
  - name: "dima-engineer"
    url: "https://github.com/dima-engineer"
    for: "Traced the empty clipboard share to wl-paste defaulting to text/plain"
  - name: "gurupak"
    url: "https://github.com/gurupak"
    for: "Traced repeated keyring wipes to two gnome-keyring-daemon start paths racing at login"
  - name: "kurtome"
    url: "https://github.com/kurtome"
    for: "Measured the 1Password unlock popup sizing failure under fractional scaling"
faq:
  - q: "Is there a Time Machine equivalent in Omarchy?"
    a: "Not for your files. Omarchy takes a Btrfs snapshot before every update and you can restore one from the Limine boot menu, but the manual is explicit that restoring brings back the root filesystem and not your home directory. For documents you still need a separate backup or sync tool."
  - q: "Do I have to give up Microsoft Office?"
    a: "No. LibreOffice ships in the base install and opens Office files. The Office web apps work in Chromium, and if you need the real desktop Office, the Windows VM under Install > Windows runs Windows 11 Pro over RDP with a shared ~/Windows folder."
  - q: "What replaces Rectangle, Magnet or FancyZones?"
    a: "Nothing, because there is nothing left to snap. Hyprland tiles every window automatically and they never overlap. Super + T pulls a single window out of the tiling when you genuinely need it floating."
  - q: "Where did Photoshop and Figma go?"
    a: "Omarchy ships Pinta, which the manual itself describes as basic and not a Photoshop alternative. GIMP, Krita and Inkscape are not in the base install, so add them yourself from Install > Package. Figma has no Linux client, so run it in the browser or add it as a web app."
related: [from-macos, from-windows, day-one-checklist, tiling-window-manager-survival]
draft: false
---

Two rules explain most of this page. First, Omarchy replaces whole categories of small utilities with things the system already does, so half your macOS menu bar has no counterpart because it has no job left. Second, what does not get replaced by the system gets replaced by one package that ships in the base install, and the base install is a fixed list you can read.

Everything below was checked against the 4.0.4 package list and the shipped keybindings, not against a forum post. When a row says an app ships, it means the package name is in the base install. When it says on demand, it means you pick it from the Omarchy menu and it installs then.

## The macOS matrix

| You reach for | In Omarchy | Ships? |
|---|---|---|
| Spotlight, Alfred, Raycast | Omarchy menu on `Super + Space`, apps only on `Super + Alt + Space` | yes |
| Rectangle, Magnet, Moom | Nothing. Hyprland tiles for you. `Super + T` floats one window | yes |
| Mission Control, Spaces | Workspaces on `Super + 1/2/3/4` | yes |
| Finder | Files (Nautilus) on `Super + Shift + F`, or `Super + Shift + Alt + F` in the terminal's directory | yes |
| Quick Look | `Space` on any file in Nautilus | yes |
| Preview, images | imv, the default image handler | yes |
| Preview, PDFs | Document Viewer, with Xournal++ for signing and non form PDFs | yes |
| Time Machine | Btrfs snapshots on every update, restored from the Limine boot menu. Root only | yes |
| Keychain Access | 1Password on `Super + Shift + /`, or Bitwarden | on demand |
| AirDrop | LocalSend on `Super + Ctrl + S`, or `omarchy share file` | yes |
| Cmd + Shift + 4 | `Print Screen`, annotated in Tensaku | yes |
| QuickTime screen recording | `Alt + Print Screen`, MP4 into `~/Videos` | yes |
| Paste, Maccy | Clipboard history on `Super + Ctrl + V`, text and images | yes |
| Notification Center | History on `Super + Shift + Alt + ,`, last notification on `Super + Alt + ,` | yes |
| System Settings | The Setup submenu, which edits plain files under `~/.config` | yes |
| App Store | _Install > Package_ or _Install > AUR_, or `omarchy pkg add` | yes |
| Parallels, VMware Fusion | _Install > Windows_, a Windows 11 Pro VM over RDP | on demand |
| Mail | The HEY web app is the default `mailto:` handler. No desktop mail client ships | yes |
| Calculator | Omacalc on `Super + Ctrl + Q` | yes |
| Notes | Obsidian on `Super + Shift + O`, or Omawrite on `Super + Shift + W` | yes |
| Pages, Numbers, Keynote | LibreOffice | yes |
| Photoshop | Pinta, which the manual calls basic. GIMP and Krita are not included | partly |
| Final Cut, iMovie | Kdenlive for editing, Omacut for trimming, OBS Studio for capture | yes |
| Messages | Signal on `Super + Shift + G`, plus WhatsApp and Google Messages web apps | on demand |
| Music, Spotify | Spotify on `Super + Shift + M`. Cliamp is the shipped terminal player | on demand |
| Activity Monitor | btop, called Activity, on `Super + Ctrl + T` | yes |
| Disk Utility | Disks from the launcher, plus Disk Usage for finding what filled the drive | yes |
| Touch ID | _Setup > Security > Fingerprint_ for lock screen and sudo | yes |

## The Windows matrix

Most rows are the same. These are the ones where the Windows habit differs.

| You reach for | In Omarchy | Ships? |
|---|---|---|
| Start menu, `Win + S` | `Super + Space` | yes |
| FancyZones, `Win + Arrow` snapping | Tiling, with nothing to configure | yes |
| Virtual desktops | Workspaces on `Super + 1/2/3/4` | yes |
| File Explorer | Nautilus on `Super + Shift + F` | yes |
| `Win + V` clipboard | `Super + Ctrl + V` | yes |
| `Win + Shift + S` | `Print Screen` | yes |
| Task Manager | `Super + Ctrl + T` | yes |
| File History, System Restore | Snapshots, root filesystem only | yes |
| Windows Hello | Fingerprint, or FIDO2 for sudo under _Setup > Security > Fido2_ | yes |
| Credential Manager | 1Password or Bitwarden | on demand |
| Nearby Share | LocalSend on `Super + Ctrl + S` | yes |
| Microsoft Office | LibreOffice, the Office web apps, or the Windows VM | yes |
| Notepad | Neovim is the default handler for plain text. Omawrite for prose | yes |
| Paint | Pinta | yes |
| Windows Terminal | The shipped terminal on `Super + Return`. Herdr on `Super + Ctrl + Return` keeps persistent sessions | yes |
| Edge | Chromium is the default. Edge, Chrome, Brave, Firefox and Zen are under _Install > Browser_ | partly |
| WSL | Nothing to install. Docker is in the base install | yes |

## Where the match is not clean

**Time Machine is the one to get right.** Snapshots are a system rollback, not a backup. The manual says restoring brings back your root filesystem but not `/home`, so a snapshot will undo a bad update and will not bring back a deleted document. Nothing in the base install does file backup either. There is no restic, borg or timeshift in the 4.0.4 package list. Dropbox and Tailscale are available under _Install > Service_ if sync is enough for you, otherwise pick your own backup tool on day one. See [rollback with snapper and limine](/upgrade/rollback-with-snapper-and-limine/).

**LocalSend is close to AirDrop, with three rough edges.** Sharing the clipboard sends an empty file when the clipboard holds an image, because the share script calls `wl-paste` with no type and gets nothing back for a screenshot (issue #8340, still open, and the code is unchanged in 4.0.4). The shipped window rule does not match LocalSend's actual window class `org.localsend.localsend_app`, so it can open tiled instead of floating, and clicks can stop registering until you float it with `Super + T` (issues #7482 and #8817, the second closed by its author as a duplicate; the rule in `default/hypr/apps/localsend.lua` is identical in 4.0.0 through 4.0.4). And the installer opens port 53317 to Anywhere on both IPv4 and IPv6 rather than to local ranges (issue #11560). See [LUKS and ufw defaults](/security/luks-and-ufw-defaults/).

**Keychain has two layers.** The password manager you actually use is 1Password or Bitwarden, both installed on demand. Underneath, the GNOME keyring holds browser and Docker secrets, and issue #9235 reports it being reset at login when two start paths race the same keyring file, which shows up as Chrome asking you to sign in again. The 1Password unlock popup from the browser extension is also clipped under fractional scaling, which is an upstream 1Password sizing bug rather than an Omarchy one (issue #9904). See [fractional scaling and HiDPI apps](/switch/fractional-scaling-hidpi-apps/).

**Office works, the file dialog sometimes does not.** LibreOffice ships and opens Word and Excel files. Issue #9393 reports its open and save dialog opening fullscreen and sliding under the top bar on 4.0.2. If you need the real thing, the Windows VM shares `~/Windows` with the guest and passes your display scaling through, but it has no GPU passthrough, so treat it as an Office box and not a workstation.

**Creative tools are the thinnest area.** Pinta is the only image editor in the base install and the manual is upfront that it is not a Photoshop replacement. Figma has no Linux client at all, so it runs in Chromium or as a web app you add under _Install > Web App_. Anything heavier is an ordinary Arch package away, but nobody has tuned it for you.

## What to watch for on newer versions

The shipped list changes between releases, so verify rather than trust this table after an upgrade. Omacalc, Omawrite, Omacut, Tensaku and Herdr are all 4.x additions and none of them exist in 3.8.4. The base terminal changed too: 3.x shipped Alacritty, 4.0.x ships foot, and both are selectable under _Setup > Defaults > Terminal_. Clipboard history moved from Walker in 3.x to the Quickshell based Omarchy shell in 4.0.0, and Walker is not in the 4.0.4 package list at all.

The next release is announced as Quattro RS 4.5. Nothing about the replacement list is confirmed for it yet, so check the preinstall list again after you update. The fastest way to see what your own machine actually has is `Super + K` for every binding. What Omarchy considers optional is the set that _Remove > Preinstalls_ strips: LibreOffice, Xournal++, Pinta, Obsidian, OBS Studio, Kdenlive, Cliamp, Aether, Moonlight, lazydocker, Omacut, Omacalc and Omawrite, plus the shipped web apps and TUI launchers. Their keybindings are disabled along with them, and _Install > Preinstalls_ only appears in the menu after you have removed them.

## Related

- [Coming from macOS](/switch/from-macos/)
- [Coming from Windows](/switch/from-windows/)
- [Day one checklist](/switch/day-one-checklist/)
- [Tiling window manager survival](/switch/tiling-window-manager-survival/)
- Official manual: [Coming From Mac or Windows](https://omarchy.org/manual/coming-from-mac-or-windows/)
