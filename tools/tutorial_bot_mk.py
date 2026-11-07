import re,sys
src=sys.argv[1] if len(sys.argv)>1 else '/home/claude/ultradeepfield/docs/index.html'
t=open(src,encoding='utf-8').read()
t=re.sub(r'<script[^>]*src="(udf-supabase|udf-firebase|supabase-config|firebase-config)[^"]*"[^>]*></script>','',t)
m=list(re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>',t,re.S)); s=max(m,key=lambda x:len(x.group(1))); body=s.group(1); body=body.replace('if (battle) { try { drawBattle(t);','if (battle) { try { const _t0 = performance.now(); drawBattle(t); (window.__dt = window.__dt || []).push(performance.now() - _t0);',1)
body=body.replace('function shipArt(k, accent, view) {','function shipArt(k, accent, view) { (window.__sa = window.__sa || {n:0,keys:{}}).n++; window.__sa.keys[k+view]=(window.__sa.keys[k+view]||0)+1;',1)
i=body.rstrip().rfind('})();')
hook='window.__dbg={get S(){return S},get G(){return G},ACT,get G3(){return G3},PB,P3,now,playBattle,duelBattle,cubeDemoStart,cubeDemoBig,get battle(){return battle},closeBattle,AU,SFX,FB,closeAll:()=>{try{closeSheet()}catch(e){}},ev:s=>eval(s)};\n'
open('index.html','w',encoding='utf-8').write(t[:s.start(1)]+body[:i]+hook+body[i:]+t[s.end(1):])
