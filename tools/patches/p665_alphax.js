    if (D.alpha) { /* an Alpha: a crown of great hooked spines swept back from the skull, and its neural core laid open along its back */
      for (let i = 0; i < 7; i++) { const a = (i - 3) * .32; cone(1.6 + (3 - Math.abs(i - 3)) * .45, .16, C.shell, V(1.55 * L, 1.35, a * .55), V(-1, 1.1 - Math.abs(a) * .3, a * 1.4), .35); }
      const cp = V(-.3 * L, 1.5 + D.hump, 0), co = orb(.55, C.core, cp, 24); co.scale.set(1.6, .8, 1); orb(1.0, C.glowS, cp, 14);
      for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; tube([cp.clone().add(V(Math.cos(a) * .95, -.15, Math.sin(a) * .55)), cp.clone().add(V(Math.cos(a) * .55, .45, Math.sin(a) * .32)), cp.clone().add(V(Math.cos(a) * .12, .6, Math.sin(a) * .06))], .1, .035, C.cableL); } }
