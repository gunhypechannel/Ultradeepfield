/* ---------- v820 one voice at a time (owner video: on login the hologram read a lore line, the full-screen portrait held the screen
   on a story line and a toast followed, all over the open Events page; "Building all"). Every unprompted line now goes through one
   queue: a line that answers what you just tapped still shows at once; anything else waits for a calm moment (the map, nothing open,
   20 s after login, 20 s since the last one), shows as a slim banner, and is kept in the Advisor log. Story beats keep the full
   portrait, once, at a calm moment. Login opens with one Welcome back card. Settings: Advisor chatter All / Important / Off. ---------- */
G.tapAt = 0; for (const ev of ["pointerdown", "keydown"]) document.addEventListener(ev, () => { G.tapAt = Date.now(); }, true);
const advTapped = () => Date.now() - (G.tapAt || 0) < 2500, advMode = () => (S && S.advCh) || "imp", ADVQ = { q: [], last: 0 };
setInterval(() => { if (typeof G !== "undefined" && G.ready && !G.readyAt) G.readyAt = Date.now(); }, 400);
const advQuietOver = () => !!G.readyAt && Date.now() - G.readyAt > 20000;
const advFilming = () => !!(G.cineOn || (typeof G3 !== "undefined" && G3 && G3.cam && G3.cam.cine));
function advCalm() { return G.ready && advQuietOver() && !tutOn() && !battle && !sheet && !advLines && !$("#adv") && !$("#celeb") && !$("#wback") && !$("#advh.on") && !$("#advbar.on") && !advFilming() && !document.hidden && Date.now() - ADVQ.last > 20000; }
function advCalmSay() { return G.ready && advQuietOver() && !sheet && !battle && !advFilming() && !$("#celeb") && !$("#wback"); }
function advLog(line, kind) { if (!S || !line) return; S.advLog = S.advLog || []; const i = S.advLog.findIndex(x => x.l === line); if (i >= 0) S.advLog.splice(i, 1);
  S.advLog.unshift({ t: now(), l: line, k: kind || "note", u: 1 }); if (S.advLog.length > 40) S.advLog.length = 40; dirty(); advBadge(); }
/* pri 2: live events and milestones (shown on Important); 1: tips, lore, news, battle remarks (shown on All); 0: chatter (log only) */
function advQueue(line, pri, kind) { advLog(line, kind); const m = advMode(); if (m === "off" || (m === "imp" && pri < 2) || pri < 1) return; if (ADVQ.q.some(x => x.l === line)) return;
  ADVQ.q.push({ l: line, p: pri, at: Date.now() }); ADVQ.q.sort((a, b) => b.p - a.p || a.at - b.at); if (ADVQ.q.length > 4) ADVQ.q.length = 4; }
function advBar(line) { ADVQ.last = Date.now(); let b = $("#advbar");
  if (!b) { b = document.createElement("div"); b.id = "advbar"; b.setAttribute("role", "button"); b.setAttribute("aria-live", "polite"); b.dataset.act = "advLogOpen"; b.innerHTML = `<img alt=""><span></span><i aria-hidden="true">›</i>`; $("#app").appendChild(b); }
  b.querySelector("img").src = advArt(); b.querySelector("span").textContent = line; b.classList.add("on"); try { speak(line); } catch (e) {}
  const u = (S.advLog || []).find(x => x.l === line); if (u && u.u) { u.u = 0; dirty(); } advBadge();
  clearTimeout(G.advBarT); G.advBarT = setTimeout(() => { const x = $("#advbar"); if (x) x.classList.remove("on"); }, Math.max(5500, line.length * 65)); }
setInterval(() => { try { if (!S) return; const T = Date.now(); ADVQ.q = ADVQ.q.filter(x => T - x.at < 10 * 60e3); if (ADVQ.q.length && advCalm()) advBar(ADVQ.q.shift().l); advBadge(); } catch (e) {} }, 1000);
/* the log: a chip with her face and the unread count, on the map only */
function advBadge() { try { const n = ((S && S.advLog) || []).filter(x => x.u).length; let c = $("#advlogb"); const show = n > 0 && G.ready && !sheet && !battle && !advFilming() && !$("#adv") && !$("#wback") && !tutOn();
    if (!c && !show) return; if (!c) { c = document.createElement("button"); c.id = "advlogb"; c.dataset.act = "advLogOpen"; c.setAttribute("aria-label", "Advisor log"); c.innerHTML = `<img alt=""><b></b>`; $("#app").appendChild(c); }
    c.classList.toggle("on", show); if (show) { c.querySelector("img").src = advArt(); c.querySelector("b").textContent = n > 9 ? "9+" : n; } } catch (e) {} }
