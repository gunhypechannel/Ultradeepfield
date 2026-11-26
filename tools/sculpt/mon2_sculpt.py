# More space monsters sculpted after the owner's paintings (docs/art/mon/<k>.webp), each in its procedural model's frame so its
# swim/walk wave (MON_WAVE) still fits: python3 mon2_sculpt.py <key> <outdir> [voxel].
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, chain, spk, blade, norm, oell
from mon_sculpt import M_, lathe_x, seg2, _fin, Rx, Ry, Rz

def bez3(a, b, c, d, n=7):
    a, b, c, d = map(np.array, (a, b, c, d)); return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d) for t in np.linspace(0, 1, n)]
def taper(M, n, pts, r0, r1, mat, k=.02, pw=1.0):
    rads = [r0 + (r1 - r0) * (i / (len(pts) - 1)) ** pw for i in range(len(pts))]; chain(M, n, pts, rads, mat, k)
def scales_on(M, C, n, surf_c, surf_r, pts_uv, mat, under, size, thick=.06, ymin=-9):
    """plates laid on an ellipsoid: pts_uv [(x, z)], each a thick plate on an under-plate, its rim showing"""
    for i, (x, z) in enumerate(pts_uv):
        q = 1 - ((x - surf_c[0]) / surf_r[0]) ** 2 - ((z - surf_c[2]) / surf_r[2]) ** 2
        if q < .04: continue
        y = surf_c[1] + surf_r[1] * np.sqrt(q)
        if y < ymin: continue
        nn = np.array(norm(((x - surf_c[0]) / surf_r[0] ** 2, (y - surf_c[1]) / surf_r[1] ** 2, (z - surf_c[2]) / surf_r[2] ** 2)))
        f = np.array((1., 0, 0)) - nn * nn[0]; f /= np.linalg.norm(f) + 1e-9; sd = np.cross(nn, f); R = np.array([f, sd, nn], f32); c = np.array((x, y, z)) + nn * .02
        M.add(f'{n}u{i}', lambda p, c=tuple(c - nn * .03), R=R: oell(p, c, R, (size * 1.08, size * 1.08, thick * .8)), under)
        M.add(f'{n}p{i}', lambda p, c=tuple(c), R=R: oell(p, c, R, (size, size, thick)), mat)

