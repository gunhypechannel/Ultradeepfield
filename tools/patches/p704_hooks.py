# v704 hooks (exec'd by p704_wire.py after the module is in place)
rep(', CRC_NESTS, CRC_PATS).filter(x => !monGone(x));', ', CRC_NESTS, CRC_PATS, CRC_KRAK, CRC_BOSSES).filter(x => !monGone(x));')
# the admirals, guardians and the Crown ride the Mimic boss plumbing (MIM_BOSS, flagged crc)
rep('function alphaForce(x, T) { const st = mimSt(T || now()), B = MIM_BOSS[x.id];', 'function alphaForce(x, T) { if (MIM_BOSS[x.id].crc) return crcBossForce(x, T); /* v704 */ const st = mimSt(T || now()), B = MIM_BOSS[x.id];')
rep('const B = MIM_BOSS[x.id]; if (!B) return false;', 'const B = MIM_BOSS[x.id]; if (!B) return false; if (B.crc) return crcHid(x, T); /* v704 */')
rep('function mimBossInfo(x, T) { if (MIM_BOSS[x.id].om) return moInfo(x, T);', 'function mimBossInfo(x, T) { if (MIM_BOSS[x.id].crc) return crcBossInfo(x, T); /* v704 */ if (MIM_BOSS[x.id].om) return moInfo(x, T);')
rep('(MIM_BOSS[f.xid].om ? moResolve(f) : mimBossResolve(f))', '(MIM_BOSS[f.xid].crc ? crcBossResolve(f) : MIM_BOSS[f.xid].om ? moResolve(f) : mimBossResolve(f))')
rep('(it.om === 1 ? 4.2 : it.om === 2 ? 2.6 : it.mon === "nexus" ? 1.5 : 1.8)', '(it.crc ? it.sc : it.om === 1 ? 4.2 : it.om === 2 ? 2.6 : it.mon === "nexus" ? 1.5 : 1.8)')
# the sheet's picture: the owner's painting, or the 3D model for the wild Kraken
rep('${CRC_M[x.mon] ? `<div class="monart crcart"><img src="art/carcinid/${CRC_ART[x.mon]}.webp?v=1" alt="" loading="lazy"></div>` : monArt(MON_ARTF[x.mon] || x.mon)}',
    '${CRC_M[x.mon] ? (CRC_ART[x.mon] ? `<div class="monart crcart"><img src="art/carcinid/${CRC_ART[x.mon]}.webp?v=1" alt="" loading="lazy"></div>` : `<div class="monart crcart"><canvas data-ship="${CRC_M[x.mon]}" width="600" height="300"></canvas></div>`) : monArt(MON_ARTF[x.mon] || x.mon)}')
# the server record: claims and the Great Molting's moments
rep("(G.crcDoc = G.crcDoc || {})[d] = s.exists ? s.data() : null; CSC = {}; softRender();", "(G.crcDoc = G.crcDoc || {})[d] = s.exists ? s.data() : null; CSC = {}; try { crcClaim(); } catch (e) {} softRender();")
# the hub's buttons
rep('  crcFind: () => { const x = crcNearest(now(), "carcinid"); if (x) mimGo(x); else toast("No Breach Zone within reach right now."); },',
    '  crcFind: d => { const m = d.m || "carcinid", x = crcNearest(now(), m); if (x) mimGo(x); else toast(m === "crcpat" ? "No patrol within reach right now." : m === "wkraken" ? "No Kraken within reach right now." : "No Breach Zone within reach right now."); },\n'
    '  crcGoB: d => { const x = PB[d.id]; if (x) mimGo(x); },\n  crcCine: d => crcCine(d.k),\n'
    '  crcForge: d => { const F = CRC_FORGE.find(r => r[0] === d.k), M = crcS(); if (!F) return; if (crcOwn(d.k)) return toast("You already own it.", "warn"); if (!crcHave(F[3], M)) return toast("Not enough materials yet.", "warn");\n'
    '    for (const [k, n] of Object.entries(F[3])) M.m[k] -= n; crcGrant({ [d.k]: d.k === "sh" ? 25 : 1 }, "Forged"); try { SFX.build(); } catch (e) {} renderSheet(); },\n'
    '  crcTrack: d => { const i = +d.i, p = d.p === "1", M = crcS(), T0 = CRC_TRACK[i]; if (!T0) return; const id = (p ? "p" : "f") + i; M.tr = M.tr || {}; if (M.tr[id] || M.pts < T0[0] || (p && !mimPrem())) return; M.tr[id] = 1; crcGrant(T0[p ? 2 : 1], "Carcinid reward track"); renderSheet(); },')
rep('o = CRC_OBJ.find(x => x[0] === d.id)', 'o = crcObjs(w).find(x => x[0] === d.id)')
rep("for (const [m, v] of Object.entries(o[4])) M.m[m] = (M.m[m] || 0) + v;", "crcAddM(o[4]);")
rep("toast(`+◆${o[3]} and ${Object.entries(o[4]).map(([m, v]) => `${v} ${CRC_MAT[m][0]}`).join(\", \")}`, \"win\");", "toast(`+◆${o[3]} and ${crcMatTxt(o[4])}`, \"win\");")
rep('S.crcPrev = w ? { w, at: now() } : null; CSC = {}; dirty(); toast(w ? `Previewing week ${w} of the Tide of the Carcinid (this device only).` : "Preview off."); renderSheet(); },',
    'S.crcPrev = w ? { w, at: now() } : null; CSC = {}; dirty(); toast(w ? `Previewing ${w === 5 ? "the Great Molting" : "week " + w} of the Tide of the Carcinid (this device only).` : "Preview off."); renderSheet(); },')
