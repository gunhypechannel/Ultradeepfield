# v709: the story in order (owner: "the story needs to be chronological and make sense to the audience").
# The Tide of the Carcinid ran in January, the Season of the Leviathan, but the Leviathan only breaks the Architects' wall at that season's
# finale (30 January): the Carcinid poured through a breach that didn't exist yet, and Korvax rode the Leviathan (always in chains) before
# its hunt had even happened, so the corpse could never appear. The tide now runs in the Season of the Cube (February), right after the
# wall breaks: the Leviathan's fate is known from the tide's first day, and decides what Korvax rides. The same edits go into the source
# modules (p704_crc.js, p706_story.js) so a later re-apply of those blocks keeps them.
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); SRC = {f: open(os.path.join(D, f), encoding='utf-8').read() for f in ('p704_crc.js', 'p706_story.js')}
def rep(a, b, n=1, src=None):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
    if src: assert SRC[src].count(a) >= 1, (src, a[:90]); SRC[src] = SRC[src].replace(a, b)

# 1. the tide's season: the Season of the Cube, the second of the year (first run: 1 February 2027)
rep('const CRC_RUN = k => k >= PRO && seaCyc(k) === 0;', 'const CRC_RUN = k => k >= PRO && seaCyc(k) === 1; /* v709 the Season of the Cube: right after the Leviathan breaks the wall */', src='p704_crc.js')
rep('''   The season's Leviathan hunt (week 3) decides what Korvax rides in week 4: its corpse (slain) or the beast itself in chains (escaped).''',
    '''   v709 the tide follows the wall breaking: last season's Leviathan hunt (Chapter 1) decides what Korvax rides in week 4: its corpse
   (slain) or the beast itself in chains (escaped).''', src='p704_crc.js')
rep('''In Chapter 1 (this season) the Leviathan turns inward''', '''In Chapter 1 (the season before the tide) the Leviathan turns inward''', src='p704_crc.js')
rep('''   The run: every Season of the Leviathan (the first season of the ten-season year), from season index 2 (4 January 2027).''',
    '''   The run (v709): every Season of the Cube (the second season of the ten-season year), from season index 3 (1 February 2027).''', src='p704_crc.js')
# 2. the Leviathan's fate: its hunt was at the end of last season (about 3-4 weeks before the tide's week 4)
rep('''/* v706 what became of the Leviathan in this season's hunt (Chapter 1): "dead" if the galaxy slew it, else "alive" (escaped, or not yet hunted) */''',
    '''/* v706 what became of the Leviathan in its hunt (Chapter 1, the finale of the season before the tide): "dead" if the galaxy slew it, else "alive" */''', src='p704_crc.js')
rep('if (s0 != null && T - s0 < 20 * 864e5 && finOutcome("lev", s0, T) === "held") return "dead";', 'if (s0 != null && T - s0 < 45 * 864e5 && finOutcome("lev", s0, T) === "held") return "dead"; /* v709 last season\'s hunt */', src='p704_crc.js')
# 3. the words: the wall is already broken when the tide begins
rep('''["First Tides", "The Leviathan is pressing on the Architects' wall from the inside, and the wall is cracking. Breach Zones are tearing open in the outer dark.''',
    '''["First Tides", "The Leviathan broke through the Architects' wall, and the wound never closed. Now Breach Zones are tearing open all along it.''', src='p704_crc.js')
rep('''The Reef Tyrant and the Trench Oracle join the war, the Leviathan's hunt begins at the wall, and the oldest things in the Abyss are rising toward the light.''',
    '''The Reef Tyrant and the Trench Oracle join the war, and the oldest things in the Abyss are rising toward the light.''', src='p704_crc.js')
rep('''This season the Leviathan has turned inward. It hears its old masters calling.</p>''',
    '''Last season the Leviathan turned inward, answering its old masters, and broke through the wall. The breach it left has never closed.</p>''', src='p704_crc.js')
rep('''${on && w >= 3 ? `<p class="note crcfate">${crcLevFate(T) === "dead" ? "The Leviathan was slain at the wall. The Carcinid have dragged its corpse into the Breach, and Korvax rides it." : w >= 4 ? "The Leviathan escaped its hunt. Korvax has it in chains." : "The Leviathan's hunt at the wall decides what Korvax rides in week 4: its corpse, or the beast itself in chains."}</p>` : ""}''',
    '''${on ? `<p class="note crcfate">${crcLevFate(T) === "dead" ? (w >= 4 ? "The Leviathan was slain at the wall. The Carcinid dragged its corpse into the Breach, and Korvax rides it." : "The Leviathan was slain at the wall. The Carcinid are dragging its corpse into the Breach: Korvax means to ride it in week 4.") : w >= 4 ? "The Leviathan escaped its hunt at the wall. Korvax has it in chains." : "The Leviathan escaped its hunt at the wall and fled into the Breach. Korvax is putting it in chains for week 4."}</p>` : ""}''', src='p704_crc.js')
rep('alive and in chains if it escaped its hunt this season, its corpse if the galaxy slew it.', 'alive and in chains if it escaped its hunt at the wall, its corpse if the galaxy slew it.', src='p704_crc.js')
rep('''adv: "He's riding the Warden of the wall into battle, Commander. Whatever happened at the wall this season, he made it his.",''',
    '''adv: "He's riding the Warden of the wall into battle, Commander. Whatever we did to it at the wall, he made it his.",''', src='p706_story.js')
# 4. the Advisor tells the Leviathan's fate as the tide opens (weeks 1-2), not in week 3 as if the hunt were still to come
rep('if (w >= 3 && w <= 4) { const M = crcS(); if (!M.levSaid)', 'if (w >= 1 && w <= 2) { const M = crcS(); if (!M.levSaid)', src='p706_story.js')
rep('if (s0 != null && T - s0 < 20 * 864e5) o = finOutcome("lev", s0, T);', 'if (s0 != null && T - s0 < 45 * 864e5) o = finOutcome("lev", s0, T);', src='p706_story.js')
rep('two four-week invasions back to back (Mimic in December, the Carcinid in January) */', 'two four-week invasions back to back (the Mimic in December, the Carcinid after it) */')
rep('const GAME_V = 708;', 'const GAME_V = 709;')
open(p, 'w', encoding='utf-8').write(s)
if p.endswith('docs/index.html'):
    for f, t in SRC.items(): open(os.path.join(D, f), 'w', encoding='utf-8').write(t)
print('ok')
