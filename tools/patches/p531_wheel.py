# v531 the Holo Glyph Wheel (owner: "For void shop remaster free gift with some kind of holo glyph lottery wheel, it should have a slot
# machine style handle for players to start the spin"). The free daily gift in the Void Shop is now a holographic wheel of eight
# glyph segments with a slot-machine lever beside it: drag the lever down (or tap it) to spin, once per UTC day. The odds are the old
# gift's: Void Shards 40% (1: 26%, 2: 12%, 3 jackpot: 2%), a Boost Pack ×5 30% (two segments), a Metal, Crystal or Gas crate 10% each.
# The day is used up when the lever is pulled; the prize is stored as S.wheelPend and paid when the wheel stops (or on the next shop
# open if the app was closed mid-spin).
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''/* v531 the Holo Glyph Wheel: the free daily gift, spun with a slot-machine lever */
const WHEEL = [{ k: "sh", n: 1, g: "ᚠ", l: "◆1", col: "#c88aff", w: 26 }, { k: "boost5", g: "ᛉ", l: "⚡×5", col: "#55d6e8", w: 15 }, { k: "crateM", g: "ᛗ", l: "Metal", col: "#b8c6d6", w: 10 }, { k: "sh", n: 2, g: "ᚱ", l: "◆2", col: "#c88aff", w: 12 },
  { k: "boost5", g: "ᛉ", l: "⚡×5", col: "#55d6e8", w: 15 }, { k: "crateC", g: "ᚲ", l: "Crystal", col: "#7af4ff", w: 10 }, { k: "sh", n: 3, g: "ᛟ", l: "◆3", col: "#ffcf5a", w: 2, jack: 1 }, { k: "crateG", g: "ᚷ", l: "Gas", col: "#5dff9a", w: 10 }];
const wheelName = W => W.k === "sh" ? `◆${W.n} Void Shard${W.n > 1 ? "s" : ""}` : SHOP[W.k].n;
function wheelHTML(T) { const can = (S.shopFree || "") !== shopDay() && S.wheelPend == null, spin = !!G.wheel, rot = G.wheelRot || 0, N = WHEEL.length, st = 360 / N;
  const cg = WHEEL.map((W, i) => `${W.col}${i % 2 ? "38" : "22"} ${i * st}deg ${(i + 1) * st}deg`).join(",");
  const segs = WHEEL.map((W, i) => `<div class="gws${G.wheelWin === i && !spin ? " win" : ""}" style="transform:rotate(${i * st + st / 2}deg);--c:${W.col}"><span><b>${W.g}</b><i>${W.l}</i></span></div>`).join("");
  const ticks = WHEEL.map((W, i) => `<div class="gwt" style="transform:rotate(${i * st}deg)"></div>`).join("");
  return `<div class="gwc${can ? " ready" : ""}${spin ? " spin" : ""}"><div class="gww"><div class="gwr"></div><div class="gw" id="gwheel" style="transform:rotate(${rot}deg);background:conic-gradient(${cg})">${ticks}${segs}</div><div class="gwh">◈</div><div class="gwp" id="gwptr"></div></div>
    <div class="gwx"><small>HOLO GLYPH WHEEL</small><b>${spin ? "Spinning…" : can ? "Free daily spin" : "Spun today"}</b><span>${spin ? "The glyphs are aligning." : can ? "Pull the lever to spin. Shards, speed-ups or a crate, every day." : `Next spin in <b data-end="${shopDayEnd()}">${ftime(shopDayEnd() - T)}</b>`}</span></div>
    <div class="gwl${can && !spin ? "" : " off"}" id="gwlever" role="button" tabindex="0" aria-label="Pull the lever to spin the wheel"><div class="gwl-slot"></div><div class="gwl-rod"></div><div class="gwl-knob"></div><div class="gwl-base"></div></div></div>`; }
function wheelPull() { if (G.wheel || (S.shopFree || "") === shopDay() || S.wheelPend != null) return;
  let r = Math.random() * WHEEL.reduce((a, W) => a + W.w, 0), idx = 0; for (let i = 0; i < WHEEL.length; i++) { r -= WHEEL[i].w; if (r < 0) { idx = i; break; } }
  const st = 360 / WHEEL.length, from = G.wheelRot || 0, aim = -(idx * st + st / 2) + (Math.random() - .5) * st * .6, to = from + 360 * 6 + (((aim - from) % 360) + 360) % 360;
  G.wheelWin = null; G.wheel = { from, to, t0: performance.now(), dur: 4800, idx, seg: -1 };
  act(() => { S.shopFree = shopDay(); S.wheelPend = idx; }); crumb("glyph wheel spun");
  requestAnimationFrame(wheelAnim); }
