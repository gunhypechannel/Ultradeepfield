# v549 the five newer monsters' paintings didn't load (owner: "some archives arts are not loading"). Their Bestiary entries and map
# cards asked for art/mon/<key>.webp (kegg, gwhale, reat, cserp, sent), but the paintings are saved as kraken, ghostwhale, rockeater,
# cserpent and sentinel. MON_IMG maps a monster key to its painting's file; archImg and monArt both go through it.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function archImg(E, lv, k) { if (/^b_/.test(k)) return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/mon/${k === "b_coll" ? "cube" : k.slice(2)}.webp?v=1"',
    'const MON_IMG = { kegg: "kraken", gwhale: "ghostwhale", reat: "rockeater", cserp: "cserpent", sent: "sentinel", coll: "cube" }, monImg = k => MON_IMG[k] || k; /* v549 */\n'
    'function archImg(E, lv, k) { if (/^b_/.test(k)) return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/mon/${monImg(k.slice(2))}.webp?v=1"')
rep('const monArt = k => `<div class="monart"><img src="art/mon/${k}.webp?v=1"', 'const monArt = k => `<div class="monart"><img src="art/mon/${monImg(k)}.webp?v=1"')
s2 = re.sub(r"GAME_V = 548\b", "GAME_V = 549", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
