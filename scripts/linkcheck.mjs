// Checks internal links in dist/. Usage: node scripts/linkcheck.mjs
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import path from 'node:path';
const root = 'dist';
const files = [];
(function walk(p) { for (const f of readdirSync(p)) { const fp = path.join(p, f); if (statSync(fp).isDirectory()) walk(fp); else if (fp.endsWith('.html')) files.push(fp); } })(root);
const bad = new Map();
let total = 0;
for (const f of files) {
  const html = readFileSync(f, 'utf8');
  for (const m of html.matchAll(/href="(\/[^"#?]*)/g)) {
    const href = m[1]; total++;
    let target;
    if (href.endsWith('/')) target = path.join(root, href, 'index.html');
    else target = path.join(root, href);
    if (!existsSync(target) && !existsSync(target + '/index.html') && !existsSync(target + '.html')) {
      if (!bad.has(href)) bad.set(href, []);
      bad.get(href).push(f.replace(root, ''));
    }
  }
}
console.log(`${files.length} pages, ${total} internal links, ${bad.size} broken targets`);
for (const [href, from] of [...bad.entries()].sort()) console.log(`✗ ${href}  ← ${from.slice(0, 3).join(', ')}${from.length > 3 ? ` (+${from.length - 3})` : ''}`);
process.exit(bad.size ? 1 : 0);
