import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const source = z.object({
  url: z.string().url(),
  title: z.string(),
  kind: z.enum(['issue', 'discussion', 'pr', 'manual', 'release', 'commit', 'blog', 'reddit', 'video', 'docs', 'other']).default('other'),
  author: z.string().optional(),
  date: z.string().optional(),
});

const credit = z.object({ name: z.string(), url: z.string().url().optional(), for: z.string().optional() });
const faq = z.object({ q: z.string(), a: z.string() });

const base = {
  title: z.string(),
  description: z.string().min(40).max(200),
  answer: z.string().min(20),
  appliesTo: z.object({ from: z.string(), to: z.string().optional() }).default({ from: '4.0.0' }),
  status: z.enum(['open', 'fixed', 'workaround', 'by-design', 'info', 'works', 'partial', 'broken', 'unknown']).default('info'),
  fixedIn: z.string().optional(),
  lastVerified: z.coerce.date(),
  omarchyVersionTested: z.string().optional(),
  tags: z.array(z.string()).default([]),
  sources: z.array(source).default([]),
  credits: z.array(credit).default([]),
  faq: z.array(faq).default([]),
  related: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
  updated: z.coerce.date().optional(),
};

const article = z.object(base);

const fix = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/fix' }),
  schema: z.object({
    ...base,
    errorStrings: z.array(z.string()).default([]),
    category: z.enum(['boot', 'update', 'display', 'audio', 'network', 'input', 'apps', 'agents', 'gaming', 'shell', 'security', 'install', 'other']).default('other'),
    issueCount: z.number().int().optional(),
  }),
});

const subsystem = z.enum(['works', 'partial', 'broken', 'unknown', 'n/a']);

const hardware = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/hardware' }),
  schema: z.object({
    ...base,
    kind: z.enum(['component', 'model', 'vendor']),
    componentKey: z.string().optional(),
    vendor: z.string().optional(),
    model: z.string().optional(),
    dmi: z.array(z.string()).default([]),
    year: z.string().optional(),
    cpu: z.string().optional(),
    gpu: z.string().optional(),
    rating: z.enum(['gold', 'silver', 'bronze', 'broken', 'experimental', 'unrated']).default('unrated'),
    subsystems: z.object({
      wifi: subsystem.default('unknown'), bluetooth: subsystem.default('unknown'), audio: subsystem.default('unknown'),
      webcam: subsystem.default('unknown'), fingerprint: subsystem.default('unknown'), gpu: subsystem.default('unknown'),
      suspend: subsystem.default('unknown'), hibernate: subsystem.default('unknown'), touchpad: subsystem.default('unknown'),
      display: subsystem.default('unknown'), battery: subsystem.default('unknown'), keyboard: subsystem.default('unknown'),
    }).default({}),
    quirkScripts: z.array(z.object({ name: z.string(), url: z.string().url(), note: z.string().optional() })).default([]),
    issueCount: z.number().int().optional(),
  }),
});

const collections = {
  fix,
  hardware,
  switch: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/switch' }), schema: article }),
  security: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/security' }), schema: z.object({ ...base, severity: z.enum(['critical', 'high', 'medium', 'low', 'info']).default('info'), reported: z.string().optional(), projectResponse: z.string().optional() }) }),
  keyboard: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/keyboard' }), schema: article }),
  vs: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/vs' }), schema: z.object({ ...base, other: z.string(), otherVersion: z.string().optional() }) }),
  upgrade: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/upgrade' }), schema: article }),
  official: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/official' }), schema: article }),
  reference: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/reference' }), schema: article }),
  run: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/run' }), schema: z.object({ ...base, platform: z.string(), hostVersion: z.string().optional() }) }),
  pages: defineCollection({ loader: glob({ pattern: '**/*.md', base: './src/content/pages' }), schema: z.object({ title: z.string(), description: z.string(), lastVerified: z.coerce.date().optional(), draft: z.boolean().default(false) }) }),
};

export { collections };
