# v342: the owner's painted resource icons (metal, crystal, gas, energy) replace the line icons wherever RI is used. They sit inside the
# same 24x24 svg box, so every existing size rule still applies. The claude.ai artifact copy can't load site files, so it keeps the line icons.
p="docs/index.html"; h=open(p).read()
a="const RI = {"
assert h.count(a)==1
h=h.replace(a,'''const RI_IMG = !/claude|anthropic|usercontent/.test(location.hostname);
const RI = {''',1)
# after the RI object closes, swap in the painted icons
b="""  e: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2L5 14h6l-1 8 8-12h-6z"/></svg>'
};"""
assert h.count(b)==1
h=h.replace(b,b+"""
if (RI_IMG) for (const k of ["m", "c", "g", "e"]) RI[k] = `<svg viewBox="0 0 24 24" class="rimg" style="overflow:visible"><image href="icons/res-${k}.webp?v=1" x="-4" y="-4" width="32" height="32"/></svg>`;""")
open(p,"w").write(h); print("ok")
