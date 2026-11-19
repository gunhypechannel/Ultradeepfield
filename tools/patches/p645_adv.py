# v645 advisor (owner: "Feels like we're missing advisor lines for explaining certain things or for certain battles", "Build all of that"):
# reactions to ordinary battles (win and loss, with a tip on a loss), first-visit explanations for the screens that had none,
# a one-time "what changed" briefing for veterans, and the rune line brought up to date. New lines are text only until voiced.
import sys, json
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

BT = {
 "hunt": {"w": ["Got it, Commander. That beast won't trouble the shipping lanes again.",
                "Clean hunt. Monsters sometimes leave rune shards behind, so check the Elements page now and then.",
                "One fewer monster out there. The deeper layers breed bigger ones, and we're ready for them."],
          "l": ["It was too much for us this time. Monsters shrug off light craft: send battleships and destroyers.",
                "We lost that hunt. Send a probe first next time, Commander. It tells us how strong the thing really is.",
                "Beaten back. More Weapons and Armour research, or more heavy hulls, and we'll have it next time."]},
 "pirate": {"w": ["The pirates scattered, Commander. Their holds are ours.",
                  "Raid done. Pirates regroup in a few hours, and then the hideout is worth hitting again.",
                  "Good work. Bring cargo ships next time and we carry home everything they had."],
            "l": ["The pirates held. Their crews were stronger than they looked, so spy the hideout before the next run.",
                  "We were driven off. Pick a hideout closer to our level, Commander. The Finder shows their levels.",
                  "Lost that one. A few more warships, and the same hideout falls."]},
 "cube": {"w": ["The Cube's shell is cracked, Commander. The Hive will feel that one.",
                "A Cube broken. Its wrecks stay in orbit for a while, so send recyclers before someone else does.",
                "That's how you take apart a Cube. The Hive is going to remember us."],
          "l": ["The Cube is beyond one fleet. Start a joint strike and let your alliance hit it with you.",
                "Its drones overwhelmed us. Bring more ships with shields, and bombers for its armour.",
                "The Cube held. Cubes in the outer layers are weaker; start there and work inward."]},
 "pyramid": {"w": ["The guardians fell. Whatever the pyramid kept is ours now.",
                   "Pyramid cleared, Commander. The old empires built those to keep something in. Or out.",
                   "Well fought. Pyramids are the best place to find rune shards."],
             "l": ["The guardians held. Pyramids test strength, not speed: bring heavier ships.",
                   "Driven back from the pyramid. Its guardians are tough, but they don't heal. Try again stronger.",
                   "Not this time. Research and a bigger fleet, then we go back."]},
 "attack": {"w": ["Their defences are down, Commander. Send a Colony Ship if you want to hold that world.",
                  "Strike successful. Whatever they had in storage is on its way home.",
                  "Clean strike. They'll be rebuilding for a while."],
            "l": ["Their defences held. Bombers are made for turrets, so bring them next time.",
                  "We hit a wall. Spy before you strike, Commander: the report shows every gun they have.",
                  "Repelled. A target that strong needs a joint strike, so ask your alliance to join."]},
 "defend": {"w": ["They came for us and went home in pieces. The defences held, Commander.",
                  "Attack repelled. Whoever that was now knows we are not an easy target.",
                  "Our worlds held. Every attacker we break leaves debris for our recyclers."],
            "l": ["They broke through and took supplies. Spend what you can before going offline: anything in storage can be plundered.",
                  "We were raided, Commander. More defences, or a Peace Shield when you need rest, will stop the next one.",
                  "They got past us. A Planetary shield on the colony, or interceptors in the silo, would have turned them back."]},
 "field": {"w": ["The field is ours. Gather what's there before someone else does.",
                 "Battle won. The outpost's crews won't contest us again soon.",
                 "Well fought, Commander. That ground is ours."],
           "l": ["We were pushed off the field. Come back with more ships.",
                 "Lost that battle. Their numbers were bigger than ours this time.",
                 "Driven back. Raise our fleet and try the field again."]},
 "trial": {"w": ["Trial cleared. The element answered us, Commander.",
                 "The Echo fell. Every trial we clear brings our mastery of that element closer.",
                 "Well fought. The rings remember a victory like that."],
           "l": ["The Echo outlasted us. A fleet with runes in the element that counters it does far better.",
                 "Not this time. The trial resets tomorrow, so build up and try again.",
                 "The Echo was stronger. Check its weakness on the Elements page before the next attempt."]},
 "boss": {"w": [],
          "l": ["That boss is beyond one fleet. Join a joint strike with your alliance next time.",
                "It shrugged us off. Bosses need everyone, Commander: rally the alliance and hit it together."]},
}
INTRO = {
 "labs": ["The Research Center. Everything we learn here makes every ship and every world better.",
          "Weapons, Shields and Armour make our fleets hit harder and last longer. Energy and the drives open new ships. One project runs at a time, so always keep the lab busy."],
 "yard": ["The Shipyard. Every hull in our fleet starts here.",
          "Each ship needs its research first; locked ones show you what's missing. A bigger Shipyard and robotics build faster, and every colony can run its own queue."],
 "planets": ["Your empire, Commander. Every world you hold, in one place.",
             "Each colony mines and builds on its own and adds a fleet slot. Tap one to manage it, or jump between them with the arrows at the top of the screen."],
 "void": ["The Void. The center of the galaxy, where the Cube waits.",
          "Everything here is stronger than anything on the Rim. Don't come here alone."],
 "layers": ["The galaxy runs in layers, Commander, from the quiet Rim to the deadly Core.",
            "Each layer inward holds stronger pirates, bigger monsters and richer worlds. Move inward when our fleet is ready, not before."],
 "mastery": ["Mastery. Every technology and ship type we perfect pays out here.",
             "Claim each mastery as it completes. Finish them all and there's a Grand Mastery waiting."],
 "find": ["The Finder. Pirates, monsters, pyramids and loot, sorted by distance.",
          "Pick targets near our level, Commander. The level is shown beside every target."],
 "tile": ["An open orbit. Nobody lives here yet.",
          "You can teleport one of our planets here, or send a Colony Ship to settle it. A teleport moves the whole world: buildings, stockpile and garrison."],
 "nexus": ["The Nexus. Whoever holds it holds the heart of the galaxy.",
           "Battles here are alliance battles. Coordinate before you send anything."],
 "pyramid": ["A pyramid. The old empires built these, and their guardians still answer.",
             "Defeat the guardians and whatever is inside is ours. Pyramids are the best source of rune shards."],
 "skin": ["Rename and reskin. Make this world your own.",
          "Name it, pick its look, and apply any planet skin you own. Some skins add a small production bonus to the world wearing them."],
 "spysend": ["Espionage. Send probes and see what they have before you strike.",
             "More probes and better Espionage research reveal more: fleets, defences, then technology. If they out-research us, our probes get caught."],
 "pirate": ["A target, Commander. Read its level and strength before you send anything.",
            "Send a probe first if you are unsure. Losing a fleet costs more than a probe ever will."],
}
NEWS = ["Commander, a few things changed while you were away.",
        "Your commander level now counts what we've built and researched, on every world. Fleets raise our ranking score instead. If your level looks lower, that's why, and nothing was taken from you.",
        "Crates, salvage pods and daily rewards now pay out in hours of our own production. Grow the mines and they grow with them.",
        "The Void Shop sells a Peace Shield now. It drops the moment we attack, spy on or fire at another commander, so use it to rest, not to hide.",
        "Teleports cost ◆200 to a chosen orbit, or ◆70 for a random jump, and shard purchases ask you to tap twice. Premium commanders can also give their hulls a trim finish now."]
