# The rest of the aliens and event units sculpted after the owner's paintings (owner: "Build all of them!"):
# the Hive (Drone, Spore Spitter, Carapace Brute, Hive Lord, Hive Leviathan; docs/art/mon/drone, spitter, brute, lord, leviathan),
# the Collective (Collective Drone, Assimilation Cube, Tactical Sphere; cdrone, cube, sphere), Omega's Neural Node and Assimilation
# Pylon, the Carcinid Breach nest and the fallen Leviathan. python3 mon4_sculpt.py <key> <outdir> [voxel] -> <outdir>/<key>[_g].
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import lerp, chain, spk, blade, norm, oell
from mon_sculpt import M_, lathe_x, seg2, _fin, Rx, Ry, Rz
from mon2_sculpt import bez3, taper, leviathan as levi_body
from mon3_sculpt import crag, _mats, _spire

# ---------------------------------------------------------------- the Hive: purple-black chitin, ivory claws, magenta light
_HC = {}
def hive_mats(glow=(1.0, .2, .85)):
    global _HC; _HC = dict(CH=M_((.025, .01, .03), .3, .55), PL=M_((.06, .02, .07), .28, .65), RIM=M_((.16, .06, .15), .25, .75), CLAW=M_((.55, .48, .44), .25, .3),
                GL=M_(tuple(x * .15 for x in glow), .2, .1, glow), EYE=M_((.1, .05, .2), .1, .2, (.5, .4, 1.0)), DARK=M_((.01, .005, .015), .5, .2)); return _HC
def plates_along(M, n, P, rads, mat, under, up=(0, 1, 0), cnt=1, spikes=None, sp_mat=None, sp_len=.3):
    """armour plates over a body chain: one shingle per segment on its back (and on its flanks if cnt 3), spikes off their rear edges"""
    for i in range(1, len(P) - 1):
        q = np.array(P[i]); tg = np.array(P[i + 1]) - np.array(P[i - 1]); tg /= np.linalg.norm(tg); u = np.array(up, float) - tg * np.dot(up, tg); u /= np.linalg.norm(u); sd = np.cross(tg, u); rr = rads[i]
        for a in ([0] if cnt == 1 else [0, .9, -.9]):
            out = u * np.cos(a) + sd * np.sin(a); c = q + out * rr * .85; Rm = np.array([tg, np.cross(out, tg), out], f32)
            M.add(f'{n}u{i}{a}', lambda p, c=tuple(c - out * .02), Rm=Rm, r=(rr * .95, rr * .85, rr * .2): oell(p, c, Rm, r), under)
            M.add(f'{n}p{i}{a}', lambda p, c=tuple(c), Rm=Rm, r=(rr * .9, rr * .8, rr * .2): oell(p, c, Rm, r), mat)
            if spikes is not None and (i % spikes == 0): spk(M, f'{n}s{i}{a}', tuple(c + out * rr * .1), tuple(out * .9 - tg * .6), sp_len * rr * 3, rr * .14, sp_mat or mat)

def leg(M, n, a, kn, ft, r0, claw=.0, spikes=2, C=None):
    C = C or _HC
    taper(M, n + 'a', [a, kn], r0, r0 * .75, C['CH']); taper(M, n + 'b', [kn, ft], r0 * .7, r0 * .2, C['PL'])
    M.add(n + 'j', lambda p: sphere(p, kn, r0 * .85), C['GL'] if spikes else C['RIM'])
    for j in range(spikes): q = lerp(a, kn, (j + 1) / (spikes + 1)); spk(M, f'{n}s{j}', q, (-.3, 1, 0), r0 * 2.2, r0 * .35, C['CLAW'])
    spk(M, n + 't', ft, tuple(np.array(ft) - np.array(kn)), r0 * 2.5 + claw, r0 * .35, C['CLAW'])
