/* ---------- v740 the Resurrection War, part two: the network fights, War Command, the map layer, the Continuum's hulls ---------- */
function cntBossSet(B, st, T) { const s = Math.max(3, Math.min(6, cntStage(T))); let esc;
  if (B.cnt === "rel") esc = { cncor: 2, cnexe: 2 + (s >= 5 ? 1 : 0), cnint: 4 };
  else if (B.cnt === "ark") { const a = st.ark[B.id]; esc = { cnasm: 2, cnexe: 3, cnint: 4 }; if (a.cap > 0) { esc.cnfab = 1; esc.cnint += 3; } if (s >= 6) esc.cndre = 1; }
  else if (B.cnt === "cmd") esc = { cnexe: 3, cncor: 2, cnint: 6, cnasm: s >= 5 ? 1 : 0 };
  else esc = { cndre: 2, cnasm: 2, cnexe: 4, cncor: 2 };
  for (const k in esc) if (!esc[k]) delete esc[k];
  const hp = B.cnt === "rel" ? st.rel[B.id].hp : B.cnt === "ark" ? st.ark[B.id].hp : st.cmd[B.id].hp, Z = cntMods(Object.assign({ [B.u]: 1 }, esc), B);
  return { u: B.u, n0: Math.max(0, hp), esc, mods: Z.m, tac: Z.tac }; }
function cntBossForce(x, T) { T = T || now(); const B = CNT_BOSS[x.id], s = cntBossSet(B, cntStC(T), T); return Object.assign({ [s.u]: Math.max(1, s.n0) }, s.esc); }
/* why a target can't be hit yet, or null */
function cntBlock(B, st, T) { const s = cntStage(T); if (!cntBossOn(B, T)) return `${B.name} isn't in play right now.`;
  if (B.cnt === "rel") { if (s < 4) return `The relays can be attacked from stage 4, Sever the Network.`; if (st.rel[B.id].down) return `${B.name} is down. It rebuilds itself 12 hours after it fell, unless its Ark is destroyed.`; }
  if (B.cnt === "ark") { if (s < 5) return `The Arks can be attacked from stage 5, The Ark Offensive.`; if (st.ark[B.id].dead) return `${B.name} is already destroyed.`; if (cntShield(st, B.reg)) return `${B.name} is shielded while any of its relays stands (${cntRelUp(st, B.reg)} up). Break its relays first.`; }
  if (B.cnt === "cmd" || B.cnt === "eter") { const c = st.cmd[B.id]; if (c.dead) return `${B.name} is gone for good.`; if (c.back > T) return `${B.name} is being rebuilt. Back in ${ftime(c.back - T)}.`; }
  return null; }
