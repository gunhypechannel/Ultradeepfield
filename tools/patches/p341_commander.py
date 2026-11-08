# v341: during the Academy every time her voice comes on, the line opens with "Commander" (owner's request). Map: old line -> new line.
import json
M=json.load(open("tools/patches/p341_commander.json")); p="docs/index.html"; h=open(p).read(); miss=[]
for a,b in M.items():
    n=h.count(a)
    if not n: miss.append(a[:60]); continue
    h=h.replace(a,b)
open(p,"w").write(h); print("replaced", len(M)-len(miss), "missing", miss)
