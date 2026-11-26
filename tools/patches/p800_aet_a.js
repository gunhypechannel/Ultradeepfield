/* ---------- v800 THE AETHERION GATEWAY (stage 1: the gateway, the Command Center, the atlas, safe travel, the Interstice).
   An ancient interdimensional gateway raised from the planet Nhalis at the end of the four Aetherion saga seasons, which follow the first
   ten-season year (seasons 14-17; the saga starts 8 Nov 2027 and the First Aperture opens after its finale on Sat 26 Feb 2028, 6 pm Phoenix).
   Fleets cross through it into realms (pockets of space under the galaxy, each its own map), act there and come home.
   Every transfer is a row in the server's ledger (aet_tx): the server keeps the clock and the order of states, so a transfer can be
   repeated safely and never doubled; ships in a transfer can only be lost, never gained. The save mirrors the ledger and is reconciled
   with it on load and every minute (see aetSync). Offline, the same rules run on this device (aetLocalTx).
   Players see nothing until docs/version.json carries "f": {"aet": 1}; the owner previews the saga weeks and the open gateway.
   Server-versus-server war (the Nexus War) is a later extension: it needs more than one server.
   All lore here is a draft awaiting the owner's approval. ---------- */
const AET_SN = 4, AET_COL = "#5fe8d0", AET_RED = "#d0404a", AET_D = 864e5, AET_WK = 7 * 864e5;
const AET_T0 = () => VP_BASE + (PRO + 10) * VP_LEN; /* season 14 */
const AET_FIN_E = 26 * AET_D + 25 * 3600e3; /* each saga season's finale: its closing Saturday, 6 pm Phoenix */
const AET_OPEN_E = 3 * 28 * 864e5 + AET_FIN_E + 3600e3; /* the gateway opens an hour after the fourth season's finale */
const AET_SAGA = [
  ["The First Contamination", "#7ff0dc", "An unknown proto-molecule infects Vesper Station, awakening an ancient intelligence."],
  ["The Living Station", "#5fe8d0", "Vesper Station gains autonomy, rebuilds itself, and descends on Nhalis."],
  ["The Planet That Awoke", "#3fd8c0", "The infection consumes Nhalis, restructuring the planet into a massive construction system."],
  ["The First Aperture", "#9ff6ea", "Nhalis rises: its reconstructed mass separates from the planet and forms the First Aperture."]];
const AET_CHARGE = 45e3, AET_LIMIT = 3;
/* the clock: ms since the saga began; the owner previews a saga week or the open gateway on his own account */
const aetPrevOn = () => !!(S && S.aetPrev && ownerFree());
const aetFlag = () => !!(G.flags && G.flags.aet);
const aetSeen = () => aetPrevOn() || aetFlag();
function aetE(T) { T = T || now(); if (aetPrevOn()) { const p = S.aetPrev; return p.m === "open" ? AET_OPEN_E + AET_D + Math.max(0, T - p.at) : p.j * VP_LEN + (p.w - 1) * AET_WK + 3600e3 + Math.max(0, T - p.at); }
  const so = G.aetSrv && +G.aetSrv.open; return so ? T - (so - AET_OPEN_E) : T - AET_T0(); }
