"""Motion audit: every continuous spin in docs/index.html as seconds per turn, fastest first.
  rotation.x/y/z = <t|T|ts|time...> * k      (k radians per ms -> 2*pi/(k*1000) s per turn; ts in seconds handled when the variable is ts)
  rotation.x/y/z += k                        (per frame at 60 fps -> 2*pi/(k*60) s per turn)
  CSS: animation: <name> <N>s ... infinite where @keyframes <name> rotates a full turn -> N s per turn
python3 tools/motion/audit.py [limit_seconds] -> lists anything faster than the limit (default 30 s per turn)."""
import re, sys, math
s = open("docs/index.html", encoding="utf-8").read(); lim = float(sys.argv[1]) if len(sys.argv) > 1 else 30
line_of = lambda i: s.count("\n", 0, i) + 1
out = []
for m in re.finditer(r"rotation\.([xyz])\s*=\s*(-?)\(?\s*([A-Za-z_][\w.]*)\s*\*\s*([0-9.]+(?:e-?[0-9]+)?)", s):
    v, k = m.group(3), float(m.group(4))
    if not k: continue
    per = 1 if v in ("ts", "tsec", "sec") else 1000  # ts: seconds
    if v not in ("t", "T", "ts", "tNow", "now", "tt", "time", "t0", "tm", "ms") and not v.endswith(".t"): continue
    out.append((2 * math.pi / (k * per), line_of(m.start()), m.group(0)[:70]))
for m in re.finditer(r"rotation\.([xyz])\s*\+=\s*([0-9.]+(?:e-?[0-9]+)?)\s*[;,)}]", s):
    k = float(m.group(2))
    if k: out.append((2 * math.pi / (k * 60), line_of(m.start()), m.group(0)[:70]))
kf = {}
for m in re.finditer(r"@keyframes\s+([\w-]+)\s*\{(.*?)\}\s*\}", s, re.S):
    if re.search(r"rotate\((?:360deg|1turn|-360deg)\)|rotate[XYZ]?\(\s*-?360deg", m.group(2)): kf[m.group(1)] = 1
for m in re.finditer(r"animation:\s*([\w-]+)\s+([0-9.]+)s[^;}]*infinite", s):
    if m.group(1) in kf: out.append((float(m.group(2)), line_of(m.start()), "css " + m.group(0)[:70]))
out.sort()
fast = [o for o in out if o[0] < lim]
print(f"{len(out)} continuous spins found; {len(fast)} faster than one turn per {lim:g} s")
for sec, ln, src in fast: print(f"{sec:7.1f} s/turn  line {ln:6d}  {src}")
