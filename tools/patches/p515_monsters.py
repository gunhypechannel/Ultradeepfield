# v515 six new space monsters (owner: "Do it all, add them! I love it, fit them well into our game"): the Void Manta, a Starhive
# (a wasp swarm round its nest), the Crystal Tortoise, the Gravity Spider, the Solar Moth and the Comet Ram. Each has its own stats
# and way of fighting, a full 3D model that moves on the map (flapping, paddling, walking, circling), a battle look on the map,
# Advisor lines and a material it tends to drop. 600 of them (100 of each) join the map on their own spiral as w1800-w2399, so every
# monster already out there keeps its species and its place. They fight as one creature (battle rules v6), the Starhive as its swarm
# plus the nest. The server's simulator is rebuilt with their stats (settle_fight redeployed).
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p515_monsters.js'), encoding='utf-8').read()
part = lambda name: J.split('//@@' + name + '\n')[1].split('//@@')[0]
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

NEW = ["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"]
# --- stats (scale with the monster's level, see unitStat); one:1 marks a creature that fights as a single squadron
rep('''  ssquid:    { n: "Space Squid", atk: 1700, sh: 1000, hull: 15000, val: 50000 }
};''', '''  ssquid:    { n: "Space Squid", atk: 1700, sh: 1000, hull: 15000, val: 50000, one: 1 },
  // v515 six more species, and the Starhive's nest (fought together with its swarm)
  vmanta:    { n: "Void Manta", atk: 1500, sh: 1800, hull: 22000, val: 70000, one: 1 },
  swasp:     { n: "Starhive Wasps", atk: 260, sh: 150, hull: 2600, val: 12000, one: 1 },
  snest:     { n: "Starhive Nest", atk: 600, sh: 1500, hull: 40000, val: 60000, one: 1 },
  ctort:     { n: "Crystal Tortoise", atk: 700, sh: 5000, hull: 90000, val: 160000, one: 1 },
  gspider:   { n: "Gravity Spider", atk: 2600, sh: 2400, hull: 34000, val: 110000, one: 1 },
  smoth:     { n: "Solar Moth", atk: 1300, sh: 900, hull: 11000, val: 40000, one: 1 },
  cram:      { n: "Comet Ram", atk: 3800, sh: 1600, hull: 42000, val: 140000, one: 1 }
};''')
rep('  swhale:    { n: "Space Shark", atk: 900, sh: 2600, hull: 60000, val: 120000 },', '  swhale:    { n: "Space Shark", atk: 900, sh: 2600, hull: 60000, val: 120000, one: 1 },')
rep('  slevi:     { n: "Space Leviathan", atk: 4200, sh: 2200, hull: 38000, val: 150000 },', '  slevi:     { n: "Space Leviathan", atk: 4200, sh: 2200, hull: 38000, val: 150000, one: 1 },')
rep('''ssquid: { fighter: 6, hauler: 6, heavyCargo: 3 }, swhale: { fighter: 3 }
};''', '''ssquid: { fighter: 6, hauler: 6, heavyCargo: 3 }, swhale: { fighter: 3 },
  vmanta: { fighter: 4, heavyFighter: 3 }, swasp: { fighter: 3, hauler: 3 }, ctort: { fighter: 2, bomber: 2 }, gspider: { fighter: 4, lancer: 3, corvette: 3 }, smoth: { corvette: 3, guardian: 2 }, cram: { fighter: 4, battleship: 3, bastion: 2 }
};
/* v515 what counters the new monsters: Corvettes shred a wasp swarm, Bombers crack the Tortoise, Lancers run down the Manta */
Object.assign(RF.corvette, { swasp: 4 }); Object.assign(RF.battleship, { swasp: 3 }); Object.assign(RF.bomber, { ctort: 3, snest: 3 }); Object.assign(RF.lancer, { vmanta: 3, smoth: 3 });''')
rep('ssquid: ["cruiser", "acid", .12, .14, 5, 1], wbOvl:', 'ssquid: ["cruiser", "acid", .12, .14, 5, 1], vmanta: ["cruiser", "laser", .08, .28, 7, 1], swasp: ["interceptor", "acid", 0, .32, 9, 0], snest: ["station", "acid", .3, 0, 0, 2], ctort: ["titan", "mass", .5, 0, .8, 4], gspider: ["capital", "beam", .25, .06, 3, 2], smoth: ["cruiser", "ion", .05, .18, 6, 0], cram: ["capital", "mass", .35, .02, 4.2, 1], wbOvl:')
rep('(V6 && (s.k === "swhale" || s.k === "slevi" || s.k === "ssquid"))', '(V6 && AL[s.k] && AL[s.k].one)')
rep('  if (MON[k]) { const s = .25 + .15 * (t.mon || 1);', '  if (MON[k] || k === "snest") { const s = .25 + .15 * (t.mon || 1);')

