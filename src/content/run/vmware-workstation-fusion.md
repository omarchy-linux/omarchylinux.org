---
title: "Running Omarchy in VMware Workstation and Fusion"
description: "Omarchy 4.x in VMware Workstation or Fusion: VM settings, the vmwgfx grey screen fix, open-vm-tools, guest resolution, clipboard, and the invisible cursor."
answer: "Enable Accelerate 3D graphics in the VM display settings, then add hl.env(\"QT_QUICK_BACKEND\", \"software\") to ~/.config/hypr/hyprland.lua. That stops the Quickshell crash loop that leaves you on a grey screen. Then install open-vm-tools, enable vmtoolsd and vmware-vmblock-fuse, turn on software cursors, and set the monitor scale to 1. Open issues #8113 and #10620 track the underlying vmwgfx bug."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "VMware Workstation and Fusion"
hostVersion: "Workstation Pro 26H1u1 and 17.6.4 on Windows"
tags: [vmware, vm, vmwgfx, quickshell, open-vm-tools, hyprland]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8113"
    title: "Issue #8113: Omarchy unusable under VMware Workstation with 3D acceleration enabled"
    kind: issue
    author: "cavanaug"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/10620"
    title: "Issue #10620: VMware guest: installer leaves the system without open-vm-tools (live ISO has them); plus working fix for the 3D-acceleration grey screen (#8113)"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/7918"
    title: "Issue #7918: Invisible mouse cursor in VMware guest: vmwgfx hardware cursor plane fails to commit (needs no_hardware_cursors)"
    kind: issue
    author: "BigNatoDemon"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/7835"
    title: "Issue #7835: I am trying to install and run Omarchy inside VMware, but I consistently get a black screen after entering my password."
    kind: issue
    author: "cn0xroot"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8943"
    title: "Issue #8943: Installed Omarchy 4.0.1 randomly hard-hangs in VMware Workstation 17.6.4 (live ISO works fine)"
    kind: issue
    author: "ncepuee"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/8240"
    title: "Issue #8240: Screenshot picker runs with hardware cursors forced on, hiding the pointer on nouveau/vmwgfx while you select"
    kind: issue
    author: "Chessing234"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/discussions/572"
    title: "Discussion #572: Omarchy on VMware Workstation on windows 11 host"
    kind: discussion
    author: "babusri"
    date: "2025-08-09"
  - url: "https://github.com/hyprwm/Hyprland/issues/16175"
    title: "Hyprland Issue #16175: vmwgfx (VMware): dmabuf handles cannot be closed with GEM_CLOSE"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://github.com/hyprwm/Hyprland/discussions/12966"
    title: "Hyprland Discussion #12966: Kitty and alacritty cannot launch in vmware workstation pro, 3d accel is enabled"
    kind: discussion
    author: "IceAsteroid"
    date: "2026-01-11"
  - url: "https://github.com/hyprwm/aquamarine/issues/360"
    title: "Aquamarine Issue #360: vmwgfx: compositor advertises dmabuf formats it cannot import"
    kind: issue
    author: "btsouth"
    date: "2026-08-20"
  - url: "https://github.com/vmware/open-vm-tools/issues/805"
    title: "open-vm-tools Issue #805: Wayland: vmusr's X11 resolutionSet plugin claims resolution_server over vmsvc's resolutionKMS"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy Manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy Manual: Monitors"
    kind: manual
  - url: "https://knowledge.broadcom.com/external/article/315602"
    title: "Compatibility considerations for Arm guest operating systems in Fusion VMs on Apple silicon"
    kind: docs