async function cntBossResolve(f) { const B = CNT_BOSS[f.xid], x = PB[f.xid]; G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(q => q !== f); };
  try { const at = f.arrive, ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), why = cntBlock(B, cur, at);
    if (why) { note(`${why} Fleet returning, nothing lost.`, "warn"); return home(); }
    const Z = cntBossSet(B, cur, at), n0 = Math.max(1, Z.n0);
    const mkA = () => { const st = stacksOf(f.n, techVs(x), G.me); for (const s of st) { s.atk *= Z.mods.pA; s.sh *= Z.mods.pS; } return st; };
    const mkD = () => { const st = stacksOf(Object.assign({ [Z.u]: n0 }, Z.esc), { mon: B.lvl }, "monster"); for (const s of st) { s.atk *= Z.mods.bA; s.hull *= Z.mods.bH; } return st; };
    const mine0 = Object.assign({}, f.n), { res, rise } = mimRise(mkA, mkD, Z.u, n0, n0);
    const left = clamp(Math.round(((res.dLeft || {})[Z.u]) || 0), 0, n0), seg = n0 - left; let pts = 0, event = "";
    if (seg) { pts = 4 * seg;
      if (B.cnt === "rel") { const r = cur.rel[B.id]; r.hp -= seg; r.dmg[G.me] = (r.dmg[G.me] || 0) + seg; if (r.hp <= 0) { r.hp = 0; r.down = at; cur.rk++; event = "reldown"; } }
      else if (B.cnt === "ark") { const a = cur.ark[B.id]; a.hp -= seg; a.dmg[G.me] = (a.dmg[G.me] || 0) + seg; if (a.hp <= 0) { a.hp = 0; a.dead = at; a.last = G.me; event = "arkdead"; } }
      else { const c = cur.cmd[B.id]; c.hp -= seg; c.dmg[G.me] = (c.dmg[G.me] || 0) + seg;
        if (c.hp <= 0) { if (cntCanRes(cur, B.reg)) { c.hp = B.hp; c.back = at + CNT_BACK; c.res++; if (B.reg >= 0) cur.ark[CNT_ARKS[B.reg][0]].cap--; event = "transfer"; } else { c.hp = 0; c.dead = at; c.last = G.me; event = "dead"; } } } }
    const counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur);
    const rep = mkRep({ at, kind: "attack", simLeft: left, title: `Assault on ${B.name}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: B.name, mon: B.mon, mimB: B.id, mimSeg: [n0, n0 - seg], omRise: rise > 1.01 ? Math.round(rise) : undefined, cntTac: Z.tac,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1); if (rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info");
    if (seg) { const L = { m: 30000 * seg, c: 20000 * seg, g: 10000 * seg }, ratio = Math.min(1, fCargo(f) / Math.max(1, total(L))); rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = 2 * seg, M = cntS(), W = cntWk(M, Math.max(1, Math.min(7, cntStage(at)))); S.shards = (S.shards || 0) + sh; rep.shards = sh; S.wins++; evPts("hunt", seg * 50);
      const mt = { echo: 2 * seg }; if (B.cnt === "rel") { mt.circ = Math.ceil(seg / 3); W.rel += seg; M.kills.rel += seg; } else if (B.cnt === "ark") { mt.cell = Math.ceil(seg / 4); mt.core = Math.floor(seg / 8); W.ark += seg; M.kills.ark += seg; } else { mt.matrix = Math.ceil(seg / 6); if (B.cnt === "eter") W.eter++; }
      if (event === "transfer" || event === "dead") { W.cmd++; M.kills.cmd++; }
      cntAddM(mt); M.pts += counted; rep.cnt = mt; logReward(`${B.name} bounty`, rep.loot, { shards: sh, kind: "battle" }); }
    for (const t of Z.tac) note(`${CNT_TAC[t][0]}: ${CNT_TAC[t][1]}`, "info");
    if (rise > 1.01) note(`${B.name} rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (event === "reldown") note(`${B.name} is down. ${cntRelUp(cur, B.reg) ? `${cntRelUp(cur, B.reg)} relay${cntRelUp(cur, B.reg) > 1 ? "s" : ""} still shield ${CNT_ARKS[B.reg][1]}.` : `${CNT_ARKS[B.reg][1]} has lost its shield. It can be destroyed now.`}`, "win");
    else if (event === "arkdead") { bump("bosses"); note(`${B.name} IS DESTROYED. Its commanders can no longer be rebuilt, and its region's machines are weakened for the rest of the war. Everyone who broke a section can claim the Arkbreaker reward.`, "win"); }
    else if (event === "transfer") note(`${B.name} is destroyed, but its mind reached ${CNT_ARKS[B.reg] ? CNT_ARKS[B.reg][1] : "its Ark"} (Continuity Transfer). It will be rebuilt in 6 hours. Break the relays and the Ark to stop it.`, "warn");
    else if (event === "dead") note(`${B.name} is destroyed, and there was nowhere to send its mind. It is gone for good.`, "win");
    else if (seg) note(`Our fleet broke ${seg} section${seg > 1 ? "s" : ""} off ${B.name}. +${counted} war points${counted < pts ? " (daily cap reached)" : ""}.`, "win");
    else note(`Our fleet couldn't break a section off ${B.name}. Send more firepower.`, "warn");
    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} cntClaim(); home();
  } catch (e) { if (e === CAS_RETRY && await casAgain(f, cntBossResolve)) return; note(`Lost contact with the ${B.name} fight. Fleet returning.`, "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* objectives, war milestones and the Arkbreaker reward: each pays once (a claim key on the account, written before it pays) */
const CNT_OBJ = { 1: [["sig", "Decrypt 3 machine signals (open a patrol's page)", 3, 5, { echo: 20 }], ["pat", "Destroy 3 Continuum patrols", 3, 8, { alloy: 6 }]],
  2: [["plat", "Shut down 3 fabrication platforms", 3, 10, { circ: 4 }], ["pat", "Destroy 4 patrols", 4, 8, { echo: 30 }], ["sig", "Decrypt 2 more signals", 2, 4, { echo: 15 }]],
  3: [["cmd", "Destroy a Continuum commander", 1, 12, { matrix: 2 }], ["scan", "Scan 2 Resurrection Relays (open their pages)", 2, 6, { circ: 4 }], ["plat", "Shut down 3 platforms", 3, 10, { alloy: 8 }]],
  4: [["rel", "Break 10 relay sections", 10, 14, { circ: 6 }], ["scan", "Scan 2 relays", 2, 4, { echo: 20 }], ["pat", "Destroy 4 patrols", 4, 8, { alloy: 8 }]],
  5: [["ark", "Break 10 Ark sections", 10, 18, { core: 2 }], ["rel", "Break 10 relay sections", 10, 12, { cell: 3 }], ["plat", "Shut down 3 platforms", 3, 10, { echo: 40 }]],
  6: [["cmd", "Destroy 2 commanders", 2, 16, { matrix: 3 }], ["ark", "Break 12 Ark sections", 12, 18, { cell: 4 }], ["eter", "Strike the Eternal Commander", 1, 20, { core: 3 }]], 7: [] };
const CNT_MILE = [[25, 6, { echo: 40 }], [50, 10, { alloy: 20 }], [75, 14, { cell: 6 }], [100, 24, { core: 4, matrix: 4 }]];
function cntGrant(r, why) { if (r.sh) S.shards = (S.shards || 0) + r.sh; const mt = {}; for (const k in CNT_MAT) if (r[k]) mt[k] = r[k]; cntAddM(mt); logReward(why, null, { shards: r.sh || 0, kind: "event" }); dirty(); }
function cntClaim() { if (!S || !G.ready) return; const T = now(); if (!cntOn(T) && cntStage(T) !== 8) return; const st = cntStC(T), M = cntS();
  for (const [id, nm] of CNT_ARKS) { const a = st.ark[id], my = a.dmg[G.me] || 0, key = "ark" + id; if (!a.dead || !my || M.got[key]) continue; M.got[key] = 1;
    const tot = Object.values(a.dmg).reduce((p, q) => p + q, 0) || 1, share = my / tot, last = a.last === G.me ? 2 : 0, r = { sh: Math.min(50, 15 + Math.round(share * 60)), core: 2 + Math.round(share * 8) + last, cell: 3 };
    S.medals = S.medals || {}; S.medals.ark = (S.medals.ark || 0) + 1; cntGrant(r, `${nm} destroyed`); note(`${nm} is destroyed. Arkbreaker: ${cntMatTxt(r)} and ◆${r.sh}${last ? ", with the final blow" : ""}.`, "win"); } }
function cntObjN(s, id) { return cntWk(cntS(), s)[id] || 0; }
/* the map layer: a red sector round each Ark, crimson transmission lines from its relays; a destroyed Ark's sector goes dark */
function cntMapTick(W, t, T) { const on = cntOn(T) && cntStage(T) < 7; let X = W.cntL;
  if (!on) { if (X) { W.scene.remove(X.grp); X.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); W.cntL = null; } return; }
  if (!X) { X = W.cntL = { grp: new TH.Group(), sec: [], lines: [], P: {} }; W.scene.add(X.grp); const R = CNT_R();
    CNT_ARKS.forEach(() => { const m = new TH.Mesh(new TH.RingGeometry(R - 34, R + 34, 48, 1, -.45, 1.05), new TH.MeshBasicMaterial({ color: 0xff2236, transparent: true, opacity: .1, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending })); m.rotation.x = -Math.PI / 2; X.grp.add(m); X.sec.push(m); });
    for (const B of CNT_NET) if (B.cnt === "rel") { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(6), 3)); const l = new TH.Line(g, new TH.LineBasicMaterial({ color: 0xff3346, transparent: true, opacity: .7, blending: TH.AdditiveBlending, depthWrite: false })); l.frustumCulled = false; X.grp.add(l); X.lines.push([B, l]); } }
  const st = cntStC(T), s = cntStage(T), q = {}, q2 = {};
  CNT_ARKS.forEach(([id], i) => { const a = st.ark[id], m = X.sec[i], B = CNT_BOSS[id], ang = B.a0 + T * TAU / period(B.r); m.rotation.z = ang; m.material.color.setHex(a.dead ? 0x3fe8f0 : 0xff2236); m.material.opacity = a.dead ? .03 : (s >= 3 ? .1 : .05) * (.85 + .15 * Math.sin(t * .002 + i)); });
  for (const [B, l] of X.lines) { const r = st.rel[B.id], a = st.ark[cntArkOf(B)], vis = s >= 3 && !r.down && !a.dead; l.visible = vis; if (!vis) continue; P3(B, T, q); P3(CNT_BOSS[cntArkOf(B)], T, q2); const p = l.geometry.attributes.position.array; p[0] = q.x; p[1] = q.y + 1; p[2] = q.z; p[3] = q2.x; p[4] = q2.y + 1; p[5] = q2.z; l.geometry.attributes.position.needsUpdate = true; l.material.opacity = .45 + .3 * Math.sin(t * .006 + B.a0 * 9); } }
