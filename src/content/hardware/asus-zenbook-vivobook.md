---
title: "ASUS Zenbook and Vivobook on Omarchy Linux"
description: "ASUS Zenbook and Vivobook support on Omarchy 4.0.4: one Zenbook UX5406AA backlight quirk ships, while audio, s2idle resume, FocalTech fingerprint and MediaTek Wi-Fi are open."
answer: "Rate the mainstream Intel Zenbook silver and the Vivobook bronze. Graphics and display work, and Omarchy ships one quirk for the Zenbook S14 UX5406AA backlight. The real risks are suspend and resume, which hangs or freezes on four different reported Zenbooks, plus FocalTech fingerprint readers with no libfprint driver and MediaTek or Realtek Wi-Fi that dies after s2idle. Avoid the Panther Lake UX5406AA if you need sound today."
appliesTo:
  from: "3.x"
status: partial
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
kind: model
vendor: "ASUS"
model: "ASUS Zenbook and Vivobook"
dmi: ["ZenBook UX325JA", "UX5406AA", "UM3406KA", "UX8402ZE", "S3407CA", "Vivobook_ASUSLaptop M6500QC_M6500QC", "Vivobook ASUSLaptop X1504VA", "VivoBook_ASUSLaptop X515DA_D515DA", "ASUSTeK COMPUTER INC."]
cpu: "Intel Ice Lake, Alder Lake, Arrow Lake-H and Panther Lake; AMD Ryzen 3000 through Ryzen AI in the reported machines"
gpu: "Intel Iris Plus, Iris Xe and Xe3; AMD Radeon Vega, 840M and 860M; RTX 3050 Mobile on some Vivobook and Zenbook Pro units"
year: "2020-2026"
rating: silver
subsystems:
  wifi: partial
  bluetooth: unknown
  audio: partial
  webcam: unknown
  fingerprint: partial
  gpu: partial
  suspend: partial
  hibernate: unknown
  touchpad: partial
  display: partial
  battery: partial
  keyboard: unknown
quirkScripts:
  - name: "omarchy-hw-asus-zenbook-ux5406aa"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/bin/omarchy-hw-asus-zenbook-ux5406aa"
    note: "Detector. Matches the DMI product name or family against \"ux5406aa\" and then confirms a Panther Lake GPU with omarchy-hw-intel-ptl."
  - name: "fix-asus-ptl-display-backlight.sh"
    url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus/fix-asus-ptl-display-backlight.sh"
    note: "Adds xe.enable_dpcd_backlight=1 to the Limine kernel command line on the Zenbook UX5406AA and the ExpertBook B9406, because the panel wants DPCD AUX backlight and the VBT says PWM."
