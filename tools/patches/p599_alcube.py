# v599 the Cube's tactical plot is back on the Alliance tab (owner: "In alliance tab I still wanted that cube animation we added
# recently"). v501 put the animated plot (the Cube, the fleets round it, their fire) in the alliance's call to arms; the v584
# simplification had cut it down to a one-line "Cube is live" button. Now, during the event, the call to arms sits above the tiles
# with the live plot and "Join the battle"; between events the plot ("Dormant · scanning", when it wakes) sits below the tiles.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''    ${evActive(T) ? `<button class="alneed cube" data-act="nexus"><b>◆ The Battle for the Cube is live</b><span>${nexusNow(T).holder === a.id ? "We hold the Cube. Reinforce it" : "Join the battle"} ›</span></button>` : ""}''',
    '''    ${evActive(T) ? `<div class="mcard tpcall alcube"><h3>◆ The Battle for the Cube is live</h3><p class="note">${nexusNow(T).holder === a.id ? "Your alliance holds the Cube. Reinforce the garrison before the rivals break it." : "The Cube is firing on the fleets around it. Every commander who joins raises your alliance's points."}</p>${tplotHTML(T)}<button class="btn amber wide" data-act="nexus">⚔ ${nexusNow(T).holder === a.id ? "Reinforce the Cube" : "Join the battle"}</button></div>` : ""} <!-- v599 the tactical plot -->''')
rep('''    <div class="allinks"><button data-act="allyView" data-v="list">Alliance list</button>''',
    '''    ${evActive(T) ? "" : `<div class="mcard alcube"><h3>◆ The Cube</h3>${tplotHTML(T)}<button class="btn ghost wide" data-act="nexus">Open the Cube</button></div>`}
    <div class="allinks"><button data-act="allyView" data-v="list">Alliance list</button>''')
s2 = re.sub(r"GAME_V = 598\b", "GAME_V = 599", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
