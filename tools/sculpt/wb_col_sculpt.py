# The Shard Colossus (World Boss "col", BOSS3D.colossus), sculpted after the owner's painting docs/art/boss/colossus-skin.webp:
# a giant of dark plum stone armoured in layered amethyst shards with ice-cyan edges, violet light in the cracks, a starburst of
# shards round the glowing heart, a crown of blades, scythe-shard forearms. Each rig part is sculpted in its own pivot frame at the
# size of the rock it replaces (the game's rock(r, det, sx, sy, sz) is an ellipsoid of radii up to 1.14 r * (sx, sy, sz) centred on
# the part's origin), so the rig, its animation and its effects are untouched. Right-hand parts only: the left side mirrors them.
# python3 wb_col_sculpt.py <part> <outdir> [voxel] -> <outdir>/col_<part>
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdf import *
from crc_lib import norm
from mon_sculpt import M_

STONE = M_((.03, .018, .045), .55, .25); STONE2 = M_((.05, .03, .07), .5, .3)
AME = M_((.09, .025, .2), .12, .3, (.1, .02, .3)); AME2 = M_((.16, .05, .32), .1, .35, (.2, .05, .5)); ICE = M_((.06, .22, .32), .06, .35, (.05, .4, .7))
VEIN = M_((.3, .1, .45), .3, .1, (.85, .3, 1.0)); EYE = M_((.4, .7, .9), .1, .1, (.7, 1.0, 1.0)); HOT = M_((.6, .4, .7), .2, .1, (1.0, .55, 1.0))

def shard(p, base, d, L, r, twist=0.0):
    """a hexagonal crystal from base along d: L long, r across the flats, the last 38% a six-sided point"""
    d = np.array(norm(d), np.float32); a0 = np.array((0, 1, 0) if abs(d[1]) < .9 else (1, 0, 0), np.float32); u = np.cross(d, a0); u /= np.linalg.norm(u); v = np.cross(d, u)
    c, s = np.cos(twist), np.sin(twist); u, v = u * c + v * s, v * c - u * s
    q = p - np.array(base, np.float32); a = q @ d; x = q @ u; y = q @ v
    hx = np.maximum(np.abs(x), np.maximum(np.abs(.5 * x + .866 * y), np.abs(.5 * x - .866 * y)))
    rr = r * np.clip((L - a) / (L * .38), 0, 1)
    return np.maximum(np.maximum(hx - rr, -a), a - L) * .75

def crag2(p, c, r, seed, amp=.18):
    q = (p - V(*c)) / V(*r); return ell(p, c, r) + noise3(q, 2.2, seed) * amp * min(r) - np.abs(noise3(q, 5.0, seed + 3)) * amp * .5 * min(r)

def surf(r, n, seed, up=0.0, front=0.0, keep=None):
    """n points on the ellipsoid of radii r, each with its outward normal (biased up / forward)"""
    rng = np.random.default_rng(seed); out = []
    while len(out) < n:
        v = rng.normal(size=3); v /= np.linalg.norm(v); v[1] += up * rng.uniform(0, 1); v[2] += front * rng.uniform(0, 1); v /= np.linalg.norm(v)
        P = v * np.array(r); N = v / np.array(r); N /= np.linalg.norm(N)
        if keep and not keep(P, N): continue
        out.append((P, N, rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)))
    return out

def armour(M, n, r, cnt, seed, L0, L1, rad, sweep=(0, .55, -.25), up=0.0, front=0.0, keep=None, ice=.25, sink=.35):
    """shards over a part: rooted under the surface, leaning out along the normal and swept back/up like scales"""
    sw = np.array(sweep)
    for j, (P, N, a, b, c) in enumerate(surf(r, cnt, seed, up, front, keep)):
        d = N * .8 + sw * (.6 + .7 * a); d /= np.linalg.norm(d); L = (L0 + (L1 - L0) * b) * 1.8; R = rad * (.8 + .6 * c) * 1.4; base = P - N * R * 1.2 - d * L * .15
        mat = ICE if c < ice else (AME2 if a > .7 else AME)
        M.add(f'{n}{j}', lambda p, base=tuple(base), d=tuple(d), L=L, R=R, t=a * 3: shard(p, base, d, L, R, t), mat)

