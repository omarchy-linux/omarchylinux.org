---
title: "Touchpad, keyboard and input on Omarchy"
description: "What the touchpad and keyboard stack does on Omarchy 4.x: the defaults in input.lua, the quirk scripts, the i2c-hid failures that break pads, and the fix order."
answer: "On Omarchy 4.0.4 most touchpads and keyboards work with no setup: libinput handles them and defaults live in ~/.config/hypr/input.lua. Breakage is usually an i2c-hid probe or resume failure, so run `omarchy restart trackpad` first, then A/B boot the stock linux kernel. Omarchy's own touchpad toggle misses pads whose device name lacks touchpad or trackpad."
appliesTo:
  from: "4.0.0"
status: info
kind: component
componentKey: "touchpad-input"
issueCount: 541
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
tags: [touchpad, keyboard, libinput, i2c-hid, input, laptop]
sources:
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://github.com/omacom/omarchy/issues/12181"
    title: "Issue #12181: linux-omarchy 7.2.5-3: SynPS/2 Synaptics touchpad completely vanishes from kernel (works on stock linux 7.2.3)"
    kind: issue
    author: "CloudWalker025"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12136"
    title: "Issue #12136: Surface Laptop Studio 2: offer an opt-in linux-surface touchpad profile"
    kind: issue
    author: "Andre1Becker"
    date: "2026-09-16"
  - url: "https://github.com/omacom/omarchy/issues/12029"
    title: "Issue #12029: omarchy-hw-touchpad returns the wrong device when an external trackpad is connected"
    kind: issue
    author: "alebak"
    date: "2026-09-15"
  - url: "https://github.com/omacom/omarchy/issues/11245"
    title: "Issue #11245: Kernel 7.2.3 (shipped in 4.0.3): ELAN i2c-hid touchpad intermittently freezes, A/B confirmed vs linux-lts"
    kind: issue
    author: "gitickle"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/11128"
    title: "Issue #11128: Keyboard/touchpad dead at LUKS prompt on AMD Surface devices (fix-surface-keyboard.sh only handles pinctrl/Intel)"
    kind: issue
    author: "gs86baker"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10924"
    title: "Issue #10924: ASUS Zenbook UM3406KA touchpad stops responding after s2idle resume"
    kind: issue
    author: "ottosilva"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/10815"
    title: "Issue #10815: T2 Macbook Pro Trackpad disable_while_typing setting not working"
    kind: issue
    author: "djfergus"
    date: "2026-09-08"
  - url: "https://github.com/omacom/omarchy/issues/10449"
    title: "Issue #10449: Stock XF86TouchpadToggle binding never fires (Hyprland resolve_binds_by_sym defaults to false)"
    kind: issue
    author: "mlusetti"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/9658"
    title: "Issue #9658: Trackpad (MSFT0001 I2C Precision Touchpad) fails to bind at boot due to i2c_designware controller timeout"
    kind: issue
    author: "vashizm0r"
    date: "2026-09-01"
  - url: "https://github.com/omacom/omarchy/issues/9389"
    title: "Issue #9389: Update > Hardware > Trackpad silently no-ops on Apple bcm5974 trackpads"
    kind: issue
    author: "cmyk"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/9347"
    title: "Issue #9347: Huawei BOD-WXX9 (Goodix GXTP7863 27C6:01E0): touchpad ignores all input on a fresh install"
    kind: issue
    author: "SemihMutlu07"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/8376"
    title: "Issue #8376: omarchy-hw-touchpad misses Apple Touch (MTP) trackpads, so omarchy-toggle-touchpad silently does nothing"
    kind: issue
    author: "GonzFC"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/issues/7010"
    title: "Issue #7010: [Quattro] Touchpad gets disabled everytime I close the laptop lid"
    kind: issue
    author: "ReetamBG"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/6935"
    title: "Issue #6935: Touchpad right-click stops working after 4.0 update"
    kind: issue
    author: "ohai89"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/pull/8281"
    title: "PR #8281: Detect touchpads by udev type when the name has no touchpad in it"
    kind: pr
    author: "Cozidian"
    date: "2026-08-26"
  - url: "https://github.com/omacom/omarchy/pull/10577"
    title: "PR #10577: Enable resolve_binds_by_sym for high XF86 keycodes"
    kind: pr
    author: "fresh3nough"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/2415"
    title: "Issue #2415: Intel based Macbook keyboard doesn't respond on installation"
    kind: issue
    author: "foretoo"
    date: "2025-10-12"
  - url: "https://github.com/omacom/omarchy/issues/1954"
    title: "Issue #1954: MacBook8,1: built-in keyboard/trackpad not working (applespi timeouts)"
    kind: issue
    author: "jpumfrey"
    date: "2025-09-26"
  - url: "https://github.com/omacom/omarchy/issues/2054"
    title: "Issue #2054: Can't switch between keyboard layouts. Stuck on Russian."
    kind: issue
    author: "antonavy"
    date: "2025-09-29"
