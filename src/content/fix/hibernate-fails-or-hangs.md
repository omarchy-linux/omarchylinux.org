---
title: "Hibernate fails or hangs on Omarchy"
description: "Hibernate writes the image but never resumes, or hangs before power-off. Check the Btrfs swapfile offset, NVIDIA early KMS, and HibernateMode on Omarchy 4."
answer: "Run omarchy hibernation setup, then check the two things it does not verify. Compare resume_offset in /etc/limine-entry-tool.d/resume.conf against btrfs inspect-internal map-swapfile -r /swap/swapfile and fix any mismatch. On NVIDIA, move /etc/mkinitcpio.conf.d/nvidia.conf aside so the driver is not loaded in the initramfs where the resume hook runs. Rebuild with sudo limine-mkinitcpio and reboot. If the machine never powers off, set HibernateMode=shutdown."
appliesTo:
  from: "3.x"
status: workaround
category: other
issueCount: 123
errorStrings:
  - "Call to Hibernate failed: Not enough suitable swap space for hibernation available on compatible block devices and file systems"
  - "Call to Hibernate failed: Specified resume device is missing or is not an active swap device"
  - "PM: hibernation: Failed to load image, recovering."
  - "PM: hibernation: resume failed (-5)"
  - "nv_pmops_freeze [nvidia] returns -5"
  - "PM: Image not found (code -22)"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [hibernate, swapfile, btrfs, limine, resume, nvidia]
sources:
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy-iso/blob/quattro/configs/airootfs/usr/share/omarchy-iso/orchestrator/phases_impl.py"
    title: "omarchy-iso orchestrator: configure_hibernation runs omarchy-hibernation-setup --force --no-rebuild during install"
    kind: code
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/105"
    title: "Issue #105: Add support for hibernate"
    kind: issue
    author: "dhh"
    date: "2025-07-09"
  - url: "https://github.com/omacom/omarchy/issues/8471"
    title: "Issue #8471: omarchy-hibernation-setup's HOOKS+=(resume) can never place resume before `filesystems`"
    kind: issue
    author: "manuelbecker123"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/10375"
    title: "Issue #10375: omarchy-hibernation-setup appends resume hook after filesystems, breaking resume"
    kind: issue
    author: "jorgenfoss"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/11437"
    title: "Issue #11437: omarchy-hibernation-setup never reconciles a stale resume_offset"
    kind: issue
    author: "adevwithpurpose"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/10037"
    title: "Issue #10037: omarchy hibernation remove leaves /etc/limine-entry-tool.d/resume.conf behind"
    kind: issue
    author: "brenodyego"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/7730"
    title: "Issue #7730: omarchy-hibernation-available returns success when the kernel has hibernation disabled"
    kind: issue
    author: "mnemonicspace"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/5554"
    title: "Issue #5554: Hibernation with Nvidia GPU Issues"
    kind: issue
    author: "ryanrhughes"
    date: "2026-05-02"
  - url: "https://github.com/omacom/omarchy/issues/10039"
    title: "Issue #10039: Hibernate resume fails (nv_pmops_freeze to -EIO) on single-NVIDIA-GPU desktops"
    kind: issue
    author: "unconnect"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/issues/8589"
    title: "Issue #8589: Hibernation aborts during image creation on ASUS ROG Zephyrus G14 (GA403UV); HibernateMode=shutdown fixes it"
    kind: issue
    author: "wjax"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9696"
    title: "Issue #9696: Hibernate hangs (forced power-off required) on hybrid-GPU ASUS ROG G14"
    kind: issue
    author: "rdelpiano"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/7618"
    title: "Issue #7618: hibernation setup installs keyboard-backlight system-sleep hook non-executable"
    kind: issue
    author: "janne"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/pull/8588"
    title: "PR #8588: Install system-sleep hooks executable"
    kind: pr
    author: "wjax"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/5337"
    title: "Issue #5337: Hibernation won't work anyway"
    kind: issue
    author: "Underday"
    date: "2026-04-17"
  - url: "https://github.com/omacom/omarchy/discussions/5500"
    title: "Discussion #5500: Hibernation failure due to NVidia driver: How I fixed it"
    kind: discussion
    author: "NicolasDorier"
    date: "2026-04-30"
  - url: "https://github.com/omacom/omarchy/issues/4259"
    title: "Issue #4259: Hibernate Crash & systemd-coredump CPU Spike"
    kind: issue
    author: "virtualabishek"
    date: "2026-01-14"
  - url: "https://github.com/omacom/omarchy/issues/11127"
    title: "Issue #11127: Hibernation already setup for PCs"
    kind: issue
    author: "QwinkleTee"
    date: "2026-09-10"
