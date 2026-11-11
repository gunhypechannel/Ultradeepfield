# v414 (4): the Convergence's pop-up art becomes a cinematic title banner: "THE CONVERGENCE" across a dark band in wide-spaced capitals,
# lit in a gradient of the five elements' colours, with a thin rule of those colours that draws out from the centre, then it fades.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""el.innerHTML = `<img src="${BOSS_ART.conv}" alt="The Convergence">`;""",
    """const cols = WB_EL.map(k => WB[k].col).join(","); el.innerHTML = `<div class="cvb" role="img" aria-label="The Convergence"><div class="cvt" style="background-image:linear-gradient(90deg,${cols})">THE CONVERGENCE</div><i class="cvr" style="background:linear-gradient(90deg,transparent,${cols},transparent)"></i></div>`; /* v414 a title banner, not the art */""")
rep("""#convcard img{width:min(78vw,420px);border-radius:14px;box-shadow:0 0 60px rgba(200,160,255,.55)}""",
    """#convcard .cvb{width:100%;padding:26px 16px 22px;display:grid;justify-items:center;gap:12px;background:linear-gradient(90deg,transparent,rgba(4,2,12,.82) 18%,rgba(4,2,12,.82) 82%,transparent);transform:scale(1.08);transition:transform 4.6s cubic-bezier(.2,.7,.2,1)}
#convcard.on .cvb{transform:scale(1)}
#convcard .cvt{font:800 clamp(24px,7.4vw,58px)/1 var(--f-display),system-ui,sans-serif;letter-spacing:.32em;padding-left:.32em;text-align:center;color:transparent;-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 0 14px rgba(210,170,255,.55)) drop-shadow(0 0 2px rgba(255,255,255,.6))}
#convcard .cvr{display:block;height:2px;width:0;transition:width 1.6s .3s cubic-bezier(.2,.7,.2,1);box-shadow:0 0 12px rgba(220,180,255,.8)}
#convcard.on .cvr{width:min(86vw,620px)}""")
rep("#convcard{position:fixed;inset:0;z-index:60;", "#convcard{position:fixed;inset:0;z-index:92;") # above the HUD and the path card
t = t.replace("const GAME_V = 413;", "const GAME_V = 414;")
open(p, "w").write(t); print("ok")
