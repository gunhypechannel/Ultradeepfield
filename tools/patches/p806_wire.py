"""v806: season skins for every event page (hero from the page's painting, the season's token in its frame, the Advisor in the
season's outfit with the next move, the season's motif and colours, lore folded, section chips)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p806_skin.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p806.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 805;", "const GAME_V = 806;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("  try { html = evkWrap(html); } catch (e) {} /* v805 */\n", "  try { html = evkWrap(html); } catch (e) {} /* v805 */\n  try { html = evkStage(html); } catch (e) {} /* v806 */\n")
rep('  if (shEl) shEl.classList.toggle("evk", EVK_T.has(sheet.type)); /* v805 */', '  if (shEl) shEl.classList.toggle("evk", EVK_T.has(sheet.type)); /* v805 */\n  if (shEl) { const sk = EVK_T.has(sheet.type) ? evkSkinOf(sheet.type) : null; if (sk) { shEl.dataset.skin = sk.motif; shEl.style.setProperty("--sc", sk.col); shEl.style.setProperty("--sc2", sk.col2); } else delete shEl.dataset.skin; } /* v806 */')
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
