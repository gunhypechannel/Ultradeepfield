# v569 the season finales get their own world bosses (the owner's Leviathan and Kraken paintings).
# The Leviathan closes Season 1 (Saturday Dec 5): a serpent of black scale and living fire patrolling just beyond the Rim. Its scales burn
# and shield it (x1.5); every 15 minutes it breathes fire and for 5 minutes they cool and it takes full damage.
# The Kraken closes Season 5: it rises from the deep layers with eight armoured arms; each arm still attached shields it (x1.8 at full
# hull, one arm severed at every eighth of its hull lost).
# Both are Saturday world bosses that appear only as finales (ROTS_X); everything the other world bosses have, they have: the battle
# relief sculpted from the painting, moves, scan, field intel, Advisor news and memories, the Archives, the Boss Lab, the hunt board.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
D = json.load(open('tools/patches/p569_lines.json'))
TH = json.load(open('tools/patches/p569_thumbs.json'))
J = lambda o: json.dumps(o, ensure_ascii=False)
# the bosses
rep('It pays Void Shards in bulk." } });', '''It pays Void Shards in bulk." } });
/* v569 the season finales' own world bosses: they rise only on a finale Saturday (ROTS_X) */
Object.assign(WB, {
  lev: { k: "wbLev", n: "The Leviathan", ic: "≋", col: "#ff7a2a", hp: 380000, atk: 260000, m3: "leviathan", sc: 1.3, bounty: { m: 96000, c: 64000, g: 30000 }, sh: 5, kill: 24, where: "The outer dark · beyond the Rim", g: 2, cam: 110, fin: 1,
    d: "A season finale. A serpent of black scale and living fire, older than the Wyrm, patrolling just beyond the Rim. Its burning scales shield it (×1.5 toughness); every 15 minutes it breathes fire, and for 5 minutes after, its scales cool and it takes full damage." },
  krk: { k: "wbKrk", n: "The Kraken", ic: "✵", col: "#c46aff", hp: 360000, atk: 250000, m3: "kraken", sc: .95, bounty: { m: 92000, c: 62000, g: 30000 }, sh: 5, kill: 24, where: "The deep layers", g: 2, cam: 112, fin: 1,
    d: "A season finale. A titan risen from the deep layers, with eight armoured arms lit by violet suckers. Every arm still attached shields its body: it starts ×1.8 tougher and loses a tenth of that with each arm severed (one falls at every eighth of its hull)." } });''')
rep('if (key === "wym") return wymOpen(at) ? 1 : 1.6;', 'if (key === "wym") return wymOpen(at) ? 1 : 1.6;\n  if (key === "lev") return levCool(at) ? 1 : 1.5; if (key === "krk") return 1 + .1 * krkArms(st); /* v569 */')
rep('const colHeart = at => elCyc(at, 6e5) < 12e4;', 'const colHeart = at => elCyc(at, 6e5) < 12e4;\n/* v569 the Leviathan breathes every 15 minutes and its scales cool for 5; the Kraken loses an arm at every eighth of its hull */\nconst levCool = at => elCyc(at, 9e5) < 3e5, krkArms = st => clamp(Math.ceil((st.hp.krk | 0) / WB_SEG * 8 - 1e-9), 0, 8);')
rep('  if (key === "wym") return wymOpen(T) ? `Segments exposed', '''  if (key === "lev") { const c = elCyc(T, 9e5); return c < 3e5 ? `Scales cooling after its breath · full damage for ${ftime(3e5 - c)}` : `Scales burning · ×1.5 toughness · it breathes fire in ${ftime(9e5 - c)}`; }
  if (key === "krk") { const a = krkArms(st); return `${a} of 8 arms · ×${(1 + .1 * a).toFixed(1)} toughness · an arm falls at every eighth of its hull`; }
  if (key === "wym") return wymOpen(T) ? `Segments exposed''')
rep('{ brd: "Drone swarm", tyr: "Vault", wym: "Segments", col: "Fragments" }[key]', '{ brd: "Drone swarm", tyr: "Vault", wym: "Segments", col: "Fragments", lev: "Scales", krk: "Arms" }[key]')
# where they are
rep('    if (key === "col") { if (!WB_MINE)', '''    if (key === "lev") { const r = LAYERS[0].r1 + 10, a = (hash("lev" + c2) % 6283) / 1000 + TAU * T / (36 * 3600e3); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 20 + 3 * Math.sin(T / 6e5); return o; } // v569 patrolling just beyond the Rim
    if (key === "krk") { const L = LAYERS[3], r = (L.r0 + L.r1) / 2, a = (hash("krk" + c2) % 6283) / 1000 + TAU * T / period(r); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 9 + 2 * Math.sin(T / 5e5); return o; } // risen among the deep layers
    if (key === "col") { if (!WB_MINE)''')
