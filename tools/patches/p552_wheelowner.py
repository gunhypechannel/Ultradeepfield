# v552 owner test mode for the Glyph Wheel (owner: "Allow owner account to spin unlimited to test and perfect the animation").
# With the owner account (G.owner) the lever is always ready: no daily limit. Tapping a prize in the list makes the next spin land
# on it (G.whlForce, owner only), so the jackpot and every other landing can be watched on demand. Rewards are still granted.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function wheelHTML(T) { const can = (S.shopFree || "") !== shopDay() && S.wheelPend == null,', 'function wheelHTML(T) { const own = !!G.owner, can = (own || (S.shopFree || "") !== shopDay()) && S.wheelPend == null,')
rep('<span class="gwchip${W.jack ? " jack" : ""}${won && won.l === W.l ? " won" : ""}" style="--c:${W.col}">',
    '<span class="gwchip${W.jack ? " jack" : ""}${won && won.l === W.l ? " won" : ""}${own && G.whlForce === WHEEL.indexOf(W) ? " force" : ""}" style="--c:${W.col}"${own ? ` data-act="whlForce" data-i="${WHEEL.indexOf(W)}" role="button"` : ""}>')
rep('<div class="gwchips">${chips}</div></div></div>`; }', '<div class="gwchips">${chips}</div>${own ? `<p class="gwown">Owner test mode · unlimited spins${G.whlForce != null && WHEEL[G.whlForce] ? ` · next spin lands on <b style="color:${WHEEL[G.whlForce].col}">${esc(wheelName(WHEEL[G.whlForce]))}</b>` : " · tap a prize to make the next spin land on it"}</p>` : ""}</div></div>`; }')
rep('function wheelPull() { if (G.wheel || (S.shopFree || "") === shopDay() || S.wheelPend != null) return;', 'function wheelPull() { if (G.wheel || (!G.owner && (S.shopFree || "") === shopDay()) || S.wheelPend != null) return;')
rep('let r = Math.random() * WHEEL.reduce((a, W) => a + W.w, 0), idx = 0; for (let i = 0; i < WHEEL.length; i++) { r -= WHEEL[i].w; if (r < 0) { idx = i; break; } }',
    'let r = Math.random() * WHEEL.reduce((a, W) => a + W.w, 0), idx = 0; for (let i = 0; i < WHEEL.length; i++) { r -= WHEEL[i].w; if (r < 0) { idx = i; break; } }\n  if (G.owner && G.whlForce != null && WHEEL[G.whlForce]) { idx = G.whlForce; G.whlForce = null; } /* v552 owner test landing */')
rep('  shopFree: () => wheelPull(),', '  shopFree: () => wheelPull(),\n  whlForce: d => { if (!G.owner) return; const i = +d.i; G.whlForce = G.whlForce === i ? null : i; sheet ? renderSheet() : render(true); }, /* v552 */')
css = '.gwown{margin:6px 0 0;font-size:11px;color:#ffcf5a;letter-spacing:.02em}.gwchip[data-act]{cursor:pointer}.gwchip.force{outline:2px solid #ffcf5a;outline-offset:1px;box-shadow:0 0 14px rgba(255,207,90,.6)}'
rep('.shopgrid{display:grid;', '/* v552 wheel owner test mode */\n' + css + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 551\b", "GAME_V = 552", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
