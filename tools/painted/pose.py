import numpy as np, itertools
HS=[11.5,12.5,11]; FX,FY,FA=1.45,1.3,1.55
def g(u,v,cu,cv,su,sv): return np.exp(-((u-cu)/su)**2-((v-cv)/sv)**2)
def faceH(u,v):
  h=0
  for s in (-1,1):
    h+= .055*g(u,v,s*.31,.31,.25,.075)-.085*g(u,v,s*.32,.14,.19,.115)+.05*g(u,v,s*.32,.125,.125,.06)-.016*g(u,v,s*.32,.195,.16,.02)+.006*g(u,v,s*.32,.09,.12,.012) \
      +.05*g(u,v,s*.45,-.05,.16,.12)-.03*g(u,v,s*.37,-.36,.13,.12)-.022*g(u,v,s*.7,.33,.14,.2)+.045*g(u,v,s*.105,-.245,.06,.05)-.04*g(u,v,s*.062,-.285,.026,.02)-.022*g(u,v,s*.23,-.495,.04,.04)-.012*g(u,v,s*.2,-.15,.03,.2)
  h+= .035*g(u,v,0,.27,.1,.1)+.055*g(u,v,0,.03,.075,.25)+.1*g(u,v,0,-.205,.095,.085)+.022*g(u,v,0,-.37,.065,.05)-.006*g(u,v,0,-.37,.015,.05)+.055*g(u,v,0,-.44,.19,.042)-.04*g(u,v,0,-.488,.23,.011) \
     +.06*g(u,v,0,-.545,.16,.048)-.025*g(u,v,0,-.64,.15,.03)+.08*g(u,v,0,-.79,.17,.12)+.02*g(u,v,0,.62,.5,.3)
  return h
def fp(u,v):
  lo,la=u*FX,v*FY; h=faceH(u,v)*FA
  return np.array([np.sin(lo)*np.cos(la)*(1+h)*HS[0],np.sin(la)*(1+h)*HS[1],np.cos(lo)*np.cos(la)*(1+h)*HS[2]])
A=np.array([fp(-.32,.125),fp(.32,.125),fp(0,-.205),fp(0,-.488),fp(0,-.75)])
Q=np.array([[470,363],[713,290],[566,372],[580,447],[600,548]],float); Q[:,1]*=-1
def R(x,y,z):
  cx,sx,cy,sy,cz,sz=np.cos(x),np.sin(x),np.cos(y),np.sin(y),np.cos(z),np.sin(z)
  Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]);Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
  return Rz@Ry@Rx   # three.js Euler XYZ order: R = Rx*Ry*Rz? see below
def RXYZ(x,y,z):  # three.js 'XYZ': matrix = Rx * Ry * Rz
  cx,sx,cy,sy,cz,sz=np.cos(x),np.sin(x),np.cos(y),np.sin(y),np.cos(z),np.sin(z)
  Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]);Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
  return Rx@Ry@Rz
def fit(e):
  P=(RXYZ(*e)@A.T).T[:,:2]; Pm=P-P.mean(0); Qm=Q-Q.mean(0); s=(Pm*Qm).sum()/(Pm*Pm).sum(); t=Q.mean(0)-s*P.mean(0); r=((s*P+t-Q)**2).sum(); return r,s,t
best=None
for x in np.linspace(-1.2,1.2,49):
  for y in np.linspace(-1,1,41):
    for z in np.linspace(-.8,.8,33):
      r,s,t=fit((x,y,z))
      if s>0 and (best is None or r<best[0]): best=(r,(x,y,z),s,t)
r,e,s,t=best
# refine
for it in range(4):
  st=.05/(it+1)
  for x in np.linspace(e[0]-st*4,e[0]+st*4,9):
    for y in np.linspace(e[1]-st*4,e[1]+st*4,9):
      for z in np.linspace(e[2]-st*4,e[2]+st*4,9):
        r2,s2,t2=fit((x,y,z))
        if s2>0 and r2<r: r,e,s,t=r2,(x,y,z),s2,t2
print('rms px',np.sqrt(r/len(Q)),'euler',np.round(e,3),'s',round(s,3),'t',np.round(t,1))
P=(RXYZ(*e)@A.T).T[:,:2]*s+t; print(np.round(np.c_[P[:,0],-P[:,1]],0))
import json; json.dump({'e':list(map(float,e)),'s':float(s),'t':list(map(float,t))},open('pose.json','w'))
