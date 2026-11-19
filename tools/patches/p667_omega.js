/* ---------- v667 Omega: The Convergence (the Mimic Protocol's live finale) ----------
   The last weekend of every Mimic run (day 26 to the end of day 28, Saturday and Sunday UTC): Omega, the First Mimic, comes through a
   dimensional rift beside its central Neural Nexus. One shared fight for the whole server, kept in the same record (event/mimic, field o):
   300 sections in three phases fixed by what is left (deterministic, never bouncing back across a boundary):
     Phase 1 · The Swarm (300-201): three Neural Nodes feed its regeneration (10 sections an hour at full, less per node broken).
     Phase 2 · Assimilation (200-101): four Assimilation Pylons. While any stands it keeps only half the damage, and it adapts to the
               ship class that hit it hardest last (that class fires at 40% against it) and fields Echoes of it.
     Phase 3 · Omega Unbound (100-0): the core is exposed (x1.5 damage) and the final countdown runs: 6 hours, then it escapes.
   Shields first: it arrives with up to 60 shield sections, fewer the more Hive Suppression the server earned (and its regeneration and
   swarm are cut by the same meter). The central Neural Nexus (4 anchors of 30): break it and Omega is cut off from its Alphas for 30
   minutes: no regeneration, no adaptation, double damage. Small fleets help by clearing its swarm (each clear slows its regeneration),
   or breaking nodes, pylons and anchors, which are far weaker than its body. Every commander who took part claims once at the end, by
   outcome (Omega slain / it escaped in phase 3 / it escaped earlier) and by participation, not just damage. */
const MO_D0 = 26 * 864e5, MO_D1 = 28 * 864e5, MO_HP = 300, MO_P3 = 6 * 3600e3, MO_NODE = 20, MO_PYL = 20, MO_ANC = 30;
Object.assign(MIM_U, { momega: 1, momegax: 1, mnode: 1, mpylon: 1 });
MON.omega = { n: "Omega, the First Mimic", sp: "Omega", ic: "⬢", col: "#bff6ff", rgb: "191,246,255", per: 99, d: "The hive consciousness of the Mimic Protocol. It commands every Alpha and every hive, adapts to whatever hurts it, and grows stronger for every hive the galaxy left alive.", names: ["Omega"] };
const MIM_OM = [{ id: "mo", kind: "pirate", mon: "omega", u: "momega", om: 1, name: "Omega, the First Mimic" }, { id: "mxo", kind: "pirate", mon: "nexus", u: "mnexus", om: 2, name: "The Central Neural Nexus" }];
(() => { const lo = Math.max(LAYERS[LAYERS.length - 1].r0, 18 * SC) + 6, hi = LAYERS[0].r1 - 6, rad = Math.sqrt(lo * lo + .2 * (hi * hi - lo * lo)), lvl = (layerOf(rad).n - 1) * 5 + 8;
  MIM_OM[0].r = +rad.toFixed(2); MIM_OM[0].a0 = Math.PI; MIM_OM[0].lvl = lvl; MIM_OM[1].r = +(rad * .9).toFixed(2); MIM_OM[1].a0 = Math.PI + .06; MIM_OM[1].lvl = lvl;
  for (const x of MIM_OM) MIM_BOSS[x.id] = x; })();
const moWin = T => { const e = mimClock(T).e; return e >= MO_D0 && e < MO_D1; };
const moStart = () => mimT0() + MO_D0;
const moPh = hp => hp > 200 ? 1 : hp > 100 ? 2 : 3;
const MO_PHN = ["", "The Swarm", "Assimilation", "Omega Unbound"];
function moNorm(st, T) { const s0 = moStart(); let o = st.o; const fx = mimSupFx(mimSupPct(st));
  if (!o || o.s !== s0) o = st.o = { s: s0, hp: MO_HP, sh0: Math.round(60 * (1 - fx.sh / 100)), shd: Math.round(60 * (1 - fx.sh / 100)), nodes: [MO_NODE, MO_NODE, MO_NODE], pyl: [MO_PYL, MO_PYL, MO_PYL, MO_PYL], nx: { anc: [MO_ANC, MO_ANC, MO_ANC, MO_ANC], open: 0 }, swarm: 0, dmg: {}, hits: {}, adapt: "", t: T, dead: 0, last: "", p3: 0, end: "" };
  if (o.nx.open && T >= o.nx.open) { o.nx = { anc: [MO_ANC, MO_ANC, MO_ANC, MO_ANC], open: 0 }; }
  const ph = moPh(o.hp); if (!o.dead && !o.end && ph < 3 && !o.nx.open && T > o.t) { const nodes = o.nodes.filter(v => v > 0).length, rate = 10 * (1 - fx.rg / 100) * Math.max(.3, 1 - o.swarm / 150) * (ph === 1 ? nodes / 3 : .5), add = Math.floor((T - o.t) / 3600e3 * rate);
    if (add > 0) { o.hp = Math.min(ph === 1 ? MO_HP : 200, o.hp + add); o.t = T; } } else o.t = T;
  if (!o.dead && !o.end) { const e = mimClock(T).e; if (o.p3 && T > o.p3 + MO_P3) o.end = "p3"; else if (e >= MO_D1) o.end = ph === 3 ? "p3" : "early"; }
  return o; }