# --- the species
rep('''const MON_K = ["swhale", "slevi", "ssquid"];''', '''Object.assign(MON, { /* v515 */
  vmanta: { n: "Void Manta", sp: "Void Manta", ic: "🪁", col: "#7af4ff", rgb: "122,244,255", per: 6, d: "A winged ray as wide as a cruiser, gliding the dark on rows of cyan light. Fast and slippery: half our shots fly wide, and its stinger tail lashes back.", names: ["Duskwing", "the Glide", "Hushveil", "Nightsail", "Skimmer", "Velvetray", "Lantern Drift", "Shadowfold"] },
  swasp: { n: "Starhive Wasps", sp: "Starhive", ic: "🐝", col: "#ffb02a", rgb: "255,176,42", per: 1, d: "A nest of resin as big as a station, its cells lit like embers, with a swarm of armoured wasps circling it. The more it grows, the more wasps defend it. Kill the swarm, then break the nest.", names: ["the Ember Comb", "Buzzing Crown", "Goldspire", "Hive Noon", "the Stinging Hall", "Ambermaw", "Waxmoon", "the Thrum"] },
  ctort: { n: "Crystal Tortoise", sp: "Crystal Tortoise", ic: "🐢", col: "#a98cff", rgb: "169,140,255", per: 12, d: "As old as the moons it grazes on. Crystal spires grow from its basalt shell, and light guns barely scratch it. Slow, patient and very hard to kill.", names: ["Old Shellmother", "the Slow Crown", "Grandfather Spire", "Prismback", "Stonepace", "the Patient One", "Geodeheart", "Amethyst Elder"] },
  gspider: { n: "Gravity Spider", sp: "Gravity Spider", ic: "🕷", col: "#c87aff", rgb: "200,122,255", per: 9, d: "It carries a caged singularity on its back and weaves gravity webs between asteroids. Ships caught in its lances are dragged off course and torn apart.", names: ["the Weaver", "Nullsilk", "Eight-Eyes", "Graveweb", "the Long Reach", "Widow Abyss", "Threadmaw", "Silkfall"] },
  smoth: { n: "Solar Moth", sp: "Solar Moth", ic: "🦋", col: "#ffc45a", rgb: "255,196,90", per: 4, d: "Drawn to stars and shields alike. Its gold wings carry burning sun-eyes, and its ion dust strips shields away. They drift in clouds, many at once.", names: ["Sunsip", "the Bright Flutter", "Embermote", "Dawnwing", "Goldendust", "Flarelight", "Corona", "Solstice"] },
  cram: { n: "Comet Ram", sp: "Comet Ram", ic: "☄", col: "#8cd2ff", rgb: "140,210,255", per: 10, d: "A horned beast of ice that rides its own comet. It charges headlong through fleets, horns first, with a tail of frost burning behind it.", names: ["Frosthorn", "the Battering Star", "Icebrow", "Old Rimecurl", "Thunderhoof", "Glacierhead", "the Long Tail", "Skull of Winter"] }
});
const MON_K = ["swhale", "slevi", "ssquid"], MON_K2 = ["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"]; // v515 MON_K2 spawn on their own spiral''')
rep('const monForce = (k, lvl) => ({ [k]: 1 + Math.floor((lvl - 1) / MON[k].per) });', 'const monForce = (k, lvl) => k === "swasp" ? { swasp: lvl, snest: 1 } : ({ [k]: 1 + Math.floor((lvl - 1) / MON[k].per) }); /* v515 a Starhive: one wasp per level, and its nest */')
# --- 600 more on their own spiral (no coordinates of their own, like MON_EXTRA)
rep('''const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA);''', '''/* v515 the six new species: 600 more (w1800 to w2399, 100 of each) on a third sunflower spiral, turned between the others */
const MON_Y = 600, MON_NEW = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6, rm = rnd(8383);
  for (let j = 0; j < MON_Y; j++) { const u = (j + .15) / MON_Y, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (2.7 + j * GOLD) % TAU, mk = MON_K2[j % 6], lvl = (layerOf(rad).n - 1) * 5 + 1 + (Math.floor(j / 6) * 7) % 5, M = MON[mk];
    out.push({ id: "w" + (MON_N + MON_X + j), kind: "pirate", mon: mk, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `${M.names[(rm() * M.names.length) | 0]} · ${M.sp}` }); } return out; })();
const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW);''')
rep('`${pool.length} Space Sharks, Leviathans and Squids drift across every layer:', '`${pool.length} space monsters of nine kinds drift across every layer:')
rep('try { for (const k of MON_K) { const x = PIRATES.find(p => p.mon === k);', 'try { for (const k of MON_K.concat(MON_K2)) { const x = PIRATES.find(p => p.mon === k);')

