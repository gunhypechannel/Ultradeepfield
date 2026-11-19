# v671 the Mimic Protocol in the Boss Lab (watchable fights, the week-by-week and Omega previews) and in the stress tests.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('const monGone = x =>', R('p671_lab.js') + 'const monGone = x =>')
rep('  return sec("The Omens (Seasons 1 and 2)", om) +', '  return sec("The Mimic Protocol", mimLabHTML(row, b)) + sec("The Omens (Seasons 1 and 2)", om) +')
# Chapter 5 is the Mimic finale now: its preview is the Omega weekend, never the old Kraken
rep('  labPrev: d => { if (!duelOwner()) return; labReset(); const k = d.k;', '  labPrev: d => { if (!duelOwner()) return; labReset(); const k = d.k; if (FIN_EV[k] && FIN_EV[k].typ === "mim") return mimLabOmega(); /* v671 */')
rep('  labStop: () => {', '  mimLabFight: d => { if (!duelOwner()) return; labReset(); mimLabFight(d.k); }, /* v671 */\n  mimLabWeek: d => { if (!duelOwner()) return; const w = +d.k; S.mimPrev = w ? { w, at: now() } : null; MSC = {}; dirty(); toast(w ? `Previewing week ${w} of the Mimic Protocol (this device only).` : "Mimic preview off."); renderSheet(); },\n  labStop: () => {')
# stress tests: the Mimic bosses, with their escorts
rep('  return C; }\nfunction stressCheck(res, fleet, n0, k, F) {', '''  for (const [u, n0, esc, form] of [["malpha1", 100, { mguard: 3, mstalk: 4 }, "Alpha, full"], ["malpha3", 25, { mguard: 3, mstalk: 4 }, "Alpha, last quarter"], ["mnexus", 25, { mguard: 2, mharv: 2 }, "Nexus anchor"], ["momega", 100, { mstalk: 6, mhunt: 3, malpha1: 1 }, "Omega, phase 1"], ["momega", 100, { e_battleship: 2, mguard: 2 }, "Omega, phase 2"], ["momegax", 100, { mstalk: 6, mhunt: 3 }, "Omega Unbound"], ["mnode", 20, { mstalk: 3 }, "Neural Node"], ["mpylon", 20, { mguard: 2 }, "Assimilation Pylon"]])
    C.push({ key: u, t: "mim", form, sh: 1, n0, d0: Object.assign({ [u]: n0 }, esc), mk: () => stacksOf(Object.assign({ [u]: n0 }, esc), { mon: 30 }, "monster") }); /* v671 */
  return C; }
function stressCheck(res, fleet, n0, k, F, d0) {''')
rep('["boss", res.dLeft || {}, { [k]: n0 }]', '["boss", res.dLeft || {}, d0 || { [k]: n0 }]')
rep('const D = c.t === "sb" ? { n: SBW[c.key].n, k: SBW[c.key].u } : c.t === "om" ?', 'const D = c.t === "mim" ? { n: AL[c.key].n, k: c.key } : c.t === "sb" ? { n: SBW[c.key].n, k: SBW[c.key].u } : c.t === "om" ?')
rep('() => stacksOf({ [D.k]: c.n0 }, { wbSh: c.sh }, "wboss"), D.k, c.n0)', '() => c.mk ? c.mk() : stacksOf({ [D.k]: c.n0 }, { wbSh: c.sh }, "wboss"), D.k, c.n0)')
rep('bad = stressCheck(res, STRESS_FLEET, c.n0, D.k, R && R.frames);', 'bad = stressCheck(res, STRESS_FLEET, c.n0, D.k, R && R.frames, c.d0);')
rep('...(c.t === "sb" ? { sbk: c.key,', '...(c.t === "mim" ? {} : c.t === "sb" ? { sbk: c.key,')
rep('const GAME_V = 670;', 'const GAME_V = 671;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
