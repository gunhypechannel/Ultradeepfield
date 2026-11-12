# v485 (owner: "In battle simulation omega cube should be bigger, its scale is far greater than any other boss right now, Aexion need
# to be moved down in the battle report for a more immersive battle experience"). The Omega Cube's report camera comes in close and its
# picture gets a larger box, so it towers over the fleet; Aexion's camera aims higher so he stands lower in the frame, feet in the fight.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("omega: [0, [-10, 7, 40], [0, 0, 0]]", "omega: [0, [-6, 4, 26], [0, 1.5, 0]]")
rep("aexion: [-.4, [-26, 2, 64], [0, -2, 0]]", "aexion: [-.4, [-26, 10, 64], [0, 9, 0]]")
rep("const tl = H > W * 1.1, aw = Math.min(Lc * 2.6, W * .96), ah = tl ? aw * .85 : aw / 2;",
    "const big = wbk === \"omg\" ? 1.35 : 1, tl = H > W * 1.1, aw = Math.min(Lc * 2.6 * big, W * (big > 1 ? 1.15 : .96)), ah = tl ? aw * .85 : aw / 2;")
s = re.sub(r"GAME_V = 484\b", "GAME_V = 485", s)
open(P, 'w').write(s)
# (owner: "What about Aexion as other form"; "Vaelthar needs to be larger in scale in battle report also") Aexion's Warform, the tall
# mech, gets its own framing: the camera stands back and aims higher, so the whole mech stands in the fight with its feet among the
# fleet. Vaelthar's camera comes in closer and his picture gets a larger box, like the Omega Cube's.
s = open(P).read()
rep("vaelthar: [-.35, [-30, 10, 74], [0, 8, 0]]", "vaelthar: [-.35, [-21, 9, 50], [0, 9, 0]]")
rep("const m3 = wbD(key).m3, V0 = WB_VIEW[m3]", "const m3 = wbD(key).m3, V0 = m3 === \"aexion\" && battle && battle.r && battle.r.sbForm ? [-.4, [-26, 14, 70], [0, 14, 0]] : WB_VIEW[m3]")
rep('const big = wbk === "omg" ? 1.35 : 1,', 'const big = wbk === "omg" ? 1.35 : wbk === "vae" ? 1.2 : 1,')
open(P, 'w').write(s)
