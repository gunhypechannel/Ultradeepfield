"""v750: live event units hold their spot. The Continuum's ships (patrols, platforms, relays, Arks, commanders), the Mimics and the
Carcinid (patrols, the Kraken, the bosses) no longer swim the monsters' two-slot figure-eight, and are no longer shoved about by passing
planets (v619's avoidance): each hangs at its own place, bobbing gently and turning slowly, so it stays where you tapped it. Other
monsters swim as before, and still steer round the event units."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 749;", "const GAME_V = 750;")
rep("""        if (it.mon === "swasp") { o.body.position.set(0, Math.sin(t * .0005 + it.a0) * .3, 0); o.body.rotation.set(0, t * .00008 + it.a0, 0); }""",
    """        if (it.mon === "swasp") { o.body.position.set(0, Math.sin(t * .0005 + it.a0) * .3, 0); o.body.rotation.set(0, t * .00008 + it.a0, 0); }
        const evStay = !!(MIM_BOSS[it.id] || CNT_M[it.mon] || CRC_M[it.mon] || it.mon === "mimic"); /* v750 an event unit holds its spot */
        if (evStay && !MIM_BOSS[it.id] && it.mon !== "mimic" && it.mon !== "carcinid") { o.body.position.set(0, Math.sin(t * .0004 + it.a0) * .2, 0); o.body.rotation.set(0, it.a0 + Math.sin(t * .00006 + it.a0 * 3) * .5, 0); }""")
rep("""if ((!down || inClash) && it.cnt !== "prime") monAvoid(W, o, q);""",
    """if ((!down || inClash) && it.cnt !== "prime") { if (evStay) { o.av = null; if (W.obG) obAdd(W.obG, q.x, q.y, q.z, 1.6 * (o.grp.scale.x || 1)); } else monAvoid(W, o, q); }""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
