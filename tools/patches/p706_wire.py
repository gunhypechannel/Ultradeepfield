# v706: the story rounded out (see p706_story.js and the v706 notes in p704_crc.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def block(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1; s = s[:i] + new + s[j:]
block('/* ---------- v703/v704 TIDE OF THE CARCINID', 'const PIRATES = PIRATES_ALL', R('p704_crc.js').rstrip('\n') + '\n')
block('/* ---------- v703/v704 the Carcinid on the battle screen and the map', 'function mimAtkAdd(b, v) {', R('p704_crcm.js').rstrip('\n') + '\n')
rep('setInterval(() => { try { crcWeekSay(); } catch (e) {} }, 20000);', 'setInterval(() => { try { crcWeekSay(); } catch (e) {} }, 20000);\n' + R('p706_story.js').rstrip('\n'))

# 1. the order: the Mimic no longer runs in the Countdown (December). Its first run is the Season of the Mimic, where Chapter 5 (the Vault
#    Seal) explains Omega; December belongs to the Countdown, and January to the Leviathan and the Carcinid. No more back-to-back invasions.
rep('const MIM_RUN = k => k === 1 || (k >= PRO && seaCyc(k) === 4);', 'const MIM_RUN = k => k >= PRO && seaCyc(k) === 4; /* v706 no longer in the Countdown: two four-week invasions back to back (Mimic in December, the Carcinid in January) */')
rep('if (MIM_RUN(k) && VP_BASE + k * VP_LEN + MIM_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + VP_LEN; }', 'if (MIM_RUN(k) && VP_BASE + k * VP_LEN + MIM_LEN > T) return VP_BASE + k * VP_LEN; return VP_BASE + (PRO + 4) * VP_LEN; }')

# 2. Chapter 5 is Omega now, not the Kraken: the lines around it said otherwise
rep('"krk": {}, "wym": {"prevH": "Previously: the Kraken sank back into the deep, and the fifth seal held. But the black hole has started to dim.", "prevC": "Previously: the Kraken escaped with its arms intact, and the fifth seal cracked. Now the black hole is dimming.",',
    '"krk": {"prevH": "Previously: the Matriarch died, and Vael\'Khor\'s ritual failed. But the Cube network is drawing power from something below it.", "prevC": "Previously: Vael\'Khor\'s ritual broke the fourth seal. Now the Cube network is drawing power from something below it."}, "wym": {"prevH": "Previously: Omega fell in its vault, and the fifth seal held. But the black hole has started to dim.", "prevC": "Previously: a fragment of Omega escaped into the Cube network, and the fifth seal cracked. Now the black hole is dimming.",')
rep('"sting": "Commander, the deep layers... the lights down there are going out. One sector at a time."', '"sting": "Commander, the Cube network is drawing power from somewhere below it. Something beneath the Cubes is pushing on a door."')

# 3. Chapter 6 is the Eclipse's rehearsal, not "Eclipse": the name belongs to the year's end
rep('"wym": {"ch": 6, "typ": "wb", "n": "Eclipse", "chap": "The Door"', '"wym": {"ch": 6, "typ": "wb", "n": "The Dark Rehearsal", "chap": "The Door"')
rep('[1800000.0, "eclipse", "Eclipse", "The light is swallowed completely."]', '[1800000.0, "eclipse", "Total Darkness", "The light is swallowed completely: a rehearsal for the Eclipse at the year\'s end."]')
rep('"eclipse": "Eclipse. It\'s swallowed the light completely. This is what the Testament warned us about."', '"eclipse": "It\'s swallowed the light completely. This is what the Testament warned us about, Commander. A rehearsal for the real Eclipse."')
rep('Its Eclipse is a rehearsal: for a few hours the galaxy sees what the real night will look like.', 'Its darkness is a rehearsal: for a few hours the galaxy sees what the real Eclipse will look like, and the door the last gate protects.')
# the door before the gate: the Wyrm showed us the door; the gate is the last thing in front of it
rep('Khezaroth guards the last gate before the door. Its trial is a question the Architects asked every age, and the answer was always the same: someone must hold the door.',
    'Khezaroth guards the last gate before the door the Wyrm showed us in the dark. Its trial is a question the Architects asked every age, and the answer was always the same: someone must hold the door.')

# 4. the Crown's ending weighs on the year: an escaped Crown costs a held seal at the verdict and adds to the Seal Strain
rep('function eclHeld(s0) { try { return finLedger(s0).filter(x => x.st === "held").length; } catch (e) { return 0; } }',
    'function eclHeld(s0) { try { return Math.max(0, finLedger(s0).filter(x => x.st === "held").length - (crcYearOutcome(s0 || now()) === "esc" ? 1 : 0)); /* v706 the Crown reborn cracks the seal over the deep */ } catch (e) { return 0; } }')
rep('  try { for (const L of finLedger()) P += L.st === "cracked" ? 12 : L.st === "held" ? 4 : 0; } catch (e) {} return P; }',
    '  try { for (const L of finLedger()) P += L.st === "cracked" ? 12 : L.st === "held" ? 4 : 0; } catch (e) {} try { const c = crcYearOutcome(now()); P += c === "esc" ? 12 : c === "win" ? 4 : 0; } catch (e) {} /* v706 the Crown */ return P; }')

# 5. the tide's Archive records (q_) show their paintings and don't count toward the Testament's lore cards
rep('if (/^[ahdxm]_/.test(k) && E.img)', 'if (/^[ahdxmq]_/.test(k) && E.img)')
rep('!/^[bslecoahdxmt]_/.test(q)', '!/^[bslecoahdxmtq]_/.test(q)')

# 6. the Lab: preview the Leviathan's fate
rep('  crcLabWeek: d =>', '  crcLabLev: d => { if (!duelOwner()) return; S.crcPrev = Object.assign(S.crcPrev || { w: 4, at: now() }, { lev: d.k }); CSC = {}; dirty(); toast(`Preview: the Leviathan ${d.k === "dead" ? "was slain at the wall" : "escaped its hunt"}.`); renderSheet(); },\n  crcLabWeek: d =>')
rep("S.crcPrev = w ? { w, at: now() } : null; CSC = {}; dirty(); toast(w ? `Previewing ${w === 5", "S.crcPrev = w ? { w, at: now(), lev: (S.crcPrev || {}).lev } : null; CSC = {}; dirty(); toast(w ? `Previewing ${w === 5")
rep('.crcart{', '.crcfate{color:#e8c890;margin:4px 0 0}\n.crcart{')
rep('const GAME_V = 705;', 'const GAME_V = 706;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
