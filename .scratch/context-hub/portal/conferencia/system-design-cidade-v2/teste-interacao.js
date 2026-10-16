// Prova de interação, conteúdo, disposição radial e legibilidade da amostra "cidade radial (v2)" do System design.
// Uso: node teste-interacao.js <url-file> <url-pagina-iframe> <pasta-saida>
// Requer puppeteer-core (NODE_PATH) e o Edge instalado. Rede externa bloqueada por --host-resolver-rules.
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const [,, URL_FILE, URL_IFRAME, OUT] = process.argv;
const PLANTA = 'C:/Projetos/context-hub/.scratch/context-hub/amostras/system-design-planta.html';
const REF = 'C:/Projetos/context-hub/.scratch/context-hub/portal/conferencia/system-design-amostra/paridade.json';

/* modelo de referência (planta técnica, paridade 124/124 com o desenho atual) */
function modeloPlanta() {
  const html = fs.readFileSync(PLANTA, 'utf8');
  const pega = nome => { const i = html.indexOf('var ' + nome + ' = ['); const j = html.indexOf('\n];', i); return html.slice(i, j + 3); };
  const src = pega('ROOMS') + pega('CARDS') + pega('EDGES') + '\nreturn {ROOMS:ROOMS, CARDS:CARDS, EDGES:EDGES};';
  return new Function(src)();
}

