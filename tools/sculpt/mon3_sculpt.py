# The last space monsters and the Mimic hive and Nexus, sculpted after the owner's paintings (owner: "no i want all of them changed
# also"). python3 mon3_sculpt.py <key> <outdir> [voxel] writes <outdir>/<key> (the solid body) and, where the creature is partly made
# of light or glass, <outdir>/<key>_g (drawn additively and see-through in the game: the Ghost Whale's skin, the eggs' glass, wings,
# holograms). Each keeps its procedural model's frame so its wave (MON_WAVE / mimWave) still fits.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, chain, spk, blade, norm, oell
from mon_sculpt import M_, lathe_x, seg2, _fin, Rx, Ry, Rz
from mon2_sculpt import bez3, taper

def rotv(v, R): return tuple(np.array(R, f32) @ np.array(v, f32))
def crag(p, c, r, seed, amp=.25, f=1.6):
    return ell(p, c, r) + noise3((p - V(*c)) / V(*r) * 1.0, f, seed) * amp - np.abs(noise3(p, f * 3.1, seed + 1)) * amp * .4
def path_pts(pts, n):
    P = np.array(pts, float); d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; t = np.linspace(0, d[-1], n)
    return [tuple(np.interp(ti, d, P[:, k]) for k in range(3)) for ti in t]

# ---------------------------------------------------------------- the Starhive: a paper nest, its comb lit from inside, golden wasps circling
def starhive(M, G, part=None):
    PAP = [M_(c, .95, 0) for c in ((.1, .09, .075), (.14, .12, .09), (.17, .14, .1), (.08, .065, .05), (.13, .1, .07), (.15, .13, .11))]
    WALL = M_((.2, .16, .11), .9, 0); CELL = M_((.5, .25, .05), .3, 0, (1.0, .55, .12)); DARK = M_((.03, .02, .01), 1, 0)
    GOLD = M_((.55, .38, .06), .3, .5, (.12, .07, .0)); BLK = M_((.02, .02, .02), .3, .4); EYE = M_((.3, .12, .0), .1, .2, (1., .6, .15)); WING = M_((.0, .0, .0), .1, .0, (.22, .15, .05))
    # v819 the nest as in the painting: a crown of dark resin bristling with spikes, under it an upturned cone of honeycomb whose cells
    # glow from inside, tapering to a point, resin dripping from the crown (all within r 1.95: the wave swings everything beyond as swarm)
    RES = [M_(c, .55, .05) for c in ((.045, .03, .018), (.06, .04, .022), (.035, .022, .014))]; CELL2 = M_((.45, .2, .03), .35, 0, (1.0, .5, .08))
    YT, YB, R0 = .95, -2.35, 1.6
    Rf = lambda y: R0 * np.clip((y - YB) / (YT - YB), 0, 1) ** .72
    def cone(p):
        y = p[..., 1]; rr = np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2); return np.maximum((rr - Rf(y)) * .8, np.maximum(y - YT, YB - y))
    if part != 'swarm':
        M.add('comb', cone, RES[2])  # v819 dark resin walls round the lit cells
        HXS = 2 * np.pi * 1.3 / (9 * np.sqrt(3)); s3 = np.sqrt(3)
        def hexm(p):  # the hex metric of the nearest cell (0 at its centre, 1 at its wall) over the cone's surface
            u = np.arctan2(p[..., 2], p[..., 0]) * 1.3; v = p[..., 1]; q = (s3 / 3 * u - v / 3) / HXS; r = (2 / 3 * v) / HXS; x, z = q, r; y_ = -x - z
            rx, ry, rz = np.round(x), np.round(y_), np.round(z); dx, dy, dz = np.abs(rx - x), np.abs(ry - y_), np.abs(rz - z)
            fx = (dx > dy) & (dx > dz); fz = ~fx & (dz >= dy); rx = np.where(fx, -ry - rz, rx); rz = np.where(fz, -rx - ry, rz)
            cu = HXS * s3 * (rx + rz / 2); cv = HXS * 1.5 * rz; du, dv = np.abs(u - cu), np.abs(v - cv)
            return np.maximum(du, du * .5 + dv * s3 / 2) / (HXS * s3 / 2)
        M.carve('cells', lambda p: np.maximum(np.maximum((hexm(p) - .7) * 1.2, np.abs(cone(p) + .02) - .12), p[..., 1] - .8), CELL2)
        M.add('cap', lambda p: ell(p, (0, 1.12, 0), (1.82, .45, 1.82)) + noise3(p, 2.5, 31) * .12, RES[0], .15)
        M.add('cap2', lambda p: ell(p, (0, 1.42, 0), (1.25, .38, 1.25)) + noise3(p, 3.5, 32) * .1, RES[1], .2)
        rng2 = np.random.default_rng(71)
        for i in range(15):  # the crown of spikes
            a = i / 15 * 2 * np.pi + rng2.uniform(-.1, .1); rb = 1.3 + rng2.uniform(0, .25); L = .9 + rng2.uniform(0, .7)
            b_ = (np.cos(a) * rb, 1.2 + rng2.uniform(0, .2), np.sin(a) * rb); d = norm((np.cos(a) * .3, 1, np.sin(a) * .3))
            M.add(f'cs{i}', lambda p, b_=b_, d=d, L=L, r0=.16 + rng2.uniform(0, .06): spike(p, b_, tuple(np.array(b_) + np.array(d) * L), r0), RES[i % 3])
        for i in range(5): a = i / 5 * 2 * np.pi + .4; M.add(f'ct{i}', lambda p, a=a, i=i: spike(p, (np.cos(a) * .5, 1.6, np.sin(a) * .5), (np.cos(a) * .7, 2.9 - (i % 2) * .5, np.sin(a) * .7), .2), RES[1])
        for i in range(18):  # resin dripping from the crown down the comb
            a = i / 18 * 2 * np.pi + .17; rb = 1.55 - (i % 3) * .08; L = .7 + (i % 4) * .28; b_ = (np.cos(a) * rb, .85, np.sin(a) * rb)
            M.add(f'dr{i}', lambda p, b_=b_, a=a, L=L, rb=rb: spike(p, b_, (np.cos(a) * (rb - L * .45), .85 - L, np.sin(a) * (rb - L * .45)), .13), RES[i % 3])
        M.add('tip', lambda p: spike(p, (0, YB + .35, 0), (0, YB - .35, 0), .2), RES[0])
    if part == 'nest': return
    # the swarm: nine golden wasps the size of fighters, as in the painting (the wave carries everything beyond r 1.95 round the nest)
    for i in range(9):
        a = i / 9 * 2 * np.pi + (i % 2) * .3; R = 2.5 + (i % 3) * .45; h = -.9 + ((i * 5) % 9) / 9 * 2.2; sc = .95 + (i % 3) * .12
        Rw = rot('y', a + np.pi / 2).T  # three's rotation.y = -(a + pi/2)
        W = lambda v, a=a, R=R, h=h, sc=sc, Rw=Rw: tuple(np.array((np.cos(a) * R, h, np.sin(a) * R)) + np.array(Rw, float) @ (np.array(v) * sc))
        RL = (np.array(Rw, f32))
        def ellw(n, c, r, mat, tilt=0.):
            cw = W(c); Rm = (RL @ rot('z', tilt)).T
            M.add(n, lambda p, cw=cw, Rm=Rm, r=tuple(x * sc for x in r): oell(p, cw, Rm, r), mat, .02)
        for j in range(4): ellw(f'w{i}a{j}', (-.2 - j * .13, -.04 - j * .02, 0), (.12, .17 - j * .02, .17 - j * .02), GOLD if j % 2 == 0 else BLK, .25)
        M.add(f'w{i}st', lambda p, A=W((-.68, -.12, 0)), B=W((-.86, -.17, 0)): spike(p, A, B, .03 * sc), EYE)
        ellw(f'w{i}t', (.04, 0, 0), (.16, .13, .13), BLK); ellw(f'w{i}h', (.24, .02, 0), (.1, .1, .11), GOLD)
        for s in (1, -1):
            M.add(f'w{i}e{s}', lambda p, c=W((.3, .05, s * .06)): sphere(p, c, .04 * sc), EYE)
            for j in range(3):  # legs
                M.add(f'w{i}l{s}{j}', lambda p, A=W((.08 - j * .07, -.08, s * .08)), B=W((.0 - j * .12, -.25, s * .22)), C=W((-.1 - j * .12, -.36, s * .2)): np.minimum(cap(p, A, B, .012 * sc), cap(p, B, C, .01 * sc)), BLK)
            for dx, Lw in ((.04, .42), (-.08, .3)):  # wings: amber light, see-through
                c = W((dx - Lw * .3, .14, s * Lw * .55)); Rm = (RL @ rot('y', s * .5)).T
                G.add(f'w{i}g{s}{dx}', lambda p, c=c, Rm=Rm, r=(Lw * .32 * sc, .012, Lw * .55 * sc): oell(p, c, Rm, r), WING)

