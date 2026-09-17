// Validates content frontmatter without a full Astro build. Usage: node scripts/validate-content.mjs [files or dirs...]
import { readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
const args = process.argv.slice(2);
const targets = args.length ? args : ['src/content'];
const files = [];
function walk(p) { const st = statSync(p); if (st.isDirectory()) for (const f of readdirSync(p)) walk(path.join(p, f)); else if (p.endsWith('.md')) files.push(p); }
targets.forEach(walk);
const STATUS = ['open', 'fixed', 'workaround', 'by-design', 'info', 'works', 'partial', 'broken', 'unknown'];
let bad = 0;
for (const f of files) {
  const s = readFileSync(f, 'utf8');
  const errs = [];
  const m = s.match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) { errs.push('no frontmatter'); }
  else {
    let d; try { d = yaml.load(m[1]); } catch (e) { errs.push('YAML: ' + e.message.split('\n')[0]); }
    if (d) {
      const isPage = f.includes('/pages/');
      if (!d.title) errs.push('missing title');
      if (!d.description) errs.push('missing description'); else if (d.description.length < 40 || d.description.length > 200) errs.push(`description length ${d.description.length} (need 40-200)`);
      if (!isPage) {
        if (!d.answer) errs.push('missing answer'); else { const w = d.answer.split(/\s+/).length; if (w < 20 || w > 110) errs.push(`answer ${w} words (aim 40-80)`); }
        if (!d.lastVerified) errs.push('missing lastVerified');
        if (d.status && !STATUS.includes(d.status)) errs.push(`bad status ${d.status}`);
        if (d.appliesTo && typeof d.appliesTo !== 'object') errs.push('appliesTo must be {from, to?}');
        for (const s of d.sources ?? []) { if (!s.url || !s.title) errs.push('source missing url/title'); else if (!/^https?:\/\//.test(s.url)) errs.push('source url not absolute: ' + s.url); }
        for (const q of d.faq ?? []) if (!q.q || !q.a) errs.push('faq item missing q/a');
        if (f.includes('/hardware/') && !d.kind) errs.push('hardware page missing kind');
        if (f.includes('/vs/') && !d.other) errs.push('vs page missing other');
        if (f.includes('/run/') && !d.platform) errs.push('run page missing platform');
        const body = s.slice(m[0].length);
        if (body.trim().length < 600) errs.push(`body too short (${body.trim().length} chars)`);
        if (/^#\s/m.test(body)) errs.push('body contains an H1 (# ...); use ## and below');
        if (/—/.test(body) || /—/.test(m[1])) errs.push('contains em dash (use commas/periods)');
        if (/\]\(\/[a-z-]+\/[^)]*\.html\)/.test(body)) errs.push('internal link uses .html');
        if (/iso\.omarchy\.org\/[^ )"]+\.iso["\s)]/.test(body) && !/omarchy\.org/.test(body)) errs.push('links an ISO file directly');
      }
    }
  }
  if (errs.length) { bad++; console.log(`✗ ${f}\n   - ${errs.join('\n   - ')}`); } else console.log(`✓ ${f}`);
}
console.log(`\n${files.length - bad}/${files.length} valid`);
process.exit(bad ? 1 : 0);
