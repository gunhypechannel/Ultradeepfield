/* ---------- v384 World Bosses: the Pyramid Overlord (shielded by four Energy Conduits), the Orbital Devourer and the Void Warden ----------
   One shared record (event/wboss) holds each boss's hull as 40 sections, who tore off how many, and who struck the final blow. Every
   Monday 18:00 UTC they all return at full strength in new places: the Overlord beside a pyramid station in the middle layers with its
   conduits around it, the Warden deep in layer 5, the Devourer roaming its own path. Any fleet can attack: win or lose, every section
   it destroys pays a bounty, and when a boss falls everyone who hurt it that week claims a share of the spoils. The models are built in
   code (BOSS3D, from the owner's reference art); the map uses the light build, the battle report the full one. */
const WB_SCAR_MS = 48 * 3600e3, WB_SEG = 40, WB_K = 60, WB_BASE = EV_BASE + 3 * 864e5;
const WB = {
  ovl: { k: "wbOvl", n: "Pyramid Overlord", ic: "▲", col: "#c58bff", hp: 240000, atk: 170000, m3: "overlord", sc: 1, bounty: { m: 60000, c: 40000, g: 18000 }, sh: 3, kill: 14, where: "Pyramid station",
    d: "A walking pyramid fortress. Four Energy Conduits feed its shield: while all four stand, it takes only a quarter of the damage." },
  dev: { k: "wbDev", n: "Orbital Devourer", ic: "✺", col: "#b45cff", hp: 300000, atk: 210000, m3: "devourer", sc: .9, bounty: { m: 72000, c: 48000, g: 22000 }, sh: 3, kill: 16, where: "Roaming",
    d: "A world-eater that never stops moving. It roams the galaxy on its own path, so catch it where it is." },
  war: { k: "wbWar", n: "Void Warden", ic: "◎", col: "#9a6bff", hp: 70000, atk: 80000, m3: "warden", sc: 1.1, bounty: { m: 40000, c: 28000, g: 12000 }, sh: 2, kill: 10, where: "Deep layers",
    d: "A void core caged in plated rings and horned crescents. It guards the deep layers near the Core." } };
for (let i = 0; i < 4; i++) WB["c" + i] = { k: "wbCon", n: "Energy Conduit", ic: "◆", col: "#d9a0ff", hp: 40000, atk: 32000, m3: "conduit", sc: .5, con: i, bounty: { m: 24000, c: 16000, g: 7000 }, sh: 1, kill: 4, where: "Overlord's shield",
  d: "One of four crystal pylons feeding the Pyramid Overlord's shield. Destroy it to weaken the Overlord." };
const WB_ATK = { ovl: ["beam", "stomp", "summon"], dev: ["bite", "lash", "beam", "roar"], war: ["pulse", "beam", "summon"], c0: ["discharge", "charge"] };
const wbMoves = key => WB_ATK[key] || WB_ATK.c0;
for (const [k, u] of [["wbOvl", WB.ovl], ["wbDev", WB.dev], ["wbWar", WB.war], ["wbCon", WB.c0]]) { const hull = Math.round(u.hp * WB_K / WB_SEG); AL[k] = { n: u.n, atk: Math.round(u.atk / WB_SEG), sh: Math.round(hull * .05), hull, val: hull * 2 }; }
const isWbU = k => typeof k === "string" && k.startsWith("wb") && !!AL[k];
const wbCyc = T => Math.floor((T - WB_BASE) / WEEK), wbEnd = c => WB_BASE + (c + 1) * WEEK;
let WB_PYR = null;
function wbHome(c) { if (!WB_PYR) { WB_PYR = PYRAMIDS.filter(y => { const n = layerOf(y.r).n; return n === 3 || n === 4; }); if (!WB_PYR.length) WB_PYR = PYRAMIDS.slice(); }
  const L5 = LAYERS[4]; return { y: WB_PYR[hash("ovl" + c) % WB_PYR.length], wr: (L5.r0 + L5.r1) / 2, wa: (hash("war" + c) % 6283) / 1000 }; }
