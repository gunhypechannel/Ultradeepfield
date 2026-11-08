# v354: models were off on the owner's Fold. The v346 crash guard took any session that ended while a model loaded as a crash and turned
# models off for 3 days, but closing the app, switching away or the reload after an update ends a session too. Now:
#  - a normal ending (pagehide, or the page going hidden) clears the "loading" note; a crash does not fire those events;
#  - it takes two such endings in a row (udfGlbCrash) to turn models off, and then for one day, and only for this version
#    (a new version tries again);
#  - the 3D loader is served from the site itself (docs/lib/GLTFLoader-r128.js, three.js r128 tag), not from a CDN.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>', '<script src="lib/GLTFLoader-r128.js"></script>')
rep('''  let ok = true; try { const busy = +localStorage.getItem("udfGlbBusy") || 0, off = +localStorage.getItem("udfGlbOff") || 0;
    if (busy && Date.now() - busy < 864e5) { localStorage.setItem("udfGlbOff", Date.now()); localStorage.removeItem("udfGlbBusy"); ok = false; try { crumb("models off: the last session ended while a model was loading"); } catch (e) {} }
    else if (off && Date.now() - off < 3 * 864e5) ok = false; } catch (e) {}''',
'''  let ok = true; try { const busy = +localStorage.getItem("udfGlbBusy") || 0, LS = localStorage; let off = {}; try { off = JSON.parse(LS.getItem("udfGlbOff2") || "{}") || {}; } catch (e) {} LS.removeItem("udfGlbOff");
    if (busy && Date.now() - busy < 864e5) { const n = (+LS.getItem("udfGlbCrash") || 0) + 1; LS.setItem("udfGlbCrash", n); LS.removeItem("udfGlbBusy"); try { crumb("model load cut off (" + n + ")"); } catch (e) {}
      if (n >= 2) { off = { t: Date.now(), v: GAME_V }; LS.setItem("udfGlbOff2", JSON.stringify(off)); LS.removeItem("udfGlbCrash"); try { crumb("models off for a day: the page died twice while a model loaded"); } catch (e) {} } }
    if (off.t && off.v === GAME_V && Date.now() - off.t < 864e5) ok = false; } catch (e) {}''')
rep('''function glbMark(on) { try { if (on) localStorage.setItem("udfGlbBusy", Date.now()); else localStorage.removeItem("udfGlbBusy"); } catch (e) {} }''',
'''function glbMark(on) { try { if (on) localStorage.setItem("udfGlbBusy", Date.now()); else localStorage.removeItem("udfGlbBusy"); } catch (e) {} }
/* v354 a normal ending (closing, switching away, reloading) is not a crash: clear the note; set it again if loading carries on */
window.addEventListener("pagehide", () => glbMark(false)); document.addEventListener("visibilitychange", () => { if (document.hidden) glbMark(false); else if (GLB_RUN || GLB_Q.length) glbMark(true); });''')
rep("const k = GLB_Q.shift(); GLB_RUN = 1; glbMark(true);", "const k = GLB_Q.shift(); GLB_RUN = 1; if (!document.hidden) glbMark(true);")
rep("clearTimeout(glbNext.t); glbNext.t = setTimeout(() => { if (!GLB_RUN && !GLB_Q.length) glbMark(false); }, 45000);", "clearTimeout(glbNext.t); glbNext.t = setTimeout(() => { if (!GLB_RUN && !GLB_Q.length) { glbMark(false); try { localStorage.removeItem(\"udfGlbCrash\"); } catch (e) {} } }, 45000);")
open(p, "w").write(h); print("ok")
