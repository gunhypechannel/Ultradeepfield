/* ---------- v622 the Glyph Wheel, reworked (owner: "What can make the lottery wheel better and more addictive? It also definitely needs
   better sound effects" ... "Do it all"). Recorded sounds the owner picked (docs/sfx/w_*.mp3), a buzz on each peg and on the landing,
   an honest slow crawl over the last pegs only when the real result is rare or a jackpot, a 7-day streak (day 7's free spin is a
   guaranteed rare prize), a lucky meter (each plain spin lifts the rare odds 10%, up to x2.5; the 31st plain spin is a sure rare), a
   weekly set of five glyphs (◆40), one Lucky Hour a day (jackpot odds doubled), and a shared jackpot pot fed by everyone's spins
   (a Jackpot takes half, a Mega Jackpot all of it; shown only when the server answers). Nothing here is sold for real money. ---------- */
const WHL_RARE = W => !!W.jack || W.w <= 2.5;
const whlDay = () => Math.round(shopDayEnd() / 864e5);
const WHL_SET_PAY = 40, WHL_LK_MAX = 30;
const WSND = { lever: 1.23, spin: 1.1, tick: 1.15, land: 1.15, win: 1.3, rare: 1.3, jack: 1.2, mega: 1.2 }, WBUF = {};
function wsLoad() { if (!AU.ctx || WBUF._l) return; WBUF._l = 1; for (const k in WSND) fetch(`sfx/w_${k}.mp3?v=622`).then(r => r.ok ? r.arrayBuffer() : null).then(ab => ab && new Promise((ok, no) => AU.ctx.decodeAudioData(ab, ok, no))).then(b => { if (b) WBUF[k] = b; }).catch(() => {}); }
function wsPlay(k, at, gain, rate) { if (!WSFX.ok()) return true; const b = WBUF[k]; if (!b) return false; const c = AU.ctx, s = c.createBufferSource(), g = c.createGain(); s.buffer = b; s.playbackRate.value = rate || 1; g.gain.value = WSND[k] * (gain || 1); s.connect(g); g.connect(AU.sfx); s.start(Math.max(c.currentTime, at || 0)); s.onended = () => { try { s.disconnect(); g.disconnect(); } catch (e) {} }; return true; }
const whlBuzz = p => { try { if (navigator.vibrate) navigator.vibrate(p); } catch (e) {} };
/* one Lucky Hour a day, at an hour picked by the day itself: returns when it ends, or 0 */
function whlHour(T = now()) { const end = shopDayEnd(), d0 = end - 864e5, h = hash("lh" + whlDay()) % 22 + 1, s = d0 + h * 3600e3; return T >= s && T < s + 3600e3 ? s + 3600e3 : 0; }
function whlW(W) { const lk = Math.min(15, S.whlLk || 0); return W.w * (WHL_RARE(W) ? 1 + .1 * lk : 1) * (W.jack && whlHour() ? 2 : 1); }
function whlPick(guar) { const pool = guar ? WHEEL.filter(WHL_RARE) : WHEEL; let r = Math.random() * pool.reduce((a, W) => a + whlW(W), 0); for (const W of pool) { r -= whlW(W); if (r < 0) return WHEEL.indexOf(W); } return WHEEL.indexOf(pool[pool.length - 1]); }
/* the streak as it stands today: days in a row the free spin was taken (a missed day breaks it) */
function whlStreak() { const d = whlDay(), st = S.whlStk || {}; return st.d === d || st.d === d - 1 ? st.n || 0 : 0; }
function whlGlyphs() { const wk = Math.floor(whlDay() / 7), cand = WHEEL.filter(W => W.w >= 4).map(W => W.g), set = []; let h = hash("gs" + wk); while (set.length < 5 && cand.length) { set.push(cand.splice(h % cand.length, 1)[0]); h = hash(String(h) + "x"); }
  const st = S.whlGs && S.whlGs.wk === wk ? S.whlGs : { wk, got: [], done: 0 }; return { set, got: st.got || [], done: st.done, wk }; }
function whlPotHTML(P) { const L = (P.last || [])[0]; return `<span>Shared pot</span><b class="gwpv">◆${fmt(P.pool | 0)}</b><small>${L ? `Last: ${esc(L.name)} ◆${fmt(L.amt)}, ${ago(L.at)}` : "Jackpot takes ½ · Mega all"}</small>`; }
function whlPotPaint() { const el = document.getElementById("gwpot"); if (!el || !G.whlPS) return; el.hidden = false; el.innerHTML = whlPotHTML(G.whlPS); }
function whlPotLoad(force) { try { if (!window.udfWheel || G.mode !== "online") return; if (!force && performance.now() - (G.whlPT || -1e9) < 30000) return whlPotPaint(); G.whlPT = performance.now(); window.udfWheel.state().then(j => { if (j && typeof j.pool === "number") { G.whlPS = j; whlPotPaint(); } }).catch(() => {}); } catch (e) {} }
function whlMeters() { const n = whlStreak(), lk = Math.min(WHL_LK_MAX, S.whlLk || 0), gs = whlGlyphs(), lh = whlHour(), P = G.whlPS;
  return `<div class="gwm">${lh ? `<div class="gwlh">✦ LUCKY HOUR · Jackpot odds ×2 · <b data-end="${lh}">${ftime(lh - now())}</b></div>` : ""}<div class="gwmg">
    <div class="gwc" title="Take your free spin every day: day 7's free spin lands a rare prize or better"><span>Daily streak</span><i class="gwdots">${[...Array(7)].map((_, i) => `<em class="${i < n ? "on" : ""}${i === 6 ? " big" : ""}"></em>`).join("")}</i><small>${n >= 6 ? (whlFree() ? "Today: a sure rare!" : "Tomorrow: a sure rare") : `Day ${n} of 7 · day 7 is a sure rare`}</small></div>
    <div class="gwc" title="Every spin without a rare prize raises the rare odds; when it's full, the next spin is a sure rare"><span>Lucky meter</span><i class="gwbar"><b style="width:${(lk / WHL_LK_MAX * 100).toFixed(0)}%"></b></i><small>${lk >= WHL_LK_MAX ? "Full: next spin is a sure rare" : `Rare ×${(1 + .1 * Math.min(15, lk)).toFixed(1)} · ${WHL_LK_MAX - lk} to a sure rare`}</small></div>
    <div class="gwc" title="Land all five of this week's glyphs for a bonus"><span>Weekly glyphs</span><i class="gwgl">${gs.set.map(g => `<em class="${gs.got.includes(g) ? "on" : ""}">${g}</em>`).join("")}</i><small>${gs.done ? "Set complete ✓" : `Land all five: ◆${WHL_SET_PAY}`}</small></div>
    <div class="gwc gwpot" id="gwpot" title="Every spin by anyone adds ◆1. A Jackpot takes half the pot, a Mega Jackpot all of it"${P ? "" : " hidden"}>${P ? whlPotHTML(P) : ""}</div></div></div>`; }
/* the Advisor calls Lucky Hour once a day, wherever you are in the game */
setInterval(() => { try { if (!S || !S.intro || G.cineOn || !whlHour()) return; const d = whlDay(); if (S.lhSaid === d) return; S.lhSaid = d; dirty(); advHolo("Lucky Hour on the Glyph Wheel, Commander. Jackpot odds are doubled for the next hour."); } catch (e) {} }, 45000);
