# v401: the Elemental Convergence. Five Elementals from the owner's concept art (Glacius ice, Ignis fire, Solara light, Voltaris storm,
# Verdanth nature) and their fusion, the Pentarch. A 48-hour live event on the Wednesday slot, alternating weeks with the titans:
#   hours 0-24  the five tear into the galaxy at five points, staining the worlds round them with their element;
#   hour 24     the survivors fly to the black hole at the centre and fuse into the Pentarch (each one slain first is missing from it,
#               and it is that much weaker);
#   hours 24-48 defeat the Pentarch above the Void.
# Own event on the Events page (Elemental Convergence), portraits and banner from the art, Advisor lines, an owner preview.
import json, sys
p = "docs/index.html"; t = open(p).read(); ART = json.load(open(sys.argv[1]))
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

# ---------- the bosses ----------
rep("""const WB_ATK = { ovl:""", """/* v401 the Elemental Convergence (g 3): five Elementals, then their fusion, the Pentarch */
Object.assign(WB, {
  eic: { k: "wbEic", n: "Glacius", ic: "❄", col: "#6ac4ff", el: "ice", hp: 180000, atk: 130000, m3: "elemental", sc: 1.3, bounty: { m: 52000, c: 46000, g: 20000 }, sh: 4, kill: 16, where: "Elemental · Ice", g: 3, cam: 150,
    d: "The ice Elemental: a silver-blue totem of liquid metal between two great crescents, freezing every world around it." },
  efi: { k: "wbEfi", n: "Ignis", ic: "✹", col: "#ff7a2a", el: "fire", hp: 180000, atk: 140000, m3: "elemental", sc: 1.3, bounty: { m: 56000, c: 40000, g: 22000 }, sh: 4, kill: 16, where: "Elemental · Fire", g: 3, cam: 150,
    d: "The fire Elemental: a horned crown over a fanged bowl of horns, pouring a river of lava and scorching every world around it." },
  eli: { k: "wbEli", n: "Solara", ic: "✸", col: "#ffd050", el: "light", hp: 170000, atk: 135000, m3: "elemental", sc: 1.3, bounty: { m: 50000, c: 44000, g: 24000 }, sh: 4, kill: 16, where: "Elemental · Light", g: 3, cam: 150,
    d: "The light Elemental: a golden compass of diamonds and claws in a pillar of light, gilding every world around it." },
  est: { k: "wbEst", n: "Voltaris", ic: "ϟ", col: "#b868ff", el: "storm", hp: 175000, atk: 145000, m3: "elemental", sc: 1.3, bounty: { m: 50000, c: 42000, g: 26000 }, sh: 4, kill: 16, where: "Elemental · Storm", g: 3, cam: 150,
    d: "The storm Elemental: stacked violet crescents and storm wings round a living vortex, lightning arcing to every world around it." },
  ena: { k: "wbEna", n: "Verdanth", ic: "❦", col: "#80ff34", el: "nature", hp: 185000, atk: 125000, m3: "elemental", sc: 1.3, bounty: { m: 54000, c: 42000, g: 22000 }, sh: 4, kill: 16, where: "Elemental · Nature", g: 3, cam: 150,
    d: "The nature Elemental: a star of thorn blades round a green eye, overgrowing every world around it." },
  epx: { k: "wbEpx", n: "The Pentarch", ic: "✪", col: "#e2d4ff", hp: 600000, atk: 420000, m3: "pentarch", sc: 1.15, bounty: { m: 130000, c: 96000, g: 48000 }, sh: 8, kill: 40, where: "Above the Void", g: 3, cam: 300,
    d: "The Elementals fused into one, tearing at the black hole at the centre of the galaxy. Every Elemental slain before the fusion is missing from it, and it is that much weaker." } });
const WB_EL = ["eic", "efi", "eli", "est", "ena"];
const WB_ATK = { eic: ["nova", "lance", "zero"], efi: ["flare", "rain", "inferno"], eli: ["lance", "halo", "judgement"], est: ["chain", "ion", "clap"], ena: ["thorn", "spore", "growth"], epx: ["converge", "storm", "cataclysm"], ovl:""")
rep("""for (const [k, u] of [["wbOvl", WB.ovl], ["wbDev", WB.dev], ["wbWar", WB.war], ["wbCon", WB.c0], ["wbBrd", WB.brd], ["wbTyr", WB.tyr], ["wbWym", WB.wym], ["wbCol", WB.col]])""",
    """for (const [k, u] of [["wbOvl", WB.ovl], ["wbDev", WB.dev], ["wbWar", WB.war], ["wbCon", WB.c0], ["wbBrd", WB.brd], ["wbTyr", WB.tyr], ["wbWym", WB.wym], ["wbCol", WB.col], ["wbEic", WB.eic], ["wbEfi", WB.efi], ["wbEli", WB.eli], ["wbEst", WB.est], ["wbEna", WB.ena], ["wbEpx", WB.epx]])""")
