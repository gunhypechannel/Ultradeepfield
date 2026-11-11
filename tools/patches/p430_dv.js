/* v430 CUBE DEVASTATION (owner: monthly on the 11th, 11am Phoenix = 18:00 UTC, first on 11 Dec 2026). Every Assimilation Cube in the
   galaxy wakes, leaves its post and flies to the Void, where they lock together round the Super Cube into the OMEGA CUBE.
   Everything is worked out from the shared clock (like the Convergence): every player sees the same cube in the same place at the
   same moment, and a late joiner simply computes where things are now. Nothing is sent per cube.
   Timeline (event time e, ms since 18:00 UTC): awakening 0-30 min; migration from 30 min (departures staggered so the cubes arrive
   in waves); each cube holds at its station round the Void, then is drawn in and locks into its slot, one every ~36 s from 90 min;
   the last lock at ~150 min; activation 150-156 min (silence, the lights die, the core erupts); then the Omega Cube stands for the
   rest of the day (combat, v431+) and from 24 h it comes apart and every cube flies home (done at 25 h).
   The form: the Super Cube is the core (2x2x2 cells of 15 units); twelve blocks the size of the Super Cube, each built from eight
   Assimilation Cubes, interlock round it, staggered by half a block, after the reference; the last four cubes crown it. Checked: no
   two pieces overlap, every block shares a face with the core or an earlier block. */
const DV_M = 60e3, DV_H = 3600e3, DV_FIRST = Date.UTC(2026, 11, 11, 18), DV_CELL = 15, DV_Y = 150, DV_HOLD = 200, DV_LOCK = 90e3;
const DV = { mig: 30 * DV_M, lock0: 90 * DV_M, lock1: 148 * DV_M, act: 150 * DV_M, erupt: 153 * DV_M, combat: 156 * DV_M, ret: 24 * DV_H, end: 25 * DV_H };
const DV_MODS = [[1, 0, -1], [-3, -2, -1], [-1, 1, 0], [-1, -3, -2], [0, -1, 1], [-2, -1, -3], [1, 2, 0], [-3, 1, -2], [1, -3, -1], [-3, 0, 1], [2, -2, 1], [0, 1, -3]];
const DV_CROWN = [[1, 4, 0], [2, 4, 1], [1, -4, -1], [-4, -2, -1]];
function dvStartOf(T) { const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 11, 18); if (T < s) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, 11, 18); return s; }
const dvPhase = e => e < DV.mig ? "awake" : e < DV.lock0 ? "mig" : e < DV.act ? "asm" : e < DV.combat ? "act" : e < DV.ret ? "combat" : "ret";
/* where the event stands at T (null outside it). The owner's preview runs the whole thing in about four minutes (dvSimStart). */
function dvNow(T) { if (G.dvSim) return dvSimNow(); if (T < DV_FIRST) return null; const s0 = dvStartOf(T), e = T - s0; return e >= 0 && e < DV.end ? { e, s0, ph: dvPhase(e) } : null; }
const DV_SIM = [[0, 0], [15, DV.mig], [165, DV.act], [190, DV.combat], [205, DV.combat + 3 * DV_H], [207, DV.ret], [240, DV.end]]; /* preview seconds -> event time */
function dvSimNow() { const C = G.dvSim, s = (performance.now() - C.t0) / 1000; if (s >= DV_SIM[DV_SIM.length - 1][0]) { dvSimStop(1); return null; }
  let i = 0; while (i < DV_SIM.length - 2 && s >= DV_SIM[i + 1][0]) i++; const [a, ea] = DV_SIM[i], [b, eb] = DV_SIM[i + 1], e = ea + (eb - ea) * (s - a) / (b - a); return { e, s0: C.s0, ph: dvPhase(e), sim: 1 }; }
/* the plan for one event: which cube takes which slot, when it leaves, arrives, holds and locks. Fixed for the event (it depends only on
   its start time), so it is the same on every device. */
