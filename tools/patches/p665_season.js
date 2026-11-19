/* ---------- v665 the Mimic Protocol, phase 2: the Alphas, their Neural Nexuses, and the server's Hive Suppression ----------
   From week 2 (Alpha Ascension) four Alphas rule the four quarters of the galaxy, each guarded by its own Neural Nexus (the owner's
   "Omega Neural Nexus" idea at regional scale). While its Nexus holds, an Alpha shrugs off 60% of the damage it takes and regrows 3
   sections an hour; break all four of the Nexus's crystal anchors and the Alpha is cut off for 30 minutes: no shield, no regrowth, then
   the network reconnects and the anchors stand again. Every hive the server destroys in an Alpha's quarter weakens it (up to +40% damage taken).
   An Alpha has 100 sections; one that falls stays dead until the next week, when a new one rises. Shared record: event/mimic
   {k, sup, con: {uid: points}, cday: {uid: [day, points]}, rk: [hives destroyed per quarter], a: {ma0..ma3: {w, hp, t, dmg, dead, last}},
   x: {mx0..mx3: {anc: [4], open}}} (owner previews use event/mimic_prev). Hive Suppression: every hive, Alpha section, Nexus section and
   weekly objective adds points (400 a commander a day at most); the meter is points against a target that grows with the number of
   commanders taking part, so a busy server fills it faster and a small one can still get there. It weakens Omega at the finale. */
Object.assign(MIM_U, { malpha1: 1, malpha2: 1, malpha3: 1, malpha4: 1, mnexus: 1 });
const MIM_AN = ["I", "II", "III", "IV"], MIM_AREG = ["the first quarter", "the second quarter", "the third quarter", "the fourth quarter"];
for (let i = 0; i < 4; i++) MON["alpha" + (i + 1)] = { n: "Alpha Sovereign " + MIM_AN[i], sp: "Alpha", ic: "⬢", col: ["#5fd8ff", "#b48cff", "#e4f4ff", "#5fffc8"][i], rgb: ["95,216,255", "180,140,255", "228,244,255", "95,255,200"][i], per: 99, d: "A regional sovereign of the Mimic swarm. It commands every hive in its quarter of the galaxy and draws its strength through its Neural Nexus. Break the Nexus to strip its shield, and burn its hives to weaken it.", names: ["Alpha"] };
MON.nexus = { n: "Neural Nexus", sp: "Neural Nexus", ic: "⬡", col: "#7ff0ff", rgb: "127,240,255", per: 99, d: "A holographic relay the Alpha uses to command its swarm. While it stands, the Alpha is shielded and heals. Break its four anchors to cut the Alpha off for 30 minutes.", names: ["Nexus"] };
const MIM_BOSS = {}, MIM_BOSSES = (() => { const out = [], lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6, rad = Math.sqrt(lo * lo + .42 * (hi * hi - lo * lo));
  for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2 + Math.PI / 4, lvl = (layerOf(rad).n - 1) * 5 + 5;
    const A = { id: "ma" + i, kind: "pirate", mon: "alpha" + (i + 1), reg: i, u: "malpha" + (i + 1), lvl, r: +rad.toFixed(2), a0: +a.toFixed(4), name: "Alpha Sovereign " + MIM_AN[i] }, X = { id: "mx" + i, kind: "pirate", mon: "nexus", reg: i, u: "mnexus", lvl, r: +(rad * .93).toFixed(2), a0: +(a + .05).toFixed(4), name: "Neural Nexus " + MIM_AN[i] };
    out.push(A, X); MIM_BOSS[A.id] = A; MIM_BOSS[X.id] = X; } return out; })();
