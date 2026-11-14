/* ---------- v571 The Ten Seals: every season ends in a great live event, one chapter of the year's story. The finale's Saturday boss
   is its climax: first a galaxy-wide set piece in stages (FIN_EV[k].st), then the fight until the hunt ends. Its result goes in the Seal
   Ledger (event/wboss .ledger[s0] = "held" when the boss falls in time; otherwise the seal cracks and leaves a scar on the map). ---------- */
const FIN_SAY = {
  lev: { burn: "Commander, the Rim is burning. Every sensor along the outer wall just lit up at once.", hunt: "It's here. The Leviathan is circling the whole galaxy, right along the Architects' wall. It's looking for something.",
    breach: "It's turning inward! Commander, it's breaking straight through the Architects' wall!", tide: "Fire tide! It's breathing across the entire outer layer!",
    fight: "It's stopped at the breach, and its scales are cooling. Now we fight, Commander. Every fleet we have.",
    held: "The Leviathan is down, and the wall is holding. The first seal held, Commander. Chapter one is ours.", cracked: "It slipped back into the dark and left the wall broken. The first seal cracked, Commander. We'll carry that scar.",
    sting: "Commander... the Cube's signal just changed. It's counting faster." } };
const finR = seed => { let a = (seed | 0) + 0x9E3779B9; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
const finStage = (k, e) => { const L = FIN_EV[k].st; let i = 0; while (i < L.length - 1 && e >= L[i + 1][0]) i++; return i; };
function finNow(T) { if (G.finSim) return finSimNow(); for (const k in FIN_EV) { const s0 = rotStartOf(k, T); if (s0 != null && T >= s0 && T < s0 + WB_LIVE) { const e = T - s0; return { k, s0, e, si: finStage(k, e) }; } } return null; }
function finLast(k, T) { const s0 = rotStartOf(k, T); return s0 != null && T >= s0 + WB_LIVE ? s0 : null; } // the last finished event
function finOutcome(k, s0, T = now()) { if (s0 == null) return null; const L = ((wbState(T) || {}).ledger || {})[s0] || (((S && S.finLed) || {})[k + s0]); if (L) return L; if (G.wbFakeDead === k && T < s0 + WB_LIVE) return "held"; return T >= s0 + WB_LIVE ? "cracked" : null; }
function finLedger(T = now()) { const out = []; for (let si = 0; si < SEAN; si++) { const [a, b] = SEA_FIN[si]; const k = FIN_EV[b] ? b : null, sat = ROTS0 + (4 * si + 2) * WEEK, cur = vpSeason(T);
    const st = k ? finOutcome(k, sat, T) : null; out.push({ si, k, n: k ? FIN_EV[k].chap : (a === "dv" ? "Cube Devastation" : a === "conv" ? "The Elemental Convergence" : WB[b] ? WB[b].n : b), sat, st: si > cur || T < sat ? "soon" : st || (T < sat + WB_LIVE ? "live" : "—") }); } return out; }
/* the owner's preview: the set piece in two minutes, then the boss on the map for five, on this device only */
function finSimNow() { const C = G.finSim, s = (performance.now() - C.t0) / 1000, F = FIN_EV[C.k], L = 120; if (s >= L + 8) { finSimStop(1); return null; } const e = Math.min(F.set + 50e3, s / L * F.set); return { k: C.k, s0: C.s0, e, si: finStage(C.k, e), sim: 1 }; }
function finSimStart(k) { if (!duelOwner() || !FIN_EV[k]) return; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } G.finSaid = {}; G.finSim = { k, t0: performance.now(), s0: Math.floor(now() / 60000) * 60000 }; toast(`Owner preview: ${FIN_EV[k].n}, the whole set piece in two minutes. Only you see this.`); setTimeout(() => { try { ACT.finWatch({ k }); } catch (e) {} }, 400); }
function finSimStop(done) { const C = G.finSim; if (!C) return; G.finSim = null; if (done) { G.wbShow = C.k; WBN = null; clearTimeout(G.wbShowT); G.wbShowT = setTimeout(() => { G.wbShow = null; WBN = null; }, 5 * 60e3); toast("Preview: the fight. The boss is on the map for five minutes, on this device only."); } else toast("Preview stopped."); }
function finSay(F) { G.finSaid = G.finSaid || {}; const k = F.k, st = FIN_EV[k].st[F.si][1], id = F.s0 + k + st; if (G.finSaid[id]) return; G.finSaid[id] = 1; if (F.si === 0 && F.e > 10 * 60e3 && !F.sim) return; const L = FIN_SAY[k] && FIN_SAY[k][st]; if (L) sbSay(L); }
/* the result: her words once, then the stinger for the next chapter */
function finLedTick() { if (!S || !G.ready || G.finSim) return; const T = now(); S.finSaid = S.finSaid || {};
  for (const k in FIN_EV) { const live = finNow(T), s0 = live && live.k === k ? live.s0 : finLast(k, T); if (s0 == null || T - s0 > WB_LIVE + 7 * 864e5) continue; const o = finOutcome(k, s0, T); if (!o || S.finSaid[k + s0]) continue;
    S.finLed = S.finLed || {}; S.finLed[k + s0] = o; S.finSaid[k + s0] = 1; dirty(); const L = FIN_SAY[k]; if (L && L[o]) { sbSay(L[o]); if (L.sting) setTimeout(() => { try { sbSay(L.sting); } catch (e) {} }, 18000); } } }
