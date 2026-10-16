// Momentos fixos da fixture (começo, meio, pico de 10 subagentes, excesso, fim, defeitos) em 1280x720 e 320x640:
// layout, cortes, alvos, teclado e gaveta. Porta 8773 para não brigar com o teste ao vivo.
import fs from 'node:fs';
import path from 'node:path';
import { QA, gerar, servidor, pronto, navegador, LER_TELA, esp } from './comum.mjs';

const CENAS = [
  ['comeco', ['--ate', '-40']], ['meio', ['--ate', '0']], ['pico', ['--ate', '6']],
  ['excesso', ['--ate', '6', '--excesso']], ['fim', ['--ate', '30']], ['defeitos', ['--ate', '0', '--defeitos']],
];
const TAM = [[1280, 720], [320, 640]];
const MEDIR = `(function(){
  var out={sobrepostos:[],fonteMin:99,pequenos:[],semNome:[],cortados:[]};
  var cs=[].slice.call(document.querySelectorAll('.agente'));
  for(var i=0;i<cs.length;i++)for(var j=i+1;j<cs.length;j++){var a=cs[i].getBoundingClientRect(),b=cs[j].getBoundingClientRect();
    if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)out.sobrepostos.push(cs[i].textContent.slice(0,14)+'|'+cs[j].textContent.slice(0,14))}
  var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);var nd;
  while(nd=w.nextNode()){if(!nd.textContent.trim())continue;var e=nd.parentElement;var r=e.getBoundingClientRect();if(!r.width||!r.height)continue;
    var f=parseFloat(getComputedStyle(e).fontSize);if(f<out.fonteMin)out.fonteMin=f;if(f<11&&out.pequenos.length<8)out.pequenos.push(f+'px:'+nd.textContent.trim().slice(0,24))}
  [].forEach.call(document.querySelectorAll('button'),function(b){var r=b.getBoundingClientRect();if(!r.width)return;
    if(r.height<24||r.width<24)out.semNome.push((b.className||'')+' '+Math.round(r.width)+'x'+Math.round(r.height));
    if(!(b.getAttribute('aria-label')||b.textContent.trim()))out.semNome.push('sem nome:'+b.className)});
  [].forEach.call(document.querySelectorAll('.alerta,.agente,.tk'),function(b){if(b.scrollWidth>b.clientWidth+1&&getComputedStyle(b).textOverflow!=='ellipsis'&&!b.querySelector('[class]'))out.cortados.push(b.className+':'+b.textContent.slice(0,20))});
  var al=document.getElementById('alertas').getBoundingClientRect();out.alertasAbaixoDaDobra=al.bottom>innerHeight;out.alertasFundo=Math.round(al.bottom);
  out.faixaSobreposta=(function(){var f=document.getElementById('faixa').getBoundingClientRect();return f.top<innerHeight-1&&false})();
  return out})()`;

const R = {};
for (const [cena, args] of CENAS) {
  const pasta = path.join(QA, 'exec-' + cena);
  gerar(pasta, ['--so-historia', ...args]);
  const s = servidor(pasta, 8773); await pronto('http://127.0.0.1:8773/api/execucao');
  const n = await navegador();
  try {
    for (const [w, h] of TAM) {
      await n.abrir('http://127.0.0.1:8773/', w, h); await esp(3500);
      const t = await n.ev(LER_TELA), m = await n.ev(MEDIR);
      await n.foto(`${cena}-${w}x${h}.png`);
      R[`${cena}@${w}x${h}`] = { trab: `${t.trab}/${t.trabDe}`, feitos: `${t.feitos}/${t.total}`, leitura: t.leitura, problemas: t.problemas,
        cartoes: t.cartoes.length, maxSubs: Math.max(...t.cartoes.map(c => c.abertos)), pips: [...new Set(t.cartoes.map(c => c.pips))],
        alertas: t.alertas.map(a => a.txt), estacoes: Object.fromEntries(t.estacoes.map(e => [e.col, e.n])), largura: t.largura, medidas: m,
        sits: t.cartoes.reduce((o, c) => (o[c.sit] = (o[c.sit] || 0) + 1, o), {}), selos: t.cartoes.filter(c => c.selo).map(c => c.nome), erros: [...n.erros] };
    }
  } finally { n.fechar(); s.kill(); }
}
fs.writeFileSync(path.join(QA, 'estatico.json'), JSON.stringify(R, null, 1));
for (const [k, v] of Object.entries(R)) {
  console.log(k, '| trab', v.trab, '| feitos', v.feitos, '| cart', v.cartoes, '| maxSubs', v.maxSubs, 'pips', v.pips, '| scrollW', v.largura.scrollW, '/', v.largura.innerW,
    '| sobrepostos', v.medidas.sobrepostos.length, '| fonteMin', v.medidas.fonteMin, '| alvos<24', v.medidas.semNome.length, '| alertasFundo', v.medidas.alertasFundo, '| prob', v.problemas, '| erros', v.erros.length);
}
process.exit(0);
