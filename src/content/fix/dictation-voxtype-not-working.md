---
title: "Voxtype dictation not working on Omarchy"
description: "F9 and Super + Ctrl + X do nothing, Voxtype crashes, or the model never loads. The install check, the CPU baseline, the GPU symlink, and the mic."
answer: "Run `command -v voxtype` first. If it is missing, install from the Omarchy menu under Install > AI > Dictation. If it is present but the keys do nothing, run `voxtype setup check` and `systemctl --user status voxtype`. The three common faults on Omarchy 4 are a CPU without AVX2 (SIGILL), a GPU backend that never got enabled because the installer omits sudo, and the input group being dropped by a 4.0.2 migration."
appliesTo:
  from: "3.x"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: apps
issueCount: 36
errorStrings:
  - "bash: line 1: voxtype: command not found"
  - "FATAL: Illegal CPU instruction (SIGILL)"
  - "Error: Failed to remove existing /usr/bin/voxtype (need sudo?): Permission denied (os error 13)"
  - "WARN playerctl not found or failed to run: No such file or directory (os error 2)"
  - "ERROR Hotkey listener error: No keyboard device found in /dev/input/"
  - "ggml_vulkan: device Vulkan0 does not support 16-bit storage."
  - "ERROR: voxtype-bin is not available for the 'aarch64' architecture."
tags: [voxtype, dictation, speech-to-text, quattro, keybindings]
sources:
  - url: "https://github.com/omacom/omarchy/issues/7883"
    title: "Issue #7883: Dictation installer offers AVX2-only Voxtype on CPUs without AVX2"
    kind: issue
    author: "t0d0r"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/8312"
    title: "Issue #8312: Dictation (Voxtype) leaves broken install on CPUs without AVX2 instead of failing gracefully"
    kind: issue
    author: "ironbract"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/11110"
    title: "Issue #11110: voxtype install silently leaves the CPU backend: 'voxtype setup gpu --enable' runs without sudo"
    kind: issue
    author: "RonildoBraga"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/7099"
    title: "Issue #7099: Voxtype does not symlink to voxtype-vulkan on Vulkan enabled system"
    kind: issue
    author: "sgruendel"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/11370"
    title: "Issue #11370: Voxtype install enables Vulkan on Haswell (hasvk) GPUs, causing an endless SIGABRT crash loop"
    kind: issue
    author: "llyorshch"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/12013"
    title: "Issue #12013: Migration 1787865477 drops the input group, silently breaking Voxtype's evdev hotkey"
    kind: issue
    author: "kurenn"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/9243"
    title: "Issue #9243: Voxtype pause_media silently fails: playerctl not installed by omarchy-voxtype-install"
    kind: issue
    author: "montanasnow"
    date: "2026-08-30"
  - url: "https://github.com/omacom/omarchy/issues/7135"
    title: "Issue #7135: Quattro removes playerctl while default Voxtype config requires it"
    kind: issue
    author: "skinandbones"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/8530"
    title: "Issue #8530: Dictation installer offers x86-only voxtype-bin on Apple Silicon, making Voxtype uninstallable"
    kind: issue
    author: "twitchax"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/11749"
    title: "Issue #11749: Dictation installer and menu check for voxtype-bin instead of the voxtype command"
    kind: issue
    author: "cristim"
    date: "2026-09-13"
  - url: "https://github.com/omacom/omarchy/issues/5882"
    title: "Issue #5882: F9 should not be bound to Voxtype dictation by default. Bare function keys must not be rebound."
    kind: issue
    author: "r3quie"
    date: "2026-05-16"
  - url: "https://github.com/omacom/omarchy/issues/4159"
    title: "Issue #4159: Voxtype keybinding sequence"
    kind: issue
    author: "pomartel"
    date: "2026-01-08"
  - url: "https://github.com/omacom/omarchy/issues/7900"
    title: "Issue #7900: Dictation indicator opens the config instead of toggling dictation, unlike every other indicator"
    kind: issue
    author: "projmans"
    date: "2026-08-23"
  - url: "https://github.com/omacom/omarchy/issues/6823"
    title: "Issue #6823: Dictation bar icon errors when voxtype isn't installed (missing guard in click handler)"
    kind: issue
    author: "brwaters"
    date: "2026-08-13"
  - url: "https://github.com/omacom/omarchy/issues/10050"
    title: "Issue #10050: Default Voxtype type mode can corrupt longer Japanese/CJK dictation through wtype"
    kind: issue
    author: "komagata"
    date: "2026-09-03"
  - url: "https://github.com/omacom/omarchy/pull/7129"
    title: "PR #7129: Fix Voxtype GPU setup failing silently"
    kind: pr
    author: "sgruendel"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/pull/7890"
    title: "PR #7890: Reject Voxtype on CPUs without AVX2"
    kind: pr
    author: "kx0101"
    date: "2026-08-23"
  - url: "https://omarchy.org/manual/text-extraction-dictation/"
    title: "Omarchy manual: Text Extraction and Dictation"
    kind: manual
