// Tela Autorizações: as rodadas do maestro. Lista à esquerda (abertas em âmbar, respondidas com carimbo,
// absorvidas esmaecidas); à direita a rodada escolhida com as perguntas como cartões, um controle por tipo
// (escolha, varias, aprovar, texto, proposta), rascunho no navegador, envio com `envio` estável, 409 e emenda.
import { api } from '/web/torre.js';

const rascunhosEmMemoria = new Map();   // id da rodada → rascunho (espelho do localStorage)
const enviosFeitos = new Map();         // id da rodada → { envio, arquivo } do envio aceito nesta sessão
const corrigindo = new Set();           // rodadas em modo "corrigir resposta" (o rascunho guarda `correcao` para sobreviver à recarga)
// id da rodada → { base, chave, el } do formulário desenhado por último. A atualização ao vivo não troca um formulário
// cuja chave continua igual (a casca preserva o nó `data-preservar`); se a rodada mudou enquanto o Gustavo escrevia,
// o formulário antigo fica com um aviso "a rodada mudou" até ele pedir a versão nova.
const formulariosVivos = new Map();
const chaveDoFormulario = r => `rodada:${r.id}:${r.base}:${corrigindo.has(r.id) ? 'corrigindo' : 'respondendo'}`;

export function renderizar(app, u) {
  const { h, icone } = u;
  const rodadas = app.estado.rodadas || [];
  const alvo = app.rota.sub && app.indices.rodadas.get(app.rota.sub);
  const escolhida = alvo || app.aguardando()[0] || rodadas.find(r => r.estado === 'aberta') || rodadas[0] || null;
  return h('div.autorizacoes',
    lista(app, u, rodadas, escolhida),
    escolhida ? detalhe(app, u, escolhida) : h('section.painel.rodada-vazia', icone('carimbo'), h('p.vazio', 'Nenhuma rodada ainda. O maestro escreve as rodadas em arquivos na pasta do portal.')));
}

// ------------------------------------------------------------------ situação de uma rodada (lista e cabeçalho)
function situacao(app, r) {
  if (r.malformada) return { classe: 's-malformada', palavra: 'malformada', carimbo: null };
  if (r.estado === 'absorvida') return { classe: 's-absorvida', palavra: 'absorvida', carimbo: 'ABSORVIDA' };
  if (r.estado === 'suspensa') return { classe: 's-suspensa', palavra: 'suspensa', carimbo: null };
  if (r.estado === 'aberta' && !r.respondida && r.ultima_resposta) return { classe: 's-aberta', palavra: 'mudou: responda de novo', carimbo: 'MUDOU' };
  if (r.respondida) {
    const msg = (app.estado.caixa || []).find(c => c.arquivo === r.ultima_resposta);
    const entregue = msg && msg.aviso === 'entregue';
    return { classe: 's-respondida', palavra: entregue ? 'entregue ao maestro' : 'na fila para o maestro', carimbo: entregue ? 'ENTREGUE' : 'NA FILA', msg };
  }
  return { classe: 's-aberta', palavra: 'aguarda você', carimbo: null };
}

function lista(app, u, rodadas, escolhida) {
  const { h, icone, palhetas } = u;
  const ordem = r => r.malformada ? 1 : r.estado === 'aberta' && !r.respondida ? 0 : r.estado === 'aberta' ? 2 : r.estado === 'suspensa' ? 3 : 4;
  const ordenadas = [...rodadas].sort((a, b) => ordem(a) - ordem(b) || (a.id < b.id ? 1 : -1));
  const grupos = [['Aguardando você', 0], ['Malformadas', 1], ['Respondidas', 2], ['Suspensas', 3], ['Absorvidas', 4]];
  return h('nav.lista-rodadas', { 'aria-label': 'rodadas' },
    grupos.map(([titulo, k]) => {
      const rs = ordenadas.filter(r => ordem(r) === k);
      if (!rs.length) return null;
      return h('div.grupo-rodadas', h('h2.secao-titulo', titulo, h('span.n', String(rs.length))),
        rs.map(r => {
          const s = situacao(app, r);
          return h('a.item-rodada', { href: `#/autorizacoes/${encodeURIComponent(r.id)}`, class: `item-rodada ${s.classe}${escolhida && escolhida.id === r.id ? ' escolhida' : ''}`, 'aria-current': escolhida && escolhida.id === r.id ? 'page' : null, dataset: { foco: `rodada-${r.id}` } },
            h('div.titulo', r.titulo || r.id),
            h('div.sub', h('span.n-ticket', r.ticket || '—'), h('span', r.ticket_titulo || 'ticket não encontrado')),
            h('div.rodape',
              r.malformada ? h('span.c-coral', icone('alerta'), ' malformada') : h('span.perguntas', `${r.perguntas.length} ${r.perguntas.length === 1 ? 'pergunta' : 'perguntas'}`),
              s.carimbo ? h('span.carimbo', { class: `carimbo ${s.classe}` }, s.carimbo) : null,
              h('span.data', r.aberta || '')));
        }));
    }));
}