# ---------------------------------------------------------------- the Crystal Tortoise (art: dark plated shell, violet crystal spires, plated legs)
def tortoise(M):
    SH = M_((.035, .035, .045), .5, .4); SHL = M_((.08, .075, .09), .45, .5); SKN = M_((.05, .048, .05), .7, .2); HORN = M_((.2, .17, .15), .4, .3)
    CRY = M_((.14, .04, .25), .05, .3, (.42, .1, .8)); CRYL = M_((.2, .1, .32), .05, .3, (.6, .3, .95)); GL = M_((.2, .05, .35), .2, .1, (.75, .3, 1.0)); EYE = M_((.3, .1, .4), .1, .1, (.9, .5, 1.0))
    rng = np.random.default_rng(18)
    SC, SR = (0, 0, 0), (2.4, 1.3, 1.75)
    M.add('shell', lambda p: np.maximum(ell(p, SC, SR), -.05 - p[..., 1]), SH, .05)
    M.add('plast', lambda p: ell(p, (0, -.05, 0), (2.3, .28, 1.68)), SKN, .05)
    # scutes: a ring of big plates on the dome, a ring of marginals at its rim, violet light in every seam
    pts = [(0, 0)] + [(np.cos(a) * 1.05, np.sin(a) * .78) for a in np.linspace(0, 2 * np.pi, 7)[:-1]] + [(np.cos(a + .26) * 1.85, np.sin(a + .26) * 1.33) for a in np.linspace(0, 2 * np.pi, 13)[:-1]]
    scales_on(M, None, 'sc', SC, SR, pts, SHL, GL, .5, .07)
    for i in range(30):
        a = i / 30 * 2 * np.pi; c = (np.cos(a) * 2.42, -.01, np.sin(a) * 1.77)
        M.add(f'mg{i}', lambda p, c=c, a=a: box(p, c, (.22, .06, .11), .02, rot('y', a) @ rot('z', -.32)), SHL)
    def prism(n, base, d, L, r0, mat):
        d = np.array(norm(d)); tip = tuple(np.array(base) + d * L); M.add(n, lambda p: rcone(p, base, tip, r0, r0 * .9), mat); spk(M, n + 't', tip, tuple(d), r0 * 2.4, r0, mat)
    for i in range(9):  # the crystal spine
        t = i / 8; x = -1.7 + t * 3.2; hgt = 1.3 * np.sqrt(max(0, 1 - (x / 2.4) ** 2)); Lc = .35 + .9 * np.sin(t * np.pi) ** 1.5
        prism(f'cs{i}', (x, hgt - .1, 0), (-x * .12, 1, 0), Lc, .1 + Lc * .07, CRY if i % 2 else CRYL)
        if i % 2 == 0 and 0 < i < 8:
            for s in (1, -1): prism(f'cl{i}{s}', (x + .1, hgt - .15, s * .26), (-x * .1, 1, s * .45), Lc * .55, .07 + Lc * .04, CRY)
    for i in range(10):  # crystal clusters on the flanks
        th = rng.uniform(0, 2 * np.pi); ph = rng.uniform(.6, 1.1); n_ = np.array((np.cos(th) * np.sin(ph) / 2.4, np.cos(ph) / 1.3, np.sin(th) * np.sin(ph) / 1.75)); n_ /= np.linalg.norm(n_)
        p0 = (2.4 * np.cos(th) * np.sin(ph), 1.3 * np.cos(ph) - .05, 1.75 * np.sin(th) * np.sin(ph))
        for j in range(3): prism(f'cc{i}{j}', tuple(np.array(p0) + rng.uniform(-.12, .12, 3)), tuple(n_ + rng.uniform(-.35, .35, 3)), rng.uniform(.2, .45), .06, CRY)
    # neck in folds, head (scaled 1.3 about (2.55, .15) like the procedural one), beak, jaw that opens on a glow, eyes, brow, horn crystals
    taper(M, 'neck', [(1.85, -.02, 0), (2.2, .06, 0), (2.48, .18, 0), (2.68, .28, 0)], .36, .27, SKN)
    for i in range(4): M.add(f'nf{i}', lambda p, i=i: torus(p, (2.0 + i * .17, .02 + i * .07, 0), 'x', .33 - i * .025, .035), SKN)
    T = lambda x, y, z=0: (2.55 + (x - 2.55) * 1.3, .15 + (y - .15) * 1.3, z * 1.3)
    M.add('skull', lambda p: ell(p, T(2.88, .33), (.37 * 1.3, .27 * 1.3, .3 * 1.3)), SKN, .06)
    M.add('beak', lambda p: spike(p, T(3.12, .3), T(3.42, .17), .2), HORN)
    M.add('jaw', lambda p: ell(p, T(3.04, -.035), (.28 * 1.3, .065 * 1.3, .21 * 1.3)), HORN, .03)
    M.add('jglow', lambda p: ell(p, T(3.0, .06), (.2 * 1.3, .03 * 1.3, .14 * 1.3)), GL)
    for s in (1, -1):
        M.add(f'eye{s}', lambda p, s=s: sphere(p, T(3.05, .42, s * .21), .1), EYE)
        M.add(f'brow{s}', lambda p, s=s: box(p, T(3.0, .5, s * .2), (.13, .03, .05), .01, rot('x', s * .3) @ rot('z', -.25)), HORN)
        prism(f'hc{s}', T(2.78, .55, s * .14), (-.6, 1, s * .4), .34, .06, CRYL)
    # four columned legs: plated thigh, a shin of scales, a broad foot with four claws
    for sx in (1, -1):
        for sz in (1, -1):
            lx, lz, fr = sx * 1.45, sz * 1.25, (1 if sx > 0 else .85)
            M.add(f'th{sx}{sz}', lambda p, c=(lx, -.32, lz), fr=fr: ell(p, c, (.42 * fr, .38, .42 * fr)), SKN, .05)
            M.add(f'sn{sx}{sz}', lambda p, c=(lx, -.68, lz), fr=fr: cyl(p, c, 'y', .31 * fr, .33, .06), SKN, .05)
            for j in range(10):
                a = j / 10 * 2 * np.pi; c = (lx + np.cos(a) * .3 * fr, -.55 - (j % 2) * .18, lz + np.sin(a) * .3 * fr)
                M.add(f'lp{sx}{sz}{j}', lambda p, c=c, a=a: oell(p, c, (rot('y', -a) @ np.eye(3, dtype=f32)).T, (.07, .13, .11)), SHL)
            M.add(f'ft{sx}{sz}', lambda p, c=(lx + sx * .05, -.98, lz), fr=fr: ell(p, c, (.42 * fr, .15, .4 * fr)), SKN, .04)
            for j in range(4):
                a = (j - 1.5) * .45 + (0 if sx > 0 else np.pi); b = (lx + np.cos(a) * .38 * fr, -1.0, lz + np.sin(a) * .32)
                spk(M, f'cw{sx}{sz}{j}', b, (np.cos(a), -.35, np.sin(a)), .22, .055, HORN)
    taper(M, 'tail', [(-2.2, -.05, 0), (-2.55, -.12, 0), (-2.85, -.22, 0)], .17, .04, SKN)
    prism('tc', (-2.85, -.22, 0), (-1, -.2, 0), .16, .035, CRY)

