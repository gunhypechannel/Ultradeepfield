import numpy as np, json, struct, io
from PIL import Image
O='/home/claude/ultradeepfield/docs/art/boss/'
def build(k,iw,ih,u,ox,oy,D,d0,nx,out):
  dep=np.asarray(Image.open(O+k+'-depth.png'),np.float32)/255; skin=Image.open(O+k+'-skin.webp').convert('RGBA')
  W,H=iw*u,ih*u; x0,y0=-ox*u,oy*u; ny=round(nx*ih/iw)
  gx,gy=np.meshgrid(np.linspace(0,1,nx+1),np.linspace(0,1,ny+1))
  dh,dw=dep.shape; d=dep[(gy*(dh-1)).round().astype(int),(gx*(dw-1)).round().astype(int)]
  z=np.maximum(-d0*D*.35,(d-d0)*D)
  P=np.stack([x0+gx*W,y0-gy*H,z],-1).reshape(-1,3).astype(np.float32); UV=np.stack([gx,gy],-1).reshape(-1,2).astype(np.float32)
  # drop quads that are fully transparent
  al=np.asarray(skin.resize((nx+1,ny+1)))[...,3]
  I=[]
  for j in range(ny):
    for i in range(nx):
      if al[j:j+2,i:i+2].max()<13: continue
      a=j*(nx+1)+i; b=a+1; c=a+nx+1; e=c+1; I+= [a,c,b,b,c,e]
  I=np.array(I,np.uint32)
  used=np.unique(I); remap=-np.ones(len(P),np.int64); remap[used]=np.arange(len(used)); P=P[used]; UV=UV[used]; I=remap[I].astype(np.uint32)
  png=io.BytesIO(); skin.save(png,'PNG',optimize=True); png=png.getvalue()
  bufs=[P.tobytes(),UV.tobytes(),I.tobytes(),png]; offs=[];bb=b''
  for b in bufs:
    offs.append(len(bb)); bb+=b; bb+=b'\0'*((-len(bb))%4)
  g={"asset":{"version":"2.0","generator":"Ultra Deep Field painted relief"},"scene":0,"scenes":[{"nodes":[0]}],
   "nodes":[{"mesh":0,"name":k}],"meshes":[{"name":k,"primitives":[{"attributes":{"POSITION":0,"TEXCOORD_0":1},"indices":2,"material":0}]}],
   "materials":[{"name":k+"-skin","pbrMetallicRoughness":{"baseColorTexture":{"index":0},"metallicFactor":0,"roughnessFactor":1},"alphaMode":"MASK","alphaCutoff":.05,"doubleSided":True,"extensions":{"KHR_materials_unlit":{}}}],
   "extensionsUsed":["KHR_materials_unlit"],"textures":[{"source":0}],"images":[{"bufferView":3,"mimeType":"image/png"}],
   "accessors":[{"bufferView":0,"componentType":5126,"count":len(P),"type":"VEC3","min":P.min(0).tolist(),"max":P.max(0).tolist()},
     {"bufferView":1,"componentType":5126,"count":len(UV),"type":"VEC2"},{"bufferView":2,"componentType":5125,"count":len(I),"type":"SCALAR"}],
   "bufferViews":[{"buffer":0,"byteOffset":offs[0],"byteLength":len(bufs[0]),"target":34962},{"buffer":0,"byteOffset":offs[1],"byteLength":len(bufs[1]),"target":34962},
     {"buffer":0,"byteOffset":offs[2],"byteLength":len(bufs[2]),"target":34963},{"buffer":0,"byteOffset":offs[3],"byteLength":len(bufs[3])}],"buffers":[{"byteLength":len(bb)}]}
  js=json.dumps(g).encode(); js+=b' '*((-len(js))%4)
  data=b'glTF'+struct.pack('<II',2,12+8+len(js)+8+len(bb))+struct.pack('<I',len(js))+b'JSON'+js+struct.pack('<I',len(bb))+b'BIN\0'+bb
  open(out,'wb').write(data); print(out,len(P),'verts',len(I)//3,'tris',len(data)//1024,'KB')
build('khezaroth',1024,1180,.0288,685,954,18,.3,220,'Khezaroth.glb')
build('medusara',1199,1060,.0266,697,543,16,.55,220,'Medusara.glb')
