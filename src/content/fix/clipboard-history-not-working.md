---
title: "Clipboard history not working on Omarchy 4"
description: "Omarchy 4 clipboard history stops recording when a capture.sh process wedges. Kill it to bring Super + Ctrl + V back, and fix Super + V paste failures."
answer: "Text history usually stops because a stuck capture.sh blocks the wl-paste watcher. Run pgrep -af 'clipboard/capture.sh', and if anything is listed, run pkill -f 'clipboard/capture.sh'. Capture resumes at once with no restart. If the picker itself never opens, run omarchy restart shell. If Super + V does not paste, that is a separate Hyprland send_key_state bug."
appliesTo:
  from: "4.0.0"
status: workaround
lastVerified: 2026-09-16
omarchyVersionTested: "4.0.4"
category: shell
issueCount: 137
errorStrings:
  - "send_key_state: key not found"
  - "=[C]:-1: send_key_state: key not found"
  - "qt.quick.styledtext: StyledText - Invalid base url in img tag"
tags: [clipboard, quickshell, wl-clipboard, quattro, keybindings, shell]
sources:
  - url: "https://github.com/omacom/omarchy/issues/9443"
    title: "Issue #9443: Stuck capture.sh silently stops text clipboard history (no timeout on wl-paste)"
    kind: issue
    author: "mzijlstra-hia"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/7027"
    title: "Issue #7027: Intermittent 'send_key_state: key not found' on Super+V/C/X clipboard shortcuts"
    kind: issue
    author: "Louis454545"
    date: "2026-08-15"
  - url: "https://github.com/omacom/omarchy/issues/7371"
    title: "Issue #7371: SUPER+C/V/X universal clipboard shortcuts fail with \"send_key_state: key not found\" when a non-Latin keyboard layout is active"
    kind: issue
    author: "rsoutar"
    date: "2026-08-18"
  - url: "https://github.com/omacom/omarchy/issues/11201"
    title: "Issue #11201: Universal copy/paste/cut (SUPER+C/V/X) fails on non-Latin keyboard layouts"
    kind: issue
    author: "airenare"
    date: "2026-09-10"
  - url: "https://github.com/omacom/omarchy/issues/10701"
    title: "Issue #10701: Super+V send_key_state can stick and retrigger the bind (~6k forks/s)"
    kind: issue
    author: "gw7523"
    date: "2026-09-07"
  - url: "https://github.com/omacom/omarchy/issues/8676"
    title: "Issue #8676: Quickshell SIGSEGV (stack overflow) when opening paste history if a copied HTML page is in the clipboard"
    kind: issue
    author: "Xaedankye"
    date: "2026-08-27"
  - url: "https://github.com/omacom/omarchy/issues/9302"
    title: "Issue #9302: [quickshell] SIGSEGV in QQuickTextPrivate::updateLayout when clipboard contains HTML <img> tags"
    kind: issue
    author: "krreeshhh"
    date: "2026-08-31"
  - url: "https://github.com/omacom/omarchy/issues/10526"
    title: "Issue #10526: Clipboard manager cannot paste images into terminal apps: Shift+Insert is consumed as a text-only paste"
    kind: issue
    author: "cxj05h"
    date: "2026-09-06"
  - url: "https://github.com/omacom/omarchy/issues/7058"
    title: "Issue #7058: Quattro: selecting an image in clipboard history copies it but does not paste it"
    kind: issue
    author: "andresreibel"
    date: "2026-08-16"
  - url: "https://github.com/omacom/omarchy/issues/7613"
    title: "Issue #7613: Clipboard: selecting entry auto-pastes into focused terminal"
    kind: issue
    author: "nightdevil00"
    date: "2026-08-20"
  - url: "https://github.com/omacom/omarchy/issues/8753"
    title: "Issue #8753: Quickshell freezes for 1-2 seconds when a focused panel reads from a stalled Wayland clipboard owner"
    kind: issue
    author: "forbidden-game"
    date: "2026-08-28"
  - url: "https://github.com/omacom/omarchy/issues/2832"
    title: "Issue #2832: Clipboard history does not add more data."
    kind: issue
    author: "LeoPazEs"
    date: "2025-10-25"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.0"
    title: "Release v4.0.0 (Quattro): adds a native clipboard manager with image previews and sensitive-content exclusion"
    kind: release
    author: "dhh"
    date: "2026-08-14"
  - url: "https://github.com/omacom/omarchy/releases/tag/v4.0.2"
    title: "Release v4.0.2: prevent remote image injection in shell text elements"
    kind: release
    author: "ErikMelton"
    date: "2026-08-31"
  - url: "https://omarchy.org/manual/unified-clipboard-history/"
    title: "Omarchy Manual: Unified Clipboard & History"
    kind: manual