/* War Command */
function cntBand(T) { if (!cntOn(T)) return ""; const s = cntStage(T), st = cntStC(T); return `<button class="omb cntb" data-act="cntOpen"><b>⬢ WAR ${s}/7</b><span>${CNT_STN[s]} · ${cntWar(st)}%</span></button>`; }
function cntNetRow(st, T, i) { const [id, nm] = CNT_ARKS[i], a = st.ark[id], B = CNT_BOSS[id], up = cntRelUp(st, i), s = cntStage(T), rels = CNT_NET.filter(b => b.cnt === "rel" && b.reg === i), cmds = CNT_NET.filter(b => b.cnt === "cmd" && b.reg === i);
  const relH = rels.map(b => { const r = st.rel[b.id]; return `<i class="${r.down ? "dn" : ""}" title="${esc(b.name)}">${r.down ? "✕" : Math.round(r.hp / b.hp * 100) + "%"}</i>`; }).join("");
  const cmdH = cmds.map(b => { const c = st.cmd[b.id]; return `<span class="${c.dead ? "dn" : c.back > T ? "rb" : ""}">${esc(b.name)}<em>${c.dead ? "gone for good" : c.back > T ? `rebuilt in ${ftime(c.back - T)}` : `${c.res ? `rebuilt ${c.res}×` : "active"}`}</em></span>`; }).join("");
  return `<div class="cntark${a.dead ? " dead" : ""}"><div class="cnth"><b>${esc(nm)}</b><small>${a.dead ? "Destroyed" : `${a.hp}/${B.hp} · ${up ? `shielded by ${up} relay${up > 1 ? "s" : ""}` : "SHIELD DOWN"} · ${a.cap} rebuilds left`}</small>${!a.dead && s >= 3 ? `<button class="btn sm" data-act="cntGo" data-id="${id}">Go</button>` : ""}</div>
    <div class="mimbar cntbar"><i style="width:${a.dead ? 0 : Math.round(a.hp / B.hp * 100)}%"></i></div><div class="cntrel"><small>Relays</small>${relH}</div><div class="cntcmd">${cmdH}</div></div>`; }
const CNT_ART = { cnint: "interceptor", cnexe: "destroyer", cnasm: "c_cruiser", cndre: "c_dreadnought", cnrel: "c_relay", cnark: "ark_side", cnprime: "c_prime", cneter: "c_eternal" };
const CNT_CD = { cnint: ["A fast machine fighter with one red sensor eye. Patrols and first strikes.", "Stage 1"], cncor: ["Electronic warfare: its dishes jam our shields (Signal Jamming).", "Stage 1"], cnexe: ["Heavy energy guns on synchronised mounts (Coordinated Fire).", "Stage 2"],
  cnfab: ["A shipyard that fights: each one launches three more Interceptors (Drone Fabrication).", "Stage 2"], cnasm: ["Salvage arms and neural processors; it patches its allies (Repair Swarm).", "Stage 4"], cndre: ["A wedge of armour around a crimson reactor that pulses when it dies (Neural Overload).", "Stage 6"],
  cnrel: ["A neural transmission tower that links commanders to their Ark.", "Stage 3"], cnark: ["Reconstruction chambers and fabrication bays: it rebuilds the dead.", "Stage 3"], cneter: ["The elite commander: a flagship that transforms, and has never stayed dead.", "Stage 6"], cnprime: ["The largest machine ever built. The final battle.", "Stage 7"] };