function dvPlan(s0) { if (G.dvP && G.dvP.s0 === s0) return G.dvP;
  const cells = [], cell = (c, m) => cells.push({ c, m, p: [(c[0] + .5) * DV_CELL, (c[1] + .5) * DV_CELL, (c[2] + .5) * DV_CELL] });
  DV_MODS.forEach((m, i) => { const L = []; for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) for (let c = 0; c < 2; c++) L.push([m[0] + a, m[1] + b, m[2] + c]); L.sort((u, v) => Math.hypot(u[0] + .5, u[1] + .5, u[2] + .5) - Math.hypot(v[0] + .5, v[1] + .5, v[2] + .5)); L.forEach(c => cell(c, i)); });
  DV_CROWN.forEach(c => cell(c, 12));
  const occ = new Set(cells.map(s => s.c.join())); for (let x = -1; x <= 0; x++) for (let y = -1; y <= 0; y++) for (let z = -1; z <= 0; z++) occ.add([x, y, z].join());
  for (const s of cells) { /* the face it is drawn in through: the open side most in line with the slot's own direction */ let best = null, bv = -1e9;
    for (const [ax, sg] of [[0, 1], [0, -1], [1, 1], [1, -1], [2, 1], [2, -1]]) { const n = s.c.slice(); n[ax] += sg; if (occ.has(n.join())) continue; const v = s.p[ax] * sg; if (v > bv) { bv = v; best = [ax, sg]; } }
    s.n = [0, 0, 0]; s.n[best[0]] = best[1]; }
  const cubes = PIRATES.filter(x => x.boss).sort((a, b) => (+a.id.slice(1)) - (+b.id.slice(1))), N = Math.min(cubes.length, cells.length), Tm = s0 + DV.lock0, P = {};
  const az = x => { const q = P3(x, Tm, P); return Math.atan2(q.z, q.x); };
  const cs = cubes.slice(0, N).map(x => ({ x, a: az(x) })).sort((u, v) => u.a - v.a), sl = cells.slice(0, N).map((s, i) => ({ s, i, a: Math.atan2(s.p[2], s.p[0]) })).sort((u, v) => u.a - v.a);
  let rot = 0, bestE = 1e9; for (let k = 0; k < N; k++) { let E = 0; for (let j = 0; j < N; j++) { const d = Math.abs(cs[j].a - sl[(j + k) % N].a) % TAU; E += Math.min(d, TAU - d); } if (E < bestE) { bestE = E; rot = k; } } /* cubes take the slots on their own side of the Void */
  const L = []; cs.forEach((c, j) => { const s = sl[(j + rot) % N].s, i = sl[(j + rot) % N].i, r = rnd(hash(c.x.id + ":" + s0)), lk = DV.lock0 + i * (DV.lock1 - DV.lock0) / N, arr = Math.max(70 * DV_M, lk - 20 * DV_M) - r() * 4 * DV_M;
    const hd = Math.hypot(s.p[0], s.p[1] * .6, s.p[2]) || 1, H = [s.p[0] / hd * DV_HOLD + (r() - .5) * 30, s.p[1] / hd * DV_HOLD * .45 + (r() - .5) * 40, s.p[2] / hd * DV_HOLD + (r() - .5) * 30];
    const q = P3(c.x, s0 + arr - 25 * DV_M, P), dist = Math.hypot(q.x - H[0], q.y - DV_Y - H[1], q.z - H[2]), trav = (15 + 20 * Math.min(1, dist / 520)) * DV_M;
    L.push({ x: c.x, s, i, lk, arr, dep: arr - trav, trav, H, sz: MK_K * (3.2 + c.x.lvl * .06), ax: [r() - .5, r() - .5, r() - .5], sp: .4 + r() * .6, lift: 60 + r() * 40, ret: DV.ret + (N - 1 - i) * 12 * DV_M / N, home: null }); });
  L.sort((a, b) => a.i - b.i); return (G.dvP = { s0, L, cells, N }); }
