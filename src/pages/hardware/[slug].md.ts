import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../../lib/site';
export async function getStaticPaths() {
  const entries = await getCollection('hardware');
  return entries.filter((e: any) => !e.data.draft).map((e: any) => ({ params: { slug: e.id }, props: { entry: e } }));
}
export const GET: APIRoute = ({ props }) => {
  const e: any = (props as any).entry;
  const d = e.data;
  const head = [
    '# ' + d.title, '', d.description, '',
    '> **Short answer:** ' + d.answer, '',
    '- Applies to Omarchy: ' + (d.appliesTo ? (d.appliesTo.to ? d.appliesTo.from + ' to ' + d.appliesTo.to : d.appliesTo.from + ' and later') : '4.x'),
    d.status ? '- Status: ' + d.status : '', d.fixedIn ? '- Fixed in: ' + d.fixedIn : '',
    '- Last verified: ' + (d.lastVerified ? d.lastVerified.toISOString().slice(0, 10) : ''),
    '- Canonical: ' + SITE.url + '/hardware/' + e.id + '/', '',
    '_Unofficial community page. Not affiliated with 37signals or the Omacom Foundation. Omarchy is a registered trademark of 37signals LLC._', '',
  ].filter((l) => l !== '').join('\n');
  const srcs = (d.sources ?? []).map((s: any) => '- [' + s.title + '](' + s.url + ')').join('\n');
  const body = head + '\n\n' + (e.body ?? '') + (srcs ? '\n\n## Sources\n\n' + srcs + '\n' : '\n');
  return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } });
};
