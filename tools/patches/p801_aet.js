/* ---------- v801 the Interstice: its structures and their neutral defenders, missions from your arrival gate, holds and their bonuses,
   the Central Nexus and its pylons, the Sleeping Intelligence, fragments and materials. Until the Nexus War (which needs other
   servers), every commander's progress here is their own: what you hold, which pylons you broke, what you gathered. ---------- */
const AET_U = {}; for (const k of ["aetDrone", "aetWeaver", "aetSentinel", "aetGuard", "aetWarden", "aetPylon", "aetNexus", "aetIntel"]) AET_U[k] = 1;
{ const U = (n, atk, sh, hull, val) => ({ n, atk, sh, hull, val, one: 1 }); Object.assign(AL, {
  aetDrone: U("Lattice Drone", 420, 300, 5000, 18000), aetWeaver: U("Weaver", 700, 700, 11000, 36000), aetSentinel: U("Interstice Sentinel", 1200, 1500, 24000, 80000),
  aetGuard: U("Anchor Warden", 1500, 2400, 36000, 120000), aetWarden: U("Fortress Warden", 2400, 2800, 56000, 220000), aetPylon: U("Nexus Pylon", 900, 6000, 90000, 300000),
  aetNexus: U("The Nexus Core", 3000, 9000, 260000, 900000), aetIntel: U("The Sleeping Intelligence", 4200, 7000, 220000, 1000000) }); }
Object.assign(MON, {
  aetPat: { n: "Interstice Sentinels", sp: "Neutral patrol", ic: "◈", col: "#5fe8d0", rgb: "95,232,208", per: 99, d: "Ancient constructs that sweep the Interstice's lanes. They answer to no server.", names: ["Sentinels"] },
  aetAnc: { n: "Gateway Anchor", sp: "Gateway Anchor", ic: "◎", col: "#9ff6ea", rgb: "159,246,234", per: 99, d: "A small ring that pins an arrival zone to the Interstice. Hold your server's anchor and crossings cost less energy.", names: ["Anchor"] },
  aetFort: { n: "Dimensional Fortress", sp: "Dimensional Fortress", ic: "⬢", col: "#7ff0dc", rgb: "127,240,220", per: 99, d: "An ancient defensive citadel. Hold it for capped shield and salvage bonuses inside the Interstice.", names: ["Fortress"] },
  aetRel: { n: "Neural Transit Relay", sp: "Transit Relay", ic: "⟟", col: "#5fe8d0", rgb: "95,232,208", per: 99, d: "A spire that bends the Interstice's lanes. Every relay you hold makes travel inside the realm faster.", names: ["Relay"] },
  aetField: { n: "Ancient Resource Field", sp: "Resource Field", ic: "◇", col: "#7fb8ff", rgb: "127,184,255", per: 99, d: "Stone and machinery threaded with Aetherion crystal. Gather it for fragments, quantum minerals and resources.", names: ["Field"] },
  aetPyl: { n: "Nexus Pylon", sp: "Nexus Pylon", ic: "⟠", col: "#9ff6ea", rgb: "159,246,234", per: 99, d: "One of four pylons that shield the Central Nexus. Break all four and the Nexus opens until the day turns.", names: ["Pylon"] },
  aetNex: { n: "The Central Nexus", sp: "The Central Nexus", ic: "✦", col: "#bffff4", rgb: "191,255,244", per: 99, d: "The colossal heart of the Interstice. Shielded by its pylons; once a day it can be assaulted for its greatest rewards.", names: ["Nexus"] },
  aetInt: { n: "The Sleeping Intelligence", sp: "The Sleeping Intelligence", ic: "◉", col: "#d0404a", rgb: "208,64,74", per: 99, d: "Something ancient, older than the Gateway's builders, dreaming at the Interstice's heart. Twice a day it wakes.", names: ["Intelligence"] } });
const AET_M = { aetPat: "aetWeaver", aetAnc: "aetGuard", aetFort: "aetWarden", aetRel: "aetWeaver", aetField: "aetDrone", aetPyl: "aetPylon", aetNex: "aetNexus", aetInt: "aetIntel" };
/* the Interstice's layout, in the realm's own coordinates (its arrival zones at the four corners, the Nexus at the heart) */
const AET_TGT = (() => { const out = [], R = "int", c = AET_RB.int.c, at = (x, y, z) => (T, o) => { o = o || {}; o.x = c[0] + x; o.y = c[1] + y; o.z = c[2] + z; return o; };
  const add = (id, mon, k, name, x, y, z, extra) => out.push(Object.assign({ id, kind: "pirate", mon, aetR: R, aetK: k, lvl: 5, name, mv: at(x, y, z), r: 1, a0: 0, lx: x, lz: z }, extra || {}));
  [["aia0", "Anchor of the Origin", -62, 52, 1], ["aia1", "Anchor Two (dormant)", 62, 52, 0], ["aia2", "Anchor Three (dormant)", 62, -52, 0], ["aia3", "Anchor Four (dormant)", -62, -52, 0]].forEach(([id, n, x, z, own]) => add(id, "aetAnc", "anc", n, x, 2, z, { own }));
  [["aif0", "Fortress Meridia", 0, 95], ["aif1", "Fortress Caldris", 95, 0], ["aif2", "Fortress Ostrava", 0, -95], ["aif3", "Fortress Vael", -95, 0]].forEach(([id, n, x, z]) => add(id, "aetFort", "fort", n, x, 0, z));
  for (let j = 0; j < 6; j++) { const a = j / 6 * TAU + .26; add("air" + j, "aetRel", "rel", `Transit Relay ${["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"][j]}`, Math.cos(a) * 52, 4, Math.sin(a) * 52); }
  [20, 70, 160, 200, 250, 340].forEach((d, j) => { const a = d * Math.PI / 180; add("aid" + j, "aetField", "field", `${["Lumen", "Cinder", "Glass", "Hollow", "Quiet", "Ember"][j]} Field`, Math.cos(a) * 112, -2, Math.sin(a) * 112, { guard: j % 2 === 0 }); });
  for (let j = 0; j < 4; j++) { const a = j / 4 * TAU + Math.PI / 4; add("aip" + j, "aetPyl", "pyl", `Pylon ${["North", "East", "South", "West"][j]}`, Math.cos(a) * 22, 3, Math.sin(a) * 22); }
  add("ain", "aetNex", "nex", "The Central Nexus", 0, 6, 0);
  for (let j = 0; j < 8; j++) { const a0 = j / 8 * TAU; out.push({ id: "ait" + j, kind: "pirate", mon: "aetPat", aetR: R, aetK: "pat", lvl: 5, r: 1, a0, name: `Sentinel Wing ${j + 1}`, mv: (T, o) => { o = o || {}; const a = a0 + T / 9e5 * (j % 2 ? 1 : -1); o.x = c[0] + Math.cos(a) * 76; o.y = c[1] + 3 + Math.sin(T / 4e4 + j) * 2; o.z = c[2] + Math.sin(a) * 76; return o; } }); }
  out.push({ id: "aii", kind: "pirate", mon: "aetInt", aetR: R, aetK: "int", lvl: 5, r: 1, a0: 0, name: "The Sleeping Intelligence", mv: (T, o) => { o = o || {}; const w = aetIntAwake(T), a = T / 3e5; o.x = c[0] + (w ? Math.cos(a) * 36 : 0); o.y = c[1] + (w ? 14 : 34); o.z = c[2] + (w ? Math.sin(a) * 36 : 0); return o; } });
  return out; })();