const dvEase = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u), dvIn = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * u;
function dvBez(a, b, c, d, u, o) { const v = 1 - u, A = v * v * v, B = 3 * v * v * u, C = 3 * v * u * u, D = u * u * u; o.x = A * a.x + B * b.x + C * c.x + D * d.x; o.y = A * a.y + B * b.y + C * c.y + D * d.y; o.z = A * a.z + B * b.z + C * c.z + D * d.z; return o; }
/* one cube at event time e: world position, scale, how aligned it is (0 = its own tumble, 1 = square to the Omega), and its state */
function dvCube(c, e, D, o) { const s0 = D.s0, sz = c.sz, full = DV_CELL * .975, rotY = e > DV.combat ? (Math.min(e, DV.ret) - DV.combat) * TAU / (40 * DV_M) : 0, cy = Math.cos(rotY), sy = Math.sin(rotY);
  const slotW = (p, out) => { out.x = p[0] * cy + p[2] * sy; out.y = DV_Y + p[1]; out.z = -p[0] * sy + p[2] * cy; return out; }, P = o.P || (o.P = [{}, {}, {}, {}]);
  o.rot = rotY;
  if (e < c.dep) { P3(c.x, s0 + e, o); o.k = sz; o.al = 0; o.st = "home"; return o; }
  if (e < c.arr) { const u = (e - c.dep) / c.trav, h = P3(c.x, s0 + c.dep, P[0]); P[1].x = h.x; P[1].y = h.y + c.lift; P[1].z = h.z;
    const hl = Math.hypot(c.H[0], c.H[2]) || 1; P[3].x = c.H[0]; P[3].y = DV_Y + c.H[1]; P[3].z = c.H[2]; P[2].x = P[3].x + c.H[0] / hl * 140; P[2].y = P[3].y + 50; P[2].z = P[3].z + c.H[2] / hl * 140;
    const w = u < .1 ? dvIn(u / .1) * .02 : .02 + .98 * dvEase((u - .1) / .9); dvBez(P[0], P[1], P[2], P[3], w, o); o.k = sz; o.al = 0; o.st = u < .1 ? "detach" : "fly"; o.u = u; return o; }
  if (e < c.lk - DV_LOCK) { o.x = c.H[0]; o.y = DV_Y + c.H[1] + Math.sin(e / 9000 + c.i) * 1.5; o.z = c.H[2]; o.k = sz; o.al = 0; o.st = "hold"; return o; }
  const S = slotW(c.s.p, P[0]);
  if (e < c.lk) { const k = (e - (c.lk - DV_LOCK)) / DV_LOCK, st = P[1]; st.x = c.s.p[0] + c.s.n[0] * 40; st.y = c.s.p[1] + c.s.n[1] * 40; st.z = c.s.p[2] + c.s.n[2] * 40; slotW([st.x, st.y, st.z], st);
    if (k < .55) { const u = dvEase(k / .55); o.x = c.H[0] + (st.x - c.H[0]) * u; o.y = DV_Y + c.H[1] + (st.y - DV_Y - c.H[1]) * u; o.z = c.H[2] + (st.z - c.H[2]) * u; o.st = "align"; }
    else { const u = 1 - Math.pow(1 - (k - .55) / .45, 3); o.x = st.x + (S.x - st.x) * u; o.y = st.y + (S.y - st.y) * u; o.z = st.z + (S.z - st.z) * u; o.st = "slide"; }
    o.k = sz + (full - sz) * dvEase(k / .5); o.al = dvEase(k / .45); return o; }
  if (e < c.ret) { o.x = S.x; o.y = S.y; o.z = S.z; o.k = full; o.al = 1; o.st = "locked"; return o; }
  /* coming apart: slide out along its face, shrink, and fly home */
  const k = (e - c.ret) / (30 * DV_M), st = P[1]; st.x = c.s.p[0] + c.s.n[0] * 60; st.y = c.s.p[1] + c.s.n[1] * 60; st.z = c.s.p[2] + c.s.n[2] * 60; slotW([st.x, st.y, st.z], st);
  if (k < .08) { const u = dvEase(k / .08); o.x = S.x + (st.x - S.x) * u; o.y = S.y + (st.y - S.y) * u; o.z = S.z + (st.z - S.z) * u; o.k = full + (sz - full) * u; o.al = 1 - u; o.st = "unlock"; return o; }
  const u = dvEase(Math.min(1, (k - .08) / .92)), h = P3(c.x, s0 + Math.min(e, c.ret + 30 * DV_M), P[2]); P[3].x = st.x; P[3].y = st.y + 60; P[3].z = st.z;
  dvBez(st, P[3], { x: h.x, y: h.y + 80, z: h.z }, h, u, o); o.k = sz; o.al = 0; o.st = k >= 1 ? "home" : "fly"; o.u = u; return o; }
