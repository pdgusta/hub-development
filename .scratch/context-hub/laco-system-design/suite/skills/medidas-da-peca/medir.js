// medir.js: mede uma peça HTML/SVG dentro de um iframe da mesma origem e escreve o JSON em <pre id="medidas">.
// Só lê a peça: não clica, não digita, não altera o DOM dela (o único efeito é focar e desfocar cada focável).
// Sem rede além do próprio servidor local; sem dependências.
(function () {
  'use strict';

  const q = new URLSearchParams(location.search);
  const peca = q.get('peca') || '';
  const largura = Math.max(200, parseInt(q.get('largura'), 10) || 1280);
  const altura = Math.max(200, parseInt(q.get('altura'), 10) || 1000);
  const espera = Math.max(0, parseInt(q.get('espera'), 10) || 1500);
  const saida = document.getElementById('medidas');

  function fim(obj) {
    saida.textContent = JSON.stringify(obj, null, 1);
    saida.setAttribute('data-pronto', '1');
  }

  // só caminhos do próprio servidor: "/algo", nunca "//outro-host" nem "http://..."
  if (!/^\/(?!\/)/.test(peca)) {
    fim({ erro: 'parâmetro "peca" ausente ou fora do servidor local; use um caminho que comece com /' });
    return;
  }

  const quadro = document.createElement('iframe');
  quadro.style.width = largura + 'px';
  quadro.style.height = altura + 'px';
  quadro.setAttribute('title', 'peça medida');
  quadro.src = peca;
  quadro.addEventListener('load', function () {
    setTimeout(function () {
      try { fim(medirTudo(quadro)); }
      catch (e) { fim({ erro: String((e && e.stack) || e) }); }
    }, espera);
  });
  document.getElementById('palco').append(quadro);

  // ---------------------------------------------------------------- utilidades

  const FORA = 'defs, marker, symbol, clipPath, mask, pattern, title, desc, metadata';
  const r1 = n => Math.round(n * 10) / 10;
  const r2 = n => Math.round(n * 100) / 100;

  function emFora(el) { return !!(el.closest && el.closest(FORA)); }

  function visivel(el, win) {
    const cs = win.getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse') return false;
    const r = el.getBoundingClientRect();
    if (r.width <= 0 && r.height <= 0) return false;
    let a = el;
    while (a && a.nodeType === 1) {
      if (parseFloat(win.getComputedStyle(a).opacity) === 0) return false;
      a = a.parentElement;
    }
    return true;
  }

  function texto(el) { return (el.textContent || '').replace(/\s+/g, ' ').trim(); }
  function curto(s, n) { s = String(s || ''); n = n || 50; return s.length > n ? s.slice(0, n - 1) + '…' : s; }

  function caixa(el) {
    const r = el.getBoundingClientRect();
    return { x: r1(r.left), y: r1(r.top), w: r1(r.width), h: r1(r.height) };
  }

  // px de tela por unidade do desenho (o SVG encolhe com a largura; os mínimos acompanham)
  function escalaSvg(s) {
    try { const m = s && s.getScreenCTM(); if (m) return Math.hypot(m.a, m.b) || 1; } catch (e) { /* nada */ }
    return 1;
  }

  function raizSvg(el) {
    let s = el.ownerSVGElement || (el.tagName.toLowerCase() === 'svg' ? el : null);
    while (s && s.ownerSVGElement) s = s.ownerSVGElement;
    return s;
  }

  function descrever(el, svgs) {
    const s = raizSvg(el);
    const idx = s ? svgs.indexOf(s) : -1;
    const nome = el.getAttribute('data-ligacao') || el.getAttribute('data-item') || (el.id ? '#' + el.id : '');
    let forma = el.tagName.toLowerCase();
    if (forma === 'path') forma += ' d="' + curto(el.getAttribute('d'), 40) + '"';
    else if (forma === 'line') forma += ' ' + ['x1', 'y1', 'x2', 'y2'].map(k => el.getAttribute(k)).join(',');
    else if (forma === 'rect') forma += ' ' + ['x', 'y', 'width', 'height'].map(k => el.getAttribute(k)).join(',');
    else if (forma === 'circle') forma += ' ' + ['cx', 'cy', 'r'].map(k => el.getAttribute(k)).join(',');
    return (idx >= 0 ? 'svg' + (idx + 1) + ' ' : '') + (nome ? nome + ' ' : '') + forma;
  }

  // ---------------------------------------------------------------- cor e contraste

  function lerCor(s) {
    if (!s || s === 'none' || s === 'transparent') return null;
    let m = s.match(/^rgba?\(([^)]+)\)$/);
    if (m) {
      const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat);
      if (p.length < 3 || p.some(isNaN)) return null;
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    m = s.match(/^#([0-9a-f]{3,8})$/i);
    if (m) {
      let h = m[1];
      if (h.length === 3 || h.length === 4) h = h.split('').map(c => c + c).join('');
      return { r: parseInt(h.slice(0, 2), 16), g: parseInt(h.slice(2, 4), 16), b: parseInt(h.slice(4, 6), 16),
        a: h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1 };
    }
    return undefined; // forma que não sei ler (color(), url(#gradiente) etc.)
  }

  // cima sobre baixo (baixo opaco)
  function compor(cima, baixo) {
    const a = cima.a;
    return { r: cima.r * a + baixo.r * (1 - a), g: cima.g * a + baixo.g * (1 - a), b: cima.b * a + baixo.b * (1 - a), a: 1 };
  }

  function hex(c) {
    return [c.r, c.g, c.b].map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('');
  }

  // mesma conta do contraste/check_contrast.py (tastemaker): limiar 0.03928, pesos 0.2126/0.7152/0.0722,
  // sobre a cor já arredondada para hex de 6 dígitos, como o script recebe.
  function linear(v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
  function luminancia(h) {
    const r = parseInt(h.slice(0, 2), 16), g = parseInt(h.slice(2, 4), 16), b = parseInt(h.slice(4, 6), 16);
    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b);
  }
  function razao(h1, h2) {
    const a = luminancia(h1), b = luminancia(h2);
    return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  }

  function opacidadeEfetiva(el, win) {
    let o = 1, a = el;
    while (a && a.nodeType === 1) { o *= parseFloat(win.getComputedStyle(a).opacity); a = a.parentElement; }
    return o;
  }

  // fundo de um elemento HTML: sobe pelos ancestrais compondo background-color até achar um opaco
  function fundoHtml(el, win) {
    const camadas = [];
    let duvida = null;
    let a = el;
    while (a && a.nodeType === 1) {
      const cs = win.getComputedStyle(a);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !duvida) duvida = 'fundo com imagem ou gradiente em ' + a.tagName.toLowerCase();
      const c = lerCor(cs.backgroundColor);
      if (c && c.a > 0) { camadas.push(c); if (c.a >= 1) break; }
      a = a.parentElement;
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = camadas.length - 1; i >= 0; i--) base = camadas[i].a >= 1 ? camadas[i] : compor(camadas[i], base);
    return { cor: base, duvida };
  }

  // fundo de um <text> SVG: a forma pintada antes dele (ordem do documento) que contém o centro do texto
  function fundoSvg(el, win, formasDoSvg) {
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const camadas = [];
    let duvida = null;
    for (let i = formasDoSvg.length - 1; i >= 0; i--) {
      const f = formasDoSvg[i];
      if (!(f.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) continue; // só o que foi pintado antes
      if (f.contains(el)) continue;
      const cs = win.getComputedStyle(f);
      if (cs.fill === 'none' || cs.display === 'none' || cs.visibility === 'hidden') continue;
      const bb = f.getBoundingClientRect();
      if (cx < bb.left || cx > bb.right || cy < bb.top || cy > bb.bottom) continue;
      let dentro = true;
      try {
        const m = f.getScreenCTM();
        if (m && f.isPointInFill) {
          const p = new DOMPoint(cx, cy).matrixTransform(m.inverse());
          dentro = f.isPointInFill(p);
        }
      } catch (e) { /* fica a caixa como aproximação */ }
      if (!dentro) continue;
      const c = lerCor(cs.fill);
      if (c === undefined) { duvida = duvida || 'fundo com gradiente ou padrão (' + curto(cs.fill, 30) + ')'; continue; }
      if (!c) continue;
      c.a *= parseFloat(cs.fillOpacity || 1) * opacidadeEfetiva(f, win);
      if (c.a <= 0) continue;
      camadas.push(c);
      if (c.a >= 1) break;
    }
    // nada opaco atrás: o fundo é o do próprio <svg> e seus ancestrais HTML
    let base;
    if (!camadas.length || camadas[camadas.length - 1].a < 1) {
      const f = fundoHtml(raizSvg(el), win);
      base = f.cor; duvida = duvida || f.duvida;
    } else base = camadas.pop();
    for (let i = camadas.length - 1; i >= 0; i--) base = compor(camadas[i], base);
    return { cor: base, duvida };
  }

  // ---------------------------------------------------------------- medições

  function medirTudo(ifr) {
    const doc = ifr.contentDocument;
    const win = ifr.contentWindow;
    if (!doc || !win) throw new Error('não consegui ler a peça (outra origem?)');
    const svgs = Array.from(doc.querySelectorAll('svg')).filter(s => !s.ownerSVGElement);

    const marcado = {
      itens: doc.querySelectorAll('[data-item]').length,
      ligacoes: doc.querySelectorAll('[data-ligacao]').length,
      encontros: doc.querySelectorAll('[data-encontro]').length
    };

    const res = {
      peca: peca,
      largura: largura,
      altura_janela: altura,
      quando: new Date().toISOString(),
      marcacao: marcado,
      pagina: {
        largura_documento: doc.documentElement.scrollWidth,
        altura_documento: doc.documentElement.scrollHeight,
        rolagem_horizontal: doc.documentElement.scrollWidth > largura + 1,
        desenhos_svg: svgs.length
      }
    };

    const rot = medirRotulos(doc, win, svgs);
    res.rotulos = rot.resumo;
    res.cruzamentos = medirCruzamentos(doc, win, svgs, marcado);
    res.distancias = medirDistancias(doc, win, svgs, marcado, rot.alturaRotulo);
    res.contraste = medirContraste(doc, win, svgs);
    res.teclado = medirTeclado(doc, win);
    res.peso_e_tempo = medirPeso(win);
    return res;
  }

  // ---- rótulos (R2 e R4)
  const CODIGO_INTERNO = /^(?:[A-Z]{1,2}\d{1,3}|#?\d{1,4})$/; // T2, C3, R18, "#12", "54"

  function medirRotulos(doc, win, svgs) {
    const porSvg = svgs.map((s, i) => {
      const lista = Array.from(s.querySelectorAll('text')).filter(t => !emFora(t) && visivel(t, win) && texto(t));
      return { svg: i + 1, nome: curto(s.getAttribute('aria-label') || '', 60), rotulos: lista.length,
        acima_de_25: lista.length > 25, textos: lista.map(t => texto(t)) };
    });
    const alturas = [];
    svgs.forEach(s => s.querySelectorAll('text').forEach(t => {
      if (!emFora(t) && visivel(t, win) && texto(t)) alturas.push(t.getBoundingClientRect().height);
    }));
    // textos HTML: elementos com texto próprio (nó de texto filho direto)
    const html = [];
    doc.body.querySelectorAll('*').forEach(el => {
      if (el.closest('svg, script, style, noscript, template')) return;
      const proprio = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
      if (!proprio || !visivel(el, win)) return;
      html.push({ el, t: proprio });
    });
    const naPrimeiraTela = el => { const r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < altura && r.right > 0 && r.left < largura; };
    const todosSvg = [];
    porSvg.forEach(p => p.textos.forEach(t => todosSvg.push(t)));
    const unicos = Array.from(new Set(todosSvg.concat(html.map(h => h.t))));
    const codigos = unicos.filter(t => CODIGO_INTERNO.test(t));
    alturas.sort((a, b) => a - b);
    const alturaRotulo = alturas.length ? alturas[Math.floor(alturas.length / 2)] : null;
    let primeiraTela = 0;
    svgs.forEach(s => s.querySelectorAll('text').forEach(t => { if (!emFora(t) && visivel(t, win) && texto(t) && naPrimeiraTela(t)) primeiraTela++; }));
    html.forEach(h => { if (naPrimeiraTela(h.el)) primeiraTela++; });
    return {
      alturaRotulo,
      resumo: {
        nota: 'R2: contar os rótulos do desenho da cidade (por desenho SVG); R4: conferir "unicos" contra o texto do hub',
        por_desenho: porSvg,
        textos_svg: todosSvg.length,
        textos_html: html.length,
        visiveis_na_primeira_tela: primeiraTela,
        altura_rotulo_px: alturaRotulo === null ? null : r1(alturaRotulo),
        possiveis_codigos_soltos: codigos,
        unicos: unicos
      }
    };
  }

  // ---- cruzamentos (R1)
  function amostrar(el) {
    const m = el.getScreenCTM();
    if (!m || !el.getTotalLength) return null;
    let L;
    try { L = el.getTotalLength(); } catch (e) { return null; }
    if (!(L > 0)) return null;
    const escala = Math.hypot(m.a, m.b) || 1;
    const passos = Math.max(2, Math.min(800, Math.ceil(L * escala / 3)));
    const pts = [];
    for (let i = 0; i <= passos; i++) {
      const p = el.getPointAtLength(L * i / passos);
      const q = new DOMPoint(p.x, p.y).matrixTransform(m);
      pts.push([q.x, q.y]);
    }
    return { pts, comprimento: L * escala };
  }

  function cruza(p1, p2, p3, p4) {
    const d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0]);
    if (Math.abs(d) < 1e-9) return null; // paralelos ou colineares: não é cruzamento
    const t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d;
    const u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d;
    if (t < 0 || t > 1 || u < 0 || u > 1) return null;
    return [p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])];
  }

  function ehLigacaoAdivinhada(el, win) {
    const tag = el.tagName.toLowerCase();
    const cs = win.getComputedStyle(el);
    if (cs.stroke === 'none' || !(parseFloat(cs.strokeWidth) > 0) || parseFloat(cs.strokeOpacity) === 0) return false;
    if (tag === 'path' && /[zZ]/.test(el.getAttribute('d') || '')) return false; // contorno fechado é forma, não ligação
    return true;
  }

  function medirCruzamentos(doc, win, svgs, marcado) {
    const adivinhado = marcado.ligacoes === 0;
    const cand = adivinhado
      ? Array.from(doc.querySelectorAll('path, line, polyline')).filter(el => !emFora(el) && visivel(el, win) && ehLigacaoAdivinhada(el, win))
      : Array.from(doc.querySelectorAll('[data-ligacao]')).filter(el => visivel(el, win));
    const encontros = Array.from(doc.querySelectorAll('[data-encontro]')).map(e => e.getBoundingClientRect());
    const lig = [];
    cand.forEach(el => {
      const a = amostrar(el);
      if (!a) return;
      if (adivinhado && a.comprimento < 30 * escalaSvg(raizSvg(el))) return; // traço de ícone (30 unidades do desenho)
      const xs = a.pts.map(p => p[0]), ys = a.pts.map(p => p[1]);
      const sw = parseFloat(win.getComputedStyle(el).strokeWidth) || 1;
      lig.push({ el, pts: a.pts, ini: a.pts[0], fimp: a.pts[a.pts.length - 1], sw,
        curva: el.tagName.toLowerCase() === 'path' && /[CcQqSsTtAa]/.test(el.getAttribute('d') || ''),
        bb: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)] });
    });
    const lista = [];
    let tocamNaPonta = 0, emEncontro = 0;
    for (let i = 0; i < lig.length; i++) {
      for (let j = i + 1; j < lig.length; j++) {
        const A = lig[i], B = lig[j];
        if (A.bb[2] < B.bb[0] || B.bb[2] < A.bb[0] || A.bb[3] < B.bb[1] || B.bb[3] < A.bb[1]) continue;
        const tol = Math.max(6, A.sw, B.sw);
        const pontas = [A.ini, A.fimp, B.ini, B.fimp];
        const achados = [];
        for (let a = 0; a < A.pts.length - 1; a++) {
          for (let b = 0; b < B.pts.length - 1; b++) {
            const x = cruza(A.pts[a], A.pts[a + 1], B.pts[b], B.pts[b + 1]);
            if (!x) continue;
            if (pontas.some(p => Math.hypot(p[0] - x[0], p[1] - x[1]) <= tol)) { tocamNaPonta++; continue; }
            if (encontros.some(r => x[0] >= r.left && x[0] <= r.right && x[1] >= r.top && x[1] <= r.bottom)) { emEncontro++; continue; }
            if (!achados.some(p => Math.hypot(p[0] - x[0], p[1] - x[1]) < 10)) achados.push(x);
          }
        }
        achados.forEach(x => lista.push({
          tipo: (A.curva || B.curva) ? 'suspeita (curva; conferir na captura)' : 'cruzamento',
          a: descrever(A.el, svgs), b: descrever(B.el, svgs), x: r1(x[0]), y: r1(x[1])
        }));
      }
    }
    return {
      modo: adivinhado ? 'adivinhado: traços abertos com contorno visível e 30 unidades do desenho ou mais (sem data-ligacao na peça)' : 'marcado (data-ligacao)',
      ligacoes_medidas: lig.length,
      cruzamentos: lista.filter(c => c.tipo === 'cruzamento').length,
      suspeitas: lista.filter(c => c.tipo !== 'cruzamento').length,
      toques_na_ponta_ignorados: tocamNaPonta,
      em_ponto_de_encontro_ignorados: emEncontro,
      lista: lista
    };
  }

  // ---- distâncias (R3)
  function folga(a, b) {
    const dx = Math.max(0, b.left - a.right, a.left - b.right);
    const dy = Math.max(0, b.top - a.bottom, a.top - b.bottom);
    if (dx === 0 && dy === 0) return 0; // encostados ou sobrepostos
    return dx > 0 && dy > 0 ? Math.hypot(dx, dy) : Math.max(dx, dy);
  }
  function contem(a, b) { return a.left <= b.left + 1 && a.top <= b.top + 1 && a.right >= b.right - 1 && a.bottom >= b.bottom - 1; }
  function area(r) { return r.width * r.height; }

  function medirDistancias(doc, win, svgs, marcado, alturaRotulo) {
    let itens, modo;
    if (marcado.itens > 0) {
      modo = 'marcado (data-item; grupo pelo data-grupo mais próximo)';
      itens = Array.from(doc.querySelectorAll('[data-item]')).filter(el => visivel(el, win)).map(el => {
        const g = el.closest('[data-grupo]');
        return { el, r: el.getBoundingClientRect(), grupo: g ? g.getAttribute('data-grupo') : '(sem grupo)' };
      });
    } else {
      modo = 'adivinhado: formas SVG de 16 unidades do desenho ou mais que não contêm outra forma; grupo = a menor forma que as contém, ou o próprio desenho';
      const formas = [];
      svgs.forEach((s, si) => {
        const rs = s.getBoundingClientRect();
        const minimo = 16 * escalaSvg(s);
        s.querySelectorAll('rect, circle, ellipse, polygon').forEach(el => {
          if (emFora(el) || !visivel(el, win)) return;
          const cs = win.getComputedStyle(el);
          if (cs.fill === 'none' && cs.stroke === 'none') return;
          const r = el.getBoundingClientRect();
          if (r.width < minimo || r.height < minimo) return;
          if (area(r) > 0.4 * area(rs)) return; // fundo do desenho
          // mesma caixa desenhada duas vezes (preenchimento e contorno, por exemplo) conta como um item só
          if (formas.some(f => f.si === si && Math.abs(f.r.left - r.left) < 1 && Math.abs(f.r.top - r.top) < 1 &&
            Math.abs(f.r.right - r.right) < 1 && Math.abs(f.r.bottom - r.bottom) < 1)) return;
          formas.push({ el, r, si });
        });
      });
      const regioes = new Set();
      formas.forEach(a => formas.forEach(b => { if (a !== b && a.si === b.si && area(a.r) > area(b.r) && contem(a.r, b.r)) regioes.add(a); }));
      itens = formas.filter(f => !regioes.has(f)).map(f => {
        let menor = null;
        regioes.forEach(g => { if (g.si === f.si && contem(g.r, f.r) && (!menor || area(g.r) < area(menor.r))) menor = g; });
        return { el: f.el, r: f.r, grupo: menor ? descrever(menor.el, svgs) : 'svg' + (f.si + 1) + ' (desenho inteiro)', si: f.si };
      });
    }
    if (itens.length < 2) return { modo, itens: itens.length, nota: 'menos de dois itens: nada a medir' };

    const pares = [];
    let sobrepostos = 0;
    const vizinho = itens.map(() => ({ d: Infinity, j: -1 }));
    for (let i = 0; i < itens.length; i++) {
      for (let j = i + 1; j < itens.length; j++) {
        if (itens[i].si !== undefined && itens[i].si !== itens[j].si) continue; // modo adivinhado: só dentro do mesmo desenho
        const d = folga(itens[i].r, itens[j].r);
        if (d === 0) sobrepostos++;
        pares.push({ i, j, d });
        if (d < vizinho[i].d) vizinho[i] = { d, j };
        if (d < vizinho[j].d) vizinho[j] = { d, j: i };
      }
    }
    pares.sort((a, b) => a.d - b.d);
    const dentro = [], entre = [];
    vizinho.forEach((v, i) => { if (v.j >= 0 && itens[v.j].grupo === itens[i].grupo) dentro.push(v.d); });
    pares.forEach(p => { if (itens[p.i].grupo !== itens[p.j].grupo) entre.push(p.d); });
    dentro.sort((a, b) => a - b);
    const medDentro = dentro.length ? dentro[Math.floor(dentro.length / 2)] : null;
    const minEntre = entre.length ? Math.min(...entre) : null;
    const minFolga = pares.length ? pares[0].d : null;
    const limiar = alturaRotulo;
    return {
      modo,
      itens: itens.length,
      grupos: Array.from(new Set(itens.map(t => t.grupo))).length,
      altura_rotulo_px: limiar === null ? null : r1(limiar),
      folga_minima_px: minFolga === null ? null : r1(minFolga),
      folga_minima_passa: limiar === null || minFolga === null ? null : minFolga >= limiar,
      pares_abaixo_de_1_rotulo: limiar === null ? null : pares.filter(p => p.d < limiar).length,
      encostados_ou_sobrepostos: sobrepostos,
      dentro_do_grupo_mediana_px: medDentro === null ? null : r1(medDentro),
      entre_grupos_minimo_px: minEntre === null ? null : r1(minEntre),
      razao_entre_sobre_dentro: medDentro && minEntre !== null ? r2(minEntre / medDentro) : null,
      razao_passa: medDentro && minEntre !== null ? minEntre / medDentro >= 1.5 : null,
      menores_folgas: pares.slice(0, 12).map(p => ({ a: descrever(itens[p.i].el, svgs), b: descrever(itens[p.j].el, svgs),
        folga_px: r1(p.d), mesmo_grupo: itens[p.i].grupo === itens[p.j].grupo }))
    };
  }

  // ---- contraste renderizado
  function medirContraste(doc, win, svgs) {
    const formasPorSvg = new Map(svgs.map(s => [s, Array.from(s.querySelectorAll('rect, circle, ellipse, polygon, path, polyline, line')).filter(f => !emFora(f))]));
    const casos = [];
    doc.body.querySelectorAll('*').forEach(el => {
      if (el.closest('script, style, noscript, template')) return;
      const tag = el.tagName.toLowerCase();
      if (el.closest('svg')) {
        if (tag !== 'text' || emFora(el) || !texto(el) || !visivel(el, win)) return;
        casos.push({ el, t: texto(el), svg: true });
      } else {
        const proprio = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
        if (!proprio || !visivel(el, win)) return;
        casos.push({ el, t: proprio, svg: false });
      }
    });
    const falhas = [], duvidas = [];
    let passam = 0;
    casos.forEach(c => {
      const cs = win.getComputedStyle(c.el);
      let cor = lerCor(c.svg ? cs.fill : cs.color);
      if (!cor) { duvidas.push({ texto: curto(c.t), motivo: 'cor do texto ilegível: ' + curto(c.svg ? cs.fill : cs.color, 30) }); return; }
      cor.a *= opacidadeEfetiva(c.el, win) * (c.svg ? parseFloat(cs.fillOpacity || 1) : 1);
      const f = c.svg ? fundoSvg(c.el, win, formasPorSvg.get(raizSvg(c.el)) || []) : fundoHtml(c.el, win);
      const texto6 = hex(cor.a >= 1 ? cor : compor(cor, f.cor));
      const fundo6 = hex(f.cor);
      const px = parseFloat(cs.fontSize);
      const peso = parseInt(cs.fontWeight, 10) || 400;
      const grande = px >= 24 || (px >= 18.66 && peso >= 700);
      const piso = grande ? 3 : 4.5;
      const r = razao(texto6, fundo6);
      const item = { texto: curto(c.t), texto_hex: texto6, fundo_hex: fundo6, razao: r2(r), piso, fonte_px: r1(px), peso };
      if (f.duvida) { item.motivo = f.duvida; duvidas.push(item); }
      else if (r < piso) falhas.push(item);
      else passam++;
    });
    falhas.sort((a, b) => a.razao - b.razao);
    return {
      conta: 'WCAG, igual a contraste/check_contrast.py; piso 4,5 (texto) ou 3 (texto grande: 24 px, ou 18,66 px em negrito)',
      textos: casos.length,
      passam,
      falham: falhas.length,
      nao_verificados: duvidas.length,
      falhas: falhas.slice(0, 60),
      nao_verificados_amostra: duvidas.slice(0, 20)
    };
  }

  // ---- teclado e foco
  const FOCAVEIS = 'a[href], area[href], button, input, select, textarea, summary, iframe, [tabindex], [contenteditable=""], [contenteditable="true"]';

  function nomeAcessivel(el, doc) {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) { const t = lb.split(/\s+/).map(id => { const x = doc.getElementById(id); return x ? texto(x) : ''; }).join(' ').trim(); if (t) return t; }
    const al = (el.getAttribute('aria-label') || '').trim(); if (al) return al;
    if (el.id) { const l = doc.querySelector('label[for="' + CSS.escape(el.id) + '"]'); if (l && texto(l)) return texto(l); }
    const l2 = el.closest('label'); if (l2 && texto(l2)) return texto(l2);
    const tag = el.tagName.toLowerCase();
    if (tag === 'input' && /^(button|submit|reset)$/i.test(el.type) && el.value) return el.value;
    const t = texto(el); if (t) return t;
    const img = el.querySelector('img[alt]'); if (img && img.alt.trim()) return img.alt.trim();
    const ti = el.querySelector && el.querySelector('title'); if (ti && texto(ti)) return texto(ti);
    const tt = (el.getAttribute('title') || '').trim(); if (tt) return tt;
    if (el.placeholder) return el.placeholder;
    return '';
  }

  function aparencia(el, win) {
    const cs = win.getComputedStyle(el);
    return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.backgroundColor, cs.borderColor,
      cs.color, cs.textDecorationLine, cs.stroke, cs.fill, cs.transform].join('|');
  }

  // Regras de CSS com :focus-visible ou :focus que valem para o elemento. O foco dado por script (el.focus) nem sempre
  // aciona :focus-visible; quando há regra assim e a aparência não mudou, o resultado é "não verificado", não falha.
  function regrasDeFoco(doc) {
    const sel = [];
    const varrer = regras => { for (const r of Array.from(regras || [])) {
      if (r.cssRules && !r.selectorText) { varrer(r.cssRules); continue; }
      const t = r.selectorText || '';
      if (/:focus(-visible|-within)?/.test(t)) t.split(',').forEach(x => {
        // o seletor até a pseudo-classe de foco é o elemento que recebe o foco (".bairro:focus-visible .zona" → ".bairro")
        const base = x.split(/:focus(?:-visible|-within)?/)[0].trim().replace(/[\s>+~]+$/, '') || '*';
        sel.push(base);
      });
    } };
    for (const f of Array.from(doc.styleSheets)) { try { varrer(f.cssRules); } catch (e) { /* folha de outra origem */ } }
    return sel;
  }
  function temRegraDeFoco(el, sels) {
    return sels.some(b => { try { return el.matches(b) || !!el.closest(b); } catch (e) { return false; } });
  }

  function medirTeclado(doc, win) {
    const sels = regrasDeFoco(doc);
    const todos = Array.from(doc.querySelectorAll(FOCAVEIS)).filter(el => {
      if (el.disabled) return false;
      if (el.closest('[inert]')) return false;
      return visivel(el, win);
    });
    const fora = todos.filter(el => el.tabIndex < 0);
    const naOrdem = todos.filter(el => el.tabIndex >= 0);
    const positivos = naOrdem.filter(el => el.tabIndex > 0).sort((a, b) => a.tabIndex - b.tabIndex);
    const ordem = positivos.concat(naOrdem.filter(el => el.tabIndex === 0));
    const anterior = doc.activeElement;
    const lista = ordem.map((el, i) => {
      const antes = aparencia(el, win);
      try { el.focus({ preventScroll: true, focusVisible: true }); } catch (e) { el.focus(); }
      const focou = doc.activeElement === el;
      const depois = aparencia(el, win);
      el.blur();
      const nome = nomeAcessivel(el, doc);
      return { ordem: i + 1, elemento: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''), nome: curto(nome, 60),
        sem_nome: !nome, tabindex: el.tabIndex, recebe_foco: focou, muda_ao_focar: focou ? antes !== depois : null,
        regra_de_foco_no_css: temRegraDeFoco(el, sels) };
    });
    if (anterior && anterior.focus) { try { anterior.focus({ preventScroll: true }); } catch (e) { /* nada */ } }
    return {
      nota: 'foco por script (el.focus), que pode não acionar :focus-visible; quem tem regra de foco no CSS e não mudou entra em "nao_verificado_focus_visible" (conferir com Tab real), não em "sem_mudanca_ao_focar"; "muda_ao_focar" compara contorno, sombra, fundo, borda, cor, sublinhado, traço e preenchimento',
      focaveis: lista.length,
      sem_nome: lista.filter(x => x.sem_nome).length,
      tabindex_positivo: positivos.length,
      sem_mudanca_ao_focar: lista.filter(x => x.muda_ao_focar === false && !x.regra_de_foco_no_css).length,
      nao_verificado_focus_visible: lista.filter(x => x.muda_ao_focar === false && x.regra_de_foco_no_css).length,
      fora_da_ordem_tabindex_negativo: fora.length,
      lista: lista.slice(0, 80)
    };
  }

  // ---- peso e tempo
  function tipoDe(nome, iniciador) {
    const ext = (nome.split('?')[0].split('#')[0].match(/\.([a-z0-9]+)$/i) || [])[1] || '';
    const e = ext.toLowerCase();
    if (/^(woff2?|ttf|otf|eot)$/.test(e)) return 'fonte';
    if (/^(png|jpe?g|gif|webp|avif|svg|ico)$/.test(e)) return 'imagem';
    if (e === 'css' || iniciador === 'css' && !e) return 'css';
    if (/^(m?js)$/.test(e) || iniciador === 'script') return 'script';
    if (/^(json|csv|txt|md)$/.test(e) || iniciador === 'fetch' || iniciador === 'xmlhttprequest') return 'dados';
    return iniciador || 'outro';
  }

  function medirPeso(win) {
    const perf = win.performance;
    const nav = perf.getEntriesByType('navigation')[0];
    const recursos = perf.getEntriesByType('resource');
    const porTipo = {};
    const externos = new Set();
    let ocultos = 0;
    const origem = win.location.origin;
    recursos.forEach(r => {
      const t = tipoDe(r.name, r.initiatorType);
      const p = porTipo[t] || (porTipo[t] = { arquivos: 0, bytes_transferidos: 0, bytes_descomprimidos: 0 });
      p.arquivos++;
      p.bytes_transferidos += r.transferSize || 0;
      p.bytes_descomprimidos += r.decodedBodySize || 0;
      let o = '';
      try { o = new URL(r.name).origin; } catch (e) { /* nada */ }
      if (o && o !== origem) externos.add(o);
      if (!r.decodedBodySize) ocultos++;
    });
    const doc = nav ? (nav.decodedBodySize || 0) : 0;
    const total = doc + Object.keys(porTipo).reduce((s, k) => s + porTipo[k].bytes_descomprimidos, 0);
    return {
      nota: 'tempos medidos no Edge sem cabeça com tempo virtual: servem para comparar versões, não como tempo real',
      documento_bytes: doc,
      total_bytes_descomprimidos: total,
      por_tipo: porTipo,
      recursos: recursos.length,
      recursos_sem_tamanho: ocultos,
      origens_externas: Array.from(externos),
      dom_pronto_ms: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
      carga_ms: nav ? Math.round(nav.loadEventEnd) : null
    };
  }
})();