credits:
  - name: "RonildoBraga"
    url: "https://github.com/RonildoBraga"
    for: "Traced the silent CPU fallback to the missing sudo on voxtype setup gpu --enable"
  - name: "kurenn"
    url: "https://github.com/kurenn"
    for: "Found that migration 1787865477 removes the input group and kills Voxtype's own evdev hotkey"
  - name: "montanasnow"
    url: "https://github.com/montanasnow"
    for: "Showed that pause_media is inert because playerctl is never installed"
  - name: "llyorshch"
    url: "https://github.com/llyorshch"
    for: "Diagnosed the Haswell Vulkan crash loop and the setup gpu --disable workaround"
  - name: "r3quie"
    url: "https://github.com/r3quie"
    for: "Documented the unbind for the default F9 binding"
faq:
  - q: "Why do F9 and Super + Ctrl + X do nothing at all?"
    a: "Both bindings live in a block guarded by `o.cmd_present(\"voxtype\")`. If the voxtype binary is not on PATH, Hyprland never registers them and the keys fall through to the focused app. Check with `command -v voxtype` before touching any config."
  - q: "How do I change which Whisper model Voxtype uses?"
    a: "Run `voxtype setup model` in a terminal, or `omarchy voxtype model`, which opens the same thing in a floating terminal and restarts the shell afterwards. The default that Omarchy installs is base.en, about 150MB. The model is also settable directly in ~/.config/voxtype/config.toml under [whisper]."
  - q: "Can I use dictation on an older laptop without AVX2?"
    a: "Not with the packaged voxtype-bin as of 4.0.4. Every variant in the package targets AVX2 or newer, so the binary dies with SIGILL on pre-Haswell CPUs. Voxtype's maintainer has said pre-AVX2 binaries are planned for a later release."
  - q: "Dictation works but my music keeps playing. Is that a bug?"
    a: "Yes, on voxtype-bin 0.7.5. The shipped config sets pause_media = true, but that path shelled out to playerctl, which Omarchy 4 does not install. Voxtype 1.0.0 replaced it with a direct D-Bus call, so upgrading the package fixes it."
related: [custom-keybindings-lost-after-quattro, quickshell-crashes-or-bar-missing, no-sound-from-laptop-speakers, hyprland-lua-attempt-to-index-nil-global-o]
draft: false
---

