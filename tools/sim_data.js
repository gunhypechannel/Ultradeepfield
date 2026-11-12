// Prints the battle simulator's data tables exactly as the game holds them once its script has run (after every Object.assign that
// adds bosses and units), for tools/sim_bundle.py. Serves docs/ itself; usage: node tools/sim_data.js NAME NAME ...
const { chromium } = require('playwright'), http = require('http'), fs = require('fs'), path = require('path');
const DOCS = path.join(__dirname, '..', 'docs'), names = process.argv.slice(2);
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p === '/') p = '/index.html'; const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f)) { r.statusCode = 404; return r.end(); } r.end(fs.readFileSync(f)); }).listen(0, async () => {
  const port = srv.address().port, b = await chromium.launch(), pg = await b.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); await pg.route(/^https?:\/\/(?!localhost)/, r => /three\.min\.js/.test(r.request().url()) && process.env.THREE_JS ? r.fulfill({ path: process.env.THREE_JS, contentType: 'application/javascript' }) : r.abort());
  await pg.route('**/index.html', async r => { let t = fs.readFileSync(path.join(DOCS, 'index.html'), 'utf8'); const ms = [...t.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)], m = ms.reduce((a, x) => x[1].length > a[1].length ? x : a);
    const body = m[1], i = body.trimEnd().lastIndexOf('})();'), hook = `window.__simdata = () => JSON.stringify({ ${names.map(n => `${n}: typeof ${n} === "undefined" ? null : ${n}`).join(', ')} });\n`;
    t = t.slice(0, m.index) + m[0].replace(body, body.slice(0, i) + hook + body.slice(i)) + t.slice(m.index + m[0].length); r.fulfill({ body: t, contentType: 'text/html' }); });
  await pg.goto(`http://localhost:${port}/index.html`, { waitUntil: 'commit' }).catch(() => {});
  try { await pg.waitForFunction(() => typeof window.__simdata === 'function', null, { timeout: 180000 }); } catch (e) { console.error('the game script did not finish:', errs.slice(0, 3)); process.exit(1); }
  process.stdout.write(await pg.evaluate(() => window.__simdata())); await b.close(); srv.close(); });
