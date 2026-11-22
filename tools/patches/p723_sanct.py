# v723 (owner: "use meshyai community page to find a building for xeno sanctuary"; chose the alien jelly dome,
# meshy.ai/posts/01a1d523-3813-7561-955f-8411de793276, CC0, 2.3 M tris -> 60 k with tools/glb_decimate.py, textures 2048/1024 via glb_retex.py,
# phones 1024/512 via glb_pack.py). docs/models/sanct.glb + m/sanct.glb; the hand-built domes stay as the fallback.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('"allyDepot", "lunarBase", "phalanx"]);', '"allyDepot", "lunarBase", "phalanx", "sanct"]); /* v723 the Xeno Sanctuary */')
rep('const GLB_V = {"armageddon": "5935b307",', 'const GLB_V = {"sanct": "e45e883a", "armageddon": "5935b307",')
# its jelly dome is bright and saturated everywhere, so the lit-window glow (meant for small windows) is turned well down on it
rep("m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT);", "m.emissiveMap = et; m.emissive.set(0xffffff); m.userData.ek = k === \"sanct\" ? .12 : 1; /* v723 */ m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT) * m.userData.ek;")
rep("for (const m of GLB_EMI) { m.emissiveIntensity = 2.6 * (1 + 1.1 * n);", "for (const m of GLB_EMI) { m.emissiveIntensity = 2.6 * (1 + 1.1 * n) * (m.userData.ek || 1);")
rep('const GAME_V = 722;', 'const GAME_V = 723;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
