# v507 the Wyrm turns its head to its target (owner: the laser pointed down but the head did not). As its jaws open for the lens
# beam its whole head swings round until its mouth faces the world or fleet it picked, the beam fires straight out of its mouth,
# and the head eases back to its coil when the jaws close.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
i0 = s.index('function wymAim(W, M, T, t) {'); j = s.index('function wbPentFx(M, g, q, st, T, t) {', i0)
NEW = r'''function wymAim(W, M, T, t) { const b = M.b, L = b.lens; if (!L) return; const hd = L.parent, head = hd && hd.parent; if (!head) return; M.wv = M.wv || [new TH.Vector3(), new TH.Vector3(), new TH.Vector3(), new TH.Quaternion(), new TH.Quaternion(), new TH.Quaternion()];
  const gape = clamp(-hd.rotation.x / .25, 0, 1); // the jaws opening for the lens: 0 closed, 1 wide
  if (gape < .02 && !L.visible) { M.tg = null; M.hw = 0; L.scale.set(1, 1, 1); if (M.hitS) M.hitS.visible = false; return; }
  if (!M.tg) { const g0 = b.grp.getWorldPosition(new TH.Vector3()), R0 = (b.r || 15) * b.grp.scale.x * 1.6, C = G.list.concat(PIRATES).map(p => { const q = P3(p, T, {}); return [p, Math.hypot(q.x - g0.x, q.z - g0.z)]; }).filter(([, d]) => d > R0 && d < R0 * 3.2).sort((a, c) => a[1] - c[1]).slice(0, 14); if (!C.length) return; M.tg = C[(Math.random() * C.length) | 0][0]; } // beyond its own coils
  const p = P3(M.tg, T, {}), tp = M.wv[0].set(p.x, p.y, p.z); L.rotation.set(0, 0, 0); L.scale.set(1, 1, 1); b.grp.updateMatrixWorld(true);
  // swing the whole head so its mouth (the lens) faces the target: the turn that takes the lens's line onto the target's, eased in with the jaws
  M.hw = ss(0, .6, gape); const qp = head.parent.getWorldQuaternion(new TH.Quaternion()).invert(), qH0 = head.getWorldQuaternion(M.wv[5]).clone(), qW = qH0.clone();
  for (let it = 0; it < 4; it++) { const o = L.getWorldPosition(M.wv[1]), d0 = M.wv[2].set(0, 0, 1).applyQuaternion(L.getWorldQuaternion(M.wv[3])).normalize(), d1 = tp.clone().sub(o).normalize(); qW.premultiply(M.wv[4].setFromUnitVectors(d0, d1)); head.quaternion.copy(qp.clone().multiply(qW)); head.updateMatrixWorld(true); } // the mouth moves as the head turns: a few passes settle it on the target
  head.quaternion.copy(qp.clone().multiply(qH0.slerp(qW, M.hw))); b.grp.updateMatrixWorld(true);
  if (!L.visible) { if (M.hitS) M.hitS.visible = false; return; }
  const o2 = L.getWorldPosition(M.wv[1]); L.lookAt(tp); L.updateMatrixWorld(true); const sc = L.getWorldScale(M.wv[2]).z || 1, d = o2.distanceTo(tp); L.scale.z = Math.max(.02, d / (50 * sc));
  if (!M.hitS) { M.hitS = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex("255,190,110", .9), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); W.scene.add(M.hitS); }
  const f = L.children[1] ? L.children[1].material.opacity : 1; M.hitS.visible = f > .02; M.hitS.position.copy(tp); M.hitS.material.opacity = Math.min(1, f * 1.1); M.hitS.scale.setScalar(14 + 6 * Math.sin(t * .03) + 10 * f); }
'''
s = s[:i0] + NEW + s[j:]
s2 = re.sub(r"GAME_V = 506\b", "GAME_V = 507", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
