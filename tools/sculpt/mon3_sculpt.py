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
    NP = [(1.75, 0), (1.6, .55), (1.15, 1.1), (.45, 1.42), (-.3, 1.45), (-.95, 1.2), (-1.45, .78), (-1.7, .3), (-1.78, 0)]
    ys = np.array([a for a, _ in NP][::-1]); rs = np.array([b for _, b in NP][::-1])
    nr = lambda y: np.interp(y, ys, rs)
    top, bot, Lb = 1.7, -1.5, 10
    for i in range(Lb if part != 'swarm' else 0):  # overlapping envelopes, each flaring at its scalloped lower edge
        y0 = top - (top - bot) * i / Lb + .08; y1 = y0 - (top - bot) / Lb * 1.75
        def env(p, y0=y0, y1=y1, i=i):
            y = p[..., 1]; u = np.clip((y0 - y) / (y0 - y1), 0, 1); th = np.arctan2(p[..., 2], p[..., 0])
            R = nr(np.clip(y, bot, top)) * (1 + .045 * i / Lb) + .03 + u ** 2.2 * .16 + .05 * np.sin(th * 2 + i * 1.7) * .5
            sc = .1 * np.maximum(0, np.sin(th * (5 + i % 3) + i)) ** 2
            rr = np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2)
            return np.maximum(np.maximum(np.abs(rr - R) - .035, y - y0), y1 + sc - y)
        M.add(f'env{i}', env, PAP[i % 6])
    if part == 'swarm': M.parts.clear()
    if part != 'swarm': M.add('core', lambda p: np.maximum(np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) - nr(np.clip(p[..., 1], bot, top)) * .96, np.maximum(p[..., 1] - top, bot - p[..., 1])), WALL)
    cr = .17  # the comb under the open mouth: hexagonal cells glowing from inside
    for q in (range(-4, 5) if part != 'swarm' else []):
        for s_ in range(-4, 5):
            x = cr * 1.74 * (q + s_ / 2); z = cr * 1.5 * s_
            if np.hypot(x, z) < nr(bot) * .92 + .25:
                M.add(f'cw{q}{s_}', lambda p, c=(x, bot - .02, z): np.maximum(np.abs(cyl(p, c, 'y', cr, .13)) - .02, -(p[..., 1] - (c[1] - .13))), WALL)
                M.add(f'cc{q}{s_}', lambda p, c=(x, bot - .1, z): cyl(p, c, 'y', cr * .85, .02), CELL)
    for i in range(6 if part != 'swarm' else 0):  # cells breaking through the envelope low on its sides
        a = i * 2.39 + .4; y = -1.1 + (i % 3) * .28; rr = nr(y) * 1.08; M.add(f'bc{i}', lambda p, c=(np.cos(a) * rr, y, np.sin(a) * rr): sphere(p, c, .13), CELL)
    pts = [(0, 1.55 + t * 1.2, 0) for t in np.linspace(0, 1, 6)]  # the twisted paper stalk
    if part != 'swarm': M.add('stalk', lambda p: np.maximum(np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) - (.34 - (p[..., 1] - 1.5) * .17) * (1 + .12 * np.sin(np.arctan2(p[..., 2], p[..., 0]) * 5 + p[..., 1] * 6)), np.maximum(p[..., 1] - 2.85, 1.4 - p[..., 1])), PAP[3])
    if part != 'swarm': M.add('throat', lambda p: cyl(p, (0, bot + .02, 0), 'y', nr(bot) * .7, .02), DARK)
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
    CORE = M_((.04, .025, .02), .9, 0); SLAB = [M_(c, .9, 0) for c in ((.09, .075, .06), (.12, .1, .075), (.07, .055, .045), (.14, .115, .09))]; ROCK = M_((.06, .05, .045), .95, 0)
    MAW = M_((.25, .05, .02), .5, 0, (.55, .12, .02)); TOOTH = M_((.75, .68, .55), .4, 0); GLOW = M_((.5, .2, .02), .2, 0, (1.0, .55, .12)); rng = np.random.default_rng(63)
    def worm(n, pts, R):
        P = bez3(*pts[:4], 6) if len(pts) == 4 else path_pts(pts, 10)
        P = path_pts(pts, 14); pf = lambda t: R * (.9 + t * 1.7 if t < .06 else 1 - (t - .7) * 1.7 if t > .7 else 1)
        ts = np.linspace(0, 1, len(P)); chain(M, f'{n}c', P[2:], [pf(t) * .9 for t in ts[2:]], CORE, .08)
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
        for rr_, d, Lt, cnt in ((.86, .05, .5, 22), (.68, -.25, .42, 18), (.5, -.55, .34, 14)):
            for j in range(cnt):
                a = (j + rr_ * 7) / cnt * 2 * np.pi; out = up * np.cos(a) + sd * np.sin(a); b = q0 + ax * d * R + out * rr_ * R
                spk(M, f'{n}t{rr_}{j}', tuple(b), tuple(-out * .8 + ax * .45), Lt * R, R * .05, TOOTH)
    worm('a', [(1.9, .95, 1.0), (1.2, 1.0, .5), (.2, .9, -.1), (-.9, .55, -.5), (-2.0, .1, -.6), (-2.9, -.3, -.3)], .98)
    worm('b', [(.1, -.35, 2.3), (-.5, -.3, 1.7), (-1.4, -.2, 1.2), (-2.3, -.1, .9), (-3.1, -.3, .9)], .74)
    worm('c', [(2.5, -.75, .7), (2.0, -.85, .1), (1.3, -.9, -.6), (.5, -1.0, -1.2), (-.3, -1.3, -1.6)], .58)
    M.add('ast', lambda p: crag(p, (-.6, -1.8, -.1), (3.3, 1.0, 2.4), 7, .3, 1.3), ROCK)
    for i in range(16):
        a = rng.uniform(0, 2 * np.pi); R0 = 2.2 + rng.uniform(0, 1.6)
        M.add(f'ch{i}', lambda p, c=(np.cos(a) * R0 - .3, -1.2 + rng.uniform(0, 2.6), np.sin(a) * R0 * .75), r0=.08 + rng.uniform(0, .2): sphere(p, c, r0) + noise3(p, 8, i) * r0 * .5, ROCK)

