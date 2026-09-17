// Generates Open Graph images with sharp (SVG -> PNG). Usage: node scripts/og.mjs
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const here = path.dirname(fileURLToPath(import.meta.url));
const fontsDir = path.join(here, 'fonts');
mkdirSync('/tmp/omarchylinux-fc', { recursive: true });
writeFileSync('/tmp/omarchylinux-fc/fonts.conf', `<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>${fontsDir}</dir><cachedir>/tmp/omarchylinux-fc/cache</cachedir></fontconfig>`);
process.env.FONTCONFIG_FILE = '/tmp/omarchylinux-fc/fonts.conf';
process.env.FONTCONFIG_PATH = '/tmp/omarchylinux-fc';
const sharp = (await import('sharp')).default;
const out = 'public/og';
mkdirSync(out, { recursive: true });
const cards = [
  ['default', 'The answers the Omarchy manual leaves out', 'Field manual', 'Hardware reports · error fixes · command reference · what changed per release'],
  ['hardware', 'Does Omarchy run on it?', 'Hardware compatibility', 'Component and model reports, stamped by Omarchy and kernel version'],
  ['fix', 'What does this error mean?', 'Omarchy error fixes', 'One page per failure, fix first, with the version it applies to'],
  ['reference', 'Every omarchy command and key', 'Reference', 'Commands, keybindings, menu tree, and diffs between releases'],
  ['releases', 'What changed in this release?', 'Releases and upgrades', 'Release notes, migrations decoded, channel status'],
  ['official', 'Is this Omarchy site official?', 'Trust', 'Which domains and accounts are official, and the trademark facts'],
];
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
function wrap(text, max) { const w = text.split(' '); const lines = []; let cur = ''; for (const x of w) { if ((cur + ' ' + x).trim().length > max) { lines.push(cur.trim()); cur = x; } else cur += ' ' + x; } if (cur.trim()) lines.push(cur.trim()); return lines; }
for (const [name, h1, eyebrow, sub] of cards) {
  const h1Lines = wrap(h1, 26);
  const subLines = wrap(sub, 62);
  const h1Svg = h1Lines.map((l, i) => `<text x="70" y="${215 + i * 86}" font-family="Barlow Condensed" font-weight="700" font-size="84" fill="#1A2129">${esc(l)}</text>`).join('');
  const subY = 215 + h1Lines.length * 86 + 10;
  const subSvg = subLines.map((l, i) => `<text x="70" y="${subY + i * 42}" font-family="Source Sans 3" font-size="32" fill="#4A5563">${esc(l)}</text>`).join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <rect width="1200" height="630" fill="#F4F6F2"/>
  <rect x="0" y="0" width="14" height="630" fill="#2C5F86"/>
  <text x="70" y="110" font-family="IBM Plex Mono" font-size="22" letter-spacing="3" fill="#6E7885">${esc(eyebrow.toUpperCase())} · UNOFFICIAL</text>
  ${h1Svg}${subSvg}
  <text x="70" y="565" font-family="Barlow Condensed" font-weight="700" font-size="44" fill="#1A2129">omarchy<tspan fill="#2C5F86">linux</tspan>.org</text>
  <text x="1130" y="565" text-anchor="end" font-family="IBM Plex Mono" font-size="19" fill="#6E7885">not affiliated with 37signals or the Omacom Foundation</text>
</svg>`;
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toFile(`${out}/${name}.png`);
  console.log('wrote', `${out}/${name}.png`);
}
