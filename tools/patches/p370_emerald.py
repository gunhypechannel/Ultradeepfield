# v370: the Emerald Geode skin's green ring was chopped off: its cut-out had lost the ring where it left the original picture and where
# background removal broke strands. docs/skins/emerald.webp was rebuilt from the original art (tools/skins/emerald_cut.py): the planet as
# before, the ring kept whole as glowing light and fading where the picture ends. Its cache version goes to 3 so devices fetch it again.
p = "docs/index.html"; h = open(p).read()
a = '"emerald.webp": 2,'; assert h.count(a) == 1; h = h.replace(a, '"emerald.webp": 3,')
open(p, "w").write(h); print("ok")
