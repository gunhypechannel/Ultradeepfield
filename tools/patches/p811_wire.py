"""v811: a phone in "desktop site" mode is still a phone. Its browser reports a desktop user agent (X11 Linux, not mobile), so the game
treated it as a computer: no pixel budget, render scale up to 2.5 x the frame zoom (one report: 327x597 at ~7.5x, ~11M pixels a frame,
3x the phone budget) and none of the weak-phone settings. A touch screen with no hover and a coarse pointer now counts as mobile."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 810;", "const GAME_V = 811;")
rep("const MOBILE = IOS || ANDROID || /Mobi/i.test(navigator.userAgent) || !!(navigator.userAgentData && navigator.userAgentData.mobile),",
    "const MOBILE = IOS || ANDROID || /Mobi/i.test(navigator.userAgent) || !!(navigator.userAgentData && navigator.userAgentData.mobile) || (() => { try { return (navigator.maxTouchPoints || 0) > 0 && matchMedia(\"(pointer: coarse)\").matches && matchMedia(\"(hover: none)\").matches; } catch (e) { return false; } })(), /* v811 desktop-site mode */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
