# v526 the Bestiary (owner approved the card texts, 2026-11-13): a new chapter of the Ancient Archives with a record for each of the
# nine space monsters. A record's fragment (the card text) is recovered the first time you open that monster on the map, and its
# field notes and the Advisor's word open after your first kill. The paintings are the owner's. Bestiary records don't count toward
# the Final Testament (that stays with the ancient records).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
B = [
 ("swhale", "The Hull-Eaters", "Severe", "The Concord's first deep-lane convoys called them \"hull-eaters.\" They follow engine wakes for days and strike only when a ship turns back. The laser turrets in their hides aren't grown.",
  "Someone built those guns into them, Commander. I'd like to know who.", "a titan-class laser platform with the heaviest hide of any monster. Send heavy hulls; Fighters barely scratch it. It drops Exotic Tissue."),
 ("slevi", "The Star-Eaters", "Extreme", "These serpents feed on the light of dying stars. The molten seams in their scales are star-fire they never finished digesting. Old pilots say a leviathan's wake can still burn a week later.",
  "Never fight one near a star. It gets stronger.", "a capital-class plasma beast that hits harder than any other monster. Scout it, then send the heaviest fleet you have. It guards rare flagship materials."),
 ("ssquid", "The Lantern Packs", "High", "They hunt in packs inside gas nebulae, talking in pulses of light that our sensors read as static. Every pack has one elder that never joins the fight.",
  "If the pack ever goes dark at once, pull back. That's the signal.", "cruiser-class acid hunters that come in packs. Bring Cruisers and armour. They drop Exotic Tissue, and sometimes Void Essence."),
 ("vmanta", "The Gulf Gliders", "High", "Mantas glide the empty gulfs between layers on wings that sail on gravity itself. They're curious, and they've been seen pacing ships for hours before turning hostile without warning.",
  "It isn't hunting us at first. It's learning how we turn.", "fast and evasive laser cruisers; slow guns miss them. Fighters and Lancers track them best. They drop Exotic Tissue, sometimes Void Essence."),
 ("swasp", "The Starhive", "High", "A queen buried in a resin nest the size of a station. The swarm grows as long as the nest is fed, and each wasp is a drone of one mind.",
  "Leave the nest standing and the swarm comes back. Always break the nest.", "an acid swarm, one wasp for every level of the hive, guarding an armoured nest. Corvettes and Battleships shred the swarm; Bombers break the nest."),
 ("ctort", "The Slow Crowns", "Severe", "Some of these are older than the moons they graze on. The crystals on their shells grow one layer a century, and miners have followed one for a whole lifetime just to harvest what it sheds.",
  "It isn't angry, Commander. It's just very hard to move.", "a titan with half its damage turned aside by its shell. Bombers and plasma crack it; bring patience. It often drops Quantum Crystal."),
 ("gspider", "The Web Between Stones", "Extreme", "It carries a caged singularity that it feeds with captured ships. Its webs are bent space strung between asteroids, invisible until something is caught.",
  "If your fleet suddenly drifts off course, stop moving. You're in the web.", "a capital-class beast with long gravity lances. Send heavy hulls, and plenty of them. It sometimes carries Void Essence."),
 ("smoth", "The Light-Drinkers", "Moderate", "Drawn to starlight and shield light alike. Clouds of them have stripped whole defense grids bare in a single night, then drifted away glowing brighter.",
  "They don't mean us harm. They just love what keeps us alive.", "ion swarms that strip shields fast, so armour matters more than shields here. Lancers run them down. They often drop Quantum Crystal."),
 ("cram", "The Lane Breakers", "Severe", "A horned beast of ice that rides its own comet and charges anything in its lane, ships, stations and moons alike. The herds migrate on a ring around the Core that takes three hundred years to complete.",
  "Get out of its lane or get under its horns. There's no third choice.", "a capital-class rammer with mass weapons that hit like a battering ram. Lead with Battleships and Bastions. It leaves Reinforced Alloy behind."),
]
js = lambda t: '"' + t.replace('\\', '\\\\').replace('"', '\\"') + '"'
recs = ",\n".join(f'  b_{k}: {{ cat: "best", t: {js(t)}, era: "Field record", civ: "Concord survey fleets", loc: "Wherever {k} roam", img: null, th: {js(th)}, frag: {js(fr)}, interp: {js(fn)}, adv: {js(ad)}, enc: [], def: [] }}'.replace(f"Wherever {k} roam", "Across every layer of the galaxy") for k, t, th, fr, ad, fn in B)
rep('''    enc: ["Commander, the archive fragments are cross-referencing on their own.", "Every civilization. Every age. The same shapes, and the same warning.", "We called them gods because we had no other word for what we saw."], def: [] } };''',
    '''    enc: ["Commander, the archive fragments are cross-referencing on their own.", "Every civilization. Every age. The same shapes, and the same warning.", "We called them gods because we had no other word for what we saw."], def: [] },
  /* v526 the Bestiary */
''' + recs + '''
};''')
rep('["final", "The Final Testament", "What the ancient empires knew, and kept for us."]];', '["final", "The Final Testament", "What the ancient empires knew, and kept for us."], ["best", "The Bestiary", "Field records of the living giants that roam the galaxy."]];')
rep('const ARCH_ORD = ["war", "wym", "col", "ovl", "vae", "khz", "med", "dev", "brd", "tyr", "aex", "est", "efi", "eli", "eic", "ena", "epx", "cube", "testament"];',
    'const ARCH_ORD = ["war", "wym", "col", "ovl", "vae", "khz", "med", "dev", "brd", "tyr", "aex", "est", "efi", "eli", "eic", "ena", "epx", "cube", "testament", ' + ", ".join(f'"b_{k}"' for k, *_ in B) + '];')
