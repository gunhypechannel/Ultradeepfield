"""v793: the Mimic units each with its own silhouette (owner: "build it all"). They all came from one recipe with nearly the same
settings, so the Stalker, Hunter, Harvester, Assimilator, Guardian and Brood Titan looked alike. Now each is pushed to its own extreme,
after the paintings and their roles: the Stalker a maned beast with a huge mane and jaws gaping wide; the Hunter long and sleek, almost
maneless, trailing long whip tails; the Harvester short and squat round its sac; the Assimilator plated with a high hump; the Guardian
heavy and armoured, short, with little mane; the Brood Titan a giant (half again as big) with a vast mane and hump. Re-sculpted
(tools/sculpt/mim_sculpt.py, art/mimic/m/<class>.bin) with the game's own table updated to match, so their swimming still fits.
Applies on top of v792."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 792;", "const GAME_V = 793;")
rep('const MIM_D = { mstalk: { s: 1, legs: 4, mane: 26, hump: .5, len: 1, gape: .55, tail: 8 }, mhunt: { s: .95, legs: 2, mane: 18, hump: .15, len: 1.35, gape: .8, tail: 16 }, mharv: { s: 1, legs: 0, mane: 12, hump: 0, len: .8, gape: .35, tail: 4, sac: 1 },\n    massim: { s: 1.05, legs: 4, mane: 20, hump: .45, len: 1.05, gape: .6, tail: 8, plates: 1 }, mguard: { s: 1.15, legs: 4, mane: 14, hump: .25, len: .9, gape: .4, tail: 6, armour: 1 }, mtitan: { s: 1.25, legs: 4, mane: 40, hump: .8, len: 1.1, gape: .7, tail: 12, brood: 1 } ', 'const MIM_D = { mstalk: { s: 1, legs: 4, mane: 44, hump: 0.7, len: 1, gape: 0.95, tail: 10}, mhunt: { s: 0.95, legs: 2, mane: 8, hump: 0.05, len: 1.75, gape: 0.85, tail: 30}, mharv: { s: 1.05, legs: 0, mane: 6, hump: 0, len: 0.65, gape: 0.3, tail: 3, sac: 1 },\n    massim: { s: 1.1, legs: 4, mane: 22, hump: 1.0, len: 1.0, gape: 0.6, tail: 6, plates: 1 }, mguard: { s: 1.3, legs: 4, mane: 10, hump: 0.45, len: 0.8, gape: 0.35, tail: 4, armour: 1 }, mtitan: { s: 1.5, legs: 4, mane: 64, hump: 1.15, len: 1.15, gape: 0.8, tail: 18, brood: 1 } ')
open(p, "w", encoding="utf-8").write(s)
print("ok")
