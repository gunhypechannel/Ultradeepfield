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

# --- v497 Aexion (owner): "when he slashes his blade an energy wave is released": at the moment of the cut a crescent of blade light
# leaves the sword's arc and flies out toward the fleet, widening and fading (two alternate, so back-to-back slashes each get one) ---
s = open(P, encoding='utf-8').read()
rep('const arcM = new TH.Mesh(new TH.RingGeometry(14, 17, 48, 1, 0, Math.PI * .9), glowMat(0x9ad8ff, 0)); arcM.userData.dyn = 1; arcM.visible = false; body.add(arcM);',
    'const arcM = new TH.Mesh(new TH.RingGeometry(14, 17, 48, 1, 0, Math.PI * .9), glowMat(0x9ad8ff, 0)); arcM.userData.dyn = 1; arcM.visible = false; body.add(arcM);\n'
    '    const bwv = [0, 1].map(() => { const g = new TH.Group(), a = new TH.Mesh(new TH.RingGeometry(13, 18, 64, 1, 0, Math.PI * .9), glowMat(0x9ad8ff, 0)), c = new TH.Mesh(new TH.RingGeometry(15, 16.2, 64, 1, .05, Math.PI * .8), glowMat(0xf2fbff, 0)); g.add(a, c); g.visible = false; g.userData.dyn = 1; body.add(g); return { g, a, c, t0: -1e9 }; }); let bwI = 0; /* v497 the blade\'s energy wave */')
rep('arcM.visible = fb >= 0 && u > .99 && !out.swordGone; if (arcM.visible) {',
    '''{ const cut = fb >= 0 && u > .99 && !out.swordGone && fb >= .46 && (out._bwp == null || out._bwp < .46); out._bwp = fb >= 0 ? fb : null;
        if (cut) { const W = bwv[bwI++ % 2]; W.t0 = t; W.g.rotation.set(-.15, 0, -.95 * arms[1].sx + Math.PI * .05); }
        for (const W of bwv) { const e = (t - W.t0) / 1300; W.g.visible = e >= 0 && e < 1; if (!W.g.visible) continue; const k = 1 - e;
          W.g.position.set(arms[1].sx * 3 * k - e * 6, 6 - e * 16, 6 + e * 46); W.g.scale.setScalar(1.6 + e * 2.6); W.a.material.opacity = Math.pow(k, 1.3) * .95; W.c.material.opacity = Math.pow(k, 2) * (.9 + .1 * Math.sin(t * .05)); } }
      arcM.visible = fb >= 0 && u > .99 && !out.swordGone; if (arcM.visible) {''')
open(P, 'w', encoding='utf-8').write(s)

# --- v497 Aexion's Warform stands higher and larger above the fleet (owner: "too low now, needs to be high") ---
s = open(P, encoding='utf-8').read()
rep('aexW: [-.4, [-26, 16, 70], [0, 21, 0]]', 'aexW: [-.4, [-24, 16, 64], [0, 11, 0]] /* v497 higher above the fleet, whole */')
rep('W.g.scale.setScalar(1.6 + e * 2.6); W.a.material.opacity = Math.pow(k, 1.3) * .95;', 'W.g.scale.setScalar(.5 + e * 1.6); W.a.material.opacity = Math.min(1, Math.pow(k, 1.1) * 1.3);')
open(P, 'w', encoding='utf-8').write(s)
