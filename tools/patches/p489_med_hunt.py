# v489 Medusara, the Stone Gaze (owner: Medusa art 2026-11-12; named Medusara; the sixth Wednesday slot, so each great event comes back
# every 6 weeks: vae, dv, aex, conv, khz, med; her first hunt Wed 2026-12-23, Vaelthar's return moves to 12-30; signature mechanic the
# Petrifying Gaze). 100 sections, 36 hours, on the shared record event/sb_med.
#   The Stone Face (100-75): serpent lunges, gaze sweeps, storm lightning, ruin-tower volleys.
#   Serpent Crown (75-50) on: every 6 hours her eyes charge the Petrifying Gaze. Sever 5 of her 8 serpent heads in the cycle and she is
#     blinded (+50% sections for an hour); if not, the gaze fires and turns fleets to stone (x1.8 firepower for an hour, only for fleets
#     that attack then). The heads regrow each cycle.
#   Petrifying Gaze (50-25): +20% firepower.   Shattered Visage (below 25): her face cracks open (+30% firepower) and her third eye can
#     be struck (x2 sections, x1.5 firepower).
#   Her fall: she turns to grey stone and crumbles away; her glyph (red-gold) burns for 3 hours.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('ROT = ["vae", "dv", "aex", "conv", "khz"]', 'ROT = ["vae", "dv", "aex", "conv", "khz", "med"]')
rep('    mats: ["krelic", "karmor", "kcore", "krune"], rare: "kcore" } };', '''    mats: ["krelic", "karmor", "kcore", "krune"], rare: "kcore" },
  med: { n: "Medusara", t: "The Stone Gaze", ev: "Gaze of the Gorgon", day: 0, first: ROT0 + 5 * WEEK, m3: "medusara", u: "wbMed", HP: 1500000, ATK: 680000, col: "#ff5a4a", art: "art/boss/medusara.webp", ic: "◉",
    mv: ["gaze", "lunge", "storm", "ring"], diff: "Ultimate", ph: [[75, "The Stone Face"], [50, "Serpent Crown"], [25, "Petrifying Gaze"], [0, "Shattered Visage"]],
    abil: [["Gorgon's Glare", "Two red beams from her eyes sweep across the fleets."], ["Serpent Lunge", "Her crown of gold-armoured serpents strikes into the line."], ["Abyssal Storm", "Lightning breaks from the violet storm beneath her."], ["Ruin Volley", "The gothic towers on her gold ring fire on the fleets."],
      ["Petrifying Gaze", "From 75% her eyes charge every 6 hours. Sever 5 of her 8 serpent heads in the cycle to blind her (+50% for an hour); if not, the gaze turns fleets to stone (×1.8 firepower for an hour). The heads regrow each cycle."], ["Shattered Visage", "Below 25% her face cracks open: she hits 30% harder, and her third eye can be struck (×2 sections, ×1.5 firepower)."]],
    mats: ["mstone", "mscale", "mgaze", "mcrown"], rare: "mgaze" } };''')
