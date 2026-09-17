---
title: "Framework Laptop 16"
description: "Framework Laptop 16 on Omarchy 4.x: what the distro detects and installs for it, the qmk-hid install failure, the theme-set hang, and the dGPU wake bug."
answer: "Silver. The Framework Laptop 16 installs and runs on Omarchy 4.x, and the distro ships model-specific enablement: a DMI detector, the qmk-hid package, a keyboard udev rule and theme-synced backlighting. Two open bugs matter: the keyboard theming script can hang omarchy theme set if another QMK or VIA keyboard is plugged in, and opening Activity wakes a suspended discrete graphics module."
appliesTo:
  from: "3.x"
  to: "4.0.4"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "Framework"
model: "Framework Laptop 16"
dmi: ["Laptop 16 (AMD Ryzen 7040 Series)", "16in Laptop"]
cpu: "AMD Ryzen 7040 Series or Ryzen AI 300 Series"
gpu: "Radeon integrated, optional Radeon RX 7700S or GeForce RTX 5070 graphics module"
year: "2024-2026"
rating: silver
subsystems:
  wifi: works
  bluetooth: unknown
  audio: unknown
  webcam: unknown
  fingerprint: unknown
  gpu: partial
  suspend: unknown
  hibernate: unknown
  touchpad: unknown
  display: works
  battery: partial
  keyboard: partial
quirkScripts:
  - name: "omarchy-hw-framework16"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-framework16"
    note: "DMI detector: sys_vendor must be Framework and the product name or family must contain \"Laptop 16\"."
  - name: "install/hardware/framework16.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/framework16.sh"
    note: "Adds the qmk-hid package on a detected Framework Laptop 16."
  - name: "install/hardware/framework/qmk-hid.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/framework/qmk-hid.sh"
    note: "Installs /etc/udev/rules.d/50-framework16-qmk-hid.rules for unprivileged hidraw access to the keyboard module."
  - name: "omarchy-theme-set-keyboard-f16"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-theme-set-keyboard-f16"
    note: "Pushes the current theme colour to the keyboard RGB through qmk_hid. Source of issue #8243."
issueCount: 6
tags: [framework, framework-laptop-16, qmk-hid, hybrid-gpu, amd, laptop]
sources:
  - url: "https://github.com/omacom/omarchy/issues/6423"
    title: "Issue #6423: (3.8.4) installation fails with `error: target not found: qmk-hid`"
    kind: issue
    author: "bsl"
    date: "2026-07-29"
  - url: "https://github.com/omacom/omarchy/issues/8243"
    title: "Issue #8243: omarchy theme set / omarchy update hangs indefinitely in omarchy-theme-set-keyboard-f16 with a Keychron K8 Pro attached"
    kind: issue
    author: "ykzird"
    date: "2026-08-25"
  - url: "https://github.com/omacom/omarchy/issues/11184"
    title: "Issue #11184: Activity (btop) wakes a suspended NVIDIA dGPU on every open"
    kind: issue
    author: "Hazakins"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10406"
    title: "Issue #10406: Wifi Panel hangs on typo'd password - Unable to forget network or change password"
    kind: issue
    author: "mortalglitch"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/6890"
    title: "Issue #6890: Can't upgrade to Quattro. Stuck on 3.8.5 that's not listed on releases page."
    kind: issue
    author: "zorzysty"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/discussions/4073"
    title: "Discussion #4073: Make Omarchy works with keyboard.frame.work and Framework 16 laptop"
    kind: discussion
    author: "liancheng"
    date: "2026-01-04"
  - url: "https://github.com/omacom/omarchy/commit/edce5809df36003c96822b456f327fa79ec1cfd7"
    title: "Commit edce5809: Add qmk-hid to omarchy-other.packages"
    kind: commit
    author: "ryanrhughes"
    date: "2026-05-21"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.4.0"
    title: "Release v3.4.0: theme-synced keyboard backlighting on Framework 16 laptops"
    kind: release
    author: "omacom"
    date: "2026-02-26"
  - url: "https://omarchy.org/manual/keyboard-mouse-trackpad/"
    title: "Omarchy manual: Keyboard, Mouse, Trackpad"
    kind: manual
  - url: "https://linux-hardware.org/?log=dmidecode&probe=a5a71686b3"
    title: "Hardware probe: Framework Laptop 16 dmidecode"
    kind: other
