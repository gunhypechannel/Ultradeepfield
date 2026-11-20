# fb-20261120 (2): six crash reports from the owner's iPhone (v673-v677), all iOS memory kills (the page reloads 1-10 s after
# dying). One died 8 s after launch on the base with nothing else open (readout ~194 MB: base 186). On iPhone (and weak Android)
# the base GPU cap is 768 px (iosTexCap), but glbShrink left each building's colour map at 1024 px: three.js scaled it to 768 at
# every upload and the 1024 px ImageBitmap stayed in memory behind the texture (~4.2 MB instead of ~2.4 MB, x19 buildings,
# not counted by the memory readout). Building colour maps are now shrunk straight to that cap: the base looks the same.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('big = shipIOS ? 512 : MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048,',
  'big = shipIOS ? 512 : (IOS || WEAK) && GLB_BLDS.has(k) ? 768 /* fb-20261120 = the base cap (iosTexCap), so no 1024 px bitmap is kept */ : MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048,'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
