# The space monsters sculpted after the owner's paintings (docs/art/mon/<k>.webp): python3 mon_sculpt.py <key> <outdir> [voxel].
# Each keeps the procedural model's frame and proportions (+x the head, y up), because the game's swim waves (MON_WAVE) bend
# the mesh by position: the shark's S-wave grows toward the tail past x 2.2, the squid's arms move past x -.9, the manta's wings
# beyond |z| .9 and its tail past x -1.9, the moth's wings beyond |z| .38, the ram's comet tail past x -2.2.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, bez, chain, curved, spk, blade, norm, oell

def M_(c, r=.5, m=.1, e=None): d = {'c': c, 'r': r, 'm': m}; d.update({'e': e} if e else {}); return d
def lathe_x(p, prof, sy=1.0, sz=1.0, c=(0, 0, 0)):
    """a body of revolution along x: prof [(x, r)...] head to tail, scaled sy, sz across"""
    xs = np.array([a for a, _ in prof][::-1], f32); rs = np.array([b for _, b in prof][::-1], f32)
    q = p - V(*c); x = q[..., 0]; r = np.interp(x, xs, rs, left=0, right=0)
    d = np.sqrt((q[..., 1] / sy) ** 2 + (q[..., 2] / sz) ** 2) - r
    return np.maximum(d * min(sy, sz) * .9, np.maximum(x - xs[-1], xs[0] - x))
def _fin(p, pts, th, c, R):  # a flat fin: a convex outline [(x, y)...] of thickness th at c, R its local-to-world turn (rows = world)
    q = p - V(*c)
    if R is not None: q = q @ R
    d2 = poly2(q[..., 0], q[..., 1], pts); return np.maximum(d2, np.abs(q[..., 2]) - th / 2) - th * .3
def Rz(a): return rot('z', a)
def seg2(x, z, A, B):  # distance in the x-z plane to the segment A-B
    ax, az = A; bx, bz = B; dx, dz = bx - ax, bz - az; t = np.clip(((x - ax) * dx + (z - az) * dz) / (dx * dx + dz * dz), 0, 1)
    return np.sqrt((x - ax - t * dx) ** 2 + (z - az - t * dz) ** 2)
def Rx(a): return rot('x', a)
def Ry(a): return rot('y', a)

