"""v846: the Neural Node, Neural Nexus and Assimilation Pylon remastered (tools/sculpt/mon4_sculpt.py mnode/mpylon, mon3_sculpt.py nexus),
each with its own attack, tethers to Omega in its battle, calm motion, and a codex card with her voice (p846_atk.js)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 845;", "const GAME_V = 846;")
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p846_atk.js"), encoding="utf-8").read()
rep("function mimAtkX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {", js + "\nfunction mimAtkX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) { if (m.a === \"synapse\" || m.a === \"command\" || m.a === \"adapt\") return mimStructX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan);")
rep("if (!lo) try { mimAmbient(ctx, b, scr, T, d); } catch (e) {}", "if (!lo) try { mimAmbient(ctx, b, scr, T, d); } catch (e) {} try { mimTethers(ctx, b, scr, T, d); } catch (e) {}")
# structures do not lunge
rep("  if (a === \"absorb\") return u < .4 ? -.06 * Math.sin(u * 60) * (u / .4) : 0;", "  if (a === \"absorb\") return u < .4 ? -.06 * Math.sin(u * 60) * (u / .4) : 0;\n  if (a === \"synapse\" || a === \"command\" || a === \"adapt\") return 0;")
# calm motion: a slow float for the Node and Pylon; the Nexus's eye and rings drift, nothing turns
rep('if (k === "mnode" || k === "mpylon") return `vec3 p = position; transformed.y += .12 * sin(mt * 2.0944) * smoothstep(-1., 2., p.y); transformed.x += .05 * sin(mt * 2.0944 + p.y) * smoothstep(0., 3., p.y);`;',
    'if (k === "mnode" || k === "mpylon") return `vec3 p = position; transformed.y += .05 * sin(mt * 1.0472) * smoothstep(-1., 2., p.y);`; /* v846 a slow float, no sway */')
i = s.index('  if (k === "mnexus") return `vec3 p = position; float rr = length(p.xz)'); j = s.index("`;", i) + 2
s = s[:i] + '  if (k === "mnexus") return `vec3 p = position; float e = 1. - smoothstep(2.3, 2.7, length(p - vec3(0., 3.6, 0.))); transformed.y += e * .07 * sin(mt * 1.0472);`; /* v846 the eye and its rings drift; nothing turns */' + s[j:]
rep('"mnode":{"g":1},"mpylon":{"g":1}}', '"mnode":{"g":1},"mpylon":{"g":1}}', 1)
# the codex: the hive's structures under the swarm
rep('  mtitan: ["A living nursery.', '''  mnode: ["A living brain-lantern rooted in rock. Three Neural Nodes feed Omega's regeneration, and every one you break slows it.", "Every Node you burn is one less heartbeat for Omega, Commander."],
  mnexus: ["The relay an Alpha speaks through. It commands every hive in its quarter; break its four anchors and the Alpha stands alone.", "Break the Nexus and the Alpha stands alone. That's when it bleeds."],
  mpylon: ["An obelisk of stolen plating. While any Pylon stands Omega takes only half the damage, and it adapts to the ships that hurt it most.", "It's learning which of our ships hurt it most, Commander. Change the fleet, and break the Pylons."],
  mtitan: ["A living nursery.''')
rep("<em>From Stage ${CS[k]}</em>${MIM_LORE[k] ?", "<em>From Stage ${CS[k]}</em>${MIM_LORE[k] ?")
i = s.index("<em>From Stage ${CS[k]}</em>${MIM_LORE[k] ?"); j = s.index('.join("")}</div>', i) + len('.join("")}</div>')
s = s[:j] + '''<h3>The hive's structures</h3><div class="mimcls">${["mnode", "mnexus", "mpylon"].map(k => `<div class="mimcl"><canvas data-ship="${k}" width="224" height="112"></canvas><div><b>${(AL[k] || {}).n || k}</b><small>${MIM_LORE[k][0]}</small><details class="mxcod"><summary>Codex</summary><button class="btn" data-act="mimLore" data-k="${k}">🔊 Her assessment</button></details></div></div>`).join("")}</div>''' + s[j:]
open(p, "w", encoding="utf-8").write(s); print("ok")
