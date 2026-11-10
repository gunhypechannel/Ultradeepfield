# v392 (owner): each boss event runs 48 hours: the Monday world bosses Mon 18:00 -> Wed 18:00 UTC, the Wednesday titans Wed 18:00 ->
# Fri 18:00 (then the Cube battle Fri -> Sun). Outside its window a boss is away: not on the map, not attackable, no wreckage trail.
# The Brood Matriarch's infection spreads every 12 hours until her event ends; the Tyrant's vault fills over the 48 hours.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("const wbHp = (k, T) => wbState(T).hp[k] | 0, wbAlive = (k, T) => wbHp(k, T) > 0;",
    "const wbHp = (k, T) => wbState(T).hp[k] | 0, wbAlive = (k, T) => wbHp(k, T) > 0;\nconst WB_LIVE = 48 * 3600e3, wbOn = (k, T = now()) => T - wbStartOf(k, T) < WB_LIVE, wbUp = (k, T = now()) => wbOn(k, T) && wbAlive(k, T), wbLiveEnd = (k, T = now()) => wbStartOf(k, T) + WB_LIVE, wbNext = (k, T = now()) => wbOn(k, T) ? wbLiveEnd(k, T) : wbEndOf(k, wbCycOf(k, T)); // v392: 48-hour events")
# the infection spreads every 12 hours
rep("""if (wbAlive("brd", T)) { const q = wbPos("brd", T, {}); v = { x: q.x, z: q.z, r2: 60 * 60 };""",
    """if (wbUp("brd", T)) { const q = wbPos("brd", T, {}), R = 45 + 20 * Math.min(3, Math.floor((T - wbStartOf("brd", T)) / (12 * 3600e3))); v = { x: q.x, z: q.z, r2: R * R, R };""")
rep("const wbVault = T => 1 + 1.5 * clamp((T - wbStartOf(\"tyr\", T)) / WEEK, 0, 1);", "const wbVault = T => 1 + 1.5 * clamp((T - wbStartOf(\"tyr\", T)) / (48 * 3600e3), 0, 1);")
rep("Its vault grows all week: the bounty per hit climbs from ×1 to ×2.5.", "Its vault fills the longer it sails: over its 48 hours the bounty per hit climbs from ×1 to ×2.5.")
rep("return `Vault ×${wbVault(T).toFixed(2)} bounty · grows all week`;", "return `Vault ×${wbVault(T).toFixed(2)} bounty · grows the longer it sails`;")
rep("if (key === \"brd\") return s > 1.02 ?", "if (key === \"brd\") { const I = wbInfect(T); return (s > 1.02 ? `Drone swarm ×${s.toFixed(1)} toughness · it thins when attacked` : \"Swarm thinned · full damage now\") + (I ? ` · infection ${I.R} wide, spreading every 12 h` : \"\"); }\n  if (key === \"brd\") return s > 1.02 ?")
rep("the worlds round her nest turn infected green.", "the worlds round her nest turn infected green, and the infection spreads every 12 hours until she leaves.")
# away: off the map, off the labels, no attack
rep("alive = st.hp[key] > 0, q = P3(WBO[key], T, WBQ),", "alive = st.hp[key] > 0 && wbOn(key, T), q = P3(WBO[key], T, WBQ),")
rep("{ const st = wbState(T); for (const key in WB) { if (!(st.hp[key] > 0)) continue;", "{ const st = wbState(T); for (const key in WB) { if (!(st.hp[key] > 0) || !wbOn(key, T)) continue;")
rep("""  if (!hp) body = `<p class="note">Defeated this week. It returns at full strength in <b data-end="${end}">${ftime(end - T)}</b>.</p>`;""",
    """  if (!wbOn(key, T)) body = `<p class="note">Away until the next hunt. It returns at full strength in <b data-end="${end}">${ftime(end - T)}</b>.</p>`;
  else if (!hp) body = `<p class="note">Defeated. It returns at full strength in <b data-end="${end}">${ftime(end - T)}</b>.</p>`;""")
rep("""<dt>Returns</dt><dd>${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC</dd></dl>""", """<dt>${wbOn(key, T) ? "Leaves in" : "Returns"}</dt><dd>${wbOn(key, T) ? ftime(wbLiveEnd(key, T) - T) : `${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC`} · hunts last 48 h</dd></dl>""")
rep("""It returns every ${wbG2(key) ? "Wednesday" : "Monday"} at full strength, in a new place.</p>""", """It returns every ${wbG2(key) ? "Wednesday" : "Monday"} at 18:00 UTC for 48 hours, at full strength, in a new place.</p>""")
rep("""${hp ? cineBtn(O.id) : ""}${body}`; }""", """${hp && wbOn(key, T) ? cineBtn(O.id) : ""}${body}`; }""")
rep("""if (!wbAlive(key)) return toast(`The ${D.n} has already fallen this week.`, "warn");""", """if (!wbOn(key)) return toast(`The ${D.n} is away until the next hunt.`, "warn"); if (!wbAlive(key)) return toast(`The ${D.n} has already fallen.`, "warn");""")
rep("""    if (!D) return home(); const at = f.arrive,""", """    if (!D) return home(); if (!wbOn(key, f.arrive)) { note(`The ${D.n} had left before our fleet arrived. Returning.`, "warn"); return home(); } const at = f.arrive,""")
# wreckage trail only while it's out
rep("""for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T; tk += step) { if (wbCycOf(key, tk) === stCyc(st, key) && st.dead[key] && st.dead[key] < tk) continue;""",
    """for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T; tk += step) { if (!wbOn(key, tk) || (wbCycOf(key, tk) === stCyc(st, key) && st.dead[key] && st.dead[key] < tk)) continue;""")
