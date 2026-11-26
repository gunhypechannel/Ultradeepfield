"""v807: the Events hub wears the current season (colours, motif) and the Advisor hands over what's ready to claim; claims there burst."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p807_hub.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p807.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 806;", "const GAME_V = 807;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep('`<div class="evhubv sheet-like">${shEvents(true)}</div>`', '(() => { try { return evkHub(shEvents(true)); } catch (e) { return `<div class="evhubv sheet-like">${shEvents(true)}</div>`; } })()')
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
