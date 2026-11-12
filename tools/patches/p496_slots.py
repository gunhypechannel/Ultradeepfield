# v496: fleet slots come from Computer Technology (and colonies, officers, VIP), not Fleet Command (which raises allies per strike).
# The "slots full" toast and the voiced FAQ answer said "Research Fleet Command"; both now name Computer Technology (FAQ re-voiced).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('slots are in use. Research Fleet Command for more.`', 'slots are in use. Research Computer Technology or settle a colony for more.`')
rep('"All your fleet slots are busy. Research Fleet Command, settle more colonies, or wait for a fleet to come home. Every colony adds a slot."',
    '"All your fleet slots are busy. Research Computer Technology, settle more colonies, or wait for a fleet to come home. Every colony adds a slot."')
s = re.sub(r"GAME_V = 495\b", "GAME_V = 496", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
