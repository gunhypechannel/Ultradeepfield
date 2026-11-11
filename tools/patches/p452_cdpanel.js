/* v452 Cube Devastation for everyone, not just the fight: the panel tells the whole event (art, every stage in your own time, what is
   happening now and what comes next, the fight, the rewards, the ranking), the band over the map shows from three days before through
   every stage, and the Advisor calls each stage as it happens to everyone on the map. */
const DVS = [[0, "awake", "Awakening", "The Super Cube wakes, and every Assimilation Cube answers.", "WARNING: MULTIPLE CUBE SIGNATURES ARE SYNCHRONIZING."],
  [DV.mig, "mig", "Migration", "All one hundred Assimilation Cubes leave their posts and fly to the Void.", "All one hundred Assimilation Cubes are leaving their posts. They're converging on the Void."],
  [DV.lock0, "asm", "Assembly", "They lock together like a puzzle around the Super Cube.", "They're locking together, piece by piece, around the Super Cube."],
  [DV.rb0, "rb", "Reconfiguration", "The puzzle tears itself apart and rebuilds into one giant cube.", "The puzzle is breaking apart. No. It's rebuilding into something far bigger."],
  [DV.act, "act", "The Omega Cube", "The finished machine wakes and erupts.", "The Omega Cube is awake."],
  [DV.stage, "stand", "The Last Stand", "A massed fleet makes its stand against it.", "Every fleet we have is taking position. This is our Last Stand."],
  [DV.fight0, "fight", "The Fight", "Every commander has 36 hours to bring it down before it disperses.", "The Omega Cube is open to attack. Thirty-six hours. All fleets, engage!"]];
const dvStage = e => { let i = 0; for (let k = 0; k < DVS.length; k++) if (e >= DVS[k][0]) i = k; return i; };
function dvSay(D) { const e = D.e, s0 = D.s0; G.dvSaid = G.dvSaid || {}; const say = (k, line) => { const id = s0 + k; if (G.dvSaid[id]) return; G.dvSaid[id] = 1; try { advHolo(line, 1); } catch (er) {} };
  const si = dvStage(e); if (e < DV.ret) say(DVS[si][1], DVS[si][4]); /* the stage you find it in, once, even arriving late */
  if (e >= DV.war0 && e < DV.war0 + 3 * 60e3) say("war", "The Last Stand has begun! Fire everything!"); if (e >= DV.war1 && e < DV.war1 + 3 * 60e3) say("lost", "The fleet is gone. The Omega Cube is still standing.");
  if (e >= DV.ret && e < DV.ret + 3 * 60e3) { const st = omState(s0); say("ret", st.hp ? "It's breaking apart. The cubes are scattering home. It will return next month." : "The Omega Cube is destroyed! Its cubes are scattering home, broken."); } }