def veins(M, n, r, cnt, seed, rad):
    """thin violet light along the stone between the shards"""
    rng = np.random.default_rng(seed)
    for j in range(cnt):
        v = rng.normal(size=3); v /= np.linalg.norm(v); w = rng.normal(size=3); w -= v * np.dot(v, w); w /= np.linalg.norm(w)
        a = v * np.array(r) * .97; b = (v + w * .45); b /= np.linalg.norm(b); b = b * np.array(r) * .97
        M.add(f'{n}{j}', lambda p, a=tuple(a), b=tuple(b), rr=rad * rng.uniform(.6, 1.2): cap(p, a, b, rr), VEIN)

def body(M, n, r, seed, sh, L0, L1, rad, **kw):
    M.add(n + 'core', lambda p: crag2(p, (0, 0, 0), r, seed), STONE, .05)
    veins(M, n + 'v', r, max(4, sh // 5), seed + 9, min(r) * .035)
    armour(M, n + 'a', r, sh, seed + 1, L0, L1, rad, **kw)

def chest(M):  # rock(3.2, 1, 1.15, 1.05, .85): radii about (3.7, 3.4, 2.7); the heart sits at (0, .3, 2.5)
    r = (3.5, 3.2, 2.55); hc = np.array((0, .3, 2.55))
    M.add('core', lambda p: crag2(p, (0, 0, 0), r, 11, .12), STONE, .05)
    M.add('pec', lambda p: crag2(p, (0, .9, .9), (3.1, 1.7, 1.9), 12, .1), STONE2, .4)
    veins(M, 'v', r, 14, 13, .1)
    # the starburst: shards radiating from the heart across the chest, longest near it
    for j in range(22):
        a = j / 22 * 2 * np.pi + .13 * np.sin(j * 3.7); dd = np.array((np.cos(a), np.sin(a) * .9, .35)); dd /= np.linalg.norm(dd)
        L = 2.1 + .9 * np.sin(j * 2.3) ** 2; base = hc + np.array((np.cos(a), np.sin(a), 0)) * 1.35 - np.array((0, 0, .5))
        M.add(f'sb{j}', lambda p, base=tuple(base), d=tuple(dd), L=L, R=.32 + .08 * np.cos(j): shard(p, base, d, L, R, j * .7), ICE if j % 5 == 0 else AME2)
    # the rest of the torso: scale-like shards swept up and back toward the shoulders
    armour(M, 'a', r, 70, 14, 1.3, 2.6, .34, sweep=(0, .7, -.5), keep=lambda P, N: not (np.linalg.norm((P - hc)[:2]) < 2.2 and P[2] > 1.2))
    # the heart's socket: a crater ringed with hot light
    M.carve('sock', lambda p: ell(p, tuple(hc + (0, 0, .35)), (1.55, 1.75, 1.3)), HOT, .25)

def pelvis(M): body(M, 'p', (2.2, 1.35, 1.7), 21, 34, .9, 1.9, .26, sweep=(0, -.8, -.2))
def head(M):  # rock(1.15, 1, 1, 1.1, 1) in a group scaled 1.35; eyes at (+-.42, .2, 1.02)
    r = (1.08, 1.2, 1.08); M.add('core', lambda p: crag2(p, (0, 0, 0), r, 31, .1), STONE, .04)
    M.add('jaw', lambda p: crag2(p, (0, -.55, .45), (.8, .55, .7), 32, .1), STONE2, .15)
    M.add('brow', lambda p: crag2(p, (0, .45, .75), (1.0, .28, .45), 33, .08), STONE2, .1)
    for sx in (1, -1):
        M.carve(f'es{sx}', lambda p, sx=sx: ell(p, (sx * .42, .2, 1.0), (.26, .17, .3)), STONE)
        M.add(f'e{sx}', lambda p, sx=sx: ell(p, (sx * .42, .2, .9), (.2, .12, .12)), EYE)
        for k in range(3): M.add(f'ck{sx}{k}', lambda p, sx=sx, k=k: shard(p, (sx * .7, -.2 - k * .2, .5), (sx * .8, -.1, .5), .7 + k * .1, .12), AME)
    # the crown of blades, tallest at the back
    for j in range(15):
        a = (j / 14 - .5) * 2.6; dd = np.array((np.sin(a) * .8, 1, -.55 - .2 * np.cos(a))); dd /= np.linalg.norm(dd); L = 1.5 + 1.1 * np.cos(a * .7) + .3 * (j % 3)
        M.add(f'cr{j}', lambda p, b=(np.sin(a) * .7, .6, -.2 + .3 * np.cos(a)), d=tuple(dd), L=L, R=.16 + .04 * (j % 2): shard(p, b, d, L, R, j), ICE if j % 4 == 0 else AME2)
    veins(M, 'v', r, 5, 34, .035)
def shoulder(M):  # rock(1.5, 1, 1, 1, 1): a boulder pauldron; spikes up and out
    body(M, 's', (1.55, 1.45, 1.5), 41, 26, 1.1, 2.4, .26, sweep=(.6, .9, -.3), up=.6)
def uarm(M): body(M, 'u', (.9, 2.3, .9), 51, 26, .7, 1.5, .18, sweep=(.5, -.4, -.4))
def farm(M):  # forearm: the scythe shards sweep down and back off its outer side
    body(M, 'f', (1.0, 2.2, 1.0), 61, 24, .7, 1.4, .18, sweep=(.3, -.7, -.3))
    for j in range(4): M.add(f'sc{j}', lambda p, j=j: shard(p, (.6, .8 - j * .7, -.2), (.55, -.75, -.35), 2.2 - j * .3, .2, j), ICE if j == 1 else AME2)
def hand(M): body(M, 'h', (1.0, .9, 1.0), 71, 12, .5, 1.0, .16, sweep=(0, -.6, .4))
def thigh(M): body(M, 't', (1.3, 2.7, 1.3), 81, 30, .8, 1.7, .22, sweep=(.3, -.6, .2))
def shin(M):
    body(M, 'n', (1.3, 2.5, 1.3), 91, 26, .8, 1.6, .22, sweep=(0, -.5, .4))
    for j in range(3): M.add(f'kp{j}', lambda p, j=j: shard(p, (0, 1.6 - j * .5, .9), (0, .6, 1), 1.6 - j * .3, .3, j), AME2)
def foot(M): body(M, 'o', (1.55, .7, 2.0), 101, 18, .6, 1.3, .2, sweep=(0, .2, .6), front=.5)
def plat(M):  # rock(8.5, 2, 1, .3, 1): the floating chunk of the mine
    r = (8.6, 2.3, 8.6); M.add('core', lambda p: crag2(p, (0, 0, 0), r, 111, .1), STONE, .1)
    M.add('top', lambda p: crag2(p, (0, .9, 0), (7.6, 1.2, 7.6), 112, .08), STONE2, .4)
    veins(M, 'v', r, 26, 113, .14)
    armour(M, 'a', r, 60, 114, 1.2, 3.0, .35, sweep=(0, .3, 0), keep=lambda P, N: abs(P[0]) > 3.2 or abs(P[2]) > 3.2 or P[1] < 0)
    for j in range(16):  # stalactites under it
        a = j / 16 * 2 * np.pi + .3 * np.sin(j); rr = 3 + 4 * ((j * 7) % 5) / 5
        M.add(f'st{j}', lambda p, b=(np.cos(a) * rr, -1.2, np.sin(a) * rr), L=2 + (j % 4) * .8: shard(p, b, (0, -1, 0), L, .45, j), AME if j % 3 else ICE)

SPEC = {  # part: (sculptor, lo, hi, voxel)
    'chest': (chest, (-6.2, -5.5, -4.8), (6.2, 6, 6.2), .06), 'pelvis': (pelvis, (-4, -3.6, -3.4), (4, 3, 3.4), .05),
    'head': (head, (-2.6, -1.6, -1.8), (2.6, 3.8, 2.2), .03), 'shoulder': (shoulder, (-3.4, -3, -3.4), (4.4, 4.6, 3.4), .045),
    'uarm': (uarm, (-2.4, -3.8, -2.4), (2.8, 3.4, 2.2), .04), 'farm': (farm, (-2.4, -4.4, -2.6), (3.2, 3.4, 2.4), .04),
    'hand': (hand, (-1.9, -2.2, -1.6), (1.9, 1.6, 2.2), .03), 'thigh': (thigh, (-2.8, -4.6, -2.6), (3.2, 3.6, 3.0), .045),
    'shin': (shin, (-2.6, -4.2, -2.4), (2.6, 3.8, 3.6), .045), 'foot': (foot, (-2.8, -1.6, -3.0), (2.8, 2.0, 3.8), .04),
    'plat': (plat, (-11.5, -6.6, -11.5), (11.5, 5.5, 11.5), .09),
}
if __name__ == '__main__':
    k = sys.argv[1]; f, lo, hi, vox = SPEC[k]; vox = float(sys.argv[3]) if len(sys.argv) > 3 else vox
    M = Model(lo, hi, vox); f(M); M.bake(sys.argv[2] + '/col_' + k)