# ---------------------------------------------------------------- the Kraken Egg Clutch: glass eggs full of violet lightning in a thorned nest
def eggs(M, G):
    BARK = M_((.05, .035, .05), .8, .1); VEIN = M_((.2, .05, .3), .2, .1, (.7, .2, 1.0)); YOLK = M_((.4, .15, .05), .3, .1, (1.0, .55, .2)); EMB = M_((.15, .05, .2), .3, .1, (.4, .12, .6))
    GLASS = M_((.0, .0, .0), .05, .0, (.16, .06, .3)); BOLT = M_((.3, .2, .5), .1, .1, (.85, .6, 1.0)); rng = np.random.default_rng(29)
    M.add('mound', lambda p: crag(p, (0, -1.0, 0), (1.8, .55, 1.6), 3, .22), BARK)
    E = [(0, .5, -.15, 1.12, 0, 0), (1.25, .1, .55, .9, .3, -.28), (-1.2, .08, .7, .88, .34, .3), (.35, -.02, 1.3, .78, .5, -.06), (-.75, .2, -1.05, .86, -.32, .2), (1.0, .22, -.95, .8, -.3, -.24)]
    for n, (x, y, z, s, rx, rz) in enumerate(E):
        R = (rot('x', rx) @ rot('z', rz)).T; s7 = s * .72
        def egg(p, x=x, y=y, z=z, R=R, s7=s7, k=1.0):
            q = ((p - V(x, y, z)) @ R.T) / s7; yy = q[..., 1]; kx = 1 - .2 * yy - .06 * yy * yy
            sy = np.where(yy > 0, 1.5, 1.08); return (np.sqrt((q[..., 0] / kx) ** 2 + (yy / sy) ** 2 + (q[..., 2] / kx) ** 2) - k) * s7 * .8
        G.add(f'egg{n}', lambda p, egg=egg: np.abs(egg(p)) - .03, GLASS)
        w = lambda v, x=x, y=y, z=z, R=R, s=s: tuple(np.array((x, y, z)) + np.array(R, float).T @ (np.array(v) * s))
        M.add(f'yolk{n}', lambda p, c=w((0, -.36, 0)), s=s: sphere(p, c, .34 * s), YOLK)
        sp = [w((np.cos(t * 5.2) * .3 * (1 - t * .75), -.12 + t * .42, np.sin(t * 5.2) * .3 * (1 - t * .75))) for t in np.linspace(0, 1, 9)]
        chain(M, f'emb{n}', sp, [.1 * s * (1 - t * .7) for t in np.linspace(0, 1, 9)], EMB, .02)
        for b in range(4):  # lightning
            a = rng.uniform(0, 2 * np.pi); px, py, pz = np.cos(a) * .3, -.62, np.sin(a) * .3; pts = [w((px, py, pz))]
            for i in range(6): px = px * .8 + rng.uniform(-.17, .17); pz = pz * .8 + rng.uniform(-.17, .17); py += .2 + rng.uniform(0, .1); pts.append(w((px, py, pz)))
            chain(M, f'bo{n}{b}', pts, [.018 * s] * len(pts), BOLT)
    for i in range(13):  # thorned branches climbing round the eggs, violet veins beside them
        a = i / 13 * 2 * np.pi + rng.uniform(-.12, .12); R0 = 1.55 + rng.uniform(0, .4); topy = .05 + rng.uniform(0, .95); tw = rng.uniform(-.55, .55)
        pts = [(np.cos(a) * R0 * .5, -1.0, np.sin(a) * R0 * .45), (np.cos(a + tw * .2) * R0 * 1.2, -.85, np.sin(a + tw * .2) * R0 * 1.05), (np.cos(a + tw * .5) * R0 * 1.15, topy - .3, np.sin(a + tw * .5) * R0 * 1.0), (np.cos(a + tw) * R0 * .7, topy + .35, np.sin(a + tw) * R0 * .6)]
        pts = bez3(*pts, 8); th = .1 + rng.uniform(0, .06); taper(M, f'br{i}', pts, th, .015, BARK)
        for j in range(1, 7): spk(M, f'th{i}{j}', pts[j], tuple(rng.uniform(-1, 1, 3)), .18 + rng.uniform(0, .15), .035 * (1.3 - j / 8), BARK)
        if i % 2 == 0: chain(M, f'vn{i}', [(q[0] * 1.04, q[1] + .05, q[2] * 1.04) for q in pts], [.022] * len(pts), VEIN)
    for i in range(11):  # roots hanging below (they sway)
        a = rng.uniform(0, 2 * np.pi); R0 = .5 + rng.uniform(0, 1.6); ln = .9 + rng.uniform(0, 1.3); dx, dz = rng.uniform(-.4, .4, 2)
        taper(M, f'rt{i}', bez3((np.cos(a) * R0, -1.2, np.sin(a) * R0), (np.cos(a) * R0 + dx * .4, -1.2 - ln * .4, np.sin(a) * R0 + dz * .4), (np.cos(a) * R0 + dx * .8, -1.2 - ln * .8, np.sin(a) * R0 + dz * .8), (np.cos(a) * R0 + dx, -1.2 - ln, np.sin(a) * R0 + dz), 6), .08, .01, BARK)

