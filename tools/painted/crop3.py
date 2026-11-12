import onnxruntime as ort, numpy as np, cv2, sys, json
from PIL import Image
R='/home/claude/ultradeepfield/assets/bosses/'
E=R+'elementals/reference/ref-2026-11-10.png'
C={'overlord':(R+'pyramid-overlord/reference/ref-2026-11-09.png',None),'conduit':(R+'energy-conduit/reference/ref-2026-11-09.png',None),
 'devourer':(R+'orbital-devourer/reference/ref-2026-11-09.png',None),'warden':(R+'void-warden/reference/ref-2026-11-09.png',None),
 'matriarch':(R+'brood-matriarch/reference/ref-2026-11-10.png',None),'tyrant':(R+'iron-tyrant/reference/ref-2026-11-10.png',None),
 'wyrm':(R+'event-horizon-wyrm/reference/ref-2026-11-10.png',None),'colossus':(R+'shard-colossus/reference/ref-2026-11-10.png',None),
 'el-ice':(E,(0,0,605,660)),'el-fire':(E,(605,0,1199,660)),'el-light':(E,(0,660,400,1312)),'el-storm':(E,(400,660,800,1312)),'el-nature':(E,(800,660,1199,1312))}
json.dump({k:[p,b] for k,(p,b) in C.items()},open('crops.json','w'))
da=ort.InferenceSession('da.onnx')
for k,(p,b) in C.items():
  if len(sys.argv)>1 and k not in sys.argv[1:]: continue
  im=Image.open(p).convert('RGB'); im=im.crop(b) if b else im; W,H=im.size
  x=np.asarray(im.resize((518,518),Image.BICUBIC),np.float32)/255; x=(x-[.485,.456,.406])/[.229,.224,.225]
  d=da.run(None,{'l_x_':x.transpose(2,0,1)[None].astype(np.float32)})[0].squeeze()
  d=(d-np.percentile(d,2))/(np.percentile(d,99.5)-np.percentile(d,2)); d=d.clip(0,1)
  Image.fromarray((d*255).astype(np.uint8)).resize((W,H),Image.BICUBIC).save(k+'_cd.png'); im.save(k+'_c.png')
  c=cv2.imread(k+'_c.png'); dd=cv2.imread(k+'_cd.png',0)/255.; rows=[]
  for t in [.3,.45]:
    a=(dd>t)[...,None]; v=(c*a+np.array([60,20,20])*(1-a)).astype(np.uint8)
    for xx in range(0,W,100): cv2.line(v,(xx,0),(xx,H),(0,255,0),1);cv2.putText(v,str(xx),(xx+2,22),0,.7,(0,255,0),2)
    for yy in range(0,H,100): cv2.line(v,(0,yy),(W,yy),(0,255,0),1);cv2.putText(v,str(yy),(2,yy-3),0,.7,(0,255,0),2)
    rows.append(cv2.resize(v,(560,int(560*H/W))))
  cv2.imwrite(k+'_mg.jpg',np.hstack(rows)); print(k,W,H)
