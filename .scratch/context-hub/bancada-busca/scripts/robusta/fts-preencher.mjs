// Preenche só a tabela fts_docs de um índice já feito pelo disco (sem refazer embedding).
// Uso: node fts-preencher.mjs [pastaCorpus]   (ROBUSTA_DB escolhe o arquivo)
import fs from 'node:fs'; import path from 'node:path';
import { openDb, ftsUpsert } from './lib.mjs';
const root = process.argv[2] || 'C:/Projetos/bancada-busca/corpus';
const db = openDb(); const t0 = Date.now();
const paths = db.prepare('SELECT path FROM docs').all().map(r => r.path);
db.exec('DELETE FROM fts_docs');
db.transaction(() => { for (const p of paths) ftsUpsert(db, p, fs.readFileSync(path.join(root, p), 'utf8')); })();
console.log(JSON.stringify({ docs: paths.length, fts: db.prepare('SELECT count(*) n FROM fts_docs').get().n, seg: (Date.now() - t0) / 1000 }));
