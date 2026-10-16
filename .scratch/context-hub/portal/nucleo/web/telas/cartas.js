// Tela Cartas: o System design como carta mestra, a grade das outras cartas agrupadas por ticket na ordem do
// plano de voo, o "Arquivo de cartas" (históricas, em sépia) e o leitor de carta em tela cheia (#/cartas/<id>).
import { prenderFoco, trocarPreservando } from '/web/torre.js';

let leitorAberto = null; // { id, soltar }
let focoPendente = null; // chave data-foco a focar depois de a grade ser reconstruída (quem fechou o leitor)

export function renderizar(app, u) {
  const { h, icone } = u;
  const cartas = app.estado.cartas || [];
  const mestra = cartas.find(c => c.mestra) || null;
  const vigentes = cartas.filter(c => c !== mestra && situacaoEfetiva(c) !== 'historica');
  const historicas = cartas.filter(c => c !== mestra && situacaoEfetiva(c) === 'historica');
  const raiz = h('div.cartas',
    mestra ? cartaMestra(app, u, mestra) : h('div.aviso-rodada', icone('alerta'), 'Nenhuma carta mestra no registro de cartas.'),
    grade(app, u, vigentes),
    historicas.length ? arquivo(app, u, historicas) : null,
    !cartas.length ? h('p.vazio', 'Nenhuma carta registrada em cartas.json ainda.') : null);
  sincronizarLeitor(app, u);
  if (focoPendente) { const k = focoPendente; focoPendente = null; requestAnimationFrame(() => { const el = document.querySelector(`[data-foco="${CSS.escape(k)}"]`); el && el.focus(); }); }
  return raiz;
}
const rotaDaCarta = () => { const r = location.hash.replace(/^#\/?/, '').split('?')[0].split('/'); return r[0] === 'cartas' && r[1] ? decodeURIComponent(r[1]) : null; };

// o leitor segue a rota: #/cartas/<id> abre; qualquer outra rota fecha
document.addEventListener('torre:redesenhando', () => { if (!rotaDaCarta()) fecharLeitor(); });

function dataDaCarta(c) {
  if (!c.data || !c.data.valor) return c.data?.tipo === 'feita' ? 'data a confirmar' : 'arquivo não encontrado';
  return `${c.data.tipo === 'feita' ? 'feita em' : 'arquivo mudado em'} ${c.data.valor}`;
}
// a situação do arquivo, ou "historica" quando outra carta a substitui (calculado pelo servidor)
const situacaoEfetiva = c => c.situacao_efetiva || c.situacao;
const hrefCarta = id => `#/cartas/${encodeURIComponent(id)}`;
const tituloDe = (app, id, titulo) => titulo || app.indices.cartas.get(id)?.titulo || id;
/** "substituída por <título da nova>" (link que abre a nova) e/ou "substitui <título da antiga>". */
function ligacoesDeSubstituicao(app, u, c) {
  const { h } = u;
  const partes = [];
  if (c.substituida_por) partes.push(h('p.ligacao-subst.por', 'substituída por ', h('a', { href: hrefCarta(c.substituida_por), dataset: { foco: `carta-${c.id}-substituta` } }, tituloDe(app, c.substituida_por, c.substituida_por_titulo))));
  if (c.substitui && c.substitui_titulo !== null && c.substitui_titulo !== undefined) partes.push(h('p.ligacao-subst.substitui', 'substitui ', h('a', { href: hrefCarta(c.substitui), dataset: { foco: `carta-${c.id}-substituida` } }, c.substitui_titulo)));
  return partes;
}
const seloDaCarta = (u, c) => c.substituida_por ? u.h('span.selo-historica.selo-substituida', 'substituída') : u.h('span.selo-historica', 'histórica');
const aConfirmar = v => v == null || v === '' || v === 'a confirmar';

function miniatura(c, escala = 0.25, largura = 1280, altura = 800, preguicosa = true) {
  const q = document.createElement('iframe');
  q.src = c.url; q.title = `miniatura de ${c.titulo}`; q.setAttribute('sandbox', 'allow-scripts'); q.loading = preguicosa ? 'lazy' : 'eager'; q.tabIndex = -1; q.setAttribute('aria-hidden', 'true');
  q.style.cssText = `width:${largura}px;height:${altura}px;transform:scale(${escala});transform-origin:0 0;border:0;pointer-events:none;background:#fff`;
  const caixa = document.createElement('div'); caixa.className = 'quadro'; caixa.style.cssText = `width:${largura * escala}px;height:${altura * escala}px`; caixa.append(q);
  return caixa;
}

function cartaMestra(app, u, c) {
  const { h, icone } = u;
  return h('section.carta-mestra',
    h('a.quadro-link', { href: `#/cartas/${encodeURIComponent(c.id)}`, 'aria-label': `abrir ${c.titulo}`, dataset: { foco: `carta-${c.id}` } }, miniatura(c, 0.5, 1280, 720, false)),
    h('div.mestra-texto',
      h('div.secao-titulo', icone('carta'), 'Carta mestra'),
      h('h1', c.titulo),
      h('p.proposito', c.proposito),
      h('div.meta-carta', h('span', icone('relogio'), dataDaCarta(c)), ticketOuNota(app, u, c),
        aConfirmar(c.decisao) ? h('span.a-confirmar', 'decisão a confirmar') : h('button.com-dica', { type: 'button', dataset: { dica: c.decisao, dicaTitulo: 'decisão a que serviu', foco: `carta-${c.id}-decisao` } }, 'decisão: ', recorte(c.decisao, 60))),
      h('p.nota-mestra', 'O desenho só muda quando um ticket que mexe nele é resolvido, com a data; quem muda é o Designer a pedido do maestro.'),
      h('a.botao.primario', { href: `#/cartas/${encodeURIComponent(c.id)}` }, icone('carta'), 'Abrir ', c.titulo)));
}

/** Chip do ticket dono; `null` = carta sem ticket (serve ao mapa inteiro); "a confirmar" = pergunta feita ao maestro. */
function ticketOuNota(app, u, c) {
  const { h } = u;
  if (c.ticket === null || c.ticket === undefined || c.ticket === '') return h('span.sem-ticket', 'serve ao mapa inteiro');
  if (aConfirmar(c.ticket)) return h('span.a-confirmar', 'ticket a confirmar');
  return chipTicket(app, u, c);
}
function chipTicket(app, u, c) {
  const { h, icone, abrirGaveta } = u;
  return h('button.chip.e-open', { type: 'button', onclick: () => abrirGaveta(c.ticket), dataset: { foco: `carta-${c.id}-ticket` } }, icone('aviao'), h('span.n-ticket', c.ticket), h('span.chip-titulo', { title: c.ticket_titulo || '' }, c.ticket_titulo || 'ticket não encontrado'));
}
const recorte = (s, n) => (s || '').length > n ? s.slice(0, n - 1).trimEnd() + '…' : (s || '');

function cartao(app, u, c, sepia = false) {
  const { h, icone } = u;
  return h('article.cartao-carta', { class: `cartao-carta${sepia ? ' sepia' : ''}` },
    h('a.quadro-link', { href: `#/cartas/${encodeURIComponent(c.id)}`, 'aria-label': `abrir ${c.titulo}`, dataset: { foco: `carta-${c.id}` } }, miniatura(c, 0.25), sepia ? seloDaCarta(u, c) : null),
    h('div.cartao-texto',
      h('h3', h('a', { href: `#/cartas/${encodeURIComponent(c.id)}` }, c.titulo)),
      h('p.proposito', aConfirmar(c.proposito) ? h('span.a-confirmar', 'propósito a confirmar') : c.proposito),
      h('div.meta-carta',
        app.cartasAguardando().some(x => x.id === c.id) ? h('span.chip.e-espera', icone('carimbo'), 'espera Aprovar ou Recusar') : null,
        ticketOuNota(app, u, c),
        h('span', icone('relogio'), dataDaCarta(c))),
      h('p.decisao', aConfirmar(c.decisao) ? h('span.a-confirmar', 'decisão a confirmar') : h('button.com-dica', { type: 'button', dataset: { dica: c.decisao, dicaTitulo: 'decisão a que serviu' } }, 'decisão: ', recorte(c.decisao, 90))),
      ligacoesDeSubstituicao(app, u, c)));
}

/** Agrupa por ticket na ordem do plano de voo (depois os demais por número; sem ticket por último). */
function grade(app, u, cartas) {
  const { h, icone } = u;
  const ordemPlano = (app.estado.plano_de_voo?.camadas || []).flat();
  const grupos = new Map();
  for (const c of cartas) { const k = c.ticket || ''; if (!grupos.has(k)) grupos.set(k, []); grupos.get(k).push(c); }
  const chaves = [...grupos.keys()].sort((a, b) => {
    if (!a) return 1; if (!b) return -1;
    const ia = ordemPlano.indexOf(a), ib = ordemPlano.indexOf(b);
    if (ia !== -1 && ib !== -1) return ia - ib; if (ia !== -1) return -1; if (ib !== -1) return 1; return a < b ? -1 : 1;
  });
  return h('section.grade-cartas', h('h2.secao-titulo', icone('carta'), 'Cartas de navegação', h('span.n', String(cartas.length))),
    cartas.length ? h('div.grupos-cartas', chaves.map(k => {
      const t = k ? app.ticket(k) : null;
      return h('div.grupo-cartas',
        h('h3.grupo-titulo', k ? [h('span.n-ticket', k), t ? t.titulo : 'ticket não encontrado', t ? h('span.chip', { class: `chip ${u.estadoTicket(t).classe}` }, u.estadoTicket(t).palavra) : null] : 'servem ao mapa inteiro (sem ticket dono)'),
        h('div.cartoes-cartas', grupos.get(k).map(c => cartao(app, u, c))));
    })) : h('p.vazio', 'Nenhuma carta vigente além da mestra.'));
}

function arquivo(app, u, historicas) {
  const { h, icone } = u;
  return h('section.arquivo-cartas',
    h('h2.secao-titulo', icone('carta'), 'Arquivo de cartas', h('span.n', String(historicas.length)), h('span.sub', 'serviram a rodadas que o desenho já superou, ou foram substituídas por uma carta nova')),
    h('div.cartoes-cartas', historicas.map(c => cartao(app, u, c, true))));
}

// ------------------------------------------------------------------ leitor de carta (tela cheia)
function sincronizarLeitor(app, u) {
  const id = app.rota.sub;
  if (!id) { fecharLeitor(); return; }
  const c = app.indices.cartas.get(id);
  if (!c) { fecharLeitor(); u.brisa(`Carta "${id}" não está no registro.`, 'coral'); return; }
  if (leitorAberto && leitorAberto.id === id) { atualizarTira(app, u, c); return; }
  fecharLeitor();
  abrirLeitor(app, u, c);
}
/** Fechamento único do leitor (Esc, X ou navegação): solta o foco preso, esvazia, concilia a rota e devolve o foco
 *  à carta na grade depois de ela ser reconstruída. */
function fecharLeitor() {
  if (!leitorAberto) return;
  const { id, soltar } = leitorAberto; leitorAberto = null;
  soltar();
  const el = document.getElementById('leitor'); el.hidden = true; el.replaceChildren();
  focoPendente = `carta-${id}`;
  if (rotaDaCarta() === id) location.hash = '#/cartas'; // hashchange → rota relida → grade redesenhada
}

function abrirLeitor(app, u, c) {
  const { h, icone } = u;
  const el = document.getElementById('leitor');
  const quadro = h('iframe.carta-cheia', { src: c.url, title: c.titulo, sandbox: 'allow-scripts' });
  el.replaceChildren(h('div.tira', { 'data-tira': '1' }), quadro);
  atualizarTira(app, u, c);
  el.hidden = false;
  const fechar = prenderFoco(el, fecharLeitor, 'carta-' + c.id); // Esc → fecharLeitor → foco de volta à carta
  leitorAberto = { id: c.id, soltar: fechar.soltar };
  // o redesenho que abriu o leitor devolve o foco pela chave a quem estava focado antes (a carta na grade); o leitor
  // é um diálogo e precisa ficar com o foco, então o prende de novo depois desse ciclo
  setTimeout(() => { if (leitorAberto && leitorAberto.id === c.id && !el.contains(document.activeElement)) { const f = el.querySelector('a, button, [tabindex]:not([tabindex="-1"])'); (f || el).focus(); } }, 0);
}
function atualizarTira(app, u, c) {
  const { h, icone, acoes } = u;
  const el = document.getElementById('leitor'); const tira = el.querySelector('.tira'); if (!tira) return;
  const focoAntes = tira.contains(document.activeElement) ? document.activeElement.dataset.foco : null;
  // troca preservando: com o comentário da carta aberto, o rodapé dele fica (texto, foco, cursor) nas atualizações ao vivo
  trocarPreservando(tira, [
    h('a.fechar-leitor', { href: '#/cartas', 'aria-label': 'Fechar a carta e voltar à grade', dataset: { foco: 'leitor-fechar' } }, icone('fechar')),
    h('div.tira-texto',
      h('strong', c.titulo), h('span.sep', '·'), aConfirmar(c.proposito) ? h('span.a-confirmar', 'propósito a confirmar') : (c.proposito.length > 72 ? h('button.com-dica.proposito-tira', { type: 'button', dataset: { dica: c.proposito, dicaTitulo: 'propósito' } }, recorte(c.proposito, 72)) : h('span', c.proposito)), h('span.sep', '·'),
      ticketOuNota(app, u, c), h('span.sep', '·'),
      h('span', dataDaCarta(c)),
      app.cartasAguardando().some(x => x.id === c.id) ? h('span.chip.e-espera', icone('carimbo'), 'espera Aprovar ou Recusar') : null,
      !c.mestra && situacaoEfetiva(c) === 'historica' ? seloDaCarta(u, c) : null,
      c.substituida_por ? h('a.ligacao-subst', { href: hrefCarta(c.substituida_por), dataset: { foco: 'leitor-substituta' } }, 'substituída por ', tituloDe(app, c.substituida_por, c.substituida_por_titulo)) : null,
      aConfirmar(c.decisao) ? h('span.a-confirmar', 'decisão a confirmar') : h('button.com-dica', { type: 'button', dataset: { dica: c.decisao, dicaTitulo: 'decisão a que serviu' } }, 'decisão')),
    h('div.tira-acoes', acoes({ tipo: 'carta', id: c.id, titulo: c.titulo }, { rotuloComentar: 'Comentar esta carta', compacto: true }))]);
  if (focoAntes && !tira.contains(document.activeElement)) { const el2 = tira.querySelector(`[data-foco="${CSS.escape(focoAntes)}"]`); el2 && el2.focus({ preventScroll: true }); }
}
