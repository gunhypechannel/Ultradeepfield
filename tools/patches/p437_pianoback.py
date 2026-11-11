# v437: the Convergence theme back to the solo-piano version of v433 (owner: the violin solo "sounds kinda bad"). ?v=437 so no
#  cached violin copy plays.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('new Audio("music_conv.mp3?v=436")', 'new Audio("music_conv.mp3?v=437")')
t = t.replace("const GAME_V = 436;", "const GAME_V = 437;")
open(p, "w").write(t); print("ok")
