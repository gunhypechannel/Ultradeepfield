/* ---------- v802 Dimensional Expeditions (stage 2): the Shattered Expanse, Aetherion Technology (six research branches), the Aetherion
   Exchange, daily expedition orders and the alliances' weekly gathering objective, reward claims recorded by the server (aet_claim). ---------- */
Object.assign(MON, {
  aetStat: { n: "Ancient Harvesting Station", sp: "Harvesting Station", ic: "⛭", col: "#8fd8ff", rgb: "143,216,255", per: 99, d: "A derelict machine that still splits stone from crystal. Gather here for quantum minerals, alloy and resources.", names: ["Station"] },
  aetPlat: { n: "Abandoned Mining Platform", sp: "Mining Platform", ic: "⬓", col: "#bcd8ff", rgb: "188,216,255", per: 99, d: "A mining rig the Expanse's beasts have nested in. Hold it and every gathering crew in the Expanse works faster.", names: ["Platform"] },
  aetAnom: { n: "Environmental Anomaly", sp: "Anomaly", ic: "✺", col: "#c8a8ff", rgb: "200,168,255", per: 99, d: "A knot of bent gravity. Fleets flying close by are slowed. Survey it once for what it hides.", names: ["Anomaly"] },
  aetBeast: { n: "Expanse Predators", sp: "Neutral alien threat", ic: "🜲", col: "#ff9a6a", rgb: "255,154,106", per: 99, d: "Void creatures that hunt the Expanse's lanes. They answer to nobody and attack anything that mines.", names: ["Predators"] },
  aetDep: { n: "Aetherion Deposit", sp: "Aetherion Deposit", ic: "◆", col: "#5fe8d0", rgb: "95,232,208", per: 99, d: "A floating shard of a broken planet, veined with raw Aetherion. Rich in fragments, and guarded.", names: ["Deposit"] } });
Object.assign(AET_M, { aetStat: "aetDrone", aetPlat: "vmanta", aetAnom: "aetDrone", aetBeast: "vmanta", aetDep: "slevi" });
{ const c = AET_RB.shat.c, at = (x, y, z) => (T, o) => { o = o || {}; o.x = c[0] + x; o.y = c[1] + y; o.z = c[2] + z; return o; }, R = "shat", out = [];
  const add = (id, mon, k, name, x, y, z, extra) => out.push(Object.assign({ id, kind: "pirate", mon, aetR: R, aetK: k, lvl: 5, name, mv: at(x, y, z), r: 1, a0: 0, lx: x, lz: z }, extra || {}));
  [[30, 96], [80, 60], [130, 20], [200, 88], [250, 40], [320, 78]].forEach(([d, r], j) => { const a = d * Math.PI / 180; add("asd" + j, "aetStat", "stat", `Harvester ${["Ivo", "Sela", "Morrow", "Qeth", "Dune", "Varr"][j]}`, Math.cos(a) * r, 0, Math.sin(a) * r, { guard: j % 3 !== 0 }); });
  [[60, 40], [150, 70], [240, 105], [330, 45]].forEach(([d, r], j) => { const a = d * Math.PI / 180; add("asp" + j, "aetPlat", "plat", `Platform ${["Kestrel", "Anvil", "Hollowmere", "Spindle"][j]}`, Math.cos(a) * r, 3, Math.sin(a) * r); });
  [[0, 0], [100, 60], [-70, -60], [40, -100], [-110, 20]].forEach(([x, z], j) => add("asa" + j, "aetAnom", "anom", `${["The Knot", "Shear Line", "Fallwell", "The Lens", "Quietfold"][j]}`, x, 6, z, { rad: 22 }));
  [[-40, 110], [115, -40], [-120, -95]].forEach(([x, z], j) => add("asx" + j, "aetDep", "dep", `${["Shard of Ilyr", "Shard of Oss", "Shard of Thren"][j]}`, x, 10, z, { guard: true }));
  for (let j = 0; j < 8; j++) { const a0 = j / 8 * TAU + .3, r0 = 50 + (j % 3) * 25; out.push({ id: "asb" + j, kind: "pirate", mon: "aetBeast", aetR: R, aetK: "beast", lvl: 5, r: 1, a0, name: `${["Manta", "Squid", "Manta", "Leviathan"][j % 4]} Pack ${j + 1}`,
    mv: (T, o) => { o = o || {}; const a = a0 + T / 7e5 * (j % 2 ? 1 : -1); o.x = c[0] + Math.cos(a) * r0; o.y = c[1] + 2 + Math.sin(T / 3e4 + j) * 3; o.z = c[2] + Math.sin(a) * r0; return o; } }); }
  AET_TGT.push(...out); for (const x of out) AET_TB[x.id] = x; }