/* ---------- on the map ---------- */
function finFree(W) { const X = W.fin; if (!X) return; try { W.scene.remove(X.grp); X.grp.traverse(o => { if (o.geometry && !o.userData.keep) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); }); } catch (e) {} W.fin = null; }
function finTick(W, t, T) { const F = finNow(T); try { finScar(W, t, T); } catch (e) {} if (!F || F.e > FIN_EV[F.k].set + 60e3) { if (W.fin) finFree(W); return; } try { finSay(F); } catch (e) {} if (F.k === "lev") levSet(W, t, F); }
const finPts = (W, X, n, size, rgb) => { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("color", new TH.BufferAttribute(new Float32Array(n * 3), 3));
  const m = new TH.PointsMaterial({ map: glowTex(rgb, .9), size, vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }); const p = new TH.Points(g, m); p.frustumCulled = false; X.grp.add(p); return p; };
function finHexTex() { if (G.finHex) return G.finHex; const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"); x.strokeStyle = "rgba(255,226,150,1)"; x.lineWidth = 3; const r = 22;
  for (let j = -1; j < 5; j++) for (let i = -1; i < 4; i++) { const cx = i * r * 3 + (j % 2 ? r * 1.5 : 0), cy = j * r * .866; x.beginPath(); for (let q = 0; q <= 6; q++) { const a = q * Math.PI / 3; x[q ? "lineTo" : "moveTo"](cx + Math.cos(a) * r, cy + Math.sin(a) * r); } x.stroke(); }
  x.globalCompositeOperation = "destination-in"; const g = x.createLinearGradient(0, 0, 0, 128); g.addColorStop(0, "rgba(0,0,0,.25)"); g.addColorStop(.5, "rgba(0,0,0,1)"); g.addColorStop(1, "rgba(0,0,0,.25)"); x.fillStyle = g; x.fillRect(0, 0, 128, 128);
  const t = new TH.CanvasTexture(c); t.wrapS = TH.RepeatWrapping; return (G.finHex = t); }
/* Chapter 1, The Leviathan Rises: the Rim burns; the Leviathan circles the galaxy along the Architects' wall; it turns inward and the
   wall shatters at the breach; its breath sweeps the outer layer as a ring of fire; then it holds at the breach for the fight */
