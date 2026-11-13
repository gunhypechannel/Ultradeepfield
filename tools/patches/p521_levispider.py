# v521 the Star Leviathan made to match its card (an armoured space whale with cyan throat grooves and hide cracks, a bone-spike ridge,
# long pectoral fins and flukes; it swims with whale strokes and its glow breathes; its colour is now cyan) and a far scarier Gravity
# Spider (plated armour with magenta seams, a banded spiked abdomen, a caged singularity whose rings spin, a purple core eye ringed by
# six, fangs that work, palps, and eight four-jointed legs that walk in a tetrapod gait; every so often it rears up on its back legs).
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p521_levispider.js'), encoding='utf-8').read()
part = lambda name: J.split('//@@' + name + '\n')[1].split('//@@')[0]
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''  return C;
}
const MONM = {};''', part('MATS') + '''  return C;
}
const MONM = {};''')
def swap(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
swap('  } else if (k === "slevi") {', '  } else if (k === "ssquid") {', part('LEVI'))
swap('  } else if (k === "gspider") {', '  } else if (k === "smoth") {', part('SPIDER'))
def wave(k, code):
    global s
    i = s.index('  ' + k + ': "', s.index('const MON_WAVE')); j = s.index('",\n', i) + 3; s = s[:i] + '  ' + k + ': "' + code + '",\n' + s[j:]
wave('slevi', 'float su = clamp((1.5 - position.x) / 6.3, 0., 1.); transformed.y += (.04 + .95 * su * su) * sin(position.x * .55 + mt * 1.5) - .04 * sin(mt * 1.5); float fz = abs(position.z), fin = smoothstep(1.15, 3.6, fz) * step(position.y, -.2) * step(0., position.x); transformed.y += fin * .6 * sin(mt * 1.1) * (fz - 1.1) / 2.5; transformed.x += fin * .15 * cos(mt * 1.1);')
wave('gspider', 'vec3 p = position; float w = smoothstep(1.05, 2.9, abs(p.z)), a = atan(p.x - .45, abs(p.z)), ph = a * 3.3 + (p.z > 0. ? 0. : 3.1416); transformed.y += w * .42 * max(0., sin(mt * 4.2 + ph)); transformed.x += w * .3 * cos(mt * 4.2 + ph); float rear = pow(max(0., sin(mt * .5)), 10.); transformed.y += rear * w * smoothstep(.25, .85, a) * 1.7 + rear * smoothstep(-1., 1.6, p.x) * .35; transformed.y += .04 * sin(mt * 8.4); if (p.x > 1.6 && p.y < .08 && abs(p.z) < .3) transformed.z += sign(p.z) * .07 * (.5 + .5 * sin(mt * 7.)); if (p.x < -.4 && w < .05 && p.y < 1.75) transformed.y += .05 * sin(mt * 2.) * (p.y - .55); vec3 cq = p - vec3(-1.7, 1.98, 0.); float cd = length(cq); if (cd > .5 && cd < .95 && p.y > 1.35) { float th = mt * 1.6; vec2 r2 = vec2(cq.x * cos(th) - cq.z * sin(th), cq.x * sin(th) + cq.z * cos(th)); transformed.x = -1.7 + r2.x; transformed.z = r2.y; }')
rep('slevi:  { n: "Space Leviathan", sp: "Star Leviathan", ic: "🐉", col: "#ff8a4a", rgb: "255,138,74", per: 10, d: "An armoured serpent that feeds on fleets. Molten light runs along its scales and its jaws can split a battleship.",',
    'slevi:  { n: "Space Leviathan", sp: "Star Leviathan", ic: "🐋", col: "#5ac8ff", rgb: "90,200,255", per: 10, d: "An armoured whale the size of a dreadnought. Starlight runs in the grooves of its throat and the cracks of its hide, and its jaws can split a battleship.",')
rep('slevi: "255,138,74"', 'slevi: "90,200,255"')
rep('slevi: [255, 138, 74]', 'slevi: [90, 200, 255]')
s2 = re.sub(r"GAME_V = 520\b", "GAME_V = 521", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
