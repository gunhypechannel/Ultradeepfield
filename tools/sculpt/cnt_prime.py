# The Prime Resurrection Ark, after art/rwar/c_prime.webp: a gothic citadel ringed with tall red resurrection chambers, a crown of
# spires, an upper ring and a broad lower ring set with crimson windows, three arms out to anchor pylons, and beneath it an inverted
# spire bristling with stalactites, a red core running through the whole height.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
M = Model((-5.4, -6.6, -5.4), (5.4, 7.4, 5.4), float(sys.argv[2]) if len(sys.argv) > 2 else .055)
cit = lambda p: rcone(p, (0, -1.2, 0), (0, 2.6, 0), 1.55, 1.2)
M.add('cit', cit, HULL)
M.add('citT', lambda p: rcone(p, (0, 2.5, 0), (0, 5.6, 0), 1.05, .28), PLATE, .1)
M.add('core', lambda p: spike(p, (0, 4.5, 0), (0, 7.3, 0), .24), RED)
M.add('coreB', lambda p: spike(p, (0, -4.0, 0), (0, -6.5, 0), .26), RED)
for i, a in enumerate(np.linspace(0, 2 * np.pi, 11)[:-1]):
    c, s = np.cos(a), np.sin(a)
    M.add(f'ch{i}', lambda p, c=c, s=s: cap(p, (c * 1.5, -.4, s * 1.5), (c * 1.42, 1.5, s * 1.42), .3), GLASS)
    M.add(f'chf{i}', lambda p, c=c, s=s: ring(p, (c * 1.48, 1.75, s * 1.48), 'y', .3, .07, .07), GUN)
    M.add(f'chg{i}', lambda p, c=c, s=s: ring(p, (c * 1.5, -.65, s * 1.5), 'y', .3, .07, .07), GUN)
    M.add(f'chm{i}', lambda p, c=c, s=s: cap(p, (c * 1.62, -.3, s * 1.62), (c * 1.6, 1.0, s * 1.6), .07), DARK)
    M.add(f'bt{i}', lambda p, c=c, s=s: cap(p, (c * 1.25, 2.6, s * 1.25), (c * .5, 4.6, s * .5), .1), GUN)
rng = np.random.default_rng(11)
for i in range(26):
    a = rng.uniform(0, 6.28); y0 = rng.uniform(2.6, 4.6); r = (1.05 - (y0 - 2.5) / 3.1 * .77) * .92; h = rng.uniform(.9, 2.2) * (1.4 if y0 > 3.8 else 1)
    M.add(f'sp{i}', lambda p, a=a, r=r, h=h, y0=y0: spike(p, (np.cos(a) * r, y0, np.sin(a) * r), (np.cos(a) * r * 1.05, y0 + h, np.sin(a) * r * 1.05), .14), GUN)
M.add('ringU', lambda p: ring(p, (0, 4.1, 0), 'y', 3.1, .17, .24, .04), PLATE)
M.carve('ringUw', ring_windows((0, 0, 0), 3.1, .24, 4.1, .34, .08, .04), RED)
for a in np.linspace(0, 2 * np.pi, 7)[:-1]:
    M.add(f'us{a:.2f}', lambda p, a=a: cap(p, (np.cos(a) * .7, 4.1, np.sin(a) * .7), (np.cos(a) * 3.0, 4.1, np.sin(a) * 3.0), .08), GUN)
M.add('deck', lambda p: cyl(p, (0, -1.15, 0), 'y', 2.7, .16, .05), PLATE, .1)
M.add('ringL', lambda p: ring(p, (0, -1.2, 0), 'y', 3.7, .26, .32, .05), PLATE)
M.carve('ringLw', ring_windows((0, 0, 0), 3.7, .32, -1.15, .34, .08, .05), RED)
M.carve('ringLt', lambda p: ring(p, (0, -.94, 0), 'y', 3.7, .03, .05, .01), RED)
for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
    M.add(f'ls{a:.2f}', lambda p, a=a: box(p, (np.cos(a) * 3.2, -1.2, np.sin(a) * 3.2), (.55, .1, .12), .02, rot('y', -a)), GUN)
for i in range(3):
    a = i * 2 * np.pi / 3 + .3; x, z = np.cos(a) * 4.8, np.sin(a) * 4.8
    M.add(f'arm{i}', lambda p, x=x, z=z: cap(p, (0, .3, 0), (x, .3, z), .17), GUN)
    M.add(f'py{i}', lambda p, x=x, z=z: rcone(p, (x, -.7, z), (x, 2.3, z), .42, .12), HULL)
    M.add(f'pyb{i}', lambda p, x=x, z=z: sphere(p, (x, 2.4, z), .26), RED)
    M.add(f'pyr{i}', lambda p, x=x, z=z: ring(p, (x, 1.1, z), 'y', .45, .06, .07), GUN)
    M.carve(f'pyw{i}', lambda p, x=x, z=z: ring(p, (x, 1.1, z), 'y', .52, .02, .03, .01), RED)
    M.add(f'pys{i}', lambda p, x=x, z=z: spike(p, (x, -.6, z), (x, -2.2, z), .3), HULL)
    for j in range(4):
        b = j * np.pi / 2
        M.add(f'pyx{i}{j}', lambda p, x=x, z=z, b=b: spike(p, (x, 1.6, z), (x + np.cos(b) * .5, 2.5, z + np.sin(b) * .5), .07), GUN)
under = lambda p: rcone(p, (0, -1.3, 0), (0, -4.8, 0), 2.3, .35)
M.add('under', under, HULL, .1)
for i in range(34):
    a = rng.uniform(0, 6.28); y0 = rng.uniform(-4.2, -1.5); r = (2.3 - (-1.3 - y0) / 3.5 * 1.95) * .9; l = rng.uniform(.8, 2.4) * (1.3 if y0 > -2.5 else 1)
    M.add(f'st{i}', lambda p, a=a, r=r, y0=y0, l=l: spike(p, (np.cos(a) * r, y0, np.sin(a) * r), (np.cos(a) * r * 1.02, y0 - l, np.sin(a) * r * 1.02), .18), HULL)
for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
    M.carve(f'uw{a:.2f}', lambda p, a=a: np.maximum(box(p, (np.cos(a) * 1.4, -2.6, np.sin(a) * 1.4), (.06, 1.0, .06), 0, rot('y', -a)), np.abs(under(p)) - .06), RED)
M.carve('citw', lambda p: np.maximum(ring_windows((0, 0, 0), 1.0, .2, 2.2, .3, .07, .05)(p), np.abs(cit(p)) - .06), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.7, sy=.6, sz=.7))