const MIM_ANC = 25, MIM_OPEN = 30 * 60e3, MIM_REGEN = 3, MIM_DAYCAP = 400;
const mimReg = x => Math.floor((((x.a0 - Math.PI / 4) % TAU + TAU) % TAU) / (Math.PI / 2) + .5) % 4; /* the quarter a hive sits in, by its own angle */
const mimDoc = () => "event/mimic" + (S && S.mimPrev && S.mimPrev.w ? "_prev" : "");
function mimRaw() { return G.mode === "online" ? (G.mimDoc || {})[mimDoc()] || null : ((S && S.ldb) || {})[mimDoc()] || null; }
function mimNorm(src, T) { const k = mimKey(), w = Math.max(1, Math.min(4, mimWeek(T))), o = src && src.k === k ? src : { k };
  o.sup = +o.sup || 0; o.con = o.con || {}; o.cday = o.cday || {}; o.rk = Array.isArray(o.rk) ? o.rk : [0, 0, 0, 0]; o.a = o.a || {}; o.x = o.x || {};
  for (let i = 0; i < 4; i++) { const ai = "ma" + i, xi = "mx" + i; let A = o.a[ai]; if (!A || A.w !== w) A = o.a[ai] = { w, hp: 100, t: T, dmg: {}, dead: 0, last: "" };
    let X = o.x[xi]; if (!X) X = o.x[xi] = { anc: [MIM_ANC, MIM_ANC, MIM_ANC, MIM_ANC], open: 0 }; if (X.open && T >= X.open) { X.anc = [MIM_ANC, MIM_ANC, MIM_ANC, MIM_ANC]; X.open = 0; }
    if (!A.dead && A.hp < 100 && !X.open) { const add = Math.floor((T - (A.t || T)) / 3600e3 * MIM_REGEN); if (add > 0) { A.hp = Math.min(100, A.hp + add); A.t = T; } } if (X.open) A.t = T; }
  return o; }
const mimSt = T => mimStC(T);
const mimBossOn = T => { const w = mimWeek(T); return w >= 2 && w <= 4; };
function mimHid(x, T) { if (x.mon === "mimic") return !mimLive(x, T); const B = MIM_BOSS[x.id]; if (!B) return false; if (!mimBossOn(T)) return true; if (B.mon !== "nexus") { const A = mimSt(T).a[B.id]; return !!(A && A.dead); } return false; }
const mimOpen = (st, reg) => st.x["mx" + reg].open || 0;
function mimSupPct(st) { const n = Object.keys(st.con).length; return Math.min(1, st.sup / (250 + 80 * n)); }
function mimSupFx(p) { return { sh: Math.round(50 * p), rg: Math.round(60 * p), sw: Math.round(50 * p) }; }
const mimTier = p => p >= 200 ? ["Vanguard", "#ffd36b"] : p >= 60 ? ["Warden", "#9fe8ff"] : p >= 10 ? ["Scout", "#8fb"] : ["Not yet ranked", "#789"];
/* points earned this fight, held to the daily cap; returns what counts */
function mimCon(st, pts, T) { const day = Math.floor(T / 864e5), c = st.cday[G.me] && st.cday[G.me][0] === day ? st.cday[G.me] : [day, 0], add = Math.max(0, Math.min(pts, MIM_DAYCAP - c[1]));
  c[1] += add; st.cday[G.me] = c; st.con[G.me] = (st.con[G.me] || 0) + add; st.sup += add; return add; }
function alphaForce(x, T) { const st = mimSt(T || now()), B = MIM_BOSS[x.id]; if (B.mon === "nexus") { const X = st.x[B.id]; const n = X.anc.find(v => v > 0) || MIM_ANC; return { mnexus: n, mguard: 2, mharv: 2 }; }
  const A = st.a[B.id], live = MIM_HIVES.filter(h => mimReg(h) === B.reg && mimLive(h, T || now())).length; return { [B.u]: Math.max(1, A.hp), mguard: 2 + Math.floor(live / 10), mstalk: 4 }; }
/* the hives the player destroys feed the meter in batches (one shared write every few minutes at most) */
function mimQueue(pts, reg) { const M = mimS(); M.pend = (M.pend || 0) + pts; M.prk = M.prk || [0, 0, 0, 0]; M.prk[reg]++; dirty(); mimFlush(); }
let MIM_FL = 0;
async function mimFlush(force) { const M = mimS(), T = now(); if (!M.pend || G.mimFlushing || (!force && T - MIM_FL < 120e3) || !G.ready) return; MIM_FL = T; G.mimFlushing = 1;
  try { const ref = adb().doc(mimDoc()); for (let i = 0; i < 6; i++) { const r = ref.acquire ? await ref.acquire({ holder: G.me, ttlMs: 10000 }) : { acquired: 1 }; if (r.acquired) break; await sleep(1200); }
    const snap = await casGet(ref), cur = mimNorm(snap.exists ? snap.data() : null, T); mimCon(cur, M.pend, T); (M.prk || []).forEach((n, i) => cur.rk[i] = (cur.rk[i] || 0) + n);
    if (await casSet(ref, snap, cur)) { M.pend = 0; M.prk = [0, 0, 0, 0]; mimLocal(cur); dirty(); } } catch (e) {} finally { G.mimFlushing = 0; } }
