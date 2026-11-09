# v373: crash and frame-rate tracking. Reports wait in a queue on the device until they reach the server (signed out or offline
# no longer loses them); every play session sends a frame-rate summary per screen (avg fps, slow frames, freezes, errors);
# the owner reads it all in Owner tools > Crash & performance.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

rep('''CRUMBS = { open: true, t0: Date.now(), ev: [] };
''', '''CRUMBS = { open: true, t0: Date.now(), ev: [] };
/* v373 health reports: a queue kept on the device (udf.hq) and sent one by one whenever the game is signed in and online */
const HQ_K = "udf.hq", PF_K = "udf.pf", hqDev = () => navigator.userAgent.slice(0, 200);
function hqPush(r) { try { const q = JSON.parse(localStorage.getItem(HQ_K) || "[]"); r.id = r.id || r.kind + "-" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); q.push(r); localStorage.setItem(HQ_K, JSON.stringify(q.slice(-14))); } catch (e) {} }
function hqFlush() { try { if (G.hqBusy || !G.db || !G.me || G.me === "local" || G.mode !== "online") return; const q = JSON.parse(localStorage.getItem(HQ_K) || "[]"); if (!q.length) return; const r = q[0]; G.hqBusy = 1;
  const id = r.id + "-" + String(G.me).slice(0, 12); G.db.doc("feedback/" + id).set(Object.assign({}, r, { id: undefined, by: G.me, name: String(G.myName || "").slice(0, 60) })).then(() => { G.hqBusy = 0; try { const q2 = JSON.parse(localStorage.getItem(HQ_K) || "[]").filter(x => x.id !== r.id); localStorage.setItem(HQ_K, JSON.stringify(q2)); } catch (e) {} setTimeout(hqFlush, 800); }, () => { G.hqBusy = 0; }); } catch (e) { G.hqBusy = 0; } }
setInterval(hqFlush, 7000);
if (G.lastCrashFresh && G.lastCrash && G.lastCrash.ev) { const C = G.lastCrash, b = C.beat || {}, last = C.ev[C.ev.length - 1]; G.crashSent = 1; G.lastCrashFresh = 0; /* queued: the old one-shot sender stands down */
  hqPush({ kind: "crash", status: "new", at: Date.now(), died: b.t || (last && last[0]) || 0, v: b.v || 0, now: typeof GAME_V !== "undefined" ? GAME_V : 0, text: `Closed unexpectedly${last ? " after: " + last[1] : ""}`.slice(0, 300),
    beat: JSON.stringify(b).slice(0, 1500), log: C.ev.map(([tt, m]) => new Date(tt).toISOString().slice(11, 19) + " " + m).join("\\n").slice(0, 4000), up: Math.round(((b.t || (last && last[0]) || C.t0) - (C.t0 || 0)) / 1000), device: hqDev(), w: innerWidth, h: innerHeight }); G.lastCrashToast = 1; }
/* v373 frame-rate tracker: every display frame is timed and counted per screen (base, galaxy, battle, with a panel open or not);
   slow frames (under 30 fps), janky ones (under 20 fps) and freezes (over 0.7 s) are counted. The session's summary is sent when the
   game goes to the background or closes, and a session that never closed is sent on the next launch, marked as a crash. */
let PF = { t0: Date.now(), v: typeof GAME_V !== "undefined" ? GAME_V : 0, vw: {}, frz: [] };
function pfKey() { try { return battle ? "battle" : (view || "?") + (sheet ? "+panel" : ""); } catch (e) { return "?"; } }
function pfFrame(rd) { if (!(rd > 0) || rd > 20000 || !G.ready || performance.now() - (G.pfOk || (G.pfOk = performance.now())) < 4000) return; /* start-up loading is not play */ const k = pfKey(), s = PF.vw[k] || (PF.vw[k] = [0, 0, 0, 0, 0]); s[0]++; s[1] += rd; if (rd > 34) s[2]++; if (rd > 50) s[3]++; if (rd > s[4]) s[4] = rd;
  if (rd > 700) { PF.frz.push([Math.round(rd), k, Date.now()]); if (PF.frz.length > 12) PF.frz.shift(); try { crumb(`freeze ${(rd / 1000).toFixed(1)} s on ${k}`); } catch (e) {} } }
function pfRec(P, end) { const vw = {}; let n = 0, ms = 0; for (const k in P.vw) { const s = P.vw[k]; if (s[0] < 30) continue; vw[k] = [s[0], Math.round(s[1]), s[2], s[3], Math.round(s[4])]; n += s[0]; ms += s[1]; }
  if (n < 600) return null; let mem = ""; try { if (performance.memory) mem = Math.round(performance.memory.usedJSHeapSize / 1e6) + " MB"; } catch (e) {}
  return { kind: "perf", status: "log", at: Date.now(), now: P.v, end, dur: Math.round(ms / 1000), fps: Math.round(n * 1000 / ms * 10) / 10, vw: JSON.stringify(vw), frz: JSON.stringify(P.frz || []).slice(0, 900), errs: (P.errs || []).slice(0, 8).join(" | ").slice(0, 900),
    device: hqDev(), w: innerWidth, h: innerHeight, dpr: devicePixelRatio, gpu: P.gpu || "", preset: P.preset || "", hz: P.hz || 0, mem }; }
function pfSave() { try { PF.errs = [...ERR_SEEN]; PF.gpu = gfxGpu(); PF.preset = gfxPreset(); PF.hz = gfxHz(); localStorage.setItem(PF_K, JSON.stringify(PF)); } catch (e) {} }
function pfSend(end) { try { pfSave(); const r = pfRec(PF, end); if (r) hqPush(r); PF = { t0: Date.now(), v: PF.v, vw: {}, frz: [] }; localStorage.removeItem(PF_K); } catch (e) {} }
try { const old = JSON.parse(localStorage.getItem(PF_K) || "null"); localStorage.removeItem(PF_K); if (old && old.vw) { const r = pfRec(old, G.crashSent ? "crash" : "closed"); if (r) hqPush(r); } } catch (e) {}
setInterval(() => { if (!document.hidden) pfSave(); }, 15000);
document.addEventListener("visibilitychange", () => { try { frame.raw = 0; } catch (e) {} if (document.hidden) pfSend("background"); });
addEventListener("pagehide", () => pfSend("closed"));
''')
# time every display frame
rep('rafId = 0; { const rd = t - (frame.raw || t); hzSample(rd);', 'rafId = 0; { const rd = t - (frame.raw || t); hzSample(rd); pfFrame(rd);')
rep('function startAnim() { if (!rafId) rafId = requestAnimationFrame(frame); }', 'function startAnim() { if (!rafId) { frame.raw = 0; rafId = requestAnimationFrame(frame); } } // v373: a restarted loop is not a frozen frame')
# the owner's inbox: read open reports only, never crowded out by logs
rep('const sn = await G.db.collection("feedback").limit(200).get(); G.fbList = sn.docs.map(d => Object.assign({ id: d.id }, d.data())).filter(r => r && r.kind !== "crash" && r.status !== "done")',
    'const sn = await G.db.collection("feedback").where("status", "==", "new").limit(1000).get(); G.fbList = sn.docs.map(d => Object.assign({ id: d.id }, d.data())).filter(r => r && !["crash", "diag", "perf"].includes(r.kind) && r.status !== "done")')