function aetSaga(T) { const e = aetE(T); if (e < 0 || e >= AET_SN * VP_LEN) return null; const j = Math.floor(e / VP_LEN), es = e - j * VP_LEN; return { j, w: Math.min(4, 1 + Math.floor(es / AET_WK)), es, e }; }
const aetOff = () => !aetPrevOn() && !!(G.aetSrv && G.aetSrv.off === true);
function aetOpen(T) { return aetSeen() && aetE(T) >= AET_OPEN_E; }
const aetOpenAt = () => (G.aetSrv && +G.aetSrv.open) || AET_T0() + AET_OPEN_E;
/* the gateway's flux: one hour a day (a different hour each day, the same for everyone) its field is unstable */
function aetFlux(T) { T = T || now(); const d = Math.floor(T / AET_D), h = hash("aetflux" + d) % 24, s0 = d * AET_D + h * 3600e3; return T >= s0 && T < s0 + 3600e3 ? { s0, end: s0 + 3600e3, integ: 62 + hash("aetint" + d) % 21 } : null; }
function aetNextFlux(T) { T = T || now(); for (let i = 0; i < 3; i++) { const d = Math.floor(T / AET_D) + i, s0 = d * AET_D + (hash("aetflux" + d) % 24) * 3600e3; if (s0 + 3600e3 > T) return s0; } return null; }
const aetInteg = T => { const f = aetFlux(T); return f ? f.integ : 100; };
/* each commander's own record */
function aetS() { if (!S.aet) S.aet = { tx: {}, en: null, hist: [], fr: 0, mk: 0, m: {}, got: {}, sv: {}, kills: {}, dest: "int", seen: {} }; const A = S.aet; A.tx = A.tx || {}; A.hist = A.hist || []; A.m = A.m || {}; A.got = A.got || {}; A.sv = A.sv || {}; A.kills = A.kills || {}; return A; }
/* transit energy: the gateway lends each commander a reserve that recharges; a crossing out costs some, the way home is always free */
const aetEnMax = () => 100 + 20 * aetRes("trans");
function aetEn(T) { T = T || now(); const A = aetS(), mx = aetEnMax(); if (!A.en) return mx; return Math.min(mx, A.en.v + (T - A.en.t) / 3600e3 * 12); }
function aetEnUse(v, T) { T = T || now(); const A = aetS(); A.en = { v: Math.max(0, aetEn(T) - v), t: T }; }
const aetCost = (n, T) => Math.round(clamp(15 + Math.ceil(sumShips(n) / 150) * 5, 15, 60) * (aetFlux(T) ? 1.5 : 1) * (1 - .05 * aetRes("stab")));
const aetSlots = () => Math.min(AET_LIMIT, 1 + (aetRes("trans") >= 2 ? 1 : 0) + (aetRes("trans") >= 4 ? 1 : 0));
const aetRes = k => ((S && S.aet && S.aet.rs) || {})[k] || 0; /* Aetherion Technology levels (v802) */
const aetPow = n => Object.entries(n || {}).reduce((a, [k, v]) => { const d = SH[k] || AL[k]; return a + (d ? (d.atk + d.sh + d.hull / 10) * v : 0); }, 0);
const aetShipsTxt = n => Object.entries(n || {}).filter(([k, v]) => v > 0 && SH[k]).map(([k, v]) => `${fmt(v)} ${SH[k].n}`).join(" · ") || "no ships";
/* ---------- the realms ---------- */
const AET_REALMS = [
  { k: "int", n: "The Interstice", cat: "Cross-Server PvP", sub: "Open for exploration while this is the only server", col: "#5fe8d0", c: [290, -1000, -290], R: 120, tt: 180, art: "art/aet/r_interstice.webp",
    d: "A giant artificial transit dimension: gateway rings hanging in the dark, ancient fortresses, resource fields, neural transit relays and, at its heart, the Central Nexus.",
    has: ["Server arrival zones", "Gateway Anchors", "Dimensional Fortresses", "Ancient Resource Fields", "Neural Transit Relays", "The Central Nexus", "Neutral defenders", "Territorial control points"],
    play: "Exploration, neutral defenders and strategic structures now; server-versus-server warfare when more servers join.", rec: 2.5e6,
    mods: [["Dimensional Instability", "During the gateway's daily flux hour, crossings cost 50% more energy."], ["Aetherion Resonance", "Fleets fighting beside a structure you hold get +5% shields (capped)."]],
    rew: ["Aetherion Fragments", "Dimensional Alloy", "Quantum Matrices", "Ancient Circuitry"] },
  { k: "shat", n: "The Shattered Expanse", cat: "Exploration and Resource Gathering", col: "#8fd8ff", c: [-290, -1000, 290], R: 120, tt: 240, art: "art/aet/r_shattered.webp",
    d: "A fractured planetary system: asteroid clusters, floating planetary fragments, abandoned mining platforms and rare Aetherion deposits.",
    has: ["Resource sectors", "Exploration missions", "Ancient harvesting stations", "Environmental anomalies", "Neutral alien threats", "Alliance gathering objectives", "Rare crafting materials"],
    play: "Exploration, PvE missions, resource competition and crafting progression.", rec: 1.5e6,
    mods: [["Gravitic Shear", "Anomalies slow fleets that fly through them."], ["Rich Veins", "Harvesting stations yield more for each commander working them, up to a cap."]],
    rew: ["Aetherion Fragments", "Quantum minerals", "Dimensional Alloy", "Rare crafting materials"] },
  { k: "dom", n: "The Silent Dominion", cat: "Cooperative PvE", col: "#c8d4e0", c: [290, -1000, 290], R: 120, tt: 300, art: "art/aet/r_dominion.webp",
    d: "An abandoned machine civilisation: dormant factories, ancient intelligences, hidden technology and colossal autonomous guardians.",
    has: ["Machine ruins", "Ancient shipyards", "Advanced enemy fleets", "Cooperative boss encounters", "Research facilities", "Hidden Archives", "Technology rewards"],
    play: "Alliance expeditions and large cooperative encounters.", rec: 6e6,
    mods: [["Dormant Defences", "Ruins wake as fleets approach: the deeper the ruin, the stronger its guard."]],
    rew: ["Quantum Matrices", "Ancient Technology Collectibles", "Rare Research Materials"] },
  { k: "tide", n: "The Primordial Tide", cat: "Faction Expedition", col: "#e8b45a", c: [-290, -1000, -290], R: 120, tt: 300, art: "art/aet/r_tide.webp",
    d: "An ancient oceanic realm tied to the origin of the Carcinid Empire: shell-world fortresses, leviathan graveyards and bioluminescent fields.",
    has: ["Ancient Carcinid cities", "Leviathan graveyards", "Shell-world fortresses", "Bioluminescent resource fields", "Colossal crustacean bosses", "Lost Carcinid technology"],
    play: "Faction exploration, cooperative boss battles and ancient lore.", rec: 5e6,
    mods: [["The Deep Current", "Fleets drift: travel inside the realm takes 20% longer."]],
    rew: ["Abyssal relics", "Aetherion Fragments", "Unique seasonal rewards"] }];
