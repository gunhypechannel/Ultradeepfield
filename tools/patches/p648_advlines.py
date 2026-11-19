# v648: spoken welcomes for the Premium page and the Sanctuary (owner: "voice advisor for premium player section", "voice lines for
# sanctuary"), and the captain line made fixed so it can be voiced.
import sys, json
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
PREM = ["Welcome to the premium deck, Commander. This is where our supporters' worlds and warships get their finest looks.",
        "Every tier unlocks planet skins, hull finishes and bonuses that never expire. The higher the tier, the rarer the finish.",
        "Pick a ship, plate it in a finish, then give it a trim. Every commander who sees our fleet will know exactly who we are."]
SANCT = ["Welcome to the Xeno Sanctuary, Commander. Every egg we bring home from a hunt can hatch here.",
         "Raise them, and each one makes its element stronger. Pair the right two in the breeding chamber, and we might bring back a species the galaxy thought was gone."]
# the Premium page: the spoken welcome replaces the one-line greeting
rep('function advFirst(k) { try {', 'const ADV_SAY1 = ' + json.dumps({"premium": PREM, "sanct": SANCT}, ensure_ascii=False) + ''';
function advSay1(k) { try { if (!S || !G.ready || !ADV_SAY1[k] || tutOn()) return false; S.advOnce = S.advOnce || {}; if (S.advOnce["s_" + k]) return false; S.advOnce["s_" + k] = S.advOnce["f_" + k] = now(); dirty(); setTimeout(() => { try { say(ADV_SAY1[k].slice()); } catch (e) {} }, 900); return true; } catch (e) { return false; } }
function advFirst(k) { if (advSay1(k)) return; try {''')
# the Sanctuary tab opens with the welcome, once
rep('function sanctCard() { const X = xsOf(), L = xsLvl(), T = now(), slots = xsIncN(L), cap = xsCap(L);', 'function sanctCard() { const X = xsOf(), L = xsLvl(), T = now(), slots = xsIncN(L), cap = xsCap(L); if (L) advSay1("sanct");')
rep('try { advHolo(`${capName(d.k)} reporting, Commander. Give them a fleet and they\'ll earn their keep.`, true); } catch (e) {}', 'try { advHolo("Your new captain is reporting for duty, Commander. Give them a fleet and they\'ll earn their keep.", true); } catch (e) {}')
rep('const GAME_V = 647', 'const GAME_V = 648')
open(p, 'w', encoding='utf-8').write(s)
