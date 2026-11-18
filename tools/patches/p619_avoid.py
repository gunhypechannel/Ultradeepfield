# v619: room to breathe on the map (owner: "Spread remaining monsters event to minimize overlap, monsters should also do best to avoid
# flying through planets, ships should do best to avoid flying through objects").
# 1. (Re-laying the monsters on one even spiral was tried and measured: every object orbits at its own speed, so any static spacing shears
#    away within hours and overlaps were no fewer. Spacing is kept live instead, by 2.)
# 2. Each frame the map keeps a light grid of solid things (planets in view, world bosses, the near stations, fields, vaults and monsters).
#    A monster's swim is nudged around planets and other monsters (sideways and a little up), easing in and out so it never jumps.
# 3. A fleet in flight lifts and slides around the same things, but never round its own start or destination.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the obstacle grid and the push
rep('const ARC = (a, b, k) => {', '/* v619 solid things on the map, in a coarse grid rebuilt every frame; obPush gives the way out of everything near a point */\n'
    'const obGrid = () => ({ c: new Map(), s: 12, q: 0 });\n'
    'function obAdd(Gd, x, y, z, r) { if (!Number.isFinite(x + y + z + r)) return; const s = Gd.s, e = { x, y, z, r, q: 0 }, m = r * 1.6 + 2; for (let i = Math.floor((x - m) / s); i <= Math.floor((x + m) / s); i++) for (let j = Math.floor((z - m) / s); j <= Math.floor((z + m) / s); j++) { const k = i * 100003 + j; let a = Gd.c.get(k); if (!a) Gd.c.set(k, a = []); a.push(e); } }\n'
    'function obPush(Gd, x, y, z, rs, out, skip, up) { out.x = out.y = out.z = 0; if (!Gd) return out; const s = Gd.s, m = rs * 1.6 + 2, q = ++Gd.q;\n'
    '  for (let i = Math.floor((x - m) / s); i <= Math.floor((x + m) / s); i++) for (let j = Math.floor((z - m) / s); j <= Math.floor((z + m) / s); j++) { const a = Gd.c.get(i * 100003 + j); if (!a) continue;\n'
    '    for (const e of a) { if (e.q === q) continue; e.q = q; if (skip && skip(e)) continue; let dx = x - e.x, dy = y - e.y, dz = z - e.z; const d = Math.hypot(dx, dy, dz), need = rs + e.r + .6, zone = need * 1.35; if (d >= zone) continue;\n'
    '      if (d < 1e-3) { dx = 0; dy = 1; dz = 0; } else { dx /= d; dy /= d; dz /= d; } dy += up || 0; const L = Math.hypot(dx, dy, dz) || 1, w = (zone - d) * (.55 + .45 * (1 - d / zone)) / L; /* out to the edge of its zone, softly at the rim */ out.x += dx * w; out.y += dy * w; out.z += dz * w; } }\n'
    '  return out; }\n'
    'const OBV = { x: 0, y: 0, z: 0 }, OBV2 = { x: 0, y: 0, z: 0 };\n'
    'function monAvoid(W, o, q) { if (!W.obG) return; const gs = o.grp.scale.x || 1, b = o.body.position; if (o.mr0 == null) { try { const sp = new TH.Box3().setFromObject(o.body).getBoundingSphere(new TH.Sphere()); o.mr0 = sp.radius > 0 ? Math.min(8, sp.radius / gs) : 2; } catch (e) { o.mr0 = 2; } }\n'
    '  const rM = o.mr0 * gs * .75, x = q.x + b.x * gs, y = q.y + b.y * gs, z = q.z + b.z * gs, P = obPush(W.obG, x, y, z, rM, OBV, null, .35), k = o.cl ? 0 : 1, f = 1 - Math.pow(.8, W.dtk || 1); o.av = o.av || { x: 0, y: 0, z: 0 };\n'
    '  o.av.x += (P.x * k - o.av.x) * f; o.av.y += (P.y * k - o.av.y) * f; o.av.z += (P.z * k - o.av.z) * f; b.x += o.av.x / gs; b.y += o.av.y / gs; b.z += o.av.z / gs; obAdd(W.obG, x + o.av.x, y + o.av.y, z + o.av.z, rM); }\n'
    'const ARC = (a, b, k) => {')
