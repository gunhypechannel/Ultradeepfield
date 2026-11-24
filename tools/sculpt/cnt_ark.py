# The Resurrection Ark, sculpted after the owner's paintings (art/rwar/ark_side.webp, ark_front.webp): a massive armoured body,
# a heavy prow of stacked blade plates with crimson light between the layers, the radial red eye on each flank, three great armoured
# hoops banded with red light, a row of tall reconstruction chambers holding machine frames, landing decks beneath, a gothic crown
# of spires and a domed tower on its back, stalactite spikes hanging under it, and crimson window slits along every deck.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
rng = np.random.default_rng(7)
body = lambda p: hull(p, [(5.0, 0), (3.6, .95), (-4.8, 1.15), (-5.6, .85), (-5.6, 0)], 1.05, -1.0, .32)
M = Model((-6.8, -3.3, -2.6), (7.6, 4.6, 2.6), float(sys.argv[2]) if len(sys.argv) > 2 else .04)
M.add('body', body, HULL)
M.add('upper', lambda p: hull(p, [(4.2, 0), (2.8, .7), (-4.4, .85), (-4.8, 0)], 1.55, .9, .26), PLATE, .06)
M.add('keel', lambda p: hull(p, [(3.6, 0), (2.4, .7), (-4.2, .8), (-4.8, 0)], -.9, -1.45, .22), PLATE, .05)
# the prow: four stacked blades, each longer than the one above, sweeping forward and down, red light in the gaps
for i, (x0, y0, y1, w) in enumerate([(7.4, -.55, -.25, 1.0), (6.9, -.12, .2, 1.1), (6.2, .33, .62, 1.05), (5.5, .75, 1.02, .9)]):
    M.add(f'prow{i}', lambda p, x0=x0, y0=y0, y1=y1, w=w: hull(p, [(x0, 0), (x0 - 2.2, w * .55), (2.4, w), (2.4, 0)], y1, y0, .09, c=(0, 0, 0), R=rot('z', -.06)), PLATE)
    M.add(f'prowL{i}', lambda p, x0=x0, y0=y0, w=w: hull(p, [(x0 - .6, 0), (x0 - 2.4, w * .42), (2.6, w * .8), (2.6, 0)], y0 + .005, y0 - .05, .02, R=rot('z', -.06)), RED)
for s in (1, -1):
    for j, (b, t, r) in enumerate([((4.4, -.3, .9), (6.4, -.7, 1.9), .2), ((3.7, .5, .95), (5.6, .8, 2.0), .17), ((2.6, -.8, .95), (4.0, -1.6, 1.7), .15)]):
        M.add(f'fin{s}{j}', lambda p, s=s, b=b, t=t, r=r: spike(p, (b[0], b[1], b[2] * s), (t[0], t[1], t[2] * s), r), PLATE)
    # the eye: an armoured rim, radial vanes and a red core
    M.add(f'eyeR{s}', lambda p, s=s: ring(p, (3.0, .05, 1.0 * s), 'z', .72, .1, .12), GUN)
    M.add(f'eyeC{s}', lambda p, s=s: sphere(p, (3.0, .05, 1.05 * s), .3), RED)
    for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
        M.add(f'eyeV{s}{a:.2f}', lambda p, s=s, a=a: box(p, (3.0 + .48 * np.cos(a), .05 + .48 * np.sin(a), 1.02 * s), (.2, .035, .06), .01, rot('z', -a)), GUN)
    for k, (y, r) in enumerate([(.05, .42), (.62, .3), (-.55, .3)]):
        M.add(f'eng{s}{k}', lambda p, s=s, y=y, r=r: cyl(p, (-5.8, y, .55 * s), 'x', r, .35, .06), GUN)
# three great armoured hoops banded with red light
for x in (1.75, -1.35, -4.2):
    M.add(f'hoop{x}', lambda p, x=x: ring(p, (x, .2, 0), 'x', 1.95, .3, .2, .04), GUN)
    M.add(f'hoopi{x}', lambda p, x=x: ring(p, (x, .2, 0), 'x', 1.72, .2, .06, .02), HULL)
    for a in np.linspace(0, 2 * np.pi, 13)[:-1]:
        M.add(f'hb{x}{a:.2f}', lambda p, x=x, a=a: box(p, (x, .2 + 2.16 * np.sin(a), 2.16 * np.cos(a)), (.36, .07, .2), .02, rot('x', -a)), PLATE)
