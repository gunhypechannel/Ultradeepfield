# v484 Multiplayer plan, phase 2 (shadow): after every world boss, super boss and Omega Cube fight, the phone sends the fight's inputs
# (the report's sim: both sides' stacks, the seed, the rules version) and the hull it says is left to the settle_fight server function,
# which re-runs the game's own simulator and logs whether the two agree (fight_log). Fire and forget: nothing waits on it, nothing
# changes for the player, and offline, the artifact and test fights send nothing.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */",
r"""/* v484 the server re-runs this boss fight and logs whether it agrees (phase 2, shadow) */
function fightShadow(rep) { try { if (G.mode !== "online" || !G.db || !G.db.fn || !rep || rep.test || !rep.sim) return; const sg = rep.sbSeg || rep.omSeg || rep.wbSeg; if (!sg) return;
  const unit = rep.omega ? "wbOmg" : rep.sbk ? SBW[rep.sbk].u : WB[rep.wb] ? WB[rep.wb].k : null; if (!unit) return;
  G.db.fn("settle_fight", { kind: rep.omega ? "om" : rep.sbk ? "sb" : "wb", unit, n0: sg[0], left: sg[1], sim: rep.sim, lossA: rep.lossA, v: GAME_V }).then(r => { if (r && r.ok === false) crumb(`server disagrees: ${unit} ${sg[1]} vs ${r.left}`); }, () => {}); } catch (e) {} }
/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */""")
rep("    addReport(rep); wbFight(key, seg, !left);", "    addReport(rep); fightShadow(rep); wbFight(key, seg, !left);")
rep('addReport(rep); omClaim(); home();', 'addReport(rep); fightShadow(rep); omClaim(); home();')
rep('addReport(rep); sbClaim(); home();', 'addReport(rep); fightShadow(rep); sbClaim(); home();')
s = re.sub(r"GAME_V = 483\b", "GAME_V = 484", s)
open(P, 'w').write(s)