Dictation on Omarchy is [Voxtype](https://voxtype.io/), installed on demand rather than shipped with the system. "Dictation is not working" turns out to be five separate faults with the same symptom, so work through them in order. Everything below was checked against the v4.0.4 source tree and against v3.8.4 for the 3.x differences.

## The fix

**1. Confirm Voxtype is actually installed.**

```bash
command -v voxtype
```

If that prints nothing, the keys were never bound. Omarchy 4 defines its dictation bindings in `default/hypr/bindings/voxtype.lua` inside a `o.cmd_present("voxtype")` guard, so with no binary there is no `F9` and no `Super + Ctrl + X`. Install it from the Omarchy menu under **Install > AI > Dictation**, or run `omarchy voxtype install`. On 3.x the same bindings lived in `default/hypr/bindings/utilities.conf` and were unconditional, so on 3.x the keys existed but did nothing.

**2. Check your CPU before you install anything.**

```bash
grep -o avx2 /proc/cpuinfo | head -1
```

If that prints nothing, stop. The packaged `voxtype-bin` ships only AVX2 and AVX-512 builds, and `/usr/bin/voxtype` points at the AVX2 one, so it aborts with `FATAL: Illegal CPU instruction (SIGILL)` on every run. The installer does not check, so you end up with a package that can never work. This is reported in issue #7883 and issue #8312, both still open on 4.0.4. PR #7890 would add a pre-flight refusal but has not merged.

**3. If the install "succeeded" but transcription is glacial, fix the GPU symlink.**

```bash
ls -la /usr/bin/voxtype
sudo voxtype setup gpu --enable
systemctl --user restart voxtype
```

`omarchy-voxtype-install` runs `voxtype setup gpu --enable` as your user, which cannot rewrite the root-owned symlink. The failure line is swallowed by a trailing `|| true`, so the install still reports success and still shows the "Voxtype Dictation Ready" notification. Reported in issue #7099 and issue #11110; PR #7129 is open.

**4. If Voxtype crash-loops instead, disable the GPU backend.**

```bash
sudo voxtype setup gpu --disable
systemctl --user restart voxtype
```

Omarchy enables Vulkan whenever any ICD file exists, which is not the same as the device being usable. On Haswell-era Intel graphics using the `hasvk` driver, the daemon aborts at model load and systemd restarts it every five seconds. Issue #11370 reports roughly 127,000 core dumps from this loop.

**5. If you use Voxtype's own hotkey rather than the Hyprland bindings, rejoin the input group.**

```bash
voxtype setup check
sudo usermod -aG input $USER
```

Log out and back in afterwards. Migration `1787865477.sh` in 4.0.2 removes the blanket `input` group grant, keeping it only for xpadneo or ydotool users. Voxtype's evdev listener reads `/dev/input/event*` directly, so it loses access and logs `No keyboard device found in /dev/input/` while otherwise looking healthy. Found by kurenn in issue #12013. Omarchy's shipped configuration does not regress here, because it ships `[hotkey] enabled = false` and binds through the compositor instead.

**6. Check the microphone and the model.**

```bash
pactl list sources short
systemctl --user status voxtype
journalctl --user -u voxtype -n 50
```

Voxtype's `[audio] device` defaults to `default`, so it follows your system input. If the wrong source is picked up, set the device name from `pactl list sources short` in `~/.config/voxtype/config.toml`. Model problems show up in the journal at load time; re-run `voxtype setup model` or `omarchy voxtype model` to re-download.

## Verify it worked

Open a text editor, hold `F9`, say a sentence, release. The text should land at the cursor. The bar indicator switches from the inactive mic glyph to a recording glyph, then to a timer glyph while transcribing.

Two things that are not proof of failure. Clicking the Dictation indicator opens the Voxtype config rather than toggling dictation. That is what `shell/plugins/bar/indicators/Dictation.qml` does on 4.0.4, and the shell test fixture asserts it, even though the manual's top bar chapter says clicking an indicator toggles that mode. Issue #7900 is open on the mismatch. And if Voxtype is not installed, clicking the same glyph opens a terminal that prints `voxtype: command not found` instead of offering to install, per issue #6823.

For the GPU case, `ls -la /usr/bin/voxtype` should now point at `voxtype-vulkan`, and the journal should show a Vulkan device at model load.

## Why it happens

Omarchy treats dictation as an optional add-on wired together by one short script. `omarchy-voxtype-install` adds `wtype` and `voxtype-bin`, copies the packaged `config.toml` into `~/.config/voxtype/`, downloads a model, optionally enables the GPU, and registers the systemd user service. Almost every failure above is a missing guard in that sequence rather than a bug in Voxtype itself.

The installer never checks the CPU baseline, never checks the architecture, and never checks whether the Vulkan device can run ggml. It also runs the one step that needs root without root. Because each of those steps ends in `|| true` or simply is not there, the script finishes cleanly and the notification claims dictation is ready.

The menu and the installer key off the package name `voxtype-bin` while the keybindings key off the `voxtype` command. On Apple Silicon `voxtype-bin` is `arch=('x86_64')` and cannot install at all, so the first-run invitation notification pushes users toward a flow that always fails. Issue #8530 covers the Apple Silicon dead end and issue #11749 covers the package-versus-command mismatch, including the case where an AUR-built `voxtype` works but Omarchy still reports dictation as not installed.

## If that did not work

**Keys fire while text is being typed.** Releasing `Super` last after `Super + Ctrl + X` makes the transcription arrive as a burst of modifier combinations. Issue #4159 collects workarounds using a Hyprland submap that swallows modifiers during output; the maintainer has said upstream hooks are the intended solution. The simplest avoidance is to dictate with bare `F9`.

**F9 collides with your editor.** It is bound by default. Add `hl.unbind("F9")` to your Lua config on 4.x, or `unbind = , F9` on 3.x, as r3quie noted in issue #5882.

**Media does not pause.** On `voxtype-bin` 0.7.5 the `pause_media` default shells out to `playerctl`, which Quattro removed and the installer never adds. Issues #7135 and #9243 both record `playerctl not found or failed to run` in the journal. Voxtype 1.0.0 switched to a D-Bus call, so upgrading the package is the fix the maintainer recommends over reinstalling `playerctl`.

**CJK text arrives corrupted.** Switch `[output] mode` away from `type` in `~/.config/voxtype/config.toml`. Issue #10050 traces this to how `wtype` assigns characters to temporary keycodes, which some clients read as physical keys.

**Pre-AVX2 hardware.** There is no supported path on 4.0.4. Voxtype's maintainer has said pre-AVX2 binaries are coming in a later Voxtype release.

## Related

- Manual chapter: [Text Extraction and Dictation](https://omarchy.org/manual/text-extraction-dictation/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [Quickshell crashes or bar missing](/fix/quickshell-crashes-or-bar-missing/)
- [Audio hardware notes](/hardware/audio/)
- [Apple Silicon Macs](/hardware/apple-silicon-macs/)
