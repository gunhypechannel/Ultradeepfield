# v571 The Ten Seals, Chapter 1: The Leviathan Rises (owner: "make some kind of live event equal to the omega cube event for each of
# these seasons to end with, each unique and matching the super boss"; "for the story to be connected"; "Do it all").
# The engine: FIN_EV holds each season finale's great event; the finale's Saturday world boss is its climax. finNow/finStage/finSay
# (the Advisor's stage calls), the set piece on the galaxy map (finTick -> levSet), the event panel (sheet "finale", shFinale), the band
# over the map (finBand), the owner's preview (Boss Lab ▶ / finSim: two minutes, then the boss on the map), and the Seal Ledger: the
# boss's kill writes event/wboss .ledger[s0] = "held" (wbNorm keeps it); if it survives the hunt the seal cracks, she says so, and a
# cracked Leviathan seal leaves a burning rift in the Rim (finScar) until the chapter returns. Each chapter is an Archives record in the
# new category "The Ten Seals" (c_<n>), opened when the event starts and interpreted when it ends.
# Chapter 1: the Rim burns (0-30 min); the Leviathan circles the galaxy along the Architects' wall, setting the Rim alight (30-90);
# it turns inward and the wall shatters at the breach (90-120); its fire tide sweeps the outer layer (120-150); the fight (150 min
# to the end of the 48-hour hunt), with the Leviathan at the breach.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = open('tools/patches/p571_finale.js', encoding='utf-8').read()
M = 60e3
FIN = {"lev": {"ch": 1, "n": "The Leviathan Rises", "chap": "The Wall Breaks", "ic": "≋", "col": "#ff7a2a", "set": 150 * M,
  "d": "The Warden of the Architects' outer wall has turned inward. Watch it circle the galaxy and break through the wall, then bring it down before the hunt ends, or the first seal cracks.",
  "st": [[0, "burn", "The Rim Burns", "Fire runs along the Rim as the Architects' outer wall begins to fail."],
         [30 * M, "hunt", "The Hunt", "The Leviathan circles the whole galaxy along the wall, setting the Rim alight behind it."],
         [90 * M, "breach", "The Breach", "It turns inward and smashes through the Architects' wall."],
         [120 * M, "tide", "The Fire Tide", "Its breath sweeps across the outer layer in a ring of fire."],
         [150 * M, "fight", "The Fight", "It holds at the breach. Every fleet can strike it until the hunt ends."]]}}
CH = {"c_1": {"cat": "saga", "t": "Chapter 1: The Wall Breaks", "era": "Season 1 finale", "civ": "The Seal Ledger", "loc": "The Architects' outer wall", "img": "art/arch/lev.webp", "th": "The Ten Seals",
  "frag": "The wall at the edge of everything has a keeper. When the keeper turns inward, the wall has already begun to fail.",
  "interp": "The Leviathan is the Warden of the Architects' outer wall. Their wardens believed the wall kept it out. In truth it patrolled the wall, and when it felt the Unmade stir beyond the black hole, it turned inward to reach the door.",
  "adv": "The Architects thought their wall kept the Leviathan out. I think the Leviathan was keeping something in.",
  "enc": ["Commander, a new chapter just opened in the Archives. It's happening right now.", "The Architects' wall at the Rim is failing, and its Warden is awake."],
  "def": ["The first chapter is closed, Commander.", "Whatever woke the Leviathan is still waiting beyond the black hole. And the next seal is already shaking."]}}
