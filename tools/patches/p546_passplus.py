# v546 more Void Pass (owner: "Yes I want it all" to the pass ideas). On top of v542:
#  - Titles: free tier 15 gives "Void Walker", premium tier 25 the season's title ("Leviathan Slayer" in Season 1). Choose one on your
#    profile card; it shows under your name on the card and in Rankings (published as ttl).
#  - A season flagship look: premium tier 35 makes your flagship fly in the season's colours with its signature weapon (FS_LOOK vpa..vpf)
#    unless a full flagship set already gives it a stronger look.
#  - Buy a tier for ◆20, and bonus XP: ×1.5 in a season's last week (catch-up) and ×1.5 while a boss hunt is live (at most ×2).
#  - Season standings: your tier is published (vp {s, lv, xp}); the pass's Ranking tab lists commanders by tier. When a season ends, the
#    top 100 by tier get ◆20 (top 10 ◆50, first ◆100) and a "Top 100 · Season N" title.
#  - Alliance goal: your alliance's members' pass XP this season fills a shared bar; at 60K, 180K and 400K every member claims ◆10, ◆20 and
#    ◆40 (S.vpAg).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const VP_SEASONS = [["Season of the Leviathan", "#ff8a4a", "blacksun"], ["Season of the Cube", "#5dff6a", "voidbloom"], ["Season of the Pentarch", "#e2d4ff", "magnetar"], ["Season of the Starhive", "#ffb02a", "phoenix"], ["Season of the Kraken", "#c890ff", "kraken"], ["Season of the Wyrm", "#ffa040", "dragon"]];',
    'const VP_SEASONS = [["Season of the Leviathan", "#ff8a4a", "blacksun", "Leviathan Slayer"], ["Season of the Cube", "#5dff6a", "voidbloom", "Cubebreaker"], ["Season of the Pentarch", "#e2d4ff", "magnetar", "Sealbreaker"], ["Season of the Starhive", "#ffb02a", "phoenix", "Hivebane"], ["Season of the Kraken", "#c890ff", "kraken", "Kraken Hunter"], ["Season of the Wyrm", "#ffa040", "dragon", "Wyrmrider"]];\nconst VP_LOOKS = ["vpa", "vpb", "vpc", "vpd", "vpe", "vpf"], vpLookOf = si => VP_LOOKS[((si % 6) + 6) % 6]; /* v546 */')
# rewards: titles and the look
rep('''  if (!prem) return t % 10 === 0 ?''', '''  if (!prem && t === 15) return { shards: 5, title: "Void Walker" }; if (prem && t === 25) return { shards: 10, title: vpInfo(si)[3] }; if (prem && t === 35) return { shards: 10, look: si }; /* v546 */
  if (!prem) return t % 10 === 0 ?''')
rep('''r.skin ? `Exclusive skin: ${''', '''r.title ? `Title: “${r.title}”` : "", r.look != null ? `Season flagship look` : "", r.skin ? `Exclusive skin: ${''')
rep('if (r.skin) { S.pxOwn = S.pxOwn || {}; S.pxOwn[r.skin] = 1; } }', 'if (r.skin) { S.pxOwn = S.pxOwn || {}; S.pxOwn[r.skin] = 1; } if (r.title) { S.vpTitles = S.vpTitles || []; if (!S.vpTitles.includes(r.title)) S.vpTitles.push(r.title); if (!S.vpTitle) S.vpTitle = r.title; } if (r.look != null) S.vpLook = r.look; }')
rep('<span>${r.skin ? "🪐" :', '<span>${r.title ? "🎖" : r.look != null ? "✦" : r.skin ? "🪐" :')
# bonus XP
rep("  if (add) { const lv0 = Math.floor(v.xp / VP_XP); v.xp += add;", "  if (add) { add = Math.round(add * vpMul()); const lv0 = Math.floor(v.xp / VP_XP); v.xp += add;")
rep('function vpTick() {', '''const vpMul = (T = now()) => { let m = 1; if (vpEnd() - T < 7 * 864e5) m += .5; try { if ([1, 2, 3].some(g => wbGroupOn(g, T))) m += .5; } catch (e) {} return Math.min(2, m); }; /* v546 catch-up week and boss hunts */
function vpTick() {''')
# season end: standings reward, and the alliance goal
rep('''    v = S.vp = { s: si, xp: 0, pr: 0, cf: [], cp: [] }; dirty(); }''', '''    if (v && typeof v.s === "number" && (v.xp || 0) > 0) { try { const old = v.s, mine = Math.floor((v.xp || 0) / VP_XP), rows = Object.values(G.players || {}).filter(p => p && p.vp && p.vp.s === old).map(p => p.vp.xp || 0); const r = 1 + rows.filter(x => x > v.xp).length; if (r <= 100 && mine > 0) { const sh = r === 1 ? 100 : r <= 10 ? 50 : 20; S.shards = (S.shards || 0) + sh; S.vpTitles = S.vpTitles || []; const tt = `Top 100 · Season ${old + 1}`; if (!S.vpTitles.includes(tt)) S.vpTitles.push(tt); note(`Void Pass Season ${old + 1}: you finished #${r}. ◆${sh} and the “${tt}” title.`, "win"); } } catch (e) {} } /* v546 season standings */
    v = S.vp = { s: si, xp: 0, pr: 0, cf: [], cp: [] }; dirty(); }''')
