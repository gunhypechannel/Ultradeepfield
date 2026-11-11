# v424: event banners fill their frame. The art was a fixed-height strip pinned to the right (125% of the banner's height), so on a wide
# screen (an open Fold, a tablet) most of the banner was an empty gradient. The art now covers the whole banner (object-fit: cover,
# framed a little right of centre, where the ships sit), fading in from the left under the title so the title stays readable, with a
# soft dark edge along the bottom for the countdown.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep(""".evban img{position:absolute;right:-8%;top:-10%;height:125%;opacity:.9;filter:drop-shadow(0 0 12px rgba(0,0,0,.6))}""",
    """.evban img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 42%;opacity:.95;-webkit-mask-image:linear-gradient(90deg,rgba(0,0,0,.25) 0,rgba(0,0,0,.85) 30%,#000 55%);mask-image:linear-gradient(90deg,rgba(0,0,0,.25) 0,rgba(0,0,0,.85) 30%,#000 55%)}
.evban:not(.vid)::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(6,14,30,.7),rgba(6,14,30,0) 45%),linear-gradient(0deg,rgba(6,14,30,.55),rgba(6,14,30,0) 40%)}
.evban .evt,.evban .evend{z-index:1}""")
t = t.replace("const GAME_V = 423;", "const GAME_V = 424;")
open(p, "w").write(t); print("ok")
