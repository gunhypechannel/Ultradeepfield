/* ---------- v628 the elements, balanced and expanded (owner: "if only those bosses drop element runes shouldn't we find different way to
   get them I want them balanced in the game" ... "Do it all"). Rune shards come from everyday play (daily tasks, monsters, pirates,
   station expeditions, alliance help, the worlds you hold, a daily Elemental Trial, the Glyph Wheel and a Void Shop cache); ten make
   a rune. Everyday shards are capped per element each week, so the super bosses stay the fastest road (they also pay shards to
   everyone who fought). Three spare runes transmute into one of another element. A ring at its top tier keeps growing through
   Mastery. Two full rings make a pair bonus, five make Harmony. Bosses and monsters carry an element, and the ring that counters it
   hits harder (Water beats Fire, Fire beats Air, Air beats Earth, Earth beats Water, Spirit meets Spirit). ---------- */
const ESH_N = 10, ESH_CAP = 25, ESH_COL = 1, MAST_MAX = 10, MAST_COST = 5, MAST_PER = .4, EL_AFF_K = .5, EL_AFF_MAX = 12;
const PTYPE_EL = { lava: "fire", ocean: "water", ice: "water", desert: "earth", toxic: "earth", gas: "air", terran: "spirit" };
const EL_PTYPE = { fire: "lava", water: "ocean", earth: "desert", air: "gas", spirit: "terran" };
const BOSS_EL = { dev: "fire", tyr: "fire", efi: "fire", aex: "fire", lev: "water", krk: "water", eic: "water", med: "water", ovl: "earth", brd: "earth", col: "earth", ena: "earth", war: "air", est: "air", khz: "air", wym: "spirit", eli: "spirit", vae: "spirit" };
const MON_EL = { swhale: "water", ssquid: "water", vmanta: "spirit", swasp: "air", ctort: "earth", gspider: "air" };
const EL_BEATS = { water: "fire", fire: "air", air: "earth", earth: "water", spirit: "spirit" };
const EL_ICON = { fire: "🔥", water: "💧", earth: "⛰", air: "🌪", spirit: "✦" };
const elCounter = x => Object.keys(EL_BEATS).find(k => EL_BEATS[k] === x);
const elWeek = () => Math.floor((now() / 864e5 + 3) / 7), elDay = () => Math.floor(now() / 864e5);
function eshWeek() { const w = elWeek(); if (!S.eshW || S.eshW.w !== w) S.eshW = { w, n: {} }; return S.eshW; }
const eshLeft = e => Math.max(0, ESH_CAP - (eshWeek().n[e] || 0));
/* shards of one element (or a random one); every ten form a rune of that element on the spot */
function grantShards(n, why, el, o = {}) { if (!S || !(n > 0)) return 0; S.esh = S.esh || {}; S.runes = S.runes || {}; const ks = Object.keys(ELEM), add = {}; let tot = 0;
  for (let i = 0; i < n; i++) { const e = ELEM[el] ? el : ks[(Math.random() * ks.length) | 0]; if (!o.nocap) { if (eshLeft(e) <= 0) continue; const W = eshWeek(); W.n[e] = (W.n[e] || 0) + 1; } add[e] = (add[e] || 0) + 1; tot++; }
  const made = []; for (const e in add) { S.esh[e] = (S.esh[e] || 0) + add[e]; while (S.esh[e] >= ESH_N) { S.esh[e] -= ESH_N; S.runes[e] = (S.runes[e] || 0) + 1; made.push(ELEM[e].n); } }
  if (made.length) G.runeMade = { at: performance.now() };
  if (tot && !o.quiet) note(`${why}: +${tot} rune shard${tot > 1 ? "s" : ""} (${Object.entries(add).map(([e, k]) => `${k} ${ELEM[e].n}`).join(", ")})${made.length ? `. ${made.length > 1 ? made.length + " runes" : "A rune"} formed: ${made.join(", ")}!` : ""}`, made.length ? "win" : "info");
  else if (made.length) toast(`A rune formed: ${made.join(", ")}!`, "win");
  try { dirty(); } catch (e) {} return tot; }
/* the worlds you hold make shards of their element: one a day per world (at most three days are counted while you're away) */
function eshColonies() { if (!S || !G.ready) return; const T = now(); if (!S.eshAt) { S.eshAt = T; return; } const dt = Math.min(3 * 864e5, T - S.eshAt); if (dt < 600e3) return; S.eshAt = T; S.eshF = S.eshF || {};
  let mine = []; try { mine = myPlanets(); } catch (e) {} for (const p of mine) { const e = PTYPE_EL[p.type]; if (e) S.eshF[e] = (S.eshF[e] || 0) + dt / 864e5 * ESH_COL; }
  for (const e in S.eshF) { const k = Math.floor(S.eshF[e]); if (k > 0) { S.eshF[e] -= k; grantShards(k, `Your ${ELEM[e].n.toLowerCase()} worlds`, e, { quiet: 1 }); } } }