/* the Super Cube, the core: it leaves its orbit at 35 min, settles at the heart of the Omega by 70 min, and goes home after 24 h */
const dvRot = e => e > DV.combat ? (Math.min(e, DV.ret) - DV.combat) * TAU / (40 * DV_M) : 0;
function dvCore(D, o) { const e = D.e, home = P3(NEXUS, D.s0 + e, {}), c = { x: 0, y: DV_Y, z: 0 }; let u = 0;
  if (e < 35 * DV_M) u = 0; else if (e < 70 * DV_M) u = dvEase((e - 35 * DV_M) / (35 * DV_M)); else if (e < DV.ret + 10 * DV_M) u = 1; else u = 1 - dvEase((e - DV.ret - 10 * DV_M) / (25 * DV_M));
  o.x = home.x + (c.x - home.x) * u; o.y = home.y + 25 + (c.y - home.y - 25) * u + Math.sin(u * Math.PI) * 60; o.z = home.z + (c.z - home.z) * u; o.u = u; return o; }
/* the map side: every Assimilation Cube is drawn here while the event runs (their usual markers and models are hidden): one instanced
   hull for all of them (one draw call), full-detail models only for the nearest few, glow points, green trails, the beams that tie
   waiting cubes to the core, lock flashes and shockwaves. */