function mimLocal(cur) { if (G.mode === "online") { G.mimDoc = G.mimDoc || {}; G.mimDoc[mimDoc()] = cur; } }
/* the fight: like a super boss, each Alpha unit (or Nexus unit) is one section; big fleets meet a boss that rises to match them */
function mimRise(mkA, mkD, u, n0, cap) { let { F, x } = wbRiseK(mkA(), mkD()); if (F <= 1) return { res: simulate(mkA(), mkD()), rise: 1 };
  const tgt = Math.min(cap, Math.max(1, Math.round(100 * clamp(.08 + .04 * Math.log10(x), .08, .2)))); let lo = 1, hi = 0, best = null;
  for (let i = 0; i < 9; i++) { const A = mkA(), D = mkD(); for (const s of D) { s.atk *= F; s.hull *= F; } const res = simulate(A, D), seg = n0 - clamp(Math.round(((res.dLeft || {})[u]) || 0), 0, n0), err = Math.abs(Math.min(seg, cap) - tgt);
    if (!best || err < best.err) best = { res, F, err }; if (err <= 2) break; if (seg > tgt) lo = F; else hi = F; F = hi ? Math.sqrt(Math.max(lo, 1) * hi) : F * Math.max(1.5, Math.pow(seg / Math.max(1, tgt), 1.6)); if (hi && hi / Math.max(lo, 1) < 1.03) break; }
  return { res: best.res, rise: best.F }; }
