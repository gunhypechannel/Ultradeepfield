# v568 ten seasons (owner's art for Seasons 7-10: "Update all missing art"). After the Wyrm come the Season of the Aeon (Aexion), the
# Ruin (Vaelthar), the Sphinx (Khezaroth) and the Petrified Star (Medusara): each with the owner's banner, portrait frame, token and
# Advisor outfit, and planet skins Aeon Glacier, Ruin of Vaelthar and Sphinx Sands (Season 10 gives the Stone Titan until its own skin
# arrives). Their finales: Aexion + the Iron Tyrant, Vaelthar + the Shard Colossus, Khezaroth + the Void Warden, Medusara + the Orbital
# Devourer. Every "six seasons" in the pass, the cosmetics, the Wardrobe and the boss calendar now counts ten.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('["Season of the Wyrm", "#ffa040", "dragon", "Wyrmrider"]];', '["Season of the Wyrm", "#ffa040", "dragon", "Wyrmrider"], ["Season of the Aeon", "#7ac8ff", "aeon", "Aeonbreaker"], ["Season of the Ruin", "#c890ff", "ruin", "Ruinwalker"], ["Season of the Sphinx", "#ffb340", "sphinx", "Gatekeeper"], ["Season of the Petrified Star", "#ff5a4a", "bonemoon", "Stoneheart"]]; const SEAN = VP_SEASONS.length; /* v568 ten seasons */')
rep('const COS_SEA = ["Leviathan", "Cube", "Pentarch", "Starhive", "Kraken", "Wyrm"], COS_C2 = ["#ffd36b", "#b8ffcf", "#9fb4ff", "#ff6a3a", "#ff6ad5", "#ff3b2a"',
    'const COS_SEA = ["Leviathan", "Cube", "Pentarch", "Starhive", "Kraken", "Wyrm", "Aeon", "Ruin", "Sphinx", "Petrified Star"], COS_C2 = ["#ffd36b", "#b8ffcf", "#9fb4ff", "#ff6a3a", "#ff6ad5", "#ff3b2a", "#e8f6ff", "#ffd36b", "#c890ff", "#ffb0a0"')
rep('function vpReward(i, prem, si = vpSeason()) { const t = i + 1, sx = ((si % 6) + 6) % 6;', 'function vpReward(i, prem, si = vpSeason()) { const t = i + 1, sx = ((si % SEAN) + SEAN) % SEAN;')
rep('const seasonTok = (si = vpSeason()) => `art/season/s${(((si % 6) + 6) % 6) + 1}-token.webp`;', 'const seasonTok = (si = vpSeason()) => `art/season/s${(((si % SEAN) + SEAN) % SEAN) + 1}-token.webp`;')
rep('style="background-image:url(art/season/s${(((si % 6) + 6) % 6) + 1}-banner.webp)"', 'style="background-image:url(art/season/s${(((si % SEAN) + SEAN) % SEAN) + 1}-banner.webp)"')
rep('const cosSx = (si = vpSeason()) => ((si % 6) + 6) % 6;', 'const cosSx = (si = vpSeason()) => ((si % SEAN) + SEAN) % SEAN;')
rep('...Object.fromEntries([0, 1, 2, 3, 4, 5].flatMap(i => [', '...Object.fromEntries([0, 1, 2, 3, 4, 5, 6, 7, 8, 9].flatMap(i => [["adv" + i, `art/season/s${i + 1}-adv.webp`], ')
rep('for (let si = 0; si < 6; si++) { const live = si <= sx || cur >= 6;', 'for (let si = 0; si < COS_SEA.length; si++) { const live = si <= sx || cur >= COS_SEA.length;')
# the boss calendar: ten finales
rep('const SEA_FIN = [["khz", "wym"], ["dv", "ovl"], ["conv", "war"], ["aex", "brd"], ["med", "dev"], ["vae", "wym"]]', 'const SEA_FIN = [["khz", "wym"], ["dv", "ovl"], ["conv", "war"], ["aex", "brd"], ["med", "dev"], ["vae", "wym"], ["aex", "tyr"], ["vae", "col"], ["khz", "war"], ["med", "dev"]]')
rep('const x = ((si % 6) + 6) % 6, L = sat ? ROTS : ROT, fin = SEA_FIN[x][sat ? 1 : 0], pf = SEA_FIN[(x + 5) % 6][sat ? 1 : 0],', 'const NF = SEA_FIN.length, x = ((si % NF) + NF) % NF, L = sat ? ROTS : ROT, fin = SEA_FIN[x][sat ? 1 : 0], pf = SEA_FIN[(x + NF - 1) % NF][sat ? 1 : 0],')
rep('function seaFinHTML(T) { try { const si = vpSeason(T), x = ((si % 6) + 6) % 6,', 'function seaFinHTML(T) { try { const si = vpSeason(T), x = ((si % SEA_FIN.length) + SEA_FIN.length) % SEA_FIN.length,')
# three painted planet skins
rep('  ["voidbloom", "Void Bloom", 1900, "all", .14, "#ff5ae8", "Black stone blooming with radiant pink and violet fractures.", "void", ["#020104", "#0a0610", "#16101e"], [255, 90, 230], { cracks: .016, fractal: 1, moons: 2 }]\n];',
    '''  ["voidbloom", "Void Bloom", 1900, "all", .14, "#ff5ae8", "Black stone blooming with radiant pink and violet fractures.", "void", ["#020104", "#0a0610", "#16101e"], [255, 90, 230], { cracks: .016, fractal: 1, moons: 2 }],
  ["aeon", "Aeon Glacier", 2000, "all", .14, "#7ac8ff", "A frozen world of blue crystal spires under white storm bands, cracked with starlight.", "ice", ["#1a3a6a", "#7ab0e0", "#f0f8ff"], [140, 210, 255], { swirl: 1 }], /* v568 */
  ["ruin", "Ruin of Vaelthar", 2000, "all", .14, "#c890ff", "A violet world of golden temple ruins adrift on seas of glowing nebula.", "void", ["#1a0a2a", "#5a2a8a", "#e0c070"], [200, 140, 255], { fractal: 1 }],
  ["sphinx", "Sphinx Sands", 2000, "all", .14, "#ffb340", "Gold dunes and black glass, crossed by glowing hieroglyph bands around a winged sigil.", "rock", ["#1a1004", "#8a6020", "#ffd080"], [255, 190, 80], { cracks: .01 }]
];''')
rep('hellgate: ["Hellgate", "A burning world split by a steel crescent, guarded by a clawed horror."], dread: 0 };', 'hellgate: ["Hellgate", "A burning world split by a steel crescent, guarded by a clawed horror."], dread: 0, aeon: 0, ruin: 0, sphinx: 0 }; /* v568 */')
s2 = re.sub(r"GAME_V = 567\b", "GAME_V = 568", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
