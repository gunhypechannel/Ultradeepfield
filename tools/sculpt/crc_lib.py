# The Carcinid's sculpted bodies (v751), after the owner's paintings in docs/art/carcinid/: armoured crabs of overlapping
# copper-violet plates with gold edges and blade spikes, cyan light in every seam, eyes and joint; thick plated legs ending in gold
# points; huge serrated claws. One parametric crab (the same knobs as the game's CRC_CRAB) and the frame the game animates:
# +x forward, claws past x 1.3, legs out beyond |z| .95, y up (see MON_WAVE's crab wave).
import numpy as np
from sdf import *
TINT = {  # shell, plate, rim, glow (rgb, emissive)
    'copper': ((.06, .025, .08), (.3, .12, .075), (.9, .56, .2), (.05, .9, .85)),
    'blue': ((.02, .025, .06), (.06, .085, .2), (.85, .6, .26), (.06, .85, 1.0)),
    'red': ((.16, .02, .015), (.55, .07, .035), (.9, .42, .12), (1.0, .45, .08)),
    'pearl': ((.15, .17, .21), (.48, .5, .56), (.85, .78, .62), (.1, .9, .85)),
    'pale': ((.12, .17, .2), (.4, .48, .53), (.72, .86, .92), (.08, .95, .9)),
    'gold': ((.08, .05, .03), (.45, .28, .07), (.95, .66, .22), (.95, .7, .25)),
    'oracle': ((.06, .025, .1), (.22, .07, .36), (.72, .5, .9), (.7, .25, 1.0)),
    'krak': ((.06, .02, .07), (.2, .04, .2), (.85, .45, .3), (.85, .2, .95)),
    'coral': ((.14, .05, .05), (.52, .18, .1), (.88, .5, .2), (.15, .9, .8)),
}
def mats(t):
    sh, pl, rim, gl = TINT.get(t or 'copper', TINT['copper'])
    return dict(SHELL={'c': sh, 'r': .32, 'm': .6}, PLATE={'c': pl, 'r': .3, 'm': .85}, RIM={'c': rim, 'r': .24, 'm': .95},
                TIP={'c': tuple(min(1, x * 1.15) for x in rim), 'r': .18, 'm': .95}, GLOW={'c': tuple(x * .12 for x in gl), 'r': .2, 'm': .1, 'e': gl},
                CORAL={'c': (.6, .06, .05), 'r': .7, 'm': .05, 'e': (.12, 0, 0)}, PURP={'c': (.35, .08, .45), 'r': .7, 'm': .05, 'e': (.18, .02, .25)},
                BARN={'c': (.5, .45, .36), 'r': .8, 'm': .05}, CRYS={'c': (.25, .7, .75), 'r': .05, 'm': .2, 'e': (.1, .55, .6)},
                PEARL={'c': (.85, .86, .9), 'r': .08, 'm': .3, 'e': (.12, .14, .16)}, DARK={'c': (.01, .01, .015), 'r': .5, 'm': .3})
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def bez(a, b, c, t): return lerp(lerp(a, b, t), lerp(b, c, t), t)
def chain(M, n, pts, rads, mat, k=0):
    for i in range(len(pts) - 1):
        M.add(f'{n}{i}', lambda p, a=pts[i], b=pts[i + 1], r1=rads[i], r2=rads[i + 1]: rcone(p, a, b, r1, r2), mat, k)
def curved(M, n, a, ctrl, b, r0, r1, mat, seg=6, k=0):
    pts = [bez(a, ctrl, b, i / seg) for i in range(seg + 1)]; rads = [r0 + (r1 - r0) * (i / seg) ** .9 for i in range(seg + 1)]
    chain(M, n, pts, rads, mat, k); return pts, rads
def spk(M, n, base, d, L, r, mat):
    tip = tuple(base[i] + d[i] * L for i in range(3)); M.add(n, lambda p: spike(p, base, tip, r), mat)
def blade(M, n, base, d, L, r, mat, flat=2.4, up=(0, 1, 0)):
    # a spike flattened across 'up' (a blade edge-on from the side), base buried a little in what it grows from
    tip = tuple(base[i] + d[i] * L for i in range(3)); u = np.array(norm(up), np.float32); b = np.array(base, np.float32)
    def f(p):
        q = p - b; k = (q @ u)[..., None]; q2 = q + u * k * (flat - 1); return spike(q2 + b, base, tip, r)
    M.add(n, f, mat)
