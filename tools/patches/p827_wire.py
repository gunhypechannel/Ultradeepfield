"""v827: the Celestial Serpent's face, refined after the painting (owner: "how can we refine and improve the mouth and face design even
further?" then "lets build it"). The sculpt (tools/sculpt/mon3_sculpt.py serpent, art/mon/m/cserp.bin) now has a viper's head: a rounded
wedge with a flat crown and broad cheeks, plated in gold with dark seams and a centre ridge, violet slit-pupilled eyes under jutting gold
brows, gold lips over a lit mouth slit with a snarl at the corner, long front fangs, a separate lower jaw with a gold chin plate, cheek
plates and nostrils. Here the swim wave opens that jaw slowly: every vertex of the lower jaw (below the mouth line, inside the upper
teeth) turns about the hinge, up to about 16 degrees, opening for ~2 s every ~10 s on the map and once per 6 s battle loop (mbfQ keeps
the .6 rate at one cycle per loop). The head frame (H0 2.6,1.75,.01; hx, hy; scale 1.6) is mon3_sculpt.SERP_JAW."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 826;", "const GAME_V = 827;")
rep('''  cserp: "vec3 p = position; float sv''', '''  cserp: "{ vec3 jq = position - vec3(2.6, 1.75, .01); float jx = dot(jq, vec3(.9989, -.0362, -.0288)) / 1.6, jy = dot(jq, vec3(.0362, .9993, -.001)) / 1.6, jz = dot(jq, vec3(.0288, 0., .9996)) / 1.6; float jm = step(jy, -.1865 + .0625 * jx) * step(abs(jz), .84 * (.33 + .325 * clamp(jx + .5, 0., .4) - .05 * clamp(jx + .1, 0., .4) - .175 * clamp(jx - .3, 0., .8) - .2 * clamp(jx - 1.1, 0., .35) - .36 * clamp(jx - 1.45, 0., .25) - clamp(jx - 1.7, 0., .1))) * step(-.75, jy) * step(jx, 1.8) * smoothstep(-.52, -.22, jx), ja = jm * .28 * pow(max(0., sin(mt * .6 - 1.)), 3.); vec2 jd = vec2(jx + .35, jy + .17), jr = vec2(jd.x * cos(ja) + jd.y * sin(ja), jd.y * cos(ja) - jd.x * sin(ja)); transformed += (vec3(.9989, -.0362, -.0288) * (jr.x - jd.x) + vec3(.0362, .9993, -.001) * (jr.y - jd.y)) * 1.6; } vec3 p = position; float sv''')
open(p, "w", encoding="utf-8").write(s); print("ok")
