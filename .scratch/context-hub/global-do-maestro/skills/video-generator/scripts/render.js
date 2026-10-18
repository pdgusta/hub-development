// Render the page to MP4: N parallel headless Edge instances (puppeteer-core *connect*, since puppeteer.launch fails with
// msedge), each encodes a contiguous frame range through ffmpeg; parts are concatenated losslessly; narration clips are
// mixed at each scene's start. Reads dist/export.html (charset-safe) from a local http.server.
// usage: node render.js <project-dir> [--port 8766] [--workers 3] [--fps 30] [--out name.mp4]
// before: cd <project>/export && npm i puppeteer-core@23.11.1 ; cd <project>/dist && python -m http.server 8766 --bind 127.0.0.1
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const PROJECT = path.resolve(argv[0]);
// puppeteer-core is installed in <project>/export (npm i puppeteer-core@23.11.1), not next to this script
const puppeteer = require(require.resolve('puppeteer-core', { paths: [path.join(PROJECT, 'export'), __dirname] }));
const PORT = parseInt(opt('--port', '8766'), 10), WORKERS = parseInt(opt('--workers', '3'), 10), FPS = parseInt(opt('--fps', '30'), 10);
const OUT = path.join(PROJECT, 'export', 'out'); fs.mkdirSync(OUT, { recursive: true });
const FINAL = path.join(OUT, opt('--out', 'video.mp4'));
const URL = `http://localhost:${PORT}/export.html?export=1&v=` + Date.now();
const EDGE = process.env.EDGE_EXE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PROF = path.join(os.tmpdir(), 'vg-pptr');

async function launchEdge(port, profile) {
  const child = spawn(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--remote-debugging-port=' + port, '--user-data-dir=' + profile, '--window-size=1600,900', 'about:blank'], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 2500));
  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:' + port, defaultViewport: { width: 1600, height: 900 } });
  return { browser, close: async () => { try { await browser.disconnect(); } catch (e) { } child.kill(); } };
}
async function openPage(browser) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('pageerror', e.message));
  await page.goto(URL, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 600));
  return page;
}
async function renderRange(w, from, to, total) {
  const { browser, close } = await launchEdge(9340 + w, PROF + '-' + w);
  const page = await openPage(browser);
  const file = path.join(OUT, `part${w}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', file], { stdio: ['pipe', 'inherit', 'inherit'] });
  const write = (buf) => new Promise((res) => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });
  const t0 = Date.now();
  for (let k = from; k < to; k++) {
    await page.evaluate(t => Player.renderAt(t), k / FPS);
    await write(await page.screenshot({ type: 'jpeg', quality: 93, clip: { x: 0, y: 0, width: 1600, height: 900 } }));
    if ((k - from) % 600 === 0) console.log(`w${w} frame ${k}/${total} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await close();
  return file;
}
(async () => {
  const { browser, close } = await launchEdge(9339, PROF + '-plan');
  const page = await openPage(browser);
  const plan = await page.evaluate(() => { const p = Player.plan(); return { total: p.total, segs: p.segs.map(g => ({ id: g.s.meta.id, start: g.start, len: g.len, dur: g.s.dur })) }; });
  await close();
  fs.writeFileSync(path.join(OUT, 'plan.json'), JSON.stringify(plan, null, 1));
  const n = Math.ceil(plan.total * FPS);
  console.log('total', plan.total.toFixed(2), 's,', n, 'frames @', FPS, 'fps,', WORKERS, 'workers');
  const bounds = [...Array(WORKERS + 1)].map((_, i) => Math.round(n * i / WORKERS));
  const parts = await Promise.all([...Array(WORKERS)].map((_, w) => renderRange(w, bounds[w], bounds[w + 1], n)));
  const list = path.join(OUT, 'parts.txt'); fs.writeFileSync(list, parts.map(p => `file '${p.replace(/\\/g, '/')}'`).join('\n'));
  const video = path.join(OUT, 'silent.mp4');
  if (spawnSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', video], { stdio: 'inherit' }).status !== 0) throw new Error('concat failed');
  const inputs = ['-i', video], filters = [], labels = [];
  plan.segs.forEach((g, i) => {
    inputs.push('-i', path.join(PROJECT, 'audio', g.id + '.mp3'));
    const ms = Math.round(g.start * 1000);
    filters.push(`[${i + 1}:a]adelay=${ms}|${ms}[a${i}]`); labels.push(`[a${i}]`);
  });
  filters.push(labels.join('') + `amix=inputs=${plan.segs.length}:normalize=0:dropout_transition=0,apad=whole_dur=${plan.total.toFixed(2)}[mix]`);
  const r = spawnSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', filters.join(';'), '-map', '0:v', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-t', plan.total.toFixed(2), '-movflags', '+faststart', FINAL], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error('mux failed');
  console.log('done', FINAL, spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', FINAL]).stdout.toString().trim());
})().catch(e => { console.error(e); process.exit(1); });