// ------------------------------------------------------------------ detalhe da rodada
function detalhe(app, u, r) {
  const { h, icone, markdown, abrirGaveta } = u;
  const s = situacao(app, r);
  const carta = r.carta ? app.indices.cartas.get(r.carta) : null;
  const cabeca = h('header.rodada-cabeca',
    h('div.rodada-rotulo', icone('carimbo'), 'rodada de perguntas', h('span.carimbo', { class: `carimbo ${s.classe}` }, s.palavra)),
    h('h1', r.titulo || r.id),
    h('div.rodada-meta',
      r.ticket ? h('button.chip.e-open', { type: 'button', onclick: () => abrirGaveta(r.ticket), dataset: { foco: 'rodada-ticket' } }, icone('aviao'), h('span.n-ticket', r.ticket), r.ticket_titulo || 'ticket não encontrado') : null,
      h('span.meta', icone('relogio'), `aberta ${r.aberta || '?'}`),
      h('span.meta.mono', r.arquivo)));
  const partes = [cabeca];
  if (r.malformada) {
    partes.push(h('div.aviso-rodada.coral', icone('alerta'), h('div', h('strong', 'Rodada malformada: '), `${r.erro}. O maestro precisa corrigir o arquivo; sem botão de enviar.`)));
    return h('section.rodada', partes);
  }
  if (r.contexto) partes.push(h('div.rodada-contexto', markdown(r.contexto)));
  if (carta) partes.push(miniaturaDaCarta(u, carta));
  else if (r.carta) partes.push(h('div.aviso-rodada', icone('alerta'), `A rodada cita a carta "${r.carta}", que não está no registro de cartas.`));

  const reaberta = r.estado === 'aberta' && !r.respondida && !!r.ultima_resposta;   // o maestro reescreveu depois da resposta
  if (reaberta) corrigindo.delete(r.id);
  if (r.respondida && !corrigindo.has(r.id) && lerRascunhoSeExiste(app, r)?.correcao) corrigindo.add(r.id);
  if (r.estado === 'absorvida' || r.estado === 'suspensa' || (r.respondida && !corrigindo.has(r.id))) {
    partes.push(respostaEnviada(app, u, r, s));
    return h('section.rodada', partes);
  }
  if (reaberta) partes.push(h('div.aviso-rodada.ambar', { dataset: { foco: 'aviso-reaberta' } }, icone('alerta'), h('div', h('strong', 'O maestro mudou esta rodada depois da sua resposta. '), 'Ela voltou a esperar por você: responda a versão nova abaixo. A resposta anterior continua guardada, logo depois do formulário, e a nova a substitui.')));
  partes.push(formularioOuPreservado(app, u, r));
  if (reaberta) partes.push(respostaEnviada(app, u, r, s, { historico: true }));
  return h('section.rodada', partes);
}

/** O formulário da rodada, ou só um marcador quando o que está na tela continua valendo (a casca mantém o nó vivo). */
function formularioOuPreservado(app, u, r) {
  const { h, icone } = u;
  const vivo = formulariosVivos.get(r.id);
  const naTela = vivo && vivo.el.isConnected && vivo.el.dataset.preservar === vivo.chave;
  const chave = chaveDoFormulario(r);
  if (naTela && vivo.chave === chave) return h('form', { dataset: { preservar: chave } });
  if (naTela && vivo.base !== r.base && (vivo.el.contains(document.activeElement) || rascunhoTemConteudo(rascunhosEmMemoria.get(chaveRascunho(app, { id: r.id, base: vivo.base }))))) {
    // a rodada mudou enquanto o Gustavo escrevia: o formulário dele fica; a troca só acontece quando ele pedir
    // (aviso e marcador como irmãos: o formulário vivo é filho direto da seção, e a casca só mantém ancestrais iguais)
    return [
      h('div.aviso-rodada.ambar.rodada-mudou', { dataset: { foco: 'rodada-mudou' } }, icone('alerta'), h('div', { style: 'flex:1' },
        h('strong', 'A rodada mudou enquanto você escrevia. '), 'O que você escreveu continua aqui e no rascunho deste navegador. Quando quiser, abra a versão nova: ela oferece copiar estas respostas.',
        h('div', { style: 'margin-top:6px' }, h('button.botao', { type: 'button', dataset: { foco: 'ver-versao-nova' }, onclick: () => { formulariosVivos.delete(r.id); document.dispatchEvent(new CustomEvent('torre:redesenhar')); } }, 'Ver a versão nova')))),
      h('form', { dataset: { preservar: vivo.chave } })];
  }
  return formularioDaRodada(app, u, r);
}
function rascunhoTemConteudo(d) { return !!(d && d.respostas && Object.values(d.respostas).some(x => !respostaVazia(x))); }

function miniaturaDaCarta(u, carta) {
  const { h, icone } = u;
  const quadro = h('iframe', { src: carta.url, title: carta.titulo, sandbox: 'allow-scripts', loading: 'lazy', tabindex: '-1', 'aria-hidden': 'true' });
  return h('a.miniatura-carta', { href: `#/cartas/${encodeURIComponent(carta.id)}`, dataset: { foco: 'rodada-carta', preservar: `miniatura:${carta.id}:${carta.url}:${carta.titulo}:${carta.proposito}` }, 'aria-label': `abrir a carta ${carta.titulo}` },
    h('div.quadro', quadro),
    h('div.legenda', icone('carta'), h('span', { style: 'flex:1' }, h('strong', carta.titulo), ` · ${carta.proposito}`), h('span.abrir', 'abrir a carta')));
}

