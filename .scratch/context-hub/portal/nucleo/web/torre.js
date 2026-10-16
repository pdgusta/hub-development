// Torre: casca da página. Rotas no #hash, estado vindo de /api/estado, atualização ao vivo por /api/versao,
// contador "aguardando você", selo de problemas, dicas (hover = foco = clique), glossário, gaveta do ticket.
import { icone, tipoTicket, estadoTicket } from '/web/icones.js';
import * as telaTorre from '/web/telas/torre.js';
import * as telaPartidas from '/web/telas/partidas.js';
import * as telaAutorizacoes from '/web/telas/autorizacoes.js';
import * as telaCartas from '/web/telas/cartas.js';
import * as telaRumo from '/web/telas/rumo.js';
import * as telaLacos from '/web/telas/lacos.js';

// Ligado no marco 7 (2026-10-14): canal A passou nos testes reais da §4.3. Fora do canvas a faixa continua.
const CANAL_DE_AVISO_VERIFICADO = true;
const INTERVALO_VERSAO_MS = 3000;

// ------------------------------------------------------------------ utilidades de DOM
/** Cria um elemento: h('div.classe#id', {atributos}, ...filhos). Texto vira nó de texto (nunca HTML). */
export function h(spec, attrs, ...filhos) {
  const [tag, ...resto] = spec.split(/(?=[.#])/);
  const el = document.createElement(tag || 'div');
  for (const r of resto) { if (r[0] === '.') el.classList.add(r.slice(1)); else if (r[0] === '#') el.id = r.slice(1); }
  if (attrs && typeof attrs === 'object' && !(attrs instanceof Node) && !Array.isArray(attrs)) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === 'class') el.className = v;
      else if (k === 'dataset') Object.assign(el.dataset, v);
      else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else if (k === 'html') el.innerHTML = v; // só com HTML já sanitizado (DOMPurify)
      else if (k === 'value') el.value = v;     // propriedade, para textarea e input restaurados de rascunho
      else if (v === true) el.setAttribute(k, '');
      else el.setAttribute(k, v);
    }
  } else if (attrs != null) filhos.unshift(attrs);
  for (const f of filhos.flat(Infinity)) {
    if (f == null || f === false) continue;
    el.append(f instanceof Node ? f : document.createTextNode(String(f)));
  }
  return el;
}

export function svg(tag, attrs = {}, ...filhos) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null && v !== false) el.setAttribute(k, v);
  for (const f of filhos.flat(Infinity)) if (f != null && f !== false) el.append(f instanceof Node ? f : document.createTextNode(String(f)));
  return el;
}