function shOmega() { const T = now(), live = dvNow(T), s0 = live ? live.s0 : null, nx = dvNext(T), e = live ? live.e : -1, h = originPlanet(), avail = originAvail(), sel = selected(), sent = S.fleets.some(f => f.om && f.phase === "out");
  const st = s0 != null ? omState(s0) : { hp: OM_SEG, dmg: {} }, hp = st.hp, pc = Math.round(hp / OM_SEG * 100), on = omOn(T), my = (st.dmg || {})[G.me] || 0, fight = live && e >= DV.fight0, end = s0 != null ? s0 + omRB(s0) : 0, base = s0 != null ? s0 : nx, si = live ? dvStage(e) : -1;
  const tm = x => new Date(x).toLocaleString([], { weekday: "short", hour: "numeric", minute: "2-digit" });
  const tl = DVS.map(([at, k, n, d], i) => { const st2 = !live ? "" : i < si ? "done" : i === si ? "now" : ""; return `<li class="${st2}"><b>${esc(n)}</b><small>${tm(base + at)}${st2 === "now" ? " · NOW" : ""}</small><span>${esc(d)}</span></li>`; }).join("");
  const nextAt = live && si < DVS.length - 1 ? s0 + DVS[si + 1][0] : 0, lead = Object.entries(st.dmg || {}).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([u, v], i) => `<li><span>${i + 1}. ${esc(u === G.me ? "You" : nameOf(u))}</span><b>${v} section${v > 1 ? "s" : ""}</b></li>`).join("");
  let body = ""; if (!live) body = `<p class="note">It forms on the 15th of every month at ${new Date(nx).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} your time. Next: <b data-end="${nx}">${ftime(nx - T)}</b>.</p>${duelOwner() ? `<button class="btn ghost wide" data-act="dvSim">▶ Watch the preview (owner)</button>` : ""}`;
  else if (!fight) body = `<p class="note">Now: <b>${esc(DVS[si][2])}</b>. ${nextAt ? `${esc(DVS[si + 1][2])} in <b data-end="${nextAt}">${ftime(nextAt - T)}</b>.` : ""} Watch it from the galaxy map; attacks open when the fight begins.</p>`;
  else if (!on) body = `<p class="note">${hp ? "The Omega Cube is not open to attack right now." : "Destroyed. Its cubes are scattering across the galaxy."}</p>`;
  else if (!canPlay()) body = `<p class="note">${G.mode === "connecting" ? connNote() : "You can only watch this galaxy."}</p>`;
  else if (sent) body = `<p class="note">Our fleet is on its way.</p>`;
  else if (!Object.keys(avail).length) body = `${originBar()}<p class="note">No ships at ${esc(h ? h.name : S.homeName)}.</p>`;
  else body = `<h2 class="sec">Attack</h2>${originBar()}${picker(avail)}${speedBar(OMO, sel)}<button class="btn wide amber" data-act="omGo" ${Object.keys(sel).length && !slotsFull() ? "" : "disabled"}>⚔ Attack the Omega Cube</button>`;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">${live ? "● LIVE · " : ""}Cube Devastation · monthly event</div><h2>The Omega Cube</h2><p class="note">A hundred Assimilation Cubes lock round the Super Cube into one machine. Every section our fleets destroy breaks a cube off it. Bring it down before it disperses.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="sbart dvart"><img src="art/cube-event.jpg" alt="Cube Devastation" loading="lazy"><span class="sbph">${live ? esc(DVS[si][2]) : `Forms in ${ftime(nx - T)}`}</span></div>
    ${fight ? `<div class="wbhp"><div class="wbbar"><i style="width:${pc}%;background:#5dff6a"></i></div><span>${hp ? `${hp} of ${OM_SEG} sections · ${pc}%` : "Destroyed"}</span></div>` : ""}
    <dl class="kv">${fight ? `<dt>Your sections</dt><dd>${my || "None yet"}</dd><dt>${on ? "Disperses in" : "Status"}</dt><dd>${on ? `<b data-end="${end}">${ftime(end - T)}</b>` : hp ? "Not attackable" : "Fallen"}</dd>` : ""}<dt>Bounty per section</dt><dd>${costHTML({ m: 40000, c: 26000, g: 12000 })} + ◆3</dd><dt>When it falls</dt><dd>◆ shards by share, 2–5 elemental runes, an item; the top damage a Teleport Ticket</dd></dl>
    ${body}${lead ? `<h2 class="sec">Top damage</h2><ol class="wblead">${lead}</ol>` : ""}<h2 class="sec">${live ? "The event" : "How it unfolds"}</h2><ol class="dvtl">${tl}</ol>`; }
/* the band over the map: three days out, every stage, the fight */
function omBand() { const T = now(), b = $("#omband"), live = dvNow(T), nx = dvNext(T); let html = "";
  if (view === "galaxy" && !sheet && !battle && !G.sbSim) { if (live) { const e = live.e; if (e >= DV.fight0) { const st = omState(live.s0); if (omOn(T)) html = `<button class="omb" data-act="omOpen"><b>Ω OMEGA CUBE</b><span>${st.hp}/${OM_SEG}</span><i>⚔ Attack</i></button>`; }
      else html = `<button class="omb" data-act="omOpen"><b>Ω CUBE DEVASTATION</b><span>${esc(DVS[dvStage(e)][2])}</span></button>`; }
    else if (nx - T < 72 * 3600e3) html = `<button class="omb soon" data-act="omOpen"><b>Ω CUBE DEVASTATION</b><span>in ${ftime(nx - T)}</span></button>`; }
  if (!html) { if (b) b.remove(); return; } if (!b) { const A = $("#app"); if (!A) return; const el = document.createElement("div"); el.id = "omband"; el.innerHTML = html; A.appendChild(el); } else if (b.dataset.h !== html) { b.dataset.h = html; b.innerHTML = html; } }
setInterval(() => { try { omBand(); omClaim(); } catch (e) {} }, 1000);
