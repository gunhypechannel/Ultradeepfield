# v598 (1) the Titan inspection viewer showed the old hand-built Eclipse Harbinger: it builds its model once when it opens, and if
# the Meshy model had not finished loading the Titan fell back to the old hull for good. Now it says "Loading the high-detail
# model…" and rebuilds itself the moment the model arrives. (2) a new owner's battle in Mail: Duel · 1 vs 1 · 10 million mixed
# units of every warship class (Light Fighters to Cube Destroyers, both carriers and all three Titans) against 5 million of the same
# mix, equal technology, built from a fixed seed and kept in memory only. (3) the original 3-million duel gets the three Titans too.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# (1) the viewer
rep('  if (V.cv.parentNode !== slot) { slot.textContent = ""; slot.appendChild(V.cv); } if (!V.raf) V.raf = requestAnimationFrame(t3Frame); }',
    '  if (V.cv.parentNode !== slot) { slot.textContent = ""; slot.appendChild(V.cv); } if (!V.raf) V.raf = requestAnimationFrame(t3Frame);\n  { const cap = document.getElementById("t3cap"); if (cap) cap.textContent = TITAN_ROT[V.k] && glbOn() && !glbGet(V.k) ? "Loading the high-detail model…" : "Drag to turn · pinch to zoom"; } } /* v598 */')
rep('function glbReady(k) {', 'function glbReady(k) { if (TITAN_ROT[k] && G.t3 && G.t3.k === k && sheet && sheet.k === k) setTimeout(() => { try { if (G.t3 && G.t3.k === k && sheet && sheet.k === k) { t3Free(); t3Start(); } } catch (e) {} }, 0); /* v598 the viewer swaps in the model once it lands */')
# (2) the 10 million vs 5 million duel
rep('/* v429 the owner\'s faction war:', '''/* v598 the owner's big mixed duel: 10 million against 5 million, every warship class in the same proportions on both sides */
const DUEL2_ID = "lab-duel-10v5", DUEL2_MIX = { fighter: 2996000, heavyFighter: 2000000, lancer: 1600000, corvette: 1200000, bomber: 600000, guardian: 400000, battleship: 400000, bastion: 250000, destroyer: 250000, dreadnought: 150000, escortCarrier: 100000, supercarrier: 40000, eclipse: 6000, worldbreaker: 4000, armageddon: 1500, sovereign: 1500, harbinger: 1000 }; /* 10,000,000 */
function duel2Battle() {
  if (G.duel2Rep) return G.duel2Rep;
  G.names.pd2A = "Imperator Rhaen Vos"; G.names.pd2D = "Admiral Liska Mourne";
  const fleet = f => { const o = {}; let r = 0; for (const k in DUEL2_MIX) { if (SH[k]) o[k] = Math.round(DUEL2_MIX[k] * f); else r += Math.round(DUEL2_MIX[k] * f); } if (r) o.fighter = (o.fighter || 0) + r; return o; };
  const A0 = fleet(1), D0 = fleet(.5); let n = 0; for (const k in A0) n += A0[k] + (D0[k] || 0);
  const res = simulate(stacksOf(A0, { weapons: 16, shields: 16, armor: 16 }, "pd2A"), stacksOf(D0, { weapons: 16, shields: 16, armor: 16 }, "pd2D"), { seed: 105105 });
  if (!S.duel2Mail) { S.duel2Mail = { t: now() }; dirty(); }
  return (G.duel2Rep = Object.assign(mkRep({ at: S.duel2Mail.t, kind: "attack", title: `Duel · 1 vs 1 · ${n.toLocaleString("en-US")} units`, aUids: [], aName: G.names.pd2A, dName: G.names.pd2D, lvl: 30, ptype: "ice", fortL: 0, alien: false,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) }), { id: DUEL2_ID, recDone: 1 }));
}
/* v429 the owner's faction war:''')
rep('  if (duelOwner() && !S.fac4Mail) { S.fac4Mail = { t: now() }; dirty(); } // v429 the faction war',
    '  if (duelOwner() && !S.fac4Mail) { S.fac4Mail = { t: now() }; dirty(); } // v429 the faction war\n  if (duelOwner() && !S.duel2Mail) { S.duel2Mail = { t: now() }; dirty(); } // v598 10 million vs 5 million')
rep('duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: "battle", fac4: 1 }] : [], (S.spyReps || [])',
    'duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: "battle", fac4: 1 }] : [], duelOwner() && S.duel2Mail ? [{ t: S.duel2Mail.t, f: "battle", duel2: 1 }] : [], (S.spyReps || [])')
rep('const list = f === "saved" ? (duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: "battle", fac4: 1 }] : [])',
    'const list = f === "saved" ? (duelOwner() && S.duel2Mail ? [{ t: S.duel2Mail.t, f: "battle", duel2: 1 }] : []).concat(duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: "battle", fac4: 1 }] : [])')
rep('    if (x.duel) return `<button class="mrowc good lab" data-act="duelBattle">',
    '''    if (x.duel2) return `<button class="mrowc good lab" data-act="duel2Battle"><span class="mi">⚔</span><span class="mt"><b>Duel · 1 vs 1 · 10 million vs 5 million mixed</b><small>Your private test: two commanders, every warship class from Light Fighters to Cube Destroyers, both carriers and all three Titans, the same mix on both sides at equal technology, 10 million against 5 million. Tap to build it and watch (it takes a moment).</small></span><span class="mw"><time>${ago(x.t)} ago</time></span></button>`;
    if (x.duel) return `<button class="mrowc good lab" data-act="duelBattle">''')
rep('  duelBattle: () => { if (!duelOwner()) return;', '''  duel2Battle: () => { if (!duelOwner()) return; toast("Building the 10 million vs 5 million duel…"); setTimeout(() => { try { playBattle(duel2Battle()); } catch (e) { toast("Couldn't build the duel on this device.", "warn"); } }, 60); }, /* v598 */
  duelBattle: () => { if (!duelOwner()) return;''')
rep('lab = r.id === LAB_ID || r.id === DUEL_ID;', 'lab = r.id === LAB_ID || r.id === DUEL_ID || r.id === DUEL2_ID;')
# (3) the original 1 vs 1 duel predates the Titans: they join its every-class list (DUEL_K titans)
rep('"destroyer", "dreadnought", "eclipse", "worldbreaker"];', '"destroyer", "dreadnought", "eclipse", "worldbreaker", "armageddon", "sovereign", "harbinger"]; /* v598 the Titans */')
rep('two commanders, every class from Light Fighters to Cube Destroyers, plus 12 million', 'two commanders, every class from Light Fighters to Cube Destroyers and the three Titans, plus 12 million')
rep('for (const k of DUEL_K) if (SH[k]) o[k] = 3e6;', 'for (const k of DUEL_K) if (SH[k]) o[k] = TITAN_INFO[k] ? 3e4 : 3e6; /* v598 Titans at 30,000 each, so it still ends with a winner */')
s2 = re.sub(r"GAME_V = 597\b", "GAME_V = 598", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
