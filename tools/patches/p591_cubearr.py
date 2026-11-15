# v591 watch the Cube's arrival during the event too (owner: "When a player clicks the super cube during the event they should be able
# to watch the arrival of the cube as well"). The Cube sheet showed "Watch the Cube's arrival" only between events; now it is always
# there, the live Cube panel gets an "▶ Arrival" button, and while the replay plays during the event the siege fleets stay out of
# the shot until the Cube settles over the Void (56 s), so the arrival plays clean and the battle rises around it as it lands.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''${live ? "Watch the battle live" : "Cinematic view"}</button>${live ? "" : `<button class="btn ghost wide" data-act="liveReplay">▶ Watch the Cube's arrival</button>`}''',
    '''${live ? "Watch the battle live" : "Cinematic view"}</button><button class="btn ghost wide" data-act="liveReplay">▶ Watch the Cube's arrival</button>''')
rep('''<button class="btn ghost sm" data-act="siegeWatch">🎥 Watch</button>''', '''<button class="btn ghost sm" data-act="siegeWatch">🎥 Watch</button><button class="btn ghost sm" data-act="liveReplay">▶ Arrival</button>''')
rep('const on = (PH && PH.i >= 2) || (LI && LI.s > 56000); let C = W.cwar;', 'const on = (PH && PH.i >= 2 && !(LI && LI.rep && LI.s <= 56000)) || (LI && LI.s > 56000); let C = W.cwar; /* v591 */')
s2 = re.sub(r"GAME_V = 590\b", "GAME_V = 591", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
# a replay is labelled as one (it showed the red "● LIVE" badge)
s = open(P, encoding='utf-8').read()
a = 'bar.innerHTML = `<div class="lb-top"><span class="lb-live">● LIVE</span><span class="lb-t">BATTLE FOR THE CUBE</span>'
assert s.count(a) == 1
s = s.replace(a, 'bar.innerHTML = `<div class="lb-top"><span class="lb-live"${LI.rep ? \' style="background:#3a4a5a"\' : ""}>${LI.rep ? "▶ REPLAY" : "● LIVE"}</span><span class="lb-t">${LI.rep ? "THE CUBE\'S ARRIVAL" : "BATTLE FOR THE CUBE"}</span>')
open(P, 'w', encoding='utf-8').write(s); print('ok2')