function shCnt() { const T = now(), s = cntStage(T), st = cntStC(T), M = cntS(), c = cntClock(T), own = ownerFree() && G.mode !== "offline" || G.owner, on = cntOn(T), war = cntWar(st);
  const nextS = s >= 1 && s < 7 ? CNT_STG[s] : null, when = s === 0 ? `Begins in ${ftime(-c.e)}` : s === 8 ? "The war is over" : s === 7 ? "The final battle" : `${CNT_STN[s + 1]} in ${ftime(nextS - c.e)}`;
  const stg = [1, 2, 3, 4, 5, 6, 7].map(i => `<div class="mimwk cntwk${i === s ? " on" : i < s ? " past" : ""}"><b>${i}</b><span>${CNT_STN[i]}</span></div>`).join("");
  const my = (st.con[G.me] || 0) + (M.pend || 0), n = Object.keys(st.con).length, top = Object.entries(st.con).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const warH = `<h3>War progress</h3><div class="mimsup"><div class="mimbar big cntbar"><i style="width:${war}%"></i></div><b>${war}%</b></div><p class="note" style="margin-top:4px">Destroyed Arks count most (40%), then commanders gone for good (20%), relays broken (15%) and every commander's war points (25%). ${n} commander${n === 1 ? "" : "s"} fighting · your share ${fmt(my)} point${my === 1 ? "" : "s"}${M.pend ? " (sending)" : ""}.</p>
    <div class="crcms">${CNT_MILE.map(([p, sh, mt]) => { const got = M.got["m" + p], ok = war >= p && my > 0; return `<div class="crcm${got ? " got" : ok ? " ok" : ""}"><b>${p}%</b><small>◆${sh} · ${cntMatTxt(mt)}</small>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${ok ? " pri" : ""}" data-act="cntMile" data-p="${p}"${ok ? "" : " disabled"}>Claim</button>`}</div>`; }).join("")}</div>`;
  const net = s >= 3 && s <= 8 ? `<h3>The resurrection network</h3><p class="note">Destroying fleets only buys time: a commander whose Ark lives is rebuilt 6 hours after it dies. Break an Ark's three relays to drop its shield, then destroy the Ark. A destroyed Ark stays destroyed.</p><div class="cntnet">${[0, 1, 2, 3].map(i => cntNetRow(st, T, i)).join("")}</div>
    ${s >= 6 ? (() => { const E = CNT_BOSS.ke0, e = st.cmd.ke0; return `<div class="crcboss${e.dead ? " dead" : ""}"><img src="art/rwar/c_eternal.webp" alt="" loading="lazy"><div><b>The Eternal Commander</b><small>${e.dead ? "Gone for good" : e.back > T ? `Being rebuilt · back in ${ftime(e.back - T)}` : `${e.hp}/${E.hp} sections · rebuilt ${e.res}×`}</small><div class="mimbar cntbar"><i style="width:${e.dead ? 0 : Math.round(e.hp / E.hp * 100)}%"></i></div></div>${!e.dead && !(e.back > T) ? `<button class="btn pri" data-act="cntGo" data-id="ke0">Go</button>` : ""}</div>`; })() : ""}` : "";
  const objs = (CNT_OBJ[s] || []), obj = on && objs.length ? `<h3>Orders · stage ${s}</h3>` + objs.map(([id, t, need, sh, mt]) => { const k = Math.min(need, cntObjN(s, id)), done = k >= need, got = M.got[`s${s}${id}`];
    return `<div class="mimobj cntobj"><div><b>${t}</b><div class="bar"><i style="width:${k / need * 100}%"></i></div><small>${k}/${need} · reward ◆${sh} and ${cntMatTxt(mt)}</small></div>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${done ? " pri" : ""}" data-act="cntClaimO" data-s="${s}" data-id="${id}"${done ? "" : " disabled"}>Claim</button>`}</div>`; }).join("") : "";
  const pats = CNT_PATS.filter(x => cntLive(x, T) && pirDown(x) <= T).length, plats = CNT_PLATS.filter(x => cntLive(x, T) && pirDown(x) <= T).length;
  const find = on && s < 7 ? `<div class="crcfind"><button class="btn pri" data-act="cntFind" data-m="cnpat"${pats ? "" : " disabled"}>Nearest patrol (${pats})</button><button class="btn" data-act="cntFind" data-m="cnplat"${plats ? "" : " disabled"}>Nearest platform (${plats})</button></div>` : "";
  const mats = Object.entries(CNT_MAT).map(([k, [nm, col]]) => `<div class="mimmat"><i class="cntmi" style="--c:${col}"></i><b>${fmt(M.m[k] || 0)}</b><small>${nm}</small></div>`).join("");
  const tac = `<details class="crclore"><summary>Machine tactics</summary>${Object.values(CNT_TAC).map(([nm, d, ctr]) => `<div class="crctac cnttac"><i></i><div><b>${nm}</b><small>${d} Counter: ${ctr}</small></div></div>`).join("")}</details>`;
  const cls = ["cnint", "cncor", "cnexe", "cnfab", "cnasm", "cndre", "cnrel", "cnark", "cneter", "cnprime"];
  const board = top.length ? `<h3>Top commanders</h3><div class="cntlb">${top.map(([u, v], i) => `<div><b>${i + 1}</b><span>${esc(u === G.me ? (S.homeName || "You") : (((G.players || {})[u] || {}).name || "Commander"))}</span><em>${fmt(v)}</em></div>`).join("")}</div>` : "";
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${CNT_COL}">War Command</div><h2>⬢ The Resurrection War</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="mimban cntban"><img src="art/rwar/ark_front.webp" alt=""><div><b>${s >= 1 && s <= 7 ? `Stage ${s} · ${CNT_STN[s]}` : s === 0 ? "A signal nobody sent" : "Continuity broken"}</b><span>${when}${c.prev ? " · owner preview" : ""}</span></div></div>
  <div class="cntwhy"><b>Why the Arks matter</b><span>Destroying their fleets buys time. Destroying their Resurrection Arks wins the war.</span></div>
  <details class="crclore"${on && !M.loreSeen ? " open" : ""}><summary>The Continuum</summary><p>The Continuum is a machine civilisation older than our records. Somewhere in the dark it found fragments of the architecture Omega used to keep minds alive, and built its own.</p><p>When one of its vessels is destroyed, the mind that commanded it is sent to a Resurrection Ark, which rebuilds the commander and a new fleet around it. Its doctrine is one line: "Flesh forgets. Machines remember. Death is merely a transmission delay."</p><p>We first heard it as a red signal nobody sent. Now it is here.</p></details>
  <p class="note">${s >= 1 && s <= 7 ? CNT_STD[s] : s === 0 ? "Deep-space listening posts keep catching one word in a narrow red band: continuity." : "The Arks are silent. Somewhere, a last transmission is still travelling."}</p>
  <div class="mimwks cntwks">${stg}</div>${find}${net}${obj}${on || s === 8 ? warH : ""}${board}${tac}
  <h3>War materials</h3><div class="mimmats">${mats}</div><p class="note" style="margin-top:6px">War points: <b>${fmt(M.pts)}</b>. Neural Echoes from everything; Machine Alloy from patrols and platforms; Circuitry from platforms and relays; Reactor Cells and Resurrection Cores from Arks; Quantum Neural Matrices from commanders.</p>
  ${S.medals && S.medals.ark ? `<div class="mimmedal"><span>🏆 Arkbreaker ×${S.medals.ark}</span></div>` : ""}
  <h3>The Continuum fleet</h3><div class="mimcls">${cls.map(k => `<div class="mimcl cntcl">${CNT_ART[k] ? `<img src="art/rwar/${CNT_ART[k]}.webp" alt="" loading="lazy">` : `<canvas data-ship="${k}" width="224" height="112"></canvas>`}<div><b>${AL[k].n}</b><small>${CNT_CD[k][0]}</small><em>${CNT_CD[k][1]}</em></div></div>`).join("")}</div>
  ${own ? `<div class="mimown"><small>Owner preview: see the war as it will look at each stage (this device only). Players see nothing until it is switched on.</small><div>${[0, 1, 2, 3, 4, 5, 6].map(k => `<button class="btn${((S.cntPrev || {}).s || 0) === k ? " pri" : ""}" data-act="cntPrev" data-s="${k}">${k ? "Stage " + k : "Off"}</button>`).join("")}</div></div>` : ""}`; }
function cntBossInfo(x, T) { const B = CNT_BOSS[x.id], st = cntStC(T), why = cntBlock(B, st, T), Z = cntBossSet(B, st, T), hp = Z.n0, my = B.cnt === "rel" ? st.rel[B.id].dmg[G.me] || 0 : B.cnt === "ark" ? st.ark[B.id].dmg[G.me] || 0 : st.cmd[B.id].dmg[G.me] || 0;
  const net = B.cnt === "rel" ? `Feeds ${CNT_ARKS[B.reg][1]}. While it stands, the Ark keeps its shield and can rebuild its commanders.` : B.cnt === "ark" ? `${cntRelUp(st, B.reg)} of 3 relays up · ${st.ark[B.id].cap} rebuilds left. Destroyed, it stays destroyed.` : B.cnt === "cmd" ? `Linked to ${CNT_ARKS[B.reg][1]}: ${cntCanRes(st, B.reg) ? "if destroyed now, it will be rebuilt in 6 hours" : "if destroyed now, it is gone for good"}.` : `${cntCanRes(st, -1) ? "Answers to no Ark: it is rebuilt 6 hours after it falls, every time." : ""}`;
  return `<div class="crcbi cntbi">${B.art ? `<img src="art/rwar/${B.art}.webp" alt="">` : ""}<div><b>${hp} of ${B.hp} sections</b><div class="mimbar cntbar"><i style="width:${Math.round(hp / B.hp * 100)}%"></i></div><small>${net} Your share: ${my} section${my === 1 ? "" : "s"}.</small></div></div>
    ${why ? `<p class="note cntwarn">${esc(why)}</p>` : ""}${Z.tac.map(t => `<div class="crctac cnttac"><i></i><div><b>${CNT_TAC[t][0]}</b><small>${CNT_TAC[t][1]}</small></div></div>`).join("")}
    <dl class="kv"><dt>Its fleet</dt><dd>${Object.entries(cntBossForce(x, T)).map(([k, v]) => `${v} ${AL[k] ? AL[k].n : k}`).join(" · ")}</dd><dt>Every section</dt><dd>◆2 · resources · Neural Echoes${B.cnt === "rel" ? " · Circuitry" : B.cnt === "ark" ? " · Reactor Cells · Resurrection Cores" : " · Quantum Neural Matrices"} · +4 war points</dd>${B.cnt === "ark" ? `<dt>When it falls</dt><dd>Everyone who broke a section claims the Arkbreaker reward</dd>` : ""}</dl>`; }
function cntInfo(x, T) { const L = cntLoot(x); return `${x.mon === "cnpat" ? "Machine patrol" : "Machine shipyard"}</dd><dt>Its force</dt><dd>${cntForceTxt(x)}</dd><dt>Salvage</dt><dd>${cntMatTxt(L)} · +${L.pts} war points`; }
function cntNearest(T, mon) { const h = originPlanet() || myPlanets()[0]; if (!h) return null; const hp = pos(h, T); let best = null, bd = 1e9;
  for (const x of mon === "cnplat" ? CNT_PLATS : CNT_PATS) { if (!cntLive(x, T) || pirDown(x) > T) continue; const q = pos(x, T), d = Math.hypot(q.x - hp.x, q.y - hp.y); if (d < bd) { bd = d; best = x; } } return best; }
/* the Battle Lab */
const CNT_LAB = [["kp", "Continuum patrol (stage 6)", () => ({ cnint: 6, cncor: 2, cnexe: 1, cnasm: 1 })], ["kf", "Fabrication platform (stage 6)", () => ({ cnfab: 1, cnint: 9, cnexe: 2, cnasm: 1, cndre: 1 })],
  ["krel", "A Resurrection Relay", () => ({ cnrel: 20, cncor: 2, cnexe: 3, cnint: 4 })], ["kark", "A Resurrection Ark", () => ({ cnark: 20, cnasm: 2, cnexe: 3, cnint: 7, cnfab: 1, cndre: 1 })],
  ["kcmd", "A Continuum commander", () => ({ cncom: 20, cnexe: 3, cncor: 2, cnint: 6, cnasm: 1 })], ["ketr", "The Eternal Commander", () => ({ cneter: 20, cndre: 2, cnasm: 2, cnexe: 4, cncor: 2 })]];
function cntLabFight(k) { const L = CNT_LAB.find(x => x[0] === k); if (!L) return; const D0 = L[2](), big = k.length > 2, A0 = big ? MIM_LAB_FLEET : { battleship: 20, destroyer: 20, fighter: 60, corvette: 20 }, lvl = 20, Z = cntMods(D0, big && k !== "krel" && k !== "kark" ? { cnt: "cmd" } : null);
  const A = stacksOf(A0, techOf(null), G.me); for (const s of A) { s.atk *= Z.m.pA; s.sh *= Z.m.pS; } const D = stacksOf(D0, { mon: lvl }, "monster"); for (const s of D) { s.atk *= Z.m.bA; s.hull *= Z.m.bH; }
  const res = simulate(A, D), mon = k === "kp" ? "cnpat" : k === "kf" ? "cnplat" : k === "krel" ? "cnrelay" : k === "kark" ? "cnarkm" : k === "ketr" ? "cneterm" : "cncmd";
  const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Battle Lab · ${L[1]}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: L[1], mon, lvl, ptype: "terran", fortL: 0, alien: true, pirate: true, cntTac: Z.tac,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
  closeSheet(); playBattle(rep); }
function cntLabHTML(row0, b) { const p = S.cntPrev || {}, row = (ic, n, sub, btns) => `<div class="strow" style="flex-wrap:wrap"><div style="flex:1 1 100%;min-width:0"><b>${ic} ${esc(n)}</b>${sub ? `<div class="note">${sub}</div>` : ""}</div><div style="display:flex;flex-wrap:wrap;gap:6px">${btns}</div></div>`;
  return row("⬢", "The war, stage by stage", `Patrols, platforms, the network and War Command as they will be · ${p.s ? `previewing stage ${p.s}, ${CNT_STN[p.s]}` : "off"}`, [1, 2, 3, 4, 5, 6].map(s => b("cntLabStage", String(s), "S" + s)).join("") + b("cntLabStage", "0", "Off") + b("cntOpen", "", "War Command"))
    + CNT_LAB.map(([k, n]) => row0("⬢", n, k.length > 2 ? "A demo fleet of 1,400 warships" : "A small fleet against it", b("cntLabFight", k, "⚔ Watch"))).join(""); }

/* ---------- the Continuum's hulls: black chrome and gunmetal, crimson neural light used sparingly, icy blue only on quantum parts.
   Angular prisms (an outline seen from above, extruded with chamfered top and bottom), visible joints, rings and reactor cores.
   Every hull points along +x; engines sit at the stern. ---------- */
function cntMats() { if (cntMats.M) return cntMats.M; const S0 = (c, m, r, e, ei, env) => new TH.MeshStandardMaterial({ color: c, metalness: m, roughness: r, emissive: e || 0, emissiveIntensity: ei || 0, side: TH.DoubleSide, envMapIntensity: env == null ? .45 : env });
  return cntMats.M = { hull: S0(0x0a0b0e, .6, .78, 0, 0, .12), plate: S0(0x050506, .4, .85, 0, 0, .08), chrome: S0(0x16181c, .95, .32, 0, 0, .45), gun: S0(0x1e2128, .7, .4, 0, 0, .5), joint: S0(0x30333a, .7, .45), red: S0(0x2a0004, .2, .5, 0xff0012, .62, .2), redDim: S0(0x140102, .2, .6, 0x9a0010, .5, .15), blue: S0(0x041018, .2, .4, 0x3fb8f0, .8), glass: S0(0x10050a, .1, .2, 0x5a0c14, .7) }; }
function buildCnt(k) { const C = cntMats(), g = new TH.Group(); g.userData.eng = []; g.userData.engCol = [0xffc0c6, 0xff2a3a];
  const add = (m, x, y, z) => { m.position.set(x || 0, y || 0, z || 0); g.add(m); return m; };
  const box = (w, h, d, mat, x, y, z, ry, rz) => { const m = add(new TH.Mesh(new TH.BoxGeometry(w, h, d), mat), x, y, z); if (ry) m.rotation.y = ry; if (rz) m.rotation.z = rz; return m; };
  const cyl = (r0, r1, h, mat, x, y, z, ax, seg) => { const m = add(new TH.Mesh(new TH.CylinderGeometry(r1, r0, h, seg || 12), mat), x, y, z); if (ax === "x") m.rotation.z = -Math.PI / 2; if (ax === "z") m.rotation.x = Math.PI / 2; return m; };
  const ring = (r, t, mat, x, y, z, ax) => { const m = add(new TH.Mesh(new TH.TorusGeometry(r, t, 8, 40), mat), x, y, z); if (ax === "x") m.rotation.y = Math.PI / 2; if (ax === "y") m.rotation.x = Math.PI / 2; return m; };
  const ball = (r, mat, x, y, z) => add(new TH.Mesh(new TH.SphereGeometry(r, 16, 12), mat), x, y, z);
  /* a hull plate: the outline as [x, z] on one side (mirrored), extruded hTop up and hBot down, its top and bottom faces pulled in by inset */
  const prism = (pts, hTop, hBot, inset, mat, x, y, z) => { const full = pts.concat(pts.slice().reverse().map(([a, b]) => [a, -b])).filter((p, i, A) => i === 0 || p[0] !== A[i - 1][0] || p[1] !== A[i - 1][1]);
    const n = full.length, P = [], I = [], ring3 = (yy, k2) => full.forEach(([a, b]) => P.push(a * (1 - (1 - k2) * .25), yy, b * k2));
    ring3(hTop, inset); ring3(0, 1); ring3(-hBot, inset);
    const tri = TH.ShapeUtils.triangulateShape(full.map(([a, b]) => new TH.Vector2(a, b)), []);
    for (const [a, b, c] of tri) { I.push(a, c, b); I.push(2 * n + a, 2 * n + b, 2 * n + c); }
    for (let i = 0; i < n; i++) { const j = (i + 1) % n; I.push(i, j, n + i, j, n + j, n + i, n + i, n + j, 2 * n + i, n + j, 2 * n + j, 2 * n + i); }
    const geo = new TH.BufferGeometry(); geo.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); geo.setIndex(I); const ng = geo.toNonIndexed(); ng.computeVertexNormals(); return add(new TH.Mesh(ng, mat), x, y, z); };
  const strip = (x0, x1, y, z, w, mat) => box(Math.abs(x1 - x0), w, w, mat || C.red, (x0 + x1) / 2, y, z);
  const eng = (x, y, z, r) => { g.userData.eng.push([x, y, z, r]); cyl(r * 1.1, r * .9, r * 1.2, C.joint, x + r * .4, y, z, "x"); };
  if (k === "cnint") { prism([[2.4, 0], [.9, .3], [-.2, .5], [-1.1, 1.7], [-1.5, 1.75], [-1.05, .45], [-1.4, .3], [-1.4, 0]], .32, .2, .45, C.hull); prism([[1.6, 0], [.4, .22], [-1, .3], [-1.2, 0]], .55, .05, .4, C.chrome, 0, .15);
    ball(.2, C.red, 1.55, .35, 0); strip(-1.2, -.2, .2, .62, .05); strip(-1.2, -.2, .2, -.62, .05); eng(-1.5, .05, .25, .18); eng(-1.5, .05, -.25, .18); }
  else if (k === "cncor") { prism([[2, 0], [.8, .45], [-1.4, .55], [-1.7, .3], [-1.7, 0]], .35, .3, .5, C.hull); cyl(.08, .05, 1.7, C.joint, .1, 1.1, 0); for (const y of [.8, 1.3, 1.8]) box(.06, .06, .9 - y * .2, C.chrome, .1, y, 0);
    for (const s of [1, -1]) { const d = add(new TH.Mesh(new TH.SphereGeometry(.42, 16, 8, 0, TAU, 0, Math.PI / 2.4), C.chrome), -.4, .55, .7 * s); d.rotation.x = s * 1.1; ring(.4, .03, C.red, -.4, .55 + .05, .78 * s, null).rotation.x = s * 1.1 + Math.PI / 2; }
    strip(-1.4, .9, .1, .56, .05, C.blue); strip(-1.4, .9, .1, -.56, .05, C.blue); eng(-1.8, 0, 0, .25); }
  else if (k === "cnexe") { prism([[3.2, 0], [1.6, .3], [.2, .55], [-1.6, .7], [-2.1, .5], [-2.1, 0]], .4, .35, .55, C.hull); prism([[2.6, 0], [1, .2], [-1.8, .3], [-1.9, 0]], .7, .05, .5, C.chrome, 0, .2);
    for (const z of [.18, -.18]) { cyl(.07, .07, 1.6, C.gun, .9, .85, z, "x"); box(.5, .22, .5, C.gun, .2, .75, 0); } ring(.62, .09, C.red, -.6, .1, 0, "x"); ring(.75, .05, C.joint, -.6, .1, 0, "x"); for (const s of [1, -1]) strip(-1.8, 1.4, -.05, .62 * s, .05); eng(-2.2, 0, .3, .26); eng(-2.2, 0, -.3, .26); }
  else if (k === "cnfab") { prism([[3, 0], [2.4, .9], [-2.6, 1], [-3, .7], [-3, 0]], .45, .5, .7, C.hull); prism([[2, 0], [1.2, .5], [-2.4, .55], [-2.5, 0]], .8, .05, .6, C.chrome, 0, .3);
    for (const x of [1.4, 0, -1.4]) { box(1, .55, .25, C.hull, x, 0, 1.05); box(.85, .38, .05, C.redDim, x, 0, 1.18); box(.18, .1, .12, C.chrome, x + .2, 0, 1.32); }
    for (const x of [1.6, .4]) box(.2, .9, .2, C.joint, x, .9, -.5); strip(-2.6, 2.4, .5, -.9, .05); eng(-3.1, 0, .5, .3); eng(-3.1, 0, -.5, .3); eng(-3.1, .3, 0, .24); }
  else if (k === "cnasm") { prism([[2.6, 0], [1.4, .5], [-.8, .8], [-2.2, .6], [-2.4, 0]], .5, .4, .55, C.hull); add(new TH.Mesh(new TH.SphereGeometry(.6, 18, 10, 0, TAU, 0, Math.PI / 2), C.blue), -.6, .45, 0).scale.set(1.3, .7, 1);
    for (const s of [1, -1]) for (const x of [1.4, .2]) { const a = new TH.Vector3(x, 0, .7 * s), b = new TH.Vector3(x + .9, -.1, 1.3 * s), c = new TH.Vector3(x + 1.7, -.15, .9 * s);
      for (const [p, q] of [[a, b], [b, c]]) { const d = q.clone().sub(p), m = cyl(.07, .06, d.length(), C.joint, (p.x + q.x) / 2, (p.y + q.y) / 2, (p.z + q.z) / 2); m.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), d.normalize()); } ball(.1, C.chrome, b.x, b.y, b.z); }
    ball(.14, C.red, 2.3, .15, 0); strip(-2, 1.2, .2, .82, .05); strip(-2, 1.2, .2, -.82, .05); eng(-2.5, 0, .35, .28); eng(-2.5, 0, -.35, .28); }
  else if (k === "cndre" || k === "cncom") { prism([[3.6, 0], [2.2, .9], [-.5, 1.5], [-2.8, 1.6], [-3.3, 1.1], [-3.3, 0]], .7, .6, .6, C.hull); prism([[2.8, 0], [1.4, .7], [-2.4, 1.1], [-2.6, 0]], 1.1, .05, .55, C.chrome, 0, .4); prism([[1.6, 0], [.4, .5], [-1.8, .7], [-2, 0]], 1.5, .05, .5, C.hull, 0, .9);
    for (const [x, z] of [[1.4, .5], [1.4, -.5], [-.4, .9], [-.4, -.9]]) { box(.55, .25, .5, C.gun, x, 1, z); cyl(.08, .08, 1.3, C.gun, x + .75, 1.08, z, "x"); }
    ball(.55, C.red, -.9, .2, 0); ring(.75, .07, C.joint, -.9, .2, 0, "x"); ring(.75, .07, C.joint, -.9, .2, 0, "y"); for (const s of [1, -1]) strip(-3, 2.4, 0, 1.25 * s, .06);
    if (k === "cncom") { for (const [x, h] of [[-.6, 1.6], [-1.1, 2.2], [-1.6, 1.6]]) { cyl(.12, .02, h, C.chrome, x, 1.7 + h / 2, 0); } ball(.18, C.red, -1.1, 2.4, 0); }
    eng(-3.4, 0, .7, .36); eng(-3.4, 0, -.7, .36); eng(-3.4, .5, 0, .3); }
  else if (k === "cnrel") { add(new TH.Mesh(new TH.DodecahedronGeometry(1.6, 0), new TH.MeshStandardMaterial({ color: 0x110e0c, roughness: 1, flatShading: true, envMapIntensity: .1 })), 0, -1.4, 0).scale.set(1.4, .6, 1.2);
    cyl(.55, .3, 3.8, C.hull, 0, 1.2, 0, null, 8); cyl(.3, .04, 1.6, C.chrome, 0, 3.9, 0, null, 8); cyl(.12, .12, 3.6, C.red, 0, 1.4, .3, null, 6); for (const [y, r] of [[.6, 1.6], [1.7, 1.3], [2.7, 1]]) { ring(r, .1, C.hull, 0, y, 0, "y"); ring(r, .035, C.red, 0, y + .08, 0, "y"); }
    for (const a of [0, 2.1, 4.2]) cyl(.06, .02, 1.2, C.chrome, Math.cos(a) * .5, 3.2, Math.sin(a) * .5); ball(.22, C.red, 0, 4.75, 0); }
  else if (k === "cnark") { prism([[5.2, 0], [3.6, .7], [-3.6, .9], [-4.6, .6], [-4.6, 0]], .9, .9, .7, C.hull); prism([[4.4, 0], [3, .5], [-3.8, .6], [-4, 0]], 1.4, .05, .6, C.chrome, 0, .5);
    for (const x of [2.6, -.2, -3]) { ring(1.9, .2, C.hull, x, .3, 0, "x"); ring(1.9, .06, C.red, x - .22, .3, 0, "x"); }
    for (let i = 0; i < 5; i++) { const x = 1.9 - i * 1.1; cyl(.32, .32, .9, C.glass, x, .2, 1, null, 10); box(.12, .5, .08, C.joint, x, .25, 1.05); ball(.12, C.red, x, .1, 1.2); }
    for (const x of [1, -1.6]) box(1.4, .5, .3, C.redDim, x, -.7, -.85); ball(.35, C.red, 4.6, .4, 0); eng(-4.8, 0, .5, .45); eng(-4.8, 0, -.5, .45); }
  else if (k === "cnprime") { cyl(1.1, .9, 7, C.hull, 0, 0, 0, null, 10); cyl(.4, .4, 7.6, C.red, 0, 0, 0, null, 8); for (const [y, r] of [[1.6, 3.6], [-1.4, 3.2]]) { ring(r, .32, C.hull, 0, y, 0, "y"); ring(r, .09, C.red, 0, y + .2, 0, "y"); }
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3, x = Math.cos(a) * 4.4, z = Math.sin(a) * 4.4; box(4.4, .25, .25, C.joint, x / 2, .2, z / 2, -a); cyl(.35, .08, 2.6, C.hull, x, .5, z, null, 6); ball(.25, C.red, x, 1.9, z); }
    for (let i = 0; i < 8; i++) cyl(.15, .01, 1.4 + (i % 3) * .6, C.chrome, Math.cos(i * .8) * .9, 3.9, Math.sin(i * .8) * .9, null, 6); cyl(1, .05, 2.2, C.hull, 0, -4.4, 0, null, 8); }
  else if (k === "cneter") { for (const [a, l] of [[.5, 4.2], [-.5, 4.2], [Math.PI - .55, 3.4], [-(Math.PI - .55), 3.4]]) { const p = prism([[l, 0], [l * .35, .28], [0, .42], [-.4, 0]], .28, .22, .5, C.hull); p.rotation.y = -a; const q = prism([[l * .85, 0], [l * .3, .18], [0, .25], [-.3, 0]], .44, .02, .45, C.chrome); q.rotation.y = -a; q.position.y = .1; }
    ball(.75, C.hull, 0, 0, 0).scale.set(1.3, .7, 1); ring(.62, .1, C.red, 0, .1, 0, "y"); ball(.28, C.red, .3, .35, 0); for (const s of [1, -1]) strip(-1.2, 2.2, .1, .5 * s, .05, C.blue); eng(-1.4, 0, .4, .3); eng(-1.4, 0, -.4, .3); }
  if (!/^cn(rel|prime)$/.test(k)) { const bb = new TH.Box3().setFromObject(g), L = bb.max.x - bb.min.x, r = rnd(hash("cnt" + k)), top = bb.max.y; /* panel greebles and a seam light along the spine */
    for (let i = 0; i < 6; i++) { const x = bb.min.x + L * (.18 + .1 * i), w = L * (.05 + r() * .04); box(w, .06, .18 + r() * .2, C.plate, x, top * (.55 + r() * .1), (r() - .5) * .5); }
    strip(bb.min.x + L * .15, bb.min.x + L * .75, top * .62, 0, .035, C.redDim); }
  g.userData.cnt = 1; return g; }
