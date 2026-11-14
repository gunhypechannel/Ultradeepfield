# v567 the Advisor, deeper (owner: "Do what we can without eleven labs, review all lines for any improvements").
# The line review: the boss calendar lines told the old schedule (Monday world bosses, Wednesday titans, every-other-Wednesday
# Convergence, the Omega Cube "next month"): rewritten for the season calendar, and Saturday's hunt now announces the one boss that
# rose (wb_new_<boss>). "I've never seen..." was in 13 lines: 11 now say it their own way. The Bestiary field notes start with a capital.
# New: she remembers. Claim a world boss or super boss and the next greeting recalls that victory (greet_mem_<boss>).
# New: the bond. Every day you play counts (S.bondDays); her own story, "The Echo", opens in the Archives one memory at a time
# (days 2, 4, 7, 10, 14, 21), each told in her own voice when it unlocks.
# New: her hologram breathes with her voice: docs/voice/env.json holds each clip's loudness at 25 steps a second and the glow round her
# follows it while she talks (no audio routing, so iPhones are unaffected).
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
D = json.load(open('tools/patches/p567_lines.json'))
for old, new, mood in D['replace']: rep(old, new)
rep('["What are the Wednesday titans?",', '["What makes each world boss different?",')
rep('["What are world bosses?", "World bosses hunt', '["What are world bosses?", "World bosses hunt')
for m in re.finditer(r'b_\w+: \{ cat: "best"[^\n]*?interp: "([a-z])', s): pass
s = re.sub(r'(b_\w+: \{ cat: "best".*?interp: ")([a-z])', lambda m: m.group(1) + m.group(2).upper(), s)  # capitalised field notes
# Saturday's hunt: the boss that rose
rep('if (["ovl", "dev", "war"].includes(rs) && satNew) advNews("wb_new", "wb:" + c2, { act: "find", r: "ev" }, "Hunt the bosses");', 'if (rs && satNew) advNews(ADV_NEWS["wb_new_" + rs] ? "wb_new_" + rs : "wb_new", "wb:" + c2, { act: "find", r: "ev" }, "Hunt the boss"); /* v567 */')
rep('if (tit) advNews("wb2_new", "wb2:" + c2, { act: "events", ev: "tboss" }, "Titan Hunt");', '/* v567 the titans are Saturday bosses now: their arrival is the hunt news above */')
NEWS = {k: v[0] for k, v in D['news'].items()}
rep('const ADV_NEWS = {', 'const ADV_NEWS = {' + json.dumps(NEWS, ensure_ascii=False)[1:-1] + ', ')
MOOD = {v[0]: v[1] for v in D['news'].values()}; MOOD.update({new: mood for old, new, mood in D['replace']})
for e in D['echo']: MOOD[e[3]] = 'tender'; MOOD[e[4]] = 'grave'; MOOD[e[5]] = 'tender'; [MOOD.__setitem__(x, 'tender') for x in e[6]]
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + json.dumps(MOOD, ensure_ascii=False)[1:-1] + ', ')
# memory: the last great kill
rep('    S.shards = (S.shards || 0) + sh; giveItem(it); let extra = "";', '    S.shards = (S.shards || 0) + sh; giveItem(it); let extra = ""; if (ADV_NEWS["greet_mem_" + key]) S.advMem = { k: key, at: now() }; /* v567 */')
rep('S.sbGot = S.sbGot || {}; if (st.hp > 0 || !my || S.sbGot[k] === s0) continue; S.sbGot[k] = s0;', 'S.sbGot = S.sbGot || {}; if (st.hp > 0 || !my || S.sbGot[k] === s0) continue; S.sbGot[k] = s0; if (ADV_NEWS["greet_mem_" + k]) S.advMem = { k, at: now() }; /* v567 */')
rep('if (T - (S.greetAt || 0) > 6 * 3600e3) { S.greetAt = T; dirty(); const h = new Date().getHours(), away = (G.awayMs || 0) >= 3 * 864e5;\n      advNews(',
    'if (T - (S.greetAt || 0) > 6 * 3600e3) { S.greetAt = T; dirty(); const h = new Date().getHours(), away = (G.awayMs || 0) >= 3 * 864e5, mem = S.advMem && S.advMem.at > (S.memSaid || 0) && T - S.advMem.at < 7 * 864e5 && ADV_NEWS["greet_mem_" + S.advMem.k] ? S.advMem : null;\n      if (mem && !away) { S.memSaid = mem.at; advNews("greet_mem_" + mem.k); } else advNews(')
# the bond and her story
rep('function advLive() { if (!S || !G.ready) return; const T = now(); S.advOnce = S.advOnce || {};', 'function advLive() { if (!S || !G.ready) return; const T = now(); S.advOnce = S.advOnce || {}; if (S.bondDay !== utcDay()) { S.bondDay = utcDay(); S.bondDays = (S.bondDays || 0) + 1; dirty(); } /* v567 the bond: days played together */')
ECHO = {}
for k, day, t, frag, interp, adv, lines in D['echo']:
    ECHO[k] = {"cat": "echo", "t": t, "era": "Day %d together" % day, "civ": "Her own memory", "loc": "The Advisor's core", "img": None, "th": "Personal", "frag": frag, "interp": interp, "adv": adv, "enc": [], "def": lines, "day": day}
