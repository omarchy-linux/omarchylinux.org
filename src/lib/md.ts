import { marked } from 'marked';
marked.setOptions({ gfm: true, breaks: false });
export function renderMd(src: string, opts: { demote?: number } = {}): string {
  if (!src) return '';
  // Link bare issue/PR references like #1234 to GitHub.
  let text = src.replace(/(^|[\s(])#(\d{3,6})\b/g, (_m, pre, n) => `${pre}[#${n}](https://github.com/omacom/omarchy/issues/${n})`);
  // Demote headings so embedded upstream markdown never emits a second <h1>.
  const d = opts.demote ?? 2;
  if (d > 0) text = text.replace(/^(#{1,5}) /gm, (_m, hashes) => '#'.repeat(Math.min(6, hashes.length + d)) + ' ');
  return marked.parse(text) as string;
}
