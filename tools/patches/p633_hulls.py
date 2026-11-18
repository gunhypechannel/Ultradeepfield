# v633: premium hull finishes for ships. See p633_hulls.js.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p633_hulls.js', encoding='utf-8').read()
# the code sits after the premium tiers
a = s.index('const PXG_FX = '); s = s[:a] + js + s[a:]
# the renderer: "^me" resolves to this ship type's finish; "~h<finish>" is parsed, applied to the hull, and sparkles added
rep('  const S = studio(); if (!S || !kind) return null; const key = k + "|" + accent + "|" + view; if (S.cache[key] !== undefined) return S.cache[key];\n  let rotK = 0;',
    '  accent = hullAccK(k, accent); const S = studio(); if (!S || !kind) return null; const key = k + "|" + accent + "|" + view; if (S.cache[key] !== undefined) return S.cache[key];\n  let fin = null; { const mh = /~h([a-z]+)/.exec(String(accent)); if (mh) { fin = HULL_F[mh[1]] ? mh[1] : null; accent = String(accent).replace(mh[0], ""); } } /* v633 */\n  let rotK = 0;')
rep(': buildDefense(k, M); S.scene.add(ship);', ': buildDefense(k, M); if (fin && kind === "s") hullFinish(ship, fin); S.scene.add(ship);')
rep('if (view === "side" && kind === "s" && k !== "eclipse" && k !== "flagship" && !ship.userData.glb) {', 'if (fin) finSpark(out, fin, k); if (view === "side" && kind === "s" && k !== "eclipse" && k !== "flagship" && !ship.userData.glb && !fin) {')
rep('function shipArtSoon(k, accent, view) {\n  const S = studio();', 'function shipArtSoon(k, accent, view) {\n  accent = hullAccK(k, accent); const S = studio();')
# your side is "^me"
rep('return { [mine]: myAcc(), [foe]:', 'return { [mine]: myAcc() + "^me", [foe]:')
rep('if (FLAG_GLOW[f] != null) Object.defineProperty(q, "acc", { value: "#" + FLAG_GLOW[f].toString(16).padStart(6, "0") + "@" + f, enumerable: false,', 'if (FLAG_GLOW[f] != null) Object.defineProperty(q, "acc", { value: "#" + FLAG_GLOW[f].toString(16).padStart(6, "0") + "@" + f + (u === G.me ? "^me" : ""), enumerable: false,')
rep('.map(k => () => shipArt(k, myAcc(), "side")), // v66', '.map(k => () => shipArt(k, myAcc() + "^me", "side")), // v66')
rep('else { const art = shipArt(k, myAcc(), "hero"); if (art) {', 'else { const art = shipArt(k, myAcc() + "^me", "hero"); if (art) {')
rep('const acc = c.dataset.fac ? facAcc(c.dataset.fac) : myAcc(), kk = needDraw(c, acc);', 'const acc = c.dataset.fac ? facAcc(c.dataset.fac) : hullAccK(c.dataset.ship, myAcc() + "^me"), kk = needDraw(c, acc);')
# the ship's page: the picker under the header, and the painting tinted in the finish
rep('`<button class="dmore" data-act="dMore">${sheet.dmore ? "Less ▴" : "More ▾"}</button>` : ""}</div><button class="x" data-act="close" aria-label="Close">✕</button></div>',
    '`<button class="dmore" data-act="dMore">${sheet.dmore ? "Less ▴" : "More ▾"}</button>` : ""}</div><button class="x" data-act="close" aria-label="Close">✕</button></div>${kind === "s" && !P ? hullPick(k) : ""}')
rep('shEl.style.setProperty("--dart", pic ? `url("${pic}")` : "none");', 'shEl.style.setProperty("--dart", pic ? `url("${pic}")` : "none"); { const hf = det && sheet.kind === "s" ? hullOf(sheet.k) : null; shEl.dataset.fin = hf || ""; if (hf) shEl.style.setProperty("--fin", HULL_F[hf].col); } /* v633 */')
# premium page: which finishes a tier brings
rep('<span class="prperk">Skin: ${pxPerk(PXS[P.k])}</span>', '<span class="prperk">Skin: ${pxPerk(PXS[P.k])}</span>${hullsAt(sel).length ? `<span class="prperk">Hull finishes: ${hullsAt(sel).join(", ")}${HULL_F[Object.keys(HULL_F).find(f => HULL_F[f].t === sel)] ? " <b>NEW</b>" : ""}</span>` : ""}')
# actions
rep('  hbShow: d => {', '''  hullSet: d => { const k = d.k, f = d.f || ""; if (f && !hullOk(f)) { toast(`${HULL_F[f].n} hulls unlock at Premium Tier ${HULL_F[f].t}.`, "warn"); return; } S.hullF = Object.assign({}, S.hullF, { [k]: f }); if (!f) delete S.hullF[k]; dirty(); if (f) toast(`${SH[k] ? SH[k].n : k}: ${HULL_F[f].n} hull.`, "win"); try { if (f) fgSnd("fg_reveal"); } catch (e) {} render(true); },
  hullAll: d => { const f = hullOf(d.k) || ""; S.hullF = {}; if (f) for (const k of Object.keys(SH)) S.hullF[k] = f; dirty(); toast(f ? `Every ship type now wears ${HULL_F[f].n}.` : "Every ship type is back to standard."); render(true); },
  hbShow: d => {''')
css = ('.hfp{flex-shrink:0;margin:10px 0 4px;padding:10px 12px;border-radius:14px;background:rgba(6,12,20,.78);border:1px solid rgba(255,210,90,.35);display:flex;flex-direction:column;gap:8px;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}'
  '.hfh{display:flex;flex-direction:column}.hfh b{font:700 14px var(--f-display);color:#ffd25a}.hfh small{font-size:11.5px;color:var(--muted)}.hfr{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px}'
  '.hfb{all:unset;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0}.hfb i{width:40px;height:40px;border-radius:12px;border:2px solid rgba(255,255,255,.18);box-shadow:inset 0 0 8px rgba(0,0,0,.4);position:relative;overflow:hidden}'
  '.hfb i::after{content:"";position:absolute;inset:-30%;background:linear-gradient(115deg,transparent 40%,rgba(255,255,255,.7) 50%,transparent 60%);background-size:300% 100%;animation:pxglint 3s ease-in-out infinite}.hfb small{font-size:10.5px;color:#cfdbe6;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}'
  '.hfb.on i{border-color:#ffd25a;box-shadow:0 0 12px rgba(255,210,90,.7)}.hfb.on small{color:#ffd25a;font-weight:700}.hfb.lk i{filter:grayscale(.75) brightness(.55)}.hfb.lk i::after{display:none}.hfb.lk small{color:var(--muted)}.hfp .gwlink{align-self:flex-start}'
  '.sheet.full.pic.uart[data-fin]:not([data-fin=""]){background-blend-mode:normal,color,normal,normal!important;background:linear-gradient(180deg,rgba(3,8,16,.96) 0%,rgba(3,8,16,.82) 14%,rgba(3,8,16,.06) 30%,rgba(3,8,16,.04) 66%,rgba(3,8,16,.85) 82%,rgba(3,8,16,.96) 100%),linear-gradient(var(--fin),var(--fin)),var(--dart) center 50%/auto 68% no-repeat,radial-gradient(ellipse at 50% 45%,#16304c,#03070d 70%)!important}'
  '@media (prefers-reduced-motion:reduce){.hfb i::after{animation:none}}\n')
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
s2 = re.sub(r"GAME_V = 632\b", "GAME_V = 633", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