function levSet(W, t, F) { const D = FIN_EV.lev, e = F.e, E = D.st.map(s => s[0]);
  let X = W.fin; if (X && X.s0 !== F.s0) { finFree(W); X = null; }
  if (!X) { X = W.fin = { k: "lev", s0: F.s0, grp: new TH.Group() }; W.scene.add(X.grp); X.R = LAYERS[0].r1 + 12; X.RW = X.R + 30; X.Ri = LAYERS[0].r0;
    const qB = wbPosRaw("lev", F.s0 + D.set, {}); X.aB = Math.atan2(qB.z, qB.x); X.rB = Math.hypot(qB.x, qB.z); X.yB = qB.y;
    X.N = MOBILE ? 900 : 1600; X.ring = finPts(W, X, X.N, MOBILE ? 15 : 19, "255,130,50"); X.ang = new Float32Array(X.N); { const p = X.ring.geometry.attributes.position.array, r = finR(91); for (let i = 0; i < X.N; i++) { const a = i / X.N * TAU + r() * .004, rr = X.R + (r() - .5) * 12; X.ang[i] = a; p[i * 3] = Math.cos(a) * rr; p[i * 3 + 1] = (r() - .5) * 8; p[i * 3 + 2] = Math.sin(a) * rr; } }
    X.P = 120; const pw = TAU * X.RW / X.P * .97; X.wall = new TH.InstancedMesh(new TH.PlaneGeometry(pw, 64), new TH.MeshBasicMaterial({ map: finHexTex(), color: 0xffd890, transparent: true, opacity: 0, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }), X.P); X.wall.frustumCulled = false; X.grp.add(X.wall);
    X.pan = []; for (let i = 0; i < X.P; i++) { const a = (i + .5) / X.P * TAU; let d = Math.atan2(Math.sin(a - X.aB), Math.cos(a - X.aB)); X.pan.push({ a, d, br: Math.abs(d) < .3, sp: finR(i)() }); }
    X.tide = new TH.Mesh(new TH.RingGeometry(.93, 1, 192), new TH.MeshBasicMaterial({ color: 0xff7a2a, transparent: true, opacity: 0, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.tide.rotation.x = -Math.PI / 2; X.grp.add(X.tide);
    X.emb = finPts(W, X, 500, 7, "255,170,80");
    X.flash = new TH.Sprite(W.additive(glowTex("255,150,60", .9), 0xffa050, 0)); X.flash.position.set(Math.cos(X.aB) * X.RW, 20, Math.sin(X.aB) * X.RW); X.grp.add(X.flash);
    X.halo = new TH.Sprite(W.additive(glowTex("255,110,30", .7), 0xff7a2a, 0)); X.grp.add(X.halo);
    try { BOSS3D.init(TH); BOSS3D.paint = 0; BOSS3D.lod = 1; X.b = BOSS3D.prep(BOSS3D.leviathan(), wbEnv(W.renderer)); X.b.grp.scale.setScalar(6); if (X.b.own) for (const o of X.b.own) o.visible = false; X.grp.add(X.b.grp); } catch (er) { X.b = null; } X.nx = 0; X.pos = new TH.Vector3(); }
  const sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u), u1 = (e - E[1]) / (E[2] - E[1]), u2 = (e - E[2]) / (E[3] - E[2]), u3 = (e - E[3]) / (E[4] - E[3]), fade = 1 - sm((e - E[4]) / 60e3);
  // the serpent's path: emerging beyond the Rim, one lap of the wall, then inward to the breach
  let a = X.aB - TAU, r = X.R + 90, y = 40, sc = 0;
  if (e >= E[1] && e < E[2]) { a = X.aB - TAU * (1 - u1); sc = sm(u1 * 12); y = 34 + 10 * Math.sin(u1 * TAU * 3); }
  else if (e >= E[2]) { a = X.aB; const k = sm(u2 * 1.4); r = X.R + 90 + (X.rB - X.R - 90) * k; y = 40 + (X.yB + 14 - 40) * k; sc = fade; }
  X.pos.set(Math.cos(a) * r, y, Math.sin(a) * r);
  if (X.b) { X.b.grp.visible = sc > .01; X.b.grp.position.copy(X.pos); X.b.grp.scale.setScalar(6 * Math.max(.01, sc)); X.b.grp.rotation.y = -a - Math.PI / 2; X.b.tick(t);
    if (t > X.nx) { if (e >= E[3] && e < E[4]) { X.b.act("lens"); X.nx = t + 3600; } else if (e >= E[1] && e < E[3]) { X.b.act(Math.random() < .5 ? "coil" : "sweep"); X.nx = t + 6000 + Math.random() * 5000; } else X.nx = t + 2000; } }
  if (G.finFollow && performance.now() < G.finFollow && sc > .05 && G3 && G3.cam && G3.cam.goal && !G3.cam.follow) Object.assign(G3.cam.goal, { tx: X.pos.x, ty: X.pos.y, tz: X.pos.z }); // the camera rides with it for a minute after Watch
  X.halo.position.copy(X.pos); X.halo.scale.setScalar(320 * sc); X.halo.material.opacity = .55 * sc * (.85 + .15 * Math.sin(t * .004));
  // the Rim burns: brighter where it has passed, a blaze under it
  { const c = X.ring.geometry.attributes.color.array, base = sm(e / E[1]) * .85 * fade, passed = e >= E[2] ? 1 : e >= E[1] ? u1 : 0, a0 = X.aB - TAU;
    for (let i = 0; i < X.N; i++) { const ai = X.ang[i]; let rel = ((ai - a0) % TAU + TAU) % TAU / TAU; const behind = passed - rel, fl = .75 + .25 * Math.sin(t * .006 + i * 1.7);
      let b = base * fl; if (behind > 0) b += (.6 + 1.2 * Math.exp(-behind * 30)) * fade * fl; c[i * 3] = b; c[i * 3 + 1] = b * .48; c[i * 3 + 2] = b * .16; } X.ring.geometry.attributes.color.needsUpdate = true; }
  // the Architects' wall: it flickers as it fails, then breaks open at the breach
  { const op = .5 * sm(e / (10 * 60e3)) * fade, brk = sm((u2 - .3) / .5), M = new TH.Matrix4(), Q = new TH.Quaternion(), V = new TH.Vector3(), Sx = new TH.Vector3(1, 1, 1), Ax = new TH.Vector3();
    X.wall.material.opacity = op * (.8 + .2 * Math.sin(t * .011) * Math.sin(t * .0037));
    for (let i = 0; i < X.P; i++) { const p = X.pan[i]; let rr = X.RW, yy = 26, s = 1, rot = 0; if (p.br && e >= E[2]) { const k = brk * (1 - Math.abs(p.d) / .3 * .5); rr += k * (140 + 120 * p.sp); yy += k * (60 * (p.sp - .3)); s = Math.max(.001, 1 - k); rot = k * (2 + 4 * p.sp); }
      V.set(Math.cos(p.a) * rr, yy, Math.sin(p.a) * rr); Q.setFromAxisAngle(Ax.set(0, 1, 0), -p.a + Math.PI / 2); if (rot) Q.multiply(new TH.Quaternion().setFromAxisAngle(Ax.set(1, .4, 0).normalize(), rot)); Sx.setScalar(s); M.compose(V, Q, Sx); X.wall.setMatrixAt(i, M); } X.wall.instanceMatrix.needsUpdate = true;
    const fl = e >= E[2] ? Math.max(0, 1 - Math.abs(u2 - .45) / .12) : 0; X.flash.material.opacity = fl; X.flash.scale.setScalar(200 + 500 * fl); }
  // the fire tide: a ring of fire sweeping inward across the outer layer
  { const on = e >= E[3] && e < E[4], R = X.R - (X.R - X.Ri) * Math.max(0, u3) * 1.05; X.tide.visible = on; if (on) { X.tide.scale.setScalar(R); X.tide.material.opacity = .85 * Math.sin(Math.PI * Math.min(1, u3 * 1.05)); }
    const p = X.emb.geometry.attributes.position.array, c = X.emb.geometry.attributes.color.array; for (let i = 0; i < 500; i++) { const q = finR(i * 7 + Math.floor(t / 900))(), aa = i / 500 * TAU + q * .05, rr = on ? R + (q - .5) * 18 : 0, b = on ? X.tide.material.opacity * (.6 + .4 * Math.sin(t * .01 + i)) : 0;
      p[i * 3] = Math.cos(aa) * rr; p[i * 3 + 1] = 4 + q * 16; p[i * 3 + 2] = Math.sin(aa) * rr; c[i * 3] = b; c[i * 3 + 1] = b * .55; c[i * 3 + 2] = b * .2; } X.emb.geometry.attributes.position.needsUpdate = true; X.emb.geometry.attributes.color.needsUpdate = true; } }
/* a cracked seal leaves its scar on the map until that chapter returns: for the Leviathan, a burning rift in the Rim at the breach */
function finScar(W, t, T) { const s0 = finLast("lev", T), cr = s0 != null && T - s0 < 40 * WEEK && finOutcome("lev", s0, T) === "cracked" && !finNow(T);
  if (!cr) { if (W.finScar) { W.scene.remove(W.finScar.p); W.finScar.p.geometry.dispose(); W.finScar = null; } return; }
  let X = W.finScar; if (!X || X.s0 !== s0) { if (X) { W.scene.remove(X.p); X.p.geometry.dispose(); } const qB = wbPosRaw("lev", s0 + FIN_EV.lev.set, {}), aB = Math.atan2(qB.z, qB.x), R = LAYERS[0].r1 + 12, n = 260, g = new TH.BufferGeometry(), pos = new Float32Array(n * 3), r = finR(5);
    for (let i = 0; i < n; i++) { const a = aB + (r() - .5) * .5, rr = R + (r() - .5) * 26; pos[i * 3] = Math.cos(a) * rr; pos[i * 3 + 1] = (r() - .5) * 10; pos[i * 3 + 2] = Math.sin(a) * rr; }
    g.setAttribute("position", new TH.BufferAttribute(pos, 3)); g.setAttribute("color", new TH.BufferAttribute(new Float32Array(n * 3), 3)); const p = new TH.Points(g, new TH.PointsMaterial({ map: glowTex("255,110,40", .9), size: 8, vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); p.frustumCulled = false; W.scene.add(p); X = W.finScar = { s0, p, n }; }
  const c = X.p.geometry.attributes.color.array; for (let i = 0; i < X.n; i++) { const b = .45 + .35 * Math.sin(t * .005 + i * 2.3); c[i * 3] = b; c[i * 3 + 1] = b * .4; c[i * 3 + 2] = b * .12; } X.p.geometry.attributes.color.needsUpdate = true; }
/* ---------- the event panel ---------- */
function shFinale() { const k = sheet.k && FIN_EV[sheet.k] ? sheet.k : "lev", D = FIN_EV[k], T = now(), live = finNow(T), on = live && live.k === k ? live : null, nx = rotNextOf(k, T), s0 = on ? on.s0 : nx, si = on ? on.si : -1, fight = on && on.e >= D.set;
  const tm = x => new Date(x).toLocaleString([], { weekday: "short", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }), st = wbState(T), hp = st.hp[k] | 0, pc = Math.round(hp / WB_SEG * 100), out = finOutcome(k, on ? on.s0 : finLast(k, T), T);
  const tl = D.st.map(([at, id, n, d], i) => { const c = !on ? "" : i < si ? "done" : i === si ? "now" : ""; return `<li class="${c}"><b>${esc(n)}</b><small>${tm(s0 + at)}${c === "now" ? " · NOW" : ""}</small><span>${esc(d)}</span></li>`; }).join("") + `<li class="${on ? "" : ""}"><b>The hunt ends</b><small>${tm(s0 + WB_LIVE)}</small><span>Bring it down before then and the seal holds. If it survives, the seal cracks and leaves a scar on the map.</span></li>`;
  const nextAt = on && si < D.st.length - 1 ? on.s0 + D.st[si + 1][0] : 0;
  const led = finLedger(T).map(x => `<li class="${x.st}"><span>${x.si + 1}. ${esc(x.n)}</span><b>${x.st === "held" ? "✓ Held" : x.st === "cracked" ? "✗ Cracked" : x.st === "live" ? "● Now" : x.st === "soon" ? new Date(x.sat).toLocaleDateString([], { month: "short", day: "numeric" }) : "—"}</b></li>`).join("");
  const now0 = on ? (fight ? `<div class="wbhp"><div class="wbbar"><i style="width:${pc}%;background:${D.col}"></i></div><span>${hp ? `${pc}% hull · the hunt ends in <b data-end="${on.s0 + WB_LIVE}">${ftime(on.s0 + WB_LIVE - T)}</b>` : "Fallen. The seal holds."}</span></div>${hp ? `<button class="btn wide amber" data-act="wboss" data-id="${k}">⚔ Hunt ${esc(WB[k].n)}</button>` : ""}`
      : `<p class="note">Now: <b>${esc(D.st[si][2])}</b>. ${nextAt ? `${esc(D.st[si + 1][2])} in <b data-end="${nextAt}">${ftime(nextAt - T)}</b>.` : ""} Watch it on the galaxy map; the fight opens at <b>${esc(D.st[D.st.length - 1][2])}</b>.</p>`) + `<button class="btn ghost wide" data-act="finWatch" data-k="${k}">🎥 Watch it on the map</button>`
    : `<p class="note">${out && T - (finLast(k, T) || 0) < WB_LIVE + 7 * 864e5 ? (out === "held" ? "The seal held. " : "The seal cracked. ") : ""}Next: <b>${tm(nx)}</b>, in <b data-end="${nx}">${ftime(nx - T)}</b>.</p>${duelOwner() ? `<button class="btn ghost wide" data-act="finSim" data-k="${k}">▶ Watch the preview (owner)</button>` : ""}`;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${D.col}">${on ? "● LIVE · " : ""}The Ten Seals · Chapter ${D.ch} · season finale</div><h2>${esc(D.n)}</h2><p class="note">${esc(D.d)}</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="sbart dvart"><img src="art/arch/${k}.webp?v=1" alt="${esc(WB[k].n)}" loading="lazy"><span class="sbph">${on ? esc(D.st[si][2]) : `Rises in ${ftime(nx - T)}`}</span></div>
    ${now0}<dl class="kv"><dt>Chapter</dt><dd>${esc(D.chap)}</dd><dt>When it falls</dt><dd>The usual world boss spoils for everyone who fought, and the seal holds for the whole galaxy</dd></dl>
    <h2 class="sec">${on ? "The event" : "How it unfolds"}</h2><ol class="dvtl fin" style="--fc:${D.col}">${tl}</ol><h2 class="sec">The Seal Ledger</h2><ol class="finled">${led}</ol>`; }
function finBand(T) { const F = finNow(T); if (F) { const D = FIN_EV[F.k], fight = F.e >= D.set; return `<button class="omb fin" style="--fc:${D.col}" data-act="finOpen" data-k="${F.k}"><b>${D.ic} ${esc(D.n.toUpperCase())}</b><span>${esc(D.st[F.si][2])}</span>${fight && wbUp(F.k, T) ? "<i>⚔ Attack</i>" : ""}</button>`; }
  for (const k in FIN_EV) { const nx = rotNextOf(k, T); if (nx - T < 72 * 3600e3 && nx > T) return `<button class="omb fin soon" style="--fc:${FIN_EV[k].col}" data-act="finOpen" data-k="${k}"><b>${FIN_EV[k].ic} ${esc(FIN_EV[k].n.toUpperCase())}</b><span>in ${ftime(nx - T)}</span></button>`; } return ""; }
setInterval(() => { try { finLedTick(); } catch (e) {} }, 5000);
