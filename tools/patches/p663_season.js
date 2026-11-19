/* ---------- v663 the Mimic Protocol: the season, its hives and their spread ----------
   A four-week invasion that opens with the second Void Pass season (Season of the Cube). 120 hives emerge on their own spiral: 40 in
   week 1, 40 more in week 2 and week 3. Each grows through four stages (Infestation, Expansion, Alpha Dominion, Omega Convergence),
   capped by the week (week 1 reaches Expansion, weeks 2 and 3 Alpha Dominion, week 4 Omega Convergence), and its garrison grows with
   it. A hive you destroy regrows from Stage 1 after 12 hours. The owner can preview any week ahead of time from the hub. */
const MIM_U = { mstalk: 1, mharv: 1, mhunt: 1, massim: 1, mguard: 1, mtitan: 1, mnest: 1 };
Object.assign(MON, { mimic: { n: "Mimic Hive", sp: "Mimic Hive", ic: "🜏", col: "#5fd8ff", rgb: "95,216,255", per: 99, d: "A nest of the Mimic Protocol: black cable spires closed round a glowing neural core, breeding more of its kind. It grows through four stages, and every stage brings a deadlier brood. Destroy it before it matures.", names: ["Hive"] } });
const MIM_N = 120, MIM_WK = 7 * 864e5, MIM_LEN = 28 * 864e5, MIM_REGROW = 12 * 3600e3;
const MIM_STAGE = ["", "Infestation", "Expansion", "Alpha Dominion", "Omega Convergence"];
const MIM_WEEKS = [["First Contact", "The infestation begins. Small hives are emerging in quiet sectors, breeding Stalkers and Harvesters."], ["Alpha Ascension", "The hives are growing, and something is coordinating them. Larger nests, specialised Mimics, stronger rewards."], ["The Great Assimilation", "The hives are absorbing our technology. Assimilators and Guardians now defend the mature nests."], ["Omega Awakens", "Every surviving hive is feeding neural energy toward one point in the dark. Break them before Omega wakes."]];
const MIM_HIVES = (() => { const out = [], GOLD = Math.PI * (3 - Math.sqrt(5)), lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6;
  for (let j = 0; j < MIM_N; j++) { const u = (j + .45) / MIM_N, rad = Math.sqrt(lo * lo + u * (hi * hi - lo * lo)), a = (5.3 + j * GOLD) % TAU, lvl = (layerOf(rad).n - 1) * 5 + 2 + (j * 3) % 4;
    out.push({ id: "mh" + j, kind: "pirate", mon: "mimic", mj: j, lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: `Mimic Hive ${String.fromCharCode(65 + (j * 7) % 26)}-${10 + j}` }); } return out; })();
const mimT0 = () => VP_BASE + VP_LEN; /* the second Void Pass season */
function mimClock(T) { const p = S && S.mimPrev; if (p && p.w && ownerFree()) return { e: (p.w - 1) * MIM_WK + 3600e3 + Math.max(0, T - p.at), prev: 1 }; return { e: T - mimT0(), prev: 0 }; }
const mimWeek = T => { const e = mimClock(T).e; return e < 0 ? 0 : e >= MIM_LEN ? 5 : 1 + Math.floor(e / MIM_WK); };
const mimEm = x => Math.floor(Math.min(x.mj, 119) / 40) * MIM_WK + (x.mj % 40) * 1.1 * 3600e3;
function mimLive(x, T) { const e = mimClock(T).e; return e >= mimEm(x) && e < MIM_LEN; }
function mimStage(x, T) { const c = mimClock(T), down = ((S && S.pir) || {})[x.id] || 0, born = Math.max(mimEm(x), down ? down - T + c.e : -1e15), wk = Math.max(1, Math.min(4, 1 + Math.floor(c.e / MIM_WK)));
  return Math.max(1, Math.min(1 + Math.floor(Math.max(0, c.e - born) / (3.5 * 864e5)), wk >= 4 ? 4 : Math.min(3, wk + 1))); }
function mimForce(x, T) { const st = mimStage(x, T || now()), n = 1 + Math.floor(x.lvl / 4), o = { mnest: 1, mstalk: 2 + n, mharv: 1 };
  if (st >= 2) { o.mstalk += 1; o.mharv = 2; o.mhunt = 1 + (n >> 1); }
  if (st >= 3) { o.massim = 1 + Math.floor(n / 3); o.mguard = 1 + Math.floor(n / 3); }
  if (st >= 4) { o.mtitan = 1; o.mguard += 1; } return o; }