credits:
  - name: "unconnect"
    url: "https://github.com/unconnect"
    for: "Isolated the initramfs NVIDIA load as the cause of nv_pmops_freeze returning -EIO on single-GPU desktops"
  - name: "jamielife"
    url: "https://github.com/jamielife"
    for: "First to confirm that disabling the early NVIDIA mkinitcpio drop-in restores resume on a desktop"
  - name: "hanshs"
    url: "https://github.com/hanshs"
    for: "Confirmed the same fix on a Blackwell dGPU-only desktop and showed why Plymouth still renders"
  - name: "diegomendi"
    url: "https://github.com/diegomendi"
    for: "Traced NVreg_PreserveVideoMemoryAllocations=1 to Arch's gpu-screen-recorder package overriding Omarchy's build"
  - name: "jorgenfoss"
    url: "https://github.com/jorgenfoss"
    for: "Fresh boot logs showing the =0 override fixing resume on nvidia-open-dkms, and the boot-ID test for a real resume"
  - name: "TechLuddite"
    url: "https://github.com/TechLuddite"
    for: "Showed from mkinitcpio's init and kernel logs that the resume hook still runs before root is mounted from last position"
  - name: "manuelbecker123"
    url: "https://github.com/manuelbecker123"
    for: "Documented the = versus += clash that puts the resume hook last in HOOKS"
  - name: "adevwithpurpose"
    url: "https://github.com/adevwithpurpose"
    for: "Showed that hibernation setup never reconciles a stale resume_offset"
  - name: "mnemonicspace"
    url: "https://github.com/mnemonicspace"
    for: "Found that a memfd_secret holder such as Bitwarden Desktop makes the kernel refuse hibernation"
  - name: "wjax"
    url: "https://github.com/wjax"
    for: "Found HibernateMode=shutdown fixes a silent image-creation abort on the Zephyrus G14"
  - name: "sspaeti"
    url: "https://github.com/sspaeti"
    for: "Documented the amdgpu cmdline combination that stopped post-hibernate crashes on a TUXEDO InfinityBook"
faq:
  - q: "Does Omarchy set up hibernation for me?"
    a: "Yes, on a fresh install. The Omarchy 4 ISO runs omarchy-hibernation-setup --force --no-rebuild from its configure_hibernation phase, and 3.x did the same from install/login/hibernation.sh. That is why #11127 found a 39 GB swapfile on a fresh 4.0.2 desktop. If you do not want it, run omarchy hibernation remove, then delete /etc/limine-entry-tool.d/resume.conf yourself and rebuild."
  - q: "How much disk does hibernation cost?"
    a: "A swapfile the size of your physical RAM, in a /swap Btrfs subvolume on the boot drive. 32 GB of RAM means a 32 GB file. On a small partition this can eat most of your free space."
  - q: "Why do I get asked for a password twice?"
    a: "The first prompt is LUKS in the initramfs, the second is the Omarchy lock screen after the session thaws. Both are expected on an encrypted install."
  - q: "Is suspend-then-hibernate set up by default?"
    a: "No. Omarchy dropped it as a default in 3.4.0 because it failed on several laptops. The menu offers plain Suspend and plain Hibernate."
related: [suspend-wont-resume-s2idle, nvidia-drivers-omarchy-4, hybrid-gpu-laptop-black-screen-aq-drm-devices, battery-drains-fast]
draft: false
---

Hibernate on Omarchy has two common failure shapes. Either the image is written and the machine powers down, but the next boot is a cold boot with your session gone, or the image is written and the machine never powers off at all. The steps below cover both. Everything here was checked against the v4.0.4 source tree and the v3.8.4 tree for comparison.

## The fix

Work through these in order. Steps 1 to 3 apply to every machine. Step 4 is NVIDIA only.

**1. Confirm the kernel will accept hibernation at all.**

```bash
cat /sys/power/state   # must contain "disk"
cat /sys/power/disk    # must not be "[disabled]"
swapon --show
```

