import sys, base64, os, glob
D = os.path.dirname(os.path.abspath(__file__)) + '/pack/out/'
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:100]); t = t.replace(a, b)
u = lambda n: 'data:image/webp;base64,' + base64.b64encode(open(D + n + '.webp', 'rb').read()).decode()
names = sorted(os.path.basename(f)[:-5] for f in glob.glob(D + '*.webp'))
W = '#sheetwrap[data-type="flagship"]'
css = '/* v302 the Flagship art pack: faction gear, materials, set emblems, skill trees and skills */\n'
css += ''.join(f'.fsimg.fsg-{n[5:]}{{background-image:url({u(n)});background-size:cover;border-radius:8px}}' for n in names if n.startswith('gear-')) + '\n'
css += ''.join(f'.fsmat-{n[4:]}{{background-image:url({u(n)})}}' for n in names if n.startswith('mat-')) + '\n'
css += ''.join(f'.fsset-{n[4:]}{{background-image:url({u(n)})}}' for n in names if n.startswith('set-')) + '\n'
css += ''.join(f'.fstr-{n[5:]}{{background-image:url({u(n)})}}' for n in names if n.startswith('tree-')) + '\n'
css += ''.join(f'.fssk-{n[3:]}{{background-image:url({u(n)})}}' for n in names if n.startswith('sk-')) + '\n'
css += f'''.fsmi,.fsseti,.fstri,.fsski{{display:inline-block;flex:none;vertical-align:middle;background-position:center;background-size:cover;background-repeat:no-repeat}}
.fspk{{display:block;width:34px;height:24px;margin:0 auto}}
.fsmi{{width:18px;height:18px;border-radius:4px;margin-right:2px}}.fsmi.lg{{width:34px;height:34px;border-radius:7px;margin-right:8px;box-shadow:0 0 8px rgba(80,200,255,.35)}}
.fsseti{{width:22px;height:22px;margin-right:5px}}.fsr .fsseti{{width:30px;height:30px}}
.fstri{{width:44px;height:36px;margin-right:8px;border-radius:6px;background-size:contain}}.fstree h3{{display:flex;align-items:center}}
.fsski{{width:52px;height:46px;border-radius:8px;border:1px solid color-mix(in srgb,var(--tc,#38dfee) 55%,transparent)}}.fsnode>span:first-of-type{{flex:1;min-width:0}}
.fsf button .fsseti{{display:block;margin:0 auto 2px}}
{W} .fshero img{{animation:fsFloat 7s ease-in-out infinite;width:84%;max-width:600px}}
@keyframes fsFloat{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
@media (prefers-reduced-motion:reduce){{{W} .fshero img{{animation:none}}}}
'''
rep('''.cubeband.live{animation:cubePulse''', css + '''.cubeband.live{animation:cubePulse''')
# painted faction flagships on the stage (the Nyx ship lit in its own blood red); the 3D render stays as the fallback
port = ',\n  '.join(f'{n[5:]}: "{u(n)}"' for n in names if n.startswith('flag-'))
rep('''function fsArt(fac) { if (FS_ART[fac]) return FS_ART[fac];''', '''const FS_PORT = {
  ''' + port + '''
}; // v302 painted portraits, one per faction
function fsArt(fac) { if (FS_PORT[fac]) return FS_PORT[fac]; if (FS_ART[fac]) return FS_ART[fac];''')
# gear: each faction's own icon on its items and on an equipped slot
rep('''const fsItemName = it =>''', '''const fsGearCls = it => it && FS_FAC[it.f] ? `fsg-${it.s}-${it.f}` : `s-${it ? it.s : "weapon"}`; // v302
const fsItemName = it =>''')
rep('''<span class="fsic fsimg s-${it.s}"></span>''', '''<span class="fsic fsimg ${fsGearCls(it)}"></span>''')
rep('''data-act="fsSlot" data-s="${s}" aria-label="${n}"><span class="fsimg s-${s}"></span>''', '''data-act="fsSlot" data-s="${s}" aria-label="${n}"><span class="fsimg ${it ? fsGearCls(it) : `s-${s}`}"></span>''')
# materials
rep('''style="--tc:${FS_TIER[t][1]}"><i>${m[1]}</i>${FS_TIER[t][0]}''', '''style="--tc:${FS_TIER[t][1]}"><i class="fsmi fsmat-${k.slice(0, -1)}"></i>${FS_TIER[t][0]}''')
rep('''<div class="fstree"><h3>${FS_MATS[m][1]} ${FS_MATS[m][0]}</h3>''', '''<div class="fstree"><h3><i class="fsmi lg fsmat-${m}"></i>${FS_MATS[m][0]}</h3>''')
# sets
rep('''<div class="fsr"><span>${FS_SETS[s][0]} · ${n}/6</span>''', '''<div class="fsr"><span><i class="fsseti fsset-${s}"></i>${FS_SETS[s][0]} · ${n}/6</span>''')
rep('''data-act="fsPick" data-k="fset" data-v="${k}">${v[0]}</button>''', '''data-act="fsPick" data-k="fset" data-v="${k}"><i class="fsseti fsset-${k}"></i>${v[0]}</button>''')
# skills
rep('''<div class="fstree" style="--tc:${col}"><h3>${n}</h3>''', '''<div class="fstree" style="--tc:${col}"><h3><i class="fstri fstr-${id}"></i>${n}</h3>''')
rep('''return `<div class="fsnode"><span><b>${nd[2]}</b>''', '''return `<div class="fsnode"><i class="fsski fssk-${id + i}"></i><span><b>${nd[2]}</b>''')
# forge slot picker: the slot icons in place of the glyphs
rep('''data-act="fsPick" data-k="fs" data-v="${k}" title="${n}">${ic}</button>''', '''data-act="fsPick" data-k="fs" data-v="${k}" title="${n}" aria-label="${n}"><span class="fsimg fspk s-${k}"></span></button>''')
# the Dock's painted card
rep('''"radar robotics dome bigDome metalMine metalStore nanite interceptor ballistic").split(" ")''', '''"radar robotics dome bigDome metalMine metalStore nanite interceptor ballistic flagDock").split(" ")''')
rep('const GAME_V = 301', 'const GAME_V = 302')
open(p, 'w', encoding='utf-8', newline='').write(t); print('v302', len(t))
