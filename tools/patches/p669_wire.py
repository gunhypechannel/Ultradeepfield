# v669 the Wardrobe remastered: try-on before applying (owner: "is there anyway players can view their wardrobe items before they apply them?").
import sys, re
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
i = s.index('function shWardrobe() {'); j = s.index('\n\n/* ---------- v555 prestige caches', i)
s = s[:i] + R('p669_ward.js').rstrip('\n') + s[j:]
rep('  cwTab: d => { if (sheet && sheet.type === "wardrobe") { sheet.k = d.v; renderSheet(); } },', '''  cwTab: d => { if (sheet && sheet.type === "wardrobe") { sheet.k = d.v; sheet.sel = null; renderSheet(); } },
  cwSel: d => { if (!sheet || sheet.type !== "wardrobe") return; const def = cosDef(d.id), C = cosOf(); if (!def) return; sheet.sel = d.id; sheet.try = sheet.try || {}; sheet.try[def.k] = d.id; C.seen = C.seen || {}; if (C.own[d.id] && !C.seen[d.id]) { C.seen[d.id] = 1; dirty(); } try { SFX.click(); } catch (e) {} renderSheet(); }, /* v669 */
  cwTry: d => { if (!sheet || sheet.type !== "wardrobe") return; const def = cosDef(d.id); if (!def) return; sheet.try = sheet.try || {}; if (sheet.try[def.k] === d.id) delete sheet.try[def.k]; else sheet.try[def.k] = d.id; sheet.sel = d.id; renderSheet(); },
  cwRevert: () => { if (sheet) { sheet.try = {}; renderSheet(); } },
  cwSave: () => { if (!sheet || !sheet.try) return; const C = cosOf(); let n = 0; for (const [kk, id] of Object.entries(sheet.try)) { if (id && C.own[id]) { C.eq[kk] = id; n++; } else if (!id) { delete C.eq[kk]; n++; } } sheet.try = {}; dirty(); try { syncPlayer(); } catch (e) {} G.whlOff = null; const h = document.getElementById("advh"); if (h) h.remove(); toast(n ? `Look saved: ${n} item${n > 1 ? "s" : ""} equipped.` : "Nothing you own to save.", n ? "win" : "warn"); try { SFX.ok(); } catch (e) {} renderSheet(); },
  cwFilt: d => { if (sheet) { sheet.f = d.v; renderSheet(); } },''')
rep('  cwEq: d => { const C = cosOf();', '  cwEq: d => { const C = cosOf(); if (sheet && sheet.try) delete sheet.try[d.k];')
rep('.arfly{', R('p669.css').strip() + '\n.arfly{')
rep('const GAME_V = 668;', 'const GAME_V = 669;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
