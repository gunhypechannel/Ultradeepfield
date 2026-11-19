/* ---------- v666 Mimic Echoes: the Assimilators copy our ships ----------
   When a fight at a Stage 3+ hive ends with its Assimilators still alive and our ships lost, they absorb the wrecks: for 6 hours a few
   Mimic Echoes of the class we lost most of fight in every hive we attack (per player, at most 6). An Echo has the silhouette of that
   class and 60% of its base stats with none of our research, cosmetics or loadout (the spec: "limited combat characteristics", never a
   player's own equipment). Counter: the same counters as the original class; destroying a Stage 3+ hive with its Echoes aboard wipes
   them and pays 2 Assimilated Alloy an Echo. */
const ECHO_BASE = ["fighter", "heavyFighter", "corvette", "bomber", "destroyer", "battleship", "bastion", "dreadnought"];
function mimEcho(x, rep, res, T) { const M = mimS(), st = mimStage(x, T), had = Object.keys(rep.lossD || {}).filter(k => /^e_/.test(k));
  if (res.winner === "a" && had.length) { const n = had.reduce((a, k) => a + (rep.lossD[k] || 0), 0); M.m.alloy = (M.m.alloy || 0) + 2 * n; M.echo = null; rep.echoWipe = n; note(`The Mimic Echoes went down with ${x.name}: +${2 * n} Assimilated Alloy. The swarm has no copies of our ships left.`, "win"); dirty(); return; }
  if (st < 3 || !(((res.dLeft || {}).massim || 0) > 0)) return;
  let best = null, bn = 0; for (const k of ECHO_BASE) { const n = (rep.lossA || {})[k] || 0; if (n > bn) { bn = n; best = k; } } if (!best) return;
  const n = Math.min(6, Math.max(1, Math.ceil(bn / 25))); M.echo = { k: best, n, until: T + 6 * 3600e3 }; rep.echo = best; dirty();
  note(`The Assimilators absorbed the wrecks of our ${SH[best].n}s. For 6 hours, ${n} Mimic Echo${n > 1 ? "es" : ""} of them will fight in the hives. Destroy a Stage 3 hive to wipe them out.`, "warn"); }
const mimEchoOn = T => { const e = S && S.mim && S.mim.echo; return e && e.until > T ? e : null; };
