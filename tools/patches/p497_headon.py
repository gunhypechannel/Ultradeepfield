# v497 (owner): every boss and super boss battle report stays head-on, except the Omega Cube and Aexion. For all others the camera
# sits straight in front (no sideways offset, looking at the boss's centre line) and the boss no longer swings up to 45 degrees
# toward the squadrons it strikes; its attacks still cross the screen. The Omega Cube and Aexion keep the angled camera and the turn.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const WB_FRONT = {', 'const WB_SWING = { omega: 1, aexion: 1 }; /* v497 the only bosses whose battle camera is angled and who turn to their targets */\nconst WB_FRONT = {')
rep('WBR.key = key; WBR.tall = tall; WBR.cam.position.set(...(tall ? [V0[1][0] * .2, V0[1][1] * .6, Math.hypot(V0[1][0], V0[1][2])] : V0[1])); WBR.cam.lookAt(new TH.Vector3(...V0[2]));',
    'WBR.key = key; WBR.tall = tall; WBR.swing = !!WB_SWING[m3]; WBR.cam.position.set(...(tall ? [WBR.swing ? V0[1][0] * .2 : 0, V0[1][1] * .6, Math.hypot(V0[1][0], V0[1][2])] : V0[1])); WBR.cam.lookAt(new TH.Vector3(WBR.swing ? V0[2][0] : 0, V0[2][1], V0[2][2]));')
rep('goal = WBR.y0 + (WBR.b.art ? 0 : (WBR.face || 0)) * Math.PI / 4;', 'goal = WBR.y0 + (WBR.b.art || !WBR.swing ? 0 : (WBR.face || 0)) * Math.PI / 4;')
s = re.sub(r"GAME_V = 496\b", "GAME_V = 497", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
