import numpy as np, cv2, sys
from scipy import ndimage as ndi
from PIL import Image, ImageFilter, ImageEnhance
im=cv2.imread("/mnt/user-data/attachments/59785d42-49cf-5378-902e-179290e8c617/964cff76-image.png")
H,W=im.shape[:2]; h2,w2=H//2,W//2
Q={"m":(0,0),"c":(w2,0),"g":(0,h2),"e":(w2,h2)}
GLOW={"m":(90,170,255),"c":(80,170,255),"g":(60,240,190),"e":(255,190,40)}
tiles=[]
for k,(x0,y0) in Q.items():
    c=im[y0+40:y0+h2-40, x0+40:x0+w2-40].astype(float); B,G,R=c[:,:,0],c[:,:,1],c[:,:,2]
    border=np.concatenate([c[:10].reshape(-1,3),c[-10:].reshape(-1,3),c[:,:10].reshape(-1,3),c[:,-10:].reshape(-1,3)])
    bg=np.percentile(border,15,axis=0)
    d=np.sqrt(((c-bg)**2).sum(2))
    a=np.clip((d-14)/45,0,1)
    hard=ndi.binary_closing(a>0.4,iterations=3); filled=ndi.binary_fill_holes(hard)
    lab,n=ndi.label(filled); s=ndi.sum(filled,lab,range(1,n+1))
    hh,ww=filled.shape; yy,xx=np.mgrid[0:hh,0:ww]; cen=np.hypot(yy-hh/2,xx-ww/2)
    score=[s[i]/(1+ndi.mean(cen,lab,i+1)/100) for i in range(n)]; main=1+int(np.argmax(score))
    near=ndi.binary_dilation(lab==main,iterations=20); print(k, "main", s[main-1], "n", n)
    keep=np.isin(lab,[i+1 for i in range(n) if s[i]>40 and near[lab==i+1].any()])
    alpha=np.maximum(a*ndi.binary_dilation(keep,iterations=10), ndi.binary_erosion(filled&keep,iterations=2)*1.0)
    V=c.max(2); core=ndi.binary_erosion(ndi.binary_fill_holes(ndi.binary_closing(a>0.85,iterations=2)),iterations=4)
    alpha=np.where(core, alpha, alpha*np.clip((V-38)/55,0,1))  # dark haze and dim reflections fade out, the object itself stays solid
    alpha=cv2.GaussianBlur(alpha.astype(np.float32),(3,3),0); print(k, "keep", keep.mean().round(3), "alpha", alpha.mean().round(3))
    ys,xs=np.where(alpha>0.04); y0b,y1b,x0b,x1b=ys.min(),ys.max(),xs.min(),xs.max(); side=int(max(y1b-y0b,x1b-x0b)*1.16); cy,cx=(y0b+y1b)//2,(x0b+x1b)//2
    rgba=np.dstack([R,G,B,alpha*255]).clip(0,255).astype(np.uint8)
    pad=side; big=np.zeros((rgba.shape[0]+2*pad,rgba.shape[1]+2*pad,4),np.uint8); big[pad:pad+rgba.shape[0],pad:pad+rgba.shape[1]]=rgba
    sq=big[pad+cy-side//2:pad+cy-side//2+side, pad+cx-side//2:pad+cx-side//2+side]
    p=Image.fromarray(sq,"RGBA").resize((256,256),Image.LANCZOS)
    rgb=p.convert("RGB"); rgb=ImageEnhance.Contrast(rgb).enhance(1.12); rgb=ImageEnhance.Color(rgb).enhance(1.1); rgb=rgb.filter(ImageFilter.UnsharpMask(radius=1.6,percent=90,threshold=2))
    ic=Image.merge("RGBA",(*rgb.split(),p.split()[3]))
    al=np.asarray(p.split()[3]).astype(np.float32)/255
    glow=np.clip(cv2.GaussianBlur(al,(0,0),9)*0.9,0,1); col=np.array(GLOW[k],np.float32)
    gl=np.dstack([np.full_like(glow,col[0]),np.full_like(glow,col[1]),np.full_like(glow,col[2]),glow*255]).astype(np.uint8)
    out=Image.fromarray(gl,"RGBA"); out.alpha_composite(ic)
    oa=np.asarray(out.split()[3]); print(k, "edge alpha max", oa[0].max(), oa[-1].max(), oa[:,0].max(), oa[:,-1].max(), "art edge", np.asarray(p.split()[3])[[0,-1]].max(), np.asarray(p.split()[3])[:,[0,-1]].max())
    out.save(f"res-{k}.webp",quality=92,method=6)
    bgv=Image.new("RGBA",(256,256),(10,20,32,255)); bgv.alpha_composite(out); tiles.append(np.asarray(bgv.convert("RGB")))
    print(k, side, bg.round())
row=np.hstack(tiles)
sm=np.hstack([np.asarray(Image.fromarray(t).resize((40,40),Image.LANCZOS).resize((160,160),Image.NEAREST)) for t in tiles]); sm=np.pad(sm,((0,0),(0,row.shape[1]-sm.shape[1]),(0,0)))
Image.fromarray(np.vstack([row,sm])).save("icons_prev.png")