credits:
  - name: "ohai89"
    url: "https://github.com/ohai89"
    for: "Showed that leaving clickfinger_behavior unset in the migrated Lua config kills right-click entirely"
  - name: "ReetamBG"
    url: "https://github.com/ReetamBG"
    for: "Traced the lid-close touchpad disable to an HP firmware KEY_TOUCHPAD_OFF scancode hitting the stock bind"
  - name: "mlusetti"
    url: "https://github.com/mlusetti"
    for: "Proved the stock XF86Touchpad binds never fire because resolve_binds_by_sym is off"
  - name: "GonzFC"
    url: "https://github.com/GonzFC"
    for: "Found that omarchy-hw-touchpad matches on device name, so Apple MTP pads are invisible to the toggle"
  - name: "ottosilva"
    url: "https://github.com/ottosilva"
    for: "Documented the i2c_hid_acpi resume failure and the scoped unbind/rebind sleep hook that fixes it"
  - name: "matthiasjg"
    url: "https://github.com/matthiasjg"
    for: "Root-caused the MacBook8,1 applespi timeouts to the DesignWare DMA engine and published a working setup"
faq:
  - q: "Where do I change touchpad settings on Omarchy 4?"
    a: "In ~/.config/hypr/input.lua, reachable from the Omarchy menu under Setup > Input. The 3.x file was ~/.config/hypr/input.conf and the 4.0 migration converted it. Anything you set there replaces Omarchy's defaults, so a setting you leave commented out is unset, not defaulted."
  - q: "Why does my touchpad toggle key do nothing?"
    a: "Two separate bugs. Hyprland's input:resolve_binds_by_sym defaults to false, so the stock XF86TouchpadToggle bind never matches (issue #10449). And omarchy-hw-touchpad only matches devices whose Hyprland name contains touchpad or trackpad, so on other pads the toggle exits with an error nobody sees (issue #8376)."
  - q: "Are touchpad gestures set up by default?"
    a: "No. The gesture lines in config/hypr/input.lua ship commented out. Add hl.gesture({ fingers = 3, direction = \"horizontal\", action = \"workspace\" }) yourself. The old 3.x gestures:workspace_swipe block does not exist in current Hyprland."
related: [suspend-wont-resume-s2idle, custom-keybindings-lost-after-quattro, layouts-and-locale, t2-mac, microsoft-surface]
draft: false
---

Input is the part of Omarchy that either disappears into the background or ruins your day. On most laptops the touchpad and keyboard just work, because libinput and the kernel do the work and Omarchy only sets a handful of defaults. When it breaks, the cause is almost always below Omarchy: an i2c-hid controller that times out, a kernel regression, or Apple firmware. Everything below was checked against the v4.0.4 source tree and against issues filed on 4.0.x. The manual chapter is [Keyboard, Mouse, Trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/).

## Status on 4.0.4

Good for most hardware. Of the 541 issues that mention touchpads, keyboards, libinput or gestures, the current 4.x failures cluster into four groups: i2c-hid pads that fail to probe at boot or fail to resume, Omarchy's own touchpad tooling missing devices it should match, Intel Macs and Surface machines with no input at the LUKS prompt, and fresh regressions from the bespoke `linux-omarchy` kernel that 4.0.4 made the default for everyone.

