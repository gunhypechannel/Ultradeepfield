# v612 (part two, applied after p612_story.py): owner, 2026-11-17: "Remove crystal tortoise monster, remove leviathan monster, remaster
# celestial serpents swimming/movement animations to be more real."
# (1) The Crystal Tortoise and the Star Leviathan (the roaming space monster, not the Leviathan Warden of the Ten Seals) leave the map and
#     the Bestiary; their spots become open space, so no address moves; a fleet already on its way turns home (pirateArrive).
# (2) The Celestial Serpent swims like an eel: its spine is modelled nearly straight and a travelling wave runs head to tail, faster than it
#     moves forward, small at the head and growing to a full tail sweep; it surges forward on each beat of its tail.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW, MON_SP);',
    'const monGone = x => x.mon === "slevi" || x.mon === "ctort"; /* v612 the Star Leviathan and the Crystal Tortoise are retired */\nconst PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW, MON_SP).filter(x => !monGone(x));')
rep('"b_swhale", "b_slevi", "b_ssquid", "b_vmanta", "b_swasp", "b_ctort", "b_gspider"', '"b_swhale", "b_ssquid", "b_vmanta", "b_swasp", "b_gspider"')
# the serpent: a nearly straight spine (the swim makes the curves now)
rep('const r = rnd(7965), pts = [[2.6, 1.55, .1], [2.1, 1.35, .3], [1.5, .62, .75], [.7, -.1, .45], [0, -.2, -.5], [-.8, .3, -.8], [-1.6, .45, .1], [-2.2, 0, .8], [-2.9, -.25, .2], [-3.5, .1, -.5], [-4.1, .15, -.1], [-4.6, 0, .25], [-4.95, -.02, .2]];',
    'const r = rnd(7965), pts = [[2.6, 1.55, .01], [2.1, 1.35, .03], [1.5, .62, .06], [.7, -.05, .04], [0, -.12, -.04], [-.8, .12, -.06], [-1.6, .2, 0], [-2.2, .02, .06], [-2.9, -.1, .02], [-3.5, .04, -.04], [-4.1, .06, -.01], [-4.6, 0, .02], [-4.95, -.02, .02]]; /* v612 straightened: the swim bends it */')
a = s.index('  cserp: "vec3 p = position; float tl = clamp((2.2 - p.x) / 7.2, 0., 1.);'); b = s.index('\n', a)
s = s[:a] + '  cserp: "vec3 p = position; float sv = clamp((2.7 - p.x) / 7.65, 0., 1.), A = .1 + .72 * pow(sv, 1.25), ph = p.x * 1.08 + mt * 4.4; transformed.z += A * sin(ph); transformed.y += .06 * sv * sin(ph * .5 + mt * 1.1); float hd = smoothstep(1.7, 3.4, p.x); transformed.y += hd * .07 * sin(mt * .9); transformed.z -= hd * .05 * sin(mt * 4.4 + 2.);", /* v612 an eel\'s travelling wave, head to tail */' + s[b:]
rep('cserp: .00035, vmanta:', 'cserp: .00027, vmanta:')
rep('a = t * sp + it.a0 * 9, RX = 7.5,', 'a = t * sp + it.a0 * 9 + (it.mon === "cserp" ? -sp * 30 * Math.cos(t * .0088 + it.a0) : 0) /* v612 the serpent surges on each tail beat */, RX = 7.5,')
open(P, 'w', encoding='utf-8').write(s); print('ok')
