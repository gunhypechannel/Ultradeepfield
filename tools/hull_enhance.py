import numpy as np, os
from PIL import Image, ImageFilter
A="/mnt/user-data/attachments/59785d42-49cf-5378-902e-179290e8c617/"
M={"ruby":"9af2628c","emerald":"9abfebac","diamond":"b0cf8434","amethyst":"feea5a09","gold":"cb84e7e1"}
OUT="/home/claude/ultradeepfield/docs/art/hull/"
def usm(im, r, a):
    b=np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32)/255; o=np.asarray(im).astype(np.float32)/255
    return np.clip(o+(o-b)*a,0,1)
row=[]
for f,h in M.items():
    im=Image.open(A+h+"-image.png").convert("RGB").resize((768,768),Image.LANCZOS)
    x=usm(im,24,.55)                                         # clarity: big local contrast
    x=usm(Image.fromarray((x*255).astype(np.uint8)),1.4,1.0) # crisp facet edges
    L=(x*[.3,.59,.11]).sum(2,keepdims=True)
    sat={"diamond":1.12,"gold":1.2}.get(f,1.32)
    x=np.clip(L+(x-L)*sat,0,1)                               # vivid colour
    x=np.clip(x,0,1); x=x*x*(3-2*x)*.55+x*.45                # S-curve: deeper shadows, brighter highlights
    hi=np.clip((L-.62)/.38,0,1)**1.5; x=np.clip(x+hi*.18,0,1)# highlights pop
    o=Image.fromarray((x*255).round().astype(np.uint8)); o.save(OUT+f+".webp",quality=84,method=6)
    print(f, os.path.getsize(OUT+f+".webp")//1024,"k"); row.append((im.resize((300,300)),o.resize((300,300))))
s=Image.new("RGB",(1500,600))
for i,(a,b) in enumerate(row): s.paste(a,(i*300,0)); s.paste(b,(i*300,300))
s.save("cmp.jpg",quality=85)
