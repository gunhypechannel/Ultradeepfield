const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await b.newPage(); await pg.goto('http://localhost:8125/icon.html');
  const L = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  for (const [out, file, o] of L) { const u = await pg.evaluate(([f, o]) => window.go(f, o), [file, o]); fs.writeFileSync(out, Buffer.from(u.split(',')[1], 'base64')); }
  await b.close(); })();