J = lambda o: json.dumps(o, ensure_ascii=False)
# the events and the calendar: the finale boss can be fought once its set piece is over
rep('ROTS_X = ["lev", "krk"]; /* v569 the finale-only Saturday bosses */', 'ROTS_X = ["lev", "krk"]; /* v569 the finale-only Saturday bosses */\nconst FIN_EV = ' + J(FIN) + '; /* v571 The Ten Seals: the season finales\' great events */')
rep('if (rotKeyS(rotWs(sat)) !== (D.con != null ? "ovl" : k)) return null; return [sat, sat + WB_LIVE]; }', 'if (rotKeyS(rotWs(sat)) !== (D.con != null ? "ovl" : k)) return null; return [sat + (FIN_EV[k] ? FIN_EV[k].set : 0), sat + WB_LIVE]; }')
# the Seal Ledger lives in the world boss document
rep('o.cyc = c; o.cyc2 = c2; o.scar =', 'o.cyc = c; o.cyc2 = c2; o.ledger = o.ledger && typeof o.ledger === "object" ? o.ledger : {}; o.scar =')
rep('if (!left) { cur.dead[key] = at; cur.last[key] = G.me; }', 'if (!left) { cur.dead[key] = at; cur.last[key] = G.me; if (FIN_EV[key]) { const fs = rotStartOf(key, at); if (fs != null) cur.ledger[fs] = "held"; } } /* v571 the seal holds */')
# the map, the band, the panel, the actions
rep('/* the band over the map: three days out, every stage, the fight */', JS + '\n/* the band over the map: three days out, every stage, the fight */')
rep('  try { dvTick(W, t, T); } catch (e) { mapErr(e); } // v430 Cube Devastation', '  try { dvTick(W, t, T); } catch (e) { mapErr(e); } // v430 Cube Devastation\n  try { finTick(W, t, T); } catch (e) { mapErr(e); } // v571 The Ten Seals')
rep('if (!live && nx - T < 72 * 3600e3) html = `<button class="omb soon" data-act="omOpen"><b>Ω CUBE DEVASTATION</b><span>in ${ftime(nx - T)}</span></button>`; }\n  if (!html) { if (b) b.remove(); return; } if (!b) { const A = $("#app");', 'if (!live && nx - T < 72 * 3600e3) html = `<button class="omb soon" data-act="omOpen"><b>Ω CUBE DEVASTATION</b><span>in ${ftime(nx - T)}</span></button>`; }\n  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim) html = finBand(T); /* v571 */\n  if (!html) { if (b) b.remove(); return; } if (!b) { const A = $("#app");')
rep('omega: shOmega, sboss: shSboss,', 'omega: shOmega, finale: shFinale, sboss: shSboss,')
rep('dvSim: () => dvSimStart(),', '''finOpen: d => openSheet({ type: "finale", k: d.k }), finSim: d => finSimStart(d.k), /* v571 */
  finWatch: d => { closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } setTimeout(() => { try { const F = finNow(now()), X = G3 && G3.fin, c = G3.cam; c.follow = null; c.followFleet = null; c.cineObj = null; c.cine = null;
      const hunt = F && F.e >= FIN_EV[F.k].st[1][0] && F.e < FIN_EV[F.k].st[2][0], q = X && X.b && X.b.grp.visible ? X.pos : F ? wbPosRaw(F.k, F.s0 + FIN_EV[F.k].set, {}) : wbPos(d.k, now(), {}); G.finFollow = performance.now() + 60000; c.goal = { tx: q.x, ty: q.y, tz: q.z, dist: hunt ? 1000 : 820, th: .7 }; } catch (e) {} }, 300); },
  dvSim: () => dvSimStart(),''')
