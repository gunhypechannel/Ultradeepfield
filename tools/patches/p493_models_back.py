# v493: owner: "No bosses get painted models". Every boss is its code-built 3D model again, in battle reports too (Khezaroth and
# Medusara included); the painting code stays dormant (BOSS3D.paint is never set, no skins are preloaded). Kept from v492: the
# head-on battle cameras and the strikes that cross the whole screen, now for every world boss's own model: each beam rakes
# across the fleet and runs to the screen edge, burning every ship it crosses, timed by each model's own move (WB_STRIKE).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('BOSS3D.paint = 1; const m3', 'BOSS3D.paint = 0; const m3')
rep('init(T) { TH = T; if (!ARL.medusara) setTimeout(() => { try { artLoad("khezaroth", () => {}); artLoad("medusara", () => {}); } catch (e) {} }, 0); }', 'init(T) { TH = T; }')
rep('PB = !!(WBR.b && WBR.b.art && WBR.b.art.ok)', 'PB = !!WB[k] /* v493 every world boss\'s strikes cross the screen */')
s = re.sub(r"GAME_V = 492\b", "GAME_V = 493", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')

# --- v493 Medusara remaster (owner: "clean it up, maybe remove the pillars on its rings and turn its rings in to glyphs that match"):
# no ruin towers on the rings and no small ruins on her face; her three rings become rings of gold Gorgon glyphs (eyes, serpents,
# crescents, eyed triangles, diamonds) between fine gold lines, turning slowly and flaring crimson while she charges her gaze ---
s = open(P, encoding='utf-8').read()
rep('for (let i = 0; i < (LO ? 3 : 6); i++) { const u = (i / 5 - .5) * 1.6', 'for (let i = 0; i < 0; i++) { const u = (i / 5 - .5) * 1.6')
GLY = r'''  // v493 Medusara's glyph rings: Gorgon glyphs on a band between fine lines (drawn for a RingGeometry, outer edge = texture radius)
  const medGlyTex = () => paint("medgly", 1024, (x, N) => { x.translate(N / 2, N / 2); x.strokeStyle = "#fff"; x.fillStyle = "#fff"; x.lineCap = "round"; x.lineJoin = "round";
    for (const [r, w] of [[.496, 6], [.481, 2.5], [.394, 2.5], [.379, 6]]) { x.lineWidth = w; x.beginPath(); x.arc(0, 0, N * r, 0, TAU); x.stroke(); }
    const n = 36, s = N * .027; for (let i = 0; i < n; i++) { x.save(); x.rotate(i / n * TAU); x.translate(0, -N * .4375); x.lineWidth = 5; const k = i % 6;
      if (k === 0) { x.beginPath(); x.moveTo(-s * 1.4, 0); x.quadraticCurveTo(0, -s * 1.1, s * 1.4, 0); x.quadraticCurveTo(0, s * 1.1, -s * 1.4, 0); x.stroke(); x.beginPath(); x.arc(0, 0, s * .38, 0, TAU); x.fill(); }
      else if (k === 1) { x.beginPath(); x.moveTo(-s * .2, -s * 1.3); x.bezierCurveTo(s * 1.1, -s * .8, -s * 1.1, s * .3, s * .3, s * 1.2); x.stroke(); x.beginPath(); x.arc(-s * .15, -s * 1.25, s * .28, 0, TAU); x.fill(); }
      else if (k === 2) { x.beginPath(); x.arc(0, 0, s, -Math.PI * .85, Math.PI * .85); x.stroke(); x.beginPath(); x.arc(s * .45, 0, s * .7, -Math.PI * .7, Math.PI * .7); x.stroke(); }
      else if (k === 3) { x.beginPath(); x.moveTo(0, -s * 1.3); x.lineTo(s * 1.15, s * .9); x.lineTo(-s * 1.15, s * .9); x.closePath(); x.stroke(); x.beginPath(); x.arc(0, s * .2, s * .3, 0, TAU); x.fill(); }
      else if (k === 4) { x.beginPath(); x.moveTo(0, -s * 1.2); x.lineTo(s * .7, 0); x.lineTo(0, s * 1.2); x.lineTo(-s * .7, 0); x.closePath(); x.stroke(); x.beginPath(); x.moveTo(0, -s * .5); x.lineTo(0, s * .5); x.stroke(); }
      else { for (const dy of [-1, 0, 1]) { x.beginPath(); x.arc(0, dy * s * .8, s * .22, 0, TAU); x.fill(); } }
      x.restore(); x.save(); x.rotate((i + .5) / n * TAU); x.beginPath(); x.arc(0, -N * .4375, s * .18, 0, TAU); x.fill(); x.restore(); } }, false);
'''
rep('  function medusara() {', GLY + '  function medusara() {')
WRAP = r'''    { // v493 glyph rings in place of the gold rails and their ruin towers
      const gT = medGlyTex(), gM = c => new TH.MeshBasicMaterial({ map: gT, color: c, transparent: true, opacity: .9, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false });
      const gR = (par, R, w, op) => { const m = new TH.Mesh(new TH.RingGeometry(R * (1 - w), R * (1 + w), LO ? 72 : 144, 1), gM(0xffc860)); m.rotation.x = Math.PI / 2; m.userData.dyn = 1; m.userData.op = op; par.add(m); return m; };
      const TW = new Set(towers.map(w => w.t)); for (const G of [RR, RR3]) [...G.children].forEach(c => { if (!TW.has(c)) G.remove(c); }); [...RR2.children].forEach(c => { if (c !== rr2) RR2.remove(c); }); towers.forEach(w => w.t.clear());
      rr2.geometry.dispose(); rr2.geometry = new TH.RingGeometry(32 * .76, 32 * 1.0, LO ? 72 : 144, 1); rr2.material.map = gT; rr2.material.color.set(0xffc860); rr2.material.needsUpdate = true;
      const GR = [gR(RR, ringR, .14, 1), gR(RR3, 39, .1, .75), rr2], G2 = gR(RR, ringR * .86, .035, .5), gold = new TH.Color(0xffc860), crim = new TH.Color(0xff2a4a), tick1 = out.tick;
      out.tick = t => { tick1(t); const ch = f("charge", t), chg = ch < 0 ? 0 : ss(0, .7, ch) * (1 - ss(.94, 1, ch)), fd = f("die", t), die = fd < 0 ? 0 : fd, aw = drv.awake != null ? drv.awake : 1, live = 1 - ss(.15, .5, die), fr = f("ring", t), rg = bell(fr, .05, .2, .7, .9);
        GR.forEach((m, i) => { m.material.color.copy(gold).lerp(crim, Math.min(1, chg * 1.4)); m.material.opacity = Math.min(1, (i === 2 ? .7 : m.userData.op) * aw * live * (1 + chg * .6 + rg * .8)) * (.85 + .15 * Math.sin(t * .002 + i)); });
        G2.rotation.z = -t * .0002 * (1 + chg * 3); G2.material.color.copy(GR[0].material.color); G2.material.opacity = .5 * aw * live * (1 + rg); }; }
'''
i0 = s.index('  function medusara() {'); END = '    tick(0); bake(body); return out; }'; j = s.index(END, i0)
s = s[:j] + WRAP + s[j:]
open(P, 'w', encoding='utf-8').write(s); print('med ok')

# --- fix (v492 bug): with the painting off, Khezaroth's and Medusara's wrappers still attach glows to the painting's anchor points;
# the anchors were never made, so building either boss threw (the galaxy map and live fights). Anchors now always exist. ---
s = open(P, encoding='utf-8').read()
rep('if (!PAINT) { g.visible = false; A.step = () => {}; A.wp = (n, p2, v) => v; return A; }',
    'if (!PAINT) { g.visible = false; for (const n in o.at || {}) { const a = new TH.Object3D(); g.add(a); A.at[n] = a; } A.step = () => {}; A.wp = (n, p2, v) => v; return A; }')
open(P, 'w', encoding='utf-8').write(s); print('fix ok')

# --- the 3D models' own camera framing again (v490 WB_VIEW); the head-on cameras were set for the paintings ---
s = open(P, encoding='utf-8').read()
i = s.index('const WB_VIEW = {'); j = s.index('};', i)
s = s[:i] + 'const WB_VIEW = { supercube: [0, [-6, 3, 31], [0, .6, 0]], omega: [0, [-6, 4, 26], [0, 1.5, 0]], vaelthar: [-.35, [-21, 9, 50], [0, 9, 0]], aexion: [-.4, [-26, 10, 64], [0, 9, 0]], khezaroth: [0, [-24, 20, 96], [0, 13, 4]], medusara: [0, [-20, 22, 104], [0, 16, 0]], aexW: [-.4, [-26, 16, 70], [0, 21, 0]] /* v486 Warform: the sweep crosses the fleet */, elemental: [-.2, [-8, 4, 62], [0, 0, 0]], pentarch: [0, [-10, 6, 120], [0, 0, 0]], matriarch: [-.55, [-12, 8, 36], [0, 6.5, 0]], tyrant: [.08, [-4, 7, 56], [1, -2.5, 0]], wyrm: [0, [-6, 21, 52], [0, 10, 0]], colossus: [-.35, [-8, 8, 37], [0, 8.5, 0]], overlord: [-Math.PI / 2, [-10, 4, 32], [0, -1.5, 0]], devourer: [Math.PI, [-8, 7, 36], [3, 0, 0]], warden: [-Math.PI / 2, [-7, 3, 27], [0, 0, 0]], conduit: [0, [0, 6, 25], [0, 6, 0]] ' + s[j:]
open(P, 'w', encoding='utf-8').write(s); print('views ok')