# --- loot: each species leans toward one material
rep('monster: (L, el) => { const t = fsTierL(L, 8), k = el ? ELITE_K.loot : 1; return [["bio", t, (1 + Math.floor(L / 8)) * k], ["void", t, k, .35], ["cube", t, 1, .08], ["bio", t + 1, 1, Math.min(1, .1 * (el ? ELITE_K.up : 1)), 1]]; },',
    'monster: (L, el, sp) => { const t = fsTierL(L, 8), k = el ? ELITE_K.loot : 1, x = MON_LOOT[sp]; return [["bio", t, (1 + Math.floor(L / 8)) * k], ["void", t, k, .35], ["cube", t, 1, .08], ["bio", t + 1, 1, Math.min(1, .1 * (el ? ELITE_K.up : 1)), 1]].concat(x ? [[x[0], t, k, x[1]]] : []); },')
rep('const FS_MATS = {', '''const MON_LOOT = { ctort: ["crystal", .7], cram: ["alloy", .6], gspider: ["void", .25], smoth: ["crystal", .35], vmanta: ["void", .15], swasp: ["bio", .5] }; /* v515 a second roll by species */
const FS_MATS = {''')
rep('lk === "mon" ? LOOT.monster(x.lvl, el)', 'lk === "mon" ? LOOT.monster(x.lvl, el, x.mon)')
rep('kind === "mon" ? LOOT.monster(L, el)', 'kind === "mon" ? LOOT.monster(L, el, x.mon)')

