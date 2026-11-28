# The Neural Corvette (owner's painting, art/rwar/c_corvette.webp): a long faceted gunmetal hull ending in a spear prow, rows of blue
# chevron vents down each flank, crimson light lines, a central pylon carrying a folding fan of red lattice panels, two jamming dishes
# with glowing red feeds on outriggers, and a forest of thin antenna masts along the deck.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
VENT = {'c': (.03, .06, .08), 'r': .3, 'm': .2, 'e': (.25, .75, 1.0)}
body = lambda p: np.maximum(hull(p, [(2.4, 0), (1.5, .42), (-1.6, .5), (-2.15, .42), (-2.15, 0)], .3, -.36, .12),
                            profile(p, [(2.7, -.06), (1.3, .34), (-2.3, .36), (-2.3, -.4), (1.3, -.38)]))
M = Model((-2.8, -.9, -1.8), (3.5, 2.9, 1.8), float(sys.argv[2]) if len(sys.argv) > 2 else .025)
M.add('body', body, HULL)
# layered armour: a raised deck plate, side skirts and a keel plate
M.add('deck', lambda p: hull(p, [(1.7, 0), (1.1, .3), (-1.7, .36), (-2.0, 0)], .42, .2, .08), PLATE, .03)
M.add('deck2', lambda p: hull(p, [(.9, 0), (.4, .2), (-1.3, .24), (-1.5, 0)], .52, .35, .06), HULL, .02)
M.add('keel', lambda p: hull(p, [(1.9, 0), (1.0, .25), (-1.8, .3), (-2.0, 0)], -.3, -.5, .08), PLATE, .03)
for s in (1, -1):
    M.add(f'sk{s}', lambda p, s=s: prism(p, [(2.0, .38 * s), (1.2, .56 * s), (-1.8, .6 * s), (-1.9, .44 * s)][::s], .08, -.24, .05, .01), PLATE, .02)
    M.add(f'bl{s}', lambda p, s=s: prism(p, [(2.9, .12 * s), (2.0, .5 * s), (1.6, .46 * s), (2.3, .1 * s)][::s], -.12, -.2, .03, .01), PLATE)
    M.add(f'fin{s}', lambda p, s=s: spike(p, (1.3, -.38, .2 * s), (2.1, -.62, .32 * s), .07), PLATE)
    # blue chevron vents: two rows of angled slots in the skirt
    for row, yv in enumerate((.0, -.16)):
        for i in range(5):
            x = -1.5 + i * .26 + row * .06
            M.add(f'v{s}{row}{i}', lambda p, s=s, x=x, yv=yv: box(p, (x, yv, .595 * s), (.028, .06, .025), .006, rot('z', .5)), VENT)
    M.carve(f'rl{s}', lambda p, s=s: box(p, (.9, -.06, .56 * s), (.75, .012, .08), 0, rot('y', -.08 * s)), RED)
    M.carve(f'rl2{s}', lambda p, s=s: box(p, (1.6, -.24, .42 * s), (.55, .01, .08), 0, rot('y', -.3 * s)), RED)
