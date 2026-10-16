// Tela Início: o caminho até o destino, numa faixa da largura toda. À esquerda, o índice a tinta (o que já foi
// feito); no meio, os tickets abertos a lápis, em colunas que são as camadas do plano de voo e ligados por fios de
// quem bloqueia para quem espera; à direita, o cartucho do destino com os critérios. Abaixo: o que espera a sua
// resposta e as últimas decisões do mapa. Tudo vem de /api/estado; nada aqui é do projeto.

const FEITO = e => e === 'resolved' || e === 'wontfix';
let escolhido = null;        // número do marco escolhido; sobrevive aos redesenhos
let folhaAtiva = null;       // quadrado que recebe o Tab no índice (roving tabindex)
let jaAnimou = false;        // a tinta assenta e o lápis traça só na primeira vez
let observador = null;
let soltarAtual = null;
document.addEventListener('torre:redesenhando', () => { if (observador) { observador.disconnect(); observador = null; } soltarAtual = null; });
// Esc solta o marco escolhido (a casca cuida de dispensar a dica)
document.addEventListener('keydown', e => { if (e.key === 'Escape' && escolhido && soltarAtual) soltarAtual(); });

export function renderizar(app, u) {
  const { h } = u;
  return h('div', { class: jaAnimou ? 'inicio ja-animou' : 'inicio' }, saudacao(app, u), caminho(app, u), h('div.inicio-baixo', paraResponder(app, u), decisoes(app, u)));
}

// ------------------------------------------------------------------ saudação
function saudacao(app, u) {
  const { h } = u;
  const agora = new Date(), hora = agora.getHours();
  const ola = hora < 12 ? 'Bom dia' : hora < 18 ? 'Boa tarde' : 'Boa noite';
  const dia = agora.toLocaleDateString('pt-BR', { weekday: 'long' });
  const data = agora.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  const ts = app.estado.tickets || [];
  const feitos = ts.filter(t => t.estado === 'resolved').length;
  const abertos = ts.filter(t => t.estado === 'open' || t.estado === 'claimed').length;
  const plano = (app.estado.plano_de_voo?.camadas || []).flat().length;
  return h('header.saudacao',
    h('h1', `${ola}. Aqui está a mesa de hoje.`),
    h('p.sub', `${dia}, ${data} · ${feitos} ${feitos === 1 ? 'ticket feito' : 'tickets feitos'}, ${abertos} ${abertos === 1 ? 'aberto' : 'abertos'}${plano ? '; aceite final do destino pendente' : ''}`));
}

