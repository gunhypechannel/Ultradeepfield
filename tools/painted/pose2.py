exec(open('pose.py').read().split('def R(x')[0])
import json
def RXYZ(x,y,z):
  cx,sx,cy,sy,cz,sz=np.cos(x),np.sin(x),np.cos(y),np.sin(y),np.cos(z),np.sin(z)
  return np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])@np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])@np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
A2=np.vstack([A,fp(0,.5)]); Q2=np.vstack([Q,[[563,-193]]])
def fit(e):
  P=(RXYZ(*e)@A2.T).T; # affine in the rotated frame's x,y: q = M @ [px,py] + t  (rotation in-plane + separate scales)
  X=np.c_[P[:,0],P[:,1],np.ones(len(P))]; sol,_,_,_=np.linalg.lstsq(X,Q2,rcond=None); r=((X@sol-Q2)**2).sum(); return r,sol
best=None
for x in np.linspace(-.6,.2,33):
  for y in np.linspace(-.8,.8,33):
    r,sol=fit((x,y,0))
    if best is None or r<best[0]: best=(r,(x,y,0),sol)
r,e,sol=best; print('rms',np.sqrt(r/len(Q2)),'e',np.round(e,3)); print(np.round(sol,3))
P=(RXYZ(*e)@A2.T).T; X=np.c_[P[:,0],P[:,1],np.ones(len(P))]; Z=X@sol; print(np.round(np.c_[Z[:,0],-Z[:,1]]), 'z', np.round(P[:,2],1))
json.dump({'e':list(map(float,e)),'M':sol.tolist()},open('pose2.json','w'))