const AET_TB = Object.fromEntries(AET_TGT.map(x => [x.id, x]));
/* the Sleeping Intelligence wakes twice a day (06:00 and 18:00 UTC, for an hour) */
function aetIntAwake(T) { T = T || now(); const h = (T % AET_D) / 3600e3; return (h >= 6 && h < 7) || (h >= 18 && h < 19); }
function aetIntNext(T) { T = T || now(); const d0 = Math.floor(T / AET_D) * AET_D; for (const t of [d0 + 6 * 3600e3, d0 + 18 * 3600e3, d0 + 30 * 3600e3]) if (t + 3600e3 > T) return t; return d0 + AET_D + 6 * 3600e3; }
const aetIntKey = T => { const t = aetIntNext(T); return Math.floor(t / 3600e3); };
/* personal state: holds, regrouping defenders, the day's pylons and the Nexus, the waking's kill */
const aetDay = T => Math.floor((T || now()) / AET_D);
function aetHeld(id, T) { return (aetS().hold || {})[id] > (T || now()); }
function aetDown(id, T) { return (aetS().dn || {})[id] > (T || now()); }
const AET_REGROUP = { pat: 2 * 3600e3, anc: 8 * 3600e3, fort: 12 * 3600e3, rel: 6 * 3600e3, field: 4 * 3600e3, pyl: 0, nex: 0, int: 0 };
const AET_HOLD = { anc: 24 * 3600e3, fort: 24 * 3600e3, rel: 24 * 3600e3 };
function aetPylDown(id, T) { const A = aetS(); return !!(A.pyl && A.pyl.d === aetDay(T) && A.pyl[id]); }
const aetPylAll = T => AET_TGT.filter(x => x.aetK === "pyl").every(x => aetPylDown(x.id, T));
const aetNexDone = T => { const A = aetS(); return !!(A.nex && A.nex === aetDay(T)); };
const aetIntDone = T => { const A = aetS(); return A.intK === aetIntKey(T); };
/* bonuses from what you hold (all capped) */
function aetBon(T) { T = T || now(); const H = k => AET_TGT.filter(x => x.aetK === k && aetHeld(x.id, T)), sup = aetIntAwake(T);
  const anc = H("anc"), fort = H("fort"), rel = H("rel"); if (sup) return { en: 0, sh: 0, loot: 0, spd: 0, sup: 1 };
  return { en: anc.some(x => x.own) ? .2 : 0, sh: Math.min(.1, .05 * fort.length), loot: Math.min(.25, .05 * fort.length + .05 * anc.filter(x => !x.own).length), spd: Math.min(.3, .05 * rel.length), sup: 0 }; }
/* who defends what */
const AET_FX = {}; /* other realms add their defenders here (v802) */
function aetForce(x, T) { T = T || now(); const k = x.aetK; if (AET_FX[k]) return AET_FX[k](x, T);
  if (k === "pat") return { aetDrone: 8, aetWeaver: 3 }; if (k === "anc") return { aetGuard: 4, aetDrone: 10 }; if (k === "fort") return { aetWarden: 3, aetSentinel: 8, aetDrone: 16 };
  if (k === "rel") return { aetWeaver: 6, aetSentinel: 3 }; if (k === "field") return x.guard ? { aetDrone: 6, aetWeaver: 1 } : {}; if (k === "pyl") return { aetPylon: 1, aetSentinel: 6, aetWarden: 1 };
  if (k === "nex") return { aetNexus: 1, aetWarden: 4, aetSentinel: 10 }; if (k === "int") return { aetIntel: 1, aetDrone: 20, aetSentinel: 4 }; return { aetDrone: 4 }; }
const aetForceTxt = x => { const o = aetForce(x); return Object.keys(o).length ? Object.entries(o).map(([k, v]) => `${v} ${AL[k].n}`).join(" · ") : "Unguarded"; };
const AET_LOOT = { pat: { fr: 4, alloy: 2, m: 20000, c: 12000 }, anc: { fr: 10, circ: 3, m: 30000 }, fort: { fr: 18, alloy: 6, qm: 1, m: 60000, c: 40000 }, rel: { fr: 8, circ: 4, c: 30000 },
  field: { fr: 2, min: 2 }, pyl: { fr: 12, qm: 1 }, nex: { fr: 60, qm: 6, relic: 1, m: 200000, c: 150000, g: 60000 }, int: { fr: 80, qm: 8, relic: 2 } };