# Wednesday cycle for groups 2 and 3; group membership
rep("wbG2 = k => !!(WB[k] && WB[k].g === 2),", "wbG2 = k => !!(WB[k] && WB[k].g >= 2), wbG3 = k => !!(WB[k] && WB[k].g === 3),")
rep("""const wbKeys = g => Object.keys(WB).filter(k => (g === 2) === wbG2(k)), wbMain = g => g === 2 ? ["brd", "tyr", "wym", "col"] : ["ovl", "dev", "war"];""",
    """const wbKeys = g => Object.keys(WB).filter(k => (WB[k].g || 1) === g), wbMain = g => g === 3 ? ["eic", "efi", "eli", "est", "ena", "epx"] : g === 2 ? ["brd", "tyr", "wym", "col"] : ["ovl", "dev", "war"];""")
# windows: titans on even Wednesday weeks, the Convergence on odd ones (Elementals the first 24 h, the Pentarch the next 24 h)
rep("""const WB_LIVE = 48 * 3600e3, wbOn = (k, T = now()) => T - wbStartOf(k, T) < WB_LIVE, wbUp = (k, T = now()) => wbOn(k, T) && wbAlive(k, T), wbLiveEnd = (k, T = now()) => wbStartOf(k, T) + WB_LIVE, wbNext = (k, T = now()) => wbOn(k, T) ? wbLiveEnd(k, T) : wbEndOf(k, wbCycOf(k, T)); // v392: 48-hour events""",
"""const WB_LIVE = 48 * 3600e3, WB_FUSE = 24 * 3600e3;
/* v401: a boss's window in a cycle (null when that week isn't its week). The owner preview (G.elePrev 1 or 2) shows the Convergence now. */
function wbWin(k, c) { const D = WB[k]; if (!D) return null; const g = D.g || 1;
  if (g === 1) { const s = WB_BASE + c * WEEK; return [s, s + WB_LIVE]; }
  const s = WB2_BASE + c * WEEK, odd = ((c % 2) + 2) % 2 === 1; if (g === 2) return odd ? null : [s, s + WB_LIVE];
  if (!odd) return null; return k === "epx" ? [s + WB_FUSE, s + WB_LIVE] : [s, s + WB_FUSE]; }
const wbPrev = k => G.elePrev && WB[k] && WB[k].g >= 2 ? (wbG3(k) ? (k === "epx" ? G.elePrev === 2 : G.elePrev === 1) : false) : null;
const wbOn = (k, T = now()) => { const pv = wbPrev(k); if (pv !== null) return pv; const w = wbWin(k, wbCycOf(k, T)); return !!w && T >= w[0] && T < w[1]; };
const wbUp = (k, T = now()) => wbOn(k, T) && wbAlive(k, T);
const wbLiveEnd = (k, T = now()) => { const w = wbWin(k, wbCycOf(k, T)); return w ? w[1] : T; };
const wbNext = (k, T = now()) => { const c = wbCycOf(k, T); for (let i = 0; i < 4; i++) { const w = wbWin(k, c + i); if (w && T < w[1]) return T >= w[0] ? w[1] : w[0]; } return T + WEEK; }; // end of this hunt, or the start of its next
const wbGroupOn = (g, T = now()) => wbMain(g).some(k => wbOn(k, T)), wbGroupEnd = (g, T = now()) => Math.max(...wbMain(g).filter(k => wbOn(k, T)).map(k => wbLiveEnd(k, T)), T), wbGroupNext = (g, T = now()) => Math.min(...wbMain(g).map(k => wbNext(k, T)));
const wbPentAlive = T => WB_EL.filter(k => (wbState(T).hp[k] | 0) > 0).map(k => WB[k].el); // the Elementals that live on in the Pentarch
const wbFuseK = T => { if (G.elePrev === 2) return clamp(((performance.now() - (G.elePrevAt || 0)) / 15000), 0, 1); const w = wbWin("epx", wbCyc2(T)); return w ? clamp((T - w[0]) / (20 * 60e3), 0, 1) : 1; }; // the fusion: 20 minutes""")
# fights: the Pentarch is as strong as the Elementals still in it; the preview can't be fought
rep("""  if (key === "wym") return wymOpen(at) ? 1 : 1.6;""", """  if (key === "wym") return wymOpen(at) ? 1 : 1.6;
  if (key === "epx") return .25 + .15 * WB_EL.filter(k => (st.hp[k] | 0) > 0).length;""")
