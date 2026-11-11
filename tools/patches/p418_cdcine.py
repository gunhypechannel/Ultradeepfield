# v418: the Cube Destroyer fires like the greatest ship in the game. One huge beam every 5 seconds per Cube Destroyer formation (cdPlan
# picks them from the replay's volleys: the first, then the next at least 5 s after the last), no flak spray between. Each shot is
# staged from the replay's own schedule: about 2 s of slow yaw onto the target, a 1.2 s charge in the dish, a 1.6 s beam that lands as
# the volley does (it starts 1.4 s before it), a wider beam and a bigger, longer splash, and the station holds its aim 1.5 s after.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
i = t.index('  worldbreaker:  ["flak", 3, "#ff3b30"'); j = t.index("\n", i) + 1; t = t[:i] + "  // v418 the Cube Destroyer has no second battery: its beam is the whole show\n" + t[j:]
rep("""if (q.k === "worldbreaker") { b.beams = b.beams.filter(m => m.s !== v.s || m.ht); b.beams.push({ t0: v.t, s: v.s, e: v.e, side, w: 12, charge: .5, life: .7, wb: 1 }); return; }""",
    """if (q.k === "worldbreaker") return; /* v418 its beams are staged ahead from the schedule (cdPlan) */""")
rep("""  b.beams = b.beams.filter(m => T - m.t0 <= m.charge + m.life + (m.wb ? 1 : 0));""",
    """  if (!b.cdQ) b.cdQ = cdPlan(b); while (b.cdQ.length && b.cdQ[0].t0 - 2.4 <= T) b.beams.push(b.cdQ.shift()); // v418 a staged shot joins 2.4 s ahead, so the station can turn onto it
  b.beams = b.beams.filter(m => T - m.t0 <= m.charge + m.life + (m.wb ? 3 : 0));""")
rep("const u = (T - m.ht) / .9;", "const u = (T - m.ht) / 1.3;")
rep("Rs = Math.max(W, H) * .2,", "Rs = Math.max(W, H) * .26,")
rep("w = Math.max(5 * d, Lg * .09)", "w = Math.max(6 * d, Lg * .13)")
rep("T - m.t0 > -.6 && T - m.t0 < m.charge + m.life);", "T - m.t0 > -2.2 && T - m.t0 < m.charge + m.life + 1.5);")
rep("A[i] = cur + d * Math.min(1, (real || 16) / 600); return A[i]; }", """A[i] = cur + d * Math.min(1, (real || 16) / 1100); return A[i]; }
/* v418 the Cube Destroyer's shots: one per formation every 5 s of the replay, each starting its charge 1.4 s before its volley so the beam lands with it */
function cdPlan(b) { const out = [], last = {}, ord = {}; let no = 0; for (const v of b.R.vols || []) { const q = b.Q[v.s]; if (!q || q.k !== "worldbreaker" || v.bounce || v.e == null || v.e < 0) continue; if (ord[v.s] == null) ord[v.s] = no++; if (v.t < ord[v.s] * 1.7) continue; /* formations take turns: a rolling barrage */ if (last[v.s] != null && v.t < last[v.s] + 5) continue; last[v.s] = v.t;
    out.push({ t0: Math.max(.3, v.t - 1.4), s: v.s, e: v.e, side: q.side, w: 12, charge: 1.2, life: 1.6, wb: 1 }); } return out.sort((x, y) => x.t0 - y.t0); }""")
t = t.replace("const GAME_V = 417;", "const GAME_V = 418;")
open(p, "w").write(t); print("ok")