# ---------------------------------------------------------------- the Ghost Whale: a humpback of cold light, its skeleton faint inside
def ghostwhale(M, G):
    SKIN = M_((.0, .0, .0), .2, .0, (.03, .12, .15)); WEB = M_((.0, .0, .0), .1, .0, (.2, .55, .65)); BONE = M_((.3, .45, .5), .3, .1, (.1, .3, .35)); EYE = M_((.2, .5, .55), .1, .1, (.6, 1.0, 1.0))
    ST = np.array([[4.55, .0, .02, .02, .02], [4.35, .0, .15, .2, .3], [3.9, .0, .27, .5, .58], [3.1, .04, .4, .84, .84], [2.1, .12, .6, 1.02, 1.02], [1.0, .2, .8, 1.0, 1.1], [-.1, .24, .84, .9, 1.02], [-1.3, .22, .7, .7, .8], [-2.4, .17, .5, .46, .52], [-3.4, .12, .3, .27, .28], [-4.2, .08, .17, .15, .14], [-4.7, .06, .1, .09, .1]])[::-1]
    def hull(p, k=1.0):
        x = p[..., 0]; cy = np.interp(x, ST[:, 0], ST[:, 1]); tp = np.interp(x, ST[:, 0], ST[:, 2]) * k; bl = np.interp(x, ST[:, 0], ST[:, 3]) * k; hw = np.interp(x, ST[:, 0], ST[:, 4]) * k
        dy = p[..., 1] - cy; h = np.where(dy > 0, tp, bl); d = (np.sqrt((dy / np.maximum(h, .02)) ** 2 + (p[..., 2] / np.maximum(hw, .02)) ** 2) - 1) * np.minimum(np.minimum(h, hw), .6) * .8
        return np.maximum(d, np.maximum(x - 4.6, -4.75 - x))
    G.add('skin', lambda p: np.abs(hull(p)) - .025, SKIN, .02)
    for j in range(14):  # a web of bright threads over the skin, brightest along the outline
        a = j / 14 * 2 * np.pi
        G.add(f'wl{j}', lambda p, a=a: np.maximum(np.abs(np.arctan2(p[..., 2], p[..., 1] - .1) - a + np.pi) % (2 * np.pi / 14) * .6 - .012, np.abs(hull(p)) - .04) if False else np.maximum(np.abs(np.sin(np.arctan2(p[..., 2], p[..., 1] - .15) * 7 + p[..., 0] * .6)) * .35 - .02, np.abs(hull(p)) - .04), WEB)
        break
    for j in range(9): G.add(f'pl{j}', lambda p, j=j: np.maximum(np.maximum(np.abs(p[..., 2] - (j - 4) * .16) - .015, p[..., 1] + .15), np.maximum(np.abs(hull(p)) - .04, np.maximum(p[..., 0] - 3.9, 1.6 - p[..., 0]))), WEB)  # throat pleats
    for s in (1, -1):  # long knuckled flippers swept back and down
        ly = np.array(norm((-.42, -.5, s * .76))); bx = np.array((1., 0, 0)) - ly * ly[0]; bx /= np.linalg.norm(bx); bz = np.cross(bx, ly); R = np.array([bx, ly, bz], f32)
        G.add(f'fl{s}', lambda p, R=R: _fin(p, [(.55, 0), (.75, .5), (.4, 1.6), (0, 2.9), (-.55, 3.5), (-.5, 2.0), (-.6, 0), (0, -.12)], .06, (2.0, -.45, s * .88), R.T), SKIN, .02)
        for f in range(4):
            o = (f - 1.5) * .16; chain(M, f'fb{s}{f}', [(2.0 + o * .4, -.45, s * .88), (1.62 + o, -.9, s * 1.56), (1.2 + o * 1.3, -1.4, s * 2.32), (.75 + o * 1.2, -1.95 + f * .05, s * (3.15 - f * .08))], [.02] * 4, BONE)
        lz = np.array(norm((-.12, .06, s))); bx = np.array((1., 0, 0)) - lz * lz[0]; bx /= np.linalg.norm(bx); bz = np.cross(bx, lz); R = np.array([bx, lz, bz], f32)
        G.add(f'fk{s}', lambda p, R=R: _fin(p, [(.4, 0), (.3, .7), (-.35, 1.7), (-1.0, 2.05), (-.7, 1.2), (-.7, 0), (-.2, -.1)], .05, (-4.5, .07, 0), R.T), SKIN, .02)
        M.add(f'eye{s}', lambda p, s=s: sphere(p, (3.15, -.1, s * .82), .09), EYE)
        for i in range(7): G.add(f'kn{s}{i}', lambda p, s=s, i=i: sphere(p, (4.2 - i * .28, .14 + i * .035, s * (.2 + i * .07)), .05 + (i % 3) * .012), WEB)
        chain(M, f'jb{s}', [(3.0, -.3, s * .55), (3.7, -.42, s * .5), (4.2, -.2, s * .2)], [.035] * 3, BONE)
    G.add('dorsal', lambda p: _fin(p, [(.5, 0), (.1, .32), (-.35, .42), (-.5, 0)], .05, (-1.55, .86, 0), None), SKIN)
    chain(M, 'spine', [(3.0, .1, 0), (1.6, .34, 0), (0, .42, 0), (-1.6, .34, 0), (-3.2, .16, 0), (-4.5, .07, 0)], [.075, .07, .065, .05, .035, .02], BONE)
    for i in range(13):
        x = 2.5 - i * .32; rr = .74 - abs(i - 4) * .05
        M.add(f'rb{i}', lambda p, x=x, rr=rr: np.maximum(torus(p, (x, .42 - rr * .98, 0), 'x', rr, .02), p[..., 1] - .4), BONE)
    M.add('skull', lambda p: np.abs(ell(p, (3.5, 0, 0), (.9, .3, .55))) - .02, BONE)

# ---------------------------------------------------------------- the Rock Eaters: three worms armoured in stone slabs, round toothed maws on fire
def rockeaters(M, G):
    CORE = M_((.03, .016, .01), .9, 0); SLAB = [M_(c, .85, 0) for c in ((.06, .035, .018), (.085, .05, .026), (.045, .027, .015), (.1, .062, .032))]; ROCK = M_((.035, .028, .024), .95, 0)  # v819 darker, warmer stone
    MAW = M_((.25, .07, .02), .5, 0, (.95, .38, .06)); TOOTH = M_((.6, .5, .36), .4, 0); GLOW = M_((.5, .2, .02), .2, 0, (1.0, .62, .16)); rng = np.random.default_rng(63)  # v819 a furnace in every throat
    def worm(n, pts, R):
        P = bez3(*pts[:4], 6) if len(pts) == 4 else path_pts(pts, 10)
        P = path_pts(pts, 14); pf = lambda t: R * (.9 + t * 1.7 if t < .06 else 1 - (t - .7) * 1.7 if t > .7 else 1)
        ts = np.linspace(0, 1, len(P)); chain(M, f'{n}c', P[4:], [pf(t) * .9 for t in ts[4:]], CORE, .08)  # v819 the core starts behind the throat
        for i in range(1, len(P) - 1):  # rings of stone slabs
            q = np.array(P[i]); tg = np.array(P[i + 1]) - np.array(P[i - 1]); tg /= np.linalg.norm(tg); up = np.array((0, 1., 0)) - tg * tg[1]; up /= np.linalg.norm(up); sd = np.cross(tg, up); rr = pf(ts[i])
            for j in range(9):
                a = (j + (i % 2) * .5) / 9 * 2 * np.pi; out = up * np.cos(a) + sd * np.sin(a); c = q + out * rr * .92
                Rm = np.array([tg, np.cross(out, tg), out], f32)
                M.add(f'{n}s{i}{j}', lambda p, c=tuple(c), Rm=Rm, r=(R * .36, rr * .38, R * .12): oell(p, c, Rm, r) + noise3(p, 9, i * 9 + j) * .015, SLAB[(i + j) % 4])
        q0 = np.array(P[0]); ax = q0 - np.array(P[1]); ax /= np.linalg.norm(ax); up = np.array((0, 1., 0)) - ax * ax[1]; up /= np.linalg.norm(up); sd = np.cross(ax, up)
        M.add(f'{n}lip', lambda p: torus((p - V(*q0)) @ np.array([sd, ax, up], f32).T, (0, R * .1, 0), 'y', R * .9, R * .1), CORE)
        M.add(f'{n}g', lambda p: np.maximum(np.abs(rcone(p, tuple(q0 + ax * R * .05), tuple(q0 - ax * R * 1.7), R * .9, R * .3)) - R * .06, (p - V(*q0)) @ ax.astype(f32) - R * .02), MAW)  # the open gullet, ribbed and lit
        M.add(f'{n}mw', lambda p: sphere(p, tuple(q0 - ax * R * 1.15), R * .5), GLOW)  # the furnace at its back
        for j in range(18):  # ribs running down into it, glowing, as in the painting
            a_ = j / 18 * 2 * np.pi; out = up * np.cos(a_) + sd * np.sin(a_)
            M.add(f'{n}rb{j}', lambda p, A=tuple(q0 + out * R * .8 - ax * R * .05), B=tuple(q0 - ax * R * 1.35 + out * R * .14): cap(p, A, B, R * .045), GLOW)
        for rr_, d, Lt, cnt in ((.86, .05, .5, 22), (.68, -.25, .42, 18), (.5, -.55, .34, 14)):
            for j in range(cnt):
                a = (j + rr_ * 7) / cnt * 2 * np.pi; out = up * np.cos(a) + sd * np.sin(a); b = q0 + ax * d * R + out * rr_ * R
                spk(M, f'{n}t{rr_}{j}', tuple(b), tuple(-out * .8 + ax * .45), Lt * R, R * .05, TOOTH)
    # v819 four worms apart from one another, as in the painting, mouths turned out to the viewer; no slab under them
    worm('a', [(2.0, 1.15, 1.2), (1.3, 1.2, .6), (.3, 1.1, -.1), (-.8, .8, -.6), (-1.9, .45, -.9), (-2.9, .2, -.8)], 1.1)
    worm('b', [(.6, -.25, 2.55), (-.1, -.2, 1.95), (-1.1, -.1, 1.55), (-2.1, 0., 1.4), (-3.0, -.15, 1.5)], .9)
    worm('c', [(2.55, -1.05, .25), (2.0, -1.15, -.45), (1.2, -1.2, -1.1), (.3, -1.3, -1.6), (-.6, -1.5, -1.9)], .78)
    worm('d', [(-1.1, 1.75, 1.9), (-1.6, 1.6, 1.25), (-2.3, 1.35, .7), (-3.1, 1.1, .45)], .62)
    for i in range(22):  # chewed rock drifting round them
        a = rng.uniform(0, 2 * np.pi); R0 = 2.2 + rng.uniform(0, 1.6)
        M.add(f'ch{i}', lambda p, c=(np.cos(a) * R0 - .3, -1.2 + rng.uniform(0, 2.6), np.sin(a) * R0 * .75), r0=.08 + rng.uniform(0, .2): sphere(p, c, r0) + noise3(p, 8, i) * r0 * .5, ROCK)