const WB_OFF = { c0: [26, 0], c1: [-26, 0], c2: [0, 26], c3: [0, -26] }; // the conduits stand round the Overlord, in its own frame (outward, along the orbit)
const WBQ = {}, WBS = {}; // scratch: WBS only inside wbPos (the station), WBQ for callers
function wbPos(key, T, out) { const o = out || {}, c = wbCyc(T), H = wbHome(c);
  if (key === "dev") { const w = T / 864e5, r = MAP_R * (.42 + .22 * Math.sin(w * .9 + c)), a = c * 1.7 + w * TAU / 2.2; o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 6 * Math.sin(w * 3); return o; }
  if (key === "war") { const a = H.wa + TAU * T / period(H.wr); o.x = Math.cos(a) * H.wr; o.z = Math.sin(a) * H.wr; o.y = 0; return o; }
  const q = P3(H.y, T, WBS), r = Math.hypot(q.x, q.z) || 1, ux = q.x / r, uz = q.z / r; o.x = q.x + ux * 16; o.z = q.z + uz * 16; o.y = q.y + 2; // the Overlord stands just outside its station
  if (WB[key].con != null) { const f = WB_OFF[key]; o.x += ux * f[0] - uz * f[1]; o.z += uz * f[0] + ux * f[1]; }
  return o; }
const WBO = {}; for (const key in WB) WBO[key] = { id: "wb_" + key, kind: "wboss", wb: key, lvl: 25, get name() { return WB[key].n; }, mv: (T, out) => wbPos(key, T, out),
  get r() { const q = wbPos(key, now(), {}); return Math.hypot(q.x, q.z); }, get a0() { const T = now(), q = wbPos(key, T, {}), r = Math.hypot(q.x, q.z); return Math.atan2(q.z, q.x) - TAU * T / period(r); } };
const wbById = id => typeof id === "string" && id.startsWith("wb_") ? WBO[id.slice(3)] || null : null;
/* the shared record, normalised for this week (a missing or older record means every boss at full hull) */
G.wb = null; let WBN = null, WBN_SRC = undefined;
function wbNorm(d, c) { const o = d && d.cyc === c ? d : { cyc: c, hp: {}, dmg: {}, dead: {}, last: {}, scar: d && Array.isArray(d.scar) ? d.scar : [] }; o.hp = o.hp || {}; o.scar = Array.isArray(o.scar) ? o.scar.filter(s => s && now() - s.at < WB_SCAR_MS).slice(-60) : []; o.dmg = o.dmg || {}; o.dead = o.dead || {}; o.last = o.last || {};
  for (const k in WB) { o.hp[k] = o.hp[k] == null ? WB_SEG : clamp(Math.round(+o.hp[k] || 0), 0, WB_SEG); } return o; }
function wbState(T = now()) { const src = G.mode === "online" ? G.wb : ((S && S.ldb) || {})["event/wboss"] || null, c = wbCyc(T);
  if (!WBN || WBN.cyc !== c || WBN_SRC !== src) { WBN = wbNorm(src && src.cyc === c ? jcopy(src) : null, c); WBN_SRC = src; } return WBN; }
