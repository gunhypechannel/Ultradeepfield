# v562 the Titans remastered to match the owner's painting ("refine and remaster the new titans images, I just want everything to be
# breathtaking"). Every hull gets hand-made plating: panel rows, seams, rivet clusters and glowing light slits (red on the Armageddon,
# blue on the Sovereign Ark, emerald on the Harbinger), so the ships read like the painting instead of flat blocks.
# Armageddon: gothic spire clusters on its weapon towers and a cathedral of spires along its spine, a hotter red reactor glow.
# Sovereign Ark: brighter silver plating with gold, blue engine light. Eclipse Harbinger: a violet heart (the painting's core), a
# crown of dark spires above it and a hanging city of spires below.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function titanMats(k) {', '''/* v562 hand-made plating for the Titans: panels, seams, rivets and light slits (the emissive map) */
const TPLATE = {}; function titanPlate(k) { if (TPLATE[k]) return TPLATE[k]; const N = 512, mk = () => { const c = document.createElement("canvas"); c.width = c.height = N; return c; }, c = mk(), e = mk(), x = c.getContext("2d"), y = e.getContext("2d"), r = rnd(hash(k) + 77);
  const O = { armageddon: { b: [150, 150, 158], sl: ["#ff2a12", "#ff5a2a", "#ff9a50"], p: .16, rp: 1 }, sovereign: { b: [205, 210, 220], sl: ["#5fc8ff", "#bfe8ff"], p: .3, gold: 1 }, harbinger: { b: [140, 144, 150], sl: ["#3dff9a", "#b06bff"], p: .22 } }[k] || { b: [160, 160, 160], sl: ["#fff"], p: .2 };
  x.fillStyle = "#222"; x.fillRect(0, 0, N, N); y.fillStyle = "#000"; y.fillRect(0, 0, N, N); const rows = 8, hh = N / rows;
  for (let i = 0; i < rows; i++) { let xx = 0; const yy = i * hh; while (xx < N) { const ww = 26 + r() * 74, v = .72 + r() * .4, gd = O.gold && r() < .1;
      x.fillStyle = gd ? `rgb(${200 * v | 0},${150 * v | 0},${60 * v | 0})` : `rgb(${O.b[0] * v | 0},${O.b[1] * v | 0},${O.b[2] * v | 0})`; x.fillRect(xx + 1.5, yy + 1.5, ww - 3, hh - 3);
      x.fillStyle = "rgba(255,255,255,.14)"; x.fillRect(xx + 1.5, yy + 1.5, ww - 3, 2); x.fillStyle = "rgba(0,0,0,.4)"; x.fillRect(xx + 1.5, yy + hh - 4, ww - 3, 2.5);
      if (r() < .3) { x.fillStyle = "rgba(0,0,0,.35)"; for (let q = 0; q < 4; q++) x.fillRect(xx + 6 + q * 7, yy + 7, 3, 3); }
      if (r() < .22) { x.fillStyle = "rgba(0,0,0,.25)"; x.fillRect(xx + ww * .2, yy + hh * .3, ww * .6, hh * .4); }
      if (r() < O.p) { const sw = ww * (.3 + r() * .5), sx = xx + (ww - sw) / 2, sy = yy + hh * (.4 + r() * .25), sl = 3 + r() * 3, col = O.sl[r() * O.sl.length | 0];
        x.fillStyle = col; x.fillRect(sx, sy, sw, sl); y.fillStyle = col; y.fillRect(sx, sy, sw, sl); y.globalAlpha = .3; y.fillRect(sx - 3, sy - 3, sw + 6, sl + 6); y.globalAlpha = 1; }
      xx += ww; } x.fillStyle = "rgba(0,0,0,.8)"; x.fillRect(0, yy, N, 2); }
  const T = t => { const tx = new TH.CanvasTexture(t); tx.wrapS = tx.wrapT = TH.RepeatWrapping; tx.repeat.set(O.rp || 2, O.rp || 2); tx.anisotropy = 4; return tx; };
  return (TPLATE[k] = { map: T(c), emi: T(e) }); }
