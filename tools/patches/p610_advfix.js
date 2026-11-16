/* v610 (owner: "remove this expression... make sure there are no weird transition expressions, she needs to be perfect"; and
   "fix the mouth"). She now has exactly two faces, each with a closed mouth, an open mouth and a blink laid onto one head so
   nothing jumps or ghosts: her warm smile (warm, excited, playful, tender and awe lines) and her calm face (every other line).
   No reaction faces, no swaps to another head in the middle of a line. Her lips open and close with her voice. */
const AF_FAM = { n: ["n_0", "n_1", "n_b"], s: ["s_0", "s_q", "s_b"] }, AF_SMILE = ["warm", "excited", "playful", "tender", "awe"];
function afFace(line) { return AF_SMILE.includes(advMood(line)) ? "s" : "n"; }
const AF_SEL = { dlg: "#adv .advimg", holo: "#advh.on .advimg", tour: "#ftour .ftcard img" };
function afSet(line, src) { if (!line) return; src = AF_SEL[src] ? src : "dlg"; const T = performance.now(), f = afFace(line);
  (G.afS = G.afS || {})[src] = { line, vk: voiceKey(line), f, blink: T + 1800 + Math.random() * 2500, open: 0, lt: 0 };
  AF_FAM[f].forEach(afPre); if (!G.afI) G.afI = setInterval(afTick, 40); afTick();
  try { afPoseFor(line, src); } catch (e) {} }
function afFrame(st, T) { const [shut, open, blink] = AF_FAM[st.f], a = VOICE.au, mk = a && /voice\/([a-z0-9]+)\.mp3/.exec(a.src || ""), talk = mk && mk[1] === st.vk && !a.paused && !a.ended && a.currentTime > 0;
  if (talk) { let lip = 0; const env = VENV && VENV[mk[1]];
    if (env) { const i = Math.floor(a.currentTime * 25), c = env.charCodeAt(Math.min(env.length - 1, i)) - 48; lip = Math.max(0, c) / 42; } else lip = .3 + .3 * Math.sin(T / 70) * Math.sin(T / 173);
    const want = st.open ? lip > .12 : lip > .22; /* a little hysteresis so the lips don't flutter */ if (want !== !!st.open && T - st.lt > 90) { st.open = want ? 1 : 0; st.lt = T; } return st.open ? open : shut; }
  st.open = 0; if (T > st.blink + 140) st.blink = T + 2200 + Math.random() * 3800; return T > st.blink ? blink : shut; }
function afTick() { const T = performance.now(), on = afOn(); let any = 0;
  for (const src in AF_SEL) { const ims = document.querySelectorAll(AF_SEL[src]), st = (G.afS || {})[src]; if (!ims.length || !st) continue; any = 1;
    if (!on) { ims.forEach(im => { if (im.classList.contains("afc")) { im.classList.remove("afc"); im.src = advArt(); im.dataset.af = ""; } }); continue; }
    const k = afFrame(st, T), pre = afPre(k);
    ims.forEach(im => { const was = im.dataset.af || ""; if (was === k) return; if (was && !(pre.complete && pre.naturalWidth)) return; /* wait for the frame so nothing flashes */
      im.classList.add("afc"); im.src = afUrl(k); im.dataset.af = k;
      if (was && was[0] !== k[0]) try { im.animate([{ opacity: .3 }, { opacity: 1 }], { duration: 220, easing: "ease-out" }); } catch (e) {} }); } /* only a new line can change her face */
  if (!any) { clearInterval(G.afI); G.afI = 0; } }
/* v610 report a player (Google Play's rule for games with chat: players can block and report). A report goes to the developer's
   inbox (Settings › Feedback inbox) with what they wrote; Block already hides their messages everywhere. */
function reportPlayer(u, msgId) { if (!u || u === G.me) return; const rep = S.reported = S.reported || {}; if (rep[u + (msgId || "")]) return toast("You already reported this. Thank you.");
  const all = [].concat(CHAT.g || [], CHAT.a || [], ...Object.values(CHAT.dms || {}).map(c => c.m || [])), mine = all.filter(m => m.u === u).slice(-8), msg = msgId ? all.find(m => m.id === msgId) : null;
  hqPush({ kind: "report", status: "new", at: Date.now(), now: GAME_V, about: u, aboutName: String(nameOf(u)).slice(0, 60), text: `Report on ${nameOf(u)}${msg ? `: "${String(msg.x || "").slice(0, 300)}"` : ""}`.slice(0, 400), log: mine.map(m => new Date(m.t).toISOString().slice(0, 16) + " " + String(m.x || "").slice(0, 200)).join("\n").slice(0, 3000), device: hqDev() });
  rep[u + (msgId || "")] = Date.now(); dirty(); try { hqFlush(); } catch (e) {} toast("Reported. The developer will review it. You can also block this commander.", "win"); }
