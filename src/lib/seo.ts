import { SITE } from './site';

export type Crumb = { name: string; href: string };

export function absolute(path: string): string {
  return new URL(path, SITE.url).toString();
}

export function websiteLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: `${SITE.name} (unofficial)`,
    alternateName: SITE.shortName,
    url: SITE.url,
    description: SITE.description,
    inLanguage: 'en',
    potentialAction: {
      '@type': 'SearchAction',
      target: { '@type': 'EntryPoint', urlTemplate: `${SITE.url}/search/?q={search_term_string}` },
      'query-input': 'required name=search_term_string',
    },
  };
}

export function breadcrumbLd(crumbs: Crumb[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((c, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: c.name,
      item: absolute(c.href),
    })),
  };
}

export function articleLd(opts: {
  type?: 'TechArticle' | 'Article' | 'HowTo';
  title: string;
  description: string;
  path: string;
  datePublished?: Date;
  dateModified?: Date;
  keywords?: string[];
  about?: string;
  proficiency?: 'Beginner' | 'Expert';
}) {
  return {
    '@context': 'https://schema.org',
    '@type': opts.type ?? 'TechArticle',
    headline: opts.title,
    description: opts.description,
    url: absolute(opts.path),
    mainEntityOfPage: absolute(opts.path),
    inLanguage: 'en',
    isAccessibleForFree: true,
    datePublished: (opts.datePublished ?? opts.dateModified ?? new Date()).toISOString(),
    dateModified: (opts.dateModified ?? new Date()).toISOString(),
    keywords: opts.keywords?.join(', '),
    about: opts.about ? { '@type': 'SoftwareApplication', name: 'Omarchy', operatingSystem: 'Linux', url: 'https://omarchy.org' } : undefined,
    proficiencyLevel: opts.proficiency,
    author: { '@type': 'Organization', name: `${SITE.name} contributors`, url: SITE.url },
    publisher: { '@type': 'Organization', name: SITE.shortName, url: SITE.url },
  };
}

export function faqLd(items: { q: string; a: string }[]) {
  if (!items.length) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
}

export function datasetLd(opts: { name: string; description: string; path: string; distribution: { url: string; format: string }[]; license?: string }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Dataset',
    name: opts.name,
    description: opts.description,
    url: absolute(opts.path),
    license: opts.license ?? 'https://creativecommons.org/publicdomain/zero/1.0/',
    creator: { '@type': 'Organization', name: SITE.shortName, url: SITE.url },
    distribution: opts.distribution.map((d) => ({ '@type': 'DataDownload', contentUrl: absolute(d.url), encodingFormat: d.format })),
  };
}

export function itemListLd(opts: { name: string; path: string; items: { name: string; url: string }[] }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: opts.name,
    url: absolute(opts.path),
    numberOfItems: opts.items.length,
    itemListElement: opts.items.slice(0, 500).map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, url: absolute(it.url) })),
  };
}

export function truncate(s: string, n = 158): string {
  const t = s.replace(/\s+/g, ' ').trim();
  if (t.length <= n) return t;
  const cut = t.slice(0, n - 1);
  return cut.slice(0, cut.lastIndexOf(' ')).replace(/[,;:]$/, '') + '…';
}
