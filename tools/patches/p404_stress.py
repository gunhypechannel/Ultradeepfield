# v404: owner-only stress-test battles. One player fleet of 10,000,000 mixed ships (50 Cube Destroyers among them) against every super
# boss and every form it takes (the Overlord's shield at 4/2/0 conduits, the swarm, the Wyrm hidden/exposed, the Colossus whole/cracked/
# shattered, the five Elementals, the Pentarch with 5/3/1/0 elements). Each battle is timed and checked (finite numbers, losses within
# what fought, frames to replay), and each can be watched as a battle report. Local only: nothing is written to the shared boss record,
# no rewards, no reports in the player's list.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

rep("""/* v402 the Pentarch's wings:""", """/* v404 owner stress tests */
const vsum = o => Object.values(o || {}).reduce((a, v) => a + (+v || 0), 0);
const STRESS_FLEET = { fighter: 3000000, heavyFighter: 2000000, corvette: 1500000, bomber: 1200000, destroyer: 900000, battleship: 700000, lancer: 400000, dreadnought: 200000, bastion: 99950, worldbreaker: 50 };
function stressCases() { const C = [], add = (key, form, sh, n0 = WB_SEG, pent) => C.push({ key, form, sh, n0, pent });
  add("ovl", "4 conduits up", 4); add("ovl", "2 conduits up", 2.5); add("ovl", "shield down", 1); add("c0", "", 1); add("dev", "", 1); add("war", "", 1);
  add("brd", "drone swarm", 2); add("brd", "swarm thinned", 1); add("tyr", "", 1); add("wym", "segments hidden", 1.6); add("wym", "segments exposed", 1);
  add("col", "whole", 1, WB_SEG); add("col", "cracked", 1.4, 20); add("col", "shattered", 1.8, 10);
  for (const k of WB_EL) add(k, "", 1);
  for (const L of [["ice", "fire", "light", "storm", "nature"], ["ice", "fire", "light"], ["fire"], []]) add("epx", `${L.length} of 5 elements`, .25 + .15 * L.length, WB_SEG, L);
  return C; }
function stressCheck(res, fleet, n0, k, F) { const bad = [], fin = v => typeof v === "number" && isFinite(v) && v >= 0;
  for (const [nm, L, S0] of [["ours", res.aLeft || {}, fleet], ["boss", res.dLeft || {}, { [k]: n0 }]]) for (const u in L) { if (!fin(L[u])) bad.push(`${nm} ${u} = ${L[u]}`); else if (L[u] > (S0[u] || 0) + .5) bad.push(`${nm} ${u} grew`); }
  if (!(res.rounds && res.rounds.length)) bad.push("no rounds"); if (!F || !F.length) bad.push("no frames"); else for (const f of F) { for (const s of f.s) if (!isFinite(s[0]) || !isFinite(s[1])) { bad.push("a ship off the field"); break; } if (bad.length > 4) break; }
  return bad; }
async function stressRun() { if (!duelOwner() || (G.stress && G.stress.busy)) return; const C = stressCases(), out = []; G.stress = { busy: true, out, n: C.length, t0: performance.now() }; if (sheet && sheet.type === "stress") renderSheet();
  for (const c of C) { await sleep(40); const D = WB[c.key]; let r = { c, ok: false };
    try { const t0 = performance.now(), A = stacksOf(STRESS_FLEET, techOf(null), G.me), Dd = stacksOf({ [D.k]: c.n0 }, { wbSh: c.sh }, "wboss"), res = simulate(A, Dd), ms = performance.now() - t0;
      const left = clamp(Math.round(((res.dLeft || {})[D.k]) || 0), 0, c.n0), lossA = lossesOf(res.start.a, res.aLeft);
      const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Stress test · ${D.n}${c.form ? ` (${c.form})` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: D.n, wb: c.key, wbSh: c.sh, wbSeg: [c.n0, left], lvl: 25, ptype: "gas", fortL: 0, alien: true,
        start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA, lossD: lossesOf(res.start.d, res.dLeft) }); if (c.pent) rep.pent = c.pent;
      await sleep(20); const t1 = performance.now(), R = battleSim(rep).res.rec, msR = performance.now() - t1, bad = stressCheck(res, STRESS_FLEET, c.n0, D.k, R && R.frames); // the replay re-simulates: check its frames too
      r = { c, ok: !bad.length, bad, ms, msR, rounds: res.rounds.length, left, lost: vsum(lossA), cd: lossA.worldbreaker || 0, frames: R && R.frames ? R.frames.length : 0, rep }; }
    catch (e) { r.bad = [String(e && e.message || e).slice(0, 120)]; }
    out.push(r); if (sheet && sheet.type === "stress") renderSheet(); }
  G.stress.busy = false; G.stress.ms = performance.now() - G.stress.t0; if (sheet && sheet.type === "stress") renderSheet(); }
function shStress() { const st = G.stress, out = st ? st.out : [], fails = out.filter(r => !r.ok).length, tot = vsum(Object.values(STRESS_FLEET));
  const head = `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">Owner</div><h2>Stress-test battles</h2><p class="note">One fleet of ${fmt(tot)} ships (${fmt(STRESS_FLEET.worldbreaker)} Cube Destroyers among them) against every super boss in every form. Only you see this; nothing is saved or shared.</p></div><div class="fhdb"><button class="x" data-act="close" aria-label="Close">✕</button></div></div>`;
  const run = `<button class="btn wide" data-act="stressRun"${st && st.busy ? " disabled" : ""}>${st && st.busy ? `Running ${out.length} of ${st.n}…` : st ? "⚔ Run them again" : "⚔ Run all " + stressCases().length + " battles"}</button>`;
  const sumL = st && !st.busy ? `<p class="note">${fails ? `<b style="color:#ff8a6a">${fails} failed</b>` : "<b style=\\"color:#7dff9a\\">All passed</b>"} · ${out.length} battles in ${(st.ms / 1000).toFixed(1)} s · slowest ${Math.round(Math.max(...out.map(r => r.ms || 0)))} ms</p>` : "";
  const fleet = `<details class="note" style="margin:6px 0"><summary>The fleet</summary>${Object.entries(STRESS_FLEET).map(([k, n]) => `${fmt(n)} ${esc(SH[k].n)}`).join(" · ")}</details>`;
  const rows = out.map((r, i) => { const D = WB[r.c.key], pct = r.rep ? Math.round((r.c.n0 - r.left) / WB_SEG * 100) : 0;
    return `<div class="strow${r.ok ? "" : " bad"}"><div style="flex:1;min-width:0"><b>${D.ic} ${esc(D.n)}</b>${r.c.form ? ` <span class="note">${esc(r.c.form)}</span>` : ""}<div class="note">${r.rep ? `${Math.round(r.ms)} ms (replay ${Math.round(r.msR)} ms) · ${r.rounds} ${r.rounds === 1 ? "volley" : "rounds"} · ${r.left ? `${pct}% of its hull destroyed` : "destroyed"} · lost ${fmt(r.lost)} ships${r.cd ? `, ${r.cd} Cube Destroyers` : ""}` : ""}${r.bad && r.bad.length ? `<br><span style="color:#ff8a6a">${esc(r.bad.join("; "))}</span>` : ""}</div></div>${r.rep ? `<button class="btn ghost" data-act="stressPlay" data-i="${i}">▶</button>` : ""}</div>`; }).join("");
  return head + run + sumL + fleet + `<div class="strows">${rows}</div>`; }
/* v402 the Pentarch's wings:""")
rep("""  epxAim: d =>""", """  stressOpen: () => { if (!duelOwner()) return; openSheet({ type: "stress" }); },
  stressRun: () => { if (!duelOwner()) return; stressRun(); },
  stressPlay: d => { const r = G.stress && G.stress.out[+d.i]; if (r && r.rep) playBattle(r.rep); },
  epxAim: d =>""")
rep("health: shHealth", "stress: shStress, health: shHealth")
rep("""<button class="btn ghost wide" data-act="elePrev">""", """<button class="btn ghost wide" data-act="stressOpen">⚔ Stress-test battles</button><button class="btn ghost wide" data-act="elePrev">""")
rep(".convband{display:flex;", ".strow{display:flex;gap:8px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.08)}.strow.bad b{color:#ff8a6a}.strows{margin-top:8px}.convband{display:flex;")
t = t.replace("const GAME_V = 403;", "const GAME_V = 404;")
open(p, "w").write(t); print("ok")
