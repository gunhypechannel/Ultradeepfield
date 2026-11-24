# The Continuum Dreadnought, after art/rwar/c_dreadnought.webp: a massive armoured wedge with a lance prow, a citadel bridge and rows of
# twin-gun turrets along its back, a great reactor ring with a red eye on each flank, crimson trenches along its sides, swept blades
# below, and a stern of heavy engines.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: np.maximum(hull(p, [(3.4, 0), (1.8, .7), (-2.6, .95), (-3.3, .8), (-3.3, 0)], .7, -.6, .2), profile(p, [(3.6, -.1), (1.4, .7), (-3.4, .72), (-3.4, -.62), (1.4, -.6)]))
M = Model((-3.9, -1.95, -1.75), (4.1, 1.95, 1.75), float(sys.argv[2]) if len(sys.argv) > 2 else .035)
M.add('body', body, HULL)
M.add('lance', lambda p: hull(p, [(3.95, 0), (2.6, .18), (1.6, .26), (1.6, 0)], .14, -.12, .06), PLATE, .04)
M.add('deck', lambda p: hull(p, [(2.4, 0), (1.2, .5), (-2.6, .62), (-2.9, 0)], 1.0, .6, .14), PLATE, .05)
M.add('bridge', lambda p: hull(p, [(-.6, 0), (-1.0, .32), (-2.0, .36), (-2.2, 0)], 1.55, .9, .14), HULL, .05)
M.add('bridgeT', lambda p: spike(p, (-1.5, 1.5, 0), (-1.6, 1.95, 0), .12), GUN)
M.add('keel', lambda p: hull(p, [(2.4, 0), (1.2, .5), (-2.4, .6), (-2.8, 0)], -.5, -.85, .12), BLACK, .04)
for s in (1, -1):
    for j, (x0, y0, L, w) in enumerate([(1.6, .45, 2.0, .45), (.2, .05, 2.4, .6), (1.3, -.4, 2.1, .5), (-1.4, .45, 1.8, .5), (-1.2, -.4, 1.8, .55), (-2.6, .05, 1.4, .45)]):
        M.add(f'bl{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: prism(p, [(x0 + L, (.9 + w) * s), (x0 + .2, (.7 + w * .55) * s), (x0 - .3, .65 * s), (x0 + .5, .65 * s)], y0 + .045, y0 - .045, .025, .012), PLATE)
        M.carve(f'blr{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: box(p, (x0 + L * .42, y0 + .05, (.78 + w * .55) * s), (L * .26, .018, .035), 0, rot('y', -np.arctan2(w * .45, L * .8) * s)), RED)
    # the great reactor wheel on each flank, the red eye at its hub, conduits of red light along the side
    M.add(f'whl{s}', lambda p, s=s: ring(p, (-.9, .1, .98 * s), 'z', .95, .12, .2, .03), GUN)
    M.carve(f'whlR{s}', lambda p, s=s: ring(p, (-.9, .1, 1.1 * s), 'z', .95, .03, .05, .01), RED)
    M.carve(f'whlR2{s}', lambda p, s=s: ring(p, (-.9, .1, 1.1 * s), 'z', .7, .03, .03, .01), RED)
    M.add(f'whlD{s}', lambda p, s=s: cyl(p, (-.9, .1, .97 * s), 'z', .78, .08), HULL)
    for a in np.linspace(0, 2 * np.pi, 13)[:-1]:
        M.add(f'whs{s}{a:.2f}', lambda p, s=s, a=a: box(p, (-.9 + .62 * np.cos(a), .1 + .62 * np.sin(a), 1.02 * s), (.12, .025, .03), .005, rot('z', -a)), GUN)
    eye(M, f'eye{s}', (-.9, .1, 1.04 * s), 'z', .5 * s)
    for (a, b, r) in [((-2.9, -.2, .86), (-1.9, -.2, .9), .075), ((.1, -.2, .9), (2.0, -.15, .72), .075), ((-2.8, .4, .82), (-1.9, .4, .85), .06), ((.1, .42, .84), (1.8, .45, .62), .06)]:
        M.add(f'cd{s}{a[0]}{a[1]}', lambda p, s=s, a=a, b=b, r=r: cap(p, (a[0], a[1], a[2] * s), (b[0], b[1], b[2] * s), r), RED)
    for k, (y, z, r) in enumerate([(.1, .5, .34), (.1, -.0, 0), (.55, .25, .26), (-.35, .25, .26)]):
        if r: engine(M, f'eng{s}{k}', -3.3, y, z * s, r, .45)
    M.add(f'cl{s}', lambda p, s=s: spike(p, (.6, -.6, .55 * s), (1.5, -1.6, .9 * s), .16), PLATE)
    M.add(f'cl2{s}', lambda p, s=s: spike(p, (-1.0, -.6, .6 * s), (-.4, -1.5, 1.0 * s), .14), PLATE)
    M.add(f'fn{s}', lambda p, s=s: spike(p, (-1.9, .9, .35 * s), (-3.0, 1.7, .9 * s), .13), PLATE)

for i, x in enumerate((2.0, 1.2, .3, -2.4)):
    for z in ((0,) if x < -2 else (.28, -.28)):
        M.add(f't{i}{z}', lambda p, x=x, z=z: cyl(p, (x, 1.08, z), 'y', .2, .09, .03), GUN)
        for dz in (.06, -.06): M.add(f'tb{i}{z}{dz}', lambda p, x=x, z=z, dz=dz: cap(p, (x, 1.12, z + dz), (x + .65, 1.12, z + dz), .032), GUN)
M.carve('seams', seams(body, .6), DARK)
offwheel = lambda f: (lambda p: np.maximum(f(p), 1.2 - np.hypot(p[..., 0] + .9, p[..., 1] - .1)))
M.carve('slits', offwheel(slit_rows(body, [.42, .18, -.3], -3.0, 2.8, .26)), RED)
M.carve('vents', offwheel(slit_rows(body, [-.05], -2.2, 1.8, .36, .035, .11)), LITE)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.55, sy=.35, sz=.4))
