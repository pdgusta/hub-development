import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { Casa } from 'file:///C:/context-hub-wt/ticket-23/agents/code/kit/par/kit/casa.mjs';
const raiz = fs.mkdtempSync(path.join(os.tmpdir(), 'hub-ensaio-23-fielzinho-'));
try {
  fs.writeFileSync(path.join(raiz, 'config.txt'), 'original de ensaio');
  const casa = new Casa(raiz);
  try {
    casa.mudar(casa.caminho('config.txt'), {tipo:'arquivo', hash:'novo'}, 'falha simulada na gravação', () => {
      const e = new Error('ENOSPC de ensaio'); e.code = 'ENOSPC'; throw e;
    });
  } catch(e) { console.log('falha=' + e.code); }
  console.log('original_no_destino=' + fs.existsSync(path.join(raiz, 'config.txt')));
  console.log('registro=' + JSON.stringify(casa.lerRegistro()));
  const arquivos = fs.readdirSync(path.join(raiz,'.hub-kit','copias'), {recursive:true});
  console.log('copia_antes=' + arquivos.some(p => p.endsWith('config.txt')));
  casa.desfazer();
  console.log('original_depois_do_desfazer=' + fs.existsSync(path.join(raiz,'config.txt')));
  console.log('copia_depois=' + fs.existsSync(path.join(raiz,'.hub-kit')));
} finally {
  if (path.dirname(raiz) !== os.tmpdir() || !path.basename(raiz).startsWith('hub-ensaio-23-fielzinho-')) throw new Error('fora do ensaio');
  fs.rmSync(raiz, {recursive:true,force:true});
}
