---
title: "Run Omarchy 4 in VirtualBox: settings, fixes, guest additions"
description: "How to run Omarchy 4 in VirtualBox: VMSVGA with 3D acceleration, 128 MB VRAM, guest additions, and the software GL fix for the black screen."
answer: "Set the VM to EFI, VMSVGA, 128 MB video memory and 3D acceleration on. Boot, drop to a TTY with Ctrl+Alt+F3, run sudo pacman -Sy, then omarchy pkg add virtualbox-guest-utils and systemctl enable --now vboxservice. Add an hl.env line setting LIBGL_ALWAYS_SOFTWARE to 1 in ~/.config/hypr/hyprland.lua after the bootstrap line, then reboot. The Omarchy kernel ships the guest modules."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "VirtualBox"
hostVersion: "7.x (exact build not stated in the Omarchy 4 reports)"
tags: [virtualbox, vm, black-screen, hyprland, quickshell]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/7758"
    title: "Discussion #7758: Omarchy on VirtualBox"
    kind: discussion
    author: "nightdevil00"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/discussions/176"
    title: "Discussion #176: Omarchy on VirtualBox"
    kind: discussion
    author: "matsest"
    date: "2025-07-14"
  - url: "https://github.com/omacom/omarchy/issues/10620"
    title: "Issue #10620: VMware guest: installer leaves the system without open-vm-tools (live ISO has them); plus working fix for the 3D-acceleration grey screen (#8113)"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/8113"
    title: "Issue #8113: Omarchy unusable under VMware Workstation with 3D acceleration enabled"
    kind: issue
    author: "cavanaug"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/issues/2028"
    title: "Issue #2028: Keyboard Not Registering Keystrokes in VirtualBox"
    kind: issue
    author: "ankur3-101106"
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/issues/11735"
    title: "Issue #11735: Super+print breaks Omarchy Instalation (VirtualBox)"
    kind: issue
    author: "andik309"
    date: "2026-09-13"
  - url: "https://github.com/hyprwm/Hyprland/issues/16175"
    title: "Hyprland issue #16175: vmwgfx (VMware): dmabuf handles cannot be closed with GEM_CLOSE"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/profiledef.sh"
    title: "omarchy-iso profiledef.sh: x86_64, bootmodes bios.syslinux and uefi.grub"
    kind: source
credits:
  - name: "nightdevil00"
    url: "https://github.com/nightdevil00"
    for: "The Omarchy 4 VirtualBox guide: VMSVGA with 3D on, guest utils, and the LIBGL_ALWAYS_SOFTWARE line in hyprland.lua"
  - name: "rodolfoghi"
    url: "https://github.com/rodolfoghi"
    for: "Diagnosing the black screen down to vmwgfx and Hyprland aborting at GPU init, and listing the dead ends"
  - name: "kevincasier"
    url: "https://github.com/kevincasier"
    for: "Tracing the vmwgfx dmabuf handle failure and reporting it upstream to Hyprland"
faq:
  - q: "Why does Super + Return do nothing while Super + B opens the browser?"
    a: "The Super key is reaching the guest. The apps bound to those keys are crashing at OpenGL init, so nothing appears. Fix the graphics stack and the bindings start working again."
  - q: "Should I turn 3D acceleration off like the old guide says?"
    a: "Not as the first thing to try. The VBoxVGA and 3D off recipe was written for Omarchy 1.x through 3.x, and the people who diagnosed the Omarchy 4 black screen found Hyprland crashing at GPU init with 3D off. One user did report 4.0.0 working with the old settings, so it is a fallback, not the recipe."
  - q: "Does editing hyprland.conf work in a VM?"
    a: "No. Omarchy 4 moved Hyprland config to Lua. Edits to ~/.config/hypr/*.conf are ignored, which is why older VM guides appear to do nothing."
  - q: "Is VirtualBox fast enough for daily use?"
    a: "It is usable but not fast. Forcing software GL means animations and GPU applications run on the CPU. On a Linux host, QEMU or KVM is a better experience."
related: [what-breaks-in-a-vm, vmware-workstation-fusion, proxmox-qemu-kvm]
draft: false
---

Omarchy 4 runs in VirtualBox, but the settings that worked for Omarchy 1.x through 3.x are now wrong, and the official manual still links to the old thread. This page was checked against Omarchy 4.0.4 (2026-09-15) and the two community guides for VirtualBox.

