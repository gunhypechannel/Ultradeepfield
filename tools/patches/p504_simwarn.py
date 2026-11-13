# v504 the owner's ultimate-attack warnings in the Boss Lab previews too (v503 put them on the live map only).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('if (fa > .4) say("v4", "The wheel is aligning. Brace for impact!");', 'if (fa > .18) say("v3u", "The outer ring is accelerating. Multiple energy channels are activating."); if (fa > .5) say("v4", "Commander, MOVE THE FLEET! NOW!");')
rep('if (s > A0 + AL) say("v5", "We survived the blast.', 'if (s > A0 + AL) say("v4b", "The energy discharge has ended. I\'m analyzing the damage."); if (s > A0 + AL) say("v5", "We survived the blast.')
rep('if (s > 50) say("a4", "Its holographic shield is soaking our fire. Wait for the blade, then strike!");', 'if (s > 50) say("a4", "Holographic shield detected. Heavy weapons active. Avoid its frontal attack arc.");')
rep('if (fj > .35) say("k4",', 'if (fj > .15) say("k3u", "The sphere between its paws is developing an event horizon."); if (fj > .35) say("k4",')
rep('if (fc > .77 && !X.gz) { X.gz = 1; sbKillN(X, 14, t); say("m5", "Her gaze is sweeping the field... our ships are turning to stone!"); }',
    'if (fc > .25) say("m4u", "Massive energy accumulation detected within both ocular structures."); if (fc > .55) say("m4b", "BREAK FORMATION! HER EYES ARE CHARGING!"); if (fc > .77 && !X.gz) { X.gz = 1; sbKillN(X, 14, t); say("m5", "Her gaze is sweeping the field... our ships are turning to stone!"); } if (s > C0 + CL + 1) say("m5b", "Commander... the ancient accounts said her gaze turned armies to stone. We\'ve just witnessed the technological equivalent.");')
# the Archives' discoveries wait their turn: never during an owner preview, and never over a line she is already saying
rep('function archTick() { try { if (!S || !G.ready || battle) return;', 'function archTick() { try { if (!S || !G.ready || battle || G.sbSim || G.dvSim || G.convSim || G.wbShow) return;')
rep('function archSeq(L) { let i = 0; const step = () => { if (i >= L.length) return; const l = L[i++], t0 = Date.now(),', 'function archSeq(L) { let i = 0, tries = 0; const step = () => { if (i >= L.length) return; { const a = VOICE.au; if (tries++ < 120 && ((a && !a.paused && !a.ended) || (G.sbQ && G.sbQ.length) || ($("#advh.on") && G.holoCur !== L[i - 1]))) { setTimeout(step, 500); return; } } tries = 0; const l = L[i++], t0 = Date.now(),')
s2 = re.sub(r"GAME_V = 503\b", "GAME_V = 504", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
