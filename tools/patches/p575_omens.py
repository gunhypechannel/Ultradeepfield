# v575 The Omens (owner: "Is there a way each server plays from the beginning season 1 ... the first two seasons without any live
# event super bosses ... just have things show up around the map as a way to soft launch their arrival and then season 3 can start
# the live events"; "Do it all"; "I like the idea of Omen symbols, is there a way to also tie in the celestial in the back of the
# map? Named ... the judge?").
# 1) Every server's calendar starts at its own launch: window.UDF_SUPABASE.launch (or window.UDF_LAUNCH), "YYYY-MM-DD", taken back to
#    its Monday 00:00 UTC (default Monday Nov 9 2026). The season calendar, the boss rotation and the Void Pass all count from it.
# 2) Seasons 1 and 2 are a prologue (PRO = 2): the Season of Omens and the Season of the Countdown, with their own Void Pass (art
#    composited from the owner's paintings, two new planet skins). No Wednesday super bosses, the usual Saturday bosses. Each week one
#    Warden's omen shows on the map; the two prologue finales are short teasers (om1 The Shadow at the Wall, om2 The Count Breaks).
#    The Ten Seals start at Season 3 (chapter n is season n + 2's finale), then the ten-season year repeats.
# 3) The Archives gain The Omens (o_1..o_8) and The Judge (l_judge). The Judge behind the galaxy opens one eye per omen; once the
#    Ten Seals begin, his hands carry the Seal Ledger (gold held, red cracked).
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
J = lambda o: json.dumps(o, ensure_ascii=False)
M = 60e3
# ---- the calendar
rep('const EV_BASE = Date.UTC(2026, 0, 2, 18), WEEK = 7 * 864e5, EV_DUR = 48 * 3600e3;\nconst ROT0 = Date.UTC(2026, 10, 18, 18),',
    'const EV_BASE = Date.UTC(2026, 0, 2, 18), WEEK = 7 * 864e5, EV_DUR = 48 * 3600e3;\n'
    '/* v575 every server counts its seasons from its own launch (supabase-config.js: launch: "YYYY-MM-DD"), taken back to that Monday 00:00 UTC */\n'
    'const SRV0 = (() => { try { const v = (window.UDF_SUPABASE || {}).launch || window.UDF_LAUNCH, m = /^(\\d{4})-(\\d{2})-(\\d{2})/.exec(v || ""); if (m) { const t = Date.UTC(+m[1], +m[2] - 1, +m[3]); return t - ((new Date(t).getUTCDay() + 6) % 7) * 864e5; } } catch (e) {} return Date.UTC(2026, 10, 9); })(), PRO = 2; /* v575 seasons 1 and 2 are the prologue */\n'
    'const seaCyc = si => si < PRO ? -1 : (si - PRO) % 10, seaCos = si => si < PRO ? 10 + Math.max(0, si) : seaCyc(si); /* the ten-season year; the cosmetics set of a season (10, 11: the prologue) */\n'
    'const ROT0 = SRV0 + 9 * 864e5 + 18 * 3600e3,')
rep('["khz", "war"], ["med", "dev"]], ROT_SEA0 = Date.UTC(2026, 10, 9);', '["khz", "war"], ["med", "dev"]], ROT_SEA0 = SRV0;')
rep('  if (si === 0) return (SEA_PLAN[key] = sat ? ["ovl", "ovl", "dev", "lev"] : ["vae", "vae", "aex", "khz"]); /* season 1 keeps the first dates already announced (Vaelthar Nov 18, the Overlord Nov 21) */',
    '  if (si < PRO) return (SEA_PLAN[key] = sat ? (si > 0 ? ["dev", "ovl", "war", "ovl"] : ["ovl", "ovl", "dev", "war"]) : [null, null, null, null]); /* v575 the prologue: no super bosses yet, the usual Saturday bosses */')