setInterval(() => { try { eshColonies(); } catch (e) {} }, 60000);
/* Mastery, pairs and Harmony add to a ring's bonus, so every system that reads runePct gets them */
const ringM = e => Math.min(MAST_MAX, ((S && S.ringM) || {})[e] || 0);
const ringFull = e => runeOn(e) > 0 && runeOn(e) >= elemSlots(e);
const mastOpen = e => ringT(e) >= RING_MAX && ringFull(e);
const EL_PAIRS = [["Wildfire", "fire", "air", { fire: 2, air: 2 }, "+2% attack, +2% speed"], ["Bulwark", "water", "earth", { water: 2, earth: 2 }, "+2% shields, +2% armor"], ["Soulfire", "fire", "spirit", { fire: 2, spirit: 1 }, "+2% attack, +1% output"],
  ["Tidewind", "water", "air", { water: 2, air: 2 }, "+2% shields, +2% speed"], ["Living Stone", "earth", "spirit", { earth: 2, spirit: 1 }, "+2% armor, +1% output"]];
const pairOn = P => ringFull(P[1]) && ringFull(P[2]), harmonyOn = () => Object.keys(ELEM).every(ringFull);
function elExtra(e) { let v = ringM(e) * MAST_PER; for (const P of EL_PAIRS) if (pairOn(P)) v += P[3][e] || 0; if (harmonyOn()) v += 2; return v; }
const runePct = e => S ? Math.round((runePct0(e) + elExtra(e)) * 10) / 10 : 0;
/* affinity: the ring that counters a foe's element adds half its bonus as extra attack against it (up to +12%) */
function elAff(foe) { if (!ELEM[foe]) return null; const c = elCounter(foe); return { foe, c, pct: Math.min(EL_AFF_MAX, Math.round(runePct(c) * EL_AFF_K * 10) / 10) }; }
const elAffRep = foe => { const a = elAff(foe); return a && a.pct > 0 ? a : undefined; };
const techEl = foe => { const t = techOf(null), a = elAff(foe); return a && a.pct > 0 ? Object.assign({}, t, { weapons: t.weapons + a.pct / 10 }) : t; };
const techElVs = x => { const t = techVs(x), a = elAff(MON_EL[x.mon]); return x.mon && a && a.pct > 0 ? Object.assign({}, t, { weapons: t.weapons + a.pct / 10 }) : t; };
function elAffFlash(a) { try { const el = document.createElement("div"); el.className = "elaff"; el.style.setProperty("--c", ELEM[a.c].col);
  el.innerHTML = `<b>SUPER EFFECTIVE</b><span>${EL_ICON[a.c]} ${ELEM[a.c].n} ${a.c === a.foe ? "meets" : "beats"} ${ELEM[a.foe].n} ${EL_ICON[a.foe]} · +${a.pct}% attack</span>`; document.body.appendChild(el); setTimeout(() => el.remove(), 2600); } catch (e) {} }
/* the daily Elemental Trial: your home warships spar with an echo of today's element (nothing is lost) */
const trialEl = () => Object.keys(ELEM)[elDay() % 5];
function trialRun() { const e = trialEl(); if (S.trialD === elDay()) return toast("Today's Trial is done. A new element tomorrow.", "warn");
  const t0 = techOf(null), mine = {}; for (const [k, v] of Object.entries(S.ships || {})) { try { if (v > 0 && SH[k] && unitStat(k, t0).atk > 0) mine[k] = Math.floor(v); } catch (er) {} }
  if (!Object.keys(mine).length) return toast("Build some warships at home first: the Trial uses your home fleet.", "warn");
  const foe = {}; for (const k in mine) foe[k] = Math.max(1, Math.round(mine[k] * .75));
  const res = simulate(stacksOf(mine, techEl(e), G.me), stacksOf(foe, t0, "hive")), win = res.winner === "a", n = win ? 8 : 4;
  const rep = mkRep({ at: now(), kind: "attack", test: true, trial: e, title: `Elemental Trial · ${ELEM[e].n} Echo`, aUids: [G.me], aName: S.homeName + " Fleet", dName: `${ELEM[e].n} Echo`, lvl: myCmdLv(), ptype: EL_PTYPE[e], fortL: 0, alien: true, elAff: elAffRep(e),
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: {}, lossD: lossesOf(res.start.d, res.dLeft) });
  S.trialD = elDay(); S.reports.unshift(rep); if (S.reports.length > 25) S.reports.length = 25;
  grantShards(n, win ? `Elemental Trial won` : `Elemental Trial`, e, { nocap: 1 }); dirty(); playBattle(rep); }
