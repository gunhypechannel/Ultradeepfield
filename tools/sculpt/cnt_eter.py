# The Eternal Commander, after art/rwar/c_eternal.webp (v856 remaster, the Continuum's crown jewel): four long swept blades in an X, the
# forward pair longer, each a polished black-chrome spine over a body of machinery sleeves banded in crimson light, tapering to a needle;
# they meet in a great arched hub whose heart is a red reactor cavity ribbed like a turbine, two red eyes beneath and a crown of fins above.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
M = Model((-4.3, -.9, -3.4), (5.0, 1.4, 3.4), float(sys.argv[2]) if len(sys.argv) > 2 else .026)
CHROME = {'c': (.13, .125, .13), 'r': .14, 'm': 1}; MACH = {'c': (.07, .066, .07), 'r': .3, 'm': .9}
HOT = {'c': (.25, .01, .015), 'r': .3, 'm': .1, 'e': (1.1, .03, .04)}
def rhomb(p, a, b, w0, w1, h0, h1, up=(0, 1, 0)):
    # a tapered segment with a diamond cross-section (sharp edges along its sides, a ridge along its top and keel): blade armour
    A = np.array(a, np.float32); B = np.array(b, np.float32); t = B - A; Ln = np.linalg.norm(t); t /= Ln; u = np.array(up, np.float32); u = u - t * (u @ t); u /= np.linalg.norm(u); s = np.cross(t, u)
    q = p - A; x = q @ t; y = q @ u; z = q @ s; k = np.clip(x / Ln, 0, 1); w = w0 + (w1 - w0) * k; h = h0 + (h1 - h0) * k
    d = (np.abs(z) / w + np.abs(y) / h - 1) * np.minimum(w, h) * .8
    return np.maximum(d, np.maximum(-x, x - Ln))
blades = [(.5, 5.2), (-.5, 5.2), (np.pi - .42, 4.3), (-(np.pi - .42), 4.3)]
for i, (th, L) in enumerate(blades):
    d = np.array((np.cos(th), 0, np.sin(th))); N = 6; W0, H0 = .46, .3
    P = [tuple(d * (.4 + (L - .4) * j / N) + np.array((0, .04 * j / N, 0))) for j in range(N + 1)]
    W = [W0 * (1 - j / N) ** .75 + .015 for j in range(N + 1)]; H = [H0 * (1 - j / N) ** .75 + .012 for j in range(N + 1)]
    for j in range(N):
        M.add(f'bd{i}{j}', lambda p, a=P[j], b=P[j + 1], w0=W[j], w1=W[j + 1], h0=H[j], h1=H[j + 1]: rhomb(p, a, b, w0, w1, h0, h1), MACH, .03)
        M.add(f'sp{i}{j}', lambda p, a=tuple(np.array(P[j]) + (0, H[j] * .55, 0)), b=tuple(np.array(P[j + 1]) + (0, H[j + 1] * .55, 0)), w0=W[j] * .35, w1=W[j + 1] * .35, h0=H[j] * .6, h1=H[j + 1] * .6: rhomb(p, a, b, w0, w1, h0, h1), CHROME, .02)
    for j in range(4):  # machinery sleeves along the inner half, a band of crimson light between each pair
        t0 = .1 + j * .1; c = np.array(P[0]) + (np.array(P[-1]) - np.array(P[0])) * t0; w = W0 * (1 - t0) ** .75 + .015; h = H0 * (1 - t0) ** .75 + .012
        M.add(f'sl{i}{j}', lambda p, a=tuple(c - d * .07), b=tuple(c + d * .07), w=w, h=h: rhomb(p, a, b, w * 1.14, w * 1.12, h * 1.14, h * 1.12), GUN, .008)
        cg = c + d * .12; wg = W0 * (1 - t0 - .025) ** .75 + .015; hg = H0 * (1 - t0 - .025) ** .75 + .012
        M.add(f'gl{i}{j}', lambda p, a=tuple(cg - d * .02), b=tuple(cg + d * .02), w=wg, h=hg: rhomb(p, a, b, w * 1.06, w * 1.06, h * 1.06, h * 1.06), HOT)
    sd = np.array((-np.sin(th), 0, np.cos(th)))
    for sdn in (1, -1):  # crimson light along each flank of the outer blade
        M.carve(f'ln{i}{sdn}', lambda p, a=tuple(np.array(P[0]) + d * L * .7 + sd * sdn * W0 * .25), b=tuple(np.array(P[0]) + d * L * .93 + sd * sdn * W0 * .06): cap(p, a, b, .025), RED)
# the hub: an arched crescent joining the blades, the reactor cavity at its heart
M.add('hub', lambda p: ell(p, (.05, .05, 0), (1.35, .45, .95)), CHROME, .25)
M.add('arch', lambda p: np.maximum(torus(p, (.25, .15, 0), 'y', .78, .2), -(.05 - p[..., 0])), CHROME, .08)

M.add('core', lambda p: sphere(p, (.4, .4, 0), .24), HOT)
for j in range(12):  # turbine ribs round the reactor
    a = j / 12 * 2 * np.pi; c = (.4 + .3 * np.cos(a), .36, .3 * np.sin(a))
    M.add(f'tr{j}', lambda p, c=c, a=a: box(p, c, (.07, .06, .02), .01, rot('y', -a)), GUN)
M.add('ring', lambda p: torus(p, (.4, .38, 0), 'y', .36, .04), HOT)
for j in range(3):  # a crown of fins over the hub
    z = (j - 1) * .3; M.add(f'fin{j}', lambda p, z=z: spike(p, (-.35, .35, z), (-1.1 - abs(z) * .4, .95 - abs(z) * .3, z * 1.3), .08), CHROME)
for s in (1, -1): eye(M, f'eye{s}', (.45, -.05, .62 * s), 'z', .22 * s)
engine(M, 'engA', -.95, 0, .3, .22, .4); engine(M, 'engB', -.95, 0, -.3, .22, .4)
M.carve('hubR', lambda p: np.maximum(ring(p, (.05, .05, 0), 'y', 1.05, .025, .5, .01), np.abs(ell(p, (.05, .05, 0), (1.35, .45, .95))) - .05), RED)
M.bake(sys.argv[1], lambda *a: paint(*a, sx=.45, sy=.35, sz=.45))
