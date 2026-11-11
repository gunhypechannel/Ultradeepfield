# v436: the Convergence theme as a violin solo (owner: "a strong violin solo, same tempo, same everything, just remaster it in
#  violin"): docs/music_conv.mp3 is now rendered by tools/conv_theme3.py, which is conv_theme2.py with the piano replaced by a bowed
#  violin playing the same motif an octave up (at the theme's pitch the A would sit below the violin's lowest string). Loaded as ?v=436.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('new Audio("music_conv.mp3?v=433")', 'new Audio("music_conv.mp3?v=436")')
t = t.replace("const GAME_V = 435;", "const GAME_V = 436;")
open(p, "w").write(t); print("ok")