credits:
  - name: "kevincasier"
    url: "https://github.com/kevincasier"
    for: "Filed the Hyprland tracking issue with a tested patch for the vmwgfx TTM surface-handle bug, and reported the missing open-vm-tools on installed systems"
  - name: "Pascal-0x90"
    url: "https://github.com/Pascal-0x90"
    for: "Traced the dmabuf rejection to vmwgfx returning TTM surface handles that GEM_CLOSE cannot release, and wrote the first patch"
  - name: "rsuarezc0"
    url: "https://github.com/rsuarezc0"
    for: "Captured the fatal wl_surface.attach error behind the Quickshell crash loop and showed LIBGL_ALWAYS_SOFTWARE clears it"
  - name: "nenad82"
    url: "https://github.com/nenad82"
    for: "Measured that QT_QUICK_BACKEND=software fixes the shell while leaving the compositor on the GPU"
  - name: "dsuarezv"
    url: "https://github.com/dsuarezv"
    for: "Worked out the resolutionKMS config, the vfr repaint fix, and an autofit helper"
  - name: "BigNatoDemon"
    url: "https://github.com/BigNatoDemon"
    for: "Found that vmwgfx never commits the hardware cursor plane, so software cursors are required"
  - name: "Kor123"
    url: "https://github.com/Kor123"
    for: "Showed XWAYLAND_NO_GLAMOR stops XWayland apps from taking the session down"
faq:
  - q: "Do I need to enable 3D acceleration for Omarchy in VMware?"
    a: "Yes, in practice. dsuarezv's report in issue #8113 says Hyprland could not initialise its renderer with Accelerate 3D graphics off, and #8943 saw the session die with it off. One #7918 reporter got a desktop without it, but every working recipe has it on. Turn it on, then work around the vmwgfx bug in software."
  - q: "Why is my Omarchy VM stuck on a grey or black screen with only a mouse cursor?"
    a: "The Omarchy shell is crash-looping, not the compositor. Quickshell's GPU surface is rejected by Hyprland on vmwgfx, and with no bar and no wallpaper the desktop is a flat fill. Check with journalctl -b -t omarchy-shell."
  - q: "Can I run Omarchy in VMware Fusion on an Apple Silicon Mac?"
    a: "No. Broadcom's documentation says Fusion on Apple Silicon runs only Arm guests, and Omarchy ships an x86_64 ISO. Fusion on an Intel Mac uses the same vmwgfx stack as Workstation, so expect the same problems and the same fixes."
  - q: "Does the Omarchy installer set up open-vm-tools for me?"
    a: "No. Issue #10620 reports that the live ISO runs VMware guest tools but the installed system has no open-vm-tools at all. Nothing in the 4.0.4 tree detects a VMware guest. You install and enable them yourself."
related: [virtualbox, proxmox-qemu-kvm, what-breaks-in-a-vm]
draft: false
---

VMware is one of the rougher places to run Omarchy 4.x. The desktop boots, and then you sit on a flat grey rectangle with a mouse cursor. That is not a broken install. It is a real bug in how the VMware graphics driver hands buffers to Hyprland, and it has a workaround that takes about five minutes.

