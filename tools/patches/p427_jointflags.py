# v427: joint battles show a flagship for each of the (up to 3) strongest commanders on both sides, each in its own faction.
#  Since v5 (merged squadrons) every ally's ships of one type fight as one stack whose `own` is the first ally in it, so a joint strike
#  showed the leader's flagship and at most one ally's. The replay squads now carry the stack's shares (`shr`, visual only, the
#  simulation is untouched), and battleFlags weighs each commander by their share of every stack. Flagships of one side fly
#  abreast (spread across the line of fire) instead of piling onto the same spot. Bots fly their own faction's flagship in battle
#  too (the one they fly on the map; it was always Terran).
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("squads: sq.map(s => ({ id: s.id, side: s.side, k: s.k, own: s.own, role: s.role,", "squads: sq.map(s => ({ id: s.id, side: s.side, k: s.k, own: s.own, shr: s.src && s.src.shares, role: s.role,")
rep("Q.forEach((q, i) => { if (q.side !== sd) return; any = 1; const f = pf(q.own); if (!f) return; const g = groups.get(q.own) || { f, idx: [], w: 0 }; g.idx.push(i); g.w += Math.sqrt(Math.max(1, q.n0 * (q.pow || 1))); groups.set(q.own, g); });",
    "Q.forEach((q, i) => { if (q.side !== sd) return; any = 1; const sh = q.shr && Object.keys(q.shr).length ? q.shr : { [q.own]: q.n0 }, tot = Object.values(sh).reduce((a, b) => a + b, 0) || 1; /* v427 every commander with ships in a merged stack */\n      for (const u in sh) { const f = pf(u); if (!f) continue; const g = groups.get(u) || { f, idx: [], w: 0 }; g.idx.push(i); g.w += Math.sqrt(Math.max(1, q.n0 * sh[u] / tot * (q.pow || 1))); groups.set(u, g); } });")
rep("const tx = clamp(mx + ux * rear, L0 * .55, W - L0 * .55), ty = clamp(my + uy * rear, vb[0] + L0 * .55, vb[1] - L0 * .5); e.dead = null;",
    "const nS = b.flags[sd].length, kS = b.flags[sd].indexOf(e), stp = L0 * (Math.abs(uy) > Math.abs(ux) ? 1.9 : .9), o = (kS - (nS - 1) / 2) * stp, half = (nS - 1) / 2 * stp, ex = Math.abs(uy) * half, ey = Math.abs(ux) * half; /* v427 a side's flagships fly abreast */\n      let tx = clamp(mx + ux * rear, L0 * .55 + ex, W - L0 * .55 - ex) - uy * o, ty = clamp(my + uy * rear, vb[0] + L0 * .55 + ey, vb[1] - L0 * .5 - ey) + ux * o;\n      const vt = Math.abs(uy) > Math.abs(ux), gx = L0 * 1.75, gy = L0 * .8; for (const q of b.flags[sd]) { if (q === e || q.x == null || q.dead != null) continue; const dx = tx - q.x, dy = ty - q.y; /* v427 two flagships never settle on each other: this one aims aside, across the line of fire */\n        if (Math.abs(dx) < gx && Math.abs(dy) < gy) { const sg = (vt ? dx : dy) > 0 || ((vt ? dx : dy) === 0 && kS > b.flags[sd].indexOf(q)) ? 1 : -1; if (vt) tx = clamp(q.x + sg * gx, L0 * .55, W - L0 * .55); else ty = clamp(q.y + sg * gy, vb[0] + L0 * .55, vb[1] - L0 * .5); } }\n      e.dead = null;")
rep('const playerFac = uid => uid === G.me ? facOf() : (G.players[uid] && FACTIONS[G.players[uid].fac] ? G.players[uid].fac : "terran");',
    'const playerFac = uid => uid === G.me ? facOf() : (G.players[uid] && FACTIONS[G.players[uid].fac] ? G.players[uid].fac : isBot(uid) ? DEMO_FAC[hash(uid) % 4] : "terran"); /* v427 a bot flies the same faction in battle as on the map (it was always Terran) */')
t = t.replace("const GAME_V = 426;", "const GAME_V = 427;")
open(p, "w").write(t); print("ok")
