"""v820: one voice at a time (owner video: on login the hologram read a lore line, the full-screen portrait held the screen and a toast
followed, all over the open Events page; owner chose all six suggestions: a single queue, quiet while a page is open or just after login,
lore to an Advisor log, the full portrait only for story beats, a Welcome back card, an Advisor chatter setting). See p820_adv.js."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p820_adv.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p820.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 819;", "const GAME_V = 820;")
rep("/* v328 celebrations: queued in S.celeb,", C + "\n/* v328 celebrations: queued in S.celeb,")
# news: queued with a priority (milestones and live events Important; greetings go to the welcome card); no duplicate toast
rep('G.newsQ.shift(); const L = ADV_NEWS[n.id]; if (!/^(x|greet)_/.test(n.id)) note(L.replace(/^Commander, /, ""), "info"); advHolo(L);',
    'G.newsQ.shift(); const L = ADV_NEWS[n.id]; if (/^greet/.test(n.id)) { G.wbGreet = L; advLog(L, "greet"); } else advQueue(L, n.act || /^x_/.test(n.id) ? 2 : 1, n.act ? "live" : "news"); /* v820 */')
# the news pump waited for the hologram; it now only waits for the tutorial, battles and the dialog
rep('if (tutOn() || battle || advLines || $("#adv") || $("#celeb") || $("#advh.on") || (G3 && G3.cam && G3.cam.cine) || document.hidden) return; // wait for a calm moment',
    'if (tutOn() || battle || advLines || $("#adv") || $("#celeb") || document.hidden) return; /* v820 the queue picks the calm moment */')
# a record found in passing is logged, not read aloud over whatever is open; tapping into the Archives still reads it
rep("if (!quiet) archSeq(lv === 1 ? E.enc : E.def);", 'if (!quiet) { if (advTapped() || (sheet && sheet.type === "archives")) archSeq(lv === 1 ? E.enc : E.def); else advLog(`${E.t}: ${(lv === 1 ? E.enc : E.def)[0] || ""}`, "lore"); } /* v820 */')
# story beats wait for a calm moment and the map
rep('function flushSay0() { if (S.say.length && !battle && !(sheet && sheet.type === "faction") && !$("#oldw")) { /* v330: not behind the old-server card */ const l = S.say.splice(0); dirty(); say(l); } }',
    'function flushSay0() { if (S.say.length && !battle && !(sheet && sheet.type === "faction") && !$("#oldw") && (tutOn() || !S.intro || advCalmSay())) { /* v330: not behind the old-server card; v820 not over a page or just after login */ const l = S.say.splice(0); dirty(); G.sayPass = 1; try { say(l); } finally { G.sayPass = 0; } } }')
# the online bonus toast waits until the welcome card has had its say
rep("if (hit >= 0) note(`Online Bonus:", "if (hit >= 0 && Date.now() - (G.readyAt || 0) > 150000) note(`Online Bonus:")
# the log page and the chatter setting next to the voice toggle
rep("mastery: () => `<div class=\"hd\">", "advlog: shAdvLog, mastery: () => `<div class=\"hd\">")
rep('${tg("voiceToggle", VOICE.on, "Advisor voice")}', '${tg("voiceToggle", VOICE.on, "Advisor voice")}${advChRow()}')
rep('${tglRow("voiceToggle", VOICE.on, "Advisor voice")}', '${tglRow("voiceToggle", VOICE.on, "Advisor voice")}${advChRow()}')
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s); print("ok")
