# v485 Multiplayer plan, phase 3 (built, switched off): the server can decide world boss fights.
# The boss fight's rules move into one pure function, wbDecide(cur, key, fleet, tech, ab, uid, at, aim, pos), used by the phone exactly
# as before. With UDF_SUPABASE.authority set to "on" (it is "off"), wbResolve asks the settle_fight server function instead: the server
# checks the fleet against the player's saved account (it must be that fleet, out, aimed at this boss, no bigger than it left), checks
# the tech is within reach of the saved research, runs the same wbDecide on the boss record itself, writes it, keeps a ledger of what
# each fight earned, and sends the result back for the phone to show and pay. A fleet is settled once (asking twice returns the first
# answer). "soft" falls back to the phone if the server can't be reached; "on" keeps the fleet out and tries again later.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
old_a = """    const shK = wbShOf(key, cur, at), mine0 = Object.assign({}, f.n);
    const { res, rise } = wbFightRise(() => stacksOf(f.n, techOf(null), G.me), () => stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"), D.k, n0);
    const left = clamp(Math.round(((res.dLeft || {})[D.k]) || 0), 0, n0), seg = n0 - left;
    { const q = wbPos(key, at, {}); cur.scar.push({ k: key, at, x: Math.round(q.x * 10) / 10, y: Math.round(q.y * 10) / 10, z: Math.round(q.z * 10) / 10, b: left ? 0 : 1 }); cur.scar = cur.scar.slice(-80); } cur.hit[key] = at; // wreckage stays 48 h; the Matriarch's swarm thins
    cur.hp[key] = left; const dm = cur.dmg[key] = cur.dmg[key] || {}; if (seg) dm[G.me] = (dm[G.me] || 0) + seg; if (!left) { cur.dead[key] = at; cur.last[key] = G.me; }
    const shedNow = []; if (key === "epx" && seg) { const fused = wbFusedIn(cur), live = () => fused.filter(k => !cur.shed.includes(k)), aim = live().includes(f.aim) ? f.aim : null; if (aim) cur.wing[aim] = (cur.wing[aim] || 0) + seg;
      for (const k of live()) if ((cur.wing[k] || 0) >= WB_SEG * .12) { cur.shed.push(k); shedNow.push(k); } // a wing everyone aims at breaks sooner
      const due = [.2, .4, .6, .8].filter(x => 1 - left / WB_SEG >= x).length; while (cur.shed.length < due && live().length) { const k = live().sort((a, b) => (cur.wing[b] || 0) - (cur.wing[a] || 0) || WB_EL.indexOf(a) - WB_EL.indexOf(b))[0]; cur.shed.push(k); shedNow.push(k); } }
    if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0;"""
assert s.count(old_a) == 1
new_a = """    const mine0 = Object.assign({}, f.n), q0 = wbPos(key, at, {}); let shK, res, rise, left, seg, shedNow, N0 = n0;
    const auth = wbAuthority(); if (auth) { const v = await wbAskServer(f, key, at, q0); if (v && v.fallen) { note(`The ${D.n} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
      if (v && v.cur) { ({ shK, res, rise, left, seg, shedNow } = v); N0 = v.n0; for (const k in cur) delete cur[k]; Object.assign(cur, v.cur); } else if (auth === "on") { G.resolving.delete(f.id); return; } } /* "on": the fleet waits for the server */
    if (res === undefined) { if (!n0) { note(`The ${D.n} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
      ({ shK, res, rise, left, seg, shedNow } = wbDecide(cur, key, f.n, techOf(null), cmdAb(), G.me, at, f.aim, q0));
      if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; } f.casN = 0;"""
