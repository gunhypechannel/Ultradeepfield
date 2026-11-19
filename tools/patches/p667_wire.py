# v667 Omega: The Convergence (owner spec sections 7, 8, 14; "Build it all"), the Kraken retired (owner: "Remove it, Mimic returns"):
# Season 5 becomes the Season of the Mimic and runs the Mimic Protocol again.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('const monGone = x =>', R('p667_omega.js') + 'const monGone = x =>')
rep('.concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES, MIM_BOSSES)', '.concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES, MIM_BOSSES, MIM_OM)')
rep('const mimT0 = () => VP_BASE + VP_LEN; /* the second Void Pass season */', '''/* v667 the runs: the first in the second Void Pass season (the prologue's Countdown), then every Season of the Mimic (the fifth season of
   the ten-season year, which was the Kraken's): mimT0 is the run under way, or the next one */
const MIM_RUN = k => k === 1 || (k >= PRO && seaCyc(k) === 4);
function mimT0(T = now()) { const c = vpSeason(T); for (let k = Math.max(0, c - 1); k <= c + 12; k++) if (MIM_RUN(k) && VP_BASE + k * VP_LEN + MIM_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + VP_LEN; }''')
rep('return { e: (p.w - 1) * MIM_WK + 3600e3 + Math.max(0, T - p.at), prev: 1 };', 'return { e: (p.om ? MO_D0 : (p.w - 1) * MIM_WK) + 3600e3 + Math.max(0, T - p.at), prev: 1 };')
rep('const B = MIM_BOSS[x.id]; if (!B) return false;', 'const B = MIM_BOSS[x.id]; if (!B) return false; if (B.om) return !moWin(T) || !!moOutcome(moSt(T).o); /* v667 */')
rep('function alphaForce(x, T) { const st = mimSt(T || now()), B = MIM_BOSS[x.id];', 'function alphaForce(x, T) { const st = mimSt(T || now()), B = MIM_BOSS[x.id]; if (B.om) { const { o } = moSt(T || now()); return B.om === 2 ? { mnexus: o.nx.anc.find(v => v > 0) || MO_ANC, mguard: 2, mharv: 2 } : { [moPh(o.hp) === 3 ? "momegax" : "momega"]: Math.max(1, o.shd > 0 ? o.shd : o.hp), mstalk: 6, mhunt: 3 }; }')
rep('function mimBossInfo(x, T) {', 'function mimBossInfo(x, T) { if (MIM_BOSS[x.id].om) return moInfo(x, T);')
rep('else if (f.xid && MIM_BOSS[f.xid]) mimBossResolve(f);', 'else if (f.xid && MIM_BOSS[f.xid]) (MIM_BOSS[f.xid].om ? moResolve(f) : mimBossResolve(f));')
rep('const f = sendFleet(x, n, "pirate", { xid: x.id });', 'const f = sendFleet(x, n, "pirate", MIM_BOSS[x.id] && MIM_BOSS[x.id].om === 1 ? { xid: x.id, omT: S.moTgt || "core" } : { xid: x.id });')
rep('(it.mon === "nexus" ? 1.5 : 1.8)', '(it.om === 1 ? 4.2 : it.om === 2 ? 2.6 : it.mon === "nexus" ? 1.5 : 1.8)')
rep('function mimClaim() { if (!S || !G.ready) return;', 'function mimClaim() { if (!S || !G.ready) return; try { moClaimM(); } catch (e) {}')
rep('function mimBand(T) {', 'function mimBand(T) { if (!G.moCC || Date.now() - G.moCC > 4000) { G.moCC = Date.now(); setTimeout(() => { try { moCineCheck(); } catch (e) {} }, 400); } /* v667 */')
rep('  ${mimHubBoss(T, w)}\n', '  ${moHub(T, w)}\n  ${mimHubBoss(T, w)}\n')
rep('data-act="mimPrev" data-w="${n}">${n ? "Week " + n : "Off"}</button>`).join("")}', 'data-act="mimPrev" data-w="${n}">${n ? "Week " + n : "Off"}</button>`).join("")}<button class="btn${(S.mimPrev || {}).om ? " pri" : ""}" data-act="mimPrev" data-w="4" data-om="1">Omega</button>')
rep('  mimGoB: d => {', '''  moTgt: d => { S.moTgt = d.t; renderSheet(); }, /* v667 */
  moCine: d => moCine(d.k || "arr"), moFinal: () => moFinal(),
  mimGoB: d => {''')