issueCount: 40
tags: [asus, zenbook, vivobook, laptop, suspend, fingerprint]
sources:
  - url: "https://github.com/omacom/omarchy/issues/5557"
    title: "Issue #5557: No sound on ASUS Zenbook S14 UX5406AA (Panther Lake) - sof_sdw topology / kernel ABI mismatch"
    kind: issue
    author: "Pegorim"
    date: "2026-05-03"
  - url: "https://github.com/omacom/omarchy/issues/11458"
    title: "Issue #11458: Hard freeze shortly after resuming from s2idle on Intel Ice Lake (i915) with kernel 7.2.3-arch1-3 (ASUS ZenBook UX325JA)"
    kind: issue
    author: "a-gracia"
    date: "2026-09-12"
  - url: "https://github.com/omacom/omarchy/issues/10924"
    title: "Issue #10924: ASUS Zenbook UM3406KA touchpad stops responding after s2idle resume"
    kind: issue
    author: "ottosilva"
    date: "2026-09-09"
  - url: "https://github.com/omacom/omarchy/issues/7788"
    title: "Issue #7788: Hard hang entering s2idle on lid close (ASUS Zenbook UX8402ZE, Alder Lake + NVIDIA)"
    kind: issue
    author: "brightwalker25"
    date: "2026-08-22"
  - url: "https://github.com/omacom/omarchy/issues/4908"
    title: "Issue #4908: ASUS Zenbook 14 UM3406KA does not go to sleep only with the latest linux-firmware-other"
    kind: issue
    author: "the-main-thing"
    date: "2026-03-05"
  - url: "https://github.com/omacom/omarchy/issues/8800"
    title: "Issue #8800: Fingerprint setup fails silently on FocalTech FT9366 reader (2808:a658)"
    kind: issue
    author: "niels-lammers"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/11384"
    title: "Issue #11384: omarchy-hw-fingerprint false negative: FocalTech readers (2808:*) report as \"no sensor\""
    kind: issue
    author: "alanwcurry-dev"
    date: "2026-09-11"
  - url: "https://github.com/omacom/omarchy/issues/7003"
    title: "Issue #7003: RTL8852BE Wi-Fi dead after s2idle; rtw89 resume wedges the chip"
    kind: issue
    author: "aquaspy"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/1829"
    title: "Issue #1829: Wifi - Mediatek 7921 / Asus Vivobook S14 (possibly others)"
    kind: issue
    author: "jkc-2"
    date: "2025-09-20"
  - url: "https://github.com/omacom/omarchy/issues/11813"
    title: "Issue #11813: WiFi does not reconnect automatically after it disconnects"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/11812"
    title: "Issue #11812: WiFi auto-connects to 2.4GHz instead of preferring 5GHz on fresh install"
    kind: issue
    author: "HIMANSHU11827"
    date: "2026-09-14"
  - url: "https://github.com/omacom/omarchy/issues/8944"
    title: "Issue #8944: Brightness issue, screen gets very dim at 100% brightness but is alright at 95%"
    kind: issue
    author: "Techyiola"
    date: "2026-08-29"
  - url: "https://github.com/omacom/omarchy/issues/10344"
    title: "Issue #10344: Battery panel ignores charge_control_end_threshold and misreports the charge limit"
    kind: issue
    author: "brightwalker25"
    date: "2026-09-05"
  - url: "https://github.com/omacom/omarchy/pull/5606"
    title: "PR #5606: Install sof-firmware on Intel Panther Lake for DSP audio"
    kind: pr
    author: "mijuny"
    date: "2026-05-06"
  - url: "https://github.com/omacom/omarchy/releases/tag/v3.8.0"
    title: "Release v3.8.0 notes, including the Zenbook UX5406AA display backlight fix"
    kind: release
    author: "omacom"
    date: "2026-05-09"
  - url: "https://github.com/omacom/omarchy/blob/v4.0.4/install/hardware/asus/fix-asus-ptl-display-backlight.sh"
    title: "install/hardware/asus/fix-asus-ptl-display-backlight.sh at v4.0.4"
    kind: commit
    author: "omacom"
    date: "2026-09-15"
credits:
  - name: "Pegorim"
    url: "https://github.com/Pegorim"
    for: "Isolated the UX5406AA SoundWire failure and proved which upstream SOF patches fix it"
  - name: "mateuszkowalczyk"
    url: "https://github.com/mateuszkowalczyk"
    for: "Contributed the Zenbook UX5406AA display backlight fix that shipped in v3.8.0"
  - name: "ottosilva"
    url: "https://github.com/ottosilva"
    for: "Found the i2c_hid_acpi unbind and rebind workaround for the UM3406KA touchpad after resume"
  - name: "brightwalker25"
    url: "https://github.com/brightwalker25"
    for: "Documented the UX8402ZE lid close hang and the MemorySleepMode=deep workaround"
  - name: "niels-lammers"
    url: "https://github.com/niels-lammers"
    for: "Showed that no libfprint driver claims the FocalTech FT9366 reader"
faq:
  - q: "Is the ASUS Zenbook a good Omarchy laptop?"
    a: "A mainstream Intel Zenbook is a reasonable choice. Graphics, display and Wi-Fi generally come up, and the open reports concentrate on suspend and resume rather than on basic desktop function. Test sleep before you commit."
  - q: "Does sound work on the Zenbook S14 UX5406AA?"
    a: "Not on the stock Omarchy kernel as of 4.0.4. The sof_sdw driver fails to register a card, so PipeWire only shows a dummy sink. One reporter says kernel 7.3.0-rc1 fixes it, and the stable channel ships linux-omarchy 7.2.5."
  - q: "Will my Vivobook fingerprint reader work?"
    a: "If it is a FocalTech reader with USB vendor 2808, probably not. Omarchy's detector does not list that vendor, and for the FT9366 no libfprint driver exists at all."
  - q: "Do the ASUS audio quirk scripts run on a Zenbook?"
    a: "No. The ASUS mic and soft mixer scripts gate on omarchy-hw-asus-rog, which requires ROG in the DMI product family. A Zenbook or Vivobook never matches."
