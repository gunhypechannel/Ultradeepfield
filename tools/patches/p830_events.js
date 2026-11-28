/* ---------- v830 the Events pages, simplified and alive (owner: "what can do to simplify and refine the events pages, every event should
   come with a how to participate page also ... events pages should be incredibly engaging and visually addicting" then "build it all").
   - One shelf instead of fifteen chips: LIVE NOW (big glowing cards with their countdowns), SEASONS & RANKINGS, and DAILY REWARDS (login,
     daily challenge, online, level and builder bonuses, VIP, gifts and achievements on one page).
   - Every event in one layout: its hero (with its own elemental particles, a light sweep and a glowing countdown), a nudge toward the next
     reward, three tabs (How to Play · Rewards · Ranking) and the Claim button pinned at the bottom.
   - How to Play: illustrated steps, a "Take me there" button, what earns points, and a tip in her voice. It opens by itself the first time
     you open each event.
   - Effects: each event has an element (the Cube green circuitry, Galaxy War crimson sparks, the Super Boss Hunt fire, the Titan Hunt toxic
     haze, the Convergence violet void, the Void Pass gold starlight, Conquest banner blue); milestone tracks are energy conduits; ready
     rewards pulse, the next one shimmers, locked top rewards glimmer; rankings have a podium, your row glows and says how far to the next
     place; the login calendar burns with your streak. One small canvas per page, paused when hidden, and fewer particles on low FX. ---------- */
const EVX = {
  pass: { el: "gold", c1: "#ffd36b", c2: "#fff1c4", shelf: "s" }, conq: { el: "banner", c1: "#5fb4ff", c2: "#d4ecff", shelf: "s" },
  sboss: { el: "fire", c1: "#ff6a3a", c2: "#ffc27a", shelf: "s" }, tboss: { el: "toxic", c1: "#8dff5a", c2: "#dcffb8", shelf: "s" },
  eboss: { el: "void", c1: "#b06cff", c2: "#e6d0ff", shelf: "s" }, gw: { el: "war", c1: "#ff3b4f", c2: "#ffb6a8", shelf: "s" },
  cube: { el: "circuit", c1: "#3dff8a", c2: "#c8ffdc", shelf: "s" }, rw: { el: "stars", c1: "#ffcf5a", c2: "#fff4d0", shelf: "d" } };
