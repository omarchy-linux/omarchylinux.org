---
title: "Omarchy in a virtual machine"
description: "What works and what breaks when Omarchy 4.x runs as a guest in VMware, VirtualBox, QEMU/KVM, Proxmox, UTM or Parallels, and the fixes people verified."
answer: "Omarchy 4.x installs and runs in a virtual machine, but nothing is tuned for it. The tree ships no guest tools and no hypervisor detection. QEMU/KVM with virtio is the smoothest. VMware with 3D acceleration crash-loops the shell, and the working fix is QT_QUICK_BACKEND=software in hyprland.lua. Give the VM UEFI firmware, or the UKI will not boot."
appliesTo:
  from: "4.0.0"
status: info
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: component
componentKey: "vm"
issueCount: 106
tags: [vm, virtual-machine, vmware, virtualbox, qemu, proxmox]
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
  - url: "https://github.com/omacom/omarchy/issues/7835"
    title: "Issue #7835: Black screen after entering password when running Omarchy inside VMware"
    kind: issue
    author: "cn0xroot"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/11337"
    title: "Issue #11337: Plymouth falls back to the unthemed text LUKS prompt on UKI installs under QEMU (systemd-stub auto-appends console=uart,io,0x3f8)"
    kind: issue
    author: "JasonStreifling"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/11011"
    title: "Issue #11011: Black screen or plymouthd crash under Proxmox with GPU passthrough, can boot with serial console help"
    kind: issue
    author: "romixlab"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10282"
    title: "Issue #10282: Sunshine error 503 on hosts with no physical input (VM / GPU passthrough)"
    kind: issue
    author: "jimdawdy-hub"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/11735"
    title: "Issue #11735: Super+print breaks Omarchy Instalation (VirtualBox)"
    kind: issue
    author: "andik309"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/1176"
    title: "Issue #1176: BUG: Wayland Drivers - Omarchy 2.0 in VMs"
    kind: issue
    author: "kmf"
    date: "2025-08-27"
  - url: "https://github.com/omacom/omarchy/issues/2028"
    title: "Issue #2028: Keyboard Not Registering Keystrokes in VirtualBox"
    kind: issue
    author: "ankur3-101106"
    date: "2025-09-28"
  - url: "https://github.com/omacom/omarchy/issues/2144"
    title: "Issue #2144: Default Hyprland Monitor Scaling set to 2x Retina in Omarchy v3.0.2 (VirtualBox)"
    kind: issue
    author: "Rovetown"
    date: "2025-10-01"
  - url: "https://github.com/omacom/omarchy/issues/2761"
    title: "Issue #2761: Keyboard not working after login screen in virtualbox"
    kind: issue
    author: "Mr-GymKid"
    date: "2025-10-23"
  - url: "https://github.com/omacom/omarchy/issues/1930"
    title: "Issue #1930: unusably slow in QEMU"
    kind: issue
    author: "tcurdt"
    date: "2025-09-25"
  - url: "https://github.com/omacom/omarchy/issues/2513"
    title: "Issue #2513: QEMU Display Scaling Issue"
    kind: issue
    author: "rami-shalhoub"
    date: "2025-10-17"
  - url: "https://github.com/omacom/omarchy/issues/2251"
    title: "Issue #2251: Add VM Guides"
    kind: issue
    author: "ryanrhughes"
    date: "2025-10-06"
  - url: "https://github.com/omacom/omarchy/issues/10617"
    title: "Issue #10617: Stale Brave Origin SingletonLock shipped in Try Omarchy image prevents the browser from starting"
    kind: issue
    author: "m-a-mohsen"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/9505"
    title: "Issue #9505: Chromium main process SIGTRAPs on VM close (VM teardown triggers gpu_data_manager fatal CHECK)"
    kind: issue
    author: "drumguy1384"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/127"
    title: "Issue #127: Add auto-detection of scale setting"
    kind: issue
    author: "dhh"
    date: "2025-07-10"
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/unattended-installs/"
    title: "Omarchy manual: Unattended Installs"
    kind: manual
    date: "2026-09-15"
