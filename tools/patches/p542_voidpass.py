# v542 the Void Pass (owner: "Do it all", idea #2, and "What else could be good content for Void pass season pass"). A 28-day season
# (VP_BASE Monday 2026-11-09 UTC, VP_LEN 28 days) with 40 tiers of 2,000 XP. XP comes from missions only: three daily missions (400 XP
# each, +300 for all three) and five weekly ones (2,000 XP each), picked from pools by the day/week, measured as the rise of a counter
# since the mission period began (S.stats, plus new counters: battlesWon, monKills, pvpWins, fleetsSent, wheelSpins, depContracts).
# Each tier pays a free reward and, with Premium (◆500 Void Shards until real-money packs exist), a premium one; premium totals ◆500 in
# shards back plus items, an officer, a forge box, and the season's exclusive planet skin at tier 40. Tiers are claimed (Claim all);
# anything earned and not claimed is paid out when the season ends. Lives in the Events hub as the first event, "Void Pass".
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''
/* ---------- v542 the Void Pass ---------- */
const VP_BASE = Date.UTC(2026, 10, 9), VP_LEN = 28 * 864e5, VP_TIERS = 40, VP_XP = 2000, VP_PREM = 500;
const VP_SEASONS = [["Season of the Leviathan", "#ff8a4a", "blacksun"], ["Season of the Cube", "#5dff6a", "voidbloom"], ["Season of the Pentarch", "#e2d4ff", "magnetar"], ["Season of the Starhive", "#ffb02a", "phoenix"], ["Season of the Kraken", "#c890ff", "kraken"], ["Season of the Wyrm", "#ffa040", "dragon"]];
const vpSeason = (T = now()) => Math.floor((T - VP_BASE) / VP_LEN), vpEnd = (i = vpSeason()) => VP_BASE + (i + 1) * VP_LEN, vpInfo = (i = vpSeason()) => VP_SEASONS[((i % VP_SEASONS.length) + VP_SEASONS.length) % VP_SEASONS.length];
const VP_DAILY = [["built", 2, "Finish 2 constructions"], ["researched", 1, "Finish a research"], ["shipsBuilt", 20, "Build 20 ships or defences"], ["battlesWon", 3, "Win 3 battles"], ["monKills", 1, "Slay a space monster"], ["hiveWins", 2, "Beat 2 Hive garrisons"], ["fleetsSent", 4, "Send 4 fleets"], ["caches", 2, "Haul in 2 salvage pods"], ["trades", 1, "Make a trade at the Supply Depot"], ["wheelSpins", 1, "Spin the Holo Glyph Wheel"], ["spdMin", 30, "Use 30 minutes of speed-ups"]];
const VP_WEEKLY = [["built", 15, "Finish 15 constructions"], ["researched", 5, "Finish 5 researches"], ["monKills", 6, "Slay 6 space monsters"], ["battlesWon", 20, "Win 20 battles"], ["bosses", 3, "Strike a boss 3 times"], ["pvpWins", 3, "Win 3 battles against commanders"], ["depContracts", 3, "Deliver 3 depot contracts"], ["shipsBuilt", 300, "Build 300 ships or defences"], ["fleetsSent", 25, "Send 25 fleets"], ["caches", 10, "Haul in 10 salvage pods"], ["spdMin", 300, "Use 5 hours of speed-ups"]];
const vpStat = k => k === "spdMin" ? Math.floor(((S.stats || {}).spdMs || 0) / 60000) : k === "battlesWon" ? ((S.rec || {}).w || 0) : ((S.stats || {})[k] || 0);
const vpPick = (pool, n, seed) => pool.map((m, i) => [hash(seed + "|" + i), m]).sort((a, b) => a[0] - b[0]).slice(0, n).map(x => x[1]);
const vpWeek = (T = now()) => Math.floor((T - VP_BASE) / (7 * 864e5));
function vpReward(i, prem, si = vpSeason()) { const t = i + 1;
  if (!prem) return t % 10 === 0 ? { shards: 15, item: "mb2" } : t % 5 === 0 ? { shards: 5 } : [{ item: "crateM" }, { item: "xb_bronze" }, { item: "crateC" }, { item: "xf_bronze" }, { item: "crateG" }, { item: "xr_bronze" }, { m: 60000 * Math.ceil(t / 8), c: 40000 * Math.ceil(t / 8), g: 15000 * Math.ceil(t / 8) }, { item: "xs_bronze" }][i % 8];
  if (t === VP_TIERS) return { shards: 100, skin: vpInfo(si)[2] };
  if (t === 10) return { shards: 10, item: "o_staff_7" }; if (t === 20) return { shards: 10, item: "mb3" }; if (t === 30) return { shards: 10, item: "pAll_gold" };
  return { shards: 10, item: ["xb_silver", "xs_silver", "xr_silver", "bf_silver", "mb2", "xf_gold", "boost5", "bm_gold", "bc_gold", "bg_gold"][i % 10] }; }
