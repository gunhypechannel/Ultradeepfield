# v357: battle-replay weapons follow ship size. The Dreadnought (bastion) and the Pathfinder (lancer) swap looks, colours kept:
#  - Dreadnought: one big charged mega beam in its purple (was three thin beams), plus its violet missile pods (CAP2).
#  - Pathfinder: quick thin twin beams in its orange from its hardpoints that stop on the target, no screen shake (it used the mega beam
#    because its weapon is "beam"). Mega beams are now only for big hulls (sz 2), stations and titans.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("if (dn) { for (let i = 0; i < 3; i++) b.beams.push({ t0: v.t + i * .06, s: v.s, e: v.e, side, w: clamp(2.3 + Math.log10(1 + many * (q.pow || 1)) * .6, 2.3, 4.6), charge: .2, life: .36, tri: i - 1, dn: 1 });",
    "if (dn) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, w: clamp(5.5 + Math.log10(1 + many * (q.pow || 1)) * 1.4, 5.5, 12), charge: .3, life: .5, dn: 1 }); // v357 one big purple mega beam")
rep("if (dl.length > (b.Q.length > 60 ? 6 : 15)) for (const m of dl.slice(0, dl.length - (b.Q.length > 60 ? 6 : 15)))",
    "if (dl.length > (b.Q.length > 60 ? 2 : 5)) for (const m of dl.slice(0, dl.length - (b.Q.length > 60 ? 2 : 5)))")
rep('  if (wk === "beam" || q.role === "station" || q.role === "titan") { if (b.beams',
    '''  if (wk === "beam" && sz < 2 && q.role !== "station" && q.role !== "titan") { /* v357 small beam ships (the Pathfinder): quick thin twin beams that stop on the target */
    if (b.beams.filter(m => m.sb).length < (b.Q.length > 60 ? 4 : 10)) for (let i = 0; i < 2; i++) b.beams.push({ t0: v.t + i * .07, s: v.s, e: v.e, side, w: clamp(.9 + Math.log10(1 + many) * .35, .9, 1.6), charge: .06, life: .18, lance: 1, sb: 1, tri: i ? .5 : -.5, wk }); return; }
  if (wk === "beam" || q.role === "station" || q.role === "titan") { if (b.beams''')
rep("if (b.beams.filter(m => m.lance).length < (b.Q.length > 60 ? 3 : 6))", "if (b.beams.filter(m => m.lance && !m.sb).length < (b.Q.length > 60 ? 3 : 6))")
rep("for (const m of b.beams) { const A = scr[m.s], E = scr[m.e], age = T - m.t0; if (!A || !E || age < m.charge) continue;",
    "for (const m of b.beams) { const A = scr[m.s], E = scr[m.e], age = T - m.t0; if (!A || !E || age < m.charge || m.sb) continue;")
rep("const [hx, hy] = hp(m.s, m.t0 + .4, 1), [tx, ty] = hp(m.e, m.t0 + .7, 0), lx = tx - hx, ly = ty - hy;",
    "const [hx, hy0] = hp(m.s, m.t0 + .4, 1), [tx, ty] = hp(m.e, m.t0 + .7, 0), hy = hy0 + (m.sb ? m.tri * 7 * d * Math.max(.6, A.s) : 0), lx = tx - hx, ly = ty - hy;")
rep("if (age < m.charge) { const k = age / m.charge, r = (5 + 16 * k) * d;", "if (age < m.charge) { const k = age / m.charge, r = (m.sb ? 3 + 5 * k : 5 + 16 * k) * d;")
rep("if (!m.fs) { m.fs = 1; SFX.laser(m.side === \"d\"); b.shake = Math.max(b.shake, 3 * d); }",
    "if (!m.fs) { m.fs = 1; if (!m.sb || m.tri < 0) SFX.laser(m.side === \"d\"); if (!m.sb) b.shake = Math.max(b.shake, 3 * d); }")
rep("const mr = (7 + m.w * 2.2) * d * al; ctx.globalAlpha = al;", "const mr = (m.sb ? 3 + m.w * 1.5 : 7 + m.w * 2.2) * d * al; ctx.globalAlpha = al;")
rep("if (reach >= 1) { const ir = (10 + m.w * 3) * d * al;", "if (reach >= 1) { const ir = (m.sb ? 5 + m.w * 2 : 10 + m.w * 3) * d * al;")
open(p, "w").write(h); print("ok")
