"""v787: the hunt monsters toward their paintings, second pass (owner: "finish it up"). The Squid, Manta and Moth re-coloured in their
sculpts (tools/sculpt/mon_sculpt.py): the Nebula Squid wine-dark and glossy with ember-glowing eyes and spots; the Void Manta
indigo-black with eleven thin vivid violet veins a wing (and branches) and a burning orange leading edge; the Solar Moth's
membranes dark amber glowing from within, thirteen bright gold veins a wing; the Star Leviathan (tools/sculpt/mon2_sculpt.py) a blue
hide streaked with cyan light and brighter silver armour; the Comet Ram bronze rock split by fire-orange cracks, gold horns and a tail
of burning debris (was ice). v785's material (glossier, x1.7 glow, 2.7x the sky reflection)
washed the dark hides and gold glows toward pastel; the hunt monsters now render as sculpted again, keeping only a faint rim light in
their colour and the glow pulsing as they swim. Applies on top of v786."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 786;", "const GAME_V = 787;")
rep('.replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.04, vRM.x * .55);")', '.replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.05, vRM.x);")')
rep('"totalEmissiveRadiance += vEm * 1.7; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 3.); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .26; }"', '"totalEmissiveRadiance += vEm; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 4.); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .12; }"')
rep('m.envMapIntensity = .75; m.onBeforeCompile = obc;', 'm.envMapIntensity = .28; m.onBeforeCompile = obc;')
open(p, "w", encoding="utf-8").write(s)
print("ok")