rep('const NF = SEA_FIN.length, x = ((si % NF) + NF) % NF,', 'const NF = SEA_FIN.length, x = seaCyc(si),')
rep('const rotFinale = s0 => Math.floor((s0 - ROT_SEA0) / WEEK) % 4 === 3;', 'const rotFinale = s0 => { const w = Math.floor((s0 - ROT_SEA0) / WEEK); return w >= 4 * PRO && w % 4 === 3; }; /* v575 the prologue finales are omens */')
rep('odd = rk ? rk === "conv" : ((c2 % 2) + 2) % 2 === 1,', 'odd = s2 >= ROT0 ? rk === "conv" : ((c2 % 2) + 2) % 2 === 1,')
rep('tit = rk ? ["brd", "tyr", "wym", "col", "lev", "krk"].includes(rs) && satNew :', 'tit = s2 >= ROT0 ? ["brd", "tyr", "wym", "col", "lev", "krk"].includes(rs) && satNew :')
rep('const VP_BASE = Date.UTC(2026, 10, 9),', 'const VP_BASE = SRV0,')
# ---- the Ten Seals move two seasons on; the omens are not chapters
rep('function finWinOf(k, n) { const D = FIN_EV[k], w = 4 * (D.ch - 1 + 10 * n) + 2;',
    'function finWinOf(k, n) { const D = FIN_EV[k]; if (D.typ === "omen") { const wed = ROT0 + (4 * D.si + 2) * WEEK; return [wed, wed + D.set, wed + D.set + 60e3]; } /* v575 once, in the prologue */ const w = 4 * (PRO + D.ch - 1 + 10 * n) + 2;')
rep('const finKeys = () => Object.keys(FIN_EV).sort(', 'const finKeys = () => Object.keys(FIN_EV).filter(k => FIN_EV[k].typ !== "omen").sort(')
rep('  for (const k in FIN_EV) { const cur = finCur(k, T), D = FIN_EV[k];\n', '  for (const k in FIN_EV) { const cur = finCur(k, T), D = FIN_EV[k]; if (D.typ === "omen") continue;\n')
rep('const finP1 = (k, s0) => { const D = FIN_EV[k]; if (D.typ === "sb")',
    'const finP1 = (k, s0) => { const D = FIN_EV[k]; if (D.typ === "omen") { const a = 2.2, R = k === "om1" ? LAYERS[0].r1 + 12 : 0; return { x: Math.cos(a) * R, y: 0, z: Math.sin(a) * R }; } if (D.typ === "sb")')
rep('function finArchTick(T) { for (const k in FIN_EV) {', 'function finArchTick(T) { if (omArchTick(T)) return true; for (const k in FIN_EV) {')
rep('function finBand(T) { const F = finNow(T); if (F) { const D = FIN_EV[F.k], fight = F.e >= D.set, up = fight && (D.typ === "wb" ? wbUp(F.k, T) : sbOn(F.k, T)); return `<button class="omb fin" style="--fc:${D.col}" data-act="finOpen"',
    'function finBand(T) { const F = finNow(T); if (F) { const D = FIN_EV[F.k], fight = F.e >= D.set && D.typ !== "omen", up = fight && (D.typ === "wb" ? wbUp(F.k, T) : sbOn(F.k, T)); return `<button class="omb fin" style="--fc:${D.col}" data-act="${D.typ === "omen" ? "finWatch" : "finOpen"}"')
rep('if (!FIN_EV[k].st || FIN_EV[k].typ === "sb") continue;', 'if (!FIN_EV[k].st || FIN_EV[k].typ === "sb" || FIN_EV[k].typ === "omen") continue;')
rep('  for (const k in FIN_SCAR) { const s0 = finLast(k, T), on = s0 != null && T - s0 < FIN_YEAR && !(F && F.k === k) && finOutcome(k, s0, T) === "cracked", Y = W.finScars[k];',
    '  const ok = omenKey(T), o2 = F && F.k === "om2"; /* v575 the prologue: this week\'s omen; the count-break shows them all itself */\n'
    '  for (const k in FIN_SCAR) { const om = ok === k, s0 = om ? omenWk0(T) : finLast(k, T), on = s0 != null && !o2 && !(F && F.k === k) && (om || (T - s0 < FIN_YEAR && finOutcome(k, s0, T) === "cracked")), Y = W.finScars[k];')
