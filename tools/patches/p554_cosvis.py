# v554 the cosmetics come alive in the game (owner: "I want it all").
# Warp trails: a fleet whose commander has a trail leaves a chain of glowing season-coloured lights behind it on the galaxy map, seen
# by everyone. Homeworld auras: two counter-turning halo rings, a soft glow and two orbiting lights round the homeworld (the season set
# aura is brighter). Animated skin: a homeworld wearing its season skin pulses with a corona. Laser colour: your side fires in your
# season colours in your battles and replays. Advisor outfit: her painted outfit when it exists, a season-coloured hologram until then.
# Wheel theme: the Glyph Wheel's rings take the season colours. Clip frame: shared battle clips get a season border and label.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

JS = r'''
/* ---------- v554 cosmetics on the map, in battle, on the wheel and in clips ---------- */
function cosCol(uid, k) { const d = cosDef(cosEq(uid, k)); if (!d) return null; const C = G.cosC || (G.cosC = {}); return C[d.id] || (C[d.id] = { id: d.id, d, c1: TH ? new TH.Color(d.col) : null, c2: TH ? new TH.Color(d.col2) : null }); }
function cosTrailFree(W, o) { if (o.ct) for (const sp of o.ct) { W.scene.remove(sp); sp.material.dispose(); } o.ct = o.cth = o.ctId = null; }
function cosRingTex(W, d, kind) { const key = "cr" + kind + d.id; if (W.glow[key]) return W.glow[key]; const N = 256, c = document.createElement("canvas"); c.width = c.height = N; const x = c.getContext("2d"), R = N / 2; x.translate(R, R);
  x.shadowColor = d.col; x.shadowBlur = 14; x.lineWidth = kind ? 3 : 5; const g = x.createLinearGradient(-R, 0, R, 0); g.addColorStop(0, d.col); g.addColorStop(.5, d.col2); g.addColorStop(1, d.col); x.strokeStyle = g;
  if (kind) { x.setLineDash([10, 9]); x.beginPath(); x.arc(0, 0, R * .9, 0, TAU); x.stroke(); }
  else { x.beginPath(); x.arc(0, 0, R * .78, 0, TAU); x.stroke(); x.lineWidth = 2; x.globalAlpha = .7; x.beginPath(); x.arc(0, 0, R * .7, .3, 2.6); x.stroke(); x.beginPath(); x.arc(0, 0, R * .7, 3.4, 5.8); x.stroke(); x.globalAlpha = 1;
    x.fillStyle = "#fff"; for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; x.beginPath(); x.arc(Math.cos(a) * R * .78, Math.sin(a) * R * .78, 3.2, 0, TAU); x.fill(); } }
  const tx = new TH.CanvasTexture(c); tx.encoding = TH.sRGBEncoding; return (W.glow[key] = tx); }
function cosAuraObj(W, C) { const g = new TH.Group(), d = C.d, wt = W.glow.wht || (W.glow.wht = glowTex("255,255,255", 1));
  const r1 = new TH.Sprite(W.additive(cosRingTex(W, d, 0), 0xffffff, d.set ? 1 : .85)), r2 = new TH.Sprite(W.additive(cosRingTex(W, d, 1), 0xffffff, .6)), glow = new TH.Sprite(W.additive(wt, C.c1, d.set ? .55 : .35));
  const moons = [new TH.Sprite(W.additive(wt, C.c2, .95)), new TH.Sprite(W.additive(wt, C.c1, .95))]; for (const s of [glow, r2, r1, ...moons]) { s.renderOrder = 7; s.material.depthWrite = false; g.add(s); }
  g.userData = { r1, r2, glow, moons, set: d.set }; return g; }
function cosAuraFree(o) { if (!o.au) return; o.grp.remove(o.au); o.au.traverse(x => { if (x.material) x.material.dispose(); }); o.au = null; o.auId = null; }
function cosSkxFree(o) { if (!o.skx) return; o.grp.remove(o.skx); o.skx.material.dispose(); o.skx = null; }
function cosShot(b, i, side) { if (b.lzD === undefined) { const r = b.r || {}, sd = r.kind === "attack" ? "a" : r.kind === "raid" || r.kind === "defense" ? "d" : null, d = cosDef(cosEq(G.me, "laser")); b.lzD = d && sd ? { side: sd, c1: d.col, c2: d.col2 } : null; }
  const L = b.lzD; return L && side === L.side ? (i % 2 ? L.c2 : L.c1) : null; }
function whlPal() { const d = S && cosDef(cosOf().eq.wheel); if (!d) return { id: "", o: "#7af4ff", o2: "#55d6e8", b: "#c88aff", b2: "#ff4fc6", k: "#7af4ff", bg: "#22145a" };
  return { id: d.id, o: d.col, o2: d.col, b: d.col2, b2: d.col, k: d.col2, bg: "#160d26" }; }
'''
rep('function cosOf() {', JS + 'function cosOf() {')