async function provar(page, ctx, nome, W, H, ref) {
  const r = { contexto: nome, janela: `${W}x${H}`, checagens: {} };
  const ok = (k, v, extra) => { r.checagens[k] = Object.assign({ ok: !!v }, extra || {}); };
  const view = () => ctx.evaluate(() => window.__cidade.view());
  const toScreen = (v, wx, wy) => [v.tx + wx * v.s, v.ty + wy * v.s];
  // ponto clicável de cada prédio/placa (centro do medalhão ou da placa), em coordenadas do mundo
  const alvos = () => ctx.evaluate(() => {
    const o = {};
    document.querySelectorAll('#world .bld').forEach(g => {
      const md = g.querySelector('.md circle'); let b;
      if (md) b = md.getBBox(); else { const rr = g.querySelector('rect:not(.ring)'); b = rr.getBBox(); }
      o[g.getAttribute('data-id')] = [b.x + b.width / 2, b.y + b.height / 2];
    });
    return o;
  });
  const quemEsta = (x, y) => ctx.evaluate((x, y) => { const e = document.elementFromPoint(x, y); const g = e && e.closest('.bld'); return g ? g.getAttribute('data-id') : (e ? e.tagName + (e.id ? '#' + e.id : '') : null); }, x, y);
  const fichaAberta = () => ctx.evaluate(() => { const f = document.getElementById('ficha'); return { aberta: !f.hidden, titulo: (f.querySelector('h2') || {}).textContent || null }; });

  await ctx.evaluate(() => window.__cidade.fit());
  const fitV = await view();

  // 1. sem rolagem do documento
  const sc = await ctx.evaluate(() => ({
    sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
    sh: document.documentElement.scrollHeight, ch: document.documentElement.clientHeight,
    ov: getComputedStyle(document.documentElement).overflow + '/' + getComputedStyle(document.body).overflow
  }));
  ok('sem_rolagem', sc.sw <= sc.cw && sc.sh <= sc.ch, sc);

  // 2. fonte mínima efetiva no enquadrar (todos os <text> do mapa) e fontes carregadas
  const fonte = await ctx.evaluate(() => {
    let min = 1e9, qual = '';
    document.querySelectorAll('#world text').forEach(t => {
      if (!t.textContent.trim() || t.getAttribute('x') === '-9999') return;
      const m = t.getScreenCTM(); const k = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c));
      const fs = parseFloat(getComputedStyle(t).fontSize) * k;
      if (fs < min) { min = fs; qual = t.textContent; }
    });
    const comprimidos = [...document.querySelectorAll('#world text[textLength]')].length;
    const faces = []; document.fonts.forEach(f => faces.push({ familia: f.family, status: f.status }));
    const usada = getComputedStyle(document.querySelector('#world text')).fontFamily;
    const outfit = document.fonts.check('600 19px Outfit');
    return { escala: window.__cidade.view().s, menor_px: +min.toFixed(2), texto: qual, comprimidos, faces, familia_css: usada, outfit_pronta: outfit };
  });
  ok('fonte_minima_14px', fonte.menor_px >= 14 && fonte.comprimidos === 0, { escala: fonte.escala, menor_px: fonte.menor_px, texto: fonte.texto, comprimidos: fonte.comprimidos });
  ok('fontes_carregadas_sem_rede', fonte.faces.length > 0 && fonte.faces.every(f => f.status === 'loaded') && fonte.outfit_pronta, { faces: fonte.faces, familia_css: fonte.familia_css });

  // 3. arrastar com o botão direito anda
  let v0 = await view();
  await page.mouse.move(700, 400);
  await page.mouse.down({ button: 'right' });
  await page.mouse.move(760, 440, { steps: 6 });
  await page.mouse.move(800, 470, { steps: 6 });
  await page.mouse.up({ button: 'right' });
  let v1 = await view();
  ok('direito_anda', Math.abs(v1.tx - v0.tx - 100) < 2 && Math.abs(v1.ty - v0.ty - 70) < 2, { antes: v0, depois: v1 });

  // 4. clique e arraste com o esquerdo no chão vazio: não anda e não abre ficha
  await ctx.evaluate(() => window.__cidade.fit());
  v0 = await view();
  const chao = await ctx.evaluate(() => window.__cidade.chao()); // chão vazio da ilha, longe de prédios e ruas
  const [ex, ey] = toScreen(v0, chao[0], chao[1]);
  const alvoChao = await quemEsta(ex, ey);
  await page.mouse.click(ex, ey);
  const fChao = await fichaAberta();
  await page.mouse.move(ex, ey); await page.mouse.down({ button: 'left' }); await page.mouse.move(ex + 120, ey - 60, { steps: 8 }); await page.mouse.up({ button: 'left' });
  v1 = await view();
  ok('chao_nao_abre_e_esquerdo_nao_anda', !fChao.aberta && v1.tx === v0.tx && v1.ty === v0.ty && v1.s === v0.s, { ponto: [ex, ey], elemento: alvoChao, ficha: fChao, antes: v0, depois: v1 });

  // 5. menu de contexto bloqueado no canvas
  const cm = await ctx.evaluate(() => {
    const ev = new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 600, clientY: 300, button: 2 });
    const alvo = document.elementFromPoint(600, 300) || document.getElementById('stage');
    alvo.dispatchEvent(ev); return { bloqueado: ev.defaultPrevented, alvo: alvo.tagName };
  });
  ok('menu_contexto_bloqueado', cm.bloqueado, cm);

  // 6. Ctrl+roda dá zoom no ponto do cursor
  v0 = await view();
  const px = 640, py = 380;
  const w0 = [(px - v0.tx) / v0.s, (py - v0.ty) / v0.s];
  await page.mouse.move(px, py);
  await page.keyboard.down('Control'); await page.mouse.wheel({ deltaY: -300 }); await page.keyboard.up('Control');
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  const w1 = [(px - v1.tx) / v1.s, (py - v1.ty) / v1.s];
  ok('ctrl_roda_zoom', v1.s > v0.s * 1.3 && Math.abs(w1[0] - w0[0]) < 0.5 && Math.abs(w1[1] - w0[1]) < 0.5, { escala_antes: v0.s, escala_depois: v1.s, ponto_mundo_antes: w0, ponto_mundo_depois: w1 });
  await page.screenshot({ path: path.join(OUT, `${nome}-${W}x${H}-zoom.png`) });

  // 7. ficha alcançável depois do zoom: clica no prédio visível mais perto do centro
  {
    const v = await view(); const A = await alvos(); let melhor = null;
    for (const id in A) { const [sx, sy] = toScreen(v, A[id][0], A[id][1]); if (sx < 40 || sy < 40 || sx > W - 480 || sy > H - 40) continue;
      const d = Math.hypot(sx - W / 2, sy - H / 2); if (!melhor || d < melhor.d) melhor = { id, sx, sy, d }; }
    const q = melhor ? await quemEsta(melhor.sx, melhor.sy) : null;
    if (melhor) await page.mouse.click(melhor.sx, melhor.sy);
    const f = await fichaAberta(); await page.keyboard.press('Escape');
    const esperado = melhor ? await ctx.evaluate(id => window.__cidade.data().cards.find(c => c.id === id).t, melhor.id) : null;
    ok('ficha_depois_do_zoom', melhor && q === melhor.id && f.aberta && f.titulo === esperado, { alvo: melhor && melhor.id, elemento: q, ficha: f });
  }

  // 8. Shift+roda anda na horizontal
  v0 = await view();
  await page.keyboard.down('Shift'); await page.mouse.wheel({ deltaY: 200 }); await page.keyboard.up('Shift');
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  ok('shift_roda_horizontal', v1.tx !== v0.tx && v1.ty === v0.ty && v1.s === v0.s, { antes: v0, depois: v1 });

  // 9. roda sozinha anda na vertical (sem zoom)
  v0 = await view();
  await page.mouse.wheel({ deltaY: 200 });
  await new Promise(r => setTimeout(r, 150));
  v1 = await view();
  ok('roda_vertical', v1.ty !== v0.ty && v1.s === v0.s, { antes: v0, depois: v1 });

  // 10. ficha alcançável depois de andar (pan)
  {
    const v = await view(); const A = await alvos(); let melhor = null;
    for (const id in A) { const [sx, sy] = toScreen(v, A[id][0], A[id][1]); if (sx < 40 || sy < 40 || sx > W - 480 || sy > H - 40) continue;
      const d = Math.hypot(sx - W / 3, sy - H / 2); if (!melhor || d < melhor.d) melhor = { id, sx, sy, d }; }
    if (melhor) await page.mouse.click(melhor.sx, melhor.sy);
    const f = await fichaAberta(); await page.keyboard.press('Escape');
    ok('ficha_depois_de_andar', melhor && f.aberta, { alvo: melhor && melhor.id, ficha: f });
  }

  // 11. tecla 0 e botão enquadrar voltam ao enquadramento
  await page.keyboard.press('0');
  v1 = await view();
  const k0 = Math.abs(v1.s - fitV.s) < 1e-6 && Math.abs(v1.tx - fitV.tx) < .5;
  await page.mouse.move(700, 400); await page.mouse.down({ button: 'right' }); await page.mouse.move(500, 300, { steps: 4 }); await page.mouse.up({ button: 'right' });
  await ctx.click('#fit');
  v1 = await view();
  ok('enquadrar_tecla0_e_botao', k0 && Math.abs(v1.s - fitV.s) < 1e-6 && Math.abs(v1.tx - fitV.tx) < .5, { fit: fitV, depois: v1 });

  // 12. no enquadrar, TODOS os prédios e placas abrem a ficha certa com clique
  {
    const v = await view(); const A = await alvos(); const dados = await ctx.evaluate(() => window.__cidade.data().cards);
    const falhas = [];
    for (const c of dados) {
      const [sx, sy] = toScreen(v, A[c.id][0], A[c.id][1]);
      const q = await quemEsta(sx, sy);
      await page.mouse.click(sx, sy);
      const f = await fichaAberta();
      if (q !== c.id || !f.aberta || f.titulo !== c.t) falhas.push({ id: c.id, elemento: q, ficha: f });
      await page.keyboard.press('Escape');
    }
    ok('todos_os_cliques_abrem_a_ficha_certa', falhas.length === 0, { total: dados.length, falhas });
  }

  // 13. clique num prédio abre a ficha (Sessão) e Esc fecha devolvendo o foco
  {
    const v = await view(); const A = await alvos();
    const [cx, cy] = toScreen(v, A.sessao[0], A.sessao[1]);
    await page.mouse.click(cx, cy);
    const f1 = await ctx.evaluate(() => { const f = document.getElementById('ficha'); return { aberta: !f.hidden, titulo: (f.querySelector('h2') || {}).textContent, texto: f.innerText }; });
    await page.screenshot({ path: path.join(OUT, `${nome}-${W}x${H}-ficha.png`) });
    await page.keyboard.press('Escape');
    const f2 = await ctx.evaluate(() => ({ aberta: !document.getElementById('ficha').hidden, foco: document.activeElement && document.activeElement.getAttribute('data-id') }));
    ok('clique_abre_ficha_esc_fecha_devolve_foco', f1.aberta && f1.titulo === 'Sessão' && !f2.aberta && f2.foco === 'sessao', { ficha: f1, depois_esc: f2 });
  }

  // 14. teclado: Tab foca (anel visível), Enter abre, Esc fecha e devolve o foco; Espaço abre
  {
    await ctx.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.__cidade.fit(); });
    await page.keyboard.press('Tab');
    const foco1 = await ctx.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-id'));
    await page.keyboard.press('Tab');
    const foco2 = await ctx.evaluate(() => { const a = document.activeElement; const ring = a && a.querySelector('.ring'); return { id: a && a.getAttribute('data-id'), anel_opacidade: ring ? getComputedStyle(ring).opacity : null }; });
    await page.keyboard.press('Enter');
    const f3 = await fichaAberta();
    await page.keyboard.press('Escape');
    const f4 = await ctx.evaluate(() => ({ aberta: !document.getElementById('ficha').hidden, foco: document.activeElement && document.activeElement.getAttribute('data-id') }));
    await page.keyboard.press(' ');
    const f5 = await fichaAberta();
    await page.keyboard.press('Escape');
    ok('teclado_tab_enter_espaco_esc', foco1 === 'gustavo' && foco2.id === 'agentes' && +foco2.anel_opacidade === 1 && f3.aberta && f3.titulo === 'Agentes' && !f4.aberta && f4.foco === 'agentes' && f5.aberta && f5.titulo === 'Agentes',
       { primeiro_tab: foco1, segundo_tab: foco2, enter: f3, depois_esc: f4, espaco: f5 });
  }

  // 15. foco em algo fora da vista: a vista anda até ele (zoom alto no canto oposto e Tab até Par 2)
  {
    await ctx.evaluate(() => window.__cidade.fit());
    await page.mouse.move(W - 60, 60); // canto livre do palco (a cartela fica no canto superior esquerdo)
    for (let i = 0; i < 4; i++) { await page.keyboard.down('Control'); await page.mouse.wheel({ deltaY: -300 }); await page.keyboard.up('Control'); }
    const antes = await ctx.evaluate(() => { const v = window.__cidade.view(), b = window.__cidade.boxOf('par2'); return [v.tx + b.x * v.s, v.ty + b.y * v.s]; });
    await new Promise(r => setTimeout(r, 150));
    await ctx.evaluate(() => { const g = document.querySelector('.bld[data-id="sessao"]'); g.focus(); });
    let foco = null, n = 0;
    while (n < 40) { await page.keyboard.press('Tab'); n++; foco = await ctx.evaluate(() => document.activeElement && document.activeElement.getAttribute('data-id')); if (foco === 'par2') break; }
    const vv = await view(); const b = await ctx.evaluate(() => window.__cidade.boxOf('par2'));
    const x1 = vv.tx + b.x * vv.s, y1 = vv.ty + b.y * vv.s, x2 = x1 + b.w * vv.s, y2 = y1 + b.h * vv.s;
    const dentro = x1 >= 0 && y1 >= 0 && x2 <= W && y2 <= H;
    await page.keyboard.press('Enter'); const f = await fichaAberta(); await page.keyboard.press('Escape');
    const foraAntes = antes[0] > W || antes[1] > H || antes[0] < 0 || antes[1] < 0;
    ok('foco_fora_da_vista_anda_ate_ele', foco === 'par2' && foraAntes && dentro && f.titulo === 'Par 2', { foco, canto_antes: antes.map(v => Math.round(v)), caixa_na_tela: [x1, y1, x2, y2].map(v => Math.round(v)), escala: vv.s, ficha: f });
  }

  await ctx.evaluate(() => window.__cidade.fit());
  const sc2 = await ctx.evaluate(() => ({ x: window.scrollX, y: window.scrollY }));
  ok('documento_nao_rolou', sc2.x === 0 && sc2.y === 0, sc2);
  return r;
}

