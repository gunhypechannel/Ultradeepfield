p="docs/index.html"; h=open(p).read()
a='''  const amt = Math.round((2500 + score() * 12) * (c.kind === "g" ? .5 : c.kind === "c" ? .75 : 1)); S.res[c.kind] += amt; return `${fmt(amt)} ${RES_N[c.kind].toLowerCase()}`;'''
assert h.count(a)==1
h=h.replace(a,'''  const amt = Math.round((2500 + score() * 12) * (c.kind === "g" ? .5 : c.kind === "c" ? .75 : 1));
  const P = actPlanet(); if (P) { settle(P); P.st[c.kind] += amt; try { putPlanet(P); } catch (e) {} return `${fmt(amt)} ${RES_N[c.kind].toLowerCase()} to ${P.name}`; } /* v341: it lands on the world you're on, not always the homeworld */
  S.res[c.kind] += amt; return `${fmt(amt)} ${RES_N[c.kind].toLowerCase()}`;''')
open(p,"w").write(h); print("ok")
