# v541 push notifications (owner: "Do it all", item 1 of the list). Server side (Supabase, 2026-11-13): tables push_subs and push_q,
# RPCs push_sub / push_unsub / push_sync / push_alert, the edge function push_send (VAPID keys and the cron secret in the vault,
# read through push_secrets() by the service role only) and a pg_cron job every minute. docs/sw.js shows them and opens the game on tap;
# docs/udf-supabase.js exposes window.udfPush. In the game:
#  - Menu › Game › Notifications: turn them on (asks the browser, subscribes this device) or off. On an iPhone/iPad they need the game
#    added to the Home Screen first (Apple's rule), and the card says so. After the Academy a one-time card offers them.
#  - pushSync() sends your own reminders (replacing the last list, at most 40): construction, research and shipyard done, each fleet
#    landing and coming home, the next boss hunt and the Battle for the Cube 10 minutes before they start, and the next free wheel spin.
#    It runs a few seconds after anything changes (on save) and when the app goes to the background.
#  - An attack on another commander's world (publishInbound, not probes) also sends them "Incoming attack!" at once (push_alert, rate
#    limited on the server).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''
/* ---------- v541 push notifications ---------- */
const PUSH_PUB = "BNBjfOGbHHdVS-JM2o0QdPsm_V_4VjfgGMvk3lZ8gfHs0Vo17ZqjOVNOiNbxPmRFiW2E9tGf5Ao7SsNLxBVTjt0";
const pushCan = () => "serviceWorker" in navigator && "PushManager" in window && "Notification" in window && G.mode === "online" && !!window.udfPush;
const pushNeedsHome = () => IOS && !STANDALONE;
const pushOn = () => { try { return localStorage.getItem("udf.push") === "1" && Notification.permission === "granted"; } catch (e) { return false; } };
const b64u = s => { const p = "=".repeat((4 - s.length % 4) % 4), b = atob((s + p).replace(/-/g, "+").replace(/_/g, "/")); return Uint8Array.from(b, c => c.charCodeAt(0)); };
async function pushEnable() {
  if (pushNeedsHome()) return toast("On iPhone and iPad, add the game to your Home Screen first (Share › Add to Home Screen), then open it from there and turn notifications on.", "warn");
  if (!pushCan()) return toast("This browser can't receive notifications from the game.", "warn");
  try { const perm = await Notification.requestPermission(); if (perm !== "granted") return toast("Notifications are blocked. Allow them for this site in your browser settings, then try again.", "warn");
    const reg = await navigator.serviceWorker.ready; let sub = await reg.pushManager.getSubscription(); if (!sub) sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64u(PUSH_PUB) });
    await window.udfPush.sub(sub.toJSON()); try { localStorage.setItem("udf.push", "1"); } catch (e) {} G.pushSig = null; pushSync(true); crumb("push notifications on");
    toast("Notifications on: builds, research, fleets, boss hunts and attacks on your worlds.", "win"); render(true); } catch (e) { toast("Couldn't turn notifications on: " + String(e && e.message || e).slice(0, 80), "warn"); } }
async function pushDisable() { try { localStorage.setItem("udf.push", "0"); const reg = await navigator.serviceWorker.ready, sub = await reg.pushManager.getSubscription(); if (sub) { try { await window.udfPush.sync([]); await window.udfPush.unsub(sub.endpoint); } catch (e) {} await sub.unsubscribe(); } } catch (e) {} toast("Notifications off."); render(true); }
function pushItems() { const T = now(), out = [], add = (tag, at, title, body) => { if (at > T + 30000 && at < T + 29 * 864e5) out.push({ tag, at: Math.round(at), title, body }); };
  try { const b = nextIn("b"), r = nextIn("r"), q = nextIn("s");
    if (b) add("bq", b.e, "Construction complete", `${b.n} is ready.${b.more ? "" : " Your builders are free for the next job."}`);
    if (r) add("rq", r.e, "Research complete", `${r.n} is finished.${r.more ? "" : " The lab is free."}`);
    if (q) add("sq", q.e, "Ships ready", `${q.n} rolled out of the shipyard.`); } catch (e) {}
  for (const f of S.fleets || []) { if (f.demo) continue; const fb = fleetBounds(f); if (!fb) continue; const p = G.byId[f.pid] || (typeof PB !== "undefined" && PB[f.pid]) || {};
    if (f.phase === "out") add("fl" + f.id, fb[1], f.mission === "spy" ? "Probe arrived" : f.mission === "attack" ? "Your fleet is attacking" : "Fleet arrived", `Your fleet reached ${p.name || "its target"}.`);
    else if (f.phase === "back") add("fb" + f.id, fb[1], "Fleet home", `Your fleet is back home${f.loot ? " with its loot" : ""}.`); }
  for (const g of [1, 2, 3]) { try { if (!wbGroupOn(g, T)) { const n = wbGroupNext(g, T); add("boss" + g, n - 10 * 60e3, `${SB_G[g].n} in 10 minutes`, `${wbMain(g).map(k => WB[k].n).join(", ")} rise soon. Gather your fleet.`); } } catch (e) {} }
  try { if (!evActive(T)) add("cube", evStart(evWeek(T) + 1) - 10 * 60e3, "Battle for the Cube in 10 minutes", "The Cube descends at the heart of the galaxy. Rally your alliance."); } catch (e) {}
  try { if ((S.shopFree || "") === shopDay()) add("wheel", shopDayEnd() + 60e3, "Free spin ready", "The Holo Glyph Wheel has a new free spin for you in the Void Shop."); } catch (e) {}
  return out.sort((a, b) => a.at - b.at).slice(0, 40); }