credits:
  - name: "godlewski"
    url: "https://github.com/godlewski"
    for: "Theme-synced Framework 16 keyboard backlighting, shipped in v3.4.0"
  - name: "ryanrhughes"
    url: "https://github.com/ryanrhughes"
    for: "Adding qmk-hid to the ISO package list so offline installs stop failing"
  - name: "ykzird"
    url: "https://github.com/ykzird"
    for: "Tracing the omarchy theme set hang to unbounded qmk_hid calls in omarchy-theme-set-keyboard-f16"
  - name: "Hazakins"
    url: "https://github.com/Hazakins"
    for: "Measuring that btop's NVML init resumes the graphics module on every Activity open"
  - name: "liancheng"
    url: "https://github.com/liancheng"
    for: "Documenting the udev rules keyboard.frame.work needs for the keyboard and numpad modules"
faq:
  - q: "Does Omarchy have specific support for the Framework Laptop 16?"
    a: "Yes. It ships omarchy-hw-framework16, a DMI detector, and two install hooks that add the qmk-hid package and a udev rule for the keyboard module. Theme changes also push colour to the keyboard RGB."
  - q: "Why did my 3.8.4 install fail with target not found: qmk-hid?"
    a: "The package was missing from the ISO's offline mirror. It was added to install/omarchy-other.packages after v3.8.4 and is present in every 4.x tree, and qmk-hid 0.1.13-1 is in the stable, rc and edge Omarchy channels."
  - q: "Should I buy the discrete graphics module?"
    a: "Only if you need it. Issue #11184 shows the RTX 5070 module leaving runtime suspend every time you open Activity, on battery included. An integrated-graphics Laptop 16 avoids that whole class of problem."
related: [framework-laptop-13, hybrid-gpu, nvidia, amd-gpu, battery-power]
draft: false
---

Omarchy treats the Framework Laptop 16 as a named machine. It has its own detector script, its own install hooks and its own keyboard theming path, which is more than most laptops get. That enablement is narrow, though: it is entirely about the swappable keyboard module. Everything else falls back to the generic AMD and hybrid GPU handling.

## Verdict

Silver. The machine installs and runs, nothing in the tracker points at a dead subsystem, and the distro ships model-specific enablement for it. Two things keep it off gold. First, the evidence is thin: the tracker index attributes six issues and four discussions to this laptop, only five of those issues were actually filed from one, and none of them exercises fingerprint, audio, webcam or sleep, so most subsystems here are marked unknown rather than working. Second, two live bugs are open on 4.0.4, and both are Omarchy bugs rather than hardware faults.

Checked against the v4.0.4 and v3.8.4 source snapshots on 2026-09-16.

## What works