credits:
  - name: "rsuarezc0"
    url: "https://github.com/rsuarezc0"
    for: "The WAYLAND_DEBUG trace pinning the VMware crash-loop on a rejected dmabuf from vmwgfx"
  - name: "nenad82"
    url: "https://github.com/nenad82"
    for: "Measuring QT_QUICK_BACKEND=software against LIBGL_ALWAYS_SOFTWARE and showing the compositor does not need software rendering"
  - name: "dsuarezv"
    url: "https://github.com/dsuarezv"
    for: "The vmwgfx dmabuf handle patch and the end to end VMware 4.0.2 recipe"
  - name: "Kor123"
    url: "https://github.com/Kor123"
    for: "Finding that XWAYLAND_NO_GLAMOR=1 stops XWayland apps from killing the VMware session"
  - name: "kevincasier"
    url: "https://github.com/kevincasier"
    for: "Documenting that the installed system ends up without open-vm-tools although the live ISO runs them"
  - name: "JasonStreifling"
    url: "https://github.com/JasonStreifling"
    for: "Root causing the text mode LUKS prompt to systemd-stub appending a serial console under OVMF"
faq:
  - q: "Which hypervisor gives the least trouble on Omarchy 4?"
    a: "QEMU/KVM with virtio-gpu on a Linux host. It is the only virtual GPU the Omarchy tree mentions at all, and the first boot greeter explicitly handles the virtio-gpu console resize. VMware has the most open graphics bugs."
  - q: "Does Omarchy install guest tools for me?"
    a: "No. As of 4.0.4 there is no open-vm-tools, spice-vdagent, qemu-guest-agent or VirtualBox guest package anywhere in the install tree, and no systemd-detect-virt call. Install them yourself after the first boot."
  - q: "Why is everything huge in my VM window?"
    a: "monitors.lua ships GDK_SCALE 2 because Omarchy assumes a retina class display. Step down with Super + / or set omarchy_gdk_scale to 1 in ~/.config/hypr/monitors.lua."
  - q: "Does the old envs.conf advice from VM guides still work?"
    a: "No. Hyprland config moved to Lua in 4.0.0. Environment variables now go in ~/.config/hypr/hyprland.lua as hl.env(\"NAME\", \"value\")."
related: [black-screen-after-login, quickshell-crashes-or-bar-missing, fractional-scaling-blurry-or-huge-apps, install-fails-or-stalls, boot-limine]
draft: false
---

## Status on 4.0.4

Omarchy installs and runs inside a virtual machine, and plenty of people trial it that way. It is also the least tended part of the hardware surface. The issue tracker counts 106 VM issues, 55 still open, and almost none of them have ever been closed by a code change in Omarchy itself.

The short version by hypervisor, checked against the v4.0.4 source tree and the open reports:

