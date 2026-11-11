# v428: the battle replay's event log is a drop-down (owner: "make the log like a drop down option"). It used to stack the last 3
#  events over the top-left of the field, on a phone right over the top side's flagships. Now a small "Log" pill: closed by default
#  (it pulses for a moment when a new event lands), tap to open the last 6 events, tap again to close. The choice is remembered.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep(".bev{position:absolute;left:10px;top:calc(13% + 56px);z-index:2;display:flex;flex-direction:column;gap:4px;max-width:62%;pointer-events:none}",
    ".bev{position:absolute;left:10px;top:calc(13% + 56px);z-index:2;display:flex;flex-direction:column;align-items:flex-start;gap:4px;max-width:62%;pointer-events:none}"
    ".bevt{pointer-events:auto;display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 10px;border-radius:13px;background:rgba(4,12,20,.78);border:1px solid rgba(95,208,255,.45);color:#cfefff;font-family:var(--f-display);font-size:11px;letter-spacing:.06em;cursor:pointer}"
    ".bevt b{font-weight:700;color:#ffd66a}.bevt i{font-style:normal;display:inline-block;transition:transform .2s}.bevt[aria-expanded=true] i{transform:rotate(90deg)}"
    ".bevt.nw{animation:bevp 1.2s ease-out 2}@keyframes bevp{0%{box-shadow:0 0 0 0 rgba(255,214,106,.7)}100%{box-shadow:0 0 0 9px rgba(255,214,106,0)}}"
    ".bevl{display:flex;flex-direction:column;gap:4px;max-height:38vh;overflow-y:auto;pointer-events:auto}")
rep("""const evs = (b.res.sim.ev || []).filter(e => e.t <= b.simT && e.kind !== "loss").slice(-3), he = evs.map(""",
    """const all = (b.res.sim.ev || []).filter(e => e.t <= b.simT && e.kind !== "loss"), open = bevOpen(), evs = open ? all.slice(-6) : [], last = all[all.length - 1], nw = !open && last && b.simT - last.t < 2.5, /* v428 the log is a drop-down */
    he = `<button class="bevt${nw ? " nw" : ""}" data-act="bevT" aria-expanded="${open}" aria-label="${open ? "Hide" : "Show"} battle log"><i>▸</i>Log${all.length ? ` <b>${all.length}</b>` : ""}</button>` + (evs.length ? `<div class="bevl">` : "") + evs.map(""")
rep("""${esc(scTxt(b.r, e.txt))}</div>`).join(""), E = $("#bev");""", """${esc(scTxt(b.r, e.txt))}</div>`).join("") + (evs.length ? "</div>" : ""), E = $("#bev");""")
rep("  bclose: () => closeBattle(),", """  bclose: () => closeBattle(),
  bevT: () => { const o = !bevOpen(); G.bevOpen = o; try { localStorage.setItem("udf.bevOpen", o ? "1" : "0"); } catch (e) {} const E = $("#bev"); if (E) E.dataset.h = ""; }, /* v428 */""")
rep("function playBattle(r) {", """/* v428 the battle log drop-down: closed unless the player opened it (remembered on this device) */
function bevOpen() { if (G.bevOpen == null) { try { G.bevOpen = localStorage.getItem("udf.bevOpen") === "1"; } catch (e) { G.bevOpen = false; } } return !!G.bevOpen; }
function playBattle(r) {""")
t = t.replace("const GAME_V = 427;", "const GAME_V = 428;")
open(p, "w").write(t); print("ok")
