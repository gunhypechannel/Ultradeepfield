# v338: commanders who finished the Academy before v336 never got the economy steps (D O O M: Solar Lv.1, power at -119).
# A finished commander whose homeworld is below the pattern is taken through the nine economy steps once, then back to done.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('  if (!S.tutTabs0) {', '''  if (!S.tutEconBk0) { S.tutEconBk0 = 1; const j = TUT.findIndex(s => s.id === "econ-solar5"); if (j >= 0 && S.tut.i >= TUT.length && !S.tut.off && TUT.slice(j, j + 9).some(s => !s.ok(S))) { S.tut.i = j; S.tut.k = "econ-solar5"; S.tutEconBack = 1; S.tut.open = 1; S.advHop = 0; } dirty(); } /* v338 */
  if (!S.tutTabs0) {''')
rep('''  S.tut.i++; S.tut.open = 0; dirty(); try { SFX.research(); } catch (e) {} // v81''', '''  S.tut.i++; if (S.tutEconBack && st.id === "econ-radar") { S.tut.i = TUT.length; delete S.tutEconBack; S.say.push("That's our homeworld balanced, Commander. Keep this order on every world we settle: power, metal, crystal, gas, storage, radar."); } /* v338: back to where they were */ S.tut.open = 0; dirty(); try { SFX.research(); } catch (e) {} // v81''')
rep('S.tut.i++; if (S.tutEconBack && st.id === "econ-radar") { S.tut.i = TUT.length; delete S.tutEconBack;', 'S.tut.i++; const back = S.tutEconBack && st.id === "econ-radar"; if (back) { S.tut.i = TUT.length; delete S.tutEconBack;')
rep('  if (nx) toast(`Academy step done:', '  if (nx || back) toast(`Academy step done:')
rep('  else { S.retGift = { at: now() + 8 * 3600e3', '  if (!nx && !back) { S.retGift = { at: now() + 8 * 3600e3')
rep('if (j >= 0 && S.tut.i >= TUT.length && !S.tut.off &&', 'if (j >= 0 && (S.tut.i >= TUT.length || S.tut.k === "done") && !S.tut.off &&')
rep('if (!G.tutFound) { G.tutFound = 1; const k = S.tut.k,', 'if (!G.tutFound) { G.tutFound = 1; if (S.tut.k === "done" && S.tut.i < TUT.length) { S.tut.i = TUT.length; dirty(); } /* v337: a finished Academy stays finished when steps are added (v336 pulled finished commanders back to step 40) */ const k = S.tut.k,')
open(p, 'w', encoding='utf-8').write(t); print('ok')
