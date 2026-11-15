/* ---------- v582 the casino Glyph Wheel: real slot-machine sound, a jackpot show, paid spins, better prizes, and a daily reminder ---------- */
const WHL_COST = 5, WHL_PACK = [5, 22], WHL_CAP = 25; /* a paid spin, a pack of five, at most 25 bought a day */
const whlTot = () => WHEEL.reduce((a, W) => a + W.w, 0), whlPct = W => { const p = W.w / whlTot() * 100; return p < 1 ? p.toFixed(2) : p.toFixed(1); };
const whlFree = () => (S.shopFree || "") !== shopDay();
const whlBon = () => (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay();
const whlBought = () => S.whlPd && S.whlPd.d === shopDay() ? S.whlPd.n : 0;
const whlReady = () => whlFree() || whlBon() || (S.whlCr || 0) > 0;
function whlBuy(n) { const cost = n === 1 ? WHL_COST : WHL_PACK[1]; if (G.wheel) return; if (whlBought() + n > WHL_CAP) return toast(`That's the most spins for today (${WHL_CAP}). The wheel resets at the daily reset.`, "warn");
  if ((S.shards || 0) < cost) return toast(`That costs ◆${cost}.`, "warn");
  act(() => { S.shards -= cost; S.whlCr = (S.whlCr || 0) + n; S.whlPd = { d: shopDay(), n: whlBought() + n }; vipAdd(cost * 10); bump("shopBuys"); });
  try { WSFX.coins(.5, 6); } catch (e) {} if (n === 1) setTimeout(() => { try { wheelPull(); } catch (e) {} }, 120); }
/* the sound: synthesised so it costs no download */
const WSFX = {
  ok: () => { try { return SFX.ok(); } catch (e) { return false; } },
  ping(t, f, a, d) { const c = AU.ctx; for (const [m, g] of [[1, 1], [2.76, .45], [5.4, .2]]) { const o = c.createOscillator(); o.type = "sine"; o.frequency.value = f * m; SFX.env(o, t, a * g, d / m * 1.4); o.start(t); o.stop(t + d + .05); } },
  /* the lever: a heavy clunk, the spring, then the reels whoosh away */
  lever() { if (!WSFX.ok()) return; const c = AU.ctx, t = c.currentTime;
    { const n = noiseSrc(), f = c.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = 500; n.connect(f); SFX.env(f, t, .5, .14); n.start(t); n.stop(t + .16); }
    { const o = c.createOscillator(); o.type = "triangle"; o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(48, t + .18); SFX.env(o, t, .45, .22); o.start(t); o.stop(t + .25); }
    { const o = c.createOscillator(), l = c.createOscillator(), lg = c.createGain(); o.type = "sine"; o.frequency.value = 420; l.frequency.value = 28; lg.gain.value = 90; l.connect(lg); lg.connect(o.frequency); SFX.env(o, t + .05, .07, .35); o.start(t + .05); l.start(t + .05); o.stop(t + .45); l.stop(t + .45); }
    { const n = noiseSrc(), f = c.createBiquadFilter(), tt = t + .12; f.type = "bandpass"; f.Q.value = 1.4; f.frequency.setValueAtTime(300, tt); f.frequency.exponentialRampToValueAtTime(2400, tt + .7); n.connect(f); SFX.env(f, tt, .16, .8); n.start(tt); n.stop(tt + .85); } },
  /* each peg: a crisp ratchet clack, brighter while the wheel is fast */
  tick(sp) { if (!WSFX.ok()) return; const c = AU.ctx, t = c.currentTime, k = Math.min(1, sp / 900);
    { const n = noiseSrc(), f = c.createBiquadFilter(); f.type = "bandpass"; f.frequency.value = 2600 + 1600 * k; f.Q.value = 5; n.connect(f); SFX.env(f, t, .22, .03); n.start(t); n.stop(t + .04); }
    { const o = c.createOscillator(); o.type = "square"; o.frequency.setValueAtTime(1100 + 500 * k, t); o.frequency.exponentialRampToValueAtTime(500, t + .025); SFX.env(o, t, .035, .03); o.start(t); o.stop(t + .04); } },
  /* coins pouring into a tray */
  coins(dur, n) { if (!WSFX.ok()) return; const t = AU.ctx.currentTime; for (let i = 0; i < n; i++) { const tt = t + Math.pow(Math.random(), 1.4) * dur; WSFX.ping(tt, 2300 + Math.random() * 2400, .05 + Math.random() * .05, .18 + Math.random() * .2); } },
  /* the slot-machine bell: a hammer on a bell, fast */
  bell(t, dur, f) { const c = AU.ctx; f = f || 1250; for (let i = 0; i < dur * 16; i++) { const tt = t + i / 16; WSFX.ping(tt, f * (i % 2 ? 1 : 1.19), .07, .12); } },
  /* a prize: ding-ding, a rising run and coins (bigger prizes ring longer) */
  win(lv) { if (!WSFX.ok()) return; const c = AU.ctx, t = c.currentTime, ns = lv >= 2 ? [72, 76, 79, 84, 88, 91, 96] : lv ? [72, 76, 79, 84, 88] : [76, 79, 84];
    ns.forEach((m, i) => { const o = c.createOscillator(), tt = t + i * .075; o.type = "square"; o.frequency.value = 440 * Math.pow(2, (m - 69) / 12); const f = c.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = 3200; o.connect(f); SFX.env(f, tt, .05, .28); o.start(tt); o.stop(tt + .32); });
    WSFX.bell(t + ns.length * .075, lv >= 2 ? 1.4 : lv ? .7 : .25); WSFX.coins(lv >= 2 ? 2.2 : lv ? 1.2 : .6, lv >= 2 ? 60 : lv ? 30 : 12); },
  /* the jackpot: the alarm bells, the fanfare, a long shower of coins, then the big chord */
  jackpot(mega) { if (!WSFX.ok()) return; const c = AU.ctx, t = c.currentTime, L = mega ? 5.5 : 3.6;
    WSFX.bell(t, L * .8, 1180); WSFX.bell(t + .03, L * .8, 1580);
    const run = [60, 64, 67, 72, 76, 79, 84, 88, 91, 96]; for (let r = 0; r < (mega ? 3 : 2); r++) run.forEach((m, i) => { const o = c.createOscillator(), tt = t + r * 1.05 + i * .085; o.type = "square"; o.frequency.value = 440 * Math.pow(2, (m - 69) / 12); const f = c.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = 3600; o.connect(f); SFX.env(f, tt, .055, .3); o.start(tt); o.stop(tt + .34); });
    const ch = t + (mega ? 3.2 : 2.15); [48, 60, 64, 67, 72, 76].forEach(m => { const o = c.createOscillator(); o.type = "sawtooth"; o.frequency.value = 440 * Math.pow(2, (m - 69) / 12); const f = c.createBiquadFilter(); f.type = "lowpass"; f.frequency.setValueAtTime(600, ch); f.frequency.exponentialRampToValueAtTime(4200, ch + .4); o.connect(f); SFX.env(f, ch, .06, 2.4); o.start(ch); o.stop(ch + 2.5); });
    { const o = c.createOscillator(); o.type = "sine"; o.frequency.setValueAtTime(55, ch); SFX.env(o, ch, .5, 1.6); o.start(ch); o.stop(ch + 1.7); }
    WSFX.coins(L, mega ? 220 : 130); }
};
/* the show: JACKPOT (or BIG WIN) over the whole screen, gold rays, the letters slamming in, the shards counting up, coins raining */
function wheelShow(W) { const lv = W.jack === 2 ? 3 : W.jack ? 2 : 1; try { document.getElementById("gwjp") && document.getElementById("gwjp").remove(); } catch (e) {}
  const el = document.createElement("div"); el.id = "gwjp"; el.className = "gwjp l" + lv; const word = lv === 3 ? "MEGA JACKPOT" : lv === 2 ? "JACKPOT" : "BIG WIN";
  el.innerHTML = `<canvas></canvas><div class="gwjr"></div><div class="gwjc"><div class="gwjt">${[...word].map((ch, i) => `<span style="--i:${i}">${ch === " " ? "&nbsp;" : ch}</span>`).join("")}</div><div class="gwja">${W.k === "sh" ? `◆<b>0</b>` : esc(wheelName(W))}</div><small>Tap to collect</small></div>`;
  document.body.appendChild(el); const app = document.getElementById("app"); if (app && lv >= 2) { app.classList.remove("gwshake"); void app.offsetWidth; app.classList.add("gwshake"); setTimeout(() => app.classList.remove("gwshake"), 900); }
  const cv = el.querySelector("canvas"), x = cv.getContext("2d"), dpr = Math.min(devicePixelRatio || 1, 2), P = [], t0 = performance.now(), life = lv === 3 ? 7000 : lv === 2 ? 5200 : 2800, amt = el.querySelector(".gwja b");
  const fit = () => { cv.width = innerWidth * dpr; cv.height = innerHeight * dpr; }; fit();
  const coin = (fx, fy, up) => { const a = up ? -Math.PI / 2 + (Math.random() - .5) * 1.6 : Math.PI / 2, v = up ? 500 + Math.random() * 700 : 80 + Math.random() * 220; P.push({ x: fx, y: fy, vx: Math.cos(a) * v + (up ? 0 : (Math.random() - .5) * 60), vy: Math.sin(a) * v, r: 9 + Math.random() * 9, s: Math.random() * 6, w: 4 + Math.random() * 8, k: Math.random() < (lv === 3 ? .45 : .25) ? 1 : 0, h: Math.random() * 360 }); };
  for (let i = 0; i < (lv === 1 ? 40 : 110); i++) coin(innerWidth / 2, innerHeight * .52, true);
  let raf = 0; const frame = now2 => { const u = now2 - t0, dt = 1 / 60; if (!el.isConnected) return; raf = requestAnimationFrame(frame); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, innerWidth, innerHeight);
    if (u < life - 1200) for (let i = 0; i < (lv === 3 ? 6 : lv === 2 ? 4 : 1); i++) coin(Math.random() * innerWidth, -30, false);
    if (lv >= 2 && u < life - 1500 && Math.random() < .06) for (let i = 0; i < 26; i++) coin(innerWidth * (Math.random() < .5 ? .15 : .85), innerHeight * .95, true);
    for (let i = P.length - 1; i >= 0; i--) { const p = P[i]; p.vy += 900 * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.s += p.w * dt; if (p.y > innerHeight + 40) { P.splice(i, 1); continue; }
      const sx = Math.abs(Math.cos(p.s)); x.save(); x.translate(p.x, p.y); if (p.k) { x.rotate(p.s * .5); x.fillStyle = lv === 3 ? `hsl(${(p.h + u * .2) % 360},100%,70%)` : "#d79bff"; x.shadowColor = x.fillStyle; x.shadowBlur = 10; x.beginPath(); x.moveTo(0, -p.r); x.lineTo(p.r * .62, 0); x.lineTo(0, p.r); x.lineTo(-p.r * .62, 0); x.closePath(); x.fill(); }
      else { x.scale(Math.max(.12, sx), 1); const g = x.createRadialGradient(-p.r * .3, -p.r * .3, 1, 0, 0, p.r); g.addColorStop(0, "#fff6c8"); g.addColorStop(.5, "#ffcc3a"); g.addColorStop(1, "#b0700a"); x.fillStyle = g; x.beginPath(); x.arc(0, 0, p.r, 0, TAU); x.fill(); x.strokeStyle = "#8a5200"; x.lineWidth = 1.5; x.beginPath(); x.arc(0, 0, p.r * .7, 0, TAU); x.stroke(); } x.restore(); }
    if (amt && W.k === "sh") { const k = Math.min(1, u / (lv === 1 ? 900 : 1900)); amt.textContent = fmt(Math.round(W.n * (1 - Math.pow(1 - k, 3)))); }
    if (u > life) close(); };
  const close = () => { if (!el.isConnected) return; el.classList.add("out"); cancelAnimationFrame(raf); setTimeout(() => el.remove(), 420); };
  el.addEventListener("pointerdown", e => { if (performance.now() - t0 > 600) close(); }); raf = requestAnimationFrame(frame); }
