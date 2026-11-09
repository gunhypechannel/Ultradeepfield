# v361: "Add to Home Screen" guide (docs/udf-install.js): an install button on the sign-in screen opens an animated walkthrough on a
# drawn phone for iPhone (Safari, iOS 26: ••• > Share > Add to Home Screen > Open as Web App > Add) and Android (Chrome: ⋮ > Add to
# Home screen / Install app > Install), with an Install now button when Chrome offers it. The game's install card gets the same guide.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('${mrow("Installed", STANDALONE ? "Yes, full screen" : "Running in the browser")}</div>',
    '${mrow("Installed", STANDALONE ? "Yes, full screen" : "Running in the browser")}${!STANDALONE && window.udfInstallGuide ? \'<button class="btn amber wide" data-act="instGuide">Show me how</button>\' : ""}</div>')
rep("const ACT = {\n  menu: () => ACT.nav({ v: \"cmd\" }),", "const ACT = {\n  instGuide: () => { try { window.udfInstallGuide && window.udfInstallGuide(); } catch (e) {} }, // v361\n  menu: () => ACT.nav({ v: \"cmd\" }),")
open(p, "w").write(h); print("ok")
