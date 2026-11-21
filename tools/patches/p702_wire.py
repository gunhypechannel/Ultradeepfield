# v702: the Shard Colossus stays put on the map (owner: "Its impossible to click on a stone golem, they shouldn't really move in map
# mode only float in place"). It rode its crystal mine round the galaxy with the mine's orbit; now it stands where the mine was when
# its week began and only bobs gently, so it can be tapped. A tap on any world boss now wins over the worlds beside it (the Colossus sat 14 units from its own mine, which kept taking the tap).
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const q = P3(WB_MINE[hash("col" + c2) % WB_MINE.length], T, WBS), r = Math.hypot(q.x, q.z) || 1; o.x = q.x - q.x / r * 14; o.z = q.z - q.z / r * 14; o.y = q.y; return o; }',
    'const q = P3(WB_MINE[hash("col" + c2) % WB_MINE.length], WB2_BASE + c2 * WEEK, WBS), r = Math.hypot(q.x, q.z) || 1; o.x = q.x - q.x / r * 14; o.z = q.z - q.z / r * 14; o.y = q.y + 1.2 * Math.sin(T / 4e5); return o; } /* v702 it stays where its mine was when the week began, bobbing in place */')
rep('hits.push({ wb: key, x: s[0], y: s[1], sr: Math.max(sr, 14) });', 'hits.push({ wb: key, x: s[0], y: s[1], sr: Math.max(sr, 22), prio: 1 }); /* v702 a tap on a world boss wins over the worlds beside it */')
rep('const GAME_V = 701;', 'const GAME_V = 702;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
