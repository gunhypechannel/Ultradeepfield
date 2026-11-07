import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# ONLINE new accounts (found by the online test bench: the real sign-in code on a copy of the live database).
# 1) The faction question fired on a fixed 8-second timer, while a new player was still on the sign-in screen, so it ran against
#    the wrong save; signing a new account in on a phone that held another account's save then skipped the faction choice and ran
#    the opening straight away. The question now waits for the sign-in and the cloud check, and a new account always gets it.
rep('''  if (S.faction || S.facAsked || !(window.claude && window.claude.use)) G.askFac(); else setTimeout(() => G.askFac && G.askFac(), 8000);''',
    '''  G.askFac0 = G.askFac; // v329: kept, so a new account signed in on this device is asked too
  const facWait = () => { if (!G.askFac) return; if (!store.ready && G.mode === "connecting" || $("#udfAuth") || $("#oldw")) return void setTimeout(facWait, 1000); G.askFac(); }; // v329: never behind the sign-in screen
  if (S.faction || S.facAsked || !(window.claude && window.claude.use)) G.askFac(); else setTimeout(facWait, 1000);''')
rep('''S.homeName = hn; live = false; advance(now()); live = true; view = "base"; rebuild(); render(true); intro(); toast("New account: a fresh homeworld is ready for you."); }''',
    '''S.homeName = hn; live = false; advance(now()); live = true; view = "base"; rebuild(); render(true); G.askFac = G.askFac0; toast("New account: a fresh homeworld is ready for you."); } // v329: faction, then the opening battle''')
# 2) The "Played before the move?" card covered the opening battle's briefing on every new account, and taps on the Advisor
#    went to it. It now comes first, on its own; the faction choice and the opening battle follow once it is answered.
rep('''if (!snap.exists) setTimeout(oldOffer, 1500);''', '''if (!snap.exists && window.udfOld && window.udfOld.available && !(S.uid && S.uid === uid && S.intro)) G.oldWait = 1; // v329''')
rep('''    if (G.askFac) G.askFac(); // v138''', '''    if (G.oldWait) oldOffer(); else if (G.askFac) G.askFac(); // v329: the old-server card first, on its own // v138''')
rep('''function closeOld() { const el = document.getElementById("oldw"); if (el) el.remove(); }''',
    '''function closeOld(keep) { const el = document.getElementById("oldw"); if (el) el.remove(); if (G.oldWait && !keep) { G.oldWait = 0; setTimeout(() => G.askFac && G.askFac(), 250); } } // v329: then the faction choice and the opening''')
rep('''async function empOld() { closeOld(); let d; try { d = await window.udfOld.fetch(); } catch (e) { return toast((e && e.message) || "Couldn't reach the old server.", "warn"); } if (d) empLoad(d, true); }''',
    '''async function empOld() { const w = G.oldWait; G.oldWait = 0; closeOld(true); const after = () => { if (w && G.askFac) G.askFac(); }; let d; try { d = await window.udfOld.fetch(); } catch (e) { toast((e && e.message) || "Couldn't reach the old server.", "warn"); return after(); } if (d) empLoad(d, true); after(); }''')
rep('''function oldOffer() { if (!window.udfOld || !window.udfOld.available || document.getElementById("oldw")) return;''',
    '''function oldOffer() { if (!window.udfOld || !window.udfOld.available || document.getElementById("oldw")) return closeOld();''')
# 3) During the Academy nothing hides the guide any more: minimizing (✕, the Academy card's minimize, the Advisor's) only folds
#    the card; the next step stays marked. Saves already holding a 5-minute snooze come back at once.
rep('''const TUT_SNOOZE = 5 * 60000, tutSnoozed = () => !!(S && S.tut && S.tut.snz > now());''',
    '''const TUT_SNOOZE = 5 * 60000, tutSnoozed = () => !!(S && S.tut && S.tut.snz > now()), guideSnz = () => !tutOn() && (tutSnoozed() || S.pathSnz > now()); // v329''')
