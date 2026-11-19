# v668 the Mimic economy: Forge, reward track, the Neural Hive planet skin, the Mimic Bioweave hull finish, the Omega medal.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('const monGone = x =>', R('p668_forge.js') + 'const monGone = x =>')
# the planet skin (procedural, the same family as the deep-ocean skins: a black sea veined with cyan light)
rep('  ["countdown", "The Countdown", 2000,', '  ["mimichive", "Neural Hive", 2400, "all", .12, "#5fd8ff", "A world wrapped in black cable and lit from inside by a cyan neural core. Forged from the Mimic swarm.", "ocean", ["#010308", "#04121e", "#0a2a3e", "#123848", "#1a4a5a"], [90, 220, 255], { sea: .92, veins: 1 }], /* v668 */\n  ["countdown", "The Countdown", 2000,')
# the hull finish: forged, or from the premium track; not a premium tier
rep('  glyph: { n: "Glyph Holo", t: 16,', '  mimic: { n: "Mimic Bioweave", t: 99, col: "#1a2836", rim: "#5fd8ff", met: .8, rough: .22, k: .85, gl: 1.25, sw: "linear-gradient(135deg,#05080c,#1a2836 40%,#5fd8ff 52%,#0a121a 64%,#3a6a80)" }, /* v668 forged */\n  glyph: { n: "Glyph Holo", t: 16,')
rep('const hullOk = f => !!HULL_F[f] && (premT() >= HULL_F[f].t || !!G.owner);', 'const hullOk = f => !!HULL_F[f] && (premT() >= HULL_F[f].t || !!G.owner || (f === "mimic" && !!((S && S.hullOwn) || {}).mimic));')
# the hub: medals, the forge and the track after the swarm list
rep('  <h3>The swarm</h3><div class="mimcls">', '  ${S.medals && S.medals.omega ? `<div class="mimmedal"><span>🏆 Omega Slayer ×${S.medals.omega}</span></div>` : ""}${mimForgeHTML()}${mimTrackHTML()}\n  <h3>The swarm</h3><div class="mimcls">')
rep('  moTgt: d => {', '''  mimForge: d => { const F = MIM_FORGE.find(r => r[0] === d.k), M = mimS(); if (!F) return; if ((d.k === "px" && (S.pxOwn || {}).mimichive) || (d.k === "hull" && (S.hullOwn || {}).mimic)) return toast("You already own it.", "warn");
    if (!mimHave(F[3], M)) return toast("Not enough materials yet.", "warn"); for (const [k, n] of Object.entries(F[3])) M.m[k] -= n; mimGrant({ [d.k]: d.k === "sh" ? 25 : 1 }, "Forged"); try { SFX.build(); } catch (e) {} renderSheet(); }, /* v668 */
  mimTrack: d => { const i = +d.i, p = d.p === "1", M = mimS(), T0 = MIM_TRACK[i]; if (!T0) return; const id = (p ? "p" : "f") + i; M.tr = M.tr || {}; if (M.tr[id] || M.pts < T0[0] || (p && !mimPrem())) return; M.tr[id] = 1; mimGrant(T0[p ? 2 : 1], "Mimic reward track"); renderSheet(); },
  moTgt: d => {''')
# the Omega medal for everyone who fought in a victory
rep('M.m.osh = (M.m.osh || 0) + osh;', 'M.m.osh = (M.m.osh || 0) + osh; if (out === "win" && p) { S.medals = S.medals || {}; S.medals.omega = (S.medals.omega || 0) + 1; } /* v668 */')
rep('.arfly{', R('p668.css').strip() + '\n.arfly{')
rep('  const sw = Object.entries(HULL_F).map(', '  const sw = Object.entries(HULL_F).filter(([f]) => f !== "mimic").map(')
rep('...Object.entries(HULL_F).filter(([f]) => f !== ok)', '...Object.entries(HULL_F).filter(([f]) => f !== ok && (f !== "mimic" || hullOk(f)))')
rep('...Object.entries(HULL_F).sort((x, y) => x[1].t - y[1].t)].map(([f, F]) => { const lk', '...Object.entries(HULL_F).filter(([f]) => f !== "mimic" || hullOk(f)).sort((x, y) => x[1].t - y[1].t)].map(([f, F]) => { const lk')
rep('Object.keys(HULL_F).length', '(Object.keys(HULL_F).length - 1)')
rep('obsidian: 2, diamond: 3, glyph: 4 };', 'obsidian: 2, diamond: 3, glyph: 4, mimic: 2 }; /* v668 the Bioweave wears as dark glass on titan liveries */')
rep('emerald: "#0fe070", glyph: "#30e8ff" };', 'emerald: "#0fe070", glyph: "#30e8ff", mimic: "#0c1620" };')
rep('const GAME_V = 667;', 'const GAME_V = 668;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
