/* v615 (owner: "Build all except your first rival"): first-day goals with a countdown, a come-back-tomorrow teaser and its payoff,
   the signal log told one line a day with the daily login, the flagship seen (and lost) in the prologue, and quicker first jobs. */
const D1_MS = 864e5, D1_RW = { shards: 60, boosts: 5, item: "xb_gold" };
const D1_GOALS = [["Finish 10 Academy steps", () => S.tut && (S.tut.k === "done" || (S.tut.i | 0) >= 10)], ["Win 3 battles", () => vpStat("battlesWon") >= 3],
  ["Explore 2 pyramid stations", () => vpStat("pyramids") >= 2], ["Reach Commander Lv.5", () => cmdLevel(score()) >= 5], ["Join an alliance", () => !!myAlly() || G.mode !== "online"]];
const d1On = (T = now()) => !!(S && S.created && S.intro && !S.d1Done && T - S.created < D1_MS);
const d1Got = () => D1_GOALS.filter(g => { try { return g[1](); } catch (e) { return false; } }).length;
function d1HTML(T = now()) { if (!d1On(T)) return ""; const end = S.created + D1_MS, n = d1Got(), all = n >= D1_GOALS.length;
  return `<article class="card d1${all ? " hi" : ""}"><header><span>⏳ Your first day</span><b data-end="${end}">${ftime(end - T)}</b></header><p class="note">Finish all five before the clock runs out for ◆60, ⚡5 boosts, a ${esc(SHOP[D1_RW.item] ? SHOP[D1_RW.item].n : "rare crate")} and the title “First Light”.</p>
    ${D1_GOALS.map(([t, f]) => { let ok = false; try { ok = f(); } catch (e) {} return `<div class="vpm${ok ? " done" : ""}"><div><b>${esc(t)}</b></div><span>${ok ? "✓" : ""}</span></div>`; }).join("")}
    <div class="rw"><span class="cost">${n}/${D1_GOALS.length} done</span><button class="btn ${all ? "amber" : "ghost"}" data-act="d1Claim" ${all ? "" : "disabled"}>${all ? "Claim" : "In progress"}</button></div></article>`; }
function d1Band(T = now()) { if (!d1On(T) || G.mode === "demo") return ""; const n = d1Got(), left = S.created + D1_MS - T, h = Math.floor(left / 3600e3), m = Math.floor(left % 3600e3 / 60e3);
  return `<button class="omb d1b" data-act="d1Go"><b>⏳ FIRST DAY · ${n}/${D1_GOALS.length}</b><span>${h}h ${m}m left</span></button>`; }
function d1Claim() { if (!d1On() || d1Got() < D1_GOALS.length) return; S.d1Done = 1; grantRw(D1_RW, "Your first day"); S.vpTitles = S.vpTitles || []; if (!S.vpTitles.includes("First Light")) S.vpTitles.push("First Light"); dirty();
  celebrate({ k: "firstday", kick: "Your first day", t: "First Light", art: "adv", s: "Five goals in your first day. The galaxy noticed, and so did I.", say: D1_SAY, rw: "◆60, ⚡5 boosts, a rare crate and the title “First Light”.", go: "Onward" }); try { flushSay(); } catch (e) {} }
const D1_SAY = "Every goal, inside a single day. I've watched a lot of first days, Commander. That was one of the good ones.";
/* the tease at the end of a first session, and the payoff the next day */
const TEASE = "Commander, the pyramid's signal is getting clearer. By tomorrow I'll be able to read it. Come back, and I'll tell you what it says.";
const D2_SAY = ["I promised I'd read the signal, Commander. I did.", "It's a war report, from the last time the stars went out. The full record is in the Archives. I think you should read it."];
function teaseTick() { try { if (!S || !G.ready || !S.intro || battle || G.cineOn) return; const T = now(), d = S.bondDays || 0;
    if (!S.d1Tease && d <= 1 && T - (S.created || T) > 25 * 60e3 && !advLines && !$("#adv")) { S.d1Tease = T; dirty(); holoSure(TEASE); return; }
    if (S.d1Tease && !S.d2Said && d >= 2 && !advLines && !$("#adv") && !$("#celeb")) { S.d2Said = 1; dirty(); say(D2_SAY); } } catch (e) {} }
setInterval(teaseTick, 20000);
/* the signal log: one line with each of the first seven daily logins */
const LOGIN_STORY = ["Day one of the signal log, Commander. Mostly static. And one word I recognise: home.", "Day two. The static has a rhythm now. Someone is counting, very slowly.",
  "Day three. There are voices under the count. Hundreds of them, speaking at once.", "Day four. I separated one voice. She's asking if anyone is still out here.",
  "Day five. She said a name I haven't heard in an age. I think it was mine.", "Day six. The voices have stopped counting. Now they're singing. I know the song.",
  "Day seven. Two words, over and over: still holding. Whoever they are, they're still holding the door. For us."];
function loginStory() { try { const i = S.logStory | 0; if (i >= LOGIN_STORY.length) return; S.logStory = i + 1; dirty(); holoSure(LOGIN_STORY[i]); } catch (e) {} }
/* say it on the hologram, and keep trying until it has actually shown (another line may be up) */
function holoSure(L, n = 0) { setTimeout(() => { try { const h = document.querySelector("#advh .hsay span"); if (h && h.textContent === L) return; if (!battle && !G.cineOn && !$("#adv")) advHolo(L, true); setTimeout(() => { const h2 = document.querySelector("#advh .hsay span"); if (!(h2 && h2.textContent === L) && n < 12) holoSure(L, n + 1); }, 600); } catch (e) {} }, n ? 5000 : 1200); }
const FLAG_LOST = "The flagship took the worst of it, Commander. She shielded the pods with her own hull. We'll rebuild her. I promise.";
[[D1_SAY, "warm"], [TEASE, "tender"], [D2_SAY[0], "tender"], [D2_SAY[1], "grave"], [FLAG_LOST, "tender"], [LOGIN_STORY[0], "tender"], [LOGIN_STORY[1], "calm"], [LOGIN_STORY[2], "awe"], [LOGIN_STORY[3], "tender"], [LOGIN_STORY[4], "tender"], [LOGIN_STORY[5], "awe"], [LOGIN_STORY[6], "tender"]].forEach(([l, m]) => { CIN_MOOD[l] = m; });
