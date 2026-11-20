# v674 map fleets clean and proportional (see p674_fleets.js)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('function fleet3D(W, n, col, hostile, big, cube, flag, look) {', R('p674_fleets.js') + 'function fleet3D(W, n, col, hostile, big, cube, flag, look) { const arm = typeof big === "string" ? FLEET_ARM : !!big; /* v674 */')
rep('for (const [k, v] of comp) { const cap = { s: 4, m: 3, l: 2, x: 1, q: 1 }[MINI_CLS[k]] * (big ? 3 : 1); for (let i = 0; i < clamp(Math.ceil(Math.log2(v + 1)) * (big ? 2 : 1), 1, cap) && ships.length < (big ? (MOBILE ? 12 : 18) : MOBILE ? 6 : 9) + (flag ? 1 : 0); i++) ships.push(k); }',
    'for (const [k, v] of comp) { const cap = { s: 4, m: 3, l: 2, x: 1, q: 1 }[MINI_CLS[k]] * (arm ? 3 : 1); for (let i = 0; i < clamp(Math.ceil(Math.log2(v + 1)) * (arm ? 2 : 1), 1, cap) && ships.length < (arm ? (MOBILE ? 12 : 18) : MOBILE ? 6 : 9) + (flag ? 1 : 0); i++) ships.push(k); }')
rep('''const order = { q: 0, x: 0, l: 1, m: 2, s: 3 }; comp.sort((a, b) => order[MINI_CLS[a[0]]] - order[MINI_CLS[b[0]]] || b[1] - a[1]);
  const ships = flag ? ["flagship"] : [];''', '''const order = { q: 9 /* v674 the Cube Destroyer holds the rear */, x: 0, l: 1, m: 2, s: 3 }; comp.sort((a, b) => order[MINI_CLS[a[0]]] - order[MINI_CLS[b[0]]] || b[1] - a[1]);
  const ships = flag ? ["flagship"] : [];''')
rep('Object.assign(grp.userData, { groups, orphan: 0, sp, flagship: flag, R:', 'Object.assign(grp.userData, { span: 2 * Math.max(...slots.map(s => Math.hypot(s.x, s.z))) + Math.max(...geos.map((g, i) => g.len * (ships[i] === "flagship" ? FLAG_K : 1))), groups, orphan: 0, sp, flagship: flag, R:')
rep('FLEET_FIN = f.demo || f.raid || f.mission === "spy" ? null : hullFleet(fleetFlagU(f, hostile), f.n);', 'FLEET_ARM = !!(f.js && f.jsK !== "in"); FLEET_FIN = f.demo || f.raid || f.mission === "spy" ? null : hullFleet(fleetFlagU(f, hostile), f.n);')
rep('FLEET_FIN = null; const tot = Object.values(f.n || {}).reduce((a, b) => a + b, 0) || 6;', 'FLEET_FIN = null; FLEET_ARM = false; const tot = Object.values(f.n || {}).reduce((a, b) => a + b, 0) || 6;')
rep('grp.userData.size = (.75 + Math.min(1.1, Math.log10(tot + 1) * .3)) * .5; // grows with fleet size', 'grp.userData.size = fleetSzOf(f.n || (hostile ? { destroyer: 2, corvette: 4 } : { fighter: 6 }), grp); /* v674 sized against a planet by strength (was a log of the ship count) */')
rep('if (f.js && f.jsK !== "in") grp.userData.size *= 1.15 + Math.min(.5, (f.cnt || 1) * .05);', 'if (f.js && f.jsK !== "in") grp.userData.size = fleetSzOf(f.n, grp, 1.15 + Math.min(.5, (f.cnt || 1) * .05));')
rep('g.userData.size = (.75 + Math.min(1.1, Math.log10(clashCnt(n) + 1) * .3)) * .5;', 'g.userData.size = fleetSzOf(sn || genComp(clashCnt(n)), g); /* v674 */')
rep('if (W.fmFr !== W.fr) { W.fmFr = W.fr; W.fleetMade = 0; }', 'if (W.fmFr !== W.fr) { W.fmFr = W.fr; W.fleetMade = 0; } W.lanes = fleetLanes(list); /* v674 */')
rep('else { pt = ARC(path.a, path.b, path.k); nx = ARC(path.a, path.b, Math.min(1, path.k + .01)); if (path.k >= 1) nx = { x: pt.x + (path.b.x - path.a.x) * .01, y: pt.y, z: pt.z + (path.b.z - path.a.z) * .01 };',
    '''else { pt = ARC(path.a, path.b, path.k); nx = ARC(path.a, path.b, Math.min(1, path.k + .01)); if (path.k >= 1) nx = { x: pt.x + (path.b.x - path.a.x) * .01, y: pt.y, z: pt.z + (path.b.z - path.a.z) * .01 };
      { const ln = W.lanes && W.lanes.get(id); if (ln) { const dx = path.b.x - path.a.x, dz = path.b.z - path.a.z, L = Math.hypot(dx, dz) || 1, w = clamp(path.k * 1.4, 0, 1), gap = (o.grp.userData.span || 20) * fsF * (o.grp.userData.size || 1) * 1.15, off = (ln[0] - (ln[1] - 1) / 2) * gap * w; pt.x += -dz / L * off; pt.z += dx / L * off; nx.x += -dz / L * off; nx.z += dx / L * off; } } /* v674 lanes into a shared target */''')
rep('ws = fsF * (o.grp.userData.size || 1) * (.25 + .75 * wk);', 'ws0 = fsF * (o.grp.userData.size || 1) * (.25 + .75 * wk), pxC = (o.grp.userData.span || 20) * ws0 * (pxS / W.renderer.getPixelRatio()) / Math.max(1, W.camera.position.distanceTo(o.grp.position)), ws = ws0 * (wk > .9 && pxC < 30 ? 30 / pxC : 1) /* v674 never under 30 px */;')
rep('const GAME_V = 673;', 'const GAME_V = 674;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
