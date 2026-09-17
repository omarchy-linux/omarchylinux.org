---
title: "Hibernate fails or hangs on Omarchy"
description: "Hibernate writes the image but never resumes, or hangs before power-off. Fix the resume hook order, the Btrfs swapfile offset, and NVIDIA early KMS on Omarchy 4."
answer: "Run omarchy hibernation setup, then fix the two things it gets wrong. Add a zz-sorted mkinitcpio drop-in that moves the resume hook before filesystems, and check resume_offset against btrfs inspect-internal map-swapfile -r /swap/swapfile. On NVIDIA, disable /etc/mkinitcpio.conf.d/nvidia.conf so the resume hook runs before the GPU driver binds. Rebuild with sudo limine-mkinitcpio."
appliesTo:
  from: "3.x"
status: workaround
category: other
issueCount: 88
errorStrings:
  - "Call to Hibernate failed: Not enough suitable swap space for hibernation available on compatible block devices and file systems"
  - "Call to Hibernate failed: Specified resume device is missing or is not an active swap device"
  - "PM: hibernation: Failed to load image, recovering."
  - "PM: hibernation: resume failed (-5)"
  - "nv_pmops_freeze [nvidia] returns -5"
  - "Failed to start System Hibernate."
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [hibernate, swapfile, btrfs, limine, resume, nvidia]
sources:
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
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
    author: "sspaeti"
    date: "2026-01-14"
credits:
  - name: "manuelbecker123"
    url: "https://github.com/manuelbecker123"
    for: "Traced the resume hook landing after filesystems to the = versus += clash between the two mkinitcpio drop-ins"
  - name: "jorgenfoss"
    url: "https://github.com/jorgenfoss"
    for: "Independent report of the same hook ordering defect with a working insert-before-filesystems snippet"
  - name: "unconnect"
    url: "https://github.com/unconnect"
    for: "Isolated the initramfs NVIDIA load as the cause of nv_pmops_freeze returning -EIO on single-GPU desktops"
  - name: "jamielife"
    url: "https://github.com/jamielife"
    for: "Confirmed that disabling the early NVIDIA mkinitcpio drop-in restores resume"
  - name: "adevwithpurpose"
    url: "https://github.com/adevwithpurpose"
    for: "Showed that hibernation setup never reconciles a stale resume_offset"
  - name: "wjax"
    url: "https://github.com/wjax"
    for: "Found HibernateMode=shutdown fixes a silent image-creation abort on the Zephyrus G14"
  - name: "sspaeti"
    url: "https://github.com/sspaeti"
    for: "Documented the AMD resume and amdgpu cmdline combination that stopped post-hibernate crashes"
faq:
  - q: "Does Omarchy set up hibernation for me?"
    a: "On 3.x it did. install/login/hibernation.sh ran omarchy-hibernation-setup --force during the install. That file is gone from the 4.0.4 tree, so on a fresh Omarchy 4 install you normally run omarchy hibernation setup yourself. Some users still report it already configured on 4.0.2, so check with swapon --show before assuming either way."
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

Work through these in order. Steps 1 to 4 apply to every machine. Step 5 is NVIDIA only.

**1. Confirm the kernel will accept hibernation at all.**

```bash
cat /sys/power/state   # must contain "disk"
cat /sys/power/disk    # must not be "[disabled]"
swapon --show
```

`omarchy hibernation available` does not check `/sys/power/state`. It only looks for `/sys/power/image_size`, non-zram swap larger than the image size, and `/etc/mkinitcpio.conf.d/omarchy_resume.conf`. mnemonicspace showed in issue #7730 that all three can pass while `/sys/power/disk` reads `[disabled]`, which is why the Hibernate menu item can appear and then do nothing.

**2. Set hibernation up if it is not already there.**

```bash
omarchy hibernation setup
```

This needs Limine and Btrfs. It creates a `/swap` subvolume with a swapfile the size of your RAM, adds it to `/etc/fstab`, writes `HOOKS+=(resume)` to `/etc/mkinitcpio.conf.d/omarchy_resume.conf`, and writes `resume=` plus `resume_offset=` to `/etc/limine-entry-tool.d/resume.conf`. On 3.x the same values were also appended to `/etc/default/limine`. Omarchy 4 writes only the drop-in.

**3. Move the resume hook before `filesystems`.**

This is the defect that breaks resume on machines with no GPU complications. `omarchy_hooks.conf` reassigns the whole array with `HOOKS=(...)`, and `omarchy_resume.conf` only appends, so `resume` always lands last, after root has already been mounted. manuelbecker123 documented the sort-order clash in issue #8471 and jorgenfoss reported the same thing independently in #10375.

Create `/etc/mkinitcpio.conf.d/zz-resume-position.conf` with sudo:

```sh
_h=()
for _hook in "${HOOKS[@]}"; do
  [[ $_hook == resume ]] && continue
  [[ $_hook == filesystems ]] && _h+=(resume)
  _h+=("$_hook")
done
HOOKS=("${_h[@]}")
unset _h _hook
```

The `zz-` prefix matters. The file has to sort after both `omarchy_hooks.conf` and `omarchy_resume.conf`.