# the omen events, their lines, the set pieces and the Judge
OM = {
 "om1": {"ch": 0, "typ": "omen", "si": 0, "n": "The Shadow at the Wall", "chap": "Omen", "ic": "☾", "col": "#ff8a4a", "set": 30 * M,
   "d": "The prologue's first finale. Fire wakes along the Rim, and something vast passes outside the Architects' wall.",
   "st": [[0, "embers", "Embers at the Rim", "Fire runs along the Rim again, brighter than before."], [8 * M, "shadow", "The Shadow", "Something enormous passes outside the wall, lit only by its own fire."], [24 * M, "gone", "Into the Dark", "It sinks back into the dark beyond the Rim."]]},
 "om2": {"ch": 0, "typ": "omen", "si": 1, "n": "The Count Breaks", "chap": "Omen", "ic": "⧗", "col": "#5dff6a", "set": 30 * M,
   "d": "The prologue's last finale. Every omen lights up at once, the Cube's countdown races, and then everything stops.",
   "st": [[0, "stir", "Every Omen Wakes", "All eight omens light up again, one after another."], [12 * M, "count", "The Count Races", "Sixty marks ring the Cube, and its countdown runs faster and faster."], [24 * M, "silence", "Silence", "Every signal stops at once."], [27 * M, "judge", "The Judge Opens His Eyes", "Behind the galaxy, all six of the giant's eyes blaze."]]},
}
SAY = {
 "om1": {"embers": ["Commander, the Rim is glowing again. Brighter this time.", "grave"],
         "shadow": ["Something enormous just passed the wall. I only saw its shadow... and fire.", "awe"],
         "gone": ["It's gone back into the dark. Commander, I think it was looking for a way in.", "grave"]},
 "om2": {"stir": ["Every omen we've seen is lighting up at once, Commander. All of them.", "urgent"],
         "count": ["The Cube's countdown just jumped. It's racing. Whatever was sleeping, it's waking up.", "urgent"],
         "silence": ["Silence. Every signal stopped at once. Season three, Commander. The Ten Seals begin.", "awe"],
         "judge": ["Commander... the giant at the edge of the galaxy. All six of its eyes are open. It's watching us.", "grave"]},
}
OMA = [
 ("lev", "Embers at the Rim", "The Rim", "Before the wall breaks, it burns. A spark, then a line of fire, then a shadow behind it.",
  "The Architects' outer wall has started to warm. Their records call it the first sign: the Warden at the wall stirring in its sleep. It isn't here yet, but it's close enough to light the Rim.",
  "I keep watching that fire. It's patient, Commander. Like it already knows the way in.",
  "Commander, there's fire along the Rim. No ships, no stars. Just fire.", "The embers at the Rim are fading. But they came back brighter every night this week."),
 ("brd", "Nests in the Dark", "Hive space", "The nests woke before the Hive did. The swarms learned to wait.",
  "Hive nests across the galaxy are glowing, and none of them have launched a swarm. The old seal-records describe this: the Hive gathering its strength around something it means to become.",
  "A Hive that doesn't attack frightens me more than one that does.",
  "Commander, every Hive nest on the scanners is glowing green, and none of them are moving.", "The nests went dark again. Whatever they were growing, it isn't finished yet."),
 ("krk", "The Deep Stirs", "The Middle Reach", "The Middle Reach went dark from below, as if something had opened beneath it.",
  "A ring of the Middle Reach has dimmed, and pillars of violet light rise from the dark at its edge. The Archives name only one thing that lives in the deep between the stars.",
  "Pillars of light, in a perfect ring. Commander, those aren't pillars. Those are arms.",
  "Commander, part of the Middle Reach just went dark, and there's light rising out of it. Like something is reaching up.", "The deep has gone quiet again. Too quiet."),
 ("wym", "A Light Gutters", "Beyond the Rim", "A ring of fire hung in the dark and flickered, as if something inside it was breathing.",
  "A halo of fire has appeared where no star burns. The Wyrm's records say it sleeps coiled around a dying sun. If that sun is flickering, the Wyrm is waking.",
  "Every time it flickers, I find myself holding my breath.",
  "Commander, a ring of fire just appeared out in the dark. No star inside it. It's flickering.", "The fire ring is gone. I counted the flickers. They were getting faster."),
 ("aex", "Frozen Shards", "The Aeon's resting place", "Shards of ice drifted in from nowhere, every one shaped like a blade.",
  "Crystal shards hang in space near the Aeon's old resting place, turning slowly like the pieces of something broken. The Warform Sovereign left nothing behind when it last fell. These shards say it's being rebuilt.",
  "They're all pointing the same way, Commander. Toward us.",
  "Commander, ice shards are drifting near the old Aeon site. Thousands of them. They're all turning the same way.", "The shards have melted back into the dark. Someone was counting them. I think it was the Aeon."),
 ("vae", "The Drifting Ruins", "Vaelthar's domain", "Temples drifted out of the nebula, older than any empire in our records, and still lit.",
  "Golden ruins are adrift near Vaelthar's domain: stones from the Celestial Wheel. The Ruin is gathering itself back together, one temple at a time.",
  "Whoever built those temples prayed to something. I don't want to meet it.",
  "Commander, there are ruins drifting near Vaelthar's domain. Golden ruins. They're still lit.", "The ruins have sunk back into the nebula. All but one. It's still out there, glowing."),
 ("khz", "The Broken Glyphs", "The inner galaxy", "Half a ring of glyphs, burning gold, and the other half missing.",
  "A broken ring of glowing glyphs has risen around the inner galaxy: the Sphinx's writing, the same marks as the last gate. Khezaroth guards the final door. Someone is writing the door back into being.",
  "I tried to read the glyphs. They were a countdown, Commander. The same one the Cube is keeping.",
  "Commander, golden glyphs just lit up around the inner galaxy. Half a ring. It's the Sphinx's writing.", "The glyphs went out. But I copied what they said. It's a number. And it's getting smaller."),
 ("med", "The Stone Worlds", "Pirate space", "Worlds turned grey overnight, and every one had a crack of red light.",
  "Pirate worlds across the galaxy have turned to stone, each one split by a burning red vein. Medusara's gaze has reached us before her eyes have opened. Every Warden is stirring now. Only the Cube's countdown is left.",
  "Eight omens, Commander. Eight Wardens stirring. And the giant at the edge of the galaxy watched every one.",
  "Commander, worlds out on the Rim are turning to stone. Every one of them has a red crack, like a burning eye.", "The stone is still there, Commander. I don't think it's going away."),
]
ARCH = {}
MOOD = {}
for i, (k, t, loc, frag, interp, adv, enc, dfn) in enumerate(OMA):
    ARCH["o_%d" % (i + 1)] = {"cat": "omens", "t": "Omen %d: %s" % (i + 1, t), "era": "Season %d · week %d" % (i // 4 + 1, i % 4 + 1), "civ": "The Omens",
        "loc": loc, "img": "art/arch/%s.webp" % k, "th": "The prologue", "frag": frag, "interp": interp, "adv": adv, "enc": [enc], "def": [dfn]}
    MOOD[enc] = "awe" if i % 2 == 0 else "grave"; MOOD[dfn] = "grave"; MOOD[adv] = "tender"
JD = {"cat": "ages", "t": "The Judge", "era": "Before the first age", "civ": "The Architects", "loc": "The edge of the galaxy", "img": "art/celestial.jpg", "th": "The canon",
      "frag": "The last of the Wardens does not guard a door. It guards the scales.",
      "interp": "The giant at the edge of the galaxy is the Architects' last Warden. It doesn't fight. It holds the Cube in its palm and weighs every seal: each one we hold, each one that cracks. Its eyes opened one by one with the omens. At the Eclipse, it gives its verdict on whoever is left.",
      "adv": "Every seal we hold, it remembers. Every seal we lose, it remembers too. I want it to remember us well.",
      "enc": [], "def": ["Commander, I found it in the Architects' records. The giant at the edge of the galaxy has a name.", "They called it the Judge. And it's been weighing us since the first omen."]}
ARCH["l_judge"] = JD
MOOD[JD["adv"]] = "tender"; MOOD[JD["def"][0]] = "awe"; MOOD[JD["def"][1]] = "grave"
for v in SAY.values():
    for line, m in v.values(): MOOD[line] = m
JS = ('Object.assign(FIN_EV, ' + J(OM) + '); Object.assign(FIN_SAY, ' + J({k: {x: y[0] for x, y in v.items()} for k, v in SAY.items()}) + ');\n'
      + open('tools/patches/p575_omens.js', encoding='utf-8').read())
rep('const FIN_SET = { lev: levSet, brd: brdSet, krk: krkSet, wym: wymSet, aex: aexSet, vae: vaeSet, khz: khzSet, med: medSet };\n',
    'const FIN_SET = { lev: levSet, brd: brdSet, krk: krkSet, wym: wymSet, aex: aexSet, vae: vaeSet, khz: khzSet, med: medSet };\n')
i = s.find('function shFinale() {'); assert i > 0
s = s[:i] + JS + s[i:]
# the Judge in the painting and on the 3D figure
rep('A.aura.material.opacity = e * (.2 + .05 * Math.sin(tt * .6));', 'A.aura.material.opacity = e * (.2 + .05 * Math.sin(tt * .6)); try { judgeArt(W, A, e, t); } catch (er) {} /* v575 */')
rep('X.eyes.forEach((s, i) => { s.material.opacity = e * (.8 + .2 * Math.sin(tt * 2.2 + i)); });',
    '{ const L = judgeLit(now()), bz = judgeBlaze(now(), t); X.eyes.forEach((s, i) => { const j = i >> 1, on = (j % 3) * 2 + (j >= 3 ? 1 : 0) < L; s.userData.s0 = s.userData.s0 || s.scale.x; s.scale.setScalar(s.userData.s0 * (1 + bz * 1.5)); s.material.opacity = on ? e * (.8 + .2 * Math.sin(tt * 2.2 + i)) : e * .05; }); } /* v575 one eye per omen */')
# ---- the Archives
s2, n = re.subn(r'("c_\d+": \{"cat": "saga", "t": "[^"]*", "era": "Season )(\d+)( finale")', lambda m: m.group(1) + str(int(m.group(2)) + 2) + m.group(3), s); assert n == 10, n; s = s2
rep('); /* v571/v572 The Ten Seals */\nconst ARCH_ORD = [', '); Object.assign(ARCH, ' + J(ARCH) + '); /* v575 The Omens */\nconst ARCH_ORD = [')
rep('"l_advisor", "c_1",', '"l_advisor", "l_judge", "c_1",')
rep('"c_10", "e_1"', '"c_10", ' + ', '.join('"o_%d"' % i for i in range(1, 9)) + ', "e_1"')
rep('["saga", "The Ten Seals", "The year', '["omens", "The Omens", "The prologue: eight signs before the Ten Seals, and the giant who watched every one."], ["saga", "The Ten Seals", "The year')
rep('const archName = k => /^c_/.test(k) ? "The Ten Seals" :', 'const archName = k => /^o_/.test(k) ? "The Omens" : /^c_/.test(k) ? "The Ten Seals" :')
rep('if (/^c_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`;',
    'if (/^c_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`; if (/^o_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" style="filter:saturate(.45) brightness(.72) contrast(1.1)" alt="" loading="lazy"></div>`; /* v575 a glimpse */')
rep('/^c_/.test(id) ? "This chapter opens when its season finale begins." :', '/^o_/.test(id) ? "This omen shows on the map in its week of the prologue." : /^c_/.test(id) ? "This chapter opens when its season finale begins." :')
rep('/^c_/.test(id) ? "The chapter" :', '/^o_/.test(id) ? "The sighting" : /^c_/.test(id) ? "The chapter" :')
rep('/^c_/.test(k) ? "Opens at its season finale" :', '/^o_/.test(k) ? "Shows in its omen week" : /^c_/.test(k) ? "Opens at its season finale" :')
rep('/^[bslec]_/', '/^[bsleco]_/', 3)
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
# ---- the Void Pass: the two prologue seasons
rep('["Season of the Petrified Star", "#ff5a4a", "petrified", "Stoneheart"]]; const SEAN',
    '["Season of the Petrified Star", "#ff5a4a", "petrified", "Stoneheart"], ["Season of Omens", "#8fb0e0", "omen", "Omen Seeker"], ["Season of the Countdown", "#ffcf6a", "countdown", "Countdown Keeper"]]; /* v575 10, 11: the prologue */ const SEAN')
rep('vpInfo = (i = vpSeason()) => VP_SEASONS[((i % VP_SEASONS.length) + VP_SEASONS.length) % VP_SEASONS.length];', 'vpInfo = (i = vpSeason()) => VP_SEASONS[seaCos(i)];')
rep('((si % SEAN) + SEAN) % SEAN', 'seaCos(si)', 4)
rep('"Sphinx", "Petrified Star"], COS_C2 = [', '"Sphinx", "Petrified Star", "Omens", "Countdown"], COS_C2 = [')
rep('"#c890ff", "#ffb0a0"];\nconst COS_K', '"#c890ff", "#ffb0a0", "#dfe9ff", "#ffe9b0"];\nconst COS_K')
rep('...Object.fromEntries([0, 1, 2, 3, 4, 5, 6, 7, 8, 9].flatMap(', '...Object.fromEntries([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].flatMap(')
rep('const m = /^([a-z]+?)(F|S)?(\\d)$/.exec(id || "");', 'const m = /^([a-z]+?)(F|S)?(\\d+)$/.exec(id || "");')
rep('const cosSx = (si = vpSeason()) => seaCos(si);', 'const cosSx = (si = vpSeason()) => seaCos(si), cosNo = cx => cx >= 10 ? cx - 9 : cx + 1 + PRO, cosLive = (cx, cur) => cx >= 10 ? cur >= cx - 10 : cur >= PRO + cx; /* v575 the season a set belongs to */')
rep('for (let si = 0; si < COS_SEA.length; si++) { const live = si <= sx || cur >= COS_SEA.length;', 'for (let si = 0; si < COS_SEA.length; si++) { const live = cosLive(si, cur);')
rep('`Void Pass · Season ${d.si + 1} · ${d.free', '`Void Pass · Season ${cosNo(d.si)} · ${d.free')
rep('<small>Season ${d.si + 1}</small>', '<small>Season ${cosNo(d.si)}</small>')
rep('for (let si = 0; si < sx; si++) for (const k of COS_ORDER)', 'for (const si of [...new Set(Array.from({ length: Math.max(0, vpSeason()) }, (_, i) => seaCos(i)))]) for (const k of COS_ORDER)')
rep("Season ${sx + 1}'s arrive here when it ends.", "Season ${vpSeason() + 1}'s arrive here when it ends.")
rep('''{ cracks: .014 }] /* v570 */
];''', '''{ cracks: .014 }], /* v570 */
  ["omen", "Omen Star", 2000, "all", .14, "#9ab8ff", "A pale world gone cold, haunted by the shadows of things that haven't arrived yet.", "ice", ["#2a3a5a", "#7a98c8", "#e8f0ff"], [150, 190, 255], { swirl: 1 }],
  ["countdown", "The Countdown", 2000, "all", .14, "#ffcf6a", "A brass world of turning rings, every gear counting down to the first seal.", "metal", ["#3a2410", "#a0702a", "#f0c070"], [255, 200, 110], { gears: 1 }] /* v575 */
];''')
rep('aeon: 0, ruin: 0, sphinx: 0, petrified: 0 };', 'aeon: 0, ruin: 0, sphinx: 0, petrified: 0, omen: 0, countdown: 0 };')
# ---- the Events hub: the prologue card
rep('function seaFinHTML(T) { try { const si = vpSeason(T), x = ((si % SEA_FIN.length) + SEA_FIN.length) % SEA_FIN.length, w = 4 * si + 2, wed = ROT0 + w * WEEK, sat = ROTS0 + w * WEEK; if (T > sat + 48 * 3600e3) return ""; /* v561 */',
    'function seaFinHTML(T) { try { const si = vpSeason(T), x = seaCyc(si), w = 4 * si + 2, wed = ROT0 + w * WEEK, sat = ROTS0 + w * WEEK; if (T > sat + 48 * 3600e3) return ""; /* v561 */\n'
    '  if (si < PRO) { const ok = si > 0 ? "om2" : "om1", O = FIN_EV[ok], ow = finWinOf(ok, 0), live = T >= ow[0] && T < ow[2], sk = rotKeyS(w), d = t => new Date(t).toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" }), when = t => T >= t ? "<b style=\\"color:#7dff9a\\">now</b>" : `${d(t)} · in <b data-end="${t}">${ftime(t - T)}</b>`, tap = live || duelOwner(); /* v575 the prologue */\n'
    '    return `<div class="seafin"><small>★ THE OMENS · PROLOGUE</small><div${tap ? ` class="finrow" data-act="${live ? "finWatch" : "finSim"}" data-k="${ok}"` : ""}><span>Omen · ${esc(O.n)}</span><em>${T >= ow[2] ? "seen" : when(ow[0])}</em></div>${sk && WB[sk] ? `<div><span>${esc(WB[sk].n)}</span><em>${when(sat)}</em></div>` : ""}<p class="note" style="margin:4px 0 0">The Ten Seals begin in Season ${PRO + 1}. Until then, watch the map for omens.</p></div>`; }')
rep('finOpen: d => openSheet({ type: "finale", k: d.k }),', 'finOpen: d => FIN_EV[d.k] && FIN_EV[d.k].typ === "omen" ? finWatchGo(d.k) : openSheet({ type: "finale", k: d.k }),')
s2 = re.sub(r"GAME_V = 574\b", "GAME_V = 575", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
