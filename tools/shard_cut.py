import numpy as np, cv2
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
src=cv2.imread("/mnt/user-data/attachments/59785d42-49cf-5378-902e-179290e8c617/fe421f6d-image.png"); H,W=src.shape[:2]; k=1254/900
poly=[(int(x*k),int(y*k)) for x,y in [(628,14),(709,308),(357,813),(238,520),(171,300),(268,213),(478,78)]]
m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon(poly,fill=255); crys=np.asarray(m)>0
crys_soft=cv2.GaussianBlur(crys.astype(np.float32),(0,0),2.2)
f=src.astype(np.float32); V=f.max(2); B,G,R=f[...,0],f[...,1],f[...,2]
# HDR-style grade: local contrast on lightness, saturation and a crisp unsharp
lab=cv2.cvtColor(src,cv2.COLOR_BGR2LAB); cl=cv2.createCLAHE(clipLimit=2.4,tileGridSize=(8,8)); lab[...,0]=cl.apply(lab[...,0]); hdr=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
hsv=cv2.cvtColor(hdr,cv2.COLOR_BGR2HSV).astype(np.float32); hsv[...,1]=np.clip(hsv[...,1]*1.18,0,255); hdr=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
bl=cv2.GaussianBlur(hdr,(0,0),2.0); hdr=cv2.addWeighted(hdr,1.7,bl,-.7,0)
# orbit ring: bright, purple-white strokes outside the crystal that link to it
ring=(V>150)&((R+B)/2>G+25)&~crys
lab2,n=ndi.label(ndi.binary_dilation(ring,iterations=1)); touch=ndi.binary_dilation(crys,iterations=6)
ids=[i for i in range(1,n+1) if (touch&(lab2==i)).any() and (lab2==i).sum()>400]
ringm=np.isin(lab2,ids)&ring; ra=np.clip((V-120)/90,0,1)*cv2.GaussianBlur(ndi.binary_dilation(ringm,iterations=3).astype(np.float32),(0,0),1.5)
def cut(alpha, name, pad=1.12):
    ys,xs=np.where(alpha>0.03); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max(); side=int(max(y1-y0,x1-x0)*pad); cy,cx=(y0+y1)//2,(x0+x1)//2
    rgba=np.dstack([hdr[...,2],hdr[...,1],hdr[...,0],np.clip(alpha,0,1)*255]).astype(np.uint8)
    big=np.zeros((H+2*side,W+2*side,4),np.uint8); big[side:side+H,side:side+W]=rgba; sq=big[side+cy-side//2:side+cy-side//2+side, side+cx-side//2:side+cx-side//2+side]
    im=Image.fromarray(sq,"RGBA"); return im
def glow(im, col, rad):
    a=np.asarray(im.split()[3]).astype(np.float32); g=np.clip(cv2.GaussianBlur(a,(0,0),rad)*.95,0,255)
    gl=Image.fromarray(np.dstack([np.full_like(g,col[0]),np.full_like(g,col[1]),np.full_like(g,col[2]),g]).astype(np.uint8),"RGBA"); gl.alpha_composite(im); return gl
full=cut(np.maximum(crys_soft,ra),"full"); crystal=cut(crys_soft,"crys",1.08)
icon=glow(full.resize((512,512),Image.LANCZOS),(190,110,255),14); icon.save("shard-icon.webp",quality=92,method=6)
cr=glow(crystal.resize((512,512),Image.LANCZOS),(190,110,255),16); cr.save("shard-crystal.webp",quality=92,method=6)
for nm,im in [("icon",icon),("crys",cr)]:
    bgv=Image.new("RGBA",im.size,(8,10,22,255)); bgv.alpha_composite(im); bgv.convert("RGB").save(f"prev_{nm}.png")
small=np.hstack([np.asarray(Image.open("prev_icon.png").resize((s,s),Image.LANCZOS).resize((160,160),Image.NEAREST)) for s in (24,40,160)]); Image.fromarray(small).save("prev_small.png")
print("ring comps", len(ids))
