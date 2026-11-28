"""v855: the Carcinid bosses remastered: new sculpts with glow layers, a wet glowing material, water effects, a slow walk, an Advisor line
(see p855_crc.js; models from tools/sculpt/crc_boss.py)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 854;", "const GAME_V = 855;")
js = open(__file__.rsplit('/', 1)[0] + "/p855_crc.js", encoding="utf-8").read()
rep("function buildCarc(k) { crcSculptLoad(k);", js + "function buildCarc(k) { crcSculptLoad(k);")
rep("function crcSculpted(k) { const D = CRC_SC[k], g = new TH.Group(), m = new TH.Mesh(CRC_GEO[k], cntMeshMat());",
    "function crcSculpted(k) { const D = CRC_SC[k], g = new TH.Group(), m = new TH.Mesh(CRC_GEO[k], CRC_BK.has(k) ? crcBossMat(k) : cntMeshMat()); /* v855 */")
# the slow, heavy walk: a step every three seconds (six in battle frames), the claws rising and settling slowly, the body sinking with each step
rep("float ph = mt * 6.28318 + p.x * 2.6", "float ph = mt * 2.0944 + p.x * 2.6")
rep("transformed.y += cl * (.09 * sin(mt * 2.0944 + (p.z > 0. ? 0. : 1.6)) + .05 * (p.x - 1.3) * sin(mt * 4.18879));", "transformed.y += cl * (.11 * sin(mt * 1.0472 + (p.z > 0. ? 0. : 1.6)) + .05 * (p.x - 1.3) * sin(mt * 2.0944));")
rep("transformed.x += tu * .05 * sin(mt * 2.0944 + p.y * 1.4); transformed.z += tu * .04 * cos(mt * 2.0944 + p.y);", "transformed.x += tu * .05 * sin(mt * 1.0472 + p.y * 1.4); transformed.z += tu * .04 * cos(mt * 1.0472 + p.y);")
rep("transformed.y += tl * .1 * sin(mt * 4.18879 + p.x * 1.6);\n    transformed.y += (1. - lz) * .045 * sin(mt * 4.18879);`;", "transformed.y += tl * .1 * sin(mt * 2.0944 + p.x * 1.6);\n    transformed.y -= (1. - lz) * .06 * abs(sin(mt * 2.0944));`;")
# battle: the bosses' light and water, their attacks, the Advisor's line
rep("if (!lo) try { mimAmbient(ctx, b, scr, T, d); mimGlow(ctx, b, scr, T, d); } catch (e) {}", "if (!lo) try { mimAmbient(ctx, b, scr, T, d); mimGlow(ctx, b, scr, T, d); } catch (e) {} if (!lo) try { crcBossFx(ctx, b, scr, T, d); } catch (e) {} try { crcBossAtk(ctx, b, scr, T, d); crcWalkSay(b); } catch (e) {}")
rep("if (alive && u < .25 && !/^(synapse|command|adapt)$/.test(m.a)) mimCharge(", "if (alive && u < .25 && !/^(synapse|command|adapt)$/.test(m.a) && !CRC_BK.has(b.Q[m.s].k)) mimCharge(")
open(p, "w", encoding="utf-8").write(s); print("ok")