# ---------------------------------------------------------------- the Void Shark (art: a great white, open jaws, scars of blue light)
def shark(M):
    HIDE = M_((.035, .045, .06), .34, .12); BELLY = M_((.36, .38, .41), .4, .06); SEAM = M_((.01, .015, .02), .5, .2); DARK = M_((.02, .02, .03), .6, .1); GUM = M_((.4, .05, .07), .5, .05, (.12, .01, .02))
    BONE = M_((.9, .88, .8), .3, .05); GLOW = M_((.0, .08, .16), .2, .1, (.1, .55, 1.0)); EYE = M_((.02, .05, .1), .1, .3, (.25, .7, 1.0)); GUN = M_((.07, .08, .1), .22, .9); CY = M_((.1, .5, .7), .2, .3, (.35, .9, 1.0)); RED = M_((.3, .02, .02), .3, .2, (1., .18, .12))
    prof = [(3.6, 0), (3.52, .11), (3.35, .27), (3.05, .45), (2.55, .63), (1.85, .78), (1.05, .85), (.2, .82), (-.6, .7), (-1.4, .52), (-2.2, .33), (-2.85, .19), (-3.25, .13), (-3.5, .1)]
    HX, HY, JA = 2.0, -.22, .62  # v785 a wider gape
    mreg = lambda p: np.maximum(np.maximum(p[..., 1] + .06, HX + .02 - p[..., 0]), -(p[..., 1] + 1.2))  # the gape under the snout
    body0 = lambda p: lathe_x(p, prof, .96, .8)
    body = lambda p: np.maximum(body0(p), -mreg(p))
    M.add('body', body, HIDE)
    M.add('palate', lambda p: np.maximum(np.maximum(body0(p) + .015, np.abs(p[..., 1] + .06) - .025), HX + .02 - p[..., 0]), GUM)
    M.add('belly', lambda p: np.maximum(body(p) - .006, p[..., 1] + .12), BELLY)  # the pale under-side
    # the open jaw, as in the painting: the snout's under-side cut away back to the hinge, the lower jaw hanging open 28 degrees,
    # a dark red throat, and rows of white teeth round both jaws
    def jawq(p):  # into the closed jaw's frame
        q = p - V(HX, HY, 0); c, sn = np.cos(JA), np.sin(JA); x = q[..., 0] * c - q[..., 1] * sn; y = q[..., 0] * sn + q[..., 1] * c
        return np.stack([x + HX, y + HY, q[..., 2]], -1)
    jprof = [(3.2, 0), (3.05, .18), (2.7, .36), (2.3, .46), (1.9, .5), (1.6, .5)]
    ljaw0 = lambda q: lathe_x(q, jprof, .5, .8, (0, -.32, 0))
    M.add('ljaw', lambda p: (lambda q: np.maximum(ljaw0(q), q[..., 1] + .34))(jawq(p)), BELLY, .04)
    M.add('ljg', lambda p: (lambda q: np.maximum(np.maximum(ljaw0(q) + .015, np.abs(q[..., 1] + .34) - .025), 1.9 - q[..., 0]))(jawq(p)), GUM)
    M.add('throat', lambda p: ell(p, (2.15, -.32, 0), (.32, .3, .4)), GUM, .05)
    M.add('tongue', lambda p: ell(jawq(p), (2.45, -.4, 0), (.45, .08, .22)), GUM)
    for row in (0, 1):
        n_ = 21 if row == 0 else 19
        for i in range(n_):
            a = (i / (n_ - 1) - .5) * 2.7
            if row == 0:
                x = 2.25 + np.cos(a) * 1.05; z = np.sin(a) * .5; y = -.07
                if x < 2.15: continue
                L_ = .25 + .12 * (1 - abs(a) / 1.35); spk(M, f'tu{i}', (x, y, z), norm((.12, -1, -z * .3)), L_, .048, BONE)
                if i % 2: spk(M, f'tv{i}', (x - .1, y + .01, z * .88), norm((.05, -1, -z * .3)), L_ * .7, .032, BONE)
            else:
                x0 = 2.2 + np.cos(a) * .9; z = np.sin(a) * .42; y0 = -.34
                if x0 < 2.1: continue
                c_, sn = np.cos(-JA), np.sin(-JA); qx, qy = x0 - HX, y0 - HY; x = HX + qx * c_ - qy * sn; y = HY + qx * sn + qy * c_
                d = norm((-.2 + np.sin(JA) * .9, np.cos(JA), -z * .3)); L_ = .22 + .1 * (1 - abs(a) / 1.35)
                spk(M, f'tl{i}', (x, y, z), d, L_, .046, BONE)
    for s in (1, -1):
        M.add(f'eye{s}', lambda p, s=s: ell(p, (2.72, .16, s * .43), (.09, .075, .05)), EYE)
        M.add(f'eyr{s}', lambda p, s=s: torus(p, (2.72, .16, s * .45), 'z', .095, .016), RED)
        for i in range(5): M.carve(f'gl{s}{i}', lambda p, s=s, i=i: np.maximum(np.maximum(np.abs(p[..., 0] - (1.85 - i * .13) - .12 * p[..., 1]) - .012, np.abs(p[..., 1] + .02) - .2), np.maximum(-s * p[..., 2], -body(p) - .05)), DARK)
        # pectorals swept back and down; pelvics
        M.add(f'pec{s}', lambda p, s=s: _fin(p, [(.55, 0), (.35, .7), (-.55, 1.3), (-.6, 0)], .07, (1.35, -.42, s * .5), Rx(s * (np.pi / 2 + .55)) @ Rz(-.18)), HIDE, .04)
        M.add(f'pel{s}', lambda p, s=s: _fin(p, [(.18, 0), (.06, .22), (-.2, .34), (-.26, 0)], .045, (-1.3, -.38, s * .28), Rx(s * (np.pi / 2 + .7))), HIDE, .02)
        # scars of light down the flanks, as in the painting
        for j, (x0, y0, L_, sl) in enumerate(((1.3, .36, 1.0, .3), (.3, .12, 1.3, .22), (-.9, .3, .9, -.25), (-1.7, .14, .7, .35), (2.15, .28, .5, -.45))):
            M.carve(f'sc{s}{j}', lambda p, s=s, x0=x0, y0=y0, L_=L_, sl=sl: np.maximum(np.maximum(np.abs((p[..., 1] - y0) - (p[..., 0] - x0) * sl) - .011, np.abs(p[..., 0] - x0) - L_ / 2), -s * p[..., 2] + .16), GLOW)
            pass  # v785 no branches: they crossed into X marks
        for j, x0 in enumerate((1.6, 1.0, .4, -.2, -.8, -1.4, -2.0)):  # armour seams across the back
            M.carve(f'se{s}{j}', lambda p, s=s, x0=x0: np.maximum(np.maximum(np.abs(p[..., 0] - x0 - .1 * p[..., 1]) - .011, -(p[..., 1] - .05)), -s * p[..., 2] - .02), SEAM)
        if False:
            M.carve(f'sc{s}{j}', lambda p, s=s, x0=x0, y0=y0, L_=L_: np.maximum(np.maximum(np.abs((p[..., 1] - y0) - (p[..., 0] - x0) * .35) - .022, np.abs(p[..., 0] - x0) - L_ / 2), -s * p[..., 2] + .2), GLOW)
    M.add('dor', lambda p: _fin(p, [(.75, 0), (.45, .95), (-.38, 1.55), (-.32, .72), (-.8, 0)], .08, (.45, .62, 0), None), HIDE, .05)
    M.add('dor2', lambda p: _fin(p, [(.25, 0), (.1, .32), (-.18, .5), (-.32, 0)], .055, (-2.15, .28, 0), None), HIDE, .03)
    M.add('anal', lambda p: _fin(p, [(.22, 0), (.08, .28), (-.16, .42), (-.3, 0)], .05, (-2.0, -.25, 0), Rx(np.pi)), HIDE, .02)
    M.add('tail', lambda p: _fin(p, [(.25, .12), (-1.4, 1.75), (-.95, .7), (-1.0, .05), (-1.08, -1.0), (.25, -.12)], .07, (-3.25, .02, 0), None), HIDE, .05)
    M.carve('nick', lambda p: sphere(p, (-4.2, .2, 0), .25), DARK)
    # two laser turrets on the back (the game's lore: twin laser turrets bolted into its hide)
    for x, y, z, sc in ((1.75, .74, 0, 1.25), (-1.05, .57, 0, 1.15), (.55, .12, .8, .9), (.55, .12, -.8, .9)):  # v785 four armoured twin turrets, cyan barrels
        M.add(f'tb{x}{z}', lambda p, x=x, y=y, z=z, k=sc: cyl(p, (x, y, z), 'y', .3 * k, .06 * k, .02), GUN, .03)
        M.add(f'tk{x}{z}', lambda p, x=x, y=y, z=z, k=sc: cyl(p, (x, y + .05 * k, z), 'y', .34 * k, .025 * k, .01), SEAM)
        M.add(f'td{x}{z}', lambda p, x=x, y=y, z=z, k=sc: ell(p, (x, y + .1 * k, z), (.27 * k, .17 * k, .23 * k)), GUN)
        M.add(f'tr{x}{z}', lambda p, x=x, y=y, z=z, k=sc: torus(p, (x, y + .05 * k, z), 'y', .31 * k, .02 * k), CY)
        M.add(f'ts{x}{z}', lambda p, x=x, y=y, z=z, k=sc: ell(p, (x + .16 * k, y + .17 * k, z), (.05 * k, .03 * k, .14 * k)), CY)  # the sight
        for dz in (-.085, .085):
            M.add(f'bl{x}{z}{dz}', lambda p, x=x, y=y, z=z, dz=dz, k=sc: cap(p, (x, y + .14 * k, z + dz * k), (x + 1.05 * k, y + .14 * k, z + dz * k), .045 * k), GUN)
            M.add(f'bm{x}{z}{dz}', lambda p, x=x, y=y, z=z, dz=dz, k=sc: cap(p, (x + .55 * k, y + .14 * k, z + dz * k), (x + .62 * k, y + .14 * k, z + dz * k), .058 * k), SEAM)  # a muzzle brake band
            M.add(f'em{x}{z}{dz}', lambda p, x=x, y=y, z=z, dz=dz, k=sc: cap(p, (x + .98 * k, y + .14 * k, z + dz * k), (x + 1.08 * k, y + .14 * k, z + dz * k), .05 * k), CY)

