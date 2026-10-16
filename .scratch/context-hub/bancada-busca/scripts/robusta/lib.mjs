// Biblioteca do protótipo "Robusta": chunking, embedding local (e5-small), SQLite+sqlite-vec, Orama (pt), RRF.
import { createRequire } from 'node:module';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL } from 'node:url';
const BASE = process.env.ROBUSTA_BASE || 'C:\\Projetos\\bancada-busca\\robusta';
const require = createRequire(BASE + '\\package.json');
const Database = require('better-sqlite3');
const sqliteVec = require('sqlite-vec');
const orama = await import(pathToFileURL(require.resolve('@orama/orama')).href);
const { stemmer, language: STEM_LANG } = await import(pathToFileURL(require.resolve('@orama/stemmers/portuguese')).href);
export const MODEL = process.env.ROBUSTA_MODEL || 'Xenova/multilingual-e5-small';
export const DIM = +(process.env.ROBUSTA_DIM || 384);
export const DBFILE = process.env.ROBUSTA_DB || BASE + '\\indice.db';

// ---------- embedding (local, ONNX via transformers.js; mesmo modelo quantizado do OHS)
let extractor;
export async function getExtractor() {
  if (extractor) return extractor;
  const tf = await import(pathToFileURL(require.resolve('@huggingface/transformers')).href);
  tf.env.cacheDir = path.join(os.homedir(), '.cache', 'huggingface');
  extractor = await tf.pipeline('feature-extraction', MODEL, { dtype: 'q8' });
  return extractor;
}
const isE5 = /e5/i.test(MODEL);
export async function embed(texts, kind /* 'passage'|'query' */) {
  const ex = await getExtractor();
  const pre = isE5 ? kind + ': ' : '';
  const out = await ex(texts.map(t => pre + t), { pooling: 'mean', normalize: true });
  return out.tolist().map(v => Float32Array.from(v));
}

