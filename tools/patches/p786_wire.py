"""v786: the Sanctuary in 3D, part one (owner: "make a small monster pop out of the egg when it's hatched, and in the menu they could
be a small 3D version of them ... how can we make it more visually engaging and addictive?" then "build it all").
- Live 3D creatures in the Sanctuary lists: every species with a 3D model turns slowly in its card, swimming with its own body wave,
  drawn once per species into a turntable strip (one small renderer, then plain images, so a long list costs nothing). Hatchlings are
  small, Juveniles bigger, Adults fill the frame; Prismatic creatures shimmer through every colour.
- 3D hatching: when the egg bursts, the baby itself pops out (a bouncy rise, a shake to dry off, then it turns and swims), instead of
  the painting in a circle. Epic and rarer hatches get a gold flare.
- Feeding: the creature grows on screen from its old size to its new one, with a burst of light and "grew into a Juvenile/Adult!".
- Care streak: feeding a creature or warming an egg once a day builds a streak shown on the Sanctuary page; every 7th day in a row
  pays 10 Void Shards (a miss resets it).
- Egg alerts: once an egg is nine-tenths of the way to hatching it wobbles in its incubator, and you are told once that something is
  moving inside it.
Applies on top of v785."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 785;", "const GAME_V = 786;")
CSS = r'''
/* v786 3D creatures in the Sanctuary */
.xsart{position:relative;background:radial-gradient(circle at 50% 58%,color-mix(in srgb,var(--c) 30%,#040a10),#040a10 72%)}
.xsspin{position:absolute;inset:0;display:none;background-size:2400% 100%;background-repeat:no-repeat;background-position:0 0;animation:xsspin 4.8s steps(24) infinite;pointer-events:none;transform-origin:50% 60%}
@keyframes xsspin{to{background-position-x:104.3478%}}
@keyframes xshue{to{filter:hue-rotate(360deg) saturate(1.4)}}
.xscr.g0 .xsspin{transform:scale(.66)}.xscr.g1 .xsspin{transform:scale(.83)}
.xscr.pr .xsspin{animation:xsspin 4.8s steps(24) infinite,xshue 6s linear infinite}
.xshatch .xsbaby{position:absolute;width:200px;height:200px;left:50%;top:50%;margin:-100px 0 0 -100px;opacity:0;transform:scale(.08) translateY(30px)}
.xsfx.burst .xshatch .xsbaby{animation:xsspin 4.2s steps(24) 1.6s infinite,xsbabypop 1s cubic-bezier(.2,1.6,.4,1) .05s forwards,xsbabyshake .45s ease-in-out 1.1s 2}
@keyframes xsbabypop{0%{opacity:0;transform:scale(.08) translateY(30px)}60%{opacity:1;transform:scale(1.15) translateY(-14px)}100%{opacity:1;transform:scale(1) translateY(0)}}
@keyframes xsbabyshake{0%,100%{rotate:0deg}25%{rotate:-10deg}75%{rotate:10deg}}
.xsfx.burst .xshatch .xsegg{transition:opacity .3s,transform .3s;opacity:0!important;transform:scale(1.5)!important}
#xsgrow .xsgs{overflow:hidden}
.xsfx.hatch.rg .xsrays{filter:sepia(1) saturate(4) hue-rotate(-8deg) brightness(1.2)}
.xsfx.hatch.rg.burst::after{content:"";position:fixed;inset:0;pointer-events:none;background:radial-gradient(circle at 50% 42%,rgba(255,214,110,.55),rgba(255,180,60,.12) 35%,transparent 60%);animation:xsgold 1.6s ease-out forwards}
@keyframes xsgold{from{opacity:1}to{opacity:0}}
#xsgrow{position:fixed;inset:0;z-index:9000;display:grid;place-items:center;background:rgba(2,6,10,.72);backdrop-filter:blur(3px);opacity:0;transition:opacity .25s}
#xsgrow.on{opacity:1}
#xsgrow .xsgb{display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
#xsgrow .xsgs{position:relative;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 50% 58%,color-mix(in srgb,var(--c) 35%,#040a10),#040a10 70%);box-shadow:0 0 0 2px var(--c),0 0 60px color-mix(in srgb,var(--c) 60%,transparent)}
#xsgrow .xsspin,#xsgrow img{display:block;transform:scale(var(--s0));animation:xsspin 4.8s steps(24) infinite,xsgrowk 1.4s cubic-bezier(.3,1.6,.4,1) .5s forwards}
#xsgrow img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:50%;animation:xsgrowk 1.4s cubic-bezier(.3,1.6,.4,1) .5s forwards}
#xsgrow .xsgs::after{content:"";position:absolute;inset:-30px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.9),color-mix(in srgb,var(--c) 70%,transparent) 30%,transparent 62%);opacity:0;animation:xsgflash .9s ease-out .9s forwards}
@keyframes xsgrowk{to{transform:scale(var(--s1))}}
@keyframes xsgflash{0%{opacity:0;transform:scale(.4)}30%{opacity:1}100%{opacity:0;transform:scale(1.5)}}
#xsgrow b{font-size:20px}#xsgrow small{opacity:.8}
.xsinc.near .xsegg{animation:xswob 1.3s ease-in-out infinite}
@keyframes xswob{0%,100%{rotate:0deg}20%{rotate:-7deg}40%{rotate:6deg}55%{rotate:-3deg}70%{rotate:0deg}}
.xsstreak{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;border:1px solid rgba(255,170,80,.5);background:rgba(255,120,40,.12);font-size:12px}
'''
rep("@keyframes xsrise{to{opacity:1;transform:scale(1)}}", "@keyframes xsrise{to{opacity:1;transform:scale(1)}}" + CSS)
JS = r'''/* v786 3D creatures for the Sanctuary: one small renderer draws each species once into a 24-frame turntable strip (it swims with its
   own body wave as it turns); the cards, the hatch and the feeding show it as a plain animated image */
const XS_STRIP = {}, XS_SQ = []; let XS_SQT = 0;
function xsStrip(sp) { if (!TH || !XS_HAS3D.has(sp)) return null; if (XS_STRIP[sp] != null) return XS_STRIP[sp] || null; if (MON_SC[sp] && !MON_GEO[sp]) { monSculptLoad(sp); return null; }
  try { const N = 24, F = 144, R = xsStrip.R || (xsStrip.R = (() => { const cv = document.createElement("canvas"); cv.width = F; cv.height = F; const rd = glNew({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true }); rd.outputEncoding = TH.sRGBEncoding; rd.toneMapping = TH.ACESFilmicToneMapping; rd.setClearColor(0, 0);
      const sc = new TH.Scene(); sc.add(new TH.AmbientLight(0x6f7a9a, .6)); const d0 = new TH.DirectionalLight(0xfff0e6, 2.2); d0.position.set(-4, 6, 8); sc.add(d0); const d1 = new TH.DirectionalLight(0x60c8ff, 1.1); d1.position.set(6, 2, -6); sc.add(d1); let env = null; try { env = wbEnv(rd); } catch (e) {} return { cv, rd, sc, env, cam: new TH.PerspectiveCamera(30, 1, .05, 500) }; })());
    const U = { value: 0 }, M = mergeGroup(buildMonster(sp)); monAnimate(M, sp, U); if (R.env) M.traverse(o => { if (o.material && o.material.isMeshStandardMaterial) { o.material.envMap = R.env; o.material.needsUpdate = true; } });
    const box = new TH.Box3().setFromObject(M), c = box.getCenter(new TH.Vector3()), r = Math.max(.01, box.getSize(new TH.Vector3()).length() * .5); M.position.sub(c); const piv = new TH.Group(); piv.add(M); R.sc.add(piv); R.cam.position.set(0, r * .45, r * 1.85); R.cam.lookAt(0, 0, 0);
    const out = document.createElement("canvas"); out.width = F * N; out.height = F; const x = out.getContext("2d");
    for (let i = 0; i < N; i++) { piv.rotation.y = -.6 + i / N * TAU; U.value = i / N * 3; R.rd.render(R.sc, R.cam); x.drawImage(R.cv, i * F, 0); } R.sc.remove(piv);
    const url = out.toDataURL("image/png"), st = document.createElement("style"); XS_STRIP[sp] = url;
    st.textContent = `.xsspin[data-sp="${sp}"]{background-image:url(${url});display:block}.xsart[data-sp="${sp}"]>img,.xshatch[data-sp="${sp}"]>img,.xsgs[data-sp="${sp}"]>img{display:none!important}`; document.head.appendChild(st); return url; }
  catch (e) { console.warn("xs strip", e); XS_STRIP[sp] = ""; return null; } }
function xsStripQueue(list) { for (const sp of list) if (XS_HAS3D.has(sp) && XS_STRIP[sp] == null && !XS_SQ.includes(sp)) XS_SQ.push(sp); if (XS_SQT) return;
  const step = (tries = 0) => { XS_SQT = 0; const sp = XS_SQ[0]; if (!sp) return; const u = xsStrip(sp); if (u != null || XS_STRIP[sp] != null || tries > 40) { XS_SQ.shift(); tries = 0; } else tries++; if (XS_SQ.length) XS_SQT = setTimeout(() => step(tries), u == null ? 400 : 90); }; XS_SQT = setTimeout(step, 60); }
/* feeding: it grows on screen */
function xsGrowFx(c, g0) { try { const el = document.createElement("div"), sc = [.6, .76, .92], sp = c.sp; xsStrip(sp); el.id = "xsgrow"; el.style.setProperty("--c", xsCol(sp)); el.style.setProperty("--s0", sc[g0]); el.style.setProperty("--s1", sc[c.g || 0]);
    el.innerHTML = `<div class="xsgb"><div class="xsgs" data-sp="${sp}"><img src="${xsImg(sp)}" alt=""><i class="xsspin" data-sp="${sp}"></i></div><b>${esc(xsName(sp))} grew into ${c.g === 2 ? "an" : "a"} ${XS_GROW[c.g][0]}!</b><small>Its bonus is now +${xsCrPct(c)}%</small><button class="btn amber">Wonderful</button></div>`;
    const old = document.getElementById("xsgrow"); if (old) old.remove(); document.body.appendChild(el); requestAnimationFrame(() => el.classList.add("on")); try { setTimeout(() => SFX.blast && SFX.blast(1.1, 0), 900); } catch (e) {}
    const close = () => { el.classList.remove("on"); setTimeout(() => el.remove(), 260); }; el.addEventListener("click", close); setTimeout(close, 4200); } catch (e) {} }
/* the care streak: feed a creature or warm an egg once a day */
function xsCare() { const d = Math.floor(now() / 864e5), st = S.xsSt || (S.xsSt = { d: 0, n: 0 }); if (st.d === d) return; st.n = st.d === d - 1 ? st.n + 1 : 1; st.d = d; dirty();
  if (st.n % 7 === 0) { S.shards = (S.shards || 0) + 10; toast(`🔥 ${st.n}-day care streak! +10 Void Shards.`, "win"); } else if (st.n > 1) toast(`🔥 Care streak: ${st.n} days.`); }
const xsStreakN = () => { const st = S && S.xsSt, d = Math.floor(now() / 864e5); return st && st.d >= d - 1 ? st.n : 0; };
/* eggs about to hatch: they wobble, and you are told once */
setInterval(() => { try { if (!S || !S.xs || !xsLvl()) return; const T = now(), X = xsOf(), A = G.xsAl || (G.xsAl = {}); X.inc.forEach(it => { if (!it || it.e <= T) return; const f = (T - it.s) / Math.max(1, it.e - it.s), k = it.sp + it.s; if (f >= .9 && !A[k]) { A[k] = 1; toast(`Something is moving inside your ${xsName(it.sp)} egg…`); } }); } catch (e) {} }, 30000);
function elExtra(e) {'''
rep("function elExtra(e) {", JS)
# the cards
rep('<div class="xsart"><img src="${xsImg(c.sp)}" alt="" loading="lazy"></div>', '<div class="xsart" data-sp="${c.sp}"><img src="${xsImg(c.sp)}" alt="" loading="lazy"><i class="xsspin" data-sp="${c.sp}"></i></div>')
rep('function sanctCard() { const X = xsOf(), L = xsLvl(), T = now(), slots = xsIncN(L), cap = xsCap(L); if (L) advSay1("sanct");',
    'function sanctCard() { const X = xsOf(), L = xsLvl(), T = now(), slots = xsIncN(L), cap = xsCap(L); if (L) advSay1("sanct"); try { if (L) setTimeout(() => xsStripQueue(X.hab.map(c => c.sp).concat(X.inc.filter(Boolean).map(it => it.sp))), 60); } catch (e) {} /* v786 */')
rep('return `<div class="dp xsc"><button class="btn wide amber xs3go" data-act="xs3Open">◉ Walk the Sanctuary in 3D</button>',
    'return `<div class="dp xsc"><button class="btn wide amber xs3go" data-act="xs3Open">◉ Walk the Sanctuary in 3D</button>${xsStreakN() ? `<div style="display:flex;justify-content:center;margin:6px 0"><span class="xsstreak">🔥 Care streak: <b>${xsStreakN()}</b> day${xsStreakN() > 1 ? "s" : ""} · every 7th day +10 ◆</span></div>` : `<div style="display:flex;justify-content:center;margin:6px 0"><span class="xsstreak">🔥 Feed a creature or warm an egg each day to build a care streak</span></div>`}')
rep('return `<div class="xsinc${done ? " ready" : ""}" style="--wb:', 'return `<div class="xsinc${done ? " ready" : (T - it.s) / Math.max(1, it.e - it.s) >= .9 ? " near" : ""}" style="--wb:')
# the hatch
rep('<div class="xsshards">${shards}</div><img src="${xsImg(c.sp)}" alt=""></div>', '<div class="xsshards">${shards}</div><img src="${xsImg(c.sp)}" alt=""><i class="xsspin xsbaby" data-sp="${c.sp}"></i></div>')
rep('<div class="xsrays"></div><div class="xsfxb"><div class="xshatch">', '<div class="xsrays"></div><div class="xsfxb"><div class="xshatch" data-sp="${c.sp}">')
rep('el.id = "xsrv"; el.className = "xsfx hatch" + (c.pr ? " pr" : "");', 'el.id = "xsrv"; el.className = "xsfx hatch" + (c.pr ? " pr" : "") + (D[1] >= 2 ? " rg" : ""); try { xsStrip(c.sp); setTimeout(() => { try { xsStrip(c.sp); } catch (e) {} }, 1700); } catch (e) {} /* v786 the baby in 3D (its sculpt may still be loading: tried again just before the burst) */')
# feeding and warming count toward the streak; feeding shows the growth
rep("c.g = (c.g || 0) + 1; try { SFX.research(); } catch (e) {} t", "const g0 = c.g || 0; c.g = g0 + 1; xsCare(); setTimeout(() => xsGrowFx(c, g0), 120); try { SFX.research(); } catch (e) {} t")
rep("const cut = Math.max(5 * 60e3, (it.e - T) * .15); it.e = Math.max(T, it.e - cut); it.w = T;", "const cut = Math.max(5 * 60e3, (it.e - T) * .15); it.e = Math.max(T, it.e - cut); it.w = T; xsCare();")
open(p, "w", encoding="utf-8").write(s)
print("ok")
