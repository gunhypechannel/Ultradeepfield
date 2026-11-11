# v421: the Orbital Devourer leaves a destruction trail. Instead of a cluster of ships at each 3-hourly mark, wrecked ships are strung
# out along its actual path: a sample every 15 minutes of the last 48 h of its route (65% kept), each a burning, broken hull (mixed
# types, the odd faction flagship; split, bow, stern or gutted) off one side of the path at 5-23 units, lying roughly along the way it
# went, purple-lit, its fires dying with age. The 3-hourly marks keep the devoured planetoids and their plates as landmarks. A pool of
# hulls (10, 6 with Lite effects, 4 on phones) fills the stretch of trail nearest the camera, sticky like the wreck sites, one new hull
# built per second.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""  if (wake) { const a = r() * TAU; hull("flagship", new TH.Vector3(Math.cos(a) * 8, 0, Math.sin(a) * 8), 3.6, LITE ? 3 : 6); }""",
    """  if (wake) { /* v421 its ships string out along the trail (wbWakeTrail) */ }""")
rep("""function wbScarFx(W, t, T) {
  try { wbWrecks(W, t, T); } catch (e) { mapErr(e); } // v415""", """/* v421 one wrecked hull of the Devourer's destruction trail */
function wakeHull(W, k, purple, seed) { const DK = debrisKit(W), r = cwRnd(seed), LITE = MOBILE || FX_LITE();
  const g = k === "flagship" ? fleet3D(W, { battleship: 1 }, 0x3a2a20, false, false, false, DEMO_FAC[seed % DEMO_FAC.length]) : fleet3D(W, { [k]: 1 }, 0x3a2a20, false); if (g.userData.eng) g.userData.eng.visible = false;
  g.userData.noBatch = 1; const done = new Map(); g.traverse(o => { if (o.isMesh && o.material && o.material.isMeshBasicMaterial) { o.visible = false; return; } if (!o.isMesh || !o.material || Array.isArray(o.material) || o.material.emissive === undefined) return;
    let m = done.get(o.material); if (!m) { m = o.material.clone(); m.color.multiplyScalar(.4); m.roughness = Math.min(1, (m.roughness || .5) + .25); m.emissive.set(purple ? 0xc77dff : 0xffffff); m.emissiveMap = DK.emi; m.emissiveIntensity = purple ? 1.9 : 1.4; m.envMapIntensity = (m.envMapIntensity == null ? 1 : m.envMapIntensity) * .3; if (m.metalness != null) m.metalness *= .55; done.set(o.material, m); } o.material = m; });
  const holder = new TH.Group(); holder.visible = false; W.add(holder); holder.add(g); g.updateMatrixWorld(true);
  const bb = new TH.Box3().setFromObject(g), sz = bb.getSize(new TH.Vector3()), d = { g, holder, fl: [], fires: [], fs: Math.max(sz.x, sz.y, sz.z) * .22, k: 3.2 + r() * 1.3, e: [(r() - .5) * .9, (r() - .5) * 1.2, (r() - .5) * .9], s: [(r() - .5) * 3e-5, (r() - .5) * 2e-5, (r() - .5) * 2e-5], id: null };
  for (let i = 0; i < (LITE ? 2 : 3); i++) { const q = new TH.Vector3(bb.min.x + r() * sz.x, bb.min.y + r() * sz.y, bb.min.z + r() * sz.z), ax = (r() * 3) | 0; q.setComponent(ax, r() < .5 ? bb.min.getComponent(ax) : bb.max.getComponent(ax)); d.fl.push(q); const f = fireSprite(W, holder, DK); if (purple) f.material.color.set(0xe8c2ff); d.fires.push(f); }
  d.brk = wreckBreak(W, g, r, null, purple, holder, DK); holder.traverse(o => { if (o.isMesh) o.frustumCulled = false; }); return d; }
/* v421 the Devourer's destruction trail: wrecks strung along its path, the stretch nearest the camera */
function wbWakeTrail(W, t, T) { const X = W.wbTr || (W.wbTr = { slots: [], at: 0, pick: [] }), cam = W.camera.position, V = X.V || (X.V = new TH.Vector3());
  if (t - X.at > 1000) { X.at = t; X.built = 0; const st = wbState(T), step = 15 * 60e3, lim = MOBILE ? 450 : 700, N = MOBILE ? 4 : FX_LITE() ? 6 : 10, held = new Set(X.slots.filter(s => s.id).map(s => s.id)), out = [];
    for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T - 20 * 60e3; tk += step) { const rr = cwRnd(hash("tr" + tk)); if (rr() < .35) continue;
      if (!wbOn("dev", tk) || (wbCycOf("dev", tk) === stCyc(st, "dev") && st.dead.dev && st.dead.dev < tk)) continue;
      const q = wbPos("dev", tk, {}), q2 = wbPos("dev", tk + 60e3, {}), dx = q2.x - q.x, dz = q2.z - q.z, L = Math.hypot(dx, dz) || 1, side = rr() < .5 ? -1 : 1, off = 5 + rr() * 18, p = { x: q.x - dz / L * off * side, y: q.y + (rr() - .5) * 10, z: q.z + dx / L * off * side };
      const ds = Math.hypot(p.x - cam.x, p.y - cam.y, p.z - cam.z); if (ds > (held.has(tk) ? lim * 1.3 : lim)) continue; out.push({ id: tk, p, yaw: Math.atan2(dx, dz) + (rr() - .5) * .9, ds: ds - (held.has(tk) ? 120 : 0) }); }
    out.sort((a, b) => a.ds - b.ds); X.pick = reduced ? [] : out.slice(0, N); }
  const used = new Set();
  for (const pk of X.pick) { let s = X.slots.find(s => s.id === pk.id) || X.slots.find(s => !used.has(s) && !X.pick.some(q => q.id === s.id));
    if (!s && X.slots.length < (MOBILE ? 4 : FX_LITE() ? 6 : 10) && !X.built) { X.built = 1; const kinds = ["battleship", "flagship", "destroyer", "dreadnought", "escortCarrier", "lancer", "supercarrier", "bastion", "corvette", "battleship"]; s = wakeHull(W, kinds[X.slots.length % kinds.length], true, 101 + X.slots.length * 37); X.slots.push(s); }
    if (!s) continue; used.add(s); s.id = pk.id; const heat = clamp(1 - (T - pk.id) / (12 * 3600e3), .15, 1);
    s.holder.visible = true; s.holder.position.set(pk.p.x, pk.p.y, pk.p.z); s.holder.updateMatrixWorld();
    s.g.rotation.set(s.e[0] + T * s.s[0], pk.yaw + s.e[1] + T * s.s[1], s.e[2] + T * s.s[2]); s.g.scale.setScalar(s.k);
    wreckTick(s, t, T, v => s.holder.worldToLocal(v)); s.g.updateMatrix();
    s.fl.forEach((lp, k) => { if (k / s.fl.length > heat + .2) { s.fires[k].visible = false; return; } fireTick(s.fires[k], t, V.copy(lp).applyMatrix4(s.g.matrix), Math.min(2.6, s.fs * s.k * (.35 + .3 * heat))); }); }
  for (const s of X.slots) if (!used.has(s)) { s.holder.visible = false; s.id = null; } }
function wbScarFx(W, t, T) {
  try { wbWrecks(W, t, T); } catch (e) { mapErr(e); } // v415
  try { wbWakeTrail(W, t, T); } catch (e) { mapErr(e); } // v421""")
t = t.replace("const GAME_V = 420;", "const GAME_V = 421;")
open(p, "w").write(t); print("ok")
