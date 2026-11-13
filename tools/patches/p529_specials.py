# v529 the special creatures (owner: "Do it all, add them!"): Kraken Egg clutches, the Ghost Whale (it only surfaces at night, the
# player's local 19:00-06:00), Rock Eaters, Celestial Serpent hatchlings and Petrified Sentinels. Each has stats and a fighting style,
# a 3D model that moves (breathing eggs and swaying root-tendrils, a whale of light with its skeleton showing, chewing worms, a
# writhing gold serpent, a stone giant with orbiting shards), its own map battle effects, Advisor lines and a material it leans to.
# 250 of them (w2400-w2649) on a fourth spiral, so every monster already out there keeps its species and place.
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p529_specials.js'), encoding='utf-8').read()
part = lambda name: J.split('//@@' + name + '\n')[1].split('//@@')[0]
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''  cram:      { n: "Comet Ram", atk: 3800, sh: 1600, hull: 42000, val: 140000, one: 1 }
};''', '''  cram:      { n: "Comet Ram", atk: 3800, sh: 1600, hull: 42000, val: 140000, one: 1 },
  // v529 the special creatures
  kegg:      { n: "Kraken Egg Clutch", atk: 400, sh: 3200, hull: 30000, val: 130000, one: 1 },
  gwhale:    { n: "Ghost Whale", atk: 1200, sh: 4000, hull: 50000, val: 200000, one: 1 },
  reat:      { n: "Rock Eaters", atk: 800, sh: 600, hull: 12000, val: 35000, one: 1 },
  cserp:     { n: "Celestial Serpent", atk: 2000, sh: 2000, hull: 20000, val: 120000, one: 1 },
  sent:      { n: "Petrified Sentinel", atk: 3200, sh: 3000, hull: 80000, val: 180000, one: 1 }
};''')
rep('cram: ["capital", "mass", .35, .02, 4.2, 1], wbOvl:', 'cram: ["capital", "mass", .35, .02, 4.2, 1], kegg: ["station", "acid", .3, 0, 0, 2], gwhale: ["capital", "ion", .1, .4, 5, 1], reat: ["cruiser", "mass", .3, .05, 4, 1], cserp: ["cruiser", "plasma", .12, .22, 6, 1], sent: ["titan", "mass", .45, 0, 0, 3], wbOvl:')
rep('const MON_K = ["swhale", "slevi", "ssquid"], MON_K2 =', '''Object.assign(MON, { /* v529 the special creatures */
  kegg: { n: "Kraken Egg Clutch", sp: "Kraken Eggs", ic: "🥚", col: "#c87aff", rgb: "200,122,255", per: 6, d: "A drifting clutch of glass eggs in a nest of black thorns, each lit violet from inside. The clutch barely fights, but its nest is tough, and something laid it.", names: ["the Violet Clutch", "Brood of the Deep", "the Drifting Nest", "Mother's Hoard", "the Sleeping Six", "Inkbloom"] },
  gwhale: { n: "Ghost Whale", sp: "Ghost Whale", ic: "🐋", col: "#7af4ff", rgb: "122,244,255", per: 8, d: "A whale of cold light with its skeleton glowing through its skin. It only surfaces at night, and by morning it is gone.", names: ["the Pale Singer", "Moonwake", "the Drowned Light", "Hollowsong", "Night Tide", "the Last Breath"] },
  reat: { n: "Rock Eaters", sp: "Rock Eaters", ic: "🪨", col: "#ff9a4a", rgb: "255,154,74", per: 3, d: "Barrel worms of plated stone that chew through asteroids, and through hulls. Their maws glow with the heat of what they swallow.", names: ["the Gnawing Three", "Grindmaw", "Stonegut", "the Hungry Belt", "Crushjaw", "Quarry Kin"] },
  cserp: { n: "Celestial Serpent", sp: "Celestial Serpent", ic: "🐍", col: "#ffd36b", rgb: "255,211,107", per: 7, d: "A hatchling of the Celestial Serpents: midnight scales edged in gold, violet fire in its eyes. It moves faster than our frigates and leaves a trail of light.", names: ["Little Sun", "Goldcoil", "the Bright Hatchling", "Emberscale", "Dawnling", "Solace"] },
  sent: { n: "Petrified Sentinel", sp: "Petrified Sentinel", ic: "🗿", col: "#6affb8", rgb: "106,255,184", per: 12, d: "A stone guardian the size of a mountain, moss in its seams and green runes waking along its body. It does not move. It does not need to.", names: ["the Watcher of the Pass", "Old Granite", "Mossguard", "the Unmoved", "Runekeeper", "Stonesworn"] }
});
const nightNow = () => { const h = new Date().getHours(); return h >= 19 || h < 6; }; /* v529 the Ghost Whale surfaces only at night, the player's own night */
const MON_K = ["swhale", "slevi", "ssquid"], MON_K2 =''')
rep('const MON_K = ["swhale", "slevi", "ssquid"], MON_K2 = ["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"];', 'const MON_K = ["swhale", "slevi", "ssquid"], MON_K2 = ["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"], MON_K3 = ["kegg", "gwhale", "reat", "cserp", "sent"];')
rep('const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW);', '''/* v529 the special creatures: 250 more (w2400-w2649: 60 clutches, 40 ghost whales, 70 rock-eater packs, 30 serpents, 50 sentinels) on a fourth spiral */
const MON_SP = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6, rm = rnd(8391), mix = []; [["kegg", 60], ["gwhale", 40], ["reat", 70], ["cserp", 30], ["sent", 50]].forEach(([k, n]) => { for (let i = 0; i < n; i++) mix.push(k); });
  for (let j = 0; j < mix.length; j++) { const mk = mix[(j * 97) % mix.length], u = (j + .6) / mix.length, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (4.1 + j * GOLD) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 1 + (Math.floor(j / 5) * 7) % 5, M = MON[mk];
    out.push({ id: "w" + (MON_N + MON_X + MON_Y + j), kind: "pirate", mon: mk, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `${M.names[(rm() * M.names.length) | 0]} · ${M.sp}` }); } return out; })();
