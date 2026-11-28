"""v845: the Mimics stop waving (owner: "i dont like how the mimics look like they are waving make their animitions slow or remove there
wiggle movement all together because it looks really unnatural and weird"). A sculpted Mimic now holds rigid: one slow float, a slight
nod and a breathing jaw, and only the outer tips of its long cables and tail sway a little, slowly."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 844;", "const GAME_V = 845;")
rep("  let w = `vec3 p = position; float ph = mt * ${W2};", '''  if (MIM_SC[k]) { const R0 = (MIM_SC[k] && MIM_RG[k]) || "0.", RJ = (MIM_SC[k] && MIM_RGJ[k]) || "0."; /* v845 rigid and heavy: no ripple along the body, no whipping cables */
    return `vec3 p = position; float rg = ${R0}, rgj = ${RJ}; transformed.y += .06 * sin(mt * ${W1});
    float hw = smoothstep(${f(1.25 * L)}, ${f(1.95 * L)}, p.x); transformed.y += hw * .025 * sin(mt * ${W1} + 1.2);
    float jw = smoothstep(${hx}, ${f(1.85 * L + .5)}, p.x) * step(p.y, ${f(.6 + (D.sac ? -.1 : 0))}) * (1. - rgj); transformed.y -= jw * (p.x - ${hx}) * (.03 + .03 * sin(mt * ${W1}));
    float dd = length(vec2(p.y - ${cy}, p.z)), tip = max(smoothstep(2.2, 3.6, dd) * step(-.05, p.y), smoothstep(${f(-4.0 * L)}, ${f(-6.0 * L)}, p.x)) * (1. - hw) * (1. - rg);
    transformed.z += tip * .07 * sin(mt * ${W1} - dd * .45); transformed.y += tip * .05 * sin(mt * ${W1} - dd * .35 + 1.);`; }
  let w = `vec3 p = position; float ph = mt * ${W2};''')
open(p, "w", encoding="utf-8").write(s); print("ok")
