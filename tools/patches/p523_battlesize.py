# v523 battle replay sizes and room (owner): every hull grows with its class on a steeper ladder (length^1.3 instead of ^1.15), the
# Cube Destroyer is half again as big, and a flagship never sits on top of a squadron: it steps aside across the line of fire until
# space monsters are drawn 35% bigger; the flagship keeps its place at the back and the squadrons make room in front of it. The Solar Moth's battle picture shows its back, head up and wings spread.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 : Math.pow(SIDE_LEN[k] || .5, 1.15) * (BOSSK[k] || 1);',
    'const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 * 1.5 : Math.pow(SIDE_LEN[k] || .5, 1.3) * (BOSSK[k] || 1); /* v523 a steeper class ladder; the Cube Destroyer x1.5 */\nfor (const k in MON) BOSSK[k] = (BOSSK[k] || 1) * 1.35; BOSSK.snest = (BOSSK.snest || 1) * 1.35; /* v523 space monsters loom larger in battle (owner: as fun to watch as possible) */')
rep('if (k === "smoth" && view === "side") ship.rotation.x = 1.15;', 'if (k === "smoth" && view === "side") { ship.rotation.order = "ZYX"; ship.rotation.set(Math.PI / 2, 0, Math.PI / 2); } /* v523 its back: head up, wings spread */')
rep('smoth: 1.6, cram: 1.8 },', 'smoth: 2.4, cram: 1.8 },')
# the flagship's room at the back: each flagship is an immovable footprint in the squadron layout, so every squadron is pushed in
# front of it (or aside) instead of sitting on it; the flagship itself keeps its place behind its line
rep("""    for (let it = 0; it < (P.length > 50 ? 3 : 5); it++) {""", """    if (b.flags && !b.superSide) { const Lf = Math.min(W, H) * .16; for (const sd of ["a", "d"]) for (const e of b.flags[sd] || []) if (e.x != null && e.dead == null) P.push({ i: -1, fixed: 1, x: e.x, y: e.y, rx: Lf * 1.02, ry: Lf * .46, w: 1e6 }); } /* v523 */
    for (let it = 0; it < (P.length > 50 ? 3 : 5); it++) {""")
rep("""      for (const p of P) { p.x = clamp(p.x, x0 + p.rx * .8, x1 - p.rx * .8);""", """      for (const p of P) { if (p.fixed) continue; p.x = clamp(p.x, x0 + p.rx * .8, x1 - p.rx * .8);""")
rep("""    for (const p of P) { const L0 = lay[p.i]; L0.x +=""", """    for (const p of P) { if (p.fixed) continue; const L0 = lay[p.i]; L0.x +=""")
# the neat formation (owner: "find the best placement and fleet pattern so everything fits neatly"): in the usual top/bottom battle,
# each side stands in ranks by class from the front line back: small craft, then frigates and cruisers, then capital ships, then
# titans and stations, each rank spread evenly across the field (a rank too wide for the field splits into two), the ranks sharing the
# side's half of the field by their size, and the flagship's room kept clear behind the last rank. A single monster or boss stands
# centred in its half. Super bosses keep their own staging.
rep("""x0 = W * .03, x1 = W * .97, y0 = top - (bot - top) * .02, y1 = bot + (bot - top) * .04;""", """x0 = W * .03, x1 = W * .97, y0 = top - (bot - top) * .02, y1 = bot + (bot - top) * .04;
    if (!b.superSide && b.fdir !== "x") { const fm = ["a", "d"].map(sd => P.filter(p => Q[p.i].side === sd)), my = fm.map(L => L.length ? L.reduce((a, p) => a + p.y, 0) / L.length : null), mid = (top + bot) / 2, Lf = Math.min(W, H) * .16;
      const RK = { interceptor: 0, fighter: 0, bomber: 0, frigate: 1, cruiser: 1, support: 1, battleship: 2, carrier: 2, capital: 2, titan: 3, station: 3, turret: 3 };
      fm.forEach((L, si) => { if (!L.length || my[si] == null) return; const oy = my[1 - si] != null ? my[1 - si] : (si ? bot : top), dir = oy < my[si] ? -1 : 1, hasF = b.flags && (b.flags[si ? "d" : "a"] || []).some(e => e.dead == null);
        const share = L.length <= 2 && fm[1 - si].length > 2 ? .38 : fm[1 - si].length <= 2 && L.length > 2 ? .6 : .46, front = dir < 0 ? bot - (bot - top) * share : top + (bot - top) * share, back = dir < 0 ? bot - (hasF ? Lf * 1.15 : 0) : top + (hasF ? Lf * 1.15 : 0), D = Math.abs(back - front), rows = [];
        const pack = () => { rows.length = 0; for (let r = 0; r < 4; r++) { const R = L.filter(p => (RK[Q[p.i].role] != null ? RK[Q[p.i].role] : 1) === r).sort((a, c) => a.x - c.x); if (!R.length) continue; let cur = [], w = 0; for (const p of R) { if (cur.length && w + p.rx * 2 > W * .94) { rows.push(cur); cur = []; w = 0; } cur.push(p); w += p.rx * 2; } rows.push(cur); }
          return rows.map(R => Math.max(...R.map(p => p.ry)) * 2); };
        let hs = pack(), sumH = hs.reduce((a, c) => a + c, 0); for (let it = 0; it < 2 && sumH > D; it++) { const kk = Math.max(.45, D / sumH); for (const p of L) { scr[p.i].s *= kk; p.rx *= kk; p.ry *= kk; } hs = pack(); sumH = hs.reduce((a, c) => a + c, 0); } /* too deep: the side is drawn smaller until it fits */
        const k = 1, pad = sumH < D ? (D - sumH) / (rows.length + 1) : 0; let acc = pad;
        rows.forEach((R, ri) => { const yy = front - dir * (acc + hs[ri] * k / 2); acc += hs[ri] * k + pad; const ws = R.reduce((a, p) => a + p.rx * 2, 0), g = Math.max(0, (W * .94 - ws) / (R.length + 1)); let xx = W * .03 + g;
          for (const p of R) { p.x = xx + p.rx; p.y = L.length === 1 ? (front + back) / 2 : yy; xx += p.rx * 2 + g; } }); }); } /* v523 */""")
s2 = re.sub(r"GAME_V = 522\b", "GAME_V = 523", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
