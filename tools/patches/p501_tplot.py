# v501 the Cube's tactical plot (owner's clip of a tactical display: one huge vessel, targeting lines to the fleets around it).
# A live 2D plot under the Cube event's clip, and on the alliance page while the Battle for the Cube runs: the Cube at the top,
# the holders' garrison, rival alliances and your own commanders as named blips; targeting lines jump between them while it is live.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

CSS = '''.cubeacts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 4px}
.tplotw{position:relative;margin:10px 0 4px;border-radius:14px;overflow:hidden;border:1px solid rgba(120,140,255,.35);background:#070a24;box-shadow:0 0 24px rgba(80,90,255,.18) inset}
.tplotw{aspect-ratio:16/11;max-width:100%;flex-shrink:0;min-height:200px}.tplotw canvas.tplot{position:absolute;inset:0;display:block;width:100%!important;height:100%!important}
.tplotw .tph{position:absolute;left:10px;top:8px;font:700 10px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.14em;color:#9fb0ff;text-transform:uppercase;pointer-events:none}
.tplotw .tpf{position:absolute;left:10px;right:10px;bottom:7px;display:flex;justify-content:space-between;gap:8px;font:600 10px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.08em;color:#c9d2ff;text-transform:uppercase;pointer-events:none}
.tplotw .tpf b{color:#ffb070}.tplotw .tpf .tplive{color:#ff6a4a}
.mcard.tpcall h3{color:#ffb070}.mcard.tpcall .tplotw{margin-top:6px}'''
rep('.cubeacts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 4px}', CSS)

