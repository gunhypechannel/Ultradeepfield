function dvPlan(s0) { if (G.dvP && G.dvP.s0 === s0) return G.dvP;
  /* v441 two forms. The PUZZLE: twelve blocks the size of the Super Cube (2x2x2 cells of 15), staggered round it, and a crown of four.
     The OMEGA CUBE: 5x5x5 cells of 30 round the Super Cube (two inside, 98 in the shell). Every cube first locks into the puzzle; then the
     puzzle bursts apart, every piece grows to the Super Cube's size, and each flies to the slot of the giant cube on its own side. */
  const face = (cells, occ) => { for (const s of cells) { let best = null, bv = -1e9; for (const [ax, sg] of [[0, 1], [0, -1], [1, 1], [1, -1], [2, 1], [2, -1]]) { const n = s.c.slice(); n[ax] += sg; if (occ.has(n.join())) continue; const v = s.p[ax] * sg; if (v > bv) { bv = v; best = [ax, sg]; } } s.n = [0, 0, 0]; s.n[best[0]] = best[1]; } };
  const P1 = [], c1 = c => P1.push({ c, p: [(c[0] + .5) * DV_CELLP, (c[1] + .5) * DV_CELLP, (c[2] + .5) * DV_CELLP] });
  DV_MODS.forEach(m => { const L = []; for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) for (let c = 0; c < 2; c++) L.push([m[0] + a, m[1] + b, m[2] + c]); L.sort((u, v) => Math.hypot(u[0] + .5, u[1] + .5, u[2] + .5) - Math.hypot(v[0] + .5, v[1] + .5, v[2] + .5)); L.forEach(c1); });
  DV_CROWN.forEach(c1); { const occ = new Set(P1.map(s => s.c.join())); for (let x = -1; x <= 0; x++) for (let y = -1; y <= 0; y++) for (let z = -1; z <= 0; z++) occ.add([x, y, z].join()); face(P1, occ); }
  const P2 = [], c2 = c => P2.push({ c, p: [c[0] * DV_CELL, c[1] * DV_CELL, c[2] * DV_CELL] }); c2([0, -1, 0]); c2([0, 1, 0]);
  { const sh = []; for (let x = -2; x <= 2; x++) for (let y = -2; y <= 2; y++) for (let z = -2; z <= 2; z++) if (Math.max(Math.abs(x), Math.abs(y), Math.abs(z)) === 2) sh.push([x, y, z]);
    sh.sort((u, v) => u[1] - v[1] || Math.atan2(u[2], u[0]) - Math.atan2(v[2], v[0]) || Math.hypot(u[0], u[2]) - Math.hypot(v[0], v[2])); sh.forEach(c2); const occ = new Set(P2.map(s => s.c.join())); occ.add("0,0,0"); face(P2, occ); }
  const cubes = PIRATES.filter(x => x.boss).sort((a, b) => (+a.id.slice(1)) - (+b.id.slice(1))), N = Math.min(cubes.length, P1.length, P2.length), Tm = s0 + DV.lock0, Q = {};
  const az = x => { const q = P3(x, Tm, Q); return Math.atan2(q.z, q.x); };
  const cs = cubes.slice(0, N).map(x => ({ x, a: az(x) })).sort((u, v) => u.a - v.a), sl = P1.slice(0, N).map((s, i) => ({ s, i, a: Math.atan2(s.p[2], s.p[0]) })).sort((u, v) => u.a - v.a);
  let rot = 0, bestE = 1e9; for (let k = 0; k < N; k++) { let E = 0; for (let j = 0; j < N; j++) { const d = Math.abs(cs[j].a - sl[(j + k) % N].a) % TAU; E += Math.min(d, TAU - d); } if (E < bestE) { bestE = E; rot = k; } } /* cubes take the puzzle slots on their own side of the Void */
  const L = []; cs.forEach((c, j) => { const s = sl[(j + rot) % N].s, i = sl[(j + rot) % N].i, r = rnd(hash(c.x.id + ":" + s0)), lk = DV.lock0 + i * (DV.lock1 - DV.lock0) / N, arr = Math.max(70 * DV_M, lk - 20 * DV_M) - r() * 4 * DV_M;
    const hd = Math.hypot(s.p[0], s.p[1] * .6, s.p[2]) || 1, H = [s.p[0] / hd * DV_HOLD + (r() - .5) * 30, s.p[1] / hd * DV_HOLD * .45 + (r() - .5) * 40, s.p[2] / hd * DV_HOLD + (r() - .5) * 30];
    const q = P3(c.x, s0 + arr - 25 * DV_M, Q), dist = Math.hypot(q.x - H[0], q.y - DV_Y - H[1], q.z - H[2]), trav = (15 + 20 * Math.min(1, dist / 520)) * DV_M;
    L.push({ x: c.x, s, i, lk, arr, dep: arr - trav, trav, H, sz: MK_K * (3.2 + c.x.lvl * .06), sp: .4 + r() * .6, lift: 60 + r() * 40 }); });
  /* the giant cube's slots, bottom face first: each goes to the piece whose puzzle slot points most nearly the same way */
  const free = new Set(L), un = p => { const l = Math.hypot(...p) || 1; return p.map(v => v / l); };
  P2.slice(0, N).forEach((s2, i2) => { const d2 = un(s2.p); let best = null, bv = -1e9; for (const c of free) { const d1 = un(c.s.p), v = d1[0] * d2[0] + d1[1] * d2[1] * 1.3 + d1[2] * d2[2]; if (v > bv) { bv = v; best = c; } }
    free.delete(best); best.s2 = s2; best.i2 = i2; best.lk2 = DV.rb0 + i2 * (DV.rb1 - DV.rb0) / N; const l = Math.hypot(...best.s.p) || 1; best.E = best.s.p.map(v => v / l * (l + 95)); best.ret = DV.ret + (N - 1 - i2) * 12 * DV_M / N; });
  L.sort((a, b) => a.i - b.i); return (G.dvP = { s0, L, cells: P1, cells2: P2, N }); }