const EVX_DAILY = [["login", "Daily Login", "▣"], ["daily", "Daily Challenge", "★"], ["online", "Online Bonus", "◷"], ["lvlb", "Level Bonus", "▲"], ["builder", "Bonus Builder", "▦"], ["vip", "VIP", "♛"], ["gifts", "Alliance Gifts", "🎁"], ["ach", "Achievements", "✦"]];
const EVX_RANK = new Set(["pass", "conq", "sboss", "tboss", "eboss", "gw", "cube"]);
/* How to Play: steps [icon, title, text], the Take me there button [label, act, data], what earns points, and her tip */
const EV_HOW = {
  pass: { s: [["✦", "Do your missions", "Three daily and five weekly missions on the Rewards tab pay Void Pass XP."], ["▲", "Climb the tiers", "Every 2,000 XP is a tier, forty in a season."], ["🎁", "Claim every tier", "Each tier pays a free reward. Premium adds a second, richer one."], ["❖", "Go past forty", "After the last tier, more XP fills Void Caches with shards and boosters."]],
    go: ["See today's missions", "evTab", { v: "ov" }], p: [["A daily mission", "+400 XP"], ["All three dailies", "+300 XP bonus"], ["A weekly mission", "+2,000 XP"]],
    tip: "Three daily missions take ten minutes, Commander. Do them every day and the Pass climbs itself." },
  conq: { s: [["⚑", "Be in an alliance", "Conquest is fought by alliances. Join one or found your own."], ["🪐", "Hold worlds", "Your homeworld and colonies count toward the sector they sit in."], ["⚔", "Take rival colonies", "Every colony you take from a rival alliance swings its sector toward you."], ["◆", "Collect on Monday", "When the week ends (Monday 00:00 UTC) every member of a sector-holding alliance claims shards."]],
    go: ["Open Alliances", "nav", { v: "ally" }], p: [["A homeworld in a sector", "3"], ["A colony", "1"], ["Every 10 Commander levels of its owner", "+1"], ["Inner Belt and Core sectors", "count double"], ["Each point of control", "◆2 (up to ◆40)"]],
    tip: "Sectors are won by numbers, Commander. Every colony our alliance plants is another vote on the map." },
  sboss: { s: [["☠", "A boss arrives", "One boss each Monday at 18:00 UTC, for 48 hours."], ["🚀", "Attack it", "Send any fleet. Every attack, win or lose, pays a bounty and forge materials."], ["▮", "Score hull", "Every 2.5% of its hull you destroy scores Hunt points."], ["🎁", "Claim and share", "Claim milestones as you go; when it falls, everyone who hurt it shares its spoils."]],
    go: ["Find the boss", "evxGo", { k: "sboss" }], p: [["2.5% hull, Overlord or Devourer", "3"], ["2.5% hull, Void Warden", "2"], ["2.5% hull, a conduit", "1"]],
    tip: "You don't have to kill it, Commander. Every scratch you put on it counts." },
  tboss: { s: [["☣", "A titan arrives", "One titan each Monday at 18:00 UTC, for 48 hours."], ["🧠", "Learn its trick", "The Matriarch rebuilds her swarm, the Tyrant's bounty grows, the Wyrm opens its segments, the Colossus shatters."], ["🚀", "Attack it", "Every attack, win or lose, pays a bounty and forge materials."], ["🎁", "Share the spoils", "When it falls, everyone who damaged it claims a share."]],
    go: ["Find the titan", "evxGo", { k: "tboss" }], p: [["2.5% of its hull", "3"]],
    tip: "Each titan has its own trick, Commander. Learn it before you send the fleet." },
  eboss: { s: [["✪", "The Elementals rise", "Every fourth Wednesday at 18:00 UTC, five Elementals tear into the galaxy for 24 hours."], ["⚔", "Slay them early", "Each one slain before the fusion leaves the Pentarch weaker. Slay all five for a Clean Sweep."], ["◉", "Break the Pentarch", "The survivors fuse at the black hole. Crack its five rune seals to expose its core."], ["💎", "Gather the shards", "When it falls its core shatters: gather the shards within ten minutes."]],
    go: ["Find an Elemental", "evxGo", { k: "eboss" }], p: [["2.5% hull, an Elemental", "3"], ["2.5% hull, the Pentarch", "6"], ["Ships it destroys", "come home damaged, never lost"]],
    tip: "Nothing you send against the Convergence is lost for good, Commander. Send everything." },
  gw: { s: [["⚔", "Wait for the war", "The Galaxy War runs on its own schedule. The countdown is above."], ["💥", "Fight commanders", "Damage you deal to other commanders' ships scores PvP points."], ["🏆", "Win battles", "Every win, attacking or defending, adds a bonus."], ["🎁", "Claim", "Milestones as soon as you reach them; rank rewards after the war ends."]],
    go: ["Open the galaxy", "nav", { v: "galaxy" }], p: [["Damage to commanders' ships", "PvP points"], ["A win, attacking or defending", "bonus"]],
    tip: "Defending counts too, Commander. A strong home fleet scores while you sleep." },
  cube: { s: [["■", "Friday, 18:00 UTC", "The Battle for the Cube runs for 48 hours every weekend."], ["⚔", "Seize it", "Beat the Hive Warden, or the fleets stationed by the alliance holding it."], ["🛡", "Hold it", "Station fleets at the Cube to defend it. Every minute your alliance holds it counts."], ["👑", "Be holding at the end", "Whoever holds it when time runs out is crowned Sovereigns of the Cube."]],
    go: ["Fly to the Cube", "nexus", {}], p: [["Every minute your alliance holds it", "hold time"], ["Holding it when the timer ends", "the crown"]],
    tip: "The last hour decides everything, Commander. Save a fleet for it." },
  rw: { s: [["▣", "Log in every day", "Every day you play adds to your login rewards, VIP points included."], ["★", "Today's challenge", "Each day has its own challenge with three reward tiers."], ["◷", "Stay a while", "Online Bonus rewards come while the game is open."], ["▲", "Grow", "Level and Bonus Builder rewards pay out as your empire grows."]],
    go: ["Claim what's ready", "evTab", { v: "ov" }], p: [["A day logged in", "+VIP"], ["Daily challenge tiers", "3 rewards"], ["Time online", "rewards every few minutes"]],
    tip: "Small things every day, Commander. They add up faster than any war." } };
