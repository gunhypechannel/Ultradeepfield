"""v739: three slow seasons. The Season of the Signal joins the prologue between the Omens and the Countdown (PRO 2 -> 3),
twelve weekly omens instead of eight (four new: the Cube's count, voices from the Abyss, five lights, a signal nobody sent),
a new prologue finale (om3 Crossed Signals), and every later season moves four weeks."""
import sys, re, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:120])
    s = s.replace(a, b)

rep("const GAME_V = 738;", "const GAME_V = 739;")
# 1. three prologue seasons; the Signal's cosmetics set is 13 (12 is the Carcinid set)
rep("return t - ((new Date(t).getUTCDay() + 6) % 7) * 864e5; } } catch (e) {} return Date.UTC(2026, 10, 9); })(), PRO = 2; /* v575 seasons 1 and 2 are the prologue */",
    "return t - ((new Date(t).getUTCDay() + 6) % 7) * 864e5; } } catch (e) {} return Date.UTC(2026, 10, 9); })(), PRO = 3, PRO_COS = [10, 13, 11]; /* v575 seasons 1 and 2 are the prologue */ /* v739 three slow seasons: Omens, the Signal, the Countdown (cosmetics sets 10, 13, 11) */")
rep("seaCos = si => si < PRO ? 10 + Math.max(0, si) : seaCyc(si);",
    "seaCos = si => si < PRO ? PRO_COS[Math.max(0, si)] : seaCyc(si);")
rep('["Season of the Countdown", "#ffcf6a", "countdown", "Countdown Keeper"]];',
    '["Season of the Countdown", "#ffcf6a", "countdown", "Countdown Keeper"], ["The Carcinid Tide", "#e8b45a", "abyssreef", "Tidebreaker"], ["Season of the Signal", "#5fe8d0", "signal", "Signal Keeper"]]; /* v739 12: the Carcinid set (never a season), 13: the Signal */')
rep('"Omens", "Countdown", "Carcinid"], COS_C2 = [', '"Omens", "Countdown", "Carcinid", "Signal"], COS_C2 = [')
m = re.search(r'COS_C2 = \[[^\]]*\]', s); assert m
s = s[:m.end() - 1] + ', "#3fe8f0", "#d8fff6"' + s[m.end() - 1:]
rep("...Object.fromEntries([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].flatMap(", "...Object.fromEntries([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13].flatMap(")
rep("cosNo = cx => cx >= 10 ? cx - 9 : cx + 1 + PRO, cosLive = (cx, cur) => cx >= 10 ? cur >= cx - 10 : cur >= PRO + cx;",
    "cosNo = cx => PRO_COS.includes(cx) ? PRO_COS.indexOf(cx) + 1 : cx >= 10 ? cx - 9 : cx + 1 + PRO, cosLive = (cx, cur) => PRO_COS.includes(cx) ? cur >= PRO_COS.indexOf(cx) : cx >= 10 ? cur >= cx - 10 : cur >= PRO + cx;")
# the Signal planet skin (generated until it is painted)
rep('  ["countdown", "The Countdown", 2000, "all", .14, "#ffcf6a", "A brass world of turning rings, every gear counting down to the first seal.", "metal", ["#3a2410", "#a0702a", "#f0c070"], [255, 200, 110], { gears: 1 }] /* v575 */',
    '  ["countdown", "The Countdown", 2000, "all", .14, "#ffcf6a", "A brass world of turning rings, every gear counting down to the first seal.", "metal", ["#3a2410", "#a0702a", "#f0c070"], [255, 200, 110], { gears: 1 }], /* v575 */\n  ["signal", "Signal Lattice", 2000, "all", .14, "#5fe8d0", "A slate world netted in teal light, every line of it listening.", "metal", ["#0a1418", "#24404a", "#5fe8d0"], [95, 232, 208], { veins: 1 }] /* v739 */')

