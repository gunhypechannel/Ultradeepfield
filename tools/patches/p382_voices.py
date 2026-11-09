# v382: every Advisor line in the Academy and its moments can be voiced. Lines built from live values (a planet name, a count) can
# never match a recorded clip, so they get a fixed spoken line (the card still shows the details); celebrations that spoke their
# caption get recorded.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
rep('''S.say.push(`A new fog season has begun (${fogSeason(T).name}). The charts have gone dark: only what our worlds and fleets can see is mapped. Send fleets and probes out to chart the galaxy again.`); flushSay(); }''',
    '''S.say.push("A new fog season has begun, Commander. The charts have gone dark: only what our worlds and fleets can see is mapped. Send fleets and probes out to chart the galaxy again."); toast(`Fog season: ${fogSeason(T).name}`); flushSay(); }''')
rep('''S.say.push(`Fleet Command has registered us in the shared galaxy. Our homeworld is ${S.homeName}.`, `Up to ${MAX_PLAYERS} commanders orbit the Void. Any colony can change hands, so guard yours.`);''',
    '''S.say.push("Fleet Command has registered us in the shared galaxy, Commander.", "Up to ten thousand commanders orbit the Void. Any colony can change hands, so guard yours.");''')
rep('''s: `Our flag flies over ${p.name}. The empire now spans two worlds, and the first one we took back from the Hive.`, go: "Onward" });''',
    '''s: `Our flag flies over ${p.name}. The empire now spans two worlds, and the first one we took back from the Hive.`, say: "Commander, our flag flies over a second world! The empire now spans two worlds, and the first one we took back from the Hive.", go: "Onward" });''')
rep('''Fleet Command sent supplies to get you moving again.`, rw:''',
    '''Fleet Command sent supplies to get you moving again.`, say: acadOn() ? "Welcome back, Commander! Your Academy is right where you left it, and Fleet Command sent supplies to get you moving again." : "Welcome back, Commander! Your missions are right where you left them, and Fleet Command sent supplies to get you moving again.", rw:''')
open(p, "w").write(t)
