---
title: "Hybrid GPU laptop black screen or login loop (AQ_DRM_DEVICES)"
description: "Hybrid NVIDIA plus Intel or AMD laptops on Omarchy 4: why a by-path AQ_DRM_DEVICES value login-loops Hyprland, and the colon-free fix that works."
answer: "Unset AQ_DRM_DEVICES first. Aquamarine splits the value on every colon, so a /dev/dri/by-path/pci-0000:01:00.0-card pin leaves zero usable GPUs and Hyprland dies into a silent SDDM loop. Get a TTY with Ctrl+Alt+F2, remove the value from your uwsm session environment, reboot. If you truly need a GPU order, use colon-free cardN names or udev symlinks, set in the session environment, never in hyprland.lua."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: display
issueCount: 13
errorStrings:
  - "drm: Found no gpus to use, cannot continue"
  - "CBackend::create() failed!"
  - "[AQ] atomic drm request: failed to commit: Cannot allocate memory"
  - "context reset due to GPU hang"
  - "The module nvidia_drm is missing"
tags: [hybrid-gpu, nvidia, aq-drm-devices, black-screen, login-loop, display]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8776"
    title: "Issue #8776: Dual-GPU AMD: PCI by-path in AQ_DRM_DEVICES silently login-loops SDDM autologin"
    kind: issue
    author: "mowgli42"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/8786"
    title: "PR #8786: Fix AQ_DRM_DEVICES by-path login loop"
    kind: pr
    author: "Elshayib"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/pull/9063"
    title: "PR #9063: Warn on bad AQ_DRM_DEVICES in debug"
    kind: pr
    author: "Elshayib"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/10350"
    title: "Issue #10350: Hybrid Pascal (nvidia-580xx) + Intel iGPU: Hyprland crashes when dGPU-driven external monitors are actively used, i915 rcs0 GPU hang; NVIDIA-first AQ_DRM_DEVICES fixes it"
    kind: issue
    author: "christianjgilman"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/issues/9720"
    title: "Issue #9720: [Hardware]: Black screen on boot on AMD Strix Point / Radeon 890M laptops (ASUS ROG Zephyrus G14) due to Aquamarine atomic DRM commit failure"
    kind: issue
    author: "codyoss"
    date: "2026-09-02"
  - url: "https://github.com/omacom/omarchy/issues/7755"
    title: "Issue #7755: NVIDIA env vars never set: os.execute() broken inside Hyprland Lua config"
    kind: issue
    author: "seanymc85"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/3242"
    title: "Issue #3242: System Freezes on Hybrid Graphics Laptops (NVIDIA Optimus)"
    kind: issue
    author: "commandlinetips"
    date: "2025-11-08"
  - url: "https://github.com/omacom/omarchy/issues/12187"
    title: "Issue #12187: Update to 4.0.4: NVIDIA hybrid laptop hard-freezes ~5 s after login once linux-omarchy is the default kernel"
    kind: issue
    author: "Nord-Nogare"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/1776"
    title: "Issue #1776: Laptop / Hybrid GPU Power Management Issue (NVIDIA, iGPU + dGPU)"
    kind: issue
    author: "itsmedardan"
    date: "2025-09-18"
  - url: "https://github.com/omacom/omarchy/issues/12289"
    title: "Issue #12289: Hybrid AMD iGPU + NVIDIA dGPU with the external display on the dGPU: nvidia.lua exports NVIDIA VA-API while Aquamarine renders on the iGPU, and Omarchy never sets AQ_DRM_DEVICES"
    kind: issue
    author: "RajdeepVerma"
    date: "2026-09-17"
  - url: "https://omarchy.org/manual/troubleshooting/"
    title: "Omarchy manual: Troubleshooting"
    kind: manual
