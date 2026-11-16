/* ---------- v608 the Advisor comes alive (owner: "use all these to bring the advisor alive"). Her portrait is no longer one still:
   every line picks a face for its mood (shocked when it's urgent, determined or angry when it's fierce, disappointed or stern when
   it's grave, smiling when it's warm, relieved when it's tender, focused when she reads a report). While her voice plays she talks:
   her lips follow the loudness of the clip (closed, parted, open) on one face so nothing jumps, and she blinks every few seconds.
   For the big moments she steps out in full: a welcome, a salute when a Titan is commissioned, a victory, an alarm, a defeat, a
   command pose for the Cube and the battles, a briefing pose for long explanations and a pointing pose toward what she's showing. */
const AF_V = 608, afUrl = k => `art/adv/${k}.webp?v=${AF_V}`, AF_TALK = ["n_0", "n_1", "n_2"], afCache = {};
function afPre(k) { let i = afCache[k]; if (!i) { i = afCache[k] = new Image(); i.src = afUrl(k); try { i.decode().catch(() => {}); } catch (e) {} } return i; }
function afOn() { try { const d = S && cosDef(cosOf().eq.adv); return !(d && d.art); } catch (e) { return true; } } /* a skin with its own portrait keeps it */
const AF_LOSS = /\b(lost|lose|fallen|fell|destroyed|defeat|defeated|gone|failed|wiped|ruins|broke through)\b/i, AF_WIN = /\b(victory|won|win|wins|first blood|broken|shattered|captured|taken|ours|did it|held|claimed)\b/i;
function afFace(line) { const m = advMood(line), t = String(line || "");
  if (m === "urgent") return { r: "shocked", hold: 1 };
  if (m === "fierce") return { r: /!/.test(t) ? "angry" : "determined", hold: 1 };
  if (m === "grave") return { r: AF_LOSS.test(t) ? "disappointed" : "stern", hold: 1 };
  if (m === "warm" || m === "excited") return { r: "s_0" };
  if (m === "playful") return { r: /\b(again|really|seriously|another)\b/i.test(t) ? "annoyed" : voiceKey(t).charCodeAt(0) % 2 ? "flustered" : "s_0" };
  if (m === "tender") return { r: "relieved" };
  if (/\b(scan|scans|radar|sensors?|reports?|reading|intel|data)\b/i.test(t)) return { r: "focused" };
  return { r: "n_0" }; }
const AF_SEL = { dlg: "#adv .advimg", holo: "#advh.on .advimg", tour: "#ftour .ftcard img" };
function afSet(line, src) { if (!line) return; src = AF_SEL[src] ? src : "dlg"; const T = performance.now(), f = afFace(line);
  (G.afS = G.afS || {})[src] = { line, vk: voiceKey(line), r: f.r, hold: !!f.hold, react: T + (f.r === "n_0" ? 0 : 1100), blink: T + 1800 + Math.random() * 2500, lk: "", lt: 0 };
  [f.r, "n_0", "n_1", "n_2", "n_b"].forEach(afPre); if (!G.afI) G.afI = setInterval(afTick, 40); afTick();
  try { afPoseFor(line, src); } catch (e) {} }
function afFrame(st, T) { const a = VOICE.au, mk = a && /voice\/([a-z0-9]+)\.mp3/.exec(a.src || ""), talk = mk && mk[1] === st.vk && !a.paused && !a.ended && a.currentTime > 0; /* only the line being spoken moves its lips */
  if (st.hold || T < st.react) return st.r;
  if (talk) { let lip = 0; const env = VENV && VENV[mk[1]];
    if (env) { const i = Math.floor(a.currentTime * 25), c = env.charCodeAt(Math.min(env.length - 1, i)) - 48; lip = Math.max(0, c) / 42; } else lip = .3 + .3 * Math.sin(T / 70) * Math.sin(T / 173);
    const k = lip < .16 ? "n_0" : lip < .42 ? "n_1" : "n_2"; if (k !== st.lk && T - st.lt > 75) { st.lk = k; st.lt = T; } return st.lk || "n_0"; }
  if (st.r === "n_0") { if (T > st.blink + 140) st.blink = T + 2200 + Math.random() * 3800; if (T > st.blink) return "n_b"; }
  return st.r; }
