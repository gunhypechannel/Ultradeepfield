/* ---------- v740 THE RESURRECTION WAR: the Continuum. The third invasion, in every Season of the Ruin (Chapter 8; first run 16 Aug 2027).
   An ancient machine civilisation that found fragments of Omega's consciousness-preservation architecture. A destroyed Continuum
   commander sends its mind to a Resurrection Ark, which rebuilds it, so destroying fleets only buys time: destroying the Arks wins.
   Seven stages over the season's four weeks (stage 7 is the closing Saturday's live battle, Extinction Protocol):
     1 First Contact (days 1-4)  2 Machine Rising (5-8)  3 Immortality Revealed (9-14)  4 Sever the Network (15-18)
     5 The Ark Offensive (19-21)  6 The Last Transmission (22-26)  7 Extinction Protocol (27-28)
   The network: four regional Arks (Meridian, Solace, Requiem, Threnody), each fed by three Resurrection Relays on its own orbit
   and served by two named commanders. A commander whose sections run out returns 6 hours later, rebuilt at its Ark, while the Ark
   lives, has reconstruction capacity (6) and at least one of its relays is up. Relays come back 12 hours after they fall, unless
   their Ark is gone. A destroyed Ark stays destroyed for the war. Everything is capped: no structure fields more than its listed
   escort, so the machines can never grow without limit.
   Shared record event/cnt {k, sup, con, cday, rk, rel: {id: {hp, down}}, ark: {id: {hp, dead, cap, dmg}}, cmd: {id: {hp, dead, back, res, dmg}}}
   (owner previews use event/cnt_prev). Players see none of it until version.json carries "f": {"cnt": 1}; the owner previews any stage.
   Lore, names and every Advisor line here are drafts awaiting the owner's approval. ---------- */
const CNT_U = {}; for (const k of ["cnint", "cncor", "cnexe", "cnfab", "cnasm", "cndre", "cnrel", "cnark", "cnprime", "cneter", "cncom"]) CNT_U[k] = 1;
{ const U = (n, atk, sh, hull, val) => ({ n, atk, sh, hull, val, one: 1 }); Object.assign(AL, {
  cnint: U("Continuum Interceptor", 860, 300, 6000, 26000), cncor: U("Neural Corvette", 620, 760, 11000, 34000), cnexe: U("Execution Destroyer", 1150, 950, 16000, 52000),
  cnfab: U("Fabrication Carrier", 680, 2400, 36000, 110000), cnasm: U("Assimilation Cruiser", 1300, 1700, 27000, 85000), cndre: U("Continuum Dreadnought", 2600, 2900, 62000, 230000),
  cnrel: U("Resurrection Relay", 600, 3000, 30000, 140000), cnark: U("Resurrection Ark", 1400, 4200, 46000, 500000), cnprime: U("Prime Resurrection Ark", 1800, 5200, 60000, 900000),
  cneter: U("The Eternal Commander", 1500, 3600, 42000, 600000), cncom: U("Continuum Command Frame", 1100, 2600, 32000, 320000) }); }
const CNT_COL = "#ff3346", CNT_GLOW = "#5fd0ff";
Object.assign(MON, {
  cnpat: { n: "Continuum Patrol", sp: "Machine Patrol", ic: "⬡", col: "#ff5a66", rgb: "255,90,102", per: 99, d: "A Continuum patrol: fast machine interceptors and a jamming corvette, sweeping our space with a single red eye. Destroy it before it reports what it saw.", names: ["Patrol"] },
  cnplat: { n: "Fabrication Platform", sp: "Fabrication Platform", ic: "⬡", col: "#ff8a5a", rgb: "255,138,90", per: 99, d: "A machine shipyard anchored in a resource field. Its bays build warships around the clock. Shut it down and the region's patrols thin out.", names: ["Platform"] },
  cnrelay: { n: "Resurrection Relay", sp: "Resurrection Relay", ic: "⬡", col: "#ff2a40", rgb: "255,42,64", per: 99, d: "A neural transmission tower. It links its region's commanders to their Resurrection Ark. While any relay of an Ark stands, that Ark keeps its shield and can rebuild its dead.", names: ["Relay"] },
  cnarkm: { n: "Resurrection Ark", sp: "Resurrection Ark", ic: "⬢", col: "#ff2236", rgb: "255,34,54", per: 99, d: "A colossal machine capital ship. Its chambers rebuild destroyed commanders and its bays build their fleets. Destroy it and its region's machines can no longer come back.", names: ["Ark"] },
  cncmd: { n: "Continuum Commander", sp: "Machine Commander", ic: "⬡", col: "#ff6a7a", rgb: "255,106,122", per: 99, d: "A machine mind in a command frame. Destroy it and, while its Ark lives, it will simply be rebuilt.", names: ["Commander"] },
  cneterm: { n: "The Eternal Commander", sp: "The Eternal Commander", ic: "⬢", col: "#ff1830", rgb: "255,24,48", per: 99, d: "The Continuum's elite commander, a transforming flagship that has never stayed dead.", names: ["Eternal"] } });
