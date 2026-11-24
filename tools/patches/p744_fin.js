/* ---------- v744 EXTINCTION PROTOCOL: the Resurrection War's live finale. The closing Saturday of the war, 6 pm Phoenix (CNT_FIN),
   an hour for everyone at once. Players don't steer ships: they send fleets at the current phase's targets, the shared record moves
   on when a phase's targets fall, and every phase has a timer so the hour always reaches an ending.
     1 The Arrival (0-5 min): a gateway opens at the heart of the galaxy and the Prime Ark comes through with its fleet.
     2 Break the Shield (to 20): three Neural Anchors hold its shield. All three down opens phase 3; none by 20 min and it withdraws.
     3 Resurrection Cascade (to 40): fabrication hangars rebuild its conduits; convoys and strike-force escorts help. Defences under
       25% (or the timer) open phase 4. Every regional Ark destroyed before the finale is one hangar fewer and a quarter fewer escorts.
     4 The Final Continuity Transfer (10 min): it sends its mind to a hidden vessel. Cut the transmitter array, then destroy the
       exposed reactor. Both: full victory. Reactor only: the war is won, the transfer completes (lower tier). Neither: it escapes.
     5 Collapse (5 min, scripted)  6 The Final Signal (5 min, scripted)
   All state is in the war record's `fin`, stamped in finale-time (ms since the finale began, so the owner's sped-up preview runs the
   same rules). Rewards pay once per run (claim key `fin`). Lore, names and Advisor lines are drafts awaiting the owner's approval. ---------- */
const CNT_PX = (() => { const R = +((LAYERS[3].r0 + LAYERS[3].r1) / 2).toFixed(2), lv = (layerOf(CNT_R()).n - 1) * 5;
  const B = { id: "kx0", kind: "pirate", mon: "cnprimem", u: "cnprime", cnt: "prime", reg: -1, name: "The Prime Resurrection Ark", hp: 1, lvl: lv + 14, r: R, a0: Math.PI, sc: 4.3, art: "c_prime" };
  B.mv = (T, out) => { const a = B.a0 + T * TAU / period(B.r), o = out || {}; o.x = Math.cos(a) * B.r; o.y = CNT_FY; o.z = Math.sin(a) * B.r; return o; }; /* it hangs above the galactic disc, clear of the planets */
  CNT_BOSS[B.id] = B; MIM_BOSS[B.id] = B; return B; })();
MON.cnprimem = { n: "The Prime Resurrection Ark", sp: "Prime Resurrection Ark", ic: "⬢", col: "#ff1830", rgb: "255,24,48", per: 99, d: "The largest machine ever built: a citadel of resurrection chambers that answers to no Ark, because every Ark answers to it.", names: ["Prime Ark"] };
CNT_M.cnprimem = "cnprime";
const CNT_FMIN = 60e3, CNT_FPH = ["", "The Arrival", "Break the Shield", "Resurrection Cascade", "The Final Continuity Transfer", "Collapse of the Ark", "The Final Signal"];
const CNT_FT = { arr: 5 * CNT_FMIN, shield: 20 * CNT_FMIN, casc: 40 * CNT_FMIN, xfer: 10 * CNT_FMIN, xcut: 6 * CNT_FMIN, coll: 5 * CNT_FMIN, sig: 5 * CNT_FMIN };
const CNT_FTRAVEL = 90e3, CNT_FY = 46; /* the battle hangs above the galactic disc, clear of the planets */ /* every fleet jumps through the staging gate: 90 s to the battle (a quarter of that in the sped-up preview) */
/* finale-time: ms since the finale began (negative before it); the owner's preview can start it now and run it faster */
function cntFinE(T) { T = T || now(); if (cntPrevOn()) { const p = S.cntPrev; if (p.s !== 7) return -1e12; return p.fin ? (T - p.fin) * (p.fs || 1) : -3600e3; } return T - (cntT0(T) + CNT_FIN); }
const cntFinSpd = () => cntPrevOn() && S.cntPrev.fin ? (S.cntPrev.fs || 1) : 1;
function cntFinInit(cur) { const n = Math.max(1, Object.keys(cur.con || {}).length), k = Math.max(.5, Math.min(3, n / 4)), dead = CNT_ARKS.filter(([id]) => cur.ark[id] && cur.ark[id].dead).length, H = Math.max(1, 4 - dead);
  const A = Math.round(18 * k), Hh = Math.round(14 * k), C = Math.round(12 * k);
  return { k: cur.k, sc: k, dead, anc: [A, A, A], anc0: A, hang: Array(H).fill(Hh), hang0: Hh, cond: [C, C, C], cond0: C, conv: 0, esc: 0, rx: Math.round(26 * k), rx0: Math.round(26 * k), tx: Math.round(16 * k), tx0: Math.round(16 * k),
    p3: 0, p4: 0, cut: 0, dead_: 0, out: "", end: 0, rg: 0, dmg: {}, hits: {}, last: "" }; }
const cntDef = o => (o.hang.reduce((a, b) => a + Math.max(0, b), 0) + o.cond.reduce((a, b) => a + Math.max(0, b), 0)) / Math.max(1, o.hang.length * o.hang0 + 3 * o.cond0);
/* the finale's record, with every timer applied (deterministic from the stored stamps, so every viewer sees the same state) */
function cntFinNorm(cur, fe) { let o = cur.fin; if (!o || o.k !== cur.k) o = cur.fin = cntFinInit(cur); o.dmg = o.dmg || {}; o.hits = o.hits || {};
  if (o.out || fe < CNT_FT.arr) return o;
  if (!o.p3) { if (fe >= CNT_FT.shield) { o.out = "fail"; o.end = CNT_FT.shield; } return o; }
  if (!o.p4) { /* the cascade: every living hangar rebuilds conduit sections, slower for every convoy intercepted */
    const t1 = Math.min(fe, CNT_FT.casc), live = o.hang.filter(v => v > 0).length, rate = live * Math.max(0, 1 - .15 * o.conv) / CNT_FMIN, t0 = Math.max(o.rg || o.p3, o.p3);
    let add = Math.floor((t1 - t0) * rate); if (add > 0) { o.rg = t0 + add / rate; while (add-- > 0) { let w = -1; o.cond.forEach((v, i) => { if (v > 0 && v < o.cond0 && (w < 0 || v < o.cond[w])) w = i; }); if (w < 0) break; o.cond[w]++; } }
    if (fe >= CNT_FT.casc) o.p4 = CNT_FT.casc; else return o; }
  if (!o.dead_ && fe >= o.p4 + CNT_FT.xfer) { o.out = "fail"; o.end = o.p4 + CNT_FT.xfer; }
  return o; }
