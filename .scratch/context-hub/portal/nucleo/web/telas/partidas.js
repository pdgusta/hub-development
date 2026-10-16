// Tela Partidas: letreiro de palhetas com todos os tickets, filtros por estado e tipo, busca, e a vista
// "Rotas" (grafo de todas as dependências, resolvidos esmaecidos). Filtros vivem na rota (?estado=&tipo=&q=).

const ESTADOS = [['open', 'aberto'], ['claimed', 'em andamento'], ['resolved', 'resolvido'], ['wontfix', 'descartado'], ['desconhecido', 'desconhecido']];
const TIPOS = [['research', 'pesquisa'], ['grilling', 'conversa'], ['prototype', 'protótipo'], ['task', 'tarefa']];
const NO_L = 196, NO_A = 52, COL_GAP = 56, LIN_GAP = 10, MARGEM = 16;

// linhas do letreiro guardadas por número de ticket, para as palhetas virarem só nas letras que mudaram
const linhas = new Map();

export function renderizar(app, u) {
  const { h } = u;
  const vista = app.rota.sub === 'rotas' ? 'rotas' : 'letreiro';
  const f = lerFiltros(app);
  return h('div.partidas',
    barraDeFiltros(app, u, f, vista),
    vista === 'rotas' ? rotas(app, u, f) : letreiro(app, u, f));
}

function lerFiltros(app) {
  const p = app.rota.params;
  return { estado: p.get('estado') || '', tipo: p.get('tipo') || '', q: (p.get('q') || '').trim() };
}
function gravarFiltros(app, f) {
  const [caminho] = location.hash.split('?');
  const ps = new URLSearchParams(location.hash.split('?')[1] || '');
  for (const k of ['estado', 'tipo', 'q']) { if (f[k]) ps.set(k, f[k]); else ps.delete(k); }
  history.replaceState(history.state, '', `${caminho}${ps.toString() ? '?' + ps : ''}`);
  app.rota.params = ps;
}
function passa(t, f) {
  if (!t) return false;
  if (f.estado && t.estado !== f.estado) return false;
  if (f.tipo && t.tipo !== f.tipo) return false;
  if (f.q) { const q = f.q.toLowerCase(); if (!t.titulo.toLowerCase().includes(q) && !t.numero.includes(q)) return false; }
  return true;
}
function sufixo(f) { const ps = new URLSearchParams(); for (const k of ['estado', 'tipo', 'q']) if (f[k]) ps.set(k, f[k]); return ps.toString() ? '?' + ps : ''; }
const reduz = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ------------------------------------------------------------------ filtros
function barraDeFiltros(app, u, f, vista) {
  const { h, icone, tipoTicket } = u;
  const ts = app.estado.tickets || [];
  const conta = fn => ts.filter(fn).length;
  const chip = (grupo, valor, rotulo, n, ic) => {
    const ativo = f[grupo] === valor;
    return h('button.chip-filtro', { type: 'button', class: `chip-filtro${ativo ? ' ativo' : ''} ${grupo === 'estado' ? 'e-' + valor : ''}`, 'aria-pressed': ativo ? 'true' : 'false', dataset: { foco: `filtro-${grupo}-${valor}`, grupo, valor },
      onclick: () => { f[grupo] = f[grupo] === valor ? '' : valor; gravarFiltros(app, f); aplicarFiltros(app, f); } },
      ic ? icone(ic) : null, rotulo, h('span.n', String(n)));
  };
  const busca = h('input.busca', { type: 'search', placeholder: 'buscar no título', value: f.q, 'aria-label': 'buscar no título ou número', dataset: { foco: 'busca' },
    oninput: ev => { f.q = ev.target.value.trim(); gravarFiltros(app, f); aplicarFiltros(app, f); } });
  const alternar = h('div.alternar', { role: 'group', 'aria-label': 'vista' },
    h('a', { href: `#/partidas${sufixo(f)}`, class: vista === 'letreiro' ? 'ativo' : '', 'aria-current': vista === 'letreiro' ? 'page' : null, dataset: { foco: 'vista-letreiro' } }, icone('lista'), 'Lista'),
    h('a', { href: `#/partidas/rotas${sufixo(f)}`, class: vista === 'rotas' ? 'ativo' : '', 'aria-current': vista === 'rotas' ? 'page' : null, dataset: { foco: 'vista-rotas' } }, icone('bussola'), 'Quem espera quem'));
  return h('div.filtros',
    h('div.grupo', { role: 'group', 'aria-label': 'filtrar por estado' }, ESTADOS.map(([v, r]) => chip('estado', v, r, conta(t => t.estado === v)))),
    h('div.grupo', { role: 'group', 'aria-label': 'filtrar por tipo' }, TIPOS.map(([v, r]) => chip('tipo', v, r, conta(t => t.tipo === v), tipoTicket(v).icone))),
    busca, alternar);
}