rep("""if (!wbOn(key)) return toast(`The ${D.n} is away until the next hunt.`, "warn");""", """if (G.elePrev && wbG3(key)) return toast("This is the owner preview. The Convergence can be fought from its first Wednesday.", "warn"); if (!wbOn(key)) return toast(`The ${D.n} is away until the next hunt.`, "warn");""")
rep("""{ const mk = { dev: "bio", war: "void", brd: "bio", tyr: "circuit", wym: "void", col: "crystal" }[key]""", """{ const mk = { dev: "bio", war: "void", brd: "bio", tyr: "circuit", wym: "void", col: "crystal", eic: "crystal", efi: "alloy", eli: "circuit", est: "void", ena: "bio", epx: "cube" }[key]""")
rep("""  if (key === "col") return s > 1 ? `Shattered · fragments shield it ×${s}` : "Whole · shatters below 50% hull";""", """  if (key === "col") return s > 1 ? `Shattered · fragments shield it ×${s}` : "Whole · shatters below 50% hull";
  if (WB_EL.includes(key)) return `Fuses into the Pentarch in ${ftime(wbLiveEnd(key, T) - T)} · slay it first and the Pentarch is weaker`;
  if (key === "epx") { const n = WB_EL.filter(k => (st.hp[k] | 0) > 0).length; return `${n} of 5 Elementals fused in · ${Math.round(s * 100)}% strength`; }""")
rep("shield = key === \"ovl\" ? `<dt>Shield</dt>", "shield = WB_EL.includes(key) || key === \"epx\" ? (hp && wbOn(key, T) ? `<dt>${key === \"epx\" ? \"Fusion\" : \"Convergence\"}</dt><dd>${wbTwist(key, T)}</dd>` : \"\") : key === \"ovl\" ? `<dt>Shield</dt>")
rep("""<dd>${wbOn(key, T) ? ftime(wbLiveEnd(key, T) - T) : `${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC`} · hunts last 48 h</dd></dl>""",
    """<dd>${wbOn(key, T) ? ftime(wbLiveEnd(key, T) - T) : wbG3(key) ? `in ${ftime(wbNext(key, T) - T)}` : `${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC`} · ${wbG3(key) ? "the Convergence: every other Wednesday" : "hunts last 48 h"}</dd></dl>""")
# placement: the Elementals on a pentagon in the Outer Reach, the Pentarch above the Void
rep("""    if (key === "brd") { const L = LAYERS[1],""", """    if (WB_EL.includes(key)) { const L = LAYERS[2], r = (L.r0 + L.r1) / 2, i = WB_EL.indexOf(key), a = (hash("conv" + c2) % 6283) / 1000 + i * TAU / 5 + TAU * T / period(r); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 34 + 4 * Math.sin(T / 7e5 + i); return o; }
    if (key === "epx") { o.x = 0; o.z = 0; o.y = 70 + 3 * Math.sin(T / 9e5); return o; }
    if (key === "brd") { const L = LAYERS[1],""")