# 2. twelve omens; each keeps its Archive record by key
rep('const OMEN_K = ["lev", "brd", "krk", "wym", "aex", "vae", "khz", "med"];',
    'const OMEN_K = ["lev", "brd", "krk", "cube", "abyss", "seal", "sig", "wym", "aex", "vae", "khz", "med"]; /* v739 twelve weeks of omens over three slow seasons */\n'
    'const OMEN_ARC = { lev: "o_1", brd: "o_2", krk: "o_3", wym: "o_4", aex: "o_5", vae: "o_6", khz: "o_7", med: "o_8", cube: "o_9", seal: "o_10", abyss: "o_11", sig: "o_12" }, omArc = k => OMEN_ARC[k] || "o_1";')
rep('OMEN_K.map((k, i) => { const E = ARCH["o_" + (i + 1)]; return row("☾", E ? E.t : k,', 'OMEN_K.map((k, i) => { const E = ARCH[omArc(k)]; return row("☾", E ? E.t : k,')
rep('const om = ["om1", "om2"].map(k =>', 'const om = ["om1", "om3", "om2"].map(k =>')
rep('for (let j = 0; j < OMEN_K.length; j++) { const k = "o_" + (j + 1), lv = archLv(k);', 'for (let j = 0; j < OMEN_K.length; j++) { const k = omArc(OMEN_K[j]), lv = archLv(k);')
rep('j = OMEN_K.indexOf(ok), E = ARCH["o_" + (j + 1)];', 'j = OMEN_K.indexOf(ok), E = ARCH[omArc(ok)];')
rep('if (!archLv("o_" + (j + 1))) archUnlock("o_" + (j + 1), 1, true); openSheet({ type: "archives", id: "o_" + (j + 1) });', 'if (!archLv(omArc(k))) archUnlock(omArc(k), 1, true); openSheet({ type: "archives", id: omArc(k) });')
# the Judge opens his six eyes over twelve weeks and never closes one he opened under the old eight-week count
rep("const wi = omenWk(T); return wi < 0 ? 0 : wi >= 4 * PRO ? 6 : Math.ceil((wi + 1) * 6 / (4 * PRO)); }",
    "const wi = omenWk(T); return wi < 0 ? 0 : wi >= 4 * PRO ? 6 : [1, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6][wi]; } /* v739 */")
rep('if (G.finSim) return G.finSim.k === "om1" ? 3 : 6;', 'if (G.finSim) return G.finSim.k === "om1" ? 3 : G.finSim.k === "om3" ? 4 : 6;')
# scars: the new omens are not chapters, so they only show in their week, the finales and previews
rep('for (const k in FIN_SCAR) { const om = ok === k, l0 = finLast(k, T),', 'for (const k in FIN_SCAR) { const om = ok === k, l0 = FIN_EV[k] ? finLast(k, T) : null,')
rep('o2 = F && F.k === "om2", all = lab && lab.scars;', 'o2 = F && (F.k === "om2" || F.k === "om3"), all = lab && lab.scars;')
rep("const Z = { grp: new TH.Group(), M: new TH.Matrix4(), Q: new TH.Quaternion(), V: new TH.Vector3(), Sc: new TH.Vector3(), at: (i + .5) * 75e3 };",
    "const Z = { grp: new TH.Group(), M: new TH.Matrix4(), Q: new TH.Quaternion(), V: new TH.Vector3(), Sc: new TH.Vector3(), at: (i + .5) * 60e3 }; /* v739 twelve omens before the count */")
