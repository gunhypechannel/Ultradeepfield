import numpy as np, colorsys, os, math, random
from PIL import Image, ImageDraw, ImageFilter
D="/home/claude/ultradeepfield/docs/art/hull/"
ld=lambda f: np.asarray(Image.open(D+f+".webp").convert("RGB")).astype(np.float32)/255
lum=lambda x: (x*[.3,.59,.11]).sum(2,keepdims=True)
def tint(x, c, sat=1., gam=1., mix=1.):   # luminance-preserving recolour toward colour c
    L=lum(x)**gam; c=np.array(c)/255; t=np.clip(L*c*1.9,0,1)
    t=t+(np.clip(L-.55,0,1)/.45)**2*(1-t)*.85              # highlights run to white
    return np.clip(x*(1-mix)+t*mix,0,1)
def save(x,f):
    Image.fromarray((np.clip(x,0,1)*255).round().astype(np.uint8)).save(D+f+".webp",quality=84,method=6); print(f, os.path.getsize(D+f+".webp")//1024,"k")
g=ld("gold"); a=ld("amethyst"); d=ld("diamond"); r=ld("ruby")
save(tint(g,(232,118,62),gam=1.05),"copper")                               # copper plating
save(tint(g,(196,206,222),gam=1.0),"silver")                               # silver plating
save(tint(a,(40,90,255),gam=1.1),"cobalt")                                 # cobalt crystal
pk=tint(r,(255,105,200),gam=.8); pl=lum(pk); pk=np.clip(pl+(pk-pl)*1.35,0,1); save(pk,"pink")                                 # pink crystal
L=lum(a); ob=np.clip(L**1.5*.42,0,1)*np.array([.55,.45,.8])+np.clip(L-.5,0,1)**1.3*np.array([1.5,1.1,2.3])+.03   # obsidian: black glass, violet sheen on the facet edges
save(ob,"obsidian")
# glyph holo: diamond facets in cyan-teal, with glowing glyph runes and scanlines
h=tint(d,(40,230,255),gam=1.25,mix=.92); im=Image.fromarray((h*255).astype(np.uint8)); W=im.width
lay=Image.new("RGB",(W,W),(0,0,0)); dr=ImageDraw.Draw(lay); random.seed(7)
for gy in range(6):
  for gx in range(6):
    cx,cy=(gx+.5)*W/6,(gy+.5)*W/6; s=W/6*.28
    for _ in range(4):
      t=random.choice(["l","c","v","x"]); ox,oy=random.uniform(-s,s),random.uniform(-s,s)
      if t=="l": dr.line([cx+ox-s*.6,cy+oy,cx+ox+s*.6,cy+oy],fill=(120,255,255),width=3)
      elif t=="c": dr.arc([cx+ox-s*.5,cy+oy-s*.5,cx+ox+s*.5,cy+oy+s*.5],random.randint(0,180),random.randint(200,360),fill=(120,255,255),width=3)
      elif t=="v": dr.line([cx+ox-s*.4,cy+oy-s*.5,cx+ox,cy+oy+s*.5,cx+ox+s*.4,cy+oy-s*.5],fill=(160,255,240),width=3)
      else: dr.line([cx+ox-s*.4,cy+oy-s*.4,cx+ox+s*.4,cy+oy+s*.4],fill=(120,240,255),width=3); dr.line([cx+ox+s*.4,cy+oy-s*.4,cx+ox-s*.4,cy+oy+s*.4],fill=(120,240,255),width=3)
glow=np.asarray(lay.filter(ImageFilter.GaussianBlur(5))).astype(np.float32)/255*1.6+np.asarray(lay).astype(np.float32)/255
scan=(np.sin(np.arange(W)/W*math.pi*2*90)*.5+.5)[:,None,None]*.08
hx=np.clip(np.asarray(im).astype(np.float32)/255*.42*np.array([.6,.9,1.])+glow*1.1+scan*np.array([.2,1,1]),0,1)
save(hx,"glyph")
row=[Image.open(D+f+".webp").resize((240,240)) for f in ["copper","silver","cobalt","pink","obsidian","glyph"]]
s=Image.new("RGB",(1440,240)); [s.paste(x,(i*240,0)) for i,x in enumerate(row)]; s.save("derived.jpg",quality=85)
