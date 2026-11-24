# Sculpted hulls

Hand-written signed-distance models of the Continuum's ships, made to match the owner's paintings in `docs/art/rwar/`.

    python3 cnt_ark.py /tmp/ark .045             # mesh + bake (needs numpy, scikit-image)
    node pack.js /tmp/ark 40000 ../../docs/art/rwar/m/cnark.bin .02   # simplify + pack (CNT2)

`cntmesh.js` is the loader and material the game uses (copied into `tools/patches/p742_sculpt.js`).
For each new class: add `CNT_SC[k]` (scale into the procedural hull's frame and the engine mouths) and its `.bin`.
