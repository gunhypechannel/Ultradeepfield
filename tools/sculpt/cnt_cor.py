# The Neural Corvette (no painting yet; drawn in the family's style): a compact plated dart with a large red eye at its brow, a dorsal
# sensor mast, swept side blades and twin engines.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
body = lambda p: np.maximum(hull(p, [(2.6, 0), (1.2, .5), (-1.5, .62), (-1.9, .45), (-1.9, 0)], .42, -.3, .14), profile(p, [(2.75, -.04), (1.0, .42), (-2.0, .44), (-2.0, -.32), (1.0, -.3)]))
M = Model((-2.4, -.9, -1.4), (2.9, 2.5, 1.4), float(sys.argv[2]) if len(sys.argv) > 2 else .025)
M.add('body', body, HULL)
M.add('deck', lambda p: hull(p, [(1.4, 0), (.6, .32), (-1.5, .4), (-1.7, 0)], .62, .3, .1), PLATE, .04)
eye(M, 'eyeF', (1.05, .62, 0), 'y', .34)
M.add('mast', lambda p: cap(p, (-.6, .6, 0), (-.7, 2.3, 0), .06), GUN); M.add('mastR', lambda p: ring(p, (-.65, 1.5, 0), 'y', .22, .03, .04), GUN)
M.add('mastB', lambda p: sphere(p, (-.7, 2.35, 0), .08), RED)
for s in (1, -1):
    M.add(f'bl{s}', lambda p, s=s: prism(p, [(2.3, .5 * s), (.4, 1.15 * s), (-.3, 1.2 * s), (.5, .5 * s)], .05, -.03, .02, .01), PLATE)
    M.carve(f'blr{s}', lambda p, s=s: box(p, (1.1, .06, .82 * s), (.6, .015, .03), 0, rot('y', -.33 * s)), RED)
    M.add(f'cl{s}', lambda p, s=s: spike(p, (.2, -.25, .35 * s), (.7, -.85, .55 * s), .08), PLATE)
    engine(M, f'eng{s}', -1.9, 0, .2 * s, .2, .4)
M.carve('seams', seams(body, .5), DARK)
M.carve('slits', slit_rows(body, [.15], -1.6, 1.8, .22), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.4, sy=.3, sz=.35))
