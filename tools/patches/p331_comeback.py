import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# a one-time welcome-back supply drop for commanders who come back to an unfinished Academy after a day or more away
rep('''  const idx = S.log.indexOf(before), n = idx < 0 ? S.log.length : idx;''',
    '''  G.awayMs = away; // v331: how long since this save was last played (the cloud save corrects it once checked)
  const idx = S.log.indexOf(before), n = idx < 0 ? S.log.length : idx;''')
rep('''            S = migrate(cs); S.cloudAt = cAt;''', '''            G.awayMs = cs.t ? now() - cs.t : 0; S = migrate(cs); S.cloudAt = cAt;''')
rep('''    if (G.oldWait) oldOffer(); else if (G.askFac) G.askFac();''',
    '''    comeback(); if (G.oldWait) oldOffer(); else if (G.askFac) G.askFac();''')
rep('''function intro() {''', '''function comeback() { if (!S || S.comeback || !tutOn() || !(S.tut.i > 0) || !(G.awayMs >= 864e5)) return; S.comeback = 1; // v331
  const rw = { m: 8000, c: 5000, g: 2500, shards: 5, boosts: 3 }; grantRw(rw, "Welcome back"); dirty();
  celebrate({ k: "comeback", kick: "Welcome back, Commander", t: "Supplies Have Landed", art: "adv", s: `The Academy is right where you left it: step ${S.tut.i + 1} of ${TUT.length}. Fleet Command sent supplies to get you moving again.`, rw: "8,000 metal, 5,000 crystal, 2,500 gas, ◆5 and ⚡3 boosts. Already in your stores.", go: "Let's go" }); }
function intro() {''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 331", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v331 from', v)
