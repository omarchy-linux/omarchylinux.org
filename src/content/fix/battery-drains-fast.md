---
title: "Battery drains fast on Omarchy"
description: "Why an Omarchy laptop burns battery faster than Windows, what power management actually ships in 4.0.4, and the profile, screensaver, and hybrid GPU fixes."
answer: "Omarchy ships power-profiles-daemon and nothing else, so nothing tunes the machine for you beyond the profile. Set the battery profile once with omarchy powerprofiles set battery power-saver and it is remembered per power source. Then kill the two big drains: the idle screensaver on HiDPI or multi-monitor setups, and an NVIDIA dGPU that never sleeps on hybrid laptops."
appliesTo:
  from: "3.x"
status: workaround
category: other
issueCount: 178
errorStrings:
  - "Time to recharge!"
  - "Battery is down to 10%"
  - "omarchy-powerprofiles-set' failed with exit code 1"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [battery, power-profiles, tlp, screensaver, hybrid-gpu, laptop]
sources:
  - url: "https://omarchy.org/manual/system-sleep/"
    title: "Omarchy manual: System sleep"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/1776"
    title: "Issue #1776: Laptop / Hybrid GPU Power Management Issue (NVIDIA, iGPU + dGPU)"
    kind: issue
    author: "itsmedardan"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/issues/9193"
    title: "Issue #9193: Screensaver saturates 5+ CPU cores and thermally throttles on HiDPI displays"
    kind: issue
    author: "markvogel"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/8596"
    title: "Issue #8596: powerprofilesctl crashes (SIGABRT) when power-profiles-daemon is masked, hit on every power event with TLP"
    kind: issue
    author: "ogrt"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11058"
    title: "Issue #11058: Battery service forks powerprofilesctl get every 2 s for the whole session (~5% of a core, on battery too)"
    kind: issue
    author: "vstoyanov"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/pull/11637"
    title: "PR #11637: Poll the active power profile over D-Bus instead of powerprofilesctl"
    kind: pr
    author: "dhh"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/7582"
    title: "Issue #7582: Power panel spawns three helper processes every five seconds while open"
    kind: issue
    author: "evo-social-world"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/8184"
    title: "Issue #8184: omarchy-powerprofiles-set fails at boot (exit 1): CPU power profile never applied on AC"
    kind: issue
    author: "kshatriya-abhay"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/12095"
    title: "Issue #12095: omarchy-usb-autosuspend.conf is a no-op; Intel Bluetooth controllers still autosuspend"
    kind: issue
    author: "jordanglean"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/8648"
    title: "Issue #8648: Consumiing insane amount of battery"
    kind: issue
    author: "notTanveer"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/discussions/3907"
    title: "Discussion #3907: Guide: Replacing Power Profiles with TLP to improve battery life"
    kind: discussion
    author: "pomartel"
    date: "2025-12-16"
  - url: "https://github.com/omacom/omarchy/discussions/4768"
    title: "Discussion #4768: System blackout after failed update 3.3.3 to 3.4.0 (pomartel's answer on the TLP conflict)"
    kind: discussion
    author: "wearethesame13"
    date: "2026-02-27"
  - url: "https://github.com/omacom/omarchy/discussions/933"
    title: "Discussion #933: Auto Switch Power Profiles on AC/Battery"
    kind: discussion
    author: "webbegg"
    date: "2025-08-20"
credits:
  - name: "itsmedardan"
    url: "https://github.com/itsmedardan"
    for: "Documented the NVIDIA dGPU never entering d3cold on hybrid laptops and the render offload setup that halved power draw for others in the thread"
  - name: "markvogel"
    url: "https://github.com/markvogel"
    for: "Measured the idle screensaver at 5.3 cores and 97 C package temperature on a HiDPI multi-monitor Framework 13"
  - name: "vstoyanov"
    url: "https://github.com/vstoyanov"
    for: "Measured the two second powerprofilesctl poll in dev builds at roughly 5 percent of a core"
  - name: "ogrt"
    url: "https://github.com/ogrt"
    for: "Showed that masking power-profiles-daemon for TLP makes powerprofilesctl crash on every power event"
  - name: "pomartel"
    url: "https://github.com/pomartel"
    for: "Wrote the TLP replacement guide and the note that TLP and power-profiles-daemon cannot both be installed"
  - name: "kshatriya-abhay"
    url: "https://github.com/kshatriya-abhay"
    for: "Traced the boot time profile helper failing because udev fires before power-profiles-daemon starts"
