import numpy as np, json, os, sys
sys.path.insert(0, "../pr")
from PIL import Image, ImageFilter
A="/mnt/user-data/attachments/59785d42-49cf-5378-902e-179290e8c617/"
OUT="/home/claude/ultradeepfield/docs/skins/"
src={1:np.asarray(Image.open(A+"f0abe587-image.png").convert("RGB")).astype(np.float32), 2:np.asarray(Image.open(A+"857caa79-image.png").convert("RGB")).astype(np.float32)}
circ=json.load(open("circ.json"))
def unwrap(D,cx,cy,R,W=1024,H=512,f=.85):
  u=(np.arange(W)+.5)/W; v=(np.arange(H)+.5)/H; U,V=np.meshgrid(u,v)
  lat=(.5-V)*np.pi; lon=(U*2*np.pi+np.pi)%(2*np.pi)-np.pi
  lon=np.where(np.abs(lon)>np.pi/2, np.sign(lon)*(np.pi-np.abs(lon)), lon)
  x=np.cos(lat)*np.sin(lon)*f; y=np.sin(lat)*f; px=cx+x*R; py=cy-y*R
  x0=np.floor(px).astype(int); y0=np.floor(py).astype(int); fx=(px-x0)[...,None]; fy=(py-y0)[...,None]
  g=lambda yy,xx: D[np.clip(yy,0,D.shape[0]-1),np.clip(xx,0,D.shape[1]-1)]
  return g(y0,x0)*(1-fx)*(1-fy)+g(y0,x0+1)*fx*(1-fy)+g(y0+1,x0)*(1-fx)*fy+g(y0+1,x0+1)*fx*fy
sheet=Image.new("RGB",(17*120,240),(5,9,15))
for n,(s,cx,cy,R) in enumerate(circ, start=1):
  D=src[s]; k=f"ps{n}"
  m=Image.fromarray(np.clip(unwrap(D,cx,cy,R),0,255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2,80,2)); m.save(OUT+k+"-map.webp",quality=86,method=6)
  sc=348/R; H0,W0=D.shape[:2]; big=Image.fromarray(D.astype(np.uint8)).resize((int(W0*sc),int(H0*sc)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.2,90,2))
  B=np.asarray(big).astype(np.float32)/255; ox=int(round(512-cx*sc)); oy=int(round(512-cy*sc))
  O=np.zeros((1024,1024,3),np.float32); x0,y0=max(0,ox),max(0,oy); x1,y1=min(1024,ox+B.shape[1]),min(1024,oy+B.shape[0]); O[y0:y1,x0:x1]=B[y0-oy:y1-oy,x0-ox:x1-ox]
  yy,xx=np.mgrid[0:1024,0:1024]; r=np.hypot(xx-512,yy-512)
  # only this planet: fade anything beyond the cell (neighbours) out
  cellR=(190 if s==1 else 205)*sc*1.02
  disc=np.clip((350-r)/3,0,1); glow=np.clip((O.max(2)-.035)/.5,0,1)**.85
  Aa=np.maximum(disc,glow)*np.clip((cellR-r)/24,0,1)*np.clip((508-r)/30,0,1)
  col=np.where((disc>=glow)[...,None],O,np.clip(O/np.clip(glow,.05,1)[...,None],0,1))
  out=Image.fromarray((np.dstack([col,Aa])*255).round().astype(np.uint8),'RGBA'); out.save(OUT+k+".webp",quality=90,method=6)
  bg=Image.new("RGBA",(1024,1024),(5,9,15,255)); bg.alpha_composite(out)
  sheet.paste(bg.convert("RGB").resize((120,120)),((n-1)*120,0)); sheet.paste(m.resize((120,60)),((n-1)*120,140))
sheet.save("sheet.jpg",quality=85); print("ok", sum(os.path.getsize(OUT+f"ps{n}.webp")+os.path.getsize(OUT+f"ps{n}-map.webp") for n in range(1,18))//1024, "KB")
