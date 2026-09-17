import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../lib/site';
import { SECTIONS } from '../lib/content';
export async function GET(context: APIContext) {
  const items: any[] = [];
  for (const key of Object.keys(SECTIONS)) {
    const entries = await getCollection(key as any);
    for (const e of entries as any[]) {
      if (e.data.draft) continue;
      items.push({ title: e.data.title, description: e.data.description, link: `${SECTIONS[key].base}${e.id}/`, pubDate: e.data.updated ?? e.data.lastVerified, categories: [SECTIONS[key].label, ...(e.data.tags ?? [])] });
    }
  }
  items.sort((a, b) => +new Date(b.pubDate) - +new Date(a.pubDate));
  return rss({ title: `${SITE.name} (unofficial)`, description: SITE.description, site: context.site!, items: items.slice(0, 100), customData: '<language>en</language>' });
}