JS = r'''
/* v546 the alliance's shared pass goal */
const VP_AG = [[60000, 10], [180000, 20], [400000, 40]];
function vpAllyXP() { const a = myAlly && myAlly(); if (!a) return 0; const si = vpSeason(); let n = 0; for (const u in a.members || {}) { const p = u === G.me ? { vp: { s: si, xp: (S.vp || {}).xp || 0 } } : (G.players || {})[u]; if (p && p.vp && p.vp.s === si) n += p.vp.xp || 0; } return n; }
const vpAgState = () => { const si = vpSeason(); if (!S.vpAg || S.vpAg.s !== si) S.vpAg = { s: si, got: [] }; return S.vpAg; };
const vpAgReady = () => { if (!S.ally) return []; const x = vpAllyXP(), g = vpAgState(); return VP_AG.map((m, i) => i).filter(i => x >= VP_AG[i][0] && !g.got.includes(i)); };
'''
rep('const vpReady = () => {', JS + 'const vpReady = () => {')
rep('if (v.pr && !v.cp.includes(i)) n++; } return n; }', 'if (v.pr && !v.cp.includes(i)) n++; } return n + vpAgReady().length; }')
# body: bonus chip, buy a tier, alliance goal, title picker hint
rep('''    ${ms("d", "Daily missions", dayEnd)}${ms("w", "Weekly missions", wkEnd)}''', '''    ${vpMul() > 1 ? `<div class="vpbonus">⚡ Bonus XP ×${vpMul()} right now${vpEnd() - T < 7 * 864e5 ? " · the season's final week" : ""}${(() => { try { return [1, 2, 3].some(g => wbGroupOn(g, T)) ? " · a boss hunt is live" : ""; } catch (e) { return ""; } })()}</div>` : ""}
    ${lv < VP_TIERS ? `<div class="vptier"><span>Need a push? Buy the next tier.</span><button class="btn ghost sm" data-act="vpBuyTier" ${(S.shards || 0) >= 20 ? "" : "disabled"}>+1 tier · ◆20</button></div>` : ""}
    ${S.ally ? (() => { const x = vpAllyXP(), g = vpAgState(), top = VP_AG[VP_AG.length - 1][0]; return `<div class="vpag"><div class="vpmh"><b>🛡 Alliance goal</b><span class="note">${fmt(x)} XP from your alliance</span></div><div class="vpagb"><i style="width:${Math.min(100, x / top * 100).toFixed(1)}%"></i>${VP_AG.map(([need]) => `<u style="left:${(need / top * 100).toFixed(1)}%"></u>`).join("")}</div><div class="vpagr">${VP_AG.map(([need, sh], i) => `<span class="${g.got.includes(i) ? "got" : x >= need ? "ready" : ""}">${fmt(need)} XP · ◆${sh}${g.got.includes(i) ? " ✓" : ""}</span>`).join("")}</div></div>`; })() : ""}
    ${ms("d", "Daily missions", dayEnd)}${ms("w", "Weekly missions", wkEnd)}''')
