# v438: the Convergence theme is the choral/orchestral piece (owner: "use it"): tools/orch_theme.py, in the vein of Omnis Lacrima
#  but original, built on our motif with real instrument samples (choir, strings, cello, bass, horns, timpani, piano). ?v=438.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('new Audio("music_conv.mp3?v=437")', 'new Audio("music_conv.mp3?v=438")')
t = t.replace("const GAME_V = 437;", "const GAME_V = 438;")
open(p, "w").write(t); print("ok")
