// Verificação da limpeza do fluxo (pedido do Designer, 2026-10-15): nada de texto cortado sob os nós; nenhuma pílula
// de palavra tocando linha alheia; nenhuma linha passando sobre texto de nó; envelope de pedido sem encostar no nó.
module.exports = () => {
  const svg = document.querySelector('svg.fluxo'); if (!svg) return null;
  const textosNos = [...svg.querySelectorAll('.no text')];
  const cortados = textosNos.map(t => t.textContent).filter(t => t.includes('…'));
  const caminhos = [...svg.querySelectorAll('path.lig')];
  const amostras = caminhos.map(p => { const L = p.getTotalLength(), pts = []; for (let d = 0; d <= L; d += 3) { const q = p.getPointAtLength(d); pts.push([q.x, q.y]); } return pts; });
  const dentro = (pts, b, folga) => pts.some(([x, y]) => x > b.x - folga && x < b.x + b.width + folga && y > b.y - folga && y < b.y + b.height + folga);
  const pilulas = [...svg.querySelectorAll('.rotulo-lig')];
  const pilulaEmLinha = [];
  pilulas.forEach((g, i) => { const b = g.querySelector('rect').getBBox(); amostras.forEach((pts, j) => { if (j !== i && dentro(pts, b, 2)) pilulaEmLinha.push(`${g.textContent} × linha ${j}`); }); });
  const pilulaEmPilula = [];
  pilulas.forEach((g, i) => pilulas.forEach((h, j) => { if (j <= i) return; const a = g.querySelector('rect').getBBox(), b = h.querySelector('rect').getBBox(); if (a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height) pilulaEmPilula.push(`${g.textContent} × ${h.textContent}`); }));
  const linhaEmTexto = [];
  amostras.forEach((pts, j) => textosNos.forEach(t => { if (dentro(pts, t.getBBox(), -1)) linhaEmTexto.push(`linha ${j} × "${t.textContent}"`); }));
  const envelopes = [...svg.querySelectorAll('.envelope-no > rect')].map(r => { const no = r.closest('.no'); const c = (no.querySelector('.caixa') || no.querySelector('.aro')).getBBox(); const b = r.getBBox(); return Math.round(c.y - (b.y + b.height)); });
  return { cortados, pilulaEmLinha, pilulaEmPilula, linhaEmTexto, folgaEnvelopes: envelopes, textos: textosNos.map(t => t.textContent) };
};