JS = r'''/* v501 the Cube's tactical plot: a live plot of the Battle for the Cube (owner's clip of a tactical display). The Cube sits at the
   top; around it, named blips for the holders' garrison (amber), rival alliances (red) and your own commanders (cyan). While the
   battle is live, targeting lines from the Cube jump between the fleets that are not holding it; otherwise it is dormant and scanning. */
function tplotData(T = now()) { const live = evActive(T), nx = nexusNow(T), my = myAlly(), out = [], seen = new Set(), add = (n, side, k) => { if (!n || seen.has(k)) return; seen.add(k); out.push({ n: String(n).toUpperCase().slice(0, 13), side, k }); };
  if (live) { if (nx.holder) for (const u of Object.keys(nx.garrison || {}).slice(0, 5)) add(u === G.me ? (G.myName || "You") : nameOf(u), "hold", "u" + u);
    Object.entries(nx.points || {}).filter(([a]) => a !== nx.holder && G.alliances[a] && (!my || a !== my.id)).sort((x, y) => y[1] - x[1]).slice(0, 4).forEach(([a]) => add(`[${G.alliances[a].tag}] fleet`, "foe", "a" + a)); }
  if (my) Object.keys(my.members).sort((x, y) => (x === G.me ? -1 : y === G.me ? 1 : ((G.players[y] || {}).score || 0) - ((G.players[x] || {}).score || 0))).slice(0, 7).forEach(u => add(u === G.me ? (G.myName || "You") : nameOf(u), my.id === nx.holder && live ? "hold" : "me", "u" + u));
  if (out.length < 4) [["Crimson Armada", "foe"], ["Iron Bastion", "foe"], ["Void Lancers", "foe"], ["Solar Wardens", "foe"]].forEach(([n, sd]) => out.length < 6 && add(n, sd, "d" + n));
  return { live, holder: live && nx.holder && G.alliances[nx.holder] ? G.alliances[nx.holder].tag : null, ships: out, end: live ? evStart(evWeek(T)) + EV_DUR : evStart(evWeek(T) + 1) }; }
function tplotHTML(T = now()) { const d = tplotData(T);
  return `<div class="tplotw"><canvas class="tplot" aria-label="Tactical plot of the Cube"></canvas><span class="tph">Tactical plot · sector 0</span><div class="tpf"><span>${d.live ? `<b class="tplive">● Live</b> · ${d.holder ? `held by <b>[${esc(d.holder)}]</b>` : "<b>unclaimed</b>"}` : "Dormant · scanning"}</span><span>${d.live ? "ends" : "wakes"} in <b data-end="${d.end}">${ftime(d.end - T)}</b></span></div></div>`; }
const TPL = { run: false, ls: [], nt: 0, hit: {}, star: null, dat: null, dt: 0 };
function tplotFrame(ts) { const cvs = [...document.querySelectorAll("canvas.tplot")].filter(c => c.offsetParent); if (!cvs.length || document.hidden) { TPL.run = false; return; } requestAnimationFrame(tplotFrame);
  if (!TPL.dat || ts - TPL.dt > 5000) { TPL.dat = tplotData(); TPL.dt = ts; } const D = TPL.dat, t = ts / 1000;
  if (!TPL.star) { TPL.star = []; let r = 7; const rnd = () => (r = (r * 16807) % 2147483647) / 2147483647; for (let i = 0; i < 110; i++) TPL.star.push([rnd(), rnd(), rnd() * 1.1 + .3, rnd()]); }
  const tg = D.ships.map((x, i) => i).filter(i => D.ships[i].side !== "hold");
  if (D.live && ts > TPL.nt && tg.length) { const n = 1 + ((Math.random() * Math.min(5, tg.length)) | 0), pick = tg.slice().sort(() => Math.random() - .5).slice(0, n); TPL.ls = pick.map(i => ({ i, t0: ts })); pick.forEach(i => TPL.hit[i] = ts); TPL.nt = ts + 420 + Math.random() * 900; }
  for (const cv of cvs) { const W = cv.clientWidth, H = cv.clientHeight; if (!W || !H) continue; const pr = Math.min(2, window.devicePixelRatio || 1);
    if (cv.width !== Math.round(W * pr) || cv.height !== Math.round(H * pr)) { cv.width = Math.round(W * pr); cv.height = Math.round(H * pr); } const x = cv.getContext("2d"); x.setTransform(pr, 0, 0, pr, 0, 0);
    x.fillStyle = "#070a24"; x.fillRect(0, 0, W, H);
    const nb = x.createRadialGradient(W * .12, H * .2, 0, W * .12, H * .2, W * .2); nb.addColorStop(0, "rgba(255,240,170,.55)"); nb.addColorStop(.45, "rgba(220,200,120,.18)"); nb.addColorStop(1, "rgba(220,200,120,0)"); x.fillStyle = nb; x.fillRect(0, 0, W, H);
    for (const [sx, sy, sr, ph] of TPL.star) { x.globalAlpha = .35 + .35 * Math.sin(t * 1.3 + ph * 9); x.fillStyle = ph > .93 ? "#ff8a6a" : "#dfe6ff"; x.fillRect(sx * W, sy * H, sr, sr); } x.globalAlpha = 1;
    x.strokeStyle = "rgba(110,110,255,.55)"; x.lineWidth = 1; x.beginPath(); for (const f of [.33, .67]) { x.moveTo(W * f, 0); x.lineTo(W * f, H); } x.moveTo(0, H * .14); x.lineTo(W, H * .14); x.moveTo(0, H * .72); x.lineTo(W, H * .72); x.stroke();
    if (!D.live) { const sw = (t * .25) % 1; x.fillStyle = "rgba(120,140,255,.10)"; x.fillRect(sw * W - 40, 0, 40, H); }
    const cx = W * .47, cy = H * .3, cs = Math.min(W, H) * .15, P = (() => { const F = D.ships.map((s2, i) => i).filter(i => D.ships[i].side !== "hold"), Hd = D.ships.map((s2, i) => i).filter(i => D.ships[i].side === "hold"), o = [];
      F.forEach((i, j) => { const h = hash(D.ships[i].k); o[i] = [W * (.09 + (j + .5) / F.length * .78 + ((h % 100) / 100 - .5) * .05), H * ((F.length > 4 ? [.58, .86, .72][j % 3] : j % 2 ? .82 : .62) + (((h >>> 8) % 100) / 100 - .5) * .06), h]; });
      Hd.forEach((i, j) => { const h = hash(D.ships[i].k), a = Math.PI * (.15 + j * .55 / Math.max(1, Hd.length - 1)) * (j % 2 ? -1 : 1) + (j % 2 ? 0 : 0); o[i] = [cx + Math.cos(a) * cs * 2.2, cy + Math.sin(a) * cs * 1.1 + j * 3, h]; }); return o; })().map(([px, py, h]) => {
      return [px + Math.sin(t * .3 + h) * 3, py + Math.cos(t * .25 + h) * 2]; });
    if (D.live) for (const L of TPL.ls) { const p = P[L.i]; if (!p) continue; const k = Math.min(1, (ts - L.t0) / 140); x.strokeStyle = "rgba(255,236,170,.95)"; x.lineWidth = 1.6; x.shadowColor = "#ffd890"; x.shadowBlur = 6; x.beginPath(); x.moveTo(cx, cy + cs * .6); x.lineTo(cx + (p[0] - cx) * k, cy + cs * .6 + (p[1] - cy - cs * .6) * k); x.stroke(); x.shadowBlur = 0; }
    x.save(); x.translate(cx, cy); const pu = D.live ? 1 + Math.sin(t * 6) * .02 : 1; x.scale(pu, pu); x.beginPath(); x.moveTo(0, -cs); x.lineTo(cs * .95, 0); x.lineTo(0, cs); x.lineTo(-cs * .95, 0); x.closePath();
    x.fillStyle = D.live ? "#f07a52" : "#7a4a40"; x.shadowColor = D.live ? "#ff7a4a" : "transparent"; x.shadowBlur = D.live ? 18 : 0; x.fill(); x.shadowBlur = 0; x.strokeStyle = "#cfe0ff"; x.lineWidth = 2; x.stroke(); x.restore();
    x.font = "700 9px ui-monospace,Menlo,monospace"; x.fillStyle = "#ffb090"; x.textAlign = "left"; x.fillText("THE CUBE", cx + cs * .75, cy - cs * .85); x.fillStyle = "rgba(255,240,190,.75)"; x.fillText("THE VOID", W * .05, H * .2 + 16);
    x.strokeStyle = "rgba(255,236,170,.8)"; x.lineWidth = 1.2; x.beginPath(); x.moveTo(cx - cs * .95, cy); x.lineTo(W * .12, H * .2); x.stroke();
    D.ships.forEach((s2, i) => { const [px, py] = P[i], hit = D.live && TPL.hit[i] && ts - TPL.hit[i] < 260, col = s2.side === "hold" ? "#ffc070" : s2.side === "me" ? "#7fe6ff" : "#ff8a7a";
      x.beginPath(); x.arc(px, py, hit ? 4.2 : 2.6, 0, Math.PI * 2); x.fillStyle = hit ? "#fff" : col; x.shadowColor = col; x.shadowBlur = 8; x.fill(); x.shadowBlur = 0;
      x.font = "700 8.5px ui-monospace,Menlo,monospace"; x.fillStyle = hit ? "#fff" : "#e8ecff"; x.textAlign = px > W * .75 ? "right" : "left"; x.fillText(s2.n, px + (px > W * .75 ? -6 : 6), py - 4); }); } }
setInterval(() => { if (!TPL.run && !document.hidden && document.querySelector("canvas.tplot")) { TPL.run = true; TPL.dat = null; requestAnimationFrame(tplotFrame); } }, 600);
'''
rep('const DEMO_ALLY = { a: {', JS + 'const DEMO_ALLY = { a: {')
# under the Cube clip
rep('''        </div></div>
      <div class="cubeacts">''', '''        </div></div>${tplotHTML(T)}
      <div class="cubeacts">''')
# the alliance page while the battle runs: a call to arms with the plot
rep('''    ${a.bio ? `<div class="mcard"><p class="albio">${esc(a.bio)}</p></div>` : ""}${allyWarCard(a)}${allyTools(a)}''',
    '''    ${evActive(T) ? `<div class="mcard tpcall"><h3>◆ The Battle for the Cube is live</h3><p class="note">${nexusNow(T).holder === a.id ? "Your alliance holds the Cube. Reinforce the garrison before the rivals break it." : "The Cube is firing on the fleets around it. Every commander who joins raises your alliance's points."}</p>${tplotHTML(T)}<button class="btn amber wide" data-act="nexus">⚔ Join the battle</button></div>` : ""}
    ${a.bio ? `<div class="mcard"><p class="albio">${esc(a.bio)}</p></div>` : ""}${allyWarCard(a)}${allyTools(a)}''')
s2 = re.sub(r"GAME_V = 500\b", "GAME_V = 501", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
