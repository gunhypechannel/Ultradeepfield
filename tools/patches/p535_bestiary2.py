# v535 the Bestiary grows (owner approved the texts 2026-11-13: "Approved approved approved"): the five special creatures (Kraken
# Eggs, Ghost Whale, Rock Eaters, Celestial Serpent, Petrified Sentinel), the Hive and the Collective. Same record format as v526.
# The specials unlock like the other monsters (first sight on the map, field notes after a win). The Hive (b_hive) unlocks from any
# Hive battle report (an alien fight that isn't a monster), the Collective (b_coll) from any fight with Cube units or the Omega Cube;
# their field notes open when you win one. Paintings: art/mon/<kind>.webp (the Collective uses the cube painting).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
B = [
 ("kegg", "The Violet Clutch", "Moderate", "Glass eggs in a nest of black thorns, each lit violet from inside. Salvage crews who tried to tow one home found its thorns had grown into their hull by morning. Whatever laid them has never been seen, and the clutches keep appearing.",
  "Every clutch we leave alone is one more of whatever laid it.", "a stationary nest that barely fights back but takes a beating. Bombers and heavy hulls crack it. It often holds Void Essence."),
 ("gwhale", "The Night Singers", "High", "A whale of cold light with its bones glowing through its skin. Night-shift crews hear it on open channels, a long low song no translator can parse. By morning it is gone, and nothing on any scanner shows where it went.",
  "Hunt it at night, Commander. It won't wait for us.", "a capital-class beast with ion weapons that strip shields, and it slips a lot of shots. It only surfaces at night, your local time. Fast ships track it best. It often drops Quantum Crystal."),
 ("reat", "The Belt Gnawers", "Moderate", "Barrel worms of plated stone that tunnel through asteroids and leave them hollow. Mining stations along the belts have been eaten from the inside out. The worms glow brighter with every hull they swallow.",
  "If an asteroid starts glowing, move the miners. Now.", "cruiser-class packs with mass weapons that hit armour hard. Lead with shields and strike fast. They often leave Reinforced Alloy behind."),
 ("cserp", "The Golden Brood", "High", "A hatchling of a serpent race older than the Concord: midnight scales edged in gold, violet fire behind its eyes. The adults have never been seen. The hatchlings are out here alone, and every year there are more of them.",
  "A hatchling this strong, Commander. I'd rather not meet its mother.", "a fast, evasive cruiser that burns with plasma. Slow guns miss it: bring Fighters and Lancers. It often carries Void Essence."),
 ("sent", "The Ones Who Wait", "Extreme", "Stone guardians the size of mountains, moss in their seams, standing watch over passes no one uses anymore. Their green runes match nothing in the Archives. They don't attack anything that keeps its distance.",
  "It's guarding something, Commander. I want to know what.", "a titan that never moves and hits like a mountain falling. Send your heaviest fleet, and plenty of it. Sometimes a Cube Fragment is buried inside it."),
 ("hive", "Vael'Khor's Children", "Severe", "The swarm that holds most of the galaxy's worlds, every drone and garrison answering to the Hive Matriarch. They stripped our convoy on the way in. They don't take prisoners and they don't bargain.",
  "Every Hive world we take back is one she has to feed without.", "Hive garrisons grow with each world's level and keep raiding your colonies. Beat their worlds for resources, and build defenses before they come back."),
 ("coll", "The Assimilators", "Extreme", "The builders of the Cubes: drones of one mind that take apart whole fleets and fold them into their own hulls. Every great Cube Devastation starts with one Cube waking up.",
  "Don't let it take our ships, Commander. It learns from every one.", "The Cubes and their Wardens grow stronger with each level. Joint strikes with your alliance break them, and they drop Cube Fragments."),
]
js = lambda t: '"' + t.replace('\\', '\\\\').replace('"', '\\"') + '"'
recs = "".join(f',\n  b_{k}: {{ cat: "best", t: {js(t)}, era: "Field record", civ: "Concord survey fleets", loc: "Across every layer of the galaxy", img: null, th: {js(th)}, frag: {js(fr)}, interp: {js(fn)}, adv: {js(ad)}, enc: [], def: [] }}' for k, t, th, fr, ad, fn in B)
i = s.index('  b_cram: { cat: "best"'); j = s.index('\n', i)
assert s[j - 1] == '}', s[j - 3:j + 3]; s = s[:j] + recs + s[j:]
rep(', "b_cram"];', ', "b_cram", ' + ", ".join(f'"b_{k}"' for k, *_ in B) + '];')
rep('const archName = k => /^b_/.test(k) && MON[k.slice(2)] ? MON[k.slice(2)].sp :', 'const archName = k => k === "b_hive" ? "The Hive" : k === "b_coll" ? "The Collective" : /^b_/.test(k) && MON[k.slice(2)] ? MON[k.slice(2)].sp :')
rep('<img src="art/mon/${k.slice(2)}.webp?v=1"', '<img src="art/mon/${k === "b_coll" ? "cube" : k.slice(2)}.webp?v=1"')
rep('if (r.mon && MON[r.mon] && ARCH["b_" + r.mon] && !r.test) {', '''{ const won = (r.winner === "a" && (r.aUids || []).includes(G.me)) || (r.winner === "d" && r.dUid === G.me), ks = JSON.stringify(r.start || {}); /* v535 the Hive and the Collective */
    const bk = r.test ? null : r.omega || /"(cube|sphere|cdrone)"/.test(ks) ? "b_coll" : r.alien && !r.mon ? "b_hive" : null; if (bk && ARCH[bk]) { archUnlock(bk, 1, true); if (won) setTimeout(() => archUnlock(bk, 2), 4000); } }
  if (r.mon && MON[r.mon] && ARCH["b_" + r.mon] && !r.test) {''')
rep('`${/^b_/.test(id) ? "Defeat a" : "Defeat"} ${esc(archName(id))}', '`${id === "b_hive" || id === "b_coll" ? "Win a battle against" : /^b_/.test(id) ? "Defeat a" : "Defeat"} ${esc(archName(id))}')
s2 = re.sub(r"GAME_V = 534\b", "GAME_V = 535", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