// ------------------------------------------------------------------ resposta já enviada
function respostaEnviada(app, u, r, s, op = {}) {
  const { h, icone } = u;
  const caixa = h('section.resposta-enviada', op.historico ? { class: 'resposta-enviada historico', dataset: { foco: 'resposta-anterior' } } : null);
  const msg = s.msg || (app.estado.caixa || []).find(c => c.arquivo === r.ultima_resposta);
  if (op.historico) {
    if (!msg) return null;
    caixa.append(h('h2.secao-titulo', icone('relogio'), 'Sua resposta à versão anterior', h('span.carimbo', { class: 'carimbo s-respondida' }, 'VERSÃO ANTERIOR')));
    const corpoEl = h('div', h('p.vazio', 'Lendo a resposta anterior…'));
    caixa.append(corpoEl);
    api.caixaItem(msg.envio).then(dados => {
      const retrato = dados.rodada || r; const respostas = dados.corpo?.respostas || {};
      corpoEl.replaceChildren(
        h('div.meta-envio', h('span', `enviada ${String(dados.enviada || msg.enviada || '').replace('T', ' ').slice(0, 16)}`), h('span', `estado no maestro: ${dados.estado || msg.estado || '?'}`), h('span.mono', dados.arquivo || msg.arquivo)),
        h('ol.respostas-em-palavras', (retrato.perguntas || []).map((p, i) => h('li', h('div.pergunta-n', `pergunta ${i + 1}`), h('div.pergunta-t', p.titulo), h('div.em-palavras', emPalavras(p, respostas[p.id]))))),
        h('div', { style: 'margin-top:12px' }, h('button.botao', { type: 'button', dataset: { foco: 'copiar-anterior' }, onclick: () => copiarRespostaAnterior(app, u, r.id, dados) }, icone('seta'), 'Copiar para o formulário'), h('span.dica-inline', ' preenche as perguntas que não mudaram e que você ainda não respondeu; o resto fica em branco.')));
    }).catch(e => corpoEl.replaceChildren(h('p.vazio', `Não deu para ler a resposta anterior: ${e.message}`)));
    return caixa;
  }
  if (!msg) {
    caixa.append(h('p.vazio', r.estado === 'absorvida' ? 'Rodada absorvida pelo maestro.' : r.estado === 'suspensa' ? 'Rodada suspensa pelo maestro: espera sem resposta.' : 'Respondida, mas a resposta não foi encontrada na caixa.'));
    return caixa;
  }
  caixa.append(h('h2.secao-titulo', icone('resolvido'), 'O que você enviou', h('span.carimbo', { class: `carimbo ${s.classe}` }, s.carimbo || s.palavra)));
  const corpoEl = h('div', h('p.vazio', 'Lendo a resposta…'));
  caixa.append(corpoEl);
  api.caixaItem(msg.envio).then(dados => {
    const retrato = dados.rodada || r;
    const respostas = dados.corpo?.respostas || {};
    corpoEl.replaceChildren(...[
      h('div.meta-envio', h('span', `enviada ${String(dados.enviada || msg.enviada || '').replace('T', ' ').slice(0, 16)}`), h('span', `envio ${String(dados.envio).slice(0, 8)}…`), h('span', `estado no maestro: ${dados.estado || msg.estado || '?'}`), h('span', `aviso: ${dados.aviso || msg.aviso || 'sem registro'}`), h('span.mono', dados.arquivo || msg.arquivo)),
      h('ol.respostas-em-palavras', (retrato.perguntas || []).map((p, i) => h('li', h('div.pergunta-n', `pergunta ${i + 1}`), h('div.pergunta-t', p.titulo), h('div.em-palavras', emPalavras(p, respostas[p.id]))))),
      r.estado === 'aberta' ? h('div', { style: 'margin-top:12px' }, h('button.botao', { type: 'button', dataset: { foco: 'corrigir' }, onclick: ev => iniciarCorrecao(app, u, r, dados, ev.currentTarget) }, icone('carimbo'), 'Corrigir resposta'), h('span.dica-inline', ' começa com a resposta gravada; você muda só o que quiser e envia uma versão nova. O maestro absorve a mais nova.')) : null].filter(Boolean));
  }).catch(e => corpoEl.replaceChildren(h('p.vazio', `Não deu para ler a resposta: ${e.message}`)));
  return caixa;
}

/** Começa uma correção: o rascunho nasce como CÓPIA da resposta gravada (lida do servidor), com `envio` novo, e
 *  guarda em `correcao` o que está gravado (arquivo + respostas) para dizer o que vai mudar antes do envio. */
function iniciarCorrecao(app, u, r, dados, botao) {
  if (!dados || !dados.corpo || !dados.corpo.respostas) { u.brisa('Não deu para ler a resposta gravada; recarregue e tente de novo.', 'coral'); return; }
  const base = { arquivo: dados.arquivo, envio: dados.envio, respostas: JSON.parse(JSON.stringify(dados.corpo.respostas)) };
  const d = { envio: crypto.randomUUID(), respostas: JSON.parse(JSON.stringify(base.respostas)), mudadoEm: null, correcao: base };
  gravarRascunho(app, r, d);
  corrigindo.add(r.id); enviosFeitos.delete(r.id);
  document.dispatchEvent(new CustomEvent('torre:redesenhar'));
}
/** Copia a resposta à versão anterior para o rascunho da versão nova: só perguntas iguais nas duas versões (mesmo id,
 *  tipo, opções e proposta) e ainda em branco no rascunho; depois troca o formulário pelo preenchido. */
function copiarRespostaAnterior(app, u, rid, dados) {
  const r = app.indices.rodadas.get(rid); if (!r) return;
  const antes = new Map((dados.rodada?.perguntas || []).map(p => [p.id, p]));
  const respostas = dados.corpo?.respostas || {};
  const forma = p => JSON.stringify([p.tipo, p.opcoes || [], p.proposta || null]);
  const d = lerRascunho(app, r); let copiadas = 0, puladas = 0;
  for (const p of r.perguntas) {
    if (!respostas[p.id]) continue;
    const q = antes.get(p.id);
    if (!q || forma(q) !== forma(p)) { puladas++; continue; }
    if (!respostaVazia(d.respostas[p.id])) continue;
    d.respostas[p.id] = JSON.parse(JSON.stringify(respostas[p.id])); copiadas++;
  }
  gravarRascunho(app, r, d);
  const vivo = formulariosVivos.get(rid);
  if (vivo && vivo.el.isConnected) vivo.el.replaceWith(formularioDaRodada(app, u, r));
  else document.dispatchEvent(new CustomEvent('torre:redesenhar'));
  u.brisa(`${copiadas} resposta${copiadas === 1 ? '' : 's'} copiada${copiadas === 1 ? '' : 's'}${puladas ? `; ${puladas} pergunta${puladas === 1 ? '' : 's'} mudou e ficou em branco` : ''}.`, 'verde');
}
/** Quais perguntas da correção diferem da resposta gravada (comparação pelo corpo que seria enviado). */
function mudancasDaCorrecao(r, d) {
  if (!d.correcao) return null;
  const agora = montarCorpo(r, d).corpo.respostas, antes = d.correcao.respostas || {};
  const canon = x => JSON.stringify(x ?? null);
  return r.perguntas.map((p, i) => ({ i: i + 1, titulo: p.titulo, mudou: canon(agora[p.id]) !== canon(antes[p.id]) })).filter(x => x.mudou);
}

