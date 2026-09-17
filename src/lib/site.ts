export const SITE = {
  url: 'https://omarchylinux.org',
  name: 'Omarchy Linux Field Manual',
  shortName: 'omarchylinux.org',
  tagline: 'Does it run on my hardware? What broke in this version? How do I fix this error?',
  description:
    'Unofficial, version-stamped reference for Omarchy Linux: hardware compatibility reports, error fixes, the full command and keybinding reference, and what changed between releases. Not affiliated with 37signals or the Omacom Foundation.',
  repo: 'https://github.com/omarchylinux/omarchylinux.org',
  editBase: 'https://github.com/omarchylinux/omarchylinux.org/edit/main/',
  contact: 'hello@omarchylinux.org',
  official: {
    site: 'https://omarchy.org',
    iso: 'https://iso.omarchy.org',
    github: 'https://github.com/omacom/omarchy',
    discord: 'https://discord.gg/tXFUdasqhY',
    manual: 'https://omarchy.org/manual/',
    plugins: 'https://plugins.omarchy.org',
  },
  disclaimerShort:
    'Unofficial community site. Not affiliated with or endorsed by 37signals or the Omacom Foundation. We never host installers; download Omarchy only from omarchy.org.',
  disclaimerLong:
    'Omarchy is a registered trademark of 37signals LLC (US Reg. No. 8250209). omarchylinux.org is an independent community project and is not affiliated with, endorsed by, or sponsored by 37signals, the Omacom Foundation, or David Heinemeier Hansson. The official site is omarchy.org. We do not host ISOs, installers, or mirrors.',
  trademark: { owner: '37signals LLC', reg: '8250209', serial: '99322411', registered: '2026-05-12' },
};

export const NAV = [
  { href: '/hardware/', label: 'Hardware' },
  { href: '/fix/', label: 'Fixes' },
  { href: '/reference/', label: 'Reference' },
  { href: '/releases/', label: 'Releases' },
  { href: '/switch/', label: 'Switching' },
  { href: '/official/', label: 'Is it official?' },
];

export const FOOTER_GROUPS = [
  { title: 'Answers', links: [
    { href: '/hardware/', label: 'Hardware compatibility' },
    { href: '/fix/', label: 'Error fixes' },
    { href: '/switch/', label: 'Coming from macOS or Windows' },
    { href: '/keyboard/', label: 'Keyboards, layouts, and input methods' },
    { href: '/run/', label: 'Run Omarchy in a VM' },
    { href: '/vs/', label: 'Omarchy vs other distros' },
  ]},
  { title: 'Reference', links: [
    { href: '/reference/commands/', label: 'All omarchy commands' },
    { href: '/reference/keybindings/', label: 'Keybindings' },
    { href: '/reference/menu/', label: 'Menu tree' },
    { href: '/reference/changes/', label: 'What changed between versions' },
    { href: '/upgrade/3-to-4-quattro/', label: 'Upgrading 3.x to 4 (Quattro)' },
    { href: '/releases/', label: 'Releases and channels' },
  ]},
  { title: 'Trust', links: [
    { href: '/official/', label: 'Which Omarchy sites are official?' },
    { href: '/official/trademark/', label: 'Trademark facts' },
    { href: '/verify/', label: 'Verify an ISO' },
    { href: '/security/', label: 'Security status' },
    { href: '/about/', label: 'About this site' },
    { href: '/contribute/', label: 'Contribute' },
  ]},
];