function pushSync(force) { if (G.pushT && !force) return; const T0 = Date.now(); if (!force && T0 - (G.pushChk || 0) < 5000) return; G.pushChk = T0; if (!pushOn() || !pushCan() || !S) return; clearTimeout(G.pushT); G.pushT = setTimeout(() => { G.pushT = null; try { const it = pushItems(), sig = JSON.stringify(it.map(x => [x.tag, Math.round(x.at / 30000)]));
    if (!force && sig === G.pushSig) return; G.pushSig = sig; window.udfPush.sync(it).catch(() => { G.pushSig = null; }); } catch (e) {} }, force ? 50 : 4000); }
document.addEventListener("visibilitychange", () => { if (document.hidden) pushSync(true); });
setInterval(() => pushSync(), 120000);
const pushCard = () => { if (G.mode !== "online") return ""; const on = pushOn();
  return `<div class="mcard"><h3>🔔 Notifications</h3>${on ? `<p>On for this device: builds, research, shipyard, fleets landing and coming home, boss hunts and the Cube 10 minutes before they start, the free wheel spin, and attacks on your worlds.</p><button class="btn ghost" data-act="pushOff">Turn off on this device</button>`
    : pushNeedsHome() ? `<p>Get a buzz when a build finishes, a fleet lands, a boss rises or someone attacks you. On iPhone and iPad this needs the game on your Home Screen: tap Share › <b>Add to Home Screen</b>, open it from there, then come back here.</p><button class="btn amber" data-act="pushOn">Turn on notifications</button>`
    : `<p>Get a buzz when a build finishes, a fleet lands, a boss rises or someone attacks you, even with the game closed.</p><button class="btn amber" data-act="pushOn">Turn on notifications</button>`}</div>`; };
'''
rep('function sendFleet(p, n, mission, extra) {', JS + 'function sendFleet(p, n, mission, extra) {')
# the attack alert
rep('''      items.push({ id: f.id + "-" + (hash(G.me || "x") % 1e6), from: G.me, pid: f.pid, out: f.out, arrive: f.arrive, ox: f.ox, oy: f.oy, n: f.n, src: launchSrc(f), spy: f.mission === "spy" ? 1 : 0 }); // the defender learns where the strike was launched from
      await ref.set({ items }); } catch (e) {}''', '''      items.push({ id: f.id + "-" + (hash(G.me || "x") % 1e6), from: G.me, pid: f.pid, out: f.out, arrive: f.arrive, ox: f.ox, oy: f.oy, n: f.n, src: launchSrc(f), spy: f.mission === "spy" ? 1 : 0 }); // the defender learns where the strike was launched from
      await ref.set({ items });
      if (f.mission !== "spy" && window.udfPush) { const p = G.byId[f.pid] || {}; window.udfPush.alert(uid, "atk" + f.id + (hash(G.me || "x") % 1e5), "⚠ Incoming attack!", `${G.myName || "A commander"} launched a fleet at ${p.name || "your world"}. It lands in ${ftime(f.arrive - now())}. Open the game to prepare.`).catch(() => {}); } /* v541 */
    } catch (e) {}''')
# Menu card and actions
rep('''    <div class="mcard"><h3>${MI.grid.replace("<svg", '<svg style="width:24px;height:24px;color:#38dfee"')}Play on your phone</h3>''', '''    ${pushCard()}<div class="mcard"><h3>${MI.grid.replace("<svg", '<svg style="width:24px;height:24px;color:#38dfee"')}Play on your phone</h3>''')
rep('  remindToggle: () => {', '  pushOn: () => { pushEnable(); }, pushOff: () => { pushDisable(); }, pushLater: () => { S.pushAsk = 2; dirty(); const c = $("#pushask"); if (c) c.remove(); }, /* v541 */\n  remindToggle: () => {')
# sync on every save
rep('const dirty = () => { store.dirty = true; };', 'const dirty = () => { store.dirty = true; try { pushSync(); } catch (e) {} }; /* v541 reminders follow every change */')
# a one-time offer after the Academy (online, supported, not on yet)
rep('function render(keepScroll) {', '''setInterval(() => { try { if (!S || !G.ready || S.pushAsk || pushOn() || !pushCan() || tutOn() || sheet || battle || advLines || !S.tut || S.tut.k !== "done" || $("#pushask")) return;
  S.pushAsk = 1; dirty(); const w = document.createElement("div"); w.id = "pushask"; w.className = "toast rmd busy pushask";
  w.innerHTML = `<span class="ric">🔔</span><span class="rtx"><small>Stay in the loop</small><b>Turn on notifications?</b><em>Know when builds finish, fleets land, bosses rise or someone attacks you.${pushNeedsHome() ? " Add the game to your Home Screen first." : ""}</em></span><span class="rbt"><button class="btn sm amber" data-act="pushOn">Turn on</button><button class="rx" data-act="pushLater" aria-label="Not now">✕</button></span>`;
  const box = $("#toasts"); if (box) box.appendChild(w); setTimeout(() => { if (w.isConnected) w.remove(); }, 20000); } catch (e) {} }, 45000); /* v541 one offer, after the Academy */
function render(keepScroll) {''')
s2 = re.sub(r"GAME_V = 540\b", "GAME_V = 541", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