/* fichas de todos os componentes, conferidas contra o modelo de referência */
async function conferirFichas(ctx, M) {
  const res = await ctx.evaluate(() => {
    const out = {};
    window.__cidade.data().cards.forEach(c => {
      window.__cidade.open(c.id);
      const f = document.getElementById('ficha');
      const li = sel => [...f.querySelectorAll(sel + ' li')].map(l => ({ de: l.getAttribute('data-de'), nome: l.querySelector('b').textContent, palavra: (l.querySelector('i') || {}).textContent || '' }));
      out[c.id] = { titulo: f.querySelector('h2').textContent, subs: [...f.querySelectorAll('.sub')].map(s => s.textContent), selo: (f.querySelector('.pill') || {}).textContent || null,
        loc: [...f.querySelectorAll('.loc span')].map(s => s.textContent), chega: li('.ins'), vai: li('.outs') };
      window.__cidade.close();
    });
    return out;
  });
  const roomName = Object.fromEntries(M.ROOMS.map(r => [r.id, r.name]));
  const ROLE = { ext: 'Externo', ent: 'Entrada', con: 'Contrato', srv: 'Serviço', pro: 'Proteção', dad: 'Dados', rede: 'Rede', acv: 'Acervo' };
  const nomeDe = id => id[0] === '@' ? roomName[id.slice(1)] : M.CARDS.find(c => c.id === id).t;
  const falhas = [];
  for (const c of M.CARDS) {
    const f = res[c.id]; if (!f) { falhas.push({ id: c.id, erro: 'sem ficha' }); continue; }
    const esp = { titulo: c.t, subs: c.s || [], selo: c.pill ? c.pill.t : null, papel: ROLE[c.role] };
    const ins = [], outs = [];
    M.EDGES.forEach(e => { const o = e[7] || {}; const lab = e[3] || (o.pair ? 'cada uma empurra' : '');
      if (e[2] === c.id) ins.push(nomeDe(e[1]) + '|' + lab); if (e[1] === c.id) outs.push(nomeDe(e[2]) + '|' + lab);
      if (o.both) { if (e[1] === c.id) ins.push(nomeDe(e[2]) + '|' + lab); if (e[2] === c.id) outs.push(nomeDe(e[1]) + '|' + lab); } });
    const got = { ins: f.chega.map(x => x.nome + '|' + x.palavra).sort(), outs: f.vai.map(x => x.nome + '|' + x.palavra).sort() };
    const erros = [];
    if (f.titulo !== esp.titulo) erros.push('titulo');
    if (JSON.stringify(f.subs) !== JSON.stringify(esp.subs)) erros.push('subtitulos');
    if (f.selo !== esp.selo) erros.push('selo');
    if (!f.loc.includes(esp.papel)) erros.push('papel');
    if (c.kind !== 'rule' && !f.loc.includes(roomName[c.room])) erros.push('bairro');
    if (c.front && !f.loc.includes('fronteira de gravação')) erros.push('fronteira');
    if (JSON.stringify(got.ins) !== JSON.stringify(ins.sort())) erros.push('chega de');
    if (JSON.stringify(got.outs) !== JSON.stringify(outs.sort())) erros.push('vai para');
    if (erros.length) falhas.push({ id: c.id, erros, ficha: f, esperado: { esp, ins, outs } });
  }
  return { total: M.CARDS.length, conferidas: Object.keys(res).length, falhas, fichas: res };
}

