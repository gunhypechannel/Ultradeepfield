# v453 what the super boss materials are for: two Mythic flagship sets forged only from them. Celestial (Vaelthar): weapon, shield,
# reactor, artifact. Sovereign (Aexion): armour, bridge, engine, computer. Mythic slot stats like any Mythic piece, their own set
# bonuses at 2 and 4 pieces, their own names; Flagship Dock Lv.12 like all Mythic gear, the usual Mythic resources and forge time.
# The normal forge's set picker never offers them. The two sets share no slot, so a commander can wear both.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('hunt: ["Void Hunter", [[2, { boss: 4 }], [4, { boss: 4 }], [6, { boss: 4, atk: 3 }]]] };',
    'hunt: ["Void Hunter", [[2, { boss: 4 }], [4, { boss: 4 }], [6, { boss: 4, atk: 3 }]]],\n  celes: ["Celestial", [[2, { shd: 3, boss: 3 }], [4, { atk: 4, shd: 3, boss: 3 }]]], sov: ["Sovereign", [[2, { hul: 3, atk: 2 }], [4, { hul: 4, atk: 3, spd: 3 }]]] }; /* v453 the super boss sets */\n'
    'const SBG = { celes: { k: "vae", it: { weapon: ["Annihilation Lance", { vastral: 2, vwheel: 6, vscale: 8 }], shield: ["Wheel of Judgment", { vwheel: 8, vscale: 6, vcata: 2 }], reactor: ["Astral Heart", { vastral: 3, vcata: 4, vscale: 6 }], artifact: ["Eye of the Ruin", { vcata: 6, vwheel: 4, vastral: 2 }] } },\n'
    '  sov: { k: "aex", it: { armor: ["Sovereign Warplate", { aalloy: 8, atitan: 6, areact: 2 }], bridge: ["Warform Command Throne", { amatrix: 6, aalloy: 4, areact: 2 }], engine: ["Titan Thrust Array", { atitan: 8, aalloy: 6, areact: 2 }], computer: ["Aegis Logic Core", { amatrix: 8, atitan: 4, areact: 2 }] } } };')
rep("const fsItemName = it => `${FS_TIER[it.t][0]} ${(FS_NAMES[it.s] || {})[it.f] || FS_SLOT[it.s][1]}`;",
    "const fsItemName = it => it.set && SBG[it.set] && SBG[it.set].it[it.s] ? `${FS_TIER[it.t][0]} ${SBG[it.set].it[it.s][0]}` : `${FS_TIER[it.t][0]} ${(FS_NAMES[it.s] || {})[it.f] || FS_SLOT[it.s][1]}`;")
rep('<div class="segc fsf">${Object.entries(FS_SETS).map(', '<div class="segc fsf">${Object.entries(FS_SETS).filter(([k]) => !SBG[k]).map(')
rep("for (const [k, n] of Object.entries(j.mats || {})) f.mats[k] = (f.mats[k] || 0) + n; for (const r of [\"m\", \"c\", \"g\"]) S.res[r] += (j.res || {})[r] || 0;",
    "for (const [k, n] of Object.entries(j.mats || {})) f.mats[k] = (f.mats[k] || 0) + n; for (const [k, n] of Object.entries(j.sbm || {})) { S.sbMat = S.sbMat || {}; S.sbMat[k] = (S.sbMat[k] || 0) + n; } for (const r of [\"m\", \"c\", \"g\"]) S.res[r] += (j.res || {})[r] || 0;")
