# v612: the story, expanded (owner's brief, 2026-11-17). Opening cinematic, a playable prologue (the Advisor wakes in a pyramid; you go
# back for the escape pods), four new Archive chapters plus the Matriarch's reason, her reactions in the pyramids, Chronicles Book Two
# (the first chapter written for your House) and the Houses' creeds on the faction picker. See p612_story.js / .css.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p612_story.js', encoding='utf-8').read()
css = open('tools/patches/p612_story.css', encoding='utf-8').read()
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:] # the main stylesheet (line 0 holds the page skeleton's reset style)
# the story block, after the Chronicles (it extends CHRON, ARCH and ARCH_CAT)
a = s.index('const chProg = (C, m) => ')
s = s[:a] + js + '\n' + s[a:]
rep('const chProg = (C, m) => m[0] === "worlds" ? Math.min(m[1], chStat("worlds")) : Math.min(m[1], Math.max(0, chStat(m[0]) - (C.base[m[0]] || 0)));',
    'const chProg = (C, m) => { if (m[0] !== "worlds" && C.base[m[0]] == null) C.base[m[0]] = chStat(m[0]); /* v612 a chapter added after you finished the book starts counting when you first see it */ return m[0] === "worlds" ? Math.min(m[1], chStat("worlds")) : Math.min(m[1], Math.max(0, chStat(m[0]) - (C.base[m[0]] || 0))); };')
rep('background-image:url(art/chron/c6.webp)', 'background-image:url(${chImg(CHRON.length - 1)})')
rep('background-image:url(art/chron/c${C.c + 1}.webp)', 'background-image:url(${chImg(C.c)})')
# moods and creeds once their tables exist
rep('const facOf = () => ', 'Object.assign(FACTIONS.terran, { creed: "The Ironborn creed: survive through strength. Heirs of the old empire\'s navy." }); Object.assign(FACTIONS.solar, { creed: "The Ascendant creed: master the Architects\' gifts and raise the empire again." });\n'
    'Object.assign(FACTIONS.nyx, { creed: "The Veil creed: knowledge is the one weapon the dark can\'t take. They listen to the Void." }); Object.assign(FACTIONS.verdant, { creed: "The Keepers\' creed: the galaxy is alive, the Wardens are its guardians, and the seals must hold." }); /* v612 */\n'
    'Object.assign(ADV_MOOD_L, CIN_MOOD);\nconst facOf = () => ')
rep('<span class="fctxt"><b>${F.n}</b><small>${F.d}</small></span>', '<span class="fctxt"><b>${F.n}</b><small>${F.d}</small>${F.creed ? `<em class="fccreed">${F.creed}</em>` : ""}</span>')
# Archives: names, pictures, hints, unlocks, the discovery reward
rep('const archName = k => /^o_/.test(k) ? "The Omens" :', 'const archName = k => /^a_/.test(k) ? "The Age of Ashes" : /^h_/.test(k) ? (FACTIONS[k.slice(2)] || {}).n || "A House" : /^d_/.test(k) ? "A discovery" : /^x_/.test(k) ? "The Architects" : k === "l_queen" ? "Queen Vael\'Khor" : /^o_/.test(k) ? "The Omens" :')
rep('function archImg(E, lv, k) { ', 'function archImg(E, lv, k) { if (/^[ahdx]_/.test(k) && E.img) return `<div class="arimg full lore"><img src="${E.img === "adv" ? advArt() : E.img}" alt="" loading="lazy"></div>`; /* v612 */ ')
rep('<p class="note">${/^s_/.test(id) ? `Open the', '<p class="note">${ARCH[id].hint ? esc(ARCH[id].hint) : /^s_/.test(id) ? `Open the')
rep('<small>${lv ? esc(archName(k)) : k === "testament"', '<small>${lv ? esc(archName(k)) : E.hint ? esc(E.hint) : k === "testament"')
rep('/^[bsleco]_/', '/^[bslecoahdx]_/', 3)
rep('for (const k of ARCH_ORD) if (/^e_/.test(k) && (S.bondDays || 0) >= ARCH[k].day) want.push([k, 1]); /* v567 her memories */',
    'for (const k of ARCH_ORD) if (/^e_/.test(k) && (S.bondDays || 0) >= ARCH[k].day) want.push([k, 1]); /* v567 her memories */ try { storyWant(want, lv); } catch (e) {} /* v612 */')
