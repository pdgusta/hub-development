// Tela Laços (#/lacos, #/lacos/<id>, ?no=<id do nó>): o que roda por trás. À esquerda, os laços por grupo (espera
// você, em voo, terminados); à direita, o laço escolhido como um fluxo de nós no estilo n8n (forma e cor pelo papel,
// setas com uma palavra, a volta "repete" em arco, botões e painéis numa faixa de cima, o trabalho fora dos scripts
// numa faixa de madeira embaixo), os pedidos com o estado de cada um e o comentário para o laço todo. Clicar num nó
// abre a gaveta dele (estado real, botões com configurado × em uso × sua proposta, comentário do nó, pedidos do nó).
// O portal só lê os laços e grava pedidos na caixa (POST /api/caixa, tipo alteracao-laco, §4.5): o navegador manda
// só ids e valores tipados; quem aplica é o maestro. Lê GET /api/lacos e GET /api/laco/<id> a cada 10 s, só enquanto
// a tela está aberta (§3.4); o redesenho preserva o que está em edição (`data-preservar`, §3.7).
import { api, trocarPreservando, prenderFoco, emEdicao } from '/web/torre.js';

const INTERVALO_MS = 10000;
const LIDO_SEM_DESFECHO_MIN = 10;   // a partir daqui "lido" vira "lido, sem desfecho há N min"
const MAX_LINHA = 22;               // caracteres de uma linha de texto sob um nó (o resto vai para a faixa de leitura)

// ------------------------------------------------------------------ dados vivos (só enquanto a tela está aberta)
const dados = { lista: null, erroLista: null, detalhes: new Map(), erros: new Map(), pedindo: new Set() };
let vigia = null, vigiando = false, assinatura = '', appRef = null;
const naTela = () => /^#\/lacos(?:[/?]|$)/.test(location.hash);
const redesenhar = () => { if (naTela()) document.dispatchEvent(new CustomEvent('torre:redesenhar')); };

function ligarVigia() { if (vigiando) return; vigiando = true; clearTimeout(vigia); ciclo(); }
function pararVigia() { vigiando = false; clearTimeout(vigia); vigia = null; }
async function ciclo() {
  if (!naTela()) { pararVigia(); return; }
  await atualizar();
  if (vigiando) vigia = setTimeout(ciclo, INTERVALO_MS);
}
/** Relê a lista e o laço escolhido; redesenha só se algo mudou (ou o minuto virou, por causa do "há N min"). */
let pedidasLista = 0, aplicadaLista = 0; // uma leitura da lista que chega depois de outra mais nova é descartada
async function atualizar(forcar = false) {
  const n = ++pedidasLista;
  try { const l = await api.lacos(); if (n > aplicadaLista) { aplicadaLista = n; dados.lista = l; dados.erroLista = null; } }
  catch (e) { if (n > aplicadaLista) { aplicadaLista = n; dados.erroLista = e; } }
  const id = appRef ? idEscolhido(appRef) : null;
  if (id) await buscarDetalhe(id);
  const sem = (k, v) => (k === 'lido_em' ? undefined : v);
  const nova = JSON.stringify([dados.lista, dados.erroLista?.message, id, dados.detalhes.get(id), dados.erros.get(id)?.message, Math.floor(Date.now() / 60000)], sem);
  if (forcar || nova !== assinatura) { assinatura = nova; redesenhar(); }
}
// uma leitura por laço de cada vez; quem pede enquanto outra está em voo espera por ela e por uma leitura nova (a que
// estava em voo pode ter saído antes do que acabou de mudar, ex.: o pedido recém-gravado)
const emVoo = new Map();
async function buscarDetalhe(id) {
  if (emVoo.has(id)) { const r = emVoo.get(id); r.denovo = true; return r.promessa; }
  const reg = { denovo: false };
  reg.promessa = (async () => {
    dados.pedindo.add(id);
    try {
      do {
        reg.denovo = false;
        try { dados.detalhes.set(id, await api.laco(id)); dados.erros.delete(id); }
        catch (e) { dados.erros.set(id, e); if (e.status === 404 || e.status === 422) dados.detalhes.delete(id); }
      } while (reg.denovo);
    } finally { dados.pedindo.delete(id); emVoo.delete(id); }
  })();
  emVoo.set(id, reg);
  return reg.promessa;
}
// fora da tela: o relógio para e a gaveta do nó fecha
document.addEventListener('torre:redesenhando', () => { if (!naTela()) { pararVigia(); fecharGavetaNo(); } });
// Esc com o foco fora da gaveta aberta (ex.: depois de um clique no fluxo) também a fecha; dentro dela quem fecha é o
// foco preso (que para a propagação)
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape' || !gavetaAberta || e.defaultPrevented) return;
  if (document.querySelector('.dialogo:not([hidden]), #leitor:not([hidden]), #gaveta:not([hidden])')) return;
  const id = gavetaAberta.laco;
  location.hash = hrefLaco(id);
});

// ------------------------------------------------------------------ palavras, números e horas
const fmt = (v, casas = 2) => Number(v).toLocaleString('pt-BR', { maximumFractionDigits: casas });
const doisDig = n => String(n).padStart(2, '0');
function hhmm(iso) { const d = new Date(iso); return isNaN(d) ? '?' : `${doisDig(d.getHours())}h${doisDig(d.getMinutes())}`; }
function mesmoDia(d) { const a = new Date(); return d.getFullYear() === a.getFullYear() && d.getMonth() === a.getMonth() && d.getDate() === a.getDate(); }
/** "23h12" hoje; "13/10 15h13" em outro dia. */
function quando(iso) {
  if (!iso) return '';
  const d = new Date(iso); if (isNaN(d)) return String(iso);
  return mesmoDia(d) ? hhmm(iso) : `${doisDig(d.getDate())}/${doisDig(d.getMonth() + 1)} ${hhmm(iso)}`;
}
function minutosDesde(iso) { const d = new Date(iso); return isNaN(d) ? null : Math.max(0, Math.round((Date.now() - d) / 60000)); }
/** "há 2 min", "há 3 h", "em 13/10 15h13". */
function ha(iso) {
  const m = minutosDesde(iso); if (m === null) return '';
  if (m < 1) return 'agora há pouco';
  if (m < 60) return `há ${m} min`;
  if (m < 24 * 60) return `há ${Math.floor(m / 60)} h`;
  return `em ${quando(iso)}`;
}
const corta = (s, n) => (s = String(s ?? '')).length > n ? s.slice(0, n - 1).trimEnd() + '…' : s;

const PAPEL = {
  etapa: { palavra: 'etapa', dica: 'script que faz trabalho' },
  decisao: { palavra: 'decisão', dica: 'ponto em que o laço escolhe por regra: repete ou termina' },
  controle: { palavra: 'botão', dica: 'limite ou regra que condiciona outro nó, sem trabalho próprio' },
  observador: { palavra: 'painel', dica: 'só olha o laço; nunca é causa de nada' },
  'fora-dos-scripts': { palavra: 'fora dos scripts', dica: 'trabalho de pessoa ou agente, conduzido pelo maestro' },
};
const LIGACAO = {
  segue: 'cadeia de trabalho', repete: 'volta de onda: o laço repete enquanto a regra manda',
  condiciona: 'um botão que condiciona este nó', observa: 'um painel que só olha; não é causa',
};
const SITUACAO = {
  rodando: { palavra: 'rodando', classe: 's-rodando', icone: 'onda' },
  'esperando-cota': { palavra: 'esperando cota', classe: 's-pedra', icone: 'relogio' },
  'sem-sinal': { palavra: 'sem sinal', classe: 's-pedra-tracejado', icone: 'sinal' },
  parado: { palavra: 'parado', classe: 's-pedra', icone: 'parar' },
  terminado: { palavra: 'terminado', classe: 's-terminado', icone: 'tarefa' },
  desconhecido: { palavra: 'estado desconhecido', classe: 's-pedra-tracejado', icone: 'pergunta' },
};
const SITUACAO_DICA = {
  rodando: 'o último sinal é recente; arquivo novo não prova processo vivo, só que algo escreveu ali',
  'esperando-cota': 'o despachante não tem modelo apto agora (nenhum, ou todos fora até a virada da cota)',
  'sem-sinal': 'o último sinal é mais velho que o limite que o laço declara; arquivo velho não prova processo morto',
  parado: 'a parada está gravada; o maestro ainda não deu a execução por terminada',
  terminado: 'o maestro deu esta execução por terminada: só leitura, mas o comentário continua',
  desconhecido: 'nenhuma fonte de sinal pôde ser lida',
};
const QUANDO_VALE = { agora: 'agora (no ciclo seguinte do laço)', 'proxima-onda': 'na próxima onda', 'ao-reiniciar': 'ao reiniciar o processo que lê', 'proxima-execucao': 'só numa execução nova' };
const RELEITURA = { continua: 'o laço relê sozinho a cada ciclo', 'ao-ligar': 'o processo só lê ao ligar: aplicar = gravar e religar quem lê', manual: 'o maestro troca à mão' };
const PRECONDICAO = { inicio: 'conta desde' };
const CAPACIDADE = {
  'parar-apos-onda': { titulo: 'Parar depois de uma onda', dica: 'a onda em curso fecha e o laço sai; pode levar muito tempo' },
  'parar-de-despachar': { titulo: 'Parar de despachar', dica: 'nenhum trabalho novo sai; o que está em voo termina; os resultados ficam' },
};

/** Um valor de controle em palavras, na unidade dele (fração com escala "porcento" vira %). */
function valorEmPalavras(c, v) {
  if (v === null || v === undefined) return c.nulo || 'vazio';
  const un = c.unidade ? ` ${c.unidade}` : '';
  switch (c.tipo) {
    case 'numero': return c.escala === 'porcento' ? `${fmt(v * 100, 2)}%${un}` : `${fmt(v, 4)}${un}`;
    case 'inteiro': return `${fmt(v, 0)}${un}`;
    case 'duracao': return `${fmt(v, 2)} ${c.unidade}`;
    case 'escolha': return (c.opcoes || []).find(o => o.valor === v)?.rotulo || String(v);
    case 'lista': return `${v.length} ${v.length === 1 ? 'item' : 'itens'}`;
    case 'texto-curto': return `“${v}”`;
    default: return String(v);
  }
}
const tipadoEmPalavras = (c, t) => !t ? '—' : (c && t.tipo === c.tipo ? valorEmPalavras(c, t.valor) : (t.tipo === 'texto' ? String(t.valor) : JSON.stringify(t.valor)));

/** O número de um contador em palavras (sem a hora); `null` quando o valor é uma série (desenhada à parte). */
function contadorEmPalavras(ct) {
  if (ct.ilegivel) return `${ct.rotulo}: ilegível`;
  const v = ct.valor;
  if (v === null || v === undefined) return `${ct.rotulo}: sem valor`;
  switch (ct.tipo) {
    case 'inteiro': return `${fmt(v, 0)} ${ct.rotulo}`;
    case 'numero': return ct.escala === 'porcento' ? `${fmt(v * 100, 1)}% ${ct.rotulo}` : `${fmt(v, 2)} ${ct.rotulo}`;
    case 'hora': return `${ct.rotulo} ${quando(v)}`;
    case 'lista': return `${v.length} ${ct.rotulo}`;
    case 'contagem': return `${fmt(Object.values(v).reduce((a, b) => a + b, 0), 0)} ${ct.rotulo}`;
    case 'serie': return `${v.length} × ${ct.rotulo}`;
    default: return corta(v, 40);
  }
}

// ------------------------------------------------------------------ escolha do laço e da gaveta
function idEscolhido(app) {
  if (app.rota.sub) return app.rota.sub;
  const l = dados.lista || [];
  return (l.find(x => x.grupo === 'espera-voce') || l.find(x => x.grupo === 'em-voo') || l[0] || {}).id || null;
}
const hrefLaco = (id, no) => `#/lacos/${encodeURIComponent(id)}${no ? `?no=${encodeURIComponent(no)}` : ''}`;
function abrirNo(lacoId, noId) { if (location.hash !== hrefLaco(lacoId, noId)) location.hash = hrefLaco(lacoId, noId); }

// ------------------------------------------------------------------ rascunhos (localStorage, uma chave por laço e execução)
// torre:<projeto>:laco:<id>:<execução> → { controles: {id: rascunho}, nos: {id: rascunho}, laco: rascunho, parada: rascunho }
// Um rascunho guarda o `envio` (UUID) e, depois de uma falha ambígua, `emVoo` = o corpo exatamente como foi enviado:
// "tentar de novo" manda esse mesmo corpo com o mesmo envio (padrão do Responder). Só nasce quando o Gustavo mexe.
const rascunhos = new Map();
const geracoes = new Map();   // chave de formulário → número; sobe quando o formulário precisa nascer de novo
const geracao = k => geracoes.get(k) || 0;
const novaGeracao = k => geracoes.set(k, geracao(k) + 1);
function chaveRascunho(app, laco) { return `torre:${app.estado.projeto?.nome || ''}:laco:${laco.id}:${laco.execucao.id}`; }
function rascunhoDo(app, laco) {
  const k = chaveRascunho(app, laco);
  if (rascunhos.has(k)) return rascunhos.get(k);
  let r = null;
  try { r = JSON.parse(localStorage.getItem(k) || 'null'); } catch { r = null; }
  if (!r || typeof r !== 'object') r = {};
  r.controles = r.controles || {}; r.nos = r.nos || {};
  rascunhos.set(k, r);
  return r;
}
function guardar(app, laco) {
  const k = chaveRascunho(app, laco); const r = rascunhoDo(app, laco);
  const vazio = !Object.keys(r.controles).length && !Object.keys(r.nos).length && !r.laco && !r.parada;
  try { if (vazio) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(r)); } catch { /* sem localStorage: só memória */ }
}