# ---------------------------------------------------------------- the Celestial Serpent: midnight scales rimmed with gold, violet fire beneath
def serpent(M, G):
    SC = M_((.03, .04, .1), .3, .5); GOLD = M_((.6, .42, .12), .25, .9); UND = M_((.2, .05, .35), .2, .1, (.65, .2, 1.0)); EYE = M_((.3, .1, .5), .1, .1, (.85, .4, 1.0))
    CRY = M_((.2, .1, .35), .05, .2, (.55, .3, .95)); HEAD = M_((.04, .05, .12), .3, .55); rng = np.random.default_rng(65)
    pts = [(2.6, 1.55, .01), (2.1, 1.35, .03), (1.5, .62, .06), (.7, -.05, .04), (0, -.12, -.04), (-.8, .12, -.06), (-1.6, .2, 0), (-2.2, .02, .06), (-2.9, -.1, .02), (-3.5, .04, -.04), (-4.1, .06, -.01), (-4.6, 0, .02), (-4.95, -.02, .02)]
    from scipy.interpolate import CubicSpline
    P0 = np.array(pts); d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P0, axis=0), axis=1))]; cs = CubicSpline(d / d[-1], P0); dc = cs.derivative()
    pf = lambda t: .42 + t * 1.3 if t < .12 else .58 if t < .3 else .58 * (1 - (t - .3) / .7) ** .8 + .03
    ts = np.linspace(0, 1, 26); chain(M, 'body', [tuple(cs(t)) for t in ts], [pf(t) for t in ts], SC, .1)
    for i in range(44):
        t = .015 + i / 43 * .95; q = cs(t); tg = dc(t); tg /= np.linalg.norm(tg); up = np.array((0, 1., 0)) - tg * tg[1]; up /= np.linalg.norm(up); sd = np.cross(tg, up); rr = pf(t)
        h = (.24 + .62 * (1 - t) ** 1.5) * (.78 if i % 2 else 1)
        blade(M, f'dr{i}', tuple(q + up * rr * .85), tuple(up * .9 - tg * .6), h, .07 + h * .1, GOLD, flat=3, up=tuple(sd))
        for s in (1, -1):  # gold-rimmed scale plates down the flanks and side spines
            out = sd * s * .9 + up * .3; out /= np.linalg.norm(out); c = q + out * rr * .9; Rm = np.array([tg, np.cross(out, tg), out], f32)
            M.add(f'sc{i}{s}', lambda p, c=tuple(c), Rm=Rm, r=(rr * .38, rr * .32, .05): oell(p, c, Rm, r), SC)
            M.add(f'sr{i}{s}', lambda p, c=tuple(c - out * .02), Rm=Rm, r=(rr * .42, rr * .36, .04): oell(p, c, Rm, r), GOLD)
            if t < .92 and i % 2: spk(M, f'ss{i}{s}', tuple(q + sd * s * rr * .9), tuple(sd * s + tg * -1.5), h * .55 + .08, (h * .55 + .08) * .13, GOLD)
    for t in np.linspace(.05, .97, 30):  # violet fire under the belly
        q = cs(t); tg = dc(t); tg /= np.linalg.norm(tg); up = np.array((0, 1., 0)) - tg * tg[1]; up /= np.linalg.norm(up)
        M.add(f'ub{t:.3f}', lambda p, c=tuple(q - up * pf(t) * .85), r=pf(t) * .34: sphere(p, c, r), UND, .1)
    # the head: a wedge skull, brow ridges, open jaw of gold teeth over violet glow, two long horns and two short, a spiked frill
    f0t = -dc(0); f0t /= np.linalg.norm(f0t); hx = f0t + np.array((0, -.42, 0)); hx /= np.linalg.norm(hx); hz = np.cross(hx, (0, 1, 0)); hz /= np.linalg.norm(hz); hy = np.cross(hz, hx)
    H0 = cs(0); Hs = 1.35; W = lambda v: tuple(H0 + (hx * v[0] + hy * v[1] + hz * v[2]) * Hs); RH = np.array([hx, hy, hz], f32)
    hq = lambda p: ((p - V(*H0)) @ RH.T) / Hs
    sk = [(-.42, .3), (-.1, .38), (.35, .4), (.75, .27), (1.15, .18), (1.5, .13), (1.7, .08), (1.78, .02)]
    M.add('skull', lambda p: lathe_x(hq(p), sk, .85, 1.05, (0, .04, 0)) * Hs, HEAD, .05)
    jq = lambda p: (lambda q: np.stack([q[..., 0] * np.cos(.3) - (q[..., 1] + .16) * np.sin(.3), q[..., 0] * np.sin(.3) + (q[..., 1] + .16) * np.cos(.3), q[..., 2]], -1))(hq(p))
    M.add('jaw', lambda p: lathe_x(jq(p), [(-.2, .25), (.4, .22), (.95, .15), (1.4, .1), (1.62, .02)], .45, 1.2) * Hs, HEAD, .03)
    M.add('mglow', lambda p: ell(hq(p), (.8, -.2, 0), (.6, .1, .2)) * Hs, UND)
    for s in (1, -1):
        M.add(f'eye{s}', lambda p, s=s: ell(hq(p), (.52, .2, s * .37), (.11, .06, .05)) * Hs, EYE)
        M.add(f'brow{s}', lambda p, s=s: ell(hq(p), (.5, .32, s * .34), (.45, .06, .08)) * Hs, GOLD)
        chain(M, f'hl{s}', [W((-.1, .3, s * .24)), W((-.6, .58, s * .4)), W((-1.15, .72, s * .5)), W((-1.7, .68, s * .46))], [.085 * Hs, .06 * Hs, .035 * Hs, .008], GOLD)
        chain(M, f'hs{s}', [W((.1, .36, s * .16)), W((-.3, .62, s * .2)), W((-.75, .86, s * .22))], [.06 * Hs, .035 * Hs, .006], GOLD)
        for i in range(5):
            a = -.7 + i * .42; Lf = .55 + (.25 if i in (2, 3) else 0); d = np.array(norm((-1, np.sin(a) * .85, s * (.38 + np.cos(a) * .25))))
            spk(M, f'fr{s}{i}', W((-.28, .1, s * .3)), tuple(hx * d[0] + hy * d[1] + hz * d[2]), Lf * Hs, .06 * Hs, GOLD)
        for i in range(9): spk(M, f'tt{s}{i}', W((.34 + i * .15, -.11 - i * .006, s * (.3 - i * .028))), tuple(-hy), (.12 - i * .005) * Hs, .022 * Hs, GOLD)
    for i in range(7):  # crystal shards drifting beside it
        c = (2.6 - rng.uniform(0, 7), -.7 + rng.uniform(0, 2.2), (1 if rng.uniform() < .5 else -1) * (1.3 + rng.uniform(0, .5))); r0 = .1 + rng.uniform(0, .14)
        M.add(f'cz{i}', lambda p, c=c, r0=r0: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) / 1.5 + np.abs(q[..., 2]) - r0)(p - V(*c)) * .55, CRY)