rep('if (key === "wym" && b.own) for (const o of b.own) o.visible = false;', 'if ((key === "wym" || key === "lev") && b.own) for (const o of b.own) o.visible = false;')
rep('    if (key === "dev" || key === "tyr") { const q2 = wbPos(key, T + 60000, {});', '    if (key === "dev" || key === "tyr" || key === "lev" || key === "krk") { const q2 = wbPos(key, T + 60000, {});')
rep('for (const key of ["ovl", "dev", "war", "brd", "tyr", "wym", "col"]) { const step', 'for (const key of ["ovl", "dev", "war", "brd", "tyr", "wym", "col", "lev", "krk"]) { const step')
# the models: the Wyrm's and the Devourer's bodies, the paintings as their skins
rep('wyrm: (...a) => painted("wyrm", wyrm(...a)),', 'wyrm: (...a) => painted("wyrm", wyrm(...a)), leviathan: () => painted("leviathan", wyrm("lev")), kraken: () => painted("kraken", devourer("krk")),')
# the Leviathan: the Wyrm's serpent body in black scale and living fire, no black hole, taller dorsal spines
rep('function wyrm() { const grp', 'function wyrm(o) { const LV = o === "lev"; const grp')
rep('const MA = hullMat("wym", { rows: 4, pal: ["#1a1424", "#221a2e", "#140f1c", "#2c2234"], slits: .45, sc: "#ffe0b0", sg: "#ff9a40", metal: .92, rough: .26, rc: RC, ei: 2.6, rep: [6, 1] });',
    'const MA = LV ? hullMat("lev", { rows: 4, pal: ["#120e0d", "#1a1311", "#0d0a09", "#22170f"], slits: .62, sc: "#ffd080", sg: "#ff5a10", metal: .85, rough: .3, rc: [1, .42, .08], ei: 3.4, rep: [6, 1] }) : hullMat("wym", { rows: 4, pal: ["#1a1424", "#221a2e", "#140f1c", "#2c2234"], slits: .45, sc: "#ffe0b0", sg: "#ff9a40", metal: .92, rough: .26, rc: RC, ei: 2.6, rep: [6, 1] });')
rep('const MJ = hullMat("wymj", {', 'const MJ = LV ? hullMat("levj", { rows: 5, pal: ["#120e0d", "#1c1410", "#0d0a09"], slits: .45, sc: "#ffd080", sg: "#ff5a10", metal: .85, rough: .3, rc: [1, .42, .08], ei: 3, rep: [2, 1], side: 1 }) : hullMat("wymj", {')
rep('const spine = inst(spG, glowMat(0xb060ff, .3), N); const finG = new TH.ConeGeometry(.3, 1.6, 4); finG.translate(0, 1.6, 0);', 'const spine = inst(spG, glowMat(LV ? 0xff5a10 : 0xb060ff, LV ? .42 : .3), N); const finG = LV ? new TH.ConeGeometry(.38, 2.7, 4) : new TH.ConeGeometry(.3, 1.6, 4); finG.translate(0, LV ? 2.1 : 1.6, 0);')
rep('for (const m of [segs, rims, cores, spine, fins]) body.add(m); for (let i = 0; i < N * 2; i++)', 'for (const m of [segs, rims, cores, spine, fins]) body.add(m); if (LV) { cores.visible = false; bh.visible = false; } for (let i = 0; i < N * 2; i++)')
rep('const vuln = puffs(N, 0xffd8ff);', 'const vuln = puffs(N, LV ? 0xffa040 : 0xffd8ff);')
rep('c1.setRGB(b * (1 + hot * .1), b * (.5 + hot * .5), b * (.22 + hot * .9));', 'if (LV) c1.setRGB(b * 1.2, b * (.4 + hot * .35), b * (.08 + hot * .2)); else c1.setRGB(b * (1 + hot * .1), b * (.5 + hot * .5), b * (.22 + hot * .9));')
# the Kraken: the Devourer's body in deep violet scale, violet eyes above its maw
rep('function devourer() { const grp', 'function devourer(o) { const KR = o === "krk"; const grp')
rep('const M = hullMat("dev", { rows: 12, bronze: .12, slits: .55, rep: [12, 3] }), MS = hullMat("devs", { rows: 2, cols: 2, bronze: .15, slits: .45, rep: [1, 1] }), MB = hullMat("devb", { rows: 4, bronze: .35, slits: .15, rep: [1, 1] });',
    'const KP = { pal: ["#1a0d28", "#26123c", "#12091c", "#30184a"], sc: "#f4c8ff", sg: "#c46aff", rc: [.8, .3, 1] }, M = KR ? hullMat("krk", { rows: 12, slits: .6, rep: [12, 3], ...KP }) : hullMat("dev", { rows: 12, bronze: .12, slits: .55, rep: [12, 3] }), MS = KR ? hullMat("krks", { rows: 2, cols: 2, slits: .5, rep: [1, 1], ...KP }) : hullMat("devs", { rows: 2, cols: 2, bronze: .15, slits: .45, rep: [1, 1] }), MB = KR ? hullMat("krkb", { rows: 4, slits: .3, rep: [1, 1], ...KP }) : hullMat("devb", { rows: 4, bronze: .35, slits: .15, rep: [1, 1] });')