const AET_RB = Object.fromEntries(AET_REALMS.map(R => [R.k, R]));
const AET_READY = { int: 1 }; /* realms that are charted and built (later stages add theirs) */
const AET_REQ = {}; /* extra conditions per realm: k -> T => reason or null (later stages) */
function aetRealmLock(k, T) { T = T || now(); const R = AET_RB[k]; if (!R) return "Unknown realm.";
  if (!aetOpen(T)) return `The Gateway has not opened. It rises from Nhalis at the end of ${AET_SAGA[3][0]}.`;
  if (!AET_READY[k]) return "Not charted yet: the Gateway's pathfinders have not found a stable route here.";
  const why = AET_REQ[k] && AET_REQ[k](T); if (why) return why;
  if (!aetPrevOn() && G.mode === "online" && G.aetSrv && Array.isArray(G.aetSrv.realms) && !G.aetSrv.realms.includes(k)) return "The server has not opened this realm yet.";
  return null; }
const aetRealmPos = k => { const R = AET_RB[k]; return { x: R.c[0], y: R.c[1], z: R.c[2] }; };
/* ---------- Nhalis and the gateway on the galaxy map ---------- */
const AET_NH = { r: 64 * SC, a0: 2.2 };
function aetNhalis(T, out) { const a = AET_NH.a0 + TAU * T / period(AET_NH.r), o = out || {}; o.x = Math.cos(a) * AET_NH.r; o.y = 0; o.z = Math.sin(a) * AET_NH.r; return o; }
function aetGatePos(T, out) { const q = aetNhalis(T, out), L = Math.hypot(q.x, q.z) || 1; q.x += q.x / L * 9; q.z += q.z / L * 9; q.y = 5; return q; }
/* ---------- the ledger: the server's when online, the same rules on this device when not ---------- */
const aetId = () => "tx-" + now().toString(36) + "-" + Math.floor(Math.random() * 1e9).toString(36);
function aetLocalTx(op, id, p) { const T = now(), L = (S.ldb = S.ldb || {}).aetTx = S.ldb.aetTx || {}, r = L[id], tt = (AET_RB[(r || p).realm] || {}).tt || 180, row = x => Object.assign({}, x, { now: T });
  if (op === "reserve") { if (r) return row(r); if (!AET_RB[p.realm]) throw new Error("unknown realm"); if (!sumShips(p.n)) throw new Error("send at least one ship");
    if (Object.values(L).filter(x => x.prev === !!p.prev && !["HOME", "VOID", "LOST"].includes(x.st)).length >= AET_LIMIT) throw new Error("every gateway slot is in use");
    return row(L[id] = { txid: id, realm: p.realm, st: "RESERVED", n: Object.assign({}, p.n), prev: !!p.prev, t_res: T }); }
  if (!r) throw new Error("no such transfer");
  if (op === "depart" && r.st === "RESERVED") { if (T < r.t_res + AET_CHARGE) throw new Error("the gateway is still charging"); Object.assign(r, { st: "IN_TRANSIT", t_out: T, eta: T + tt * 1000 }); }
  else if (op === "arrive" && r.st === "IN_TRANSIT") { if (T < r.eta) throw new Error("still in the corridor"); Object.assign(r, { st: "ACTIVE", t_arr: T }); }
  else if (op === "recall") { if (r.st === "RESERVED") Object.assign(r, { st: "HOME", t_home: T }); else if (r.st === "ACTIVE") Object.assign(r, { st: "RETURNING", t_ret: T, ret_eta: T + tt * 1000 }); }
  else if (op === "home" && r.st === "RETURNING") { if (T < r.ret_eta) throw new Error("still on the way home"); Object.assign(r, { st: "HOME", t_home: T }); }
  else if (op === "losses") { if (!["ACTIVE", "RETURNING"].includes(r.st)) throw new Error("that fleet is not beyond the gateway"); for (const k in p.n) if (p.n[k] > (r.n[k] || 0)) throw new Error("a fleet can only lose ships out there"); r.n = Object.assign({}, p.n); if (!sumShips(r.n)) r.st = "LOST"; }
  else if (op === "void" && !["HOME", "VOID", "LOST"].includes(r.st)) r.st = "VOID";
  return row(r); }