FIRST = {"premium": "The Premium page. Each tier adds a planet skin, hull finishes and lasting bonuses. Pick a hull, then a finish, then a trim to make it yours.",
         "inv": "Your inventory, sorted by kind. Tap a tab to see one kind of item, or Use to put it to work right away."}

rep('function addReport(rep) { battleXP(rep); recordBattle(rep); S.reports.unshift(rep);',
    'function addReport(rep) { battleXP(rep); recordBattle(rep); try { advBattle(rep); } catch (e) {} S.reports.unshift(rep);')
rep('  S.trialD = elDay(); S.reports.unshift(rep);', '  S.trialD = elDay(); try { advBattle(rep); } catch (e) {} S.reports.unshift(rep);')
rep('function advOnce(k) {', '''/* v645 the advisor reacts to ordinary battles: once per fresh report, at most every 90 s, after the replay closes */
const ADV_BT = ''' + json.dumps(BT, ensure_ascii=False) + ''';
function advBattle(rep) { if (!rep || rep.test || !S || !G.ready) return; const T = now(); if (rep.at && T - rep.at > 5 * 60000) return; if (T - (G.advBt || 0) < 90000) return;
  const t = String(rep.title || ""); if (/^(Stress test|DEMO)/.test(t) || rep.winner === "draw") return; const win = repWin(rep), def = rep.kind === "defense" || rep.kind === "raid" || /^Hive raid|^Cube strike/.test(t);
  const c = rep.trial ? "trial" : def ? "defend" : /^Hunt:/.test(t) ? "hunt" : /Cube/.test(t) ? "cube" : /^Raid on /.test(t) ? "pirate" : /^Guardians of /.test(t) ? "pyramid" : /^(Outpost|Field) battle/.test(t) ? "field" : /^Assault on /.test(t) ? "boss" : /^Attack on /.test(t) ? "attack" : null;
  const L = c && ADV_BT[c] && ADV_BT[c][win ? "w" : "l"]; if (!L || !L.length) return; G.advBt = T; const line = L[(Math.random() * L.length) | 0];
  if (battle) G.advBtQ = line; else setTimeout(() => { try { advHolo(line, true); } catch (e) {} }, 1600); }
/* v645 a one-line welcome the first time a few screens open */
const ADV_FIRST = ''' + json.dumps(FIRST, ensure_ascii=False) + ''';
function advFirst(k) { try { if (!S || !G.ready || !ADV_FIRST[k] || tutOn()) return; S.advOnce = S.advOnce || {}; if (S.advOnce["f_" + k]) return; S.advOnce["f_" + k] = now(); dirty(); setTimeout(() => { try { advHolo(ADV_FIRST[k]); } catch (e) {} }, 1200); } catch (e) {} }
/* v645 what changed, once, for commanders who were already playing */
const ADV_V645 = ''' + json.dumps(NEWS, ensure_ascii=False) + ''';
function advNews645() { try { if (!S || !G.ready || !S.intro || tutOn() || score() < 200) return; S.advOnce = S.advOnce || {}; if (S.advOnce.v645) return; S.advOnce.v645 = now(); dirty(); say(ADV_V645.slice()); } catch (e) {} }
function advOnce(k) {''')
rep('function closeBattle() { if (battle) {', 'function closeBattle() { if (G.advBtQ) { const l = G.advBtQ; G.advBtQ = null; setTimeout(() => { try { advHolo(l, true); } catch (e) {} }, 900); } if (battle) {')
rep('function openSheet(s) {', 'function openSheet(s) { if (s && (s.type === "premium" || s.type === "inv")) advFirst(s.type);')
i = s.index('const ADV_INTRO = '); j = s.index('};\n', i) + 3
s = s[:j] + 'Object.assign(ADV_INTRO, ' + json.dumps(INTRO, ensure_ascii=False) + '); /* v645 */\n' + s[j:]
rep('Only super bosses drop them: the top damage dealers and the final blow on a world boss, and everyone who breaks the Omega Cube.',
    'Whole runes come from super bosses: the top damage dealers and the final blow on a world boss, and everyone who breaks the Omega Cube. Rune shards turn up from hunts, pyramids, raids and daily tasks, and ten shards make a rune.', 2)
# the briefing runs a few seconds after the game is ready, once
rep('function advOnce(k) {', 'setTimeout(function nw() { if (typeof G === "undefined" || !G.ready) return setTimeout(nw, 3000); setTimeout(advNews645, 6000); }, 3000);\nfunction advOnce(k) {')
rep('const GAME_V = 644', 'const GAME_V = 645')
open(p, 'w', encoding='utf-8').write(s)