# ---------------------------------------------------------------- the Celestial Serpent: midnight scales rimmed with gold, violet fire beneath
def serpent(M, G):
    SC = M_((.03, .04, .1), .3, .5); GOLD = M_((.6, .42, .12), .25, .9); UND = M_((.12, .03, .25), .2, .1, (.42, .12, .9)); EYE = M_((.14, .02, .35), .1, .1, (.52, .1, 1.0))
    CRY = M_((.2, .1, .35), .05, .2, (.55, .3, .95)); HEAD = M_((.04, .05, .13), .42, .25); BLK = M_((.01, .0, .02), .2, .1); MOUTH = M_((.16, .03, .4), .35, 0, (.55, .12, 1.0)); rng = np.random.default_rng(65)  # v827 the head less metallic: it went grey head-on
    # v819 coiled as in the painting: the body rises and falls in great S-loops (the swim wave adds the side-to-side)
    pts = [(2.6, 1.75, .01), (2.1, 1.5, .03), (1.6, .7, .06), (1.0, -.35, .04), (.3, -.95, -.04), (-.4, -.8, -.06), (-1.1, .05, 0), (-1.7, .95, .06), (-2.4, 1.2, .02), (-3.1, .55, -.04), (-3.7, -.35, -.01), (-4.3, -.75, .02), (-4.95, -.55, .02)]
    from scipy.interpolate import CubicSpline
    P0 = np.array(pts); d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P0, axis=0), axis=1))]; cs = CubicSpline(d / d[-1], P0); dc = cs.derivative()
    pf = lambda t: .38 + t * 1.1 if t < .12 else .5 if t < .3 else .5 * (1 - (t - .3) / .7) ** .8 + .03  # v819 slimmer
    ts = np.linspace(0, 1, 26); chain(M, 'body', [tuple(cs(t)) for t in ts], [pf(t) for t in ts], SC, .1)
    for i in range(60):  # v819 more blades, taller
        t = .015 + i / 59 * .95; q = cs(t); tg = dc(t); tg /= np.linalg.norm(tg); up = np.array((0, 1., 0)) - tg * tg[1]; up /= np.linalg.norm(up); sd = np.cross(tg, up); rr = pf(t)
        h = (.34 + .75 * (1 - t) ** 1.3) * (.72 if i % 2 else 1)
        blade(M, f'dr{i}', tuple(q + up * rr * .85), tuple(up * .9 - tg * .6), h, .1 + h * .16, GOLD, flat=3, up=tuple(sd))
        for s in (1, -1):  # gold-rimmed scale plates down the flanks and side spines
            out = sd * s * .9 + up * .3; out /= np.linalg.norm(out); c = q + out * rr * .9; Rm = np.array([tg, np.cross(out, tg), out], f32)
            M.add(f'sc{i}{s}', lambda p, c=tuple(c), Rm=Rm, r=(rr * .38, rr * .32, .05): oell(p, c, Rm, r), SC)
            M.add(f'sr{i}{s}', lambda p, c=tuple(c - out * .02), Rm=Rm, r=(rr * .42, rr * .36, .04): oell(p, c, Rm, r), GOLD)
            if t < .92 and i % 2: spk(M, f'ss{i}{s}', tuple(q + sd * s * rr * .9), tuple(sd * s + tg * -1.5), h * .55 + .08, (h * .55 + .08) * .13, GOLD)
    for t in np.linspace(.05, .97, 30):  # violet fire under the belly
        q = cs(t); tg = dc(t); tg /= np.linalg.norm(tg); up = np.array((0, 1., 0)) - tg * tg[1]; up /= np.linalg.norm(up)
        M.add(f'ub{t:.3f}', lambda p, c=tuple(q - up * pf(t) * .85), r=pf(t) * .26: sphere(p, c, r), UND, .1)
    # v827 the head, after the painting: a viper's wedge (flat crown, angled sides, broad cheeks), a separate lower jaw under a lit mouth slit
    # (the game's swim wave opens it slowly: SERP_JAW below), gold lips with a snarl at the corner, long front fangs, brows jutting over
    # violet slit-pupilled eyes, gold-rimmed scales over the crown and snout, cheek plates, nostrils, and the horns and frill swept back
    f0t = -dc(0); f0t /= np.linalg.norm(f0t); hx = f0t + np.array((0, -.2, 0)); hx /= np.linalg.norm(hx); hz = np.cross(hx, (0, 1, 0)); hz /= np.linalg.norm(hz); hy = np.cross(hz, hx)  # v826 head held level, as in the painting (was -.42, nose-down)
    H0 = cs(0); Hs = 1.6; W = lambda v: tuple(H0 + (hx * v[0] + hy * v[1] + hz * v[2]) * Hs); RH = np.array([hx, hy, hz], f32)
    hq = lambda p: ((p - V(*H0)) @ RH.T) / Hs
    global SERP_JAW; SERP_JAW = (tuple(map(float, H0)), tuple(map(float, hx)), tuple(map(float, hy)), tuple(map(float, hz)), Hs)
    XS = [-.5, -.1, .3, .7, 1.1, 1.45, 1.7, 1.8]; WW = [.33, .46, .44, .37, .3, .23, .14, .04]; TT = [.2, .34, .36, .31, .25, .19, .12, .03]; MM = [-.17, -.15, -.12, -.1, -.08, -.06, -.045, -.03]
    Wf = lambda x: np.interp(x, XS, WW); Tf = lambda x: np.interp(x, XS, TT); Mf = lambda x: np.interp(x, XS, MM) + .045 * np.exp(-((x - .3) / .14) ** 2)  # the snarl lifts the lip at the corner
    JX = [-.5, -.1, .3, .7, 1.1, 1.4, 1.6, 1.68]; JB = [-.36, -.39, -.36, -.31, -.25, -.19, -.12, -.07]; Jt = lambda x: np.interp(x, XS, MM) - .085; Jb = lambda x: np.interp(x, JX, JB)
    def wedge(q, top, bot, w, tt, tb, x0, x1, rr=.06):  # a rounded wedge: its edges rounded by rr, so it reads carved, not boxed
        x, y, z = q[..., 0], q[..., 1], q[..., 2]; T_, B_ = top(x), bot(x); sv = np.clip((y - B_) / np.maximum(T_ - B_, 1e-3), 0, 1)
        e = [(np.abs(z) - np.maximum(w(x) * (1 - tt * sv - tb * (1 - sv)) - rr, .005)) * .8, y - T_ + rr, B_ + rr - y, x - x1 + rr, x0 + rr - x]
        return np.sqrt(sum(np.maximum(c, 0) ** 2 for c in e)) + np.minimum(np.maximum.reduce(e), 0) - rr
    M.add('skull', lambda p: wedge(hq(p), Tf, Mf, Wf, .42, .04, -.55, 1.8, .09) * Hs, HEAD, .06)
    M.add('jaw', lambda p: wedge(hq(p), Jt, Jb, lambda x: Wf(x) * .74, .02, .4, -.5, 1.68, .05) * Hs, HEAD)
    M.add('palate', lambda p: (lambda q: np.maximum.reduce([np.abs(q[..., 2]) - Wf(q[..., 0]) * .72, q[..., 1] - Mf(q[..., 0]) - .03, Mf(q[..., 0]) - .025 - q[..., 1], q[..., 0] - 1.45, -.25 - q[..., 0]]))(hq(p)) * Hs, MOUTH)
    M.add('tongue', lambda p: (lambda q: np.maximum.reduce([np.abs(q[..., 2]) - Wf(q[..., 0]) * .62, q[..., 1] - Jt(q[..., 0]) - .025, Jt(q[..., 0]) - .03 - q[..., 1], q[..., 0] - 1.35, -.25 - q[..., 0]]))(hq(p)) * Hs, MOUTH)
    lx = np.linspace(-.2, 1.72, 14)
    for s in (1, -1):  # gold lips
        chain(M, f'lu{s}', [W((x, float(Mf(x)) + .004, s * float(Wf(x)) * .97)) for x in lx], [.026 * Hs] * 13 + [.01], GOLD)
        lj = lx[lx < 1.5]; chain(M, f'lj{s}', [W((x, float(Jt(x)) - .006, s * float(Wf(x)) * .72)) for x in lj], [.022 * Hs] * (len(lj) - 1) + [.008], GOLD)
        for i in range(8):  # small teeth hanging outside the lower jaw, longer under the snarl
            x = .08 + i * .17; L = .085 + .07 * np.exp(-((x - .3) / .16) ** 2); spk(M, f'tu{s}{i}', W((x, float(Mf(x)) + .015, s * (float(Wf(x)) * .97 + .03))), tuple(-hy), L * Hs, .026 * Hs, GOLD)
        spk(M, f'fu{s}', W((1.4, float(Mf(1.4)) + .02, s * (float(Wf(1.4)) * .97 + .035))), tuple(-hy * .95 - hx * .25 + hz * s * .12), .22 * Hs, .034 * Hs, GOLD)  # the long front fangs
        for i in range(4): spk(M, f'tl{s}{i}', W((.5 + i * .24, float(Jt(.5 + i * .24)) - .01, s * float(Wf(.5 + i * .24)) * .58)), tuple(hy), .035 * Hs, .015 * Hs, GOLD)  # lower teeth, behind the lip
        # the eye: a socket under a jutting gold brow, a violet eyeball with a black slit pupil
        ex, ey = .55, .14; ez = float(Wf(ex)) * (1 - .42 * (ey - float(Mf(ex))) / (float(Tf(ex)) - float(Mf(ex)))) - .01
        M.add(f'eye{s}', lambda p, s=s, ez=ez: ell(hq(p), (ex, ey, s * ez), (.15, .09, .075)) * Hs, EYE)
        M.add(f'pup{s}', lambda p, s=s, ez=ez: ell(hq(p), (ex + .02, ey, s * (ez + .065)), (.018, .075, .02)) * Hs, BLK)
        Rb = np.array([norm(hx - hy * .3), norm(hy + hx * .3), hz * s], f32)  # the brow slopes down toward the snout
        M.add(f'brow{s}', lambda p, s=s, ez=ez, Rb=Rb: oell(p, W((.52, .255, s * (ez + .01))), Rb, (.34 * Hs, .055 * Hs, .09 * Hs)), GOLD, .02)
        for i in range(2): spk(M, f'bs{s}{i}', W((.22 - i * .16, .33 + i * .02, s * (ez - .06))), tuple(norm(-hx + hy * .35 + hz * s * .35)), (.22 - i * .05) * Hs, .04 * Hs, GOLD)
        # cheek plates: dark scales rimmed in gold, broad behind the jaw corner
        for i, (cx, cy, r0) in enumerate([(-.15, -.0, .2), (.15, -.04, .14)]):
            cz = float(Wf(cx)) * (1 - .42 * (cy - float(Mf(cx))) / (float(Tf(cx)) - float(Mf(cx)))) - .03; Rc = np.array([norm(hx), norm(hy), hz * s], f32)
            M.add(f'chr{s}{i}', lambda p, c=W((cx, cy, s * cz)), Rc=Rc, r0=r0: oell(p, c, Rc, (r0 * Hs, r0 * .62 * Hs, .045 * Hs)), GOLD)
            M.add(f'chs{s}{i}', lambda p, c=W((cx + .02, cy + .005, s * (cz + .012))), Rc=Rc, r0=r0: oell(p, c, Rc, (r0 * .84 * Hs, r0 * .5 * Hs, .045 * Hs)), HEAD)
        M.carve(f'nos{s}', lambda p, s=s: ell(hq(p), (1.6, float(Tf(1.6)) - .005, s * .055), (.035, .025, .02)) * Hs, HEAD)  # nostrils
        chain(M, f'hl{s}', [W((-.15, .3, s * .26)), W((-.6, .58, s * .4)), W((-1.15, .72, s * .5)), W((-1.7, .68, s * .46))], [.085 * Hs, .06 * Hs, .035 * Hs, .008], GOLD)
        chain(M, f'hs{s}', [W((.05, .34, s * .16)), W((-.3, .62, s * .2)), W((-.75, .86, s * .22))], [.06 * Hs, .035 * Hs, .006], GOLD)
        for i in range(5):
            a = -.7 + i * .42; Lf = .55 + (.25 if i in (2, 3) else 0); d = np.array(norm((-1, np.sin(a) * .85, s * (.38 + np.cos(a) * .25))))
            spk(M, f'fr{s}{i}', W((-.3, .05, s * .36)), tuple(hx * d[0] + hy * d[1] + hz * d[2]), Lf * Hs, .06 * Hs, GOLD)
    # the crown and snout plated in gold (the painting's armoured head), the plates parted by dark seams; a raised ridge down the middle
    M.add('cap', lambda p: (lambda q: np.maximum(wedge(q, Tf, Mf, Wf, .42, .04, -.45, 1.78, .09) - .014, Tf(q[..., 0]) - .085 - q[..., 1]))(hq(p)) * Hs, GOLD)
    band = lambda q, a, b: np.maximum(Tf(q[..., 0]) - a - q[..., 1], q[..., 1] - Tf(q[..., 0]) - b)  # only the crown's own skin, never the horns above it
    for i in range(5):
        x0 = -.2 + i * .3
        M.carve(f'seam{i}', lambda p, x0=x0: (lambda q: np.maximum(np.abs(q[..., 0] - x0 + .12 * np.abs(q[..., 2]) / .4) - .009, band(q, .1, .03)))(hq(p)) * Hs, HEAD)
    for zz in (-1, 1): M.carve(f'seamL{zz}', lambda p, zz=zz: (lambda q: np.maximum.reduce([np.abs(q[..., 2] - zz * Wf(q[..., 0]) * .3) - .009, np.abs(q[..., 0] - .6) - 1.0, band(q, .06, .03)]))(hq(p)) * Hs, HEAD)
    M.add('ridge', lambda p: (lambda q: np.maximum.reduce([np.abs(q[..., 2]) - .028, band(q, .03, .028), np.abs(q[..., 0] - .55) - .9]))(hq(p)) * Hs, GOLD, .015)
    M.add('snout', lambda p: ell(hq(p), (1.62, float(Tf(1.62)) - .03, 0), (.17, .05, .1)) * Hs, GOLD)
    M.add('chin', lambda p: ell(hq(p), (1.2, float(Jb(1.2)) + .02, 0), (.38, .04, .13)) * Hs, GOLD)
    for i in range(7):  # crystal shards drifting beside it
        c = (2.6 - rng.uniform(0, 7), -.7 + rng.uniform(0, 2.2), (1 if rng.uniform() < .5 else -1) * (1.3 + rng.uniform(0, .5))); r0 = .1 + rng.uniform(0, .14)
        M.add(f'cz{i}', lambda p, c=c, r0=r0: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) / 1.5 + np.abs(q[..., 2]) - r0)(p - V(*c)) * .55, CRY)