faq:
  - q: "Does Omarchy install TLP?"
    a: "No. The only power daemon in install/omarchy-base.packages is power-profiles-daemon, enabled in install/config/enable-services.sh. Intel laptops with a battery also get thermald and, on Alder Lake and newer hybrid CPUs, intel-lpmd. Nothing else tunes disks, PCIe, or USB."
  - q: "Can I just install TLP instead?"
    a: "You can, but it is a trade. TLP and power-profiles-daemon conflict, and if you mask the daemon the shell's power panel and menu still shell out to powerprofilesctl, which crashes against a dead daemon. That is issue #8596, still open on 4.0.4."
  - q: "Why is there no charge limit slider?"
    a: "Omarchy 4.0.4 reads charge thresholds for display in omarchy-battery-status but ships no command to set one. Set it in firmware, or with your laptop vendor's own tool."
  - q: "Does the bespoke kernel in 4.0.4 help battery life?"
    a: "The 4.0.4 release notes describe linux-omarchy as tuned for desktop responsiveness under load and for gaming, and say it refines power management, without numbers or a battery life claim. If your drain started exactly at 4.0.4, the stock linux kernel is still installable as a comparison."
related: [suspend-wont-resume-s2idle, hibernate-fails-or-hangs, nvidia-drivers-omarchy-4, hybrid-gpu-laptop-black-screen-aq-drm-devices]
draft: false
---

An Omarchy laptop that empties in two hours is almost never one bug. It is a stack of small things: a power profile that was never applied, a screensaver that rasterizes on the CPU, and on hybrid laptops a discrete GPU that never sleeps. Everything below was checked against the v4.0.4 source tree, with v3.8.4 for comparison.

## The fix

**1. Check the profile actually applied, then set the one you want for battery.**

```bash
powerprofilesctl get
omarchy powerprofiles list
omarchy powerprofiles set battery power-saver
```

