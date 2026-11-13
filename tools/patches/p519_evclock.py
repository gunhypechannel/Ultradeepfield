# v519 the rune clock over the Void counts down to every live event that has a preview (owner): the Wednesday great events (the four
# super bosses, Cube Devastation, the Convergence) and the Saturday world bosses, whichever starts next, and only from 7 days before
# it. The whole clock takes that event's colour (it is drawn in greys and tinted by its material) and its title. Hidden while an
# event is live, as before.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function dvCdBuild(W)'); j = s.index('function dvCountdown(W, t, T, live)')
def grey(m):
    t = m.group(0)
    if t.startswith('#'):
        r, g, b = int(t[1:3], 16), int(t[3:5], 16), int(t[5:7], 16); v = round(.3 * r + .59 * g + .11 * b); return '#%02x%02x%02x' % (v, v, v)
    nums = [x.strip() for x in t[t.index('(') + 1:-1].split(',')]; r, g, b = map(int, nums[:3]); v = round(.3 * r + .59 * g + .11 * b)
    return 'rgba(%d,%d,%d,%s)' % (v, v, v, nums[3])
seg = re.sub(r'#[0-9a-fA-F]{6}|rgba\([0-9]+,[0-9]+,[0-9]+,[0-9.]+\)', grey, s[i:j])
seg = seg.replace('function dvCdBuild(W) {', 'function dvCdBuild(W, N) {', 1)
assert seg.count('const txt = "CUBE DEVASTATION"') == 1; seg = seg.replace('const txt = "CUBE DEVASTATION"', 'const txt = String(N.n).toUpperCase()')
assert seg.count('C.grp.scale.setScalar(1.55); W.scene.add(C.grp); return (W.dvCd = C); }') == 1
seg = seg.replace('C.grp.scale.setScalar(1.55); W.scene.add(C.grp); return (W.dvCd = C); }', 'C.mesh.material.color.set(N.col).lerp(new TH.Color(0xffffff), .18); C.key = N.k; /* v519 drawn in greys, tinted to the event */\n  C.grp.scale.setScalar(1.55); W.scene.add(C.grp); return (W.dvCd = C); }')
assert seg.count('const left = Math.max(0, dvNext(T) - T)') == 1; seg = seg.replace('const left = Math.max(0, dvNext(T) - T)', 'const left = Math.max(0, (C.s0 || dvNext(T)) - T)')
s = s[:i] + seg + s[j:]
rep('function dvCountdown(W, t, T, live) { const show = !live && view === "galaxy" && !G.sbSim && !sbLiveKey(T); /* v488 */\n  if (!show) {',
    '''/* v519 which event the clock counts down to: the next great event or world boss, within 7 days */
function evCdNext(T) { let best = null; for (const k of ROT.concat(ROTS)) { const D = k === "dv" ? { n: "Cube Devastation", col: "#5dff6a" } : k === "conv" ? { n: "The Convergence", col: "#ffd36b" } : SBX[k] || SBW[k] ? { n: (SBW[k] || SBX[k]).n, col: (SBX[k] || {}).col || (SBW[k] || {}).col || "#c890ff" } : WB[k] ? { n: WB[k].n, col: WB[k].col } : null;
    if (!D) continue; const s0 = rotNextOf(k, T); if (s0 > T && s0 - T <= 7 * 864e5 && (!best || s0 < best.s0)) best = { k, s0, n: D.n, col: D.col }; } return best; }
const evCdLive = T => { try { return wbGroupOn(3, T) || ROTS.some(k => WB[k] && wbOn(k, T)); } catch (e) { return false; } };
function dvCountdown(W, t, T, live) { const N = evCdNext(T), show = !!N && !live && view === "galaxy" && !G.sbSim && !sbLiveKey(T) && !evCdLive(T); /* v488; v519 */
  if (W.dvCd && N && W.dvCd.key !== N.k) { try { W.scene.remove(W.dvCd.grp); W.dvCd.mesh.material.dispose(); W.dvCd.mesh.geometry.dispose(); W.dvCd.tex.dispose(); } catch (e) {} W.dvCd = null; }
  if (!show) {''')
rep('const C = W.dvCd || dvCdBuild(W); C.grp.visible = true;', 'const C = W.dvCd || dvCdBuild(W, N); C.s0 = N.s0; C.grp.visible = true;')
s2 = re.sub(r"GAME_V = 518\b", "GAME_V = 519", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
