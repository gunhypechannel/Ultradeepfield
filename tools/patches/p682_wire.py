# v682: the Omega Cube's 3D model plays the move its battle shows (after v681 it still picked random moves)
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const BMV_ACT = { aex:', 'const BMV_ACT = { omg: { tractor: "tractor", wave: "wave", split: "burst" }, aex:')
rep('function bossAct(b, a, t) { try { const k = b.r && b.r.sbk,', 'function bossAct(b, a, t) { try { const k = bmvKey(b) || (b.r && b.r.sbk),')
rep('if (!(battle && battle.r && battle.r.sbk === key && BMV_ACT[key]))', 'if (!(battle && battle.r && (battle.r.sbk === key || bmvKey(battle) === key) && BMV_ACT[key]))')
rep('const GAME_V = 681;', 'const GAME_V = 682;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
