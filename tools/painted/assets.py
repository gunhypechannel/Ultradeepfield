import cv2,numpy as np
from PIL import Image
O='/home/claude/ultradeepfield/docs/art/boss/'
def make(k,col,t,excl,name,TW):
  c=cv2.imread(col); d=cv2.imread(k+'_cd.png',0)/255.; H,W=d.shape
  a=(d>t).astype(np.float32); a=cv2.morphologyEx(a,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); a=cv2.morphologyEx(a,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
  m=np.ones_like(a); 
  for f in excl: f(m,W,H)
  m=cv2.GaussianBlur(m,(0,0),10); a=cv2.GaussianBlur(a,(0,0),1.6)*m
  rgba=np.dstack([cv2.cvtColor(c,cv2.COLOR_BGR2RGB),(a*255).astype(np.uint8)])
  th=int(TW*H/W); Image.fromarray(rgba).resize((TW,th),Image.LANCZOS).save(O+name+'-skin.webp','WEBP',quality=88,method=6)
  inm=(a>.02).astype(np.float32); dm=d*inm
  for _ in range(40): dm=np.where(inm>0,dm,cv2.dilate(dm,np.ones((7,7),np.uint8))); inm=np.maximum(inm,(dm>0).astype(np.float32))
  ds=cv2.GaussianBlur(dm.astype(np.float32),(0,0),9)  # outside the cut, the nearest surface depth (no stretched edges)
  Image.fromarray((ds*255).astype(np.uint8)).resize((256,int(256*H/W)),Image.LANCZOS).save(O+name+'-depth.png',optimize=True)
  return d
def kx(m,W,H):
  m[810:, :300]=0; m[1110:, :]=0; m[1060:, :260]=0
  yy=np.arange(H)[:,None]; m*= np.clip((1170-yy)/170,0,1); xx=np.arange(W)[None,:]; m*=np.clip(xx/140,0,1)*np.clip((W-xx)/60,0,1)
def mx(m,W,H):
  yy=np.arange(H)[:,None]; m*=np.clip((1045-yy)/40,0,1)
d=make('khz','khz_c.png',.3,[kx],'khezaroth',1024); print('khz hole',d[954,685], 'eyes',d[209,614],d[209,717], 'front',np.percentile(d,99))
d=make('med','med_ci.png',.3,[mx],'medusara',1024); print('med eyes',d[360,482],d[292,718],'gem',d[192,570],'ctr',d[543,697])
