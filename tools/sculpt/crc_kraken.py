# v863 the Kraken remastered (owner: "update and remaster the carcinid wild kraken, its very small and boring ... a menacing space boss
# with superior special effects and significant scale for the crab army to be able to control something like that", then "build it all").
# python3 crc_kraken.py <outdir> [voxel] -> <outdir>/ckrak and <outdir>/ckrak_g. Same frame as before (+x forward, the arms reaching
# forward past x .4, the mantle trailing to x -3.6) so the game's tentacle wave still fits: a great ribbed mantle spotted with light, two
# slit-pupilled eyes, a hooked beak in a ring of teeth, eight arms set with glowing suckers and hooks and two long feeding tentacles ending
# in hooked clubs; the Carcinid's harness on it: bolted chitin plates, coral-crusted straps, and a control spire on its head whose cyan
# neural spikes are driven into its flesh.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from crc_lib import *
def M_(c, r, m, e=None):
    d = {'c': c, 'r': r, 'm': m}
    if e is not None: d['e'] = e
    return d
SKIN = M_((.05, .012, .07), .22, .35); SKIN2 = M_((.11, .025, .13), .2, .4); BELLY = M_((.2, .07, .16), .3, .25)
SPOT = M_((.12, .03, .16), .2, .1, (.32, .09, .48)); CYAN = M_((.02, .15, .18), .2, .1, (.1, 1.3, 1.5)); EYE = M_((.3, .08, .02), .1, .1, (1.0, .32, .04))
PUPIL = M_((.005, .005, .005), .2, .2); CHIT = M_((.09, .05, .03), .22, .85); RIM = M_((.85, .6, .25), .2, .95); CORAL = M_((.6, .07, .06), .7, .05, (.1, 0, 0))
HOOK = M_((.9, .85, .7), .15, .9); TOOTH = M_((.92, .9, .82), .2, .3)
GG = M_((0, 0, 0), .2, 0, (.06, .02, .09)); GC = M_((0, 0, 0), .2, 0, (.015, .14, .17)); GE = M_((0, 0, 0), .2, 0, (.16, .07, .01))
vox = float(sys.argv[2]) if len(sys.argv) > 2 else .04
M = Model((-4.4, -2.4, -3.4), (6.8, 2.8, 3.4), vox); G = Model((-4.4, -2.4, -3.4), (6.8, 2.8, 3.4), vox * 2)
rng = np.random.default_rng(11)
def mantle(p):
    x = p[..., 0]; u = np.clip((.1 - x) / 4.0, 0, 1); rr = np.interp(u, [0, .05, .22, .45, .7, .9, 1], [.5, .9, 1.15, 1.1, .8, .35, .04])
    return np.maximum(np.sqrt((p[..., 1] - .05) ** 2 + (p[..., 2] / .92) ** 2) - rr, np.maximum(x - .2, -3.95 - x))
M.add('man', mantle, SKIN, .1)
M.add('head', lambda p: ell(p, (.25, .05, 0), (.95, .85, .9)), SKIN, .35)
M.add('bel', lambda p: np.maximum(ell(p, (-.8, -.4, 0), (1.9, .7, .85)), -p[..., 1] - .1 - 3), BELLY, .3)
for j in range(9):  # ribs ringing the mantle
    x = -.5 - .38 * j; M.add(f'rb{j}', lambda p, x=x: np.maximum(np.abs(mantle(p)) - .04, np.abs(p[..., 0] - x) - .06), SKIN2, .02)
for j in range(26):  # spots of light along the mantle
    x = rng.uniform(-3.4, -.2); a = rng.uniform(-2.2, 2.2); u = np.clip((.1 - x) / 4.0, 0, 1); rr = float(np.interp(u, [0, .05, .22, .45, .7, .9, 1], [.5, .9, 1.15, 1.1, .8, .35, .04]))
    c = (x, .05 + np.cos(a) * rr, np.sin(a) * rr * .92); M.add(f'sp{j}', lambda p, c=c: sphere(p, c, .07 + .03 * (j % 3)), SPOT); G.add(f'gsp{j}', lambda p, c=c: sphere(p, c, .2), GG)
