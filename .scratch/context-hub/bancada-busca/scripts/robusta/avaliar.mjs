// Uso: node avaliar.mjs <rotulo> ; roda as 40 perguntas em lex / vec / hibrida
// LEX_ENGINE=fts5 troca o léxico do Orama pela FTS5 (tabela fts_docs do mesmo SQLite).
// e grava C:\Projetos\bancada-busca\resultados\robusta-<rotulo>-<modo>.json (mesmo formato do avaliar.py).
import fs from 'node:fs';
import { openDb, buildOrama, searchLex, searchFts, searchVec, rrf } from './lib.mjs';
const FTS = process.env.LEX_ENGINE === 'fts5';
const BASE = 'C:\\Projetos\\bancada-busca'; const rot = process.argv[2] || 'e5';
const Q = JSON.parse(fs.readFileSync(BASE + '\\perguntas.json', 'utf8'));
const db = openDb(); const tO = Date.now(); const o = FTS ? null : await buildOrama(db); const segOrama = (Date.now() - tO) / 1000;
await searchVec(db, 'aquecer'); // carrega o modelo fora da medição
const agg = (rows, sel) => {
  const s = rows.filter(sel); if (!s.length) return null;
  return { n: s.length, hit5: +(s.filter(r => r.rank).length / s.length).toFixed(3),
    mrr: +(s.reduce((a, r) => a + (r.rank ? 1 / r.rank : 0), 0) / s.length).toFixed(3) };
};
// EXCLUI_YAML=1: tira dos resultados os 12 arquivos que o OHS não indexou (mesmo conjunto de candidatos)
const bad = new Set(process.env.EXCLUI_YAML ? JSON.parse(fs.readFileSync(BASE + '/robusta/yaml-invalido.json', 'utf8')) : []);
const lx = async q => (FTS ? searchFts(db, q) : await searchLex(o, q)).filter(p => !bad.has(p));
const vc = async q => (await searchVec(db, q)).filter(p => !bad.has(p));
const modes = { lex: lx, vec: vc, hibrida: async q => rrf([await lx(q), await vc(q)]) };
fs.mkdirSync(BASE + '\\resultados', { recursive: true });
for (const [m, fn] of Object.entries(modes)) {
  const rows = []; const t = Date.now();
  for (const q of Q) {
    const top = (await fn(q.q)).slice(0, 5); const i = top.findIndex(p => q.files.includes(p));
    rows.push({ n: q.n, tipo: q.tipo, lang: q.lang, q: q.q, esperado: q.files, top5: top, rank: i < 0 ? null : i + 1 });
  }
  const res = { config: `robusta-${rot}-${m}`, segundos: +((Date.now() - t) / 1000).toFixed(2), seg_montar_orama: segOrama,
    metricas: { total: agg(rows, () => true), L: agg(rows, r => r.tipo === 'L'), P: agg(rows, r => r.tipo === 'P'),
      pt: agg(rows, r => r.lang === 'pt'), en: agg(rows, r => r.lang === 'en') }, perguntas: rows };
  fs.writeFileSync(BASE + `\\resultados\\robusta-${rot}-${m}.json`, JSON.stringify(res, null, 1));
  console.log(res.config, JSON.stringify(res.metricas), res.segundos + 's');
}