// ------------------------------------------------------------------ o caminho até o destino
function caminho(app, u) {
  const { h, svg, icone, abrirGaveta, tipoTicket, estadoTicket } = u;
  const e = app.estado;
  const T = new Map((e.tickets || []).map(t => [t.numero, t]));
  const tipo = t => tipoTicket(t.tipo).palavra;
  const estado = t => estadoTicket(t).palavra;
  const nomes = l => l.map(x => `${T.get(x)?.titulo || 'ticket'} (${x})`).join(', ');
  const ancestrais = (n, acc = new Set()) => { (T.get(n)?.bloqueado_por || []).forEach(d => { if (T.has(d) && !acc.has(d)) { acc.add(d); ancestrais(d, acc); } }); return acc; };
  const descendentes = (n, acc = new Set()) => { (T.get(n)?.bloqueia || []).forEach(d => { if (T.has(d) && !acc.has(d)) { acc.add(d); descendentes(d, acc); } }); return acc; };
  const feitosAntes = n => [...ancestrais(n)].filter(d => FEITO(T.get(d).estado));
  const esperando = new Set(app.aguardando().map(r => r.ticket));

  const camadas = (e.plano_de_voo?.camadas || []).map(c => c.filter(n => T.has(n)));
  const noPlano = new Set(camadas.flat());
  // a volta de cada ciclo fica fora das camadas e dos fios comuns; é desenhada à parte, pontilhada em tijolo
  const ciclos = e.plano_de_voo?.ciclos || [];
  const ignorada = new Set(ciclos.map(c => (c.aresta_ignorada || []).join('>')));
  const espera = n => (T.get(n).bloqueado_por || []).filter(b => noPlano.has(b) && !ignorada.has(`${n}>${b}`));
  const libera = n => (T.get(n).bloqueia || []).filter(b => noPlano.has(b) && !ignorada.has(`${b}>${n}`));
  // o que de fato prende um ticket (para rótulo, nota, placa e aria): bloqueadores abertos da API, inclusive os do
  // ciclo, e dependências para tickets que não existem. `espera` acima serve só para ordenar e desenhar.
  const bloqueios = n => [...(T.get(n).bloqueios_abertos || [])];
  const inexistentes = n => [...(T.get(n).bloqueios_inexistentes || [])];
  const preso = n => bloqueios(n).length + inexistentes(n).length;
  const esperaEmPalavras = n => [...(bloqueios(n).length ? [nomes(bloqueios(n))] : []), ...inexistentes(n).map(x => `ticket ${x}, que não existe`)].join('; ');
  // à margem: nada aberto os bloqueia e ninguém no caminho espera por eles (só quando há mais de uma camada)
  const margem = camadas.length > 1 ? camadas.slice(0, -1).flat().filter(n => !espera(n).length && !libera(n).length) : [];
  const colunas = camadas.map(c => c.filter(n => !margem.includes(n))).filter(c => c.length);
  const L = colunas.length;
  const R = Math.max(1, ...colunas.map(c => c.length));

  // linhas: cada coluna se alinha às vizinhas (média das linhas de quem bloqueia / de quem espera), sem repetir linha
  const linha = new Map();
  const assentar = (col, desejo) => {
    const usadas = new Set();
    col.map((n, i) => [n, desejo(n, i)]).sort((a, b) => a[1] - b[1]).forEach(([n, d]) => {
      const alvo = Math.min(R - 1, Math.max(0, Math.round(d)));
      for (let k = 0; k < 2 * R; k++) { const r = alvo + (k % 2 ? (k + 1) / 2 : -k / 2); if (r >= 0 && r < R && !usadas.has(r)) { usadas.add(r); linha.set(n, r); break; } }
    });
  };
  const media = (l, i) => l.length ? l.reduce((s, x) => s + linha.get(x), 0) / l.length : i;
  const espalhar = (col, i) => col.length === 1 ? (R - 1) / 2 : i * (R - 1) / (col.length - 1);
  const ida = () => colunas.forEach((col, c) => assentar(col, (n, i) => c === 0 && !linha.has(n) ? espalhar(col, i) : c === 0 ? linha.get(n) : media(espera(n).filter(x => linha.has(x)), espalhar(col, i))));
  ida();

  const nomeColuna = i => i === 0 ? 'Agora' : i === L - 1 ? 'Por fim' : i === 1 ? 'Em seguida' : L > 4 ? `Depois (${i - 1})` : 'Depois';
  const colDestino = L + 2, linhaMargem = R + 2;

  // ---- marcos a lápis
  const marco = (n, extra = {}) => {
    const t = T.get(n), voce = esperando.has(n), aqui = t.estado === 'claimed', inex = inexistentes(n), np = preso(n);
    const est = aqui ? ['andamento', 'em andamento'] : np ? ['relogio', `espera ${np}`] : ['seta', 'pode partir'];
    const dica = [`${tipo(t)} · ${estado(t)}`, np ? `espera por: ${esperaEmPalavras(n)}` : 'nada aberto o bloqueia',
      `${feitosAntes(n).length} feitos vieram antes dele`, voce ? 'uma rodada dele espera a sua resposta' : null,
      inex.length ? `"Blocked by" aponta para ${inex.map(x => `o ticket ${x}`).join(' e ')}, que não existe nos arquivos` : null].filter(Boolean).join('\n');
    return h('button.marco', { type: 'button', class: `marco${aqui ? ' aqui' : ''}${voce ? ' voce' : ''}${extra.margem ? ' na-margem' : ''}`, style: extra.style,
      'aria-label': `${t.titulo}, ticket ${n}, ${estado(t)}${np ? `, espera por ${esperaEmPalavras(n)}` : ', pode partir'}${voce ? ', uma rodada espera você' : ''}`,
      dataset: { t: n, foco: `marco-${n}`, dicaTitulo: t.titulo, dica, dicaSemClique: '1', obstaculo: '1' } },
      aqui ? h('span.selo-aqui', icone('alfinete'), 'estamos aqui') : null,
      voce ? h('span.selo-voce', icone('carimbo'), 'espera você') : null,
      h('span.num', n), h('span.tit', t.titulo),
      extra.margem ? null : h('span.est', icone(est[0]), est[1]),
      inex.length && !extra.margem ? h('span.quebrada', icone('alerta'), `depende de ${inex.join(', ')}, que não existe`) : null);
  };
  const marcos = [];
  colunas.forEach((col, c) => col.forEach(n => marcos.push(marco(n, { style: `grid-column:${c + 2};grid-row:${linha.get(n) + 2}` }))));
  const marcosMargem = margem.map(n => marco(n, { margem: true }));

  // ---- índice a tinta
  const feitos = (e.tickets || []).filter(t => FEITO(t.estado)).sort((a, b) => a.numero.localeCompare(b.numero, 'pt-BR', { numeric: true }));
  const resolvidos = feitos.filter(t => t.estado === 'resolved').length;
  if (!feitos.some(t => t.numero === folhaAtiva)) folhaAtiva = feitos[0]?.numero ?? null;
  const quadrados = feitos.map((t, i) => {
    const lib = (t.bloqueia || []).filter(x => T.has(x));
    return h('button.folha', { type: 'button', class: `folha${t.estado === 'wontfix' ? ' descartada' : ''}`, tabindex: t.numero === folhaAtiva ? '0' : '-1', style: `--i:${i}`,
      'aria-label': `${t.titulo}, ticket ${t.numero}, ${estado(t)}`,
      dataset: { t: t.numero, foco: `folha-${t.numero}`, dicaTitulo: t.titulo, dica: `${tipo(t)} · ${estado(t)}\n${lib.length ? `abriu caminho para: ${nomes(lib)}` : 'ninguém dependia dele'}` } }, t.numero);
  });
  const destaques = feitos.filter(t => t.estado === 'resolved' && (t.bloqueia || []).length)
    .sort((a, b) => b.bloqueia.length - a.bloqueia.length || a.numero.localeCompare(b.numero, 'pt-BR', { numeric: true })).slice(0, 3);
  const conquistas = destaques.map(t => h('li', h('button.conquista', { type: 'button', 'aria-label': `${t.titulo}, ticket ${t.numero}, resolvido; ${t.bloqueia.length} tickets dependiam dele`,
    dataset: { t: t.numero, foco: `conquista-${t.numero}`, dicaTitulo: t.titulo, dica: `abriu caminho para: ${nomes(t.bloqueia.filter(x => T.has(x)))}` } }, icone('tarefa'), h('span', t.titulo))));
  const indice = h('div.indice', { role: 'group', 'aria-label': `já feito: ${resolvidos} tickets resolvidos`, style: `grid-row:2 / ${linhaMargem + 1}`, dataset: { obstaculo: '1' } },
    h('div.total', h('b', String(resolvidos)), h('span', resolvidos === 1 ? 'ticket resolvido' : 'tickets resolvidos')),
    feitos.length ? h('div.folhas', quadrados) : h('p.vazio', 'Nada resolvido ainda.'),
    conquistas.length ? h('div.conquistas', h('div.rot', 'Os que mais abriram caminho:'), h('ul', conquistas)) : null);

  // ---- cartucho do destino
  const d = e.destino || { texto: '', criterios: [] };
  const resumo = (d.texto || '').split(/\s\(|:\s*$|:\s/)[0].trim();
  const cartucho = h('aside.cartucho', { 'aria-label': 'o destino', style: `grid-column:${colDestino};grid-row:2 / ${linhaMargem + 1}`, dataset: { obstaculo: '1' } },
    d.texto && d.texto !== resumo
      ? h('button.rotulo.com-dica', { type: 'button', dataset: { foco: 'destino-texto', dicaTitulo: 'o destino', dica: d.texto } }, icone('bandeira'), 'o destino')
      : h('div.rotulo', icone('bandeira'), 'o destino'),
    h('h3', resumo || 'destino não encontrado no mapa'),
    (d.criterios || []).length ? h('ul.selos', d.criterios.map(c => h('li', h('button.selo', { type: 'button', 'aria-label': `critério ${c.n}: ${c.palavra || c.texto}; aceite final pendente`,
      dataset: { foco: `criterio-${c.n}`, dicaTitulo: `critério ${c.n}${c.palavra ? `: ${c.palavra}` : ''}`, dica: `${c.texto}\naceite final pendente` } },
      h('span.lacre', String(c.n)), h('span', c.palavra || c.texto))))) : null,
    h('div.estado', noPlano.size ? 'Lacre tracejado: aceite final pendente.' : 'Nenhum ticket aberto no caminho.'));

  // ---- montagem
  const fios = svg('svg', { class: 'fios', 'aria-hidden': 'true' },
    svg('defs', {}, ...[['ponta', 'var(--lapis)'], ['ponta-realce', 'var(--ambar)'], ['ponta-madeira', 'var(--madeira)'], ['ponta-tijolo', 'var(--coral)']].map(([id, cor]) =>
      svg('marker', { id, viewBox: '0 0 10 10', refX: '8.5', refY: '5', markerWidth: '8', markerHeight: '8', markerUnits: 'userSpaceOnUse', orient: 'auto' }, svg('path', { d: 'M0 0 L10 5 L0 10 z', style: `fill:${cor}` })))));
  const grade = h('div.caminho', { style: `--colunas:${Math.max(L, 1)};--linhas:${R}` },
    fios,
    h('div.col-cab.feito', { style: 'grid-column:1' }, h('div.nome', 'Já feito'), h('div.escala')),
    colunas.map((_, c) => h('div.col-cab', { class: `col-cab${c === 0 ? ' agora' : ''}`, style: `grid-column:${c + 2}` }, h('div.nome', nomeColuna(c)), h('div.escala'))),
    h('div.col-cab.destino', { style: `grid-column:${colDestino}` }, h('div.nome', 'Destino'), h('div.escala')),
    h('div.fronteira', { 'aria-hidden': 'true', style: `grid-row:1 / ${linhaMargem + 1}` }),
    indice, marcos,
    !L ? h('p.vazio', { style: `grid-column:2 / ${colDestino};grid-row:2` }, 'Nenhum ticket aberto ou em andamento: o caminho está todo a tinta.') : null,
    marcosMargem.length ? h('div.margem', { style: `grid-column:2 / ${colDestino};grid-row:${linhaMargem}` }, h('span.rot', 'À margem do caminho · ninguém espera por eles'), marcosMargem) : null,
    cartucho);

  const legenda = h('div.legenda', { 'aria-hidden': 'true' },
    h('span', h('i.l-tinta'), 'a tinta: feito'), h('span', h('i.l-risco'), 'riscado: descartado'),
    h('span', h('i.l-lapis'), 'a lápis: falta fazer'), h('span', h('i.l-aqui'), 'em andamento'),
    h('span', svg('svg', { viewBox: '0 0 34 12' }, svg('path', { d: 'M1 6 H28', style: 'stroke:var(--lapis);stroke-width:2.2;fill:none' }), svg('path', { d: 'M26 1 L33 6 L26 11 z', style: 'fill:var(--lapis)' })), 'de quem bloqueia para quem espera'));
  const placa = h('div.placa', { hidden: true, 'aria-live': 'polite' });
  const avisosCiclo = ciclos.map(c => h('p.aviso-ciclo', icone('alerta'), `Ciclo de dependência entre ${c.tickets.map(x => T.get(x)?.titulo || `ticket ${x}`).join(' e ')}: um espera o outro. O fio pontilhado mostra a volta; as colunas foram montadas sem ela.`));
  // a leitura do ponto vai para a faixa reservada da casca (#leitura), fora da área que rola: sempre visível, não cobre nada
  const REPOUSO = 'Passe o mouse ou foque um ponto do mapa: a leitura dele aparece aqui, sem cobrir nada.';
  u.repousoDaFaixa(REPOUSO);
  const secao = h('section.cartao.mesa', { 'aria-labelledby': 't-caminho', dataset: { docaDica: '1' } },
    h('div.mesa-cab', h('div', h('h2#t-caminho', 'O caminho até o destino'),
      h('p.h2-sub', 'A tinta é o que já foi feito; o lápis, o que falta. Cada fio sai de quem bloqueia e chega em quem espera. Escolha um ponto para ver a corrente inteira.')),
      rosaDosVentos(svg)),
    h('div.caminho-rolagem', grade), avisosCiclo, legenda, placa);

  // ---- fios (desenhados depois do layout) e realce da corrente
  const todosMarcos = [...marcos, ...marcosMargem];
  const porNum = n => todosMarcos.find(m => m.dataset.t === n);
  const FIOS = [];
  colunas.flat().forEach(n => espera(n).filter(b => porNum(b) && !margem.includes(b)).forEach(b => FIOS.push({ de: b, para: n })));
  const finais = L ? colunas[L - 1].filter(n => !libera(n).length) : [];
  const voltas = ciclos.map(c => ({ de: c.aresta_ignorada[1], para: c.aresta_ignorada[0] })).filter(v => porNum(v.de) && porNum(v.para));
  let fiosFinais = [];

  function desenhar() {
    if (!grade.isConnected) return;
    [...fios.querySelectorAll('path.fio, text.fio-rot')].forEach(x => x.remove());
    const base = grade.getBoundingClientRect();
    const caixa = el => { const r = el.getBoundingClientRect(); return { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height }; };
    const cy = n => { const c = caixa(porNum(n)); return c.y + c.h / 2; };
    const entradas = {}, saidas = {};
    FIOS.forEach(f => { (entradas[f.para] ||= []).push(f); (saidas[f.de] ||= []).push(f); });
    Object.values(entradas).forEach(l => l.sort((a, b) => cy(a.de) - cy(b.de)));
    Object.values(saidas).forEach(l => l.sort((a, b) => cy(a.para) - cy(b.para)));
    const ponta = (lista, f, c) => { const i = lista.indexOf(f), k = lista.length; return c.y + c.h * (k === 1 ? .5 : .28 + .44 * i / (k - 1)); };
    const novo = (dd, classe, marcador) => { const p = svg('path', { d: dd, class: classe, 'marker-end': `url(#${marcador})` }); fios.append(p); return p; };
    const obstaculos = marcos.map(m => ({ t: m.dataset.t, c: caixa(m) }));
    FIOS.forEach(f => {
      const a = caixa(porNum(f.de)), b = caixa(porNum(f.para));
      const x1 = a.x + a.w, y1 = ponta(saidas[f.de], f, a), x2 = b.x - 2, y2 = ponta(entradas[f.para], f, b);
      // um marco no meio do caminho: o fio passa pelo corredor entre as linhas
      const noMeio = obstaculos.filter(o => o.t !== f.de && o.t !== f.para && o.c.x > x1 + 4 && o.c.x + o.c.w < x2 - 4 && Math.max(y1, y2) > o.c.y - 6 && Math.min(y1, y2) < o.c.y + o.c.h + 6).map(o => o.c);
      if (noMeio.length) {
        const acima = Math.min(...noMeio.map(c => c.y)) - 9, abaixo = Math.max(...noMeio.map(c => c.y + c.h)) + 9, meio = (y1 + y2) / 2;
        const yc = Math.abs(abaixo - meio) <= Math.abs(acima - meio) ? abaixo : acima;
        const xa = Math.min(...noMeio.map(c => c.x)) - 4, xb = Math.max(...noMeio.map(c => c.x + c.w)) + 4;
        const g1 = (xa - x1) * .55, g2 = (x2 - xb) * .55;
        f.el = novo(`M${x1} ${y1} C ${x1 + g1} ${y1}, ${xa - g1} ${yc}, ${xa} ${yc} L ${xb} ${yc} C ${xb + g2} ${yc}, ${x2 - g2} ${y2}, ${x2} ${y2}`, 'fio', 'ponta');
      } else {
        const dx = Math.max(18, (x2 - x1) * .5);
        f.el = novo(`M${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`, 'fio', 'ponta');
      }
    });
    // a volta de um ciclo: pontilhada em tijolo, por baixo dos dois marcos
    voltas.forEach(v => {
      const a = caixa(porNum(v.de)), b = caixa(porNum(v.para));
      // sai pela lateral de quem bloqueia e entra pela lateral de quem espera, no vão entre as colunas
      const daDireita = a.x > b.x;
      const x1 = daDireita ? a.x : a.x + a.w, y1 = a.y + a.h * .8, x2 = daDireita ? b.x + b.w + 2 : b.x - 2, y2 = b.y + b.h * .8, dx = daDireita ? -26 : 26;
      v.el = novo(`M${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`, 'fio ciclo', 'ponta-tijolo');
    });
    // quem fecha o caminho chega ao destino: fio de madeira com uma palavra
    const dest = caixa(cartucho);
    fiosFinais = finais.map(n => {
      const c = caixa(porNum(n)), x1 = c.x + c.w, y1 = c.y + c.h / 2, x2 = dest.x - 2, y2 = Math.min(Math.max(y1, dest.y + 30), dest.y + dest.h - 30);
      const el = novo(`M${x1} ${y1} C ${x1 + (x2 - x1) / 2} ${y1}, ${x2 - (x2 - x1) / 2} ${y2}, ${x2} ${y2}`, 'fio fecha', 'ponta-madeira');
      fios.append(svg('text', { class: 'fio-rot', x: (x1 + x2) / 2, y: (y1 + y2) / 2 - 9, 'text-anchor': 'middle' }, 'fecha'));
      return { n, el };
    });
    if (!jaAnimou && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      [...fios.querySelectorAll('path.fio')].forEach((p, i) => {
        const comp = p.getTotalLength(); p.style.strokeDasharray = comp; p.style.setProperty('--comp', comp); p.style.animationDelay = `${450 + i * 90}ms`; p.classList.add('desenhar');
        p.addEventListener('animationend', () => { p.style.strokeDasharray = ''; p.classList.remove('desenhar'); }, { once: true });
      });
    }
    jaAnimou = true;
    if (escolhido) realcar(escolhido); else if (emFoco) realcar(emFoco);
  }

  let emFoco = null;
  function realcar(n) {
    const up = ancestrais(n), down = descendentes(n);
    grade.classList.add('focado');
    todosMarcos.forEach(m => m.classList.toggle('na-corrente', m.dataset.t === n || up.has(m.dataset.t) || down.has(m.dataset.t)));
    quadrados.forEach(q => q.classList.toggle('acesa', up.has(q.dataset.t)));
    FIOS.forEach(f => {
      if (!f.el) return;
      const liga = ((f.para === n || up.has(f.para)) && up.has(f.de)) || ((f.de === n || down.has(f.de)) && down.has(f.para));
      f.el.classList.toggle('na-corrente', liga); f.el.setAttribute('marker-end', `url(#${liga ? 'ponta-realce' : 'ponta'})`);
    });
    fiosFinais.forEach(({ n: m, el }) => el.classList.toggle('na-corrente', m === n || up.has(m) || down.has(m)));
  }
  function soltarRealce() {
    grade.classList.remove('focado', 'so-indice');
    todosMarcos.forEach(m => m.classList.remove('na-corrente'));
    quadrados.forEach(q => q.classList.remove('acesa'));
    FIOS.forEach(f => { if (f.el) { f.el.classList.remove('na-corrente'); f.el.setAttribute('marker-end', 'url(#ponta)'); } });
    fiosFinais.forEach(({ el }) => el.classList.remove('na-corrente'));
  }
  function mostrarPlaca(n) {
    const t = T.get(n), np = preso(n), lib = (t.bloqueia || []).filter(x => T.has(x)), fa = feitosAntes(n);
    placa.replaceChildren(
      h('div', h('div.meta', h('span.chip', { class: `chip ${estadoTicket(t).classe}` }, h('span.n-ticket', n), estado(t)), h('span', tipo(t))),
        h('h3', t.titulo),
        h('div.linhas',
          h('div', h('b', 'Espera por: '), np ? esperaEmPalavras(n) : 'nada aberto; pode andar já', '.'),
          h('div', h('b', 'Quem espera por ele: '), lib.length ? nomes(lib) : 'ninguém', '.'),
          h('div', h('b', 'Feitos antes dele: '), `${fa.length} ${fa.length === 1 ? 'ticket, aceso' : 'tickets, acesos'} no índice à esquerda.`))),
      h('div.acoes',
        h('button.botao.primario', { type: 'button', dataset: { foco: 'placa-abrir' }, onclick: () => abrirGaveta(n) }, 'Abrir o ticket'),
        h('button.botao', { type: 'button', dataset: { foco: 'placa-soltar' }, onclick: () => soltar() }, 'Soltar')));
    placa.hidden = false;
  }
  function escolher(n) {
    escolhido = n;
    todosMarcos.forEach(m => m.classList.toggle('escolhido', m.dataset.t === n));
    realcar(n); mostrarPlaca(n);
  }
  function soltar() {
    const n = escolhido; escolhido = null;
    todosMarcos.forEach(m => m.classList.remove('escolhido'));
    soltarRealce(); placa.hidden = true;
    const m = n && porNum(n); if (m) { window.dispatchEvent(new CustomEvent('torre:dispensar-dica', { detail: m })); m.focus(); }
  }
  soltarAtual = soltar;

  todosMarcos.forEach(m => {
    const n = m.dataset.t;
    const entrar = () => { emFoco = n; if (!escolhido) realcar(n); };
    const sair = () => { emFoco = null; if (!escolhido) soltarRealce(); else realcar(escolhido); };
    m.addEventListener('click', () => escolher(n));
    m.addEventListener('mouseenter', entrar); m.addEventListener('mouseleave', sair);
    m.addEventListener('focus', entrar); m.addEventListener('blur', sair);
  });
  // índice: setas, Home e End andam pelos quadrados (uma parada só no Tab)
  quadrados.forEach((q, i) => q.addEventListener('keydown', ev => {
    const cols = quadrados.filter(x => x.offsetTop === quadrados[0].offsetTop).length || 1;
    const passo = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: cols, ArrowUp: -cols, Home: -i, End: quadrados.length - 1 - i }[ev.key];
    if (passo === undefined) return;
    ev.preventDefault();
    const alvo = quadrados[Math.max(0, Math.min(quadrados.length - 1, i + passo))];
    q.tabIndex = -1; alvo.tabIndex = 0; folhaAtiva = alvo.dataset.t; alvo.focus();
  }));
  // destaques: acendem o próprio quadrado
  indice.querySelectorAll('.conquista').forEach(b => {
    const acender = () => { if (escolhido) return; grade.classList.add('so-indice'); quadrados.forEach(q => q.classList.toggle('acesa', q.dataset.t === b.dataset.t)); };
    const apagar = () => { if (escolhido) return; grade.classList.remove('so-indice'); quadrados.forEach(q => q.classList.remove('acesa')); };
    b.addEventListener('mouseenter', acender); b.addEventListener('mouseleave', apagar); b.addEventListener('focus', acender); b.addEventListener('blur', apagar);
  });

  observador = new ResizeObserver(() => desenhar());
  observador.observe(grade);
  if (document.fonts) document.fonts.ready.then(() => desenhar());
  if (escolhido && noPlano.has(escolhido) && porNum(escolhido)) { todosMarcos.forEach(m => m.classList.toggle('escolhido', m.dataset.t === escolhido)); mostrarPlaca(escolhido); }
  else escolhido = null;
  return secao;
}

