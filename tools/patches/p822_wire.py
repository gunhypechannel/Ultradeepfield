"""v822: the motion standard (owner: "The models are spinning WAY TO FAST ... a reoccurring theme of me telling you to slow things down";
"the lines on the streets don't need to move"; "Do that"). Speed does not cost frames, but the game had 129 continuous spins, 89 faster than
a turn every 30 s. One standard now: MOT (base .22 of real time, was .55; the map's decorative spins x.35), the street-line flow and the
ring lane's pulse stop, Sanctuary turntables stand still in the list and turn (at half speed) only under the finger or pointer, and the
decorative UI rays and rings turn about 2.5x slower. Loading spinners and battle effects keep their pace. Audit: tools/motion/audit.py."""
import sys, re
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 821;", "const GAME_V = 822;")
rep("const OBV = { x: 0, y: 0, z: 0 }, OBV2", "const MOT = { base: .22, map: .35 }; /* v822 the motion standard: one place for how fast the world moves */\nconst OBV = { x: 0, y: 0, z: 0 }, OBV2")
# the base: one clock for all its ambient motion
rep("const T = reduced ? 0 : t * .55; // v190", "const T = reduced ? 0 : t * MOT.base; // v822 the motion standard (was .55); v190")
rep("if (!reduced) { roadKit().flow.offset.x = -(T * .0005) % 1; if (W.props) W.props.userData.scr.offset.y = (T * .00012) % 1; if (W.roads && W.roads.userData.ringLane) W.roads.userData.ringLane.material.opacity = .55 + .25 * Math.sin(T * .003); }",
    "if (!reduced) { if (W.props) W.props.userData.scr.offset.y = (T * .00012) % 1; if (W.roads && W.roads.userData.ringLane && !W.roads.userData.rlSet) { W.roads.userData.ringLane.material.opacity = .7; W.roads.userData.rlSet = 1; } } /* v822 the street lines and the ring lane hold still */")
# the map's decorative spins
for a, b in [("b.ring.rotation.y = t * .0006; b.ring2.rotation.y = -t * .0003;", "b.ring.rotation.y = t * .0006 * MOT.map; b.ring2.rotation.y = -t * .0003 * MOT.map;"),
             ("o.ring.rotation.y = t * .0003; o.grp.rotation.y = t * 4e-5 + it.a0;", "o.ring.rotation.y = t * .0003 * MOT.map; o.grp.rotation.y = t * 4e-5 + it.a0;"),
             ("else o.grp.rotation.y = t * .0003 + it.a0; o.grp.scale.setScalar(MK_K * (hl ? 1.3 : 1)); }", "else o.grp.rotation.y = t * .0003 * MOT.map + it.a0; o.grp.scale.setScalar(MK_K * (hl ? 1.3 : 1)); }"),
             ("o.grp.rotation.y = t * (it.boss ? .00008 : .0002) + it.a0; o.ring.rotation.z = t * .0006;", "o.grp.rotation.y = t * (it.boss ? .00008 : .0002) * MOT.map + it.a0; o.ring.rotation.z = t * .0006 * MOT.map;"),
             ("if (o.ring) { o.ring.rotation.y = t * .00025;", "if (o.ring) { o.ring.rotation.y = t * .00025 * MOT.map;")]:
    rep(a, b)
# CSS: decorative turns about 2.5x slower (spins only; flickers, hue shifts and pops keep their pace); turntables wait for a touch
KEEP = {"raflick", "xshue", "xsgrowk", "xsbabypop", "xsbabyshake"}
def slow(sel, k=2.5):
    i = s.find(sel + "{"); assert i >= 0, sel; j = s.find("}", i); body = s[i + len(sel) + 1:j]; m = re.search(r"animation:([^;}]*)", body); assert m, sel
    parts = [x.strip() for x in re.split(r",(?![^(]*\))", m.group(1))]; durs = []
    for x in parts:
        nm = x.split()[0]; d = re.search(r"\s([0-9.]+)s", " " + x.split(" ", 1)[1] if " " in x else ""); d = float(d.group(1)) if d else 1
        durs.append(f"{d if nm in KEEP else round(d * k, 1):g}s")
    return f"body {sel}{{animation-duration:{','.join(durs)}}}"
CSS = [slow(x) for x in [".xsrays", ".rvrays", ".fgrays", "#celeb .cbrays", ".prring", ".prcard.gold .prring", ".gwjr", ".rw .ra.a1", ".rw .ra.a2", ".rw .ws", ".rkav::before", ".pau .r1", ".pau .r2", ".pau .mo", ".pwh i", ".rw .lf"]]
CSS += [slow(".xsspin", 2), slow(".xscr.pr .xsspin", 2), slow("#xsgrow .xsspin,#xsgrow img", 2).replace("body #xsgrow .xsspin,#xsgrow img{", "body #xsgrow .xsspin{"),
        "body .xsspin{animation-play-state:paused}body .xscr:hover .xsspin,body .xscr:active .xsspin,body .xscr:focus-within .xsspin,body #xsgrow .xsspin,body .xshatch .xsspin{animation-play-state:running}"]
i = s.index("</style>"); s = s[:i] + "".join(CSS) + s[i:]
open(p, "w", encoding="utf-8").write(s); print("ok"); print("\n".join(CSS))
