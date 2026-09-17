import { marked } from 'marked';
marked.setOptions({ gfm: true, breaks: false });
export function renderMd(src: string): string {
  if (!src) return '';
  // Link bare issue/PR references like #1234 to GitHub.
  const linked = src.replace(/(^|[\s(])#(\d{3,6})\b/g, (_m, pre, n) => `${pre}[#${n}](https://github.com/omacom/omarchy/issues/${n})`);
  return marked.parse(linked) as string;
}