# ---------------------------------------------------------------- the Nebula Squid (art: dark red, a great orange eye, thick suckered arms)
def squid(M):
    SK = M_((.07, .01, .022), .26, .38); SKD = M_((.025, .004, .01), .4, .25); PALE = M_((.2, .07, .08), .35, .1); GLO = M_((.2, .03, .02), .2, .1, (1.0, .32, .1))  # v787 wine-dark, ember glow
    EYE = M_((.3, .06, .0), .1, .2, (1., .35, .05)); PUP = M_((.01, .0, .0), .1, .2); BONE = M_((.6, .52, .45), .3, .2)
    mprof = [(2.45, 0), (2.3, .25), (1.8, .52), (.9, .66), (0, .62), (-.45, .48), (-.6, .42)]
    mant = lambda p: lathe_x(p, mprof, .9, 1)
    M.add('mantle', mant, SK)
    rng = np.random.default_rng(3)
    for j in range(26):  # glowing freckles
        x = rng.uniform(-.3, 2.1); a = rng.uniform(0, 2 * np.pi); r = np.interp(x, [a_ for a_, _ in mprof][::-1], [b for _, b in mprof][::-1])
        M.add(f'fr{j}', lambda p, c=(x, np.sin(a) * r * .9, np.cos(a) * r): sphere(p, c, .045), GLO)
    for s in (1, -1):
        M.add(f'fin{s}', lambda p, s=s: oell(p, (1.85, 0, s * .6), Ry(s * .35).T, (.6, .05, .55)), SK, .05)
        M.add(f'eye{s}', lambda p, s=s: sphere(p, (-.6, .14, s * .36), .26), EYE)
        M.add(f'pup{s}', lambda p, s=s: ell(p, (-.6, .14, s * .6), (.05, .15, .04)), PUP)
        M.add(f'lid{s}', lambda p, s=s: np.maximum(np.abs(sphere(p, (-.6, .14, s * .36), .29)) - .035, -(p[..., 1] - .27)), SKD)
        M.add(f'lan{s}', lambda p, s=s: spike(p, (.6, .5, s * .28), (1.5, .5, s * .28), .07), BONE)
        M.add(f'lg{s}', lambda p, s=s: sphere(p, (1.52, .5, s * .28), .08), GLO)
        M.add(f'sac{s}', lambda p, s=s: ell(p, (.2, .52, s * .3), (.26, .13, .13)), GLO)
    M.add('head', lambda p: ell(p, (-.75, 0, 0), (.42, .38, .45)), SK, .15)
    for i in range(10):
        a = i / 10 * 2 * np.pi; long = i in (2, 7); ln = 4.6 if long else 2.6; y0, z0 = np.sin(a) * .28, np.cos(a) * .28
        pts = [(-1 - t * ln, y0 * (1 + t * 1.6) + np.sin(t * 5 + i) * .5 * t * t, z0 * (1 + t * 1.6) + np.cos(t * 4 + i * 1.3) * .5 * t * t) for t in np.linspace(0, 1, 9)]
        rads = [((.09 if long else .23) * (1 - t * .8) + (.07 * np.sin((t - .8) / .2 * np.pi) if long and t > .8 else 0)) for t in np.linspace(0, 1, 9)]
        chain(M, f'arm{i}', pts, rads, SK, .03)
        inw = np.array((0, -y0, -z0)); inw = inw / np.linalg.norm(inw)
        for j in range(1, 8):  # suckers on the inner face
            if long and j < 6: continue
            q = np.array(pts[j]); rr = rads[j]
            M.add(f'su{i}{j}', lambda p, c=tuple(q + inw * rr * .75), rr=rr: sphere(p, c, rr * .38), PALE)
            if j % 2: M.add(f'sg{i}{j}', lambda p, c=tuple(q - inw * rr * .8), rr=rr: sphere(p, c, rr * .22), GLO)
        if long: spk(M, f'st{i}', pts[-1], (-1, 0, 0), .4, .07, BONE)

