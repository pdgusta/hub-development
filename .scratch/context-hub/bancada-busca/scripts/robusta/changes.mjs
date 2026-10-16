// Consumidor do _changes do CouchDB do LiveSync -> índice Robusta. Com --e2ee, decifra no próprio Node.
// Uso (via lancar-changes.py, que injeta COUCH_AUTH e, com --e2ee, E2EE_PASSPHRASE, sem imprimir):
//   node changes.mjs <banco> [--fresh] [--e2ee] [--dump <pasta>] [--no-embed] [--wait <seg>]
// Estado em <ROBUSTA_DB>.seq. --dump grava o texto montado de cada nota (para diff). --no-embed só monta/decifra.
// --wait: fica em feed=longpoll a partir do seq guardado até indexar ao menos uma nota (ou estourar o prazo).
//
// Decifragem (E2EE v2/HKDF), seguindo o código da livesync-commonlib 0.1.36 (a lib que o LiveSync e o MCP do
// es617 usam; README do es617), em livesync-src/node_modules/@vrtmrz/livesync-commonlib/dist/:
//  - pouchdb/encryption.js, outgoingDecryptHKDF: chunk (h:) com data "%=..." -> decryptHKDF(data, passphrase, salt);
//    meta com path "/\:..." -> decryptMetaWithHKDF -> JSON {path, mtime, ctime, size, children};
//    eden em eden["h:++encrypted-hkdf"].data -> JSON com os chunks embutidos.
//  - replication/SyncParamsHandler.js: o sal PBKDF2 vem de _local/obsidian_livesync_sync_parameters (pbkdf2salt, base64).
//  - worker/bgWorker.direct.js: decryptHKDFWorker = decrypt de octagonal-wheels/encryption/hkdf (importado aqui).
import fs from 'node:fs'; import path from 'node:path'; import { pathToFileURL } from 'node:url';
import { openDb, indexDoc, deleteDoc, getExtractor } from './lib.mjs';
const S = process.env.COUCH_URL || 'http://127.0.0.1:5984';
const AUTH = process.env.COUCH_AUTH; // "Basic ..."
const args = process.argv.slice(2);
const dbname = args[0] || 'bancada';
const fresh = args.includes('--fresh'), E2EE = args.includes('--e2ee'), noEmbed = args.includes('--no-embed');
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const dumpDir = opt('--dump'), waitSec = +(opt('--wait') || 0);
const DBF = process.env.ROBUSTA_DB || 'C:/Projetos/bancada-busca/robusta/indice.db';
const seqFile = DBF + '.seq';
const hdr = { Authorization: AUTH, Accept: 'application/json', 'Content-Type': 'application/json' };
const j = async (url, body) => {
  const r = await fetch(S + url, body ? { method: 'POST', headers: hdr, body: JSON.stringify(body) } : { headers: hdr });
  if (!r.ok) throw new Error(url.split('?')[0] + ' -> ' + r.status);
  return r.json();
};
const t0 = Date.now();
const db = noEmbed ? null : openDb(DBF, fresh);
if (db) db.exec('CREATE TABLE IF NOT EXISTS ids(id TEXT PRIMARY KEY, path TEXT)');
if (!noEmbed) await getExtractor();
const segModelo = (Date.now() - t0) / 1000;

// ---------- E2EE
let dec = async x => x, salt = null, pass = null, segDecifrar = 0;
if (E2EE) {
  pass = process.env.E2EE_PASSPHRASE; if (!pass) throw new Error('E2EE_PASSPHRASE ausente');
  const OW = process.env.OW_HKDF || 'C:/Projetos/spike-livesync/livesync-src/node_modules/octagonal-wheels/dist/encryption/hkdf.js';
  const { decrypt } = await import(pathToFileURL(OW).href);
  const sp = await j(`/${dbname}/_local/obsidian_livesync_sync_parameters`);
  salt = new Uint8Array(Buffer.from(sp.pbkdf2salt, 'base64'));
  dec = async s => { const t = Date.now(); const r = await decrypt(s, pass, salt); segDecifrar += (Date.now() - t) / 1000; return r; };
}
const META = '/\\:', EDEN_HKDF = 'h:++encrypted-hkdf';
async function openMeta(d) {
  d = { ...d };
  if (E2EE && typeof d.path === 'string' && d.path.startsWith(META)) Object.assign(d, JSON.parse(await dec(d.path.slice(META.length))));
  let eden = d.eden || {};
  if (E2EE && eden[EDEN_HKDF]) eden = JSON.parse(await dec(eden[EDEN_HKDF].data));
  d.eden = eden;
  return d;
}
const chunkText = async c => (E2EE && c.e_ && typeof c.data === 'string' && c.data.startsWith('%=')) ? dec(c.data) : c.data;

