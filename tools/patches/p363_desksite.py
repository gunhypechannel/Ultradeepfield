# v363: Chrome's "desktop site" mode on Android (the default on big screens like a Fold's inner screen, and it can stick on the cover screen)
# reports a Linux desktop and ignores the viewport tag, so the game laid itself out ~980 px wide and everything was tiny. When a touch-only
# (hover:none, pointer:coarse) Linux browser shows a page much wider than its screen, the page stops loading itself and shows the game in a
# full-screen frame that is phone-width and scaled up (CSS zoom). Inside the frame the browser treats the frame as the screen, so layout rules,
# vw/vh, taps and the pixel ratio (sharp 3D) are all native. The frame follows folding, unfolding and rotation. ?nodesk=1 turns it off;
# ?desktest=1 forces it (testing). Website only: the line sits in the head part the artifact build drops.
p = "docs/index.html"; h = open(p).read()
a = "<title>Ultra Deep Field</title>\n"
assert h.count(a) == 1
js = r'''<script>/* v363 Chrome "desktop site" on Android phones: show the game in a phone-width frame */(function () { try {
  var q = location.search, force = /[?&]desktest=1/.test(q); if (window.top !== window.self || /[?&]nodesk=1/.test(q)) return;
  var ua = navigator.userAgent, mm = function (x) { return !!(window.matchMedia && matchMedia(x).matches); };
  if (!force && !(/Linux/.test(ua) && !/Android|CrOS|Windows|Macintosh|iPhone|iPad/.test(ua) && navigator.maxTouchPoints > 0 && mm("(hover:none)") && mm("(pointer:coarse)"))) return;
  var zoomFor = function () { var dpr = window.devicePixelRatio || 1, W = innerWidth, T = Math.max(360, W * dpr / 2.6); return W / T; };
  if (!force && zoomFor() < 1.3) return;
  window.stop(); window.__deskFrame = 1;
  document.documentElement.innerHTML = '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#05090f"><title>Ultra Deep Field</title><link rel="manifest" href="manifest.webmanifest">' +
    '<style>html,body{margin:0;height:100%;overflow:hidden;background:#05090f}iframe{position:fixed;left:0;top:0;border:0;display:block;background:#05090f}</style></head><body></body>';
  var f = document.createElement("iframe"); f.title = "Ultra Deep Field"; f.allow = "fullscreen; autoplay; clipboard-read; clipboard-write; screen-wake-lock; web-share; gamepad"; f.setAttribute("allowfullscreen", "");
  var fit = function () { var z = Math.max(1, zoomFor()); f.style.zoom = z; f.style.width = Math.round(innerWidth / z) + "px"; f.style.height = Math.round(innerHeight / z) + "px"; };
  fit(); addEventListener("resize", fit); addEventListener("orientationchange", function () { setTimeout(fit, 250); }); if (window.visualViewport) visualViewport.addEventListener("resize", fit);
  f.src = location.href; document.body.appendChild(f);
} catch (e) {} })();</script>
'''
h = h.replace(a, a + js)
open(p, "w").write(h); print("ok")
