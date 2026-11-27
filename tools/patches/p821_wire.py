"""v821: the Cube Destroyer holds its post again (owner video: "Cube destroyer is moving once again", a replay against a Cube boss: the
Destroyer crossed the whole field). Cause: v531/v659's post was skipped whenever the battle has a boss side (b.superSide, set for the
Cube's boss forms, super bosses and world bosses), so against exactly those foes it floated with the layout; and which edge is its rear
was worked out afresh every frame from the fleets' average positions, so it could flip to the other edge. Now the post holds unless the
Destroyer is itself on the boss side, and its edge (side-on or top/bottom, which end) is decided once per battle."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 820;", "const GAME_V = 821;")
rep('if (!b.superSide) for (const p of P) { const q = Q[p.i]; if (q.k !== "worldbreaker") continue; /* v531 the Cube Destroyer holds the rear */',
    'for (const p of P) { const q = Q[p.i]; if (q.k !== "worldbreaker" || b.superSide === q.side) continue; /* v531 the Cube Destroyer holds the rear; v821 against bosses too */')
rep("const cd = b.cdA || (b.cdA = {}), ca = cd[p.i] || (cd[p.i] = { x: ox, y: my }), ck = Math.min(1, real / 9000); ca.x += (ox - ca.x) * ck; ca.y += (my - ca.y) * ck; /* v659 a steady post: drifts, never slides */",
    "const cd = b.cdA || (b.cdA = {}), ca = cd[p.i] || (cd[p.i] = { x: ox, y: my, v: vert, e: vert ? (ne ? my >= ey : q.side === \"a\") : (ne ? ox <= ex : q.side === \"a\") }), ck = Math.min(1, real / 9000); ca.x += (ox - ca.x) * ck; ca.y += (my - ca.y) * ck; /* v659 a steady post: drifts, never slides; v821 its edge chosen once */")
rep('if (vert) { const down = ne ? my >= ey : q.side === "a"; p.y = down ?', 'if (ca.v) { const down = ca.e; p.y = down ?')
rep('else { const left = ne ? ox <= ex : q.side === "a"; p.x = left ?', 'else { const left = ca.e; p.x = left ?')
open(p, "w", encoding="utf-8").write(s); print("ok")