# ---------------------------------------------------------------- the Gravity Spider (art: black armour, magenta light, a singularity caged on its back)
def spider(M):
    AR = M_((.025, .022, .03), .25, .75); ARL = M_((.07, .06, .08), .3, .8); MG = M_((.15, .01, .1), .2, .1, (.75, .08, .55)); FANG = M_((.5, .45, .5), .15, .6)
    EYE = M_((.3, .05, .4), .1, .1, (.85, .3, 1.0)); CORE = M_((.1, .05, .2), .1, .1, (.6, .5, 1.0)); RING = M_((.2, .15, .3), .2, .6, (.4, .3, .8))
    abc, abr = (-1.7, .55, 0), (1.5, 1.12, 1.08)
    M.add('abd', lambda p: ell(p, abc, abr), AR, .05)
    for i in range(6):  # glowing bands round the abdomen, each with spines
        x = -1.7 + (i - 2.5) * .44
        M.carve(f'ab{i}', lambda p, x=x: np.maximum(np.abs(p[..., 0] - x) - .012, -ell(p, abc, abr) - .04), MG)
        f = np.sqrt(max(.05, 1 - ((x + 1.7) / 1.5) ** 2))
        for j in (-1, 0, 1):
            b = (x, .55 + 1.12 * f * np.cos(j * .5), 1.08 * f * np.sin(j * .5)); spk(M, f'as{i}{j}', b, norm((-.35, np.cos(j * .5), np.sin(j * .5))), .34, .055, FANG)
    M.add('ceph', lambda p: ell(p, (.45, .18, 0), (.95, .48, .74)), AR, .08)
    for i in range(4): M.add(f'cp{i}', lambda p, i=i: np.maximum(ell(p, (.85 - i * .3, .33, 0), (.3, .22, .5 - i * .05)), .33 - p[..., 1]), ARL, .02)
    M.add('head', lambda p: ell(p, (1.38, .22, 0), (.42, .34, .4)), AR, .06)
    M.add('ering', lambda p: torus(p, (1.72, .28, 0), 'x', .19, .045), FANG)
    M.add('eye', lambda p: ell(p, (1.7, .28, 0), (.15, .21, .21)), EYE)
    for i in range(6):
        a = i / 6 * 2 * np.pi; M.add(f'e{i}', lambda p, a=a: sphere(p, (1.66, .28 + np.sin(a) * .3, np.cos(a) * .3), .05), MG)
    for s in (1, -1):
        taper(M, f'fang{s}', [(1.62, .02, s * .14), (1.88, -.12, s * .2), (2.0, -.38, s * .16), (1.94, -.6, s * .08)], .09, .015, FANG)
        taper(M, f'palp{s}', [(1.5, .05, s * .3), (1.95, .2, s * .45), (2.25, -.05, s * .5), (2.35, -.32, s * .46)], .055, .025, AR)
    # the caged singularity on its back, three tilted rings round it (the rings turn, as the old model's did)
    M.add('core', lambda p: sphere(p, (-1.7, 1.98, 0), .38), CORE)
    for j, (rx, rz) in enumerate(((.4, 0), (-.5, .7), (1.2, -.4))):
        R = (rot('x', np.pi / 2 + rx) @ rot('y', rz)).astype(f32)
        M.add(f'rg{j}', lambda p, R=R: torus((p - V(-1.7, 1.98, 0)) @ R, (0, 0, 0), 'y', .66, .035), RING)
    for i in range(4):
        a = i / 4 * 2 * np.pi + .4
        taper(M, f'cg{i}', [(-1.7 + np.cos(a) * .7, 1.45, np.sin(a) * .6), (-1.7 + np.cos(a) * .62, 1.95, np.sin(a) * .55), (-1.7 + np.cos(a) * .2, 2.48, np.sin(a) * .15)], .06, .03, ARL)
    # eight four-jointed legs, high-kneed, magenta joints, spiked femurs
    for i in range(4):
        for s in (1, -1):
            th = .95 - i * .62; hx = .95 - i * .33; dx = np.sin(th); dz = s * np.cos(th); Lg = 1.12 if i == 0 else 1
            P0 = (hx, .12, s * .5); P1 = (hx + dx * .85 * Lg, 1.65 * Lg, s * .5 + dz * .85 * Lg); P2 = (hx + dx * 1.95 * Lg, 1.3 * Lg, s * .5 + dz * 1.95 * Lg); P3 = (hx + dx * 2.6 * Lg, .1, s * .5 + dz * 2.6 * Lg); P4 = (hx + dx * 2.95 * Lg, -1.0, s * .5 + dz * 2.95 * Lg)
            taper(M, f'l{i}{s}a', [P0, P1], .16, .13, AR); taper(M, f'l{i}{s}b', [P1, P2], .13, .1, AR); taper(M, f'l{i}{s}c', [P2, P3], .1, .075, AR); taper(M, f'l{i}{s}d', [P3, P4], .075, .015, FANG)
            for J in (P1, P2, P3): M.add(f'j{i}{s}{J[1]:.2f}', lambda p, J=J: sphere(p, J, .1), MG)
            for j in range(1, 4):
                q = lerp(P1, P2, j / 4); spk(M, f'ls{i}{s}{j}', (q[0], q[1] + .08, q[2]), norm((-.2, 1, s * .4)), .22, .04, FANG)
            for j in range(1, 3):  # armour sleeves on the femur
                q = lerp(P0, P1, j / 3); M.add(f'sv{i}{s}{j}', lambda p, q=q, P0=P0, P1=P1: rcone(p, q, lerp(q, P1, .25), .19, .12), ARL)
    for z in (-.15, .15): M.add(f'spn{z}', lambda p, z=z: spike(p, (-3.0, .45, z), (-3.4, .45, z), .09), AR)

