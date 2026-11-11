/* v447 the countdown is a revolving rune clock (owner: "a glyph clock that showed days, hours, minutes, seconds in a revolving style glyph
   rune clock", and "in and out, matrix style, glyphs and then time"). Four concentric rings of the elemental rune marks turn like an
   astrolabe: seconds (outer, turning smoothly), minutes, hours, days (inner), each clicking round as its unit changes, the current rune
   under a marker at the top. Across the middle the time reads in large glowing digits that, every 14 s, scramble into runes and decode
   back, with power surges and green lightning. One canvas on one textured plane: only the real digits are drawn (v440's per-segment
   instance colours did not take on some iPhones, which lit every digit as 8). */
const DVM = { CW: 1024, CH: 1024, P: 14000, IN: 2600, RG: [["SEC", 60, 432], ["MIN", 60, 362], ["HRS", 24, 292], ["DAYS", 30, 222]] };
function dvCdBuild(W) { const C = { grp: new TH.Group(), arc: [] }, cv = document.createElement("canvas"); cv.width = DVM.CW; cv.height = DVM.CH; C.g = cv.getContext("2d");
  C.tex = new TH.CanvasTexture(cv); C.tex.minFilter = TH.LinearFilter; C.tex.generateMipmaps = false;
  const PW = 150, PH = PW * DVM.CH / DVM.CW; C.mesh = new TH.Mesh(new TH.PlaneGeometry(PW, PH), new TH.MeshBasicMaterial({ map: C.tex, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }));
  C.mesh.renderOrder = 5; C.mesh.frustumCulled = false; C.grp.add(C.mesh);
  /* the glyph atlas: the rune marks of the elemental rings and hex code, each in three brightnesses (head, body, tail) */
  const GS = 28, kinds = RUNE_G.length + 16, at = document.createElement("canvas"); at.width = GS * kinds; at.height = GS * 3; const a = at.getContext("2d"), cols = ["#f0fff4", "#5dff7e", "#1f8f3c"];
  a.lineCap = "round"; a.lineJoin = "round"; a.textAlign = "center"; a.textBaseline = "middle"; a.font = `700 ${Math.round(GS * .78)}px ui-monospace, Menlo, Consolas, monospace`;
  for (let r = 0; r < 3; r++) for (let k = 0; k < kinds; k++) { const x = k * GS + GS / 2, y = r * GS + GS / 2; a.strokeStyle = a.fillStyle = cols[r];
    if (k < RUNE_G.length) { a.save(); a.translate(x, y); a.scale(GS / 24, GS / 24); a.lineWidth = 2.2; try { a.stroke(new Path2D(RUNE_G[k])); } catch (e) {} a.restore(); } else a.fillText("0123456789ABCDEF"[k - RUNE_G.length], x, y + 1); }
  C.at = at; C.GS = GS; C.kinds = kinds; C.ang = [0, 0, 0, 0];
  /* the digits: 8 seven-segment cells and 3 colons */
  const DW = 70, DH = 118, T = 12, cy = 524; C.cy = cy; C.cells = []; let x = 118, d = 0;
  for (const it of "DDCDDCDDCDD") { if (it === "C") { C.cells.push({ colon: 1, x: x + 18 }); x += 48; continue; }
    const cx = x + DW / 2, L = cx - DW / 2 + T / 2, R = cx + DW / 2 - T / 2, Tp = cy - DH / 2 + T / 2, Bt = cy + DH / 2 - T / 2;
    const H = yc => ({ x: cx - DW / 2 + T, y: yc - T / 2, w: DW - 2 * T, h: T }), V = (xc, y0, y1) => ({ x: xc - T / 2, y: y0 + T * .5, w: T, h: y1 - y0 - T });
    const seg = { a: H(Tp), g: H(cy), d: H(Bt), b: V(R, Tp, cy), c: V(R, cy, Bt), f: V(L, Tp, cy), e: V(L, cy, Bt) }; for (const k in seg) { seg[k].cx = seg[k].x + seg[k].w / 2; seg[k].cy = seg[k].y + seg[k].h / 2; }
    C.cells.push({ d: d++, x: cx, seg }); x += DW + 12; }
  /* the fixed plate: title, unit names and the faint ghost of every segment, drawn once */
  const pl = document.createElement("canvas"); pl.width = DVM.CW; pl.height = DVM.CH; const p = pl.getContext("2d"); p.textAlign = "center"; p.textBaseline = "middle";
  const O = DVM.CW / 2; p.fillStyle = "#c9ffd2"; p.shadowColor = "#38ff6a"; p.shadowBlur = 20; p.font = `800 46px ${cssFont()}`; { const txt = "CUBE DEVASTATION", R = 486, sp = .068; let a = -Math.PI / 2 - sp * (txt.length - 1) / 2;
    for (const ch of txt) { p.save(); p.translate(O + Math.cos(a) * R, O + Math.sin(a) * R); p.rotate(a + Math.PI / 2); p.fillText(ch, 0, 0); p.restore(); a += sp; } }
  p.shadowBlur = 8; p.lineWidth = 2; for (const [, , R] of DVM.RG) for (const r of [R - 30, R + 30]) { p.strokeStyle = "rgba(93,255,130,.28)"; p.beginPath(); p.arc(O, O, r, 0, Math.PI * 2); p.stroke(); }
  p.shadowBlur = 0; p.fillStyle = "rgba(70,255,120,.07)"; const dc = C.cells.filter(c => !c.colon); for (const c of dc) for (const k in c.seg) { const r = c.seg[k]; p.fillRect(r.x, r.y, r.w, r.h); } C.plate = pl;
  C.grp.scale.setScalar(1.55); W.scene.add(C.grp); return (W.dvCd = C); }