const dvLive = T => !!dvNow(T);
function dvBuild(W) { const X = { grp: new TH.Group() }, M = borgMats(false); if (!W.borgMaster) W.borgMaster = borgCube(1, 2, 777);
  X.mat = M.hull.clone(); X.mat.emissiveIntensity = .6; X.inst = new TH.InstancedMesh(new TH.BoxGeometry(1, 1, 1), X.mat, 104); X.inst.frustumCulled = false; X.inst.count = 0; X.grp.add(X.inst);
  X.det = []; X.detN = MOBILE ? 8 : FX_LITE() ? 14 : 24;
  const gt = W.glow.dv || (W.glow.dv = glowTex("93,255,106", .85)), pm = (n, size) => { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("color", new TH.BufferAttribute(new Float32Array(n * 3), 3)); const m = new TH.PointsMaterial({ map: gt, size, vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }); const p = new TH.Points(g, m); p.frustumCulled = false; X.grp.add(p); return p; };
  X.TR = 30; X.trail = pm(104 * X.TR, 6); X.glow = pm(104, 22);
  const sg = new TH.BufferGeometry(); sg.setAttribute("position", new TH.BufferAttribute(new Float32Array(104 * 32 * 3), 3)); sg.setAttribute("color", new TH.BufferAttribute(new Float32Array(104 * 32 * 3), 3));
  X.seams = new TH.LineSegments(sg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.seams.frustumCulled = false; X.grp.add(X.seams);
  { const c = [], e = .502, b = .1; for (const [a, d] of [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]) for (const k of [a, d]) c.push([k & 1 ? e : -e, k & 2 ? e : -e, k & 4 ? e : -e]);
    for (const [u, v] of [[[-e, b, -e], [e, b, -e]], [[e, b, -e], [e, b, e]], [[e, b, e], [-e, b, e]], [[-e, b, e], [-e, b, -e]]]) c.push(u, v); X.SE = c.map(q => new TH.Vector3(...q)); } /* 12 edges + a band of light round the middle */
  const lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(104 * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(104 * 6), 3));
  X.beams = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.beams.frustumCulled = false; X.grp.add(X.beams);
  X.fx = []; for (let i = 0; i < 8; i++) { const f = new TH.Sprite(W.additive(gt, 0xbfffc8, 0)); f.visible = false; X.grp.add(f);
    const ring = new TH.Mesh(new TH.RingGeometry(.86, 1, 48), new TH.MeshBasicMaterial({ color: 0x7dff90, transparent: true, opacity: 0, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); ring.visible = false; X.grp.add(ring); X.fx.push({ f, ring, t: -1e9 }); }
  X.haze = []; { const ht = W.glow.dvh || (W.glow.dvh = glowTex("70,255,110", .35)); for (let i = 0; i < 7; i++) { const h = new TH.Sprite(W.additive(ht, 0x3dff6a, 0)); h.material.depthWrite = false; const a = i / 7 * TAU; h.userData.o = [Math.cos(a) * 55, (i % 3 - 1) * 35, Math.sin(a) * 55, 220 + (i * 37) % 120]; X.grp.add(h); X.haze.push(h); } } /* the green nebula the machine sits in */
  X.core = new TH.Sprite(W.additive(gt, 0x9dffae, 0)); X.core.material.depthTest = false; X.core.visible = false; X.grp.add(X.core);
  X.wave = new TH.Mesh(new TH.SphereGeometry(1, 32, 16), new TH.MeshBasicMaterial({ color: 0x5dff6a, transparent: true, opacity: 0, side: TH.BackSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.wave.visible = false; X.grp.add(X.wave);
  X.locked = new Set(); X.SV = new TH.Vector3(); X.fxi = 0; X.D3 = new TH.Object3D(); X.V = new TH.Vector3(); X.q = {}; X.tq = {};
  W.scene.add(X.grp); return (W.dv = X); }
function dvFree(W) { const X = W.dv; if (!X) return; for (const d of X.det) X.grp.remove(d.g); /* the detail models share the master's geometry: never disposed */ W.scene.remove(X.grp);
  X.grp.traverse(o => { try { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); } catch (e) {} }); W.dv = null; G.dvP = null; }
function dvFx(X, p, n, big, t) { const f = X.fx[X.fxi++ % X.fx.length]; f.t = t; f.p = [p.x, p.y, p.z]; f.n = n; f.big = big || 1; }
function dvTick(W, t, T) { const D = dvNow(T); if (!D) { if (W.dv) dvFree(W); return; } const X = W.dv || dvBuild(W), P = dvPlan(D.s0), e = D.e, cp = W.camera.position, o = X.q, D3 = X.D3, lite = reduced || FX_LITE();
  /* the galaxy's mood: the Collective's lights brighten as it wakes, die before the eruption, then burn */
  const wake = clamp(e / DV.mig, 0, 1), eru = e >= DV.erupt ? Math.exp(-(e - DV.erupt) / (D.sim ? 20e3 : 90e3)) : 0, dark = e >= DV.act && e < DV.erupt ? dvEase((e - DV.act) / (DV.erupt - DV.act - 30e3)) : 0;
  X.mat.emissiveIntensity = (.55 + .25 * wake + (reduced ? 0 : .12 * wake * Math.sin(t * .004))) * (1 - .85 * dark) + .5 * eru;
  const near = []; let n = 0, tr = 0, bm = 0, sm = 0; const sp2 = X.seams.geometry.attributes.position.array, sc2 = X.seams.geometry.attributes.color.array; const tp = X.trail.geometry.attributes.position.array, tc = X.trail.geometry.attributes.color.array, gp = X.glow.geometry.attributes.position.array, gc = X.glow.geometry.attributes.color.array, bp = X.beams.geometry.attributes.position.array, bc = X.beams.geometry.attributes.color.array;
  for (const c of P.L) { dvCube(c, e, D, o); if (!fogSeen(o.x, o.z) && o.st === "home") continue;
    const dc = Math.hypot(o.x - cp.x, o.y - cp.y, o.z - cp.z); near.push([dc, c, o.x, o.y, o.z, o.k, o.al, o.rot]);
    D3.position.set(o.x, o.y, o.z); D3.scale.setScalar(o.k); const tum = (1 - o.al) * (o.st === "home" ? .12 : 1); D3.rotation.set(Math.sin(e / 7e4 * c.sp + c.i) * tum * 1.2 + (o.st === "home" ? Math.sin(t * 1.5e-4 + c.x.a0) * .12 : 0), (1 - o.al) * (c.x.a0 + e / 5e4 * c.sp) + o.al * o.rot, Math.cos(e / 9e4 * c.sp + c.i) * tum); D3.updateMatrix(); X.inst.setMatrixAt(n, D3.matrix); c.ni = n; n++;
    { /* the emerald seams: faint on a cube in flight, burning once it locks, flaring in the eruption, dead in the silence before it */ const lv = o.st === "locked" ? (.2 + .1 * Math.sin(t * .002 + c.i * .7)) * (1 - .9 * dark) + 1.1 * eru : o.st === "slide" || o.st === "align" ? .3 + .7 * o.al : o.st === "home" ? .12 * wake : .22;
      if (lv > .02) { for (let k = 0; k < 32; k++) { X.SV.copy(X.SE[k]).applyMatrix4(D3.matrix); const j = (sm * 32 + k) * 3, band = k >= 24 ? (o.st === "locked" ? 3.2 : 1.3) : 1; /* the bands of light run across the machine like the reference's light strips */ sp2[j] = X.SV.x; sp2[j + 1] = X.SV.y; sp2[j + 2] = X.SV.z; sc2[j] = .3 * lv * band; sc2[j + 1] = lv * band; sc2[j + 2] = .45 * lv * band; } sm++; } }
    const g = n - 1, glw = o.st === "locked" ? .35 + 1.1 * eru : o.st === "fly" || o.st === "detach" ? 1 : .55 + .45 * wake; gp[g * 3] = o.x; gp[g * 3 + 1] = o.y; gp[g * 3 + 2] = o.z; gc[g * 3] = .35 * glw; gc[g * 3 + 1] = glw; gc[g * 3 + 2] = .42 * glw;
    if ((o.st === "fly" || o.st === "detach") && !lite) for (let k = 1; k <= X.TR; k++) { const tq = dvCube(c, e - k * (D.sim ? 14e3 : 25e3), D, X.tq); const a = (1 - k / (X.TR + 1)) * (o.st === "detach" ? .4 : .9), j = tr * 3; tp[j] = tq.x; tp[j + 1] = tq.y; tp[j + 2] = tq.z; tc[j] = .25 * a; tc[j + 1] = a; tc[j + 2] = .35 * a; tr++; }
    if (o.st === "hold" || o.st === "align") { const pul = .35 + .3 * Math.sin(t * .006 + c.i * 1.7), j = bm * 6, cx = Math.sign(o.x) * 15, cy2 = DV_Y + Math.sign(o.y - DV_Y) * 15, cz = Math.sign(o.z) * 15; bp[j] = o.x; bp[j + 1] = o.y; bp[j + 2] = o.z; bp[j + 3] = cx; bp[j + 4] = cy2; bp[j + 5] = cz; for (let q = 0; q < 6; q += 3) { bc[j + q] = .3 * pul; bc[j + q + 1] = pul; bc[j + q + 2] = .4 * pul; } bm++; }
    if (o.st === "locked" && !X.locked.has(c.i)) { X.locked.add(c.i); if (e - c.lk < 8000 * (D.sim ? 1 : 3)) dvFx(X, o, c.s.n, 1, t); }
    if (o.st !== "locked") X.locked.delete(c.i); }
  X.inst.count = n; X.inst.instanceMatrix.needsUpdate = true;
  X.glow.geometry.setDrawRange(0, n); X.glow.geometry.attributes.position.needsUpdate = X.glow.geometry.attributes.color.needsUpdate = true; X.glow.material.size = 26;
  X.trail.geometry.setDrawRange(0, tr); X.trail.geometry.attributes.position.needsUpdate = X.trail.geometry.attributes.color.needsUpdate = true;
  X.seams.geometry.setDrawRange(0, sm * 32); X.seams.geometry.attributes.position.needsUpdate = X.seams.geometry.attributes.color.needsUpdate = true;
  X.beams.geometry.setDrawRange(0, bm * 2); X.beams.geometry.attributes.position.needsUpdate = X.beams.geometry.attributes.color.needsUpdate = true;
  /* full detail for the nearest cubes: the instanced hull of each is folded away under its model */
  near.sort((a, b) => a[0] - b[0]); const want = near.slice(0, X.detN).filter(r => r[0] < 260 + r[5] * 18);
  while (X.det.length < want.length) { const g = W.borgMaster.clone(); g.traverse(m => { if (m.isMesh) m.frustumCulled = false; if (m.isPoints) m.visible = false; }); /* its pin-lights read as green static at this size */ X.grp.add(g); X.det.push({ g }); }
  X.det.forEach((d, i) => { const r = want[i]; d.g.visible = !!r; if (!r) return; const c = r[1]; X.inst.getMatrixAt(c.ni, d.g.matrix); d.g.matrix.decompose(d.g.position, d.g.quaternion, d.g.scale); d.g.scale.multiplyScalar(1.001); D3.scale.setScalar(0); D3.updateMatrix(); X.inst.setMatrixAt(c.ni, D3.matrix); });
  /* lock flashes: a white-green flare and a shockwave ring racing out across the face it locked onto */
  for (const f of X.fx) { const a = (t - f.t) / 1400; if (a < 0 || a > 1 || reduced) { f.f.visible = f.ring.visible = false; continue; }
    f.f.visible = f.ring.visible = true; f.f.position.set(f.p[0], f.p[1], f.p[2]); f.f.scale.setScalar(70 * f.big * (.4 + a)); f.f.material.opacity = Math.pow(1 - a, 2) * .95;
    f.ring.position.set(f.p[0] - f.n[0] * 7, f.p[1] - f.n[1] * 7, f.p[2] - f.n[2] * 7); f.ring.lookAt(f.ring.position.x + f.n[0], f.ring.position.y + f.n[1], f.ring.position.z + f.n[2]); f.ring.scale.setScalar(6 + 90 * dvEase(a)); f.ring.material.opacity = (1 - a) * .8; }
  { const done = X.locked.size / Math.max(1, P.N), hz = (lite ? .05 : .09) * done * (1 - .8 * dark) + .25 * eru; for (const h of X.haze) { const u = h.userData.o, cr = dvRot(e); h.visible = hz > .005; h.position.set(u[0] * Math.cos(cr) + u[2] * Math.sin(cr), DV_Y + u[1], -u[0] * Math.sin(cr) + u[2] * Math.cos(cr)); h.scale.setScalar(u[3] * (1 + .5 * eru)); h.material.opacity = hz * (.8 + .2 * Math.sin(t * .0008 + u[3])); } }
  /* the core: silent and dark, then the eruption (a sphere of light racing out), then it burns at the heart of the machine */
  const live = e >= DV.erupt && e < DV.ret + 10 * DV_M; X.core.visible = live; if (live) { X.core.position.set(0, DV_Y, 0); X.core.scale.setScalar(120 + 260 * eru + (reduced ? 0 : 12 * Math.sin(t * .003))); X.core.material.opacity = .35 + .6 * eru; }
  const wa = (e - DV.erupt) / (D.sim ? 6e3 : 40e3); X.wave.visible = wa >= 0 && wa < 1 && !reduced; if (X.wave.visible) { X.wave.position.set(0, DV_Y, 0); X.wave.scale.setScalar(20 + 900 * dvEase(wa)); X.wave.material.opacity = .55 * (1 - wa); }
  /* the Super Cube itself (W.nexus) is moved by the map's own Cube code (dvCore there) */
}
/* the owner's preview: the whole event (awakening, migration, assembly, eruption, a turn of the finished Omega, and its break-up) in
   four minutes, on this device only */
function dvSimStart() { if (!duelOwner()) return; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } G.dvP = null; G.dvSim = { t0: performance.now(), s0: Math.floor(now() / 60000) * 60000 };
  toast("Owner preview: Cube Devastation in four minutes. Only you see this."); try { const c = G3 && G3.cam; if (c) { c.follow = null; c.followFleet = null; c.goal = { tx: 0, ty: DV_Y, tz: 0, dist: 520, th: .6 }; } } catch (e) {} }
function dvSimStop(done) { if (!G.dvSim) return; G.dvSim = null; G.dvP = null; toast(done ? "Preview over: the cubes are home." : "Preview stopped."); }
