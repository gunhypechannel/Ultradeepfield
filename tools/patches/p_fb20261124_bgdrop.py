# fb-20261124: crash report from the owner's Fold app (v738): the game sat on the Rank screen with the base world still
# alive behind it (~253 MB of textures), went to the background for 85 min and was closed ~5 s after coming back
# ("Closed unexpectedly after: back from the background (5106 s)"). In the Android app, going to the background now also
# releases the map and the base when they are NOT on screen (worldDrop never drops the world on screen); they are built
# again when you open them. Before the crumb that closes the session, so the session stays closed while hidden.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {}',
  '    if (/UDFApp\\//.test(navigator.userAgent) && !battle) { try { worldDrop("gal", "background, not on screen"); worldDrop("col", "background, not on screen"); } catch (e) {} } /* fb-20261124 Android app: off-screen worlds go while hidden */\n    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {}'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
