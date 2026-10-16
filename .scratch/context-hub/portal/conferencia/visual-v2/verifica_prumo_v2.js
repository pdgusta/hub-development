// revisão dirigida do visual v2: (1) bloqueios reais, (2) leitura sempre visível, (3) dica flutuante sem cobrir vizinhos
// uso: node verifica_prumo_v2.js <pasta-capturas> [so=1|2|3]
const puppeteer = require('puppeteer-core'); const path = require('path');
const espera = ms => new Promise(r => setTimeout(r, ms));
const OBST = '[data-obstaculo], .cartao-carta, .carta-mestra, .item-rodada, .cartao-pergunta, .termo-par, .linha-do-tempo li, .carta-rodada, ul.decisoes li, .miniatura-carta, .resposta-enviada, .rodada-cabeca, .coluna-fora li, .lista-radar li';
const out = process.argv[2], so = process.argv[3];
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: 'new', args: ['--disable-gpu'] });
  const erros = [];
  const pagina = async (url, w = 1600, h = 900) => { const p = await b.newPage(); p.on('pageerror', e => erros.push(String(e))); await p.setViewport({ width: w, height: h }); await p.goto(url, { waitUntil: 'networkidle0' }); await espera(2200); return p; };

  if (!so || so === '1') {
    const p = await pagina('http://127.0.0.1:8771/#/torre');
    const ler = async n => p.evaluate(n => {
      const m = document.querySelector(`.marco[data-t="${n}"]`); m.click();
      const placa = document.querySelector('.placa').innerText.replace(/\s+/g, ' ');
      return { est: m.querySelector('.est')?.innerText, aria: m.getAttribute('aria-label'), dica: m.dataset.dica.replace(/\n/g, ' | '), placa: placa.slice(0, 220) };
    }, n);
    console.log('[1] fixture 05', JSON.stringify(await ler('05')));
    console.log('[1] fixture 07', JSON.stringify(await ler('07')));
    console.log('[1] proximo', await p.evaluate(() => document.querySelector('.proximo').innerText));
    await p.screenshot({ path: path.join(out, 'fixture-07-bloqueios-reais-1600.png') });
    await p.close();
  }
  if (!so || so === 'c') {
    const p = await pagina('http://127.0.0.1:8771/#/torre');
    const m = await p.evaluate(() => { const m = document.querySelector('.marco[data-t="07"]'); m.click(); return { est: m.querySelector('.est')?.innerText, dica: m.dataset.dica.replace(/\n/g, ' | '), placa: document.querySelector('.placa').innerText.replace(/\s+/g, ' ').slice(0, 200) }; });
    console.log('[1] copia sem 03 no 07', JSON.stringify(m));
    await p.screenshot({ path: path.join(out, 'fixture-ciclo-sem-03-1600.png') });
    await p.close();
  }
  if (!so || so === '2') {
    for (const [w, h] of [[1280, 800], [1600, 900]]) {
      const p = await pagina('http://127.0.0.1:8770/#/torre', w, h);
      for (const sel of ['.cartucho .selo:last-of-type', '.marco[data-t="17"]', '.conquista', '.folha[data-t="52"]', '.margem .marco']) {
        const r = await p.evaluate(sel => {
          const alvo = [...document.querySelectorAll(sel)].pop(); alvo.focus();
          const l = document.getElementById('leitura').getBoundingClientRect(), a = alvo.getBoundingClientRect();
          const cobre = [...document.querySelectorAll('.marco, .cartucho, .indice')].filter(m => { const q = m.getBoundingClientRect(); return q.left < l.right && l.left < q.right && q.top < l.bottom && l.top < q.bottom; }).length;
          return `${sel}: alvo y=${Math.round(a.top)}..${Math.round(a.bottom)} leitura y=${Math.round(l.top)}..${Math.round(l.bottom)} visivel=${l.top >= 0 && l.bottom <= innerHeight} lendo=${document.getElementById('leitura').classList.contains('lendo')} cobreCartoes=${cobre}`;
        }, sel);
        console.log(`[2] ${w}`, r);
      }
      await p.screenshot({ path: path.join(out, `leitura-foco-baixo-${w}.png`) });
      await p.close();
    }
  }
  if (!so || so === '3') {
    for (const [w, h] of [[1600, 900], [1280, 800]]) for (const rota of ['partidas', 'autorizacoes', 'cartas', 'rumo']) {
      const p = await pagina('http://127.0.0.1:8770/#/' + rota, w, h);
      const res = await p.evaluate(async OBST => {
        const dorme = ms => new Promise(r => setTimeout(r, ms));
        const alvos = [...document.querySelectorAll('#tela [data-dica]')].filter(a => { const r = a.getBoundingClientRect(); return r.width && !a.closest('[hidden]'); });
        let total = 0, naFaixa = 0, cobrem = [];
        for (const a of alvos.slice(0, 60)) {
          a.scrollIntoView({ block: 'center' }); await dorme(30);
          if (typeof a.focus === 'function') a.focus(); a.dispatchEvent(new MouseEvent('mouseover', { bubbles: true })); await dorme(40);
          const d = document.getElementById('dica'); const f = document.getElementById('leitura'); if (d.hidden) { if (f.classList.contains('lendo')) naFaixa++; a.blur && a.blur(); continue; }
          total++;
          const r = d.getBoundingClientRect();
          const viz = [...document.querySelectorAll('#tela ' + OBST.split(', ').join(', #tela '))].filter(o => !o.contains(a)).filter(o => { const q = o.getBoundingClientRect(); return q.width && Math.min(q.right, r.right) - Math.max(q.left, r.left) > 2 && Math.min(q.bottom, r.bottom) - Math.max(q.top, r.top) > 2; });
          if (viz.length) cobrem.push(`${(a.dataset.dicaTitulo || a.textContent).trim().slice(0, 30)} → ${viz.map(v => (v.querySelector('h3,.titulo,dt')?.textContent || v.className).trim().slice(0, 24)).join(' / ')}`);
          a.blur && a.blur(); a.dispatchEvent(new MouseEvent('mouseout', { bubbles: true })); document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })); await dorme(20);
        }
        return { flutuantes: total, naFaixa, cobrem: cobrem.length, exemplos: cobrem.slice(0, 4) };
      }, OBST);
      console.log(`[3] ${rota} ${w}: ${JSON.stringify(res)}`);
      await p.close();
    }
  }
  console.log('erros', erros); await b.close();
})();
