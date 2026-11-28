# v866 the Abyssal Breach Nest remastered (owner: "can we remaster and revise the abyssal nests, it has no glow like the rest of the crabs and
# no special effects", then "build all of the rest"). python3 crc_nest.py <outdir> [voxel] -> <outdir>/cnest and <outdir>/cnest_g.
# Same frame as v756's (a rift standing on a mound, y up, the rift's face toward +z/-z) so the game's scale still fits: a mound of black
# basalt split by cracks of sea-light; a rift into the Abyss framed by a ring of bolted chitin with bronze edges and inward hooks, its
# face a whirlpool of teal light round a burning cyan eye; nine curved chitin spires closing round it, bronze-tipped, a cyan vein up each;
# clutches of glowing eggs in dark membranes at its foot; coral with lit tips.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, chain, spk, norm
from mon2_sculpt import bez3, taper
from mon3_sculpt import crag
from crc_boss import worley
def M_(c, r, m, e=None):
    d = {'c': c, 'r': r, 'm': m}
    if e is not None: d['e'] = e
    return d
ROCK = M_((.045, .045, .06), .85, .15); CHIT = M_((.05, .035, .07), .3, .7); PLATE = M_((.07, .045, .075), .28, .85); BRZ = M_((.78, .5, .2), .22, .95)
VEIN = M_((.02, .2, .22), .15, .1, (.06, .95, 1.0)); EYE = M_((.2, .9, 1.0), .1, .1, (.5, 1.6, 1.8)); VOID = M_((.004, .012, .025), .4, .2)
EGG = M_((.04, .25, .22), .12, .15, (.1, .75, .6)); MEMB = M_((.03, .02, .04), .5, .2); COR = M_((.55, .05, .05), .7, .05, (.08, 0, 0)); PUR = M_((.3, .06, .4), .7, .05, (.12, .02, .2))
CTIP = M_((.9, .4, .5), .3, .05, (.9, .25, .45)); PTIP = M_((.7, .4, 1.0), .3, .05, (.55, .25, .95))
GT = M_((0, 0, 0), .2, 0, (.02, .16, .17)); GE = M_((0, 0, 0), .2, 0, (.02, .11, .09)); GP = M_((0, 0, 0), .2, 0, (.1, .03, .06))
vox = float(sys.argv[2]) if len(sys.argv) > 2 else .03
M = Model((-3.5, -2.6, -3.2), (3.5, 4.2, 3.2), vox); G = Model((-3.5, -2.6, -3.2), (3.5, 4.2, 3.2), vox * 2)
rng = np.random.default_rng(77)
M.add('mound', lambda p: crag(p, (0, -1.55, 0), (3.0, .96, 2.55), 5, .3, 1.2), ROCK)
for i in range(11): M.add(f'bo{i}', lambda p, c=(np.cos(i * 2.3) * (1.6 + i % 3 * .45), -1.05, np.sin(i * 2.3) * (1.4 + i % 3 * .35)), r0=.32 + (i % 3) * .12: sphere(p, c, r0) + noise3(p, 6, i) * .09, ROCK)
RC = (0, 1.15, 0)  # the rift's centre; its ring an upright ellipse in the xy plane
ring = lambda p, R, w: torus((p - V(*RC)) / V(1, 1.32, 1), (0, 0, 0), 'z', R, w) * .82
M.add('ring', lambda p: ring(p, 1.16, .2), CHIT, .04)
M.add('rimF', lambda p: np.maximum(ring(p, 1.16, .23), -np.abs(p[..., 2]) + .17), BRZ)  # bronze edges on both faces
for i in range(14):  # bolted plates round the ring, and hooks curling inward
    a = i / 14 * 2 * np.pi; c = (np.cos(a) * 1.16, RC[1] + np.sin(a) * 1.16 * 1.32, 0)
    M.add(f'pl{i}', lambda p, c=c, a=a: box(p, c, (.2, .2, .27), .04, rot('z', a)), PLATE)
    M.add(f'bt{i}', lambda p, c=c: sphere(p, (c[0], c[1], .28), .045), BRZ); M.add(f'bu{i}', lambda p, c=c: sphere(p, (c[0], c[1], -.28), .045), BRZ)
    if i % 2: spk(M, f'hk{i}', (c[0] * 1.15, RC[1] + (c[1] - RC[1]) * 1.15, 0), (np.cos(a + .4), np.sin(a + .4) * 1.3, 0), .5, .07, BRZ)
