# v429: the owner's faction war, a private test battle in Mail (owner: "a 4 vs 4 battle simulation with mixed 10 million units and
#  each side has all 4 different factions, viewable only for me"). Eight commanders, four a side, one of each faction (Terran Union,
#  Solar Dominion, Nyx Syndicate, Verdant Collective) on both sides, 1.25 million mixed warships each (10,000,000 in all, every class
#  from Light Fighters to Cube Destroyers plus carriers). Every commander's flagship flies (this battle shows all 4 a side; real
#  battles keep their 3). Built on this device from a fixed seed like the duel, never saved to the cloud; shown only to duelOwner().
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("/* ---------- Mail: one inbox for battle reports,", """/* v429 the owner's faction war: 4 vs 4, one commander of every faction a side, 10 million mixed units */
const FAC4_ID = "lab-fac4v4", FAC4_N = { a: ["High Admiral Seren Vale", "Sunlord Idris Kaan", "Matriarch Vey Solenne", "Warden Thal Orrin"], d: ["Fleet Marshal Dax Corwen", "Solarch Mira Teve", "Shadow Regent Kael Vros", "Grovemaster Ysra Lune"] };
function fac4Battle() {
  if (G.fac4Rep) return G.fac4Rep;
  const base = { fighter: 375000, heavyFighter: 250000, lancer: 200000, corvette: 150000, bomber: 75000, guardian: 50000, battleship: 50000, bastion: 31250, destroyer: 31250, dreadnought: 18750, escortCarrier: 12500, supercarrier: 5000, eclipse: 750, worldbreaker: 500 }; /* 1,250,000 a commander */
  const mix = i => { const o = Object.assign({}, base), k = ["lancer", "corvette", "bomber", "destroyer"][i]; o.fighter -= 60000 * i; o[k] += 60000 * i; for (const x in o) if (!SH[x]) { o.fighter += o[x]; delete o[x]; } return o; }; /* each faction leans on a different class; the total stays the same */
  const side = (sd, tech) => { let L = []; FAC4_F.forEach((f, i) => { const u = "p4" + sd + i; G.names[u] = FAC4_N[sd][i]; L = L.concat(stacksOf(mix(sd === "a" ? i : (i + 2) % 4), { weapons: tech + i % 2, shields: tech + (i + 1) % 2, armor: tech }, u)); }); return L; };
  let n = 0; for (let i = 0; i < 4; i++) for (const k in mix(i)) n += mix(i)[k] * 2;
  const res = simulate(side("a", 16), side("d", 15), { seed: 4444 }); /* at this size the titans outlast the 8 rounds, so it ends with both fleets disengaging */
  if (!S.fac4Mail) { S.fac4Mail = { t: now() }; dirty(); }
  return (G.fac4Rep = Object.assign(mkRep({ at: S.fac4Mail.t, kind: "attack", title: `Faction war · 4 vs 4 · ${n.toLocaleString("en-US")} units`, aUids: [], aName: "Coalition of the Four", dName: "Concord of the Four", lvl: 30, ptype: "lava", fortL: 0, alien: false,
    start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) }), { id: FAC4_ID, recDone: 1 }));
}
/* ---------- Mail: one inbox for battle reports,""")
rep("  if (duelOwner() && !S.labMail) { S.labMail = { t: now() }; dirty(); }", "  if (duelOwner() && !S.fac4Mail) { S.fac4Mail = { t: now() }; dirty(); } // v429 the faction war\n  if (duelOwner() && !S.labMail) { S.labMail = { t: now() }; dirty(); }")
rep("duelOwner() && S.duelMail ? [{ t: S.duelMail.t, f: \"battle\", duel: 1 }] : [], (S.spyReps", "duelOwner() && S.duelMail ? [{ t: S.duelMail.t, f: \"battle\", duel: 1 }] : [], duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: \"battle\", fac4: 1 }] : [], (S.spyReps")
rep("const list = f === \"saved\" ? (duelOwner() && S.duelMail && S.duelSaved !== 0 ? [{ t: S.duelMail.t, f: \"battle\", duel: 1 }] : [])",
    "const list = f === \"saved\" ? (duelOwner() && S.fac4Mail ? [{ t: S.fac4Mail.t, f: \"battle\", fac4: 1 }] : []).concat(duelOwner() && S.duelMail && S.duelSaved !== 0 ? [{ t: S.duelMail.t, f: \"battle\", duel: 1 }] : [])")
rep("    if (x.duel) return `", """    if (x.fac4) return `<button class="mrowc good lab" data-act="fac4Battle"><span class="mi">⚔</span><span class="mt"><b>Faction war · 4 vs 4 · 10 million units</b><small>Your private test: Terran Union, Solar Dominion, Nyx Syndicate and Verdant Collective on both sides, 1.25 million mixed warships per commander, every flagship in the fight. Tap to build it and watch (it takes a moment).</small></span><span class="mw"><time>${ago(x.t)} ago</time></span></button>`;
    if (x.duel) return `""")
rep("  labBattle: () => { if (!duelOwner()) return;", """  fac4Battle: () => { if (!duelOwner()) return; toast("Building the 4 vs 4 faction war…"); setTimeout(() => { try { playBattle(fac4Battle()); } catch (e) { toast("Couldn't build the faction war on this device.", "warn"); } }, 60); }, /* v429 */
  labBattle: () => { if (!duelOwner()) return;""")
rep("const playerFac = uid => uid === G.me ? facOf() : (", "/* v429 the faction war's eight commanders (fac4Battle) */\nconst FAC4_F = [\"terran\", \"solar\", \"nyx\", \"verdant\"], FAC4_U = {}; for (const sd of [\"a\", \"d\"]) FAC4_F.forEach((f, i) => FAC4_U[\"p4\" + sd + i] = f);\nconst playerFac = uid => uid === G.me ? facOf() : FAC4_U[uid] ? FAC4_U[uid] : (")
rep("  const pf = u => typeof u === \"string\" && u !== \"pirates\"", "  const f4 = r.id === FAC4_ID, pf = u => f4 ? FAC4_U[u] || null : typeof u === \"string\" && u !== \"pirates\"")
rep("let L = [...groups.values()].sort((x, y) => y.w - x.w).slice(0, 3);", "let L = [...groups.values()].sort((x, y) => y.w - x.w).slice(0, f4 ? 4 : 3); /* v429 the faction war shows all four */")
rep("for (const q of R.squads) { const u = q.own; if (typeof u === \"string\" && u !== \"pirates\" && u !== \"cube\" && (u === G.me || G.players[u] || isBot(u))) {",
    "for (const q of R.squads) { const u = q.own; if (typeof u === \"string\" && u !== \"pirates\" && u !== \"cube\" && (u === G.me || G.players[u] || isBot(u) || FAC4_U[u])) {")
t = t.replace("const GAME_V = 428;", "const GAME_V = 429;")
open(p, "w").write(t); print("ok")
