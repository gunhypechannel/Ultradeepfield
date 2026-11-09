# v372: flagship hero portrait fits its frame (absolute box + object-fit:contain, never squashed or cropped)
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, (t.count(a), a[:80]); t = t.replace(a, b)
rep('#sheetwrap[data-type="flagship"] .fshero img{animation:fsFloat 7s ease-in-out infinite;width:84%;max-width:600px}',
    '#sheetwrap[data-type="flagship"] .fshero img{animation:fsFloat 7s ease-in-out infinite;position:absolute;left:6%;top:-11%;width:88%;height:120%;max-width:none;max-height:none;margin:0;object-fit:contain;object-position:50% 50%}')
open(p, "w").write(t)
