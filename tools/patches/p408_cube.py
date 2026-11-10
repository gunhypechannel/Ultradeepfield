# v408: (1) tapping the Super Cube offers a choice: the cinematic view (the live siege camera, or the arrival film when no battle is on),
# the Events page, or (during the battle) the scan; (2) the owner can watch the whole Elemental Convergence as a 3-minute time-lapse on
# the map: the five loose, fights against them, two slain, the countdown, the fusion set piece, the Pentarch's wings torn loose and its
# fall with the shards (a local copy of the state only: nothing is saved, shared or rewarded); (3) the Collective Warden rises to meet a
# huge fleet like the super bosses: one attack wears it down by 30% rising to 60% of its force instead of seizing the Cube at once, until
# it is worn to its limit; a Cube held by an alliance (a player garrison) is never scaled.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

# ---------- (1) the Cube's tap menu ----------
rep("""  if (best && best.nexus) { if (cubePhase(now())) { G.cubeScan = performance.now() + 9000; G.cubeOpen = true; const el = $("#cubepanel"); if (el) el._h = ""; } else openSheet({ type: "events", ev: "cube" }); return; }""",
    """  if (best && best.nexus) { openSheet({ type: "cubepick" }); return; } /* v408: tapping the Cube asks what to do */""")
rep("""/* v402 the Pentarch's wings:""", """/* v408 tapping the Super Cube */
function shCubePick() { const T = now(), ph = cubePhase(T), live = evActive(T), cur = nexusNow(T), who = cur.holder ? `Held by ${esc(allyTag(cur.holder))}` : live ? "Unclaimed · the Collective Warden guards it" : `Next battle in ${ftime(evStart(evWeek(T) + 1) - T)}`;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">${live ? "● LIVE · " : ""}Battle for the Cube</div><h2>The Super Cube</h2><p class="note">${who}</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="cubepick"><button class="btn amber wide" data-act="cubeCine">🎬 ${live ? "Watch the battle live" : "Cinematic view"}</button>${live ? "" : `<button class="btn ghost wide" data-act="liveReplay">▶ Watch the Cube's arrival</button>`}
    <button class="btn wide" data-act="events" data-ev="cube">📅 Events page</button>${ph ? `<button class="btn ghost wide" data-act="cubeScanHere">◎ Scan the Cube</button>` : ""}</div>`; }
/* v408 the owner's time-lapse of the whole Elemental Convergence, on a local copy of the boss state */
const CONV_SIM = [[0, "start"], [4000, "say:wb3_new"], [7000, "cam:eic"], [9000, "hit:eic:6"], [14000, "hit:efi:8"], [17000, "cam:eli"], [19000, "hit:eli:14"], [24000, "hit:eli:14"], [27000, "cam:est"], [29000, "hit:est:16"],
  [33000, "hit:eli:12"], [36000, "hit:est:16"], [40000, "cam:ena"], [42000, "hit:ena:9"], [46000, "hit:est:8"], [50000, "cam:efi"], [52000, "hit:efi:7"], [58000, "say:wb3_soon"], [66000, "fuse"],
  [116000, "pent:8"], [122000, "pent:9"], [128000, "pent:9"], [134000, "pent:8"], [140000, "pent:6"], [146000, "end"]];
function convSimStart() { if (!duelOwner()) return; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } const st = jcopy(wbState(now())); for (const k of [...WB_EL, "epx"]) { st.hp[k] = WB_SEG; st.dead[k] = 0; st.dmg[k] = {}; } st.shed = []; st.wing = {};
  G.convSim = { t0: performance.now(), st, i: 0 }; G.elePrev = 1; WB_SEPC = null; WB_ZONES = null; WB_INF = null; toast("Owner preview: the whole Elemental Convergence in three minutes. Only you see this."); }
function convSimTick() { const C = G.convSim; if (!C) return; const s = performance.now() - C.t0, st = C.st;
  while (C.i < CONV_SIM.length && s >= CONV_SIM[C.i][0]) { const [, ev] = CONV_SIM[C.i++], [a, b, c] = ev.split(":");
    if (a === "say") advHolo(ADV_NEWS[b]);
    else if (a === "cam") { try { cineObjStart("wb_" + b); } catch (e) {} }
    else if (a === "hit") { const n0 = st.hp[b], seg = Math.min(n0, +c); st.hp[b] = n0 - seg; WB_ZONES = null; try { wbFight(b, seg, !st.hp[b]); } catch (e) {} if (!st.hp[b]) { st.dead[b] = now(); advHolo(ADV_NEWS["wb_fall_" + b]); } }
    else if (a === "fuse") { G.elePrev = 2; G.fuseRep = performance.now(); WB_SEPC = null; WB_ZONES = null; if (G3 && G3.wbM && G3.wbM.epx) G3.wbM.epx.dk = null; try { cineObjStart("wb_epx"); } catch (e) {} advHolo(ADV_NEWS.wb3_fuse); }
    else if (a === "pent") { const n0 = st.hp.epx, seg = Math.min(n0, +b), left = n0 - seg; st.hp.epx = left; const live = () => wbFusedIn(st).filter(k => !st.shed.includes(k)), due = [.2, .4, .6, .8].filter(x => 1 - left / WB_SEG >= x).length;
      while (st.shed.length < due && live().length) { const k = live()[0]; st.shed.push(k); advHolo(ADV_NEWS["wb_shed_" + k]); } try { wbFight("epx", seg, !left); } catch (e) {} if (!left) { st.dead.epx = now(); setTimeout(() => advHolo(ADV_NEWS.wb_fall_epx), 2500); setTimeout(() => advHolo(ADV_NEWS.wb3_shards), 9000); } }
    else if (a === "end") { setTimeout(() => { if (G.convSim === C) { G.convSim = null; G.elePrev = 0; G.fuseRep = 0; WB_SEPC = null; WB_ZONES = null; WB_INF = null; try { cineEnd(); } catch (e) {} toast("The Convergence preview has ended."); } }, 20000); } } }
setInterval(() => { try { convSimTick(); } catch (e) {} }, 250);
/* v402 the Pentarch's wings:""")
rep("""function wbState(T = now()) { const src""", """function wbState(T = now()) { if (G.convSim) return G.convSim.st; const src""")
rep("""  epxAim: d =>""", """  cubeCine: () => { closeSheet(); siegeStart(); const go = n => { if (G3 && G3.cam.siege) G3.cam.siege.show = 1; else if (n < 20) setTimeout(() => go(n + 1), 300); }; go(0); },
  cubeScanHere: () => { closeSheet(); G.cubeScan = performance.now() + 9000; G.cubeOpen = true; const el = $("#cubepanel"); if (el) el._h = ""; },
  convSim: () => convSimStart(),
  convSimStop: () => { if (G.convSim) { G.convSim = null; G.elePrev = 0; G.fuseRep = 0; WB_SEPC = null; WB_ZONES = null; try { cineEnd(); } catch (e) {} toast("Preview stopped."); } if (sheet) renderSheet(); },
  epxAim: d =>""")