# 3. the new omens' marks on the map
scars = r'''
/* v739 the four new omens: the Cube's count (sixty faint marks round the Cube, a few lit), voices from the Abyss (a slow cyan tide beyond the
   Rim), five lights (five colourless pillars), and a signal nobody sent (a thin crimson line from past the charted stars, a pulse running it) */
Object.assign(FIN_SCAR, {
  cube: (W, X) => { const n = 60, p = finPts(W, X, n, 40, "93,255,106"), cp = new TH.Vector3(); try { if (W.nexus) W.nexus.getWorldPosition(cp); } catch (e) {} const R = LAYERS[4].r1 * 1.15;
    for (let i = 0; i < n; i++) { const a = i / n * TAU - Math.PI / 2; p.P[i * 3] = cp.x + Math.cos(a) * R; p.P[i * 3 + 1] = cp.y + 30; p.P[i * 3 + 2] = cp.z + Math.sin(a) * R; }
    return t => { const lit = 1 + Math.floor((Date.now() / 864e5) % 7); for (let i = 0; i < n; i++) { const b = i < lit ? 1.2 + .3 * Math.sin(t * .004 + i) : .3; p.C[i * 3] = b * .45; p.C[i * 3 + 1] = b; p.C[i * 3 + 2] = b * .55; } p.up(); }; },
  abyss: (W, X) => { const n = MOBILE ? 800 : 1400, R = LAYERS[0].r1 + 46, r = finR(911), p = finPts(W, X, n, 20, "63,232,240"), ang = new Float32Array(n), rr = new Float32Array(n);
    for (let i = 0; i < n; i++) { ang[i] = r() * TAU; rr[i] = R + (r() - .5) * 40; p.P[i * 3] = Math.cos(ang[i]) * rr[i]; p.P[i * 3 + 2] = Math.sin(ang[i]) * rr[i]; }
    return t => { for (let i = 0; i < n; i++) { const w = Math.sin(t * .0009 - ang[i] * 3), b = .3 + .7 * Math.max(0, w); p.P[i * 3 + 1] = -6 + 10 * w; p.C[i * 3] = b * .25; p.C[i * 3 + 1] = b * .9; p.C[i * 3 + 2] = b; } p.up(); }; },
  seal: (W, X) => { const N = 5, M = 44, p = finPts(W, X, N * M, 24, "235,240,255");
    for (let i = 0; i < N; i++) { const a = i / N * TAU + .6, L = LAYERS[2], R = (L.r0 + L.r1) / 2; for (let j = 0; j < M; j++) { const q = (i * M + j) * 3; p.P[q] = Math.cos(a) * R; p.P[q + 1] = 24 + j * 6; p.P[q + 2] = Math.sin(a) * R; } }
    return t => { for (let i = 0; i < N * M; i++) { const j = i % M, k = i / M | 0, b = (1 - j / M) * (.7 + .3 * Math.sin(t * .0016 + k * 1.3)) * (k === 3 ? .6 + .4 * Math.sin(t * .004) : 1); p.C[i * 3] = b; p.C[i * 3 + 1] = b; p.C[i * 3 + 2] = b * 1.05; } p.up(); }; },
  sig: (W, X) => { const n = MOBILE ? 400 : 700, a0 = -0.7, A = { x: Math.cos(a0) * LAYERS[0].r1 * 2.4, z: Math.sin(a0) * LAYERS[0].r1 * 2.4 }, B = { x: -A.x * .25, z: -A.z * .25 }, p = finPts(W, X, n, 20, "255,60,50");
    for (let i = 0; i < n; i++) { const u = i / (n - 1); p.P[i * 3] = A.x + (B.x - A.x) * u; p.P[i * 3 + 1] = 8 + 40 * Math.sin(u * Math.PI); p.P[i * 3 + 2] = A.z + (B.z - A.z) * u; }
    return t => { const h = (t * .00012) % 1.4; for (let i = 0; i < n; i++) { const u = i / (n - 1), d = Math.abs(u - h), b = .35 + 2 * Math.exp(-d * 40); p.C[i * 3] = b; p.C[i * 3 + 1] = b * .18; p.C[i * 3 + 2] = b * .14; } p.up(); }; } });
function finScars(W, t, T) {'''
rep("\nfunction finScars(W, t, T) {", scars)
rep('function omenFocus(k, T) { const s0 = omenWk0(T); try {', 'function omenFocus(k, T) { const s0 = omenWk0(T); if (k === "abyss") { const a = -2.4, R = LAYERS[0].r1 + 46; return [Math.cos(a) * R, 0, Math.sin(a) * R, 900]; } if (k === "sig") return [0, 0, 0, 1700]; try {')