const CNT_M = { cnpat: "cnint", cnplat: "cnfab", cnrelay: "cnrel", cnarkm: "cnark", cncmd: "cncom", cneterm: "cneter" };
const CNT_RUN = k => k >= PRO && seaCyc(k) === 7, CNT_LEN = 28 * 864e5, CNT_D = 864e5;
const CNT_STG = [0, 4, 8, 14, 18, 21, 26].map(d => d * CNT_D); /* where each stage starts in the season */
const CNT_FIN = 26 * CNT_D + 25 * 3600e3; /* the finale: Sunday 01:00 UTC, which is Saturday 6 pm in Phoenix */
const CNT_STN = ["", "First Contact", "Machine Rising", "Immortality Revealed", "Sever the Network", "The Ark Offensive", "The Last Transmission", "Extinction Protocol"];
const CNT_STD = ["", "Unknown machine signals cross our space. Their patrols are fast, silent and curious. Find them, destroy them, and decrypt what they carry.",
  "Machine fleets have moved into the resource sectors and built fabrication platforms. Every platform left standing builds more warships.",
  "Commanders we destroyed are back. Something rebuilds them. The network that does it is now visible on the map: relays, and the Arks they feed.",
  "Strike the Resurrection Relays. Every relay that falls weakens its Ark's shield; when all three of an Ark's relays are down, the Ark is exposed.",
  "The regional Arks can be destroyed for good. Every Ark that dies takes its commanders' second lives with it and weakens the final battle.",
  "Every remaining transmission is converging on one point. The Prime Ark is waking. Hold the staging sectors and ready your fleets.",
  "The Prime Resurrection Ark arrives. Saturday at 6 pm Phoenix time, everyone at once."];
const CNT_ARKS = [["ka0", "Ark Meridian", .8], ["ka1", "Ark Solace", 2.37], ["ka2", "Ark Requiem", 3.94], ["ka3", "Ark Threnody", 5.51]];
const CNT_CMDS = [["kc0", "Executor Sarn", 0], ["kc1", "Sentinel Kade-7", 0], ["kc2", "Overseer Mirex", 1], ["kc3", "Arbiter Calyx", 1], ["kc4", "Archivist Hollow", 2], ["kc5", "Herald Null", 2], ["kc6", "Custodian Vire", 3], ["kc7", "Marshal Ixion", 3]];
const CNT_HP = { rel: 60, ark: 160, cmd: 40, eter: 200 }, CNT_CAP = 6, CNT_BACK = 6 * 3600e3, CNT_RELBACK = 12 * 3600e3, CNT_REGROW = 8 * 3600e3, CNT_DAYCAP = 300;
const CNT_R = () => +(LAYERS[0].r1 * .72).toFixed(2);
const CNT_BOSS = {}, CNT_NET = (() => { const out = [], R = CNT_R(), lv = (layerOf(R).n - 1) * 5;
  const add = B => { out.push(B); CNT_BOSS[B.id] = B; MIM_BOSS[B.id] = B; };
  CNT_ARKS.forEach(([id, name, a], i) => {
    add({ id, kind: "pirate", mon: "cnarkm", u: "cnark", cnt: "ark", reg: i, name, hp: CNT_HP.ark, lvl: lv + 9, r: R, a0: +a.toFixed(4), sc: 1.6, art: "ark_side" });
    [.14, -.14, .28].forEach((o, j) => add({ id: `kr${i}${j}`, kind: "pirate", mon: "cnrelay", u: "cnrel", cnt: "rel", reg: i, name: `${name.replace("Ark ", "")} Relay ${j + 1}`, hp: CNT_HP.rel, lvl: lv + 6, r: R, a0: +(a + o).toFixed(4), sc: 1.1, art: "c_relay" })); });
  CNT_CMDS.forEach(([id, name, reg], j) => add({ id, kind: "pirate", mon: "cncmd", u: "cncom", cnt: "cmd", reg, name, hp: CNT_HP.cmd, lvl: lv + 7, r: R, a0: +(CNT_ARKS[reg][2] + (j % 2 ? .44 : -.3)).toFixed(4), sc: 1.2, art: null }));
  add({ id: "ke0", kind: "pirate", mon: "cneterm", u: "cneter", cnt: "eter", reg: -1, name: "The Eternal Commander", hp: CNT_HP.eter, lvl: lv + 12, r: +((LAYERS[3].r0 + LAYERS[3].r1) / 2).toFixed(2), a0: 0, sc: 1.8, art: "c_eternal" });
  return out; })();