credits:
  - name: "mzijlstra-hia"
    url: "https://github.com/mzijlstra-hia"
    for: "Tracing silent text-history loss to a capture.sh process that never exits"
  - name: "maxcroy1"
    url: "https://github.com/maxcroy1"
    for: "Reproducing both unbounded wl-paste reads against the shipped capture.sh"
  - name: "assada"
    url: "https://github.com/assada"
    for: "Finding the xkb group lookup behind send_key_state failures and the raw keycode workaround"
  - name: "cxj05h"
    url: "https://github.com/cxj05h"
    for: "Explaining why Shift+Insert drops image pastes in terminals"
faq:
  - q: "Where does Omarchy 4 store clipboard history?"
    a: "Text entries live in ~/.local/state/omarchy/clipboard-history.json and images in ~/.local/state/omarchy/clipboard-images/. The picker keeps the most recent 300 entries."
  - q: "Why do my 1Password copies never show up in history?"
    a: "That is deliberate. capture.sh skips anything marked with CLIPBOARD_STATE=sensitive or the x-kde-passwordManagerHint mime type, which is how password managers flag a copy."
  - q: "Do I still need cliphist or clipse on Omarchy 4?"
    a: "No. Omarchy 4 ships its own Quickshell clipboard plugin on Super + Ctrl + V. Clipse was dropped back in v1.3.0 because it stored passwords in plain text."
related: [quickshell-crashes-or-bar-missing, custom-keybindings-lost-after-quattro, walker-launcher-missing-after-update, screenshot-shortcut-not-working]
draft: false
---

Omarchy 4 replaced Walker's clipboard provider with a Quickshell plugin. `Super + Ctrl + V` opens it, `Super + V` is universal paste. When people say "clipboard history is broken" on 4.x they usually mean one of three different faults, and they have different fixes. Checked against v4.0.0 through v4.0.4, with v3.8.4 as the last 3.x reference.

## The fix

### 1. History stopped recording text (most common on 4.x)

The picker still opens, old entries are all there, images still get added, but nothing you copy as text appears. Look for a wedged capture process:

```bash
pgrep -af 'clipboard/capture.sh'
```

On a healthy system this prints nothing. `capture.sh` runs for a fraction of a second per copy. Anything listed has been stuck long enough to block the watcher. Confirm the age:

```bash
ps -eo pid,etimes,args | grep '[c]lipboard/capture.sh'
```

Kill it:

```bash
pkill -f 'clipboard/capture.sh'
```

Text capture resumes immediately. You do not need to restart the shell or log out. This is issue #9443, still open on v4.0.4.

### 2. The picker does not open at all

Check that both watchers are alive:

```bash
pgrep -af 'wl-paste .*--watch'
```

You should see exactly two, one `--type text` and one `--type image/png`. If either is missing, or if `Super + Ctrl + V` does nothing, restart the shell:

```bash
omarchy restart shell
```

You can also call the picker directly to separate a broken keybinding from a broken plugin:

```bash
omarchy-shell shell toggle omarchy.clipboard
omarchy-shell shell listPlugins
```

