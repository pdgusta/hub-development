// Fase 2: carrega cada modelo, mede um lote de 16 trechos reais (dos maiores) e estima a indexação. Uso: node sonda.mjs slug...
import fs from 'node:fs'; import path from 'node:path';
import { chunkText } from './lib.mjs';
import { carregar } from './modelos.mjs';
const ROOT = 'C:/Projetos/bancada-busca/corpus'; const items = [];
function* walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { if (e.name.startsWith('.') || e.name === 'rajada') continue;
  const p = path.join(d, e.name); if (e.isDirectory()) yield* walk(p); else if (e.name.endsWith('.md')) yield p; } }
for (const f of walk(ROOT)) { const { title, chunks } = chunkText(fs.readFileSync(f, 'utf8')); for (const c of chunks) items.push(`${title}${c.head ? ' | ' + c.head : ''}\n${c.text}`); }
items.sort((a, b) => a.length - b.length);
const med = items.slice(Math.floor(items.length / 2) - 8, Math.floor(items.length / 2) + 8);
for (const slug of process.argv.slice(2)) {
  const t0 = Date.now();
  try {
    const { cfg, embed } = await carregar(slug); const tl = (Date.now() - t0) / 1000;
    await embed(med.slice(0, 2).map(x => cfg.d(x, 'T', x)));
    const t1 = Date.now(); const v = await embed(med.map(x => cfg.d(x, 'T', x))); const tb = (Date.now() - t1) / 1000;
    const q = await embed([cfg.q + 'teste de consulta']);
    console.log(JSON.stringify({ slug, ok: true, dim: v[0].length, seg_carregar: tl, seg_lote16_mediano: tb, estimativa_min: +(tb * items.length / 16 / 60).toFixed(1), cos_q_d: +[...q[0]].reduce((a, x, i) => a + x * v[0][i], 0).toFixed(3), rss_mb: Math.round(process.memoryUsage().rss / 1048576) }));
  } catch (e) { console.log(JSON.stringify({ slug, ok: false, erro: String(e.message || e).slice(0, 400), seg: (Date.now() - t0) / 1000 })); }
}
console.log(JSON.stringify({ fim: true, trechos: items.length }));
