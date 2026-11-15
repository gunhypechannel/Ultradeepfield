# v586 On the planet the week's omen (and the free-spin reminder) sit IN the HUD, in place of the "Events · My own · Friendly ·
# Hostile · Slots" strip (owner: "Can we replace this with the banner at the top events: my own etc" — the floating band covered the
# strip and the job bars). A hostile fleet on its way still shows the Events strip, so an attack warning is never hidden.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''    <button class="evbar" data-act="nav" data-v="fleets"><span class="k">Events</span>''', '''    ${G.hb && !hostile ? `<div class="evbar hb">${G.hb}</div>` : `<button class="evbar" data-act="nav" data-v="fleets"><span class="k">Events</span>''')
rep('''<span>Slots <b>${fleetsUsed()}/${maxFleets()}</b></span></button>${qbarHTML()}`;''', '''<span>Slots <b>${fleetsUsed()}/${maxFleets()}</b></span></button>`}${qbarHTML()}`;''')
rep('''  if (!html && view === "base" && !sheet && !battle) html = omenBand(T); /* v580 the week's omen: on the planet only */
  if (view === "base" && !sheet && !battle && !cineOn) { const wb = wheelBand(); if (wb) html = (html || "") + wb; } /* v582 */''',
    '''  { let hb = ""; if (view === "base" && !battle) { hb = omenBand(T) + wheelBand(); } if ((G.hb || "") !== hb) { G.hb = hb; try { hud(); } catch (e) {} } } /* v586 on the planet: in the HUD strip */''')
rep('.evbar{background:transparent;border-top-color:rgba(85,214,232,.14)}', '''.evbar{background:transparent;border-top-color:rgba(85,214,232,.14)}
.evbar.hb{gap:6px;padding:3px 8px 4px;cursor:default}.evbar.hb .omb{flex:1 1 0;min-width:0;justify-content:center;gap:8px;padding:4px 10px;border-radius:9px;font-size:11.5px;box-shadow:none;white-space:nowrap;overflow:hidden}
.evbar.hb .omb b{letter-spacing:.08em}.evbar.hb .omb span{overflow:hidden;text-overflow:ellipsis;color:#cfe0f2}.evbar.hb .omb i{font-size:12px}.evbar.hb .omb.whb{flex:0 1 auto;animation:none;box-shadow:0 0 10px rgba(255,207,90,.35)}.evbar.hb .omb.whb span{display:none}''')
s2 = re.sub(r"GAME_V = 586\b", "GAME_V = 586", s); s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