rep("stress: shStress, health: shHealth", "stress: shStress, cubepick: shCubePick, health: shHealth")
rep("""<button class="btn ghost wide" data-act="stressOpen">⚔ Stress-test battles</button>""", """<button class="btn ghost wide" data-act="stressOpen">⚔ Stress-test battles</button><button class="btn ghost wide" data-act="${G.convSim ? "convSimStop" : "convSim"}">${G.convSim ? "■ Stop the Convergence preview" : "▶ Watch the whole Elemental Convergence"}</button>""")
rep(".strow{display:flex;", ".cubepick{display:grid;gap:8px;margin-top:6px}.strow{display:flex;")

# ---------- (3) the Collective Warden rises to meet a huge fleet ----------
rep("""/* a fight against a boss that rises to meet the fleet:""", """/* v408 the same for the Cube's Collective Warden: aim one attack at a share of its force (30% rising to 60%); a Warden worn to its
   limit (integrity 25% or less) can be broken and the Cube seized; frac(res) is the share of the defenders destroyed */
function riseFight(mkA, mkD, frac, worn) { let { F, x } = wbRiseK(mkA(), mkD()); if (F <= 1 || worn) return { res: simulate(mkA(), mkD()), rise: 1 };
  const tgt = clamp(.3 + .09 * Math.log10(x), .3, .6); let lo = 1, hi = 0, best = null;
  for (let i = 0; i < 9; i++) { const A = mkA(), D = mkD(); for (const s of D) { s.atk *= F; s.hull *= F; } const res = simulate(A, D), f = frac(res), err = Math.abs(f - tgt);
    if (!best || err < best.err) best = { res, F, err }; if (err <= .05) break; if (f > tgt) lo = F; else hi = F; F = hi ? Math.sqrt(Math.max(lo, 1) * hi) : F * Math.max(1.5, Math.pow(f / tgt, 1.6)); if (hi && hi / Math.max(lo, 1) < 1.03) break; }
  return { res: best.res, rise: best.F }; }
const cubeKilled = res => { const s0 = Object.values(res.start.d || {}).reduce((a, v) => a + v, 0), s1 = Object.values(res.dLeft || {}).reduce((a, v) => a + Math.max(0, v), 0); return s0 ? 1 - s1 / s0 : 1; };
function cubeFight(A0, cur) { const D = nexusDefense(cur); if (!D.alien) return { D, res: simulate(A0(), D.stacks), rise: 1 }; const { res, rise } = riseFight(A0, () => nexusDefense(cur).stacks, cubeKilled, cubeIntegrity(cur) <= .25); return { D, res, rise }; }
/* a fight against a boss that rises to meet the fleet:""")
rep("""    const D = nexusDefense(cur), res = simulate(stacksOf(f.n, techOf(null), G.me), D.stacks);
    const rep = mkRep({ at, kind: "attack", title: "Assault on the Cube",""", """    const { D, res, rise } = cubeFight(() => stacksOf(f.n, techOf(null), G.me), cur); if (rise > 1.01) note(`The Collective Warden rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    const rep = mkRep({ at, kind: "attack", title: "Assault on the Cube",""")
rep("""        else { const D = nexusDefense(cur), res = simulate(A, D.stacks); if (!cur.holder) wardenWear(cur, res);""", """        else { const A1 = A.map(s => Object.assign({}, s)), { D, res } = cubeFight(() => A1.map(s => Object.assign({}, s)), cur); if (!cur.holder) wardenWear(cur, res);""")
rep("""  if (!cubePhase(now())) siegeEnd(); // films every phase of the event, Arrival to Aftermath""", """  if (!cubePhase(now()) && !c.siege.show) siegeEnd(); // films every phase of the event, Arrival to Aftermath (v408: or the Cube on its own, from its tap menu)""")
rep("""if (w) w.textContent = `● LIVE · Battle for the Cube · ${SIEGE_SHOTS[sh]}`;""", """if (w) w.textContent = c.siege.show && !cubePhase(now()) ? `◎ The Super Cube · ${SIEGE_SHOTS[sh]}` : `● LIVE · Battle for the Cube · ${SIEGE_SHOTS[sh]}`;""")
t = t.replace("const GAME_V = 407;", "const GAME_V = 408;")
open(p, "w").write(t); print("ok")
