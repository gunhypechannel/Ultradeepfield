"""v789: the Squid, the Comet Ram and the Star Leviathan reshaped toward their paintings (owner: "do all of it except the Meshy AI
part"). Sculpts only (tools/sculpt/mon_sculpt.py, mon2_sculpt.py; art/mon/m/ssquid.bin, cram.bin, slevi.bin): the Squid's arms
half again as thick and curling at their tips; the Ram's spiral horns a third bigger and wound further, its legs reaching out in a
gallop (were tucked); the Leviathan's armoured whale head 16% bigger, its body fuller and the spines down its back much taller.
Same frames, so their swim and gallop waves still run. Applies on top of v788."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 788;", "const GAME_V = 789;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