rep('karmor: ["Khezaroth Armor Fragment", "#2a2238", "#e6b23c", "karmor"] };', 'karmor: ["Khezaroth Armor Fragment", "#2a2238", "#e6b23c", "karmor"],\n  mgaze: ["Gorgon Eye Core", "#ffd0c0", "#e0202a", "mgaze"], mscale: ["Gilded Serpent Scale", "#f4cf72", "#7a4a12", "mscale"], mstone: ["Petrified Heartstone", "#6a6478", "#e8b048", "mstone"], mcrown: ["Crown Shard of the Gorgon", "#f5c84a", "#c0202a", "mcrown"] };')
rep("""    gear: '<circle cx="12" cy="12" r="6.5" fill="url(#ID)"/>""", """    mgaze: '<ellipse cx="12" cy="12" rx="10.5" ry="6.4" fill="url(#ID)" stroke="#f5c84a" stroke-width="1.2"/><circle cx="12" cy="12" r="4.2" fill="#ff3a2a"/><ellipse cx="12" cy="12" rx="1.1" ry="3.6" fill="#1a0406"/><circle cx="10.2" cy="10.3" r="1" fill="#fff" opacity=".8"/>',
    mscale: '<path d="M12 2 Q21 7 19 15 Q16 21 12 22 Q8 21 5 15 Q3 7 12 2 Z" fill="url(#ID)" stroke="#7a4a12" stroke-width="1"/><path d="M6 10 Q12 13 18 10 M6.6 14.6 Q12 17.6 17.4 14.6" stroke="#7a4a12" stroke-width="1.3" fill="none"/>',
    mstone: '<path d="M5 6 L12 2.5 L19.5 6.5 L20.5 15 L13 21.5 L4.5 17.5 L3.5 10 Z" fill="url(#ID)" stroke="#2a2632" stroke-width="1"/><path d="M8 5 L11 11 L9 16 M11 11 L16 9 L18 14 M11 11 L13 18" stroke="#ffc850" stroke-width="1.4" fill="none"/>',
    mcrown: '<path d="M3 18 L4.5 8 L8.5 12 L12 4 L15.5 12 L19.5 8 L21 18 Z" fill="url(#ID)" stroke="#7a4a12" stroke-width="1"/><circle cx="12" cy="14" r="2.4" fill="#e0202a"/><path d="M3 18 H21 V20.5 H3 Z" fill="#c8901e"/>',
    gear: '<circle cx="12" cy="12" r="6.5" fill="url(#ID)"/>""")
rep("WPK = { stab: 4, eng: 3, emit: 3, an: 15, an0: 15, an1: 15, an2: 15 }", "WPK = { stab: 4, eng: 3, emit: 3, an: 15, an0: 15, an1: 15, an2: 15, snk: 4 }")
rep("/* Aexion's transformation: the first time its hull fell to 60% */", r"""/* v489 Medusara's Petrifying Gaze: 8 serpent heads a cycle; sever 5 to blind her */
function medResult(st, s0, c) { const ce = s0 + SB_ARR + (c + 1) * SB_VC; if (sbHpAt(st, ce) > 75) return "dormant"; return wpN(st, "snk" + c, "snk") >= 5 ? "interrupted" : "fired"; }
/* Aexion's transformation: the first time its hull fell to 60% */""")
rep('  else if (k === "khz") { const { c } = vaeCycle(s0, T);\n    if (ph === 1 || ph === 2)', r'''  else if (k === "med") { const { c } = vaeCycle(s0, T); if (c >= 1) { const prevEnd = s0 + SB_ARR + c * SB_VC; if (T < prevEnd + SB_H) { const r = medResult(st, s0, c - 1); if (r === "interrupted") { m *= 1.5; why.push("her gaze is blinded (+50%)"); } else if (r === "fired") { fp *= 1.8; why.push("the Petrifying Gaze is still turning fleets to stone (×1.8 firepower)"); } } }
    if (ph === 2) { fp *= 1.2; why.push("Petrifying Gaze (+20% firepower)"); } if (ph === 3) { fp *= 1.3; why.push("Shattered Visage (+30% firepower)"); if (tgt === "eye") { m *= 2; fp *= 1.5; why.push("striking her third eye (×2 sections, ×1.5 firepower)"); } } }
  else if (k === "khz") { const { c } = vaeCycle(s0, T);
    if (ph === 1 || ph === 2)''')
rep('  else if (k === "khz") { const ph = sbPhase(k, st.hp); if (ph === 1 || ph === 2) { const { c } = vaeCycle(s0, T); KHZ_AN', r'''  else if (k === "med") { const ph = sbPhase(k, st.hp); if (st.hp <= 75 && ph < 3) { const { c } = vaeCycle(s0, T), d = Math.min(8, wpN(st, "snk" + c, "snk")); L.push(["snk", "Serpent heads", 8 * WPK.snk - (st.wp["snk" + c] || 0), `${d} of 8 severed this cycle`]); } if (ph === 3) L.push(["eye", "Third eye", null, "double damage, deadlier"]); }
  else if (k === "khz") { const ph = sbPhase(k, st.hp); if (ph === 1 || ph === 2) { const { c } = vaeCycle(s0, T); KHZ_AN''')
