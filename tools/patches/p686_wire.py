# v686: the Super Cube falls to one strong assault again (owner: "I used to be able to take it with me and 30 boys"). It still rises to
# meet a fleet stronger than it, but only as far as that fleet can still destroy it: the rise aims at a win, not at a share of its hull.
# A fleet weaker than the Warden itself still can't take it, and every assault wears it down for the week as before.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function cubeFight(A0, cur) { const D = nexusDefense(cur); if (!D.alien) return { D, res: simulate(A0(), D.stacks), rise: 1 }; const { res, rise } = riseFight(A0, () => nexusDefense(cur).stacks, cubeKilled, cubeIntegrity(cur) <= CUBE_BREAK, .5); return { D, res, rise }; }',
    'function cubeFight(A0, cur) { const D = nexusDefense(cur); if (!D.alien) return { D, res: simulate(A0(), D.stacks), rise: 1 }; const won = r => r.winner === "a", frac = r => won(r) ? 1 : Math.min(.9, cubeKilled(r));\n  let { res, rise } = riseFight(A0, () => nexusDefense(cur).stacks, frac, cubeIntegrity(cur) <= CUBE_BREAK, .99); /* v686 it rises only as far as this fleet can still destroy it */\n  if (!won(res) && rise > 1) { const r1 = simulate(A0(), nexusDefense(cur).stacks); if (won(r1)) { res = r1; rise = 1; } } return { D, res, rise }; }')
