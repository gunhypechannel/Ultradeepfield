# v433: the Convergence theme again (owner: "slower and deep/sad sounding, isolate the piano, enhance the emotional and cinematic
#  experience"): docs/music_conv.mp3 is now built by tools/conv_theme2.py from the song's own solo-piano motif at 80% speed, scored
#  with strings, cellos, choir, sub and a heartbeat drum (109 s, loops). The file is loaded with ?v=433 so no cached copy plays.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('new Audio("music_conv.mp3")', 'new Audio("music_conv.mp3?v=433")')
t = t.replace("const GAME_V = 432;", "const GAME_V = 433;")
open(p, "w").write(t); print("ok")