/** Markdown → HTML seguro (marked + DOMPurify); links externos com rel seguro. */
export function markdown(texto) {
  const bruto = window.marked ? window.marked.parse(texto || '', { gfm: true, breaks: false }) : escapar(texto || '');
  const limpo = window.DOMPurify ? window.DOMPurify.sanitize(bruto, { USE_PROFILES: { html: true } }) : escapar(texto || '');
  const caixa = h('div.markdown', { html: limpo });
  for (const a of caixa.querySelectorAll('a[href]')) {
    const href = a.getAttribute('href') || '';
    if (/^https?:/i.test(href)) { a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener noreferrer'); }
  }
  return caixa;
}
function escapar(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

export const reduzMovimento = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ------------------------------------------------------------------ foco estável entre renderizações
/** Chave estável do elemento focado (`data-foco`), para devolver o foco depois de redesenhar. */
function chaveDoFoco(el) { const c = el && el.closest ? el.closest('[data-foco]') : null; return c ? c.dataset.foco : null; }
/** Um campo onde o Gustavo escreve (textarea, input de texto, contenteditable). */
export function emEdicao(el) {
  if (!el || el === document.body) return false;
  if (el.isContentEditable || el.tagName === 'TEXTAREA') return true;
  return el.tagName === 'INPUT' && !['checkbox', 'radio', 'button', 'submit', 'reset', 'file', 'range', 'color'].includes(el.type);
}
function focarPorChave(chave, raiz = document) {
  if (!chave) return false;
  const el = raiz.querySelector(`[data-foco="${CSS.escape(chave)}"]`);
  if (!el) return false;
  el.focus({ preventScroll: true });
  return document.activeElement === el;
}

// ------------------------------------------------------------------ troca preservando o que está em edição
// A atualização ao vivo (a cada 3 s, quando qualquer arquivo muda) redesenha a tela inteira. Um elemento marcado com
// `data-preservar="<chave>"` (formulário em edição, iframe de carta) que já está na página com a mesma chave NÃO é
// trocado: o nó antigo fica no lugar, sem sair do documento, e por isso não perde foco, cursor, seleção, rolagem
// interna, texto, `<details>` aberto nem recarrega. Os ancestrais dele também ficam (com os atributos novos); tudo o
// mais vem da renderização nova. Quem decide a chave é a tela: chave igual = o conteúdo do nó continua válido.
// Limite: um ancestral mantido conserva os ouvintes de evento antigos (as telas não põem ouvintes nesses invólucros).
export function trocarPreservando(pai, novos) {
  novos = (Array.isArray(novos) ? novos : [novos]).filter(n => n != null && n !== false).map(n => n instanceof Node ? n : document.createTextNode(String(n)));
  const velhos = new Map();
  for (const el of pai.querySelectorAll('[data-preservar]')) if (!velhos.has(el.dataset.preservar)) velhos.set(el.dataset.preservar, el);
  const porNovo = new Map();
  for (const raiz of novos) {
    if (raiz.nodeType !== 1) continue;
    const cands = raiz.matches('[data-preservar]') ? [raiz, ...raiz.querySelectorAll('[data-preservar]')] : [...raiz.querySelectorAll('[data-preservar]')];
    for (const el of cands) { const v = velhos.get(el.dataset.preservar); if (v && ![...porNovo.values()].includes(v)) porNovo.set(el, v); }
  }
  if (!porNovo.size) { pai.replaceChildren(...novos); return; }
  mesclarFilhos(pai, novos, porNovo);
  // estrutura que não casou (ancestral de outro tipo): o nó antigo entra no lugar do novo mesmo assim; o conteúdo
  // fica, mas aí o foco se perde (o nó sai e volta ao documento)
  for (const [novoEl, velhoEl] of porNovo) if (novoEl.isConnected) novoEl.replaceWith(velhoEl);
}
function mesclarFilhos(pai, novos, porNovo) {
  const usados = new Set();
  const alvo = novos.map(n => {
    if (porNovo.has(n)) { const v = porNovo.get(n); usados.add(v); return v; }
    if (n.nodeType !== 1) return n;
    // um descendente preservado dentro de `n`: o filho antigo de `pai` que contém o par dele é mantido e mesclado
    for (const [novoEl, velhoEl] of porNovo) {
      if (!n.contains(novoEl)) continue;
      let c = velhoEl; while (c && c.parentNode !== pai) c = c.parentNode;
      if (!c || usados.has(c) || c.nodeType !== 1 || c.tagName !== n.tagName) continue;
      usados.add(c);
      for (const a of [...c.attributes]) if (!n.hasAttribute(a.name)) c.removeAttribute(a.name);
      for (const a of [...n.attributes]) if (c.getAttribute(a.name) !== a.value) c.setAttribute(a.name, a.value);
      mesclarFilhos(c, [...n.childNodes], porNovo);
      return c;
    }
    return n;
  });
  const manter = new Set(alvo);
  for (const c of [...pai.childNodes]) if (!manter.has(c)) c.remove();
  let ref = pai.firstChild;
  for (const n of alvo) { if (n === ref) { ref = ref.nextSibling; continue; } pai.insertBefore(n, ref); }
}

// ------------------------------------------------------------------ letreiro de palhetas
/** Mostra `texto` em palhetas; ao mudar, só as letras diferentes viram. */
export function palhetas(el, texto) {
  texto = String(texto);
  el.classList.add('palhetas');
  const atuais = [...el.children];
  const n = Math.max(atuais.length, texto.length);
  for (let i = 0; i < n; i++) {
    const ch = texto[i];
    let p = atuais[i];
    if (ch === undefined) { p && p.remove(); continue; }
    if (!p) { p = h('span.palheta', h('span', ch)); el.append(p); if (atuais.length) virar(p); continue; }
    if (p.firstChild.textContent !== ch) { p.firstChild.textContent = ch; virar(p); }
  }
  function virar(p) {
    if (reduzMovimento()) return;
    p.classList.remove('vira'); void p.offsetWidth; p.classList.add('vira');
  }
  return el;
}

// ------------------------------------------------------------------ dica (tooltip acessível)
// Aparece com hover, foco e clique; dá para levar o ponteiro até ela; Esc a dispensa sem mexer no foco, e ela não
// reabre no mesmo alvo até ele perder o hover e o foco. A leitura vai sempre para a faixa reservada #leitura, uma linha
// própria da casca fora da área que rola: sempre visível, em todas as telas, nunca cobre nada.
const dicaEl = document.getElementById('dica');
const faixaEl = document.getElementById('leitura');
const REPOUSO_FAIXA = 'Passe o mouse ou foque um item com explicação: a leitura dele aparece aqui.';
let dicaFixa = null, dicaAlvo = null, dicaDispensada = null, dicaTimer = null, dicaNaFaixa = false;
function naFaixa(alvo, titulo, texto) {
  dicaEl.hidden = true; dicaNaFaixa = true;
  dicaAlvo = alvo; alvo.setAttribute('aria-describedby', 'leitura');
  faixaEl.hidden = false; faixaEl.classList.add('lendo');
  faixaEl.replaceChildren(titulo ? h('div.dica-titulo', titulo) : null, h('div', (texto || '').split('\n').join(' · ')));
}
function limparFaixa() {
  dicaNaFaixa = false;
  faixaEl.classList.remove('lendo');
  faixaEl.replaceChildren(h('div', faixaEl.dataset.repouso || REPOUSO_FAIXA));
}
/** Volta a faixa ao texto de repouso; uma tela pode trocar o texto (o Início fala do mapa). */
export function repousoDaFaixa(texto = REPOUSO_FAIXA) { faixaEl.dataset.repouso = texto; if (!dicaNaFaixa) limparFaixa(); }
function mostrarDica(alvo, fixa = false) {
  const titulo = alvo.dataset.dicaTitulo;
  const texto = alvo.dataset.dica;
  if (!texto && !titulo) return;
  if (alvo === dicaDispensada && !fixa) return;
  clearTimeout(dicaTimer);
  if (dicaAlvo && dicaAlvo !== alvo) { dicaAlvo.removeAttribute('aria-describedby'); if (dicaNaFaixa) limparFaixa(); }
  if (fixa) { dicaFixa = alvo; dicaDispensada = null; }
  naFaixa(alvo, titulo, texto);
}
function esconderDica(forcar = false) {
  clearTimeout(dicaTimer);
  if (dicaFixa && !forcar) return;
  if (dicaAlvo) dicaAlvo.removeAttribute('aria-describedby');
  if (dicaNaFaixa) limparFaixa();
  dicaFixa = null; dicaAlvo = null; dicaEl.hidden = true;
}
function esconderDepois() { clearTimeout(dicaTimer); if (!dicaFixa) dicaTimer = setTimeout(() => esconderDica(), 250); }
function dispensarDica(alvo = dicaAlvo) { esconderDica(true); dicaDispensada = alvo; }
const alvoDica = e => (e.target && e.target.closest) ? e.target.closest('[data-dica]') : null;
document.addEventListener('mouseover', e => { if (dicaEl.contains(e.target)) { clearTimeout(dicaTimer); return; } const a = alvoDica(e); if (a && !dicaFixa) mostrarDica(a); });
document.addEventListener('mouseout', e => {
  const a = alvoDica(e), para = e.relatedTarget;
  if (a && a === dicaDispensada && !(para && a.contains(para)) && document.activeElement !== a) dicaDispensada = null;
  if (para && dicaEl.contains(para)) return;          // o ponteiro está entrando na dica
  if ((a || dicaEl.contains(e.target)) && !(para && dicaAlvo && dicaAlvo.contains(para)) && document.activeElement !== dicaAlvo) esconderDepois();
});
document.addEventListener('focusin', e => { const a = alvoDica(e); if (a) mostrarDica(a); });
document.addEventListener('focusout', e => { const a = alvoDica(e); if (a) { if (a === dicaDispensada) dicaDispensada = null; esconderDica(); } });
document.addEventListener('click', e => {
  if (dicaEl.contains(e.target)) return;
  const a = alvoDica(e);
  if (a && !a.dataset.dicaSemClique) { if (dicaFixa === a) esconderDica(true); else mostrarDica(a, true); }
  else if (dicaFixa) esconderDica(true);
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && (!dicaEl.hidden || dicaNaFaixa)) dispensarDica();
  // Enter/espaço num elemento com dica que não é botão (ex.: aresta do SVG) fixa a dica, como o clique faria
  const a = (e.key === 'Enter' || e.key === ' ') ? alvoDica(e) : null;
  if (a && !a.dataset.dicaSemClique && !a.closest('button, a, [role="button"]')) { e.preventDefault(); if (dicaFixa === a) esconderDica(true); else mostrarDica(a, true); }
});
// uma tela pode pedir que a dica de um alvo não reabra quando ele recebe o foco de volta (ex.: depois do Esc)
window.addEventListener('torre:dispensar-dica', e => dispensarDica(e.detail));
// ------------------------------------------------------------------ glossário
/** Sublinha termos do glossário nos nós de texto dentro de `raiz` (fora de botões, links, títulos grandes e números). */
export function marcarGlossario(raiz, glossario) {
  if (!glossario || !glossario.length) return;
  const termos = glossario.filter(g => g.termo && g.termo.length > 2);
  if (!termos.length) return;
  const padrao = `(^|[^\\p{L}\\p{N}])(${termos.map(t => t.termo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})(?![\\p{L}\\p{N}])`;
  const reTeste = new RegExp(padrao, 'iu');   // sem flag global: `test` não mexe em lastIndex
  const reVarre = new RegExp(padrao, 'giu');
  const porNome = new Map(termos.map(t => [t.termo.toLowerCase(), t]));
  const andarilho = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      const p = n.parentElement;
      if (!p || p.closest('button, a, .termo, .palhetas, .n-ticket, .mono, code, pre, svg, .pista-destino, h1, h2, .cartao-rodada .titulo')) return NodeFilter.FILTER_REJECT;
      return reTeste.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
    },
  });
  const nos = []; let n; while ((n = andarilho.nextNode())) nos.push(n);
  for (const no of nos) {
    const frag = document.createDocumentFragment();
    let ultimo = 0; const s = no.nodeValue; reVarre.lastIndex = 0; let m;
    while ((m = reVarre.exec(s))) {
      const ini = m.index + m[1].length;
      frag.append(s.slice(ultimo, ini));
      const g = porNome.get(m[2].toLowerCase());
      frag.append(h('button.termo', { type: 'button', dataset: { dicaTitulo: g.termo, dica: g.definicao + (g.evite ? ` (evite: ${g.evite})` : '') } }, m[2]));
      ultimo = ini + m[2].length;
    }
    frag.append(s.slice(ultimo));
    no.replaceWith(frag);
  }
}

