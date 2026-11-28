"""v863: the Kraken remastered (see p863_krak.js; the sculpt tools/sculpt/crc_kraken.py)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 862;", "const GAME_V = 863;")
# its scale, its slow writhe
rep("ckrak: 2.8, cfrig: 1.15,", "ckrak: 6.6, cfrig: 1.15,")
rep("ckrak: 2.6, cfrig: 1.7,", "ckrak: 4.6, cfrig: 1.7,")
rep("transformed.y += ar * ar * .55 * sin(mt * 2.0944 + p.x * 1.3 + p.z * 2.2); transformed.z += ar * ar * .45 * cos(mt * 2.0944 + p.x * 1.1 + p.y * 1.7);\n    float mn = smoothstep(.2, -2.5, p.x); transformed.yz *= 1. + mn * .05 * sin(mt * 4.18879); transformed.y += .08 * sin(mt * 2.0944);`;",
    "transformed.y += ar * ar * .42 * sin(mt * 1.0472 + p.x * 1.1 + p.z * 2.); transformed.z += ar * ar * .36 * cos(mt * 1.0472 + p.x * .9 + p.y * 1.5);\n    float mn = smoothstep(.2, -2.5, p.x); transformed.yz *= 1. + mn * .04 * sin(mt * 2.0944); transformed.y += .08 * sin(mt * 1.0472);`; /* v863 slower */")
# its own attacks instead of the crabs' grab and the ships' pulse
rep('ckrak: "grab", ckbr: "grab" });', 'ckbr: "grab" }); /* v863 the Kraken has its own */')
rep('ckrak: ["pulse", "crush"]', 'ckrak_old: ["pulse", "crush"]')
# the story: the Carcinid have chained it again (owner: "for the crab army to be able to control something like that")
rep('d: "The Kraken has come back up from the Abyss, wild now, its Carcinid riders gone. It drifts through the deep layers and drags down anything that strays close.',
    'd: "The Kraken has come back up from the Abyss, and the Carcinid have chained it again: bolted armour on its mantle, a harness of coral, and a control spire driven into its head, its riders steering it through the deep layers to drag down anything that strays close.')
rep('ckrak: ["The Kraken, back from the Abyss. Wild now, and in the deep layers for good.", "Wild"]', 'ckrak: ["The Kraken, back from the Abyss and bound again: the Carcinid steer it from a spire in its head.", "Bound"]')
js = open(__file__.rsplit('/', 1)[0] + "/p863_krak.js", encoding="utf-8").read()
rep("/* the Eternal Commander's five */", js + "/* the Eternal Commander's five */")
rep("try { cntAtkAdd(b, v); } catch (e) {} /* v856 */", "try { cntAtkAdd(b, v); } catch (e) {} /* v856 */ try { krakAtkAdd(b, v); } catch (e) {} /* v863 */")
rep("cntPrimeFx(ctx, b, scr, T, W, H, d, t); cntDread(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v856, v861 */", "cntPrimeFx(ctx, b, scr, T, W, H, d, t); cntDread(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v856, v861 */ try { krakAtkDraw(ctx, b, scr, T, W, H, d, t); krakFx(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v863 */")
open(p, "w", encoding="utf-8").write(s); print("ok")