rep('''    if (n) { toast(`Void Pass: ${n} reward${n > 1 ? "s" : ""} claimed${sh ? ` (◆${sh} among them)` : ""}.`, "win"); try { SFX.research(); } catch (e) {} } }), /* v542 */''',
    '''    for (const i of vpAgReady()) { const g = vpAgState(); g.got.push(i); S.shards = (S.shards || 0) + VP_AG[i][1]; sh += VP_AG[i][1]; n++; } /* v546 the alliance goal */
    if (n) { toast(`Void Pass: ${n} reward${n > 1 ? "s" : ""} claimed${sh ? ` (◆${sh} among them)` : ""}.`, "win"); try { SFX.research(); } catch (e) {} } }), /* v542 */
  vpBuyTier: () => act(() => { const v = vpState(); if ((S.shards || 0) < 20 || v.xp >= VP_TIERS * VP_XP) return; S.shards -= 20; v.xp = (Math.floor(v.xp / VP_XP) + 1) * VP_XP; toast(`Tier ${Math.floor(v.xp / VP_XP)} reached.`, "win"); }),
  vpTitle: d => { S.vpTitle = d.v || null; dirty(); try { syncPlayer(); } catch (e) {} renderSheet(); },''')
# the ranking tab
rep('body = tab === "rk" ? `<p class="note" style="padding:10px">Season standings arrive with the next update. Climb the tiers in the meantime.</p>` : vpBody(T);',
    '''body = tab === "rk" ? (() => { const si = vpSeason(T), rows = Object.entries(G.players || {}).filter(([u, p]) => u !== G.me && p && p.vp && p.vp.s === si).map(([u, p]) => ({ u, xp: p.vp.xp || 0 })).concat([{ u: G.me, xp: (S.vp || {}).xp || 0, me: 1 }]).sort((a, b) => b.xp - a.xp), mi = rows.findIndex(r => r.me), show = rows.slice(0, 100); if (mi >= 100) show.push(rows[mi]);
      return `<p class="note" style="padding:6px 10px">The top 100 when the season ends get ◆20 (top 10: ◆50, first: ◆100) and a title.</p><div class="evrank"><div class="evrh"><span>Rank</span><span>Commander</span><span>Tier</span></div>${show.map(r => { const pos = rows.indexOf(r) + 1; return `<div class="evrr${r.me ? " me" : ""}"><span>${pos <= 3 ? ["🥇", "🥈", "🥉"][pos - 1] : pos + "."}</span><span>${esc(r.me ? (G.myName || "You") + " (you)" : nameOf(r.u))}</span><span>${Math.min(VP_TIERS, Math.floor(r.xp / VP_XP))}</span></div>`; }).join("")}</div>`; })() : vpBody(T);''')
# publish tier and title
rep('planets: myPlanets().length, ally: S.ally || null, last: now() });', 'planets: myPlanets().length, ally: S.ally || null, last: now(), vp: S.vp ? { s: S.vp.s, xp: S.vp.xp || 0 } : null, ttl: S.vpTitle || null }); /* v546 the pass tier and title */')
# titles on the profile card and in rankings
rep('<h2>${esc(nm)}</h2><p class="note">${titleOf(lvl)}', '<h2>${esc(nm)}</h2>${P.ttl ? `<div class="vpttl">🎖 ${esc(P.ttl)}</div>` : ""}<p class="note">${titleOf(lvl)}')
rep('''    ${me ? `<div class="row2"><button class="btn wide" data-act="avatars">Change avatar</button>''', '''    ${me && (S.vpTitles || []).length ? `<h2 class="sec">Title</h2><div class="vptsel">${[null].concat(S.vpTitles).map(t => `<button class="${(S.vpTitle || null) === t ? "on" : ""}" data-act="vpTitle" data-v="${esc(t || "")}">${t ? "🎖 " + esc(t) : "None"}</button>`).join("")}</div>` : ""}
    ${me ? `<div class="row2"><button class="btn wide" data-act="avatars">Change avatar</button>''')
