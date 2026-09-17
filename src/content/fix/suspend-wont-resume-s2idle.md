---
title: "Laptop will not resume from suspend on Omarchy"
description: "Omarchy 4 laptop stuck black after suspend: tell a failed freeze from a kernel resume failure, then fix FUSE mounts, NVIDIA sleep services and kernel bugs."
answer: "First read the previous boot's kernel log: journalctl -k -b -1 | grep -E 'PM: suspend|refusing to freeze'. A freeze failure names the stuck tasks, usually an rclone, sshfs or gvfs FUSE mount. A suspend entry with no exit, or a log that simply stops, is a kernel or firmware failure: test stock linux or linux-lts and, on NVIDIA, enable nvidia-suspend.service with NVreg_PreserveVideoMemoryAllocations=1. Entry and exit both present means only the display stayed dark."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: other
issueCount: 311
errorStrings:
  - "PM: suspend entry (s2idle)"
  - "PM: Some devices failed to suspend, or early wake event detected"
  - "Freezing user space processes failed after 20.006 seconds (8 tasks refusing to freeze)"
  - "usb usb1: PM: failed to suspend async: error -16"
  - "brcmfmac 0000:01:00.0: PM: failed to suspend: error -5"
  - "i915 0000:00:02.0: [drm] *ERROR* [CRTC:149:pipe A] flip_done timed out"