rep("""const WB_CLR = { wym: 30, ovl: 50, war: 22, col: 26, brd: 24, dev: 32, tyr: 38 }, WB_CUBE_R = 34, WB_SEP_ORDER = ["wym", "ovl", "war", "col", "brd", "dev", "tyr"];""",
    """const WB_CLR = { wym: 30, epx: 70, ovl: 50, war: 22, col: 26, brd: 24, dev: 32, tyr: 38, eic: 48, efi: 48, eli: 48, est: 48, ena: 48 }, WB_CUBE_R = 34, WB_SEP_ORDER = ["wym", "epx", "ovl", "war", "col", "brd", "dev", "tyr", "eic", "efi", "eli", "est", "ena"];""")
rep("""for (const k of WB_SEP_ORDER) { if (!wbOn(k, T)) continue; const q = wbPosRaw(k, T, {}); let y = q.y;
    if (k !== "wym")""", """for (const k of WB_SEP_ORDER) { if (!wbOn(k, T)) continue; const q = wbPosRaw(k, T, {}); let y = q.y;
    if (k !== "wym" && k !== "epx")""")
# the worlds round each Elemental take its colour; the Pentarch scorches the Core; the Matriarch's green as before
rep("""function wbInfect(T) { if (WB_INF && Math.abs(T - WB_INF.T) < 2000) return WB_INF.v; let v = null; try { if (wbUp("brd", T)) { const q = wbPos("brd", T, {}), R = 45 + 20 * Math.min(3, Math.floor((T - wbStartOf("brd", T)) / (12 * 3600e3))); v = { x: q.x, z: q.z, r2: R * R, R }; if (!INFC) INFC = new TH.Color(.6, 1.75, .3); } } catch (e) {} WB_INF = { T, v }; return v; }""",
"""function wbInfect(T) { if (WB_INF && Math.abs(T - WB_INF.T) < 2000) return WB_INF.v; let v = null; try { if (wbUp("brd", T)) { const q = wbPos("brd", T, {}), R = 45 + 20 * Math.min(3, Math.floor((T - wbStartOf("brd", T)) / (12 * 3600e3))); v = { x: q.x, z: q.z, r2: R * R, R }; if (!INFC) INFC = new TH.Color(.6, 1.75, .3); } } catch (e) {} WB_INF = { T, v }; return v; }
/* v401: every stained zone on the map: the Matriarch's infection, each Elemental's element, and the Pentarch tearing at the Core */
const WB_STAIN = { eic: [.55, 1.1, 1.9], efi: [1.9, .55, .25], eli: [1.8, 1.45, .45], est: [1.15, .6, 1.9], ena: [.6, 1.75, .35], epx: [1.35, 1.1, 1.9] }; let WB_ZONES = null;
function wbZones(T) { if (WB_ZONES && Math.abs(T - WB_ZONES.T) < 2000) return WB_ZONES.z; const z = []; try { const I = wbInfect(T); if (I) z.push({ x: I.x, z: I.z, r2: I.r2, c: INFC });
    for (const k of [...WB_EL, "epx"]) if (wbUp(k, T)) { const q = wbPos(k, T, {}), R = k === "epx" ? 95 : 70; z.push({ x: q.x, z: q.z, r2: R * R, c: new TH.Color(...WB_STAIN[k]) }); } } catch (e) {} WB_ZONES = { T, z }; return z; }
const zoneCol = (Z, q) => { for (const s of Z) if ((q.x - s.x) ** 2 + (q.z - s.z) ** 2 < s.r2) return s.c; return null; };""")
rep("  const INF = wbInfect(T);", "  const ZN = wbZones(T);")
rep("e.mesh.setColorAt(i, INF && !pxOf(p) && (q.x - INF.x) ** 2 + (q.z - INF.z) ** 2 < INF.r2 ? INFC : fg ? FOGC :", "e.mesh.setColorAt(i, (ZN.length && !pxOf(p) && zoneCol(ZN, q)) || (fg ? FOGC :")
rep("p.tn && !pxOf(p) ? tintC(p.tn) : WHITEC); /* v69: a colour tint never dim", "p.tn && !pxOf(p) ? tintC(p.tn) : WHITEC)); /* v69: a colour tint never dim")
# the models: an Elemental takes its element; the Pentarch the survivors; the map fusion
rep("const b = BOSS3D.prep(BOSS3D[D.m3](), wbEnv(W.renderer));", "const b = BOSS3D.prep(BOSS3D[D.m3](D.el || (key === \"epx\" ? wbPentAlive(T) : undefined)), wbEnv(W.renderer));")
rep("    if (M.sweep && !(G.wbScan && G.wbScan.key === key)) M.sweep.visible = false; M.b.tick(t); }", "    if (key === \"epx\") M.b.form = wbFuseK(T); /* the fusion: the aspects fly in */ if (M.sweep && !(G.wbScan && G.wbScan.key === key)) M.sweep.visible = false; M.b.tick(t); }")
rep("WBR.b = BOSS3D.prep(BOSS3D[m3](), wbEnv(WBR.r));", "WBR.b = BOSS3D.prep(BOSS3D[m3](WB[key].el || (key === \"epx\" ? wbPentAlive(now()) : undefined)), wbEnv(WBR.r));")
rep("""const WB_FRONT = { overlord: 0,""", """const WB_FRONT = { elemental: 0, pentarch: 0, overlord: 0,""")
rep("""const WB_VIEW = { matriarch:""", """const WB_VIEW = { elemental: [-.2, [-8, 4, 62], [0, 0, 0]], pentarch: [0, [-10, 6, 120], [0, 0, 0]], matriarch:""")
rep("""const WB_YR = { overlord: [-8, 7],""", """const WB_YR = { elemental: [-15, 15], pentarch: [-28, 28], overlord: [-8, 7],""")
rep("""const WB_ATT = {""", """const WB_ATT = {"eic": [["nova", "Frost Nova", "Its crescents clench, then burst out in a ring of frost."], ["lance", "Ice Lance", "Its orbs swing out and fire lances of ice."], ["zero", "Absolute Zero", "Its rings spin up and a freezing shockwave rolls out."]], "efi": [["flare", "Solar Flare", "Its horns flare open in a wave of fire."], ["rain", "Magma Rain", "The lava fall surges and molten rock rains down."], ["inferno", "Inferno", "Its core blazes and a ring of fire explodes outward."]], "eli": [["lance", "Radiant Lance", "Its diamonds align and a lance of light fires."], ["halo", "Halo Burst", "Its halo rings spin out in blinding light."], ["judgement", "Judgement", "The pillar of light surges and the sky detonates."]], "est": [["chain", "Chain Lightning", "Lightning leaps from ship to ship."], ["ion", "Ion Storm", "The vortex spins up and strips our shields."], ["clap", "Thunderclap", "Its crescents slam together in a thunderous shockwave."]], "ena": [["thorn", "Thorn Volley", "Its blades flare out and fire thorns."], ["spore", "Spore Bloom", "A choking cloud of spores bursts out."], ["growth", "Overgrowth", "The green beam surges and its tendrils lash out."]], "epx": [["converge", "Convergence Beam", "Every aspect fires into the heart, and the heart fires."], ["storm", "Elemental Storm", "The aspects whirl round the heart in a storm of every element."], ["cataclysm", "Cataclysm", "The heart detonates in a shockwave of every element."]], """)
rep("""WB_SCAN_SAY = {""", """WB_SCAN_SAY = {"eic": "Scanning Glacius. Beware its frost nova, the ice lances from its orbs, and absolute zero when its rings spin up.", "efi": "Scanning Ignis. Beware the solar flare from its horns, the magma rain, and the inferno when its core blazes.", "eli": "Scanning Solara. Beware the radiant lance, the halo burst, and judgement when its pillar of light surges.", "est": "Scanning Voltaris. Beware chain lightning, the ion storm that strips our shields, and the thunderclap of its crescents.", "ena": "Scanning Verdanth. Beware the thorn volley, the spore bloom, and the overgrowth when its beam surges.", "epx": "Scanning the Pentarch. Beware the convergence beam, the elemental storm, and the cataclysm when its heart detonates. Every Elemental we slew is missing from it.", """)
rep("""const WB_INTEL = {""", """const WB_INTEL = { eic: ["Elemental · ice", "Its core, when its crescents open to strike.", "EXTREME"], efi: ["Elemental · fire", "Its diamond heart, exposed as its horns flare.", "EXTREME"], eli: ["Elemental · light", "The central ring, between its diamonds.", "EXTREME"], est: ["Elemental · storm", "The vortex eye, while the storm spins up.", "EXTREME"], ena: ["Elemental · nature", "The green eye at the heart of its thorns.", "EXTREME"], epx: ["Fused Elementals · above the Void", "Slay Elementals before the fusion: each one is missing from it.", "CATASTROPHIC"], """)

