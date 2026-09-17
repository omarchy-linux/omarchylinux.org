import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { issueComponents, issueModels } from '../../lib/data';
export const GET: APIRoute = async () => {
  const hw = (await getCollection('hardware')).filter((e: any) => !e.data.draft);
  const out = {
    license: 'CC0-1.0', source: 'https://omarchylinux.org/hardware/', generated: new Date().toISOString(),
    models: hw.filter((e: any) => e.data.kind === 'model').map((e: any) => ({ slug: e.id, url: `https://omarchylinux.org/hardware/${e.id}/`, title: e.data.title, vendor: e.data.vendor, model: e.data.model, dmi: e.data.dmi, cpu: e.data.cpu, gpu: e.data.gpu, rating: e.data.rating, subsystems: e.data.subsystems, quirkScripts: e.data.quirkScripts, appliesTo: e.data.appliesTo, omarchyVersionTested: e.data.omarchyVersionTested, lastVerified: e.data.lastVerified, issueCount: e.data.issueCount })),
    components: hw.filter((e: any) => e.data.kind === 'component').map((e: any) => ({ slug: e.id, url: `https://omarchylinux.org/hardware/${e.id}/`, title: e.data.title, status: e.data.status, issueCount: e.data.issueCount })),
    upstreamIssueCounts: { components: (issueComponents().components ?? []).map((c: any) => ({ key: c.key, counts: c.counts })), models: (issueModels().models ?? []).map((m: any) => ({ key: m.key, vendor: m.vendor, model: m.model, counts: m.counts })) },
  };
  return new Response(JSON.stringify(out, null, 1), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
