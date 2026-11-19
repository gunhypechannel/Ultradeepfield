# v650 voice: the 45 most-heard unvoiced advisor lines (screen intros, the veteran briefing, Premium deck, Xeno Sanctuary, eggs, captains)
# now speak in the advisor's ElevenLabs voice. Their moods drive the holo's expression.
import sys, json
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
M = json.load(open(sys.argv[2], encoding='utf-8'))
i = s.index('ADV_MOOD_L = {'); j = s.index('};', i)
d = json.loads(s[i + 13:j + 1]); d.update(M)
s = s[:i + 13] + json.dumps(d, ensure_ascii=False, separators=(', ', ': ')) + s[j + 1:]
a = 'const GAME_V = 649'
if s.count(a) != 1: raise SystemExit('GAME_V')
s = s.replace(a, 'const GAME_V = 650')
open(p, 'w', encoding='utf-8').write(s)
