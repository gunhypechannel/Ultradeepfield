# v607 the Advisor's 24 Titan lines (v606) are voiced: generated with her ElevenLabs voice (UDF Advisor v4, eleven_v4, seed 4242,
# stability .5, similarity .75) with mood tags, converted to docs/voice/<key>.mp3 (index v5) and added to her mood table so her
# hologram takes the same mood as the voice.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
M = json.load(open('tools/titan_voice_moods.json', encoding='utf-8'))
add = ", ".join(json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v) for k, v in M.items())
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + add + ', ')
s2 = re.sub(r"GAME_V = 606\b", "GAME_V = 607", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
