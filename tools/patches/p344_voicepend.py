# v344: Academy voice on a fresh page load. The current step's line plays as the game opens, before any tap, and phones refuse sound
# then; the line was marked as spoken and never came back (a player waiting on one step heard nothing at all). A refused line now waits
# and plays on the first tap (within 3 minutes). Also: the unlock listened on pointerdown, which on touch screens comes BEFORE the
# browser allows sound (Chrome grants it on touchend/click/pointerup), so the silent unlock clip was refused and retried; now it waits
# for the end of the tap.
p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,(h.count(a),a[:70]); h=h.replace(a,b)
rep('["pointerdown", "touchend", "click", "keydown"].forEach(t => document.removeEventListener(t, voiceUnlock, true)); };',
    '["pointerup", "touchend", "click", "keydown"].forEach(t => document.removeEventListener(t, voiceUnlock, true)); };')
rep('["pointerdown", "touchend", "click", "keydown"].forEach(t => document.addEventListener(t, voiceUnlock, true));',
    '''["pointerup", "touchend", "click", "keydown"].forEach(t => document.addEventListener(t, voiceUnlock, true));
/* a line the browser refused (no tap yet) plays on the next tap instead of being lost */
function voicePendTap() { const p = VOICE.pend; if (!p) return; VOICE.pend = null; if (performance.now() - p.t > 180000 || !VOICE.on || (typeof AU !== "undefined" && AU.muted)) return; const a = VOICE.el; if (a && !a.paused && a.currentTime > .15) return; /* it did start after all */ if ($("#adv") || (advLines && advLines[0] === p.line)) speak(p.line); else advHolo(p.line); /* her hologram comes back with the line */ }
["pointerup", "touchend", "click", "keydown"].forEach(t => document.addEventListener(t, voicePendTap, true));''')
rep('a.onplay = () => voiceTalk(1); a.onended = a.onpause = a.onerror = () => voiceTalk(0); a.play().catch(() => voiceTalk(0)); } catch (e) {} }',
    'VOICE.pend = (navigator.userActivation && !navigator.userActivation.hasBeenActive) ? { line, t: performance.now() } : null; /* no tap yet: the browser will refuse or hold it */ a.onplay = () => voiceTalk(1); a.onended = a.onpause = a.onerror = () => voiceTalk(0); a.play().catch(e => { voiceTalk(0); if (e && e.name === "NotAllowedError" && VOICE.au === a) VOICE.pend = { line, t: performance.now() }; }); } catch (e) {} }')
rep("function voiceUnlock() { if (VOICE.unl) return;","function voiceUnlock() { if (VOICE.unl || VOICE.pend) return; /* a waiting line unlocks the player itself */")
rep('document.addEventListener("touchend", unlockAudio, { passive: true });','document.addEventListener("touchend", unlockAudio, { passive: true }); document.addEventListener("click", unlockAudio, { passive: true }); /* v344: Chrome allows sound from a finished tap, not its start */')
open(p,"w").write(h); print("ok")
