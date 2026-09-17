import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../lib/site';
import { SECTIONS } from '../lib/content';
export const GET: APIRoute = async () => {
  const out: string[] = [`# ${SITE.name} (unofficial) — full text`, '', SITE.disclaimerLong, ''];
  for (const key of Object.keys(SECTIONS)) {
    const sec = SECTIONS[key];
    const entries = (await getCollection(key as any)).filter((e: any) => !e.data.draft);
    for (const e of entries as any[]) {
      const d = e.data;
      out.push(`---`, `# ${d.title}`, `URL: ${SITE.url}${sec.base}${e.id}/`, `Section: ${sec.label}`, `Applies to Omarchy: ${d.appliesTo?.from ?? '4.x'}${d.appliesTo?.to ? ' to ' + d.appliesTo.to : ' and later'}`, `Status: ${d.status ?? 'info'}${d.fixedIn ? ' (fixed in ' + d.fixedIn + ')' : ''}`, `Last verified: ${d.lastVerified?.toISOString?.().slice(0, 10) ?? ''}`, '', `Short answer: ${d.answer}`, '', e.body ?? '', '');
      if (d.sources?.length) { out.push('Sources:'); for (const s of d.sources) out.push(`- ${s.title}: ${s.url}`); out.push(''); }
    }
  }
  return new Response(out.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
