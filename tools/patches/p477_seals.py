# v477 Remaster step 5b, the Convergence's rune seals (2026-12-09). Five rune seals hold the fusion together, one per element, between
# its wing and the heart. They are the real targets the aim buttons always were (the wing damage record): damage aimed at a seal cracks
# it on the model (it spins faster and flickers as it fills), and when the element is torn loose its seal bursts in its colour. With
# every seal gone the heart shows a white target ring: the fusion core is exposed. The aim bar, launch toast and guide say seals now.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("    // three rune rings, each carrying orbs\n    const rings = [[31, 1.15, 0,",
r"""    /* v477 the five rune seals holding the fusion together */
    const seals = {}; ORDER.forEach(k => { const p = P[k], g = new TH.Group(); g.position.set(Math.cos(p.a) * 19, Math.sin(p.a) * 19 + 2, 9); body.add(g); const m = runeRing(7.5, p.E.c1, .9); g.add(m); const m2 = runeRing(4.8, 0xffffff, .6); m2.rotation.z = .5; g.add(m2); const ed = new TH.Mesh(new TH.RingGeometry(7.55, 7.95, 96), glowMat(p.E.c1, .9)); ed.userData.dyn = 1; m.add(ed); for (const x of [m, m2, ed]) { x.material.depthTest = false; x.renderOrder = 12; }
      const gl = sprite(20, `rgba(${p.E.rgb},1)`, "px" + k); gl.material.opacity = .35; g.add(gl); const fl = sprite(16, `rgba(${p.E.rgb},1)`, "px" + k); fl.visible = false; g.add(fl); seals[k] = { g, m, m2, gl, fl, br: -1 }; });
    const coreTgt = new TH.Sprite(new TH.SpriteMaterial({ map: radial("elwkR", [[0, "rgba(255,255,255,0)"], [.68, "rgba(255,255,255,0)"], [.76, "rgba(255,255,255,1)"], [.84, "rgba(255,255,255,0)"], [1, "rgba(255,255,255,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); coreTgt.visible = false; coreTgt.material.depthTest = false; coreTgt.renderOrder = 13; body.add(coreTgt);
    // three rune rings, each carrying orbs
    const rings = [[31, 1.15, 0,""")
rep("      sw(fk < 0 ? -1 : (fk - .45) / .55); sw2(fk < 0 ? -1 : (fk - .48) / .52); hit(bell(fh, 0, .05, .4, 1), t); body.position.y = Math.sin(t * .0009) * 1.2 - crouch * 2; };",
"""      ORDER.forEach((k, i) => { const S0 = seals[k], p = P[k], gone = p.dead || p.shedT != null, c = Math.min(1, (api.seal && api.seal[k]) || 0); if (p.shedT != null && S0.br < 0) S0.br = t; const b = S0.br < 0 ? -1 : (t - S0.br) / 1600;
        S0.m.visible = S0.m2.visible = S0.gl.visible = !gone; if (!gone) { S0.m.rotation.z = t * (.0004 + c * .003) * (i % 2 ? -1 : 1); S0.m2.rotation.z = -t * (.0007 + c * .004); S0.m.material.opacity = .9 * form * (c > .4 && Math.random() < c * .3 ? .2 : 1); S0.m2.material.opacity = .6 * form * (1 - c * .5); S0.gl.material.opacity = (.3 + c * .4) * form; S0.g.scale.setScalar(1 + Math.sin(t * .003 + i) * .04 + c * .18); }
        S0.fl.visible = b >= 0 && b < 1; if (S0.fl.visible) { S0.fl.material.opacity = Math.min(1, (1 - b) * 1.3); S0.fl.scale.setScalar(16 + b * 80); } });
      { const open = form > .5 && ORDER.every(k => P[k].dead || P[k].shedT != null); coreTgt.visible = open; if (open) { const q = .5 + .5 * Math.sin(t * .005); coreTgt.position.copy(core.position); coreTgt.material.opacity = 1 - q * .3; coreTgt.scale.setScalar(42 - q * 10); } }
      sw(fk < 0 ? -1 : (fk - .45) / .55); sw2(fk < 0 ? -1 : (fk - .48) / .52); hit(bell(fh, 0, .05, .4, 1), t); body.position.y = Math.sin(t * .0009) * 1.2 - crouch * 2; };""")
# the map tells it how cracked each seal is (the damage aimed at it)
rep("const al = wbPentAlive(T), sh = (st.shed || []).map(k => WB[k].el);",
    "b.seal = {}; for (const k of WB_EL) b.seal[WB[k].el] = Math.min(1, ((st.wing || {})[k] || 0) / (WB_SEG * .12)); const al = wbPentAlive(T), sh = (st.shed || []).map(k => WB[k].el);")
# the words: seals, not wings
rep("/* v402 the Pentarch's wings: aim your fleet at one (its damage counts toward breaking that wing) or at the core */",
    "/* v402 the Pentarch's wings, v477 its rune seals: aim your fleet at one (its damage counts toward breaking that seal) or at the core */")
rep("<p class=\"note\">Every fifth of its hull tears one element loose. Aim at a wing to break it sooner and silence it.</p>",
    "<p class=\"note\">Five rune seals hold the fusion together, one for each element. Aim at a seal to crack it: when it breaks, that element is torn loose and the Pentarch weakens. Every fifth of its hull breaks one too. With all five broken, its core is exposed.</p>")
rep("aimed at ${WB[aim].n}'s wing", "aimed at ${WB[aim].n}'s seal")
rep("At every fifth of its hull it tears an element loose; aim at a wing to break it sooner.", "Five rune seals hold it together; aim at one to break it sooner and tear that element loose. Every fifth of its hull breaks one too.")
rep("At every fifth of its hull the Pentarch tears one element loose, and you can aim at a wing to break it sooner.",
    "Five rune seals hold the Pentarch together, one for each element: aim at a seal to crack it, and when it breaks that element is torn loose. Every fifth of its hull breaks one too, and with all five broken its core is exposed.")
s = re.sub(r"GAME_V = 476\b", "GAME_V = 477", s)
open(P, 'w').write(s)
