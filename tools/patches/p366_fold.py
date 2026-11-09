# v366: the desktop-site check ran only when the page loaded. The user's Fold diagnostic (v365): unfolded, Chrome showed 707 px on a 708 px
# screen (fine, no frame). Folding to the cover screen afterwards makes Chrome's desktop mode zoom the page out, and nothing re-checked.
# Now a resize that leaves the page 1.3x+ too wide (and not yet framed) saves the empire and reloads, so it comes back in the phone-width frame.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('''  window.__deskZ = zoomFor();
  if (!force && zoomFor() < 1.3) return;''', '''  window.__deskZ = zoomFor();
  if (!force && zoomFor() < 1.3) { var rt = 0, chk = function () { clearTimeout(rt); rt = setTimeout(function () { if (zoomFor() < 1.3 || window.__deskReloading) return; window.__deskReloading = 1; // folded after loading
      var go = function () { location.reload(); }; try { var b = window.__udfBeforeReload; if (b) { Promise.race([b(), new Promise(function (r) { setTimeout(r, 2500); })]).then(go, go); return; } } catch (e) {} go(); }, 700); };
    addEventListener("resize", chk); if (window.visualViewport) visualViewport.addEventListener("resize", chk); return; }''')
rep("async function flush() {", "window.__udfBeforeReload = async () => { try { dirty(); await flush(); } catch (e) {} }; // v366 a save before the desktop-site reload\nasync function flush() {")
open(p, "w").write(h); print("ok")
# and the pixel-ratio estimate is dropped (the Fold keeps its ratio; a low-ratio tablet would have been framed by mistake)
h = open(p).read(); a = '    if (dpr < 1.8 && mm("(hover:none)")) c.push(W * dpr / 2.6);\n'
if a in h: h = h.replace(a, ''); open(p, "w").write(h)
