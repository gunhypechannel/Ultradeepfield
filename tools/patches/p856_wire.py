"""v856: the Continuum remastered: finer hulls with crimson glow layers (the Eternal Commander re-sculpted), a red material, bigger in
battle, the opening scan, the dread, an attack for every hull and five for the Eternal Commander (see p856_cnt.js)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 855;", "const GAME_V = 856;")
js = open(__file__.rsplit('/', 1)[0] + "/p856_cnt.js", encoding="utf-8").read()
rep("Object.assign(MIM_HULL, { cnint: .85, cncor: 1, cnexe: 1.35, cnfab: 2, cnasm: 1.6, cndre: 2.6, cnrel: 2.2, cnark: 4, cnprime: 5.4, cneter: 3.6, cncom: 3.2 });",
    "Object.assign(MIM_HULL, { cnint: .85, cncor: 1, cnexe: 1.35, cnfab: 2, cnasm: 1.6, cndre: 2.6, cnrel: 2.2, cnark: 4, cnprime: 5.4, cneter: 3.6, cncom: 3.2 });\n" + js)
rep('''  fetch("art/rwar/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { CNT_GEO[k] = cntMeshGeo(b); cntSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }''',
    '''  sculptFetch("art/rwar/m/", k, CNT_SC[k].g, (a, bg) => { CNT_GEO[k + "_g"] = bg; CNT_GEO[k] = a; cntSculptSwap(k); }); } /* v856 with its glow layer */''')
rep("function cntSculpted(k) { const D = CNT_SC[k], g = new TH.Group(), m = new TH.Mesh(CNT_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s); g.add(m);",
    "function cntSculpted(k) { const D = CNT_SC[k], g = new TH.Group(), m = new TH.Mesh(CNT_GEO[k], cntRedMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s); g.add(m); sculptGhost(g, CNT_GEO[k + \"_g\"], D.s); /* v856 */")
rep("try { crcAtkAdd(b, v); crcShAdd(b, v); } catch (e) {} /* v704 */", "try { crcAtkAdd(b, v); crcShAdd(b, v); } catch (e) {} /* v704 */ try { cntAtkAdd(b, v); } catch (e) {} /* v856 */")
rep("try { crcBossAtk(ctx, b, scr, T, d); crcWalkSay(b); } catch (e) {}", "try { crcBossAtk(ctx, b, scr, T, d); crcWalkSay(b); } catch (e) {} try { cntAtkDraw(ctx, b, scr, T, W, H, d, t); cntDread(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v856 */")
open(p, "w", encoding="utf-8").write(s); print("ok")
