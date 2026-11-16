# v606 the Advisor talks about the Titans in play (owner: "shouldn't the advisor have lines for titan ships without having to see
# preview?"). Her only Titan lines were in their archive entries, heard only in the Titan inspection viewer. Now, on her hologram:
#  - when a Titan leaves the shipyard (commissioned),
#  - when you gather enough Titan Cores for a Titan you don't have yet (once per Titan),
#  - when a battle opens with your Titan on the field, and a warning when the enemy brings one (once per battle),
#  - when your Titan unleashes its ultimate (once per Titan per battle).
# Two or three lines for each, picked at random; the v605 rule still keeps any line from repeating within 2 minutes.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''/* ---------- v606 the Advisor on the Titans ---------- */
const TADV = {
  built: { armageddon: ["The Armageddon is out of the dock, Commander. Six Warden hearts in its spine and one very large cannon. Point it at something.", "Armageddon commissioned. When it fires the Worldbreaker, I'd suggest everyone look away."],
    sovereign: ["The Sovereign Ark has launched. I can feel every ship it commands, Commander. They fight as one now.", "Sovereign Ark commissioned. The fleet has a crown again."],
    harbinger: ["The Eclipse Harbinger is awake. Its reactor beats in time with the Void, Commander. Use it before it starts using us.", "Eclipse Harbinger commissioned. Its drones are already restless."] },
  cores: { armageddon: "We have enough Titan Cores for an Armageddon, Commander. The shipyard is waiting.", sovereign: "We have the Titan Cores for a Sovereign Ark. Imagine the whole fleet moving as one.", harbinger: "There are enough Titan Cores for the Eclipse Harbinger. I don't like it, Commander, but I understand why we'd build it." },
  battle: { armageddon: ["The Armageddon is with us. Clear a line for the Worldbreaker.", "Armageddon on the line. Charge the cannon, Commander."],
    sovereign: ["The Sovereign Ark takes command. Every ship, link up and hold formation.", "Sovereign Ark on the field. Shields up, fighters out."],
    harbinger: ["The Harbinger is here. Release the swarm, Commander.", "Eclipse Harbinger on the field. Let the drones hunt."] },
  foe: { armageddon: "Commander, they've brought an Armageddon. Break it with bombers and the Harbinger before its cannon charges.", sovereign: "Their Sovereign Ark is linking their fleet. Hit its hangars hard, Commander.", harbinger: "An enemy Harbinger. Spread the fleet before its swarm finds us." },
  ult: { wbc: ["Worldbreaker Cannon, firing!", "There it goes. Worldbreaker away!"], wing: ["Fleet Command Uplink! Strike wing, launch!", "The Ark is calling its wing. Fighters away!"], swarm: ["Neural Swarm released. Six targets, one mind.", "The swarm is loose, Commander!"] } };
const tadvPick = L => Array.isArray(L) ? L[(Math.random() * L.length) | 0] : L;
function titAdv(kind, k) { try { if (!S || !G.ready) return; const L = (TADV[kind] || {})[k]; if (L) advHolo(tadvPick(L)); } catch (e) {} }
/* a battle opening with a Titan in it: yours, or a warning about theirs */
function titAdvBattle(b) { try { if (!b || !b.r || b.tAdv) return; const r = b.r, mine = r.kind === "defense" || r.kind === "raid" ? "d" : "a"; if (!((r.aUids || []).includes(G.me) || r.dUid === G.me)) return; b.tAdv = 1;
  const my = b.Q.find(q => q.side === mine && TITAN_INFO[q.k]), foe = b.Q.find(q => q.side !== mine && TITAN_INFO[q.k]); if (foe) titAdv("foe", foe.k); else if (my) titAdv("battle", my.k); } catch (e) {} }
/* enough Titan Cores for a Titan you don't have yet: once for each */
setInterval(() => { try { if (!S || !G.ready || battle || typeof SH === "undefined") return; for (const k of ["armageddon", "sovereign", "harbinger"]) if (SH[k] && SH[k].tc && (S.tcore || 0) >= SH[k].tc && !((S.ships || {})[k] > 0) && advOnce("tcore_" + k)) { titAdv("cores", k); break; } } catch (e) {} }, 15000);
'''
rep('/* ---------- v589 battle effects remaster', JS + '/* ---------- v589 battle effects remaster')
rep('note(`${UDEF(h.k).n} ×${h.n} finished`);', 'note(`${UDEF(h.k).n} ×${h.n} finished`); if (TITAN_INFO[h.k]) titAdv("built", h.k); /* v606 */')
rep('b.ult590 = { t: tn, i: v.s, col:', '{ const qq = b.Q[v.s], ms = b.r && (b.r.kind === "defense" || b.r.kind === "raid") ? "d" : "a"; b.tUlt = b.tUlt || {}; if (qq && qq.side === ms && !b.tUlt[qq.k] && b.r && ((b.r.aUids || []).includes(G.me) || b.r.dUid === G.me)) { b.tUlt[qq.k] = 1; titAdv("ult", v.ab); } } /* v606 */ b.ult590 = { t: tn, i: v.s, col:')
rep('battle.superSide = r.sbk || r.omega ? "d"', 'setTimeout(() => titAdvBattle(battle), 2600); /* v606 */ battle.superSide = r.sbk || r.omega ? "d"')
s2 = re.sub(r"GAME_V = 605\b", "GAME_V = 606", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
