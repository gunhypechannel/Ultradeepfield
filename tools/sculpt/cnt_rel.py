# The Resurrection Relay, after art/rwar/c_relay.webp and relay.webp: a gothic tower on a dark asteroid veined with red, its crimson core
# column rising through two great rings, buttresses and window slots up its sides, spires crowding its crown and the rings.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
M = Model((-2.8, -2.8, -2.8), (2.8, 7.7, 2.8), float(sys.argv[2]) if len(sys.argv) > 2 else .04)
rockf = lambda p: smin(ell(p, (0, -1.1, 0), (2.6, 1.05, 2.4)), ell(p, (.6, -1.8, .3), (1.3, .8, 1.2)), .4) + noise3(p, 1.3, 3) * .3
M.add('rock', rockf, ROCK)
M.carve('veins', lambda p: np.maximum(np.abs(noise3(p, 1.7, 9)) - .022, np.abs(rockf(p)) - .05), RED)
M.add('plat', lambda p: cyl(p, (0, .05, 0), 'y', 2.05, .12, .04), PLATE, .05)
M.add('plat2', lambda p: cyl(p, (0, .32, 0), 'y', 1.45, .16, .04), HULL, .04)
M.carve('platR', lambda p: ring(p, (0, .05, 0), 'y', 2.07, .035, .04, .01), RED)
tower = lambda p: rcone(p, (0, .3, 0), (0, 6.3, 0), .9, .26)
M.add('tower', tower, HULL)
for a in np.linspace(0, 2 * np.pi, 7)[:-1]:
    c, s = np.cos(a), np.sin(a)
    M.add(f'rib{a:.2f}', lambda p, c=c, s=s: cap(p, (c * .92, .4, s * .92), (c * .3, 5.8, s * .3), .11), GUN)
    M.carve(f'win{a:.2f}', lambda p, c=c, s=s: box(p, (c * .62, 2.6, s * .62), (.07, 1.9, .07), 0, rot('y', -np.arctan2(s, c))), RED)
    M.add(f'bsp{a:.2f}', lambda p, c=c, s=s: spike(p, (c * 1.3, .45, s * 1.3), (c * 1.4, 1.6, s * 1.4), .12), GUN)
M.add('core', lambda p: spike(p, (0, 5.6, 0), (0, 7.6, 0), .16), RED)
for k, (y, R) in enumerate([(3.0, 2.25), (4.7, 1.85)]):
    M.add(f'ring{k}', lambda p, y=y, R=R: ring(p, (0, y, 0), 'y', R, .17, .2, .04), PLATE)
    M.carve(f'ringR{k}', ring_windows((0, 0, 0), R, .2, y), RED)
    M.carve(f'ringT{k}', lambda p, y=y, R=R: ring(p, (0, y + .17, 0), 'y', R, .025, .035, .01), RED)
    for a in np.linspace(0, 2 * np.pi, 5)[:-1] + k * .4:
        c, s = np.cos(a), np.sin(a); rr = .9 - y * .1
        M.add(f'sk{k}{a:.2f}', lambda p, c=c, s=s, y=y, R=R, rr=rr: cap(p, (c * rr, y, s * rr), (c * R, y, s * R), .07), GUN)
    for a in np.linspace(0, 2 * np.pi, 7)[:-1] + k * .3:
        c, s = np.cos(a), np.sin(a)
        M.add(f'rs{k}{a:.2f}', lambda p, c=c, s=s, y=y, R=R: spike(p, (c * R, y + .1, s * R), (c * R, y + .75, s * R), .09), GUN)
rng = np.random.default_rng(4)
for i in range(9):
    a = rng.uniform(0, 6.28); r = rng.uniform(.15, .45); h = rng.uniform(.6, 1.4)
    M.add(f'cr{i}', lambda p, a=a, r=r, h=h: spike(p, (np.cos(a) * r, 5.4, np.sin(a) * r), (np.cos(a) * r * 1.2, 5.4 + h + .4, np.sin(a) * r * 1.2), .1), GUN)
for i in range(10):
    a = rng.uniform(0, 6.28); r = rng.uniform(.5, 1.7); l = rng.uniform(.4, 1.1)
    M.add(f'st{i}', lambda p, a=a, r=r, l=l: spike(p, (np.cos(a) * r, -2.0 + r * .3, np.sin(a) * r), (np.cos(a) * r, -2.0 + r * .3 - l, np.sin(a) * r), .16), ROCK)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.5, sy=.5, sz=.5))
