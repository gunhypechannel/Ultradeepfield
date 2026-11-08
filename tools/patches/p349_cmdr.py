# v349: "Commander" scaled back (owner: keep it where it fits naturally). v341 opened 110 lines with it; 96 go back to their original
# wording (the building/ship/research card lines, routine Academy steps). Their original clips never left docs/voice (same text -> same
# key), so no re-recording. Kept on 14 lines where she addresses you at a moment that calls for it (naming the capital, the first spy run
# and attack, the second-world goal, raiders, battle results, the scout report, the homeworld balance and Academy-complete lines).
# Map: p349_cmdr.json = [new, old, new_key, old_key]. Also restores tools/voice_lines.json, voicelab and voicecheck to the old lines.
import json, re, html
rev = json.load(open("tools/patches/p349_cmdr.json"))
p = "docs/index.html"; h = open(p).read()
for n, o, kn, ko in rev:
    a, b = json.dumps(n, ensure_ascii=False)[1:-1], json.dumps(o, ensure_ascii=False)[1:-1]
    assert h.count(a) >= 1, a[:60]; h = h.replace(a, b)
open(p, "w").write(h)
L = json.load(open("tools/voice_lines.json")); m = {kn: (ko, o) for n, o, kn, ko in rev}
for x in L:
    if x["key"] in m: x["key"], x["line"] = m[x["key"]][0], m[x["key"]][1]
open("tools/voice_lines.json", "w").write(json.dumps(L, indent=1, ensure_ascii=False) + "\n")
p = "docs/voicelab.html"; s = open(p).read()
s = re.sub(r"const LINES = \[.*?\];", lambda mm: "const LINES = " + json.dumps(L, ensure_ascii=False) + ";", s, count=1, flags=re.S); open(p, "w").write(s)
p = "docs/voicecheck.html"; s = open(p).read()
for n, o, kn, ko in rev: s = s.replace(f'data-k="{kn}"', f'data-k="{ko}"').replace(html.escape(n), html.escape(o))
open(p, "w").write(s); print("ok", len(rev))