const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW, MON_SP);''')
rep('`${pool.length} space monsters of nine kinds drift across every layer:', '`${pool.length} space monsters of fourteen kinds drift across every layer (the Ghost Whale only at night):')
rep('try { for (const k of MON_K.concat(MON_K2)) {', 'try { for (const k of MON_K.concat(MON_K2, MON_K3)) {')
rep('const MON_LOOT = { ctort: ["crystal", .7],', 'const MON_LOOT = { kegg: ["void", .5], gwhale: ["crystal", .6], reat: ["alloy", .7], cserp: ["void", .45], sent: ["cube", .4], ctort: ["crystal", .7],')
# night: the Ghost Whale isn't drawn or listed by day
rep('A.aCol[j + 3] = !nf || M.near.has(it.id) || (it.boss && dvLive(T)) ? 0 :', 'const hid = it.mon === "gwhale" && !nightNow(); A.aCol[j + 3] = hid || !nf || M.near.has(it.id) || (it.boss && dvLive(T)) ? 0 :')
rep('    if (nf) { const dc = Math.hypot(x - cp.x, P3(it, T, PQS).y - cp.y, z - cp.z),', '    if (nf && !hid) { const dc = Math.hypot(x - cp.x, P3(it, T, PQS).y - cp.y, z - cp.z),')
# battle look
rep('    case "cram": ', '''    case "kegg": for (const [x, y, r] of [[0, -.35, .42], [-.45, .2, .36], [.45, .2, .36], [0, .55, .3]]) { ctx.beginPath(); ctx.ellipse(x, y, r * .8, r, 0, 0, TAU); ctx.fill(); } break;
    case "gwhale": ctx.ellipse(0, 0, .45, 1.0, 0, 0, TAU); ctx.fill(); ctx.beginPath(); P([0, .9, -.5, 1.3, .5, 1.3]); ctx.fill(); break;
    case "reat": for (const [x, y] of [[-.4, -.2], [.4, -.1], [0, .5]]) { ctx.beginPath(); ctx.arc(x, y, .32, 0, TAU); ctx.fill(); } break;
    case "cserp": ctx.lineWidth = .28; ctx.beginPath(); ctx.moveTo(0, -.9); ctx.bezierCurveTo(.8, -.4, -.8, .3, 0, 1.0); ctx.stroke(); break;
    case "sent": ctx.fillRect(-.45, -.8, .9, 1.1); ctx.fillRect(-.75, -.55, .3, .8); ctx.fillRect(.45, -.55, .3, .8); ctx.fillRect(-.35, .3, .25, .6); ctx.fillRect(.1, .3, .25, .6); break;
    case "cram": ''')
rep('smoth: 2.4, cram: 1.8 },', 'smoth: 2.4, cram: 1.8, kegg: 1.6, gwhale: 1.9, reat: 1.5, cserp: 1.6, sent: 1.9 },')
rep('BOSS_GLOW = { vmanta: "122,244,255",', 'BOSS_GLOW = { kegg: "200,122,255", gwhale: "122,244,255", reat: "255,154,74", cserp: "255,211,107", sent: "106,255,184", vmanta: "122,244,255",')
rep('smoth: 1.2, cram: 1.5 };', 'smoth: 1.2, cram: 1.5, kegg: 1.1, gwhale: 1.5, reat: 1.2, cserp: 1.3, sent: 1.4 };')
# 3D
rep('''  return C;
}
const MONM = {};''', part('MATS') + '''  return C;
}
const MONM = {};''')
rep('''  }
  return g;
}
function buildAlien(k) {''', part('MODELS') + '''  }
  return g;
}
function buildAlien(k) {''')
rep('''geo.rotateZ(-Math.PI / 2); return add(new TH.Mesh(geo, mat)); };
  if (k === "swhale") {''', '''geo.rotateZ(-Math.PI / 2); return add(new TH.Mesh(geo, mat)); };
