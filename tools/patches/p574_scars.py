# v574 (owner: "Continue with the rest of the build"; "titan preview page doesn't show anything, its blocked or hidden").
# 1) The Titan viewer was squashed to 86 px: the sheet is a flex column and the viewer box (.t3w, overflow hidden) shrank as the
#    sheet's text grew. It no longer shrinks; nor do the finale and event headers.
# 2) Every cracked seal leaves its mark on the map for a year (FIN_SCAR builders, finScars replaces the Leviathan-only finScar).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('.t3w{position:relative;margin:4px 0 8px;', '.t3w{flex-shrink:0;position:relative;margin:4px 0 8px;')
rep('.dvart{height:min(46vw,240px)}', '.dvart{height:min(46vw,240px);flex-shrink:0}')
i = s.find('/* a cracked seal leaves its scar on the map until that chapter returns'); j = s.find('/* ---------- the event panel ---------- */', i); assert 0 < i < j
s = s[:i] + open('tools/patches/p574_scars.js', encoding='utf-8').read() + s[j:]
rep('try { finScar(W, t, T); } catch (e) {}', 'try { finScars(W, t, T); } catch (e) { mapErr(e); }')
s2 = re.sub(r"GAME_V = 573\b", "GAME_V = 574", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
