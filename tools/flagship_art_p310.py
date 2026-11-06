import sys, base64, os, re
D = os.path.dirname(os.path.abspath(__file__)) + '/art2/'
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
u = lambda n: 'data:image/webp;base64,' + base64.b64encode(open(D + n + '.webp', 'rb').read()).decode()
# ---------- the new paintings: Flagship Command stage and the menu icon ----------
for fac in ['terran', 'solar', 'nyx', 'verdant']:
    t, k = re.subn(r'(\n  ' + fac + r': ")data:image/webp;base64,[A-Za-z0-9+/=]+(")', lambda m: m.group(1) + u('flag-' + fac) + m.group(2), t, count=1); assert k == 1, fac
    cls = '.fsmini-' + fac + '{background-image:url('; i = t.index(cls) + len(cls); j = t.index(')', i); t = t[:i] + u('mini-' + fac) + t[j:]
# ---------- the 3D flagship (map and battles), tuned to the new paintings ----------
# every painting hovers over a holographic ring of its faction's light (Verdant floats on three glowing pods instead)
rep('''  glow(-.6, -.12 - tall * 1.1, 0, 2.6, .22);''', '''  glow(-.6, -.12 - tall * 1.1, 0, 2.6, .22);
  if (fac !== "verdant") { const ry = -.12 - tall * 1.45; for (const [R, tb] of [[1.75, .018], [1.25, .014], [.8, .012], [.38, .01]]) { const rg = ring(-.6, ry, 0, R, tb, NEON, Math.PI / 2, 0, 48); rg.userData.nomid = 1; }
    if (fac === "nyx") { const CY = FLAG_X.cyan || (FLAG_X.cyan = new TH.MeshBasicMaterial({ color: 0x3ff0ff, toneMapped: false })); const rg = ring(-.6, ry, 0, 2.05, .012, CY, Math.PI / 2, 0, 48); rg.userData.nomid = 1; }
    for (const [a, b] of [[-1.5, -.4], [-1.1, -.9], [-.1, -.5], [.3, -1.0]]) beam([a, -.12 - tall * .6, 0], [-.6 + b * .2, ry, 0], .012, NEON); glow(-.6, ry, 0, 1.4, .5); glow(-.6, ry + .05, 0, .5, .9); } // v308''')
# Nyx: the painting's cyan accents among the red: a cyan stern drive and cyan running lights
rep('''      seam([-4.6, -.12 - tall * .46, s * beamW * .5], [3.8, -.12 - tall * .2, s * beamW * .14], .036, .7, .4, .7);''',
    '''      seam([-4.6, -.12 - tall * .46, s * beamW * .5], [3.8, -.12 - tall * .2, s * beamW * .14], .036, .7, .4, .7);
      { const CY = FLAG_X.cyan || (FLAG_X.cyan = new TH.MeshBasicMaterial({ color: 0x3ff0ff, toneMapped: false })); for (const [x, y, w] of [[-3.2, .05, .5], [-1.0, -.18, .4], [1.6, -.02, .35], [3.2, -.1, .3]]) { box(w, .03, .02, CY, x, -.12 + y, s * (beamW * .5 + .012)); glow(x, -.12 + y, s * (beamW * .5 + .06), .2, .7, 0x3ff0ff); } } // v308''')
rep('''for (const [y, z, rr] of fac === "terran" ? [[-.04, 0, .42], [-.04, beamW * .33, .22], [-.04, -beamW * .33, .22]] : [[.06, beamW * .2, .28], [.06, -beamW * .2, .28], [-.3, 0, .24]]) { engine(-4.95, y, z, rr, .2); glow(-5.1, y, z, rr * 2.6, .95); }''',
    '''for (const [y, z, rr] of fac === "terran" ? [[-.04, 0, .42], [-.04, beamW * .33, .22], [-.04, -beamW * .33, .22]] : [[.06, beamW * .2, .28], [.06, -beamW * .2, .28], [-.3, 0, .24]]) { engine(-4.95, y, z, rr, .2); glow(-5.1, y, z, rr * 2.6, .95, fac === "nyx" ? 0x3ff0ff : 0); } // v308 the Nyx drive burns cyan''')