function rosaDosVentos(svg) {
  return svg('svg', { class: 'rosa', viewBox: '0 0 46 46', 'aria-hidden': 'true' },
    svg('circle', { cx: 23, cy: 23, r: 20, fill: 'none', style: 'stroke:var(--madeira-clara)', 'stroke-width': 1.5 }),
    svg('circle', { cx: 23, cy: 23, r: 14, fill: 'none', style: 'stroke:var(--linha)', 'stroke-width': 1 }),
    svg('path', { d: 'M23 3 L27 23 L23 43 L19 23 Z', style: 'fill:var(--madeira)' }),
    svg('path', { d: 'M3 23 L23 19 L43 23 L23 27 Z', style: 'fill:var(--madeira-clara)' }),
    svg('path', { d: 'M23 3 L27 23 L23 23 Z', style: 'fill:var(--ambar)' }));
}

// ------------------------------------------------------------------ para responder
function paraResponder(app, u) {
  const { h, icone } = u;
  const e = app.estado;
  const rs = app.aguardando();
  const cs = app.cartasAguardando();
  const nada = !rs.length && !cs.length;
  const malformadas = (e.rodadas || []).filter(r => r.malformada && r.estado === 'aberta');
  const caixa = [...(e.caixa || [])].filter(c => !c.substituida).sort((a, b) => (b.enviada || '').localeCompare(a.enviada || ''));
  const ultima = caixa[0];
  const T = new Map((e.tickets || []).map(t => [t.numero, t]));
  const camadas = e.plano_de_voo?.camadas || [];
  const vivos = (e.tickets || []).filter(t => t.estado === 'claimed').map(t => t.titulo);
  const partem = (camadas[0] || []).filter(n => T.get(n)?.estado === 'open' && !(T.get(n).bloqueios_abertos || []).length && !(T.get(n).bloqueios_inexistentes || []).length).map(n => T.get(n).titulo);
  const lista = l => l.length > 1 ? `${l.slice(0, -1).join(', ')} e ${l[l.length - 1]}` : l[0];
  const AVISO = { pendente: 'o aviso ao maestro ainda não saiu', enviando: 'o aviso ao maestro está saindo', entregue: 'o maestro foi avisado', falhou: 'o aviso ao maestro falhou' };

  const cartas = rs.map(r => h('div.carta-rodada.espera', { dataset: { foco: `rodada-${r.id}` } },
    h('div', h('h3', r.titulo),
      h('div.meta', h('span.chip.e-espera', h('span.n-ticket', r.ticket), r.ticket_titulo || 'ticket não encontrado'),
        h('span', `${r.perguntas.length} ${r.perguntas.length === 1 ? 'pergunta' : 'perguntas'}`), r.aberta ? h('span', `aberta em ${r.aberta}`) : null)),
    h('a.botao.primario', { href: `#/autorizacoes/${r.id}` }, icone('carimbo'), 'Responder')));
  const vereditos = cs.map(c => h('div.carta-rodada.espera', { dataset: { foco: `carta-espera-${c.id}` } },
    h('div', h('h3', c.titulo),
      h('div.meta', h('span.chip.e-espera', 'carta'), h('span', 'espera Aprovar ou Recusar'))),
    h('a.botao.primario', { href: `#/cartas/${encodeURIComponent(c.id)}` }, icone('carimbo'), 'Ver e decidir')));
  const quebradas = malformadas.map(r => h('div.carta-rodada.malformada', { dataset: { foco: `rodada-${r.id}` } },
    h('div', h('h3', r.titulo || r.id), h('div.meta', h('span.c-coral', `malformada: ${r.erro}`), h('span', 'o maestro precisa corrigir o arquivo'))),
    h('a.botao', { href: `#/autorizacoes/${r.id}` }, 'Ver')));
  const proximo = h('p.proximo', h('strong', 'Próximo passo: '),
    rs.length ? `responder ${rs.length === 1 ? 'a rodada acima' : `as ${rs.length} rodadas acima`}. ` : '',
    cs.length ? `Aprovar ou Recusar ${cs.length === 1 ? 'a carta acima' : `as ${cs.length} cartas acima`}. ` : '',
    nada ? 'nada seu. ' : '',
    vivos.length ? `A expedição está em ${lista(vivos)}${partem.length ? `; ${partem.length === 1 ? 'pode partir agora' : 'podem partir agora'}: ${lista(partem)}` : ''}.` : partem.length ? `${partem.length === 1 ? 'Pode partir agora' : 'Podem partir agora'}: ${lista(partem)}.` : '');
  return h('section.cartao', { 'aria-labelledby': 't-responder' },
    h('h2#t-responder', 'Para responder'),
    h('p.h2-sub', nada ? 'Nenhuma pergunta espera você agora.' : 'As cartas da expedição que pedem a sua palavra.'),
    cartas, vereditos, quebradas,
    nada && ultima ? h('div.carta-rodada', h('div', h('h3', ultima.alvo?.titulo || ultima.arquivo),
      h('div.meta', ultima.ticket ? h('span.chip.e-open', h('span.n-ticket', ultima.ticket), T.get(ultima.ticket)?.titulo || 'ticket') : null,
        h('span.chip.e-resolved', `${ultima.tipo === 'resposta' ? 'respondida' : 'enviado'} ${quando(ultima.enviada)}`))),
      ultima.alvo?.tipo === 'rodada' ? h('a.botao', { href: `#/autorizacoes/${ultima.alvo.id}` }, 'Ver a resposta') : null) : null,
    nada && ultima ? h('div.aviso-salvo', { class: `aviso-salvo${ultima.aviso === 'falhou' ? ' falhou' : ''}` }, icone(ultima.aviso === 'falhou' ? 'alerta' : 'tarefa'),
      h('div', h('strong', 'Gravado na caixa. '), `${AVISO[ultima.aviso] || 'aviso ao maestro sem estado'}${ultima.aviso === 'entregue' ? '.' : '; até lá, diga "respondi" no chat.'}`)) : null,
    proximo);
}
function quando(iso) {
  if (!iso) return '';
  const d = new Date(iso); if (isNaN(d)) return iso;
  const hoje = new Date().toDateString() === d.toDateString();
  const hora = d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  return hoje ? `hoje às ${hora}` : `em ${d.toLocaleDateString('pt-BR')} às ${hora}`;
}

// ------------------------------------------------------------------ últimas decisões
function decisoes(app, u) {
  const { h, abrirGaveta, tipoTicket } = u;
  const ds = [...(app.estado.decisoes || [])].slice(-3).reverse();
  const T = new Map((app.estado.tickets || []).map(t => [t.numero, t]));
  const comCodigo = texto => String(texto || '').split(/(`[^`]+`)/).map(p => p.startsWith('`') && p.endsWith('`') && p.length > 2 ? h('code', p.slice(1, -1)) : p);
  return h('section.cartao', { 'aria-labelledby': 't-decisoes' },
    h('h2#t-decisoes', 'Últimas decisões do mapa'),
    ds.length ? h('ul.decisoes', ds.map(d => h('li',
      h('div.quando', `resolvido · ticket ${d.numero}${T.get(d.numero) ? ` · ${tipoTicket(T.get(d.numero).tipo).palavra}` : ''}`),
      h('h3', h('button.link-decisao', { type: 'button', dataset: { foco: `decisao-${d.numero}` }, onclick: () => abrirGaveta(d.numero) }, d.titulo)),
      h('p', comCodigo(d.resumo))))) : h('p.vazio', 'Nenhuma decisão registrada no mapa ainda.'));
}