`omarchy hibernation available` does not check `/sys/power/state`. It only looks for `/sys/power/image_size`, non-zram swap larger than the image size, and `/etc/mkinitcpio.conf.d/omarchy_resume.conf`. mnemonicspace showed in issue #7730 that all three can pass while `/sys/power/disk` reads `[disabled]`, which is why the Hibernate menu item can appear and then do nothing. In that thread the cause turned out to be Bitwarden Desktop holding a `memfd_secret` file, which the kernel treats as a hibernation blocker. Closing it, or launching it with `SECURE_KEY_CONTAINER_BACKEND=mlock`, brought `disk` back.

**2. Set hibernation up if it is not already there.**

```bash
omarchy hibernation setup
```

This needs Limine and Btrfs. It creates a `/swap` subvolume with a swapfile the size of your RAM, adds it to `/etc/fstab`, writes `HOOKS+=(resume)` to `/etc/mkinitcpio.conf.d/omarchy_resume.conf`, and writes `resume=` plus `resume_offset=` to `/etc/limine-entry-tool.d/resume.conf`. On 3.x the same values were also appended to `/etc/default/limine`. Omarchy 4 writes only the drop-in. If it prints `Hibernation is already set up`, it changed nothing, which matters for the next step.

**3. Check the resume offset actually matches the swapfile.**

```bash
sudo btrfs inspect-internal map-swapfile -r /swap/swapfile
cat /etc/limine-entry-tool.d/resume.conf
```

If the numbers differ, edit the drop-in. `omarchy hibernation setup` will not repair this for you. As adevwithpurpose showed in issue #11437, the script only writes the drop-in when the file is absent, and its repair branch matches an empty value, never a stale one. On 3.x, fix `/etc/default/limine` too.

Then rebuild:

```bash
sudo limine-mkinitcpio
sudo reboot
```

**4. On NVIDIA, take the driver out of the initramfs.**

```bash
sudo mv /etc/mkinitcpio.conf.d/nvidia.conf /etc/mkinitcpio.conf.d/nvidia.conf.disabled
sudo limine-mkinitcpio
sudo reboot
```

This is the change reported working on single-GPU desktops across Ampere, Ada and Blackwell in issues #5554 and #10039. NVIDIA still loads once the root filesystem is up and `nvidia-smi` still works. The cost is a plainer LUKS prompt on a single-GPU box, since Plymouth falls back to the firmware framebuffer. The installer writes this file from `install/hardware/nvidia.sh`, so re-check it after a reinstall or a major upgrade.

On a hybrid laptop there is a lighter option. The `-5` failure needs `NVreg_PreserveVideoMemoryAllocations=1`, and on Omarchy that value comes from `/usr/lib/modprobe.d/gsr-nvidia.conf`, installed by Arch's `gpu-screen-recorder` package. Appending `options nvidia NVreg_PreserveVideoMemoryAllocations=0` to `/etc/modprobe.d/nvidia.conf` sorts after it and wins. diegomendi and jorgenfoss both confirmed resume working with only that change, on a Radeon 680M plus RTX 4050 laptop in #5554 and an ASUS ProArt P16 in #10375.

## Verify it worked

Check the live cmdline first:

```bash
tr ' ' '\n' < /proc/cmdline | grep resume
```

Now hibernate with `systemctl hibernate`, power back on, and look at the boot list:

```bash
journalctl --list-boots | tail -3
```

A real resume keeps the same boot ID before and after, because the restored image is the old kernel instance. A failed resume shows up as a new boot. jorgenfoss pointed this out in #10375 as a cleaner test than grepping for strings. If you want the strings anyway:

```bash
journalctl -b -k | grep -E 'PM: |resume'
```

A good run shows `Image signature found`, `Image successfully loaded`, and `hibernation exit`. `PM: Image not found (code -22)` means the hook ran and found nothing at the offset, so go back to step 3. `Failed to load image, recovering` after a full load is the NVIDIA case. If the machine hung instead, the evidence is in the next boot's journal, not the failed one. Once userspace is frozen, journald has stopped writing.

## Why it happens

Hibernation on Omarchy stacks four fragile things. The swap is a file on Btrfs, so the kernel needs a physical block offset rather than a device, and that offset changes if the file is ever recreated. The root is LUKS, so the resume hook has to run after `encrypt`. The boot is a Limine UKI, so every cmdline change needs a rebuild. And zram sits at priority 100 above the disk swapfile at priority 0, sized to all of RAM since 4.0.0, which is correct but makes `swapon --show` confusing to read.

