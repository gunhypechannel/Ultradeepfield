# v570 Season 10's own planet skin, the Petrified Star (the owner's painting: a world of grey stone, temples, serpents and Medusara's
# face, split by crimson veins). It replaces the stand-in (Bone Moon) as the Season of the Petrified Star's planet reward.
# Also: the Leviathan's and the Kraken's paintings for the Events hub banner, its boss strip and their Archives pages
# (art/arch/lev.webp, krk.webp; v569 left those images missing).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''{ cracks: .01 }]
];''', '''{ cracks: .01 }],
  ["petrified", "Petrified Star", 2000, "all", .14, "#ff5a4a", "A world turned to stone by a gorgon's gaze: temples, coiled serpents and a sleeping face, split by veins of burning crimson.", "rock", ["#141012", "#5a4a4e", "#c8b8b8"], [255, 70, 60], { cracks: .014 }] /* v570 */
];''')
rep('dread: 0, aeon: 0, ruin: 0, sphinx: 0 };', 'dread: 0, aeon: 0, ruin: 0, sphinx: 0, petrified: 0 };')
rep('["Season of the Petrified Star", "#ff5a4a", "bonemoon", "Stoneheart"]', '["Season of the Petrified Star", "#ff5a4a", "petrified", "Stoneheart"]')
s2 = re.sub(r"GAME_V = 569\b", "GAME_V = 570", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