# ---------- the event ----------
rep("""const SB_W = k => k === "ovl" || k === "dev" || wbG2(k) ? 3 : k === "war" ? 2 : 1;""", """const SB_W = k => k === "epx" ? 6 : k === "ovl" || k === "dev" || wbG2(k) ? 3 : k === "war" ? 2 : 1;""")
rep("""2: { ev: "tboss", n: "Titan Hunt", day: "Wednesday", sk: "sb2", art: "wym", artN: "The Event Horizon Wyrm" } };""", """2: { ev: "tboss", n: "Titan Hunt", day: "Wednesday", sk: "sb2", art: "wym", artN: "The Event Horizon Wyrm" }, 3: { ev: "eboss", n: "Elemental Convergence", day: "other Wednesday", sk: "sb3", art: "epx", artN: "The Elementals" } };""")
rep("""function sbMine(T = now(), g = 1) { const st = wbState(T), E = SB_G[g], cy = g === 2 ? st.cyc2 : st.cyc;""", """function sbMine(T = now(), g = 1) { const st = wbState(T), E = SB_G[g], cy = g >= 2 ? st.cyc2 : st.cyc;""")
rep("""function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), main = wbMain(g), live = wbOn(main[0], T), end = wbNext(main[0], T),""", """function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), main = wbMain(g), live = wbGroupOn(g, T), end = live ? wbGroupEnd(g, T) : wbGroupNext(g, T),""")
rep("""<small>${!live ? `Every ${E.day} 18:00 UTC, for 48 hours` : up ?""", """<small>${!live ? `Every ${E.day} 18:00 UTC, for 48 hours` : g === 3 ? (wbOn("epx", T) ? (st.hp.epx > 0 ? "The Pentarch tears at the Void. Bring it down!" : "The Pentarch has fallen. The Void is saved.") : `${WB_EL.filter(k => st.hp[k] > 0).length} of 5 Elementals still standing · they fuse in ${ftime(wbLiveEnd("eic", T) - T)}`) : up ?""")
rep("""  const cons = g === 2 ? "" :""", """  const cons = g !== 1 ? "" :""")
rep("""  const rules = g === 2 ?""", """  const rules = g === 3 ? `The Elemental Convergence comes every other Wednesday at 18:00 UTC, for 48 hours. For the first 24 hours the five Elementals, Glacius, Ignis, Solara, Voltaris and Verdanth, tear into the galaxy, staining the worlds around them with their element. Then the survivors fly to the black hole at the centre and fuse into the Pentarch, and for the last 24 hours it tears at the Void. Every Elemental slain before the fusion is missing from the Pentarch, and it is that much weaker. Every 2.5% of hull you destroy scores 3 Hunt points, or 6 on the Pentarch, and every attack pays a bounty and drops forge materials.` : g === 2 ?""")
rep("""${pts ? (g === 2 ? "every 2.5% of hull you destroy scores 3" :""", """${pts ? (g === 3 ? "every 2.5% of hull you destroy scores 3, or 6 on the Pentarch" : g === 2 ? "every 2.5% of hull you destroy scores 3" :""")
rep("""const EVS = [["sboss", "Super Boss Hunt", "☠"], ["tboss", "Titan Hunt", "☣"], """, """const EVS = [["sboss", "Super Boss Hunt", "☠"], ["tboss", "Titan Hunt", "☣"], ["eboss", "Convergence", "✪"], """)
rep("""  if (k === "tboss") return sbReady(2);""", """  if (k === "tboss") return sbReady(2);
  if (k === "eboss") return sbReady(3);""")