/** Uma resposta em palavras (para a vista "o que você enviou" e para o resumo do rascunho antigo). */
function emPalavras(p, resp) {
  if (!resp) return 'em branco';
  const texto = o => (p.opcoes || []).find(x => x.chave === o)?.texto || o;
  const partes = [];
  if (p.tipo === 'escolha' || p.tipo === 'varias') {
    if (resp.escolha?.length) partes.push((p.tipo === 'escolha' ? 'escolha: ' : 'escolhas: ') + resp.escolha.map(texto).join('; '));
    if (resp.outra) partes.push(`outra: ${resp.outra}`);
  } else if (p.tipo === 'aprovar') { if (resp.veredito) partes.push({ aprovado: 'aprovado', 'aprovado-com-ajuste': 'aprovado com ajuste', recusado: 'recusado' }[resp.veredito] || resp.veredito); }
  else if (p.tipo === 'texto') { if (resp.texto) partes.push(resp.texto); }
  else if (p.tipo === 'proposta') { if (resp.linhas) partes.push(descreverMudancas(p.proposta, resp.linhas).join('; ') || 'proposta mantida como o maestro propôs'); }
  if (resp.comentario) partes.push(`comentário: ${resp.comentario}`);
  return partes.length ? partes.join(' · ') : 'em branco';
}

// ------------------------------------------------------------------ rascunho
function chaveRascunho(app, r) { return `torre:${app.estado.projeto?.nome || ''}:${r.id}:${r.base}`; }
function lerRascunhoSeExiste(app, r) {
  const k = chaveRascunho(app, r);
  if (rascunhosEmMemoria.has(k)) return rascunhosEmMemoria.get(k);
  try { const bruto = localStorage.getItem(k); if (bruto) { const d = JSON.parse(bruto); if (d && typeof d === 'object' && d.respostas) return d; } } catch {}
  return null;
}
function lerRascunho(app, r) {
  const k = chaveRascunho(app, r);
  if (rascunhosEmMemoria.has(k)) return rascunhosEmMemoria.get(k);
  let d = null;
  try { const bruto = localStorage.getItem(k); if (bruto) d = JSON.parse(bruto); } catch { d = null; }
  if (!d || typeof d !== 'object' || !d.respostas) d = { envio: crypto.randomUUID(), respostas: {}, mudadoEm: null };
  rascunhosEmMemoria.set(k, d);
  return d;
}
function gravarRascunho(app, r, d) {
  d.mudadoEm = new Date().toISOString();
  const k = chaveRascunho(app, r); rascunhosEmMemoria.set(k, d);
  try { localStorage.setItem(k, JSON.stringify(d)); } catch { /* sem localStorage: fica só em memória */ }
}
function apagarRascunho(app, r) { const k = chaveRascunho(app, r); rascunhosEmMemoria.delete(k); try { localStorage.removeItem(k); } catch {} }
/** Rascunhos desta rodada feitos sobre outra `base` (a rodada mudou depois que o Gustavo começou). */
function rascunhosAntigos(app, r) {
  const prefixo = `torre:${app.estado.projeto?.nome || ''}:${r.id}:`;
  const achados = [];
  try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith(prefixo) && !k.endsWith(':' + r.base)) { try { const d = JSON.parse(localStorage.getItem(k)); if (d && d.respostas) { for (const id of Object.keys(d.respostas)) if (respostaVazia(d.respostas[id])) delete d.respostas[id]; if (Object.keys(d.respostas).length) achados.push({ chave: k, dados: d }); else localStorage.removeItem(k); } } catch {} } } } catch {}
  return achados;
}

