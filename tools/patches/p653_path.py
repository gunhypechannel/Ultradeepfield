# v653 "Next on your path" remaster (owner: "I thought we were gonna remaster this? Why didn't it?"). Each step is a card now: the
# ship's or technology's own picture, its name large, a bar for how close its requirements are, the requirements as chips you can
# tap (each opens that building or research), and the reward on its own strip. A step you can start glows green with a Start
# button that opens it; otherwise Next step opens the first thing still missing. Ships are amber, research cyan.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
old_start = '<div class="mcard"><h3>Next on your path</h3>${next.map(({ m, miss }) =>'
i = s.index(old_start); j = s.index("|| '<p class=\"note\">Everything unlocked. Claim your rewards above.</p>'}</div>", i)
s = s[:i] + '<div class="mcard"><h3>Next on your path</h3>${next.map(({ m, miss }) => pathCard(m, miss, rw)).join("") ' + s[j:]
rep('function mMastery() {', r'''/* v653 one step on the path, as a card */
const pathKind = k => k in B ? "b" : k in R ? "r" : null;
function pathCard(m, miss, rw) { const E = Object.entries(m.req || {}).filter(([k]) => ANY[k]), tot = E.length, met = E.filter(([k, l]) => lvlOf(k) >= l).length, ready = !miss,
    pct = tot ? Math.round(E.reduce((a, [k, l]) => a + Math.min(1, lvlOf(k) / l), 0) / tot * 100) : 100, first = E.find(([k, l]) => lvlOf(k) < l && pathKind(k)), sh = m.kind !== "r";
  const go = ready ? `data-act="detail" data-kind="${sh ? "s" : "r"}" data-k="${m.k}"` : first ? `data-act="detail" data-kind="${pathKind(first[0])}" data-k="${first[0]}"` : `data-act="nav" data-v="build" data-s="${sh ? "ships" : "research"}"`;
  const chips = E.map(([k, l]) => { const ok = lvlOf(k) >= l, pk = pathKind(k); return `<button class="pchip${ok ? " ok" : ""}"${pk ? ` data-act="detail" data-kind="${pk}" data-k="${k}"` : ""}>${ok ? "✓ " + esc(ANY[k].n) : `${esc(ANY[k].n)} <b>${lvlOf(k)}/${l}</b>`}</button>`; }).join("");
  return `<div class="pth ${sh ? "ps" : "pr"}${ready ? " rdy" : ""}"><div class="pth-art"><canvas ${sh ? `data-ship="${m.k}"` : `data-rs="${m.k}|1"`} role="img" aria-label="${esc(m.n)}"></canvas></div>
    <div class="pth-b"><small class="pth-k">${sh ? (TITAN_INFO[m.k] ? "Titan" : "New ship") : "New research"}</small><b class="pth-n">${esc(m.n)}</b>
      <div class="pth-bar"><i style="width:${pct}%"></i></div><small class="pth-st">${ready ? "Ready to start" : `${met}/${tot} requirements met`}</small></div>
    <button class="btn ${ready ? "amber" : "ghost"} sm pth-go" ${go}>${ready ? "Start" : "Next step"}</button>
    ${ready ? "" : `<div class="pth-req">${chips}</div>`}<div class="pth-rw"><span>Reward</span>${pathGain(m)}</div></div>`; }
/* the reward, as a gain: never red for what you cannot afford */
function pathGain(m) { const r = masteryReward(m); return ["m", "c", "g"].filter(k => r[k]).map(k => `<span class="pg r-${k}">${RI[k]}+${fmt(r[k])}</span>`).join("") + `<span class="pg shard">◆${r.sh}</span>`; }
function mMastery() {''')
rep('.chipq.met{', r'''.pth{display:grid;grid-template-columns:84px minmax(0,1fr) auto;grid-template-areas:"a b g" "q q q" "r r r";gap:8px 12px;align-items:center;margin:10px 0;padding:12px;border-radius:14px;position:relative;overflow:hidden;
  --pc:255,196,90;border:1px solid rgba(var(--pc),.28);background:radial-gradient(120% 140% at 0% 0%,rgba(var(--pc),.13),transparent 55%),linear-gradient(180deg,rgba(255,255,255,.035),rgba(0,0,0,.12));box-shadow:inset 3px 0 0 rgba(var(--pc),.75)}
.pth.pr{--pc:85,214,232}.pth.rdy{--pc:113,223,144;box-shadow:inset 3px 0 0 rgba(var(--pc),.9),0 0 18px rgba(var(--pc),.22);animation:pthGlow 2.8s ease-in-out infinite}
@keyframes pthGlow{50%{box-shadow:inset 3px 0 0 rgba(var(--pc),.9),0 0 26px rgba(var(--pc),.38)}}
.pth-art{grid-area:a;width:84px;height:56px;border-radius:10px;background:radial-gradient(circle at 50% 60%,rgba(var(--pc),.22),#02060c 72%);border:1px solid rgba(var(--pc),.3);display:grid;place-items:center;overflow:hidden}
.pth-art canvas{width:84px;height:56px;display:block}
.pth-b{grid-area:b;min-width:0;display:flex;flex-direction:column;gap:3px}.pth-k{font-family:var(--f-display);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:rgb(var(--pc))}
.pth-n{font-size:16px;font-weight:700;color:#eef8fc;line-height:1.15;overflow-wrap:anywhere}
.pth-bar{height:5px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden;margin-top:2px}.pth-bar i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,rgba(var(--pc),.55),rgb(var(--pc)));box-shadow:0 0 8px rgba(var(--pc),.6)}
.pth-st{font-size:11.5px;color:var(--muted)}.pth.rdy .pth-st{color:var(--green);font-weight:600}
.pth-go{grid-area:g;align-self:center;white-space:nowrap}
.pth-req{grid-area:q;display:flex;flex-wrap:wrap;gap:6px}
.pchip{all:unset;cursor:pointer;white-space:nowrap;font-size:12px;padding:4px 9px;border-radius:999px;border:1px solid rgba(255,196,90,.55);color:#ffd27a;background:rgba(255,196,90,.08);font-family:var(--f-display);letter-spacing:.02em}
.pchip b{font-weight:700}.pchip.ok{border-color:rgba(113,223,144,.4);color:#8fe7a8;background:rgba(113,223,144,.07)}.pchip:active{transform:scale(.96)}
.pth-rw{grid-area:r;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;padding:7px 10px;border-radius:10px;background:rgba(0,0,0,.28);border:1px solid rgba(255,255,255,.06);font-size:13px}
.pth-rw .pg{display:inline-flex;align-items:center;gap:3px;color:#d9f6e4;font-weight:600}.pth-rw .pg svg,.pth-rw .pg img{width:16px;height:16px}.pth-rw .pg.shard{color:#d9a6ff}
.pth-rw > span:first-child{font-family:var(--f-display);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
@media (max-width:360px){.pth{grid-template-columns:64px minmax(0,1fr);grid-template-areas:"a b" "g g" "q q" "r r"}.pth-art,.pth-art canvas{width:64px;height:44px}.pth-go{justify-self:stretch}}
.chipq.met{''')
rep('const GAME_V = 652', 'const GAME_V = 653')
open(p, 'w', encoding='utf-8').write(s)
