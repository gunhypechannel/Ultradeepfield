# v665 The Mimic Protocol, phase 2: the Alphas, their Neural Nexuses, server-wide Hive Suppression (owner: "Build it all").
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('const monGone = x =>', R('p665_season.js') + 'const monGone = x =>')
rep('.concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES)', '.concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES, MIM_BOSSES)')
rep('if (p.mon === "mimic" && !mimLive(p, T || now())) return true;', 'if ((p.mon === "mimic" || MIM_BOSS[p.id]) && mimHid(p, T || now())) return true;')
rep('(it.mon === "mimic" && !mimLive(it, T))', '((it.mon === "mimic" || MIM_BOSS[it.id]) && mimHid(it, T))', 2)
rep('        if (it.mon === "mimic") { o.body', '        if (MIM_BOSS[it.id]) { o.body.position.set(0, Math.sin(t * .0003 + it.a0) * .25, 0); o.body.rotation.set(0, it.mon === "nexus" ? 0 : it.a0 + Math.sin(t * .0001 + it.a0) * .5, 0); o.body.scale.setScalar((.6 + it.lvl * .0082) * (it.mon === "nexus" ? 1.5 : 1.8)); } /* v665 the Alphas and Nexuses loom */\n        if (it.mon === "mimic") { o.body')
rep('  if (k === "mimic") return buildMimic("mnest"); /* v663 */', '  if (k === "mimic") return buildMimic("mnest"); /* v663 */\n  if (/^alpha\\d$/.test(k)) return buildMimic("malpha" + k.slice(5)); if (k === "nexus") return buildMimic("mnexus"); /* v665 */')
rep('MON_WAVE.mimic = mimWave("mnest");', 'MON_WAVE.mimic = mimWave("mnest"); for (let i = 1; i <= 4; i++) MON_WAVE["alpha" + i] = mimWave("malpha" + i); MON_WAVE.nexus = mimWave("mnexus"); /* v665 */')
rep('x.mon === "mimic" ? mimForce(x) :', 'MIM_BOSS[x.id] ? alphaForce(x) : x.mon === "mimic" ? mimForce(x) :')
rep('f.xid ? pirateArrive(f)', 'f.xid && MIM_BOSS[f.xid] ? (f.phase = "resolving") : f.xid ? pirateArrive(f)')
rep('else if (f.pid === "nexus" && !f.assault) resolveNexus(f);', 'else if (f.xid && MIM_BOSS[f.xid]) mimBossResolve(f); else if (f.pid === "nexus" && !f.assault) resolveNexus(f);')
rep('  const info = `${el ?', '  const info = MIM_BOSS[x.id] ? mimBossInfo(x, T) + cineBtn(x.id) : `${el ?')
rep('${(x.boss || x.mon) && G.mode === "online" ? `<button class="toggle', '${(x.boss || x.mon) && !MIM_BOSS[x.id] && G.mode === "online" ? `<button class="toggle')
rep('    if (sheet && sheet.joint && (x.boss || x.mon)) {', '    if (sheet && sheet.joint && (x.boss || x.mon) && !MIM_BOSS[x.id]) {')
rep('  M.pts += L.pts; M.kills[st] = (M.kills[st] || 0) + 1;', '  M.pts += L.pts; M.kills[st] = (M.kills[st] || 0) + 1; try { mimQueue(5 * st, mimReg(x)); } catch (e) {} /* v665 */')
rep('M.got["w" + w] = 1; S.shards = (S.shards || 0) + o[2];', 'M.got["w" + w] = 1; M.pend = (M.pend || 0) + 10; setTimeout(() => mimFlush(1), 50); S.shards = (S.shards || 0) + o[2];')
rep('  ${obj}\n', '  ${obj}\n  ${mimHubBoss(T, w)}\n')
rep('  mimFind: ', '  mimGoB: d => { const x = PB[d.id]; if (x) mimGo(x); }, /* v665 */\n  mimFind: ')
rep('    db.doc("event/omega").onSnapshot(', '    for (const d of ["event/mimic", "event/mimic_prev"]) db.doc(d).onSnapshot(s => { (G.mimDoc = G.mimDoc || {})[d] = s.exists ? s.data() : null; mimClaim(); softRender(); }, () => {}); /* v665 */\n    db.doc("event/omega").onSnapshot(')
rep('  mnest:     { n: "Mimic Hive",', '  malpha1:   { n: "Alpha Sovereign I", atk: 900, sh: 2500, hull: 30000, val: 300000, one: 1 },\n  malpha2:   { n: "Alpha Sovereign II", atk: 1100, sh: 2000, hull: 28000, val: 300000, one: 1 },\n  malpha3:   { n: "Alpha Sovereign III", atk: 800, sh: 3200, hull: 34000, val: 300000, one: 1 },\n  malpha4:   { n: "Alpha Sovereign IV", atk: 950, sh: 2600, hull: 30000, val: 300000, one: 1 },\n  mnexus:    { n: "Neural Nexus", atk: 300, sh: 2000, hull: 20000, val: 120000, one: 1 },\n  mnest:     { n: "Mimic Hive",')
rep('  mstalk: ["fighter", "acid", .08, .24, 7, 0],', '  malpha1: ["titan", "plasma", .34, 0, 1.4, 4], malpha2: ["titan", "acid", .3, .05, 2.2, 3], malpha3: ["titan", "acid", .4, 0, 1.2, 5], malpha4: ["titan", "plasma", .34, 0, 1.4, 4], mnexus: ["station", "ion", .3, 0, 0, 4], /* v665 */\n  mstalk: ["fighter", "acid", .08, .24, 7, 0],')
rep('  mnest: [["missile", 4, "#5fd8ff", .2, { flank: 1 }],', '  malpha1: [["plasma", 4, "#7fe0ff", .22, { hv: 1 }], ["missile", 6, "#5fd8ff", .2, { flank: 1 }]], malpha2: [["laser", 4, "#c6a8ff", .12, {}], ["plasma", 3, "#9b6bff", .22, { hv: 1 }]], malpha3: [["ion", 4, "#e4f4ff", .2, {}], ["flak", 8, "#cfe8ff", .12, {}]], malpha4: [["acid", 5, "#5fffc8", .2, {}], ["missile", 6, "#3fffc0", .2, { flank: 1 }]],\n  mnexus: [["ion", 6, "#7ff0ff", .16, {}], ["laser", 4, "#bff8ff", .12, {}]], /* v665 */\n  mnest: [["missile", 4, "#5fd8ff", .2, { flank: 1 }],')
rep('mtitan: 2.5, mnest: 2.1 }); Object.assign(BOSS_GLOW, {', 'mtitan: 2.5, mnest: 2.1, malpha1: 3.2, malpha2: 3.2, malpha3: 3.2, malpha4: 3.2, mnexus: 2.8 }); Object.assign(BOSS_GLOW, { malpha1: "95,216,255", malpha2: "180,140,255", malpha3: "228,244,255", malpha4: "95,255,200", mnexus: "127,240,255",')
rep('.arfly{', R('p665.css').strip() + '\n.arfly{')
# the builder: tintable materials, the Alphas, the Nexus
for a, b in [('g.addColorStop(0, "rgba(40,190,255,.9)"); g.addColorStop(.05, "rgba(40,190,255,.0)"); g.addColorStop(.94, "rgba(40,190,255,0)"); g.addColorStop(1, "rgba(80,220,255,.9)");', 'g.addColorStop(0, "rgba(220,245,255,.9)"); g.addColorStop(.05, "rgba(220,245,255,0)"); g.addColorStop(.94, "rgba(220,245,255,0)"); g.addColorStop(1, "rgba(235,250,255,.9)");'),
             ('x.strokeStyle = `rgba(60,200,255,${', 'x.strokeStyle = `rgba(255,255,255,${')]:
    rep(a, b)
