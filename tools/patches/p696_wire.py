# v696: a stale copy could still win at sign-in (owner: "I spend void shard to bring my fleet home and now it's saying for me to spend
# shards again like they never returned home"). At 20:42 a copy of the empire from 14:19 that had sat open, not saving, on another
# device reloaded for an update and was saved over the real one. v689 made the save number decide, but only on devices that had already
# recorded one; a device opening v689+ for the first time still fell back to its "last in sync" time, which the old code kept stamping
# while it was not saving. Now a device that has no save number on record always takes the account's save (its own copy is set aside,
# as before, and can be restored from Menu > Save & data), and one that has a number takes the account's save whenever it has moved on.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const lseq = cseqGet(), take = foreign || (!behind && (S.uid === uid ? cAt > (S.cloudAt || 0) || (lseq > 0 && (+d.seq || 0) > lseq) : true)); /* v689 */',
    'const lseq = cseqGet(), take = foreign || (!behind && (S.uid === uid ? (lseq > 0 ? (+d.seq || 0) > lseq : true) : true)); /* v689; v696 the save number decides, and a device with none on record takes the account\'s save (its "last in sync" time could be stale) */')
rep('const GAME_V = 695;', 'const GAME_V = 696;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
