# Build the claude.ai artifact copy from the website build: python3 tools/to_artifact.py docs/index.html artifact.html
# Drops the website-only head tags (theme-color to the end of line 1, the config/script lines) and the service-worker line.
import sys
src,dst=sys.argv[1],sys.argv[2]
L=open(src,encoding='utf-8').read().split('\n')
i=L[0].index('<meta name="theme-color"')
# rebuild line 0: everything before theme-color, then the part after the website-only head tags
rest=L[0][i:]; k=rest.find('</head>'); L0=L[0][:i]+(rest[k:] if k>=0 else '')
assert L[1].startswith('<title>'), L[1][:40]
cm=[x for x in L[2:8] if x.startswith('<!-- udf-firebase.js -->')]; assert cm
L1=L[1]+cm[0].replace('<!-- udf-firebase.js -->','')
n=next(idx for idx in range(2,10) if L[idx].startswith('<!-- udf-firebase.js -->'))
body=L[n+1:]
assert body[-1].startswith('<script>if("serviceWorker"'), body[-1][:40]
body=body[:-1]+['','','</body></html>']
open(dst,'w',encoding='utf-8').write('\n'.join([L0,L1]+body))
