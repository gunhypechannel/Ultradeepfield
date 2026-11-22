# v710: the dots joined (see p710_lore.js). Also edits p704_crc.js and p706_story.js so a re-apply of those blocks keeps the changes.
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
SRC = {f: R(f) for f in ('p704_crc.js', 'p706_story.js')}
def rep(a, b, n=1, src=None):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
    if src: assert SRC[src].count(a) >= 1, (src, a[:90]); SRC[src] = SRC[src].replace(a, b)
L = 'setInterval(() => { try { crcStoryTick(); crcArchTick(); } catch (e) {} }, 15000);'
rep(L, L + '\n' + R('p710_lore.js').rstrip('\n'))
# the Carcinid record no longer says the masters were the only reason (see q_warden)
rep('''adv: "The Leviathan was theirs, Commander. That's why it turned inward. It heard them calling it home."''',
    '''adv: "The Leviathan was theirs, Commander. That's half of why it turned inward. It heard them calling it home."''', src='p706_story.js')
# the tide's screen opens with a "Previously"
rep('<p class="note">${on ? CRC_WEEKS[w - 1][1]', '${on ? `<p class="note crcprev">${CRC_SAY[crcLevFate(T) === "dead" ? "prev_held" : "prev_cracked"]}</p>` : ""}<p class="note">${on ? CRC_WEEKS[w - 1][1]', src='p704_crc.js')
rep('.crcfate{color:#e8c890;margin:4px 0 0}', '.crcfate{color:#e8c890;margin:4px 0 0}\n.crcprev{font-style:italic;opacity:.85;margin:0 0 4px}')
rep('const GAME_V = 709;', 'const GAME_V = 710;')
open(p, 'w', encoding='utf-8').write(s)
if p.endswith('docs/index.html'):
    for f, t in SRC.items(): open(os.path.join(D, f), 'w', encoding='utf-8').write(t)
print('ok')