/* the daily reminder: a band on the planet and, once a day, a word from her */
const WHL_NAG = ["Commander, your free spin on the Glyph Wheel is waiting in the Void Shop. Today could be the jackpot.", "The Glyph Wheel has a free spin for you today. Go on, pull the lever. I'll keep my fingers crossed.", "Don't forget your free spin, Commander. The wheel is glowing, just waiting for you."];
function wheelBand() { if (!whlFree() || !G.ready || G.mode === "demo") return ""; try { if (acadOn()) return ""; } catch (e) {}
  if (S.whlNag !== shopDay() && !G.whlNagT) G.whlNagT = setTimeout(() => { G.whlNagT = 0; try { if (view === "base" && !sheet && !battle && whlFree() && S.whlNag !== shopDay()) { const L = WHL_NAG[(Math.floor(now() / DAY)) % WHL_NAG.length]; advHolo(L); setTimeout(() => { try { const h = document.querySelector("#advh .hsay span"); if (h && h.textContent === L) S.whlNag = shopDay(); } catch (e) {} }, 500); } } catch (e) {} }, 6000); /* tried again every 6 s until she has actually said it (she may be busy with another line) */
  return `<button class="omb whb" data-act="whlGo"><b>🎰 FREE SPIN READY</b><span>Holo Glyph Wheel</span></button>`; }