/* which phase a moment of finale-time is in, and when that phase ends */
function cntFinPh(o, fe) { if (fe < 0) return { ph: 0, end: 0 }; if (fe < CNT_FT.arr) return { ph: 1, end: CNT_FT.arr };
  if (o.out) { const e = o.end; return fe < e + CNT_FT.coll ? { ph: 5, end: e + CNT_FT.coll } : fe < e + CNT_FT.coll + CNT_FT.sig ? { ph: 6, end: e + CNT_FT.coll + CNT_FT.sig } : { ph: 7, end: 0 }; }
  if (!o.p3) return { ph: 2, end: CNT_FT.shield }; if (!o.p4) return { ph: 3, end: CNT_FT.casc }; return { ph: 4, end: o.p4 + CNT_FT.xfer }; }
const cntXfer = (o, fe) => o.p4 && !o.cut && fe < o.p4 + CNT_FT.xcut; /* the transfer still running: the reactor stays shielded */
function cntFinSt(T) { T = T || now(); const st = cntStC(T), fe = cntFinE(T), cur = JSON.parse(JSON.stringify(st)), o = cntFinNorm(cur, fe); return { st, o, fe, P: cntFinPh(o, fe) }; }
const cntFinOn = T => cntOn(T) && cntStage(T) === 7 && cntFinE(T) >= 0 && cntFinPh(cntFinSt(T).o, cntFinE(T)).ph <= 6;
const cntFinLive = T => { if (!cntOn(T) || cntStage(T) !== 7) return false; const { P } = cntFinSt(T); return P.ph >= 2 && P.ph <= 4; };
/* what each phase can be hit with */
function cntFinTg(o, fe) { const P = cntFinPh(o, fe), t = [];
  if (P.ph === 2) o.anc.forEach((v, i) => v > 0 && t.push(["anc" + i, `Neural Anchor ${i + 1}`, v, o.anc0]));
  if (P.ph === 3) { o.hang.forEach((v, i) => v > 0 && t.push(["hang" + i, `Fabrication Hangar ${i + 1}`, v, o.hang0])); o.cond.forEach((v, i) => v > 0 && t.push(["cond" + i, `Energy Conduit ${i + 1}`, v, o.cond0])); t.push(["conv", "Intercept a reinforcement convoy", null, 0], ["esc", "Escort an alliance strike force", null, 0]); }
  if (P.ph === 4) { if (o.tx > 0 && cntXfer(o, fe)) t.push(["tx", "The transmitter array", o.tx, o.tx0]); t.push(["rx", cntXfer(o, fe) ? "The central reactor (shielded by the transfer)" : "The central reactor", o.rx, o.rx0]); }
  return t; }
/* who it fields at each target: each living hangar launches more, every regional Ark destroyed earlier takes a quarter off */
function cntFinSet(o, tg, fe) { const P = cntFinPh(o, fe), live = o.hang.filter(v => v > 0).length, w = Math.max(.25, 1 - .25 * o.dead); let u, n0, esc;
  if (/^anc/.test(tg)) { u = "cnrel"; n0 = o.anc[+tg.slice(3)]; esc = { cnexe: 3, cncor: 2, cnint: 6 }; }
  else if (/^hang/.test(tg)) { u = "cnfab"; n0 = o.hang[+tg.slice(4)]; esc = { cnint: 6, cnasm: 1, cnexe: 2 }; }
  else if (/^cond/.test(tg)) { u = "cnasm"; n0 = o.cond[+tg.slice(4)]; esc = { cncor: 2, cnint: 4 }; }
  else if (tg === "tx") { u = "cnrel"; n0 = o.tx; esc = { cneter: 1, cnexe: 3, cncor: 2 }; }
  else if (tg === "rx") { u = "cnprime"; n0 = o.rx; esc = { cndre: 2, cnasm: 2, cnexe: 3 }; }
  else if (tg === "conv") { u = "cnfab"; n0 = 0; esc = { cnfab: 1, cnint: 4, cnexe: 1 }; }
  else { u = "cnint"; n0 = 0; esc = { cnint: 6, cnexe: 2, cncor: 1 }; }
  if (P.ph >= 3 && tg !== "conv" && tg !== "esc") { esc.cnint = (esc.cnint || 0) + 2 * live; esc.cnexe = (esc.cnexe || 0) + live; } /* the cascade's reinforcements */
  for (const k in esc) esc[k] = Math.max(1, Math.round(esc[k] * w));
  const Z = cntMods(Object.assign(n0 ? { [u]: n0 } : {}, esc), tg === "rx" || tg === "tx" ? { cnt: "cmd" } : null); return { u, n0, esc, mods: Z.m, tac: Z.tac }; }
