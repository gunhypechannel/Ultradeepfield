# v364: the Mail header's buttons (New message, Mail all, Clear alerts) ran off the right edge on phones. They now wrap onto a second row,
# right-aligned, and the whole button row drops under the title when even that is too tight.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep(".mailhd{display:flex;justify-content:space-between;align-items:flex-end;gap:8px;margin:4px 0 8px}", ".mailhd{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:8px;margin:4px 0 8px}")
rep(".mailact{display:flex;gap:6px}", ".mailact{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;flex:1 1 220px;min-width:0}.mailact .btn{white-space:nowrap}")
open(p, "w").write(h); print("ok")
