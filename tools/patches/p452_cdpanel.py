# v452 Cube Devastation: the full event panel, the band from three days out through every stage, the Advisor calling each stage
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p452_cdpanel.js')).read().rstrip("\n")
i = s.index("function shOmega() {"); k = "setInterval(() => { try { omBand(); omClaim(); } catch (e) {} }, 1000);"; j = s.index(k, i) + len(k)
s = s[:i] + js + s[j:]
rep("if (!D) { if (W.dv) dvFree(W); return; } const X = W.dv || dvBuild(W),", "if (!D) { if (W.dv) dvFree(W); return; } try { dvSay(D); } catch (e) {} const X = W.dv || dvBuild(W),")
rep("G.dvP = null; G.dvF = null; G.dvSim = { t0: performance.now(),", "G.dvP = null; G.dvF = null; G.dvSaid = {}; G.dvSim = { t0: performance.now(),")
rep("#omband{position:absolute;", ".dvart{height:min(46vw,240px)}.dvtl{list-style:none;padding:0;margin:6px 0 10px;display:grid;gap:4px;counter-reset:dv}.dvtl li{display:grid;grid-template-columns:1fr auto;gap:0 8px;padding:7px 10px;border-radius:10px;background:rgba(255,255,255,.03);border-left:3px solid rgba(93,255,106,.25)}.dvtl li span{grid-column:1/3;opacity:.72;font-size:12px}.dvtl li small{opacity:.75;font-size:11px;white-space:nowrap}.dvtl li.done{opacity:.55;border-left-color:rgba(93,255,106,.5)}.dvtl li.now{background:rgba(93,255,106,.1);border-left-color:#5dff6a}.dvtl li.now small{color:#5dff6a;opacity:1}.omb.soon{opacity:.92}\n#omband{position:absolute;")
s = re.sub(r"GAME_V = 451\b", "GAME_V = 452", s)
open(P, 'w').write(s)