/** Aplica os filtros sem redesenhar a tela: esconde linhas, esmaece nós e atualiza chips e links da vista. */
function aplicarFiltros(app, f) {
  const tela = document.getElementById('tela');
  for (const b of tela.querySelectorAll('.chip-filtro')) {
    const ativo = f[b.dataset.grupo] === b.dataset.valor; b.classList.toggle('ativo', ativo); b.setAttribute('aria-pressed', ativo ? 'true' : 'false');
  }
  const a1 = tela.querySelector('[data-foco="vista-letreiro"]'), a2 = tela.querySelector('[data-foco="vista-rotas"]');
  if (a1) a1.setAttribute('href', `#/partidas${sufixo(f)}`); if (a2) a2.setAttribute('href', `#/partidas/rotas${sufixo(f)}`);
  let visiveis = 0;
  for (const tr of tela.querySelectorAll('tr.linha')) { const ok = passa(app.ticket(tr.dataset.numero), f); tr.hidden = !ok; if (ok) visiveis++; }
  reconciliarEntrada(tela.querySelector('table.letreiro tbody'));
  const vazio = tela.querySelector('.letreiro-vazio'); if (vazio) vazio.hidden = visiveis > 0;
  const tot = tela.querySelector('.letreiro-total'); if (tot) tot.textContent = `${visiveis} de ${(app.estado.tickets || []).length}`;
  for (const g of tela.querySelectorAll('svg.rotas .no')) g.classList.toggle('fora', !passa(app.ticket(g.dataset.numero), f));
}

/** Roving tabindex: exatamente uma linha visível entra pelo Tab (a corrente, se continua visível; senão a primeira). */
function reconciliarEntrada(tbody) {
  if (!tbody) return;
  const linhasVis = [...tbody.querySelectorAll('tr.linha:not([hidden])')];
  const corrente = linhasVis.find(tr => tr === document.activeElement) || linhasVis.find(tr => tr.tabIndex === 0) || linhasVis[0] || null;
  for (const tr of tbody.querySelectorAll('tr.linha')) tr.tabIndex = tr === corrente ? 0 : -1;
}

