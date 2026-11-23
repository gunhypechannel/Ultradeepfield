import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
js=open('tools/patches/p731_gl.js').read()
rep('function drawBattle(t) {', js+'function drawBattle(t) {')
rep('  if (fxL) { ctx = mainCtx; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = b.expo; ctx.drawImage(fxL, 0, 0); ctx.imageSmoothingEnabled = true;',
    '  if (fxL && bglLight(b, cv, fxL, W, H, busy)) ctx = mainCtx; /* v731 on the GPU */\n  else if (fxL) { bglHide(b); ctx = mainCtx; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = b.expo; ctx.drawImage(fxL, 0, 0); ctx.imageSmoothingEnabled = true;')
rep('    ctx.restore(); ctx.globalAlpha = 1; }\n  /* v76 HDR grade','    ctx.restore(); ctx.globalAlpha = 1; } else bglHide(b);\n  /* v76 HDR grade')
# the clip recorder draws the light layer over the battlefield
rep('try { x.drawImage(cv, (W - dw) / 2, (H - dh) / 2, dw, dh); } catch (e) {} }','try { x.drawImage(cv, (W - dw) / 2, (H - dh) / 2, dw, dh); const gc = battle && battle.gl && battle.gl.c; if (gc && gc.style.visibility !== "hidden") { x.globalCompositeOperation = "lighter"; x.drawImage(gc, (W - dw) / 2, (H - dh) / 2, dw, dh); x.globalCompositeOperation = "source-over"; } } catch (e) {} }')
rep('function battleFree(b) { try {','function battleFree(b) { try { bglFree(b); } catch (e) {} try {')
rep('.battle canvas{position:absolute;inset:0;width:100%;height:100%}','.battle canvas{position:absolute;inset:0;width:100%;height:100%}.battle canvas.bgl{pointer-events:none;mix-blend-mode:plus-lighter}')
open(p,'w').write(s)