rep("""if (k === "tboss") return sbBanner(T, 2);""", """if (k === "tboss") return sbBanner(T, 2); if (k === "eboss") return sbBanner(T, 3);""")
rep("""  else if (k === "sboss" || k === "tboss") { const g = k === "tboss" ? 2 : 1;""", """  else if (k === "sboss" || k === "tboss" || k === "eboss") { const g = k === "eboss" ? 3 : k === "tboss" ? 2 : 1;""")
rep("""sbClaim: d => act(() => { const g = +(d && d.g) === 2 ? 2 : 1,""", """sbClaim: d => act(() => { const g = [1, 2, 3].includes(+(d && d.g)) ? +d.g : 1,""")
rep("""${[1, 2].map(g => `${g === 2 ? `<h2 class="sec">Wednesday titans</h2><button class="btn ghost wide" data-act="events" data-ev="tboss" style="margin:0 0 8px">☣ Titan Hunt · live board, points and rewards</button>` : ""}""",
    """${[1, 2, 3].map(g => `${g === 2 ? `<h2 class="sec">Wednesday titans</h2><button class="btn ghost wide" data-act="events" data-ev="tboss" style="margin:0 0 8px">☣ Titan Hunt · live board, points and rewards</button>` : g === 3 ? `<h2 class="sec">Elemental Convergence</h2><button class="btn ghost wide" data-act="events" data-ev="eboss" style="margin:0 0 8px">✪ Convergence · live board, points and rewards</button>` : ""}""")
