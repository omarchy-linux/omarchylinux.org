---
title: "Steam or Proton game crashes on launch"
description: "Steam and Proton games that die seconds after launch on Omarchy 4: the lib32 driver check, leftover SDL_VIDEODRIVER, and the gamescope launch option."
answer: "Almost always a driver or environment problem, not Hyprland. First run omarchy-install-gaming-gpu-lib32 so your 32-bit Vulkan driver matches your GPU, and confirm no NVIDIA userspace was installed on an AMD or Intel machine. Then check for a leftover SDL_VIDEODRIVER from Omarchy 3.x. If a single game still dies, wrap it in gamescope as a per-game Steam launch option."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: gaming
issueCount: 102
errorStrings:
  - "Failed to load steamui.so"
  - "libXtst.so.6: cannot open shared object file: No such file or directory"
  - "warning: SDL_VIDEODRIVER='wayland' does not allow fallback, use 'wayland,x11' instead"
tags: [steam, proton, gamescope, gaming, nvidia, lib32]
sources:
  - url: "https://github.com/omacom/omarchy/issues/3971"
    title: "Issue #3971: Steam/Proton games crash immediately on Hyprland - fix: gamescope"
    kind: issue
    author: "sebishogun"
    date: "2025-12-23"
  - url: "https://github.com/omacom/omarchy/issues/2564"
    title: "Issue #2564: Setting SDL_VIDEODRIVER=wayland as a default causes compatibility issues with Proton games"
    kind: issue
    author: "RyanBreaker"
    date: "2025-10-19"
  - url: "https://github.com/omacom/omarchy/issues/2466"
    title: "Issue #2466: Steam (intel) missing 32-bit deps"
    kind: issue
    author: "GyHUN95"
    date: "2025-10-15"
  - url: "https://github.com/omacom/omarchy/issues/8856"
    title: "Issue #8856: omarchy-install-gaming-steam pulls nvidia-utils onto non-NVIDIA systems"
    kind: issue
    author: "microfire21-og"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/9688"
    title: "Issue #9688: Hybrid Intel+NVIDIA laptops without supergfxctl: forced __GLX_VENDOR_LIBRARY_NAME=nvidia with no PRIME offload breaks Steam gaming"
    kind: issue
    author: "osungjinwoo"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/4016"
    title: "Issue #4016: Paradox native titles (HoI4, Stellaris) fail to launch after the first run"
    kind: issue
    author: "DarkiBoi"
    date: "2025-12-29"
  - url: "https://github.com/omacom/omarchy/issues/4595"
    title: "Issue #4595: Steam games (xwayland) won't fullscreen."
    kind: issue
    author: "JordanAnthonyKing"
    date: "2026-02-13"
  - url: "https://github.com/omacom/omarchy/issues/2870"
    title: "Issue #2870: Steam won't start"
    kind: issue
    author: "Luquatic"
    date: "2025-10-26"
  - url: "https://github.com/omacom/omarchy/issues/8373"
    title: "Issue #8373: /dev/uinput permissions not applied at boot, breaks Steam Input controller support in every game"
    kind: issue
    author: "DGBooth"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/9636"
    title: "Issue #9636: Screensaver fires over fullscreen Steam games every 150s: the idle_inhibit rule can never match a game"
    kind: issue
    author: "angel-ventura"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.7.0"
    title: "Omarchy v3.7.0 release notes: The Gaming Edition"
    kind: release
    date: "2026-05-04"
  - url: "https://omarchy.org/manual/gaming/"
    title: "Omarchy manual: Gaming"
    kind: manual
credits:
  - name: "RyanBreaker"
    url: "https://github.com/RyanBreaker"
    for: "Tracing Proton launch failures to the default SDL_VIDEODRIVER env"
  - name: "sebishogun"
    url: "https://github.com/sebishogun"
    for: "The gamescope launch-option writeup and the AMD lib32 package list"
  - name: "limehawk"
    url: "https://github.com/limehawk"
    for: "The LD_PRELOAD trick that keeps the Steam overlay alive under gamescope"
  - name: "microfire21-og"
    url: "https://github.com/microfire21-og"
    for: "Finding the installer ordering bug that puts NVIDIA userspace on AMD machines"
faq:
  - q: "Does Omarchy install gamescope for me?"
    a: "No. As of 4.0.4 the Steam installer only adds the steam package and GPU-matched lib32 drivers. A PR that would have bundled gamescope and gamemode was closed unmerged, so you install gamescope yourself if you want it."
  - q: "Is SDL_VIDEODRIVER still set on Omarchy 4?"
    a: "No. It is absent from default/hypr/envs.lua in v4.0.4 and from v3.8.4 before it. It was dropped in v3.7.0. If you still see it, it is coming from your own dotfiles or a stale uwsm session environment."
  - q: "My game flashes back to the desktop every couple of minutes but does not close. Is that a crash?"
    a: "Probably not. The Steam window rule inhibits idle for class steam only, and games run as steam_app_<appid>, so the screensaver fires over fullscreen games. That is issue 9636, still open on 4.0.x."
related: [nvidia-drivers-omarchy-4, hybrid-gpu-laptop-black-screen-aq-drm-devices, fractional-scaling-blurry-or-huge-apps, multi-monitor-layout-not-saved]
draft: false
---

Games that vanish two or three seconds after you press Play, with no window and no error dialog, are the single most common Steam complaint in the Omarchy tracker. The cause is almost never Hyprland itself. It is usually a 32-bit Vulkan driver that does not match your GPU, or an environment variable inherited from an older config.

Checked on v4.0.4 against the source snapshots for v3.8.4, v4.0.3 and v4.0.4.

## The fix

1. Confirm what you are running, so you know which advice applies.

   ```bash
   omarchy version
   ```

