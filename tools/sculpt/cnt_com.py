# The Continuum Command Frame (no painting yet; drawn in the family's style): a heavy wedge like the Dreadnought's but crowned with a
# tall command spire and a ring of antennae, a red eye on the spire's face, turrets fore and aft, blades and engines.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: np.maximum(hull(p, [(3.6, 0), (1.8, .7), (-2.6, .95), (-3.3, .8), (-3.3, 0)], .65, -.6, .2), profile(p, [(3.8, -.1), (1.4, .65), (-3.4, .67), (-3.4, -.62), (1.4, -.6)]))
M = Model((-3.9, -1.95, -1.75), (4.1, 4.0, 1.75), float(sys.argv[2]) if len(sys.argv) > 2 else .035)
M.add('body', body, HULL)
M.add('deck', lambda p: hull(p, [(2.4, 0), (1.2, .5), (-2.6, .62), (-2.9, 0)], .95, .55, .14), PLATE, .05)
tower = lambda p: np.maximum(hull(p, [(.2, 0), (-.3, .45), (-1.6, .5), (-1.9, 0)], 2.6, .9, .14), profile(p, [(.3, .9), (-.1, 2.7), (-1.5, 2.9), (-2.0, .9)]))
M.add('tower', tower, PLATE, .08)
M.add('spire', lambda p: spike(p, (-.9, 2.6, 0), (-1.0, 3.9, 0), .14), GUN)
eye(M, 'eyeT', (-.15, 1.95, 0), 'x', .36)
for a in np.linspace(0, 2 * np.pi, 7)[:-1]:
    M.add(f'ant{a:.2f}', lambda p, a=a: spike(p, (-.9 + np.cos(a) * .35, 2.7, np.sin(a) * .35), (-.9 + np.cos(a) * .6, 3.4, np.sin(a) * .6), .05), GUN)
M.carve('towerw', lambda p: np.maximum(slit_rows(tower, [1.3, 1.6, 2.2], -1.8, .2, .2)(p), np.abs(tower(p)) - .05), RED)
for s in (1, -1):
    for j, (x0, y0, L, w) in enumerate([(1.6, .4, 2.0, .45), (.2, .0, 2.4, .6), (1.3, -.4, 2.1, .5), (-1.6, .0, 1.6, .5)]):
        M.add(f'bl{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: prism(p, [(x0 + L, (.9 + w) * s), (x0 + .2, (.7 + w * .55) * s), (x0 - .3, .65 * s), (x0 + .5, .65 * s)], y0 + .045, y0 - .045, .025, .012), PLATE)
        M.carve(f'blr{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: box(p, (x0 + L * .42, y0 + .05, (.78 + w * .55) * s), (L * .26, .018, .035), 0, rot('y', -np.arctan2(w * .45, L * .8) * s)), RED)
    eye(M, f'eye{s}', (-1.0, .05, .95 * s), 'z', .4 * s)
    for k, (y, z, r) in enumerate([(.1, .5, .34), (.55, .22, .24), (-.35, .22, .24)]):
        engine(M, f'eng{s}{k}', -3.3, y, z * s, r, .45)
    M.add(f'cl{s}', lambda p, s=s: spike(p, (.6, -.6, .55 * s), (1.5, -1.6, .9 * s), .16), PLATE)
for i, x in enumerate((2.0, 1.1, -2.5)):
    M.add(f't{i}', lambda p, x=x: cyl(p, (x, 1.03, 0), 'y', .2, .09, .03), GUN)
    for dz in (.06, -.06): M.add(f'tb{i}{dz}', lambda p, x=x, dz=dz: cap(p, (x, 1.07, dz), (x + .65, 1.07, dz), .032), GUN)
M.carve('seams', seams(body, .6), DARK)
M.carve('slits', slit_rows(body, [.38, .12, -.3], -3.0, 3.0, .26), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.55, sy=.35, sz=.4))