const vpRwText = r => [r.shards ? `◆${r.shards}` : "", r.item && SHOP[r.item] ? SHOP[r.item].n + (ITIERS[SHOP[r.item].tier] ? " " + ITIERS[SHOP[r.item].tier][1] : "") : "", r.m ? `${fmt(r.m)} metal, ${fmt(r.c)} crystal, ${fmt(r.g)} gas` : "", r.skin ? `Exclusive skin: ${(typeof PXS !== "undefined" && PXS[r.skin] && PXS[r.skin].n) || r.skin}` : ""].filter(Boolean).join(" + ");
function vpGrant(r) { if (r.shards) S.shards = (S.shards || 0) + r.shards; if (r.item && SHOP[r.item]) giveItem(r.item); if (r.m) { S.res.m += r.m; S.res.c += r.c; S.res.g += r.g; } if (r.skin) { S.pxOwn = S.pxOwn || {}; S.pxOwn[r.skin] = 1; } }
function vpState(T = now()) { const si = vpSeason(T); let v = S.vp;
  if (!v || v.s !== si) { if (v && typeof v.s === "number") { const lv = Math.min(VP_TIERS, Math.floor((v.xp || 0) / VP_XP)); let n = 0; for (let i = 0; i < lv; i++) { if (!(v.cf || []).includes(i)) { vpGrant(vpReward(i, false, v.s)); n++; } if (v.pr && !(v.cp || []).includes(i)) { vpGrant(vpReward(i, true, v.s)); n++; } } if (n) note(`Void Pass: ${n} unclaimed reward${n > 1 ? "s" : ""} from last season added to your stores.`, "win"); }
    v = S.vp = { s: si, xp: 0, pr: 0, cf: [], cp: [] }; dirty(); }
  const day = utcDay(), wk = vpWeek(T), snap = () => { const o = {}; for (const [k] of VP_DAILY.concat(VP_WEEKLY)) o[k] = vpStat(k); return o; };
  if (!v.d || v.d.day !== day) { v.d = { day, base: snap(), done: [] }; dirty(); } if (!v.w || v.w.wk !== wk) { v.w = { wk, base: snap(), done: [] }; dirty(); }
  return v; }
const vpMissions = (v, kind) => { const daily = kind === "d", L = daily ? vpPick(VP_DAILY, 3, "vpd" + v.d.day) : vpPick(VP_WEEKLY, 5, "vpw" + v.w.wk), P = daily ? v.d : v.w;
  return L.map(([k, need, t]) => ({ k, need, t, have: Math.min(need, Math.max(0, vpStat(k) - (P.base[k] || 0))), done: P.done.includes(k), xp: daily ? 400 : 2000 })); };
function vpTick() { if (!S || !G.ready) return; try { const v = vpState(); let add = 0, msg = [];
  for (const [kind, P] of [["d", v.d], ["w", v.w]]) for (const m of vpMissions(v, kind)) if (!m.done && m.have >= m.need) { P.done.push(m.k); add += m.xp; msg.push(m.t); }
  if (v.d.done.length >= 3 && !v.d.all) { v.d.all = 1; add += 300; msg.push("All three daily missions"); }
  if (add) { const lv0 = Math.floor(v.xp / VP_XP); v.xp += add; dirty(); const lv1 = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)); toast(`Void Pass +${fmt(add)} XP · ${msg[0]}${msg.length > 1 ? ` and ${msg.length - 1} more` : ""}${lv1 > lv0 ? `. Tier ${lv1} reached!` : ""}`, "win"); if (lv1 > lv0) try { SFX.research(); } catch (e) {} } } catch (e) {} }