/** Códigos internos do projeto (uma a três letras e um número) ganham a explicação em palavras que o `projeto.json`
 *  dá em `codigos` ({ "Q": "pergunta numerada das rodadas de mapeamento" }); sem o mapa, nada é marcado. */
export function marcarCodigos(raiz, codigos) {
  const prefixos = Object.keys(codigos || {}).filter(p => /^[A-Za-z]{1,3}$/.test(p));
  if (!prefixos.length) return;
  const padrao = `(^|[^\\p{L}\\p{N}])(${prefixos.join('|')})(\\d{1,4})(?![\\p{L}\\p{N}])`;
  const reTeste = new RegExp(padrao, 'u'), reVarre = new RegExp(padrao, 'gu');
  const andarilho = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      const p = n.parentElement;
      if (!p || p.closest('button, a, .termo, .codigo, .palhetas, .n-ticket, code, pre, svg, h1, h2')) return NodeFilter.FILTER_REJECT;
      return reTeste.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
    },
  });
  const nos = []; let n; while ((n = andarilho.nextNode())) nos.push(n);
  for (const no of nos) {
    const frag = document.createDocumentFragment();
    let ultimo = 0; const s = no.nodeValue; reVarre.lastIndex = 0; let m;
    while ((m = reVarre.exec(s))) {
      const ini = m.index + m[1].length, cod = m[2] + m[3];
      frag.append(s.slice(ultimo, ini));
      frag.append(h('button.codigo', { type: 'button', 'aria-label': `${cod}: ${codigos[m[2]]}, número ${m[3]}`, dataset: { dicaTitulo: cod, dica: `${codigos[m[2]]}, número ${m[3]}` } }, cod));
      ultimo = ini + cod.length;
    }
    frag.append(s.slice(ultimo));
    no.replaceWith(frag);
  }
}

// ------------------------------------------------------------------ brisa (aviso passageiro)
export function brisa(texto, cor = '') {
  const s = h('div.sopro', { class: `sopro ${cor}`.trim() }, texto);
  document.getElementById('brisa').append(s);
  setTimeout(() => s.remove(), 5000);
}

// ------------------------------------------------------------------ foco preso (gaveta, leitor, diálogos)
const FOCAVEIS = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
/** Prende o foco em `el`; Esc fecha. Devolve a função de fechar, que leva o foco de volta a quem abriu
 *  (pela chave `data-foco`, que sobrevive a uma redesenhada da tela). */
export function prenderFoco(el, aoFechar, chaveOrigem = null) {
  const antes = chaveOrigem ? null : document.activeElement;
  const chaveAntes = chaveOrigem || chaveDoFoco(antes);
  const trata = e => {
    if (e.key === 'Escape') { e.stopPropagation(); fechar(); return; }
    if (e.key !== 'Tab') return;
    const f = [...el.querySelectorAll(FOCAVEIS)].filter(x => x.offsetParent !== null || x.getClientRects().length);
    if (!f.length) { e.preventDefault(); return; }
    const i = f.indexOf(document.activeElement);
    if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && (i === f.length - 1 || i === -1)) { e.preventDefault(); f[0].focus(); }
  };
  el.addEventListener('keydown', trata);
  const primeiro = el.querySelector(FOCAVEIS); (primeiro || el).focus();
  function soltar() { el.removeEventListener('keydown', trata); }
  function fechar() {
    soltar();
    aoFechar && aoFechar();
    if (antes && antes !== document.body && antes.isConnected && antes.focus) antes.focus();
    else if (!focarPorChave(chaveAntes)) document.getElementById('tela').focus();
  }
  fechar.soltar = soltar;
  return fechar;
}

