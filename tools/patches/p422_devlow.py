# v422: the Orbital Devourer hunts lower, just above the worlds. Its centre was at 24 +/- 3 (body from about 5 up to 41, well over the
# planet tops, which reach about 18 near it); now 14 +/- 2, so its body skims just above the worlds and its lowest tentacles reach down
# among them. It still rises over the Cube and other bosses where its path crosses them (wbSep). Its trail and wreck sites follow.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 24 + 3 * Math.sin(w * 3); return o; } // v394: it hunts from just above the worlds",
    "o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 14 + 2 * Math.sin(w * 3); return o; } // v394: it hunts from just above the worlds (v422: lower, skimming them)")
t = t.replace("const GAME_V = 421;", "const GAME_V = 422;")
open(p, "w").write(t); print("ok")
