"""v781: Medusara, second pass toward her painting (owner approved: "build it all").
- Her crown and gem stay on: the gold diadem over her brow, its tall spikes and the magenta gem (the painted face skin used to hide
  them all when it loaded).
- Her lower half: below her chin the planet continues as a cracked dark-stone sphere split by glowing violet and gold seams, wrapped
  in the storm clouds, as painted.
- Cobra serpents: narrower, longer heads with a flared cobra hood behind each (the heads read as open duck bills).
- Stone Gaze, a new attack: twin red beams fan out from her eyes in opposite directions; every ship they cross turns to cracked grey
  stone, then crumbles. Her fight cycles Petrifying Gaze, Serpent Strike, Stone Gaze, with Shattered Visage still her signature.
Applies on top of v780."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 780;", "const GAME_V = 781;")
# the crown and gem stay when the skin loads (only the pink crystal studs are hidden)
rep('(c.material === MG && !(c.geometry && c.geometry.type === "ConeGeometry")) || (c.material.color && c.material.color.getHex() === 0x2a0a18))) c.visible = false; }); gemG.children.forEach(c => { if (c.isMesh) c.visible = false; });',
    '(c.material.color && c.material.color.getHex() === 0x2a0a18))) c.visible = false; }); /* v781 the crown, its spikes and the gem stay */')
# cobra heads: narrower and longer, with a hood
rep("hd = put(g, new TH.Group(), tip.toArray(), null, 3.1)", "hd = put(g, new TH.Group(), tip.toArray(), null, [2.5, 3.0, 3.6])")
rep("      { put(hd, new TH.Mesh(VHT, MSk), [0, .08, 0]);", "      { put(hd, new TH.Mesh(VHT, MSk), [0, .08, 0]); { const hood = put(hd, sph(MSk, 16), [0, .15, -.75], [-.5, 0, 0], [1.25, .95, .2]); } /* v781 a cobra hood */")
# the lower sphere: cracked dark stone with glowing seams, under her chin
rep("const clouds = put(body, new TH.Group(), [0, 14, 0], null, 1.25);", r'''const lowT = (() => { const N = 1024, c = cv(N, N / 2), e = cv(N, N / 2), x = c.getContext("2d"), y = e.getContext("2d"); x.fillStyle = "#2a2630"; x.fillRect(0, 0, N, N / 2); y.fillStyle = "#000"; y.fillRect(0, 0, N, N / 2);
        for (let i = 0; i < 900; i++) { x.fillStyle = `rgba(${60 + rnd() * 40 | 0},${54 + rnd() * 34 | 0},${70 + rnd() * 40 | 0},${.25 + rnd() * .3})`; x.fillRect(rnd() * N, rnd() * N / 2, 3 + rnd() * 30, 2 + rnd() * 14); }
        for (let i = 0; i < 46; i++) { let px = rnd() * N, py = N * .12 + rnd() * N * .38, a = rnd() * TAU; const gold = rnd() < .45, P = [[px, py]]; for (let k = 0; k < 18 + rnd() * 20; k++) { a += (rnd() - .5) * 1.3; px += Math.cos(a) * 9; py += Math.sin(a) * 6; P.push([px, py]); }
          const ln = (cx2, col, w, al) => { cx2.globalAlpha = al; cx2.strokeStyle = col; cx2.lineWidth = w; cx2.beginPath(); P.forEach(([u2, v2], k) => k ? cx2.lineTo(u2, v2) : cx2.moveTo(u2, v2)); cx2.stroke(); cx2.globalAlpha = 1; };
          ln(x, "#120c18", 4, .9); ln(y, gold ? "#ffb050" : "#b060ff", 7, .35); ln(y, gold ? "#ffe0a0" : "#e0b0ff", 2, 1); }
        const T1 = new TH.CanvasTexture(c), T2 = new TH.CanvasTexture(e); T1.encoding = T2.encoding = TH.sRGBEncoding; return [T1, T2]; })();
      const lowM = new TH.MeshStandardMaterial({ map: lowT[0], emissiveMap: lowT[1], emissive: 0xffffff, emissiveIntensity: 2.4, roughness: .8, metalness: .2, envMapIntensity: .3 }); lowM.userData.P = {};
      const lowS = put(body, new TH.Mesh(new TH.SphereGeometry(15, LO ? 32 : 56, LO ? 20 : 36, 0, TAU, Math.PI * .35, Math.PI * .65), lowM), [0, 4.5, -2.5]); lowS.userData.dyn = 1; /* v781 the planet below her chin */
      const clouds = put(body, new TH.Group(), [0, 14, 0], null, 1.25);''')
rep("clouds.rotation.y = T * .03;", "clouds.rotation.y = T * .03; lowS.rotation.y = -T * .01; lowM.emissiveIntensity = (2.1 + .5 * Math.sin(T * .9)) * aw * live * st; lowS.visible = die < .7;")
# Stone Gaze in battle
rep('med: { gaze: "gaze", serpents: "lunge", shards: "storm" }', 'med: { gaze: "gaze", serpents: "lunge", shards: "storm", stone: "gaze" }')
rep('med: { col: "125,255,176", seq: ["gaze", "serpents"], sig: "shards" }', 'med: { col: "125,255,176", seq: ["gaze", "serpents", "stone"], sig: "shards" }')
rep("gaze: 1.6, serpents: 1.4, shards: 2.2,", "gaze: 1.6, serpents: 1.4, shards: 2.2, stone: 2.6,")
rep("else if (/rain|shards|crush|wave|throw|orrery|gate|lances|sun/.test(m.a))", "else if (/rain|shards|crush|wave|throw|orrery|gate|lances|sun|stone/.test(m.a))")
ST = r'''    else if (m.a === "stone") { /* v781 Stone Gaze: twin red beams fan out from her eyes; ships they cross turn to stone, then crumble */ const ey = cy - B.ah * .12, E2 = [[cx - B.aw * .09, ey, -1], [cx + B.aw * .09, ey, 1]], hit = m.hit || (m.hit = {}), k2 = clamp((u - .12) / .5, 0, 1), fade = u > .66 ? Math.max(0, (.8 - u) / .14) : 1;
      if (u < .14) { const r = B.aw * .06 * (u / .14); for (const [x, y2] of E2) { ctx.globalAlpha = u / .14; ctx.drawImage(glowSprite("#ff3020"), x - r * 2, y2 - r * 2, r * 4, r * 4); } }
      else if (fade > 0) { E2.forEach(([x, y2, sd]) => { const a = Math.PI / 2 - sd * (-.15 + k2 * 1.45); for (const [lw, al, c2] of [[26, .22, "rgba(255,40,30,1)"], [9, .6, "rgba(255,70,50,1)"], [3, 1, "#fff0e8"]]) { ctx.globalAlpha = al * fade; ctx.strokeStyle = c2; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.moveTo(x, y2); ctx.lineTo(x + Math.cos(a) * R * 1.3, y2 + Math.sin(a) * R * 1.3); ctx.stroke(); }
          fx.forEach((p, j) => { const i = foes[j]; if (hit[i] || Math.sign(p.x - cx || 1) !== sd) return; const ap = Math.atan2(p.y - y2, p.x - x); if (sd > 0 ? ap >= a : ap <= a) hit[i] = t;}); }); once("bang", () => big(7)); }
      ctx.save(); ctx.globalCompositeOperation = "source-over"; for (const i in hit) { const p = scr[i]; if (!p) continue; const k3 = (t - hit[i]) / 1500; if (k3 < 0) continue;
        if (k3 < 1) { ctx.globalAlpha = .75; ctx.fillStyle = "rgb(140,138,132)"; ctx.beginPath(); ctx.ellipse(p.x, p.y, 20 * d, 8 * d, 0, 0, TAU); ctx.fill(); ctx.strokeStyle = "rgb(60,56,52)"; ctx.lineWidth = 1.4 * d; ctx.beginPath(); const nc = 2 + Math.floor(k3 * 5); for (let q = 0; q < nc; q++) { const a2 = q * 2.4 + +i; ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + Math.cos(a2) * 18 * d, p.y + Math.sin(a2) * 7 * d); } ctx.stroke(); }
        else if (k3 < 2) { const k4 = k3 - 1; ctx.globalAlpha = 1 - k4; ctx.fillStyle = "rgb(150,146,138)"; for (let q = 0; q < 7; q++) { const a2 = q * .9 + +i, dd = k4 * (10 + q * 3) * d; ctx.fillRect(p.x + Math.cos(a2) * dd, p.y + Math.sin(a2) * dd * .6 + k4 * k4 * 30 * d, 4 * d, 3 * d); } if (!m["c" + i]) { m["c" + i] = 1; aexBoom(b, p.x, p.y, t, 1.2, +i % 3 === 0); } } } ctx.restore(); }
    else if (m.a === "throw") {'''
rep('    else if (m.a === "throw") {', ST)
rep('["Ruin Volley", "The gothic towers on her gold ring fire on the fleets."],', '["Ruin Volley", "The gothic towers on her gold ring fire on the fleets."], ["Stone Gaze", "Twin red beams fan out from her eyes: every ship they cross turns to stone, then crumbles."],')
open(p, "w", encoding="utf-8").write(s)
print("ok")