for s in (1, -1):  # the fins at its tail
    M.add(f'fin{s}', lambda p, s=s: oell(p, (-3.2, .15, s * .55), np.array(((np.cos(.6), 0, -s * np.sin(.6)), (s * np.sin(.6), 0, np.cos(.6)), (0, 1, 0)), np.float32), (1.2, .75, .06)), SKIN2, .04)
    ec = (.55, .35, s * .78)  # a great slit-pupilled eye in a ring of armour
    M.add(f'ey{s}', lambda p, c=ec: sphere(p, c, .24), EYE); M.add(f'pu{s}', lambda p, c=ec, s=s: box(p, (c[0] + .02, c[1], c[2] + s * .2), (.035, .16, .06), .02), PUPIL)
    M.add(f'eyr{s}', lambda p, c=ec, s=s: torus(p, (c[0], c[1], c[2] + s * .04), 'z', .27, .05), CHIT); G.add(f'gey{s}', lambda p, c=ec: sphere(p, c, .55), GE)
    for k in range(3): blade(M, f'brw{s}{k}', (ec[0] - .1 + .12 * k, ec[1] + .25, ec[2] - s * .05), norm((.6, .7, s * .2)), .35, .07, RIM, flat=3)
M.add('beak', lambda p: spike(p, (.75, -.2, 0), (1.55, -.35, 0), .3), HOOK)
for j in range(10):  # a ring of teeth round the beak
    a = j / 10 * 2 * np.pi; c = (1.05, -.2 + np.sin(a) * .34, np.cos(a) * .34); M.add(f'tt{j}', lambda p, c=c, a=a: spike(p, c, (c[0] + .25, c[1] - np.sin(a) * .1, c[2] - np.cos(a) * .1), .05), TOOTH)
# the arms: eight, thick at the root, set with suckers of light and hooks; and two long feeding tentacles ending in hooked clubs
for i in range(10):
    feed = i >= 8; a = (i / 8 * 2 * np.pi) if not feed else (np.pi / 2 if i == 8 else -np.pi / 2); R0 = .55
    by, bz = np.sin(a) * R0 - .15, np.cos(a) * R0; pts = [(.7, by, bz)]; px, py, pz = .7, by, bz; n = 9 if feed else 7
    for j in range(1, n):
        px += (.62 if feed else .58) + rng.uniform(0, .12); py += np.sin(a) * .18 + np.sin(j * 1.3 + i) * .22; pz += np.cos(a) * .22 + np.cos(j * 1.1 + i) * .22; pts.append((px, py, pz))
    r0 = .22 if feed else .36; rads = [r0 * (1 - u * (.8 if feed else .9)) for u in np.linspace(0, 1, len(pts))]; chain(M, f'arm{i}', pts, rads, SKIN, .04)
    for j in range(1, len(pts) - 1):
        q = pts[j]; rr = rads[j]; sd = (-np.sin(a) * .8, -np.cos(a) * .8)
        M.add(f'su{i}{j}', lambda p, c=(q[0], q[1] + sd[0] * rr, q[2] + sd[1] * rr), r=rr * .3: sphere(p, c, r), SPOT)
        if j % 2 == 0: G.add(f'gsu{i}{j}', lambda p, c=(q[0], q[1] + sd[0] * rr, q[2] + sd[1] * rr), r=rr * .7: sphere(p, c, r), GG)
        if j % 2: spk(M, f'hk{i}{j}', (q[0], q[1] - sd[0] * rr * .9, q[2] - sd[1] * rr * .9), norm((-.4, -sd[0], -sd[1])), rr * 1.5 + .05, rr * .35, HOOK)
    if feed:  # the club: a broad pad of hooks
        c = pts[-1]; M.add(f'club{i}', lambda p, c=c: ell(p, c, (.5, .22, .3)), SKIN2, .08)
        for k in range(6): spk(M, f'ch{i}{k}', (c[0] - .3 + .12 * k, c[1] + (.15 if k % 2 else -.15), c[2]), norm((.3, 1 if k % 2 else -1, 0)), .3, .06, HOOK)
        G.add(f'gcl{i}', lambda p, c=c: sphere(p, c, .45), GG)
