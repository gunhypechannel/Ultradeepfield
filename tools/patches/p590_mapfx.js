/* ---------- v590 the Titan ultimate moment, and map battles remastered ---------- */
/* when a Titan unleashes its ultimate (Worldbreaker Cannon, Wing launch, Swarm) the battle drops into slow motion for a beat: the screen
   flashes in the weapon's colour, cinematic bars slide in, and speed lines rush toward the Titan */
function fx590UltStart(b, v) { try { if (b.lowFx || reduced || !(v.ab === "wbc" || v.ab === "wing" || v.ab === "swarm")) return; const tn = performance.now(); if (b.ult590 && tn - b.ult590.t < 4000) return;
  b.ult590 = { t: tn, i: v.s, col: v.ab === "wbc" ? "255,170,60" : v.ab === "wing" ? "122,244,255" : "93,255,168" }; b.slowUntil = Math.max(b.slowUntil || 0, tn + 1200); b.shake = Math.max(b.shake || 0, 10 * (b.qs || 1)); } catch (e) {} }
function fx590Ult(ctx, b, t, W, H, d, scr, vs, vtx, vty) { const u = b.ult590; if (!u) return; const age = t - u.t, L = 1700; if (age < 0 || age > L) { if (age > L) b.ult590 = null; return; }
  const k = age / L, inA = Math.min(1, age / 140), outA = k > .7 ? 1 - (k - .7) / .3 : 1, A = inA * outA, S0 = scr[u.i], cx = S0 ? S0.x * vs + vtx : W / 2, cy = S0 ? S0.y * vs + vty : H / 2;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  /* the flash: white first, then the weapon's colour */
  const fl = Math.max(0, 1 - age / 260); if (fl > 0) { ctx.globalCompositeOperation = "lighter"; ctx.fillStyle = `rgba(255,255,255,${.55 * fl})`; ctx.fillRect(0, 0, W, H); }
  ctx.globalCompositeOperation = "lighter"; const rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, H) * .9); rg.addColorStop(0, `rgba(${u.col},${.32 * A})`); rg.addColorStop(.35, `rgba(${u.col},${.1 * A})`); rg.addColorStop(1, `rgba(${u.col},0)`); ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H);
  /* speed lines rushing in toward the Titan */
  const n = 34, R0 = Math.hypot(W, H) * .62; for (let i = 0; i < n; i++) { const a = i / n * TAU + ((i * 7919) % 100) / 100 * .18, ph = ((age / 520) + ((i * 37) % 11) / 11) % 1, r1 = R0 * (1 - ph * .55), r2 = r1 - R0 * (.18 + ((i * 13) % 7) / 40), w = (1.2 + (i % 3)) * d;
    ctx.strokeStyle = `rgba(${i % 4 ? u.col : "255,255,255"},${.5 * A * (1 - ph * .6)})`; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1); ctx.lineTo(cx + Math.cos(a) * r2, cy + Math.sin(a) * r2); ctx.stroke(); }
  /* cinematic bars */
  /* (the HUD panels cover the canvas's top ~12% and bottom ~11%, so the bars slide in just inside them) */
  const y1 = H * .118, y2 = H * .886, bh = H * .07 * (age < 180 ? age / 180 : outA); ctx.globalCompositeOperation = "source-over"; ctx.fillStyle = "rgba(0,0,0,.9)"; ctx.fillRect(0, 0, W, y1 + bh); ctx.fillRect(0, y2 - bh, W, H - y2 + bh);
  ctx.globalCompositeOperation = "lighter"; ctx.fillStyle = `rgba(${u.col},${.8 * A})`; ctx.fillRect(0, y1 + bh - 1.5 * d, W, 1.5 * d); ctx.fillRect(0, y2 - bh, W, 1.5 * d);
  ctx.restore(); }

/* map battles: glowing tracer heads on every bolt, a shockwave ring and flying sparks where a ship blows apart, a warp-in flash with
   speed streaks as the attackers drop out of warp, and a big ring over the beaten side when the battle is decided */
