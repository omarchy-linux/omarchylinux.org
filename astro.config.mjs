// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://omarchylinux.org',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  compressHTML: true,
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.6,
      lastmod: new Date(),
      filter: (page) => !page.includes('/search/') && !page.includes('/404'),
      serialize(item) {
        if (item.url === 'https://omarchylinux.org/') { item.priority = 1.0; item.changefreq = 'daily'; }
        if (/\/(fix|hardware|reference)\//.test(item.url)) { item.priority = 0.8; }
        return item;
      },
    }),
  ],
  markdown: {
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' }, wrap: true },
  },
});