# ---------------------------------------------------------------- the Void Manta (art: violet-black wings veined with purple light)
def manta(M):
    SK = M_((.025, .01, .06), .24, .4); TOP = M_((.05, .02, .1), .24, .4); GLO = M_((.15, .03, .25), .2, .1, (.95, .25, 1.0)); EDG = M_((.3, .08, .0), .2, .1, (1.0, .42, .08)); CY = M_((.05, .3, .4), .2, .1, (.3, .9, 1.0))
    body = lambda p: ell(p, (0, 0, 0), (2.1, .38, 1.1))
    def wing(p, s):
        # an arrowhead wing, thick at the root and thin at the tip, its leading edge curving forward then back to a point
        z = s * p[..., 2]; u = np.clip(z / 3.55, 0, 1); xl = 1.75 - 1.95 * u ** 1.15; xt = -1.9 + 1.7 * u ** .8   # leading / trailing edge
        th = .26 * (1 - u) ** 1.3 + .025; xm = (xl + xt) / 2; hw = np.maximum((xl - xt) / 2, .02)
        d = np.maximum(np.abs(p[..., 0] - xm) - hw, np.abs(p[..., 1] - .02 - .1 * u) - th * np.clip(1 - ((p[..., 0] - xm) / hw) ** 2, .05, 1))
        return np.maximum(d * .7, np.maximum(-z + .3, z - 3.6))
    for s in (1, -1):
        M.add(f'w{s}', lambda p, s=s: wing(p, s), SK, .25)
        for j in range(11):  # v787 thin vivid veins of light from the root out to the edge, raised on both faces
            A = (1.25 - j * .29, .55); B = (1.05 - j * .33 - .2 * (j > 6), 3.45 - abs(j - 4) * .2)
            M.add(f'v{s}{j}', lambda p, s=s, A=A, B=B: np.maximum(seg2(p[..., 0], s * p[..., 2], A, B) - .017, np.abs(wing(p, s)) - .02), GLO)
            if j % 2: M.add(f'vb{s}{j}', lambda p, s=s, A=((A[0] + B[0]) / 2, (A[1] + B[1]) / 2), B=((A[0] + B[0]) / 2 - .45, (A[1] + B[1]) / 2 + .6): np.maximum(seg2(p[..., 0], s * p[..., 2], A, B) - .012, np.abs(wing(p, s)) - .02), GLO)
        M.add(f'edge{s}', lambda p, s=s: (lambda z: np.maximum(np.maximum(np.abs(p[..., 0] - (1.75 - 1.95 * np.clip(z / 3.55, 0, 1) ** 1.15) + .04) - .05, np.abs(wing(p, s)) - .02), -z + .5))(s * p[..., 2]), EDG)
        M.add(f'lobe{s}', lambda p, s=s: oell(p, (2.15, -.02, s * .52), (Ry(s * .5) @ Rx(0)).T, (.42, .06, .18)), TOP, .05)
        M.add(f'lt{s}', lambda p, s=s: spike(p, (2.3, -.02, s * .62), (2.75, .05, s * .5), .07), TOP)
        M.add(f'eye{s}', lambda p, s=s: sphere(p, (1.82, .15, s * .62), .1), CY)
        for i in range(5): M.carve(f'gil{s}{i}', lambda p, s=s, i=i: np.maximum(np.maximum(np.abs(p[..., 0] - (.6 - i * .16)) - .025, np.abs(p[..., 1] + .3) - .12), np.abs(s * p[..., 2] - .45) - .12), CY)
    M.add('body', body, TOP, .15)
    M.carve('spine', lambda p: np.maximum(np.maximum(np.abs(p[..., 2]) - .03, -p[..., 1] + .25), np.abs(p[..., 0] - .1) - 1.6), GLO)
    tp = [(-1.9 - t * 4.8, np.sin(t * 3) * .12, 0) for t in np.linspace(0, 1, 9)]; chain(M, 'tail', tp, [.11 * (1 - t * .8) for t in np.linspace(0, 1, 9)], SK, .03)
    for j in range(1, 8): spk(M, f'ts{j}', tp[j], (-.4, 1, 0), .14 * (1 - j / 9), .03, TOP)
    M.add('sting', lambda p: spike(p, (-6.6, .02, 0), (-7.15, .02, 0), .08), GLO)

