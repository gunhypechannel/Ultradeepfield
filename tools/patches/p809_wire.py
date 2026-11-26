"""v809: the Aetherion preview gets a door in the Boss Lab (before, its controls only showed once a preview was already on)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 808;", "const GAME_V = 809;")
rep("""${labAllHTML(T)}<h2 class="sec">The rotation calendar</h2>""", """${labAllHTML(T)}${typeof aetLabHTML === "function" ? aetLabHTML(T) : ""}<h2 class="sec">The rotation calendar</h2>""")
rep("const PIRATES = PIRATES_ALL.filter(", r"""function aetLabHTML(T) { const cur = S.aetPrev ? (S.aetPrev.m === "open" ? "open" : `s${S.aetPrev.j}_${S.aetPrev.w}`) : "off", b = (v, l) => `<button class="btn ${cur === v ? "pri" : "ghost"}" data-act="labAet" data-v="${v}">${l}</button>`;
  return `<h2 class="sec">The Aetherion (players: hidden until the switch is on)</h2><div class="strows">${AET_SAGA.map((s, j) => `<div class="strow" style="flex-wrap:wrap;gap:6px"><div style="flex:1 1 100%;min-width:0"><b>◈ ${esc(s[0])}</b><div class="note">Season ${vpSeason(AET_T0() + j * VP_LEN + 864e5) + 1} · ${new Date(AET_T0() + j * VP_LEN).toLocaleDateString([], { month: "short", day: "numeric", year: "numeric" })}</div></div>${[1, 2, 3, 4].map(w => b(`s${j}_${w}`, "W" + w)).join("")}${b("f" + j, "★ Finale")}</div>`).join("")}
    <div class="strow" style="flex-wrap:wrap;gap:6px"><div style="flex:1 1 100%;min-width:0"><b>◈ The Gateway open</b><div class="note">Opens ${new Date(aetOpenAt()).toLocaleDateString([], { month: "short", day: "numeric", year: "numeric" })} · Command Center, realms, bosses</div></div>${b("open", "▶ Open")}${b("off", "■ Off")}</div></div>`; }
const PIRATES = PIRATES_ALL.filter(""")
rep("const ACT = { ...AET_ACT,", """const ACT = { ...AET_ACT, labAet: d => { if (!ownerFree()) return; AET_ACT.aetPrev(d); if (d.v === "off") { renderSheet(); return; } closeSheet(); setTimeout(() => { if (/^(s\\d_\\d|f\\d)$/.test(d.v)) AET_ACT.aetSgOpen ? AET_ACT.aetSgOpen() : openSheet({ type: "aetsaga" }); else openSheet({ type: "aet" }); }, 250); },""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