// ------------------------------------------------------------------ letreiro
function letreiro(app, u, f) {
  const { h, icone, palhetas, abrirGaveta, estadoTicket, tipoTicket } = u;
  const ts = app.estado.tickets || [];
  const esperando = new Set(app.aguardando().map(r => r.ticket));
  const tbody = h('tbody');
  let visiveis = 0;
  for (const t of ts) {
    let tr = linhas.get(t.numero);
    if (!tr) {
      tr = h('tr.linha', { tabindex: -1, dataset: { numero: t.numero, foco: `linha-${t.numero}` } });
      tr.append(h('td.col-n', h('span.n-ticket')), h('td.col-titulo', h('span.titulo')), h('td.col-tipo'), h('td.col-estado', h('span.chip', h('span.palavra'))), h('td.col-espera'), h('td.col-voce'));
      // clique ou tecla vindos de um controle dentro da linha (as dicas de "espera por") não abrem a gaveta
      tr.addEventListener('click', ev => { if (ev.target.closest('button')) return; abrirGaveta(tr.dataset.numero); });
      tr.addEventListener('keydown', ev => {
        if (ev.target !== tr) return; // Enter/setas só agem quando a própria linha tem o foco
        const vis = () => [...tr.parentElement.querySelectorAll('tr.linha:not([hidden])')];
        const ir = p => { if (p) { ev.preventDefault(); tr.tabIndex = -1; p.tabIndex = 0; p.focus(); } };
        if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); abrirGaveta(tr.dataset.numero); }
        else if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') { const v = vis(); const i = v.indexOf(tr); ir(v[ev.key === 'ArrowDown' ? i + 1 : i - 1]); }
        else if (ev.key === 'Home') ir(vis()[0]);
        else if (ev.key === 'End') { const v = vis(); ir(v[v.length - 1]); }
      });
      linhas.set(t.numero, tr);
    }
    const est = estadoTicket(t); const tipo = tipoTicket(t.tipo);
    tr.className = `linha ${est.classe}`;
    tr.querySelector('.n-ticket').textContent = t.numero;
    palhetas(tr.querySelector('.titulo'), t.titulo);
    tr.querySelector('.col-tipo').replaceChildren(icone(tipo.icone), h('span', tipo.palavra));
    const chip = tr.querySelector('.col-estado .chip'); chip.className = `chip ${est.classe}`;
    palhetas(chip.querySelector('.palavra'), est.palavra);
    const esp = t.estado === 'open' || t.estado === 'claimed' ? (t.bloqueios_abertos || []).length : 0;
    const inex = (t.bloqueios_inexistentes || []).length;
    tr.querySelector('.col-espera').replaceChildren(...[
      esp ? h('button.espera.com-dica', { type: 'button', dataset: { foco: `espera-${t.numero}`, dica: `espera por ${t.bloqueios_abertos.map(b => app.ticket(b)?.titulo || b).join(', ')}`, dicaTitulo: 'espera por' } }, icone('bloqueado'), String(esp)) : h('span.nada', '—'),
      inex ? h('button.c-coral.com-dica', { type: 'button', style: 'margin-left:6px', dataset: { foco: `quebrada-${t.numero}`, dica: `Blocked by aponta para ticket inexistente: ${t.bloqueios_inexistentes.join(', ')}`, dicaTitulo: 'dependência quebrada' } }, icone('alerta')) : null].filter(Boolean));
    tr.querySelector('.col-voce').replaceChildren(...[esperando.has(t.numero) ? h('span.voce', icone('carimbo'), 'aguarda você') : null].filter(Boolean));
    tr.hidden = !passa(t, f); if (!tr.hidden) visiveis++;
    tr.setAttribute('aria-label', `${t.numero} ${t.titulo}, ${tipo.palavra}, ${est.palavra}${esp ? `, espera por ${t.bloqueios_abertos.map(b => app.ticket(b)?.titulo || b).join(', ')}` : ''}${inex ? `, Blocked by aponta para ticket inexistente ${t.bloqueios_inexistentes.join(', ')}` : ''}${esperando.has(t.numero) ? ', aguarda você' : ''}`);
    tbody.append(tr);
  }
  for (const n of [...linhas.keys()]) if (!app.ticket(n)) linhas.delete(n);
  reconciliarEntrada(tbody);
  const tabela = h('table.letreiro', { 'aria-label': 'tickets' },
    h('thead', h('tr', h('th', { scope: 'col' }, 'nº'), h('th', { scope: 'col' }, 'ticket'), h('th', { scope: 'col' }, 'tipo'), h('th', { scope: 'col' }, 'estado'), h('th', { scope: 'col' }, 'espera por'), h('th', { scope: 'col' }, h('span.visualmente-oculto', 'aguarda você')))),
    tbody);
  // cascata de palhetas na primeira vez que a tela aparece
  if (!reduz()) { let i = 0; for (const tr of tbody.children) { if (tr.hidden) continue; tr.style.setProperty('--atraso', `${Math.min(i * 28, 900)}ms`); tr.classList.add('cascata'); i++; } }
  return h('section.letreiro-painel',
    h('div.letreiro-topo', h('h2.secao-titulo', icone('lista'), 'Todos os tickets'), h('span.letreiro-total', `${visiveis} de ${ts.length}`), h('span.letreiro-dica', 'setas navegam; Enter abre a gaveta')),
    tabela,
    h('p.vazio.letreiro-vazio', { hidden: visiveis > 0 }, 'Nenhum ticket passa pelos filtros.'));
}