rep("""const BOSS_ART = """, """const BOSS_ART_EL = """ + json.dumps(ART) + """; // v401 the Elementals' concept art
const BOSS_ART = """)
rep("""// v389 concept art: banners g1/g2, portraits per boss""", """// v389 concept art: banners g1/g2, portraits per boss
Object.assign(BOSS_ART, BOSS_ART_EL);""")

# ---------- the Advisor ----------
rep("""  wbcon: "Commander, this Energy Conduit""", """  wbeic: "Commander, this is Glacius, the ice Elemental. It has frozen every world around it, and in a day it will join the others at the Void. Bring it down before the fusion, and the Pentarch is weaker for it.",
  wbefi: "Commander, this is Ignis, the fire Elemental. The worlds around it are burning, and in a day it will join the others at the Void. Bring it down before the fusion, and the Pentarch is weaker for it.",
  wbeli: "Commander, this is Solara, the light Elemental. Its pillar of light is gilding every world around it, and in a day it will join the others at the Void. Bring it down before the fusion.",
  wbest: "Commander, this is Voltaris, the storm Elemental. Its lightning is tearing at every world around it, and in a day it will join the others at the Void. Bring it down before the fusion.",
  wbena: "Commander, this is Verdanth, the nature Elemental. It is overgrowing every world around it, and in a day it will join the others at the Void. Bring it down before the fusion.",
  wbepx: "Commander, this is the Pentarch, every surviving Elemental fused into one, tearing at the black hole at the centre of the galaxy. It is the greatest threat we have faced. Rally every fleet and every ally.",
  wbcon: "Commander, this Energy Conduit""")