function wheelAnim() { const R = G.wheel; if (!R) return; const u = Math.min(1, (performance.now() - R.t0) / R.dur), e = 1 - Math.pow(1 - u, 4), rot = R.from + (R.to - R.from) * e; G.wheelRot = rot;
  const el = document.getElementById("gwheel"); if (el) el.style.transform = `rotate(${rot}deg)`;
  const seg = Math.floor(((rot % 360) + 360) % 360 / (360 / WHEEL.length)); if (seg !== R.seg) { R.seg = seg; try { SFX.click(); } catch (er) {} const p = document.getElementById("gwptr"); if (p) { p.classList.remove("tk"); void p.offsetWidth; p.classList.add("tk"); } }
  if (u < 1) return requestAnimationFrame(wheelAnim);
  G.wheel = null; G.wheelRot = rot % 360; G.wheelWin = R.idx; wheelGrant(); }
function wheelGrant() { if (S.wheelPend == null) return; const W = WHEEL[S.wheelPend]; if (!W) { S.wheelPend = null; return; }
  act(() => { S.wheelPend = null; if (W.k === "sh") S.shards = (S.shards || 0) + W.n; else giveItem(W.k); });
  toast(`${W.jack ? "JACKPOT! " : ""}Glyph Wheel: ${wheelName(W)}${W.k === "sh" ? "" : " added to your inventory"}. Spin again tomorrow.`, "win"); try { W.jack ? SFX.fanfare(true) : SFX.research(); } catch (e) {} }
/* the lever: drag the knob down past halfway (or tap it) to pull */
(() => { let D = null; const lev = () => document.getElementById("gwlever"), setP = p => { const L = lev(); if (L) L.style.setProperty("--p", p.toFixed(3)); };
  const release = pulled => { D = null; const L = lev(); if (L) { L.classList.add("back"); setP(pulled ? 1 : 0); setTimeout(() => { setP(0); setTimeout(() => { const L2 = lev(); if (L2) L2.classList.remove("back"); }, 420); }, pulled ? 160 : 0); } if (pulled) wheelPull(); };
  document.addEventListener("pointerdown", e => { const L = e.target && e.target.closest && e.target.closest("#gwlever"); if (!L || L.classList.contains("off")) return; e.preventDefault(); L.classList.remove("back"); const r = L.getBoundingClientRect(); D = { y0: e.clientY, h: r.height * .62, p: 0, moved: false }; });
  document.addEventListener("pointermove", e => { if (!D) return; const p = clamp((e.clientY - D.y0) / D.h, 0, 1); if (Math.abs(e.clientY - D.y0) > 6) D.moved = true; D.p = p; setP(p); }, { passive: true });
  document.addEventListener("pointerup", () => { if (!D) return; release(D.p > .55 || !D.moved); });
  document.addEventListener("pointercancel", () => { if (D) release(false); });
  document.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && document.activeElement === lev() && !lev().classList.contains("off")) { e.preventDefault(); release(true); } }); })();