tags: [suspend, s2idle, resume, nvidia, kernel, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/4184"
    title: "Issue #4184: Suspend not working in Omarchy 3.3"
    kind: issue
    author: "erikwestlund"
    date: "2026-01-09"
  - url: "https://github.com/omacom/omarchy/pull/4940"
    title: "PR #4940: Unmount FUSE filesystems before suspend/hibernate"
    kind: pr
    author: "alansikora"
    date: "2026-03-10"
  - url: "https://github.com/omacom/omarchy/issues/394"
    title: "Issue #394: suspend on BeeLink SER9 (and new Framework 13 AMD Ryzen AI 9 HX 370)"
    kind: issue
    author: "marcinczenko"
    date: "2025-07-29"
  - url: "https://github.com/omacom/omarchy/issues/5695"
    title: "Issue #5695: Black image on resume from suspend (sometimes ~60s freeze) after 3.7 kernel bump to 7.0"
    kind: issue
    author: "b-Tomas"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/12190"
    title: "Issue #12190: linux-omarchy 7.2.5-3 hangs during suspend entry on Wildcat Lake (XPS 13 DX13260); stock linux 7.2.3 suspends fine"
    kind: issue
    author: "t27duck"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12129"
    title: "Issue #12129: Black screen / Failure to wake from sleep on NVIDIA hardware"
    kind: issue
    author: "rafi-the-dev"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12041"
    title: "Issue #12041: Whole-screen rainbow/color corruption after lid resume on hybrid AMD+NVIDIA laptop"
    kind: issue
    author: "BigRed4547"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12193"
    title: "Issue #12193: Lid close starts suspend immediately; a quick reopen leaves a dark screen"
    kind: issue
    author: "ijt"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/2635"
    title: "Issue #2635: Omarchy 3.1 No Signal to Monitors When Waking from Sleep"
    kind: issue
    author: "ochowie"
    date: "2025-10-20"
  - url: "https://github.com/omacom/omarchy/issues/4740"
    title: "Issue #4740: Suspend and Hibernation not working"
    kind: issue
    author: "Divyanshu-kumar14"
    date: "2026-02-25"
  - url: "https://github.com/omacom/omarchy/issues/8106"
    title: "Issue #8106: T2 Mac: lid close never suspends, brcmfmac PCIe D3 timeout aborts every suspend attempt"
    kind: issue
    author: "nelKorajkic"
    date: "2026-08-24"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.4"
    title: "Omarchy v4.0.4 release notes"
    kind: release
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
credits:
  - name: "gulp"
    url: "https://github.com/gulp"
    for: "Traced a failed suspend to rclone FUSE mounts refusing to freeze, and posted the pre-sleep unmount unit"
  - name: "alansikora"
    url: "https://github.com/alansikora"
    for: "Wrote the unmount-fuse sleep hook that ships with Omarchy"
  - name: "t27duck"
    url: "https://github.com/t27duck"
    for: "Measured suspend success per kernel across boots, isolating a linux-omarchy regression"
  - name: "marcinczenko"
    url: "https://github.com/marcinczenko"
    for: "Documented s2idle-only firmware and the Wi-Fi rfkill state after a failed resume"
faq:
  - q: "Is s2idle or deep better on Omarchy?"
    a: "Neither is better in general. Use what your firmware offers. Read /sys/power/mem_sleep: if it prints only [s2idle], deep does not exist on that machine and no kernel parameter will create it. Omarchy only forces deep on T2 Macs."
  - q: "Does Omarchy enable the NVIDIA suspend services for me?"
    a: "No. In v4.0.4, install/hardware/nvidia.sh only writes nvidia_drm modeset=1 and the early-load MODULES line. nvidia-suspend.service, nvidia-resume.service and NVreg_PreserveVideoMemoryAllocations are yours to enable."
  - q: "Suspend broke right after I updated to 4.0.4. Why?"
    a: "4.0.4 ships the bespoke linux-omarchy kernel to everyone. At least one open report, issue #12190, shows suspend working on stock linux 7.2.3 and hanging on linux-omarchy 7.2.5-3 on the same machine."
  - q: "How do I get suspend out of the way until it works?"
    a: "Run omarchy toggle suspend. That hides the Suspend entry from the System menu under Super + Esc. Run it again to bring it back."
related: [hibernate-fails-or-hangs, bluetooth-stops-after-resume, black-screen-after-login, battery-drains-fast]
draft: false
---

Your laptop goes to sleep, and the only way back is holding the power button. This page splits that one symptom into the three different failures it actually is, because the fixes do not overlap. Checked against Omarchy 4.0.4 source, with notes where 3.x behaved differently.

## The fix

**1. Find out whether the kernel ever suspended.** After a forced reboot, read the previous boot's kernel log:

```bash
journalctl -k -b -1 | grep -E 'PM: suspend (entry|exit)|refusing to freeze|failed to suspend'
```

Three outcomes, three different problems:

- `PM: suspend entry`, then `Freezing user space processes failed` or `failed to suspend`, then a quick `PM: suspend exit`: the kernel aborted and the machine never actually slept. Go to step 2.
- `PM: suspend entry` with no `exit`, or a log that simply stops after logind's `Suspending...`: the kernel or firmware went down and never came up. A hard hang can take the unflushed tail of the journal with it, which is why three of the four hangs in issue #12190 below have no entry line at all. Go to step 4.
- `PM: suspend entry` with a matching `exit` and no errors between them: the kernel resumed. Your display or session never came back. Go to step 5.

**2. Nothing froze: hunt the stuck process.**

```bash
journalctl -k -b -1 | grep -i 'refusing to freeze'
mount | grep fuse
```

FUSE daemons stuck in uninterruptible sleep are the classic cause. In issue [#4184](https://github.com/omacom/omarchy/issues/4184), commenter `gulp` found rclone mounting Google Drive held the freeze for 20 seconds until it timed out, and the machine then sat awake pretending to be asleep, eating battery.

Omarchy ships a pre-sleep hook for this. `alansikora`'s [PR #4940](https://github.com/omacom/omarchy/pull/4940) merged on 2026-03-10 and shipped in v3.5.0. Confirm it is installed and root-owned:

```bash
ls -l /usr/lib/systemd/system-sleep/
```

Read the shipped script before trusting it. In v4.0.4 `unmount-fuse` only matches the `fuse.gvfsd-fuse` filesystem type, so it clears Nautilus mounts and leaves rclone, sshfs and other FUSE mounts alone. Unmount those yourself before sleeping, or add your own `pre` hook next to it.

v4.0.3 added migration `1788662350.sh`, which replaces the shipped `keyboard-backlight` and `force-igpu` hooks if they are not root-owned and parks the old copy under `/var/lib/omarchy/migrations/` for review. It does not touch `unmount-fuse` or hooks you wrote yourself, so check the `ls -l` output above for anything not owned by root and fix that by hand.

**3. Check what sleep state your firmware offers.**

```bash
cat /sys/power/mem_sleep
```

If the only entry is `[s2idle]`, deep sleep does not exist on that machine and no kernel parameter will invent one. That is the case on the Framework 13 with the Ryzen AI 9 HX 370 in issue [#394](https://github.com/omacom/omarchy/issues/394). If both are listed and s2idle is flaky, you can test deep for the current boot only:

```bash
echo deep | sudo tee /sys/power/mem_sleep
```

Omarchy itself only forces `mem_sleep_default=deep` (with `pm_async=off`) on T2 Macs, in `install/hardware/apple/fix-t2.sh` and migration `1785944594.sh`. Do not copy that Limine drop-in onto non-Apple hardware without testing the temporary switch first.

**4. Kernel went down and never came up.**

On NVIDIA, enable the driver's own sleep services. Omarchy does not do this for you: in v4.0.4, `install/hardware/nvidia.sh` writes only `options nvidia_drm modeset=1` and the early-load `MODULES` line.

```bash
echo 'options nvidia NVreg_PreserveVideoMemoryAllocations=1' | sudo tee /etc/modprobe.d/nvidia-power.conf
sudo systemctl enable nvidia-suspend.service nvidia-resume.service nvidia-hibernate.service
sudo limine-mkinitcpio
```

Reboot before testing. This helps when the NVIDIA card drives your panel. It does nothing on an offload-only hybrid laptop where the iGPU owns the display: in [#12041](https://github.com/omacom/omarchy/issues/12041) the reporter enabled all three services and the preserve flag and the corruption on resume was unchanged.

Then suspect the kernel. v4.0.4 ships the bespoke `linux-omarchy` kernel to everyone, and that is a real regression vector. Issue [#12190](https://github.com/omacom/omarchy/issues/12190) counts suspend outcomes per boot on a Dell XPS 13 with Wildcat Lake graphics: 13 of 13 suspends completed and resumed on stock `linux` 7.2.3, and 0 of 4 came back on `linux-omarchy` 7.2.5-3 with the same kernel command line (three of those four never even logged `PM: suspend entry`). Install `linux-lts`, or plain `linux` as that report did, boot it from the Limine menu, and suspend twice. If it resumes, you have a kernel bug, not an Omarchy configuration bug.

**5. Kernel resumed, screen stayed dark.** Get a TTY with `Ctrl + Alt + F3`. One reporter in [#2635](https://github.com/omacom/omarchy/issues/2635) found the monitors lit up the moment they switched VT; others in the same thread got no TTY at all. From a TTY or over SSH as your own user, point `hyprctl` at the running instance and ask Hyprland to re-enable output:

```bash
export HYPRLAND_INSTANCE_SIGNATURE=$(hyprctl instances | awk -F'[ :]' '/^instance / {print $2}')
omarchy system wake
hyprctl dispatch dpms on
```

If `dpms on` does nothing, `sudo systemctl restart sddm` brought the screens back for two people in that thread, at the cost of the whole Hyprland session. If the TTY is dead too, the compositor or the kernel display driver is wedged and only a power cycle will clear it. Issue [#5695](https://github.com/omacom/omarchy/issues/5695) shows the i915 form of this, with `flip_done timed out` and PHY A errors after resume. A commenter there linked an upstream kernel commit, but the one person who applied it found it only covers DisplayPort tunnels and did nothing for the internal panel; what worked for several reporters was booting `linux-lts` or another 6.x kernel. That is a kernel problem, not a config change.

**6. If it never works, take suspend off the menu.**

```bash
omarchy toggle suspend
```

That hides Suspend from the System menu (`Super + Esc`). The 3.x path was different: 3.3.0 removed suspend from the menu by default and offered it back under Setup > System Sleep, and 3.4.0 made it default-on again with the same opt-out. See the manual chapter on [system sleep](https://omarchy.org/manual/system-sleep/).

## Verify it worked

Suspend and resume twice, then check the pairs line up:

```bash
journalctl -k -b -1 | grep -E 'PM: suspend (entry|exit)'
journalctl -k -b -1 | grep -iE 'failed to suspend|refusing to freeze|early wake event'
```

You want one `exit` for every `entry` and nothing in the second command. Also confirm the lock path is healthy, since in 4.x the pre-suspend lock runs through Quickshell:

```bash
systemctl --user status omarchy-sleep-lock.service
omarchy debug idle
busctl get-property org.freedesktop.login1 /org/freedesktop/login1 \
  org.freedesktop.login1.Manager InhibitDelayMaxUSec
```

That last value should be `15000000`. Omarchy ships a logind drop-in raising `InhibitDelayMaxSec` to 15 seconds, and migration `1784970000.sh` sets the reboot-required flag when the running value does not match.

## Why it happens

A suspend is three separate stages, and "it did not wake up" is the same symptom for a failure in any of them.

Freezing userspace comes first. Any task stuck in an uninterruptible kernel call, typically FUSE, blocks the freeze until it times out, and the machine stays on.

Then the kernel hands off to firmware. On s2idle the CPU never fully powers down and the platform is responsible for the low-power state, so a single misbehaving device (a WWAN modem, a Wi-Fi card, an NVMe controller) can keep the system awake or wedge it on the way back. Errors like `usb usb1: PM: failed to suspend async: error -16` (a Dell G15 with a USB hub in [#4740](https://github.com/omacom/omarchy/issues/4740)) and `brcmfmac 0000:01:00.0: PM: failed to suspend: error -5` (T2 MacBooks in [#8106](https://github.com/omacom/omarchy/issues/8106)) show up here, and in both the kernel abandons the suspend and wakes straight back up. deep sleep pushes more of the work onto firmware, which is why swapping states sometimes helps and sometimes makes things worse.

Last, the display has to come back. The NVIDIA driver discards video memory across suspend unless `NVreg_PreserveVideoMemoryAllocations` is set and the suspend services are enabled. Intel and AMD have their own resume-path bugs; the i915 timeouts in #5695 are a kernel issue, not an Omarchy one, which is why it also reproduces on Fedora for one commenter in that thread.

Quattro adds a fourth wrinkle on the way down. Locking now happens in Quickshell, and `omarchy-system-lid-close` starts the lock the moment the lid shuts rather than waiting for logind's `PrepareForSleep`, precisely so the lock finishes inside the inhibitor window. Issue [#12193](https://github.com/omacom/omarchy/issues/12193) describes the remaining race: logind commits to suspend on lid close while Hyprland never sees the lid reopen, because `user.slice` is already frozen, so a quick close and open leaves a dark screen.

## If that did not work

Collect logs before filing anything. `omarchy debug` uploads a bundle to `logs.omarchy.org` and prints the link, which is what maintainers ask for. Include your `/sys/power/mem_sleep` output, the `PM: suspend` lines from the failed boot, your exact kernel package and version, and whether stock `linux` behaves differently.

The evidence here is uneven on purpose. The FUSE cause is confirmed and fixed in-tree. The kernel regressions are recent and open; #12190 is the only one A/B tested against stock `linux`, while #12129 and #12041 sit on the same `linux-omarchy` 7.2.5-3 build without that comparison. The hybrid-GPU corruption in #12041 has no known fix at all. If your machine is not in one of those buckets, assume it is firmware or device specific and say so when you report it.

## Related

- [Hibernate fails or hangs](/fix/hibernate-fails-or-hangs/): a different code path, shares the FUSE and resume-parameter problems
- [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/) and [Wi-Fi drops after a kernel update](/fix/wifi-drops-after-kernel-update-iwlwifi/): for when only one device fails to come back
- [Black screen after login](/fix/black-screen-after-login/): if the panel is dark at boot, not just after sleep
- [Suspend, sleep and resume hardware notes](/hardware/suspend-sleep/) and [T2 Macs](/hardware/t2-mac/)
- [omarchy-toggle-suspend](/reference/commands/omarchy-toggle-suspend/) and [v4.0.4 release notes](/releases/v4.0.4/)