credits:
  - name: "mowgli42"
    url: "https://github.com/mowgli42"
    for: "Reported the dual-AMD login loop and traced it to Aquamarine splitting AQ_DRM_DEVICES on every colon, with the udev symlink pin that avoids it"
  - name: "Elshayib"
    url: "https://github.com/Elshayib"
    for: "Opened the session-environment sanitizer PR and the omarchy debug warning PR"
  - name: "slhuckstead"
    url: "https://github.com/slhuckstead"
    for: "Reproduced it on a muxless NVIDIA laptop and showed that snapshots on @home inherit the broken value, plus the colon-free udev symlink approach"
  - name: "christianjgilman"
    url: "https://github.com/christianjgilman"
    for: "Measured that an NVIDIA-first device order stops i915 GPU hangs on Optimus laptops driving externals from the dGPU"
  - name: "codyoss"
    url: "https://github.com/codyoss"
    for: "Documented that Aquamarine reads its env vars before Hyprland parses Lua, so the pin has to live in the session environment"
  - name: "seanymc85"
    url: "https://github.com/seanymc85"
    for: "Found that os.execute() could not report exit status inside Hyprland's Lua config on 4.0.0, so nvidia.lua silently set nothing until 4.0.1"
faq:
  - q: "Does Omarchy set AQ_DRM_DEVICES for me?"
    a: "No. We grepped the whole 4.0.4 tree and the string does not appear in bin/, default/, config/ or install/. If it is set on your machine, you, a guide, or an AI agent put it there. That is also what the triage comment on issue #8776 says."
  - q: "Will a Limine snapshot rollback fix it?"
    a: "Usually not. The value normally lives in ~/.config/uwsm, which is on the @home subvolume, and snapshots of the root subvolume do not revert it. slhuckstead makes this point on issue #8776: because the file sits on @home, each older snapshot in the Limine menu boots with the same bad pin."
  - q: "Can I just put the pin in hyprland.lua?"
    a: "Not reliably. Aquamarine reads AQ_DRM_DEVICES and AQ_NO_ATOMIC from the process environment before Hyprland parses any Lua, so hl.env() runs too late. Issue #9720 and PR #8786 both say so, and the #8776 report describes a Lua pin as sometimes late but often still applied, which is worse than a clean miss. Use ~/.config/uwsm/env.d instead."
related: [black-screen-after-login, nvidia-drivers-omarchy-4, login-loop-or-password-not-accepted-sddm, suspend-wont-resume-s2idle, multi-monitor-layout-not-saved]
draft: false
---

You have a laptop with two GPUs, you followed a multi-GPU guide (or an agent did), and now the machine shows a black screen and drops back to the login screen forever. Nothing in the UI tells you why. In the reports this page is built on, the cause is one environment variable with a colon in the wrong place.

## The fix