function aetLootOf(x, T) { const L = Object.assign({}, AET_LOOT[x.aetK] || {}), b = 1 + (x.aetR === "int" ? aetBon(T).loot : 0) + .1 * aetRes("sig") * (x.aetK === "anom" ? 1 : 0); for (const k in L) L[k] = Math.round(L[k] * b); return L; }
/* why a target can't be attacked right now */
function aetBlock(x, T) { T = T || now(); const k = x.aetK;
  if (aetDown(x.id, T)) return `Its defenders are regrouping: ready in ${ftime(aetS().dn[x.id] - T)}.`;
  if (AET_HOLD[k] && aetHeld(x.id, T)) return `You hold it until ${new Date(aetS().hold[x.id]).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}.`;
  if (k === "pyl" && aetPylDown(x.id, T)) return "Broken for today. Pylons rise again when the day turns (00:00 UTC).";
  if (k === "nex") { if (aetNexDone(T)) return "You already assaulted the Nexus today. It reseals when the day turns (00:00 UTC)."; if (!aetPylAll(T)) return `Shielded by its pylons: ${AET_TGT.filter(y => y.aetK === "pyl" && !aetPylDown(y.id, T)).length} of 4 still stand. Break them first.`; }
  if (k === "int") { if (!aetIntAwake(T)) return `Asleep. It wakes in ${ftime(aetIntNext(T) - T)} (06:00 and 18:00 UTC, for an hour).`; if (aetIntDone(T)) return "You already drove it back this waking."; }
  return null; }
/* ---------- missions from the arrival gate: attack, gather, scout ---------- */
const aetGateAvail = x => Object.fromEntries(Object.entries(x.n || {}).filter(([k, v]) => v > 0 && SH[k]));
function aetBaseOf(f) { const x = aetS().tx[f.aet], k = x ? x.realm : "int"; return { id: "aetb:" + (f.aet || ""), name: `Arrival gate · ${AET_RB[k].n.replace("The ", "")}`, kind: "aetbase", r: 1, a0: 0, mv: (T, o) => aetArrPos(k, o) }; }
function aetTravel(tg, n, k) { const b = { mv: (T, o) => aetArrPos(k, o), r: 1, a0: 0 }; let t = travelMs(b, tg, n, S.r, 100) * .35 * (1 - (k === "int" ? aetBon().spd : 0)) * (1 - .02 * aetRes("logi")) * (typeof aetDrift === "function" ? aetDrift(tg, k) : 1); return Math.max(30e3, Math.round(t)); }
function aetSend(xid, txid, n, mission) { const T = now(), tg = AET_TB[xid], x = aetS().tx[txid];
  if (!tg || !x || x.st !== "ACTIVE" || x.realm !== tg.aetR) { toast("That fleet isn't waiting in this realm.", "warn"); return null; }
  n = Object.fromEntries(Object.entries(n || {}).filter(([k, v]) => v > 0 && SH[k]).map(([k, v]) => [k, Math.min(Math.floor(v), x.n[k] || 0)]).filter(([k, v]) => v > 0));
  if (!sumShips(n)) { toast("Pick ships from the fleet at the gate.", "warn"); return null; }
  if (mission === "spy") { if (!n.spyProbe) { toast("Scouting needs an espionage probe in this fleet.", "warn"); return null; } n = { spyProbe: 1 }; }
  else if (mission === "gather") { if (!aetGK(tg.aetK)) return null; }
  else if (mission === "explore") { if (tg.aetK !== "anom") return null; if (aetS().sv["ex:" + tg.id]) { toast("Already surveyed.", "info"); return null; } }
  else { const why = aetBlock(tg, T); if (why) { toast(why, "warn"); return null; } if (aetGK(tg.aetK)) return null; }
  if (slotsFull()) return null;
  if (S.fleets.some(f => f.aet && f.xid === xid && f.mission === "gather" && f.phase !== "back")) { if (mission === "gather") { toast("Another of your fleets is already gathering there.", "warn"); return null; } }
  for (const k in n) { x.n[k] -= n[k]; if (x.n[k] <= 0) delete x.n[k]; }
  const tt = aetTravel(tg, n, x.realm), hp = aetArrPos(x.realm, {}), f = { id: "f" + (S.seq++), pid: tg.id, xid: tg.id, mission: mission === "gather" ? "gather" : mission === "spy" ? "spy" : mission === "explore" ? "explore" : "attack", n, out: T, arrive: T + tt, tt, back: null, loot: null, phase: "out", ox: hp.x, oy: hp.z, from: null, spd: 100, fuel: 0, aet: txid, all: !sumShips(x.n), aetLoot: {} };
  S.fleets.push(f); dirty(); note(`${aetShipsTxt(n)} left the arrival gate for ${tg.name}. Arrives in ${ftime(tt)}.`, "info"); return f; }
