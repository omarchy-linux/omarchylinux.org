---
title: "Suspend, sleep and resume on Omarchy"
description: "What suspend, sleep and resume actually do on Omarchy 4.x: the lock-before-sleep path, the sleep hooks it ships, the models that break, and the fix order."
answer: "Suspend works on most Omarchy 4.0.4 machines and is on by default; hibernation is opt-in via `omarchy hibernation setup`. Most failures are kernel or GPU driver bugs, not Omarchy: try the stock `linux` or `linux-lts` kernel first, then check NVIDIA sleep services, then force a real DPMS transition if the screen alone stays dark."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "suspend-sleep"
issueCount: 460
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [suspend, sleep, resume, hibernate, laptop, power]
sources:
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/12190"
    title: "Issue #12190: linux-omarchy 7.2.5-3 hangs during suspend entry on Wildcat Lake (XPS 13 DX13260); stock linux 7.2.3 suspends fine"
    kind: issue
    author: "t27duck"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12193"
    title: "Issue #12193: Lid close starts suspend immediately; a quick reopen leaves a dark screen"
    kind: issue
    author: "ijt"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/pull/12210"
    title: "PR #12210: Debounce lid-close suspend so a quick reopen does not sleep in the dark"
    kind: pr
    author: "ijt"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12194"
    title: "Issue #12194: MacBookPro14,2 (T1 Alpine Ridge): S3 wake loop heats the chassis and eventually hangs resume"
    kind: issue
    author: "ijt"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12147"
    title: "Issue #12147: LG display stays off after wake: dpmsStatus desyncs true while panel has no signal"
    kind: issue
    author: "SykesTheLord"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12140"
    title: "Issue #12140: Lock screen never blanks display again after resume-from-suspend"
    kind: issue
    author: "MolluscMonk"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12129"
    title: "Issue #12129: Black screen / Failure to wake from sleep on NVIDIA hardware"
    kind: issue
    author: "rafi-the-dev"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12096"
    title: "Issue #12096: hibernation remove leaves resume kernel parameters in the UKI"
    kind: issue
    author: "maandrij"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12095"
    title: "Issue #12095: omarchy-usb-autosuspend.conf is a no-op; Intel Bluetooth controllers still autosuspend"
    kind: issue
    author: "jordanglean"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12041"
    title: "Issue #12041: Whole-screen rainbow/color corruption after lid resume on hybrid AMD+NVIDIA laptop"
    kind: issue
    author: "BigRed4547"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/11412"
    title: "Issue #11412: Fingerprint unlock fails after every suspend (fprintd device stuck busy)"
    kind: issue
    author: "callumau"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/5695"
    title: "Issue #5695: Black image on resume from suspend (sometimes ~60s freeze) after 3.7 kernel bump to 7.0"
    kind: issue
    author: "b-Tomas"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/issues/5554"
    title: "Issue #5554: Hibernation with Nvidia GPU Issues"
    kind: issue
    author: "ryanrhughes"
    date: "2026-05-02"
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
  - url: "https://github.com/omacom/omarchy/issues/2635"
    title: "Issue #2635: Omarchy 3.1 No Signal to Monitors When Waking from Sleep"
    kind: issue
    author: "ochowie"
    date: "2025-10-20"
credits:
  - name: "alansikora"
    url: "https://github.com/alansikora"
    for: "Traced suspend failure and battery drain to frozen FUSE mounts and shipped the pre-sleep unmount hook"
  - name: "ijt"
    url: "https://github.com/ijt"
    for: "Documented the lid close/open suspend race and the Alpine Ridge Thunderbolt wake loop"
  - name: "SykesTheLord"
    url: "https://github.com/SykesTheLord"
    for: "Found the dpmsStatus desync that makes omarchy-brightness-display skip a dark monitor on wake"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Maintains the NVIDIA hibernation tracking issue and its test matrix"
  - name: "jordanglean"
    url: "https://github.com/jordanglean"
    for: "Showed that the shipped usbcore autosuspend drop-in cannot apply to a builtin module"
faq:
  - q: "Does Omarchy suspend when the screen locks or goes idle?"
    a: "No. The shipped idle path locks the session and blanks the display. Nothing in the default config suspends on a timer, so a machine left alone stays awake unless you close the lid or pick Suspend from the menu."
  - q: "Why is there no Hibernate entry in my system menu?"
    a: "The menu entry is gated on omarchy-hibernation-available, which needs non-zram swap larger than /sys/power/image_size plus /etc/mkinitcpio.conf.d/omarchy_resume.conf. Run `omarchy hibernation setup` to create both. It needs the Limine bootloader and free disk space equal to your RAM."
  - q: "Suspend is unreliable on my machine. Can I just turn it off?"
    a: "Yes. `omarchy toggle suspend` hides the Suspend entry from the system menu so you stop hitting it by accident. It does not stop logind from suspending on lid close, so pair it with a logind drop-in if that is the trigger."
related: [suspend-wont-resume-s2idle, hibernate-fails-or-hangs, bluetooth-stops-after-resume, nvidia, hybrid-gpu]
draft: false
---

