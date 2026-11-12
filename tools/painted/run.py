import onnxruntime as ort, numpy as np, sys
from PIL import Image
R='/home/claude/ultradeepfield/assets/bosses/'
src={'khz':R+'khezaroth/ref/sphinx-blackhole-2026-11-12.png','khz2':R+'khezaroth/ref/sphinx-rings-2026-11-12.png','med':R+'medusa/ref/medusa-face-2026-11-12.png','med2':R+'medusa/ref/medusa-ring-2026-11-12.png'}
da=ort.InferenceSession('da.onnx'); seg=ort.InferenceSession('isnet.onnx')
print([ (i.name,i.shape) for i in da.get_inputs()],[(i.name,i.shape) for i in seg.get_inputs()])
for k,p in src.items():
  im=Image.open(p).convert('RGB'); W,H=im.size
  # depth at 518 multiple keeping aspect
  h=518; w=518
  x=np.asarray(im.resize((w,h),Image.BICUBIC),np.float32)/255
  x=(x-[.485,.456,.406])/[.229,.224,.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
  d=da.run(None,{da.get_inputs()[0].name:x})[0].squeeze()
  d=(d-d.min())/(d.max()-d.min())
  Image.fromarray((d*255).astype(np.uint8)).resize((W,H),Image.BICUBIC).save(k+'_d.png')
  x=np.asarray(im.resize((1024,1024),Image.BILINEAR),np.float32)/255-.5
  m=seg.run(None,{seg.get_inputs()[0].name:x.transpose(2,0,1)[None].astype(np.float32)})[0].squeeze()
  m=(m-m.min())/(m.max()-m.min())
  Image.fromarray((m*255).astype(np.uint8)).resize((W,H),Image.BILINEAR).save(k+'_m.png')
  print(k,d.shape)
