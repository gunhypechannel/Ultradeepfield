# v380: (1) worlds no longer vanish up close: the "which worlds are near and on screen" sweep treated every world as if it sat on the
# orbital plane, but worlds orbit on tilted paths (up to 7% of their orbit radius above or below it), so a world high above the plane
# failed the on-screen test as the camera closed in (most visible with the Finder on and in cinematic view). Fields and hideouts had the
# same flat distance. (2) Whatever the camera is filming or following is always drawn, whatever the Finder is filtering.
# (3) Cinematic view for every hideout and every resource field / Void Shard mine, not just bosses, monsters and stations.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
# (1) planets
rep('''    const dc = Math.hypot(x - cp.x, cp.y, z - cp.z), mine = p.owner === G.me || p.id === G.sel;
    if (mine || (rad / dc * pxK > 1.6 && (FR.s.center.set(x, 0, z),''', '''    const py = P3(p, T, PQS).y, dc = Math.hypot(x - cp.x, py - cp.y, z - cp.z), mine = p.owner === G.me || p.id === G.sel; /* v380: its real height on its tilted orbit */
    if (mine || (rad / dc * pxK > 1.6 && (FR.s.center.set(x, py, z),''')
rep('''if (G.sel && G.byId[G.sel] && !P.near.includes(G.sel)) P.near.push(G.sel); } else P.cur = e;''',
    '''if (G.sel && G.byId[G.sel] && !P.near.includes(G.sel)) P.near.push(G.sel); for (const f of [W.cam && W.cam.cineObj && W.cam.cineObj.id, W.cam && W.cam.follow]) if (f && G.byId[f] && !P.near.includes(f)) P.near.push(f); /* v380: what the camera films or follows is always drawn */ } else P.cur = e;''')
rep('function P3(p, T, out) {', 'const PQS = {}; // v380 scratch for the sweeps\nfunction P3(p, T, out) {')
# fields, hideouts, stations: their real height too, and the filmed or selected one is always drawn
rep('''    if (nf) { const dc = Math.hypot(x - cp.x, cp.y, z - cp.z), hl =''', '''    if (nf) { const dc = Math.hypot(x - cp.x, P3(it, T, PQS).y - cp.y, z - cp.z), hl =''')
rep('''    for (const c of G.clashes || []) if (c.loc && PB[c.loc.id]) M.near.add(c.loc.id); } else M.cur = e;''',
    '''    for (const c of G.clashes || []) if (c.loc && PB[c.loc.id]) M.near.add(c.loc.id);
    for (const f of [W.cam && W.cam.cineObj && W.cam.cineObj.id, G.selNode]) if (f && (PB[f] || YB[f] || (f[0] === "r" && NB[f]))) M.near.add(f); /* v380 */ } else M.cur = e;''')
# (3) cinematic for every hideout and field
rep('${x.mon || x.boss ? cineBtn(x.id) : ""}', '${cineBtn(x.id)}')
rep('''  return head + info + body;
}''', '''  return head + info + cineBtn(n.id) + body;
}''')
cob = '(id[0] === "r" ? NB[id] : null)'
rep('function cineObjStart(id, n) { const it = PB[id] || YB[id] || G.byId[id]; if (!it) return;', 'function cineObjStart(id, n) { const it = PB[id] || YB[id] || G.byId[id] || ' + cob + '; if (!it) return;')
rep('function cineObjPos(W, T) { const id = W.cam.cineObj.id, it = PB[id] || YB[id] || G.byId[id]; if (!it) return null;', 'function cineObjPos(W, T) { const id = W.cam.cineObj.id, it = PB[id] || YB[id] || G.byId[id] || ' + cob + '; if (!it) return null;')
rep('const o = (id[0] === "y" ? W.pyramids : W.pirates) && (id[0] === "y" ? W.pyramids : W.pirates).get(id);', 'const M3 = id[0] === "y" ? W.pyramids : id[0] === "r" ? W.nodes : W.pirates, o = M3 && M3.get(id);')
rep('o = (id[0] === "y" ? W.pyramids : W.pirates).get(id); if (o && o.grp.visible)', 'o = (id[0] === "y" ? W.pyramids : id[0] === "r" ? W.nodes : W.pirates).get(id); if (o && o.grp.visible)')
rep('''if (c.cineObj) { const it = PB[c.cineObj.id] || YB[c.cineObj.id]; if (it) w.textContent = `${it.mon ? MON[it.mon].ic + " " + MON[it.mon].n : it.boss ? "■ Assimilation Cube" : "▲ Pyramid station"} · ${it.name} · Lv.${it.lvl}`; return; }''',
    '''if (c.cineObj) { const id = c.cineObj.id, it = PB[id] || YB[id] || (id[0] === "r" ? NB[id] : null); if (it) w.textContent = `${it.res ? (it.res === "s" ? "◆ Void Shard mine" : RES_N[it.res] + " field") : it.mon ? MON[it.mon].ic + " " + MON[it.mon].n : it.boss ? "■ Assimilation Cube" : id[0] === "y" ? "▲ Pyramid station" : "☠ Pirate hideout"} · ${it.name} · Lv.${it.lvl}`; else if (G.byId[id]) w.textContent = G.byId[id].name; return; }''')
open(p, "w").write(t)
# the filmed / followed / selected world is drawn from the very next frame, not after the next full sweep
t = open(p).read()
def rep2(a, b):
    global t; assert t.count(a) == 1, a[:80]; t = t.replace(a, b)
rep2('  const near = P.near || [], counts = new Map(), info = new Map(), cpos = W.camera.position;',
     '  let near = P.near || []; { const fz = [W.cam && W.cam.cineObj && W.cam.cineObj.id, W.cam && W.cam.follow, G.sel].filter(f => f && G.byId[f] && !near.includes(f)); if (fz.length) near = near.concat(fz); }\n  const counts = new Map(), info = new Map(), cpos = W.camera.position;')
open(p, "w").write(t)
t = open(p).read()
rep2('    for (const id of M.near) { const isN = id[0] === "r", isY = id[0] === "y",',
     '    for (const f of [W.cam && W.cam.cineObj && W.cam.cineObj.id, G.selNode]) if (f && (PB[f] || YB[f] || (f[0] === "r" && NB[f]))) M.near.add(f); /* v380 at once, not after the sweep */\n    for (const id of M.near) { const isN = id[0] === "r", isY = id[0] === "y",')
open(p, "w").write(t)
