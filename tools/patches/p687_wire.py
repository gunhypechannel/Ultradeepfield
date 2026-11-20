# v687 speeding up fleets on their way home: the top-bar chip and alliance help for the trip home (see p687_home.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('help[u] = { id: h.id.slice(0, 80), k: String(h.k || "").slice(0, 60), e: +h.e || 0, t: +h.t || 0, by }; }',
    'help[u] = { id: h.id.slice(0, 80), k: String(h.k || "").slice(0, 60), e: +h.e || 0, t: +h.t || 0, by }; }\n  const fhelp = {}; if (d.fhelp && typeof d.fhelp === "object") for (const u in d.fhelp) { const h = d.fhelp[u]; if (!members[u] || !h || typeof h !== "object" || typeof h.id !== "string") continue; const by = {}; if (h.by && typeof h.by === "object") for (const b in h.by) if (members[b] && b !== u) by[b] = +h.by[b] || 1; fhelp[u] = { id: h.id.slice(0, 80), k: String(h.k || "").slice(0, 60), e: +h.e || 0, t: +h.t || 0, by }; } /* v687 help on the trip home */')
rep('members, created: +d.created || 0, fund, help, sos, crest:', 'members, created: +d.created || 0, fund, help, fhelp, sos, crest:')
rep("Object.entries(a.help || {}).filter(([u, r]) => u !== G.me && r && a.members[u] && r.e > now() && !(r.by || {})[G.me] && Object.keys(r.by || {}).length < HELP_MAX).length", "allyHelpN(a)", 2)
rep('${canHurry && rem > 0 ? `<button class="btn amber sm" data-act="hurry"', '${fhelpBtn(f)}${canHurry && rem > 0 ? `<button class="btn amber sm" data-act="hurry"')
rep('<button data-act="fBoost" data-id="${f.id}" aria-label="Afterburners" ${b && !f.assault && S.shards >= fbCost(f) ? "" : "disabled"}>⚡</button>',
    '<button data-act="fBoost" data-id="${f.id}" aria-label="Afterburners" ${b && !f.assault && S.shards >= fbCost(f) ? "" : "disabled"}>⚡</button>${fhelpBtn(f, 1)}')
rep('key = f.id + f.phase + rk + (S.shards >= fbCost(f)) + fformOf(f);', 'key = f.id + f.phase + rk + (S.shards >= fbCost(f)) + fformOf(f) + fhelpBtn(f, 1);')
rep("${reqs.length ? reqs.map(([u, r]) =>", """${(() => { const fr = Object.entries(a.fhelp || {}).filter(([u, r]) => u !== G.me && r && a.members[u] && r.e > T && Object.keys(r.by || {}).length < HELP_MAX); return fr.map(([u, r]) => { const did = r.by && r.by[G.me]; return `<div class="crow"><span class="nm">${esc(nameOf(u))}<small>↩ ${esc(r.k)} · home in <b data-end="${r.e}">${ftime(r.e - T)}</b> · ${Object.keys(r.by || {}).length}/${HELP_MAX}</small></span>${did ? '<span class="pill ok">Helped</span>' : `<button class="btn amber sm" data-act="giveFHelp" data-u="${u}" ${today >= HELP_DAY ? "disabled" : ""}>Help</button>`}</div>`; }).join(""); })()}
      ${reqs.length ? reqs.map(([u, r]) =>""")
rep('function helpApply() {', 'function helpApply() { try { fhelpApply(); } catch (e) {} /* v687 */')
rep('else if (view === "galaxy" && !battle && !cineOn) hb = cubeHB(T); /* v593 */', 'else if (view === "galaxy" && !battle && !cineOn) hb = homeHB(T) + cubeHB(T); /* v593, v687 */')
rep('hb = nxCallBand(T) + omenBand(T) + d1Band(T) + mimBand(T) + wheelBand(); }', 'hb = nxCallBand(T) + homeHB(T) + omenBand(T) + d1Band(T) + mimBand(T) + wheelBand(); }')
rep('  giveHelp: d => {', '''  askFHelp: d => { const a = myAlly(), f = S.fleets.find(x => x.id === d.id); if (!a || !G.db || !f || f.phase !== "back" || f.assault) return toast("Join an alliance to ask for help.", "warn");
    const tg = fleetTarget(f), req = { id: fhId(f), k: `${fmt(sumShips(f.n))} ships from ${tg && tg.name ? tg.name : "a mission"}`.slice(0, 60), e: Math.round(f.back), t: now(), by: null }; a.fhelp = a.fhelp || {}; a.fhelp[G.me] = Object.assign({}, req, { by: {} }); render(true); try { fleetHud(true); } catch (e) {}
    G.db.doc("alliances/" + a.id).update({ fhelp: { [G.me]: req } }).then(() => toast("Your alliance has been asked to help this fleet home.", "win")).catch(() => toast("Couldn't reach your alliance.", "warn")); },
  giveFHelp: d => { const a = myAlly(), r = a && a.fhelp && a.fhelp[d.u]; if (!r || !G.db || r.e < now() || (r.by || {})[G.me]) return;
    S.helpDay = S.helpDay && S.helpDay.d === utcDay() ? S.helpDay : { d: utcDay(), n: 0 }; if (S.helpDay.n >= HELP_DAY) return toast(`You've helped ${HELP_DAY} times today. Thank you, Commander.`, "warn");
    S.helpDay.n++; if (Math.random() < ESH_P.help) grantShards(1, "Alliance help"); S.helpsGiven = (S.helpsGiven || 0) + 1; if (S.helpsGiven % 10 === 0) { S.shards = (S.shards || 0) + 1; toast("◆1 for helping your alliance.", "win"); } else toast(`You helped ${nameOf(d.u)}'s fleet home.`);
    r.by = Object.assign({}, r.by, { [G.me]: now() }); dirty(); render(true);
    G.db.doc("alliances/" + a.id).update({ fhelp: { [d.u]: { by: { [G.me]: now() } } } }).catch(() => {}); }, /* v687 */
  giveHelp: d => {''')
rep('function myJob() {', R('p687_home.js') + 'function myJob() {')
rep('.omb.fin b{color:var(--fc);white-space:nowrap}', '.omb.fin b{color:var(--fc);white-space:nowrap}\n.evbar.hb .omb.homeb{--fc:#7be3ff}\n.evbar.hb .omb.homeb b{color:#7be3ff;white-space:nowrap}\n.evbar.hb .omb.hbz{flex:0 0 auto;font-weight:700;color:#ffd36a}\n.evbar.hb .omb.hbz[disabled]{opacity:.45}')
rep('<p class="note">Each help cuts 4% of the remaining build time (at least 1 minute), up to ${HELP_MAX} per job.', '<p class="note">Each help cuts 4% of the remaining build time (at least 1 minute), or of a fleet\'s trip home (at least 30 seconds), up to ${HELP_MAX} per job.')
rep('const GAME_V = 686;', 'const GAME_V = 687;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