Object.assign(AET_FX, { stat: x => x.guard ? { vmanta: 3, ssquid: 4 } : {}, plat: () => ({ vmanta: 5, ssquid: 6, swhale: 1 }), anom: () => ({}), beast: x => (+x.id.slice(3)) % 4 === 3 ? { slevi: 2, vmanta: 3 } : { vmanta: 4, ssquid: 5 }, dep: () => ({ slevi: 3, swhale: 2, ssquid: 4 }) });
Object.assign(AET_LOOT, { plat: { fr: 8, alloy: 4, m: 40000 }, anom: { fr: 6, circ: 2, relic: 0 }, beast: { fr: 5, min: 3, m: 30000, c: 20000 }, stat: { fr: 3, alloy: 2 }, dep: { fr: 10, min: 4 } });
Object.assign(AET_REGROUP, { plat: 10 * 3600e3, beast: 2 * 3600e3, stat: 4 * 3600e3, dep: 6 * 3600e3, anom: 0 }); Object.assign(AET_HOLD, { plat: 24 * 3600e3 });
AET_READY.shat = 1; AET_REQ.shat = () => aetRes("nav") >= 1 ? null : "Not charted yet: research Dimensional Navigation I (Aetherion Technology) to plot a route there.";
/* the Expanse's own rules: platforms speed gathering, anomalies slow fleets that pass close, a survey pays once per anomaly */
const aetExBon = T => Math.min(.2, .05 * AET_TGT.filter(x => x.aetK === "plat" && aetHeld(x.id, T || now())).length);
function aetDrift(tg, k) { if (k !== "shat") return 1; const q = tg.mv(now(), {}), c = AET_RB.shat.c, a = AET_ARR.shat, ax = c[0] + a[0], az = c[2] + a[2]; let slow = 1;
  for (const y of AET_TGT) if (y.aetK === "anom") { const p = y.mv(now(), {}), dx = q.x - ax, dz = q.z - az, L = Math.hypot(dx, dz) || 1, t = clamp(((p.x - ax) * dx + (p.z - az) * dz) / (L * L), 0, 1), d = Math.hypot(ax + dx * t - p.x, az + dz * t - p.z); if (d < y.rad) slow += .2; }
  return Math.min(1.6, slow); }
const AET_ANOM_LORE = ["Inside the knot the stars repeat: the same patch of sky, folded over itself seven times.", "The shear line is a wound in space. Something very large passed through here, a long time ago.", "Fallwell's floor is littered with hulls of a make nobody has seen, all pointing at the Interstice.",
  "The Lens shows the galaxy as it was before the Rim burned. The image is ten thousand years old, and perfectly sharp.", "In Quietfold, signals arrive before they are sent. The Advisor asked us not to linger."];
/* surveying an anomaly: a squadron flies there (mission "explore"), pays once, and recovers a line of its record */
AET_ACT.aetExplore = () => { const x = AET_TB[sheet.id]; if (!x || x.aetK !== "anom") return; const sel = Object.fromEntries(Object.entries(pick).filter(([k, v]) => v > 0)); const f = aetSend(x.id, sheet.tx, sel, "explore"); if (f) { for (const k in pick) delete pick[k]; closeSheet(); } };
/* ---------- Aetherion Technology ---------- */
const AET_RS = [["stab", "Gateway Stabilization", "Each level: crossings cost 5% less energy. Level 3: the flux hour adds only half its usual surcharge.", 5],
  ["nav", "Dimensional Navigation", "Level 1 charts the Shattered Expanse. Level 3 can follow the Carcinid's old current to the Primordial Tide (after the Carcinid Tide has run).", 5],
  ["sig", "Ancient Signal Analysis", "Each level: +10% from surveys and discoveries. Level 3, with a Silent Archive recovered from the Interstice, decodes the way to the Silent Dominion.", 5],
  ["harv", "Aetherion Harvesting", "Each level: +10% from every gathering crew in the realms.", 5],
  ["trans", "Fleet Transit Systems", "Each level: +20 transit energy. Level 2: a second gateway slot. Level 4: a third.", 5],
  ["logi", "Nexus War Logistics", "Each level: travel inside the realms 2% faster. In a Nexus War it will also shorten reinforcement (capped).", 5]];
