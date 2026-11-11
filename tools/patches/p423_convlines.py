# v423: the Convergence's Advisor lines no longer repeat themselves. The five "torn loose from the Pentarch" lines, the six "under attack
# right now" lines, the five "won't join the fusion" lines and the five Elemental card introductions were one sentence with the name
# swapped, almost all opening "Commander,"; each is now its own line in its element's voice (frost, fire, light, storm, growth).
import json, re, sys
p = "docs/index.html"; t = open(p).read()
NEW = {
 "wb_shed_eic": "Glacius has been ripped out of the Pentarch! The cold drains from its core.",
 "wb_shed_efi": "Ignis breaks away! The Pentarch's flames are guttering out.",
 "wb_shed_eli": "Solara is torn free, and the Pentarch's light begins to dim.",
 "wb_shed_est": "We've cut Voltaris loose! Its storm no longer answers the Pentarch.",
 "wb_shed_ena": "Verdanth is wrenched away, and the Pentarch's living armour withers.",
 "wb_live_eic": "Fleets are hammering Glacius right now. Want to watch?",
 "wb_live_efi": "A battle is raging around Ignis. Take a look, Commander.",
 "wb_live_eli": "Solara is under fire as we speak. Watch it live.",
 "wb_live_est": "Someone is taking on Voltaris right now, and the storm is fighting back!",
 "wb_live_ena": "Verdanth is under attack. Watch the battle unfold.",
 "wb_live_epx": "The Pentarch is under fire! Every commander should see this.",
 "wb_fall_eic": "Glacius is shattered! One less power for the fusion.",
 "wb_fall_efi": "Ignis is out, snuffed in its own smoke. Its fire will never reach the Void.",
 "wb_fall_eli": "Solara has gone dark. The Pentarch will have no light to call on.",
 "wb_fall_est": "Voltaris is grounded! Its storm is spent before the Convergence.",
 "wb_fall_ena": "Verdanth has withered away. Nothing green will grow inside the Pentarch.",
 "wb3_fuse": "The survivors have reached the Void and fused. The Pentarch is tearing at the black hole. Rally every fleet, Commander!",
}
HOLO = {
 "wbeic": "Glacius, the ice Elemental. Every world in its path is frozen solid. Tomorrow it rides for the Void, so break it while it still stands alone.",
 "wbefi": "That is Ignis, living fire. The worlds around it are burning down to cinders. Douse it now, and the fusion will burn far weaker.",
 "wbeli": "Solara, the Elemental of light, is gilding the worlds around it in a blinding pillar. Dim that light before it reaches the others.",
 "wbest": "Voltaris rides a storm that never ends, and its lightning is tearing at every world nearby. Ground it before the Convergence calls.",
 "wbena": "Verdanth, the green Elemental. Whole worlds are vanishing under its growth. Cut it back now, and the Pentarch will be one power short.",
}
m = re.search(r'const ADV_NEWS = (\{.*?\});\n', t, re.S); news = json.loads(m.group(1)); old = dict(news)
for k, v in NEW.items(): assert k in news, k; news[k] = v
t = t[:m.start(1)] + json.dumps(news, ensure_ascii=False, separators=(", ", ": ")) + t[m.end(1):]
for k, v in HOLO.items():
    rx = re.compile(r'(\b' + k + r': ")([^"]*)(")'); assert len(rx.findall(t)) == 1, k; t = rx.sub(lambda mm: mm.group(1) + v + mm.group(3), t)
t = t.replace("const GAME_V = 422;", "const GAME_V = 423;")
open(p, "w").write(t)
def fnv(s):
    h = 0x811c9dc5
    for c in s: h ^= ord(c); h = (h * 0x01000193) & 0xffffffff
    return h
def b36(n):
    d = "0123456789abcdefghijklmnopqrstuvwxyz"; o = ""
    while n: n, r = divmod(n, 36); o = d[r] + o
    return o
out = [{"key": b36(fnv(v)), "where": "Convergence · " + k, "line": v} for k, v in list(NEW.items()) + list(HOLO.items())]
json.dump(out, open("tools/patches/p423_voice.json", "w"), indent=1, ensure_ascii=False); print("ok", len(out))
