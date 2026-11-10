# fb-20261110: "Restarted after 0 min in the background" false crash reports.
# A reload (update, Reload button) fires pagehide (which cleared udf.bg) and THEN visibilitychange->hidden
# (which wrote udf.bg again), so the next launch reported a background kill. pagehide now marks the page as
# leaving and the hidden handler stands down; a launch on a newer version within 60 s of hiding is not reported.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('document.addEventListener("visibilitychange", () => { try { if (document.hidden) localStorage.setItem("udf.bg",',
  'document.addEventListener("visibilitychange", () => { try { if (document.hidden && window.__udfLeaving) return; if (document.hidden) localStorage.setItem("udf.bg",'),
 ('addEventListener("pagehide", e => { try { if (!e.persisted) localStorage.removeItem("udf.bg"); } catch (er) {} });',
  'addEventListener("pagehide", e => { try { if (!e.persisted) { window.__udfLeaving = 1; localStorage.removeItem("udf.bg"); } } catch (er) {} }); /* v402: reloads fire pagehide before the hidden event */\naddEventListener("pageshow", () => { window.__udfLeaving = 0; });'),
 ('if (bg && bg.t && !(G.lastCrashFresh)) { const gone = Date.now() - bg.t;',
  'if (bg && bg.t && !(G.lastCrashFresh)) { const gone = Date.now() - bg.t; if (bg.v && typeof GAME_V !== "undefined" && bg.v !== GAME_V && gone < 60e3) throw 0; /* v402: an update reload, not a kill */'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
