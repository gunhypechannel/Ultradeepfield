# v855 the Carcinid bosses remastered after their paintings (docs/art/carcinid/<boss>.webp): python3 crc_boss.py <key> <outdir> [voxel]
# writes <outdir>/<key> and the glow layer <outdir>/<key>_g. Owner: "they look very smooth and soft and unrealistic ... more visually
# entertaining and colorful ... more glows and elemental water effects", then "build it all".
# The v751 crab was rounded everywhere (ellipsoid plates, sausage legs, smooth claws) and dull (no glow layer, a muted tint). This one is
# hard-edged: a faceted carapace under angular armour plates with light burning in every seam, sickle claws with serrated, glowing inner
# edges, thin bladed legs on glowing joints, a dark face with four burning eyes, mandibles and whip antennae, and each boss's own
# signature from its painting. Same frame as the game's crab wave: +x forward, claws past x 1.3, legs out beyond |z| .95, y up.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from crc_lib import *
from crc_crab import CRAB

def M_(c, r, m, e=None):
    d = {'c': c, 'r': r, 'm': m}
    if e is not None: d['e'] = e
    return d
# shell (between plates), plate, edge/rim, glow (emissive), accent (claw tips, teeth)
BT = {
    'cmar': ((.05, .008, .006), (.62, .05, .03), (.95, .5, .14), (2.2, .75, .12), (.98, .82, .55)),
    'cmat': ((.1, .12, .14), (.82, .84, .88), (.62, .9, .92), (.25, 1.9, 1.7), (.95, .96, 1.0)),
    'ctyr': ((.015, .02, .03), (.1, .13, .17), (.55, .62, .7), (.2, 1.6, 2.1), (.75, .85, .95)),
    'cora': ((.04, .01, .07), (.36, .1, .55), (.82, .55, 1.0), (1.4, .35, 2.2), (.95, .85, 1.0)),
    'ckor': ((.02, .015, .01), (.12, .09, .05), (.92, .66, .24), (.25, 1.5, 2.2), (.98, .78, .35)),
    'cbeh': ((.03, .025, .02), (.42, .27, .1), (.95, .7, .3), (.2, 1.8, 1.6), (.98, .85, .5)),
    'ckbr': ((.04, .008, .05), (.34, .06, .32), (.9, .5, .6), (1.8, .3, 2.1), (.98, .8, .7)),
    'cpal': ((.1, .14, .17), (.78, .9, .95), (.85, .97, 1.0), (.3, 1.7, 2.2), (.95, 1.0, 1.0)),
    'ccrown': ((.03, .02, .01), (.5, .34, .08), (1.0, .78, .3), (.25, 1.7, 2.0), (1.0, .88, .5)),
    'ccrownm': ((.08, .1, .12), (.6, .7, .76), (.8, .92, .98), (.3, 1.6, 2.0), (.95, 1.0, 1.0)),
    # v859 the wave crabs, after their paintings (docs/art/carcinid/drone, spitter, harvester ...): bronze and copper armour, cyan light
    'cscut': ((.03, .025, .03), (.3, .17, .08), (.85, .6, .3), (.15, 1.6, 1.8), (.95, .8, .5)),
    'cspit': ((.04, .02, .05), (.32, .14, .18), (.85, .55, .35), (.2, 1.5, 1.8), (.95, .8, .6)),
    'charv': ((.03, .03, .04), (.25, .2, .12), (.85, .65, .3), (.2, 1.7, 1.6), (.95, .85, .5)),
    'cguard': ((.02, .025, .04), (.12, .14, .2), (.7, .6, .45), (.15, 1.4, 2.0), (.9, .85, .7)),
    'cbrood': ((.05, .01, .05), (.45, .12, .4), (.9, .55, .7), (1.6, .35, 1.9), (.98, .8, .9)),
    'cwar': ((.04, .02, .02), (.38, .16, .08), (.9, .55, .25), (.2, 1.5, 1.7), (.95, .75, .45)),
    'ccrys': ((.03, .03, .05), (.3, .22, .16), (.85, .7, .45), (.25, 1.8, 2.1), (.9, .95, 1.0)),
    'clanc': ((.04, .02, .03), (.4, .2, .12), (.9, .6, .3), (.9, 1.6, .4), (.95, .8, .5)),
    'cmolt': ((.05, .02, .05), (.4, .15, .35), (.9, .6, .5), (1.7, .6, .9), (.98, .85, .8)),
}
def bmats(k, t):
    sh, pl, rim, gl, ac = BT[k]; gl = tuple(x * .5 for x in gl); C = mats(t)
    C.update(SHELL=M_(sh, .3, .5), PLATE=M_(pl, .22, .75), RIM=M_(rim, .2, .95), TIP=M_(ac, .15, .9), GLOW=M_(tuple(x * .08 for x in gl), .2, .1, gl),
             HOT=M_(tuple(min(1, x * .3) for x in gl), .2, .1, tuple(x * 1.6 for x in gl)), FACE=M_((.01, .01, .012), .35, .4))
    return C