# the spear prow
M.add('spear', lambda p: rcone(p, (2.3, -.05, 0), (3.35, -.12, 0), .2, .01), GUN)
M.add('spearC', lambda p: hull(p, [(2.9, 0), (2.4, .2), (2.1, .2), (2.1, 0)], .1, -.22, .06), PLATE, .02)
# the central pylon and its folding fan array
M.add('py', lambda p: box(p, (-.25, .9, 0), (.16, .5, .14), .03), GUN, .03)
M.add('pyb', lambda p: box(p, (-.25, .55, 0), (.3, .12, .22), .03), PLATE, .02)
M.add('hub', lambda p: cyl(p, (-.25, 1.45, 0), 'z', .17, .16, .03), GUN)
M.add('hubR', lambda p: cyl(p, (-.25, 1.45, 0), 'z', .08, .19, .02), RED)
def fan_panel(a, tilt, Lp=1.15, W=.4):
    # one lattice panel of the fan: spread fore and aft (about z), each leaning slightly outward (about x)
    R = rot('z', a) @ rot('x', tilt); hub = np.array((-.25, 1.45, 0), f32); d = R @ np.array((0, 1, 0), f32); c = hub + d * (Lp / 2 + .16)
    def frame(p):
        q = (p - c) @ R; outer = box(q, (0, 0, 0), (W / 2, Lp / 2, .022), .006); inner = box(q, (0, 0, 0), (W / 2 - .045, Lp / 2 - .045, .1))
        return np.maximum(outer, -inner)
    def grid(p):
        q = (p - c) @ R; g = q.copy(); g[..., 0] = np.mod(g[..., 0] + 9, .14) - .07; g[..., 1] = np.mod(g[..., 1] + 9, .14) - .07
        bars = np.minimum(np.abs(g[..., 0]), np.abs(g[..., 1])) - .013
        return np.maximum(np.maximum(bars, np.abs(q[..., 2]) - .016), box(q, (0, 0, 0), (W / 2 - .03, Lp / 2 - .03, .2)))
    glass = lambda p: box((p - c) @ R, (0, 0, 0), (W / 2 - .035, Lp / 2 - .035, .007))
    arm = lambda p: cap(p, tuple(hub + d * .05), tuple(hub + d * .5), .04)
    return frame, grid, glass, arm
for i, a in enumerate(np.linspace(-1.0, 1.0, 6)):
    fr, gr, gl, ar = fan_panel(a, (.18 if i % 2 else -.18))
    M.add(f'fF{i}', fr, GUN); M.add(f'fG{i}', gr, GUN); M.add(f'fL{i}', gl, GLASS); M.add(f'fA{i}', ar, GUN)
M.carve('pyS', lambda p: box(p, (-.25, .95, 0), (.03, .32, .2)), RED)
# two jamming dishes on outriggers, facing outward and up, red feeds
def dish(c, n, R, depth, t=.02):
    c = np.array(c, f32); n = np.array(n, f32); n /= np.linalg.norm(n); Rc = (R * R + depth * depth) / (2 * depth); sc = c - n * depth + n * Rc
    return lambda p: np.maximum(np.abs(L(p - sc) - Rc) - t, (p - c) @ n)
for s, x in ((1, .75), (-1, -.95)):
    c = (x, .78, .82 * s); n = (.1, .55, .85 * s)
    M.add(f'arm{s}', lambda p, s=s, x=x: cap(p, (x, .3, .3 * s), (x, .6, .7 * s), .07), GUN)
    M.add(f'mnt{s}', lambda p, s=s, x=x: sphere(p, (x, .6, .7 * s), .11), GUN)
    M.add(f'dsh{s}', dish(c, n, .42, .13), PLATE)
    nn = np.array(n, f32) / np.linalg.norm(n); tip = tuple(np.array(c, f32) + nn * .32); base = tuple(np.array(c, f32) - nn * .1)
    M.add(f'fd{s}', lambda p, a=base, b=tip: cap(p, a, b, .025), GUN)
    M.add(f'fdR{s}', lambda p, b=tip: sphere(p, b, .06), RED)
    M.add(f'fdC{s}', lambda p, a=base: sphere(p, a, .07), RED)
# antenna masts along the deck
for i, (x, z, h) in enumerate(((1.25, .12, .5), (1.0, -.16, .38), (.45, .22, .62), (.3, -.24, .48), (-.75, .25, .55), (-1.05, -.2, .45), (-1.45, .1, .35), (1.9, 0, .3))):
    M.add(f'ant{i}', lambda p, x=x, z=z, h=h: cap(p, (x, .4, z), (x, .4 + h, z), .016), GUN)
for s in (1, -1):
    engine(M, f'eng{s}', -2.15, 0, .2 * s, .2, .4)
M.carve('seams', seams(body, .45), DARK)
M.carve('slits', slit_rows(body, [.18], -1.9, 1.4, .2), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.35, sy=.25, sz=.3))