const evxEl = k => EVX[k] || EVX.rw;
const evxLow = () => reduced || !!G.lowFx || (typeof WEAK !== "undefined" && WEAK);
const evxDay = T => Date.UTC(new Date(T).getUTCFullYear(), new Date(T).getUTCMonth(), new Date(T).getUTCDate() + 1);
/* when: [live, the end or the start] */
function evxWhen(k, T) { try {
  if (k === "gw") { const i = gwIdx(T), l = gwLive(T); return [l, l ? gwEnd(i) : gwStart(i + 1)]; }
  if (k === "cube") { const l = evActive(T); return [l, l ? evStart(evWeek(T)) + EV_DUR : evStart(evWeek(T) + 1)]; }
  if (k === "sboss" || k === "tboss" || k === "eboss") { const g = k === "eboss" ? 3 : k === "tboss" ? 2 : 1, l = wbGroupOn(g, T); return [l, l ? wbGroupEnd(g, T) : wbGroupNext(g, T)]; }
  if (k === "conq") { const d = new Date(T), dw = (d.getUTCDay() + 6) % 7; return [false, Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - dw + 7)]; }
  if (k === "rw") return [false, evxDay(T)];
} catch (e) {} return [false, 0]; }
const evxRwCount = () => EVX_DAILY.reduce((a, [k]) => a + (k === "gifts" && !myAlly() ? 0 : evCount(k)), 0);
function evxShelf(VIS, k, T) {
  const card = (key, n, ic, big) => { const [live, at] = evxWhen(key, T), c = key === "rw" ? evxRwCount() : evCount(key), X = evxEl(key), sub = at ? `<small${live ? ' class="lv"' : ""}>${live ? "● ends " : key === "rw" ? "resets " : "in "}<b data-end="${at}">${ftime(at - T)}</b></small>` : key === "pass" ? `<small>Tier ${Math.min(VP_TIERS, Math.floor(vpState(T).xp / VP_XP))}/${VP_TIERS}</small>` : "";
    return `<button class="evcard evx-card ec-${key}${key === k ? " on" : ""}${live ? " live" : ""}${big ? " big" : ""}" data-el="${X.el}" style="--x1:${X.c1};--x2:${X.c2}" data-act="evPick" data-v="${key}"><span class="eci">${ic}</span><span class="ecn">${esc(n)}</span>${sub}${c ? `<i class="ecb">${c}</i>` : ""}</button>`; };
  const ev = VIS.filter(e => EVX[e[0]]), live = ev.filter(e => evxWhen(e[0], T)[0]), rest = ev.filter(e => !evxWhen(e[0], T)[0]);
  return `<div class="evchips evhub">${live.length ? `<span class="evx-lab live">Live now</span>${live.map(e => card(e[0], e[1], e[2], 1)).join("")}` : ""}<span class="evx-lab">Seasons &amp; rankings</span>${rest.map(e => card(e[0], e[1], e[2])).join("")}<span class="evx-lab">Daily</span>${card("rw", "Daily Rewards", "✹", 0)}</div>`; }
/* the next reward, in one line */
function evxNudge(k, T, mt) { try {
  if (k === "pass") { const v = vpState(T), lv = Math.floor(v.xp / VP_XP); return lv >= VP_TIERS ? "Every tier reached. More XP fills Void Caches." : `<b>${fmt((lv + 1) * VP_XP - v.xp)} XP</b> to tier ${lv + 1}`; }
  if (k === "rw") { const n = evxRwCount(); return n ? `<b>${n} reward${n > 1 ? "s" : ""}</b> ready to collect` : "All collected. New rewards at 00:00 UTC."; }
  if (mt && mt.nx) return `<b>${fmt(mt.nx[0] - mt.pts)} ${esc(mt.unit)}</b> to your next reward${mt.ready ? ` · <em>${mt.ready} ready</em>` : ""}`;
  if (mt && mt.ready) return `<em>${mt.ready} reward${mt.ready > 1 ? "s" : ""} ready to claim</em>`;
} catch (e) {} return ""; }
function evxHow(k) { const H = EV_HOW[k]; if (!H) return ""; const X = evxEl(k), [gl, ga, gd] = H.go, da = Object.entries(gd).map(([a, b]) => ` data-${a}="${esc(String(b))}"`).join("");
  return `<div class="evx-how" style="--x1:${X.c1};--x2:${X.c2}"><div class="evx-steps">${H.s.map(([ic, t, x], i) => `<div class="evx-step" style="--i:${i}"><span class="evx-sn">${i + 1}</span><span class="evx-si">${ic}</span><div><b>${esc(t)}</b><p>${esc(x)}</p></div></div>`).join("")}</div>
    <button class="btn amber wide evx-go" data-act="${ga}"${da}>${esc(gl)} ›</button>
    <h4 class="evx-h4">What earns points</h4><div class="evx-pts">${H.p.map(([a, b]) => `<div><span>${esc(a)}</span><b>${esc(b)}</b></div>`).join("")}</div>
    <button class="evx-tip" data-act="evxTip" data-k="${k}"><i class="evx-face" style="background-image:url('${advArt()}')"></i><span><small>${ADV} · tip</small>${esc(H.tip)}</span><u>🔊</u></button></div>`; }
function evxDailyBody(inline) { const E = evState(), keep = [E.ev, E.evTab]; let out = "";
  for (const [key, n, ic] of EVX_DAILY) { if (key === "gifts" && !myAlly()) continue; E.ev = key; E.evTab = "ov"; let P = null; try { P = shEvents0(inline, true); } catch (e) {} if (!P || P.k !== key) continue; const c = evCount(key);
    out += `<section class="evx-sec${c ? " rd" : ""}"><h3><span>${ic}</span>${esc(n)}${c ? `<i class="ecb">${c}</i>` : ""}</h3>${P.body || ""}${(P.claim || "").replace('class="btn amber evclaim" data-act="achOpen"', 'class="btn amber" data-act="achOpen"')}</section>`; } /* Achievements' button is not a claim */
  E.ev = keep[0]; E.evTab = keep[1]; return out; }
