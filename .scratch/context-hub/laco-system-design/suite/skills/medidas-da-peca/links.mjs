// links.mjs: confere os links de uma peça servida localmente. Node 18+ (fetch embutido), sem pacote.
// Uso: node links.mjs http://127.0.0.1:<porta>/caminho/da/peca.html
// Só acessa o próprio servidor local. Links de outra origem são só listados, nunca acessados.
// Escreve o JSON na saída padrão; quem grava em arquivo é o rodar.ps1 (em qa/).

const LOCAIS = new Set(['127.0.0.1', 'localhost', '[::1]']);

const arg = process.argv[2];
if (!arg) {
  console.error('uso: node links.mjs http://127.0.0.1:<porta>/peca.html');
  process.exit(2);
}
const pagina = new URL(arg);
if (!LOCAIS.has(pagina.hostname)) {
  console.error('recusado: só confiro peças servidas em 127.0.0.1 ou localhost');
  process.exit(2);
}

async function baixar(url, metodo = 'GET') {
  try {
    const r = await fetch(url, { method: metodo, redirect: 'manual' });
    return { status: r.status, tipo: r.headers.get('content-type') || '', corpo: metodo === 'GET' ? await r.text() : '' };
  } catch (e) {
    return { status: 0, erro: String(e.message || e), corpo: '' };
  }
}

// tira comentários e corpos de <script>/<style> antes de procurar atributos (o src da tag continua)
function limpar(html) {
  return html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/(<script\b[^>]*>)[\s\S]*?(<\/script>)/gi, '$1$2')
    .replace(/(<style\b[^>]*>)([\s\S]*?)(<\/style>)/gi, (m, a, css, c) => a + css.replace(/[^\n]/g, ' ') + c);
}

function decodificar(v) {
  return v.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}

function extrair(html) {
  const achados = [];
  const limpo = limpar(html);
  const re = /\s(href|src|xlink:href|poster|data|action)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi;
  let m;
  while ((m = re.exec(limpo))) achados.push({ atributo: m[1].toLowerCase(), valor: decodificar((m[3] ?? m[4] ?? m[5] ?? '').trim()) });
  const reSet = /\ssrcset\s*=\s*("([^"]*)"|'([^']*)')/gi;
  while ((m = reSet.exec(limpo))) {
    (m[2] ?? m[3] ?? '').split(',').forEach(p => { const u = p.trim().split(/\s+/)[0]; if (u) achados.push({ atributo: 'srcset', valor: decodificar(u) }); });
  }
  // url(...) dentro de <style> e de style="" (o original, não o limpo)
  const estilos = [];
  html.replace(/<style\b[^>]*>([\s\S]*?)<\/style>/gi, (x, css) => { estilos.push(css); return x; });
  html.replace(/\sstyle\s*=\s*"([^"]*)"/gi, (x, css) => { estilos.push(css); return x; });
  estilos.forEach(css => {
    const ru = /url\(\s*(['"]?)([^'")]+)\1\s*\)/gi;
    let u;
    while ((u = ru.exec(css))) achados.push({ atributo: 'url()', valor: decodificar(u[2].trim()) });
  });
  return achados;
}

function ancoras(html) {
  const ids = new Set();
  const re = /\s(?:id|name)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi;
  let m;
  while ((m = re.exec(html))) ids.add(decodificar(m[2] ?? m[3] ?? m[4] ?? ''));
  return ids;
}

const principal = await baixar(pagina);
if (principal.status !== 200) {
  console.log(JSON.stringify({ peca: pagina.href, erro: 'a peça não abriu', status: principal.status, detalhe: principal.erro || '' }, null, 1));
  process.exit(1);
}

const idsDaPagina = ancoras(principal.corpo);
const cache = new Map();
const res = {
  peca: pagina.href,
  nota: 'links montados por script na hora (JavaScript) não aparecem aqui; só os escritos no HTML',
  total: 0,
  locais_ok: 0,
  quebrados: [],
  ancoras_ok: 0,
  ancoras_quebradas: [],
  externos: [],
  embutidos: 0,
  ignorados: 0
};

for (const { atributo, valor } of extrair(principal.corpo)) {
  res.total++;
  if (!valor || /^(javascript:|about:)/i.test(valor)) { res.ignorados++; continue; }
  if (/^data:/i.test(valor)) { res.embutidos++; continue; }
  if (/^(mailto:|tel:)/i.test(valor)) { res.externos.push({ atributo, valor }); continue; }
  let alvo;
  try { alvo = new URL(valor, pagina); } catch { res.quebrados.push({ atributo, valor, motivo: 'endereço inválido' }); continue; }
  if (alvo.origin !== pagina.origin) { res.externos.push({ atributo, valor: alvo.href }); continue; }

  const semAncora = alvo.origin + alvo.pathname + alvo.search;
  const ancora = alvo.hash ? decodeURIComponent(alvo.hash.slice(1)) : '';
  const mesmaPagina = semAncora === pagina.origin + pagina.pathname + pagina.search;

  if (!mesmaPagina) {
    if (!cache.has(semAncora)) cache.set(semAncora, await baixar(semAncora, ancora ? 'GET' : 'HEAD'));
    let r = cache.get(semAncora);
    if (ancora && !r.corpo && r.status === 200) { r = await baixar(semAncora, 'GET'); cache.set(semAncora, r); }
    if (r.status !== 200) { res.quebrados.push({ atributo, valor, status: r.status, motivo: r.erro || 'HTTP ' + r.status }); continue; }
    res.locais_ok++;
    if (ancora && /html/i.test(r.tipo)) {
      if (ancoras(r.corpo).has(ancora)) res.ancoras_ok++;
      else res.ancoras_quebradas.push({ atributo, valor, motivo: 'âncora não existe no arquivo de destino' });
    }
  } else if (ancora) {
    if (idsDaPagina.has(ancora)) res.ancoras_ok++;
    else res.ancoras_quebradas.push({ atributo, valor, motivo: 'âncora não existe nesta página' });
  } else {
    res.locais_ok++;
  }
}

console.log(JSON.stringify(res, null, 1));
