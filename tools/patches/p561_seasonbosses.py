# v561 the boss calendar follows the seasons (owner: "Boss schedule will have to fit new season schedule right?"). Each 4-week Void Pass
# season holds four Wednesdays and four Saturdays. Weeks 1-3 bring other bosses in turn; week 4 is the season finale with the season's
# own headline boss: Leviathan: Khezaroth + the Event Horizon Wyrm (the serpent on the season banner), Cube: Cube Devastation + the
# Pyramid Overlord, Pentarch: the Elemental Convergence + the Void Warden, Starhive: Aexion + the Brood Matriarch, Kraken: Medusara +
# the Orbital Devourer, Wyrm: Vaelthar + the Event Horizon Wyrm. Nothing had run yet (the first Wednesday is Nov 18), so no one's
# progress moves. The Void Pass shows the coming finale; the Boss Lab marks finale days.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''const rotW = T => Math.floor((T - ROT0) / WEEK), rotKey = w => w < 0 ? null : ROT[w % ROT.length], rotWs = T => Math.floor((T - ROTS0) / WEEK), rotKeyS = w => w < 0 ? null : ROTS[w % ROTS.length];
const rotStartOf = (key, T) => { const sm = ROTS.includes(key), L = sm ? ROTS : ROT, B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= L.length; i++) { const w = W - i; if (w < 0) return null; if (L[w % L.length] === key) return B + w * WEEK; } return null; };
const rotNextOf = (key, T) => { const sm = ROTS.includes(key), L = sm ? ROTS : ROT, B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + L.length + 1; w++) { const s0 = B + w * WEEK; if (L[w % L.length] === key && s0 > T) return s0; } return T + WEEK; };''',
'''/* v561 the calendar follows the seasons: rotation week w is week (w + 1) of the season calendar (season 1 began on Monday Nov 9; its
   first Wednesday had no event). Week 4 of every season is its finale. */
const SEA_FIN = [["khz", "wym"], ["dv", "ovl"], ["conv", "war"], ["aex", "brd"], ["med", "dev"], ["vae", "wym"]], ROT_SEA0 = Date.UTC(2026, 10, 9);
const SEA_PLAN = {}; function seaPlan(si, sat) { const key = si + (sat ? "s" : "w"); if (SEA_PLAN[key]) return SEA_PLAN[key];
  if (si === 0) return (SEA_PLAN[key] = sat ? ["ovl", "ovl", "dev", "wym"] : ["vae", "vae", "aex", "khz"]); /* season 1 keeps the first dates already announced (Vaelthar Nov 18, the Overlord Nov 21) */
  const x = ((si % 6) + 6) % 6, L = sat ? ROTS : ROT, fin = SEA_FIN[x][sat ? 1 : 0], pf = SEA_FIN[(x + 5) % 6][sat ? 1 : 0], pool = L.filter(k => k !== fin && k !== pf), o = ((si * 3) % pool.length + pool.length) % pool.length;
  const p = [0, 1, 2].map(i => pool[(o + i) % pool.length]); if (p[0] === pf) [p[0], p[1]] = [p[1], p[0]]; return (SEA_PLAN[key] = [...p, fin]); }
const rotW = T => Math.floor((T - ROT0) / WEEK), rotKey = w => w < 0 ? null : seaPlan(Math.floor((w + 1) / 4), false)[(w + 1) % 4], rotWs = T => Math.floor((T - ROTS0) / WEEK), rotKeyS = w => w < 0 ? null : seaPlan(Math.floor((w + 1) / 4), true)[(w + 1) % 4];
const rotFinale = s0 => Math.floor((s0 - ROT_SEA0) / WEEK) % 4 === 3;
const rotStartOf = (key, T) => { const sm = ROTS.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= 24; i++) { const w = W - i; if (w < 0) return null; if (K(w) === key) return B + w * WEEK; } return null; };
const rotNextOf = (key, T) => { const sm = ROTS.includes(key), K = sm ? rotKeyS : rotKey, B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + 25; w++) { const s0 = B + w * WEEK; if (K(w) === key && s0 > T) return s0; } return T + WEEK; };''')
rep('DV_FIRST = ROT0 + WEEK /* v469 the second Wednesday of the rotation */', 'DV_FIRST = ROT0 /* v469; v561 wherever the season calendar puts it */')
# the Boss Lab
rep('''<div class="note">${live(k) ? "<b style=\\"color:#7dff9a\\">● live now</b>" : `${new Date(at)''', '''<div class="note">${rotFinale(at) && !live(k) ? '<b style="color:#ffd36b">★ Season finale</b> · ' : ""}${live(k) ? "<b style=\\"color:#7dff9a\\">● live now</b>" : `${new Date(at)''')
rep('<p class="note">Wednesdays: the great events in turn (each back every ${ROT.length} weeks). Saturdays between them: the world bosses in turn (each back every ${ROTS.length} weeks). All at 18:00 UTC.',
    '<p class="note">The calendar follows the Void Pass seasons: each season has four Wednesday great events and four Saturday world bosses, and its last week is the finale, with the bosses of that season. All at 18:00 UTC.')
rep('comes with the Wednesday boss rotation, every ${ROT.length} weeks, at', 'comes with the season calendar of Wednesday great events, at')
# the coming finale on the Void Pass
rep('function vpBody(T) {', '''function seaFinHTML(T) { try { const si = vpSeason(T), x = ((si % 6) + 6) % 6, w = 4 * si + 2, wed = ROT0 + w * WEEK, sat = ROTS0 + w * WEEK; if (T > sat + 48 * 3600e3) return ""; /* v561 */
  const NM = { vae: "Vaelthar, the Celestial Ruin", aex: "Aexion, the Warform Sovereign", khz: "Khezaroth, the Dark Matter Sphinx", med: "Medusara, the Petrified Star", dv: "Cube Devastation", conv: "The Elemental Convergence" }, [a, b] = SEA_FIN[x];
  const d = t => new Date(t).toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" }), when = t => T >= t ? "<b style=\\"color:#7dff9a\\">now</b>" : `${d(t)} · in <b data-end="${t}">${ftime(t - T)}</b>`;
  return `<div class="seafin"><small>★ SEASON FINALE</small><div><span>${esc(NM[a] || a)}</span><em>${when(wed)}</em></div><div><span>${esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div></div>`; } catch (e) { return ""; } }
function vpBody(T) { return seaFinHTML(T) + vpBody0(T); }
function vpBody0(T) {''')
rep('/* v560 the season pack */\n.cbn.art', '''/* v560 the season pack */
.seafin{margin:10px 0;padding:10px 12px;border-radius:12px;border:1px solid rgba(255,211,107,.45);background:linear-gradient(110deg,rgba(255,180,60,.16),rgba(10,12,22,.9))}.seafin small{color:#ffd36b;letter-spacing:.12em;font-weight:700}
.seafin div{display:flex;justify-content:space-between;gap:10px;margin-top:4px;font-size:13.5px}.seafin span{color:#fff;font-weight:600;min-width:0}.seafin em{font-style:normal;color:var(--muted);white-space:nowrap}
.cbn.art''')
s2 = re.sub(r"GAME_V = 560\b", "GAME_V = 561", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