const advChSeg = () => `<span class="advseg" role="group" aria-label="Advisor chatter">${[["all", "All"], ["imp", "Important"], ["off", "Off"]].map(([v, l]) => `<button class="${advMode() === v ? "on" : ""}" data-act="advChSet" data-v="${v}" aria-pressed="${advMode() === v}">${l}</button>`).join("")}</span>`;
const advChRow = () => `<div class="tgl advchr"><span>Advisor chatter<small>${advMode() === "all" ? "Tips, lore and news as they come" : advMode() === "imp" ? "Live events and milestones; the rest waits in her log" : "Only story moments; the rest waits in her log"}</small></span>${advChSeg()}</div><button class="btn ghost sm advlogbtn" data-act="advLogOpen">Advisor log${((S && S.advLog) || []).some(x => x.u) ? " •" : ""}</button>`;
function shAdvLog() { const L = (S.advLog || []);
  const h = `<div class="hd"><div><div class="chapter">${ADV}</div><h2>Advisor log</h2><p class="note">What she noticed while you were busy. Tap a line to hear it again.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="card">${advChRow()}</div>
    <div class="card advlog">${L.length ? L.map((x, i) => `<button class="alrow${x.u ? " new" : ""}" data-act="advLogSay" data-i="${i}"><small>${{ live: "Live", lore: "Archives", news: "News", note: "Note", greet: "Greeting" }[x.k] || "Note"} · ${ago(x.t)}</small><span>${esc(x.l)}</span></button>`).join("") : '<p class="note">Nothing yet.</p>'}</div>`;
  if (L.some(x => x.u)) { L.forEach(x => { x.u = 0; }); dirty(); } setTimeout(advBadge, 0); return h; }
/* the welcome card: one card on login instead of a greeting, an online-bonus toast and a lore line */
function advWelcome() { try { if (G.wbDone || !S || !S.intro || tutOn() || battle || advFilming() || $("#adv") || $("#celeb")) return; G.wbDone = 1;
    let n = 0; const rows = []; for (const e of EVS) { const c = evCount(e[0]); if (c > 0) { n += c; if (rows.length < 3) rows.push(`<li><i>${e[2]}</i>${esc(e[1])}<b>${c}</b></li>`); } }
    const m = obMin(), got = (S.online && S.online.got) || [], nx = OB_T.find(([t], i) => t > m && !got.includes(i)), away = G.awayMs || 0;
    if (!n && away < 30 * 60e3) return;
    const line = G.wbGreet || (away >= 3 * 864e5 ? "You're back, Commander. I kept the lights on." : "Welcome back, Commander.");
    const w = document.createElement("div"); w.id = "wback"; w.setAttribute("role", "dialog"); w.setAttribute("aria-label", "Welcome back");
    w.innerHTML = `<div class="wbbox"><img class="wbav" src="${advArt()}" alt=""><div class="wbtx"><small>${ADV}</small><p>${esc(line)}</p>
      ${n ? `<ul>${rows.join("")}</ul>` : ""}${nx ? `<div class="wbob">⏱ Online bonus: next reward in ${obLabel(Math.max(1, nx[0] - m))}</div>` : ""}
      <div class="wbbt">${n ? `<button class="btn amber sm" data-act="wbGo">🎁 ${n} ready in Events</button>` : ""}<button class="btn ghost sm" data-act="wbX">${n ? "Later" : "Thanks"}</button></div></div></div>`;
    $("#app").appendChild(w); advLog(line, "greet"); try { speak(line); } catch (e) {} ADVQ.last = Date.now(); clearTimeout(G.wbT); G.wbT = setTimeout(() => { const x = $("#wback"); if (x) x.remove(); advBadge(); }, 22000); } catch (e) {} }
setInterval(() => { try { if (G.ready && G.readyAt && !G.wbDone && Date.now() - G.readyAt > 9000) { if (Date.now() - G.readyAt > 60000) G.wbDone = 1; else advWelcome(); } } catch (e) {} }, 1000);
Object.assign(AET_ACT, {
  advLogOpen: () => { const b = $("#advbar"); if (b) b.classList.remove("on"); openSheet({ type: "advlog" }); },
  advLogSay: d => { const x = (S.advLog || [])[+d.i]; if (x) { try { speak(x.l); } catch (e) {} } },
  advChSet: d => { S.advCh = d.v; dirty(); ADVQ.q = ADVQ.q.filter(x => d.v === "all" || (d.v === "imp" && x.p >= 2)); if (sheet) renderSheet(); else render(true); },
  wbGo: () => { const x = $("#wback"); if (x) x.remove(); openSheet({ type: "events" }); },
  wbX: () => { const x = $("#wback"); if (x) x.remove(); advBadge(); } });
/* the gates on her two ways of speaking */
{ const base = advHolo; advHolo = function (line, force) { if (!line) return;
    if (force === "arch") return G.archRd ? base(line, force) : advLog(line, "lore"); /* reading in the Archives: at once; otherwise to the log */
    if (tutOn() || advTapped() || G.advPass) return base(line, force); /* a reply to what you just did */
    advQueue(line, force === 1 ? 2 : 1, force === 1 ? "live" : "note"); }; }
{ const base = say; say = function (lines) { if (!lines || !lines.length || G.sayPass || tutOn() || !S || !S.intro || G.advThen || $("#adv") || advTapped()) return base(lines);
    if (!advCalmSay()) { for (const l of lines) if (l && !S.say.includes(l)) S.say.push(l); dirty(); return; } /* a story beat waits for the map, then plays once */
    return base(lines); }; }