# ---------------------------------------------------------------- the Petrified Sentinel: a colossus of fitted stone, moss in the seams, a star-rune in its chest
def sentinel(M, G):
    ST = [M_(c, .95, 0) for c in ((.075, .075, .075), (.095, .09, .08), (.06, .06, .065), (.11, .105, .095))]; MOSS = M_((.04, .09, .02), 1, 0); RUNE = M_((.03, .25, .3), .2, 0, (.2, .9, 1.0)); EYE = M_((.03, .25, .3), .2, 0, (.35, .95, 1.0))
    Ry0 = rot('y', -.62)  # the whole figure turned .62 about y, as before (rows of Ry0 map world into its frame)
    bn = [0]
    def B(w, h, d, x, y, z, rx=0, ry=0, rz=0, par=None):
        R = rot('x', rx) @ rot('y', ry) @ rot('z', rz)
        if par is not None:
            sc = par[2] if len(par) > 2 else 1.0; c = tuple(np.array(par[0]) + sc * (np.array(par[1], float) @ np.array((x, y, z)))); R = np.array(par[1], f32) @ R; w, h, d = w * sc, h * sc, d * sc
        else: c = (x, y, z)
        k = bn[0]; bn[0] += 1; Rw = (np.array(rot('y', .62), f32) @ R).astype(f32); cw = tuple(np.array(rot('y', .62), float) @ np.array(c))
        M.add(f'b{k}', lambda p, cw=cw, Rw=Rw, h3=(w / 2, h / 2, d / 2), k=k: box(p, cw, h3, min(w, h, d) * .08, Rw) + noise3(p, 5, k) * min(w, h, d) * .05, ST[k % 4])
    def moss(x, y, z, s, par=None):
        c = (x, y, z) if par is None else tuple(np.array(par[0]) + np.array(par[1], float) @ np.array((x, y, z))); cw = tuple(np.array(rot('y', .62), float) @ np.array(c))
        M.add(f'm{bn[0]}', lambda p, cw=cw, s=s: ell(p, cw, (s * 1.2, s * .32, s * 1.2)) + noise3(p, 8, bn[0]) * s * .2, MOSS); bn[0] += 1
    M.add('base', lambda p: crag(p, tuple(np.array(rot('y', .62), float) @ np.array((0, -2.75, -.2))), (2.45, 1.05, 2.2), 11, .3, 1.4), ST[1])
    rng = np.random.default_rng(66)
    for i in range(12):  # spires of the crag
        a = np.pi * (.12 + i / 11 * 1.76) + np.pi / 2 + rng.uniform(-.1, .1); R0 = 1.75 + rng.uniform(0, .65); hh = .8 + rng.uniform(0, 1.5)
        b = tuple(np.array(rot('y', .62), float) @ np.array((np.sin(a) * R0, -2.3, np.cos(a) * R0))); M.add(f'sp{i}', lambda p, b=b, hh=hh * .6, r0=.2 + rng.uniform(0, .22): spike(p, b, (b[0], b[1] + hh, b[2]), r0), ST[i % 4])
    B(1.9, .95, 1.3, 0, -1.45, 0); B(2.15, .34, 1.5, 0, -.82, 0); B(1.7, .5, 1.2, 0, -.45, .02); B(2.35, .72, 1.42, 0, .15, 0); B(3.0, .95, 1.62, 0, .95, -.02); B(2.3, .3, 1.3, 0, 1.56, -.05)
    for s in (1, -1):
        B(1.05, 1.0, .3, s * .88, .92, .84, -.08, s * -.2, s * .06); B(.8, .6, .26, s * .72, .12, .76, .05, s * -.12, 0); B(.5, .3, .2, s * .55, -.82, .8); B(.34, 1.5, .5, s * 1.32, .5, .55, 0, 0, s * .08)
    B(.5, .34, .22, 0, 1.36, .86); B(.42, .3, .22, 0, -.3, .7); B(.9, .42, .2, 0, -.86, .8)
    rw = lambda v: tuple(np.array(rot('y', .62), float) @ np.array(v))
    M.add('ring', lambda p: torus((p - V(*rw((0, .72, .82)))) @ np.array(rot('y', .62), f32), (0, 0, 0), 'z', .46, .1), ST[0])
    # v819 the chest star as in the painting: a small bright core, four long thin rays and four short, not a solid disc
    M.add('star', lambda p: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) + np.abs(q[..., 2]) * 2 - .26)((p - V(*rw((0, .72, 1.0)))) @ np.array(rot('y', .62), f32)) * .5, RUNE)
    for i in range(8):
        a_ = i * np.pi / 4; L_ = .62 if i % 2 == 0 else .3
        M.add(f'ray{i}', lambda p, a_=a_, L_=L_: (lambda q: cap(q, (0, 0, 0), (np.cos(a_) * L_, np.sin(a_) * L_, 0), .045))((p - V(*rw((0, .72, .99)))) @ np.array(rot('y', .62), f32)), RUNE)
    HD = ((0, 1.75, 0), np.eye(3), 1.3)  # head and helm
    hB = lambda w, h, d, x, y, z, rx=0, ry=0, rz=0: B(w, h, d, x, y - 1.75, z, rx, ry, rz, HD)
    B(.95, .38, .85, 0, 1.86, -.02); hB(.98, 1.0, .95, 0, 2.5, -.05); hB(.84, .34, .3, 0, 2.08, .42, .1); hB(1.1, .2, .34, 0, 2.74, .44, .32); hB(.17, .36, .2, 0, 2.42, .5, -.1); hB(.5, .14, .12, 0, 2.2, .56)
    for s in (1, -1):
        hB(.3, .5, .2, s * .36, 2.32, .46, 0, s * -.25, s * -.1); hB(.2, 1.05, 1.0, s * .6, 2.52, -.05, 0, 0, s * -.05); hB(.26, .34, .5, s * .7, 2.98, -.05, 0, 0, s * .3)
        M.add(f'eye{s}', lambda p, c=rw(tuple(np.array((0, 1.75, 0)) + 1.3 * np.array((s * .26, 2.56 - 1.75, .48)))): ell((p - V(*c)) @ np.array(rot('y', .62), f32), (0, 0, 0), (.16, .06, .05)), EYE)
    hB(1.0, .22, 1.0, 0, 3.08, -.05)
    # v819 the stone crest arching over the head, as in the painting
    M.add('crest', lambda p: (lambda q: np.maximum(torus(q, (0, 0, 0), 'z', 1.25, .2) + noise3(p, 4, 77) * .05, -q[..., 1] + .1))((p - V(*rw((0, 2.75, -.45)))) @ np.array(rot('y', .62), f32)), ST[3])
    for i in range(7):
        a_ = .25 + i / 6 * (np.pi - .5); M.add(f'cr{i}', lambda p, a_=a_: (lambda q: box(q, (np.cos(a_) * 1.25, np.sin(a_) * 1.25, 0), (.17, .26, .27), .03, rot('z', a_ - np.pi / 2)))((p - V(*rw((0, 2.75, -.45)))) @ np.array(rot('y', .62), f32)), ST[i % 4])
    for i in range(11): a = -.35 + i / 10 * (np.pi + .7); hB(.4, .44, .34, np.cos(a) * .92, 2.78 + np.sin(a) * .78, -.12, 0, 0, a - np.pi / 2)
    for s in (1, -1):  # shoulders like fortress walls, arms, fists
        A = ((s * 2.05, 1.5, -.05), rot('z', s * -.2))
        B(1.75, .5, 1.95, 0, .12, 0, par=A); B(1.4, .4, 1.6, s * -.08, .55, 0, 0, s * .1, s * .06, A); B(.9, .34, 1.1, s * -.2, .9, 0, 0, s * -.1, 0, A); B(.26, .95, 1.75, s * .85, -.25, 0, 0, 0, s * .12, A); B(1.5, .3, .26, 0, -.2, .92, .12, 0, 0, A); B(1.5, .3, .26, 0, -.2, -.92, -.12, 0, 0, A)
        for i in range(4):
            b = tuple(np.array(A[0]) + np.array(A[1], float) @ np.array((s * (.72 - i * .08), .52 + (i % 2) * .1, -.78 + i * .52))); d = np.array(A[1], float) @ np.array((s * np.sin(.7), np.cos(.7), 0))
            bw = rw(b); dw = rw(tuple(d)); M.add(f'as{s}{i}', lambda p, bw=bw, dw=dw: spike(p, bw, tuple(np.array(bw) + np.array(dw) * .62), .15), ST[2])
        moss(s * -.1, 1.1, .1, .42, A); moss(s * .4, .42, .6, .3, A); moss(s * .2, .78, -.55, .26, A)
        B(.95, .9, 1.0, s * 2.1, .85, 0); B(.8, 1.15, .86, s * 2.2, -.05, .08, -.1, 0, s * .05); B(.92, .4, .98, s * 2.26, -.72, .2, -.2); B(1.02, 1.25, 1.05, s * 2.3, -1.4, .5, -.42, 0, s * .04); B(1.12, .3, 1.14, s * 2.3, -1.12, .4, -.42)
        B(1.12, .85, 1.1, s * 2.32, -2.2, .98, -.2, s * .1, 0)
        for i in range(4): B(.24, .4, .34, s * 2.32 + (i - 1.5) * .28, -2.36, 1.56, .25)
        B(.3, .5, .4, s * (2.32 - .62), -2.1, 1.25, 0, s * .3, 0)
    for (x, y, z, s_) in ((0, 3.75, -.1, .3), (.5, 1.74, .3, .28), (-.6, 1.74, -.3, .3), (.3, -.62, .72, .24), (.9, .6, .7, .3), (-.9, .2, .75, .28), (1.2, 1.4, .4, .3), (-1.1, 1.3, .5, .32), (.6, -1.4, .75, .3), (0, 2.95, .5, .22), (-.4, 3.5, -.4, .28), (-1.3, -1.95, 1.0, .5), (1.5, -2.0, .4, .55), (.2, -1.9, 1.5, .4), (-.4, -1.95, -1.7, .5)): moss(x, y, z, s_)
    for i in range(18):  # shards of the mountain still circling its foot (the wave turns everything beyond r 3.5)
        a = i / 18 * 2 * np.pi + rng.uniform(0, .3); R0 = 3.8 + rng.uniform(0, .4)
        M.add(f'sh{i}', lambda p, c=(np.cos(a) * R0, -3.0 + rng.uniform(0, 1.5), np.sin(a) * R0), r0=.12 + rng.uniform(0, .2), i=i: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) + np.abs(q[..., 2]) - r0)(p - V(*c)) * .58 + noise3(p, 9, i) * .02, ST[i % 4])

