"""v748: the Resurrection War at 10,000 commanders (server-applied fights and war points; see supabase/migrations/v748_cnt_scale.sql),
and each finale preview gets a fresh record."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 747;", "const GAME_V = 748;")
js = open(os.path.join(D, "p748_scale.js"), encoding="utf-8").read().strip()
rep("\n/* ---------- the Continuum's hulls:", "\n" + js + "\n/* ---------- the Continuum's hulls:")
# a fresh record for every preview (the second preview used to open on the first one's finished finale)
rep('const cntKey = () => cntPrevOn() ? "prev" : String(cntT0());', 'const cntKey = () => cntPrevOn() ? "prev" + (S.cntPrev.at || "") : String(cntT0()); /* v748 */')
# reading a v2 record: this commander's own numbers and the top five fill the maps
rep("""    else { const c = o.cmd[B.id] = o.cmd[B.id] || {}; c.hp = c.hp == null ? B.hp : +c.hp; c.dead = +c.dead || 0; c.back = +c.back || 0; c.res = +c.res || 0; c.dmg = c.dmg || {}; } }""",
    """    else { const c = o.cmd[B.id] = o.cmd[B.id] || {}; c.hp = c.hp == null ? B.hp : +c.hp; c.dead = +c.dead || 0; c.back = +c.back || 0; c.res = +c.res || 0; c.dmg = c.dmg || {}; } }
  if (o.v2) cntV2Fill(o); /* v748 */""")
# commanders in the war, Ark shares and the finale's top ten come from the server's totals on a v2 record
rep("""const arks = CNT_ARKS.filter(([id]) => st.ark[id].dead).length, perm = CNT_NET.filter(B => B.cnt === "cmd" && st.cmd[B.id].dead).length, n = Object.keys(st.con).length;""",
    """const arks = CNT_ARKS.filter(([id]) => st.ark[id].dead).length, perm = CNT_NET.filter(B => B.cnt === "cmd" && st.cmd[B.id].dead).length, n = st.v2 ? +st.n || 0 : Object.keys(st.con).length;""")
rep("""const my = (st.con[G.me] || 0) + (M.pend || 0), n = Object.keys(st.con).length, top = Object.entries(st.con).sort((a, b) => b[1] - a[1]).slice(0, 5);""",
    """cntMeLoad(); const my = (st.con[G.me] || 0) + (M.pend || 0), n = st.v2 ? Math.max(+st.n || 0, my > 0 ? 1 : 0) : Object.keys(st.con).length, top = Object.entries(st.con).sort((a, b) => b[1] - a[1]).slice(0, 5);""")
rep("""    const tot = Object.values(a.dmg).reduce((p, q) => p + q, 0) || 1, share = my / tot, last = a.last === G.me ? 2 : 0, r = { sh: Math.min(50, 15 + Math.round(share * 60)), core: 2 + Math.round(share * 8) + last, cell: 3 };""",
    """    const tot = (a.tot != null ? +a.tot : Object.values(a.dmg).reduce((p, q) => p + q, 0)) || 1, share = Math.min(1, my / tot), last = a.last === G.me ? 2 : 0, r = { sh: Math.min(50, 15 + Math.round(share * 60)), core: 2 + Math.round(share * 8) + last, cell: 3 };""")
rep("""function cntFinPart(o, uid) { const d = o.dmg[uid] || 0, h = o.hits[uid] || 0; if (!h) return 0; const top = Object.entries(o.dmg).sort((a, b) => b[1] - a[1]).slice(0, 10).some(([u]) => u === uid);""",
    """function cntFinPart(o, uid) { const d = o.dmg[uid] || 0, h = o.hits[uid] || 0; if (!h) return 0; const top = o.t10 != null && uid === G.me ? !!o.t10 : Object.entries(o.dmg).sort((a, b) => b[1] - a[1]).slice(0, 10).some(([u]) => u === uid);""")
rep("""function cntFinInit(cur) { const n = Math.max(1, Object.keys(cur.con || {}).length),""", """function cntFinInit(cur) { const n = Math.max(1, cur.v2 ? +cur.n || 0 : Object.keys(cur.con || {}).length),""")
rep("""function cntFinInfo(x, T) { const""", """function cntFinInfo(x, T) { cntMeLoad(); const""")
rep("""function cntBossInfo(x, T) { if (CNT_BOSS[x.id].cnt === "prime") return cntFinInfo(x, T); /* v744 */""", """function cntBossInfo(x, T) { if (CNT_BOSS[x.id].cnt === "prime") return cntFinInfo(x, T); /* v744 */ cntMeLoad();""")
# war points: one server call, no lock
rep("""  try { const ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, T); const add = cntCon(cur, M.pend, T);
    if (await casSet(ref, snap, cur)) { M.pend = 0; cntLocal(cur); dirty(); } } catch (e) {} finally { G.cntFlushing = 0; } }""",
    """  try { if (await cntSrvW()) { const pend = M.pend, r = await window.udfCnt.apply(cntDoc(), cntKey(), [{ t: "con", pts: pend }]); M.pend = Math.max(0, (M.pend || 0) - pend); cntMeSet(r && r.me); dirty(); return; } /* v748 */
    const ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, T); const add = cntCon(cur, M.pend, T);
    if (await casSet(ref, snap, cur)) { M.pend = 0; cntLocal(cur); dirty(); } } catch (e) {} finally { G.cntFlushing = 0; } }""")
# a fight on the network: read the record (no lock), fight, then the server applies the damage
rep("""  try { const at = f.arrive, ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), why = cntBlock(B, cur, at);""",
    """  try { const at = f.arrive, ref = adb().doc(cntDoc()), srv = await cntSrvW(); if (!srv) await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), why = cntBlock(B, cur, at);""")
rep("""    const left = clamp(Math.round(((res.dLeft || {})[Z.u]) || 0), 0, n0), seg = n0 - left; let pts = 0, event = "";
    if (seg) { pts = 4 * seg;""",
    """    const left = clamp(Math.round(((res.dLeft || {})[Z.u]) || 0), 0, n0); let seg = n0 - left, pts = 0, event = "", counted = 0;
    if (srv) { if (seg) { const r = await window.udfCnt.apply(cntDoc(), cur.k, [{ t: "hit", id: B.id, seg, at }]), q = (r && r.o && r.o[0]) || {}; if (r && r.d) cntLocal(r.d); cntMeSet(r && r.me); /* v748 */
        if (q.ev === "blocked") { note(`${B.name} changed while our fleet was on the way: another commander got there first. Fleet returning, nothing lost.`, "warn"); return home(); }
        seg = q.seg || 0; event = q.ev || ""; counted = q.counted || 0; } }
    else { if (seg) { pts = 4 * seg;""")
rep("""    const counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur);""",
    """    counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur); }""")
# a fight in the finale
rep("""  try { const at = f.arrive, fe = cntFinE(at), ref = adb().doc(cntDoc()); await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), o = cntFinNorm(cur, fe), P = cntFinPh(o, fe);""",
    """  try { const at = f.arrive, fe = cntFinE(at), ref = adb().doc(cntDoc()), srv = await cntSrvW(); if (!srv) await crcLock(ref); const snap = await casGet(ref), cur = cntNorm(snap.exists ? snap.data() : null, at), o = cntFinNorm(cur, fe), P = cntFinPh(o, fe);""")
rep(""", seg = Z.n0 - left; let pts = 0, msg = "", ev = "";
    if (tg === "conv" || tg === "esc") {""",
    """; let seg = Z.n0 - left, pts = 0, msg = "", ev = "", counted = 0;
    if (srv) { const r = await window.udfCnt.apply(cntDoc(), cur.k, [{ t: "fin", tg, seg, fe, win: res.winner === "a" }]), q = (r && r.o && r.o[0]) || {}; if (r && r.d) cntLocal(r.d); cntMeSet(r && r.me); /* v748 */
      if (q.ev === "closed" || q.ev === "gone" || q.ev === "shielded") { note(q.ev === "closed" ? "The battle for the Prime Ark moved on while our fleet was jumping. Fleet returning, nothing lost." : q.ev === "shielded" ? "The reactor is still shielded by the transfer. Cut the transmitter array first. Fleet returning, nothing lost." : `${cntFinTgName(tg)} fell to another fleet first. Fleet returning, nothing lost.`, "warn"); return home(); }
      const o2 = cntFinNorm(cntNorm(r && r.d, at), fe); seg = q.seg || 0; counted = q.counted || 0; ev = q.ev || ""; pts = tg === "conv" || tg === "esc" ? (ev === tg ? 3 : 0) : 4 * seg; msg = cntFinMsg(tg, ev, o2, seg); }
    else { if (tg === "conv" || tg === "esc") {""")
rep("""    o.hits[G.me] = (o.hits[G.me] || 0) + 1; const counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur);""",
    """    o.hits[G.me] = (o.hits[G.me] || 0) + 1; counted = pts ? cntCon(cur, pts, at) : 0;
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0; cntLocal(cur); }""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