related: [asus-rog-zephyrus, suspend-sleep, audio, fingerprint, wifi]
draft: false
---

## Verdict

Silver for a mainstream Intel Zenbook, bronze for most Vivobooks, and one named model you should skip for now.

That split is what the evidence supports. Across 21 Zenbook and 19 Vivobook issues in the tracker, almost nothing is broken about the basic desktop. The open reports cluster in three places: suspend and resume, fingerprint readers, and Wi-Fi chips. Omarchy ships exactly one piece of enablement aimed at this family, a backlight fix for the Zenbook S14 UX5406AA, and that same model has had no working audio since May 2026.

The honest summary is that a Zenbook or Vivobook will install and run, and the thing most likely to annoy you is closing the lid.

## What works

Graphics come up on their own. Intel Iris Plus, Iris Xe and AMD Radeon integrated graphics all use in-tree drivers, and no Zenbook or Vivobook issue in the tracker reports a machine that fails to reach a desktop.

Wi-Fi works once firmware is current. The MediaTek MT7921 and MT7922 breakage reported on a Vivobook S14 in issue #1829 was a `linux-firmware-mediatek` regression, and the reporter later confirmed version 20251011-1 works again.

Fingerprint hardware itself is fine where a driver exists. On issue #11384 the reporter bypassed Omarchy's detection gate and got enrollment, `fprintd-verify` and PAM all working end to end, so the plumbing is sound and only the presence test was wrong.

Checked on 4.0.4. Most of this was already true on 3.x, since none of it depends on the Quickshell rewrite.

## What breaks

Suspend is the recurring theme, and it is not one bug.

On the Zenbook UX325JA, an Ice Lake machine, issue #11458 reports a hard freeze 20 to 50 seconds after a successful s2idle resume on kernel 7.2.3. The reporter had 42 clean cycles on 7.1.9 before the update, which makes it a kernel regression rather than a configuration problem. Still open.

On the Zenbook 14 UM3406KA, issue #10924 reports the ASUP1206 I2C touchpad going dead after resume, with `i2c_hid_acpi` failing its power state restore and returning error 121. Unbinding and rebinding only that device brings it back, and the reporter runs that from a systemd sleep hook. Still open.

On the Zenbook UX8402ZE, an Alder Lake machine with NVIDIA graphics, issue #7788 reports a hard hang entering s2idle on lid close, 5 boots out of 7 before the reporter pinned `MemorySleepMode=deep`. A commenter links the same class of failure to the NVIDIA GSP suspend path. Still open.

Older but worth knowing: issue #4908 traced a UM3406KA that would not sleep at all to a `linux-firmware-other` update, and the fix was downgrading that package. DHH's answer on that thread was blunt about scope, saying Omarchy has no power over the firmware bundle.

Audio is broken on one model. Issue #5557 shows the Panther Lake Zenbook S14 UX5406AA failing to register any sound card, with `sof_sdw` refusing the topology over an ABI mismatch and `aplay -l` reporting no soundcards. Pegorim tracked this to upstream SOF work and confirmed speakers, headphones, mic and HDMI all work with two Intel patches applied. A later commenter reports kernel 7.3.0-rc1 fixes it with no patching. Omarchy's stable channel ships `linux-omarchy` 7.2.5, so as of this writing that fix has not reached you. Note that PR #5606, which the tracker links to this issue, only installs `sof-firmware` on Panther Lake machines. It does not address the UX5406AA failure.

FocalTech fingerprint readers are a dead end on some units. Issue #8800 covers a Vivobook M6500QC where libfprint reports no driver for USB device 2808:A658, and there is no open source driver for that chip. Issue #11384 is the neighbouring problem: `omarchy-hw-fingerprint` lists vendors `27c6 138a 06cb 08ff 1c7a 147e`, and FocalTech's `2808` is not among them, so readers that would work are told they do not exist.

Wi-Fi after resume is chip dependent. Issue #7003 covers a Vivobook S 14 S3407CA whose Realtek RTL8852BE is dead after s2idle until the driver is reloaded. Issues #11813 and #11812, both on a Vivobook X1504VA with MediaTek MT7902, cover Wi-Fi that never reconnects on its own and a fresh install that prefers 2.4 GHz over the same SSID on 5 GHz.