setInterval(vpTick, 5000);
const vpReady = () => { try { const v = vpState(), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)); let n = 0; for (let i = 0; i < lv; i++) { if (!v.cf.includes(i)) n++; if (v.pr && !v.cp.includes(i)) n++; } return n; } catch (e) { return 0; } };
function vpBanner(T) { const v = vpState(T), si = vpSeason(T), [nm, col] = vpInfo(si), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)), into = lv >= VP_TIERS ? VP_XP : v.xp - lv * VP_XP;
  return `<div class="evban vpban" style="--vc:${col}"><div class="vpglyph" aria-hidden="true">${"ᚠᚱᛉᛗᚲᛟᚷᛞ".split("").map((g, i) => `<i style="--a:${i * 45}deg">${g}</i>`).join("")}</div>
    <div class="vptop"><span class="vlive on">SEASON ${si + 1}</span><small>Ends in <b data-end="${vpEnd(si)}">${ftime(vpEnd(si) - T)}</b></small></div>
    <div class="vpbot"><b>Void Pass</b><em>${esc(nm)}</em><div class="vplv"><span>Tier <b>${lv}</b>/${VP_TIERS}</span><div class="vpxp"><i style="width:${(into / VP_XP * 100).toFixed(1)}%"></i></div><small>${fmt(into)} / ${fmt(VP_XP)} XP</small></div></div>${v.pr ? '<span class="vpprem">♛ PREMIUM</span>' : ""}</div>`; }
function vpBody(T) { const v = vpState(T), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)), si = vpSeason(T), skin = vpInfo(si)[2];
  const ms = (kind, head, end) => `<div class="vpms"><div class="vpmh"><b>${head}</b><span class="note">resets in <b data-end="${end}">${ftime(end - T)}</b></span></div>${vpMissions(v, kind).map(m => `<div class="vpm${m.done ? " done" : ""}"><div><b>${esc(m.t)}</b><div class="vpmb"><i style="width:${(m.have / m.need * 100).toFixed(0)}%"></i></div></div><span>${m.done ? "✓" : `${fmt(m.have)}/${fmt(m.need)}`}<small>+${fmt(m.xp)} XP</small></span></div>`).join("")}${kind === "d" ? `<p class="note">All three today: +300 XP bonus${v.d.all ? " ✓" : ""}.</p>` : ""}</div>`;
  const dayEnd = Date.UTC(new Date(T).getUTCFullYear(), new Date(T).getUTCMonth(), new Date(T).getUTCDate() + 1), wkEnd = VP_BASE + (vpWeek(T) + 1) * 7 * 864e5;
  const cell = (i, prem) => { const r = vpReward(i, prem, si), got = (prem ? v.cp : v.cf).includes(i), open = i < lv, lock = prem && !v.pr; return `<div class="vpc${prem ? " p" : ""}${got ? " got" : open && !lock ? " ready" : ""}${lock ? " lock" : ""}"><span>${r.skin ? "🪐" : r.shards && !r.item ? "◆" : r.m ? "▣" : "🎁"}</span><small>${esc(vpRwText(r))}</small>${got ? "<em>✓</em>" : lock ? "<em>♛</em>" : ""}</div>`; };
  const track = Array.from({ length: VP_TIERS }, (_, i) => `<div class="vpt${i < lv ? " on" : ""}${i === lv ? " cur" : ""}"><b>${i + 1}</b>${cell(i, false)}${cell(i, true)}</div>`).join("");
  return `<div class="evinfo vpw">
    ${v.pr ? "" : `<div class="vpbuy"><div><b>♛ Unlock Premium</b><small>A second reward on every tier: ◆${VP_PREM} back in shards over the season, speed-ups, boosters, an officer, forge boxes and the exclusive <b>${esc((typeof PXS !== "undefined" && PXS[skin] && PXS[skin].n) || skin)}</b> planet skin at tier ${VP_TIERS}. Tiers you've already reached pay out at once.</small></div><button class="btn amber" data-act="vpPrem" ${(S.shards || 0) >= VP_PREM ? "" : "disabled"}>◆${VP_PREM}</button></div>`}
    ${ms("d", "Daily missions", dayEnd)}${ms("w", "Weekly missions", wkEnd)}
    <div class="vpmh"><b>Rewards</b><span class="note">Free · Premium</span></div><div class="vptrack">${track}</div>
    <p class="note">XP comes from missions. Rewards you reach and don't claim are paid out when the season ends.</p></div>`; }