That last group is new and worth watching. On an Alienware m15 Ryzen Edition R5, `linux-omarchy` 7.2.5-3 makes the SynPS/2 Synaptics pad vanish from `/proc/bus/input/devices` entirely, while stock `linux` 7.2.3 on the same machine enumerates it fine (issue #12181). If your pad died the day you took 4.0.4, suspect the kernel before anything else.

## What Omarchy does automatically

The defaults live in `default/hypr/input.lua` and are short. Keyboard layout and variant are read out of `/etc/vconsole.conf` at reload time. If the layout cannot type Latin letters, Omarchy prepends `us` and adds `grp:alts_toggle` so Left Alt plus Right Alt switches, because Hyprland resolves keybindings against the first layout only. Caps Lock becomes the compose key, and both Shift keys together give you Caps Lock back with a self-cancelling variant. Repeat rate is 40 with a 250 ms delay, and numlock starts on.

For the pad itself the defaults are `natural_scroll = false`, `clickfinger_behavior = true`, and `scroll_factor = 0.4`, plus per-app scroll multipliers for Alacritty, kitty, foot and Ghostty. Gestures are not enabled: the `hl.gesture` examples in `config/hypr/input.lua` ship commented out.

At install time `install/hardware/all.sh` runs several input quirk scripts:

- `fix-fkeys.sh` writes `options hid_apple fnmode=2` so F keys on Apple-style keyboards stay F keys.
- `fix-synaptic-touchpad.sh` loads `psmouse` with `synaptics_intertouch=1` when `/proc/bus/input/devices` names a Synaptics pad. It is deliberately not persisted to `/etc/modprobe.d`, and it was made non-fatal after it took whole installs down during `arch-chroot`.
- `dell-xps-touchpad-haptics.sh` installs the haptics helper when `omarchy-hw-dell-xps-haptic-touchpad` matches an XPS with the i2c device `VEN_06CB:00`. You then get Trigger > Hardware > Touchpad Haptics with low, mid and high.
- `asus/fix-asus-ptl-b9406-touchpad.sh` drops a libinput quirk masking the pressure axes on the ExpertBook B9406 Pixart pad, whose 0 to 1 pressure values make libinput discard every motion event as a touch jump.
- `asus/fix-z13-touchpad.sh` adds a udev rule marking the ROG Flow Z13 detachable keyboard's pad as internal so disable-while-typing can pair with the keyboard.
- `apple/fix-spi-keyboard.sh` installs `macbook12-spi-driver-dkms` and the right mkinitcpio `MODULES` line for MacBook8,1 through MacBookPro14,x.
- `fix-surface-keyboard.sh` writes a Surface aggregator module list into the initramfs so the keyboard works before decryption.
- `framework/qmk-hid.sh` adds the udev rule for Framework 16 keyboard RGB control.

Three helper commands matter day to day. `omarchy-hw-touchpad` prints the detected pad by matching `hyprctl devices` names against `touchpad|trackpad`. `omarchy toggle touchpad` enables or disables it and, since migration `1787618700`, persists the device name as plain data rather than generated Lua. `omarchy restart trackpad` unbinds and rebinds every `i2c_hid_acpi` device, then reloads `intel_quicki2c` if present.

## Known problems

| Issue | Models | Status | Fixed in |
| --- | --- | --- | --- |
| [#12181](https://github.com/omacom/omarchy/issues/12181) PS/2 pad absent under linux-omarchy 7.2.5-3 | Alienware m15 Ryzen R5, SynPS/2 pads | open | not fixed |
| [#11245](https://github.com/omacom/omarchy/issues/11245) ELAN i2c-hid pad freezes for seconds on kernel 7.2.3 | Acer Nitro 5, Intel LPSS | open | not fixed |
| [#10924](https://github.com/omacom/omarchy/issues/10924) i2c_hid_acpi fails to resume after s2idle | ASUS Zenbook UM3406KA | open | workaround only |
| [#9658](https://github.com/omacom/omarchy/issues/9658) i2c_designware times out at boot, no pad created | Lenovo 21DM convertible | open | workaround only |
| [#9347](https://github.com/omacom/omarchy/issues/9347) Goodix GXTP7863 probe fails with -110 | Huawei MateBook D BOD-WXX9 | open | not fixed |
| [#6935](https://github.com/omacom/omarchy/issues/6935) right-click dead when clickfinger_behavior is unset | any install upgraded to 4.0 | open | workaround only |
| [#10449](https://github.com/omacom/omarchy/issues/10449) XF86TouchpadToggle bind never fires | any laptop with a touchpad Fn key | open | PR #10577 open |
| [#8376](https://github.com/omacom/omarchy/issues/8376) toggle no-ops when the device name lacks touchpad or trackpad | Apple MTP and bcm5974, Pixelbook, Synaptics TM3053 and TM3096 | open | PR #8281 open |
| [#12029](https://github.com/omacom/omarchy/issues/12029) an external pad shadows the internal one | any laptop plus a Magic Trackpad | open | not fixed |
| [#7010](https://github.com/omacom/omarchy/issues/7010) lid close disables the touchpad and it stays off | HP Pavilion Gaming | open | not fixed |
| [#11128](https://github.com/omacom/omarchy/issues/11128) no keyboard or pad at the LUKS prompt | AMD Surface Laptop 3 and 4 | open | not fixed |
| [#12136](https://github.com/omacom/omarchy/issues/12136) haptic pad needs linux-surface plus iptsd | Surface Laptop Studio 2 | open | not fixed |
| [#10815](https://github.com/omacom/omarchy/issues/10815) disable-while-typing has no effect | T2 MacBook Pro | open | not fixed |
| [#2415](https://github.com/omacom/omarchy/issues/2415) internal keyboard dead in the installer | Intel MacBooks | open | not fixed |

Two of these are Omarchy's own code rather than hardware. Issue #6935 is the sharper one: the 4.0 migration faithfully converted a commented-out `clickfinger_behavior` line from `input.conf` into a commented-out Lua line, and under the Lua config an unset value means no working right-click at all, by corner or by two-finger tap. Setting it explicitly to `true` or `false` fixes it. Issue #10449 is the other: Hyprland's `input:resolve_binds_by_sym` defaults to false and nothing in the v4.0.4 tree sets it, which we confirmed by grepping the tree, so all three stock `XF86Touchpad*` binds are dead out of the box.

The reporter of #7010 found the nastiest interaction. HP firmware injects a fake `KEY_TOUCHPAD_OFF` press through the internal keyboard just before the lid switch fires, which hits the stock `XF86TouchpadOff` bind, writes the persisted disable state, and leaves the pad off after every lid close.

On Intel Macs the story is older and mostly not Omarchy's to fix. The `applespi` timeouts on MacBook8,1 (issue #1954, continued in #2099) survived several rounds of module fixes; in August 2026 matthiasjg traced them to the DesignWare DMA engine the SPI controller transfers through and published a working setup for Omarchy 4.0. The installer keyboard problem in #2415 is two bugs in one thread, and an external USB keyboard gets you through either.

## Fixes that work

Try these in order.

1. Check whether the device exists at all. `hyprctl devices -j | jq -r '.mice[].name'` and `libinput list-devices`. If the pad is missing from both, it is a kernel or firmware problem, not configuration.
2. Run `omarchy restart trackpad`. This clears the common i2c-hid wedge, including the 7.2.3 ELAN freezes in #11245. Note that it only touches `i2c_hid_acpi` and `intel_quicki2c`, so it does nothing for Apple bcm5974 pads (#9389).
3. A/B the kernel. Reboot into the stock `linux` or `linux-lts` entry in Limine and retest. This is what isolated both #12181 and #11245, and it is the single most useful thing you can put in a bug report.
4. If right-click or scrolling changed after upgrading from 3.x, open `~/.config/hypr/input.lua` and set the touchpad options explicitly instead of leaving them commented.
5. If the Fn touchpad key does nothing, add `hl.config({ input = { resolve_binds_by_sym = true } })` to your input config.
6. If the pad only dies after suspend, wrap the scoped `i2c_hid_acpi` unbind and rebind for your device in a `systemd` sleep hook, as in #10924. See [suspend and sleep](/hardware/suspend-sleep/).
7. If the toggle seems stuck off, delete `~/.local/state/omarchy/toggles/hypr/touchpad-disabled-name` and reload Hyprland.
8. For layout trouble, set `kb_layout` and `kb_options` in `input.lua` rather than fighting the installer. See [layouts and locale](/keyboard/layouts-and-locale/).

## Report it

Run `omarchy debug`, which writes `/tmp/omarchy-debug.log` with `inxi -Farz`, `dmesg`, the current boot's warnings and errors, and your package list. Add the four things maintainers keep asking for: the output of `hyprctl devices -j`, the exact device string from `libinput list-devices`, `journalctl -k -b | grep -i 'i2c_hid\|i2c_designware\|applespi'`, and your DMI product name from `/sys/class/dmi/id/product_name`. If you can, include an A/B result against the stock kernel. Reports in this area that name the controller, the HID id and the kernel version get fixed. Reports that say the touchpad stopped working do not.

## Related

- [Suspend, sleep and resume](/hardware/suspend-sleep/) for pads that die only after resume
- [Keyboard layouts and locale](/keyboard/layouts-and-locale/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [Hyprland conf to Lua migration](/reference/hyprland-conf-to-lua-migration/)
- [T2 Macs](/hardware/t2-mac/) and [Microsoft Surface](/hardware/microsoft-surface/)
- [Submit your hardware report](/hardware/submit/)