# build the grid before the near models are placed: planets in view and the world bosses
rep('    for (const id of M.near) { const isN = id[0] === "r"', '    { const Gd = W.obG = obGrid(); for (const [, o] of W.planets) obAdd(Gd, o.grp.position.x, o.grp.position.y, o.grp.position.z, o.rad || .8); /* v619 */\n'
    '      if (W.wbM) { const V = W._obV || (W._obV = new TH.Vector3()); for (const k in W.wbM) { const M3 = W.wbM[k]; if (k === "lev" || !M3 || !M3.b || !M3.b.grp || !M3.b.grp.visible) continue; M3.b.grp.getWorldPosition(V); obAdd(Gd, V.x, V.y, V.z, (WB_CLR[k] || 30) * .6); } } }\n'
    '    for (const id of M.near) { const isN = id[0] === "r"')
# a monster weaves round them (not in a fight: it holds where the battle is)
rep('o.body.visible = !down || inClash; o.beacon.position.copy(o.body.position); o.beacon.material.opacity = down ? 0 : .4; o.grp.scale.setScalar(MK_K * (hl && !down ? 1.25 : 1)); }',
    'o.grp.scale.setScalar(MK_K * (hl && !down ? 1.25 : 1)); if (!down || inClash) monAvoid(W, o, q); /* v619 round planets and other monsters */ o.body.visible = !down || inClash; o.beacon.position.copy(o.body.position); o.beacon.material.opacity = down ? 0 : .4; }')
# the near stations, fields and vaults join the grid for the fleets
rep('    // models that left the near set are hidden, then freed\n', '    if (W.obG) for (const M2 of [W.nodes, W.pyramids, W.pirates]) for (const [id, o] of M2) if (!o.mon && M.near.has(id) && o.grp.visible) obAdd(W.obG, o.grp.position.x, o.grp.position.y, o.grp.position.z, 1.6 * (o.grp.scale.x || 1)); /* v619 */\n    // models that left the near set are hidden, then freed\n')
# a fleet in flight lifts and slides round them, never round its own start or destination
rep('else if (o.lastC) o.lastC = null; }', 'else if (o.lastC) o.lastC = null;\n'
    '      if (W.obG && path.k > 0 && path.k < 1) { const rs = Math.min(3, (o.grp.userData.R || 4) * fsF * (o.grp.userData.size || 1) * .35), ea = path.a, eb = path.b, sk = e => Math.hypot(e.x - eb.x, e.z - eb.z) < e.r * 1.6 + 6 || Math.hypot(e.x - ea.x, e.z - ea.z) < e.r * 1.6 + 6, ed = Math.min(1, path.k / .06, (1 - path.k) / .06); /* v619 */\n'
    '        const P = obPush(W.obG, pt.x, pt.y, pt.z, rs, OBV, sk, .8), Q = obPush(W.obG, nx.x, nx.y, nx.z, rs, OBV2, sk, .8), f = 1 - Math.pow(.88, W.dtk || 1); o.av = o.av || { x: 0, y: 0, z: 0 }; o.av.x += (P.x * ed - o.av.x) * f; o.av.y += (P.y * ed - o.av.y) * f; o.av.z += (P.z * ed - o.av.z) * f;\n'
    '        pt = { x: pt.x + o.av.x, y: pt.y + o.av.y, z: pt.z + o.av.z }; nx = { x: nx.x + o.av.x + (Q.x - P.x) * ed, y: nx.y + o.av.y + (Q.y - P.y) * ed, z: nx.z + o.av.z + (Q.z - P.z) * ed }; } else if (o.av) o.av.x = o.av.y = o.av.z = 0; }')
s2 = re.sub(r"GAME_V = 618\b", "GAME_V = 619", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