# --- battle look: icons, sizes, glow
rep('''    case "ssquid": ''', '''    case "vmanta": P([0, -.95, 1.15, .1, .25, .35, 0, .5, -.25, .35, -1.15, .1]); ctx.fill(); ctx.lineWidth = .08; ctx.beginPath(); ctx.moveTo(0, .45); ctx.lineTo(0, 1.25); ctx.stroke(); break;
    case "swasp": for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; ctx.beginPath(); ctx.ellipse(Math.cos(a) * .7, Math.sin(a) * .7, .14, .24, a, 0, TAU); ctx.fill(); } break;
    case "snest": ctx.ellipse(0, .1, .62, .85, 0, 0, TAU); ctx.fill(); ctx.fillStyle = "#05090f"; for (let i = 0; i < 3; i++) ctx.fillRect(-.45, -.35 + i * .35, .9, .07); break;
    case "ctort": ctx.ellipse(0, .1, .78, .9, 0, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(0, -.95, .25, 0, TAU); ctx.fill(); for (const [x, y] of [[-.85, -.45], [.85, -.45], [-.75, .75], [.75, .75]]) { ctx.beginPath(); ctx.ellipse(x, y, .22, .12, 0, 0, TAU); ctx.fill(); } break;
    case "gspider": ctx.arc(0, .35, .5, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(0, -.35, .3, 0, TAU); ctx.fill(); ctx.lineWidth = .09; for (let i = 0; i < 4; i++) for (const sd of [1, -1]) { ctx.beginPath(); ctx.moveTo(0, -.3); ctx.lineTo(sd * .7, -.75 + i * .35); ctx.lineTo(sd * 1.05, -.5 + i * .5); ctx.stroke(); } break;
    case "smoth": for (const sd of [1, -1]) { ctx.beginPath(); ctx.ellipse(sd * .5, -.25, .5, .38, sd * .5, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.ellipse(sd * .4, .4, .35, .3, -sd * .5, 0, TAU); ctx.fill(); } ctx.fillRect(-.07, -.7, .14, 1.4); break;
    case "cram": ctx.arc(0, -.45, .5, 0, TAU); ctx.fill(); ctx.lineWidth = .16; for (const sd of [1, -1]) { ctx.beginPath(); ctx.arc(sd * .45, -.6, .35, 0, TAU * .8); ctx.stroke(); } ctx.beginPath(); P([-.4, -.1, .4, -.1, 0, 1.3]); ctx.fill(); break;
    case "ssquid": ''')
rep('const BOSSK = { cube: 1.7, sphere: 1.35, swhale: 1.8, slevi: 1.8, ssquid: 1.6, leviathan: 1.5 },', 'const BOSSK = { cube: 1.7, sphere: 1.35, swhale: 1.8, slevi: 1.8, ssquid: 1.6, leviathan: 1.5, vmanta: 1.7, swasp: 1.3, snest: 1.6, ctort: 1.8, gspider: 1.7, smoth: 1.6, cram: 1.8 },')
rep('BOSS_GLOW = { cube: "90,255,140",', 'BOSS_GLOW = { vmanta: "122,244,255", swasp: "255,176,42", snest: "255,176,42", ctort: "169,140,255", gspider: "200,122,255", smoth: "255,196,90", cram: "140,210,255", cube: "90,255,140",')
rep('leviathan: 1.2, swhale: 1.5, slevi: 1.5, ssquid: 1.05 };', 'leviathan: 1.2, swhale: 1.5, slevi: 1.5, ssquid: 1.05, vmanta: 1.3, swasp: .9, snest: 1.2, ctort: 1.4, gspider: 1.3, smoth: 1.2, cram: 1.5 };')

# --- 3D: materials, models, swimming
rep('''  return C;
}
const MONM = {};''', part('MATS') + '''  return C;
}
const MONM = {};''')
rep('''function buildMonster(k) {
  const C = monMats(), g = new TH.Group(); g.userData.eng = [];''', '''function buildMonster(k, part) {
  const C = monMats(), g = new TH.Group(); g.userData.eng = [];
  /* v515 a flat part with rounded bevelled edges, outlined by quadratic curves (moveTo, then control/end pairs) in its own x/y plane */
  const slab = (pts, th) => { const sh = new TH.Shape(); sh.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i += 2) sh.quadraticCurveTo(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]); sh.closePath();
    const geo = new TH.ExtrudeGeometry(sh, { depth: th, bevelEnabled: true, bevelThickness: th * .6, bevelSize: th * .8, bevelSegments: 3, curveSegments: 24 }); geo.translate(0, 0, -th / 2); return geo; };''')
models = part('MODELS')
# the Starhive's battle look is split: the swarm unit is only the wasps, the nest unit only the nest
models = models.replace('''    const nest = lathe(''', '''    if (part !== "swarm") { const nest = lathe(''')
models = models.replace('''    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + (i % 2) * .3,''', '''    }
    if (part !== "nest") for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + (i % 2) * .3,''')