/** O pedido ainda aberto (nova, lida ou conflito, não substituído) que um envio novo do mesmo grupo substitui (§4.5). */
function substituivel(laco, casa) {
  return (laco.pedidos || []).find(p => p.atual && !p.substituido_por && ['nova', 'lida', 'conflito'].includes(p.estado) && casa(p)) || null;
}
// ---- substituição sem referência velha (revisão do Prumo, 2026-10-15)
// O rascunho NÃO guarda o alvo de `substitui` calculado quando nasceu: guarda só qual alvo a tela mostrou (`alvoVisto`)
// e, numa recuperação, o alvo que o Gustavo escolheu (`substituiDecidido`). Na hora de enviar, o laço é relido e o alvo
// é recalculado; se não é mais o que a tela mostrou (o maestro deu desfecho enquanto ele escrevia), ou se a torre
// responde 400 `substitui-invalido`, nada é enviado em silêncio: a tela diz em palavras o que aconteceu e oferece
// "Enviar como pedido novo" (UUID novo, sem referência) ou, se houver outro pedido aberto, substituí-lo dizendo qual.
// O "tentar de novo" de um erro ambíguo de rede não passa por aqui: reenvia o mesmo corpo com o mesmo envio.
const lacoAtual = laco => dados.detalhes.get(laco.id) || laco;
const CASA_PARADA = p => ['pedir-parada', 'pedir-pausa', 'pedir-retomada'].includes(p.operacao);
const casaControle = id => p => p.operacao === 'mudar-controle' && p.controle === id;
/** O alvo de `substitui` de um envio agora: o escolhido numa recuperação, ou o pedido aberto do grupo no estado atual. */
function alvoDaSubstituicao(laco, d, casa) {
  const L = lacoAtual(laco);
  if (d.substituiDecidido) return d.substitui ? substituivel(L, p => p.arquivo === d.substitui && casa(p)) : null;
  return substituivel(L, casa);
}
/** O alvo que a tela mostrou deixou de valer (ou a torre recusou a referência): é preciso o Gustavo decidir. */
function precisaDecidir(laco, d, casa) {
  if (!d || d.emVoo) return false;
  if (d.recuperar) return true;
  if (d.substituiDecidido) return !!d.substitui && !alvoDaSubstituicao(laco, d, casa);
  if (d.alvoVisto === undefined) return false;
  return (d.alvoVisto || null) !== (alvoDaSubstituicao(laco, d, casa)?.arquivo || null);
}
const descreverPedido = (L, p) => `o de ${quando(p.enviada)} (${palavraDoPedido(L, p)}${p.operacao === 'mudar-controle' && p.depois ? ` para ${tipadoEmPalavras(L.controles.find(c => c.id === p.controle), p.depois)}` : ''})`;
/** Nota fora do formulário (refeita a cada atualização): o que este envio vai substituir, em palavras. */
function notaDeSubstituicao(u, laco, d, casa) {
  const { h, icone } = u;
  if (!d || precisaDecidir(laco, d, casa)) return null;
  const alvo = alvoDaSubstituicao(laco, d, casa);
  if (!alvo) return null;
  const L = lacoAtual(laco);
  return h('div.nota-substitui', icone('recibo'), `este pedido substitui o seu pedido anterior, ${descreverPedido(L, alvo)}, ainda ${estadoDoPedido(L, alvo).palavra}`);
}
/** A recuperação: o que aconteceu com o pedido que seria substituído e como enviar agora (sempre dito em palavras). */
function blocoDeRecuperacao(u, laco, d, casa, aoEscolher, foco) {
  const { h, icone } = u;
  const L = lacoAtual(laco);
  const antigoId = d.recuperar?.alvo ?? (d.substituiDecidido ? d.substitui : d.alvoVisto);
  const antigo = antigoId ? (L.pedidos || []).find(p => p.arquivo === antigoId) : null;
  const outro = substituivel(L, p => casa(p) && p.arquivo !== antigoId);
  let oQue;
  if (antigo) {
    const e = estadoDoPedido(L, antigo);
    const motivo = antigo.recibo?.motivo ? ` (motivo: ${antigo.recibo.motivo})` : '';
    oQue = antigo.substituido_por ? `O pedido que este substituiria, ${descreverPedido(L, antigo)}, já foi substituído por outro.` : `O pedido que este substituiria, ${descreverPedido(L, antigo)}, já teve desfecho: ${e.palavra}${motivo}.`;
  } else if (antigoId) oQue = 'O pedido que este substituiria não está mais aberto.';
  else oQue = 'Apareceu um pedido aberto que este substituiria; a tela não substitui sem você dizer.';
  return h('div.recuperar-subst', { role: 'alert' },
    h('p', icone('alerta'), h('strong', 'Nada foi gravado. '), oQue, ' Seu valor e seu texto continuam aqui.'),
    outro ? h('p', `Há outro pedido seu ainda aberto: ${descreverPedido(L, outro)}, ${estadoDoPedido(L, outro).palavra}.`) : null,
    h('div.rodape-acao',
      outro ? h('button.botao.primario', { type: 'button', dataset: { foco: `${foco}-subst` }, onclick: () => aoEscolher(outro.arquivo) }, icone('envelope'), `Enviar substituindo o de ${quando(outro.enviada)}`) : null,
      h('button.botao', { type: 'button', class: outro ? 'botao' : 'botao primario', dataset: { foco: `${foco}-novo` }, onclick: () => aoEscolher(null) }, icone('envelope'), outro ? 'Enviar como pedido novo, sem substituir' : 'Enviar como pedido novo')));
}
/** Aplica a escolha da recuperação: envio NOVO (o 400 não gravou nada), referência dita pelo Gustavo, e envia. */
function escolherSubstituicao(app, laco, d, alvo, chaveBotao) {
  d.envio = crypto.randomUUID(); d.substitui = alvo; d.substituiDecidido = true; d.alvoVisto = alvo; d.recuperar = null; d.emVoo = null;
  guardar(app, laco);
  document.querySelector(`[data-foco="${CSS.escape(chaveBotao)}"]`)?.click();
}

// ------------------------------------------------------------------ tela
let escutando = false;
export function renderizar(app, u) {
  const { h, icone } = u;
  appRef = app;
  ligarVigia();
  // um arquivo do projeto mudou (a casca releu o estado: ex. o maestro gravou um desfecho no .md): relê o laço já,
  // sem esperar o relógio de 10 s
  if (!escutando) { escutando = true; app.aoMudar(() => { if (naTela()) atualizar(); }); }
  u.repousoDaFaixa('Passe o mouse ou foque um nó, uma seta ou um selo: a leitura dele aparece aqui. Clique num nó para abrir a gaveta dele.');
  if (!dados.lista && !dados.erroLista) { sincronizarGaveta(app, u, null); return h('div.lacos', h('p.vazio', 'Lendo os laços…')); }
  if (!dados.lista) { sincronizarGaveta(app, u, null); return h('div.lacos', h('div.aviso-rodada.coral', icone('alerta'), h('div', h('strong', 'Não deu para ler os laços. '), `${dados.erroLista.message}. Tentando de novo a cada 10 segundos.`))); }
  const id = idEscolhido(app);
  const item = dados.lista.find(x => x.id === id) || null;
  const laco = id ? dados.detalhes.get(id) : null;
  const erro = id ? dados.erros.get(id) : null;
  if (id && !laco && !erro && !dados.pedindo.has(id)) buscarDetalhe(id).then(() => atualizar(true));
  const raiz = h('div.lacos',
    listaDeLacos(app, u, id),
    h('div.laco-lado', !dados.lista.length ? h('section.laco-vazio', icone('laco'), h('p.vazio', 'Nenhum laço registrado. O maestro registra cada laço no lacos.json da pasta do portal.'))
      : !item ? h('div.aviso-rodada.coral', icone('alerta'), h('div', `O laço "${id}" não está no registro de laços.`))
      : laco ? detalheDoLaco(app, u, laco)
      : erro ? lacoComErro(u, item, erro)
      : h('p.vazio', 'Lendo o laço…')));
  sincronizarGaveta(app, u, laco && item ? laco : null);
  return raiz;
}

// ------------------------------------------------------------------ lista de laços
function listaDeLacos(app, u, escolhido) {
  const { h, icone } = u;
  const grupos = [['espera-voce', 'espera você', 'bandeira', 'g-espera'], ['em-voo', 'em voo', 'onda', 'g-voo'], ['terminado', 'terminados', 'tarefa', 'g-feito']];
  return h('nav.lista-lacos', { 'aria-label': 'laços' },
    grupos.map(([g, titulo, ic, classe]) => {
      const itens = dados.lista.filter(x => x.grupo === g);
      return h('div.grupo-lacos', { class: `grupo-lacos ${classe}` },
        h('h2.grupo-lacos-titulo', icone(ic), titulo, itens.length ? h('span.n', String(itens.length)) : null),
        itens.length ? itens.map(x => itemDaLista(app, u, x, escolhido)) : h('p.vazio-grupo', g === 'espera-voce' ? 'nada espera você' : g === 'em-voo' ? 'nenhum agora' : 'nenhum ainda'));
    }));
}
function itemDaLista(app, u, x, escolhido) {
  const { h, icone } = u;
  const sit = SITUACAO[x.situacao] || SITUACAO.desconhecido;
  const linhas = [];
  if (x.problema) linhas.push(h('span.selo-laco.s-erro', { dataset: { dica: x.problema, dicaTitulo: 'laço malformado' } }, icone('alerta'), 'malformado'));
  else if (x.grupo === 'terminado') linhas.push(h('span.selo-laco.s-terminado', icone('tarefa'), `terminou ${quando(x.terminou_em)}`));
  else linhas.push(h('span.selo-laco', { class: `selo-laco ${sit.classe}`, dataset: { dica: SITUACAO_DICA[x.situacao] || '', dicaTitulo: sit.palavra } }, icone(sit.icone), sit.palavra));
  const sub = [];
  if (x.destaque) sub.push(h('span', icone('caixa'), x.destaque.ilegivel ? `${x.destaque.rotulo}: ilegível` : contadorEmPalavras({ ...x.destaque, tipo: typeof x.destaque.valor === 'number' ? (Number.isInteger(x.destaque.valor) ? 'inteiro' : 'numero') : 'texto' })));
  if (x.grupo !== 'terminado' && !x.problema) sub.push(h('span', icone('sinal'), x.ultimo_sinal ? `sinal ${ha(x.ultimo_sinal.hora)}` : 'sem sinal'));
  if (x.pedidos_abertos) sub.push(h('span.c-ambar', icone('envelope'), `${x.pedidos_abertos} pedido${x.pedidos_abertos > 1 ? 's' : ''} aberto${x.pedidos_abertos > 1 ? 's' : ''}`));
  const ticket = x.ticket ? app.ticket(x.ticket) : null;
  return h('a.item-laco', { href: hrefLaco(x.id), class: `item-laco g-${x.grupo}${x.id === escolhido ? ' escolhido' : ''}${x.problema ? ' malformado' : ''}`, 'aria-current': x.id === escolhido ? 'page' : null, dataset: { foco: `laco-${x.id}` } },
    h('div.titulo', x.titulo),
    x.ticket ? h('div.sub', { dataset: { dica: ticket ? ticket.titulo : 'ticket não encontrado', dicaTitulo: `ticket ${x.ticket}` } }, `ticket ${x.ticket}`) : null,
    h('div.linha-selos', linhas),
    sub.length ? h('div.numeros', sub) : null);
}

function lacoComErro(u, item, erro) {
  const { h, icone } = u;
  const malformado = erro.status === 422;
  return h('section.laco-aberto',
    h('header.laco-cabeca', h('div.laco-cabeca-texto',
      h('h1', item.titulo),
      h('div.laco-meta', h('span.selo-laco.s-erro', icone('alerta'), malformado ? 'malformado' : 'não lido')))),
    h('div.aviso-rodada.coral', icone('alerta'), h('div', h('strong', malformado ? 'A descrição deste laço está fora do contrato. ' : 'Não deu para ler este laço. '),
      `${erro.message}. ${malformado ? 'Sem fluxo, sem botões e sem comentário: o maestro precisa corrigir o laco.json.' : 'Tentando de novo a cada 10 segundos.'}`)));
}

// ------------------------------------------------------------------ o laço aberto
function detalheDoLaco(app, u, laco) {
  const { h, icone, abrirGaveta } = u;
  const terminado = !!laco.execucao.terminou_em;
  const sit = SITUACAO[laco.situacao] || SITUACAO.desconhecido;
  const ticket = laco.ticket ? app.ticket(laco.ticket) : null;
  const caps = (laco.capacidades || []).map(c => c.id);
  const podeParar = !terminado && (caps.includes('parar-apos-onda') || caps.includes('parar-de-despachar'));
  const podePausar = !terminado && caps.includes('pausar-retomar');
  const r = rascunhoDo(app, laco);
  const abrirPainel = op => { r.parada = r.parada && r.parada.operacao === op ? r.parada : { aberto: true, operacao: op, alvoVisto: substituivel(laco, CASA_PARADA)?.arquivo || null }; r.parada.aberto = true; guardar(app, laco); redesenhar(); };

  const cabeca = h('header.laco-cabeca',
    h('div.laco-cabeca-texto',
      h('div.laco-rotulo', icone('laco'), 'laço', laco.grupo === 'espera-voce' ? h('span.chip.e-espera', icone('bandeira'), 'espera você') : null),
      h('h1', laco.titulo),
      h('div.laco-meta',
        laco.ticket ? h('button.chip.e-open', { type: 'button', onclick: () => abrirGaveta(laco.ticket), dataset: { foco: 'laco-ticket', dicaTitulo: `ticket ${laco.ticket}`, dica: `${ticket ? ticket.titulo : 'ticket não encontrado'} · clique para abrir o ticket` } }, icone('aviao'), `ticket ${laco.ticket}`) : null,
        h('button.chip.e-open.com-dica', { type: 'button', dataset: { dica: `identificador da execução: ${laco.execucao.id}. Uma execução é uma partida do laço, do plano da onda 1 até o fim; um pedido nunca passa sozinho para a execução seguinte.`, dicaTitulo: 'execução', foco: 'laco-execucao' } }, icone('relogio'), laco.execucao.inicio ? `execução desde ${quando(laco.execucao.inicio)}` : 'execução sem início anotado'),
        terminado
          ? h('span.selo-laco.s-terminado', icone('tarefa'), `terminou ${quando(laco.execucao.terminou_em)}`)
          : h('button.selo-laco.com-dica', { type: 'button', class: `selo-laco com-dica ${sit.classe}`, dataset: { dica: SITUACAO_DICA[laco.situacao] || '', dicaTitulo: sit.palavra, foco: 'laco-situacao' } }, icone(sit.icone), sit.palavra),
        !terminado ? h('button.meta-sinal.com-dica', { type: 'button', dataset: { foco: 'laco-sinal', dicaTitulo: 'último sinal', dica: laco.ultimo_sinal ? `a hora mais nova entre as fontes que o laço declara: ${laco.ultimo_sinal.fonte}, ${quando(laco.ultimo_sinal.hora)}. Nunca quer dizer "vivo": arquivo novo não prova processo vivo.` : 'nenhuma fonte de sinal pôde ser lida' } }, icone('sinal'), laco.ultimo_sinal ? `sinal ${ha(laco.ultimo_sinal.hora)}` : 'sem sinal') : null,
        laco.cota?.ilegivel && !terminado ? h('span.meta-sinal.c-coral', { dataset: { dica: laco.cota.ilegivel, dicaTitulo: 'cota ilegível' } }, icone('alerta'), 'cota: ilegível') : null,
        laco.pedidos_abertos ? h('span.meta-sinal.c-ambar', icone('envelope'), `${laco.pedidos_abertos} pedido${laco.pedidos_abertos > 1 ? 's' : ''} aberto${laco.pedidos_abertos > 1 ? 's' : ''}`) : null)),
    h('div.laco-acoes',
      terminado ? h('div.so-leitura', icone('olho'), h('span', h('strong', 'só leitura'), ' · o laço terminou; comentário continua')) : null,
      podeParar ? h('button.botao.de-pedido', { type: 'button', 'aria-expanded': r.parada?.aberto && r.parada.operacao === 'pedir-parada' ? 'true' : 'false', dataset: { foco: 'pedir-parada' }, onclick: () => abrirPainel('pedir-parada') }, icone('parar'), 'Pedir parada') : null,
      podePausar ? h('button.botao.de-pedido', { type: 'button', 'aria-expanded': r.parada?.aberto && r.parada.operacao === 'pedir-pausa' ? 'true' : 'false', dataset: { foco: 'pedir-pausa' }, onclick: () => abrirPainel('pedir-pausa') }, icone('pausa'), 'Pedir pausa') : null,
      podePausar ? h('button.botao.de-pedido', { type: 'button', dataset: { foco: 'pedir-retomada' }, onclick: () => abrirPainel('pedir-retomada') }, icone('retomar'), 'Pedir retomada') : null,
      podeParar || podePausar ? h('div.nota-cota', icone('alerta'), 'até valer, chamadas em voo ainda gastam cota') : null));

  const partes = [cabeca];
  const porQue = esperaVoce(app, u, laco);
  if (porQue) partes.push(porQue);
  if (!terminado && r.parada?.aberto) partes.push(painelDeParada(app, u, laco));
  partes.push(quadroDoFluxo(app, u, laco));
  partes.push(h('div.laco-baixo', comentarioDoLaco(app, u, laco), pedidosDoLaco(app, u, laco)));
  return h('section.laco-aberto', partes);
}

