import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 (owner's request) the Advisor's hologram appears every time she speaks: the Academy step lines now come with a compact
# hologram of her and her words, placed in the half of the screen the guide isn't pointing at; taps go through it
lines = t.split('\n'); i0 = next(i for i, l in enumerate(lines) if l.startswith('#adv .advimg{')); i1 = next(i for i in range(i0, i0 + 20) if lines[i].startswith('@media (prefers-reduced-motion:reduce){#adv .advimg'))
dup = [l.replace('#adv.talk', '#advh.talk').replace('#adv ', '#advh ') for l in lines[i0:i1] if '#adv' in l or l.startswith('  ')]
css = '\n'.join(dup) + '''
#advh{position:fixed;left:max(8px,env(safe-area-inset-left,0px));z-index:69;display:flex;align-items:flex-end;gap:8px;pointer-events:none;opacity:0;transform:translateY(10px);transition:opacity .3s,transform .3s;max-width:min(94vw,520px)}
#advh.on{opacity:1;transform:none}#advh .holo{position:relative;flex:none;width:84px;height:126px}
#advh .advimg{position:absolute;left:0;bottom:0;width:84px;height:126px;object-fit:cover;object-position:50% 8%}
#advh .hscan{width:84px;height:126px}#advh .hbeam{width:84px;bottom:-8px;height:22px}#advh .hbeam::before{height:90px}
#advh .hsay{margin-bottom:10px;padding:8px 11px;border-radius:12px;background:rgba(4,18,28,.9);border:1px solid rgba(85,214,232,.65);box-shadow:0 0 18px rgba(85,214,232,.28);color:#e2f9ff;font:500 13.5px/1.38 var(--f-body,system-ui);text-wrap:pretty}
#advh .hsay b{display:block;font:700 10px/1 var(--f-display);letter-spacing:.2em;text-transform:uppercase;color:#7fe8ff;margin-bottom:4px}
@media (prefers-reduced-motion:reduce){#advh,#advh .advimg,#advh .hscan,#advh .hbeam{animation:none;transition:none}}'''
lines.insert(i1 + 1, css); t = '\n'.join(lines)
rep('''function voiceTalk(on) { const a = $("#adv"); if (a) a.classList.toggle("talk", !!on);''', '''function voiceTalk(on) { const a = $("#adv"); if (a) a.classList.toggle("talk", !!on); const h = $("#advh"); if (h) h.classList.toggle("talk", !!on);''')
rep('''function speak(line) {''', '''function advHoloPlace() { const w = $("#advh"); if (!w || !w.classList.contains("on")) return; const el = GD.el && GD.el.isConnected ? GD.el : null, r = el && el.getBoundingClientRect(), dock = $("#dock"), db = dock ? dock.getBoundingClientRect().top : innerHeight;
  const top = r ? r.top + r.height / 2 > innerHeight * .5 : false; w.style.top = top ? "max(86px, calc(env(safe-area-inset-top,0px) + 86px))" : "auto"; w.style.bottom = top ? "auto" : (innerHeight - db + 64) + "px"; }
function advHolo(line) { if (!line) return; let w = $("#advh"); // v334: her hologram for every spoken step line
  if (!w) { w = document.createElement("div"); w.id = "advh"; w.setAttribute("aria-live", "polite"); w.innerHTML = `<div class="holo"><img class="advimg" src="${ADV_ART}" alt=""><i class="hscan"></i><i class="hbeam"></i></div><div class="hsay"><b>${ADV}</b><span></span></div>`; $("#app").appendChild(w); }
  w.querySelector(".hsay span").textContent = line; w.classList.add("on"); advHoloPlace(); clearTimeout(G.advhT); speak(line);
  const hide = () => { clearTimeout(G.advhT); G.advhT = setTimeout(() => { const x = $("#advh"); if (x) x.classList.remove("on", "talk"); }, 900); };
  const a = VOICE.au; if (a && !a.ended) { a.addEventListener("ended", hide, { once: true }); a.addEventListener("error", hide, { once: true }); G.advhT = setTimeout(hide, 30000); } else G.advhT = setTimeout(hide, Math.max(4500, line.length * 65)); }
function speak(line) {''')
rep('''VOICE.lastStep = S.tut.i; speak(st.say); }''', '''VOICE.lastStep = S.tut.i; advHolo(st.say); }''')
# keep her out of the way of blocking screens, and follow the guide's target as it moves
rep('''  try { tutTrack(); } catch (e) {}''', '''  try { tutTrack(); } catch (e) {} try { const h = $("#advh"); if (h && h.classList.contains("on")) { if ($("#adv") || battle || $("#celeb")) h.classList.remove("on"); else advHoloPlace(); } } catch (e) {}''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok', len(dup))
