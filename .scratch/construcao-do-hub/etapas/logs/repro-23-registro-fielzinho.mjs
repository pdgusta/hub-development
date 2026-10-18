import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { Casa } from 'file:///C:/context-hub-wt/ticket-23/agents/code/kit/par/kit/casa.mjs';
const raiz = fs.mkdtempSync(path.join(os.tmpdir(), 'hub-ensaio-23-registro-fielzinho-'));
const escrever = fs.writeFileSync;
try {
  const alvo = path.join(raiz,'config.txt');
  escrever(alvo,'original de ensaio');
  const casa = new Casa(raiz);
  fs.writeFileSync = (p,...args) => {
    if (String(p) === casa.arquivoRegistro) throw Object.assign(new Error('ENOSPC registro de ensaio'),{code:'ENOSPC'});
    return escrever(p,...args);
  };
  try { casa.escrever('config.txt','novo de ensaio','troca'); } catch(e) { console.log('falha=' + e.code); }
  finally { fs.writeFileSync = escrever; }
  console.log('registro=' + JSON.stringify(casa.lerRegistro()));
  console.log('conteudo_antes_desfazer=' + fs.readFileSync(alvo,'utf8'));
  casa.desfazer();
  console.log('conteudo_depois_desfazer=' + fs.readFileSync(alvo,'utf8'));
  console.log('copia_depois=' + fs.existsSync(path.join(raiz,'.hub-kit')));
} finally {
  fs.writeFileSync = escrever;
  if (path.dirname(raiz) !== os.tmpdir() || !path.basename(raiz).startsWith('hub-ensaio-23-registro-fielzinho-')) throw new Error('fora do ensaio');
  fs.rmSync(raiz,{recursive:true,force:true});
}