function shEvents(inline) {
  const T = now(), E = evState();
  if (EVX_DAILY.some(e => e[0] === E.ev)) E.ev = "rw"; /* the daily rewards live on one page now */
  let k = E.ev, P = null; if (k !== "rw") { G.mtLast = null; P = shEvents0(inline, true); k = P.k; }
  S.evHow = S.evHow || {}; if (!S.evHow[k]) { S.evHow[k] = 1; dirty(); if (E.evTab !== "rk") E.evTab = "how"; }
  const tab = E.evTab === "rk" && EVX_RANK.has(k) ? "rk" : E.evTab === "how" ? "how" : "ov", X = evxEl(k), VIS = P ? P.VIS : EVS.filter(e => (e[0] !== "gifts" || myAlly()) && evShow(e[0], T));
  const tabs = `<div class="evtabs evx-tabs${inline ? " ev3" : ""}"><button class="${tab === "how" ? "on" : ""}" data-act="evTab" data-v="how">How to Play</button><button class="${tab === "ov" ? "on" : ""}" data-act="evTab" data-v="ov">Rewards</button>${EVX_RANK.has(k) ? `<button class="${tab === "rk" ? "on" : ""}" data-act="evTab" data-v="rk">Ranking</button>` : ""}${inline ? `<button data-act="hubTab" data-v="rk">🏆 Board</button>` : ""}</div>`;
  let body, claim = "", hero;
  if (k === "rw") { const at = evxDay(T), n = evxRwCount(); hero = `<div class="evban evx-rwbn"><span class="evt">Daily Rewards</span><span class="evend">Resets in: <b data-end="${at}">${ftime(at - T)}</b></span><span class="evx-rwn">${n ? `${n} ready` : "All collected"}</span></div>`;
    body = tab === "how" ? evxHow("rw") : evxDailyBody(inline); }
  else { hero = evBanner(k, T); body = tab === "how" ? (evxHow(k) || P.body) : P.body; claim = P.claim; }
  const ng = evxNudge(k, T, G.mtLast), [live] = evxWhen(k, T);
  return `<div class="evx" data-el="${X.el}" style="--x1:${X.c1};--x2:${X.c2}">${inline ? "" : `<div class="hd evhd"><div><h2>Events</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`}${evxShelf(VIS, k, T)}<div class="evx-hero${live ? " live" : ""}"><canvas class="evx-fx" aria-hidden="true"></canvas>${hero}<i class="evx-sweep"></i></div>${ng ? `<div class="evx-nudge">${ng}</div>` : ""}${tabs}<div class="evx-body t-${tab}">${body || ""}</div>${claim ? `<div class="evx-claim">${claim}</div>` : ""}</div>`; }
setTimeout(() => Object.assign(ACT, { /* after ACT exists */
  evxTip: d => { const H = EV_HOW[d.k]; if (!H) return; if (voiceHas(H.tip)) { try { speak(H.tip); } catch (e) {} } else { try { advHolo(H.tip); } catch (e) {} } },
  evxGo: d => { const g = d.k === "eboss" ? 3 : d.k === "tboss" ? 2 : 1, T = now(); let key = null; try { key = wbMain(g).find(x => wbOn(x, T) && WBO[x]); } catch (e) {}
    if (key) ACT.wboss({ id: key }); else { evState().evTab = "ov"; sheet && sheet.type === "events" ? renderSheet() : render(true); toast("It isn't here yet. The countdown says when it arrives.", "info"); } } }), 0);
