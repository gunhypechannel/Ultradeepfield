/* ---------- v671 the Mimic Protocol in the Boss Lab and the stress tests ----------
   Owner: "Is this also gonna be in battle lab and battle previews?" Every Mimic fight can be watched from the Boss Lab on this device
   (a demo fleet against each hive stage, an Echo hive, each Alpha, a Nexus, each Omega phase and its nodes and pylons), the invasion
   can be previewed week by week, the Omega weekend with its arrival cinematic, and the stress tests run the Mimic bosses too. */
const MIM_LAB_FLEET = { battleship: 400, destroyer: 200, dreadnought: 80, bomber: 100, fighter: 600, armageddon: 2 };
const MIM_LAB = [["hive1", "Hive · Stage 1", () => mimLabForce(1)], ["hive2", "Hive · Stage 2", () => mimLabForce(2)], ["hive3", "Hive · Stage 3", () => mimLabForce(3)], ["hive4", "Hive · Stage 4 with a Brood Titan", () => mimLabForce(4)],
  ["echo", "Hive with Mimic Echoes", () => Object.assign(mimLabForce(3), { e_battleship: 4, e_destroyer: 2 })],
  ["alpha1", "Alpha Sovereign I", () => ({ malpha1: 12, mguard: 3, mstalk: 4 })], ["alpha2", "Alpha Sovereign II", () => ({ malpha2: 12, mguard: 3, mstalk: 4 })], ["alpha3", "Alpha Sovereign III", () => ({ malpha3: 12, mguard: 3, mstalk: 4 })], ["alpha4", "Alpha Sovereign IV", () => ({ malpha4: 12, mguard: 3, mstalk: 4 })],
  ["nexus", "Neural Nexus · an anchor", () => ({ mnexus: 25, mguard: 2, mharv: 2 })],
  ["om1", "Omega · phase 1, The Swarm", () => ({ momega: 20, mstalk: 6, mhunt: 3, malpha1: 1 })], ["node", "Omega · a Neural Node", () => ({ mnode: 20, mstalk: 3 })],
  ["om2", "Omega · phase 2, Assimilation", () => ({ momega: 20, e_battleship: 2, mguard: 2 })], ["pylon", "Omega · an Assimilation Pylon", () => ({ mpylon: 20, mguard: 2 })],
  ["om3", "Omega Unbound · phase 3", () => ({ momegax: 20, mstalk: 6, mhunt: 3 })], ["swarm", "Omega's swarm (small fleet)", () => ({ mstalk: 6, mhunt: 2, mharv: 1 })]];
function mimLabForce(st) { const n = 1 + Math.floor(20 / 4), o = { mnest: 1, mstalk: 2 + n, mharv: 1 }; if (st >= 2) { o.mstalk += 1; o.mharv = 2; o.mhunt = 1 + (n >> 1); } if (st >= 3) { o.massim = 1 + Math.floor(n / 3); o.mguard = 1 + Math.floor(n / 3); } if (st >= 4) { o.mtitan = 1; o.mguard += 1; } return o; }
function mimLabFight(k) { const L = MIM_LAB.find(x => x[0] === k); if (!L) return; const D0 = L[2](), small = k === "swarm", A0 = small ? { battleship: 20, fighter: 40, corvette: 20 } : MIM_LAB_FLEET, lvl = small ? 5 : 20;
  const res = simulate(stacksOf(A0, techOf(null), G.me), stacksOf(D0, { mon: lvl }, "monster"));
  const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Battle Lab · ${L[1]}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: L[1], mon: /^hive|^echo/.test(k) ? "mimic" : null, lvl, ptype: "desert", fortL: 0, alien: true, pirate: true,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
  closeSheet(); playBattle(rep); }
function mimLabOmega() { if (!duelOwner()) return; S.mimPrev = { w: 4, at: now(), om: 1 }; MSC = {}; dirty(); closeSheet();
  setTimeout(() => { try { moCine("arr"); } catch (e) {} }, 900); toast("Owner preview: the Omega weekend, on this device only. Turn it off in the Boss Lab (W Off)."); }
function mimLabHTML(row0, b) { const p = S.mimPrev || {}, row = (ic, n, sub, btns) => `<div class="strow" style="flex-wrap:wrap"><div style="flex:1 1 100%;min-width:0"><b>${ic} ${esc(n)}</b>${sub ? `<div class="note">${sub}</div>` : ""}</div><div style="display:flex;flex-wrap:wrap;gap:6px">${btns}</div></div>`;
  return row("⬢", "The invasion, week by week", `Hives, Alphas and the hub as they will be · ${p.w ? (p.om ? "previewing Omega" : `previewing week ${p.w}`) : "off"}`, [1, 2, 3, 4].map(w => b("mimLabWeek", String(w), "W" + w)).join("") + b("mimLabWeek", "0", "Off"))
    + row("⬢", "Omega: The Convergence", "The arrival cinematic, then Omega on the map with its Central Nexus", b("labPrev", "krk", "▶ Preview") + b("moCine", "p2", "Phase 2") + b("moCine", "p3", "Phase 3") + b("moFinal", "", "Ending"))
    + MIM_LAB.map(([k, n]) => row0(k === "echo" ? "◈" : /^om|node|pylon|swarm/.test(k) ? "⬢" : "✣", n, k === "swarm" ? "A small fleet clears a wave" : "A demo fleet of 1,400 warships", b("mimLabFight", k, "⚔ Watch"))).join(""); }