# event pages
rep("""function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), end = g === 2 ? wbEnd2(st.cyc2) : wbEnd(st.cyc), main = wbMain(g), up = main.filter(k => st.hp[k] > 0).length, art = BOSS_ART["g" + g];
  return `<div class="evban ev-sboss sbban art${g === 2 ? " sb2" : ""}"><img src="${art}" alt="${main.map(k => WB[k].n).join(", ")}"><div class="sbtop"><span class="vlive on">● LIVE</span><b>${E.n}</b><small>${up ? `${up} of ${main.length} ${g === 2 ? "titans" : "world bosses"} still standing` : `Every ${g === 2 ? "titan" : "world boss"} has fallen this week`}</small></div>
    <span class="evend">${g === 2 ? "Titans" : "Bosses"} return in: <b data-end="${end}">${ftime(end - T)}</b></span></div>`; }""",
"""function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), main = wbMain(g), live = wbOn(main[0], T), end = wbNext(main[0], T), up = main.filter(k => st.hp[k] > 0).length, art = BOSS_ART["g" + g];
  return `<div class="evban ev-sboss sbban art${g === 2 ? " sb2" : ""}${live ? "" : " off"}"><img src="${art}" alt="${main.map(k => WB[k].n).join(", ")}"><div class="sbtop"><span class="vlive${live ? " on" : ""}">${live ? "● LIVE" : "NEXT HUNT"}</span><b>${E.n}</b><small>${!live ? `Every ${E.day} 18:00 UTC, for 48 hours` : up ? `${up} of ${main.length} ${g === 2 ? "titans" : "world bosses"} still standing` : `Every ${g === 2 ? "titan" : "world boss"} has fallen`}</small></div>
    <span class="evend">${live ? "Event ends in" : "Starts in"}: <b data-end="${end}">${ftime(end - T)}</b></span></div>`; }""")
rep("""<span class="sbst">${hp ? (hot ? "⚔ UNDER ATTACK" : "ALIVE") : "DEFEATED"}</span>""", """<span class="sbst">${!wbOn(k, T) ? "AWAY" : hp ? (hot ? "⚔ UNDER ATTACK" : "ALIVE") : "DEFEATED"}</span>""")
rep("""${hp && wbG2(k) ? `<div class="sbtw">${wbTwist(k, T)}</div>` : ""}${hp ? `<div class="sbb">""", """${hp && wbOn(k, T) && wbG2(k) ? `<div class="sbtw">${wbTwist(k, T)}</div>` : ""}${hp && wbOn(k, T) ? `<div class="sbb">""")
rep("return every Wednesday at 18:00 UTC, each with a trick of its own: the Matriarch's swarm rebuilds while she's left alone, the Tyrant's bounty grows all week,", "return every Wednesday at 18:00 UTC for 48 hours, each with a trick of its own: the Matriarch's swarm rebuilds while she's left alone and her infection spreads every 12 hours, the Tyrant's bounty grows the longer it sails,")
rep("return every Monday at 18:00 UTC. Every attack, win or lose, pays a bounty for the hull it destroys and drops forge materials. Hunt points add up all week.", "return every Monday at 18:00 UTC for 48 hours. Every attack, win or lose, pays a bounty for the hull it destroys and drops forge materials. Hunt points add up over the hunt.")
# Finder rows
rep("""`Defeated · back in ${ftime(wbEndOf(k, stCyc(st, k)) - T)}`}</span>${hp && wbG2(k) ?""", """`Defeated · back in ${ftime(wbEndOf(k, stCyc(st, k)) - T)}`}</span>${hp && wbOn(k, T) && wbG2(k) ?""")
rep("""<span class="sub">${hp ? `${Math.round(hp / WB_SEG * 100)}% hull · ${D.where}""", """<span class="sub">${!wbOn(k, T) ? `Away · next hunt in ${ftime(wbNext(k, T) - T)}` : hp ? `${Math.round(hp / WB_SEG * 100)}% hull · ${D.where}""")
rep("""<span class="pill ${hp ? "bad" : "wait"}">${hp ? "Hunt" : "Down"}</span></button>`; }).join("")}</div>`).join("")}""", """<span class="pill ${hp && wbOn(k, T) ? "bad" : "wait"}">${!wbOn(k, T) ? "Away" : hp ? "Hunt" : "Down"}</span></button>`; }).join("")}</div>`).join("")}""")
# the Advisor's lines that said "all week"
rep("Its vault grows all week, so the later we hit it, the richer the bounty.", "Its vault fills the longer it sails, so the later we hit it, the richer the bounty.")
rep("""["What are world bosses?", "The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at eighteen hundred UTC.""", """["What are world bosses?", "The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at eighteen hundred UTC, for forty-eight hours.""")
rep("return every Wednesday at eighteen hundred UTC, each with its own trick. The Matriarch's swarm rebuilds if she's left alone, the Tyrant's bounty grows all week,", "return every Wednesday at eighteen hundred UTC, for forty-eight hours, each with its own trick. The Matriarch's swarm rebuilds if she's left alone and her infection spreads every twelve hours, the Tyrant's bounty keeps growing,")
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + "\n/* v392 a boss event between hunts */\n.sbban.off img{filter:saturate(.45) brightness(.7)}.sbban .vlive:not(.on){background:rgba(20,16,34,.8);color:#c9b8ff;border-color:rgba(201,184,255,.4)}\n" + t[i:]
t = t.replace("const GAME_V = 391;", "const GAME_V = 392;")
open(p, "w").write(t); print("ok")