# the cosmetics: a Carcinid set (index 12), the hull finish, the planet skin
rep('"Petrified Star", "Omens", "Countdown"]', '"Petrified Star", "Omens", "Countdown", "Carcinid"]')
rep('const col = VP_SEASONS[si] ? VP_SEASONS[si][1] : "#7af4ff", col2 = COS_C2[si] || "#ffffff";', 'const col = si === 12 ? "#e8b45a" : VP_SEASONS[si] ? VP_SEASONS[si][1] : "#7af4ff", col2 = si === 12 ? "#3fe8f0" : COS_C2[si] || "#ffffff"; /* v704 the Carcinid set */')
rep('cache: "art/season/cache.webp"', 'banner12: "art/carcinid/cos-banner.webp", frame12: "art/carcinid/frame.webp", cache: "art/season/cache.webp"')
rep('src = d => d.set ? `Own every ${COS_SEA[d.si]} season cosmetic` : `Void Pass', 'src = d => d.si === 12 ? "Tide of the Carcinid · the Abyssal Forge and the reward track" : d.set ? `Own every ${COS_SEA[d.si]} season cosmetic` : `Void Pass')
rep('  mimic: { n: "Mimic Bioweave",', '  carcinid: { n: "Carcinid Chitin", t: 99, col: "#1a1226", rim: "#e8b45a", met: .7, rough: .26, k: .9, gl: 1.2, sw: "linear-gradient(135deg,#0a0610,#2a1a3a 40%,#e8b45a 52%,#140a1e 64%,#3fe8f0)" }, /* v704 forged */\n  mimic: { n: "Mimic Bioweave",')
rep('(f === "mimic" && !!((S && S.hullOwn) || {}).mimic));', '(f === "mimic" && !!((S && S.hullOwn) || {}).mimic) || (f === "carcinid" && !!((S && S.hullOwn) || {}).carcinid));')
rep('  ["mimichive", "Neural Hive",', '  ["abyssreef", "Abyssal Reef", 2400, "all", .12, "#e8b45a", "A world of black chitin plates and violet coral, lit by cyan tide-water. Forged from the Carcinid tide.", "ocean", ["#06030c", "#1a0a2a", "#3a1a4a", "#0a3a44", "#1a5a6a"], [63, 232, 240], { sea: .85, veins: 1 }], /* v704 */\n  ["mimichive", "Neural Hive",')
# the hub's new pieces
rep('.crcart{', '''.crcbosses{display:flex;flex-direction:column;gap:6px;flex:none}.crcboss{display:flex;gap:9px;align-items:center;padding:6px;border-radius:10px;border:1px solid rgba(232,180,90,.2);background:rgba(18,10,30,.55)}
.crcboss img{width:64px;height:64px;flex:none;border-radius:8px;object-fit:cover;object-position:50% 30%}.crcboss>div{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.crcboss small{font-size:11px;color:#b9a9c9}.crcboss.dead{opacity:.5}.crcboss.off{opacity:.65}
.crcmolt{display:flex;gap:10px;align-items:center;flex:none;margin:8px 0;padding:8px;border-radius:12px;border:1px solid #e8b45a;background:linear-gradient(135deg,rgba(40,24,6,.85),rgba(6,30,34,.85));box-shadow:0 0 18px rgba(232,180,90,.25)}
.crcmolt img{width:86px;height:86px;flex:none;border-radius:9px;object-fit:cover}.crcmolt>div{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}.crcmolt b{font:700 14px/1.15 var(--f-display);color:#ffd07a}.crcmolt span{font-size:12px;color:#c9e9ea}
.crcph{display:flex;gap:4px}.crcph i{font-style:normal;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:11px;border:1px solid rgba(232,180,90,.4);color:#c9b48a}.crcph i.on{background:#e8b45a;color:#1a1006;font-weight:700}.crcph i.done{background:rgba(63,232,240,.25);color:#7ff8e4;border-color:#3fe8f0}
.crctac{display:flex;gap:9px;align-items:center;margin-top:7px}.crctac img{width:40px;height:40px;flex:none;border-radius:8px}.crctac>div{display:flex;flex-direction:column;min-width:0}.crctac small{font-size:12px;color:#c9bdd6;line-height:1.35}
.crcbi{display:flex;flex-direction:column;gap:4px;margin:6px 0;flex:none}.crcbi small{font-size:12px;color:#b9a9c9}.crcbi img{display:none}
.crcmi.s{width:16px;height:16px;margin:0 2px -3px 0;border-radius:3px}.crcfr{border-color:rgba(232,180,90,.25)}
.crcart{''')
# a Carcinid boss is drawn at the front of its line, at full size (it was placed by a hash, often at the back and small)
rep('if (!b.z) b.z = Q.map((q, i) => q.k === "worldbreaker" ? .98 :', 'if (!b.z) b.z = Q.map((q, i) => q.k === "worldbreaker" || (CRC_U[q.k] && bHero(q.k)) ? .98 :')
