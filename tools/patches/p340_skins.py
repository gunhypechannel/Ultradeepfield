p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,a[:60]; h=h.replace(a,b)
rep('"glacier.webp": 2, "glacier-map.webp": 2, "hellgate.webp": 2 };','"glacier.webp": 2, "glacier-map.webp": 2, "hellgate.webp": 2, "singular.webp": 2, "singular-map.webp": 2, "emerald.webp": 2, "emerald-map.webp": 2, "atoll.webp": 2, "atoll-map.webp": 2, "dread.webp": 2, "dread-map.webp": 2 }; /* v340: four more remastered */')
rep('emerald: ["Emerald Cube", "A blazing green crystal cube in orbit around its own shattered world."]','emerald: ["Emerald Cube", "A vast machine cube buried in a world of peaks and waterfalls, ringed in green light."]')
rep('d: "A bone-white skull world with horns and burning red eyes. Rivals will know who lives here." }','d: "A horned skull world of scorched bone and lava, its red eyes burning. Rivals will know who lives here." }')
rep('const GAME_V = 339;','const GAME_V = 340;')
open(p,"w").write(h); print("ok")
