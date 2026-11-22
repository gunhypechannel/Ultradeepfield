/* ---------- v703/v704 TIDE OF THE CARCINID (the owner's master prompt) ----------
   v706 the story, tied into the year: beyond the Architects' outer wall lies the Abyss, a sea that runs down to the prison's floor. The
   Carcinid Abyssal Empire ruled it and bred the deep beasts as war mounts; the Architects took the greatest of them, the Leviathan, and
   made it the Warden of their wall. In Chapter 1 (the season before the tide) the Leviathan turns inward: it hears its old masters. The Empire is not
   conquering; something beneath the Abyss (the Unmade) is stirring, and the whole Empire is rising to flee it through the cracks.
   v709 the tide follows the wall breaking: last season's Leviathan hunt (Chapter 1) decides what Korvax rides in week 4: its corpse
   (slain) or the beast itself in chains (escaped).
   The Crown's tide ends one of two ways: slain (the finale, and the Abyss answers) or reborn (it escapes: the Judge counts one seal
   fewer held, the Seal Strain rises, and next year the Crown and Korvax return with harder shells).
   The run (v709): every Season of the Cube (the second season of the ten-season year), from season index 3 (1 February 2027).
   - Week 1, First Tides: 40 Breach Zones open (Stages 1-2), scout patrols chart our worlds.
   - Week 2, The Claw Admirals: 40 more; Stage 3 (Reef Fortress); the Red Claw Marshal and the Pearl Matron take the field.
   - Week 3, The Deep Guardians: the last 40; the Reef Tyrant and the Trench Oracle; the Trench Behemoth, the Krakenbreaker and the
     Pale Sovereign rise.
   - Week 4, The Great Molting: Stage 4 (Abyssal Dominion); Dread Admiral Korvax rides a chained Leviathan; from day 23 the Abyssal Crown
     surfaces and molts through four phases. Kill it and the server sees the finale.
   The wild Kraken is back in the deep layers for good from the first tide (it was retired as a world boss in v700).
   Shared record event/carcinid {k, sup, con, cday, b: {boss id: {hp, dmg: {uid: sections}, dead, last, t}}} (previews use _prev).
   The six Abyssal tactics (each a real effect in the fights that carry it): Shell Armor, Brood Deployment, Tidal Pulse, Molting,
   Monster Resonance, Pincer Lock. Eight materials feed the Abyssal Forge (cosmetics, a hull finish, a planet skin, accelerators, a
   Titan Core); a reward track pays out by tide points, its premium side with Void Pass Premium. */
const CRC_U = {}; for (const k of ["cscut", "cspit", "charv", "cguard", "cbrood", "cwar", "ccrys", "clanc", "cmolt", "ckrak", "cfrig", "cint", "cdest", "cvang", "ccarr", "cpearl", "cmint", "cregent", "cempr", "cbrlord", "cnest", "cmar", "cmat", "ctyr", "cora", "ckor", "cbeh", "ckbr", "cpal", "ccrown", "ccrownm", "clevd"]) CRC_U[k] = 1;
{ const U = (n, atk, sh, hull, val) => ({ n, atk, sh, hull, val, one: 1 }); Object.assign(AL, {
  cscut: U("Scuttle Drone", 380, 320, 5600, 16000), cspit: U("Coral Spitter", 760, 240, 5200, 22000), charv: U("Tide Harvester", 160, 900, 9800, 20000), cguard: U("Shell Guardian", 420, 3000, 28000, 52000),
  cbrood: U("Broodmother", 300, 1800, 24000, 60000), cwar: U("Claw Warrior", 900, 1200, 16000, 48000), ccrys: U("Crystal Reaver", 820, 900, 11000, 40000), clanc: U("Trench Lancer", 1300, 1400, 22000, 70000),
  cmolt: U("Molting Titan", 2800, 2600, 64000, 200000), ckrak: U("The Kraken", 3600, 2400, 90000, 260000),
  cfrig: U("Scuttle Frigate", 600, 800, 12000, 36000), cint: U("Tidal Interceptor", 820, 260, 5800, 24000), cdest: U("Reef Guard Destroyer", 1000, 900, 15000, 46000), cvang: U("Abyssal Vanguard", 1400, 1600, 26000, 80000),
  ccarr: U("Brood Warden Carrier", 700, 2400, 36000, 110000), cpearl: U("Pearl Hunter", 900, 300, 6000, 26000), cmint: U("Molting Interceptor", 1000, 360, 6400, 30000), cregent: U("Tidal Regent", 2600, 2800, 60000, 220000),
  cempr: U("Emperor's Shell", 3400, 3600, 80000, 320000), cbrlord: U("Broodlord Carrier", 1200, 3000, 52000, 180000), cnest: U("Abyssal Breach Nest", 650, 2600, 50000, 90000),
  cmar: U("Red Claw Marshal", 1000, 2200, 30000, 300000), cmat: U("Pearl Matron", 700, 3000, 32000, 300000), ctyr: U("Reef Tyrant", 900, 3600, 38000, 300000), cora: U("Trench Oracle", 1100, 2400, 28000, 300000),
  ckor: U("Dread Admiral Korvax", 1300, 3200, 36000, 400000), cbeh: U("Trench Behemoth", 1000, 4200, 44000, 350000), ckbr: U("Krakenbreaker", 1300, 2600, 34000, 350000), cpal: U("Pale Sovereign", 1200, 3000, 32000, 350000),
  ccrown: U("The Abyssal Crown", 1500, 4000, 42000, 600000), ccrownm: U("The Abyssal Crown, molting", 2300, 1500, 32000, 600000), clevd: U("Leviathan Corpse", 3600, 2400, 80000, 150000) }); }
const CRC_COL = "#e8b45a", CRC_GLOW = "#3fe0c8";
Object.assign(MON, {
  carcinid: { n: "Abyssal Breach Zone", sp: "Breach Zone", ic: "❖", col: CRC_COL, rgb: "232,180,90", per: 99, d: "A tear into the Abyss. Coral and black chitin have grown round the wound, and the Carcinid pour through it: drones, spitters and the shelled guardians of the brood. It grows through four infestation stages, and every stage brings a heavier garrison. Close it before it matures.", names: ["Breach"] },
  crcpat: { n: "Carcinid Scout Patrol", sp: "Scout Patrol", ic: "❖", col: "#5fe0e8", rgb: "95,224,232", per: 99, d: "A Carcinid war patrol charting our worlds for the Abyssal Empire. Sink it before it reports home.", names: ["Patrol"] },
  wkraken: { n: "The Kraken", sp: "Kraken", ic: "✵", col: "#c46aff", rgb: "196,106,255", per: 99, d: "The Kraken has come back up from the Abyss, wild now, its Carcinid riders gone. It drifts through the deep layers and drags down anything that strays close. Slaying one breaks the Abyssal war-song: Dread Admiral Korvax loses his Monster Resonance against you for 12 hours.", names: ["Kraken"] } });
const CRC_BDEF = [ /* id, mon, unit, name, from week, sections, mech, map angle, radius (share of the galaxy), map size, painting, colour, lore */
  ["ca0", "crcmar", "cmar", "The Red Claw Marshal", 2, 100, "pincer", .55, .42, 2, "marshal", "#ff5a5a", "First of the Claw Admirals, a crimson war-crab who leads from the front. Her pincers lock a fleet in place: our ships fight her with a sixth less firepower."],
  ["ca1", "crcmat", "cmat", "The Pearl Matron", 2, 100, "brood", 2.15, .42, 2, "matron", "#e8fbff", "Mother of the broods, crowned in pearls. Her sac never stops: every fight brings a fresh wave of Broodmothers and drones, more the healthier she is."],
  ["ca2", "crctyr", "ctyr", "The Reef Tyrant", 3, 100, "shell", 3.7, .42, 2.1, "tyrant", "#ff9a7a", "A walking reef fortress. His shell turns aside 30% of every blow until the server's Abyssal Suppression passes 50%."],
  ["ca3", "crcora", "cora", "The Trench Oracle", 3, 100, "pulse", 5.3, .42, 2, "oracle", "#b48cff", "The Empire's seer, who hears the tides before they turn. Her Tidal Pulse strips 40% of our fleet's shields."],
  ["ca4", "crckor", "ckor", "Dread Admiral Korvax", 4, 150, "reson", 1.0, .26, 2.4, "korvax", "#ffc870", "Supreme commander of the Abyssal Empire. He rides the Leviathan into battle: alive and in chains if it escaped its hunt at the wall, its corpse if the galaxy slew it. Its war-song makes his fleet 30% tougher and deadlier (15% from a corpse), unless you have slain a wild Kraken in the last 12 hours."],
  ["cg0", "crcbeh", "cbeh", "The Trench Behemoth", 3, 150, "shell", .2, .72, 2.4, "behemoth", "#7ff8e4", "A guardian so old that cities grew on its back. Its shell keeps 40% of every blow off it. It does not heal."],
  ["cg1", "crckbr", "ckbr", "The Krakenbreaker", 3, 150, "pincer", 2.3, .72, 2.3, "krakenbreaker", "#d070ff", "The guardian that tamed the Kraken, with the Kraken's own arms grafted to its shell. Two Krakens fight at its side, and its grip costs our fleet a sixth of its firepower."],
  ["cg2", "crcpal", "cpal", "The Pale Sovereign", 3, 150, "pulse", 4.4, .72, 2.3, "pale", "#e8fbff", "A ghost-white guardian of living crystal. Its Tidal Pulse strips 40% of our shields, and Crystal Reavers swarm around it."],
  ["cc", "crccrown", "ccrown", "The Abyssal Crown", 4, 400, "molt", 3.9, .14, 3.6, "s_crownship", "#ffd07a", "The Emperor of the Abyss, a moon of a crab with a city on its back. It surfaces for the Great Molting: four phases, and if it completes its molt, the Empire is reborn."]];
