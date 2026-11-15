/* ---------- v589 battle effects remaster (owner's reference videos): skill banners over the ship that fires a special, violet chain
   lightning that leaps between enemy formations, starburst light rays on big blasts, and bold game-style damage numbers ---------- */
function fx589Spawn(b, v) { try { if (b.lowFx || v.bounce) return; const q = b.Q[v.s]; if (!q) return; const t = performance.now();
    /* skill banners: a Titan's or super boss's named attack, at most one per formation every 6 s */
    const sk = b.sk589 || (b.sk589 = {}); let name = null, col = null;
    if (TITAN_INFO[q.k] && (v.ab || !sk[v.s])) { name = TITAN_INFO[q.k].ab; col = q.side === "a" ? "#7af4ff" : "#ff8a5a"; }
    else if (typeof SBW !== "undefined" && SBW[q.k] && SBW[q.k].abil) { const A = SBW[q.k].abil; b.skN = b.skN || {}; const n = (b.skN[v.s] = ((b.skN[v.s] || 0) + 1)); name = A[n % Math.min(4, A.length)][0]; col = SBW[q.k].col || "#c890ff"; }
    else if (v.crit && (q.role === "capital" || q.role === "battleship" || q.role === "titan")) { name = "Critical Salvo"; col = "#ffd36b"; }
    if (name && (!sk[v.s] || t - sk[v.s] > 6000)) { sk[v.s] = t; (b.skb = b.skb || []).push({ i: v.s, t, txt: String(name).toUpperCase(), col }); if (b.skb.length > 4) b.skb.shift(); }
    /* chain lightning: ion and acid weapons arc from the target to up to two nearby enemy formations */
    if ((v.wk === "ion" || v.wk === "acid" || (q.k && /ion|storm|volt/i.test(q.k))) && (b.arcs589 || []).length < (b.Q.length > 60 ? 4 : 10)) (b.arcs589 = b.arcs589 || []).push({ s: v.s, e: v.e, t0: v.t, life: .42, col: v.wk === "acid" ? "140,255,120" : "190,130,255", seed: Math.random() * 1e4 });
  } catch (e) {} }
function fx589Draw(ctx, b, t, d, vs, scr, Q, T, vtx) { const dS = d / vs, lo = b.lowFx;
  /* starbursts: thin light rays fanning out of a big blast, slowly turning, plus a white-hot core */
  if (b.bursts589 && b.bursts589.length) { ctx.save(); ctx.globalCompositeOperation = "lighter"; b.bursts589 = b.bursts589.filter(o => t - o.t < o.life);
    for (const o of b.bursts589) { const k = (t - o.t) / o.life; if (k < 0) continue; const a = (1 - k) * (k < .1 ? k / .1 : 1), R = o.r * (.55 + k * .75); ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.rot + k * .35);
      for (let i = 0; i < o.n; i++) { const L = R * (.55 + ((i * 37) % 10) / 14), w = R * (.018 + ((i * 13) % 5) * .006); ctx.rotate(TAU / o.n); const g = ctx.createLinearGradient(0, 0, L, 0); g.addColorStop(0, `rgba(255,255,255,${.85 * a})`); g.addColorStop(.25, `rgba(${o.col},${.55 * a})`); g.addColorStop(1, `rgba(${o.col},0)`); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, -w); ctx.lineTo(L, 0); ctx.lineTo(0, w); ctx.fill(); }
      ctx.restore(); ctx.globalAlpha = a; const cr = R * .28; ctx.drawImage(glowSprite("rgba(255,255,255,1)"), o.x - cr, o.y - cr, cr * 2, cr * 2); ctx.globalAlpha = 1; }
    ctx.restore(); }
  /* chain lightning */
  if (b.arcs589 && b.arcs589.length) { b.arcs589 = b.arcs589.filter(m => T - m.t0 < m.life + .05); ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineJoin = "round"; ctx.lineCap = "round";
    for (const m of b.arcs589) { const age = T - m.t0; if (age < 0) continue; const A = scr[m.e]; if (!A || !(b.n[m.e] > 0 || age < .2)) continue; const k = age / m.life, a = (1 - k) * (.7 + .3 * Math.sin(t * .09 + m.seed));
      if (!m.hops) { const es = []; Q.forEach((q2, j) => { if (j !== m.e && q2.side === Q[m.e].side && b.n[j] > 0 && scr[j]) es.push([Math.hypot(scr[j].x - A.x, scr[j].y - A.y), j]); }); es.sort((x, y) => x[0] - y[0]); m.hops = [m.e].concat(es.slice(0, 2).map(x => x[1])); }
      const pts = m.hops.map(j => scr[j]).filter(Boolean); if (pts.length < 2) { const r0 = 22 * dS; pts.push({ x: A.x + r0, y: A.y - r0 * .6 }); }
      const jag = (P, Q2, seg, amp, sd) => { const out = [[P.x, P.y]]; for (let s = 1; s < seg; s++) { const u = s / seg, nx = -(Q2.y - P.y), ny = Q2.x - P.x, nl = Math.hypot(nx, ny) || 1, off = (Math.sin(sd + s * 12.9898 + Math.floor(t / 45) * 7.1) * 43758.5453 % 1) * amp; out.push([P.x + (Q2.x - P.x) * u + nx / nl * off, P.y + (Q2.y - P.y) * u + ny / nl * off]); } out.push([Q2.x, Q2.y]); return out; };
      for (let h = 0; h + 1 < pts.length; h++) { const P = pts[h], Q2 = pts[h + 1], Ln = Math.hypot(Q2.x - P.x, Q2.y - P.y), seg = Math.max(4, Math.min(14, Math.round(Ln / (14 * dS)))), path = jag(P, Q2, seg, Math.min(26 * dS, Ln * .12), m.seed + h * 3.7);
        for (const [w, al, c] of [[9, .22, m.col], [3.6, .55, m.col], [1.4, 1, "255,255,255"]]) { ctx.strokeStyle = `rgba(${c},${al * a})`; ctx.lineWidth = w * dS; ctx.beginPath(); path.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke(); }
        const gr = 16 * dS * (1 + .3 * Math.sin(t * .05)); ctx.globalAlpha = a; ctx.drawImage(glowSprite(`rgba(${m.col},1)`), Q2.x - gr, Q2.y - gr, gr * 2, gr * 2); ctx.globalAlpha = 1; } }
    ctx.restore(); }
  /* skill banners: a slanted glowing ribbon over the ship that slides in, holds and fades */
  if (b.skb && b.skb.length && !lo) { b.skb = b.skb.filter(o => t - o.t < 1900);
    for (const o of b.skb) { const A = scr[o.i]; if (!A) continue; const k = (t - o.t) / 1900, slide = Math.min(1, (t - o.t) / 160), a = k > .8 ? (1 - k) / .2 : 1, fs = 13 * dS; let x = A.x - (1 - slide) * 40 * dS;
      const y = A.y - 46 * dS - k * 8 * dS;
      ctx.save(); ctx.font = `italic 800 ${fs}px Oxanium, sans-serif`; const tw = ctx.measureText(o.txt).width, hw = tw / 2 + 14 * dS, hh = fs * .78; ctx.globalAlpha = a; { const W0 = ctx.canvas.width, xs = clamp(x * vs + (vtx || 0), hw * vs + 10 * d, W0 - hw * vs - 10 * d); x = (xs - (vtx || 0)) / vs; }
      const g = ctx.createLinearGradient(x - hw, 0, x + hw, 0); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(.15, "rgba(6,10,24,.82)"); g.addColorStop(.85, "rgba(6,10,24,.82)"); g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - hw + 8 * dS, y - hh); ctx.lineTo(x + hw + 8 * dS, y - hh); ctx.lineTo(x + hw - 8 * dS, y + hh); ctx.lineTo(x - hw - 8 * dS, y + hh); ctx.closePath(); ctx.fill();
      ctx.globalCompositeOperation = "lighter"; ctx.fillStyle = o.col; ctx.globalAlpha = a * .9; ctx.fillRect(x - hw + 4 * dS, y + hh - 1.6 * dS, hw * 2 - 8 * dS, 1.6 * dS); ctx.fillRect(x - hw + 12 * dS, y - hh, hw * 2 - 8 * dS, 1.2 * dS); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = a;
      ctx.textAlign = "center"; ctx.textBaseline = "middle"; const tg = ctx.createLinearGradient(0, y - fs / 2, 0, y + fs / 2); tg.addColorStop(0, "#ffffff"); tg.addColorStop(1, o.col); ctx.lineWidth = 3 * dS; ctx.strokeStyle = "rgba(0,0,0,.8)"; ctx.strokeText(o.txt, x, y + 1 * dS); ctx.fillStyle = tg; ctx.fillText(o.txt, x, y + 1 * dS); ctx.restore(); } } }
