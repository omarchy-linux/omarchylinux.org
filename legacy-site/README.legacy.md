# omarchylinux.org

Unofficial hardware and switcher notes for [Omarchy](https://omarchy.org).

This is **not** the distro, **not** an ISO mirror, and **not** affiliated with the Omacom Foundation, 37signals, or DHH. Omarchy is a pending trademark.

Static files live in `site/`. Point Cloudflare Pages (or any static host) at that directory. The domain is already on Cloudflare nameservers.

```bash
python3 -m http.server 4173 --directory site
```

Then open http://127.0.0.1:4173

## Why this exists

Official omarchy.org already covers install, manual, plugins, themes, news, and meetups. The gap is a searchable **per-model** compatibility list (Wi-Fi, audio, webcam, fingerprint, GPU, suspend) for people who google “omarchy linux” after a YouTube video.

## Do not

- Host ISOs or “mirrors”
- Use the official wordmark/logo
- Pretend this is omarchy.org
