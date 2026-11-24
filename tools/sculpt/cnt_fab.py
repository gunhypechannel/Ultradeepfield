# The Fabrication Carrier (no painting yet; drawn in the family's style): a broad flat-decked hull, a row of glowing launch bays down
# each flank where its drones are built, a raised spine with fabrication cranes, swept blades and a stern of three engines.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: np.maximum(hull(p, [(3.2, 0), (2.0, .85), (-2.9, 1.05), (-3.4, .8), (-3.4, 0)], .45, -.55, .16), profile(p, [(3.4, -.1), (1.8, .45), (-3.5, .47), (-3.5, -.57), (1.8, -.55)]))
M = Model((-3.9, -1.5, -1.6), (3.6, 2.1, 1.6), float(sys.argv[2]) if len(sys.argv) > 2 else .035)
M.add('body', body, HULL)
M.add('spine', lambda p: hull(p, [(1.8, 0), (1.0, .35), (-2.6, .4), (-2.9, 0)], .9, .4, .12), PLATE, .05)
M.add('bridge', lambda p: hull(p, [(-1.6, 0), (-1.9, .25), (-2.6, .28), (-2.8, 0)], 1.45, .8, .1), HULL, .04)
eye(M, 'eyeB', (-1.9, 1.15, 0), 'x', .22)
for i, x in enumerate((1.0, -.2, -1.4)):
    M.add(f'cr{i}', lambda p, x=x: cap(p, (x, .9, 0), (x, 1.5, 0), .06), GUN)
    M.add(f'cra{i}', lambda p, x=x: cap(p, (x, 1.5, 0), (x + .55, 1.5, .0), .05), GUN)
    M.add(f'crh{i}', lambda p, x=x: spike(p, (x + .55, 1.5, 0), (x + .55, 1.15, 0), .05), GUN)
for s in (1, -1):
    for i, x in enumerate((1.4, .4, -.6, -1.6, -2.6)):
        M.add(f'bay{s}{i}', lambda p, s=s, x=x: box(p, (x, -.1, 1.02 * s), (.36, .26, .08), .03), BLACK, .02)
        M.carve(f'bayc{s}{i}', lambda p, s=s, x=x: box(p, (x, -.1, 1.12 * s), (.28, .18, .08)), RED)
    M.add(f'bl{s}', lambda p, s=s: prism(p, [(3.1, .5 * s), (.8, 1.4 * s), (.0, 1.42 * s), (1.2, .7 * s)], .45, .38, .03, .01), PLATE)
    M.add(f'cl{s}', lambda p, s=s: spike(p, (-.4, -.5, .6 * s), (.4, -1.4, .95 * s), .13), PLATE)
    engine(M, f'eng{s}', -3.4, 0, .55 * s, .32, .45)
engine(M, 'eng0', -3.4, .3, 0, .26, .45)
M.carve('seams', seams(body, .6), DARK)
M.carve('slits', slit_rows(body, [.3], -3.0, 2.6, .26), RED)
M.carve('vents', slit_rows(body, [-.42], -2.6, 2.0, .36, .03, .1), LITE)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.55, sy=.35, sz=.45))
