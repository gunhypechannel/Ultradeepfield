# Rebuild the Emerald Geode skin cut-out from the original art: the planet as before, the green ring kept whole as glowing light,
# fading where the original picture ends; only the oval band round the planet is kept (no stray stars, dust or asteroids).
from PIL import Image
import numpy as np, sys
S="/tmp/claude-0/-home-claude/59785d42-49cf-5378-902e-179290e8c617/scratchpad"
cur=np.asarray(Image.open(sys.argv[1]).convert('RGBA')).astype(float)/255
orig=Image.open(sys.argv[2]).convert('RGB')
k,ox,oy=.64,114,126; sz=int(round(1254*k))
O=np.zeros((1024,1024,3)); Os=np.asarray(orig.resize((sz,sz),Image.LANCZOS)).astype(float)/255
O[oy:oy+sz, ox:ox+sz]=Os[:1024-oy,:1024-ox]
yy,xx=np.mgrid[0:1024,0:1024]; cx,cy,R=512,512,352
d=np.minimum.reduce([xx-ox, (ox+sz-1)-xx, yy-oy, (oy+sz-1)-yy]).clip(0,None); feather=np.clip(d/55,0,1)**1.5
r,g,b=O[...,0],O[...,1],O[...,2]
greenness=np.clip((g-np.maximum(r,b)*.85)/.18,0,1)
e=((xx-cx)/(1.32*R))**2+((yy-cy)/(.97*R))**2; band=np.clip((1-e)/.12,0,1)
ringA=np.clip((g-.16)/.45,0,1)*greenness*feather*band
disc=np.clip((R+6-np.hypot(xx-cx,yy-cy))/8,0,1); planetA=cur[...,3]*disc
A=np.maximum(planetA,ringA); ringCol=np.clip(O/np.clip(ringA,.35,1)[...,None],0,1)
RGB=np.where((planetA>=ringA)[...,None],cur[...,:3],ringCol)
im=Image.fromarray((np.dstack([RGB,A])*255).round().astype(np.uint8),'RGBA'); im.save(sys.argv[3],quality=92,method=6)
bg=Image.new('RGBA',(1024,1024),(5,9,15,255)); bg.alpha_composite(im); bg.convert('RGB').resize((512,512)).save(S+'/emerald_check.jpg',quality=90)