// ------------------------------------------------------------------ estado e API
export const app = {
  estado: null,
  versaoDoEstado: null,   // a versão que o estado em memória representa; só muda com uma leitura bem-sucedida
  ligado: true,
  erroEstado: null,
  rota: { tela: 'torre', sub: null, params: new URLSearchParams() },
  indices: { tickets: new Map(), cartas: new Map(), rodadas: new Map() },
  /** Rodadas que esperam o Gustavo: abertas, não respondidas, não malformadas. */
  aguardando() { return (this.estado?.rodadas || []).filter(r => r.estado === 'aberta' && !r.respondida && !r.malformada); },
  /** Cartas que esperam Aprovar ou Recusar: `pede_veredito` no cartas.json, vigentes, sem aprovação na caixa. */
  cartasAguardando() {
    const caixa = this.estado?.caixa || [];
    return (this.estado?.cartas || []).filter(c => c.pede_veredito === true && !c.mestra
      && (c.situacao_efetiva || c.situacao) === 'vigente'
      && !caixa.some(m => m.tipo === 'aprovacao' && m.alvo?.tipo === 'carta' && m.alvo.id === c.id && !m.substituida));
  },
  ticket(n) { return this.indices.tickets.get(String(n)); },
  escutas: new Set(),
  aoMudar(fn) { this.escutas.add(fn); return () => this.escutas.delete(fn); },
};

async function pedir(url, opcoes = {}) {
  const { headers, ...resto } = opcoes;
  const r = await fetch(url, { ...resto, headers: { 'X-Torre': '1', ...(headers || {}) } });
  if (!r.ok) { let corpo = null; try { corpo = await r.json(); } catch {} const e = new Error(corpo?.mensagem || `${r.status} em ${url}`); e.status = r.status; e.corpo = corpo; throw e; }
  return r.json();
}
export const api = {
  estado: () => pedir('/api/estado'),
  versao: () => pedir('/api/versao'),
  ticket: n => pedir(`/api/ticket/${encodeURIComponent(n)}`),
  caixa: corpo => pedir('/api/caixa', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corpo) }),
  caixaItem: envio => pedir(`/api/caixa/${encodeURIComponent(envio)}`),
  // laços (§3.4): lidos só pela tela Laços, a cada 10 s enquanto ela está aberta
  lacos: () => pedir('/api/lacos'),
  laco: id => pedir(`/api/laco/${encodeURIComponent(id)}`),
};

function indexar(estado) {
  app.indices.tickets = new Map((estado.tickets || []).map(t => [t.numero, t]));
  app.indices.cartas = new Map((estado.cartas || []).map(c => [c.id, c]));
  app.indices.rodadas = new Map((estado.rodadas || []).map(r => [r.id, r]));
}

/** Lê /api/estado e redesenha. Devolve true se leu. `versao` é a versão que esse estado passa a representar. */
async function carregarEstado(versao) {
  let estado;
  try {
    estado = await api.estado();
  } catch (e) {
    app.erroEstado = e;
    renderizarFaixa();
    if (!app.estado) document.getElementById('tela').replaceChildren(h('div.em-construcao', icone('alerta'), h('h2', 'Sem ligação com a torre'), h('p', `Não deu para ler o estado do servidor: ${e.message}. Tentando de novo a cada 3 segundos.`)));
    return false;
  }
  app.estado = estado; app.erroEstado = null; indexar(estado);
  if (versao !== undefined) app.versaoDoEstado = versao;
  renderizarCasca(); renderizarTela(); atualizarGaveta();
  for (const fn of app.escutas) fn(estado);
  return true;
}

/** Pergunta a versão a cada 3 s. Carrega o estado quando ainda não há um, quando a última leitura falhou
 *  ou quando a versão mudou; a versão só é "consumida" junto de um estado lido com sucesso. */
async function vigiarVersao() {
  try {
    const { versao } = await api.versao();
    marcarLigado(true);
    if (!app.estado || app.erroEstado || versao !== app.versaoDoEstado) {
      const mudou = !!app.estado && versao !== app.versaoDoEstado;
      if (await carregarEstado(versao) && mudou) piscarAoVivo();
    }
  } catch (e) { marcarLigado(false, e); }
  setTimeout(vigiarVersao, INTERVALO_VERSAO_MS);
}

function marcarLigado(ok, erro) {
  const dot = document.getElementById('ao-vivo');
  if (ok) {
    const estava = app.ligado; app.ligado = true;
    dot.classList.remove('parado'); dot.title = 'ligado ao servidor; atualiza sozinho a cada 3 segundos';
    if (!estava) renderizarFaixa();
  } else {
    app.ligado = false;
    dot.classList.add('parado'); dot.title = `sem ligação com o servidor: ${erro?.message || ''}`;
    renderizarFaixa();
  }
}
function piscarAoVivo() { const dot = document.getElementById('ao-vivo'); dot.classList.add('pulsa'); setTimeout(() => dot.classList.remove('pulsa'), 2500); }

// ------------------------------------------------------------------ casca: menu, contador, problemas, faixa
const TELAS = [
  { id: 'torre', rotulo: 'Início', icone: 'inicio', modulo: telaTorre, sub: 'o caminho até o destino' },
  { id: 'partidas', rotulo: 'Tickets', icone: 'lista', modulo: telaPartidas, sub: 'todos os tickets e o estado deles' },
  { id: 'autorizacoes', rotulo: 'Responder', icone: 'envelope', modulo: telaAutorizacoes, sub: 'rodadas que pedem a sua palavra' },
  { id: 'cartas', rotulo: 'Designs', icone: 'carta', modulo: telaCartas, sub: 'os visuais e por que existem' },
  { id: 'rumo', rotulo: 'Decisões', icone: 'bussola', modulo: telaRumo, sub: 'no horizonte, fora do mapa, diário e legenda' },
  { id: 'lacos', rotulo: 'Laços', icone: 'laco', modulo: telaLacos, sub: 'o que roda por trás' },
];

/** O menu é construído uma vez; depois só o `aria-current` muda (o foco não se perde). */
function montarMenu() {
  const ul = document.getElementById('menu');
  ul.replaceChildren(...TELAS.map(t => h('li', h('a', { href: `#/${t.id}`, title: t.rotulo, dataset: { foco: `menu-${t.id}` } }, icone(t.icone), h('span', t.rotulo)))));
}
function marcarMenu() {
  for (const a of document.querySelectorAll('#menu a')) {
    if (a.getAttribute('href') === `#/${app.rota.tela}`) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  }
}

