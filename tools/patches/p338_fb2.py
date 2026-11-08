# v338: the floating Feedback button still opened mid-Academy: it reappears the moment a card closes or the guide hides, right
# under a finger that was tapping something else (the fleet chips sit in the same corner). It is now hidden for the whole Academy
# (Menu has Feedback) and ignores taps for 0.7 s after it reappears.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('body:has(#tutguide.acad[style*="block"]) #fbBtn,', 'body.acadon #fbBtn,body:has(#tutguide.acad[style*="block"]) #fbBtn,')
rep('function closeSheet() { sheetStack = [];', 'function closeSheet() { window.__shutAt = performance.now(); sheetStack = [];')
rep('  tutSupply(); try { pathBoostTopUp(); } catch (e) {}', '  tutSupply(); document.body.classList.toggle("acadon", tutOn()); try { pathBoostTopUp(); } catch (e) {}')
rep('document.getElementById("fbBtn").addEventListener("click", e => { e.stopPropagation(); open(); });',
    'document.getElementById("fbBtn").addEventListener("click", e => { e.stopPropagation(); if (performance.now() - (window.__shutAt || 0) < 700 || performance.now() - (window.__gdHideAt || 0) < 700) return; open(); }); /* v338: not a tap meant for something that just closed */')
rep('if (!el) { g.style.display = "none"; return requestAnimationFrame(guideFrame); }', 'if (!el) { if (g.style.display !== "none") window.__gdHideAt = performance.now(); g.style.display = "none"; return requestAnimationFrame(guideFrame); }')
open(p, 'w', encoding='utf-8').write(t); print('ok')
