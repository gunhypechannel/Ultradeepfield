# v694: the Leviathan's head no longer rolls upside down (owner: "The leviathans head turns upside and looks silly"). The head was
# aimed along its neck with the shortest rotation from straight ahead, which leaves the roll to chance: as the neck swung round, the
# head rolled over with its horns underneath. It is now aimed with its crown kept up (the same model serves the Event Horizon Wyrm).
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const mv = moves({ coil: 3000, lens: 3000, sweep: 2200, hit: 520 }), hit = hitKit(body, shk); const S = scr(), c1 = new TH.Color(), tmp = V(0, 0, 0);',
    'const mv = moves({ coil: 3000, lens: 3000, sweep: 2200, hit: 520 }), hit = hitKit(body, shk); const S = scr(), c1 = new TH.Color(), tmp = V(0, 0, 0);\n'
    '    const hM = new TH.Matrix4(), hX = V(1, 0, 0), hY = V(0, 1, 0), hUP = V(0, 1, 0), aimUp = (q, z) => { const px = hX.x, pz = hX.z; hX.crossVectors(hUP, z); if (hX.lengthSq() < 1e-4) hX.set(px, 0, pz); hX.normalize(); hY.crossVectors(z, hX); hM.makeBasis(hX, hY, z); q.setFromRotationMatrix(hM); }; /* v694 aim the head with its crown up (no roll) */')
rep('head.quaternion.setFromUnitVectors(S.Z, S.v)', 'aimUp(head.quaternion, S.v)', 3)
rep('const GAME_V = 693;', 'const GAME_V = 694;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