# ---------------------------------------------------------------- the Solar Moth (art: wings of burning gold veined with light, a furred body)
def moth(M):
    FUR = M_((.3, .18, .06), .8, .05, (.05, .025, .0)); FURD = M_((.12, .065, .025), .8, .05); WING = M_((.1, .04, .005), .35, .3, (.42, .14, .0)); VEIN = M_((.5, .33, .08), .25, .5, (1.0, .78, .28))
    EYE = M_((.3, .05, .0), .2, .1, (1., .45, .08)); EYC = M_((.05, .3, .35), .2, .1, (.3, 1., 1.)); DARK = M_((.06, .03, .02), .6, .1)
    rng = np.random.default_rng(5)
    for j, (x, r) in enumerate(((1.05, .2), (.75, .26), (.3, .3), (-.15, .27), (-.55, .24), (-.9, .2), (-1.2, .15), (-1.45, .1))):
        M.add(f'b{j}', lambda p, x=x, r=r: ell(p, (x, 0, 0), (r * 1.2 if j > 2 else r, r, r)), FUR if j % 2 else FURD, .08)
    for j in range(60):  # a furred surface
        x = rng.uniform(-1.4, 1.1); a = rng.uniform(0, 2 * np.pi); r = .24 - .06 * abs(x + .1)
        M.add(f'f{j}', lambda p, c=(x, np.sin(a) * r, np.cos(a) * r), d=(rng.uniform(-.3, .1), np.sin(a), np.cos(a)): spike(p, c, tuple(c[i] + d[i] * .09 for i in range(3)), .035), FUR)
    M.add('head', lambda p: sphere(p, (1.35, .03, 0), .2), FURD, .05)
    for s in (1, -1):
        M.add(f'e{s}', lambda p, s=s: sphere(p, (1.45, .07, s * .13), .1), EYC)
        pts, _ = curved(M, f'an{s}', (1.5, .15, s * .08), (1.95, .55, s * .35), (1.9, .75, s * .85), .025, .012, DARK, 6)
        for j in range(1, 6):
            for u in (1, -1): spk(M, f'af{s}{j}{u}', pts[j], norm((-.3, .3 * u, s * .2 * u + s * .1)), .14 * (1 - j / 7), .012, VEIN)
        # four wings: forewings big, hindwings rounder; thin plates with raised veins, a burning sun-eye on each
        # four wings, as in the painting: pointed forewings, rounded hindwings, thin dark-gold membranes crossed by raised burning
        # veins, a gold rim, and a sun-eye on each
        WP = ([(.55, .3), (1.3, 2.1), (1.05, 3.65), (-.3, 2.7), (-.25, .3)], [(-.15, .3), (-.3, 2.25), (-1.2, 2.55), (-1.85, 1.4), (-.95, .3)])
        for w in (0, 1):
            pts = [(x, s * z) for x, z in WP[w]] if s > 0 else [(x, s * z) for x, z in WP[w][::-1]]; y0 = .06 + .03 * w
            wf = lambda p, pts=pts, y0=y0: np.maximum(poly2(p[..., 0], p[..., 2], pts) - .1, np.abs(p[..., 1] - y0) - .025)
            M.add(f'w{s}{w}', wf, WING, .02)
            M.add(f'rim{s}{w}', lambda p, pts=pts, y0=y0: np.maximum(np.abs(poly2(p[..., 0], p[..., 2], pts) - .08) - .035, np.abs(p[..., 1] - y0) - .04), VEIN)
            root = (.15 if w == 0 else -.5, .35); tips = WP[w][1:4]
            for v in range(13):  # veins from the root out to the edge
                u = v / 12; seg = min(2, int(u * 2.999)); f = u * 3 - seg if seg < 2 else (u * 3 - 2)
                tx = tips[min(seg, 2)][0] + (tips[min(seg + 1, 2)][0] - tips[min(seg, 2)][0]) * f * (seg < 2); tz = tips[min(seg, 2)][1] + (tips[min(seg + 1, 2)][1] - tips[min(seg, 2)][1]) * f * (seg < 2)
                B = (root[0] + (tx - root[0]) * .93, root[1] + (tz - root[1]) * .93)
                M.add(f'v{s}{w}{v}', lambda p, A=root, B=B, wf=wf, s=s: np.maximum(seg2(p[..., 0], s * p[..., 2], A, B) - .02, np.abs(wf(p)) - .022), VEIN)
            ec = ((.55, 2.0) if w == 0 else (-1.0, 1.55)); r0 = .32 if w == 0 else .24
            M.add(f'se{s}{w}', lambda p, ec=ec, r0=r0, y0=y0: cyl(p, (ec[0], y0, s * ec[1]), 'y', r0, .05, .02), EYE)
            M.add(f'sr{s}{w}', lambda p, ec=ec, r0=r0, y0=y0: torus(p, (ec[0], y0, s * ec[1]), 'y', r0 * 1.12, .035), VEIN)
            M.add(f'sp{s}{w}', lambda p, ec=ec, y0=y0: sphere(p, (ec[0], y0 + .04, s * ec[1]), .09), EYC)
        for j in range(3):  # legs tucked under
            x = .6 - j * .35; pts = [(x, -.15, s * .15), (x - .1, -.35, s * .4), (x - .35, -.5, s * .45)]; chain(M, f'lg{s}{j}', pts, [.04, .03, .015], DARK)