async function aetLedger(op, id, p) { p = p || {}; if (G.mode === "online" && window.udfAet) { const r = await window.udfAet.tx(op, id, p); return r; } return aetLocalTx(op, id, p); }
const aetErr = e => String((e && (e.message || e.msg || e.details)) || e || "error").replace(/^.*?:\s*(?=[a-z])/i, "").slice(0, 120);
/* adopt the ledger's row (the server wins on state, times and ships) */
function aetAdopt(x, r) { if (!r) return; const tm = { t_res: "res", t_out: "out", eta: "eta", t_arr: "arr", t_ret: "ret", ret_eta: "reta", t_home: "home" }; x.t = x.t || {};
  for (const k in tm) if (r[k] != null && !isNaN(+r[k])) x.t[tm[k]] = +r[k] - (r.now ? +r.now - now() : 0); /* server times on this device's clock */
  if (r.n && typeof r.n === "object") x.n = Object.assign({}, r.n); x.st = r.st; x.srv = 1; }
/* ---------- deploy, recall and the ticks that move a transfer along ---------- */
async function aetDeploy(k, n) { const T = now(), A = aetS(), why = aetRealmLock(k, T); if (why) { toast(why, "warn"); return false; }
  if (A.busy && T - A.busy.t < 20e3) { toast("The gateway is already handling a departure.", "warn"); return false; }
  n = Object.fromEntries(Object.entries(n || {}).filter(([s, v]) => SH[s] && v > 0 && s !== "spyProbe").map(([s, v]) => [s, Math.floor(v)]));
  if (!sumShips(n)) { toast("Pick the ships to send through.", "warn"); return false; }
  for (const s in n) if ((S.ships[s] || 0) < n[s]) { toast(`You have ${fmt(S.ships[s] || 0)} ${SH[s].n} at ${S.homeName}.`, "warn"); return false; }
  if (aetOpenTx().length >= aetSlots()) { toast(`All ${aetSlots()} gateway slot${aetSlots() > 1 ? "s are" : " is"} in use. Recall a fleet first.`, "warn"); return false; }
  const cost = aetCost(n, T); if (aetEn(T) < cost) { toast(`This crossing needs ${cost} transit energy; the gateway has ${Math.floor(aetEn(T))} for you. It recharges 12 an hour.`, "warn"); return false; }
  if (aetOff()) { toast("The gateway is closed for maintenance. Returns still work.", "warn"); return false; }
  const id = aetId(); A.busy = { id, t: T }; renderSheet();
  try { const r = await aetLedger("reserve", id, { realm: k, n, prev: aetPrevOn() });
    for (const s in n) if ((S.ships[s] || 0) < n[s]) { try { await aetLedger("recall", id); } catch (e) {} toast("Those ships left on another mission while the gateway answered. Nothing was sent.", "warn"); return false; }
    for (const s in n) S.ships[s] -= n[s]; aetEnUse(cost, T);
    const x = A.tx[id] = { id, realm: k, n: Object.assign({}, n), n0: Object.assign({}, n), hold: {}, prev: aetPrevOn(), cost, t: { res: T } }; aetAdopt(x, r);
    aetHist(x, "reserved"); dirty(); aetCine(x, "out"); return true; }
  catch (e) { toast(`The gateway refused: ${aetErr(e)}. Your fleet stays at ${S.homeName}.`, "warn"); return false; }
  finally { A.busy = null; renderSheet(); } }