const wbHp = (k, T) => wbState(T).hp[k] | 0, wbAlive = (k, T) => wbHp(k, T) > 0;
const wbCons = T => [0, 1, 2, 3].filter(i => wbAlive("c" + i, T)).length, wbShield = T => 1 + .75 * wbCons(T);
const wbSegLoot = key => { const b = WB[key].bounty; return { m: Math.round(b.m / 4), c: Math.round(b.c / 4), g: Math.round(b.g / 4) }; };
/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */
async function wbResolve(f) {
  G.resolving.add(f.id); const key = f.wb, D = WB[key], T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(x => x !== f); };
  try {
    if (!D) return home(); const at = f.arrive, c = wbCyc(at), ref = adb().doc("event/wboss");
    for (let i = 0; i < 8; i++) { const r = await ref.acquire({ holder: G.me, ttlMs: 15000 }); if (r.acquired) break; await sleep(1500); }
    const snap = await ref.get(), cur = wbNorm(snap.exists ? snap.data() : null, c), n0 = cur.hp[key] | 0;
    if (!n0) { note(`The ${D.n} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
    const shK = key === "ovl" ? 1 + .75 * [0, 1, 2, 3].filter(i => (cur.hp["c" + i] | 0) > 0).length : 1, mine0 = Object.assign({}, f.n);
    const res = simulate(stacksOf(f.n, techOf(null), G.me), stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"));
    const left = clamp(Math.round(((res.dLeft || {})[D.k]) || 0), 0, n0), seg = n0 - left;
    { const q = wbPos(key, at, {}); cur.scar.push({ k: key, at, x: Math.round(q.x * 10) / 10, y: Math.round(q.y * 10) / 10, z: Math.round(q.z * 10) / 10, b: left ? 0 : 1 }); cur.scar = cur.scar.slice(-60); } // wreckage stays 48 h
    cur.hp[key] = left; const dm = cur.dmg[key] = cur.dmg[key] || {}; if (seg) dm[G.me] = (dm[G.me] || 0) + seg; if (!left) { cur.dead[key] = at; cur.last[key] = G.me; }
    await ref.set(cur); if (G.mode === "online") G.wb = cur; WBN = null;
    const rep = mkRep({ at, kind: "attack", title: `Assault on the ${D.n}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: D.n, wb: key, wbSh: shK, wbSeg: [n0, left], lvl: 25, ptype: "gas", fortL: 0, alien: true,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));
    if (seg) { const per = wbSegLoot(key), L = { m: per.m * seg, c: per.c * seg, g: per.g * seg }, ratio = Math.min(1, cargoOf(f.n) / Math.max(1, total(L)));
      rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = Math.max(1, Math.round(seg * D.sh / 4)); S.shards = (S.shards || 0) + sh; rep.shards = sh; evPts("hunt", seg * 40); S.wins++;
      logReward(`Boss bounty · ${D.n}`, rep.loot, { shards: sh, kind: "battle" }); }
    if (!left) { bump("bosses"); note(`We brought down the ${D.n}! Everyone who fought it this week can claim the spoils.`, "win"); }
    else note(seg ? `Our fleet tore ${Math.round(seg / WB_SEG * 100)}% of the ${D.n}'s hull away (${Math.round(left / WB_SEG * 100)}% left)${rep.loot ? `. Bounty: ${fmt(rep.loot.m)} metal, ${fmt(rep.loot.c)} crystal, ${fmt(rep.loot.g)} gas on the way home, plus ◆${rep.shards}` : ""}.` : `The ${D.n} shrugged off our attack.`, seg ? "win" : "loss");
    addReport(rep); wbFight(key, seg, !left); wbClaim(); home();
  } catch (e) { note("Lost contact with the boss fight. Fleet returning.", "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); }
}
/* a boss fell: everyone who hurt it this week claims once (a share of shards and an item; top damage a Teleport Ticket; the final blow one more item) */
function wbClaim() { if (!S || !G.ready) return; const st = wbState(), c = st.cyc; S.wbGot = S.wbGot || {};
  for (const id in S.wbGot) if (+id.split(":")[0] < c - 1) delete S.wbGot[id];
  for (const key in WB) { const dm = st.dmg[key] || {}, my = dm[G.me] || 0, id = c + ":" + key; if (st.hp[key] > 0 || !my || S.wbGot[id]) continue; S.wbGot[id] = 1;
    const D = WB[key], tot = Object.values(dm).reduce((a, b) => a + b, 0) || 1, share = my / tot, sh = Math.max(2, Math.round(D.kill * Math.min(1, share * 3))), it = DROPS[(Math.random() * DROPS.length) | 0];
    S.shards = (S.shards || 0) + sh; giveItem(it); let extra = "";
    if (D.con == null && Object.entries(dm).sort((a, b) => b[1] - a[1])[0][0] === G.me) { giveItem("teleport"); extra += ", a Teleport Ticket for top damage"; }
    if (st.last[key] === G.me) { const it2 = DROPS[(Math.random() * DROPS.length) | 0]; giveItem(it2); extra += `, ${SHOP[it2].n} for the final blow`; }
    if (D.con == null) { const rn = cubeRunes(25); if (rn) grantRunes(rn, `${D.n} core`); }
    logReward(`Boss defeated · ${D.n}`, null, { shards: sh, item: it, kind: "battle" });
    note(`The ${D.n} has fallen! Your share (${Math.round(share * 100)}% of the damage): ◆${sh} and ${SHOP[it].n}${extra}.`, "win"); dirty(); } }
/* someone else hit a boss (the shared record changed): it reacts on the map */
let WB_PREV = null;
function wbSeen(d) { try { const st = wbNorm(d ? jcopy(d) : null, wbCyc(now())); if (WB_PREV && WB_PREV.cyc === st.cyc) for (const k in WB) if (st.hp[k] < WB_PREV.hp[k]) wbFight(k, WB_PREV.hp[k] - st.hp[k], !st.hp[k]); WB_PREV = st; } catch (e) {} }
/* ---------- the bosses on the map ---------- */
const WB_ENV = new WeakMap();
function wbEnv(R) { let e = WB_ENV.get(R); if (e) return e; const es = new TH.Scene(); es.background = new TH.Color(0x08080b);
  for (let i = 0; i < 9; i++) { const m = new TH.Mesh(new TH.SphereGeometry(4, 12, 8), new TH.MeshBasicMaterial({ color: [0x9a9aa0, 0x8a7a68, 0x3a2266, 0x6a6e80][i % 4] })); const a = i * .7; m.position.set(Math.cos(a) * 30, (i % 3 - 1) * 15, Math.sin(a) * 30); es.add(m); }
  const pm = new TH.PMREMGenerator(R); e = pm.fromScene(es, .04).texture; pm.dispose(); es.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); WB_ENV.set(R, e); return e; }
