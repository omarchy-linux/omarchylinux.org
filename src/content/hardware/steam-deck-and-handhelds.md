---
title: "Steam Deck, Legion Go and ROG Ally on Omarchy"
description: "Omarchy on handheld PCs: Steam Deck, Legion Go and ROG Ally. Experimental, no handheld enablement in the installer, and the known open bugs in 4.0.4."
answer: "Experimental. Omarchy runs on AMD handhelds like the Steam Deck and Legion Go 2, but there is no handheld detection, no Deck quirk script and no gaming-mode session in the installer. You get a desktop, not SteamOS. Expect HiDPI scaling bugs, an on-screen keyboard that fights the shell, and community kernels you maintain yourself."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Valve, Lenovo, ASUS, GPD"
model: "Handheld gaming PCs"
dmi: []
cpu: "AMD Van Gogh (Steam Deck), AMD Ryzen Z1/Z2 class (Legion Go, ROG Ally)"
gpu: "AMD integrated (amdgpu)"
rating: experimental
issueCount: 8
subsystems:
  wifi: unknown
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: unknown
  gpu: works
  suspend: unknown
  hibernate: unknown
  touchpad: unknown
  display: partial
  battery: unknown
  keyboard: partial
quirkScripts:
  - name: "asus-rog.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus-rog.sh"
    note: "Installs asusctl when omarchy-hw-asus-rog matches. Only relevant to ASUS ROG hardware."
  - name: "omarchy-hw-asus-rog"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-asus-rog"
    note: "Matches sys_vendor ASUSTeK COMPUTER INC. plus ROG in product_family."
  - name: "fix-z13-touchpad.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus/fix-z13-touchpad.sh"
    note: "ROG Flow Z13 (GZ302) only. Marks the detachable keyboard touchpad as internal via udev."
tags: [steam-deck, handheld, legion-go, rog-ally, amd-gpu, gamescope]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10357"
    title: "Issue #10357: `omarchy toggle bar on/off` behaves in reverse"
    kind: issue
    author: "zieglerziga"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/8378"
    title: "Issue #8378: Shell restart buries external animated wallpapers"
    kind: issue
    author: "ChimeraMind"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/9950"
    title: "Issue #9950: Display panel's scale presets silently no-op with explicit per-output hl.monitor lines"
    kind: issue
    author: "isaac30503"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/9949"
    title: "Issue #9949: Plymouth omarchy theme renders off-centre on HiDPI panels"
    kind: issue
    author: "isaac30503"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/9029"
    title: "Issue #9029: Menu blocks on-screen keyboard input"
    kind: issue
    author: "ekollof"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/9756"
    title: "Issue #9756: Bar panels dismiss when typing on an on-screen keyboard"
    kind: issue
    author: "ekollof"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/pull/9757"
    title: "PR #9757: Let on-screen keyboards reach bar panels"
    kind: pr
    author: "ekollof"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/pull/9135"
    title: "PR #9135: Let on-screen keyboards reach the menu"
    kind: pr
    author: "yashranaway"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/2057"
    title: "Issue #2057: Auto Update (spin button) disable Wi-Fi after update"
    kind: issue
    author: "nhac-lly"
    date: "2025-09-29"
  - url: "https://github.com/omacom/omarchy/issues/3971"
    title: "Issue #3971: Steam/Proton games crash immediately on Hyprland - fix: gamescope"
    kind: issue
    author: "sebishogun"
    date: "2025-12-23"
  - url: "https://github.com/omacom/omarchy/issues/7696"
    title: "Issue #7696: Brightness 100% turns the panel completely off on ASUS ROG Flow Z13 GZ302EA"
    kind: issue
    author: "zicochaos"
    date: "2026-08-21"
  - url: "https://github.com/omacom/omarchy/discussions/4534"
    title: "Discussion #4534: Omarchy STEAM DECK MODE"
    kind: discussion
    author: "28allday"
    date: "2026-02-07"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
    date: "2026-09-16"
  - url: "https://omarchy.org/manual/gaming/"
    title: "Omarchy manual: Gaming"
    kind: manual
    date: "2026-09-16"
  - url: "https://github.com/aorumbayev/deckarchy"
    title: "deckarchy: Steam Deck kernel setup script for Arch"
    kind: other
    author: "aorumbayev"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Omarchy v4.0.4 release notes"
    kind: release
    date: "2026-09-15"
credits:
  - name: "zieglerziga"
    url: "https://github.com/zieglerziga"
    for: "Root-caused the reversed bar toggle on a Steam Deck"
  - name: "isaac30503"
    url: "https://github.com/isaac30503"
    for: "Per-monitor scaling and Plymouth HiDPI findings on a Legion Go 2"
  - name: "ekollof"
    url: "https://github.com/ekollof"
    for: "Traced on-screen keyboard input loss to the shell's layer surfaces"
  - name: "ChimeraMind"
    url: "https://github.com/ChimeraMind"
    for: "Reported the wallpaper layer regression from a docked Steam Deck LCD"
  - name: "28allday"
    url: "https://github.com/28allday"
    for: "Built a community gamescope session installer for Omarchy"
