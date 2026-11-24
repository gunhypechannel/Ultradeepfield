# The Eternal Commander, after art/rwar/c_eternal.webp: four long tapering blades swept out from a smooth hub in an X, the forward pair
# longer, polished black chrome ridged along each blade's spine and lined beneath with machinery and crimson light, a red heart at the hub.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
M = Model((-3.9, -.7, -3.0), (4.5, 1.1, 3.0), float(sys.argv[2]) if len(sys.argv) > 2 else .03)
CHROME = {'c': (.09, .088, .09), 'r': .18, 'm': 1}
blades = [(.5, 4.75), (-.5, 4.75), (np.pi - .48, 3.95), (-(np.pi - .48), 3.95)]
for i, (th, L) in enumerate(blades):
    R = rot('y', -th)
    M.add(f'bl{i}', lambda p, R=R, L=L: hull(p, [(L, 0), (L * .45, .25), (.2, .46), (-.4, 0)], .26, -.22, .2, .02, R=R), CHROME, .25)
    M.add(f'sp{i}', lambda p, R=R, L=L: hull(p, [(L * .9, 0), (L * .4, .1), (0, .18), (-.2, 0)], .38, .2, .08, .01, R=R), HULL, .08)
    M.add(f'ub{i}', lambda p, R=R, L=L: hull(p, [(L * .75, 0), (L * .3, .16), (0, .24), (-.2, 0)], -.15, -.36, .08, .01, R=R), BLACK, .06)
    for j in range(5):
        t = .9 + j * L * .11; w = .2 * (1 - t / L) + .04
        M.add(f'mb{i}{j}', lambda p, R=R, t=t, w=w: box(p @ R, (t, -.3, 0), (.12, .07, w), .02), GUN, .03)
    for sd in (1, -1):
        M.carve(f'ln{i}{sd}', lambda p, R=R, L=L, sd=sd: box(p @ R, (L * .4, .05, sd * .27), (L * .26, .02, .05), 0, rot('y', sd * .07)), RED)
M.add('hub', lambda p: ell(p, (.1, .1, 0), (1.45, .5, .8)), HULL, .3)
M.add('hubT', lambda p: ell(p, (0, .4, 0), (.9, .3, .5)), CHROME, .15)
M.add('heart', lambda p: sphere(p, (.25, .58, 0), .2), RED)
M.carve('hubR', lambda p: np.maximum(ring(p, (.1, .15, 0), 'y', 1.0, .03, .5, .01), np.abs(ell(p, (.1, .1, 0), (1.45, .5, .8))) - .05), RED)
for s in (1, -1): eye(M, f'eye{s}', (.1, .05, .7 * s), 'z', .3 * s)
engine(M, 'engA', -1.3, 0, .38, .28, .4); engine(M, 'engB', -1.3, 0, -.38, .28, .4)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.5, sy=.4, sz=.5))
