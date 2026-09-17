import { getCollection, type CollectionKey } from 'astro:content';

export const SECTIONS: Record<string, { base: string; label: string; description: string }> = {
  fix: { base: '/fix/', label: 'Fixes', description: 'One page per real Omarchy error, with the fix first and the version it applies to.' },
  hardware: { base: '/hardware/', label: 'Hardware', description: 'Does Omarchy run on this machine? Component and model reports, stamped by version.' },
  switch: { base: '/switch/', label: 'Switching', description: 'Coming from macOS or Windows: what blocks you on day one and what replaces what.' },
  security: { base: '/security/', label: 'Security', description: 'Every reported Omarchy security issue mapped to the fix and the release it shipped in.' },
  keyboard: { base: '/keyboard/', label: 'Keyboards and input', description: 'Layouts, locale, and typing in Chinese, Japanese, and Korean on Omarchy 4.' },
  vs: { base: '/vs/', label: 'Comparisons', description: 'Omarchy against the distros people actually decide between, verified against versions.' },
  upgrade: { base: '/upgrade/', label: 'Upgrades', description: 'What an Omarchy upgrade does to your machine and what to do before and after.' },
  official: { base: '/official/', label: 'Is it official?', description: 'Which Omarchy sites, domains, and accounts are official, and the trademark facts.' },
  reference: { base: '/reference/', label: 'Reference', description: 'Commands, keybindings, menu tree, hooks, and config, generated from source per version.' },
  run: { base: '/run/', label: 'Run anywhere', description: 'Omarchy in VirtualBox, VMware, Proxmox, Hyper-V, Apple Silicon, and more, with verdicts.' },
};

export async function visible<K extends CollectionKey>(key: K) {
  const all = await getCollection(key);
  return all.filter((e: any) => !e.data.draft).sort((a: any, b: any) => (a.data.title ?? a.id).localeCompare(b.data.title ?? b.id));
}

export function versionRangeLabel(r?: { from: string; to?: string }): string {
  if (!r) return '4.x';
  if (r.from === '3.x' && !r.to) return '3.x';
  if (!r.to) return `${r.from} and later`;
  if (r.from === r.to) return r.from;
  return `${r.from} – ${r.to}`;
}

export function fmtDate(d: Date | string | undefined): string {
  if (!d) return '';
  const dt = typeof d === 'string' ? new Date(d) : d;
  return dt.toISOString().slice(0, 10);
}
