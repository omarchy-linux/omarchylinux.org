---
title: "Chromium flickers, plays black video, or loses hardware acceleration"
description: "Chromium flicker, black video, and dead hardware acceleration on Omarchy 4.x hybrid laptops: override LIBVA_DRIVER_NAME so VA-API stays on the GPU that drives your screen."
answer: "On a hybrid laptop whose screen runs off the integrated GPU, Omarchy points the whole session at the NVIDIA VA-API driver, so video decodes on the dGPU and fails to import on the iGPU. Add hl.env(\"LIBVA_DRIVER_NAME\", \"iHD\") (or \"radeonsi\" on AMD) to ~/.config/hypr/hyprland.lua, run systemctl --user set-environment with the same value, then restart the browser. Still open on 4.0.4."
appliesTo:
  from: "3.x"
status: workaround
category: apps
issueCount: 357
errorStrings:
  - "eglCreateImage failed with 0x00003009"
  - "OzoneImageBacking::ProduceSkiaGanesh failed to create GL representation"
  - "SharedImageManager::ProduceSkia: Trying to produce a Skia representation from an incompatible backing: OzoneImageBacking"
  - "vaEndPicture failed, VA error: internal decoding error"
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [chromium, hybrid-gpu, vaapi, nvidia, video, wayland]
sources:
  - url: "https://github.com/omacom/omarchy/issues/8215"
    title: "Issue #8215: 4.0.1: `shell_succeeds` fix enables NVDEC VAAPI routing on hybrid laptops with Intel-driven displays, corrupting browser video"
    kind: issue
    author: "SisyphusOfCorinth"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/4901"
    title: "Issue #4901: Hybrid Intel+NVIDIA: Chromium hardware acceleration requires manual workarounds"
    kind: issue
    author: "josefdc"
    date: "2026-03-04"
  - url: "https://github.com/omacom/omarchy/issues/7851"
    title: "Issue #7851: Don't force the NVIDIA VA-API driver on hybrid-GPU systems"
    kind: issue
    author: "Suzu1Dev"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8989"
    title: "Issue #8989: Hybrid iGPU-primary laptops: nvidia.lua forces NVIDIA env session-wide, video corruption (root cause of #4901) and blocked dGPU runtime suspend"
    kind: issue
    author: "karluiz"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/8726"
    title: "Issue #8726: Hybrid AMD+NVIDIA laptop: forcing LIBVA_DRIVER_NAME=nvidia breaks all hardware-decoded video (black video players)"
    kind: issue
    author: "ArghyaRanjanDas"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/9483"
    title: "Issue #9483: Only point the session at NVIDIA when NVIDIA is driving the screen"
    kind: issue
    author: "VykosMolt"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/8328"
    title: "Issue #8328: nvidia.lua forces LIBVA_DRIVER_NAME=nvidia on hybrid laptops where the dGPU drives no display"
    kind: issue
    author: "emshiarla"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/3899"
    title: "Issue #3899: Chromium GPU/Ozone errors after update to 3.2.3"
    kind: issue
    author: "GuilhermeNobre"
    date: "2025-12-16"
  - url: "https://github.com/omacom/omarchy/issues/5372"
    title: "Issue #5372: Brave/Chromium lock up and performance glitches"
    kind: issue
    author: "raybarrera"
    date: "2026-04-20"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/default/hypr/nvidia.lua"
    title: "default/hypr/nvidia.lua in v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
  - url: "https://omarchy.org/manual/browsers/"
    title: "Omarchy manual: Browsers"
    kind: manual
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "SisyphusOfCorinth"
    url: "https://github.com/SisyphusOfCorinth"
    for: "Traced the 4.0.1 regression to the shell_succeeds rewrite that finally let nvidia.lua fire"
  - name: "josefdc"
    url: "https://github.com/josefdc"
    for: "Found the GLVND EGL vendor priority half of the problem and the per-browser Mesa EGL wrapper"
  - name: "Suzu1Dev"
    url: "https://github.com/Suzu1Dev"
    for: "Proposed gating LIBVA_DRIVER_NAME on a sysfs hybrid-GPU detector"
  - name: "VykosMolt"
    url: "https://github.com/VykosMolt"
    for: "Proposed setting the NVIDIA session variables only when NVIDIA drives a connected display"
  - name: "Rookie0ne"
    url: "https://github.com/Rookie0ne"
    for: "Showed that libva picks the right driver on its own when the variable is unset"
  - name: "AharonG298"
    url: "https://github.com/AharonG298"
    for: "A/B measurements of nvidia versus iHD decode, and the systemctl --user set-environment tip"
