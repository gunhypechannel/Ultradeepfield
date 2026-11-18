# v620 the Leviathan, again (owner: "Slow the leviathan and make it half the length, fix his tail"). The ring now spans 46.5% of a lap
# (was 93%) on 60 sections (48 on the map LOD; was 110/84) so each section keeps its size; one lap round the galaxy takes 8 hours (was 4),
# its slither and drift run at half speed; and the tail tapers to a point with a vertical crescent fluke (two mirrored blades) that
# trails straight behind the body, a third of the old size, instead of the big blade that stuck out sideways.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const N = LV ? (LOD === 1 ? 84 : 110) : LOD === 1 ? 30 : 42', 'const N = LV ? (LOD === 1 ? 48 : 60) : LOD === 1 ? 30 : 42')
rep('L = TAU * .93 * k,', 'L = TAU * .465 * k,')
rep('s: TAU * .93 * R0 / M.b.N * .52 }', 's: TAU * .465 * R0 / M.b.N * .57 }')
rep('s: TAU * .93 * R0 / X.b.N * .52 }', 's: TAU * .465 * R0 / X.b.N * .57 }')
rep('TAU * T / (4 * 3600e3); o.x = Math.cos(a)', 'TAU * T / (8 * 3600e3); o.x = Math.cos(a)')
rep('Math.sin(u * TAU * 9 - t * .0024)', 'Math.sin(u * TAU * 5 - t * .0012)')
rep('Math.sin(th * 3 + t * .00017)', 'Math.sin(th * 3 + t * .00009)')
rep('Math.sin(u * TAU * 6 - t * .0017)', 'Math.sin(u * TAU * 4 - t * .0009)')
rep('sc = (RG ? RG.s * (1 - u * .55)', 'sc = (RG ? RG.s * (1 - Math.pow(u, 1.6) * .8)')
# the tail: a ring-mode fluke beside the old blade (which only the coiled Leviathan shows now)
rep('const b = new TH.Mesh(bladeGeo(8, 2.6, .35), MA); b.rotation.set(Math.PI / 2, 0, -Math.PI / 2 + .3); tail.add(b); const e = new TH.Mesh(bladeGeo(8, 2.6, .06), glowMat(ORA, .7)); e.rotation.copy(b.rotation); e.scale.set(1.01, 1.03, 1.5); tail.add(e);',
    'const b = new TH.Mesh(bladeGeo(8, 2.6, .35), MA); b.rotation.set(Math.PI / 2, 0, -Math.PI / 2 + .3); tail.add(b); const e = new TH.Mesh(bladeGeo(8, 2.6, .06), glowMat(ORA, .7)); e.rotation.copy(b.rotation); e.scale.set(1.01, 1.03, 1.5); tail.add(e);\n'
    '      const fl = new TH.Group(); fl.visible = false; tail.add(fl); tail.userData.fl = fl; tail.userData.old = [b, e]; for (const up of [1, -1]) { const f = new TH.Mesh(bladeGeo(7, 2.2, .3), MA); f.rotation.z = up * .32; f.scale.y = up; fl.add(f); const g = new TH.Mesh(bladeGeo(7, 2.2, .05), glowMat(ORA, .65)); g.rotation.z = up * .32; g.scale.set(1.01, up * 1.03, 1.4); fl.add(g); } b.userData.dyn = e.userData.dyn = 1; /* v620 the ring Leviathan\'s fluke (the old blade is kept whole so it can hide) */')
rep('tail.scale.setScalar(RG ? RG.s * .45 / 1.05 : LV ? 1 : Math.max(.001, 1 - pull(1)));',
    'tail.scale.setScalar(RG ? RG.s * .17 : LV ? 1 : Math.max(.001, 1 - pull(1))); if (tail.userData.fl) { tail.userData.fl.visible = !!RG; for (const m of tail.userData.old) m.visible = !RG; }')
s2 = re.sub(r"GAME_V = 620\b", "GAME_V = 620", s); s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
a = 'tail.position.copy(pts[N - 1]); S.v.subVectors(pts[N - 1], pts[N - 2]).normalize();'
assert s.count(a) == 1
s = s.replace(a, '{ const tn = RG ? N : N - 1; tail.position.copy(pts[tn]); S.v.subVectors(pts[tn], pts[tn - 1]).normalize(); } /* v620 the fluke sits at the very end of the spine */')
open(P, 'w', encoding='utf-8').write(s); print('ok2')
