# v492: the world bosses (Overlord, Conduit, Devourer, Warden, Matriarch, Tyrant, Wyrm, Colossus) and the five Elementals modelled
# from the owner's paintings like v491's super bosses; every painted boss shows its painting only in battle reports (a fixed,
# head-on camera) and keeps its code-built 3D model on the galaxy map (owner's choice: the 3D models work with the map).
# Battle reports: head-on camera, the boss no longer swings 45 degrees to its targets, every strike leaves from a point on the
# painting (mouth, cannon, core) and beams rake across the whole fleet to the edge of the screen.
import sys, json, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)

# --- the painting only where BOSS3D.paint is on (battle reports) ---
rep('let TH = null; const cache = {}; let LOD = 0;', 'let TH = null; const cache = {}; let LOD = 0, PAINT = 0;')
rep('  function artRelief(par, o) { const g = new TH.Group(); g.position.set(0, o.cy, o.z); g.userData.dyn = 1; par.add(g); const A = { g, ok: 0, at: {}, mat: null };',
    '  function artRelief(par, o) { const g = new TH.Group(); g.position.set(o.cx || 0, o.cy, o.z); g.userData.dyn = 1; par.add(g); const A = { g, ok: 0, at: {}, mat: null }; if (!PAINT) { g.visible = false; A.step = () => {}; A.wp = (n, p2, v) => v; return A; } // v492 the galaxy map keeps the 3D model')
rep('    artLoad(o.k, L => { if (!L.ok) return; const D = L.dep,', '    artLoad(o.k, L => { if (!L.ok || !g.parent) return; const D = L.dep,')
rep('const nx = LOD === 1 ? 110 : 220', 'const nx = LOD >= 1 ? 110 : 220')
rep('get lod() { return LOD; },', 'get lod() { return LOD; }, set paint(v) { PAINT = v ? 1 : 0; }, get paint() { return PAINT; },')
# Khezaroth and Medusara: painted only in battle reports, head-on there (out.art stops the swing)
rep('stormS.position.z = -16;', 'if (PAINT) stormS.position.z = -16;')
rep('    const aE = [0, 1].map(j => { const s2 = sprite(9,', '    if (PAINT) out.art = AR; const aE = [0, 1].map(j => { const s2 = sprite(9,')
rep('    const aE = [0, 1].map(j => { const s2 = sprite(3.2,', '    if (PAINT) out.art = AR; const aE = [0, 1].map(j => { const s2 = sprite(3.2,')

# --- the world bosses' paintings: crop size, the boss's box in the painting, mean depth, the strike point ---
M = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'tools/painted/meta.json'))
COL = {'overlord': '#c58bff', 'conduit': '#d9a0ff', 'devourer': '#b45cff', 'warden': '#9a6bff', 'matriarch': '#a8ff3a', 'tyrant': '#ff8a3a', 'wyrm': '#ffa040', 'colossus': '#c070ff',
       'el-ice': '#7fd8ff', 'el-fire': '#ff7a2a', 'el-light': '#ffd860', 'el-storm': '#b070ff', 'el-nature': '#7aff5a'}
