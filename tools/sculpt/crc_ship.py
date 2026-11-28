# One Carcinid ship: python3 crc_ship.py <key> <outdir> [voxel]. After the owner's ship paintings (docs/art/carcinid/frigate,
# interceptor, s_lance, s_war, s_brood, s_eye ...): dark gunmetal hulls of overlapping shell plates with bronze edges, great sickle
# claws at the prow, cyan light in eyes, seams and drives. The knobs match the game's CRC_SHIP (f form, L, w, h, n plates, hk, eggs, t).
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from crc_lib import *
SHIP = {
    'cfrig': dict(f='beetle', L=2.0, w=.9, h=.55, n=4), 'cint': dict(f='fork', L=1.9, w=.6, h=.4, n=3), 'cdest': dict(f='trident', L=2.6, w=.75, h=.5, n=6),
    'cvang': dict(f='manta', L=2.5, w=.8, h=.5, n=5), 'ccarr': dict(f='pod', L=2.6, w=1.0, h=.6, n=5, hk=5, eggs=5), 'cpearl': dict(f='needle', L=2.1, w=.55, h=.36, n=4, t='pearl'),
    'cmint': dict(f='twin', L=1.9, w=.6, h=.4, n=3, t='oracle'), 'cregent': dict(f='regent', L=3.2, w=1.0, h=.6, n=7), 'cempr': dict(f='crown', L=3.2, w=1.15, h=.65, n=6, t='gold'),
    'cbrlord': dict(f='hump', L=2.9, w=1.05, h=.6, n=5, hk=5, t='krak'),
}
TINT['steel'] = ((.025, .025, .035), (.085, .08, .1), (.78, .52, .24), (.05, .9, .95))

