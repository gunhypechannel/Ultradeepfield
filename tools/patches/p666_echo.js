  if (/^e_/.test(cls)) { /* v666 a Mimic Echo: the silhouette of one of our ship classes, its plating gone black and veined with neural light,
       cables wound round the hull and trailing from its engines like a corrupted drive plume */
    const base = cls.slice(2), ship = buildShip(base, shipMats("#3fc8ff")); g.add(ship); g.userData.eng = (ship.userData.eng || []).slice();
    ship.traverse(o => { if (!o.isMesh || (o.userData && o.userData.fx)) return; const m = o.material; if (m && !m.isMeshBasicMaterial && !(m.transparent && m.opacity < .9)) o.material = C.ecorr; });
    const b = new TH.Box3().setFromObject(ship), Lx = b.max.x - b.min.x, R = Math.max(b.max.y - b.min.y, b.max.z - b.min.z) * .5, cy = (b.max.y + b.min.y) / 2, cz = (b.max.z + b.min.z) / 2, rr = Math.max(.03, R * .07);
    for (let i = 0; i < 10; i++) { const a0 = r() * TAU, tw = (r() - .5) * 4, pts = [];
      for (let j = 0; j <= 6; j++) { const t = j / 6, x = b.max.x - Lx * (.1 + r() * .15) - t * Lx * .85, a = a0 + tw * t, rad = R * (.75 + r() * .2); pts.push(V(x, cy + Math.cos(a) * rad, cz + Math.sin(a) * rad)); }
      const e = pts[pts.length - 1]; for (let j = 1; j <= 3; j++) pts.push(V(e.x - Lx * .13 * j, e.y + (r() - .5) * R * j * .5, e.z + (r() - .5) * R * j * .7));
      tube(pts, rr, rr * .3, i % 4 === 1 ? C.cableL : C.cable, 0, 1.2); }
    for (let i = 0; i < 6; i++) { const x = b.min.x + Lx * (.2 + r() * .6), z = cz + (r() - .5) * R; tube([V(x, b.min.y + R * .1, z), V(x - Lx * .05, b.min.y - R * .6, z * 1.1), V(x - Lx * .12, b.min.y - R * 1.1, z * 1.2 + (r() - .5) * R)], rr * .8, rr * .2, C.cable, 0, 1.3); }
    for (let i = 0; i < 3; i++) { const p = V(b.min.x + Lx * (.3 + i * .2), cy + R * .55, cz + (r() - .5) * R * .4); orb(R * .16, C.core, p, 12); orb(R * .32, C.glowS, p, 10); }
    return g; }