rep('an0: "krune", an1: "krune", an2: "krune", heart: "kcore" }[tgt];', 'an0: "krune", an1: "krune", an2: "krune", heart: "kcore", snk: "mscale", eye: "mgaze" }[tgt];')
rep('cap = tgt === "core" || tgt === "reactor" || tgt === "heart" ? n0 : open[2];', 'cap = tgt === "core" || tgt === "reactor" || tgt === "heart" || tgt === "eye" ? n0 : open[2];')
rep('tgt === "core" || tgt === "reactor" || tgt === "heart" ? m : 1);', 'tgt === "core" || tgt === "reactor" || tgt === "heart" || tgt === "eye" ? m : 1);')
rep('if (tgt === "core" || tgt === "reactor" || tgt === "heart") { const take = Math.min(n0, tgt === "reactor" || tgt === "heart" ? seg * 2 : seg);', 'if (tgt === "core" || tgt === "reactor" || tgt === "heart" || tgt === "eye") { const take = Math.min(n0, tgt === "reactor" || tgt === "heart" || tgt === "eye" ? seg * 2 : seg);')
rep('const key = tgt === "stab" ? "stab" + vaeCycle(s0, at).c : /^an\\d$/.test(tgt)', 'const key = tgt === "stab" || tgt === "snk" ? tgt + vaeCycle(s0, at).c : /^an\\d$/.test(tgt)')
rep('`Our fleet ${tgt === "core" || tgt === "reactor" || tgt === "heart" ?', '`Our fleet ${tgt === "core" || tgt === "reactor" || tgt === "heart" || tgt === "eye" ?')
rep('  if (live && k === "khz") {', '''  if (live && k === "med") { const { c, ce } = vaeCycle(s0, T), d = Math.min(8, wpN(st, "snk" + c, "snk")); shield = `<dt>Serpent heads</dt><dd>${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<i class="sbpip ${i < d ? "off" : ""}"></i>`).join("")} ${hp > 75 ? "dormant" : sbPhase(k, hp) === 3 ? "shattered" : `${d}/8 severed (5 blinds her) · gaze in <b data-end="${ce}">${ftime(ce - T)}</b>`}</dd>`; }
  if (live && k === "khz") {''')
rep('k === "khz" ? "Its glyph burns where it fell, for a few hours."', 'k === "khz" ? "Its glyph burns where it fell, for a few hours." : k === "med" ? "Her glyph burns where she fell, for a few hours."')
rep('const set = { vae: "celes", aex: "sov", khz: "abyss" }[k],', 'const set = { vae: "celes", aex: "sov", khz: "abyss", med: "gorgon" }[k],')
rep('abyss: ["Abyssal", [[2, { shd: 3, hul: 2 }], [4, { shd: 4, hul: 3, boss: 4 }]]] };', 'abyss: ["Abyssal", [[2, { shd: 3, hul: 2 }], [4, { shd: 4, hul: 3, boss: 4 }]]], gorgon: ["Gorgon", [[2, { atk: 3, boss: 2 }], [4, { atk: 4, shd: 2, boss: 4 }]]] };')
rep('artifact: ["Eye of Khezaroth", { krune: 6, krelic: 4, kcore: 2 }] } } };', 'artifact: ["Eye of Khezaroth", { krune: 6, krelic: 4, kcore: 2 }] } },\n  gorgon: { k: "med", it: { armor: ["Petrified Aegis Plate", { mstone: 8, mscale: 6, mgaze: 2 }], bridge: ["Gorgon\'s Throne", { mcrown: 6, mstone: 4, mgaze: 2 }], engine: ["Serpent Coil Drive", { mscale: 8, mcrown: 4, mgaze: 2 }], computer: ["Gaze of Stone Targeting", { mcrown: 6, mscale: 4, mgaze: 3 }] } } };')
rep('''"Its chest armour is splitting open... that\'s its heart! Strike the dark-matter heart!"] };''', '''"Its chest armour is splitting open... that\'s its heart! Strike the dark-matter heart!"],
  med: [null, "Her serpents are rearing and her eyes are starting to burn. Sever five of her serpent heads before her gaze charges!", "The Petrifying Gaze is getting stronger. Keep cutting those serpents down!", "Her face is cracking apart... there\'s a third eye in her crown! Strike the third eye!"] };''')