/* paridade estrutural: componentes e ligações iguais aos da planta; nenhuma rua sem ligação */
async function paridadeEstrutural(ctx, M) {
  const D = await ctx.evaluate(() => ({ data: window.__cidade.data(), edges: window.__cidade.edges,
    ruas: [...document.querySelectorAll('#edges > g')].map(g => ({ cls: g.getAttribute('class'), id: g.getAttribute('data-id'), de: g.getAttribute('data-from'), para: g.getAttribute('data-to') })),
    soltos: [...document.querySelectorAll('#edges > :not(g.edge)')].length }));
  const comp = [];
  for (const c of M.CARDS) { const n = D.data.cards.find(x => x.id === c.id);
    const a = JSON.stringify([c.room, c.role, c.t, c.s || null, c.pill || null, !!c.front, c.kind || null]);
    const b = n ? JSON.stringify([n.room, n.role, n.t, n.s, n.pill, n.front, n.kind]) : null;
    if (a !== b) comp.push({ id: c.id, planta: a, cidade: b }); }
  const extraComp = D.data.cards.filter(n => !M.CARDS.find(c => c.id === n.id)).map(n => n.id);
  const lig = [];
  for (const e of M.EDGES) { const n = D.edges.find(x => x[0] === e[0]); const o = e[7] || {}, p = n ? (n[5] || {}) : {};
    const a = JSON.stringify([e[1], e[2], e[3], e[4], !!o.both, !!o.pair, !!o.noArrow, !!o.origin]);
    const b = n ? JSON.stringify([n[1], n[2], n[3], n[4], !!p.both, !!p.pair, !!p.noArrow, !!p.origin]) : null;
    if (a !== b) lig.push({ id: e[0], planta: a, cidade: b }); }
  const ruasSemLigacao = D.ruas.filter(r => r.cls !== 'edge' || !M.EDGES.find(e => e[0] === r.id && e[1] === r.de && e[2] === r.para));
  const ligSemRua = M.EDGES.filter(e => !D.ruas.find(r => r.id === e[0])).map(e => e[0]);
  return { componentes: { total_planta: M.CARDS.length, total_cidade: D.data.cards.length, diferentes: comp, a_mais: extraComp },
           ligacoes: { total_planta: M.EDGES.length, total_cidade: D.edges.length, diferentes: lig, sem_rua: ligSemRua },
           ruas: { total: D.ruas.length, sem_ligacao: ruasSemLigacao, elementos_soltos_na_camada_de_ruas: D.soltos } };
}