const CNT_PATS = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 10, hi = LAYERS[0].r1 - 10, N = 30;
  for (let j = 0; j < N; j++) { const u = (j + .5) / N, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (1.1 + j * 2.399963 * 1.3) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 3 + (j * 3) % 3;
    out.push({ id: "kp" + j, kind: "pirate", mon: "cnpat", pj: j, reg: j % 4, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Continuum Patrol ${["Theta", "Kappa", "Sigma", "Omicron", "Lambda", "Zeta"][j % 6]}-${101 + j * 7}` }); }
  return out; })();
const CNT_PLATS = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 8, hi = LAYERS[1].r1 - 8, N = 24;
  for (let j = 0; j < N; j++) { const u = (j + .6) / N, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (.4 + j * GOLD) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 2 + (j * 5) % 4;
    out.push({ id: "kf" + j, kind: "pirate", mon: "cnplat", fj: j, reg: j % 4, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Fabrication Platform F-${String(j * 37 % 900 + 100)}` }); }
  return out; })();

/* the clock: stage 1-7 in a run, 0 before, 8 after; the owner previews any stage on his own account */
function cntT0(T = now()) { const c = vpSeason(T); for (let k = Math.max(0, c - 1); k <= c + 12; k++) if (CNT_RUN(k) && VP_BASE + k * VP_LEN + CNT_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + (PRO + 7) * VP_LEN; }
const cntPrevOn = () => !!(S && S.cntPrev && S.cntPrev.s && ownerFree());
const cntFlag = () => !!(G.flags && G.flags.cnt);
function cntClock(T) { T = T || now(); if (cntPrevOn()) { const p = S.cntPrev; return { e: CNT_STG[p.s - 1] + 3600e3 + Math.max(0, T - p.at), prev: 1 }; } const t0 = cntT0(T); return { e: T - t0, t0 }; }
function cntStage(T) { const e = cntClock(T).e; if (e < 0) return 0; if (e >= CNT_LEN) return 8; let s = 1; for (let i = 1; i < CNT_STG.length; i++) if (e >= CNT_STG[i]) s = i + 1; return s; }
const cntOn = T => { const s = cntStage(T); return s >= 1 && s <= 7 && (cntPrevOn() || cntFlag()); };
const cntKey = () => cntPrevOn() ? "prev" : String(cntT0());
const cntDoc = () => cntPrevOn() ? "event/cnt_prev" : "event/cnt";
/* when each map target is in play */
const cntEm = x => x.mon === "cnpat" ? (x.pj % 10) * 7 * 3600e3 : x.mon === "cnplat" ? CNT_STG[1] + (x.fj % 12) * 4 * 3600e3 : 0;
function cntLive(x, T) { if (!cntOn(T)) return false; const s = cntStage(T), e = cntClock(T).e; if (s >= 7) return false; if (x.mon === "cnpat") return e >= cntEm(x); if (x.mon === "cnplat") return s >= 2 && e >= cntEm(x); return false; }
function cntBossOn(B, T) { if (!cntOn(T)) return false; const s = cntStage(T); if (s >= 7) return false; return B.cnt === "eter" ? s >= 6 : s >= 3; }
function cntHid(x, T) { const B = CNT_BOSS[x.id]; if (B) { if (!cntBossOn(B, T)) return true; const st = cntStC(T); if (B.cnt === "ark") return !!st.ark[B.id].dead; if (B.cnt === "rel") return !!st.rel[B.id].down; if (B.cnt === "cmd" || B.cnt === "eter") { const c = st.cmd[B.id]; return !!(c.dead || c.back > T); } return false; } return !cntLive(x, T); }
/* the shared record */
function cntRaw() { return G.mode === "online" ? (G.cntDoc || {})[cntDoc()] || null : ((S && S.ldb) || {})[cntDoc()] || null; }
function cntNorm(src, T) { T = T || now(); const k = cntKey(); let o = src && src.k === k ? JSON.parse(JSON.stringify(src)) : null;
  if (!o) o = { k, sup: 0, con: {}, cday: {}, rk: 0, rel: {}, ark: {}, cmd: {} }; o.sup = +o.sup || 0; o.con = o.con || {}; o.cday = o.cday || {}; o.rk = +o.rk || 0; o.rel = o.rel || {}; o.ark = o.ark || {}; o.cmd = o.cmd || {};
  for (const B of CNT_NET) { if (B.cnt === "ark") { const a = o.ark[B.id] = o.ark[B.id] || {}; a.hp = a.hp == null ? B.hp : +a.hp; a.cap = a.cap == null ? CNT_CAP : +a.cap; a.dead = +a.dead || 0; a.dmg = a.dmg || {}; }
    else if (B.cnt === "rel") { const r = o.rel[B.id] = o.rel[B.id] || {}; r.hp = r.hp == null ? B.hp : +r.hp; r.down = +r.down || 0; r.dmg = r.dmg || {}; }
    else { const c = o.cmd[B.id] = o.cmd[B.id] || {}; c.hp = c.hp == null ? B.hp : +c.hp; c.dead = +c.dead || 0; c.back = +c.back || 0; c.res = +c.res || 0; c.dmg = c.dmg || {}; } }
  for (const B of CNT_NET) if (B.cnt === "rel") { const r = o.rel[B.id], arkDead = o.ark[CNT_ARKS[B.reg][0]].dead; if (r.down && !arkDead && T - r.down >= CNT_RELBACK) { r.down = 0; r.hp = B.hp; } } /* a relay rebuilds itself, unless its Ark is gone */
  return o; }
let CNTC = {};
function cntStC(T) { const src = cntRaw(), d = cntDoc(); if (CNTC.src === src && CNTC.d === d && Math.abs(T - CNTC.t) < 2000) return CNTC.s; const s = cntNorm(src, T); CNTC = { src, d, t: T, s }; return s; }
function cntLocal(cur) { if (G.mode === "online") { G.cntDoc = G.cntDoc || {}; G.cntDoc[cntDoc()] = cur; } else { S.ldb = S.ldb || {}; S.ldb[cntDoc()] = cur; } CNTC = {}; }
const cntArkOf = B => CNT_ARKS[B.reg] ? CNT_ARKS[B.reg][0] : null;
const cntRelUp = (st, reg) => CNT_NET.filter(B => B.cnt === "rel" && B.reg === reg && !st.rel[B.id].down).length;
const cntShield = (st, reg) => cntRelUp(st, reg) > 0; /* an Ark is shielded while any of its relays stands */
const cntCanRes = (st, reg) => { if (reg < 0) return true; const a = st.ark[CNT_ARKS[reg][0]]; return !a.dead && a.cap > 0 && cntRelUp(st, reg) > 0; };
function cntWar(st) { const arks = CNT_ARKS.filter(([id]) => st.ark[id].dead).length, perm = CNT_NET.filter(B => B.cnt === "cmd" && st.cmd[B.id].dead).length, n = Object.keys(st.con).length;
  return Math.min(100, Math.round(40 * arks / 4 + 20 * perm / 8 + 15 * Math.min(1, st.rk / 12) + 25 * Math.min(1, st.sup / (300 + 90 * n)))); }
/* each player's own record */
function cntS() { const k = cntKey(); if (!S.cnt || S.cnt.k !== k) S.cnt = { k, m: {}, pts: 0, got: {}, wk: {}, sv: {}, kills: { pat: 0, plat: 0, rel: 0, ark: 0, cmd: 0 }, pend: 0 }; return S.cnt; }
const CNT_MAT = { echo: ["Neural Echoes", "#ff5a66"], alloy: ["Machine Alloy", "#a8b0bc"], circ: ["Continuum Circuitry", "#ff8a5a"], cell: ["Crimson Reactor Cell", "#ff2236"], core: ["Resurrection Core", "#ff4060"], matrix: ["Quantum Neural Matrix", "#5fd0ff"] };
const cntMatTxt = L => Object.entries(L).filter(([k, v]) => CNT_MAT[k] && v > 0).map(([k, v]) => `${fmt(v)} ${CNT_MAT[k][0]}`).join(", ");
function cntAddM(L) { const M = cntS(); for (const k in CNT_MAT) if (L[k]) M.m[k] = (M.m[k] || 0) + L[k]; }
/* what each target fields: escorts grow by stage; a destroyed Ark leaves its region's garrisons a quarter weaker (capped everywhere) */
function cntForce(x, T) { T = T || now(); const n = 1 + Math.floor(x.lvl / 4), s = Math.max(1, Math.min(6, cntStage(T))); let o;
  if (x.mon === "cnpat") { o = { cnint: 2 + (n >> 1), cncor: 1 + Math.floor(n / 4) }; if (s >= 4) o.cnexe = 1; if (s >= 6) o.cnasm = 1; }
  else { o = { cnfab: 1, cnint: 2 + (n >> 1), cnexe: 1 + Math.floor(n / 5) }; if (s >= 4) o.cnasm = 1; if (s >= 6) o.cndre = 1; o.cnint += 3 * o.cnfab; } /* Drone Fabrication: each carrier launches three interceptors */
  try { const st = cntStC(T), a = CNT_ARKS[x.reg] && st.ark[CNT_ARKS[x.reg][0]]; if (a && a.dead) for (const k in o) o[k] = Math.max(1, Math.ceil(o[k] * .75)); } catch (e) {}
  return o; }
const cntForceTxt = x => Object.entries(cntForce(x)).map(([k, v]) => `${v} ${AL[k].n}`).join(" · ");
/* the machine tactics: each a real effect, shown in the report, each with a counter */
const CNT_TAC = { jam: ["Signal Jamming", "Neural Corvettes jam our shield harmonics: our shields −15%.", "Destroy the corvettes first; fewer corvettes, shorter jamming."], coord: ["Coordinated Fire", "Two or more Execution Destroyers synchronise their guns: machine firepower +10%.", "Hit with fast hulls before they line up."],
  fab: ["Drone Fabrication", "Each Fabrication Carrier launches three extra Interceptors.", "Platforms and Arks with no bays left launch none."], repair: ["Repair Swarm", "Assimilation Cruisers patch their allies: machine hulls +10%.", "Capped at 10%; it cannot heal past that."],
  overload: ["Neural Overload", "A dying Dreadnought's reactor pulses: our shields −10%.", "Only while a Dreadnought fights."], adapt: ["Adaptive Targeting", "Commanders read our attack patterns: machine firepower +10%.", "Never more than 10%."],
  recon: ["Neural Reconstruction", "A destroyed commander is rebuilt at its Ark 6 hours later.", "Break the Ark's relays, then the Ark itself."], transfer: ["Continuity Transfer", "A commander about to die sends its mind to its Ark.", "No Ark, no capacity or no relay: the transfer fails and it dies for good."] };
function cntMods(force, B) { const m = { pA: 1, pS: 1, bA: 1, bH: 1 }, tac = []; if (force.cncor) { m.pS *= .85; tac.push("jam"); } if ((force.cnexe || 0) >= 2) { m.bA *= 1.1; tac.push("coord"); } if (force.cnfab) tac.push("fab");
  if (force.cnasm) { m.bH *= 1.1; tac.push("repair"); } if (force.cndre) { m.pS *= .9; tac.push("overload"); } if (B && (B.cnt === "cmd" || B.cnt === "eter")) { m.bA *= 1.1; tac.push("adapt"); } return { m, tac }; }
/* a patrol or a platform: the usual hunt, with the machine tactics applied */
function cntFight(x, f) { if (!CNT_M[x.mon] || CNT_BOSS[x.id]) return null; const force = xForce(x), Z = cntMods(force, null);
  const A = stacksOf(f.n, techElVs(x), G.me).concat(allyStacks(f.allies, x.lvl)); for (const s of A) { s.sh *= Z.m.pS; s.atk *= Z.m.pA; }
  const D = stacksOf(force, xTech(x), "monster"); for (const s of D) { s.atk *= Z.m.bA; s.hull *= Z.m.bH; } const res = simulate(A, D); res.cntTac = Z.tac; return res; }
function cntLoot(x) { const l = x.lvl; return x.mon === "cnpat" ? { echo: 6 + (l >> 2), alloy: 1 + Math.floor(l / 10), pts: 12 + (l >> 1) } : { echo: 10 + (l >> 2), alloy: 2 + Math.floor(l / 8), circ: 1 + Math.floor(l / 12), pts: 20 + l }; }
const cntWk = (M, s) => M.wk[s] || (M.wk[s] = { pat: 0, plat: 0, sig: 0, scan: 0, rel: 0, ark: 0, cmd: 0, eter: 0 });
function cntWin(x, rep, T) { const M = cntS(), L = cntLoot(x), s = Math.max(1, Math.min(7, cntStage(T))), W = cntWk(M, s); cntAddM(L); M.pts += L.pts;
  if (x.mon === "cnpat") { W.pat++; M.kills.pat++; } else { W.plat++; M.kills.plat++; }
  rep.cnt = L; M.pend = (M.pend || 0) + L.pts; dirty(); cntFlush();
  note(`${x.name} destroyed. Salvaged ${cntMatTxt(L)} · +${L.pts} war points.`, "win"); }
/* noncombat orders: decrypt a patrol's signal or scan a relay by opening its page (once each) */
function cntSurvey(x) { const T = now(), s = cntStage(T); if (!cntOn(T) || s >= 7) return; const M = cntS(), W = cntWk(M, s), key = s + ":" + x.id; if (M.sv[key]) return;
  if (x.mon === "cnpat" && cntLive(x, T)) { M.sv[key] = 1; W.sig++; dirty(); toast(`Signal decrypted from ${x.name}.`, "info"); }
  else if (x.mon === "cnrelay" && s >= 3) { M.sv[key] = 1; W.scan++; dirty(); toast(`${x.name} scanned: its transmission lines are mapped.`, "info"); } }
let CNT_FL = 0;
async function cntFlush(force) { const M = cntS(), T = now(); if (!M.pend || G.cntFlushing || (!force && T - CNT_FL < 90e3) || !G.ready) return; CNT_FL = T; G.cntFlushing = 1;
  try { const ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, T); const add = cntCon(cur, M.pend, T);
    if (await casSet(ref, snap, cur)) { M.pend = 0; cntLocal(cur); dirty(); } } catch (e) {} finally { G.cntFlushing = 0; } }
function cntCon(st, pts, T) { const day = Math.floor(T / 864e5), c = st.cday[G.me] && st.cday[G.me][0] === day ? st.cday[G.me] : [day, 0], add = Math.max(0, Math.min(pts, CNT_DAYCAP - c[1]));
  c[1] += add; st.cday[G.me] = c; st.con[G.me] = (st.con[G.me] || 0) + add; st.sup += add; return add; }
setInterval(() => { try { if (S && S.cnt && S.cnt.pend) cntFlush(); } catch (e) {} }, 60e3);