# the reconstruction chambers between the hoops: tall red glass with a machine frame inside, ringed top and bottom
for i, x in enumerate([1.0, .35, -.3, -2.1, -2.75, -3.4]):
    for s in (1, -1):
        M.add(f'ch{i}{s}', lambda p, x=x, s=s: cap(p, (x, -.45, 1.25 * s), (x, .75, 1.25 * s), .27), GLASS)
        M.add(f'cf{i}{s}', lambda p, x=x, s=s: ring(p, (x, .92, 1.25 * s), 'y', .28, .09, .06), GUN)
        M.add(f'cg{i}{s}', lambda p, x=x, s=s: ring(p, (x, -.62, 1.25 * s), 'y', .28, .09, .06), GUN)
        for dx in (-.06, .06): M.add(f'cl{i}{s}{dx}', lambda p, x=x, s=s, dx=dx: cap(p, (x + dx, -.38, 1.47 * s), (x + dx * .6, .02, 1.48 * s), .035), DARK)
        M.add(f'cm{i}{s}', lambda p, x=x, s=s: cap(p, (x, .02, 1.48 * s), (x, .36, 1.49 * s), .065), DARK)
        for dx in (-.11, .11): M.add(f'ca{i}{s}{dx}', lambda p, x=x, s=s, dx=dx: cap(p, (x + dx * .6, .34, 1.48 * s), (x + dx, .02, 1.47 * s), .028), DARK)
        M.add(f'ck{i}{s}', lambda p, x=x, s=s: sphere(p, (x, .47, 1.48 * s), .07), DARK)
# landing decks underneath, with pale running lights on their lips
for i, x in enumerate([.9, -1.0, -2.9]):
    for s in (1, -1):
        M.add(f'dk{i}{s}', lambda p, x=x, s=s: box(p, (x, -1.25, 1.45 * s), (.75, .06, .55), .02), PLATE)
        M.add(f'dl{i}{s}', lambda p, x=x, s=s: box(p, (x, -1.25, 1.99 * s), (.7, .03, .02), .01), LITE)
for i in range(22):
    x = rng.uniform(-5, 5.6); z = rng.uniform(-.85, .85); l = rng.uniform(.5, 1.7) * (1.25 if -3 < x < 3 else .8)
    M.add(f'st{i}', lambda p, x=x, z=z, l=l: spike(p, (x, -1.3, z), (x - .25, -1.3 - l, z * 1.1), .14), DARK)
# the crown: a gothic cluster of spires around a domed tower
for i in range(16):
    x = rng.uniform(-4.0, -.4); z = rng.uniform(-.65, .65); l = rng.uniform(.6, 2.0) * (1.5 if abs(x + 2.2) < .8 else 1)
    M.add(f'sp{i}', lambda p, x=x, z=z, l=l: spike(p, (x, 1.5, z), (x, 1.5 + l, z), .11), GUN)
M.add('dome', lambda p: ell(p, (-2.2, 1.6, 0), (.85, .5, .6)), PLATE, .08)
M.add('domeR', lambda p: ring(p, (-2.2, 1.75, 0), 'y', .62, .04, .06), RED)
M.add('tower', lambda p: spike(p, (-2.2, 1.6, 0), (-2.2, 4.4, 0), .22), GUN)
# carves: panel seams, crimson window slits along the decks, red bands on the hoops' faces, red engine throats
shell = lambda p: body(p) + .06
def seams(p):
    q = p.copy(); q[..., 0] = np.mod(q[..., 0] + 20, .62) - .31; return np.maximum(box(q, (0, 0, 0), (.014, 3, 3)), np.abs(body(p)) - .06)
M.carve('seams', seams, DARK)
def slits(p):
    q = p.copy(); q[..., 0] = np.mod(q[..., 0] + 20, .3) - .15; q[..., 1] = 0; w = box(q, (0, 0, 0), (.09, 1, 3))
    band = np.minimum(np.minimum(np.abs(p[..., 1] - .72), np.abs(p[..., 1] + .62)), np.abs(p[..., 1] - 1.25))
    return np.maximum(np.maximum(w, band - .035), np.maximum(np.abs(body(p)) - .06, np.abs(p[..., 0] - .2) - 4.9))
M.carve('slits', slits, RED)
for x in (1.75, -1.35, -4.2):
    M.carve(f'hband{x}', lambda p, x=x: ring(p, (x, .2, 0), 'x', 2.16, .045, .06, .01), RED)
    M.carve(f'hface{x}', lambda p, x=x: ring(p, (x + .3, .2, 0), 'x', 1.95, .03, .035, .01), RED)
for s in (1, -1):
    for k, (y, r) in enumerate([(.05, .42), (.62, .3), (-.55, .3)]):
        M.carve(f'thr{s}{k}', lambda p, s=s, y=y, r=r: cyl(p, (-6.15, y, .55 * s), 'x', r * .5, .1), RED)
def paint(P, N, A, E, idx):
    v = panels(P, .62, .45, .4); hullish = (A[:, 0] < .1) & (E[:, 0] < .01)
    A[hullish, :3] *= (.7 + .65 * v[hullish])[:, None]
    top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .3 * top)[:, None]
M.bake(sys.argv[1], paint)
