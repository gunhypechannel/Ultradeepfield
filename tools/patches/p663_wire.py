# v663 The Mimic Protocol, phase 1 wiring: the hives on the map, their garrison and loot, the hub and the band.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
season = open('tools/patches/p663_season.js', encoding='utf-8').read()
rep('const monGone = x =>', season + 'const monGone = x =>')
rep('.concat(MON_EXTRA, MON_NEW, MON_SP)', '.concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES)')
rep('if (p.mon === "gwhale" && !nightNow()) return true;', 'if (p.mon === "gwhale" && !nightNow()) return true; if (p.mon === "mimic" && !mimLive(p, T || now())) return true; /* v663 */')
rep('const hid = it.mon === "gwhale" && !nightNow();', 'const hid = (it.mon === "gwhale" && !nightNow()) || (it.mon === "mimic" && !mimLive(it, T));')
rep('o.grp.visible = nf && !(G.vmode === "planet" && dc < 9 && !W.cam.cine) && !(it.boss && dvLive(T));', 'o.grp.visible = nf && !(G.vmode === "planet" && dc < 9 && !W.cam.cine) && !(it.boss && dvLive(T)) && !(it.mon === "mimic" && !mimLive(it, T));')
rep('if (it.mon === "sent") { o.body.position.set(0, Math.sin(t * .0003 + it.a0) * .15, 0); o.body.rotation.set(0, it.a0, 0); }',
    'if (it.mon === "sent") { o.body.position.set(0, Math.sin(t * .0003 + it.a0) * .15, 0); o.body.rotation.set(0, it.a0, 0); }\n        if (it.mon === "mimic") { o.body.position.set(0, Math.sin(t * .0004 + it.a0) * .2, 0); o.body.rotation.set(0, t * .00003 + it.a0, 0); o.body.scale.setScalar((.6 + it.lvl * .0082) * (.5 + .17 * mimStage(it, T))); } /* v663 a hive stays put and grows with its stage */')
rep('const xForce0 = x => trainingPir(x) ? { fighter: 1 } : x.mon ? monForce(x.mon, x.lvl) : pirateForce(x.lvl, x.boss);', 'const xForce0 = x => trainingPir(x) ? { fighter: 1 } : x.mon === "mimic" ? mimForce(x) : x.mon ? monForce(x.mon, x.lvl) : pirateForce(x.lvl, x.boss);')
rep('const xRegroup = x => x.mon ? (25 + 3 * x.lvl) * 60000 : pirRegroup(x.lvl, x.boss);', 'const xRegroup = x => x.mon === "mimic" ? MIM_REGROW : x.mon ? (25 + 3 * x.lvl) * 60000 : pirRegroup(x.lvl, x.boss);')
rep('  if (pirDown(x) > f.arrive) { note(`${x.name} was already empty. Fleet returning.`, "warn"); return; }',
    '  if (pirDown(x) > f.arrive) { note(`${x.name} was already empty. Fleet returning.`, "warn"); return; }\n  if (x.mon === "mimic" && !mimLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v663 */\n  const mimSt = x.mon === "mimic" ? mimStage(x, f.arrive) : 0;')
rep('    if (x.mon) try { xsEggDrop(x, rep, f); } catch (e) {} /* v646 */', '    if (x.mon) try { xsEggDrop(x, rep, f); } catch (e) {} /* v646 */\n    if (mimSt) try { mimWin(x, rep, f.arrive); } catch (e) {} /* v663 */')
rep('${xForce(x)[x.mon]} in the ${x.mon === "ssquid" ? "pack" : "pod"}', '${x.mon === "mimic" ? `Stage ${mimStage(x, T)} · ${MIM_STAGE[mimStage(x, T)]}</dd><dt>The brood</dt><dd>${mimForceTxt(x)}` : `${xForce(x)[x.mon]} in the ${x.mon === "ssquid" ? "pack" : "pod"}`}')
rep('if (MON[k] || k === "snest") {', 'if (MON[k] || k === "snest" || MIM_U[k]) {')
rep('function buildMonster(k, part) {', 'function buildMonster(k, part) {\n  if (k === "mimic") return buildMimic("mnest"); /* v663 */')
rep('for (const k in MON) BOSSK[k] = (BOSSK[k] || 1) * 1.35;', 'Object.assign(BOSSK, { mstalk: 1.55, mharv: 1.6, mhunt: 1.55, massim: 1.7, mguard: 1.8, mtitan: 2.5, mnest: 2.1 }); Object.assign(BOSS_GLOW, { mstalk: "95,216,255", mharv: "95,216,255", mhunt: "95,216,255", massim: "95,216,255", mguard: "95,216,255", mtitan: "150,120,255", mnest: "95,216,255" }); /* v663 */\nfor (const k in MON) BOSSK[k] = (BOSSK[k] || 1) * 1.35;')
rep('  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */', '  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */\n  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = mimBand(T); /* v663 */')
rep('hb = omenBand(T) + d1Band(T) + wheelBand();', 'hb = omenBand(T) + d1Band(T) + mimBand(T) + wheelBand();')
rep('  archEntry: d => openSheet({ type: "archives", id: d.id }),', '  archEntry: d => openSheet({ type: "archives", id: d.id }),\n' + open('tools/patches/p663_act.js', encoding='utf-8').read())
rep('  let html = ({ planet: shPlanet,', '  let html = ({ mimic: shMimic, planet: shPlanet,')
rep('const MON_ATK = {', 'const MON_ATK = {\n  mstalk: [["flak", 4, "#7fe0ff", .12, {}], ["laser", 2, "#bff3ff", .16, {}]], mharv: [["acid", 3, "#5fd8ff", .2, {}], ["flak", 3, "#9fe8ff", .14, {}]], mhunt: [["laser", 3, "#9fe8ff", .1, {}], ["flak", 5, "#7fe0ff", .1, {}]],\n  massim: [["ion", 3, "#9fe4ff", .18, {}], ["missile", 3, "#7fd4ff", .2, {}]], mguard: [["flak", 6, "#5fd8ff", .12, {}], ["ion", 2, "#9fe8ff", .22, {}]], mtitan: [["plasma", 3, "#b48cff", .24, { hv: 1 }], ["missile", 6, "#5fd8ff", .2, { flank: 1 }]],\n  mnest: [["missile", 4, "#5fd8ff", .2, { flank: 1 }], ["plasma", 2, "#9b4dff", .26, { hv: 1 }]], /* v663 the Mimics */')
rep('const CPROF = {', 'const CPROF = {\n  mstalk: ["fighter", "acid", .08, .24, 7, 0], mharv: ["support", "acid", .12, .08, 3, 0], mhunt: ["interceptor", "acid", .05, .3, 9, 0], massim: ["cruiser", "ion", .15, .1, 4, 1], mguard: ["cruiser", "acid", .3, .04, 3, 2], mtitan: ["titan", "plasma", .32, 0, 1.6, 4], mnest: ["station", "acid", .3, 0, 0, 2], /* v663 */')
rep('.arfly{', open('tools/patches/p663.css', encoding='utf-8').read().strip() + '\n.arfly{')
rep('const GAME_V = 662;', 'const GAME_V = 663;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
