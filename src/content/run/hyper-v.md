---
title: "Run Omarchy in Hyper-V on Windows 11"
description: "Omarchy in Hyper-V: Generation 2 VM with Secure Boot off, fixed resolution via Set-VMVideo, the invisible LUKS prompt, and why there is no audio or GPU."
answer: "Create a Generation 2 VM, turn Secure Boot off, give it 4 vCPU, 8 GB RAM and a 64 GB VHDX, then set the guest resolution from the host with Set-VMVideo while the VM is off. Expect no sound, no enhanced session, no clipboard sharing and software rendering. For a GPU accelerated desktop on Windows, use Try Omarchy for Windows instead, which runs QEMU on WHPX rather than as a Hyper-V guest."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Hyper-V"
hostVersion: "Windows 11 Pro 24H2"
tags: [hyper-v, windows, virtual-machine, whpx, gpu]
sources:
  - url: "https://github.com/omacom/omarchy/discussions/445"
    title: "Discussion #445: Guide - Omarchy on Hyper-V"
    kind: discussion
    author: "max-pv"
    date: "2025-08-01"
  - url: "https://github.com/omacom/omarchy/discussions/1580"
    title: "Discussion #1580: Hyper-V install script"
    kind: discussion
    author: "axelfontaine"
    date: "2025-09-09"
  - url: "https://github.com/omacom/omarchy/issues/1397"
    title: "Issue #1397: No audio in Hyper-V"
    kind: issue
    author: "axelfontaine"
    date: "2025-09-01"
  - url: "https://github.com/omacom/omarchy/issues/1752"
    title: "Issue #1752: Black screen after post-installation reboot with Hyper-V"
    kind: issue
    author: "axelfontaine"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/discussions/6301"
    title: "Discussion #6301: Add VM Guides"
    kind: discussion
    author: "ryanrhughes"
    date: "2025-10-06"
  - url: "https://github.com/Chainfire/omarchy-windows-hyperv-gpu"
    title: "Chainfire/omarchy-windows-hyperv-gpu: Omarchy in a QEMU VM on Windows-on-Hyper-V with GPU acceleration"
    kind: other
    author: "Chainfire"
    date: "2026-08-23"
  - url: "https://github.com/omacom/try-omarchy-windows"
    title: "omacom/try-omarchy-windows: Use Omarchy Linux on Windows without any hassle."
    kind: other
    author: "omacom"
    date: "2026-08-28"
  - url: "https://github.com/omacom/try-omarchy-windows/issues/19"
    title: "Issue #19: Can start the app (WHPX: Failed to enable nested virtualization)"
    kind: issue
    author: "joce"
    date: "2026-08-30"
  - url: "https://github.com/omacom/try-omarchy-windows/issues/77"
    title: "Issue #77: Road to v1.0"
    kind: issue
    author: "btsouth"
    date: "2026-09-05"
  - url: "https://github.com/omacom/try-omarchy-windows/blob/master/docs/FINDINGS.md"
    title: "try-omarchy-windows docs/FINDINGS.md: nested virtualization refusal and the kernel-irqchip fallback"
    kind: docs
    author: "omacom"
  - url: "https://wiki.archlinux.org/title/Hyper-V"
    title: "ArchWiki: Hyper-V (enhanced session mode, xrdp, hv_sock, setting resolution)"
    kind: docs
  - url: "https://x.com/dhh/status/2097236884531351700"
    title: "DHH: next version of Omarchy is going to be Quattro RS 4.5"
    kind: blog
    author: "dhh"
  - url: "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/gpu-partitioning"
    title: "Partition and share GPUs with virtual machines on Hyper-V"
    kind: docs
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "The Omarchy Manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/getting-started/"
    title: "The Omarchy Manual: Getting Started"
    kind: manual
credits:
  - name: "max-pv"
    url: "https://github.com/max-pv"
    for: "the original Hyper-V guide and the Set-VMVideo resolution trick"
  - name: "axelfontaine"
    url: "https://github.com/axelfontaine"
    for: "the PowerShell script that builds the whole VM, and reporting the audio and black screen problems"
  - name: "hellsinger-cyber"
    url: "https://github.com/hellsinger-cyber"
    for: "identifying the invisible boot stall as the LUKS passphrase prompt on Omarchy 4.0.3"
  - name: "Chainfire"
    url: "https://github.com/Chainfire"
    for: "the QEMU on WHPX approach that gets GPU acceleration on a Hyper-V host"