SCL = {'wyrm': 4.2, 'colossus': 1.35, 'matriarch': .85, 'overlord': 1.4, 'devourer': 1.25}
pnt = ', '.join('"%s": [%d, %d, [%s], %s, [%d, %d], "%s", %s]' % (k, v['iw'], v['ih'], ', '.join(map(str, v['bb'])), v['dm'], v['m'][0], v['m'][1], COL[k], SCL.get(k, 1)) for k, v in M.items())
HELP = r'''  /* v492 a world boss modelled from its painting: the painted relief sized to the code-built model's solid parts (so its camera
     framing holds), those solid parts hidden, the effects kept; it leans into each attack, a glow gathers at its strike point
     (out.mouth, where the battle report's strikes leave from), and it flinches when hit. PNT: [crop w, h, boss box x0 y0 x1 y1,
     mean depth, strike point x y, colour]. */
  const PNT = { __PNT__ };
  function painted(k, out) { const P = PNT[k]; if (!P || !out || !out.grp || !PAINT) return out; const root = out.grp; root.updateMatrixWorld(true);
    const solid = o => o.isMesh && o.material && !Array.isArray(o.material) && o.material.blending !== TH.AdditiveBlending && !(o.material.transparent && o.material.opacity < .9), box = new TH.Box3(), hide = [];
    root.traverse(o => { if (solid(o)) box.expandByObject(o); if (o.isMesh || o.isLine || o.isPoints || o.isSprite) hide.push(o); }); if (box.isEmpty()) return out; // only the painting shows; the strikes are drawn across the field
    const sz = box.getSize(new TH.Vector3()), c = box.getCenter(new TH.Vector3()), [iw, ih, bb, dm, [mx, my], col] = P, pw = bb[2] - bb[0], ph = bb[3] - bb[1];
    const u = Math.min(Math.max(sz.x, sz.z) / pw, sz.y / ph) * 1.08 * (P[6] || 1), L = Math.max(pw, ph) * u, z0 = c.z + Math.max(sz.x, sz.z) * .15;
    const A = artRelief(root, { k, iw, ih, u, ox: (bb[0] + bb[2]) / 2, oy: (bb[1] + bb[3]) / 2, cx: c.x, cy: c.y, z: z0, D: L * .3, d0: dm, pitch: .6, at: { m: [mx, my] }, hide });
    out.art = A; out.mouth = A.at.m; const gl = sprite(1, col.length === 7 ? `rgba(${parseInt(col.slice(1, 3), 16)},${parseInt(col.slice(3, 5), 16)},${parseInt(col.slice(5, 7), 16)},1)` : col, "pnt_" + k); gl.material.opacity = 0; A.at.m.add(gl);
    const act0 = out.act, tick0 = out.tick; let mv = null; out.act = n => { if (act0) act0(n); mv = { n, t0: -1 }; };
    out.tick = t => { tick0(t); if (!A.ok) return; A.step(); let e = 0, h = 0; if (mv) { if (mv.t0 < 0) mv.t0 = t; const q = (t - mv.t0) / 1000; if (mv.n === "hit") h = Math.max(0, 1 - q / .45); else e = q < .6 ? q / .6 : q < 1.8 ? 1 : Math.max(0, 1 - (q - 1.8) / .8); if (q > 3) mv = null; }
      const sm = e * e * (3 - 2 * e); A.g.position.set(c.x + Math.sin(t * .09) * L * .006 * h, c.y + Math.sin(t * .0007) * L * .006, z0 + sm * L * .07); A.g.scale.setScalar(1 + sm * .035);
      A.mat.color.setScalar(1 + h * .4 + sm * .12); gl.material.opacity = sm * .95; gl.scale.setScalar(L * (.1 + .12 * sm) * (1 + .1 * Math.sin(t * .02))); };
    return out; }
'''.replace('__PNT__', pnt)
i = s.index('  /* v491 a boss modelled from its own painting'); s = s[:i] + HELP + s[i:]
rep('conduit, warden, overlord, devourer, matriarch, tyrant, wyrm, colossus, station, elemental, pentarch,',
    'conduit: (...a) => painted("conduit", conduit(...a)), warden: (...a) => painted("warden", warden(...a)), overlord: (...a) => painted("overlord", overlord(...a)), devourer: (...a) => painted("devourer", devourer(...a)), '
    'matriarch: (...a) => painted("matriarch", matriarch(...a)), tyrant: (...a) => painted("tyrant", tyrant(...a)), wyrm: (...a) => painted("wyrm", wyrm(...a)), colossus: (...a) => painted("colossus", colossus(...a)), station, '
    'elemental: kind => painted("el-" + kind, elemental(kind)), pentarch,')

# --- battle reports: paint on, head-on, no 45-degree swing ---
rep('BOSS3D.init(TH); BOSS3D.lod = MOBILE ? 2 : 0; const m3 = wbD(key).m3,', 'BOSS3D.init(TH); BOSS3D.lod = MOBILE ? 2 : 0; BOSS3D.paint = 1; const m3 = wbD(key).m3,')
a = 'wbEnv(WBR.r)); if (key === "epx") {'
rep(a, 'wbEnv(WBR.r)); BOSS3D.paint = 0; if (key === "epx") {')
rep('goal = WBR.y0 + (WBR.face || 0) * Math.PI / 4;', 'goal = WBR.y0 + (WBR.b.art ? 0 : (WBR.face || 0)) * Math.PI / 4;')
# head-on cameras for the world bosses and Elementals (same distance, straight in front)
def headon(m):
    k, y0, cx, cy, cz, rest = m.group(1), m.group(2), float(m.group(3)), m.group(4), float(m.group(5)), m.group(6)
    d = round((cx * cx + cz * cz) ** .5, 1)
    return '%s: [%s, [0, %s, %s], %s' % (k, y0, cy, ('%g' % d), rest)
