// Fase 2, etapa 3: reranker (cross-encoder ONNX) por cima dos 20 primeiros da híbrida de um modelo.
// Uso: node rerank.mjs <slug-embedding> <modo: hib-rrf|hib-ohs> <reranker: bge|gte>
// Texto de cada candidato: o trecho dele mais próximo da pergunta no vetor (entre os 60 vizinhos); se não houver, o 1º trecho.
// Pontua o par (pergunta, "título | cabeçalhos\ntrecho") com truncamento em 512 tokens; ordena pelo logit.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { createRequire } from 'node:module'; import { pathToFileURL } from 'node:url';
import { searchFts, searchFuzzyTitle, rrf, rrfW } from './lib.mjs';
import { carregar } from './modelos.mjs';
const require = createRequire('C:/Projetos/bancada-busca/robusta/package.json');
const Database = require('better-sqlite3'); const sqliteVec = require('sqlite-vec');
const [slug, modo, rk] = process.argv.slice(2); const BASE = 'C:/Projetos/bancada-busca';
const RK = { bge: 'onnx-community/bge-reranker-v2-m3-ONNX', gte: 'onnx-community/gte-multilingual-reranker-base' }[rk];
const Q = JSON.parse(fs.readFileSync(BASE + '/perguntas.json', 'utf8'));
const BAD = new Set(JSON.parse(fs.readFileSync(BASE + '/robusta/yaml-invalido.json', 'utf8')));
const db = new Database(`${BASE}/fase2/${slug}.db`, { readonly: true }); db.loadExtension(sqliteVec.getLoadablePath());
const { cfg, embed } = await carregar(slug);
const tf = await import(pathToFileURL(require.resolve('@huggingface/transformers')).href);
tf.env.cacheDir = path.join(os.homedir(), '.cache', 'huggingface');
const t0 = Date.now();
const tok = await tf.AutoTokenizer.from_pretrained(RK);
// gte-multilingual-reranker-base tem model_type "new", que o transformers.js 4.3.1 não mapeia para SequenceClassification;
// nesse caso carrega pela classe base (AutoModel), que roda o mesmo ONNX e devolve "logits".
let model;
try { model = await tf.AutoModelForSequenceClassification.from_pretrained(RK, { dtype: 'q8' }); }
catch (e) { console.error('fallback AutoModel:', e.message); model = await tf.AutoModel.from_pretrained(RK, { dtype: 'q8' }); }
const segCarregar = (Date.now() - t0) / 1000;
const stVec = db.prepare(`SELECT c.id, c.path AS path, v.distance AS d FROM vec_chunks v JOIN chunks c ON c.id=v.rowid WHERE v.embedding MATCH ? AND k = 60 ORDER BY v.distance`);
const firstChunk = db.prepare('SELECT text FROM chunks WHERE path=? ORDER BY id LIMIT 1'); const byId = db.prepare('SELECT text FROM chunks WHERE id=?');
async function score(q, texts) {
  const out = []; for (let i = 0; i < texts.length; i += 10) {
    const part = texts.slice(i, i + 10);
    const inp = tok(part.map(() => q), { text_pair: part, padding: true, truncation: true, max_length: 512 });
    const { logits } = await model(inp); const d = logits.data; const C = logits.dims[1] || 1;
    for (let j = 0; j < part.length; j++) out.push(d[j * C + (C - 1)]);
  } return out;
}
const agg = (rows, sel) => { const s = rows.filter(sel); return { n: s.length, hit5: +(s.filter(r => r.rank).length / s.length).toFixed(3),
  mrr: +(s.reduce((a, r) => a + (r.rank ? 1 / r.rank : 0), 0) / s.length).toFixed(3) }; };
const res = {}; const tempos = [];
await score('aquecer', ['aquecer o modelo']);
for (const base of ['124', 'sem12']) {
  const f = l => base === 'sem12' ? l.filter(p => !BAD.has(p)) : l;
  const rowsAntes = [], rowsDepois = [];
  for (const q of Q) {
    const [v] = await embed([cfg.q + q.q]);
    const vrows = stVec.all(Buffer.from(v.buffer)); const best = new Map(); const vec = [];
    for (const r of vrows) if (!best.has(r.path)) { best.set(r.path, r.id); vec.push(r.path); }
    const lex = searchFts(db, q.q, 50); const fz = searchFuzzyTitle(db, q.q, 20);
    const top = (modo === 'hib-ohs' ? rrfW([f(vec).slice(0, 20), f(lex).slice(0, 20), f(fz.exact), f(fz.partial)], [1.5, 1.5, 2.0, 0.25]) : rrf([f(lex), f(vec)])).slice(0, 20);
    const texts = top.map(p => best.has(p) ? byId.get(best.get(p)).text : (firstChunk.get(p)?.text || p));
    const t = Date.now(); const s = await score(q.q, texts); if (base === '124') tempos.push(Date.now() - t);
    const re = top.map((p, i) => [p, s[i]]).sort((a, b) => b[1] - a[1]).map(x => x[0]);
    const mk = (lst) => { const k = lst.slice(0, 5).findIndex(p => q.files.includes(p)); return { n: q.n, tipo: q.tipo, lang: q.lang, q: q.q, esperado: q.files, top5: lst.slice(0, 5), rank: k < 0 ? null : k + 1 }; };
    rowsAntes.push(mk(top)); rowsDepois.push(mk(re));
  }
  for (const [nome, rows] of [['antes', rowsAntes], ['depois', rowsDepois]]) {
    const met = { total: agg(rows, () => true), L: agg(rows, r => r.tipo === 'L'), P: agg(rows, r => r.tipo === 'P'), pt: agg(rows, r => r.lang === 'pt'), en: agg(rows, r => r.lang === 'en') };
    res[`${nome}-${base}`] = met;
    if (nome === 'depois') fs.writeFileSync(`${BASE}/resultados/fase2-rerank-${rk}-${slug}-${modo}-${base}.json`, JSON.stringify({ metricas: met, perguntas: rows }, null, 1));
  }
}
const s = [...tempos].sort((a, b) => a - b);
const out = { slug, modo, reranker: RK, seg_carregar: segCarregar, ms_rerank20_mediana: s[Math.floor(s.length / 2)], ms_rerank20_max: s[s.length - 1], rss_mb: Math.round(process.memoryUsage().rss / 1048576), ...res };
fs.appendFileSync(`${BASE}/fase2/rerank.jsonl`, JSON.stringify(out) + '\n'); console.log(JSON.stringify(out));
