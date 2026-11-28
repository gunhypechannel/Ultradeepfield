"""v837: the Mimics remastered after the paintings: new head (armoured skull, crest, four slit eyes, cheek plates, two rows of fangs,
glowing throat), sharper bodies (ribbed conduits, chrome hook plates, seam light), an additive glow layer for every class, a slower
heartbeat pulse and stronger rim light, and the approved lore: a codex per class with her voice, and "The Living Alloy" in the Archives."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 836;", "const GAME_V = 837;")
rep('const MIM_SC = {"mstalk":{},"mhunt":{},"mharv":{},"massim":{},"mguard":{},"mtitan":{},"malpha1":{},"malpha2":{},"malpha3":{},"malpha4":{},"momega":{},"momegax":{},',
    'const MIM_SC = {"mstalk":{"g":1},"mhunt":{"g":1},"mharv":{"g":1},"massim":{"g":1},"mguard":{"g":1},"mtitan":{"g":1},"malpha1":{"g":1},"malpha2":{"g":1},"malpha3":{"g":1},"malpha4":{"g":1},"momega":{"g":1},"momegax":{"g":1},')
# the glow: a stronger cyan rim, and a slow double heartbeat running from the head back along the body
rep("totalEmissiveRadiance += vec3(.1, .55, .95) * fr * .32; }", "totalEmissiveRadiance += vec3(.1, .55, .95) * fr * .55; }")
rep('m.userData.pulse = "(1. + 1.5 * pow(.5 + .5 * sin(uMT * 3. - vMP.x * 1.2), 8.))"; m.customProgramCacheKey = () => "mimsculpt3";',
    'm.userData.pulse = "(1. + 1.5 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1), 10.) + .8 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1 - .9), 10.))"; m.customProgramCacheKey = () => "mimsculpt4";')
# the codex on each swarm card
rep("<em>From Stage ${CS[k]}</em></div></div>", "<em>From Stage ${CS[k]}</em>${MIM_LORE[k] ? `<details class=\"mxcod\"><summary>Codex</summary><p>${MIM_LORE[k][0]}</p><button class=\"btn\" data-act=\"mimLore\" data-k=\"${k}\">🔊 Her assessment</button></details>` : \"\"}</div></div>")
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p837_lore.js"), encoding="utf-8").read()
rep('ARCH_ORD.push("m_protocol", "m_alpha", "m_echo", "m_vault", "m_omega", "m_frag");', 'ARCH_ORD.push("m_protocol", "m_alpha", "m_echo", "m_vault", "m_omega", "m_frag");\n' + js)
open(p, "w", encoding="utf-8").write(s); print("ok")