async function aetRecall(id) { const A = aetS(), x = A.tx[id]; if (!x || x.lock) return; if (!["RESERVED", "ACTIVE"].includes(x.st)) { toast(x.st === "IN_TRANSIT" ? "It's in the corridor; recall it once it arrives." : "It's already on its way home.", "info"); return; }
  if (S.fleets.some(f => f.aet === id)) { toast("Part of this fleet is out on a mission in the realm. Recall it when every squadron is back at the arrival gate.", "warn"); return; }
  x.lock = 1; try { const r = await aetLedger("recall", id); const was = x.st; aetAdopt(x, r); if (x.st === "HOME") { aetCredit(x); if (was === "RESERVED") { const A2 = aetS(); A2.en = { v: Math.min(aetEnMax(), aetEn() + (x.cost || 0)), t: now() }; } toast("Departure cancelled: the fleet is back home and the energy refunded.", "info"); }
    else { aetHist(x, "recalled"); toast(`${AET_RB[x.realm].n}: fleet recalled. Home in ${ftime((x.t.reta || now()) - now())}.`, "info"); } dirty(); }
  catch (e) { toast(`Recall failed: ${aetErr(e)}. Try again in a moment.`, "warn"); } finally { x.lock = 0; renderSheet(); } }
function aetCredit(x) { if (x.credited) return; x.credited = 1; for (const s in x.n) if (SH[s]) S.ships[s] = (S.ships[s] || 0) + x.n[s];
  const h = x.hold || {}; for (const r of ["m", "c", "g"]) if (h[r]) S.res[r] = (S.res[r] || 0) + h[r]; aetBank(h);
  if (x.st !== "VOID") { aetHist(x, "home"); note(`${AET_RB[x.realm].n}: fleet back through the Gateway${total(h) || h.fr ? " with its hold" : ""}. ${aetShipsTxt(x.n)}.`, "win"); }
  x.done = now(); }
function aetHist(x, what) { const A = aetS(); A.hist.unshift({ id: x.id, realm: x.realm, what, at: now(), n: sumShips(x.n) }); if (A.hist.length > 40) A.hist.length = 40; }
const aetOpenTx = () => Object.values(aetS().tx).filter(x => !x.done && !["HOME", "VOID", "LOST"].includes(x.st));
const aetActive = k => aetOpenTx().filter(x => x.st === "ACTIVE" && (!k || x.realm === k));
async function aetStep(x, op) { if (x.lock) return; x.lock = 1; try { const r = await aetLedger(op, x.id); const was = x.st; aetAdopt(x, r);
    if (x.st !== was) { if (x.st === "ACTIVE") { aetHist(x, "arrived"); note(`${AET_RB[x.realm].n}: fleet arrived through the Gateway. ${aetShipsTxt(x.n)}.`, "win"); aetCine(x, "arrive"); }
      if (x.st === "HOME") aetCredit(x); if (x.st === "IN_TRANSIT") aetHist(x, "departed"); dirty(); softRender(); } x.err = null; }
  catch (e) { x.err = aetErr(e); x.errT = now(); } finally { x.lock = 0; } }
