# Pack art composed from the game's own paintings (backgrounds) and painted icons (materials, resources). 640x360 webp.
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np, colorsys
D="/home/claude/ultradeepfield/docs/"; W,H=640,360
def bg(path, focus=0.45):
    im=Image.open(D+path).convert("RGB"); w,h=im.size; s=max(W/w,H/h); im=im.resize((int(w*s+1),int(h*s+1)),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*focus); im=im.crop((x,y,x+W,y+H))
    im=ImageEnhance.Brightness(im).enhance(.62); im=ImageEnhance.Color(im).enhance(1.15)
    g=np.zeros((H,W,4),np.uint8); ys=np.linspace(0,1,H)[:,None]; g[...,3]=(np.clip((ys-.35)/.65,0,1)*190).astype(np.uint8).repeat(W,1)
    im=im.convert("RGBA"); im.alpha_composite(Image.fromarray(g,"RGBA")); return im
def icon(path, size, hue=None, glow=None):
    im=Image.open(path).convert("RGBA").resize((size,size),Image.LANCZOS)
    if hue is not None:
        a=np.asarray(im).astype(np.float32)/255; r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
        mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b); v=mx; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
        h=np.full_like(v,hue); i=(h*6).astype(int)%6; f=h*6-np.floor(h*6); p=v*(1-s); q=v*(1-f*s); t=v*(1-(1-f)*s)
        R=np.choose(i,[v,q,p,p,t,v]); G=np.choose(i,[t,v,v,q,p,p]); B=np.choose(i,[p,p,t,v,v,q])
        im=Image.fromarray((np.dstack([R,G,B,al])*255).astype(np.uint8),"RGBA")
    if glow:
        al=np.asarray(im.split()[3]).astype(np.float32); pad=size//4; big=np.zeros((size+2*pad,size+2*pad),np.float32); big[pad:pad+size,pad:pad+size]=al
        import cv2; bl=cv2.GaussianBlur(big,(0,0),size/9)*.9; gl=np.dstack([np.full_like(bl,glow[0]),np.full_like(bl,glow[1]),np.full_like(bl,glow[2]),np.clip(bl,0,255)]).astype(np.uint8)
        out=Image.fromarray(gl,"RGBA"); out.alpha_composite(im,(pad,pad)); return out
    return im
def tile(path, size, col):
    im=Image.open(path).convert("RGBA").resize((size,size),Image.LANCZOS); m=Image.new("L",(size,size),0); ImageDraw.Draw(m).rounded_rectangle((0,0,size-1,size-1),radius=size//6,fill=255)
    im.putalpha(m); ImageDraw.Draw(im).rounded_rectangle((1,1,size-2,size-2),radius=size//6,outline=col+(255,),width=max(2,size//40))
    import cv2; pad=size//4; al=np.zeros((size+2*pad,size+2*pad),np.float32); al[pad:pad+size,pad:pad+size]=np.asarray(m,np.float32); bl=np.clip(cv2.GaussianBlur(al,(0,0),size/8)*.85,0,255)
    gl=Image.fromarray(np.dstack([np.full_like(bl,col[0]),np.full_like(bl,col[1]),np.full_like(bl,col[2]),bl]).astype(np.uint8),"RGBA"); gl.alpha_composite(im,(pad,pad)); return gl
def space(hue_rgb):
    rng=np.random.default_rng(3); a=np.zeros((H,W,3),np.float32); yy,xx=np.mgrid[0:H,0:W]
    for (cx,cy,r,w) in [(320,180,260,1),(140,90,160,.6),(520,260,180,.5)]: a+=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*r*r))[...,None]*np.array(hue_rgb)*w*.28
    for _ in range(420): x,y=rng.integers(0,W),rng.integers(0,H); a[y,x]+=rng.uniform(80,255)
    a=np.clip(a+np.array([4,6,14]),0,255).astype(np.uint8); return Image.fromarray(a).filter(ImageFilter.GaussianBlur(.6)).convert("RGBA")
def put(c, im, cx, cy): c.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
M=lambda k: f"mat-{k}.webp"; R=lambda k: D+f"icons/res-{k}.webp"
TIER={1:(170,170,170),2:(90,220,110),3:(80,160,255),4:(190,110,255),5:(255,160,50),6:(255,70,70)}
def fam(name):
    if name=="starter":
        c=bg("art/metalMine.webp",.5); 
        for i,k in enumerate("mcge"): put(c, Image.open(R(k)).convert("RGBA").resize((150,150),Image.LANCZOS), 140+i*120, 190+(-14 if i%2 else 10))
    elif name=="shards":
        c=space((120,50,200))
        for (x,y,s) in [(320,200,230),(190,230,150),(450,230,150),(110,265,95),(530,265,95),(255,140,80),(390,135,70)]: put(c, icon(R("c"),s,hue=.77,glow=(190,120,255)), x,y)
    elif name=="empire":
        c=bg("art/robotics.webp",.4)
        for i,k in enumerate("mcg"): put(c, Image.open(R(k)).convert("RGBA").resize((175,175),Image.LANCZOS), 165+i*155, 195)
    elif name=="fleet":
        c=bg("art/battleship.webp",.45); put(c, Image.open(R("e")).convert("RGBA").resize((150,150),Image.LANCZOS), 540, 240)
    elif name=="forge":
        c=bg("art/flagDock.webp",.35)
        for i,k in enumerate(["alloy","circuit","crystal"]): put(c, tile(M(k),130,TIER[3+i]), 170+i*150, 200)
    elif name=="hunter":
        c=bg("art/dreadnought.webp",.45)
        for i,k in enumerate(["bio","void"]): put(c, tile(M(k),115,TIER[4]), 450+i*125, 240)
    elif name=="legend":
        c=bg("art/eclipse.webp",.45)
        for i,k in enumerate(["alloy","crystal","void","cube","circuit"]): put(c, tile(M(k),105 if i!=2 else 140,TIER[5]), 110+i*105, 210 if i!=2 else 195)
    elif name=="cube":
        c=bg("art/cube-event.jpg",.4)
        for i,k in enumerate(["cube","void"]): put(c, tile(M(k),145,TIER[5 if i==0 else 4]), 230+i*180, 205)
    elif name=="ultimate":
        c=bg("art/worldbreaker.webp",.45)
        for i,k in enumerate(["alloy","circuit","crystal","bio","cube","void"]): put(c, tile(M(k),82,TIER[6]), 90+i*92, 275)
        put(c, icon(R("c"),130,hue=.77,glow=(255,200,90)), 320, 135)
    return c.convert("RGB")
FAMS=["starter","shards","empire","fleet","forge","hunter","legend","cube","ultimate"]
tiles=[]
for f in FAMS:
    im=fam(f); im.save(f"pack-{f}.webp",quality=86,method=6); tiles.append(np.asarray(im.resize((320,180))))
rows=[np.hstack(tiles[i:i+3]) for i in range(0,9,3)]; Image.fromarray(np.vstack(rows)).save("packart_prev.png")
