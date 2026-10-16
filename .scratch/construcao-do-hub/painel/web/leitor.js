// Leitor do painel da construção (contrato.md, seções 4, 5 e 7). Só lê: monta o estado que a tela desenha.
// Duas fontes com a mesma cara: FonteApi (servidor.py, HTTP) e FonteEmbutida (fixture embutida, file://).
// montar() é pura: recebe o que foi lido e a hora, devolve o estado. Os nomes do contrato ficam nas tabelas abaixo.
(function (raiz) {
  'use strict';

  var FORMATO = 1;
  // tipos de evento do contrato (seção 5); fora desta lista: conta como sinal e entra nos problemas
  var TIPOS = ['inicio', 'sinal', 'pegou_ticket', 'passou_ticket', 'resolveu_ticket', 'devolveu', 'esperando_gustavo',
    'abriu_subagente', 'fechou_subagente', 'chamou_fable', 'mandou_mensagem', 'recebeu_mensagem', 'rodou_teste',
    'commit', 'passou_1h', 'falhou', 'fim'];
  // Status: do arquivo do ticket (seção 4, convenção do repositório) → coluna de partida.
  // "bloqueado" sai do Blocked by; um claimed vira revisão ou teste pelo papel de quem está com ele.
  var STATUS = { 'needs-triage': 'a_fazer', 'ready-for-agent': 'a_fazer', open: 'a_fazer', claimed: 'em_curso',
    review: 'revisao', testing: 'teste', resolved: 'feito', 'ready-for-human': 'esperando', 'needs-info': 'esperando',
    wontfix: 'descartado' };
  var ETAPA_DO_PAPEL = { revisor: 'revisao', prumo: 'revisao', testador: 'teste' };
  var COLUNAS = ['a_fazer', 'em_curso', 'revisao', 'teste', 'feito', 'bloqueado', 'esperando'];
  // eventos que encerram a tentativa em curso
  var FECHA = { passou_ticket: 1, resolveu_ticket: 1, devolveu: 1, esperando_gustavo: 1 };
  var PADRAO = { tentativa_min: 60, subagentes_por_agente: 10, sem_sinal_apos_s: 300 };
  var CONVERSA_MIN = 20; // a rede mostra as conversas destes últimos minutos

  function hora(v) { var t = Date.parse(v); return isNaN(t) ? null : t }
  function num(v) { if (v == null || v === '') return null; var m = String(v).match(/\d+/); return m ? (m[0].length < 2 ? '0' + m[0] : m[0]) : null }
  function fable(modelo) { return typeof modelo === 'string' && modelo.indexOf('claude-fable') === 0 }

  // --- fontes ---
  function FonteApi(base) { this.base = base || ''; this.nome = 'servidor' }
  FonteApi.prototype.json = function (c) {
    // prazo de 20 s: um pedido que não volta não pode congelar a sondagem
    var ctl = typeof AbortController === 'function' ? new AbortController() : null, prazo = ctl && setTimeout(function () { ctl.abort() }, 20000);
    return fetch(this.base + c, { cache: 'no-store', signal: ctl && ctl.signal }).then(function (r) {
      clearTimeout(prazo);
      return r.json().catch(function () { return null }).then(function (j) {
        if (!r.ok) throw new Error((j && j.mensagem) || ('HTTP ' + r.status));
        return j;
      });
    }, function (e) { clearTimeout(prazo); throw new Error(e && e.name === 'AbortError' ? 'o servidor não respondeu em 20 s' : 'o servidor do painel não responde'); });
  };
  FonteApi.prototype.execucao = function () { return this.json('api/execucao') };
  FonteApi.prototype.eventos = function (cur) {
    var c = Object.keys(cur).map(function (a) { return a + ':' + cur[a] }).join(',');
    return this.json('api/eventos' + (c ? '?c=' + encodeURIComponent(c) : ''));
  };
  // a fixture embutida responde como o servidor: cursor = posição no texto
  function FonteEmbutida(d) { this.d = d; this.nome = 'fixture embutida' }
  FonteEmbutida.prototype.execucao = function () { return Promise.resolve(this.d.execucao) };
  FonteEmbutida.prototype.eventos = function (cur) {
    var d = this.d, arq = {}, probl = [];
    Object.keys(d.eventos).forEach(function (a) {
      var txt = d.eventos[a], de = cur[a] || 0, rec = de > txt.length; if (rec) de = 0;
      var fim = txt.lastIndexOf('\n'), pedaco = fim >= de ? txt.slice(de, fim + 1) : '', linhas = [];
      pedaco.split('\n').forEach(function (l) { if (!l.trim()) return; try { linhas.push(JSON.parse(l)) } catch (e) { probl.push({ arquivo: 'eventos/' + a + '.jsonl', erro: 'linha', mensagem: 'linha que não é JSON' }) } });
      arq[a] = { ate: de + pedaco.length, linhas: linhas, recomecou: rec };
    });
    return Promise.resolve({ lido_em: null, arquivos: arq, problemas: probl });
  };

  // --- acompanhamento: guarda o que já leu e pede só o novo ---
  function Acompanhamento(fonte) { this.fonte = fonte; this.cur = {}; this.linhas = {}; this.problemasEv = []; this.api = null }
  Acompanhamento.prototype.atualizar = function () {
    var self = this;
    return self.fonte.execucao().then(function (api) {
      self.api = api;
      (api.agentes_com_arquivo || []).forEach(function (a) { if (!(a in self.cur)) self.cur[a] = 0 });
      ((api.execucao && api.execucao.agentes) || []).forEach(function (a) { if (a && a.id && !(a.id in self.cur)) self.cur[a.id] = 0 });
      return self.fonte.eventos(self.cur);
    }).then(function (r) {
      Object.keys(r.arquivos || {}).forEach(function (a) {
        var f = r.arquivos[a];
        if (f.recomecou || !self.linhas[a]) self.linhas[a] = [];
        self.linhas[a] = self.linhas[a].concat(f.linhas || []);
        self.cur[a] = f.ate;
      });
      // problemas de linha são do pedaço lido: acumulam (a linha ruim não volta no próximo pedido)
      self.problemasEv = self.problemasEv.concat(r.problemas || []).slice(-200);
      return { api: self.api, linhas: self.linhas, problemasEv: self.problemasEv };
    });
  };

  // --- reconstrução (seção 7) ---
  function montar(lido, agora) {
    var api = lido.api || {}, desc = api.execucao, problemas = (api.problemas || []).concat(lido.problemasEv || []);
    var est = { agora: agora, lido_em: hora(api.lido_em), problemas: problemas, ilegivel: null };
    if (!desc) { est.ilegivel = (api.problemas && api.problemas[0] && api.problemas[0].mensagem) || 'execucao.json não foi lido'; return est }
    if (desc.formato !== FORMATO) { est.ilegivel = 'formato desconhecido: ' + desc.formato + ' (o painel lê o formato ' + FORMATO + ')'; return est }
    var lim = {}; Object.keys(PADRAO).forEach(function (k) { lim[k] = +((desc.limites || {})[k]) || PADRAO[k] });
    est.desc = desc; est.titulo = desc.titulo || 'Construção'; est.limites = lim;
    est.inicio = hora(desc.inicio); est.terminou = hora(desc.terminou_em); est.fases = desc.fases || [];
    est.papeis = desc.papeis || [];

    // agentes: os da lista, mais quem tem arquivo e não está nela
    var defs = (desc.agentes || []).slice(), ids = {};
    defs.forEach(function (d) { ids[d.id] = 1 });
    Object.keys(lido.linhas || {}).forEach(function (id) { if (!ids[id]) { defs.push({ id: id, papel: id.replace(/-\d+$/, ''), foraDaLista: true }); ids[id] = 1 } });

    var tentativas = {}; // ticket -> [t de cada pegou_ticket], de todos os arquivos
    var conversas = [];
    var agentes = defs.map(function (d) {
      var evs = [];
      (lido.linhas[d.id] || []).forEach(function (l, i) {
        var t = hora(l.t);
        if (t == null) { problemas.push({ arquivo: 'eventos/' + d.id + '.jsonl', erro: 'hora', mensagem: 'evento sem hora válida (n.º ' + (i + 1) + ')' }); return }
        if (l.agente && l.agente !== d.id) problemas.push({ arquivo: 'eventos/' + d.id + '.jsonl', erro: 'agente', mensagem: 'evento com agente "' + l.agente + '" no arquivo de ' + d.id });
        var tipo = l.tipo;
        if (TIPOS.indexOf(tipo) < 0) { problemas.push({ arquivo: 'eventos/' + d.id + '.jsonl', erro: 'tipo', mensagem: 'tipo desconhecido: ' + tipo + ' (conta como sinal)' }); tipo = 'sinal' }
        evs.push({ t: t, tipo: tipo, ticket: num(l.ticket), sub: l.sub || null, para: l.para || null, de: l.de || null,
          assunto: l.assunto || null, detalhe: l.detalhe || null, ok: l.ok == null ? null : !!l.ok, modelo: l.modelo || null });
      });
      // ordem do arquivo; empate de hora não reordena
      var a = { id: d.id, papel: d.papel || null, titulo: d.titulo || d.id, modelo: d.modelo || null, esforco: d.esforco || null,
        terminal: d.terminal || null, temporario: !!d.temporario, foraDaLista: !!d.foraDaLista, eventos: evs,
        temArquivo: d.id in (lido.linhas || {}), ultimo: null, atual: null, subs: [], falha: null, esperando: null,
        encerrado: false, testes: { ok: 0, falha: 0 }, commits: 0, iniciouModelo: null };
      var subs = {}, ultimoTrabalho = null;
      evs.forEach(function (e) {
        a.ultimo = a.ultimo == null ? e.t : Math.max(a.ultimo, e.t);
        if (e.tipo !== 'sinal' && e.tipo !== 'inicio') ultimoTrabalho = e;
        switch (e.tipo) {
          case 'inicio': a.iniciouModelo = e.modelo; a.encerrado = false; break;
          case 'pegou_ticket':
            (tentativas[e.ticket] = tentativas[e.ticket] || []).push(e.t);
            a.atual = { ticket: e.ticket, desde: e.t, tentativa: tentativas[e.ticket].length, passou1h: false };
            a.falha = null; a.esperando = null; break;
          case 'passou_1h': if (a.atual && (!e.ticket || e.ticket === a.atual.ticket)) a.atual.passou1h = true; break;
          case 'esperando_gustavo': a.esperando = { t: e.t, ticket: e.ticket, detalhe: e.detalhe };
          /* falls through */
          case 'passou_ticket': case 'resolveu_ticket': case 'devolveu':
            if (a.atual && (!e.ticket || e.ticket === a.atual.ticket)) a.atual = null; break;
          case 'abriu_subagente': case 'chamou_fable':
            if (e.sub) subs[e.sub] = { id: e.sub, desde: e.t, assunto: e.assunto || (subs[e.sub] && subs[e.sub].assunto), modelo: e.modelo || (subs[e.sub] && subs[e.sub].modelo), ticket: e.ticket || (a.atual && a.atual.ticket) };
            if (e.tipo === 'chamou_fable' && e.para) conversas.push({ t: e.t, de: d.id, para: e.para, assunto: 'chamou o Fable' + (e.ticket ? ' para o ' + e.ticket : ''), ticket: e.ticket, fable: true });
            break;
          case 'fechou_subagente': delete subs[e.sub]; break;
          case 'mandou_mensagem': conversas.push({ t: e.t, de: d.id, para: e.para, assunto: e.assunto, ticket: e.ticket }); break;
          case 'rodou_teste': if (e.ok === false) a.testes.falha++; else a.testes.ok++; break;
          case 'commit': a.commits++; break;
          case 'falhou': a.falha = { t: e.t, ticket: e.ticket || (a.atual && a.atual.ticket), detalhe: e.detalhe }; subs = {}; break;
          case 'fim': a.encerrado = true; a.atual = null; subs = {}; break;
        }
      });
      a.subs = Object.keys(subs).map(function (k) { return subs[k] }).sort(function (x, y) { return x.desde - y.desde });
      a.fable = a.subs.filter(function (s) { return fable(s.modelo) });
      a.ehFable = fable(a.modelo) || fable(a.iniciouModelo);
      // a falha vale até o próximo pegou_ticket (mensagem e teste depois dela não a apagam)
      a.ultimoTrabalho = ultimoTrabalho;
      a.minutos = a.atual ? (agora - a.atual.desde) / 60000 : null;
      a.estourou = a.minutos != null && a.minutos >= lim.tentativa_min;
      a.silencioMin = a.ultimo == null ? null : (agora - a.ultimo) / 60000;
      a.semSinal = !!(a.ultimo != null && !a.encerrado && (agora - a.ultimo) / 1000 > lim.sem_sinal_apos_s);
      a.situacao = !a.temArquivo ? 'nao_comecou' : a.encerrado ? 'encerrado' : a.falha ? 'falhou' : a.semSinal ? 'sem_sinal'
        : a.atual ? 'trabalhando' : 'ocioso';
      return a;
    });
    var porId = {}; agentes.forEach(function (a) { porId[a.id] = a });

    // tickets: a coluna vem do arquivo, nunca do evento
    var tickets = (api.tickets || []).map(function (x) {
      var s = (x.status || '').trim().toLowerCase();
      return { numero: num(x.numero), arquivo: x.arquivo, titulo: x.titulo || x.arquivo, statusCru: x.status, base: STATUS[s] || 'desconhecido',
        dono: x.dono || null, com: x.com || null, blocked_by: (x.blocked_by || []).map(num), texto: x.texto || '' };
    });
    var tPor = {}; tickets.forEach(function (t) { tPor[t.numero] = t });
    tickets.forEach(function (t) {
      if (t.base === 'desconhecido') problemas.push({ arquivo: 'tickets/' + t.arquivo, erro: 'status', mensagem: 'Status desconhecido: ' + (t.statusCru || '(vazio)') });
      t.abertos = t.blocked_by.filter(function (b) { return !tPor[b] || tPor[b].base !== 'feito' });
      t.inexistentes = t.blocked_by.filter(function (b) { return !tPor[b] });
      t.triagem = (t.statusCru || '').trim().toLowerCase() === 'needs-triage';
      t.coluna = t.base === 'a_fazer' ? (t.abertos.length ? 'bloqueado' : 'a_fazer') : t.base === 'descartado' ? 'feito' : t.base;
      t.bloqueia = tickets.filter(function (o) { return o.blocked_by.indexOf(t.numero) >= 0 }).map(function (o) { return o.numero });
      t.agentes = agentes.filter(function (a) { return a.atual && a.atual.ticket === t.numero && a.situacao !== 'encerrado' }).map(function (a) { return a.id });
      var cur = t.agentes.length ? porId[t.agentes[0]] : null;
      t.relogio = cur ? { agente: cur.id, desde: cur.atual.desde, minutos: cur.minutos, estourou: cur.estourou, tentativa: cur.atual.tentativa } : null;
      t.falhou = agentes.filter(function (a) { return a.situacao === 'falhou' && a.falha.ticket === t.numero }).map(function (a) { return a.id });
      t.tentativas = (tentativas[t.numero] || []).length;
      // divergência: Com: diferente de quem deu o último pegou_ticket
      var ultimoPegou = null;
      agentes.forEach(function (a) { a.eventos.forEach(function (e) { if (e.tipo === 'pegou_ticket' && e.ticket === t.numero && (!ultimoPegou || e.t >= ultimoPegou.t)) ultimoPegou = { t: e.t, agente: a.id } }) });
      t.naoConfere = !!(t.com && ultimoPegou && t.com !== ultimoPegou.agente);
      // claimed: a etapa vem do papel de quem está com ele (Com:, senão o último pegou_ticket)
      var quem = t.com || (ultimoPegou && ultimoPegou.agente);
      if (t.base === 'em_curso' && quem && porId[quem] && ETAPA_DO_PAPEL[porId[quem].papel]) t.coluna = ETAPA_DO_PAPEL[porId[quem].papel];
    });
    // ciclo em Blocked by: problema, sem travar
    (function () {
      var cor = {};
      function visita(n, pilha) {
        if (cor[n] === 2 || !tPor[n]) return; if (cor[n] === 1) { problemas.push({ arquivo: 'tickets', erro: 'ciclo', mensagem: 'ciclo em Blocked by: ' + pilha.concat(n).join(' → ') }); return }
        cor[n] = 1; tPor[n].blocked_by.forEach(function (b) { visita(b, pilha.concat(n)) }); cor[n] = 2;
      }
      tickets.forEach(function (t) { visita(t.numero, []) });
    })();

    conversas.sort(function (x, y) { return x.t - y.t });
    // alertas: o que falhou, estourou, travou (sem sinal) ou espera o Gustavo
    var alertas = [];
    agentes.forEach(function (a) {
      if (a.situacao === 'falhou') alertas.push({ tipo: 'falhou', agente: a.id, ticket: a.falha.ticket, t: a.falha.t, texto: a.falha.detalhe });
      if (a.estourou && a.situacao !== 'encerrado') alertas.push({ tipo: 'estourou', agente: a.id, ticket: a.atual.ticket, t: a.atual.desde, minutos: a.minutos });
      if (a.semSinal) alertas.push({ tipo: 'sem_sinal', agente: a.id, ticket: a.atual && a.atual.ticket, t: a.ultimo, minutos: a.silencioMin });
    });
    tickets.forEach(function (t) {
      if (t.coluna !== 'esperando') return;
      var quem = null, det = null;
      agentes.forEach(function (a) { a.eventos.forEach(function (e) { if (e.tipo === 'esperando_gustavo' && e.ticket === t.numero) { quem = a.id; det = e.detalhe } }) });
      alertas.push({ tipo: 'esperando', ticket: t.numero, agente: quem, texto: det });
    });
    var ORD = { falhou: 0, estourou: 1, sem_sinal: 2, esperando: 3 };
    alertas.sort(function (x, y) { return ORD[x.tipo] - ORD[y.tipo] || (x.ticket || '').localeCompare(y.ticket || '') });

    var cont = {}; COLUNAS.forEach(function (c) { cont[c] = 0 });
    tickets.forEach(function (t) { cont[t.coluna] = (cont[t.coluna] || 0) + 1 });
    var validos = tickets.filter(function (t) { return t.base !== 'descartado' });
    // a equipe do placar: sem o maestro (conduz), sem o Fable e sem quem está fora da lista
    var trabalhadores = agentes.filter(function (a) { return a.papel !== 'maestro' && !a.temporario && !a.ehFable && !a.foraDaLista });
    var ultimos = agentes.map(function (a) { return a.ultimo }).filter(function (x) { return x != null });

    est.agentes = agentes; est.tickets = tickets; est.conversas = conversas; est.alertas = alertas; est.contagem = cont;
    est.recentes = conversas.filter(function (c) { return agora - c.t <= CONVERSA_MIN * 60000 });
    est.conversaMin = CONVERSA_MIN;
    est.feitos = validos.filter(function (t) { return t.base === 'feito' }).length; est.total = validos.length;
    est.trabalhando = trabalhadores.filter(function (a) { return a.situacao === 'trabalhando' }).length;
    est.equipe = trabalhadores.length;
    est.ultimo = ultimos.length ? Math.max.apply(null, ultimos) : null;
    return est;
  }

  var Leitor = { FonteApi: FonteApi, FonteEmbutida: FonteEmbutida, Acompanhamento: Acompanhamento, montar: montar, COLUNAS: COLUNAS, TIPOS: TIPOS, STATUS: STATUS };
  if (typeof module === 'object' && module.exports) module.exports = Leitor; else raiz.Leitor = Leitor;
})(this);
