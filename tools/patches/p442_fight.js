/* v442 THE OMEGA CUBE FIGHT. After the Last Stand the Omega Cube stays over the Void for 36 hours, and every commander can attack it.
   Its hull is 100 sections, one per Assimilation Cube in it: every section a fleet destroys breaks that cube off the machine (it goes
   dark and drifts away, for everyone to see), the topmost first. If the galaxy brings it down, it shatters; if the 36 hours run out
   first, it comes apart on its own and the cubes go home. Shared record: event/omega {cyc, hp, dmg, log, dead, last}, written under
   the doc lock like the world bosses. A fleet takes a share of its hull that rises with the fleet (8% to 20% for the largest). */
const OM_SEG = 100, OM_FIGHT = 36 * DV_H, OM_HP = 1200000, OM_ATK = 520000;
{ const hull = Math.round(OM_HP * WB_K / OM_SEG); AL.wbOmg = { n: "Omega Cube section", atk: Math.round(OM_ATK / OM_SEG), sh: Math.round(hull * .05), hull, val: hull * 2 }; }
const OMO = { id: "omega", kind: "omega", lvl: 30, name: "Omega Cube", mv: (T, out) => { const o = out || {}; o.x = 0; o.y = DV_Y; o.z = 0; return o; }, r: .01, a0: 0 };
G.om = null; let OMN = null, OMN_SRC = undefined;
function omNorm(d, s0) { const o = d && typeof d === "object" && d.cyc === s0 ? d : { cyc: s0 }; o.hp = o.hp == null ? OM_SEG : clamp(Math.round(+o.hp || 0), 0, OM_SEG);
  o.dmg = o.dmg && typeof o.dmg === "object" ? o.dmg : {}; o.log = Array.isArray(o.log) ? o.log.filter(x => Array.isArray(x) && x.length === 2).slice(-150) : []; o.dead = +o.dead || 0; o.last = o.last || null; return o; }
function omState(s0) { const src = G.mode === "online" ? G.om : ((S && S.ldb) || {})["event/omega"] || null; if (!OMN || OMN.cyc !== s0 || OMN_SRC !== src) { OMN = omNorm(src ? jcopy(src) : null, s0); OMN_SRC = src; } return OMN; }
/* when the Omega Cube comes apart (event time): 3 minutes after it falls, or when its 36 hours run out; the preview has it fall at 36 min */
function omRB(s0) { if (G.dvSim) return DV.fight0 + 39 * DV_M; const st = omState(s0); return st.dead && st.dead > s0 ? st.dead - s0 + 3 * DV_M : DV.fight0 + OM_FIGHT; }
const omHp = D => D.sim ? Math.round(OM_SEG * (1 - clamp((D.e - DV.fight0) / (36 * DV_M), 0, 1))) : omState(D.s0).hp;
/* when a section broke off: the r-th from the top goes when the r-th section of hull is destroyed */
function dvBrk(c, D, N) { const r = N - 1 - c.i2; if (D.sim) return DV.fight0 + (r + 1) / OM_SEG * 36 * DV_M; const st = omState(D.s0); for (const [at, left] of st.log) if (OM_SEG - left > r) return at - D.s0; return Infinity; }
function omOn(T = now()) { if (G.dvSim || T < DV_FIRST) return false; const s0 = dvStartOf(T), e = T - s0; return e >= DV.fight0 && e < omRB(s0) && omState(s0).hp > 0; }
function omFightRise(mkA, mkD, n0) { let { F, x } = wbRiseK(mkA(), mkD()); if (F <= 1) return { res: simulate(mkA(), mkD()), rise: 1 };
  const tgt = Math.min(n0, Math.max(1, Math.round(OM_SEG * clamp(.08 + .04 * Math.log10(x), .08, .2)))); let lo = 1, hi = 0, best = null;
  for (let i = 0; i < 9; i++) { const A = mkA(), D = mkD(); for (const s of D) { s.atk *= F; s.hull *= F; } const res = simulate(A, D), seg = n0 - clamp(Math.round(((res.dLeft || {}).wbOmg) || 0), 0, n0), err = Math.abs(seg - tgt);
    if (!best || err < best.err) best = { res, F, err }; if (err <= 2) break; if (seg > tgt) lo = F; else hi = F; F = hi ? Math.sqrt(Math.max(lo, 1) * hi) : F * Math.max(1.5, Math.pow(seg / Math.max(1, tgt), 1.6)); if (hi && hi / Math.max(lo, 1) < 1.03) break; }
  return { res: best.res, rise: best.F }; }