If the shell crashes the moment the picker opens, and you are on v4.0.0 or v4.0.1, update. The clipboard preview rendered entries as rich text, so a copied web page could crash Quickshell with a SIGSEGV (issues #8676 and #9302). v4.0.2 set `textFormat: Text.PlainText` on those elements, shipped as "Prevent remote image injection in shell text elements". That change is present in the v4.0.2, v4.0.3 and v4.0.4 sources.

### 3. Super + V, C or X does nothing, or flashes a Lua error

If you see `send_key_state: key not found`, the history is fine. The universal copy and paste binds are failing. This bites hardest on non-Latin layouts, because Hyprland resolves the key name against the active xkb group only, and a Cyrillic or Arabic group has no `c` or `v` keysym to find. Put a raw keycode version in `~/.config/hypr/bindings.lua`:

```lua
hl.unbind("SUPER + C")
hl.unbind("SUPER + V")
hl.unbind("SUPER + X")

local function send_once(mods, key)
  return function()
    hl.dispatch(hl.dsp.send_key_state({ mods = mods, key = key, state = "down" }))
    hl.timer(function()
      hl.dispatch(hl.dsp.send_key_state({ mods = mods, key = key, state = "up" }))
    end, { timeout = 50, type = "oneshot" })
  end
end

local function in_terminal()
  local window = hl.get_active_window()
  if not window then return false end
  for _, tag in ipairs(window.tags or {}) do
    if tag:gsub("%*$", "") == "terminal" then return true end
  end
  return false
end

local function universal(mods, key, term_mods, term_key)
  return function()
    if in_terminal() then send_once(term_mods, term_key)() else send_once(mods, key)() end
  end
end

o.bind("SUPER + C", "Universal copy", universal("CTRL", "code:54", "CTRL", "Insert"))
o.bind("SUPER + V", "Universal paste", universal("CTRL", "code:55", "SHIFT", "Insert"))
o.bind("SUPER + X", "Universal cut", send_once("CTRL", "code:53"))
```

`code:54`, `code:55` and `code:53` are the physical C, V and X keys, so the lookup skips xkb entirely. Credit to assada on issue #7027 for the diagnosis and the keycode form. The terminal branch is kept from the shipped `default/hypr/bindings/clipboard.lua` so terminals keep getting `Ctrl + Insert` and `Shift + Insert`.

### 4. On 3.x

3.8.4 and earlier had no Quickshell plugin. History came from Walker and its elephant backend, bound to `Super + Ctrl + V` since v3.1.0. When it stopped adding entries the fix was to restart the services:

```bash
omarchy-restart-walker
```

That is what resolved issue #2832. `wl-clip-persist` was a known offender in the 2.x and early 3.x era and is not shipped in 3.8.4, so there is nothing to remove there.

## Verify it worked

Copy two different strings from two different apps, then:

```bash
jq 'length' ~/.local/state/omarchy/clipboard-history.json
stat -c %y ~/.local/state/omarchy/clipboard-history.json
```

The count should grow and the timestamp should be seconds old. Open `Super + Ctrl + V` and both entries should be at the top. Copy an image too, since text and image capture are independent and one can work while the other is dead.

## Why it happens

The plugin does not poll. On startup it reaps leftover watchers, then spawns two `wl-paste --watch` processes that call `shell/plugins/clipboard/capture.sh`, one for `text` and one for `image/png`. `wl-paste --watch` waits for its command to exit before handling the next clipboard event, so one capture that never returns silently stops that flavour forever.

In the shipped `capture.sh`, the image branch is guarded with `timeout 2s`, but the `wl-paste --list-types` call at the top and the final text read are not. `wl-paste` blocks indefinitely when the clipboard's owning client disappears mid transfer, so a single badly timed copy wedges text capture. That asymmetry is why images keep working while text quietly dies. The same stalled-owner behaviour also shows up as a one to two second freeze when a focused panel reads the clipboard (issue #8753).

The shell does restart a watcher that exits, on a one second timer. It has no way to notice a watcher that is alive but blocked, which is exactly this case.

For the paste keys, the cause is different. `send_key_state` resolves a key name against the currently active xkb group and caches the result per keyboard and key name, without the group in the cache key. So the same binding can work all day and then fail after a config reload or an input hotplug. A related report, issue #10701, describes the injected key retriggering its own bind because Super is still physically held, spinning up thousands of forks a second.

## If that did not work

- Selecting an image in the picker copies it but does not paste, especially into terminals. `omarchy-clipboard-paste-file` finishes with `Shift + Insert`, which terminals intercept as a text-only paste. Press `Ctrl + V` yourself after picking the entry. See issues #7058 and #10526.
- Selecting any entry auto-pastes into whatever is focused. That is current behaviour, not a fault, and issue #7613 argues it should be copy only.
- Copies from a password manager never appear. `capture.sh` deliberately drops anything flagged `CLIPBOARD_STATE=sensitive` or carrying the `x-kde-passwordManagerHint` type. Sensitive-content exclusion shipped with the plugin in v4.0.0.
- Old entries vanish on their own. The picker keeps 300 entries.
- As a last resort, reset the store. This loses your history: `mv ~/.local/state/omarchy/clipboard-history.json{,.bak}` then `omarchy restart shell`.
- Non-Latin layouts break more than clipboard keys. See [keyboard layouts and locale](/keyboard/layouts-and-locale/).

Nothing here needs a reinstall, and none of the open issues above have shipped a fix as of v4.0.4.

## Related

- [Quickshell crashes or the bar is missing](/fix/quickshell-crashes-or-bar-missing/)
- [Custom keybindings lost after Quattro](/fix/custom-keybindings-lost-after-quattro/)
- [Walker launcher missing after update](/fix/walker-launcher-missing-after-update/)
- [Upgrading 3.x to 4 Quattro](/upgrade/3-to-4-quattro/)
- [Keybindings reference](/reference/keybindings/)
- [Still broken on the current release](/releases/still-broken/)
- Manual chapter: [Unified Clipboard & History](https://omarchy.org/manual/unified-clipboard-history/)