rep('''  }
  return g;
}
function buildAlien(k) {
  if (MON[k]) return buildMonster(k);''', models + '''  }
  return g;
}
function buildAlien(k) {
  if (k === "swasp" || k === "snest") return buildMonster("swasp", k === "snest" ? "nest" : "swarm");
  if (MON[k]) return buildMonster(k);''')
rep('''  ssquid: "float ar = clamp((-.9 - position.x) / 3., 0., 1.),''', '''  /* v515 the Manta's wings ripple from root to tip and its tail whips; the Starhive's swarm circles its nest; the Tortoise paddles
     its four flippers in turn; the Spider walks its legs in waves; the Moth beats its wings; the Ram's comet tail streams behind it */
  vmanta: "float sp = abs(position.z), w = smoothstep(.9, 3.5, sp); transformed.y += w * w * 1.05 * sin(mt * 1.7 - sp * .55); float tl = clamp((-1.9 - position.x) / 5., 0., 1.); transformed.z += tl * tl * .7 * sin(mt * 2.3 + position.x * 1.1); transformed.y += tl * .15 * sin(mt * 1.7 + 1.);",
  swasp: "float rr = length(position.xz); if (rr > 1.95) { float th = mt * (1.5 - rr * .18), c = cos(th), sn = sin(th); transformed.xz = vec2(transformed.x * c - transformed.z * sn, transformed.x * sn + transformed.z * c); transformed.y += .28 * sin(mt * 3.1 + rr * 5.); } else { transformed.x += .03 * sin(mt * 1.3 + position.y * 2.); }",
  ctort: "float fl = smoothstep(1.7, 2.6, abs(position.z)), ph = mt * 1.1 + sign(position.z) * 1.57 + step(0., position.x) * 3.14; transformed.y += fl * .32 * sin(ph); transformed.x += fl * .22 * cos(ph); float hd = smoothstep(2.2, 3.2, position.x); transformed.y += hd * .1 * sin(mt * .7); transformed.z += hd * .12 * sin(mt * .45);",
  gspider: "float lg = smoothstep(1.3, 3., abs(position.z)), ph = position.x * 1.6 + sign(position.z) * 1.57; transformed.y += lg * .32 * max(0., sin(mt * 3.4 + ph)); transformed.x += lg * .2 * cos(mt * 3.4 + ph); transformed.y += .04 * sin(mt * 6.8);",
  smoth: "float sp = abs(position.z); if (sp > .38) { float a = .7 * sin(mt * 2.4), d = sp - .38; transformed.y += d * sin(a); transformed.z = sign(position.z) * (.38 + d * cos(a)); } transformed.y += .18 * sin(mt * 2.4 + 1.4);",
  cram: "float tl = clamp((-2.2 - position.x) / 6., 0., 1.); transformed.z += tl * tl * .8 * sin(position.x * .9 + mt * 4.); transformed.y += tl * tl * .45 * cos(position.x * .7 + mt * 3.3); float hb = smoothstep(.8, 2.8, position.x); transformed.y += hb * .1 * sin(mt * 1.6);",
  ssquid: "float ar = clamp((-.9 - position.x) / 3., 0., 1.),''')
rep('sp = it.mon === "ssquid" ? .00034 : it.mon === "slevi" ? .00022 : .0002 /*', 'sp = MON_SWIM[it.mon] || (it.mon === "ssquid" ? .00034 : it.mon === "slevi" ? .00022 : .0002) /*')
rep('''        if (it.mon === "ssquid") { const p = 1 + .07 * Math.sin(t * .006 + it.a0);''', '''        if (it.mon === "swasp") { o.body.position.set(0, Math.sin(t * .0005 + it.a0) * .3, 0); o.body.rotation.set(0, t * .00008 + it.a0, 0); } // v515 a Starhive hangs where it is; its swarm does the moving
        if (it.mon === "ssquid") { const p = 1 + .07 * Math.sin(t * .006 + it.a0);''')
