# v604 performance (owner: "Game is super laggy for all players, can we optimize it", then "do it for the boss battle also"). The perf
# logs: Macs on Safari at 15-20 fps (base, base with a panel, the map), the owner's Fold at 29 fps with 3 s freezes.
# 1. No live glass blur: 52 rules blurred whatever was behind them (the dock, the HUD strips, panels, toasts, the chat bar, the Cube
#    band) and every one sits over the animated 3D base or map, so the browser re-blurred the scene under each of them every frame
#    (Safari worst of all). html.nobd turns backdrop-filter off everywhere; the panels keep their dark tinted glass, a little denser.
# 2. Computers may now drop render resolution under load: the adaptive resolution's floor on a PC or Mac was its native density, so a
#    Retina Mac always drew the base and map at 2x however slow it ran. It may now step down to 60% of that (never below 1x) and climbs
#    back when there is headroom, as phones already did.
# 3. Boss battles: while frames run long (over 22 ms), the boss's 3D model is redrawn every other frame (the soft-edged picture is
#    reused in between), and below 15 ms it is redrawn every frame again; its render size drops a quarter while slow (with hysteresis,
#    so it doesn't resize back and forth). The reactive barrier draws at most 4 strikes and 40 hex cells on a boss when slow.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('<html>', '<html class="nobd">')
rep('let PF = { t0: Date.now(),', 'try { document.documentElement.classList.add("nobd"); } catch (e) {} /* v604 also where the page is wrapped (the claude.ai copy) */ let PF = { t0: Date.now(),')
CSS = '''html.nobd *,html.nobd *::before,html.nobd *::after{-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
html.nobd .sheet{background:linear-gradient(180deg,rgba(14,34,50,.95),rgba(6,16,26,.97))!important}html.nobd .dock{background:linear-gradient(180deg,rgba(10,32,50,.94),rgba(4,14,24,.98))!important}html.nobd .tray-panel{background:rgba(8,22,36,.94)!important}html.nobd .toast{background:rgba(10,24,38,.94)!important}html.nobd #sheetwrap.glass .sheet{background:rgba(8,16,28,.9)!important}html.nobd .alcmdst{background:rgba(6,12,24,.82)}html.nobd .altabs{background:rgba(5,10,18,.97)}
'''
rep('.alcmd{position:relative;', CSS + '.alcmd{position:relative;')
rep('floor = WEAK || gfx("detail") === 0 ? .6 : MOBILE ? Math.min(max, Math.max(1, dprN * .5)) : Math.min(max, dprN);',
    'floor = WEAK || gfx("detail") === 0 ? .6 : MOBILE ? Math.min(max, Math.max(1, dprN * .5)) : Math.min(max, Math.max(1, dprN * .6)); /* v604 a PC or Mac may give up resolution too */')
rep('const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0, tg: Q.map((q2, k) => q2.side !== b.superSide && b.n[k] > 0 && scr[k] ? (scr[k].x - cx) / W : null).filter(v => v != null) }); if (A) ctx.drawImage(wbSoft(A), -aw / 2, -ah / 2, aw, ah); b.wbBox = { cx, cy, aw, ah };',
    '''const fe = frame.rawEma || 16.7; if (fe > 22) WBR.slow = 1; else if (fe < 15) WBR.slow = 0; /* v604 a slow device redraws the boss every other frame */
          let SA = null; if (WBR.slow && WBR.soft && WBR.softKey === wbk && ((b.wbFr = (b.wbFr || 0) + 1) & 1)) SA = WBR.soft; else { const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0, tg: Q.map((q2, k) => q2.side !== b.superSide && b.n[k] > 0 && scr[k] ? (scr[k].x - cx) / W : null).filter(v => v != null) }); if (A) { SA = wbSoft(A); WBR.softKey = wbk; } }
          if (SA) ctx.drawImage(SA, -aw / 2, -ah / 2, aw, ah); b.wbBox = { cx, cy, aw, ah };''')
