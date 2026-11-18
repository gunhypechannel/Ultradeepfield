# v621: the battle's round gong, victory and defeat stings, picked by the owner in a second round of four styles each
# (round: "Starship bell", victory: "Sci-fi synth", defeat: "Sad cello"). Files in docs/sfx/; levels in p620_sfx.json (calibrated
# to the old sounds' loudest 100 ms in an offline render; the two end stings +2 dB, as the old ones were quiet).
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
G = json.load(open('tools/patches/p620_sfx.json'))
a = re.search(r'const SFX_F = \{[^}]*\};', s).group(0); s = s.replace(a, 'const SFX_F = ' + json.dumps(G) + ';', 1)
assert s.count('sfx/${k}.mp3?v=620') == 1; s = s.replace('sfx/${k}.mp3?v=620', 'sfx/${k}.mp3?v=621')
s2 = re.sub(r"GAME_V = 620\b", "GAME_V = 621", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