# owner page
rep('''function shHowTo() {''', '''/* v373 Crash & performance (owner): every player's crash reports and frame-rate sessions, by device, version and screen */
const hDev = u => { u = String(u || ""); const io = u.match(/iPhone OS (\\d+)_(\\d+)/), an = u.match(/Android (\\d+)(?:; ([^;)]+))?/); return io ? "iPhone · iOS " + io[1] + "." + io[2] : /iPad/.test(u) ? "iPad" : an ? "Android " + an[1] + (an[2] && an[2] !== "K" ? " · " + an[2].trim() : "") : /Linux/.test(u) ? "Linux / desktop-mode" : /Windows/.test(u) ? "Windows" : /Mac OS X/.test(u) ? "Mac" : "Other"; };
async function healthLoad() { try { const [c, p] = await Promise.all(["crash", "perf"].map(k => G.db.collection("feedback").where("kind", "==", k).limit(1000).get()));
  const rows = sn => sn.docs.map(d => Object.assign({ id: d.id }, d.data())).sort((a, b) => (+b.at || 0) - (+a.at || 0)); G.health = { crash: rows(c), perf: rows(p) }; } catch (e) { G.health = null; G.healthErr = 1; } if (sheet && sheet.type === "health") renderSheet(); }
function shHealth() { const head = `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">Owner</div><h2>Crash &amp; performance</h2><p class="note">Every player's crashes and frame rates. Phones send them the next time they're online.</p></div><div class="fhdb"><button class="x" data-act="healthOpen" aria-label="Refresh">↻</button><button class="x" data-act="close" aria-label="Close">✕</button></div></div>`;
  if (!G.owner) return head + `<p class="note">The server doesn't list this account as the game's owner, so it won't hand over the reports.</p>`;
  const H = G.health; if (!H) return head + `<p class="note">${G.healthErr ? "Couldn't load the reports." : "Loading…"}</p>`;
  const days = sheet.d || 7, T0 = Date.now() - days * 864e5, C = H.crash.filter(r => (+r.at || 0) > T0), P = H.perf.filter(r => (+r.at || 0) > T0);
  const agg = () => ({ s: 0, c: 0, n: 0, ms: 0, slow: 0, jank: 0, frz: 0 }), add = (a, r) => { a.s++; let vw = {}; try { vw = JSON.parse(r.vw || "{}"); } catch (e) {} for (const k in vw) { const v = vw[k]; a.n += v[0]; a.ms += v[1]; a.slow += v[2]; a.jank += v[3]; } try { a.frz += JSON.parse(r.frz || "[]").length; } catch (e) {} };
  const fps = a => a.ms ? (a.n * 1000 / a.ms).toFixed(0) : "–", pct = (x, n) => n ? (x / n * 100).toFixed(1) + "%" : "–";
  const byDev = {}, byVer = {}, byView = {}, tot = agg();
  for (const r of P) { add(tot, r); add(byDev[hDev(r.device)] = byDev[hDev(r.device)] || agg(), r); add(byVer[r.now] = byVer[r.now] || agg(), r); let vw = {}; try { vw = JSON.parse(r.vw || "{}"); } catch (e) {} for (const k in vw) { const a = byView[k] = byView[k] || agg(), v = vw[k]; a.s++; a.n += v[0]; a.ms += v[1]; a.slow += v[2]; a.jank += v[3]; } }
  for (const r of C) { (byDev[hDev(r.device)] = byDev[hDev(r.device)] || agg()).c++; (byVer[r.now] = byVer[r.now] || agg()).c++; }
  const tbl = (hd, rows) => `<div class="htbl" style="--hc:minmax(0,2fr) repeat(${hd.length - 1},minmax(0,1fr))"><div class="hrow hh">${hd.map(h => `<span>${h}</span>`).join("")}</div>${rows.map(r => `<div class="hrow">${r.map(c => `<span>${c}</span>`).join("")}</div>`).join("") || '<p class="note">Nothing yet.</p>'}</div>`;
  const beat = r => { try { const b = JSON.parse(r.beat || "{}"); return [b.view && "on " + b.view + (b.battle ? " (battle)" : ""), b.fps && b.fps + " fps", b.mem, b.tex && b.tex + " textures"].filter(Boolean).join(" · "); } catch (e) { return ""; } };
  return head + `<div class="segc">${[1, 7, 30].map(d => `<button class="${d === days ? "on" : ""}" data-act="healthDays" data-d="${d}">${d === 1 ? "24 hours" : d + " days"}</button>`).join("")}</div>
    <div class="hsum"><div><b>${C.length}</b><small>crashes</small></div><div><b>${tot.s}</b><small>play runs</small></div><div><b>${fps(tot)}</b><small>avg fps</small></div><div><b>${pct(tot.slow, tot.n)}</b><small>slow frames</small></div><div><b>${tot.frz}</b><small>stalls</small></div></div>
    <h2 class="sec">By device</h2>${tbl(["Device", "Crash", "Runs", "FPS", "Slow", "Stall"], Object.entries(byDev).sort((a, b) => b[1].c - a[1].c || b[1].s - a[1].s).map(([k, a]) => [esc(k), a.c, a.s, fps(a), pct(a.slow, a.n), a.frz]))}
    <h2 class="sec">By screen</h2>${tbl(["Screen", "Runs", "FPS", "Slow", "Janky"], Object.entries(byView).sort((a, b) => b[1].n - a[1].n).map(([k, a]) => [esc(k), a.s, fps(a), pct(a.slow, a.n), pct(a.jank, a.n)]))}
    <h2 class="sec">By version</h2>${tbl(["Version", "Crash", "Runs", "FPS", "Slow"], Object.entries(byVer).sort((a, b) => (+b[0] || 0) - (+a[0] || 0)).slice(0, 10).map(([k, a]) => ["v" + esc(String(k)), a.c, a.s, fps(a), pct(a.slow, a.n)]))}
    <h2 class="sec">Latest crashes</h2>${C.slice(0, 20).map(r => `<details class="card hcr"><summary><b>${esc(String(r.name || "Unnamed"))}</b> <small>${r.at ? ago(+r.at) + " ago" : ""} · v${okInt(r.now)} · ${esc(hDev(r.device))}</small><br><span>${esc(String(r.text || ""))}</span><br><small class="note">${esc(beat(r))}${r.up ? ` · ${Math.round(r.up / 60)} min into the session` : ""}</small></summary><pre>${esc(String(r.log || ""))}</pre></details>`).join("") || '<p class="note">No crashes in this period.</p>'}
    <h2 class="sec">Slowest sessions</h2>${tbl(["Player", "Device", "FPS", "Stall", "Errors"], P.filter(r => r.fps).sort((a, b) => a.fps - b.fps).slice(0, 10).map(r => [esc(String(r.name || "?")), esc(hDev(r.device)), r.fps, (() => { try { return JSON.parse(r.frz || "[]").length; } catch (e) { return 0; } })(), esc(String(r.errs || "").slice(0, 60)) || "–"]))}`; }
function shHowTo() {''')
rep('fbinbox: "feedback",', 'fbinbox: "feedback", health: "crash & performance",')
rep('fbinbox:', 'health: shHealth, fbinbox:', 1) if False else None
i = t.index('howto: shHowTo, fbinbox:'); t = t[:i] + 'health: shHealth, ' + t[i:]
rep('''${duelOwner() ? `<button class="btn ghost wide" data-act="fbInbox">💬 Feedback inbox</button>` : ""}''',
    '''${duelOwner() ? `<button class="btn ghost wide" data-act="fbInbox">💬 Feedback inbox</button><button class="btn ghost wide" data-act="healthOpen">📉 Crash &amp; performance</button>` : ""}''')