/** Por que o laço espera você: a rodada aberta do ticket dele e/ou um pedido em conflito (§3.4). */
function esperaVoce(app, u, laco) {
  const { h, icone } = u;
  if (laco.grupo !== 'espera-voce') return null;
  const rodadas = app.aguardando().filter(r => String(Number(r.ticket)) === String(Number(laco.ticket)) || r.ticket === laco.ticket);
  const conflitos = (laco.pedidos || []).filter(p => p.estado === 'conflito' && p.atual && !p.substituido_por);
  return h('div.espera-voce', icone('bandeira'),
    h('div', h('strong', 'Espera você: '),
      rodadas.map((r, i) => [i ? ' · ' : null, 'a rodada ', h('a', { href: `#/autorizacoes/${encodeURIComponent(r.id)}` }, r.titulo || r.id), ' está aberta']),
      rodadas.length && conflitos.length ? ' · ' : null,
      conflitos.length ? `${conflitos.length === 1 ? 'um pedido está' : `${conflitos.length} pedidos estão`} em conflito (veja em Pedidos, abaixo)` : null));
}

// ------------------------------------------------------------------ fluxo de nós (SVG)
// O fluxo lê de cima para baixo em faixas: botões e painéis; a cadeia dos scripts em colunas; logo abaixo de um nó, o
// trabalho humano que ele consulta no meio da volta (ex.: ambíguos); a pista das voltas ("repete"); e a faixa de
// madeira com o trabalho humano depois do laço. Toda linha que sobe ou desce passa pelo vão entre colunas, afastada
// do texto dos nós; cada palavra de seta foge de linhas e textos alheios. Nada de texto cortado com reticências.
const COL = 250, CX0 = 36, CAIXA = 64, R_DEC = 40, TOPO = 136, VAO_LINHA = 26, PX_14 = 7.5, PX_16 = 9;
const LIGA = new Set(['a', 'o', 'as', 'os', 'de', 'da', 'do', 'das', 'dos', 'no', 'na', 'nos', 'nas', 'em', 'por', 'para', 'com', 'que', 'e', 'ou', 'um', 'uma']);
function iconeDoNo(n) {
  if (n.papel === 'fora-dos-scripts') return 'pessoa';
  if (n.papel === 'observador') return 'olho';
  if (n.papel === 'controle') return 'botao';
  if (n.papel === 'decisao') return 'bifurca';
  const t = `${n.id} ${n.titulo}`.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  for (const [re, ic] of [[/plano/, 'plano'], [/despach/, 'placa'], [/gerador/, 'faisca'], [/junta/, 'funil'], [/confer/, 'conferir'], [/audit/, 'pesquisa'], [/sintese/, 'livro']]) if (re.test(t)) return ic;
  return 'caixa';
}
const faixaDe = n => n.papel === 'controle' || n.papel === 'observador' ? 'topo' : n.papel === 'fora-dos-scripts' ? 'fora' : 'meio';
const meiaLargura = n => n.papel === 'decisao' ? R_DEC : n.papel === 'controle' ? 28 : n.papel === 'observador' ? 28 : CAIXA / 2;

/** Camadas: o caminho mais longo pela cadeia de trabalho, sem as voltas (DFS na ordem do laco.json corta os ciclos). */
function camadas(ids, arestas) {
  const saem = new Map(ids.map(i => [i, []]));
  for (const a of arestas) saem.get(a.de)?.push(a.para);
  const estado = new Map(), aceitas = [];
  const visita = v => { estado.set(v, 1); for (const w of saem.get(v) || []) { if (estado.get(w) === 1) continue; aceitas.push([v, w]); if (!estado.get(w)) visita(w); } estado.set(v, 2); };
  for (const v of ids) if (!estado.get(v)) visita(v);
  const col = new Map(ids.map(i => [i, 0]));
  for (let k = 0; k < ids.length; k++) for (const [a, b] of aceitas) if (col.get(b) < col.get(a) + 1) col.set(b, col.get(a) + 1);
  return col;
}

// ---- o texto sob um nó: valor + palavra-chave que cabe inteira (o rótulo completo vai para a faixa e a gaveta)
/** Até duas linhas de no máximo `max` caracteres, quebrando entre palavras; null se não couber. */
function quebrar(texto, max = MAX_LINHA) {
  const linhas = [''];
  for (const p of texto.split(' ')) {
    const l = linhas[linhas.length - 1], novo = l ? `${l} ${p}` : p;
    if (novo.length <= max) linhas[linhas.length - 1] = novo;
    else { if (linhas.length === 2 || p.length > max) return null; linhas.push(p); }
  }
  return linhas;
}
/** A forma curta de um rótulo: até a primeira vírgula ou palavra de ligação ("pedidos, todas as ondas" → "pedidos"). */
function rotuloCurto(rotulo) {
  const r = [];
  for (const p of String(rotulo).split(',')[0].trim().split(/\s+/)) { if (r.length && LIGA.has(p.toLowerCase())) break; r.push(p); }
  return r.join(' ');
}
function numeroDoContador(ct) {
  const v = ct.valor;
  switch (ct.tipo) {
    case 'inteiro': return fmt(v, 0);
    case 'numero': return ct.escala === 'porcento' ? `${fmt(v * 100, 1)}%` : fmt(v, 2);
    case 'hora': return quando(v);
    case 'lista': return fmt(v.length, 0);
    case 'contagem': return fmt(Object.values(v).reduce((a, b) => a + b, 0), 0);
    default: return String(v);
  }
}
/** "1.684 tentativas", "onda 6" (rótulo de uma palavra no singular vem antes), "última chamada 21h11" (hora no fim). */
function comporContador(ct, rotulo) {
  const n = numeroDoContador(ct);
  if (ct.tipo === 'hora' || ct.tipo === 'texto' || (!rotulo.includes(' ') && !/s$/i.test(rotulo))) return `${rotulo} ${n}`;
  return `${n} ${rotulo}`;
}
function linhasDoContador(ct) {
  const curto = rotuloCurto(ct.rotulo);
  if (ct.ilegivel) return (quebrar(`${curto}: ilegível`) || ['ilegível']).map(t => ({ texto: t, classe: 'nl ilegivel' }));
  if (ct.valor === null || ct.valor === undefined) return (quebrar(`${curto}: sem valor`) || ['sem valor']).map(t => ({ texto: t, classe: 'nl' }));
  const cheio = comporContador(ct, ct.rotulo), breve = comporContador(ct, curto);
  const linhas = cheio.length <= MAX_LINHA ? [cheio] : breve.length <= MAX_LINHA ? [breve] : (quebrar(breve) || quebrar(cheio) || [numeroDoContador(ct)]);
  return linhas.map(t => ({ texto: t, classe: 'nl' }));
}
/** Uma série vira barrinhas mais o último valor e a palavra-chave ("▮▮▮▮ 21,7% novos"). */
function resumoDaSerie(ct) {
  const campo = [...(ct.campos || [])].reverse().find(c => ct.valor.every(v => typeof v[c] === 'number')) || null;
  if (!campo) return null;
  const vals = ct.valor.slice(-8).map(v => v[campo]);
  const ult = vals[vals.length - 1];
  const num = ult <= 1 && /taxa|fra|porc/.test(campo) ? `${fmt(ult * 100, 1)}%` : fmt(ult, 2);
  return { vals, texto: `${num} ${rotuloCurto(ct.rotulo)}` };
}
/** As linhas sob um nó (no máximo quatro): os contadores dele (até dois) e o primeiro botão, em petróleo. */
function linhasDoNo(laco, n) {
  const linhas = [];
  for (const ct of (laco.contadores || []).filter(c => c.no === n.id).slice(0, 2)) {
    if (ct.tipo === 'serie' && !ct.ilegivel && Array.isArray(ct.valor) && ct.valor.length) { const r = resumoDaSerie(ct); if (r) { linhas.push({ serie: r, texto: r.texto, classe: 'nl' }); continue; } }
    linhas.push(...linhasDoContador(ct));
  }
  const ctrls = (laco.controles || []).filter(c => c.no === n.id);
  if (ctrls.length) {
    const c = ctrls.find(x => x.tipo !== 'lista') || null;
    let texto;
    if (!c) texto = ctrls.length > 1 ? `${ctrls.length} botões` : '1 botão';
    else {
      const v = c.configurado.ilegivel ? 'ilegível' : valorEmPalavras(c, c.configurado.valor);
      const mais = ctrls.length > 1 ? ` +${ctrls.length - 1}` : '';
      texto = `${v}${mais}`.length <= MAX_LINHA - 2 ? `${v}${mais}` : (quebrar(v, MAX_LINHA - 2) || [v])[0] + mais;
    }
    linhas.push({ botao: true, texto, classe: c && c.configurado.ilegivel ? 'nl ilegivel' : 'nl botao' });
  }
  return linhas.slice(0, 4);
}
const larguraDaLinha = ln => ln.serie ? ln.serie.vals.length * 9 + 6 + ln.texto.length * PX_14 : (ln.botao ? 20 : 0) + ln.texto.length * PX_14;
function dicaDoNo(laco, n) {
  const partes = [PAPEL[n.papel]?.dica || n.papel];
  if (n.detalhe) partes.push(n.detalhe);
  for (const ct of (laco.contadores || []).filter(c => c.no === n.id)) partes.push(`${contadorEmPalavras(ct)}${ct.ilegivel ? ` (${ct.ilegivel})` : ct.hora ? ` (${quando(ct.hora)})` : ''}`);
  const nb = (laco.controles || []).filter(c => c.no === n.id).length;
  if (nb) partes.push(nb > 1 ? `${nb} botões que viram pedido` : '1 botão que vira pedido');
  partes.push('clique para abrir a gaveta');
  return partes.join(' · ');
}

function posicionar(laco) {
  const nos = laco.nos, porId = new Map(nos.map(n => [n.id, n]));
  const ligs = laco.ligacoes.filter(l => porId.has(l.de) && porId.has(l.para) && l.de !== l.para);
  const fx = id => faixaDe(porId.get(id));
  const textos = new Map(nos.map(n => [n.id, linhasDoNo(laco, n)]));
  // meia largura de um nó com o texto dele (as linhas que passam ao lado ficam fora disso)
  const meia = new Map(nos.map(n => [n.id, Math.max(meiaLargura(n), Math.max(n.titulo.length * PX_16, ...(n.papel === 'controle' || n.papel === 'observador' ? [0] : textos.get(n.id).map(larguraDaLinha))) / 2)]));
  const alturaAbaixo = id => meiaLargura(porId.get(id)) + 22 + textos.get(id).length * 20 + 8;
  // meio: etapas e decisões, em colunas pela cadeia
  const meio = nos.filter(n => fx(n.id) === 'meio').map(n => n.id);
  const colM = camadas(meio, ligs.filter(l => l.tipo !== 'repete' && fx(l.de) === 'meio' && fx(l.para) === 'meio'));
  const alvoDoTopo = new Set(ligs.filter(l => fx(l.de) === 'topo').map(l => l.para));
  const porColuna = new Map();
  for (const id of meio) { const c = colM.get(id); if (!porColuna.has(c)) porColuna.set(c, []); porColuna.get(c).push(id); }
  for (const lista of porColuna.values()) lista.sort((a, b) => (alvoDoTopo.has(b) - alvoDoTopo.has(a)) || meio.indexOf(a) - meio.indexOf(b));
  const linhasMeio = Math.max(1, ...[...porColuna.values()].map(l => l.length));
  const ROW = Math.max(150, ...meio.map(id => meiaLargura(porId.get(id)) + alturaAbaixo(id))) + 44;
  // fora dos scripts: grupos ligados entre si
  const fora = nos.filter(n => fx(n.id) === 'fora').map(n => n.id);
  const ligsFora = ligs.filter(l => fx(l.de) === 'fora' && fx(l.para) === 'fora');
  const grupoDe = new Map(); let nGrupos = 0;
  for (const id of fora) {
    if (grupoDe.has(id)) continue;
    const pilha = [id]; grupoDe.set(id, nGrupos);
    while (pilha.length) { const v = pilha.pop(); for (const l of ligsFora) { const w = l.de === v ? l.para : l.para === v ? l.de : null; if (w && !grupoDe.has(w)) { grupoDe.set(w, nGrupos); pilha.push(w); } } }
    nGrupos++;
  }
  const colunasMeio = Math.max(0, ...colM.values()) + 1;
  const consultas = new Map();   // id do trabalho humano → id do nó que o consulta no meio da volta
  const grupos = [];
  for (let k = 0; k < nGrupos; k++) {
    const ids = fora.filter(i => grupoDe.get(i) === k);
    const entra = ligs.filter(l => ids.includes(l.para) && fx(l.de) === 'meio').map(l => l.de);
    const sai = ligs.filter(l => ids.includes(l.de) && fx(l.para) === 'meio').map(l => l.para);
    const vizinhos = new Set([...entra, ...sai]);
    // um único trabalho humano que recebe de um nó e devolve ao mesmo nó: fica logo abaixo dele, dentro da volta
    if (ids.length === 1 && entra.length && sai.length && vizinhos.size === 1) { consultas.set(ids[0], entra[0]); continue; }
    const local = camadas(ids, ligsFora.filter(l => ids.includes(l.de)));
    const largura = Math.max(...local.values()) + 1;
    const ancoras = entra.length ? entra.map(id => colM.get(id)) : sai.map(id => colM.get(id));
    const ancora = ancoras.length ? Math.min(...ancoras) : 0;
    grupos.push({ ids, local, largura, ancora, inicio: ancora + largura > colunasMeio ? Math.max(0, colunasMeio - largura) : ancora });
  }
  grupos.sort((a, b) => a.ancora - b.ancora);
  const ocupadas = [], colF = new Map(), linhaF = new Map();
  for (const gr of grupos) {
    const cols = Array.from({ length: gr.largura }, (_, i) => gr.inicio + i);
    let r = 0; while (ocupadas[r] && cols.some(c => ocupadas[r].has(c))) r++;
    ocupadas[r] = ocupadas[r] || new Set(); cols.forEach(c => ocupadas[r].add(c));
    const porLocal = new Map();
    for (const id of gr.ids) { const c = gr.local.get(id); const i = porLocal.get(c) || 0; porLocal.set(c, i + 1); colF.set(id, gr.inicio + c); linhaF.set(id, r + i); }
  }
  const naFaixa = fora.filter(id => colF.has(id));
  const linhasFora = naFaixa.length ? Math.max(...naFaixa.map(id => linhaF.get(id))) + 1 : 0;
  const ROW_F = Math.max(0, ...naFaixa.map(id => CAIXA / 2 + alturaAbaixo(id))) + 30;
  const ROW_C = Math.max(0, ...[...consultas.keys()].map(id => CAIXA / 2 + alturaAbaixo(id))) + 28;
  // alturas das faixas
  const topo = nos.filter(n => fx(n.id) === 'topo');
  const yMeio = topo.length ? TOPO + 22 : 18;
  const xCol = c => CX0 + c * COL + COL / 2;
  const pos = new Map();
  for (const [c, lista] of porColuna) lista.forEach((id, i) => pos.set(id, { x: xCol(c), y: yMeio + 60 + (linhasMeio - lista.length) * ROW / 2 + i * ROW, faixa: 'meio', col: c }));
  const yConsulta = yMeio + linhasMeio * ROW;
  for (const [id, m] of consultas) pos.set(id, { x: pos.get(m).x, y: yConsulta + CAIXA / 2 + 4, faixa: 'consulta', col: colM.get(m), dono: m });
  const voltas = ligs.filter(l => fx(l.de) === 'meio' && fx(l.para) === 'meio' && (l.tipo === 'repete' || colM.get(l.para) <= colM.get(l.de))).length;
  const yVolta = yConsulta + (consultas.size ? ROW_C : 0) - 10;   // a pista das voltas
  const yFora = yVolta + (voltas ? 24 + voltas * 16 + 26 : 10);
  for (const id of naFaixa) pos.set(id, { x: xCol(colF.get(id)), y: yFora + 46 + CAIXA / 2 + linhaF.get(id) * ROW_F, faixa: 'fora', col: colF.get(id) });
  // topo: acima dos alvos (média), sem encostar um no outro; o texto fica à direita do ícone, e a largura é a dele
  const topoX = topo.map(n => {
    const alvos = ligs.filter(l => l.de === n.id && pos.has(l.para)).map(l => pos.get(l.para).x);
    const linhas = n.papel === 'observador' ? [n.carta ? 'só olha · abre o painel' : 'só olha'] : textos.get(n.id).slice(0, 3).map(ln => `${ln.botao ? '   ' : ''}${ln.serie ? '▮▮▮▮▮▮ ' : ''}${ln.texto}`);
    const larg = 46 + Math.max(n.titulo.length * PX_16, ...linhas.map(t => t.length * PX_14)) + 40;
    return { id: n.id, larg, x: alvos.length ? alvos.reduce((a, b) => a + b, 0) / alvos.length - 40 : xCol(0) };
  }).sort((a, b) => a.x - b.x);
  let minX = CX0 + 30;
  for (const t of topoX) { t.x = Math.max(t.x, minX); minX = t.x + t.larg; pos.set(t.id, { x: t.x, y: 18 + 46, faixa: 'topo', larg: t.larg }); }
  const colunas = Math.max(0, ...[...colM.values(), ...colF.values()]) + 1;
  const largura = Math.max(CX0 * 2 + colunas * COL, ...topoX.map(t => t.x + t.larg));
  const altura = (naFaixa.length ? yFora + 46 + linhasFora * ROW_F + 30 : yFora) + 8;
  return { pos, ligs, porId, colM, textos, meia, largura, altura, yMeio, yVolta, yFora, temTopo: !!topo.length, temFora: !!naFaixa.length, fx };
}

