"""v745: the Resurrection War's economy: the Continuum Forge, the war reward track, medals, and the Continuum looks with their art."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
eco = open(os.path.join(D, "p745_eco.js"), encoding="utf-8").read().strip()
rep("const GAME_V = 744;", "const GAME_V = 745;")
rep("\n/* ---------- the Continuum's hulls:", "\n" + eco + "\n/* ---------- the Continuum's hulls:")
# War Command: icons for the materials, the forge, the track, the medals
rep('<i class="cntmi" style="--c:${col}"></i>', '<img class="cntmi" src="art/rwar/i_${k}.webp" alt="">')
rep('${S.medals && S.medals.ark ? `<div class="mimmedal"><span>🏆 Arkbreaker ×${S.medals.ark}</span></div>` : ""}', '${cntMedalsHTML()}${cntForgeHTML()}${cntTrackHTML()}')
rep("Quantum Neural Matrices from commanders.</p>", "Quantum Neural Matrices from commanders; Elite Flagship Materials from the Eternal Commander and the Prime Ark's reactor.</p>")
# Elite Flagship Materials drop from the Eternal Commander and the Prime Ark's transmitter and reactor
rep("else { mt.matrix = Math.ceil(seg / 6); if (B.cnt === \"eter\") W.eter++; }", "else { mt.matrix = Math.ceil(seg / 6); if (B.cnt === \"eter\") { W.eter++; mt.elite = Math.ceil(seg / 5); } }")
rep("if (tg === \"rx\") mt.core = Math.ceil(k / 4); else if (tg === \"tx\") mt.matrix = Math.ceil(k / 4);", "if (tg === \"rx\") { mt.core = Math.ceil(k / 4); mt.elite = Math.ceil(k / 5); } else if (tg === \"tx\") mt.matrix = Math.ceil(k / 4);")
rep("const CNT_FREW = { win: [{}, { echo: 80, core: 2, matrix: 1, sh: 30 }, { echo: 160, core: 4, matrix: 2, sh: 60 }, { echo: 260, core: 7, matrix: 4, sh: 100 }],", "const CNT_FREW = { win: [{}, { echo: 80, core: 2, matrix: 1, elite: 1, sh: 30 }, { echo: 160, core: 4, matrix: 2, elite: 2, sh: 60 }, { echo: 260, core: 7, matrix: 4, elite: 3, sh: 100 }],")
# the cosmetics: set 14 is the Continuum's
rep('"Omens", "Countdown", "Carcinid", "Signal"], COS_C2 = [', '"Omens", "Countdown", "Carcinid", "Signal", "Continuum"], COS_C2 = [')
rep('"#3fe8f0", "#d8fff6"];', '"#3fe8f0", "#d8fff6", "#5fd0ff"];')
rep('const col = si === 12 ? "#e8b45a" : VP_SEASONS[si]', 'const col = si === 12 ? "#e8b45a" : si === 14 ? "#ff3346" : VP_SEASONS[si]')
rep('banner12: "art/carcinid/cos-banner.webp",', 'banner12: "art/carcinid/cos-banner.webp", banner14: "art/rwar/cos-banner.webp", frame14: "art/rwar/cos-frame.webp",')
# the hull finish and the planet skin
rep('  mimic: { n: "Mimic Bioweave", t: 99,', '  continuum: { n: "Continuum Black Chrome", t: 99, col: "#0c0d10", rim: "#ff3346", met: .95, rough: .18, k: .9, gl: 1.3, sw: "linear-gradient(135deg,#030304,#16171c 40%,#ff3346 52%,#08080a 64%,#5fd0ff)" }, /* v745 forged */\n  mimic: { n: "Mimic Bioweave", t: 99,')
rep('(f === "carcinid" && !!((S && S.hullOwn) || {}).carcinid));', '(f === "carcinid" && !!((S && S.hullOwn) || {}).carcinid) || (f === "continuum" && !!((S && S.hullOwn) || {}).continuum));')
rep('  ["mimichive", "Neural Hive", 2400,', '  ["cntdebris", "Machine Debris", 2400, "all", .12, "#ff3346", "A world buried in black machine wreckage, its seams still lit red. Forged from the Resurrection War.", "metal", ["#040405", "#121216", "#26262e"], [255, 51, 70], { veins: 1, cracks: .014 }], /* v745 */\n  ["mimichive", "Neural Hive", 2400,')
# the Continuum Commander portrait, for those who forged it
rep('const AV_IDS = AV_LIST.map(a => a[0]);', 'const AV_IDS = AV_LIST.map(a => a[0]);\nconst AV_X = [["continuum", "Continuum Commander"]], AV_XIDS = AV_X.map(a => a[0]); /* v745 forged portraits */')
rep('const avNorm = id => AV_IDS.includes(id) ? id :', 'const avNorm = id => AV_IDS.includes(id) || AV_XIDS.includes(id) ? id :')
rep('const cur = avOf(G.me), ids = AV_LIST.map(x => x[0]), pick = ids.includes(sheet.pick) ? sheet.pick : cur, lab = id => id === "photo" ? "Your photo" : (AV_LIST.find(x => x[0] === id) || [0, ""])[1];',
    'const cur = avOf(G.me), ids = AV_LIST.map(x => x[0]).concat(AV_XIDS.filter(k => ((S.avOwn || {})[k]))), pick = ids.includes(sheet.pick) ? sheet.pick : cur, lab = id => id === "photo" ? "Your photo" : (AV_LIST.concat(AV_X).find(x => x[0] === id) || [0, ""])[1];')
rep('  avatar: d => { if (!AV_IDS.includes(d.id)) return;', '  avatar: d => { if (!AV_IDS.includes(d.id) && !(AV_XIDS.includes(d.id) && (S.avOwn || {})[d.id])) return;')
rep('  if (id === "photo" || !AV_IDS.includes(id)) id = defAv(uid || G.me);\n  { const im = avPic(', '  if (id === "photo" || !(AV_IDS.includes(id) || AV_XIDS.includes(id))) id = defAv(uid || G.me); /* v745 forged portraits draw too */\n  { const im = avPic(')
# actions
rep("  cntFind: d => {", """  cntForge: d => { const F = CNT_FORGE.find(r => r[0] === d.k), M = cntS(); if (!F) return; if (cntOwn(d.k)) return toast("You already own it.", "warn"); if (d.k === "elitefs" && !fsOn()) return toast("Your flagship takes command at commander Lv.15.", "warn"); if (!cntHave(F[3], M)) return toast("Not enough war materials yet.", "warn");
    for (const [k, n] of Object.entries(F[3])) M.m[k] -= n; cntGrant2({ [d.k === "sh" ? "sh" : d.k]: d.k === "sh" ? 25 : d.k === "tcore" ? 1 : 1 }, `Forged: ${F[1]}`); renderSheet(); }, /* v745 */
  cntTrack: d => { const i = +d.i, p = d.p === "1", M = cntS(), row = CNT_TRACK[i], id = (p ? "p" : "f") + i; M.tr = M.tr || {}; if (!row || M.tr[id] || M.pts < row[0] || (p && !mimPrem())) return; M.tr[id] = 1; cntGrant2(p ? row[2] : row[1], `War reward track · ${fmt(row[0])}`); renderSheet(); },
  cntFind: d => {""")
CSS = open(os.path.join(D, "p745.css"), encoding="utf-8").read().replace("\n", "")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