const AET_RSB = Object.fromEntries(AET_RS.map(r => [r[0], r]));
const aetRsCost = (k, L) => ({ fr: Math.round(25 * L * L), alloy: 4 * L, circ: k === "sig" || k === "nav" ? 3 * L : 0, qm: L >= 3 ? L - 2 : 0, ms: Math.round(45 * 60e3 * Math.pow(L, 1.4)) });
function aetHave(L) { const A = aetS(); for (const k in L) { if (k === "ms") continue; if (k === "fr" ? (A.fr || 0) < L[k] : (A.m[k] || 0) < L[k]) return false; } return true; }
function aetPay(L) { const A = aetS(); for (const k in L) { if (k === "ms" || !L[k]) continue; if (k === "fr") A.fr -= L[k]; else A.m[k] -= L[k]; } }
function aetRsTick() { const A = S && S.aet; if (!A || !A.rq) return; if (now() >= A.rq.end) { const k = A.rq.k; A.rs = A.rs || {}; A.rs[k] = A.rq.L; A.rq = null; note(`Aetherion Technology: ${AET_RSB[k][1]} reached level ${A.rs[k]}.`, "win"); if (typeof aetMissionBump === "function") aetMissionBump("rs", 1); dirty(); softRender(); } }
setInterval(() => { try { aetRsTick(); } catch (e) {} }, 3000);
function aetResearchHTML(T) { const A = aetS(); const rq = A.rq;
  return `<h3>Aetherion Technology</h3><p class="note">Research paid with what your fleets bring back through the Gateway. One project at a time; the bonuses are capped and only touch Gateway and realm play.</p><div class="aetrs">${AET_RS.map(([k, n, d, mx]) => { const L = aetRes(k), nx = L + 1, C = aetRsCost(k, nx), run = rq && rq.k === k, can = !rq && L < mx && aetHave(C);
    return `<div class="aetrsr"><div><b>${esc(n)} <em>Lv.${L}/${mx}</em></b><small>${esc(d)}</small>${L < mx ? `<small>Next: ${aetMatTxt(C)} · ${ftime(C.ms)}</small>` : `<small>Complete</small>`}${run ? `<small class="aetok">Researching · <span data-end="${rq.end}">${ftime(rq.end - T)}</span></small>` : ""}</div>${L < mx && !run ? `<button class="btn${can ? " pri" : ""}" data-act="aetRs" data-k="${k}"${can ? "" : " disabled"}>Research</button>` : ""}</div>`; }).join("")}</div>`; }
AET_ACT.aetRs = d => { const A = aetS(), r = AET_RSB[d.k]; if (!r || A.rq) return; const L = aetRes(d.k) + 1; if (L > r[3]) return; const C = aetRsCost(d.k, L); if (!aetHave(C)) { toast("Not enough Aetherion materials yet.", "warn"); return; }
  aetPay(C); A.rq = { k: d.k, L, end: now() + Math.round(C.ms * (S.r && S.r.hyperT ? 1 : 1)) }; dirty(); toast(`Researching ${r[1]} Lv.${L}.`, "info"); renderSheet(); };
/* ---------- claims: the server records each one once (online); this device records it offline ---------- */
async function aetClaim(cid, v) { const A = aetS(); A.cl = A.cl || {}; if (A.cl[cid]) return false;
  if (G.mode === "online" && window.udfAet) { const ok = await window.udfAet.claim(cid, v || null); A.cl[cid] = 1; dirty(); return !!ok; }
  A.cl[cid] = 1; dirty(); return true; }