rep('<span class="ln"><b>${esc(nm)}${r.bot ? \' <i class="botk">bot</i>\' : ""}</b>', '<span class="ln"><b>${esc(nm)}${r.bot ? \' <i class="botk">bot</i>\' : ""}</b>${r.p && r.p.ttl ? `<em class="lbttl">🎖 ${esc(r.p.ttl)}</em>` : ""}')
# the season flagship look
rep('''  sci: ["#4af0ff", "lance", "Ion lance"],''', '''  vpa: ["#ff8a4a", "lance", "Leviathan lance"], vpb: ["#5dff6a", "pulse", "Cube shockwave"], vpc: ["#e2d4ff", "lance", "Pentarch beam"], vpd: ["#ffb02a", "missiles", "Starhive swarm"], vpe: ["#c890ff", "pulse", "Kraken wave"], vpf: ["#ffa040", "lance", "Wyrm fire"], /* v546 season looks */
  sci: ["#4af0ff", "lance", "Ion lance"],''')
rep('''  for (const k in c) { if (!FS_LOOK[k] || !FS_SETS[k]) continue; const n = c[k], t = n >= fsSetMax(k) ? 3 : n >= 4 ? 2 : n >= 2 ? 1 : 0; if (t && (!best || t > best.t || (t === best.t && n > best.n))) best = { s: k, n, t }; } return best; }''',
    '''  for (const k in c) { if (!FS_LOOK[k] || !FS_SETS[k]) continue; const n = c[k], t = n >= fsSetMax(k) ? 3 : n >= 4 ? 2 : n >= 2 ? 1 : 0; if (t && (!best || t > best.t || (t === best.t && n > best.n))) best = { s: k, n, t }; }
  if (S && S.vpLook != null && (!best || best.t < 3)) best = { s: vpLookOf(S.vpLook), n: 0, t: 3 }; /* v546 the season look */ return best; }''')
rep('FS_SETS[lk.s][0]', '(FS_SETS[lk.s] || [(vpInfo(VP_LOOKS.indexOf(lk.s)) || ["Season"])[0]])[0]')
rep('function fsLookOf(f) { if (!f || !f.eq || !f.inv) return null;', 'function fsLookOf(f) { if (!f || !f.eq || !f.inv) return S && S.vpLook != null ? { s: vpLookOf(S.vpLook), n: 0, t: 3 } : null;')
css = '''
/* v546 more Void Pass */
.vpbonus{padding:8px 12px;border-radius:10px;border:1px solid rgba(255,207,90,.6);background:rgba(255,207,90,.12);color:#ffcf5a;font-weight:700;font-size:13px;margin-bottom:6px}
.vptier{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px;border-radius:10px;border:1px solid var(--line);background:rgba(4,10,16,.5);font-size:12.5px;margin-bottom:6px}
.vpag{padding:10px 12px;border-radius:12px;border:1px solid rgba(85,214,232,.4);background:rgba(4,12,20,.6);margin-bottom:6px}.vpagb{position:relative;height:10px;border-radius:5px;background:rgba(255,255,255,.08);margin:6px 0;overflow:visible}.vpagb i{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,#55d6e8,#9a7bff)}.vpagb u{position:absolute;top:-2px;width:2px;height:14px;background:#fff8}
.vpagr{display:flex;gap:6px;flex-wrap:wrap}.vpagr span{font-size:11px;padding:2px 7px;border-radius:7px;border:1px solid var(--line);color:var(--muted)}.vpagr span.ready{border-color:#5dff9a;color:#5dff9a}.vpagr span.got{color:#ffcf5a;border-color:rgba(255,207,90,.5)}
.vpttl{display:inline-block;margin:2px 0;padding:2px 8px;border-radius:7px;background:linear-gradient(90deg,rgba(255,207,90,.25),rgba(255,207,90,.05));color:#ffcf5a;font-size:12px;font-weight:700}
.vptsel{display:flex;gap:6px;flex-wrap:wrap}.vptsel button{padding:6px 10px;border-radius:9px;border:1px solid var(--line);background:rgba(4,10,16,.55);color:var(--fg);font-size:12.5px}.vptsel button.on{border-color:#ffcf5a;color:#ffcf5a;background:rgba(255,207,90,.12)}
.lbttl{display:block;font-style:normal;font-size:10.5px;color:#ffcf5a}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 545\b", "GAME_V = 546", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
