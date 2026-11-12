import cv2,numpy as np,json,sys
from PIL import Image
O='/home/claude/ultradeepfield/docs/art/boss/'
def rect(x0,y0,x1,y1): return ('r',x0,y0,x1,y1)
B={ # mode, threshold, exclusions (rects zeroed) or polygon, feather, mouth anchor
 'overlord':dict(t=.3,ex=[rect(0,790,1672,941)],m=(830,520)),
 'conduit':dict(poly=[(480,0),(720,0),(780,150),(1000,180),(1010,420),(980,560),(880,700),(1010,1050),(1000,1180),(200,1180),(180,1050),(300,700),(150,560),(120,400),(160,180),(420,150)],f=30,m=(590,300)),
 'devourer':dict(t=.3,ex=[rect(0,700,600,941)],m=(1170,390)),
 'warden':dict(t=.3,ex=[rect(0,780,380,1024),rect(1330,600,1536,1024)],m=(820,400)),
 'matriarch':dict(poly=[(60,60),(400,0),(820,40),(1000,200),(1122,330),(1122,520),(950,620),(900,800),(700,920),(560,1000),(300,1000),(100,920),(0,700),(0,250)],f=60,m=(760,260)),
 'tyrant':dict(t=.3,ex=[rect(0,1180,1122,1402),rect(300,1150,700,1402)],m=(700,415)),
 'wyrm':dict(poly=[(0,40),(560,0),(1122,40),(1122,1300),(560,1360),(0,1300)],f=120,m=(860,330)),
 'colossus':dict(poly=[(60,40),(950,40),(1050,250),(1020,600),(820,780),(300,780),(60,620),(0,300)],f=60,m=(560,380)),
 'el-ice':dict(t=.3,ex=[rect(0,585,605,660)],m=(300,300)),
 'el-fire':dict(t=.3,ex=[rect(0,555,594,660),rect(0,380,80,660)],m=(300,220)),
 'el-light':dict(t=.3,ex=[rect(0,500,400,652),rect(0,0,400,10)],m=(190,240)),
 'el-storm':dict(t=.3,ex=[rect(0,575,400,652),rect(0,400,70,652),rect(0,520,90,652),rect(330,470,400,652)],m=(200,290)),
 'el-nature':dict(t=.3,ex=[rect(0,535,399,652),rect(300,470,399,652)],m=(200,300)),
}
meta={}
for k,cfg in B.items():
  if len(sys.argv)>1 and k not in sys.argv[1:]: continue
  c=cv2.imread(k+'_c.png'); d=cv2.imread(k+'_cd.png',0)/255.; H,W=d.shape
  if 'poly' in cfg:
    a=np.zeros((H,W),np.float32); cv2.fillPoly(a,[np.array(cfg['poly'],np.int32)],1); a=cv2.GaussianBlur(a,(0,0),cfg['f']); a=np.clip((a-.15)/.7,0,1)
  else:
    a=(d>cfg['t']).astype(np.float32); a=cv2.morphologyEx(a,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); a=cv2.morphologyEx(a,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    m=np.ones_like(a)
    for _,x0,y0,x1,y1 in cfg['ex']: m[y0:y1,x0:x1]=0
    m=cv2.GaussianBlur(m,(0,0),8); a=cv2.GaussianBlur(a,(0,0),1.4)*m
  yy,xx=np.mgrid[0:H,0:W]; e=np.minimum.reduce([xx,yy,W-1-xx,H-1-yy]).astype(np.float32); a=a*np.clip(e/(220 if 'poly' in cfg else 12),0,1)  # no hard edge at the painting's border
  rgba=np.dstack([cv2.cvtColor(c,cv2.COLOR_BGR2RGB),(a*255).astype(np.uint8)])
  TW=min(1024,W); Image.fromarray(rgba).resize((TW,round(TW*H/W)),Image.LANCZOS).save(O+k+'-skin.webp','WEBP',quality=86,method=6)
  inm=(a>.02).astype(np.float32); dm=d*inm
  for _ in range(40): dm=np.where(inm>0,dm,cv2.dilate(dm,np.ones((7,7),np.uint8))); inm=np.maximum(inm,(dm>0).astype(np.float32))
  ds=cv2.GaussianBlur(dm.astype(np.float32),(0,0),9)
  Image.fromarray((ds*255).clip(0,255).astype(np.uint8)).resize((256,round(256*H/W)),Image.LANCZOS).save(O+k+'-depth.png',optimize=True)
  ys,xs=np.where(a>.3); bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]; dmean=float((d*a).sum()/a.sum())
  meta[k]=dict(iw=W,ih=H,bb=bb,dm=round(dmean,3),m=cfg['m'])
  bg=Image.new('RGBA',(W,H),(0,255,0,255)); bg.alpha_composite(Image.fromarray(rgba)); bg.convert('RGB').resize((300,round(300*H/W))).save(k+'_a.jpg')
old=json.load(open('meta.json')) if len(sys.argv)>1 else {}
old.update(meta); json.dump(old,open('meta.json','w')); print(json.dumps(old))