faq:
  - q: "Do I need to reinstall or replace Chromium?"
    a: "No. Omarchy 4.x ships plain Arch Chromium, not a fork, and the same breakage shows up in Brave, Chrome, Helium and every Electron app on the affected machines. The fault is a session environment variable, not the package."
  - q: "Will disabling hardware acceleration in Chromium settings fix it?"
    a: "It stops the flicker, but you lose VA-API decode and GPU rasterization, and your fans will tell you. Overriding LIBVA_DRIVER_NAME keeps acceleration on the GPU that actually drives your screen."
  - q: "Is this fixed in 4.0.4?"
    a: "No. Issues 7851, 8215, 8726, 8989, 9483 and 8328 were all still open when this page was checked, and no 4.0.x release note mentions a change to nvidia.lua. The file is byte-identical from 4.0.0 through 4.0.4."
related: [hybrid-gpu-laptop-black-screen-aq-drm-devices, nvidia-drivers-omarchy-4, black-screen-after-login]
draft: false
---

If your browser flickers, shows a black rectangle where the video should be, or drops to software rendering, and you have a laptop with both an integrated GPU and an NVIDIA card, this is almost certainly one bug. Omarchy points the whole session at the NVIDIA VA-API driver whenever an NVIDIA GPU is present, even when your screen is driven by the integrated GPU. Video then decodes on the discrete card and cannot be imported for display on the integrated one.

## The fix

**1. Confirm you are affected.** In a terminal:

```bash
systemctl --user show-environment | grep -E 'LIBVA_DRIVER_NAME|NVD_BACKEND'
```

If that prints `LIBVA_DRIVER_NAME=nvidia` and your laptop panel is wired to the integrated GPU, you have it. Check which card owns the panel with:

```bash
for c in /sys/class/drm/card*-*/status; do echo "$c $(cat "$c")"; done
```

**2. Pick the right driver name.** Intel graphics from about Broadwell onwards use `iHD`. Older Intel generations use `i965`. An AMD integrated GPU uses `radeonsi`.

**3. On 4.0.0 through 4.0.4**, add one line at the bottom of `~/.config/hypr/hyprland.lua`, below the `require` lines. Your file loads after Omarchy's defaults, and the later `env` wins:

```lua
hl.env("LIBVA_DRIVER_NAME", "iHD")
```

**4. Apply it without logging out**, then restart the browser:

```bash
systemctl --user set-environment LIBVA_DRIVER_NAME=iHD
hyprctl reload
```

Apps launched through `uwsm-app`, which is how Omarchy starts your browser, inherit from the user systemd environment, so the `set-environment` call matters. An already running browser keeps its old environment until you close every window. Log out and back in if you want the clean version.

**On 3.x** the same variables were written once at install time into `~/.config/hypr/envs.conf` by the NVIDIA install step, as plain `env = LIBVA_DRIVER_NAME,nvidia` lines. Edit or delete the line there. Note that the `hyprland.conf` template shipped in later 3.x releases sources Omarchy's own `envs.conf`, not yours, so if your edit has no effect, put `env = LIBVA_DRIVER_NAME,iHD` at the bottom of `~/.config/hypr/hyprland.conf` instead.

**5. If video now plays but the window still flickers or goes black**, you have the second, separate half: Chromium rendering on the NVIDIA GPU while Hyprland composites on the integrated one. josefdc's fix in issue 4901 is a wrapper that forces Mesa EGL for the browser only:

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/chromium <<'EOF'
#!/bin/bash
export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/50_mesa.json
export LIBVA_DRIVER_NAME=iHD
exec /usr/bin/chromium "$@"
EOF
chmod +x ~/.local/bin/chromium
```

Do not export `__EGL_VENDOR_LIBRARY_FILENAMES` session wide. josefdc reports Hyprland then fails to initialise EGL at startup and you recover from a TTY.

To make launchers use the wrapper, copy `/usr/share/applications/chromium.desktop` to `~/.local/share/applications/` and point `Exec` at the absolute path of the wrapper. Keep the first word of `Exec` a real program: `omarchy-launch-browser` reads that first token out of the desktop file, so an `Exec=env VAR=x /usr/bin/chromium` line makes `Super + Shift + Return` do nothing. rvalue reported exactly that on issue 4901.

**6. The blunt fallback.** Adding `--disable-gpu-compositing` to `~/.config/chromium-flags.conf` stops the corruption on every machine in these threads, at the cost of software compositing and the fan noise that comes with it. The equivalent files are `~/.config/brave-flags.conf`, `~/.config/chrome-flags.conf` and `~/.config/microsoft-edge-stable-flags.conf`. Brave Origin reads `~/.config/brave-origin-flags.conf` and nothing else, which is why the workaround looks like it failed if you only edited Brave's file.

## Verify it worked

```bash
vainfo | grep 'Driver version'
```

You want `Intel iHD driver` or the Mesa Gallium line for radeonsi, not `VA-API NVDEC driver`.

Then open `chrome://gpu`. Video Decode and Compositing should both read "Hardware accelerated". For a live test, scroll a feed with autoplaying video, which is where most reporters first saw it, or open an incoming Discord stream, which CompleteDotTech used as a regression test on 4.0.2. If you want the decoder's own account, launch with `chromium --vmodule=*vaapi*=2` and watch for a repeating `vaEndPicture failed` construct and teardown loop. That loop disappearing is the signal.