2. Install the 32-bit graphics libraries that match your actual GPU. Omarchy ships a script for this and it is GPU aware.

   ```bash
   omarchy-install-gaming-gpu-lib32
   ```

   This exists on both 3.x and 4.x. It picks `lib32-vulkan-intel`, `lib32-vulkan-radeon`, or the NVIDIA lib32 userspace based on detection, and it is the step most crash reports turn out to have skipped.

3. Check that you did not get NVIDIA userspace on a machine with no NVIDIA card. The Steam installer runs `omarchy-pkg-add steam` before the GPU-aware step, so pacman's `--noconfirm` provider pick can win the race and pull `lib32-nvidia-utils` plus `nvidia-utils` for Steam's `lib32-vulkan-driver` dependency. That is issue 8856, open as of 4.0.4.

   ```bash
   pacman -Qq | grep -E '^(lib32-)?nvidia'
   lspci | grep -iE 'VGA|3D|Display'
   ```

   If NVIDIA packages are present and no NVIDIA GPU is, remove them and reinstall the right driver:

   ```bash
   sudo pacman -Rns lib32-nvidia-utils nvidia-utils
   omarchy-install-gaming-gpu-lib32
   ```

   Reboot afterwards. The NVIDIA EGL vendor file outranks Mesa's until it is gone.

4. Look for a leftover `SDL_VIDEODRIVER`. Omarchy 3.x set `env = SDL_VIDEODRIVER,wayland` in `hypr/envs.conf`, and it broke a long list of Proton titles. It was removed in v3.7.0 and it is not in `default/hypr/envs.lua` on v4.0.4. But it survives in personal dotfiles and in an old session environment.

   ```bash
   grep -rn SDL_VIDEODRIVER ~/.config/hypr/ ~/.config/uwsm/ 2>/dev/null
   systemctl --user show-environment | grep -i sdl
   ```

   Delete any line you find, then log out and back in.

5. If one specific game still dies, set a per-game launch option. Right click the game in Steam, choose Properties, then Launch Options. Try the cheap one first:

   ```
   unset SDL_VIDEODRIVER; %command%
   ```

6. If that does not do it, wrap the game in gamescope. Omarchy does not install gamescope for you, so add it first:

   ```bash
   sudo pacman -S --needed gamescope
   ```

   Then use a launch option shaped like this, with your own resolution and refresh rate:

   ```
   env -u LD_PRELOAD gamescope -W 2560 -H 1440 -r 165 -f -- env LD_PRELOAD="$LD_PRELOAD" %command%
   ```

   The `LD_PRELOAD` dance matters. A plain `gamescope ... -- %command%` applies Steam's overlay library to gamescope instead of the game, which is why people report an invisible cursor and dead keyboard input inside the overlay. limehawk described that fix on issue 3971 and credited the ScopeBuddy project for the technique.

## Verify it worked

Launch the game from a terminal so you can see what Steam prints:

```bash
steam -console
```

Then check that the right driver is actually loaded:

```bash
vulkaninfo --summary | grep -i driverName
glxinfo -B | grep -i 'OpenGL renderer'
```

On an AMD or Intel machine you want Mesa drivers named there, not NVIDIA. If you are on a hybrid laptop, run `nvidia-smi` while the game is up and confirm the discrete GPU is actually doing work.

## Why it happens

Three separate problems produce the same symptom.

The historical one is `SDL_VIDEODRIVER`. Forcing SDL to a single backend removes its fallback chain, so any game whose SDL build cannot talk to Wayland exits instead of trying X11. RyanBreaker opened issue 2564 with a list of affected titles and pointed at the SDL documentation saying the auto-detection is the sane default. dhh first tried `wayland,x11`, which silenced the console warning but did not fix the crashes, and the variable was dropped entirely in the v3.7.0 "Gaming Edition" release.

The current one is driver mismatch. Steam's 32-bit runtime needs a lib32 Vulkan driver for your card. Issue 2466 showed Intel machines where every game reported a fatal error until `lib32-mesa` and `lib32-vulkan-intel` were added by hand. Issue 8856 shows the opposite failure, where NVIDIA userspace lands on an AMD laptop because of installer ordering.

The third is hybrid laptops. `default/hypr/nvidia.lua` on v4.0.4 sets `__GLX_VENDOR_LIBRARY_NAME=nvidia` session wide whenever an NVIDIA GPU with GSP firmware is detected, without consulting `omarchy-hw-hybrid-gpu`. There is no PRIME offload wrapper anywhere in the tree. Issue 9688 documents the result: the dGPU sits at zero percent while games freeze or crawl on the iGPU. That issue is open.

## If that did not work

- Native Linux builds that only launch once, such as the Paradox titles in issue 4016, are a game-side bug. Forcing Proton or running under gamescope is the reported workaround.
- Fullscreen flicker rather than an outright crash is issue 4595. Proton Experimental fixed it for one reporter. gamescope is the other option.
- If Steam itself never shows a window, that is a different failure. Check for `Failed to load steamui.so` and a missing `libXtst.so.6` in the console output, which was the upstream packaging break behind issue 2870 in October 2025.
- Controllers that Steam sees but games ignore are issue 8373, a `/dev/uinput` permission problem, not a crash.
- A game that seems to blink to the desktop every 150 seconds is the screensaver, not a crash. See issues 6947 and 9636.

Evidence for 4.x specifically is thinner than for 3.x. Most of the detailed crash reports predate Quattro, and the 4.0.x gaming issues in the tracker are about driver selection and idle handling rather than new crash causes.

## Related

- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Hybrid GPU laptop black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [NVIDIA hardware notes](/hardware/nvidia/) and [hybrid GPU notes](/hardware/hybrid-gpu/)
- [Omarchy manual: Gaming](https://omarchy.org/manual/gaming/)
