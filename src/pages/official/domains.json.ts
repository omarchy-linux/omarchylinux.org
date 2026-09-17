import type { APIRoute } from 'astro';
import { domains } from '../../lib/data';
export const GET: APIRoute = () => new Response(JSON.stringify(domains(), null, 1), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
