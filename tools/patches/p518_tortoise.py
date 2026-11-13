# v518 the Crystal Tortoise remastered (owner: "high definition and detailed with blue glyph shell and more animatronic features").
# A new model (p518_tortoise.js): rune-carved scutes with blue seams and a bump map, marginal plates, spine and flank crystal prisms,
# columned legs with claws, a horn-beaked head on a folded neck. On the map it walks (diagonal legs in step, the body bobbing), looks
# about, opens its jaw on a blue glow, sways its tail, and its runes and crystals pulse. monAnimate gains a per-material emissive
# pulse (material.userData.pulse, a GLSL expression in uMT).
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p518_tortoise.js'), encoding='utf-8').read()
part = lambda name: J.split('//@@' + name + '\n')[1].split('//@@')[0]
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''  return C;
}
const MONM = {};''', part('MATS') + '''  return C;
}
const MONM = {};''')
i = s.index('  } else if (k === "ctort") {'); j = s.index('  } else if (k === "gspider") {')
s = s[:i] + part('MODEL') + s[j:]
i = s.index('  ctort: "', s.index('const MON_WAVE')); j = s.index('",\n', i) + 3
s = s[:i] + '''  ctort: "vec3 p = position; float lw = 1. - smoothstep(-.6, -.3, p.y), nr = 1. - smoothstep(.55, .85, length(vec2(abs(p.x) - 1.45, abs(p.z) - 1.25))), ph = mt * 1.7 + (sign(p.x) * sign(p.z) > 0. ? 0. : 3.1416); transformed.x += lw * nr * (-.3 - p.y) * .5 * sin(ph); transformed.y += lw * nr * .1 * max(0., cos(ph)); transformed.y += .035 * sin(mt * 3.4); if (p.x > 2.74 && p.y < .02) { float jo = .38 * pow(max(0., sin(mt * .42)), 6.), dx = p.x - 2.74; transformed.y -= dx * sin(jo); transformed.x -= dx * (1. - cos(jo)); } float hw = smoothstep(1.9, 2.6, p.x), yaw = .3 * sin(mt * .45) * hw; vec2 q = transformed.xz - vec2(1.9, 0.); transformed.xz = vec2(1.9, 0.) + vec2(q.x * cos(yaw) - q.y * sin(yaw), q.x * sin(yaw) + q.y * cos(yaw)); transformed.y += hw * .07 * sin(mt * .9) * (p.x - 1.9); float tw = clamp((-2.2 - p.x) / .65, 0., 1.); transformed.z += tw * .2 * sin(mt * 1.3);",
''' + s[j:]
rep('''      m.customProgramCacheKey = () => "monwave-" + kind; done.set(o.material, m); } o.material = m; }); }''',
    '''      const pu = m.userData && m.userData.pulse; if (pu) { const vb = m.onBeforeCompile; m.onBeforeCompile = sh => { vb(sh); sh.fragmentShader = "uniform float uMT;\\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\\n totalEmissiveRadiance *= " + pu + ";"); }; } /* v518 glow that breathes */
      m.customProgramCacheKey = () => "monwave-" + kind + (pu ? "-p" + hash(pu) : ""); done.set(o.material, m); } o.material = m; }); }''')
s2 = re.sub(r"GAME_V = 517\b", "GAME_V = 518", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
