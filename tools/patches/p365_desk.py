# v365: the v363 desktop-site frame didn't switch on for the user's Fold. v363 measured "how much too wide" from devicePixelRatio, which
# only works if Chrome lowers the pixel ratio; Chrome can instead keep it and zoom the whole page out. Now the phone width is the smallest of:
# the screen's own width (screen.width), the width actually shown (innerWidth x visualViewport.scale), and the pixel-ratio estimate (only
# when the ratio is low). A touch device counts as touch by maxTouchPoints or touch events. One diagnostic record per device (feedback,
# kind "diag") reports what Chrome says, so a miss can be seen.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('''  if (!force && !(/Linux/.test(ua) && !/Android|CrOS|Windows|Macintosh|iPhone|iPad/.test(ua) && navigator.maxTouchPoints > 0 && mm("(hover:none)") && mm("(pointer:coarse)"))) return;
  var zoomFor = function () { var dpr = window.devicePixelRatio || 1, W = innerWidth, T = Math.max(360, W * dpr / 2.6); return W / T; };''',
'''  var touch = navigator.maxTouchPoints > 0 || "ontouchstart" in window, handset = mm("(hover:none)") || mm("(any-hover:none)") || mm("(pointer:coarse)");
  if (!force && !(/Linux/.test(ua) && !/Android|CrOS|Windows|Macintosh|iPhone|iPad/.test(ua) && touch && handset)) return;
  var zoomFor = function () { var dpr = window.devicePixelRatio || 1, W = Math.max(innerWidth, document.documentElement.clientWidth || 0), vv = window.visualViewport, c = [];
    if (screen && screen.width > 200) c.push(innerWidth <= innerHeight ? Math.min(screen.width, screen.height || 1e9) : Math.max(screen.width, screen.height || 0));
    if (vv && vv.scale > 0 && vv.scale < .95) c.push(W * vv.scale);
    var T = Math.max(320, Math.min.apply(null, c.length ? c : [W])); return W / T; };
  window.__deskZ = zoomFor();''')
# the diagnostic: once per device, from a touch "Linux" browser (Chrome's desktop mode on Android), what it reports
rep("setInterval(() => { try { const C = G.lastCrash;", r'''setInterval(() => { try { if (G.diagSent || !G.db || !G.me || G.me === "local" || G.mode !== "online") return; const tu = /Linux/.test(navigator.userAgent) && !/Android/.test(navigator.userAgent) && (navigator.maxTouchPoints > 0 || "ontouchstart" in window); G.diagSent = 1;
  if (!tu || localStorage.getItem("udfDiag365")) return; localStorage.setItem("udfDiag365", "1"); let top = {}; try { const T = window.top; top = { iw: T.innerWidth, ih: T.innerHeight, dpr: T.devicePixelRatio, z: T.__deskZ, fr: T.__deskFrame || 0, vs: T.visualViewport && T.visualViewport.scale }; } catch (e) {}
  const mq = q => !!(window.matchMedia && matchMedia(q).matches); G.db.doc("feedback/diag-" + String(G.me).slice(0, 36) + "-" + Date.now().toString(36)).set({ kind: "diag", status: "new", by: G.me, at: Date.now(), now: GAME_V, device: navigator.userAgent.slice(0, 200),
    text: JSON.stringify({ framed: window.top !== window, iw: innerWidth, ih: innerHeight, dpr: devicePixelRatio, sw: screen.width, sh: screen.height, vs: window.visualViewport && visualViewport.scale, mtp: navigator.maxTouchPoints, hoverNone: mq("(hover:none)"), coarse: mq("(pointer:coarse)"), top }).slice(0, 900) }).catch(() => {}); } catch (e) {} }, 15000); // v365
setInterval(() => { try { const C = G.lastCrash;''')
open(p, "w").write(h); print("ok")
