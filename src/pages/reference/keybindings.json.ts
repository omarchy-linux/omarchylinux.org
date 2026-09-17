import type { APIRoute } from 'astro';
import { bindings, latestTag } from '../../lib/data';
export const GET: APIRoute = () => new Response(JSON.stringify({ tag: latestTag(), generatedFrom: 'https://github.com/omacom/omarchy', license: 'CC0 (data); MIT (upstream source)', bindings: bindings() }, null, 1), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