s = s.replace(old_a, new_a)
rep("    if (!n0) { note(`The ${D.n} had already fallen when our fleet arrived. Returning.`, \"warn\"); return home(); }\n    const mine0", "    const mine0")
rep("/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */",
r"""/* v485 a world boss fight's rules in one pure function, the same on the phone and on the server (settle_fight cuts it out of the game):
   the record cur is changed in place (hull, damage board, kill, wreck, the Pentarch's seals); the commander's tech and gunnery (ab) come in
   as values, so nothing here reads the phone's own state */
function wbDecide(cur, key, n, tech, ab, uid, at, aim, pos) { const D = WB[key], n0 = cur.hp[key] | 0; if (!n0) return null;
  const shK = wbShOf(key, cur, at), mkA = () => stacksOf(n, tech, null).map(x => Object.assign(x, { own: uid, ab: +ab || 0 }));
  const { res, rise } = wbFightRise(mkA, () => stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"), D.k, n0);
  const left = clamp(Math.round(((res.dLeft || {})[D.k]) || 0), 0, n0), seg = n0 - left;
  if (pos) { cur.scar.push({ k: key, at, x: Math.round(pos.x * 10) / 10, y: Math.round(pos.y * 10) / 10, z: Math.round(pos.z * 10) / 10, b: left ? 0 : 1 }); cur.scar = cur.scar.slice(-80); } cur.hit[key] = at; // wreckage stays 48 h; the Matriarch's swarm thins
  cur.hp[key] = left; const dm = cur.dmg[key] = cur.dmg[key] || {}; if (seg) dm[uid] = (dm[uid] || 0) + seg; if (!left) { cur.dead[key] = at; cur.last[key] = uid; }
  const shedNow = []; if (key === "epx" && seg) { const fused = wbFusedIn(cur), live = () => fused.filter(k => !cur.shed.includes(k)), am = live().includes(aim) ? aim : null; if (am) cur.wing[am] = (cur.wing[am] || 0) + seg;
    for (const k of live()) if ((cur.wing[k] || 0) >= WB_SEG * .12) { cur.shed.push(k); shedNow.push(k); } // a seal everyone aims at breaks sooner
    const due = [.2, .4, .6, .8].filter(x => 1 - left / WB_SEG >= x).length; while (cur.shed.length < due && live().length) { const k = live().sort((a, b) => (cur.wing[b] || 0) - (cur.wing[a] || 0) || WB_EL.indexOf(a) - WB_EL.indexOf(b))[0]; cur.shed.push(k); shedNow.push(k); } }
  return { n0, shK, res, rise, left, seg, shedNow }; }
/* the commander's gunnery: +0.3% accuracy per commander level, up to +6% (stacksOf's ab for the player's own fleet) */
const cmdAb = () => S ? Math.min(.06, (cmdLevel(score()) - 1) * .0006) : 0;
/* v485 phase 3: who decides boss fights. "off" (the phone, today), "soft" (the server, the phone if it can't be reached), "on" (the server) */
const wbAuthority = () => { try { const a = window.UDF_SUPABASE && window.UDF_SUPABASE.authority; return G.mode === "online" && G.db && G.db.fn && (a === "on" || a === "soft") ? a : null; } catch (e) { return null; } };
async function wbAskServer(f, key, at, pos) { try { const v = await G.db.fn("settle_fight", { mode: "decide", kind: "wb", key, fleet: { id: f.id, n: f.n, aim: f.aim || null, arrive: at }, tech: techOf(null), ab: cmdAb(), pos: { x: pos.x, y: pos.y, z: pos.z }, v: GAME_V });
  if (v && v.error) { crumb("server refused the fight: " + v.error); return null; } return v; } catch (e) { crumb("server unreachable: " + String(e && e.message || e).slice(0, 80)); return null; } }
/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */""")
# the server already logged it: no shadow check for a fight the server decided
rep("    addReport(rep); fightShadow(rep); wbFight(key, seg, !left);", "    addReport(rep); if (!rep.srv) fightShadow(rep); wbFight(key, seg, !left);")
rep("const rep = mkRep({ at, kind: \"attack\", title: `Assault on the ${D.n}`, aUids: [G.me],", "const rep = mkRep({ srv: auth && res && res.srv ? 1 : undefined, at, kind: \"attack\", title: `Assault on the ${D.n}`, aUids: [G.me],")
rep("wbRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, wbSeg: [n0, left], lvl: 25, ptype: \"gas\", fortL: 0, alien: true,\n      start: res.start", "wbRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, wbSeg: [N0, left], lvl: 25, ptype: \"gas\", fortL: 0, alien: true,\n      start: res.start")
i = s.find("async function wbResolve"); j = s.find("finally {", i); seg_ = s[i:j]; assert seg_.count("const pv = jcopy(cur); pv.hp[key] = n0;") == 1
s = s[:i] + seg_.replace("const pv = jcopy(cur); pv.hp[key] = n0;", "const pv = jcopy(cur); pv.hp[key] = N0;") + s[j:]
s = re.sub(r"GAME_V = 484\b", "GAME_V = 485", s)
open(P, 'w').write(s)