const CRC_BOSS = {}, CRC_BOSSES = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6;
  for (const [id, mon, u, name, wk, hp, mech, a, f, sc, art, col, d] of CRC_BDEF) { const rad = Math.sqrt(lo * lo + f * (hi * hi - lo * lo)), lvl = (layerOf(rad).n - 1) * 5 + 5;
    const B = { id, kind: "pirate", mon, u, crc: 1, name, wk, hp, mech, lvl, r: +rad.toFixed(2), a0: a, sc, art, guard: id[1] === "g", crown: id === "cc" };
    MON[mon] = { n: name.replace(/^The /, ""), sp: id === "cc" ? "The Crown" : id[1] === "g" ? "Deep Guardian" : "Claw Admiral", ic: "❖", col, rgb: hexRgb(col), per: 99, d, names: [name] }; out.push(B); CRC_BOSS[id] = B; MIM_BOSS[id] = B; }
  return out; })();
function hexRgb(h) { const n = parseInt(h.slice(1), 16); return `${n >> 16 & 255},${n >> 8 & 255},${n & 255}`; }
const CRC_M = { carcinid: "cnest", crcpat: "cpat", wkraken: "ckrak" }; for (const B of CRC_BOSSES) CRC_M[B.mon] = B.u;
const CRC_N = 120, CRC_P = 16, CRC_KN = 6, CRC_WK = 7 * 864e5, CRC_LEN = 28 * 864e5, CRC_REGROW = 12 * 3600e3, CRC_CROWN0 = 3 * CRC_WK + 2 * 864e5;
const CRC_WAVES = 3, CRC_CAP = 4;
const CRC_STAGE = ["", "Breach", "Spawning Tide", "Reef Fortress", "Abyssal Dominion"];
const CRC_WEEKS = [["First Tides", "The Leviathan broke through the Architects' wall, and the wound never closed. Now Breach Zones are tearing open all along it. Scuttle Drones and Coral Spitters pour through, and Carcinid scout frigates are charting our worlds."], ["The Claw Admirals", "The scouts have reported home. The Red Claw Marshal and the Pearl Matron have taken the field, and the nests are hardening into reef fortresses."], ["The Deep Guardians", "The Empire wakes its guardians. The Reef Tyrant and the Trench Oracle join the war, and the oldest things in the Abyss are rising toward the light."], ["The Great Molting", "Dread Admiral Korvax has claimed the Leviathan and rides it to war, and the Abyssal Crown is surfacing to shed its shell. If it completes its molt, the Empire is reborn."]];
const CRC_NESTS = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6;
  for (let j = 0; j < CRC_N; j++) { const u = (j + .7) / CRC_N, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (2.1 + j * GOLD) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 2 + (j * 5) % 4;
    out.push({ id: "cn" + j, kind: "pirate", mon: "carcinid", cj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Breach Zone ${String.fromCharCode(65 + (j * 11) % 26)}${String.fromCharCode(65 + (j * 5 + 7) % 26)}-${100 + j}` }); }
  return out; })();
const CRC_PATS = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 10, hi = LAYERS[0].r1 - 10;
  for (let j = 0; j < CRC_P; j++) { const u = (j + .5) / CRC_P, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (.6 + j * 2.399963 * 1.7) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 3 + (j * 3) % 3;
    out.push({ id: "cp" + j, kind: "pirate", mon: "crcpat", pj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Carcinid Patrol ${["Kesh", "Vorr", "Thal", "Mokk", "Szal", "Ruun", "Qarr", "Ilth"][j % 8]}-${j + 1}` }); }
  return out; })();
const CRC_KRAK = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6;
  for (let j = 0; j < CRC_KN; j++) { const u = .55 + .4 * (j + .5) / CRC_KN, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (1.3 + j * TAU / CRC_KN) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 4;
    out.push({ id: "wk" + j, kind: "pirate", mon: "wkraken", kj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `The Kraken of ${["Thessa", "the Long Dark", "Vhool", "the Drowned Rim", "Morrow", "the Silent Shelf"][j]}` }); }
  return out; })();
