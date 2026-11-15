/* ---------- v579 The Eclipse: the year's verdict. The Sunday after the tenth seal, the black hole goes silent and the Judge weighs
   the Seal Ledger: one column of light rises where each chapter was fought (gold held, red cracked), then he gives his verdict for the
   whole galaxy. Seven or more seals held: Worthy (gold floods out from his palm). Four to six: Weighed (he holds the Cube still and
   gives us another year). Three or fewer: Found Wanting (his eyes turn red and a violet rift opens in the black hole, and stays
   until next year's Eclipse). ---------- */
function eclHeld(s0) { try { return finLedger(s0).filter(x => x.st === "held").length; } catch (e) { return 0; } }
function eclVerdict(s0) { if (G.eclForce && G.finSim && G.finSim.k === "ecl") return G.eclForce; const h = eclHeld(s0); return h >= 7 ? "worthy" : h >= 4 ? "weighed" : "wanting"; }
const ECL_COL = { worthy: 0xffd27a, weighed: 0x7dffa0, wanting: 0xff3a2a };
function eclSet(W, t, F) { const D = FIN_EV.ecl, e = F.e, E = D.st.map(s => s[0]); let X = W.fin;
  if (!X || X.s0 !== F.s0 || X.k !== F.k) { X = finNew(W, F); X.cp = new TH.Vector3(); X.fv = new TH.Vector3(); X.hd = new TH.Vector3(); X.R = new TH.Vector3(); X.U = new TH.Vector3(); X.foc = X.fv; X.dist = 1650; X.v = eclVerdict(F.s0);
    let led = []; try { led = G.finSim ? finKeys().map((k, i) => ({ k, st: X.v === "worthy" ? (i % 5 === 3 ? "cracked" : "held") : X.v === "weighed" ? (i % 2 ? "cracked" : "held") : (i % 4 === 0 ? "held" : "cracked") })) : finLedger(F.s0).map(x => ({ k: x.k, st: x.st })); } catch (er) {}
    X.cols = led.map((x, i) => { let p = { x: 0, y: 0, z: 0 }; try { p = x.k === "dv" || x.k === "conv" ? { x: Math.cos(i) * 60, y: 0, z: Math.sin(i) * 60 } : finP1(x.k, F.s0); } catch (er) {} const held = x.st === "held", s = finSpr(W, X, held ? "255,214,120" : "255,70,50", held ? 0xffd27a : 0xff3a2a); s.position.set(p.x, (p.y || 0) + 140, p.z); s.userData = { at: E[1] + 60e3 + i * 110e3, held, p }; const b = finSpr(W, X, held ? "255,240,200" : "255,120,100", held ? 0xfff0c8 : 0xff6040); b.position.set(p.x, (p.y || 0) + 6, p.z); s.userData.base = b; return s; });
    X.hole = finSpr(W, X, "255,220,170", 0xffd8a0); X.hole.material.map = finPhotonTex(); X.wave = finRing(X, ECL_COL[X.v], 192); X.wave2 = finRing(X, ECL_COL[X.v], 192); X.glow = finSpr(W, X, "255,230,160", ECL_COL[X.v]); X.rift = finSpr(W, X, "170,90,255", 0xc080ff); X.rift.material.map = finSwirlTex("190,110,255"); X.rift2 = finSpr(W, X, "150,60,255", 0x8a40ff); X.flash = finSpr(W, X, "255,255,255", 0xffffff); }
  try { if (W.nexus) W.nexus.getWorldPosition(X.cp); } catch (er) {}
  const end = 1 - fsm((e - D.set) / 50e3), dark = fsm(e / 90e3) * (1 - fsm((e - E[2]) / 20e3) * (X.v === "wanting" ? .3 : 1)) * end, v = X.v, uV = fseg(e, E[2], D.set);
  /* the silence: the black hole's light goes out */
  X.hole.position.set(0, 2, 0); X.hole.scale.setScalar(180 * (1 - .7 * fsm(e / 120e3))); X.hole.material.opacity = .9 * (1 - fsm(e / 150e3)) + (e >= E[2] && v !== "wanting" ? .7 * fsm(uV * 4) * end : 0);
  /* the weighing: one column per chapter */
  for (const s of X.cols) { const u = s.userData, k = fsm((e - u.at) / 8e3) * (e < E[2] + 6e4 ? 1 : 1 - fsm((e - E[2] - 6e4) / 3e4)) * end, pulse = .8 + .2 * Math.sin(t * .005 + u.at); s.position.y = (u.p.y || 0) + 330 * k; s.scale.set(60 + 20 * k, 660 * k, 1); s.material.opacity = .9 * k * pulse; u.base.scale.setScalar(170 * k * (1 + .5 * Math.max(0, 1 - (e - u.at) / 4e3))); u.base.material.opacity = k; }
  /* the verdict */
  const vk = e >= E[2] ? end : 0, fl = Math.max(0, 1 - Math.abs(e - E[2]) / 4e3); X.flash.position.set(X.cp.x, X.cp.y + 40, X.cp.z); X.flash.scale.setScalar(300 + 1800 * fl); X.flash.material.opacity = fl;
  X.wave.position.set(X.cp.x, X.cp.y + 2, X.cp.z); X.wave2.position.copy(X.wave.position);
  if (v === "worthy") { const w = (uV * 5) % 1; X.wave.scale.setScalar(40 + 1500 * w); X.wave.material.opacity = vk * .7 * (1 - w); const w2 = (uV * 5 + .5) % 1; X.wave2.scale.setScalar(40 + 1500 * w2); X.wave2.material.opacity = vk * .7 * (1 - w2); }
  else if (v === "weighed") { const w = (uV * 3) % 1; X.wave.scale.setScalar(60 + 600 * w); X.wave.material.opacity = vk * .5 * (1 - w); X.wave2.material.opacity = 0; }
  else { X.wave.material.opacity = X.wave2.material.opacity = 0; }
  X.glow.position.set(X.cp.x, X.cp.y + 10, X.cp.z); X.glow.scale.setScalar((v === "worthy" ? 700 : 360) * (1 + .1 * Math.sin(t * .003))); X.glow.material.opacity = vk * (v === "wanting" ? 0 : .6);
  X.rift.position.set(0, 8, 0); X.rift.material.rotation = t * .0006; X.rift.scale.setScalar(v === "wanting" ? 100 + 600 * fsm(uV * 3) : 0); X.rift.material.opacity = v === "wanting" ? vk : 0; X.rift2.position.set(0, 6, 0); X.rift2.scale.setScalar(v === "wanting" ? 120 + 700 * fsm(uV * 3) : 0); X.rift2.material.opacity = v === "wanting" ? vk * (.55 + .2 * Math.sin(t * .004)) : 0;
  /* the camera lifts to the Judge for his verdict */
  { const A = W.celArt, cam = W.camera, k = fsm((e - E[2] - 4e3) / 20e3) * .92; X.fv.copy(X.cp); if (A && cam && k > 0) { X.R.setFromMatrixColumn(cam.matrixWorld, 0); X.U.setFromMatrixColumn(cam.matrixWorld, 1); X.hd.copy(A.grp.position).addScaledVector(X.R, (395 / 1100 - .5) * CEL_ART_W).addScaledVector(X.U, (.5 - 160 / 619) * CEL_ART_W * CEL_ART_AR); X.fv.lerp(X.hd, k); } }
  if (G.finFollow && performance.now() < G.finFollow) X.watched = 1; if (X.watched && e >= E[2] && !X.lift && view === "galaxy" && !sheet && G3 && G3.cam) { X.lift = 1; G.finFollow = performance.now() + 240000; const c = G3.cam; c.cineObj = null; c.follow = null; c.followFleet = null; c.goal = { tx: X.cp.x, ty: X.cp.y, tz: X.cp.z, dist: 1650, th: .7 }; }
  W.renderer.toneMappingExposure = X.exp0 * (1 - .45 * dark + (v === "worthy" ? .25 * vk * fsm(uV * 3) : 0));
  /* her verdict lines (the stage calls cover the silence and the weighing) */
  if (e >= E[2] + 3e3) { G.finSaid = G.finSaid || {}; const id = F.s0 + "eclv"; if (!G.finSaid[id]) { G.finSaid[id] = 1; sbSay(ECL_SAY[v][0]); setTimeout(() => { try { sbSay(ECL_SAY[v][1]); } catch (er) {} }, 15000); } } }
FIN_SET.ecl = eclSet;
/* a verdict of Found Wanting leaves a violet rift in the black hole until the next Eclipse */
FIN_SCAR.ecl = (W, Z) => { const r = new TH.Sprite(new TH.SpriteMaterial({ map: finSwirlTex("170,90,255"), color: 0xa860ff, transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false })); r.position.set(0, 4, 0); r.scale.setScalar(150); Z.grp.add(r);
  return t => { r.material.rotation = t * .0003; r.material.opacity = .4 + .15 * Math.sin(t * .0017); }; };
