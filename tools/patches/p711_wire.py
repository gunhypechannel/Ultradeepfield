# v711 (owner): "Allow players to recall fleets when stationed at the cube" and "make bosses like pyramid overlord only come out when cube
# event is not running" (chosen slot: Monday 18:00 to Wednesday 18:00 UTC).
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# ---- 1. the weekly hunts move off the weekend ----
# The Saturday track (Pyramid Overlord, Devourer, Warlord, Matriarch, Tyrant, Wyrm, Colossus and the Saturday chapter finales) ran
# Saturday 18:00 to Monday 18:00 UTC, across the Battle for the Cube (Friday 18:00 to Sunday 18:00). From the first Monday slot at or
# after 23 Nov 2026 18:00 UTC each week's hunt opens on that week's Monday 18:00 and ends as the Wednesday events begin. Earlier weeks keep
# their Saturday (so a hunt already running isn't cut short); the last Saturday hunt ends exactly when the first Monday hunt opens.
# The Eclipse (the Sunday after the last finale) and the Mimic finale weekend keep their own dates.
rep('ROTS_X = ["lev"]; /* v569 the finale-only Saturday bosses */',
    'ROTS_X = ["lev"]; /* v569 the finale-only Saturday bosses */\n/* v711 the weekly hunts run Monday 18:00 to Wednesday 18:00 UTC from ROTS_CUT on (they were Saturday to Monday, across the Battle for the Cube) */\nconst ROTS_CUT = Math.max(0, Math.ceil((Date.UTC(2026, 10, 23, 18) - (ROT0 - 2 * 864e5)) / WEEK));')
rep('rotWs = T => Math.floor((T - ROTS0) / WEEK),', 'rotWs = T => { const n = Math.floor((T - ROT0 + 2 * 864e5) / WEEK); return n >= ROTS_CUT ? n : Math.floor((T - ROTS0) / WEEK); }, satOf = w => ROT0 + w * WEEK + (w >= ROTS_CUT ? -2 : 3) * 864e5,')
rep('B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= 44; i++) { const w = W - i; if (w < 0) return null; if (K(w) === key) return B + w * WEEK; } return null; };',
    'B = ROT0, W = sm ? rotWs(T) : Math.floor((T - B) / WEEK); for (let i = 0; i <= 44; i++) { const w = W - i; if (w < 0) return null; if (K(w) === key) return sm ? satOf(w) : B + w * WEEK; } return null; };')
rep('B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + 45; w++) { const s0 = B + w * WEEK;',
    'B = ROT0, W = Math.max(0, sm ? rotWs(T) : Math.floor((T - B) / WEEK)); for (let w = W; w <= W + 45; w++) { const s0 = sm ? satOf(w) : B + w * WEEK;')
rep('const sat = s2 + 3 * 864e5; if (rotKeyS(rotWs(sat)) !== (D.con != null ? "ovl" : k)) return null; return [sat + finShift(k, sat), sat + WB_LIVE]; }',
    'const want = D.con != null ? "ovl" : k, wm = rotWs(s2 + 5 * 864e5), wl = Math.floor((s2 + 3 * 864e5 - ROTS0) / WEEK); let sat = null; if (wm >= ROTS_CUT && rotKeyS(wm) === want) sat = satOf(wm); else if (wl < ROTS_CUT && rotKeyS(wl) === want) sat = satOf(wl); if (sat == null) return null; return [sat + finShift(k, sat), sat + WB_LIVE]; } /* v711 the cycle (Wed to Wed) holds the next week\'s Monday hunt */')
rep('  const sat = ROTS0 + w * WEEK; return [sat, sat + D.set, sat + WB_LIVE]; }', '  const sat = satOf(w); return [sat, sat + D.set, sat + WB_LIVE]; } /* v711 */')
rep('ws = rotWs(T), s1 = ROTS0 + ws * WEEK;', 'ws = rotWs(T), s1 = satOf(ws);')
# the hunt news: the current week's slot (not "the cycle's Saturday")
rep('sat = s2 + 3 * 864e5, rs = s2 >= ROT0 ? rotKeyS(rotWs(sat)) : null, satNew = T >= sat && T - sat < 24 * 3600e3,',
    'wsN = rotWs(T), sat = satOf(wsN), rs = s2 >= ROT0 && wsN >= 0 ? rotKeyS(wsN) : null, satNew = T >= sat && T - sat < 24 * 3600e3,')