'''
rep('function shShop() {', JS + 'function shShop() {')
rep('''<div class="shead"><button class="btn ${free ? "amber" : "ghost"} sm" data-act="shopFree" ${free ? "" : "disabled"}>${free ? "🎁 Free daily gift" : "✓ Gift claimed · back tomorrow"}</button>''',
    '''${S.wheelPend != null && !G.wheel ? (setTimeout(wheelGrant, 60), "") : ""}${cat !== "inv" ? wheelHTML(T) : ""}<div class="shead">''')
rep('  shopFree: () => act(() => { if ((S.shopFree || "") === shopDay()) return;', '  shopFree: () => wheelPull(), shopFreeOld: () => act(() => { if ((S.shopFree || "") === shopDay()) return;')
css = '''
/* v531 the Holo Glyph Wheel */
.gwc{position:relative;flex-shrink:0;display:grid;grid-template-columns:auto minmax(0,1fr) 46px;gap:12px;align-items:center;padding:12px 10px 12px 12px;border-radius:16px;overflow:hidden;border:1px solid rgba(122,244,255,.42);background:radial-gradient(circle at 18% 50%,rgba(122,244,255,.18),transparent 58%),radial-gradient(circle at 60% 120%,rgba(200,138,255,.18),transparent 60%),linear-gradient(125deg,#08182a,#0c0d24)}
.gwc::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(122,244,255,.06) 0 1px,transparent 1px 4px);pointer-events:none;animation:gwscan 6s linear infinite}@keyframes gwscan{to{background-position:0 40px}}
.gwc.ready{box-shadow:0 0 22px rgba(122,244,255,.28)}.gwc.ready .gwp{animation:gwbob 1.6s ease-in-out infinite}@keyframes gwbob{50%{transform:translateX(-50%) translateY(2px)}}
.gww{position:relative;width:148px;height:148px}
.gwr{position:absolute;inset:0;border-radius:50%;background:repeating-conic-gradient(rgba(122,244,255,.85) 0 1.2deg,transparent 1.2deg 7.5deg);-webkit-mask:radial-gradient(circle,transparent 66px,#000 67px,#000 71px,transparent 72px);mask:radial-gradient(circle,transparent 66px,#000 67px,#000 71px,transparent 72px);animation:gwring 30s linear infinite;filter:drop-shadow(0 0 4px rgba(122,244,255,.8))}@keyframes gwring{to{transform:rotate(360deg)}}
.gw{position:absolute;inset:9px;border-radius:50%;border:1.5px solid rgba(122,244,255,.75);box-shadow:inset 0 0 22px rgba(122,244,255,.35),0 0 18px rgba(122,244,255,.3);will-change:transform}
.gwt{position:absolute;left:50%;top:0;width:1px;height:50%;margin-left:-.5px;transform-origin:50% 100%;background:linear-gradient(rgba(122,244,255,.85),transparent 80%)}
.gws{position:absolute;left:50%;top:50%;width:0;height:0}.gws span{position:absolute;left:0;top:0;transform:translate(-50%,-49px);display:flex;flex-direction:column;align-items:center;gap:1px;color:var(--c);text-shadow:0 0 6px var(--c)}
.gws b{font-size:19px;line-height:1;font-weight:700}.gws i{font-style:normal;font-size:9px;letter-spacing:.04em;color:#e9f6ff;opacity:.9;white-space:nowrap}
.gws.win span{animation:gwwin 1s ease-in-out 3}@keyframes gwwin{50%{transform:translate(-50%,-49px) scale(1.35);filter:brightness(1.8)}}
.gwh{position:absolute;left:50%;top:50%;width:36px;height:36px;margin:-18px 0 0 -18px;border-radius:50%;display:grid;place-items:center;font-size:17px;color:#bff3fa;background:radial-gradient(circle,#123a52,#06121e 70%);border:1px solid rgba(122,244,255,.8);box-shadow:0 0 12px rgba(122,244,255,.6)}
.gwp{position:absolute;left:50%;top:-2px;transform:translateX(-50%);width:0;height:0;border-left:9px solid transparent;border-right:9px solid transparent;border-top:17px solid #ffcf5a;filter:drop-shadow(0 0 5px #ffcf5a)}.gwp.tk{animation:gwtk .12s ease-out}@keyframes gwtk{50%{transform:translateX(-50%) rotate(-14deg)}}
.gwx{position:relative;display:flex;flex-direction:column;gap:3px;min-width:0}.gwx small{font-size:10px;letter-spacing:.16em;color:#7af4ff}.gwx>b{font-size:16px}.gwx span{font-size:12px;color:var(--muted);line-height:1.35}
.gwl{--p:0;position:relative;width:46px;height:132px;touch-action:none;cursor:grab;-webkit-user-select:none;user-select:none}.gwl.off{opacity:.35;cursor:default;pointer-events:none}
.gwl-slot{position:absolute;left:50%;top:10px;bottom:22px;width:8px;margin-left:-4px;border-radius:4px;background:linear-gradient(90deg,#030a12,#132637,#030a12);box-shadow:inset 0 0 4px #000,0 0 6px rgba(122,244,255,.35)}
.gwl-base{position:absolute;left:4px;right:4px;bottom:0;height:28px;border-radius:9px;background:linear-gradient(180deg,#1e3a50,#0b1826);border:1px solid rgba(122,244,255,.5);box-shadow:0 0 10px rgba(122,244,255,.25)}
.gwl-rod{position:absolute;left:50%;width:6px;margin-left:-3px;border-radius:3px;background:linear-gradient(90deg,#8aa4b8,#eef6ff,#7d93a6);top:calc(14px + var(--p) * 74px);height:calc(100% - 36px - 14px - var(--p) * 74px)}
.gwl-knob{position:absolute;left:50%;top:calc(var(--p) * 74px);width:30px;height:30px;margin-left:-15px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 8%,#ff6ad5 22%,#b0157d 70%,#5a0840);box-shadow:0 0 14px #ff4fc6,0 3px 8px rgba(0,0,0,.5)}
.gwl.back .gwl-knob,.gwl.back .gwl-rod{transition:top .38s cubic-bezier(.3,1.6,.5,1),height .38s cubic-bezier(.3,1.6,.5,1)}
.gwc.ready .gwl-knob{animation:gwk 1.8s ease-in-out infinite}@keyframes gwk{50%{box-shadow:0 0 22px #ff4fc6,0 0 4px #fff,0 3px 8px rgba(0,0,0,.5)}}
@media (max-width:400px){.gww{width:124px;height:124px}.gwr{-webkit-mask:radial-gradient(circle,transparent 54px,#000 55px,#000 59px,transparent 60px);mask:radial-gradient(circle,transparent 54px,#000 55px,#000 59px,transparent 60px)}.gws span{transform:translate(-50%,-40px)}.gws b{font-size:16px}.gwc{gap:8px}}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
open(P, 'w', encoding='utf-8').write(s); print('ok')
