/* ---------- v703 TIDE OF THE CARCINID, phase 1: First Tides (the owner's master prompt, built in phases) ----------
   Below the Kraken Deep lies the Abyss, a sea older than the stars. The Carcinid Abyssal Empire ruled it before the Architects built
   their prison: armoured crustacean legions who bred the great ocean beasts (the Leviathan, the Kraken, the serpents of the deep) as war
   mounts. Every time a Warden fell, the seal over the Abyss thinned. Now Abyssal Breach Zones are tearing open across the galaxy.
   The run: every Season of the Leviathan (the first season of the ten-season year), from the first one after the prologue (season 3,
   4 January 2027). 120 Breach Zones on their own spiral; each grows through four infestation stages, capped by the week, and its
   garrison grows with it; a nest you destroy reforms at Stage 1 after 12 hours. Carcinid scout patrols (Scuttle Frigates and Tidal
   Interceptors) roam between them. Phase 1 ships week 1 (First Tides): the first 40 Breach Zones, Stages 1 and 2, the patrols, the
   first four Carcinid monsters and two ships (3D models built in code), three materials (Abyssal Chitin, Coral Alloy, Tidal Resin),
   weekly exploration orders, and the server-wide Abyssal Suppression Meter (shared record event/carcinid {k, sup, con, cday}; owner
   previews use event/carcinid_prev). CRC_WAVES and CRC_CAP open the later weeks as their phases are built. */
const CRC_U = { cscut: 1, cspit: 1, charv: 1, cguard: 1, cfrig: 1, cint: 1, cnest: 1 };
Object.assign(AL, {
  cscut:  { n: "Scuttle Drone", atk: 380, sh: 320, hull: 5600, val: 16000, one: 1 },
  cspit:  { n: "Coral Spitter", atk: 760, sh: 240, hull: 5200, val: 22000, one: 1 },
  charv:  { n: "Tide Harvester", atk: 160, sh: 900, hull: 9800, val: 20000, one: 1 },
  cguard: { n: "Shell Guardian", atk: 420, sh: 3000, hull: 28000, val: 52000, one: 1 },
  cfrig:  { n: "Scuttle Frigate", atk: 600, sh: 800, hull: 12000, val: 36000, one: 1 },
  cint:   { n: "Tidal Interceptor", atk: 820, sh: 260, hull: 5800, val: 24000, one: 1 },
  cnest:  { n: "Abyssal Breach Nest", atk: 650, sh: 2600, hull: 50000, val: 90000, one: 1 } });
const CRC_COL = "#e8b45a", CRC_GLOW = "#3fe0c8";
Object.assign(MON, {
  carcinid: { n: "Abyssal Breach Zone", sp: "Breach Zone", ic: "❖", col: CRC_COL, rgb: "232,180,90", per: 99, d: "A tear into the Abyss. Coral and black chitin have grown round the wound, and the Carcinid pour through it: drones, spitters and the shelled guardians of the brood. It grows through four infestation stages, and every stage brings a heavier garrison. Close it before it matures.", names: ["Breach"] },
  crcpat: { n: "Carcinid Scout Patrol", sp: "Scout Patrol", ic: "❖", col: "#5fe0e8", rgb: "95,224,232", per: 99, d: "Scuttle Frigates and Tidal Interceptors charting our worlds for the Abyssal Empire. Sink them before they report home.", names: ["Patrol"] } });
const CRC_M = { carcinid: "cnest", crcpat: "cpat" };
const CRC_N = 120, CRC_P = 16, CRC_WK = 7 * 864e5, CRC_LEN = 28 * 864e5, CRC_REGROW = 12 * 3600e3;
const CRC_WAVES = 1, CRC_CAP = 2; /* phase 1: only week 1's 40 Breach Zones, and Stages 1 and 2 */
const CRC_STAGE = ["", "Breach", "Spawning Tide", "Reef Fortress", "Abyssal Dominion"];
const CRC_WEEKS = [["First Tides", "Breach Zones are tearing open in the outer dark. Scuttle Drones and Coral Spitters pour through, and Carcinid scout frigates are charting our worlds."], ["The Claw Admirals", "The scouts have reported home. The Claw Admirals are taking the field, and the nests are hardening into reef fortresses."], ["The Deep Guardians", "The Empire wakes its guardians. The oldest things in the Abyss are rising toward the light."], ["The Great Molting", "The Abyssal Crown is shedding its shell. When it molts, the Empire is reborn. Break the tide before it does."]];
const CRC_NESTS = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6;
  for (let j = 0; j < CRC_N; j++) { const u = (j + .7) / CRC_N, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (2.1 + j * GOLD) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 2 + (j * 5) % 4;
    out.push({ id: "cn" + j, kind: "pirate", mon: "carcinid", cj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Breach Zone ${String.fromCharCode(65 + (j * 11) % 26)}${String.fromCharCode(65 + (j * 5 + 7) % 26)}-${100 + j}` }); }
  return out; })();
const CRC_PATS = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 10, hi = LAYERS[0].r1 - 10;
  for (let j = 0; j < CRC_P; j++) { const u = (j + .5) / CRC_P, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (.6 + j * 2.399963 * 1.7) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 3 + (j * 3) % 3;
    out.push({ id: "cp" + j, kind: "pirate", mon: "crcpat", pj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Carcinid Scout Patrol ${["Kesh", "Vorr", "Thal", "Mokk", "Szal", "Ruun", "Qarr", "Ilth"][j % 8]}-${j + 1}` }); }
  return out; })();
