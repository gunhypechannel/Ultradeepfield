const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const pg = await b.newPage();
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('http://localhost:8124/', { waitUntil: 'commit' }).catch(() => {}); await pg.waitForTimeout(18000);
  const r = await pg.evaluate(() => __dbg.ev(`JSON.stringify([...new Set([...Object.keys(ADV_MOOD_L), ...Object.values(AWE).flat()])].filter(t => !VOICE.clips[voiceKey(t)]).map(t => ({ key: voiceKey(t), line: t, mood: ADV_MOOD_L[t] || "awe" })))`));
  fs.writeFileSync('../miss584.json', r); console.log(r.length, JSON.parse(r).length); await b.close(); })();
