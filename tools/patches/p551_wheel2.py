# v551 the Holo Glyph Wheel, remastered (owner: "a really detailed animation of the inner rings of each wheel spinning in opposite
# direction of each other with a lot of different glowing runes and glyph symbols ... wider with everything else underneath").
# The wheel is now a full-width canvas with five rings, each turning against its neighbour: an outer band of Elder Futhark runes,
# the prize ring with chase lights, a violet ring of sigils, a gold ring of triangles and a hexagram core with a glowing gem. At rest
# they drift; when the lever is pulled they wind back, whip up to speed with the prize ring, throw sparks and blaze brighter, then
# crawl to a stop with a peg tick per notch. The win flashes its segment, bursts light from the pointer and lights the rays.
# The rings are drawn once into offscreen canvases (glow included) and only rotated per frame. One persistent canvas is moved into
# each re-render's slot, so a shop refresh never blanks it; the loop stops when the shop closes and idles while scrolled away.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def cut(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1; s = s[:i] + new + s[j:]

# 20 prizes (owner: "It should also have chance to win a lot more prizes"). Weights are relative; the jackpot sits beside ◆1 for near misses.
cut('const WHEEL = [', 'const wheelName', r"""const WHEEL = [{ k: "sh", n: 1, g: "ᚠ", l: "◆1", col: "#c88aff", w: 14 }, { k: "sh", n: 25, g: "ᛟ", l: "◆25", col: "#ffcf5a", w: .7, jack: 1 }, { k: "sh", n: 2, g: "ᚢ", l: "◆2", col: "#c88aff", w: 10 },
  { k: "crateM", g: "ᛗ", l: "🔩", col: "#b8c6d6", w: 8 }, { k: "xf_bronze", g: "ᚱ", l: "🚀", col: "#ff8a3a", w: 8 }, { k: "sh", n: 5, g: "ᛊ", l: "◆5", col: "#d9a0ff", w: 5 }, { k: "xb_bronze", g: "ᛒ", l: "🏗", col: "#ffb35a", w: 7 },
  { k: "crateC", g: "ᚲ", l: "💎", col: "#7af4ff", w: 7 }, { k: "vipAct1", g: "ᛇ", l: "👑1d", col: "#ffd66a", w: 1.5 }, { k: "boost5", g: "ᛉ", l: "⚡5", col: "#55d6e8", w: 7 }, { k: "vipPts100", g: "ᚹ", l: "👑+", col: "#ffe08a", w: 5 },
  { k: "crateG", g: "ᚷ", l: "🧪", col: "#5dff9a", w: 6 }, { k: "sh", n: 10, g: "ᛞ", l: "◆10", col: "#ffb0f0", w: 1.5 }, { k: "xr_bronze", g: "ᛁ", l: "🔬", col: "#9a7bff", w: 5 }, { k: "mb1", g: "ᛜ", l: "🧰", col: "#c8d4e0", w: 4 },
  { k: "bm_bronze", g: "ᛏ", l: "⛏", col: "#d0dbe6", w: 3 }, { k: "pAll_gold", g: "ᛚ", l: "📦", col: "#ffcf5a", w: .8 }, { k: "bf_bronze", g: "ᚦ", l: "🛸", col: "#5a9aff", w: 3 }, { k: "xs_bronze", g: "ᚾ", l: "🛠", col: "#55e0c0", w: 3 },
  { k: "mb2", g: "ᛃ", l: "🧰+", col: "#5dff9a", w: 1.5 }];
""")
rep('const wheelName = W => W.k === "sh" ? `◆${W.n} Void Shard${W.n > 1 ? "s" : ""}` : SHOP[W.k].n;', 'const wheelName = W => W.k === "sh" ? `◆${W.n} Void Shard${W.n > 1 ? "s" : ""}` : SHOP[W.k].n + ((W.k.match(/_(bronze|silver|gold)$/) || [])[1] ? " · " + W.k.match(/_(bronze|silver|gold)$/)[1].replace(/^./, c => c.toUpperCase()) : "");')
JS = r'''/* v551 the remastered Holo Glyph Wheel: five counter-rotating rune rings on one canvas */
const WHL_RUNES = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ", WHL_SIG = "⊕⊗⊛⊙⌬⍟△▽◇⬡⟁⟐⨀⌖☉☽✶✷";
function whlCv(px, fn) { const c = document.createElement("canvas"); c.width = c.height = px; const x = c.getContext("2d"); x.translate(px / 2, px / 2); x.textAlign = "center"; x.textBaseline = "middle"; fn(x, px / 2); return c; }
function whlBuild(px) { const glow = (x, col, b) => { x.shadowColor = col; x.shadowBlur = b; }, N = WHEEL.length, st = TAU / N, ring = (x, R, a, b) => { x.beginPath(); x.arc(0, 0, R * a, 0, TAU); x.arc(0, 0, R * b, 0, TAU, true); x.fill(); };
  const bg = whlCv(px, (x, R) => { const g = x.createRadialGradient(0, 0, 0, 0, 0, R); g.addColorStop(0, "#22145a"); g.addColorStop(.55, "#0a1534"); g.addColorStop(1, "rgba(4,8,18,0)"); x.fillStyle = g; x.beginPath(); x.arc(0, 0, R, 0, TAU); x.fill();
    for (let i = 0; i < 90; i++) { const a = Math.random() * TAU, r = Math.sqrt(Math.random()) * R * .97, z = R * (.003 + Math.random() * .006); x.fillStyle = `rgba(210,235,255,${(.15 + Math.random() * .55).toFixed(2)})`; x.beginPath(); x.arc(Math.cos(a) * r, Math.sin(a) * r, z, 0, TAU); x.fill(); } });
  const outer = whlCv(px, (x, R) => { x.fillStyle = "rgba(8,28,48,.7)"; ring(x, R, .985, .9); x.lineWidth = R * .006; glow(x, "#7af4ff", R * .03); x.strokeStyle = "rgba(122,244,255,.95)"; for (const r of [.9, .985]) { x.beginPath(); x.arc(0, 0, R * r, 0, TAU); x.stroke(); }
    x.font = `700 ${R * .064}px serif`; const n = 36; for (let i = 0; i < n; i++) { x.save(); x.rotate(i / n * TAU); x.translate(0, -R * .9425); if (i % 3) { x.fillStyle = i % 3 === 1 ? "#c8fbff" : "#9fe9ff"; glow(x, "#55d6e8", R * .045); x.fillText(WHL_RUNES[(i * 7) % WHL_RUNES.length], 0, 0); } else { x.fillStyle = "#ffe7a0"; glow(x, "#ffcf5a", R * .03); x.beginPath(); x.moveTo(0, -R * .016); x.lineTo(R * .011, 0); x.lineTo(0, R * .016); x.lineTo(-R * .011, 0); x.fill(); } x.restore(); } });
  const prize = whlCv(px, (x, R) => { for (let i = 0; i < N; i++) { const W = WHEEL[i], a0 = -Math.PI / 2 + i * st, a1 = a0 + st, g = x.createRadialGradient(0, 0, R * .5, 0, 0, R * .86);
      g.addColorStop(0, W.col + "14"); g.addColorStop(.65, W.col + (i % 2 ? "50" : "34")); g.addColorStop(1, W.col + "90"); x.fillStyle = g; x.beginPath(); x.arc(0, 0, R * .86, a0, a1); x.arc(0, 0, R * .5, a1, a0, true); x.closePath(); x.fill(); }
    x.lineWidth = R * .008; glow(x, "#ffe7a0", R * .035); x.strokeStyle = "rgba(255,222,150,.95)"; for (const r of [.5, .86]) { x.beginPath(); x.arc(0, 0, R * r, 0, TAU); x.stroke(); }
    x.lineWidth = R * .005; x.strokeStyle = "rgba(255,232,180,.8)"; for (let i = 0; i < N; i++) { const a = -Math.PI / 2 + i * st; x.beginPath(); x.moveTo(Math.cos(a) * R * .5, Math.sin(a) * R * .5); x.lineTo(Math.cos(a) * R * .86, Math.sin(a) * R * .86); x.stroke(); }
    for (let i = 0; i < N; i++) { const W = WHEEL[i]; x.save(); x.rotate(i * st + st / 2); x.fillStyle = W.col; glow(x, W.col, R * .07); x.font = `700 ${R * .105}px serif`; x.fillText(W.g, 0, -R * .78); x.fillStyle = "#ffffff"; glow(x, W.col, R * .025); x.font = `700 ${R * .105}px serif`; x.globalAlpha = .35; x.fillText(W.g, 0, -R * .78); x.globalAlpha = 1;
      x.font = `800 ${R * .058}px Rajdhani, system-ui, sans-serif`; x.fillStyle = "#f4fbff"; glow(x, W.col, R * .03); x.fillText(W.l, 0, -R * .645); if (W.jack) { x.font = `800 ${R * .028}px Rajdhani, system-ui, sans-serif`; x.fillStyle = "#ffcf5a"; glow(x, "#ffcf5a", R * .03); x.fillText("JACKPOT", 0, -R * .56); } x.restore(); } });
  const ringB = whlCv(px, (x, R) => { x.fillStyle = "rgba(46,12,72,.62)"; ring(x, R, .48, .38); glow(x, "#c88aff", R * .03); x.strokeStyle = "rgba(210,150,255,.9)"; x.lineWidth = R * .005; for (const r of [.38, .48]) { x.beginPath(); x.arc(0, 0, R * r, 0, TAU); x.stroke(); }
    x.setLineDash([R * .008, R * .02]); x.lineWidth = R * .004; x.beginPath(); x.arc(0, 0, R * .468, 0, TAU); x.stroke(); x.beginPath(); x.arc(0, 0, R * .392, 0, TAU); x.stroke(); x.setLineDash([]);
    x.font = `700 ${R * .052}px "Apple Symbols","Segoe UI Symbol","Noto Sans Symbols 2","DejaVu Sans",serif`; const n = 18; for (let i = 0; i < n; i++) { x.save(); x.rotate(i / n * TAU); x.fillStyle = i % 3 ? "#ecd4ff" : "#ff9ae6"; glow(x, i % 3 ? "#c88aff" : "#ff4fc6", R * .04); x.fillText(WHL_SIG[i % WHL_SIG.length], 0, -R * .43); x.restore(); } });
  const ringC = whlCv(px, (x, R) => { glow(x, "#ffcf5a", R * .03); x.strokeStyle = "rgba(255,207,90,.9)"; x.lineWidth = R * .005; for (const r of [.29, .355]) { x.beginPath(); x.arc(0, 0, R * r, 0, TAU); x.stroke(); }
    x.fillStyle = "#ffe7a0"; for (let i = 0; i < 12; i++) { x.save(); x.rotate(i / 12 * TAU); x.beginPath(); x.moveTo(0, -R * .346); x.lineTo(R * .019, -R * .31); x.lineTo(-R * .019, -R * .31); x.closePath(); x.stroke(); x.beginPath(); x.arc(0, -R * .298, R * .0055, 0, TAU); x.fill(); x.restore(); }
    x.lineWidth = R * .0035; for (let k = 0; k < 6; k++) { x.beginPath(); x.arc(0, 0, R * .322, k / 6 * TAU + .12, k / 6 * TAU + .78); x.stroke(); } });
  const core = whlCv(px, (x, R) => { glow(x, "#7af4ff", R * .04); x.strokeStyle = "rgba(150,248,255,.95)"; x.lineWidth = R * .006; const tri = o => { x.beginPath(); for (let k = 0; k < 3; k++) { const a = o + k / 3 * TAU, X = Math.cos(a) * R * .24, Y = Math.sin(a) * R * .24; k ? x.lineTo(X, Y) : x.moveTo(X, Y); } x.closePath(); x.stroke(); };
    tri(-Math.PI / 2); tri(Math.PI / 2); for (const r of [.24, .125]) { x.beginPath(); x.arc(0, 0, R * r, 0, TAU); x.stroke(); }
    x.font = `700 ${R * .04}px serif`; x.fillStyle = "#c8fbff"; for (let k = 0; k < 6; k++) { x.save(); x.rotate(k / 6 * TAU + Math.PI / 6); x.fillText(WHL_RUNES[k * 4], 0, -R * .185); x.restore(); } });
  return { px, bg, outer, prize, ringB, ringC, core }; }
function whlStart() { if (G.whlRaf || !document.getElementById("gwslot")) return; G.whlLast = 0; G.whlRaf = requestAnimationFrame(whlFrame); }
function whlFrame(t) { const slot = document.getElementById("gwslot"); if (!slot) { G.whlRaf = 0; return; } G.whlRaf = requestAnimationFrame(whlFrame);
  let cv = G.whlCv; if (!cv) { cv = G.whlCv = document.createElement("canvas"); cv.setAttribute("aria-hidden", "true"); } if (cv.parentNode !== slot) { slot.textContent = ""; slot.appendChild(cv); }
  const bx = slot.getBoundingClientRect(); if (!bx.width || bx.bottom < 0 || bx.top > innerHeight || document.hidden) { G.whlLast = t; return; }
  const px = Math.round(bx.width * Math.min(devicePixelRatio || 1, IOS ? 1.5 : 2)); if (cv.width !== px) cv.width = cv.height = px; if (!G.whlOff || G.whlOff.px !== px) G.whlOff = whlBuild(px);
  const O = G.whlOff, x = cv.getContext("2d"), R = px / 2, dt = G.whlLast ? Math.min(.05, (t - G.whlLast) / 1000) : 0; G.whlLast = t;
  const A = G.whlA = G.whlA || { o: 0, b: 0, c: 0, k: 0, prev: G.wheelRot || 0, v: 0, tick: 0, parts: [] }, rot = G.wheelRot || 0;
  if (dt) { A.v += ((Math.abs(rot - A.prev) / dt) - A.v) * .35; } A.prev = rot; const sp = A.v, T = t / 1000, heat = Math.min(1, sp / 650), win = G.whlWinT ? Math.max(0, 1 - (t - G.whlWinT) / 2800) : 0, pulse = .5 + .5 * Math.sin(T * 2.3);
  A.o -= (5 + sp * .3) * dt; A.b -= (16 + sp * .95) * dt; A.c += (10 + sp * .6) * dt; A.k -= (22 + sp * 1.25) * dt; A.tick = Math.max(0, A.tick - dt * 7);
  const rotd = (img, deg, a) => { x.save(); x.translate(R, R); x.rotate(deg * Math.PI / 180); x.globalAlpha *= a; x.drawImage(img, -R, -R); x.restore(); };
  x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = "source-over"; x.globalAlpha = 1; x.clearRect(0, 0, px, px);
  rotd(O.bg, T * 3, 1); rotd(O.outer, A.o, .78 + .22 * pulse); rotd(O.prize, rot, 1);
  x.save(); x.translate(R, R); x.rotate(rot * Math.PI / 180); x.globalCompositeOperation = "lighter"; const nb = 40, ch = Math.floor(T * (sp > 60 ? 22 : 7));
  for (let i = 0; i < nb; i++) { const on = win ? (Math.floor(T * 12) + i) % 2 === 0 : sp > 60 ? (i + ch) % 3 !== 0 : (i + ch) % 4 === 0, a = i / nb * TAU, X = Math.sin(a) * R * .878, Y = -Math.cos(a) * R * .878, rr = R * (on ? .034 : .02), g = x.createRadialGradient(X, Y, 0, X, Y, rr), c = on ? "255,236,170" : "140,170,200";
    g.addColorStop(0, `rgba(${c},${on ? 1 : .55})`); g.addColorStop(.35, `rgba(${c},${on ? .55 : .2})`); g.addColorStop(1, `rgba(${c},0)`); x.fillStyle = g; x.beginPath(); x.arc(X, Y, rr, 0, TAU); x.fill(); }
  if (G.wheelWin != null && !G.wheel) { const W = WHEEL[G.wheelWin], s2 = TAU / WHEEL.length, a0 = -Math.PI / 2 + G.wheelWin * s2; x.globalAlpha = win ? .25 + .4 * (.5 + .5 * Math.sin(T * 16)) : .12 + .12 * pulse; x.fillStyle = W.col; x.beginPath(); x.arc(0, 0, R * .86, a0, a0 + s2); x.arc(0, 0, R * .5, a0 + s2, a0, true); x.closePath(); x.fill(); }
  x.restore();
  rotd(O.ringB, A.b, .78 + .22 * pulse); rotd(O.ringC, A.c, .85); rotd(O.core, A.k, .85 + .15 * pulse);
  const hot = Math.max(heat, win); if (hot > .04) { x.save(); x.globalCompositeOperation = "lighter"; rotd(O.outer, A.o, hot * .55); rotd(O.ringB, A.b, hot * .75); rotd(O.ringC, A.c, hot * .6); rotd(O.core, A.k, hot * .5); x.restore(); }
  x.save(); x.translate(R, R); x.globalCompositeOperation = "lighter";
  if (win) { x.save(); x.rotate(T * .9); for (let i = 0; i < 14; i++) { x.rotate(TAU / 14); const g = x.createLinearGradient(0, 0, 0, -R); g.addColorStop(0, `rgba(255,236,170,${(.4 * win).toFixed(3)})`); g.addColorStop(1, "rgba(255,236,170,0)"); x.fillStyle = g; x.beginPath(); x.moveTo(0, 0); x.lineTo(R * .045, -R); x.lineTo(-R * .045, -R); x.fill(); } x.restore(); }
  const gr = R * (.085 + .015 * pulse + .035 * heat + .06 * win), cc = G.wheelWin != null && !G.wheel ? WHEEL[G.wheelWin].col : "#7af4ff", gg = x.createRadialGradient(0, 0, 0, 0, 0, gr * 2.4); gg.addColorStop(0, "#ffffff"); gg.addColorStop(.22, cc); gg.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = gg; x.beginPath(); x.arc(0, 0, gr * 2.4, 0, TAU); x.fill(); x.restore();
  const Pt = A.parts; if (G.whlBurst != null) { const W = WHEEL[G.whlBurst]; G.whlBurst = null; for (let i = 0; i < (W.jack ? 160 : 90); i++) { const a = Math.random() * TAU, v = R * (.4 + Math.random() * 1.4); Pt.push({ x: R, y: R * .3, vx: Math.cos(a) * v, vy: Math.sin(a) * v - R * .3, l: .8 + Math.random() * 1.1, m: 0, c: Math.random() < .35 ? "#ffe7a0" : W.col, z: R * (.007 + Math.random() * .012), g: 1 }); } }
  if (sp > 140 && Pt.length < 170) { const n = Math.min(5, Math.ceil(sp / 500)); for (let i = 0; i < n; i++) { const a = Math.random() * TAU, W = WHEEL[(Math.random() * WHEEL.length) | 0], f = R * (.5 + Math.random() * .9) * Math.min(1.6, sp / 900 + .4); Pt.push({ x: R + Math.cos(a) * R * .87, y: R + Math.sin(a) * R * .87, vx: (-Math.sin(a) * .75 + Math.cos(a) * .35) * f, vy: (Math.cos(a) * .75 + Math.sin(a) * .35) * f, l: .35 + Math.random() * .5, m: 0, c: W.col, z: R * (.005 + Math.random() * .008), g: 0 }); } }
  x.save(); x.globalCompositeOperation = "lighter"; for (let i = Pt.length - 1; i >= 0; i--) { const p = Pt[i]; p.m += dt; if (p.m > p.l) { Pt.splice(i, 1); continue; } p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= .97; p.vy = p.vy * .97 + R * .9 * dt * p.g; const a = 1 - p.m / p.l; x.globalAlpha = a; x.fillStyle = p.c; x.beginPath(); x.arc(p.x, p.y, p.z * (.5 + a), 0, TAU); x.fill(); } x.restore();
  x.save(); x.translate(R, R * .03); x.rotate(-A.tick * .5); x.shadowColor = "#ffcf5a"; x.shadowBlur = R * .05; const pg = x.createLinearGradient(0, 0, 0, R * .15); pg.addColorStop(0, "#fff6d0"); pg.addColorStop(1, "#e0981f"); x.fillStyle = pg; x.beginPath(); x.moveTo(-R * .06, 0); x.quadraticCurveTo(0, -R * .02, R * .06, 0); x.lineTo(0, R * .155); x.closePath(); x.fill(); x.shadowBlur = 0; x.fillStyle = "#fff"; x.beginPath(); x.arc(0, R * .03, R * .014, 0, TAU); x.fill(); x.restore(); }
function wheelHTML(T) { const can = (S.shopFree || "") !== shopDay() && S.wheelPend == null, spin = !!G.wheel, won = !spin && G.wheelWin != null ? WHEEL[G.wheelWin] : null; setTimeout(whlStart, 0);
  const chips = [...new Map(WHEEL.map(W => [W.l, W])).values()].map(W => `<span class="gwchip${W.jack ? " jack" : ""}${won && won.l === W.l ? " won" : ""}" style="--c:${W.col}"><b>${W.g}</b>${esc(wheelName(W))}${W.jack ? " · jackpot" : ""}</span>`).join("");
  return `<div class="gwz${can ? " ready" : ""}${spin ? " spin" : ""}"><div class="gwtop"><div class="gwstage"><div class="gwslot" id="gwslot"></div></div>
    <div class="gwl${can && !spin ? "" : " off"}" id="gwlever" role="button" tabindex="0" aria-label="Pull the lever to spin the wheel"><div class="gwl-slot"></div><div class="gwl-rod"></div><div class="gwl-knob"></div><div class="gwl-base"></div></div></div>
    <div class="gwx"><small>HOLO GLYPH WHEEL</small><b>${spin ? "The glyphs are aligning…" : won ? `${won.jack ? "JACKPOT! " : ""}You won ${esc(wheelName(won))}` : can ? "Free daily spin" : "Spun today"}</b><span>${spin ? `Landing on: <b id="gwnow">…</b>` : can ? `Pull the lever to spin the rings. One free spin every day, ${WHEEL.length} prizes.` : `Next spin in <b data-end="${shopDayEnd()}">${ftime(shopDayEnd() - T)}</b>`}</span><div class="gwchips">${chips}</div></div></div>`; }
'''
cut('function wheelHTML(T) {', 'function wheelPull() {', JS)
rep('G.wheel = { from, to, t0: performance.now(), dur: 4800, idx, seg: -1 };', 'G.wheel = { from, to, t0: performance.now(), dur: 6400, idx, peg: null }; G.wheelWin = null; G.whlWinT = 0; whlStart();')
cut('function wheelAnim() {', 'function wheelGrant() {', r'''function wheelAnim() { const R = G.wheel; if (!R) return; const u = Math.min(1, (performance.now() - R.t0) / R.dur), back = 18; let rot; /* v551 wind back, whip, crawl */
  if (u < .07) rot = R.from - back * Math.sin(u / .07 * Math.PI / 2); else { const v = (u - .07) / .93; rot = R.from - back + (R.to - R.from + back) * (1 - Math.pow(1 - v, 4.4)); }
  G.wheelRot = rot; const peg = Math.floor(rot / (360 / WHEEL.length)), cur = Math.floor((((-rot) % 360) + 360) % 360 / (360 / WHEEL.length)); if (cur !== R.cur) { R.cur = cur; const el = document.getElementById("gwnow"); if (el) { el.textContent = wheelName(WHEEL[cur]); el.style.color = WHEEL[cur].col; } } if (peg !== R.peg) { if (R.peg != null) { const n = performance.now(); if (n - (R.ck || 0) > 42) { R.ck = n; try { SFX.click(); } catch (er) {} } if (G.whlA) G.whlA.tick = 1; } R.peg = peg; }
  if (u < 1) return requestAnimationFrame(wheelAnim);
  G.wheel = null; G.wheelRot = rot % 360; if (G.whlA) G.whlA.prev = G.wheelRot; G.wheelWin = R.idx; G.whlWinT = performance.now(); G.whlBurst = R.idx; wheelGrant(); }
''')
css = '''
/* v551 the remastered glyph wheel */
.gwz{position:relative;flex-shrink:0;display:flex;flex-direction:column;gap:8px;padding:12px 10px 14px;border-radius:18px;overflow:hidden;border:1px solid rgba(122,244,255,.45);background:radial-gradient(75% 55% at 45% 34%,rgba(122,96,255,.24),transparent 72%),radial-gradient(circle at 50% 112%,rgba(255,79,198,.18),transparent 60%),linear-gradient(160deg,#07142a,#0c0a24)}
.gwz::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(122,244,255,.05) 0 1px,transparent 1px 4px);pointer-events:none;animation:gwscan 6s linear infinite}
.gwz.ready{box-shadow:0 0 28px rgba(122,244,255,.3),inset 0 0 30px rgba(122,96,255,.18)}.gwz.ready .gwl-knob{animation:gwk 1.8s ease-in-out infinite}
.gwtop{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 46px;gap:4px;align-items:center}
.gwstage{width:100%;max-width:480px;justify-self:center}.gwslot{width:100%;aspect-ratio:1/1}.gwslot canvas{display:block;width:100%;height:100%}
.gwz .gwx{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:3px}.gwz .gwx>b{font-size:19px;letter-spacing:.02em}.gwz.spin .gwx>b{color:#7af4ff;text-shadow:0 0 12px rgba(122,244,255,.7)}
.gwchips{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;margin-top:6px}
.gwchip{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;font-size:10.5px;color:#e9f6ff;border:1px solid color-mix(in srgb,var(--c) 55%,transparent);background:color-mix(in srgb,var(--c) 12%,rgba(6,12,24,.85))}
.gwchip b{color:var(--c);text-shadow:0 0 6px var(--c);font-size:12.5px;font-weight:700}.gwchip.jack{border-color:#ffcf5a;box-shadow:0 0 10px rgba(255,207,90,.35)}.gwchip.won{background:color-mix(in srgb,var(--c) 32%,rgba(6,12,24,.85));box-shadow:0 0 14px color-mix(in srgb,var(--c) 60%,transparent)}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 550\b", "GAME_V = 551", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
