# fb-20261112: false "Closed unexpectedly after: background: N drawing buffers released" crash reports (v425+, iPhone).
# Going to the background marks the flight log closed (CRUMBS.open = false), but bgDiet's crumb() runs after that listener
# and crumb() sets open = true again, so every normal trip to the background was reported as a crash on the next launch.
# The diet now marks the log closed again after its crumb. Real background kills still report via udf.bg ("Restarted after N min").
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
a = '    try { crumb("background: " + n + " drawing buffers released"); } catch (e) {} }\n'
b = '    try { crumb("background: " + n + " drawing buffers released"); CRUMBS.open = false; crumbSave(); } catch (e) {} } /* fb-20261112: crumb() reopened the log, so every background trip read as a crash */\n'
assert t.count(a) == 1
t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
