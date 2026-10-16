// Fase 2: avalia um índice fase2/<slug>.db nas 40 perguntas: só vetor, híbrida RRF (2 listas, pesos iguais, 50 itens, como
// na fase 1) e híbrida "fusão OHS" (OHS 0.16.2, searcher.js: vetor, bm25, alias exato, título aproximado; 20 itens cada;
// pesos 1,5 / 1,5 / 2,0 / 0,25; k=60). Cada modo em 124 arquivos e "sem os 12".
// Uso: node avaliar-modelo.mjs <slug>   -> resultados/fase2-<slug>-<modo>-<base>.json e uma linha JSON de resumo.
import fs from 'node:fs';
import { createRequire } from 'node:module';
import { searchFts, searchFuzzyTitle, rrf, rrfW } from './lib.mjs';
import { carregar, API_USO } from './modelos.mjs';
const require = createRequire('C:/Projetos/bancada-busca/robusta/package.json');
const Database = require('better-sqlite3'); const sqliteVec = require('sqlite-vec');
const slug = process.argv[2]; const BASE = 'C:/Projetos/bancada-busca';
const Q = JSON.parse(fs.readFileSync(BASE + '/perguntas.json', 'utf8'));
const BAD = new Set(JSON.parse(fs.readFileSync(BASE + '/robusta/yaml-invalido.json', 'utf8')));
const db = new Database(`${BASE}/fase2/${slug}.db`, { readonly: true }); db.loadExtension(sqliteVec.getLoadablePath());
const { cfg, embed } = await carregar(slug);
// vetores das perguntas (local: uma por vez, medindo; API: um lote só, para poupar cota)
const qv = []; const tq = [];
if (cfg.api) { const t = Date.now(); qv.push(...await embed(Q.map(q => cfg.q + q.q))); tq.push((Date.now() - t) / Q.length); }
else { await embed([cfg.q + 'aquecer']); for (const q of Q) { const t = Date.now(); qv.push((await embed([cfg.q + q.q]))[0]); tq.push(Date.now() - t); } }
const stVec = db.prepare(`SELECT c.path AS path, v.distance AS d FROM vec_chunks v JOIN chunks c ON c.id=v.rowid WHERE v.embedding MATCH ? AND k = 60 ORDER BY v.distance`);
const tb = []; const lists = Q.map((q, i) => {
  const t = Date.now();
  const rows = stVec.all(Buffer.from(qv[i].buffer)); const seen = new Set(); const vec = [];
  for (const r of rows) if (!seen.has(r.path)) { seen.add(r.path); vec.push(r.path); }
  const lex = searchFts(db, q.q, 50); const fz = searchFuzzyTitle(db, q.q, 20);
  tb.push(Date.now() - t);
  return { vec, lex, fz };
});
const agg = (rows, sel) => { const s = rows.filter(sel); return { n: s.length, hit5: +(s.filter(r => r.rank).length / s.length).toFixed(3),
  mrr: +(s.reduce((a, r) => a + (r.rank ? 1 / r.rank : 0), 0) / s.length).toFixed(3) }; };
const resumo = { slug };
for (const base of ['124', 'sem12']) {
  const f = l => base === 'sem12' ? l.filter(p => !BAD.has(p)) : l;
  const modos = {
    vec: L => f(L.vec),
    'hib-rrf': L => rrf([f(L.lex), f(L.vec)]),
    'hib-ohs': L => rrfW([f(L.vec).slice(0, 20), f(L.lex).slice(0, 20), f(L.fz.exact), f(L.fz.partial)], [1.5, 1.5, 2.0, 0.25]),
  };
  for (const [m, fn] of Object.entries(modos)) {
    const rows = Q.map((q, i) => { const top = fn(lists[i]).slice(0, 5); const k = top.findIndex(p => q.files.includes(p));
      return { n: q.n, tipo: q.tipo, lang: q.lang, q: q.q, esperado: q.files, top5: top, rank: k < 0 ? null : k + 1 }; });
    const met = { total: agg(rows, () => true), L: agg(rows, r => r.tipo === 'L'), P: agg(rows, r => r.tipo === 'P'), pt: agg(rows, r => r.lang === 'pt'), en: agg(rows, r => r.lang === 'en') };
    fs.writeFileSync(`${BASE}/resultados/fase2-${slug}-${m}-${base}.json`, JSON.stringify({ config: `fase2-${slug}-${m}-${base}`, metricas: met, perguntas: rows }, null, 1));
    resumo[`${m}-${base}`] = met;
  }
}
const med = a => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
resumo.ms_embed_consulta_mediana = med(tq); resumo.ms_busca_mediana = med(tb);
if (cfg.api) resumo.api = API_USO;
fs.appendFileSync(`${BASE}/fase2/avaliacao.jsonl`, JSON.stringify(resumo) + '\n');
console.log(JSON.stringify(resumo));
