# v655 owner grants can carry Titan Cores (owner: "Give owner account 100 titan cores"). pkApply takes contents.tcore; a grant meant only
# for v655+ also carries mats: [null], which makes an older client stop before it marks the grant delivered (so it can't swallow it),
# and this client ignores malformed mats entries. Grants from the hidden "owner_gift" pack are named Owner gift.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('function pkApply(c, sign) { const got = [];', 'function pkApply(c, sign) { const got = []; if (c.tcore) { S.tcore = Math.max(0, (S.tcore || 0) + sign * c.tcore); got.push(`${fmt(c.tcore)} Titan Cores`); } /* v655 */')
rep('  const mats = c.mats || []; if (mats.length) {', '  const mats = (Array.isArray(c.mats) ? c.mats : []).filter(Array.isArray); if (mats.length) {')
rep('nm = P ? P.name : g.pack_id;', 'nm = P ? P.name : g.pack_id === "owner_gift" ? "Owner gift" : g.pack_id;')
rep('const GAME_V = 654', 'const GAME_V = 655')
open(p, 'w', encoding='utf-8').write(s)