rep('const ARCH_ORD = [', 'Object.assign(ARCH, ' + json.dumps(ECHO, ensure_ascii=False) + '); /* v567 her story, The Echo */\nconst ARCH_ORD = [')
rep('"l_advisor", "s_fighter"', '"l_advisor", ' + ', '.join('"%s"' % e[0] for e in D['echo']) + ', "s_fighter"')
rep('["ages", "The Ages of the Deep",', '["echo", "The Echo: her story", "The Advisor\'s own memories. One more surfaces as your days together add up."], ["ages", "The Ages of the Deep",')
rep('archName = k => /^s_/.test(k)', 'archName = k => /^e_/.test(k) ? "The Advisor" : /^s_/.test(k)')
rep('if (/^l_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`;', 'if (/^l_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`; if (/^e_/.test(k)) return `<div class="arimg full lore echo"><img src="${advArt()}" alt="" loading="lazy"></div>`; /* v567 */')
rep("Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsl]_/.test(q)).length >= 10", "Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsle]_/.test(q)).length >= 10")
rep('if (k !== "testament" && !/^[bsl]_/.test(k) &&', 'if (k !== "testament" && !/^[bsle]_/.test(k) &&')
rep('const n2 = Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsl]_/.test(q)).length, lv = k => archLv(k);', 'const n2 = Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsle]_/.test(q)).length, lv = k => archLv(k);')
rep('for (const [k, ok] of want) if (ok && lv(k) < 2) { archUnlock(k, 2, !S.archLo); S.archLo = 1; return; } S.archLo = 1; }',
    'for (const k of ARCH_ORD) if (/^e_/.test(k) && (S.bondDays || 0) >= ARCH[k].day) want.push([k, 1]); /* v567 her memories */\n  for (const [k, ok] of want) if (ok && lv(k) < 2) { archUnlock(k, 2, !S.archLo); S.archLo = 1; return; } S.archLo = 1; }')
rep('/^l_/.test(id) ? "This part of the story opens as you uncover the Archives."', '/^e_/.test(id) ? `This memory surfaces on your day ${ARCH[id].day} together (you are on day ${S.bondDays || 1}).` : /^l_/.test(id) ? "This part of the story opens as you uncover the Archives."')
rep(': /^l_/.test(k) ? "Opens as the Archives fill"', ': /^e_/.test(k) ? `Surfaces on day ${ARCH[k].day} together` : /^l_/.test(k) ? "Opens as the Archives fill"')
rep('/^l_/.test(id) ? "What it means" : "Modern interpretation"', '/^e_/.test(id) ? "What we know" : /^l_/.test(id) ? "What it means" : "Modern interpretation"')
# her glow breathes with her voice
rep("function speak(line) {", '''/* v567 her hologram breathes with her voice: each clip's loudness envelope (docs/voice/env.json, 25 steps a second) */
let VENV = null; try { fetch("voice/env.json", { cache: "no-cache" }).then(r => r.ok ? r.json() : null).then(j => { if (j) VENV = j; }).catch(() => {}); } catch (e) {}
function lipRun(k) { const env = VENV && VENV[k]; if (!env) return; const R = document.documentElement, t0 = performance.now(); cancelAnimationFrame(G.lipRaf);
  const step = () => { const a = VOICE.au; if (!a || a.ended || (a.paused && performance.now() - t0 > 1500)) { R.style.setProperty("--lip", "0"); return; } const i = Math.floor((a.currentTime || 0) * 25), c = env.charCodeAt(Math.min(env.length - 1, i)) - 48; R.style.setProperty("--lip", (Math.max(0, c) / 42).toFixed(2)); G.lipRaf = requestAnimationFrame(step); };
  G.lipRaf = requestAnimationFrame(step); }
function speak(line) {''')
rep('a.src = "voice/" + k + ".mp3?v=" + VOICE.clips[k];', 'a.src = "voice/" + k + ".mp3?v=" + VOICE.clips[k]; try { lipRun(k); } catch (e) {}')
rep('#advh .holo,#adv .holo{filter:drop-shadow(0 0 10px color-mix(in srgb,var(--amood) 70%,transparent));transition:filter .6s}',
    '#advh .holo,#adv .holo{filter:drop-shadow(0 0 calc(8px + var(--lip,0) * 22px) color-mix(in srgb,var(--amood) calc(55% + var(--lip,0) * 45%),transparent))}\n#advh.talk .hbeam,#adv.talk .hbeam{opacity:calc(.55 + var(--lip,0) * .45)}\n.arimg.echo img{object-fit:cover;object-position:50% 12%}')
s2 = re.sub(r"GAME_V = 566\b", "GAME_V = 567", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