function wbFight(key, seg, dead) { const W = G3, M = W && W.wbM && W.wbM[key]; if (!M) return; const mv = wbMoves(key);
  M.b.act(mv[0]); setTimeout(() => { try { M.b.act("hit"); } catch (e) {} }, 900); if (mv[1]) setTimeout(() => { try { M.b.act(mv[1]); } catch (e) {} }, 2600);
  if (seg && W.bursts) { const q = P3(WBO[key], now()); W.bursts.push({ p: new TH.Vector3(q.x, q.y + 12 * WB[key].sc, q.z), t: performance.now(), col: WB[key].col, txt: dead ? `${WB[key].n} destroyed!` : `−${Math.round(seg / WB_SEG * 100)}% hull` }); } }
function wbMapFx(W, t, T) {
  if (typeof BOSS3D === "undefined") return; const st = wbState(T), cp = W.camera.position; W.wbM = W.wbM || {};
  for (const key in WB) { const D = WB[key], alive = st.hp[key] > 0, q = P3(WBO[key], T, WBQ), d = Math.hypot(q.x - cp.x, q.y - cp.y, q.z - cp.z), near = alive && d < 1400; let M = W.wbM[key];
    if (!M) { if (!near || W.wbBuilt === t) continue; W.wbBuilt = t; try { BOSS3D.init(TH); BOSS3D.lod = 1; const b = BOSS3D.prep(BOSS3D[D.m3](), wbEnv(W.renderer)); b.grp.scale.setScalar(D.sc * 1.6); W.scene.add(b.grp); M = W.wbM[key] = { b, next: t + 4000 + Math.random() * 6000, q: new TH.Vector3() }; } catch (e) { W.wbM[key] = M = { b: null }; } }
    if (!M.b) continue; const g = M.b.grp; g.visible = near; if (!near) continue;
    g.position.set(q.x, q.y, q.z);
    if (key === "dev") { const q2 = wbPos("dev", T + 60000, {}); g.rotation.y = -Math.atan2(q2.z - q.z, q2.x - q.x); } else if (key === "war") g.rotation.y = t * 4e-5; else g.rotation.y = Math.atan2(-q.x, -q.z); // the Overlord and its conduits face the Core
    if (t > M.next) { M.next = t + 9000 + Math.random() * 10000; const m = M.b.moves.filter(x => x !== "hit" && x !== "link"); M.b.act(m[(Math.random() * m.length) | 0]); } // alive: a move every few seconds
    if (D.con != null) { const on = st.hp.ovl > 0; M.b.feed = on ? 1 : 0; if (on) { const tq = P3(WBO.ovl, T, {}), s = g.scale.x, lk = M.b.link; // the feed beam runs to the Overlord's crown
      const dx = tq.x - q.x, dz = tq.z - q.z, dy = (tq.y + 5 * WB.ovl.sc * 1.6) - (q.y + 9 * s), yaw = Math.atan2(dz, dx); lk.rotation.set(0, -yaw - g.rotation.y, Math.atan2(dy, Math.hypot(dx, dz))); lk.userData.len = Math.hypot(dx, dy, dz) / s; } }
    if (M.sweep && !(G.wbScan && G.wbScan.key === key)) M.sweep.visible = false; M.b.tick(t); }
  try { wbScanFx(W, t); wbScarFx(W, t, T); } catch (e) {}
  if (!W.wbComp && Object.keys(W.wbM).length === Object.keys(WB).length) { W.wbComp = 1; try { W.renderer.compile(W.scene, W.camera); } catch (e) {} } } // all built (one a frame, usually during the background map build): compile their shaders now, not on first sight