# 4. the finales: om2 moves to the third slow season, om3 is the Signal's
rep('"om2": {"ch": 0, "typ": "omen", "si": 1,', '"om2": {"ch": 0, "typ": "omen", "si": 2,')
rep('"All eight omens light up again, one after another."', '"All twelve omens light up again, one after another."')
om3 = r'''
/* v739 the Signal's finale: the season's four omens speak at once, their signals cross above the Cube, and one of them answers back */
FIN_EV.om3 = { ch: 0, typ: "omen", si: 1, n: "Crossed Signals", chap: "Omen", ic: "⌁", col: "#5fe8d0", set: 1800000, d: "The Signal's finale. The season's four omens light up at once, their signals cross above the Cube, and something far away answers.", st: [[0, "voices", "Four Voices", "The Abyss, the five lights, the red signal and the guttering halo all wake together."], [600000, "cross", "Crossed Signals", "Lines of light arc across the galaxy and meet above the Cube."], [1320000, "answer", "An Answer", "One red pulse comes back from past the charted stars."], [1620000, "quiet", "Static", "Every line fades to static."]] };
function om3Set(W, t, F) { const D = FIN_EV.om3, e = F.e, E = D.st.map(s => s[0]); let X = W.fin;
  if (!X || X.s0 !== F.s0 || X.k !== F.k) { X = finNew(W, F); X.cp = new TH.Vector3(); X.foc = X.cp; X.dist = 1500; X.sc = [];
    ["abyss", "seal", "sig", "wym"].forEach((k, i) => { const Z = { grp: new TH.Group(), M: new TH.Matrix4(), Q: new TH.Quaternion(), V: new TH.Vector3(), Sc: new TH.Vector3(), at: (i + .5) * 40e3 }; Z.grp.visible = false; X.grp.add(Z.grp); try { Z.tick = FIN_SCAR[k](W, Z, F.s0); } catch (er) { Z.tick = null; } X.sc.push(Z); });
    X.src = [[-2.4, LAYERS[0].r1 + 46], [.6, (LAYERS[2].r0 + LAYERS[2].r1) / 2], [-.7, LAYERS[0].r1 * 1.6], [2.2, LAYERS[0].r1 + 12]].map(([a, R]) => ({ x: Math.cos(a) * R, z: Math.sin(a) * R }));
    X.NL = MOBILE ? 160 : 260; X.lines = finPts(W, X, X.NL * 4, 18, "150,255,235"); X.ans = finPts(W, X, X.NL, 24, "255,70,50"); X.flash = finSpr(W, X, "255,90,70", 0xff5a46); X.glow = finSpr(W, X, "150,255,235", 0x96ffeb); }
  try { if (W.nexus) W.nexus.getWorldPosition(X.cp); } catch (er) {}
  const cp = X.cp, voice = e < E[3], cross = fsm((e - E[1]) / 90e3) * (1 - fsm((e - E[3]) / 60e3)), ans = e >= E[2] ? fseg(e, E[2], E[2] + 40e3) : 0, end = 1 - fsm((e - D.set) / 50e3);
  for (const Z of X.sc) { const on = voice && e >= Z.at; Z.grp.visible = on; if (on && Z.tick && (Z.nt || 0) <= t) { Z.tick(t); Z.nt = t + 33; } }
  { const P = X.lines.P, C = X.lines.C, NL = X.NL; for (let l = 0; l < 4; l++) { const A = X.src[l]; for (let i = 0; i < NL; i++) { const u = i / (NL - 1), q = (l * NL + i) * 3, h = (t * .00025 + l * .25) % 1, b = cross * (.35 + 1.6 * Math.exp(-Math.abs(u - h) * 30));
      P[q] = A.x + (cp.x - A.x) * u; P[q + 1] = cp.y + 10 + 220 * Math.sin(u * Math.PI) * .6; P[q + 2] = A.z + (cp.z - A.z) * u; C[q] = b * .55; C[q + 1] = b; C[q + 2] = b * .9; } } X.lines.up(); }
  { const P = X.ans.P, C = X.ans.C, NL = X.NL, A = X.src[2]; for (let i = 0; i < NL; i++) { const u = i / (NL - 1), q = i * 3, b = e >= E[2] && e < E[3] + 60e3 ? (u <= ans ? .25 + 1.6 * Math.exp(-(ans - u) * 18) : 0) * end : 0;
      P[q] = cp.x + (A.x * 2.2 - cp.x) * (1 - u); P[q + 1] = cp.y + 30 + 60 * Math.sin(u * Math.PI); P[q + 2] = cp.z + (A.z * 2.2 - cp.z) * (1 - u); C[q] = b; C[q + 1] = b * .2; C[q + 2] = b * .15; } X.ans.up(); }
  X.glow.position.set(cp.x, cp.y + 40, cp.z); X.glow.scale.setScalar(180 + 260 * cross); X.glow.material.opacity = .35 * cross * (.8 + .2 * Math.sin(t * .006));
  const fl = e >= E[2] ? Math.max(0, 1 - Math.abs(e - (E[2] + 40e3)) / 6e3) : 0; X.flash.position.set(cp.x, cp.y + 30, cp.z); X.flash.scale.setScalar(260 + 1200 * fl); X.flash.material.opacity = fl; }
FIN_SET.om1 = om1Set; FIN_SET.om2 = om2Set; FIN_SET.om3 = om3Set;'''
rep("\nFIN_SET.om1 = om1Set; FIN_SET.om2 = om2Set;", om3)
rep('if (si < PRO) { const ok = si > 0 ? "om2" : "om1",', 'if (si < PRO) { const ok = si >= PRO - 1 ? "om2" : si > 0 ? "om3" : "om1",')

