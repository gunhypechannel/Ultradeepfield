# fb-20261119 (2): the owner's iPhone (v651) was closed with "memory ~271 MB (map 0, base 186, studio 74 ...)" after seven monster-hunt
# replays in a row: 110 cached ship/monster pictures (74 MB) although iOS keeps at most 48 battle + 32 other pictures.
# Cause: iOS drops the picture studio 800 ms after every battle closes (v580) and keeps its picture cache (G.stuCache), but the
# lists that say which pictures are oldest (S.order / S.orderSide) lived on the studio and were lost, so the rebuilt studio never
# evicted any picture from earlier battles. v651's monster loops (10 frames per monster) made the pile grow much faster.
# studio() now rebuilds both lists from the kept cache and trims it to the usual caps at once.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('    STU = { cv, renderer, scene, camera: new TH.PerspectiveCamera(28, 2, .1, 400), cache: G.stuCache || {}, tex: null, key };\n',
  '    STU = { cv, renderer, scene, camera: new TH.PerspectiveCamera(28, 2, .1, 400), cache: G.stuCache || {}, tex: null, key };\n'
  '    try { const C = STU.cache, o = [], os = []; for (const k in C) { const c = C[k]; if (c && c.getContext) (k.endsWith("|side") ? os : o).push(k); } /* fb-20261119 a kept cache keeps its eviction order */\n'
  '      for (const [L, n] of [[os, IOS ? 48 : MOBILE ? 64 : 96], [o, IOS ? 32 : 48]]) { let i = 0; while (L.length > n && i < L.length) { const k = L[i]; if (ART_LIVE.has(k)) { i++; continue; } L.splice(i, 1); const c = C[k]; if (c && c.getContext) { c.width = c.height = 0; c._mip = null; } delete C[k]; } }\n'
  '      STU.order = o; STU.orderSide = os; } catch (e) {}\n'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