// ------------------------------------------------------------------ formulário da rodada
function formularioDaRodada(app, u, r) {
  const { h, icone } = u;
  const d = lerRascunho(app, r);
  const estadoEnvio = enviosFeitos.get(r.id);
  const chaveForm = chaveDoFormulario(r);
  const form = h('form.formulario-rodada', { novalidate: true, onsubmit: ev => ev.preventDefault(), dataset: { preservar: chaveForm } });
  formulariosVivos.set(r.id, { base: r.base, chave: chaveForm, el: form });
  const salvar = () => { gravarRascunho(app, r, d); aviso.textContent = 'rascunho guardado neste navegador'; atualizarMudancasDaCorrecao(); };
  const antigos = rascunhosAntigos(app, r);
  if (antigos.length) form.append(painelRascunhoAntigo(app, u, r, antigos, d, () => { salvar(); form.replaceWith(formularioDaRodada(app, u, r)); }));
  const resumoCorrecao = h('div.mudancas-correcao', { 'aria-live': 'polite' });
  const atualizarMudancasDaCorrecao = () => {
    if (!corrigindo.has(r.id) || !d.correcao) return;
    const m = mudancasDaCorrecao(r, d);
    resumoCorrecao.replaceChildren(m.length ? h('span', 'Vai mudar: ', m.map((x, j) => [j ? ', ' : null, h('strong', `pergunta ${x.i}`), ` (${x.titulo})`])) : h('span', 'Nada mudou ainda em relação à resposta gravada; o que você não mexer vai igual.'));
  };
  if (corrigindo.has(r.id)) {
    if (!d.correcao) form.append(h('div.aviso-rodada.coral', icone('alerta'), h('div', h('strong', 'Correção sem a resposta gravada. '), 'Este rascunho não partiu da resposta gravada; o que você enviar substitui a resposta inteira. Clique em "Limpar rascunho" e depois em "Corrigir resposta" para começar da resposta gravada.')));
    else form.append(h('div.aviso-rodada', icone('carimbo'), h('div', h('strong', 'Corrigindo a resposta. '), 'O formulário já está preenchido com o que foi gravado; mude só o que quiser. A nova versão substitui a anterior inteira, e o maestro absorve só a mais nova.', h('div', resumoCorrecao))));
    atualizarMudancasDaCorrecao();
  }
  const cartoes = r.perguntas.map((p, i) => cartaoPergunta(app, u, r, p, i, d, salvar));
  form.append(h('ol.perguntas', cartoes));
  const aviso = h('span.aviso-rascunho', { 'aria-live': 'polite' }, d.mudadoEm ? `rascunho guardado ${d.mudadoEm.replace('T', ' ').slice(0, 16)}` : '');
  const erro = h('div.erro-acao', { role: 'alert' });
  const enviar = h('button.botao.primario.grande', { type: 'button', dataset: { foco: 'enviar-torre' } }, icone('carimbo'), d.emVoo ? 'Tentar de novo' : 'Enviar à torre');
  const limpar = h('button.botao', { type: 'button', onclick: () => { if (Object.keys(d.respostas).length === 0 && !d.correcao) return; d.respostas = {}; apagarRascunho(app, r); if (corrigindo.has(r.id)) { corrigindo.delete(r.id); document.dispatchEvent(new CustomEvent('torre:redesenhar')); return; } form.replaceWith(formularioDaRodada(app, u, r)); } }, corrigindo.has(r.id) ? 'Desistir da correção' : 'Limpar rascunho');
  const rodape = h('div.rodada-rodape-caixa', h('div.rodape-rodada', enviar, limpar, aviso, erro));
  form.append(rodape);
  if (d.emVoo) erro.textContent = `Envio pendente (${d.emVoo.motivo}). "Tentar de novo" reenvia exatamente a resposta original, com o mesmo envio; o que você mudar depois só vai numa correção, depois de ele ser resolvido.`;
  const concluir = (resp) => {
    enviosFeitos.set(r.id, { envio: resp.envio, arquivo: resp.arquivo, repetido: !!resp.repetido, base: r.base });
    apagarRascunho(app, r); corrigindo.delete(r.id);
    u.brisa('Resposta gravada na caixa.', 'verde');
    form.replaceWith(confirmacaoDeEnvio(app, u, r, resp));
  };
  enviar.onclick = async () => {
    let corpo;
    if (d.emVoo) corpo = d.emVoo.corpo; // retentativa: o par (envio, corpo) congelado no primeiro envio
    else {
      const m = montarCorpo(r, d); corpo = m.corpo;
      if (m.faltas.length) { erro.textContent = m.faltas.join(' '); return; }
      if (m.vazio) { erro.textContent = 'Nada respondido ainda: marque pelo menos uma pergunta.'; return; }
      const atual = app.indices.rodadas.get(r.id) || r;
      if (corrigindo.has(r.id)) { const ant = d.correcao?.arquivo || (app.estado.caixa || []).find(c => c.arquivo === atual.ultima_resposta)?.arquivo; if (ant) corpo.substitui = ant; }
      // rodada reescrita depois da resposta: a resposta à versão nova substitui a anterior (o maestro absorve a mais nova)
      else if (atual.ultima_resposta && !atual.respondida && atual.base === r.base) corpo.substitui = atual.ultima_resposta;
    }
    enviar.disabled = true; limpar.disabled = true; erro.textContent = '';
    try {
      const resp = await api.caixa(corpo);
      concluir(resp);
    } catch (e) {
      enviar.disabled = false; limpar.disabled = false;
      if (!e.status || e.status >= 500) {
        d.emVoo = { corpo, motivo: e.message }; salvar();
        erro.textContent = `Não deu para confirmar a gravação (${e.message}). "Tentar de novo" reenvia a mesma resposta com o mesmo envio.`;
        enviar.replaceChildren(icone('carimbo'), 'Tentar de novo');
      } else if (e.status === 409 && e.corpo?.erro === 'rodada-mudou') {
        d.emVoo = null; salvar();
        erro.textContent = 'A rodada mudou depois que você começou. O rascunho ficou guardado; em instantes aparece acima o botão "Ver a versão nova", que oferece copiar as respostas para ela.';
      } else if (e.status === 409 && e.corpo?.erro === 'envio-conflito') {
        // o envio já existe com outro corpo: o primeiro envio foi gravado; é ele que vale
        try { const g = await api.caixaItem(corpo.envio); concluir({ envio: g.envio, arquivo: g.arquivo, repetido: true }); return; }
        catch { erro.textContent = 'A torre diz que este envio já existe com outro conteúdo, mas não deu para relê-lo. Recarregue a página e confira a caixa.'; }
      } else {
        d.emVoo = null; salvar();
        erro.textContent = `A torre recusou: ${e.message}${e.corpo?.campo ? ` (campo ${e.corpo.campo})` : ''}.`;
        enviar.replaceChildren(icone('carimbo'), 'Enviar à torre');
      }
      enviar.focus();
    }
  };
  if (estadoEnvio && estadoEnvio.base === r.base && !corrigindo.has(r.id)) return confirmacaoDeEnvio(app, u, r, estadoEnvio);
  return form;
}

function confirmacaoDeEnvio(app, u, r, resp) {
  const { h, icone } = u;
  const caixa = h('section.resposta-enviada', { tabindex: -1, dataset: { foco: 'confirmacao' } },
    h('div.resultado-acao', h('div', { style: 'display:flex;align-items:center;gap:8px' }, icone('resolvido'), h('span', `Resposta gravada na caixa${resp.repetido ? ' (já estava gravada)' : ''}. O maestro absorve no ticket.`)), h('div.mono', resp.arquivo || ''), h('div', { style: 'font-size:12px;color:var(--texto-apagado)' }, `envio ${String(resp.envio).slice(0, 8)}…`)));
  const corpoEl = h('div', h('p.vazio', 'Lendo o que foi gravado…'));
  caixa.append(corpoEl);
  api.caixaItem(resp.envio).then(dados => {
    const retrato = dados.rodada || r; const respostas = dados.corpo?.respostas || {};
    corpoEl.replaceChildren(
      h('h2.secao-titulo', icone('carimbo'), 'O que foi gravado', h('span.carimbo.s-respondida', dados.aviso === 'entregue' ? 'ENTREGUE' : 'NA FILA')),
      h('ol.respostas-em-palavras', (retrato.perguntas || []).map((p, i) => h('li', h('div.pergunta-n', `pergunta ${i + 1}`), h('div.pergunta-t', p.titulo), h('div.em-palavras', emPalavras(p, respostas[p.id]))))),
      h('div', { style: 'margin-top:12px' }, h('button.botao', { type: 'button', dataset: { foco: 'corrigir' }, onclick: ev => iniciarCorrecao(app, u, r, dados, ev.currentTarget) }, icone('carimbo'), 'Corrigir resposta'), h('span.dica-inline', ' começa com a resposta gravada; você muda só o que quiser.')));
  }).catch(e => corpoEl.replaceChildren(h('p.vazio', `Gravado, mas não deu para reler: ${e.message}`)));
  setTimeout(() => caixa.focus({ preventScroll: true }), 0);
  return caixa;
}

