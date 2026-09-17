---
title: "What breaks when you run Omarchy 4 in a VM"
description: "Black screen, dead Super key, tiny resolution, missing guest tools, invisible cursor and clipboard: what breaks in an Omarchy 4 VM and how to fix each one."
answer: "Omarchy 4.0.4 never checks whether it is virtualised, so it installs no guest tools and applies a 2x scale to a small virtual display. Fix the graphics first: add hl.env(\"LIBGL_ALWAYS_SOFTWARE\", \"1\") to ~/.config/hypr/hyprland.lua, install your hypervisor's guest package, set omarchy_gdk_scale to 1 in monitors.lua, then reboot. Most other symptoms disappear with it."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Any hypervisor"
hostVersion: "any"
tags: [vm, virtualization, black-screen, guest-tools, hyprland, quickshell]
sources:
  - url: "https://github.com/omacom/omarchy/issues/10620"
    title: "Issue #10620: VMware guest: installer leaves the system without open-vm-tools (live ISO has them); plus working fix for the 3D-acceleration grey screen (#8113)"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7835"
    title: "Issue #7835: I am trying to install and run Omarchy inside VMware, but I consistently get a black screen after entering my password."
    kind: issue
    author: "cn0xroot"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7918"
    title: "Issue #7918: Invisible mouse cursor in VMware guest: vmwgfx hardware cursor plane fails to commit (needs no_hardware_cursors)"
    kind: issue
    author: "BigNatoDemon"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8240"
    title: "Issue #8240: Screenshot picker runs with hardware cursors forced on, hiding the pointer on nouveau/vmwgfx while you select"
    kind: issue
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/2028"
    title: "Issue #2028: Keyboard Not Registering Keystrokes in VirtualBox"
    kind: issue
    author: "ankur3-101106"
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/issues/8760"
    title: "Issue #8760: Default repeat_delay = 250 causes duplicated characters during normal typing (Parallels VM guest)"
    kind: issue
    author: "Crankygeek01-dev"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/8834"
    title: "Issue #8834: Bar centre section is unclickable with an absolute pointing device; relative mouse mode fixes it"
    kind: issue
    author: "novastate"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/8554"
    title: "Issue #8554: 120 FPS ttfx screensaver triggers QXL TTM failures and freezes the session"
    kind: issue
    author: "howdeploy"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/8943"
    title: "Issue #8943: Installed Omarchy 4.0.1 randomly hard-hangs in VMware Workstation 17.6.4 (live ISO works fine)"
    kind: issue
    author: "ncepuee"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/11337"
    title: "Issue #11337: Plymouth falls back to the unthemed text LUKS prompt on UKI installs under QEMU (systemd-stub auto-appends console=uart,io,0x3f8)"
    kind: issue
    author: "JasonStreifling"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/2513"
    title: "Issue #2513: QEMU Display Scaling Issue"
    kind: issue
    author: "rami-shalhoub"
    date: "2025-10-17"
  - url: "https://github.com/omacom/omarchy/issues/1930"
    title: "Issue #1930: unusably slow in QEMU"
    kind: issue
    author: "tcurdt"
    date: "2025-09-25"
  - url: "https://github.com/hyprwm/Hyprland/issues/16175"
    title: "Hyprland issue #16175: vmwgfx (VMware): dmabuf handles cannot be closed with GEM_CLOSE"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/omarchy/discussions/452"
    title: "Discussion #452: Installing Omarchy in a VM on an M* Mac"
    kind: discussion
    author: "swombat"
    date: "2025-08-02"
credits:
  - name: "kevincasier"
    url: "https://github.com/kevincasier"
    for: "Tracing the vmwgfx dmabuf failure to GEM_CLOSE and documenting the missing guest tools on installed systems"
  - name: "zhaozigu"
    url: "https://github.com/zhaozigu"
    for: "Finding that QT_QUICK_BACKEND set to software brings the Quickshell desktop back on VMware"
  - name: "BigNatoDemon"
    url: "https://github.com/BigNatoDemon"
    for: "Pinning the invisible cursor on vmwgfx to the hardware cursor plane and the no_hardware_cursors fix"
  - name: "howdeploy"
    url: "https://github.com/howdeploy"
    for: "Measuring the 120 FPS screensaver against QXL and showing 20 to 30 FPS is stable"
  - name: "novastate"
    url: "https://github.com/novastate"
    for: "Isolating the unclickable bar centre section to absolute pointing devices"