/** Caminho ortogonal com cantos arredondados. */
function ortogonal(p, raio = 12) {
  let d = `M${p[0][0]},${p[0][1]}`;
  for (let i = 1; i < p.length - 1; i++) {
    const [x0, y0] = p[i - 1], [x1, y1] = p[i], [x2, y2] = p[i + 1];
    const r = Math.min(raio, Math.hypot(x1 - x0, y1 - y0) / 2, Math.hypot(x2 - x1, y2 - y1) / 2);
    const a = [x1 - Math.sign(x1 - x0) * r, y1 - Math.sign(y1 - y0) * r], b = [x1 + Math.sign(x2 - x1) * r, y1 + Math.sign(y2 - y1) * r];
    d += ` L${a[0]},${a[1]} Q${x1},${y1} ${b[0]},${b[1]}`;
  }
  const f = p[p.length - 1];
  return d + ` L${f[0]},${f[1]}`;
}
const naCurva = (c, t) => { const m = 1 - t; return [0, 1].map(k => m * m * m * c[0][k] + 3 * m * m * t * c[1][k] + 3 * m * t * t * c[2][k] + t * t * t * c[3][k]); };
/** Pontos ao longo de uma seta (a cada ~4 px), para as palavras não pousarem em cima de uma linha alheia. */
function pontosDa(tr) {
  if (tr.curva) return Array.from({ length: 41 }, (_, i) => naCurva(tr.curva, i / 40));
  const pts = [];
  for (let i = 1; i < tr.orto.length; i++) {
    const [a, b] = [tr.orto[i - 1], tr.orto[i]]; const n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / 4));
    for (let k = 0; k <= n; k++) pts.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]);
  }
  return pts;
}

function quadroDoFluxo(app, u, laco) {
  const { h, svg, icone } = u;
  const L = posicionar(laco);
  const { pos, porId, meia } = L;
  const aberto = app.rota.params.get('no');
  const s = svg('svg', { class: 'fluxo', width: L.largura, height: L.altura, viewBox: `0 0 ${L.largura} ${L.altura}`, role: 'group', 'aria-label': `fluxo do laço ${laco.titulo}` });
  s.append(svg('defs', {},
    svg('marker', { id: 'lc-seta', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 8, markerHeight: 8, orient: 'auto-start-reverse' }, svg('path', { d: 'M0,0 L10,5 L0,10 z', class: 'ponta' })),
    svg('marker', { id: 'lc-seta-c', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 8, markerHeight: 8, orient: 'auto-start-reverse' }, svg('path', { d: 'M0,0 L10,5 L0,10 z', class: 'ponta-c' }))));
  // faixas: madeira do trabalho humano depois do laço (rótulo no rodapé: por cima chegam as setas)
  if (L.temFora) {
    const xs = laco.nos.filter(n => pos.get(n.id)?.faixa === 'fora').map(n => pos.get(n.id).x);
    const x1 = Math.max(8, Math.min(Math.min(...xs) - COL / 2 + 10, Math.max(...xs) + COL / 2 - 10 - 330)), x2 = Math.min(L.largura - 8, Math.max(...xs) + COL / 2 - 10);
    s.append(svg('rect', { class: 'faixa-fora', x: x1, y: L.yFora, width: x2 - x1, height: L.altura - L.yFora - 8, rx: 16 }));
    const yr = L.altura - 8 - 16;
    const g = svg('g', { class: 'faixa-rot fora' }); const ic = icone('pessoa'); ic.setAttribute('x', x1 + 14); ic.setAttribute('y', yr - 14); ic.setAttribute('width', 18); ic.setAttribute('height', 18);
    g.append(ic, svg('text', { x: x1 + 38, y: yr }, 'fora dos scripts · o maestro conduz'));
    s.append(g);
  }
  if (L.temTopo) s.append(svg('line', { class: 'sep-topo', x1: 14, x2: L.largura - 14, y1: L.yMeio - 6, y2: L.yMeio - 6 }));
  // nós humanos consultados no meio da volta: um tom de madeira sob eles, para a separação semântica
  for (const n of laco.nos) { const p = pos.get(n.id); if (p?.faixa === 'consulta') s.append(svg('rect', { class: 'faixa-fora consulta', x: p.x - Math.max(70, meia.get(n.id) + 8), y: p.y - CAIXA / 2 - 12, width: 2 * Math.max(70, meia.get(n.id) + 8), height: CAIXA + 22 + L.textos.get(n.id).length * 20 + 30, rx: 14 })); }

  // ligações: primeiro as voltas, depois as que descem para o trabalho humano (assim os vãos ficam em ordem)
  const porta = (id, lado, dy = 0) => { const p = pos.get(id), m = meiaLargura(porId.get(id)); return lado === 'esq' ? [p.x - m, p.y + dy] : lado === 'dir' ? [p.x + m, p.y + dy] : lado === 'cima' ? [p.x, p.y - m] : [p.x, p.y + m]; };
  const saidas = new Map(), entradas = new Map(); let pistas = 0;
  const vaoDir = id => { const k = saidas.get(id) || 0; saidas.set(id, k + 1); return pos.get(id).x + meia.get(id) + 18 + k * VAO_LINHA; };
  const vaoEsq = id => { const k = entradas.get(id) || 0; entradas.set(id, k + 1); return pos.get(id).x - meia.get(id) - 18 - k * VAO_LINHA; };
  const ehVolta = l => { const A = pos.get(l.de), B = pos.get(l.para); return A && B && A.faixa === 'meio' && B.faixa === 'meio' && (l.tipo === 'repete' || B.col <= A.col); };
  const ordem = [...L.ligs].sort((a, b) => (ehVolta(b) - ehVolta(a)) || ((pos.get(a.para)?.faixa === 'fora') - (pos.get(b.para)?.faixa === 'fora')));
  const tracos = [];
  for (const l of ordem) {
    if (!pos.has(l.de) || !pos.has(l.para)) continue;
    const A = pos.get(l.de), B = pos.get(l.para);
    const curva = (p0, p1, p2, p3) => ({ d: `M${p0[0]},${p0[1]} C${p1[0]},${p1[1]} ${p2[0]},${p2[1]} ${p3[0]},${p3[1]}`, curva: [p0, p1, p2, p3] });
    const orto = (pts, meio) => ({ d: ortogonal(pts), orto: pts, meio });
    let t;
    if (A.faixa === 'topo') {
      const [x1, y1] = porta(l.de, 'baixo'); const [x2, y2] = porta(l.para, 'cima'); const ym = (y1 + y2) / 2;
      t = curva([x1, y1], [x1, ym], [x2, ym], [x2, y2 - 2]);
    } else if (A.faixa === 'meio' && B.faixa === 'meio' && !ehVolta(l)) {
      const [x1, y1] = porta(l.de, 'dir'); const [x2, y2] = porta(l.para, 'esq'); const dx = Math.max(40, (x2 - x1) / 2);
      t = curva([x1, y1], [x1 + dx, y1], [x2 - dx, y2], [x2 - 2, y2]);
    } else if (ehVolta(l)) {
      // volta: sai pela direita, desce pelo vão até a pista própria, corre por baixo de tudo e sobe pelo vão à esquerda
      // do alvo, entrando pelo lado dele abaixo da porta
      const [x1, y1] = porta(l.de, 'dir'); const [x2, y2] = porta(l.para, 'esq', 20);
      const xs = vaoDir(l.de), xe = vaoEsq(l.para), yv = L.yVolta + 24 + (pistas++) * 16;
      t = orto([[x1, y1], [xs, y1], [xs, yv], [xe, yv], [xe, y2], [x2 - 2, y2]], [(xs + xe) / 2, yv]);
    } else if (A.faixa === 'meio' && B.faixa === 'consulta') {
      // consulta: desce pelo vão à direita e entra pelo lado direito do trabalho humano
      const [x1, y1] = porta(l.de, 'dir'); const [x2, y2] = porta(l.para, 'dir');
      const xs = vaoDir(l.de);
      t = orto([[x1, y1], [xs, y1], [xs, y2], [x2 + 2, y2]], [xs, (y1 + y2) / 2]);
    } else if (A.faixa === 'consulta' && B.faixa === 'meio') {
      // devolve: sai pela esquerda, sobe pelo vão à esquerda e entra pelo lado do nó, abaixo da porta
      const [x1, y1] = porta(l.de, 'esq'); const [x2, y2] = porta(l.para, 'esq', 20);
      const xe = vaoEsq(l.para);
      t = orto([[x1, y1], [xe, y1], [xe, y2], [x2 - 2, y2]], [xe, (y1 + y2) / 2]);
    } else if (A.faixa === 'meio' && B.faixa === 'fora') {
      // para o trabalho humano depois do laço: desce pelo vão à direita (por fora das voltas) e entra por cima
      const [x1, y1] = porta(l.de, 'dir'); const [x2, y2] = porta(l.para, 'cima');
      const xs = vaoDir(l.de), yb = y2 - 24;
      t = orto([[x1, y1], [xs, y1], [xs, yb], [x2, yb], [x2, y2 - 2]], [xs, (L.yVolta + L.yFora) / 2 + 20]);
    } else if (A.faixa === 'fora' && B.faixa === 'meio') {
      const [x1, y1] = porta(l.de, 'esq'); const [x2, y2] = porta(l.para, 'esq', 20);
      const xe = Math.min(vaoEsq(l.para), x1 - 20);
      t = orto([[x1, y1], [xe, y1], [xe, y2], [x2 - 2, y2]], [xe, (y1 + y2) / 2]);
    } else {
      const dir = B.x >= A.x;
      const [x1, y1] = porta(l.de, dir ? 'dir' : 'esq'); const [x2, y2] = porta(l.para, dir ? 'esq' : 'dir');
      const dx = Math.max(40, Math.abs(x2 - x1) / 2) * (dir ? 1 : -1);
      t = curva([x1, y1], [x1 + dx, y1], [x2 - dx, y2], [x2, y2]);
    }
    tracos.push({ l, ...t });
    s.append(svg('path', { class: `lig t-${l.tipo}`, d: t.d, 'marker-end': l.tipo === 'observa' ? null : (l.tipo === 'condiciona' ? 'url(#lc-seta-c)' : 'url(#lc-seta)') }));
    if (l.tipo === 'observa') { const [x2, y2] = porta(l.para, 'cima'); s.append(svg('circle', { class: 'fim-observa', cx: x2, cy: y2 - 3, r: 3.5 })); }
  }
  // nós (e as áreas que ocupam: caixa + texto, e o envelope de pedido)
  const ocupado = [];
  for (const n of laco.nos) {
    const p = pos.get(n.id); if (!p) continue;
    const { g, areas } = desenharNo(app, u, laco, n, p, n.id === aberto, L);
    s.append(g); ocupado.push(...areas);
  }
  // palavras das setas: numa pílula que desliza pela própria seta até não tocar linha, texto ou outra pílula
  const pontos = tracos.map(pontosDa);
  const colide = (r, i) => ocupado.some(q => r.x < q.x + q.w && q.x < r.x + r.w && r.y < q.y + q.h && q.y < r.y + r.h)
    || pontos.some((ps, j) => j !== i && ps.some(([x, y]) => x > r.x - 5 && x < r.x + r.w + 5 && y > r.y - 5 && y < r.y + r.h + 5));
  tracos.forEach((tr, i) => {
    const l = tr.l;
    const larg = Math.max(44, String(l.palavra).length * 8.2 + 22 + (l.tipo === 'repete' ? 18 : 0));
    const ret = ([x, y]) => ({ x: x - larg / 2, y: y - 13, w: larg, h: 26, cx: x, cy: y });
    let candidatos;
    if (tr.curva) candidatos = [0.5, 0.42, 0.58, 0.34, 0.66, 0.27, 0.73, 0.2, 0.8].map(t => naCurva(tr.curva, t));
    else {
      const [mx, my] = tr.meio; candidatos = [[mx, my]];
      const trechos = [];
      for (let k = 1; k < tr.orto.length; k++) trechos.push([tr.orto[k - 1], tr.orto[k]]);
      trechos.sort((a, b) => Math.hypot(b[1][0] - b[0][0], b[1][1] - b[0][1]) - Math.hypot(a[1][0] - a[0][0], a[1][1] - a[0][1]));
      for (const [a, b] of trechos) for (const f of [0.5, 0.35, 0.65, 0.2, 0.8]) candidatos.push([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]);
    }
    const r = candidatos.map(ret).find(x => !colide(x, i)) || ret(candidatos[0]);
    ocupado.push(r);
    const g = svg('g', { class: `rotulo-lig t-${l.tipo}`, tabindex: 0, 'data-dica-titulo': `${porId.get(l.de).titulo} → ${porId.get(l.para).titulo}`, 'data-dica': `“${l.palavra}”: ${LIGACAO[l.tipo] || l.tipo}` });
    g.append(svg('rect', { x: r.x, y: r.y, width: r.w, height: r.h, rx: 13 }));
    if (l.tipo === 'repete') { const ic = icone('laco'); ic.setAttribute('x', r.x + 8); ic.setAttribute('y', r.cy - 8); ic.setAttribute('width', 16); ic.setAttribute('height', 16); g.append(ic); }
    g.append(svg('text', { x: r.cx + (l.tipo === 'repete' ? 9 : 0), y: r.cy + 5, 'text-anchor': 'middle' }, l.palavra));
    s.append(g);
  });
  const legenda = h('div.legenda-fluxo',
    h('span', h('i.lg-etapa'), 'etapa'), h('span', h('i.lg-decisao'), 'decide'), h('span', h('i.lg-botao'), 'botão'), h('span', h('i.lg-painel'), 'painel: só olha'), h('span', h('i.lg-fora'), 'fora dos scripts'),
    h('span', h('i.lg-linha.seg'), 'segue'), h('span', h('i.lg-linha.rep'), 'repete'), h('span', h('i.lg-linha.cond'), 'condiciona'), h('span', h('i.lg-linha.obs'), 'observa'),
    h('span.c-ambar', icone('envelope'), 'pedido aberto'));
  // quando o fluxo não cabe (1280 px), ele rola dentro do quadro: a borda direita esmaece e um selo diz "rola →"
  const rolagem = h('div.fluxo-rolagem', s);
  const moldura = h('div.fluxo-moldura', rolagem, h('span.rola-aviso', { 'aria-hidden': 'true' }, 'rola →'));
  const medir = () => { if (!rolagem.isConnected) return; const sobra = rolagem.scrollWidth - rolagem.clientWidth; moldura.classList.toggle('transborda', sobra > 2); moldura.classList.toggle('no-fim', rolagem.scrollLeft >= sobra - 2); };
  rolagem.addEventListener('scroll', medir, { passive: true });
  requestAnimationFrame(medir); setTimeout(medir, 300);
  return h('section.quadro-fluxo', { 'aria-label': 'fluxo de nós' }, moldura, legenda);
}