/* the particles: one canvas per page, its own element */
const EVX_FX = { t: 0, raf: 0 };
function evxFx() { if (EVX_FX.raf) return; const step = ts => { EVX_FX.raf = 0; const cv = document.querySelector(".evx-fx"); if (!cv || !cv.isConnected || document.hidden) return;
    EVX_FX.raf = requestAnimationFrame(step); if (ts - EVX_FX.t < 33) return; const dt = Math.min(80, ts - (EVX_FX.t || ts)) / 1000; EVX_FX.t = ts;
    const host = cv.closest(".evx"), el = host ? host.dataset.el : "stars", r = cv.parentNode.getBoundingClientRect(), W = Math.max(10, r.width | 0), H = Math.max(10, r.height | 0);
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; cv._p = null; }
    const x = cv.getContext("2d"), n = evxLow() ? 14 : 42, R = Math.random, c1 = getComputedStyle(host).getPropertyValue("--x1").trim() || "#ffd36b", c2 = getComputedStyle(host).getPropertyValue("--x2").trim() || "#fff";
    if (!cv._p || cv._el !== el) { cv._el = el; cv._p = Array.from({ length: n }, () => ({ x: R() * W, y: R() * H, v: R(), a: R() * 6.28, l: R() })); }
    x.clearRect(0, 0, W, H); x.globalCompositeOperation = "lighter";
    for (const p of cv._p) { p.l += dt * (.25 + p.v * .35);
      if (el === "fire") { p.y -= dt * (30 + p.v * 50); p.x += Math.sin(p.l * 6 + p.a) * dt * 14; if (p.y < -6) { p.y = H + 4; p.x = R() * W; } const s = 1.2 + p.v * 2.4, f = .5 + .5 * Math.sin(p.l * 20 + p.a); x.fillStyle = f > .5 ? c1 : c2; x.globalAlpha = .35 + .5 * f * (p.y / H); x.beginPath(); x.arc(p.x, p.y, s, 0, 6.28); x.fill(); }
      else if (el === "war") { p.x += dt * (160 + p.v * 200); p.y += dt * (60 + p.v * 60); if (p.x > W + 20 || p.y > H + 20) { p.x = -20 + R() * W * .6; p.y = -10; } x.strokeStyle = p.v > .6 ? c2 : c1; x.globalAlpha = .55; x.lineWidth = 1 + p.v; x.beginPath(); x.moveTo(p.x, p.y); x.lineTo(p.x - 10 - p.v * 10, p.y - 4 - p.v * 4); x.stroke(); }
      else if (el === "circuit") { const hz = p.a > 3.14; if (hz) p.x += dt * (40 + p.v * 60); else p.y += dt * (30 + p.v * 50); if (p.x > W + 4 || p.y > H + 4) { p.x = hz ? -4 : Math.round(R() * W / 18) * 18; p.y = hz ? Math.round(R() * H / 18) * 18 : -4; } x.fillStyle = c1; x.globalAlpha = .7; x.fillRect(p.x - 1.5, p.y - 1.5, 3, 3); x.globalAlpha = .18; x.fillRect(hz ? p.x - 24 : p.x - .5, hz ? p.y - .5 : p.y - 24, hz ? 24 : 1, hz ? 1 : 24); }
      else if (el === "toxic") { p.x += Math.sin(p.l + p.a) * dt * 10; p.y -= dt * (6 + p.v * 8); if (p.y < -30) { p.y = H + 30; p.x = R() * W; } const rr = 14 + p.v * 26, g = x.createRadialGradient(p.x, p.y, 0, p.x, p.y, rr); g.addColorStop(0, c1); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.globalAlpha = .12 + .08 * Math.sin(p.l * 2); x.fillRect(p.x - rr, p.y - rr, rr * 2, rr * 2); }
      else if (el === "void") { const cx = W * .5, cy = H * .45, dx = p.x - cx, dy = p.y - cy, d = Math.hypot(dx, dy) || 1; p.x += (-dy / d * 40 - dx / d * 14) * dt * (.6 + p.v); p.y += (dx / d * 40 - dy / d * 14) * dt * (.6 + p.v); if (d < 8) { const a = R() * 6.28, rr = Math.max(W, H) * .6; p.x = cx + Math.cos(a) * rr; p.y = cy + Math.sin(a) * rr; } x.fillStyle = p.v > .5 ? c2 : c1; x.globalAlpha = .3 + .5 * Math.min(1, 40 / d); x.beginPath(); x.arc(p.x, p.y, 1 + p.v * 1.6, 0, 6.28); x.fill(); }
      else if (el === "banner") { p.x += dt * (50 + p.v * 90); if (p.x > W + 40) { p.x = -40; p.y = R() * H; } const g = x.createLinearGradient(p.x - 40, 0, p.x, 0); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, p.v > .5 ? c2 : c1); x.strokeStyle = g; x.globalAlpha = .45; x.lineWidth = 1 + p.v * 1.5; x.beginPath(); x.moveTo(p.x - 40, p.y); x.lineTo(p.x, p.y); x.stroke(); }
      else { p.y -= dt * (6 + p.v * 12); if (p.y < -4) { p.y = H + 4; p.x = R() * W; } const tw = .5 + .5 * Math.sin(p.l * 5 + p.a), s = .8 + p.v * 1.8; x.fillStyle = tw > .7 ? "#fff" : c1; x.globalAlpha = .25 + .65 * tw; x.beginPath(); x.moveTo(p.x, p.y - s * 2.2); x.lineTo(p.x + s * .5, p.y); x.lineTo(p.x, p.y + s * 2.2); x.lineTo(p.x - s * .5, p.y); x.closePath(); x.fill(); x.beginPath(); x.moveTo(p.x - s * 2.2, p.y); x.lineTo(p.x, p.y + s * .5); x.lineTo(p.x + s * 2.2, p.y); x.lineTo(p.x, p.y - s * .5); x.closePath(); x.fill(); } }
    x.globalAlpha = 1; x.globalCompositeOperation = "source-over"; };
  EVX_FX.t = 0; EVX_FX.raf = requestAnimationFrame(step); }
