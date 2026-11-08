# v338: weekly missions (three per server week, Monday 00:00 UTC), each paying resources, shards and materials, with a bonus for all three
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('function vQuests() {', r'''const WEEKLY = [
  { k: "wins", t: n => `Win ${n} battles`, n: 15 }, { k: "hiveWins", t: n => `Defeat ${n} Hive garrisons`, n: 5 }, { k: "gathers", t: n => `Gather from resource fields ${n} times`, n: 8 },
  { k: "pirates", t: n => `Raid ${n} pirate hideouts`, n: 4 }, { k: "monsters", t: n => `Hunt ${n} space monsters`, n: 3 }, { k: "built", t: n => `Complete ${n} constructions`, n: 12 },
  { k: "researched", t: n => `Finish ${n} research`, n: 5 }, { k: "shipsBuilt", t: n => `Build ${n} ships or defenses`, n: 60 }];
const weekEnd = () => Date.UTC(2026, 0, 5) + (weekNo() + 1) * 7 * 864e5;
function ensureWeekly() { const wk = weekNo(); if (S.weekly && S.weekly.wk === wk) return; const r = rnd(hash("wk" + wk)), pool = WEEKLY.slice(), picks = [];
  while (picks.length < 3) picks.push(pool.splice((r() * pool.length) | 0, 1)[0]); S.weekly = { wk, bonus: false, tasks: picks.map(d => ({ k: d.k, n: d.n, base: metric(d.k), claimed: false })) }; dirty(); }
const weeklyRw = () => { const d = dailyReward(); return { m: d.m * 4, c: d.c * 4, g: d.g * 4, shards: 2, mats: LOOT.weekly() }; };
const WEEKLY_BONUS = () => ({ shards: 5, mats: LOOT.weeklyBonus() });
const weeklyReady = () => { try { ensureWeekly(); return S.weekly.tasks.filter(t => !t.claimed && dailyDone(t)).length + (!S.weekly.bonus && S.weekly.tasks.every(t => t.claimed) ? 1 : 0); } catch (e) { return 0; } };
function weeklyTasksCard(T) { ensureWeekly(); const end = weekEnd();
  return `<section class="evc" data-ev="wtasks"><div class="evh"><b>WEEKLY MISSIONS</b><span class="note">new missions in <b data-end="${end}">${ftime(end - T)}</b></span></div><p class="note">Bigger goals, bigger rewards, and the only regular source of every material. Each pays ${rwText(weeklyRw())}</p>
    ${S.weekly.tasks.map((w, i) => { const def = WEEKLY.find(x => x.k === w.k), prog = Math.max(0, Math.min(w.n, metric(w.k) - w.base)), d = prog >= w.n; if (!def) return "";
      return `<div class="tier"><span class="tn">${def.t(w.n)}<small>${prog} / ${w.n}</small></span><span class="trw"><span class="xp" style="display:block;min-width:60px"><i style="width:${prog / w.n * 100}%"></i></span></span>${w.claimed ? '<span class="pill ok">Claimed</span>' : `<button class="btn sm${d ? " amber" : " ghost"}" data-act="weeklyClaim" data-i="${i}" ${d ? "" : "disabled"}>Claim</button>`}</div>`; }).join("")}
    <div class="tier"><span class="tn">All three done<small>bonus</small></span><span class="trw">${rwText(WEEKLY_BONUS())}</span>${S.weekly.bonus ? '<span class="pill ok">Claimed</span>' : `<button class="btn sm${S.weekly.tasks.every(w => w.claimed) ? " amber" : " ghost"}" data-act="weeklyBonus" ${S.weekly.tasks.every(w => w.claimed) ? "" : "disabled"}>Claim</button>`}</div></section>`; }
function vQuests() {''')
rep('${dailyTasksCard(endDay, T)}', '${dailyTasksCard(endDay, T)}${weeklyTasksCard(T)}')
rep('''  dailyClaim: d => act(() => {''', '''  weeklyClaim: d => act(() => { ensureWeekly(); const w = S.weekly.tasks[+d.i]; if (!w || w.claimed || !dailyDone(w)) return; w.claimed = true; dirty(); grantRw(weeklyRw(), "Weekly mission"); SFX.research(); toast("Weekly mission claimed.", "win"); }), /* v338 */
  weeklyBonus: () => act(() => { ensureWeekly(); if (S.weekly.bonus || !S.weekly.tasks.every(w => w.claimed)) return; S.weekly.bonus = true; dirty(); grantRw(WEEKLY_BONUS(), "Weekly missions bonus"); SFX.research(); toast("Weekly bonus claimed.", "win"); }),
  dailyClaim: d => act(() => {''')
# the Quests badge and the Ready-to-claim box count weekly rewards too
rep('''n += masteryReady() || 0; if (S.daily && S.daily.tasks)''', '''n += masteryReady() || 0; n += weeklyReady(); if (S.daily && S.daily.tasks)''')
rep('''      if (dN) r.push(`<button class="btn amber" data-act="qJump" data-ev="qdaily">✓ ${dN} daily mission${dN > 1 ? "s" : ""} ready</button>`);''',
    '''      if (dN) r.push(`<button class="btn amber" data-act="qJump" data-ev="qdaily">✓ ${dN} daily mission${dN > 1 ? "s" : ""} ready</button>`);
      { const wN = weeklyReady(); if (wN) r.push(`<button class="btn amber" data-act="qJump" data-ev="wtasks">✓ ${wN} weekly reward${wN > 1 ? "s" : ""} ready</button>`); } /* v338 */''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