rep('''!(sheet && sheet.type === "faction") && !tutSnoozed() && !(S.pathSnz > now()) ? (m =>''', '''!(sheet && sheet.type === "faction") && !guideSnz() ? (m =>''')
rep('''const mode = !battle && G.ready && !G.cubeDemo && !tutSnoozed() && !(S.pathSnz > now()) ? advPick() : null;''', '''const mode = !battle && G.ready && !G.cubeDemo && !guideSnz() ? advPick() : null;''')
rep('''const T = now(); if (S.tut) { S.tut.open = 0; S.tut.snz = T + TUT_SNOOZE; } S.pathSnz = T + TUT_SNOOZE; dirty(); coachRender(true); g.style.display = "none"; toast("Guide hidden for 5 minutes. Open it any time from the Quests tab."); }, true); }''',
    '''const T = now(); if (tutOn()) { S.tut.open = 0; dirty(); coachRender(true); return; } if (S.tut) { S.tut.open = 0; S.tut.snz = T + TUT_SNOOZE; } S.pathSnz = T + TUT_SNOOZE; dirty(); coachRender(true); g.style.display = "none"; toast("Guide hidden for 5 minutes. Open it any time from the Quests tab."); }, true); }
  g.classList.toggle("acad", tutOn()); // v329: no ✕ during the Academy''')
rep('''#tutguide .tg-tip .tgl{flex:1 1 auto;min-width:0}''', '''#tutguide.acad .tgx{display:none!important}#tutguide .tg-tip .tgl{flex:1 1 auto;min-width:0}''')
rep('''  tutMin: () => { S.tut.open = 0; S.tut.snz = now() + TUT_SNOOZE; dirty(); coachRender(true); toast("Academy hidden. It'll pop back up in 5 minutes, or open it any time from the Quests tab."); },''',
    '''  tutMin: () => { S.tut.open = 0; if (!tutOn()) S.tut.snz = now() + TUT_SNOOZE; dirty(); coachRender(true); toast(tutOn() ? "Academy folded. Your next step stays marked on screen." : "Academy hidden. It'll pop back up in 5 minutes, or open it any time from the Quests tab."); }, // v329''')
rep('''  pathMin: () => { S.pathOpen = 0; S.pathSnz = now() + TUT_SNOOZE;''', '''  pathMin: () => { S.pathOpen = 0; if (!tutOn()) S.pathSnz = now() + TUT_SNOOZE;''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 329", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v329 from', v)
import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# joining: a returning commander whose homeworld record hadn't arrived yet could get a brand-new homeworld written over the real one
# (same id); the record is now read directly first, and an existing homeworld of yours is never overwritten
rep('''    if (existing && existing.home && G.byId[existing.home]) { G.myHome = existing.home;''',
    '''    if (existing && existing.home && !G.byId[existing.home]) { try { const hs = await G.db.doc("planets/" + existing.home).get(); if (hs.exists) { const d = cleanDoc(hs.data()); if (d) { G.docs[existing.home] = d; rebuild(); } } } catch (e) {} } // v329
    if (existing && existing.home && G.byId[existing.home]) { G.myHome = existing.home;''')
rep('''    const h = makeHome(G.me, G.list.filter(p => p.kind === "home")); h.name = genName(rnd(hash(G.me) + 3));
    await G.db.doc("planets/" + h.id).set(planetDoc(h));''',
    '''    const h = makeHome(G.me, G.list.filter(p => p.kind === "home")); h.name = genName(rnd(hash(G.me) + 3));
    { const old = await G.db.doc("planets/" + h.id).get().catch(() => null), od = old && old.exists ? cleanDoc(old.data()) : null; // v329: never write over a homeworld you already have
      if (od && od.owner === G.me) { G.docs[h.id] = od; G.myHome = h.id; G.joinedAt = T; rebuild(); G.mode = "online"; store.lastPlayer = ""; syncPlayer(); finishJoin(true); return; } }
    await G.db.doc("planets/" + h.id).set(planetDoc(h));''')
# a join that failed on a network hiccup dropped the player into a solo galaxy for the session; it now tries again first
rep('''    else { G.mode = "connecting"; initOffline(); softRender(); }
  } finally { joining = false; }''',
    '''    else if ((G.joinTry = (G.joinTry || 0) + 1) < 4) { G.mode = "connecting"; setTimeout(maybeJoin, 2500 * G.joinTry); } // v329: try again before giving up
    else { G.mode = "connecting"; initOffline(); softRender(); }
  } finally { joining = false; }''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# the naming step starts with the name you signed up with; if another commander already has it, the guide now says so
rep('''path: () => [['.sheet [data-act="nameSave"]', "Type your name, then tap Save"], ['.sheet #cnin', "Type your commander name"], SHOWME]''',
    '''path: () => { const v = (($(".sheet #cnin") || {}).value || "").trim().toLowerCase(), taken = v && Object.entries(G.names || {}).some(([id, n]) => id !== G.me && (n || "").toLowerCase() === v); // v329
      return taken ? [['.sheet #cnin', "That name is taken: type a different one"], SHOWME] : [['.sheet [data-act="nameSave"]', "Type your name, then tap Save"], ['.sheet #cnin', "Type your commander name"], SHOWME]; }''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
