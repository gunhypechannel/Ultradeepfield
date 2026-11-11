/* v440 the countdown to Cube Devastation: a giant 3D clock hanging over the Void (DAYS : HRS : MIN : SEC), every digit built of glowing
   emerald segments, with power surges racing through it and green lightning arcing between the digits. It faces the camera, it is
   drawn in 4 calls (segments, halos, arcs, title plate), and it hides while the event itself runs. */
const DVC_SEG = { a: [0, 1, 1, 0], b: [1, .5, 0, 1], c: [1, -.5, 0, 1], d: [0, -1, 1, 0], e: [-1, -.5, 0, 1], f: [-1, .5, 0, 1], g: [0, 0, 1, 0] };
const DVC_DIG = ["abcdef", "bc", "abdeg", "abcdg", "bcfg", "acdfg", "acdefg", "abc", "abcdefg", "abcdfg"];
function dvNext(T) { let s = Math.max(DV_FIRST, dvStartOf(T)); if (T >= s) { const d = new Date(s); s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 11, 18); } return s; }
function dvCdBuild(W) { const C = { grp: new TH.Group(), segs: [] }, DW = 10, DH = 9, TH0 = 1.9, GAP = 15.5, COL = 7; let x = 0;
  const lay = []; for (let i = 0; i < 4; i++) { for (let k = 0; k < 2; k++) { lay.push({ d: i * 2 + k, x }); x += GAP; } if (i < 3) { lay.push({ colon: 1, x: x - GAP / 2 + COL / 2 - 1 }); x += COL; } }
  const x0 = (x - GAP) / 2; C.lay = lay;
  for (const L of lay) { if (L.colon) { for (const y of [-4.5, 4.5]) C.segs.push({ x: L.x - x0, y, sx: 2.6, sy: 2.6, colon: 1 }); continue; }
    for (const s in DVC_SEG) { const [ox, oy, hz] = DVC_SEG[s]; C.segs.push({ d: L.d, s, x: L.x - x0 + ox * DW / 2, y: oy * DH, sx: hz ? DW - 1.4 : TH0, sy: hz ? TH0 : DH - 1.4 }); } }
  const n = C.segs.length; C.box = new TH.InstancedMesh(new TH.BoxGeometry(1, 1, 1.6), new TH.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }), n);
  C.halo = new TH.InstancedMesh(new TH.PlaneGeometry(1, 1), new TH.MeshBasicMaterial({ map: W.glow.dv || (W.glow.dv = glowTex("93,255,106", .85)), color: 0xffffff, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }), n);
  const D3 = new TH.Object3D(); C.segs.forEach((s, i) => { D3.position.set(s.x, s.y, 0); D3.scale.set(s.sx, s.sy, 1); D3.updateMatrix(); C.box.setMatrixAt(i, D3.matrix); D3.scale.set(s.sx * 2.6 + 6, s.sy * 2.6 + 6, 1); D3.position.z = -1; D3.updateMatrix(); C.halo.setMatrixAt(i, D3.matrix); C.box.setColorAt(i, new TH.Color(0, 0, 0)); C.halo.setColorAt(i, new TH.Color(0, 0, 0)); });
  for (const m of [C.box, C.halo]) { m.frustumCulled = false; C.grp.add(m); }
  const ag = new TH.BufferGeometry(); ag.setAttribute("position", new TH.BufferAttribute(new Float32Array(16 * 10 * 6), 3)); C.arcs = new TH.LineSegments(ag, new TH.LineBasicMaterial({ color: 0xb8ffc8, transparent: true, opacity: .95, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); C.arcs.frustumCulled = false; C.grp.add(C.arcs); C.arc = [];
  /* the title above the clock and the unit names under it, on one plate as wide as the clock (the canvas keeps the plate's shape) */
  const PW = x + 10, PH = 64, cv = document.createElement("canvas"); cv.width = 1024; cv.height = Math.round(1024 * PH / PW); const g = cv.getContext("2d"), sx = 1024 / PW, Y = y => (PH / 2 - y) * sx;
  g.textAlign = "center"; g.textBaseline = "middle"; g.fillStyle = "#c9ffd2"; g.shadowColor = "#38ff6a"; g.shadowBlur = 26; g.font = `800 ${Math.round(9.5 * sx)}px ${cssFont()}`; g.fillText("CUBE DEVASTATION", 512, Y(21));
  g.shadowBlur = 12; g.fillStyle = "#7dffa0"; g.font = `700 ${Math.round(3.6 * sx)}px ${cssFont()}`; ["DAYS", "HRS", "MIN", "SEC"].forEach((w, i) => g.fillText(w, 512 + (lay[i * 3].x + GAP / 2 - x0) * sx, Y(-15)));
  C.title = new TH.Mesh(new TH.PlaneGeometry(PW, PH), new TH.MeshBasicMaterial({ map: new TH.CanvasTexture(cv), transparent: true, depthWrite: false, toneMapped: false })); C.title.position.z = -.5; C.title.renderOrder = 5; C.grp.add(C.title); C.w = x;
  C.grp.scale.setScalar(1.55); W.scene.add(C.grp); return (W.dvCd = C); }
function dvCountdown(W, t, T, live) { const show = !live && view === "galaxy";
  if (!show) { if (W.dvCd) W.dvCd.grp.visible = false; return; } const C = W.dvCd || dvCdBuild(W); C.grp.visible = true;
  const left = Math.max(0, dvNext(T) - T), sec = Math.floor(left / 1000), v = [Math.min(99, Math.floor(sec / 86400)), Math.floor(sec / 3600) % 24, Math.floor(sec / 60) % 60, sec % 60], dg = v.flatMap(q => [Math.floor(q / 10), q % 10]);
  C.grp.position.set(0, 128 + Math.sin(t * .0006) * 2, 0); C.grp.quaternion.copy(W.camera.quaternion);
  /* the power surge: a bright front sweeps the clock every few seconds; every second a ripple runs out from the seconds */
  const sw = ((t / 2600) % 1) * (C.w + 60) - C.w / 2 - 30, rip = (t % 1000) / 1000, tick = Math.exp(-rip * 5), col = new TH.Color(), hcol = new TH.Color(); const lit = [];
  C.segs.forEach((s, i) => { const on = s.colon ? 1 : (DVC_DIG[dg[s.d]].includes(s.s) ? 1 : 0), su = Math.exp(-Math.pow((s.x - sw) / 9, 2)), tk = s.d >= 6 ? tick * .6 : 0, fl = reduced ? 1 : .88 + .12 * Math.sin(t * .02 + i * 1.7);
    const k = on ? (s.colon ? .7 + .3 * Math.sin(t * .006) : 1) * fl * (1 + 1.6 * su + tk) : .035 + .05 * su; col.setRGB(.25 * k + .5 * su * on, 1 * k, .42 * k + .3 * su * on); hcol.setRGB(.2 * k, .9 * k, .35 * k).multiplyScalar(on ? .55 : .2);
    C.box.setColorAt(i, col); C.halo.setColorAt(i, hcol); if (on && !s.colon) lit.push(s); });
  C.box.instanceColor.needsUpdate = C.halo.instanceColor.needsUpdate = true;
  /* green lightning: short jagged arcs leap between lit segments, a few at a time, each for a heartbeat */
  if (!reduced && Math.random() < .35 && C.arc.length < 10 && lit.length > 1) { const a = lit[(Math.random() * lit.length) | 0], b = lit[(Math.random() * lit.length) | 0]; if (a !== b && Math.abs(a.x - b.x) < 40) C.arc.push({ a: [a.x, a.y], b: [b.x, b.y], t0: t, life: 90 + Math.random() * 180, sd: Math.random() * 1e4 }); }
  C.arc = C.arc.filter(A => t - A.t0 < A.life); const P = C.arcs.geometry.attributes.position.array; let n = 0;
  for (const A of C.arc) { let px = A.a[0], py = A.a[1]; const steps = 8, j = ((t / 40) | 0) + A.sd;
    for (let k = 1; k <= steps; k++) { const u = k / steps, nx = A.a[0] + (A.b[0] - A.a[0]) * u + (k < steps ? Math.sin(j * 12.9 + k * 78.2) * 3.2 : 0), ny = A.a[1] + (A.b[1] - A.a[1]) * u + (k < steps ? Math.cos(j * 4.1 + k * 31.7) * 3.2 : 0); P.set([px, py, 1.2, nx, ny, 1.2], n * 6); n++; px = nx; py = ny; } }
  C.arcs.geometry.setDrawRange(0, n * 2); C.arcs.geometry.attributes.position.needsUpdate = true; C.arcs.material.opacity = .7 + .3 * Math.random(); }