rep('const w = +d.w; S.mimPrev = w ? { w, at: now() } : null;', 'const w = +d.w; S.mimPrev = w ? { w, at: now(), om: d.om ? 1 : 0 } : null; MSC = {};')
# models
rep('const MIM_TINT = { malpha2: 0x9b6bff, malpha3: 0xd8f0ff, malpha4: 0x3fffc0 };', '''const MIM_TINT = { malpha2: 0x9b6bff, malpha3: 0xd8f0ff, malpha4: 0x3fffc0, momegax: 0xd8f8ff };
Object.assign(MIM_D, { momega: { s: 2.0, legs: 4, mane: 70, hump: 1.2, len: 1.3, gape: 1.0, tail: 30, alpha: 1, omega: 1 }, momegax: { s: 2.0, legs: 4, mane: 70, hump: 1.2, len: 1.3, gape: 1.1, tail: 30, alpha: 1, omega: 2 } }); /* v667 */''')
rep('    if (D.alpha) { /* an Alpha', R('p667_omegax.js') + '    if (D.alpha) { /* an Alpha')
rep('  if (/^e_/.test(cls)) {', R('p667_models.js') + '  if (/^e_/.test(cls)) {')
rep('  if (k === "mnexus") return `vec3 p = position;', '  if (k === "mnode" || k === "mpylon") return `vec3 p = position; transformed.y += .12 * sin(mt * 2.0944) * smoothstep(-1., 2., p.y); transformed.x += .05 * sin(mt * 2.0944 + p.y) * smoothstep(0., 3., p.y);`; /* v667 */\n  if (k === "mnexus") return `vec3 p = position;')
rep('  if (/^alpha\\d$/.test(k)) return buildMimic("malpha" + k.slice(5)); if (k === "nexus") return buildMimic("mnexus"); /* v665 */', '  if (/^alpha\\d$/.test(k)) return buildMimic("malpha" + k.slice(5)); if (k === "nexus") return buildMimic("mnexus"); if (k === "omega") return buildMimic("momega"); /* v665, v667 */')
rep('MON_WAVE.nexus = mimWave("mnexus");', 'MON_WAVE.nexus = mimWave("mnexus"); MON_WAVE.omega = mimWave("momega");')
rep('  mnexus:    { n: "Neural Nexus",', '  momega:    { n: "Omega", atk: 1400, sh: 3500, hull: 38000, val: 500000, one: 1 },\n  momegax:   { n: "Omega Unbound", atk: 2200, sh: 1500, hull: 30000, val: 500000, one: 1 },\n  mnode:     { n: "Neural Node", atk: 200, sh: 900, hull: 9000, val: 60000, one: 1 },\n  mpylon:    { n: "Assimilation Pylon", atk: 350, sh: 1400, hull: 11000, val: 60000, one: 1 },\n  mnexus:    { n: "Neural Nexus",')
rep(' mnexus: ["station", "ion", .3, 0, 0, 4], /* v665 */', ' mnexus: ["station", "ion", .3, 0, 0, 4], /* v665 */ momega: ["titan", "plasma", .38, 0, 1.2, 6], momegax: ["titan", "plasma", .2, 0, 1.6, 4], mnode: ["station", "ion", .25, 0, 0, 2], mpylon: ["station", "laser", .3, 0, 0, 3], /* v667 */')
rep('  mnexus: [["ion", 6,', '  momega: [["plasma", 5, "#e8fbff", .26, { hv: 1 }], ["missile", 8, "#5fd8ff", .2, { flank: 1 }]], momegax: [["plasma", 6, "#ffffff", .3, { hv: 1 }], ["laser", 6, "#9ff0ff", .12, {}]], mnode: [["ion", 3, "#7ff0ff", .2, {}]], mpylon: [["laser", 4, "#9ff0ff", .14, {}]], /* v667 */\n  mnexus: [["ion", 6,')
rep('malpha4: 3.2, mnexus: 2.8 }); Object.assign(BOSS_GLOW, {', 'malpha4: 3.2, mnexus: 2.8, momega: 4.2, momegax: 4.2, mnode: 2.2, mpylon: 2.4 }); Object.assign(BOSS_GLOW, { momega: "191,246,255", momegax: "232,251,255", mnode: "127,240,255", mpylon: "127,240,255",')
# the Kraken retires: its finale slot, its Saturday, its season's name
rep('["med", "krk"]', '["med", null]')
rep('ROTS_X = ["lev", "krk"]', 'ROTS_X = ["lev"]')
rep('g === 2 ? ["brd", "tyr", "wym", "col", "lev", "krk"]', 'g === 2 ? ["brd", "tyr", "wym", "col", "lev"]')
rep('["Season of the Kraken", "#c890ff", "kraken", "Kraken Hunter"]', '["Season of the Mimic", "#5fd8ff", "kraken", "Swarmbreaker"]')
rep('"Starhive", "Kraken", "Wyrm"', '"Starhive", "Mimic", "Wyrm"')
rep('const finKeys = () => Object.keys(FIN_EV).filter(k => FIN_EV[k].typ !== "omen"', 'const finKeys = () => Object.keys(FIN_EV).filter(k => k !== "krk" && FIN_EV[k].typ !== "omen"')
rep('.arfly{', R('p667.css').strip() + '\n.arfly{')
rep('pts.push(V(e.x - Lx * .22 * j,', 'pts.push(V(e.x - Lx * .13 * j,') # shorter Echo drive tendrils
rep('const GAME_V = 666;', 'const GAME_V = 667;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
