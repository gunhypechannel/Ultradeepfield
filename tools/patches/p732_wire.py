import sys,re
p=sys.argv[1]; s=open(p).read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
i=s.index("/* ---------- v731 the battle's light on the graphics chip"); j=s.index("function bglFree(b) {",i); j=s.index("\n",j)+1
s=s[:i]+open('tools/patches/p732_gl.js').read()+s[j:]
rep('  ctx.setTransform(vs, 0, 0, vs, vtx + shx, vty + shy); ctx.drawImage(b.bg, 0, 0);\n',
    '  if (bglBegin(b, cv, mainCtx, W, H, lo)) { ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); try { bglBackdrop(b, W, H, vs, vtx + shx, vty + shy); } catch (e) { b.glFail = 1; } ctx.setTransform(vs, 0, 0, vs, vtx + shx, vty + shy); } /* v732 the backdrop on the GPU */\n  else { ctx.setTransform(vs, 0, 0, vs, vtx + shx, vty + shy); ctx.drawImage(b.bg, 0, 0); }\n')
rep('if (!b.bg || b.bg.width !== W || b.bg.height !== H) { b.dustL = b.fgL = null; const c = b.bg || (b.bg = document.createElement("canvas")); c.width = W; c.height = H;',
    'if (!b.bg || b.bg.width !== W || b.bg.height !== H) { b.dustL = b.fgL = null; const c = b.bg || (b.bg = document.createElement("canvas")); c.width = W; c.height = H; b.bgV = (b.bgV || 0) + 1;')
rep('  if (fxL) { ctx = fxL.getContext("2d"); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); ctx.setTransform(vs, 0, 0, vs, vtx + shx, vty + shy); }',
    '  if (fxL) { ctx = fxL.getContext("2d"); if (b.glOn) bglHook(ctx, "l"); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); ctx.setTransform(vs, 0, 0, vs, vtx + shx, vty + shy); }')
rep('  if (fxL && bglLight(b, cv, fxL, W, H, busy)) ctx = mainCtx; /* v731 on the GPU */','  if (fxL && b.glOn && bglLight(b, fxL, W, H, busy)) ctx = mainCtx; /* v731 on the GPU */')
rep('if (b.flash > .01 && !reduced) { ctx.save(); ctx.globalCompositeOperation = "lighter";','if (b.glOn) b.glFlash = b.flash > .01 && !reduced ? Math.min(.6, b.flash * .5) : 0; /* v732 the flash is added on the GPU layer */\n  else if (b.flash > .01 && !reduced) { ctx.save(); ctx.globalCompositeOperation = "lighter";')
rep('  if (b.ending) { endingFx(ctx, W, H, d, t, b); if (!b.done && t - b.ending > 2900) finishBattle(); }\n}',
    '  if (b.ending) { endingFx(ctx, W, H, d, t, b); if (!b.done && t - b.ending > 2900) finishBattle(); }\n  if (b.glOn && b.gl) bglFlush(b); /* v732 */\n}')
rep('if (cv && cv.width && cv.height) { const sc = Math.max(W / cv.width, H / cv.height), dw = cv.width * sc, dh = cv.height * sc; try { x.drawImage(cv,',
    'if (cv && cv.width && cv.height) { const sc = Math.max(W / cv.width, H / cv.height), dw = cv.width * sc, dh = cv.height * sc; try { const gu = battle && battle.gl && battle.gl.u && battle.gl.u.c; if (gu && gu.style.visibility !== "hidden") x.drawImage(gu, (W - dw) / 2, (H - dh) / 2, dw, dh); x.drawImage(cv,')
rep('const gc = battle && battle.gl && battle.gl.c;','const gc = battle && battle.gl && battle.gl.o && battle.gl.o.c;')
rep('.battle canvas.bgl{pointer-events:none;mix-blend-mode:plus-lighter}','.battle canvas.bgl{pointer-events:none;mix-blend-mode:plus-lighter}.battle canvas.bgu{pointer-events:none}')
open(p,'w').write(s)