function textoSvg(u, x, y, texto, classe, ancora = 'middle') { return u.svg('text', { x, y, class: classe, 'text-anchor': ancora }, texto); }

/** Desenha um nó; devolve o grupo SVG e as áreas que ele ocupa (para as palavras das setas não pousarem nele). */
function desenharNo(app, u, laco, n, p, aberto, L) {
  const { svg, icone } = u;
  const g = svg('g', { class: `no p-${n.papel}${aberto ? ' aberto' : ''}`, tabindex: 0, role: 'button', 'aria-label': `${n.titulo}, ${PAPEL[n.papel]?.palavra || n.papel}: abrir a gaveta`, 'data-foco': `no-${n.id}`, 'data-dica-titulo': `${n.titulo} · ${PAPEL[n.papel]?.palavra || n.papel}`, 'data-dica': dicaDoNo(laco, n), 'data-dica-sem-clique': '1' });
  g.addEventListener('click', () => abrirNo(laco.id, n.id));
  g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrirNo(laco.id, n.id); } });
  const { x, y } = p;
  const ic = (nome, tam, cx = x, cy = y, classe = 'ico') => { const el = icone(nome); el.setAttribute('x', cx - tam / 2); el.setAttribute('y', cy - tam / 2); el.setAttribute('width', tam); el.setAttribute('height', tam); el.setAttribute('class', classe); return el; };
  const linhas = L.textos.get(n.id);
  const m = meiaLargura(n);
  const areas = [];
  if (n.papel === 'controle' || n.papel === 'observador') {
    // faixa de cima: ícone à esquerda, texto à direita (a linha sai por baixo do ícone, longe do texto)
    if (n.papel === 'controle') {
      g.append(svg('circle', { class: 'anel', cx: x, cy: y, r: 37 }));
      for (let i = 0; i < 11; i++) { const a = (-225 + i * 27) * Math.PI / 180; g.append(svg('line', { class: 'marca', x1: x + Math.cos(a) * 31, y1: y + Math.sin(a) * 31, x2: x + Math.cos(a) * 35, y2: y + Math.sin(a) * 35 })); }
      g.append(svg('circle', { class: 'aro', cx: x, cy: y, r: 27 }), svg('circle', { class: 'miolo', cx: x, cy: y, r: 18 }), svg('line', { class: 'ponteiro', x1: x, y1: y, x2: x - 10, y2: y - 10 }));
    } else {
      g.append(svg('rect', { class: 'anel', x: x - 36, y: y - 36, width: 72, height: 72, rx: 18 }));
      g.append(svg('rect', { class: 'caixa', x: x - 28, y: y - 28, width: 56, height: 56, rx: 14 }), ic('olho', 28));
    }
    g.append(textoSvg(u, x + 46, y - 12, n.titulo, 'nt', 'start'));
    const sub = n.papel === 'observador' ? [{ texto: n.carta ? 'só olha · abre o painel' : 'só olha', classe: 'nl painel' }] : linhas.slice(0, 3);
    sub.forEach((ln, i) => {
      const yy = y + 12 + i * 20;
      if (ln.serie) { desenharSerie(u, g, ln.serie, x + 46, yy - 15, 'start'); return; }
      if (ln.botao) g.append(ic('botao', 15, x + 53, yy - 5, 'ico botao'));
      g.append(textoSvg(u, ln.botao ? x + 65 : x + 46, yy, ln.texto, ln.classe, 'start'));
    });
    areas.push({ x: x - 38, y: y - 38, w: (p.larg || 220) - 10, h: 76 + Math.max(0, sub.length - 2) * 20 });
  } else {
    if (n.papel === 'decisao') {
      g.append(svg('rect', { class: 'anel', x: x - 46, y: y - 46, width: 92, height: 92, rx: 18 }));
      g.append(svg('path', { class: 'caixa', d: `M${x},${y - R_DEC} L${x + R_DEC},${y} L${x},${y + R_DEC} L${x - R_DEC},${y} Z` }), ic('bifurca', 26));
    } else {
      g.append(svg('rect', { class: 'anel', x: x - 40, y: y - 40, width: 80, height: 80, rx: 20 }));
      g.append(svg('rect', { class: 'caixa', x: x - CAIXA / 2, y: y - CAIXA / 2, width: CAIXA, height: CAIXA, rx: 15 }), ic(iconeDoNo(n), 30));
    }
    g.append(svg('circle', { class: 'porta', cx: x - m, cy: y, r: 4.5 }), svg('circle', { class: 'porta', cx: x + m, cy: y, r: 4.5 }));
    const y0 = y + m + 22;
    g.append(textoSvg(u, x, y0, n.titulo, 'nt'));
    linhas.forEach((ln, i) => {
      const yy = y0 + 22 + i * 20;
      if (ln.serie) { desenharSerie(u, g, ln.serie, x, yy - 15, 'middle'); return; }
      if (ln.botao) {
        const larg = ln.texto.length * PX_14;
        g.append(ic('botao', 15, x - larg / 2 - 4, yy - 5, 'ico botao'));
        g.append(textoSvg(u, x + 9, yy, ln.texto, ln.classe));
        return;
      }
      g.append(textoSvg(u, x, yy, ln.texto, ln.classe));
    });
    const mw = L.meia.get(n.id);
    areas.push({ x: x - mw, y: y - m - 4, w: 2 * mw, h: m * 2 + 22 + linhas.length * 20 + 14 });
  }
  // a área inteira do nó (ícone e texto) responde ao clique, inclusive os vãos entre as linhas
  const a0 = areas[0];
  g.insertBefore(svg('rect', { class: 'alvo', x: a0.x, y: a0.y, width: a0.w, height: a0.h, rx: 12 }), g.firstChild);
  // envelope de pedido aberto (terracota tracejado), acima do nó e sem encostar nele; conflito atual: cheio, com "!"
  const meus = (laco.pedidos || []).filter(q => q.atual && q.no === n.id && !q.substituido_por);
  const conflito = meus.some(q => q.estado === 'conflito');
  const abertos = meus.filter(q => q.trabalho_pendente).length;
  if (conflito || abertos) {
    const larg = abertos > 1 || conflito ? 46 : 32;
    const topoNo = n.papel === 'controle' ? 37 : n.papel === 'observador' ? 36 : n.papel === 'decisao' ? 46 : 40;
    const bx = x + 12, by = y - topoNo - 10 - 24;
    const env = svg('g', { class: `envelope-no${conflito ? ' conflito' : ''}` });
    env.append(svg('rect', { x: bx, y: by, width: larg, height: 24, rx: 7 }));
    const e = icone('envelope'); e.setAttribute('x', bx + 7); e.setAttribute('y', by + 4); e.setAttribute('width', 18); e.setAttribute('height', 16); env.append(e);
    if (conflito) env.append(svg('text', { x: bx + 34, y: by + 17, 'text-anchor': 'middle' }, '!'));
    else if (abertos > 1) env.append(svg('text', { x: bx + 34, y: by + 17, 'text-anchor': 'middle' }, String(abertos)));
    g.append(env);
    areas.push({ x: bx - 2, y: by - 2, w: larg + 4, h: 28 });
  }
  return { g, areas };
}
/** Barrinhas de uma série (ex.: novos por onda) e, ao lado, o último valor com a palavra-chave. */
function desenharSerie(u, g, r, x, y, ancora) {
  const { svg } = u;
  const max = Math.max(...r.vals, 1e-9);
  const larg = r.vals.length * 9, total = larg + 6 + r.texto.length * PX_14, x0 = ancora === 'middle' ? x - total / 2 : x;
  r.vals.forEach((v, i) => { const hb = Math.max(2, 16 * v / max); g.append(svg('rect', { class: 'barra-serie', x: x0 + i * 9, y: y + 16 - hb, width: 6, height: hb, rx: 1 })); });
  g.append(textoSvg(u, x0 + larg + 6, y + 15, r.texto, 'nl', 'start'));
}

// ------------------------------------------------------------------ pedir parada, pausa, retomada (cabeçalho do laço)
function painelDeParada(app, u, laco) {
  const { h, icone } = u;
  const r = rascunhoDo(app, laco);
  const d = r.parada;
  const kForm = `parada:${laco.id}:${laco.execucao.id}`;
  const caps = new Map((laco.capacidades || []).map(c => [c.id, c]));
  const ops = [];
  if (d.operacao === 'pedir-parada') { for (const id of ['parar-apos-onda', 'parar-de-despachar']) if (caps.has(id)) ops.push(id); }
  if (!d.capacidade || !ops.includes(d.capacidade)) d.capacidade = ops[0] || null;
  const apos = caps.get('parar-apos-onda');
  if (d.onda === undefined) d.onda = apos && Number.isInteger(apos.onda_atual) ? apos.onda_atual : '';
  if (!d.envio) d.envio = crypto.randomUUID();
  if (!d.substituiDecidido && 'substitui' in d) delete d.substitui;
  if (d.alvoVisto === undefined) d.alvoVisto = alvoDaSubstituicao(laco, d, CASA_PARADA)?.arquivo || null;
  const form = h('form.painel-parada', { novalidate: true, onsubmit: e => e.preventDefault(), dataset: { preservar: `${kForm}:${d.operacao}:${geracao(kForm)}` } });
  const titulo = { 'pedir-parada': 'Pedir parada', 'pedir-pausa': 'Pedir pausa', 'pedir-retomada': 'Pedir retomada' }[d.operacao];
  const salvar = () => guardar(app, laco);
  form.append(h('div.painel-parada-cabeca', icone(d.operacao === 'pedir-pausa' ? 'pausa' : d.operacao === 'pedir-retomada' ? 'retomar' : 'parar'), h('strong', titulo), h('span.dica-inline', '· vira um pedido ao maestro; nada para agora'),
    h('button.fechar', { type: 'button', 'aria-label': 'Fechar sem pedir', onclick: () => { r.parada = null; salvar(); novaGeracao(kForm); redesenhar(); } }, icone('fechar'))));
  if (d.operacao === 'pedir-parada') {
    const grupo = h('div.opcoes-parada', { role: 'radiogroup', 'aria-label': 'como parar' });
    for (const id of ops) {
      const inp = h('input', { type: 'radio', name: `cap-${laco.id}`, value: id, checked: d.capacidade === id || null, dataset: { foco: `cap-${id}` }, onchange: () => { d.capacidade = id; salvar(); } });
      const extra = id === 'parar-apos-onda' ? h('span.onda-alvo', 'depois da onda ', h('input.numero-onda', { type: 'number', min: String(apos.onda_atual || 1), step: '1', value: d.onda === '' ? '' : String(d.onda), 'aria-label': 'número da onda', dataset: { foco: 'onda-alvo' }, oninput: ev => { d.onda = ev.target.value === '' ? '' : Number(ev.target.value); d.capacidade = id; inp.checked = true; salvar(); } }),
        apos.onda_atual != null ? h('span.dica-inline', ` (em curso: ${apos.onda_atual})`) : h('span.dica-inline.c-coral', ' (onda em curso ilegível: diga qual)')) : null;
      grupo.append(h('label.opcao-parada', inp, h('span.texto', h('strong', CAPACIDADE[id].titulo), extra, h('span.dica-inline', CAPACIDADE[id].dica))));
    }
    form.append(grupo);
  } else {
    form.append(h('p.dica-inline', d.operacao === 'pedir-pausa' ? 'Pausa no mesmo ponto, na mesma execução; o maestro confere antes de qualquer efeito.' : 'Retomada da mesma execução pausada; o maestro confere se ela está pausada. Recebido não quer dizer retomado.'));
  }
  const area = h('textarea', { 'aria-label': 'por quê (opcional)', placeholder: 'por quê (opcional)', maxlength: '20000', dataset: { foco: 'parada-texto' }, oninput: ev => { d.texto = ev.target.value; salvar(); } });
  area.value = d.texto || '';
  const erro = h('div.erro-acao', { role: 'alert' });
  const enviar = h('button.botao.primario', { type: 'button', dataset: { foco: 'parada-enviar' } }, icone('envelope'), d.emVoo ? 'Tentar de novo' : 'Pedir ao maestro');
  form.append(area, h('div.nota-cota', icone('alerta'), 'até valer, chamadas em voo ainda gastam cota'), h('div.rodape-acao', enviar, erro));
  if (d.emVoo) erro.textContent = `Envio pendente (${d.emVoo.motivo}). "Tentar de novo" reenvia o mesmo pedido, com o mesmo envio.`;
  enviar.onclick = () => enviarPedido(app, u, laco, d, {
    decidir: () => precisaDecidir(laco, d, CASA_PARADA),
    aoRecuperar: async alvo => {
      d.recuperar = { alvo: alvo || d.recuperar?.alvo || (d.substituiDecidido ? d.substitui : (d.alvoVisto || null)) };
      salvar(); await atualizar(true); redesenhar();
      setTimeout(() => document.querySelector('[data-foco^="rec-parada-"]')?.focus({ preventScroll: true }), 60);
    },
    montar: () => {
      const corpo = { envio: d.envio, tipo: 'alteracao-laco', laco: laco.id, execucao: laco.execucao.id, operacao: d.operacao, revisao: lacoAtual(laco).revisao };
      if (d.operacao === 'pedir-parada') {
        if (!d.capacidade) return { erro: 'Escolha como parar.' };
        corpo.capacidade = d.capacidade;
        if (d.capacidade === 'parar-apos-onda') {
          if (!Number.isInteger(d.onda) || d.onda < 1) return { erro: 'Diga depois de qual onda (um número inteiro).' };
          if (apos.onda_atual != null && d.onda < apos.onda_atual) return { erro: `A onda ${d.onda} já passou; a onda em curso é ${apos.onda_atual}.` };
          corpo.onda = d.onda;
        }
      }
      const t = (d.texto || '').trim(); if (t) corpo.texto = t;
      const alvo = alvoDaSubstituicao(laco, d, CASA_PARADA);
      if (alvo) corpo.substitui = alvo.arquivo;
      return { corpo };
    },
    erro, botao: enviar, rotulo: 'Pedir ao maestro',
    concluir: () => { r.parada = null; guardar(app, laco); novaGeracao(kForm); u.brisa(`${titulo}: gravado na caixa. O maestro dá o desfecho.`, 'verde'); },
  });
  // fora do formulário preservado: refeitos a cada atualização, sobre o estado atual dos pedidos
  const fora = precisaDecidir(laco, d, CASA_PARADA) ? blocoDeRecuperacao(u, laco, d, CASA_PARADA, alvo => escolherSubstituicao(app, laco, d, alvo, 'parada-enviar'), 'rec-parada') : notaDeSubstituicao(u, laco, d, CASA_PARADA);
  return fora ? [fora, form] : form;
}