function dvCube(c, e, D, o) { const s0 = D.s0, sz = c.sz, f1 = DV_CELLP * .975, f2 = DV_CELL * .975, rotY = e > DV.combat ? (Math.min(e, DV.ret) - DV.combat) * TAU / (40 * DV_M) : 0, cy = Math.cos(rotY), sy = Math.sin(rotY);
  const slotW = (p, out) => { out.x = p[0] * cy + p[2] * sy; out.y = DV_Y + p[1]; out.z = -p[0] * sy + p[2] * cy; return out; }, P = o.P || (o.P = [{}, {}, {}, {}]), at = (p, out) => { out.x = p[0]; out.y = DV_Y + p[1]; out.z = p[2]; return out; };
  o.rot = rotY; o.lkT = 0;
  if (e < c.dep) { P3(c.x, s0 + e, o); o.k = sz; o.al = 0; o.st = "home"; return o; }
  if (e < c.arr) { const u = (e - c.dep) / c.trav, h = P3(c.x, s0 + c.dep, P[0]); P[1].x = h.x; P[1].y = h.y + c.lift; P[1].z = h.z;
    const hl = Math.hypot(c.H[0], c.H[2]) || 1; P[3].x = c.H[0]; P[3].y = DV_Y + c.H[1]; P[3].z = c.H[2]; P[2].x = P[3].x + c.H[0] / hl * 140; P[2].y = P[3].y + 50; P[2].z = P[3].z + c.H[2] / hl * 140;
    const w = u < .1 ? dvIn(u / .1) * .02 : .02 + .98 * dvEase((u - .1) / .9); dvBez(P[0], P[1], P[2], P[3], w, o); o.k = sz; o.al = 0; o.st = u < .1 ? "detach" : "fly"; o.u = u; return o; }
  if (e < c.lk - DV_LOCK) { o.x = c.H[0]; o.y = DV_Y + c.H[1] + Math.sin(e / 9000 + c.i) * 1.5; o.z = c.H[2]; o.k = sz; o.al = 0; o.st = "hold"; return o; }
  const S1 = at(c.s.p, P[0]);
  if (e < c.lk) { const k = (e - (c.lk - DV_LOCK)) / DV_LOCK, st = at([c.s.p[0] + c.s.n[0] * 40, c.s.p[1] + c.s.n[1] * 40, c.s.p[2] + c.s.n[2] * 40], P[1]);
    if (k < .55) { const u = dvEase(k / .55); o.x = c.H[0] + (st.x - c.H[0]) * u; o.y = DV_Y + c.H[1] + (st.y - DV_Y - c.H[1]) * u; o.z = c.H[2] + (st.z - c.H[2]) * u; o.st = "align"; }
    else { const u = 1 - Math.pow(1 - (k - .55) / .45, 3); o.x = st.x + (S1.x - st.x) * u; o.y = st.y + (S1.y - st.y) * u; o.z = st.z + (S1.z - st.z) * u; o.st = "slide"; }
    o.k = sz + (f1 - sz) * dvEase(k / .5); o.al = dvEase(k / .45); return o; }
  if (e < DV.ex0) { o.x = S1.x; o.y = S1.y; o.z = S1.z; o.k = f1; o.al = 1; o.st = "locked"; o.lkT = c.lk; return o; }
  /* the reconfiguration: the puzzle bursts apart and every piece grows, then flies to its slot in the giant cube and slides home */
  const st2 = at([c.s2.p[0] + c.s2.n[0] * 75, c.s2.p[1] + c.s2.n[1] * 75, c.s2.p[2] + c.s2.n[2] * 75], P[1]), E = at(c.E, P[2]);
  if (e < DV.ex1) { const u = dvEase((e - DV.ex0) / (DV.ex1 - DV.ex0)); o.x = S1.x + (E.x - S1.x) * u; o.y = S1.y + (E.y - S1.y) * u; o.z = S1.z + (E.z - S1.z) * u; o.k = f1 + (f2 - f1) * u; o.al = 1; o.st = "shift"; return o; }
  if (e < c.lk2 - DV_LOCK2) { const u = dvEase((e - DV.ex1) / Math.max(1, c.lk2 - DV_LOCK2 - DV.ex1)); o.x = E.x + (st2.x - E.x) * u; o.y = E.y + (st2.y - E.y) * u + Math.sin(u * Math.PI) * 30; o.z = E.z + (st2.z - E.z) * u; o.k = f2; o.al = 1; o.st = "shift"; return o; }
  const S2 = slotW(c.s2.p, P[3]);
  if (e < c.lk2) { const u = 1 - Math.pow(1 - (e - (c.lk2 - DV_LOCK2)) / DV_LOCK2, 3); o.x = st2.x + (S2.x - st2.x) * u; o.y = st2.y + (S2.y - st2.y) * u; o.z = st2.z + (S2.z - st2.z) * u; o.k = f2; o.al = 1; o.st = "slide"; return o; }
  if (e < c.ret) { o.x = S2.x; o.y = S2.y; o.z = S2.z; o.k = f2; o.al = 1; o.st = "locked"; o.lkT = c.lk2; return o; }
  /* coming apart: slide out along its face, shrink, and fly home */
  const k = (e - c.ret) / (30 * DV_M), so = slotW([c.s2.p[0] + c.s2.n[0] * 110, c.s2.p[1] + c.s2.n[1] * 110, c.s2.p[2] + c.s2.n[2] * 110], P[1]);
  if (k < .08) { const u = dvEase(k / .08); o.x = S2.x + (so.x - S2.x) * u; o.y = S2.y + (so.y - S2.y) * u; o.z = S2.z + (so.z - S2.z) * u; o.k = f2 + (sz - f2) * u; o.al = 1 - u; o.st = "unlock"; return o; }
  const u = dvEase(Math.min(1, (k - .08) / .92)), h = P3(c.x, s0 + Math.min(e, c.ret + 30 * DV_M), P[2]); P[0].x = so.x; P[0].y = so.y + 60; P[0].z = so.z;
  dvBez(so, P[0], { x: h.x, y: h.y + 80, z: h.z }, h, u, o); o.k = sz; o.al = 0; o.st = k >= 1 ? "home" : "fly"; o.u = u; return o; }
