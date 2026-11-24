# The Execution Destroyer, after art/rwar/destroyer.webp: a long dagger hull of stacked blade plates, twin-gun turrets along its back,
# a reactor hoop with a red eye on each flank, hooked claws beneath, swept fins, blue vents, and a heavy engine block banded in red.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: np.maximum(hull(p, [(3.6, 0), (2.0, .42), (-1.6, .6), (-2.3, .5), (-2.3, 0)], .5, -.42, .14), profile(p, [(3.7, -.06), (1.8, .5), (-2.5, .52), (-2.5, -.44), (1.8, -.42)]))
M = Model((-2.9, -1.25, -1.1), (3.8, 1.3, 1.1), float(sys.argv[2]) if len(sys.argv) > 2 else .03)
M.add('body', body, HULL)
M.add('deck', lambda p: hull(p, [(2.6, 0), (1.4, .3), (-1.8, .42), (-2.0, 0)], .78, .4, .12), PLATE, .04)
M.add('keel', lambda p: hull(p, [(2.9, 0), (1.6, .3), (-1.6, .38), (-1.9, 0)], -.35, -.6, .1), BLACK, .03)
for s in (1, -1):
    # forward-swept knife blades along the flanks, at three heights, as in the painting's jagged outline
    for j, (x0, y0, L, w) in enumerate([(1.2, .28, 2.0, .5), (-.2, -.02, 2.3, .62), (1.0, -.3, 1.9, .5), (-1.6, .3, 1.6, .55), (-1.4, -.28, 1.5, .55)]):
        M.add(f'bl{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: prism(p, [(x0 + L, (.62 + w) * s), (x0 + .2, (.42 + w * .55) * s), (x0 - .3, .4 * s), (x0 + .5, .4 * s)], y0 + .035, y0 - .035, .02, .01), PLATE)
        M.carve(f'blr{j}{s}', lambda p, s=s, x0=x0, y0=y0, L=L, w=w: box(p, (x0 + L * .42, y0 + .04, (.5 + w * .55) * s), (L * .26, .015, .03), 0, rot('y', -np.arctan2(w * .45, L * .8) * s)), RED)
    M.add(f'prow{s}', lambda p, s=s: prism(p, [(3.75, .05 * s), (2.2, .5 * s), (1.6, .45 * s), (1.8, .1 * s)], .14, .08, .03, .01), PLATE)
    eye(M, f'eye{s}', (-.25, .05, .66 * s), 'z', .36 * s)
    engine(M, f'eng{s}', -2.3, .05, .35 * s, .27, .4)
    M.add(f'cl1{s}', lambda p, s=s: spike(p, (.9, -.35, .38 * s), (1.5, -1.1, .62 * s), .11), PLATE)
    M.add(f'cl2{s}', lambda p, s=s: spike(p, (-.3, -.35, .42 * s), (.2, -1.0, .72 * s), .1), PLATE)
    M.add(f'fn{s}', lambda p, s=s: spike(p, (-.5, .55, .3 * s), (-1.5, 1.2, .8 * s), .1), PLATE)
    M.add(f'fn2{s}', lambda p, s=s: spike(p, (.6, .55, .25 * s), (-.1, 1.0, .6 * s), .08), PLATE)
M.add('hoop', lambda p: ring(p, (-1.15, .05, 0), 'x', .86, .16, .14, .03), GUN)
M.carve('hoopR', lambda p: ring(p, (-1.15, .05, 0), 'x', 1.0, .04, .05, .01), RED)
M.carve('hoopF', lambda p: ring(p, (-.99, .05, 0), 'x', .86, .02, .03, .01), RED)
M.add('block', lambda p: cyl(p, (-1.95, .08, 0), 'x', .56, .35, .06), GUN, .05)
for x in (-1.7, -2.15): M.carve(f'bk{x}', lambda p, x=x: ring(p, (x, .08, 0), 'x', .56, .03, .04, .01), RED)
for i, x in enumerate((1.5, .5, -1.4)):
    M.add(f't{i}', lambda p, x=x: cyl(p, (x, .84, 0), 'y', .17, .08, .03), GUN)
    for z in (.05, -.05): M.add(f'tb{i}{z}', lambda p, x=x, z=z: cap(p, (x, .88, z), (x + .55, .88, z), .028), GUN)
M.carve('seams', seams(body, .55), DARK)
M.carve('slits', slit_rows(body, [.2, -.12], -1.8, 2.6, .24), RED)
M.carve('vents', slit_rows(body, [.05], -1.3, 1.4, .34, .03, .1), LITE)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.45, sy=.3, sz=.35))
