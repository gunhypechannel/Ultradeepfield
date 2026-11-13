# v528 the monster battle changes the owner wanted kept (v523), without the line formation: space monsters drawn 35% bigger in battle
# replays, and the Solar Moth seen from its back, head up and wings spread (BOSSK.smoth 2.4).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 : Math.pow(SIDE_LEN[k] || .5, 1.15) * (BOSSK[k] || 1);\n',
    'const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 : Math.pow(SIDE_LEN[k] || .5, 1.15) * (BOSSK[k] || 1);\nfor (const k in MON) BOSSK[k] = (BOSSK[k] || 1) * 1.35; BOSSK.snest = (BOSSK.snest || 1) * 1.35; /* v528 space monsters loom larger in battle */\n')
rep('if (k === "smoth" && view === "side") ship.rotation.x = 1.15; /* v522 the Solar Moth shows its wings in battle, not their edge */', 'if (k === "smoth" && view === "side") { ship.rotation.order = "ZYX"; ship.rotation.set(Math.PI / 2, 0, Math.PI / 2); } /* v528 its back: head up, wings spread */')
rep('smoth: 1.6, cram: 1.8 },', 'smoth: 2.4, cram: 1.8 },')
s2 = re.sub(r"GAME_V = 527\b", "GAME_V = 528", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