function painelRascunhoAntigo(app, u, r, antigos, d, aoCopiar) {
  const { h, icone } = u;
  const a = antigos[antigos.length - 1];
  const porId = new Map(r.perguntas.map(p => [p.id, p]));
  return h('div.aviso-rodada.ambar',
    icone('alerta'),
    h('div', { style: 'flex:1' },
      h('strong', 'A rodada mudou depois que você começou a responder. '), 'Seu rascunho sobre a versão anterior está guardado:',
      h('ul', { style: 'margin:6px 0' }, Object.entries(a.dados.respostas).map(([id, resp]) => { const p = porId.get(id); return h('li', h('strong', p ? p.titulo : `pergunta "${id}" (não existe mais)`), ': ', p ? emPalavras(p, resp) : JSON.stringify(resp)); })),
      h('div', { style: 'display:flex;gap:8px;margin-top:6px' },
        h('button.botao', { type: 'button', dataset: { foco: 'copiar-rascunho' }, onclick: () => { for (const [id, resp] of Object.entries(a.dados.respostas)) if (porId.has(id) && respostaVazia(d.respostas[id])) d.respostas[id] = resp; try { localStorage.removeItem(a.chave); } catch {} aoCopiar(); } }, 'Copiar para a versão nova'),
        h('button.botao', { type: 'button', onclick: () => { try { localStorage.removeItem(a.chave); } catch {} aoCopiar(); } }, 'Descartar o antigo'))));
}

/** Uma resposta de rascunho sem nada marcado nem escrito (os cartões criam `{}` ao desenhar). */
function respostaVazia(x) {
  if (!x) return true;
  return !((x.escolha && x.escolha.length) || (x.outra || '').trim() || (x.comentario || '').trim() || x.veredito || (x.texto || '').trim() || x.linhas);
}

// ------------------------------------------------------------------ montagem do corpo do POST
function montarCorpo(r, d) {
  const respostas = {}; const faltas = [];
  for (const p of r.perguntas) {
    const x = d.respostas[p.id]; if (!x) continue;
    const com = (x.comentario || '').trim() || null;
    if (p.tipo === 'escolha' || p.tipo === 'varias') {
      const esc = (x.escolha || []).filter(k => p.opcoes.some(o => o.chave === k));
      const outra = (x.outra || '').trim() || null;
      if (!esc.length && !outra && !com) continue;
      respostas[p.id] = { escolha: esc, outra, comentario: com };
    } else if (p.tipo === 'aprovar') {
      if (!x.veredito && !com) continue;
      if (!x.veredito) { faltas.push(`"${p.titulo}": escolha aprovar, aprovar com ajuste ou recusar.`); continue; }
      if (x.veredito !== 'aprovado' && !com) { faltas.push(`"${p.titulo}": ${x.veredito === 'recusado' ? 'a recusa' : 'o ajuste'} precisa de comentário.`); continue; }
      respostas[p.id] = { veredito: x.veredito, comentario: com };
    } else if (p.tipo === 'texto') {
      const t = (x.texto || '').trim(); if (!t) continue;
      respostas[p.id] = { texto: t };
    } else if (p.tipo === 'proposta') {
      if (!x.linhas && !com) continue;
      const linhas = (x.linhas || linhasBase(p.proposta)).map(l => ({ id: l.id, ativa: l.ativa !== false, valores: { ...l.valores } }));
      if (!x.linhas || !descreverMudancas(p.proposta, linhas).length) { if (!com) continue; respostas[p.id] = { linhas, comentario: com }; continue; }
      respostas[p.id] = { linhas, comentario: com };
    }
  }
  return { corpo: { envio: d.envio, tipo: 'resposta', rodada: r.id, base: r.base, respostas }, vazio: Object.keys(respostas).length === 0, faltas };
}

// ------------------------------------------------------------------ cartão de pergunta
function cartaoPergunta(app, u, r, p, i, d, salvar) {
  const { h, icone, markdown } = u;
  const x = d.respostas[p.id] || (d.respostas[p.id] = {});
  const corpo = h('div.pergunta-corpo');
  const TIPOS = { escolha: 'escolha uma', varias: 'marque uma ou mais', aprovar: 'aprovação', texto: 'texto livre', proposta: 'proposta editável' };
  const tipo = TIPOS[p.tipo] || `tipo "${p.tipo}"`;
  if (p.tipo === 'escolha' || p.tipo === 'varias') corpo.append(controleOpcoes(u, p, x, salvar, i));
  else if (p.tipo === 'aprovar') corpo.append(controleAprovar(u, p, x, salvar, i));
  else if (p.tipo === 'texto') corpo.append(h('textarea.texto-livre', { 'aria-label': p.titulo, placeholder: 'escreva aqui (opcional)', maxlength: '20000', dataset: { foco: `q-${p.id}-texto` }, value: x.texto || '', oninput: ev => { x.texto = ev.target.value; salvar(); } }));
  else if (p.tipo === 'proposta') corpo.append(controleProposta(u, p, x, salvar, i));
  else corpo.append(h('p.vazio', `Tipo de pergunta desconhecido: "${p.tipo}". A torre recusa respostas a ela.`));
  if (p.tipo !== 'texto') corpo.append(comentarioDaPergunta(u, p, x, salvar));
  return h('li.cartao-pergunta', { dataset: { foco: `q-${p.id}` } },
    h('div.pergunta-cabeca', h('span.pergunta-n', `pergunta ${i + 1}`), h('span.pergunta-tipo', tipo), p.recomendada?.length ? h('span.recomendada-selo', icone('resolvido'), 'o maestro recomenda uma opção') : null),
    h('h3', p.titulo),
    corpo,
    p.porque ? h('details.porque', h('summary', icone('pergunta'), 'por quê'), markdown(p.porque)) : null);
}