def head(M, n, c, s, C, gape=.35, fangs=6, horn=True):
    M.add(n + 'sk', lambda p: ell(p, c, (.55 * s, .32 * s, .36 * s)), C['PL'], .04)
    M.add(n + 'jw', lambda p: ell(p, (c[0] + .1 * s, c[1] - .2 * s - gape * .2 * s, c[2]), (.45 * s, .12 * s, .3 * s)), C['CH'], .02)
    M.add(n + 'mo', lambda p: ell(p, (c[0] + .2 * s, c[1] - .12 * s, c[2]), (.35 * s, .05 * s + gape * .08 * s, .24 * s)), C['GL'])
    for sd in (1, -1):
        M.add(f'{n}e{sd}', lambda p, sd=sd: sphere(p, (c[0] + .25 * s, c[1] + .12 * s, c[2] + sd * .22 * s), .08 * s), C['EYE'])
        for j in range(fangs // 2):
            spk(M, f'{n}f{sd}{j}', (c[0] + (.42 - j * .1) * s, c[1] - .08 * s, c[2] + sd * (.08 + j * .06) * s), (.2, -1, 0), max(.08, .28 - j * .03) * s, .04 * s, C['CLAW'])
            spk(M, f'{n}g{sd}{j}', (c[0] + (.38 - j * .1) * s, c[1] - (.22 + gape * .2) * s, c[2] + sd * (.07 + j * .05) * s), (.2, 1, 0), max(.06, .18 - j * .02) * s, .035 * s, C['CLAW'])
        if horn:
            for j in range(3): spk(M, f'{n}h{sd}{j}', (c[0] - (.1 + j * .15) * s, c[1] + .22 * s, c[2] + sd * (.15 + j * .05) * s), (-1, .6, sd * .35), (.55 - j * .1) * s, .07 * s, C['RIM'])

def hdrone(M, G):
    C = hive_mats(); P = [(1.0, .05, 0), (.4, .08, 0), (-.2, .1, 0), (-.8, .05, 0), (-1.3, -.05, 0)]; R = [.22, .3, .28, .22, .1]
    chain(M, 'b', P, R, C['CH'], .08); plates_along(M, 'p', P, R, C['PL'], C['GL'], spikes=1, sp_mat=C['RIM'], sp_len=.35)
    head(M, 'h', (1.05, .1, 0), .55, C, .3)
    for sd in (1, -1):
        for i, x in enumerate((.55, .1, -.35)): leg(M, f'l{sd}{i}', (x, -.05, sd * .2), (x - .05, .3, sd * .75), (x - .3, -.3, sd * 1.25), .055)
        chain(M, f'sc{sd}', [(.8, 0, sd * .2), (1.05, .25, sd * .55), (1.4, .1, sd * .6)], [.07, .06, .04], C['PL']); spk(M, f'sct{sd}', (1.4, .1, sd * .6), (.4, -1, -sd * .2), .5, .06, C['CLAW'])
        for j, (x, L) in enumerate(((.1, 1.1), (-.25, .9))):  # the wings, see-through magenta veined
            c = (x - L * .4, .3, sd * L * .55); Rm = rot('y', sd * .4).T
            G.add(f'w{sd}{j}', lambda p, c=c, Rm=Rm, L=L: oell(p, c, Rm, (L * .45, .015, L * .55)), M_((0, 0, 0), .2, 0, (.35, .06, .3)))
def hspitter(M, G):
    C = hive_mats((.4, 1.0, .25)); ACID = M_((.15, .35, .05), .1, .1, (.5, 1.0, .2))
    P = [(1.1, .1, 0), (.5, .15, 0), (-.1, .2, 0), (-.7, .15, 0), (-1.25, 0, 0)]; R = [.24, .34, .36, .3, .15]
    chain(M, 'b', P, R, C['CH'], .08); plates_along(M, 'p', P, R, C['PL'], C['CH'], spikes=2, sp_mat=C['RIM'])
    for j, (x, y, z, r0) in enumerate(((-.2, .55, .12, .26), (-.6, .52, -.12, .24), (.2, .5, -.05, .2), (-.9, .4, .08, .18))): M.add(f'sac{j}', lambda p, c=(x, y, z), r0=r0: sphere(p, c, r0), ACID, .03)
    head(M, 'h', (1.25, .12, 0), .6, C, .6, 8)
    for j in range(5): M.add(f'ac{j}', lambda p, j=j: sphere(p, (1.75 + j * .08, .0 - j * .03, 0), .07 - j * .008), ACID)
    for sd in (1, -1):
        for i, x in enumerate((.6, .15, -.3, -.75)): leg(M, f'l{sd}{i}', (x, -.05, sd * .25), (x - .1, .35, sd * .65), (x - .3, -.52, sd * .55), .05, spikes=1)
def hbrute(M, G):
    C = hive_mats((1.0, .35, .2)); P = [(1.0, .25, 0), (.4, .3, 0), (-.3, .25, 0), (-1.0, .1, 0), (-1.6, -.05, 0)]; R = [.42, .55, .52, .4, .18]
    chain(M, 'b', P, R, C['CH'], .1); plates_along(M, 'p', P, R, C['PL'], C['RIM'], cnt=3, spikes=1, sp_mat=C['RIM'], sp_len=.3)
    head(M, 'h', (1.2, .25, 0), .85, C, .6, 10)
    for sd in (1, -1):
        for i, x in enumerate((.55, -.6)): leg(M, f'l{sd}{i}', (x, .05, sd * .4), (x + .1, -.25, sd * .62), (x + .25, -.62, sd * .66), .14, claw=.1)
        chain(M, f'ar{sd}', [(.8, .2, sd * .45), (1.2, -.1, sd * .72), (1.55, -.35, sd * .6)], [.14, .12, .1], C['PL']);
        for j in range(3): spk(M, f'cl{sd}{j}', (1.55, -.35, sd * .6), (.6, -.4 + j * .2, sd * (j - 1) * .2), .45, .05, C['CLAW'])
def hlord(M, G):
    C = hive_mats(); P = [(1.2, .1, 0), (.5, .15, 0), (-.3, .15, 0), (-1.2, .05, 0), (-2.1, -.05, 0), (-2.9, -.1, 0)]; R = [.3, .4, .45, .38, .26, .1]
    chain(M, 'b', P, R, C['CH'], .1); plates_along(M, 'p', P, R, C['PL'], C['GL'], cnt=3, spikes=1, sp_mat=C['RIM'])
    for i in range(6): M.carve(f'sg{i}', lambda p, i=i: np.maximum(np.abs(p[..., 0] - (.6 - i * .45)) - .03, -(p[..., 1] - .1)), C['GL'])
    head(M, 'h', (1.35, .15, 0), .7, C, .3)
    for j in range(7):  # the crown of blades
        a = (j - 3) * .3; blade(M, f'cr{j}', (1.3, .4, a * .4), norm((-.6, 1, a)), .7 + (3 - abs(j - 3)) * .15, .08, C['RIM'], up=(0, 0, 1))
    for sd in (1, -1):  # great carapace wings of blades and scythe arms held out
        for j in range(4):
            b = (.3 - j * .35, .3, sd * .4); blade(M, f'wg{sd}{j}', b, norm((-.5, .25, sd)), 1.9 - j * .25, .14, C['PL'], up=(0, 1, 0))
        chain(M, f'ar{sd}', [(.8, .1, sd * .35), (1.3, .35, sd * 1.1), (1.75, .1, sd * 1.5)], [.1, .08, .06], C['PL']); spk(M, f'as{sd}', (1.75, .1, sd * 1.5), (.3, -1, -sd * .4), .9, .08, C['CLAW'])
        for i, x in enumerate((.4, -.3, -1.0)): leg(M, f'l{sd}{i}', (x, -.05, sd * .3), (x - .1, -.2, sd * .7), (x - .4, -.38, sd * .9), .05, spikes=0)
def hleviathan(M, G):
    C = hive_mats(); n = 12; P = [(4.2 - t * 9.6, .1 * np.sin(t * 4), .25 * np.sin(t * 5) * t) for t in np.linspace(0, 1, n)]; R = [.75 * (1 - t * .85) + .08 for t in np.linspace(0, 1, n)]
    chain(M, 'b', P, R, C['CH'], .12); plates_along(M, 'p', P, R, C['PL'], C['GL'], cnt=3, spikes=1, sp_mat=C['RIM'], sp_len=.35)
    head(M, 'h', (4.35, .3, 0), 2.4, C, 1.1, 12)
    for sd in (1, -1):
        for i, x in enumerate((2.8, 1.5, .2, -1.1)): leg(M, f'l{sd}{i}', (x, -.1, sd * .5), (x + .25, .35, sd * 1.25), (x - .2, -.85, sd * 1.4), .15, claw=.15, spikes=1)
def cdrone(M, G):
    # v819 after the painting: a wide armoured crab-spider, a great green eye, eight long segmented claw legs hooked down, lit joints
    MET = M_((.07, .08, .08), .3, .85); DK = M_((.025, .03, .03), .45, .7); GL = M_((.1, .4, .1), .1, .1, (.4, 1.0, .45))
    M.add('core', lambda p: ell(p, (0, .05, 0), (.6, .38, .6)) + noise3(p, 9, 2) * .01, MET)
    M.add('belly', lambda p: ell(p, (0, -.1, 0), (.38, .2, .38)), DK)
    for i in range(12):  # overlapping armour plates over the shell
        a = i / 12 * 2 * np.pi; M.add(f'pl{i}', lambda p, a=a: box(p, (np.cos(a) * .4, .32, np.sin(a) * .4), (.16, .03, .13), .01, rot('y', -a) @ rot('z', .55)), DK if i % 2 else MET)
    M.add('crown', lambda p: ell(p, (0, .33, 0), (.2, .07, .2)), MET)
    M.add('eye', lambda p: sphere(p, (.56, .06, 0), .15), GL); M.add('eyr', lambda p: torus(p, (.56, .06, 0), 'x', .18, .04), MET); M.add('eyr2', lambda p: torus(p, (.58, .06, 0), 'x', .26, .022), GL)
    for i in range(8):
        a = (i + .5) / 8 * 2 * np.pi; o = np.array((np.cos(a), 0, np.sin(a)))
        pts = bez3(tuple(o * .38 + (0, .1, 0)), tuple(o * .8 + (0, .62, 0)), tuple(o * 1.3 + (0, .35, 0)), tuple(o * 1.42 + (0, -.62, 0)), 9)
        taper(M, f'lg{i}', pts, .13, .04, MET)
        for j in (2, 5): M.add(f'lj{i}{j}', lambda p, q=pts[j]: sphere(p, q, .075), GL if j == 2 else DK)
        for j in range(1, 8, 2): M.add(f'lp{i}{j}', lambda p, q=pts[j], j=j: sphere(p, q, .14 - j * .01), DK)  # armour cuffs
        tip = np.array(pts[-1]); spk(M, f'cl{i}', tuple(tip), tuple(-o * .6 + np.array((0, -.3, 0))), .4, .08, MET)  # the hooked claw
def cube(M, G):
    # v819 after the painting: dense dark machinery, recessed shafts, small scattered green lights and one bright shaft down each face
    MET = M_((.05, .055, .055), .45, .85); DK = M_((.018, .02, .02), .55, .7); GL = M_((.08, .35, .1), .1, .1, (.35, 1.0, .4)); rng = np.random.default_rng(31); S = 1.3
    M.add('hull', lambda p: box(p, (0, 0, 0), (S, S, S), .03), DK)
    def onface(ax, sg, u, v, w, h, d):
        c = [0, 0, 0]; c[ax] = sg * (S + d * .5); c[(ax + 1) % 3] = u; c[(ax + 2) % 3] = v; hs = [0, 0, 0]; hs[ax] = d / 2 + .01; hs[(ax + 1) % 3] = w / 2; hs[(ax + 2) % 3] = h / 2; return tuple(c), tuple(hs)
    for i in range(420):  # two layers of machinery
        ax = rng.integers(3); sg = rng.choice((-1, 1)); w, h = rng.uniform(.04, .45) * S, rng.uniform(.04, .45) * S; d = rng.uniform(.02, .14) * S
        c, hs = onface(ax, sg, rng.uniform(-1, 1) * (S - w / 2), rng.uniform(-1, 1) * (S - h / 2), w, h, d)
        M.add(f'bk{i}', lambda p, c=c, hs=hs: box(p, c, hs, .004), MET if i % 3 else DK)
    for i in range(40):  # recessed shafts
        ax = rng.integers(3); sg = rng.choice((-1, 1)); w, h = rng.uniform(.06, .22) * S, rng.uniform(.06, .4) * S
        c = [0, 0, 0]; c[ax] = sg * S; c[(ax + 1) % 3] = rng.uniform(-.85, .85) * S; c[(ax + 2) % 3] = rng.uniform(-.85, .85) * S; hs = [0, 0, 0]; hs[ax] = .14; hs[(ax + 1) % 3] = w / 2; hs[(ax + 2) % 3] = h / 2
        M.carve(f'rs{i}', lambda p, c=tuple(c), hs=tuple(hs): box(p, c, hs, .004), DK)
    BK = [b_ for b_ in M.parts if b_[0].startswith('bk')]
    for i in range(170):  # small green lights laid on top of machinery blocks, as in the painting
        ax = rng.integers(3); sg = rng.choice((-1, 1)); vert = rng.uniform() < .5; L_ = rng.uniform(.04, .22) * S; dep = rng.uniform(.03, .15) * S
        c, hs = onface(ax, sg, rng.uniform(-.95, .95) * S, rng.uniform(-.95, .95) * S, .02 if vert else L_, L_ if vert else .02, dep)
        M.add(f'gl{i}', lambda p, c=c, hs=hs: box(p, c, hs, .004), GL)
    for ax in range(3):
        for sg in (1, -1):  # the bright shaft down each face
            c, hs = onface(ax, sg, rng.uniform(-.3, .3) * S, 0, .04, 2 * S * .96, .1 * S)
            M.add(f'sh{ax}{sg}', lambda p, c=c, hs=hs: box(p, c, hs, .006), GL)
def sphere_(M, G):
    # v819 after the painting: dark plating in panels (dark seams), a few thin green seams standing proud, a recessed emitter dish of rings
    MET = M_((.09, .1, .1), .3, .85); DK = M_((.025, .03, .03), .5, .7); GL = M_((.08, .35, .1), .1, .1, (.4, 1.0, .45)); R = 1.1; rng = np.random.default_rng(41)
    M.add('hull', lambda p: sphere(p, (0, 0, 0), R), MET)
    for lat in np.linspace(-1.2, 1.2, 9): M.carve(f'la{lat:.2f}', lambda p, lat=lat: np.maximum(np.abs(np.arcsin(np.clip(p[..., 1] / (np.linalg.norm(p, axis=-1) + 1e-6), -1, 1)) - lat) * R - .012, -(np.linalg.norm(p, axis=-1) - R + .03)), DK)
    for lo in range(16): M.carve(f'lo{lo}', lambda p, a=lo / 16 * np.pi: np.maximum(np.abs(-np.sin(a) * p[..., 0] + np.cos(a) * p[..., 2]) - .012, -(np.linalg.norm(p, axis=-1) - R + .03)), DK)
    for i in range(70):  # raised plates
        th = rng.uniform(0, 2 * np.pi); ph = rng.uniform(-1.3, 1.3); n = np.array((np.cos(ph) * np.cos(th), np.sin(ph), np.cos(ph) * np.sin(th)))
        if n[0] > .55: continue
        t1 = norm(tuple(np.cross(n, (0, 1, 0)) + 1e-4)); t2 = np.cross(n, t1); Rm = np.array([t1, t2, n], f32)
        M.add(f'pp{i}', lambda p, c=tuple(n * R), Rm=Rm, w=rng.uniform(.1, .25), h=rng.uniform(.08, .2): box(p, c, (w, h, .035), .01, Rm.T), MET if i % 2 else DK)
    for i in range(44):  # thin green seams standing proud
        th = rng.uniform(0, 2 * np.pi); ph = rng.uniform(-1.2, 1.2); n = np.array((np.cos(ph) * np.cos(th), np.sin(ph), np.cos(ph) * np.sin(th)))
        if n[0] > .5: continue
        t1 = norm(tuple(np.cross(n, (0, 1, 0)) + 1e-4)); t2 = np.cross(n, t1); Rm = np.array([t1, t2, n], f32); L_ = rng.uniform(.12, .4); vert = i % 2
        M.add(f'gs{i}', lambda p, c=tuple(n * (R + .03)), Rm=Rm, hs=((.016, L_, .03) if vert else (L_, .016, .03)): box(p, c, hs, .006, Rm.T), GL)
    for j, r0 in enumerate((.66, .52, .38, .24)): M.add(f'em{j}', lambda p, r0=r0, j=j: torus(p, (np.sqrt(max(0, (R + .02) ** 2 - r0 ** 2)) + .035, 0, 0), 'x', r0, .04 if j % 2 == 0 else .026), GL if j % 2 == 0 else MET)
    M.add('emc', lambda p: sphere(p, (R * 1.0, 0, 0), .2), GL)
    M.add('emd', lambda p: np.maximum(sphere(p, (0, 0, 0), R + .015), R * .72 - p[..., 0]), DK)  # the dark dish face behind the rings
    M.add('belt', lambda p: np.maximum(torus(p, (0, 0, 0), 'y', R * 1.0, .045), p[..., 0] - .3), MET)
# ---------------------------------------------------------------- Omega's Neural Node and Assimilation Pylon (Mimic frame)
# v846 remastered after the Mimics' design legends: chrome, ribbed conduits, hooked claws and cyan light; legless, rooted in rock
CHRN = M_((.28, .31, .36), .16, 1.); ROCKN = M_((.06, .055, .06), .9, .1)
def _ring_bands(M, C, n, pts, rr):  # three lit bands on a conduit
    P = np.array(pts, np.float32)
    for j, f in enumerate((.3, .55, .8)):
        i = int(f * (len(P) - 1)); c = P[i]; d = P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]; d = d / (np.linalg.norm(d) + 1e-6)
        M.add(f'{n}b{j}', lambda p, c=c, d=d, r=rr: (lambda q: np.sqrt((np.sqrt(np.maximum((q * q).sum(-1) - (q @ d) ** 2, 0)) - r) ** 2 + (q @ d) ** 2) - r * .3)(p - c), C['GLOW'])