rep('  fbInbox: () => {', '''  healthOpen: () => { if (!duelOwner()) return; G.health = null; G.healthErr = 0; if (!sheet || sheet.type !== "health") openSheet({ type: "health", d: 7 }); else renderSheet(); healthLoad(); },
  healthDays: d => { if (sheet && sheet.type === "health") { sheet.d = +d.d; renderSheet(); } },
  fbInbox: () => {''')
css = '''
/* v373 crash & performance page */
.hsum{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:10px 0}.hsum div{border:1px solid var(--line);border-radius:10px;padding:8px 4px;text-align:center;background:var(--hull)}.hsum b{display:block;font-family:var(--f-display);font-size:18px;color:#dff4ff}.hsum small{font-size:10.5px;color:var(--muted)}
.htbl{flex:none;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:6px}.hrow{display:grid;grid-template-columns:var(--hc);gap:6px;padding:7px 10px;font-size:12.5px;border-top:1px solid var(--line)}.hrow:first-child{border-top:0}.hrow.hh{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em;background:rgba(85,214,232,.06)}.hrow span{overflow-wrap:anywhere}
.hcr{flex:none}.hcr summary{cursor:pointer;list-style:none;font-size:13px;line-height:1.4}.hcr pre{white-space:pre-wrap;font-size:11px;max-height:260px;overflow:auto;margin:8px 0 0;user-select:text}
'''
i = t.index('</style>', t.index('.fshero{')); t = t[:i] + css + t[i:]  # the main stylesheet, not the tiny first one
open(p, "w").write(t)
# the "closed unexpectedly" toast still shows for a crash that went into the queue
t = open(p).read(); a = 'setTimeout(() => { try { if (G.lastCrashFresh) { const L = G.lastCrash.ev'; assert t.count(a) == 1; t = t.replace(a, 'setTimeout(() => { try { if (G.lastCrashFresh || G.lastCrashToast) { const L = G.lastCrash.ev'); open(p, "w").write(t)