faq:
  - q: "Does Omarchy know it is running in a VM?"
    a: "No. There is no systemd-detect-virt call anywhere in the 4.0.4 tree, and no guest tooling is in the package lists. Every VM adjustment has to be made by hand after install."
  - q: "Why does Super + B work but Super + Return do nothing?"
    a: "Most likely because the Super key is reaching the guest fine and the terminal is dying at GPU init while the browser survives. That exact pattern was reported in issue #2028 and fits the vmwgfx buffer failure in Hyprland issue #16175. Fix the graphics first; if the bindings come back, it was never a keyboard problem."
  - q: "Which hypervisor gives the least trouble?"
    a: "QEMU with KVM on a Linux host. It avoids the vmwgfx driver entirely, which is the source of the black screen, the invisible cursor and the buffer errors on VMware and VirtualBox. Its own problems are smaller: the screensaver freeze on QXL and the plain text LUKS prompt, both covered on this page."
  - q: "Is the host-to-guest clipboard supposed to work out of the box?"
    a: "No. It needs the guest agent for your hypervisor, and Omarchy installs none of them. Omarchy's own Super + C and Super + V bindings are unrelated, they only move text inside the guest."
related: [virtualbox, vmware-workstation-fusion, proxmox-qemu-kvm, parallels]
draft: false
---

Omarchy 4 runs in a virtual machine, but it never adapts to one. Grep the 4.0.4 source and there is no call to `systemd-detect-virt` anywhere, no guest agent in `install/omarchy-base.packages` or `install/omarchy-other.packages`, and nothing hypervisor-specific in `install/user/hardware/`, which holds only the vendor directories and the nouveau cursor fix. Every adjustment below is one you have to make yourself after the install finishes.

That single fact explains most of what people report. This page was checked against Omarchy 4.0.4 (2026-09-15).

## The one thing to fix first

Almost every dramatic symptom in a VM, black screen, dead keybindings, crashing apps, comes from the same place: the guest GPU driver. VMware exposes its SVGA II adapter, and VirtualBox's VMSVGA controller emulates the same thing, so both land you on the `vmwgfx` kernel driver in the guest.

kevincasier traced the failure in issue #10620. On `vmwgfx`, a dmabuf that Hyprland imports comes back as a TTM surface handle rather than a GEM handle, so the `GEM_CLOSE` call Hyprland uses to release it fails with EINVAL. Hyprland treats that as a broken buffer, refuses the attach for every GPU client, and fills its log with close errors. Quickshell, which draws the whole Omarchy 4 shell, is a GPU client, so the desktop never appears.

Two workarounds are known to work. The broad one is system-wide software GL:

```bash
sed -i '/bootstrap.lua/a hl.env("LIBGL_ALWAYS_SOFTWARE", "1")' ~/.config/hypr/hyprland.lua
```

The narrower one, found by zhaozigu in issue #7835, only pushes Qt Quick onto its software backend and leaves other GL clients alone:

```bash
sed -i '/bootstrap.lua/a hl.env("QT_QUICK_BACKEND", "software")' ~/.config/hypr/hyprland.lua
```

Then reboot. On QEMU with virtio or QXL you should not need either.

The upstream Hyprland report, issue #16175, was closed as not planned rather than fixed, so treat these as workarounds with no end date.

Note that the fix people pass around in older threads such as issue #2028, adding `env = LIBGL_ALWAYS_SOFTWARE, 1` to `~/.config/hypr/envs.conf`, does nothing on Omarchy 4. kevincasier makes that point in issue #10620: the config is Lua now, and 4.0.4 does not ship that file at all. See [the Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

## The Super key

There are two different problems wearing the same costume.

The real one is host capture. VirtualBox, VMware and Parallels can all claim the Windows or Command key for the host UI before the guest ever sees it. Omarchy binds nearly everything to Super, so a captured modifier kills the whole desktop's controls. Each hypervisor has its own setting for passing it through, and that is a host-side change, not a guest-side one.

