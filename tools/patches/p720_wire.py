# v720 (owner: "Yes I like it better, update it"): the Cube Devastation's theme is now the new piano piece (tools/ruin_theme.py, an
# original piece in the vein of FFX's Zanarkand: solo piano, strings and cello join, swell and leave; 142.5 s loop) instead of v719's
# choral piece. docs/music_cube.mp3 replaced; the URL's ?v bumped so phones fetch the new file.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('new Audio("music_cube.mp3?v=719")', 'new Audio("music_cube.mp3?v=720")')
rep('const GAME_V = 719;', 'const GAME_V = 720;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