function wbMapFree(W) { if (!W || !W.wbM) return; for (const k in W.wbM) { const M = W.wbM[k]; if (!M.b) continue; W.scene.remove(M.b.grp); M.b.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); }); } W.wbM = {}; }
/* ---------- the boss in the battle report: the full model, rendered live into the replay ---------- */
const WBR = {}; const WB_FRONT = { overlord: 0, devourer: -Math.PI / 2, warden: 0, conduit: 0 }; const WB_VIEW = { overlord: [-Math.PI / 2, [-10, 4, 32], [0, -1.5, 0]], devourer: [Math.PI, [-8, 7, 36], [3, 0, 0]], warden: [-Math.PI / 2, [-7, 3, 27], [0, 0, 0]], conduit: [0, [0, 6, 25], [0, 6, 0]] };
function wbArt(key, w, h, t, b) { if (typeof BOSS3D === "undefined" || !WB[key]) return null;
  try { if (!WBR.r) { const cv = document.createElement("canvas"); WBR.r = new TH.WebGLRenderer({ canvas: cv, alpha: true, antialias: true }); WBR.r.setPixelRatio(1); WBR.r.outputEncoding = TH.sRGBEncoding; WBR.r.toneMapping = TH.ACESFilmicToneMapping; WBR.r.toneMappingExposure = 1.1; WBR.r.setClearColor(0, 0);
      WBR.sc = new TH.Scene(); WBR.sc.add(new TH.AmbientLight(0x5f6a8a, .3)); const d0 = new TH.DirectionalLight(0xfff0e6, 2.1); d0.position.set(-6, 8, 10); WBR.sc.add(d0); const d1 = new TH.DirectionalLight(0x8a50ff, 1.2); d1.position.set(10, 4, -8); WBR.sc.add(d1); WBR.cam = new TH.PerspectiveCamera(36, 2, .1, 500); }
    if (WBR.key !== key) { if (WBR.b) { WBR.sc.remove(WBR.b.grp); WBR.b.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); }); } BOSS3D.init(TH); BOSS3D.lod = MOBILE ? 2 : 0; const m3 = WB[key].m3, V0 = WB_VIEW[m3], tall = h > w * .75; // phones: simpler tentacles; a portrait replay has the attackers above, so the boss faces the camera
      WBR.b = BOSS3D.prep(BOSS3D[m3](), wbEnv(WBR.r)); WBR.b.grp.rotation.y = tall ? WB_FRONT[m3] : V0[0]; WBR.sc.add(WBR.b.grp); WBR.key = key; WBR.tall = tall; WBR.cam.position.set(...(tall ? [V0[1][0] * .2, V0[1][1] * .6, Math.hypot(V0[1][0], V0[1][2])] : V0[1])); WBR.cam.lookAt(new TH.Vector3(...V0[2])); WBR.hp = null; WBR.next = 0; }
    const W2 = Math.min(MOBILE ? 820 : 1100, Math.round(w)), H2 = Math.round(W2 * h / w); if (WBR.w !== W2 || WBR.h !== H2) { WBR.r.setSize(W2, H2, false); WBR.cam.aspect = W2 / H2; WBR.cam.updateProjectionMatrix(); WBR.w = W2; WBR.h = H2; }
    if (b) { if (WBR.hp != null && b.hp < WBR.hp - .004 && t > (WBR.hitT || 0)) { WBR.b.act("hit"); WBR.hitT = t + 700; } WBR.hp = b.hp;
      if (b.live && t > WBR.next) { WBR.next = t + 2400 + Math.random() * 1400; const m = wbMoves(key); WBR.b.act(m[(Math.random() * m.length) | 0]); } }
    WBR.b.tick(t); WBR.r.render(WBR.sc, WBR.cam); return WBR.r.domElement; } catch (e) { return null; } }