def sickle(M, n, base, d, cd, L, r, mat, teeth=0, curl=.6, tm=None):
    """a curved blade-claw: out along d, curling toward cd, tapering to a point; teeth on its inner (cd) side"""
    d = np.array(norm(d)); cd = np.array(norm(cd)); b = np.array(base)
    pts = [tuple(b + d * L * t * (1 - curl * .3 * t) + cd * L * curl * .55 * t ** 2.2) for t in np.linspace(0, 1, 8)]
    rads = [r * (1 - t) ** .8 + .012 for t in np.linspace(0, 1, 8)]
    chain(M, n, pts, rads, mat, .01)
    for j in range(1, teeth + 1):
        q = pts[1 + j * 5 // (teeth + 1)]; rr = rads[1 + j * 5 // (teeth + 1)]
        spk(M, f'{n}t{j}', tuple(np.array(q) + cd * rr * .5), tuple(norm(cd - d * .3)), rr * 1.6 + .05, rr * .45, tm or mat)
    return pts

def armour(M, C, SC, SR, rows, x0, x1, sz=1.0, sp=1.0, cols=3, ymin=-9, body=None):
    """shell plates laid like shingles over an ellipsoid hull from the back forward, each on a bronze under-plate, its rear edge a blade"""
    for i in range(rows):
        u = i / max(1, rows - 1); x = x0 + (x1 - x0) * u; ncol = cols + (i % 2)
        for j in range(ncol):
            v = (j - (ncol - 1) / 2) / ((ncol - 1) / 2 + .7) if ncol > 1 else 0; z = SC[2] + v * SR[2] * .95
            q = 1 - ((x - SC[0]) / SR[0]) ** 2 - ((z - SC[2]) / SR[2]) ** 2
            if q < .08: continue
            y = SC[1] + SR[1] * np.sqrt(q)
            if body is not None:
                lo_, hi_ = SC[1], SC[1] + SR[1] * 1.2
                for _ in range(24):
                    mid = (lo_ + hi_) / 2; d0 = float(body(np.array([[x, mid, z]], np.float32))[0])
                    lo_, hi_ = (mid, hi_) if d0 < 0 else (lo_, mid)
                y = lo_
            if y < ymin: continue
            nn = norm(((x - SC[0]) / SR[0] ** 2, (y - SC[1]) / SR[1] ** 2, (z - SC[2]) / SR[2] ** 2))
            f = np.array((1., 0, 0)) - np.array(nn) * nn[0]; f = f / np.linalg.norm(f); sd = np.cross(nn, f)
            R = np.array([f, sd, nn], np.float32); r0 = (SR[0] / rows * 1.9 * sz, SR[2] / (ncol * .55 + .4) * sz + .06, .055)
            c = np.array((x, y, z)) + np.array(nn) * .02
            M.add(f'au{x:.2f}{j}', lambda p, c=tuple(c - f * r0[0] * .2 - np.array(nn) * .025), R=R, r0=r0: oell(p, c, R, (r0[0] * 1.02, r0[1] * .96, r0[2] * .9)), C['RIM'])
            M.add(f'ap{x:.2f}{j}', lambda p, c=tuple(c), R=R, r0=r0: oell(p, c, R, r0), C['PLATE'])
            blade(M, f'ab{x:.2f}{j}', tuple(c - f * r0[0] * .55 + np.array(nn) * .04), norm(tuple(-f * .9 + np.array(nn) * .7)), .22 * sp + .08, .08, C['RIM'], flat=3, up=tuple(sd))

def hull(M, C, n, c, r, rows, cols=3, sz=1.0, sp=1.0):
    # a long shell hull drawn to a point at the prow and tapering aft, a keel beneath, a cyan seam along its waist, plates over its back
    def body(p, k=1.0):
        q = p - np.array(c, np.float32); x = q[..., 0] / r[0]; t = np.clip(1 - .55 * np.clip(x, 0, 1) ** 1.6 - .25 * np.clip(-x - .3, 0, 1), .2, 1)
        return ell(np.stack([q[..., 0], q[..., 1] / t, q[..., 2] / t], -1), (0, 0, 0), (r[0] * k, r[1] * k, r[2] * k)) * (.75 + .25 * t)
    M.add(n, lambda p: body(p), C['SHELL'], .04)
    M.add(n + 'k', lambda p: ell(p, (c[0], c[1] - r[1] * .3, c[2]), (r[0] * .85, r[1] * .6, r[2] * .9)), C['PLATE'], .06)  # the keel
    M.carve(n + 'sm', lambda p: np.maximum(np.abs(p[..., 1] - (c[1] - r[1] * .08)) - .03, np.maximum(-body(p, .93), body(p, 1.12))), C['GLOW'])
    armour(M, C, c, r, rows + 2, c[0] + r[0] * .45, c[0] - r[0] * .8, sz * .78, sp, cols + 2, body=body)

def eye(M, C, n, c, r0):
    M.add(n + 'r', lambda p: torus(p, c, 'x', r0 * 1.15, r0 * .28), C['RIM']); M.add(n, lambda p: sphere(p, (c[0] + r0 * .5, c[1], c[2]), r0 * 1.05), C['GLOW'])

def drives(M, C, x, zs, s=1.0, y=0):
    for z in zs:
        M.add(f'nac{z:.2f}', lambda p, z=z: rcone(p, (x + .55 * s, y, z), (x, y, z), .15 * s, .21 * s), C['SHELL'], .02)
        M.add(f'nr{z:.2f}', lambda p, z=z: torus(p, (x, y, z), 'x', .2 * s, .045 * s), C['RIM'])
        M.add(f'ng{z:.2f}', lambda p, z=z: ell(p, (x - .02, y, z), (.06 * s, .16 * s, .16 * s)), C['GLOW'])

def ship(M, P):
    C = mats(P.get('t', 'steel')); L, W, H, n, F = P['L'] * .92, P['w'] * 1.3, P['h'] * 1.8, P['n'], P['f']; rng = np.random.default_rng(int(sum(map(ord, P['k']))))
    eng = []
    if F == 'beetle':
        hull(M, C, 'h', (0, 0, 0), (L * .85, H * .62, W * .95), n, 3, 1.1)
        for s in (1, -1):
            sickle(M, f'cl{s}', (L * .55, H * .3, s * W * .6), (1, .25, s * .2), (.1, -1, -s * .35), L * .95, .2, C['PLATE'], 4, .75, C['TIP'])
            sickle(M, f'mn{s}', (L * .6, -H * .3, s * W * .25), (1, -.4, s * .1), (0, 1, -s * .3), L * .5, .09, C['RIM'], 2)
            for i in range(3): sickle(M, f'hk{s}{i}', (L * (.2 - .35 * i), -H * .35, s * W * .55), (.5, -1, s * .45), (1, .15, -s * .1), .6, .07, C['RIM'], 0, .65)
            eye(M, C, f'e{s}', (L * .72, H * .1, s * W * .45), .1)
        drives(M, C, -L * .92, (-W * .4, W * .4), 1.1); eng = [(-L * .95, 0, -W * .4), (-L * .95, 0, W * .4)]
    elif F == 'fork':
        hull(M, C, 'h', (0, 0, 0), (L * .9, H * .32, W * .45), n, 2, .9)
        for s in (1, -1):
            a = (L * .1, 0, s * W * .4); e2 = (L * .55, 0, s * W * 1.05); f2 = (L * 1.05, .02, s * W * .85)
            chain(M, f'arm{s}', [a, e2, f2], [.1, .09, .08], C['PLATE'], .02); M.add(f'el{s}', lambda p, e2=e2: sphere(p, e2, .11), C['GLOW'])
            M.add(f'pc{s}', lambda p, f2=f2: ell(p, f2, (.28, .2, .18)), C['PLATE'], .03)
            sickle(M, f'pu{s}', (f2[0] + .15, f2[1] + .08, f2[2]), (1, .5, -s * .15), (.1, -1, -s * .2), .8, .09, C['RIM'], 3, .65, C['TIP'])
            sickle(M, f'pd{s}', (f2[0] + .12, f2[1] - .08, f2[2]), (1, -.4, -s * .15), (0, 1, -s * .1), .65, .08, C['RIM'], 2, .55, C['TIP'])
            M.add(f'wg{s}', lambda p, s=s: oell(p, (-L * .45, 0, s * W * .9), np.array(((np.cos(.55), 0, -s * np.sin(.55)), (s * np.sin(.55), 0, np.cos(.55)), (0, 1, 0)), np.float32), (L * .35, W * .9, .06)), C['SHELL'], .03)
            eye(M, C, f'e{s}', (L * .62, H * .1, s * W * .3), .07)
        sickle(M, 'fin', (-L * .3, H * .3, 0), (-.8, 1, 0), (-1, -.3, 0), .9, .1, C['RIM'], 0, .5)
        drives(M, C, -L * .95, (-W * .3, W * .3), .9)
    elif F == 'trident':
        hull(M, C, 'h', (0, 0, 0), (L, H * .45, W * .7), n, 3)
        M.add('prow', lambda p: spike(p, (L * .85, 0, 0), (L * 1.9, 0, 0), .14), C['TIP'])
        for s in (1, -1):
            sickle(M, f'tr{s}', (L * .85, 0, s * W * .45), (1, s * .35, s * .45), (0, -s * .6, -s), L * .9, .15, C['PLATE'], 3, .5, C['TIP'])
            for i in range(4): sickle(M, f'hk{s}{i}', (L * (.3 - .3 * i), -H * .3, s * W * .5), (.5, -1, s * .45), (1, .15, -s * .1), .55, .07, C['RIM'], 0, .65)
            eye(M, C, f'e{s}', (L * .6, H * .05, s * W * .45), .09)
        for i in range(5):
            x = L * (.3 - .25 * i); z = rng.uniform(-.15, .15) * W; base = (x, H * .5, z); c = C['CORAL'] if i % 2 else C['PURP']
            for b in range(3):
                d = norm((rng.uniform(-.5, .5), 1, rng.uniform(-.5, .5))); tip = tuple(base[q] + d[q] * rng.uniform(.4, .7) for q in range(3)); M.add(f'co{i}{b}', lambda p, a=base, t=tip: cap(p, a, t, .05), c)
        drives(M, C, -L * .95, (-W * .35, W * .35))
    elif F == 'manta':
        hull(M, C, 'h', (0, 0, 0), (L * .95, H * .45, W * .7), n, 3)
        for s in (1, -1):
            M.add(f'wg{s}', lambda p, s=s: oell(p, (-L * .2, -H * .05, s * W * 1.15), np.array(((np.cos(.5), 0, -s * np.sin(.5)), (s * np.sin(.5), 0, np.cos(.5)), (0, 1, 0)), np.float32), (L * .7, W * 1.25, .1)), C['SHELL'], .05)
            M.carve(f'wgs{s}', lambda p, s=s: np.maximum(np.maximum(np.abs(p[..., 2] - s * W * 1.05) - .025, np.abs(p[..., 1] + H * .05) - .2), np.abs(p[..., 0] + L * .2) - L * .5), C['GLOW'])
            sickle(M, f'wt{s}', (L * .05, -H * .05, s * W * 2.1), (1, 0, -s * .1), (0, -.2, -s), L * .8, .14, C['PLATE'], 3, .55, C['TIP'])
            sickle(M, f'wb{s}', (-L * .75, 0, s * W * 1.6), (-1, .3, s * .4), (1, 0, 0), L * .45, .09, C['RIM'], 0, .5)
            sickle(M, f'cl{s}', (L * .85, H * .1, s * W * .4), (1, s * .3, s * .2), (0, -s * .6, -s * .5), L * .6, .12, C['PLATE'], 2, .55, C['TIP'])
        eye(M, C, 'e', (L * .55, H * .35, 0), .13); drives(M, C, -L * .95, (-W * .35, W * .35))
    elif F == 'pod':
        hull(M, C, 'h', (0, 0, 0), (L * .9, H * .6, W * 1.15), n, 4, 1.1)
        for s in (1, -1):
            for i in range(P['eggs']):
                x = L * (.4 - 1 * i / (P['eggs'] - 1))
                M.add(f'eg{s}{i}', lambda p, x=x, s=s: ell(p, (x, H * .05, s * W * 1.28), (.22, .26, .19)), C['GLOW'], .02)
                M.add(f'er{s}{i}', lambda p, x=x, s=s: np.maximum(np.abs(ell(p, (x, H * .05, s * W * 1.28), (.25, .29, .22))) - .02, np.abs(p[..., 1] - H * .05) - .04), C['RIM'])
            sickle(M, f'cl{s}', (L * .85, 0, s * W * .4), (1, s * .3, s * .2), (0, -s * .7, -s * .5), L * .5, .12, C['PLATE'], 2, .6, C['TIP'])
            for i in range(P['hk']): sickle(M, f'hk{s}{i}', (L * (.4 - i / max(1, P['hk'] - 1)), -H * .4, s * W * .7), (.5, -1, s * .45), (1, .15, -s * .1), .45, .06, C['RIM'], 0, .65)
        eye(M, C, 'e', (L * .82, H * .15, 0), .1); drives(M, C, -L * .95, (-W * .5, 0, W * .5))
    elif F == 'needle':
        hull(M, C, 'h', (0, 0, 0), (L * 1.05, H * .3, W * .4), n, 2, .9)
        for s in (1, -1): sickle(M, f'pr{s}', (L * .9, s * H * .15, s * W * .2), (1, s * .4, s * .1), (0, -s, -s * .2), L * .95, .1, C['PLATE'], 3, .5, C['TIP'])
        for i in range(3):
            a = (i - 1) * .9; sickle(M, f'tf{i}', (-L * .7, 0, 0), (-1, np.cos(a) * .8, np.sin(a) * .8), (-1, 0, 0), .7, .08, C['RIM'], 0, .3)
        eye(M, C, 'e', (L * .7, H * .2, 0), .08); drives(M, C, -L * 1.0, (-W * .25, W * .25), .8)
    elif F == 'twin':
        for s in (1, -1):
            hull(M, C, f'h{s}', (0, 0, s * W * .55), (L * .85, H * .32, W * .32), n, 2, .85)
            for u in (1, -1): sickle(M, f'cl{s}{u}', (L * .8, u * H * .15, s * W * .55), (1, u * .4, 0), (0, -u, 0), L * .7, .1, C['PLATE'], 2, .55, C['TIP'])
        M.add('br', lambda p: box(p, (0, 0, 0), (L * .25, .05, W * .55), .03), C['SHELL'])
        for i in range(4): M.add(f'gl{i}', lambda p, i=i: ell(p, (L * (.3 - .2 * i), H * .28, (1 if i % 2 else -1) * W * .55), (L * .2, .025, .025)), C['GLOW'])
        eye(M, C, 'e', (L * .25, H * .1, 0), .1); drives(M, C, -L * .9, (-W * .55, W * .55), .85)
    elif F == 'regent':
        hull(M, C, 'h', (0, 0, 0), (L, H * .5, W * .8), n, 3, 1.1, 1.2)
        for q in range(2):
            for s in (1, -1): sickle(M, f'cr{q}{s}', (L * (.8 - q * .2), H * (-.05 + q * .45), s * W * (.6 - q * .12)), (1, .15 + q * .3, s * (.25 + q * .1)), (-.1, -.8, -s * .5), L * (1.05 - q * .2), .2 - q * .04, C['PLATE'], 4, .65, C['TIP'])
        for s in (1, -1):
            sickle(M, f'af{s}', (-L * .6, H * .2, s * W * .5), (-1, .2, s * .4), (1, .2, 0), L * .55, .12, C['RIM'], 0, .55)
            for i in range(4): sickle(M, f'hk{s}{i}', (L * (.3 - .28 * i), -H * .35, s * W * .55), (.5, -1, s * .45), (1, .15, -s * .1), .7, .07, C['RIM'], 0, .65)
        M.add('eyer', lambda p: torus(p, (L * .05, H * .55, 0), 'y', .3, .06), C['RIM']); M.add('eye', lambda p: sphere(p, (L * .05, H * .55, 0), .24), C['GLOW'])
        for i in range(7): spk(M, f'sp{i}', (L * (.45 - .17 * i), H * .45, 0), norm((-.5, 1, 0)), .35 + .3 * np.sin(i / 6 * np.pi), .07, C['TIP'])
        drives(M, C, -L * .95, (-W * .4, W * .4), 1.2)
    elif F == 'crown':
        hull(M, C, 'h', (0, 0, 0), (L * .95, H * .55, W * 1.05), n, 4, 1.15, 1.2)
        for q in range(2):
            for s in (1, -1): sickle(M, f'cr{q}{s}', (L * (.8 - q * .15), H * (q * .5), s * W * (.7 - q * .15)), (1, .2 + q * .3, s * (.3 + q * .1)), (-.1, -.85, -s * .5), L * (1.1 - q * .15), .22 - q * .04, C['PLATE'], 5, .7, C['TIP'])
        for i in range(9):
            a = -np.pi * .8 + i / 8 * np.pi * 1.6; hh = (.45 if i % 2 else .8) * (1.5 if i == 4 else 1)
            spk(M, f'sp{i}', (np.cos(a) * L * .3, H * .5, np.sin(a) * W * .45), norm((np.cos(a) * .3, 1, np.sin(a) * .3)), hh, .08, C['TIP'])
        eye(M, C, 'e', (L * .05, H * .72, 0), .15)
        for i in range(5):
            for s in (1, -1): sickle(M, f'rb{i}{s}', (L * (.3 - .25 * i), 0, s * W * 1.0), (.2, -.2, s), (1, 0, 0), .6, .09, C['RIM'], 0, .5)
        drives(M, C, -L * .95, (-W * .5, 0, W * .5), 1.2)
    elif F == 'hump':
        hull(M, C, 'h', (0, 0, 0), (L * .95, H * .45, W * .9), 2, 3)
        M.add('sac', lambda p: ell(p, (-L * .15, H * .7, 0), (L * .55, H * .75, W * .75)), {'c': (.1, .02, .12), 'r': .2, 'm': .3, 'e': (.16, .03, .22)}, .1)
        for i in range(4): M.add(f'sr{i}', lambda p, i=i: np.maximum(np.abs(ell(p, (-L * .15, H * .7, 0), (L * .56, H * .77, W * .77))) - .04, np.abs(p[..., 0] + L * .15 - (i - 1.5) * L * .25) - .06), C['PLATE'])
        for i in range(5):
            x = L * (.4 - .15 * i); base = (x, H * .4, rng.uniform(-.3, .3) * W)
            for b in range(3):
                d = norm((rng.uniform(-.5, .5), 1, rng.uniform(-.5, .5))); tip = tuple(base[q] + d[q] * rng.uniform(.4, .7) for q in range(3)); M.add(f'co{i}{b}', lambda p, a=base, t=tip: cap(p, a, t, .05), C['CORAL'])
        for s in (1, -1):
            sickle(M, f'cl{s}', (L * .85, 0, s * W * .4), (1, s * .3, s * .2), (0, -s * .7, -s * .5), L * .7, .14, C['PLATE'], 3, .6, C['TIP'])
            for i in range(P['hk']): sickle(M, f'hk{s}{i}', (L * (.4 - i / max(1, P['hk'] - 1)), -H * .35, s * W * .6), (.5, -1, s * .45), (1, .15, -s * .1), .6, .07, C['RIM'], 0, .65)
        eye(M, C, 'e', (L * .85, H * .1, 0), .1); drives(M, C, -L * .95, (-W * .45, 0, W * .45))
    for s in (1, -1):  # cyan light along both flanks
        M.add(f'fl{s}', lambda p, s=s: ell(p, (-.1, -H * .1, s * W * (1.2 if F == 'pod' else .72 if F == 'manta' else .45 if F in ('fork', 'needle') else 0 if F == 'twin' else .8)), (L * .55, .025, .025)), C['GLOW'])
    return C

def kraken(M):
    """the wild Kraken: a long ribbed mantle trailing behind, fins at its tail, a ring of eyes, eight arms reaching forward"""
    C = mats('krak'); rng = np.random.default_rng(7)
    def mantle(p):
        x = p[..., 0]; u = np.clip((.2 - x) / 3.7, 0, 1); rr = np.interp(u, [0, .05, .25, .5, .75, .95, 1], [.2, .55, .8, .75, .5, .18, .02])
        return np.maximum(np.sqrt(p[..., 1] ** 2 + (p[..., 2] / .9) ** 2) - rr * .98, np.maximum(x - .05, -3.5 - x))
    M.add('man', mantle, C['PLATE'], .05)
    M.add('head', lambda p: ell(p, (.05, .02, 0), (.55, .6, .58)), C['PLATE'], .25)
    for j in range(7):  # gold-edged ribs round the mantle
        x = -.5 - .42 * j; M.add(f'rb{j}', lambda p, x=x: np.maximum(np.abs(mantle(p) + .0) - .03, np.abs(p[..., 0] - x) - .05), C['RIM'])
    for j in range(5): M.carve(f'gr{j}', lambda p, j=j: np.maximum(np.abs(p[..., 0] + .71 + .42 * j) - .035, -mantle(p) - .06), C['GLOW'])
    for s in (1, -1):
        M.add(f'fin{s}', lambda p, s=s: oell(p, (-2.6, .1, s * .45), np.array(((np.cos(.6), 0, -s * np.sin(.6)), (s * np.sin(.6), 0, np.cos(.6)), (0, 1, 0)), np.float32), (.9, .55, .05)), C['SHELL'], .03)
        M.add(f'ey{s}', lambda p, s=s: sphere(p, (.3, .32, s * .58), .13), C['GLOW']); M.add(f'eyr{s}', lambda p, s=s: torus(p, (.3, .32, s * .6), 'z', .15, .035), C['RIM'])
    for i in range(8):
        a = i / 8 * 2 * np.pi; by, bz = np.sin(a) * .42, np.cos(a) * .42; pts = [(.35, by, bz)]; px, py, pz = .35, by, bz
        for j in range(1, 7):
            px += .55 + rng.uniform(0, .15); py += np.sin(a) * .2 + np.sin(j * 1.3 + i) * .3; pz += np.cos(a) * .25 + np.cos(j * 1.1 + i) * .25; pts.append((px, py, pz))
        rads = [.2 * (1 - u * .88) for u in np.linspace(0, 1, len(pts))]; chain(M, f'arm{i}', pts, rads, C['PLATE'], .03)
        for j in range(1, 6):  # suckers of light and hooks along each arm
            q = pts[j]; M.add(f'su{i}{j}', lambda p, q=q, rr=rads[j]: sphere(p, (q[0], q[1] - np.sin(a) * rr * .8, q[2] - np.cos(a) * rr * .8), rr * .35), C['GLOW'])
            if j % 2: spk(M, f'hk{i}{j}', (q[0], q[1] + np.sin(a) * rads[j] * .7, q[2] + np.cos(a) * rads[j] * .7), norm((-.4, np.sin(a), np.cos(a))), rads[j] * 1.6, rads[j] * .4, C['TIP'])
    M.add('beak', lambda p: spike(p, (.2, 0, 0), (.75, 0, 0), .18), C['TIP'])

if __name__ == '__main__':
    # v859 every ship: a glow layer (its lit parts grown a little, baked to <path>_g) and faint light in the cracks between its plates
    from crc_boss import worley
    _bk = Model.bake
    def _bake(self, path, pt=None):
        def pt2(P, N, A, E, idx):
            pt(P, N, A, E, idx); lit = E[:, :3].sum(1) > .05; cv = worley(P, .55); g = (cv < .008) & ~lit & (N[:, 1] > -.3)
            gc = np.array(TINT.get(SHIP.get(sys.argv[1], {}).get('t', 'steel'), TINT['steel'])[3], np.float32); E[g, :3] = gc * .35; A[g, :3] *= .3
        _bk(self, path, pt2 if pt else None)
        G = Model(self.lo, self.hi, self.vox * 2)
        for (n, f, m, kk) in self.parts + self.carves:
            e = m.get('e')
            if e and sum(e) > .5: G.add(n, lambda p, f=f: f(p) - .05, {'c': (0, 0, 0), 'r': .2, 'm': 0, 'e': tuple(x * .14 for x in e)})
        if G.parts: _bk(G, path + '_g', None)
    Model.bake = _bake
    if sys.argv[1] == 'ckrak':
        M = Model((-3.8, -2.6, -2.8), (4.8, 2.6, 2.8), float(sys.argv[3]) if len(sys.argv) > 3 else .035); kraken(M); M.bake(sys.argv[2], paint); sys.exit()
    k = sys.argv[1]; P = dict(SHIP[k]); P['k'] = k; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .035
    L, W, H = P['L'] * .92, P['w'] * 1.3, P['h'] * 1.8
    M = Model((-L * 1.25, -H - .8, -W * 2.3 - 1.4), (L * 2.0 + 1.4, H * 1.6 + 1.2, W * 2.3 + 1.4), vox)
    ship(M, P); M.bake(sys.argv[2], paint)