rep('const GAME_V = 685;', 'const GAME_V = 686;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
# v686 part 2: the alliance holding the Cube can call for reinforcements (owner). Any member of the holding alliance sounds the call
# (📣 on the Cube's page); for the next 20 minutes every member, wherever they are, can warp ships into the Cube's garrison: they
# arrive in 2 minutes and burn no fuel. The call goes to the alliance chat and shows as a band on the map and the planet.
s = open(p, encoding='utf-8').read()
rep('return { week: Math.floor(+d.week || 0), holder: typeof d.holder === "string" ? d.holder : null, since: +d.since || 0, garrison, points, wd: clamp(+d.wd || 0, 0, .8), ret }; // v117: ret = routed garrisons flying home',
    'const call = d.call && typeof d.call === "object" && typeof d.call.aly === "string" ? { by: String(d.call.by || ""), aly: d.call.aly, at: +d.call.at || 0, until: +d.call.until || 0 } : null; /* v686 */\n  return { week: Math.floor(+d.week || 0), holder: typeof d.holder === "string" ? d.holder : null, since: +d.since || 0, garrison, points, wd: clamp(+d.wd || 0, 0, .8), ret, call }; // v117: ret = routed garrisons flying home')
rep('function nexusNow(T = now()) {', '''const NX_CALL = 20 * 60e3, NX_WARP = 120e3; /* v686 the holders' call for reinforcements: 20 minutes; ships warp in within 2 minutes from anywhere, no fuel */
const nxCallOn = (T = now()) => { const cur = nexusNow(T), c = cur.call; return c && S && S.ally && c.aly === S.ally && cur.holder === S.ally && T < c.until && evActive(T) && myAlly() ? c : null; };
function nxCallBand(T) { const c = nxCallOn(T); if (!c) return ""; const by = c.by === G.me ? "You" : nameOf(c.by); return `<button class="omb fin" style="--fc:#c9a6ff" data-act="nxAnswer"><b>📣 THE CUBE CALLS</b><span>${esc(by)} · ${ftime(c.until - T)} left</span><i>🛡 Reinforce</i></button>`; }
function nexusNow(T = now()) {''')
rep('const pct = spdPct(), fuel = fuelFor(h, p, n, pct);', 'const pct = spdPct(), fuel = extra && extra.warp ? 0 : fuelFor(h, p, n, pct); /* v686 a warp to the Cube burns no fuel */')
rep('const f = sendFleet(NEXUS, n, nexusNow().holder === S.ally ? "nexusHold" : "nexusAtk"); if (!f) return;',
    'const wc = nexusNow().holder === S.ally && nxCallOn(), f = sendFleet(NEXUS, n, nexusNow().holder === S.ally ? "nexusHold" : "nexusAtk", wc ? { arrive: now() + NX_WARP, tt: NX_WARP, warp: 1 } : undefined); if (!f) return; /* v686 answering the call: a warp */')
rep('      ${hold && md === "solo" ? `<p class="note">Your alliance holds the Cube. Send more ships any time',
    '      ${hold ? (() => { const c = nxCallOn(T); return c ? `<div class="nxcall on"><b>📣 Reinforcements called</b><span>${esc(c.by === G.me ? "You" : nameOf(c.by))} called the alliance. Until the call ends (<b data-end="${c.until}">${ftime(c.until - T)}</b>), every member’s ships warp into the garrison in ${Math.round(NX_WARP / 60e3)} minutes from anywhere, with no fuel.</span></div>` : `<div class="nxcall"><span>Call every member of ${esc(allyTag(S.ally))} to the Cube: for ${Math.round(NX_CALL / 60e3)} minutes their ships warp straight into the garrison, wherever they are.</span><button class="btn amber" data-act="nxCall">📣 Call reinforcements</button></div>`; })() : ""}\n      ${hold && md === "solo" ? `<p class="note">Your alliance holds the Cube. Send more ships any time')
rep('hold ? "🛡 Reinforce the Cube" : "Launch assault"}</button>`;', 'hold ? (nxCallOn(T) && md === "solo" ? `🛡 Warp in · arrives in ${Math.round(NX_WARP / 60e3)} min` : "🛡 Reinforce the Cube") : "Launch assault"}</button>`;')
rep('  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */', '  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = nxCallBand(T); /* v686 */\n  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */')
rep('if (view === "base" && !battle) { hb = omenBand(T) + d1Band(T)', 'if (view === "base" && !battle) { hb = nxCallBand(T) + omenBand(T) + d1Band(T)')
rep('  nxMode: d => { if (sheet) { sheet.nxMode = d.v; sheet.oddsKey = null; renderSheet(); } },', '''  nxMode: d => { if (sheet) { sheet.nxMode = d.v; sheet.oddsKey = null; renderSheet(); } },
  nxAnswer: () => { openSheet({ type: "nexus" }); if (sheet) { sheet.nxMode = "solo"; renderSheet(); } }, /* v686 */
  nxCall: async () => { if (G.mode !== "online" || !G.db || !myAlly()) return toast("Calling the alliance needs the shared galaxy.", "warn"); const T = now(); if (!evActive(T) || nexusNow(T).holder !== S.ally) return toast("Only the alliance holding the Cube can call for reinforcements.", "warn"); if (nxCallOn(T)) return toast("The call is already out.", "warn");
    try { const ref = G.db.doc("event/nexus"); for (let i = 0; i < 8; i++) { const r = await ref.acquire({ holder: G.me, ttlMs: 15000 }); if (r.acquired) break; await sleep(1500); }
      const snap = await ref.get(), w = evWeek(T); const cur = snap.exists ? cleanNexus(snap.data()) : null; if (!cur || cur.week !== w || cur.holder !== S.ally) return toast("Your alliance no longer holds the Cube.", "warn");
      if (cur.call && cur.call.aly === S.ally && T < cur.call.until) { G.nexus = cur; renderSheet(); return toast("The call is already out.", "warn"); }
      cur.call = { by: G.me, aly: S.ally, at: T, until: T + NX_CALL }; await ref.set(cur); G.nexus = cur;
      try { await chatPost("a", null, { u: G.me, x: `📣 Reinforcements to the Cube! For the next ${Math.round(NX_CALL / 60e3)} minutes, send ships from the Cube's page: they warp into our garrison in ${Math.round(NX_WARP / 60e3)} minutes from anywhere, no fuel.`, t: T }, true); } catch (e) {}
      toast("The alliance has been called. For 20 minutes every member can warp ships into the Cube.", "win"); renderSheet(); } catch (e) { toast("The call didn't go out. Try again.", "warn"); } },''')
rep('.omb.fin b{color:var(--fc);white-space:nowrap}', '.omb.fin b{color:var(--fc);white-space:nowrap}\n.nxcall{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;padding:10px 12px;margin:8px 0;border:1px solid rgba(201,166,255,.45);border-radius:12px;background:rgba(40,20,70,.45);color:#e8dcff}\n.nxcall span{flex:1 1 220px;min-width:0;font-size:13px;line-height:1.4}\n.nxcall.on{border-color:#c9a6ff;box-shadow:0 0 14px rgba(201,166,255,.35)}\n.nxcall.on b{display:block;color:#c9a6ff;letter-spacing:.06em;width:100%}')
open(p, 'w', encoding='utf-8').write(s); print('ok2')