def lath(p, a, b, r0, r1, flat, up):
    # a bladed leg/arm segment: a tapered cone flattened across 'up', so it has edges instead of a round section
    u = np.array(norm(up), np.float32); A = np.array(a, np.float32); q = p - A; k = (q @ u)[..., None]; q2 = q + u * k * (flat - 1)
    return rcone(q2 + A, a, b, r0, r1)

def sickle(M, n, base, fwd, up, L, W, T, curl, mat, edge, teeth, tmat, G=None, gmat=None, side=1):
    # a crescent claw finger in the plane (fwd, up): it leaves base along fwd and curls toward -up*side; its outer edge is thick armour,
    # its inner edge a glowing seam set with serrated teeth. built as a chain of flattened blade segments along a curve.
    f = np.array(norm(fwd)); u = np.array(norm(up)); sd = np.cross(f, u); N = 9; pts = []; rads = []
    rads = [W * (1 - i / N) ** .8 + .012 for i in range(N + 1)]
    # recompute the arc properly: integrate the direction
    pts = [np.array(base, float)]; ang = 0
    for i in range(N):
        t = (i + .5) / N; ang = curl * t; d = f * np.cos(ang) - u * side * np.sin(ang); pts.append(pts[-1] + d * L / N)
    for i in range(N):
        a, b = tuple(pts[i]), tuple(pts[i + 1])
        M.add(f'{n}{i}', lambda p, a=a, b=b, r0=rads[i], r1=rads[i + 1]: lath(p, a, b, r0, r1, 2.6, sd), mat, .025)
        if edge is not None and i < N - 1:  # the glowing inner edge: a thin seam just inside the curve
            ia = tuple(np.array(a) - u * side * rads[i] * .62); ib = tuple(np.array(b) - u * side * rads[i + 1] * .62)
            M.add(f'{n}e{i}', lambda p, a=ia, b=ib, r0=rads[i] * .22, r1=rads[i + 1] * .22: lath(p, a, b, r0 + .008, r1 + .008, 3.2, sd), edge)
            if G is not None: G.add(f'{n}g{i}', lambda p, a=ia, b=ib, r0=rads[i] * .5 + .03: cap(p, a, b, r0), gmat)
    for j in range(teeth):  # serrated teeth along the inner edge, raking back toward the hand
        i = 1 + int(j * (N - 2) / max(1, teeth)); c = pts[i]; tg = norm(tuple(pts[i + 1] - pts[i]))
        dn = np.array(norm(tuple(-u * side * 1.0 - np.array(tg) * .35))); r = rads[i]
        tb = tuple(c - u * side * r * .55); tt = tuple(c - u * side * r * .55 + dn * (r * .9 + .05))
        M.add(f'{n}t{j}', lambda p, a=tb, b=tt, rr=r * .32 + .012: lath(p, a, b, rr, rr * .05, 2.2, sd), tmat)
    M.add(f'{n}x', lambda p, a=tuple(pts[-2]), b=tuple(pts[-1] + (pts[-1] - pts[-2]) * .9): lath(p, a, b, rads[-2] * .9, .004, 2.4, sd), tmat)
    return pts, rads