# ---------------------------------------------------------------- the Star Leviathan (art: an armoured whale-headed sea serpent, cyan light in its seams)
def leviathan(M):
    SK = M_((.025, .05, .1), .3, .45); PL = M_((.07, .09, .13), .28, .75); PLR = M_((.18, .21, .26), .22, .9); BONE = M_((.75, .72, .65), .3, .1)
    GL = M_((.05, .3, .4), .15, .1, (.25, .9, 1.0)); MOL = M_((.4, .1, .02), .2, .1, (1.0, .45, .1)); FIN = M_((.05, .2, .3), .2, .2, (.12, .5, .65))
    S = 1.45; HXo = 2.6; T = lambda x, y, z=0: (HXo + (x - HXo) * S, y * S, z * S)
    hprof = [(4.7, 0), (4.62, .3), (4.4, .6), (4.0, .84), (3.5, .96), (3.0, .98), (2.6, .92)]
    hq = lambda p: np.stack([HXo + (p[..., 0] - HXo) / S, p[..., 1] / S, p[..., 2] / S], -1)
    M.add('head', lambda p: lathe_x(hq(p), hprof, .78, .95) * S, SK, .1)
    M.add('jaw', lambda p: lathe_x(hq(p), [(4.45, 0), (4.3, .22), (3.9, .38), (3.4, .44), (3.0, .4)], .55, .95, (0, -.42, 0)) * S, PL, .05)
    M.add('throat', lambda p: ell(p, T(3.75, -.3), (.55 * S, .06 * S, .38 * S)), MOL)
    for s in (1, -1):
        for i in range(9):
            x = 4.3 - i * .14; z = s * (.18 + i * .05)
            spk(M, f'tu{s}{i}', T(x, -.3, z), (0, -1, 0), (.2 - i * .008) * S, .04 * S, BONE); spk(M, f'tl{s}{i}', T(x - .05, -.36, z * .92), (0, 1, 0), (.16 - i * .006) * S, .035 * S, BONE)
        M.add(f'eye{s}', lambda p, s=s: sphere(p, T(3.75, .25, s * .78), .1 * S), GL)
        M.add(f'lid{s}', lambda p, s=s: box(p, T(3.8, .38, s * .74), (.21 * S, .03 * S, .07 * S), .01, rot('x', s * .35) @ rot('y', s * .2) @ rot('z', -.18)), PLR)
        for j in range(3): M.add(f'hp{s}{j}', lambda p, s=s, j=j: box(p, T(4.15 - j * .5, .5 + j * .12, s * (.36 + j * .12)), ((.3 - j * .05) * S, .035 * S, .16 * S), .015, rot('x', s * (.55 - j * .08)) @ rot('z', -.18)), PLR)
        M.add(f'pec{s}', lambda p, s=s: _fin(p, [(.35, 0), (.2, .7), (-.5, 1.35), (-.45, 0)], .06 * S, T(2.1, -.25, s * .62), Rx(s * (np.pi / 2 + .45)) @ Rz(-.3)), FIN, .03)
    for j in range(5): M.carve(f'hs{j}', lambda p, j=j: np.maximum(np.maximum(np.abs(p[..., 0] - (4.6 - j * .38)) - .025, np.abs(p[..., 2]) - .9), -(p[..., 1] - .55)), GL)
    # the body: a long eel ringed with armour plates, spikes forward, a glowing fin membrane down the tail
    pts = [(2.9 - t * 11.6, np.sin(t * 3.2) * .12, np.sin(t * 6.2) * .75 * t) for t in np.linspace(0, 1, 15)]
    rad = lambda t: .95 * (.95 + t if t < .05 else 1.0 - t * .84) + .04
    ts = np.linspace(0, 1, 15); chain(M, 'body', pts, [rad(t) for t in ts], SK, .15)
    from scipy.interpolate import CubicSpline
    cs = CubicSpline(ts, np.array(pts)); dcs = cs.derivative()
    for i in range(1, 30):
        t = i / 31; q = cs(t); tg = dcs(t); tg = tg / np.linalg.norm(tg); rr = rad(t)
        R = np.array(norm(tg), f32)
        M.add(f'rg{i}', lambda p, q=tuple(q), tg=tg, rr=rr: (lambda d, a: np.maximum(np.abs(np.sqrt(np.maximum(0, np.sum(d * d, -1) - a * a)) - rr * 1.02) - .035 - rr * .02, np.abs(a) - .07 - rr * .03))(p - V(*q), (p - V(*q)) @ tg.astype(f32)), PLR)
        if i % 2: M.carve(f'gs{i}', lambda p, q=tuple(q), tg=tg, rr=rr: (lambda d, a: np.maximum(np.abs(a - .18) - .025, np.sqrt(np.maximum(0, np.sum(d * d, -1) - a * a)) - rr * .9))(p - V(*q), (p - V(*q)) @ tg.astype(f32)), GL)
    for i in range(40):
        t = .02 + i / 40 * .9; q = cs(t); rr = rad(t)
        if t < .5: spk(M, f'sp{i}', (q[0], q[1] + rr * .9, q[2]), norm((-.5, 1, 0)), .35 + rr * .75, .05 + rr * .06, PLR)
        else: M.add(f'fn{i}', lambda p, q=tuple(q), rr=rr: _fin(p, [(.16, 0), (.05, .3), (-.2, .55), (-.3, 0)], .03, (q[0], q[1] + rr * .85, q[2]), None) * 1.0, FIN, .02)
    q = cs(1.0); M.add('tail', lambda p: _fin(p, [(.2, 0), (-1.1, .9), (-.8, .1), (-1.15, -.7), (.2, -.05)], .05, (q[0] - .05, q[1], q[2]), None), FIN, .03)

