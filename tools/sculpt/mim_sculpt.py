# The Mimic sculpted after the owner's paintings (docs/art/mimic/stalker, titan): black glossy cables bundled into a living hull,
# cyan neural light in the gaps, a fanged skull for a prow. Owner: "make sure to do them without legs so they are more like ships":
# no legs; the cables that were legs and mane now sweep back as fins, keels and a streaming tail.
# python3 mim_sculpt.py <class> <outdir> [voxel]. Built at the class's unit scale (the game scales by MIM_D.s), in buildMimic's frame:
# spine along +x, head at x 1.85 L, back at y ~.8, so mimWave (with the legs off) still ripples the cables, nods the head, works the jaw.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, chain, spk, norm, oell

MIM_D = {
    'mstalk': dict(s=1, mane=26, hump=.5, len=1, gape=.55, tail=8), 'mhunt': dict(s=.95, mane=18, hump=.15, len=1.35, gape=.8, tail=16),
    'mharv': dict(s=1, mane=12, hump=0, len=.8, gape=.35, tail=4, sac=1), 'massim': dict(s=1.05, mane=20, hump=.45, len=1.05, gape=.6, tail=8, plates=1),
    'mguard': dict(s=1.15, mane=14, hump=.25, len=.9, gape=.4, tail=6, armour=1), 'mtitan': dict(s=1.25, mane=40, hump=.8, len=1.1, gape=.7, tail=12, brood=1),
    'malpha1': dict(s=1.35, mane=46, hump=.9, len=1.15, gape=.8, tail=14, alpha=1), 'malpha2': dict(s=1.3, mane=36, hump=.3, len=1.45, gape=.9, tail=24, alpha=1, tint=(.6, .42, 1.0)),
    'malpha3': dict(s=1.4, mane=30, hump=.5, len=1.0, gape=.6, tail=10, armour=1, alpha=1, tint=(.85, .94, 1.0)), 'malpha4': dict(s=1.35, mane=40, hump=.8, len=1.1, gape=.7, tail=12, brood=1, alpha=1, tint=(.25, 1.0, .75)),
    'momega': dict(s=2.0, mane=70, hump=1.2, len=1.3, gape=1.0, tail=30, alpha=1, omega=1), 'momegax': dict(s=2.0, mane=70, hump=1.2, len=1.3, gape=1.1, tail=30, alpha=1, omega=2, tint=(.85, .97, 1.0)),
}
def M_(c, r=.5, m=.1, e=None): d = {'c': c, 'r': r, 'm': m}; d.update({'e': e} if e else {}); return d

def cable(M, n, pts, r0, r1, mat, k=.015):
    rads = [r0 + (r1 - r0) * (i / (len(pts) - 1)) ** 1.2 for i in range(len(pts))]; chain(M, n, pts, rads, mat, k)
def bez3(a, b, c, d, n=7):
    a, b, c, d = map(np.array, (a, b, c, d)); return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d) for t in np.linspace(0, 1, n)]