/* after each draw: start the particles, mark the last hour's countdowns, and say how far the next place is */
const evxUnfmt = s => { const m = String(s).replace(/,/g, "").match(/([\d.]+)\s*([KMB])?/i); if (!m) return NaN; return +m[1] * ({ k: 1e3, m: 1e6, b: 1e9 }[(m[2] || "").toLowerCase()] || 1); };
function evxPost() { try { if (!document.querySelector(".evx")) return; evxFx(); const T = Date.now();
  document.querySelectorAll(".evx [data-end]").forEach(b => { const left = +b.dataset.end - T; b.classList.toggle("evx-hot", left > 0 && left < 3600e3); });
  const me = document.querySelector(".evx .evrank .evrr.me"); if (me && !document.querySelector(".evx-climb")) { const rows = [...me.parentNode.querySelectorAll(".evrr")], i = rows.indexOf(me);
    if (i > 0) { const up = rows[i - 1], a = evxUnfmt((me.lastElementChild || {}).textContent), b = evxUnfmt((up.lastElementChild || {}).textContent);
      if (isFinite(a) && isFinite(b) && b >= a) { const d = document.createElement("div"); d.className = "evx-climb"; d.innerHTML = `⬆ <b>${fmt(Math.max(1, Math.ceil(b - a + (b === a ? 1 : 0))))}</b> to pass #${i}`; me.parentNode.insertBefore(d, rows[0]); } }
    else if (i === 0) { const d = document.createElement("div"); d.className = "evx-climb top"; d.innerHTML = "👑 You're in first place. Hold it."; me.parentNode.insertBefore(d, rows[0]); } } } catch (e) {} }
