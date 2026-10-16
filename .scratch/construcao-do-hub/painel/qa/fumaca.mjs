import fs from 'node:fs';
import path from 'node:path';
import { QA, gerar, servidor, pronto, navegador, LER_TELA, esp } from './comum.mjs';
const [momento = '0', ...extra] = process.argv.slice(2);
const pasta = path.join(QA, 'exec-' + momento);
gerar(pasta, ['--so-historia', '--ate', momento, ...extra]);
const s = servidor(pasta, 8772); await pronto('http://127.0.0.1:8772/api/execucao');
const n = await navegador();
const R = {};
try {
  for (const [w, h] of [[1280, 800], [320, 640]]) {
    await n.abrir('http://127.0.0.1:8772/', w, h); await esp(3500);
    R[`${w}x${h}`] = await n.ev(LER_TELA);
    await n.foto(`fumaca-${momento}-${w}x${h}.png`);
  }
  R.erros = n.erros;
} finally { n.fechar(); s.kill(); }
fs.writeFileSync(path.join(QA, `fumaca-${momento}.json`), JSON.stringify(R, null, 1));
const t = R['1280x800'];
console.log(JSON.stringify({ trab: t.trab, de: t.trabDe, feitos: t.feitos, total: t.total, leitura: t.leitura, problemas: t.problemas, alertas: t.alertas.map(a => a.txt), estacoes: t.estacoes.map(e => e.col + ':' + e.n), erros: R.erros }, null, 1));
console.log(t.cartoes.map(c => `${c.nome} | ${c.sit} | subs ${c.abertos}/${c.pips} | ${c.sinal} | ${c.oque.slice(0, 40)}`).join('\n'));
process.exit(0);