function renderizarCasca() {
  const e = app.estado; if (!e) return;
  document.getElementById('nome-projeto').textContent = e.projeto?.nome || '';
  document.title = `Torre · ${e.projeto?.nome || ''}`;
  // contador
  const nr = app.aguardando().length;
  const cartasEsp = app.cartasAguardando();
  const n = nr + cartasEsp.length;
  const c = document.getElementById('contador');
  let p = c.querySelector('.palhetas'); let r = c.querySelector('.rotulo');
  if (!p) { p = h('span'); r = h('span.rotulo'); c.replaceChildren(p, r); }
  palhetas(p, n);
  r.textContent = 'aguardando você';
  c.classList.toggle('zerado', n === 0);
  // rodada primeiro (Responder); só cartas: abre a primeira carta que espera o veredito
  c.setAttribute('href', nr || !cartasEsp.length ? '#/autorizacoes' : `#/cartas/${encodeURIComponent(cartasEsp[0].id)}`);
  const partes = [];
  if (nr) partes.push(`${nr} rodada${nr > 1 ? 's' : ''} aberta${nr > 1 ? 's' : ''} esperando a sua resposta`);
  if (cartasEsp.length) partes.push(`${cartasEsp.length > 1 ? `${cartasEsp.length} cartas esperam` : '1 carta espera'} Aprovar ou Recusar: ${cartasEsp.map(x => x.titulo).join('; ')}`);
  c.title = partes.length ? partes.join(' · ') : 'nenhuma rodada ou carta espera você';
  // problemas
  const bp = document.getElementById('problemas');
  const probs = e.problemas || [];
  bp.hidden = probs.length === 0;
  bp.textContent = `⚠ ${probs.length} problema${probs.length === 1 ? '' : 's'}`;
  bp.onclick = abrirProblemas;
  renderizarFaixa();
}

/** A faixa mostra, por prioridade: sem ligação; estado não lido; aviso ao maestro indisponível ou não verificado. */
function renderizarFaixa() {
  const faixa = document.getElementById('faixa-aviso');
  const aviso = app.estado?.aviso;
  if (!app.ligado) {
    faixa.hidden = false; faixa.className = 'faixa-aviso erro';
    faixa.replaceChildren(icone('alerta'), h('strong', 'Sem ligação com o servidor'), h('span', 'o portal mostra o último estado lido e tenta de novo a cada 3 segundos.'));
    return;
  }
  if (app.erroEstado) {
    faixa.hidden = false; faixa.className = 'faixa-aviso erro';
    faixa.replaceChildren(icone('alerta'), h('strong', 'Estado não lido'), h('span', `o servidor responde, mas a leitura do estado falhou: ${app.erroEstado.message}. Tentando de novo a cada 3 segundos; a tela mostra o último estado lido.`));
    return;
  }
  if (!aviso || aviso.disponivel === false || !CANAL_DE_AVISO_VERIFICADO) {
    faixa.hidden = false; faixa.className = 'faixa-aviso';
    const motivo = aviso && aviso.disponivel === false ? aviso.motivo : 'o canal de aviso ainda não foi testado';
    faixa.replaceChildren(icone('balao'), h('strong', 'O maestro não é avisado sozinho'), h('span', `diga "respondi" no chat depois de enviar. Motivo: ${motivo || 'não informado'}.`));
  } else faixa.hidden = true;
}

function abrirProblemas() {
  const d = document.getElementById('dialogo-problemas');
  const probs = app.estado?.problemas || [];
  const caixa = h('div.dialogo-caixa',
    h('header', icone('alerta'), h('h2', `${probs.length} problema${probs.length === 1 ? '' : 's'} nos arquivos`), h('button.fechar', { type: 'button', 'aria-label': 'Fechar' }, icone('fechar'))),
    h('div.corpo', probs.length ? h('ul.lista-problemas', probs.map(p => h('li', h('span.mono', p.arquivo), h('span', p.mensagem)))) : h('p.vazio', 'Nenhum problema.')));
  d.replaceChildren(caixa); d.hidden = false;
  const fechar = prenderFoco(caixa, () => { d.hidden = true; d.replaceChildren(); });
  caixa.querySelector('.fechar').onclick = fechar;
  d.onclick = ev => { if (ev.target === d) fechar(); };
}

// ------------------------------------------------------------------ gaveta do ticket
// A rota (`?ticket=NN`) é a verdade: abrir = navegar; fechar pelo X/Esc = navegar sem o ticket (o "voltar"
// do navegador volta ao ticket anterior). `conciliarGaveta` faz a gaveta seguir a rota.
let gaveta = null; // { numero, fecharVisual }
let origemDaGaveta = null; // chave `data-foco` de quem abriu a primeira gaveta da cadeia (fora dela); o foco volta para lá no fim

function rotaComTicket(numero) {
  const [p, q] = location.hash.split('?'); const ps = new URLSearchParams(q || '');
  if (numero) ps.set('ticket', numero); else ps.delete('ticket');
  return `${p || '#/torre'}${ps.toString() ? '?' + ps : ''}`;
}
export function abrirGaveta(numero) {
  numero = String(numero);
  if (!app.ticket(numero)) { brisa(`Ticket ${numero} não encontrado nos arquivos.`, 'coral'); return; }
  if (app.rota.params.get('ticket') !== numero) {
    history.pushState({ ticket: numero }, '', rotaComTicket(numero));
    app.rota = lerRota();
  }
  conciliarGaveta();
}
function fecharGavetaPelaRota() {
  if (app.rota.params.get('ticket')) { history.pushState({}, '', rotaComTicket(null)); app.rota = lerRota(); }
  conciliarGaveta();
}
/** Faz a gaveta seguir a rota: abre, troca o ticket ou fecha. */
function conciliarGaveta() {
  const alvo = app.rota.params.get('ticket');
  if (!alvo) { if (gaveta) gaveta.fecharVisual(); return; }
  if (!app.estado) return;
  if (gaveta && gaveta.numero === alvo) return;
  const g = document.getElementById('gaveta');
  if (!gaveta) origemDaGaveta = g.contains(document.activeElement) ? null : chaveDoFoco(document.activeElement);
  if (gaveta) gaveta.fecharVisual({ trocando: true });
  const t = app.ticket(alvo);
  if (!t) { brisa(`Ticket ${alvo} não encontrado nos arquivos.`, 'coral'); g.hidden = true; return; }
  g.hidden = false;
  preencherGaveta(g, t);
  const soltar = prenderFoco(g, () => {
    g.hidden = true; g.replaceChildren(); gaveta = null; resultadosRecentes.delete(`ticket:${alvo}`);
    // fechada pelo Esc: a rota também solta o ticket (senão a próxima redesenhada reabria a gaveta)
    if (app.rota.params.get('ticket') === alvo) { history.pushState({}, '', rotaComTicket(null)); app.rota = lerRota(); }
    origemDaGaveta = null;
  }, origemDaGaveta);
  gaveta = { numero: alvo, fecharVisual: (op = {}) => { if (op.trocando) { soltar.soltar(); g.hidden = true; g.replaceChildren(); gaveta = null; resultadosRecentes.delete(`ticket:${alvo}`); } else soltar(); } };
}
/** Depois de uma atualização do estado, o conteúdo da gaveta aberta acompanha o ticket atual. */
function atualizarGaveta() {
  if (!gaveta) return;
  const g = document.getElementById('gaveta');
  const t = app.ticket(gaveta.numero);
  if (!t) { brisa(`O ticket ${gaveta.numero} sumiu dos arquivos.`, 'coral'); fecharGavetaPelaRota(); return; }
  const chave = g.contains(document.activeElement) ? chaveDoFoco(document.activeElement) : null;
  const rolagem = g.querySelector('.gaveta-corpo')?.scrollTop || 0;
  preencherGaveta(g, t, { chave, rolagem });
}
/** Devolve foco e rolagem à gaveta depois de uma redesenhada; chamado duas vezes: com o corpo provisório
 *  (para o foco não cair no body) e depois com o corpo completo (para a ligação focada voltar ao mesmo lugar). */
