---
title: "Omarchy 4 in Proxmox, QEMU/KVM and virt-manager"
description: "Running Omarchy 4 as a QEMU/KVM guest under Proxmox or virt-manager: OVMF firmware, q35, virtio disk and display, guest agents, and the verified bugs."
answer: "Give the VM UEFI firmware (OVMF), a q35 machine, host CPU passthrough, a virtio disk and NIC, and a virtio display rather than QXL. After install, add a Limine drop-in with console=tty0 so the themed LUKS prompt comes back, set omarchy_gdk_scale and omarchy_monitor_scale to 1 in monitors.lua, and install qemu-guest-agent yourself."
appliesTo:
  from: "4.0.0"
  to: "4.0.4"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
platform: "Proxmox, QEMU/KVM, virt-manager"
hostVersion: "Proxmox VE 9.2, QEMU 10.x (pc-q35-10.2), libvirt and virt-manager"
tags: [proxmox, qemu, kvm, virt-manager, virtio, vm]
sources:
  - url: "https://omarchy.org/manual/unattended-installs/"
    title: "Omarchy manual: Unattended Installs"
    kind: manual
  - url: "https://omarchy.org/manual/omarchy-on/"
    title: "Omarchy manual: Omarchy on..."
    kind: manual
  - url: "https://omarchy.org/manual/monitors/"
    title: "Omarchy manual: Monitors"
    kind: manual
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
  - url: "https://github.com/omacom/omarchy/issues/8554"
    title: "Issue #8554: 120 FPS ttfx screensaver triggers QXL TTM failures and freezes the session"
    kind: issue
    author: "howdeploy"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/2513"
    title: "Issue #2513: QEMU Display Scaling Issue"
    kind: issue
    author: "rami-shalhoub"
    date: "2025-10-17"
  - url: "https://github.com/omacom/omarchy/issues/10620"
    title: "Issue #10620: VMware guest: installer leaves the system without open-vm-tools (live ISO has them); plus working fix for the 3D-acceleration grey screen (#8113)"
    kind: issue
    author: "kevincasier"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/8834"
    title: "Issue #8834: Bar centre section is unclickable with an absolute pointing device; relative mouse mode fixes it"
    kind: issue
    author: "novastate"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/10282"
    title: "Issue #10282: Sunshine error 503 on hosts with no physical input (VM / GPU passthrough): idle screensaver blanks the display and KMS capture can never start"
    kind: issue
    author: "jimdawdy-hub"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/1930"
    title: "Issue #1930: unusably slow in QEMU"
    kind: issue
    author: "tcurdt"
    date: "2025-09-25"
  - url: "https://github.com/omacom/omarchy/issues/4208"
    title: "Issue #4208: Boot fails on first boot with Libreboot/Coreboot (no EFI payload) - installer should detect non-EFI and offer legacy/BIOS install"
    kind: issue
    author: "Somnius"
    date: "2026-01-10"
  - url: "https://github.com/omacom/omarchy/discussions/4352"
    title: "Discussion #4352: vm-curator: a TUI alternative to virt-manager with working NVIDIA 3D para-virtualization!"
    kind: discussion
    author: "mroboff"
    date: "2026-01-25"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Release v4.0.4"
    kind: release
    date: "2026-09-15"
  - url: "https://pve.proxmox.com/pve-docs/qm.1.html"
    title: "Proxmox VE qm(1) manual page"
    kind: docs
credits:
  - name: "JasonStreifling"
    url: "https://github.com/JasonStreifling"
    for: "Tracing the unthemed LUKS prompt under QEMU to systemd-stub appending a serial console= to the UKI command line"
  - name: "romixlab"
    url: "https://github.com/romixlab"
    for: "Finding empirically that a console=tty0 drop-in restored the graphical password prompt on a Proxmox guest"
  - name: "howdeploy"
    url: "https://github.com/howdeploy"
    for: "Isolating the 120 FPS screensaver as the trigger for QXL TTM buffer eviction failures on a SPICE guest"
  - name: "kevincasier"
    url: "https://github.com/kevincasier"
    for: "Pointing out that the installer skips guest tooling and that the default 2x GDK scale is wrong on small virtual displays"