s2 = re.sub(r'\b(khezaroth|medusara|elemental|matriarch|tyrant|wyrm|colossus|overlord|devourer|warden|conduit): \[([^,]+(?:\s*/\s*2)?), \[(-?[\d.]+), (-?[\d.]+), (-?[\d.]+)\], (\[[^\]]*\])', headon, s)
assert s2 != s and s2.count('[0, ') > s.count('[0, '); s = s2

# --- strikes leave from the painted strike point; beams rake across the fleet and run to the edge of the screen ---
rep('MO = k === "wym" && WBR.mouth && b.wbBox ?', 'PB = !!(WBR.b && WBR.b.art && WBR.b.art.ok), MO = (k === "wym" || PB) && WBR.mouth && b.wbBox ?')
rep('ctx.drawImage(glowSprite("rgba(255,170,60,1)"), MO.x - r * 2, MO.y - r * 2, r * 4, r * 4);', 'ctx.drawImage(glowSprite(PB && k !== "wym" ? WB[k].col : "rgba(255,170,60,1)"), MO.x - r * 2, MO.y - r * 2, r * 4, r * 4);')
rep('    if (S[0] === "sweep") ex += Math.sin((u - .5) * Math.PI) * W * .38; // the Wyrm\'s sweep: across the whole fleet',
    '    if (S[0] === "sweep" || PB) ex += Math.sin((u - .5) * Math.PI) * W * .38; // the Wyrm\'s sweep, and (v492) every painted boss\'s beam: across the whole fleet')
rep('const wide = k === "epx" || M.m === "judgement" ? 1.6 : 1, grow = Math.min(1, u * 5), x1 = cx + (ex - cx) * grow, y1 = cy + (ey - cy) * grow;',
    'const wide = k === "epx" || M.m === "judgement" ? 1.6 : 1, grow = Math.min(1, u * 5), x1 = cx + (ex - cx) * grow, y1 = cy + (ey - cy) * grow, run = PB ? Math.max(1, Math.hypot(W, H) / Math.max(1, Math.hypot(ex - cx, ey - cy))) * Math.min(1, u * 3) : 1, xe = cx + (x1 - cx) * Math.max(1, run), ye = cy + (y1 - cy) * Math.max(1, run);')
rep('ctx.lineWidth = lw * d * (.7 + .3 * Math.sin(t * .05)); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x1, y1); ctx.stroke(); }',
    'ctx.lineWidth = lw * d * (.7 + .3 * Math.sin(t * .05)); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(xe, ye); ctx.stroke(); }\n'
    '    if (PB && grow >= 1) { const dx = xe - cx, dy = ye - cy, L2 = dx * dx + dy * dy || 1; for (const i of tg) { const p = scr[i], q = clamp(((p.x - cx) * dx + (p.y - cy) * dy) / L2, 0, 1); if (Math.hypot(p.x - cx - dx * q, p.y - cy - dy * q) < W * .05 * wide) hit(p.x, p.y, .8, "r" + i + Math.round(u * 6)); } } /* v492 everything the beam crosses burns */')
s = re.sub(r"GAME_V = 491\b", "GAME_V = 492", s)
open(P, 'w', encoding='utf-8').write(s)
print('ok')
s = open(P, encoding='utf-8').read()
a = 'transparent: true, alphaTest: .05, side: TH.DoubleSide, toneMapped: false })'
assert s.count(a) == 1; s = s.replace(a, 'transparent: true, alphaTest: .01, side: TH.DoubleSide, toneMapped: false })')
open(P, 'w', encoding='utf-8').write(s)
s = open(P, encoding='utf-8').read()
for a in ['BOSS3D.init(TH); BOSS3D.lod = 1; const b = BOSS3D.prep(BOSS3D[D.m3]', 'BOSS3D.init(TH); BOSS3D.lod = MOBILE ? 1 : 0; X.b = BOSS3D.prep(BOSS3D[D.m3]()']:
    assert s.count(a) == 1, a; s = s.replace(a, a.replace('BOSS3D.init(TH);', 'BOSS3D.init(TH); BOSS3D.paint = 0;'))
open(P, 'w', encoding='utf-8').write(s)
