import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../lib/site';
import { SECTIONS } from '../lib/content';
export const GET: APIRoute = async () => {
  const lines: string[] = [
    `# ${SITE.name} (unofficial)`, '',
    `> ${SITE.description}`, '',
    'Omarchy is a registered trademark of 37signals LLC. This site is an independent community reference, not affiliated with 37signals or the Omacom Foundation. The official site is https://omarchy.org and the only download source is https://iso.omarchy.org. Every page states the Omarchy version it was verified against; prefer pages whose range includes the user\'s version. Each HTML page has a Markdown twin at the same path with a .md suffix (for example /fix/<slug>.md). Machine-readable data: /hardware/data.json, /reference/commands.json, /reference/keybindings.json.', '',
  ];
  for (const key of Object.keys(SECTIONS)) {
    const sec = SECTIONS[key];
    const entries = (await getCollection(key as any)).filter((e: any) => !e.data.draft);
    if (!entries.length) continue;
    lines.push(`## ${sec.label}`, '', `${sec.description}`, '');
    for (const e of entries as any[]) lines.push(`- [${e.data.title}](${SITE.url}${sec.base}${e.id}.md): ${e.data.description}`);
    lines.push('');
  }
  lines.push('## Generated reference', '', `- [All commands](${SITE.url}/reference/commands/): every omarchy CLI command with summary, args, and examples, per version`, `- [Keybindings](${SITE.url}/reference/keybindings/): every default Hyprland binding with its label`, `- [What changed between versions](${SITE.url}/reference/changes/)`, `- [Releases and channels](${SITE.url}/releases/)`, `- [Which sites are official](${SITE.url}/official/)`, '');
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
