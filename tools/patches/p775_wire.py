"""v775: Medusara back to her pre-remodel model (owner: "put Medusara back to the old model, I don't really like the new one").
Her builder is restored exactly as it was in v761 (pale stone face and pale serpents fanned all round her, before v769 recoloured
her and gathered the serpents at her crown), and she is taken off the v774 surface-detail layer. Her battle camera was never
changed. Applies on top of v774."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
OLD = sys.argv[2] if len(sys.argv) > 2 else None
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
def fn(t):
    i = t.find("function medusara("); assert i > 0 and t.count("function medusara(") == 1
    e = min(x for x in (t.find("\n  function ", i + 10), t.find("\n  /*", i + 10)) if x > 0); return i, e
import subprocess
o = open(OLD, encoding="utf-8").read() if OLD else subprocess.run(["git", "show", "4938128:docs/index.html"], capture_output=True, text=True, check=True).stdout
oi, oe = fn(o); ni, ne = fn(s); s = s[:ni] + o[oi:oe] + s[ne:]
rep("const GAME_V = 774;", "const GAME_V = 775;")
rep(", matriarch: [2, 60], medusara: [2, 70] };", ", matriarch: [2, 60] };")
open(p, "w", encoding="utf-8").write(s)
print("ok")