Two smaller ones. Issue #8944 on a Vivobook 15 Pro reports the panel going dim above 95 percent brightness, resolved by swapping kernels. Issue #10344 was filed from a Zenbook using `asus_nb_wmi` and is about the battery panel misreporting a charge limit it did not set.

## What Omarchy does for this model

Less than you might expect. Two files, one model.

`bin/omarchy-hw-asus-zenbook-ux5406aa` matches the string `ux5406aa` against `/sys/class/dmi/id/product_name` or `product_family` through `omarchy-hw-match`, then confirms a Panther Lake GPU. `install/hardware/asus/fix-asus-ptl-display-backlight.sh` uses that detector to write `xe.enable_dpcd_backlight=1` into a Limine entry drop-in, because the panel reports an empty EDID and the xe driver otherwise picks PWM backlight, which makes brightness effectively binary. That fix shipped in v3.8.0 and is still wired into `install/hardware/all.sh` at v4.0.4. The script's own comment says it is enabled only for the ExpertBook B9406 and the UX5406AA for now.

Everything else under `install/hardware/asus/` targets other machines. The B9406 display and touchpad scripts, the ROG Flow Z13 touchpad rule, the ROG `asusctl` install, and the user level ALC285 mic and soft mixer fixes all gate on a different detector. `omarchy-hw-asus-rog` requires the literal string `ROG` in the DMI product family, so a Zenbook or Vivobook never triggers them. Speaker tunings ship only for the 2026 Dell XPS.

## Variants

Prefer a recent Intel Zenbook that is not Panther Lake. Lunar Lake and Arrow Lake units avoid the SoundWire audio problem entirely.

Avoid the Zenbook S14 UX5406AA if you want sound now. It is the one model with dedicated Omarchy enablement and the one model with a dead sound card.

Treat any Zenbook with a discrete NVIDIA GPU, such as the UX8402ZE, as a hybrid graphics machine first. Read [/hardware/hybrid-gpu/](/hardware/hybrid-gpu/) before buying.

On Vivobooks, check the fingerprint reader vendor and the Wi-Fi chip before you count on either. FocalTech readers and RTL8852BE Wi-Fi are both represented in open issues.

Zenbook Duo owners should expect the second panel to be extra monitor configuration work. That claim comes from an earlier hand written prototype for this site and is not backed by a tracker issue.

## Before you install

- Run `lspci -nnk | grep -iA3 network` and `lsusb` on a live session, and write down the Wi-Fi chip and the fingerprint reader vendor id.
- Test suspend and resume ten times before you migrate your data. Close the lid, wait, open it.
- If the machine hangs entering suspend, try `MemorySleepMode=deep` in a `sleep.conf.d` drop-in. See [/fix/suspend-wont-resume-s2idle/](/fix/suspend-wont-resume-s2idle/).
- Keep the previous kernel entry in Limine. Several of these reports are kernel regressions, and rolling back is the fastest test. See [/releases/channels/](/releases/channels/).
- Check for sound before anything else on a Panther Lake machine. An empty `/proc/asound/cards` is the tell.

## Related

- [/hardware/suspend-sleep/](/hardware/suspend-sleep/), [/hardware/audio/](/hardware/audio/), [/hardware/fingerprint/](/hardware/fingerprint/), [/hardware/wifi/](/hardware/wifi/)
- [/fix/no-sound-from-laptop-speakers/](/fix/no-sound-from-laptop-speakers/), [/fix/fingerprint-enrollment-fails/](/fix/fingerprint-enrollment-fails/), [/fix/battery-drains-fast/](/fix/battery-drains-fast/)
- [/hardware/asus-rog-zephyrus/](/hardware/asus-rog-zephyrus/) for ROG machines, which get `asusctl` and the audio quirks this family does not
- Omarchy manual: [system sleep](https://omarchy.org/manual/system-sleep/), [keyboard, mouse and trackpad](https://omarchy.org/manual/keyboard-mouse-trackpad/), [monitors](https://omarchy.org/manual/monitors/)
- Have one of these machines? Send what you found to [/hardware/submit/](/hardware/submit/)