faq:
  - q: "Do I need Windows 11 Pro to run Omarchy in Hyper-V?"
    a: "For the Hyper-V role, yes. Hyper-V ships on Pro, Education and Enterprise, not on Home, as max-pv noted in the original guide. The Windows Hypervisor Platform used by Try Omarchy for Windows does run on Home, so that path has no edition requirement."
  - q: "Why is there no sound in my Hyper-V Omarchy VM?"
    a: "Nobody has found a sound path for a Linux guest outside enhanced session mode, which the Arch Wiki documents as xrdp over hv_sock, started from an .xinitrc, so an X11 path. Omarchy runs Hyprland on Wayland and ships no xrdp, and the AUR package for it failed to install. Issue #1397 was closed without a fix."
  - q: "Can I use GPU partitioning to accelerate Omarchy?"
    a: "No. Microsoft's supported guest list for GPU-P is Windows 10 or later, Windows Server 2019 or later, and Ubuntu 18.04, 20.04 and 22.04 LTS, on datacenter GPUs. Arch is not on that list and neither is a consumer GeForce or Radeon card."
  - q: "My VM boots to a black screen after install. Is it broken?"
    a: "Usually not. Omarchy encrypts the root filesystem with LUKS, and the passphrase prompt can be invisible on the Hyper-V synthetic display. Click into the console window and type the passphrase blind, then press Enter."
related: [virtualbox, vmware-workstation-fusion, wsl2, what-breaks-in-a-vm]
draft: false
---

Hyper-V will run Omarchy, and by max-pv's account it runs more smoothly there than in VirtualBox. It will not give you a GPU, sound, a shared clipboard or a window that resizes. Decide on that basis. If you want a desktop that feels like the real thing on a Windows box, skip the Hyper-V guest entirely and use [Try Omarchy for Windows](https://github.com/omacom/try-omarchy-windows), which runs QEMU on the Windows Hypervisor Platform beside Hyper-V rather than inside it. Everything below was checked against the Omarchy 4.0.4 source tree (2026-09-15) and the community reports linked in the sources. The host details come from those reports, not from a run of my own.