This page was checked against Omarchy 4.0.4. The official manual lists VMware under [Omarchy on...](https://omarchy.org/manual/omarchy-on/), but it points at [discussion #572](https://github.com/omacom/omarchy/discussions/572) from August 2025, which is 3.x era advice written before Quattro replaced the whole desktop shell. Every confirmed report below is VMware Workstation, nearly all on a Windows host; the reporter in [issue #7835](https://github.com/omacom/omarchy/issues/7835) saw the same black screen from an Ubuntu host too. Fusion on an Intel Mac uses the same `vmwgfx` driver and should behave the same, but there is no Omarchy-specific Fusion report to cite. The closest is a comment in [Hyprland discussion #12966](https://github.com/hyprwm/Hyprland/discussions/12966) reporting the same `vmwgfx` failure, and the same patch, on Fusion. Fusion on Apple Silicon is out: [Broadcom's documentation](https://knowledge.broadcom.com/external/article/315602) says it runs Arm guests only, and Omarchy is x86_64.

## VM settings before you install

- Firmware: UEFI.
- Display: turn **Accelerate 3D graphics** on. dsuarezv's write-up in issue #8113 reports that with it off, Hyprland never got a renderer up and the display stayed blank, and issue #8943 saw the session die after unlock with it off. One reporter in #7918 did reach a desktop without acceleration, so it is not absolute, but every working recipe in the tracker has it on. Counter-intuitive, given that the fix below is partly software rendering, but the compositor still wants a working GL stack.
- The one report that lists VM sizing (issue #8943) used 4 vCPUs and 8 GB of RAM. Software-rendered surfaces cost CPU, so do not go smaller than that without a reason.
- Get the ISO from [omarchy.org](https://omarchy.org) and check it against [the verification page](/verify/) before you boot it.

## The fix

The live ISO is usually fine. The problems start on the installed system. If you are already stuck on the grey screen, switch to a TTY with `Ctrl + Alt + F2` and log in there.

1. Stop the shell crash loop. Add this at the bottom of `~/.config/hypr/hyprland.lua`:

```lua
hl.env("QT_QUICK_BACKEND", "software")
hl.env("XWAYLAND_NO_GLAMOR", "1")
```

The first line makes Qt Quick render the Omarchy shell into a shared-memory buffer instead of a GPU dmabuf, so the buffer Hyprland rejects is never created. The second stops XWayland apps from taking the session down the same way.

2. Install the VMware guest tools and turn them on:

```bash
omarchy pkg add open-vm-tools gtkmm3 libxtst
sudo systemctl enable --now vmtoolsd.service vmware-vmblock-fuse.service
```

3. The desktop-side agent does not start on its own under Omarchy's uwsm session. Add it to `~/.config/hypr/autostart.lua`:

```lua
o.launch_on_start("vmtoolsd -n vmusr")
```

That agent is what carries the shared clipboard and drag and drop between host and guest.

4. Make the guest follow the VMware window size. On a Wayland-only install there is no `xf86-video-vmware`, so open-vm-tools does not enable its KMS resolution plugin by itself:

```bash
sudo install -d /etc/vmware-tools
printf '%s\n' '[resolutionKMS]' 'enable=true' | sudo tee /etc/vmware-tools/tools.conf
sudo systemctl restart vmtoolsd
```

5. Make the mouse pointer visible. `vmwgfx` never commits the hardware cursor plane, so add this to `~/.config/hypr/looknfeel.lua`:

```lua
hl.config({
  cursor = {
    no_hardware_cursors = true,
  },
})
```

6. Fix the scale. Omarchy ships `GDK_SCALE=2` for retina-class panels, which on a 1280x800 virtual display gives you an effective 640x400 desktop. Open `~/.config/hypr/monitors.lua` and set both values to 1:

```lua
local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1
```

7. Reboot, or log out and back in. `GDK_SCALE` and the `hl.env` lines only reach processes started after the session begins.

## Verify it worked

```bash
journalctl -b -t omarchy-shell | grep -c 'exited with status'
hyprctl getoption cursor:no_hardware_cursors
pgrep -a -f vmtoolsd
head -n1 /sys/class/drm/card0-Virtual-1/modes
```

The first should print `0`. Omarchy's shell launcher gives up after five relaunches inside a minute and logs each one, so any non-zero count means the shell is still dying. The second should show the option switched on; issue #7918 reports `set: true` in its output once the block is loaded. The third should show both `/usr/bin/vmtoolsd` and a `vmtoolsd -n vmusr` process. The fourth should change when you resize the VMware window, which tells you `resolutionKMS` is live.

## Why it happens

Mesa's `svga` driver advertises no dmabuf render modifiers for the scanout formats, while the `vmwgfx` kernel driver advertises only `LINEAR`. Hyprland's compositor side survives that, falling back to implicit modifiers, but GPU-accelerated Wayland clients do not. Quickshell's surface gets rejected at `wl_surface.attach` with `invalid arguments`, which is a fatal Wayland protocol error, and Qt leaves through `_exit()` without raising a signal. Omarchy's `bin/omarchy-launch-shell` supervises exactly that kind of silent death, retries five times, then gives up. With no bar and no wallpaper you are left looking at Hyprland's background fill, which is why it reads as a black or grey screen rather than a crash.

There is a second half to the same mess. Pascal-0x90 traced it in [Hyprland discussion #12966](https://github.com/hyprwm/Hyprland/discussions/12966) and kevincasier filed it as [Hyprland #16175](https://github.com/hyprwm/Hyprland/issues/16175): when `vmwgfx` imports a surface-backed dmabuf it hands back a TTM surface handle, not a GEM handle, so the `drmCloseBufferHandle()` call Hyprland makes afterwards returns `EINVAL` and the log fills up. That issue carries a tested patch, but it was auto-closed as not planned by the Hyprland bot, which no longer accepts user-filed issues. The live discussion is [Hyprland #12966](https://github.com/hyprwm/Hyprland/discussions/12966), and the aquamarine side is [#360](https://github.com/hyprwm/aquamarine/issues/360), open since 2026-08-20. Nothing has shipped upstream as of 2026-09-16.

On the Omarchy side, `grep` over the 4.0.4 tree finds no VMware detection at all. What the tree does have is `install/user/hardware/fix-nouveau-cursor.sh`, which appends the same `no_hardware_cursors` block when it sees nouveau. Issue #7918 asks for the identical treatment for `vmwgfx` and issue #10620 asks the installer to install open-vm-tools when `systemd-detect-virt` reports `vmware`. Both were open on 2026-09-16.

## If that did not work

**The shell comes up but text appears only when you move the mouse.** Damage-driven page flips get missed on this driver. dsuarezv's fix is to make Hyprland repaint continuously, in `~/.config/hypr/looknfeel.lua`:

```lua
hl.config({
  debug = {
    vfr = false,
  },
})
```

Apply with `hyprctl reload` and confirm with `hyprctl getoption debug:vfr`. It costs some idle CPU.

**`QT_QUICK_BACKEND=software` is not enough.** The bigger hammer is `hl.env("LIBGL_ALWAYS_SOFTWARE", "1")`, which pushes the whole session onto llvmpipe. nenad82 measured roughly 12 percent idle Hyprland CPU that way against about 4 percent with the narrower setting, so try the narrow one first. Note that `hl.env` does not reach the SDDM greeter, which runs its own Hyprland; for that you need the variable in `/etc/environment` instead, as suggested in #10620.

**Advice from a 3.x guide does nothing.** Omarchy 4 moved Hyprland config to Lua. Editing `~/.config/hypr/envs.conf` has no effect, and #7918 found that Hyprland skips a `cursor { }` block in a leftover `hyprland.conf` once `hyprland.lua` is present. See [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

**Screenshots lose the pointer.** Issue #8240 reports that `omarchy-capture-screenshot` forces hardware cursors back on for the duration of the region picker, which makes the pointer vanish on exactly the drivers that needed software cursors. Open on 2026-09-16, no workaround beyond picking blind.

**The whole guest hard-hangs at random.** Issue #8943 reports that on Workstation 17.6.4, with acceleration on or off, and notes the installed kernel was an Apple T2 build. I checked: `install/hardware/apple/fix-t2.sh` only installs `linux-t2` when `lspci` finds Apple PCI IDs `106b:1801` or `106b:1802`, so that path should not run on an ordinary VMware guest. Why that reporter ended up on a T2 kernel is unexplained. Check `uname -r` before assuming the same cause.

**Autofit still does nothing after step 4.** Hyprland reads the connector's preferred mode at startup and does not react to the `vmwgfx` hotplug update, so `hyprctl monitors` keeps reporting the old size even though `/sys` shows the new one. You can apply it by hand:

```bash
hyprctl eval 'hl.monitor({ output = "Virtual-1", mode = "1600x900@60", position = "auto", scale = 1 })'
```

dsuarezv published a polling helper in #8113 that does this automatically and rounds the requested size so fractional scales survive.

## What to watch for on newer versions

The current development branch snapshot still contains no VMware or `vmwgfx` handling. The only match in that tree is the same manual paragraph as in 4.0.4. So the real fix has to come from Hyprland or aquamarine, and neither has merged one. Watch [aquamarine #360](https://github.com/hyprwm/aquamarine/issues/360) rather than the Omarchy tracker. Until then, treat every item above as something you apply yourself after each fresh install.