const CRC_RUN = k => k >= PRO && seaCyc(k) === 1; /* v709 the Season of the Cube: right after the Leviathan breaks the wall */
function crcT0(T = now()) { const c = vpSeason(T); for (let k = Math.max(0, c - 1); k <= c + 12; k++) if (CRC_RUN(k) && VP_BASE + k * VP_LEN + CRC_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + (PRO + 10) * VP_LEN; }
function crcClock(T) { const p = S && S.crcPrev; if (p && p.w && ownerFree()) return { e: (p.w === 5 ? CRC_CROWN0 + 3600e3 : (p.w - 1) * CRC_WK + 3 * 864e5) + Math.max(0, T - p.at), prev: 1 }; return { e: T - crcT0(T), prev: 0 }; } /* a preview opens three days into the week (W5: the Great Molting) */
const crcWeek = T => { const e = crcClock(T).e; return e < 0 ? 0 : e >= CRC_LEN ? 5 : 1 + Math.floor(e / CRC_WK); };
const crcEm = x => x.mon === "crcpat" ? x.pj * 3 * 3600e3 : Math.floor(x.cj / 40) * CRC_WK + (x.cj % 40) * 1.1 * 3600e3;
const crcKrakOn = T => (S && S.crcPrev && S.crcPrev.w && ownerFree()) || T >= VP_BASE + PRO * VP_LEN; /* the wild Kraken: back for good from the first tide */
function crcLive(x, T) { if (x.mon === "wkraken") return crcKrakOn(T); const e = crcClock(T).e; if (x.mon === "carcinid" && x.cj >= 40 * CRC_WAVES) return false; return e >= crcEm(x) && e < CRC_LEN; }
function crcHid(x, T) { const B = CRC_BOSS[x.id]; if (B) { if (!crcBossOn(B, T)) return true; const s = crcStC(T).b[B.id]; return !!(s && s.dead); } return !crcLive(x, T); }
function crcBossOn(B, T) { const e = crcClock(T).e; return e < CRC_LEN && (B.crown ? e >= CRC_CROWN0 : e >= (B.wk - 1) * CRC_WK); }
function crcStage(x, T) { if (x.mon !== "carcinid") return 1; const c = crcClock(T), down = ((S && S.pir) || {})[x.id] || 0, born = Math.max(crcEm(x), down ? down - T + c.e : -1e15), wk = Math.max(1, Math.min(4, 1 + Math.floor(c.e / CRC_WK)));
  return Math.max(1, Math.min(1 + Math.floor(Math.max(0, c.e - born) / (3 * 864e5)), wk >= 4 ? 4 : Math.min(3, wk + 1), CRC_CAP)); }
function crcForce(x, T) { T = T || now(); const n = 1 + Math.floor(x.lvl / 4), sup = crcSupPct(crcStC(T)) >= 1, w = Math.max(1, Math.min(4, crcWeek(T)));
  let o; if (x.mon === "wkraken") return { ckrak: 1 + Math.floor(x.lvl / 12) };
  if (x.mon === "crcpat") { o = { cfrig: 1 + Math.floor(n / 3), cint: 2 + (n >> 1) }; if (w >= 2) o.cpearl = 1 + (n >> 2); if (w >= 3) { o.cdest = 1; o.cmint = 1 + (n >> 2); } if (w >= 4) { o.cvang = 1; o.ccarr = 1; } }
  else { const st = crcStage(x, T); o = { cnest: 1, cscut: 2 + n, charv: 1, cspit: 1 };
    if (st >= 2) { o.cscut += 1; o.cspit = 1 + (n >> 1); o.cguard = 1 + Math.floor(n / 4); o.cfrig = 1; }
    if (st >= 3) { o.cbrood = 1; o.cscut += 2; o.cwar = 1 + Math.floor(n / 4); o.ccrys = 1; o.cdest = 1; } /* Brood Deployment: every Broodmother brings two more drones */
    if (st >= 4) { o.cmolt = 1; o.clanc = 1 + Math.floor(n / 5); o.cguard += 1; o.cvang = 1; } }
  if (sup) for (const k in o) if (k !== "cnest") o[k] = Math.max(1, Math.ceil(o[k] * .75)); /* a full Suppression Meter thins every garrison by a quarter */
  return o; }
const crcForceTxt = x => Object.entries(crcForce(x)).filter(([k]) => k !== "cnest").map(([k, v]) => `${v} ${AL[k].n}`).join(" · ");
/* the eight materials */
const CRC_MAT = { chitin: ["Abyssal Chitin", "#e8b45a"], coral: ["Coral Alloy", "#ff7ab0"], resin: ["Tidal Resin", "#3fe0c8"], enzyme: ["Brood Enzyme", "#7ff8e4"], pearl: ["Pearl Core", "#e8fbff"], rcrystal: ["Ancient Reef Crystal", "#9fd8ff"], eshell: ["Emperor Shell Fragment", "#d8b070"], crown: ["Crown Reactor Shard", "#ffd07a"] };
const CRC_MSRC = { chitin: "every Breach Zone", coral: "Stage 2+ Breach Zones", resin: "scout patrols", enzyme: "Stage 3+ Breach Zones and wild Krakens", pearl: "Stage 4 Breach Zones and the Pearl Matron", rcrystal: "the Deep Guardians", eshell: "the Claw Admirals", crown: "the Abyssal Crown" };
const crcKey = () => (S && S.crcPrev && S.crcPrev.w ? "p" : "") + String(crcT0()); /* an owner preview keeps its own tally */
function crcS() { const k = crcKey(); if (!S.crc || S.crc.k !== k) S.crc = { k, m: {}, pts: 0, kills: [0, 0, 0, 0, 0], wk: {}, got: {} }; return S.crc; }
function crcLoot(x, st) { if (x.mon === "wkraken") return { enzyme: 3 + Math.floor(x.lvl / 8), chitin: 4, pts: 40 + x.lvl };
  return x.mon === "crcpat" ? { chitin: 1 + Math.floor(x.lvl / 10), resin: 2 + Math.floor(x.lvl / 6), pts: 15 + (x.lvl >> 1) } : { chitin: 2 + st * 2 + Math.floor(x.lvl / 5), coral: st >= 2 ? st : 0, enzyme: st >= 3 ? st - 2 : 0, pearl: st >= 4 ? 1 + (x.lvl >= 20 ? 1 : 0) : 0, pts: 25 * st + x.lvl }; }
const crcWk = (M, w) => { M.wk = M.wk || {}; const W = M.wk[w] || (M.wk[w] = {}); W.sv = W.sv || {}; for (const k of ["nest", "pat", "coral", "st3", "boss", "grd", "crn", "krk"]) W[k] = W[k] || 0; return W; };
const crcMatTxt = L => Object.keys(CRC_MAT).filter(k => L[k]).map(k => `${L[k]} ${CRC_MAT[k][0]}`).join(", ");
function crcAddM(L) { const M = crcS(); for (const k in CRC_MAT) if (L[k]) M.m[k] = (M.m[k] || 0) + L[k]; }
function crcWin(x, rep, T) { const st = crcStage(x, T), M = crcS(), L = crcLoot(x, st), w = Math.max(1, Math.min(4, crcWeek(T))), W = crcWk(M, w), on = crcWeek(T) >= 1 && crcWeek(T) <= 4;
  if (x.mon === "wkraken") { const K0 = S.crcKrk = S.crcKrk || {}; K0.at = T; K0.n = (K0.n || 0) + 1; if (!on) { crcAddM({ enzyme: L.enzyme }); note(`${x.name} is dead. Salvaged ${L.enzyme} Brood Enzyme. Korvax's Monster Resonance is broken against you for 12 hours.`, "win"); dirty(); return; } W.krk++; }
  crcAddM(L); M.pts += L.pts; if (x.mon === "crcpat") { W.pat++; M.pat = (M.pat || 0) + 1; } else if (x.mon === "carcinid") { W.nest++; if (st >= 3) W.st3++; M.kills[st] = (M.kills[st] || 0) + 1; } W.coral += L.coral || 0; try { crcQueue(L.pts); } catch (e) {}
  rep.crc = Object.assign({ st }, L); dirty();
  note(x.mon === "wkraken" ? `${x.name} is dead. Salvaged ${crcMatTxt(L)} · +${L.pts} tide points. Korvax's Monster Resonance is broken against you for 12 hours.` : x.mon === "crcpat" ? `${x.name} sunk. Salvaged ${crcMatTxt(L)} · +${L.pts} tide points.` : `${x.name} closed at Stage ${st} (${CRC_STAGE[st]}). Salvaged ${crcMatTxt(L)} · +${L.pts} tide points.`, "win"); }
/* the week's exploration orders: [id, text, need, shards, {material: n}] */
const CRC_OBJW = { 1: [["sv", "Chart 3 Breach Zones (open one you have explored on the map)", 3, 5, { resin: 4 }], ["nest", "Close 3 Breach Zones", 3, 10, { chitin: 15 }], ["pat", "Sink 2 Carcinid patrols", 2, 8, { resin: 6 }], ["coral", "Salvage 10 Coral Alloy", 10, 10, { chitin: 10 }]],
  2: [["sv", "Chart 5 Breach Zones", 5, 5, { resin: 6 }], ["st3", "Close 2 Reef Fortresses (Stage 3 or above)", 2, 12, { enzyme: 4 }], ["boss", "Break 10 sections off a Claw Admiral", 10, 15, { eshell: 2 }], ["krk", "Slay a wild Kraken", 1, 10, { enzyme: 3 }]],
  3: [["nest", "Close 5 Breach Zones", 5, 12, { chitin: 25 }], ["grd", "Break 10 sections off a Deep Guardian", 10, 15, { rcrystal: 3 }], ["boss", "Break 15 sections off the Claw Admirals", 15, 15, { eshell: 3 }], ["pat", "Sink 4 Carcinid patrols", 4, 10, { resin: 10 }]],
  4: [["st3", "Close 4 Breach Zones at Stage 3 or above", 4, 15, { pearl: 2 }], ["boss", "Break 10 sections off Dread Admiral Korvax or any admiral", 10, 20, { eshell: 4 }], ["crn", "Break 5 sections off the Abyssal Crown", 5, 25, { crown: 1 }], ["krk", "Slay a wild Kraken", 1, 10, { enzyme: 4 }]] };
const crcObjs = w => CRC_OBJW[w] || CRC_OBJW[1];
function crcObjN(w, id) { const W = crcWk(crcS(), w); return id === "sv" ? Object.keys(W.sv).length : W[id] || 0; }
function crcSurvey(x) { const T = now(), w = crcWeek(T); if (w < 1 || w > 4 || !crcLive(x, T) || x.mon !== "carcinid") return; const W = crcWk(crcS(), w); if (!W.sv[x.id]) { W.sv[x.id] = 1; dirty(); } }
/* the Abyssal Suppression Meter, and the shared health of the admirals, guardians and the Crown */
const CRC_DAYCAP = 300, CRC_SUPM = [[25, 5, 4], [50, 8, 6], [75, 12, 8], [100, 20, 12]];
const crcDoc = () => "event/carcinid" + (S && S.crcPrev && S.crcPrev.w ? "_prev" : "");
function crcRaw() { return G.mode === "online" ? (G.crcDoc || {})[crcDoc()] || null : ((S && S.ldb) || {})[crcDoc()] || null; }
const CRC_REGEN = { ca0: 2, ca1: 2, ca2: 2, ca3: 2, ca4: 3 };
function crcNorm(src, T) { T = T || now(); const k = crcKey(); let o = src && src.k === k ? src : null;
  if (!o) { o = { k, hist: Object.assign({}, (src && src.hist) || {}) }; if (src && src.k && src.b && src.b.cc) o.hist[src.k] = src.b.cc.dead ? "win" : "esc"; } /* v706 how each tide ended */
  o.sup = +o.sup || 0; o.con = o.con || {}; o.cday = o.cday || {}; o.b = o.b || {}; o.hist = o.hist || {}; const pe = o.hist[String(+k.replace(/^p/, "") - 10 * VP_LEN)] === "esc";
  CRC_BOSS.cc.hp = pe ? 500 : 400; CRC_BOSS.ca4.hp = pe ? 190 : 150; /* the Crown escaped last time: it and Korvax return with harder shells */
  for (const B of CRC_BOSSES) { let A = o.b[B.id]; if (!A) A = o.b[B.id] = { hp: B.hp, dmg: {}, dead: 0, last: "", t: T }; A.dmg = A.dmg || {};
    const rg = CRC_REGEN[B.id] || 0; if (rg && !A.dead && A.hp < B.hp) { const add = Math.floor((T - (A.t || T)) / 3600e3 * rg); if (add > 0) { A.hp = Math.min(B.hp, A.hp + add); A.t = T; } } }
  return o; }
let CSC = {};
function crcStC(T) { const src = crcRaw(), d = crcDoc(); if (CSC.src === src && CSC.d === d && Math.abs(T - CSC.t) < 2000) return CSC.st; CSC = { src, d, t: T, st: crcNorm(src ? jcopy(src) : null, T) }; return CSC.st; }
function crcSupPct(st) { const n = Object.keys(st.con).length; return Math.min(1, st.sup / (300 + 90 * n)); }
function crcCon(st, pts, T) { const day = Math.floor(T / 864e5), c = st.cday[G.me] && st.cday[G.me][0] === day ? st.cday[G.me] : [day, 0], add = Math.max(0, Math.min(pts, CRC_DAYCAP - c[1]));
  c[1] += add; st.cday[G.me] = c; st.con[G.me] = (st.con[G.me] || 0) + add; st.sup += add; return add; }
function crcQueue(pts) { const M = crcS(); M.pend = (M.pend || 0) + pts; dirty(); crcFlush(); }
let CRC_FL = 0;
function crcLocal(cur) { if (G.mode === "online") { G.crcDoc = G.crcDoc || {}; G.crcDoc[crcDoc()] = cur; } CSC = {}; }
async function crcLock(ref) { for (let i = 0; i < 8; i++) { const r = ref.acquire ? await ref.acquire({ holder: G.me, ttlMs: 15000 }) : { acquired: 1 }; if (r.acquired) return; await sleep(1300); } }
async function crcFlush(force) { const M = crcS(), T = now(); if (!M.pend || G.crcFlushing || (!force && T - CRC_FL < 120e3) || !G.ready) return; CRC_FL = T; G.crcFlushing = 1;
  try { const ref = adb().doc(crcDoc()); await crcLock(ref); const snap = await casGet(ref), cur = crcNorm(snap.exists ? snap.data() : null, T); crcCon(cur, M.pend, T);
    if (await casSet(ref, snap, cur)) { M.pend = 0; crcLocal(cur); dirty(); } } catch (e) {} finally { G.crcFlushing = 0; } }
setInterval(() => { try { if (S && S.crc && S.crc.pend) crcFlush(); } catch (e) {} }, 60e3);
/* ---------- the boss fights: each section of an admiral, guardian or the Crown is one unit; the tactics bend the fight ---------- */
const CRC_PHN = ["", "The Shell Holds", "The Brood Wakes", "The Great Molting", "The Crown Reborn"];
const crcPh = hp => hp > 300 ? 1 : hp > 200 ? 2 : hp > 100 ? 3 : 4; /* a harder shell (500) only lengthens the first phase */
/* v706 what became of the Leviathan in its hunt (Chapter 1, the finale of the season before the tide): "dead" if the galaxy slew it, else "alive" */
function crcLevFate(T) { const p = S && S.crcPrev; if (p && p.w && p.lev && ownerFree()) return p.lev; try { const s0 = finLast("lev", T); if (s0 != null && T - s0 < 45 * 864e5 && finOutcome("lev", s0, T) === "held") return "dead"; /* v709 last season's hunt */ } catch (e) {} return "alive"; }
const crcKrkFresh = T => !!(S && S.crcKrk && T - S.crcKrk.at < 12 * 3600e3);
function crcBossSet(B, A, T) { /* what the boss fields right now: [unit, sections in this phase, escort, notes] */
  const st = crcStC(T), pct = crcSupPct(st); let u = B.u, n0 = A.hp, esc = {}, mods = { pA: 1, pS: 1, seg: 1, bK: 1 }, tac = [];
  if (B.mech === "pincer") { mods.pA = .84; tac.push("pincer"); esc = B.guard ? { ckrak: 2, cwar: 2 } : { cwar: 3, cscut: 4 }; }
  if (B.mech === "brood") { tac.push("brood"); esc = { cbrood: 2, cscut: 4 + Math.floor(A.hp / 10), ccarr: 1 }; }
  if (B.mech === "shell") { tac.push("shell"); mods.seg = B.guard ? .6 : pct >= .5 ? .85 : .7; esc = B.guard ? { cguard: 4, ctyr: 0 } : { cguard: 3, ccrys: 2 }; delete esc.ctyr; }
  if (B.mech === "pulse") { tac.push("pulse"); mods.pS = .6; esc = B.guard ? { ccrys: 4, cmint: 2 } : { cspit: 4, cint: 4, cmint: 2 }; }
  if (B.mech === "reson") { const dead = crcLevFate(T) === "dead"; esc = { [dead ? "clevd" : "slevi"]: 1, cregent: 2, cvang: 2 }; if (!crcKrkFresh(T)) { tac.push("reson"); mods.bK = dead ? 1.15 : 1.3; } }
  if (B.crown) { const ph = crcPh(A.hp); n0 = A.hp - (4 - ph) * 100; u = ph === 3 ? "ccrownm" : "ccrown";
    if (ph === 1) { tac.push("shell"); mods.seg = .5 + .5 * pct; esc = { cguard: 4, cempr: 1 }; }
    else if (ph === 2) { tac.push("brood"); esc = { cbrood: 3, cscut: 12, cbrlord: 1 }; }
    else if (ph === 3) { tac.push("molt"); mods.seg = 2; mods.bK = 1.5; esc = { cmolt: 2, cmint: 4 }; }
    else { tac.push("reson"); mods.bK = crcKrkFresh(T) ? 1.1 : 1.3; esc = { cempr: 2, cregent: 2, slevi: 1 }; } }
  return { u, n0, esc, mods, tac }; }
function crcBossForce(x, T) { T = T || now(); const B = CRC_BOSS[x.id], A = crcStC(T).b[B.id], s = crcBossSet(B, A, T); return Object.assign({ [s.u]: Math.max(1, s.n0) }, s.esc); }
async function crcBossResolve(f) { const B = CRC_BOSS[f.xid], x = PB[f.xid]; G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(q => q !== f); };
  try { const at = f.arrive; if (!crcBossOn(B, at)) { note(`${B.name} was gone when our fleet arrived. Returning.`, "warn"); return home(); }
    const ref = adb().doc(crcDoc()); await crcLock(ref); const snap = await casGet(ref), cur = crcNorm(snap.exists ? snap.data() : null, at), A = cur.b[B.id];
    if (A.dead) { note(`${B.name} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
    const ph0 = B.crown ? crcPh(A.hp) : 0, Z = crcBossSet(B, A, at), n0 = Math.max(1, Z.n0);
    const mkA = () => { const st = stacksOf(f.n, techVs(x), G.me); for (const s of st) { s.atk *= Z.mods.pA; s.sh *= Z.mods.pS; } return st; };
    const mkD = () => { const st = stacksOf(Object.assign({ [Z.u]: n0 }, Z.esc), { mon: B.lvl }, "monster"); if (Z.mods.bK !== 1) for (const s of st) { s.atk *= Z.mods.bK; s.hull *= Z.mods.bK; } return st; };
    const mine0 = Object.assign({}, f.n), { res, rise } = mimRise(mkA, mkD, Z.u, n0, n0);
    const left = clamp(Math.round(((res.dLeft || {})[Z.u]) || 0), 0, n0), raw = n0 - left, seg = raw ? Math.min(n0, Math.max(1, Math.round(raw * Z.mods.seg))) : 0;
    let pts = 0; if (seg) { A.hp -= seg; A.t = at; A.dmg[G.me] = (A.dmg[G.me] || 0) + seg; if (A.hp <= 0) { A.hp = 0; A.dead = at; A.last = G.me; } pts = 4 * seg; }
    const counted = pts ? crcCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; crcLocal(cur);
    const rep = mkRep({ at, kind: "attack", simLeft: left, title: `Assault on ${B.name}${B.crown ? ` · Phase ${ph0}, ${CRC_PHN[ph0]}` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: B.name, mon: B.mon, mimB: B.id, mimSeg: [n0, n0 - seg], omRise: rise > 1.01 ? Math.round(rise) : undefined,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1); if (rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info");
    if (seg) { const L = { m: 30000 * seg, c: 20000 * seg, g: 10000 * seg }, ratio = Math.min(1, fCargo(f) / Math.max(1, total(L))); rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = 2 * seg, M = crcS(), w = Math.max(1, Math.min(4, crcWeek(at))), W = crcWk(M, w); S.shards = (S.shards || 0) + sh; rep.shards = sh; S.wins++; evPts("hunt", seg * 50);
      const mt = { chitin: 2 * seg }; if (B.crown) { mt.crown = Math.ceil(seg / 3); W.crn += seg; } else if (B.guard) { mt.rcrystal = Math.ceil(seg / 2); W.grd += seg; } else { mt.eshell = Math.ceil(seg / 3); if (B.mech === "brood") mt.pearl = Math.ceil(seg / 2); W.boss += seg; }
      crcAddM(mt); M.pts += counted; logReward(`${B.name} bounty`, rep.loot, { shards: sh, kind: "battle" }); }
    const T = { pincer: `Pincer Lock: ${B.name} pinned our fleet (−16% firepower).`, pulse: `Tidal Pulse: our shields were stripped (−40%).`, shell: `Shell Armor: ${B.name}'s shell turned aside part of every blow.`, brood: `Brood Deployment: a fresh brood joined the fight.`, reson: `Monster Resonance: the war-song of the deep beasts made the enemy ${Math.round((Z.mods.bK - 1) * 100)}% tougher. Slay a wild Kraken to break it.`, molt: `Molting: the Crown's new shell is soft, every blow counts double, but it strikes 50% harder.` };
    for (const t of Z.tac) note(T[t], "info");
    if (rise > 1.01) note(`${B.name} rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (A.dead) { bump("bosses"); note(B.crown ? `THE ABYSSAL CROWN HAS FALLEN. Everyone who broke a section can claim the spoils.` : `We brought down ${B.name}! Everyone who broke a section can claim the spoils.`, "win"); }
    else if (seg) note(`Our fleet broke ${seg} section${seg > 1 ? "s" : ""} off ${B.name} (${A.hp} of ${B.hp} left${B.crown && crcPh(A.hp) !== ph0 ? `; the Crown enters Phase ${crcPh(A.hp)}, ${CRC_PHN[crcPh(A.hp)]}` : ""}). +${counted} Abyssal Suppression${counted < pts ? " (daily cap reached)" : ""}.`, "win");
    else note(`Our fleet couldn't break a section off ${B.name}. Send more firepower.`, "warn");
    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} crcClaim(); home();
  } catch (e) { if (e === CAS_RETRY && await casAgain(f, crcBossResolve)) return; note(`Lost contact with the ${B.name} fight. Fleet returning.`, "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* a fallen boss: everyone who broke a section claims once, by share; the final blow pays extra. The Crown's fall plays the finale. */
function crcClaim() { if (!S || !G.ready) return; const T = now(), w = crcWeek(T); if (w < 2) return; const st = crcStC(T), M = crcS(); M.got = M.got || {};
  for (const B of CRC_BOSSES) { const A = st.b[B.id], my = (A.dmg || {})[G.me] || 0, id = "b" + B.id; if (!A.dead || !my || M.got[id]) continue; M.got[id] = 1;
    const tot = Object.values(A.dmg).reduce((a, b) => a + b, 0) || 1, share = my / tot, last = A.last === G.me ? 2 : 0, sh = Math.min(B.crown ? 60 : 40, (B.crown ? 25 : 10) + Math.round(share * 60)), r = { sh };
    if (B.crown) { r.crown = Math.min(10, 3 + Math.round(share * 20)) + last; r.eshell = 4; S.medals = S.medals || {}; S.medals.crown = (S.medals.crown || 0) + 1; }
    else if (B.guard) r.rcrystal = Math.min(12, 4 + Math.round(share * 20)) + last; else { r.eshell = Math.min(12, (B.id === "ca4" ? 6 : 3) + Math.round(share * 20)) + last; r.pearl = B.mech === "brood" ? 4 : 1; }
    crcGrant(r, `${B.name} slain`); note(`${B.name} is dead. Your share (${Math.round(share * 100)}%): ${crcMatTxt(r)} and ◆${sh}${last ? ", with the final blow" : ""}.`, "win"); }
  const C = st.b.cc; if (C && C.dead && !M.fin) { M.fin = 1; dirty(); setTimeout(() => { try { crcCine("fin"); } catch (e) {} }, 1200); } }
/* the Great Molting's moments, in the Omega cinematic frame: its rise, each new phase, and the finale */
const CRC_CINE = { arr: ["s_crownship", "THE GREAT MOLTING", "“The Crown rises. Kneel, or be shed with the old shell.”", "The Abyssal Crown has surfaced at the heart of the galaxy. Four phases stand between it and its rebirth."],
  p2: ["s_hatchery", "PHASE II · THE BROOD WAKES", "“Every egg remembers. Every egg will hatch.”", "The Crown's shell has cracked, and its brood is pouring from the hatcheries on its back."],
  p3: ["crownbrood", "PHASE III · THE GREAT MOLTING", "“The old shell falls. The new one hardens.”", "The Crown is shedding its shell. Its new one is soft: strike now, before it hardens."],
  p4: ["s_throne", "PHASE IV · THE CROWN REBORN", "“I have been born a thousand times. You have been born once.”", "The Crown has molted. Its last shell is its hardest, and the deep beasts sing for it."],
  fin: ["s_throne", "THE TIDE HAS TURNED", "THE ABYSS REMEMBERS WHAT THE STARS HAVE FORGOTTEN.", "The Abyssal Crown is dead. Its shell drifts empty above the Breach. Far below the Abyss, something answers its last cry: the thing the whole Empire was fleeing."],
  esc: ["s_moon", "THE CROWN IS REBORN", "“Remember this tide. The next one is mine.”", "The Abyssal Crown completed its molt and sank back into the Abyss, reborn. The seal over the deep has cracked, and the Judge will remember. Next year the tide returns with a harder shell."] };
function crcCine(k) { if (document.getElementById("omcine")) return; const D = CRC_CINE[k]; if (!D) return; const w = document.createElement("div"); w.id = "omcine"; w.className = "fin crccine"; document.body.appendChild(w);
  w.innerHTML = `<div class="omcimg" style="background-image:url(art/carcinid/${D[0]}.webp)"></div><div class="omctx tx"><small>${esc(D[1])}</small><b class="q"></b><span class="after">${esc(D[3])}</span></div><small>Tap to close</small>`;
  const q = D[2], el = w.querySelector(".q"); let n = 0; const tick = () => { if (!document.body.contains(w)) return; el.textContent = q.slice(0, ++n); if (n < q.length) setTimeout(tick, 45); else w.classList.add("done"); };
  try { SFX.gong(); } catch (e) {} setTimeout(tick, 900); setTimeout(() => { try { if (document.body.contains(w)) sbSay(CRC_SAY["cine_" + k]); } catch (e) {} }, 2600); /* v705 */ w.addEventListener("click", () => { if (n < q.length) n = q.length - 1; else { w.classList.add("out"); setTimeout(() => w.remove(), 600); } }); }
function crcCineCheck() { if (!S || !G.ready || G.cineOn || battle || document.getElementById("omcine")) return; const T = now(), e = crcClock(T).e; if (e < CRC_CROWN0 || e >= CRC_LEN) return; const M = crcS(), C = crcStC(T).b.cc; M.cine = M.cine || {}; if (!C || C.dead) return;
  if (!M.cine.arr) { M.cine.arr = 1; dirty(); return crcCine("arr"); } const ph = crcPh(C.hp); for (const p of [2, 3, 4]) if (ph >= p && !M.cine["p" + p]) { M.cine["p" + p] = 1; dirty(); return crcCine("p" + p); } }
function crcBossInfo(x, T) { const B = CRC_BOSS[x.id], st = crcStC(T), A = st.b[B.id], Z = crcBossSet(B, A, T), tot = Object.values(A.dmg || {}).reduce((a, b) => a + b, 0), my = (A.dmg || {})[G.me] || 0, pct = Math.round(A.hp / B.hp * 100);
  return `<div class="crcbi"><img src="art/carcinid/${B.art}.webp" alt=""><div><b>${A.dead ? "Slain" : `${A.hp} of ${B.hp} sections`}${B.crown && !A.dead ? ` · Phase ${crcPh(A.hp)}, ${CRC_PHN[crcPh(A.hp)]}` : ""}</b><div class="mimbar crcbar"><i style="width:${pct}%"></i></div><small>${CRC_REGEN[B.id] ? `Regrows ${CRC_REGEN[B.id]} sections an hour.` : "Does not heal."} Your share: ${my} section${my === 1 ? "" : "s"}${tot ? ` (${Math.round(my / tot * 100)}%)` : ""}.</small></div></div>
    ${Z.tac.map(t => `<div class="crctac"><img src="art/carcinid/k_${CRC_TAC[t][1]}.webp" alt=""><div><b>${CRC_TAC[t][0]}</b><small>${CRC_TAC[t][2]}</small></div></div>`).join("")}
    <dl class="kv"><dt>Its fleet</dt><dd>${Object.entries(crcBossForce(x, T)).map(([k, v]) => `${v} ${AL[k] ? AL[k].n : k}`).join(" · ")}</dd><dt>Every section</dt><dd>◆2 · resources · ${B.crown ? "Crown Reactor Shards" : B.guard ? "Ancient Reef Crystal" : "Emperor Shell Fragments"} · +4 Suppression</dd><dt>When it falls</dt><dd>Everyone who broke a section claims a share${B.crown ? ", the Crown Slayer medal, and the finale" : ""}</dd></dl>`; }
const CRC_TAC = { shell: ["Shell Armor", "shell", "Carcinid shells turn aside part of every blow: the Reef Tyrant 30% (15% once Suppression passes 50%), the Trench Behemoth 40%, the Crown's first phase up to half until Suppression is full. Shell Guardians carry the heaviest plate of the line."],
  brood: ["Brood Deployment", "brood", "Broodmothers bring two more drones into every Reef Fortress; the Pearl Matron fields a fresh brood each fight, bigger the healthier she is; the Crown's second phase pours out its hatcheries."],
  pulse: ["Tidal Pulse", "pulse", "The Trench Oracle and the Pale Sovereign roll a wave of abyssal water over the field that strips 40% of our fleet's shields."],
  molt: ["Molting", "molt", "In its third phase the Abyssal Crown sheds its shell: every blow counts double, but it strikes 50% harder. Molting Titans hold Stage 4 nests."],
  reson: ["Monster Resonance", "reson", "Korvax rides the Leviathan (in chains if it escaped its hunt, its corpse if we slew it) and the reborn Crown sings with the deep beasts: their fleets are 15-30% tougher and deadlier, unless you slew a wild Kraken in the last 12 hours."],
  pincer: ["Pincer Lock", "pincer", "The Red Claw Marshal and the Krakenbreaker lock our ships in their claws: our fleet fights with a sixth less firepower."] };
/* ---------- the Abyssal Forge, the reward track, the cosmetics ---------- */
const CRC_FORGE = [
  ["px", "Abyssal Reef planet skin", "A world of black chitin plates and violet coral, lit by cyan tide-water.", { chitin: 150, coral: 40, pearl: 6 }],
  ["hull", "Carcinid Chitin hull finish", "Plate your ships in black-violet chitin with gilded seams. Looks only.", { coral: 60, eshell: 10, rcrystal: 6 }],
  ["frame12", "Tide Lord portrait frame", "A gilded ring of antlers and pearls.", { pearl: 10, rcrystal: 4 }],
  ["banner12", "Abyssal Fleet banner", "The Carcinid armada under the Crown.", { chitin: 100, resin: 30 }],
  ["trail12", "Tidal warp trail", "Your fleets leave a gold-and-cyan wake.", { resin: 40, enzyme: 10 }],
  ["laser12", "Abyssal laser colour", "Your guns fire tide-cyan and gold.", { coral: 40, enzyme: 12 }],
  ["aura12", "Crown of the Abyss aura", "A gold-and-cyan ring round your homeworld.", { crown: 4, eshell: 10 }],
  ["acc", "Tidal accelerator (silver)", "A silver time accelerator for your Void Shop inventory.", { chitin: 40 }],
  ["tcore", "Titan Core ⬢", "Forged from Emperor Shell and the Crown's own reactor.", { eshell: 8, crown: 3 }],
  ["sh", "Void Shards ◆25", "A Crown Reactor Shard sells high.", { crown: 1 }]];
const CRC_TRACK = [[100, { sh: 5 }, { chitin: 25 }], [300, { resin: 10 }, { sh: 10 }], [600, { item: "crateM" }, { banner12: 1 }], [1000, { sh: 10 }, { px: 1 }], [1600, { enzyme: 8 }, { frame12: 1 }], [2400, { sh: 15 }, { hull: 1 }], [3500, { eshell: 4 }, { sh: 30 }], [5000, { pearl: 4 }, { tcore: 1 }], [7000, { crown: 1 }, { aura12: 1 }]];
const crcHave = (c, M) => Object.entries(c).every(([k, n]) => (M.m[k] || 0) >= n);
const crcCostTxt = c => Object.entries(c).map(([k, n]) => `<span style="color:${CRC_MAT[k][1]}"><img class="crcmi s" src="art/carcinid/m_${k}.webp" alt="">${n}</span>`).join(" ");
const crcOwn = k => k === "px" ? !!(S.pxOwn || {}).abyssreef : k === "hull" ? !!(S.hullOwn || {}).carcinid : /12$/.test(k) ? !!((S.cos || {}).own || {})[k] : false;
function crcGrant(r, why) { const got = []; for (const k in CRC_MAT) if (r[k]) { crcAddM({ [k]: r[k] }); got.push(`${r[k]} ${CRC_MAT[k][0]}`); }
  if (r.sh) { S.shards = (S.shards || 0) + r.sh; got.push(`◆${r.sh}`); } if (r.item) { giveItem(r.item); got.push(SHOP[r.item] ? SHOP[r.item].n : r.item); }
  if (r.tcore) { S.tcore = (S.tcore || 0) + r.tcore; got.push("a Titan Core ⬢"); } if (r.px) { (S.pxOwn = S.pxOwn || {}).abyssreef = 1; got.push("the Abyssal Reef planet skin"); }
  if (r.hull) { (S.hullOwn = S.hullOwn || {}).carcinid = 1; got.push("the Carcinid Chitin hull finish"); } if (r.acc) { giveItem("xb_silver"); got.push("a silver time accelerator"); }
  for (const c of ["frame12", "banner12", "trail12", "laser12", "aura12"]) if (r[c]) { try { cosGive(c); } catch (e) {} got.push(cosDef(c) ? cosDef(c).n : c); }
  dirty(); if (got.length) { toast(`${why}: ${got.join(", ")}`, "win"); try { logReward(why, null, { shards: r.sh || 0, kind: "event" }); } catch (e) {} } return got; }
function crcForgeHTML() { const M = crcS(); return `<h3>The Abyssal Forge</h3><div class="mimforge">${CRC_FORGE.map(([k, n, d, c]) => { const done = crcOwn(k), ok = !done && crcHave(c, M);
    return `<div class="mimfr crcfr${done ? " done" : ""}"><div><b>${esc(n)}</b><small>${esc(d)}</small><em>${crcCostTxt(c)}</em></div><button class="btn${ok ? " pri" : ""}" data-act="crcForge" data-k="${k}"${ok ? "" : " disabled"}>${done ? "Owned" : "Forge"}</button></div>`; }).join("")}</div>`; }
function crcTrackHTML() { const M = crcS(), pr = mimPrem(), got = M.tr || {};
  const nm = (k, v) => k === "px" ? "Abyssal Reef skin" : k === "hull" ? "Chitin finish" : k === "item" ? (SHOP[v] ? SHOP[v].n : v) : k === "sh" ? `◆${v}` : k === "tcore" ? "Titan Core ⬢" : /12$/.test(k) ? (cosDef(k) || {}).n || k : `${v} ${CRC_MAT[k][0]}`;
  const cell = (r, i, p) => { const id = (p ? "p" : "f") + i, have = got[id], open = M.pts >= CRC_TRACK[i][0] && (!p || pr); return `<button class="mimtc${p ? " p" : ""}${have ? " got" : open ? " ready" : ""}" data-act="crcTrack" data-i="${i}" data-p="${p ? 1 : 0}"${open && !have ? "" : " disabled"}>${have ? "✓ " : ""}${esc(Object.entries(r).map(([k, v]) => nm(k, v)).join(", "))}</button>`; };
  return `<h3>Carcinid reward track</h3><p class="note">${fmt(M.pts)} tide points. Premium rewards need Void Pass Premium${pr ? " (yours is active)" : ""}.</p><div class="mimtrack">${CRC_TRACK.map(([pts, f, p], i) => `<div class="mimtr${M.pts >= pts ? " on" : ""}"><b>${fmt(pts)}</b>${cell(f, i, 0)}${cell(p, i, 1)}</div>`).join("")}</div>`; }
/* ---------- finding things and the hub ---------- */
function crcNearest(T, mon) { const h = originPlanet() || myPlanets()[0]; if (!h) return null; const hp = pos(h, T); let best = null, bd = 1e9;
  for (const x of mon === "crcpat" ? CRC_PATS : mon === "wkraken" ? CRC_KRAK : CRC_NESTS) { if (!crcLive(x, T) || pirDown(x) > T) continue; const q = pos(x, T), d = Math.hypot(q.x - hp.x, q.y - hp.y) * (fogSeen(q.x, q.y) ? 1 : 3); if (d < bd) { bd = d; best = x; } } return best; }
function crcBand(T) { try { if (!G.crcCC || Date.now() - G.crcCC > 4000) { G.crcCC = Date.now(); setTimeout(() => { try { crcCineCheck(); } catch (e) {} }, 500); } } catch (e) {}
  const w = crcWeek(T), c = crcClock(T); if (w === 5) return "";
  if (w === 0) { if (-c.e > 3 * 864e5) return ""; return `<button class="omb fin crcb soon" data-act="crcOpen"><b>❖ TIDE OF THE CARCINID</b><span>in ${ftime(-c.e)}</span></button>`; }
  { const M = crcS(); if (!M.intro && G.ready) { M.intro = 1; dirty(); setTimeout(() => { try { note("Tide of the Carcinid: Abyssal Breach Zones are opening across the galaxy. Open the event from the band at the top of the map.", "warn"); } catch (e) {} }, 1500); } }
  const live = c.e >= CRC_CROWN0 && !(crcStC(T).b.cc || {}).dead;
  return `<button class="omb fin crcb" data-act="crcOpen"><b>❖ ${live ? "THE GREAT MOLTING" : "TIDE OF THE CARCINID"}</b><span>${live ? `LIVE · Phase ${crcPh(crcStC(T).b.cc.hp)}` : `Week ${w} · ${CRC_WEEKS[w - 1][0]}`}</span></button>`; }
function crcInfo(x, T) { const L = crcLoot(x, crcStage(x, T)), sal = crcMatTxt(L).replace(/, /g, " · ") + (crcWeek(T) >= 1 && crcWeek(T) <= 4 ? ` · +${L.pts} tide points` : "");
  return (x.mon === "wkraken" ? `A wild creature</dd><dt>Breaks</dt><dd>Korvax's Monster Resonance against you, for 12 hours` : x.mon === "crcpat" ? `War patrol</dd><dt>The patrol</dt><dd>${crcForceTxt(x)}` : `Stage ${crcStage(x, T)} · ${CRC_STAGE[crcStage(x, T)]}</dd><dt>The garrison</dt><dd>${crcForceTxt(x)}`) + `</dd><dt>${x.mon === "wkraken" ? "Salvage" : "Tide salvage"}</dt><dd>${sal}`; }
/* the owner's paintings */
const CRC_ART = { cscut: "drone", cspit: "spitter", charv: "harvester", cguard: "guardian", cbrood: "broodmother", cwar: "warrior", ccrys: "crystal", clanc: "spitter_b", cmolt: "crownbrood", cfrig: "frigate", cint: "interceptor", cdest: "s_lance", cvang: "s_war", ccarr: "s_brood", cpearl: "s_eye", cmint: "s_crown", cregent: "s_citadel", cempr: "s_shell", cbrlord: "s_brood2",
  carcinid: "s_reef", crcpat: "frigate", crcmar: "marshal", crcmat: "matron", crctyr: "tyrant", crcora: "oracle", crckor: "korvax", crcbeh: "behemoth", crckbr: "krakenbreaker", crcpal: "pale", crccrown: "s_crownship" };
const CRC_CD = { cscut: ["The Empire's foot soldier. Small, fast, and never alone.", "Stage 1"], cspit: ["A living coral battery that lobs searing spore-shot from its back.", "Stage 1"], charv: ["Strips wrecks and asteroids for the brood, its resin sacs glowing.", "Stage 1"], cguard: ["A walking bulwark. Its shell turns aside what our guns throw at it.", "Stage 2"],
  cbrood: ["Carries the next brood on its back; two more drones hatch into every fight.", "Stage 3"], cwar: ["Built around its pincers. It closes on a ship and does not let go.", "Stage 3"], ccrys: ["Grows Ancient Reef Crystal through its shell and fires it as light.", "Stage 3"], clanc: ["A long trench-hunter with lance-claws and a whip of a tail.", "Stage 4"], cmolt: ["A crab mid-molt, its soft new shell glowing through the old. Enormous.", "Stage 4"],
  ckrak: ["The Kraken, back from the Abyss. Wild now, and in the deep layers for good.", "Wild"],
  cfrig: ["A beetle-hulled warship with two great claws hooked under its brow.", "Patrols · Stage 2"], cint: ["A slim hunter with two pincer arms thrust forward.", "Patrols"], cdest: ["A trident prow and a spine of living coral.", "Patrols · Stage 3"], cvang: ["An arrowhead with two great claw-wings swept back.", "Stage 4 · Admirals"],
  ccarr: ["Rows of glowing eggs down both flanks; every one a ship.", "Week 4 patrols"], cpearl: ["A pale needle with two pincer prongs.", "Week 2 patrols"], cmint: ["Two hulls split like a shed shell.", "Week 3 patrols"], cregent: ["A flagship with crescents fore and aft and a great cyan eye.", "Korvax, the Crown"], cempr: ["The Crown's golden flagship.", "The Crown"], cbrlord: ["A brood sac on a carrier's back.", "The Crown"] };
function crcBossRow(B, T, st) { const A = st.b[B.id], on = crcBossOn(B, T), pct = Math.round(A.hp / B.hp * 100), soon = !on && crcClock(T).e < CRC_LEN;
  return `<div class="crcboss${A.dead ? " dead" : on ? "" : " off"}"><img src="art/carcinid/${B.art}.webp" alt="" loading="lazy"><div><b>${esc(B.name)}</b><small>${A.dead ? "Slain" : on ? `${A.hp}/${B.hp}${B.crown ? ` · Phase ${crcPh(A.hp)}, ${CRC_PHN[crcPh(A.hp)]}` : ""}` : soon ? (B.crown ? "Surfaces on day 23" : `Arrives in week ${B.wk}`) : "Gone"}</small><div class="mimbar crcbar"><i style="width:${A.dead ? 0 : pct}%"></i></div></div>${on && !A.dead ? `<button class="btn${B.crown ? " pri" : ""}" data-act="crcGoB" data-id="${B.id}">Go</button>` : ""}</div>`; }
function shCarcinid() { const T = now(), M = crcS(), w = crcWeek(T), c = crcClock(T), own = ownerFree() && G.mode !== "offline" || G.owner, on = w >= 1 && w <= 4;
  const live = CRC_NESTS.filter(x => crcLive(x, T)), up = live.filter(x => pirDown(x) <= T), byS = [0, 0, 0, 0, 0]; up.forEach(x => byS[crcStage(x, T)]++); const pats = CRC_PATS.filter(x => crcLive(x, T) && pirDown(x) <= T).length, krk = CRC_KRAK.filter(x => crcLive(x, T) && pirDown(x) <= T).length;
  const when = w === 0 ? `Begins in ${ftime(-c.e)}` : w === 5 ? "The tide has turned" : w === 4 ? `Ends in ${ftime(CRC_LEN - c.e)}` : `Week ${w + 1} in ${ftime(w * CRC_WK - c.e)}`;
  const weeks = CRC_WEEKS.map(([t], i) => `<div class="mimwk crcwk${i + 1 === w ? " on" : i + 1 < w ? " past" : ""}"><b>Week ${i + 1}</b><span>${t}</span></div>`).join("");
  const st = crcStC(T), pct = crcSupPct(st), my = (st.con[G.me] || 0) + (M.pend || 0), n = Object.keys(st.con).length, C = st.b.cc;
  const sup = `<h3>Abyssal Suppression</h3><div class="mimsup"><div class="mimbar big crcbar"><i style="width:${Math.round(pct * 100)}%"></i></div><b>${Math.round(pct * 100)}%</b></div>
    <p class="note" style="margin-top:4px">Everything any commander destroys pushes the Abyss back. ${n} commander${n === 1 ? "" : "s"} so far · your share ${fmt(my)} point${my === 1 ? "" : "s"}${M.pend ? " (sending)" : ""}. At 50% the Reef Tyrant's shell weakens; at 100% every garrison is a quarter weaker and the Crown's first shell is broken.</p>
    <div class="crcms">${CRC_SUPM.map(([p, sh, rs]) => { const got = M.got["s" + p], ok = pct * 100 >= p && my > 0; return `<div class="crcm${got ? " got" : ok ? " ok" : ""}"><b>${p}%</b><small>◆${sh} · ${rs} Resin</small>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${ok ? " pri" : ""}" data-act="crcSup" data-p="${p}"${ok ? "" : " disabled"}>Claim</button>`}</div>`; }).join("")}</div>`;
  const obj = on ? `<h3>Exploration orders · week ${w}</h3>` + crcObjs(w).map(([id, t, need, sh, mt]) => { const k = Math.min(need, crcObjN(w, id)), done = k >= need, got = M.got[`w${w}${id}`];
    return `<div class="mimobj crcobj"><div><b>${t}</b><div class="bar"><i style="width:${k / need * 100}%"></i></div><small>${k}/${need} · reward ◆${sh} and ${crcMatTxt(mt)}</small></div>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${done ? " pri" : ""}" data-act="crcClaim" data-w="${w}" data-id="${id}"${done ? "" : " disabled"}>Claim</button>`}</div>`; }).join("") : "";
  const molt = C && c.e >= CRC_CROWN0 && on ? `<div class="crcmolt${C.dead ? " won" : ""}"><img src="art/carcinid/${C.dead ? "s_throne" : "s_crownship"}.webp" alt=""><div><b>${C.dead ? "The Abyssal Crown is dead" : `THE GREAT MOLTING · Phase ${crcPh(C.hp)}`}</b><span>${C.dead ? "The Abyss remembers what the stars have forgotten." : `${CRC_PHN[crcPh(C.hp)]} · ${C.hp}/400 sections`}</span><div class="crcph">${[1, 2, 3, 4].map(p => `<i class="${C.dead || crcPh(C.hp) > p ? "done" : crcPh(C.hp) === p ? "on" : ""}">${p}</i>`).join("")}</div>${C.dead ? `<button class="btn" data-act="crcCine" data-k="fin">Replay the finale</button>` : `<button class="btn pri" data-act="crcGoB" data-id="cc">Join the fight</button>`}</div></div>` : "";
  const cmd = w >= 2 && on ? `<h3>The Abyssal Command</h3><div class="crcbosses">${CRC_BOSSES.filter(B => !B.crown && (B.wk <= w || own)).map(B => crcBossRow(B, T, st)).join("")}</div>` : "";
  const mats = Object.entries(CRC_MAT).map(([k, [nm, col]]) => `<div class="mimmat"><img class="crcmi" src="art/carcinid/m_${k}.webp" alt=""><b>${fmt(M.m[k] || 0)}</b><small>${nm}</small></div>`).join("");
  const tac = `<details class="crclore"><summary>Abyssal tactics</summary>${Object.values(CRC_TAC).map(([nm, ic, d]) => `<div class="crctac"><img src="art/carcinid/k_${ic}.webp" alt=""><div><b>${nm}</b><small>${d}</small></div></div>`).join("")}</details>`;
  const cls = ["cscut", "cspit", "charv", "cguard", "cbrood", "cwar", "ccrys", "clanc", "cmolt", "ckrak", "cfrig", "cint", "cpearl", "cdest", "cmint", "cvang", "ccarr", "cregent", "cempr", "cbrlord"];
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${CRC_COL}">Seasonal invasion</div><h2>❖ Tide of the Carcinid</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="mimban crcban"><img src="art/carcinid/banner.webp" alt=""><div><b>${on ? `Week ${w} · ${CRC_WEEKS[w - 1][0]}` : w === 0 ? "The deep is stirring" : "The tide has turned"}</b><span>${when}${c.prev ? " · owner preview" : ""}</span></div></div>
  <details class="crclore"${on && !M.loreSeen ? " open" : ""}><summary>The Abyss wakes</summary><p>Beyond the Architects' outer wall lies the Abyss, a sea older than the stars that runs all the way down to the prison's floor. It belonged to the Carcinid Abyssal Empire: armoured legions who bred the great beasts of the deep as war mounts, the Kraken and the Leviathan among them.</p><p>When the Architects built their prison, they took the Empire's greatest beast, made it the Warden of their wall, and sealed the Abyss behind it. Last season the Leviathan turned inward, answering its old masters, and broke through the wall. The breach it left has never closed.</p><p>The Carcinid are not here to conquer. Something beneath the Abyss is stirring, and the whole Empire is rising to flee it through the cracks in the wall: its scouts first, then the Claw Admirals, then the guardians of the deep, and last of all the Abyssal Crown, rising to be reborn on our side of the wall.</p><p>The Kraken came up with them: the light we saw rising from the deep in the omens. It answers to no one now.</p></details>
  <p class="note">${on ? CRC_WEEKS[w - 1][1] : w === 0 ? "Deep-scan buoys in the outer layers are picking up pressure waves where there is no water. Something is pressing against the dark from the other side." : "The Breaches have sealed. The Abyss remembers."}</p>
  ${on ? `<p class="note crcfate">${crcLevFate(T) === "dead" ? (w >= 4 ? "The Leviathan was slain at the wall. The Carcinid dragged its corpse into the Breach, and Korvax rides it." : "The Leviathan was slain at the wall. The Carcinid are dragging its corpse into the Breach: Korvax means to ride it in week 4.") : w >= 4 ? "The Leviathan escaped its hunt at the wall. Korvax has it in chains." : "The Leviathan escaped its hunt at the wall and fled into the Breach. Korvax is putting it in chains for week 4."}</p>` : ""}${CRC_BOSS.cc.hp > 400 && on ? `<p class="note crcfate">Last tide the Crown escaped. It has returned with a harder shell, and so has Korvax.</p>` : ""}
  <div class="mimwks">${weeks}</div>${molt}
  ${on ? `<div class="mimst crcst">${[1, 2, 3, 4].map(s => `<div class="s${s}${s > Math.min(CRC_CAP, w >= 4 ? 4 : w + 1) ? " off" : ""}"><b>${byS[s]}</b><small>Stage ${s}<br>${CRC_STAGE[s]}</small></div>`).join("")}</div>
  <div class="crcfind"><button class="btn pri" data-act="crcFind" data-m="carcinid"${up.length ? "" : " disabled"}>Nearest Breach Zone</button><button class="btn" data-act="crcFind" data-m="crcpat"${pats ? "" : " disabled"}>Nearest patrol (${pats})</button><button class="btn" data-act="crcFind" data-m="wkraken"${krk ? "" : " disabled"}>Nearest Kraken (${krk})</button></div>` : ""}
  ${cmd}${obj}${on || w === 5 ? sup : ""}${tac}
  <h3>Season materials</h3><div class="mimmats">${mats}</div><p class="note" style="margin-top:6px">Tide points: <b>${fmt(M.pts)}</b>. ${Object.entries(CRC_MSRC).map(([k, s]) => `${CRC_MAT[k][0]} from ${s}`).join("; ")}.</p>
  ${S.medals && S.medals.crown ? `<div class="mimmedal"><span>🏆 Crown Slayer ×${S.medals.crown}</span></div>` : ""}${crcForgeHTML()}${crcTrackHTML()}
  <h3>The Abyssal Empire</h3><div class="mimcls">${cls.map(k => `<div class="mimcl crccl">${CRC_ART[k] ? `<img src="art/carcinid/${CRC_ART[k]}.webp" alt="" loading="lazy">` : `<canvas data-ship="${k}" width="224" height="112"></canvas>`}<div><b>${AL[k].n}</b><small>${CRC_CD[k][0]}</small><em>${CRC_CD[k][1]}</em></div></div>`).join("")}</div>
  ${own ? `<div class="mimown"><small>Owner preview: see the tide as it will look in a given week (this device only). W5 opens the Great Molting.</small><div>${[0, 1, 2, 3, 4, 5].map(k => `<button class="btn${((S.crcPrev || {}).w || 0) === k ? " pri" : ""}" data-act="crcPrev" data-w="${k}">${k ? (k === 5 ? "Molting" : "Week " + k) : "Off"}</button>`).join("")}</div></div>` : ""}`; }
/* the Battle Lab */
const CRC_LAB = [["crc1", "Breach Zone · Stage 1", () => ({ cnest: 1, cscut: 7, charv: 1, cspit: 1 })], ["crc2", "Breach Zone · Stage 2", () => ({ cnest: 1, cscut: 8, charv: 1, cspit: 3, cguard: 2, cfrig: 1 })],
  ["crc3", "Breach Zone · Stage 3", () => ({ cnest: 1, cscut: 11, charv: 1, cspit: 3, cguard: 2, cfrig: 1, cbrood: 1, cwar: 2, ccrys: 1, cdest: 1 })], ["crc4", "Breach Zone · Stage 4", () => ({ cnest: 1, cscut: 11, cspit: 3, cguard: 3, cbrood: 1, cwar: 2, ccrys: 1, cmolt: 1, clanc: 2, cvang: 1 })],
  ["crcp", "Carcinid patrol (week 4)", () => ({ cfrig: 2, cint: 5, cpearl: 2, cdest: 1, cmint: 2, cvang: 1, ccarr: 1 })], ["crck", "The wild Kraken", () => ({ ckrak: 2 })],
  ...CRC_BOSSES.map(B => ["b" + B.id, B.name, () => { const A = { hp: B.hp }, Z = crcBossSet(B, A, now()); return Object.assign({ [Z.u]: 20 }, Z.esc); }]),
  ["bcc3", "The Abyssal Crown · Phase 3, molting", () => ({ ccrownm: 20, cmolt: 2, cmint: 4 })]];
function crcLabFight(k) { const L = CRC_LAB.find(x => x[0] === k); if (!L) return; const D0 = L[2](), big = /^b/.test(k), A0 = big ? MIM_LAB_FLEET : { battleship: 20, destroyer: 20, fighter: 60, corvette: 20 }, lvl = 20;
  const res = simulate(stacksOf(A0, techOf(null), G.me), stacksOf(D0, { mon: lvl }, "monster")), B = big ? CRC_BOSS[k.slice(1)] || CRC_BOSS.cc : null;
  const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Battle Lab · ${L[1]}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: L[1], mon: B ? B.mon : k === "crcp" ? "crcpat" : k === "crck" ? "wkraken" : "carcinid", lvl, ptype: "terran", fortL: 0, alien: true, pirate: true,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
  closeSheet(); playBattle(rep); }
function crcLabHTML(row0, b) { const p = S.crcPrev || {}, row = (ic, n, sub, btns) => `<div class="strow" style="flex-wrap:wrap"><div style="flex:1 1 100%;min-width:0"><b>${ic} ${esc(n)}</b>${sub ? `<div class="note">${sub}</div>` : ""}</div><div style="display:flex;flex-wrap:wrap;gap:6px">${btns}</div></div>`;
  return row("❖", "The tide, week by week", `Breach Zones, patrols, the admirals and the hub as they will be · ${p.w ? (p.w === 5 ? "previewing the Great Molting" : `previewing week ${p.w}`) : "off"}`, [1, 2, 3, 4].map(w => b("crcLabWeek", String(w), "W" + w)).join("") + b("crcLabWeek", "5", "Molting") + b("crcLabWeek", "0", "Off") + b("crcOpen", "", "Hub"))
    + row("❖", "The Great Molting · cinematics", "The rise, each phase, the finale, and the Crown's escape", ["arr", "p2", "p3", "p4", "fin", "esc"].map(k => b("crcCine", k, k === "fin" ? "Finale" : k === "esc" ? "Escape" : k === "arr" ? "Rise" : "Phase " + k[1])).join(""))
    + row("❖", "The Leviathan's fate (preview)", `What Korvax rides in week 4 · ${p.lev === "dead" ? "its corpse" : "the beast in chains"}`, b("crcLabLev", "dead", "Slain") + b("crcLabLev", "alive", "Escaped"))
    + CRC_LAB.map(([k, n]) => row0("❖", n, /^b/.test(k) ? "A demo fleet of 1,400 warships" : "A small fleet against it", b("crcLabFight", k, "⚔ Watch"))).join(""); }
