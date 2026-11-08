# v358: the Cube Destroyer goes back to its hand-built sphere (dark hull, red city lights, equator ring, dish). The Meshy sphere from
# v352 rendered as a noisy, spiky ball in battle. Its model files are removed.
import re
p = "docs/index.html"; h = open(p).read()
m = re.search(r'const GLB_SHIPS = new Set\(\[[^\]]*\]\)', h); s = m.group(0)
assert s.count('"worldbreaker"') == 1
s2 = re.sub(r',\s*"worldbreaker"|"worldbreaker",\s*', '', s, count=1); h = h.replace(s, s2)
h = re.sub(r'"worldbreaker":"[0-9a-f]+",?', '', h, count=1)
open(p, "w").write(h); print("ok")
h = open(p).read(); m = re.search(r'const GLB_V = \{[^}]*\}', h); h = h.replace(m.group(0), m.group(0).replace(',}', '}')); open(p, 'w').write(h)