rep('khz: "Something ancient is stirring in the dark between the stars. Khezaroth wakes within three days." };', 'khz: "Something ancient is stirring in the dark between the stars. Khezaroth wakes within three days.", med: "Long-range scopes picked up something like a face... carved from a moon. Medusara arrives within three days." };')
rep('khz: "The gravity readings are bending again. Khezaroth is waking, within three days." };', 'khz: "The gravity readings are bending again. Khezaroth is waking, within three days.", med: "Medusara is coming back. Keep your eyes off hers. She arrives within three days." };')
rep('''say(k + s0 + "a", k === "khz" ?''', '''say(k + s0 + "a", k === "med" ? (back ? "She's back. Medusara's gaze is on our galaxy again, and her serpents look hungrier." : "WARNING: a moon-sized stone face is rising out of a violet storm. Medusara has arrived!") : k === "khz" ?''')
rep('  else if (k === "khz") khzLive(W, X, b, T, t, e, st, s0, dead, df, scl, say);', '  else if (k === "khz") khzLive(W, X, b, T, t, e, st, s0, dead, df, scl, say);\n  else if (k === "med") medLive(W, X, b, T, t, e, st, s0, dead, df, scl, say);')
rep("/* v454 Aexion's death (owner:", r"""/* v489 Medusara live: her eyes open over 30 s, the Petrifying Gaze charging on the shared clock (and, if too few serpents are severed,
   firing), her serpents cut as the cycle's count rises, the Shattered Visage, and her fall into stone and her glyph */
function medLive(W, X, b, T, t, e, st, s0, dead, df, scl, say) { const k = "med"; b.grp.scale.setScalar(scl); const dt = Math.min(64, t - (X.lt || t)); X.lt = t;
  const aw = clamp(e / 30, 0, 1); b.drive("awake", aw < 1 ? aw : -1); if (aw > .5 && e < 300) say(k + s0 + "w1", "Her eyes are opening... don't look straight into them!");
  const hp = st.hp, ph = sbPhase(k, hp), { c, ce } = vaeCycle(s0, T), d = hp <= 75 && ph < 3 ? Math.min(8, wpN(st, "snk" + c, "snk")) : ph === 3 ? 5 : 0; b.snk = [0, 1, 2, 3, 4, 5, 6, 7].map(i => i < d ? 0 : 1);
  if (X.snP != null && X.snC === c && d > X.snP && d < 9) say(k + c + "s" + d, d >= 5 ? "Five serpents down! She can't hold her gaze now!" : "We severed a serpent head!"); X.snP = d; X.snC = c;
  const f = (T - (ce - 150e3)) / 180e3, res = medResult(st, s0, c); let fc = -1;
  if (!dead && hp && sbHpAt(st, ce) <= 75 && f >= 0 && f < 1) { fc = res === "interrupted" && f > .58 ? -1 : f; if (f < .06) say(k + ce + "w", "WARNING: PETRIFYING GAZE CHARGING. SEVER HER SERPENTS, AND DON'T LOOK INTO HER EYES."); if (res === "interrupted" && f > .58) say(k + ce + "i", "Her gaze broke! She's blinded. Hit her now!"); if (res !== "interrupted" && f > .76 && f < .9) say(k + ce + "f", "Her gaze is sweeping the field... our ships are turning to stone!"); }
  b.drive("charge", fc); X.sh = (X.sh || 0) + ((ph === 3 && hp && !dead ? 1 : 0) - (X.sh || 0)) * Math.min(1, dt * .0015); b.drive("shatter", X.sh > .002 ? X.sh : -1);
  if (!dead && hp && fc < 0 && aw >= 1) { const slot = Math.floor(T / 13000); if (slot !== X.slot) { X.slot = slot; b.act(b.moves[Math.abs(hash("m" + slot)) % b.moves.length]); } }
  if (dead) { const dd = df / 8; b.drive("die", dd < 1 ? dd : -1); X.glySeed = st.dead; sbGlyph(W, X, df - 7.5, t, clamp((st.dead + SB_GLY - T) / 600e3, 0, 1)); if (dd < 2) say(k + st.dead + "x", "She's turning to stone herself... Medusara is crumbling!"); if (dd > 1.2 && dd < 8) say(k + st.dead + "r", "She's gone. Only her glyph is left, burning where she fell."); } }
/* the owner preview, about 90 s */
function sbMed(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.med.sc; b.drive("awake", s < 12 ? Math.max(0, s / 12) : -1); if (s > 6) say("m0", "Her eyes are opening... don't look straight into them!");
  if (s > 13) say("m1", "Medusara, the Stone Gaze. Her serpents are her eyes' shield. All fleets, engage!");
  for (const [at, mv, kn, near] of [[14, "lunge", 3, 1], [18, "gaze", 4], [22.5, "storm", 3, 1], [26.5, "ring", 4], [64, "lunge", 4, 1], [68, "gaze", 5], [72, "storm", 4, 1]]) if (s > at && !X["m" + at]) { X["m" + at] = 1; b.act(mv); if (kn) setTimeout(() => { try { sbKillN(X, kn, performance.now(), near); } catch (e) {} }, 1300); }
  if (s > 30) say("m2", SBL.med[1]); const d = s < 32 ? 0 : Math.min(8, Math.floor((s - 32) / 2.2)); b.snk = [0, 1, 2, 3, 4, 5, 6, 7].map(i => i < Math.min(d, 4) ? 0 : 1); if (d >= 1) say("m3", "We severed a serpent head!");
  const C0 = 42, CL = 16, fc = (s - C0) / CL; b.drive("charge", fc >= 0 && fc < 1 ? fc : -1); X.quiet = fc > .2 && fc < .76;
  if (fc > 0) say("m4", "WARNING: PETRIFYING GAZE CHARGING. SEVER HER SERPENTS, AND DON'T LOOK INTO HER EYES."); if (fc > .77 && !X.gz) { X.gz = 1; sbKillN(X, 14, t); say("m5", "Her gaze is sweeping the field... our ships are turning to stone!"); }
  const shv = clamp((s - 60) / 4, 0, 1); b.drive("shatter", shv > 0 ? shv : -1); if (s > 60.5) say("m6", SBL.med[3]);
  if (s > 76 && !X.fall) { X.fall = s; say("m7", "She's turning to stone herself... Medusara is crumbling!"); }
  if (X.fall) { const dd = (s - X.fall) / 8; b.drive("die", dd < 1 ? dd : -1); b.drive("shatter", -1); sbGlyph(W, X, s - X.fall - 7.5, t); if (dd > 1.1) say("m8", "She's gone. Only her glyph is left, burning where she fell."); }
  const bp = b.grp.position, tb = { tx: bp.x, tz: bp.z };
  const K = s < 13 ? Object.assign(tb, { y: 15 * sc, d: 900 - s * 40, th: .15, ph: .2 }) : s < 30 ? Object.assign(tb, { y: 14 * sc, d: 520, th: .2, ph: .5 + (s - 13) * .03 }) : s < 42 ? Object.assign(tb, { y: 22 * sc, d: 560, th: .35, ph: 1.0 - (s - 30) * .04 })
    : s < 60 ? Object.assign(tb, { y: 15 * sc, d: 300 + fc * 160, th: .05, ph: .1 }) : s < 76 ? Object.assign(tb, { y: 15 * sc, d: 360, th: .12, ph: .3 + (s - 60) * .02 }) : Object.assign(tb, { y: 12 * sc, d: 560 + (s - 76) * 16, th: .25, ph: .5 });
  SBX_CAM(X, W, s, dt, K); }
/* v454 Aexion's death (owner:""")
rep('else if (P.key === "khz") sbKhz(X, W, b, s, t, dt, say, yaw, side);', 'else if (P.key === "khz") sbKhz(X, W, b, s, t, dt, say, yaw, side); else if (P.key === "med") sbMed(X, W, b, s, t, dt, say, yaw, side);')
rep('  khz: { n: "Khezaroth", t: "The Dark Matter Sphinx", m3: "khezaroth", p: [-330, 30, -310], sc: 4.2, dur: 100, col: "#a860ff", look: 6 } };', '  khz: { n: "Khezaroth", t: "The Dark Matter Sphinx", m3: "khezaroth", p: [-330, 30, -310], sc: 4.2, dur: 100, col: "#a860ff", look: 6 },\n  med: { n: "Medusara", t: "The Stone Gaze", m3: "medusara", p: [350, 50, 290], sc: 4.0, dur: 90, col: "#ff5a4a", look: 14 } };')
rep('for (const k of ["vae", "aex", "khz"]) db.doc("event/sb_" + k)', 'for (const k of ["vae", "aex", "khz", "med"]) db.doc("event/sb_" + k)')
rep('khz: ["▲", "Khezaroth, the Dark Matter Sphinx"],', 'khz: ["▲", "Khezaroth, the Dark Matter Sphinx"], med: ["◉", "Medusara, the Stone Gaze"],')
rep('sbKhz: () => sbSimStart("khz"),', 'sbKhz: () => sbSimStart("khz"), sbMed: () => sbSimStart("med"),')
rep('"▶ Watch Khezaroth, the Dark Matter Sphinx"}</button>', '"▶ Watch Khezaroth, the Dark Matter Sphinx"}</button><button class="btn ghost wide" data-act="${G.sbSim && G.sbSim.key === "med" ? "sbStop" : "sbMed"}">${G.sbSim && G.sbSim.key === "med" ? "■ Stop the Medusara preview" : "▶ Watch Medusara, the Stone Gaze"}</button>')
rep('wbk === "khz" ? 1.25 : 1', 'wbk === "khz" || wbk === "med" ? 1.25 : 1')
rep('khezaroth: [0, [-24, 20, 96], [0, 13, 4]],', 'khezaroth: [0, [-24, 20, 96], [0, 13, 4]], medusara: [0, [-20, 22, 104], [0, 16, 0]],')
rep('const WB_FRONT = { khezaroth: 0,', 'const WB_FRONT = { medusara: 0, khezaroth: 0,')
rep('if (h <= 25) WBR.b.drive("heart", 1); }', 'if (h <= 25) WBR.b.drive("heart", 1); } if (key === "med" && battle && battle.r) { const h = (battle.r.sbSeg || [100])[0]; if (h <= 25) WBR.b.drive("shatter", 1); if (battle.r.sbT === "snk") WBR.b.snk = [0, 0, 1, 1, 1, 1, 1, 1]; }')
rep('khz: [[.45, .16, .85], [.92, .78, 1]],', 'khz: [[.45, .16, .85], [.92, .78, 1]], med: [[.85, .18, .14], [1, .82, .55]],')
rep('{ key: "khz", t: "sb", form: "Unsealed Heart", sh: 1, n0: 20 },', '{ key: "khz", t: "sb", form: "Unsealed Heart", sh: 1, n0: 20 }, { key: "med", t: "sb", form: "The Stone Face", sh: 1, n0: 100 }, { key: "med", t: "sb", form: "Serpent Crown", sh: 1, n0: 65 }, { key: "med", t: "sb", form: "Shattered Visage", sh: 1, n0: 20 },')
rep('"khz": ["It\'s a sphinx', '"med": ["A face the size of a moon, and it\'s looking right at us. I don\'t like this, Commander.", "Her serpents are moving on their own. Every single one of them is hunting.", "I watched a whole squadron turn grey. Just... stone. I\'ve never seen anything like it."], "khz": ["It\'s a sphinx')
s = re.sub(r"GAME_V = 489\b", "GAME_V = 489", s)
open(P, 'w').write(s)