function comentarioDaPergunta(u, p, x, salvar) {
  const { h } = u;
  const det = h('details.comentario-pergunta', { open: !!x.comentario });
  det.append(h('summary', 'comentário'), h('textarea', { 'aria-label': `comentário sobre ${p.titulo}`, placeholder: 'opcional', maxlength: '20000', dataset: { foco: `q-${p.id}-comentario` }, value: x.comentario || '', oninput: ev => { x.comentario = ev.target.value; salvar(); } }));
  return det;
}

function controleOpcoes(u, p, x, salvar, i) {
  const { h, icone } = u;
  const multi = p.tipo === 'varias';
  x.escolha = x.escolha || [];
  const grupo = h('div.opcoes', { role: multi ? 'group' : 'radiogroup', 'aria-label': p.titulo });
  for (const o of p.opcoes) {
    const marcado = x.escolha.includes(o.chave);
    const inp = h('input', { type: multi ? 'checkbox' : 'radio', name: `q-${i}`, value: o.chave, checked: marcado || null, dataset: { foco: `q-${p.id}-${o.chave}` },
      onchange: ev => { if (multi) { x.escolha = ev.target.checked ? [...x.escolha, o.chave] : x.escolha.filter(k => k !== o.chave); } else { x.escolha = [o.chave]; } salvar(); } });
    grupo.append(h('label.opcao', { class: `opcao${p.recomendada.includes(o.chave) ? ' recomendada' : ''}` }, inp, h('span.texto', o.texto), p.recomendada.includes(o.chave) ? h('span.selo', icone('resolvido'), 'recomendada') : null));
  }
  if (!multi && x.escolha.length) grupo.append(h('button.limpar-escolha', { type: 'button', onclick: ev => { x.escolha = []; salvar(); for (const r of grupo.querySelectorAll('input')) r.checked = false; ev.target.remove(); } }, 'desmarcar'));
  const outra = h('details.outra', { open: !!x.outra }, h('summary', 'nenhuma destas, e sim…'), h('textarea', { 'aria-label': 'outra resposta', placeholder: 'outra resposta', maxlength: '20000', dataset: { foco: `q-${p.id}-outra` }, value: x.outra || '', oninput: ev => { x.outra = ev.target.value; salvar(); } }));
  return h('div', grupo, outra);
}

function controleAprovar(u, p, x, salvar, i) {
  const { h, icone } = u;
  const ops = [['aprovado', 'Aprovar', 'verde', 'resolvido'], ['aprovado-com-ajuste', 'Aprovar com ajuste', 'ambar', 'carimbo'], ['recusado', 'Recusar', 'coral', 'descartado']];
  const grupo = h('div.veredito', { role: 'radiogroup', 'aria-label': p.titulo });
  for (const [v, rot, cor, ic] of ops) {
    const b = h('button.botao', { type: 'button', role: 'radio', 'aria-checked': x.veredito === v ? 'true' : 'false', class: `botao ${cor}${x.veredito === v ? ' marcado' : ''}`, dataset: { foco: `q-${p.id}-${v}` },
      onclick: () => { x.veredito = x.veredito === v ? null : v; salvar(); for (const o of grupo.children) { const on = o.dataset.v === x.veredito; o.setAttribute('aria-checked', on ? 'true' : 'false'); o.classList.toggle('marcado', on); } nota.textContent = x.veredito && x.veredito !== 'aprovado' ? 'este veredito pede um comentário abaixo' : ''; } }, icone(ic), rot);
    b.dataset.v = v; grupo.append(b);
  }
  const nota = h('div.nota-veredito', x.veredito && x.veredito !== 'aprovado' ? 'este veredito pede um comentário abaixo' : '');
  return h('div', grupo, nota);
}

// ------------------------------------------------------------------ proposta editável (emenda)
function linhasBase(prop) { return (prop?.linhas || []).map(l => ({ id: l.id, ativa: true, valores: Object.fromEntries((prop.colunas || []).map(c => [c, l[c] ?? ''])) })); }
function descreverMudancas(prop, linhas) {
  const colunas = prop?.colunas || []; const base = new Map((prop?.linhas || []).map(l => [l.id, l])); const ordemBase = (prop?.linhas || []).map(l => l.id);
  const out = [];
  const ids = linhas.map(l => l.id);
  for (const l of linhas) {
    const b = base.get(l.id);
    if (!b) { out.push(`linha nova "${l.id}": ${colunas.map(c => `${c} "${l.valores[c] ?? ''}"`).join(', ')}`); continue; }
    for (const c of colunas) if ((l.valores[c] ?? '') !== (b[c] ?? '')) out.push(`linha "${rotuloLinha(prop, b)}": ${c} de "${b[c] ?? ''}" para "${l.valores[c] ?? ''}"`);
    if (l.ativa === false) out.push(`linha "${rotuloLinha(prop, b)}": desligada`);
  }
  for (const id of ordemBase) if (!ids.includes(id)) out.push(`linha "${rotuloLinha(prop, base.get(id))}": removida`);
  const sobre = ids.filter(id => base.has(id)); const esperado = ordemBase.filter(id => ids.includes(id));
  const novasNoFim = ids.slice(ids.length - linhas.filter(l => !base.has(l.id)).length).every(id => !base.has(id));
  if (sobre.join() !== esperado.join() || !novasNoFim) out.push(`ordem nova: ${linhas.map(l => rotuloLinha(prop, base.get(l.id)) || l.id).join(', ')}`);
  return out;
}
function rotuloLinha(prop, b) { if (!b) return null; const c = (prop.colunas || [])[0]; return c && b[c] ? String(b[c]) : b.id; }