def mnode(M, G):
    """the Neural Node: a living brain-lantern. A folded glowing brain in a cage of hooked chrome ribs, rooted in a broken asteroid,
    three antenna spines lit at the tips"""
    C = _mats(); cp = (0, .95, 0); BR = M_((.05, .2, .26), .3, .2, (.22, .8, 1.0))
    M.add('rock', lambda p: crag(p, (0, -2.05, 0), (1.9, .72, 1.6), 5, .3, 1.4), ROCKN)
    def brain(p):
        q = p - V(*cp); d = ell(p, cp, (.78, .66, .62))
        fold = np.abs(np.sin(q[..., 0] * 11 + np.sin(q[..., 1] * 8) * 1.6) * np.sin(q[..., 2] * 10 + np.sin(q[..., 0] * 6)))
        return np.maximum(d + .045 * fold, np.where(q[..., 1] > 0, -(np.abs(q[..., 2]) - .025), -1e3))  # the folds, and the split between the halves
    M.add('brain', brain, BR, .02)
    M.add('stem', lambda p: rcone(p, (0, -1.3, 0), (0, .5, 0), .32, .2), C['SHELL'], .1)
    G.add('gbrain', lambda p: ell(p, cp, (1.05, .92, .9)), C['GLOW'])
    for i in range(7):  # the cage: chrome ribs from the stem rising round the brain, hooked outward at the top
        a = i / 7 * 2 * np.pi; pts = bez3((np.cos(a) * .45, -.5, np.sin(a) * .45), (np.cos(a) * 1.35, .4, np.sin(a) * 1.35), (np.cos(a) * 1.25, 1.75, np.sin(a) * 1.25), (np.cos(a) * .55, 2.35, np.sin(a) * .55), 9)
        taper(M, f'rib{i}', pts, .11, .04, CHRN); hk = np.array(pts[-1]); spk(M, f'rh{i}', tuple(hk), norm((np.cos(a) * .7, .9, np.sin(a) * .7)), .45, .05, CHRN)
    M.add('crown', lambda p: torus(p, (0, 2.3, 0), 'y', .6, .06), CHRN)
    for i in range(3):  # three antenna spines, lit at the tips
        a = i / 3 * 2 * np.pi + .3; b = (np.cos(a) * .5, 2.2, np.sin(a) * .5); t = (np.cos(a) * 1.2, 3.6 + .25 * i, np.sin(a) * 1.2)
        pts = bez3(b, (b[0] * 1.2, 2.8, b[2] * 1.2), (t[0] * .9, 3.3, t[2] * .9), t, 7); taper(M, f'an{i}', pts, .07, .025, C['CABL']); _ring_bands(M, C, f'an{i}', pts, .06)
        M.add(f'bulb{i}', lambda p, t=t: sphere(p, t, .16), C['GLOW']); G.add(f'gb{i}', lambda p, t=t: sphere(p, t, .38), C['GLOW'])
    for i in range(6):  # ribbed conduits from the rock up into the stem
        a = i / 6 * 2 * np.pi + .4; pts = bez3((np.cos(a) * 1.4, -1.55, np.sin(a) * 1.4), (np.cos(a) * 1.0, -1.1, np.sin(a) * 1.0), (np.cos(a) * .5, -.7, np.sin(a) * .5), (0, -.2, 0), 7)
        taper(M, f'cd{i}', pts, .12, .07, C['CABL'] if i % 2 else C['CAB']); (_ring_bands(M, C, f'cd{i}', pts, .11) if i % 2 else None)
    _roots(M, C, 9, 1.9)