faq:
  - q: "Does Omarchy have a Steam Deck gaming mode?"
    a: "No. Omarchy 4.0.4 ships no gamescope session and no handheld detection. The manual points at a community setup script, and a separate community installer adds a ChimeraOS-style gamescope session."
  - q: "Will installing Omarchy remove SteamOS?"
    a: "Yes, if you install to the internal drive. Omarchy is a normal Arch install with no dual-boot step for SteamOS. Going back means reimaging with Valve's own recovery image."
  - q: "Do the Deck's controls work as a gamepad on the desktop?"
    a: "We have no verified report either way on Omarchy 4.x, so treat controller and trackpad behaviour as untested."
related: [steam-or-proton-game-crashes, fractional-scaling-blurry-or-huge-apps, multi-monitor-layout-not-saved, amd-gpu, asus-rog-zephyrus]
draft: false
---

## Verdict

Experimental. Omarchy runs on AMD handhelds, but nothing in the distribution knows what a handheld is. Searching the v4.0.4 tree for Valve, Jupiter, Galileo, ROG Ally or Legion Go product strings returns nothing in `bin/`, `install/` or `default/`. There is no Deck quirk script, no handheld audio tuning, and no gamescope session. You are installing a tiling desktop on a device designed around a controller.

That said, people are running it. Two Steam Deck reports and two Legion Go 2 reports in the tracker describe a live Hyprland session with the Quickshell bar up. The bugs they filed are shell and scaling bugs, not "it does not boot" bugs. Read the Legion Go 2 reports with one caveat: both are Omarchy packages layered on CachyOS, not a stock Omarchy install. That is the honest ceiling right now: it works, and then it annoys you.

Checked against 4.0.0 through 4.0.4. The 3.x picture is thinner still, because Quattro rewrote the shell that most of these reports touch.

## What works

Graphics. Every handheld report in the data uses AMD integrated graphics through `amdgpu`, and the desktop renders. Omarchy's `vulkan.sh` installs `vulkan-radeon` whenever `lspci` shows an AMD display device, so the Vulkan stack lands without special handling.

Docking, tentatively. The Steam Deck LCD report in issue #8378 is from a docked unit driving a 2560x1080 external plus the internal panel, and the multi-monitor side of that setup was not what the reporter was complaining about. Omarchy 4.0.4's release notes also call out smoother gaming on supported AMD HDMI displays with the new `linux-omarchy` kernel.