# the Carcinid's harness: bolted chitin plates on the mantle, coral-crusted straps round it, and the control spire on its head
for j in range(5):
    x = -.4 - .55 * j; u = np.clip((.1 - x) / 4.0, 0, 1); rr = float(np.interp(u, [0, .05, .22, .45, .7, .9, 1], [.5, .9, 1.15, 1.1, .8, .35, .04]))
    M.add(f'pl{j}', lambda p, x=x, rr=rr: np.maximum(np.maximum(np.abs(np.sqrt((p[..., 1] - .05) ** 2 + (p[..., 2] / .92) ** 2) - rr - .06) - .05, np.abs(p[..., 0] - x) - .22), .5 - (p[..., 1] - .05) / (rr + .1) * 1.0), CHIT, .02)
    for k in (-1, 1): M.add(f'bo{j}{k}', lambda p, x=x, rr=rr, k=k: sphere(p, (x, .05 + rr * .8, k * rr * .55), .06), RIM)
for j, x in enumerate((-1.0, -2.3)):  # straps
    u = np.clip((.1 - x) / 4.0, 0, 1); rr = float(np.interp(u, [0, .05, .22, .45, .7, .9, 1], [.5, .9, 1.15, 1.1, .8, .35, .04]))
    M.add(f'st{j}', lambda p, x=x, rr=rr: np.maximum(np.abs(np.sqrt((p[..., 1] - .05) ** 2 + (p[..., 2] / .92) ** 2) - rr - .04) - .05, np.abs(p[..., 0] - x) - .1), RIM)
    for k in range(5):
        a = rng.uniform(0, 2 * np.pi); base = (x, .05 + np.cos(a) * (rr + .08), np.sin(a) * (rr + .08)); d = norm((rng.uniform(-.3, .3), np.cos(a), np.sin(a)))
        M.add(f'cr{j}{k}', lambda p, a=base, b=tuple(np.array(base) + np.array(d) * .35): cap(p, a, b, .05), CORAL)
sp0 = (.0, .85, 0)  # the control spire
M.add('spb', lambda p: cyl(p, sp0, 'y', .5, .15, .04), CHIT); M.add('spt', lambda p: rcone(p, sp0, (-.15, 2.5, 0), .36, .07), CHIT, .03)
for k in range(6): blade(M, f'spf{k}', (-.05 - .02 * k, 1.15 + .22 * k, (k % 2 - .5) * .3), norm((-.6, .7, (k % 2 - .5) * 1.4)), .7 - .08 * k, .08, RIM, flat=3)
M.add('orb', lambda p: sphere(p, (-.15, 2.6, 0), .22), CYAN); G.add('gorb', lambda p: sphere(p, (-.15, 2.6, 0), .7), GC)
for k in range(6):  # its neural spikes, driven into the flesh
    a = k / 6 * 2 * np.pi; b0 = (sp0[0] + np.cos(a) * .3, sp0[1] - .05, np.sin(a) * .3); b1 = (sp0[0] + np.cos(a) * .75, sp0[1] - .6, np.sin(a) * .7)
    M.add(f'ns{k}', lambda p, a=b0, b=b1: rcone(p, a, b, .05, .015), CYAN); G.add(f'gns{k}', lambda p, a=b0, b=b1: cap(p, a, b, .1), GC)
def kpaint(P, N, A, E, idx):
    v = panels(P, .4, .35, .35); lit = E[:, :3].sum(1) > .05; A[~lit, :3] *= (.8 + .4 * v[~lit])[:, None]
    top = np.clip(N[:, 1], 0, 1); bot = np.clip(-N[:, 1], 0, 1); A[:, :3] *= (1 + .25 * top - .35 * bot)[:, None]
M.bake(sys.argv[1] + '/ckrak', kpaint); G.bake(sys.argv[1] + '/ckrak_g', None)
