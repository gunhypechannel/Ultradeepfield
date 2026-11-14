# v566 the Advisor, alive (owner: "Make the advisor sound alive, like a person that displays all emotions and tone levels ... she is the
# biggest hook to this whole experience and I want her to be perfect").
# 1) She greets you: once per session (at most every 6 hours) by time of day (morning, afternoon, evening, late night), and warmly
#    when you come back after three days or more. Variants never repeat back to back.
# 2) She reacts: the season starting and its finale, Void Pass Premium and tier 40, the Glyph Wheel's rare spins and jackpots, epic
#    cache finds, the Wardrobe, the Vault and the Fleet Registry the first time, every Titan the first time it is built, the first
#    Titan Core, the 3D Titan viewer, and the Titans' signature moves in battle (voice only, once per battle).
# 3) She shows how she feels: every line carries a mood (calm, warm, playful, excited, urgent, fierce, awe, grave, tender) that tints
#    her hologram's glow and sets the pace of her talking shimmer. The new lines are recorded in that mood (docs/voicelab.html MOODS).
# Out-of-date note lines (the "x_" and "greet_" news) stay out of the event log.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
L = json.load(open('tools/patches/p566_lines.json'))
NEWS = {x['id']: x['line'] for x in L if x.get('id')}
MOOD = {x['line']: x['mood'] for x in L}
rep('const ADV_NEWS = {', 'const ADV_NEWS = {' + json.dumps(NEWS, ensure_ascii=False)[1:-1] + ', ')
rep('G.newsQ.shift(); const L = ADV_NEWS[n.id]; note(L.replace(/^Commander, /, ""), "info"); advHolo(L);', 'G.newsQ.shift(); const L = ADV_NEWS[n.id]; if (!/^(x|greet)_/.test(n.id)) note(L.replace(/^Commander, /, ""), "info"); advHolo(L);')
# moods: a table for the new lines, a reading of the rest
rep('function advHolo(line, force) {', '''/* v566 her moods */
const ADV_MOOD_L = ''' + json.dumps(MOOD, ensure_ascii=False) + ''';
function advMood(line) { const m = ADV_MOOD_L[line]; if (m) return m; const t = String(line || "");
  if (/!/.test(t) && /(attack|incoming|brace|hurry|watch out|under fire|now!|run|careful|shields)/i.test(t)) return "urgent"; if (/!/.test(t)) return "excited";
  if (/(fallen|lost|destroyed|dead|never|warning|darkness|vanished|price|end)/i.test(t)) return "grave"; if (/\\.\\.\\./.test(t)) return "tender"; if (/\\?/.test(t)) return "warm"; return "calm"; }
const advPk = (pre, n) => { G.advLast = G.advLast || {}; let i = Math.floor(Math.random() * n) + 1; if (n > 1 && G.advLast[pre] === i) i = i % n + 1; G.advLast[pre] = i; return pre + i; };
function advOnce(k) { S.advOnce = S.advOnce || {}; if (S.advOnce[k]) return false; S.advOnce[k] = now(); dirty(); return true; }
function advLive() { if (!S || !G.ready) return; const T = now(); S.advOnce = S.advOnce || {};
  if (!G.greeted && !tutOn() && !battle) { G.greeted = 1; if (T - (S.greetAt || 0) > 6 * 3600e3) { S.greetAt = T; dirty(); const h = new Date().getHours(), away = (G.awayMs || 0) >= 3 * 864e5;
      advNews(away ? advPk("greet_away", 2) : h < 5 ? advPk("greet_n", 3) : h < 12 ? advPk("greet_m", 3) : h < 18 ? advPk("greet_a", 2) : h < 22 ? advPk("greet_e", 2) : advPk("greet_n", 3)); } }
  const si = vpSeason(T); if (S.advSea == null) { S.advSea = si; dirty(); } else if (S.advSea !== si) { S.advSea = si; dirty(); advNews("x_sea_new", "sea:" + si); }
  { const w = rotW(T), s0 = ROT0 + w * WEEK, ws = rotWs(T), s1 = ROTS0 + ws * WEEK; if (w >= 0 && rotFinale(s0) && T >= s0 && T - s0 < 24 * 3600e3) advNews("x_fin_w", "finw:" + s0, { act: "events" }, "Season finale"); if (ws >= 0 && rotFinale(s1) && T >= s1 && T - s1 < 24 * 3600e3) advNews("x_fin_s", "fins:" + s1, { act: "events" }, "Season finale"); }
  try { const v = vpState(T); if (Math.floor(v.xp / VP_XP) >= VP_TIERS && advOnce("vp40:" + si)) advNews("x_vp40"); } catch (e) {}
  if ((S.tcore || 0) > 0 && advOnce("tcore")) advNews("x_tcore");
  for (const k of ["armageddon", "sovereign", "harbinger"]) { let n = 0; try { n = own(k); } catch (e) {} if (n > 0 && advOnce("tb:" + k)) { advNews("x_tb_" + k); break; } } }
setInterval(() => { try { advLive(); } catch (e) {} }, 8000);
function advHolo(line, force) {''')
# the hologram shows her mood
rep("  G.holoSaid[line] = T0; G.holoCur = line; let w = $(\"#advh\");", "  G.holoSaid[line] = T0; G.holoCur = line; let w = $(\"#advh\"); try { document.documentElement.dataset.advMood = advMood(line); } catch (e) {} /* v566 */")
rep('$("#advt").textContent = advLines[0]; speak(advLines[0]);', '$("#advt").textContent = advLines[0]; try { document.documentElement.dataset.advMood = advMood(advLines[0]); } catch (e) {} speak(advLines[0]);', 2)
CSS = '''/* v566 her moods: the glow round her hologram and the pace of her talking shimmer */
:root{--amood:#7fe8ff}html[data-adv-mood=warm]{--amood:#ffd38a}html[data-adv-mood=playful]{--amood:#ff9ae6}html[data-adv-mood=excited]{--amood:#9ffcff}html[data-adv-mood=urgent]{--amood:#ff6a5a}html[data-adv-mood=fierce]{--amood:#ffb04a}html[data-adv-mood=awe]{--amood:#c8a8ff}html[data-adv-mood=grave]{--amood:#6a8cff}html[data-adv-mood=tender]{--amood:#ffb8d0}
#advh .holo,#adv .holo{filter:drop-shadow(0 0 10px color-mix(in srgb,var(--amood) 70%,transparent));transition:filter .6s}
#advh .hsay b,#adv .who{color:var(--amood);transition:color .6s}
html[data-adv-mood=urgent] #advh.talk .advimg,html[data-adv-mood=excited] #advh.talk .advimg,html[data-adv-mood=fierce] #advh.talk .advimg{animation-duration:.8s,.26s}
html[data-adv-mood=tender] #advh.talk .advimg,html[data-adv-mood=grave] #advh.talk .advimg,html[data-adv-mood=awe] #advh.talk .advimg{animation-duration:.8s,.7s}
html[data-adv-mood=urgent] #advh .holo{animation:amUrg .5s steps(2) infinite}@keyframes amUrg{50%{filter:drop-shadow(0 0 16px var(--amood))}}
'''
rep('/* v563 the Fleet Registry and the Ages of the Deep */\n.arimg.ship', CSS + '/* v563 the Fleet Registry and the Ages of the Deep */\n.arimg.ship')
# the Titan viewer
rep('t3Open: d => { if (TITAN_INFO[d.k]) openSheet({ type: "titan3d", k: d.k }); },', 't3Open: d => { if (TITAN_INFO[d.k]) { openSheet({ type: "titan3d", k: d.k }); G.t3Said = G.t3Said || {}; if (!G.t3Said[d.k]) { G.t3Said[d.k] = 1; setTimeout(() => { try { advHolo(ADV_NEWS["x_t3_" + d.k]); } catch (e) {} }, 1600); } } },')
# the Titans' signature moves in battle: her voice only, once each per battle
rep('function titanFx(b, v) {', 'function titanFx(b, v) { try { const ab = v.ab === "wbcC" ? "x_bt_wbc" : v.ab === "wing" ? "x_bt_wing" : v.ab === "swarm" ? "x_bt_swarm" : null; if (ab && b.simT != null && !((b.tiSaid = b.tiSaid || {})[ab]) && Math.abs(b.simT - v.t) < 1.5) { b.tiSaid[ab] = 1; speak(ADV_NEWS[ab]); } } catch (e) {} /* v566 */')
# the Glyph Wheel
rep('toast(`${W.jack ? "JACKPOT! " : ""}Glyph Wheel: ${wheelName(W)}', 'try { if (W.jack) advHolo(ADV_NEWS[advPk("x_jack", 2)], true); else if (W.w <= 1.6) advHolo(ADV_NEWS[advPk("x_rare", 3)], true); } catch (e) {} /* v566 */ toast(`${W.jack ? "JACKPOT! " : ""}Glyph Wheel: ${wheelName(W)}')
# Void Pass Premium
rep('toast("Void Pass Premium unlocked! Claim the premium rewards for every tier you\'ve reached.", "win"); try { SFX.fanfare(true); } catch (e) {} }),', 'toast("Void Pass Premium unlocked! Claim the premium rewards for every tier you\'ve reached.", "win"); try { SFX.fanfare(true); } catch (e) {} setTimeout(() => { try { advHolo(ADV_NEWS.x_vp_prem, true); } catch (e) {} }, 900); }),')
# epic cache finds
rep('  if (!it.prev) try { SFX.click(); } catch (e) {} }', '  if (!it.prev) try { SFX.click(); } catch (e) {} if (!it.prev && (rar === "epic" || rar === "legendary") && !G.rvSaid) { G.rvSaid = 1; setTimeout(() => { try { if (document.getElementById("rvbox")) speak(ADV_NEWS[d && d.k !== "skinx" ? "x_rv_cos" : "x_rv_epic"]); } catch (e) {} }, 1300); } }')
# first visits
rep('function shVault() {', 'function shVault() { if (S && advOnce("vault")) setTimeout(() => { try { advHolo(ADV_NEWS.x_vault); } catch (e) {} }, 900); /* v566 */')
rep('function shWardrobe() {', 'function shWardrobe() { if (S && advOnce("ward")) setTimeout(() => { try { advHolo(ADV_NEWS.x_ward); } catch (e) {} }, 900); /* v566 */')
rep("  if (!quiet) archSeq(lv === 1 ? E.enc : E.def);", "  if (!quiet) archSeq(lv === 1 ? E.enc : E.def); if (/^s_/.test(k) && advOnce(\"registry\")) setTimeout(() => { try { advNews(\"x_registry\"); } catch (e) {} }, 2500); /* v566 */")
s2 = re.sub(r"GAME_V = 565\b", "GAME_V = 566", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok', len(NEWS), 'lines')
