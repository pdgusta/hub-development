// Render still frames of scenes for visual review, through ONE headless Edge (puppeteer-core connect), tiled 2x2 per scene.
// usage: node qa.js <project-dir> [--port 8766] [--ids s01,s02] [--frames 0.12,0.4,0.7,0.985] [--theme dark]
// before: cd <project>/export && npm i puppeteer-core@23.11.1 ; serve dist/ at http://localhost:<port>/ (dev.html)
// Why one Edge: launching a fresh msedge process per frame (the previous qa.py) hung whenever another headless Edge was
// running on the machine (the process came up without a renderer and never wrote the PNG). One instance, one page,
// navigate per frame: seconds instead of minutes, and the same file names as before (qa/<id>_<k>.png, qa/<id>_sheet.png).
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const PROJECT = path.resolve(argv[0]);
const puppeteer = require(require.resolve('puppeteer-core', { paths: [path.join(PROJECT, 'export'), __dirname] }));
const PORT = opt('--port', '8766'), THEME = opt('--theme', '');
const FR = opt('--frames', '0.12,0.4,0.7,0.985').split(',').map(Number);
const durs = fs.existsSync(path.join(PROJECT, 'durations.json')) ? JSON.parse(fs.readFileSync(path.join(PROJECT, 'durations.json'), 'utf8')) : {};
const ids = (opt('--ids', '') || fs.readdirSync(path.join(PROJECT, 'scenes')).filter(f => /^(s\d+|_template)\.js$/.test(f)).map(f => f.replace('.js', '')).sort().join(',')).split(',');
const QA = path.join(PROJECT, 'qa'); fs.mkdirSync(QA, { recursive: true });
const EDGE = process.env.EDGE_EXE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const DBG = 9400 + Math.floor(Math.random() * 100);            // random port: two QA runs on the machine must not collide
const PROF = path.join(os.tmpdir(), 'vg-qa-' + DBG);
(async () => {
  const child = spawn(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--remote-debugging-port=' + DBG, '--user-data-dir=' + PROF, '--window-size=1600,900', 'about:blank'], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 2500));
  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:' + DBG, defaultViewport: { width: 1600, height: 900 } });
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 0.75 });
  page.on('pageerror', e => console.error('pageerror', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
  const pfx = THEME ? THEME + '_' : '';
  for (const id of ids) {
    const D = durs[id] || 20; const outs = [];
    for (let k = 0; k < FR.length; k++) {
      const t = D * FR[k];
      const url = `http://localhost:${PORT}/dev.html?scene=${id}&t=${t.toFixed(2)}&v=${Date.now()}` + (THEME ? `&theme=${THEME}` : '');
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 700));
      const out = path.join(QA, `${pfx}${id}_${k}.png`);
      await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1600, height: 900 } });
      outs.push(out);
    }
    const sheet = path.join(QA, `${pfx}${id}_sheet.png`);
    const r = spawnSync('ffmpeg', ['-v', 'error', '-y', ...outs.flatMap(o => ['-i', o]), '-filter_complex', '[0:v][1:v]hstack[a];[2:v][3:v]hstack[b];[a][b]vstack', sheet]);
    console.log(id, 'frames at', FR.map(f => (D * f).toFixed(1) + 's').join(' '), r.status === 0 ? '-> ' + path.relative(PROJECT, sheet) : 'ffmpeg failed');
  }
  await browser.disconnect(); child.kill();
  try { fs.rmSync(PROF, { recursive: true, force: true }); } catch (e) { }
})().catch(e => { console.error(e); process.exit(1); });
