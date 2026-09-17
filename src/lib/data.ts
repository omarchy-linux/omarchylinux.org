// Loads generated JSON from ../../data. Files may be absent during early scaffolding; every accessor degrades to empty data.
function loadAll<T = any>(globResult: Record<string, any>): Record<string, T> {
  const out: Record<string, T> = {};
  for (const [p, mod] of Object.entries(globResult)) {
    const name = p.split('/').pop()!.replace(/\.json$/, '');
    out[name] = (mod as any).default ?? mod;
  }
  return out;
}
const commandsRaw = loadAll(import.meta.glob('../../data/commands/*.json', { eager: true }));
const bindingsRaw = loadAll(import.meta.glob('../../data/bindings/*.json', { eager: true }));
const menuRaw = loadAll(import.meta.glob('../../data/menu/*.json', { eager: true }));
const migrationsRaw = loadAll(import.meta.glob('../../data/migrations/*.json', { eager: true }));
const hooksRaw = loadAll(import.meta.glob('../../data/hooks/*.json', { eager: true }));
const diffsRaw = loadAll(import.meta.glob('../../data/diffs/*.json', { eager: true }));
const rootRaw = loadAll(import.meta.glob('../../data/*.json', { eager: true }));
const issuesRaw = loadAll(import.meta.glob('../../data/issues/*.json', { eager: true }));

export const TAG_ORDER = ['v3.8.4', 'v4.0.0', 'v4.0.1', 'v4.0.2', 'v4.0.3', 'v4.0.4', 'quattro-dev'];
export function tagsAvailable(): string[] {
  return TAG_ORDER.filter((t) => t in commandsRaw);
}
export function latestTag(): string {
  const t = tagsAvailable().filter((x) => x !== 'quattro-dev');
  return t[t.length - 1] ?? 'v4.0.4';
}
export const latestVersion = () => latestTag().replace(/^v/, '');
const unwrap = (o: any, key: string): any[] => (Array.isArray(o) ? o : (o?.[key] ?? []));
export function commands(tag = latestTag()): any[] { return unwrap(commandsRaw[tag], 'commands'); }
export function commandsIndex(): any { return commandsRaw['index'] ?? { groups: {}, counts: {} }; }
export function bindings(tag = latestTag()): any[] { return unwrap(bindingsRaw[tag], 'bindings'); }
export function menu(tag = latestTag()): any { return menuRaw[tag] ?? { tree: [], flat: [] }; }
export function migrations(tag = latestTag()): any[] { return unwrap(migrationsRaw[tag], 'migrations'); }
export function newMigrationFiles(tag: string): string[] { const idx: any = migrationsRaw['index'] ?? {}; const entry = idx.byTag?.[tag]; if (!entry) return []; return (entry.new ?? []).map((x: any) => (typeof x === 'string' ? x : x.file)); }
export function migrationsIndex(): any { return migrationsRaw['index'] ?? {}; }
export function hooks(tag = latestTag()): any { return hooksRaw[tag] ?? { events: [], docs: [] }; }
export function diff(from: string, to: string): any { return diffsRaw[`${from}-to-${to}`] ?? null; }
export function diffsIndex(): any { return diffsRaw['index'] ?? { pairs: [] }; }
export function allDiffNames(): string[] { return Object.keys(diffsRaw).filter((k) => k !== 'index'); }
export const versions = (): any => rootRaw['versions'] ?? { releases: [], latest: null };
export function latestRelease(): any { const v: any = rootRaw['versions']; if (!v) return null; const tag = typeof v.latest === 'string' ? v.latest : v.latest?.tag; return (v.releases ?? []).find((r: any) => r.tag === tag) ?? (v.releases ?? [])[0] ?? null; }
export const channels = (): any => rootRaw['channels'] ?? null;
export const isos = (): any => rootRaw['isos'] ?? { isos: [] };
export const domains = (): any => rootRaw['domains'] ?? { entries: [] };
export const facts = (): any => rootRaw['facts'] ?? {};
export const issueComponents = (): any => issuesRaw['components'] ?? { components: [] };
export const issueModels = (): any => issuesRaw['models'] ?? { models: [] };
export const issueClusters = (): any => issuesRaw['clusters'] ?? { clusters: [] };
export const stillBroken = (): any => issuesRaw['still-broken'] ?? { issues: [] };
export const issueStats = (): any => issuesRaw['stats'] ?? {};
