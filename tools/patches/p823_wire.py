"""v823: the Eclipse Harbinger, more of it: ten new lines and the Eclipse Cage (see p823_harb.js)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p823_harb.js"), encoding="utf-8").read()
rep("const GAME_V = 822;", "const GAME_V = 823;")
rep("/* tell the defender's radar that a fleet is coming */", C + "\n/* tell the defender's radar that a fleet is coming */")
# every 4th main volley of a Harbinger (3rd when awakened) is the Cage; the damage lands when the cage closes on the point
rep('if (q.k === "harbinger" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "HP", charge: 0, life: 1.45, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .92 })); try { SFX.charge && SFX.charge(); } catch (e) {} return true; } /* v595 */',
    'if (q.k === "harbinger" && main) { const hc = b.hc823 || (b.hc823 = {}), nH = hc[v.s] = (hc[v.s] || 0) + 1, cage = nH % (S && S.choices && S.choices.harb === "wake" ? 3 : 4) === 0; /* v823 the Eclipse Cage */\n    b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: cage ? "HC" : "HP", charge: 0, life: cage ? 2.3 : 1.45, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + (cage ? 1.5 : .92) })); try { SFX.charge && SFX.charge(); } catch (e) {} return true; } /* v595 */')
open(p, "w", encoding="utf-8").write(s); print("ok")
