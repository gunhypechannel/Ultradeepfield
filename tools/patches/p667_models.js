  if (cls === "mnode" || cls === "mpylon") { /* v667 Omega's Neural Nodes (a caged crystal of neural light) and Assimilation Pylons (a hooked black spire with a burning tip) */
    if (cls === "mnode") { const cp = V(0, .9, 0), c = orb(.75, C.core, cp, 20); c.scale.set(1, 1.9, 1); orb(1.5, C.glowS, cp, 14);
      for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; tube([V(Math.cos(a) * 1.4, -1.3, Math.sin(a) * 1.4), V(Math.cos(a) * 1.15, .9, Math.sin(a) * 1.15), V(Math.cos(a) * .3, 2.8, Math.sin(a) * .3)], .14, .04, i % 2 ? C.cable : C.cableL, 0, 1); }
      for (const [rr, y] of [[1.3, .2], [1.0, 1.7]]) { const t = add(new TH.Mesh(new TH.TorusGeometry(rr, .025, 6, 48), C.holo), 0, y, 0); t.rotation.x = Math.PI / 2; } }
    else { const b = V(0, -1.4, 0), mid = V(.7, 1.2, 0), tip = V(-.1, 3.6, 0); tube([b, V(.4, -.2, 0), mid, V(.3, 2.6, 0), tip], .55, .04, C.shell, 6, .8); bundle([b, mid, tip], 5, .5, { t1: .8, r0: .08, r1: .05 });
      orb(.3, C.glow, tip, 12); orb(.75, C.glowS, tip, 12); const t = add(new TH.Mesh(new TH.TorusGeometry(1.1, .03, 6, 48), C.holo), .5, 1.0, 0); t.rotation.x = Math.PI / 2; }
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + r() * .3, R = 1.8 + r() * 1.2; tube([V(Math.cos(a) * .4, -1.35, Math.sin(a) * .4), V(Math.cos(a) * 1.4, -1.5, Math.sin(a) * 1.4), V(Math.cos(a + .25) * R, -1.6, Math.sin(a + .25) * R)], .16, .05); }
    return g; }