rep('if (k === "conv") return convSimStart();', 'if (k === "conv") return convSimStart(); if (FIN_EV[k]) return finSimStart(k); /* v571 */')
rep('<div><span>${esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div>', '<div${FIN_EV[b] ? ` class="finrow" data-act="finOpen" data-k="${b}"` : ""}><span>${FIN_EV[b] ? `Chapter ${FIN_EV[b].ch} · ${esc(FIN_EV[b].n)}` : esc(WB[b] ? WB[b].n : b)}</span><em>${when(sat)}</em></div>')
# the Archives: The Ten Seals
rep('/* v567 her story, The Echo */\nconst ARCH_ORD = [', '/* v567 her story, The Echo */\nObject.assign(ARCH, ' + J(CH) + '); /* v571 The Ten Seals */\nconst ARCH_ORD = [')
rep('"l_advisor", "e_1"', '"l_advisor", "c_1", "e_1"')
rep('["echo", "The Echo: her story",', '["saga", "The Ten Seals", "The year\'s story. One chapter opens at every season finale, and the Seal Ledger remembers how each one ended."], ["echo", "The Echo: her story",')
rep('const archName = k => /^e_/.test(k) ? "The Advisor"', 'const archName = k => /^c_/.test(k) ? "The Ten Seals" : /^e_/.test(k) ? "The Advisor"')
rep('if (/^e_/.test(k)) return `<div class="arimg full lore echo">', 'if (/^c_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`; if (/^e_/.test(k)) return `<div class="arimg full lore echo">')
rep('/^e_/.test(id) ? `This memory surfaces', '/^c_/.test(id) ? "This chapter opens when its season finale begins." : /^e_/.test(id) ? `This memory surfaces')
rep(': /^e_/.test(k) ? `Surfaces on day', ': /^c_/.test(k) ? "Opens at its season finale" : /^e_/.test(k) ? `Surfaces on day')
rep('/^e_/.test(id) ? "What we know"', '/^c_/.test(id) ? "The chapter" : /^e_/.test(id) ? "What we know"')
s = s.replace('/^[bsle]_/', '/^[bslec]_/')
rep('if (!S || !G.ready || battle || G.sbSim || G.dvSim || G.convSim || G.wbShow) return; const T = now(), onMap = view === "galaxy";',
    'if (!S || !G.ready || battle || G.sbSim || G.dvSim || G.convSim || G.wbShow || G.finSim) return; const T = now(), onMap = view === "galaxy";\n    for (const fk in FIN_EV) { const ck = "c_" + FIN_EV[fk].ch, F = finNow(T), on = F && F.k === fk; if (on && !archLv(ck)) { archUnlock(ck, 1); return; } const ls = on ? F.s0 : finLast(fk, T); if (archLv(ck) === 1 && ls != null && finOutcome(fk, ls, T)) { archUnlock(ck, 2); return; } } /* v571 */')
# her moods for the new lines
MOOD = {}
for k, m in {"burn": "urgent", "hunt": "awe", "breach": "urgent", "tide": "urgent", "fight": "fierce", "held": "excited", "cracked": "grave", "sting": "grave"}.items():
    MOOD[re.search(r'\b' + k + r': "((?:[^"\\]|\\.)*)"', JS).group(1)] = m
for E in CH.values():
    for x in E['enc']: MOOD[x] = 'awe'
    for x in E['def']: MOOD[x] = 'grave'
    MOOD[E['adv']] = 'tender'
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
CSS = '''/* v571 The Ten Seals */
.omb.fin{border-color:var(--fc);background:rgba(26,10,4,.92);color:#ffe8d6;box-shadow:0 0 18px color-mix(in srgb,var(--fc) 45%,transparent)}.omb.fin b{color:var(--fc)}
.dvtl.fin li{border-left-color:color-mix(in srgb,var(--fc) 30%,transparent)}.dvtl.fin li.done{border-left-color:color-mix(in srgb,var(--fc) 55%,transparent)}.dvtl.fin li.now{background:color-mix(in srgb,var(--fc) 14%,transparent);border-left-color:var(--fc)}.dvtl.fin li.now small{color:var(--fc)}
.finled{list-style:none;padding:0;margin:6px 0 12px;display:grid;gap:3px}.finled li{display:flex;justify-content:space-between;gap:8px;padding:6px 10px;border-radius:9px;background:rgba(255,255,255,.03);font-size:13px}.finled li b{white-space:nowrap}.finled li.held b{color:#7dff9a}.finled li.cracked b{color:#ff6a5a}.finled li.live b{color:#ffd36b}.finled li.soon{opacity:.6}
.seafin .finrow{cursor:pointer}.seafin .finrow span{text-decoration:underline dotted}
'''
rep('.omb.soon{opacity:.92}', '.omb.soon{opacity:.92}\n' + CSS)
s2 = re.sub(r"GAME_V = 570\b", "GAME_V = 571", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