**4. Check the resume offset actually matches the swapfile.**

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

**5. On NVIDIA, take the driver out of the initramfs.**

```bash
sudo mv /etc/mkinitcpio.conf.d/nvidia.conf /etc/mkinitcpio.conf.d/nvidia.conf.disabled
sudo limine-mkinitcpio
sudo reboot
```

You lose the graphical Plymouth LUKS prompt on a single-GPU box. NVIDIA still loads in userspace and `nvidia-smi` still works.

## Verify it worked

Before the test, check the hook order that mkinitcpio will actually build:

```bash
bash -c 'source /etc/mkinitcpio.conf
         for f in /etc/mkinitcpio.conf.d/*.conf; do source "$f"; done
         printf "%s\n" "${HOOKS[@]}" | nl'
```

`resume` should sit immediately before `filesystems`, and after `encrypt` on a LUKS install. Then check the live cmdline:

```bash
tr ' ' '\n' < /proc/cmdline | grep resume
```

Now hibernate. Use the unit rather than the menu action, because `systemctl hibernate` returns as soon as logind takes the request:

```bash
sudo systemctl start systemd-hibernate.service
```

Power back on and read the journal for the boot you just came back into:

```bash
journalctl -b | grep -i 'hibernation\|Image signature'
```

A good run shows the image signature found, the image successfully loaded, and `hibernation exit`. A failed restore shows `PM: hibernation: Failed to load image, recovering.` If the machine hung instead, the evidence is in the next boot's journal, not the failed one. Once userspace is frozen, journald has stopped writing.

## Why it happens

Hibernation on Omarchy stacks four fragile things. The swap is a file on Btrfs, so the kernel needs a physical block offset rather than a device, and that offset changes if the file is ever recreated. The root is LUKS, so the resume hook has to run after `encrypt` but before `filesystems`, and Omarchy's two mkinitcpio drop-ins cannot express that ordering between them. The boot is a Limine UKI, so every cmdline change needs a rebuild. And zram sits at priority 100 covering all of RAM since 4.0.0, above the disk swapfile at priority 0, which is correct but makes `swapon --show` confusing to read.

The NVIDIA case is separate and worse. Omarchy early-loads `nvidia`, `nvidia_modeset`, `nvidia_uvm` and `nvidia_drm` from the initramfs for the Plymouth LUKS screen. The resume hook runs in that same initramfs, after the driver has bound to the card. With `NVreg_PreserveVideoMemoryAllocations` set to 1, the driver demands a `/proc/driver/nvidia/suspend` handshake that was performed by the old kernel's userspace and cannot carry over, so `nv_pmops_freeze` returns `-EIO` and the restore is discarded. unconnect laid this out in issue #10039. Issue #5554 is the tracking issue and it is still open.

## If that did not work

**Image written, machine never powers off.** wjax found in issue #8589 that the kernel can abort silently during image creation on an s2idle-only machine. Create `/etc/systemd/sleep.conf.d/hibernate-mode.conf` containing a `[Sleep]` section with `HibernateMode=shutdown`.

**Hybrid ASUS ROG.** Omarchy ships a `force-igpu` sleep hook that detaches the dGPU through supergfxctl before hibernate, but rdelpiano showed in issue #9696 that neither the hook nor supergfxctl is installed unless you have run `omarchy toggle hybrid gpu`. Run it.

**Single NVIDIA GPU with no iGPU.** There is no reliable answer yet. Both settings of `NVreg_PreserveVideoMemoryAllocations` have been reported failing on Blackwell and Ada in #5554, one with a failed restore and the other with Xid faults after resume. Treat hibernate as unavailable on these machines for now.

**AMD crashes after resume.** sspaeti reported in issue #4259 that adding `amdgpu.gpu_recovery=1` and `amdgpu.noretry=0` to the kernel cmdline, later with `amdgpu.cwsr_enable=0`, ended the post-hibernate crashes on a TUXEDO InfinityBook. That was on 3.x, where the cmdline lived in `/etc/default/limine`. On 4.x put it in a `/etc/limine-entry-tool.d/` drop-in instead.

**You removed hibernation and boot got worse.** `omarchy hibernation remove` deletes the swapfile and the mkinitcpio hook but leaves `/etc/limine-entry-tool.d/resume.conf` in place, so the rebuilt UKI still carries `resume=` pointing at blocks that no longer hold a swapfile. brenodyego reported this in issue #10037. Delete the drop-in yourself, then run `sudo limine-mkinitcpio`.

**Nothing changed on 4.0.0 to 4.0.2.** The keyboard backlight sleep hook was installed non-executable on those releases, so it never ran. janne reported it in issue #7618 and 4.0.3 replaced the `cp -p` with a mode 0755 install. The visible impact is limited to ASUS keyboards blocking S4.

## Related

- The [System sleep](https://omarchy.org/manual/system-sleep/) chapter of the official manual
- [Suspend will not resume from s2idle](/fix/suspend-wont-resume-s2idle/)
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Hybrid GPU laptop black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [Suspend and sleep hardware notes](/hardware/suspend-sleep/)
- [omarchy-hibernation-setup](/reference/commands/omarchy-hibernation-setup/)
