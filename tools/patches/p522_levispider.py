# v522 the Star Leviathan made longer and eel-like (owner) with its card's armoured whale head: a plated skull with cyan throat grooves
# and a toothed jaw that opens, a long ringed eel body cracked with cyan light, a spike ridge turning into a glowing fin down the tail;
# it swims in a serpentine wave and its glow breathes; its colour is now cyan and a far scarier Gravity
# Spider (plated armour with magenta seams, a banded spiked abdomen, a caged singularity whose rings spin, a purple core eye ringed by
# six, fangs that work, palps, and eight four-jointed legs that walk in a tetrapod gait; every so often it rears up on its back legs).
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p522_levispider.js'), encoding='utf-8').read()
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
wave('slevi', 'float tl = clamp((3.2 - position.x) / 11.8, 0., 1.); transformed.z += (.12 + .85 * tl) * sin(position.x * .62 + mt * 2.4); transformed.y += .2 * tl * sin(position.x * .4 + mt * 1.6); if (position.x > 3.2 && position.y < -.45) { float jo = .45 * pow(max(0., sin(mt * .5)), 4.), dx = position.x - 3.2; transformed.y -= dx * sin(jo); transformed.x -= dx * (1. - cos(jo)); }')
wave('gspider', 'vec3 p = position; float w = smoothstep(1.05, 2.9, abs(p.z)), a = atan(p.x - .45, abs(p.z)), ph = a * 3.3 + (p.z > 0. ? 0. : 3.1416); transformed.y += w * .42 * max(0., sin(mt * 4.2 + ph)); transformed.x += w * .3 * cos(mt * 4.2 + ph); float rear = pow(max(0., sin(mt * .5)), 10.); transformed.y += rear * w * smoothstep(.25, .85, a) * 1.7 + rear * smoothstep(-1., 1.6, p.x) * .35; transformed.y += .04 * sin(mt * 8.4); if (p.x > 1.6 && p.y < .08 && abs(p.z) < .3) transformed.z += sign(p.z) * .07 * (.5 + .5 * sin(mt * 7.)); if (p.x < -.4 && w < .05 && p.y < 1.75) transformed.y += .05 * sin(mt * 2.) * (p.y - .55); vec3 cq = p - vec3(-1.7, 1.98, 0.); float cd = length(cq); if (cd > .5 && cd < .95 && p.y > 1.35) { float th = mt * 1.6; vec2 r2 = vec2(cq.x * cos(th) - cq.z * sin(th), cq.x * sin(th) + cq.z * cos(th)); transformed.x = -1.7 + r2.x; transformed.z = r2.y; }')
rep('slevi:  { n: "Space Leviathan", sp: "Star Leviathan", ic: "🐉", col: "#ff8a4a", rgb: "255,138,74", per: 10, d: "An armoured serpent that feeds on fleets. Molten light runs along its scales and its jaws can split a battleship.",',
    'slevi:  { n: "Space Leviathan", sp: "Star Leviathan", ic: "🐉", col: "#5ac8ff", rgb: "90,200,255", per: 10, d: "A sea serpent as long as a fleet, with the armoured head of a whale. Starlight runs in the cracks of its hide, and its jaws can split a battleship.",')
rep('slevi: "255,138,74"', 'slevi: "90,200,255"')
rep('slevi: [255, 138, 74]', 'slevi: [90, 200, 255]')
rep('C.gring = new TH.MeshBasicMaterial({ color: 0x9a5cff, transparent: true, opacity: .75,', 'C.gring = new TH.MeshBasicMaterial({ color: 0x7a3cff, transparent: true, opacity: .5,')
rep('if (k === "eclipse" && view === "side") ship.rotation.x = .42;', 'if (k === "eclipse" && view === "side") ship.rotation.x = .42; if (k === "smoth" && view === "side") ship.rotation.x = 1.15; /* v522 the Solar Moth shows its wings in battle, not their edge */')
s2 = re.sub(r"GAME_V = 521\b", "GAME_V = 522", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