faq:
  - q: "Can I install Omarchy on a VM with SeaBIOS or legacy BIOS?"
    a: "Treat it as unsupported. Omarchy installs a UKI and Limine onto an EFI system partition, and issue #4208 reported an install that finished but would not boot on firmware with no EFI services. DHH replied there that the team has nobody on that setup and would take a patch, but none has shipped as of 4.0.4. Use OVMF."
  - q: "Should I use virtio, QXL or Standard VGA for the display?"
    a: "Use virtio. QXL is the one display path with a confirmed Omarchy bug: issue #8554 records the stock 120 FPS screensaver driving a QXL guest into repeated TTM buffer eviction failures until the session had to be killed."
  - q: "Does the shared clipboard work over SPICE?"
    a: "Not through spice-vdagent. Issue #2513 is a virt-manager user who installed spice-vdagent and qemu-guest-agent and still had no shared clipboard and could not get a usable screen size. spice-vdagent's clipboard integration talks to an X server, and Omarchy 4 runs Hyprland on Wayland."
  - q: "Can I run the Omarchy Windows VM inside an Omarchy guest?"
    a: "Only if the host enables nested virtualization. omarchy-windows-vm checks for /dev/kvm and refuses to continue when it is missing, so the guest needs a CPU model that exposes VMX or SVM."
related: [virtualbox, vmware-workstation-fusion, unattended-install-cidata, what-breaks-in-a-vm]
draft: false
---

Omarchy 4 boots a unified kernel image through Limine on an EFI system partition, and runs Hyprland on Wayland with a Quickshell bar on top. Three host decisions follow from that, and almost every VM problem on this page traces back to getting one of them wrong: the firmware must be UEFI, the display device must be one the DRM stack can drive without an X11 helper, and the guest has to be told it is not on a retina laptop.

Checked against the Omarchy 4.0.4 source (released 2026-09-15) and the reports linked below, which come from 4.0.1 through 4.0.3 guests. Nothing they hinge on changed in 4.0.4: the screensaver still runs at 120 FPS, `monitors.lua` still ships a 2x GDK scale, and the default kernel command line still carries no `console=` parameter. The manual's own [Omarchy on...](https://omarchy.org/manual/omarchy-on/) chapter covers Parallels, VirtualBox and VMware and says nothing about QEMU, Proxmox or virt-manager, which is the gap this page fills. On 3.x the same host settings applied, but the config edits below went into `~/.config/hypr/*.conf`, not the Lua files that 4.0 moved to.

## Host settings that matter

| Setting | Use | Why |
|---|---|---|
| Firmware | OVMF / UEFI | The installer writes a UKI and Limine to an ESP. See #4208. |
| Machine | q35 | Modern chipset with proper PCIe. The manual's Proxmox recipe uses it. |
| CPU | `host` / host-passthrough | Needed for sane performance, and for nested KVM if you want the Windows VM. |
| Disk | virtio-scsi or virtio-blk | Anything emulated is slow. |
| NIC | virtio | Same reason. |
| Display | virtio-gpu | QXL has a confirmed freeze, see #8554. |
| Memory | 8 GB and up | The manual's recipe and the working `virt-install` posted in #1930 both use 8192 MB. The "unusably slow" report that opened #1930 was x86 emulation under UTM on an M1 with 4 GB, so read it as a warning about emulation, not a RAM figure. |
| Secure Boot | off | The manual's getting-started chapter says to turn Secure Boot and/or TPM off. |

### Proxmox

