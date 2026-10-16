// Fase 2: indexa o corpus do disco com um modelo do catálogo. Uso: node indexar-modelo.mjs <slug> [--limite N]
// Grava C:/Projetos/bancada-busca/fase2/<slug>.db (chunks, vec_chunks, docs, FTS5). Trechos ordenados por tamanho
// (lotes de 16 locais; lote do catálogo para API) para reduzir preenchimento.
import fs from 'node:fs'; import path from 'node:path';
import { createRequire } from 'node:module';
import { chunkText, ftsUpsert } from './lib.mjs';
import { carregar, API_USO } from './modelos.mjs';
const require = createRequire('C:/Projetos/bancada-busca/robusta/package.json');
const Database = require('better-sqlite3'); const sqliteVec = require('sqlite-vec');
const slug = process.argv[2]; const ROOT = 'C:/Projetos/bancada-busca/corpus';
const lim = process.argv.includes('--limite') ? +process.argv[process.argv.indexOf('--limite') + 1] : Infinity;
const OUT = `C:/Projetos/bancada-busca/fase2/${slug}.db`;
function* walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { if (e.name.startsWith('.') || e.name === 'rajada') continue;
  const p = path.join(d, e.name); if (e.isDirectory()) yield* walk(p); else if (e.name.endsWith('.md')) yield p; } }
const t0 = Date.now();
const { cfg, embed } = await carregar(slug);
const segModelo = (Date.now() - t0) / 1000;
const docs = [], items = [];
for (const f of walk(ROOT)) {
  const rel = path.relative(ROOT, f).split(path.sep).join('/'); const raw = fs.readFileSync(f, 'utf8');
  const { title, chunks } = chunkText(raw); docs.push({ rel, raw, title });
  for (const c of chunks) { const corpo = `${c.head ? c.head + '\n' : ''}${c.text}`;
    items.push({ path: rel, text: `${title}${c.head ? ' | ' + c.head : ''}\n${c.text}`, inp: cfg.d(`${title}${c.head ? ' | ' + c.head : ''}\n${c.text}`, title, corpo) }); }
}
const sel = items.slice(0, lim);
const order = sel.map((_, i) => i).sort((a, b) => sel[a].inp.length - sel[b].inp.length);
const B = cfg.api ? cfg.lote : 16; const vecs = new Array(sel.length);
const te = Date.now(); let parou = null;
for (let i = 0; i < order.length; i += B) {
  const idx = order.slice(i, i + B);
  let ok = false;
  for (let tent = 0; tent < 3 && !ok; tent++) {
    try { const v = await embed(idx.map(k => sel[k].inp), 'passage'); idx.forEach((k, j) => vecs[k] = v[j]); ok = true; }
    catch (e) { // 429: para na hora (regra da fase 2); 5xx/rede da API: espera 60 s e tenta de novo (até 3 vezes)
      if (!cfg.api || e.status === 429 || !(e.status >= 500) || tent === 2) { parou = e.message; break; }
      console.log(JSON.stringify({ nova_tentativa: tent + 1, erro: e.message.slice(0, 200) })); await new Promise(r => setTimeout(r, 60000)); }
  }
  if (parou) break;
  if (cfg.api && i + B < order.length) await new Promise(r => setTimeout(r, cfg.pausaMs));
  if ((i / B) % 20 === 0) console.log(JSON.stringify({ prog: i + idx.length, de: sel.length, seg: (Date.now() - te) / 1000 }));
}
const segEmbed = (Date.now() - te) / 1000;
if (parou) { console.log(JSON.stringify({ slug, parou, feitos: vecs.filter(Boolean).length, de: sel.length, api: API_USO })); process.exit(2); }
const DIM = vecs[0].length;
fs.mkdirSync(path.dirname(OUT), { recursive: true }); for (const x of ['', '-wal', '-shm']) fs.rmSync(OUT + x, { force: true });
const db = new Database(OUT); db.loadExtension(sqliteVec.getLoadablePath());
db.exec(`CREATE TABLE docs(path TEXT PRIMARY KEY, title TEXT, rev TEXT); CREATE TABLE chunks(id INTEGER PRIMARY KEY, path TEXT, head TEXT, text TEXT);
  CREATE INDEX chunks_path ON chunks(path); CREATE VIRTUAL TABLE vec_chunks USING vec0(embedding float[${DIM}]);
  CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);`);
process.env.ROBUSTA_DIM = String(DIM);
const { FTS_DDL } = await import('./lib.mjs'); db.exec(FTS_DDL);
db.transaction(() => {
  for (const d of docs) { db.prepare('INSERT INTO docs VALUES(?,?,?)').run(d.rel, d.title, ''); ftsUpsert(db, d.rel, d.raw); }
  sel.forEach((it, i) => { const r = db.prepare('INSERT INTO chunks(path,head,text) VALUES(?,?,?)').run(it.path, '', it.text);
    db.prepare('INSERT INTO vec_chunks(rowid, embedding) VALUES(?,?)').run(BigInt(r.lastInsertRowid), Buffer.from(vecs[i].buffer)); });
  db.prepare('INSERT INTO meta VALUES(?,?)').run('modelo', slug); db.prepare('INSERT INTO meta VALUES(?,?)').run('dim', String(DIM));
})();
db.close();
console.log(JSON.stringify({ slug, docs: docs.length, chunks: sel.length, dim: DIM, chars_entrada: sel.reduce((a, x) => a + x.inp.length, 0),
  seg_carregar_modelo: +segModelo.toFixed(1), seg_embed: +segEmbed.toFixed(1), seg_total: +((Date.now() - t0) / 1000).toFixed(1),
  ...(cfg.api ? { api: API_USO } : {}), tamanho_db_mb: +(fs.statSync(OUT).size / 1e6).toFixed(2) }));