function aetTick() { if (!S || !S.aet || !G.ready) return; const T = now();
  for (const x of Object.values(S.aet.tx)) { if (x.done || x.lock || (x.errT && T - x.errT < 15e3)) continue; const t = x.t || {};
    if (x.st === "RESERVED" && T >= (t.res || 0) + AET_CHARGE + 500) aetStep(x, "depart");
    else if (x.st === "IN_TRANSIT" && t.eta && T >= t.eta + 500) aetStep(x, "arrive");
    else if (x.st === "RETURNING" && t.reta && T >= t.reta + 500) aetStep(x, "home"); }
  for (const id in S.aet.tx) { const x = S.aet.tx[id]; if (x.done && T - x.done > 7 * AET_D) delete S.aet.tx[id]; } }
setInterval(() => { try { aetTick(); } catch (e) {} }, 2000);
/* reconcile the save with the server's ledger: on load and every minute while anything is beyond the gateway */
let AET_SYNC = 0;
async function aetSync(force) { if (!S || !G.ready || G.mode !== "online" || !window.udfAet) return; const T = now(); if (!force && T - AET_SYNC < 60e3) return; AET_SYNC = T;
  try { const st = await window.udfAet.state(); if (st) G.aetSrv = st; } catch (e) {}
  let rows; try { rows = await window.udfAet.mine(); } catch (e) { return; } if (!Array.isArray(rows)) return; const A = aetS(), seen = {};
  for (const r of rows) { seen[r.txid] = 1; const x = A.tx[r.txid];
    if (!x) { if (!["HOME", "VOID", "LOST"].includes(r.st)) try { await aetLedger("void", r.txid); } catch (e) {} continue; } /* the save never took those ships out: cancel it, so nothing is doubled */
    if (x.done) continue; const was = x.st; aetAdopt(x, r);
    if (x.st === "HOME") aetCredit(x); else if (x.st === "LOST") { x.done = now(); aetHist(x, "lost"); } else if (x.st === "VOID") { x.done = now(); }
    if (x.st !== was) dirty(); }
  for (const x of Object.values(A.tx)) if (!x.done && x.srv && !seen[x.id] && !["HOME", "VOID", "LOST"].includes(x.st)) { /* the server has no record of it: bring the fleet home */
    x.st = "HOME"; aetCredit(x); note(`${AET_RB[x.realm].n}: a transfer the server had no record of was recovered; the fleet is home.`, "info"); dirty(); }
  softRender(); }
setInterval(() => { try { if (S && S.aet && (aetOpenTx().length || !AET_SYNC)) aetSync(); } catch (e) {} }, 15e3);
/* what a realm fleet brought back (resources go home with the fleet; fragments and materials into the Aetherion stores) */
const AET_MAT = { fr: ["Aetherion Fragments", "#5fe8d0"], alloy: ["Dimensional Alloy", "#a9c2d4"], qm: ["Quantum Matrices", "#9ff6ea"], circ: ["Ancient Circuitry", "#d8c27a"], min: ["Quantum Minerals", "#7fb8ff"], relic: ["Ancient Technology", "#e0e8f0"] };
function aetBank(h) { const A = aetS(); for (const k in AET_MAT) if (h[k]) { if (k === "fr") A.fr = (A.fr || 0) + h[k]; else A.m[k] = (A.m[k] || 0) + h[k]; } }
const aetMatTxt = L => Object.entries(L || {}).filter(([k, v]) => v > 0 && (AET_MAT[k] || k === "m" || k === "c" || k === "g")).map(([k, v]) => AET_MAT[k] ? `${fmt(v)} ${AET_MAT[k][0]}` : `${fmt(v)} ${({ m: "metal", c: "crystal", g: "gas" })[k]}`).join(", ");
