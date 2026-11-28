# The Fabrication Carrier (owner's painting, art/rwar/c_fabcarrier.webp): a long boxy plated hull with a flat deck, a faceted prow of
# stacked armour blades sweeping down and forward like claws, three open fabrication bays down each flank (red-lit, with gold robot
# arms welding new fighters that sit on launch rails), a command tower with spires at the stern and blue-lit engines.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
BAY = {'c': (.035, .012, .012), 'r': .5, 'm': .4, 'e': (.11, .012, .008)}; ARM = {'c': (.36, .25, .1), 'r': .3, 'm': 1}
SPARK = {'c': (.4, .25, .1), 'r': .3, 'm': 0, 'e': (2.2, 1.1, .35)}; BLUE = {'c': (.03, .05, .08), 'r': .3, 'm': .2, 'e': (.2, .55, 1.0)}
body = lambda p: np.maximum(hull(p, [(2.6, 0), (2.3, .9), (-3.2, .95), (-3.4, .85), (-3.4, 0)], .42, -.55, .12),
                            profile(p, [(2.9, -.2), (2.3, .45), (-3.5, .45), (-3.5, -.6), (2.0, -.6)]))
BAYS = ((1.55, .55), (.35, -.75), (-.95, -2.05))  # (front x, back x) of each flank bay
def bays(p):
    d = None
    for s in (1, -1):
        for xf, xb in BAYS:
            b = box(p, ((xf + xb) / 2, -.08, .95 * s), ((xf - xb) / 2, .3, .5), .02); d = b if d is None else np.minimum(d, b)
    return d
hullb = lambda p: np.maximum(body(p), -bays(p))
M = Model((-4.0, -1.5, -1.75), (3.9, 2.0, 1.75), float(sys.argv[2]) if len(sys.argv) > 2 else .03)
M.add('body', hullb, HULL)
M.add('deck', lambda p: hull(p, [(2.2, 0), (1.9, .75), (-3.0, .8), (-3.2, 0)], .5, .38, .06), PLATE, .02)
M.add('keel', lambda p: hull(p, [(2.0, 0), (1.6, .6), (-3.0, .65), (-3.2, 0)], -.5, -.72, .08), PLATE, .03)
# the faceted prow: stacked blades, each sweeping forward and down
for i, (x0, y0, w, h, dy) in enumerate(((2.2, .3, .9, .2, -.05), (2.35, .05, .8, .2, -.3), (2.4, -.22, .7, .2, -.55), (2.3, -.48, .55, .18, -.8))):
    M.add(f'pr{i}', lambda p, x0=x0, y0=y0, w=w, h=h, dy=dy: np.maximum(hull(p, [(x0 + 1.4, 0), (x0 + .5, w * .72), (x0 - .3, w), (x0 - .3, 0)], y0 + h, y0 - h, .08),
                                                                  profile(p, [(x0 + 1.45, y0 + dy), (x0 - .4, y0 + h + .05), (x0 - .4, y0 - h - .05)])), PLATE, .02)
