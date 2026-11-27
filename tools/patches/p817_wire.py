"""v817: monsters closer to their card art (owner: build and refine the monsters to look closer to their card art). v816's wide rim
and strong reflections bleached the dark hides toward white; the cards are dark bodies laced with neon. So: the rim narrows and takes
each card's own vein colour, reflections come back down, glowing parts stay saturated instead of clipping white under ACES, and every
sculpted monster gets a network of glowing veins in its card's colour (blue cracks on the shark, cyan on the leviathan, violet on the
manta, magenta on the squid, gold on the moth). The Comet Ram is recoloured from blue ice to its card's bronze rock and orange lava."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 816;", "const GAME_V = 817;")
# the card palette: [vein colour, vein scale, vein threshold, vein strength], an optional albedo grade and emissive recolour
rep("const MON_WING = {", """const MON_CARD = { swhale: ["60, 150, 255", 2.6, .965, 1.1], slevi: ["40, 190, 255", 2.2, .96, 1.1], vmanta: ["150, 50, 255", 1.8, .955, 1.3, "", "", .55], ssquid: ["215, 45, 175", 3., .965, 1.],
  smoth: ["255, 120, 15", 3.4, .97, .8, "", "vec3(1., .5, .07) * 1.6"], cram: ["255, 95, 15", 2.4, .95, 1.6, "vec3(1.45, .95, .55) * 1.25", "vec3(1., .42, .09) * 1.8"] }; /* v817 */
const MON_WING = {""")
rep('totalEmissiveRadiance += vEm * 1.9; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 2.2); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .95; } /* v816 HDR glow and a rim of their own colour */',
    '" + monCardGlow(k, rgb) + "')
rep('.replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.05, vRM.x);")',
    '.replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.05, vRM.x);" + (MON_CARD[k] && MON_CARD[k][4] ? " diffuseColor.rgb = min(vec3(dot(diffuseColor.rgb, vec3(.3, .59, .11))) * " + MON_CARD[k][4] + ", vec3(.7));" : ""))')
rep("m.envMapIntensity = .7; m.onBeforeCompile = obc;", "m.envMapIntensity = .32; m.onBeforeCompile = obc;")
rep("function monBump(k) {", """/* v817 the glow: hot but saturated (no clip to white), a thin rim and a vein network in the card's colour */
function monCardGlow(k, rgb) { const c = MON_CARD[k], vc = (c ? c[0] : rgb.split(", ").map(v => Math.round(v * 255)).join(", ")).split(",").map(v => (+v / 255).toFixed(3)).join(", ");
  let g = "{ vec3 e = vEm; " + (c && c[5] ? "e = vec3(dot(e, vec3(.3, .59, .11))) * " + c[5] + "; " : "") + "e = max(mix(vec3(dot(e, vec3(.3, .59, .11))), e, 1.35), 0.) * " + (c && c[6] ? c[6] * 1.45 : 1.45).toFixed(2) + "; totalEmissiveRadiance += e;"
    + " float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 3.5); totalEmissiveRadiance += vec3(" + vc + ") * fr * .45;";
  if (c) g += ` vec3 vq = vMP * ${c[1].toFixed(2)}; float vn = mnV(vq) * .65 + mnV(vq * 2.1 + 7.) * .35; float vv = smoothstep(${c[2].toFixed(2)}, 1., 1. - abs(vn * 2. - 1.)); totalEmissiveRadiance += vec3(${vc}) * vv * ${c[3].toFixed(2)};`;
  return g + " } /* v817 card glow */"; }
function monBump(k) {""")
# the halo takes the same recolour and stays saturated (it is additive and skips tone mapping, so raw pale emissive read as cream/ice)
rep('diffuseColor.rgb = vEm * " + ({ smoth: ".26", cram: ".42" }[k] || ".85") + ";"); };',
    'vec3 e = vEm; " + (MON_CARD[k] && MON_CARD[k][5] ? "e = vec3(dot(e, vec3(.3, .59, .11))) * " + MON_CARD[k][5] + " * .6; " : "") + "diffuseColor.rgb = max(mix(vec3(dot(e, vec3(.3, .59, .11))), e, 1.6), 0.) * " + ({ smoth: ".12", cram: ".3" }[k] || ".6") + ";"); };')
rep('totalEmissiveRadiance += diffuseColor.rgb * " + (k === "smoth" ? "1.1" : "2.6") + " * smoothstep(',
    'totalEmissiveRadiance += diffuseColor.rgb * " + (k === "smoth" ? "vec3(2.4, 1.1, .2)" : "1.4") + " * smoothstep(')
open(p, "w", encoding="utf-8").write(s); print("ok")
