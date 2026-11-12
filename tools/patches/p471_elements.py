# v471 the Elementals get the remaster spec's names (owner decision 2026-11-11): Glacius -> Gravemorn, Ignis -> Ignaroth, Solara -> Auricor,
# Verdanth -> Viridrax, Voltaris stays; the event stays the Convergence and the fused form the Pentarch. Gravemorn is the void Elemental now
# (deep violet, dark energy, gravity lances, event collapse) instead of ice; Voltaris turns electric blue (its old violet is Gravemorn's).
# Keys (eic, efi, eli, est, ena), the model kinds ("ice", ...) and the runes each gives are unchanged, so saves and records carry over.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
SPEC = [("Glacius has been ripped out of the Pentarch! The cold drains from its core.", "Gravemorn has been ripped out of the Pentarch! The dark drains from its core."),
        ("Glacius, the ice Elemental. Every world in its path is frozen solid. Tomorrow it rides for the Void, so break it while it still stands alone.", "Gravemorn, the void Elemental. Every world in its path is sinking into the dark. Tomorrow it rides for the Void, so break it while it still stands alone."),
        ("Scanning Glacius. Frost nova, ice lances from its orbs, and absolute zero once its rings spin up.", "Scanning Gravemorn. Void nova, gravity lances from its orbs, and an event collapse once its rings spin up.")]
NAMES = [("Glacius", "Gravemorn"), ("Ignis", "Ignaroth"), ("Solara", "Auricor"), ("Verdanth", "Viridrax")]
def xform(t):
    for a, b in SPEC: t = t.replace(a, b)
    for a, b in NAMES: t = re.sub(r"\b" + a + r"\b", b, t)
    return t
if __name__ == "__main__":
    for a, b in SPEC: rep(a, b)
    rep('eic: { k: "wbEic", n: "Glacius", ic: "❄", col: "#6ac4ff", el: "ice",', 'eic: { k: "wbEic", n: "Gravemorn", ic: "◐", col: "#9a5cff", el: "ice",')
    rep('where: "Elemental · Ice", g: 3, cam: 150,\n    d: "The ice Elemental: a silver-blue totem of liquid metal between two great crescents, freezing every world around it." },',
        'where: "Elemental · Void", g: 3, cam: 150,\n    d: "The void Elemental: a dark totem of liquid metal between two great crescents, dragging every world around it into the dark." },')
    rep('est: { k: "wbEst", n: "Voltaris", ic: "ϟ", col: "#b868ff",', 'est: { k: "wbEst", n: "Voltaris", ic: "ϟ", col: "#4ac8ff",')
    rep('["nova", "Frost Nova", "Its crescents clench, then burst out in a ring of frost."], ["lance", "Ice Lance", "Its orbs swing out and fire lances of ice."], ["zero", "Absolute Zero", "Its rings spin up and a freezing shockwave rolls out."]',
        '["nova", "Void Nova", "Its crescents clench, then burst out in a ring of dark energy."], ["lance", "Gravity Lance", "Its orbs swing out and fire lances that drag ships off course."], ["zero", "Event Collapse", "Its rings spin up and space folds inward in a crushing wave."]')
    rep('eic: ["Elemental · ice",', 'eic: ["Elemental · void",')
    rep("WB_STAIN = { eic: [.55, 1.1, 1.9], efi: [1.9, .55, .25], eli: [1.8, 1.45, .45], est: [1.15, .6, 1.9],", "WB_STAIN = { eic: [1.2, .5, 1.9], efi: [1.9, .55, .25], eli: [1.8, 1.45, .45], est: [.5, 1.2, 1.9],")
    rep('ice:    { c1: 0x4ab0ff, c2: 0xe6f6ff, c3: 0x2a5cff, pal: ["#d8e2f0", "#9ab4d8", "#1e3c8c", "#f2f6fc"], vc: "#ffffff", sg: "#6ac4ff", rc: [.45, .8, 1], spark: 0xcfeeff, aura: 0x58b8ff, rgb: "120,200,255" },',
        'ice:    { c1: 0x8a3cff, c2: 0xdcc0ff, c3: 0x4a10c0, pal: ["#1e1430", "#34204e", "#0c0816", "#4a2c70"], vc: "#c8a0ff", sg: "#9a50ff", rc: [.6, .3, 1], spark: 0xc8a0ff, aura: 0x7a30ff, rgb: "150,80,255" }, /* v471 Gravemorn, the void (the key stays "ice") */')
    rep('storm:  { c1: 0xa456ff, c2: 0xead0ff, c3: 0x6a20ff, pal: ["#3c1a70", "#5e2ca0", "#1a0a3c", "#8050cc"], vc: "#e6b8ff", sg: "#b868ff", rc: [.7, .38, 1], spark: 0xe0b0ff, aura: 0xa050ff, rgb: "190,120,255" },',
        'storm:  { c1: 0x3ab8ff, c2: 0xd8f6ff, c3: 0x1a6cff, pal: ["#1a2c48", "#22406a", "#0c1628", "#3a6898"], vc: "#c8f0ff", sg: "#4ac8ff", rc: [.35, .75, 1], spark: 0xcff4ff, aura: 0x3aa8ff, rgb: "90,190,255" }, /* v471 Voltaris, electric blue */')
    rep('ELC = { fire: "#ff7a30", ice: "#8fe0ff", light: "#fff0a0", storm: "#c890ff", nature: "#7dff8a" }', 'ELC = { fire: "#ff7a30", ice: "#9a5cff", light: "#fff0a0", storm: "#5ac8ff", nature: "#7dff8a" }')
    for a, b in NAMES: s = re.sub(r"\b" + a + r"\b", b, s)
    s = re.sub(r"GAME_V = 470\b", "GAME_V = 471", s)
    open(P, 'w').write(s)