/* the damage numbers, game-style: they pop in big and settle, bold with a gradient and a heavy outline; critical hits are huge and gold */
function fx589Nums(ctx, b, t, d, vs, Q) { const dS = d / vs; b.nums = b.nums.filter(o => t - o.t < 1150); if (b.nums.length > 24) b.nums.splice(0, b.nums.length - 24);
  const numR = []; for (let ni = b.nums.length - 1; ni >= 0; ni--) { const o = b.nums[ni]; if (t < o.t) continue; const age = t - o.t, p = age / 1150, crit = o.txt === "CRITICAL", kill = /^−/.test(o.txt), yy = o.y - (1 - Math.pow(1 - p, 2)) * 40 * dS;
    if (numR.length >= (Q.length > 60 ? 7 : 99)) break; if (numR.some(([x2, y2]) => Math.abs(x2 - o.x) < 62 * dS && Math.abs(y2 - yy) < 18 * dS)) continue; numR.push([o.x, yy]);
    const pop = age < 90 ? 1.9 - age / 90 * .9 : age < 170 ? 1 + Math.sin((age - 90) / 80 * Math.PI) * .12 : 1, base = crit ? 15 : kill ? 21 : o.big ? 19 : 15, fs = base * dS * pop;
    ctx.save(); ctx.globalAlpha = p > .7 ? 1 - (p - .7) / .3 : 1; ctx.font = `${crit ? "italic " : ""}900 ${fs}px Oxanium, sans-serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const c1 = crit ? "#fff6c2" : "#ffffff", c2 = crit ? "#ffb21f" : kill ? "#ff3b3b" : o.col, g = ctx.createLinearGradient(0, yy - fs / 2, 0, yy + fs / 2); g.addColorStop(0, c1); g.addColorStop(.55, c2); g.addColorStop(1, crit ? "#c46a00" : c2);
    if (crit || kill) { ctx.globalCompositeOperation = "lighter"; const gr = fs * 1.6; ctx.globalAlpha *= .55; ctx.drawImage(glowSprite(crit ? "rgba(255,190,60,1)" : "rgba(255,60,60,1)"), o.x - gr, yy - gr * .6, gr * 2, gr * 1.2); ctx.globalAlpha = p > .7 ? 1 - (p - .7) / .3 : 1; ctx.globalCompositeOperation = "source-over"; }
    ctx.lineJoin = "round"; ctx.lineWidth = 4.2 * dS; ctx.strokeStyle = "rgba(4,6,14,.92)"; ctx.strokeText(o.txt, o.x, yy); ctx.fillStyle = g; ctx.fillText(o.txt, o.x, yy); ctx.restore(); } }