def mpylon(M, G):
    """the Assimilation Pylon: an obelisk fused from stolen ship plating and chrome fins, conduits spiralling up it, lit panels, and on
    top an adaptation crystal held in three chrome claws (the battle tints its light to what Omega has adapted to)"""
    C = _mats(); PLT = M_((.13, .14, .16), .34, .9); PNL = M_((.04, .15, .2), .2, .2, (.25, .85, 1.0))
    M.add('rock', lambda p: crag(p, (0, -2.05, 0), (1.8, .7, 1.6), 9, .3, 1.4), ROCKN)
    rng = np.random.default_rng(46)
    for i in range(9):  # stacked hull plates, each narrower, each a little turned
        y = -1.3 + i * .48; w = .72 - i * .055; R = rot('y', rng.uniform(-.35, .35)) @ rot('z', rng.uniform(-.05, .05))
        M.add(f'pl{i}', lambda p, y=y, w=w, R=R: box(p, (0, y, 0), (w, .25, w * .8), .04, R), PLT, .03)
        for s in (1, -1): M.add(f'pn{i}{s}', lambda p, y=y, w=w, R=R, s=s: box(p, (0, y, s * w * .8), (w * .55, .05, .03), .01, R), PNL)
    M.add('neck', lambda p: rcone(p, (0, 2.9, 0), (0, 3.55, 0), .22, .12), CHRN)
    for i in range(4):  # chrome fins hooked back down the sides
        a = i / 4 * 2 * np.pi + np.pi / 4; base = (np.cos(a) * .62, 1.6, np.sin(a) * .62)
        pts = bez3(base, (np.cos(a) * 1.3, 2.1, np.sin(a) * 1.3), (np.cos(a) * 1.4, 1.0, np.sin(a) * 1.4), (np.cos(a) * 1.15, .1, np.sin(a) * 1.15), 8)
        taper(M, f'fn{i}', pts, .13, .02, CHRN)
    for j in range(3):  # conduits spiralling up the obelisk
        pts = [(np.cos(j * 2.1 + t * 5.5) * (.95 - t * .5), -1.4 + t * 4.2, np.sin(j * 2.1 + t * 5.5) * (.85 - t * .45)) for t in np.linspace(0, 1, 14)]
        taper(M, f'sc{j}', pts, .1, .05, C['CABL']); _ring_bands(M, C, f'sc{j}', pts, .09)
    cr = (0, 4.15, 0); CRY = M_((.55, .65, .7), .05, .3, (.7, 1.1, 1.3))
    M.add('cry', lambda p: (lambda q: np.abs(q[..., 0]) + np.abs(q[..., 1]) * .55 + np.abs(q[..., 2]) - .48)(p - V(*cr)) * .55, CRY)
    G.add('gcry', lambda p: sphere(p, cr, .95), C['GLOW'])
    for i in range(3):  # the cradle of claws
        a = i / 3 * 2 * np.pi; b = (np.cos(a) * .2, 3.5, np.sin(a) * .2)
        pts = bez3(b, (np.cos(a) * .75, 3.7, np.sin(a) * .75), (np.cos(a) * .7, 4.35, np.sin(a) * .7), (np.cos(a) * .25, 4.75, np.sin(a) * .25), 7); taper(M, f'cl{i}', pts, .08, .015, CHRN)
    _roots(M, C, 9, 1.9)