One thing that looks broken is not. `omarchy_hooks.conf` reassigns the whole array with `HOOKS=(...)` and `omarchy_resume.conf` only appends, so `resume` always lands last, after `filesystems`. manuelbecker123 documented the sort-order clash in issue #8471 and jorgenfoss reported it in #10375. But `filesystems` and `fsck` have no runtime hook, and mkinitcpio's init runs every `run_hook` before it mounts anything, so `resume` at the end is still the next hook after `encrypt`. TechLuddite showed this from a kernel log in #8471, and jorgenfoss's own failed boot in #10375 had the image fully loaded before NVIDIA aborted it. Reordering the hook is not the fix.

The NVIDIA case is separate and worse. Omarchy early-loads `nvidia`, `nvidia_modeset`, `nvidia_uvm` and `nvidia_drm` from the initramfs for early KMS at the LUKS prompt. The resume hook runs in that same initramfs, after the driver has bound to the card. With `NVreg_PreserveVideoMemoryAllocations` set to 1, the driver refuses a freeze that did not come through its own suspend path, so `nv_pmops_freeze` returns `-EIO` and the kernel discards the restore. unconnect laid this out in issue #10039. Issue #5554 is the tracking issue and it is still open.

## If that did not work

**Image written, machine never powers off.** wjax found in issue #8589 that the kernel can abort silently during image creation on an s2idle-only machine. Create `/etc/systemd/sleep.conf.d/hibernate-mode.conf` containing a `[Sleep]` section with `HibernateMode=shutdown`.

**Hybrid ASUS ROG.** Omarchy ships a `force-igpu` sleep hook that detaches the dGPU through supergfxctl before hibernate, but rdelpiano showed in issue #9696 that neither the hook nor supergfxctl is installed unless you have run `omarchy toggle hybrid gpu`. Run it. On 4.0.0 to 4.0.2 the toggle copied the hook without the executable bit, per PR #8588, so also check that `stat -c %A /usr/lib/systemd/system-sleep/force-igpu` starts with `-rwx`.

**NVIDIA desktop still cold-boots after step 4.** hanshs got a Blackwell 5070 Ti desktop resuming in #5554 with the drop-in disabled plus `nvidia-suspend.service`, `nvidia-hibernate.service` and `nvidia-resume.service` enabled. A different symptom, the image written and restored but the machine never powering off, is the NVIDIA `.shutdown` hang that tzalkind and asmyshlyaev177 reported in the same thread. No module parameter avoids it.

**AMD crashes after resume.** sspaeti reported in issue #4259 that adding `amdgpu.gpu_recovery=1` and `amdgpu.noretry=0` to the kernel cmdline, later with `amdgpu.ip_block_mask=0xfffff7ff` and `amdgpu.cwsr_enable=0`, ended the post-hibernate crashes on a TUXEDO InfinityBook Pro 14. That was on 3.x, where the cmdline lived in `/etc/default/limine`. On 4.x put it in a `/etc/limine-entry-tool.d/` drop-in instead.

**You removed hibernation and boot got worse.** `omarchy hibernation remove` deletes the swapfile and the mkinitcpio hook but leaves `/etc/limine-entry-tool.d/resume.conf` in place, so the rebuilt UKI still carries `resume=` pointing at blocks that no longer hold a swapfile. brenodyego reported this in issue #10037. Delete the drop-in yourself, then run `sudo limine-mkinitcpio`.

**Nothing changed on 4.0.0 to 4.0.2.** The keyboard backlight sleep hook was installed non-executable on those releases, so it never ran. janne reported it in issue #7618 and 4.0.3 replaced the `cp -p` with a mode 0755 install. The visible impact is limited to ASUS keyboards blocking S4.

## Related

- The [System sleep](https://omarchy.org/manual/system-sleep/) chapter of the Omarchy manual
- [Suspend will not resume from s2idle](/fix/suspend-wont-resume-s2idle/)
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Hybrid GPU laptop black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [Suspend and sleep hardware notes](/hardware/suspend-sleep/)
- [omarchy-hibernation-setup](/reference/commands/omarchy-hibernation-setup/)