def claw(M, G, n, c, fwd, kk, C, GL, GG, s):
    # a great crescent pincer in the plane (fwd, up): an armoured hand swelling into two hooked fingers round a round gap, the gap's
    # edge a glowing seam set with serrated teeth; thick along the back, thinning to an edge at the mouth (a lens cross-section)
    f = np.array(norm(fwd), np.float32); u = np.array((0, 1, 0), np.float32); u = u - f * (u @ f); u /= np.linalg.norm(u); z = np.cross(f, u)
    R = np.stack([f, u, z], 1).astype(np.float32); O = np.array(c, np.float32)
    A, B, T = 1.3 * kk, .55 * kk, .3 * kk; gx, gr = 1.35 * kk, .36 * kk
    def loc(p): return (p - O) @ R
    def e2(x, y, cx, cy, rx, ry):
        qx, qy = (x - cx) / rx, (y - cy) / ry; k0 = np.sqrt(qx * qx + qy * qy); return (k0 - 1) * min(rx, ry)
    def d2(x, y):
        outer = np.minimum(e2(x, y, .75 * kk, 0, A, B), e2(x, y, .05 * kk, 0, .55 * kk, .42 * kk))
        gap = np.sqrt((x - gx) ** 2 + y * y) - gr
        mouth = np.where(x > gx, .32 * (x - gx) - np.abs(y), -1)  # the mouth opens forward between the fingertips
        return np.maximum(np.maximum(outer, -gap), mouth * .9)
    def body(p):
        q = loc(p); x, y, zz = q[..., 0], q[..., 1], q[..., 2]; d = d2(x, y); depth = np.clip(-d / (.3 * kk), 0, 1)
        return np.maximum(d, np.abs(zz) - T * (.28 + .72 * np.sqrt(depth)))
    M.add(n, body, C['PLATE'], .03)
    def seam(p):  # the gap's lit edge
        q = loc(p); x, y, zz = q[..., 0], q[..., 1], q[..., 2]; g = np.sqrt((x - gx) ** 2 + y * y) - gr
        return np.maximum(np.maximum(np.abs(g) - .028, np.abs(zz) - T * .42), np.maximum(-(x - .7 * kk), d2(x, y) - .03))
    M.add(n + 'sm', seam, GL); G.add(n + 'gsm', lambda p: seam(p) - .08, GG)
    for j in range(9):  # serrated teeth round the gap, raking toward the hand
        a = np.radians(-150 + j * 300 / 8)
        if abs(a) < np.radians(35): continue
        bp = np.array((gx + gr * np.cos(a), gr * np.sin(a), 0), np.float32); tp = bp + np.array((-np.cos(a) - .45, -np.sin(a), 0), np.float32) * (.13 * kk + .03 * (j % 2))
        M.add(f'{n}t{j}', lambda p, a=tuple(O + R @ bp), b=tuple(O + R @ tp): lath(p, a, b, .055 * kk, .004, 2.4, tuple(z)), C['TIP'])
    for sg in (1, -1):  # the fingertips hook toward each other
        tb = np.array((gx + gr * .55, sg * gr * 1.05, 0), np.float32); tt = np.array((gx + gr * 1.35, sg * gr * .25, 0), np.float32)
        M.add(f'{n}h{sg}', lambda p, a=tuple(O + R @ tb), b=tuple(O + R @ tt): lath(p, a, b, .12 * kk, .004, 2.2, tuple(z)), C['TIP'])
    for j in range(4):  # a ridge of spikes along the back of the hand, a row of small ones down the outer finger
        bp = np.array((.1 * kk + j * .3 * kk, B * .92 - .05 * j * kk, 0), np.float32); dd = np.array((.5, 1, 0), np.float32)
        blade(M, f'{n}k{j}', tuple(O + R @ bp), tuple(R @ (dd / np.linalg.norm(dd))), .3 * kk + .05 * j, .07 * kk, C['RIM'], flat=3, up=tuple(z))
    hcore = tuple(O + R @ np.array((.05 * kk, 0, T * .62 * s * 0 + T * .62), np.float32))
    M.add(n + 'c', lambda p: sphere(p, hcore, .1 * kk), C['HOT']); G.add(n + 'gc', lambda p: sphere(p, hcore, .3 * kk), GG)
    hcore2 = tuple(O + R @ np.array((.05 * kk, 0, -T * .62), np.float32))
    M.add(n + 'c2', lambda p: sphere(p, hcore2, .1 * kk), C['HOT']); G.add(n + 'gc2', lambda p: sphere(p, hcore2, .3 * kk), GG)

