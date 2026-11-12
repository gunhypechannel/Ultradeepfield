# fb-20261112: false and duplicate "Closed unexpectedly after: background: N drawing buffers released" crash reports (iPhone).
# (1) On hide, the flight-log listener marks the session closed, then bgDiet (registered later) calls crumb(), which set
#     CRUMBS.open = true again, so every normal background clean-up by iOS looked like a crash, however long the player was away.
#     bgDiet now closes the session again after its crumb (a kill in the background is still reported by the v379/v402
#     "Restarted after N min in the background" path, under 30 min only, as the owner chose).
# (2) A launch that found a dead session only cleared it on the first crumb/heartbeat; a launch closed within seconds left it
#     in place and the next launch queued the same crash again. The fresh flight log is saved at once, and a crash whose
#     died time was already queued (udf.crashDied) is not queued twice.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('try { crumb("background: " + n + " drawing buffers released"); } catch (e) {} }',
  'try { crumb("background: " + n + " drawing buffers released"); CRUMBS.open = false; crumbSave(); } catch (e) {} } /* fb-20261112: the crumb must not reopen a session that just went to the background */'),
 ('CRUMBS = { open: true, t0: Date.now(), ev: [] };\n',
  'CRUMBS = { open: true, t0: Date.now(), ev: [] }; try { localStorage.setItem(CRUMB_K, JSON.stringify(CRUMBS)); } catch (e) {} /* fb-20261112: the dead session is reported once */\n'),
 ('if (G.lastCrashFresh && G.lastCrash && G.lastCrash.ev) { const C = G.lastCrash, b = C.beat || {}, last = C.ev[C.ev.length - 1]; G.crashSent = 1; G.lastCrashFresh = 0; /* queued: the old one-shot sender stands down */\n  hqPush({',
  'if (G.lastCrashFresh && G.lastCrash && G.lastCrash.ev) { const C = G.lastCrash, b = C.beat || {}, last = C.ev[C.ev.length - 1]; G.crashSent = 1; G.lastCrashFresh = 0; /* queued: the old one-shot sender stands down */\n  const dk = String(b.t || (last && last[0]) || 0); let dup = 0; try { dup = localStorage.getItem("udf.crashDied") === dk; localStorage.setItem("udf.crashDied", dk); } catch (e) {} /* fb-20261112 */\n  if (!dup) hqPush({'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