# Union: the deep blue flank panel carrying the laurel-and-sword crest, ahead of the white stripes
rep('''      box(.9, .12, .02, ALT, -2.6, -.02, oz); box(.7, .03, .022, WIN, -2.6, .02, oz); glow(-2.6, 0, oz + s * .06, .45, .5);''',
    '''      { const BL = FLAG_X.ublue || (FLAG_X.ublue = new TH.MeshStandardMaterial({ color: 0x1d3f8f, roughness: .5, metalness: .35 })); box(2.3, tall * .42, .02, BL, -2.75, -.1, oz); const cr = ring(-2.6, -.08, oz + s * .012, .12, .014, WH, 0, 0, 24); cr.scale.set(1, 1.1, 1);
        box(.02, .2, .022, WH, -2.6, -.08, oz + s * .014); box(.07, .02, .022, WH, -2.6, -.01, oz + s * .014); } // v308 crest: a laurel ring round an upright sword''')
# Verdant: brown vines furred with moss, two crystal clusters on the spine, swept tendrils at the stern and three glowing pods beneath
rep('''new TH.MeshStandardMaterial({ color: 0x0d1f07, roughness: 1, metalness: 0, envMapIntensity: .2 })''', '''new TH.MeshStandardMaterial({ color: 0x150d06, roughness: 1, metalness: 0, envMapIntensity: .2 })''')
rep('''new TH.MeshStandardMaterial({ color: 0x26330b, roughness: 1, metalness: 0, envMapIntensity: .2 })''', '''new TH.MeshStandardMaterial({ color: 0x18260a, roughness: 1, metalness: 0, envMapIntensity: .2 })''')
a = t.index('''      for (let i = 0; i < 11; i++) { const x = -3.6 + i * .52''')
b = t.index('\n', a)
t = t[:a] + '''      for (const [cx, n, hh] of [[-2.2, 6, .62], [1.05, 4, .48]]) for (let i = 0; i < n; i++) { const x = cx + (i - n / 2) * .2, h = hh * (.6 + .4 * Math.sin(i * 1.7 + 1) ** 2), lf = new TH.Mesh(new TH.ConeGeometry(.09, h, 5), LF); lf.position.set(x, tall * (x < .7 ? .95 : .82) + h * .4, (i % 2 ? .09 : -.09)); lf.rotation.z = .35 + (i % 3) * .12; lf.rotation.x = (i % 2 ? -.3 : .3); lf.userData.nomid = 1; g.add(lf); if (i % 2 === 0) glow(x - .1, tall * .98 + h * .7, 0, .28, .7); }
      for (let i = 0; i < 5; i++) { const td = new TH.Mesh(new TH.ConeGeometry(.045, 1.5 + i * .18, 5), VN); td.rotation.z = Math.PI / 2 + .18 + i * .07; td.position.set(-4.3 - i * .08, tall * (.25 + i * .14), (i % 2 ? .12 : -.12)); td.userData.nomid = 1; g.add(td); } // swept tendrils
      { const PD = FLAG_X.pod || (FLAG_X.pod = new TH.MeshStandardMaterial({ color: 0x5dffb0, emissive: 0x2aff8a, emissiveIntensity: .9, roughness: .2, metalness: 0, transparent: true, opacity: .55 }));
        for (const x of [-2.1, -.1, 1.9]) { const pd = new TH.Mesh(new TH.SphereGeometry(.42, 18, 10, 0, TAU, Math.PI / 2, Math.PI / 2), PD); pd.position.set(x, -.12 - tall * .42, 0); pd.scale.set(1.05, 1.25, 1); g.add(pd); glow(x, -.12 - tall * .62, 0, .95, .95); glow(x, -.12 - tall * .95, 0, .5, .6); } } // v308 the three glowing pods''' + t[b:]
# the flagship's own materials join its material set M: the map batches parts by M's names, so anything outside M was drawn in plain hull
t, k = re.subn(r'FLAG_X\.(\w+) \|\| \(FLAG_X\.\1 =', lambda m: f'M.x_{m.group(1)} || (M.x_{m.group(1)} =', t); assert k >= 7, k
assert 'FLAG_X.' not in t.replace('const FLAG_X = {};', ''), 'stray FLAG_X'
rep('const GAME_V = 309', 'const GAME_V = 310')
open(p, 'w', encoding='utf-8', newline='').write(t); print('v310')