# ---------------------------------------------------------------- the Petrified Sentinel: a colossus of fitted stone, moss in the seams, a star-rune in its chest
def sentinel(M, G):
    ST = [M_(c, .95, 0) for c in ((.075, .075, .075), (.095, .09, .08), (.06, .06, .065), (.11, .105, .095))]; MOSS = M_((.04, .09, .02), 1, 0); RUNE = M_((.05, .35, .2), .2, 0, (.3, 1.0, .6)); EYE = M_((.05, .3, .2), .2, 0, (.4, 1.0, .7))
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
    M.add('rune', lambda p: (lambda q: np.maximum(np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - .5, np.abs(q[..., 2]) - .05))((p - V(*rw((0, .72, .9)))) @ np.array(rot('y', .62), f32)), RUNE)
    M.add('star', lambda p: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) + np.abs(q[..., 2]) * 2 - .3)((p - V(*rw((0, .72, 1.0)))) @ np.array(rot('y', .62), f32)) * .5, RUNE)
    HD = ((0, 1.75, 0), np.eye(3), 1.3)  # head and helm
    hB = lambda w, h, d, x, y, z, rx=0, ry=0, rz=0: B(w, h, d, x, y - 1.75, z, rx, ry, rz, HD)
    B(.95, .38, .85, 0, 1.86, -.02); hB(.98, 1.0, .95, 0, 2.5, -.05); hB(.84, .34, .3, 0, 2.08, .42, .1); hB(1.1, .2, .34, 0, 2.74, .44, .32); hB(.17, .36, .2, 0, 2.42, .5, -.1); hB(.5, .14, .12, 0, 2.2, .56)
    for s in (1, -1):
        hB(.3, .5, .2, s * .36, 2.32, .46, 0, s * -.25, s * -.1); hB(.2, 1.05, 1.0, s * .6, 2.52, -.05, 0, 0, s * -.05); hB(.26, .34, .5, s * .7, 2.98, -.05, 0, 0, s * .3)
        M.add(f'eye{s}', lambda p, c=rw(tuple(np.array((0, 1.75, 0)) + 1.3 * np.array((s * .26, 2.56 - 1.75, .48)))): ell((p - V(*c)) @ np.array(rot('y', .62), f32), (0, 0, 0), (.16, .06, .05)), EYE)
    hB(1.0, .22, 1.0, 0, 3.08, -.05)
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
    for (x, y, z, s_) in ((0, 3.75, -.1, .3), (.5, 1.74, .3, .28), (-.6, 1.74, -.3, .3), (.3, -.62, .72, .24), (-1.3, -1.95, 1.0, .5), (1.5, -2.0, .4, .55), (.2, -1.9, 1.5, .4), (-.4, -1.95, -1.7, .5)): moss(x, y, z, s_)
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