function fx590Init(W, c) { const g = new TH.Group(); W.scene.add(g); const tx = W.glow.trc || (W.glow.trc = glowTex("255,255,255", 1)), sp = (col, ro) => { const s = new TH.Sprite(W.additive(tx, col, 0)); s.renderOrder = ro || 15; g.add(s); return s; };
  const heads = [], sparks = [], rings = [], nh = MOBILE ? 28 : 48, ns = MOBILE ? 24 : 48; for (let i = 0; i < nh; i++) heads.push(sp(0xffffff)); for (let i = 0; i < ns; i++) sparks.push({ sp: sp(0xffb060), t0: -1e9, v: new TH.Vector3(), p: new TH.Vector3() });
  const rgeo = new TH.RingGeometry(.88, 1, 64); for (let i = 0; i < 6; i++) { const m = new TH.Mesh(rgeo, new TH.MeshBasicMaterial({ color: 0xffc070, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); m.frustumCulled = false; m.renderOrder = 14; g.add(m); rings.push({ m, t0: -1e9, p: new TH.Vector3(), s: 1, life: 650 }); }
  const sg = new TH.BufferGeometry(); sg.setAttribute("position", new TH.BufferAttribute(new Float32Array(16 * 6), 3).setUsage(TH.DynamicDrawUsage));
  const streak = new TH.LineSegments(sg, new TH.LineBasicMaterial({ color: c.aCol, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); streak.frustumCulled = false; streak.renderOrder = 14; g.add(streak);
  return { g, heads, sparks, rings, flash: sp(0xffffff, 16), streak, si: 0, ri: 0, warp: (performance.now() - c.t0) < 900, vd: 0 }; }
function fx590Free(W, o) { const f = o && o.f5; if (!f) return; W.scene.remove(f.g); const gs = new Set(); f.g.traverse(m => { if (m.material) m.material.dispose(); if (m.geometry && !m.isSprite) gs.add(m.geometry); }); gs.forEach(x => x.dispose()); o.f5 = null; }
function fx590Ring(f, p, s, col, tn, life) { const r = f.rings[(f.ri++) % f.rings.length]; r.t0 = tn; r.p.copy(p); r.s = s; r.life = life || 650; r.m.material.color.set(col); }
function fx590Boom(o, p, big, hs, tn, fsC) { const f = o && o.f5; if (!f || !big) return; const s = hs || fsC * 2.6; fx590Ring(f, p, s, hs ? 0xffd27a : 0xffb060, tn);
  for (let i = 0; i < (MOBILE ? 5 : 8); i++) { const k = f.sparks[(f.si++) % f.sparks.length]; k.t0 = tn; k.p.copy(p); k.v.set(Math.random() - .5, Math.random() - .5, Math.random() - .5).normalize().multiplyScalar(s * (.0018 + Math.random() * .0022)); k.sz = s * (.12 + Math.random() * .1); k.sp.material.color.setHex(Math.random() < .3 ? 0xffffff : 0xffa040); } }
function fx590Tick(W, c, o, tn, fsC, e, k, q) { const f = o.f5; if (!f) return; const cam = W.camera;
  /* tracer heads ride the leading tip of every bolt (boss fights already have their own) */
  let i = 0; if (!o.boss) for (const b of o.bl) { if (i >= f.heads.length) break; const s0 = (tn - b.t0) / 320, s1 = Math.min(1, s0 + (b.L ? Math.min(.22, 3.5 / b.L) : .22)), h = f.heads[i++];
    h.position.set(b.a.x + (b.b.x - b.a.x) * s1, b.a.y + (b.b.y - b.a.y) * s1, b.a.z + (b.b.z - b.a.z) * s1); h.material.color.setRGB(b.col[0], b.col[1], b.col[2]); h.material.opacity = .9; h.scale.setScalar(fsC * .55); }
  for (; i < f.heads.length; i++) f.heads[i].material.opacity = 0;
  for (const r of f.rings) { const a = (tn - r.t0) / r.life; if (a < 0 || a > 1) { r.m.material.opacity = 0; continue; } r.m.position.copy(r.p); r.m.lookAt(cam.position); r.m.scale.setScalar(r.s * (.25 + Math.pow(a, .6) * 2.4)); r.m.material.opacity = Math.pow(1 - a, 1.5) * .9; }
  for (const s of f.sparks) { const a = (tn - s.t0) / 700; if (a < 0 || a > 1) { s.sp.material.opacity = 0; continue; } s.sp.position.copy(s.p).addScaledVector(s.v, tn - s.t0); s.sp.scale.setScalar(s.sz * (1 - a * .6)); s.sp.material.opacity = 1 - a; }
  /* warp-in: a flash where the attackers drop out of warp and streaks trailing behind them while they close in */
  const wa = e / 900; if (f.warp && wa < 1) { f.flash.position.copy(o.ga.position); f.flash.scale.setScalar(fsC * (3 + wa * 7)); f.flash.material.color.setHex(c.aCol); f.flash.material.opacity = Math.pow(1 - wa, 2); } else f.flash.material.opacity = 0;
  const sa = e / 2000; if (f.warp && sa < 1) { const P = f.streak.geometry.attributes.position.array, dir = new TH.Vector3().subVectors(o.ga.position, o.gd.position).normalize(), side = new TH.Vector3().crossVectors(dir, cam.up).normalize(), up = new TH.Vector3().crossVectors(side, dir), sz = fsC * (o.ga.userData.size || .5) * 3;
    for (let j = 0; j < 16; j++) { const ox = Math.sin(j * 12.9898) * sz, oy = Math.cos(j * 78.233) * sz * .5, L = fsC * (6 + (j % 5) * 2) * (1 - sa), st = new TH.Vector3().copy(o.ga.position).addScaledVector(side, ox).addScaledVector(up, oy).addScaledVector(dir, sz * .3);
      P.set([st.x, st.y, st.z, st.x + dir.x * L, st.y + dir.y * L, st.z + dir.z * L], j * 6); }
    f.streak.geometry.attributes.position.needsUpdate = true; f.streak.material.opacity = .85 * (1 - sa); } else f.streak.material.opacity = 0;
  if (f.warp && e < 40 && !f.wr) { f.wr = 1; fx590Ring(f, o.ga.position, fsC * 4, c.aCol, tn, 800); }
  /* the decision: a big ring and flash over the side that lost */
  if (k > .86 && !f.vd && (c.winner === "a" || c.winner === "d")) { f.vd = 1; const lost = c.winner === "a" ? (o.bx || o.boss ? new TH.Vector3(q.x, q.y, q.z) : o.gd.position) : o.ga.position, win = c.winner === c.you;
    fx590Ring(f, lost, fsC * 6, c.you ? (win ? 0x7be39a : 0xff6b5a) : 0xffd66a, tn, 1100); fx590Ring(f, lost, fsC * 3.5, 0xffffff, tn + 120, 900); for (let j = 0; j < 3; j++) fx590Boom(o, lost.clone().add(new TH.Vector3(Math.random() - .5, Math.random() - .5, Math.random() - .5).multiplyScalar(fsC * 2)), 1, 0, tn, fsC); }
}