# ---------------------------------------------------------------- the Comet Ram (art: a ram of craggy stone and bronze, spiral horns, a trail of burning debris)
def ram(M):
    ROCK = M_((.035, .05, .075), .6, .2); ROCKL = M_((.09, .13, .18), .35, .5); HORN = M_((.55, .68, .8), .2, .85); CRK = M_((.05, .25, .45), .2, .1, (.3, .8, 1.0));
    ICE = M_((.45, .7, .9), .08, .2, (.25, .6, .95)); EYE = M_((.1, .3, .4), .1, .1, (.5, .95, 1.0)); HOOF = M_((.08, .07, .07), .5, .3)
    def bodyf(p):
        b = ell(p, (.6, 0, 0), (1.55, .9, .95)); b = smin(b, ell(p, (1.9, .25, 0), (.75, .75, .7)), .4)  # shoulders
        b = smin(b, ell(p, (2.7, .35, 0), (.55, .45, .4)), .25)  # the head
        b = smin(b, ell(p, (3.05, .15, 0), (.32, .26, .26)), .15)  # the muzzle
        return b + noise3(p, 2.2, 4) * .12 - np.abs(noise3(p, 5.5, 8)) * .1
    M.add('body', bodyf, ROCK)
    rng = np.random.default_rng(9)
    for j in range(22):  # armour slabs of stone
        u = rng.uniform(-.9, 2.2); a = rng.uniform(.15, np.pi - .15); s = 1 if j % 2 else -1
        c = (u, np.sin(a) * .85 * (1 - .15 * max(0, u - 1.5)), s * np.cos(a) * .9)
        nn = norm((0, c[1], c[2])); f_ = np.array((1., 0, 0)); sd_ = np.cross(nn, f_); R_ = np.array([f_, sd_, nn], f32)
        if j % 3 == 0: M.add(f'sl{j}', lambda p, c=c, R_=R_, r0=rng.uniform(.22, .36): oell(p, c, R_, (r0 * 1.3, r0, .07)) + noise3(p, 7, j) * .03, ROCKL)
    for j in range(9): M.carve(f'ck{j}', lambda p, j=j, c=(rng.uniform(-.5, 2.2), rng.uniform(-.1, .7), rng.uniform(-1, 1)), d=norm((rng.uniform(-1, 1), rng.uniform(-.3, .3), rng.uniform(-1, 1))):
                              np.maximum(np.abs((p - V(*c)) @ np.array(d, f32)) - .02, sphere(p, c, .45)), CRK)
    for s in (1, -1):
        M.add(f'eye{s}', lambda p, s=s: sphere(p, (2.95, .5, s * .32), .07), EYE)
        # a spiral horn: from the brow back, down and round, forward to a point
        pts = []; rads = []
        for t in np.linspace(0, 1, 16):
            ang = t * 1.85 * np.pi; R = .95 * (1 - .45 * t)
            pts.append((2.55 - np.sin(ang) * R + .1, .65 + (np.cos(ang) - 1) * R * .9 + .35 * np.sin(t * np.pi), s * (.38 + .35 * t + .05 * np.sin(ang)))); rads.append(.34 * (1 - t * .85))
        chain(M, f'horn{s}', pts, rads, HORN, .02)
        for j in range(1, 15, 2): M.add(f'hr{s}{j}', lambda p, a=pts[j], r=rads[j]: sphere(p, a, r * 1.1), HORN, .03)  # ridged
        for x0, leg in ((1.75, 0), (-.35, 1)):  # legs tucked as it charges
            k_ = (x0 + (-.35 if leg else .25), -.75, s * .55); f_ = (x0 + (-1.25 if leg else 1.05), -1.2, s * .5)
            chain(M, f'lg{s}{leg}', [(x0, -.35, s * .55), k_, f_], [.24, .17, .12], ROCK, .05); M.add(f'hf{s}{leg}', lambda p, f_=f_: ell(p, f_, (.15, .1, .13)), HOOF)
    M.add('beard', lambda p: spike(p, (3.0, -.05, 0), (2.85, -.55, 0), .12), ROCK)
    # the comet tail: shards of ice and stone streaming back, bright at their cores (the wave streams it past x -2.2)
    for j in range(26):
        u = rng.uniform(0, 1); c = (-1.0 - u * 6.0, rng.uniform(-.6, .6) * (1 - u * .5), rng.uniform(-.7, .7) * (1 - u * .5)); L_ = rng.uniform(.4, 1.0) * (1 - u * .5)
        M.add(f'sh{j}', lambda p, c=c, L_=L_, r0=rng.uniform(.06, .14): spike(p, (c[0] + L_ * .3, c[1], c[2]), (c[0] - L_, c[1] * 1.1, c[2] * 1.1), r0), ICE if j % 3 else ROCKL)
    for j in range(5): M.add(f'tr{j}', lambda p, j=j: cap(p, (-.6 - j * .3, .1 * np.sin(j * 2), .15 * np.cos(j * 3)), (-3.5 - j * .8, .3 * np.sin(j * 2.1), .35 * np.cos(j * 2.7)), .12 - j * .015), ICE, .2)