rep('const archName = k => k === "cube" ? "The Cube"', 'const archName = k => /^b_/.test(k) && MON[k.slice(2)] ? MON[k.slice(2)].sp : k === "cube" ? "The Cube"')
rep('if (k !== "testament" && Object.values(S.arch).filter(v => v >= 2).length >= 10 && !S.arch.testament)', 'if (k !== "testament" && !/^b_/.test(k) && Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^b_/.test(q)).length >= 10 && !S.arch.testament)')
rep('function archFromRep(r) { try { if (!r) return;', 'function archFromRep(r) { try { if (!r) return; if (r.mon && MON[r.mon] && ARCH["b_" + r.mon] && !r.test) { archUnlock("b_" + r.mon, 1, true); if (r.winner === "a" && (r.aUids || []).includes(G.me)) setTimeout(() => archUnlock("b_" + r.mon, 2), 4000); } /* v526 */')
rep('function archSheetSeen(s) { try { if (!s) return false;', 'function archSheetSeen(s) { try { if (!s) return false; if (s.type === "pirate" && PB[s.id] && PB[s.id].mon && ARCH["b_" + PB[s.id].mon] && !archLv("b_" + PB[s.id].mon)) { archUnlock("b_" + PB[s.id].mon, 1); return false; } /* v526 the Bestiary; her monster line still plays */')
rep('function archImg(E, lv, k) { if (k === "testament" || k === "cube")', 'function archImg(E, lv, k) { if (/^b_/.test(k)) return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/mon/${k.slice(2)}.webp?v=1" alt="" loading="lazy"></div>`; if (k === "testament" || k === "cube")')
rep('`Defeat ${esc(archName(id))} to unlock what the record really means.`', '`${/^b_/.test(id) ? "Defeat a" : "Defeat"} ${esc(archName(id))} to unlock ${/^b_/.test(id) ? "its field notes" : "what the record really means"}.`')
rep('<small>Modern interpretation</small><p>${esc(E.interp)}</p>', '<small>${/^b_/.test(id) ? "Field notes" : "Modern interpretation"}</small><p>${esc(E.interp)}</p>')
s2 = re.sub(r"GAME_V = 525\b", "GAME_V = 526", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