/* v2: disposição radial, cruzamentos, etiquetas e analogias */
async function provasV2(ctx, M) {
  return await ctx.evaluate(() => {
    const C = window.__cidade, R = C.route;
    // 1) cruzamentos: interseção de segmentos entre todas as ruas desenhadas, fora o túnel (e7);
    //    a rua "Desktop grava?" termina SOBRE a rua "agente no disco?" (entroncamento, como no desenho atual) e não conta como cruzamento
    const ids = Object.keys(R).filter(k => k !== 'e7'), segs = [];
    ids.forEach(id => { const P = R[id].pts; for (let i=0;i<P.length-1;i++) segs.push({id, a:P[i], b:P[i+1]}); });
    function inter(p, q, r, s){ const d = (q[0]-p[0])*(s[1]-r[1]) - (q[1]-p[1])*(s[0]-r[0]); if (Math.abs(d) < 1e-9) return null;
      const t = ((r[0]-p[0])*(s[1]-r[1]) - (r[1]-p[1])*(s[0]-r[0]))/d, u = ((r[0]-p[0])*(q[1]-p[1]) - (r[1]-p[1])*(q[0]-p[0]))/d;
      return (t > 1e-6 && t < 1-1e-6 && u > 1e-6 && u < 1-1e-6) ? [p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])] : null; }
    const cruz = []; let pares = 0;
    for (let i=0;i<segs.length;i++) for (let j=i+1;j<segs.length;j++){ const A = segs[i], B = segs[j]; if (A.id === B.id) continue; pares++;
      if ((A.id === 'e27' && B.id === 'e28') || (A.id === 'e28' && B.id === 'e27')) continue;
      const x = inter(A.a, A.b, B.a, B.b); if (x) cruz.push({ruas:[A.id, B.id], ponto:x.map(v => Math.round(v))}); }
    const tunel = []; R.e7.pts.forEach((p, i, P) => { if (i === P.length-1) return; segs.forEach(s => { const x = inter(p, P[i+1], s.a, s.b); if (x) tunel.push(s.id); }); });
    // 2) níveis: anel normalizado (elipse da vista) de cada prédio; todo nível k+1 fica mais longe do centro que todo nível k
    const rad = C.radial(); const porNivel = {};
    rad.forEach(o => { (porNivel[o.lvl] = porNivel[o.lvl] || []).push(o); });
    const niveis = Object.keys(porNivel).map(Number).sort((a,b)=>a-b).map(l => ({nivel:l, pecas:porNivel[l].map(o => o.id + ' ' + o.anel.toFixed(2)),
      min:Math.min(...porNivel[l].map(o => o.anel)), max:Math.max(...porNivel[l].map(o => o.anel))}));
    const quebras = []; for (let i=0;i<niveis.length-1;i++) if (!(niveis[i].max < niveis[i+1].min)) quebras.push(`nível ${niveis[i].nivel} (máx ${niveis[i].max.toFixed(2)}) >= nível ${niveis[i+1].nivel} (mín ${niveis[i+1].min.toFixed(2)})`);
    // 3) etiqueta mais perto do próprio prédio que de qualquer outro (distância do centro da etiqueta ao contorno de cada prédio)
    const T = C.tags(), H = C.hulls();
    function dPoly(x, y, P){ let best = 1e9; for (let i=0;i<P.length;i++){ const a = P[i], b = P[(i+1)%P.length]; const dx = b[0]-a[0], dy = b[1]-a[1];
      let t = ((x-a[0])*dx + (y-a[1])*dy)/(dx*dx+dy*dy||1); t = Math.max(0, Math.min(1, t)); best = Math.min(best, Math.hypot(x-a[0]-t*dx, y-a[1]-t*dy)); } return best; }
    const etiquetas = Object.keys(T).map(id => { const r = T[id], cx = (r.x+r.x2)/2, cy = (r.y+r.y2)/2; let dono = null, d1 = 1e9, d2 = 1e9;
      Object.keys(H).forEach(h => { const d = dPoly(cx, cy, H[h]); if (d < d1){ d2 = d1; d1 = d; dono = h; } else if (d < d2) d2 = d; });
      return {id, mais_perto:dono, ok:dono === id, dist_dono:+d1.toFixed(1), dist_segundo:+d2.toFixed(1)}; });
    // 4) analogia na ficha
    const analog = C.data().cards.map(c => { C.open(c.id); const p = document.querySelector('#ficha .na-cidade'); const s = p ? p.textContent : ''; C.close();
      return {id:c.id, linha:s, ok:/^Na cidade: .+ — porque .+/.test(s)}; });
    // 5) CouchDB no centro do enquadramento (coordenada do cofre = 0,0 no mundo)
    const B = C.bounds(), centro = {};
    [[1600,900],[1280,800]].forEach(([W, H]) => { const s = Math.min(W/B.w, H/B.h), tx = (W - B.w*s)/2 - B.x*s, ty = (H - B.h*s)/2 - B.y*s;
      centro[W+'x'+H] = {couchdb_px:[+tx.toFixed(1), +ty.toFixed(1)], centro_px:[W/2, H/2], desvio_pct_largura:+((tx - W/2)/W*100).toFixed(2), desvio_pct_altura:+((ty - H/2)/H*100).toFixed(2)}; });
    const v = C.view(), vw = document.getElementById('stage').clientWidth, vh = document.getElementById('stage').clientHeight;
    centro.medido_nesta_janela = {janela:vw+'x'+vh, desvio_pct_largura:+((v.tx - vw/2)/vw*100).toFixed(2), desvio_pct_altura:+((v.ty - vh/2)/vh*100).toFixed(2)};
    return { couchdb_no_centro:centro, cruzamentos:{pares_de_segmentos:pares, total:cruz.length, lista:cruz, tunel_passa_por_baixo_de:[...new Set(tunel)]},
             niveis:{quebras, niveis}, etiquetas:{total:etiquetas.length, fora_do_dono:etiquetas.filter(e => !e.ok), lista:etiquetas},
             analogias:{total:analog.length, sem_linha:analog.filter(a => !a.ok).map(a => a.id), lista:analog} };
  });
}