The one in the Omarchy tracker is probably not a keyboard problem at all. In issue #2028, a 3.x-era thread that was closed without a stated fix, reporters listed exactly which bindings worked and which did not: `Super + E`, `Super + W` and `Super + B` fired, while `Super + Return`, `Super + Space` and `Super + Alt + Space` did nothing. A captured modifier would kill all six. The likeliest reading, given what Hyprland issue #16175 later established, is that the terminal and the launcher were GPU clients dying at startup while the browser survived, and the one fix offered in that thread was software GL. Nobody there confirmed it, so treat it as the best explanation rather than a proven one. Fix the graphics first and see whether those bindings come back.

If you are locked out entirely, `Ctrl + Alt + F2` or `Ctrl + Alt + F3` still reaches a text console, and clicking the Omarchy logo at the left of the top bar opens the menu with the mouse alone.

## Resolution and scaling

Omarchy ships `~/.config/hypr/monitors.lua` with `omarchy_gdk_scale = 2` and monitor scale set to `auto`. That is right for a HiDPI laptop and wrong for a virtual display. kevincasier measured it on a 1280x800 VMware display: an effectively 640x400 desktop.

Set the scale back to 1 and pin the mode:

```bash
hyprctl monitors all
```

Then edit `~/.config/hypr/monitors.lua`, change `local omarchy_gdk_scale = 2` to `1`, and uncomment the specific-monitor line with your output name and mode. Apply with `hyprctl reload`.

Dynamic resizing, where the guest desktop follows the hypervisor window, is a separate thing. That needs the guest agent.

## Guest tools are never installed

Issue #10620 shows the gap clearly: the live ISO runs the VMware toolbox during install, and the installed system has none of it. There is no `vmtoolsd` process, so shared folders, the shared clipboard and display integration are all missing. The same is true of the QEMU and VirtualBox agents.

Install the right one by hand. If pacman answers with target not found, run `sudo pacman -Sy` first: the ISO installs offline, so the package database starts out stale, and `omarchy pkg add` runs a plain `pacman -S --needed` without syncing it. [The VirtualBox page](/run/virtualbox/) has the reports behind that.

On VMware:

```bash
omarchy pkg add open-vm-tools
sudo systemctl enable --now vmtoolsd vmware-vmblock-fuse
```

On QEMU, KVM, Proxmox, virt-manager or GNOME Boxes:

```bash
omarchy pkg add qemu-guest-agent spice-vdagent
sudo systemctl enable --now qemu-guest-agent
```

On VirtualBox:

```bash
omarchy pkg add virtualbox-guest-utils
sudo systemctl enable --now vboxservice
```

Host to guest clipboard comes from these packages, not from Omarchy. Omarchy's own `Super + C` and `Super + V` are a universal copy and paste that synthesises key events inside the session, so they do nothing for the host clipboard.

In issue #2513, from the 3.0 era, a commenter reported that installing `virtualbox-guest-utils-nox` was what finally let their virt-manager guest change resolution, and a GNOME Boxes user later confirmed the same. Nobody in that thread established why it works, but the package is small, so it is worth trying if `spice-vdagent` alone does not give you dynamic resizing.

## Invisible mouse cursor

On `vmwgfx` the DRM cursor plane never accepts Hyprland's cursor buffer, so the pointer is visible in the boot splash and the display manager and then vanishes the moment the compositor starts. BigNatoDemon counted over 1,700 failed cursor commits in a single session in issue #7918. Append to `~/.config/hypr/looknfeel.lua`:

```lua
hl.config({
  cursor = {
    no_hardware_cursors = true,
  },
})
```

Check it took with `hyprctl getoption cursor:no_hardware_cursors`. Two things that do not work, per the same report: current Hyprland pays no attention to the old `WLR_NO_HARDWARE_CURSORS` variable, and putting a `cursor` block in a leftover `hyprland.conf` has no effect once `hyprland.lua` is in charge.

Omarchy already does this automatically for nouveau, in `install/user/hardware/fix-nouveau-cursor.sh`. It does not do it for `vmwgfx`. One knock-on, reported in issue #8240 and still open: `omarchy-capture-screenshot` forces hardware cursors back on for the duration of the region picker, so your pointer vanishes while you drag the selection box.

## Input oddities

