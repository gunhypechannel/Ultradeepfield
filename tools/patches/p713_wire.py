# v713 (owner): the Advisor said "Did it just block that? With a shield on its arm?" (and "It fights like a swordsman!") while Aexion was
# still a dreadnought, before it had an arm, a shield or a sword. Those lines stay with the Warform; the dreadnought gets its own.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('"aex": ["It fights like a swordsman!', '"aexd": ["Look at the size of that hull. It only turns when it means to fire.", "Its broadside is rippling down the whole flank, Commander. Get under those guns!", "Hit the stern engines and the shield emitters. Break that hull open and we\'ll see what\'s inside."], "aex": ["It fights like a swordsman!')
rep('function bVoiceKey(b) { const r = b.r || {}; if (r.sbk) return r.sbk;', 'function bVoiceKey(b) { const r = b.r || {}; if (r.sbk) return r.sbk === "aex" && !r.sbForm ? "aexd" : r.sbk; /* v713 the dreadnought has no shield arm yet */')
rep('const GAME_V = 712;', 'const GAME_V = 713;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