const moSt = T => { const st = mimStC(T); return { st, o: moNorm(st, T) }; };
const moOutcome = o => o.dead ? "win" : o.end === "p3" ? "part" : o.end ? "fail" : "";
function moMods(o, T) { const ph = moPh(o.hp), cut = !!o.nx.open, pylUp = ph === 2 && o.pyl.some(v => v > 0) && !cut; return { ph, cut, pylUp, mul: (ph === 3 ? 1.5 : 1) * (pylUp ? .5 : 1) * (cut ? 2 : 1), adapt: pylUp && o.adapt ? o.adapt : "" }; }
function moTargets(o) { const ph = moPh(o.hp), t = [["core", o.shd > 0 ? "Its shield" : ph === 3 ? "The exposed core" : "Omega's body", null]];
  if (ph === 1) o.nodes.forEach((v, i) => v > 0 && t.push(["node" + i, `Neural Node ${i + 1}`, v]));
  if (ph === 2) o.pyl.forEach((v, i) => v > 0 && t.push(["pyl" + i, `Assimilation Pylon ${i + 1}`, v]));
  t.push(["swarm", "Clear the swarm (small fleets)", null]); return t; }
async function moResolve(f) { const B = MIM_BOSS[f.xid], x = PB[f.xid]; G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(q => q !== f); };
  try { const at = f.arrive; if (!moWin(at)) { note(`${B.name} was not there when our fleet arrived. Returning.`, "warn"); return home(); }
    const ref = adb().doc(mimDoc()); for (let i = 0; i < 8; i++) { const r = ref.acquire ? await ref.acquire({ holder: G.me, ttlMs: 15000 }) : { acquired: 1 }; if (r.acquired) break; await sleep(1500); }
    const snap = await casGet(ref), cur = mimNorm(snap.exists ? snap.data() : null, at), o = moNorm(cur, at);
    if (o.dead || o.end) { note(`The fight with Omega is over. Fleet returning.`, "warn"); return home(); }
    const M0 = moMods(o, at), nx = B.om === 2; let tgt = nx ? "nx" : f.omT || "core"; if (!nx && !moTargets(o).some(t => t[0] === tgt)) tgt = "core";
    if (nx && o.nx.open) { note(`The Central Nexus is already broken. It reconnects in ${ftime(o.nx.open - at)}. Fleet returning.`, "warn"); return home(); }
    const sw = 1 - mimSupFx(mimSupPct(cur)).sw / 100, lvl = B.lvl; let u, n0, esc;
    if (tgt === "core") { u = M0.ph === 3 ? "momegax" : "momega"; n0 = Math.max(1, o.shd > 0 ? o.shd : o.hp - (M0.ph === 1 ? 200 : M0.ph === 2 ? 100 : 0)); esc = { mstalk: Math.round(6 * sw), mhunt: Math.round(3 * sw) }; if (M0.ph === 1 && Math.floor(at / 3600e3) % 3 === 0) esc.malpha1 = 1; if (M0.adapt) esc["e_" + M0.adapt] = 2; }
    else if (/^node/.test(tgt)) { u = "mnode"; n0 = o.nodes[+tgt.slice(4)]; esc = { mstalk: 3 }; } else if (/^pyl/.test(tgt)) { u = "mpylon"; n0 = o.pyl[+tgt.slice(3)]; esc = { mguard: 2 }; }
    else if (tgt === "nx") { u = "mnexus"; const ai = o.nx.anc.findIndex(v => v > 0); n0 = o.nx.anc[ai]; esc = { mguard: 2, mharv: 2 }; }
    else { u = "mstalk"; n0 = 0; esc = { mstalk: Math.max(3, Math.round(6 * sw)), mhunt: Math.round(2 * sw), mharv: 1 }; }
    const mine0 = Object.assign({}, f.n), mkA = () => { const st = stacksOf(f.n, techVs(x), G.me); if (M0.adapt) for (const s of st) if (s.k === M0.adapt) s.atk *= .4; return st; };
    const mkD = () => stacksOf(Object.assign(n0 ? { [u]: n0 } : {}, esc), { mon: tgt === "swarm" ? Math.max(1, Math.round(lvl / 4)) : lvl }, "monster");
    const { res, rise } = n0 ? mimRise(mkA, mkD, u, n0, n0) : { res: simulate(mkA(), mkD()), rise: 1 };
    const left = n0 ? clamp(Math.round(((res.dLeft || {})[u]) || 0), 0, n0) : 0, raw = n0 - left; let seg = 0, pts = 0, msg = "";
    if (tgt === "swarm") { if (res.winner === "a") { o.swarm++; pts = 2; msg = `Our fleet cleared a wave of Omega's swarm (${o.swarm} cleared): its regeneration slows.`; } else msg = "The swarm held. Bring a few more warships."; }
    else if (raw) { seg = tgt === "core" ? Math.min(n0, Math.max(1, Math.round(raw * M0.mul))) : raw;
      if (tgt === "core") { if (o.shd > 0) { o.shd = Math.max(0, o.shd - seg); msg = o.shd ? `Our fleet stripped ${seg} shield section${seg > 1 ? "s" : ""} off Omega (${o.shd} left).` : "Omega's shield is down! Its body is open to every fleet."; }
        else { const ph0 = moPh(o.hp); o.hp = Math.max(0, o.hp - seg); const ph1 = moPh(o.hp); if (ph1 === 3 && !o.p3) o.p3 = at; if (!o.hp) { o.dead = at; o.last = G.me; }
          msg = o.dead ? "We brought down Omega, the First Mimic!" : ph1 > ph0 ? `Omega is breaking: phase ${ph1}, ${MO_PHN[ph1]}!${ph1 === 3 ? " Its core is exposed and the final countdown has begun: 6 hours." : " Its Assimilation Pylons are rising."}` : `Our fleet broke ${seg} section${seg > 1 ? "s" : ""} off Omega (${o.hp} of ${MO_HP} left).`; }
        pts = 4 * seg;
        { let best = "", bv = 0; for (const k in mine0) { const v = (mine0[k] || 0) * ((SH[k] || {}).atk || 0); if (ECHO_BASE.includes(k) && v > bv) { bv = v; best = k; } } if (best && moPh(o.hp) === 2) o.adapt = best; } }
      else if (/^node/.test(tgt)) { const i = +tgt.slice(4); o.nodes[i] -= seg; pts = 3 * seg; msg = o.nodes[i] <= 0 ? `Neural Node ${i + 1} is destroyed! Omega's regeneration weakens.` : `Neural Node ${i + 1}: ${o.nodes[i]} of ${MO_NODE} left.`; }
      else if (/^pyl/.test(tgt)) { const i = +tgt.slice(3); o.pyl[i] -= seg; pts = 3 * seg; msg = o.pyl[i] <= 0 ? `Assimilation Pylon ${i + 1} is down!${o.pyl.every(v => v <= 0) ? " Omega can no longer adapt: its body takes full damage." : ""}` : `Assimilation Pylon ${i + 1}: ${o.pyl[i]} of ${MO_PYL} left.`; }
      else { const ai = o.nx.anc.findIndex(v => v > 0); o.nx.anc[ai] -= seg; pts = 3 * seg; if (o.nx.anc.every(v => v <= 0)) { o.nx.open = at + MIM_OPEN; msg = "The Central Neural Nexus collapsed! Omega is cut off from its Alphas for 30 minutes: no healing, no adapting, double damage. Everyone, strike now!"; } else msg = `Anchor ${ai + 1} of the Central Nexus: ${Math.max(0, o.nx.anc[ai])} of ${MO_ANC} left.`; }
      if (seg) o.dmg[G.me] = (o.dmg[G.me] || 0) + Math.min(100, seg); }
    else msg = `Our fleet couldn't break a section off ${tgt === "core" ? "Omega" : "its target"}. Send more firepower${M0.adapt ? `, and not ${SH[M0.adapt].n}s: Omega has adapted to them` : ""}.`;
    o.hits[G.me] = (o.hits[G.me] || 0) + 1; const counted = pts ? mimCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; mimLocal(cur);
    const rep = mkRep({ at, kind: "attack", simLeft: left, title: `Omega: The Convergence · ${{ core: "Omega", swarm: "the swarm", nx: "the Central Nexus" }[tgt] || (/^node/.test(tgt) ? `Neural Node ${+tgt.slice(4) + 1}` : `Assimilation Pylon ${+tgt.slice(3) + 1}`)}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: B.name, mimB: B.id, omegaM: 1, omRise: rise > 1.01 ? Math.round(rise) : undefined,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1);
    if (seg || pts) { const k = Math.max(1, seg), L = { m: 30000 * k, c: 20000 * k, g: 10000 * k }, ratio = Math.min(1, fCargo(f) / Math.max(1, total(L))); rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = 2 * k; S.shards = (S.shards || 0) + sh; rep.shards = sh; S.wins++; evPts("hunt", k * 50); const M = mimS(); M.m.ncf = (M.m.ncf || 0) + k; M.pts += counted; logReward("Omega: The Convergence", rep.loot, { shards: sh, kind: "battle" }); }
    note(msg + (counted ? ` +${counted} Hive Suppression.` : ""), seg || pts ? "win" : "warn"); if (rise > 1.01) note(`Omega rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} moClaimM(); moCineCheck(); home();
  } catch (e) { if (e === CAS_RETRY && await casAgain(f, moResolve)) return; note(`Lost contact with the Omega fight. Fleet returning.`, "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* participation, not just damage: everyone who attacked at least once is a Participant; 5+ sections or 4+ attacks a Contender; 20+
   sections or a top-ten damage share a Champion; the season rank (Scout/Warden/Vanguard) adds a bonus Omega Core Shard each */
function moPart(o, uid) { const d = o.dmg[uid] || 0, h = o.hits[uid] || 0; if (!h) return 0; const top = Object.entries(o.dmg).sort((a, b) => b[1] - a[1]).slice(0, 10).some(([u]) => u === uid); return d >= 20 || top ? 3 : d >= 5 || h >= 4 ? 2 : 1; }
const MO_PART = ["", "Participant", "Contender", "Champion"];
function moClaimM() { if (!S || !G.ready) return; const T = now(), { st, o } = moSt(T), out = moOutcome(o), M = mimS(); if (!out) return; const id = "om" + o.s; M.got = M.got || {}; if (M.got[id]) return;
  const p = moPart(o, G.me), rk = mimTier(st.con[G.me] || 0)[0], rb = { Vanguard: 3, Warden: 2, Scout: 1 }[rk] || 0; M.got[id] = 1; M.moEnd = { s: o.s, out, seen: 0 }; dirty();
  if (!p && !rb) return; const base = out === "win" ? [0, 3, 6, 10] : out === "part" ? [0, 2, 3, 5] : [0, 1, 1, 2], osh = (p ? base[p] : 0) + (p ? rb : Math.min(1, rb)), sh = (out === "win" ? 30 : out === "part" ? 15 : 8) * Math.max(1, p);
  M.m.osh = (M.m.osh || 0) + osh; S.shards = (S.shards || 0) + sh; logReward(`Omega: The Convergence · ${out === "win" ? "victory" : out === "part" ? "it escaped, wounded" : "it escaped"}`, null, { shards: sh, kind: "event" });
  note(`Omega: The Convergence is over (${out === "win" ? "Omega is dead" : out === "part" ? "it escaped in its final phase" : "it escaped"}). As a ${p ? MO_PART[p] : "season " + rk}: ${osh} Omega Core Shard${osh === 1 ? "" : "s"} and ◆${sh}.`, "win"); }
/* the cinematics: the arrival (once, when you first see the event live), each phase change, and the final transmission at the end. The
   owner's paintings, slow push-ins, lines that set each beat, a sting. Tap to skip; replayable from the hub. */
const MO_CINE = { arr: [["art/mimic/hive.webp", "The surviving hives wake at once.", "Every Alpha hive left alive sends its neural energy toward one point in the dark."], ["art/mimic/nexus.webp", "The Central Nexus ignites.", "A dimensional rift opens over the old vault."], ["art/mimic/stalker.webp", "Something reaches through.", "Tendrils first. Then the claws."], ["art/mimic/titan.webp", "OMEGA", "The First Mimic. Every fleet in the galaxy is needed now."]],
  p2: [["art/mimic/titan.webp", "Phase 2 · Assimilation", "Omega's armour shifts to whatever hurts it. Break the Assimilation Pylons, and bring every kind of ship."]],
  p3: [["art/mimic/nexus.webp", "Phase 3 · Omega Unbound", "Its core is exposed and it is drawing in everything it has. Six hours, Commander. Then it's gone."]] };
function moCine(key, done) { const L = MO_CINE[key]; if (!L || document.getElementById("omcine")) return; const w = document.createElement("div"); w.id = "omcine"; document.body.appendChild(w); let i = 0, tm = 0;
  const show = () => { if (i >= L.length) { w.classList.add("out"); setTimeout(() => { w.remove(); done && done(); }, 600); return; } const [img, t, s] = L[i];
    w.innerHTML = `<div class="omcimg" style="background-image:url(${img})"></div><div class="omcrift"></div><div class="omctx${t === "OMEGA" ? " big" : ""}"><b>${esc(t)}</b><span>${esc(s)}</span></div><small>Tap to continue</small>`; try { (t === "OMEGA" ? SFX.megaBeam : i ? SFX.charge : SFX.alarm)(); } catch (e) {} i++; clearTimeout(tm); tm = setTimeout(show, t === "OMEGA" ? 5200 : 4200); };
  w.addEventListener("click", () => { clearTimeout(tm); show(); }); show(); }
function moFinal() { if (document.getElementById("omcine")) return; const T = now(), { o } = moSt(T), out = moOutcome(o), w = document.createElement("div"); w.id = "omcine"; w.className = "fin"; document.body.appendChild(w);
  const head = out === "win" ? "Omega is dead." : "Omega withdrew into the dark.";
  w.innerHTML = `<div class="omcimg" style="background-image:url(art/mimic/nexus.webp)"></div><div class="omctx tx"><small>INTERCEPTED TRANSMISSION</small><b class="q"></b><span class="after">${esc(head)} But as its body failed, a fragment of its consciousness escaped into the ancient Cube network.</span></div><small>Tap to close</small>`;
  const q = "“I did not create the swarm. I was created to survive what is coming.”", el = w.querySelector(".q"); let n = 0; const tick = () => { if (!document.body.contains(w)) return; el.textContent = q.slice(0, ++n); if (n < q.length) setTimeout(tick, 45); else w.classList.add("done"); };
  try { SFX.gong(); } catch (e) {} setTimeout(tick, 900); w.addEventListener("click", () => { if (n < q.length) { n = q.length - 1; } else { w.classList.add("out"); setTimeout(() => w.remove(), 600); } }); }
function moCineCheck() { if (!S || !G.ready || G.cineOn || battle || document.getElementById("omcine")) return; const T = now(); if (!moWin(T) && !(S.mim && S.mim.moEnd && !S.mim.moEnd.seen)) return; const M = mimS(), { o } = moSt(T), k = "c" + o.s; M.cine = M.cine || {};
  if (M.moEnd && !M.moEnd.seen) { M.moEnd.seen = 1; dirty(); return moFinal(); }
  if (!M.cine[k + "a"]) { M.cine[k + "a"] = 1; dirty(); return moCine("arr"); }
  const ph = moPh(o.hp); if (ph >= 2 && !M.cine[k + "2"]) { M.cine[k + "2"] = 1; dirty(); return moCine("p2"); } if (ph >= 3 && !M.cine[k + "3"]) { M.cine[k + "3"] = 1; dirty(); return moCine("p3"); } }
function moInfo(x, T) { const { st, o } = moSt(T), M0 = moMods(o, T), out = moOutcome(o), fx = mimSupFx(mimSupPct(st)), B = MIM_BOSS[x.id];
  const bar = (v, mx, col) => `<div class="mimbar"><i style="width:${Math.max(0, v) / mx * 100}%;background:${col}"></i></div>`;
  if (B.om === 2) return `<div class="mimboss"><b>${o.nx.open ? `Collapsed · Omega cut off for <span data-end="${o.nx.open}">${ftime(o.nx.open - T)}</span>` : `Anchors ${o.nx.anc.filter(v => v > 0).length} of 4 standing`}</b>${o.nx.anc.map((v, i) => `<div class="mimanc"><span>Anchor ${i + 1}</span>${bar(v, MO_ANC, "linear-gradient(90deg,#2fa8ff,#9ff0ff)")}<small>${Math.max(0, v)}/${MO_ANC}</small></div>`).join("")}
    <p class="note">Break all four anchors and Omega is cut off from its Alphas for 30 minutes: no healing, no adapting, double damage. Then the network reconnects.</p></div>`;
  if (out) return `<div class="mimboss"><b>${out === "win" ? "Omega is dead." : out === "part" ? "Omega escaped in its final phase." : "Omega escaped."}</b><p class="note">Everyone who took part has claimed their share.</p><button class="btn wide" data-act="moFinal">Replay the final transmission</button></div>`;
  const tg = moTargets(o), cur = (S.moTgt && tg.some(t => t[0] === S.moTgt)) ? S.moTgt : "core";
  return `<div class="mimboss om"><b>Phase ${M0.ph} · ${MO_PHN[M0.ph]}</b>${o.shd > 0 ? `<small>Shield ${o.shd}/${o.sh0} (Hive Suppression cut it by ${fx.sh}%)</small>${bar(o.shd, 60, "linear-gradient(90deg,#9ff0ff,#fff)")}` : ""}<small>${o.hp} of ${MO_HP} sections</small>${bar(o.hp, MO_HP, "linear-gradient(90deg,#7a3cff,#5fd8ff,#e8fbff)")}
    <dl class="kv">${M0.ph === 1 ? `<dt>Neural Nodes</dt><dd>${o.nodes.filter(v => v > 0).length} of 3 feeding its regeneration</dd>` : ""}${M0.ph === 2 ? `<dt>Assimilation Pylons</dt><dd>${o.pyl.filter(v => v > 0).length} of 4 standing${M0.pylUp ? " · it keeps half the damage" : ""}</dd>${M0.adapt ? `<dt>Adapted to</dt><dd style="color:var(--amber)">${SH[M0.adapt].n}s (40% firepower against it)</dd>` : ""}` : ""}
    ${M0.ph === 3 ? `<dt>Final countdown</dt><dd style="color:var(--red)"><span data-end="${o.p3 + MO_P3}">${ftime(o.p3 + MO_P3 - T)}</span> until it escapes</dd>` : ""}<dt>Central Nexus</dt><dd>${o.nx.open ? `<span style="color:var(--green)">Broken: Omega cut off, double damage</span>` : `${o.nx.anc.filter(v => v > 0).length}/4 anchors`}</dd><dt>Swarm cleared</dt><dd>${o.swarm}</dd>
    <dt>Ends</dt><dd><span data-end="${T + MO_D1 - mimClock(T).e}">${ftime(MO_D1 - mimClock(T).e)}</span></dd><dt>You</dt><dd>${o.dmg[G.me] || 0} sections · ${o.hits[G.me] || 0} attacks · ${MO_PART[moPart(o, G.me)] || "not yet in the fight"}</dd></dl>
    <div class="omtg">${tg.map(t => `<button class="btn${t[0] === cur ? " pri" : ""}" data-act="moTgt" data-t="${t[0]}">${esc(t[1])}${t[2] != null ? ` · ${t[2]}` : ""}</button>`).join("")}</div>
    <button class="btn ghost wide" data-act="moCine" data-k="arr">Replay the arrival</button></div>`; }
function moHub(T, w) { const e = mimClock(T).e; if (w !== 4 && !(w === 5 && S.mim && S.mim.moEnd)) return ""; const { o } = moSt(T), out = moOutcome(o);
  if (e < MO_D0) return `<div class="omhub soon"><b>Omega: The Convergence</b><span>The final battle opens in <b data-end="${T + MO_D0 - e}">${ftime(MO_D0 - e)}</b>. Everything the server does before then weakens it.</span></div>`;
  return `<div class="omhub"><b>Omega: The Convergence${out ? "" : " · LIVE"}</b><span>${out ? (out === "win" ? "Omega is dead." : "Omega escaped.") : `Phase ${moPh(o.hp)} · ${MO_PHN[moPh(o.hp)]} · ${o.hp}/${MO_HP}`}</span><button class="btn pri" data-act="mimGoB" data-id="mo">${out ? "See the result" : "Join the fight"}</button></div>`; }