function wbArtFree() { if (!WBR.r) return; try { if (WBR.b) WBR.b.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); }); const e = WB_ENV.get(WBR.r); if (e) e.dispose(); WBR.r.dispose(); WBR.r.forceContextLoss(); } catch (e) {} for (const k in WBR) delete WBR[k]; }
/* ---------- the boss card ---------- */
function shWboss() {
  const key = sheet.id, D = WB[key], O = WBO[key]; if (!D) return ""; const T = now(), st = wbState(T), hp = st.hp[key] | 0, pc = Math.round(hp / WB_SEG * 100), h = originPlanet(), avail = originAvail(), sel = selected(), end = wbEnd(st.cyc);
  const sent = S.fleets.some(f => f.wb === key && f.phase === "out"), my = (st.dmg[key] || {})[G.me] || 0, per = wbSegLoot(key), L = layerOf(O.r);
  const shield = key === "ovl" ? `<dt>Shield</dt><dd>${wbCons(T) ? `${wbCons(T)}/4 conduits · ${Math.round(100 / wbShield(T))}% damage` : "Down"}</dd>` : "";
  let body = "";
  if (!hp) body = `<p class="note">Defeated this week. It returns at full strength in <b data-end="${end}">${ftime(end - T)}</b>.</p>`;
  else if (!canPlay()) body = `<p class="note">${G.mode === "connecting" ? connNote() : "You can only watch this galaxy."}</p>`;
  else if (sent) body = `<p class="note">Our fleet is on its way.</p>`;
  else if (!Object.keys(avail).length) body = `${originBar()}<p class="note">No ships at ${esc(h ? h.name : S.homeName)}.</p>`;
  else body = `<h2 class="sec">Attack</h2>${originBar()}${picker(avail)}${speedBar(O, sel)}    <button class="btn wide amber" data-act="wbGo" data-id="${key}" ${Object.keys(sel).length && !slotsFull() ? "" : "disabled"}>⚔ Attack the ${esc(D.n)}</button>`;
  const lead = Object.entries(st.dmg[key] || {}).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([u, v], i) => `<li><span>${i + 1}. ${esc(u === G.me ? "You" : nameOf(u))}</span><b>${Math.round(v / WB_SEG * 100)}%</b></li>`).join("");
  const cons = key === "ovl" ? `<h2 class="sec">Energy Conduits</h2><div class="list">${[0, 1, 2, 3].map(i => { const c = "c" + i, ch = st.hp[c] | 0; return `<button class="tgt" data-act="wboss" data-id="${c}"><span class="lvl" style="color:${WB[c].col};border-color:${WB[c].col}">◆</span><span><span class="nm">Energy Conduit ${"ABCD"[i]}</span><br><span class="sub">${ch ? `${Math.round(ch / WB_SEG * 100)}% hull · feeding the shield` : "Destroyed"}</span></span><span class="pill ${ch ? "bad" : "wait"}">${ch ? "Attack" : "Down"}</span></button>`; }).join("")}</div>` : "";
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${D.col}">World boss · ${D.where}</div><h2>${D.ic} ${esc(D.n)}</h2><p class="note">${D.d}</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="wbhp"><div class="wbbar"><i style="width:${pc}%;background:${D.col}"></i></div><span>${hp ? `${pc}% hull · ${fmt(Math.round(hp / WB_SEG * D.hp))} / ${fmt(D.hp)} HP` : "DEFEATED"}</span></div>
    <dl class="kv">${shield}<dt>Location</dt><dd>[${coordStr(O)}] · L${L.n} ${L.name}</dd>${h && hp ? `<dt>Flight from ${esc(h.name)}</dt><dd>${ftime(travelMs(h, O, { fighter: 1 }))}</dd>` : ""}
      <dt>Bounty per 2.5% hull</dt><dd>${costHTML(per)} + ◆</dd><dt>Your damage this week</dt><dd>${my ? Math.round(my / WB_SEG * 100) + "%" : "None yet"}</dd><dt>Returns</dt><dd>Mondays 18:00 UTC</dd></dl>
    <p class="note">Every bit of hull you destroy pays its bounty, win or lose. When it falls, everyone who damaged it this week claims Void Shards and an item${D.con == null ? ", and the top damage dealer wins a Teleport Ticket" : ""}. It returns every Monday at full strength, in a new place.</p>
    ${lead ? `<h2 class="sec">Top damage</h2><ol class="wblead">${lead}</ol>` : ""}${cons}${hp ? cineBtn(O.id) : ""}${body}`; }

/* ---------- destruction on the map: every fight leaves wreckage where it happened, and each boss leaves a mark wherever it has been
   (the Devourer every 3 hours along its path, the others every 4), burning hot at first and decaying away over 48 hours ---------- */
function wbScars(T) { const st = wbState(T), out = [];
  for (const s of st.scar || []) if (T - s.at < WB_SCAR_MS && T >= s.at) out.push(s);
  for (const key of ["ovl", "dev", "war"]) { const step = (key === "dev" ? 3 : 4) * 3600e3;
    for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T; tk += step) { if (wbCyc(tk) === st.cyc && st.dead[key] && st.dead[key] < tk) continue; const q = wbPos(key, tk, {}); out.push({ k: key, at: tk, x: q.x, y: q.y, z: q.z, a: 1 }); } }
  return out; }
function wbScarFx(W, t, T) {
  let X = W.wbScar; if (!X) { const N = 1400, P = 4200;
    const mesh = new TH.InstancedMesh(new TH.IcosahedronGeometry(1, 0), new TH.MeshStandardMaterial({ color: 0xffffff, roughness: .75, metalness: .55, flatShading: true, envMap: wbEnv(W.renderer), envMapIntensity: .6 }), N); mesh.count = 0; mesh.frustumCulled = false;
    mesh.instanceColor = new TH.InstancedBufferAttribute(new Float32Array(N * 3), 3); W.scene.add(mesh);
    const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(P * 3), 3)); g.setAttribute("color", new TH.BufferAttribute(new Float32Array(P * 3), 3)); g.setDrawRange(0, 0);
    const dot = (() => { const c = document.createElement("canvas"); c.width = c.height = 64; const x = c.getContext("2d"), gr = x.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(.35, "rgba(255,255,255,.45)"); gr.addColorStop(1, "rgba(255,255,255,0)"); x.fillStyle = gr; x.fillRect(0, 0, 64, 64); return new TH.CanvasTexture(c); })();
    const pts = new TH.Points(g, new TH.PointsMaterial({ size: 13, map: dot, vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); pts.frustumCulled = false; W.scene.add(pts);
    X = W.wbScar = { mesh, pts, N, P, at: 0, m4: new TH.Matrix4(), q: new TH.Quaternion(), e: new TH.Euler(), v: new TH.Vector3(), s: new TH.Vector3() }; }
  X.pts.material.opacity = .75 + .25 * Math.sin(t * .003);
  if (t - X.at < 5000) return; X.at = t; // decay is slow: refresh every 5 s
  const L = wbScars(T), pos = X.pts.geometry.attributes.position.array, col = X.pts.geometry.attributes.color.array, ic = X.mesh.instanceColor.array; let n = 0, p = 0;
  for (const s of L) { const r = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647)(1 + hash(s.k + ":" + s.at) % 2147483646), age = clamp((T - s.at) / WB_SCAR_MS, 0, 1), fade = 1 - age, heat = clamp(1 - (T - s.at) / (6 * 3600e3), 0, 1);
    const R = s.b ? 34 : s.a ? 14 : 20, nc = s.b ? 30 : s.a ? 7 : 15, ne = s.b ? 90 : s.a ? 26 : 50, hot = WB[s.k] && s.k === "dev" ? [1, .35, .9] : [1, .5, .18];
    for (let i = 0; i < nc && n < X.N; i++, n++) { const a = r() * TAU, d = Math.sqrt(r()) * R, sc = (.8 + r() * (s.b ? 4.5 : 2.6)) * (.3 + .7 * fade);
      X.v.set(s.x + Math.cos(a) * d, s.y + (r() - .5) * 5, s.z + Math.sin(a) * d); X.q.setFromEuler(X.e.set(r() * TAU, r() * TAU, r() * TAU)); X.s.set(sc, sc * (.4 + r() * .7), sc * (.6 + r() * .8)); X.m4.compose(X.v, X.q, X.s); X.mesh.setMatrixAt(n, X.m4);
      const k = .1 + .12 * r(), hh = heat * r() * .35; ic[n * 3] = k + hh; ic[n * 3 + 1] = k * .92 + hh * .3; ic[n * 3 + 2] = k * 1.1 + hh * .1; } // charred hull plates; fresh ones still glowing at the edges
    for (let i = 0; i < ne && p < X.P; i++, p++) { const ring = i % 3 === 0, a = r() * TAU, d = ring ? R * (1.05 + r() * .25) : Math.sqrt(r()) * R * 1.1, b = (ring ? .6 : 1.2) * (.3 + .7 * fade) * (.55 + .45 * heat) * (.5 + r() * .5);
      pos[p * 3] = s.x + Math.cos(a) * d; pos[p * 3 + 1] = s.y + (r() - .5) * (ring ? 1 : 6); pos[p * 3 + 2] = s.z + Math.sin(a) * d;
      const c = ring ? [.55, .3, 1] : heat > .05 ? hot : [.6, .35, 1]; col[p * 3] = c[0] * b; col[p * 3 + 1] = c[1] * b; col[p * 3 + 2] = c[2] * b; } }
  X.mesh.count = n; X.mesh.instanceMatrix.needsUpdate = true; X.mesh.instanceColor.needsUpdate = true; X.pts.geometry.setDrawRange(0, p); X.pts.geometry.attributes.position.needsUpdate = true; X.pts.geometry.attributes.color.needsUpdate = true; }
/* ---------- the scan: a boss's own cinematic. The camera circles and dollies while a sensor sweep passes over the hull, the boss shows
   each of its moves in turn, and an analysis readout builds up beside it ---------- */
const WB_YR = { overlord: [-8, 7], devourer: [-6, 6], warden: [-7, 7], conduit: [0, 12.5] };
const WB_MOVE_N = { walk: "Walk", beam: "Beam", stomp: "Stomp", summon: "Surge", bite: "Bite", lash: "Tentacle lash", roar: "Roar", pulse: "Void pulse", charge: "Charge", discharge: "Discharge", link: "Shield feed" };
const WB_INTEL = { ovl: ["Siege walker · monumental", "Its shield runs on four conduits. Destroy them first.", "EXTREME"], dev: ["Roaming world-eater", "The maw is exposed while it gapes to fire.", "EXTREME"],
  war: ["Void sentinel · deep layers", "The core flares just before each pulse.", "SEVERE"], con: ["Power pylon", "The crystal overheats while it charges.", "MODERATE"] };
function wbScanOn(key) { const D = WB[key]; if (!D) return; wbScanOff(); const I = WB_INTEL[D.con != null ? "con" : key], el = document.createElement("div"); el.id = "wbscan"; el.style.setProperty("--sc", D.col);
  el.innerHTML = `<i class="ws-c tl"></i><i class="ws-c tr"></i><i class="ws-c bl"></i><i class="ws-c br"></i><i class="ws-line"></i><i class="ws-ret"></i>
    <div class="ws-card"><small>SCANNING · WORLD BOSS</small><b>${D.ic} ${esc(D.n)}</b><dl>
      <div style="--d:.4s"><dt>Class</dt><dd>${I[0]}</dd></div><div style="--d:.9s"><dt>Hull</dt><dd id="wsHull">…</dd></div>${key === "ovl" ? `<div style="--d:1.4s"><dt>Shield</dt><dd id="wsSh">…</dd></div>` : ""}
      <div style="--d:1.9s"><dt>Firepower</dt><dd>${fmt(D.atk)} per round</dd></div><div style="--d:2.4s"><dt>Threat</dt><dd class="ws-th">${I[2]}</dd></div>
      <div style="--d:2.9s"><dt>Weak point</dt><dd>${I[1]}</dd></div><div style="--d:3.4s"><dt>Observed</dt><dd id="wsMv">…</dd></div></dl></div>`;
  $("#app").appendChild(el); G.wbScan = { key, t0: performance.now(), seen: [], next: 0, i: 0 }; wbScanTick(); }
function wbScanOff() { const el = $("#wbscan"); if (el) el.remove(); G.wbScan = null; }
function wbScanTick() { const s = G.wbScan; if (!s) return; const st = wbState(), hp = st.hp[s.key] | 0, a = $("#wsHull"), b = $("#wsSh"), m = $("#wsMv");
  if (a) a.textContent = hp ? `${Math.round(hp / WB_SEG * 100)}% · ${fmt(Math.round(hp / WB_SEG * WB[s.key].hp))} HP` : "Destroyed"; if (b) b.textContent = wbCons() ? `Up · ${wbCons()}/4 conduits` : "Down";
  if (m) m.textContent = s.seen.length ? s.seen.map(k => WB_MOVE_N[k] || k).join(" · ") : "Watching…"; }
setInterval(() => { try { if (G.wbScan && !(G3 && G3.cam.cineObj && G3.cam.cineObj.id === "wb_" + G.wbScan.key)) wbScanOff(); else wbScanTick(); } catch (e) {} }, 500);
function wbScanFx(W, t) { const s = G.wbScan, M = s && W.wbM && W.wbM[s.key]; if (!M || !M.b) return; const g = M.b.grp, c = W.cam;
  if (!M.sweep) { const sw = new TH.Group(), R = M.b.r * 1.15; sw.add(new TH.Mesh(new TH.CylinderGeometry(R, R, .25, 64, 1, true), new TH.MeshBasicMaterial({ color: 0x9ff3ff, transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })));
    sw.add(new TH.Mesh(new TH.CylinderGeometry(R, R, 2.6, 64, 1, true), new TH.MeshBasicMaterial({ color: 0x5fd8ff, transparent: true, opacity: .12, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false }))); M.sweep = sw; M.b.grp.add(sw); }
  const k = ((t - s.t0) % 3600) / 3600, Y = WB_YR[WB[s.key].m3]; M.sweep.visible = true; M.sweep.position.y = Y[0] + k * (Y[1] - Y[0]); M.sweep.children[0].material.opacity = .55 * Math.sin(k * Math.PI);
  if (t > s.next) { s.next = t + 4500; const mv = M.b.moves.filter(x => x !== "hit"), n = mv[s.i++ % mv.length]; M.b.act(n); if (!s.seen.includes(n)) s.seen.push(n); }
  const base = (WB[s.key].con != null ? 45 : 105) * WB[s.key].sc; c.goal = Object.assign(c.goal || {}, { dist: base * (1 + .28 * Math.sin((t - s.t0) * .00035)) }); c.head = (c.head || 0) + .0006 * (W.dtk || 1); } // a slow circle that dollies in and out