def _roots(M, C, n, R0):
    rng = np.random.default_rng(n * 7)
    for i in range(n):
        a = i / n * 2 * np.pi + rng.uniform(0, .3); R = R0 + rng.uniform(0, 1.2)
        taper(M, f'rt{i}', bez3((np.cos(a) * .4, -1.35, np.sin(a) * .4), (np.cos(a) * 1.4, -1.5, np.sin(a) * 1.4), (np.cos(a + .2) * R, -1.6, np.sin(a + .2) * R), (np.cos(a + .25) * R * 1.1, -1.55, np.sin(a + .25) * R * 1.1), 7), .16, .05, C['CAB'])
# ---------------------------------------------------------------- the Carcinid Breach nest: a rift into the Abyss in a mound of rock, crescent spires, coral, eggs
def bnest(M, G):
    ROCK = M_((.07, .06, .065), .9, .1); SH = M_((.08, .04, .1), .3, .6); CLAW = M_((.75, .48, .18), .25, .9); GL = M_((.05, .3, .3), .1, .1, (.2, .95, .9))
    COR = M_((.4, .04, .04), .7, .05, (.12, 0, 0)); PUR = M_((.25, .06, .3), .7, .05, (.18, .02, .25)); EGG = M_((.25, .08, .02), .2, .1, (.9, .45, .1)); VOID = M_((.005, .005, .01), 1, 0)
    rng = np.random.default_rng(77)
    M.add('mound', lambda p: crag(p, (0, -1.55, 0), (3.0, .96, 2.55), 5, .3, 1.2), ROCK)
    for i in range(9): M.add(f'bo{i}', lambda p, c=(np.cos(i * 2.3) * (1.6 + i % 3 * .4), -1.05, np.sin(i * 2.3) * (1.4 + i % 3 * .3)), r0=.35 + (i % 3) * .12: sphere(p, c, r0) + noise3(p, 6, i) * .08, ROCK)
    for i in range(9):  # crescent spires closing round the rift, gold-tipped
        a = i / 9 * 2 * np.pi + .2; b = (np.cos(a) * 2.35, -1.1, np.sin(a) * 2.0); inw = np.array((-np.cos(a), 0, -np.sin(a)))
        L = 3.4 + rng.uniform(0, 1.2); pts = bez3(b, tuple(np.array(b) + np.array((0, L * .45, 0)) + inw * .1), tuple(np.array(b) + np.array((0, L * .8, 0)) + inw * .5), tuple(np.array(b) + np.array((0, L * .95, 0)) + inw * 1.1), 8)
        taper(M, f'sp{i}', pts, .26, .02, SH if i % 2 else CLAW, .02, .9)
        for j in range(2, 7, 2): spk(M, f'ss{i}{j}', pts[j], tuple(-inw + np.array((0, .4, 0))), .35, .06, CLAW)
    M.add('ring', lambda p: torus((p - V(0, 1.1, 0)) / V(1, 1.35, 1), (0, 0, 0), 'z', 1.15, .2) * .85, CLAW)
    M.add('void', lambda p: np.maximum((np.sqrt(p[..., 0] ** 2 + ((p[..., 1] - 1.1) / 1.35) ** 2) - 1.02) * .8, np.abs(p[..., 2]) - .05), VOID)
    M.add('core', lambda p: ell(p, (0, 1.1, 0), (.55, .75, .2)), GL)
    G.add('glow', lambda p: np.abs(ell(p, (0, 1.1, 0), (1.0, 1.35, .5))) - .02, M_((0, 0, 0), .2, 0, (.1, .45, .45)))
    for i in range(12): a = i / 12 * 2 * np.pi; spk(M, f'rs{i}', (np.cos(a) * 1.25, 1.1 + np.sin(a) * 1.6, 0), (np.cos(a), np.sin(a) * 1.3, 0), .42, .08, CLAW)
    for i in range(14):  # coral trees
        a = rng.uniform(0, 2 * np.pi); d = .9 + rng.uniform(0, 1.7); base = (np.cos(a) * d, -1.0, np.sin(a) * d * .85); c = COR if i % 3 else PUR
        for bb in range(3):
            dd = norm((rng.uniform(-.6, .6), 1, rng.uniform(-.6, .6))); L = rng.uniform(.4, .8); tip = tuple(base[k] + dd[k] * L for k in range(3))
            M.add(f'co{i}{bb}', lambda p, a=base, t=tip: cap(p, a, t, .05), c)
            for e in range(2): t2 = tuple(np.array(lerp(base, tip, .6)) + np.array(norm((dd[0] + rng.uniform(-.8, .8), 1, dd[2] + rng.uniform(-.8, .8)))) * L * .45); M.add(f'ce{i}{bb}{e}', lambda p, a=lerp(base, tip, .6), t=t2: cap(p, a, t, .035), c)
    for i in range(26):
        a = rng.uniform(0, 2 * np.pi); d = .6 + rng.uniform(0, 1.8); s = .14 + rng.uniform(0, .16)
        M.add(f'eg{i}', lambda p, c=(np.cos(a) * d, -.95 + s * .6, np.sin(a) * d * .85), s=s: ell(p, c, (s, s * 1.15, s)), EGG)