/* paridade de texto: os 124 textos do atual, achados no mapa, na ficha, no título ou na legenda */
async function paridadeTexto(ctx) {
  const ref = JSON.parse(fs.readFileSync(REF, 'utf8')).textos_atual;
  const camadas = await ctx.evaluate(() => {
    const norm = s => s.replace(/\s+/g, ' ').trim();
    const mapa = [...document.querySelectorAll('#world text')].map(t => norm(t.textContent)).filter(Boolean);
    const titulo = [norm(document.querySelector('#cartela h1').textContent), norm(document.querySelector('#cartela p').textContent), norm(document.querySelector('#cartela .stamp').textContent)];
    const legenda = [norm(document.querySelector('#legenda b').textContent), ...[...document.querySelectorAll('#legList li span')].map(s => norm(s.textContent))];
    const ficha = [];
    window.__cidade.data().cards.forEach(c => { window.__cidade.open(c.id); const f = document.getElementById('ficha');
      ficha.push(norm(f.querySelector('h2').textContent)); f.querySelectorAll('.sub').forEach(s => ficha.push(norm(s.textContent)));
      const p = f.querySelector('.pill'); if (p) ficha.push(norm(p.textContent)); window.__cidade.close(); });
    return { mapa, titulo, legenda, ficha };
  });
  const pool = {}; const origem = {};
  for (const k of ['mapa', 'titulo', 'legenda', 'ficha']) for (const s of camadas[k]) { pool[s] = (pool[s] || 0) + 1; (origem[s] = origem[s] || new Set()).add(k); }
  const need = {}; ref.forEach(s => need[s] = (need[s] || 0) + 1);
  const faltando = []; for (const s in need) if ((pool[s] || 0) < need[s]) faltando.push({ texto: s, no_atual: need[s], na_amostra: pool[s] || 0 });
  const achados = ref.map(s => ({ texto: s, onde: origem[s] ? [...origem[s]] : [] }));
  return { total_atual: ref.length, achados: ref.length - faltando.reduce((a, f) => a + (f.no_atual - f.na_amostra), 0), faltando, onde: achados, camadas };
}

