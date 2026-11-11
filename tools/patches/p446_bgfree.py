# v446 phones: going to the background also frees what the map rebuilds on its own when it is needed again (boss wreck sites and,
# outside a live Cube Devastation, the event's models), so the paused game holds less memory and the phone is less likely to close it
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("""    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {} if (!battle && G.stuCache)""",
"""    if (MOBILE && G3) { try { const X = G3.wbWk; if (X) { for (const S of X.sets) wreckDispose(S.grp); X.sets = []; X.at = 0; } } catch (e) {} try { if (G3.dv && !G.dvSim && !dvNow(now())) dvFree(G3); } catch (e) {} } /* v446 */
    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {} if (!battle && G.stuCache)""")
s, k = re.subn(r"GAME_V = 445\b", "GAME_V = 446", s); assert k == 1
open(P, 'w').write(s)
