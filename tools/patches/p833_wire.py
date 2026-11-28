"""v833: 26 new Advisor voice lines (Harbinger, event tips, titan holo lines, welcome back) and painted cards for the Mimic Stalker, Mimic Titan and The Kraken."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 832;", "const GAME_V = 833;")
rep('''const CRC_ART = { cscut: "drone",''', '''const CRC_ART = { ckrak: "../boss/kraken-skin", cscut: "drone",''')
rep('''<div class="mimcls">${cls.map(k => `<div class="mimcl"><canvas data-ship="${k}" width="224" height="112"></canvas>''',
    '''<div class="mimcls">${cls.map(k => `<div class="mimcl">${MIM_ART[k] ? `<img src="art/mimic/${MIM_ART[k]}.webp" alt="" loading="lazy" style="width:112px;height:72px;flex:none;border-radius:7px;object-fit:cover;object-position:50% 30%">` : `<canvas data-ship="${k}" width="224" height="112"></canvas>`}''')
rep("const CRC_ART = {", "const MIM_ART = { mstalk: \"stalker\", mtitan: \"titan\" };\nconst CRC_ART = {")
open(p, "w", encoding="utf-8").write(s); print("ok")
