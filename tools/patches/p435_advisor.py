# v435: the Advisor's lines, cleaner and less repetitive (owner: "make sure all adviser lines are clean and unrepetitive, she should
#  sound like a talking expert and super fluid"). 83 of her 421 voiced lines rewritten (p435_advisor.json: old -> new): far fewer
#  "Commander, ..." openers, the eight identical "... is under attack right now! Watch it live." and the six "everyone who fought it
#  can claim the spoils" each said a different way, the boss scans no longer all "Scanning X. Beware ...", and no more repeated
#  "the galaxy is yours to take", "never attack blind" or "earns experience in every fight". Every fact is kept.
import json
p = "docs/index.html"; t = open(p).read()
for x in json.load(open("tools/patches/p435_advisor.json")):
    assert t.count(x["old"]) == 1, (t.count(x["old"]), x["old"][:80]); t = t.replace(x["old"], x["new"])
t = t.replace("const GAME_V = 434;", "const GAME_V = 435;")
open(p, "w").write(t); print("ok")
