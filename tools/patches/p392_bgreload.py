# Feedback triage 2026-11-10: false "Restarted after 0 min in the background" crash rows.
#  On a reload (Update now, desktop-site reload, Reconnect) the browser fires pagehide and THEN visibilitychange(hidden)
#  (HTML spec order; confirmed in Chromium). pagehide cleared udf.bg, the hidden event wrote it straight back, so the next
#  launch reported a background restart of 0 min. Three of the five iPhone rows on 2026-11-10 were update reloads (v386->387,
#  v387->389, v389->390). Now pagehide marks the page as unloading and the hidden handler skips the write.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
rep('''document.addEventListener("visibilitychange", () => { try { if (document.hidden) localStorage.setItem("udf.bg",''',
    '''document.addEventListener("visibilitychange", () => { try { if (document.hidden && window.__udfUnload) return; if (document.hidden) localStorage.setItem("udf.bg",''')
rep('''addEventListener("pagehide", e => { try { if (!e.persisted) localStorage.removeItem("udf.bg"); } catch (er) {} });''',
    '''addEventListener("pagehide", e => { try { if (!e.persisted) { window.__udfUnload = 1; localStorage.removeItem("udf.bg"); } } catch (er) {} }); /* v392: pagehide comes before the hidden event on a reload */
addEventListener("pageshow", () => { window.__udfUnload = 0; });''')
open(p, "w").write(t)
