# fb-20261127: false "Restarted after 0 min in the background" reports from a second copy of the game. The owner's
# Windows Edge report (v823, on galaxy) came less than a second after the page hid, on the same version, same window
# size: the hidden copy was still open and a new tab of the game was opened. Both copies share localStorage, so the new
# tab read the old tab's "udf.bg" note and reported a restart. Now a launch that finds the note first asks the other
# copies of the game (BroadcastChannel "udf.alive", 1.5 s); if any answers, it was not a restart and nothing is sent.
# A copy that is frozen or killed does not answer, so real restarts are still reported.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
A = 'if (gone < 30 * 60e3) hqPush({ kind: "crash", status: "new", at: Date.now(), now: typeof GAME_V !== "undefined" ? GAME_V : 0, bg: 1, text: `Restarted after ${Math.round(gone / 60000)} min in the background (on ${bg.view || "?"})`, beat: JSON.stringify(bg).slice(0, 1500), device: hqDev(), w: innerWidth, h: innerHeight }); } } catch (e) {}'
B = ('if (gone < 30 * 60e3) { const rr = { kind: "crash", status: "new", at: Date.now(), now: typeof GAME_V !== "undefined" ? GAME_V : 0, bg: 1, text: `Restarted after ${Math.round(gone / 60000)} min in the background (on ${bg.view || "?"})`, beat: JSON.stringify(bg).slice(0, 1500), device: hqDev(), w: innerWidth, h: innerHeight };'
     ' const ch = window.__udfAlive; if (!ch) hqPush(rr); else { let seen = 0; const on = e => { if (e.data && e.data.a) seen = 1; }; ch.addEventListener("message", on); ch.postMessage({ q: 1 });'
     ' setTimeout(() => { ch.removeEventListener("message", on); if (!seen) hqPush(rr); }, 1500); } /* fb-20261127: another open copy of the game answers, so this is a second tab, not a restart */ } } } catch (e) {}')
C = '/* v379: the app was in the background and then started fresh: on iPhone that is usually iOS closing it to free memory */'
D = ('/* fb-20261127: every running copy of the game answers "are you there?" so a second tab is not taken for a restart */\n'
     'try { if (typeof BroadcastChannel === "function") { window.__udfAlive = new BroadcastChannel("udf.alive"); window.__udfAlive.addEventListener("message", e => { try { if (e.data && e.data.q) window.__udfAlive.postMessage({ a: 1 }); } catch (er) {} }); } } catch (e) {}\n' + C)
for a, b in [(A, B), (C, D)]:
    assert t.count(a) == 1, a[:80]
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