Since 4.0.0 Omarchy remembers an explicit choice per power source. `omarchy-powerprofiles-set` writes it to `~/.local/state/omarchy/powerprofiles/battery` (or `/ac`) and restores it next time you are in that state. Out of the box you get performance on AC and balanced on battery, so battery never drops to `power-saver` unless you ask. The [system sleep chapter](https://omarchy.org/manual/system-sleep/) covers the same commands.

On 3.x there was no memory. The helper always picked balanced on battery, driven by udev rules in `/etc/udev/rules.d/99-power-profile.rules`. Those rules ran a script out of your home directory, and the 4.x migration `1788102906` removes or quarantines them. If you upgraded, confirm the profile still changes when you unplug.

**2. Measure before you change anything.**

```bash
omarchy battery status
sudo pacman -S powertop && sudo powertop
```

`omarchy battery status` prints percentage, time remaining, and instantaneous draw in watts, read from `power_now` in sysfs rather than UPower's lagging average. Note the watts with the screen on and nothing running. Anything above roughly 10 W idle on a modern thin laptop means something is awake that should not be. Powertop's overview tab names it.

**3. Turn off the screensaver if you have a HiDPI or multi-monitor setup.**

```bash
omarchy toggle screensaver
```

The screensaver starts after 150 seconds of idle by default and opens one fullscreen terminal per monitor at a hardcoded 120 frames per second. Omarchy's shipped terminal is foot, which rasterizes on the CPU. markvogel measured 5.3 cores of CPU, a package temperature climb from 60 C to 97 C, and rising throttle counts on a three monitor Framework 13 in issue #9193. That is the single worst idle drain on the list and it fires while you are away from the machine.

Idle timings live in `~/.config/omarchy/shell.json` under `idle`, as `screensaver` and `lock` in seconds. The shipped defaults are 150 and 300.

**4. On a hybrid NVIDIA laptop, check whether the dGPU is actually asleep.**

```bash
cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status
sudo lsof /dev/nvidia*
```

Use your own PCI address from `lspci`. If the status is `active` at idle, or Hyprland and the launcher hold the device open, the card is burning watts for nothing. That is issue #1776, where itsmedardan showed the dGPU never reaching d3cold and another reporter halved power draw after moving rendering to the iGPU. On supported laptops `omarchy toggle hybrid gpu` installs supergfxctl and switches modes. See [hybrid GPU](/hardware/hybrid-gpu/) and [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/) first, because switching modes can cost you a session.

**5. Close the power panel when you are done with it.**

Leaving the panel open runs three helper processes every five seconds, one of which produces data the panel never displays. evo-social-world documented it in issue #7582, still open on 4.0.4. It is small, but it is exactly the kind of never stopping wakeup that keeps a CPU out of deep idle.

**6. If you run the dev channel, update.**

Dev builds of Quattro polled `powerprofilesctl get` every two seconds for the whole session. vstoyanov measured that at roughly 5 percent of a core and 111 ms of CPU per call in issue #11058. dhh swapped the Python CLI for a `busctl` property read in PR #11637, merged 2026-09-13; the two second timer stays, but each tick is a cheap D-Bus call instead of an interpreter start. The battery service in the tagged 4.0.x trees has no such timer at all, so this only matters on `dev` or an older dev checkout.

## Verify it worked

Unplug, leave the machine idle at the desktop with the lid open, wait a minute, then run `omarchy battery status` twice about 30 seconds apart. You want a stable watt figure, not a moving one. Compare it with what you noted in step 2.

Then confirm the profile survives a plug cycle:

```bash
powerprofilesctl get   # while unplugged
powerprofilesctl get   # again, a few seconds after plugging in
```

If nothing changes on unplug, the shell's battery service is not firing. It reacts to `UPower.onBattery`, so check `busctl get-property org.freedesktop.UPower /org/freedesktop/UPower org.freedesktop.UPower OnBattery` while unplugged.

## Why it happens

Omarchy ships one power daemon and nothing else. `install/omarchy-base.packages` lists `power-profiles-daemon`, and `install/config/enable-services.sh` enables it. There is no TLP, no laptop-mode-tools, no disk or PCIe tuning. Intel machines with a battery additionally get `thermald`, and Alder Lake and newer hybrid Intel CPUs get `intel-lpmd`, both from `install/hardware/intel/`. That is the whole of it. Arch with a bare profile daemon idles higher than a vendor tuned Windows install, which is what reports like issue #8648 describe. Automatic switching on plug and unplug only arrived in 3.4.0; before that, people wired it up themselves with udev rules, as in discussion #933.

Two shipped defaults deliberately spend power. Wi-Fi power save is switched off in `/etc/NetworkManager/conf.d/omarchy-wifi-powersave.conf`, and the file says why: it trades a fraction of a watt for avoiding latency spikes and broken Intel BE200 firmware. A migration turns it off on running interfaces too. The USB autosuspend file every 4.0.x release ships at `/etc/modprobe.d/omarchy-usb-autosuspend.conf` sets a `usbcore` option that cannot apply, because `usbcore` is built into the kernel, which jordanglean documented in issue #12095. So USB devices keep whatever the udev hwdb gives them.

The low battery warning is a warning only. The shell's battery service checks every 30 seconds and, at 10 percent while discharging, runs `omarchy-battery-low`, which sends the "Time to recharge!" notification and fires the `battery-low` hook. Drop an executable script in `~/.config/omarchy/hooks/battery-low.d/` to add your own action. There is a `play-warning-sound.sample` to copy. Nothing in that path reduces power draw or suspends the machine for you.

One more failure mode worth ruling out: the profile may never have applied at boot. In issue #8184, on a machine upgraded from 3.x that still carried the old `99-power-profile.rules`, the udev event fired before `power-profiles-daemon` had started, the helper exited 1, and the machine stayed on whatever profile was left over. A clean 4.x install has no udev rule; the shell applies the profile when UPower reports a change. `journalctl -b | grep powerprofiles` shows either path.

## If that did not work

**Consider TLP, with your eyes open.** pomartel's guide in discussion #3907 replaces power-profiles-daemon with `tlp` plus `tlp-pd` and symlinks `powerprofilesctl` to `tlpctl`. It works, and TLP tunes far more than CPU governors. But the two daemons conflict and cannot both be installed, as pomartel put it in the accepted answer on discussion #4768. Worse on 4.x: when the daemon is masked, `powerprofilesctl` crashes with SIGABRT instead of failing cleanly, and the shell calls it from the power panel, the menu, and every AC transition. That is ogrt's issue #8596, open as of 2026-09-16. Note that `tlp-pd` was not in the Arch repos for at least one reader of that guide, and pomartel later wrote in the same thread that he went back to power-profiles-daemon because TLP caused odd issues when not tuned carefully.

**Check the battery itself.** `omarchy battery status` prints the full charge capacity in watt hours; compare it with the design capacity in `/sys/class/power_supply/BAT0/energy_full_design`. A cell at half its design capacity drains twice as fast and no software fixes that. On dual battery laptops the readout covers only the first battery: `omarchy-battery-status` takes the first UPower BAT device, so a ThinkPad with an internal and an external pack shows one of them.

**Look for a single runaway process.** A stuck Chromium tab, a compile loop, or an agent CLI left running will beat every tweak on this page. `btop` ships by default.

The drains with measurements attached are the screensaver, the dGPU, and the dev channel poll. If you measure something else, open an issue with `omarchy debug` output attached.

## Related

- [Suspend will not resume from s2idle](/fix/suspend-wont-resume-s2idle/)
- [Hibernate fails or hangs](/fix/hibernate-fails-or-hangs/)
- [Battery and power hardware notes](/hardware/battery-power/)
- [Hybrid GPU laptops](/hardware/hybrid-gpu/)
- [Suspend and sleep](/hardware/suspend-sleep/)
- [Omarchy commands reference](/reference/commands/)
