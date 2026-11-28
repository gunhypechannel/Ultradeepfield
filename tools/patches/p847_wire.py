"""v847: the Battle Lab covers every Carcinid and Continuum wave, as the Mimic one does (owner: "i want battle tests similar to all mimic
waves for the crabs and the continuum"): Carcinid patrols for weeks 1-3 beside week 4; Continuum patrols and fabrication platforms at
each stage band, and the Prime Resurrection Ark finale."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 846;", "const GAME_V = 847;")
# Carcinid patrols, week by week (the same make-up crcForce gives a level-20 patrol)
rep('''  ["crcp", "Carcinid patrol (week 4)", () => ({ cfrig: 2, cint: 5, cpearl: 2, cdest: 1, cmint: 2, cvang: 1, ccarr: 1 })],''',
    '''  ["crcp1", "Carcinid patrol (week 1)", () => ({ cfrig: 3, cint: 5 })], ["crcp2", "Carcinid patrol (week 2)", () => ({ cfrig: 3, cint: 5, cpearl: 2 })],
  ["crcp3", "Carcinid patrol (week 3)", () => ({ cfrig: 3, cint: 5, cpearl: 2, cdest: 1, cmint: 2 })],
  ["crcp", "Carcinid patrol (week 4)", () => ({ cfrig: 2, cint: 5, cpearl: 2, cdest: 1, cmint: 2, cvang: 1, ccarr: 1 })],''')
rep('mon: B ? B.mon : k === "crcp" ? "crcpat" :', 'mon: B ? B.mon : /^crcp/.test(k) ? "crcpat" :')
# the Continuum, stage by stage (cntForce's make-up at level 20), and the finale
rep('const CNT_LAB = [["kp", "Continuum patrol (stage 6)", () => ({ cnint: 6, cncor: 2, cnexe: 1, cnasm: 1 })], ["kf", "Fabrication platform (stage 6)", () => ({ cnfab: 1, cnint: 9, cnexe: 2, cnasm: 1, cndre: 1 })],',
    '''const CNT_LAB = [["kp1", "Continuum patrol (stages 1-3)", () => ({ cnint: 5, cncor: 2 })], ["kp4", "Continuum patrol (stages 4-5)", () => ({ cnint: 5, cncor: 2, cnexe: 1 })], ["kp", "Continuum patrol (stage 6)", () => ({ cnint: 6, cncor: 2, cnexe: 1, cnasm: 1 })],
  ["kf1", "Fabrication platform (stages 1-3)", () => ({ cnfab: 1, cnint: 8, cnexe: 2 })], ["kf4", "Fabrication platform (stages 4-5)", () => ({ cnfab: 1, cnint: 8, cnexe: 2, cnasm: 1 })], ["kf", "Fabrication platform (stage 6)", () => ({ cnfab: 1, cnint: 9, cnexe: 2, cnasm: 1, cndre: 1 })],''')
rep('["ketr", "The Eternal Commander", () => ({ cneter: 20, cndre: 2, cnasm: 2, cnexe: 4, cncor: 2 })]];',
    '["ketr", "The Eternal Commander", () => ({ cneter: 20, cndre: 2, cnasm: 2, cnexe: 4, cncor: 2 })], ["kprime", "The Prime Resurrection Ark (finale)", () => ({ cnprime: 20, cneter: 1, cndre: 2, cnasm: 2, cnexe: 4, cncor: 2, cnint: 6 })]];')
rep('const D0 = L[2](), big = k.length > 2, A0 = big ? MIM_LAB_FLEET', 'const D0 = L[2](), big = cntLabBig(k), A0 = big ? MIM_LAB_FLEET')
rep('mon = k === "kp" ? "cnpat" : k === "kf" ? "cnplat" : k === "krel"', 'mon = /^kp(\\d|$)/.test(k) ? "cnpat" : /^kf/.test(k) ? "cnplat" : k === "kprime" ? "cnprimem" : k === "krel"')
rep('CNT_LAB.map(([k, n]) => row0("⬢", n, k.length > 2 ?', 'CNT_LAB.map(([k, n]) => row0("⬢", n, cntLabBig(k) ?')
rep("function cntLabFight(k) {", "const cntLabBig = k => /^k(rel|ark|cmd|etr|prime)$/.test(k);\nfunction cntLabFight(k) {")
open(p, "w", encoding="utf-8").write(s); print("ok")