1. Get a text console. Press `Ctrl + Alt + F2`, and try `F3` through `F6` if that key does nothing. Log in there. The manual covers this under [Troubleshooting](https://omarchy.org/manual/troubleshooting/).

2. Find out whether anything sets the variable:

   ```bash
   grep -rn AQ_DRM_DEVICES ~/.config/uwsm/ ~/.config/hypr/ /etc/environment 2>/dev/null
   ```

   On 4.x, look hardest at `~/.config/uwsm/env.d/*`, `~/.config/uwsm/env-hyprland` and `~/.config/uwsm/default`. If you upgraded from 3.x, check `~/.config/uwsm/env.d/99-omarchy-upgrade-env` too: the Quattro upgrader moves the old `~/.config/uwsm/env` content into that file, so a 3.x pin comes along for the ride.

3. If the value contains a colon inside a device name, such as `/dev/dri/by-path/pci-0000:01:00.0-card`, delete the whole line. Do not try to escape or quote it. An unset variable is safe: Hyprland then picks a GPU on its own.

4. Reboot. On a muxless laptop that is usually the end of it.

5. Only if you actually need a specific GPU order, write a colon-free value. List the real nodes first:

   ```bash
   ls -l /dev/dri/by-path/
   readlink -f /dev/dri/by-path/pci-0000:01:00.0-card
   ```

   Then put the resolved node names, separated by a single colon, into a new file `~/.config/uwsm/env.d/50-gpu`:

   ```bash
   export AQ_DRM_DEVICES=/dev/dri/card1:/dev/dri/card0
   ```

   The first entry is the render-primary. On a hybrid machine list **both** cards. christianjgilman warns on issue #10350 that pinning only one GPU takes down every output wired to the other, and a reader of issue #1776 hit exactly that: after copying a one-card pin, the laptop stopped seeing any external monitor.

6. `cardN` numbers can move between boots. Both reporters on issue #8776 give each card a stable, colon-free name with a udev rule keyed on its PCI address, the same approach itsmedardan scripted for 3.x on issue #1776. Take the addresses and vendor IDs from `lspci -nn | grep -i vga`; the ones below are examples. Put the rule in `/etc/udev/rules.d/60-drm-names.rules`:

   ```udev
   SUBSYSTEM=="drm", KERNEL=="card[0-9]*", KERNELS=="0000:01:00.0", ATTRS{vendor}=="0x10de", SYMLINK+="dri/dgpu"
   SUBSYSTEM=="drm", KERNEL=="card[0-9]*", KERNELS=="0000:00:02.0", ATTRS{vendor}=="0x8086", SYMLINK+="dri/igpu"
   ```

   Then the pin reads `AQ_DRM_DEVICES=/dev/dri/dgpu:/dev/dri/igpu`, which no parser can mangle. Note the rule lives on the root subvolume while the env file lives on `/home`, so a snapshot restore can delete one and keep the other.

On 3.x the same variable belonged in `~/.config/uwsm/env`, which was a user-owned file. On 4.x that file was retired into `/usr/share/uwsm/env.d/10-omarchy`, and your overrides go in `~/.config/uwsm/env.d/`, which is what the manual FAQ chapter also tells you for other session variables.

## Verify it worked

Log in, then check what the compositor actually received:

```bash
tr '\0' '\n' < /proc/$(pgrep -x Hyprland | head -1)/environ | grep '^AQ_'
systemctl --user show-environment | grep '^AQ_'
```

Either both agree with what you wrote, or both are empty. Anything else means something in the session is still rewriting it.

Then confirm the old failure is gone:

```bash
journalctl -b | grep -iE 'found no gpus|CBackend::create'
```

That should return nothing. If you set an NVIDIA-first order deliberately, `nvidia-smi` is the check: christianjgilman reports Hyprland holding roughly 145 MiB of VRAM once it renders on the dGPU, against about 1 MiB before.

## Why it happens

Aquamarine, Hyprland's backend library, parses `AQ_DRM_DEVICES` by splitting on the `:` character. The triage on issue #8776 cites Aquamarine 0.14.0 doing this in `src/backend/drm/DRM.cpp`. A by-path name already contains two colons from the PCI address, so it is chopped into fragments, every fragment fails to resolve to a real file, and the explicit device list ends up empty. Once the variable exists at all, Aquamarine takes the explicit branch unconditionally and never falls back to automatic selection, so the result is fatal rather than degraded: `drm: Found no gpus to use, cannot continue`, then `CBackend::create() failed!`, then SDDM autologin restarts the whole cycle with nothing on screen.

The trap is that the Hyprland wiki's own detection step produces exactly that by-path string. Two unrelated machines hit this the same way in issue #8776, a dual-AMD desktop and a muxless MSI laptop, both because an AI agent followed the documented detection step and pasted the output into the documented variable.

Omarchy does not set the variable itself. We grepped the whole v4.0.4 source tree for `AQ_` and found nothing in `bin/`, `default/`, `config/` or `install/`. What Omarchy does ship for NVIDIA is `default/hypr/nvidia.lua`, which sets `NVD_BACKEND`, `LIBVA_DRIVER_NAME` and `__GLX_VENDOR_LIBRARY_NAME` when it detects an NVIDIA card. On 4.0.0 even those never landed: seanymc85 showed in issue #7755 that `os.execute()` inside Hyprland's Lua config always returns "No child processes", so every detection branch was skipped. The 4.0.1 release notes carry the fix (PR #6939), and `default/hypr/helpers.lua` in 4.0.4 reads an `OK` marker from `io.popen` instead of an exit status. The lesson survives the fix: anything Aquamarine needs at backend startup has to be in the session environment, not in Lua.

A second, rarer failure mode is ordering rather than syntax. On an Optimus laptop Hyprland's default render primary is normally the iGPU. When the external monitors hang off the dGPU, every frame needs a cross-GPU copy, and christianjgilman's issue #10350 shows that stalling i915 into a GPU hang that aborts the compositor: `Resetting rcs0 for preemption time out` followed by `context reset due to GPU hang`. Putting the NVIDIA node first fixed it there, verified over multi-hour use.

## If that did not work

- **The black screen started right after updating to 4.0.4, and you never touched any config.** That is likely the kernel change, not this. 4.0.4 makes `linux-omarchy` the default boot entry, and Nord-Nogare reports in issue #12187 that a hybrid laptop on the prebuilt `nvidia-open` package has no modules for it, so the desktop hard-freezes about five seconds after login. Omarchy's own installer uses `nvidia-open-dkms`, which builds against every installed kernel, so this bites machines where the prebuilt package was swapped in. Pick the stock `linux` entry in the Limine menu and boot that. See [/releases/v4.0.4/](/releases/v4.0.4/) and [/fix/nvidia-drivers-omarchy-4/](/fix/nvidia-drivers-omarchy-4/).
- **AMD Strix Point or Radeon 890M, black screen on a fresh install.** codyoss's issue #9720 reports Aquamarine failing its atomic commit with `Cannot allocate memory`. The reported workaround is `AQ_NO_ATOMIC=1` and `WLR_NO_HARDWARE_CURSORS=1`, again exported from the session environment, not Lua.
- **The machine boots fine, then freezes randomly 20 to 30 minutes in.** commandlinetips's issue #3242 pins that on NVIDIA runtime power management, fixed there with `options nvidia NVreg_DynamicPowerManagement=0x00` in `/etc/modprobe.d/` plus a udev rule forcing `power/control=on`, then `sudo mkinitcpio -P`.
- **Video is corrupted or the browser stutters, but nothing goes black.** That is the `LIBVA_DRIVER_NAME` family, not this one. Start at [/fix/chromium-flicker-hardware-acceleration/](/fix/chromium-flicker-hardware-acceleration/).
- **You are filing a report.** `omarchy debug` in 4.0.4 does not capture `AQ_DRM_DEVICES` at all, so paste the two commands from the verify section by hand. PR #9063 would add that dump and PR #8786 would sanitize the value at session-env load, but neither was merged as of 4.0.4, which is why this page says workaround rather than fixed.

Evidence for the ordering half of this page is thinner than for the colon half. The colon bug is confirmed against Aquamarine source in the triage comment on issue #8776 and reproduced on two machines. The NVIDIA-first ordering result is one careful report on one Pascal laptop, and its working line used the by-path form with colons, which did not loop that machine on Aquamarine 0.14.0. A later comment on issue #10350 from RajdeepVerma reports the same string fatal on Aquamarine 0.15.0, resolves it with `readlink -f` at session-environment time instead, and adds that with NVIDIA as primary his iGPU-driven internal panel needed `AQ_MGPU_NO_EXPLICIT=1` or its atomic commit failed with `Invalid argument` (issue #12289). One machine each, so treat both as leads, not rules.

## Related

- [Black screen after login](/fix/black-screen-after-login/) for the general decision tree
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Login loop or password not accepted (SDDM)](/fix/login-loop-or-password-not-accepted-sddm/)
- [Hardware: hybrid GPU](/hardware/hybrid-gpu/) and [Hardware: NVIDIA](/hardware/nvidia/)
- [Stuck at TTY or cannot switch TTY](/fix/stuck-at-tty-or-cannot-switch-tty/)
- Omarchy manual: [Troubleshooting](https://omarchy.org/manual/troubleshooting/) and [Monitors](https://omarchy.org/manual/monitors/)