const mimForceTxt = x => Object.entries(mimForce(x)).filter(([k]) => k !== "mnest").map(([k, v]) => `${v} ${AL[k].n.replace("Mimic ", "")}`).join(" · ");
/* the season's own loot: Mimic Tissue from every hive, Assimilated Alloy from Stage 2, Neural Core Fragments from Stage 3 (more from a Brood Titan) */
const MIM_MAT = { tis: ["Mimic Tissue", "❋", "#7fe0ff"], alloy: ["Assimilated Alloy", "▰", "#9fb4cc"], ncf: ["Neural Core Fragment", "✺", "#5fd8ff"], cat: ["Alpha Neural Catalyst", "✹", "#b48cff"], osh: ["Omega Core Shard", "◈", "#e8f6ff"] };
const mimKey = () => String(mimT0());
function mimS() { const k = mimKey(); if (!S.mim || S.mim.k !== k) S.mim = { k, m: {}, pts: 0, kills: [0, 0, 0, 0, 0], got: {} }; return S.mim; }
function mimLoot(x, st) { return { tis: 2 + st * 2 + Math.floor(x.lvl / 5), alloy: st >= 2 ? st : 0, ncf: st >= 3 ? st - 2 + (st >= 4 ? 1 : 0) : 0, pts: 25 * st + x.lvl }; }
function mimWin(x, rep, T) { const st = mimStage(x, T), M = mimS(), L = mimLoot(x, st); for (const k of ["tis", "alloy", "ncf"]) if (L[k]) M.m[k] = (M.m[k] || 0) + L[k];
  M.pts += L.pts; M.kills[st] = (M.kills[st] || 0) + 1; { const w = Math.max(1, Math.min(4, mimWeek(T))); M.wk = M.wk || {}; const a = M.wk[w] || (M.wk[w] = [0, 0, 0, 0, 0]); a[st]++; } rep.mim = { st, tis: L.tis, alloy: L.alloy, ncf: L.ncf, pts: L.pts }; dirty();
  note(`${x.name} destroyed at Stage ${st} (${MIM_STAGE[st]}). Salvaged ${L.tis} Mimic Tissue${L.alloy ? `, ${L.alloy} Assimilated Alloy` : ""}${L.ncf ? `, ${L.ncf} Neural Core Fragment${L.ncf > 1 ? "s" : ""}` : ""} · +${L.pts} invasion points.`, "win"); }
/* one objective a week: [stage at least, hives, shards, tissue] */
const MIM_OBJ = [[1, 3, 5, 10], [2, 5, 10, 20], [3, 3, 15, 30], [4, 5, 20, 40]];
const mimObjN = w => { const M = mimS(), o = MIM_OBJ[w - 1], a = (M.wk || {})[w] || []; let n = 0; for (let s = o[0]; s <= 4; s++) n += a[s] || 0; return n; };
/* the band on the map and the planet while the invasion runs (and for three days before it) */
function mimBand(T) { const w = mimWeek(T), c = mimClock(T); if (w === 5) return ""; if (w === 0) { if (-c.e > 3 * 864e5) return ""; return `<button class="omb fin mimb soon" data-act="mimOpen"><b>🜏 THE MIMIC PROTOCOL</b><span>in ${ftime(-c.e)}</span></button>`; }
  return `<button class="omb fin mimb" data-act="mimOpen"><b>🜏 THE MIMIC PROTOCOL</b><span>Week ${w} · ${MIM_WEEKS[w - 1][0]}</span></button>`; }
function mimNearest(T) { const h = originPlanet() || myPlanets()[0]; if (!h) return null; const hp = pos(h, T); let best = null, bd = 1e9;
  for (const x of MIM_HIVES) { if (!mimLive(x, T) || pirDown(x) > T) continue; const q = pos(x, T), d = Math.hypot(q.x - hp.x, q.y - hp.y) * (fogSeen(q.x, q.y) ? 1 : 3); if (d < bd) { bd = d; best = x; } } return best; }