rep('const W2 = Math.min(MOBILE ? 820 : 1100, Math.round(w))', 'const W2 = Math.min(Math.round((MOBILE ? 820 : 1100) * (WBR.slow ? .75 : 1)), Math.round(w))')
rep('if (seen[key] > (g[5] ? 6 : busy ? 1 : 3)) continue;', 'if (seen[key] > (g[5] ? (WBR.slow ? 4 : 6) : busy ? 1 : 3)) continue;')
rep('for (let gx = gx0 - cols; gx <= gx0 + cols && cnt < (boss ? 70 : 34); gx++)', 'for (let gx = gx0 - cols; gx <= gx0 + cols && cnt < (boss ? (WBR.slow ? 40 : 70) : 34); gx++)')
s2 = re.sub(r"GAME_V = 603\b", "GAME_V = 604", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
# --- and (owner, same evening): "Make it easier to skip past the advisor whenever she comes up"
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the big dialog: a Skip ✕ button ends the whole conversation; the dark area outside and Esc do too; the box still steps line by line
rep('<div class="tap">Tap to continue</div></div><button class="advv" data-act="voiceToggle" aria-label="Advisor voice">${VOICE.on ? "🔊" : "🔇"}</button></div></div>`;',
    '<div class="tap">Tap to continue</div></div><button class="advv" data-act="voiceToggle" aria-label="Advisor voice">${VOICE.on ? "🔊" : "🔇"}</button><button class="advskip" data-act="advSkip" aria-label="Skip the Advisor">Skip ✕</button></div></div>`;')
rep('<div class="advscrim"></div><div class="adv" data-act="advNext"', '<div class="advscrim" data-act="advSkip"></div><div class="adv" data-act="advNext"')
rep('function advNext() {', '''function advSkip() { voiceStop(); advLines = null; const a = $("#adv"); if (a) a.remove(); const th = G.advThen; G.advThen = null; if (th) try { th(); } catch (e) {} } /* v604 skip the whole conversation */
function advhHide() { clearTimeout(G.advhT); voiceStop(); const x = $("#advh"); if (x) x.classList.remove("on", "talk"); document.body.classList.remove("advtalk"); }
document.addEventListener("keydown", e => { if (e.key === "Escape") { if ($("#adv")) { advSkip(); e.preventDefault(); } else if ($("#advh.on")) advhHide(); } });
function advNext() {''')
rep('  advNext: () => advNext()\n};', '  advNext: () => advNext(), advSkip: () => advSkip(), advhX: () => advhHide() /* v604 */\n};')
# the hologram card: one tap anywhere on it dismisses it (only while it shows), with a small ✕
rep('''w.innerHTML = `<div class="holo"><img class="advimg" src="${advArt()}" style="${advFx()}" alt=""><i class="hscan"></i><i class="hbeam"></i></div><div class="hsay"><b>${ADV}</b><span></span></div>`; $("#app").appendChild(w); }''',
    '''w.innerHTML = `<div class="holo" data-act="advhX"><img class="advimg" src="${advArt()}" style="${advFx()}" alt=""><i class="hscan"></i><i class="hbeam"></i></div><div class="hsay" data-act="advhX" role="button" aria-label="Dismiss the Advisor"><b>${ADV}</b><span></span><i class="hx" aria-hidden="true">✕</i></div>`; $("#app").appendChild(w); }''')
CSS2 = '''.advskip{position:absolute;right:10px;bottom:8px;z-index:3;height:34px;padding:0 14px;border-radius:17px;border:1px solid rgba(255,255,255,.35);background:rgba(4,14,22,.8);color:#eaf7fc;font:700 13px var(--f-display);letter-spacing:.06em;cursor:pointer}.advskip:active{transform:scale(.96)}.adv .tap{text-align:left;padding-right:96px}.advscrim{cursor:pointer}
#advh.on .holo,#advh.on .hsay{pointer-events:auto;cursor:pointer}body:has(#adv) #advh{display:none}#advh .hsay{position:relative}#advh .hx{position:absolute;right:6px;top:4px;font-style:normal;font-size:12px;color:rgba(234,247,252,.7)}
'''
rep('.alcmd{position:relative;', CSS2 + '.alcmd{position:relative;')
open(P, 'w', encoding='utf-8').write(s); print('ok2')
