// Tela do painel da construção. Lê pelo leitor.js e desenha; nunca manda nada para a execução.
// A cada 3 s pede o novo; a cada 1 s remonta o estado e atualiza a tela no lugar (sem refazer o DOM),
// para não perder foco, hover nem a gaveta aberta.
(function () {
  'use strict';
  var L = window.Leitor, $ = function (id) { return document.getElementById(id) };
  var LEITURA_MS = 3000;

  // --- textos em palavras ---
  var SIT = { trabalhando: 'trabalhando', ocioso: 'ocioso', falhou: 'falhou', sem_sinal: 'sem sinal', encerrado: 'encerrado', nao_comecou: 'não começou' };
  var COL = { a_fazer: 'A fazer', bloqueado: 'Bloqueado', em_curso: 'Em curso', esperando: 'Espera você', revisao: 'Em revisão', teste: 'Em teste', feito: 'Feito', desconhecido: 'Desconhecido' };
  // a linha, de cima para baixo; o ramal sai da estação de cima
  var ESTACOES = [['a_fazer'], ['bloqueado', 'ramal'], ['em_curso'], ['esperando', 'ramal'], ['revisao'], ['teste'], ['feito'], ['desconhecido', 'ramal']];
  var EM_LISTA = { em_curso: 1, esperando: 1, revisao: 1, teste: 1 }; // estações com título por extenso
  var TIPO_TXT = { inicio: 'subiu', sinal: 'sinal', pegou_ticket: 'pegou', passou_ticket: 'passou adiante', resolveu_ticket: 'deu por feito',
    devolveu: 'devolveu', esperando_gustavo: 'parou à espera do Gustavo', abriu_subagente: 'abriu subagente', fechou_subagente: 'fechou subagente',
    chamou_fable: 'chamou o Fable', mandou_mensagem: 'mandou mensagem', recebeu_mensagem: 'recebeu mensagem', rodou_teste: 'rodou teste',
    commit: 'commit', passou_1h: 'passou de 1 hora', falhou: 'falhou', fim: 'encerrou' };
  var GRUPOS = [['construtor'], ['revisor', 'prumo'], ['testador', 'integrador']];

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c] }) }
  function dois(n) { return (n < 10 ? '0' : '') + n }
  function hm(ms) { var d = new Date(ms); return dois(d.getHours()) + ':' + dois(d.getMinutes()) }
  function hms(ms) { var d = new Date(ms); return hm(ms) + ':' + dois(d.getSeconds()) }
  function dur(min) { min = Math.max(0, Math.floor(min)); return min < 60 ? min + ' min' : Math.floor(min / 60) + ' h ' + dois(min % 60) }
  function ha(ms, agora) { var m = (agora - ms) / 60000; return m < 1 ? 'agora' : 'há ' + dur(m) }
  function txt(el, s) { if (el.textContent !== s) el.textContent = s }
  function attr(el, k, v) { if (v == null) { if (el.hasAttribute(k)) el.removeAttribute(k) } else if (el.getAttribute(k) !== String(v)) el.setAttribute(k, v) }
  function html(el, s) { if (el.__h !== s) { el.innerHTML = s; el.__h = s } }
  function corPapel(p) { return 'var(--p-' + ({ construtor: 1, revisor: 1, prumo: 1, testador: 1, integrador: 1, maestro: 1 }[p] ? p : 'outro') + ')' }

  // --- ícones (forma + cor; nunca só cor) ---
  function ic(nome, t) {
    t = t || 16; var a = '<svg width="' + t + '" height="' + t + '" viewBox="0 0 16 16" aria-hidden="true" focusable="false">', f = '</svg>';
    switch (nome) {
      case 'trabalhando': return a + '<circle cx="8" cy="8" r="6" fill="#1f5f73"/>' + f;
      case 'ocioso': return a + '<circle cx="8" cy="8" r="5.5" fill="none" stroke="#5a544b" stroke-width="2"/>' + f;
      case 'falhou': return a + '<rect x="1.5" y="1.5" width="13" height="13" rx="2" fill="#9b2a1c"/><path d="M5 5l6 6M11 5l-6 6" stroke="#fff" stroke-width="2" stroke-linecap="round"/>' + f;
      case 'sem_sinal': return a + '<path d="M2 6.5a8.5 8.5 0 0 1 12 0M4.3 9a5.2 5.2 0 0 1 7.4 0" fill="none" stroke="#5a544b" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="2.2 2"/><circle cx="8" cy="12" r="1.6" fill="#5a544b"/><path d="M2.5 14.5l11-13" stroke="#2b2117" stroke-width="1.8" stroke-linecap="round"/>' + f;
      case 'encerrado': return a + '<path d="M3 8.5l3 3 7-7" fill="none" stroke="#5a544b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>' + f;
      case 'nao_comecou': return a + '<circle cx="8" cy="8" r="5.5" fill="none" stroke="#5a544b" stroke-width="1.6" stroke-dasharray="1.6 2.2"/>' + f;
      case 'estourou': return a + '<circle cx="8" cy="8.5" r="6" fill="#fbf6ec" stroke="#9b2a1c" stroke-width="2"/><path d="M8 5v3.8l2.4 1.6" fill="none" stroke="#9b2a1c" stroke-width="1.8" stroke-linecap="round"/><path d="M6 1h4" stroke="#9b2a1c" stroke-width="1.8" stroke-linecap="round"/>' + f;
      case 'esperando': return a + '<path d="M5 14V6.5a1.1 1.1 0 0 1 2.2 0V9V3.6a1.1 1.1 0 0 1 2.2 0V9V4.6a1.1 1.1 0 0 1 2.2 0V10c0 2.5-1.6 4-3.8 4H7.6C6.4 14 5.6 13.3 5 12.3L3.3 9.6a1 1 0 0 1 1.7-1z" fill="#7a4a00"/>' + f;
      case 'fable': return a + '<path d="M8 1.5l2 4.5 4.5 2-4.5 2-2 4.5-2-4.5L1.5 8 6 6z" fill="#8a6a00"/>' + f;
      case 'nada': return a + '<circle cx="8" cy="8" r="7" fill="#3f6b32"/><path d="M4.5 8.2l2.4 2.4 4.6-4.8" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' + f;
      case 'nao_confere': return a + '<rect x="1" y="1" width="14" height="14" rx="3" fill="#fbf6ec" stroke="#5a544b"/><path d="M4 6.5h8M4 9.5h8M10.5 3.5l-5 9" stroke="#2b2117" stroke-width="1.5" stroke-linecap="round"/>' + f;
    }
    return '';
  }
  function anel(min, lim, estourou) {
    var r = 6.5, c = 2 * Math.PI * r, p = min == null ? 0 : Math.min(1, min / lim);
    return '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="' + r + '" fill="none" stroke="#d9cdb8" stroke-width="3"/>' +
      (p ? '<circle cx="9" cy="9" r="' + r + '" fill="none" stroke="' + (estourou ? '#9b2a1c' : '#1f5f73') + '" stroke-width="3" stroke-dasharray="' + (c * p).toFixed(2) + ' ' + c.toFixed(2) + '" transform="rotate(-90 9 9)"/>' : '') + '</svg>';
  }

  // --- estado da página ---
  var acomp, fonte, lido = null, erro = null, lidoEm = null, falhaDesde = null, est = null;
  var relogio = function () { return Date.now() }, modo = 'ao vivo';
  var escolha = null, origem = null, sobre = null; // escolha: {tipo, id}; sobre: id do agente sob o mouse ou foco
  var cartoes = {}, marcas = {}, alertasEl = {}, estacoesEl = {};

  function nome(id) { var a = est && est.agentes.filter(function (x) { return x.id === id })[0]; return a ? a.titulo : (id || '?') }
  function ticket(n) { return est && est.tickets.filter(function (t) { return t.numero === n })[0] }
  function tituloT(n) { var t = ticket(n); return t ? t.titulo : 'ticket ' + n }

  // --- placar ---
  function placar() {
    var agora = est.agora;
    txt($('titulo'), est.titulo); attr($('titulo'), 'title', est.titulo); document.title = est.titulo;
    html($('fases'), est.fases.map(function (f) { return '<li class="' + esc(f.estado) + '">' + (f.estado === 'feita' ? '✓ ' : f.estado === 'em-curso' ? '● ' : '○ ') + esc(f.titulo) + '</li>' }).join(''));
    txt($('p-trab-n'), String(est.trabalhando)); txt($('p-trab-de'), String(est.equipe));
    var prumos = est.agentes.filter(function (a) { return a.papel === 'prumo' && !a.temporario && !a.ehFable && !a.foraDaLista }).length;
    txt($('p-trab-nota'), (est.equipe - prumos) + ' agentes + ' + prumos + ' Prumos; maestro à parte');
    txt($('p-feitos-n'), String(est.feitos)); txt($('p-feitos-de'), String(est.total));
    $('p-feitos-barra').style.width = (est.total ? 100 * est.feitos / est.total : 0).toFixed(1) + '%';
    txt($('p-desde-h'), est.inicio ? hm(est.inicio) : '–');
    txt($('p-desde-ha'), est.terminou ? 'terminou às ' + hm(est.terminou) : est.inicio ? ha(est.inicio, agora) : 'sem hora de início');
  }
  function leitura() {
    var el = $('leitura'), t;
    el.classList.toggle('falha', !!erro); el.classList.toggle('fixa', modo !== 'ao vivo' && !erro);
    if (erro) t = (lidoEm ? 'sem leitura há ' + Math.round((Date.now() - falhaDesde) / 1000) + ' s' : 'não consegui ler') + ': ' + erro;
    else if (!lidoEm) t = 'lendo…';
    else if (modo !== 'ao vivo') t = modo + ' · relógio em ' + hms(relogio());
    else t = 'ao vivo · lido às ' + hms(lidoEm);
    txt($('leitura-txt'), t);
    var b = $('b-problemas'), n = est && est.problemas ? est.problemas.length : 0;
    b.hidden = !n; txt(b, n === 1 ? '1 problema na leitura' : n + ' problemas na leitura');
  }
  function ilegivel(msg) {
    ['p-trab-n', 'p-feitos-n', 'p-desde-h'].forEach(function (id) { txt($(id), 'ilegível') });
    ['p-trab-de', 'p-feitos-de'].forEach(function (id) { txt($(id), '?') });
    var v = $('ilegivel'); v.hidden = !msg; if (msg) txt(v, 'Ilegível: ' + msg + '. O painel não mostra números que não conseguiu ler.');
  }

  // --- alertas ---
  function alertas() {
    var ul = $('alertas-lista'), agora = est.agora, vistos = {};
    if (!est.alertas.length) {
      html(ul, '<li class="calmo">' + ic('nada', 18) + '<span>Nada travado, nada falhou, nada espera você.</span></li>'); alertasEl = {}; return;
    }
    if (ul.querySelector('.calmo')) { ul.innerHTML = ''; ul.__h = null }
    // três ou mais do mesmo tipo viram um chip só (a execução inteira parada não pode empurrar o resto para baixo)
    var porTipo = {}, lista = [];
    est.alertas.forEach(function (al) { (porTipo[al.tipo] = porTipo[al.tipo] || []).push(al) });
    est.alertas.forEach(function (al) {
      var g = porTipo[al.tipo];
      if (g.length < 3) lista.push(al); else if (g[0] === al) lista.push({ tipo: al.tipo, grupo: g });
    });
    lista.forEach(function (al, i) {
      var k = al.grupo ? al.tipo + '|grupo' : al.tipo + '|' + (al.agente || '') + '|' + (al.ticket || ''); vistos[k] = 1;
      var li = alertasEl[k];
      if (!li) {
        li = document.createElement('li'); li.innerHTML = '<button type="button" class="alerta"></button>';
        alertasEl[k] = li;
        li.firstChild.addEventListener('click', function (ev) { if (li.__al.grupo) abrir('alertas', li.__al.tipo, ev.currentTarget); else if (li.__al.tipo === 'esperando') abrir('ticket', li.__al.ticket, ev.currentTarget); else abrir('agente', li.__al.agente, ev.currentTarget) });
      }
      li.__al = al;
      var b = li.firstChild, s;
      b.className = 'alerta ' + al.tipo;
      var tk = al.ticket ? ' · <span class="mono">' + esc(al.ticket) + '</span> ' + esc(tituloT(al.ticket)) : '';
      var QUAL = { falhou: 'Falharam', estourou: 'Passaram de 1 hora', sem_sinal: 'Sem sinal', esperando: 'Esperam você' };
      if (al.grupo) s = ic(al.tipo, 20) + '<span><b>' + QUAL[al.tipo] + '</b> ' + al.grupo.length + (al.tipo === 'esperando' ? ' tickets' : ' agentes') + '</span>';
      else if (al.tipo === 'falhou') s = ic('falhou', 20) + '<span><b>Falhou</b> ' + esc(nome(al.agente)) + tk + '</span>';
      else if (al.tipo === 'estourou') s = ic('estourou', 20) + '<span><b>Passou de 1 hora</b> ' + esc(nome(al.agente)) + ' · ' + dur(al.minutos) + '</span>';
      else if (al.tipo === 'sem_sinal') s = ic('sem_sinal', 20) + '<span><b>Sem sinal ' + ha(al.t, agora) + '</b> ' + esc(nome(al.agente)) + '</span>';
      else s = ic('esperando', 20) + '<span><b>Espera você</b>' + tk + '</span>';
      html(b, s);
      attr(b, 'data-dica', al.grupo ? QUAL[al.tipo] + ': ' + al.grupo.map(function (x) { return al.tipo === 'esperando' ? tituloT(x.ticket) : nome(x.agente) }).join(', ') : al.tipo === 'esperando' ? 'Espera você: ' + tituloT(al.ticket) + (al.texto ? '. ' + al.texto : '') : (al.texto || b.textContent));
      if (ul.children[i] !== li) ul.insertBefore(li, ul.children[i] || null);
    });
    Object.keys(alertasEl).forEach(function (k) { if (!vistos[k]) { alertasEl[k].remove(); delete alertasEl[k] } });
  }

  // --- rede de agentes: cartões numa grade regular; conversas pelas calhas entre eles ---
  var G = { PAD: 14, GV: 20, GH: 26, CH: 108, MH: 46 };
  function rede() {
    var campo = $('rede-campo'), W = campo.clientWidth;
    if (!W) return;
    var cols = W >= 760 ? 5 : W >= 580 ? 4 : W >= 420 ? 3 : 2;
    G.PAD = W < 420 ? 8 : 14; G.GV = W < 420 ? 14 : 20;
    var CH = G.CH, cw = (W - 2 * G.PAD - (cols - 1) * G.GV) / cols;
    var pos = {}, maestros = est.agentes.filter(function (a) { return a.papel === 'maestro' }), resto = est.agentes.filter(function (a) { return a.papel !== 'maestro' });
    var r = 0, c = 0, topo = maestros.length ? G.MH + G.GH : G.GH / 2;
    function y(r) { return topo + r * (CH + G.GH) }
    function x(c) { return G.PAD + c * (cw + G.GV) }
    // cada papel abre fileira; temporários (o Fable), quem está fora da lista e papel sem grupo ocupam as vagas da última
    function avulso(a) { return a.temporario || a.ehFable || a.foraDaLista || !GRUPOS.some(function (g) { return g.indexOf(a.papel) >= 0 }) }
    var grupos = GRUPOS.map(function (g) { return resto.filter(function (a) { return !avulso(a) && g.indexOf(a.papel) >= 0 }) });
    grupos.push(resto.filter(avulso));
    grupos.forEach(function (g, gi) {
      if (!g.length) return;
      if (c && gi < GRUPOS.length) { r++; c = 0 }
      g.forEach(function (a) { if (c === cols) { r++; c = 0 } pos[a.id] = { r: r, c: c, x: x(c), y: y(r), w: cw, h: CH }; c++ });
    });
    var linhas = c ? r + 1 : r;
    maestros.forEach(function (a, i) { pos[a.id] = { r: -1, c: 0, x: G.PAD, y: 0, w: W - 2 * G.PAD, h: G.MH, maestro: true } });
    var altura = y(linhas) - G.GH / 2;
    campo.style.height = altura + 'px';
    var vivos = {};
    est.agentes.forEach(function (a) {
      vivos[a.id] = 1;
      var el = cartoes[a.id];
      if (!el) {
        el = document.createElement('button'); el.type = 'button'; el.className = 'agente';
        el.innerHTML = '<span class="nome"><span></span><span class="sit"></span></span><span class="oque"></span><span class="pe"></span><span class="sinal"></span>';
        el.addEventListener('click', function () { abrir('agente', a.id, el) });
        el.addEventListener('mouseenter', function () { sobre = a.id; realcar() });
        el.addEventListener('mouseleave', function () { if (sobre === a.id) { sobre = null; realcar() } });
        el.addEventListener('focus', function () { sobre = a.id; realcar() });
        el.addEventListener('blur', function () { if (sobre === a.id) { sobre = null; realcar() } });
        campo.appendChild(el); cartoes[a.id] = el;
      }
      var p = pos[a.id];
      el.style.left = p.x + 'px'; el.style.top = p.y + 'px'; el.style.width = p.w + 'px'; el.style.height = p.h + 'px';
      cartao(el, a, !!p.maestro);
    });
    Object.keys(cartoes).forEach(function (id) { if (!vivos[id]) { cartoes[id].remove(); delete cartoes[id] } });
    fios(pos, y, x, W, altura);
    var n = est.recentes.length;
    txt($('legenda-rede'), n ? 'linhas: conversas dos últimos ' + est.conversaMin + ' min (' + n + ')' : 'nenhuma conversa nos últimos ' + est.conversaMin + ' min');
  }

  function cartao(el, a, maestro) {
    var agora = est.agora, lim = est.limites;
    el.className = 'agente ' + a.situacao + (a.estourou ? ' estourou' : '') + (maestro ? ' maestro' : '') + (a.fable.length || a.ehFable ? ' com-fable' : '');
    el.style.setProperty('--cor-papel', corPapel(a.papel));
    attr(el, 'aria-pressed', escolha && escolha.tipo === 'agente' && escolha.id === a.id ? 'true' : 'false');
    var nomeEl = el.firstChild.firstChild, sitEl = el.firstChild.lastChild, oque = el.children[1], pe = el.children[2], sinalEl = el.children[3];
    txt(nomeEl, a.titulo + (maestro ? ' · conduz' : ''));
    html(sitEl, maestro && (a.situacao === 'ocioso' || a.situacao === 'trabalhando') ? '' : ic(a.estourou && a.situacao === 'trabalhando' ? 'estourou' : a.situacao, 16) + (a.fable.length || a.ehFable ? ic('fable', 16) : ''));
    var o;
    if (a.situacao === 'falhou') o = 'falhou' + (a.falha.ticket ? ' no <span class="n">' + esc(a.falha.ticket) + '</span>' + esc(tituloT(a.falha.ticket)) : '');
    else if (a.atual) o = '<span class="n">' + esc(a.atual.ticket) + '</span>' + esc(tituloT(a.atual.ticket));
    else if (maestro) { var m = est.conversas.filter(function (c) { return c.de === a.id }).pop(); o = m ? '→ ' + esc(nome(m.para)) + ': ' + esc(m.assunto) : 'conduz a execução' }
    else o = { ocioso: 'ocioso', encerrado: 'encerrado', nao_comecou: 'ainda não começou', sem_sinal: 'sem ticket' }[a.situacao] || '';
    html(oque, o);
    var lims = lim.subagentes_por_agente, abertos = a.subs.length, pips = '';
    if (!maestro) {
      var nf = abertos - a.fable.length;
      for (var i = 0; i < Math.max(lims, abertos); i++) pips += '<i class="' + (i < nf ? 'on' : i < abertos ? 'fab' : '') + '"></i>';
    }
    // estreito, o cartão não tem largura para "há": "sem sinal 14 min"
    var curto = estreito() && !maestro, quanto = curto && agora - a.ultimo >= 60000 ? dur((agora - a.ultimo) / 60000) : ha(a.ultimo, agora);
    var sinal = a.ultimo == null ? 'sem eventos' : a.situacao === 'sem_sinal' ? 'sem sinal ' + quanto : 'sinal ' + quanto;
    html(pe, maestro ? '' : anel(a.minutos, lim.tentativa_min, a.estourou) + '<span class="min">' + (a.atual ? dur(a.minutos) : '–') + '</span>' +
      (a.foraDaLista ? '<span class="selo">fora da lista</span>' : '') + '<span class="subs">' + pips + '</span>');
    txt(sinalEl, sinal);
    var dica = a.titulo + ': ' + SIT[a.situacao] + (a.atual ? ', ticket ' + a.atual.ticket + ' (' + tituloT(a.atual.ticket) + '), ' + dur(a.minutos) + ' de ' + lim.tentativa_min + ' min' : '') +
      (abertos ? ', ' + abertos + ' subagente' + (abertos > 1 ? 's' : '') + ' aberto' + (abertos > 1 ? 's' : '') : '') + (a.fable.length ? ', com Fable' : '') +
      (a.ultimo ? ', último sinal às ' + hm(a.ultimo) : ', sem eventos');
    attr(el, 'aria-label', dica); attr(el, 'data-dica', dica);
  }

  // caminho com cantos arredondados por uma lista de pontos
  function caminho(p) {
    var d = 'M' + p[0][0].toFixed(1) + ',' + p[0][1].toFixed(1), R = 9;
    for (var i = 1; i < p.length - 1; i++) {
      var a = p[i - 1], b = p[i], c = p[i + 1];
      var l1 = Math.hypot(b[0] - a[0], b[1] - a[1]), l2 = Math.hypot(c[0] - b[0], c[1] - b[1]), r = Math.min(R, l1 / 2, l2 / 2);
      if (!l1 || !l2) continue;
      var p1 = [b[0] - (b[0] - a[0]) / l1 * r, b[1] - (b[1] - a[1]) / l1 * r], p2 = [b[0] + (c[0] - b[0]) / l2 * r, b[1] + (c[1] - b[1]) / l2 * r];
      d += 'L' + p1[0].toFixed(1) + ',' + p1[1].toFixed(1) + 'Q' + b[0].toFixed(1) + ',' + b[1].toFixed(1) + ' ' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1);
    }
    var z = p[p.length - 1]; return d + 'L' + z[0].toFixed(1) + ',' + z[1].toFixed(1);
  }

  function fios(pos, y, x, W, altura) {
    var svg = $('fios'), agora = est.agora;
    svg.setAttribute('width', W); svg.setAttribute('height', altura); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + altura);
    // uma ligação por par, com quantas conversas e a última hora
    var pares = {};
    est.recentes.forEach(function (m) {
      if (!pos[m.de] || !pos[m.para] || m.de === m.para) return;
      var k = [m.de, m.para].sort().join('|'), p = pares[k] || (pares[k] = { a: m.de, b: m.para, n: 0, t: 0 });
      p.n++; p.t = Math.max(p.t, m.t);
    });
    // de cima para baixo: a = o de cima
    var lista = Object.keys(pares).map(function (k) {
      var p = pares[k], A = pos[p.a], B = pos[p.b];
      if (A.r > B.r || (A.r === B.r && A.c > B.c)) { var t = p.a; p.a = p.b; p.b = t }
      return p;
    });
    // portas: cada cartão reparte a borda entre as suas ligações, na ordem de onde vem a outra ponta
    var portas = {};
    function porta(id, borda, outroX, chave) { var k = id + '|' + borda; (portas[k] = portas[k] || []).push({ x: outroX, chave: chave }) }
    lista.forEach(function (p, i) {
      var A = pos[p.a], B = pos[p.b];
      p.mesma = A.r === B.r;
      porta(p.a, p.mesma ? 'cima' : 'baixo', B.x + B.w / 2, i); porta(p.b, 'cima', A.x + A.w / 2, i);
    });
    var px = {};
    Object.keys(portas).forEach(function (k) {
      var id = k.split('|')[0], P = pos[id], l = portas[k].sort(function (u, v) { return u.x - v.x });
      l.forEach(function (q, j) { px[k + '|' + q.chave] = P.maestro ? null : P.x + P.w * (0.2 + 0.6 * (j + 0.5) / l.length) });
    });
    var faixas = {};
    function raia(k) { var n = faixas[k] = (faixas[k] || 0) + 1; return ((n - 1) % 5 - 2) * 4 }
    var d = '';
    lista.forEach(function (p, i) {
      var A = pos[p.a], B = pos[p.b], pts;
      var xb = px[p.b + '|cima|' + i], yB = B.y;
      if (p.mesma) {
        var xa = px[p.a + '|cima|' + i], yg = A.y - G.GH / 2 + raia('h' + A.r);
        pts = [[xa, A.y], [xa, yg], [xb, yg], [xb, yB]];
      } else {
        var vx = x(B.c) - G.GV / 2 + raia('v' + B.c), g1 = A.y + A.h + G.GH / 2 + raia('h' + (A.r + 1));
        var xa2 = A.maestro ? (B.r === A.r + 1 ? xb : vx) : px[p.a + '|baixo|' + i];
        if (B.r === A.r + 1) pts = [[xa2, A.y + A.h], [xa2, g1], [xb, g1], [xb, yB]];
        else { var g2 = B.y - G.GH / 2 + raia('h' + B.r); pts = [[xa2, A.y + A.h], [xa2, g1], [vx, g1], [vx, g2], [xb, g2], [xb, yB]] }
      }
      var w = (1.6 + Math.min(p.n - 1, 3) * 0.9).toFixed(1), novo = agora - p.t < 2 * 60000;
      d += '<path class="fio' + (novo ? ' novo' : '') + '" data-a="' + esc(p.a) + '" data-b="' + esc(p.b) + '" stroke-width="' + w + '" d="' + caminho(pts) + '"/>';
      d += '<circle class="fio porta" data-a="' + esc(p.a) + '" data-b="' + esc(p.b) + '" r="3" cx="' + pts[0][0].toFixed(1) + '" cy="' + pts[0][1].toFixed(1) + '"/>';
      var z = pts[pts.length - 1];
      d += '<circle class="fio porta" data-a="' + esc(p.a) + '" data-b="' + esc(p.b) + '" r="3" cx="' + z[0].toFixed(1) + '" cy="' + z[1].toFixed(1) + '"/>';
    });
    html(svg, d);
    realcar();
  }
  function realcar() {
    var id = sobre || (escolha && escolha.tipo === 'agente' ? escolha.id : null), campo = $('rede-campo');
    campo.classList.toggle('com-foco', !!id);
    Array.prototype.forEach.call($('fios').children, function (f) { f.classList.toggle('realce', !!id && (f.getAttribute('data-a') === id || f.getAttribute('data-b') === id)) });
    // o ticket do agente sob o foco acende na linha
    var a = id && est && est.agentes.filter(function (x) { return x.id === id })[0], tk = a && a.atual ? a.atual.ticket : null;
    Object.keys(marcas).forEach(function (n) { marcas[n].classList.toggle('realce', n === tk) });
  }

  // --- linha dos tickets ---
  function metro() {
    var ol = $('linha'), agora = est.agora;
    ESTACOES.forEach(function (e, i) {
      var col = e[0], li = estacoesEl[col];
      var dela = est.tickets.filter(function (t) { return t.coluna === col });
      if (col === 'desconhecido' && !dela.length) { if (li) { li.remove(); delete estacoesEl[col] } return }
      if (!li) {
        li = document.createElement('li'); li.className = 'estacao' + (e[1] ? ' ramal' : ''); li.setAttribute('data-col', col);
        li.innerHTML = '<span class="trilho" aria-hidden="true"></span><div class="est-cab"><span class="nome"></span><span class="n"></span><span class="extra"></span></div><div class="marcas"></div>';
        estacoesEl[col] = li;
      }
      if (ol.children[i] !== li) ol.insertBefore(li, ol.children[i] || null);
      var cab = li.children[1], caixa = li.children[2], lista = !!EM_LISTA[col];
      var descartados = dela.filter(function (t) { return t.base === 'descartado' }).length;
      txt(cab.children[0], COL[col]); txt(cab.children[1], String(dela.length - descartados));
      txt(cab.children[2], descartados ? '+ ' + descartados + ' descartado' + (descartados > 1 ? 's' : '') + ', fora da conta' : '');
      caixa.className = 'marcas' + (lista ? ' lista' : '');
      li.className = 'estacao' + (e[1] ? ' ramal' : '') + (lista ? '' : ' curta');
      dela.forEach(function (t, j) {
        var b = marcas[t.numero];
        if (!b) {
          b = document.createElement('button'); b.type = 'button'; b.className = 'tk';
          b.addEventListener('click', function () { abrir('ticket', t.numero, b) });
          marcas[t.numero] = b;
        }
        b.__vivo = true;
        tk(b, t, lista, agora);
        if (caixa.children[j] !== b) { var f = document.activeElement === b; caixa.insertBefore(b, caixa.children[j] || null); if (f) b.focus({ preventScroll: true }) }
      });
    });
    Object.keys(marcas).forEach(function (n) { if (!marcas[n].__vivo) { marcas[n].remove(); delete marcas[n] } else marcas[n].__vivo = false });
  }
  function tk(b, t, lista, agora) {
    b.className = 'tk' + (t.base === 'descartado' ? ' descartado' : '') + (t.relogio && t.relogio.estourou ? ' estourou' : '') + (t.falhou.length ? ' falhou' : '') + (b.classList.contains('realce') ? ' realce' : '');
    attr(b, 'aria-pressed', escolha && escolha.tipo === 'ticket' && escolha.id === t.numero ? 'true' : 'false');
    var sobre = (t.triagem ? '<span class="triagem" title="falta triagem">?</span>' : '') + (t.falhou.length ? ic('falhou', 14) : '') + (t.relogio && t.relogio.estourou ? ic('estourou', 14) : '') + (t.naoConfere ? ic('nao_confere', 14) : '');
    var s = '<span class="n">' + esc(t.numero) + '</span>';
    if (lista) {
      s += '<span class="tt">' + esc(t.titulo) + '</span>' + (sobre ? '<span class="sobre">' + sobre + '</span>' : '') +
        (t.relogio ? '<span class="min">' + dur(t.relogio.minutos) + '</span>' : '');
    } else if (sobre) s += '<span class="sobre">' + sobre + '</span>';
    html(b, s);
    var dica = 'Ticket ' + t.numero + ': ' + t.titulo + ' · ' + (t.base === 'descartado' ? 'descartado' : COL[t.coluna]) +
      (t.coluna === 'bloqueado' ? ', espera ' + t.abertos.map(function (n) { return n + (ticket(n) ? '' : ' (não existe)') }).join(', ') : '') +
      (t.relogio ? ', com ' + nome(t.relogio.agente) + ' há ' + dur(t.relogio.minutos) : '') +
      (t.falhou.length ? ', falhou' : '') + (t.relogio && t.relogio.estourou ? ', passou de 1 hora' : '') + (t.naoConfere ? ', "Com:" não confere com quem pegou' : '') + (t.triagem ? ', falta triagem' : '');
    attr(b, 'aria-label', dica); attr(b, 'data-dica', dica);
  }

  // --- gaveta de detalhe ---
  function abrir(tipo, id, de) {
    var era = escolha; escolha = { tipo: tipo, id: id };
    if (!era) origem = de || document.activeElement;
    else if (de) origem = de;
    $('gaveta').hidden = false; $('g-corpo').__h = null; $('g-corpo').scrollTop = 0;
    desenhar();
    $('g-titulo').focus({ preventScroll: true });
    estreito() ? $('gaveta').setAttribute('aria-modal', 'true') : $('gaveta').removeAttribute('aria-modal');
  }
  function fechar() {
    escolha = null; $('gaveta').hidden = true; desenhar();
    if (origem && document.contains(origem)) origem.focus({ preventScroll: true });
    origem = null;
  }
  function estreito() { return window.matchMedia('(max-width:760px)').matches }
  function chipT(n) { var t = ticket(n); return '<button type="button" class="tk" data-abre="ticket:' + esc(n) + '"><span class="n">' + esc(n) + '</span><span class="tt">' + esc(t ? t.titulo : 'não existe') + '</span></button>' }
  function chipA(id) { return '<button type="button" class="tk" data-abre="agente:' + esc(id) + '">' + esc(nome(id)) + '</button>' }
  function evTxt(e) {
    var s = TIPO_TXT[e.tipo] || e.tipo;
    if (e.ticket && e.tipo !== 'mandou_mensagem') s += ' ' + e.ticket;
    if (e.para) s += ' → ' + nome(e.para);
    if (e.tipo === 'rodou_teste' || e.tipo === 'commit' || e.tipo === 'fechou_subagente') s += e.ok === false ? ' (falhou)' : e.ok ? ' (ok)' : '';
    if (e.assunto) s += ': ' + e.assunto; else if (e.detalhe) s += ': ' + e.detalhe;
    return s;
  }
  function gaveta() {
    var g = $('gaveta'); if (!escolha || !est || est.ilegivel) { g.hidden = true; return }
    var agora = est.agora, corpo = '', titulo = '', marca = '';
    if (escolha.tipo === 'agente') {
      var a = est.agentes.filter(function (x) { return x.id === escolha.id })[0];
      if (!a) { titulo = escolha.id; corpo = '<p class="vazio-g">Este agente não está mais na leitura.</p>' } else {
        titulo = a.titulo; marca = ic(a.situacao, 22);
        corpo += '<dl><dt>Situação</dt><dd>' + esc(SIT[a.situacao]) + (a.estourou ? ', passou de 1 hora' : '') + '</dd>' +
          '<dt>Papel</dt><dd>' + esc(a.papel || '?') + (a.foraDaLista ? ' (fora da lista)' : '') + '</dd>' +
          '<dt>Modelo</dt><dd>' + esc((a.modelo || a.iniciouModelo || '?') + (a.esforco ? ', esforço ' + a.esforco : '')) + '</dd>' +
          '<dt>Último sinal</dt><dd>' + (a.ultimo ? hms(a.ultimo) + ' (' + ha(a.ultimo, agora) + ')' : 'nenhum') + '</dd>' +
          (a.terminal ? '<dt>Terminal</dt><dd>' + esc(a.terminal) + '</dd>' : '') + '</dl>';
        if (a.falha) corpo += '<div class="det">' + ic('falhou', 14) + ' Falhou às ' + hm(a.falha.t) + (a.falha.detalhe ? ': ' + esc(a.falha.detalhe) : '') + '</div>';
        corpo += '<h3>Agora</h3>' + (a.atual ? '<div class="chips">' + chipT(a.atual.ticket) + '</div><p class="g-sub">' + anel(a.minutos, est.limites.tentativa_min, a.estourou) + ' ' + dur(a.minutos) + ' de ' + est.limites.tentativa_min + ' min · tentativa ' + a.atual.tentativa + ' · desde ' + hm(a.atual.desde) + '</p>' : '<p class="vazio-g">sem ticket</p>');
        corpo += '<h3>Subagentes (' + a.subs.length + ' de ' + est.limites.subagentes_por_agente + ')</h3>' + (a.subs.length ? '<ul>' + a.subs.map(function (s) { return '<li><span class="h">' + hm(s.desde) + '</span><span>' + (s.modelo && s.modelo.indexOf('claude-fable') === 0 ? ic('fable', 14) + ' Fable: ' : '') + esc(s.assunto || s.id) + '</span></li>' }).join('') + '</ul>' : '<p class="vazio-g">nenhum aberto</p>');
        var conv = est.conversas.filter(function (c) { return c.de === a.id || c.para === a.id }).slice(-12).reverse();
        corpo += '<h3>Conversas</h3>' + (conv.length ? '<ul>' + conv.map(function (c) { return '<li><span class="h">' + hm(c.t) + '</span><span>' + (c.de === a.id ? '→ ' + esc(nome(c.para)) : '← ' + esc(nome(c.de))) + ': ' + esc(c.assunto || '') + '</span></li>' }).join('') + '</ul>' : '<p class="vazio-g">nenhuma</p>');
        corpo += '<p class="g-sub">' + a.testes.ok + ' testes ok, ' + a.testes.falha + ' com falha · ' + a.commits + ' commits</p>';
        corpo += '<h3>Últimos eventos</h3><ul>' + a.eventos.filter(function (e) { return e.tipo !== 'sinal' }).slice(-15).reverse().map(function (e) { return '<li><span class="h">' + hm(e.t) + '</span><span>' + esc(evTxt(e)) + '</span></li>' }).join('') + '</ul>';
      }
    } else if (escolha.tipo === 'ticket') {
      var t = ticket(escolha.id);
      if (!t) { titulo = 'Ticket ' + escolha.id; corpo = '<p class="vazio-g">Este ticket não está mais na leitura.</p>' } else {
        titulo = t.titulo; marca = '<span class="tk' + (t.base === 'descartado' ? ' descartado' : '') + '" aria-hidden="true"><span class="n">' + esc(t.numero) + '</span></span>';
        corpo += '<dl><dt>Etapa</dt><dd>' + esc(t.base === 'descartado' ? 'Descartado' : COL[t.coluna]) + ' <span class="g-sub">(Status: ' + esc(t.statusCru || 'vazio') + ')</span></dd>' +
          '<dt>Dono</dt><dd>' + esc(t.dono || '–') + '</dd><dt>Com</dt><dd>' + (t.com ? chipA(t.com) : '–') + (t.naoConfere ? ' ' + ic('nao_confere', 14) + ' não confere com quem pegou' : '') + '</dd>' +
          '<dt>Tentativas</dt><dd>' + t.tentativas + '</dd></dl>';
        if (t.coluna === 'esperando') {
          var det = est.alertas.filter(function (x) { return x.tipo === 'esperando' && x.ticket === t.numero })[0];
          corpo += '<div class="det voce">' + ic('esperando', 14) + ' Espera você' + (det && det.texto ? ': ' + esc(det.texto) : '') + '</div>';
        }
        if (t.falhou.length) corpo += '<div class="det">' + ic('falhou', 14) + ' Falhou com ' + esc(t.falhou.map(nome).join(', ')) + '</div>';
        if (t.relogio) corpo += '<h3>Agora</h3><div class="chips">' + chipA(t.relogio.agente) + '</div><p class="g-sub">' + anel(t.relogio.minutos, est.limites.tentativa_min, t.relogio.estourou) + ' ' + dur(t.relogio.minutos) + ' de ' + est.limites.tentativa_min + ' min · tentativa ' + t.relogio.tentativa + '</p>';
        corpo += '<h3>Bloqueado por</h3>' + (t.blocked_by.length ? '<div class="chips">' + t.blocked_by.map(chipT).join('') + '</div>' : '<p class="vazio-g">nada</p>');
        corpo += '<h3>Bloqueia</h3>' + (t.bloqueia.length ? '<div class="chips">' + t.bloqueia.map(chipT).join('') + '</div>' : '<p class="vazio-g">nada</p>');
        var evs = [];
        est.agentes.forEach(function (a) { a.eventos.forEach(function (e) { if (e.ticket === t.numero && e.tipo !== 'sinal') evs.push({ e: e, a: a.id }) }) });
        evs.sort(function (u, v) { return v.e.t - u.e.t });
        corpo += '<h3>Eventos do ticket</h3>' + (evs.length ? '<ul>' + evs.slice(0, 15).map(function (x) { return '<li><span class="h">' + hm(x.e.t) + '</span><span>' + esc(nome(x.a)) + ' ' + esc(evTxt(x.e)) + '</span></li>' }).join('') + '</ul>' : '<p class="vazio-g">nenhum</p>');
      }
    } else if (escolha.tipo === 'alertas') {
      var QUAL2 = { falhou: 'Falharam', estourou: 'Passaram de 1 hora', sem_sinal: 'Sem sinal', esperando: 'Esperam você' };
      var g2 = est.alertas.filter(function (x) { return x.tipo === escolha.id });
      titulo = QUAL2[escolha.id] + ' (' + g2.length + ')'; marca = ic(escolha.id, 22);
      corpo = g2.length ? '<div class="chips">' + g2.map(function (x) { return escolha.id === 'esperando' ? chipT(x.ticket) : chipA(x.agente) }).join('') + '</div>' : '<p class="vazio-g">nenhum agora</p>';
    } else {
      titulo = 'Problemas na leitura';
      corpo = est.problemas.length ? '<ul>' + est.problemas.map(function (p) { return '<li><span class="h mono">' + esc(p.arquivo || '') + '</span><span>' + esc(p.mensagem || p.erro) + '</span></li>' }).join('') + '</ul>' : '<p class="vazio-g">nenhum</p>';
    }
    txt($('g-titulo'), titulo); html($('g-marca'), marca);
    var c = $('g-corpo'), foco = document.activeElement && c.contains(document.activeElement) ? document.activeElement.getAttribute('data-abre') : null, top = c.scrollTop;
    html(c, corpo); c.scrollTop = top;
    if (foco) { var f = c.querySelector('[data-abre="' + foco + '"]'); if (f && document.activeElement !== f) f.focus({ preventScroll: true }) }
  }

  // --- faixa de leitura ---
  var FAIXA = 'Passe o mouse ou o foco num agente, ticket ou alerta para ler aqui; clique para o detalhe.';
  function dica(ev) { var t = ev.target.closest && ev.target.closest('[data-dica]'); txt($('faixa-txt'), t ? t.getAttribute('data-dica') : FAIXA) }
  document.addEventListener('mouseover', dica); document.addEventListener('focusin', dica);

  // --- um ciclo ---
  function desenhar() {
    if (!lido) { leitura(); if (erro) ilegivel(erro); return }
    est = L.montar(lido, relogio());
    leitura();
    if (est.ilegivel) { ilegivel(est.ilegivel); return }
    ilegivel(null);
    placar(); alertas(); metro(); rede(); gaveta();
  }
  function ler() {
    acomp.atualizar().then(function (l) { lido = l; erro = null; falhaDesde = null; lidoEm = Date.now() })
      .catch(function (e) { erro = (e && e.message) || 'erro de leitura'; if (!falhaDesde) falhaDesde = Date.now() })
      .then(function () { setTimeout(ler, LEITURA_MS); desenhar() }); // agenda antes: um erro de desenho não para a sondagem
  }
  function comecar() {
    var q = new URLSearchParams(location.search), fixo = q.get('agora') && Date.parse(q.get('agora'));
    if (window.PAINEL_EMBUTIDO) { fonte = new L.FonteEmbutida(window.PAINEL_EMBUTIDO); modo = 'fixture embutida'; fixo = fixo || Date.parse(window.PAINEL_EMBUTIDO.agora) }
    else fonte = new L.FonteApi('/');
    if (fixo) { var t0 = Date.now(); relogio = function () { return fixo + (Date.now() - t0) }; if (modo === 'ao vivo') modo = 'relógio fixado' }
    txt($('faixa-txt'), FAIXA);
    acomp = new L.Acompanhamento(fonte);
    ler(); setInterval(desenhar, 1000);
  }

  $('g-fechar').addEventListener('click', fechar);
  $('b-problemas').addEventListener('click', function (ev) { abrir('problemas', null, ev.currentTarget) });
  $('g-corpo').addEventListener('click', function (ev) { var b = ev.target.closest('[data-abre]'); if (!b) return; var p = b.getAttribute('data-abre').split(':'); abrir(p[0], p[1], null) });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { if (escolha) { ev.preventDefault(); fechar() } else txt($('faixa-txt'), FAIXA); return }
    // estreito, a gaveta cobre a tela: o Tab fica dentro dela
    if (ev.key === 'Tab' && escolha && estreito()) {
      var g = $('gaveta'), f = g.querySelectorAll('button,[tabindex="-1"]'), pri = f[0], ult = f[f.length - 1];
      if (!g.contains(document.activeElement)) { ev.preventDefault(); pri.focus() }
      else if (ev.shiftKey && document.activeElement === pri) { ev.preventDefault(); ult.focus() }
      else if (!ev.shiftKey && document.activeElement === ult) { ev.preventDefault(); pri.focus() }
    }
  });
  window.addEventListener('resize', function () { if (est && !est.ilegivel) rede() });

  // aberto direto do disco: a fixture embutida, se existir
  if (location.protocol === 'file:') {
    var s = document.createElement('script'); s.src = '../fixture/embutida.js';
    s.onload = comecar; s.onerror = function () { erro = 'aberto do disco sem fixture embutida: rode iniciar.cmd'; desenhar() };
    document.body.appendChild(s);
  } else comecar();
})();