# ---------------------------------------------------------------- the Mimic hive and the Neural Nexus (the owner's third and fourth Mimic paintings)
def _mats(gl=(.2, .85, 1.0)):
    return dict(CAB=M_((.018, .02, .026), .18, .65), CABL=M_((.04, .05, .065), .15, .75), SHELL=M_((.03, .034, .042), .25, .7), GLOW=M_(tuple(x * .15 for x in gl), .2, .1, gl),
                HOLO=M_((.0, .0, .0), .1, .0, (.1, .4, .5)), SAC=M_((.05, .12, .18), .1, .2, (.25, .75, 1.0)), EGG=M_((.1, .03, .16), .12, .3, (.45, .12, .75)), CLAW=M_((.35, .4, .45), .15, .7))
def _spire(M, C, n, b, tip, a, R0, out=.7):
    mid = tuple(np.array(lerp(b, tip, .5)) + np.array((np.cos(a) * out, 0, np.sin(a) * out))); q = tuple(np.array(lerp(b, mid, .5)) + np.array((np.cos(a) * .2, 0, np.sin(a) * .2)))
    pts = bez3(b, q, mid, tip, 10); taper(M, n, pts, R0, .02, C['SHELL'], .02, .8)
    for j in range(3):
        off = np.array((np.cos(a + j * 2.1), 0, np.sin(a + j * 2.1))) * R0 * .7
        taper(M, f'{n}c{j}', [tuple(np.array(p) + off * (1 - i / 9)) for i, p in enumerate(pts[:8])], .06, .03, C['CAB'])
