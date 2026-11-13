# v510 super bosses and the Convergence: harder, and no ship is lost for good (owner). The four super bosses (Vaelthar, Aexion,
# Khezaroth, Medusara) hit 1.5x harder (their hull stays: at 2x the owner's whole fleet could not break a single section); the
# Convergence (the five Elementals and the Pentarch) has twice the hull and hits 1.5x harder; every ship
# they destroy comes home damaged and waits in the Repair Yard (rebuilt over time by the yard, or repaired now for resources), so a
# fight with them costs time, never ships. Other world bosses keep normal losses (45% of losses recovered).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# harder
rep('for (const k in SBW) { const D = SBW[k], hull = Math.round(D.HP * WB_K / 100); AL[D.u] = { n: D.n + " section", atk: Math.round(D.ATK / 100),',
    'const BOSS_HARD = { hull: 1, atk: 1.5 }; /* v510 (hull 2 tested: the strongest fleet in the galaxy then did 0 of 100 sections per attack) */ for (const k in SBW) { const D = SBW[k], hull = Math.round(D.HP * WB_K / 100 * BOSS_HARD.hull); AL[D.u] = { n: D.n + " section", atk: Math.round(D.ATK / 100 * BOSS_HARD.atk),')
rep('["wbEpx", WB.epx]]) { const hull = Math.round(u.hp * WB_K / WB_SEG); AL[k] = { n: u.n, atk: Math.round(u.atk / WB_SEG),',
    '["wbEpx", WB.epx]]) { const cv = /^wbE(ic|fi|li|st|na|px)$/.test(k), hull = Math.round(u.hp * WB_K / WB_SEG * (cv ? 2 : 1)); AL[k] = { n: u.n, atk: Math.round(u.atk / WB_SEG * (cv ? 1.5 : 1)), /* v510 the Convergence: 2x hull, 1.5x firepower */')
# no losses for good: every ship destroyed comes home damaged
rep('function repairDocks(rep, lost) {\n  const back = {}; let n = 0; S.wrecks = S.wrecks || {};\n  for (const k in lost) if (SH[k]) { const v = Math.floor(lost[k] * .45 + Math.random());',
    'function repairDocks(rep, lost, all) { /* v510 all: every ship destroyed comes home damaged (super bosses and the Convergence) */\n  const back = {}; let n = 0; S.wrecks = S.wrecks || {}; if (all) rep.free = 1;\n  for (const k in lost) if (SH[k]) { const v = all ? lost[k] : Math.floor(lost[k] * .45 + Math.random());')
rep('    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));\n    if (seg) { const L = { m: 45000 * seg',
    '    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1); if (rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info");\n    if (seg) { const L = { m: 45000 * seg')
i0 = s.index('async function wbResolve(f) {'); j0 = s.index('f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));', i0); assert j0 - i0 < 6000
s = s[:j0] + 'f.n = cleanShips(res.aLeft); { const cv = WB_EL.includes(key) || key === "epx"; repairDocks(rep, lossesOf(mine0, f.n), cv); if (cv && rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info"); }' + s[j0 + len('f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));'):]
rep('<dt>Lost</dt><dd>${Object.entries(r.lossA)', '<dt>${r.free ? "Damaged · in the Repair Yard" : "Lost"}</dt><dd>${Object.entries(r.lossA)')
rep('${r.repaired ? `<dt>Recovered by repair docks</dt>', '${r.repaired && !r.free ? `<dt>Recovered by repair docks</dt>')
s2 = re.sub(r"GAME_V = 509\b", "GAME_V = 510", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
