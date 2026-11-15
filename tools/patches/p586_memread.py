# v586 (fb-20261115): memory readout for crash reports (owner chose this before any memory cuts).
# The v580 iPhone crashes and the v579 iPad ones did not happen during the cold map build: the phone survived it and closed 25-70 s
# later in normal play, so memory fills up over time. iOS has no performance.memory, so the crash beat could not say what was big.
# memEst() estimates, at most every 12 s: texture memory per 3D world (gal/col/stu, MB and texture count), the studio's cached ship
# pictures (art, artN), the paintings decoded on the page (img, imgN) and all canvases on the page (cv). It goes into every
# heartbeat as "mx", so the next crash report shows what was holding memory, and a "memory ~N MB" crumb is written whenever the
# total rises 80 MB above its previous peak, so the flight log shows when it grew. Read-only: nothing is freed or changed.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
MEM = r'''/* fb-20261115 memory readout for crash reports (MB, estimated): textures per 3D world, cached ship pictures, decoded paintings, canvases */
function memEst() { try { const T = Date.now(); if (G.memEst && T - G.memEst.t < 12000) return G.memEst.v;
  const px = im => !im ? 0 : Array.isArray(im) ? im.reduce((a, x) => a + px(x), 0) : (im.naturalWidth || im.width || 0) * (im.naturalHeight || im.height || 0), v = {};
  for (const [k, W] of [["gal", G3], ["col", C3], ["stu", STU]]) { if (!W || !W.scene || !W.scene.traverse) continue; const seen = new Set(); let b = 0;
    W.scene.traverse(o => { const ms = Array.isArray(o.material) ? o.material : o.material ? [o.material] : []; for (const m of ms) for (const q in m) { const t = m[q]; if (t && t.isTexture && !seen.has(t)) { seen.add(t); b += px(t.image) * 4 * (t.generateMipmaps === false ? 1 : 1.33); } } });
    v[k] = Math.round(b / 1e6); v[k + "N"] = seen.size; }
  { const C = (STU && STU.cache) || G.stuCache; let b = 0, n = 0; if (C) for (const k in C) { const c = C[k]; if (c && c.getContext) { b += c.width * c.height * 4; n++; } } v.art = Math.round(b / 1e6); v.artN = n; }
  { let b = 0, n = 0; for (const im of document.images) if (im.complete && im.naturalWidth && im.isConnected) { b += im.naturalWidth * im.naturalHeight * 4; n++; } v.img = Math.round(b / 1e6); v.imgN = n; }
  { let b = 0; for (const c of document.getElementsByTagName("canvas")) b += c.width * c.height * 4; v.cv = Math.round(b / 1e6); }
  const tot = (v.gal || 0) + (v.col || 0) + (v.stu || 0) + v.art + v.img + v.cv; v.tot = tot; G.memEst = { t: T, v };
  if (tot > (G.memPk || 0) + 80 && !document.hidden) { G.memPk = tot; crumb(`memory ~${tot} MB (map ${v.gal || 0}, base ${v.col || 0}, studio ${(v.stu || 0) + v.art}, paintings ${v.img}, canvases ${v.cv})`); }
  return v; } catch (e) { return null; } }
function crumbBeat() {'''
rep('function crumbBeat() {', MEM)
rep('mt: typeof MEMT !== "undefined" ? MEMT : null, /* v537 the memory meter */',
    'mt: typeof MEMT !== "undefined" ? MEMT : null, mx: memEst(), /* v537 the memory meter; fb-20261115 mx = memory readout */')
s2 = re.sub(r"GAME_V = 584\b", "GAME_V = 586", s); assert s2 != s; s = s2  # v585 was voice only, no game version
open(P, 'w', encoding='utf-8').write(s); print('ok')