# ---------------------------------------------------------------- the fallen Leviathan: its body gone dark, cyan rot in the wounds, gilded chains and a war-saddle
def fallen(M, G):
    levi_body(M)
    for (n, f, mat, k) in M.parts:
        pass
    for i, (nm, f, mat, k) in enumerate(list(M.parts)):  # its own colours drained toward violet-grey
        c = mat['c']; nc = tuple(min(1, x * .6 * .75 + y * .25) for x, y in zip(c, (.24, .2, .33))); M.parts[i] = (nm, f, dict(mat, c=nc, e=(.03, .3, .32) if 'e' in mat else mat.get('e', (0, 0, 0))), k)
    GOLD = M_((.7, .5, .15), .25, .9); SH = M_((.08, .04, .1), .3, .6); ROT = M_((.05, .3, .3), .1, .1, (.2, .9, .9))
    for i in range(4):
        x = -1.2 - i * 1.0; M.add(f'ch{i}', lambda p, x=x, i=i: torus(p, (x, .05, .12 * i), 'x', .85 - i * .08, .07), GOLD)
    for i in range(3): M.add(f'cl{i}', lambda p, i=i: cap(p, (-1.2 - i, .85 - i * .08, 0), (-2.2 - i, .8 - i * .08, 0), .05), GOLD)
    M.add('saddle', lambda p: np.maximum(ell(p, (.9, 1.0, 0), (.9, .35, .6)), .8 - p[..., 1]), SH, .05)
    for i in range(5): spk(M, f'sd{i}', (.5 + i * .2, 1.25, 0), (-.2, 1, 0), .6 + (i % 2) * .3, .06, GOLD)
    rng = np.random.default_rng(9)
    for i in range(8): M.add(f'wd{i}', lambda p, c=(rng.uniform(-6, 3), rng.uniform(-.2, .5), rng.uniform(-.5, .5)): sphere(p, c, .12), ROT)