def hive(M, G):
    C = _mats(); rng = np.random.default_rng(81)
    for i in range(14):
        a = i / 14 * 2 * np.pi + rng.uniform(0, .3); R = 2.6 + rng.uniform(0, 1.3)
        taper(M, f'rt{i}', bez3((np.cos(a) * .4, -1.2, np.sin(a) * .4), (np.cos(a) * 1.4, -1.45, np.sin(a) * 1.4), (np.cos(a + .2) * R, -1.6 + rng.uniform(0, .2), np.sin(a + .2) * R), (np.cos(a + .35) * (R + 1), -1.4, np.sin(a + .35) * (R + 1)), 8), .24, .07, C['CAB'] if i % 3 else C['CABL'])
    for i in range(7):
        a = i / 7 * 2 * np.pi + .2; R = 1.5 + (i % 2) * .4; H = 3.1 + (i % 3) * .7
        _spire(M, C, f'sp{i}', (np.cos(a) * R, -1.3, np.sin(a) * R), (np.cos(a) * .55, -1.3 + H, np.sin(a) * .55), a, .36)
    M.add('orb', lambda p: sphere(p, (0, 1.15, 0), .72), C['SAC'])
    G.add('orbg', lambda p: np.abs(sphere(p, (0, 1.15, 0), 1.1)) - .02, C['HOLO'])
    for j, (rr, tx, tz) in enumerate(((1.25, 1.35, .2), (1.55, 1.45, -.3), (1.0, .4, 1.2))):
        R = (rot('x', tx) @ rot('z', tz)).astype(f32); G.add(f'hr{j}', lambda p, R=R, rr=rr: torus((p - V(0, 1.15, 0)) @ R, (0, 0, 0), 'y', rr, .025), C['HOLO'])
    G.add('plat', lambda p: np.maximum(np.abs(np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) - (1.15 - (p[..., 1] + .55) * .55)) - .02, np.abs(p[..., 1] + .55) - .45), C['HOLO'])
    for i in range(9):
        a = 2.1 + i * .5 + rng.uniform(0, .3); R = 1.9 + rng.uniform(0, .7); r0 = .3 + rng.uniform(0, .14)
        M.add(f'egg{i}', lambda p, c=(np.cos(a) * R, -1.15 + rng.uniform(0, .15), np.sin(a) * R), r0=r0: ell(p, c, (r0, r0 * 1.25, r0)), C['EGG'])
    for j in range(10):
        a = j / 10 * 2 * np.pi; taper(M, f'cb{j}', [(np.cos(a) * .3, -1.4, np.sin(a) * .3), (np.cos(a + .4) * .25, -.6, np.sin(a + .4) * .25), (np.cos(a + .8) * .12, .4, np.sin(a + .8) * .12)], .08, .04, C['CABL'] if j % 3 == 0 else C['CAB'])