async function mimBossResolve(f) { const B = MIM_BOSS[f.xid], x = PB[f.xid]; G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(q => q !== f); };
  try { const at = f.arrive; if (!mimBossOn(at)) { note(`${B.name} was gone when our fleet arrived. Returning.`, "warn"); return home(); }
    const ref = adb().doc(mimDoc()); for (let i = 0; i < 8; i++) { const r = ref.acquire ? await ref.acquire({ holder: G.me, ttlMs: 15000 }) : { acquired: 1 }; if (r.acquired) break; await sleep(1500); }
    const snap = await casGet(ref), cur = mimNorm(snap.exists ? snap.data() : null, at), nx = B.mon === "nexus", X = cur.x["mx" + B.reg], A = cur.a["ma" + B.reg];
    if (!nx && A.dead) { note(`${B.name} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
    let ai = -1, n0; if (nx) { if (X.open) { note(`${B.name} is already broken. It reconnects in ${ftime(X.open - at)}. Fleet returning.`, "warn"); return home(); } ai = X.anc.findIndex(v => v > 0); n0 = X.anc[ai]; } else n0 = A.hp;
    const shielded = !nx && !X.open, weak = nx ? 0 : Math.min(.4, (cur.rk[B.reg] || 0) / 250), live = MIM_HIVES.filter(h => mimReg(h) === B.reg && mimLive(h, at)).length;
    const esc = nx ? { mguard: 2, mharv: 2 } : { mguard: 2 + Math.floor(live / 10), mstalk: 4 };
    const mkD = () => stacksOf(Object.assign({ [B.u]: n0 }, esc), { mon: B.lvl }, "monster");
    const mine0 = Object.assign({}, f.n), { res, rise } = mimRise(() => stacksOf(f.n, techVs(x), G.me), mkD, B.u, n0, n0);
    const left = clamp(Math.round(((res.dLeft || {})[B.u]) || 0), 0, n0), raw = n0 - left, seg = raw ? Math.min(n0, Math.max(1, Math.round(raw * (shielded ? .4 : 1) * (1 + weak)))) : 0; /* the Nexus shield keeps 60% of the damage off; the quarter's dead hives add up to 40% */
    let pts = 0, broke = 0; if (seg) { if (nx) { X.anc[ai] -= seg; if (X.anc[ai] <= 0) broke = 1; if (X.anc.every(v => v <= 0)) { X.open = at + MIM_OPEN; A.t = at; } pts = 3 * seg; }
      else { A.hp = n0 - seg; A.t = at; A.dmg[G.me] = (A.dmg[G.me] || 0) + seg; if (!A.hp) { A.dead = at; A.last = G.me; } pts = 4 * seg; } }
    const counted = pts ? mimCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; mimLocal(cur);
    const rep = mkRep({ at, kind: "attack", simLeft: left, title: `Assault on ${B.name}${nx ? ` · anchor ${ai + 1}` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: B.name, mimB: B.id, mimSeg: [n0, n0 - seg], omRise: rise > 1.01 ? Math.round(rise) : undefined,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1); if (rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info");
    if (seg) { const L = { m: 30000 * seg, c: 20000 * seg, g: 10000 * seg }, ratio = Math.min(1, fCargo(f) / Math.max(1, total(L))); rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = 2 * seg, M = mimS(); S.shards = (S.shards || 0) + sh; rep.shards = sh; S.wins++; evPts("hunt", seg * 50);
      if (nx) M.m.ncf = (M.m.ncf || 0) + seg; else { M.m.alloy = (M.m.alloy || 0) + seg; M.m.tis = (M.m.tis || 0) + 2 * seg; } M.pts += counted;
      logReward(`${B.name} bounty`, rep.loot, { shards: sh, kind: "battle" }); }
    if (shielded && seg) note(`${B.name} is shielded by its Neural Nexus: it shrugged off 60% of our damage. Break the Nexus's anchors to cut it off.`, "info");
    if (rise > 1.01) note(`${B.name} rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (nx && X.open && broke) note(`The ${B.name} collapsed! Alpha Sovereign ${MIM_AN[B.reg]} is cut off from the swarm for 30 minutes: no shield, no healing. Strike now.`, "win");
    else if (nx && broke) note(`Anchor ${ai + 1} of the ${B.name} shattered. ${X.anc.filter(v => v > 0).length} left.`, "win");
    if (!nx && A.dead) { bump("bosses"); note(`We brought down ${B.name}! Everyone who broke a section can claim the spoils.`, "win"); }
    else if (seg) note(`Our fleet broke ${seg} section${seg > 1 ? "s" : ""} ${nx ? `off anchor ${ai + 1} of the ${B.name} (${Math.max(0, X.anc[ai])} left)` : `off ${B.name} (${A.hp} of 100 left)`}. +${counted} Hive Suppression${counted < pts ? " (daily cap reached)" : ""}.`, "win");
    else note(`Our fleet couldn't break a section off ${B.name}. Send more firepower${shielded ? ", or break its Nexus first" : ""}.`, "warn");
    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} mimClaim(); home();
  } catch (e) { if (e === CAS_RETRY && await casAgain(f, mimBossResolve)) return; note(`Lost contact with the ${B.name} fight. Fleet returning.`, "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* a fallen Alpha: everyone who broke a section claims once, by share: Alpha Neural Catalysts, shards, Mimic Tissue; the final blow +2 Catalysts */
function mimClaim() { if (!S || !G.ready) return; const T = now(); if (!mimBossOn(T) && mimWeek(T) !== 5) return; const st = mimSt(T), M = mimS(); M.got = M.got || {};
  for (let i = 0; i < 4; i++) { const A = st.a["ma" + i], my = (A.dmg || {})[G.me] || 0, id = `a${i}w${A.w}`; if (!A.dead || !my || M.got[id]) continue; M.got[id] = 1;
    const tot = Object.values(A.dmg).reduce((a, b) => a + b, 0) || 1, share = my / tot, cat = Math.min(8, 2 + Math.round(share * 20)) + (A.last === G.me ? 2 : 0), sh = Math.min(40, 10 + Math.round(share * 60));
    M.m.cat = (M.m.cat || 0) + cat; M.m.tis = (M.m.tis || 0) + 20; S.shards = (S.shards || 0) + sh; logReward(`Alpha Sovereign ${MIM_AN[i]} slain`, null, { shards: sh, kind: "event" });
    note(`Alpha Sovereign ${MIM_AN[i]} is dead. Your share (${Math.round(share * 100)}%): ${cat} Alpha Neural Catalyst${cat > 1 ? "s" : ""}, ◆${sh} and 20 Mimic Tissue${A.last === G.me ? ", with the final blow" : ""}.`, "win"); dirty(); } }
function mimBossInfo(x, T) { const st = mimSt(T), B = MIM_BOSS[x.id], X = st.x["mx" + B.reg], A = st.a["ma" + B.reg], nx = B.mon === "nexus";
  const live = MIM_HIVES.filter(h => mimReg(h) === B.reg && mimLive(h, T)).length, weak = Math.round(Math.min(.4, (st.rk[B.reg] || 0) / 250) * 100);
  const bar = (v, mx, col) => `<div class="mimbar"><i style="width:${v / mx * 100}%;background:${col}"></i></div>`;
  if (nx) return `<div class="mimboss"><b>${X.open ? `Collapsed · reconnects in <span data-end="${X.open}">${ftime(X.open - T)}</span>` : `Anchors ${X.anc.filter(v => v > 0).length} of 4 standing`}</b>
    ${X.anc.map((v, i) => `<div class="mimanc"><span>Anchor ${i + 1}</span>${bar(Math.max(0, v), MIM_ANC, "linear-gradient(90deg,#2fa8ff,#9ff0ff)")}<small>${Math.max(0, v)}/${MIM_ANC}</small></div>`).join("")}
    <p class="note">While the Nexus stands, Alpha Sovereign ${MIM_AN[B.reg]} shrugs off 60% of all damage and regrows ${MIM_REGEN} sections an hour. Break all four anchors and it is cut off for 30 minutes. Each section broken: +3 Hive Suppression and a Neural Core Fragment.</p></div>`;
  return `<div class="mimboss"><b>${A.dead ? "Slain this week. A new Alpha rises next week." : `${A.hp} of 100 sections`}</b>${bar(A.hp, 100, "linear-gradient(90deg,#7a3cff,#5fd8ff)")}
    <dl class="kv"><dt>Neural Nexus</dt><dd>${X.open ? `<span style="color:var(--green)">Broken: no shield, no healing for <span data-end="${X.open}">${ftime(X.open - T)}</span></span>` : `<span style="color:var(--amber)">Connected: shrugs off 60% of damage, regrowing</span>`}</dd>
    <dt>Hives in its quarter</dt><dd>${live} alive · takes +${weak}% damage from the server's hive kills</dd><dt>Your sections</dt><dd>${(A.dmg || {})[G.me] || 0}</dd></dl>
    <p class="note">Each section broken: +4 Hive Suppression, Assimilated Alloy and Mimic Tissue. When it falls, everyone who broke a section shares Alpha Neural Catalysts by damage, and the final blow earns 2 more.</p></div>`; }
let MSC = {}; /* mimSt reads the shared record many times a frame (map visibility): one normalised copy per two seconds per source */
function mimStC(T) { const src = mimRaw(), d = mimDoc(); if (MSC.src === src && MSC.d === d && Math.abs(T - MSC.t) < 2000) return MSC.st; MSC = { src, d, t: T, st: mimNorm(src ? jcopy(src) : null, T) }; return MSC.st; }
function mimHubBoss(T, w) { const st = mimStC(T), pct = mimSupPct(st), fx = mimSupFx(pct), my = st.con[G.me] || 0, M = mimS(), [tn, tc] = mimTier(my + (M.pend || 0)), n = Object.keys(st.con).length;
  const sup = `<h3>Hive Suppression · the whole server</h3><div class="mimsup"><div class="mimbar big"><i style="width:${pct * 100}%"></i></div><b>${Math.round(pct * 100)}%</b></div>
    <p class="note">${fmt(st.sup)} points from ${fmt(n)} commander${n === 1 ? "" : "s"}. At the finale this cuts Omega's starting shields by ${fx.sh}%, its regeneration by ${fx.rg}% and its swarm by ${fx.sw}%.</p>
    <div class="mimme"><span style="color:${tc}">◆ ${tn}</span><small>Your contribution: ${fmt(my)}${M.pend ? ` (+${M.pend} sending)` : ""} · today ${Math.min(MIM_DAYCAP, ((st.cday[G.me] || [])[0] === Math.floor(T / 864e5) ? st.cday[G.me][1] : 0))}/${MIM_DAYCAP}. Ranks: Scout 10, Warden 60, Vanguard 200.</small></div>`;
  if (w < 2 || w > 4) return sup + (w === 1 ? `<p class="note">The Alphas rise in week 2.</p>` : "");
  const rows = [0, 1, 2, 3].map(i => { const A = st.a["ma" + i], X = st.x["mx" + i]; return `<div class="mimal"><div><b style="color:${MON["alpha" + (i + 1)].col}">Alpha Sovereign ${MIM_AN[i]}</b><small>${A.dead ? "Slain this week" : `${A.hp}/100 sections · ${X.open ? `<span style="color:var(--green)">Nexus broken</span>` : `Nexus ${X.anc.filter(v => v > 0).length}/4 anchors`}`}</small><div class="mimbar"><i style="width:${A.dead ? 0 : A.hp}%"></i></div></div>
    <div class="mimalb">${A.dead ? "" : `<button class="btn" data-act="mimGoB" data-id="ma${i}">Alpha</button>`}<button class="btn" data-act="mimGoB" data-id="mx${i}">Nexus</button></div></div>`; }).join("");
  return sup + `<h3>The Alphas</h3>${rows}`; }
