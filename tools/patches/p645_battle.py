# v645: battle scale by opponent (owner: "When fighting monsters your ships should be bigger, when fighting bosses smaller"):
# against monsters (map creatures, the Hive) a fleet is drawn x1.6, against the Cube or a world/super boss x0.55, so the scale of the
# enemy reads at a glance. Monsters and bosses themselves keep their size.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('const bLen = k =>', '''const bBeast = k => !!(MON[k] || BOSSK[k] || /^wb[A-Z]/.test(k));
const bBig = k => /^wb[A-Z]/.test(k) || k === "cube" || k === "worldbreaker"; /* world and super bosses, the Cube */
function bVsK(b, q) { if (!b || !q || bBeast(q.k)) return 1; const C = b.vsK || (b.vsK = {}); if (C[q.side] != null) return C[q.side];
  const foes = (b.Q || []).filter(x => x && x.side !== q.side); return (C[q.side] = foes.some(x => bBig(x.k)) ? .55 : foes.some(x => (MON[x.k] || BOSSK[x.k]) && !bBig(x.k) && x.k !== "sphere" && x.k !== "cdrone") ? 1.6 : 1); }
const bLen = k =>''')
rep('const L = Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs),',
    'const L = Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs * bVsK(b, q)), /* v645 */')
# "Next on your path": "Build an Armageddon", and requirement tags never split across lines (a tag broke as "Hyperspace Drive / 8/12")
rep('<span class="nm">${m.kind === "r" ? "Research" : "Build a"} ${esc(m.n)}', '<span class="nm">${m.kind === "r" ? "Research" : /^[aeiou]/i.test(m.n) ? "Build an" : "Build a"} ${esc(m.n)}')
rep('.chipq{font-size:11.5px;padding:2px 6px;', '.chipq{display:inline-block;white-space:nowrap;margin:2px 4px 2px 0;font-size:11.5px;padding:2px 6px;')
open(p, 'w', encoding='utf-8').write(s)