# 5. the Archives: renumber the omens in their new order, their weeks, the chapters one season later, and the four new omens (drafts for the owner)
order = ["lev", "brd", "krk", "cube", "abyss", "seal", "sig", "wym", "aex", "vae", "khz", "med"]
arc = {"lev": "o_1", "brd": "o_2", "krk": "o_3", "wym": "o_4", "aex": "o_5", "vae": "o_6", "khz": "o_7", "med": "o_8"}
for i, k in enumerate(order):
    if k not in arc: continue
    o = arc[k]
    m = re.search(r'"%s": \{"cat": "omens", "t": "Omen \d+: ' % o, s); assert m, o
    s = s[:m.start()] + '"%s": {"cat": "omens", "t": "Omen %d: ' % (o, i + 1) + s[m.end():]
    m = re.search(r'("%s": \{"cat": "omens", "t": "[^"]*", "era": ")Season \d+ · week \d+"' % o, s); assert m, o
    s = s[:m.start()] + m.group(1) + 'Season %d · week %d"' % (i // 4 + 1, i % 4 + 1) + s[m.end():]
for n in range(12, 2, -1):
    rep('"era": "Season %d finale"' % n, '"era": "Season %d finale"' % (n + 1))
rep('"era": "Season 12 · the year\'s end"', '"era": "Season 13 · the year\'s end"')
new = {
 "o_9": {"cat": "omens", "t": "Omen 4: The Count Begins", "era": "Season 1 · week 4", "civ": "The Omens", "loc": "The Cube", "img": "art/arch/dev.webp", "th": "The prologue",
  "frag": "Sixty marks appeared around the Cube in the night. One of them was already lit.",
  "interp": "A ring of faint marks circles the Cube, and another one glows every day. The Architects' records call it the count: the time left before the seals are tested. It has started early.",
  "adv": "Someone started a clock, Commander. I'd like to know who, and what happens at zero.",
  "enc": ["Commander, there are marks around the Cube. Sixty of them. One is lit."], "def": ["Another mark lit tonight. The count isn't waiting for us."]},
 "o_11": {"cat": "omens", "t": "Omen 5: Voices From the Abyss", "era": "Season 2 · week 1", "civ": "The Omens", "loc": "Beyond the outer wall", "img": "art/carcinid/s_tide.webp", "th": "The prologue",
  "frag": "Something below the outer wall is calling, in a rhythm like a tide.",
  "interp": "Our listening posts on the Rim have picked up a slow, rolling pulse from the dark beyond the Architects' wall. It rises and falls like water. The oldest records place an ocean of shells down there, and an empire that never stopped wanting out.",
  "adv": "It sounds like breathing, Commander. Very large, very patient breathing.",
  "enc": ["Commander, the Rim posts are hearing something beyond the wall. It comes and goes like a tide."], "def": ["The tide signal faded this week. It didn't stop. It went deeper."]},
 "o_10": {"cat": "omens", "t": "Omen 6: Five Lights", "era": "Season 2 · week 2", "civ": "The Omens", "loc": "The Pentarch's seals", "img": "art/arch/epx.webp", "th": "The prologue",
  "frag": "Five pale lights rose around the galaxy at once, and none of them cast a shadow.",
  "interp": "Five pillars of colourless light stand at five points of the galaxy, one for each element the Pentarch bound. The seal-records say they only show when the five seals are being tested from the inside.",
  "adv": "Five locks, Commander, and something is trying every one of them.",
  "enc": ["Commander, five pillars of light just rose across the galaxy. Same moment, same colour."], "def": ["The five lights are dimming. One of them is dimming slower than the others."]},
 "o_12": {"cat": "omens", "t": "Omen 7: A Signal Nobody Sent", "era": "Season 2 · week 3", "civ": "The Omens", "loc": "Past the charted stars", "img": "art/rwar/relay.webp", "th": "The prologue",
  "frag": "A thin red signal crossed the galaxy and asked a question in no language we know.",
  "interp": "For a week a narrow crimson transmission ran through our space from somewhere past the charted stars. It isn't Hive, it isn't Mimic, and it matches nothing in the Archives. It repeats every few hours, and our decoders return only one word with any confidence: continuity.",
  "adv": "Whatever sent it isn't alive the way we are, Commander. I can't tell you how I know that.",
  "enc": ["Commander, we're receiving a signal. Red band, very narrow. It isn't from anyone we know."], "def": ["The red signal stopped. Our decoders kept one word from it: continuity."]}}
rep('Object.assign(ARCH, {"c_1": {', 'Object.assign(ARCH, %s); /* v739 the four new omens (drafts for the owner) */\nObject.assign(ARCH, {"c_1": {' % json.dumps(new, ensure_ascii=False))
rep('"o_1", "o_2", "o_3", "o_4", "o_5", "o_6", "o_7", "o_8", "e_1"', '"o_1", "o_2", "o_3", "o_9", "o_11", "o_10", "o_12", "o_4", "o_5", "o_6", "o_7", "o_8", "e_1"')
# 6. the Judge stays out of sight through the Omens, is only a faint shape while the Signal season listens, and comes fully into view when his answer
#    reaches the Cube in the Signal's finale; his eyes then blaze at the Count Breaks (owner: keep the celestial hidden until a certain season)
rep("function celestialTick(W, t) {\n  const c = W.cam, k = c.cine || c.live ? 0 : clamp((c.dist - CEL_NEAR) / (CEL_FULL - CEL_NEAR), 0, 1), art = gfx(\"cel\") !== 0;",
    "function judgeShow(T) { if (G.judgeSim || G.finSim || (G.labMap && performance.now() < G.labMap.until)) return 1; const s1 = VP_BASE + VP_LEN; if (T < s1) return 0; const w = finWinOf(\"om3\", 0), a = w[0] + FIN_EV.om3.st[2][0]; return T < a ? .22 : Math.min(1, .22 + .78 * (T - a) / 120e3); } /* v739 */\nfunction celestialTick(W, t) {\n  const c = W.cam, k = (c.cine || c.live ? 0 : clamp((c.dist - CEL_NEAR) / (CEL_FULL - CEL_NEAR), 0, 1)) * judgeShow(now()), art = gfx(\"cel\") !== 0;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