rep('advNews(ADV_NEWS["wb_new_" + rs] ? "wb_new_" + rs : "wb_new", "wb:" + c2,', 'advNews(ADV_NEWS["wb_new_" + rs] ? "wb_new_" + rs : "wb_new", wsN >= ROTS_CUT ? "wbm:" + sat : "wb:" + c2,')
# the season finale card: the Monday finale comes first now; the Mimic finale weekend and the Eclipse keep their Saturday/Sunday
rep('wed = ROT0 + w * WEEK, sat = ROTS0 + w * WEEK; if (T > sat + 48 * 3600e3) return ""; /* v561 */',
    'wed = ROT0 + w * WEEK, sat = satOf(w), satL = ROTS0 + w * WEEK; if (T > Math.max(sat, wed, satL) + 48 * 3600e3) return ""; /* v561; v711 the Monday hunt, the legacy Saturday for the Mimic weekend and the Eclipse */')
rep('''  return `<div class="seafin"><small>★ SEASON FINALE</small><div${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${a}"` : ""}><span>${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? `Chapter ${FIN_EV[a].ch} · ${esc(FIN_EV[a].n)}` : esc(NM[a] || a)}</span><em>${when(wed)}</em></div><div${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${b}"` : ""}><span>${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? `Chapter ${FIN_EV[b].ch} · ${esc(FIN_EV[b].n)}` : esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div>${x === 9 ? `<div class="finrow" data-act="finWatch" data-k="ecl"><span>◐ The Eclipse · The Verdict</span><em>${when(sat + 864e5)}</em></div>` : ""}</div>`; }''',
    '''  const rA = `<div${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${a}"` : ""}><span>${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? `Chapter ${FIN_EV[a].ch} · ${esc(FIN_EV[a].n)}` : esc(NM[a] || a)}</span><em>${when(wed)}</em></div>`, tB = b0 ? sat : satL,
    rB = `<div${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${b}"` : ""}><span>${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? `Chapter ${FIN_EV[b].ch} · ${esc(FIN_EV[b].n)}` : esc(WB[b] ? WB[b].n : b)}</span><em>${when(tB)}</em></div>`;
  return `<div class="seafin"><small>★ SEASON FINALE</small>${tB < wed ? rB + rA : rA + rB}${x === 9 ? `<div class="finrow" data-act="finWatch" data-k="ecl"><span>◐ The Eclipse · The Verdict</span><em>${when(satL + 864e5)}</em></div>` : ""}</div>`; }''')
# the words
rep('the Saturday hunts between the great events (one boss each Saturday, 18:00 UTC) for 48 hours', 'the Monday hunts before the great events (one boss each Monday, 18:00 UTC) for 48 hours', 3)
rep('"the Saturday hunts"', '"the Monday hunts"')
rep('"Saturday world boss"', '"Monday world boss"')
rep('four Wednesday great events and four Saturday world bosses', 'four Monday world bosses and four Wednesday great events')
rep("Saturday's hunt is on! A world boss has risen, Commander. Open the Finder and let's track it down.", "Monday's hunt is on! A world boss has risen, Commander. Open the Finder and let's track it down.", 2)
rep("Saturday's hunt is on! The Pyramid Overlord has risen,", "Monday's hunt is on! The Pyramid Overlord has risen,", 2)
rep("The Brood Matriarch has nested for this Saturday's hunt.", "The Brood Matriarch has nested for this Monday's hunt.", 2)
rep("The Orbital Devourer is loose for this Saturday's hunt.", "The Orbital Devourer is loose for this Monday's hunt.", 2)
rep("World bosses hunt on Saturdays at eighteen hundred UTC, one each week, for forty-eight hours,", "World bosses hunt on Mondays at eighteen hundred UTC, one each week, for forty-eight hours,", 2)

# ---- 2. recall a garrison from the Cube ----
# Your stationed ships leave the Cube's garrison and fly home (a normal returning fleet). If yours were the last ships holding it, the
# Cube falls back to the Collective Warden and your alliance keeps the hold time it scored; the button says so before you confirm.
rep('''    <h2 class="sec">Defenders</h2>${cur.holder ? unitGrid(D.n) :''', '''    ${nxMineHTML(T, cur)}
    <h2 class="sec">Defenders</h2>${cur.holder ? unitGrid(D.n) :''')
