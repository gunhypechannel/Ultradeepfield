# v579 The Eclipse (owner: "Complete all"; the open story choice was decided as: the verdict depends on how many of the year's ten
# seals held, three outcomes, see p579_eclipse.js). Every year, the Sunday after the tenth seal (Medusara's finale week), 18:00 UTC,
# 45 minutes: The Silence, The Weighing, The Verdict. Archives: Chapter 11, The Verdict. Boss Lab: preview each verdict.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
J = lambda o: json.dumps(o, ensure_ascii=False)
M = 60e3
EV = {"ecl": {"ch": 11, "typ": "eclipse", "n": "The Eclipse", "chap": "The Verdict", "ic": "◐", "col": "#d8c8ff", "set": 45 * M,
  "d": "The year's end. The black hole goes silent, and the Judge weighs every seal the galaxy held or lost, then gives his verdict.",
  "st": [[0, "silence", "The Silence", "The black hole's light goes out, and the galaxy dims."], [10 * M, "weigh", "The Weighing", "A column of light rises where each of the year's ten chapters was fought: gold for a seal held, red for a seal cracked."], [30 * M, "verdict", "The Verdict", "Seven or more seals held: Worthy. Four to six: Weighed. Three or fewer: Found Wanting."]]}}
SAY = {"silence": ["Commander... the black hole has gone silent. No signal, no light. This is the Eclipse.", "grave"],
       "weigh": ["The Judge is moving. He's weighing every seal we held, and every seal we lost. One by one.", "awe"]}
ECL = {"worthy": [["His hand is closing gently around the Cube. Golden light, Commander. He found us worthy. We held the line.", "tender"], ["Whatever comes next, Commander, the galaxy knows what we are now.", "warm"]],
       "weighed": [["He's holding the Cube still. Not a blessing, not a sentence. He's giving us another year to prove ourselves.", "grave"], ["Another year. Every seal counts. Let's make them all hold.", "calm"]],
       "wanting": [["His eyes are red, Commander. We were found wanting. Something is bleeding through the black hole... the Unmade is closer than ever.", "grave"], ["We have one year to undo this. I won't let it end like this. I promise you.", "tender"]]}
ARCH = {"c_11": {"cat": "saga", "t": "Chapter 11: The Verdict", "era": "Season 12 · the year's end", "civ": "The Seal Ledger", "loc": "The black hole", "img": "art/celestial.jpg", "th": "The Ten Seals",
  "frag": "When the last seal is tried, the door goes quiet, and the one who holds the scales looks up.",
  "interp": "At the end of every year the black hole falls silent: the Eclipse. The Judge, the Architects' last Warden, weighs the Seal Ledger and gives his verdict on the whole galaxy. Held seals earn his favour. Cracked seals let the Unmade lean closer to the door.",
  "adv": "He doesn't judge one commander. He judges all of us together. That's the part I find hardest, and the part I find most beautiful.",
  "enc": ["Commander, a new chapter just opened in the Archives. The year is ending.", "The black hole has gone silent. The Judge is about to give his verdict."],
  "def": ["The verdict is given, Commander.", "And next year, the Leviathan returns to the wall. The story starts again, with everything we've learned."]}}
MOOD = {}
for x, m in SAY.values(): MOOD[x] = m
for v in ECL.values():
    for x, m in v: MOOD[x] = m
for x in ARCH["c_11"]["enc"]: MOOD[x] = "awe"
for x in ARCH["c_11"]["def"]: MOOD[x] = "grave"
MOOD[ARCH["c_11"]["adv"]] = "tender"
JS = ('Object.assign(FIN_EV, ' + J({k: dict(v, set=v["set"], st=[[a, b, c, d] for a, b, c, d in v["st"]]) for k, v in EV.items()}) + '); FIN_SAY.ecl = ' + J({k: v[0] for k, v in SAY.items()}) + ';\n'
      'const ECL_SAY = ' + J({k: [x[0] for x in v] for k, v in ECL.items()}) + ';\n' + open('tools/patches/p579_eclipse.js', encoding='utf-8').read())
i = s.find('function shFinale() {'); assert i > 0
s = s[:i] + JS + s[i:]
# the calendar: the Sunday after the tenth seal's Wednesday, every year
rep('if (D.typ === "omen") { const wed = ROT0 + (4 * D.si + 2) * WEEK; return [wed, wed + D.set, wed + D.set + 60e3]; }',
    'if (D.typ === "omen") { const wed = ROT0 + (4 * D.si + 2) * WEEK; return [wed, wed + D.set, wed + D.set + 60e3]; } if (D.typ === "eclipse") { const sun = ROTS0 + (4 * (PRO + 9 + 10 * n) + 2) * WEEK + 864e5; return [sun, sun + D.set, sun + D.set + 60e3]; } /* v579 */')
