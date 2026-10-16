// Ícones do núcleo: SVG inline desenhados aqui, nada de biblioteca. Todos em viewBox 0 0 24 24, cor = currentColor.

const CAMINHOS = {
  // torre de controle (marca e tela Torre)
  inicio: '<path d="M3 20h18M5 20l5-11 3 5 2-3 4 9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="18" cy="5" r="2" fill="none" stroke="currentColor" stroke-width="2"/>',
  lista: '<path d="M4 6h16M4 12h10M4 18h7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="18" cy="16" r="3" fill="none" stroke="currentColor" stroke-width="2"/>',
  envelope: '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 7l9 6 9-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  bussola: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 8.5l-2 5-5 2 2-5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  alfinete: '<path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
  bandeira: '<path d="M5 21V4M5 4h11l-2 4 2 4H5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  torre: '<path d="M12 2 8.5 13h7L12 2zM6 13h12v3H6zM9 16h6v6H9z"/>',
  // pista em perspectiva
  pista: '<path d="M9 3h6l5 18H4L9 3zm3 3v2m0 4v2m0 4v2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  // avião (partidas)
  aviao: '<path d="M3 12V4.5A1.5 1.5 0 0 1 4.5 3H12l9 9-9 9-9-9z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="7.5" cy="7.5" r="1.6"/>',
  // carimbo (autorizações)
  carimbo: '<path d="M12 3a3.5 3.5 0 0 0-3.5 3.5c0 1.5.8 2.6 1.5 3.5v2H7a2 2 0 0 0-2 2v2h14v-2a2 2 0 0 0-2-2h-3v-2c.7-.9 1.5-2 1.5-3.5A3.5 3.5 0 0 0 12 3zM5 18h14v3H5z"/>',
  // carta de navegação (cartas)
  carta: '<path d="M3 5l6-2 6 2 6-2v16l-6 2-6-2-6 2V5zm6 0v14m6-12v14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  // radar (rumo)
  radar: '<path d="M12 12 19 5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".6"/><circle cx="12" cy="12" r="1.6"/>',
  // balão (comentário)
  balao: '<path d="M4 4h16v11H9l-5 4V4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  // tipos de ticket
  pesquisa: '<circle cx="10.5" cy="10.5" r="6" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M15 15l5.5 5.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  conversa: '<path d="M3 5h12v8H8l-4 3V5z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M17 9h4v8h-2l-3 2v-2h-4v-2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
  prototipo: '<path d="M12 2l9 5v10l-9 5-9-5V7l9-5zm0 10 9-5M12 12v10M12 12 3 7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
  tarefa: '<path d="M5 12l5 5 9-10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
  tipo_desconhecido: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M12 8v5m0 3v.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  // estados
  aberto: '<circle cx="12" cy="12" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/>',
  andamento: '<circle cx="12" cy="12" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 12V7.5M12 12l3 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  resolvido: '<circle cx="12" cy="12" r="7"/><path d="M8.5 12l2.5 2.5 4.5-5" fill="none" stroke="#fbf6ec" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  descartado: '<circle cx="12" cy="12" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 16 16 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  bloqueado: '<rect x="5" y="11" width="14" height="9" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="1.9"/>',
  // utilidades
  alerta: '<path d="M12 3 2.5 20h19L12 3zm0 6v5m0 3v.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round"/>',
  fechar: '<path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  seta: '<path d="M4 12h16m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  pergunta: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7m0 3v.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  relogio: '<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  andaime: '<path d="M4 20V4m16 16V4M4 8h16M4 14h16M4 20h16M8 8l8 6M16 8l-8 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
  // laços (tela Laços): o laço do menu, o papel de cada nó e os pedidos
  laco: '<path d="M17 7a7 7 0 1 0 2 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 3.5V8h-4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="2.2"/>',
  olho: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.9"/>',
  pessoa: '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
  botao: '<circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M12 12 8.5 8.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M12 1.8v2M1.8 12h2M20.2 12h2M4.8 4.8l1.4 1.4M19.2 4.8l-1.4 1.4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
  parar: '<path d="M8 3h8l5 5v8l-5 5H8l-5-5V8z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/><path d="M8.5 12h7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  pausa: '<rect x="6" y="4.5" width="4" height="15" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.9"/><rect x="14" y="4.5" width="4" height="15" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.9"/>',
  retomar: '<path d="M7 4.5l12.5 7.5L7 19.5z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/>',
  plano: '<rect x="4.5" y="3" width="15" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
  placa: '<path d="M12 3v18" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/><path d="M12 5.5h6.5l2 2-2 2H12M12 12H5.5l-2 2 2 2H12" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/>',
  faisca: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
  funil: '<path d="M4 4.5h16l-6 7v6l-4 2.5v-8.5z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/>',
  bifurca: '<path d="M5 12h5l4-5h5M10 12l4 5h5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 5l2 2-2 2M17 15l2 2-2 2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>',
  caixa: '<path d="M3.5 7.5 12 3.5l8.5 4v9L12 20.5l-8.5-4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M3.5 7.5 12 11.5l8.5-4M12 11.5v9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  livro: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M4 21V5M9 7.5h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  conferir: '<circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M8 12.2l2.8 2.8 5.2-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  onda: '<path d="M2.5 10c2.4-3.6 4.8-3.6 7.2 0s4.8 3.6 7.2 0 3.4-2.7 4.6-1M2.5 16.5c2.4-3 4.8-3 7.2 0s4.8 3 7.2 0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
  sinal: '<circle cx="12" cy="17" r="1.8"/><path d="M8.2 13.4a5.4 5.4 0 0 1 7.6 0M5.2 10.4a9.6 9.6 0 0 1 13.6 0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
  lapis: '<path d="M4 20l1-5L16 4l4 4L9 19z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M14 6l4 4" stroke="currentColor" stroke-width="1.8"/>',
  recibo: '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 8h6M9 12h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
};

/** Devolve um elemento <svg> do ícone pedido. `rotulo` vira aria-label; sem ele, o ícone é decorativo. */
export function icone(nome, rotulo) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('fill', 'currentColor');
  if (rotulo) { svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', rotulo); }
  else svg.setAttribute('aria-hidden', 'true');
  svg.innerHTML = CAMINHOS[nome] || CAMINHOS.tipo_desconhecido;
  return svg;
}

/** Ícone + palavra do tipo de ticket (nunca o código cru sozinho). */
export function tipoTicket(tipo) {
  const mapa = { research: ['pesquisa', 'pesquisa'], grilling: ['conversa', 'conversa'], prototype: ['prototipo', 'protótipo'], task: ['tarefa', 'tarefa'] };
  if (tipo == null) return { icone: 'tipo_desconhecido', palavra: 'sem tipo' };
  const m = mapa[tipo];
  return m ? { icone: m[0], palavra: m[1] } : { icone: 'tipo_desconhecido', palavra: `tipo "${tipo}"` };
}

/** Ícone, palavra e classe de cor do estado de um ticket. */
export function estadoTicket(t) {
  switch (t.estado) {
    case 'open': return { icone: 'aberto', palavra: 'aberto', classe: 'e-open' };
    case 'claimed': return { icone: 'andamento', palavra: 'em andamento', classe: 'e-claimed' };
    case 'resolved': return { icone: 'resolvido', palavra: 'resolvido', classe: 'e-resolved' };
    case 'wontfix': return { icone: 'descartado', palavra: 'descartado', classe: 'e-wontfix' };
    default: return { icone: 'tipo_desconhecido', palavra: t.estado_cru == null ? 'sem estado' : `desconhecido ("${t.estado_cru}")`, classe: 'e-desconhecido' };
  }
}
