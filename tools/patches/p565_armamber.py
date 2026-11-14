# v565 the Armageddon in amber (owner: "Can we alter the art and the color for the Armageddon to be amber instead of red"). Every red of
# the Armageddon turns amber: its glowing ribs, vents, slits and windows, the cannon's charge and beam, its plasma broadsides, tracers
# and missiles, the arrival rupture in the viewer and its colour on the map. The card painting is re-graded to amber (art/armageddon.webp).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
MAP = {'#ff6a2a': '#ffa62a', '#ff4a2a': '#ff9a1a', '#ff7a3a': '#ffb848', '#ffd0a0': '#ffe2a0', '#ff5a1a': '#ff9c18', '#ffb070': '#ffcc70', '#ff2a12': '#ff9810', '#ff5a2a': '#ffb030', '#ff9a50': '#ffd070',
       '0xff2a12': '0xff9810', '0xff5a2a': '0xffb030', '0xff2a10': '0xff9a10', '0xff3a10': '0xffa010', '0xff4a10': '0xffaa18', '0xff6a2a': '0xffb030', '0xff4a1a': '0xffa020', '0xffb070': '0xffcc70'}
def recolor(a, b, only=None):
    global s
    i = s.find(a); assert i >= 0, a[:50]; j = s.find(b, i + len(a)); assert j > i, b[:50]; seg = s[i:j]; n = 0
    for k, v in MAP.items():
        if only and k not in only: continue
        n += seg.count(k); seg = seg.replace(k, v)
    assert n > 0, a[:50]; s = s[:i] + seg + s[j:]
recolor('function titanFx', 'function titanBeamDraw')
i = s.find('function titanBeamDraw'); recolor('function titanBeamDraw', '  if (m.ti === "l" || m.ti === "p" || m.ti === "t")') # the cannon's charge
recolor('function titanPlate', 'sovereign: { b: [205')
recolor('if (k === "armageddon") o = { hull:', 'else if (k === "sovereign") o =')
recolor('  if (k === "armageddon") { ud.engCol', '  else if (k === "sovereign") { ud.engCol')
recolor('V.k === "armageddon"', 'V.k === "sovereign"')
# the beam itself (the generic end of titanBeamDraw draws the Armageddon's beam, ti "b")
j0 = s.find('function titanBeamDraw'); j1 = s.find('\nfunction ', j0 + 30); k0 = s.find('if (!E0) { ctx.restore(); return; } const k = age / m.life, wv = Lg * .11', j0); assert j0 < k0 < j1
seg = s[k0:j1]; n = 0
for k, v in MAP.items(): n += seg.count(k); seg = seg.replace(k, v)
s = s[:k0] + seg + s[j1:]; print('beam colours', n)
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('armageddon:    ["missile", 8, "#ff6a2a", .22, { flank: 1 }]', 'armageddon:    ["missile", 8, "#ffa62a", .22, { flank: 1 }]')
rep('armageddon: "#ff5a2a", sovereign: "#a8e4ff"', 'armageddon: "#ffb030", sovereign: "#a8e4ff"')
rep('"Fortress Point Defence: red tracer streams"', '"Fortress Point Defence: amber tracer streams"')
rep('arrive: "Emerges from a burning crimson rupture, its cannon powering up"', 'arrive: "Emerges from a burning amber rupture, its cannon powering up"')
s2 = re.sub(r"GAME_V = 564\b", "GAME_V = 565", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