rep('const glow = sprite(9); glow.position.x = .2; maw.add(glow);', 'const glow = sprite(9); glow.position.x = .2; maw.add(glow); if (KR) for (const sz of [-1, 1]) { const e = sprite(2.4, "rgba(225,150,255,1)", "kreye"); e.position.set(.6, 3.7, sz * 1.15); maw.add(e); const e2 = sprite(.9, "rgba(255,240,255,1)", "kreye2"); e2.position.set(.7, 3.7, sz * 1.15); maw.add(e2); }')
rep('  const PNT = { ', '  const PNT = { "leviathan": [762, 506, [26, 0, 741, 503], 0.438, [140, 215], "#ff7a2a", 2.2], "kraken": [762, 506, [0, 0, 759, 503], 0.516, [405, 175], "#c46aff", 1.05], ')
# battle
rep('wym: ["lens", "coil", "sweep"], col: ["prism", "rain", "shatter"] };', 'wym: ["lens", "coil", "sweep"], col: ["prism", "rain", "shatter"], lev: ["lens", "coil", "sweep"], krk: ["bite", "lash", "beam", "grab", "storm", "roar"] };')
rep('  wym: { lens: ["beam", .35, .85, 0, 3000], sweep: ["sweep", .2, .82, 0, 2200] },', '  wym: { lens: ["beam", .35, .85, 0, 3000], sweep: ["sweep", .2, .82, 0, 2200] },\n  lev: { lens: ["beam", .35, .85, 0, 3000], sweep: ["sweep", .2, .82, 0, 2200] },\n  krk: { lash: ["bolts", .3, .65, 4, 1900], beam: ["beam", .42, .88, 0, 3800], roar: ["wave", .3, .85, 0, 2400], grab: ["bolts", .45, .75, 3, 3000], storm: ["bolts", .32, .85, 9, 4200] },')
rep('wbWym: ["titan", "beam", .38, 0, 1.6, 7],', 'wbWym: ["titan", "beam", .38, 0, 1.6, 7], wbLev: ["titan", "beam", .4, 0, 1.6, 8], wbKrk: ["titan", "plasma", .38, 0, 1.6, 8],')
rep('["wbWym", WB.wym], ', '["wbWym", WB.wym], ["wbLev", WB.lev], ["wbKrk", WB.krk], ')
rep('{ const mk = { dev: "bio",', '{ const mk = { lev: "void", krk: "bio", dev: "bio",')
rep('const WB_CLR = { wym: 30,', 'const WB_CLR = { lev: 34, krk: 34, wym: 30,')
rep('"est", "ena"];\nlet WB_SEPC', '"est", "ena", "lev", "krk"];\nlet WB_SEPC')
rep('const SB_CRY = { ', 'const SB_CRY = { lev: [[.85, .3, .04], [1, .72, .4]], krk: [[.55, .12, .85], [.95, .7, 1]], ')
rep('wym: [1, .7, .3] }[s.k]', 'wym: [1, .7, .3], lev: [1, .5, .15], krk: [.8, .35, 1] }[s.k]')
# scan, intel, the Advisor
ATT = {"lev": [["coil", "Burning coil", "It wraps its fiery body round the fleet and crushes inward."], ["lens", "Fire breath", "Its jaws gape and a river of fire pours through the fleet."], ["sweep", "Tail scythe", "Its spined tail sweeps through everything near it."]],
       "krk": [["bite", "Beak", "Its hidden beak snaps at anything that drifts beneath it."], ["lash", "Arm lash", "Two arms sweep across the fleet."], ["beam", "Abyss eyes", "Its violet eyes flare and burn a line through the fleet."], ["roar", "Ink pulse", "A cloud of void ink bursts out, crackling with lightning."], ["grab", "Constrict", "Its arms seize ships and drag them in."], ["storm", "Sucker storm", "Every sucker on its arms flares at once and fires."]]}
