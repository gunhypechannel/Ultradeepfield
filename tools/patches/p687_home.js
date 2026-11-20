/* v687 fleets flying home. (1) A "↩ Fleet home" chip in the top bar on the map and on the planet whenever a fleet is on its way back:
   the countdown, ⚡ afterburners in one tap, and a tap on the chip flies the camera to it (the ⚡ on the follow bar only showed once you
   had found the fleet). (2) Alliance help for the trip home, like help with a construction: ask once per trip; each member who helps
   cuts 4% of the time left (at least 30 seconds), up to 10 helps. Helping counts toward the same 30 helps a day and earns the same. */
const fhId = f => f.id + "-" + Math.round(f.arrive || f.out || 0);
function homeHB(T) { const fl = (S.fleets || []).filter(f => f.phase === "back" && !f.assault && f.back - T > 20000); if (!fl.length) return ""; const f = fl.reduce((a, b) => b.back > a.back ? b : a), c = fbCost(f);
  return `<button class="omb homeb" data-act="fleetMap" data-id="${f.id}"><b>↩ ${fl.length > 1 ? fl.length + " " : ""}HOME</b><span class="cpt" data-end="${f.back}"></span></button><button class="omb homeb hbz" data-act="fBoost" data-id="${f.id}" aria-label="Afterburners: the rest of the trip 50% faster" ${S.shards >= c ? "" : "disabled"}>⚡${c ? ` ◆${c}` : ""}</button>`; }
function fhelpBtn(f, sm) { const a = myAlly(); if (!a || !G.db || f.phase !== "back" || f.assault) return ""; const r = a.fhelp && a.fhelp[G.me];
  if (r && r.id === fhId(f)) return `<span class="pill ok" title="Alliance help on the trip home">🤝 ${Object.keys(r.by || {}).length}/${HELP_MAX}</span>`;
  return f.back - now() > 60000 ? `<button class="${sm ? "" : "btn ghost sm"}" data-act="askFHelp" data-id="${f.id}" aria-label="Ask your alliance to help this fleet home">🤝${sm ? "" : " Ask for help"}</button>` : ""; }
function fhelpApply() { const a = myAlly(), r = a && a.fhelp && a.fhelp[G.me]; if (!r) return; const f = (S.fleets || []).find(x => fhId(x) === r.id && x.phase === "back"); if (!f) return;
  S.fhelpGot = S.fhelpGot || {}; const got = Math.min(HELP_MAX, Object.keys(r.by || {}).length), done = S.fhelpGot[r.id] || 0; if (got <= done) return;
  let cut = 0; const T = now(); for (let i = done; i < got; i++) { const rem = f.back - cut - T; if (rem <= 1000) break; cut += Math.max(30000, rem * .04); }
  if (cut > 0) fleetSpeedUp(f, cut); S.fhelpGot[r.id] = got; dirty(); toast(`${got - done} alliance member${got - done > 1 ? "s" : ""} helped your fleet home: −${ftime(cut)}.`, "win"); softRender(); }
const allyHelpN = a => { const T = now(), n = o => Object.entries(o || {}).filter(([u, r]) => u !== G.me && r && a.members[u] && r.e > T && !(r.by || {})[G.me] && Object.keys(r.by || {}).length < HELP_MAX).length; return a ? n(a.help) + n(a.fhelp) : 0; };
