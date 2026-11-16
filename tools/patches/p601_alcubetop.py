# v601 the Cube's tactical plot sits at the top of the Alliance tab at all times (owner: "On alliance page put cube tactical plot up
# top"): between events the dormant plot card moves up from below the tiles, and both cards now come right under the header.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
dorm = '`<div class="mcard alcube"><h3>◆ The Cube</h3>${tplotHTML(T)}<button class="btn ghost wide" data-act="nexus">Open the Cube</button></div>`'
rep('''    ${evActive(T) ? "" : ''' + dorm + '''}\n''', '')
rep('''Join the battle"}</button></div>` : ""} <!-- v599 the tactical plot -->''', '''Join the battle"}</button></div>` : ''' + dorm + '''} <!-- v599 the tactical plot; v601 always at the top -->''')
# and it comes straight after the alliance header, above the glory banner and the bio
i = s.index('function alHome('); a0 = s.index('\n    ${gloryBanner(a.id)}${a.bio ?', i); a1 = s.index('\n', a0 + 1); c0 = a1; c1 = s.index('<!-- v599 the tactical plot; v601 always at the top -->', c0) + len('<!-- v599 the tactical plot; v601 always at the top -->')
glory = s[a0:a1]; cube = s[c0:c1]; assert cube.startswith('\n    ${evActive(T) ?'), cube[:40]
s = s[:a0] + cube + glory + s[c1:]
s2 = re.sub(r"GAME_V = 600\b", "GAME_V = 601", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