SPEC = {'swasp': (starhive, (-4.0, -2.0, -4.0), (4.0, 3.0, 4.0)), 'swasp_nest': (lambda M, G: starhive(M, G, 'nest'), (-2.2, -2.0, -2.2), (2.2, 3.0, 2.2)),
        'swasp_swarm': (lambda M, G: starhive(M, G, 'swarm'), (-4.0, -2.0, -4.0), (4.0, 2.0, 4.0)), 'kegg': (eggs, (-3.0, -3.5, -2.6), (3.0, 2.0, 2.9)),
        'gwhale': (ghostwhale, (-5.8, -2.6, -4.0), (4.8, 1.5, 4.0)), 'reat': (rockeaters, (-4.4, -3.0, -3.0), (3.6, 2.4, 3.4)),
        'cserp': (serpent, (-5.3, -1.2, -2.2), (5.6, 3.2, 2.2)), 'sent': (sentinel, (-4.5, -4.0, -4.5), (4.5, 4.7, 4.5)),
        'mnest': (hive, (-4.6, -2.0, -4.6), (4.6, 3.1, 4.6)), 'mnexus': (nexus, (-5.6, -2.1, -5.6), (5.6, 5.6, 5.6))}
def paint(P, N, A, E, idx):
    glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05; top = np.clip(N[:, 1], 0, 1); A[~glowing, :3] *= (1 + .3 * top[~glowing])[:, None]
if __name__ == '__main__':
    k = sys.argv[1]; f, lo, hi = SPEC[k]; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .04
    M = Model(lo, hi, vox); Gm = Model(lo, hi, vox); f(M, Gm); M.bake(sys.argv[2] + '/' + k, paint)
    if Gm.parts: Gm.bake(sys.argv[2] + '/' + k + '_g', None)