# warp trails on the map
rep('o.pt = pt; o.f = f;', '''o.pt = pt; o.f = f;
    { const cu = noLine || path.park ? null : cosCol(fleetFlagU(f, hostile), "trail"); /* v554 warp trails */
      if (cu) { if (!o.ct || o.ctId !== cu.id) { cosTrailFree(W, o); o.ctId = cu.id; o.ct = []; o.cth = []; const tx = W.glow.ctr || (W.glow.ctr = glowTex("255,255,255", 1)); for (let i = 0; i < 16; i++) { const sp = new TH.Sprite(W.additive(tx, i % 2 ? cu.c2 : cu.c1, 0)); sp.renderOrder = 12; sp.material.depthWrite = false; W.scene.add(sp); o.ct.push(sp); } }
        const nw = performance.now(); if (!o.ctT || nw - o.ctT > 80) { o.ctT = nw; o.cth.unshift([pt.x, pt.y, pt.z]); if (o.cth.length > 16) o.cth.length = 16; }
        for (let i = 0; i < 16; i++) { const sp = o.ct[i], q = o.cth[i]; if (!q || i === 0) { sp.visible = false; continue; } sp.visible = true; sp.position.set(q[0], q[1], q[2]); const k = 1 - i / 16; sp.scale.setScalar(fs * (3.2 * k + .5) * (1 + .18 * Math.sin(t * .012 + i * 1.7))); sp.material.opacity = .9 * k; } }
      else if (o.ct) cosTrailFree(W, o); }''')
rep('function disposeObj(W, o) {', 'function disposeObj(W, o) { cosTrailFree(W, o);')
# homeworld auras and the animated skin's corona
rep('      if (o.sh) { o.sh.scale.setScalar(o.rad * 1.55); o.sh.rotation.y = t * .00015; W.shieldList.push([p, o]); } }', '''      if (o.sh) { o.sh.scale.setScalar(o.rad * 1.55); o.sh.rotation.y = t * .00015; W.shieldList.push([p, o]); } }
    { const home = p.kind === "home" && p.owner && !fg && dc < 900, au = home ? cosCol(p.owner, "aura") : null; /* v554 homeworld auras */
      if (au) { if (!o.au || o.auId !== au.id) { cosAuraFree(o); o.auId = au.id; o.au = cosAuraObj(W, au); o.grp.add(o.au); }
        const A = o.au.userData, R = o.rad; A.r1.material.rotation = t * .00055; A.r2.material.rotation = -t * .00032; A.r1.scale.setScalar(R * (A.set ? 4.4 : 3.9)); A.r2.scale.setScalar(R * 5.1); A.glow.scale.setScalar(R * (3.4 + .35 * Math.sin(t * .0026)));
        for (let i = 0; i < A.moons.length; i++) { const m = A.moons[i], a = t * (i ? -.0009 : .0007) + i * 2.4, rr = R * (2.05 + i * .4); m.position.set(Math.cos(a) * rr, Math.sin(a * .8 + i) * R * .35, Math.sin(a) * rr); m.scale.setScalar(R * (.55 + .12 * Math.sin(t * .004 + i))); } }
      else if (o.au) cosAuraFree(o);
      const sx = home && pxOf(p) ? cosCol(p.owner, "skinx") : null, skOn = sx && VP_SEASONS[sx.d.si] && VP_SEASONS[sx.d.si][2] === p.px;
      if (skOn) { if (!o.skx) { o.skx = new TH.Sprite(W.additive(W.glow.wht || (W.glow.wht = glowTex("255,255,255", 1)), sx.c1, .7)); o.skx.renderOrder = 6; o.skx.material.depthWrite = false; o.grp.add(o.skx); }
        const pu = .5 + .5 * Math.sin(t * .0028); o.skx.scale.setScalar(o.rad * (2.6 + .8 * pu)); o.skx.material.opacity = .35 + .45 * pu; o.skx.material.color.copy(pu > .5 ? sx.c1 : sx.c2); }
      else if (o.skx) cosSkxFree(o); }''')