for s in (1, -1):
    M.add(f'cw{s}', lambda p, s=s: spike(p, (2.2, -.35, .7 * s), (3.3, -.95, .55 * s), .16), PLATE)
    M.add(f'cw2{s}', lambda p, s=s: spike(p, (1.9, -.2, .85 * s), (2.9, -.6, .95 * s), .12), PLATE)
    for j, (xf, xb) in enumerate(BAYS):
        xm, hx = (xf + xb) / 2, (xf - xb) / 2
        # the open bay, its red-lit walls, and the armoured frames either side of it
        M.add(f'bw{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, -.08, .465 * s), (hx, .3, .02)), BAY)
        M.add(f'bc{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, .205, .7 * s), (hx, .02, .25)), BAY)
        for xe in (xf + .06, xb - .06):
            M.add(f'fr{s}{j}{xe:.2f}', lambda p, s=s, xe=xe: box(p, (xe, -.08, .93 * s), (.07, .42, .1), .02), PLATE)
        for xr in np.linspace(xb + .15, xf - .15, 4):
            M.add(f'rib{s}{j}{xr:.2f}', lambda p, s=s, xr=xr: box(p, (xr, -.08, .5 * s), (.025, .28, .03), .005), GUN)
        M.add(f'bl1{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, .08, .49 * s), (hx * .92, .012, .012)), RED)
        M.add(f'bl2{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, -.2, .49 * s), (hx * .92, .012, .012)), RED)
        M.add(f'floor{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, -.36, .78 * s), (hx, .025, .2), .01), GUN)
        M.add(f'lite{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm, .19, .62 * s), (hx * .9, .018, .03), .005), RED)
        # a gold robot arm from the ceiling, its welding tip sparking over a half-built fighter
        sh = (xm + hx * .45, .16, .6 * s); el = (xm + hx * .2, .02, .82 * s); tp = (xm - hx * .05, -.18, .8 * s)
        M.add(f'a1{s}{j}', lambda p, a=sh, b=el: cap(p, a, b, .07), ARM); M.add(f'a2{s}{j}', lambda p, a=el, b=tp: cap(p, a, b, .055), ARM)
        M.add(f'aj{s}{j}', lambda p, a=el: sphere(p, a, .085), GUN); M.add(f'sp{s}{j}', lambda p, a=tp: sphere(p, a, .06), SPARK)
        M.add(f'crate{s}{j}', lambda p, s=s, xm=xm, hx=hx: box(p, (xm - hx * .7, -.22, .66 * s), (.1, .12, .1), .015), BLACK)
        # fighters on launch rails, noses poking out of the bay
        for k, (dx, dy) in enumerate(((-.12, -.27), (.25, -.05))):
            fx, fy = xm + dx, -.08 + dy
            M.add(f'rail{s}{j}{k}', lambda p, s=s, fx=fx, fy=fy: box(p, (fx, fy - .05, 1.08 * s), (.06, .012, .4), .005), GUN)
            M.add(f'ft{s}{j}{k}', lambda p, s=s, fx=fx, fy=fy: prism(p, [(fx, 1.62 * s), (fx + .24, .9 * s), (fx + .1, .85 * s), (fx - .1, .85 * s), (fx - .24, .9 * s)][::s], fy + .03, fy - .02, .015, .005), PLATE)
            M.add(f'fe{s}{j}{k}', lambda p, s=s, fx=fx, fy=fy: sphere(p, (fx, fy + .005, .98 * s), .028), RED)
    M.carve(f'sl{s}', lambda p, s=s: box(p, (-2.7, .1, .95 * s), (.45, .015, .1)), RED)
    M.carve(f'sl2{s}', lambda p, s=s: box(p, (1.95, .1, .9 * s), (.25, .015, .1)), RED)
# the command tower and spires at the stern, a smaller spire cluster forward
M.add('tw', lambda p: hull(p, [(-2.3, 0), (-2.55, .38), (-3.15, .42), (-3.3, 0)], .9, .4, .1), HULL, .04)
M.add('tw2', lambda p: hull(p, [(-2.55, 0), (-2.7, .22), (-3.05, .25), (-3.15, 0)], 1.15, .85, .06), PLATE, .02)
M.add('twc', lambda p: cyl(p, (-2.85, 1.22, 0), 'y', .3, .05, .02), GUN)
M.carve('tws', lambda p: box(p, (-2.4, .72, 0), (.1, .025, .3)), RED)
for i, (x, z, h) in enumerate(((-2.8, .1, .75), (-2.95, -.12, .6), (-2.7, -.05, .5), (-3.05, .15, .4))):
    M.add(f'spr{i}', lambda p, x=x, z=z, h=h: rcone(p, (x, 1.2, z), (x, 1.2 + h, z), .04, .008), GUN)
    M.add(f'sprR{i}', lambda p, x=x, z=z, h=h: sphere(p, (x, 1.2 + h * .7, z), .025), RED)
for i, (x, z, h) in enumerate(((1.75, .1, .55), (1.6, -.08, .45), (1.85, -.15, .35))):
    M.add(f'fs{i}', lambda p, x=x, z=z, h=h: rcone(p, (x, .5, z), (x, .5 + h, z), .035, .006), GUN)
M.add('fsb', lambda p: box(p, (1.72, .56, 0), (.18, .06, .2), .02), PLATE)
# blue-lit engines
for (y, z, r) in ((0, .55, .32), (0, -.55, .32), (.3, 0, .26)):
    n = f'e{y}{z}'
    M.add(n, lambda p, y=y, z=z, r=r: cyl(p, (-3.6, y, z), 'x', r, .22, r * .15), GUN)
    M.add(n + 'b', lambda p, y=y, z=z, r=r: ring(p, (-3.5, y, z), 'x', r * 1.03, r * .14, r * .12), BLACK)
    M.carve(n + 't', lambda p, y=y, z=z, r=r: cyl(p, (-3.85, y, z), 'x', r * .66, r * .3), BLUE)
M.carve('seams', lambda p: np.maximum(seams(body, .6)(p), -bays(p) - .05), DARK)
M.carve('deckL', slit_rows(hullb, [.27], -2.2, 2.0, .5, .012, .2), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.55, sy=.35, sz=.45))
