# v663 The Mimic Protocol, phase 1 (owner's spec "THE MIMIC PROTOCOL" + four reference paintings; "Omega Neural Nexus" note).
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
js = open('tools/patches/p663_mimic.js', encoding='utf-8').read()
rep('function buildAlien(k) {\n', js + 'function buildAlien(k) {\n  if (MIM_U[k]) return buildMimic(k);\n')
rep('''  sent:      { n: "Petrified Sentinel", atk: 3200, sh: 3000, hull: 80000, val: 180000, one: 1 }
};''', '''  sent:      { n: "Petrified Sentinel", atk: 3200, sh: 3000, hull: 80000, val: 180000, one: 1 },
  // v663 the Mimic Protocol (stats scale with the hive's level, as monsters do)
  mstalk:    { n: "Mimic Stalker", atk: 420, sh: 260, hull: 5200, val: 16000, one: 1 },
  mharv:     { n: "Mimic Harvester", atk: 180, sh: 700, hull: 9000, val: 20000, one: 1 },
  mhunt:     { n: "Mimic Hunter", atk: 900, sh: 300, hull: 6400, val: 26000, one: 1 },
  massim:    { n: "Mimic Assimilator", atk: 650, sh: 900, hull: 11000, val: 40000, one: 1 },
  mguard:    { n: "Mimic Guardian", atk: 500, sh: 2600, hull: 26000, val: 52000, one: 1 },
  mtitan:    { n: "Brood Titan", atk: 3400, sh: 3200, hull: 70000, val: 220000, one: 1 },
  mnest:     { n: "Mimic Hive", atk: 700, sh: 2400, hull: 48000, val: 90000, one: 1 }
};''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
