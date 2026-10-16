// Tela Decisões (rota rumo): no horizonte (o "Radar" da estratégia), diário de bordo (decisões do mapa), fora da rota
// (não especificado e fora do escopo) e o glossário.

export function renderizar(app, u) {
  const { h } = u;
  return h('div.rumo',
    radar(app, u),
    foraDaRota(app, u),
    diario(app, u),
    glossario(app, u));
}

const limpar = s => String(s || '').replace(/\*\*/g, '').replace(/`/g, '');

function radar(app, u) {
  const { h, svg, icone } = u;
  const itens = app.estado.radar || [];
  // no horizonte: anéis de rumo sobre o papel; cada eco leva um número, e a lista ao lado traz o mesmo número
  const R = 180, M = 26, C = R + M, LARG = 2 * C;
  const g = svg('svg', { class: 'radar-tela', viewBox: `0 0 ${LARG} ${LARG}`, role: 'group', 'aria-label': `no horizonte: ${itens.length} temas no ar, ainda longe` });
  g.append(svg('defs', {},
    svg('linearGradient', { id: 'g-varredura', x1: '0', y1: '0', x2: '1', y2: '0' }, svg('stop', { offset: '0', style: 'stop-color:var(--ciano);stop-opacity:0' }), svg('stop', { offset: '1', style: 'stop-color:var(--ciano);stop-opacity:.22' }))));
  g.append(svg('circle', { class: 'fundo', cx: C, cy: C, r: R }));
  for (const f of [0.25, 0.5, 0.75]) g.append(svg('circle', { class: 'anel', cx: C, cy: C, r: R * f }));
  for (let k = 0; k < 16; k++) { const a = k * Math.PI / 8; g.append(svg('line', { class: k % 4 ? 'rumo-fino' : 'rumo', x1: C, y1: C, x2: C + R * Math.cos(a), y2: C + R * Math.sin(a) })); }
  g.append(svg('path', { class: 'varredura', d: `M${C} ${C} L${C + R} ${C} A${R} ${R} 0 0 0 ${C + R * Math.cos(-Math.PI / 3)} ${C + R * Math.sin(-Math.PI / 3)} Z`, fill: 'url(#g-varredura)', style: `transform-origin:${C}px ${C}px` }));
  const n = Math.max(itens.length, 1);
  itens.forEach((it, i) => {
    const ang = -Math.PI / 2 + i * 2 * Math.PI / n + Math.PI / n;
    const raio = R * (i % 2 ? 0.8 : 0.5);
    const x = C + raio * Math.cos(ang), y = C + raio * Math.sin(ang);
    const tema = limpar(it.tema), gat = limpar(it.gatilho);
    g.append(svg('g', { class: 'eco', tabindex: 0, role: 'img', 'aria-label': `${i + 1}: ${tema}. Volta quando: ${gat}`, 'data-dica-titulo': tema, 'data-dica': `volta quando: ${gat}`, 'data-foco': `radar-${i}` },
      svg('circle', { class: 'halo', cx: x, cy: y, r: 17 }),
      svg('text', { x, y: y + 6, 'text-anchor': 'middle' }, String(i + 1))));
  });
  return h('section.painel-radar',
    h('h2.secao-titulo', icone('radar'), 'No horizonte', h('span.sub', 'no ar, ainda longe; cada eco diz o gatilho que o traz de volta')),
    itens.length ? g : h('p.vazio', 'Nenhum tema no horizonte da estratégia.'),
    h('ol.lista-radar', itens.map((it, i) => h('li', h('button.com-dica', { type: 'button', dataset: { dica: `volta quando: ${limpar(it.gatilho)}`, dicaTitulo: limpar(it.tema), foco: `radar-lista-${i}` } }, h('span.ponto-lista', String(i + 1)), limpar(it.tema))))));
}

function foraDaRota(app, u) {
  const { h, icone } = u;
  const f = app.estado.fora || { nao_especificado: [], fora_do_escopo: [] };
  const col = (titulo, itens, vazio) => h('div.coluna-fora', h('h3', titulo, h('span.n', String(itens.length))), itens.length ? h('ul', itens.map(x => h('li', limpar(x)))) : h('p.vazio', vazio));
  return h('section.painel.fora-da-rota',
    h('h2.secao-titulo', icone('pista'), 'Fora do mapa'),
    h('div.colunas-fora', col('ainda não especificado', f.nao_especificado, 'nada pendente de especificar'), col('fora do escopo', f.fora_do_escopo, 'nada fora do escopo')));
}

function diario(app, u) {
  const { h, icone, abrirGaveta } = u;
  const ds = [...(app.estado.decisoes || [])].reverse();
  return h('section.diario',
    h('h2.secao-titulo', icone('resolvido'), 'Diário de bordo', h('span.n', String(ds.length)), h('span.sub', 'as decisões do mapa, da mais recente à primeira')),
    ds.length ? h('ol.linha-do-tempo', ds.map((d, i) => h('li', { dataset: { foco: `decisao-${d.numero}-${i}` } },
      h('span.marca-pouso'),
      h('details', h('summary', h('span.n-ticket', d.numero), h('span.titulo', d.titulo)),
        h('p.resumo', d.resumo),
        h('button.botao', { type: 'button', onclick: () => abrirGaveta(d.numero) }, 'Abrir o ticket'))))) : h('p.vazio', 'Nenhuma decisão registrada no mapa ainda.'));
}

function glossario(app, u) {
  const { h, icone } = u;
  const gs = app.estado.glossario || [];
  return h('section.glossario-tela',
    h('h2.secao-titulo', icone('pergunta'), 'Legenda do mapa', h('span.n', String(gs.length)), h('span.sub', 'o glossário: os termos aparecem sublinhados em qualquer tela; passe o mouse ou foque para ver a definição')),
    gs.length ? h('dl.termos', gs.map(g => h('div.termo-par', h('dt', g.termo), h('dd', g.definicao, g.evite ? h('span.evite', ` evite: ${g.evite}`) : null)))) : h('p.vazio', 'Glossário vazio.'));
}
