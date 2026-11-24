# The Continuum Interceptor, after art/rwar/interceptor.webp: a plated dart with a red eye on each cheek, three forward blades at the
# nose, long swept wings with up-turned blade fins at their tips and crimson light along their edges, twin engines in a heavy housing.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: hull(p, [(2.2, 0), (1.1, .38), (-1.3, .44), (-1.8, .3), (-1.8, 0)], .3, -.2, .12)
M = Model((-2.3, -.5, -2.5), (3.2, 1.2, 2.5), float(sys.argv[2]) if len(sys.argv) > 2 else .03)
M.add('body', body, HULL)
M.add('hump', lambda p: ell(p, (.3, .12, 0), (1.7, .42, .55)), PLATE, .08)
M.add('cowl', lambda p: ell(p, (1.0, .05, 0), (.8, .3, .5)), HULL, .06)
M.add('spear', lambda p: hull(p, [(3.0, 0), (2.0, .12), (1.5, .2), (1.5, 0)], .07, -.07, .05), PLATE, .03)
def segline(a, b):
    d = np.subtract(b, a); L = np.hypot(d[0], d[1]); ang = np.arctan2(-d[1], d[0]); return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), L, rot('y', ang)
for s in (1, -1):
    M.add(f'blade{s}', lambda p, s=s: prism(p, [(3.0, .75 * s), (.6, 1.05 * s), (.2, .5 * s), (1.2, .35 * s)], .03, -.07, .03, .01), PLATE)
    M.add(f'can{s}', lambda p, s=s: spike(p, (1.3, -.05, .42 * s), (2.3, -.2, 1.15 * s), .09), PLATE)
    W = [(.6, .36 * s), (-1.5, 2.25 * s), (-1.95, 2.2 * s), (-1.05, .4 * s)]
    M.add(f'wing{s}', lambda p, W=W: prism(p, W, .07, -.05, .04, .01), HULL)
    M.add(f'wingp{s}', lambda p, s=s: prism(p, [(.3, .45 * s), (-1.3, 1.9 * s), (-1.6, 1.85 * s), (-.9, .5 * s)], .11, .04, .03, .01), PLATE)
    M.add(f'fin{s}', lambda p, s=s: prism(p, [(-1.05, 0), (-1.95, 0), (-1.85, .25), (-1.25, .95)], .035, -.035, .015, .01, c=(0, 0, 2.2 * s), R=XYZ_XZY), PLATE)
    M.add(f'finb{s}', lambda p, s=s: prism(p, [(-1.25, 0), (-1.85, 0), (-1.75, -.18), (-1.45, -.3)], .03, -.03, .01, .01, c=(0, 0, 2.15 * s), R=XYZ_XZY), PLATE)
    eye(M, f'eye{s}', (.95, .08, .64 * s), 'z', .36 * s)
    engine(M, f'eng{s}', -1.8, .05, .28 * s, .2, .55)
    # crimson along the wing's leading edge, top and bottom, and along the fin
    (m, L, R) = segline((.45, .5 * s), (-1.55, 2.14 * s)); M.carve(f'lead{s}', lambda p, m=m, L=L, R=R: box(p, (m[0], .065, m[1]), (L / 2 - .1, .025, .028), 0, R), RED)
    M.carve(f'leadb{s}', lambda p, m=m, L=L, R=R: box(p, (m[0] - .2, -.05, m[1]), (L / 2 - .25, .02, .035), 0, R), RED)
    M.carve(f'finl{s}', lambda p, s=s: box(p, (-1.55, .55, 2.2 * s), (.04, .3, .05), 0, rot('z', .55)), RED)
M.add('house', lambda p: cyl(p, (-1.35, .05, 0), 'x', .42, .4, .08), GUN, .04)
M.add('houseR', lambda p: ring(p, (-1.05, .05, 0), 'x', .43, .05, .05), BLACK)
M.carve('houseC', lambda p: ring(p, (-1.4, .05, 0), 'x', .43, .03, .03), RED)
M.carve('seams', seams(body, .6), DARK)
M.carve('slits', slit_rows(body, [.12], -1.2, 1.5, .22), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.4, sy=.3, sz=.35))