def oell(p, c, R, r):
    q = (p - np.array(c, np.float32)) @ R.T; return ell(q, (0, 0, 0), r)
def norm(v): v = np.array(v, float); return tuple(v / (np.linalg.norm(v) + 1e-9))

def crab(M, P, t=None):
    """P: w half-width, l half-length, h height, kk claw size, fg fangs, hn horn pairs, th leg thickness, plus extras."""
    C = mats(P.get('t', t)); w, l, h, kk, th = P['w'], P['l'], P['h'], P['kk'], P['th']; legs = P.get('legs', 3)
    yb = .1  # body centre height
    # the body: a dark core with cyan light along its lower flanks, under a domed shield of overlapping plates
    M.add('core', lambda p: ell(p, (0, yb, 0), (l * .92, h * .48, w * .8)), C['SHELL'])
    M.add('belly', lambda p: ell(p, (-.05, yb - h * .18, 0), (l * .78, h * .3, w * .86)), C['GLOW'], .06)
    shield = lambda p: ell(p, (-.05, yb + h * .2, 0), (l * 1.06, h * .98, w * 1.04))
    M.add('shield', lambda p: np.maximum(shield(p), yb - .02 - p[..., 1]), C['PLATE'], .05)
    # armour scales over the dome, each a thick copper plate on a gold under-plate, laid like roof shingles from the back forward,
    # its rear edge lifting into a blade; the dark shell and cyan light show in the gaps between them
    SC = (-.05, yb + h * .2, 0); SR = (l * 1.06, h * .98, w * 1.04)
    rows = P.get('rows', 4) + 1; sz = P.get('ss', 1.0)
    for i in range(rows):
        u = i / (rows - 1); x = l * (.72 - 1.62 * u); ncol = 3 + 2 * (i % 2 == 0)
        for j in range(ncol):
            v = (j - (ncol - 1) / 2) / ((ncol - 1) / 2 + .6); z = v * w * .95
            q = 1 - ((x - SC[0]) / SR[0]) ** 2 - (z / SR[2]) ** 2
            if q < .06: continue
            y = SC[1] + SR[1] * np.sqrt(q); n = norm(((x - SC[0]) / SR[0] ** 2, (y - SC[1]) / SR[1] ** 2, z / SR[2] ** 2))
            f = np.array((1., 0, 0)) - np.array(n) * n[0]; f = tuple(f / np.linalg.norm(f)); sd = tuple(np.cross(n, f))
            R = np.array([f, sd, n], np.float32); r0 = (.5 * l / rows * 2.1 * sz, .36 * w / 2.2 * sz * (1.15 - .2 * abs(v)) + .12, .1)
            c = tuple(np.array((x, y, z)) + np.array(n) * .03)
            M.add(f'su{i}{j}', lambda p, c=c, R=R, r0=r0: oell(p, (c[0] - R[0][0] * .06 - R[2][0] * .03, c[1] - R[0][1] * .06 - R[2][1] * .03, c[2] - R[0][2] * .06 - R[2][2] * .03), R, (r0[0] * 1.12, r0[1] * 1.1, r0[2] * .7)), C['RIM'])
            M.add(f'sc{i}{j}', lambda p, c=c, R=R, r0=r0: oell(p, c, R, r0), C['PLATE'])
            tb = tuple(np.array(c) - np.array(f) * r0[0] * .55 + np.array(n) * .05)
            blade(M, f'sb{i}{j}', tb, norm(tuple(-np.array(f) * .8 + np.array(n) * .9)), .32 * P.get('sp', 1) * sz + .1, .1, C['RIM'], flat=3, up=tuple(sd))
    M.carve('ridge', lambda p: np.maximum(box(p, (0, yb + h * 1.18, 0), (l, .05, .03)), ell(p, SC, SR) + .03), C['GLOW'])
    # the rim: blade spikes all round the shield's edge, longer at the front corners, curling up and out
    nr = P.get('rim', 14)
    for j in range(nr):
        a = (j + .5) / nr * 2 * np.pi; cx, cz = np.cos(a), np.sin(a)
        if cx > .75: continue  # the face stays clear
        base = (cx * l * .95, yb + h * .12, cz * w * .93); L = (.32 + .3 * max(0, cx + .3)) * P.get('sp', 1)
        blade(M, f'rim{j}', base, norm((cx * .9, .22, cz)), L * 1.6 + .35, .26, C['RIM'], flat=3.2)
    for j in range(P.get('spikes', 0)):  # dorsal spines
        u = j / max(1, P['spikes'] - 1); s = 1 if j % 2 else -1; base = (l * (.5 - u * 1.1), yb + h * 1.08, s * w * (.25 + .25 * ((j // 2) % 2)))
        spk(M, f'dsp{j}', base, norm((-.3, 1, s * .25)), .35 + .25 * (1 - u), .07, C['RIM'])
    # the face: a heavy brow, two glowing eyes in gold sockets, horns, and fangs below
    M.add('brow', lambda p: ell(p, (l * .82, yb + h * .18, 0), (l * .28, h * .26, w * .55)), C['PLATE'], .04)
    for s in (1, -1):
        M.add(f'sock{s}', lambda p, s=s: sphere(p, (l * .98, yb + h * .16, s * w * .24), .16), C['RIM'], .02)
        M.add(f'eye{s}', lambda p, s=s: sphere(p, (l * 1.07, yb + h * .17, s * w * .24), .12), C['GLOW'])
        for k in range(P.get('hn', 1)):
            base = (l * (.9 - .12 * k), yb + h * .3, s * w * (.42 + .14 * k)); spk(M, f'horn{s}{k}', base, norm((.9, .5 - .1 * k, s * .25)), .45 + .1 * k, .07, C['RIM'])
        for k in range(P.get('fg', 4) // 2):
            base = (l * .96, yb - h * .08, s * (.08 + .07 * k)); spk(M, f'fang{s}{k}', base, norm((.55, -1, s * .15)), .22 + .04 * (k % 2), .045, C['TIP'])
        if P.get('ant'):
            curved(M, f'ant{s}', (l * 1.0, yb + h * .2, s * .12), (l * 1.6, yb + h * 1.8, s * .5), (l * .4, yb + h * 2.6, s * 1.4), .025, .008, C['RIM'], 8)
    # the claws: a two-segment arm and a great serrated chela pointing forward, a little inward
    for s in (1, -1):
        sh = (l * .62, yb - .05, s * w * .66); el = (l * .95, yb + .12, s * (w * .9 + .25 * kk)); wr = (l * 1.12 + .2 * kk, yb, s * (w * .78 + .1))
        chain(M, f'arm{s}', [sh, el, wr], [.16 * th, .19 * th * kk ** .4, .15 * th * kk ** .4], C['PLATE'], .03)
        M.add(f'elb{s}', lambda p, el=el: sphere(p, el, .15 * th * kk ** .4), C['RIM'], .02)
        pc = (wr[0] + .55 * kk, yb + .02, s * (w * .72)); pr = (.62 * kk, .3 * kk, .28 * kk)
        M.add(f'palm{s}', lambda p, pc=pc, pr=pr: ell(p, pc, pr), C['PLATE'], .06)
        M.add(f'palmr{s}', lambda p, pc=pc, pr=pr: np.maximum(np.maximum(ell(p, (pc[0], pc[1] + pr[1] * .25, pc[2]), (pr[0] * .9, pr[1] * .82, pr[2] * 1.06)), pc[1] + pr[1] * .62 - p[..., 1]), np.abs(p[..., 2] - pc[2]) - pr[2] * .35), C['RIM'])
        for j in range(3):  # knobs along the top of the hand
            blade(M, f'pk{s}{j}', (pc[0] - pr[0] * (.5 - .45 * j), pc[1] + pr[1] * .75, pc[2]), norm((.5, 1, s * .2)), .32 * kk, .08 * kk, C['RIM'], up=(0, 0, 1))
        f0 = (pc[0] + pr[0] * .8, pc[1] - pr[1] * .25, pc[2]); g0 = (pc[0] + pr[0] * .7, pc[1] + pr[1] * .35, pc[2])
        fix, fr = curved(M, f'fix{s}', f0, (f0[0] + 1.0 * kk, f0[1] - .12 * kk, f0[2] - s * .05), (f0[0] + 1.35 * kk, f0[1] + .3 * kk, f0[2] - s * .28 * kk), .17 * kk, .02, C['PLATE'], 7)
        dac, dr = curved(M, f'dac{s}', g0, (g0[0] + .9 * kk, g0[1] + .38 * kk, g0[2] - s * .05), (g0[0] + 1.45 * kk, g0[1] - .12 * kk, g0[2] - s * .3 * kk), .19 * kk, .02, C['PLATE'], 7)
        for j in range(1, 6):  # teeth on the inner edges
            a = fix[j]; spk(M, f'ft{s}{j}', (a[0], a[1] + fr[j] * .5, a[2]), norm((.4, 1, 0)), .17 * kk * (1.2 - j * .12), .05 * kk, C['TIP'])
            a = dac[j]; spk(M, f'dt{s}{j}', (a[0], a[1] - dr[j] * .5, a[2]), norm((.4, -1, 0)), .17 * kk * (1.2 - j * .12), .05 * kk, C['TIP'])
        M.add(f'fxt{s}', lambda p, a=fix[-2], b=fix[-1]: spike(p, a, b, .06 * kk), C['TIP']); M.add(f'dxt{s}', lambda p, a=dac[-2], b=dac[-1]: spike(p, a, b, .07 * kk), C['TIP'])
        M.carve(f'pg{s}', lambda p, pc=pc, pr=pr: np.maximum(np.abs(p[..., 1] - pc[1]) - .018, ell(p, pc, (pr[0] * 1.01, pr[1] * 1.01, pr[2] * 1.01)) + .015) , C['GLOW'])
    # the legs: plated segments up to a high knee and down to a gold point, a spine on each segment
    for s in (1, -1):
        for i in range(legs):
            u = i / max(1, legs - 1); x0 = l * (.35 - .95 * u); sp = 1.0 + .25 * (1 - abs(u - .5) * 2)
            a = (x0, yb - .05, s * w * .7); kn = (x0 - .1 + .15 * (1 - u), yb + h * .55 + .35, s * (w + .75 * sp)); an = (x0 - .25 + .45 * (1 - u), yb - .25, s * (w + 1.3 * sp)); ft = (x0 - .3 + .55 * (1 - u), -.85, s * (w + 1.55 * sp))
            chain(M, f'leg{s}{i}', [a, kn, an], [.11 * th, .1 * th, .08 * th], C['SHELL'], .02)
            for (q0, q1, r0) in ((a, kn, .22), (kn, an, .17)):
                for j in range(2):  # two plated sleeves per segment, wide at the near end, each with a blade rising off its back
                    u0, u1 = j / 2 - .02, (j + 1) / 2 + .14; A0 = lerp(q0, q1, u0); B0 = lerp(q0, q1, u1)
                    M.add(f'sv{s}{i}{r0}{j}', lambda p, A=A0, B=B0, r0=r0: rcone(p, A, B, r0 * th * 1.05, r0 * th * .16), C['PLATE'])
                    dd = norm(tuple(B0[t] - A0[t] for t in range(3))); bb = lerp(A0, B0, .3)
                    blade(M, f'svb{s}{i}{r0}{j}', (bb[0], bb[1] + r0 * th * .6, bb[2]), norm((dd[0] * .7, .8 + dd[1] * .7, dd[2] * .7)), .3 * th, .07 * th, C['RIM'], up=(0, 0, 1))
                M.add(f'svg{s}{i}{r0}', lambda p, q=lerp(q0, q1, .5), r0=r0: sphere(p, q, r0 * th * .7), C['GLOW'])
            curved(M, f'tip{s}{i}', an, (an[0] + .15, an[1] - .1, an[2] + s * .45), ft, .1 * th, .012, C['TIP'], 5)
            for q, r0 in ((kn, .15), (an, .1)): M.add(f'jt{s}{i}{q[0]:.2f}', lambda p, q=q, r0=r0: sphere(p, q, r0 * th), C['GLOW'], .02)
            blade(M, f'kns{s}{i}', kn, norm((-.2, 1, s * .3)), .4 * th, .09 * th, C['RIM'])
            mid = lerp(a, kn, .55); spk(M, f'ls{s}{i}', (mid[0], mid[1] + .06, mid[2]), norm((-.2, 1, s * .4)), .22, .045 * th, C['RIM'])
            mid = lerp(kn, an, .4); spk(M, f'ls2{s}{i}', mid, norm((-.4, .2, s * 1)), .18, .04 * th, C['RIM'])
    extras(M, P, C, yb)
    return C

def extras(M, P, C, yb):
    w, l, h = P['w'], P['l'], P['h']; rng = np.random.default_rng(int(sum(map(ord, P.get('k', 'x')))))
    top = yb + h * 1.12
    def yt(x, z): return yb + h * .2 + h * .98 * np.sqrt(max(.05, 1 - ((x + .05) / (l * 1.06)) ** 2 - (z / (w * 1.04)) ** 2)) + .06
    for j in range(P.get('coral', 0)):  # branching red coral and violet tufts on the back
        x = rng.uniform(-l * .6, l * .45); z = rng.uniform(-w * .55, w * .55); c = C['CORAL'] if j % 3 else C['PURP']; base = (x, yt(x, z) - .05, z)
        for b in range(3):
            d = norm((rng.uniform(-.6, .6), 1, rng.uniform(-.6, .6))); L = rng.uniform(.4, .75); tip = tuple(base[i] + d[i] * L for i in range(3))
            M.add(f'cor{j}{b}', lambda p, a=base, b2=tip: cap(p, a, b2, .06), c)
            for e in range(2):
                d2 = norm((d[0] + rng.uniform(-.8, .8), 1, d[2] + rng.uniform(-.8, .8))); m = lerp(base, tip, .6); t2 = tuple(m[i] + d2[i] * L * .5 for i in range(3))
                M.add(f'cor{j}{b}{e}', lambda p, a=m, b2=t2: cap(p, a, b2, .04), c)
    for j in range(P.get('barn', 0)):  # barnacles
        x = rng.uniform(-l * .5, l * .4); z = rng.uniform(-w * .6, w * .6)
        M.add(f'bar{j}', lambda p, c=(x, yt(x, z) - .03, z): np.maximum(cyl(p, c, 'y', .13, .1, .02), -cyl(p, (c[0], c[1] + .1, c[2]), 'y', .065, .06)), C['BARN'])
    for j in range(P.get('crys', 0)):  # glowing crystals
        x = rng.uniform(-l * .6, l * .4); z = rng.uniform(-w * .6, w * .6); d = norm((rng.uniform(-.5, .5), 1, rng.uniform(-.5, .5))); L = rng.uniform(.4, .8)
        spk(M, f'crys{j}', (x, yt(x, z) - .1, z), d, L, .09, C['CRYS'])
    if P.get('crest'):
        for j in range(P['crest']):
            u = j / max(1, P['crest'] - 1); spk(M, f'cre{j}', (l * (.3 - .9 * u), top, 0), norm((-.5, 1, 0)), .55 + .35 * np.sin(u * np.pi), .08, C['RIM'])
    if P.get('crown'):
        for j in range(9):
            a = j / 9 * 2 * np.pi; c = (l * .1 + .35 * np.cos(a), top + .05, .35 * np.sin(a)); spk(M, f'crn{j}', c, norm((np.cos(a) * .3, 1, np.sin(a) * .3)), .45 + .2 * (j % 2), .06, C['RIM'])
        M.add('crwg', lambda p: sphere(p, (l * .1, top + .15, 0), .16), C['GLOW'])
    if P.get('turret'):  # the Spitter's coral cannon on its back
        M.add('tur', lambda p: ell(p, (-.1, top + .1, 0), (.35, .25, .35)), C['PLATE'], .05)
        M.add('tub', lambda p: rcone(p, (-.05, top + .2, 0), (.6, top + .55, 0), .14, .1), C['RIM'])
        M.add('tug', lambda p: sphere(p, (.62, top + .56, 0), .09), C['GLOW'])
    if P.get('sacs'):  # the Harvester's glowing tanks
        for j in range(3):
            M.add(f'sac{j}', lambda p, j=j: ell(p, (-.55 + .45 * j, top + .12, 0), (.24, .2, .32)), C['GLOW'], .03)
            M.add(f'sacr{j}', lambda p, j=j: ring(p, (-.55 + .45 * j, top + .12, 0), 'x', .3, .03, .04), C['RIM'])
    if P.get('abdo'):  # a brood sac behind
        M.add('abdo', lambda p: ell(p, (-l * 1.35, yb + .1, 0), (l * .8, h * .55, w * .7)), C['GLOW'], .12)
        for j in range(5): M.add(f'abr{j}', lambda p, j=j: np.maximum(np.abs(ell(p, (-l * 1.35, yb + .1, 0), (l * .8, h * .55, w * .7))) - .035, np.abs(p[..., 0] + l * (.85 + .22 * j)) - .045), C['RIM'])
    if P.get('pearls'):
        for j in range(6):
            a = j / 6 * 2 * np.pi; M.add(f'prl{j}', lambda p, c=(l * .05 + .3 * np.cos(a), top + .1, .3 * np.sin(a)): sphere(p, c, .12), C['PEARL'])
    if P.get('eye3'):
        M.add('eye3r', lambda p: torus(p, (0, top + .75, 0), 'x', .45, .04), C['RIM']); M.add('eye3', lambda p: sphere(p, (0, top + .75, 0), .22), C['GLOW'])
        M.add('eye3s', lambda p: cap(p, (0, top, 0), (0, top + .5, 0), .06), C['PLATE'])
    if P.get('tail'):  # a lobster's tail fan behind
        for j in range(6):
            x = -l * (.85 + .36 * j); rr = w * (.5 - .045 * j)
            M.add(f'tl{j}', lambda p, x=x, rr=rr: ell(p, (x, yb + .05, 0), (l * .26, rr * .75, rr)), C['PLATE'], .03)
            M.add(f'tlr{j}', lambda p, x=x, rr=rr: np.maximum(np.abs(ell(p, (x, yb + .05, 0), (l * .27, rr * .78, rr * 1.03))) - .02, np.abs(p[..., 0] - x - l * .2) - .04), C['RIM'])
            blade(M, f'tlb{j}', (x, yb + .05 + rr * .6, 0), norm((-.6, 1, 0)), .3, .07, C['RIM'], up=(0, 0, 1))
        for s in (-1, 0, 1): M.add(f'fan{s}', lambda p, s=s: ell(p, (-l * 3.0, yb, s * .3), (.5, .06, .24)), C['RIM'])
    if P.get('tent'):  # the Krakenbreaker's grafted arms
        for j in range(P['tent']):
            s = 1 if j % 2 else -1; u = (j // 2) / max(1, P['tent'] // 2 - 1); a = (-l * (.2 + .6 * u), yb + h * .3, s * w * .5)
            curved(M, f'ten{j}', a, (-l * (.8 + .5 * u), yb + h * (1.6 + .5 * u), s * (w + .5)), (-l * (1.6 + .6 * u), yb + h * (.6 + .8 * u), s * (w + 1.3)), .12, .02, C['PLATE'], 8)
    if P.get('city'):  # towers on the back of the oldest guardians
        for j in range(9):
            x = rng.uniform(-l * .5, l * .3); z = rng.uniform(-w * .45, w * .45); H = rng.uniform(.4, 1.0)
            M.add(f'twr{j}', lambda p, c=(x, top + H / 2, z), H=H: box(p, c, (.08, H / 2, .08), .02), C['RIM'])
            M.add(f'twl{j}', lambda p, c=(x + .081, top + H * .6, z): box(p, c, (.005, H * .3, .03)), C['GLOW'])
    if P.get('molt'):  # a split old shell lifting off
        M.add('molt', lambda p: np.maximum(np.maximum(np.abs(ell(p, (-l * .35, yb + h * .45, 0), (l * .85, h * .95, w * .95))) - .035, yb + h * .6 - p[..., 1]), p[..., 0] + l * .05), C['PEARL'])
        M.carve('moltc', lambda p: box(p, (0, top + .4, 0), (l, .4, .06)), C['GLOW'])

def paint(P, N, A, E, idx):
    v = .5 * panels(P, .35, .3, .3) + .5 * hashf(idx.astype(np.int64), idx.astype(np.int64) * 7 + 1, 3); glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05
    A[~glowing, :3] *= (.62 + .76 * v[~glowing])[:, None]
    top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .25 * top)[:, None]
    E[glowing, :3] *= (.75 + .5 * v[glowing])[:, None]
