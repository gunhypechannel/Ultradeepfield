"""v864: the story voiced everywhere (Aetherion beats, the Continuum and Omega cinematics, the naming line, the Prime Ark's arrival),
the Abyssal Crown's own voice in its cinematics, the Overlord's shield layers in its battle, and the battle backdrop: a world
only where the fight is at one, painted sharp and in eclipse (p864_bg.js)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
D = __file__.rsplit('/', 1)[0]
rep("const GAME_V = 863;", "const GAME_V = 864;")
# --- the cinematics speak their lines, and each panel holds until its line is spoken
rep("function cntCine(key, done) {", """/* v864 a cinematic panel's line, spoken by the Advisor (or the Crown) when it is voiced; the panel holds until it is said */
function cineVo(s, base) { try { if (!s || !voiceHas(s) || !VOICE.on || (typeof AU !== "undefined" && AU.muted)) return base; speak(s); const e = VENV && VENV[voiceKey(s)]; return e ? Math.max(base, e.length / 25 * 1000 + 900) : base; } catch (e) { return base; } }
function cntCine(key, done) {""")
rep("i++; clearTimeout(tm); tm = setTimeout(show, big ? 5600 : 4400); };", "i++; clearTimeout(tm); tm = setTimeout(show, cineVo(s, big ? 5600 : 4400)); }; /* v864 */")
rep("i++; clearTimeout(tm); tm = setTimeout(show, t === \"OMEGA\" ? 5200 : 4200); };", "i++; clearTimeout(tm); tm = setTimeout(show, cineVo(s, t === \"OMEGA\" ? 5200 : 4200)); }; /* v864 */")
rep('setTimeout(tick, 900); setTimeout(() => { try { if (document.body.contains(w)) sbSay(CRC_SAY["cine_" + k]); } catch (e) {} }, 2600); /* v705 */',
    'let vo = 0; setTimeout(() => { tick(); vo = cineVo(q, 0); setTimeout(() => { try { if (document.body.contains(w)) sbSay(CRC_SAY["cine_" + k]); } catch (e) {} }, Math.max(1700, vo + 500)); }, 900); /* v705; v864 the Crown speaks its words first */')
# --- the Prime Ark's first appearance in a fight
rep("const CNT_SIG = [", 'const CNT_PRIME_LINE = "That\'s the Prime Ark, Commander. Every ship we\'ve ever killed went through it. Bring it down and they stay dead."; /* v864, approved */\nconst CNT_SIG = [')
rep("if (alive && P) { const ph = cntEterPh(b, i), fast =", "if (alive && P && !(b.intro > 0) && !b.primeSaid) { b.primeSaid = 1; try { if (advOnce(\"primeArk\")) sbSay(CNT_PRIME_LINE); } catch (e) {} } /* v864 */\n    if (alive && P) { const ph = cntEterPh(b, i), fast =")
# --- the label
rep('"The wild Kraken"', '"The Kraken"')
# --- the Overlord's conduits in its battle, and its shield shells showing how many still stand
js = "const ovlCons = r => r && r.wb === \"ovl\" ? (r.wbSh ? Math.max(0, Math.min(4, Math.round((r.wbSh - 1) / .75))) : 4) : 0; /* v864 the conduits standing when the fight began */\n" + open(D + "/p864_bg.js", encoding="utf-8").read()
rep("function drawBattle(t) {", js + "function drawBattle(t) {")
rep("if (WB_EL.includes(key) && battle && battle.r) WBR.b.mech = { s: battle.r.wbSh || 1, k: 0 };", 'if (WB_EL.includes(key) && battle && battle.r) WBR.b.mech = { s: battle.r.wbSh || 1, k: 0 }; if (key === "ovl" && battle && battle.r) WBR.b.cons = ovlCons(battle.r); /* v864 */')
# --- the backdrop: a world only where the fight is at one, painted sharp and in eclipse; open space elsewhere
rep('''    drawPlanetBody(x, { type: r.ptype || "terran", v: 0 }, pcx, pcy, pr, -.8, -.7);
    const ag = x.createRadialGradient(pcx, pcy, pr * .96, pcx, pcy, pr * 1.09); ag.addColorStop(0, "rgba(90,170,255,0)"); ag.addColorStop(.35, "rgba(110,190,255,.55)"); ag.addColorStop(1, "rgba(60,120,255,0)");
    x.fillStyle = ag; x.beginPath(); x.arc(pcx, pcy, pr * 1.09, 0, TAU); x.fill();''',
    '''    b.atP = bpAt(r); /* v864 */ if (b.atP) { try { bpPaint(x, r, W, H, pcx, pcy, pr); } catch (e) { drawPlanetBody(x, { type: r.ptype || "terran", v: 0 }, pcx, pcy, pr, -.8, -.7); } } else bpSpace(x, W, H);''')
rep("if (heat > .03 && !lo) { ctx.globalCompositeOperation = \"lighter\"; const nF", "if (heat > .03 && !lo && b.atP) { ctx.globalCompositeOperation = \"lighter\"; const nF")
# which reports are fought at a world
rep("ptype: p.type", 'site: "planet", ptype: p.type', 4)
rep('ptype: hp ? hp.type : "terran"', 'site: "planet", ptype: hp ? hp.type : "terran"', 2)
rep("ptype: EL_PTYPE[e]", 'site: "planet", ptype: EL_PTYPE[e]')
rep('ptype: TYPES.includes(it.ptype) ? it.ptype : "terran"', 'site: it.kind === "tile" ? "space" : "planet", ptype: TYPES.includes(it.ptype) ? it.ptype : "terran"')
rep('dName: `${y.name} Guardians`, lvl: y.lvl * 2, ptype: "desert"', 'dName: `${y.name} Guardians`, lvl: y.lvl * 2, site: "planet", ptype: "desert"')
rep('dName: "Fortress Kesh Prime", lvl: 30, ptype: "lava"', 'dName: "Fortress Kesh Prime", lvl: 30, site: "planet", ptype: "lava"')
rep('title: "The first defence", aName: "Hive Scouts", dName: S.homeName || "Our new world", lvl: 1, ptype: "terran"', 'title: "The first defence", aName: "Hive Scouts", dName: S.homeName || "Our new world", lvl: 1, site: "planet", ptype: "terran"')
# the Overlord's four conduits on the map: since the Overlord moved to the rotation calendar its conduits took its position and never got
# their offsets, so all four sat inside it (owner: "why are they not on the map when the overlord has his 4 shields, it used to have them
# on all 4 corners")
rep("function wbPosRaw(key, T, out) { const o = out || {};", """function wbPosRaw(key, T, out) { const o = out || {};
  if (WB[key] && WB[key].con != null && wbG2(key)) { wbPosRaw("ovl", T, o); const r = Math.hypot(o.x, o.z) || 1, ux = o.x / r, uz = o.z / r, f = WB_OFF[key]; o.x += ux * f[0] - uz * f[1]; o.z += uz * f[0] + ux * f[1]; return o; } /* v864 */""")
open(p, "w", encoding="utf-8").write(s); print("ok")