rep('C.shell = new TH.MeshPhysicalMaterial({ map: sC, emissiveMap: sE, emissive: 0xffffff,', 'C.shell = new TH.MeshPhysicalMaterial({ map: sC, emissiveMap: sE, emissive: 0x46ccff,')
rep('function mimMats() { const C = MIMM; if (C.cable) return C;', 'function mimMats(t) { const C = t ? (MIMM[t] || (MIMM[t] = {})) : MIMM; if (C.cable) return C;')
rep('  C.holo = new TH.MeshBasicMaterial({ color: 0x5ff0ff, transparent: true, opacity: .35, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });\n  return C; }',
    '  C.holo = new TH.MeshBasicMaterial({ color: 0x5ff0ff, transparent: true, opacity: .35, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });\n  if (t) { const c = new TH.Color(t), W = new TH.Color(0xffffff); for (const m of [C.cable, C.cableL, C.shell, C.core, C.sac]) m.emissive.copy(c); C.claw.emissive.copy(c).multiplyScalar(.2); C.glow.color.copy(c).lerp(W, .45); C.glowS.color.copy(c).multiplyScalar(.75); C.mouth.color.copy(c).lerp(W, .15); C.holo.color.copy(c).lerp(W, .2); } /* v665 an Alpha\'s own glow */\n  return C; }')