function titanMats(k) {''')
# use the plating on the hulls (the colour multipliers keep each hull's tone; the slits glow through the emissive map)
rep('''  if (S) S.cache[key] = o; return o; }
function titanModel(k, g) {''', '''  try { const PL = titanPlate(k); for (const m of [o.hull, o.dark]) { m.map = PL.map; m.emissive = new TH.Color(0xffffff); m.emissiveMap = PL.emi; m.emissiveIntensity = m === o.hull ? 1.25 : .7; m.needsUpdate = true; } } catch (e) {} /* v562 */
  if (S) S.cache[key] = o; return o; }
function titanModel(k, g) {''')
rep('glow: E(0xff4a1a, "accent"), hot: E(0xffb070, "engine"), core: E(0xfff0d8, "win"), win: E(0xff7a3a, "win") };', 'glow: E(0xff2a12, "accent"), hot: E(0xffb070, "engine"), core: E(0xfff0d8, "win"), win: E(0xff5a2a, "win") };')
rep('trim: P({ color: 0x9a6514, metalness: 1,', 'trim: P({ color: 0xff6c12, metalness: 1,')
rep('o = { hull: P({ map: T.hull, color: 0xf4f6fa, roughness: .2, metalness: .72, clearcoat: .9 }, "hull")', 'o = { hull: P({ map: T.hull, color: 0xffffff, roughness: .24, metalness: .66, clearcoat: .9 }, "hull")')
# Armageddon: gothic spires
rep('add(mesh(new TH.ConeGeometry(.36, .55, 6), MT.dark), x, .86 + h + .27, z); for (let j = 0; j < 3; j++)',
    'add(mesh(new TH.ConeGeometry(.24, 1.25, 6), MT.dark), x, .86 + h + .62, z); for (let q = 0; q < 4; q++) { const a = q / 4 * TAU + .4; add(mesh(new TH.ConeGeometry(.08, .62, 5), MT.dark), x + Math.cos(a) * .27, .86 + h + .3, z + Math.sin(a) * .27); } box(.03, .5, .03, MT.glow, x, .86 + h + .3, z + .245); for (let j = 0; j < 3; j++)')
rep('    for (const z of [.42, -.42]) for (let i = 0; i < 5; i++) { const x = -3.0 + i * .32;', '''    for (let i = 0; i < 9; i++) { const x = -3.5 + i * .19, hS = .5 + Math.sin(i / 8 * Math.PI) * 1.1; cylY(.07, .1, hS, MT.dark, x, 1.25 + hS / 2, 0, 6); add(mesh(new TH.ConeGeometry(.08, .45, 6), MT.dark), x, 1.25 + hS + .22, 0); box(.02, hS * .6, .02, MT.glow, x + .08, 1.25 + hS * .5, 0); } /* v562 the cathedral of spires on its spine */
    for (const z of [.42, -.42]) for (let i = 0; i < 5; i++) { const x = -3.0 + i * .32;''')
# Harbinger: violet heart, crown and hanging city
rep('add(mesh(new TH.SphereGeometry(.82, 32, 20), MT.glow)); TI.core = g.children[g.children.length - 1];', '''add(mesh(new TH.SphereGeometry(.82, 32, 20), MT.win)); TI.core = g.children[g.children.length - 1]; /* v562 the violet heart */
    for (let j = 0; j < 22; j++) { const a = j / 22 * TAU + r() * .2, rr = .35 + r() * 1.15, L = .5 + r() * 1.3 * (1.6 - rr / 1.5); const sp = add(mesh(new TH.ConeGeometry(.05 + r() * .07, L, 6), MT.dark), Math.cos(a) * rr, -.2 - L / 2, Math.sin(a) * rr); sp.rotation.x = Math.PI; if (j % 3 === 0) add(mesh(new TH.SphereGeometry(.035, 6, 4), j % 2 ? MT.glow : MT.win), Math.cos(a) * rr, -.25 - L * .4, Math.sin(a) * rr); } /* the hanging city */
    for (let j = 0; j < 7; j++) { const a = j / 7 * TAU, rr = j ? .95 : 0, L = j ? .7 + r() * .4 : 1.4; add(mesh(new TH.ConeGeometry(j ? .07 : .12, L, 6), MT.dark), Math.cos(a) * rr, .85 + L / 2, Math.sin(a) * rr); } /* its crown */''')
s2 = re.sub(r"GAME_V = 561\b", "GAME_V = 562", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