const CRC_RUN = k => k >= PRO && seaCyc(k) === 0;
function crcT0(T = now()) { const c = vpSeason(T); for (let k = Math.max(0, c - 1); k <= c + 12; k++) if (CRC_RUN(k) && VP_BASE + k * VP_LEN + CRC_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + (PRO + 10) * VP_LEN; }
function crcClock(T) { const p = S && S.crcPrev; if (p && p.w && ownerFree()) return { e: (p.w - 1) * CRC_WK + 3 * 864e5 + Math.max(0, T - p.at), prev: 1 }; return { e: T - crcT0(T), prev: 0 }; } /* a preview opens three days into the week, when Stage 2 is out */
const crcWeek = T => { const e = crcClock(T).e; return e < 0 ? 0 : e >= CRC_LEN ? 5 : 1 + Math.floor(e / CRC_WK); };
const crcEm = x => x.mon === "crcpat" ? x.pj * 3 * 3600e3 : Math.floor(x.cj / 40) * CRC_WK + (x.cj % 40) * 1.1 * 3600e3;
function crcLive(x, T) { const e = crcClock(T).e; if (x.mon === "carcinid" && x.cj >= 40 * CRC_WAVES) return false; return e >= crcEm(x) && e < CRC_LEN; }
const crcHid = (x, T) => !crcLive(x, T);
function crcStage(x, T) { if (x.mon !== "carcinid") return 1; const c = crcClock(T), down = ((S && S.pir) || {})[x.id] || 0, born = Math.max(crcEm(x), down ? down - T + c.e : -1e15), wk = Math.max(1, Math.min(4, 1 + Math.floor(c.e / CRC_WK)));
  return Math.max(1, Math.min(1 + Math.floor(Math.max(0, c.e - born) / (3 * 864e5)), wk >= 4 ? 4 : Math.min(3, wk + 1), CRC_CAP)); }
function crcForce(x, T) { T = T || now(); const n = 1 + Math.floor(x.lvl / 4), sup = crcSupPct(crcStC(T)) >= 1;
  let o; if (x.mon === "crcpat") o = { cfrig: 1 + Math.floor(n / 3), cint: 2 + (n >> 1) };
  else { const st = crcStage(x, T); o = { cnest: 1, cscut: 2 + n, charv: 1, cspit: 1 }; if (st >= 2) { o.cscut += 1; o.cspit = 1 + (n >> 1); o.cguard = 1 + Math.floor(n / 4); o.cfrig = 1; } }
  if (sup) for (const k in o) if (k !== "cnest") o[k] = Math.max(1, Math.ceil(o[k] * .75)); /* a full Suppression Meter thins every garrison by a quarter */
  return o; }
const crcForceTxt = x => Object.entries(crcForce(x)).filter(([k]) => k !== "cnest").map(([k, v]) => `${v} ${AL[k].n}`).join(" · ");
/* the season's materials: Abyssal Chitin from every nest, Coral Alloy from Stage 2 on, Tidal Resin from the scout patrols.
   The other five (Pearl Core, Emperor Shell Fragment, Brood Enzyme, Ancient Reef Crystal, Crown Reactor Shard) come with later weeks. */
const CRC_MAT = { chitin: ["Abyssal Chitin", "⬣", "#e8b45a"], coral: ["Coral Alloy", "✲", "#ff7ab0"], resin: ["Tidal Resin", "◉", "#3fe0c8"] };
const crcKey = () => (S && S.crcPrev && S.crcPrev.w ? "p" : "") + String(crcT0()); /* an owner preview keeps its own tally */
function crcS() { const k = crcKey(); if (!S.crc || S.crc.k !== k) S.crc = { k, m: {}, pts: 0, kills: [0, 0, 0, 0, 0], wk: {}, got: {} }; return S.crc; }
function crcLoot(x, st) { return x.mon === "crcpat" ? { chitin: 1 + Math.floor(x.lvl / 10), coral: 0, resin: 2 + Math.floor(x.lvl / 6), pts: 15 + (x.lvl >> 1) } : { chitin: 2 + st * 2 + Math.floor(x.lvl / 5), coral: st >= 2 ? st : 0, resin: 0, pts: 25 * st + x.lvl }; }
const crcWk = (M, w) => { M.wk = M.wk || {}; return M.wk[w] || (M.wk[w] = { nest: 0, pat: 0, coral: 0, sv: {} }); };
function crcWin(x, rep, T) { const st = crcStage(x, T), M = crcS(), L = crcLoot(x, st), w = Math.max(1, Math.min(4, crcWeek(T))), W = crcWk(M, w);
  for (const k of ["chitin", "coral", "resin"]) if (L[k]) M.m[k] = (M.m[k] || 0) + L[k];
  M.pts += L.pts; if (x.mon === "crcpat") { W.pat++; M.pat = (M.pat || 0) + 1; } else { W.nest++; M.kills[st] = (M.kills[st] || 0) + 1; } W.coral += L.coral; try { crcQueue(L.pts); } catch (e) {}
  rep.crc = { st, chitin: L.chitin, coral: L.coral, resin: L.resin, pts: L.pts }; dirty();
  const got = [L.chitin ? `${L.chitin} Abyssal Chitin` : "", L.coral ? `${L.coral} Coral Alloy` : "", L.resin ? `${L.resin} Tidal Resin` : ""].filter(Boolean).join(", ");
  note(x.mon === "crcpat" ? `${x.name} sunk. Salvaged ${got} · +${L.pts} tide points.` : `${x.name} closed at Stage ${st} (${CRC_STAGE[st]}). Salvaged ${got} · +${L.pts} tide points.`, "win"); }
/* the week's exploration orders: [id, text, need, shards, {material: n}] (the same orders every week, counted week by week) */
const CRC_OBJ = [["sv", "Chart 3 Breach Zones (open one you have explored on the map)", 3, 5, { resin: 4 }], ["nest", "Close 3 Breach Zones", 3, 10, { chitin: 15 }], ["pat", "Sink 2 Carcinid scout patrols", 2, 8, { resin: 6 }], ["coral", "Salvage 10 Coral Alloy", 10, 10, { chitin: 10 }]];
function crcObjN(w, id) { const W = crcWk(crcS(), w); return id === "sv" ? Object.keys(W.sv).length : W[id] || 0; }
function crcSurvey(x) { const T = now(), w = crcWeek(T); if (w < 1 || w > 4 || !crcLive(x, T) || x.mon !== "carcinid") return; const W = crcWk(crcS(), w); if (!W.sv[x.id]) { W.sv[x.id] = 1; dirty(); } }
/* the Abyssal Suppression Meter: every nest, patrol and order adds points (300 a commander a day at most) against a target that grows
   with the number of commanders taking part. 25, 50, 75 and 100% pay everyone who helped; at 100% every garrison is thinned by a quarter. */
const CRC_DAYCAP = 300, CRC_SUPM = [[25, 5, 4], [50, 8, 6], [75, 12, 8], [100, 20, 12]];
const crcDoc = () => "event/carcinid" + (S && S.crcPrev && S.crcPrev.w ? "_prev" : "");
function crcRaw() { return G.mode === "online" ? (G.crcDoc || {})[crcDoc()] || null : ((S && S.ldb) || {})[crcDoc()] || null; }
function crcNorm(src) { const k = crcKey(), o = src && src.k === k ? src : { k }; o.sup = +o.sup || 0; o.con = o.con || {}; o.cday = o.cday || {}; return o; }
let CSC = {};
function crcStC(T) { const src = crcRaw(), d = crcDoc(); if (CSC.src === src && CSC.d === d && Math.abs(T - CSC.t) < 2000) return CSC.st; CSC = { src, d, t: T, st: crcNorm(src ? jcopy(src) : null) }; return CSC.st; }
function crcSupPct(st) { const n = Object.keys(st.con).length; return Math.min(1, st.sup / (300 + 90 * n)); }
function crcCon(st, pts, T) { const day = Math.floor(T / 864e5), c = st.cday[G.me] && st.cday[G.me][0] === day ? st.cday[G.me] : [day, 0], add = Math.max(0, Math.min(pts, CRC_DAYCAP - c[1]));
  c[1] += add; st.cday[G.me] = c; st.con[G.me] = (st.con[G.me] || 0) + add; st.sup += add; return add; }
function crcQueue(pts) { const M = crcS(); M.pend = (M.pend || 0) + pts; dirty(); crcFlush(); }
let CRC_FL = 0;
async function crcFlush(force) { const M = crcS(), T = now(); if (!M.pend || G.crcFlushing || (!force && T - CRC_FL < 120e3) || !G.ready) return; CRC_FL = T; G.crcFlushing = 1;
  try { const ref = adb().doc(crcDoc()); for (let i = 0; i < 6; i++) { const r = ref.acquire ? await ref.acquire({ holder: G.me, ttlMs: 10000 }) : { acquired: 1 }; if (r.acquired) break; await sleep(1200); }
    const snap = await casGet(ref), cur = crcNorm(snap.exists ? snap.data() : null); crcCon(cur, M.pend, T);
    if (await casSet(ref, snap, cur)) { M.pend = 0; if (G.mode === "online") { G.crcDoc = G.crcDoc || {}; G.crcDoc[crcDoc()] = cur; } CSC = {}; dirty(); } } catch (e) {} finally { G.crcFlushing = 0; } }
setInterval(() => { try { if (S && S.crc && S.crc.pend) crcFlush(); } catch (e) {} }, 60e3);
function crcNearest(T, mon) { const h = originPlanet() || myPlanets()[0]; if (!h) return null; const hp = pos(h, T); let best = null, bd = 1e9;
  for (const x of mon === "crcpat" ? CRC_PATS : CRC_NESTS) { if (!crcLive(x, T) || pirDown(x) > T) continue; const q = pos(x, T), d = Math.hypot(q.x - hp.x, q.y - hp.y) * (fogSeen(q.x, q.y) ? 1 : 3); if (d < bd) { bd = d; best = x; } } return best; }
function crcBand(T) { const w = crcWeek(T), c = crcClock(T); if (w === 5) return "";
  if (w === 0) { if (-c.e > 3 * 864e5) return ""; return `<button class="omb fin crcb soon" data-act="crcOpen"><b>❖ TIDE OF THE CARCINID</b><span>in ${ftime(-c.e)}</span></button>`; }
  { const M = crcS(); if (!M.intro && G.ready) { M.intro = 1; dirty(); setTimeout(() => { try { note("Tide of the Carcinid: Abyssal Breach Zones are opening across the galaxy. Open the event from the band at the top of the map.", "warn"); } catch (e) {} }, 1500); } }
  return `<button class="omb fin crcb" data-act="crcOpen"><b>❖ TIDE OF THE CARCINID</b><span>Week ${w} · ${CRC_WEEKS[w - 1][0]}</span></button>`; }
function crcInfo(x, T) { const L = crcLoot(x, crcStage(x, T)), sal = [L.chitin ? `${L.chitin} Abyssal Chitin` : "", L.coral ? `${L.coral} Coral Alloy` : "", L.resin ? `${L.resin} Tidal Resin` : ""].filter(Boolean).join(" · ") + ` · +${L.pts} tide points`;
  return (x.mon === "crcpat" ? `Scout patrol</dd><dt>The patrol</dt><dd>${crcForceTxt(x)}` : `Stage ${crcStage(x, T)} · ${CRC_STAGE[crcStage(x, T)]}</dd><dt>The garrison</dt><dd>${crcForceTxt(x)}`) + `</dd><dt>Tide salvage</dt><dd>${sal}`; }
/* the owner's paintings (art/carcinid; the rest of the set is kept there for the later weeks) */
const CRC_ART = { cscut: "drone", cspit: "spitter", charv: "harvester", cguard: "guardian", cfrig: "frigate", cint: "interceptor", carcinid: "crownbrood", crcpat: "frigate" };
const CRC_CD = { cscut: "The Empire's foot soldier. Small, fast, and never alone.", cspit: "A living coral battery that lobs searing spore-shot from its back.", charv: "Strips wrecks and asteroids for the brood, its resin sacs glowing.", cguard: "A walking bulwark. Its shell turns aside what our guns throw at it.", cfrig: "The scouts' flagship, a carapace hull with folded legs for landing.", cint: "A split-claw hunter built to run down lone ships." },
  CRC_CS = { cscut: "Stage 1", cspit: "Stage 1", charv: "Stage 1", cguard: "Stage 2", cfrig: "Patrols · Stage 2", cint: "Patrols" };
function shCarcinid() { const T = now(), M = crcS(), w = crcWeek(T), c = crcClock(T), own = ownerFree() && G.mode !== "offline" || G.owner, on = w >= 1 && w <= 4;
  const live = CRC_NESTS.filter(x => crcLive(x, T)), up = live.filter(x => pirDown(x) <= T), byS = [0, 0, 0, 0, 0]; up.forEach(x => byS[crcStage(x, T)]++); const pats = CRC_PATS.filter(x => crcLive(x, T) && pirDown(x) <= T).length;
  const when = w === 0 ? `Begins in ${ftime(-c.e)}` : w === 5 ? "The tide has turned" : w === 4 ? `Ends in ${ftime(CRC_LEN - c.e)}` : `Week ${w + 1} in ${ftime(w * CRC_WK - c.e)}`;
  const weeks = CRC_WEEKS.map(([t], i) => `<div class="mimwk crcwk${i + 1 === w ? " on" : i + 1 < w ? " past" : ""}"><b>Week ${i + 1}</b><span>${t}</span></div>`).join("");
  const st = crcStC(T), pct = crcSupPct(st), my = (st.con[G.me] || 0) + (M.pend || 0), n = Object.keys(st.con).length;
  const sup = `<h3>Abyssal Suppression</h3><div class="mimsup"><div class="mimbar big crcbar"><i style="width:${Math.round(pct * 100)}%"></i></div><b>${Math.round(pct * 100)}%</b></div>
    <p class="note" style="margin-top:4px">Every Breach Zone and patrol any commander destroys pushes the Abyss back. ${n} commander${n === 1 ? "" : "s"} so far · your share ${fmt(my)} point${my === 1 ? "" : "s"}${M.pend ? " (sending)" : ""}. ${pct >= 1 ? "<b>The Breaches are suppressed: every garrison is a quarter weaker.</b>" : "At 100% every garrison is a quarter weaker."}</p>
    <div class="crcms">${CRC_SUPM.map(([p, sh, rs]) => { const got = M.got["s" + p], ok = pct * 100 >= p && my > 0; return `<div class="crcm${got ? " got" : ok ? " ok" : ""}"><b>${p}%</b><small>◆${sh} · ${rs} Resin</small>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${ok ? " pri" : ""}" data-act="crcSup" data-p="${p}"${ok ? "" : " disabled"}>Claim</button>`}</div>`; }).join("")}</div>`;
  const obj = on ? `<h3>Exploration orders · week ${w}</h3>` + CRC_OBJ.map(([id, t, need, sh, mt]) => { const k = Math.min(need, crcObjN(w, id)), done = k >= need, got = M.got[`w${w}${id}`];
    return `<div class="mimobj crcobj"><div><b>${t}</b><div class="bar"><i style="width:${k / need * 100}%"></i></div><small>${k}/${need} · reward ◆${sh} and ${Object.entries(mt).map(([m, v]) => `${v} ${CRC_MAT[m][0]}`).join(", ")}</small></div>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${done ? " pri" : ""}" data-act="crcClaim" data-w="${w}" data-id="${id}"${done ? "" : " disabled"}>Claim</button>`}</div>`; }).join("") : "";
  const mats = Object.entries(CRC_MAT).map(([k, [nm, ic, col]]) => `<div class="mimmat"><img class="crcmi" src="art/carcinid/m_${k}.webp" alt=""><b>${fmt(M.m[k] || 0)}</b><small>${nm}</small></div>`).join("");
  const cls = ["cscut", "cspit", "charv", "cguard", "cfrig", "cint"];
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${CRC_COL}">Seasonal invasion</div><h2>❖ Tide of the Carcinid</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="mimban crcban"><img src="art/carcinid/banner.webp" alt=""><div><b>${on ? `Week ${w} · ${CRC_WEEKS[w - 1][0]}` : w === 0 ? "The deep is stirring" : "The tide has turned"}</b><span>${when}${c.prev ? " · owner preview" : ""}</span></div></div>
  <details class="crclore"${on && !M.loreSeen ? " open" : ""}><summary>The Abyss wakes</summary><p>Below the Kraken Deep lies the Abyss, a sea older than the stars. Before the Architects built their prison, it belonged to the Carcinid Abyssal Empire: armoured legions who bred the great ocean beasts as war mounts. The Leviathan, the Kraken and the serpents of the deep were theirs before they were ours.</p><p>Every time a Warden fell, the seal over the Abyss grew thinner. Now it has torn. Breach Zones are opening across the galaxy, and the Empire is coming through them, one tide at a time.</p></details>
  <p class="note">${on ? CRC_WEEKS[w - 1][1] : w === 0 ? "Deep-scan buoys in the outer layers are picking up pressure waves where there is no water. Something is pressing against the dark from the other side." : "The Breaches have sealed. The Abyss remembers."}</p>
  <div class="mimwks">${weeks}</div>
  ${on ? `<div class="mimst crcst">${[1, 2, 3, 4].map(s => `<div class="s${s}${s > CRC_CAP ? " off" : ""}"><b>${s > CRC_CAP ? "–" : byS[s]}</b><small>Stage ${s}<br>${CRC_STAGE[s]}</small></div>`).join("")}</div>
  <div class="crcfind"><button class="btn pri" data-act="crcFind"${up.length ? "" : " disabled"}>Nearest Breach Zone</button><button class="btn" data-act="crcFindP"${pats ? "" : " disabled"}>Nearest scout patrol (${pats})</button></div>` : ""}
  ${obj}${on || w === 5 ? sup : ""}
  <h3>Season materials</h3><div class="mimmats">${mats}</div><p class="note" style="margin-top:6px">Tide points: <b>${fmt(M.pts)}</b>. Every Breach Zone pays Abyssal Chitin; Stage 2 and above also gives up Coral Alloy; scout patrols carry Tidal Resin. Keep them: the Abyssal forges open later in the tide.</p>
  <h3>The Abyssal Empire</h3><div class="mimcls">${cls.map(k => `<div class="mimcl crccl"><img src="art/carcinid/${CRC_ART[k]}.webp" alt="" loading="lazy"><div><b>${AL[k].n}</b><small>${CRC_CD[k]}</small><em>${CRC_CS[k]}</em></div></div>`).join("")}</div>
  ${own ? `<div class="mimown"><small>Owner preview: see the tide as it will look in a given week (this device only).</small><div>${[0, 1, 2, 3, 4].map(k => `<button class="btn${((S.crcPrev || {}).w || 0) === k ? " pri" : ""}" data-act="crcPrev" data-w="${k}">${k ? "Week " + k : "Off"}</button>`).join("")}</div></div>` : ""}`; }
/* the Battle Lab */
const CRC_LAB = [["crc1", "Breach Zone · Stage 1", () => ({ cnest: 1, cscut: 7, charv: 1, cspit: 1 })], ["crc2", "Breach Zone · Stage 2", () => ({ cnest: 1, cscut: 8, charv: 1, cspit: 3, cguard: 2, cfrig: 1 })], ["crcp", "Carcinid scout patrol", () => ({ cfrig: 2, cint: 5 })]];
function crcLabFight(k) { const L = CRC_LAB.find(x => x[0] === k); if (!L) return; const D0 = L[2](), A0 = { battleship: 20, destroyer: 20, fighter: 60, corvette: 20 }, lvl = 20;
  const res = simulate(stacksOf(A0, techOf(null), G.me), stacksOf(D0, { mon: lvl }, "monster"));
  const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Battle Lab · ${L[1]}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: L[1], mon: k === "crcp" ? "crcpat" : "carcinid", lvl, ptype: "ocean", fortL: 0, alien: true, pirate: true,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
  closeSheet(); playBattle(rep); }
function crcLabHTML(row0, b) { const p = S.crcPrev || {}, row = (ic, n, sub, btns) => `<div class="strow" style="flex-wrap:wrap"><div style="flex:1 1 100%;min-width:0"><b>${ic} ${esc(n)}</b>${sub ? `<div class="note">${sub}</div>` : ""}</div><div style="display:flex;flex-wrap:wrap;gap:6px">${btns}</div></div>`;
  return row("❖", "The tide, week by week", `Breach Zones, patrols and the hub as they will be · ${p.w ? `previewing week ${p.w}` : "off"} · phase 1 builds week 1`, [1, 2, 3, 4].map(w => b("crcLabWeek", String(w), "W" + w)).join("") + b("crcLabWeek", "0", "Off") + b("crcOpen", "", "Hub"))
    + CRC_LAB.map(([k, n]) => row0("❖", n, "A small fleet against it", b("crcLabFight", k, "⚔ Watch"))).join(""); }
