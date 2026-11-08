import numpy as np, cv2
from PIL import Image, ImageFilter
W,H=640,360; rng=np.random.default_rng(11)
def trim(im):
    a=np.asarray(im.split()[3]); ys,xs=np.where(a>40); return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
cr=trim(Image.open("shard-crystal.webp").convert("RGBA")); full=trim(Image.open("shard-icon.webp").convert("RGBA"))
def space(seed):
    r=np.random.default_rng(seed); a=np.zeros((H,W,3),np.float32); yy,xx=np.mgrid[0:H,0:W]
    for (cx,cy,rad,col,w) in [(320,230,230,(110,40,190),.30),(110,70,140,(40,60,160),.12),(560,90,150,(150,40,160),.10)]: a+=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*rad*rad))[...,None]*np.array(col)*w
    for _ in range(450): x,y=r.integers(0,W),r.integers(0,H); a[y,x]+=r.uniform(60,255)
    a+=np.array([4,3,10]); return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.5)).convert("RGBA")
def put(c, im, h, cx, cy, rot):
    w=int(im.width*h/im.height); t=im.resize((w,int(h)),Image.LANCZOS).rotate(rot,resample=Image.BICUBIC,expand=True); c.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2)))
# rows of a heap, back to front: (count per row); the shard height shrinks a little toward the back
T=[("pouch",[3],0),("satchel",[3,4],0),("crate",[3,4,5],0),("vault",[4,5,6,7],150),("hoard",[5,6,7,8,9],175),("treasury",[6,7,8,9,10,11],205)]
tiles=[]
for i,(nm,rows,hero) in enumerate(T):
    c=space(i+5); R=len(rows); base=318; hs={1:150,2:128,3:108}.get(R,max(54,112-12*R))
    if hero: put(c, full, hero*1.2, 320, max(hero*.62, base-R*hs*.42-hero*.42), 0)
    for ri,cnt in enumerate(rows):
        depth=(R-1-ri)/max(1,R-1) if R>1 else 0; h=hs*(1-.22*depth); y=base-(R-1-ri)*hs*.42-h*.32 - (40 if R<=3 else 0); span=cnt*h*.52
        for j in range(cnt):
            x=320+(j-(cnt-1)/2)*(span/max(1,cnt-1) if cnt>1 else 0)+rng.normal(0,5); put(c, cr, h*rng.uniform(.9,1.08), x, y+rng.normal(0,4), rng.uniform(-28,28))
    c=c.convert("RGB"); c.save(f"pack-shards-{nm}.webp",quality=88,method=6); tiles.append(np.asarray(c.resize((320,180))))
Image.fromarray(np.vstack([np.hstack(tiles[:3]),np.hstack(tiles[3:])])).save("piles_prev.png")