Steam and Proton. The standard Omarchy gaming stack applies. Install Steam from the Omarchy menu under Install, Gaming, as the [gaming chapter](https://omarchy.org/manual/gaming/) describes. Nothing about that path is handheld specific.

Audio is the one partial. The community `deckarchy` script exists in part to set up the Deck's audio DSP and firmware on top of a plain Arch install, which tells you the stock path is not enough on that machine. No Omarchy issue reports handheld audio either way.

Everything else is unknown rather than good. Wi-Fi, Bluetooth, suspend, battery life, fingerprint, webcam and controller input have no verified 4.x reports we could find, so this page marks them unknown. The issue tracker only proves what is broken.

## What breaks

On-screen keyboard input is the big one. Without a physical keyboard you need a layer-shell OSK, and the Quickshell surfaces fight it. Issue #9029 shows the Omarchy menu taking exclusive keyboard focus, so the first OSK tap dismisses the menu instead of typing. Issue #9756 shows the same failure in every bar popdown, including the Wi-Fi passphrase field, through the shared `Ui/KeyboardPanel.qml`. Both were filed on a GPD Pocket 4, and both are in shell code that every device runs. PR #9135 and PR #9757 propose the `ExclusionMode.Auto` fix, and both were still open when we checked on 2026-09-16.

HiDPI scaling. Handheld panels are dense. Issue #9950, from a Legion Go 2 with a 257 DPI internal panel, shows that once you add explicit per-output `hl.monitor` lines to `monitors.lua`, the bar's Display scale presets silently stop doing anything. `omarchy-hyprland-monitor-scaling` only knows how to save one scale value for the whole machine, so it rewrites a lone Lua variable that your explicit output lines then override on the next reload. Its own save step undoes the change it just applied. See [fractional scaling](/fix/fractional-scaling-blurry-or-huge-apps/) for the general case.

Plymouth boot theme. Issue #9949, same machine, same author. Plymouth computes one device scale for the whole daemon out of panel DPI, and a 257 DPI panel lands it on 2. The theme script is then told the window is half its real size, so the logo, lock icon and entry box all bunch into the top-left corner, on the external monitor too. The verified workaround is `DeviceScale=1` in `/etc/plymouth/plymouthd.conf` followed by `sudo mkinitcpio -P`. The initramfs rebuild is not optional.

Reversed bar toggle. Issue #10357 was filed from a Steam Deck on 4.0.1: `omarchy toggle bar on` hides the bar and `off` shows it. We read `bin/omarchy-toggle-bar` in the v4.0.4 tree and the bug is still there. The script hands your action to `omarchy-toggle bar-off`, and in that helper `on` means create the flag. Since the flag itself means the bar is hidden, asking for `on` hides it. Use the bare `omarchy toggle bar` until it is fixed.

Animated wallpapers. Issue #8378, from a docked Deck LCD, reports that restarting the shell puts Omarchy's own background layer back on top of an `mpvpaper` layer that was already there. No error appears; the video is simply painted over. Restart the wallpaper service after each shell restart.

Proton crashes. Issue #3971 is the general Hyprland answer, not a handheld one: wrap the game in gamescope through Steam launch options. It was closed in May 2026. See [Steam or Proton game crashes](/fix/steam-or-proton-game-crashes/).

## What Omarchy does for this model

For the Steam Deck and the Legion Go, nothing. No DMI match, no quirk script, no audio tuning. The only shipped speaker tuning in v4.0.4 is for the Dell XPS 2026.

For an ASUS ROG handheld there is a partial path. `install/hardware/asus-rog.sh` installs `asusctl` when `omarchy-hw-asus-rog` returns true, and that helper requires `sys_vendor` to equal `ASUSTeK COMPUTER INC.` and `product_family` to contain `ROG`. Check your own machine with `cat /sys/class/dmi/id/product_family` before assuming it matches. The Flow Z13 tablet gets a dedicated `fix-z13-touchpad.sh`, gated on `omarchy-hw-match "GZ302"`, but that is a detachable keyboard fix and not a handheld one. The Z13 also carries an open backlight bug, issue #7696: any raw value above 64532 of 65535 switches the panel off, so the 100% brightness binding gives you a black screen. That is a panel firmware fault with no kernel quirk yet, so stop at 98%.

One general detection note. `omarchy-hw-laptop` looks for an ACPI lid switch first, then falls back to DMI chassis types 8, 9, 10, 14, 30, 31 and 32. A handheld with no lid switch and an unusual chassis type may not be treated as a laptop at all, which affects lid and power behaviour.

Version 4.0.4 installs the bespoke `linux-omarchy` kernel and sets it as the default boot entry. If you are running a Deck on a community kernel for audio DSP and firmware reasons, check your Limine default after that update.

## Variants

Steam Deck LCD, Van Gogh APU. The units in issues #10357 and #8378. Works well enough to file detailed bug reports from.

Steam Deck OLED, Galileo. The community `deckarchy` script is explicit that it is experimental and tested only on the OLED model. It installs the Neptune kernel `linux-neptune-611` plus audio DSP and firmware setup, and it is meant to run after a vanilla Arch install and before Omarchy. That ordering matters.

Legion Go 2, machine type 83N0, Ryzen Z2 Extreme with Radeon 890M. The best documented non-Valve handheld in the data, with two open scaling bugs against it.

ROG Ally. Thin evidence. The only issue indexed to it, #2057, is a 3.x-era Wi-Fi regression on Omarchy 3.0.1 and 3.0.2. DHH closed it in February 2026 saying the MT7922 should be working well on the 6.18 kernel. Nothing 4.x specific, and nobody has retested.

GPD Pocket 4. A UMPC rather than a gaming handheld, but it is where both on-screen keyboard bugs were found, so its findings apply to any keyboardless install.

The community gamescope session from discussion #4534 is an AMD and NVIDIA path only. Its author says the installer refuses to run on Intel-only graphics, and a commenter in the same thread asks about an NVIDIA resolution limit that went unanswered. Neither the script nor the discussion is part of Omarchy.

## Before you install

Read the manual's [Omarchy on](https://omarchy.org/manual/omarchy-on/) chapter first. It says the Deck runs Arch so you can run Omarchy on it, and links Altynbek Orumbayev's `deckarchy` setup script. That is the only place the project's own documentation acknowledges this configuration, and it covers the Deck alone, not the Legion Go or the Ally.

Have a USB keyboard and hub ready. Until PR #9135 and PR #9757 land, the menu and the bar panels cannot be driven by an on-screen keyboard, and joining Wi-Fi needs a passphrase field that works.

Decide what happens to your existing install. Installing Omarchy to the internal drive replaces SteamOS, and recovery means Valve's own image. Consider installing to a microSD or an external SSD first.

Plan for the boot theme fix. If you use LUKS on a dense panel, apply the `DeviceScale=1` workaround from issue #9949 straight away.

Expect to maintain the kernel story yourself. Community Deck kernels and Omarchy's own default kernel are two different answers to the same question, and 4.0.4 changed the default.

Check [before you update](/upgrade/before-you-update-checklist/) and [rollback with Snapper](/upgrade/rollback-with-snapper-and-limine/) before your first big update.

Evidence here is thinner than on any mainstream laptop page. Eight issues across five devices is not a broad sample. If you run Omarchy on a handheld, please [submit what you find](/hardware/submit/).

## Related

- [AMD GPU notes](/hardware/amd-gpu/)
- [Steam or Proton game crashes](/fix/steam-or-proton-game-crashes/)
- [Fractional scaling blurry or huge apps](/fix/fractional-scaling-blurry-or-huge-apps/)
- [Multi-monitor layout not saved](/fix/multi-monitor-layout-not-saved/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