def boss(M, G, P, k):
    C = bmats(k, P.get('t')); w, l, h, kk, th = P['w'], P['l'], P['h'], P['kk'], P['th']; yb = .1
    GL = C['GLOW']; GG = M_((0, 0, 0), .2, 0, tuple(x * .12 for x in BT[k][3]))
    # the carapace: a broad armoured dome over a dark core lit from within; the dome is cracked into plates (Voronoi cells over its
    # surface) and light burns in every crack; each plate's rear edge lifts a little, and a keel of blades runs down the middle
    top = yb + h * 1.08; SC = (-.05, yb + h * .15, 0); SR = (l * 1.08, top - yb - h * .15, w * 1.06)
    def dome(x, z): return SC[1] + SR[1] * np.sqrt(max(0., 1 - ((x - SC[0]) / SR[0]) ** 2 - (z / SR[2]) ** 2))
    M.add('core', lambda p: ell(p, (0, yb - h * .05, 0), (l * .95, h * .5, w * .85)), C['SHELL'], .05)
    M.add('belly', lambda p: ell(p, (0, yb - h * .2, 0), (l * .8, h * .3, w * .75)), GL, .04)
    shell = lambda p: np.maximum(ell(p, SC, SR), yb - h * .05 - p[..., 1])
    M.add('shell', shell, C['PLATE'], .04)
    rng = np.random.default_rng(len(k) * 7 + int(w * 100)); pts = []
    nC = 26 + 6 * P.get('rows', 4)
    while len(pts) < nC:
        x = rng.uniform(-1, 1); z = rng.uniform(-1, 1)
        if x * x + z * z <= .98: pts.append((SC[0] + x * SR[0] * .98, z * SR[2] * .98))
    pts = np.array(pts, np.float32)
    def cells(p):  # half the gap between the nearest two cell centres, measured over the dome's plan
        q = p[..., [0, 2]]; d = np.sqrt(((q[..., None, :] - pts) ** 2).sum(-1)); d.sort(-1); return (d[..., 1] - d[..., 0]) * .5
    CRK.update(pl=C['PLATE'], cells=cells, shell=len(M.parts) - 1, glow=tuple(x * .28 for x in BT[k][3]), gcol=tuple(x * .08 for x in BT[k][3]))  # the cracks are painted (bpaint)
    # the rim: long blades all round the shield's edge, the front corners curling forward like horns
    nr = P.get('rim', 16)
    for j in range(nr):
        a = (j + .5) / nr * 2 * np.pi; cxx, czz = np.cos(a), np.sin(a)
        if cxx > .8: continue
        base = (cxx * l * .98, yb + h * .3, czz * w * .98); L = (.38 + .42 * max(0, cxx + .2)) * P.get('sp', 1)
        blade(M, f'rim{j}', base, norm((cxx * .9 + .25, .3, czz)), L * 1.5 + .3, .22, C['RIM'], flat=3.6)
    nsp = max(4, P.get('spikes', 0) // 2 + 2)
    for j in range(nsp):  # dorsal spines, tall and raked back
        u2 = j / max(1, nsp - 1); s = 1 if j % 2 else -1; x = l * (.55 - u2 * 1.2); z = s * w * (.18 + .22 * ((j // 2) % 2))
        blade(M, f'dsp{j}', (x, dome(x, z) + .02, z), norm((-.45, 1, s * .2)), .6 + .45 * (1 - u2) * P.get('sp', 1), .13, C['RIM'], flat=3.2, up=(0, 0, 1))
    M.carve('spine', lambda p: np.maximum(box(p, (0, top + .03, 0), (l * .9, .05, .028)), -box(p, (0, 0, 0), (9, 9, 9))), GL)
    # the face: a dark recessed face plate, a heavy brow of blades, four burning eyes, mandibles and fangs, whip antennae
    fx0 = l * .98
    M.add('face', lambda p: hull(p, [(fx0 + .22, 0), (fx0 + .12, w * .42), (fx0 - .25, w * .5), (fx0 - .25, 0)], yb + h * .38, yb - h * .3, .12, .02), C['FACE'])
    for s in (1, -1):
        blade(M, f'brow{s}', (fx0 - .1, yb + h * .45, s * w * .12), norm((1, .35, s * .9)), w * .55 + .2, .12, C['RIM'], flat=3.2)
        for e, (ez, ey, er) in enumerate(((.2, .2, .1), (.36, .1, .065))):
            ec = (fx0 + .16 - e * .05, yb + h * ey, s * w * ez)
            M.add(f'sock{s}{e}', lambda p, c=ec, r=er: sphere(p, c, r * 1.5), C['FACE'])
            M.add(f'eye{s}{e}', lambda p, c=(ec[0] + er * .5, ec[1], ec[2]), r=er: sphere(p, c, r), C['HOT'])
            G.add(f'geye{s}{e}', lambda p, c=(ec[0] + er * .5, ec[1], ec[2]), r=er: sphere(p, c, r * 3.2), GG)
        for j in range(max(2, P.get('fg', 6) // 2)):  # fangs and mandibles hanging under the face
            base = (fx0 + .12, yb - h * .2, s * (.07 + .075 * j)); blade(M, f'fang{s}{j}', base, norm((.45, -1, s * .1)), .28 + .06 * (j % 2), .045, C['TIP'], flat=2.4, up=(0, 0, 1))
        blade(M, f'mand{s}', (fx0 + .1, yb - h * .1, s * w * .3), norm((1, -.35, -s * .55)), .5 + .15 * kk, .08, C['RIM'], flat=2.8, up=(0, 1, 0))
        curved(M, f'ant{s}', (fx0 + .15, yb + h * .32, s * .1), (fx0 + 1.4, yb + h * 2.2, s * .6), (fx0 - .2, yb + h * 3.2, s * 1.6), .03, .006, C['RIM'], 10)
        for hn in range(P.get('hn', 0)):  # horns over the brow
            base = (fx0 - .2 - .14 * hn, yb + h * .62, s * w * (.32 + .13 * hn)); blade(M, f'horn{s}{hn}', base, norm((.75, .75 - .1 * hn, s * .35)), .55 + .12 * hn, .085, C['RIM'], flat=2.6)
    # the claws: a bladed two-segment arm on a glowing elbow, a faceted hand with a ridge of spikes, two sickle fingers
    for s in (1, -1):
        sh = (l * .62, yb - .02, s * w * .62); el = (l * .98, yb + .2 * kk, s * (w * .92 + .3 * kk)); wr = (l * 1.15 + .25 * kk, yb + .05, s * (w * .78 + .12))
        M.add(f'ar1{s}', lambda p, a=sh, b=el: lath(p, a, b, .2 * th, .17 * th * kk ** .4, 1.8, (0, 0, 1)), C['PLATE'], .03)
        M.add(f'ar2{s}', lambda p, a=el, b=wr: lath(p, a, b, .19 * th * kk ** .4, .16 * th * kk ** .4, 1.8, (0, 0, 1)), C['PLATE'], .03)
        M.add(f'elb{s}', lambda p, c=el: sphere(p, c, .13 * th * kk ** .4), C['HOT']); G.add(f'gelb{s}', lambda p, c=el: sphere(p, c, .3 * th * kk ** .4), GG)
        blade(M, f'elbs{s}', el, norm((-.3, 1, s * .4)), .45 * kk, .08 * kk, C['RIM'], flat=3)
        hc = (wr[0] + .1 * kk, yb + .05, s * w * .74); claw(M, G, f'cl{s}', hc, (1, .08, -s * .14), kk, C, GL, GG, s)
    # the legs: three pairs of thin bladed segments, a high knee, glowing joints, long hooked points
    for s in (1, -1):
        for i in range(P.get('legs', 3)):
            u = i / max(1, P.get('legs', 3) - 1); x0 = l * (.35 - .95 * u); spr = 1.05 + .25 * (1 - abs(u - .5) * 2)
            a = (x0, yb - .02, s * w * .72); kn = (x0 - .1 + .15 * (1 - u), yb + h * .65 + .45, s * (w + .8 * spr)); an = (x0 - .25 + .45 * (1 - u), yb - .2, s * (w + 1.4 * spr)); ft = (x0 - .3 + .6 * (1 - u), -.9, s * (w + 1.65 * spr))
            M.add(f'lg1{s}{i}', lambda p, a=a, b=kn: lath(p, a, b, .19 * th, .13 * th, 2.2, (-1, 0, 0)), C['PLATE'], .02)
            M.add(f'lg2{s}{i}', lambda p, a=kn, b=an: lath(p, a, b, .14 * th, .09 * th, 2.2, (-1, 0, 0)), C['PLATE'], .02)
            M.add(f'lg3{s}{i}', lambda p, a=an, b=ft: lath(p, a, b, .09 * th, .004, 2.4, (-1, 0, 0)), C['TIP'], .01)
            for q, r0 in ((kn, .1), (an, .075)):
                M.add(f'lj{s}{i}{q[0]:.2f}', lambda p, q=q, r0=r0: sphere(p, q, r0 * th), C['HOT'])
                G.add(f'glj{s}{i}{q[0]:.2f}', lambda p, q=q, r0=r0: sphere(p, q, r0 * th * 2.4), GG)
            blade(M, f'lk{s}{i}', kn, norm((-.25, 1, s * .3)), .48 * th, .08 * th, C['RIM'], flat=3.2)
            mid = lerp(a, kn, .5); blade(M, f'ls{s}{i}', (mid[0], mid[1] + .05, mid[2]), norm((-.2, 1, s * .5)), .26, .05 * th, C['RIM'], flat=3)
            mid = lerp(kn, an, .45); blade(M, f'ls2{s}{i}', mid, norm((-.4, .3, s)), .22, .045 * th, C['RIM'], flat=3)
    # a heart of light under the shell (the glow layer carries it through the seams)
    G.add('gcore', lambda p: ell(p, (0, yb + h * .35, 0), (l * .7, h * .5, w * .6)), M_((0, 0, 0), .2, 0, tuple(x * .04 for x in BT[k][3])))
    sig(M, G, P, C, k, yb, top, dome, GG)
    extras(M, P, C, yb)
    return C

def sig(M, G, P, C, k, yb, top, dome, GG):
    # each boss's own mark, from its painting
    w, l, h, kk = P['w'], P['l'], P['h'], P['kk']; GL = C['GLOW']
    if k == 'cmar':  # the Red Claw Marshal: a ringed eye-sigil on the brow plate and a crest of great swept blades
        M.add('sig', lambda p: torus(p, (l * .45, dome(l * .45, 0) + .06, 0), 'y', .22, .03), C['RIM']); M.add('sigc', lambda p: sphere(p, (l * .45, dome(l * .45, 0) + .06, 0), .1), C['HOT'])
        G.add('gsig', lambda p: sphere(p, (l * .45, dome(l * .45, 0) + .08, 0), .35), GG)
        for j in range(5): blade(M, f'cr{j}', (l * (.2 - .3 * j), dome(l * (.2 - .3 * j), 0), 0), norm((-.7, 1, 0)), .9 - .1 * j, .12, C['RIM'], flat=3.5, up=(0, 0, 1))
    if k == 'cmat':  # the Pearl Matron: glowing teal sacs along her back between nacre plates, a ring of pearls
        for j in range(4):
            for s in (1, -1):
                c = (l * (.3 - .45 * j), dome(l * (.3 - .45 * j), s * w * .45) + .02, s * w * .45)
                M.add(f'sac{j}{s}', lambda p, c=c: ell(p, c, (.2, .14, .16)), C['HOT']); G.add(f'gsac{j}{s}', lambda p, c=c: sphere(p, c, .35), GG)
    if k == 'ctyr':  # the Reef Tyrant: a crown spire on its back and a halo ring of light behind it
        M.add('spire', lambda p: spike(p, (-l * .1, top - .1, 0), (-l * .1, top + 1.5, 0), .18), C['RIM'])
        for j in range(6):
            a = j / 6 * 2 * np.pi; blade(M, f'sp{j}', (-l * .1 + .25 * np.cos(a), top, .25 * np.sin(a)), norm((np.cos(a) * .5, 1, np.sin(a) * .5)), .7, .08, C['RIM'], flat=3)
        M.add('halo', lambda p: torus(p, (-l * .6, top + .2, 0), 'x', w * .95, .035), GL); G.add('ghalo', lambda p: torus(p, (-l * .6, top + .2, 0), 'x', w * .95, .12), GG)
    if k == 'cora':  # the Trench Oracle: a crown of curved blades round a glowing third eye
        for j in range(7):
            a = (j - 3) * .32; blade(M, f'oc{j}', (l * .3, top - .05, np.sin(a) * w * .5), norm((np.sin(a) * .2 - .2, 1, np.sin(a))), .8 + .3 * (j % 2), .09, C['RIM'], flat=3.2)
        G.add('geye3', lambda p: sphere(p, (0, top + .75, 0), .6), GG)
    if k == 'ckor':  # Dread Admiral Korvax: a heart of cyan light in his chest plate, a gold war-crown, armoured pauldrons
        c = (l * 1.05, yb - h * .05, 0); M.add('heart', lambda p: sphere(p, c, .16), C['HOT']); M.add('heartr', lambda p: torus(p, c, 'x', .22, .035), C['RIM'])
        G.add('gheart', lambda p: sphere(p, c, .55), GG)
        for s in (1, -1): M.add(f'paul{s}', lambda p, s=s: hull(p, [(.5, 0), (.3, .35), (-.4, .3), (-.5, 0)], yb + h * .75, yb + h * .35, .15, .02, (l * .55, 0, s * w * .75)), C['RIM'])
    if k == 'cbeh':  # the Trench Behemoth: lit windows in the city on its back
        for j in range(8):
            rng = np.random.default_rng(j + 7); x = rng.uniform(-l * .5, l * .3); z = rng.uniform(-w * .45, w * .45)
            G.add(f'gcity{j}', lambda p, c=(x, top + .5, z): sphere(p, c, .22), GG)
    if k == 'ckbr':  # the Krakenbreaker: the grafted arms end in glowing hooks
        for j in range(P.get('tent', 0)):
            s = 1 if j % 2 else -1; u = (j // 2) / max(1, P['tent'] // 2 - 1); e = (-l * (1.6 + .6 * u), yb + h * (.6 + .8 * u), s * (w + 1.3))
            M.add(f'thk{j}', lambda p, c=e: sphere(p, c, .07), C['HOT']); G.add(f'gthk{j}', lambda p, c=e: sphere(p, c, .2), GG)
    if k == 'cpal':  # the Pale Sovereign: crystals of light grow out of its shell
        for j in range(8):
            rng = np.random.default_rng(j + 31); x = rng.uniform(-l * .6, l * .4); z = rng.uniform(-w * .6, w * .6); d = norm((rng.uniform(-.4, .4), 1, rng.uniform(-.4, .4)))
            G.add(f'gcr{j}', lambda p, c=(x, dome(x, z) + .3, z): sphere(p, c, .28), GG)
    if k in ('ccrown', 'ccrownm'):  # the Abyssal Crown: a ring of great blades and a burning jewel over its back
        c = (l * .05, top + .45, 0); M.add('jewel', lambda p: sphere(p, c, .2), C['HOT']); G.add('gjewel', lambda p: sphere(p, c, .7), GG)
        for j in range(8):
            a = j / 8 * 2 * np.pi; blade(M, f'cb{j}', (l * .05 + .45 * np.cos(a), top, .45 * np.sin(a)), norm((np.cos(a) * .35, 1, np.sin(a) * .35)), .8 + .3 * (j % 2), .1, C['RIM'], flat=3)

CRK = {}
def worley(P, sc):
    # half the gap between the nearest two jittered points of a grid of cells (size sc): zero along the cracks between armour plates
    g = np.floor(P / sc).astype(np.int64); f1 = np.full(len(P), 9.0, np.float32); f2 = np.full(len(P), 9.0, np.float32)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c = g + np.array((dx, dy, dz)); j = np.stack([hashf(c[:, 0] + 17 * a, c[:, 1] + 5 * a, c[:, 2] + 3 * a) for a in range(3)], 1)
                q = (c + .15 + .7 * j) * sc; d = np.sqrt(((P - q) ** 2).sum(1)); n1 = np.minimum(f1, d); f2 = np.minimum(f2, np.maximum(f1, d)); f1 = n1
    return (f2 - f1) * .5
def bpaint(P, N, A, E, idx):
    if CRK.get('plates') is not None:  # the claws and legs are cracked into plates too
        m = np.where(np.isin(idx, CRK['plates']))[0]; cv = worley(P[m], .68); g = cv < .011; dk = (cv >= .011) & (cv < .04)
        E[m[g], :3] = CRK['glow']; A[m[g], :3] = CRK['gcol']; A[m[dk], :3] *= (.4 + .6 * (cv[dk] - .011) / .029)[:, None]
    if CRK:  # light burning in the cracks between the plates, the plate edges darkened on either side
        m = np.where(idx == CRK['shell'])[0]; cv = CRK['cells'](P[m]); g = cv < .018; dk = (cv >= .018) & (cv < .055)
        E[m[g], :3] = CRK['glow']; A[m[g], :3] = CRK['gcol']; A[m[dk], :3] *= (.35 + .65 * (cv[dk] - .018) / .037)[:, None]
    v = .5 * panels(P, .3, .25, .25) + .5 * hashf(idx.astype(np.int64), idx.astype(np.int64) * 7 + 1, 3); glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05
    A[~glowing, :3] *= (.7 + .6 * v[~glowing])[:, None]
    top = np.clip(N[:, 1], 0, 1); bot = np.clip(-N[:, 1], 0, 1)
    A[:, :3] *= (1 + .3 * top - .45 * bot)[:, None]  # lit from above, dark underneath, like the paintings
    E[glowing, :3] *= (.8 + .4 * v[glowing])[:, None]

if __name__ == '__main__':
    k = sys.argv[1]; P = dict(CRAB[k]); P['k'] = k; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .03
    lo = (-P['l'] * (2.6 if P.get('abdo') or P.get('tent') else 1.7), -1.15, -(P['w'] + 2.5)); hi = (P['l'] * 1.3 + 2.9 * P['kk'] + .6, 4.6, P['w'] + 2.5)
    M = Model(lo, hi, vox); G = Model(lo, hi, vox * 2)
    boss(M, G, P, k); CRK['plates'] = [i for i, (n, f, m, kk) in enumerate(M.parts) if m is CRK['pl'] and i != CRK['shell']]; M.bake(sys.argv[2] + '/' + k, bpaint); G.bake(sys.argv[2] + '/' + k + '_g', None)