The short version: the graphics controller must be VMSVGA with 3D acceleration on, and OpenGL clients have to be forced onto software rendering. Everything that looks like a broken keyboard is really a graphics failure.

## The fix

### 1. VM settings, before you boot

In VirtualBox Manager, select the VM and open Settings.

- System, Motherboard: enable EFI. The Omarchy ISO is x86_64 only. Its build profile lists both a BIOS and a UEFI boot mode, but every working Omarchy 4 report used UEFI, and one user in discussion #176 found the ISO did not show up in the boot menu until EFI was on. Treat EFI on as the tested path.
- System: leave Secure Boot and TPM off. The manual asks for this on bare metal too, in [Getting Started](https://omarchy.org/manual/getting-started/).
- Display: Graphics Controller `VMSVGA`, Video Memory `128 MB`, Enable 3D Acceleration checked.
- 8 GB RAM, 4 vCPUs and a 40 GB disk is the sizing the community guides have used since 2025. Give it more if you have it.

Do not start from the VBoxVGA and "3D acceleration unchecked" recipe in discussion #176. That was written for Omarchy 1.x and updated for 3.x. On Omarchy 4.0.2, rodolfoghi found Hyprland crashing at GPU init with 3D acceleration off. One person in that thread (jontzi, 2026-08-25) did report 4.0.0 working with the old VBoxVGA settings, so they are not impossible, but the VMSVGA recipe is the one that comes with a diagnosis and multiple confirmations.

### 2. Install, then get to a terminal

Install Omarchy normally. Remove the ISO from the virtual optical drive before the first reboot, or the VM boots the installer again.

If you get a black screen with only a mouse pointer after the login, switch to a text console with `Ctrl + Alt + F3` and log in there.

### 3. Refresh pacman and install the guest additions

The Omarchy ISO is an offline installer, so the package database on a fresh install is stale. Several people hit "target not found" or dependency loops purely because of that.

```bash
sudo pacman -Sy
omarchy pkg add virtualbox-guest-utils
sudo systemctl enable --now vboxservice.service
```

`virtualbox-guest-utils` is in Arch's `extra` repository. It depends on a kernel that provides `VIRTUALBOX-GUEST-MODULES`, and both Arch's stock `linux` and Omarchy's own `linux-omarchy` (7.2.5 in the stable channel as of this check) provide it, so no separate module package or DKMS build is needed. The guest additions are what give you automatic display resizing when you resize the VirtualBox window.

### 4. Force GL clients onto software rendering

Omarchy 4 reads Hyprland config from Lua, not `.conf` files. Add the environment variable to `~/.config/hypr/hyprland.lua`, right after the line that loads the bootstrap file:

```bash
sed -i '/bootstrap.lua/a hl.env("LIBGL_ALWAYS_SOFTWARE", "1")' ~/.config/hypr/hyprland.lua
```

Take a backup first if you prefer, for example `cp ~/.config/hypr/hyprland.lua ~/.config/hypr/hyprland.lua.bak`.

Then reboot. rodolfoghi rebooted and the desktop came up. The original guide instead restarts only the shell from a working session:

```bash
omarchy restart shell
```

If the shell restart does not bring the bar back, reboot.

### 5. Fix the resolution

Omarchy 4 ships `~/.config/hypr/monitors.lua` with `omarchy_gdk_scale = 2` and monitor scale set to `auto`. On a small virtual display that gives you a desktop that looks half-size. List what the virtual GPU offers, then pin it:

```bash
hyprctl monitors all
```

Edit `~/.config/hypr/monitors.lua`, set `local omarchy_gdk_scale = 1`, and uncomment the specific-monitor line for the virtual output:

```lua
hl.monitor({ output = "Virtual-1", mode = "1920x1080@60", position = "0x0", scale = 1 })
```

Apply it with `hyprctl reload`.

## Verify it worked

```bash
hyprctl layers | grep omarchy-bar
hyprctl configerrors
journalctl -b | grep -i vmwgfx
```

The `omarchy-bar` layer is the Omarchy top bar. If it is listed and `hyprctl configerrors` is clean, the shell is running. The `vmwgfx` grep should be quiet. A repeating channel error there means the guest graphics stack is still failing.

Resizing the VirtualBox window should now resize the guest desktop, which tells you `vboxservice` is running.

## Why it happens

VirtualBox's VMSVGA controller emulates a VMware SVGA II adapter, so inside the guest you are on the `vmwgfx` kernel driver. That driver's buffer sharing does not work the way Hyprland expects. Hyprland 0.56 uses Aquamarine rather than wlroots, and it does not fall back to software when GPU buffer import fails. It either aborts at GPU init or rejects every client's buffer, which shows up as `invalid arguments for wl_surface.attach` and a fatal Wayland connection error, and Quickshell crashes in a loop until the shell supervisor gives up.

This is the same defect people hit on VMware Workstation, reported in issues #8113 and #10620. In #10620 the cause was traced to `GEM_CLOSE` failing on `vmwgfx` when Hyprland closes an imported dmabuf handle. The upstream report, Hyprland issue #16175, was closed automatically by a bot because that project no longer accepts user-filed issues, not because a fix shipped. So treat the software rendering setting as a workaround with no end date.

This is also the most likely explanation for the long run of "the keyboard does not work in a VM" reports, such as issue #2028. People found that `Super + B` opened the browser while `Super + Return` and `Super + Space` did nothing. The bindings that worked all launched apps that survived a broken GL path, and the ones that failed launched the terminal and the launcher. In that issue, the suggested fix was `LIBGL_ALWAYS_SOFTWARE`, and in discussion #176 the fix was changing the graphics controller. Fix the graphics and the bindings come back.

## If that did not work

- **`virtualbox-guest-utils` will not install.** Run `sudo pacman -Sy` first. jfedgar reported in discussion #176 (on 3.x, with the `-nox` package) that syncing the database, then installing `linux-headers`, cleared the dependency loop. With the stock kernels no module build is needed, so the sync is the part that matters.
- **Appending to a file does nothing.** Follow bash-style instructions with `sed` or `tee` rather than `>>` if your shell is not bash. rodolfoghi flagged this as a trap while debugging in a TTY.
- **You cannot paste into the TTY.** VirtualBox's shared clipboard only works inside the graphical session, so expect to type the commands out.
- **Black screen after the disk decryption prompt, not after login.** Go back to Display settings and confirm all three of VMSVGA, 128 MB and 3D acceleration.
- **You updated to 4.0.4 and want to know what changed for the VM.** That release installs the `linux-omarchy` kernel and makes it the first Limine boot entry. That kernel provides the VirtualBox guest modules, so `vboxservice` should keep working. The previous kernel is deliberately left installed, so if the new one does not boot in your VM you can pick the old entry in the Limine menu. No VirtualBox report about the 4.0.4 kernel exists yet.
- **You cannot open the menu at all.** Click the Omarchy logo at the left of the top bar with the mouse. That reaches the menu without any keybinding.
- **The install itself failed.** Issue #11735 is open as of 2026-09-13: pressing `Super + Print` repeatedly during the install, on a Russian layout, breaks the installation. Leave the keyboard alone while it installs.
- **Apple silicon Mac host.** There is no ARM64 Omarchy ISO. The manual points M-series Mac users at Asahi or a Parallels guide instead. See [running Omarchy on Apple silicon](/hardware/apple-silicon-asahi/).

## What to watch for on newer versions

Omarchy 4.0.4 does not detect that it is running in a VM. There is no `systemd-detect-virt` call anywhere in the tree, no guest tooling is installed, and the default 2x GDK scale is applied whatever the display. Issue #10620 asks for exactly that detection, covering VMware, QEMU and VirtualBox. If it lands in a later release, steps 3 and 5 above become unnecessary.

If a Mesa, kernel or VirtualBox update fixes the buffer sharing, remove the `hl.env` line you added and restart the session to get hardware rendering back. Until then, expect slow animations and poor performance in anything GPU heavy. On a Linux host, one user in discussion #176 who moved from VirtualBox to QEMU with virt-manager found it noticeably faster.

Note the version boundaries. Anything written before 2026-08-14 describes Omarchy 3.x, where the Hyprland config was `.conf` files and the advice was the opposite: VBoxVGA with 3D off. See [the Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) if you are converting an older VM guide.

## Related

- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [VMware Workstation and Fusion](/run/vmware-workstation-fusion/)
- [Proxmox, QEMU and KVM](/run/proxmox-qemu-kvm/)
- [Upgrading 3 to 4](/upgrade/3-to-4-quattro/)
