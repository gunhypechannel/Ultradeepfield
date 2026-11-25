"""v758: the Xeno Sanctuary in 3D (tools/patches/p758_xs3.js). Owner: "is there any way to make the xeno sanctuary a 3d experience?"
... "Do it all". A "Walk the Sanctuary in 3D" button on the Sanctuary page opens a glass bio-dome over the screen (see the file's
header). The map behind it is drawn at 3 fps while it is open. Applies on top of v757."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 757;", "const GAME_V = 758;")
js = open("tools/patches/p758_xs3.js", encoding="utf-8").read()
a = "const xsHexRgb = h => { const n = parseInt(String(h).replace(\"#\", \"\"), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255].join(\",\"); };\n"
rep(a, a + js)
css = """body.xs3on #fbBtn{display:none!important}
#xs3{position:fixed;inset:0;z-index:59;background:#02060a;animation:xs3in .35s ease both}@keyframes xs3in{from{opacity:0}}
.xs3slot{position:absolute;inset:0}.xs3slot canvas{width:100%;height:100%;display:block}
.xs3top{position:absolute;top:calc(env(safe-area-inset-top,0px) + 10px);left:max(12px,env(safe-area-inset-left,0px));right:max(12px,env(safe-area-inset-right,0px));display:flex;justify-content:space-between;align-items:flex-start;gap:10px;pointer-events:none}
.xs3top>div{background:rgba(5,16,20,.74);border:1px solid rgba(127,255,208,.35);border-radius:12px;padding:6px 12px;display:flex;flex-direction:column;gap:1px;min-width:0}
.xs3top b{color:#7fffd0;font-family:Oxanium,sans-serif;letter-spacing:.08em;text-transform:uppercase;font-size:13px}.xs3top small{color:#bfe8dc;font-size:11px}
.xs3x{pointer-events:auto;flex:none;width:42px;height:42px;border-radius:50%;background:rgba(5,16,20,.82);border:1px solid rgba(127,255,208,.5);color:#e6fff6;font-size:18px;cursor:pointer}
.xs3hint{position:absolute;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 16px);transform:translateX(-50%);width:max-content;max-width:calc(100% - 32px);text-align:center;font-size:12px;color:#d6fff2;background:rgba(5,16,20,.7);border:1px solid rgba(127,255,208,.25);border-radius:20px;padding:6px 14px;pointer-events:none}
.xs3card{position:absolute;left:max(10px,env(safe-area-inset-left,0px));right:max(10px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 10px);max-width:520px;margin:0 auto;background:linear-gradient(180deg,rgba(14,34,42,.95),rgba(5,14,20,.97));border:1px solid rgba(127,255,208,.4);border-radius:16px;padding:12px;display:flex;flex-direction:column;gap:10px;max-height:48vh;overflow:auto;animation:up .22s ease-out}
.xs3cr{display:flex;gap:12px;align-items:center}.xs3cr>div{display:flex;flex-direction:column;gap:3px;min-width:0;flex:1}.xs3cr b{color:#f2fff9}.xs3cr small{color:#bcd8d0}
.xs3cr img{width:76px;height:76px;flex:none;border-radius:14px;object-fit:cover;border:2px solid var(--r,#7fffd0);box-shadow:0 0 18px color-mix(in srgb,var(--c,#7fffd0) 55%,transparent)}
.xs3star{color:#ffd36b;font-size:12px;font-weight:600}.xs3tr b{color:#ffe7a8!important}
.xs3b,.xs3eggs{display:flex;flex-wrap:wrap;gap:6px}.xs3eggs .btn{display:flex;align-items:center;gap:6px}.xs3eggs .btn span{display:flex;flex-direction:column;align-items:flex-start;line-height:1.2}
.xs3go{display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:4px}
"""
rep(".xsfx{position:fixed;inset:0;z-index:9500;", css + ".xsfx{position:fixed;inset:0;z-index:9500;")
rep("""  return `<div class="dp xsc"><div class="xsh"><b>Incubators</b>""", """  return `<div class="dp xsc"><button class="btn wide amber xs3go" data-act="xs3Open">◉ Walk the Sanctuary in 3D</button><div class="xsh"><b>Incubators</b>""")
rep("""  xsSel: d => { const s0 = G.xsSel || [];""", """  xs3Open: () => xs3Open(), /* v758 */
  xsSel: d => { const s0 = G.xsSel || [];""")
rep("""function sheetCap() { if (!sheet || battle""", """function sheetCap() { if (G.xs3 && !battle) return 3; /* v758 the 3D Sanctuary covers the screen */ if (!sheet || battle""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