function afTick() { const T = performance.now(), on = afOn(); let any = 0;
  for (const src in AF_SEL) { const ims = document.querySelectorAll(AF_SEL[src]), st = (G.afS || {})[src]; if (!ims.length || !st) continue; any = 1;
    if (!on) { ims.forEach(im => { if (im.classList.contains("afc")) { im.classList.remove("afc"); im.src = advArt(); im.dataset.af = ""; } }); continue; }
    const k = afFrame(st, T), pre = afPre(k);
    ims.forEach(im => { const was = im.dataset.af || ""; if (was === k) return; if (was && !(pre.complete && pre.naturalWidth)) return; /* wait for the frame so nothing flashes */
      im.classList.add("afc"); im.src = afUrl(k); im.dataset.af = k;
      const fam = x => AF_TALK.includes(x) || x === "n_b" ? "n" : x; if (was && fam(was) !== fam(k)) try { im.animate([{ opacity: .3 }, { opacity: 1 }], { duration: 220, easing: "ease-out" }); } catch (e) {} }); }
  if (!any) { clearInterval(G.afI); G.afI = 0; } }
/* the full-body poses */
const AP_K = ["welcome", "victory", "alarm", "explain", "defeated", "salute", "point", "cube", "command", "ready"];
function advPose(k, o) { o = o || {}; if (!AP_K.includes(k) || !afOn()) return; const T = Date.now(), key = k === "point" ? "apP" : "apT";
  if (!o.force && T - (G[key] || 0) < (k === "point" ? 75000 : 100000)) return; G[key] = T; if (k !== "point") G.apP = Math.max(G.apP || 0, T - 50000);
  const im = new Image(); im.src = `art/adv/p_${k}.webp?v=${AF_V}`; const show = () => { const old = $("#advpose"); if (old) old.remove();
    const side = o.side || "r", w = document.createElement("div"); w.id = "advpose"; w.className = `ap${side === "l" ? " l" : ""}${o.flip ? " flip" : ""}${advColor() ? " color" : ""} p-${k}`; w.setAttribute("aria-hidden", "true");
    w.innerHTML = `<img src="${im.src}" alt="" style="${advFx()}"><i class="apbeam"></i>`; $("#app").prepend(w); requestAnimationFrame(() => requestAnimationFrame(() => w.classList.add("on")));
    clearTimeout(G.apHide); G.apHide = setTimeout(() => { w.classList.remove("on"); setTimeout(() => w.remove(), 600); }, o.ms || 3800); };
  try { im.decode().then(show, () => { im.onload = show; }); } catch (e) { im.onload = show; } }
function afPoseFor(line, src) { const t = String(line || ""), m = advMood(line);
  if (!G.apWel) { G.apWel = 1; let last = 0; try { last = +localStorage.getItem("udfApWel") || 0; } catch (e) {} if (Date.now() - last > 4 * 3600e3) { try { localStorage.setItem("udfApWel", Date.now()); } catch (e) {} return advPose("welcome", { force: 1 }); } }
  let k = null;
  if (/\bCube\b/.test(t) && /urgent|fierce|excited/.test(m)) k = "cube";
  else if (m === "urgent") k = "alarm";
  else if (m === "grave" && AF_LOSS.test(t)) k = "defeated";
  else if (/\b(commissioned|launched|promoted|promotion|new rank|out of the dock)\b/i.test(t)) k = "salute";
  else if (m === "excited" && AF_WIN.test(t)) k = "victory";
  else if (m === "fierce") k = /!/.test(t) ? "command" : "ready";
  if (k) return advPose(k);
  if (src === "dlg") { const d = $("#adv"); if (d && !d.dataset.af) { d.dataset.af = 1; if ((advLines || []).length >= 3) return advPose("explain"); } }
  if (src === "holo" && typeof GD !== "undefined" && GD.el && GD.el.isConnected && (m === "calm" || m === "warm")) { const r = GD.el.getBoundingClientRect(); if (r.width) advPose("point", r.left + r.width / 2 > innerWidth / 2 ? { side: "l" } : { side: "r", flip: 1 }); } }
function advCelebArt(c) { return afOn() ? `art/adv/p_${c.k === "comeback" ? "welcome" : "victory"}.webp?v=${AF_V}` : ADV_ART; }