''' + part('HELPERS') + '''  if (k === "swhale") {''')
rep('''  vmanta: "float sp = abs(position.z)''', '''  /* v529 the special creatures: the clutch breathes and its branches and roots sway; the Ghost Whale swims with slow beats of its tail and
     flippers; the Rock Eaters squirm on their asteroid; the Serpent winds along its length and lifts its head; the Sentinel breathes,
     turns its head slowly from side to side, and the shards of its mountain circle it */
  kegg: "vec3 p = position; float rr = length(p.xz), ph = atan(p.z, p.x) * 2.; transformed.xz += normalize(p.xz + vec2(.001)) * smoothstep(-.4, 1.4, p.y) * .05 * sin(mt * 1.5 + ph); transformed.y += smoothstep(-.2, 1.6, p.y) * .035 * sin(mt * 1.5 + ph + 1.); float rt = smoothstep(-1.25, -2.6, p.y); transformed.x += rt * .3 * sin(mt * 1.1 + p.z * 1.5); transformed.z += rt * .3 * cos(mt * .9 + p.x * 1.5);",
  gwhale: "vec3 p = position; float su = clamp((1.4 - p.x) / 6.1, 0., 1.); transformed.y += (.03 + .8 * su * su) * sin(p.x * .5 + mt * 1.15); float fz = abs(p.z), fin = smoothstep(1.1, 3.4, fz) * step(-3.2, p.x); transformed.y += fin * .6 * sin(mt * .85 - fz * .5); transformed.x -= fin * .15 * cos(mt * .85 - fz * .5); transformed.y += .06 * sin(mt * .6);",
  reat: "vec3 p = position; float w = smoothstep(-1.5, -.7, p.y); transformed.y += w * .08 * sin(mt * 2. + p.x * 1.3 + p.z * 1.1); transformed.z += w * .06 * sin(mt * 1.6 + p.x * 1.7); transformed.x += w * .04 * sin(mt * 2.3 + p.z * 2.);",
  cserp: "vec3 p = position; float tl = clamp((2.2 - p.x) / 7.2, 0., 1.); transformed.z += (.04 + .5 * tl) * sin(p.x * 1.15 + mt * 2.6); transformed.y += .16 * tl * cos(p.x * .9 + mt * 2.); float hd = smoothstep(1.6, 3.6, p.x); transformed.y += hd * .12 * sin(mt * 1.2); transformed.z += hd * .1 * sin(mt * .7);",
  sent: "vec3 p = position; float rr = length(p.xz); if (rr > 3.5) { float th = mt * .22, c = cos(th), sn = sin(th); transformed.xz = vec2(p.x * c - p.z * sn, p.x * sn + p.z * c); transformed.y += .18 * sin(mt * .7 + rr * 9.); } else { transformed.y += smoothstep(-.8, 1.4, p.y) * .04 * sin(mt * .7); float hw = smoothstep(1.72, 1.95, p.y) * (1. - smoothstep(1., 1.2, abs(.814 * p.x - .581 * p.z))), yaw = .2 * sin(mt * .28) * hw, c = cos(yaw), sn = sin(yaw); transformed.xz = vec2(transformed.x * c - transformed.z * sn, transformed.x * sn + transformed.z * c); }",
  vmanta: "float sp = abs(position.z)''')
rep('const MON_SWIM = { vmanta: .00026,', 'const MON_SWIM = { kegg: .00005, gwhale: .0002, reat: .00012, cserp: .00035, vmanta: .00026,')
rep('const NEWBEAST = new Set(["vmanta", "swasp", "ctort", "gspider", "smoth", "cram"]);', 'const NEWBEAST = new Set(["vmanta", "swasp", "ctort", "gspider", "smoth", "cram", "kegg", "gwhale", "reat", "cserp", "sent"]);')
rep('const BEAST_FX = { vmanta: [122, 244, 255],', 'const BEAST_FX = { kegg: [200, 122, 255], gwhale: [122, 244, 255], reat: [255, 154, 74], cserp: [255, 211, 107], sent: [106, 255, 184], vmanta: [122, 244, 255],')
# how they fight a fleet on the map: eggs and rock eaters spit like the hive, the sentinel slams like the tortoise, whale and serpent lance
rep('    if (kind === "swasp") { if (tn - (bx.lt || 0) > 110) {', '    if (kind === "kegg" || kind === "reat") { if (tn - (bx.lt || 0) > (kind === "reat" ? 200 : 320)) { bx.lt = tn; const tg = pick(); if (tg) { tg(_bB); glob(beastPt(bx, cen, dir, new TH.Vector3(), 1.2), _bB.clone().sub(src).multiplyScalar(1 / 600), 600, fsC * .5, fsC * 1.2, .95); if (Math.random() < .25) o.boom(_bB.clone(), 0); } } }\n    else if (kind === "sent") { const u = (e % 3400) / 3400; if (Math.floor(e / 3400) !== bx.cyc) { bx.cyc = Math.floor(e / 3400); ring(cen); for (let i = 0; i < 3; i++) { const tg = pick(); if (tg) o.boom(tg(new TH.Vector3()), 1); } } if (u < .25 && Math.random() < .4) { const tg = pick(); if (tg) { tg(_bB); glob(beastPt(bx, cen, dir, new TH.Vector3(), .8), _bB.clone().sub(src).multiplyScalar(1 / 700), 700, fsC * .7, fsC * 1.5, .95); } } }\n    else if (kind === "swasp") { if (tn - (bx.lt || 0) > 110) {')
# Ghost Whale and the Rock Eaters' sentinel stand still; the sentinel holds its place
rep('        if (it.mon === "swasp") { o.body.position.set(0,', '        if (it.mon === "sent") { o.body.position.set(0, Math.sin(t * .0003 + it.a0) * .15, 0); o.body.rotation.set(0, it.a0, 0); } /* v529 the Sentinel does not move */\n        if (it.mon === "swasp") { o.body.position.set(0,')
rep('''  cram: "A Comet Ram is charging the lanes.''', '''  kegg: "Kraken eggs, Commander. The clutch barely fights back, but its nest is tough. Break it for Void Essence before whatever laid it comes back.",
  gwhale: "A Ghost Whale. They only surface at night, and they slip half our shots. If you see one, hunt it now. It won't be there in the morning.",
  reat: "Rock Eaters. They chew through asteroids and armour alike, so send shields and hit them hard. They leave Reinforced Alloy behind.",
  cserp: "A Celestial Serpent hatchling. Young, fast and burning hot. Bring fast ships. It often carries Void Essence.",
  sent: "A Petrified Sentinel. It doesn't move, but it hits like a mountain. Bring your heaviest fleet. Something old is buried in it: it drops Cube Fragments.",
  cram: "A Comet Ram is charging the lanes.''')
# by day the Ghost Whale is not in the hunt lists or counts either, and its spot reads as empty space
rep('function isFogged(p, T) { if (!p || p.owner === G.me) return false;', 'function isFogged(p, T) { if (!p || p.owner === G.me) return false; if (p.mon === "gwhale" && !nightNow()) return true; /* v529 gone by day */')
# their paintings on the monster sheet (the files carry the paintings' own names)
rep('${monArt(x.mon)}`', '${monArt(MON_ARTF[x.mon] || x.mon)}`')
rep('const monArt = k =>', 'const MON_ARTF = { kegg: "kraken", gwhale: "ghostwhale", reat: "rockeater", cserp: "cserpent", sent: "sentinel" }; /* v529 */\nconst monArt = k =>')
s2 = re.sub(r"GAME_V = 528\b", "GAME_V = 529", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