function restaurarGaveta(g, r) {
  if (!r) return;
  const corpo = g.querySelector('.gaveta-corpo'); if (corpo) corpo.scrollTop = r.rolagem;
  if (!r.chave) return;
  if (emEdicao(document.activeElement) && g.contains(document.activeElement)) return; // nunca tirar o foco de quem escreve
  if (focarPorChave(r.chave, g)) return;
  if (!g.contains(document.activeElement)) (g.querySelector(FOCAVEIS) || g).focus({ preventScroll: true });
}
function preencherGaveta(g, t, restaurar = null) {
  const est = estadoTicket(t); const tipo = tipoTicket(t.tipo);
  const linkTicket = (n, inexistente = false) => {
    const alvo = app.ticket(n);
    return h('li', h('button.ticket-link', { type: 'button', class: `ticket-link${inexistente || !alvo ? ' inexistente' : ''}`, dataset: { foco: `gaveta-lig-${n}` }, onclick: () => abrirGaveta(n) },
      h('span.n-ticket', n), h('span', alvo ? alvo.titulo : 'ticket não encontrado'),
      alvo ? h('span.chip', { class: `chip ${estadoTicket(alvo).classe}` }, estadoTicket(alvo).palavra) : null));
  };
  const bloqueadoPor = [...(t.bloqueado_por || [])];
  const cartas = (t.cartas || []).map(id => app.indices.cartas.get(id)).filter(Boolean);
  const rodadas = (app.estado.rodadas || []).filter(r => r.ticket === t.numero);
  // o corpo é preservado entre atualizações do mesmo ticket (fica o texto antigo até o novo chegar, sem piscar nem
  // pular a rolagem); o rodapé com um formulário aberto também (ver `rodapeDeAcoes`)
  const corpo = h('div.gaveta-corpo', { dataset: { preservar: `gaveta-corpo:${t.numero}` } }, h('p.vazio', 'Lendo o ticket…'));
  trocarPreservando(g, [
    h('div.gaveta-cabeca',
      h('div', { style: 'flex:1;min-width:0' },
        h('div.n-ticket', `ticket ${t.numero} · ${t.arquivo}`),
        h('h2', t.titulo),
        h('div.linha-chips',
          h('span.chip', { class: `chip ${est.classe}` }, icone(est.icone), est.palavra),
          h('span.chip.e-open', icone(tipo.icone), tipo.palavra),
          t.estado === 'open' && t.bloqueios_abertos?.length ? h('span.chip.e-bloqueado', icone('bloqueado'), `espera por ${t.bloqueios_abertos.length}`) : null,
          app.aguardando().some(r => r.ticket === t.numero) ? h('span.chip.e-espera', icone('carimbo'), 'aguarda você') : null)),
      h('button.fechar', { type: 'button', 'aria-label': 'Fechar a gaveta', dataset: { foco: 'gaveta-fechar' }, onclick: () => fecharGavetaPelaRota() }, icone('fechar'))),
    corpo,
    rodapeDeAcoes({ tipo: 'ticket', id: t.numero, titulo: t.titulo })]);
  restaurarGaveta(g, restaurar);
  const numero = t.numero;
  const corpoVivo = corpo.isConnected ? corpo : g.querySelector('.gaveta-corpo');
  api.ticket(numero).then(({ markdown: md }) => {
    if (!corpoVivo || !corpoVivo.isConnected || !gaveta || gaveta.numero !== numero) return; // a gaveta já mudou
    const rolagem = corpoVivo.scrollTop;
    corpoVivo.replaceChildren(...[
      h('div.ligacoes',
        h('div', h('h3', 'bloqueado por'), bloqueadoPor.length ? h('ul', bloqueadoPor.map(n => linkTicket(n, (t.bloqueios_inexistentes || []).includes(n)))) : h('p.vazio', 'nada')),
        h('div', h('h3', 'bloqueia'), t.bloqueia?.length ? h('ul', t.bloqueia.map(n => linkTicket(n))) : h('p.vazio', 'nada'))),
      cartas.length ? h('div', { style: 'margin-bottom:14px' }, h('h3.sub', 'cartas'), h('ul', { style: 'margin:0;padding-left:18px' }, cartas.map(c => h('li', h('a', { href: `#/cartas/${c.id}` }, c.titulo), ` · ${c.proposito}`)))) : null,
      rodadas.length ? h('div', { style: 'margin-bottom:14px' }, h('h3.sub', 'rodadas'), h('ul', { style: 'margin:0;padding-left:18px' }, rodadas.map(r => h('li', h('a', { href: `#/autorizacoes/${r.id}` }, r.titulo), ` · ${r.estado}${r.respondida ? ', respondida' : ''}${r.malformada ? ', malformada' : ''}`)))) : null,
      markdown(semCabecalhoDoTicket(md))].filter(Boolean));
    marcarGlossario(corpoVivo, app.estado.glossario);
    marcarCodigos(corpoVivo, app.estado.projeto?.codigos);
    restaurarGaveta(g, restaurar ? { ...restaurar, rolagem } : null);
  }).catch(e => { if (corpoVivo && corpoVivo.isConnected) corpoVivo.replaceChildren(h('p.vazio', `Não deu para ler o ticket: ${e.message}`)); });
}