// ------------------------------------------------------------------ envio de um pedido (o mesmo fluxo do Responder)
/** Grava um pedido na caixa. Erro ambíguo (rede, 5xx): guarda o corpo em `emVoo` e "tentar de novo" manda o mesmo par
 *  (envio, corpo). 400/409 viram mensagem em palavras; o 409 de revisão mostra "você viu / agora está / você pediu". */
async function enviarPedido(app, u, laco, d, op) {
  const { h, icone } = u;
  let corpo;
  if (d.emVoo) corpo = d.emVoo.corpo; // erro ambíguo: o mesmo par (envio, corpo), sem reler nem recalcular nada
  else {
    await buscarDetalhe(laco.id);     // o alvo de `substitui` é calculado sobre o laço de agora, não o do desenho
    if (op.decidir && op.decidir()) { await op.aoRecuperar(null); return; }
    const m = op.montar();
    if (m.erro) { op.erro.textContent = m.erro; return; }
    corpo = m.corpo;
  }
  op.botao.disabled = true; op.erro.textContent = '';
  // o formulário renasce depois do envio: o foco volta ao botão de mesmo papel no formulário novo
  const chaveBotao = op.botao.dataset.foco;
  const devolverFoco = () => { if (!document.activeElement || document.activeElement === document.body) document.querySelector(`[data-foco="${CSS.escape(chaveBotao)}"]`)?.focus({ preventScroll: true }); };
  try {
    await api.caixa(corpo);
    d.emVoo = null; d.conflito = null;
    op.concluir();
    await atualizar(true);
    devolverFoco();
  } catch (e) {
    op.botao.disabled = false;
    if (!e.status || e.status >= 500) {
      d.emVoo = { corpo, motivo: e.message }; guardar(app, laco);
      op.erro.textContent = `Não deu para confirmar a gravação (${e.message}). "Tentar de novo" reenvia o mesmo pedido, com o mesmo envio.`;
      op.botao.replaceChildren(icone('envelope'), 'Tentar de novo');
    } else if (e.status === 409 && e.corpo?.erro === 'envio-conflito') {
      try { await api.caixaItem(corpo.envio); d.emVoo = null; op.concluir(); await atualizar(true); devolverFoco(); return; }
      catch { op.erro.textContent = 'A torre diz que este envio já existe com outro conteúdo, mas não deu para relê-lo. Recarregue a página e confira os pedidos.'; }
    } else {
      d.emVoo = null; guardar(app, laco);
      op.botao.replaceChildren(icone('envelope'), op.rotulo);
      if (e.corpo?.erro === 'substitui-invalido' && op.aoRecuperar) { await op.aoRecuperar(corpo.substitui || null); return; }
      op.erro.replaceChildren(...mensagemDeRecusa(u, laco, e, op.controle));
      if (e.corpo?.conflito) { d.conflito = e.corpo.conflito; guardar(app, laco); op.erro.append(op.aoConflito ? op.aoConflito(e.corpo.conflito) : ''); }
    }
    op.botao.focus();
  }
}
// os 400 mais prováveis em palavras (o navegador só manda ids; a torre confere tudo contra o laco.json atual)
const RECUSA = {
  'capacidade-ausente': 'o laço não declara (mais) essa forma de parar ou pausar',
  'onda-invalida': 'essa onda já passou ou não é um número inteiro',
  'nada-muda': 'o valor pedido é igual ao configurado',
  'valor-invalido': 'o valor pedido não cabe na regra do botão (faixa, opções ou itens)',
  'tipo-errado': 'o tipo do valor não é o do botão',
  'controle-inexistente': 'esse botão não existe mais no laço',
  'no-inexistente': 'esse nó não existe mais no laço',
  'no-invalido': 'o botão não pertence mais a esse nó',
  'substitui-invalido': 'o pedido anterior já teve desfecho ou já foi substituído; envie sem substituir',
  'texto-obrigatorio': 'o comentário precisa de texto',
  'texto-longo': 'o texto passa de 20 000 caracteres',
  'laco-malformado': 'a descrição do laço está fora do contrato; o maestro precisa corrigi-la',
};
const CAMPO = { revisao: 'a revisão vista', antes: 'o valor que você viu', depois: 'o valor pedido', 'depois.valor': 'o valor pedido', onda: 'a onda', texto: 'o texto', capacidade: 'a forma de parar', execucao: 'a execução', laco: 'o laço', no: 'o nó', controle: 'o botão', substitui: 'o pedido substituído', operacao: 'a operação' };
/** 400 e 409 do POST em palavras. */
function mensagemDeRecusa(u, laco, e, controle) {
  const { h } = u;
  const c = e.corpo || {};
  if (e.status === 409 && c.erro === 'laco-mudou' && c.conflito) {
    const cf = c.conflito;
    const regra = cf.definicao_mudou === true ? 'A regra deste botão mudou (tipo, faixa ou opções): o pedido não cabe mais nela.'
      : cf.definicao_mudou === null ? 'A configuração ou a regra do laço mudou; o portal não sabe qual.'
      : 'O valor configurado mudou depois que você o viu.';
    return [h('div.conflito-tri',
      h('div', h('small', 'você viu'), h('b', tipadoEmPalavras(controle, cf.viu))),
      h('div.agora', h('small', 'agora está'), h('b', tipadoEmPalavras(controle, cf.agora))),
      h('div.pediu', h('small', 'você pediu'), h('b', tipadoEmPalavras(controle, cf.pediu)))),
      h('p.conflito-texto', h('strong', 'Nada foi gravado. '), regra, ' O rascunho ficou guardado.')];
  }
  if (e.status === 409 && c.erro === 'execucao-mudou') return [h('p', h('strong', 'A execução mudou. '), 'O laço partiu de novo; um pedido nunca passa sozinho para a execução seguinte. Nada foi gravado.')];
  if (e.status === 409 && c.erro === 'laco-terminou') return [h('p', h('strong', 'O laço terminou. '), 'Agora só comentário é aceito. Nada foi gravado.')];
  if (e.status === 409 && c.erro === 'configurado-ilegivel') return [h('p', h('strong', 'O valor configurado não pôde ser lido. '), `${c.mensagem || ''}. Nada foi gravado.`)];
  if (e.status === 409) return [h('p', h('strong', 'Conflito: '), `${c.mensagem || e.message}. Nada foi gravado.`)];
  const dica = RECUSA[c.erro];
  return [h('p', h('strong', 'A torre recusou: '), dica || `${c.mensagem || e.message}${c.campo ? ` (${CAMPO[c.campo] || c.campo})` : ''}`, '. Nada foi gravado.')];
}

// ------------------------------------------------------------------ comentários (nó e laço)
function formularioDeComentario(app, u, laco, { chave, d, garantir, operacao, no, rotulo, placeholder }) {
  const { h, icone } = u;
  const kForm = `${chave}:${geracao(chave)}`;
  const form = h('form.comentario-form', { novalidate: true, onsubmit: e => e.preventDefault(), dataset: { preservar: kForm } });
  const contagem = h('span.contagem');
  const area = h('textarea', { 'aria-label': rotulo, placeholder, maxlength: '20000', dataset: { foco: `${chave}-texto` },
    oninput: ev => { const dd = garantir(); dd.texto = ev.target.value; contagem.textContent = dd.texto ? `${dd.texto.length} / 20000` : ''; guardar(app, laco); } });
  area.value = d?.texto || '';
  contagem.textContent = d?.texto ? `${d.texto.length} / 20000` : '';
  const erro = h('div.erro-acao', { role: 'alert' });
  const enviar = h('button.botao.primario', { type: 'button', dataset: { foco: `${chave}-enviar` } }, icone('balao'), d?.emVoo ? 'Tentar de novo' : 'Enviar comentário');
  if (d?.emVoo) erro.textContent = `Envio pendente (${d.emVoo.motivo}). "Tentar de novo" reenvia o mesmo comentário, com o mesmo envio.`;
  enviar.onclick = () => {
    const dd = garantir();
    enviarPedido(app, u, laco, dd, {
      montar: () => {
        const t = (dd.texto || '').trim();
        if (!t) return { erro: 'Escreva o comentário antes de enviar.' };
        const corpo = { envio: dd.envio, tipo: 'alteracao-laco', laco: laco.id, execucao: laco.execucao.id, operacao, revisao: laco.revisao, texto: t };
        if (no) corpo.no = no;
        return { corpo };
      },
      erro, botao: enviar, rotulo: 'Enviar comentário',
      concluir: () => { dd.apagar(); guardar(app, laco); novaGeracao(chave); u.brisa('Comentário gravado na caixa. O maestro lê e absorve no ticket.', 'verde'); },
    });
  };
  form.append(area, h('div.rodape-acao', enviar, contagem), erro);
  return form;
}
function comentarioDoLaco(app, u, laco) {
  const { h, icone } = u;
  const r = rascunhoDo(app, laco);
  const garantir = () => { if (!r.laco) r.laco = { envio: crypto.randomUUID(), texto: '' }; r.laco.apagar = () => { r.laco = null; }; return r.laco; };
  if (r.laco) r.laco.apagar = () => { r.laco = null; };
  return h('section.comentario-laco',
    h('h2.secao-titulo', icone('balao'), 'Para o laço todo'),
    h('p.dica-inline', 'um comentário vira pedido ao maestro pela caixa; ex.: partir de novo com outros valores, uma ideia para a próxima execução'),
    formularioDeComentario(app, u, laco, { chave: `com-laco:${laco.id}:${laco.execucao.id}`, d: r.laco, garantir, operacao: 'comentario-laco', rotulo: 'comentário sobre o laço todo', placeholder: 'o que o maestro deve saber sobre este laço' }));
}

// ------------------------------------------------------------------ pedidos e estados
function palavraDoPedido(laco, p) {
  const no = laco.nos.find(n => n.id === p.no);
  const c = laco.controles.find(x => x.id === p.controle);
  switch (p.operacao) {
    case 'mudar-controle': return `mudar “${c ? c.rotulo : p.controle}”${no ? ` (${no.titulo})` : ''}`;
    case 'pedir-parada': return p.capacidade === 'parar-apos-onda' ? `parar depois da onda ${p.onda}` : 'parar de despachar';
    case 'pedir-pausa': return 'pausar';
    case 'pedir-retomada': return 'retomar';
    case 'comentario-no': return `comentário em ${no ? no.titulo : p.no}`;
    case 'comentario-laco': return 'comentário no laço';
    default: return p.operacao || 'pedido';
  }
}
/** Estado de um pedido em palavras e cor (§2.6): enviado → lido → aplicando → aplicado | recusado | conflito | encerrado. */
function estadoDoPedido(laco, p) {
  const rc = p.recibo || {};
  if (!rc.estado_valido) return { palavra: `estado desconhecido${p.estado ? ` (“${p.estado}”)` : ''}`, classe: 'ep-desconhecido' };
  if (rc.valido === false) return { palavra: `${PALAVRA_ESTADO[p.estado] || p.estado} com recibo inválido`, classe: 'ep-invalido' };
  const comentario = p.operacao === 'comentario-no' || p.operacao === 'comentario-laco';
  switch (p.estado) {
    case 'nova': return { palavra: 'enviado', classe: 'ep-enviado' };
    case 'lida': {
      if (comentario) return { palavra: 'lido', classe: 'ep-feito' };
      const m = minutosDesde(p.enviada);
      return { palavra: m !== null && m >= LIDO_SEM_DESFECHO_MIN ? `lido, sem desfecho há ${m < 60 ? `${m} min` : `${Math.floor(m / 60)} h`}` : 'lido', classe: 'ep-lido' };
    }
    case 'aplicando': return { palavra: `aplicando desde ${quando(rc.aplicando_desde)}`, classe: 'ep-lido' };
    case 'aplicado':
      if (rc.efeito === 'valeu') return { palavra: `aplicado · valeu ${quando(rc.valeu_em)}`, classe: 'ep-feito' };
      if (rc.efeito === 'aguarda') { const c = laco.controles.find(x => x.id === p.controle); return { palavra: `aplicado, aguarda efeito: ${c ? QUANDO_VALE[c.quando_vale] || c.quando_vale : 'a confirmar'}`, classe: 'ep-aguarda' }; }
      return { palavra: 'configuração gravada; efeito não confirmado', classe: 'ep-naoconf' };
    case 'recusado': return { palavra: 'recusado', classe: 'ep-recusado' };
    case 'conflito': return { palavra: 'conflito', classe: 'ep-conflito' };
    case 'encerrado-sem-aplicar': return { palavra: 'encerrado sem aplicar', classe: 'ep-encerrado' };
    default: return { palavra: p.estado || '?', classe: 'ep-desconhecido' };
  }
}
const PALAVRA_ESTADO = { nova: 'enviado', lida: 'lido', aplicando: 'aplicando', aplicado: 'aplicado', recusado: 'recusado', conflito: 'conflito', 'encerrado-sem-aplicar': 'encerrado sem aplicar' };
const TRILHA = ['enviado', 'lido', 'aplicando', 'aplicado'];

