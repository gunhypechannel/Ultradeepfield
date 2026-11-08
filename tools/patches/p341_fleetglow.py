p="docs/index.html"; h=open(p).read()
def rep(a,b,n=1):
    global h; c=h.count(a); assert c==n,(c,a[:70]); h=h.replace(a,b)
rep('''  battle.acc = battleAcc(r);''','''  battle.acc = battleAcc(r);
  /* v341: every commander's squadrons fly in their own flagship's glow colour (a friend's or an ally's report shows their colours, not yours) */
  for (const q of R.squads) { const u = q.own; if (typeof u === "string" && u !== "pirates" && u !== "cube" && (u === G.me || G.players[u] || isBot(u))) { const f = playerFac(u); if (FLAG_GLOW[f] != null) Object.defineProperty(q, "acc", { value: "#" + FLAG_GLOW[f].toString(16).padStart(6, "0") + "@" + f, enumerable: false, writable: true, configurable: true }); } }''')
rep('shipArtSoon(q.k, battle.acc[q.side], "side"); if (q.role === "carrier") shipArtSoon(q.k === "lord" ? "drone" : "fighter", battle.acc[q.side], "side");',
    'shipArtSoon(q.k, q.acc || battle.acc[q.side], "side"); if (q.role === "carrier") shipArtSoon(q.k === "lord" ? "drone" : "fighter", q.acc || battle.acc[q.side], "side");')
rep('b.acc[q.side]','(q.acc || b.acc[q.side])',5)
rep('b.acc[qk.side]','(qk.acc || b.acc[qk.side])')
rep('card("a", aN, youA)','card("a", aN, youA && !b.notMine)')
rep('card("d", dN, !youA)','card("d", dN, !youA && !b.notMine)')
rep("""  battle.acc = battleAcc(r);
""","""  battle.acc = battleAcc(r);
  { const own = R.squads.map(q => q.own).filter(u => typeof u === "string" && u !== "pirates" && u !== "cube" && (u === G.me || G.players[u] || isBot(u))); battle.notMine = own.length > 0 && !own.includes(G.me); } /* a friend's shared report: nobody in it is "you" */
""")
open(p,"w").write(h); print("ok")