/* ---------- the Aetherion Exchange (fragments; Nexus War Marks for what only a war can earn) ---------- */
const AET_SHOP = [
  ["frame18", "Gateway Avatar Frame", "Portrait frame from the Aperture set.", { fr: 120 }, "cos"], ["banner18", "Gateway Profile Banner", "Profile banner from the Aperture set.", { fr: 120 }, "cos"],
  ["trail18", "Aetherion Warp Trail", "Your fleets' warp trail in signal teal (the hull finish of the set).", { fr: 160 }, "cos"], ["skinx18", "Aetherion Planet Skin", "An animated skin for your homeworld, threaded with teal light.", { fr: 260 }, "cos"],
  ["laser18", "Aetherion Beam Colour", "Your guns fire signal teal.", { fr: 90 }, "cos"],
  ["qmx", "Ancient Quantum Materials", "3 Quantum Matrices, refined from fragments and alloy.", { fr: 40, alloy: 10 }, "mat"], ["cache", "Dimensional Crafting Cache", "Two Silver accelerators and a crate of metal.", { fr: 30 }, "cache"],
  ["rsm", "Rare Research Materials", "A Gold Insight Matrix (research accelerator).", { fr: 45, circ: 4 }, "item"], ["fsm", "Specialized Flagship Materials", "A Gold Yard Overdrive and a Gold Forge Swarm (accelerators).", { fr: 70, qm: 2 }, "item2"],
  ["relic", "Ancient Technology Collectible", "Recover one of the Gateway builders' artefacts for your collection.", { relic: 2, fr: 20 }, "col"],
  ["nxf", "Nexus Conqueror Avatar Frame", "Earned with Nexus War Marks.", { mk: 300 }, "war"], ["apc", "Alliance Prestige Banner", "Earned with Nexus War Marks.", { mk: 500 }, "war"]];
const AET_COLS = ["The Builder's Compass", "A Lattice Seed (inert)", "Glass Map of the Network", "The Silent Key", "A Choir Shard", "The Last Log of Vesper Station"];
function aetShopHTML(T) { const A = aetS(), C = cosOf();
  return `<h3>Aetherion Exchange</h3><p class="note">Prices are this server's live settings.</p><div class="aetshop">${AET_SHOP.map(([k, n, d, cost, kind]) => { const own = kind === "cos" && C.own[k], war = kind === "war", col = kind === "col" && (A.col || 0) >= AET_COLS.length, can = !own && !war && !col && aetHave(cost);
    return `<div class="aetsi${own ? " own" : ""}"><div><b>${esc(n)}</b><small>${esc(d)}</small><small class="aetpr">${war ? `${cost.mk} Nexus War Marks · earned only in a Nexus War` : aetMatTxt(cost)}</small></div>${own ? `<span class="pill">Owned</span>` : war ? `<span class="pill">Nexus War</span>` : col ? `<span class="pill">All found</span>` : `<button class="btn${can ? " pri" : ""}" data-act="aetBuy" data-k="${k}"${can ? "" : " disabled"}>${sheet.buy === k ? "Confirm" : "Buy"}</button>`}</div>`; }).join("")}</div>
  ${A.col ? `<h3>Collection</h3><div class="aethist">${AET_COLS.slice(0, A.col).map(n => `<div><b>◈</b><span>${esc(n)}</span><em></em></div>`).join("")}</div>` : ""}`; }
AET_ACT.aetBuy = async d => { const it = AET_SHOP.find(s => s[0] === d.k), A = aetS(); if (!it) return; const [k, n, , cost, kind] = it; if (kind === "war" || !aetHave(cost)) return;
  if (sheet.buy !== k) { sheet.buy = k; renderSheet(); setTimeout(() => { if (sheet && sheet.buy === k) { sheet.buy = null; renderSheet(); } }, 5000); return; } sheet.buy = null;
  const cid = "buy:" + k + ":" + now().toString(36) + Math.floor(Math.random() * 1e6).toString(36); aetPay(cost);
  let ok = false; try { ok = await aetClaim(cid, { k }); } catch (e) { aetPay(Object.fromEntries(Object.entries(cost).map(([a, b]) => [a, -b]))); toast("The exchange couldn't record that purchase. Nothing was spent.", "warn"); renderSheet(); return; }
  if (!ok) { toast("That purchase was already recorded.", "info"); renderSheet(); return; }
  if (kind === "cos") cosGive(k); else if (kind === "mat") A.m.qm = (A.m.qm || 0) + 3; else if (kind === "cache") { giveItem("xb_silver"); giveItem("xs_silver"); S.res.m += 250000; } else if (kind === "item") giveItem("xr_gold"); else if (kind === "item2") { giveItem("xs_gold"); giveItem("xb_gold"); } else if (kind === "col") A.col = (A.col || 0) + 1;
  logReward(`Aetherion Exchange · ${n}`, null, { kind: "shop" }); dirty(); toast(`${n}: yours.`, "win"); renderSheet(); };