function cartaoDoPedido(app, u, laco, p, op = {}) {
  const { h, icone } = u;
  const e = estadoDoPedido(laco, p);
  const c = laco.controles.find(x => x.id === p.controle);
  const rc = p.recibo || {};
  const passo = { nova: 0, lida: 1, aplicando: 2, aplicado: 3 }[p.estado];
  const corpo = [];
  if (p.operacao === 'mudar-controle') corpo.push(h('div.antes-depois', h('span.de', tipadoEmPalavras(c, p.antes)), icone('seta'), h('span.para', tipadoEmPalavras(c, p.depois)), h('span.dica-inline', 'configurado')));
  if (p.texto) corpo.push(h('blockquote.texto-pedido', corta(p.texto, 240)));
  if (p.estado === 'aplicado' && rc.valido) corpo.push(h('div.recibo', icone('recibo'), h('span', `recibo: ${tipadoEmPalavras(c, rc.antes)} → ${tipadoEmPalavras(c, rc.depois)} · aplicado ${quando(rc.aplicado_em)}${rc.efeito === 'valeu' ? ` · valeu ${quando(rc.valeu_em)}` : rc.efeito === 'aguarda' ? ' · efeito ainda não valeu' : ' · efeito não confirmado'}`),
    h('button.com-dica.mono', { type: 'button', dataset: { dicaTitulo: 'recibo do maestro', dica: `execução ${rc.execucao}; revisão depois de aplicar ${rc.revisao} (a impressão digital da configuração: muda quando algo que importa ao pedido muda)` } }, `revisão ${String(rc.revisao || '').slice(0, 8)}`)));
  if ((p.estado === 'recusado' || p.estado === 'encerrado-sem-aplicar') && rc.motivo) corpo.push(h('p.motivo-pedido', h('strong', 'motivo: '), rc.motivo));
  if (p.estado === 'conflito' && rc.valido !== false) {
    corpo.push(h('div.conflito-tri',
      h('div', h('small', 'você viu'), h('b', tipadoEmPalavras(c, p.antes))),
      h('div.agora', h('small', 'agora está'), h('b', rc.agora_esta ? tipadoEmPalavras(c, rc.agora_esta) : '—')),
      h('div.pediu', h('small', 'você pediu'), h('b', p.operacao === 'mudar-controle' ? tipadoEmPalavras(c, p.depois) : palavraDoPedido(laco, p)))));
    if (p.atual && !p.substituido_por && p.operacao === 'mudar-controle' && c && !laco.execucao.terminou_em) corpo.push(h('button.botao.de-pedido', { type: 'button', dataset: { foco: `propor-${p.envio}` }, onclick: () => proporDeNovo(app, laco, p) }, icone('lapis'), 'Propor de novo'));
  }
  if (rc.valido === false && rc.erros?.length) corpo.push(h('ul.erros-recibo', rc.erros.map(x => h('li', x))));
  const trilha = passo !== undefined && rc.valido !== false && !['recusado', 'conflito', 'encerrado-sem-aplicar'].includes(p.estado) && !(p.operacao || '').startsWith('comentario')
    ? h('ol.trilha-pedido', TRILHA.map((t, i) => h('li', { class: i < passo ? 'feito' : i === passo ? 'agora' : '' }, t))) : null;
  return h('li.cartao-pedido', { class: `cartao-pedido ${e.classe}${p.substituido_por ? ' substituido' : ''}${p.atual ? '' : ' antigo'}`, dataset: { foco: `pedido-${p.envio}` } },
    h('div.pedido-cabeca',
      h('span.pedido-o-que', icone(p.operacao === 'mudar-controle' ? 'botao' : (p.operacao || '').startsWith('comentario') ? 'balao' : p.operacao === 'pedir-pausa' ? 'pausa' : p.operacao === 'pedir-retomada' ? 'retomar' : 'parar'), op.semNo && p.operacao === 'mudar-controle' && c ? `mudar “${c.rotulo}”` : palavraDoPedido(laco, p)),
      h('span.estado-pedido', { class: `estado-pedido ${e.classe}` }, e.palavra)),
    trilha,
    corpo,
    h('div.pedido-rodape',
      h('span', `enviado ${quando(p.enviada)}`),
      p.estado === 'nova' && p.aviso ? h('span', p.aviso === 'entregue' ? 'aviso entregue' : p.aviso === 'falhou' ? 'aviso falhou' : 'aviso na fila') : null,
      p.substituido_por ? h('span.c-cinza', 'substituído por um pedido mais novo') : null,
      p.substitui ? h('span.c-cinza', 'substitui um pedido anterior') : null,
      !p.atual ? h('span.c-cinza', 'de uma execução anterior') : null));
}
const maisAbertos = new Set(); // laços com os pedidos antigos à mostra (sobrevive ao redesenho)
function pedidosDoLaco(app, u, laco) {
  const { h, icone } = u;
  // o que espera você (conflito atual) vem primeiro; depois do mais novo ao mais velho
  const esperando = p => p.estado === 'conflito' && p.atual && !p.substituido_por;
  const ps = [...(laco.pedidos || []).filter(esperando), ...(laco.pedidos || []).filter(p => !esperando(p))];
  return h('section.pedidos-laco',
    h('h2.secao-titulo', icone('envelope'), 'Pedidos', ps.length ? h('span.n', String(ps.length)) : null),
    ps.length ? h('ol.lista-pedidos', ps.slice(0, 5).map(p => cartaoDoPedido(app, u, laco, p))) : h('p.vazio', 'Nenhum pedido ainda. Botões, parada e comentários viram pedidos aqui.'),
    // os mais velhos ficam recolhidos (o que pede atenção vem primeiro: os 5 mais novos)
    ps.length > 5 ? h('details.mais-pedidos', { open: maisAbertos.has(laco.id) || null, ontoggle: ev => { if (ev.target.open) maisAbertos.add(laco.id); else maisAbertos.delete(laco.id); } }, h('summary', `mais ${ps.length - 5} pedido${ps.length - 5 > 1 ? 's' : ''}, mais antigos`), h('ol.lista-pedidos', ps.slice(5).map(p => cartaoDoPedido(app, u, laco, p)))) : null);
}
function proporDeNovo(app, laco, p) {
  const r = rascunhoDo(app, laco);
  const c = laco.controles.find(x => x.id === p.controle); if (!c) return;
  r.controles[c.id] = { envio: crypto.randomUUID(), valor: p.depois?.valor ?? null, texto: p.texto || '', antes: { tipo: c.tipo, valor: c.configurado.valor }, revisao: laco.revisao, substitui: p.arquivo, substituiDecidido: true, alvoVisto: p.arquivo };
  guardar(app, laco); novaGeracao(`prop:${laco.id}:${laco.execucao.id}:${c.id}`);
  abrirNo(laco.id, p.no);
}

// ------------------------------------------------------------------ gaveta do nó (à direita; prende o foco; Esc fecha)
let gavetaAberta = null; // { laco, no, soltar }
function fecharGavetaNo(devolverFoco = false) {
  if (!gavetaAberta) return;
  const no = gavetaAberta.no;
  gavetaAberta.soltar(); gavetaAberta = null;
  const g = document.getElementById('gaveta-no');
  const tinhaFoco = g && (g.contains(document.activeElement) || document.activeElement === document.body);
  if (g) { g.hidden = true; g.replaceChildren(); }
  // fechada pela rota (X, Esc fora dela, voltar do navegador): o foco volta ao nó no fluxo, depois do redesenho
  if (devolverFoco && tinhaFoco) setTimeout(() => document.querySelector(`[data-foco="no-${CSS.escape(no)}"]`)?.focus({ preventScroll: true }), 0);
}
function sincronizarGaveta(app, u, laco) {
  const noId = app.rota.params.get('no');
  const g = document.getElementById('gaveta-no');
  if (!g) return;
  const n = laco && noId ? laco.nos.find(x => x.id === noId) : null;
  if (!n) { if (gavetaAberta && !(noId && !laco)) fecharGavetaNo(true); return; }
  if (gavetaAberta && (gavetaAberta.laco !== laco.id || gavetaAberta.no !== n.id)) fecharGavetaNo();
  const chave = g.contains(document.activeElement) && !emEdicao(document.activeElement) ? document.activeElement.closest('[data-foco]')?.dataset.foco : null;
  const rolagem = g.querySelector('.gaveta-corpo')?.scrollTop || 0;
  trocarPreservando(g, conteudoDaGaveta(app, u, laco, n));
  const corpo = g.querySelector('.gaveta-corpo'); if (corpo) corpo.scrollTop = rolagem;
  if (chave && !g.contains(document.activeElement)) g.querySelector(`[data-foco="${CSS.escape(chave)}"]`)?.focus({ preventScroll: true });
  if (!gavetaAberta) {
    g.hidden = false;
    const soltar = prenderFoco(g, () => { gavetaAberta = null; g.hidden = true; g.replaceChildren(); if (app.rota.params.get('no')) location.hash = hrefLaco(laco.id); }, `no-${n.id}`);
    gavetaAberta = { laco: laco.id, no: n.id, soltar: soltar.soltar };
    // o redesenho que abriu a gaveta devolve o foco ao nó no fluxo; a gaveta é um diálogo e precisa ficar com ele
    setTimeout(() => { if (gavetaAberta && gavetaAberta.no === n.id && !g.contains(document.activeElement)) (g.querySelector('.fechar') || g).focus(); }, 0);
  }
}

function conteudoDaGaveta(app, u, laco, n) {
  const { h, icone } = u;
  const terminado = !!laco.execucao.terminou_em;
  const contadores = (laco.contadores || []).filter(c => c.no === n.id);
  const controles = (laco.controles || []).filter(c => c.no === n.id);
  const pedidos = (laco.pedidos || []).filter(p => p.no === n.id);
  const carta = n.carta ? app.indices.cartas.get(n.carta) : null;
  const r = rascunhoDo(app, laco);
  const garantirNo = () => { if (!r.nos[n.id]) r.nos[n.id] = { envio: crypto.randomUUID(), texto: '' }; r.nos[n.id].apagar = () => { delete r.nos[n.id]; }; return r.nos[n.id]; };
  if (r.nos[n.id]) r.nos[n.id].apagar = () => { delete r.nos[n.id]; };
  const corpo = h('div.gaveta-corpo',
    n.detalhe ? h('p.detalhe-no', n.detalhe) : null,
    carta ? h('a.botao', { href: `#/cartas/${encodeURIComponent(carta.id)}`, dataset: { foco: 'gaveta-no-carta' } }, icone('carta'), 'Abrir o painel: ', carta.titulo) : null,
    h('section.bloco-real',
      h('h3.bloco-titulo', icone('olho'), 'Estado real', h('span.selo-camada.real', 'lido do laço · só olhar')),
      contadores.length ? h('ul.contadores', contadores.map(ct => contadorNaGaveta(u, ct))) : h('p.vazio', 'Este nó não declara números.')),
    controles.length ? h('section.bloco-botoes',
      h('h3.bloco-titulo', icone('botao'), controles.length > 1 ? 'Botões' : 'Botão', terminado ? h('span.selo-camada', 'laço terminado: só leitura') : h('span.selo-camada.de-pedido', 'mudar vira pedido')),
      controles.map(c => cartaoDoControle(app, u, laco, c, terminado))) : null,
    h('section.bloco-comentario',
      h('h3.bloco-titulo', icone('balao'), 'Comentário sobre este nó'),
      formularioDeComentario(app, u, laco, { chave: `com-no:${laco.id}:${laco.execucao.id}:${n.id}`, d: r.nos[n.id], garantir: garantirNo, operacao: 'comentario-no', no: n.id, rotulo: `comentário sobre ${n.titulo}`, placeholder: 'ex.: mudar o harness, testar outro modelo, uma dúvida' })),
    h('section.bloco-pedidos',
      h('h3.bloco-titulo', icone('envelope'), 'Pedidos deste nó', pedidos.length ? h('span.n', String(pedidos.length)) : null),
      pedidos.length ? h('ol.lista-pedidos', pedidos.map(p => cartaoDoPedido(app, u, laco, p, { semNo: true }))) : h('p.vazio', 'Nenhum pedido para este nó.')));
  return [
    h('div.gaveta-cabeca',
      h('span.icone-no', { class: `icone-no p-${n.papel}` }, icone(iconeDoNo(n))),
      h('div', { style: 'flex:1;min-width:0' },
        h('div.gaveta-sup', `${laco.titulo} · ${PAPEL[n.papel]?.palavra || n.papel}`),
        h('h2', n.titulo),
        h('div.linha-chips', h('span.chip.e-open', PAPEL[n.papel]?.dica || n.papel))),
      h('button.fechar', { type: 'button', 'aria-label': 'Fechar a gaveta do nó', dataset: { foco: 'gaveta-no-fechar' }, onclick: () => { location.hash = hrefLaco(laco.id); } }, icone('fechar'))),
    corpo];
}

function contadorNaGaveta(u, ct) {
  const { h } = u;
  let valor;
  if (ct.ilegivel) valor = h('span.c-coral', `ilegível: ${ct.ilegivel}`);
  else if (ct.valor === null || ct.valor === undefined) valor = h('span.c-cinza', 'sem valor');
  else if (ct.tipo === 'lista') valor = h('span.fichas', ct.valor.slice(0, 24).map(x => h('span.ficha', x)), ct.valor.length > 24 ? h('span.ficha.mais', `+${ct.valor.length - 24}`) : null);
  else if (ct.tipo === 'contagem') valor = h('span.fichas', Object.entries(ct.valor).map(([k, v]) => h('span.ficha', h('b', fmt(v, 0)), ` ${k.replace(/_/g, ' ')}`)));
  else if (ct.tipo === 'serie') {
    const campos = ct.campos || Object.keys(ct.valor[0] || {});
    valor = h('table.serie', h('thead', h('tr', campos.map(c => h('th', c.replace(/_/g, ' '))))), h('tbody', ct.valor.slice(-10).map(v => h('tr', campos.map(c => h('td', typeof v[c] === 'number' ? (v[c] <= 1 && /taxa|fra/.test(c) ? `${fmt(v[c] * 100, 1)}%` : fmt(v[c], 2)) : String(v[c] ?? '')))))));
  } else if (ct.tipo === 'hora') valor = h('b.valor-grande', quando(ct.valor));
  else valor = h('b.valor-grande', contadorEmPalavras(ct).replace(` ${ct.rotulo}`, '').replace(`${ct.rotulo}: `, ''));
  return h('li.contador-no',
    h('div.cn-rotulo', ct.rotulo),
    h('div.contador-valor', valor),
    h('div.fonte', ct.ilegivel ? `fonte: ${ct.fonte || '?'}` : `${ct.fonte} · ${quando(ct.hora)}`));
}