rep('S.arch[k] = lv; dirty();', 'S.arch[k] = lv; dirty(); if (lv === 2 && /^d_/.test(k)) { S.shards = (S.shards || 0) + 10; setTimeout(() => { try { toast(`◆10 for the discovery: ${ARCH[k].t}.`, "win"); } catch (e) {} }, 1600); } /* v612 */')
# her pauses in the pyramids (only when it happens live, not in the catch-up after time away)
rep('S.pyr[y.id] = f.arrive + PYR_CD; bump("pyramids");', 'S.pyr[y.id] = f.arrive + PYR_CD; bump("pyramids"); if (live) pyrSay(); /* v612 */')
# the cinematic before the first faction pick; the prologue for new commanders; replay from the Menu
rep('if (!S.faction) { S.facAsked = 1; dirty(); openSheet({ type: "faction" }); } else intro();',
    'if (!S.faction) { S.facAsked = 1; dirty(); if (!S.cinSeen && score() <= 200) cinWhenClear(() => cinOpen(() => openSheet({ type: "faction" }))); else openSheet({ type: "faction" }); } else intro(); /* v612 the opening cinematic first */')
rep('function intro() { if (!S.intro) { S.intro = true; dirty(); if (score() > 200) say(INTRO); else introPlay(); } }',
    'function intro() { if (!S.intro) { S.intro = true; dirty(); if (score() > 200) say(INTRO); else { try { proPlay(); } catch (e) { introPlay(); } } } } /* v612 the prologue */')
rep('  replayIntro: () => { closeSheet(); closeMenu(); introPlay(); },', '  replayIntro: () => { closeSheet(); closeMenu(); cinOpen(() => proPlay(true)); }, /* v612 the opening and the prologue */')
rep('<p>Relive the ambush on the way in and hear Admiral Kaskov\'s opening briefing again.</p><button class="mbtn" data-act="replayIntro">Replay briefing</button>',
    '<p>Watch the opening, Before the Darkness, and relive the night the Advisor chose you.</p><button class="mbtn" data-act="replayIntro">Watch the opening</button>')
rep('<button class="btn ghost wide" data-act="replayIntro">Replay the briefing</button>', '<button class="btn ghost wide" data-act="replayIntro">Watch the opening</button>')
rep('} ART_LIVE.clear(); battle = null;', '} ART_LIVE.clear(); battle = null; if (G.proAfter) { const pf = G.proAfter; G.proAfter = null; setTimeout(() => { try { pf(); } catch (e) {} }, 700); } /* v612 the prologue goes on after the ambush */')
# nothing else talks over the cinematic
rep('function say(lines) {\n', 'function say(lines) { if (G.cineOn && lines && lines.length) { S.say.push(...lines); dirty(); return; } /* v612 */\n')
rep('function advHolo(line, force) { if (!line) return;', 'function advHolo(line, force) { if (!line || G.cineOn) return;')
rep('function flushSay() { if (S.celeb && S.celeb.length && !battle', 'function flushSay() { if (G.cineOn) return; if (S.celeb && S.celeb.length && !battle')
# carrier wings launch from the hangar when the fight begins (owner: "right when the battle starts the carrier ships are already circling the
# enemy, no launch from ship"). Each pair used to start part-way through its sortie; now pair k leaves the hangar k steps after the start.
rep('for (let k = 0; k < nD; k++) { const wing = k & 1, u = ((b.wclk / P) + (k >> 1) / nP + (i * .137) - wing * .014 + 1) % 1, [x0, y0] = at(u, k),',
    'for (let k = 0; k < nD; k++) { const wing = k & 1, el = b.wclk - ((k >> 1) / nP * .6 + (i % 5) * .03 + wing * .014) * P; if (el < 0) continue; /* v612 still in the hangar */ const u = (el / P) % 1, [x0, y0] = at(u, k),')
s2 = re.sub(r"GAME_V = 611\b", "GAME_V = 612", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