The Omarchy manual ships its own `qm create` recipe in the [unattended installs chapter](https://omarchy.org/manual/unattended-installs/). Trimmed to the parts that matter for an interactive install:

```bash
qm create 101 --name omarchy \
  --bios ovmf --machine q35 --cpu host --cores 4 --memory 8192 \
  --ostype l26 --scsihw virtio-scsi-single \
  --efidisk0 local-lvm:0,efitype=4m,pre-enrolled-keys=0 \
  --scsi0 local-lvm:60,discard=on,iothread=1 \
  --net0 virtio,bridge=vmbr0 --vga virtio \
  --ide2 local:iso/omarchy.iso,media=cdrom \
  --boot order='scsi0;ide2'
```

`pre-enrolled-keys=0` is what keeps Secure Boot out of the way. Putting `scsi0` ahead of `ide2` in the boot order is deliberate: a blank disk cannot boot, so the first start lands on the ISO, and every start after the install goes straight to disk. The manual's full recipe also attaches a serial socket, which is the kind of port that let romixlab see boot text behind a black screen in #11011.

The `vga` option also takes a `memory` integer, per the [qm manual page](https://pve.proxmox.com/pve-docs/qm.1.html). That is the knob to raise if the virtual display will not offer the resolution you want.

### virt-manager and virt-install

Adapted from the `virt-install` command herboh posted in #1930 (a Zen 3 host, 8 GB, four vCPUs, performance reported as fine), with their GPU passthrough, audio and SPICE channel devices removed:

```bash
virt-install --name omarchy \
  --boot uefi --machine q35 --cpu host-passthrough \
  --vcpus 4 --memory 8192 \
  --disk size=60,bus=virtio,discard=unmap \
  --network bridge=virbr0,model=virtio \
  --video virtio --graphics spice \
  --osinfo archlinux \
  --cdrom /path/to/omarchy.iso
```

In the virt-manager GUI the equivalents are Overview > Firmware set to a UEFI x86_64 OVMF entry, Video set to Virtio, and Display Spice with OpenGL ticked (which requires listen type None, so the console only works on the local machine).

### GNOME Boxes

Boxes gives you no firmware, video or CPU controls. If a Boxes guest will not boot the installed system, edit the domain directly with `virsh --connect qemu:///session edit <name>` or rebuild it in virt-manager. The only Boxes report in the Omarchy tracker is a comment on #2513 from mjpowersjr, who hit the tiny-display problem covered below and could barely read the installer text. Nobody has filed a Boxes boot failure, so treat the `virsh` advice as generic libvirt advice rather than a tested path.

## Verify it worked

From a terminal in the guest:

```bash
systemd-detect-virt          # kvm
hyprctl monitors             # the virtual output, its mode and its scale
lspci -k | grep -A3 -i vga   # expect virtio-pci and the virtio_gpu driver
cat /proc/cmdline            # see the serial console note below
```

## Fixes you will want on a fresh guest

### The LUKS prompt is plain text, or the screen goes black

Omarchy boots as a UKI (`ENABLE_UKI=yes` in `/etc/limine-entry-tool.d/omarchy-uki.conf`), so systemd-stub gets a say before the kernel does. The stub inspects the firmware's console output devices, and OVMF under QEMU lists the emulated serial port among them. If the built-in command line has no `console=` of its own, the stub adds `console=uart,io,0x3f8 console=tty0`. Plymouth spots the serial console, drops every display into detailed text mode, and the themed passphrase prompt never appears. JasonStreifling worked this out in issue #11337. The tell is that those parameters are in `/proc/cmdline` but absent from `/boot/limine.conf`, the drop-in directory and the UKI itself, because they are added at boot. romixlab had already stumbled on the cure on a Proxmox guest in #11011, with `plymouth.enable=0` thrown in as well; the follow-up there points out that the `console=tty0` half is the part doing the work.

Claim the parameter yourself with a drop-in, following the same pattern Omarchy uses for its own hardware quirks:

```bash
sudo mkdir -p /etc/limine-entry-tool.d
cat <<'EOF' | sudo tee /etc/limine-entry-tool.d/qemu-serial-console.conf
KERNEL_CMDLINE[default]+=" console=tty0"
EOF
sudo limine-update
```

Use a new file rather than editing `/etc/limine-entry-tool.d/omarchy-defaults.conf`, which Omarchy owns. `omarchy refresh limine` also rebuilds the boot entries, but it resets `/boot/limine.conf` from the shipped default first, so reach for `limine-update` when you only want to regenerate.

If you want boot messages to keep flowing to the serial port, #11337 lists `plymouth.ignore-serial-consoles` as an alternative that makes Plymouth disregard the serial console instead of suppressing it. The report names it but did not verify it, and neither has this page.

### Everything is twice the size it should be

`~/.config/hypr/monitors.lua` ships with `omarchy_gdk_scale = 2` and `omarchy_monitor_scale = "auto"`, because Omarchy assumes a 218 PPI or better panel. On a 1280x800 or 1920x1080 virtual display that gives you a tiny desktop full of enormous GTK windows. kevincasier raised exactly this in #10620 from a VMware guest at 1280x800, and the shipped default is identical under QEMU; they suggested VM detection should default to 1x. Until that happens, open _Setup > Monitors_ and set both to 1:

```lua
local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1
```

`Super + /` and `Super + Alt + /` step the focused monitor through 1x, 1.25x, 1.6x, 2x, 3x and 4x if you want to try values first. GDK_SCALE only applies to applications started after the change.

If the resolution list itself is wrong, pin a mode instead of fighting the scale. Run `hyprctl monitors all` to see what the virtual output actually offers, then add an `hl.monitor` line in the same file. Note that rami-shalhoub in #2513 reported that adding `video=` to the kernel command line changed nothing on a virt-manager guest, so do not spend time on that route.

### No guest agent, no clipboard, no auto-resize

The Omarchy package lists in 4.0.4 contain no `qemu-guest-agent` and no `spice-vdagent`, so the installed system has neither. Add the agent if you want graceful shutdown and IP reporting from the host:

```bash
omarchy pkg add qemu-guest-agent
sudo systemctl enable --now qemu-guest-agent
```

Do not expect `spice-vdagent` to buy you a shared clipboard. Its clipboard integration talks to an X server, Hyprland is not one, and issue #2513 is a user who installed both packages on a virt-manager guest and still had no shared clipboard and no usable screen size. Proxmox also exposes a `clipboard=vnc` sub-option on `vga`, which is a separate mechanism from the SPICE agent.

### Do not pick QXL

On a SPICE guest with the Red Hat QXL device, howdeploy recorded in #8554 that the stock terminal screensaver (which runs `ttfx` at a hard-coded 120 FPS) drove the kernel into repeated QXL and TTM buffer eviction failures about 48 seconds after it started, froze the display and input, and could only be recovered by stopping the session. Disabling the screensaver with `omarchy toggle screensaver` avoided it across a following boot of more than an hour. Their follow-up on the same issue ran a patched screensaver at 20 and 30 FPS for 20 minutes each with zero eviction failures, so a lower frame rate is a mitigation if a frame-rate setting ever ships, but as of 4.0.4 `omarchy-screensaver` still hard-codes `--frame-rate 120`. The cleanest answer is to use virtio-gpu instead.

### Clicks on the middle of the bar do nothing

novastate reported in #8834 that every clickable widget in the bar's centre section stops responding when the pointer is an absolute device, while the left and right sections keep working. Their guest was a KVM machine driven over Sunshine, with `qemu-qemu-usb-tablet` among the devices Hyprland saw, and switching the client to relative mouse mode fixed it immediately. QEMU and Proxmox consoles normally attach a USB tablet, so if the clock will not open a calendar for you, this is the likely cause. The report is open and the mechanism is not proven. Nobody has confirmed it on a plain SPICE or noVNC console yet, so treat it as a lead rather than a diagnosis.

## GPU passthrough

Passthrough works, with caveats that are worth knowing before you start.

romixlab installed 4.0.2 on Proxmox 9.2.2 with an AMD Radeon Pro W6600 passed through and got either a black screen or a crashing plymouthd (#11011). A serial port revealed that boot was actually fine behind the blank display, and the `console=tty0` drop-in above restored a graphical prompt. On 2026-09-16 they added that a reinstall worked with no changes at all, and guessed that leaving the q35 machine version at the latest (9.2) rather than 5.1 was the difference. That is a guess rather than a bisect, but a current machine version costs nothing, and the issue was closed on that note.

If you are building a headless streaming host, read #10282 first. A guest with no keyboard or mouse attached never produces input, so the idle timer fires on schedule, the display goes dark, and Sunshine's `capture = kms` backend has nothing to capture and fails with error 503. jimdawdy-hub's workaround is `omarchy-toggle-idle stay-awake` (undo with `omarchy-toggle-idle allow-idle`), at the price of losing the auto-lock and screensaver on that box. The issue is open.

For NVIDIA cards without passthrough, mroboff's `vm-curator` (discussion #4352) is a Rust TUI that drives QEMU directly, written because the author found NVIDIA 3D paravirtualisation broken through libvirt but working through QEMU's `virtio-vga-gl`. It is third-party and unaffiliated, and the discussion carries the author's own caveat that it is not suitable for Windows gaming.

## Unattended installs

Omarchy's ISO installs itself when it finds a second drive labelled `cidata` with the wizard's own configuration files on it, which makes Proxmox a natural fit for disposable dev boxes. The whole flow, including the `genisoimage` command and the caveat that an encrypted install still needs someone to type the passphrase once, is on [our cidata page](/run/unattended-install-cidata/) and in the manual's [unattended installs chapter](https://omarchy.org/manual/unattended-installs/).

## What to watch for on newer versions

Two things on this page are open upstream and could change under you in the next release: the serial console drop-in becomes unnecessary if Omarchy ships any `console=` parameter in its defaults, and the 2x GDK scale could gain the VM detection #10620 asks for. Re-read `~/.config/hypr/monitors.lua` and `cat /proc/cmdline` after a major upgrade before assuming your workarounds are still needed. Note also that the [Try Omarchy](https://omarchy.org) builds on omarchy.org target Apple Silicon Macs and Windows 10 and 11 only; in the site's own words, on Linux the ISO is the way in.

## Related

- [Run Omarchy in VirtualBox](/run/virtualbox/)
- [Run Omarchy in VMware Workstation or Fusion](/run/vmware-workstation-fusion/)
- [Unattended installs with cidata](/run/unattended-install-cidata/)
- [What breaks in a VM](/run/what-breaks-in-a-vm/)