def nexus(M, G):
    C = _mats(); rng = np.random.default_rng(82)
    M.add('base', lambda p: cyl(p, (0, -1.6, 0), 'y', 3.4, .25, .08), C['SHELL'])
    for j in range(24): M.carve(f'bs{j}', lambda p, a=j / 24 * 2 * np.pi: np.maximum(np.abs(-np.sin(a) * p[..., 0] + np.cos(a) * p[..., 2]) - .02, np.abs(p[..., 1] + 1.35) - .03), C['GLOW'])
    for i in range(18):
        a = i / 18 * 2 * np.pi + rng.uniform(0, .2); R = 3.4 + rng.uniform(0, 1.4)
        taper(M, f'rt{i}', bez3((np.cos(a) * 1.5, -1.42, np.sin(a) * 1.5), (np.cos(a) * 3.2, -1.5, np.sin(a) * 3.2), (np.cos(a + .25) * R, -1.75, np.sin(a + .25) * R), (np.cos(a + .4) * (R + .9), -1.6, np.sin(a + .4) * (R + .9)), 8), .2, .06, C['CAB'])
    for i in range(6):
        a = i / 6 * 2 * np.pi + .5; _spire(M, C, f'sp{i}', (np.cos(a) * 3.15, -1.4, np.sin(a) * 3.15), (np.cos(a) * 1.9, 3.7 + (i % 2) * .9, np.sin(a) * 1.9), a, .42, 1.0)
    top, bot = 2.6, 1.05
    G.add('prism', lambda p: (lambda rr, y: np.maximum(np.abs(rr - (bot + (top - bot) * np.clip(y / 2.4, 0, 1))) - .02, np.maximum(y - 2.4, -y)))(np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) * np.cos(np.pi / 6) / np.maximum(np.cos(((np.arctan2(p[..., 2], p[..., 0]) % (np.pi / 3)) - np.pi / 6)), .5), p[..., 1] - 0), C['HOLO'])
    for i in range(6):
        a = i / 6 * 2 * np.pi; a2 = a + np.pi / 3
        for A_, B_, r in (((np.cos(a) * bot, 0, np.sin(a) * bot), (np.cos(a) * top, 2.4, np.sin(a) * top), .03), ((np.cos(a) * top, 2.4, np.sin(a) * top), (np.cos(a2) * top, 2.4, np.sin(a2) * top), .03), ((np.cos(a) * bot, 0, np.sin(a) * bot), (np.cos(a2) * bot, 0, np.sin(a2) * bot), .025)):
            M.add(f'be{i}{A_[1]}{B_[1]}{r}', lambda p, A_=A_, B_=B_, r=r: cap(p, A_, B_, r), C['GLOW'])
    for j, (rr, y, tx) in enumerate(((2.9, 2.45, 0), (1.75, 1.0, .25), (3.3, 2.1, -.12), (2.2, 3.9, .4))):
        R = rot('x', tx).astype(f32); G.add(f'rg{j}', lambda p, R=R, rr=rr, y=y: torus((p - V(0, y, 0)) @ R, (0, 0, 0), 'y', rr, .025), C['HOLO'])
    M.add('orb', lambda p: sphere(p, (0, 3.95, 0), .95), C['SAC']); G.add('orbg', lambda p: np.abs(sphere(p, (0, 3.95, 0), 1.4)) - .02, C['HOLO'])
    M.add('beam', lambda p: cap(p, (0, -1.3, 0), (0, 3.2, 0), .045), C['GLOW']); G.add('beamg', lambda p: cap(p, (0, -1.3, 0), (0, 3.2, 0), .12), C['HOLO'])
    M.add('star', lambda p: sphere(p, (0, 1.35, 0), .24), C['GLOW'])
    for i in range(10):
        a = i / 10 * 2 * np.pi; d = norm((np.cos(a), .25 if i % 2 else -.2, np.sin(a))); b = tuple(np.array((0, 1.35, 0)) + np.array(d) * .12)
        spk(M, f'cl{i}', b, d, 1.15 + (i % 2) * .35, .08, C['CLAW'])
    for i in range(4):  # the four crystal anchors fleets break
        a = i / 4 * 2 * np.pi + np.pi / 4; c = (np.cos(a) * 3.05, -.75, np.sin(a) * 3.05)
        M.add(f'an{i}', lambda p, c=c: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) / 2.5 + np.abs(q[..., 2]) - .38)(p - V(*c)) * .5, M_((.05, .2, .25), .05, .2, (.3, .85, 1.0)))
        for j in range(4):
            off = rng.uniform(-.2, .2, 3); taper(M, f'ab{i}{j}', [tuple(np.array(c) + (0, -.8, 0) + off), tuple(np.array(c) + np.array((np.cos(a) * .4, -.6, np.sin(a) * .4)) + off), tuple(np.array(c) + np.array((np.cos(a) * .9, -.85, np.sin(a) * .9)) + off)], .09, .05, C['CAB'])

SPEC = {'swasp': (starhive, (-4.0, -2.8, -4.0), (4.0, 3.1, 4.0)), 'swasp_nest': (lambda M, G: starhive(M, G, 'nest'), (-2.2, -2.8, -2.2), (2.2, 3.1, 2.2)),
        'swasp_swarm': (lambda M, G: starhive(M, G, 'swarm'), (-4.0, -2.0, -4.0), (4.0, 2.0, 4.0)), 'kegg': (eggs, (-3.0, -3.5, -2.6), (3.0, 2.0, 2.9)),
        'gwhale': (ghostwhale, (-5.8, -2.6, -4.0), (4.8, 1.5, 4.0)), 'reat': (rockeaters, (-4.4, -3.0, -3.2), (3.8, 3.0, 3.6)),
        'cserp': (serpent, (-5.6, -2.4, -2.4), (5.9, 3.7, 2.4)), 'sent': (sentinel, (-4.5, -4.0, -4.5), (4.5, 4.7, 4.5)),
        'mnest': (hive, (-4.6, -2.0, -4.6), (4.6, 3.1, 4.6)), 'mnexus': (nexus, (-5.6, -2.1, -5.6), (5.6, 5.6, 5.6))}
def paint(P, N, A, E, idx):
    glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05; top = np.clip(N[:, 1], 0, 1); A[~glowing, :3] *= (1 + .3 * top[~glowing])[:, None]
if __name__ == '__main__':
    k = sys.argv[1]; f, lo, hi = SPEC[k]; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .04
    M = Model(lo, hi, vox); Gm = Model(lo, hi, vox); f(M, Gm); M.bake(sys.argv[2] + '/' + k, paint)
    if Gm.parts: Gm.bake(sys.argv[2] + '/' + k + '_g', None)