'''
rep('/* v539 Events lives in the hub', JS + '/* v539 Events lives in the hub')
rep('const EVS = [["sboss", "Super Boss Hunt", "☠"],', 'const EVS = [["pass", "Void Pass", "❖"], ["sboss", "Super Boss Hunt", "☠"],')
rep('  if (k === "ach") return achReady();', '  if (k === "pass") return vpReady(); /* v542 */\n  if (k === "ach") return achReady();')
rep('function evBanner(k, T) { if (k === "sboss") return sbBanner(T);', 'function evBanner(k, T) { if (k === "pass") return vpBanner(T); /* v542 */ if (k === "sboss") return sbBanner(T);')
rep('  else if (k === "builder" || k === "online" || k === "lvlb") body = tab === "rk" ? evRankHTML(k) : bonusBody(k, T);', '''  else if (k === "pass") { body = tab === "rk" ? `<p class="note" style="padding:10px">Season standings arrive with the next update. Climb the tiers in the meantime.</p>` : vpBody(T); const n = vpReady(); claim = `<button class="btn ${n ? "amber" : "ghost"} evclaim" data-act="vpClaim" ${n ? "" : "disabled"}>${n ? `Claim all · ${n} reward${n > 1 ? "s" : ""}` : "Claim"}</button>`; } /* v542 */
  else if (k === "builder" || k === "online" || k === "lvlb") body = tab === "rk" ? evRankHTML(k) : bonusBody(k, T);''')
rep('  evPick: d => {', '''  vpClaim: () => act(() => { const v = vpState(), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)); let n = 0, sh = 0; for (let i = 0; i < lv; i++) { if (!v.cf.includes(i)) { const r = vpReward(i, false); vpGrant(r); sh += r.shards || 0; v.cf.push(i); n++; } if (v.pr && !v.cp.includes(i)) { const r = vpReward(i, true); vpGrant(r); sh += r.shards || 0; v.cp.push(i); n++; } }
    if (n) { toast(`Void Pass: ${n} reward${n > 1 ? "s" : ""} claimed${sh ? ` (◆${sh} among them)` : ""}.`, "win"); try { SFX.research(); } catch (e) {} } }), /* v542 */
  vpPrem: () => act(() => { const v = vpState(); if (v.pr) return; if ((S.shards || 0) < VP_PREM) return toast(`Premium costs ◆${VP_PREM} Void Shards.`, "warn"); S.shards -= VP_PREM; v.pr = 1; bump("shopBuys"); vipAdd(VP_PREM * 10); toast("Void Pass Premium unlocked! Claim the premium rewards for every tier you've reached.", "win"); try { SFX.fanfare(true); } catch (e) {} }),
  evPick: d => {''')
# the new counters
rep('  S.rec = S.rec || { w: 0, l: 0, d: 0 }; if (rep.winner === "draw") S.rec.d++; else if (repWin(rep)) S.rec.w++; else S.rec.l++;',
    '  S.rec = S.rec || { w: 0, l: 0, d: 0 }; if (rep.winner === "draw") S.rec.d++; else if (repWin(rep)) { S.rec.w++; if (rep.mon) bump("monKills"); if ((rep.kind === "defense" || rep.kind === "raid" ? (rep.aUids || []) : [rep.dUid]).some(u => humanFoe(u))) bump("pvpWins"); } else S.rec.l++; /* v542 the pass counters */')
rep('  S.fleets.push(f);\n  if (Object.keys(n).some(k => CLASS_OF[k] === "frigate"', '  S.fleets.push(f); bump("fleetsSent"); /* v542 */\n  if (Object.keys(n).some(k => CLASS_OF[k] === "frigate"')
rep('  act(() => { S.shopFree = shopDay(); S.wheelPend = idx; }); crumb("glyph wheel spun");', '  act(() => { S.shopFree = shopDay(); S.wheelPend = idx; bump("wheelSpins"); }); crumb("glyph wheel spun");')
rep('S.res[C.r] -= C.amt; S.depC = C.day;', 'S.res[C.r] -= C.amt; S.depC = C.day; bump("depContracts");')
css = '''
/* v542 the Void Pass */
.vpban{height:auto;min-height:190px;border:1.5px solid color-mix(in srgb,var(--vc) 70%,transparent);border-radius:14px;background:radial-gradient(120% 90% at 80% 20%,color-mix(in srgb,var(--vc) 32%,#0b0f24),#05070f 70%);box-shadow:0 0 24px color-mix(in srgb,var(--vc) 30%,transparent);overflow:hidden}
.vpglyph{position:absolute;right:-30px;top:50%;width:220px;height:220px;margin-top:-110px;border-radius:50%;border:1px solid color-mix(in srgb,var(--vc) 55%,transparent);animation:gwring 40s linear infinite;opacity:.85}
.vpglyph i{position:absolute;left:50%;top:50%;font-style:normal;font-size:22px;color:var(--vc);text-shadow:0 0 10px var(--vc);transform:rotate(var(--a)) translateY(-96px) rotate(calc(-1 * var(--a)))}
.vptop{position:absolute;top:10px;left:12px;right:12px;display:flex;gap:8px;align-items:center}.vptop small{font-size:11.5px;color:#d6e2ea}
.vpbot{position:relative;padding:44px 12px 12px;display:flex;flex-direction:column;gap:3px;max-width:72%}.vpbot>b{font:800 28px var(--f-display,sans-serif);letter-spacing:.06em;color:#fff;text-shadow:0 0 16px var(--vc)}.vpbot>em{font-style:normal;color:color-mix(in srgb,var(--vc) 60%,#fff);font-size:13px}
.vplv{display:grid;grid-template-columns:auto minmax(0,1fr);gap:2px 8px;align-items:center;margin-top:6px}.vplv span{font-size:12px;color:#d6e2ea}.vplv span b{font-size:18px;color:#fff}.vplv small{grid-column:2;font-size:10.5px;color:#aab8c4}
.vpxp{height:10px;border-radius:5px;background:rgba(0,0,0,.55);overflow:hidden;border:1px solid color-mix(in srgb,var(--vc) 50%,transparent)}.vpxp i{display:block;height:100%;background:linear-gradient(90deg,#fff8,var(--vc));box-shadow:0 0 8px var(--vc)}
.vpprem{position:absolute;right:10px;bottom:10px;font-size:10.5px;font-weight:800;letter-spacing:.1em;padding:3px 8px;border-radius:7px;background:#ffcf5a;color:#1a1000}
.vpbuy{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:12px;border-radius:14px;border:1px solid rgba(255,207,90,.6);background:linear-gradient(110deg,rgba(255,207,90,.16),rgba(8,14,22,.9));margin-bottom:8px}.vpbuy b{color:#ffcf5a}.vpbuy small{display:block;font-size:12px;color:var(--muted);margin-top:2px}
.vpms{display:flex;flex-direction:column;gap:6px;margin:8px 0}.vpmh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-top:6px}.vpmh>b{font-size:15px}
.vpm{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:9px 11px;border-radius:11px;border:1px solid var(--line);background:rgba(4,10,16,.55)}.vpm b{font-size:13px}.vpm>span{text-align:right;font-weight:700;font-size:13px;font-variant-numeric:tabular-nums}.vpm>span small{display:block;font-weight:400;font-size:10.5px;color:var(--cyan)}
.vpmb{height:6px;border-radius:3px;background:rgba(255,255,255,.08);margin-top:5px;overflow:hidden}.vpmb i{display:block;height:100%;background:var(--cyan)}.vpm.done{border-color:rgba(93,255,154,.5)}.vpm.done .vpmb i{background:#5dff9a}.vpm.done>span{color:#5dff9a}
.vptrack{display:flex;flex-direction:column;gap:5px;max-height:460px;overflow-y:auto;padding-right:2px}
.vpt{display:grid;grid-template-columns:34px minmax(0,1fr) minmax(0,1fr);gap:6px;align-items:stretch}.vpt>b{display:grid;place-items:center;border-radius:9px;background:rgba(255,255,255,.05);font-size:13px;color:var(--muted)}.vpt.on>b{background:rgba(85,214,232,.2);color:var(--cyan)}.vpt.cur>b{box-shadow:0 0 0 1.5px var(--cyan)}
.vpc{position:relative;display:flex;gap:6px;align-items:center;padding:6px 8px;border-radius:9px;border:1px solid var(--line);background:rgba(4,10,16,.55);min-height:44px}.vpc span{font-size:16px}.vpc small{font-size:10.5px;line-height:1.25;color:#cfdbe4}
.vpc.p{border-color:rgba(255,207,90,.35);background:linear-gradient(110deg,rgba(255,207,90,.08),rgba(4,10,16,.55))}.vpc.ready{border-color:#5dff9a;box-shadow:0 0 10px rgba(93,255,154,.3)}.vpc.got{opacity:.55}.vpc.lock{opacity:.6}
.vpc em{position:absolute;top:3px;right:6px;font-style:normal;font-size:11px;color:#5dff9a}.vpc.lock em{color:#ffcf5a}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 541\b", "GAME_V = 542", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