// ---------- chunking
export function stripFrontmatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { meta: '', body: raw };
  return { meta: m[1], body: raw.slice(m[0].length) };
}
export function chunkText(raw, maxChars = 1400, overlap = 200) {
  const { meta, body } = stripFrontmatter(raw);
  const titleM = meta.match(/^title:\s*(.+)$/m) || body.match(/^#\s+(.+)$/m);
  const title = titleM ? titleM[1].replace(/^["']|["']$/g, '').trim() : '';
  const lines = body.split(/\r?\n/);
  const sections = []; let cur = { head: '', text: '' };
  const chain = [];
  for (const l of lines) {
    const h = l.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      if (cur.text.trim()) sections.push(cur);
      chain.length = h[1].length - 1; chain[h[1].length - 1] = h[2];
      cur = { head: chain.filter(Boolean).join(' > '), text: l + '\n' };
    } else cur.text += l + '\n';
  }
  if (cur.text.trim()) sections.push(cur);
  const chunks = [];
  for (const s of sections) {
    const t = s.text.trim();
    if (t.length <= maxChars) { if (t.length >= 50) chunks.push({ head: s.head, text: t }); continue; }
    let i = 0;
    while (i < t.length) {
      let end = Math.min(i + maxChars, t.length);
      if (end < t.length) { const br = t.lastIndexOf('\n', end); if (br > i + maxChars * 0.5) end = br; }
      const piece = t.slice(i, end).trim();
      if (piece.length >= 50) chunks.push({ head: s.head, text: piece });
      if (end >= t.length) break;
      i = Math.max(end - overlap, i + 1);
    }
  }
  if (!chunks.length && body.trim()) chunks.push({ head: '', text: body.trim().slice(0, maxChars) });
  return { title, chunks };
}

// ---------- SQLite + sqlite-vec
export function openDb(file = DBFILE, fresh = false) {
  const db = new Database(file);
  db.loadExtension(sqliteVec.getLoadablePath());
  db.pragma('journal_mode = WAL');
  if (fresh) db.exec('DROP TABLE IF EXISTS chunks; DROP TABLE IF EXISTS vec_chunks; DROP TABLE IF EXISTS docs; DROP TABLE IF EXISTS fts_docs; DROP TABLE IF EXISTS fts_titles; DROP TABLE IF EXISTS note_aliases;');
  db.exec(`CREATE TABLE IF NOT EXISTS docs(path TEXT PRIMARY KEY, title TEXT, rev TEXT);
    CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY, path TEXT, head TEXT, text TEXT);
    CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);
    CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(embedding float[${DIM}]);`);
  db.exec(FTS_DDL);
  return db;
}
// ---------- FTS5 (léxico alternativo ao Orama), no mesmo arquivo SQLite.
// Desenho a partir do OHS 0.16.2 (dist/src/db.js, tabela notes_fts_bm25; dist/src/searcher.js, searchBm25):
// um registro por nota, colunas título/aliases/conteúdo, unicode61 com tokenchars '+#', bm25 com pesos 10/5/1,
// consulta com cada palavra entre aspas e prefixo (*), unidas por OR. Diferença minha: remove_diacritics 2.
export const FTS_DDL = `CREATE VIRTUAL TABLE IF NOT EXISTS fts_docs USING fts5(path UNINDEXED, title, aliases, content,
  tokenize = "unicode61 remove_diacritics 2 tokenchars '+#'");
  CREATE VIRTUAL TABLE IF NOT EXISTS fts_titles USING fts5(path UNINDEXED, title, aliases, tokenize = 'trigram');
  CREATE TABLE IF NOT EXISTS note_aliases(path TEXT, alias_norm TEXT);`;
let matter; try { matter = require('gray-matter'); } catch { matter = null; }
export function ftsFields(p, raw) {
  const { meta, body } = stripFrontmatter(raw);
  let fm = {};
  if (meta && matter) { try { fm = matter(raw).data || {}; } catch { fm = {}; } }
  const tm = !fm.title && meta.match(/^title:\s*(.+)$/m);
  const title = fm.title != null ? String(fm.title) : tm ? tm[1].replace(/^["']|["']$/g, '').trim() : path.posix.basename(p, '.md');
  const al = fm.aliases == null ? [] : Array.isArray(fm.aliases) ? fm.aliases.map(String) : String(fm.aliases).split(',').map(x => x.trim());
  return { title, aliases: al.join(' '), aliasList: al, content: body };
}
export function ftsUpsert(db, p, raw) {
  const f = ftsFields(p, raw);
  db.prepare('DELETE FROM fts_docs WHERE path=?').run(p);
  db.prepare('INSERT INTO fts_docs(path,title,aliases,content) VALUES(?,?,?,?)').run(p, f.title, f.aliases, f.content);
  db.prepare('DELETE FROM fts_titles WHERE path=?').run(p);
  db.prepare('INSERT INTO fts_titles(path,title,aliases) VALUES(?,?,?)').run(p, f.title, JSON.stringify(f.aliasList));
  db.prepare('DELETE FROM note_aliases WHERE path=?').run(p);
  for (const a of f.aliasList) db.prepare('INSERT INTO note_aliases VALUES(?,?)').run(p, a.normalize('NFD').toLowerCase());
}
// Título aproximado como no OHS 0.16.2 (searcher.js: searchByAliasExact, buildTrigramOrQuery, calculateTrigramOverlap,
// searchFuzzyTitle): devolve { exact: [paths], partial: [paths] } na ordem do bm25 trigram, já filtrados (score > 0).
const trig = t => { const s = new Set(); if (t.length < 3) { s.add(t.toLowerCase()); return s; } for (let i = 0; i <= t.length - 3; i++) s.add(t.slice(i, i + 3).toLowerCase()); return s; };
const overlap = (q, t) => { const a = trig(q); if (!a.size) return 0; const b = trig(t); let m = 0; for (const x of a) if (b.has(x)) m++; return m / a.size; };
export function searchFuzzyTitle(db, q, limit = 20) {
  const exact = db.prepare('SELECT DISTINCT path FROM note_aliases WHERE alias_norm=? LIMIT ?').all(q.normalize('NFD').toLowerCase(), limit).map(r => r.path);
  const ex = new Set(exact);
  const fq = q.length < 3 ? `"${q.replace(/"/g, '')}"` : [...Array(q.length - 2).keys()].map(i => `"${q.slice(i, i + 3).replace(/"/g, '')}"`).join(' OR ');
  let partial = [];
  try {
    partial = db.prepare('SELECT path, title, aliases, bm25(fts_titles) AS r FROM fts_titles WHERE fts_titles MATCH ? ORDER BY r LIMIT ?').all(fq, limit)
      .map(r => { const al = JSON.parse(r.aliases || '[]').filter(a => a.length >= 3); const ov = Math.max(overlap(q, r.title || ''), ...al.map(a => overlap(q, a)), 0);
        return { path: r.path, s: Math.max(0, Math.abs(r.r) / (1 + Math.abs(r.r))) * ov * ov }; })
      .filter(r => r.s > 0 && !ex.has(r.path)).map(r => r.path);
  } catch { partial = []; }
  const all = [...exact, ...partial].slice(0, limit);
  return { exact: all.filter(p => ex.has(p)), partial: all.filter(p => !ex.has(p)) };
}
export function rrfW(lists, weights, k = 60, limit = 50) {
  const s = new Map();
  lists.forEach((l, li) => l.forEach((p, i) => s.set(p, (s.get(p) || 0) + (weights[li] ?? 1) / (k + i + 1))));
  return [...s.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(e => e[0]);
}
function toFtsQuery(q) {
  const w = q.replace(/["*^()]/g, ' ').replace(/\s+/g, ' ').trim().split(' ').filter(Boolean);
  return w.length ? w.map(x => `"${x}"*`).join(' OR ') : '""';
}
export function searchFts(db, q, limit = 50) {
  return db.prepare(`SELECT path, bm25(fts_docs, 0.0, 10.0, 5.0, 1.0) AS r FROM fts_docs WHERE fts_docs MATCH ? ORDER BY r LIMIT ?`)
    .all(toFtsQuery(q), limit).map(x => x.path);
}

// Indexa um documento (substitui o anterior). embedFn permite trocar o modelo na fase 2.
export async function indexDoc(db, p, raw, rev = '', embedFn = embed) {
  const { title, chunks } = chunkText(raw);
  const old = db.prepare('SELECT id FROM chunks WHERE path=?').all(p);
  const texts = chunks.map(c => `${title}${c.head ? ' | ' + c.head : ''}\n${c.text}`);
  const vecs = [];
  for (let i = 0; i < texts.length; i += 16) vecs.push(...await embedFn(texts.slice(i, i + 16), 'passage'));
  db.transaction(() => {
    for (const o of old) db.prepare('DELETE FROM vec_chunks WHERE rowid=?').run(BigInt(o.id));
    db.prepare('DELETE FROM chunks WHERE path=?').run(p);
    db.prepare('INSERT OR REPLACE INTO docs VALUES(?,?,?)').run(p, title, rev);
    chunks.forEach((c, i) => {
      const r = db.prepare('INSERT INTO chunks(path,head,text) VALUES(?,?,?)').run(p, c.head, texts[i]);
      db.prepare('INSERT INTO vec_chunks(rowid, embedding) VALUES(?,?)').run(BigInt(r.lastInsertRowid), Buffer.from(vecs[i].buffer));
    });
    ftsUpsert(db, p, raw);
  })();
  return chunks.length;
}
export function deleteDoc(db, p) {
  const old = db.prepare('SELECT id FROM chunks WHERE path=?').all(p);
  db.transaction(() => {
    for (const o of old) db.prepare('DELETE FROM vec_chunks WHERE rowid=?').run(BigInt(o.id));
    db.prepare('DELETE FROM chunks WHERE path=?').run(p);
    db.prepare('DELETE FROM docs WHERE path=?').run(p);
    db.prepare('DELETE FROM fts_docs WHERE path=?').run(p);
    db.prepare('DELETE FROM fts_titles WHERE path=?').run(p);
    db.prepare('DELETE FROM note_aliases WHERE path=?').run(p);
  })();
}

// ---------- Orama (léxico, stemmer pt) construído a partir da tabela chunks
const STOP = new Set(('a o as os um uma uns umas de do da dos das em no na nos nas por para com sem sob sobre e ou mas que se ao aos à às ' +
  'é são foi ser há como qual quais quando onde quem esse essa isso este esta isto the of and to in is are for on with by an be it that this what which how where when who does do').split(/\s+/));
export async function buildOrama(db) {
  const o = await orama.create({
    schema: { path: 'string', title: 'string', text: 'string' },
    components: { tokenizer: { stemming: true, stemmer, language: STEM_LANG, stopWords: [...STOP] } },
  });
  let rows = db.prepare('SELECT c.id,c.path,c.text,d.title FROM chunks c JOIN docs d ON d.path=c.path ORDER BY c.id').all();
  if (process.env.LEX_LEVEL === 'doc') { const m = new Map(); for (const r of rows) { const x = m.get(r.path); if (x) x.text += ' ' + r.text; else m.set(r.path, { ...r }); } rows = [...m.values()]; }
  await orama.insertMultiple(o, rows.map(r => ({ id: String(r.id), path: r.path, title: (r.title || '') + ' ' + r.path.replace(/[\/\-_.]/g, ' '), text: r.text })));
  return o;
}
function bestPerPath(items, asc = false, limit = 50) {
  const m = new Map();
  for (const it of items) {
    const cur = m.get(it.path);
    if (cur === undefined || (asc ? it.score < cur : it.score > cur)) m.set(it.path, it.score);
  }
  return [...m.entries()].sort((a, b) => asc ? a[1] - b[1] : b[1] - a[1]).slice(0, limit).map(e => e[0]);
}
export async function searchLex(o, q, limit = 50) {
  const TB = +(process.env.LEX_TITLE_BOOST ?? 0), TH = +(process.env.LEX_THRESHOLD ?? 1);
  const r = await orama.search(o, TB ? { term: q, properties: ['text', 'title'], boost: { title: TB }, threshold: TH, limit: 200 } : { term: q, properties: ['text'], threshold: TH, limit: 200 });
  return bestPerPath(r.hits.map(h => ({ path: h.document.path, score: h.score })), false, limit);
}
export async function searchVec(db, q, limit = 50, embedFn = embed) {
  const [v] = await embedFn([q], 'query');
  const rows = db.prepare(`SELECT c.path AS path, v.distance AS d FROM vec_chunks v JOIN chunks c ON c.id=v.rowid
    WHERE v.embedding MATCH ? AND k = 60 ORDER BY v.distance`).all(Buffer.from(v.buffer));
  return bestPerPath(rows.map(r => ({ path: r.path, score: r.d })), true, limit);
}
export function rrf(lists, k = 60, limit = 50) {
  const s = new Map();
  for (const l of lists) l.forEach((p, i) => s.set(p, (s.get(p) || 0) + 1 / (k + i + 1)));
  return [...s.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit).map(e => e[0]);
}
