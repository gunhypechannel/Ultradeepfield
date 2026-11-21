# v689: a joint-strike fleet left flying to a fight that already happened (an older copy of the empire on another device was saved
# over the newer one, bringing the fleet back from before the strike), fleets coming home from a joint strike can be sped up, the
# Cube-formation fleet model no longer crashes the map without a flagship, and an older copy of the empire can no longer win at sign-in
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# 1. the Cube formation read the flagship's size even when there was no flagship: every map frame threw before the fleets were drawn
rep('const s = cube ? FM.slot(i, N, sp, k, F0, j)', 'const s = cube ? FM.slot(i, N, sp, k, F0 || { len: geos[0].len, wid: geos[0].wid }, j) /* v689 */')

# 2. a fleet on its way home from a joint strike is an ordinary fleet: afterburners, boosts, hurry, the top-bar chip and alliance help
rep('canHurry = bnd && !f.assault && f.phase !== "resolving"', 'canHurry = bnd && (!f.assault || f.phase === "back") && f.phase !== "resolving"')
rep('${!f.assault && f.phase !== "resolving" && rem > 20000 ?', '${(!f.assault || f.phase === "back") && f.phase !== "resolving" && rem > 20000 ?')
rep('if (!f || f.assault) return; const c = fbCost(f);', 'if (!f || (f.assault && f.phase !== "back")) return; const c = fbCost(f);')
rep('if (!f || f.assault || !(S.boosts > 0)) return;', 'if (!f || (f.assault && f.phase !== "back") || !(S.boosts > 0)) return;')
rep('if (!f || !b || f.assault) return;', 'if (!f || !b || (f.assault && f.phase !== "back")) return;')
rep('if (f.phase === "back" && !f.assault && f.back - T > 20000)', 'if (f.phase === "back" && f.back - T > 20000)')
rep('(!f.assault && f.mission !== "spy" && (f.phase === "back" || f.phase === "out"))', '((!f.assault || f.phase === "back") && f.mission !== "spy" && (f.phase === "back" || f.phase === "out"))')

# 3. orphaned strike fleets: the strike's record says it already fought (or is gone), so the fleet takes that result now
rep('setInterval(() => { try { if (S) strikeSync(); } catch (e) {} }, 1000);', '''setInterval(() => { try { if (S) strikeSync(); } catch (e) {} }, 1000);
/* v689 a fleet still flying to a joint strike that has already fought (an older copy of the empire, saved from another device, brought
   it back from before the battle) or that no longer exists: it used to fly on for hours to a fight that was over, with no speed-ups.
   Now it lands at once and takes the strike's recorded result (or turns home if the strike is gone). */
function strikeOrphans(o) { if (!S || !G.db) return; for (const f of S.fleets) { const id = f.assault; if (!id || o[id] || f.orph === id || !(f.phase === "out" || f.phase === "muster") || G.resolving.has(f.id)) continue; f.orph = id;
    adb().doc("assaults/" + id).get().then(sn => { const a = sn && sn.exists ? sn.data() : null; if (!S.fleets.includes(f) || f.assault !== id || !(f.phase === "out" || f.phase === "muster")) return;
      if (a && a.status === "open") { f.orph = null; return; } const T = now(); f.phase = "out"; f.launched = 1; if (f.arrive > T + 2000) { f.arrive = T + 2000; f.out = Math.min(f.out || T, T - 1); }
      dirty(); flush(); toast(a ? "Your joint strike already fought while this device was behind. Your fleet's result is coming in." : "That joint strike no longer exists. Your fleet is turning home.", "warn"); softRender(); }).catch(() => { f.orph = null; }); } }''')
rep('G.assaults = o; callNew();', 'G.assaults = o; callNew(); try { strikeOrphans(o); } catch (e) {} /* v689 */')

# 4. an older copy of the empire could win at sign-in: a copy that stopped saving (another device took over) kept stamping itself as
#    "in sync with the cloud" every few seconds, so when that device reloaded, its older empire looked newer and was saved over the
#    real one. Now only a save that reached the server counts, and the save number this device last wrote or read decides.
rep('const cloudOk = store.db && store.uid && store.ready; if (cloudOk) S.cloudAt = S.savedAt;', 'const cloudOk = store.db && store.uid && store.ready && !store.paused; if (cloudOk) S.cloudAt = S.savedAt; /* v689 a paused copy no longer marks itself in sync */')
rep('store.lastW = Date.now(); store.seq = seq;', 'store.lastW = Date.now(); store.seq = seq; cseqSet(seq);')
rep('S = st; store.seq = +v.seq || 0;', 'S = st; store.seq = +v.seq || 0; cseqSet(store.seq);')
rep('const take = foreign || (!behind && (S.uid === uid ? cAt > (S.cloudAt || 0) : true));', 'const lseq = cseqGet(), take = foreign || (!behind && (S.uid === uid ? cAt > (S.cloudAt || 0) || (lseq > 0 && (+d.seq || 0) > lseq) : true)); /* v689 */')
rep('if (snap && snap.exists) store.seq = +(snap.data() || {}).seq || 0;', 'if (snap && snap.exists) { store.seq = +(snap.data() || {}).seq || 0; cseqSet(store.seq); }')
rep('const KEY = "novaDominion.save.v1";', '''const KEY = "novaDominion.save.v1";
/* v689 the cloud save number this device last wrote or loaded: if the account's save number is past it, another device saved since */
const cseqGet = () => { try { return +localStorage.getItem(KEY + ".cseq") || 0; } catch (e) { return 0; } }, cseqSet = n => { try { if (n > 0) localStorage.setItem(KEY + ".cseq", String(n)); } catch (e) {} };''')

# 5. the white light on a long flight: the warp-trail cosmetic dropped a glow every 80 ms where the fleet was, so a fleet crawling across a
#    15-hour march stacked all 15 additive glows on one spot. The trail now lies along the course behind the fleet, evenly spaced.
rep("""const nw = performance.now(); if (!o.ctT || nw - o.ctT > 80) { o.ctT = nw; o.cth.unshift([pt.x, pt.y, pt.z]); if (o.cth.length > 16) o.cth.length = 16; }
        for (let i = 0; i < 16; i++) { const sp = o.ct[i], q = o.cth[i]; if (!q || i === 0) { sp.visible = false; continue; } sp.visible = true; sp.position.set(q[0], q[1], q[2]); const k = 1 - i / 16;""",
    """const L = Math.max(1, Math.hypot(path.b.x - path.a.x, (path.b.y || 0) - (path.a.y || 0), path.b.z - path.a.z)), stp = fs * 1.1 / L, q0 = ARC(path.a, path.b, path.k), ox = pt.x - q0.x, oy = pt.y - q0.y, oz = pt.z - q0.z; /* v689 */
        for (let i = 0; i < 16; i++) { const sp = o.ct[i], kk = path.k - i * stp; if (i === 0 || kk <= 0) { sp.visible = false; continue; } const q = ARC(path.a, path.b, kk); sp.visible = true; sp.position.set(q.x + ox, q.y + oy, q.z + oz); const k = 1 - i / 16;""")
rep('sp.material.opacity = .9 * k; } }', 'sp.material.opacity = .6 * k; } }')

rep('const GAME_V = 688;', 'const GAME_V = 689;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
