# The Mimic sculpted after the owner's paintings (docs/art/mimic/stalker, titan): black glossy cables bundled into a living hull,
# cyan neural light in the gaps, a fanged skull for a prow. Owner: "make sure to do them without legs so they are more like ships":
# no legs; the cables that were legs and mane now sweep back as fins, keels and a streaming tail.
# python3 mim_sculpt.py <class> <outdir> [voxel]. Built at the class's unit scale (the game scales by MIM_D.s), in buildMimic's frame:
# spine along +x, head at x 1.85 L, back at y ~.8, so mimWave (with the legs off) still ripples the cables, nods the head, works the jaw.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import blade,  lerp, chain, spk, norm, oell

MIM_D = {
    'mstalk': dict(stalk=1, s=1, mane=44, hump=0.7, len=1, gape=0.95, tail=10), 'mhunt': dict(hunt=1, s=0.95, mane=8, hump=0.05, len=1.75, gape=0.85, tail=30),
    'mharv': dict(s=1.05, mane=6, hump=0, len=0.65, gape=0.3, tail=3, sac=1), 'massim': dict(s=1.1, mane=22, hump=1.0, len=1.0, gape=0.6, tail=6, plates=1),
    'mguard': dict(s=1.3, mane=10, hump=0.45, len=0.8, gape=0.35, tail=4, armour=1), 'mtitan': dict(s=1.5, mane=64, hump=1.15, len=1.15, gape=0.8, tail=18, brood=1),
    'malpha1': dict(s=1.35, mane=46, hump=.9, len=1.15, gape=.8, tail=14, alpha=1), 'malpha2': dict(s=1.3, mane=36, hump=.3, len=1.45, gape=.9, tail=24, alpha=1, tint=(.6, .42, 1.0)),
    'malpha3': dict(s=1.4, mane=30, hump=.5, len=1.0, gape=.6, tail=10, armour=1, alpha=1, tint=(.85, .94, 1.0)), 'malpha4': dict(s=1.35, mane=40, hump=.8, len=1.1, gape=.7, tail=12, brood=1, alpha=1, tint=(.25, 1.0, .75)),
    'momega': dict(s=2.0, mane=70, hump=1.2, len=1.3, gape=1.0, tail=30, alpha=1, omega=1), 'momegax': dict(s=2.0, mane=70, hump=1.2, len=1.3, gape=1.1, tail=30, alpha=1, omega=2, tint=(.85, .97, 1.0)),
}
def M_(c, r=.5, m=.1, e=None): d = {'c': c, 'r': r, 'm': m}; d.update({'e': e} if e else {}); return d

def cable(M, n, pts, r0, r1, mat, k=.015, rings=True):
    # v837 a ribbed conduit: raised armour bands every quarter unit (along its run), as the paintings' cables have
    rads = [r0 + (r1 - r0) * (i / (len(pts) - 1)) ** 1.2 for i in range(len(pts))]
    if not rings or r0 < .06: chain(M, n, pts, rads, mat, k); return
    for i in range(len(pts) - 1):
        a, b = np.array(pts[i], np.float32), np.array(pts[i + 1], np.float32); ab = b - a; l2 = float(ab @ ab) + 1e-9
        def f(p, a=a, b=b, ab=ab, l2=l2, r1=rads[i], r2=rads[i + 1], off=i * 1.7):
            d = rcone(p, tuple(a), tuple(b), r1, r2); t = np.clip(((p - a) @ ab) / l2, 0, 1) * np.sqrt(l2)
            return d - min(r1, r2) * .22 * np.clip((np.cos((t + off) * 25.) - .55) * 2.5, 0, 1)
        M.add(f'{n}{i}', f, mat, k)
def bez3(a, b, c, d, n=7):
    a, b, c, d = map(np.array, (a, b, c, d)); return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d) for t in np.linspace(0, 1, n)]