function shMimic() { const T = now(), M = mimS(), w = mimWeek(T), c = mimClock(T), own = ownerFree() && G.mode !== "offline" || G.owner;
  const live = MIM_HIVES.filter(x => mimLive(x, T)), up = live.filter(x => pirDown(x) <= T), byS = [0, 0, 0, 0, 0]; up.forEach(x => byS[mimStage(x, T)]++);
  const when = w === 0 ? `Begins in ${ftime(-c.e)}` : w === 5 ? "The invasion is over" : w === 4 ? `Ends in ${ftime(MIM_LEN - c.e)}` : `Week ${w + 1} in ${ftime(w * MIM_WK - c.e)}`;
  const weeks = MIM_WEEKS.map(([t, d], i) => `<div class="mimwk${i + 1 === w ? " on" : i + 1 < w ? " past" : ""}"><b>Week ${i + 1}</b><span>${t}</span></div>`).join("");
  const cls = ["mstalk", "mharv", "mhunt", "massim", "mguard", "mtitan"], CD = { mstalk: "The basic drone. Fast, numerous, all claws.", mharv: "Gathers biomass and salvage into its glowing sac.", mhunt: "Runs down weak and isolated fleets.", massim: "Wears the plating of the ships it has absorbed.", mguard: "Armoured in plates. Shields the hive and its kin.", mtitan: "A rare elite, born only in mature hives." },
    CS = { mstalk: 1, mharv: 1, mhunt: 2, massim: 3, mguard: 3, mtitan: 4 };
  const obj = w >= 1 && w <= 4 ? (() => { const o = MIM_OBJ[w - 1], n = Math.min(o[1], mimObjN(w)), done = n >= o[1], got = M.got["w" + w];
    return `<div class="mimobj"><div><b>This week: destroy ${o[1]} hive${o[1] > 1 ? "s" : ""}${o[0] > 1 ? ` at Stage ${o[0]} or above` : ""}</b><div class="bar"><i style="width:${n / o[1] * 100}%"></i></div><small>${n}/${o[1]} · reward ◆${o[2]} and ${o[3]} Mimic Tissue</small></div>${got ? `<span class="pill">Claimed</span>` : `<button class="btn${done ? " pri" : ""}" data-act="mimClaim" data-w="${w}"${done ? "" : " disabled"}>Claim</button>`}</div>`; })() : "";
  const mats = Object.entries(MIM_MAT).map(([k, [n, ic, col]]) => `<div class="mimmat"><i style="color:${col}">${ic}</i><b>${fmt(M.m[k] || 0)}</b><small>${n}</small></div>`).join("");
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:#5fd8ff">Seasonal invasion</div><h2>🜏 The Mimic Protocol</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="mimban"><img src="art/mimic/banner.webp" alt=""><div><b>${w >= 1 && w <= 4 ? `Week ${w} · ${MIM_WEEKS[w - 1][0]}` : w === 0 ? "Something is waking" : "The swarm is broken"}</b><span>${when}${c.prev ? " · owner preview" : ""}</span></div></div>
  <p class="note">${w >= 1 && w <= 4 ? MIM_WEEKS[w - 1][1] : w === 0 ? "Recent Cube activity has weakened something that was never meant to be opened. Our scanners are picking up movement in the empty sectors." : "The hives are silent. For now."}</p>
  <div class="mimwks">${weeks}</div>
  ${w >= 1 && w <= 4 ? `<div class="mimst">${[1, 2, 3, 4].map(s => `<div class="s${s}"><b>${byS[s]}</b><small>Stage ${s}<br>${MIM_STAGE[s]}</small></div>`).join("")}</div>
  <button class="btn pri wide" data-act="mimFind"${up.length ? "" : " disabled"}>Find the nearest hive</button>` : ""}
  ${obj}
  <h3>Season materials</h3><div class="mimmats">${mats}</div><p class="note" style="margin-top:6px">Invasion points: <b>${fmt(M.pts)}</b>. Every hive pays Mimic Tissue; mature hives also give up Assimilated Alloy and Neural Core Fragments.</p>
  <h3>The swarm</h3><div class="mimcls">${cls.map(k => `<div class="mimcl"><canvas data-ship="${k}" width="224" height="112"></canvas><div><b>${AL[k].n}</b><small>${CD[k]}</small><em>From Stage ${CS[k]}</em></div></div>`).join("")}</div>
  ${own ? `<div class="mimown"><small>Owner preview: see the invasion as it will look in a given week.</small><div>${[0, 1, 2, 3, 4].map(n => `<button class="btn${((S.mimPrev || {}).w || 0) === n ? " pri" : ""}" data-act="mimPrev" data-w="${n}">${n ? "Week " + n : "Off"}</button>`).join("")}</div></div>` : ""}`; }
function mimGo(x) { closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); }
  setTimeout(() => { try { const c = G3 && G3.cam, q = P3(x, now()); if (c) { c.follow = null; c.followFleet = null; c.goal = { tx: q.x, ty: q.y, tz: q.z, dist: 26, th: .8 }; } } catch (e) {} }, 300);
  setTimeout(() => { try { if (view === "galaxy" && !sheet && !battle) openSheet({ type: "pirate", id: x.id }); } catch (e) {} }, 2600); }
