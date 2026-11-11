# v443 the Omega Cube pays elemental runes instead of Omega Core Fragments (owner: "switch omega core fragments for runes or elements").
# 2 runes for everyone who broke a section, +1 top ten, +1 top damage, +1 final blow (2 to 5). Runes stay boss-only.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep("shards by share, Omega Core Fragments (more for the top ten, the top damage and the\n   final blow)", "shards by share, elemental runes (2, +1 for the top ten, +1 the top damage, +1 the\n   final blow)")
rep("frag = 1 + (i < 10 ? 1 : 0)", "frag = 2 + (i < 10 ? 1 : 0)")
rep("S.omegaFrag = (S.omegaFrag || 0) + frag; giveItem(it);", "grantRunes(frag, \"Omega Cube core\"); giveItem(it);")
rep('logReward("Omega Cube destroyed", null, { shards: sh, item: it, kind: "battle" });', 'logReward("Omega Cube destroyed", null, { shards: sh, item: it, runes: frag, kind: "battle" });')
rep('${frag} Omega Core Fragment${frag > 1 ? "s" : ""}', '${frag} elemental runes')
rep("◆ shards by share, Omega Core Fragments, an item;", "◆ shards by share, 2–5 elemental runes, an item;")
rep("A joint strike on a Lv.10+ Cube adds +10%.</p>", "A joint strike on a Lv.10+ Cube adds +10%. The Omega Cube, on the 15th of every month, gives 2 to 5 to everyone who breaks a section off it.</p>")
s, k = re.subn(r"GAME_V = 442\b", "GAME_V = 443", s); assert k == 1
open(P, 'w').write(s)