The Ryzen AI 300 configuration drives its displays from the integrated Radeon 890M through `amdgpu`, reported directly by the owner in [#11184](https://github.com/omacom/omarchy/issues/11184) on Omarchy 4.0.3 with kernel 7.2.3. Wi-Fi connects on a fresh 4.x install; the only Wi-Fi report, [#10406](https://github.com/omacom/omarchy/issues/10406), is about the panel refusing to forget a mistyped network, not about the radio, and the reporter got online through `nmtui` on the same hardware.

Keyboard RGB follows your theme. That landed in [v3.4.0](https://github.com/omacom/omarchy/releases/tag/v3.4.0), contributed by @godlewski, and still runs in 4.0.4 through `omarchy-theme-set-keyboard-f16`. The `qmk-hid` tool it needs is now carried in the Omarchy package repository at 0.1.13-1 on the stable, rc and edge channels.

Subsystems with no Omarchy-specific report either way: fingerprint, webcam, audio, Bluetooth, touchpad, hibernate and system suspend. Nobody has filed on them from this laptop, so they stay unknown here.

## What breaks

**Install fails with `error: target not found: qmk-hid`.** Reported by @bsl in [#6423](https://github.com/omacom/omarchy/issues/6423) against the 3.8.4 ISO. The Framework 16 hook asked pacman for `qmk-hid`, but the package was never listed in the ISO builder's sources, so it was absent from the offline mirror. Commit [edce5809](https://github.com/omacom/omarchy/commit/edce5809df36003c96822b456f327fa79ec1cfd7) by @ryanrhughes added it to `install/omarchy-other.packages`; it was written in May and cherry-picked onto the main branch on 2026-07-30, nine days after the 3.8.4 release. That file has no `qmk-hid` entry in the v3.8.4 tree and does have one from v4.0.0 onward, so 4.x installs are clear. The issue is still open on the tracker, but the cause is gone.

**`omarchy theme set` and `omarchy update` hang forever.** [#8243](https://github.com/omacom/omarchy/issues/8243), open, filed by @ykzird against 4.0.1. The report did not come from a Framework 16. It came from a desktop where `qmk-hid` had been installed by hand for a Keychron K8 Pro, and it matters here because `install/hardware/framework16.sh` installs that same package on every Framework 16. The script it implicates is `omarchy-theme-set-keyboard-f16`: its whole precondition is that `qmk_hid` exists and the theme has a `keyboard.rgb`, after which it runs `qmk_hid via` five times with no time limit and no check that the device on the other end is a Framework keyboard, or that it answers at all. With the Keychron attached, the first call never returned. A 4.0.1 migration (`1787481315`) re-stages the current theme through `omarchy-theme-refresh`, so `omarchy update` sat on that step until the keyboard was unplugged, after which it finished immediately. The reporter suggests wrapping the calls in `timeout`; that has not shipped as of 4.0.4. Whether the Framework 16's own keyboard module can trigger the same stall is unreported.

**Opening Activity wakes the discrete graphics module.** [#11184](https://github.com/omacom/omarchy/issues/11184), open, on a Laptop 16 with a Ryzen AI 9 HX 370 and an RTX 5070 module. Omarchy's `config/btop/btop.conf` sets `shown_gpus = "nvidia amd intel"` on line 254. Because `nvidia` is in that list, btop 1.4.7 loads NVML as soon as it starts, and it does so whether or not you have a GPU panel showing. The reporter watched the card's `runtime_status`: it went from `suspended` to `resuming` about two seconds after Activity opened, stayed `active` for as long as the window was up, and dropped back roughly fifteen seconds after it closed. With `shown_gpus = "amd"` in a private btop config, the card never left `suspended`, even with a GPU box turned on.

**keyboard.frame.work could not open the input modules on 3.2.3.** Discussion [#4073](https://github.com/omacom/omarchy/discussions/4073) by @liancheng, from January 2026, predates every piece of Framework 16 enablement in the tree: the udev rule, the detector and the theming script all arrived with @godlewski's PR #4524 on 2026-02-18. Back then the browser configurator got `NotAllowedError` on both the keyboard module (`32ac:0012`) and the numpad module (`32ac:0014`), and the recipe was QMK's `50-qmk.rules` plus two `uaccess` rules for those IDs. The discussion also notes that `50-qmk.rules` fails `udevadm verify` on Omarchy because it references a `plugdev` group that does not exist. On 4.x, the shipped `default/udev/framework16-qmk-hid.rules` is a single line granting `uaccess` on `hidraw` devices with vendor `32ac` and product `0012`, so the keyboard module is now user-accessible, but nothing covers the numpad module, and no one has reported whether keyboard.frame.work works out of the box on a 4.x install.

**Stuck on 3.8.5 during the Quattro upgrade.** [#6890](https://github.com/omacom/omarchy/issues/6890) by @zorzysty was filed from a Framework 16 on release day and closed within four minutes. Nothing model-specific; see [upgrading 3 to 4](/upgrade/3-to-4-quattro/).

## What Omarchy does for this model

Detection is `bin/omarchy-hw-framework16`. It requires `/sys/class/dmi/id/sys_vendor` to read exactly `Framework`, then calls `omarchy-hw-match "Laptop 16"`, which greps `product_name` and `product_family` case-insensitively. A hardware probe of a 7040-series unit reports the product name `Laptop 16 (AMD Ryzen 7040 Series)` and the family `16in Laptop`, so the match lands on the product name.

Two install hooks use that detector, both run from `install/hardware/all.sh`:

- `install/hardware/framework16.sh` adds the `qmk-hid` package.
- `install/hardware/framework/qmk-hid.sh` copies `default/udev/framework16-qmk-hid.rules` to `/etc/udev/rules.d/50-framework16-qmk-hid.rules`, granting `uaccess` on the keyboard module's hidraw node so RGB control works without root.

At runtime, `omarchy-theme-set-keyboard` calls `omarchy-theme-set-keyboard-f16`, which converts the theme's `keyboard.rgb` hex to QMK HSV and writes it through `qmk_hid via`.

If you fit a discrete module, `install/hardware/nvidia.sh` installs `nvidia-open-dkms` for any GSP-capable NVIDIA card (PCI device ID `0x1e00` or above, which includes the RTX 5070), sets `nvidia_drm modeset=1` and adds the NVIDIA modules to the initramfs. `omarchy-hw-hybrid-gpu` then counts GPUs and unlocks the hybrid GPU toggle. None of that is Framework-specific; see [hybrid GPU laptops](/hardware/hybrid-gpu/).

**3.x versus 4.x.** Mostly the paths moved. On v3.8.4 the hooks lived at `install/packaging/framework16.sh` and `install/config/hardware/framework/qmk-hid.sh`; on 4.x both sit under `install/hardware/`. The detector, the udev rule and `framework16.sh` are byte-identical between the two trees. `qmk-hid.sh` changed slightly: the 3.8.4 version ran `udevadm control --reload-rules` and `udevadm trigger` after copying the rule, and the 4.x version does not, so the rule takes effect at the next boot.

## Variants

Mainboards come in Ryzen 7040 Series and Ryzen AI 300 Series. Both are seen in Omarchy reports, 7040 in [#10406](https://github.com/omacom/omarchy/issues/10406) and AI 300 in [#11184](https://github.com/omacom/omarchy/issues/11184). Graphics modules are integrated only, Radeon RX 7700S, or GeForce RTX 5070.

Prefer integrated graphics if you can. It is the only configuration with no hybrid GPU surface, and the one open GPU bug on this machine is specific to having a discrete module fitted. The RTX 5070 module additionally pulls you into the proprietary NVIDIA stack, covered on [NVIDIA drivers on Omarchy 4](/fix/nvidia-drivers-omarchy-4/).

There is no evidence either way about the RX 7700S module under Omarchy. Nobody has filed on it.

## Before you install

- Use a 4.x ISO. The `qmk-hid` install failure is a 3.x problem and there is no reason to start there.
- If you own another QMK or VIA keyboard, unplug it before your first `omarchy theme set` or `omarchy update` until [#8243](https://github.com/omacom/omarchy/issues/8243) is fixed.
- If you fit the RTX 5070 module, edit `shown_gpus` in your btop config before you start trusting the battery estimate.
- If the Wi-Fi panel gets stuck on a mistyped password, `nmtui` gets you online. The reporter of [#10406](https://github.com/omacom/omarchy/issues/10406) hit this on 4.0.0 install media and found the panel's lock icon handles it after updating.
- For keyboard.frame.work, expect to add a udev rule for the numpad module, `32ac:0014`. Omarchy's rule covers only the keyboard module, `32ac:0012`.
- Check your BIOS version against Framework's own releases first.

## Related

[Framework Laptop 13](/hardware/framework-laptop-13/) shares the vendor but not the enablement. For the graphics module, read [hybrid GPU laptops](/hardware/hybrid-gpu/) and [AMD GPU](/hardware/amd-gpu/). For the battery cost of a wakeful discrete card, [battery drains fast](/fix/battery-drains-fast/). The manual chapter on [keyboard, mouse and trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/) covers input configuration generally. If you run this laptop, add what you find at [hardware submit](/hardware/submit/).