function dvCdDraw(C, t, T, dt) { const g = C.g, CW = DVM.CW, CH = DVM.CH, GS = C.GS, A = C.at, IN = DVM.IN, OUT = DVM.P - 3000, h = n => Math.abs(Math.sin(n * 127.1 + 311.7) * 43758.5453) % 1;
  const left = Math.max(0, dvNext(T) - T), sec = Math.floor(left / 1000), v = [Math.min(99, Math.floor(sec / 86400)), Math.floor(sec / 3600) % 24, Math.floor(sec / 60) % 60, sec % 60], dg = v.flatMap(q => [Math.floor(q / 10), q % 10]);
  const u = reduced ? 5000 : t % DVM.P, rain = reduced ? 0 : u < IN ? 1 - .72 * u / IN : u > OUT ? .28 + .72 * Math.min(1, (u - OUT) / 1400) : .28, sw = ((t / 2600) % 1) * (CW + 300) - 150;
  g.globalCompositeOperation = "source-over"; g.globalAlpha = 1; g.clearRect(0, 0, CW, CH); g.globalCompositeOperation = "lighter";
  const glyph = (k, row, x, y, s, al) => { if (al <= .01) return; g.globalAlpha = Math.min(1, al); g.drawImage(A, (Math.abs(k | 0) % C.kinds) * GS, row * GS, GS, GS, x - s / 2, y - s / 2, s, s); };
  const rr = (x, y, w, hh, q) => { g.beginPath(); if (g.roundRect) g.roundRect(x, y, w, hh, q); else g.rect(x, y, w, hh); g.fill(); };
  const seg = (r, k) => { g.globalAlpha = Math.min(1, .16 * k); g.fillStyle = "#38ff6a"; rr(r.x - 7, r.y - 7, r.w + 14, r.h + 14, 9); g.globalAlpha = Math.min(1, .3 * k); g.fillStyle = "#5dff86"; rr(r.x - 3, r.y - 3, r.w + 6, r.h + 6, 6);
    g.globalAlpha = Math.min(1, .55 + .3 * k); g.fillStyle = k > 1.6 ? "#ffffff" : "#c8ffd6"; rr(r.x, r.y, r.w, r.h, 4); };
  /* the rings: each turns so its current value sits under the marker at the top; seconds glide, the rest click round and settle */
  const O = CW / 2, cur = [reduced ? sec % 60 : (left / 1000) % 60, v[2], v[1], v[0]];
  DVM.RG.forEach(([nm, N, R], ri) => { const tgt = cur[ri], dA = tgt - C.ang[ri], wrap = ((dA % N) + N * 1.5) % N - N / 2; C.ang[ri] = ri === 0 || reduced ? tgt : C.ang[ri] + wrap * (1 - Math.exp(-dt / 220));
    const st = Math.PI * 2 / N, sz = ri === 0 ? 30 : 36;
    for (let k = 0; k < N; k++) { const a = -Math.PI / 2 + (k - C.ang[ri]) * st, x = O + Math.cos(a) * R, y = O + Math.sin(a) * R, top = Math.cos(a + Math.PI / 2), near = Math.max(0, top), band = Math.abs(y - C.cy) < 86 ? .25 : 1;
      const dk = ((k - C.ang[ri]) % N + N) % N, on = dk < .5 || dk > N - .5; if (dk >= .5 && dk < 1.6) continue; /* the label's window */ glyph((k * 7 + ri * 13) % RUNE_G.length, on ? 0 : near > .9 ? 1 : 2, x, y, on ? sz * 1.35 : sz, band * (on ? 1 : .35 + .55 * near * near)); }
    g.globalAlpha = .9; g.strokeStyle = "#9dffb4"; g.lineWidth = 3; g.beginPath(); g.moveTo(O - 26, O - R - 34); g.lineTo(O, O - R - 22); g.lineTo(O + 26, O - R - 34); g.stroke();
    g.fillStyle = "#7dffa0"; g.font = `700 20px ${cssFont()}`; g.textAlign = "left"; g.textBaseline = "middle"; g.globalAlpha = .85; g.fillText(nm, O + 30, O - R); });
  g.globalAlpha = .95; g.drawImage(C.plate, 0, 0);
  /* the digits decode in, hold, and dissolve */
  const lit = []; for (const c of C.cells) {
    if (c.colon) { if (reduced || (u >= IN - 500 && u < OUT + 400)) { const k = .7 + .3 * Math.sin(t * .006); for (const y of [-28, 28]) seg({ x: c.x - 7, y: C.cy + y - 7, w: 14, h: 14 }, k); } continue; }
    const i = c.d, lockT = 450 + i * 230, outT = OUT + i * 170, val = dg[i];
    if (c.v !== val) { if (c.v != null && u > lockT && u < outT) c.sh = t; c.v = val; }
    if (!reduced && u >= outT) { const q = (u - outT) / 900; if (q < 1) { const k = Math.floor(t / 70) + i * 7; glyph(k, 0, c.x, C.cy - 30 + q * 110, 64, 1 - q); glyph(k + 5, 1, c.x, C.cy + 30 + q * 140, 56, (1 - q) * .75); } continue; }
    if (!reduced && (u < lockT || t - (c.sh || -1e9) < 120)) { const k = Math.floor(t / 70) + i * 7; glyph(k, 0, c.x, C.cy - 34, 62, .95); glyph(k + 3, 1, c.x, C.cy + 34, 62, .8); continue; }
    const fl = !reduced && u < lockT + 500 ? 1 + 1.6 * Math.exp(-(u - lockT) / 160) : 1, tk = i >= 6 ? .5 * Math.exp(-(t % 1000) / 180) : 0;
    for (const s of DVC_DIG[val]) { const r = c.seg[s]; seg(r, fl * (1 + 1.4 * Math.exp(-Math.pow((r.cx - sw) / 60, 2)) + tk)); lit.push(r); } }
  /* green lightning between lit segments */
  if (!reduced && lit.length > 1 && Math.random() < .3 && C.arc.length < 6) { const a = lit[(Math.random() * lit.length) | 0], b = lit[(Math.random() * lit.length) | 0]; if (a !== b && Math.abs(a.cx - b.cx) < 260) C.arc.push({ a, b, t0: t, life: 90 + Math.random() * 180, sd: Math.random() * 1e4 }); }
  C.arc = C.arc.filter(q => t - q.t0 < q.life); g.lineCap = "round"; g.lineJoin = "round";
  for (const q of C.arc) { const j = ((t / 40) | 0) + q.sd, pts = [[q.a.cx, q.a.cy]]; for (let k = 1; k <= 8; k++) { const f = k / 8; pts.push([q.a.cx + (q.b.cx - q.a.cx) * f + (k < 8 ? Math.sin(j * 12.9 + k * 78.2) * 12 : 0), q.a.cy + (q.b.cy - q.a.cy) * f + (k < 8 ? Math.cos(j * 4.1 + k * 31.7) * 12 : 0)]); }
    for (const [w, al, col] of [[7, .25, "#38ff6a"], [2.4, .95, "#e2ffe9"]]) { g.globalAlpha = al; g.strokeStyle = col; g.lineWidth = w; g.beginPath(); pts.forEach(([x, y], k) => k ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); } }
  g.globalAlpha = 1; }
function dvCountdown(W, t, T, live) { const show = !live && view === "galaxy";
  if (!show) { if (W.dvCd) { W.dvCd.grp.visible = false; W.dvCd.hid = 1; } return; } const C = W.dvCd || dvCdBuild(W); C.grp.visible = true;
  /*POS*/
  C.grp.quaternion.copy(W.camera.quaternion);
  if (C.drawn && t - C.drawn < (reduced ? 1000 : MOBILE ? 60 : 33)) return; const dt = Math.min(200, t - (C.drawn || t)); C.drawn = t; dvCdDraw(C, t, T, dt); C.tex.needsUpdate = true; }
