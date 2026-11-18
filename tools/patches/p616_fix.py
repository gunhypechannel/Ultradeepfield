# v616 (owner: "Remove spider monsters, and I hate how [renaming] a planet is on the top but the save is scrolled all the way to the
# bottom, it should be easier to rename a planet"). (1) The Gravity Spider joins the retired species (monGone; out of the Bestiary).
# (2) Rename & reskin: a Save button right beside the name box, Enter saves, and the Save button at the bottom stays on screen.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const monGone = x => x.mon === "slevi" || x.mon === "ctort";', 'const monGone = x => x.mon === "slevi" || x.mon === "ctort" || x.mon === "gspider"; /* v616 the Gravity Spider too */')
rep('"b_swasp", "b_gspider", ', '"b_swasp", ')
rep('<h2 class="sec">Name</h2><input class="minput" id="pname" maxlength="20" value="${esc(nm)}" aria-label="Planet name">',
    '<h2 class="sec">Name</h2><div class="pnrow"><input class="minput" id="pname" maxlength="20" value="${esc(nm)}" aria-label="Planet name" enterkeyhint="done"><button class="btn amber" data-act="skinSave">Save</button></div>')
rep('    <button class="btn wide" data-act="skinSave">Save ${esc(p.kind === "home" ? "homeworld" : "colony")}</button>`;',
    '    <div class="skbar"><button class="btn wide amber" data-act="skinSave">Save ${esc(p.kind === "home" ? "homeworld" : "colony")}</button></div>`;')
css = '.pnrow{display:flex;gap:8px;align-items:stretch}.pnrow .minput{flex:1;min-width:0}.pnrow .btn{flex:none;min-width:84px}\n.skbar{position:sticky;bottom:calc(40px + env(safe-area-inset-bottom,0px));z-index:5;margin:12px 0 0;padding:6px 0;background:none}.skbar .btn{background:linear-gradient(#3d2c08,#1f1504);box-shadow:0 6px 20px rgba(0,0,0,.7)}\n'
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
rep('document.addEventListener("keydown", e => { if (e.key === "Escape") {', 'document.addEventListener("keydown", e => { if (e.key === "Enter" && e.target && e.target.id === "pname") { e.preventDefault(); try { ACT.skinSave(); } catch (er) {} return; } /* v616 Enter saves the name */ if (e.key === "Escape") {')
s2 = re.sub(r"GAME_V = 615\b", "GAME_V = 616", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
