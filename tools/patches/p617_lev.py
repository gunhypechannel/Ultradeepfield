# v617 the Leviathan swims the edge of the galaxy (owner: "It should be almost swimming around the edges of the map, not coiled up",
# "so long that it almost nearly eats its own tail around the edges"). The Leviathan's model (BOSS3D wyrm("lev")) gets a ring mode:
# when the map or the finale set piece hands it a ring ({R0, Rh, a, y, k, s}), its body is laid along the galaxy's edge, 93% of the
# way round, head nearly at its own tail, with a swimming wave running head to tail; its head can leave the ring (the breach).
# Battles and previews still use the coiled form. On the map it now laps the galaxy every 4 hours (it was 36).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const N = LOD === 1 ? 30 : 42, accM', 'const N = LV ? (LOD === 1 ? 84 : 110) : LOD === 1 ? 30 : 42, accM')
rep('      for (let i = 0; i <= N + 1; i++) path(i / N, t, pts[i]);',
    '''      const RG = LV && out.ring; /* v617 laid round the galaxy's edge */
      const TW = RG ? Math.max(coil, gape) : 0, UT = .2; out.tw = TW; /* its attack: the front of the body coils up into a tower and the head looks down */
      if (RG) { const k = Math.max(.04, RG.k), L = TAU * .93 * k, tb = RG.a - UT * L, bx = Math.cos(tb) * RG.R0, bz = Math.sin(tb) * RG.R0, HT = RG.s * 14, RC = RG.s * 2.4;
        for (let i = 0; i <= N + 1; i++) { const u = i / N, th = RG.a - u * L, Rr = RG.R0 + (RG.Rh - RG.R0) * Math.exp(-u * 9), w = RG.s * .6 * (.3 + .7 * u) * Math.sin(u * TAU * 9 - t * .0024) + RG.s * 1.6 * Math.sin(th * 3 + t * .00017) * (1 - Math.exp(-u * 9)) /* drifting in and out along the edge */, y = RG.y + RG.s * .3 * Math.sin(u * TAU * 6 - t * .0017) + (RG.yh - RG.y) * Math.exp(-u * 9); pts[i].set(Math.cos(th) * (Rr + w), y, Math.sin(th) * (Rr + w));
          if (TW > .001 && u < UT) { const q = 1 - u / UT, wgt = TW * Math.min(1, q * 4), ph = q * TAU * 2.6 + t * .0006; tmp.set(bx + Math.cos(ph) * RC * (1 - q * .35), RG.y + q * HT, bz + Math.sin(ph) * RC * (1 - q * .35)); pts[i].lerp(tmp, wgt); } } }
      else for (let i = 0; i <= N + 1; i++) path(i / N, t, pts[i]);''')
rep('for (let i = 0; i < N; i++) { const u = i / N, sc = 2.35 * (1 - u * .62) * (i === 0 ? 1.1 : 1);', 'for (let i = 0; i < N; i++) { const u = i / N, sc = (RG ? RG.s * (1 - u * .55) : 2.35 * (1 - u * .62)) * (i === 0 ? 1.1 : 1);')
rep('head.position.copy(pts[0]); S.v.subVectors(pts[0], pts[1]).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); head.rotateX(.75 - gape * .35);',
    'head.position.copy(pts[0]); S.v.subVectors(pts[0], pts[1]).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); if (RG) { /* searching: the head turns to look in over the galaxy, its gaze sweeping slowly */ const look = .5 + .3 * Math.sin(t * .00035), sw = .35 * Math.sin(t * .00021); tmp.set(-pts[0].x, 0, -pts[0].z).normalize(); S.w.subVectors(pts[0], pts[1]).normalize(); tmp2.position.set(-S.w.z, 0, S.w.x); tmp.addScaledVector(tmp2.position, sw).normalize(); tmp.y = -.18 + .1 * Math.sin(t * .0005); S.v.lerp(tmp, look * (1 - TW)).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); } if (RG && TW > .001) { tmp.set(-pts[0].x, 0, -pts[0].z).normalize().multiplyScalar(.55); tmp.y = -1; tmp.normalize(); S.v.lerp(tmp, TW).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); } head.rotateX(RG ? .12 * (1 - TW) - gape * .1 : .75 - gape * .35); head.scale.setScalar(RG ? RG.s * 1.1 / 2.35 : 1); tail.scale.setScalar(RG ? RG.s * .45 / 1.05 : 1); deb.visible = !RG;')
rep('bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG], mouth, lens, open: null }; return out; }',
    'bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG], mouth, lens, open: null, N, ring: null }; return out; }')
# the map: the live world boss is laid round the edge, its head where the boss is
rep('    if (t > M.next && !pdie) { M.next = t + 9000', '    if (key === "lev" && !pdie && M.b.N) { const R0 = Math.hypot(q.x, q.z); M.b.ring = { R0, Rh: R0, a: Math.atan2(q.z, q.x), y: q.y, yh: q.y, k: 1, s: TAU * .93 * R0 / M.b.N * .52 }; g.position.set(0, 0, 0); g.rotation.set(0, 0, 0); g.scale.setScalar(1); } /* v617 */\n    if (t > M.next && !pdie) { M.next = t + 9000')
# the finale set piece: it rises at the wall and swims round it, then its head turns in to the breach
rep('finHand(X, X.b, e, D.set, 6 * sc, WB.lev.sc * 1.6, X.pos); X.b.grp.rotation.y = -a - Math.PI / 2; X.b.tick(t);', 'finHand(X, X.b, e, D.set, 6 * sc, WB.lev.sc * 1.6, X.pos); X.b.grp.rotation.y = -a - Math.PI / 2; if (X.b.N) { const R0 = X.R + 60; X.b.ring = { R0, Rh: r, a, y: 30, yh: y, k: sc, s: TAU * .93 * R0 / X.b.N * .52 }; X.b.grp.position.set(0, 0, 0); X.b.grp.rotation.set(0, 0, 0); X.b.grp.scale.setScalar(1); } /* v617 round the wall */ X.b.tick(t);')
rep('TAU * T / (36 * 3600e3); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 20 + 3 * Math.sin(T / 6e5); return o; } // v569 patrolling just beyond the Rim',
    'TAU * T / (4 * 3600e3); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 20 + 3 * Math.sin(T / 6e5); return o; } // v569 patrolling just beyond the Rim; v617 a lap every 4 hours')
s2 = re.sub(r"GAME_V = 616\b", "GAME_V = 617", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