// ------------------------------------------------------------------ ações da gaveta: comentar, aprovar, recusar
// Cada ação vira uma mensagem na caixa (POST /api/caixa, §3.4 da proposta). O `envio` (UUID) nasce com o
// formulário e é reaproveitado em "tentar de novo", para a torre reconhecer a repetição.
const ACOES = {
  comentario: { rotulo: 'Comentar', icone: 'balao', classe: '', titulo: 'comentário no ticket', texto: 'obrigatório', dica: 'Escreva o comentário; ele vai para a caixa e o maestro absorve no ticket.' },
  aprovado: { rotulo: 'Aprovar', icone: 'resolvido', classe: 'verde', titulo: 'aprovar o ticket', texto: 'opcional', dica: 'Motivo opcional.' },
  recusado: { rotulo: 'Recusar', icone: 'descartado', classe: 'coral', titulo: 'recusar o ticket', texto: 'obrigatório', dica: 'Diga o motivo da recusa.' },
};
const formulariosAbertos = new Map(); // "tipo:id" do alvo → { acao, envio, texto, emVoo } (sobrevive à redesenhada)
// `emVoo` é o corpo exatamente como foi enviado na primeira tentativa: "tentar de novo" manda esse mesmo corpo com o
// mesmo `envio`, mesmo que o texto tenha sido editado depois; só um envio resolvido (gravado) libera um corpo novo.
const resultadosRecentes = new Map();  // "tipo:id" do alvo → { acao, arquivo, envio, repetido } até o Gustavo dispensar
const chaveAlvo = a => `${a.tipo}:${a.id}`;

/** Botões Comentar / Aprovar / Recusar para um alvo (ticket ou carta), com formulário e confirmação. */
export function rodapeDeAcoes(alvo, op = {}) {
  const k = chaveAlvo(alvo);
  const aberto = formulariosAbertos.get(k);
  // com um formulário aberto, o rodapé inteiro é preservado nas atualizações ao vivo (chave = alvo, ação e envio):
  // o texto, o foco e o cursor ficam; os próprios botões dele o trocam quando o Gustavo age
  const rodape = h('div.gaveta-rodape', { class: `gaveta-rodape${op.compacto ? ' compacto' : ''}`, dataset: aberto ? { preservar: `rodape:${k}:${aberto.acao}:${aberto.envio}` } : null });
  const recente = resultadosRecentes.get(k);
  const botoes = h('div.acoes', Object.entries(ACOES).map(([acao, d]) =>
    h('button.botao', { type: 'button', class: `botao ${d.classe}`.trim(), dataset: { foco: `acao-${acao}` }, 'aria-pressed': aberto?.acao === acao ? 'true' : 'false',
      onclick: () => { if (aberto?.acao === acao) { formulariosAbertos.delete(k); } else { formulariosAbertos.set(k, { acao, envio: crypto.randomUUID(), texto: '' }); } rodape.replaceWith(rodapeDeAcoes(alvo, op)); focarPorChave(`acao-${acao}`); } },
      icone(d.icone), acao === 'comentario' && op.rotuloComentar ? op.rotuloComentar : d.rotulo)));
  rodape.append(botoes);
  if (recente) rodape.append(caixaDeResultado(alvo, op, recente, rodape));
  if (aberto) rodape.append(formularioDeAcao(alvo, op, aberto, rodape));
  return rodape;
}
export function esquecerAcoes(alvo) { formulariosAbertos.delete(chaveAlvo(alvo)); resultadosRecentes.delete(chaveAlvo(alvo)); }

/** A confirmação de uma ação fica na gaveta (sobrevive às atualizações) até ser dispensada ou a gaveta fechar. */
function caixaDeResultado(alvo, op, r, rodape) {
  const d = ACOES[r.acao];
  return h('div.resultado-acao', { tabindex: -1, dataset: { foco: 'acao-resultado' }, role: 'status' },
    h('div', { style: 'display:flex;align-items:center;gap:8px' },
      icone('resolvido'), h('span', { style: 'flex:1' }, `${d.rotulo}: gravado na caixa${r.repetido ? ' (já estava gravado)' : ''}. O maestro absorve no ticket.`),
      h('button.fechar', { type: 'button', 'aria-label': 'Dispensar a confirmação', style: 'width:26px;height:26px', onclick: () => { resultadosRecentes.delete(chaveAlvo(alvo)); rodape.replaceWith(rodapeDeAcoes(alvo, op)); focarPorChave(`acao-${r.acao}`); } }, icone('fechar'))),
    h('div.mono', r.arquivo || ''),
    h('div', { style: 'font-size:12px;color:var(--texto-apagado)' }, `envio ${String(r.envio).slice(0, 8)}…`));
}