rep('/* the super Cube\'s rules and prizes, shown every time it is opened */', '''/* v711 your own ships in the Cube's garrison, with a recall (two taps: the second confirms) */
function nxMineHTML(T, cur) { const g = live0 => live0 && cur.garrison && cur.garrison[G.me], mine = g(evActive(T)); if (!mine || !sumShips(mine)) return "";
  const last = Object.keys(cur.garrison).filter(u => sumShips(cur.garrison[u] || {})).length <= 1, ask = sheet && sheet.nxRecallAsk, h = homePlanet(), tt = h ? Math.max(60000, travelMs(NEXUS, h, mine)) : 0;
  return `<h2 class="sec">Your garrison</h2><div class="fcard"><div class="top"><b>■ Stationed at the Cube</b><span class="pill go">${fmt(sumShips(mine))} ships</span></div>${unitGrid(mine)}
    ${ask ? `<p class="note">${last ? `<b>Yours are the last ships holding the Cube.</b> If you recall them, the Cube falls back to the Collective Warden and ${esc(allyTag(S.ally))} stops scoring hold time (the time it already scored stays).` : "Your ships leave the garrison and fly home; the rest of the garrison keeps holding."} Home in about ${ftime(tt)}.</p>
      <div class="acts"><button class="btn red sm" data-act="nxRecall" data-ok="1">Recall ${fmt(sumShips(mine))} ships</button><button class="btn ghost sm" data-act="nxRecall" data-no="1">Keep them there</button></div>`
      : `<div class="acts"><button class="btn red sm" data-act="nxRecall">Recall to ${esc(S.homeName)}</button></div>`}</div>`; }
/* the super Cube's rules and prizes, shown every time it is opened */''')
rep('      <li>Stationed ships fly home when the event ends. Ships lost in the fight are lost.</li></ol>', '      <li>Stationed ships fly home when the event ends, or when you recall them. Ships lost in the fight are lost.</li></ol>')
rep('  nxCall: async () => {', '''  nxRecall: async d => { if (d.no) { sheet.nxRecallAsk = 0; return renderSheet(); } if (!d.ok) { sheet.nxRecallAsk = 1; return renderSheet(); } sheet.nxRecallAsk = 0;
    if (G.mode !== "online" || !G.db) return toast("Recalling needs the shared galaxy.", "warn"); const T = now(); if (!evActive(T)) return toast("The battle is over: your ships are already coming home.", "warn");
    try { const ref = G.db.doc("event/nexus"); for (let i = 0; i < 8; i++) { const r = await ref.acquire({ holder: G.me, ttlMs: 15000 }); if (r.acquired) break; await sleep(1500); }
      const snap = await ref.get(), w = evWeek(T), cur = snap.exists ? cleanNexus(snap.data()) : null, n = cur && cur.week === w ? cleanShips(cur.garrison[G.me] || {}) : {};
      if (!sumShips(n)) { if (cur) G.nexus = cur; renderSheet(); return toast("You have no ships stationed at the Cube.", "warn"); }
      delete cur.garrison[G.me]; const left = Object.keys(cur.garrison).some(u => sumShips(cur.garrison[u] || {}));
      if (!left && cur.holder) { cur.points[cur.holder] = (cur.points[cur.holder] || 0) + Math.max(0, T - cur.since); cur.holder = null; cur.since = 0; }
      await ref.set(cur); G.nexus = cur; const h = homePlanet(), tt = Math.max(60000, travelMs(NEXUS, h, n));
      S.fleets.push({ id: "f" + (S.seq++), pid: "nexus", mission: "station", n, out: T - tt, arrive: T, tt, back: T + tt, loot: null, phase: "back" });
      note(left ? `${fmt(sumShips(n))} ships recalled from the Cube. They're flying home.` : `${fmt(sumShips(n))} ships recalled from the Cube. It has fallen back to the Collective Warden.`, left ? "win" : "warn");
      dirty(); softRender(); renderSheet(); toast(`Recalled. Home in ${ftime(tt)}.`); } catch (e) { toast("Lost contact with the Cube. Try again.", "warn"); } },
  nxCall: async () => {''')
# the Fleets screen lists your Cube garrison too
rep('    <h2 class="sec">${label} · ${sorted.length}</h2>', '''    ${(() => { try { const T0 = now(), cur = nexusNow(T0), mine = evActive(T0) && cur.garrison && cur.garrison[G.me]; return mine && sumShips(mine) ? `<h2 class="sec">Stationed at the Cube</h2><div class="fcard"><div class="top"><b>■ The Cube · ${esc(allyTag(S.ally))} garrison</b><span class="pill go">${fmt(sumShips(mine))} ships</span></div><div class="route">${Object.entries(mine).filter(([, v]) => v).map(([k, v]) => `${fmt(v)} ${SH[k] ? SH[k].n : k}`).join(", ")}</div><div class="acts"><button class="btn sm" data-act="nexus">Open the Cube to recall</button></div></div>` : ""; } catch (e) { return ""; } })()}
    <h2 class="sec">${label} · ${sorted.length}</h2>''')
rep('const GAME_V = 710;', 'const GAME_V = 711;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
