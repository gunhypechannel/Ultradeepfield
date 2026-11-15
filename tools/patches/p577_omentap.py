# v577 The week's omen can be tapped (owner: "Yes" to "the weekly omens can't be tapped"). In the prologue, when no event band is up,
# the map shows a band "☾ OMEN n OF 8 · <name>": tapping it flies the camera to the omen and then opens its page in the Archives.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''const nx = finNext(k, T); if (nx - T < 72 * 3600e3 && nx > T) return `<button class="omb fin soon" style="--fc:${FIN_EV[k].col}" data-act="finOpen" data-k="${k}"><b>${FIN_EV[k].ic} ${esc(FIN_EV[k].n.toUpperCase())}</b><span>in ${ftime(nx - T)}</span></button>`; } return ""; }''',
    '''const nx = finNext(k, T); if (nx - T < 72 * 3600e3 && nx > T) return `<button class="omb fin soon" style="--fc:${FIN_EV[k].col}" data-act="finOpen" data-k="${k}"><b>${FIN_EV[k].ic} ${esc(FIN_EV[k].n.toUpperCase())}</b><span>in ${ftime(nx - T)}</span></button>`; }
  { const ok = omenKey(T), j = OMEN_K.indexOf(ok), E = ARCH["o_" + (j + 1)]; if (ok && E) return `<button class="omb fin omen" style="--fc:#8fb0e0" data-act="omenGo" data-k="${ok}"><b>☾ OMEN ${j + 1} OF ${OMEN_K.length}</b><span>${esc(E.t.replace(/^Omen \\d+: /, ""))}</span><i>📜</i></button>`; } /* v577 the week's omen */
  return ""; }
/* v577 where each omen shows on the map: fly there, then its Archives page */
function omenFocus(k, T) { const s0 = omenWk0(T); try { if (k === "lev" || k === "wym") { const p = finP1(k, s0); return [p.x, p.y, p.z, 620]; } if (k === "aex" || k === "vae") { const p = SBX[k].p; return [p[0], p[1], p[2], 820]; } } catch (e) {} return [0, 0, 0, k === "krk" ? 1000 : k === "khz" ? 900 : 1250]; }
function omenGo(k) { const T = now(), j = OMEN_K.indexOf(k); if (j < 0) return; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); }
  setTimeout(() => { try { const c = G3 && G3.cam, f = omenFocus(k, T); if (c) { c.follow = null; c.followFleet = null; c.goal = { tx: f[0], ty: f[1], tz: f[2], dist: f[3], th: .7 }; } } catch (e) {} }, 300);
  clearTimeout(G.omenT); G.omenT = setTimeout(() => { try { if (view === "galaxy" && !sheet && !battle) { if (!archLv("o_" + (j + 1))) archUnlock("o_" + (j + 1), 1, true); openSheet({ type: "archives", id: "o_" + (j + 1) }); } } catch (e) {} }, 4200); }''')
rep('  finWatch: d => finWatchGo(d.k),', '  finWatch: d => finWatchGo(d.k), omenGo: d => omenGo(d.k), /* v577 */')
rep('.omb{display:flex;align-items:center;', '.omb.omen{background:rgba(6,12,26,.92);color:#e2ecff}.omb.omen i{font-style:normal;opacity:.85}\n.omb{display:flex;align-items:center;')
rep('<p>${id === "testament" ? "" : `${/^s_/.test(id) ? `Build a',
    '<p>${id === "testament" ? "" : /^o_/.test(id) ? "What it means comes clear when the omen fades at the end of its week." : /^c_/.test(id) ? "The rest of this chapter is written when its season finale ends." : `${/^s_/.test(id) ? `Build a') # v577 omens and chapters are not defeated
# The Count Breaks, from the check on the owner's PC: the count marks read grey, so they are bigger and brighter; and whoever watched
# it (Watch, any time during the event) is carried out to the Judge for the silence, even if the 90-second ride has ended.
rep('b = lit * (.14 + (big ? .1 : 0) + 1.3 * tr);', 'b = lit * (.3 + (big ? .2 : 0) + 2.4 * tr);')
rep('X.Sc.set(big ? 26 : 15, 3, big ? 5 : 3);', 'X.Sc.set(big ? 36 : 22, 4, big ? 8 : 5);')
rep("  /* at the end the camera lifts toward the Judge's face, his eyes blazing */",
    "  if (G.finFollow && performance.now() < G.finFollow) X.watched = 1; if (X.watched && e >= E[2] && !X.lift && view === \"galaxy\" && !sheet && G3 && G3.cam) { X.lift = 1; G.finFollow = performance.now() + 240000; const c = G3.cam; c.cineObj = null; c.follow = null; c.followFleet = null; c.goal = { tx: X.cp.x, ty: X.cp.y, tz: X.cp.z, dist: 1650, th: .7 }; } /* v577 */\n  /* at the end the camera lifts toward the Judge's face, his eyes blazing */")
s2 = re.sub(r"GAME_V = 576\b", "GAME_V = 577", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
