# v505 the Wyrm's lens beam on the map fires down at the worlds and ships around the black hole (owner). Each time it opens its
# lens it picks one of the twelve nearest planets or pirate fleets, the beam runs from its head to that target and stops there,
# and the hit flares where it lands. Battle reports are unchanged.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('M.b.tick(t); }\n  try { wbScanFx(W, t);', 'M.b.tick(t); if (key === "wym" && !pdie) wymAim(W, M, T, t); }\n  try { wbScanFx(W, t);')
rep('function wbPentFx(M, g, q, st, T, t) {', '''/* v505 the Wyrm's lens beam aimed down at a world or a fleet near the black hole, and the flare where it hits */
function wymAim(W, M, T, t) { const b = M.b, L = b.lens; if (!L) return; M.wv = M.wv || [new TH.Vector3(), new TH.Vector3(), new TH.Vector3()];
  if (!L.visible) { M.tg = null; L.scale.set(1, 1, 1); if (M.hitS) M.hitS.visible = false; return; }
  if (!M.tg) { const g0 = b.grp.getWorldPosition(new TH.Vector3()), R0 = (b.r || 15) * b.grp.scale.x * 1.6, C = G.list.concat(PIRATES).map(p => { const q = P3(p, T, {}); return [p, Math.hypot(q.x - g0.x, q.z - g0.z)]; }).filter(([, d]) => d > R0 && d < R0 * 3.2).sort((a, c) => a[1] - c[1]).slice(0, 14); if (!C.length) return; M.tg = C[(Math.random() * C.length) | 0][0]; } // beyond its own coils
  const p = P3(M.tg, T, {}), tp = M.wv[0].set(p.x, p.y, p.z); b.grp.updateMatrixWorld(true); L.scale.set(1, 1, 1); L.lookAt(tp); L.updateMatrixWorld(true);
  const o = L.getWorldPosition(M.wv[1]), sc = L.getWorldScale(M.wv[2]).z || 1, d = o.distanceTo(tp); L.scale.z = Math.max(.2, d / (50 * sc));
  if (!M.hitS) { M.hitS = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex("255,190,110", .9), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); W.scene.add(M.hitS); }
  const f = L.children[1] ? L.children[1].material.opacity : 1; M.hitS.visible = f > .02; M.hitS.position.copy(tp); M.hitS.material.opacity = Math.min(1, f * 1.1); M.hitS.scale.setScalar(14 + 6 * Math.sin(t * .03) + 10 * f); }
function wbPentFx(M, g, q, st, T, t) {''')
s2 = re.sub(r"GAME_V = 504\b", "GAME_V = 505", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