rep('const BEAST_FX = { cube: [93, 255, 106],', '''const MON_SWIM = { vmanta: .00026, ctort: .00009, gspider: .00016, smoth: .0003, cram: .00038 }; /* v515 how fast each new species swims its figure-eight */
const NEWBEAST = new Set(["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"]);
const BEAST_FX = { vmanta: [122, 244, 255], swasp: [255, 176, 42], ctort: [169, 140, 255], gspider: [200, 122, 255], smoth: [255, 196, 90], cram: [140, 210, 255], cube: [93, 255, 106],''')
# --- how each new species fights a fleet on the map
rep('''  if (dying && !gone && tn - (bx.dt || 0) > 140) {''', '''  /* v515 the Starhive's swarm darts in from all round the nest; the Tortoise hurls crystal shards; the Ram charges its horns and
     slams into the line; the Manta, Spider and Moth charge and fire a lance (the Spider's drags a gravity ring, the Moth's is wide) */
  if (live && !dying && NEWBEAST.has(kind)) { const src = _bA.copy(dir).multiplyScalar(r * .9).add(cen);
    if (kind === "swasp") { if (tn - (bx.lt || 0) > 110) { bx.lt = tn; const tg = pick(); if (tg) { tg(_bB); o.bl.push({ a: beastPt(bx, cen, dir, new TH.Vector3(), 2.2), b: _bB.clone(), t0: tn, col: [1, .72, .2] }); } }
      if (Math.floor(e / 2200) !== bx.cyc) { bx.cyc = Math.floor(e / 2200); for (let i = 0; i < 10; i++) glob(beastPt(bx, cen, dir, new TH.Vector3(), 2), new TH.Vector3(Math.random() - .5, (Math.random() - .5) * .6, Math.random() - .5).multiplyScalar(.6).add(dir).normalize().multiplyScalar(r / 700), 1400, fsC * .4, fsC * 1.2, .9); } }
    else if (kind === "ctort") { const u = (e % 3000) / 3000; if (u < .3 && Math.random() < .5) { const tg = pick(); if (tg) { tg(_bB); glob(beastPt(bx, cen, dir, new TH.Vector3(), .8), _bB.clone().sub(src).multiplyScalar(1 / 700), 700, fsC * .6, fsC * 1.4, .95); if (Math.random() < .3) o.boom(_bB.clone(), 0); } }
      if (Math.floor(e / 3000) !== bx.cyc) { bx.cyc = Math.floor(e / 3000); ring(cen); } }
    else if (kind === "cram") { const u = (e % 4200) / 4200; if (Math.floor(e / 4200) !== bx.cyc) { bx.cyc = Math.floor(e / 4200); bx.fired = 0; }
      if (u < .3) { bx.charge.position.copy(src); bx.charge.scale.setScalar(fsC * (1 + u * 9)); bx.charge.material.opacity = .4 + u * 2; bx.charge.material.color.copy(bx.col); }
      else if (!bx.fired) { bx.fired = 1; ring(src); for (let i = 0; i < 3; i++) { const tg = pick(); if (tg) o.boom(tg(new TH.Vector3()), 1); } }
      if (Math.random() < .2) { const tg = pick(); if (tg) { tg(_bB); o.bl.push({ a: beastPt(bx, cen, dir, new TH.Vector3(), 1), b: _bB.clone(), t0: tn, col: [.7, .9, 1] }); } } }
    else { const Pd = kind === "smoth" ? 2400 : kind === "gspider" ? 2800 : 2000, cy = Math.floor(e / Pd), u = (e % Pd) / Pd; if (cy !== bx.cyc) { bx.cyc = cy; bx.tgt = pick(); bx.fired = 0; }
      if (u < .3) { const a = u / .3; bx.charge.position.copy(src); bx.charge.scale.setScalar(fsC * (.5 + a * 2)); bx.charge.material.opacity = .3 + a * .6; bx.charge.material.color.copy(bx.col); }
      else if (u < .5 && bx.tgt) { const a = (u - .3) / .2, w = fsC * (kind === "smoth" ? .5 : .3) * (1 - a * .5); bx.tgt(_bB); beamSet(bx.beam, src, _bB, w); beamSet(bx.core, src, _bB, w * .3); bx.beam.material.opacity = .85 * (1 - a * .5); bx.core.material.opacity = 1 - a * .4;
        if (!bx.fired) { bx.fired = 1; o.boom(_bB.clone(), kind === "gspider" ? 1 : 0); if (kind === "gspider") ring(_bB); } }
      if (kind === "vmanta" && tn - (bx.lt || 0) > 420) { bx.lt = tn; const tg = pick(); if (tg) { tg(_bB); o.bl.push({ a: beastPt(bx, cen, dir, new TH.Vector3(), 1.6), b: _bB.clone(), t0: tn, col: [.5, .97, 1] }); } } } }
  if (dying && !gone && tn - (bx.dt || 0) > 140) {''')

