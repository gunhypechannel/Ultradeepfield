# v610: the Advisor's faces cut to two lip-synced families (calm, smile) with no odd expressions or mid-line head swaps,
# and Report a player (profile card and chat messages), next to the existing Block. See p610_advfix.js.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function afFace(line) { const m = advMood(line), t = String(line || "");'); j = s.index('/* the full-body poses */', i)
s = s[:i] + open('tools/patches/p610_advfix.js', encoding='utf-8').read() + s[j:]
rep('const AF_V = 609,', 'const AF_V = 610,')
# Report on the profile card, under Block
rep('<button class="btn ghost wide sm" data-act="${blocked ? "unblock" : "block"}" data-u="${uid}">${blocked ? "Unblock" : "Block messages from this commander"}</button>`',
    '<button class="btn ghost wide sm" data-act="${blocked ? "unblock" : "block"}" data-u="${uid}">${blocked ? "Unblock" : "Block messages from this commander"}</button><button class="btn ghost wide sm" data-act="reportU" data-u="${uid}">⚑ Report this commander</button>`')
# Report and Block on someone else's chat message (tap the message)
rep('<button class="crep2" data-act="chatReply" data-id="${m.id}">↩ Reply</button></div>`;',
    '<button class="crep2" data-act="chatReply" data-id="${m.id}">↩ Reply</button>${mine ? "" : `<button class="crep2" data-act="reportMsg" data-id="${m.id}" data-u="${esc(m.u)}">⚑ Report</button><button class="crep2" data-act="block" data-u="${esc(m.u)}">Block</button>`}</div>`;')
rep('  unblock: d => {', '  reportU: d => reportPlayer(d.u), reportMsg: d => reportPlayer(d.u, d.id), // v610\n  unblock: d => {')
s2 = re.sub(r"GAME_V = 609\b", "GAME_V = 610", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
