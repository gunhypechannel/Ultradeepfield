# v572 The Ten Seals, all ten chapters (owner: "I want it all, the live events, the story, and perfect seamless transitions, each
# should have their own unique animations that fit them and their story, they should show off their grand scale").
# Engine v2 (p572_finale.js replaces the v571 block): chapter n is season n's finale, the year repeats every ten seasons (finWinOf);
# Saturday world boss chapters (wb: Leviathan, Starhive/Matriarch, Kraken, Wyrm) open their fight when the set piece ends; Wednesday
# super boss chapters (sb: Aexion, Vaelthar, Khezaroth, Medusara) play their set piece in the 150 minutes before the boss tears in,
# so it arrives at the climax; chapters 2 and 3 are Cube Devastation and the Convergence (story, ledger and Archives).
# Seamless: the giant shrinks into the boss at its place and size in the last 40 seconds (finHand); Watch rides with the action and
# hands over to the boss's own cinematic; "Previously..." recaps how the last seal went at every chapter's start; each result is
# followed by the stinger for the next chapter. Seven new set pieces (brdSet, krkSet, wymSet, aexSet, vaeSet, khzSet, medSet).
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
D = json.load(open('tools/patches/p572_chapters.json', encoding='utf-8'))
J = lambda o: json.dumps(o, ensure_ascii=False)
M = 60e3
FIN = {}
for k, v in D['fin'].items():
    v = dict(v); v['set'] = v['set'] * M
    if 'st' in v: v['st'] = [[a * M, b, c, d] for a, b, c, d in v['st']]
    FIN[k] = v
SAY = {k: {x: y[0] for x, y in v.items()} for k, v in D['say'].items()}
# FIN_EV, early
s2, n = re.subn(r'const FIN_EV = \{.*?\}; /\* v571 The Ten Seals: the season finales\' great events \*/', lambda m: 'const FIN_EV = ' + J(FIN) + '; /* v571/v572 The Ten Seals: the season finales\' great events */', s, flags=re.S); assert n == 1; s = s2
# the block
i = s.find('/* ---------- v571 The Ten Seals'); j = s.find('setInterval(() => { try { finLedTick(); } catch (e) {} }, 5000);\n', i); assert 0 < i < j
JS = 'const FIN_SAY = ' + J(SAY) + ';\n' + open('tools/patches/p572_finale.js', encoding='utf-8').read()
s = s[:i] + JS + s[j + len('setInterval(() => { try { finLedTick(); } catch (e) {} }, 5000);\n'):]
# the calendar, the ledger, the camera, the Boss Lab, the Archives
rep('return [sat + (FIN_EV[k] ? FIN_EV[k].set : 0), sat + WB_LIVE]; }', 'return [sat + finShift(k, sat), sat + WB_LIVE]; }')
rep('if (FIN_EV[key]) { const fs = rotStartOf(key, at); if (fs != null) cur.ledger[fs] = "held"; } } /* v571 the seal holds */', '{ const fk = key === "epx" ? "conv" : key, fw = FIN_EV[fk] ? finCur(fk, at) : null; if (fw) cur.ledger[fw[0]] = "held"; } } /* v571/v572 the seal holds */')
s2, n = re.subn(r'  finWatch: d => \{ closeSheet\(\);.*?\}, 300\); \},\n', '  finWatch: d => finWatchGo(d.k),\n', s, flags=re.S); assert n == 1, n; s = s2
rep('if (k === "conv") return convSimStart(); if (FIN_EV[k]) return finSimStart(k); /* v571 */', 'if (k === "conv") return convSimStart();')
rep('const k = d.k; if (SBW[k]) return sbSimStart(k);', 'const k = d.k; if (FIN_EV[k] && FIN_EV[k].st) return finSimStart(k); /* v572 the finale first, then the boss */ if (SBW[k]) return sbSimStart(k);')
s2, n = re.subn(r'\n    for \(const fk in FIN_EV\) \{ const ck = "c_" \+ FIN_EV\[fk\]\.ch.*?/\* v571 \*/', '\n    if (finArchTick(T)) return; /* v571/v572 The Ten Seals */', s, flags=re.S); assert n == 1, n; s = s2
rep('<div><span>${esc(NM[a] || a)}</span><em>${when(wed)}</em></div>', '<div${FIN_EV[a] && FIN_EV[a].st ? ` class="finrow" data-act="finOpen" data-k="${a}"` : ""}><span>${FIN_EV[a] && FIN_EV[a].st ? `Chapter ${FIN_EV[a].ch} · ${esc(FIN_EV[a].n)}` : esc(NM[a] || a)}</span><em>${when(wed)}</em></div>')
CH = {}
for k, v in D['arch'].items():
    CH[k] = {"cat": "saga", "t": v['t'], "era": v['era'], "civ": "The Seal Ledger", "loc": v['loc'], "img": v['img'], "th": "The Ten Seals", "frag": v['frag'], "interp": v['interp'], "adv": v['adv'], "enc": v['enc'], "def": v['def']}
rep('); /* v571 The Ten Seals */\nconst ARCH_ORD = [', '); Object.assign(ARCH, ' + J(CH) + '); /* v571/v572 The Ten Seals */\nconst ARCH_ORD = [')
rep('"l_advisor", "c_1", "e_1"', '"l_advisor", ' + ', '.join('"c_%d"' % i for i in range(1, 11)) + ', "e_1"')
MOOD = {}
for v in D['say'].values():
    for line, m in v.values(): MOOD[line] = m
for v in D['arch'].values():
    for x in v['enc']: MOOD[x] = 'awe'
    for x in v['def']: MOOD[x] = 'grave'
    MOOD[v['adv']] = 'tender'
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
rep('else for (const k2 in SBW) { const nx = sbNext(k2, T); if (nx - T < 72 * SB_H) {', 'else for (const k2 in SBW) { const nx = sbNext(k2, T), fF = finNow(T); if (fF && fF.k === k2) break; /* v572 its finale set piece has the band */ if (nx - T < 72 * SB_H) {')
s2 = re.sub(r"GAME_V = 571\b", "GAME_V = 572", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
