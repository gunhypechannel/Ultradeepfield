"""Add voiced lines to the lists: python3 tools/voice_add.py new.json [replace_old_key]
new.json: [{"key","where","line"}]. Updates tools/voice_lines.json, voicelab LINES and voicecheck."""
import json, re, sys, html
new = json.load(open(sys.argv[1])); old = sys.argv[2] if len(sys.argv) > 2 else None
L = json.load(open("tools/voice_lines.json"))
if old: L = [x for x in L if x["key"] != old]
have = {x["key"] for x in L}; L += [x for x in new if x["key"] not in have]
open("tools/voice_lines.json", "w").write(json.dumps(L, indent=1, ensure_ascii=False) + "\n")
p = "docs/voicelab.html"; s = open(p).read()
s = re.sub(r"const LINES = \[.*?\];", lambda m: "const LINES = " + json.dumps(L, ensure_ascii=False) + ";", s, count=1, flags=re.S)
s = re.sub(r"All \d+ Advisor lines", f"All {len(L)} Advisor lines", s)
open(p, "w").write(s)
p = "docs/voicecheck.html"; s = open(p).read()
items = re.findall(r'<li data-k="([a-z0-9]+)">.*?<small>\d+ · (.*?)</small><span>(.*?)</span></div></li>', s)
items = [(k, w, t) for k, w, t in items if k != old]
ks = {k for k, _, _ in items}; items += [(x["key"], html.escape(x["where"]), html.escape(x["line"])) for x in new if x["key"] not in ks]
ol = "".join(f'<li data-k="{k}"><button aria-label="Play">▶</button><div><small>{i + 1} · {w}</small><span>{t}</span></div></li>' for i, (k, w, t) in enumerate(items))
s = re.sub(r'(<ol id="l">).*?(</ol>)', lambda m: m.group(1) + ol + m.group(2), s, count=1, flags=re.S)
s = re.sub(r"\b\d+ lines", f"{len(items)} lines", s, count=1); open(p, "w").write(s); print(len(L), "lines in lab;", len(items), "in voicecheck")