def mimic(M, k, MH=None, G=None):
    D = MIM_D[k]; L = D['len']; hump = D['hump']; rng = np.random.default_rng(sum(map(ord, k)) * 7)
    gl = D.get('tint', (.2, .85, 1.0)); GLOW = M_(tuple(x * .15 for x in gl), .2, .1, gl); GLOWS = M_(tuple(x * .1 for x in gl), .2, .1, tuple(x * .55 for x in gl))
    CAB = M_((.018, .02, .026), .18, .65); CABL = M_((.04, .05, .065), .15, .75); SHELL = M_((.03, .034, .042), .25, .7); FANG = M_((.42, .46, .52), .15, .6)
    EGG = M_((.08, .03, .14), .12, .3, (.3, .08, .5)); PLATE = M_((.14, .15, .17), .4, .85); PLL = M_((.4, .1, .05), .2, .2, (1., .5, .15))
    sp = np.array([(-2.6 * L, .35), (-1.6 * L, .55 + hump * .5), (-.4 * L, .72 + hump), (.8 * L, .9 + hump * .8), (1.75 * L, .8)])
    yc = lambda x: np.interp(x, sp[:, 0], sp[:, 1])
    if D.get('sac'):
        hx, hy, hs = 2.0, .55, .75
    else:
        hx, hy, hs = 1.85 * L, .78, 1.55
    # ------------------------------------------------ the hull: a long dark body under the cables, flattened and wide like a ship
    x0, x1 = -2.75 * L, 1.75 * L
    def rad(x): u = np.clip((x - x0) / (x1 - x0), 0, 1); return (.25 + .85 * np.maximum(0, np.sin(np.pi * u ** .8)) ** .7) * (1.0 if not D.get('sac') else .7)
    def hull(p, k_=1.0):
        x = p[..., 0]; r = rad(x) * k_; d = np.sqrt(((p[..., 1] - yc(x)) / .72) ** 2 + (p[..., 2] / 1.15) ** 2) - r
        return np.maximum(d * .7, np.maximum(x - x1 - .3, x0 - x))
    M.add('hull', hull, SHELL, .1)
    for j in range(6):  # neural light deep in the gaps between the cables
        x = x0 + (x1 - x0) * (.15 + .13 * j); M.add(f'ng{j}', lambda p, x=x: ell(p, (x, yc(x) + .1, 0), (.3, rad(x) * .7, rad(x) * 1.0)), GLOWS, .05)
    # cables wrapped along the hull, twisting gently, a few lit
    n = 26 + D['mane'] // 3
    for c in range(n):
        a0 = rng.uniform(0, 2 * np.pi); tw = rng.uniform(-1.2, 1.2); xs = np.linspace(x0 + rng.uniform(0, .5), x1 + .25 - rng.uniform(0, .4), 8); rr = 1.0 + rng.uniform(0, .12)
        pts = [(x, yc(x) + np.sin(a0 + tw * i / 7) * rad(x) * .72 * rr, np.cos(a0 + tw * i / 7) * rad(x) * 1.15 * rr) for i, x in enumerate(xs)]
        cable(M, f'c{c}', pts, .1 + rng.uniform(0, .05), .07, CABL if c % 7 == 3 else CAB)
    # ------------------------------------------------ swept fins of cable (what were the mane and the legs): a dorsal crest, two
    # pairs of side fins raked back like a ship's wings, a keel underneath; each a fan of cables curling at the tips
    def fan(tag, base_x0, base_x1, cnt, side, up, out, ln, r0):
        for i in range(cnt):
            u = i / max(1, cnt - 1); bx = base_x0 + (base_x1 - base_x0) * u + rng.uniform(-.1, .1); by = yc(bx) + up * rad(bx) * .65; bz = side * rad(bx) * 1.05 * abs(out) if out else rng.uniform(-.15, .15)
            Ln = ln * (.75 + .5 * np.sin(np.pi * (u * .8 + .1))) * rng.uniform(.85, 1.15)
            d = np.array((-1.0, up * .55, (side * out * .9) if out else 0)); d /= np.linalg.norm(d)
            a = (bx, by, bz); b = tuple(np.array(a) + d * Ln * .35 + np.array((0, up * .15, 0))); c_ = tuple(np.array(a) + d * Ln * .75 + np.array((0, up * .25, side * out * .2 if out else 0)))
            e = tuple(np.array(a) + d * Ln + np.array((.15 * Ln, up * .05 - .1, side * out * .35 if out else rng.uniform(-.2, .2))))
            cable(M, f'{tag}{i}', bez3(a, b, c_, e, 7), r0, .025, CABL if i % 5 == 2 else CAB)
            if i % 3 == 1: M.add(f'{tag}g{i}', lambda p, q=c_: sphere(p, q, r0 * .55), GLOW)
    nm = max(6, D['mane'] // 3)
    fan('dc', .9 * L, -1.9 * L, nm, 1, 1.0, 0, 1.6 * (1.3 if D.get('alpha') else 1), .11)
    for s in (1, -1):
        fan(f'sf{s}', .6 * L, -.9 * L, max(4, nm // 2), s, .25, 1.0, 2.3 * (1.2 if D.get('alpha') else 1), .12)
        fan(f'sr{s}', -1.0 * L, -2.2 * L, max(3, nm // 3), s, -.15, .8, 1.6, .1)
    fan('kl', .5 * L, -1.6 * L, max(4, nm // 3), 1, -1.0, 0, 1.0, .09)
    # ------------------------------------------------ the tail: cables streaming back from the stern like a drive plume, lit at the tips
    for i in range(D['tail'] + 4):
        z = rng.uniform(-.35, .35); y = rng.uniform(-.25, .25); Lt = (1.8 + rng.uniform(0, 2.2)) * (1.4 if D['tail'] > 10 else 1)
        a = (x0 + .25, yc(x0) + y * .6, z * .6); pts = bez3(a, (x0 - Lt * .35, a[1] + y, z * 1.6), (x0 - Lt * .7, a[1] + y * 1.8 + rng.uniform(-.3, .3), z * 2.6), (x0 - Lt, a[1] + y * 2.2 + rng.uniform(-.2, .4), z * 3.2), 7)
        cable(M, f't{i}', pts, .11, .02, CAB)
        if i % 2 == 0: M.add(f'tg{i}', lambda p, q=pts[-1]: sphere(p, q, .06), GLOW)
    M.add('drive', lambda p: torus(p, (x0 + .05, yc(x0), 0), 'x', .32, .07), CABL); M.add('drg', lambda p: ell(p, (x0 - .02, yc(x0), 0), (.1, .26, .26)), GLOW)
    # ------------------------------------------------ the neural cores on its back
    for j, (cx, cy) in enumerate(((-.9 * L, .65 + hump * .7), (.3 * L, .72 + hump * .8), (1.1 * L, .72))):
        top = yc(cx) + rad(cx) * .72
        M.add(f'core{j}', lambda p, c=(cx, top - .02, 0): ell(p, c, (.26, .16, .2)), GLOW)
        M.add(f'cring{j}', lambda p, c=(cx, top - .02, 0): torus(p, c, 'y', .27, .05), CABL)
    # ------------------------------------------------ v837 armour after the paintings: chrome hook plates overlapping down its spine, curved
    # hooks raking back off its flanks, and a seam of cyan light under every plate
    CHRB = M_((.26, .29, .33), .18, 1.)
    def hook(Mx, n, base, d1, d2, Ln, w, mat):  # a flat curved blade: out along d1, curling along d2 to a point
        a = np.array(base); m = a + np.array(norm(d1)) * Ln * .55; t = m + np.array(norm(d2)) * Ln * .5
        blade(Mx, n + 'a', tuple(a), norm(m - a), float(np.linalg.norm(m - a)) * 1.08, w, mat, 3.0, (0, 0, 1) if abs(d1[2]) < .5 else (0, 1, 0))
        blade(Mx, n + 'b', tuple(m), norm(t - m), float(np.linalg.norm(t - m)), w * .62, mat, 3.0, (0, 0, 1) if abs(d1[2]) < .5 else (0, 1, 0))
    nd = 7 if not D.get('sac') else 4
    for i in range(nd):
        x = (1.05 - i * .5) * L; top = yc(x) + rad(x) * .7; Ln = (.75 + .35 * np.sin(np.pi * (i + .5) / nd)) * (1.25 if D.get('alpha') else 1)
        M.add(f'dsg{i}', lambda p, c=(x - .05, top - .02, 0): ell(p, c, (.22, .06, .14)), GLOW)
        hook(M, f'dp{i}', (x, top - .05, 0), (-.55, 1, 0), (-1, -.35, 0), Ln, .2, CHRB)
    for s_ in (1, -1):
        for i in range(3):
            x = (.55 - i * .75) * L; base = (x, yc(x) + .1, s_ * rad(x) * 1.02)
            M.add(f'fsg{s_}{i}', lambda p, c=base: ell(p, c, (.25, .05, .08)), GLOW)
            hook(M, f'fh{s_}{i}', base, (-.6, .25, s_ * .8), (-1, -.15, s_ * .1), .95 - i * .15, .14, CHRB)
        for i in range(4):  # small crescent spines along the keel
            x = (.6 - i * .6) * L; base = (x, yc(x) - rad(x) * .68, s_ * .25)
            hook(M, f'ks{s_}{i}', base, (-.4, -1, s_ * .3), (-1, .2, 0), .45, .07, CHRB)
    # ------------------------------------------------ v837 the head, remastered after the paintings, sculpted on its own finer grid (MH):
    # a long armoured xeno skull swept back into a crest, faceted snout with nostril ridges, heavy blade brows over two pairs of slit eyes,
    # chrome cheek plates hooked back, a hinged lower jaw with a chin spike and mandible plates, two rows of curved fangs, cyan light
    # in the throat with strands of it strung between the jaws, and a ringed neck. G (drawn additively) holds the eye and throat bloom.
    H = MH if MH is not None else M
    CHR2 = M_((.26, .29, .33), .18, 1.); EYE = M_((.3, .9, 1.0), .1, .1, tuple(x * 2.6 for x in gl)); DRL = M_(tuple(x * .2 for x in gl), .1, .1, tuple(x * 1.2 for x in gl))
    def hq(p):  # into the head's frame (unit skull)
        return (p - V(hx, hy, 0)) / hs
    def hw_(x, y, z): return (hx + x * hs, hy + y * hs, z * hs)
    def sel(q, c, r, pw=1.45):  # a superellipsoid: angular where pw < 2
        a = np.abs((q - V(*c)) / V(*r)); return ((a[..., 0] ** pw + a[..., 1] ** pw + a[..., 2] ** pw) ** (1 / pw) - 1) * min(r) * .9
    sk = [(-.3, .02), (-.22, .42), (.05, .55), (.45, .47), (.85, .34), (1.25, .23), (1.6, .12), (1.82, .02)]
    SKY, SKZ = .6, .95
    def lathe(p, prof, c, sy, sz, pw=1.5):  # a profile turned round x with an angular (superellipse) cross-section
        q = p - V(*c); x = q[..., 0]; xs = np.array([a for a, _ in prof], f32); rs = np.array([b for _, b in prof], f32)
        r = np.interp(x, xs, rs, left=0, right=0); d = (np.abs(q[..., 1] / sy) ** pw + np.abs(q[..., 2] / sz) ** pw) ** (1 / pw) - r
        return np.maximum(d * min(sy, sz) * .85, np.maximum(x - xs[-1], xs[0] - x))
    skull = lambda p: lathe(hq(p), sk, (0, .12, 0), SKY, SKZ) * hs
    cran = lambda p: sel(hq(p), (-.35, .34, 0), (.85, .38, .46), 1.7) * hs
    crest = lambda p: (lambda q: sel(q, (0, 0, 0), (.75, .13, .16), 1.3))(((hq(p) - V(-.95, .62, 0)) @ rot('z', -.42).T)) * hs
    H.add('skull', skull, SHELL, .05); H.add('cran', cran, SHELL, .08); H.add('crest', crest, CHR2, .05)
    for j, (zs, ln, r) in enumerate(((0, 1.0, .1), (.17, .85, .075), (-.17, .85, .075), (.3, .6, .06), (-.3, .6, .06))):  # crest horns, curving back and down
        pts = bez3((-.55, .66, zs), (-1.1, .95 + .1 * ln, zs * 1.3), (-1.6 * ln - .2, 1.05 * ln, zs * 1.7), (-1.9 * ln - .3, .7 * ln, zs * 2.0), 7)
        rads = [r * (1 - i / 6) ** .8 + .006 for i in range(7)]
        for i in range(6): H.add(f'hn{j}{i}', lambda p, a=pts[i], b=pts[i + 1], r1=rads[i], r2=rads[i + 1]: rcone(hq(p), a, b, r1, r2) * hs, CHR2)
    for j in range(5):  # armour ribs across the cranium
        x = .25 - j * .24
        H.add(f'crb{j}', lambda p, x=x, j=j: np.maximum(np.abs(sel(hq(p), (-.35, .34, 0), (.88, .41, .49), 1.7)) - .018, np.abs(hq(p)[..., 0] - x) - .035) * hs, CHR2)
    skr = lambda x: float(np.interp(x, [a_ for a_, _ in sk], [b_ for _, b_ in sk]))
    ga = .2 + .26 * D['gape']; JC, JS = float(np.cos(ga)), float(np.sin(ga))
    def jq(p):  # the jaw's frame: rotate back up by the gape round its hinge
        q = hq(p) - V(-.05, -.16, 0); x = q[..., 0] * JC - q[..., 1] * JS; y = q[..., 0] * JS + q[..., 1] * JC
        return np.stack([x, y, q[..., 2]], -1)
    def jw(x, y, z): return (hx + (x * JC + y * JS - .05) * hs, hy + (-x * JS + y * JC - .16) * hs, z * hs)
    def jd(x, y, z): return norm((x * JC + y * JS, -x * JS + y * JC, z))
    jp = [(-.1, .02), (.12, .42), (.7, .36), (1.25, .22), (1.66, .05)]; JY, JZ = .48, .9
    jr = lambda x: float(np.interp(x, [a_ for a_, _ in jp], [b_ for _, b_ in jp]))
    jaw = lambda p: lathe(jq(p), jp, (0, 0, 0), JY, JZ) * hs
    H.add('jaw', jaw, SHELL, .04)
    H.add('chin', lambda p: rcone(jq(p), (1.45, -.04, 0), (1.95, -.2, 0), .07, .008) * hs, CHR2)  # the chin spike
    H.add('throat', lambda p: ell(hq(p), (.2, -.08, 0), (.55, .17, .3)) * hs, GLOW)
    H.add('maw', lambda p: ell(jq(p), (.55, .1, 0), (.85, .06, .24)) * hs, GLOW)
    H.add('gum', lambda p: ell(hq(p), (.8, .02, 0), (.95, .06, .34)) * hs, M_((.06, .02, .03), .3, .4, tuple(x * .35 for x in gl)))
    if G is not None:
        G.add('gthroat', lambda p: ell(hq(p), (.35, -.1, 0), (.95, .32, .45)) * hs, GLOW)
    for s in (1, -1):
        # the brows: heavy blades over the eyes, each ending in a spike swept back over the crown
        H.add(f'brow{s}', lambda p, s=s: (lambda q: sel(q, (0, 0, 0), (.5, .065, .12), 1.3))((hq(p) - V(.55, .4, s * .3)) @ (rot('y', s * .22) @ rot('z', -.12)).T) * hs, CHR2, .03)
        H.add(f'bsp{s}', lambda p, s=s: rcone(hq(p), (.2, .44, s * .36), (-.55, .66, s * .55), .06, .006) * hs, CHR2)
        # two pairs of slit eyes, slanting, lit hard
        for (ex, ey, ez, rx, ry, rz, tl) in ((.74, .29, .33, .15, .028, .055, .3), (.47, .33, .4, .09, .02, .04, .25)):
            H.add(f'eye{s}{ex}', lambda p, s=s, e=(ex, ey, ez), r=(rx, ry, rz), tl=tl: ell((hq(p) - V(e[0], e[1], s * e[2])) @ (rot('z', -tl) @ rot('y', s * .3)).T, (0, 0, 0), r) * hs, EYE)
            H.add(f'eso{s}{ex}', lambda p, s=s, e=(ex, ey, ez), r=(rx, ry, rz), tl=tl: ell((hq(p) - V(e[0] - .01, e[1] - .005, s * (e[2] - .03))) @ (rot('z', -tl) @ rot('y', s * .3)).T, (0, 0, 0), (r[0] * 1.35, r[1] * 2.2, r[2] * 1.2)) * hs, M_((.008, .01, .014), .5, .3), .015)
            if G is not None: G.add(f'geye{s}{ex}', lambda p, s=s, e=(ex, ey, ez), r=rx: ell(hq(p), (e[0], e[1], s * (e[2] + .03)), (r * 1.7, r * .9, r * .9)) * hs, EYE)
        # the cheek plates, chrome, hooked back past the jaw hinge
        H.add(f'chk{s}', lambda p, s=s: (lambda q: sel(q, (0, 0, 0), (.42, .16, .05), 1.3))((hq(p) - V(.25, .12, s * .47)) @ (rot('y', s * .18) @ rot('z', .2)).T) * hs, CHR2, .02)
        H.add(f'chh{s}', lambda p, s=s: rcone(hq(p), (-.08, .07, s * .5), (-.55, -.12, s * .6), .07, .006) * hs, CHR2)
        # nostril ridges down the snout, ending in lit pits
        H.add(f'nr{s}', lambda p, s=s: rcone(hq(p), (.55, .41, s * .1), (1.55, .2, s * .07), .045, .02) * hs, CHR2)
        H.add(f'ns{s}', lambda p, s=s: ell(hq(p), (1.5, .2, s * .085), (.05, .018, .025)) * hs, DRL)
        # the mandible plates along the lower jaw
        H.add(f'mp{s}', lambda p, s=s: (lambda q: sel(q, (0, 0, 0), (.55, .07, .04), 1.3))((jq(p) - V(.55, -.05, s * .33)) @ rot('y', s * .12).T) * hs, CHR2, .02)
        # fangs: an outer row, long at the front, and a shorter inner row, all curving in and back
        for row, (nu, zf, lf) in enumerate(((12, .78, 1.0), (9, .5, .55))):
            for i in range(nu):
                u = i / (nu - 1); x = 1.66 - 1.45 * u; r = skr(x); L0 = (.62 if i == 1 else .45 if i == 0 else .17 + .17 * (1 - u)) * lf * rng.uniform(.75, 1.2)
                b0 = np.array(hw_(x, .12 - r * SKY * .6, s * r * SKZ * zf)); d1 = np.array(norm((.2, -1, s * .1))); d2 = np.array(norm((-.25, -1, -s * .4)))
                m = b0 + d1 * L0 * .55 * hs; t = m + d2 * L0 * .5 * hs
                chain(H, f'fu{row}{s}{i}', [tuple(b0), tuple(m), tuple(t)], [.04 * hs * lf ** .5, .022 * hs * lf ** .5, .003 * hs], FANG)
            for i in range(nu - 1):
                u = i / (nu - 2); x = 1.55 - 1.35 * u; r = jr(x); L0 = (.5 if i == 1 else .34 if i == 0 else .15 + .15 * (1 - u)) * lf * rng.uniform(.75, 1.2)
                b0 = np.array(jw(x, r * JY * .58, s * r * JZ * zf)); d1 = np.array(jd(.2, 1, s * .1)); d2 = np.array(jd(-.25, 1, -s * .4))
                m = b0 + d1 * L0 * .55 * hs; t = m + d2 * L0 * .5 * hs
                chain(H, f'fl{row}{s}{i}', [tuple(b0), tuple(m), tuple(t)], [.036 * hs * lf ** .5, .02 * hs * lf ** .5, .003 * hs], FANG)
        # strands of light strung between the jaws
        for j, x in enumerate((1.05, .6)):
            a = np.array(hw_(x, .12 - skr(x) * SKY * .55, s * skr(x) * SKZ * .45)); b = np.array(jw(x - .05, jr(x) * JY * .55, s * jr(x) * JZ * .45))
            m = (a + b) / 2 + np.array((-.06 * hs, 0, 0)); chain(H, f'dr{s}{j}', [tuple(a), tuple(m), tuple(b)], [.012 * hs, .007 * hs, .012 * hs], DRL)
        # a few cables over the face, as in the paintings, leaving the eyes and the snarl clear
        for j in range(3):
            th = [1.2, .95, -.2][j]; xe = [1.0, 1.25, .9][j]
            def sp_(x, th=th, j=j):
                r = skr(x) * 1.04 + .03; ang = th + .1 * np.sin(x * 4. + j)
                return hw_(x, .12 + np.sin(ang) * r * SKY, s * np.cos(ang) * r * SKZ)
            cable(H, f'fc{s}{j}', [sp_(x) for x in np.linspace(-.45, xe, 8)], .06 * hs, .025 * hs, CABL if j == 1 else CAB)
        for j in range(3):  # cables over the crown, swept back into the hull (on the body's grid)
            a = (hx + (.2 - j * .25) * hs, hy + (.5 + .05 * j) * hs, s * (.15 + .1 * j) * hs)
            cable(M, f'cr{s}{j}', bez3(a, (hx - .3 * hs, hy + .65 * hs, s * .3 * hs), (hx - .9 * hs, hy + .55 * hs, s * .35 * hs), (x1 - .6, yc(x1 - .6) + .45, s * .3), 7), .09, .07, CAB)
    for j in range(4):  # the ringed neck
        x = -.75 - j * .28
        H.add(f'nk{j}', lambda p, x=x, j=j: sel(hq(p), (x, .2 - j * .02, 0), (.16, .36 - j * .02, .42 - j * .02), 1.8) * hs, SHELL, .03)
        H.add(f'nkr{j}', lambda p, x=x, j=j: (lambda q: np.sqrt((np.sqrt((q[..., 1] / .9) ** 2 + q[..., 2] ** 2) - (.42 - j * .02)) ** 2 + (q[..., 0] * 1.6) ** 2) - .035)(hq(p) - V(x + .14, .2 - j * .02, 0)) * hs, CHR2)
    # ------------------------------------------------ the classes
    CHR = M_((.5, .54, .6), .16, 1.); GOLD = M_((.46, .34, .13), .25, 1.)
    if D.get('sac'):  # v836 the Harvester, after its painting: a mane of tentacles, a dark caged sac, and long harvesting tendrils that
        # reach forward and down from under the head, each ending in a glass canister of glowing biomass ringed with spiked metal
        c0 = (-.5, .5, 0); M.add('sac', lambda p: ell(p, c0, (1.15, .85, .95)), M_((.02, .05, .07), .1, .3, (.04, .2, .28)), .1)
        for i in range(12):
            a = i / 12 * 2 * np.pi; cable(M, f'cd{i}', bez3((.9, .65, 0), (.4, .5 + np.sin(a) * 1.05, np.cos(a) * 1.15), (-1.2, .5 + np.sin(a) * 1.0, np.cos(a) * 1.1), (-1.9, .6 + np.sin(a) * .25, np.cos(a) * .25), 8), .1, .08, CAB)
        for i in range(10):  # the mane: tentacles curling up and back off its shoulders
            z = (i - 4.5) * .22; a = (rng.uniform(-.6, .8), 1.0 + rng.uniform(0, .3), z); Lm = rng.uniform(1.8, 2.8)
            cable(M, f'mn{i}', bez3(a, (a[0] + .2, a[1] + Lm * .5, z * 1.3), (a[0] - Lm * .5, a[1] + Lm * .75, z * 1.6), (a[0] - Lm * .9, a[1] + Lm * .35, z * 1.9), 8), .11, .03, CABL if i % 3 == 1 else CAB)
        CAN = M_((.04, .12, .16), .05, .2, (.15, .75, 1.0))
        for i, (z, Lg, drop) in enumerate(((-1.0, 1.8, .8), (-.5, 2.2, 1.05), (.0, 2.5, .9), (.5, 2.2, 1.05), (1.0, 1.8, .8), (-1.4, 1.4, .55), (1.4, 1.4, .55))):
            a = (1.2, .05, z * .45); e = (1.3 + Lg, -.1 - drop, z * 1.5)
            pts = bez3(a, (a[0] + Lg * .35, .45, z * .8), (a[0] + Lg * .75, -.4, z * 1.1), e, 8); cable(M, f'ht{i}', pts, .12, .07, CABL if i % 2 else CAB)
            d = np.array(norm(np.array(e) - np.array(pts[-2]))); c = np.array(e) + d * .3
            M.add(f'cg{i}', lambda p, c=tuple(c), d=tuple(d): rcone(p, tuple(np.array(c) - np.array(d) * .26), tuple(np.array(c) + np.array(d) * .26), .17, .15), CAN)
            for u in (-1, 0, 1):
                rc = tuple(c + d * u * .24); M.add(f'cr{i}{u}', lambda p, rc=rc, d=tuple(d): np.maximum(np.abs(np.sqrt(((p - V(*rc)) ** 2).sum(-1)) - .2) - .035, np.abs((p - V(*rc)) @ V(*d)) - .035), CHR)
            for u in range(4):
                ang = u * np.pi / 2; perp = np.array(norm(np.cross(d, (0, 1, 0)) * np.cos(ang) + np.array((0, 1, 0)) * np.sin(ang)))
                spk(M, f'cs{i}{u}', tuple(c + d * .22 + perp * .17), tuple(norm(d + perp * .5)), .28, .045, CHR)
    if D.get('armour'):  # v836 the Guardian, after its painting: silver-plated shoulders trimmed in gold, the carapace down its back, and
        # two great round energy shields held at its flanks like wings, gold-rimmed, a cyan hexagon lattice of light across each face
        for i in range(5):
            x = (1.2 - i * .75) * L; top = yc(x) + rad(x) * .72
            M.add(f'ap{i}', lambda p, c=(x, top + .02, 0): np.maximum(ell(p, c, (.7 * L, .32, rad(x) * 1.25 + .15)), -(p[..., 1] - c[1] + .12)), SHELL, .03)
            M.add(f'at{i}', lambda p, c=(x, top + .02, 0): np.maximum(np.abs(ell(p, c, (.72 * L, .34, rad(x) * 1.27 + .17))) - .02, np.abs(p[..., 0] - c[0] - .55 * L) - .06), GOLD)
        HEX = M_((.012, .04, .06), .08, .3, (.02, .12, .22)); HEXL = M_((.06, .2, .26), .1, .2, (.3, 1.0, 1.3))
        for s in (1, -1):
            sh = (.55 * L, .95, s * 1.05)
            M.add(f'sp{s}', lambda p, c=sh, s=s: ell(p, c, (.75, .45, .55)), CHR, .05)  # the pauldron
            M.add(f'spg{s}', lambda p, c=sh: np.maximum(np.abs(ell(p, c, (.78, .48, .58))) - .025, -(p[..., 1] - c[1] - .1)), GOLD)
            for j in range(3): spk(M, f'pk{s}{j}', (sh[0] - .3 + j * .3, sh[1] + .35, sh[2] * 1.05), norm((-.6, 1, s * .4)), .55 - .1 * j, .1, CHR)
            cen = np.array((-.35 * L, 1.7, s * 2.05)); R = rot('y', -s * .8) @ rot('x', s * .5)  # the shield's frame: its face looks out to the side
            nrm = R @ np.array((0, 0, 1.0), f32)
            def disc(p, cen=cen, R=R, r=1.55, t=.06):
                q = (p - cen) @ R; return np.maximum(np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - r, np.abs(q[..., 2]) - t)
            def rim(p, cen=cen, R=R):
                q = (p - cen) @ R; rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2); return np.sqrt((rr - 1.58) ** 2 + (q[..., 2] * 1.0) ** 2) - .11
            def rim2(p, cen=cen, R=R):
                q = (p - cen) @ R; rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2); return np.maximum(np.abs(rr - 1.36) - .035, np.abs(q[..., 2]) - .1)
            def hexl(p, cen=cen, R=R):  # a lattice of hexagon cells on both faces
                q = (p - cen) @ R; X, Y = q[..., 0] / .42, q[..., 1] / .42
                ax = np.mod(X, 1.0) - .5; ay = np.mod(Y, 1.7320508) - .8660254; bx = np.mod(X - .5, 1.0) - .5; by = np.mod(Y - .8660254, 1.7320508) - .8660254
                pa = ax * ax + ay * ay < bx * bx + by * by; gx = np.where(pa, ax, bx); gy = np.where(pa, ay, by)
                hd = np.maximum(np.abs(gx), np.abs(gx) * .5 + np.abs(gy) * .8660254); e = (.5 - hd) * .42
                rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2)
                return np.maximum(np.maximum(e - .02, np.abs(q[..., 2]) - .1), rr - 1.34)
            (G if G is not None else M).add(f'sd{s}', disc, M_((.05, .25, .4), .1, .2, (.15, .6, 1.0)) if G is not None else HEX); M.add(f'sh{s}', hexl, HEXL); M.add(f'sr{s}', rim, GOLD); M.add(f'sr2{s}', rim2, CHR)
            M.add(f'sb{s}', lambda p, a=(sh[0] - .2, sh[1] - .1, sh[2] * .9), b=tuple(cen - nrm * .2 + np.array((0, .1, 0))): rcone(p, a, b, .16, .12), CHR)  # the arm that holds it
            M.add(f'sc{s}', lambda p, c=tuple(cen + nrm * .12): sphere(p, c, .22), M_((.2, .7, .9), .1, .2, (.5, 1.2, 1.5)))
            M.add(f'scr{s}', lambda p, c=tuple(cen + nrm * .1), R=R: (lambda q: np.sqrt((np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - .3) ** 2 + q[..., 2] ** 2) - .05)((p - V(*c)) @ R), GOLD)
    if D.get('plates'):  # v836 the Assimilator, after its painting: a stolen starship fused into its back (a grey hull with spires and
        # running lights), and a great reactor wheel set in each flank, its rings of segments around a blazing core
        hb = (-.6 * L, yc(-.6 * L) + rad(-.6 * L) * .62 + .25, .15)
        M.add('sh', lambda p: box(p, hb, (1.1 * L, .22, .42), .05, rot('z', .12) @ rot('y', .2)), PLATE, .04)
        M.add('sh2', lambda p: box(p, (hb[0] - .35, hb[1] + .3, hb[2]), (.55, .16, .3), .04, rot('z', .12) @ rot('y', .2)), PLATE, .03)
        M.add('sh3', lambda p: box(p, (hb[0] + .8, hb[1] - .05, hb[2] + .1), (.5, .12, .5), .04, rot('y', .5)), PLATE, .03)
        for i in range(4):
            bx = hb[0] - .6 + i * .22; M.add(f'spi{i}', lambda p, bx=bx, h=.7 - i * .1: rcone(p, (bx, hb[1] + .4, hb[2]), (bx, hb[1] + .4 + h, hb[2]), .045, .008), CHR)
        for i in range(8):
            c = (hb[0] - .9 + i * .3, hb[1] + .05, hb[2] + (.43 if i % 2 else -.43)); M.add(f'pll{i}', lambda p, c=c: sphere(p, c, .045), PLL)
        for i in range(6):  # cables clutching the stolen hull
            x = hb[0] - .9 + i * .38; cable(M, f'clh{i}', bez3((x, yc(x) + .2, -.6), (x + .1, hb[1] + .45, -.3), (x + .2, hb[1] + .45, .5), (x + .1, yc(x) + .15, .75), 6), .08, .07, CAB)
        RC = M_((.2, .7, .9), .1, .2, (.8, 1.5, 1.8)); RS = M_((.2, .21, .23), .28, 1.)
        for s in (1, -1):
            cen = np.array((.1 * L, yc(.1 * L) - .05, s * (rad(.1 * L) * 1.4 + .3)))
            def tor(p, r, w, cen=cen):  # rings facing out along z
                q = p - cen; rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2); return np.sqrt((rr - r) ** 2 + (q[..., 2] * 1.6) ** 2) - w
            def segs(p, r0, r1, n, cen=cen):
                q = p - cen; rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2); an = np.arctan2(q[..., 1], q[..., 0]); g = np.abs(np.mod(an * n / (2 * np.pi) + .5, 1) - .5) * 2 * np.pi * rr / n
                return np.maximum(np.maximum(np.abs(rr - (r0 + r1) / 2) - (r1 - r0) / 2, np.abs(q[..., 2]) - .09), .04 - g)
            M.add(f'rw{s}', lambda p, sg=segs: sg(p, .95, 1.22, 22), RS); M.add(f'rw2{s}', lambda p, sg=segs: sg(p, .55, .78, 12), RS)
            M.add(f'rr{s}', lambda p, tr=tor: tr(p, 1.27, .06), CHR); M.add(f'rr2{s}', lambda p, tr=tor: tr(p, .86, .045), CHR)
            M.add(f'rg{s}', lambda p, c=tuple(cen): ell(p, c, (.5, .5, .18)), GLOW)
            (G if G is not None else M).add(f'rbk{s}', lambda p, c=tuple(cen - np.array((0, 0, s * .16))): np.maximum(np.sqrt((p[..., 0] - c[0]) ** 2 + (p[..., 1] - c[1]) ** 2) - 1.24, np.abs(p[..., 2] - c[2]) - .03), M_(tuple(x * .05 for x in gl), .3, .2, tuple(x * .22 for x in gl)))
            M.add(f'rgc{s}', lambda p, c=tuple(cen + np.array((0, 0, s * .1))): sphere(p, c, .18), RC)
            for j in range(8):  # cables binding the wheel into the flesh
                a = j / 8 * 2 * np.pi; cable(M, f'rb{s}{j}', [tuple(cen + np.array((np.cos(a) * 1.3, np.sin(a) * 1.3, -s * .05))), tuple(cen + np.array((np.cos(a) * 1.45, np.sin(a) * 1.3, -s * .45))), tuple(cen + np.array((np.cos(a) * 1.0, np.sin(a) * .6, -s * .95)))], .07, .06, CAB)
    if D.get('stalk'):  # v797 the Stalker, after its painting: a writhing mass of cables arching high over its back, and hooked
        # grapple tendrils reaching forward beneath the jaws (still no legs: they trail like a ship's grapples)
        for i in range(12):
            bx = (-1.6 + i * .24) * L; z = rng.uniform(-.7, .7); hgt = rng.uniform(1.4, 2.6); a = (bx, yc(bx) + rad(bx) * .6, z)
            pts = bez3(a, (bx + .3, a[1] + hgt, z * 1.4), (bx - 1.4, a[1] + hgt * 1.1, z * 2.0), (bx - 2.2, a[1] + hgt * .45, z * 2.4), 8)
            cable(M, f'sw{i}', pts, .12, .03, CABL if i % 4 == 1 else CAB)
        for s_ in (1, -1):
            for j in range(3):
                a = (hx - .4 * hs, hy - .45 * hs, s_ * (.25 + .2 * j) * hs); Lg = 1.6 + .4 * j
                pts = bez3(a, (a[0] + Lg * .3, a[1] - .7, a[2] * 1.5), (a[0] + Lg * .75, a[1] - .9, a[2] * 1.9), (a[0] + Lg, a[1] - .55, a[2] * 2.0), 7)
                cable(M, f'gt{s_}{j}', pts, .12, .07, CAB)
                for u in range(3): spk(M, f'gc{s_}{j}{u}', pts[-1], norm((1, -.8 + u * .35, s_ * (u - 1) * .5)), .55, .07, FANG)
    if D.get('hunt'):  # v836 the Hunter, after its painting: chrome armour over the skull, two great chrome scythes held forward under its
        # jaws like a mantis's (no legs: they fold under the prow), a segmented tail arched high over its back ending in a hooked blade
        for s_ in (1, -1):
            sh = (hx - .55 * hs, hy - .35 * hs, s_ * .42 * hs); el = (hx + .35 * hs, hy - 1.05 * hs, s_ * .6 * hs)
            cable(M, f'sa{s_}', [sh, ((sh[0] + el[0]) / 2, (sh[1] + el[1]) / 2 - .1, s_ * .55 * hs), el], .2, .13, SHELL)
            M.add(f'sae{s_}', lambda p, c=el: sphere(p, c, .17), CHR)
            # the scythe: a long curved chrome blade from the elbow sweeping forward and up, its edge lit
            P0 = np.array(el); pts = bez3(tuple(P0), tuple(P0 + np.array((.8, -.25, s_ * .05)) * hs), tuple(P0 + np.array((1.6, .05, s_ * .1)) * hs), tuple(P0 + np.array((2.05, .6, s_ * .12)) * hs), 9)
            z0 = pts[0][2]
            def scy(p, pts=pts, z0=z0):  # one smooth blade: the curve's cones, squashed thin across z
                q = p.copy(); q[..., 2] = z0 + (p[..., 2] - z0) * 3.4; d = None
                for k_ in range(len(pts) - 1):
                    r1 = .2 * (1 - k_ / 8) ** .8 + .012; r2 = .2 * (1 - (k_ + 1) / 8) ** .8 + .01
                    e = rcone(q, pts[k_], pts[k_ + 1], r1, r2); d = e if d is None else np.minimum(d, e)
                return d / 3.4 * 1.6
            M.add(f'sy{s_}', scy, CHR)
            cable(M, f'sye{s_}', [tuple(np.array(q) + np.array((0, -.06, 0))) for q in pts], .035, .01, GLOW)
        # the scorpion tail: from the stern, up and over the back, the blade hooked forward above its head
        tp = bez3((x0 + .2, yc(x0) + .2, 0), (x0 - 1.4, 2.6, 0), (-.4 * L, 4.1, 0), (1.0 * L, 3.3, 0), 12)
        for k_ in range(len(tp) - 1):
            M.add(f'ts{k_}', lambda p, a=tp[k_], b=tp[k_ + 1], r=.24 - k_ * .013: rcone(p, a, b, r, r * .92), SHELL, .02)
            M.add(f'tsr{k_}', lambda p, c=tp[k_ + 1], r=.24 - k_ * .013: sphere(p, c, r * 1.08), CHR if k_ % 2 else SHELL)
            if k_ % 2 == 0: M.add(f'tsg{k_}', lambda p, c=tp[k_ + 1], r=.24 - k_ * .013: sphere(p, (c[0], c[1] - r * .7, c[2]), r * .35), GLOW)
        tip = np.array(tp[-1]); M.add('tbl', lambda p: spike(p, tuple(tip), tuple(tip + np.array((.9, -.85, 0))), .2), CHR)
        blade(M, 'tbl2', tuple(tip), norm((.4, -1, 0)), 1.1, .16, CHR, 2.8, (0, 0, 1))
    if D.get('brood'):  # the Brood Titan: violet brood sacs swelling along its flanks
        for i in range(8):
            s = 1 if i % 2 else -1; x = (-1.8 + (i >> 1) * .8) * L
            M.add(f'eg{i}', lambda p, c=(x, yc(x) - .1 + rng.uniform(0, .25), s * (rad(x) * 1.1 + .1)), r0=rng.uniform(.28, .4): ell(p, c, (r0 * 1.1, r0 * 1.25, r0)), EGG, .05)
    if D.get('alpha'):  # an Alpha: a crown of great hooked spines swept back from the skull, its neural core laid open along its back
        for i in range(7):
            a = (i - 3) * .32; base = (hx - .15 * hs, hy + .35 * hs, a * .45 * hs); Ls = (1.6 + (3 - abs(i - 3)) * .45)
            d = norm((-1, 1.1 - abs(a) * .3, a * 1.4)); mid = tuple(np.array(base) + np.array(d) * Ls * .6); tip = tuple(np.array(base) + np.array(d) * Ls + np.array((-.35 * Ls, -.15 * Ls, 0)))
            chain(M, f'cs{i}', [base, mid, tip], [.17, .1, .015], SHELL)
        cp = (-.3 * L, yc(-.3 * L) + rad(-.3 * L) * .72 + .2, 0)
        M.add('acore', lambda p: ell(p, cp, (.9, .45, .55)), GLOW); M.add('acr', lambda p: np.maximum(np.abs(ell(p, cp, (1.05, .55, .7))) - .05, p[..., 1] - cp[1] - .05), CABL)
        for i in range(8):
            a = i / 8 * 2 * np.pi; cable(M, f'ac{i}', bez3((cp[0] + np.cos(a) * 1.0, cp[1] - .1, np.sin(a) * .6), (cp[0] + np.cos(a) * .8, cp[1] + .4, np.sin(a) * .45), (cp[0] + np.cos(a) * .3, cp[1] + .6, np.sin(a) * .2), (cp[0], cp[1] + .7, 0), 6), .1, .035, CABL)
    if D.get('omega'):  # Omega: two great grappling arms reaching forward over its prow, and long tendrils reaching ahead
        for s in (1, -1):
            sh = (1.0 * L, yc(L) + .6, s * .6); el = (2.2 * L, 2.4, s * 1.7); wr = (3.3 * L, 1.7, s * 1.25)
            cable(M, f'oa{s}', [sh, el, wr], .38, .24, SHELL);
            for j in range(9): cable(M, f'ob{s}{j}', [tuple(np.array(sh) + rng.uniform(-.2, .2, 3)), tuple(np.array(el) + rng.uniform(-.25, .25, 3)), tuple(np.array(wr) + rng.uniform(-.2, .2, 3))], .1, .07, CAB)
            for i in range(4):
                a = (i - 1.5) * .5; d = norm((1, -.6 + a * .3, s * a)); mid = tuple(np.array(wr) + np.array(d) * .8); tip = tuple(np.array(wr) + np.array(d) * 1.5 + np.array((0, -.4, 0)))
                chain(M, f'oc{s}{i}', [wr, mid, tip], [.12, .08, .012], FANG)
        for i in range(8):
            z = rng.uniform(-.8, .8); y = rng.uniform(.6, 1.8); Lg = rng.uniform(3, 5)
            cable(M, f'ot{i}', bez3((hx - .5, y, z), (hx + Lg * .4, y + rng.uniform(-.5, .5), z * 1.5), (hx + Lg * .8, y - .3 + rng.uniform(-.7, .7), z * 2), (hx + Lg, y - .8, z * 2.2), 7), .1, .02, CABL if i % 3 == 0 else CAB)
        if D['omega'] == 2:  # Unbound: its neural core torn open, ringed with spines
            cp = (-.2 * L, 1.9 + hump, 0); M.add('ocore', lambda p: sphere(p, cp, 1.2), GLOW)
            for i in range(12):
                a = i / 12 * 2 * np.pi; b = (cp[0] + np.cos(a) * 1.1, cp[1] + np.sin(a) * .9, np.sin(a) * 1.0)
                spk(M, f'os{i}', b, norm((np.cos(a), np.sin(a) * .7 + .4, np.sin(a))), 1.2, .14, SHELL)

def bounds(k):
    D = MIM_D[k]; L = D['len']; ex = 2.5 + (2.0 if D.get('omega') else 0) + (D['tail'] > 10) * 1.5
    return (-2.75 * L - 4.5 - (D['tail'] > 10) * 1.6, -2.8, -4.2 - (1 if D.get('omega') else 0)), (1.85 * L + 3.2 + (4.5 * L + 1 if D.get('omega') else 0) + (1.2 if D.get('hunt') or D.get('sac') else 0), 4.6 + D['hump'] + (1.5 if D.get('alpha') else 0) + (1.5 if D.get('omega') else 0), 4.2 + (1 if D.get('omega') else 0))
def paint(P, N, A, E, idx):
    glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05; top = np.clip(N[:, 1], 0, 1); A[~glowing, :3] *= (1 + .4 * top[~glowing])[:, None]
def bake_merge(models, path, paint=None):
    # mesh several models (each on its own grid) and write them as one
    Ps, Ns, Fs, As, Es = [], [], [], [], []; off = 0
    for Mx in models:
        if not Mx.parts: continue
        P, N, F, idx, ao = Mx.mesh(); mats = [m for (_, _, m, _) in Mx.parts]; cm = [m for (_, _, m, _) in Mx.carves]
        A = np.zeros((len(P), 4), np.float32); E = np.zeros((len(P), 4), np.float32)
        for i in np.unique(idx):
            sel_ = idx == i; m = cm[i - 100000] if i >= 100000 else mats[i]
            A[sel_, :3] = m['c']; A[sel_, 3] = m.get('r', .5); E[sel_, :3] = m.get('e', (0, 0, 0)); E[sel_, 3] = m.get('m', .7)
        if paint: paint(P, N, A, E, idx)
        A[:, :3] *= ao[:, None] ** 1.2; E[:, :3] *= np.clip(ao[:, None] + .45, 0, 1)
        Ps.append(P); Ns.append(N); As.append(A); Es.append(E); Fs.append(F + off); off += len(P)
    import os; os.makedirs(path, exist_ok=True)
    for k_, a in (('P', np.concatenate(Ps)), ('N', np.concatenate(Ns)), ('A', np.concatenate(As)), ('E', np.concatenate(Es))): np.ascontiguousarray(a, np.float32).tofile(f'{path}/{k_}.bin')
    np.ascontiguousarray(np.concatenate(Fs), np.uint32).tofile(f'{path}/F.bin'); print(path, off, 'verts', sum(len(f) for f in Fs), 'tris')
def head_bounds(k):
    D = MIM_D[k]; L = D['len']; hx, hy, hs = (2.0, .55, .75) if D.get('sac') else (1.85 * L, .78, 1.55)
    return (hx - 2.2 * hs, hy - 1.25 * hs, -.95 * hs), (hx + 2.15 * hs, hy + 1.45 * hs, .95 * hs)
if __name__ == '__main__':
    k = sys.argv[1]; lo, hi = bounds(k); vox = float(sys.argv[3]) if len(sys.argv) > 3 else .04
    M = Model(lo, hi, vox); hl, hh = head_bounds(k); MH = Model(hl, hh, vox * .5); Gm = Model(lo, hi, vox * 1.5)
    mimic(M, k, MH, Gm)
    if len(sys.argv) > 4 and sys.argv[4] == 'head': bake_merge([MH], sys.argv[2] + '/' + k + '_head', paint); sys.exit()
    bake_merge([M, MH], sys.argv[2] + '/' + k, paint)
    if Gm.parts: Gm.bake(sys.argv[2] + '/' + k + '_g', None)