const cntFinTgName = tg => ({ conv: "a reinforcement convoy", esc: "the strike force's escort", tx: "the transmitter array", rx: "the central reactor" }[tg] || (/^anc/.test(tg) ? `Neural Anchor ${+tg.slice(3) + 1}` : /^hang/.test(tg) ? `Fabrication Hangar ${+tg.slice(4) + 1}` : `Energy Conduit ${+tg.slice(4) + 1}`));
async function cntFinResolve(f) { const B = CNT_PX, x = PB[B.id]; G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(q => q !== f); };
  try { const at = f.arrive, fe = cntFinE(at), ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), o = cntFinNorm(cur, fe), P = cntFinPh(o, fe);
    if (P.ph < 2 || P.ph > 4) { note(P.ph < 2 ? "The Prime Ark isn't open to attack yet. Fleet returning, nothing lost." : "The battle for the Prime Ark is over. Fleet returning.", "warn"); return home(); }
    const tgs = cntFinTg(o, fe); let tg = f.cntT; if (!tgs.some(t => t[0] === tg)) tg = (tgs.find(t => t[2] != null && !(t[0] === "rx" && cntXfer(o, fe))) || tgs[0])[0];
    if (tg === "rx" && cntXfer(o, fe)) { note("The reactor is still shielded by the transfer. Cut the transmitter array first. Fleet returning, nothing lost.", "warn"); return home(); }
    const Z = cntFinSet(o, tg, fe), mine0 = Object.assign({}, f.n), bonus = 1 + Math.min(.5, .05 * o.esc);
    const mkA = () => { const s = stacksOf(f.n, techVs(x), G.me); for (const q of s) { q.atk *= Z.mods.pA * bonus; q.sh *= Z.mods.pS; } return s; };
    const mkD = () => { const s = stacksOf(Object.assign(Z.n0 ? { [Z.u]: Z.n0 } : {}, Z.esc), { mon: B.lvl }, "monster"); for (const q of s) { q.atk *= Z.mods.bA; q.hull *= Z.mods.bH; } return s; };
    const { res, rise } = Z.n0 ? mimRise(mkA, mkD, Z.u, Z.n0, Z.n0) : { res: simulate(mkA(), mkD()), rise: 1 };
    const left = Z.n0 ? clamp(Math.round(((res.dLeft || {})[Z.u]) || 0), 0, Z.n0) : 0, seg = Z.n0 - left; let pts = 0, msg = "", ev = "";
    if (tg === "conv" || tg === "esc") { if (res.winner === "a") { pts = 3; if (tg === "conv") { o.conv++; msg = `Convoy intercepted (${o.conv}): the hangars rebuild ${Math.min(100, o.conv * 15)}% slower.`; } else { o.esc++; msg = `Strike force escorted (${o.esc}): every fleet hits ${Math.min(50, o.esc * 5)}% harder.`; } } else msg = `Our fleet couldn't break ${cntFinTgName(tg)}. Bring more warships.`; }
    else if (seg) { pts = 4 * seg;
      if (/^anc/.test(tg)) { const i = +tg.slice(3); o.anc[i] -= seg; if (o.anc[i] <= 0) { o.anc[i] = 0; if (o.anc.every(v => v <= 0)) { o.p3 = fe; o.rg = fe; ev = "p3"; msg = "The last Neural Anchor is down. The Prime Ark's shield has collapsed: its fabrication chambers are exposed!"; } else msg = `Neural Anchor ${i + 1} is down. ${o.anc.filter(v => v > 0).length} still hold the shield.`; } else msg = `Neural Anchor ${i + 1}: ${o.anc[i]} of ${o.anc0} left.`; }
      else if (/^hang/.test(tg)) { const i = +tg.slice(4); o.hang[i] = Math.max(0, o.hang[i] - seg); msg = o.hang[i] ? `Fabrication Hangar ${i + 1}: ${o.hang[i]} of ${o.hang0} left.` : `Fabrication Hangar ${i + 1} is destroyed. It builds nothing more.`; }
      else if (/^cond/.test(tg)) { const i = +tg.slice(4); o.cond[i] = Math.max(0, o.cond[i] - seg); msg = o.cond[i] ? `Energy Conduit ${i + 1}: ${o.cond[i]} of ${o.cond0} left.` : `Energy Conduit ${i + 1} is cut.`; }
      else if (tg === "tx") { o.tx = Math.max(0, o.tx - seg); if (!o.tx) { o.cut = fe; msg = "The transmitter array is down! The transfer is broken off, and the reactor is exposed. Everyone: the reactor!"; } else msg = `The transmitter array: ${o.tx} of ${o.tx0} left.`; }
      else if (tg === "rx") { o.rx = Math.max(0, o.rx - seg); if (!o.rx) { o.dead_ = fe; o.out = o.cut ? "win" : "part"; o.end = fe; o.last = G.me; ev = "dead"; msg = o.cut ? "THE PRIME ARK'S REACTOR IS GONE. The transfer was stopped. The Ark is dying." : "The Prime Ark's reactor is gone, but the transfer finished first. The Ark is dying; its mind is not."; } else msg = `The central reactor: ${o.rx} of ${o.rx0} left.`; }
      if (ev !== "dead" && !o.p4 && o.p3 && cntDef(o) <= .25) { o.p4 = fe; ev = "p4"; msg += " Its defences are broken: the Prime Ark is trying to send its mind away. Cut the transmitter array!"; }
      o.dmg[G.me] = (o.dmg[G.me] || 0) + Math.min(100, seg); }
    else msg = `Our fleet couldn't break a section off ${cntFinTgName(tg)}. Send more firepower.`;
    o.hits[G.me] = (o.hits[G.me] || 0) + 1; const counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur);
    const rep = mkRep({ at, kind: "attack", simLeft: left, title: `Extinction Protocol · ${cntFinTgName(tg)}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: B.name, mon: B.mon, mimB: B.id, omRise: rise > 1.01 ? Math.round(rise) : undefined, cntTac: Z.tac,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n), 1); if (rep.wrecks) note(`No ships lost for good: ${fmt(rep.wrecks)} damaged ships are coming home to the Repair Yard.`, "info");
    if (seg || pts) { const k = Math.max(1, seg), L = { m: 30000 * k, c: 20000 * k, g: 10000 * k }, ratio = Math.min(1, fCargo(f) / Math.max(1, total(L))); rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot;
      const sh = 2 * k, M = cntS(), mt = { echo: 3 * k }; if (tg === "rx") mt.core = Math.ceil(k / 4); else if (tg === "tx") mt.matrix = Math.ceil(k / 4); else if (/^hang|^cond/.test(tg)) mt.cell = Math.ceil(k / 4); S.shards = (S.shards || 0) + sh; rep.shards = sh; S.wins++; evPts("hunt", k * 50);
      cntAddM(mt); M.pts += counted; M.fin = M.fin || {}; rep.cnt = mt; logReward("Extinction Protocol", rep.loot, { shards: sh, kind: "battle" }); }
    for (const t of Z.tac) note(`${CNT_TAC[t][0]}: ${CNT_TAC[t][1]}`, "info");
    note(msg + (counted ? ` +${counted} war points.` : ""), seg || pts ? "win" : "warn"); if (rise > 1.01) note(`The Prime Ark's fleet rose to meet ours: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} cntFinClaim(); home();
  } catch (e) { if (e === CAS_RETRY && await casAgain(f, cntFinResolve)) return; note("Lost contact with the battle for the Prime Ark. Fleet returning.", "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* everyone who fought is rewarded once, by how the hour ended and how much they did */
function cntFinPart(o, uid) { const d = o.dmg[uid] || 0, h = o.hits[uid] || 0; if (!h) return 0; const top = Object.entries(o.dmg).sort((a, b) => b[1] - a[1]).slice(0, 10).some(([u]) => u === uid); return d >= 16 || top ? 3 : d >= 4 || h >= 3 ? 2 : 1; }
const CNT_PART = ["", "Participant", "Contender", "Champion"];
const CNT_FREW = { win: [{}, { echo: 80, core: 2, matrix: 1, sh: 30 }, { echo: 160, core: 4, matrix: 2, sh: 60 }, { echo: 260, core: 7, matrix: 4, sh: 100 }],
  part: [{}, { echo: 50, core: 1, matrix: 1, sh: 18 }, { echo: 100, core: 2, matrix: 1, sh: 36 }, { echo: 160, core: 4, matrix: 2, sh: 60 }],
  fail: [{}, { echo: 25, cell: 1, sh: 8 }, { echo: 50, cell: 2, sh: 15 }, { echo: 80, core: 1, cell: 3, sh: 25 }] };
function cntFinClaim() { if (!S || !G.ready) return; const T = now(); if (!cntOn(T) && cntStage(T) !== 8) return; const fe = cntFinE(T); if (fe < 0) return; const { o, P } = cntFinSt(T); if (!o.out || P.ph < 5) return;
  const M = cntS(), id = "fin"; if (M.got[id]) return; M.got[id] = 1; M.finEnd = { out: o.out, seen: 0 }; const p = cntFinPart(o, G.me); dirty(); if (!p) return;
  const r = Object.assign({}, CNT_FREW[o.out][p]); if (o.out === "win") { S.medals = S.medals || {}; S.medals.prime = (S.medals.prime || 0) + 1; } cntGrant(r, `Extinction Protocol · ${o.out === "win" ? "victory" : o.out === "part" ? "the Ark destroyed, the transfer complete" : "the Ark withdrew"}`);
  note(`Extinction Protocol is over (${o.out === "win" ? "full victory" : o.out === "part" ? "the Ark destroyed, its mind escaped" : "the Ark withdrew"}). As a ${CNT_PART[p]}: ${cntMatTxt(r)} and ◆${r.sh}${o.out === "win" ? ", and the Prime Ark Trophy" : ""}.`, "win"); }
/* the cinematic cards: the owner's paintings, slow push-ins, a line per beat; and the final transmission */
const CNT_CINE = { arr: [["art/rwar/relay.webp", "Every relay still standing fires at once.", "Their beams meet at the heart of the galaxy, and the dark there begins to turn."], ["art/rwar/ark_front.webp", "A gateway opens.", "Through it come the Continuum's last fleets, in formation, silent."], ["art/rwar/c_prime.webp", "THE PRIME RESURRECTION ARK", "Every Ark answered to it. Every commander we killed came back through it. Commander, this is the war."]],
  p2: [["art/rwar/c_prime.webp", "Phase 2 · Break the Shield", "Three Neural Anchors hold its shield. Break all three before it settles in."]],
  p3: [["art/rwar/ark_battle.webp", "Phase 3 · Resurrection Cascade", "Its chambers are open and its hangars are building. Destroy the hangars, cut the conduits, stop the convoys."]],
  p4: [["art/rwar/c_eternal.webp", "Phase 4 · The Final Continuity Transfer", "It is sending its mind to something hidden in the dark. Cut the transmitter array, then destroy the reactor."]],
  coll: [["art/rwar/c_prime.webp", "Its lights are failing.", "The shields go first. Then the reactor. Then everything that held it together."]],
  away: [["art/rwar/c_prime.webp", "The gateway is closing.", "The Prime Ark pulls back through it, wounded. We will see it again."]] };
function cntCine(key, done) { const L = CNT_CINE[key]; if (!L || document.getElementById("omcine")) return; const w = document.createElement("div"); w.id = "omcine"; w.className = "cntc"; document.body.appendChild(w); let i = 0, tm = 0;
  const show = () => { if (i >= L.length) { w.classList.add("out"); setTimeout(() => { w.remove(); done && done(); }, 600); return; } const [img, t, s] = L[i], big = /^THE PRIME/.test(t);
    w.innerHTML = `<div class="omcimg" style="background-image:url(${img})"></div><div class="omcrift"></div><div class="omctx${big ? " big" : ""}"><b>${esc(t)}</b><span>${esc(s)}</span></div><small>Tap to continue</small>`; try { (big ? SFX.megaBeam : i ? SFX.charge : SFX.alarm)(); } catch (e) {} i++; clearTimeout(tm); tm = setTimeout(show, big ? 5600 : 4400); };
  w.addEventListener("click", () => { clearTimeout(tm); show(); }); show(); }
const CNT_SIG = ["CONTINUITY TRANSFER: INCOMPLETE.", "UNKNOWN RECIPIENT DETECTED.", "OMEGA PROTOCOL: ACTIVE."]; /* the owner's own words */
function cntFinal() { if (document.getElementById("omcine")) return; const T = now(), { o } = cntFinSt(T), w = document.createElement("div"); w.id = "omcine"; w.className = "fin cntc"; document.body.appendChild(w);
  const head = o.out === "win" ? "The Prime Ark is destroyed, and its mind went nowhere." : o.out === "part" ? "The Prime Ark is destroyed. Its mind reached somewhere first." : "The Prime Ark withdrew through its gateway.";
  w.innerHTML = `<div class="omcimg" style="background-image:url(art/rwar/c_prime.webp)"></div><div class="omctx tx cntsig"><small>FINAL TRANSMISSION · INTERCEPTED</small><b class="q"></b><span class="after">${esc(head)} The Archives have a new record.</span></div><small>Tap to close</small>`;
  const q = CNT_SIG.join("\n"), el = w.querySelector(".q"); let n = 0; const tick = () => { if (!document.body.contains(w)) return; el.textContent = q.slice(0, ++n); if (n < q.length) setTimeout(tick, q[n - 1] === "\n" ? 700 : 55); else w.classList.add("done"); };
  try { SFX.gong(); } catch (e) {} setTimeout(tick, 900); w.addEventListener("click", () => { if (n < q.length) { n = q.length - 1; } else { w.classList.add("out"); setTimeout(() => w.remove(), 600); } }); }
function cntCineCheck() { if (!S || !G.ready || G.cineOn || battle || document.getElementById("omcine") || tutOn()) return; const T = now(); if (!cntOn(T) && cntStage(T) !== 8) return; const fe = cntFinE(T); if (fe < 0) return;
  const { o, P } = cntFinSt(T), M = cntS(); M.cine = M.cine || {}; const once = k => { if (M.cine[k]) return false; M.cine[k] = 1; dirty(); return true; };
  if (P.ph === 6 || P.ph === 7) { if (once("sig")) { try { archUnlock("c_signal", 2, true); archUnlock("c_prime", 2, true); } catch (e) {} cntFinClaim(); return cntFinal(); } return; }
  if (P.ph >= 1 && P.ph <= 4 && once("arr")) { try { archUnlock("c_prime", 1, true); } catch (e) {} try { advSay1("cntArr"); } catch (e) {} return cntCine("arr"); }
  if (P.ph === 2 && once("p2")) return cntCine("p2"); if (P.ph === 3 && once("p3")) { try { advSay1("cntP3"); } catch (e) {} return cntCine("p3"); } if (P.ph === 4 && once("p4")) { try { advSay1("cntP4"); } catch (e) {} return cntCine("p4"); }
  if (P.ph === 5 && once("p5")) { try { advSay1(o.out === "fail" ? "cntAway" : "cntColl"); } catch (e) {} return cntCine(o.out === "fail" ? "away" : "coll"); } }
/* the sheet: phase, timers, targets, and a way to watch */
function cntFinInfo(x, T) { const { o, fe, P } = cntFinSt(T), spd = cntFinSpd(), real = ms => T + ms / spd, bar = (v, mx) => `<div class="mimbar cntbar"><i style="width:${Math.max(0, v) / Math.max(1, mx) * 100}%"></i></div>`;
  if (fe < 0) return `<div class="mimboss cntfin"><b>Extinction Protocol</b><p class="note">The Prime Ark arrives in <b data-end="${Math.round(real(-fe))}">${ftime(-fe / spd)}</b>. Every regional Ark destroyed before then is one fabrication hangar fewer and a quarter fewer escorts in the battle.</p></div>`;
  if (P.ph >= 5) return `<div class="mimboss cntfin"><b>${o.out === "win" ? "The Prime Ark is destroyed. Full victory." : o.out === "part" ? "The Prime Ark is destroyed. Its mind escaped." : "The Prime Ark withdrew."}</b><p class="note">${P.ph === 5 ? `Phase 5 · ${o.out === "fail" ? "The gateway closing" : CNT_FPH[5]}` : "Everyone who fought has been rewarded once."} You: ${o.dmg[G.me] || 0} sections · ${o.hits[G.me] || 0} attacks · ${CNT_PART[cntFinPart(o, G.me)] || "not in the fight"}.</p>
    <button class="btn wide" data-act="cntWatch">Watch the Ark</button>${P.ph >= 6 ? `<button class="btn ghost wide" data-act="cntFinal">Replay the final transmission</button>` : ""}</div>`;
  const tg = cntFinTg(o, fe), cur = S.cntTgt && tg.some(t => t[0] === S.cntTgt) ? S.cntTgt : (tg[0] || [""])[0], live = o.hang.filter(v => v > 0).length;
  return `<div class="mimboss cntfin"><b>Phase ${P.ph} · ${CNT_FPH[P.ph]}</b><small>Ends in <span data-end="${Math.round(real(P.end - fe))}">${ftime((P.end - fe) / spd)}</span>${spd > 1 ? ` (preview at ×${spd})` : ""}</small>
    ${P.ph === 2 ? o.anc.map((v, i) => `<div class="mimanc"><span>Anchor ${i + 1}</span>${bar(v, o.anc0)}<small>${v}/${o.anc0}</small></div>`).join("") + `<p class="note">Break all three anchors before the timer or the Ark withdraws, wounded but whole.</p>` : ""}
    ${P.ph === 3 ? `<small>Ark defences ${Math.round(cntDef(o) * 100)}% · under 25% opens phase 4</small>${bar(cntDef(o), 1)}<dl class="kv"><dt>Hangars</dt><dd>${live} of ${o.hang.length} building${o.dead ? ` (${o.dead} fewer: regional Arks destroyed earlier)` : ""}</dd><dt>Conduits</dt><dd>${o.cond.map(v => `${v}/${o.cond0}`).join(" · ")}</dd><dt>Convoys stopped</dt><dd>${o.conv} · hangars rebuild ${Math.min(100, o.conv * 15)}% slower</dd><dt>Strike forces escorted</dt><dd>${o.esc} · +${Math.min(50, o.esc * 5)}% firepower for everyone</dd></dl>` : ""}
    ${P.ph === 4 ? `<dl class="kv"><dt>The transfer</dt><dd>${o.cut ? `<span style="color:var(--green)">Broken off</span>` : cntXfer(o, fe) ? `<span style="color:var(--red)">Sending · completes in <span data-end="${Math.round(real(o.p4 + CNT_FT.xcut - fe))}">${ftime((o.p4 + CNT_FT.xcut - fe) / spd)}</span></span>` : "Complete: its mind is gone"}</dd><dt>Transmitter array</dt><dd>${o.tx}/${o.tx0}</dd><dt>Central reactor</dt><dd>${o.rx}/${o.rx0}${cntXfer(o, fe) ? " · shielded" : " · exposed"}</dd></dl>${bar(o.rx, o.rx0)}` : ""}
    ${P.ph === 1 ? `<p class="note">The gateway is opening. The fight starts in <span data-end="${Math.round(real(CNT_FT.arr - fe))}">${ftime((CNT_FT.arr - fe) / spd)}</span>; fleets sent now jump through the staging gate and arrive as it begins.</p>` : ""}
    <dl class="kv"><dt>You</dt><dd>${o.dmg[G.me] || 0} sections · ${o.hits[G.me] || 0} attacks · ${CNT_PART[cntFinPart(o, G.me)] || "not yet in the fight"}</dd><dt>Travel</dt><dd>${ftime(CNT_FTRAVEL / (spd > 1 ? 3 : 1))} through the staging gate, no fuel</dd></dl>
    ${tg.length ? `<div class="omtg">${tg.map(t => `<button class="btn${t[0] === cur ? " pri" : ""}" data-act="cntTgt" data-t="${t[0]}"${t[0] === "rx" && cntXfer(o, fe) ? " disabled" : ""}>${esc(t[1])}${t[2] != null ? ` · ${t[2]}` : ""}</button>`).join("")}</div>` : ""}
    <div class="crcfind"><button class="btn" data-act="cntWatch">Watch the battle</button><button class="btn ghost" data-act="cntCineR" data-k="arr">Replay the arrival</button></div></div>`; }
/* ---------- the battle on the galaxy map: the gateway, the Prime Ark rising through it, its anchors and shield, its fleet in formation,
   the transfer beam, and the collapse: lights failing, the hull breaking apart, ships losing sync, a blue-white shockwave ---------- */
function cntBreakMat() { if (cntBreakMat.M) return cntBreakMat.M; const m = cntMeshMat().clone(), U = { uBreak: { value: 0 }, uDim: { value: 1 } }; m.userData.U = U;
  m.onBeforeCompile = sh => { cntMeshMat().onBeforeCompile(sh); Object.assign(sh.uniforms, U);
    sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nuniform float uBreak;\nfloat h31(vec3 p){ return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453); }")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nif (uBreak > 0.) { vec3 c = floor(position * .55); float h = h31(c); vec3 d = normalize(vec3(h31(c + 1.7), h31(c + 3.1), h31(c + 5.3)) - .5 + normalize(c + .5) * .8); transformed += d * uBreak * (.8 + 2.2 * h) + vec3(0., -.5 * uBreak * uBreak * h, 0.); }");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nuniform float uDim;").replace("totalEmissiveRadiance += vEm;", "totalEmissiveRadiance += vEm * uDim;"); };
  m.customProgramCacheKey = () => "cntbreak2"; return cntBreakMat.M = m; }
/* how far the arrival, the collapse and a withdrawal have got (0..1), from the finale clock */
function cntFinK(o, fe) { const inP = (a, b) => Math.max(0, Math.min(1, (fe - a) / (b - a))), ease = u => u * u * (3 - 2 * u), end = o.out ? o.end : 1e12;
  return { arr: ease(inP(.6 * CNT_FMIN, 3.6 * CNT_FMIN)), end, cf: o.out && o.out !== "fail" ? inP(end, end + CNT_FT.coll) : 0, away: o.out === "fail" ? inP(end, end + 3 * CNT_FMIN) : 0 }; }
/* the Prime Ark is the map target kx0: it slides out of the gateway as it arrives and back into it if it withdraws; in the collapse its
   lights fail and its hull breaks apart (the sculpted mesh's break material) */
function cntPrimePose(o0, it, t, T) { const fe = cntFinE(T); if (fe < 0) return; const { o } = cntFinSt(T), { arr, end, cf, away } = cntFinK(o, fe), mv = (1 - arr) + away, b = o0.body, s0 = b.scale.x;
  const gs = o0.grp.scale.x || 1; b.position.set(-22 * mv / gs, (.25 * Math.sin(t * .0003) + 2 * mv) / gs, 0); b.rotation.set(0, 0, 0); b.scale.setScalar(s0 * (.35 + .65 * arr) * (1 - .6 * away));
  if (CNT_GEO.cnprime && !o0.brk) b.traverse(m => { if (m.isMesh && m.userData.sculpt) { m.material = cntBreakMat(); o0.brk = 1; } });
  if (o0.brk) { const U = cntBreakMat().userData.U, k = Math.max(0, Math.min(1, (fe - end) / (2 * CNT_FMIN))); U.uDim.value = o.out && o.out !== "fail" ? (1 - k) * (fe < end + 2 * CNT_FMIN && Math.sin(t * .04 + Math.sin(t * .013) * 3) < -.3 ? .15 : 1) : 1; U.uBreak.value = cf > .45 ? Math.pow((cf - .45) / .55, 1.4) * 3 : 0; }
  b.visible = !(o.out && o.out !== "fail" && fe > end + CNT_FT.coll + CNT_FMIN) && !(away >= 1); }
function cntFinTick(W, t, T) { let X = W.cntF; const on = cntOn(T) && cntStage(T) === 7, fe = on ? cntFinE(T) : -1, { o, P } = on && fe >= 0 ? cntFinSt(T) : { o: null, P: { ph: 0 } };
  const show = o && P.ph >= 1 && P.ph <= 6;
  if (!show) { if (X) { W.scene.remove(X.grp); X.grp.traverse(q => { if (q.geometry && !q.userData.keep) q.geometry.dispose(); if (q.material && q.material.dispose && !q.userData.keep) q.material.dispose(); }); W.cntF = null; } return; }
  if (!X) { X = W.cntF = { grp: new TH.Group(), anc: [], beams: [], hang: [], q: {} }; W.scene.add(X.grp); const G0 = X.grp, add = (tex, col, op) => { const s = new TH.Sprite(W.additive(tex, col, op)); G0.add(s); return s; };
    const ringT = W.glow.cntRing || (W.glow.cntRing = (() => { const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), g = x.createRadialGradient(128, 128, 60, 128, 128, 128); g.addColorStop(0, "rgba(255,40,60,0)"); g.addColorStop(.72, "rgba(255,40,60,.15)"); g.addColorStop(.86, "rgba(255,70,90,1)"); g.addColorStop(.92, "rgba(255,30,50,.4)"); g.addColorStop(1, "rgba(255,30,50,0)"); x.fillStyle = g; x.fillRect(0, 0, 256, 256); return new TH.CanvasTexture(c); })());
    const swirlT = W.glow.cntSwirl || (W.glow.cntSwirl = (() => { const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"); x.translate(128, 128); for (let i = 0; i < 260; i++) { const a = i * .29, r = 6 + i * .42; x.fillStyle = `rgba(255,${40 + (i % 5) * 18},70,${.5 - i / 600})`; x.beginPath(); x.arc(Math.cos(a) * r, Math.sin(a) * r, 2 + i / 50, 0, 7); x.fill(); } return new TH.CanvasTexture(c); })());
    const gate = new TH.Mesh(new TH.PlaneGeometry(1, 1), W.additive ? new TH.MeshBasicMaterial({ map: ringT, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide }) : null); gate.renderOrder = 12; G0.add(gate); X.gate = gate;
    const sw = new TH.Mesh(new TH.PlaneGeometry(1, 1), new TH.MeshBasicMaterial({ map: swirlT, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, opacity: .8 })); sw.renderOrder = 11; G0.add(sw); X.swirl = sw;
    const shell = new TH.Mesh(new TH.SphereGeometry(1, 32, 20), new TH.MeshBasicMaterial({ color: 0xff2a40, transparent: true, opacity: .1, blending: TH.AdditiveBlending, depthWrite: false })); G0.add(shell); X.shell = shell;
    for (let i = 0; i < 3; i++) { const a = buildCnt("cnrel"); a.scale.setScalar(.85); a.traverse(q => { q.userData.keep = 1; }); G0.add(a); X.anc.push(a); const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(6), 3)); const l = new TH.Line(g, new TH.LineBasicMaterial({ color: 0xff3346, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false })); l.frustumCulled = false; G0.add(l); X.beams.push(l); }
    { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(6), 3)); X.tx = new TH.Line(g, new TH.LineBasicMaterial({ color: 0xff6070, transparent: true, opacity: 1, blending: TH.AdditiveBlending, depthWrite: false })); X.tx.frustumCulled = false; G0.add(X.tx); }
    const dotT = W.glow.cntDot || (W.glow.cntDot = glowTex("255,50,70", .6)), blueT = W.glow.cntBlue || (W.glow.cntBlue = glowTex("200,235,255", .9));
    for (let i = 0; i < 4; i++) { const s = add(dotT, 0xffffff, .9); X.hang.push(s); }
    X.wave = add(W.glow.cntRingB || (W.glow.cntRingB = (() => { const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), g = x.createRadialGradient(128, 128, 70, 128, 128, 128); g.addColorStop(0, "rgba(160,220,255,0)"); g.addColorStop(.7, "rgba(170,225,255,.25)"); g.addColorStop(.88, "rgba(235,250,255,1)"); g.addColorStop(.95, "rgba(150,210,255,.35)"); g.addColorStop(1, "rgba(150,210,255,0)"); x.fillStyle = g; x.fillRect(0, 0, 256, 256); return new TH.CanvasTexture(c); })()), 0xffffff, 0); X.flash = add(blueT, 0xffffff, 0); X.booms = []; for (let i = 0; i < 10; i++) X.booms.push({ s: add(W.glow.boom || (W.glow.boom = glowTex("255,170,80", 1)), 0xffffff, 0), t0: -1e9 });
    const geo = CNT_GEO.cnint || new TH.ConeGeometry(.35, 1.4, 5).rotateZ(-Math.PI / 2), N = 48, im = new TH.InstancedMesh(geo, CNT_GEO.cnint ? cntMeshMat() : new TH.MeshStandardMaterial({ color: 0x18181c, emissive: 0x501018, metalness: .9, roughness: .4 }), N); im.userData.keep = !!CNT_GEO.cnint; im.frustumCulled = false; G0.add(im); X.fleet = im; X.fN = N; X.dm = new TH.Object3D(); }
  const q = P3(CNT_PX, T, X.q), e = fe / 1000, inP = (a, b) => Math.max(0, Math.min(1, (fe - a) / (b - a))), ease = u => u * u * (3 - 2 * u);
  const { arr, end, cf, away } = cntFinK(o, fe);
  X.grp.position.set(q.x, q.y, q.z);
  /* the gateway: opens over the first minute, holds while the Ark comes through, then fades to a scar (or reopens to take it back) */
  const gOpen = ease(inP(0, CNT_FMIN)) * (1 - .75 * inP(4 * CNT_FMIN, 6 * CNT_FMIN)) + .8 * Math.sin(Math.PI * Math.min(1, away)), gR = 34 * (.2 + .8 * gOpen);
  X.gate.position.set(-22, 4, 0); X.gate.rotation.set(0, Math.PI / 2, 0); X.gate.scale.setScalar(gR); X.gate.material.opacity = Math.min(1, gOpen * 1.2); X.swirl.position.copy(X.gate.position); X.swirl.rotation.set(0, Math.PI / 2, t * .0004); X.swirl.scale.setScalar(gR * .9); X.swirl.material.opacity = .7 * gOpen;
  /* the shield while the anchors stand, the anchors themselves and their beams */
  const shieldUp = P.ph <= 2 && !o.p3 && !o.out; X.shell.visible = shieldUp && arr > .3; X.shell.scale.setScalar(15 * (.9 + .1 * arr)); X.shell.material.opacity = .13 + .05 * Math.sin(t * .003);
  X.anc.forEach((a, i) => { const ang = i * TAU / 3 + t * .00004, alive = o.anc[i] > 0 && !o.out, r = 23; a.position.set(Math.cos(ang) * r, 4 + 2 * Math.sin(t * .001 + i), Math.sin(ang) * r); a.visible = arr > .5 && (alive || P.ph < 2); a.rotation.y = -ang;
    const l = X.beams[i], p = l.geometry.attributes.position.array; l.visible = a.visible && P.ph <= 2; p[0] = a.position.x; p[1] = a.position.y + 4; p[2] = a.position.z; p[3] = 0; p[4] = 2; p[5] = 0; l.geometry.attributes.position.needsUpdate = true; l.material.opacity = .5 + .4 * Math.sin(t * .01 + i); });
  /* hangar glows on the hull during the cascade */
  X.hang.forEach((s, i) => { const alive = P.ph === 3 && i < o.hang.length && o.hang[i] > 0; s.visible = alive; if (alive) { const a = i * TAU / Math.max(1, o.hang.length); s.position.set(Math.cos(a) * 5, -4, Math.sin(a) * 5); s.scale.setScalar(5 + 1.5 * Math.sin(t * .006 + i)); } });
  /* the transfer: a beam out into the dark, flickering out when the array is cut */
  { const run = P.ph === 4 && cntXfer(o, fe), done = P.ph === 4 && !o.cut && !cntXfer(o, fe); X.tx.visible = run || (P.ph === 4 && o.cut && fe - o.cut < 20e3 && Math.sin(t * .05) > 0); const p = X.tx.geometry.attributes.position.array; p[0] = 0; p[1] = 10; p[2] = 0; p[3] = 220; p[4] = 140; p[5] = -110; X.tx.geometry.attributes.position.needsUpdate = true; X.tx.material.opacity = done ? 0 : .6 + .4 * Math.sin(t * .02); }
  /* its fleet: three rings in formation; in the collapse they lose sync and drift */
  { const im = X.fleet, d = X.dm, lose = o.out && o.out !== "fail" ? inP(end + .8 * CNT_FMIN, end + 3 * CNT_FMIN) : 0, vis = arr; for (let i = 0; i < X.fN; i++) { const ring = i % 3, k = Math.floor(i / 3), n = Math.ceil(X.fN / 3), R = 26 + ring * 8, sp = (ring % 2 ? -1 : 1) * .00006 * (1 + ring * .3) * (1 - lose), a0 = k / n * TAU + ring * .4, a = a0 + t * sp, yy = -4 + ring * 6 + Math.sin(a * 3 + ring) * 2;
      d.position.set(Math.cos(a) * R * (.6 + .4 * vis) - 26 * (1 - vis), yy - lose * 10 * ((i * 7) % 5) / 5, Math.sin(a) * R * (.6 + .4 * vis)); d.rotation.set(lose * (i % 5) * .5 * e % TAU, -a + (sp > 0 ? -Math.PI / 2 : Math.PI / 2), lose * ((i * 3) % 7) * .3);
      d.scale.setScalar(vis < .05 || (o.out === "fail" && away > .7) ? 0 : 1); d.updateMatrix(); im.setMatrixAt(i, d.matrix); } im.instanceMatrix.needsUpdate = true; }
  /* explosions through the collapse, then the blue-white shockwave */
  if (cf > 0 && cf < .95) for (const b of X.booms) if (t - b.t0 > 900 + (b.d || 0)) { if (Math.random() < .05 + cf * .1) { b.t0 = t; b.d = Math.random() * 600; b.s.position.set((Math.random() - .5) * 16, (Math.random() - .5) * 14, (Math.random() - .5) * 16); } }
  for (const b of X.booms) { const k = (t - b.t0) / 900; b.s.material.opacity = k >= 0 && k < 1 ? (1 - k) * .9 : 0; b.s.scale.setScalar(4 + k * 10); }
  { const w = (fe - (end + .62 * CNT_FT.coll)) / 14000; X.wave.material.opacity = w > 0 && w < 1 && o.out !== "fail" ? (1 - w) * .9 : 0; X.wave.scale.setScalar(20 + w * 300); X.flash.material.opacity = w > -.05 && w < .35 && o.out !== "fail" ? (1 - Math.abs(w) * 3) : 0; X.flash.scale.setScalar(60 + w * 80); }
  if (t - (X.cc || 0) > 2000) { X.cc = t; try { cntCineCheck(); } catch (e) {} } }
