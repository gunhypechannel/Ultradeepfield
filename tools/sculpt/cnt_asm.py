# The Assimilation Cruiser, after art/rwar/c_cruiser.webp: a dark, grown-looking hull: a long lance forward, a tall horn swept back
# from its spine, swept arms flowing out from its flanks, all smoothly fused, faintly veined with red, machinery along its belly.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
M = Model((-2.9, -1.0, -1.7), (3.9, 1.35, 1.7), float(sys.argv[2]) if len(sys.argv) > 2 else .028)
K = .22
M.add('body', lambda p: ell(p, (.3, 0, 0), (2.0, .34, .42)), ORGAN)
M.add('lance', lambda p: spike(p, (1.2, 0, 0), (3.85, -.12, 0), .3), ORGAN, K)
M.add('tail', lambda p: spike(p, (-.8, 0, 0), (-2.8, .08, 0), .3), ORGAN, K)
M.add('horn', lambda p: spike(p, (.3, .15, 0), (-1.35, 1.3, 0), .36), ORGAN, K)
for s in (1, -1):
    M.add(f'arm{s}', lambda p, s=s: spike(p, (-.1, -.02, .25 * s), (-2.3, -.3, 1.65 * s), .22), ORGAN, K)
    M.add(f'fa{s}', lambda p, s=s: spike(p, (.7, -.05, .25 * s), (2.3, -.4, 1.15 * s), .14), ORGAN, K)
    for j in range(6):
        x = 1.6 - j * .42
        M.add(f'bl{s}{j}', lambda p, s=s, x=x: box(p, (x, -.28, .12 * s), (.13, .05, .07), .02), BLACK, .04)
skin = lambda p: smin(smin(ell(p, (.3, 0, 0), (2.0, .34, .42)), spike(p, (1.2, 0, 0), (3.85, -.12, 0), .3), K), spike(p, (.3, .15, 0), (-1.35, 1.3, 0), .36), K)
M.carve('veins', lambda p: np.maximum(np.abs(p[..., 1] + .1) - .01, np.maximum(np.abs(skin(p)) - .05, np.abs(p[..., 0] - .6) - 1.9)), RED)
M.carve('belly', lambda p: np.maximum(box(p, (.6, -.3, 0), (1.5, .02, .03)), np.abs(skin(p)) - .06), RED)
def paintO(P, N, A, E, idx):
    v = noise3(P, 2.0, 1); rib = .93 + .07 * np.sign(np.sin(P[:, 0] * 16)); org = E[:, 0] < .01; A[org, :3] *= ((.8 + .3 * v[org]) * rib[org])[:, None]
M.bake(sys.argv[1], paintO)