SPEC = {'ctort': (tortoise, (-3.3, -1.4, -2.2), (4.0, 2.9, 2.2)), 'gspider': (spider, (-3.6, -1.3, -3.6), (3.9, 2.8, 3.6)),
        'slevi': (leviathan, (-9.6, -1.6, -2.2), (6.2, 2.0, 2.2))}
PAINT_K = ''
def paint(P, N, A, E, idx):
    v = .5 + .5 * hashf(idx.astype(np.int64), idx.astype(np.int64) * 7 + 1, 3); glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05
    A[~glowing, :3] *= (.8 + .4 * v[~glowing])[:, None]; top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .25 * top)[:, None]
    if PAINT_K == 'slevi':  # v787 streaks of cyan light across the hide, as in the painting
        x, y, z = P[:, 0], P[:, 1], P[:, 2]; st = np.sin(x * 5.3 + z * 2.1 + np.sin(x * 1.7) * 2.) * np.sin(x * 2.3 - y * 4.1 + z * 1.3)
        m = (st > .86) & (~glowing) & (x < 2.6); E[m, 0] += .12; E[m, 1] += .6; E[m, 2] += .95
if __name__ == '__main__':
    k = sys.argv[1]; PAINT_K = k; f, lo, hi = SPEC[k]; M = Model(lo, hi, float(sys.argv[3]) if len(sys.argv) > 3 else .035); f(M); M.bake(sys.argv[2], paint)