SPEC = {'swhale': (shark, (-4.9, -1.5, -2.0), (4.0, 2.5, 2.0)), 'ssquid': (squid, (-6.3, -1.4, -1.6), (2.7, 1.2, 1.6)),
        'vmanta': (manta, (-7.4, -.7, -3.9), (3.0, .8, 3.9)), 'smoth': (moth, (-2.4, -.8, -3.9), (2.3, 1.1, 3.9)), 'cram': (ram, (-7.8, -1.4, -1.6), (3.5, 1.9, 1.6))}
PAINT_K = ''
def paint(P, N, A, E, idx):
    v = .5 + .5 * hashf(idx.astype(np.int64), idx.astype(np.int64) * 7 + 1, 3); glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05
    A[~glowing, :3] *= (.85 + .3 * v[~glowing])[:, None]; top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .15 * top)[:, None]
    if PAINT_K == 'swhale':  # v785 a mottled, scarred hide: low-frequency blotches from position, darker along the spine
        x, y, z = P[:, 0], P[:, 1], P[:, 2]; m = .5 + .25 * np.sin(x * 3.1 + z * 2.3) * np.sin(y * 4.7 - x * 1.3) + .25 * np.sin(x * 7.9 + y * 5.1 + z * 6.3)
        A[~glowing, :3] *= (.72 + .5 * m[~glowing])[:, None]
if __name__ == '__main__':
    k = sys.argv[1]; PAINT_K = k; f, lo, hi = SPEC[k]; M = Model(lo, hi, float(sys.argv[3]) if len(sys.argv) > 3 else .03); f(M); M.bake(sys.argv[2], paint)