(async () => {
  const M = modeloPlanta();
  const resultado = { gerado: new Date().toISOString(), rodadas: [], erros_js: [], pedidos_externos: [] };
  const browser = await puppeteer.launch({ executablePath: EDGE, headless: 'new',
    args: ['--disable-gpu', '--allow-file-access-from-files', '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1'] });
  const vigiar = (page, rot) => {
    page.on('pageerror', e => resultado.erros_js.push(`${rot}: ${e.message}`));
    page.on('console', m => { if (m.type() === 'error') resultado.erros_js.push(`${rot} console: ${m.text()}`); });
    page.on('request', q => { const u = q.url(); if (!/^(file:|data:|about:|http:\/\/127\.0\.0\.1)/.test(u)) resultado.pedidos_externos.push(`${rot}: ${u}`); });
  };
  try {
    for (const [W, H] of [[1600, 900], [1280, 800]]) {
      // (a) arquivo direto
      let page = await browser.newPage(); vigiar(page, `file ${W}`);
      await page.setViewport({ width: W, height: H });
      await page.goto(URL_FILE, { waitUntil: 'networkidle0' });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 1200));
      await page.screenshot({ path: path.join(OUT, `file-${W}x${H}.png`) });
      if (W === 1600) {
        const est = await paridadeEstrutural(page.mainFrame(), M);
        const fic = await conferirFichas(page.mainFrame(), M);
        const txt = await paridadeTexto(page.mainFrame());
        await page.evaluate(() => window.__cidade.fit());
        const v2 = await provasV2(page.mainFrame(), M);
        fs.writeFileSync(path.join(OUT, 'paridade.json'), JSON.stringify({
          regra: 'v2 (cidade radial). Os 124 textos do desenho atual (lista textos_atual da amostra anterior) contados contra o que a cidade mostra: <text> do mapa, cartela (título, subtítulo, data), legenda e as fichas de todos os componentes (título, subtítulos, selo). Mais a paridade estrutural: componentes com o mesmo bairro, papel, nome, subtítulos e selo; as 30 ligações com a mesma origem, destino, palavra, tipo e sentido; nenhuma rua sem ligação.',
          total_atual: txt.total_atual, achados: txt.achados, faltando: txt.faltando,
          estrutural: est,
          v2_radial: v2,
          fichas: { total: fic.total, conferidas: fic.conferidas, falhas: fic.falhas },
          interface_fora_do_desenho: { botao: 'enquadrar', rotulos_ficha: ['chega de', 'vai para', '×'] },
          onde_cada_texto_aparece: txt.onde, textos_por_camada: txt.camadas, fichas_conteudo: fic.fichas
        }, null, 2));
        resultado.paridade = { texto: `${txt.achados}/${txt.total_atual}`, faltando: txt.faltando.length,
          componentes_diferentes: est.componentes.diferentes.length, ligacoes_diferentes: est.ligacoes.diferentes.length,
          ruas_sem_ligacao: est.ruas.sem_ligacao.length, ligacoes_sem_rua: est.ligacoes.sem_rua.length, fichas_com_falha: fic.falhas.length,
          couchdb_desvio_centro_pct: v2.couchdb_no_centro.medido_nesta_janela, cruzamentos: v2.cruzamentos.total, niveis_quebrados: v2.niveis.quebras.length, etiquetas_fora_do_dono: v2.etiquetas.fora_do_dono.length, fichas_sem_analogia: v2.analogias.sem_linha.length };
      }
      resultado.rodadas.push(await provar(page, page.mainFrame(), 'file', W, H));
      await page.close();

      // (b) dentro de iframe sandbox allow-scripts (origem opaca), servido por http local
      page = await browser.newPage(); vigiar(page, `iframe ${W}`);
      await page.setViewport({ width: W, height: H });
      await page.goto(URL_IFRAME + `#${W}x${H}`, { waitUntil: 'networkidle0' });
      await new Promise(r => setTimeout(r, 1800));
      const frame = page.frames().find(f => f.url().includes('amostras/system-design-cidade-v2.html'));
      await page.screenshot({ path: path.join(OUT, `iframe-${W}x${H}.png`) });
      const sandbox = await page.evaluate(() => document.querySelector('iframe').getAttribute('sandbox'));
      const origem = await frame.evaluate(() => { try { return String(window.origin); } catch (e) { return 'erro'; } });
      const r = await provar(page, frame, 'iframe', W, H);
      r.sandbox = sandbox; r.origem_no_iframe = origem;
      resultado.rodadas.push(r);
      await page.close();
    }
  } finally { await browser.close(); }
  resultado.tudo_ok = resultado.rodadas.every(r => Object.values(r.checagens).every(c => c.ok)) && resultado.erros_js.length === 0 && resultado.pedidos_externos.length === 0
    && resultado.paridade && resultado.paridade.faltando === 0 && resultado.paridade.componentes_diferentes === 0 && resultado.paridade.ligacoes_diferentes === 0
    && resultado.paridade.ruas_sem_ligacao === 0 && resultado.paridade.ligacoes_sem_rua === 0 && resultado.paridade.fichas_com_falha === 0
    && resultado.paridade.cruzamentos === 0 && resultado.paridade.niveis_quebrados === 0 && resultado.paridade.etiquetas_fora_do_dono === 0 && resultado.paridade.fichas_sem_analogia === 0;
  fs.writeFileSync(path.join(OUT, 'resultado-interacao.json'), JSON.stringify(resultado, null, 2));
  const resumo = resultado.rodadas.map(r => `${r.contexto} ${r.janela}: ` + Object.entries(r.checagens).map(([k, c]) => `${k}=${c.ok ? 'ok' : 'FALHA'}`).join(' ')).join('\n');
  console.log(resumo + '\nparidade: ' + JSON.stringify(resultado.paridade) + '\nerros_js: ' + resultado.erros_js.length + ' ' + resultado.erros_js.slice(0, 3).join(' | ') + '\npedidos_externos: ' + resultado.pedidos_externos.length + '\ntudo_ok: ' + resultado.tudo_ok);
})();
