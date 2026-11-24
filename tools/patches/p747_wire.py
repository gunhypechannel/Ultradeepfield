"""v747: the finale's map scene draws less: the three anchors use the sculpted relay (one draw each, swapped in when it finishes
loading; the hand-built fallback is merged by material), and its explosion, shockwave and flash sprites are drawn only while lit."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 746;", "const GAME_V = 747;")
rep("""    for (let i = 0; i < 3; i++) { const a = buildCnt("cnrel"); a.scale.setScalar(.85); a.traverse(q => { q.userData.keep = 1; }); G0.add(a); X.anc.push(a);""",
    """    X.ancSc = !!CNT_GEO.cnrel; for (let i = 0; i < 3; i++) { const a = cntAnc(); G0.add(a); X.anc.push(a);""")
rep("""  /* the shield while the anchors stand, the anchors themselves and their beams */""",
    """  /* v747 the sculpted relay arrived after the scene was built: swap the anchors over */
  if (!X.ancSc && CNT_GEO.cnrel) { X.ancSc = 1; X.anc = X.anc.map(a => { const b = cntAnc(); X.grp.add(b); X.grp.remove(a); a.traverse(q => { if (q.userData.mg) q.geometry.dispose(); }); return b; }); }
  /* the shield while the anchors stand, the anchors themselves and their beams */""")
rep("""X.grp.traverse(q => { if (q.geometry && !q.userData.keep) q.geometry.dispose();""", """X.grp.traverse(q => { if (q.geometry && (!q.userData.keep || q.userData.mg)) q.geometry.dispose();""")
# sprites that are fully faded are not drawn at all
rep("""  for (const b of X.booms) { const k = (t - b.t0) / 900; b.s.material.opacity = k >= 0 && k < 1 ? (1 - k) * .9 : 0; b.s.scale.setScalar(4 + k * 10); }""",
    """  for (const b of X.booms) { const k = (t - b.t0) / 900; b.s.material.opacity = k >= 0 && k < 1 ? (1 - k) * .9 : 0; b.s.visible = b.s.material.opacity > .005; b.s.scale.setScalar(4 + k * 10); }""")
rep("""X.flash.scale.setScalar(60 + w * 80); }""",
    """X.flash.scale.setScalar(60 + w * 80); X.wave.visible = X.wave.material.opacity > .005; X.flash.visible = X.flash.material.opacity > .005; X.gate.visible = X.gate.material.opacity > .005; X.swirl.visible = X.swirl.material.opacity > .005; }""")
rep("""/* War Command's finale card */""",
    """/* v747 one finale anchor: the sculpted relay (a single draw), or the hand-built one merged by material until it loads */
function cntAnc() { const a = buildCnt("cnrel"); if (CNT_GEO.cnrel) { a.scale.setScalar(.85); a.traverse(q => { q.userData.keep = 1; }); return a; }
  const g = mergeGroup(a); g.scale.setScalar(.85); g.traverse(q => { q.userData.keep = 1; if (q.isMesh && !q.userData.sculpt) q.userData.mg = 1; }); return g; }
/* War Command's finale card */""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
# the cinematic caption named a target twice when its name is its species' name ("The Prime Resurrection Ark · The Prime Resurrection Ark")
s = open(p, encoding="utf-8").read()
a = """: id[0] === "y" ? "▲ Pyramid station" : "☠ Pirate hideout"} · ${it.name} · Lv.${it.lvl}`;"""
assert s.count(a) == 1
s = s.replace(a, """: id[0] === "y" ? "▲ Pyramid station" : "☠ Pirate hideout"}${it.mon && MON[it.mon] && MON[it.mon].n === it.name ? "" : " · " + it.name} · Lv.${it.lvl}`;""")
open(p, "w", encoding="utf-8").write(s)
print("caption ok")