setInterval(evxPost, 600); document.addEventListener("visibilitychange", () => { if (!document.hidden) evxFx(); });
/* the styles */
{ const st = document.createElement("style"); st.textContent = `
.evx{--x1:#ffd36b;--x2:#fff}
.evx .evchips.evhub{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:8px;padding:4px 2px 10px;scrollbar-width:none;align-items:stretch}.evx .evchips.evhub::-webkit-scrollbar{display:none}
.evx-lab{flex:0 0 auto;writing-mode:vertical-rl;transform:rotate(180deg);font:700 9px/1 system-ui;letter-spacing:.16em;text-transform:uppercase;color:#7f97a9;align-self:center;padding:0 2px}.evx-lab.live{color:#ff6a6a}
.evx .evx-card{flex:0 0 auto;position:relative;min-width:84px;max-width:96px;display:flex;flex-direction:column;align-items:center;gap:3px;padding:9px 6px 8px;border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(0,0,0,.25));border:1px solid color-mix(in srgb,var(--x1) 30%,transparent);color:#e6eef5;transition:transform .15s}
.evx .evx-card .eci{font-size:20px;filter:drop-shadow(0 0 6px var(--x1));color:var(--x1)}.evx .evx-card .ecn{font-size:11px;font-weight:700;text-align:center;line-height:1.15}.evx .evx-card small{font-size:9.5px;color:#93a8b8;text-align:center}.evx .evx-card small.lv{color:#ff8a8a}
.evx .evx-card.on{background:linear-gradient(180deg,color-mix(in srgb,var(--x1) 28%,transparent),rgba(0,0,0,.3));border-color:var(--x1);box-shadow:0 0 16px color-mix(in srgb,var(--x1) 45%,transparent),inset 0 0 12px color-mix(in srgb,var(--x1) 25%,transparent);transform:translateY(-1px)}
.evx .evx-card.big{min-width:112px;max-width:124px;padding:12px 8px}.evx .evx-card.big .eci{font-size:26px}.evx .evx-card.live{animation:evxLive 2.2s ease-in-out infinite}
@keyframes evxLive{0%,100%{box-shadow:0 0 6px color-mix(in srgb,var(--x1) 35%,transparent)}50%{box-shadow:0 0 20px var(--x1),0 0 2px var(--x2) inset}}
.evx .evx-card .ecb{position:absolute;top:-4px;right:-4px;min-width:18px;height:18px;border-radius:9px;background:#ff4d6a;color:#fff;font:700 11px/18px system-ui;font-style:normal;box-shadow:0 0 10px #ff4d6a;animation:evxBadge 1.4s ease-in-out infinite}@keyframes evxBadge{50%{transform:scale(1.15)}}
.evx-hero{position:relative;border-radius:16px;overflow:hidden;margin:2px 0 8px;box-shadow:0 0 0 1px color-mix(in srgb,var(--x1) 35%,transparent),0 8px 30px rgba(0,0,0,.4)}.evx-hero.live{animation:evxLive 2.6s ease-in-out infinite}
.evx-fx{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:3;mix-blend-mode:screen}
.evx-sweep{position:absolute;inset:0;pointer-events:none;z-index:4;background:linear-gradient(105deg,transparent 35%,color-mix(in srgb,var(--x2) 22%,transparent) 48%,transparent 60%);background-size:250% 100%;animation:evxSweep 5.5s ease-in-out infinite}@keyframes evxSweep{0%{background-position:130% 0}55%,100%{background-position:-130% 0}}
.evx-hero [data-end]{color:var(--x2);text-shadow:0 0 8px var(--x1)}.evx [data-end].evx-hot{color:#ff6a6a;text-shadow:0 0 10px #ff2a3a;animation:evxHot 1s steps(2) infinite}@keyframes evxHot{50%{opacity:.6}}
.evx-rwbn{position:relative;min-height:110px;display:flex;flex-direction:column;justify-content:flex-end;gap:4px;padding:14px;background:radial-gradient(120% 140% at 80% 0%,color-mix(in srgb,var(--x1) 40%,#120d02),#05070c 70%)}.evx-rwbn .evt{font:800 22px/1.1 system-ui;color:#fff;text-shadow:0 0 14px var(--x1)}.evx-rwbn .evend{font-size:12px;color:#c9d6e0}.evx-rwn{position:absolute;top:12px;right:12px;padding:4px 10px;border-radius:12px;background:color-mix(in srgb,var(--x1) 25%,transparent);border:1px solid var(--x1);font:700 11px system-ui;color:var(--x2)}
.evx-nudge{margin:0 0 8px;padding:9px 12px;border-radius:12px;font-size:13px;color:#dfe8ef;background:linear-gradient(90deg,color-mix(in srgb,var(--x1) 22%,transparent),transparent);border-left:3px solid var(--x1)}.evx-nudge b{color:var(--x2);text-shadow:0 0 8px var(--x1)}.evx-nudge em{color:#ffd36b;font-style:normal;font-weight:700}
.evx .evx-tabs button{font-size:12px;padding-left:4px;padding-right:4px;white-space:nowrap;overflow:hidden;text-overflow:clip}.evx-body.t-how+.evx-claim:has(.btn[disabled]){display:none}
.evx .evx-tabs button.on{box-shadow:inset 0 -2px 0 var(--x1),0 0 12px color-mix(in srgb,var(--x1) 30%,transparent);color:#fff}
.evx-how{display:flex;flex-direction:column;gap:10px;padding:4px 0 8px}.evx-steps{display:flex;flex-direction:column;gap:8px}
.evx-step{display:flex;gap:10px;align-items:flex-start;padding:11px 12px;border-radius:14px;background:linear-gradient(90deg,color-mix(in srgb,var(--x1) 14%,transparent),rgba(255,255,255,.02));border:1px solid color-mix(in srgb,var(--x1) 25%,transparent);animation:evxIn .5s ease both;animation-delay:calc(var(--i)*90ms)}@keyframes evxIn{from{opacity:0;transform:translateY(8px)}}
.evx-sn{flex:0 0 22px;height:22px;border-radius:11px;display:grid;place-items:center;font:800 12px system-ui;color:#05070c;background:var(--x1);box-shadow:0 0 10px var(--x1)}.evx-si{font-size:22px;filter:drop-shadow(0 0 6px var(--x1))}.evx-step b{display:block;font-size:14px;color:#fff}.evx-step p{margin:2px 0 0;font-size:12.5px;line-height:1.4;color:#b9c8d4}
.evx-go{box-shadow:0 0 18px color-mix(in srgb,var(--x1) 45%,transparent)}.evx-h4{margin:6px 2px 0;font:700 11px system-ui;letter-spacing:.12em;text-transform:uppercase;color:#8ea4b5}
.evx-pts{display:flex;flex-direction:column;border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,.07)}.evx-pts div{display:flex;justify-content:space-between;gap:10px;padding:8px 12px;font-size:12.5px;color:#cfdbe4;background:rgba(255,255,255,.025)}.evx-pts div:nth-child(2n){background:rgba(255,255,255,.045)}.evx-pts b{color:var(--x2);text-shadow:0 0 6px var(--x1);white-space:nowrap}
.evx-tip{display:flex;gap:10px;align-items:center;text-align:left;width:100%;padding:10px 12px;border-radius:14px;background:rgba(10,16,26,.7);border:1px solid color-mix(in srgb,var(--x1) 35%,transparent);color:#e7eef4;font-size:13px;line-height:1.35}.evx-tip small{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--x1)}.evx-tip u{text-decoration:none;margin-left:auto;font-size:16px}
.evx-face{flex:0 0 40px;height:40px;border-radius:20px;background-size:cover;background-position:50% 18%;box-shadow:0 0 0 2px var(--x1),0 0 12px var(--x1)}
.evx-claim{position:sticky;bottom:8px;z-index:6;padding-top:8px}.evx-claim .btn.amber{box-shadow:0 0 22px rgba(255,190,70,.55);animation:evxClaim 1.6s ease-in-out infinite}@keyframes evxClaim{50%{box-shadow:0 0 34px rgba(255,200,90,.9)}}
.evx-sec{margin:0 0 12px;padding:10px;border-radius:14px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06)}.evx-sec.rd{border-color:color-mix(in srgb,var(--x1) 55%,transparent);box-shadow:0 0 14px color-mix(in srgb,var(--x1) 22%,transparent)}.evx-sec h3{display:flex;align-items:center;gap:8px;margin:2px 2px 8px;font-size:15px;color:#fff}.evx-sec h3 span{color:var(--x1);filter:drop-shadow(0 0 5px var(--x1))}.evx-sec h3 .ecb{margin-left:auto;font-style:normal;min-width:20px;height:20px;border-radius:10px;background:#ff4d6a;color:#fff;font-size:11px;display:grid;place-items:center}.evx-sec .evc{margin:0;border:0;background:none;padding:0}
.evx .mtrk-bar i{background:linear-gradient(90deg,var(--x1),var(--x2),var(--x1));background-size:200% 100%;box-shadow:0 0 12px var(--x1);animation:evxFlow 2.4s linear infinite}@keyframes evxFlow{to{background-position:-200% 0}}
.evx .mtrk-bar u.on{background:var(--x2);box-shadow:0 0 10px var(--x1)}.evx .mcrd.ready{border-color:#ffd36b;animation:evxReady 1.5s ease-in-out infinite}@keyframes evxReady{50%{box-shadow:0 0 22px rgba(255,211,107,.55)}}
.evx .mcrd.next{position:relative;overflow:hidden;border-color:color-mix(in srgb,var(--x1) 60%,transparent)}.evx .mcrd.next::after,.evx .mcrd.lock:nth-last-child(-n+2)::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(105deg,transparent 40%,color-mix(in srgb,var(--x2) 18%,transparent) 50%,transparent 60%);background-size:250% 100%;animation:evxSweep 3.6s ease-in-out infinite}.evx .mcrd.lock:nth-last-child(-n+2){position:relative;overflow:hidden}
.evx .evrank .evrr:nth-child(2),.evx .evrank .evrr:nth-child(3),.evx .evrank .evrr:nth-child(4){font-weight:700;font-size:14px}
.evx .evrank .evrr:nth-child(2){background:linear-gradient(90deg,rgba(255,211,107,.25),transparent);box-shadow:inset 3px 0 0 #ffd36b}.evx .evrank .evrr:nth-child(3){background:linear-gradient(90deg,rgba(210,225,240,.18),transparent);box-shadow:inset 3px 0 0 #d6e2ee}.evx .evrank .evrr:nth-child(4){background:linear-gradient(90deg,rgba(214,140,80,.2),transparent);box-shadow:inset 3px 0 0 #d68c50}
.evx .evrank .evrr.me{background:linear-gradient(90deg,color-mix(in srgb,var(--x1) 30%,transparent),transparent)!important;box-shadow:inset 3px 0 0 var(--x1),0 0 14px color-mix(in srgb,var(--x1) 35%,transparent);animation:evxMe 2s ease-in-out infinite}@keyframes evxMe{50%{box-shadow:inset 3px 0 0 var(--x2),0 0 22px color-mix(in srgb,var(--x1) 55%,transparent)}}
.evx-climb{margin:4px 0 8px;padding:8px 12px;border-radius:10px;font-size:12.5px;color:#e6eef4;background:color-mix(in srgb,var(--x1) 18%,transparent);border:1px solid color-mix(in srgb,var(--x1) 45%,transparent)}.evx-climb b{color:var(--x2)}
.evx .cal .cd.done{background:linear-gradient(180deg,rgba(255,140,40,.28),rgba(255,80,20,.08));border-color:rgba(255,150,60,.6);box-shadow:0 0 10px rgba(255,120,30,.35)}.evx .cal .cd.done::after{content:"🔥";position:absolute;top:-7px;right:-5px;font-size:12px;filter:drop-shadow(0 0 4px #ff7a1a)}.evx .cal .cd{position:relative}.evx .cal .cd.now{animation:evxReady 1.3s ease-in-out infinite;border-color:#ffd36b}
@media (prefers-reduced-motion:reduce){.evx *{animation:none!important}}
`; document.head.appendChild(st); }
