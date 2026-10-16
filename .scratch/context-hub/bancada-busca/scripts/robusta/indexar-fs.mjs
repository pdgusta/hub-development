// Indexa o corpus pelo disco. Uso: node indexar-fs.mjs [pastaCorpus]
import fs from 'node:fs'; import path from 'node:path';
import { openDb, indexDoc, getExtractor } from './lib.mjs';
const root = process.argv[2] || 'C:\\Projetos\\bancada-busca\\corpus';
function* walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.name.startsWith('.') || e.name === 'rajada') continue;
    const p = path.join(d, e.name);
    if (e.isDirectory()) yield* walk(p); else if (e.name.endsWith('.md')) yield p;
  }
}
const t0 = Date.now();
const db = openDb(undefined, true);
await getExtractor(); const tModel = Date.now();
let n = 0, ch = 0;
for (const f of walk(root)) {
  const rel = path.relative(root, f).replace(/\\/g, '/');
  ch += await indexDoc(db, rel, fs.readFileSync(f, 'utf8')); n++;
}
console.log(JSON.stringify({ docs: n, chunks: ch, seg_total: +((Date.now() - t0) / 1000).toFixed(1),
  seg_carregar_modelo: +((tModel - t0) / 1000).toFixed(1), seg_indexar: +((Date.now() - tModel) / 1000).toFixed(1) }));
