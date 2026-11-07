import re,sys,os,json
D='/home/claude/ultradeepfield/docs'; O=os.path.dirname(os.path.abspath(__file__))
t=open(D+'/index.html',encoding='utf-8').read()
t=t.replace('<script src="supabase-config.js"></script>','<script src="seed.js"></script><script src="fakesb.js"></script><script src="supabase-config.js"></script>',1)
m=list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>',t,re.S)); s=max(m,key=lambda x:len(x.group(1))); body=s.group(1)
i=body.rstrip().rfind('})();')
hook='window.__dbg={get S(){return S},get G(){return G},get battle(){return battle},closeBattle,closeAll:()=>{try{closeSheet()}catch(e){}},ev:s=>eval(s)};\n'
out=t[:s.start(1)]+body[:i]+hook+body[i:]+t[s.end(1):]
open(O+'/index.html','w',encoding='utf-8').write(out)
open(O+'/index2.html','w',encoding='utf-8').write(out.replace('<script src="seed.js"></script><script src="fakesb.js"></script>','<script src="fakesb2.js"></script>',1))
open(O+'/seed.js','w').write('window.__seedRows='+open(O+'/seed.json').read()+';')
for f in os.listdir(D):
  if f in('index.html',): continue
  p=O+'/'+f
  if not os.path.lexists(p): os.symlink(D+'/'+f,p)
print('ok')
