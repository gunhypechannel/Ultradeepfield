"""v866: the Abyssal Breach Nest remastered (see p866_nest.js; the sculpt tools/sculpt/crc_nest.py)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 865;", "const GAME_V = 866;")
js = open(__file__.rsplit('/', 1)[0] + "/p866_nest.js", encoding="utf-8").read()
rep("function crcAtkAdd(b, v) {", js + "function crcAtkAdd(b, v) {")
rep("function crcAtkAdd(b, v) { const q = b.Q[v.s]; if (!q || v.e == null || v.e < 0) return;", "function crcAtkAdd(b, v) { const q = b.Q[v.s]; if (!q || v.e == null || v.e < 0) return; if (q.k === \"cnest\") return nestAtkAdd(b, v); /* v866 its own */")
rep("try { krakAtkDraw(ctx, b, scr, T, W, H, d, t); krakFx(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v863 */",
    "try { krakAtkDraw(ctx, b, scr, T, W, H, d, t); krakFx(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v863 */ try { nestFx(ctx, b, scr, T, d, lo); nestAtkDraw(ctx, b, scr, T, W, H, d, t); } catch (e) {} /* v866 */")
open(p, "w", encoding="utf-8").write(s); print("ok")