SPEC = {'drone': (hdrone, (-1.8, -.8, -1.8), (2.0, 1.2, 1.8)), 'spitter': (hspitter, (-1.6, -.9, -1.0), (2.2, 1.0, 1.0)), 'brute': (hbrute, (-2.0, -1.1, -1.3), (2.3, 1.4, 1.3)),
        'lord': (hlord, (-3.2, -.8, -2.6), (2.6, 1.6, 2.6)), 'leviathan': (hleviathan, (-5.8, -1.6, -2.2), (6.0, 2.2, 2.2)), 'cdrone': (cdrone, (-1.85, -1.05, -1.85), (1.85, .85, 1.85)),
        'cube': (cube, (-1.5, -1.5, -1.5), (1.5, 1.5, 1.5)), 'sphere': (sphere_, (-1.3, -1.3, -1.3), (1.3, 1.3, 1.3)),
        'mnode': (mnode, (-3.8, -2.9, -3.8), (3.8, 4.4, 3.8)), 'mpylon': (mpylon, (-3.6, -2.9, -3.6), (3.6, 5.3, 3.6)),
        'cnest': (bnest, (-3.5, -2.6, -3.2), (3.5, 4.2, 3.2)), 'clevd': (fallen, (-9.6, -1.6, -2.2), (6.2, 2.4, 2.2))}
def paint(P, N, A, E, idx):
    glowing = E[:, 0] + E[:, 1] + E[:, 2] > .05; top = np.clip(N[:, 1], 0, 1); A[~glowing, :3] *= (1 + .3 * top[~glowing])[:, None]
if __name__ == '__main__':
    k = sys.argv[1]; f, lo, hi = SPEC[k]; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .03
    M = Model(lo, hi, vox); Gm = Model(lo, hi, vox); f(M, Gm); M.bake(sys.argv[2] + '/' + k, paint)
    if Gm.parts: Gm.bake(sys.argv[2] + '/' + k + '_g', None)