rep('for (const [id, o] of W.planets) if (!seen.has(id)) { hiDrop(W, o);', 'for (const [id, o] of W.planets) if (!seen.has(id)) { hiDrop(W, o); cosAuraFree(o); cosSkxFree(o);')
# laser colours in battle
rep('col = f.col || shotCol((Q[v.s] || {}).k, f.side)', 'col = f.col || cosShot(b, v.s, f.side) || shotCol((Q[v.s] || {}).k, f.side)')
# the Advisor's outfit
rep('src="${ADV_ART}" alt=""', 'src="${advArt()}" style="${advFx()}" alt=""', 5)
rep('cwEq: d => { const C = cosOf();', 'cwEq: d => { const C = cosOf(); if (d.k === "adv") { const h = document.getElementById("advh"); if (h) h.remove(); }')
# the wheel theme
rep('function whlBuild(px) {', 'function whlBuild(px) { const PL = whlPal();')
rep('return { px, bg, outer, prize, ringB, ringC, core }; }', 'return { px, th: PL.id, bg, outer, prize, ringB, ringC, core }; }')
rep('if (!G.whlOff || G.whlOff.px !== px) G.whlOff = whlBuild(px);', 'if (!G.whlOff || G.whlOff.px !== px || G.whlOff.th !== whlPal().id) G.whlOff = whlBuild(px);')
rep('glow(x, "#7af4ff", R * .03); x.strokeStyle = "rgba(122,244,255,.95)"', 'glow(x, PL.o, R * .03); x.strokeStyle = PL.o')
rep('x.fillStyle = i % 3 === 1 ? "#c8fbff" : "#9fe9ff"; glow(x, "#55d6e8", R * .045)', 'x.fillStyle = i % 3 === 1 ? "#ffffff" : PL.o; glow(x, PL.o2, R * .045)')
rep('glow(x, "#c88aff", R * .03); x.strokeStyle = "rgba(210,150,255,.9)"', 'glow(x, PL.b, R * .03); x.strokeStyle = PL.b')
rep('x.fillStyle = i % 3 ? "#ecd4ff" : "#ff9ae6"; glow(x, i % 3 ? "#c88aff" : "#ff4fc6", R * .04)', 'x.fillStyle = i % 3 ? "#ffffff" : PL.b2; glow(x, i % 3 ? PL.b : PL.b2, R * .04)')
rep('glow(x, "#7af4ff", R * .04); x.strokeStyle = "rgba(150,248,255,.95)"', 'glow(x, PL.k, R * .04); x.strokeStyle = PL.k')
rep('g.addColorStop(0, "#22145a")', 'g.addColorStop(0, PL.bg)')
# the clip frame
rep('x.fillText(CLIP_URL, W / 2, H - 56);', '''x.fillText(CLIP_URL, W / 2, H - 56);
    { const cd = cosDef(cosOf().eq.clip); if (cd) { const gg = x.createLinearGradient(0, 0, W, H); gg.addColorStop(0, cd.col); gg.addColorStop(.5, cd.col2); gg.addColorStop(1, cd.col); x.strokeStyle = gg; x.lineWidth = 16; x.shadowColor = cd.col; x.shadowBlur = 24; x.strokeRect(8, 8, W - 16, H - 16); x.shadowBlur = 0; /* v554 the season clip frame */
      x.fillStyle = cd.col; const cr = (cx, cy, sx, sy) => { x.beginPath(); x.moveTo(cx, cy); x.lineTo(cx + 70 * sx, cy); x.lineTo(cx, cy + 70 * sy); x.closePath(); x.fill(); }; cr(0, 0, 1, 1); cr(W, 0, -1, 1); cr(0, H, 1, -1); cr(W, H, -1, -1);
      x.fillStyle = cd.col2; x.font = "700 20px 'Rajdhani',sans-serif"; x.fillText(`${COS_SEA[cd.si].toUpperCase()} SEASON`, W / 2, H - 22); } }''')
rep('clip: "Your shared battle clips get this season frame.", skinx: "Brings your season planet skin to life: a pulsing corona on the map and in your world view." }', 'clip: "Your shared battle clips get this season frame.", skinx: "Brings your season planet skin to life: your homeworld pulses with a season corona on the galaxy map while it wears the skin." }')
s2 = re.sub(r"GAME_V = 553\b", "GAME_V = 554", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