- QEMU/KVM and Proxmox on a Linux host are the smoothest path. virtio-gpu is the only virtual GPU the Omarchy tree acknowledges anywhere, and the first boot greeter in `bin/omarchy-provision-owner` has code that waits for the virtio-gpu KMS handoff before painting.
- VMware Workstation and Fusion are the worst. With 3D acceleration on, the Quickshell bar and panels crash-loop and you get a black or grey desktop with a cursor (#8113, #7835). With 3D acceleration off, Hyprland cannot initialise its renderer at all. There is a workaround, below.
- VirtualBox works for some people and not others. Most reports are old and 3.x era, and the closed ones were closed without a fix landing (#2028, #1176).
- Parallels, UTM and Hyper-V have no first party support at all. The manual points at community guides in [Omarchy on...](https://omarchy.org/manual/omarchy-on/).

One hard requirement: Omarchy 4 boots a UKI written to an EFI System Partition and managed by `limine-entry-tool`. Give the VM UEFI firmware. VirtualBox defaults to legacy BIOS, and that is behind a share of the "installed fine, will not boot" reports.

Nothing here changed with Quattro except the config format. The 3.x guides that tell you to edit `~/.config/hypr/envs.conf` are dead on 4.x, because Hyprland config is Lua now. See [the conf to Lua migration](/reference/hyprland-conf-to-lua-migration/).

## What Omarchy does automatically

Almost nothing, and that is the single most useful fact on this page.

Grep the v4.0.4 tree for `systemd-detect-virt`, `open-vm-tools`, `spice-vdagent`, `qemu-guest-agent` or `virtualbox-guest-utils` and you get no hits. `install/hardware/all.sh` runs 27 quirk scripts, every one of them keyed to physical hardware: ASUS ROG, Framework 16, Dell XPS haptics, Surface, NVIDIA, Intel, Apple. There is no VM leaf and no quirk script for this component.

Two consequences worth knowing:

- `install/hardware/vulkan.sh` only installs a Vulkan driver when `lspci` shows an Intel, AMD or Apple display device. A VMware SVGA II or VirtualBox adapter matches none of them, so a VM guest gets no Vulkan ICD installed.
- The live ISO runs VMware guest tools during install, but the installed system has none. kevincasier confirmed that on 4.0.2 in #10620: no `vmtoolsd`, no shared clipboard, no display resize.

What the tree does contain for VMs is all on the host side, for when you run VMs on Omarchy: `default/hypr/apps/qemu.lua` forces full opacity on QEMU windows, `omarchy-windows-vm` drives the Dockur Windows container, and the installer can consume a `cidata` drive for [unattended installs](https://omarchy.org/manual/unattended-installs/), which is aimed squarely at Proxmox and Packer.

Scaling is the other default that bites in a VM. `config/hypr/monitors.lua` ships `omarchy_monitor_scale = "auto"` but a hardcoded `omarchy_gdk_scale = 2`, because Omarchy assumes a retina class display. On a 1280x800 virtual display you get an effectively 640x400 desktop. Auto detection was requested in #127 back in July 2025 and closed in November 2025 without shipping a VM aware default.

## Known problems

| Issue | Where it hits | Status | Fixed in |
| --- | --- | --- | --- |
| [#8113](https://github.com/omacom/omarchy/issues/8113) shell crash-loops, black or grey desktop | VMware Workstation and Fusion, 3D acceleration on, vmwgfx | open | not fixed, workaround below |
| [#7835](https://github.com/omacom/omarchy/issues/7835) black screen after entering password | VMware on Windows and Linux hosts | open | not fixed |
| [#10620](https://github.com/omacom/omarchy/issues/10620) no open-vm-tools after install | VMware guests | open | not fixed |
| [#11337](https://github.com/omacom/omarchy/issues/11337) unthemed text LUKS prompt | QEMU and Proxmox with OVMF, UKI boot | open | not fixed |
| [#11011](https://github.com/omacom/omarchy/issues/11011) black screen or plymouthd crash | Proxmox 9.2 with GPU passthrough, q35 5.1 | closed, not reproducible on a newer q35 | no code change |
| [#10282](https://github.com/omacom/omarchy/issues/10282) Sunshine 503, capture never starts | any VM with no physical keyboard or mouse | open | not fixed |
| [#11735](https://github.com/omacom/omarchy/issues/11735) Super+Print during install breaks it | VirtualBox, reported once, no comments yet | open | unverified |
| [#2028](https://github.com/omacom/omarchy/issues/2028), [#2761](https://github.com/omacom/omarchy/issues/2761) keystrokes ignored after login | VirtualBox and VMware, 3.x | closed | no fix committed |
| [#2144](https://github.com/omacom/omarchy/issues/2144) desktop rendered at 2x, edges cut off | VirtualBox | closed as a duplicate of #127 | still the 4.0.4 default |
| [#2513](https://github.com/omacom/omarchy/issues/2513) tiny window or low resolution | QEMU with virt-manager | closed | no fix committed |
| [#9505](https://github.com/omacom/omarchy/issues/9505) Chromium dies when a VM shuts down | Omarchy as libvirt host, AMD GPU | open | not fixed |
| [#10617](https://github.com/omacom/omarchy/issues/10617) Brave will not start in the Try Omarchy image | Try Omarchy guest under Hyper-V | open | not fixed |

## Fixes that work

Work in this order.

**1. Firmware first.** Set the VM to UEFI, turn Secure Boot off, and give it 4 CPUs and 8 GB if you can. Emulated CPU, as opposed to KVM or a host matched hypervisor, is what made Omarchy unusably slow for the UTM reporter in #1930.

**2. VMware graphics.** Leave "Accelerate 3D graphics" enabled, then put this in `~/.config/hypr/hyprland.lua`:

```lua
hl.env("QT_QUICK_BACKEND", "software")
```

nenad82 measured that against the wider `LIBGL_ALWAYS_SOFTWARE=1` in #8113: both stop the crash-loop, but the Qt switch keeps Hyprland itself on the GPU, with idle CPU around 4 percent instead of 12. `QSG_RHI_BACKEND=software`, which several older guides recommend, does nothing at all here. Kor123 adds `hl.env("XWAYLAND_NO_GLAMOR", "1")` if XWayland apps such as Spotify take the session down with them.

The underlying bug is upstream, not in Omarchy: vmwgfx imports dmabufs as surface handles, the compositor's GEM close fails, and the client's `wl_surface.attach` is rejected with a fatal protocol error. dsuarezv posted a Hyprland patch in the same thread.

**3. VirtualBox graphics.** In #1176 the reporter got Hyprland starting by changing the graphics controller and leaving 3D acceleration unchecked. That is 2.x era advice and nobody has reconfirmed it on 4.x, so treat it as a thing to try rather than the answer.

**4. Install the guest tools yourself.** On VMware, `pacman -S open-vm-tools` then enable `vmtoolsd` and `vmware-vmblock-fuse`. On QEMU, `spice-vdagent` and `qemu-guest-agent`. That is what buys you clipboard sharing and window resize, which Omarchy will not set up for you.

**5. Fix the scale.** Press `Super + /` and `Super + Alt + /` to step scaling, which also rewrites `monitors.lua` so it survives a reboot, or edit `omarchy_gdk_scale` to 1 yourself. See [fractional scaling](/fix/fractional-scaling-blurry-or-huge-apps/).

**6. Text mode LUKS prompt under QEMU or Proxmox.** Add a console parameter so systemd-stub stops adding a serial one:

```
echo 'KERNEL_CMDLINE[default]+=" console=tty0"' | sudo tee -a /etc/limine-entry-tool.d/omarchy-defaults.conf
omarchy refresh limine
```

Both #11337 and #11011 verified that on their own machines.

## Report it

VM reports get closed as environment problems unless you make the environment legible. Run `omarchy debug`, upload the log, and put these in the issue:

- hypervisor and exact version, plus host OS
- firmware mode, UEFI or BIOS, and whether Secure Boot is off
- the virtual GPU, its PCI id from `lspci -nn`, the bound kernel driver, and whether 3D acceleration is on
- `cat /proc/cmdline`, which is where the QEMU serial console parameter shows up even though it is in no file on disk
- which guest tools you installed, if any

`omarchy debug --no-sudo` skips the dmesg capture if you would rather not share it. Details on [omarchy debug](/reference/commands/omarchy-debug/).

Check first whether your case is already one of the issues in the table above. A "me too" with a new hypervisor version on #8113 is worth more than a fresh duplicate.

## Related

- [Run Omarchy in VMware Workstation or Fusion](/run/vmware-workstation-fusion/)
- [Run Omarchy in VirtualBox](/run/virtualbox/)
- [Run Omarchy in Proxmox, QEMU or KVM](/run/proxmox-qemu-kvm/)
- [Run Omarchy in UTM on Apple Silicon](/run/utm-apple-silicon/)
- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Unattended installs with cidata](/run/unattended-install-cidata/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Black screen after login](/fix/black-screen-after-login/)
- [Limine and boot](/hardware/boot-limine/)