Suspend is enabled by default on Omarchy 4.x. Hibernation is not: you opt into it. This page covers what the shipped system actually does around sleep, which failures are real and current on 4.0.4, and the order to try fixes in. Everything below was checked against the v4.0.4 source tree and against issues filed on 4.0.x. The manual chapter is [System sleep](https://omarchy.org/manual/system-sleep/).

## Status on 4.0.4

Suspend works on most machines. The 460 issues that touch sleep are dominated by a handful of hardware classes: NVIDIA and hybrid NVIDIA laptops that come back to a black screen, Intel Meteor Lake panels that freeze for about a minute on resume, Intel Macs, and whatever the current kernel has just broken. Very little of the breakage lives in Omarchy's own code. Most of it is the kernel, the GPU driver, or firmware, which is why the first fix below is a kernel swap rather than a config edit.

Hibernation is a different story. It is opt-in, it requires Limine, and on NVIDIA it is still openly unfinished. Treat working hibernation as a nice surprise rather than a baseline.

## What Omarchy does automatically

Locking before sleep is the part Omarchy owns. A user unit, `omarchy-sleep-lock.service`, runs `omarchy-system-sleep-monitor`, which holds a `systemd-inhibit --what=sleep --mode=delay` lock and watches logind's `PrepareForSleep` signal. When the signal arrives it runs `omarchy-system-sleep-lock`, which asks Quickshell to lock and polls until the session reports secure. A delay inhibitor is a timer, not a promise, so logind suspends when the window expires whether or not the lock landed. Omarchy ships `/etc/systemd/logind.conf.d/20-inhibit-delay.conf` raising `InhibitDelayMaxSec` from the 5 second default to 15, and the lock script derives its own budget from what logind reports, capped at 12 seconds. If it loses the race you get a critical notification saying the session was left unlocked.

Closing the lid is bound in Hyprland, not just in logind. `default/hypr/bindings/utilities.lua` binds `switch:on:Lid Switch` to `omarchy-system-lid-close`, which locks immediately, unless external monitors are connected, and then reconciles clamshell state. Locking on lid close rather than waiting for `PrepareForSleep` is deliberate: it gives the shell a head start before logind commits.

Three `system-sleep` hooks ship in `default/systemd/system-sleep/`:

- `unmount-fuse` lazily unmounts gvfsd-fuse mounts before sleep and restarts gvfs afterwards. FUSE daemons stuck in uninterruptible sleep used to time out the process freeze, so suspend silently failed and the machine cooked in a bag. Added by PR #4940, shipped in v3.5.0.
- `keyboard-backlight` turns the keyboard backlight off before hibernate, because some ASUS LED controllers block S4.
- `force-igpu` uses supergfxctl to park a discrete GPU in Vfio before hibernate and restore Integrated mode afterwards, since the NVIDIA driver cannot freeze a powered-off dGPU.

Apple hardware gets two install-time quirks. `install/hardware/apple/fix-suspend-nvme.sh` installs a service that clears `d3cold_allowed` on the NVMe controller for MacBook8,1, 9,1, 10,1 and MacBookPro13,x and 14,x. `fix-t2.sh` adds `pm_async=off mem_sleep_default=deep` to the Limine cmdline on T2 Macs, which v4.0.0 listed as fixing T2 suspend and fan defaults.

Hibernation setup is a single command, `omarchy hibernation setup`. It creates a `/swap` btrfs subvolume with a swapfile the size of your RAM, marks it nodatacow, adds the fstab entry, adds the `resume` mkinitcpio hook, writes `resume=` and `resume_offset=` into a Limine drop-in, adds `rtc_cmos.use_acpi_alarm=1` on s2idle systems, and rebuilds the UKI. `omarchy hibernation remove` undoes it.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#12190](https://github.com/omacom/omarchy/issues/12190) suspend entry hangs on `linux-omarchy` 7.2.5-3, stock `linux` 7.2.3 fine | Dell XPS 13 DX13260, Intel Wildcat Lake | open | not fixed |
| [#12129](https://github.com/omacom/omarchy/issues/12129) black screen, no wake | ASUS TUF F17, RTX 4070 Mobile | open | not fixed |
| [#12041](https://github.com/omacom/omarchy/issues/12041) rainbow corruption after lid resume, survives shell restart | Lenovo Slim Pro 7 14ARP8, AMD iGPU plus RTX 3050 | open | not fixed |
| [#5695](https://github.com/omacom/omarchy/issues/5695) i915 commit timeouts, roughly 60s freeze on resume | ThinkPad P1 Gen 7, Alienware m16 R2, Meteor Lake | open | not fixed |
| [#12194](https://github.com/omacom/omarchy/issues/12194) Thunderbolt PME wakes the machine every 45s with the lid shut | MacBookPro14,2 and Alpine Ridge siblings | open | not fixed |
| [#12193](https://github.com/omacom/omarchy/issues/12193) lid close then quick reopen leaves a dark screen | any laptop, reported on MacBookPro14,2 | open, PR [#12210](https://github.com/omacom/omarchy/pull/12210) | not fixed |
| [#12147](https://github.com/omacom/omarchy/issues/12147) one monitor stays dark after wake while Hyprland reports DPMS on | external DisplayPort monitors | open | not fixed |
| [#12140](https://github.com/omacom/omarchy/issues/12140) lock screen never blanks again after a resume | any | open | not fixed |
| [#5554](https://github.com/omacom/omarchy/issues/5554) hibernate does not power off, display corruption on resume | NVIDIA desktops and laptops | open, tracking issue | not fixed |
| [#12096](https://github.com/omacom/omarchy/issues/12096) hibernation remove leaves stale `resume=` in the UKI | any | open | not fixed |
| [#12095](https://github.com/omacom/omarchy/issues/12095) shipped usbcore autosuspend drop-in is a no-op, BLE mice fail to reconnect | Intel Bluetooth, AX201 and similar | open | not fixed |
| [#11412](https://github.com/omacom/omarchy/issues/11412) fingerprint unlock dead after suspend, fprintd stuck busy | Framework Laptop 13, Goodix sensor | open | not fixed |
| [#4184](https://github.com/omacom/omarchy/issues/4184) no wake plus heavy battery drain during sleep | Framework 13 AMD | partly fixed | v3.5.0 for the FUSE half |

Two patterns are worth naming. First, several of these reproduce outside Omarchy. In #5695 a reporter hit the same i915 timeouts on Ubuntu with GNOME on the same ThinkPad, and the same reporter measured zero events on a 6.17 kernel against 17 on 7.0. Second, #12190 is a clean kernel bisect by package: 13 suspends out of 13 on stock `linux` 7.2.3, one successful suspend entry out of four and zero resumes on `linux-omarchy` 7.2.5-3, which is the kernel v4.0.4 shipped to everyone.

## Fixes that work

Work in this order.

1. Update, then reboot. `omarchy update` gets you to 4.0.4 and the current shell.
2. Read the journal from the boot after the failure, not the failing one. Once userspace freezes, journald stops, so a hard power-off loses everything the kernel printed. `journalctl -b -1 -k | grep -E "PM: suspend (entry|exit)"` tells you whether the kernel entered sleep, resumed, or never came back.
3. Swap kernels. If suspend entry hangs or resume never happens, boot stock `linux`, or `linux-lts` for Meteor Lake panel freezes, and test the same cycle. This is the single highest-yield step right now.
4. On NVIDIA, enable `nvidia-suspend.service`, `nvidia-hibernate.service` and `nvidia-resume.service`, and set the video memory parameter that matches your driver branch: `NVreg_PreserveVideoMemoryAllocations=1` on older branches, `NVreg_UseKernelSuspendNotifiers=1` on 595 and newer. Check with `cat /proc/driver/nvidia/params` after a reboot, and rerun `limine-update` after any change.
5. If only the screen is dead and the machine is alive over SSH, force a real DPMS transition rather than a redundant enable: `hyprctl dispatch 'hl.dsp.dpms({ action = "disable" })'` then the same with enable. A plain `omarchy system wake` can no-op when Hyprland already believes the panel is lit.
6. If the machine wakes itself, look at `/proc/acpi/wakeup` for Thunderbolt root ports, xHCI controllers and the Wi-Fi PME, and disable the ones you do not need to wake on.
7. If nothing helps, `omarchy toggle suspend` removes Suspend from the system menu so you stop triggering a known-bad path.

For hibernation specifically: it needs Limine, free space equal to your RAM, and a correct `resume_offset`. Verify with `btrfs inspect-internal map-swapfile -r /swap/swapfile` against the value in `/etc/limine-entry-tool.d/resume.conf`. Use `systemctl start systemd-hibernate.service` when testing, because `systemctl hibernate` returns immediately and will mislead you.

## Report it

Sleep bugs are only actionable with the boot after the failure attached. Run `omarchy debug`, pick Upload log, and paste the `logs.omarchy.org` URL into the issue. For lock and idle problems specifically, `omarchy debug idle` dumps the shell's idle state, the sleep-lock unit status, and current idle inhibitors. Include your exact kernel package and version, since `linux-omarchy` and stock `linux` behave differently, plus `cat /sys/power/mem_sleep` so it is clear whether you are on s2idle or deep. If you can, report the result on both kernels. That comparison is what moved #12190 forward.

## Related

Component pages: [NVIDIA](/hardware/nvidia/), [hybrid GPU laptops](/hardware/hybrid-gpu/), [multi-monitor](/hardware/multi-monitor/), [battery and power](/hardware/battery-power/), [T2 Macs](/hardware/t2-mac/), [Bluetooth](/hardware/bluetooth/).

Fix pages: [suspend will not resume on s2idle](/fix/suspend-wont-resume-s2idle/), [hibernate fails or hangs](/fix/hibernate-fails-or-hangs/), [Bluetooth stops after resume](/fix/bluetooth-stops-after-resume/), [black screen after login](/fix/black-screen-after-login/), [lock screen will not unlock](/fix/lock-screen-wont-unlock/), [battery drains fast](/fix/battery-drains-fast/).
