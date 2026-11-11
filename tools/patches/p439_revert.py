# v439: the Convergence theme back to the solo-piano version (v433/v437) (owner: "nvm revert" the choral piece of v438). ?v=439.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('new Audio("music_conv.mp3?v=438")', 'new Audio("music_conv.mp3?v=439")')
t = t.replace("const GAME_V = 438;", "const GAME_V = 439;")
open(p, "w").write(t); print("ok")
