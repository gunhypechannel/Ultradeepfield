# fb-20261125: crash report from Bacon Tempest (Android 10, Chrome browser, v759): the game sat on the Quests screen with
# the base world still alive behind it (~198 MB of textures), went to the background for 5 min and was closed within ~4 s
# of coming back ("Closed unexpectedly after: back from the background (324 s)"). Same pattern as the owner's Fold app
# report of 2026-11-24 (branch fb-20261124-0926, which covered only the Android app). Now every Android device (app and
# Chrome) releases the map and the base when they are NOT on screen as the page hides (worldDrop never drops the world on
# screen); they are built again when opened. This patch replaces p_fb20261124_bgdrop.py: apply one or the other, not both.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {}',
  '    if (ANDROID && !battle) { try { worldDrop("gal", "background, not on screen"); worldDrop("col", "background, not on screen"); } catch (e) {} } /* fb-20261125 Android (app and Chrome): off-screen worlds go while hidden */\n    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {}'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