# forging a piece, from the boss's panel
rep("  sbTgt: d => {", """  sbForge: d => act(() => { const [set, sl] = String(d.id).split(":"), G0 = SBG[set], it = G0 && G0.it[sl]; if (!it || !fsOn()) return toast("Your flagship takes command at commander Lv.15.", "warn"); const f = fsOf(), rc = fsRecipe(sl, 6);
    if (!fsDockL()) return toast("Build the Flagship Dock first.", "warn"); if (FS_DOCK_T[6] > fsDockL()) return toast(`Mythic gear needs Flagship Dock Lv.${FS_DOCK_T[6]}.`, "warn"); if (f.q.length >= fsQMax()) return toast("The forge queue is full. Upgrade the Flagship Dock for more slots.", "warn");
    S.sbMat = S.sbMat || {}; if (!Object.entries(it[1]).every(([k, n]) => (S.sbMat[k] || 0) >= n)) return toast("Not enough materials. Hunt it again!", "warn"); if (!pay(rc.res)) return toast("Not enough resources.", "warn");
    for (const [k, n] of Object.entries(it[1])) S.sbMat[k] -= n; const T = now(), first = !f.q.length; f.q.push({ id: "fj" + (f.seq++) + "-" + T.toString(36), s: sl, t: 6, set, f: facOf(), ms: rc.ms, s0: first ? T : null, e: first ? T + rc.ms : 9e15, mats: {}, sbm: Object.assign({}, it[1]), res: rc.res });
    fsBump(); toast(`Forging the ${it[0]}: ${ftime(rc.ms)}.`, "win"); renderSheet(); }), /* v453 */
  sbTgt: d => {""")
# the forge list in the boss panel replaces "recipes are coming"
rep('<h2 class="sec">Your ${esc(D.n)} materials</h2><div class="sbmats">${mine}</div><p class="note">Forge recipes for these are coming.</p>`; }',
    '<h2 class="sec">Your ${esc(D.n)} materials</h2><div class="sbmats">${mine}</div>${sbForgeHTML(k)}`; }\n'
    'function sbForgeHTML(k) { const set = k === "vae" ? "celes" : "sov", G0 = SBG[set], B = FS_SETS[set][1], have = S.sbMat || {}, f = S.fs ? fsOf() : null, own = f ? f.inv.filter(x => x.set === set).length : 0;\n'
    '  const rows = Object.entries(G0.it).map(([sl, [n, need]]) => { const ok = Object.entries(need).every(([m, q]) => (have[m] || 0) >= q), st = fsItemStats({ s: sl, t: 6, f: facOf(), lv: 0 });\n'
    '    return `<li class="sbg"><div><b>${FS_SLOT[sl][2]} ${esc(n)}</b><small>Mythic ${esc(FS_SLOT[sl][1])} · ${Object.entries(st).map(([a, v]) => `${FS_NEG[a] ? "−" : "+"}${v}% ${esc(FS_STAT[a].toLowerCase())}`).join(", ")}</small><span>${Object.entries(need).map(([m, q]) => `${sbMatIcon(m, 16)}<em class="${(have[m] || 0) >= q ? "" : "short"}">${have[m] || 0}/${q}</em>`).join(" ")}</span></div><button class="btn ghost" data-act="sbForge" data-id="${set}:${sl}" ${ok ? "" : "disabled"}>Forge</button></li>`; }).join("");\n'
    '  return `<h2 class="sec">${esc(FS_SETS[set][0])} set · forge</h2><p class="note">Mythic flagship gear forged only from ${esc(SBW[k].n)}\'s materials, at the Flagship Dock (Lv.${FS_DOCK_T[6]}). Set bonus: ${B.map(([c, o]) => `${c} pieces ${Object.entries(o).map(([a, v]) => `+${v}% ${esc(FS_STAT[a].toLowerCase())}`).join(", ")}`).join("; ")}.${own ? ` You own ${own}.` : ""}</p><ul class="sbgl">${rows}</ul>`; }')
rep("#sbband{position:absolute;", ".sbgl{list-style:none;padding:0;margin:4px 0 10px;display:grid;gap:6px}.sbg{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:10px;background:rgba(255,255,255,.04)}.sbg>div{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.sbg small{opacity:.72;font-size:11px}.sbg span{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;font-size:12px}.sbg em{font-style:normal}.sbg em.short{color:#ff8a8a}\n#sbband{position:absolute;")
s = re.sub(r"GAME_V = 452\b", "GAME_V = 453", s)
open(P, 'w').write(s)
