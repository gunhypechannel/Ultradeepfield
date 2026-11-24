# Build the claude.ai artifact copy from the website build: python3 tools/to_artifact.py docs/index.html artifact.html
# Drops the website-only head tags (theme-color to the end of line 1, the config/script lines) and the service-worker line.
import sys
src,dst=sys.argv[1],sys.argv[2]
L=open(src,encoding='utf-8').read().split('\n')
i=L[0].index('<meta name="theme-color"')
# rebuild line 0: everything before theme-color, then the part after the website-only head tags
rest=L[0][i:]; k=rest.find('</head>'); L0=L[0][:i]+(rest[k:] if k>=0 else '')
assert L[1].startswith('<title>'), L[1][:40]
cm=[x for x in L[2:60] if x.startswith('<!-- udf-firebase.js -->')]; assert cm
L1=L[1]+cm[0].replace('<!-- udf-firebase.js -->','')
n=next(idx for idx in range(2,60) if L[idx].startswith('<!-- udf-firebase.js -->'))
body=L[n+1:]
assert body[-1].startswith('<script>if("serviceWorker"'), body[-1][:40]
body=body[:-1]+['','','</body></html>']
open(dst,'w',encoding='utf-8').write('\n'.join([L0,L1]+body))

# v636: pictures the artifact can't hold as files (its 511-file cap). tools/artifact_pack.txt lists them (paths under docs/).
# Ones the stylesheet names are inlined as data URIs; the rest go into a few lazily loaded packs (pk/<name>.json: {path: [type,
# base64]}) next to the output file, and a small loader at the top of the page swaps their addresses for blob URLs as the game
# asks for them (img src, the DOM's src/style attributes, fetch, audio src). Publish the packs with the page: files {"pk/x.json": ...}.
import os, re, json, base64
here = os.path.dirname(os.path.abspath(__file__)); docs = os.path.dirname(os.path.abspath(src))
lst = os.path.join(here, 'artifact_pack.txt')
if os.path.exists(lst):
    paths = [p.strip() for p in open(lst) if p.strip() and os.path.exists(os.path.join(docs, p.strip()))]
    page = open(dst, encoding='utf-8').read()
    css = ''.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>', page))
    MT = {'webp': 'image/webp', 'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'gif': 'image/gif', 'svg': 'image/svg+xml'}
    mt = lambda p: MT.get(p.rsplit('.', 1)[-1].lower(), 'application/octet-stream')
    b64 = lambda p: base64.b64encode(open(os.path.join(docs, p), 'rb').read()).decode()
    inl = [p for p in paths if p in css]
    for p in inl: page = re.sub(r'url\((["\']?)' + re.escape(p) + r'(\?[^"\')]*)?\1\)', lambda m: f'url("data:{mt(p)};base64,{b64(p)}")', page)
    def grp(p):
        if p.startswith('art/season/'): return 'season'
        if p.startswith(('art/arch/', 'art/lore/', 'art/chron/', 'art/ev/')): return 'arch'
        if p.startswith('art/carcinid/'): return 'crc' # v703
        if p.startswith('art/rwar/'): return 'cnt' # v742 sculpted hulls
        return 'misc'
    packs = {}
    for p in paths:
        if p not in inl: packs.setdefault(grp(p), {})[p] = [mt(p), b64(p)]
    od = os.path.join(os.path.dirname(os.path.abspath(dst)), 'pk'); os.makedirs(od, exist_ok=True)
    for n, o in packs.items(): json.dump(o, open(os.path.join(od, n + '.json'), 'w'), separators=(',', ':'))
    PK = {p: 'pk/' + n + '.json' for n, o in packs.items() for p in o}
    shim = '''<script>/* v636 packed pictures */(function(){const PK=%s,C={},B={};
function nm(u){try{u=String(u);if(/^(data:|blob:)/.test(u))return null;if(/^https?:/.test(u)){const a=new URL(u,location.href);if(a.origin!==location.origin)return null;u=a.pathname.replace(/^\\/+/,"")}return u.split("?")[0].replace(/^\\.\\//,"")}catch(e){return null}}
function ld(p){return C[p]||(C[p]=fetch(p).then(r=>r.json()).then(o=>{for(const k in o){const s=atob(o[k][1]),a=new Uint8Array(s.length);for(let i=0;i<s.length;i++)a[i]=s.charCodeAt(i);B[k]=URL.createObjectURL(new Blob([a],{type:o[k][0]}))}}).catch(()=>{delete C[p]}))}
const get=window.__udfPk=function(u,cb){const k=nm(u);if(!k||!PK[k])return false;if(B[k]){cb(B[k]);return true}ld(PK[k]).then(()=>{if(B[k])cb(B[k])});return true};
for(const P of [HTMLImageElement.prototype,HTMLMediaElement.prototype]){const d=Object.getOwnPropertyDescriptor(P,"src");if(d&&d.set)Object.defineProperty(P,"src",{get(){return d.get.call(this)},set(v){const el=this;if(!get(v,b=>d.set.call(el,b)))d.set.call(el,v)},configurable:true,enumerable:d.enumerable})}
const fix=el=>{if(!el.getAttribute)return;if(el.tagName==="IMG"){const s=el.getAttribute("src");if(s)get(s,b=>{if(el.getAttribute("src")===s)el.setAttribute("src",b)})}const st=el.getAttribute("style");if(st&&st.indexOf("url(")>=0)st.replace(/url\\((['"]?)([^'")]+)\\1\\)/g,(m,q,u)=>{get(u,b=>{const cur=el.getAttribute("style")||"";if(cur.indexOf(u)>=0)el.setAttribute("style",cur.split(u).join(b))});return m})};
new MutationObserver(ms=>{for(const m of ms){if(m.type==="attributes")fix(m.target);else for(const n of m.addedNodes)if(n.nodeType===1){fix(n);if(n.querySelectorAll)n.querySelectorAll("img[src],[style*='url(']").forEach(fix)}}}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:["src","style"]});
const of=window.fetch;window.fetch=function(u,o){const s=typeof u==="string"?u:u&&u.url,k=nm(s);if(k&&PK[k])return new Promise(r=>get(k,b=>r(of(b,o))));return of.apply(this,arguments)};})();</script>''' % json.dumps(PK, separators=(',', ':'))
    i = page.index('\n', page.index('<title>')); page = page[:i + 1] + shim + '\n' + page[i + 1:]
    open(dst, 'w', encoding='utf-8').write(page)
    print('packed', {n: len(o) for n, o in packs.items()}, 'inlined', len(inl), 'page', os.path.getsize(dst) // 1024, 'KB')
