/* v864 the battle backdrop's world (owner: "some battles dont take place at a planet but the battle simulation still shows a planet for
   every battle ... the planet in the background is so pixelated and uninteresting ... sharper or more eclipsed in the background").
   A world shows only when the fight is at one (raids on a world, attacks on and defences of planets, joint strikes on a planet, the
   Guardians of a ruin world, the Elemental trials, the fortress simulator); deep-space fights (expeditions, pirates, monsters, world
   bosses, the Cube, gathering fields, the labs) get open space. The world is painted per pixel at close to the screen's resolution from
   3D noise on its sphere, so it stays sharp, and it is mostly in eclipse: the sun sits behind it, so only a thin lit crescent and its
   glowing air face the battle, with the night side barely visible (city lights on living worlds, glowing rifts on lava worlds). */
const BP_RE = /^(Attack on |Hive raid on |Cube strike on |The first defence|Guardians of |Elemental Trial)/;
function bpAt(r) { if (!r) return false; if (r.site) return r.site === "planet"; const t = r.title || "";
  return !!(r.pid || BP_RE.test(t) || (r.kind === "defense" && !/battle at /.test(t)) || (/^Joint strike on /.test(t) && r.dUid) || /^Fortress /.test(r.dName || "")); }
const bpH = (x, y, z) => { let h = Math.imul(x, 374761393) + Math.imul(y, 668265263) + Math.imul(z, 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
function bpN(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf);
  const a = bpH(xi, yi, zi), b = bpH(xi + 1, yi, zi), c = bpH(xi, yi + 1, zi), d = bpH(xi + 1, yi + 1, zi), e = bpH(xi, yi, zi + 1), f = bpH(xi + 1, yi, zi + 1), g = bpH(xi, yi + 1, zi + 1), h = bpH(xi + 1, yi + 1, zi + 1);
  const k0 = a + (b - a) * u, k1 = c + (d - c) * u, k2 = e + (f - e) * u, k3 = g + (h - g) * u, m0 = k0 + (k1 - k0) * v, m1 = k2 + (k3 - k2) * v; return m0 + (m1 - m0) * w; }
function bpF(x, y, z, o) { let s = 0, a = .5, f = 1, n = 0; for (let i = 0; i < o; i++) { s += a * bpN(x * f, y * f, z * f); n += a; f *= 2.03; a *= .5; } return s / n; }
const bpRGB = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const bpMix = (A, B, k) => [A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k, A[2] + (B[2] - A[2]) * k];
const bpSS = (a, b, x) => { const u = Math.max(0, Math.min(1, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
const BP_C = []; // the last couple of worlds painted (a battle repaints only when its size changes)
// the surface colour of one point of the world (n: its unit normal, seeded), with its own glow; cheap when only the night side needs it
function bpSurf(type, P, nx, ny, nz, full) { const o = full ? 5 : 3, h = bpF(nx * 3.1 + 11, ny * 3.1 + 3, nz * 3.1 + 7, o); let c, em = 0, emc = null, spec = 0;
  if (type === "gas") { const band = ny * 7 + (bpF(nx * 1.4, ny * 5, nz * 1.4, full ? 4 : 2) - .5) * 3.2, s = .5 + .5 * Math.sin(band); c = bpMix(bpMix(P[2], P[0], s), bpMix(P[1], P[3], s), bpSS(.3, .8, h)); }
  else if (type === "lava") { const r = Math.abs(bpF(nx * 3.2 + 5, ny * 3.2, nz * 3.2, o) - .5); c = bpMix(P[0], P[3], bpSS(.35, .7, h)); if (r < .045) { em = (1 - r / .045) ** 1.6; emc = bpMix(P[1], P[2], em); } }
  else if (type === "ice") { const r = Math.abs(bpF(nx * 4 + 2, ny * 4, nz * 4, full ? 3 : 2) - .5); c = bpMix(bpMix(P[2], P[0], bpSS(.3, .6, h)), P[1], bpSS(.55, .8, h)); if (r < .02) c = bpMix(c, P[2], .6); }
  else if (type === "desert") { const dn = .5 + .5 * Math.sin((nx * 9 + ny * 14 + h * 9)); c = bpMix(bpMix(P[2], P[0], bpSS(.3, .55, h)), bpMix(P[1], P[3], dn * .5), bpSS(.5, .8, h)); }
  else if (type === "toxic") { c = bpMix(bpMix(P[2], P[0], bpSS(.3, .6, h)), P[1], bpSS(.6, .85, h)); if (full) c = bpMix(c, P[3], bpSS(.6, .9, bpF(nx * 3 + 9, ny * 3, nz * 3, 3)) * .35); }
  else { const sea = type === "ocean" ? .64 : .52, land = h > sea; // terran / ocean
    if (land) { c = bpMix(P[1], P[2], bpSS(.5, .75, bpF(nx * 5 + 1, ny * 5, nz * 5, full ? 3 : 1))); if (bpN(nx * 70, ny * 70, nz * 70) > .8 && type === "terran") { em = .55; emc = [255, 196, 128]; } }
    else { c = bpMix(bpMix(P[0], [8, 20, 44], .45), P[0], bpSS(sea - .2, sea, h)); spec = 1; }
    if (ny * .92 + nx * .3 > .86) c = bpMix(c, P[3], bpSS(.86, .93, ny * .92 + nx * .3)); }
  if (full && (type === "terran" || type === "ocean" || type === "toxic" || type === "gas")) { const cl = bpSS(.56, .74, bpF(nx * 4.4 + 21, ny * 6 + 5, nz * 4.4 + 2, 4)) * (type === "gas" ? .25 : type === "toxic" ? .35 : .75); c = bpMix(c, type === "toxic" ? P[3] : [240, 246, 250], cl); spec *= 1 - cl; }
  return [c, em, emc, spec]; }
function bpPaint(x, r, W, H, pcx, pcy, pr) { const type = PAL[r.ptype] ? r.ptype : "terran", seed = hash(String(r.dName || type)) % 97, key = `${type}|${seed}|${W}|${H}`;
  let hit = BP_C.find(e => e.k === key);
  if (!hit) { const A = 1.075, x0 = Math.max(0, Math.floor(pcx - pr * A)), x1 = Math.min(W, Math.ceil(pcx + pr * A)), y0 = Math.max(0, Math.floor(pcy - pr * A)), y1 = Math.min(H, Math.ceil(pcy + pr * A)); if (x1 <= x0 || y1 <= y0) return;
    const bw = x1 - x0, bh = y1 - y0, k = Math.min(1, Math.sqrt((MOBILE ? 240000 : 360000) / (bw * bh))), cw = Math.max(1, Math.round(bw * k)), ch = Math.max(1, Math.round(bh * k));
    const cv = document.createElement("canvas"); cv.width = cw; cv.height = ch; const cx = cv.getContext("2d"), im = cx.createImageData(cw, ch), D = im.data, P = PAL[type].slice(0, 4).map(bpRGB), AT = bpRGB(PAL[type][4]);
    const Lx = -.42, Ly = -.36, Lz = -.83, ll = Math.hypot(Lx, Ly, Lz), lx = Lx / ll, ly = Ly / ll, lz = Lz / ll, l2 = Math.hypot(lx, ly), sx = seed * 1.7, sz = seed * .9;
    const ca = Math.cos(.35), sa = Math.sin(.35); // a tilt of its axis
    for (let j = 0; j < ch; j++) { const py = y0 + (j + .5) / k, dy = (py - pcy) / pr;
      for (let i = 0; i < cw; i++) { const px = x0 + (i + .5) / k, dx = (px - pcx) / pr, r2 = dx * dx + dy * dy, o = (j * cw + i) * 4; if (r2 > A * A) continue;
        const rr = Math.sqrt(r2), facing = rr > 1e-6 ? (dx * lx + dy * ly) / (rr * l2) : 0; // how far round this point of the limb faces the sun
        if (rr > 1) { // its air beyond the limb, glowing where the sun shines through it
          const f = Math.exp(-(rr - 1) * 38) * Math.max(0, facing) ** 2.2 * .95 + Math.exp(-(rr - 1) * 70) * .08; if (f < .004) continue;
          D[o] = AT[0]; D[o + 1] = AT[1]; D[o + 2] = AT[2]; D[o + 3] = Math.min(255, f * 255); continue; }
        const nz = Math.sqrt(1 - r2), lam = dx * lx + dy * ly + nz * lz, lit = bpSS(-.02, .22, lam), full = lit > .002;
        const tx = dx * ca - dy * sa, ty = dx * sa + dy * ca, [c, em, emc, spec] = bpSurf(type, P, tx + sx, ty, nz + sz, full);
        const night = .045 + .03 * Math.max(0, facing), sh = night + (1.15 - night) * lit; let R = c[0] * sh, Gc = c[1] * sh, B = c[2] * sh;
        const rim = (1 - nz) ** 2.6 * (.25 + .75 * Math.max(0, facing)) * (.2 + .8 * bpSS(-.25, .15, lam)); R += AT[0] * rim * .9; Gc += AT[1] * rim * .9; B += AT[2] * rim * .9; // its air seen edge-on
        if (spec && lit > .05) { const hz = lz + 1, hl = Math.hypot(lx, ly, hz), sp = Math.max(0, (dx * lx + dy * ly + nz * hz) / hl) ** 60 * lit * .8; R += 255 * sp; Gc += 236 * sp; B += 210 * sp; }
        if (em) { const e2 = em * (1 - lit * .85) * (type === "lava" ? 1 : .5); R += emc[0] * e2; Gc += emc[1] * e2; B += emc[2] * e2; }
        const edge = Math.min(1, (1 - rr) * pr * k * 1.2 + .001); // a crisp, anti-aliased limb
        D[o] = Math.min(255, R); D[o + 1] = Math.min(255, Gc); D[o + 2] = Math.min(255, B); D[o + 3] = 255 * Math.min(1, edge * 1.5 + 0); } }
    cx.putImageData(im, 0, 0); hit = { k: key, cv, x0, y0, bw, bh }; BP_C.unshift(hit); BP_C.length = Math.min(BP_C.length, 2); }
  x.save(); x.imageSmoothingEnabled = true; try { x.imageSmoothingQuality = "high"; } catch (e) {} x.drawImage(hit.cv, hit.x0, hit.y0, hit.bw, hit.bh); x.restore(); }
// open space where the fight has no world: a far nebula and a faint dust lane where the world used to sit, so the frame stays balanced
function bpSpace(x, W, H) { const g = x.createRadialGradient(W * .9, H * .92, 0, W * .9, H * .92, W * .7); g.addColorStop(0, "rgba(80,60,150,.2)"); g.addColorStop(.5, "rgba(40,50,120,.08)"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(0, 0, W, H);
  const r = rnd(77); x.save(); x.globalCompositeOperation = "lighter"; for (let i = 0; i < 60; i++) { const u = r(), px = W * (.35 + u * .75), py = H * (1.05 - u * .55) + (r() - .5) * H * .12, s = W * (.03 + r() * .08), gg = x.createRadialGradient(px, py, 0, px, py, s); gg.addColorStop(0, `rgba(120,110,190,${.025 + r() * .03})`); gg.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = gg; x.fillRect(px - s, py - s, s * 2, s * 2); } x.restore(); }