rep('"wym": [["coil", "Gravity coil"', J(ATT)[1:-1] + ', "wym": [["coil", "Gravity coil"')
rep('"wym": "Scanning the Event Horizon Wyrm.', ', '.join('"%s": %s' % (k, J(v[0])) for k, v in D['scan'].items()) + ', "wym": "Scanning the Event Horizon Wyrm.')
rep('wym: ["Black-hole serpent",', 'lev: ["Primordial fire serpent · beyond the Rim", "Its scales, while they cool after each breath.", "CATASTROPHIC"], krk: ["Abyssal titan · the deep layers", "Its arms: every one severed weakens its guard.", "CATASTROPHIC"], wym: ["Black-hole serpent",')
rep('const AWE = {', 'const AWE = {' + ', '.join('"%s": %s' % (k, J([x[0] for x in v])) for k, v in D['awe'].items()) + ', ')
rep('  wbwym: "', ''.join('  %s: %s,\n' % (k, J(v[0])) for k, v in D['holo'].items()) + '  wbwym: "')
rep('const ADV_NEWS = {', 'const ADV_NEWS = {' + ', '.join('"%s": %s' % (k, J(v[0])) for k, v in D['news'].items()) + ', ')
MOOD = {}
for grp in ('news', 'holo', 'scan'):
    for v in D[grp].values(): MOOD[v[0]] = v[1]
for v in D['awe'].values():
    for line, m in v: MOOD[line] = m
for E in D['arch'].values():
    for x in E['enc']: MOOD[x] = 'awe'
    for x in E['def']: MOOD[x] = 'grave'
    MOOD[E['adv']] = 'grave'
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
# the Archives
rep('  wym: { cat: "warn", t: "The Serpent That Encircled the Sun"', ''.join('  %s: %s,\n' % (k, J(v)) for k, v in D['arch'].items()) + '  wym: { cat: "warn", t: "The Serpent That Encircled the Sun"')
rep('const ARCH_ORD = ["war", "wym",', 'const ARCH_ORD = ["war", "wym", "lev", "krk",')
rep('const BOSS_ART = {', 'const BOSS_ART = {' + J(TH)[1:-1] + ', ')
# the calendar: the finales are theirs (season 1's Saturday finale is the Leviathan, season 5's the Kraken)
rep('ROTS = ["ovl", "dev", "war", "brd", "tyr", "wym", "col"];', 'ROTS = ["ovl", "dev", "war", "brd", "tyr", "wym", "col"], ROTS_X = ["lev", "krk"]; /* v569 the finale-only Saturday bosses */')
rep('const SEA_FIN = [["khz", "wym"], ["dv", "ovl"], ["conv", "war"], ["aex", "brd"], ["med", "dev"],', 'const SEA_FIN = [["khz", "lev"], ["dv", "ovl"], ["conv", "war"], ["aex", "brd"], ["med", "krk"],')
rep('sat ? ["ovl", "ovl", "dev", "wym"] : ["vae", "vae", "aex", "khz"]', 'sat ? ["ovl", "ovl", "dev", "lev"] : ["vae", "vae", "aex", "khz"]')
rep('const rotStartOf = (key, T) => { const sm = ROTS.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= 24; i++)',
    'const rotStartOf = (key, T) => { const sm = ROTS.includes(key) || ROTS_X.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= 44; i++)')
rep('const rotNextOf = (key, T) => { const sm = ROTS.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + 25; w++)',
    'const rotNextOf = (key, T) => { const sm = ROTS.includes(key) || ROTS_X.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + 45; w++)')
rep('g === 2 ? ["brd", "tyr", "wym", "col"] : ["ovl", "dev", "war"];', 'g === 2 ? ["brd", "tyr", "wym", "col", "lev", "krk"] : ["ovl", "dev", "war"];')
rep('tit = rk ? ["brd", "tyr", "wym", "col"].includes(rs)', 'tit = rk ? ["brd", "tyr", "wym", "col", "lev", "krk"].includes(rs)')
rep('const st = wbState(T); for (const w of ROTS) if (wbOn(w, T))', 'const st = wbState(T); for (const w of [...ROTS, ...ROTS_X]) if (wbOn(w, T))')
rep('const rows = [...ROT, ...ROTS].map(k =>', 'const rows = [...ROT, ...ROTS, ...ROTS_X].map(k =>')
# the battle camera, facing and scan framing (by model)
rep('tyrant: -.55, wyrm: 0, colossus: 0 };', 'tyrant: -.55, wyrm: 0, colossus: 0, leviathan: 0, kraken: -Math.PI / 2 };')
rep('wyrm: [0, [-6, 21, 52], [0, 10, 0]], colossus:', 'wyrm: [0, [-6, 21, 52], [0, 10, 0]], leviathan: [0, [-6, 21, 52], [0, 10, 0]], kraken: [Math.PI, [-8, 7, 36], [3, 0, 0]], colossus:')
rep('wyrm: [-3, 13], colossus: [-1, 19] };', 'wyrm: [-3, 13], colossus: [-1, 19], leviathan: [-3, 13], kraken: [-6, 6] };')
s2 = re.sub(r"GAME_V = 568\b", "GAME_V = 569", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
