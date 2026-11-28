"""v836: Hunter, Harvester, Assimilator and Guardian re-sculpted after the owner's paintings (legless), their paintings on the cards,
and every Mimic class given its own signature attack (p836_atk.js)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 835;", "const GAME_V = 836;")
rep('const MIM_ART = { mstalk: "stalker", mtitan: "titan" };', 'const MIM_ART = { mstalk: "stalker", mtitan: "titan", mhunt: "hunter", mharv: "harvester", massim: "assimilator", mguard: "guardian" };')
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p836_atk.js"), encoding="utf-8").read()
rep("const MIM_TENT = { bite: 1, grab: 3, claw: 2, storm: 3 }; /* how many tentacles each attack throws */",
    "const MIM_TENT = { bite: 1, grab: 3, claw: 2, storm: 3 }; /* how many tentacles each attack throws */\n" + js)
# the bodies move with the new attacks
rep("if (!done.has(S0)) { const k = m.a === \"bite\" ||", "if (!done.has(S0)) { const k = MIMX_DUR[m.a] ? mimLK(m.a, u) : m.a === \"bite\" ||")
rep("if (k) { const reach = Math.min(dl * .35, Lg * .6);", "if (k) { const reach = MIMX_DUR[m.a] ? mimLR(m.a, dl, Lg) : Math.min(dl * .35, Lg * .6);")
rep("if (MIM_TENT[m.a] && u > .3 && !done.has(E0))", "if ((MIM_TENT[m.a] || m.a === \"drain\") && u > .3 && !done.has(E0))")
# their sounds and drawing
rep("if (!m.snd && u >= 0 && (m.a === \"omegaX\" || m.a === \"storm\")) bVoice(b, \"sig\");", "if (!m.snd && u >= 0 && MIMX_SND[m.a]) { m.snd = 1; mimSfx(MIMX_SND[m.a], pan); } if (!m.snd && u >= 0 && (m.a === \"omegaX\" || m.a === \"storm\")) bVoice(b, \"sig\");")
rep("    if (MIM_TENT[m.a] && alive) { /* tentacles:", "    if (MIMX_DUR[m.a]) { if (alive) mimAtkX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan); }\n    else if (MIM_TENT[m.a] && alive) { /* tentacles:")
# the rigid parts of the new sculpts do not writhe like the cables: the Guardian's shields, the Assimilator's wheels and stolen hull, the Hunter's scythes
rep("function mimWave(k) {", '''const MIM_RG = { mguard: "smoothstep(1.4, 1.7, abs(p.z))", massim: "max(smoothstep(1.4, 1.55, abs(p.z)) * (1. - smoothstep(1.35, 1.6, length(vec2(p.x - .17, p.y - 1.66)))), smoothstep(2.05, 2.25, p.y) * (1. - smoothstep(1.1, 1.4, abs(p.x + .6))) * (1. - smoothstep(.75, .95, abs(p.z - .15))))", mhunt: "smoothstep(1.9, 2.3, p.x) * (1. - smoothstep(.3, .6, p.y))" };
const MIM_RGJ = { mhunt: "smoothstep(.72, .86, abs(p.z))" };
function mimWave(k) {''')
rep("let w = `vec3 p = position; float ph = mt * ${W2};`;", "let w = `vec3 p = position; float ph = mt * ${W2}; float rg = ${(MIM_SC[k] && MIM_RG[k]) || \"0.\"}, rgj = ${(MIM_SC[k] && MIM_RGJ[k]) || \"0.\"};`;")
rep("transformed.y -= jw * (p.x - ${hx}) * (.1 + .12 * sin(mt * ${W1} * 2.));", "transformed.y -= jw * (1. - rgj) * (p.x - ${hx}) * (.1 + .12 * sin(mt * ${W1} * 2.));")
rep("smoothstep(${tl}, ${te}, p.x)) * (1. - lw) * (1. - hw);", "smoothstep(${tl}, ${te}, p.x)) * (1. - lw) * (1. - hw) * (1. - rg);")
open(p, "w", encoding="utf-8").write(s); print("ok")