/* War Command's finale card */
function cntFinHub(T) { const s = cntStage(T); if (s !== 7 && !(s === 8 && (cntS().finEnd))) return ""; const fe = cntFinE(T), spd = cntFinSpd(); if (fe < 0) return `<div class="omhub soon cnthub"><b>Extinction Protocol</b><span>The Prime Ark arrives in <b data-end="${Math.round((T - fe / spd))}">${ftime(-fe / spd)}</b>, Saturday 6 pm Phoenix time. Every Ark destroyed before then makes the battle easier.</span></div>`;
  const { o, P } = cntFinSt(T); return `<div class="omhub cnthub"><b>Extinction Protocol${P.ph <= 4 ? " · LIVE" : ""}</b><span>${P.ph <= 6 ? `Phase ${P.ph} · ${CNT_FPH[P.ph]}` : o.out === "win" ? "The Prime Ark is destroyed." : o.out === "part" ? "The Prime Ark is destroyed; its mind escaped." : "The Prime Ark withdrew."}</span><button class="btn pri" data-act="cntGo" data-id="kx0">${P.ph >= 2 && P.ph <= 4 ? "Join the fight" : "Go to the Prime Ark"}</button><button class="btn" data-act="cntWatch">Watch</button></div>`; }
const cntFinCanSend = T => { if (!cntOn(T) || cntStage(T) !== 7) return false; const fe = cntFinE(T); if (fe < 0) return false; const { P } = cntFinSt(T); return P.ph >= 1 && P.ph <= 4; };
/* watch the whole battle: the gateway, the anchors and the fleet rings, not just the hull */
function cntWatch(n) { try { cineObjStart("kx0"); if (!G3 || !G3.cam.cineObj) { if ((n || 0) < 10) setTimeout(() => cntWatch((n || 0) + 1), 400); return; } const c = G3.cam; c.cineObj.fit = 1; c.cineObj.r = 26; c.goal = Object.assign({}, c.goal || {}, { dist: 72 }); } catch (e) {} }
const cntFinTravel = () => CNT_FTRAVEL / (cntFinSpd() > 1 ? 3 : 1);
/* what the launch screen and the battle preview show: the force at the target you picked */
function cntFinForce(T) { T = T || now(); const { o, fe } = cntFinSt(T), tg = cntFinTg(o, fe); if (!tg.length) return { cnprime: 1, cndre: 2, cnexe: 4 }; const pick = S.cntTgt && tg.some(t => t[0] === S.cntTgt) ? S.cntTgt : tg[0][0], Z = cntFinSet(o, pick, fe);
  return Object.assign(Z.n0 ? { [Z.u]: Z.n0 } : {}, Z.esc); }
/* the header art of a Continuum target: its painting, or a render of its hull */
function cntHeadArt(x) { const k = CNT_M[x.mon], a = (CNT_BOSS[x.id] && CNT_BOSS[x.id].art) || CNT_ART[k]; return a ? `<div class="monart crcart"><img src="art/rwar/${a}.webp" alt="" loading="lazy"></div>` : `<div class="monart crcart"><canvas data-ship="${k}" width="600" height="300"></canvas></div>`; }