/* ---------- daily expedition orders, weekly alliance objective ---------- */
const AET_ORD = [["pat", "Destroy 2 Sentinel wings", 2, 6], ["fort", "Take a Dimensional Fortress", 1, 10], ["gather", "Finish 2 gathering runs", 2, 6], ["rel", "Take a Transit Relay", 1, 6], ["pyl", "Break 2 Nexus pylons", 2, 10], ["beast", "Drive off 2 predator packs", 2, 6], ["plat", "Take a mining platform", 1, 8], ["anom", "Survey an anomaly", 1, 5]];
function aetOrders(T) { const d = aetDay(T), pool = AET_ORD.filter(o => aetRes("nav") >= 1 || !["beast", "plat", "anom"].includes(o[0])), out = []; let h = hash("aetord" + d); while (out.length < 3 && pool.length) { const i = h % pool.length; out.push(pool.splice(i, 1)[0]); h = hash("x" + h); } return out; }
function aetMissionBump(k, n) { const A = aetS(), d = aetDay(); if (!A.od || A.od.d !== d) A.od = { d, n: {} }; A.od.n[k] = (A.od.n[k] || 0) + (n || 1);
  if (k === "gather" && aetRes("nav") >= 0) aetAllyAdd(1); dirty(); }
function aetMissionsHTML(T) { const A = aetS(), d = aetDay(T), od = A.od && A.od.d === d ? A.od.n : {}, ord = aetOrders(T);
  const ally = typeof myAlly === "function" ? myAlly() : null, wk = Math.floor(T / AET_WK), st = G.aetAlly && G.aetAlly.wk === wk ? G.aetAlly : null, goal = aetAllyGoal(ally), sum = st ? st.sum : 0, mine = st && st.by ? st.by[G.me] || 0 : 0, acid = `ally:${ally ? ally.id || ally.tag : "-"}:${wk}`;
  return `<h3>Expedition orders · today</h3><div class="aetord">${ord.map(([k, t, need, fr]) => { const v = Math.min(need, od[k] || 0), cid = `ord:${d}:${k}`, got = (A.cl || {})[cid];
    return `<div class="mimobj"><div><b>${esc(t)}</b><div class="bar"><i style="width:${v / need * 100}%"></i></div><small>${v}/${need} · ${fr} Aetherion Fragments</small></div>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${v >= need ? " pri" : ""}" data-act="aetOrd" data-k="${k}"${v >= need ? "" : " disabled"}>Claim</button>`}</div>`; }).join("")}</div>
  <h3>Alliance objective · this week</h3>${ally ? `<div class="mimobj"><div><b>Gather together in the realms: ${fmt(goal)} runs</b><div class="bar"><i style="width:${Math.min(100, sum / goal * 100)}%"></i></div><small>${fmt(sum)}/${fmt(goal)} · you ${fmt(mine)} · 40 fragments and 4 Dimensional Alloy for every member who helped</small></div>${(A.cl || {})[acid] ? `<span class="pill">Claimed</span>` : `<button class="btn${sum >= goal && mine ? " pri" : ""}" data-act="aetAllyClaim"${sum >= goal && mine ? "" : " disabled"}>Claim</button>`}</div>` : `<p class="note">Join an alliance to share a weekly gathering objective in the realms.</p>`}`; }
AET_ACT.aetOrd = async d => { const A = aetS(), dd = aetDay(), o = aetOrders().find(x => x[0] === d.k), od = A.od && A.od.d === dd ? A.od.n : {}; if (!o || (od[o[0]] || 0) < o[2]) return;
  try { if (!(await aetClaim(`ord:${dd}:${o[0]}`))) { toast("Already claimed.", "info"); renderSheet(); return; } } catch (e) { toast("The claim didn't reach the server. Try again.", "warn"); return; }
  A.fr = (A.fr || 0) + o[3]; logReward(`Expedition order · ${o[1]}`, null, { kind: "event" }); toast(`Order complete: +${o[3]} Aetherion Fragments.`, "win"); dirty(); renderSheet(); };
const aetAllyGoal = a => 20 + 6 * Math.max(1, a && a.members ? Object.keys(a.members).length : 1);
let AET_ALLY_P = 0;
function aetAllyAdd(n) { AET_ALLY_P += n; aetAllyFlush(); }
async function aetAllyFlush() { const a = typeof myAlly === "function" ? myAlly() : null; if (!a || !AET_ALLY_P || G.aetAllyFl) return; const wk = Math.floor(now() / AET_WK), id = a.id || a.tag; G.aetAllyFl = 1;
  try { const ref = adb().doc(`event/aetally_${id}_${wk}`); await crcLock(ref); const snap = await casGet(ref), cur = snap.exists ? snap.data() : { wk, sum: 0, by: {} }; cur.wk = wk; cur.by = cur.by || {}; const add = AET_ALLY_P;
    cur.sum = (cur.sum || 0) + add; cur.by[G.me] = (cur.by[G.me] || 0) + add; if (await casSet(ref, snap, cur)) { AET_ALLY_P -= add; G.aetAlly = cur; } } catch (e) {} finally { G.aetAllyFl = 0; } }
async function aetAllyRead() { const a = typeof myAlly === "function" ? myAlly() : null; if (!a) return; const wk = Math.floor(now() / AET_WK); try { const snap = await casGet(adb().doc(`event/aetally_${a.id || a.tag}_${wk}`)); G.aetAlly = snap.exists ? Object.assign({ wk }, snap.data()) : { wk, sum: 0, by: {} }; softRender(); } catch (e) {} }
setInterval(() => { try { if (S && S.aet && aetOpen()) { if (AET_ALLY_P) aetAllyFlush(); else if (sheet && sheet.type === "aet" && sheet.tab === "more") aetAllyRead(); } } catch (e) {} }, 30e3);
AET_ACT.aetAllyClaim = async () => { const a = myAlly(), wk = Math.floor(now() / AET_WK), st = G.aetAlly; if (!a || !st || st.wk !== wk || st.sum < aetAllyGoal(a) || !(st.by || {})[G.me]) return;
  try { if (!(await aetClaim(`ally:${a.id || a.tag}:${wk}`))) { toast("Already claimed.", "info"); return; } } catch (e) { toast("The claim didn't reach the server. Try again.", "warn"); return; }
  const A = aetS(); A.fr = (A.fr || 0) + 40; A.m.alloy = (A.m.alloy || 0) + 4; toast("Alliance objective: +40 Aetherion Fragments, +4 Dimensional Alloy.", "win"); dirty(); renderSheet(); };
/* ---------- the Expanse drawn ---------- */
function aetStructTick(x, m, t, T) { const U = m.userData; if (U.anom) { U.anom.rotation.z = t * .0004; U.anom.material.opacity = .25 + .1 * Math.sin(t * .002 + x.lx); } if (U.dep) U.dep.rotation.y = t * .0002; }
{ const base = aetStructMesh; aetStructMesh = function (x) { const k = x.aetK; if (!["stat", "plat", "anom", "beast", "dep"].includes(k)) return base(x);
  const g = new TH.Group(), M = (c, e) => new TH.MeshStandardMaterial({ color: c, metalness: .6, roughness: .5, emissive: e || 0, emissiveIntensity: e ? .55 : 0 }), rock = M(0x2a2e33), dark = M(0x1a1f24), gun = M(0x3a4450), teal = aetGlowM(0x5fe8d0, .9);
  if (k === "stat") { const b = new TH.Mesh(new TH.BoxGeometry(7, 3, 5), gun); g.add(b); const arm = new TH.Mesh(new TH.BoxGeometry(10, .6, .8), dark); arm.position.set(3, 2.5, 0); arm.rotation.z = -.3; g.add(arm); const d = new TH.Mesh(new TH.CylinderGeometry(1.2, 1.2, 4, 8), dark); d.position.set(-2, 3, 0); g.add(d);
    const r = new TH.Mesh(new TH.IcosahedronGeometry(3.2, 0), rock); r.position.set(7, 1, 0); g.add(r); const l = new TH.Mesh(new TH.BoxGeometry(6, .12, .12), teal); l.position.set(0, 1.6, 2.6); g.add(l); }
  else if (k === "plat") { const d = new TH.Mesh(new TH.CylinderGeometry(6, 6.5, 1.4, 10), gun); g.add(d); for (let i = 0; i < 4; i++) { const a = i / 4 * TAU, t2 = new TH.Mesh(new TH.BoxGeometry(1, 8, 1), dark); t2.position.set(Math.cos(a) * 4.5, 4, Math.sin(a) * 4.5); g.add(t2); } const c = new TH.Mesh(new TH.ConeGeometry(2, 5, 6), dark); c.position.y = 3; g.add(c);
    const ring = new TH.Mesh(new TH.TorusGeometry(6.6, .1, 4, 48), teal); ring.rotation.x = Math.PI / 2; g.add(ring); g.userData.ring = ring; }
  else if (k === "anom") { const s = new TH.Mesh(new TH.RingGeometry(4, x.rad || 20, 64, 1), new TH.MeshBasicMaterial({ map: aetRadial("aetanom", [[0, "rgba(200,168,255,0)"], [.5, "rgba(200,168,255,.5)"], [.8, "rgba(120,90,255,.18)"], [1, "rgba(0,0,0,0)"]]), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, opacity: .3 }));
    s.rotation.x = -Math.PI / 2; g.add(s); g.userData.anom = s; const c = aetSprite(9, "rgba(220,200,255,1)", "aetanomc"); g.add(c); }
  else if (k === "dep") { const r = new TH.Mesh(new TH.DodecahedronGeometry(9, 0), rock); r.scale.set(1.3, .7, 1); g.add(r); for (let i = 0; i < 9; i++) { const h = hash(x.id + i), cr = new TH.Mesh(new TH.OctahedronGeometry(1 + (h % 3) * .5, 0), M(0x1c3a36, 0x2f9f8f)); cr.position.set(((h % 100) - 50) / 6, 5 + (h % 4), (((h >> 8) % 100) - 50) / 6); cr.scale.y = 2.2; g.add(cr); }
    const gl = aetSprite(22, "rgba(95,232,208,1)", "aetdep"); gl.material.opacity = .35; gl.position.y = 4; g.add(gl); g.userData.dep = r; }
  else if (k === "beast") { let b; try { b = buildMonster((+x.id.slice(3)) % 4 === 3 ? "slevi" : "vmanta"); } catch (e) { b = null; } if (b) { b.scale.setScalar(1.4); g.add(b); } else g.add(aetSprite(4, "rgba(255,154,106,1)", "aetbeast")); }
  return g; }; }
/* scenery of the Expanse: broken planets and asteroid belts drawn once with the realm */
{ const base = aetRealmScene; aetRealmScene = function (k) { const g = base(k); if (k !== "shat") return g; const M = c => new TH.MeshStandardMaterial({ color: c, metalness: .3, roughness: .8 });
  for (const [x, y, z, r, c] of [[150, -40, -160, 60, 0x3a3430], [-210, -60, 120, 44, 0x2c3036], [60, -80, 220, 38, 0x30343a]]) { const p = new TH.Mesh(new TH.IcosahedronGeometry(r, 2), M(c)); p.position.set(x, y, z); p.scale.set(1, .8, 1); g.add(p); const cut = new TH.Mesh(new TH.DodecahedronGeometry(r * .4, 0), M(0x171a1e)); cut.position.set(x + r * .9, y + r * .3, z); g.add(cut); }
  const rg = new TH.IcosahedronGeometry(1, 0), rm = M(0x33373c); for (let i = 0; i < 180; i++) { const a = i * 2.39996, r = 60 + (hash("sb" + i) % 90); const m = new TH.Mesh(rg, rm); m.position.set(Math.cos(a) * r, -6 + (hash("sy" + i) % 14), Math.sin(a) * r); m.scale.setScalar(.4 + (hash("ss" + i) % 12) / 8); g.add(m); }
  return g; }; }