M.add('void', lambda p: np.maximum((np.sqrt(p[..., 0] ** 2 + ((p[..., 1] - RC[1]) / 1.32) ** 2) - 1.0) * .8, np.abs(p[..., 2]) - .06), VOID)
M.add('eye', lambda p: ell(p, RC, (.26, .36, .12)), EYE)
G.add('geye', lambda p: ell(p, RC, (.75, .95, .3)), GT); G.add('grift', lambda p: np.abs(ell(p, RC, (1.05, 1.4, .25))) - .03, GT)
for i in range(9):  # crescent spires closing round the rift, bronze-tipped, a vein of light up each
    a = i / 9 * 2 * np.pi + .2; b = (np.cos(a) * 2.35, -1.1, np.sin(a) * 2.0); inw = np.array((-np.cos(a), 0, -np.sin(a)))
    L = 3.4 + rng.uniform(0, 1.2); pts = bez3(b, tuple(np.array(b) + np.array((0, L * .45, 0)) + inw * .1), tuple(np.array(b) + np.array((0, L * .8, 0)) + inw * .5), tuple(np.array(b) + np.array((0, L * .95, 0)) + inw * 1.05))
    taper(M, f'sp{i}', pts, .27, .02, CHIT, .02, .9)
    vp = [tuple(np.array(q) + inw * (.2 * (1 - j / (len(pts) - 1)) + .02)) for j, q in enumerate(pts)]
    taper(M, f'sv{i}', vp[:-1], .05, .015, VEIN, .01, .9); G.add(f'gv{i}', lambda p, a0=vp[1], b0=vp[-2]: cap(p, a0, b0, .12), GT)
    M.add(f'st{i}', lambda p, c=pts[-1]: sphere(p, c, .07), BRZ); spk(M, f'stp{i}', pts[-2], tuple(np.array(pts[-1]) - np.array(pts[-2])), .45, .07, BRZ)
    for j in range(2, 7, 2): spk(M, f'ss{i}{j}', pts[j], tuple(-inw + np.array((0, .4, 0))), .32, .055, BRZ)
for k in range(7):  # clutches of eggs in dark membranes
    a = k / 7 * 2 * np.pi + .5; d = 1.05 + (k % 3) * .35; cx, cz = np.cos(a) * d, np.sin(a) * d * .85
    M.add(f'mb{k}', lambda p, c=(cx, -.98, cz): ell(p, c, (.5, .2, .42)), MEMB, .08)
    for e in range(5):
        s = .13 + rng.uniform(0, .09); ox, oz = rng.uniform(-.3, .3), rng.uniform(-.25, .25); c = (cx + ox, -.86 + s * .7, cz + oz)
        M.add(f'eg{k}{e}', lambda p, c=c, s=s: ell(p, c, (s, s * 1.2, s)), EGG); G.add(f'ge{k}{e}', lambda p, c=c, s=s: sphere(p, c, s * 2.1), GE)
for i in range(14):  # coral trees, their tips lit
    a = rng.uniform(0, 2 * np.pi); d = .9 + rng.uniform(0, 1.7); base = (np.cos(a) * d, -1.0, np.sin(a) * d * .85); red = i % 3 > 0; c = COR if red else PUR
    for bb in range(3):
        dd = norm((rng.uniform(-.6, .6), 1, rng.uniform(-.6, .6))); L = rng.uniform(.4, .8); tip = tuple(base[q] + dd[q] * L for q in range(3))
        M.add(f'co{i}{bb}', lambda p, a=base, t=tip: cap(p, a, t, .05), c); M.add(f'ct{i}{bb}', lambda p, t=tip: sphere(p, t, .07), CTIP if red else PTIP)
        if bb == 0: G.add(f'gc{i}', lambda p, t=tip: sphere(p, t, .22), GP)
CI = {}
def npaint(P, N, A, E, idx):
    v = .5 * panels(P, .35, .3, .3) + .5 * hashf(idx.astype(np.int64), idx.astype(np.int64) * 7 + 1, 3); lit = E[:, :3].sum(1) > .05
    A[~lit, :3] *= (.62 + .76 * v[~lit])[:, None]; top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .25 * top)[:, None]
    rock = np.isin(idx, CI['rock']); m = np.where(rock)[0]; cv = worley(P[m], 1.1); g = cv < .012; dk = (cv >= .012) & (cv < .045)  # sea-light in the rock's cracks
    E[m[g], :3] = (.03, .5, .55); A[m[g], :3] = (.01, .05, .06); A[m[dk], :3] *= (.35 + .65 * (cv[dk] - .012) / .033)[:, None]
    m = np.where(idx == CI['void'])[0]; x = P[m, 0]; y = (P[m, 1] - RC[1]) / 1.32; r = np.sqrt(x * x + y * y); th = np.arctan2(y, x)  # the whirlpool
    sw = .5 + .5 * np.sin(5 * th + 8 * r); arm = np.clip((sw - .72) / .28, 0, 1) ** 1.5 * np.clip(1.1 - r, 0, 1); E[m, :3] = np.array((.02, .55, .6)) * arm[:, None] + np.array((.0, .1, .14)) * (1 - r)[:, None].clip(0, 1); A[m, :3] = np.array((.004, .03, .05))
CI['rock'] = [i for i, (n, f, mt, kk) in enumerate(M.parts) if mt is ROCK]; CI['void'] = [i for i, (n, f, mt, kk) in enumerate(M.parts) if n == 'void'][0]
M.bake(sys.argv[1] + '/cnest', npaint); G.bake(sys.argv[1] + '/cnest_g', None)
