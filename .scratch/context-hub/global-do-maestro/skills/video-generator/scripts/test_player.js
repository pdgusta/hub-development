// Functional test of the player in headless Edge with autoplay allowed: start, pause (audio must freeze), resume,
// scene change, pause at a scene edge (must hold), resume into the next scene. Prints a JSON state per step.
// usage: node test_player.js <project-dir> <page.html> [--port 8766]   (page served from dist/ by http.server)
// Needs >= 2 scenes for the 'scene change' and 'pause at edge' steps to mean anything; with one scene the player ends and restarts.
const { spawn } = require('child_process');
const path = require('path'), os = require('os');
const argv = process.argv.slice(2);
const PROJECT = path.resolve(argv[0]);
const puppeteer = require(require.resolve('puppeteer-core', { paths: [path.join(PROJECT, 'export'), __dirname] }));
const PORT = (argv.indexOf('--port') >= 0) ? argv[argv.indexOf('--port') + 1] : '8766';
const PAGE = argv[1] || 'export.html';
const EDGE = process.env.EDGE_EXE || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const state = (page) => page.evaluate(() => ({ i: Player.i, playing: Player.playing, audioPaused: Player.audio.paused, audioT: +Player.audio.currentTime.toFixed(2), on: [...document.querySelectorAll('.scene.on')].map(e => e.dataset.id), badge: document.getElementById('paused').classList.contains('on') }));
(async () => {
  const prof = path.join(os.tmpdir(), 'vg-pptr-test');
  const child = spawn(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required', '--remote-debugging-port=9336', '--user-data-dir=' + prof, 'about:blank'], { stdio: 'ignore' });
  await sleep(2500);
  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9336', defaultViewport: { width: 1280, height: 720 } });
  const page = await browser.newPage();
  const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())) errs.push(m.text()); });
  await page.goto(`http://localhost:${PORT}/${PAGE}?v=` + Date.now(), { waitUntil: 'networkidle0' });
  await page.keyboard.press('Space'); await sleep(3000); console.log('after start   ', JSON.stringify(await state(page)));
  await page.keyboard.press('Space'); await sleep(1500); const p1 = await state(page); console.log('after pause   ', JSON.stringify(p1));
  await sleep(2500); const p2 = await state(page); console.log('still paused  ', JSON.stringify({ audioPaused: p2.audioPaused, frozen: p1.audioT === p2.audioT }));
  await page.keyboard.press('Space'); await sleep(1500); console.log('after resume  ', JSON.stringify(await state(page)));
  const d0 = await page.evaluate(() => Player.scenes[0].dur);
  await sleep(Math.max(1000, (d0 - 5) * 1000)); console.log('scene 2?      ', JSON.stringify(await state(page)));
  await page.evaluate(() => { Player.audio.currentTime = Player.audio.duration - 0.3; }); await sleep(600);
  await page.keyboard.press('Space'); await sleep(1200); console.log('pause at edge ', JSON.stringify(await state(page)));
  await sleep(2500); console.log('held?         ', JSON.stringify(await state(page)));
  await page.keyboard.press('Space'); await sleep(2500); console.log('resume -> next', JSON.stringify(await state(page)));
  console.log('errors', errs);
  try { await browser.disconnect(); } catch (e) { } child.kill();
})().catch(e => { console.error(e); process.exit(1); });
