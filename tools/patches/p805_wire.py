"""v805: the event remaster kit (hero banners, one next-move button, reward chips, win-chance meters, streaks, a burst on every claim)
for every event sheet, and the Aetherion screens rebuilt with it. The reward coach no longer covers event screens."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
K = open(os.path.join(D, "p805_kit.js"), encoding="utf-8").read()
C = open(os.path.join(D, "p805_aet.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p805.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 804;", "const GAME_V = 805;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + K + "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("  if (!html) { closeSheet(); return; }\n", "  if (!html) { closeSheet(); return; }\n  try { html = evkWrap(html); } catch (e) {} /* v805 */\n")
rep('if (shEl) shEl.classList.toggle("facsh", sheet.type === "faction"); /* v249 */', 'if (shEl) shEl.classList.toggle("facsh", sheet.type === "faction"); /* v249 */\n  if (shEl) shEl.classList.toggle("evk", EVK_T.has(sheet.type)); /* v805 */')
rep("""const cx = sheet && document.querySelector('.sheet [data-act="close"]');""", """const cx = sheet && !EVK_T.has(sheet.type) && document.querySelector('.sheet [data-act="close"]'); /* v805: never cover an event screen */""")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