rep('const C = mimMats(), g = new TH.Group(), r = rnd(hash("mim" + cls));', 'const C = mimMats(MIM_TINT[cls]), g = new TH.Group(), r = rnd(hash("mim" + cls));')
rep('  /* the creatures: one recipe, sized and shaped by class */', R('p665_nexus.js') + '  /* the creatures: one recipe, sized and shaped by class */')
rep('    if (D.brood) /* the Brood Titan', R('p665_alphax.js') + '    if (D.brood) /* the Brood Titan')
i = s.index('const MIM_D = '); j = s.index('};', i) + 2
s = s[:j + 1] + R('p665_models.js') + s[j + 1:]
rep('  if (k === "mnest") return `vec3 p = position;', '''  if (k === "mnexus") return `vec3 p = position; float rr = length(p.xz), hc = (1. - smoothstep(2.75, 2.95, rr)) * step(-.35, p.y) * (1. - step(3.15, p.y)), th = mt * .349066, c = cos(th), s = sin(th);
    transformed.xz = mix(transformed.xz, vec2(c * transformed.x - s * transformed.z, s * transformed.x + c * transformed.z), hc);
    float ob = step(3.0, p.y) * (1. - smoothstep(1.7, 2.3, rr)); transformed.y += ob * .2 * sin(mt * 2.0944);
    float sp = smoothstep(-1., 4.5, p.y) * step(2.95, rr) * step(-1.3, p.y); transformed.x += sp * .07 * sin(mt * 2.0944 + atan(p.z, p.x) * 2.); transformed.z += sp * .07 * cos(mt * 2.0944 + atan(p.z, p.x) * 2.);
    float rt = smoothstep(3.3, 4.2, rr) * step(p.y, -1.3); transformed.y += rt * .14 * sin(mt * 4.18879 - rr * 2.2 + atan(p.z, p.x));`;
  if (k === "mnest") return `vec3 p = position;''')
rep('<p class="note">${MON[x.mon].d} Slay it for a hoard of resources, Void Shards and ${monAccel(x.lvl).n} ${monAccel(x.lvl).tier} time accelerator${monAccel(x.lvl).n > 1 ? "s" : ""}.</p>', '<p class="note">${MON[x.mon].d}${MIM_BOSS[x.id] ? "" : ` Slay it for a hoard of resources, Void Shards and ${monAccel(x.lvl).n} ${monAccel(x.lvl).tier} time accelerator${monAccel(x.lvl).n > 1 ? "s" : ""}.`}</p>')
s = s.replace("🜏", "⬢")
rep('const GAME_V = 664;', 'const GAME_V = 665;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