function formularioDeAcao(alvo, op, form, rodape) {
  const d = ACOES[form.acao];
  const k = chaveAlvo(alvo);
  const titulos = { comentario: `comentário ${alvo.tipo === 'carta' ? 'na carta' : 'no ticket'}`, aprovado: `aprovar ${alvo.tipo === 'carta' ? 'a carta' : 'o ticket'}`, recusado: `recusar ${alvo.tipo === 'carta' ? 'a carta' : 'o ticket'}` };
  const erro = h('div.erro-acao', { role: 'alert' });
  const contagem = h('span.contagem');
  const area = h('textarea', { 'aria-label': d.titulo, placeholder: d.dica, maxlength: '20000', dataset: { foco: 'acao-texto' },
    oninput: ev => { form.texto = ev.target.value; contagem.textContent = `${form.texto.length} / 20000`; erro.textContent = form.emVoo ? 'Há um envio pendente: "Tentar de novo" manda o texto original; o que você editou só vai depois que ele for resolvido.' : ''; } });
  area.value = form.texto; contagem.textContent = `${form.texto.length} / 20000`;
  const enviar = h('button.botao.primario', { type: 'button', dataset: { foco: 'acao-enviar' } }, icone('carimbo'), form.emVoo ? 'Tentar de novo' : form.acao === 'comentario' ? 'Enviar à torre' : `${d.rotulo} e enviar`);
  if (form.emVoo) erro.textContent = `Envio pendente (${form.emVoo.motivo}). "Tentar de novo" reenvia a mesma mensagem com o mesmo envio.`;
  const cancelar = h('button.botao', { type: 'button', onclick: () => { formulariosAbertos.delete(k); rodape.replaceWith(rodapeDeAcoes(alvo, op)); focarPorChave(`acao-${form.acao}`); } }, 'Cancelar');
  const caixa = h('div.formulario-acao',
    h('div.titulo-acao', icone(d.icone), titulos[form.acao], h('span', { style: 'font-weight:400;letter-spacing:0;text-transform:none;color:var(--texto-apagado)' }, `· texto ${d.texto}`)),
    area, erro, h('div.rodape-acao', enviar, cancelar, contagem));
  const concluir = (r) => {
    formulariosAbertos.delete(k);
    resultadosRecentes.set(k, { acao: form.acao, arquivo: r.arquivo, envio: r.envio || form.envio, repetido: !!r.repetido });
    rodape.replaceWith(rodapeDeAcoes(alvo, op));
    focarPorChave('acao-resultado');
    brisa(`${d.rotulo}: gravado na caixa.`, 'verde');
  };
  enviar.onclick = async () => {
    let corpo;
    if (form.emVoo) corpo = form.emVoo.corpo; // retentativa: o mesmo par (envio, corpo), sem reconstruir
    else {
      const texto = form.texto.trim();
      if (!texto && form.acao !== 'aprovado') { erro.textContent = form.acao === 'comentario' ? 'Escreva o comentário antes de enviar.' : 'A recusa precisa de um motivo.'; area.focus(); return; }
      corpo = form.acao === 'comentario'
        ? { envio: form.envio, tipo: 'comentario', alvo: { tipo: alvo.tipo, id: alvo.id }, texto }
        : { envio: form.envio, tipo: 'aprovacao', alvo: { tipo: alvo.tipo, id: alvo.id }, veredito: form.acao, ...(texto ? { texto } : {}) };
    }
    enviar.disabled = true; cancelar.disabled = true; erro.textContent = '';
    try {
      const r = await api.caixa(corpo);
      concluir(r);
    } catch (e) {
      enviar.disabled = false; cancelar.disabled = false;
      const ambiguo = !e.status || e.status >= 500; // a torre pode ter gravado sem a resposta chegar
      if (ambiguo) {
        form.emVoo = { corpo, motivo: e.message };
        erro.textContent = `Não deu para confirmar a gravação (${e.message}). "Tentar de novo" reenvia a mesma mensagem com o mesmo envio.`;
        enviar.replaceChildren(icone('carimbo'), 'Tentar de novo');
      } else if (e.status === 409 && e.corpo?.erro === 'envio-conflito') {
        // o envio já existe com outro corpo: o primeiro envio foi gravado; é ele que vale
        try { const g = await api.caixaItem(corpo.envio); concluir({ envio: g.envio, arquivo: g.arquivo, repetido: true }); return; }
        catch { erro.textContent = 'A torre diz que este envio já existe com outro conteúdo, mas não deu para relê-lo. Recarregue a página e confira a caixa.'; }
      } else {
        erro.textContent = `A torre recusou: ${e.message}${e.corpo?.campo ? ` (campo ${e.corpo.campo})` : ''}.`;
        form.emVoo = null; enviar.replaceChildren(icone('carimbo'), form.acao === 'comentario' ? 'Enviar à torre' : `${d.rotulo} e enviar`);
      }
      enviar.focus();
    }
  };
  return caixa;
}

/** Tira do Markdown do ticket o `# Título` e as linhas Type/Status/Blocked by, que a gaveta já mostra em chips. */
function semCabecalhoDoTicket(md) {
  const linhas = (md || '').split(/\r?\n/);
  let i = 0;
  if (linhas[0] && /^#\s/.test(linhas[0])) i = 1;
  while (i < linhas.length && (/^\s*$/.test(linhas[i]) || /^(Type|Status|Blocked by):/i.test(linhas[i]))) i++;
  return linhas.slice(i).join('\n');
}

// ------------------------------------------------------------------ rotas
function lerRota() {
  const bruto = location.hash.replace(/^#\/?/, '') || 'torre';
  const [caminho, q] = bruto.split('?');
  const [tela, ...sub] = caminho.split('/');
  return { tela: TELAS.some(t => t.id === tela) ? tela : 'torre', sub: sub.length ? decodeURIComponent(sub.join('/')) : null, params: new URLSearchParams(q || '') };
}

const ferramentas = { h, svg, icone, palhetas, markdown, marcarGlossario, abrirGaveta, brisa, prenderFoco, tipoTicket, estadoTicket, acoes: rodapeDeAcoes, repousoDaFaixa };

/** Redesenha a tela atual preservando rolagem e o foco (pela chave `data-foco`). */
function renderizarTela() {
  const def = TELAS.find(t => t.id === app.rota.tela);
  const main = document.getElementById('tela');
  document.getElementById('rota-atual').replaceChildren(icone(def.icone), def.rotulo, h('small', def.sub));
  marcarMenu();
  if (!app.estado) return;
  const topo = main.scrollTop;
  const focoAntes = main.contains(document.activeElement) ? chaveDoFoco(document.activeElement) : null;
  document.dispatchEvent(new CustomEvent('torre:redesenhando'));
  repousoDaFaixa();
  trocarPreservando(main, def.modulo.renderizar(app, ferramentas));
  marcarGlossario(main, app.estado.glossario);
  marcarCodigos(main, app.estado.projeto?.codigos);
  main.scrollTop = topo;
  if (focoAntes && !focarPorChave(focoAntes, main)) main.focus({ preventScroll: true });
  conciliarGaveta();
}

function aoMudarRota() { app.rota = lerRota(); renderizarTela(); }
// uma tela pode pedir para ser redesenhada sem mudar a rota nem o estado (ex.: "corrigir resposta")
document.addEventListener('torre:redesenhar', () => renderizarTela());
window.addEventListener('hashchange', aoMudarRota);
window.addEventListener('popstate', aoMudarRota);

// ------------------------------------------------------------------ arranque
app.rota = lerRota();
montarMenu(); marcarMenu();
document.getElementById('rota-atual').replaceChildren(icone('inicio'), 'Início');
vigiarVersao();