## Why it happens

`default/hypr/nvidia.lua` sets `NVD_BACKEND=direct`, `LIBVA_DRIVER_NAME=nvidia` and `__GLX_VENDOR_LIBRARY_NAME=nvidia` whenever a GSP-era NVIDIA GPU is detected. The detector asks whether such a card exists, not whether it drives a screen. `autostart.lua` then exports the session environment with `systemctl --user import-environment`, so every app inherits it. On a hybrid laptop each frame is decoded on the NVIDIA card and imported into an integrated GPU GL context as a DMA-BUF, which fails with `EGL_BAD_MATCH`. karluiz traced that chain in issue 8989, and ArghyaRanjanDas showed the same failure with an AMD integrated GPU, where radeonsi cannot import NVIDIA vendor modifiers.

The reason this arrived as a 4.0.1 regression, with nothing GPU related in the release notes, is subtler. `nvidia.lua` is byte-identical from 4.0.0 to 4.0.4, which I checked against the tagged sources. What changed in 4.0.1 was `o.shell_succeeds` in `default/hypr/helpers.lua`, rewritten from `os.execute` to `io.popen` with an `OK` marker because Hyprland reaps its own children and swallows exit statuses. That repair made the NVIDIA detector actually fire for the first time. SisyphusOfCorinth documented the attribution, and AharonG298 confirmed it independently through the edge channel.

Rookie0ne added a useful correction: libva is not the problem. With the variable unset it picks the right driver per render node on its own.

The second half is GLVND. NVIDIA's EGL vendor file has priority 10 against Mesa's 50, so Chromium loads NVIDIA EGL by default, which is why the rendering side needs its own override.

## If that did not work

- **Single-GPU NVIDIA desktop.** This is a different problem. Issue 5372 tracks lockups on media-heavy pages with `NVRM: dmaAllocMapping_GM107: can't alloc VA space for mapping` in the journal, and it is still open with no accepted fix.
- **Still on 3.x with `SharedImageManager` and `eglCreateImage` spam.** That is issue 3899, and its reporter said the problem cleared on 3.4.0, which also carried Chromium Wayland colour manager flag changes. Update before you chase flags, and see [upgrading 3 to 4](/upgrade/3-to-4-quattro/).
- **Your flags vanished after an update.** `omarchy refresh chromium` overwrites `~/.config/chromium-flags.conf` with the Omarchy default and leaves your old file as `~/.config/chromium-flags.conf.bak.<timestamp>`.
- **Browser version matters.** daedalus-codes needed `--disable-gpu-compositing` on Brave 1.94 and Chromium 152 on hardware where 1.93.138 was fine without it. If a browser update broke a previously working setup, that is a plausible cause.
- **Every app is black, not just the browser.** Then this is not your bug. Start at [hybrid GPU black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/).

Evidence for the workaround is strong: four separate hardware pairings in these threads, with before and after measurements. Evidence that any 4.0.x release fixed it is absent.

## Related

- [Hybrid GPU laptop black screen](/fix/hybrid-gpu-laptop-black-screen-aq-drm-devices/)
- [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/)
- [Hybrid GPU hardware notes](/hardware/hybrid-gpu/)
- [Intel GPU hardware notes](/hardware/intel-gpu/)
- [Still broken on the latest release](/releases/still-broken/)
- [Omarchy manual: Browsers](https://omarchy.org/manual/browsers/)