// ------------------------------------------------------------------ um botão: configurado × em uso × sua proposta
function cartaoDoControle(app, u, laco, c, terminado) {
  const { h, icone } = u;
  const cfg = c.configurado, uso = c.em_uso;
  const linhaCfg = h('div.linha-cfg',
    h('span.rot', 'configurado'),
    cfg.ilegivel ? h('b.c-coral', 'ilegível') : h('b.valor-grande', valorEmPalavras(c, cfg.valor)),
    h('span.fonte', cfg.ilegivel ? `${cfg.fonte || '?'}: ${cfg.ilegivel}` : cfg.como === 'declarado' ? 'declarado pelo maestro' : `lido de ${cfg.fonte} às ${hhmm(cfg.hora)}`));
  const usoTexto = uso.estado === 'confirmado'
    ? [h('b', { class: uso.diverge ? 'c-coral' : '' }, valorEmPalavras(c, uso.valor)), h('span.explica', `confirmado (${uso.como})${uso.diverge ? ' · diverge do configurado' : ''}`)]
    : uso.estado === 'relido' ? [h('b', 'relido'), h('span.explica', 'relido pelo laço a cada ciclo; não é prova de uso')]
    : [h('b.c-cinza', 'não confirmado'), h('span.explica', uso.ilegivel ? `a fonte de uso não pôde ser lida: ${uso.ilegivel}` : 'o processo pode ter subido com outro valor ou ainda não ter sido religado')];
  const linhaUso = h('div.linha-uso', { class: `linha-uso u-${uso.estado}` }, h('span.rot', 'em uso'), usoTexto);
  const precond = Object.entries(c.precondicoes || {}).map(([nome, p]) => h('div.precondicao', `${(PRECONDICAO[nome] || nome).replace(/_/g, ' ')}: `, p.ilegivel ? h('span.c-coral', 'ilegível') : h('b', typeof p.valor === 'string' && !isNaN(new Date(p.valor)) ? quando(p.valor) : String(p.valor))));
  const partes = [h('div.cc-cabeca', h('strong', c.rotulo), h('span.vale', { dataset: { dicaTitulo: 'quando vale', dica: `${QUANDO_VALE[c.quando_vale] || c.quando_vale}; ${RELEITURA[c.releitura] || c.releitura}` }, tabindex: 0 }, icone('relogio'), `vale ${QUANDO_VALE[c.quando_vale] || c.quando_vale}`)), linhaCfg, linhaUso, precond];
  if (!terminado) partes.push(...propostaDoControle(app, u, laco, c));
  const ultimo = (laco.pedidos || []).find(p => p.atual && p.controle === c.id);
  if (ultimo) { const e = estadoDoPedido(laco, ultimo); partes.push(h('div.ultimo-pedido', icone('envelope'), `último pedido: ${tipadoEmPalavras(c, ultimo.depois)} · `, h('span.estado-pedido', { class: `estado-pedido ${e.classe}` }, e.palavra))); }
  return h('article.cartao-controle', { dataset: { foco: `controle-${c.id}` } }, partes);
}

/** Validação do valor pedido, a mesma da torre (§4.5); devolve o motivo em palavras ou null. */
function motivoInvalido(c, v) {
  if (v === null) return c.aceita_nulo ? null : 'este botão não aceita vazio';
  if (['numero', 'inteiro', 'duracao'].includes(c.tipo)) {
    if (typeof v !== 'number' || !Number.isFinite(v)) return 'precisa ser um número';
    if (c.tipo === 'inteiro' && !Number.isInteger(v)) return 'precisa ser um número inteiro';
    if (c.faixa && (v < c.faixa[0] || v > c.faixa[1])) return `fora da faixa (${valorEmPalavras(c, c.faixa[0])} a ${valorEmPalavras(c, c.faixa[1])})`;
  } else if (c.tipo === 'escolha') { if (!(c.opcoes || []).some(o => o.valor === v)) return 'escolha uma das opções'; }
  else if (c.tipo === 'lista') {
    if (!Array.isArray(v)) return 'precisa ser uma lista';
    if (new Set(v).size !== v.length) return 'há item repetido';
    if (c.itens && v.length > c.itens.max) return `no máximo ${c.itens.max} itens`;
    if (v.some(x => typeof x !== 'string' || !x.trim() || /[\r\n]/.test(x) || (c.itens && x.length > c.itens.comprimento))) return 'cada item é uma linha curta';
    if (c.opcoes && v.some(x => !c.opcoes.some(o => o.valor === x))) return 'há item fora das opções';
  } else if (c.tipo === 'texto-curto') { if (typeof v !== 'string' || v.length > 200 || /[\r\n]/.test(v)) return 'até 200 caracteres, numa linha'; }
  return null;
}
const iguaisValor = (c, a, b) => c.tipo === 'lista' ? (Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every(x => b.includes(x))) : a === b;
const arred = v => Math.round(v * 1e9) / 1e9;

/** "Sua proposta": tracejado terracota, com a faixa, as opções ou os itens; "Pedir ao maestro" grava o pedido. */
function propostaDoControle(app, u, laco, c) {
  const { h, icone } = u;
  const r = rascunhoDo(app, laco);
  const kBase = `prop:${laco.id}:${laco.execucao.id}:${c.id}`;
  const cfg = c.configurado;
  if (cfg.ilegivel && !r.controles[c.id]) return [h('div.proposta-no.desligada', icone('alerta'), 'Sem pedido enquanto o valor configurado não puder ser lido.')];
  let d = r.controles[c.id] || null;
  // rascunho de antes desta correção: a referência guardada não volta (o alvo é recalculado na hora de enviar)
  if (d && !d.substituiDecidido && 'substitui' in d) { delete d.substitui; if (d.alvoVisto === undefined) d.alvoVisto = alvoDaSubstituicao(laco, d, casaControle(c.id))?.arquivo || null; guardar(app, laco); }
  const chave = () => `${kBase}:${geracao(kBase)}:${d ? 'rascunho' : JSON.stringify(cfg.valor)}`;
  const form = h('form.proposta-no', { novalidate: true, onsubmit: e => e.preventDefault(), dataset: { preservar: chave() } });
  // o rascunho só nasce quando o Gustavo mexe; aí a chave do formulário vivo muda junto (sem trocar o nó em edição)
  const garantir = () => {
    if (!d) {
      const ant = substituivel(lacoAtual(laco), casaControle(c.id));
      d = r.controles[c.id] = { envio: crypto.randomUUID(), valor: cfg.valor, texto: '', antes: { tipo: c.tipo, valor: cfg.valor }, revisao: laco.revisao, alvoVisto: ant ? ant.arquivo : null };
      form.dataset.preservar = chave();
      // a nota do que este pedido substitui vive fora do formulário: redesenha (o formulário em edição fica)
      if (ant) setTimeout(redesenhar, 0);
    }
    return d;
  };
  const atual = () => (d ? d.valor : cfg.valor);
  const mostraValor = h('b.valor-proposta');
  const aviso = h('div.aviso-proposta');
  const enviar = h('button.botao.primario', { type: 'button', dataset: { foco: `pedir-${c.id}` } }, icone('envelope'), d?.emVoo ? 'Tentar de novo' : 'Pedir ao maestro');
  const erro = h('div.erro-acao', { role: 'alert' });
  const atualizarEstado = () => {
    const v = atual();
    mostraValor.textContent = valorEmPalavras(c, v);
    const motivo = motivoInvalido(c, v);
    const igual = iguaisValor(c, v, d ? d.antes.valor : cfg.valor);
    aviso.textContent = motivo ? motivo : igual ? 'igual ao configurado: mude o valor para pedir' : '';
    aviso.className = `aviso-proposta${motivo ? ' c-coral' : ''}`;
    enviar.disabled = !d || (!d.emVoo && (!!motivo || igual));
  };
  const mudar = v => { garantir().valor = v; guardar(app, laco); atualizarEstado(); };
  const entrada = entradaDoControle(u, c, atual, mudar);
  const area = h('textarea.texto-proposta', { 'aria-label': `por quê (opcional): ${c.rotulo}`, placeholder: 'por quê (opcional)', maxlength: '20000', rows: '2', dataset: { foco: `por-que-${c.id}` }, oninput: ev => { garantir().texto = ev.target.value; guardar(app, laco); } });
  area.value = d?.texto || '';
  form.append(...[
    h('div.pp-cabeca', h('span.rot', 'sua proposta'), mostraValor),
    entrada, aviso, area,
    h('div.rodape-acao', enviar, h('span.dica-inline', `vale ${QUANDO_VALE[c.quando_vale] || c.quando_vale}`)), erro].filter(Boolean));
  if (d?.emVoo) erro.textContent = `Envio pendente (${d.emVoo.motivo}). "Tentar de novo" reenvia o mesmo pedido, com o mesmo envio.`;
  const caixaConflito = cf => h('div', h('button.botao', { type: 'button', dataset: { foco: `adotar-${c.id}` }, onclick: () => {
    const dd = garantir();
    dd.antes = cf.agora; dd.revisao = cf.revisao; dd.envio = crypto.randomUUID(); dd.conflito = null; dd.emVoo = null;
    guardar(app, laco); novaGeracao(kBase); redesenhar();
  } }, icone('lapis'), 'Propor sobre o valor atual'));
  if (d?.conflito) { erro.replaceChildren(...mensagemDeRecusa(u, laco, { status: 409, corpo: { erro: 'laco-mudou', conflito: d.conflito } }, c), caixaConflito(d.conflito)); }
  const casa = casaControle(c.id);
  enviar.onclick = () => enviarPedido(app, u, laco, garantir(), {
    controle: c, erro, botao: enviar, rotulo: 'Pedir ao maestro', aoConflito: caixaConflito,
    decidir: () => precisaDecidir(laco, d, casa),
    aoRecuperar: async alvo => {
      const dd = garantir();
      dd.recuperar = { alvo: alvo || dd.recuperar?.alvo || (dd.substituiDecidido ? dd.substitui : (dd.alvoVisto || null)) };
      guardar(app, laco); await atualizar(true); redesenhar();
      setTimeout(() => document.querySelector(`[data-foco^="rec-${c.id}-"]`)?.focus({ preventScroll: true }), 60);
    },
    montar: () => {
      const v = d.valor; const motivo = motivoInvalido(c, v);
      if (motivo) return { erro: `Valor inválido: ${motivo}.` };
      if (iguaisValor(c, v, d.antes.valor)) return { erro: 'O valor pedido é igual ao configurado.' };
      const corpo = { envio: d.envio, tipo: 'alteracao-laco', laco: laco.id, execucao: laco.execucao.id, operacao: 'mudar-controle', no: c.no, controle: c.id, antes: d.antes, depois: { tipo: c.tipo, valor: v }, revisao: d.revisao };
      const t = (d.texto || '').trim(); if (t) corpo.texto = t;
      const alvo = alvoDaSubstituicao(laco, d, casa);
      if (alvo) corpo.substitui = alvo.arquivo;
      return { corpo };
    },
    concluir: () => { delete r.controles[c.id]; d = null; guardar(app, laco); novaGeracao(kBase); u.brisa(`Pedido gravado na caixa: ${c.rotulo}. O maestro confere e dá o desfecho.`, 'verde'); },
  });
  atualizarEstado();
  const avisos = [];
  if (d && d.revisao !== laco.revisao) avisos.push(h('div.nota-mudou', icone('alerta'), 'A configuração do laço mudou depois que você começou esta proposta; ao pedir, a torre mostra a diferença.'));
  // fora do formulário preservado: refeitos a cada atualização, sobre o estado atual dos pedidos
  if (precisaDecidir(laco, d, casa)) avisos.push(blocoDeRecuperacao(u, laco, d, casa, alvo => escolherSubstituicao(app, laco, d, alvo, `pedir-${c.id}`), `rec-${c.id}`));
  else { const nota = notaDeSubstituicao(u, laco, d, casa); if (nota) avisos.push(nota); }
  return [...avisos, form];
}

/** O controle de entrada pelo tipo: faixa (deslizante + número), escolha, lista (fichas), texto curto, "sem limite". */
function entradaDoControle(u, c, atual, mudar) {
  const { h, icone } = u;
  const v0 = atual();
  if (['numero', 'inteiro', 'duracao'].includes(c.tipo)) {
    const pct = c.escala === 'porcento';
    const vista = v => v === null ? '' : pct ? arred(v * 100) : v;
    const real = x => pct ? arred(x / 100) : x;
    const [mn, mx] = c.faixa || [0, 100];
    const passo = c.tipo === 'inteiro' ? 1 : (() => { const p = (vista(mx) - vista(mn)) / 100; const e = Math.pow(10, Math.floor(Math.log10(p))); return arred(e); })();
    const num = h('input.numero-proposta', { type: 'number', min: String(vista(mn)), max: String(vista(mx)), step: c.tipo === 'inteiro' ? '1' : 'any', value: v0 === null ? '' : String(vista(v0)), 'aria-label': `${c.rotulo}${pct ? ' (em %)' : c.unidade ? ` (${c.unidade})` : ''}`, dataset: { foco: `num-${c.id}` } });
    const des = h('input.deslizante', { type: 'range', min: String(vista(mn)), max: String(vista(mx)), step: String(passo), value: v0 === null ? String(vista(mn)) : String(vista(v0)), 'aria-label': `${c.rotulo}: deslizar`, dataset: { foco: `des-${c.id}` } });
    const nulo = c.aceita_nulo ? h('label.nulo', h('input', { type: 'checkbox', checked: v0 === null || null, dataset: { foco: `nulo-${c.id}` }, onchange: ev => { const on = ev.target.checked; num.disabled = des.disabled = on; mudar(on ? null : real(Number(des.value))); if (!on) num.value = des.value; } }), c.nulo || 'vazio') : null;
    if (v0 === null) num.disabled = des.disabled = true;
    num.oninput = () => { if (num.value === '') return; const x = Number(num.value); des.value = String(x); mudar(c.tipo === 'inteiro' ? x : real(x)); };
    des.oninput = () => { num.value = des.value; mudar(c.tipo === 'inteiro' ? Number(des.value) : real(Number(des.value))); };
    return h('div.entrada-faixa',
      h('div.linha-faixa', h('span.extremo', valorEmPalavras(c, mn).replace(c.unidade && c.tipo !== 'duracao' ? ` ${c.unidade}` : '', '')), des, h('span.extremo', valorEmPalavras(c, mx).replace(c.unidade && c.tipo !== 'duracao' ? ` ${c.unidade}` : '', ''))),
      h('div.linha-numero', num, h('span.unidade', pct ? `%${c.unidade ? ` ${c.unidade}` : ''}` : c.tipo === 'duracao' ? c.unidade : (c.unidade || '')), nulo));
  }
  if (c.tipo === 'escolha') {
    return h('div.opcoes-escolha', { role: 'radiogroup', 'aria-label': c.rotulo }, (c.opcoes || []).map(o =>
      h('label.opcao', h('input', { type: 'radio', name: `esc-${c.id}`, value: o.valor, checked: v0 === o.valor || null, dataset: { foco: `esc-${c.id}-${o.valor}` }, onchange: () => mudar(o.valor) }), h('span.texto', o.rotulo))));
  }
  if (c.tipo === 'lista') {
    const caixa = h('div.entrada-lista');
    const desenhar = () => {
      const v = atual() || [];
      const base = new Set(v);
      const fichas = h('div.fichas.editaveis', v.map(x => h('span.ficha', x, h('button.mini', { type: 'button', 'aria-label': `remover ${x}`, dataset: { foco: `rem-${c.id}-${x}` }, onclick: () => { mudar(v.filter(y => y !== x)); desenhar(); focar(); } }, icone('fechar')))));
      const novo = h('input.novo-item', { type: 'text', placeholder: c.opcoes ? 'adicionar (uma das opções)' : 'adicionar um item', maxlength: String(c.itens?.comprimento || 200), 'aria-label': `adicionar item a ${c.rotulo}`, dataset: { foco: `add-${c.id}` },
        onkeydown: ev => { if (ev.key === 'Enter') { ev.preventDefault(); adicionar(); } } });
      const adicionar = () => { const t = novo.value.trim(); if (!t || base.has(t)) { novo.value = ''; return; } mudar([...v, t]); desenhar(); caixa.querySelector('.novo-item')?.focus(); };
      const focar = () => caixa.querySelector('.novo-item')?.focus();
      caixa.replaceChildren(fichas, h('div.linha-numero', novo, h('button.botao', { type: 'button', onclick: adicionar }, '+ adicionar')));
    };
    desenhar();
    return caixa;
  }
  return h('input.texto-curto', { type: 'text', maxlength: '200', value: v0 ?? '', 'aria-label': c.rotulo, dataset: { foco: `txt-${c.id}` }, oninput: ev => mudar(ev.target.value) });
}