async function omResolve(f) {
  G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(x => x !== f); };
  try {
    const at = f.arrive, s0 = dvStartOf(at), e = at - s0; if (at < DV_FIRST || e < DV.fight0 || e >= omRB(s0)) { note("The Omega Cube was gone when our fleet arrived. Returning.", "warn"); return home(); }
    const ref = adb().doc("event/omega"); for (let i = 0; i < 8; i++) { const r = await ref.acquire({ holder: G.me, ttlMs: 15000 }); if (r.acquired) break; await sleep(1500); }
    const snap = await ref.get(), cur = omNorm(snap.exists ? snap.data() : null, s0), n0 = cur.hp;
    if (!n0) { note("The Omega Cube had already fallen when our fleet arrived. Returning.", "warn"); return home(); }
    const mine0 = Object.assign({}, f.n), { res, rise } = omFightRise(() => stacksOf(f.n, techOf(null), G.me), () => stacksOf({ wbOmg: n0 }, { wbSh: 1 }, "wboss"), n0);
    const left = clamp(Math.round(((res.dLeft || {}).wbOmg) || 0), 0, n0), seg = n0 - left;
    cur.hp = left; if (seg) { cur.dmg[G.me] = (cur.dmg[G.me] || 0) + seg; cur.log.push([at, left]); } if (!left) { cur.dead = at; cur.last = G.me; }
    await ref.set(cur); if (G.mode === "online") G.om = cur; OMN = null;
    const rep = mkRep({ at, kind: "attack", title: "Assault on the Omega Cube", aUids: [G.me], aName: S.homeName + " Fleet", dName: "Omega Cube", omega: 1, omSeg: [n0, left], omRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, lvl: 30, ptype: "gas", fortL: 0, alien: true,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));
    if (seg) { const L = { m: 40000 * seg, c: 26000 * seg, g: 12000 * seg }, ratio = Math.min(1, cargoOf(f.n) / Math.max(1, total(L)));
      rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot; const sh = 3 * seg; S.shards = (S.shards || 0) + sh; rep.shards = sh; evPts("hunt", seg * 60); S.wins++;
      logReward("Omega Cube bounty", rep.loot, { shards: sh, kind: "battle" }); rep.mats = fsDrop(lootRoll([["cube", 5, 1 + Math.floor(seg / 3)], ["void", 5, 1 + Math.floor(seg / 5)]]), "the Omega Cube", { nocap: 1 }); }
    if (rise > 1.01) note(`The Omega Cube rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (!left) { bump("bosses"); note("We brought down the Omega Cube! It is shattering. Everyone who fought it can claim the spoils.", "win"); }
    else note(seg ? `Our fleet broke ${seg} section${seg > 1 ? "s" : ""} off the Omega Cube (${left} of ${OM_SEG} left)${rep.loot ? `. Bounty: ${fmt(rep.loot.m)} metal, ${fmt(rep.loot.c)} crystal, ${fmt(rep.loot.g)} gas, plus ◆${rep.shards}` : ""}.` : "The Omega Cube shrugged off our attack.", seg ? "win" : "loss");
    addReport(rep); omClaim(); home();
  } catch (e) { note("Lost contact with the Omega Cube fight. Fleet returning.", "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* it fell: everyone who broke a section claims once: shards by share, Omega Core Fragments (more for the top ten, the top damage and the
   final blow), an item, and a Teleport Ticket for the top damage */
function omClaim() { if (!S || !G.ready || G.dvSim) return; const T = now(); if (T < DV_FIRST) return; const s0 = dvStartOf(T), st = omState(s0), my = st.dmg[G.me] || 0;
  if (st.hp > 0 || !my || S.omGot === s0) return; S.omGot = s0; const rank = Object.entries(st.dmg).sort((a, b) => b[1] - a[1]).map(x => x[0]), tot = Object.values(st.dmg).reduce((a, b) => a + b, 0) || 1, share = my / tot, i = rank.indexOf(G.me);
  const sh = 20 + Math.round(160 * Math.min(1, share * 4)), frag = 1 + (i < 10 ? 1 : 0) + (i === 0 ? 1 : 0) + (st.last === G.me ? 1 : 0), it = DROPS[(Math.random() * DROPS.length) | 0];
  S.shards = (S.shards || 0) + sh; S.omegaFrag = (S.omegaFrag || 0) + frag; giveItem(it); if (i === 0) giveItem("teleport");
  logReward("Omega Cube destroyed", null, { shards: sh, item: it, kind: "battle" });
  note(`The Omega Cube is destroyed! Your share: ◆${sh}, ${frag} Omega Core Fragment${frag > 1 ? "s" : ""}, ${SHOP[it].n}${i === 0 ? " and a Teleport Ticket for top damage" : ""}.`, "win"); dirty(); }
/* the attack panel */
function shOmega() { const T = now(); if (T < DV_FIRST && !G.dvSim) return `<div class="hd"><h2>The Omega Cube</h2></div><p class="note">It has not formed yet.</p>`;
  const s0 = dvStartOf(T), st = omState(s0), hp = st.hp, pc = Math.round(hp / OM_SEG * 100), end = s0 + omRB(s0), on = omOn(T), my = st.dmg[G.me] || 0, h = originPlanet(), avail = originAvail(), sel = selected(), sent = S.fleets.some(f => f.om && f.phase === "out");
  const lead = Object.entries(st.dmg).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([u, v], i) => `<li><span>${i + 1}. ${esc(u === G.me ? "You" : nameOf(u))}</span><b>${v} section${v > 1 ? "s" : ""}</b></li>`).join("");
  let body = ""; if (!on) body = `<p class="note">${hp ? "The Omega Cube is not open to attack right now." : "Destroyed. Its cubes are scattering across the galaxy."}</p>`;
  else if (!canPlay()) body = `<p class="note">${G.mode === "connecting" ? connNote() : "You can only watch this galaxy."}</p>`;
  else if (sent) body = `<p class="note">Our fleet is on its way.</p>`;
  else if (!Object.keys(avail).length) body = `${originBar()}<p class="note">No ships at ${esc(h ? h.name : S.homeName)}.</p>`;
  else body = `<h2 class="sec">Attack</h2>${originBar()}${picker(avail)}${speedBar(OMO, sel)}<button class="btn wide amber" data-act="omGo" ${Object.keys(sel).length && !slotsFull() ? "" : "disabled"}>⚔ Attack the Omega Cube</button>`;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">${on ? "● LIVE · " : ""}Cube Devastation</div><h2>The Omega Cube</h2><p class="note">A hundred Assimilation Cubes locked round the Super Cube. Every section our fleets destroy breaks a cube off the machine. Bring it down before it disperses.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="wbhp"><div class="wbbar"><i style="width:${pc}%;background:#5dff6a"></i></div><span>${hp ? `${hp} of ${OM_SEG} sections · ${pc}%` : "Destroyed"}</span></div>
    <dl class="kv"><dt>Bounty per section</dt><dd>${costHTML({ m: 40000, c: 26000, g: 12000 })} + ◆3</dd><dt>Your sections</dt><dd>${my || "None yet"}</dd><dt>${on ? "Disperses in" : "Status"}</dt><dd>${on ? `<b data-end="${end}">${ftime(end - T)}</b>` : hp ? "Not attackable" : "Fallen"}</dd><dt>When it falls</dt><dd>◆ shards by share, Omega Core Fragments, an item; the top damage a Teleport Ticket</dd></dl>
    ${lead ? `<h2 class="sec">Top damage</h2><ol class="wblead">${lead}</ol>` : ""}${body}`; }
/* the band over the map while it can be fought */
function omBand() { const on = omOn(), b = $("#omband"); if (!on || view !== "galaxy") { if (b) b.remove(); return; } const st = omState(dvStartOf(now()));
  const html = `<button class="omb" data-act="omOpen"><b>Ω OMEGA CUBE</b><span>${st.hp} of ${OM_SEG} sections</span><i>⚔ Attack</i></button>`;
  if (!b) { const e = document.createElement("div"); e.id = "omband"; e.innerHTML = html; $("#app").appendChild(e); } else if (b.dataset.h !== html) { b.dataset.h = html; b.innerHTML = html; } }
setInterval(() => { try { omBand(); omClaim(); } catch (e) {} }, 1000);