// ------------------------------------------------------------------ rotas (grafo de todas as dependências)
function rotas(app, u, f) {
  const { h, svg, icone, abrirGaveta, estadoTicket } = u;
  const ts = app.estado.tickets || [];
  const por = new Map(ts.map(t => [t.numero, t]));
  const esperando = new Set(app.aguardando().map(r => r.ticket));
  // arestas bloqueador → dependente, só entre tickets existentes; a volta de cada ciclo é ignorada para as camadas
  const ignoradas = new Set((app.estado.plano_de_voo?.ciclos || []).map(c => c.aresta_ignorada.join('>')));
  const dentro = new Map(ts.map(t => [t.numero, []])); // dependente → bloqueadores existentes
  const arestas = []; const quebradas = [];
  for (const t of ts) for (const b of t.bloqueado_por || []) {
    if (!por.has(b)) { quebradas.push([t.numero, b]); continue; }
    arestas.push([b, t.numero]); if (!ignoradas.has(`${t.numero}>${b}`)) dentro.get(t.numero).push(b);
  }
  // camadas por caminho mais longo, com quebra genérica de ciclos que a API não listou (DFS)
  const camada = new Map(); const visitando = new Set(); const ciclosExtras = [];
  const prof = n => {
    if (camada.has(n)) return camada.get(n);
    if (visitando.has(n)) { ciclosExtras.push(n); return 0; }
    visitando.add(n);
    let p = 0; for (const b of dentro.get(n) || []) p = Math.max(p, prof(b) + 1);
    visitando.delete(n); camada.set(n, p); return p;
  };
  for (const t of ts) prof(t.numero);
  const colunas = []; for (const [n, c] of camada) (colunas[c] ||= []).push(n);
  for (const c of colunas) c && c.sort();
  const maxLinhas = Math.max(1, ...colunas.map(c => (c || []).length));
  const altura = MARGEM * 2 + 22 + maxLinhas * NO_A + (maxLinhas - 1) * LIN_GAP;
  const largura = MARGEM * 2 + colunas.length * NO_L + (colunas.length - 1) * COL_GAP;
  const pos = new Map();
  colunas.forEach((col, i) => {
    if (!col) return;
    const hCol = col.length * NO_A + (col.length - 1) * LIN_GAP; const y0 = MARGEM + 22 + (altura - MARGEM * 2 - 22 - hCol) / 2;
    col.forEach((n, j) => pos.set(n, { x: MARGEM + i * (NO_L + COL_GAP), y: y0 + j * (NO_A + LIN_GAP) }));
  });
  const g = svg('svg', { class: 'rotas', viewBox: `0 0 ${largura} ${altura}`, width: largura, height: altura, role: 'group', 'aria-label': 'rotas: todas as dependências entre tickets, da esquerda para a direita' });
  colunas.forEach((c, i) => c && g.append(svg('text', { class: 'camada-rotulo', x: MARGEM + i * (NO_L + COL_GAP), y: MARGEM + 8 }, i === 0 ? 'sem bloqueio' : `nível ${i}`)));
  const curva = (a, b) => a.x < b.x
    ? `M${a.x + NO_L} ${a.y + NO_A / 2} C ${a.x + NO_L + COL_GAP / 2} ${a.y + NO_A / 2}, ${b.x - COL_GAP / 2} ${b.y + NO_A / 2}, ${b.x} ${b.y + NO_A / 2}`
    : `M${a.x} ${a.y + NO_A} C ${a.x - 20} ${a.y + NO_A + 26}, ${b.x + NO_L + 20} ${b.y + NO_A + 26}, ${b.x + NO_L} ${b.y + NO_A}`;
  for (const [b, n] of arestas) {
    const pb = pos.get(b), pn = pos.get(n); if (!pb || !pn) continue;
    const ciclo = ignoradas.has(`${n}>${b}`);
    const pousou = por.get(b).estado === 'resolved';
    const texto = ciclo ? `${por.get(n).titulo} e ${por.get(b).titulo} dependem um do outro` : `${por.get(b).titulo} ${pousou ? 'liberou' : 'libera'} ${por.get(n).titulo}`;
    g.append(svg('g', { class: `aresta-g${pousou ? ' pousada' : ''}`, tabindex: 0, role: 'img', 'aria-label': texto, 'data-dica': texto, 'data-dica-titulo': ciclo ? 'ciclo de dependência' : 'dependência', 'data-foco': `rota-aresta-${b}-${n}` },
      svg('path', { class: 'aresta-alvo', d: curva(pb, pn) }), svg('path', { class: `aresta${ciclo ? ' ciclo' : ''}`, d: curva(pb, pn) })));
  }
  for (const [n, b] of quebradas) {
    const pn = pos.get(n); if (!pn) continue;
    const texto = `"Blocked by" de ${por.get(n).titulo} aponta para o ticket ${b}, que não foi encontrado`;
    g.append(svg('g', { class: 'fantasma', tabindex: 0, role: 'img', 'aria-label': texto, 'data-dica': texto, 'data-dica-titulo': 'dependência quebrada', 'data-foco': `rota-fantasma-${n}-${b}` },
      svg('path', { class: 'aresta quebrada', d: `M${pn.x - 22} ${pn.y + NO_A / 2} L ${pn.x} ${pn.y + NO_A / 2}` }),
      svg('circle', { cx: pn.x - 26, cy: pn.y + NO_A / 2, r: 5, fill: 'none', stroke: 'var(--coral)', 'stroke-dasharray': '2 2' })));
  }
  for (const [n, p] of pos) {
    const t = por.get(n); const est = estadoTicket(t);
    const titulo = t.titulo.length > 21 ? t.titulo.slice(0, 20).trimEnd() + '…' : t.titulo;
    const desc = `${est.palavra}${(t.bloqueios_abertos || []).length ? `; espera por ${t.bloqueios_abertos.map(b => por.get(b)?.titulo || b).join(', ')}` : ''}${esperando.has(n) ? '; uma rodada aguarda você' : ''}. Enter abre a gaveta.`;
    const no = svg('g', { class: `no ${t.estado}${esperando.has(n) ? ' espera' : ''}${passa(t, f) ? '' : ' fora'}`, tabindex: 0, role: 'button', 'aria-label': `ticket ${n}: ${t.titulo}, ${desc}`, 'data-dica': desc, 'data-dica-titulo': t.titulo, 'data-dica-sem-clique': '1', 'data-foco': `rota-no-${n}`, 'data-numero': n, transform: `translate(${p.x} ${p.y})` },
      svg('rect', { class: 'caixa', width: NO_L, height: NO_A }),
      svg('text', { class: 'numero', x: 10, y: 19 }, n),
      svg('text', { class: 'titulo', x: 10, y: 40 }, titulo),
      esperando.has(n) ? svg('circle', { class: 'marca-espera', cx: NO_L - 8, cy: 8, r: 4 }) : null);
    no.addEventListener('click', () => abrirGaveta(n));
    no.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); abrirGaveta(n); } });
    g.append(no);
  }
  const legenda = h('div.plano-legenda',
    h('span', h('i', { style: 'color:var(--ciano)' }), 'em andamento'), h('span', h('i', { style: 'color:var(--cinza)' }), 'aberto'),
    h('span', h('i', { style: 'color:var(--verde)' }), 'resolvido'), h('span', h('i', { style: 'color:var(--texto-apagado);border-style:dashed' }), 'descartado / desconhecido'),
    h('span', h('i', { style: 'color:var(--ambar)' }), 'aguarda você'), h('span', h('i', { style: 'color:var(--coral);border-style:dashed' }), 'quebrada / ciclo'));
  return h('section.plano-painel.rotas-painel',
    h('div.cabeca', h('h2.secao-titulo', icone('bussola'), 'Quem espera quem'), legenda),
    h('div.plano-rolagem', g),
    ciclosExtras.length ? h('p.plano-ciclo-aviso', icone('alerta'), `ciclo de dependência envolvendo ${ciclosExtras.map(n => por.get(n)?.titulo || n).join(', ')}; desenhado sem a volta.`) : null);
}
