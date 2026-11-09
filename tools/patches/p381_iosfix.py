# v381: iPhone stability, second pass, from the v379 reports.
#  - v379's "release the world you are not looking at after 30 s" made every switch back rebuild it: 2-3 s freezes on base and
#    galaxy, and the one crash after v379 came right after such a rebuild. Worlds stay built again; in the background only the
#    portrait studio is released (its portraits are kept, nothing to rebuild).
#  - The real memory hog on iPhone was ship model textures: 18 ships x ~7 MB (1024 px colour + 512 px normal/roughness + a glow map),
#    uploaded again into every 3D view that shows them. On iOS ships now load at 512 / 256 px (the glow map stays 512): about a quarter.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
rep('''if (MEM_DIET) { setInterval(() => { const T = performance.now(); if (view === "galaxy") G.galAt = T; if (view === "base") G.colAt = T;
    if (G3 && view !== "galaxy" && T - (G.galAt || 0) > 30000) worldDrop("gal", "away 30 s"); if (C3 && view !== "base" && T - (G.colAt || 0) > 30000) worldDrop("col", "away 30 s"); }, 4000);
  document.addEventListener("visibilitychange", () => { if (document.hidden) { worldDrop("gal", "background"); worldDrop("col", "background"); worldDrop("stu", "background"); } }); }''',
    '''if (MEM_DIET) document.addEventListener("visibilitychange", () => { if (document.hidden) worldDrop("stu", "background"); }); /* v381: worlds stay built (rebuilding them froze and crashed); only the studio goes */''')
rep('if (MEM_DIET) { worldDrop("gal", "battle"); worldDrop("col", "battle"); } gpuNap(true);', 'gpuNap(true);')
rep('const s = g.scene, big = MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048, aux = MOBILE ? 512 : 1024,',
    'const shipIOS = IOS && GLB_SHIPS.has(k), s = g.scene, big = shipIOS ? 512 : MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048, aux = shipIOS ? 256 : MOBILE ? 512 : 1024, /* v381: iPhone ships at a quarter */')
open(p, "w").write(t)
