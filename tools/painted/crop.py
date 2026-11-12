import onnxruntime as ort, numpy as np
from PIL import Image, ImageFilter
R='/home/claude/ultradeepfield/assets/bosses/'
C={'khz':(R+'khezaroth/ref/sphinx-blackhole-2026-11-12.png',(0,0,1024,1180)),
   'med':(R+'medusa/ref/medusa-face-2026-11-12.png',(0,0,1199,1060))}
da=ort.InferenceSession('da.onnx')
def depth(im):
  x=np.asarray(im.resize((518,518),Image.BICUBIC),np.float32)/255
  x=(x-[.485,.456,.406])/[.229,.224,.225]
  d=da.run(None,{'l_x_':x.transpose(2,0,1)[None].astype(np.float32)})[0].squeeze()
  return d
for k,(p,b) in C.items():
  im=Image.open(p).convert('RGB').crop(b); W,H=im.size
  d=depth(im); d=(d-np.percentile(d,2))/(np.percentile(d,99.5)-np.percentile(d,2)); d=d.clip(0,1)
  D=Image.fromarray((d*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
  D.save(k+'_cd.png'); im.save(k+'_c.png')
  a=np.asarray(D,np.float32)/255
  print(k,W,H,np.percentile(a,[10,30,50,70,90]))