// ---------- uma passada
let since = fresh || !fs.existsSync(seqFile) ? 0 : fs.readFileSync(seqFile, 'utf8').trim();
const st = { linhas_changes: 0, indexados: 0, apagados: 0, ignorados: 0, erros: 0, seg_ler_changes: 0, seg_montar_texto: 0, seg_indexar_embed: 0 };
const feedChunks = new Map();
async function pass1(feed) {
  const tc = Date.now();
  const ch = await j(`/${dbname}/_changes?include_docs=true&since=${encodeURIComponent(since)}${feed}`);
  st.seg_ler_changes += (Date.now() - tc) / 1000; st.linhas_changes += ch.results.length;
  for (const row of ch.results) if (row.id.startsWith('h:') && row.doc) feedChunks.set(row.id, row.doc);
  for (const row of ch.results) {
    const id = row.id; const raw = row.doc;
    if (id.startsWith('h:') || id.startsWith('_design') || !raw) continue;
    if (raw._deleted) { const r = db?.prepare('SELECT path FROM ids WHERE id=?').get(id); if (r) { deleteDoc(db, r.path); st.apagados++; } continue; }
    try {
      const tm = Date.now();
      const d = await openMeta(raw);
      const p = d.path || id;
      if (!p.endsWith('.md')) { st.ignorados++; continue; }
      if (d.deleted) { if (db) deleteDoc(db, p); st.apagados++; continue; }
      if (d.type !== 'plain') { st.ignorados++; continue; }
      const ids = d.children || [];
      const got = new Map(Object.entries(d.eden).map(([k, v]) => [k, v.data]));
      for (const c of ids) if (!got.has(c) && feedChunks.has(c)) got.set(c, await chunkText(feedChunks.get(c)));
      const missing = ids.filter(c => !got.has(c));
      if (missing.length) {
        const r = await j(`/${dbname}/_all_docs?include_docs=true`, { keys: missing });
        for (const x of r.rows) if (x.doc) got.set(x.id, await chunkText(x.doc));
      }
      const text = ids.map(c => got.get(c) ?? '').join('');
      st.seg_montar_texto += (Date.now() - tm) / 1000;
      if (dumpDir) { const f = path.join(dumpDir, p); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, text); }
      if (db) {
        const te = Date.now();
        await indexDoc(db, p, text, d._rev);
        db.prepare('INSERT OR REPLACE INTO ids VALUES(?,?)').run(id, p);
        st.seg_indexar_embed += (Date.now() - te) / 1000;
        console.log(JSON.stringify({ indexado: p, rev: d._rev, ts: Date.now() }));
      }
      st.indexados++;
    } catch (e) { st.erros++; console.error('erro', id, e.message); }
  }
  since = ch.last_seq;
  if (!noEmbed) fs.writeFileSync(seqFile, String(since));
}
if (waitSec) {
  const fim = Date.now() + waitSec * 1000;
  while (st.indexados === 0 && Date.now() < fim) await pass1(`&feed=longpoll&timeout=${Math.max(1000, fim - Date.now())}`);
} else await pass1('');
const r = x => +x.toFixed(2);
console.log(JSON.stringify({ banco: dbname, e2ee: E2EE, ...st, seg_ler_changes: r(st.seg_ler_changes), seg_montar_texto: r(st.seg_montar_texto),
  seg_decifrar: r(segDecifrar), seg_indexar_embed: +st.seg_indexar_embed.toFixed(1), seg_carregar_modelo: r(segModelo),
  seg_total: +((Date.now() - t0) / 1000).toFixed(1), ts_fim: Date.now() }));