One edition note first. The Hyper-V role is only on Windows Pro, Education and Enterprise, which max-pv called out when he wrote the community guide in [discussion #445](https://github.com/omacom/omarchy/discussions/445). The Windows Hypervisor Platform that Try Omarchy uses is the layer WSL2 already depends on, and that works on Home too.

## Build the VM

Omarchy needs a Generation 2 VM with Secure Boot turned off. The [Getting Started](https://omarchy.org/manual/getting-started/) chapter of the official manual is blunt about it: you must turn off Secure Boot and/or TPM to install Omarchy, and it describes those as Microsoft schemes meant for Windows and Microsoft-affiliated distributions. A Generation 2 VM has Secure Boot on by default, and the alternative Microsoft UEFI Certificate Authority template exists for those affiliated distributions. Nobody on the Omarchy threads reports the ISO booting under it, and axelfontaine's script simply disables Secure Boot with a comment that unsigned Linux ISOs need it off. Do the same and move on.

Run this in an elevated PowerShell. It is a trimmed version of the script axelfontaine posted in [discussion #1580](https://github.com/omacom/omarchy/discussions/1580), with the ISO download left to you. Get the ISO from [omarchy.org](https://omarchy.org) and check it against the [verification page](/verify/) first.

```powershell
$vmName  = "Omarchy"
$vmPath  = "C:\VMs"
$vhdPath = "$vmPath\$vmName.vhdx"
$isoPath = "$vmPath\$vmName.iso"

New-VM -Name $vmName -MemoryStartupBytes 8GB -Generation 2 -Path $vmPath
Set-VMProcessor -VMName $vmName -Count 4
New-VHD -Path $vhdPath -SizeBytes 64GB -Dynamic
Add-VMHardDiskDrive -VMName $vmName -Path $vhdPath
Add-VMDvdDrive -VMName $vmName -Path $isoPath

Set-VMFirmware -VMName $vmName -EnableSecureBoot Off
Connect-VMNetworkAdapter -VMName $vmName -SwitchName "Default Switch"
```

Two details that bite people. axelfontaine's original script enables dynamic memory sized to half the host; the trimmed version above skips that and gives the VM a fixed 8 GB, which is easier to reason about for a desktop guest. And after the install finishes, use Media then Eject in the console window before rebooting, or the VM boots the installer again. One commenter on the guide reported the opposite, that leaving the ISO attached was what finally worked, so if the first reboot fails, try the other order before assuming the install is broken.

## Set the resolution from the host

This is the part that surprises everyone. The guest cannot change its own resolution. The Hyper-V synthetic display is whatever the host says it is, and the default is 1024x768. Shut the VM down, then run:

```powershell
Set-VMVideo -VMName "Omarchy" -HorizontalResolution 2560 -VerticalResolution 1440 -ResolutionType Single
```

Boot it again and match the guest to it. On Omarchy 4.x that means `~/.config/hypr/monitors.lua`, reachable from the Omarchy menu under Setup then Monitors. The file ships with two values at the top, `omarchy_gdk_scale = 2` and `omarchy_monitor_scale = "auto"`, because Omarchy assumes a 2x retina-class display by default. That is wrong for almost any Hyper-V window. The [Monitors](https://omarchy.org/manual/monitors/) chapter's own recommendation for a 1080p or 1440p display is the sane starting point:

```lua
local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1
``` If you want to pin the synthetic output explicitly, the same file takes `hl.monitor` entries and the output is named `Virtual-1`.

Older copies of the community guide tell you to add `video=hyperv_fb:1920x1080` to `GRUB_CMDLINE_LINUX_DEFAULT` and run `grub-mkconfig`. Ignore that. The Arch Wiki notes the kernel parameter tops out at 1920x1080 anyway, and points at `Set-VMVideo` when it does not work. Omarchy has used Limine rather than GRUB for a long time, which a commenter flagged on the thread itself, and a later commenter reported on 3.2.2 that the host side `Set-VMVideo` call was all that was needed. They also tell you to edit `monitors.conf`, which stopped existing when 4.0.0 moved Hyprland config to Lua.

## The black screen that is not a crash

A very common report: the VM installs fine, then shows nothing after reboot. [Issue #1752](https://github.com/omacom/omarchy/issues/1752) is exactly this, filed against 3.0.1. The reporter typed the passphrase blind, closed the console window, reopened the VM from Hyper-V Manager, and the desktop was there. His own guess was an encryption screen display issue.

The clean explanation arrived on the guide thread in September 2026 from hellsinger-cyber, tested on Omarchy 4.0.3. Omarchy encrypts the root filesystem with LUKS2, and the boot sits in the initramfs at Plymouth's passphrase prompt, which the Hyper-V console does not always show, as #1752 found. Nothing has started yet, so the VM looks dead from the outside and is unreachable over the network. The giveaway is `systemd-analyze`, which attributes a minute or more to the kernel stage. Click into the console and type your passphrase blind.

If you want unattended boots, the same comment documents enrolling a TPM2 keyslot so the volume unlocks itself. That needs a vTPM on the VM, which you enable in the VM's Security settings while it is off, and a switch from the busybox `encrypt` initramfs hook to `sd-encrypt`, because the busybox hook has no TPM support. It also needs the kernel command line changed from Omarchy's `cryptdevice=` form to `rd.luks.name=`. That is real surgery on your boot path. Read the source comment before you start, keep the passphrase keyslot as a fallback, and take a snapshot first. Omarchy's own [snapshot](https://omarchy.org/manual/system-snapshots/) support is worth having in place before you touch the initramfs.

## Audio, clipboard and enhanced session

There is no sound, and there is no fix in the project. [Issue #1397](https://github.com/omacom/omarchy/issues/1397) asked for it in 2025 and was closed without one. Nobody on either thread found an audio path outside enhanced session mode, which is also where the integrated clipboard and a better display come from. The [Arch Wiki](https://wiki.archlinux.org/title/Hyper-V) documents that mode for Linux guests as xrdp plus the `hv_sock` kernel module, started from an `.xinitrc`, which is X11. Omarchy is Hyprland on Wayland and ships no xrdp, and the AUR package for enhanced session support failed to install for the person who tried it. A commenter on the install script thread reached the same conclusion from the Arch Wiki side.

Do not expect Omarchy to help here. Grep the 4.0.4 tree for Hyper-V and you get nothing, not even in the manual. There is no hypervisor detection, no guest tooling, no Hyper-V branch in the installer's hardware directory.

## GPU: partitioning will not save you

Microsoft's GPU partitioning documentation lists the supported guest operating systems as Windows 10 or later, Windows Server 2019 or later, and Ubuntu 18.04, 20.04 and 22.04 LTS, on datacenter cards such as the NVIDIA A10, L4 and L40S or the AMD Radeon PRO V710. Arch is not on that list, and a consumer GeForce or Radeon in a desktop is not either. Treat GPU-P as unavailable for Omarchy.

Two projects route around it by not being a Hyper-V guest at all:

- [Chainfire/omarchy-windows-hyperv-gpu](https://github.com/Chainfire/omarchy-windows-hyperv-gpu), published August 2026, runs Omarchy in QEMU on WHPX on a machine where Windows is already on Hyper-V, using a patched WINQ-EMU build for GPU rendering. Its README now points readers at the newer project below.
- [omacom/try-omarchy-windows](https://github.com/omacom/try-omarchy-windows), maintained in the same GitHub organisation as Omarchy itself, is a single launcher that downloads a prebuilt Arch plus Omarchy image and boots it with virgl and Venus Vulkan on your real GPU. The v0.0.19-preview release from 16 September 2026 carries Omarchy 4.0.3. It is still labelled preview, not v1.

If you keep the Hyper-V role enabled and try Try Omarchy, know about one specific failure. [Issue #19](https://github.com/omacom/try-omarchy-windows/issues/19) reported QEMU dying at startup with `WHPX: Failed to enable nested virtualization, hr=80370302` on a Core Ultra laptop. The project's [findings notes](https://github.com/omacom/try-omarchy-windows/blob/master/docs/FINDINGS.md) explain it: QEMU requests nested virtualization whenever the processor advertises it, and Meteor Lake laptops and hosts with the full Hyper-V feature set advertise it and then refuse. The fix shipped in v0.0.11-preview is two layers, a QEMU patch that downgrades the refusal to a warning and a launcher retry with `kernel-irqchip=off`, so current releases boot. Full Hyper-V host coverage is still an open item on the v1 checklist in [issue #77](https://github.com/omacom/try-omarchy-windows/issues/77), so this is the configuration most likely to surprise you.

## What to watch for on newer versions

The [Omarchy on...](https://omarchy.org/manual/omarchy-on/) manual chapter lists VirtualBox, VMware Workstation, Parallels, the Steam Deck, NixOS and Asahi as of 4.0.4. Hyper-V is not among them, and [discussion #6301](https://github.com/omacom/omarchy/discussions/6301) tracked the wider request for proper VM guides. Nothing in the tree detects Hyper-V, and nothing announced for the next release, which [DHH has said](https://x.com/dhh/status/2097236884531351700) will be called Quattro RS 4.5, mentions audio or enhanced session work. Assume the situation holds unless a release note says otherwise.

The bigger trap is age. Most Hyper-V write-ups for Omarchy were written against 3.x, and 4.0.0 replaced the whole shell and moved Hyprland config to Lua. Any instruction naming `monitors.conf`, `hyprland.conf` or GRUB is stale. See [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/) if you are converting an old snippet.

## Related

- [What breaks in a VM](/run/what-breaks-in-a-vm/)
- [Run Omarchy in VirtualBox](/run/virtualbox/)
- [Run Omarchy in VMware Workstation and Fusion](/run/vmware-workstation-fusion/)
- [Unattended install with cidata](/run/unattended-install-cidata/)