rep('const finKeys = () => Object.keys(FIN_EV).filter(k => FIN_EV[k].typ !== "omen")', 'const finKeys = () => Object.keys(FIN_EV).filter(k => FIN_EV[k].typ !== "omen" && FIN_EV[k].typ !== "eclipse")')
rep('if (D.typ === "omen") continue;', 'if (D.typ === "omen" || D.typ === "eclipse") continue;')
rep('if (D.typ === "omen") { const a = 2.2,', 'if (D.typ === "eclipse") return { x: 0, y: 0, z: 0 }; if (D.typ === "omen") { const a = 2.2,')
rep('fight = F.e >= D.set && D.typ !== "omen",', 'fight = F.e >= D.set && D.typ !== "omen" && D.typ !== "eclipse",')
rep('data-act="${D.typ === "omen" ? "finWatch" : "finOpen"}"', 'data-act="${D.typ === "omen" || D.typ === "eclipse" ? "finWatch" : "finOpen"}"')
rep('finOpen: d => FIN_EV[d.k] && FIN_EV[d.k].typ === "omen" ? finWatchGo(d.k)', 'finOpen: d => FIN_EV[d.k] && (FIN_EV[d.k].typ === "omen" || FIN_EV[d.k].typ === "eclipse") ? finWatchGo(d.k)')
rep('(om || all || (T - s0 < FIN_YEAR && finOutcome(k, s0, T) === "cracked"))', '(om || all || (T - s0 < FIN_YEAR && (k === "ecl" ? eclVerdict(s0) === "wanting" : finOutcome(k, s0, T) === "cracked")))')
# the Judge in the Eclipse
rep('if (F && F.k === "om2") {', 'G.jbV = F && F.k === "ecl" && F.e >= FIN_EV.ecl.st[2][0] ? eclVerdict(F.s0) : null; if (F && F.k === "ecl") { const E = FIN_EV.ecl.st; b = F.e < E[1][0] ? 0 : F.e < E[2][0] ? .35 : 1; } else if (F && F.k === "om2") {')
rep('J.glow.s.material.opacity = ', 'J.glow.s.material.color.setHex(G.jbV ? ECL_COL[G.jbV] : 0xffffff); /* v579 his eyes take the verdict\'s colour */ J.glow.s.material.opacity = ')
# the Events hub: Season 12's card names the Eclipse too
rep('esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div></div>`; } catch (e) { return ""; } }',
    'esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div>${x === 9 ? `<div class="finrow" data-act="finWatch" data-k="ecl"><span>◐ The Eclipse · The Verdict</span><em>${when(sat + 864e5)}</em></div>` : ""}</div>`; } catch (e) { return ""; } }')
# the Boss Lab
rep("const ch = finKeys().map(k => {", "const eclRow = row(\"◐\", \"The Eclipse · The Verdict\", `The year's end · ${d(finWinOf(\"ecl\", 0)[0])} · 45 min (preview: 2 min) · the verdict follows the Ledger`, b(\"labEcl\", \"worthy\", \"▶ Worthy\") + b(\"labEcl\", \"weighed\", \"▶ Weighed\") + b(\"labEcl\", \"wanting\", \"▶ Wanting\"));\n  const ch = finKeys().map(k => {")
rep('return sec("The Omens (Seasons 1 and 2)", om) + sec("The Ten Seals (Seasons 3 to 12)", ch) +', 'return sec("The Omens (Seasons 1 and 2)", om) + sec("The Ten Seals (Seasons 3 to 12)", ch + eclRow) +')
rep('  labScars: () => {', '  labEcl: d => { if (!duelOwner()) return; labReset(); G.eclForce = d.k; finSimStart("ecl"); }, /* v579 */\n  labScars: () => {')
# the Archives
rep('); /* v575 The Omens */\nconst ARCH_ORD = [', '); Object.assign(ARCH, ' + J(ARCH) + '); /* v579 The Eclipse */\nconst ARCH_ORD = [')
rep('"c_10", "o_1"', '"c_10", "c_11", "o_1"')
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
rep('J.lid = lay(1, 1); J.glow = lay(0, 2); J.held = lay(0, 3); J.crk = lay(0, 3); J.live = lay(0, 3); }',
    'J.lid = lay(1, 1); J.glow = lay(0, 2); J.held = lay(0, 3); J.crk = lay(0, 3); J.live = lay(0, 3); J.lidAll = lay(1, 1.5); JUDGE_EYE.forEach(([px, py]) => { const x = J.lidAll.x, g = x.createRadialGradient(px / 2, py / 2, 0, px / 2, py / 2, 10); g.addColorStop(0, "rgba(2,4,3,1)"); g.addColorStop(.6, "rgba(2,4,3,.95)"); g.addColorStop(1, "rgba(2,4,3,0)"); x.fillStyle = g; x.beginPath(); x.arc(px / 2, py / 2, 10, 0, TAU); x.fill(); }); J.lidAll.tx.needsUpdate = true; } /* v579 the verdict recolours his eyes: the painted green is covered first */')
rep('J.glow.s.material.color.setHex(G.jbV ? ECL_COL[G.jbV] : 0xffffff);', 'J.glow.s.material.color.setHex(G.jbV ? ECL_COL[G.jbV] : 0xffffff); if (J.lidAll) J.lidAll.s.material.opacity = G.jbV ? e : 0;')
open(P, 'w', encoding='utf-8').write(s); print('ok')