rep("""const ADV_NEWS = {""", """const ADV_NEWS = {"wb3_new": "Commander, the Elementals have torn through the Void! Glacius, Ignis, Solara, Voltaris and Verdanth are loose in the galaxy. In a day they will fuse. Strike them down before they do.", "wb3_fuse": "Commander, the Elementals are converging on the Void! The survivors have fused into the Pentarch, and it is tearing at the black hole. Rally every fleet.", "wb_live_eic": "Commander, Glacius is under attack right now! Watch it live.", "wb_live_efi": "Commander, Ignis is under attack right now! Watch it live.", "wb_live_eli": "Commander, Solara is under attack right now! Watch it live.", "wb_live_est": "Commander, Voltaris is under attack right now! Watch it live.", "wb_live_ena": "Commander, Verdanth is under attack right now! Watch it live.", "wb_live_epx": "Commander, the Pentarch is under attack right now! Watch the battle live.", "wb_fall_eic": "Commander, Glacius is shattered! It won't join the fusion.", "wb_fall_efi": "Commander, Ignis is extinguished! It won't join the fusion.", "wb_fall_eli": "Commander, Solara has gone dark! It won't join the fusion.", "wb_fall_est": "Commander, Voltaris is grounded! It won't join the fusion.", "wb_fall_ena": "Commander, Verdanth has withered! It won't join the fusion.", "wb_fall_epx": "Commander, the Pentarch has fallen! The Void is saved, and everyone who fought it can claim the spoils.", """)
rep("""  const c2 = wbCyc2(T); if (T - (WB2_BASE + c2 * WEEK) < 24 * 3600e3) advNews("wb2_new", "wb2:" + c2, { act: "events", ev: "tboss" }, "Titan Hunt"); }""",
"""  const c2 = wbCyc2(T), s2 = WB2_BASE + c2 * WEEK, odd = ((c2 % 2) + 2) % 2 === 1;
  if (!odd && T - s2 < 24 * 3600e3) advNews("wb2_new", "wb2:" + c2, { act: "events", ev: "tboss" }, "Titan Hunt");
  if (odd && T - s2 < 24 * 3600e3) advNews("wb3_new", "wb3:" + c2, { act: "events", ev: "eboss" }, "Convergence");
  if (odd && T - s2 >= WB_FUSE && T - s2 < WB_FUSE + 3 * 3600e3) advNews("wb3_fuse", "wb3f:" + c2, { act: "cineObj", id: "wb_epx" }, "Watch the fusion"); }""")
rep("""["What are the Wednesday titans?",""", """["What is the Elemental Convergence?", "Every other Wednesday at eighteen hundred UTC, five Elementals tear through the Void for forty-eight hours. For the first day they stain the worlds around them with their element. Then the survivors fuse into the Pentarch above the black hole. Every Elemental we slay before the fusion is missing from the Pentarch, so hunt them early."], ["What are the Wednesday titans?",""")
rep("""The Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus return every Wednesday at 18:00 UTC for 48 hours, each with a trick""", """The Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus return every other Wednesday at 18:00 UTC for 48 hours (the Elemental Convergence takes the weeks between), each with a trick""")
rep("""d: "The Hive's queen, nesting""", """d: "The Hive's queen, nesting""")

# ---------- the owner preview ----------
rep("""<button class="btn ghost wide" data-act="healthOpen">📉 Crash &amp; performance</button>` : ""}""", """<button class="btn ghost wide" data-act="healthOpen">📉 Crash &amp; performance</button><button class="btn ghost wide" data-act="elePrev">✪ Preview the Elemental Convergence: ${["off", "the five Elementals", "the Pentarch"][G.elePrev || 0]}</button>` : ""}""")
rep("""  cineWide: () => {""", """  elePrev: () => { G.elePrev = ((G.elePrev || 0) + 1) % 3; G.elePrevAt = performance.now(); WB_SEPC = null; WB_ZONES = null; WB_INF = null; if (G3 && G3.wbM && G3.wbM.epx) { const M = G3.wbM.epx; if (M.b) { G3.scene.remove(M.b.grp); } delete G3.wbM.epx; G3.wbComp = 0; }
    toast(G.elePrev ? `Owner preview: ${G.elePrev === 1 ? "the five Elementals are on the map (Finder › Map Events)" : "the Pentarch fuses above the Void"}. Only you see this.` : "Preview off."); if (sheet) renderSheet(); },
  cineWide: () => {""")
t = t.replace("const GAME_V = 400;", "const GAME_V = 401;")
open(p, "w").write(t); print("ok")
# (applied after) the Pentarch rebuilds when an Elemental falls, so the fallen aspect leaves it
