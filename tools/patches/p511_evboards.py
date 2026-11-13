# v511 a leaderboard on every event page (owner). The Ranking tab already ranked the Galaxy War, the Battle for the Cube and the boss
# hunts; now Bonus Builder (days played), Online Bonus (time online today), Level Bonus (commander level), Daily Challenge (points
# today), Daily Login (streak), Achievements (points), VIP (VIP points) and Alliance Gifts (gifts sent, your alliance) rank too.
# Each commander's numbers ride on their player record (ev), so everyone sees the same boards.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('gw: S.gw && S.gw.i === gwIdx(now()) ? { i: S.gw.i, p: S.gw.pts } : null };', 'gw: S.gw && S.gw.i === gwIdx(now()) ? { i: S.gw.i, p: S.gw.pts } : null, ev: evPub() };')
rep('lvl: 0, tech: 0, gw: 0 }));', 'lvl: 0, tech: 0, gw: 0, ev: 0 }));')
JS = r'''/* v511 the event leaderboards: each commander's event numbers ride on their player record */
function evPub() { try { const ls = loginState(); return { d: utcDay(), bd: bonusState().days | 0, on: obMin(), sp: Math.round(soloState().pts || 0), ls: ls.claimed ? ls.streak : (ls.next > 1 ? ls.next - 1 : 0), vip: Math.round(vipPts()), ap: Math.round(achPts()) }; } catch (e) { return null; } }
const EVB = { builder: ["Days played", e => e.bd, v => `${fmt(v)} day${v === 1 ? "" : "s"}`], online: ["Online today", e => e.d === utcDay() ? e.on : 0, v => v >= 60 ? `${Math.floor(v / 60)} h ${v % 60} min` : `${v} min`],
  lvlb: ["Commander level", null, v => `Lv.${v}`], daily: ["Points today", e => e.d === utcDay() ? e.sp : 0, v => fmt(v)], login: ["Login streak", e => e.ls, v => `${fmt(v)} day${v === 1 ? "" : "s"}`],
  ach: ["Achievement points", e => e.ap, v => `${fmt(v)} AP`], vip: ["VIP points", e => e.vip, v => fmt(v)], gifts: ["Gifts sent", null, v => fmt(v)] };
function evBoard(k) { const D = EVB[k], rows = [], T = now();
  if (k === "gifts") { const a = myAlly(); if (!a) return []; const n = {}; for (const g of Object.values(a.gifts || {})) if (g && g.by) n[g.by] = (n[g.by] || 0) + 1; for (const u of Object.keys(a.members)) rows.push({ id: u, v: n[u] || 0, me: u === G.me }); }
  else { const mine = evPub() || {};
    for (const [uid, p] of Object.entries(G.players || {})) { if (uid === G.me || !p) continue; const v = k === "lvlb" ? (p.lvl | 0) : p.ev && typeof p.ev === "object" ? (+D[1](p.ev) || 0) : 0; if (v > 0 || k === "lvlb") rows.push({ id: uid, v }); }
    if (k === "lvlb") for (const b of BOTS) rows.push({ id: b.id, v: cmdLevel(botScore(b)), bot: 1 });
    rows.push({ id: G.me, v: k === "lvlb" ? cmdLevel(score()) : (+D[1](mine) || 0), me: 1 }); }
  return rows.sort((x, y) => y.v - x.v || (x.me ? -1 : y.me ? 1 : 0)); }
function evRankHTML(k) { const D = EVB[k], rows = evBoard(k), mi = rows.findIndex(r => r.me), show = rows.slice(0, 50); if (mi >= 50) show.push(rows[mi]);
  if (k === "gifts" && !myAlly()) return `<p class="note" style="padding:10px">Join an alliance to see who sends the most gifts.</p>`;
  return `<div class="evrank"><div class="evrh"><span>Rank</span><span>${k === "gifts" ? "Member" : "Commander"}</span><span>${esc(D[0])}</span></div>${show.map(r => { const pos = rows.indexOf(r) + 1; return `<div class="evrr${r.me ? " me" : ""}"><span>${pos <= 3 ? ["🥇", "🥈", "🥉"][pos - 1] : pos + "."}</span><span>${esc(r.me ? (G.myName || "You") + " (you)" : r.bot ? BOT_BY[r.id].name : nameOf(r.id))}${r.bot ? ' <i class="botk">bot</i>' : ""}</span><span>${D[2](r.v)}</span></div>`; }).join("")}</div>
    ${rows.length < 2 ? `<p class="note" style="padding:6px 10px">${k === "gifts" ? "Gifts your alliance members send show up here." : "Other commanders show up here as they play."}</p>` : ""}`; }
'''
rep('function shEvents() {', JS + 'function shEvents() {')
rep('  else if (k === "builder" || k === "online" || k === "lvlb") body = bonusBody(k, T);', '  else if (k === "builder" || k === "online" || k === "lvlb") body = tab === "rk" ? evRankHTML(k) : bonusBody(k, T);')
rep('  else if (k === "ach") { body = `<div class="evinfo">', '  else if (k === "ach" && tab === "rk") body = evRankHTML(k);\n  else if (k === "ach") { body = `<div class="evinfo">')
rep('  else { body = `<div class="evinfo">${oldEvSection(k, T)}</div>`; }', '  else { body = tab === "rk" && EVB[k] ? evRankHTML(k) : `<div class="evinfo">${oldEvSection(k, T)}</div>`; }')
s2 = re.sub(r"GAME_V = 510\b", "GAME_V = 511", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