**Duplicated letters while typing.** Omarchy's default `repeat_delay` is 250 ms, still set in `default/hypr/input.lua` on 4.0.4. Crankygeek01-dev reported in issue #8760 that on a Parallels guest a normal key press can stay down long enough to trip that threshold, and because `repeat_rate = 40` is fast you get a burst rather than one extra letter: `helllo`, `commmand`, a few times per paragraph. The reporter flags a caveat up front: with a hypervisor in the path, key timing is less regular than on bare metal, so the problem could be limited to VM guests. Their override in `~/.config/hypr/input.lua` cleared it completely, with 500 already a big improvement:

```lua
hl.config({
  input = {
    repeat_delay = 600,
    repeat_rate = 30,
  },
})
```

**The middle of the top bar does not respond to clicks.** novastate isolated this in issue #8834 to absolute pointing devices. The report is a KVM guest driven over Moonlight: with the client in its normal absolute mouse mode, the clock, weather, microphone and media widgets in the centre ignored every click while the left and right sections worked, and switching Moonlight to relative (game) mouse mode fixed it immediately. A QEMU USB tablet is also an absolute device, but the report does not test one on its own, and the mechanism inside the bar is still unproven.

## Things that freeze or hang

**The screensaver freezes a SPICE session.** `bin/omarchy-screensaver` launches `ttfx` with `--frame-rate 120` and offers no way to change it, still true in 4.0.4. On a QXL guest with 16 MiB of VRAM, howdeploy recorded the first TTM buffer eviction failure 48 seconds after the screensaver started, followed by a dead render path that only a session restart cleared. With a patched launcher from a draft PR, the same guest ran clean for 20 minutes each at 20 and at 30 FPS. Until that default changes, turn it off in a VM:

```bash
omarchy toggle screensaver
```

**Random hard hangs under VMware Workstation.** Issue #8943 is open: an installed 4.0.1 guest hung at varying points while the live ISO ran fine, and the reporter believes the T2 patched kernel is involved. That one is a single report and the cause is not confirmed. Note that the 4.0.4 update brings in the `linux-omarchy` kernel through a migration that deliberately leaves the kernel you were running installed, so on an upgraded system you can pick the older Limine entry if the new kernel makes things worse. A fresh 4.0.4 install gets `linux-omarchy` only.

**A plain text LUKS prompt instead of the themed one.** Cosmetic only. Under QEMU with OVMF, systemd-stub sees the emulated serial console and appends `console=uart,io,0x3f8`, which makes Plymouth drop to its text plugin. JasonStreifling documented the whole chain in issue #11337. His verified fix is a drop-in under `/etc/limine-entry-tool.d/` containing `KERNEL_CMDLINE[default]+=" console=tty0"`, followed by `limine-update`: once the command line already carries a `console=` parameter, systemd-stub stops adding its own.

## Performance

Forcing software GL means the compositor's animations and every GPU application run on the CPU. Expect it to feel slow, and do not judge Omarchy's performance from a VM configured this way.

Emulation is worse again. Issue #1930, now closed, is a UTM guest on an M1 Pro where the install alone took about 90 minutes. There is no ARM64 Omarchy ISO, so on Apple silicon you are emulating x86 unless you use a different route. The manual points M-series users at Asahi or at the community Parallels guide, discussion #452.

## What to watch for on newer versions

Issue #10620 asks upstream for the obvious fix: detect the hypervisor at install time with `systemd-detect-virt` and install the matching guest package, covering VMware, QEMU and VirtualBox, and default the scale to 1x on a virtual display. It is open as of 2026-09-16. If that lands in a later release, the guest tools and scaling sections above stop being necessary.

The graphics workaround is the one to keep checking. If a Mesa, kernel or Hyprland update makes `vmwgfx` buffer sharing work, delete the `hl.env` line and restart the session to get hardware rendering back. The Hyprland side of that was filed with a patch but the issue was auto-closed, so watch the packaged Hyprland version rather than the issue tracker.

Anything written before 2026-08-14 describes Omarchy 3.x, where Hyprland config was `.conf` files and the VirtualBox display advice was the reverse of what works on 4, as [the VirtualBox page](/run/virtualbox/) explains. Check the date on any VM guide before following it.

## Related

- [Omarchy in VirtualBox](/run/virtualbox/)
- [Omarchy in VMware Workstation and Fusion](/run/vmware-workstation-fusion/)
- [Omarchy on Proxmox, QEMU and KVM](/run/proxmox-qemu-kvm/)
- [Omarchy in Parallels](/run/parallels/)
- [The Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