function controleProposta(u, p, x, salvar, i) {
  const { h, icone } = u;
  const prop = p.proposta || { colunas: [], linhas: [], pode: [] };
  const pode = new Set(prop.pode || []);
  // as linhas só entram no rascunho quando o Gustavo mexe (senão a cópia de um rascunho antigo acharia este "preenchido")
  const linhas = () => x.linhas || (x.linhas = linhasBase(prop));
  const raiz = h('div.emenda');
  let arrastando = null;
  const desenhar = () => {
    const L = x.linhas || linhasBase(prop);
    const tabela = h('table.tabela-emenda', h('thead', h('tr', pode.has('reordenar') ? h('th', { scope: 'col' }, h('span.visualmente-oculto', 'ordem')) : null, pode.has('ligar') ? h('th', { scope: 'col' }, 'ativa') : null, prop.colunas.map(c => h('th', { scope: 'col' }, c)), pode.has('remover') ? h('th', { scope: 'col' }, h('span.visualmente-oculto', 'remover')) : null)));
    const tbody = h('tbody');
    L.forEach((l, idx) => {
      const nova = !prop.linhas.some(b => b.id === l.id);
      const tr = h('tr', { class: `${l.ativa === false ? 'desligada' : ''}${nova ? ' nova' : ''}`, draggable: pode.has('reordenar') ? 'true' : null, dataset: { idx: String(idx) } });
      if (pode.has('reordenar')) tr.append(h('td.ordem', h('span.alca', { 'aria-hidden': 'true' }, '⋮⋮'), h('button.mini', { type: 'button', 'aria-label': `subir a linha ${idx + 1}`, disabled: idx === 0 || null, dataset: { foco: `q-${p.id}-sobe-${l.id}` }, onclick: () => { const X = linhas(); [X[idx - 1], X[idx]] = [X[idx], X[idx - 1]]; salvar(); desenhar(); focarPorChave(`q-${p.id}-sobe-${l.id}`); } }, '▲'), h('button.mini', { type: 'button', 'aria-label': `descer a linha ${idx + 1}`, disabled: idx === L.length - 1 || null, dataset: { foco: `q-${p.id}-desce-${l.id}` }, onclick: () => { const X = linhas(); [X[idx + 1], X[idx]] = [X[idx], X[idx + 1]]; salvar(); desenhar(); focarPorChave(`q-${p.id}-desce-${l.id}`); } }, '▼')));
      if (pode.has('ligar')) tr.append(h('td', h('input', { type: 'checkbox', 'aria-label': `linha ${idx + 1} ativa`, checked: l.ativa !== false || null, dataset: { foco: `q-${p.id}-liga-${l.id}` }, onchange: ev => { linhas()[idx].ativa = ev.target.checked; salvar(); desenhar(); focarPorChave(`q-${p.id}-liga-${l.id}`); } })));
      for (const c of prop.colunas) {
        tr.append(h('td', pode.has('editar')
          ? h('input.celula', { type: 'text', value: l.valores[c] ?? '', 'aria-label': `${c}, linha ${idx + 1}`, maxlength: '20000', dataset: { foco: `q-${p.id}-${l.id}-${c}` }, oninput: ev => { linhas()[idx].valores[c] = ev.target.value; salvar(); atualizarMudancas(); } })
          : h('span', l.valores[c] ?? '')));
      }
      if (pode.has('remover')) tr.append(h('td', h('button.mini.coral', { type: 'button', 'aria-label': `remover a linha ${idx + 1}`, onclick: () => { linhas().splice(idx, 1); salvar(); desenhar(); focarPorChave(`q-${p.id}-adicionar`) || focarPorChave(`q-${p.id}`); } }, icone('fechar'))));
      if (pode.has('reordenar')) {
        tr.addEventListener('dragstart', ev => { arrastando = idx; ev.dataTransfer.effectAllowed = 'move'; tr.classList.add('arrastando'); });
        tr.addEventListener('dragover', ev => { ev.preventDefault(); tr.classList.add('alvo-drop'); });
        tr.addEventListener('dragleave', () => tr.classList.remove('alvo-drop'));
        tr.addEventListener('drop', ev => { ev.preventDefault(); if (arrastando === null || arrastando === idx) return; const X = linhas(); const [m] = X.splice(arrastando, 1); X.splice(idx, 0, m); arrastando = null; salvar(); desenhar(); });
        tr.addEventListener('dragend', () => { arrastando = null; desenhar(); });
      }
      tbody.append(tr);
    });
    tabela.append(tbody);
    const acoes = h('div.acoes-emenda',
      pode.has('adicionar') ? h('button.botao', { type: 'button', dataset: { foco: `q-${p.id}-adicionar` }, onclick: () => { const X = linhas(); let n = 1; while (X.some(l => l.id === `nova-${n}`)) n++; X.push({ id: `nova-${n}`, ativa: true, valores: Object.fromEntries(prop.colunas.map(c => [c, ''])) }); salvar(); desenhar(); focarPorChave(`q-${p.id}-nova-${n}-${prop.colunas[0]}`); } }, '+ linha') : null,
      h('button.botao', { type: 'button', dataset: { foco: `q-${p.id}-desfazer` }, onclick: () => { delete x.linhas; salvar(); desenhar(); focarPorChave(`q-${p.id}-desfazer`); } }, icone('seta'), 'Desfazer tudo'),
      h('span.pode', `o maestro permite: ${[...pode].join(', ') || 'nada (só comentar)'}`));
    const mudancas = h('div.mudancas', { 'aria-live': 'polite' });
    raiz.replaceChildren(tabela, acoes, h('h4', 'o que mudou'), mudancas);
    atualizarMudancas();
    function atualizarMudancas() {
      const lista = descreverMudancas(prop, x.linhas || linhasBase(prop));
      mudancas.replaceChildren(lista.length ? h('ul', lista.map(m => h('li', m))) : h('p.vazio', 'nada: a proposta está como o maestro propôs.'));
    }
  };
  desenhar();
  return raiz;
}
function focarPorChave(chave) { const el = document.querySelector(`[data-foco="${CSS.escape(chave)}"]`); if (el) { el.focus({ preventScroll: true }); return true; } return false; }
