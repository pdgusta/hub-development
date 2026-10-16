// Lista os .md cujo frontmatter o gray-matter (parser do OHS) rejeita. Rodar de dentro de robusta\.
const gm = require('gray-matter'), fs = require('fs'), p = require('path');
const root = 'C:\\Projetos\\bancada-busca\\corpus', bad = [];
(function w(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.name.startsWith('.') || e.name === 'rajada') continue;
    const f = p.join(d, e.name);
    if (e.isDirectory()) w(f);
    else if (e.name.endsWith('.md')) { try { gm(fs.readFileSync(f, 'utf8')); } catch { bad.push(p.relative(root, f).split(p.sep).join('/')); } }
  }
})(root);
console.log(bad.length);
fs.writeFileSync('C:\\Projetos\\bancada-busca\\robusta\\yaml-invalido.json', JSON.stringify(bad));
