# v350: the Academy Complete / Flagship Commissioned cards showed only the top of the Advisor's hair. Her portrait (330x1219, full length)
# was stretched across the full card width as a 200px-tall banner (cover, top), so the frame held the top ~16% of a 3x-enlarged picture.
# It is now a centred head-and-shoulders frame (about 220px wide, cropped from the top of the picture), at under 2x enlargement.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("#celeb .cbart.adv{max-height:min(200px,24vh);object-fit:cover;object-position:top;border-radius:12px}#celeb .cbart{max-height:min(200px,26vh)}",
    "#celeb .cbart{max-height:min(200px,26vh)}#celeb .cbart.adv{display:block;margin:0 auto;width:auto;height:min(200px,24vh);max-height:none;aspect-ratio:1/1.05;object-fit:cover;object-position:50% 3%;border-radius:12px;border:1px solid rgba(255,200,120,.35)}")
open(p, "w").write(h); print("ok")
