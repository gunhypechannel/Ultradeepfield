import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# found by the unfolded-Fold online run: the worlds the Academy sends you to (the spy target, the world you scouted) keep moving
# along their orbits, so a few minutes later they slid back into uncharted space and their card lost its Espionage/Attack
# buttons; the guide looped "Close this to continue". Worlds the Academy marks stay charted until the Academy is done.
rep('''function isFogged(p, T) { if (!p || p.owner === G.me) return false;''',
    '''function isFogged(p, T) { if (!p || p.owner === G.me) return false; if (S && S.tutSee && S.tutSee.includes(p.id) && tutOn()) return false; /* v331: the Academy targets */''')
rep('''    if (p && isFogged(p[0], T)) { const q = pos(p[0], T); reveal(q.x, q.y, 24); fogSave(); } // v330: never an uncharted target''',
    '''    if (p && isFogged(p[0], T)) { const q = pos(p[0], T); reveal(q.x, q.y, 24); fogSave(); } // v330: never an uncharted target
    if (p) tutMark(p[0].id);''')
rep('''pStatus(G.byId[S.tutSpyP], now()) === "hive") { if (sheet) closeSheet();''', '''pStatus(G.byId[S.tutSpyP], now()) === "hive") { tutMark(S.tutSpyP); if (sheet) closeSheet();''')
rep('''function tutShow() {''', '''function tutMark(id) { S.tutSee = (S.tutSee || []).filter(x => x !== id).concat([id]).slice(-12); dirty(); } // v331
function tutShow() {''')
rep('''S.tutSpyP = p.id; S.tutSpyW = (S.stats || {}).hiveWins || 0;''', '''S.tutSpyP = p.id; S.tutSpyW = (S.stats || {}).hiveWins || 0; tutMark(p.id);''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
