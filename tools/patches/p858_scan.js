  /* the scan (v858: on its own clock from the moment the battle is first drawn, so a replay's time jumping about cannot restart or
     reverse it; it always sweeps from the left edge to the right; every ship of ours is marked a target as the field crosses it; then it
     all fades away. Eyes 0-1 s, the sweep .8-2.8 s, held to 3.4 s, faded by 4.2 s, and never again in that battle.) */
  if (b.kScan0 == null && !(b.intro > 0)) b.kScan0 = t; const sT = b.kScan0 == null ? -1 : (t - b.kScan0) / 1000; /* it starts when the battle does, after the VS card */
  if (!b.kScanDone && sT >= 0 && sT < 4.2) { ctx.globalCompositeOperation = "lighter"; const fade = sT < 3.4 ? 1 : 1 - (sT - 3.4) / .8, eyeK = Math.min(1, sT / 1);
    them.forEach((i, n) => { if (n / Math.max(1, them.length) > eyeK || !(b.n[i] > 0)) return; const P = scr[i], Lg = geoL(i); ctx.globalAlpha = .9 * fade; ctx.drawImage(rs, P.x - Lg * .15, P.y - Lg * .15, Lg * .3, Lg * .3); }); /* their eyes light, one by one */
    const k = clamp((sT - .8) / 2, 0, 1), x = W * k;
    if (k > 0 && k < 1) { ctx.globalAlpha = .9; ctx.strokeStyle = `rgba(${CNT_RED},1)`; ctx.lineWidth = 2.4 * d; ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      const gr = ctx.createLinearGradient(x - W * .14, 0, x, 0); gr.addColorStop(0, `rgba(${CNT_RED},0)`); gr.addColorStop(1, `rgba(${CNT_RED},.24)`); ctx.fillStyle = gr; ctx.globalAlpha = 1; ctx.fillRect(x - W * .14, 0, W * .14, H);
      ctx.globalAlpha = .25; ctx.lineWidth = 1 * d; ctx.beginPath(); for (let y = 0; y < H; y += 22 * d) { ctx.moveTo(x - W * .14, y); ctx.lineTo(x, y); } ctx.stroke(); } /* the laser field sweeping the map, left to right */
    const big = us.filter(i => b.n[i] > 0).sort((a, c) => (bLen(b.Q[c].k) || 1) - (bLen(b.Q[a].k) || 1)).slice(0, 3), mk = b.kMk || (b.kMk = {});
    for (const i of us) { const P = scr[i]; if (!(b.n[i] > 0)) continue; if (mk[i] == null && k > 0 && P.x <= x) mk[i] = sT; if (mk[i] == null) continue; const a = Math.min(1, (sT - mk[i]) / .25) * fade, Lg = geoL(i) * .75;
      ctx.globalAlpha = .85 * a; ctx.strokeStyle = `rgba(${CNT_RED},1)`; ctx.lineWidth = 1.6 * d; ctx.beginPath(); ctx.ellipse(P.x, P.y, Lg * .6, Lg * .3, 0, 0, TAU); ctx.stroke(); ctx.lineWidth = 2.2 * d; kBox(ctx, P.x, P.y, Lg * .7, d); /* each one marked */
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .95 * a; ctx.font = `800 ${(big.includes(i) ? 12 : 10) * d}px Oxanium, sans-serif`; ctx.textAlign = "center"; ctx.fillStyle = `rgba(${CNT_RED},1)`; ctx.strokeStyle = "rgba(0,0,0,.85)"; ctx.lineWidth = 3 * d; const lb = big.includes(i) ? (big.indexOf(i) ? "THREAT CATALOGUED" : "TARGET ACQUIRED") : "TARGET"; ctx.strokeText(lb, P.x, P.y - Lg * .5);
      ctx.fillText(big.includes(i) ? (big.indexOf(i) ? "THREAT CATALOGUED" : "TARGET ACQUIRED") : "TARGET", P.x, P.y - Lg * .5); ctx.globalCompositeOperation = "lighter"; }
    if (!b.kScanSnd && sT > .7) { b.kScanSnd = 1; try { mimSfx("hum", 0); } catch (e) {} try { if (!them.some(i => b.Q[i].k === "cneter") && advOnce("cntScan")) sbSay(CNT_SCAN_LINE); } catch (e) {} } }
  else if (sT >= 4.2) b.kScanDone = 1;