# --- the Advisor
rep('''  slevi: "A Star Leviathan, Commander.''', '''  vmanta: "A Void Manta, Commander. It glides faster than our frigates and slips half our shots, so send ships that track well: Fighters and Lancers. It drops Exotic Tissue, and sometimes Void Essence.",
  swasp: "That's a Starhive. The nest is armoured, and its wasp swarm stings with acid. Corvettes and Battleships tear through the swarm, and Bombers break the nest. The bigger the hive, the bigger the swarm.",
  ctort: "A Crystal Tortoise. Its shell shrugs off light guns, so bring Bombers and plasma, and be patient. The crystals on its back are real: it often drops Quantum Crystal.",
  gspider: "Careful, Commander. A Gravity Spider. Its lances drag ships out of formation, so send heavy hulls and plenty of them. It sometimes carries Void Essence.",
  smoth: "Solar Moths. Their wing dust strips shields fast, so armour matters more than shields here. Lancers run them down, and they often drop Quantum Crystal.",
  cram: "A Comet Ram is charging the lanes. It hits like a battering ram, horns first, so lead with Battleships and Bastions that can take it. It leaves Reinforced Alloy behind.",
  slevi: "A Star Leviathan, Commander.''')
s2 = re.sub(r"GAME_V = 514\b", "GAME_V = 515", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
# --- v515 the owner's paintings (art/mon/, cut from his sheet; he will send larger ones): a banner on each monster's and pyramid's sheet
s = open(P, encoding='utf-8').read()
def rep2(a, b):
    global s
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
rep2('const voiceKey = s =>', 'const monArt = k => `<div class="monart"><img src="art/mon/${k}.webp?v=1" alt="" loading="lazy"></div>`; /* v515 */\nconst voiceKey = s =>')
rep2(' time accelerator${monAccel(x.lvl).n > 1 ? "s" : ""}.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`', ' time accelerator${monAccel(x.lvl).n > 1 ? "s" : ""}.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>${monArt(x.mon)}`')
rep2('''still guards the halls" : ""}.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>''', '''still guards the halls" : ""}.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>${monArt("pyramid")}''')
rep2('#sheetwrap[data-type="flagship"] .fshero{', '.monart{flex-shrink:0;height:180px;margin:0 -16px 12px;overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#0a1220}.monart img{width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block}\n#sheetwrap[data-type="flagship"] .fshero{')
open(P, 'w', encoding='utf-8').write(s); print('art ok')
# the Archives' Cube and Final Testament records get the owner's paintings in place of their glyphs
s = open(P, encoding='utf-8').read()
a = 'if (k === "testament" || k === "cube") return `<div class="arimg glyph">${k === "cube" ? "◼" : "✦"}</div>`; return'
assert s.count(a) == 1; s = s.replace(a, 'if (k === "testament" || k === "cube") return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/mon/${k}.webp?v=1" alt="" loading="lazy"></div>`; return')
open(P, 'w', encoding='utf-8').write(s); print('arch art ok')