/* a squadron reaches its target */
function aetArrive(f) { const x = AET_TB[f.xid], tt = f.tt || (f.arrive - f.out), T = f.arrive; f.phase = "back"; f.back = T + tt; if (!x) return; const A = aetS();
  if (f.mission === "explore" || x.aetK === "anom") { const key = "ex:" + x.id; if (A.sv[key]) { note(`${x.name} was already surveyed.`, "info"); return; } A.sv[key] = 1; const L = aetLootOf(x, T); aetAddL(f.aetLoot, L); aetMissionBump && aetMissionBump("anom", 1);
    note(`Survey of ${x.name}: ${typeof AET_ANOM_LORE !== "undefined" ? AET_ANOM_LORE[+x.id.slice(3) % AET_ANOM_LORE.length] + " " : ""}In the hold: ${aetMatTxt(L)}.`, "win"); dirty(); return; }
  if (f.mission === "spy") { const key = "sv:" + x.id; let msg = `Scouted ${x.name}: ${aetForceTxt(x)}.`; if (!A.sv[key]) { A.sv[key] = 1; f.aetLoot.fr = (f.aetLoot.fr || 0) + 2; msg += " First survey: +2 Aetherion Fragments in the hold."; } note(msg, "info"); dirty(); return; }
  const force = aetForce(x, T);
  if (aetGK(x.aetK)) { if (f.mission !== "gather") return; if (!x.guard || aetDown(x.id, T)) return aetGatherStart(f, x); } /* a guarded field: beat the guard first */
  else { const why = aetBlock(x, T); if (why) { note(`${x.name}: ${why} Squadron returning, nothing lost.`, "warn"); return; } }
  const mine0 = Object.assign({}, f.n), bon = x.aetR === "int" ? aetBon(T) : { sh: 0, loot: 0 }, A0 = stacksOf(f.n, techElVs(x), G.me); for (const s of A0) s.sh *= 1 + bon.sh;
  const D0 = stacksOf(force, { mon: x.lvl }, "monster"), mods = []; if (bon.sh) mods.push(`Aetherion Resonance: our shields +${Math.round(bon.sh * 100)}%`);
  if (x.aetR === "int" && aetIntAwake(T) && x.aetK !== "int") { const q = x.mv(T, {}), w = AET_TB.aii.mv(T, {}); if (Math.hypot(q.x - w.x, q.z - w.z) < 45) { for (const s of A0) s.atk *= .9; mods.push("The Sleeping Intelligence is near: our firepower −10%"); } }
  const res = simulate(A0, D0), rep = mkRep({ at: T, kind: "attack", title: `${MON[x.mon].n}: ${x.name}`, aUids: [G.me], aName: S.homeName + " Expedition", dName: x.name, mon: x.mon, lvl: x.lvl, ptype: "desert", fortL: 0, alien: true, aet: x.aetR,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
  if (mods.length) note(mods.join(" · "), "info");
  f.n = Object.assign({}, res.aLeft); try { fieldRepair(f, mine0, rep); } catch (e) {}
  if (res.winner === "a") { const L = aetLootOf(x, T); aetAddL(f.aetLoot, L); rep.aetLoot = L; A.kills[x.aetK] = (A.kills[x.aetK] || 0) + 1;
    if (AET_REGROUP[x.aetK]) (A.dn = A.dn || {})[x.id] = T + AET_REGROUP[x.aetK];
    if (AET_HOLD[x.aetK]) (A.hold = A.hold || {})[x.id] = T + AET_HOLD[x.aetK];
    if (x.aetK === "pyl") { if (!A.pyl || A.pyl.d !== aetDay(T)) A.pyl = { d: aetDay(T) }; A.pyl[x.id] = 1; if (aetPylAll(T)) note("Every pylon is down: the Central Nexus is open until the day turns.", "win"); }
    if (x.aetK === "nex") A.nex = aetDay(T); if (x.aetK === "int") A.intK = aetIntKey(T);
    if (aetGK(x.aetK)) { (A.dn = A.dn || {})[x.id] = T + (AET_REGROUP[x.aetK] || AET_REGROUP.field); if (f.mission === "gather") { addReport(rep); return aetGatherStart(f, x); } }
    if (typeof aetMissionBump === "function") aetMissionBump(x.aetK, 1);
    note(`${x.name}: ${AET_HOLD[x.aetK] ? "taken and held" : "defenders destroyed"}. In the hold: ${aetMatTxt(L)}.`, "win"); }
  else note(res.winner === "d" ? `${x.name}'s defenders drove our squadron back.` : `Stalemate at ${x.name}. Survivors are pulling back.`, "loss");
  addReport(rep); try { mapClash(x, rep); } catch (e) {}
  if (!sumShips(f.n)) { S.fleets = S.fleets.filter(y => y !== f); aetLossSync(f.aet); } }
const aetAddL = (h, L) => { for (const k in L) h[k] = (h[k] || 0) + L[k]; };
/* gathering a field: two hours at most, faster with more cargo; fragments, quantum minerals and resources */
function aetGatherStart(f, x) { const cap = fCargo(f), hrs = clamp(cap / 200000, .25, 2); f.phase = "gather"; f.gend = f.arrive + hrs * 3600e3; f.haul = { hrs }; f.back = f.gend + (f.tt || 60e3); note(`Gathering at ${x.name} for ${ftime(hrs * 3600e3)}.`, "info"); dirty(); }
let aetGK = k => k === "field" || k === "stat" || k === "dep";
const AET_GY = { field: { fr: 3, min: 6, m: 40000, c: 25000, g: 8000 }, stat: { fr: 3, min: 10, alloy: 2, m: 60000, c: 30000, g: 10000 }, dep: { fr: 9, min: 2, g: 20000 } };
function aetGatherEnd(f) { const x = AET_TB[f.xid], h = (f.haul && f.haul.hrs) || 1, b = 1 + (x && x.aetR === "int" ? aetBon().loot : typeof aetExBon === "function" ? aetExBon() : 0) + .1 * aetRes("harv"), Y = AET_GY[x ? x.aetK : "field"] || AET_GY.field, L = {}; for (const k in Y) L[k] = Math.round(Y[k] * h * b);
  aetAddL(f.aetLoot, L); f.phase = "back"; f.back = f.gend + (f.tt || 60e3); if (typeof aetMissionBump === "function") aetMissionBump("gather", 1); note(`${x ? x.name : "The field"}: gathered ${aetMatTxt(L)}. Heading back to the gate.`, "win"); dirty(); }
/* back at the gate: ships rejoin the fleet there, the hold fills; the server learns of any losses */
function aetHome(f) { const x = aetS().tx[f.aet]; S.fleets = S.fleets.filter(y => y !== f); if (!x) return;
  for (const k in f.n) if (f.n[k] > 0) x.n[k] = (x.n[k] || 0) + f.n[k]; x.hold = x.hold || {}; aetAddL(x.hold, f.aetLoot || {}); if (f.loot) aetAddL(x.hold, f.loot);
  note(`Squadron back at the arrival gate${f.aetLoot && Object.keys(f.aetLoot).length ? `: ${aetMatTxt(f.aetLoot)} into the hold` : ""}.`, "info"); aetLossSync(f.aet); dirty(); }
function aetLossSync(id) { const x = aetS().tx[id]; if (!x) return; const tot = Object.assign({}, x.n); for (const f of S.fleets) if (f.aet === id) for (const k in f.n) tot[k] = (tot[k] || 0) + f.n[k];
  const n0 = x.srvN || x.n0 || {}; let less = false; for (const k in n0) if ((tot[k] || 0) < n0[k]) less = true; if (!less) return;
  const send = Object.fromEntries(Object.keys(n0).map(k => [k, Math.min(n0[k], tot[k] || 0)]));
  aetLedger("losses", id, { n: send }).then(r => { x.srvN = send; if (r && r.st === "LOST" && !sumShips(x.n)) { x.st = "LOST"; x.done = now(); aetHist(x, "lost"); note(`${AET_RB[x.realm].n}: the whole fleet was lost.`, "loss"); dirty(); } }).catch(() => { x.lossPend = 1; }); }
setInterval(() => { try { if (S && S.aet) for (const x of Object.values(S.aet.tx)) if (x.lossPend && !x.done) { x.lossPend = 0; aetLossSync(x.id); } } catch (e) {} }, 30e3);
/* ---------- the target's page ---------- */
function shAetTgt() { const T = now(), x = AET_TB[sheet.id]; if (!x) return ""; const R = AET_RB[x.aetR], why = aetBlock(x, T), held = AET_HOLD[x.aetK] && aetHeld(x.id, T), here = aetActive(x.aetR), A = aetS();
  const tx = here.find(y => y.id === sheet.tx) || here[0]; if (tx) sheet.tx = tx.id; const avail = tx ? aetGateAvail(tx) : {}, pk = tx ? picker(avail) : "", sel = Object.fromEntries(Object.entries(pick).filter(([k, v]) => v > 0 && avail[k]));
  const L = aetLootOf(x, T), bon = x.aetR === "int" ? aetBon(T) : { sup: 0 }, tt = tx && sumShips(sel) ? aetTravel(x, sel, x.aetR) : 0, field = aetGK(x.aetK);
  const hold = { anc: x.own ? "Holding your server's anchor: crossings cost 20% less energy." : "Holding a dormant anchor: +5% salvage in the Interstice.", fort: "+5% shields and +5% salvage in Interstice fights (up to 10% and 25%).", rel: "Travel inside the Interstice 5% faster (up to 30%)." }[x.aetK];
  const status = x.aetK === "int" ? (aetIntAwake(T) ? (aetIntDone(T) ? "Awake · you drove it back this waking" : "AWAKE · its presence weakens fleets fighting near it and suppresses every hold's bonus") : `Asleep · wakes in ${ftime(aetIntNext(T) - T)}`)
    : x.aetK === "nex" ? (aetNexDone(T) ? "Sealed for today" : aetPylAll(T) ? "OPEN · its shield is down until 00:00 UTC" : "Shielded") : held ? "Held by you" : aetDown(x.id, T) ? "Regrouping" : "Guarded by neutral defenders";
  const btns = !tx ? `<p class="note">You need a fleet waiting at your arrival gate in ${esc(R.n)}. <button class="btn" data-act="aetOpen" data-t="fleet">Send one</button></p>`
    : `${here.length > 1 ? `<div class="segc">${here.map(y => `<button class="${y.id === tx.id ? "on" : ""}" data-act="aetTgtTx" data-id="${y.id}">${fmt(sumShips(y.n))} ships</button>`).join("")}</div>` : ""}${pk}
      <dl class="kv"><dt>Squadron</dt><dd>${fmt(sumShips(sel))} ships · power ${fmt(aetPow(sel))} · flight ${tt ? ftime(tt) : "–"}</dd><dt>Defenders</dt><dd>power ${fmt(aetPow(aetForce(x)) || 0)}</dd></dl>
      <div class="aetacts">${x.aetK === "anom" ? `<button class="btn amber" data-act="aetExplore"${sumShips(sel) && !A.sv["ex:" + x.id] ? "" : " disabled"}>${A.sv["ex:" + x.id] ? "Surveyed" : "Survey"}</button>` : field ? `<button class="btn amber" data-act="aetMis" data-m="gather"${sumShips(sel) && !aetDown(x.id, T) || sumShips(sel) && !x.guard ? "" : " disabled"}>${x.guard && !aetDown(x.id, T) ? "Clear the guard and gather" : "Gather"}</button>` : `<button class="btn amber" data-act="aetMis" data-m="attack"${sumShips(sel) && !why ? "" : " disabled"}>${AET_HOLD[x.aetK] ? "Attack and hold" : "Attack"}</button>`}
        <button class="btn" data-act="aetMis" data-m="spy"${avail.spyProbe ? "" : " disabled"}>Scout (1 probe)</button></div>`;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${MON[x.mon].col}">${esc(R.n)} · ${esc(MON[x.mon].sp)}</div><h2>${esc(x.name)}</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="aettg"><p class="note">${esc(MON[x.mon].d)}</p><dl class="kv"><dt>Status</dt><dd>${esc(status)}</dd>${why ? `<dt>Now</dt><dd class="aetlk">${esc(why)}</dd>` : ""}<dt>Defenders</dt><dd>${esc(aetForceTxt(x))}</dd><dt>Rewards</dt><dd>${field ? `per hour gathering: ~${aetMatTxt(AET_GY[x.aetK] || AET_GY.field)}${x.guard ? ` · clearing its guard: ${aetMatTxt(L)}` : ""}` : esc(aetMatTxt(L))}</dd>
    ${hold ? `<dt>If held (24 h)</dt><dd>${esc(hold)}</dd>` : ""}${bon.sup ? `<dt>Bonuses</dt><dd class="aetlk">Suppressed while the Sleeping Intelligence is awake.</dd>` : ""}</dl>${btns}</div>`; }
function aetTapT(id) { if (id.startsWith("t:")) { const x = AET_TB[id.slice(2)]; if (!x) return; for (const k in pick) delete pick[k]; openSheet({ type: "aettgt", id: x.id }); } }
Object.assign(AET_ACT, {
  aetTgtTx: d => { sheet.tx = d.id; for (const k in pick) delete pick[k]; sheet.pkSeen = 0; renderSheet(); },
  aetMis: d => { const x = AET_TB[sheet.id]; if (!x) return; const sel = Object.fromEntries(Object.entries(pick).filter(([k, v]) => v > 0)); const f = aetSend(x.id, sheet.tx, sel, d.m); if (f) { for (const k in pick) delete pick[k]; closeSheet(); } } });
/* ---------- the Interstice drawn: its structures, defenders and the Intelligence ---------- */
function aetStructMesh(x) { const g = new TH.Group(), k = x.aetK, M = (c, e) => new TH.MeshStandardMaterial({ color: c, metalness: .75, roughness: .35, emissive: e || 0x000000, emissiveIntensity: e ? .6 : 0 }), dark = M(0x1a2128), gun = M(0x323c46), teal = aetGlowM(0x5fe8d0, .9);
  const box = (w, h, d, m, x0, y0, z0) => { const b = new TH.Mesh(new TH.BoxGeometry(w, h, d), m); b.position.set(x0 || 0, y0 || 0, z0 || 0); g.add(b); return b; };
  const spire = (r, h, m, x0, z0, y0) => { const c = new TH.Mesh(new TH.ConeGeometry(r, h, 6), m); c.position.set(x0 || 0, (y0 || 0) + h / 2, z0 || 0); g.add(c); const l = new TH.Mesh(new TH.BoxGeometry(.08, h * .7, .08), teal); l.position.set(x0 || 0, (y0 || 0) + h * .42, (z0 || 0) + r * .6); g.add(l); return c; };
  if (k === "anc") { const a = buildAetGate(true); a.scale.setScalar(.42); a.position.y = 4.5; a.lookAt(-x.lx, 4.5, -x.lz); g.add(a); g.userData.gate = a; box(7, 1, 7, gun, 0, -.6, 0); box(1.2, 4, 1.2, dark, 0, 1.4, 0); }
  else if (k === "fort") { for (let i = 0; i < 3; i++) { const t = new TH.Mesh(new TH.CylinderGeometry(9 - i * 2.4, 10 - i * 2.4, 2.2, 8), i % 2 ? gun : dark); t.position.y = i * 2.2; g.add(t); }
    for (let j = 0; j < 8; j++) { const a = j / 8 * TAU; spire(.7, j % 2 ? 6 : 9, dark, Math.cos(a) * 7.2, Math.sin(a) * 7.2, 2); } spire(1.4, 16, gun, 0, 0, 6);
    const r = new TH.Mesh(new TH.TorusGeometry(10.4, .12, 4, 64), teal); r.rotation.x = Math.PI / 2; r.position.y = 1.2; g.add(r); g.userData.ring = r; }
  else if (k === "rel") { const c = new TH.Mesh(new TH.CylinderGeometry(.6, 1.4, 12, 6), gun); c.position.y = 6; g.add(c); spire(.6, 7, dark, 0, 0, 12); const r = new TH.Mesh(new TH.TorusGeometry(2.6, .15, 4, 40), teal); r.position.y = 10; g.add(r); g.userData.spin = r; }
  else if (k === "field") { const rg = new TH.IcosahedronGeometry(1, 0); for (let i = 0; i < 11; i++) { const h = hash(x.id + i), m = new TH.Mesh(rg, i % 3 ? M(0x262c33) : M(0x1c2a30, 0x1f6f66)); m.position.set(((h % 100) - 50) / 6, ((h >> 7) % 40 - 20) / 8, (((h >> 13) % 100) - 50) / 6); m.scale.setScalar(1 + (h % 7) * .5); m.rotation.set(h % 3, h % 5, 0); g.add(m); }
    for (let i = 0; i < 6; i++) { const s = aetSprite(3, "rgba(127,240,220,1)", "aetcrys"); const h = hash(x.id + "c" + i); s.position.set(((h % 100) - 50) / 7, ((h >> 6) % 30) / 10, (((h >> 12) % 100) - 50) / 7); g.add(s); } }
  else if (k === "pyl") { const o = new TH.Mesh(new TH.CylinderGeometry(.4, 1.3, 14, 4), dark); o.position.y = 7; g.add(o); const c = aetSprite(5, "rgba(159,246,234,1)", "aetpyl"); c.position.y = 15; g.add(c); g.userData.core = c;
    for (let i = 0; i < 5; i++) { const s = new TH.Mesh(new TH.OctahedronGeometry(.6, 0), gun); g.add(s); (g.userData.sh = g.userData.sh || []).push(s); } }
  else if (k === "nex") { for (let i = 0; i < 5; i++) { const t = new TH.Mesh(new TH.CylinderGeometry(16 - i * 3, 18 - i * 3, 3, 12), i % 2 ? gun : dark); t.position.y = i * 3 - 6; g.add(t); }
    spire(2.2, 34, gun, 0, 0, 9); for (let j = 0; j < 12; j++) { const a = j / 12 * TAU; spire(.9, 8 + (j % 3) * 4, dark, Math.cos(a) * 12, Math.sin(a) * 12, -1); }
    for (const [r, y, w] of [[19, -3, .2], [13, 4, .16], [8, 12, .12]]) { const t = new TH.Mesh(new TH.TorusGeometry(r, w, 4, 96), teal); t.rotation.x = Math.PI / 2; t.position.y = y; g.add(t); (g.userData.rings = g.userData.rings || []).push(t); }
    const core = aetSprite(16, "rgba(191,255,244,1)", "aetnexc"); core.position.y = 22; g.add(core); g.userData.core = core; }
  else if (k === "int") { const s = new TH.Mesh(new TH.IcosahedronGeometry(6, 2), new TH.MeshStandardMaterial({ color: 0x0c1418, metalness: .9, roughness: .25, emissive: 0x1f6f66, emissiveIntensity: .25, flatShading: true }));
    g.add(s); g.userData.body = s; for (let i = 0; i < 26; i++) { const sp = new TH.Mesh(new TH.ConeGeometry(.5, 3 + (hash("ii" + i) % 40) / 10, 4), dark), v = new TH.Vector3().setFromSphericalCoords(6, Math.acos(1 - 2 * ((i + .5) / 26)), i * 2.4); sp.position.copy(v); sp.lookAt(v.clone().multiplyScalar(2)); sp.rotateX(Math.PI / 2); g.add(sp); }
    const e = aetSprite(26, "rgba(208,64,74,1)", "aetinte"); e.material.opacity = 0; g.add(e); g.userData.eye = e; }
  else if (k === "pat") { for (let i = 0; i < 5; i++) { const s = new TH.Group(), b = new TH.Mesh(new TH.ConeGeometry(.5, 2.4, 4), dark); b.rotation.x = Math.PI / 2; s.add(b); const l = aetSprite(1.2, "rgba(95,232,208,1)", "aetpat"); l.position.z = -1.2; s.add(l); s.position.set((i % 3 - 1) * 2.2, (i % 2) * .8, -Math.floor(i / 3) * 2.4); g.add(s); } }
  return g; }
function aetRealmTick(W, rs, R, t, T) { const st = rs.st || (rs.st = {}), q = {};
  for (const x of AET_TGT) { if (x.aetR !== R.k) continue; let m = st[x.id]; if (!m) { m = st[x.id] = aetStructMesh(x); rs.g.add(m); } x.mv(T, q); m.position.set(q.x - rs.g.position.x, q.y - rs.g.position.y, q.z - rs.g.position.z);
    const dn = aetDown(x.id, T), held = AET_HOLD[x.aetK] && aetHeld(x.id, T), U = m.userData;
    if (typeof aetStructTick === "function") aetStructTick(x, m, t, T);
    if (x.aetK === "pat" || x.aetK === "beast") { m.visible = !dn; const a = Math.atan2(q.z - rs.g.position.z, q.x - rs.g.position.x); m.rotation.y = -a + (x.a0 && +x.id.slice(3) % 2 ? 0 : Math.PI); }
    if (U.gate) U.gate.userData.tick(t, held ? 2 : 0, held ? .9 : .15);
    if (U.ring) { U.ring.material.opacity = held ? .9 : dn ? .15 : .45; U.ring.material.color.setHex(held ? 0x9ff6ea : 0x5fe8d0); }
    if (U.spin) { U.spin.rotation.x = t * .001; U.spin.rotation.y = t * .0007; U.spin.material.opacity = held ? 1 : .35; }
    if (x.aetK === "pyl") { const br = aetPylDown(x.id, T); U.core.material.opacity = br ? .05 : .8 + .2 * Math.sin(t * .004); (U.sh || []).forEach((s, i) => { const a = t * .0009 + i / 5 * TAU; s.position.set(Math.cos(a) * 3, 9 + Math.sin(a * 2) * 1.5, Math.sin(a) * 3); s.visible = !br; }); }
    if (x.aetK === "nex") { const open = aetPylAll(T) && !aetNexDone(T); (U.rings || []).forEach((r, i) => { r.rotation.z = t * .0002 * (i % 2 ? 1 : -1); r.material.opacity = open ? .95 : .4; }); U.core.material.opacity = open ? .95 + .05 * Math.sin(t * .006) : .35; U.core.scale.setScalar(open ? 22 : 16); }
    if (x.aetK === "int") { const w = aetIntAwake(T); U.body.rotation.y = t * (w ? .0006 : .00008); U.body.material.emissive.setHex(w ? 0x8a1f28 : 0x1f6f66); U.body.material.emissiveIntensity = w ? .5 + .3 * Math.sin(t * .003) : .18; U.eye.material.opacity = w ? .55 : 0; } }
  /* lines: relay to relay, pylon to Nexus while it stands */
  if (R.k !== "int") return; if (!rs.ln) { const g2 = new TH.BufferGeometry(), N = 64; g2.setAttribute("position", new TH.BufferAttribute(new Float32Array(N * 6), 3)); rs.ln = new TH.LineSegments(g2, new TH.LineBasicMaterial({ color: 0x5fe8d0, transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false })); rs.ln.frustumCulled = false; rs.g.add(rs.ln); }
  const P = rs.ln.geometry.attributes.position.array; let n = 0; const seg = (a, b, y1, y2) => { P[n++] = a.lx; P[n++] = y1; P[n++] = a.lz; P[n++] = b.lx; P[n++] = y2; P[n++] = b.lz; };
  const rel = AET_TGT.filter(x => x.aetK === "rel"); rel.forEach((x, i) => seg(x, rel[(i + 1) % rel.length], 10, 10)); const nx = AET_TB.ain; for (const x of AET_TGT) if (x.aetK === "pyl" && !aetPylDown(x.id, T)) seg(x, nx, 15, 22);
  rs.ln.geometry.setDrawRange(0, n / 3); rs.ln.geometry.attributes.position.needsUpdate = true; rs.ln.material.opacity = .35 + .2 * Math.sin(t * .002); }
function aetRealmOverlay(W, hits, proj, label, cp, k, T) { const q = {}, v = new TH.Vector3(); const cand = [];
  for (const x of AET_TGT) { if (x.aetR !== G.aetView) continue; x.mv(T, q); v.set(q.x, q.y + (x.aetK === "nex" ? 30 : x.aetK === "fort" ? 18 : 10), q.z); const s = proj(v); if (!s) continue; const d = cp.distanceTo(v);
    if ((x.aetK === "pat" || x.aetK === "beast") && aetDown(x.id, T)) continue; hits.push({ aet: "t:" + x.id, x: s[0], y: s[1] + 8, sr: Math.max(14, 160 / d * (x.aetK === "nex" ? 3 : x.aetK === "fort" ? 2 : 1)) }); cand.push([d, x, s]); }
  cand.sort((a, b) => a[0] - b[0]); const used = []; for (const [d, x, s] of cand) { if (used.some(u => Math.abs(u[0] - s[0]) < 90 && Math.abs(u[1] - s[1]) < 16)) continue; if (used.length > 14 && x.aetK !== "nex" && x.aetK !== "int") continue; used.push(s);
    const held = AET_HOLD[x.aetK] && aetHeld(x.id, T), dn = aetDown(x.id, T), col = x.aetK === "int" ? (aetIntAwake(T) ? "#ff7a80" : "#8aa") : held ? "#bffff4" : dn ? "#6a8a8a" : MON[x.mon].col;
    const tag = x.aetK === "int" ? (aetIntAwake(T) ? " · AWAKE" : " · asleep") : x.aetK === "nex" ? (aetNexDone(T) ? " · sealed" : aetPylAll(T) ? " · OPEN" : " · shielded") : x.aetK === "pyl" && aetPylDown(x.id, T) ? " · broken" : held ? " · HELD" : dn ? " · regrouping" : "";
    label(`${MON[x.mon].ic} ${x.name}${tag}`, s[0], s[1], col, x.aetK === "nex" ? 12 : 10); } }
/* ---------- Aetherion constructs for battle and the studio: obsidian hulls, teal seams ---------- */
const AET_UMAT = {}; function aetUMats() { if (AET_UMAT.d) return AET_UMAT; AET_UMAT.d = new TH.MeshStandardMaterial({ color: 0x141a20, metalness: .85, roughness: .3 }); AET_UMAT.g = new TH.MeshStandardMaterial({ color: 0x3a4652, metalness: .8, roughness: .35 }); AET_UMAT.t = aetGlowM(0x5fe8d0, .95); AET_UMAT.r = aetGlowM(0xd0404a, .95); return AET_UMAT; }
function buildAet(k) { const C = aetUMats(), g = new TH.Group(); g.userData.eng = []; g.userData.engCol = [0xbffff4, 0x5fe8d0]; const add = (geo, m, p, r, s) => { const o = new TH.Mesh(geo, m); if (p) o.position.set(...p); if (r) o.rotation.set(...r); if (s) o.scale.set(...s); g.add(o); return o; };
  const L = { aetDrone: 1, aetWeaver: 1.4, aetSentinel: 2, aetGuard: 2.2, aetWarden: 3, aetPylon: 3.2, aetNexus: 5, aetIntel: 4.4 }[k] || 1.5;
  if (k === "aetIntel") { add(new TH.IcosahedronGeometry(L * .5, 1), C.d); for (let i = 0; i < 18; i++) { const v = new TH.Vector3().setFromSphericalCoords(L * .5, Math.acos(1 - 2 * ((i + .5) / 18)), i * 2.4), c = add(new TH.ConeGeometry(L * .06, L * .35, 4), C.g); c.position.copy(v); c.lookAt(v.clone().multiplyScalar(2)); c.rotateX(Math.PI / 2); } add(new TH.SphereGeometry(L * .18, 12, 8), C.r, [0, 0, L * .42]); return g; }
  if (k === "aetPylon" || k === "aetNexus") { add(new TH.CylinderGeometry(L * .08, L * .24, L, 6), C.d, [0, 0, 0]); add(new TH.TorusGeometry(L * .3, L * .02, 4, 32), C.t, [0, L * .1, 0], [Math.PI / 2, 0, 0]); add(new TH.SphereGeometry(L * .1, 10, 8), C.t, [0, L * .55, 0]); if (k === "aetNexus") for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; add(new TH.ConeGeometry(L * .05, L * .5, 5), C.g, [Math.cos(a) * L * .28, -L * .1, Math.sin(a) * L * .28]); } return g; }
  /* ships: a blade hull with a teal spine; the bigger ones grow side vanes and a crown */
  add(new TH.ConeGeometry(L * .16, L, 4), C.d, [0, 0, 0], [Math.PI / 2, 0, Math.PI / 4], [1, 1, .55]); add(new TH.BoxGeometry(L * .04, L * .03, L * .8), C.t, [0, L * .09, -L * .05]);
  if (L >= 1.4) for (const s of [-1, 1]) add(new TH.BoxGeometry(L * .34, L * .03, L * .26), C.g, [s * L * .2, 0, L * .12], [0, s * .3, 0]);
  if (L >= 2) { add(new TH.CylinderGeometry(L * .05, L * .09, L * .25, 6), C.g, [0, L * .14, L * .15]); add(new TH.SphereGeometry(L * .05, 8, 6), C.t, [0, L * .29, L * .15]); }
  const e = add(new TH.SphereGeometry(L * .07, 8, 6), C.t, [0, 0, L * .5]); g.userData.eng.push(e); return g; }