def mimic(M, k):
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
    # ------------------------------------------------ the prow: a long fanged skull, the jaw dropped open on a glowing throat, cyan eyes
    sk = [(-.3, .02), (-.22, .42), (.05, .56), (.4, .5), (.75, .38), (1.1, .26), (1.38, .15), (1.5, .03)]
    def lathe(p, prof, c, sy, sz):
        q = p - V(*c); x = q[..., 0]; xs = np.array([a for a, _ in prof], f32); rs = np.array([b for _, b in prof], f32)
        r = np.interp(x, xs, rs, left=0, right=0); d = np.sqrt((q[..., 1] / sy) ** 2 + (q[..., 2] / sz) ** 2) - r
        return np.maximum(d * min(sy, sz) * .9, np.maximum(x - xs[-1], xs[0] - x))
    def hq(p):  # into the head's frame (unit skull)
        return (p - V(hx, hy, 0)) / hs
    skull = lambda p: lathe(hq(p), sk, (0, .12, 0), .74, 1.1) * hs
    M.add('skull', skull, SHELL, .06)
    ga = D['gape']; c_, s_ = np.cos(ga), np.sin(ga)
    def jq(p):  # the jaw's frame: rotate back up by the gape round its hinge
        q = hq(p) - V(-.05, -.16, 0); x = q[..., 0] * c_ - q[..., 1] * s_; y = q[..., 0] * s_ + q[..., 1] * c_
        return np.stack([x, y, q[..., 2]], -1)
    jaw = lambda p: lathe(jq(p), [(-.05, .02), (.15, .3), (.6, .3), (1.05, .16), (1.3, .03)], (0, 0, 0), .5, 1.05) * hs
    M.add('jaw', jaw, SHELL, .04)
    M.add('throat', lambda p: ell(hq(p), (.15, -.05, 0), (.45, .16, .3)) * hs, GLOW)
    for s in (1, -1):
        M.add(f'eye{s}', lambda p, s=s: ell(hq(p), (.62, .3, s * .33), (.12, .06, .06)) * hs, GLOW)
        for i in range(6):  # fangs, upper and lower
            u = i / 5; xu = .2 + 1.05 * u; zu = s * (.36 * (1 - u * .75) + .02)
            Lf = (.42 - .18 * u) * (1.2 if i == 1 else 1)
            a = (hx + xu * hs, hy + .02 * hs, zu * hs); spk(M, f'fu{s}{i}', a, norm((.15, -1, -s * .1)), Lf * hs * .75, .06 * hs, FANG)
            jx, jy = .15 + .95 * u, .05; X = jx * c_ + jy * s_; Y = -jx * s_ + jy * c_  # back into the open jaw
            b = (hx + (X - .05) * hs, hy + (Y - .16) * hs, s * (.3 * (1 - u * .7)) * hs); spk(M, f'fl{s}{i}', b, norm((s_ * .4, c_, -s * .1)), Lf * hs * .6, .055 * hs, FANG)
        for j in range(3):  # cables over the crown, swept back into the hull
            a = (hx + (1.0 - j * .25) * hs, hy + (.35 + .05 * j) * hs, s * (.15 + .1 * j) * hs)
            cable(M, f'cr{s}{j}', bez3(a, (hx + .3 * hs, hy + .55 * hs, s * .3 * hs), (hx - .4 * hs, hy + .5 * hs, s * .35 * hs), (x1 - .6, yc(x1 - .6) + .45, s * .3), 7), .09, .07, CAB)
    # ------------------------------------------------ the classes
    if D.get('sac'):  # the Harvester: a great glowing biomass sac cradled in cables, grasping tendrils trailing back beneath it
        c0 = (-.4, .45, 0); M.add('sac', lambda p: ell(p, c0, (1.55, 1.25, 1.25)), M_((.03, .07, .1), .1, .3, (.05, .22, .3)), .1)
        for i in range(14):
            a = i / 14 * 2 * np.pi; cable(M, f'cd{i}', bez3((1.3, .7, 0), (.6, .45 + np.sin(a) * 1.45, np.cos(a) * 1.45), (-1.4, .45 + np.sin(a) * 1.4, np.cos(a) * 1.4), (-2.2, .6 + np.sin(a) * .3, np.cos(a) * .3), 8), .11, .08, CAB)
        for i in range(8):
            z = rng.uniform(-.8, .8); a = (rng.uniform(-1.2, .6), -.5, z); Lg = rng.uniform(1.6, 2.6)
            pts = bez3(a, (a[0] - Lg * .3, -.9, z * 1.2), (a[0] - Lg * .7, -.8, z * 1.4), (a[0] - Lg, -.5, z * 1.5), 7); cable(M, f'gr{i}', pts, .08, .02, CAB)
            spk(M, f'gk{i}', pts[-1], (-1, .3, 0), .3, .05, FANG)
    if D.get('armour'):  # the Guardian: overlapping carapace plates down its back with cyan seams, and two great crushing pincers at the prow
        for i in range(6):
            x = (1.3 - i * .7) * L; top = yc(x) + rad(x) * .72
            M.add(f'ap{i}', lambda p, c=(x, top + .02, 0): np.maximum(ell(p, c, (.7 * L, .32, rad(x) * 1.25 + .15)), -(p[..., 1] - c[1] + .12)), SHELL, .03)
            M.carve(f'as{i}', lambda p, x=x: np.maximum(np.abs(p[..., 0] - x + .55 * L) - .03, -(p[..., 1] - yc(x))), GLOW)
        for s in (1, -1):
            sh = (.9 * L, .5, s * .6); el = (1.9 * L, .25, s * 1.25); wr = (2.6 * L, .2, s * .95)
            cable(M, f'arm{s}', [sh, el, wr], .28, .2, SHELL)
            for u in (1, -1): spk(M, f'pz{s}{u}', wr, norm((1, .35 * u, -s * .35)), 1.1, .14, FANG)
    if D.get('plates'):  # the Assimilator: torn starship plating fused into its hull, running lights still lit
        for i in range(8):
            x = (-1.9 + i * .52) * L; top = yc(x) + rad(x) * .6; R = rot('y', rng.uniform(0, 3)) @ rot('x', rng.uniform(-.5, .5))
            c = (x, top + rng.uniform(0, .25), rng.uniform(-.5, .5)); M.add(f'pl{i}', lambda p, c=c, R=R, w=rng.uniform(.25, .45): box(p, c, (w, .04, w * .7), .01, R), PLATE)
            M.add(f'pll{i}', lambda p, c=c: sphere(p, (c[0], c[1] + .06, c[2]), .05), PLL)
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
    return (-2.75 * L - 4.5 - (D['tail'] > 10) * 1.6, -2.4, -4.2 - (1 if D.get('omega') else 0)), (1.85 * L + 3.2 + (4.5 * L + 1 if D.get('omega') else 0), 4.6 + D['hump'] + (1.5 if D.get('alpha') else 0) + (1.5 if D.get('omega') else 0), 4.2 + (1 if D.get('omega') else 0))
def paint(P, N, A, E, idx):
    glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05; top = np.clip(N[:, 1], 0, 1); A[~glowing, :3] *= (1 + .4 * top[~glowing])[:, None]
if __name__ == '__main__':
    k = sys.argv[1]; lo, hi = bounds(k); M = Model(lo, hi, float(sys.argv[3]) if len(sys.argv) > 3 else .04); mimic(M, k); M.bake(sys.argv[2], paint)
