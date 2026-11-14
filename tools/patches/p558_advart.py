# v558 the owner's six Advisor season outfits (art/season/s1..s6-adv.webp, cut to her portrait's 330:1219 shape): the Wardrobe's Advisor
# outfit for each season now shows the painting instead of the tinted hologram (COS_ART, read by cosDef/advArt/advFx).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
a = 'const COS_ART = {}; /* id -> file, filled as the owner\'s season art arrives */'
assert s.count(a) == 1
s = s.replace(a, 'const COS_ART = { adv0: "art/season/s1-adv.webp", adv1: "art/season/s2-adv.webp", adv2: "art/season/s3-adv.webp", adv3: "art/season/s4-adv.webp", adv4: "art/season/s5-adv.webp", adv5: "art/season/s6-adv.webp" }; /* id -> file: the owner\'s season art (v558 Advisor outfits) */')
s2 = re.sub(r"GAME_V = 557\b", "GAME_V = 558", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
